# Autonomous Test Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `tools/test.py` — a 4-layer autonomous test platform that lets the AI team test Teardown mods without the user playing the game.

**Architecture:** Layer 1 (deepcheck.py) traces code logic chains statically. Layer 2 (injector.py) instruments mods with diagnostic counters. Layer 3 (gamerunner.py) launches Teardown, simulates input, captures screenshots, and reads savegame diagnostics. Layer 4 (test.py) orchestrates all layers and generates reports. Each layer is independently testable.

**Tech Stack:** Python 3.10+, click (CLI), mss (screenshots), pyautogui (input sim), pygetwindow (window mgmt), Pillow (image processing). Follows existing tools/ patterns (regex-based, click CLI, pytest tests).

**Spec:** `docs/superpowers/specs/2026-03-19-autonomous-test-platform-design.md`

**IMPORTANT RULES:**
- All mod edits happen in `C:/Users/trust/Documents/Teardown/mods/` — NEVER the patches repo
- Use `tools.common.LIVE_MODS_DIR`, `LOG_PATH`, `discover_mods()`, `read_lua_files()` — don't reinvent
- `python -m tools.test` invocation pattern (same as `python -m tools.lint`)
- Follow existing CLI patterns: `click.command()` decorator, `if __name__ == "__main__"` guard
- **Type deviation note:** `deepcheck.py` uses `@dataclass` Finding types instead of lint.py's plain dicts. This is intentional — dataclasses provide richer type info for chain tracing. If findings need to be merged with lint results, use `Finding.to_dict()` method.
- Tasks 3, 4, 5 MUST run sequentially (all modify `deepcheck.py` and `test_deepcheck.py`)
- Verify Teardown's actual `savegame.xml` format during Task 7 — the assumed `<entry key="..." value="..."/>` structure must be checked against a real file

---

## File Structure

```
tools/
├── common.py              — MODIFY: add TEARDOWN_DATA_DIR, SAVEGAME_PATH constants
├── deepcheck.py           — CREATE: Layer 1 semantic analyzer (6 validators)
├── injector.py            — CREATE: Layer 2 diagnostic code injection/cleanup
├── gamerunner.py           — CREATE: Layer 3 game launch, input sim, screenshots
├── test.py                — CREATE: Layer 4 orchestrator + CLI + report generator
├── test_config.json       — GENERATED: by --setup (menu coordinates, exe path)
├── test_results/          — GENERATED: reports + screenshots per mod per run
tests/
├── test_deepcheck.py      — CREATE: tests for all 6 validators
├── test_injector.py       — CREATE: tests for injection + cleanup
├── test_gamerunner.py     — CREATE: tests for game runner (mocked, no real game)
├── test_test_cli.py       — CREATE: integration tests for CLI
├── fixtures/
│   └── deepcheck/         — CREATE: sample mods for semantic analysis
│       ├── complete_gun/  — mod with all chains valid
│       ├── broken_chain/  — mod with missing ServerCall target
│       ├── wrong_side/    — mod with Shoot on client
│       ├── missing_asset/ — mod referencing nonexistent sound file
│       └── id_mismatch/   — mod with RegisterTool/SetToolEnabled ID mismatch
```

---

## Task 1: Add shared constants to tools/common.py

**Files:**
- Modify: `tools/common.py`
- Test: `tests/test_common.py`

- [ ] **Step 1: Write tests for new constants**

```python
# Append to tests/test_common.py

from tools.common import TEARDOWN_DATA_DIR, SAVEGAME_PATH, TEARDOWN_EXE_PATHS

def test_teardown_data_dir():
    assert TEARDOWN_DATA_DIR.name == "Teardown"
    assert "AppData" in str(TEARDOWN_DATA_DIR)

def test_savegame_path():
    assert SAVEGAME_PATH.name == "savegame.xml"
    assert SAVEGAME_PATH.parent == TEARDOWN_DATA_DIR

def test_teardown_exe_paths_is_list():
    assert isinstance(TEARDOWN_EXE_PATHS, list)
    assert len(TEARDOWN_EXE_PATHS) > 0
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_common.py -v -k "teardown_data or savegame or exe_paths"`
Expected: FAIL — names not imported

- [ ] **Step 3: Add constants to common.py**

Add to `tools/common.py` after the existing constants:

```python
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
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_common.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
cd C:/Users/trust/teardown-mp-patches && git add tools/common.py tests/test_common.py && git commit -m "feat: add Teardown paths and test infrastructure constants to common.py"
```

---

## Task 2: Deep Semantic Analyzer — Asset Validator (1.4)

Starting with the simplest validator to establish the `deepcheck.py` module pattern.

**Files:**
- Create: `tools/deepcheck.py`
- Create: `tests/test_deepcheck.py`
- Create: `tests/fixtures/deepcheck/missing_asset/` (test mod)

- [ ] **Step 1: Create test fixture — mod with missing asset reference**

Create `tests/fixtures/deepcheck/missing_asset/info.txt`:
```
name = Missing Asset Test
version = 2
```

Create `tests/fixtures/deepcheck/missing_asset/main.lua`:
```lua
#version 2
#include "script/include/player.lua"

players = {}
function createPlayerData() return { ammo = 7 } end

function server.init()
    RegisterTool("missingtool", "Missing Tool", "MOD/vox/tool.vox", 5)
end

function client.tick(dt)
    for p in Players() do
        if GetPlayerTool(p) == "missingtool" then
            PlaySound(LoadSound("MOD/snd/shoot.ogg"), GetPlayerEyeTransform(p).pos)
        end
    end
end
```

Note: `vox/tool.vox` and `snd/shoot.ogg` do NOT exist in this fixture → asset validator should flag both.

- [ ] **Step 2: Write tests for asset validator**

Create `tests/test_deepcheck.py`:
```python
"""Tests for tools/deepcheck.py — deep semantic analysis."""

import pytest
from pathlib import Path

from tools.deepcheck import check_assets, AssetFinding

FIXTURES = Path(__file__).parent / "fixtures" / "deepcheck"


class TestAssetValidator:
    def test_missing_vox_flagged(self):
        mod_dir = FIXTURES / "missing_asset"
        findings = check_assets(mod_dir)
        vox_findings = [f for f in findings if "vox/tool.vox" in f.path]
        assert len(vox_findings) == 1
        assert vox_findings[0].status == "FAIL"

    def test_missing_sound_flagged(self):
        mod_dir = FIXTURES / "missing_asset"
        findings = check_assets(mod_dir)
        snd_findings = [f for f in findings if "snd/shoot.ogg" in f.path]
        assert len(snd_findings) == 1
        assert snd_findings[0].status == "FAIL"

    def test_existing_asset_passes(self, tmp_path):
        # Create a mod with an actual asset file present
        mod = tmp_path / "good_mod"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Good\nversion = 2")
        (mod / "snd").mkdir()
        (mod / "snd" / "bang.ogg").write_bytes(b"fake")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'PlaySound(LoadSound("MOD/snd/bang.ogg"))\n'
        )
        findings = check_assets(mod)
        assert all(f.status == "PASS" for f in findings)

    def test_no_assets_returns_empty(self, tmp_path):
        mod = tmp_path / "no_assets"
        mod.mkdir()
        (mod / "info.txt").write_text("name = NoAssets\nversion = 2")
        (mod / "main.lua").write_text('#version 2\n-- no asset refs\n')
        findings = check_assets(mod)
        assert findings == []
```

