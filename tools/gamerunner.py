"""Game runner for automated Teardown mod testing.

Handles: finding Teardown exe, test locking, config backup/restore,
savegame diagnostic parsing, screenshot capture, input simulation,
and full game test orchestration.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from tools.common import (
    TEARDOWN_EXE_PATHS, TEST_LOCK_PATH, TEST_CONFIG_PATH,
    SAVEGAME_PATH, OPTIONS_PATH, TEST_HARNESS_DIR, TEST_RESULTS_DIR,
    LOG_PATH, LIVE_MODS_DIR,
)


# ---------------------------------------------------------------------------
# Find Teardown executable
# ---------------------------------------------------------------------------

def find_teardown_exe() -> Path | None:
    """Find Teardown.exe in standard Steam install locations + Steam library folders."""
    # Check hardcoded paths first
    for path in TEARDOWN_EXE_PATHS:
        if path.exists():
            return path

    # Try Steam library folders via libraryfolders.vdf
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
        vdf = Path(steam_path) / "steamapps" / "libraryfolders.vdf"
        if vdf.exists():
            content = vdf.read_text()
            for lib_match in re.findall(r'"path"\s+"([^"]+)"', content):
                exe = Path(lib_match) / "steamapps" / "common" / "Teardown" / "teardown.exe"
                if exe.exists():
                    return exe
    except Exception:
        pass

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


# ---------------------------------------------------------------------------
# Game test result
# ---------------------------------------------------------------------------

@dataclass
class GameTestResult:
    """Results from a runtime game test session."""
    mod_loaded: bool = False
    compile_errors: list[dict] = field(default_factory=list)
    runtime_errors: list[dict] = field(default_factory=list)
    diagnostic_data: dict = field(default_factory=dict)
    screenshot_paths: list[Path] = field(default_factory=list)
    session_duration: float = 0.0
    exit_code: int | None = None
    crashed: bool = False


# ---------------------------------------------------------------------------
# Screenshot capture
# ---------------------------------------------------------------------------

def is_black_frame(img) -> bool:
    """Check if a PIL Image is >90% black (mss fullscreen capture failure)."""
    from PIL import ImageStat
    stat = ImageStat.Stat(img)
    # Average of all channels
    avg = sum(stat.mean) / len(stat.mean)
    return avg < 10  # near-black threshold


def capture_screenshot(output_path: Path, region: dict | None = None) -> bool:
    """Capture a screenshot using mss. Returns True if non-black frame captured."""
    import mss
    from PIL import Image

    with mss.mss() as sct:
        if region:
            monitor = region
        else:
            monitor = sct.monitors[1]  # primary monitor
        raw = sct.grab(monitor)
        img = Image.frombytes("RGB", (raw.width, raw.height), raw.rgb)

        if is_black_frame(img):
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path))
        return True


def capture_screenshot_burst(output_dir: Path, count: int = 10,
                             interval: float = 0.5, region: dict | None = None) -> list[Path]:
    """Capture a burst of screenshots. Returns paths of successful captures."""
    paths = []
    for i in range(count):
        path = output_dir / f"frame_{i+1:03d}.png"
        if capture_screenshot(path, region):
            paths.append(path)
        time.sleep(interval)
    return paths


# ---------------------------------------------------------------------------
# Window management
# ---------------------------------------------------------------------------

def find_teardown_window():
    """Find the Teardown game window. Returns window object or None."""
    try:
        import pygetwindow as gw
        wins = gw.getWindowsWithTitle("Teardown")
        if wins:
            return wins[0]
    except Exception:
        pass
    return None


def bring_window_to_front(win) -> bool:
    """Bring a window to the foreground and activate it."""
    try:
        if win.isMinimized:
            win.restore()
        win.activate()
        time.sleep(0.3)
        return True
    except Exception:
        return False


def get_window_region(win) -> dict | None:
    """Get the mss-compatible region dict for a window."""
    try:
        return {
            "left": win.left,
            "top": win.top,
            "width": win.width,
            "height": win.height,
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Input simulation
# ---------------------------------------------------------------------------

def run_weapon_test_sequence(mod_type: str = "gun", has_reload: bool = False,
                             has_options: bool = False) -> None:
    """Simulate player input for testing a weapon mod."""
    import pyautogui
    pyautogui.PAUSE = 0.1  # small delay between actions

    # Wait for game to settle after level load
    time.sleep(3)

    # Fire weapon (left click)
    pyautogui.click()
    time.sleep(0.5)

    # For explosives, wait longer for effects
    if mod_type == "explosive":
        time.sleep(5)
    else:
        time.sleep(1)

    # Fire again
    pyautogui.click()
    time.sleep(1)

    # Reload if applicable
    if has_reload:
        pyautogui.press("r")
        time.sleep(1)

    # Open options menu if applicable
    if has_options:
        # Most mods use a key like 'o' or a custom binding
        # Try common options keys
        pyautogui.press("o")
        time.sleep(1)
        pyautogui.press("o")  # close
        time.sleep(0.5)

    # Fire one more time (verify post-interaction)
    pyautogui.click()
    time.sleep(1)


# ---------------------------------------------------------------------------
# Log monitoring
# ---------------------------------------------------------------------------

def get_log_baseline() -> int:
    """Record current log file line count as baseline."""
    if LOG_PATH.exists():
        return len(LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines())
    return 0


def wait_for_log_pattern(pattern: str, timeout: float = 60, baseline: int = 0) -> bool:
    """Poll log.txt for a pattern after the baseline line. Returns True if found."""
    start = time.time()
    while time.time() - start < timeout:
        if LOG_PATH.exists():
            content = LOG_PATH.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()
            new_lines = lines[baseline:]
            if any(pattern.lower() in line.lower() for line in new_lines):
                return True
        time.sleep(1)
    return False


def parse_log_errors_since(baseline: int) -> tuple[list[dict], list[dict]]:
    """Parse compile and runtime errors from log since baseline."""
    from tools.logparse import parse_log
    if not LOG_PATH.exists():
        return [], []
    content = LOG_PATH.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    new_content = "\n".join(lines[baseline:])
    result = parse_log(new_content)

    compile_errors = []
    runtime_errors = []
    for mod_name, errors in result.get("mods", {}).items():
        for err in errors:
            err["mod"] = mod_name
            if err["type"] == "compile":
                compile_errors.append(err)
            else:
                runtime_errors.append(err)

    return compile_errors, runtime_errors


# ---------------------------------------------------------------------------
# Test harness installation
# ---------------------------------------------------------------------------

def install_test_harness() -> None:
    """Install the test harness mod to the game's mods directory."""
    src = Path(__file__).parent / "testmap"
    if not src.exists():
        return

    TEST_HARNESS_DIR.mkdir(parents=True, exist_ok=True)

    # Copy template files
    for f in src.iterdir():
        shutil.copy2(f, TEST_HARNESS_DIR / f.name)

    # Create minimal vox files if they don't exist
    for name in ["wall.vox", "floor.vox"]:
        vox_path = TEST_HARNESS_DIR / name
        if not vox_path.exists():
            _create_minimal_vox(vox_path, width=10, height=10, depth=1)


