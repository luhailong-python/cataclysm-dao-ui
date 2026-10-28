"""Behavior checks against disposable, real on-disk game/user directories."""
from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from app.domain import (
    GameLauncher,
    Settings,
    SettingsStore,
    build_launch_command,
    discover_game_executable,
    scan_worlds,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DomainBehaviorTests(unittest.TestCase):
    def setUp(self) -> None:
        fixture_parent = PROJECT_ROOT / ".local" / "qa-fixtures"
        fixture_parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="domain-", dir=fixture_parent)
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def executable(self) -> Path:
        game = self.root / "游戏 program & symbols" / "cataclysm-tiles.exe"
        game.parent.mkdir(parents=True, exist_ok=True)
        game.write_bytes(b"QA fixture: never execute this file")
        return game

    def settings(self) -> Settings:
        return Settings(
            game_executable=str(self.executable()),
            user_directory=str(self.root / "存档 folder & symbols"),
        )

    def world(self, userdir: Path, name: str, *, saves: tuple[str, ...] = (), timestamp: float = 1000) -> Path:
        world = userdir / "save" / name
        world.mkdir(parents=True)
        (world / "worldoptions.json").write_text("[]", encoding="utf-8")
        for filename in saves:
            save = world / filename
            save.write_text("# QA-only save fixture", encoding="utf-8")
            os.utime(save, (timestamp, timestamp))
        os.utime(world, (timestamp, timestamp))
        return world

    def test_missing_or_corrupt_settings_restore_safe_project_local_defaults(self) -> None:
        store = SettingsStore(self.root)
        first = store.load()
        self.assertEqual(first.game_executable, "")
        self.assertEqual(Path(first.user_directory), self.root / ".local" / "game-user")
        store.path.parent.mkdir(parents=True)
        store.path.write_text('{"user_directory": ', encoding="utf-8")
        self.assertEqual(store.load(), first)
        self.assertEqual(store.path.read_text(encoding="utf-8"), '{"user_directory": ')

    def test_settings_round_trip_unicode_and_user_preferences_without_temp_residue(self) -> None:
        settings = self.settings()
        settings.text_scale = "large"
        settings.window_mode = "fullscreen"
        store = SettingsStore(self.root)
        store.save(settings)
        self.assertEqual(store.load(), settings)
        self.assertEqual(json.loads(store.path.read_text(encoding="utf-8")), asdict(settings))
        self.assertEqual(list(store.path.parent.glob("settings-*.tmp")), [])

    def test_unknown_setting_options_and_nul_paths_do_not_reach_ui(self) -> None:
        store = SettingsStore(self.root)
        store.path.parent.mkdir(parents=True)
        store.path.write_text(json.dumps({
            "game_executable": "bad\u0000path", "user_directory": [],
            "text_scale": "gigantic", "window_mode": "other", "unknown": True,
        }), encoding="utf-8")
        loaded = store.load()
        self.assertEqual(loaded.text_scale, "standard")
        self.assertEqual(loaded.window_mode, "windowed")
        self.assertEqual(loaded.game_executable, "")
        self.assertEqual(Path(loaded.user_directory), self.root / ".local" / "game-user")

    def test_invalid_save_does_not_destroy_previous_valid_settings(self) -> None:
        store = SettingsStore(self.root)
        settings = self.settings()
        store.save(settings)
        previous = store.path.read_bytes()
        settings.window_mode = "unrecognized"
        with self.assertRaises(ValueError):
            store.save(settings)
        self.assertEqual(store.path.read_bytes(), previous)

    def test_valid_json_with_wrong_option_value_types_recovers_without_crashing(self) -> None:
        store = SettingsStore(self.root)
        store.path.parent.mkdir(parents=True)
        store.path.write_text(json.dumps({"text_scale": ["large"], "window_mode": {}}), encoding="utf-8")
        restored = store.load()
        self.assertEqual(restored.text_scale, "standard")
        self.assertEqual(restored.window_mode, "windowed")

    def test_save_discovery_reports_real_worlds_and_not_backups_or_map_files(self) -> None:
        userdir = self.root / "独立 save user"
        populated = self.world(userdir, "青山 & Last Shelter", saves=("alice.sav", "bob.sav.gz"))
        (populated / "old.sav.bak").write_text("backup", encoding="utf-8")
        (populated / "overmap.map").write_text("map", encoding="utf-8")
        nested = populated / "not-a-character.sav"
        nested.mkdir()
        self.world(userdir, "未有人物的世界", timestamp=900)
        (userdir / "save" / "readme.txt").write_text("not a world", encoding="utf-8")
        (userdir / "save" / "random-directory").mkdir()
        worlds = scan_worlds(userdir)
        self.assertEqual([item.name for item in worlds], ["青山 & Last Shelter", "未有人物的世界"])
        self.assertEqual([item.save_count for item in worlds], [2, 0])
        self.assertEqual(worlds[0].path, populated)
        self.assertEqual(worlds[0].last_played, 1000)

    def test_missing_save_root_and_malformed_metadata_do_not_crash(self) -> None:
        self.assertEqual(scan_worlds(self.root / "missing"), [])
        self.assertEqual(scan_worlds(""), [])
        world = self.world(self.root, "Malformed metadata")
        (world / "worldoptions.json").write_text("{ broken metadata", encoding="utf-8")
        self.assertEqual(scan_worlds(self.root)[0].save_count, 0)

    def test_latest_character_save_controls_world_sorting(self) -> None:
        self.world(self.root, "Old", saves=("a.sav",), timestamp=200)
        self.world(self.root, "Recent", saves=("a.sav",), timestamp=300)
        self.assertEqual([item.name for item in scan_worlds(self.root)], ["Recent", "Old"])

    def test_launch_argument_list_preserves_world_and_paths_as_single_values(self) -> None:
        settings = self.settings()
        name = "青山 & Last Shelter"
        self.world(Path(settings.user_directory), name, saves=("character.sav",))
        command = build_launch_command(settings, scan_worlds(settings.user_directory)[0])
        self.assertIsInstance(command, list)
        self.assertEqual(command[0], str(Path(settings.game_executable).resolve()))
        self.assertEqual(command[command.index("--userdir") + 1], str(Path(settings.user_directory).resolve()) + os.sep)
        self.assertEqual(command[command.index("--basepath") + 1], str(Path(settings.game_executable).parent.resolve()) + os.sep)
        self.assertEqual(command[-2:], ["--world", name])

    def test_launch_without_world_opens_the_actual_game_main_menu(self) -> None:
        command = build_launch_command(self.settings())
        self.assertNotIn("--world", command)

    def test_missing_executable_and_user_directory_file_block_launch(self) -> None:
        settings = self.settings()
        Path(settings.game_executable).unlink()
        with self.assertRaises(FileNotFoundError):
            build_launch_command(settings)
        settings = self.settings()
        Path(settings.user_directory).write_text("this is a file", encoding="utf-8")
        with self.assertRaises(ValueError):
            build_launch_command(settings)

    def test_missing_empty_or_traversal_world_cannot_be_launched(self) -> None:
        settings = self.settings()
        self.world(Path(settings.user_directory), "Empty World")
        for world in ("missing", "Empty World", "../outside", "C:\\outside", ""):
            with self.subTest(world=world), self.assertRaises(ValueError):
                build_launch_command(settings, world)

    def test_launcher_uses_no_shell_and_blocks_duplicate_running_game(self) -> None:
        settings = self.settings()
        process = Mock()
        process.poll.return_value = None
        launcher = GameLauncher()
        with patch("app.domain.subprocess.Popen", return_value=process) as spawn:
            self.assertIs(launcher.start(settings), process)
            arguments, options = spawn.call_args
            self.assertEqual(arguments[0], build_launch_command(settings))
            self.assertIs(options["shell"], False)
            self.assertEqual(options["cwd"], str(Path(settings.game_executable).parent))
            self.assertTrue(Path(settings.user_directory).is_dir())
            self.assertTrue(launcher.running)
            with self.assertRaises(RuntimeError):
                launcher.start(settings)
            self.assertEqual(spawn.call_count, 1)
            process.poll.return_value = 0
            self.assertFalse(launcher.running)
            launcher.start(settings)
            self.assertEqual(spawn.call_count, 2)

    def test_discovery_finds_real_nested_runtime_executable(self) -> None:
        executable = self.root / ".local" / "runtime" / "release folder" / "cataclysm-tiles.exe"
        executable.parent.mkdir(parents=True)
        executable.write_bytes(b"not executed")
        self.assertEqual(discover_game_executable(self.root), str(executable.resolve()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
