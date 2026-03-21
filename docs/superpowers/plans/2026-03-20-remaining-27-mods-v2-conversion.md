# Remaining 27 Mods V2 Conversion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert all 27 remaining v1 mods to v2 multiplayer compatibility.

**Architecture:** Batch by complexity — SIMPLE mods get mechanical callback renames, MEDIUM mods need file-scope API deferral + callback split, COMPLEX mods need full server/client split with per-player state.

**Tech Stack:** Teardown Lua v2 API

---

## Batch 1: SIMPLE (5 mods, ~940 lines total)

Mechanical conversion — rename callbacks, add headers. No file-scope API issues.

### Task 1: Simple Callback Renames

**Mods:** Ability_to_read (29 lines), Colossus_Attack (181 lines), Micro_Metropolis (447 lines), The_World_Trade_Center (118 lines), New_York_mini (163 lines)

For each mod:
- [ ] Add `#version 2` + `#include "script/include/player.lua"` to main.lua
- [ ] Add `version = 2` to info.txt
- [ ] Rename `init()` → `server.init()`
- [ ] Rename `tick(dt)` → `client.tick(dt)` (these are map/content mods, mostly visual)
- [ ] Rename `draw()` → `client.draw()` if present
- [ ] Rename `update(dt)` → `client.update(dt)` if present
- [ ] For New_York_mini: defer file-scope `GetBool`/`SetFloat` calls to init
- [ ] Lint each mod
- [ ] Commit: `feat: convert 5 simple mods to v2`

---

## Batch 2: MEDIUM (4 mods, ~3,436 lines total)

Need file-scope API deferral + callback split.

### Task 2: Bikes, Ramps & Ragdolls (1,088 lines)
- [ ] Add v2 headers
- [ ] Split callbacks — server: vehicle physics. Client: visuals, input
- [ ] Lint + commit

### Task 3: Bridge Launcher System (143 lines)
- [ ] Add v2 headers
- [ ] Defer file-scope API calls
- [ ] Split callbacks
- [ ] Lint + commit

### Task 4: Tool Menu (456 lines)
- [ ] Add v2 headers
- [ ] Defer file-scope API calls (5 calls)
- [ ] Split callbacks — client-only (UI tool)
- [ ] Lint + commit

### Task 5: Miniature World (1,749 lines)
- [ ] Add v2 headers
- [ ] Defer file-scope API calls (29 calls)
- [ ] Split callbacks — server: vehicle/entity physics. Client: visuals
- [ ] Lint + commit

---

## Batch 3: COMPLEX Tools (3 mods, ~18,646 lines total)

Tools with custom mechanics needing full server/client split.

### Task 6: GLARE - Laser Weapon (6,344 lines)
- [ ] Add v2 headers
- [ ] Defer 53 file-scope API calls
- [ ] Split: server handles beam damage/MakeHole, client handles visuals/particles
- [ ] Convert RegisterTool to v2 pattern with PlayersAdded
- [ ] Add per-player state
- [ ] Apply UI standards
- [ ] Lint + commit

### Task 7: Thermite Cannon (4,804 lines)
- [ ] Add v2 headers (has UMF framework — may need UMF translation per docs/UMF_TRANSLATION_GUIDE.md)
- [ ] Defer 37 file-scope API calls
- [ ] Split: server handles damage, client handles stream visuals
- [ ] Convert RegisterTool
- [ ] Lint + commit

### Task 8: Centurion C-RAM (7,498 lines)
- [ ] Add v2 headers
- [ ] Defer 34 file-scope API calls
- [ ] Split: server handles turret AI/shooting, client handles visuals/sounds
- [ ] Sync turret state via shared table
- [ ] Lint + commit

---

## Batch 4: COMPLEX Vehicles & Aircraft (4 mods, ~64,314 lines total)

Large vehicle/aircraft mods with flight models, AI, weapons.

### Task 9: Active Volatile Aviation (7,949 lines)
- [ ] Add v2 headers
- [ ] Defer 58 file-scope API calls
- [ ] Split flight physics to server, cockpit UI/camera to client
- [ ] Lint + commit

### Task 10: Flying Planes (24,529 lines — UMF/TDSU framework)
- [ ] Add v2 headers
- [ ] This mod uses UMF/TDSU framework — follow docs/UMF_TRANSLATION_GUIDE.md
- [ ] Defer 60 file-scope API calls
- [ ] Split: server handles flight physics/weapons, client handles HUD/camera
- [ ] Convert UMF RegisterTool calls
- [ ] Lint + commit

### Task 11: Kooshing's Dynamic Aircraft (27,421 lines)
- [ ] Add v2 headers
- [ ] Defer 291 file-scope API calls (MASSIVE — many in entity scripts)
- [ ] Split flight model, weapons, AI to server; cockpit, camera, effects to client
- [ ] Entity scripts need individual #version 2 + v2 callbacks
- [ ] Lint + commit

