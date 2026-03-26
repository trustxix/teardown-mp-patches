# Last Session: 2026-03-25

## What Was Done

### Claude Code Global System (built from scratch)
- Built 6 hook scripts: destructive-gate, conflict-detector, syntax-validator, bash-error-helper, session-context, uncommitted-check
- Built 12 slash commands: /orient, /fix, /backup, /validate, /review-changes, /deploy-mod, /audit, /quick-test, /remember, /wrap-up, /init-project, /status
- Built 5 subsystem rulesets: game-modding-lua, game-modding-csharp, web-node, python-tools, ios-dev
- Created global CLAUDE.md (113 lines, ~69 rules)
- Created settings.json with deny list, hooks, and dontAsk mode

### Teardown Project Cleanup
- CLAUDE.md trimmed 475 → 252 lines (removed team system overhead, preserved all coding rules)
- Team system archived to archive/team-system/ (5 ROLE files, 229 .comms messages, 6 MCP servers)
- Documents/Teardown/mods/ cleared (49 duplicate mods, 1.9GB freed) and hard-blocked
- Memory files cleaned: 13 → 10 (merged duplicates, fixed contradictions, removed superseded)
- mousedx/camerax contradiction fixed in FIX_PLAN, MP_REFERENCE, ISSUES_AND_FIXES
- Stale consolidation plans archived
- Credentials stripped from 3 files (delete_workshop.py, Publish_Teardown_Mods.py, Delete_Workshop_Web.py)