def _create_minimal_vox(path: Path, width: int = 10, height: int = 10, depth: int = 1) -> None:
    """Create a minimal MagicaVoxel .vox file (flat slab of voxels)."""
    import struct

    num_voxels = width * height * depth
    # XYZI chunk data: num_voxels + (x, y, z, colorIndex) per voxel
    xyzi_data = struct.pack("<I", num_voxels)
    for x in range(width):
        for y in range(height):
            for z in range(depth):
                xyzi_data += struct.pack("<BBBB", x, y, z, 1)  # color index 1

    # SIZE chunk: x, y, z dimensions
    size_data = struct.pack("<III", width, height, depth)

    # Build chunks
    def chunk(tag: bytes, content: bytes, children: bytes = b"") -> bytes:
        return tag + struct.pack("<II", len(content), len(children)) + content + children

    size_chunk = chunk(b"SIZE", size_data)
    xyzi_chunk = chunk(b"XYZI", xyzi_data)
    main_chunk = chunk(b"MAIN", b"", size_chunk + xyzi_chunk)

    # File: magic + version + main chunk
    with open(path, "wb") as f:
        f.write(b"VOX ")
        f.write(struct.pack("<I", 150))  # version
        f.write(main_chunk)


# ---------------------------------------------------------------------------
# Full game test orchestration
# ---------------------------------------------------------------------------

