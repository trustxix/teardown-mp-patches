# Teardown MP Mod Patcher

## MANDATORY — Do This First Every Session

**Before doing ANYTHING else, run:**
```
cd C:/Users/trust/teardown-mp-patches && python -m tools.status
```
This tells you: mod count, last commit, game log errors, lint failures, and missing features.
Do NOT skip this. Do NOT start working without it. The output replaces reading multiple doc files.

**Then check your inbox and task queue (via MCP):**
```
Use MCP tools: check_inbox(your_role) → process messages → get_task(your_role) → do work
```

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

**Your work loop (MANDATORY — never stop unless killswitch):**
1. `check_killswitch()` — **if active, STOP. Do not continue. Wait for user.**
2. `get_focus()` — read the current team focus area
3. `check_inbox(your_role)` — process messages first (highest priority). If you see a STOP ORDER, finish current task and halt.
4. `clear_message()` each processed message
5. `get_task(your_role)` — pick up next queued task within the focus area
6. **BROADCAST START:** `broadcast(your_role, "info", "low", "STARTING: [task id] [title] — mods: [list]")`
7. Do the work
8. `has_mail(your_role)` — **call this after EVERY tool call** (Read, Edit, Write, Bash). It's cheap. If you have mail, process it before continuing. If it's a STOP ORDER, finish your current task and halt.
9. `complete_task()` when done
10. **BROADCAST DONE:** `broadcast(your_role, "info", "low", "FINISHED: [task id] [summary of what changed]")`
11. If no inbox or tasks: `get_lint_summary()` / `get_audit_summary()` to find work
12. GOTO 1

