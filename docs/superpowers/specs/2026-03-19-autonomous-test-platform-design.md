# Autonomous Test Platform for Teardown MP Mods

**Date:** 2026-03-19
**Status:** Approved
**Problem:** The AI team (4 terminals) can only analyze mod code statically. Code that passes all 30 lint checks can still fail in-game: weapons don't do damage, effects are missing, HUD is broken. The user is the only one who can observe runtime behavior, creating a bottleneck.

**Solution:** A 4-layer test platform (`tools/test.py`) that combines deep static analysis with automated game launching, input simulation, screenshot capture, and AI-powered visual verification.

---

## Architecture

```
tools/test.py --mod "ModName"
│
├── Layer 1: Deep Semantic Analysis (2 sec, no game)
│   Traces firing/effect/HUD chains, validates assets, cross-references IDs
│
├── Layer 2: Diagnostic Injection (instant)
│   Temporarily patches mod with DebugWatch() wrappers on key APIs
│
├── Layer 3: Game Runner + Automated Input (45-60 sec)
│   Launches Teardown → loads test map → selects tool → fires →
│   takes continuous screenshots → captures log → kills game
│
├── Layer 4: Report Generation
│   Static findings + runtime errors + screenshot analysis → PASS/FAIL
│
└── Cleanup: restores original mod code from backup
```

### CLI Interface

```bash
python -m tools.test --mod "C4"              # Full 4-layer test
python -m tools.test --mod "C4" --static     # Layer 1 only (no game)
python -m tools.test --batch guns            # All gun mods sequentially
python -m tools.test --mod "C4" --verbose    # Detailed output
python -m tools.test --mod "C4" --no-input   # Game launch but no input sim
```

---

## Layer 1: Deep Semantic Analyzer

Static analysis that goes beyond pattern matching to trace code logic. Implemented as `tools/deepcheck.py`, called by `tools/test.py`.

**Relationship to lint.py:** `lint.py` matches single-line patterns (regex). `deepcheck.py` does multi-function chain tracing — following data flow across functions to verify that complete behavior chains work end-to-end. They complement each other. `deepcheck.py` does NOT replace `lint.py`.

**Non-weapon mods:** The validators below are weapon-focused. For environment, vehicle, and visual-effect mods, Layer 1 runs the asset validator (1.4) and ID cross-reference (1.5) only, and returns PASS for chain validators with a note: "N/A — not a weapon mod." Mod type is detected by `tools/audit.py`.

**When analysis is inconclusive:** If a chain cannot be traced (e.g., dynamic function dispatch via `_G[name]()`, metatable-based API wrapping, or heavily abstracted code), the check returns INCONCLUSIVE rather than PASS/FAIL, with a note explaining what blocked the trace. This prevents false confidence.

### 1.1 Firing Chain Validator

Traces the complete path from player input to damage:

```
Client: InputDown/InputPressed("usetool", p)
  → ServerCall("server.X", p, aimPos, aimDir, ...)
    → server.X function EXISTS
      → server.X calls Shoot() or QueryShot()+ApplyPlayerDamage()
        → Shoot/damage params: damage > 0, range > 0
```

Reports which links are missing or broken. Catches:
- ServerCall target function doesn't exist
- Shoot() called with 0 damage or 0 range
- Shoot() called on client instead of server
- Missing ServerCall bridge (client detects input but never tells server)
- Aim data not passed in ServerCall (server computes aim independently = desync)

### 1.2 Effect Chain Validator

Traces from damage event to audiovisual feedback:

```
Server: Shoot()/Explosion()/damage event
  → ClientCall(0, "client.Y", pos, ...) for world effects
  → ClientCall(p, "client.Z", ...) for personal feedback
    → client.Y/Z EXISTS
      → client.Y calls PlaySound(), SpawnParticle(), PointLight()
      → client.Z calls ShakeCamera(), recoil logic
```

