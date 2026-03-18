# Teardown MP Patcher — Developer Toolkit Design Spec

## Problem

The project has 47 patched mods with 32 documented bugs/rules accumulated over multiple sessions. Current pain points:

1. **Bug recurrence**: `validate.py` checks structural v2 compliance but misses ALL 32 real-world bugs (ipairs on iterators, raw keys with player params, missing ammo display, etc.)
2. **Context loss**: Each new conversation reads 8+ memory files and still misses nuance. No single-command way to get project state.
3. **Manual repetition**: Checking logs, running validation, deploying — all manual steps that should be one command.
4. **No batch fixing**: When a new rule is discovered (e.g., "all mods need `SetToolAmmoPickupAmount`"), applying it to 47 mods requires manual editing each one.

## Solution

Seven new components that encode institutional knowledge as executable tools:

### 1. `tools/lint.py` — Bug Scanner

Scans Lua files in `C:/Users/trust/Documents/Teardown/mods/` for all known bugs.

**Tier 1 — Hard errors (crash or silently break):**

| Check ID | Pattern | Regex/Logic |
|---|---|---|
| `IPAIRS-ITERATOR` | `ipairs(Players())` etc. | `ipairs\s*\(\s*(Players|PlayersAdded|PlayersRemoved)\s*\(` |
| `RAW-KEY-PLAYER` | `InputPressed("rmb", p)` — raw key with player param | Detect Input* calls where first arg is a raw key name AND second arg exists |
| `TOOL-ENABLED-ORDER` | `SetToolEnabled(p, "id", true)` | First arg is not a string literal |
| `ALTTOOL` | `"alttool"` anywhere | Literal string match |
| `GOTO-LABEL` | `goto` or `::label::` | `\bgoto\b` or `::[\w]+::` |
| `MOUSEDX` | `mousedx`/`mousedy` | Literal string match |
| `SET-PLAYER-TRANSFORM-CLIENT` | `SetPlayerTransform` in client.* function | Context-aware check using depth tracking from validate.py |
| `DRAW-NOT-CLIENT` | `function draw()` at top level | `^\s*function\s+draw\s*\(` without `client.` prefix |

**Tier 2 — Missing features (work but incomplete):**

| Check ID | Pattern | Logic |
|---|---|---|
| `MISSING-AMMO-DISPLAY` | Has RegisterTool but no `SetString("game.tool.X.ammo.display", "")` | Extract tool ID from RegisterTool, search for matching SetString |
| `MISSING-TOOL-AMMO` | Has RegisterTool but no `SetToolAmmo` in PlayersAdded block | Check for SetToolAmmo call with the registered tool ID |
| `MISSING-AMMO-PICKUP` | No `SetToolAmmoPickupAmount` | Absence check |
| `MISSING-OPTIONS-GUARD` | Has optionsOpen but usetool not gated | Search for InputPressed/InputDown("usetool") without `not data.optionsOpen` nearby |
| `MISSING-OPTIONS-SYNC` | Has optionsOpen but no `server.setOptionsOpen` | Absence check when optionsOpen exists |
| `HANDLE-GT-ZERO` | `handle > 0` | Regex from existing validate.py |
| `MANUAL-AIM` | Uses QueryRaycast but not GetPlayerAimInfo | Presence of QueryRaycast + absence of GetPlayerAimInfo |
| `MAKEHOLE-DAMAGE` | Uses MakeHole for damage (gun mods) | Presence of MakeHole (info-only, many mods legitimately use it) |
| `MISSING-KEYBIND-HINTS` | Has custom InputPressed on raw keys but no UiText hint | Heuristic: counts raw key inputs vs UI hint text |

**CLI:**
- `python -m tools.lint` — scan all mods in Documents/Teardown/mods/
- `python -m tools.lint --mod "Bee Gun"` — single mod
- `python -m tools.lint --tier 1` — hard errors only
- `python -m tools.lint --json` — machine-readable output
- Exit code: 1 if any tier-1 failures, 0 otherwise

**Output format:**
```
[FAIL] AK-47/main.lua:142  MISSING-AMMO-PICKUP  No SetToolAmmoPickupAmount found
[WARN] AK-47/main.lua:89   MANUAL-AIM           Uses QueryRaycast instead of GetPlayerAimInfo
[PASS] Bee_Gun — all checks passed
```

### 2. `tools/fix.py` — Batch Auto-Fixer

Deterministic fixes that are safe to apply without human judgment:

| Fix ID | Transform |
|---|---|
| `ipairs-iterator` | `for _, p in ipairs(Players()) do` → `for p in Players() do` (and Added/Removed) |
| `mousedx` | `InputValue("mousedx")` → `InputValue("camerax") * 180 / math.pi` |
| `alttool` | `"alttool"` → `"rmb"` |
| `draw-func` | `function draw(` → `function client.draw(` (top-level only) |
| `handle-gt` | `> 0 then` → `~= 0 then` for handle patterns |
| `ammo-display` | Insert `SetString("game.tool.X.ammo.display", "")` after RegisterTool if missing |

**NOT auto-fixed** (require judgment): optionsOpen guards, server/client splits, ServerCall wiring, keybind remapping, Shoot() conversion, GetPlayerAimInfo conversion.

**CLI:**
- `python -m tools.fix --dry-run` — preview all changes
- `python -m tools.fix` — apply to all mods
- `python -m tools.fix --mod "AK-47" --only ipairs-iterator,mousedx`
- Creates backup of each file before modifying (`.bak` suffix, overwritten on next run)

