"""Native Tk desktop interface. Text and controls remain separate from artwork."""
from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import subprocess
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, ttk
from typing import Callable

from PIL import Image, ImageEnhance, ImageTk

from .domain import (GameLauncher, Settings, SettingsStore, WorldInfo,
                     discover_game_executable, scan_worlds)


JADE = "#224f43"
DARK = "#183e35"
GOLD = "#aa8748"
PAPER = "#f7efdc"
MUTED = "#697267"
RED = "#a14d3c"
FONT = "Microsoft YaHei UI"
SLICES = {
    "main_frame": (76, 79, 76, 79),
    "title_plate": (142, 29, 142, 35),
    "section_plate": (76, 16, 72, 21),
    "member_row": (24, 19, 24, 19),
    "button_primary": (45, 16, 45, 16),
    "button_secondary": (45, 16, 45, 16),
}


class LauncherApp:
    DESIGN_W, DESIGN_H = 1920, 1080

    def __init__(self, root: tk.Tk, project_root: Path):
        self.root = root
        self.project_root = Path(project_root).resolve()
        self.store = SettingsStore(self.project_root)
        self.settings = self.store.load()
        if not self.settings.game_executable or not Path(self.settings.game_executable).is_file():
            discovered = discover_game_executable(self.project_root)
            if discovered:
                self.settings.game_executable = discovered
        self.launcher = GameLauncher()
        self.screen_name = "home"
        self.worlds: list[WorldInfo] = []
        self.selected_world: str | None = None
        self.list_offset = 0
        self.buttons: list[dict] = []
        self.focus_index = -1
        self.message = ""
        self.message_error = False
        self._resize_job = None
        self._images: list[ImageTk.PhotoImage] = []
        self._originals: dict[str, Image.Image] = {}
        self._skin_cache: dict[tuple, Image.Image] = {}
        self._widgets: list[tk.Widget] = []
        self._settings_vars: dict[str, tk.StringVar] = {}
        self.settings_entries: dict[str, ttk.Entry | ttk.Combobox] = {}
        self.scale, self.ox, self.oy = 1.0, 0.0, 0.0
        self.root.title("Cataclysm: Dark Days Ahead · 道风主题")
        self.root.minsize(1040, 640)
        self.root.configure(bg="#d8e1d4")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.canvas = tk.Canvas(root, bg="#d8e1d4", highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._resize)
        self.canvas.bind("<MouseWheel>", self._scroll)
        self.root.bind("<Tab>", self._tab)
        self.root.bind("<Shift-Tab>", lambda event: self._tab(event, -1))
        self.root.bind("<Return>", self._enter)
        self.root.bind("<Escape>", self._escape)
        self.root.bind("<F1>", lambda event: self.show_screen("help"))
        self.root.bind("<F5>", lambda event: self.refresh())
        self.root.bind("<F11>", self._fullscreen)
        self.root.bind("<Control-s>", self._save_shortcut)
        self.root.bind("<Control-S>", self._save_shortcut)
        self.root.bind("<Up>", lambda event: self._move_world(-1))
        self.root.bind("<Down>", lambda event: self._move_world(1))
        self.root.bind("<KeyPress>", self._hotkey, add=True)
        self.root.after(100, self.render)
        self.root.after(700, self._poll_game)
        if self.settings.window_mode == "fullscreen":
            self.root.attributes("-fullscreen", True)

    def _resize(self, _event=None):
        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(80, self.render)

    def _poll_game(self):
        if not self.root.winfo_exists():
            return
        if self.launcher.process is not None and not self.launcher.running:
            code = self.launcher.process.returncode
            self.launcher.process = None
            self.refresh()
            self.notify("已返回旅程入口" if code == 0 else f"游戏已结束运行（返回码 {code}）", code != 0)
        self.root.after(700, self._poll_game)

    def _xy(self, x: float, y: float):
        return self.ox + x * self.scale, self.oy + y * self.scale

    def _box(self, x: float, y: float, w: float, h: float):
        a, b = self._xy(x, y)
        return a, b, a + w * self.scale, b + h * self.scale

    def text(self, x, y, value, size=22, color=DARK, anchor="nw", width=None,
             bold=False, align="left", tags=()):
        return self.canvas.create_text(*self._xy(x, y), text=value,
            font=(FONT, max(10, round(size * self.scale * (1.12 if self.settings.text_scale == "large" else 1))),
                  "bold" if bold else "normal"), fill=color, anchor=anchor,
            width=None if width is None else width * self.scale, justify=align, tags=tags)

    def _single_line(self, value: str, size: int, max_width: int, bold=False) -> str:
        font = tkfont.Font(self.root, family=FONT,
            size=max(10, round(size * self.scale * (1.12 if self.settings.text_scale == "large" else 1))),
            weight="bold" if bold else "normal")
        if font.measure(value) <= max_width * self.scale:
            return value
        while value and font.measure(value + "…") > max_width * self.scale:
            value = value[:-1]
        return value + "…"

    def _load(self, name: str) -> Image.Image | None:
        if name not in self._originals:
            file = self.project_root / "assets" / "ui" / f"{name}.png"
            if not file.is_file():
                return None
            with Image.open(file) as image:
                self._originals[name] = image.convert("RGBA")
        return self._originals[name]

    def skin(self, name, x, y, w, h, disabled=False, tags=()):
        original = self._load(name)
        tw, th = max(1, round(w * self.scale)), max(1, round(h * self.scale))
        if original is None:
            # A plain native surface while optional artwork is not installed.
            return self.canvas.create_rectangle(*self._box(x, y, w, h), fill=PAPER,
                outline=GOLD, width=max(1, self.scale), tags=tags)
        key = (name, tw, th, disabled)
        if key not in self._skin_cache:
            if name in SLICES:
                left, bottom, right, top = SLICES[name]
                sw, sh = original.size
                k = min(self.scale, tw / (left + right + 1), th / (top + bottom + 1))
                dl, dr, dt, db = (max(1, round(value * k)) for value in (left, right, top, bottom))
                source_x, source_y = (0, left, sw - right, sw), (0, top, sh - bottom, sh)
                target_x, target_y = (0, dl, tw - dr, tw), (0, dt, th - db, th)
                result = Image.new("RGBA", (tw, th))
                for col in range(3):
                    for row in range(3):
                        patch = original.crop((source_x[col], source_y[row], source_x[col + 1], source_y[row + 1]))
                        size = (target_x[col + 1] - target_x[col], target_y[row + 1] - target_y[row])
                        if min(size) > 0:
                            result.alpha_composite(patch.resize(size, Image.Resampling.LANCZOS), (target_x[col], target_y[row]))
            else:
                result = original.resize((tw, th), Image.Resampling.LANCZOS)
            if disabled:
                alpha = result.getchannel("A")
                result = ImageEnhance.Color(result).enhance(.18)
                result.putalpha(alpha.point(lambda value: int(value * .65)))
            self._skin_cache[key] = result
        photo = ImageTk.PhotoImage(self._skin_cache[key], master=self.root)
        self._images.append(photo)
        return self.canvas.create_image(*self._xy(x, y), image=photo, anchor="nw", tags=tags)

    def button(self, label: str, x: float, y: float, w: float, h: float,
               callback: Callable, primary=False, enabled=True, key=None):
        tag = f"button-{len(self.buttons)}"
        button = {"label": label, "rect": (x, y, w, h), "tag": tag,
                  "enabled": enabled, "callback": callback, "key": key}
        self.buttons.append(button)
        self.skin("button_primary" if primary else "button_secondary", x, y, w, h, not enabled, (tag,))
        self.text(x + w / 2, y + h / 2 - 1, label, size=25 if h >= 75 else 21,
                  color=("#fff6d9" if primary and enabled else DARK if enabled else "#8d9187"),
                  anchor="center", bold=primary, tags=(tag,))
        self.canvas.tag_bind(tag, "<Button-1>", lambda event, item=button: self._activate(item))
        self.canvas.tag_bind(tag, "<Enter>", lambda event, active=enabled: self.canvas.configure(cursor="hand2" if active else "arrow"))
        self.canvas.tag_bind(tag, "<Leave>", lambda event: self.canvas.configure(cursor="arrow"))

    def _activate(self, button):
        if button["enabled"]:
            self.canvas.focus_set()
            button["callback"]()

    def _tab(self, event=None, direction=1):
        sequence = [("button", index) for index, button in enumerate(self.buttons) if button["enabled"]]
        if self.screen_name == "settings" and self.settings_entries:
            button_keys = {button.get("key"): index for index, button in enumerate(self.buttons) if button["enabled"] and button.get("key")}
            form_buttons = set(button_keys.values())
            sequence = [("button", index) for index, button in enumerate(self.buttons)
                        if button["enabled"] and index not in form_buttons]
            for kind, value in (("widget", "game_executable"), ("button", "browse-game"),
                                ("widget", "user_directory"), ("button", "browse-userdir"),
                                ("widget", "text_scale"), ("widget", "window_mode"),
                                ("button", "save-settings")):
                if kind == "widget":
                    sequence.append((kind, self.settings_entries[value]))
                elif value in button_keys:
                    sequence.append((kind, button_keys[value]))
        origin_widget = event.widget if event is not None else self.root.focus_get()
        origin = ("widget", origin_widget) if origin_widget in self.settings_entries.values() else ("button", self.focus_index)
        if sequence:
            current = sequence.index(origin) if origin in sequence else (-1 if direction > 0 else 0)
            kind, value = sequence[(current + direction) % len(sequence)]
            if kind == "widget":
                self.focus_index = -1
                value.focus_set()
            else:
                self.focus_index = value
                self.canvas.focus_set()
            self._draw_focus()
        return "break"

    def _save_shortcut(self, event=None):
        if self.screen_name == "settings":
            self._save_settings()
        else:
            self.show_screen("settings")
        return "break"

    def _draw_focus(self):
        self.canvas.delete("keyboard-focus")
        if 0 <= self.focus_index < len(self.buttons) and self.buttons[self.focus_index]["enabled"]:
            x, y, w, h = self.buttons[self.focus_index]["rect"]
            self.canvas.create_rectangle(*self._box(x + 12, y + 8, w - 24, h - 16),
                outline="#d2a043", width=max(2, 2 * self.scale), dash=(4, 3), tags="keyboard-focus")

    def _enter(self, event=None):
        if isinstance(self.root.focus_get(), (ttk.Entry, ttk.Combobox)):
            return None
        if 0 <= self.focus_index < len(self.buttons):
            self._activate(self.buttons[self.focus_index])
        return "break"

    def _escape(self, event=None):
        if self.screen_name != "home":
            self.show_screen("home")
        return "break"

    def _hotkey(self, event):
        if isinstance(self.root.focus_get(), (ttk.Entry, ttk.Combobox)):
            return
        if event.state & (0x4 | 0x8):
            return
        key = event.keysym.lower()
        if key == "n":
            self.launch_game()
        elif key in {"c", "w", "s"}:
            self.show_screen({"c": "continue", "w": "worlds", "s": "settings"}[key])

    def _fullscreen(self, event=None):
        active = not bool(self.root.attributes("-fullscreen"))
        self.root.attributes("-fullscreen", active)
        return "break"

    def _scroll(self, event):
        if self.screen_name in {"continue", "worlds"} and len(self.worlds) > 4:
            self.list_offset = max(0, min(len(self.worlds) - 4, self.list_offset + (-1 if event.delta > 0 else 1)))
            self.render()

    def show_screen(self, name: str):
        if name not in {"home", "continue", "worlds", "settings", "help"}:
            raise ValueError(f"Unknown screen: {name}")
        if name != self.screen_name:
            self.list_offset = 0
            self.focus_index = -1
            self.message = ""
        self.screen_name = name
        if name == "settings":
            self._settings_vars = {
                "game_executable": tk.StringVar(self.root, self.settings.game_executable),
                "user_directory": tk.StringVar(self.root, self.settings.user_directory),
                "text_scale": tk.StringVar(self.root, "大字" if self.settings.text_scale == "large" else "标准"),
                "window_mode": tk.StringVar(self.root, "全屏" if self.settings.window_mode == "fullscreen" else "窗口"),
            }
        self.refresh()

    def refresh(self):
        self.worlds = scan_worlds(self.settings.user_directory)
        if self.selected_world not in {world.name for world in self.worlds}:
            playable = next((world for world in self.worlds if world.save_count), None)
            self.selected_world = playable.name if playable else self.worlds[0].name if self.worlds else None
        self.list_offset = max(0, min(self.list_offset, max(0, len(self.worlds) - 4)))
        self.render()

    def _game_ready(self):
        return bool(self.settings.game_executable and Path(self.settings.game_executable).is_file())

    def _selected(self) -> WorldInfo | None:
        return next((world for world in self.worlds if world.name == self.selected_world), None)

    def render(self):
        self._resize_job = None
        width, height = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        if width < 10 or height < 10:
            return
        self.scale = min(width / self.DESIGN_W, height / self.DESIGN_H)
        self.ox, self.oy = (width - self.DESIGN_W * self.scale) / 2, (height - self.DESIGN_H * self.scale) / 2
        self.canvas.delete("all")
        self._images.clear()
        for widget in self._widgets:
            widget.destroy()
        self._widgets.clear()
        self.settings_entries = {}
        self.buttons = []
        self._background(width, height)
        self._brand()
        if self.screen_name == "home":
            self._home()
        else:
            self._navigation()
            self.skin("member_row", 480, 180, 1340, 785)
            titles = {"continue": ("继续旅程", "选择一处熟悉的世界，再次出发"),
                      "worlds": ("世界与存档", "每一段旅程，都保存在本地"),
                      "settings": ("旅程设置", "选择游戏位置，让下一次启程更从容"),
                      "help": ("行前手记", "关于启程、存档与操作")}
            heading, subtitle = titles[self.screen_name]
            self.skin("title_plate", 880, 145, 560, 112)
            self.text(1160, 199, heading, size=32, color="#fff4d5", anchor="center", bold=True)
            self.text(555, 290, subtitle, size=22, color=MUTED)
            if self.screen_name in {"continue", "worlds"}:
                self._world_page()
            elif self.screen_name == "settings":
                self._settings_page()
            else:
                self._help_page()
        self._footer()
        self._draw_focus()

    def _background(self, width, height):
        file = self.project_root / "assets" / "art" / "survivor-keyart.png"
        if file.is_file():
            if "_background" not in self._originals:
                with Image.open(file) as picture:
                    self._originals["_background"] = picture.convert("RGB")
            original = self._originals["_background"]
            ratio = max(width / original.width, height / original.height)
            fitted = original.resize((round(original.width * ratio), round(original.height * ratio)), Image.Resampling.LANCZOS)
            left, top = (fitted.width - width) // 2, (fitted.height - height) // 2
            fitted = fitted.crop((left, top, left + width, top + height))
            photo = ImageTk.PhotoImage(fitted, master=self.root)
            self._images.append(photo)
            self.canvas.create_image(0, 0, image=photo, anchor="nw")
        else:
            self.canvas.create_rectangle(0, 0, width, height, fill="#d9e7da", outline="")

    def _brand(self):
        self.skin("member_row", 66, 51, 730, 207)
        self.text(95, 78, "C A T A C L Y S M", size=41, bold=True, color="#214c41")
        self.text(98, 139, "DARK DAYS AHEAD", size=25, color="#426858")
        self.canvas.create_line(*self._xy(100, 190), *self._xy(395, 190), fill=GOLD, width=max(1, 2 * self.scale))
        self.text(100, 211, "道风主题 · 旅途未尽", size=21, color="#5c6e5f")

    def _home(self):
        self.skin("member_row", 1060, 185, 760, 780)
        self.skin("title_plate", 1165, 145, 550, 115)
        self.text(1440, 201, "新的黎明", size=34, color="#fff4d5", anchor="center", bold=True)
        self.text(1440, 317, "世界已经改变。\n旅途，仍在继续。", size=29, anchor="center", align="center", bold=True)
        self.text(1440, 410, "收拾行囊，寻找下一个安身之处。", size=20, anchor="center", color=MUTED)
        ready, running = self._game_ready(), self.launcher.running
        self.button("开始游戏   N", 1175, 470, 530, 98, self.launch_game, True, ready and not running, "n")
        self.button("继续旅程   C", 1175, 585, 530, 94,
                    lambda: self.show_screen("continue"), enabled=ready and not running, key="c")
        if running:
            state = "游戏正在运行，旅程入口将留在这里。"
        elif not ready:
            state = "尚未找到游戏程序，请在设置中选择。"
        else:
            self.worlds = scan_worlds(self.settings.user_directory)
            count = sum(world.save_count for world in self.worlds)
            state = f"已连接本地游戏 · {len(self.worlds)} 个世界 · {count} 份角色存档"
        self.text(1440, 710, state, size=19, color=MUTED, anchor="center", width=590, align="center")
        self.button("游戏设置", 1175, 772, 255, 73, lambda: self.show_screen("settings"))
        self.button("世界存档", 1450, 772, 255, 73, lambda: self.show_screen("worlds"))
        self.button("行前手记   F1", 1275, 867, 330, 58, lambda: self.show_screen("help"))

    def _navigation(self):
        pages = [("home", "旅程入口"), ("continue", "继续旅程"),
                 ("worlds", "世界存档"), ("settings", "游戏设置"), ("help", "行前手记")]
        for index, (name, label) in enumerate(pages):
            self.button(label, 95, 355 + index * 99, 300, 78,
                        lambda target=name: self.show_screen(target), primary=self.screen_name == name)

    def _world_page(self):
        self.text(1500, 305, f"{len(self.worlds)} 个世界", size=20, color=MUTED, anchor="ne")
        if not self.worlds:
            self.skin("section_plate", 875, 390, 550, 80)
            self.text(1150, 430, "还没有留下足迹", size=27, color="#fff3d3", anchor="center", bold=True)
            self.text(1150, 545, "这个存档目录里，尚未发现世界。", size=25, anchor="center")
            self.text(1150, 603, "开始游戏创建旅程，或在设置中选择已有的用户目录。", size=20,
                      anchor="center", color=MUTED, width=1000, align="center")
            self.button("前往游戏设置", 940, 700, 420, 82, lambda: self.show_screen("settings"), True)
        else:
            for index, world in enumerate(self.worlds[self.list_offset:self.list_offset + 4]):
                self._world_row(world, 352 + index * 108)
            if len(self.worlds) > 4:
                self.button("上一页", 565, 798, 175, 58, lambda: self._page(-4), enabled=self.list_offset > 0)
                end = min(self.list_offset + 4, len(self.worlds))
                self.text(835, 828, f"{self.list_offset + 1}—{end} / {len(self.worlds)}", size=18, anchor="center", color=MUTED)
                self.button("下一页", 930, 798, 175, 58, lambda: self._page(4), enabled=end < len(self.worlds))
            selected = self._selected()
            if self.screen_name == "continue":
                enabled = self._game_ready() and selected is not None and selected.save_count > 0 and not self.launcher.running
                self.button("进入选定世界", 1240, 823, 465, 82, lambda: self.launch_game(self._selected()), True, enabled)
                self.text(580, 910, "将读取该世界的首个角色存档；其他角色可在游戏内选择。", size=18, color=MUTED, width=1080)
            else:
                self.button("打开世界文件夹", 1240, 823, 465, 82,
                            lambda: self._open_folder(self._selected().path if self._selected() else None),
                            True, selected is not None)
                self.text(580, 910, "存档由游戏维护；这里仅查看和打开文件夹。", size=18, color=MUTED, width=1050)
        self.button("刷新   F5", 1540, 280, 220, 58, self.refresh)

    def _world_row(self, world: WorldInfo, y):
        tag = f"world-{y}"
        self.skin("member_row", 555, y, 1190, 98, tags=(tag,))
        selected = world.name == self.selected_world
        if selected:
            self.canvas.create_rectangle(*self._box(565, y + 8, 1170, 81), outline="#ac8c46", width=max(1, 2 * self.scale), tags=(tag,))
        self.text(595, y + 18, self._single_line(world.name, 25, 780, True), size=25, bold=True, tags=(tag,))
        timestamp = datetime.fromtimestamp(world.last_played).strftime("%Y.%m.%d  %H:%M")
        self.text(595, y + 57, f"最近存档  {timestamp}", size=17, color=MUTED, tags=(tag,))
        self.text(1695, y + 48, f"{world.save_count} 份角色存档" if world.save_count else "尚无角色存档",
                  size=21, color=JADE if world.save_count else MUTED, anchor="e", tags=(tag,))
        self.canvas.tag_bind(tag, "<Button-1>", lambda event, name=world.name: self._choose_world(name))

    def _choose_world(self, name):
        self.selected_world = name
        self.render()

    def _move_world(self, direction):
        if self.screen_name not in {"continue", "worlds"} or not self.worlds:
            return None
        names = [world.name for world in self.worlds]
        index = names.index(self.selected_world) if self.selected_world in names else 0
        index = max(0, min(len(names) - 1, index + direction))
        self.selected_world = names[index]
        if index < self.list_offset:
            self.list_offset = index
        elif index >= self.list_offset + 4:
            self.list_offset = index - 3
        self.render()
        return "break"

    def _page(self, delta):
        self.list_offset = max(0, min(max(0, len(self.worlds) - 4), self.list_offset + delta))
        self.render()

    def _field(self, key, x, y, w, h=52, choices=None):
        if key not in self._settings_vars:
            self._settings_vars[key] = tk.StringVar(self.root)
        options = dict(textvariable=self._settings_vars[key], font=(FONT, max(12, round(21 * self.scale))))
        if choices:
            widget = ttk.Combobox(self.root, values=choices, state="readonly", **options)
        else:
            widget = ttk.Entry(self.root, **options)
        ax, ay = self._xy(x, y)
        widget.place(x=ax, y=ay, width=w * self.scale, height=h * self.scale)
        self._widgets.append(widget)
        self.settings_entries[key] = widget
        # Widget bindings run before ttk's native focus traversal.
        widget.bind("<Tab>", self._tab)
        widget.bind("<Shift-Tab>", lambda event: self._tab(event, -1))

    def _settings_page(self):
        if not self._settings_vars:
            self._settings_vars = {
                "game_executable": tk.StringVar(self.root, self.settings.game_executable),
                "user_directory": tk.StringVar(self.root, self.settings.user_directory),
                "text_scale": tk.StringVar(self.root, "大字" if self.settings.text_scale == "large" else "标准"),
                "window_mode": tk.StringVar(self.root, "全屏" if self.settings.window_mode == "fullscreen" else "窗口")}
        self.text(580, 365, "游戏程序", size=23, bold=True)
        self._field("game_executable", 580, 410, 905)
        self.button("浏览…", 1510, 402, 210, 68, self._browse_game, key="browse-game")
        self.text(580, 483, "选择 Cataclysm: Dark Days Ahead 的游戏程序。", size=18, color=MUTED)
        self.text(580, 545, "用户与存档目录", size=23, bold=True)
        self._field("user_directory", 580, 590, 905)
        self.button("浏览…", 1510, 582, 210, 68, self._browse_userdir, key="browse-userdir")
        self.text(580, 662, "选择包含 save 文件夹的用户目录；已有存档会保留。", size=18, color=MUTED)
        self.text(580, 724, "界面文字", size=22, bold=True)
        self._field("text_scale", 760, 714, 250, choices=("标准", "大字"))
        self.text(1110, 724, "启动界面窗口", size=22, bold=True)
        self._field("window_mode", 1390, 714, 315, choices=("窗口", "全屏"))
        self.button("保存设置", 1260, 820, 445, 85, self._save_settings, True, key="save-settings")
        self.text(580, 848, "设置只影响此启动界面与游戏启动位置。", size=18, color=MUTED, width=610)

    def _browse_game(self):
        filename = filedialog.askopenfilename(parent=self.root, title="选择游戏程序",
            filetypes=(("游戏程序", "*.exe"), ("所有文件", "*.*")),
            initialdir=str(self.project_root / ".local" / "runtime"))
        if filename:
            self._settings_vars["game_executable"].set(filename)

    def _browse_userdir(self):
        folder = filedialog.askdirectory(parent=self.root, title="选择包含 save 的用户目录",
            initialdir=self._settings_vars["user_directory"].get() or str(self.project_root), mustexist=True)
        if folder:
            self._settings_vars["user_directory"].set(folder)

    def _save_settings(self):
        candidate = Settings(
            game_executable=self._settings_vars["game_executable"].get().strip(),
            user_directory=self._settings_vars["user_directory"].get().strip(),
            text_scale="large" if self._settings_vars["text_scale"].get() == "大字" else "standard",
            window_mode="fullscreen" if self._settings_vars["window_mode"].get() == "全屏" else "windowed")
        if candidate.game_executable and not Path(candidate.game_executable).is_file():
            self.notify("未找到所选游戏程序，设置尚未保存。", True)
            return
        if not candidate.user_directory or (Path(candidate.user_directory).exists() and not Path(candidate.user_directory).is_dir()):
            self.notify("请选择有效的用户目录，设置尚未保存。", True)
            return
        try:
            self.store.save(candidate)
        except (OSError, ValueError) as error:
            self.notify(f"无法保存设置：{error}", True)
            return
        self.settings = candidate
        self.root.attributes("-fullscreen", candidate.window_mode == "fullscreen")
        self.refresh()
        self.notify("设置已保存，下次打开会继续沿用。")

    def _help_page(self):
        sections = [
            ("01  启程", "“开始游戏”打开游戏主菜单。在游戏中创建世界、人物并开始旅程。"),
            ("02  继续旅程", "列表读取所选用户目录中的真实存档。进入世界时读取首个角色存档；其他角色可在游戏内选择。"),
            ("03  保存你的旅途", "游戏会维护存档内容。此界面可查看世界和打开文件夹，不删除、改写或伪造存档。"),
            ("04  操作随手记", "N 开始游戏　C 继续旅程　W 世界存档　S 设置\nTab 切换控件　Enter 确认　Ctrl+S 保存设置　Esc 返回　F5 刷新　F11 全屏"),
        ]
        for index, (heading, body) in enumerate(sections):
            y = 355 + index * 135
            self.text(585, y, heading, size=23, bold=True)
            self.text(585, y + 45, body, size=20, color=MUTED, width=1120)
        self.text(585, 914, "游戏内的画面、规则及角色操作仍由 Cataclysm: Dark Days Ahead 提供。", size=18, color=MUTED, width=1120)

    def _footer(self):
        self.skin("member_row", 70, 990, 1750, 65)
        self.text(100, 1018, "CATACLYSM: DARK DAYS AHEAD", size=15, color="#4c685a")
        if self.message:
            self.text(1800, 1020, self._single_line(self.message, 18, 1150), size=18,
                      color=RED if self.message_error else JADE, anchor="ne")
        else:
            self.text(1800, 1020, "F1 行前手记    ·    F11 全屏", size=17, color="#4c685a", anchor="ne")

    def notify(self, message: str, error=False):
        self.message, self.message_error = message, error
        self.render()

    def launch_game(self, world: WorldInfo | None = None):
        if not self._game_ready():
            self.show_screen("settings")
            self.notify("请先选择本地游戏程序。", True)
            return
        try:
            self.store.save(self.settings)
            self.launcher.start(self.settings, world)
        except (OSError, ValueError, RuntimeError) as error:
            self.notify(f"无法启程：{error}", True)
            return
        self.notify("游戏已启动，愿旅途平安。")

    def _open_folder(self, path: Path | None):
        if path is None or not path.is_dir():
            self.notify("文件夹已不存在，请刷新列表。", True)
            return
        try:
            if os.name == "nt":
                os.startfile(str(path))
            else:
                subprocess.Popen(["xdg-open", str(path)], shell=False)
        except OSError as error:
            self.notify(f"无法打开文件夹：{error}", True)
