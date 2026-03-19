"""Game runner for automated Teardown mod testing.

Handles: finding Teardown exe, test locking, config backup/restore,
savegame diagnostic parsing, screenshot capture, and game orchestration.
"""

from __future__ import annotations

import json
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from tools.common import (
    TEARDOWN_EXE_PATHS, TEST_LOCK_PATH, TEST_CONFIG_PATH,
    SAVEGAME_PATH, OPTIONS_PATH, TEST_HARNESS_DIR,
)


# ---------------------------------------------------------------------------
# Find Teardown executable
# ---------------------------------------------------------------------------

def find_teardown_exe() -> Path | None:
    """Find Teardown.exe in standard Steam install locations."""
    for path in TEARDOWN_EXE_PATHS:
        if path.exists():
            return path
    return None


# ---------------------------------------------------------------------------
# Test lock (prevent concurrent game tests)
# ---------------------------------------------------------------------------

def _is_pid_alive(pid: int) -> bool:
    """Check if a process with the given PID is running."""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def acquire_test_lock() -> bool:
    """Acquire the test lock. Returns False if already locked by a live process."""
    if TEST_LOCK_PATH.exists():
        try:
            data = json.loads(TEST_LOCK_PATH.read_text())
            pid = data.get("pid", 0)
            if _is_pid_alive(pid):
                return False
            # Stale lock — clear it
        except (json.JSONDecodeError, KeyError):
            pass
        TEST_LOCK_PATH.unlink(missing_ok=True)

    TEST_LOCK_PATH.write_text(json.dumps({"pid": os.getpid()}))
    return True


def release_test_lock() -> None:
    """Release the test lock."""
    TEST_LOCK_PATH.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Savegame diagnostic parser
# ---------------------------------------------------------------------------

def _empty_diagnostics() -> dict:
    return {
        "server_ticks": 0, "client_ticks": 0,
        "shoot_count": 0, "queryshot_count": 0,
        "damage_count": 0, "explosion_count": 0,
        "sound_count": 0, "particle_count": 0, "light_count": 0,
        "tool_ids": [],
        "error_count": 0,
    }


def parse_savegame_diagnostics(savegame_path: Path) -> dict:
    """Parse diagnostic data from Teardown's savegame.xml.

    Teardown stores registry values as nested XML elements:
    SetString("savegame.mod.diag.ticks", "100,200")
    becomes: <savegame><mod><diag><ticks value="100,200"/></diag></mod></savegame>
    """
    data = _empty_diagnostics()

    if not savegame_path.exists():
        return data

    try:
        tree = ET.parse(savegame_path)
        root = tree.getroot()
    except ET.ParseError:
        return data

    # Navigate: registry > savegame > mod > diag
    savegame = root.find("savegame")
    if savegame is None:
        return data
    mod = savegame.find("mod")
    if mod is None:
        return data
    diag = mod.find("diag")
    if diag is None:
        return data

    # Parse ticks: "server,client"
    ticks_el = diag.find("ticks")
    if ticks_el is not None:
        parts = ticks_el.get("value", "0,0").split(",")
        if len(parts) >= 2:
            data["server_ticks"] = int(parts[0])
            data["client_ticks"] = int(parts[1])

    # Parse combat: "shoot,queryshot,damage,explosion"
    combat_el = diag.find("combat")
    if combat_el is not None:
        parts = combat_el.get("value", "0,0,0,0").split(",")
        if len(parts) >= 4:
            data["shoot_count"] = int(parts[0])
            data["queryshot_count"] = int(parts[1])
            data["damage_count"] = int(parts[2])
            data["explosion_count"] = int(parts[3])

    # Parse effects: "sound,particle,light"
    effects_el = diag.find("effects")
    if effects_el is not None:
        parts = effects_el.get("value", "0,0,0").split(",")
        if len(parts) >= 3:
            data["sound_count"] = int(parts[0])
            data["particle_count"] = int(parts[1])
            data["light_count"] = int(parts[2])

    # Parse tools: "id1,id2,..."
    tools_el = diag.find("tools")
    if tools_el is not None:
        val = tools_el.get("value", "")
        data["tool_ids"] = [t for t in val.split(",") if t]

    # Parse errors
    errors_el = diag.find("errors")
    if errors_el is not None:
        data["error_count"] = int(errors_el.get("value", "0"))

    return data


# ---------------------------------------------------------------------------
# Game runner config
# ---------------------------------------------------------------------------

@dataclass
class GameRunnerConfig:
    """Persistent config for the game runner (saved by --setup)."""
    teardown_exe: Path | None = None
    menu_coords: dict = field(default_factory=dict)
    window_width: int = 1280
    window_height: int = 720

    def save(self) -> None:
        TEST_CONFIG_PATH.write_text(json.dumps({
            "teardown_exe": str(self.teardown_exe) if self.teardown_exe else None,
            "menu_coords": self.menu_coords,
            "window_width": self.window_width,
            "window_height": self.window_height,
        }, indent=2))

    @classmethod
    def load(cls) -> GameRunnerConfig:
        if not TEST_CONFIG_PATH.exists():
            return cls()
        try:
            data = json.loads(TEST_CONFIG_PATH.read_text())
            return cls(
                teardown_exe=Path(data["teardown_exe"]) if data.get("teardown_exe") else None,
                menu_coords=data.get("menu_coords", {}),
                window_width=data.get("window_width", 1280),
                window_height=data.get("window_height", 720),
            )
        except (json.JSONDecodeError, KeyError):
            return cls()