### 3. `tools/audit.py` — Mod Feature Matrix

Scans all mods and generates a feature/compliance matrix.

**Detected features:**
- `has_shoot`: Uses `Shoot()` API
- `has_aim_info`: Uses `GetPlayerAimInfo()`
- `has_ammo_pickup`: Has `SetToolAmmoPickupAmount`
- `has_options_menu`: Has `optionsOpen` / `UiMakeInteractive`
- `has_options_guard`: Options menu gates usetool input
- `has_keybind_hints`: Has UiText with key name hints
- `has_keybind_remap`: Has savegame.mod.keys reads
- `has_ammo_display_hidden`: Has `SetString("game.tool.*.ammo.display", "")`
- `is_gun_mod`: Heuristic — has Shoot/MakeHole/bullet patterns

**Output:** Markdown table to stdout, optionally writes `docs/AUDIT_REPORT.md`.

**CLI:** `python -m tools.audit` or `python -m tools.audit --output docs/AUDIT_REPORT.md`

### 4. `tools/logparse.py` — Teardown Log Parser

Reads `C:/Users/trust/AppData/Local/Teardown/log.txt`.

**Extracts:**
- Session timestamp (from log header)
- All ERROR lines, grouped by mod path
- Compile errors vs runtime errors (different format)
- Mod name extracted from path

**CLI:**
- `python -m tools.logparse` — all errors from latest session
- `python -m tools.logparse --mod "Hook Shotgun"` — filter to one mod
- `python -m tools.logparse --raw` — show full error lines

**Output:**
```
Session: 2026-03-17 14:32:05
────────────────────────────
Hook_Shotgun/main.lua
  line 142: runtime — attempt to call nil value 'GetPlayerAimInfo'
  line 89:  runtime — SetPlayerTransform is not available in client script

Bee_Gun/main.lua
  line 45:  compile — unexpected symbol near 'goto'

2 mods with errors, 3 total errors
```

### 5. `tools/status.py` — Session Boot Script

Single command that gives a new conversation full situational awareness.

**Collects:**
- Mod count: patched vs total (from `Documents/Teardown/mods/` and `MASTER_MOD_LIST.md`)
- Last git commit (hash + message)
- Lint summary: count of tier-1 failures, top 5 listed
- Log errors: count + top 3 listed
- Missing features summary: how many mods missing Shoot, AimInfo, AmmoPickup

**CLI:** `python -m tools.status`

**Output:**
```
TEARDOWN MP PATCHER — Status
═══════════════════════════════════════
Mods installed:   47
Last commit:      46abade — fix: proper rewrites for Magic Bag...
Game log:         2026-03-17 14:32 — 0 errors

Lint (Tier 1):    0 hard errors across 47 mods ✓
Lint (Tier 2):    3 warnings
  - 36 mods missing Shoot() (MANUAL-AIM)
  - 47 mods missing SetToolAmmoPickupAmount (MISSING-AMMO-PICKUP)
  - 12 mods missing keybind hints (MISSING-KEYBIND-HINTS)
```

### 6. Enhanced `CLAUDE.md`

Add to existing CLAUDE.md:

**Session Boot Procedure** section:
```
## First Thing Every Session
1. Run: python -m tools.status
2. If user mentions testing: python -m tools.logparse
3. Only read ISSUES_AND_FIXES.md when hitting a NEW bug
```

**Tool Usage** section documenting all new CLI commands.

**Subagent Dispatch Template** section with the 3 mandatory bug warnings.

### 7. `QUICKSTART.md`

Under 100 lines. Single file for new conversations containing:
- Project summary (3 lines)
- Key paths table
- "Run `python -m tools.status` first"
- Top 10 rules (condensed from the 19 in CLAUDE.md)
- Links to detailed docs

## File Structure

```
tools/
├── lint.py          # NEW — bug scanner
├── fix.py           # NEW — batch auto-fixer
├── audit.py         # NEW — feature matrix generator
├── logparse.py      # NEW — Teardown log parser
├── status.py        # NEW — session boot script
├── validate.py      # EXISTING — structural v2 checks (unchanged)
├── patch.py         # EXISTING — CLI entry point (add new commands)
└── ...

tests/
├── test_lint.py     # NEW
├── test_fix.py      # NEW
├── test_audit.py    # NEW
├── test_logparse.py # NEW
├── test_status.py   # NEW
└── ...

CLAUDE.md            # MODIFY — add session boot + tool usage sections
QUICKSTART.md        # NEW
docs/
└── AUDIT_REPORT.md  # GENERATED by audit.py
```

## Design Decisions

1. **Separate lint.py from validate.py**: validate.py does structural v2 compliance. lint.py does project-specific bug detection. Different concerns, different audiences. validate.py runs during the pipeline; lint.py runs during development.

2. **Fix only deterministic patterns**: Auto-fixing is limited to string-level transforms that are always correct. No context-dependent fixes — those stay as lint warnings.

3. **All tools read from Documents/Teardown/mods/**: This is where the game reads mods. Never the patches repo.

4. **Click CLI integration**: All tools use Click and integrate into the existing `td-patch` CLI group, but also work standalone via `python -m tools.X`.

5. **No external dependencies**: All new tools use only stdlib + Click (already a dependency). No tree-sitter needed for regex-based pattern matching.
