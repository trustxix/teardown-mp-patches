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

You are one of 3 terminals that coordinate via MCP tools and a filesystem inbox system.

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
20. Options menus MUST call `UiMakeInteractive()` before `UiPush()` — without it, buttons render but can't be clicked

## Known Subagent Bugs (agents ALWAYS make these)

When dispatching subagents for ANY Teardown mod work, ALWAYS include:
1. `Players()`/`PlayersAdded()`/`PlayersRemoved()` are ITERATORS — NO `ipairs()`
2. Raw keys (`"rmb"`, `"r"`, etc.) do NOT take player param — use `InputPressed("rmb")` + ServerCall
3. `SetToolEnabled("toolid", true, p)` — string first, bool second, player third
4. ALWAYS run `python -m tools.lint --mod "ModName"` after writing any mod code

## Do NOT Use Agents to Write Mod Code

Agents can research, analyze, update docs, run tools. But mod rewrites must be done manually.

## Reference Docs

The tools automatically tell you which docs to read:
- `python -m tools.status` outputs a "Recommended reading" section based on current project state
- `python -m tools.lint` findings include "See docs/RESEARCH.md Finding #N" or "See ISSUES_AND_FIXES.md Issue #N" where relevant

**When the tools point you to a doc, read it.** Here's what each contains:

| Doc | Contents |
|-----|----------|
| `docs/RESEARCH.md` | 42 findings on official API patterns — Shoot(), GetPlayerAimInfo(), QueryShot(), SetToolAmmoPickupAmount(), sync mechanisms, tool animation, kill attribution. Exact function signatures + code from official mods. |
| `docs/V2_SYNC_PATTERNS.md` | Registry sync, RPC (ServerCall/ClientCall), shared table, local-prediction + server-synced-remote pattern, quaternion sync, interpolation tuning. For any mod with custom entities. |
| `docs/AUDIT_REPORT.md` | Generated feature matrix — which mods have/lack each feature. Regenerate: `python -m tools.audit --output docs/AUDIT_REPORT.md` |
| `ISSUES_AND_FIXES.md` | 32 resolved bugs with root causes, fixes, and rules. Check before debugging. Append after fixing new bugs. |
| `MASTER_MOD_LIST.md` | All patched mods by batch with workshop IDs. Update after converting new mods. |
| `C:/Users/trust/Documents/Teardown/TEARDOWN_V2_API_REFERENCE.md` | Full v2 API (550+ functions). For exact function signatures. |
