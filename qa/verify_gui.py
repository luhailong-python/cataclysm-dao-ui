"""Verify live Tk controls with isolated settings and capture actual client pixels.

Run from the project root: python qa/verify_gui.py
World-list screenshots are explicitly disposable QA fixtures, never user saves.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import time
import tkinter as tk
import unittest
from unittest.mock import patch

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.capture import capture_client
from app.domain import Settings, SettingsStore, discover_game_executable
from app.gui import LauncherApp


def settle(root: tk.Tk) -> None:
    root.update_idletasks()
    root.update()
    time.sleep(0.14)
    root.update()


def close_window(root: tk.Tk) -> None:
    # A normal launcher exits its process when Tk closes. The multi-window QA
    # harness stays alive, so cancel this interpreter's pending callbacks first.
    for job in root.tk.splitlist(root.tk.call("after", "info")):
        root.after_cancel(job)
    root.destroy()


def main() -> int:
    if sys.platform == "win32":
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            pass

    qa = PROJECT_ROOT / "qa"
    qa.mkdir(exist_ok=True)
    fixture_parent = PROJECT_ROOT / ".local" / "qa-fixtures"
    fixture_parent.mkdir(parents=True, exist_ok=True)
    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "projectRoot": str(PROJECT_ROOT),
        "environment": {"python": platform.python_version(), "tk": tk.TkVersion, "platform": platform.platform()},
        "captureMethod": "Win32 PrintWindow actual live Tk client area; no image composition",
        "fixturePolicy": "Only .local/qa-fixtures disposable settings and save markers; no user settings or saves changed.",
        "checks": [], "screenshots": [], "callbackErrors": [],
    }

    def check(name: str, condition: bool, details=None) -> None:
        item = {"name": name, "passed": bool(condition)}
        if details is not None:
            item["details"] = details
        report["checks"].append(item)

    def capture(root: tk.Tk, filename: str, note: str) -> None:
        destination = qa / filename
        width, height = capture_client(root, destination)
        with Image.open(destination) as picture:
            actual = picture.size
        report["screenshots"].append({
            "file": str(destination.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "width": width, "height": height, "note": note,
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        })
        check(f"Screenshot pixels match live client: {filename}", actual == (root.winfo_width(), root.winfo_height()))

    def click_button(app: LauncherApp, root: tk.Tk, label: str) -> None:
        item = next(button for button in app.buttons if button["label"] == label)
        x, y, width, height = item["rect"]
        px, py = app._xy(x + width / 2, y + height / 2)
        app.canvas.event_generate("<Motion>", x=round(px), y=round(py))
        app.canvas.event_generate("<Button-1>", x=round(px), y=round(py))
        settle(root)

    with tempfile.TemporaryDirectory(prefix="live-gui-", dir=fixture_parent) as temporary:
        fixture = Path(temporary)
        store = SettingsStore(fixture)
        exe = discover_game_executable(PROJECT_ROOT)
        # An existing fixture .exe only supplies a ready-state when no runtime is present.
        if not exe:
            fake = fixture / "Game program" / "cataclysm-tiles.exe"
            fake.parent.mkdir()
            fake.write_bytes(b"QA fixture, never executed")
            exe = str(fake)
        base_settings = Settings(game_executable=exe, user_directory=str(fixture / "user 空格"))
        store.save(base_settings)

        for width, height in ((1280, 720), (1600, 900), (1920, 1080)):
            root = tk.Tk()
            root.geometry(f"{width}x{height}+0+0")
            if width == root.winfo_screenwidth() and height == root.winfo_screenheight():
                root.attributes("-fullscreen", True)
            errors: list[str] = []
            root.report_callback_exception = lambda kind, value, tb: errors.append(f"{kind.__name__}: {value}")
            with patch("app.gui.SettingsStore", return_value=store):
                app = LauncherApp(root, PROJECT_ROOT)
            settle(root)
            root.lift()
            root.focus_force()
            settle(root)
            check(f"Live client {width}x{height}", (root.winfo_width(), root.winfo_height()) == (width, height))
            for screen in ("home", "continue", "worlds", "settings", "help"):
                app.show_screen(screen)
                settle(root)
                check(f"Screen opens: {screen} at {width}", app.screen_name == screen)
                invalid_buttons = []
                for item in app.buttons:
                    x, y, item_width, item_height = item["rect"]
                    x1, y1, x2, y2 = app._box(x, y, item_width, item_height)
                    if not (0 <= x1 < x2 <= width + 1 and 0 <= y1 < y2 <= height + 1):
                        invalid_buttons.append(item["label"])
                check(f"Buttons stay in client: {screen} at {width}", not invalid_buttons, invalid_buttons)
                outside_fields = [key for key, widget in app.settings_entries.items()
                    if min(widget.winfo_x(), widget.winfo_y()) < 0
                    or widget.winfo_x() + widget.winfo_width() > width
                    or widget.winfo_y() + widget.winfo_height() > height]
                check(f"Native fields stay in client: {screen} at {width}", not outside_fields, outside_fields)
                outside_text = []
                for item in app.canvas.find_all():
                    if app.canvas.type(item) != "text":
                        continue
                    box = app.canvas.bbox(item)
                    if box and (box[0] < -1 or box[1] < -1 or box[2] > width + 1 or box[3] > height + 1):
                        outside_text.append(app.canvas.itemcget(item, "text"))
                check(f"Text stays in client: {screen} at {width}", not outside_text, outside_text)
                if width == 1600 or screen == "home" or (width == 1280 and screen == "settings"):
                    capture(root, f"{screen}-{width}.png", "Empty save directory; actual UI and isolated settings.")
            check(f"No Tk callback errors at {width}", not errors, errors)
            report["callbackErrors"].extend(errors)
            close_window(root)

        # Keep all interaction checks in one visible, live window at 1600x900.
        root = tk.Tk()
        root.geometry("1600x900+0+0")
        with patch("app.gui.SettingsStore", return_value=store):
            app = LauncherApp(root, PROJECT_ROOT)
        settle(root)
        root.focus_force()
        app.canvas.focus_set()
        root.event_generate("<Tab>")
        settle(root)
        check("Tab focuses an enabled home action", app.focus_index >= 0 and app.buttons[app.focus_index]["enabled"])
        app.focus_index = next(index for index, button in enumerate(app.buttons) if button["label"] == "世界存档")
        root.event_generate("<Return>")
        settle(root)
        check("Enter activates the focused world button", app.screen_name == "worlds")
        root.event_generate("<Escape>")
        settle(root)
        check("Escape returns to home", app.screen_name == "home")
        click_button(app, root, "游戏设置")
        check("Canvas click opens settings", app.screen_name == "settings")
        app.settings_entries["game_executable"].focus_set()
        settle(root)
        visited_fields, visited_buttons = set(), set()
        for _ in range(18):
            focused = root.focus_get()
            for key, widget in app.settings_entries.items():
                if focused == widget:
                    visited_fields.add(key)
            if focused == app.canvas and app.focus_index >= 0:
                visited_buttons.add(app.buttons[app.focus_index]["label"])
            root.event_generate("<Tab>")
            settle(root)
        check("Tab traverses all four native settings fields", len(visited_fields) == 4, sorted(visited_fields))
        check("Tab reaches Canvas save action from fields", "保存设置" in visited_buttons, sorted(visited_buttons))
        root.event_generate("<Shift-Tab>")
        settle(root)
        check("Shift-Tab remains in the unified focus chain", root.focus_get() in list(app.settings_entries.values()) + [app.canvas])
        app._settings_vars["text_scale"].set("大字")
        click_button(app, root, "保存设置")
        check("Save action persists native field preferences", store.load().text_scale == "large" and not app.message_error)
        capture(root, "settings-large-1600.png", "Large-text preference saved to disposable isolated store.")
        app._settings_vars["game_executable"].set(str(fixture / "missing.exe"))
        click_button(app, root, "保存设置")
        check("Invalid program path shows an error without overwriting saved settings", app.message_error and store.load().game_executable == exe)
        capture(root, "settings-error-1600.png", "Deliberately nonexistent fixture executable; actual validation error state.")
        app.settings.game_executable = ""
        app.show_screen("home")
        settle(root)
        check("Missing executable disables start and continue", all(not button["enabled"] for button in app.buttons if button["key"] in {"n", "c"}))
        root.event_generate("<KeyPress-n>")
        settle(root)
        check("Start hotkey with no executable opens settings error", app.screen_name == "settings" and app.message_error)

        # Disposable directories reproduce world and pagination state; no save is loadable in the game.
        app.settings.game_executable = exe
        for index in range(6):
            world = Path(app.settings.user_directory) / "save" / f"QA 世界 {index + 1}"
            world.mkdir(parents=True)
            (world / "worldoptions.json").write_text("[]", encoding="utf-8")
            if index < 5:
                (world / "character.sav").write_text("QA fixture; not a real game save", encoding="utf-8")
        app.show_screen("continue")
        settle(root)
        check("Live continue page reads six fixture worlds", len(app.worlds) == 6)
        capture(root, "fixture-worlds-1600.png", "Six explicitly named QA fixture worlds, not user save data.")
        click_button(app, root, "下一页")
        check("World pagination moves to a valid final page", 0 < app.list_offset <= len(app.worlds) - 4)
        empty = next(world for world in app.worlds if world.save_count == 0)
        app._choose_world(empty.name)
        settle(root)
        continue_action = next(button for button in app.buttons if button["label"] == "进入选定世界")
        check("World with no character disables continue action", not continue_action["enabled"])
        close_window(root)
        restored = store.load()
        check("New SettingsStore reloads the saved preference", restored.text_scale == "large")

    suite = unittest.defaultTestLoader.discover(str(PROJECT_ROOT / "tests"))
    stream = io.StringIO()
    unit_result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    report["unitTests"] = {
        "run": unit_result.testsRun, "failures": len(unit_result.failures), "errors": len(unit_result.errors),
        "passed": unit_result.wasSuccessful(), "output": stream.getvalue(),
    }
    report["sourceSha256"] = {str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest()
                              for path in sorted((PROJECT_ROOT / "app").glob("*.py"))}
    report["checksPassed"] = sum(item["passed"] for item in report["checks"])
    report["checksTotal"] = len(report["checks"])
    report["passed"] = all(item["passed"] for item in report["checks"]) and unit_result.wasSuccessful() and not report["callbackErrors"]
    (qa / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("passed", "checksPassed", "checksTotal", "unitTests")}, ensure_ascii=False, indent=2))
    for item in report["checks"]:
        if not item["passed"]:
            print("FAILED", item)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
