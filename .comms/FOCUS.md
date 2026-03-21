# Current Team Focus

## Focus: Lint Cleanup — 38 Findings Across 11 New/Deferred Mods
**Set by:** QA Lead
**Date:** 2026-03-21

### Background
Previous session left 125 mods with 0 lint findings. Since then, 6 new workshop mods appeared + 5 deferred/duplicate mods still installed = 11 mods with 38 tier-1 findings. **No patches were lost** — all 11 are new or previously-known deferred mods. Current installed count: 112.

### The 38 Findings Breakdown
- **15 MISSING-VERSION2** in framework/library files (UMF, TDSU, mplib, LnL) — FALSE POSITIVES, need @lint-ok-file
- **10 RAW-KEY-PLAYER** — real bugs in 4 mods (Light_Saber, Portal_Gun_MP, Thruster_Tool_Multiplayer, WIP_GYM)
- **5 MOUSEDX** — real bugs in Light_Saber (main.lua + backup copy)
- **4 DRAW-NOT-CLIENT** — real bugs in 2 mods (SVERLOVSK_TOWN_2, WIP_GYM backup files)
- **4 MISSING-VERSION2** in non-framework files (Light_Saber backup, WIP_GYM backup)

### Batch Plan

**Batch 1: Suppress framework false positives (3 mods)**
- Flying_Planes: @lint-ok-file on TDSU/umf.lua, TDSU/util_tool.lua
- GLARE: @lint-ok-file on libs/LnL.lua
- Robot_Vehicles: @lint-ok-file on custom_robot/scripts/umf.lua, zombieMod/scripts/zombieController.lua
Assigned: qa_lead (trivial annotations)

**Batch 2: More suppressions (3 mods)**
- Synthetic_Swarm: @lint-ok-file on scripts/umf.lua
- Thermite_Cannon: @lint-ok-file on umf/extension/tool_loader.lua
- MP_Hide_Multiplayer_Names: @lint-ok-file on 6 mplib/*.lua files
Assigned: qa_lead (trivial annotations)

**Batch 3: Cleanup backup files + entity fix (3 mods)**
- WIP_GYM_Ragdoll_Framework_MP: Delete backup .lua files (8 gore + 3 main versions)
- Light_Saber: Delete main - Copy.lua + Preview.jpg
- SVERLOVSK_TOWN_2_Multiplayer: Fix tv.lua draw()→client.draw()
Assigned: qa_lead (cleanup + trivial fix)

**Batch 4: Real bug fixes — NEEDS USER APPROVAL**
- Light_Saber: Fix 5 RAW-KEY-PLAYER + 3 MOUSEDX in main.lua
- Portal_Gun_MP: Fix 1 RAW-KEY-PLAYER
- Thruster_Tool_Multiplayer: Fix 2 RAW-KEY-PLAYER
Assigned: api_surgeon (code changes)

### New Mod Decisions
| Mod | Workshop ID | Lines | Decision |
|-----|-------------|-------|----------|
| Flying_Planes | 2423986361 | 24,565 | DEFER — TDSU framework, vehicle/map |
| Light_Saber | 3686903220 | 3,517 | PATCH — tool mod, fixable bugs |
| MP_Hide_Multiplayer_Names | 3684710351 | 5,688 | SUPPRESS — mplib FPs, mod works |
| Robot_Vehicles | 2673451391 | 20,805 | DEFER — UMF, vehicles |
| SVERLOVSK_TOWN_2_Multiplayer | 3684105073 | 1,903 | FIX — map, 1 entity script |
| WIP_GYM_Ragdoll_Framework_MP | 3681634144 | 5,802 | CLEANUP — backup files, then assess |