### Task 12: AndRe's BMW E36 (4,415 lines)
- [ ] Add v2 headers
- [ ] Defer 67 file-scope API calls
- [ ] Split: server handles vehicle physics, client handles lights/wipers/radio
- [ ] Lint + commit

---

## Batch 5: COMPLEX Maps (5 mods, ~37,471 lines total)

Maps with scripted content (NPCs, elevators, systems).

### Task 13: Bright Valley Correctional Center (20,625 lines)
- [ ] Add v2 headers
- [ ] Defer 210 file-scope API calls
- [ ] Split: server handles NPC AI/gates/elevators, client handles sounds/visuals
- [ ] Entity scripts need individual conversion
- [ ] Lint + commit

### Task 14: Vida Hospital (13,986 lines)
- [ ] Add v2 headers
- [ ] Defer 1,003 file-scope API calls (!!!)
- [ ] Split: server handles doors/elevators/electrical, client handles lights/sounds
- [ ] Lint + commit

### Task 15: Russian Town 6 (2,309 lines)
- [ ] Add v2 headers
- [ ] Defer 25 file-scope API calls
- [ ] Split map scripts
- [ ] Lint + commit

### Task 16: New York mini — already in Batch 1

### Task 17: World Trade Center — already in Batch 1

---

## Batch 6: COMPLEX NPC/AI Systems (5 mods, ~173,835 lines total)

Massive AI systems — most complex conversions.

### Task 18: Modern Soldier NPCs (100,611 lines)
- [ ] Add v2 headers
- [ ] Defer 490 file-scope API calls
- [ ] NPC AI runs on server, visual effects on client
- [ ] 49 NPC variant files — mostly copy-paste, batch conversion
- [ ] Lint + commit

### Task 19: Steve's NPCs (14,828 lines)
- [ ] Add v2 headers
- [ ] Defer 100 file-scope API calls
- [ ] Split AI to server, visuals to client
- [ ] Lint + commit

### Task 20: STAR WARS AI Pack (25,695 lines)
- [ ] Add v2 headers
- [ ] Defer 198 file-scope API calls
- [ ] AT-ST/TIE fighter AI to server, effects to client
- [ ] Lint + commit

### Task 21: SW's Advanced Gore Mod (13,590 lines)
- [ ] Add v2 headers
- [ ] Defer 80 file-scope API calls
- [ ] Gore system: server handles ragdoll physics, client handles blood FX
- [ ] Embedded AVF code needs conversion too
- [ ] Lint + commit

### Task 22: Synthetic Swarm (18,111 lines)
- [ ] Add v2 headers
- [ ] Defer 64 file-scope API calls
- [ ] Drone AI to server, visual effects to client
- [ ] Convert UMF RegisterTool
- [ ] Lint + commit

---

## Batch 7: COMPLEX Misc (4 mods, ~16,882 lines total)

### Task 23: AVF Vehicles (9,895 lines)
- [ ] Add v2 headers
- [ ] Defer 25 file-scope API calls
- [ ] Vehicle spawning/weapons to server, visuals to client
- [ ] Lint + commit

### Task 24: EVF Emergency Vehicles (6,491 lines)
- [ ] Add v2 headers
- [ ] Defer 142 file-scope API calls
- [ ] Lights/sirens to client, vehicle physics to server
- [ ] Lint + commit

### Task 25: Robot Vehicles (20,751 lines)
- [ ] Add v2 headers
- [ ] Defer 110 file-scope API calls
- [ ] Robot AI to server, cameras/visuals to client
- [ ] Convert UMF RegisterTool
- [ ] Lint + commit

### Task 26: Colossus Attack — already in Batch 1

---

## Estimated Effort

| Batch | Mods | Lines | Effort |
|-------|------|-------|--------|
| 1. Simple | 5 | 940 | 30 min |
| 2. Medium | 4 | 3,436 | 1-2 hours |
| 3. Complex Tools | 3 | 18,646 | 3-4 hours |
| 4. Complex Vehicles | 4 | 64,314 | 6-8 hours |
| 5. Complex Maps | 3 | 36,920 | 4-6 hours |
| 6. Complex NPC/AI | 5 | 173,835 | 8-12 hours |
| 7. Complex Misc | 3 | 37,137 | 4-6 hours |
| **Total** | **27** | **~335,228** | **~30-40 hours** |

---

## Priority Order

1. **Batch 1 (Simple)** — quick wins, 5 mods working in MP in 30 min
2. **Batch 2 (Medium)** — Tool Menu is useful, Miniature World is fun
3. **Batch 3 (Complex Tools)** — GLARE and Thermite Cannon add weapon variety
4. **Batch 5 (Complex Maps)** — Russian Town 6 is MP-tagged, should work in MP
5. **Batch 4 (Complex Vehicles)** — planes/helicopters add gameplay
6. **Batch 7 (Complex Misc)** — vehicles and robots
7. **Batch 6 (Complex NPC/AI)** — massive effort, lowest priority for MP (AI is typically single-player)