### DEF Framework (Desync Exterminator Framework)
- Built lib/def.lua v1.2 — preprocessor-safe architecture with top-level callbacks
- Converted Charge_Shotgun from v1 (189 lines) to v2+DEF (220 lines)
- Documented 9 new issues (#80-88) in ISSUES_AND_FIXES.md
- Added 9 new rules to CLAUDE.md Known Subagent Bugs section
- Created lib/def_example.lua with full before/after conversion guide

### Workshop Publisher Tool
- Rewrote Publish_Teardown_Mods.py: update-only (no new publishes), vanilla filter, VDF escaping, change detection with categorized diffs, line previews, upload size estimates
- Matched all 49 Workshop IDs from subscribed mods
- Published 5 updated mods successfully (Charge_Shotgun, FPV_Drone_Tool, Performance_Mod, Predator_Missile_MP, Thruster_Tool_Multiplayer)
- Created update.bat for one-click Workshop updates

### Workshop Tools Fixed
- Fixed Delete_Workshop_Web.bat wrong path
- Fixed Delete_Workshop_Duplicates.bat missing env var note
- Fixed visibility from friends-only to public
- Cleaned dead artifacts (stale IDs, empty results, pycache)

## Incomplete Work
- 14 v1 mods still need DEF conversion (Asteroid_Strike, Black_Hole, C4, Desert_Eagle, Exploding_Star, High_Tech_Drone, Hook_Shotgun, Jetskis, Laser_Cutter, Multiple_Grenade_Launcher, ODM_Gear, Rocket, Russian_Town_4_MP, Tool_Menu)
- Charge_Shotgun needs in-game MP testing (converted but not play-tested)
- DEF has no projectile tracer system yet (visual feedback for custom projectiles)
- Desktop/Teardown-ModSync flagged for deletion (redundant exe copies) — user denied rm -rf
- Steam password needs rotation (was exposed in conversation)

## Next Steps
1. Test Charge_Shotgun in-game (solo first, then MP)
2. Convert more v1 mods using DEF (start with simple ones: C4, Rocket, Laser_Cutter)
3. Add client-side tracer system to DEF for projectile visuals
4. Rotate Steam password

## Gotchas Discovered
- v2 preprocessor breaks closures inside function definitions (Issue #80) — always define server/client callbacks at top level
- PlayersAdded/PlayersRemoved/Players iterators consumed after one pass (Issue #81) — collect into table first
- SpawnParticle/PointLight are CLIENT-ONLY, PlaySound on server is the exception (Issue #83)
- Server-owned timers need explicit registry sync for client visuals (Issue #84)
- LoadLoop() is client-only — must use ClientInit hook (Issue #85)
- VDF file paths must NOT be escaped — only title/description need vdf_escape (would have broken all Workshop uploads)
- Workshop visibility "1" = friends-only, "0" = public (was publishing as friends-only)

---

# Session: 2026-03-25 (Part 2)

## What Was Done
- Built teardown-autosync.js hook — mirrors mod edits to sandbox via robocopy /MIR on every Write/Edit/Bash
- Built sync_installs.py with robocopy backend, per-mod change detection, --check verify mode
- Built sync.bat for bulk sync, update.bat for Workshop updates
- Initial full sync: 49 mods, 1.8GB, 6792 files to sandbox — verified identical
- Added game-running warning to PreToolUse guard
- Added /test-mp command for MP testing workflow
- Removed polling watcher (wasteful) — autosync hook is event-driven, zero overhead when idle

## Gotchas Discovered
- subprocess.run on Windows spawns visible cmd windows — use STARTUPINFO with SW_HIDE
- robocopy /MIR exit codes 0-7 are success, 8+ are errors — node throws on any non-zero
- Polling watchers are wasteful — event-driven hooks are better when Claude Code is the primary editor

---

# Session: 2026-03-26

## What Was Done

### Documentation Consolidation (entire session)
Consolidated ALL Teardown knowledge from 13 scattered filesystem locations, 22 memory files, 82 git commits, and 14 existing project docs into 4 new documents + updates.

**New docs:**
- `docs/TESTING_SETUP.md` — Sandboxie dual-Steam, mod sync, modlists, crash logs
- `docs/ECOSYSTEM.md` — 13 dirs, 25+ tools, 4 hooks, pipeline, trust-realism, game config
- `docs/KNOWN_LIMITATIONS.md` — Engine limits, preprocessor, camera, v1→v2, desync RC1-7, interpolation, UMF, pending work
- `docs/LINT_RULES.md` — All 45 lint rules, 6 deepcheck validators, API database

**Drift elimination:**
- Fixed QUICKSTART.md: options.lua handling + mod path (contradicted 3 other files)
- Converted 19 memory files from stale duplicates to canonical-source pointers

**Trust Realism sync:**
- `lib/realistic_ballistics.lua` → `~/trust-realism/src/ballistics.lua` (patcher is source of truth)

**10 commits, all pushed** (65a1c642..77e70a59 on patcher, 7d35b60 on trust-realism)

## Incomplete Work
- `docs/V2_SYNC_PATTERNS.md` — flagged as needed, not created
- 14 v1 mods still need DEF conversion
- Charge_Shotgun + Predator_Missile_MP need in-game MP testing
- ~75 workshop subs pending install
- AIO integration with Trust Realism (5-phase plan)
- Outdated TEARDOWN_V2_API_REFERENCE.md in Documents needs regenerating

## Next Steps
1. Create `docs/V2_SYNC_PATTERNS.md` (the one missing doc)
2. Resume mod conversion (DEF-based v1→v2)
3. Test Charge_Shotgun + fix Predator_Missile_MP in-game
4. Install pending workshop mods (watch 150 ceiling)

## Gotchas Discovered
- QUICKSTART.md had two wrong facts (options.lua + mod dir) — now fixed
- Memory files are a drift vector — 19 contained stale knowledge, all converted to pointers
- trust-realism was 13 lines behind patcher (shared.toolOptions superseded by registry reads)
- 25+ tools in tools/ but only 6 were in CLAUDE.md — full inventory now in ECOSYSTEM.md
- Global autosync hook wasn't documented anywhere — now in ECOSYSTEM.md

---

# Session: 2026-03-26 (Part 2 — Mod Fixes + Workflow Overhaul)

## What Was Done

### Bulk Lint Fixes (526 FAIL → 0)
- 461 FILE-SCOPE-LOCAL: stripped `local` from file-scope vars (42 files)
- 126 V1-ENTITY-SCRIPT: auto-converted to v2 callbacks (entity_v2_convert)
- ~94 RAW-KEY-PLAYER: removed player param from raw keys
- ~62 DRAW-NOT-CLIENT: renamed draw() → client.draw()
- ~47 MISSING-VERSION2: added #version 2 headers
- 29 MISSING-AMMO-PICKUP: added SetToolAmmoPickupAmount
- 25 INFO-MISSING-VERSION2: added version = 2 to info.txt
- 12 MISSING-TOOL-AMMO: added SetToolAmmo in PlayersAdded
- 4 DOUBLE-PROCESS-TIMER: gated client coolDown with IsPlayerLocal
- 4 DAMAGE-NO-ATTACKER: added attacker param (Light_Katana, Light_Saber)
- ~50 lint suppressions with documented reasons (false positives)

### RegisterTool Fix (15 mods invisible in toolbar)
- Root cause: v1 `SetBool("game.tool.X.enabled", true)` doesn't register tools in v2 MP
- Added RegisterTool() + SetToolEnabled() + SetToolAmmo() + PlayersAdded loops
- Also added #include player.lua where needed
- CnC_Weather_Machine had p→id bug in SetToolAmmo — fixed

### Built-In Mod Protection
- 123 files restored by Steam verify after we modified built-in mods
- Added 3 safeguards: CLAUDE.md rule, pre_edit_guard hook, discover_mods() filter
- All tools now skip 40 built-in mods automatically

### New Working Directory
- All mods moved to D:/The Vault/Modding/Games/Teardown/ (49 custom mods)
- Updated ALL tool paths: common.py, publish.py, sync.py, deploy_framework.py, pack.py
- Updated ALL hooks: pre_edit_guard, post_edit_lint, post_write_fix_lua
- Disabled autosync hook (no longer needed)
- Game install dirs are now read-only (managed by Workshop)

### Workshop Publishing Overhaul
- Publish script reads from new working directory
- Batched uploads: single SteamCMD session for all mods (was one per mod)
- Parsing: split on "Preparing update..." for per-item success/fail
- update.bat: publish → SteamTestLauncher.exe (restarts both Steam clients)
- SteamTestLauncher.exe: moves main Steam to monitor 1, sandboxed to monitor 3
- Steam Guard session cached (authenticate once, reuse for weeks)
- Credentials set via setx env vars + hardcoded in update.bat

### MP Testing Guide
- Created docs/MP_TESTING_GUIDE.md with 3-tier priority testing
- Created Desktop/TEST_SHEET.md with HOST/CLIENT lines per mod
- Convention: blank = UNTESTED (never assume blank = working)

## Incomplete Work
- MP testing not yet started (all prep work done, test sheet ready)
- 19 deep analysis FAILs (SERVER-EFFECT in entity scripts — structural)
- PER-TICK-RPC (25 WARN) — need per-mod registry conversion
- V2_SYNC_PATTERNS.md still not created
- Jetskis, Rocket, gm_construct_MP have no #version 2

## Next Steps
1. User runs update.bat to publish all changes
2. User fills out TEST_SHEET.md during MP testing
3. User submits results — I fix broken mods and repeat
4. After testing pass: address remaining WARN issues

## Gotchas Discovered
- 15 mods invisible in toolbar: v1 SetBool pattern doesn't register tools in v2 MP
- Modifying built-in mods causes MP disconnects (Steam depot hash mismatch)
- SteamCMD can't batch upload with per-item PublishFileID — but "Success." per item works
- Steam Guard code needed once, then cached (even after re-enabling authenticator)
- Workshop updates not instant — must restart Steam to force sync
- Blank test sheet = untested, NOT working

---

# Session: 2026-03-26 (Part 3 — Testing + Fixes)

## What Was Done

### MP Testing (Session 2)
- User tested tools in real MP with dual Steam
- 2 mods confirmed working perfectly (Jackhammer, Tripmine)
- 2 working with minor issues (Thruster_Tool, VectorRazor)
- 20 mods "not in toolbar" — RegisterTool changes from earlier weren't published to Workshop yet
- ARM weapons: reload with R broken (operator precedence), no animation watching other player
- Light_Katana: massive model (raw vox instead of XML prefab with scale=0.1)
- FPV_Drone: too many issues, deferred

### Fixes Applied
- ARM_AK47/Glock/M4A4: fixed reload operator precedence
- Light_Katana_MP: changed prefab to Katana.xml (has scale=0.1)
- VectorRazor: added PlayersAdded loop for client tool enable
- Thruster_Tool: power capped at ±300
- ODM_Gear: added RegisterTool + server.init + PlayersAdded (was completely v1)
- Keybind standards doc created (docs/KEYBIND_STANDARDS.md)
- Interactive HTML test sheet with checkboxes, copy/paste, auto-save

### Publishing Issues
- SteamCMD batched uploads hang on large mods (>1MB content folders)
- Reverted to one-at-a-time uploads
- 20 mods with RegisterTool changes STILL NOT PUBLISHED to Workshop
- Publish script changed back to sequential mode

## Incomplete Work (CRITICAL)
- **20 mods not published to Workshop** — RegisterTool changes exist in working dir but never uploaded
  AC130, Asteroid_Strike, Black_Hole, Bunker_Buster, C4, Charge_Shotgun (DEF),
  CnC_Weather_Machine, Desert_Eagle, Exploding_Star, Fire_Fighter, High_Tech_Drone,
  Hook_Shotgun, Laser_Cutter, Light_Saber, Molotov_Cocktail, Multiple_Grenade_Launcher,
  ODM_Gear, Predator_Missile, Rods_from_Gods
- **ARM animation sync** — no animation/effects visible when watching other player use ARM weapons
- **FPV_Drone_Tool** — too many issues, needs dedicated investigation
- **Light_Katana terrain damage** — player damage works but no terrain/building damage
- **Light_Katana Q dash** — does nothing
- Maps, vehicles, utilities not yet tested
- Publish script needs reliability improvement (batched hangs, sequential is slow)

## Next Steps
1. **Run update.bat** to publish the 20+ mods with RegisterTool changes (sequential mode now)
2. Re-test the 20 mods that were missing from toolbar
3. Fix ARM animation sync issue (custom animation framework not syncing to other players)
4. Investigate FPV_Drone issues
5. Test maps, vehicles, utilities
6. Fix Light_Katana terrain damage + Q dash

## Gotchas Discovered
- SteamCMD batched uploads hang on large content folders — must use sequential
- Publish script only detects changes vs Workshop cache — if you add RegisterTool AFTER a publish, must run update.bat again
- RegisterTool 4th param is toolbar group (1-6), NOT model scale
- XML prefabs can have scale attributes — raw .vox files don't. Katana.vox is 10x too large without Katana.xml's scale=0.1
- Lua operator precedence: `A and B or C and D` evaluates as `(A and B) or (C and D)` — must parenthesize
- SetToolEnabled(ID, true) without player param only enables for host
- Charge_Shotgun uses DEF framework (RegisterTool handled internally by def.lua)
- ODM_Gear had bare init() function despite #version 2 — silently broken in MP
