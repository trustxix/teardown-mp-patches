"""Tests for tools/injector.py — diagnostic code injection and cleanup."""

import pytest
from pathlib import Path

from tools.injector import inject_diagnostics, restore_from_backup, DIAG_PREFIX


SAMPLE_MOD = '''\
#version 2
#include "script/include/player.lua"

players = {}

function server.tick(dt)
    for p in Players() do
        -- game logic
    end
end

function client.tick(dt)
    for p in Players() do
        -- effects
    end
end

function client.draw()
    UiText("hello")
end
'''


class TestInjector:
    def test_inject_adds_wrappers(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        (mod / "info.txt").write_text("name = Test\nversion = 2")
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        assert "__diag" in injected
        assert "__origShoot" in injected

    def test_inject_creates_backup(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        (mod / "info.txt").write_text("name = Test\nversion = 2")
        inject_diagnostics(mod)
        assert (mod / "main.lua.testbackup").exists()

    def test_restore_from_backup(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        (mod / "info.txt").write_text("name = Test\nversion = 2")
        inject_diagnostics(mod)
        restore_from_backup(mod)
        assert (mod / "main.lua").read_text() == SAMPLE_MOD
        assert not (mod / "main.lua.testbackup").exists()

    def test_inject_preserves_version_and_includes(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        (mod / "info.txt").write_text("name = Test\nversion = 2")
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        lines = injected.splitlines()
        assert lines[0] == "#version 2"
        assert '#include "script/include/player.lua"' in lines[1]

    def test_inject_increments_tick_counters(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        (mod / "info.txt").write_text("name = Test\nversion = 2")
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        assert "__diag.serverTicks = __diag.serverTicks + 1" in injected
        assert "__diag.clientTicks = __diag.clientTicks + 1" in injected

    def test_inject_writes_savegame_registry(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        (mod / "info.txt").write_text("name = Test\nversion = 2")
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        assert 'SetString("savegame.mod.diag.' in injected

    def test_inject_adds_debugwatch(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        (mod / "info.txt").write_text("name = Test\nversion = 2")
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        assert "DebugWatch" in injected

    def test_orphan_backup_restored(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text("-- injected version")
        (mod / "main.lua.testbackup").write_text(SAMPLE_MOD)
        restore_from_backup(mod)
        assert (mod / "main.lua").read_text() == SAMPLE_MOD
        assert not (mod / "main.lua.testbackup").exists()

    def test_restore_noop_without_backup(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        restore_from_backup(mod)  # should not crash
        assert (mod / "main.lua").read_text() == SAMPLE_MOD