- [ ] **Step 3: Run tests, verify they fail**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_deepcheck.py::TestAssetValidator -v`
Expected: FAIL — module doesn't exist

- [ ] **Step 4: Implement asset validator**

Create `tools/deepcheck.py`:
```python
"""Deep semantic analysis for Teardown v2 mods.

Traces code logic chains, validates assets, cross-references IDs.
Complements lint.py (single-line regex) with multi-function analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from tools.common import read_lua_files


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    """Single finding from a deepcheck validator."""
    validator: str
    status: str  # PASS, FAIL, WARN, INCONCLUSIVE
    detail: str
    line: int = 0
    file: str = ""

@dataclass
class AssetFinding(Finding):
    """Asset validation finding."""
    path: str = ""  # the asset path referenced in code


@dataclass
class ChainFinding(Finding):
    """Chain validation finding (firing, effect, HUD)."""
    chain: list[str] = field(default_factory=list)  # traced links


@dataclass
class DeepcheckReport:
    """Complete deepcheck results for one mod."""
    mod_name: str
    assets: list[AssetFinding] = field(default_factory=list)
    firing_chain: list[ChainFinding] = field(default_factory=list)
    effect_chain: list[ChainFinding] = field(default_factory=list)
    hud: list[Finding] = field(default_factory=list)
    id_xref: list[Finding] = field(default_factory=list)
    servercall_params: list[Finding] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        all_findings = (
            self.assets + self.firing_chain + self.effect_chain +
            self.hud + self.id_xref + self.servercall_params
        )
        if any(f.status == "FAIL" for f in all_findings):
            return "FAIL"
        if any(f.status == "INCONCLUSIVE" for f in all_findings):
            return "INCONCLUSIVE"
        if any(f.status == "WARN" for f in all_findings):
            return "WARN"
        return "PASS"


# ---------------------------------------------------------------------------
# 1.4 Asset Validator
# ---------------------------------------------------------------------------

# Matches "MOD/path/to/file.ext" in Lua code
_ASSET_REF_RE = re.compile(r'"(MOD/[^"]+\.(ogg|vox|png|jpg|xml|kv6))"')


def check_assets(mod_dir: Path) -> list[AssetFinding]:
    """Check that all MOD/ asset references point to existing files."""
    findings = []
    seen = set()

    for rel_path, source in read_lua_files(mod_dir):
        for m in _ASSET_REF_RE.finditer(source):
            asset_ref = m.group(1)  # e.g. "MOD/snd/shoot.ogg"
            if asset_ref in seen:
                continue
            seen.add(asset_ref)

            # MOD/ maps to the mod's root directory
            local_path = asset_ref.replace("MOD/", "", 1)
            full_path = mod_dir / local_path

            if full_path.exists():
                findings.append(AssetFinding(
                    validator="ASSET",
                    status="PASS",
                    detail=f"Asset found: {local_path}",
                    file=rel_path,
                    path=local_path,
                ))
            else:
                # Find the line number for better reporting
                line_no = 0
                for i, line in enumerate(source.splitlines(), 1):
                    if asset_ref in line:
                        line_no = i
                        break
                findings.append(AssetFinding(
                    validator="ASSET",
                    status="FAIL",
                    detail=f"Asset NOT found: {local_path}",
                    file=rel_path,
                    line=line_no,
                    path=local_path,
                ))

    return findings
```

- [ ] **Step 5: Run tests, verify they pass**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_deepcheck.py::TestAssetValidator -v`
Expected: all PASS

- [ ] **Step 6: Commit**

```bash
cd C:/Users/trust/teardown-mp-patches && git add tools/deepcheck.py tests/test_deepcheck.py tests/fixtures/deepcheck/ && git commit -m "feat: add deepcheck module with asset validator"
```

---

## Task 3: Deep Semantic Analyzer — ID Cross-Reference Validator (1.5)

**Files:**
- Modify: `tools/deepcheck.py`
- Modify: `tests/test_deepcheck.py`
- Create: `tests/fixtures/deepcheck/id_mismatch/`
- Create: `tests/fixtures/deepcheck/complete_gun/`

- [ ] **Step 1: Create test fixtures**

Create `tests/fixtures/deepcheck/id_mismatch/info.txt`:
```
name = ID Mismatch Test
version = 2
```

Create `tests/fixtures/deepcheck/id_mismatch/main.lua`:
```lua
#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7 } end
function server.init()
    RegisterTool("mygun", "My Gun", "MOD/vox/gun.vox", 5)
    SetString("game.tool.mygun.ammo.display", "")
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("MyGun", true, p)
        SetToolAmmo("my_gun", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
end
function client.draw()
    local p = GetLocalPlayer()
    if not p then return end
    if GetPlayerTool(p) == "MYGUN" then
        UiText("ammo: 7")
    end
end
```

Note: RegisterTool uses `"mygun"`, SetToolEnabled uses `"MyGun"`, SetToolAmmo uses `"my_gun"`, GetPlayerTool uses `"MYGUN"` — 4 different strings for the same tool.

Create `tests/fixtures/deepcheck/complete_gun/info.txt`:
```
name = Complete Gun Test
version = 2
```

Create `tests/fixtures/deepcheck/complete_gun/main.lua`:
```lua
#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7, coolDown = 0 } end
function server.init()
    RegisterTool("pistol", "Pistol", "MOD/vox/pistol.vox", 5)
    SetString("game.tool.pistol.ammo.display", "")
    SetToolAmmoPickupAmount("pistol", 7)
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("pistol", true, p)
        SetToolAmmo("pistol", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        local data = players[p]
        if not data then return end
        data.coolDown = math.max(0, data.coolDown - dt)
    end
end
function server.shoot(p, pos, dir)
    local data = players[p]
    if not data or data.ammo <= 0 or data.coolDown > 0 then return end
    Shoot(pos, dir, "bullet", 1.0, 100, p, "pistol")
    data.ammo = data.ammo - 1
    data.coolDown = 0.15
    ClientCall(0, "client.onShoot", pos, dir)
    ClientCall(p, "client.onRecoil")
end
function client.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
    end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        if IsPlayerLocal(p) and GetPlayerTool(p) == "pistol" then
            if InputPressed("usetool", p) then
                local hit, dist, normal, shape = GetPlayerAimInfo(p)
                local eye = GetPlayerEyeTransform(p)
                local dir = TransformToParentVec(eye, Vec(0, 0, -1))
                ServerCall("server.shoot", p, eye.pos, dir)
            end
        end
    end
end
function client.onShoot(pos, dir)
    PlaySound(LoadSound("MOD/snd/shoot.ogg"), pos)
    SpawnParticle("smoke", pos, Vec(0, 0.5, 0), 0.5, 1)
end
function client.onRecoil()
    ShakeCamera(0.2)
end
function client.draw()
    local p = GetLocalPlayer()
    if not p then return end
    local data = players[p]
    if not data then return end
    if GetPlayerTool(p) == "pistol" then
        UiAlign("right")
        UiTranslate(UiWidth() - 50, UiHeight() - 80)
        UiText(data.ammo)
    end
end
```

Also create the assets so asset validator passes:

Create directories and placeholder files for `tests/fixtures/deepcheck/complete_gun/vox/` and `tests/fixtures/deepcheck/complete_gun/snd/`.

- [ ] **Step 2: Write tests for ID cross-reference validator**

Append to `tests/test_deepcheck.py`:

```python
from tools.deepcheck import check_id_xref


class TestIdCrossRef:
    def test_mismatched_ids_flagged(self):
        mod_dir = FIXTURES / "id_mismatch"
        findings = check_id_xref(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        # Should flag SetToolEnabled("MyGun"), SetToolAmmo("my_gun"), GetPlayerTool("MYGUN")
        assert len(fails) >= 2  # at least the mismatches vs RegisterTool

    def test_consistent_ids_pass(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_id_xref(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0

    def test_missing_set_tool_ammo_flagged(self, tmp_path):
        mod = tmp_path / "no_ammo"
        mod.mkdir()
        (mod / "info.txt").write_text("name = NoAmmo\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.init()\n'
            '    RegisterTool("gun", "Gun", "MOD/vox/g.vox", 5)\n'
            'end\n'
            'function server.tick(dt)\n'
            '    for p in PlayersAdded() do\n'
            '        SetToolEnabled("gun", true, p)\n'
            '    end\n'
            'end\n'
        )
        findings = check_id_xref(mod)
        warns = [f for f in findings if f.status == "WARN" and "SetToolAmmo" in f.detail]
        assert len(warns) == 1
```

- [ ] **Step 3: Run tests, verify they fail**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_deepcheck.py::TestIdCrossRef -v`
Expected: FAIL

- [ ] **Step 4: Implement ID cross-reference validator**

Add to `tools/deepcheck.py`:

```python
# ---------------------------------------------------------------------------
# 1.5 ID Cross-Reference Validator
# ---------------------------------------------------------------------------

_REGISTER_TOOL_ID_RE = re.compile(r'RegisterTool\s*\(\s*"([^"]+)"')
_SET_TOOL_ENABLED_ID_RE = re.compile(r'SetToolEnabled\s*\(\s*"([^"]+)"')
_SET_TOOL_AMMO_ID_RE = re.compile(r'SetToolAmmo\s*\(\s*"([^"]+)"')
_GET_PLAYER_TOOL_ID_RE = re.compile(r'GetPlayerTool\s*\([^)]*\)\s*==\s*"([^"]+)"')
_AMMO_DISPLAY_ID_RE = re.compile(r'SetString\s*\(\s*"game\.tool\.([^.]+)\.ammo\.display"')
_SET_AMMO_PICKUP_ID_RE = re.compile(r'SetToolAmmoPickupAmount\s*\(\s*"([^"]+)"')


def check_id_xref(mod_dir: Path) -> list[Finding]:
    """Verify tool IDs are consistent across Register/Enable/Ammo/HUD."""
    findings = []
    all_source = ""
    for _, source in read_lua_files(mod_dir):
        all_source += source + "\n"

    registered_ids = _REGISTER_TOOL_ID_RE.findall(all_source)
    if not registered_ids:
        return []  # not a tool mod

    for tool_id in registered_ids:
        # Check SetToolEnabled uses same ID
        enabled_ids = _SET_TOOL_ENABLED_ID_RE.findall(all_source)
        if tool_id not in enabled_ids:
            # Check for case-insensitive match (common mistake)
            case_matches = [eid for eid in enabled_ids if eid.lower() == tool_id.lower()]
            if case_matches:
                findings.append(Finding(
                    validator="ID-XREF",
                    status="FAIL",
                    detail=f'Case mismatch: RegisterTool("{tool_id}") vs SetToolEnabled("{case_matches[0]}")',
                ))
            elif enabled_ids:
                findings.append(Finding(
                    validator="ID-XREF",
                    status="FAIL",
                    detail=f'SetToolEnabled uses "{enabled_ids[0]}" but RegisterTool uses "{tool_id}"',
                ))
            else:
                findings.append(Finding(
                    validator="ID-XREF",
                    status="WARN",
                    detail=f'No SetToolEnabled found for "{tool_id}" — tool may not appear for joining players',
                ))

        # Check SetToolAmmo uses same ID
        ammo_ids = _SET_TOOL_AMMO_ID_RE.findall(all_source)
        if tool_id not in ammo_ids:
            case_matches = [aid for aid in ammo_ids if aid.lower() == tool_id.lower()]
            if case_matches:
                findings.append(Finding(
                    validator="ID-XREF",
                    status="FAIL",
                    detail=f'Case mismatch: RegisterTool("{tool_id}") vs SetToolAmmo("{case_matches[0]}")',
                ))
            else:
                findings.append(Finding(
                    validator="ID-XREF",
                    status="WARN",
                    detail=f'No SetToolAmmo found for "{tool_id}" — tool may not appear in toolbar',
                ))

        # Check GetPlayerTool uses same ID (HUD guard)
        hud_ids = _GET_PLAYER_TOOL_ID_RE.findall(all_source)
        if hud_ids and tool_id not in hud_ids:
            case_matches = [hid for hid in hud_ids if hid.lower() == tool_id.lower()]
            if case_matches:
                findings.append(Finding(
                    validator="ID-XREF",
                    status="FAIL",
                    detail=f'Case mismatch: RegisterTool("{tool_id}") vs GetPlayerTool check "{case_matches[0]}"',
                ))

    return findings
```

- [ ] **Step 5: Run tests, verify they pass**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_deepcheck.py::TestIdCrossRef -v`
Expected: all PASS

- [ ] **Step 6: Commit**

```bash
cd C:/Users/trust/teardown-mp-patches && git add tools/deepcheck.py tests/test_deepcheck.py tests/fixtures/deepcheck/ && git commit -m "feat: add ID cross-reference validator to deepcheck"
```

---

## Task 4: Deep Semantic Analyzer — Firing Chain Validator (1.1)

**Files:**
- Modify: `tools/deepcheck.py`
- Modify: `tests/test_deepcheck.py`
- Create: `tests/fixtures/deepcheck/broken_chain/`
- Create: `tests/fixtures/deepcheck/wrong_side/`

- [ ] **Step 1: Create test fixtures**

Create `tests/fixtures/deepcheck/broken_chain/info.txt`:
```
name = Broken Chain Test
version = 2
```

Create `tests/fixtures/deepcheck/broken_chain/main.lua` — client ServerCalls `server.shoot` but only `server.fire` exists:
```lua
#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7 } end
function server.init()
    RegisterTool("bchain", "Broken", "MOD/vox/gun.vox", 5)
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("bchain", true, p)
        SetToolAmmo("bchain", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
end
function server.fire(p, pos, dir)
    Shoot(pos, dir, "bullet", 1.0, 100, p, "bchain")
end
function client.tick(dt)
    for p in PlayersAdded() do players[p] = createPlayerData() end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        if IsPlayerLocal(p) and GetPlayerTool(p) == "bchain" then
            if InputPressed("usetool", p) then
                local eye = GetPlayerEyeTransform(p)
                local dir = TransformToParentVec(eye, Vec(0, 0, -1))
                ServerCall("server.shoot", p, eye.pos, dir)
            end
        end
    end
end
```

Create `tests/fixtures/deepcheck/wrong_side/info.txt`:
```
name = Wrong Side Test
version = 2
```

Create `tests/fixtures/deepcheck/wrong_side/main.lua` — Shoot() called in client code:
```lua
#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7 } end
function server.init()
    RegisterTool("wside", "Wrong", "MOD/vox/gun.vox", 5)
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("wside", true, p)
        SetToolAmmo("wside", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
end
function client.tick(dt)
    for p in PlayersAdded() do players[p] = createPlayerData() end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        if IsPlayerLocal(p) and GetPlayerTool(p) == "wside" then
            if InputPressed("usetool", p) then
                local eye = GetPlayerEyeTransform(p)
                local dir = TransformToParentVec(eye, Vec(0, 0, -1))
                Shoot(eye.pos, dir, "bullet", 1.0, 100, p, "wside")
            end
        end
    end
end
```

- [ ] **Step 2: Write tests**

```python
from tools.deepcheck import check_firing_chain


class TestFiringChain:
    def test_complete_chain_passes(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_firing_chain(mod_dir)
        assert all(f.status == "PASS" for f in findings)

    def test_missing_server_target_fails(self):
        mod_dir = FIXTURES / "broken_chain"
        findings = check_firing_chain(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert any("target" in f.detail.lower() or "not found" in f.detail.lower() for f in fails)

    def test_shoot_on_client_fails(self):
        mod_dir = FIXTURES / "wrong_side"
        findings = check_firing_chain(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert any("client" in f.detail.lower() for f in fails)

    def test_no_usetool_input_is_inconclusive(self, tmp_path):
        """Non-weapon mod with no usetool input -> INCONCLUSIVE, not FAIL."""
        mod = tmp_path / "util_mod"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Util\nversion = 2")
        (mod / "main.lua").write_text('#version 2\nfunction server.init()\nend\n')
        findings = check_firing_chain(mod)
        # No usetool found = not a weapon = empty/inconclusive, not FAIL
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0
```

- [ ] **Step 3: Run tests, verify they fail**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_deepcheck.py::TestFiringChain -v`

- [ ] **Step 4: Implement firing chain validator**

Add `check_firing_chain(mod_dir: Path) -> list[ChainFinding]` to `tools/deepcheck.py`.

The implementation should:
1. Find all `InputPressed("usetool"` / `InputDown("usetool"` calls
2. On the same or nearby lines, find `ServerCall("server.XXX", ...)` calls
3. Verify `server.XXX` function is defined in the source
4. Inside `server.XXX`, verify `Shoot()` or `QueryShot()` + `ApplyPlayerDamage()` is called
5. Check `Shoot()` is NOT called in client code context
6. If `Shoot()` is found, verify damage param (2nd-to-last positional arg) is not literal 0

Return `ChainFinding` with `chain=["usetool", "ServerCall:server.shoot", "Shoot"]` for the traced path.

- [ ] **Step 5: Run tests, verify they pass**

- [ ] **Step 6: Commit**

```bash
git add tools/deepcheck.py tests/test_deepcheck.py tests/fixtures/deepcheck/ && git commit -m "feat: add firing chain validator to deepcheck"
```

---

## Task 5: Deep Semantic Analyzer — Effect Chain Validator (1.2)

**Files:**
- Modify: `tools/deepcheck.py`
- Modify: `tests/test_deepcheck.py`

- [ ] **Step 1: Write tests for effect chain validator**

Test cases using `complete_gun` fixture + `tmp_path`:
- `complete_gun` fixture passes (has ClientCall → client.onShoot → PlaySound + SpawnParticle)
- Mod with PlaySound in server.tick → FAIL ("server-side effects")
- Mod with Shoot but no ClientCall after → WARN ("silent weapon")
- Mod with ClientCall(p, ...) for world effects instead of ClientCall(0, ...) → WARN

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_deepcheck.py::TestEffectChain -v`

- [ ] **Step 3: Implement effect chain validator**

Add `check_effect_chain(mod_dir: Path) -> list[ChainFinding]` to `tools/deepcheck.py`.

The implementation should:
1. Find all server functions that call `Shoot()`, `Explosion()`, `QueryShot()`
2. From those functions, find `ClientCall(0, "client.X", ...)` calls
3. Verify `client.X` function exists
4. Inside `client.X`, verify `PlaySound()` or `SpawnParticle()` or `PointLight()` is called
5. Check that `PlaySound`/`SpawnParticle` are NOT in server functions (server_side_effects)

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add tools/deepcheck.py tests/test_deepcheck.py && git commit -m "feat: add effect chain validator to deepcheck"
```

---

## Task 5b: Deep Semantic Analyzer — HUD + ServerCall + Orchestrator (1.3, 1.6)

**Files:**
- Modify: `tools/deepcheck.py`
- Modify: `tests/test_deepcheck.py`

- [ ] **Step 1: Write tests for HUD validator**

Test cases:
- `complete_gun` fixture passes (client.draw references data.ammo, uses GetPlayerTool guard)
- Mod with no client.draw → WARN (not FAIL — some mods legitimately have no HUD)
- Mod with client.draw but no GetPlayerTool guard → WARN

- [ ] **Step 2: Write tests for ServerCall param validator**

Test cases:
- `complete_gun` passes (ServerCall arg count matches function params)
- Mod with `ServerCall("server.shoot", pos, dir)` but `function server.shoot(p, pos, dir)` → FAIL (missing player ID — 2 args sent, 3 expected)
- Mod with ServerCall to non-existent function → FAIL

- [ ] **Step 3: Write test for run_deepcheck orchestrator**

```python
class TestRunDeepcheck:
    def test_orchestrator_runs_all_validators(self):
        mod_dir = FIXTURES / "complete_gun"
        report = run_deepcheck(mod_dir, is_weapon=True)
        assert report.mod_name == "complete_gun"
        assert report.overall_status == "PASS"
        assert len(report.assets) >= 0
        assert len(report.id_xref) >= 0

    def test_non_weapon_skips_chain_validators(self, tmp_path):
        mod = tmp_path / "env_mod"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Env\nversion = 2")
        (mod / "main.lua").write_text('#version 2\nfunction server.init()\nend\n')
        report = run_deepcheck(mod, is_weapon=False)
        assert report.firing_chain == []
        assert report.effect_chain == []
```

- [ ] **Step 4: Run all tests, verify they fail**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_deepcheck.py -v`

- [ ] **Step 5: Implement HUD validator, ServerCall validator, and orchestrator**

Add to `tools/deepcheck.py`:
- `check_hud(mod_dir: Path) -> list[Finding]`
- `check_servercall_params(mod_dir: Path) -> list[Finding]`
- `run_deepcheck(mod_dir: Path, is_weapon: bool = True) -> DeepcheckReport`
- Add `to_dict()` method to `Finding` dataclass for lint.py interop

```python
def run_deepcheck(mod_dir: Path, is_weapon: bool = True) -> DeepcheckReport:
    """Run all deepcheck validators on a mod and return a report."""
    report = DeepcheckReport(mod_name=mod_dir.name)
    report.assets = check_assets(mod_dir)
    report.id_xref = check_id_xref(mod_dir)
    report.servercall_params = check_servercall_params(mod_dir)
    if is_weapon:
        report.firing_chain = check_firing_chain(mod_dir)
        report.effect_chain = check_effect_chain(mod_dir)
        report.hud = check_hud(mod_dir)
    return report
```

- [ ] **Step 6: Run tests, verify they pass**

- [ ] **Step 7: Commit**

```bash
git add tools/deepcheck.py tests/test_deepcheck.py && git commit -m "feat: add HUD, ServerCall validators and deepcheck orchestrator"
```

---

## Task 6: Diagnostic Injector (Layer 2)

**Files:**
- Create: `tools/injector.py`
- Create: `tests/test_injector.py`

- [ ] **Step 1: Write tests for injection**

```python
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
        main = mod / "main.lua"
        main.write_text(SAMPLE_MOD)
        inject_diagnostics(mod)
        injected = main.read_text()
        assert "__diag" in injected
        assert "__origShoot" in injected
        assert "DebugWatch" in injected

    def test_inject_creates_backup(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        inject_diagnostics(mod)
        assert (mod / "main.lua.testbackup").exists()

    def test_restore_from_backup(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        inject_diagnostics(mod)
        restore_from_backup(mod)
        assert (mod / "main.lua").read_text() == SAMPLE_MOD
        assert not (mod / "main.lua.testbackup").exists()

    def test_inject_preserves_version_and_includes(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        lines = injected.splitlines()
        assert lines[0] == "#version 2"
        assert '#include "script/include/player.lua"' in lines[1]

    def test_inject_increments_tick_counters(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        assert "__diag.serverTicks = __diag.serverTicks + 1" in injected
        assert "__diag.clientTicks = __diag.clientTicks + 1" in injected

    def test_inject_writes_savegame_registry(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text(SAMPLE_MOD)
        inject_diagnostics(mod)
        injected = (mod / "main.lua").read_text()
        assert 'SetString("savegame.mod.diag.' in injected

    def test_orphan_backup_restored_on_startup(self, tmp_path):
        mod = tmp_path / "test_mod"
        mod.mkdir()
        (mod / "main.lua").write_text("-- injected version")
        (mod / "main.lua.testbackup").write_text(SAMPLE_MOD)
        restore_from_backup(mod)
        assert (mod / "main.lua").read_text() == SAMPLE_MOD
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_injector.py -v`

- [ ] **Step 3: Implement injector**

Create `tools/injector.py`:

The implementation should:
1. Read `main.lua`
2. Back up to `main.lua.testbackup`
3. Find all `#version` and `#include` lines at the top — these stay first
4. After includes, insert the `__diag` table and API wrapper block
5. Find `function server.tick(`, `function client.tick(`, `function client.draw(` — insert counter increments as the first line inside each
6. Find the `end` that closes `server.tick` and `client.tick` — insert DebugWatch + SetString calls before it
7. Write modified source back

Key constant: `DIAG_PREFIX = "__diag"` — all injected names use this prefix.

API wrappers for: `Shoot`, `QueryShot`, `ApplyPlayerDamage`, `Explosion`, `MakeHole`, `PlaySound`, `SpawnParticle`, `PointLight`, `RegisterTool`, `SetToolEnabled`, `SetToolAmmo`.

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add tools/injector.py tests/test_injector.py && git commit -m "feat: add diagnostic injector for runtime instrumentation"
```

---

## Task 7: Game Runner — Core Launch/Kill/Cleanup (Layer 3)

**Files:**
- Create: `tools/gamerunner.py`
- Create: `tests/test_gamerunner.py`

- [ ] **Step 1: Write tests (mocked — no real game launch)**

```python
"""Tests for tools/gamerunner.py — game launch/kill/cleanup.

