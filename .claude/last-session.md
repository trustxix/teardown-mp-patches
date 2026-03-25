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
