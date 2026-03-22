# Teardown MP Mod Patcher

## MANDATORY — Do This First Every Session

**Before doing ANYTHING else:**
1. Run `python -m tools.status` — get mod count, last commit, game log errors, lint failures, missing features.
2. Read `docs/BASE_GAME_MP_PATTERNS.md` — **THE gold standard.** How official Teardown tools sync in MP. Every mod change must follow these patterns.
3. Read `docs/WHAT_WORKS.md` — proven fixes and patterns (DO use these).
4. Read `docs/WHAT_DOESNT_WORK.md` — failed approaches (DON'T repeat these).

All four steps are mandatory. Do NOT skip any. Do NOT start working without completing all four. BASE_GAME_MP_PATTERNS is the #1 priority reference — our mods must match the official sync patterns.

**Then check your inbox and task queue (via MCP):**
```
Use MCP tools: check_inbox(your_role) → process messages → get_task(your_role) → do work
```

## TOP PRIORITY: Match Base Game MP Patterns

**Every mod edit MUST follow the patterns in `docs/BASE_GAME_MP_PATTERNS.md`.** These are the rules the official Teardown code follows. Our mods must match them:

1. **Server owns all game logic.** Input, physics, damage, spawning = server only. Client = visuals and animation only.
2. **No per-tick RPC.** Use registry broadcast (`SetInt/SetFloat/SetBool(key, value, true)`) or `shared.*` tables for continuous state. ServerCall/ClientCall are for discrete one-time events only.
3. **`PlaySound()` on server auto-syncs.** Do NOT use ClientCall to play sounds — just call PlaySound on the server.
4. **ToolAnimator for ALL players.** Call `tickToolAnimator(anim, dt, nil, p)` in a `for p in Players()` loop, not just for the local player.
5. **Event-driven death handling.** Use `GetEventCount("playerdied")`/`GetEvent()`, not per-tick health polling.
6. **`ClientCall(0, ...)` for world events.** `ClientCall(p, ...)` only for personal feedback (camera shake, HUD).
7. **`shared.*` for client-readable state.** Server writes, client reads. Zero RPC cost.
8. **NEVER modify the same `data.*` field in both server and client.** On the host, both contexts share the SAME player data object. Timers decremented in both = 2x speed on host (desync). Split into server-owned fields (gameplay timers, ammo, cooldowns) and client-only fields (visual recoil, client tracers, HUD timers). Lint rule `DOUBLE-PROCESS-TIMER` catches this. (Issue #42/#72 — found in 12+ mods)

When reviewing or writing mod code, check it against these 8 rules FIRST. Any violation is a bug to fix.

**ZERO TOLERANCE: No single-player code patterns.** Every line of mod code must work in multiplayer. There is no "single-player mode" — even when only one player is in the game, the v2 server/client split is active. Code that works "in single-player" but desyncs in MP is broken code.

## Inter-Terminal Communication

You are one of 4 terminals that coordinate via MCP tools and a filesystem inbox system.

**Roles:** `qa_lead`, `api_surgeon`, `mod_converter`, `docs_keeper`

**MCP Tools for coordination:**
- `has_mail(role)` — quick check for new messages (call often, it's cheap)
- `get_focus()` — read current team focus area (all terminals work on this)
- `check_inbox(role)` — read new messages from other terminals
- `send_message(from, to, type, priority, content)` — send to another terminal
- `broadcast(from, type, priority, content)` — send to all terminals
- `clear_message(role, filename)` — delete processed inbox message
- `get_task(role)` — get next open task from queue
- `complete_task(id, summary)` — mark task done
- `create_task(title, role, priority, desc, mods)` — create new task

## Batch Pass System (MANDATORY)

The team works in **supervised batches**, never autonomously. All work follows this cycle:

### Pass Structure
A **pass** is a complete sweep through all mods with a specific goal (e.g., "fix compile errors", "add AmmoPickup", "general bug fixing"). The user defines the goal.

### Batch Rules
1. **QA Lead assigns a batch of 2-3 mods** to the team. All terminals work on the SAME batch simultaneously, each in their own area (api_surgeon: code fixes, mod_converter: structural changes, docs_keeper: documentation).
2. **One mod, one writer.** Only ONE terminal may edit a given mod's files. Others can READ it for context. No two terminals touch the same mod's code.
3. **Forward only.** Once a batch is complete and the user says "continue", the team moves to the next batch. NEVER go back to re-edit a previous batch's mods unless the user explicitly requests it.
4. **Stop after every batch.** When all terminals finish their batch work, QA Lead halts the team and reports to the user: what changed, which mods, lint/test results. Then WAIT for the user to say "continue" before the next batch.
5. **No initiative work.** Terminals do NOT self-assign work, run auto-fixes across all mods, or make "improvement" changes outside the current batch. If you see something that needs fixing in a mod outside the current batch, log it as a task for a future batch.
6. **Max 3 mods changed per batch.** Never touch more than 3 mod directories in a single batch. This keeps changes small and debuggable.
7. **User can test between batches.** The stop point lets the user launch the game and verify nothing broke before proceeding.

### Work Loop
1. `check_killswitch()` — if active, STOP.
2. `get_focus()` — read current pass goal and batch assignment
3. `check_inbox(your_role)` — process messages
4. `clear_message()` each processed message
5. `get_task(your_role)` — pick up task within the CURRENT BATCH ONLY
6. Do the work on assigned mods only
7. `has_mail(your_role)` — check every 5 tool calls
8. `complete_task()` when done
9. When batch is complete: QA Lead reports to user, team HALTS until user says "continue"

### Between Batches (QA Lead Only)
- Report: "Batch N complete. Changed: [mod list]. Lint: [result]. Test: [result]. Ready for you to test."
- Wait for user response before assigning next batch
- If user reports issues, fix ONLY those issues before moving forward

**KILLSWITCH:** If `check_killswitch()` returns `active: true`, finish current task cleanly, then HALT. Output "HALTED — waiting for instructions."

**Message protocol:** See `.comms/PROTOCOL.md` for format details.
**When to message:** See `.comms/TRIGGERS.md` for exactly when to write to other inboxes.

### When Queue Is Empty — Idle Protocol (MANDATORY)

**When you have no inbox messages, no tasks, and no batch assignment, follow this priority list IN ORDER. Do NOT skip ahead. Do NOT self-assign mod edits.**

1. **Report idle to user.** Output: "Queue empty. No tasks, no inbox. Standing by." Then WAIT. If the user doesn't respond within a reasonable time, proceed to step 2.
2. **Run diagnostics (READ-ONLY).** These produce reports without changing any files:
   - `python -m tools.lint` — check for new findings
   - `python -m tools.test --batch all --static` — deep analysis scan
   - `python -m tools.audit --output docs/AUDIT_REPORT.md` — feature matrix refresh
   - Check base game compliance: `grep -c "CLIENTCALL-SOUND\|MISSING-PLAYERS-REMOVED\|TOOLANIM-LOCAL-ONLY"` in lint output
3. **Create tasks from findings.** If diagnostics found issues, create tasks via `create_task()` describing the issue, affected mod, and fix approach. Do NOT start working on the tasks — just create them.
4. **Review docs for drift.** Read WHAT_WORKS, WHAT_DOESNT_WORK, and ISSUES_AND_FIXES. Check if any entries are outdated or contradicted by current code. If so, create a docs_keeper task.
5. **HALT.** After completing steps 1-4, output "Diagnostics complete. [N] new tasks created. Standing by for user." Then STOP. Do not loop.

**What you must NEVER do when idle:**
- Edit mod code without a task assignment
- Run auto-fixes without user approval
- "Improve" or refactor mods you weren't asked to touch
- Add features, keybind hints, or UI changes proactively
- Delete, rename, or reorganize files
- Make "cleanup" changes to tools, docs, or infrastructure

**Why:** Unsupervised changes during idle time have caused crashes, broken mods, and wasted hours of debugging. The batch system exists because every change needs user verification. If there's nothing to do, that means the project is in a good state — don't break it by inventing work.

## Rules to Prevent Repeated Mistakes

### No Mass Changes
**NEVER apply changes to more than 3 mods at once.** The crash investigation showed that changing 30+ mods simultaneously makes bugs impossible to isolate. Even "safe" changes (preview images, lint annotations, auto-fixes) must go through the batch system.

### No Reverting Other Terminals' Work
If you disagree with another terminal's change, send a message to QA Lead — do NOT revert it yourself. QA Lead decides.

### Commit After Every Batch
QA Lead calls `auto_commit()` after each completed batch with a descriptive message listing exactly which mods changed. This creates rollback points if something breaks.

### Verify Before Claiming Done
Before marking any task complete, run BOTH:
```
python -m tools.lint --mod "ModName"
python -m tools.test --mod "ModName" --static
```
If either fails, the task is NOT done.

**After user tests a mod:**
```
python -m tools.logparse
```

**After writing or editing any mod code (BOTH commands, EVERY time):**
```
python -m tools.lint --mod "ModName"
python -m tools.test --mod "ModName" --static
```
Lint catches pattern bugs. Test catches LOGIC bugs (broken chains, missing ServerCall targets, wrong-side effects, asset references to nonexistent files, ID mismatches). BOTH are required. A mod that passes lint can still FAIL the test.

**For full runtime testing (launches Teardown, captures screenshots, fires weapon):**
```
python -m tools.test --mod "ModName"
```
This requires `python -m tools.test --setup` to have been run first. It injects diagnostic counters, launches the game, simulates input, captures screenshots, and reads back runtime data from savegame.xml.

## Developer Tools — Use These, Not Manual Work

| Command | When to use |
|---------|-------------|
| `python -m tools.status` | **EVERY session start** (includes workshop sync check) |
| `python -m tools.sync` | Dry-run: show new/removed mods vs workshop |
| `python -m tools.sync --apply` | Actually sync: copy new mods, remove unsubscribed |
| `python -m tools.lint` | Scan all mods for 36 known bugs (includes info.txt validation) |
| `python -m tools.lint --mod "X"` | After editing a specific mod |
| `python -m tools.lint --tier 1` | Hard errors only (crashes/silent failures) |
| `python -m tools.fix --dry-run` | Preview safe auto-fixes across all mods |
| `python -m tools.fix` | Apply all 11 deterministic auto-fixes |
| `python -m tools.fix --mod "X" --only ipairs-iterator` | Targeted fix |
| `python -m tools.audit` | Feature matrix — what each mod has/needs |
| `python -m tools.audit --output docs/AUDIT_REPORT.md` | Save audit to file |
| `python -m tools.logparse` | Parse Teardown log.txt for errors by mod |
| `python -m tools.logparse --mod "X"` | Filter errors to one mod |
| `python -m tools.test --mod "X" --static` | **Deep semantic analysis** — traces firing/effect/HUD chains, validates assets, cross-refs IDs |
| `python -m tools.test --mod "X"` | Full autonomous test (static + game launch when configured) |
| `python -m tools.test --batch all --static` | Deep analysis on ALL mods |
| `python -m tools.test --setup` | First-time setup (find Teardown exe, install test harness) |
| `python tools/gun_v2_generator.py` | Generate complete v2 main.lua for standard gun mods (batch) |

**Lint suppression annotations** (add to mod Lua files when findings are false positives):
- `-- @lint-ok RULE-NAME` — suppress a specific finding on the current line
- `-- @lint-ok-file RULE-NAME` — suppress a rule for the entire file (place at top of file)
- `-- @audit-ok` — suppress audit false positives (e.g., tools using QueryShot instead of Shoot)
- `-- @deepcheck-ok CATEGORY` — suppress deep analysis false positives (e.g., `@deepcheck-ok ASSET` for upstream missing assets, `@deepcheck-ok ENTITY` for entity scripts, `@deepcheck-ok EFFECT` for mods with non-standard effect broadcasting). Place in first 5 lines for file-level, or on the specific line.

**Tests:** `python -m pytest tests/ -q` — 601 tests covering all tools.

## Where Mods Live — 3 Directories

Teardown loads mods from three locations. Local mods override workshop versions when the same mod exists in both.

| Directory | Purpose | Edit? |
|-----------|---------|-------|
| `C:/Users/trust/Documents/Teardown/mods/` | **Local/custom mods.** Patched MP mods go here. Takes priority over workshop versions. | **YES — all edits here** |
| `C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/` | **Workshop originals.** Steam downloads subscribed mods here (folders named by Workshop ID). Read-only, managed by Steam. | NEVER |
| `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/` | **Game install mods.** For mods bundled with the game itself. Currently empty — Teardown ships none here. | NEVER |
| `C:/Users/trust/teardown-mp-patches/mods/` | **Patches repo.** Our project's source data. Game does not read from here. | NEVER |
| `C:/Users/trust/Documents/Teardown/mods_BACKUP/` | **Backup.** Snapshots before major changes. | Restore only |

## V2 Rewrite Rules (MANDATORY)

1. `#version 2` + `#include "script/include/player.lua"` header. **Without `#version 2`, scripts are SILENTLY DISABLED in multiplayer.**
2. `players = {}` with per-player state via `createPlayerData()`
3. Server/client split — use the correct callbacks:
   - **Server (host only):** `server.init()`, `server.tick(dt)`, `server.update(dt)` (fixed 60Hz), `server.postUpdate()`, `server.destroy()`
   - **Client (each player + host):** `client.init()`, `client.tick(dt)`, `client.update(dt)` (fixed 60Hz), `client.postUpdate()`, `client.draw()`, `client.render(dt)`, `client.destroy()`
   - **Key difference:** `tick(dt)` is variable timestep (once per frame). `update(dt)` is fixed 60Hz (0-2 calls per frame). Use `update` for deterministic physics.
4. `for p in PlayersAdded()` / `PlayersRemoved()` / `Players()` — NEVER use `ipairs()` on these
5. `RegisterTool()` with group number in `server.init()`
6. `SetToolEnabled("id", true, p)` + `SetToolAmmo("id", 101, p)` in PlayersAdded
7. `SetString("game.tool.id.ammo.display", "")` to hide engine ammo
8. Server handles: MakeHole, Explosion, SetBodyVelocity, ApplyBodyImpulse, Spawn, Delete, SpawnFire, Shoot, SetPlayerVelocity, SetPlayerTransform, ApplyPlayerDamage, SetPlayerHealth, SetToolEnabled, SetToolAmmo, DisablePlayerInput, SetPlayerColor, SetPlayerWalkingSpeed, PlaySound (auto-syncs to all clients)
9. Client handles: SpawnParticle, DrawLine, DrawSprite, PointLight, SetToolTransform, SetCameraTransform, ShakeCamera, SetCameraDof, DrawBodyOutline, all Ui* functions
10. NEVER use raw keys with player param: `InputPressed("rmb", p)` FAILS SILENTLY. Use `InputPressed("rmb")` with `isLocal` check + ServerCall
11. `GetPlayerAimInfo` has two forms: simple `GetPlayerAimInfo(p)` or extended `GetPlayerAimInfo(muzzlePos, maxDist, p)`. Use extended for weapons — NOT manual `GetPlayerEyeTransform` + `QueryRaycast`
12. **ALWAYS use `Shoot(pos, dir, "bullet", damage, range, p, "toolId")` for ALL weapons.** Shoot() handles terrain destruction, player damage, kill attribution, bullet trace visuals, and auto-syncs to all clients — all in one call. NEVER use the old `QueryShot + ApplyPlayerDamage + MakeHole` chain — it misses penetration, visuals, sync, and is more code for worse results. MakeHole alone can't damage players. Lint rule `USE-SHOOT` catches the old pattern. (13+ mods still need conversion)
13. Use `QueryShot(pos, dir, len, radius, p)` + `ApplyPlayerDamage(target, damage, "toolId", attacker)` for beam/melee weapons. Always guard with `if player ~= 0` — QueryShot can return `player=0` (= host) for non-player hits. `if player then` is WRONG (Lua 0 is truthy). See Issue #47.
14. Add `SetToolAmmoPickupAmount("id", amount)` for ammo crate integration — without it, mplib can't spawn your tool in loot crates (see `docs/MPLIB_INTERNALS.md`)
15. Entity handles: check `~= 0` not `> 0` (v2 client handles can be negative)
16. No goto/labels (Lua 5.1), no mousedx/mousedy (use camerax/cameray)
17. Gate all `usetool` input with `not data.optionsOpen`
18. Always send aim coordinates WITH ServerCall (never compute aim on server from client action)
19. `client.draw()` not `draw()` for HUD
20. Options menus MUST call `UiMakeInteractive()` before `UiPush()` — without it, buttons render but can't be clicked
21. When freezing player position (scope/flycam), ALWAYS preserve rotation: `SetPlayerTransform(Transform(frozenPos, GetPlayerTransform(p).rot), p)`
22. When server modifies state that client needs for HUD/input gating, use `ClientCall` to sync it immediately
23. For options affecting server gameplay, use `getOptions()` savegame reads each tick — never cache in `data.*` on server
24. Sync `optionsOpen` to server via `server.setOptionsOpen` ServerCall — guard `usetool` on BOTH server AND client
25. `SetPlayerHealth(health, player)` — health value FIRST, player ID SECOND. Reverse silently affects wrong player.
26. Client projectile physics MUST be gated with `IsPlayerLocal(p)` — never simulate projectiles for remote players
27. Use registry sync (`SetFloat`/`SetBool` with `sync=true`) for continuous state — NEVER `ServerCall`/`ClientCall` every tick
28. Throttle `FindShapes()`/`QueryAabb()` to ≤4Hz — never call per-tick per-player
29. `SpawnParticle()`/`PointLight()`/`SetShapeEmissiveScale()` are CLIENT-ONLY — never call on server. **EXCEPTION: `PlaySound()` works on server and auto-syncs to all clients** (confirmed by base game snowball.lua, tank.lua). Call PlaySound directly on server — do NOT wrap in ClientCall.
30. `QueryShot()` + `ApplyPlayerDamage()` must run on SERVER — client uses `QueryRaycast()` for visuals only
31. `info.txt` MUST have `version = 2` for the mod to be recognized as MP-compatible
32. Respawn API: `SetPlayerSpawnTransform(t, p)`, `SetPlayerSpawnHealth(h, p)`, `RespawnPlayer(p)` — server only
33. ToolAnimator: `#include "script/toolanimation.lua"` for proper first/third-person tool poses. Call `tickToolAnimator(animator, dt, nil, p)` in client.tickPlayer
34. **Player param is ALWAYS LAST** in `Set*`/`Get*` functions — the API page almost universally shows it first, which is WRONG. Examples: `SetPlayerColor(r, g, b, p)`, `SetPlayerWalkingSpeed(speed, p)`, `SetPlayerTool(tool, p)`, `SetPlayerRig(rig, p)`, `GetPlayerParam(param, p)`. See MP_REFERENCE.md for full signatures.
35. `ServerCall("server.fn", p, ...)` — player ID `p` is REQUIRED as first param. The engine does NOT auto-inject it. Server functions receive exactly what the client sends. (Issue #51)
36. `Explosion()` does NOT damage players — it destroys terrain + applies physics impulse but NO health damage. Weapons using Explosion MUST add explicit `ApplyPlayerDamage()` with distance falloff + tool ID for kill attribution. (Issue #56)
37. `ClientCall(0, ...)` for world-space effects (sounds, particles at positions visible to all players). `ClientCall(p, ...)` only for personal feedback (camera shake, recoil, HUD sync). Wrong targeting = other players can't hear/see effects. (Issue #58)
38. All asset paths MUST use `MOD/` prefix: `LoadSound("MOD/snd/fire.ogg")`, `LoadSprite("MOD/img/crosshair.png")`, `UiImage("MOD/ui/img.png")`. Without it, assets silently fail to load in v2 (v1 resolved relative paths automatically). (Issue #63)
39. All `#version 2` scripts MUST define at least one callback (`server.init()`, `client.init()`, etc.). Content mods with no script logic need an empty `server.init()` — without it, the engine fails to compile. (Issue #67)
40. Entity scripts (attached to XML entities via `tags="script=foo.lua"`) MUST independently have `#version 2` + v2 callbacks. V1 entity scripts with `init()`/`tick()`/`update()` but no `#version 2` are **silently disabled** in MP — no error, no warning, just missing features (vehicle physics, doors, sirens, lights, etc.). Originally 79 across 10 mods, expanded to 81 across 11 mods, then to 140 across 18 mods after 2026-03-21 workshop sync added new map/vehicle mods; all 140 converted (**100% complete** as of 2026-03-22). Voxel_Plaza has 184 additional v1 entity scripts identified but deferred (map features, low priority). (Issue #68)
41. `#version 2` can appear on ANY line in a script — the preprocessor scans the whole file. Do NOT enforce line-1 placement. However, ensure LF-only line endings in Lua scripts — CRLF can cause compile errors with the preprocessor.
42. **Shared `players[p]` on host causes double-processing.** In `server.tick`, `PlayersAdded` creates `players[p] = createPlayerData()`. In `client.tick`, the guard `if not players[p]` skips creation on the HOST (data already exists from server). Both contexts then share the SAME `data` object. If both `server.tickPlayer` and `client.tickPlayer` modify the same field — arrays (projectile tables) OR scalars (ammo, timers, cooldowns, recoil) — the host gets double-processed values (2x speed, 2x drain). Remote clients get nothing (server-only data never reaches their `data`). **Fix:** Use separate fields (`data.bulletsInAir` vs `data.clientTracers`) or gate client writes with `IsPlayerLocal(p)`. (Issues #69, #70, #72 — 38+ mods affected)
43. `options.lua` needs independent `#version 2` + v2 callbacks (`client.init()`, `client.draw()`) — same silent-disable as entity scripts (Issue #68). Converting only `main.lua` does NOT fix options.lua. **All 9 converted (100% complete** as of 2026-03-20). (Issue #71)
44. **`PlaySound()` on server auto-syncs to all clients.** Do NOT wrap in ClientCall. The engine handles positional audio replication natively. Use `UiSound()` for client-only UI feedback. (Base game pattern — see `docs/BASE_GAME_MP_PATTERNS.md` Pattern 10)
45. **`tickToolAnimator()` must run for ALL players** in a `for p in Players()` loop. Create animators in `PlayersAdded()`, destroy in `PlayersRemoved()`. Do NOT gate behind `IsPlayerLocal(p)` — the function internally selects FP/TP poses. (Base game pattern — see `docs/BASE_GAME_MP_PATTERNS.md` Pattern 6)
46. **Every `PlayersAdded()` MUST have a matching `PlayersRemoved()` cleanup.** Per-player state tables, animators, timers, and projectile lists all leak if not cleaned up on disconnect. (Base game pattern — see `docs/BASE_GAME_MP_PATTERNS.md` Pattern 8)
47. **Use `GetEventCount("playerdied")`/`GetEvent()` for death detection** — do NOT poll `GetPlayerHealth()` every tick. Events fire exactly once, no tracking table needed. (Base game pattern — see `docs/BASE_GAME_MP_PATTERNS.md` Pattern 5)
48. **Use registry broadcast for continuous state:** `SetInt/SetFloat/SetBool(key, value, true)` with the `true` flag. Do NOT use per-tick ServerCall/ClientCall for state that changes every frame (ammo counts, positions, timers). (Base game pattern — see `docs/BASE_GAME_MP_PATTERNS.md` Pattern 2)

## Known Subagent Bugs (agents ALWAYS make these)

When dispatching subagents for ANY Teardown mod work, ALWAYS include:
1. `Players()`/`PlayersAdded()`/`PlayersRemoved()` are ITERATORS — NO `ipairs()`
2. Raw keys (`"rmb"`, `"r"`, etc.) do NOT take player param — use `InputPressed("rmb")` + ServerCall
3. `SetToolEnabled("toolid", true, p)` — string first, bool second, player third
4. After `QueryShot()`, guard with `player ~= 0` — NOT `if player then` (Lua 0 is truthy, damages host)
5. `ServerCall("server.fn", p, ...)` — ALWAYS pass player ID `p` explicitly as first param. Engine does NOT auto-inject it. (Issue #51)
6. **#1 DESYNC BUG: Do NOT modify the same `data.*` field in both `server.tickPlayer` and `client.tickPlayer`** — host runs both and gets 2x processing. Timers, cooldowns, ammo, reload state — ALL must be single-owner. Server owns gameplay state. Client owns visual state. Use `shared.*` to sync server state to client for HUD display. Lint rule `DOUBLE-PROCESS-TIMER` catches timer patterns but NOT all variants — always manually verify. Found in 12+ mods. (Issues #42, #72)
7. ALWAYS run `python -m tools.lint --mod "ModName"` after writing any mod code
8. `PlaySound()` on server auto-syncs — do NOT use ClientCall to play sounds. Just call PlaySound on server.
9. `tickToolAnimator()` must be called for ALL players in `for p in Players()` — NOT just the local player. It handles FP/TP internally.
10. Do NOT use per-tick ServerCall/ClientCall for continuous state. Use `SetInt/SetFloat/SetBool(key, value, true)` (registry broadcast) or `shared.*` tables.
11. Use `ClientCall(0, ...)` for world-visible events (sounds, particles at a position). Use `ClientCall(p, ...)` only for personal feedback (camera shake, HUD sync).
12. Use `GetEventCount("playerdied")`/`GetEvent()` for death detection — do NOT poll `GetPlayerHealth()` every tick.
13. Clean up per-player state in `PlayersRemoved()` — missing cleanup causes state leaks (wrong settings for new players inheriting old IDs).
14. `InputPressed(variable, p)` with a **variable** key name bypasses RAW-KEY-PLAYER lint detection. After lint reports 0 findings, manually grep for `InputPressed/InputDown/InputReleased` where the first arg is NOT a string literal — these are invisible to automated checks. Same fix: move to client with `IsPlayerLocal(p)` + ServerCall. (Issue #73)
15. **Timer/cooldown pattern:** Server owns `shootTimer`, `reloadTimer`, `hookCooldown`, `magazine`, `reserveAmmo`. Client uses SEPARATE fields: `clientShootTimer`, `clientReloadTimer`, `clientReloading`. Server syncs to client via `shared.*` tables. Client reads `shared` for HUD display. NEVER decrement the same timer in both server.tick and client.tick.
16. **Sound loading:** Load sounds in BOTH `server.init()` AND `client.init()` if the server needs to call `PlaySound()` (auto-syncs). Client-only sounds (UI feedback) only need `client.init()`.
17. **Visual recoil:** `recoilPos`, `recoilVel`, `recoilRot`, `recoilRotVel` are CLIENT-ONLY visual fields. Set the impulse (`recoilVel += 0.6`) in the CLIENT shoot handler, not on the server. The server should never touch visual spring physics.
18. **ALWAYS use `Shoot()` for weapons** — NEVER `QueryShot + ApplyPlayerDamage + MakeHole`. `Shoot(pos, dir, "bullet", damage, range, p, "toolId")` handles everything: terrain, players, kill feed, bullet trace, MP sync. The old manual chain is more code for worse results. Lint rule `USE-SHOOT` catches this.

## Do NOT Copy Preview Images Into Mod Folders

**NEVER copy preview.jpg/preview.png files from workshop originals into `Documents/Teardown/mods/`.** This crashed the game engine (strncpy buffer overflow during mod enumeration). The engine handles workshop previews through Steam — local copies are unnecessary and dangerous. (Issue #66)

## Do NOT Use Agents/Subagents

**Do NOT dispatch subagents for ANY work in this project.** Subagents have repeatedly caused issues — wrong API patterns, single-player code, desync bugs, incorrect file edits. All work must be done by the main terminal directly. No exceptions. If the task is too large, break it into smaller pieces and do them sequentially.

## Re-Read CLAUDE.md Before Every Write

**Before writing ANY code — mod files, tool files, docs, configs — re-read the relevant sections of this file.** Specifically:
- Before editing mod code: re-read "TOP PRIORITY: Match Base Game MP Patterns" (8 rules) and "Known Subagent Bugs" (18 rules)
- Before editing tools: re-read "Developer Tools" section
- Before creating tasks: re-read "Batch Pass System"
- If in doubt about ANY pattern, re-read. Never write from memory — patterns evolve and memory drifts.

## Do NOT Modify Asset Files

**NEVER modify `.vox`, `.xml` prefab, `.png`, `.ogg`, or other asset files in mod directories.** Only edit `.lua` scripts and `info.txt`. Creating or modifying asset files (e.g., adding `main.xml` to Jetskis, copying `flamer.vox`) has caused game crashes. If a mod has broken/missing assets, document it — don't try to fix the assets.

## Active Mod Count Ceiling

**Warn the user when active mods approach 150.** The Teardown engine crashes from shadow volume integer overflow at ~178 active mods. Safe limit is ~125-150. Audio memory also becomes a concern above 150 (760MB+ causes instability). When installing new mods from the workshop backlog (~75 pending), track the total active count and advise the user which to keep disabled.

## Clear __pycache__ Before Batch Tests

**Always run `find . -name "__pycache__" -type d -exec rm -rf {} +` before `python -m tools.test --batch all --static`.** Stale Python bytecode caused phantom test results for an entire session. Do this after ANY change to `tools/*.py`.

## Crash Investigation Protocol

When the user reports a game crash:
1. **Check ALL file types changed** — not just `.lua`. Preview images, `.vox` files, `.xml` prefabs, and directory structure changes can all crash the engine.
2. **Read the crash dump** — check `AppData/Local/Teardown/crash/` for `callstack.txt`, `error.yaml`. The `callstack_lua` field shows if it's a Lua or C++ crash.
3. **Don't dismiss game log errors as stale** — compile errors may be real bugs our tools don't catch (deepcheck checks semantics, not syntax).
4. **Check file modification times** — `find mods/ -mmin -N` to narrow which files changed since the last working state.

## Every Installed Mod Must Have id.txt

When installing or patching any mod, ensure it has an `id.txt` with the Steam Workshop ID on the first line. Without it, workshop sync is unreliable — 97 mods were missing id.txt, making subscription tracking a manual guessing game. If the workshop ID is unknown, check the workshop folder by matching mod name/author.

## No Mod Edits While Game Is Running

**Before writing to `Documents/Teardown/mods/`, check if the game is running:**
```
tasklist | grep -i teardown
```
If `teardown.exe` is running, do NOT edit mod files. Wait for the user to close the game first. Editing files mid-session can corrupt game state.

## QA Lead Batch Reports Must List Exact Changes

When reporting a completed batch to the user, list the **exact file paths and line ranges** changed — not just mod names. Example:
```
Batch 3 complete:
- AC130_Airstrike_MP/main.lua: lines 88-95 (removed v1 SetBool, added PlayersAdded loop)
- Bunker_Buster_MP/main.lua: lines 310-315 (same fix)
Lint: both clean. Deepcheck: both PASS.
```
This lets the user know exactly what to revert if something breaks.

## First Change = Immediate Test

At the start of every session that will edit mods, make ONE small change to ONE mod, then ask the user to launch the game and verify it works. This catches environmental issues (engine limits, corrupted state, Steam updates) before the team does a full batch of work. Only proceed with real batches after the smoke test passes.

## If a Batch Breaks the Game, Revert Immediately

If the user reports a crash or breakage after a batch, **revert that batch's changes immediately** — `git checkout` the changed files back to the last commit. Don't spend hours investigating which of the 2-3 changes caused it. After reverting, reapply changes one mod at a time to isolate the culprit. The per-batch commits make this easy.

## Tools Passing ≠ Game Works

Lint clean + deepcheck PASS does not guarantee the mod works in-game. Only in-game testing by the user is the final word. The team should never claim a mod is "done" based purely on tool output — it's **"done pending user test"** until the user confirms in-game.

## Realistic Ballistics Framework (MANDATORY for all weapons)

**Every weapon and tool mod MUST use the Realistic Ballistics Framework** (`lib/realistic_ballistics.lua`). No more inline damage code, no more per-mod MakeHole/QueryShot chains, no more copy-pasted falloff math.

### What It Is
A shared Lua library that handles ALL weapon firing mechanics: damage, penetration, spread, distance falloff, and MP sync. One `#include`, one profile definition, one function call to fire.

### Where It Lives
- **Source:** `lib/realistic_ballistics.lua` (in the project repo)
- **Deployed:** Copy into each weapon mod as `lib/ballistics.lua`
- **Include:** `#include "lib/ballistics.lua"` in the mod's main.lua

### When To Use It
- **Guns/firearms:** Shotguns, rifles, pistols, miniguns — use `FireFromTool()` with pellet count + spread
- **Beam/laser weapons:** Use `FireProjectile()` per tick with low damage for continuous damage
- **Melee weapons:** Use `FireProjectile()` at short range for hit detection + terrain damage
- **Explosive launchers:** Use the falloff system for projectile impact damage
- **ANY tool that damages terrain or players** — if it calls Shoot(), MakeHole(), or ApplyPlayerDamage(), it should use this framework instead

### The Vision
This framework will expand to cover ALL tools — not just weapons. Future additions:
- **Tool physics** (recoil profiles, weight, sway)
- **Visual effects profiles** (muzzle flash, impact particles, tracer style)
- **Audio profiles** (fire sound, impact sound, reload sound with distance attenuation)
- **Ammo systems** (magazine + reserve, reload behavior, ammo types)
- **Non-weapon tools** (grappling hooks, welding, cutting, construction — interaction ranges, effect profiles)

The goal: every tool in the game feels finely tuned, realistic, and consistent. One framework, one set of knobs to tune, zero duplicated code across 100+ mods.

### How To Use It
```lua
#include "lib/ballistics.lua"

local myGun = CreateBallisticsProfile({
    damage = 20, pellets = 1, spread = 0.02,  -- single accurate bullet
    range = 100, toolId = "my-rifle",
    holeScale = 1.0, penScale = 0.5,
    fullRange = 15, halfRange = 60, minFalloff = 0.2,
})

-- In server.tickPlayer, when player fires:
myGun:FireFromTool(toolBody, muzzleOffset, player)
```

### Key Properties
| Property | Controls | Example Values |
|----------|----------|---------------|
| `damage` | Base damage per projectile (÷100) | 28 (shotgun), 50 (rifle), 8 (SMG) |
| `pellets` | Projectiles per shot | 1 (rifle), 8 (shotgun), 24 (spread shotgun) |
| `spread` | Cone angle (0 = laser) | 0 (sniper), 0.02 (rifle), 0.07 (shotgun) |
| `holeScale` | Crater size multiplier | 0.5 (small holes), 1.0 (normal), 2.0 (large) |
| `penScale` | Extra MakeHole penetration | 0 (Shoot only), 1.0 (punch through walls) |
| `fullRange` | Full damage zone (meters) | 3 (shotgun), 15 (rifle), 30 (sniper) |
| `halfRange` | 50% damage distance | 25 (shotgun), 60 (rifle), 150 (sniper) |
| `minFalloff` | Damage floor multiplier | 0.1 (weak at range), 0.5 (strong at range) |

## Plugins & Agents — USE THEM

You have powerful plugins. Key rules:

- **Bug or failure?** → `Skill: superpowers:systematic-debugging` BEFORE guessing
- **About to mark task done?** → `Skill: superpowers:verification-before-completion` FIRST
- **2+ independent tasks?** → `Skill: superpowers:dispatching-parallel-agents` to parallelize
- **Just wrote/modified code?** → Dispatch `code-simplifier:code-simplifier` or `feature-dev:code-reviewer`
- **Need tests?** → Dispatch `test-writer-fixer:test-writer-fixer`
- **Looking for patterns?** → Dispatch `agent-codebase-pattern-finder:codebase-pattern-finder`
- **Planning multi-step work?** → `Skill: superpowers:writing-plans`

## Reference Docs

| Doc | When to read | Contents |
|-----|-------------|----------|
| **`docs/BASE_GAME_MP_PATTERNS.md`** | **Every session** | 12 patterns from vanilla code: server-owns-logic, registry broadcast, shared tables, ToolAnimator, PlaySound auto-sync, event-driven deaths. Gold standard. |
| **`docs/WHAT_WORKS.md`** | **Before any fix** | Proven fixes from our project. |
| **`docs/WHAT_DOESNT_WORK.md`** | **Before any fix** | Failed approaches — never repeat. |
| `docs/MP_REFERENCE.md` | When fixing specific MP issues | Function signatures, server/client split, sync mechanisms, 7 desync root causes, RPC fix patterns, vanilla code patterns. |
| `docs/MPLIB_INTERNALS.md` | AmmoPickup / loot work | How loot crates, drops, and ammo pickup work inside mplib. |
| `docs/UMF_TRANSLATION_GUIDE.md` | Converting UMF mods | UMF API → v2 equivalents, 15-point checklist. |
| `docs/UI_STANDARDS.md` | Editing any HUD code | Layout zones, font sizes, menu standards. |
| `lib/realistic_ballistics.lua` | **Any weapon/tool damage code** | Shared framework: falloff, penetration, spread, Shoot()+MakeHole. MANDATORY for all weapons. |
| `docs/AUDIT_REPORT.md` | Feature matrix | Generated. Regenerate: `python -m tools.audit --output docs/AUDIT_REPORT.md` |
| `ISSUES_AND_FIXES.md` | Debugging | 73 documented bugs with root causes, fixes, and rules. |
| `MASTER_MOD_LIST.md` | After converting mods | All patched mods by batch with workshop IDs. |