All tests use mocks — they never actually launch Teardown.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from tools.gamerunner import (
    find_teardown_exe,
    acquire_test_lock,
    release_test_lock,
    backup_teardown_config,
    restore_teardown_config,
    parse_savegame_diagnostics,
    GameRunnerConfig,
)


class TestFindTeardownExe:
    def test_returns_path_when_found(self, tmp_path):
        exe = tmp_path / "teardown.exe"
        exe.write_bytes(b"fake")
        with patch("tools.gamerunner.TEARDOWN_EXE_PATHS", [exe]):
            assert find_teardown_exe() == exe

    def test_returns_none_when_not_found(self):
        with patch("tools.gamerunner.TEARDOWN_EXE_PATHS", [Path("/nonexistent/teardown.exe")]):
            assert find_teardown_exe() is None


class TestTestLock:
    def test_acquire_and_release(self, tmp_path):
        lock = tmp_path / ".test_lock"
        with patch("tools.gamerunner.TEST_LOCK_PATH", lock):
            assert acquire_test_lock()
            assert lock.exists()
            release_test_lock()
            assert not lock.exists()

    def test_acquire_fails_when_locked(self, tmp_path):
        lock = tmp_path / ".test_lock"
        lock.write_text(json.dumps({"pid": 999999999}))  # non-existent PID
        with patch("tools.gamerunner.TEST_LOCK_PATH", lock):
            # Stale lock (dead PID) should be cleared
            assert acquire_test_lock()


