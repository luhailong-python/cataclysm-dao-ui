"""Local settings, real save discovery, and process launching.

This module never deletes or rewrites game saves and does not import Tk.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any


@dataclass
class Settings:
    game_executable: str = ""
    user_directory: str = ""
    text_scale: str = "standard"
    window_mode: str = "windowed"


class SettingsStore:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root).resolve()
        self.path = self.project_root / ".local" / "user" / "settings.json"

    def load(self) -> Settings:
        settings = Settings(user_directory=str(self.project_root / ".local" / "game-user"))
        try:
            values = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(values, dict):
                return settings
        except (OSError, ValueError, TypeError):
            return settings
        for key in ("game_executable", "user_directory"):
            value = values.get(key)
            if isinstance(value, str) and "\x00" not in value and value.strip():
                setattr(settings, key, value.strip())
        if isinstance(values.get("text_scale"), str) and values["text_scale"] in {"standard", "large"}:
            settings.text_scale = values["text_scale"]
        if isinstance(values.get("window_mode"), str) and values["window_mode"] in {"windowed", "fullscreen"}:
            settings.window_mode = values["window_mode"]
        return settings

    def save(self, settings: Settings) -> None:
        if not isinstance(settings.text_scale, str) or settings.text_scale not in {"standard", "large"}:
            raise ValueError("文字大小选项无效")
        if not isinstance(settings.window_mode, str) or settings.window_mode not in {"windowed", "fullscreen"}:
            raise ValueError("窗口模式选项无效")
        for value in (settings.game_executable, settings.user_directory):
            if not isinstance(value, str) or "\x00" in value:
                raise ValueError("路径中含有无效字符")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(asdict(settings), ensure_ascii=False, indent=2) + "\n"
        temp_name: str | None = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=self.path.parent,
                                             prefix="settings-", suffix=".tmp", delete=False) as stream:
                temp_name = stream.name
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, self.path)
            temp_name = None
        finally:
            if temp_name:
                try:
                    Path(temp_name).unlink(missing_ok=True)
                except OSError:
                    pass


@dataclass(frozen=True)
class WorldInfo:
    name: str
    path: Path
    save_count: int
    last_played: float


def scan_worlds(user_directory: str | Path) -> list[WorldInfo]:
    """Read real world folders; inaccessible or disappearing entries are skipped."""
    if not str(user_directory).strip():
        return []
    save_root = Path(user_directory).expanduser() / "save"
    try:
        entries = list(save_root.iterdir())
    except (OSError, ValueError):
        return []
    worlds: list[WorldInfo] = []
    for entry in entries:
        try:
            # Avoid following a junction/symlink into an unrelated user directory.
            if entry.is_symlink() or (hasattr(entry, "is_junction") and entry.is_junction()) or not entry.is_dir():
                continue
            files = [item for item in entry.iterdir() if item.is_file()
                     and not item.is_symlink()
                     and (item.name.endswith(".sav") or item.name.endswith(".sav.gz"))]
            if not files and not (entry / "worldoptions.json").is_file():
                continue
            last_played = max((item.stat().st_mtime for item in files), default=entry.stat().st_mtime)
            worlds.append(WorldInfo(entry.name, entry, len(files), last_played))
        except (OSError, ValueError):
            continue
    return sorted(worlds, key=lambda world: (-world.last_played, world.name.casefold()))


def discover_game_executable(project_root: Path) -> str:
    root = Path(project_root)
    names = ("cataclysm-tiles.exe", "cataclysm.exe")
    for folder in (root / ".local" / "runtime", root / ".local" / "game", root / "game"):
        if not folder.is_dir():
            continue
        for name in names:
            for candidate in sorted(folder.rglob(name)):
                if candidate.is_file():
                    return str(candidate.resolve())
    return ""


def build_launch_command(settings: Settings, world: WorldInfo | str | None = None) -> list[str]:
    if not settings.game_executable.strip() or "\x00" in settings.game_executable:
        raise FileNotFoundError("请先在设置中选择游戏程序")
    executable = Path(settings.game_executable).expanduser().resolve()
    if not executable.is_file():
        raise FileNotFoundError("游戏程序不存在，请重新选择")
    if os.name == "nt" and executable.suffix.lower() != ".exe":
        raise ValueError("请选择游戏的 .exe 程序")
    if not settings.user_directory.strip() or "\x00" in settings.user_directory:
        raise ValueError("请选择有效的存档目录")
    userdir = Path(settings.user_directory).expanduser().resolve()
    if userdir.exists() and not userdir.is_dir():
        raise ValueError("存档位置必须是目录")
    command = [str(executable), "--basepath", str(executable.parent) + os.sep,
               "--userdir", str(userdir) + os.sep]
    if world is not None:
        name = world.name if isinstance(world, WorldInfo) else world
        if not isinstance(name, str) or not name or name in {".", ".."} or any(c in name for c in ("/", "\\", "\x00")):
            raise ValueError("世界名称无效")
        selected = next((item for item in scan_worlds(userdir) if item.name == name), None)
        if selected is None or selected.save_count == 0:
            raise ValueError("该世界没有可继续的角色存档，请刷新列表")
        command.extend(["--world", name])
    return command


class GameLauncher:
    def __init__(self):
        self.process: subprocess.Popen[Any] | None = None

    @property
    def running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start(self, settings: Settings, world: WorldInfo | str | None = None) -> subprocess.Popen[Any]:
        if self.running:
            raise RuntimeError("游戏正在运行，请先返回或关闭游戏")
        command = build_launch_command(settings, world)
        user_directory = Path(settings.user_directory).expanduser().resolve()
        user_directory.mkdir(parents=True, exist_ok=True)
        self.process = subprocess.Popen(command, cwd=str(Path(command[0]).parent), shell=False)
        return self.process
