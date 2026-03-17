# Teardown MP Mod Patcher

## MANDATORY — Do This First Every Session

**Before doing ANYTHING else, run:**
```
cd C:/Users/trust/teardown-mp-patches && python -m tools.status
```
This tells you: mod count, last commit, game log errors, lint failures, and missing features.
Do NOT skip this. Do NOT start working without it. The output replaces reading multiple doc files.

**After user tests a mod:**
```
python -m tools.logparse
```

**After writing or editing any mod code:**
```
python -m tools.lint --mod "ModName"
```

## Developer Tools — Use These, Not Manual Work

| Command | When to use |
|---------|-------------|
| `python -m tools.status` | **EVERY session start** |
| `python -m tools.lint` | Scan all mods for 17 known bugs |
| `python -m tools.lint --mod "X"` | After editing a specific mod |
| `python -m tools.lint --tier 1` | Hard errors only (crashes/silent failures) |
| `python -m tools.fix --dry-run` | Preview safe auto-fixes across all mods |
| `python -m tools.fix` | Apply all 6 deterministic auto-fixes |
| `python -m tools.fix --mod "X" --only ipairs-iterator` | Targeted fix |
| `python -m tools.audit` | Feature matrix — what each mod has/needs |
| `python -m tools.audit --output docs/AUDIT_REPORT.md` | Save audit to file |
| `python -m tools.logparse` | Parse Teardown log.txt for errors by mod |
| `python -m tools.logparse --mod "X"` | Filter errors to one mod |

**Tests:** `python -m pytest tests/ -q` — 181 tests covering all tools.

## Where Mods Live

- **ALL edits go here:** `C:/Users/trust/Documents/Teardown/mods/` — game reads from this
- **NEVER edit:** `C:/Users/trust/teardown-mp-patches/mods/` — patches repo, game ignores it
- **Workshop originals:** `C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/`
- **Backup:** `C:/Users/trust/Documents/Teardown/mods_BACKUP/`

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

## Known Subagent Bugs (agents ALWAYS make these)

When dispatching subagents for ANY Teardown mod work, ALWAYS include:
1. `Players()`/`PlayersAdded()`/`PlayersRemoved()` are ITERATORS — NO `ipairs()`
2. Raw keys (`"rmb"`, `"r"`, etc.) do NOT take player param — use `InputPressed("rmb")` + ServerCall
3. `SetToolEnabled("toolid", true, p)` — string first, bool second, player third
4. ALWAYS run `python -m tools.lint --mod "ModName"` after writing any mod code

## Do NOT Use Agents to Write Mod Code

Agents can research, analyze, update docs, run tools. But mod rewrites must be done manually.

## Reference Docs (read only when needed)

- `docs/RESEARCH.md` — 34 API findings from official sources
- `ISSUES_AND_FIXES.md` — 32 resolved bugs with rules
- `docs/V2_SYNC_PATTERNS.md` — network sync patterns
- `docs/AUDIT_REPORT.md` — generated feature matrix
- `QUICKSTART.md` — condensed quick reference
- `C:/Users/trust/Documents/Teardown/TEARDOWN_V2_API_REFERENCE.md` — full v2 API