class TestSavegameDiagnostics:
    def test_parse_diagnostics_from_xml(self, tmp_path):
        xml = tmp_path / "savegame.xml"
        xml.write_text('''<?xml version="1.0"?>
<registry>
    <entry key="savegame.mod.diag.ticks" value="100,200"/>
    <entry key="savegame.mod.diag.combat" value="5,2,3,1"/>
    <entry key="savegame.mod.diag.effects" value="10,15,3"/>
    <entry key="savegame.mod.diag.tools" value="pistol"/>
    <entry key="savegame.mod.diag.errors" value="0"/>
</registry>''')
        data = parse_savegame_diagnostics(xml)
        assert data["server_ticks"] == 100
        assert data["client_ticks"] == 200
        assert data["shoot_count"] == 5
        assert data["sound_count"] == 10
        assert data["tool_ids"] == ["pistol"]
        assert data["error_count"] == 0

    def test_parse_empty_savegame(self, tmp_path):
        xml = tmp_path / "savegame.xml"
        xml.write_text('<?xml version="1.0"?><registry></registry>')
        data = parse_savegame_diagnostics(xml)
        assert data["server_ticks"] == 0
        assert data["shoot_count"] == 0
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement core game runner functions**

Create `tools/gamerunner.py` with:
- `find_teardown_exe() -> Path | None`
- `acquire_test_lock() -> bool` / `release_test_lock()`
- `backup_teardown_config()` / `restore_teardown_config()`
- `set_windowed_mode(width=1280, height=720)`
- `parse_savegame_diagnostics(savegame_path: Path) -> dict`
- `GameRunnerConfig` dataclass (exe path, menu coords, etc.)

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add tools/gamerunner.py tests/test_gamerunner.py && git commit -m "feat: add game runner core — exe finder, lock, config, savegame parser"
```

---

## Task 8: Game Runner — Screenshot Capture + Input Simulation

**Files:**
- Modify: `tools/gamerunner.py`
- Modify: `tests/test_gamerunner.py`

- [ ] **Step 1: Write tests for screenshot capture**

```python
class TestScreenCapture:
    def test_is_black_frame(self):
        from tools.gamerunner import is_black_frame
        from PIL import Image
        # All-black image
        black = Image.new("RGB", (100, 100), (0, 0, 0))
        assert is_black_frame(black) is True
        # Normal image
        normal = Image.new("RGB", (100, 100), (128, 128, 128))
        assert is_black_frame(normal) is False
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement screenshot and input functions**

