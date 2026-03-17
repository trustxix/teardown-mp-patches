# Teardown MP Mod Patcher

## Project Overview
Automated pipeline to patch Teardown Workshop mods for v2 multiplayer compatibility. 46 mods patched so far, ~130 remaining.

## Critical Files
- `docs/RESEARCH.md` — 34 findings from official API/code analysis. READ BEFORE ANY MOD WORK.
- `docs/ISSUES_AND_FIXES.md` — 32 resolved issues with rules. READ BEFORE ANY MOD WORK.
- `docs/MASTER_MOD_LIST.md` — current patched mod list (46 mods)
- `C:/Users/trust/Documents/Teardown/TEARDOWN_V2_API_REFERENCE.md` — full v2 API (1117 lines, 550+ functions)

## Where Mods Live
- **Game reads from:** `C:/Users/trust/Documents/Teardown/mods/` — ALL edits go here
- **Workshop originals:** `C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/`
- **Patches repo:** `C:/Users/trust/teardown-mp-patches/mods/` — template copies, NOT used by game

## V2 Rewrite Rules (MANDATORY)
1. `#version 2` + `#include "script/include/player.lua"` header
2. `players = {}` with per-player state via `createPlayerData()`
3. Server/client split: `server.init()`, `server.tick(dt)`, `client.init()`, `client.tick(dt)`, `client.draw()`
4. `for p in PlayersAdded()` / `PlayersRemoved()` / `Players()` — NEVER use `ipairs()` on these
5. `RegisterTool()` with group number in `server.init()`
6. `SetToolEnabled("id", true, p)` + `SetToolAmmo("id", 101, p)` in PlayersAdded
7. `SetString("game.tool.id.ammo.display", "")` to hide engine ammo
8. Server handles: MakeHole, Explosion, SetBodyVelocity, ApplyBodyImpulse, Spawn, Delete, SpawnFire, Shoot, SetPlayerVelocity, SetPlayerTransform, ApplyPlayerDamage
9. Client handles: PlaySound, SpawnParticle, DrawLine, DrawSprite, PointLight, SetToolTransform, SetCameraTransform, all Ui* functions
10. NEVER use raw keys with player param: `InputPressed("rmb", p)` FAILS SILENTLY. Use `InputPressed("rmb")` with `isLocal` check + ServerCall
11. Use `GetPlayerAimInfo(muzzlePos, maxDist, p)` for aim — NOT manual `GetPlayerEyeTransform` + `QueryRaycast`
12. Use `Shoot(pos, dir, "bullet", damage, range, p, "toolId")` for guns — NOT `MakeHole` (MakeHole can't damage players)
13. Use `QueryShot()` + `ApplyPlayerDamage()` for beam/melee weapons
14. Add `SetToolAmmoPickupAmount("id", amount)` for ammo crate integration
15. Entity handles: check `~= 0` not `> 0` (v2 client handles can be negative)
16. No goto/labels (Lua 5.1), no mousedx/mousedy (use camerax/cameray)
17. Gate all `usetool` input with `not data.optionsOpen`
18. Always send aim coordinates WITH ServerCall (never compute aim on server from client action)
19. `client.draw()` not `draw()` for HUD

## Known Subagent Bugs (agents ALWAYS make these — check every time)
1. `ipairs()` on `Players()`/`PlayersAdded()`/`PlayersRemoved()` — these are iterators, not tables
2. `"alttool"` instead of `"rmb"` for right mouse button
3. Wrong `SetToolEnabled` arg order: correct is `SetToolEnabled("id", true, p)` not `SetToolEnabled("id", p, true)`

## Team Roles (for multi-terminal setup)

### API Surgeon (Terminal 1)
- Upgrades existing 46 mods with Shoot/QueryShot/GetPlayerAimInfo/SetToolAmmoPickupAmount
- Works ONLY on existing mods in `Documents/Teardown/mods/`
- Never creates new mods, never edits docs

### Mod Converter (Terminal 2)
- Converts new v1 mods from Workshop to v2 multiplayer
- Creates NEW mod folders in `Documents/Teardown/mods/`
- Never touches mods that Terminal 1 is upgrading

### QA & Integration (Terminal 3 / Lead)
- Reviews output from other terminals
- Runs safety checks, updates docs
- Handles bug reports from user testing
- Applies polish (options menus, keybind remapping)
- Owns all files in `docs/`

## Developer Tools

### First Thing Every Session
1. Run: `python -m tools.status` — full project status report
2. If user mentions testing: `python -m tools.logparse` — parse game log for errors
3. Only read ISSUES_AND_FIXES.md when hitting a NEW bug

### Available Commands
| Command | Purpose |
|---------|---------|
| `python -m tools.status` | Full project status report |
| `python -m tools.lint` | Scan all mods for known bugs |
| `python -m tools.lint --mod "X"` | Scan single mod |
| `python -m tools.lint --tier 1` | Hard errors only |
| `python -m tools.fix --dry-run` | Preview auto-fixes |
| `python -m tools.fix` | Apply all safe auto-fixes |
| `python -m tools.fix --mod "X" --only ipairs-iterator` | Targeted fix |
| `python -m tools.audit` | Generate mod feature matrix |
| `python -m tools.audit --output docs/AUDIT_REPORT.md` | Save audit report |
| `python -m tools.logparse` | Parse Teardown log for errors |
| `python -m tools.logparse --mod "X"` | Filter to one mod |

### After User Tests a Mod
1. Run `python -m tools.logparse` IMMEDIATELY
2. If errors found, read the specific lines referenced
3. Fix and have user re-test

### After Writing Any Mod Code
Run `python -m tools.lint --mod "ModName"` to catch known bugs before testing.

### Subagent Dispatch Template
When dispatching subagents for ANY Teardown mod work, ALWAYS include these 3 warnings:
1. `Players()`/`PlayersAdded()`/`PlayersRemoved()` are ITERATORS — NO `ipairs()`
2. Raw keys (`"rmb"`, `"r"`, etc.) do NOT take player param — use `InputPressed("rmb")` + ServerCall
3. `SetToolEnabled("toolid", true, p)` — string first, bool second, player third