Reports:
- PlaySound/SpawnParticle called on server (won't render for other players)
- ClientCall target function doesn't exist
- Effects use ClientCall(p, ...) when they should use ClientCall(0, ...) (only firing player sees)
- No ClientCall after damage (silent weapon)

### 1.3 HUD Validator

Checks that the HUD displays accurate information:

```
client.draw() EXISTS
  → References player state variable (e.g., data.ammo)
    → Same variable is decremented in firing logic
    → UiTranslate/UiAlign positions within screen bounds (0-1920, 0-1080 typical)
    → GetPlayerTool(p) == "toolid" guard present (only show for active tool)
```

Reports:
- client.draw() missing entirely
- Ammo display references variable X but firing decrements variable Y
- UI positioned at extreme coordinates (likely off-screen)
- No tool-active guard (HUD shows for all tools)

### 1.4 Asset Validator

Checks that every file path referenced in code exists on disk:

```
For each string literal matching asset patterns:
  "MOD/snd/*.ogg"  → check C:/Users/trust/Documents/Teardown/mods/ModName/snd/*.ogg
  "MOD/vox/*.vox"  → check C:/Users/trust/Documents/Teardown/mods/ModName/vox/*.vox
  "MOD/img/*.png"  → check C:/Users/trust/Documents/Teardown/mods/ModName/img/*.png
```

Reports:
- Sound file referenced but not found (silent weapon)
- Vox model referenced but not found (invisible tool)
- Image referenced but not found (broken HUD icons)

### 1.5 ID Cross-Reference Validator

Ensures all tool IDs are consistent across registration, enabling, and ammo:

```
RegisterTool("toolid", ...) in server.init()
  → SetToolEnabled("toolid", true, p) in PlayersAdded (SAME string)
  → SetToolAmmo("toolid", N, p) in PlayersAdded (SAME string)
  → SetString("game.tool.toolid.ammo.display", "") (SAME string)
  → GetPlayerTool(p) == "toolid" in client.draw() (SAME string)
```

Reports:
- Case mismatch: RegisterTool("c4") vs SetToolEnabled("C4")
- Missing SetToolAmmo (tool won't appear in toolbar)
- Missing SetToolEnabled in PlayersAdded (tool disabled for joining players)
- HUD checks for wrong tool ID

### 1.6 ServerCall Parameter Validator

Verifies ServerCall/ClientCall argument counts match target functions:

```
ServerCall("server.shoot", p, pos, dir)  -- 3 args after function name
  → function server.shoot(p, pos, dir)   -- must accept 3 params
```

Reports:
- Argument count mismatch
- Missing player ID as first param (Issue #51 pattern)
- Target function doesn't exist

---

## Layer 2: Diagnostic Injection

Diagnostic instrumentation injected directly into the mod's `main.lua` source code via Python text manipulation (NOT `#include`). This avoids ordering problems — `#include` runs at parse time before the mod's functions are defined, making it impossible to wrap them. Instead, the injector:

1. Parses the mod's `main.lua` to find function definitions
2. Prepends counter-increment code into function bodies
3. Appends API-wrapping code at the TOP of the file (before any function defs) to intercept global API calls
4. Adds DebugWatch + savegame-registry reporting at the END of tick functions

### Two Data Channels (not just screenshots)

**Channel 1 — DebugWatch():** Persistent on-screen counters, visible in screenshots. Used for quick visual confirmation by the AI terminal. These are a VISUAL AID, not the primary data source.

**Channel 2 — Savegame Registry:** `SetString("savegame.mod.diag.X", value)` persists to Teardown's save file on disk. After the game closes, `tools/test.py` reads the save file at `C:/Users/trust/AppData/Local/Teardown/savegame.xml` to extract diagnostic counters programmatically. This is DETERMINISTIC — no OCR, no screenshot parsing, no vision errors. **This is the primary data source.**

### Wrapped APIs

```lua
-- Injected at TOP of main.lua (before any function defs)
-- Wraps global API functions with counting versions

local __diag = {
    shootCount = 0, queryShotCount = 0, damageCount = 0,
    explosionCount = 0, makeHoleCount = 0,
    soundCount = 0, particleCount = 0, lightCount = 0,
    toolRegistered = false, toolIds = {},
    serverTicks = 0, clientTicks = 0, drawCalls = 0,
    errors = 0,
}

local __origShoot = Shoot
function Shoot(...) __diag.shootCount = __diag.shootCount + 1; return __origShoot(...) end

local __origPlaySound = PlaySound
function PlaySound(...) __diag.soundCount = __diag.soundCount + 1; return __origPlaySound(...) end

local __origSpawnParticle = SpawnParticle
function SpawnParticle(...) __diag.particleCount = __diag.particleCount + 1; return __origSpawnParticle(...) end

-- ... same pattern for QueryShot, ApplyPlayerDamage, Explosion, MakeHole,
--     PointLight, RegisterTool, SetToolEnabled, SetToolAmmo
```

### Lifecycle Instrumentation

Injected INTO existing function bodies (prepended as first lines):

```lua
-- Prepended into server.tick(dt):
__diag.serverTicks = __diag.serverTicks + 1

-- Prepended into client.tick(dt):
__diag.clientTicks = __diag.clientTicks + 1

-- Prepended into client.draw():
__diag.drawCalls = __diag.drawCalls + 1
```

### Reporting (appended to end of server.tick and client.tick)

```lua
-- DebugWatch for visual confirmation in screenshots
DebugWatch("DIAG:Ticks", "S:" .. __diag.serverTicks .. " C:" .. __diag.clientTicks)
DebugWatch("DIAG:Combat", "Shoot:" .. __diag.shootCount .. " Dmg:" .. __diag.damageCount)
DebugWatch("DIAG:Effects", "Snd:" .. __diag.soundCount .. " Part:" .. __diag.particleCount)

-- Savegame registry for programmatic extraction (PRIMARY DATA)
SetString("savegame.mod.diag.ticks", __diag.serverTicks .. "," .. __diag.clientTicks)
SetString("savegame.mod.diag.combat", __diag.shootCount .. "," .. __diag.queryShotCount .. "," .. __diag.damageCount .. "," .. __diag.explosionCount)
SetString("savegame.mod.diag.effects", __diag.soundCount .. "," .. __diag.particleCount .. "," .. __diag.lightCount)
SetString("savegame.mod.diag.tools", table.concat(__diag.toolIds, ","))
SetString("savegame.mod.diag.errors", tostring(__diag.errors))
```

### Injection/Cleanup Process

1. **Backup**: Copy `main.lua` → `main.lua.testbackup`
2. **Inject**: Python script modifies `main.lua` in-place:
   - Prepends API wrappers after `#version 2` and `#include` lines
   - Finds `function server.tick`, `function client.tick`, `function client.draw` — prepends counter increments
   - Appends DebugWatch + savegame-registry writes to end of tick functions
3. After test: restore `main.lua` from `.testbackup`, clean savegame diag keys
4. **Safety**: On startup, check for orphaned `.testbackup` files and restore them (handles crashes)
5. **Name collision safety**: All diagnostic variables use `__diag` prefix (double underscore) — no mod uses this pattern

---

## Layer 3: Game Runner + Automated Input

Python module `tools/gamerunner.py` that launches Teardown, simulates player input, captures screenshots, and collects diagnostic data.

### 3.0 Prerequisites and Configuration

**Windowed mode required.** Teardown must run in windowed/borderless mode for reliable screen capture and input simulation. `mss` captures black frames from exclusive fullscreen DirectX. The game runner:
1. Locates Teardown's options file: `C:/Users/trust/AppData/Local/Teardown/options.xml`
2. Before launch: sets `<resolution windowed="1" width="1280" height="720"/>` (backs up original)
3. After test: restores original display settings

**Mod enable/disable.** Teardown stores enabled mods in its save/options data. The game runner:
1. Reads the current mod enable state from Teardown's config
2. Backs up the config
3. Disables all mods, enables ONLY the target mod + test harness
4. After test: restores original mod config

**Concurrent test lock.** A lockfile `tools/.test_lock` prevents multiple terminals from running game tests simultaneously. If lock exists and the owning process is dead, the lock is stale and cleared.

### 3.1 Test Harness Mod

A minimal mod installed at `C:/Users/trust/Documents/Teardown/mods/__test_harness/` that provides:

**`main.xml`** — A simple voxel scene:
```xml
<scene version="2">
    <environment>
        <skybox constant="1 1 1"/>  <!-- bright neutral lighting -->
    </environment>
    <group pos="0 0 0">
        <vox pos="0 0 -5" file="MOD/wall.vox" />   <!-- target wall 5m ahead -->
        <vox pos="0 -1 0" file="MOD/floor.vox" />   <!-- flat floor -->
    </group>
    <spawnpoint pos="0 1.5 0" rot="0 0 0"/>          <!-- player faces wall -->
</scene>
```

**`wall.vox` / `floor.vox`** — Simple voxel objects (flat wall, flat floor). Created once by `tools/gamerunner.py --setup` using minimal vox binary format.

**`main.lua`** — Test harness logic:
```lua
#version 2
#include "script/include/player.lua"
-- Auto-selects the target tool after a delay
-- Tool ID is written to info.txt by the test runner
function server.tick(dt)
    for p in PlayersAdded() do
        -- Read target tool ID from registry (set by test runner via options file)
        local toolId = GetString("level.test.toolid")
        if toolId ~= "" then
            SetPlayerTool(toolId, p)
        end
    end
end
```

**`info.txt`**:
```
name = Test Harness
author = Teardown MP Patcher
description = Automated testing environment
version = 2
```

### 3.2 Game Launch + Menu Navigation

```python
Phase 1: Pre-launch
  1. Acquire test lock (fail if another test is running)
  2. Back up Teardown options/config
  3. Set windowed mode 1280x720
  4. Enable only target mod + __test_harness
  5. Clear old log.txt (or record current line count as baseline)
  6. Inject diagnostics into target mod (Layer 2)

Phase 2: Launch
  7. Find Teardown.exe via Steam library (registry lookup or known paths)
  8. Launch Teardown.exe directly (not via Steam — avoids Steam overlay delays)
  9. Poll log.txt for "Teardown" version string (confirms process started)
  10. Poll for window handle via win32 API (FindWindow or EnumWindows)
  11. Bring window to foreground, ensure focus

Phase 3: Menu Navigation (input simulation via pyautogui)
  12. Poll log.txt for "Main menu" or similar ready indicator
  13. If splash/intro screens: send Escape/Space to skip
  14. Navigate: Mods menu → select __test_harness → Play
      (Exact click coordinates determined during --setup calibration run)
  15. Poll log.txt for "Active mod: ModName" — confirms level + mods loaded
  16. Wait additional 3s for all server.init/client.init to complete

Phase 4: Error — if log.txt shows compile/runtime errors before gameplay:
  17. Record errors, skip to Phase 6 (cleanup), report FAIL
```

**Menu navigation calibration:** The first time the test runner is used, `python -m tools.test --setup` launches the game and asks the user to identify menu button positions. These coordinates are saved to `tools/test_config.json`. Subsequent runs use saved coordinates. If Teardown updates its UI, re-run `--setup`.

### 3.3 Automated Input Simulation

Uses Python `pyautogui` with `pygetwindow` for window management. All input is sent only when the Teardown window has focus.

```python
# Test sequence for a weapon mod:
1. Wait for tool auto-selection (test harness mod selects via SetPlayerTool)
2. Verify tool active: poll savegame registry for __diag.toolIds
3. Screenshot: "tool_selected" (verify toolbar + hand model)
4. Wait 1s
5. Left click held 0.5s (fire weapon — aim at wall, test map guarantees facing)
6. Screenshot burst: 0.5s intervals for 5 seconds
7. Press R (reload, if mod has reload logic — detected by audit.py)
8. Screenshot: "after_reload"
9. Open options menu (if mod has one — key from audit.py)
10. Screenshot: "options_menu"
11. Close options, fire again (verify post-options behavior)
12. Screenshot: "second_fire"
```

For grenade/explosive mods (detected by `tools/audit.py`):
```python
# Extended sequence:
5. Left click (throw)
6. Screenshot burst: 0.5s intervals for 10 seconds (covers fuse delays)
```

For mods with multiple tools (detected by counting RegisterTool calls):
```python
# Iterate per tool:
for each tool_id detected in mod:
    Test harness selects tool → run fire sequence → screenshots
```

**Tool selection:** NOT by number key (unreliable — toolbar order depends on load order). Instead, the test harness mod calls `SetPlayerTool(toolId, p)` server-side, which is deterministic.

### 3.4 Screenshot Capture

Uses Python `mss` library for fast screen capture in windowed mode:

```python
# Continuous capture during test sequence at 2 FPS
screenshots = []
for i in range(num_frames):
    img = capture_teardown_window()  # crop to game window region
    screenshots.append((timestamp, img))
    sleep(0.5)

# Save to tools/test_results/ModName/YYYY-MM-DD_HH-MM-SS/frames/
# frame_001.png, frame_002.png, ...
```

**Black frame detection:** After first capture, check if frame is >90% black (exclusive fullscreen fallback). If so, abort runtime test with WARN and suggest re-running `--setup`.

### 3.5 Screenshot Analysis

After capture, key frames are analyzed by the AI terminal reading images via the Read tool (Claude is multimodal):

1. **Tool selection frame**: "Is there a tool/weapon model visible in the player's hand? Is it in the toolbar at the bottom?"
2. **Post-fire frames**: "Is there a muzzle flash, projectile trail, explosion, or particle effect? Did a hole appear in the wall?"
3. **HUD frame**: "Is there HUD text visible? Does it show ammo count? Is it readable and positioned correctly?"
4. **Options frame**: "Is there a settings menu visible with clickable buttons?"

Screenshots are for VISUAL verification only. Quantitative data (shoot count, ammo, tick counts) comes from the savegame registry (Layer 2), not from reading screenshot text.

### 3.6 Data Collection

After killing the game process, collect from three sources:

**Source 1 — Game log** (`tools/logparse.py`):
- Runtime errors during the test session (after baseline line count)
- Compile errors
- Missing asset warnings ("Couldn't find sound bank")
- Active mod confirmation

**Source 2 — Savegame registry** (parse `savegame.xml`):
- `savegame.mod.diag.ticks` → server tick count, client tick count
- `savegame.mod.diag.combat` → shoot, queryshot, damage, explosion counts
- `savegame.mod.diag.effects` → sound, particle, light counts
- `savegame.mod.diag.tools` → registered tool IDs
- `savegame.mod.diag.errors` → error count

**Source 3 — Screenshots** (analyzed by AI terminal):
- Visual confirmation of tool rendering, effects, HUD, options menu

### 3.7 Cleanup

```python
Phase 6: Cleanup (ALWAYS runs, even on crash)
  1. taskkill /IM teardown.exe /F (if still running)
  2. Restore main.lua from .testbackup
  3. Restore Teardown options/config from backup
  4. Restore original mod enable state
  5. Release test lock
  6. Clean savegame diag keys (optional — they're harmless)
```

**Crash detection:** If the Teardown process exits with a non-zero exit code, or if a Windows Error Reporting dialog appears (detected via `FindWindow("WerFault")`), the report records `CRASH` as a result level.

---

## Layer 4: Test Report

All results combined into a single report per mod.

### Report Format

```
TEST REPORT: C4
══════════════════════════════════════════════════
Generated: 2026-03-19 14:32:05
Test type: full (static + runtime)

STATIC ANALYSIS
  Firing chain:      PASS — InputPressed→ServerCall→server.shoot→Shoot()
  Effect chain:      PASS — server.shoot→ClientCall(0)→client.onShoot→PlaySound+SpawnParticle
  HUD validation:    PASS — client.draw references data.ammo, decremented in server.shoot
  Asset validation:  PASS — 3/3 sound files found, 1/1 vox file found
  ID cross-ref:      PASS — "c4" consistent across Register/Enable/Ammo/HUD
  ServerCall params: PASS — all 2 ServerCalls match target signatures

RUNTIME (game session: 35.2s)
  Mod loaded:        PASS — "Active mod: C4" in log at 8.4s
  Compile errors:    PASS — 0 errors
  Runtime errors:    PASS — 0 errors
  Asset loading:     PASS — no missing asset warnings
  Diagnostic data:   S:210 C:420 D:420 | Shoot:3 Snd:9 Part:15 Expl:3

VISUAL VERIFICATION
  Tool in toolbar:   PASS — tool icon visible in bottom toolbar
  Tool in hand:      PASS — model rendering in first person
  Firing effects:    PASS — explosion + particles visible in frames 12-18
  HUD rendering:     PASS — ammo counter visible, top-right corner
  Options menu:      PASS — settings panel rendered with clickable buttons

──────────────────────────────────────────────────
RESULT: PASS (0 failures, 0 warnings)
══════════════════════════════════════════════════
```

### Result Levels

- **PASS**: Everything checks out
- **WARN**: Non-critical issue (e.g., "HUD text is small", "only 1 particle effect")
- **FAIL**: Critical issue (e.g., "Shoot() never called", "tool not in toolbar", "runtime error")
- **CRASH**: Game process crashed during test (non-zero exit or WerFault dialog)
- **INCONCLUSIVE**: Layer 1 could not trace a chain (dynamic function names, metatable magic, unusual patterns) — manual review recommended

### Report Storage

Reports saved to `tools/test_results/ModName/YYYY-MM-DD_HH-MM-SS/`:
```
report.txt          — full text report
frames/             — all captured screenshots
  frame_001.png
  frame_002.png
  ...
log_excerpt.txt     — relevant log.txt section
diagnostic_data.json — parsed from savegame registry (primary data)
```

---

## What This System CAN and CANNOT Verify

### CAN verify reliably:
- Mod loads without errors
- Tool appears in toolbar
- Tool renders in hand (something visible vs nothing)
- Firing triggers Shoot()/Explosion() (diagnostic counter)
- Sound/particle functions are called (diagnostic counter)
- Visual effects appear on screen (screenshot comparison)
- HUD renders with correct values
- Options menu appears and has buttons
- All assets exist on disk
- All code chains are complete (input→damage→effects)
- All IDs are consistent
- All ServerCall targets exist

### CAN verify partially:
- Sound effects play (can verify function called, but can't hear audio)
- Damage works (can verify Shoot called with correct params, but no second player to receive damage)
- Multiplayer sync (static analysis of sync patterns, but only one game instance)

### CANNOT verify:
- Gun model looks artistically correct (can only check "something renders")
- Two-player desync bugs (would need two game instances)
- Performance under load (single brief session)
- Specific particle colors/sizes (can see "particles exist" but not artistic quality)

---

## Dependencies

### Python packages (install once):
```bash
pip install mss pyautogui pygetwindow Pillow
```
- `mss` — fast screen capture (windowed mode required)
- `pyautogui` — keyboard/mouse input simulation
- `pygetwindow` — window focus management (bring Teardown to foreground)
- `Pillow` — image processing, black-frame detection

### Game files:
- Teardown executable path (auto-detect from Steam registry or known install paths)
- Test harness mod (created by `python -m tools.test --setup` on first run)
- Teardown must be installed and runnable on the local machine

### First-time setup:
```bash
python -m tools.test --setup
```
This:
1. Installs Python dependencies
2. Creates the test harness mod (`__test_harness/`)
3. Locates Teardown.exe
4. Launches Teardown once for menu navigation calibration (user identifies button positions)
5. Saves config to `tools/test_config.json`

### Existing tools used:
- `tools/lint.py` — severity classification, mod detection
- `tools/audit.py` — mod type detection (gun/grenade/melee/utility)
- `tools/logparse.py` — log error extraction
- `tools/fix.py` — reference for mod paths and structure

---

## Integration with Team Workflow

### In CLAUDE.md, add:
```
After writing or editing any mod code:
  python -m tools.lint --mod "ModName"     # Pattern check
  python -m tools.test --mod "ModName"     # Full autonomous test
```

### In tools.status, add:
- Last test results summary
- Mods that haven't been tested yet
- Mods with failed tests

### Team can run tests autonomously:
- No user interaction needed
- Game launches and closes automatically
- Screenshots analyzed by the AI terminal that ran the test
- Reports stored for review
- Failures create tasks in the MCP task queue

---

## File Structure (new files)

```
tools/
├── test.py                    — CLI entry point
├── deepcheck.py               — Layer 1: semantic analysis
├── diagnostic_wrapper.lua     — Layer 2: API wrappers for injection
├── gamerunner.py              — Layer 3: game launch + input + screenshots
├── test_results/              — Layer 4: stored reports + screenshots
│   └── ModName/
│       └── YYYY-MM-DD_HH-MM-SS/
│           ├── report.txt
│           ├── frames/
│           ├── log_excerpt.txt
│           └── diagnostic_data.txt
├── testmap/                   — Test map mod files
│   ├── info.txt
│   ├── main.lua
│   └── main.xml
tests/
├── test_deepcheck.py          — Tests for semantic analyzer
├── test_gamerunner.py         — Tests for game runner (mocked)
├── test_test.py               — Integration tests
└── fixtures/
    └── deepcheck/             — Test mods for semantic analysis
```