Add to `tools/gamerunner.py`:
- `capture_screenshot(output_path: Path) -> bool` — uses `mss`, detects black frames
- `is_black_frame(img: PIL.Image) -> bool` — >90% pixels near-black
- `run_input_sequence(mod_type: str, tool_ids: list[str])` — pyautogui sequences
- `run_game_test(mod_dir: Path, config: GameRunnerConfig) -> GameTestResult` — full orchestration

`GameTestResult` dataclass:
```python
@dataclass
class GameTestResult:
    mod_loaded: bool
    compile_errors: list[dict]
    runtime_errors: list[dict]
    diagnostic_data: dict
    screenshot_paths: list[Path]
    session_duration: float
    exit_code: int | None
    crashed: bool
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add tools/gamerunner.py tests/test_gamerunner.py && git commit -m "feat: add screenshot capture and input simulation to game runner"
```

---

## Task 9: Test Harness Mod

**Files:**
- Create: `tools/testmap/info.txt`
- Create: `tools/testmap/main.lua`
- Create: `tools/testmap/main.xml`
- Modify: `tools/gamerunner.py` — add `install_test_harness()` function

- [ ] **Step 1: Create test harness mod files**

Create `tools/testmap/info.txt`:
```
name = Test Harness
author = Teardown MP Patcher
description = Automated testing environment — do not delete
version = 2
```

