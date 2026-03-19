"""Tests for tools/gamerunner.py — game launch/kill/cleanup.

All tests use mocks — they never actually launch Teardown.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from tools.gamerunner import (
    find_teardown_exe,
    acquire_test_lock,
    release_test_lock,
    parse_savegame_diagnostics,
    is_black_frame,
    install_test_harness,
    GameTestResult,
)


class TestFindTeardownExe:
    def test_returns_path_when_found(self, tmp_path):
        exe = tmp_path / "teardown.exe"
        exe.write_bytes(b"fake")
        with patch("tools.gamerunner.TEARDOWN_EXE_PATHS", [exe]):
            assert find_teardown_exe() == exe

    def test_returns_none_when_not_found(self):
        with patch("tools.gamerunner.TEARDOWN_EXE_PATHS", [Path("/nonexistent/teardown.exe")]):
            with patch("tools.gamerunner.re.findall", return_value=[]):
                assert find_teardown_exe() is None

    def test_returns_first_found(self, tmp_path):
        exe1 = tmp_path / "first" / "teardown.exe"
        exe2 = tmp_path / "second" / "teardown.exe"
        exe1.parent.mkdir()
        exe2.parent.mkdir()
        exe1.write_bytes(b"fake1")
        exe2.write_bytes(b"fake2")
        with patch("tools.gamerunner.TEARDOWN_EXE_PATHS", [exe1, exe2]):
            assert find_teardown_exe() == exe1


class TestTestLock:
    def test_acquire_and_release(self, tmp_path):
        lock = tmp_path / ".test_lock"
        with patch("tools.gamerunner.TEST_LOCK_PATH", lock):
            assert acquire_test_lock()
            assert lock.exists()
            release_test_lock()
            assert not lock.exists()

    def test_acquire_fails_when_locked_by_live_process(self, tmp_path):
        import os
        lock = tmp_path / ".test_lock"
        # Lock with our own PID (a live process)
        lock.write_text(json.dumps({"pid": os.getpid()}))
        with patch("tools.gamerunner.TEST_LOCK_PATH", lock):
            assert acquire_test_lock() is False

    def test_stale_lock_cleared(self, tmp_path):
        lock = tmp_path / ".test_lock"
        # Lock with non-existent PID
        lock.write_text(json.dumps({"pid": 999999999}))
        with patch("tools.gamerunner.TEST_LOCK_PATH", lock):
            assert acquire_test_lock() is True


class TestSavegameDiagnostics:
    def test_parse_nested_xml(self, tmp_path):
        """Teardown savegame uses nested elements: savegame.mod.diag.X -> <savegame><mod><diag><X/></diag></mod></savegame>"""
        xml = tmp_path / "savegame.xml"
        xml.write_text('''<registry version="2.0.0">
\t<savegame>
\t\t<mod>
\t\t\t<diag>
\t\t\t\t<ticks value="100,200"/>
\t\t\t\t<combat value="5,2,3,1"/>
\t\t\t\t<effects value="10,15,3"/>
\t\t\t\t<tools value="pistol"/>
\t\t\t\t<errors value="0"/>
\t\t\t</diag>
\t\t</mod>
\t</savegame>
</registry>''')
        data = parse_savegame_diagnostics(xml)
        assert data["server_ticks"] == 100
        assert data["client_ticks"] == 200
        assert data["shoot_count"] == 5
        assert data["queryshot_count"] == 2
        assert data["damage_count"] == 3
        assert data["explosion_count"] == 1
        assert data["sound_count"] == 10
        assert data["particle_count"] == 15
        assert data["light_count"] == 3
        assert data["tool_ids"] == ["pistol"]
        assert data["error_count"] == 0

    def test_parse_empty_savegame(self, tmp_path):
        xml = tmp_path / "savegame.xml"
        xml.write_text('<registry version="2.0.0"><savegame></savegame></registry>')
        data = parse_savegame_diagnostics(xml)
        assert data["server_ticks"] == 0
        assert data["shoot_count"] == 0
        assert data["tool_ids"] == []

    def test_parse_missing_file(self, tmp_path):
        xml = tmp_path / "nonexistent.xml"
        data = parse_savegame_diagnostics(xml)
        assert data["server_ticks"] == 0

    def test_parse_multiple_tools(self, tmp_path):
        xml = tmp_path / "savegame.xml"
        xml.write_text('''<registry version="2.0.0">
\t<savegame>
\t\t<mod>
\t\t\t<diag>
\t\t\t\t<tools value="pistol,shotgun,rifle"/>
\t\t\t</diag>
\t\t</mod>
\t</savegame>
</registry>''')
        data = parse_savegame_diagnostics(xml)
        assert data["tool_ids"] == ["pistol", "shotgun", "rifle"]


class TestScreenCapture:
    def test_is_black_frame_black(self):
        from PIL import Image
        black = Image.new("RGB", (100, 100), (0, 0, 0))
        assert is_black_frame(black) is True

    def test_is_black_frame_normal(self):
        from PIL import Image
        normal = Image.new("RGB", (100, 100), (128, 128, 128))
        assert is_black_frame(normal) is False

    def test_is_black_frame_near_black(self):
        from PIL import Image
        dark = Image.new("RGB", (100, 100), (5, 5, 5))
        assert is_black_frame(dark) is True


class TestInstallHarness:
    def test_installs_files(self, tmp_path):
        harness_dir = tmp_path / "__test_harness"
        with patch("tools.gamerunner.TEST_HARNESS_DIR", harness_dir):
            install_test_harness()
            assert (harness_dir / "info.txt").exists()
            assert (harness_dir / "main.lua").exists()
            assert (harness_dir / "main.xml").exists()
            assert (harness_dir / "wall.vox").exists()
            assert (harness_dir / "floor.vox").exists()

    def test_vox_magic_bytes(self, tmp_path):
        harness_dir = tmp_path / "__test_harness"
        with patch("tools.gamerunner.TEST_HARNESS_DIR", harness_dir):
            install_test_harness()
            wall = (harness_dir / "wall.vox").read_bytes()
            assert wall[:4] == b"VOX "


class TestGameTestResult:
    def test_default_values(self):
        r = GameTestResult()
        assert r.mod_loaded is False
        assert r.crashed is False
        assert r.session_duration == 0.0
        assert r.screenshot_paths == []
