"""Shared constants and helpers for Teardown MP Patcher developer tools."""

from pathlib import Path

# Where the game actually loads mods from
LIVE_MODS_DIR = Path.home() / "Documents" / "Teardown" / "mods"

# Teardown log file
LOG_PATH = Path.home() / "AppData" / "Local" / "Teardown" / "log.txt"

# Raw key names that do NOT work with player parameter in Teardown v2
RAW_KEYS = frozenset([
    "lmb", "rmb", "mmb",
    "esc", "tab", "return", "enter", "backspace", "delete",
    "space", "shift", "ctrl", "alt",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "mousedx", "mousedy", "mousewheel",
    "plus", "minus", "uparrow", "downarrow", "leftarrow", "rightarrow",
])

# Input names that DO work with player parameter
PLAYER_INPUTS = frozenset([
    "usetool", "interact", "flashlight", "jump", "crouch",
    "camerax", "cameray",
])


def discover_mods(mods_dir: Path = LIVE_MODS_DIR, mod_name: str | None = None) -> list[Path]:
    """Find mod directories. Each must have info.txt to be considered a mod."""
    if not mods_dir.exists():
        return []
    mods = []
    for d in sorted(mods_dir.iterdir()):
        if d.is_dir() and (d / "info.txt").exists():
            if mod_name is None or d.name == mod_name:
                mods.append(d)
    return mods


def read_lua_files(mod_dir: Path) -> list[tuple[str, str]]:
    """Return list of (relative_path, source_code) for all .lua files in a mod."""
    results = []
    for lua_file in sorted(mod_dir.rglob("*.lua")):
        rel = str(lua_file.relative_to(mod_dir)).replace("\\", "/")
        source = lua_file.read_text(encoding="utf-8", errors="replace")
        results.append((rel, source))
    return results