Create `tools/testmap/main.lua`:
```lua
#version 2
#include "script/include/player.lua"

local toolId = ""
local selectTimer = 0

function server.init()
    toolId = GetString("savegame.mod.test.toolid")
end

function server.tick(dt)
    for p in PlayersAdded() do
        selectTimer = 2.0  -- wait 2s for mods to register tools
    end
    if selectTimer > 0 then
        selectTimer = selectTimer - dt
        if selectTimer <= 0 and toolId ~= "" then
            for p in Players() do
                SetPlayerTool(toolId, p)
            end
        end
    end
end
```

Create `tools/testmap/main.xml`:
```xml
<scene version="2" shadowVolume="50 20 50">
    <environment template="sunset"/>
    <group pos="0 0 0">
        <vox pos="0 0 -5" file="LEVEL/wall.vox" object="wall"/>
        <vox pos="0 -0.5 0" file="LEVEL/floor.vox" object="floor"/>
    </group>
    <spawnpoint pos="0 1.5 0" rot="0 0 0"/>
</scene>
```

**Vox files:** The test map needs `wall.vox` and `floor.vox`. These are minimal MagicaVoxel format files. Create them programmatically in `install_test_harness()` using the MagicaVoxel binary format (4-byte magic "VOX ", version, MAIN chunk, SIZE chunk with dimensions, XYZI chunk with voxel data, RGBA palette). A 10x10x1 flat slab is sufficient for both wall and floor. The implementation should include a `create_minimal_vox(width, height, depth, output_path)` helper function.

- [ ] **Step 2: Write test for install function**