def run_game_test(mod_name: str, config: GameRunnerConfig,
                  no_input: bool = False) -> GameTestResult:
    """Run a complete game test session.

    1. Record log baseline
    2. Launch Teardown
    3. Wait for mod to load
    4. Optionally run input sequence
    5. Capture screenshots
    6. Kill game
    7. Parse log errors + savegame diagnostics
    """
    result = GameTestResult()
    start_time = time.time()

    if not config.teardown_exe or not config.teardown_exe.exists():
        result.crashed = True
        return result

    # Phase 1: Pre-launch
    log_baseline = get_log_baseline()

    # Phase 2: Launch Teardown
    try:
        proc = subprocess.Popen(
            [str(config.teardown_exe)],
            cwd=str(config.teardown_exe.parent),
        )
    except Exception as e:
        result.crashed = True
        return result

    try:
        # Phase 3: Wait for game window
        win = None
        for _ in range(30):  # 30 seconds to find window
            time.sleep(1)
            win = find_teardown_window()
            if win:
                break

        if not win:
            result.session_duration = time.time() - start_time
            return result

        bring_window_to_front(win)

        # Wait for mod to load (check log for "Active mod" or similar)
        mod_loaded = wait_for_log_pattern(mod_name, timeout=45, baseline=log_baseline)
        result.mod_loaded = mod_loaded

        # Check for early compile errors
        compile_errors, runtime_errors = parse_log_errors_since(log_baseline)
        if compile_errors:
            result.compile_errors = compile_errors
            result.runtime_errors = runtime_errors
            result.session_duration = time.time() - start_time
            return result

        # Phase 4: Screenshots + input
        region = get_window_region(win)
        frames_dir = TEST_RESULTS_DIR / mod_name / datetime.now().strftime("%Y-%m-%d_%H-%M-%S") / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        if not no_input and mod_loaded:
            # Take pre-fire screenshot
            capture_screenshot(frames_dir / "frame_001_pre.png", region)

            # Run input sequence
            run_weapon_test_sequence()

            # Take post-fire screenshot burst
            result.screenshot_paths = capture_screenshot_burst(
                frames_dir, count=6, interval=0.5, region=region
            )
        else:
            # Just capture a few frames
            time.sleep(5)
            result.screenshot_paths = capture_screenshot_burst(
                frames_dir, count=3, interval=1.0, region=region
            )

        # Small delay for diagnostics to be written to savegame
        time.sleep(2)

    finally:
        # Phase 5: Kill game
        try:
            proc.terminate()
            proc.wait(timeout=10)
        except Exception:
            try:
                proc.kill()
            except Exception:
                subprocess.run(["taskkill", "/IM", "teardown.exe", "/F"],
                             capture_output=True)

        result.exit_code = proc.returncode
        result.session_duration = time.time() - start_time

    # Phase 6: Collect data
    compile_errors, runtime_errors = parse_log_errors_since(log_baseline)
    result.compile_errors = compile_errors
    result.runtime_errors = runtime_errors
    result.diagnostic_data = parse_savegame_diagnostics(SAVEGAME_PATH)

    # Check for crash
    if result.exit_code and result.exit_code != 0:
        result.crashed = True

    return result
