"""Shared constants and helpers for Teardown MP Patcher developer tools."""

from pathlib import Path

# Working directory for mod editing — this is the single source of truth.
# Mods are edited here, then published to Workshop via update.bat.
# Both game installations get mods via Workshop subscription (no local sync).
LIVE_MODS_DIR = Path("D:/The Vault/Modding/Games/Teardown")

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


# Teardown application data
TEARDOWN_DATA_DIR = Path.home() / "AppData" / "Local" / "Teardown"
SAVEGAME_PATH = TEARDOWN_DATA_DIR / "savegame.xml"
OPTIONS_PATH = TEARDOWN_DATA_DIR / "options.xml"

# Common Teardown install locations (checked in order)
TEARDOWN_EXE_PATHS = [
    Path("C:/Program Files (x86)/Steam/steamapps/common/Teardown/teardown.exe"),
    Path("C:/Program Files/Steam/steamapps/common/Teardown/teardown.exe"),
    Path("D:/Steam/steamapps/common/Teardown/teardown.exe"),
    Path("D:/SteamLibrary/steamapps/common/Teardown/teardown.exe"),
]

# Test infrastructure
TEST_LOCK_PATH = Path(__file__).parent / ".test_lock"
TEST_CONFIG_PATH = Path(__file__).parent / "test_config.json"
TEST_RESULTS_DIR = Path(__file__).parent / "test_results"
TEST_HARNESS_DIR = LIVE_MODS_DIR / "__test_harness"


def is_builtin_mod(mod_dir: Path) -> bool:
    """Check if a mod is a built-in Steam depot mod (no id.txt).
    Built-in mods must NEVER be modified — Steam verify restores them
    and modifications cause MP file mismatch disconnects."""
    return not (mod_dir / "id.txt").exists()


def discover_mods(mods_dir: Path = LIVE_MODS_DIR, mod_name: str | None = None, include_builtin: bool = False) -> list[Path]:
    """Find mod directories. Each must have info.txt to be considered a mod.
    By default, skips built-in mods (no id.txt) to prevent accidental modification."""
    if not mods_dir.exists():
        return []
    mods = []
    for d in sorted(mods_dir.iterdir()):
        if d.is_dir() and (d / "info.txt").exists():
            if mod_name is None or d.name == mod_name:
                if include_builtin or not is_builtin_mod(d):
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