```python
class TestInstallHarness:
    def test_installs_to_mods_dir(self, tmp_path):
        from tools.gamerunner import install_test_harness
        with patch("tools.gamerunner.TEST_HARNESS_DIR", tmp_path / "__test_harness"):
            install_test_harness()
            assert (tmp_path / "__test_harness" / "info.txt").exists()
            assert (tmp_path / "__test_harness" / "main.lua").exists()
            assert (tmp_path / "__test_harness" / "main.xml").exists()
            assert (tmp_path / "__test_harness" / "wall.vox").exists()
            assert (tmp_path / "__test_harness" / "floor.vox").exists()

    def test_vox_files_are_valid(self, tmp_path):
        from tools.gamerunner import install_test_harness
        with patch("tools.gamerunner.TEST_HARNESS_DIR", tmp_path / "__test_harness"):
            install_test_harness()
            # MagicaVoxel files start with "VOX " magic bytes
            wall = (tmp_path / "__test_harness" / "wall.vox").read_bytes()
            assert wall[:4] == b"VOX "
```

- [ ] **Step 3: Implement install_test_harness()**

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add tools/testmap/ tools/gamerunner.py tests/test_gamerunner.py && git commit -m "feat: add test harness mod for automated testing environment"
```

---

## Task 10: Test Orchestrator + CLI (Layer 4)

**Files:**
- Create: `tools/test.py`
- Create: `tests/test_test_cli.py`

- [ ] **Step 1: Write tests for report generation**

```python
"""Tests for tools/test.py — test orchestrator and CLI."""

import pytest
from pathlib import Path

from tools.test import generate_report, TestReport


class TestReportGeneration:
    def test_all_pass_report(self):
        from tools.deepcheck import DeepcheckReport
        static = DeepcheckReport(mod_name="TestMod")
        report = generate_report(
            mod_name="TestMod",
            static_report=static,
            runtime=None,
            test_type="static",
        )
        assert report.overall_status == "PASS"
        assert "TestMod" in report.to_text()

    def test_fail_report_from_static(self):
        from tools.deepcheck import DeepcheckReport, Finding
        static = DeepcheckReport(mod_name="BadMod")
        static.id_xref = [Finding(
            validator="ID-XREF", status="FAIL",
            detail="Case mismatch: RegisterTool vs SetToolEnabled"
        )]
        report = generate_report(
            mod_name="BadMod", static_report=static,
            runtime=None, test_type="static",
        )
        assert report.overall_status == "FAIL"
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement test orchestrator**

Create `tools/test.py`:

```python
"""Autonomous test platform for Teardown MP mods.

Usage:
    python -m tools.test --mod "ModName"           # Full test
    python -m tools.test --mod "ModName" --static   # Static only
    python -m tools.test --setup                    # First-time calibration
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import click

from tools.common import LIVE_MODS_DIR, discover_mods, TEST_RESULTS_DIR
from tools.deepcheck import run_deepcheck, DeepcheckReport
from tools.audit import audit_mod  # for mod type detection


@dataclass
class TestReport:
    mod_name: str
    test_type: str  # "static", "full"
    timestamp: str = ""
    static_report: DeepcheckReport | None = None
    runtime: dict | None = None
    screenshots: list[Path] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        statuses = []
        if self.static_report:
            statuses.append(self.static_report.overall_status)
        if self.runtime:
            if self.runtime.get("crashed"):
                return "CRASH"
            if self.runtime.get("compile_errors"):
                return "FAIL"
            if self.runtime.get("runtime_errors"):
                return "FAIL"
        if not statuses:
            return "PASS"
        if "FAIL" in statuses:
            return "FAIL"
        if "INCONCLUSIVE" in statuses:
            return "INCONCLUSIVE"
        if "WARN" in statuses:
            return "WARN"
        return "PASS"

    def to_text(self) -> str:
        # Generate the full text report
        ...  # Full implementation in step 3


def generate_report(mod_name, static_report, runtime, test_type) -> TestReport:
    return TestReport(
        mod_name=mod_name,
        test_type=test_type,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        static_report=static_report,
        runtime=runtime,
    )


def run_test(mod_name: str, static_only: bool = False, verbose: bool = False) -> TestReport:
    """Run the full test pipeline on a mod."""
    mod_dirs = discover_mods(mod_name=mod_name)
    if not mod_dirs:
        raise click.ClickException(f"Mod not found: {mod_name}")
    mod_dir = mod_dirs[0]

    # Detect mod type via audit for weapon/non-weapon classification
    from tools.audit import audit_mod
    mod_features = audit_mod(mod_dir)
    is_weapon = mod_features.get("is_gun_mod", False) or mod_features.get("has_register_tool", False)

    # Layer 1: Deep semantic analysis
    static_report = run_deepcheck(mod_dir, is_weapon=is_weapon)

    runtime = None
    if not static_only:
        # Layer 2 + 3: Inject diagnostics, run game, collect data
        from tools.injector import inject_diagnostics, restore_from_backup
        from tools.gamerunner import run_game_test, GameRunnerConfig

        config = GameRunnerConfig.load()
        try:
            inject_diagnostics(mod_dir)
            runtime = run_game_test(mod_dir, config)
        finally:
            restore_from_backup(mod_dir)

    # Layer 4: Generate report
    report = generate_report(
        mod_name=mod_name,
        static_report=static_report,
        runtime=runtime,
        test_type="static" if static_only else "full",
    )

    # Save report
    _save_report(report, mod_dir)

    return report


def _save_report(report: TestReport, mod_dir: Path):
    """Save report to test_results/ModName/YYYY-MM-DD_HH-MM-SS/."""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result_dir = TEST_RESULTS_DIR / report.mod_name / ts
    result_dir.mkdir(parents=True, exist_ok=True)
    (result_dir / "report.txt").write_text(report.to_text())
    if report.runtime:
        (result_dir / "diagnostic_data.json").write_text(
            json.dumps(report.runtime, indent=2, default=str)
        )


@click.command("test")
@click.option("--mod", "mod_name", required=False, help="Mod folder name")
@click.option("--static", "static_only", is_flag=True, help="Layer 1 only, no game launch")
@click.option("--batch", default=None, help="Test category: guns, all")
@click.option("--no-input", "no_input", is_flag=True, help="Game launch without input simulation")
@click.option("--verbose", is_flag=True)
@click.option("--setup", is_flag=True, help="First-time calibration")
def test_cli(mod_name, static_only, batch, verbose, setup):
    """Run autonomous tests on Teardown mods."""
    if setup:
        from tools.gamerunner import run_setup
        run_setup()
        return

    if batch:
        # Run on all mods of a type
        mods = discover_mods()
        for mod_dir in mods:
            try:
                report = run_test(mod_dir.name, static_only=static_only, verbose=verbose)
                status = report.overall_status
                click.echo(f"  [{status}] {mod_dir.name}")
            except Exception as e:
                click.echo(f"  [ERROR] {mod_dir.name}: {e}")
        return

    if not mod_name:
        raise click.ClickException("Specify --mod or --batch")

    report = run_test(mod_name, static_only=static_only, verbose=verbose)
    click.echo(report.to_text())


if __name__ == "__main__":
    test_cli()
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/test_test_cli.py -v`

