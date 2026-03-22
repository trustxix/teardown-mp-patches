# Current Team Focus

## Focus: Workshop Sync Complete — Triage & Patch New Mods
**Set by:** User (via main terminal)
**Date:** 2026-03-21

### What Happened
Workshop sync performed by user: 29 unsubscribed mods removed, 19 newly subscribed mods copied in. Mod count: 112 → 101. All local mods now 1:1 match workshop subscriptions.

### Current State
- **101 mods** installed
- **173 tier-1 hard errors** — all from newly added unpatched mods
- **0 errors** on previously patched mods
- **10/53 gun mods** need AimInfo
- **2/52 tool mods** need AmmoPickup

### New Mods Added (19 — need triage)
| Folder Name | Workshop ID | Type | Notes |
|-------------|-------------|------|-------|
| Voxel_Plaza | 2430961153 | Map | |
| GTAV_Map | 2603154222 | Map | |
| Volkograd_Town_2_Remastered | 2984855900 | Map | |
| Volkotomsk_Town | 3024970462 | Map | |
| Twin_Towers | 3340357504 | Map | |
| Chebyrmansk_Town_MP | 3622439581 | Map | [MP] — may be v2 |
| Boeing_737_Full_MP | 3622995276 | Vehicle | [MP] — may be v2 |
| Russian_Town_5_Winter_MP | 3623099610 | Map | May be v2 |
| Hide_Gamertags_MP | 3624164337 | Utility | May be v2 |
| Fire_Fighter_MP | 3628141333 | Tool | version=2 in info.txt |
| DAM_MP_Optimized | 3634551685 | Map | MP Optimized |
| Performance_Mod | 3635399720 | Utility | May have no scripts |
| Rocket | 3656888075 | Tool | |
| SCP-3008 | 3661347086 | Map | |
| Armour_Framework_MP | 3662000095 | Vehicle | **173 lint errors** — biggest job |
| de_nuke_MP | 3669825346 | Map | [MP] |
| Russian_Town_3_4_MP | 3681169788 | Map | |
| Russian_Town_4_MP | 3685769925 | Map | |
| Russian_Town_5_MP | 3686055038 | Map | |

### Mods Removed (29)
AVF_Vehicles, Acid_Gun, Active_Volatile_Aviation, Adjustable_Fire, Advanced_Tornado, Airstrike_Arsenal, Bikes_Ramps_&_Ragdolls, Control, Dumb_Stupid_Fast_Cars, Dynamic_AT-AT_Map, EVF_International_Emergency_Vehicles, Final_Flash, Flying_Planes, Futuristic_Vehicle_pack, Geardown, Hurricanes_and_Blizzards, Kooshing's_Dynamic_Aircraft_Mod, Lava_Gun, Lightning_Gun, M249, Magic_Bag, Micro_Metropolis, Miniature_World, RPM_Playermodels, STAR_WARS_AI_PACK, SW's_ADVANCED_GORE_MOD_2, Steve's_NPCS, Synthetic_Swarm, WIP_GYM_Ragdoll_Framework_MP

### Priority
1. **Triage new mods** — which are already v2? which need conversion? which are content-only?
2. **Fix Armour_Framework_MP** — 173 tier-1 errors
3. **Patch remaining tools** — Rocket, Fire_Fighter_MP
4. **Maps** — likely minimal work (no tool scripts)

### Key Reminders
- Follow BASE_GAME_MP_PATTERNS for ALL conversions
- Read WHAT_WORKS and WHAT_DOESNT_WORK before fixing anything
- Follow Idle Protocol when queue empties
- Max 3 mods per batch
