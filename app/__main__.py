"""Run with: python -m app."""
import argparse
from pathlib import Path
import sys
import tkinter as tk

from .capture import capture_client
from .gui import LauncherApp


def main():
    parser = argparse.ArgumentParser(description="Cataclysm: Dark Days Ahead · 道风主题启动界面")
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--screen", choices=("home", "continue", "worlds", "settings", "help"), default="home")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--quit-after", type=int, default=0, metavar="MILLISECONDS")
    args = parser.parse_args()
    if args.width < 1040 or args.height < 640:
        parser.error("窗口至少为 1040×640")
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            pass
    root = tk.Tk()
    fullscreen_capture = bool(args.screenshot and args.width == root.winfo_screenwidth()
                              and args.height == root.winfo_screenheight())
    width = min(args.width, root.winfo_screenwidth() if fullscreen_capture else root.winfo_screenwidth() - 32)
    height = min(args.height, root.winfo_screenheight() if fullscreen_capture else root.winfo_screenheight() - 80)
    root.geometry(f"{width}x{height}+16+16")
    project_root = Path(__file__).resolve().parents[1]
    app = LauncherApp(root, project_root)
    if fullscreen_capture:
        root.attributes("-fullscreen", True)
    root.after(160, lambda: app.show_screen(args.screen))
    if args.screenshot:
        def capture():
            root.update_idletasks()
            capture_client(root, args.screenshot)
            print(f"Screenshot: {args.screenshot.resolve()}", flush=True)
        root.after(1200, capture)
    if args.quit_after:
        root.after(max(args.quit_after, 1400 if args.screenshot else 0), root.destroy)
    root.mainloop()


if __name__ == "__main__":
    main()