- [ ] **Step 5: Commit**

```bash
git add tools/test.py tests/test_test_cli.py && git commit -m "feat: add test orchestrator CLI with report generation"
```

---

## Task 11: Integration — Wire Layers Together + Status Integration

**Files:**
- Modify: `tools/status.py` — add test results summary
- Modify: `CLAUDE.md` — add test command to workflow

- [ ] **Step 1: Add test results to tools.status**

In `tools/status.py`, after the lint summary section, add a block that checks for recent test results in `TEST_RESULTS_DIR` and reports:
- Number of mods tested
- Last test result per mod (PASS/FAIL/WARN)
- Mods never tested

- [ ] **Step 2: Update CLAUDE.md**

Add to the "Developer Tools" table:
```
| `python -m tools.test --mod "X"` | Full autonomous test (static + game launch) |
| `python -m tools.test --mod "X" --static` | Static analysis only (no game) |
| `python -m tools.test --setup` | First-time calibration |
```

Add to the workflow section:
```
After writing or editing any mod code:
  python -m tools.lint --mod "ModName"     # Pattern check (2s)
  python -m tools.test --mod "ModName" --static  # Deep analysis (2s)
  python -m tools.test --mod "ModName"     # Full test with game launch (60s)
```

- [ ] **Step 3: Run full test suite**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/ -q`
Expected: All existing tests still pass + new tests pass

- [ ] **Step 4: Run tools.status to verify integration**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m tools.status`
Expected: Status report now includes test results section

- [ ] **Step 5: Commit**

```bash
git add tools/status.py CLAUDE.md && git commit -m "feat: integrate test platform into status report and CLAUDE.md workflow"
```

---

## Task 12: Install Dependencies + First-Time Setup

**Files:**
- Modify: `tools/gamerunner.py` — implement `run_setup()`
- Create: `requirements-test.txt` (or add to existing requirements)

- [ ] **Step 1: Create requirements file**

Create `requirements-test.txt`:
```
mss>=9.0
pyautogui>=0.9
PyGetWindow>=0.0.9
Pillow>=10.0
```

- [ ] **Step 2: Implement run_setup()**

Add to `tools/gamerunner.py`:
```python
def run_setup():
    """First-time calibration: install deps, find exe, create test harness."""
    click.echo("=== Teardown Test Platform Setup ===")

    # 1. Check Python deps
    click.echo("Checking dependencies...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-r",
                    str(Path(__file__).parent.parent / "requirements-test.txt")],
                   check=True)

    # 2. Find Teardown exe
    exe = find_teardown_exe()
    if exe:
        click.echo(f"Found Teardown: {exe}")
    else:
        click.echo("Teardown.exe not found in standard locations.")
        exe_str = click.prompt("Enter full path to teardown.exe")
        exe = Path(exe_str)
        if not exe.exists():
            raise click.ClickException(f"File not found: {exe}")

    # 3. Install test harness mod
    install_test_harness()
    click.echo("Test harness mod installed")

    # 4. Save config
    config = GameRunnerConfig(teardown_exe=exe)
    config.save()
    click.echo(f"Config saved to {TEST_CONFIG_PATH}")
    click.echo("\nSetup complete! Run: python -m tools.test --mod \"ModName\"")
```

- [ ] **Step 3: Test setup flow manually**

Run: `cd C:/Users/trust/teardown-mp-patches && python -m tools.test --setup`
Expected: Dependencies install, exe found, test harness created, config saved

- [ ] **Step 4: Commit**

```bash
git add requirements-test.txt tools/gamerunner.py && git commit -m "feat: add first-time setup flow for test platform"
```

---

## Task 13: End-to-End Validation — Static Test on Real Mod

No new files — validation that the system works on actual mods.

- [ ] **Step 1: Run static test on a real mod**

```bash
cd C:/Users/trust/teardown-mp-patches && python -m tools.test --mod "C4" --static
```

Expected: Full deepcheck report with results for all 6 validators.

- [ ] **Step 2: Fix any issues found**

If the report has false positives or crashes, fix the validators.

- [ ] **Step 3: Run static test on 5 different mod types**

```bash
python -m tools.test --mod "AK-47" --static       # standard gun
python -m tools.test --mod "C4" --static           # explosive
python -m tools.test --mod "Laser" --static        # beam weapon
python -m tools.test --mod "Grapple_Hook" --static # utility tool
python -m tools.test --mod "Katana" --static       # melee
```

- [ ] **Step 4: Verify all existing tests still pass**

```bash
cd C:/Users/trust/teardown-mp-patches && python -m pytest tests/ -q
```

- [ ] **Step 5: Commit any fixes**

```bash
git add -A && git commit -m "fix: tune deepcheck validators based on real mod testing"
```

---

## Execution Order and Dependencies

```
Task 1 (common.py constants) — no deps, foundation
  ↓
Task 2 (asset validator)     — needs common.py, creates deepcheck.py
  ↓
Task 3 (ID xref validator)   — needs deepcheck.py module (SEQUENTIAL with 2)
  ↓
Task 4 (firing chain)        — needs deepcheck.py module (SEQUENTIAL with 3)
  ↓
Task 5 (effect chain)        — needs deepcheck.py module (SEQUENTIAL with 4)
  ↓
Task 5b (HUD/SC/orchestrator) — needs deepcheck.py module (SEQUENTIAL with 5)
  ↓
Task 6 (injector)             — independent of deepcheck, can PARALLEL with 3-5b
  ↓
Task 7 (gamerunner core)      — independent, can PARALLEL with 3-6
  ↓
Task 8 (screenshots/input)    — needs gamerunner.py
  ↓
Task 9 (test harness mod)     — needs gamerunner.py
  ↓
Task 10 (orchestrator CLI)    — needs deepcheck + injector + gamerunner
  ↓
Task 11 (integration)         — needs test.py working
  ↓
Task 12 (setup flow)          — needs gamerunner.py (can run after Task 9)
  ↓
Task 13 (E2E validation)      — needs everything
```

**Parallelizable groups:**
- Tasks 3→4→5→5b MUST be sequential (all modify deepcheck.py and test_deepcheck.py)
- Tasks 6 and 7 can run in PARALLEL with each other and with 3-5b (independent modules)
- Tasks 8, 9 are sequential after 7
- Task 12 can run after Task 9 (does not depend on Task 11)
