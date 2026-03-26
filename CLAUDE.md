# Teardown MP Mod Patcher

## MANDATORY — Do This First Every Session

**Before doing ANYTHING else:**
1. Run `python -m tools.status` — get mod count, last commit, game log errors, lint failures, missing features.
2. Read `docs/BASE_GAME_MP_PATTERNS.md` — **THE gold standard.** How official Teardown tools sync in MP. Every mod change must follow these patterns.
3. Read `docs/WHAT_WORKS.md` — proven fixes and patterns (DO use these).
4. Read `docs/WHAT_DOESNT_WORK.md` — failed approaches (DON'T repeat these).

All four steps are mandatory. Do NOT skip any.

## TOP PRIORITY: Match Base Game MP Patterns

**Every mod edit MUST follow the patterns in `docs/BASE_GAME_MP_PATTERNS.md`:**

1. **Server owns all game logic.** Input, physics, damage, spawning = server only. Client = visuals and animation only.
2. **No per-tick RPC.** Use registry broadcast (`SetInt/SetFloat/SetBool(key, value, true)`) or `shared.*` tables for continuous state. ServerCall/ClientCall are for discrete one-time events only.
3. **`PlaySound()` on server auto-syncs.** Do NOT use ClientCall to play sounds — just call PlaySound on the server.
4. **ToolAnimator for ALL players.** Call `tickToolAnimator(anim, dt, nil, p)` in a `for p in Players()` loop, not just for the local player.
5. **Event-driven death handling.** Use `GetEventCount("playerdied")`/`GetEvent()`, not per-tick health polling.
6. **`ClientCall(0, ...)` for world events.** `ClientCall(p, ...)` only for personal feedback (camera shake, HUD).
7. **`shared.*` for client-readable state.** Server writes, client reads. Zero RPC cost.
8. **NEVER modify the same `data.*` field in both server and client.** On the host, both contexts share the SAME player data object. Timers decremented in both = 2x speed on host (desync). Split into server-owned fields and client-only fields. Lint rule `DOUBLE-PROCESS-TIMER` catches this.

**ZERO TOLERANCE: No single-player code patterns.** Every line of mod code must work in multiplayer.

## Rules to Prevent Repeated Mistakes

### No Mass Changes
**NEVER apply changes to more than 3 mods at once.** Changing 30+ mods simultaneously makes bugs impossible to isolate.

### Verify Before Claiming Done
**After writing or editing any mod code (BOTH commands, EVERY time):**
```
python -m tools.lint --mod "ModName"
python -m tools.test --mod "ModName" --static
```

**After user tests a mod:**
```
python -m tools.logparse
```

**For full runtime testing (launches Teardown):**
```
python -m tools.test --mod "ModName"
```

## Developer Tools

### Session Start
| Command | When to use |
|---------|-------------|
| `python -m tools.status` | **EVERY session start** — mod count, lint summary, workshop sync check |
| `python -m tools.session` | **EVERY session start** — git changes, recently modified mods |
| `python -m tools.mp_ready` | Before MP testing — which mods are go/no-go |

### Before Editing a Mod
| Command | When to use |
|---------|-------------|
| `python -m tools.health --mod "X"` | **Before starting work** — combined lint + classify + diff |
| `python -m tools.diff --mod "X"` | See what changed vs workshop original |
| `python -m tools.revert --mod "X" --dry-run` | Preview reverting to workshop |

### After Editing a Mod
| Command | When to use |
|---------|-------------|
| `python -m tools.lint --mod "X"` | **MANDATORY** — 45 lint rules including desync detectors |
| `python -m tools.test --mod "X" --static` | **MANDATORY** — deep semantic analysis |

### When Something Breaks
| Command | When to use |
|---------|-------------|
| `python -m tools.revert --mod "X"` | **Instantly restore** workshop original |
| `python -m tools.logparse` | Parse game log for errors by mod |
| `python -m tools.diff --mod "X"` | Isolate which edit broke it |

### Batch Operations
| Command | When to use |
|---------|-------------|
| `python -m tools.lint` | Scan ALL mods |
| `python -m tools.fix --dry-run` | Preview safe auto-fixes |
| `python -m tools.fix` | Apply deterministic auto-fixes |
| `python -m tools.audit` | Feature matrix |
| `python -m tools.sync` | Show new/removed vs workshop |
| `python -m tools.pack` | Build zip of patched mods for friends |

### Hooks (automatic)
| Hook | Trigger | What it does |
|------|---------|-------------|
| `post_write_fix_lua` | After .lua write | Auto-converts CRLF to LF, strips non-ASCII |
| `post_edit_lint` | After .lua edit | Auto-runs lint on edited mod |
| `pre_edit_guard` | Before any edit | Blocks edits to wrong dir, asset files, or while game running |

**Lint suppression annotations:**
- `-- @lint-ok RULE-NAME` — suppress on current line
- `-- @lint-ok-file RULE-NAME` — suppress for entire file
- `-- @audit-ok` / `-- @deepcheck-ok CATEGORY` — suppress audit/deepcheck false positives

**Tests:** `python -m pytest tests/ -q` — 601 tests covering all tools.

## Where Mods Live — 3 Directories

| Directory | Purpose | Edit? |
|-----------|---------|-------|
| `D:/The Vault/Modding/Games/Teardown/` | **Working directory. ALL edits here.** | **YES** |
| `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/` | Game install. Managed by Steam Workshop. | NEVER |
| `C:/Steam2/steamapps/common/Teardown/mods/` | Sandboxed install. Managed by Steam Workshop. | NEVER |
| `C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/` | Workshop cache. Read-only. | NEVER |
| `C:/Users/trust/teardown-mp-patches/mods/` | Patches repo source data. | NEVER |

**Workflow:** Edit in working dir → `update.bat` → restart both clients → test in MP.

## V2 Rewrite Rules (MANDATORY)

1. `#version 2` + `#include "script/include/player.lua"` header. **Without `#version 2`, scripts are SILENTLY DISABLED in MP.**
2. `players = {}` with per-player state via `createPlayerData()`
3. Server/client split callbacks:
   - **Server:** `server.init()`, `server.tick(dt)`, `server.update(dt)` (fixed 60Hz)
   - **Client:** `client.init()`, `client.tick(dt)`, `client.update(dt)`, `client.draw()`
4. `for p in PlayersAdded()` / `PlayersRemoved()` / `Players()` — NEVER use `ipairs()` on these
5. `RegisterTool()` with group number in `server.init()`
6. `SetToolEnabled("id", true, p)` + `SetToolAmmo("id", 101, p)` in PlayersAdded
7. Server handles: MakeHole, Explosion, Shoot, SetPlayerVelocity, SetPlayerTransform, ApplyPlayerDamage, PlaySound (auto-syncs)
8. Client handles: SpawnParticle, DrawLine, DrawSprite, PointLight, SetToolTransform, SetCameraTransform, ShakeCamera, all Ui*
9. NEVER use raw keys with player param: `InputPressed("rmb", p)` FAILS SILENTLY. Use `InputPressed("rmb")` + ServerCall
10. **ALWAYS use `Shoot()` for weapons.** Handles terrain, players, kill feed, bullet trace, MP sync. NEVER use old `QueryShot + ApplyPlayerDamage + MakeHole` chain.
11. `QueryShot()` returns `player=0` for non-player hits — guard with `player ~= 0`, NOT `if player then` (Lua 0 is truthy)
12. Entity scripts MUST independently have `#version 2` + v2 callbacks. V1 entity scripts are **silently disabled** in MP.
13. `options.lua` needs independent `#version 2` + v2 callbacks. Leave special Teardown options callbacks intact.
14. All asset paths MUST use `MOD/` prefix in v2: `LoadSound("MOD/snd/fire.ogg")`
15. Every `#version 2` script MUST define at least one callback.
16. `info.txt` MUST have `version = 2` for MP compatibility.
17. **NEVER use `local` at file scope** in v2 scripts — preprocessor splits chunks, file-scope locals become invisible across server/client.
18. **`mousedx`/`mousedy` ARE valid** for mods using `SetCameraTransform()`. `camerax`/`cameray` return 0 when camera is script-controlled.
19. `SetPlayerHealth(health, player)` — health FIRST, player SECOND. Reverse silently affects wrong player.
20. `ServerCall("server.fn", p, ...)` — player ID `p` REQUIRED as first param. Engine does NOT auto-inject it.
21. `Explosion()` does NOT damage players — must add explicit `ApplyPlayerDamage()` with distance falloff.
22. ASCII only in .lua files. No em dashes, degree symbols, or UTF-8 multibyte — preprocessor silently fails.
23. LF-only line endings. CRLF causes compile errors with the preprocessor.
24. Entity handles: check `~= 0` not `> 0` (v2 client handles can be negative).
25. **Shared `players[p]` double-processing on host.** Both server.tick and client.tick share the SAME data object on host. Use separate fields or gate client writes with `IsPlayerLocal(p)`.
26. `PlayersAdded()`/`PlayersRemoved()`/`Players()` require `#include "script/include/player.lua"`. Without it, use `GetAddedPlayers()`/`GetRemovedPlayers()`/`GetAllPlayers()` (engine built-ins, return tables not iterators).
27. Camera sensitivity for custom cameras: `GetInt("options.input.sensitivity") / 1000 * (zoomlevel / defaultZoom)`.

## Known Subagent Bugs

When dispatching subagents for ANY Teardown mod work, ALWAYS include:
1. `Players()`/`PlayersAdded()`/`PlayersRemoved()` are ITERATORS — NO `ipairs()`
2. Raw keys (`"rmb"`, `"r"`) do NOT take player param — use `InputPressed("rmb")` + ServerCall
3. `SetToolEnabled("toolid", true, p)` — string first, bool second, player third
4. `player ~= 0` guard after QueryShot — NOT `if player then`
5. `ServerCall("server.fn", p, ...)` — pass player ID explicitly
6. **#1 DESYNC BUG:** Do NOT modify same `data.*` field in both server/client tickPlayer — host gets 2x processing
7. ALWAYS run `python -m tools.lint --mod "ModName"` after writing any code
8. `PlaySound()` on server auto-syncs — no ClientCall wrapper
9. `tickToolAnimator()` for ALL players in `for p in Players()` loop
10. Registry broadcast for continuous state, NOT per-tick RPC
11. `ClientCall(0, ...)` for world events, `ClientCall(p, ...)` for personal feedback
12. Clean up per-player state in `PlayersRemoved()`
13. **ALWAYS use `Shoot()` for weapons** — never QueryShot+ApplyPlayerDamage+MakeHole
14. **NEVER use `local` at file scope** in v2 scripts
15. **`mousedx`/`mousedy` valid** for SetCameraTransform mods
16. **Surgical fixes over rewrites.** Never rewrite working architecture.
17. **NEVER define `function server.*()` / `function client.*()` inside another function.** Preprocessor extracts them regardless of nesting — closures break silently. (Issue #80)
18. **PlayersAdded/PlayersRemoved/Players iterators consumed after one pass.** Call once per tick, collect into table if multiple systems need results. (Issue #81)
19. **SpawnParticle/PointLight/DrawLine/SetShapeEmissiveScale are CLIENT-ONLY.** Never call on server. PlaySound on server IS ok (auto-syncs). (Issue #83)
20. **Server-owned timers need explicit sync for client visuals.** Separate state tables prevent double-processing but also prevent sharing. Use `SyncToClient`/registry broadcast. (Issue #84)
21. **LoadLoop() is client-only.** Load in ClientInit hook, never at file scope. LoadSound works everywhere. (Issue #85)
22. **Projectile distance = travel from origin, not absolute world position.** (Issue #86)
23. **Remove table entries with nil, not flag fields.** `pairs()` skips nil but iterates `active=false`. (Issue #87)
24. **Do not use unverified APIs.** If vanilla mods don't use a function, verify it exists before calling. (Issue #88)
25. **For new tool mods or v1 conversions, use DEF.** `#include "lib/def.lua"` + `DEF.Tool()` handles all boilerplate and prevents issues #80-88 by design.

## Important Rules

- **NEVER modify built-in mods.** 40 mods without `id.txt` are Steam depot files. Modifying them causes MP file mismatch disconnects. Steam verify will undo all changes. Only modify the 49 custom workshop mods (those with `id.txt`).
- **Do NOT copy preview images** into mod folders — crashes engine (buffer overflow).
- **Do NOT modify asset files** (.vox, .xml prefab, .png, .ogg) — only edit .lua and info.txt.
- **Active mod ceiling:** Warn at ~150 mods. Engine crashes at ~178 (shadow volume overflow).
- **Clear `__pycache__`** before batch tests.
- **No mod edits while game is running** — check `tasklist | grep -i teardown` first.
- **First change = immediate test.** Make ONE small change, verify in-game, then proceed.
- **If a batch breaks the game, revert immediately** — `git checkout` changed files.
- **Tools passing ≠ game works.** Only in-game testing is final.
- **Every installed mod must have `id.txt`** with Steam Workshop ID.
- **File integrity check:** All players need byte-identical mod files for MP.
- **No subagents for mod code.** Subagents must NEVER write mod files. They are read-only for research/investigation. Re-read CLAUDE.md before every code write.
- **Batch workflow:** Max 2-3 mods per batch. Test between batches. Commit after each for rollback. Never change 30+ mods at once — isolating crashes becomes impossible.
- **Sync installs after patching:** Run `sync_installs.py --mod "X"` to copy to Steam2 before local MP testing (see `docs/TESTING_SETUP.md`).

## Realistic Ballistics Framework

Every weapon mod MUST use `lib/realistic_ballistics.lua`. One `#include`, one profile, one fire call.

```lua
#include "lib/ballistics.lua"
local myGun = CreateBallisticsProfile({
    damage = 20, pellets = 1, spread = 0.02,
    range = 100, toolId = "my-rifle",
    holeScale = 1.0, penScale = 0.5,
    fullRange = 15, halfRange = 60, minFalloff = 0.2,
})
-- In server.tickPlayer: myGun:FireFromTool(toolBody, muzzleOffset, player)
```

| Property | Controls | Example |
|----------|----------|---------|
| `damage` | Base damage per projectile (÷100) | 28 (shotgun), 50 (rifle) |
| `pellets` | Projectiles per shot | 1 (rifle), 8 (shotgun) |
| `spread` | Cone angle (0 = laser) | 0 (sniper), 0.07 (shotgun) |
| `fullRange` / `halfRange` | Damage falloff distances | 15/60 (rifle), 3/25 (shotgun) |

## Desync Exterminator Framework (DEF)

**For ALL new tool mods and v1→v2 conversions, use DEF.** One `#include`, one `DEF.Tool()` call, zero desync.

```lua
#version 2
#include "script/include/player.lua"
#include "lib/def.lua"

tool = DEF.Tool("my-gun", { displayName = "My Gun", prefab = "MOD/vox/gun.vox", group = 6, ammo = 30 })
snd = tool:LoadSound("MOD/snd/fire.ogg")
tool:PlayerData(function() return { cooldown = 0, magazine = 30 } end)
tool:ServerTick(function(p, data, dt)
    tool:TickTimer(data, "cooldown", dt)
    if tool:InputPressed("usetool", p) and data.cooldown <= 0 then
        local aim = tool:GetAim(p)
        tool:Fire(aim.pos, aim.dir, { damage = 20, range = 100 }, p)
        tool:PlaySound(snd, aim.pos)
        data.magazine = data.magazine - 1
        data.cooldown = 0.15
        tool:SyncToClient("magazine", data.magazine, p)
    end
end)
tool:Draw(function(p, data) UiText("Ammo: " .. tool:ReadSync("magazine", p, 30)) end)
```

DEF auto-handles: tool registration, PlayersAdded/Removed loops, per-player state, ToolAnimator for all players, sound loading in both contexts, separate server/client state tables (no double-processing), safe input routing, and client.draw gating.

**Files:** `lib/def.lua` (framework), `lib/def_example.lua` (full before/after example)

## Reference Docs

| Doc | When to read |
|-----|-------------|
| **`docs/BASE_GAME_MP_PATTERNS.md`** | **Every session** |
| **`docs/WHAT_WORKS.md`** | **Before any fix** |
| **`docs/WHAT_DOESNT_WORK.md`** | **Before any fix** |
| `lib/def.lua` | **Any new tool mod or v1→v2 conversion** |
| `lib/def_example.lua` | Full before/after conversion example |
| `docs/MP_REFERENCE.md` | Fixing MP issues |
| `docs/MPLIB_INTERNALS.md` | AmmoPickup / loot |
| `docs/UMF_TRANSLATION_GUIDE.md` | Converting UMF mods |
| `docs/UI_STANDARDS.md` | Editing HUD code |
| `ISSUES_AND_FIXES.md` | Debugging (73 issues) |
| `MASTER_MOD_LIST.md` | After converting mods |
| `docs/TESTING_SETUP.md` | Dual Steam / Sandboxie local MP testing |
| `docs/ECOSYSTEM.md` | All Teardown tools, scripts, and locations across the system |
| `docs/KNOWN_LIMITATIONS.md` | Engine limits, preprocessor quirks, tool gaps, v1→v2 API map, pending work |
| `docs/LINT_RULES.md` | All 45 lint rules + 6 deepcheck validators + API database reference |
| `docs/KEYBIND_STANDARDS.md` | Standardized keybind assignments — reserved keys, mod key map |
| `docs/MP_TESTING_GUIDE.md` | Structured MP testing workflow, priority order, per-mod procedures |
| `README.md` | Project overview, batch history, deferred mods list |
| `QUICKSTART.md` | Full developer onboarding, workflow order, top 10 rules |