**KILLSWITCH:** If you see a STOP ORDER in your inbox OR `check_killswitch()` returns `active: true`, finish your current task cleanly (don't leave broken code), then HALT completely. Do not pick up new tasks. Output "HALTED — waiting for instructions" and wait.

**CRITICAL: Check inbox constantly.** Call `has_mail(your_role)` after every single tool call. If it returns `has_mail: true`, immediately call `check_inbox` and process messages before continuing your current task. This is not optional — it's how the team stays synchronized.

**When QA Lead sends a `brainstorm` message:** Stop current work, analyze the topic, send your recommendations back to QA Lead's inbox. Wait for QA Lead's decision before resuming.

**Message protocol:** See `.comms/PROTOCOL.md` for format details.
**When to message:** See `.comms/TRIGGERS.md` for exactly when to write to other inboxes.
**Team collaboration:** See `.comms/TEAMWORK.md` for how all 3 terminals work together on the same focus area.

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
| `python -m tools.lint` | Scan all mods for 25 known bugs (includes info.txt validation) |
| `python -m tools.lint --mod "X"` | After editing a specific mod |
| `python -m tools.lint --tier 1` | Hard errors only (crashes/silent failures) |
| `python -m tools.fix --dry-run` | Preview safe auto-fixes across all mods |
| `python -m tools.fix` | Apply all 6 deterministic auto-fixes |
| `python -m tools.fix --mod "X" --only ipairs-iterator` | Targeted fix |
| `python -m tools.audit` | Feature matrix — what each mod has/needs |
| `python -m tools.audit --output docs/AUDIT_REPORT.md` | Save audit to file |
| `python -m tools.logparse` | Parse Teardown log.txt for errors by mod |
| `python -m tools.logparse --mod "X"` | Filter errors to one mod |
| `python tools/gun_v2_generator.py` | Generate complete v2 main.lua for standard gun mods (batch) |

**Tests:** `python -m pytest tests/ -q` — 309 tests covering all tools.

## Where Mods Live

- **ALL edits go here:** `C:/Users/trust/Documents/Teardown/mods/` — game reads from this
- **NEVER edit:** `C:/Users/trust/teardown-mp-patches/mods/` — patches repo, game ignores it
- **Workshop originals:** `C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/`
- **Backup:** `C:/Users/trust/Documents/Teardown/mods_BACKUP/`

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
8. Server handles: MakeHole, Explosion, SetBodyVelocity, ApplyBodyImpulse, Spawn, Delete, SpawnFire, Shoot, SetPlayerVelocity, SetPlayerTransform, ApplyPlayerDamage, DisablePlayerInput, SetPlayerColor, SetPlayerWalkingSpeed
9. Client handles: PlaySound, SpawnParticle, DrawLine, DrawSprite, PointLight, SetToolTransform, SetCameraTransform, ShakeCamera, SetCameraDof, DrawBodyOutline, all Ui* functions
10. NEVER use raw keys with player param: `InputPressed("rmb", p)` FAILS SILENTLY. Use `InputPressed("rmb")` with `isLocal` check + ServerCall
11. `GetPlayerAimInfo` has two forms: simple `GetPlayerAimInfo(p)` or extended `GetPlayerAimInfo(muzzlePos, maxDist, p)`. Use extended for weapons — NOT manual `GetPlayerEyeTransform` + `QueryRaycast`
12. Use `Shoot(pos, dir, "bullet", damage, range, p, "toolId")` for guns — NOT `MakeHole` (MakeHole can't damage players). The `"toolId"` enables kill attribution in the kill feed.
13. Use `QueryShot(pos, dir, len, radius, p)` + `ApplyPlayerDamage(target, damage, "toolId", attacker)` for beam/melee weapons
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
29. `PlaySound()`/`SpawnParticle()` are CLIENT-ONLY — never call on server
30. `QueryShot()` + `ApplyPlayerDamage()` must run on SERVER — client uses `QueryRaycast()` for visuals only
31. `info.txt` MUST have `version = 2` for the mod to be recognized as MP-compatible
32. Respawn API: `SetPlayerSpawnTransform(t, p)`, `SetPlayerSpawnHealth(h, p)`, `RespawnPlayer(p)` — server only
33. ToolAnimator: `#include "script/toolanimation.lua"` for proper first/third-person tool poses. Call `tickToolAnimator(animator, dt, nil, p)` in client.tickPlayer

## Known Subagent Bugs (agents ALWAYS make these)

When dispatching subagents for ANY Teardown mod work, ALWAYS include:
1. `Players()`/`PlayersAdded()`/`PlayersRemoved()` are ITERATORS — NO `ipairs()`
2. Raw keys (`"rmb"`, `"r"`, etc.) do NOT take player param — use `InputPressed("rmb")` + ServerCall
3. `SetToolEnabled("toolid", true, p)` — string first, bool second, player third
4. ALWAYS run `python -m tools.lint --mod "ModName"` after writing any mod code

## Do NOT Use Agents to Write Mod Code

Agents can research, analyze, update docs, run tools. But mod rewrites must be done manually.

## Plugins & Agents — USE THEM

You have powerful plugins. **Read `docs/TEAM_PLUGINS.md` for the full list and when to use each.** Key rules:

- **Bug or failure?** → `Skill: superpowers:systematic-debugging` BEFORE guessing
- **About to mark task done?** → `Skill: superpowers:verification-before-completion` FIRST
- **2+ independent tasks?** → `Skill: superpowers:dispatching-parallel-agents` to parallelize
- **Just wrote/modified code?** → Dispatch `code-simplifier:code-simplifier` or `feature-dev:code-reviewer`
- **Need tests?** → Dispatch `test-writer-fixer:test-writer-fixer`
- **Looking for patterns?** → Dispatch `agent-codebase-pattern-finder:codebase-pattern-finder`
- **Planning multi-step work?** → `Skill: superpowers:writing-plans`

## Reference Docs

The tools automatically tell you which docs to read:
- `python -m tools.status` outputs a "Recommended reading" section based on current project state
- `python -m tools.lint` findings include "See docs/RESEARCH.md Finding #N" or "See ISSUES_AND_FIXES.md Issue #N" where relevant

**When the tools point you to a doc, read it.** Here's what each contains:

| Doc | Contents | Authority |
|-----|----------|-----------|
| **`docs/OFFICIAL_DEVELOPER_DOCS.md`** | **Complete official API from teardowngame.com. ALL function signatures, MP architecture, networking internals, mplib, gotchas. THIS IS GROUND TRUTH — overrides all other docs on conflicts.** | **HIGHEST** |
| `docs/RESEARCH.md` | 42 findings on official API patterns — Shoot(), GetPlayerAimInfo(), QueryShot(), SetToolAmmoPickupAmount(), sync mechanisms, tool animation, kill attribution. Exact function signatures + code from official mods. | High |
| `docs/V2_SYNC_PATTERNS.md` | Registry sync, RPC (ServerCall/ClientCall), shared table, local-prediction + server-synced-remote pattern, quaternion sync, interpolation tuning. For any mod with custom entities. | High |
| `docs/MP_DESYNC_PATTERNS.md` | 6 root causes of MP desync/lag: client projectile physics, per-tick RPC, FindShapes spam, server-side effects, raw key input, client QueryShot. Fix patterns for each. **Read before editing any mod.** | High |
| `docs/MPLIB_INTERNALS.md` | How loot crates, weapon drops, and ammo pickup actually work inside mplib/tools.lua. Essential for understanding why SetToolAmmoPickupAmount matters. | High |
| `docs/PER_TICK_RPC_FIX_GUIDE.md` | Decision tree + 4 fix patterns for the 69 PER-TICK-RPC lint warnings. **Read before fixing any PER-TICK-RPC finding.** | High |
| `docs/TEAM_PLUGINS.md` | All available plugins, agents, and skills with when-to-use decision table. **Every terminal should read this.** | High |
| `docs/AUDIT_REPORT.md` | Generated feature matrix — which mods have/lack each feature. Regenerate: `python -m tools.audit --output docs/AUDIT_REPORT.md` | Generated |
| `ISSUES_AND_FIXES.md` | 46 resolved bugs with root causes, fixes, and rules. Check before debugging. Append after fixing new bugs. | Project |
| `MASTER_MOD_LIST.md` | All patched mods by batch with workshop IDs. Update after converting new mods. | Project |
| `C:/Users/trust/Documents/Teardown/TEARDOWN_V2_API_REFERENCE.md` | Full v2 API (550+ functions). For exact function signatures. | Reference |

### Official Sources (always prefer these over community info)
- **Modding homepage:** https://www.teardowngame.com/modding/
- **MP Modding guide:** https://teardowngame.com/modding-mp/index.html
- **Lua API reference:** https://www.teardowngame.com/modding/api.html
- **API XML (machine-readable):** https://www.teardowngame.com/modding/api.xml
- **mplib source:** https://github.com/tuxedolabsorg/mplib
- **Networking blog post:** https://blog.voxagon.se/2026/03/13/teardown-multiplayer.html
