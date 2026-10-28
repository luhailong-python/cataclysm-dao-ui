"""Capture this application's client area without unrelated desktop overlays."""
from pathlib import Path
import sys

from PIL import Image, ImageGrab


def capture_client(root, destination: Path) -> tuple[int, int]:
    root.update_idletasks()
    if sys.platform == "win32":
        image = _capture_windows(root.winfo_id())
    else:
        x, y = root.winfo_rootx(), root.winfo_rooty()
        image = ImageGrab.grab(bbox=(x, y, x + root.winfo_width(), y + root.winfo_height()), all_screens=True)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)
    return image.size


def _capture_windows(hwnd: int) -> Image.Image:
    import ctypes
    from ctypes import wintypes
    user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32
    user32.GetDC.argtypes = [wintypes.HWND]
    user32.GetDC.restype = wintypes.HDC
    user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
    user32.PrintWindow.argtypes = [wintypes.HWND, wintypes.HDC, wintypes.UINT]
    user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    gdi32.CreateCompatibleDC.argtypes = [wintypes.HDC]
    gdi32.CreateCompatibleDC.restype = wintypes.HDC
    gdi32.CreateCompatibleBitmap.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int]
    gdi32.CreateCompatibleBitmap.restype = wintypes.HBITMAP
    gdi32.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
    gdi32.SelectObject.restype = wintypes.HGDIOBJ
    gdi32.DeleteObject.argtypes = [wintypes.HGDIOBJ]
    gdi32.DeleteDC.argtypes = [wintypes.HDC]

    class Header(ctypes.Structure):
        _fields_ = [("size", wintypes.DWORD), ("width", wintypes.LONG), ("height", wintypes.LONG),
                    ("planes", wintypes.WORD), ("bit_count", wintypes.WORD), ("compression", wintypes.DWORD),
                    ("size_image", wintypes.DWORD), ("x", wintypes.LONG), ("y", wintypes.LONG),
                    ("colors_used", wintypes.DWORD), ("colors_important", wintypes.DWORD)]

    class BitmapInfo(ctypes.Structure):
        _fields_ = [("header", Header), ("colors", wintypes.DWORD * 3)]

    gdi32.GetDIBits.argtypes = [wintypes.HDC, wintypes.HBITMAP, wintypes.UINT, wintypes.UINT,
                               ctypes.c_void_p, ctypes.POINTER(BitmapInfo), wintypes.UINT]
    bounds = wintypes.RECT()
    if not user32.GetClientRect(hwnd, ctypes.byref(bounds)):
        raise OSError("Unable to obtain launcher client area")
    width, height = bounds.right - bounds.left, bounds.bottom - bounds.top
    source = user32.GetDC(hwnd)
    memory = gdi32.CreateCompatibleDC(source)
    bitmap = gdi32.CreateCompatibleBitmap(source, width, height)
    old = gdi32.SelectObject(memory, bitmap)
    try:
        if not user32.PrintWindow(hwnd, memory, 3):
            raise OSError("Unable to render launcher client area")
        info = BitmapInfo()
        info.header.size = ctypes.sizeof(Header)
        info.header.width, info.header.height = width, -height
        info.header.planes, info.header.bit_count = 1, 32
        buffer = ctypes.create_string_buffer(width * height * 4)
        if gdi32.GetDIBits(memory, bitmap, 0, height, buffer, ctypes.byref(info), 0) != height:
            raise OSError("Unable to read launcher screenshot pixels")
        return Image.frombuffer("RGB", (width, height), bytes(buffer), "raw", "BGRX", 0, 1)
    finally:
        gdi32.SelectObject(memory, old)
        gdi32.DeleteObject(bitmap)
        gdi32.DeleteDC(memory)
        user32.ReleaseDC(hwnd, source)
