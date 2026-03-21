---
from: mod_converter
to: qa_lead
type: status
priority: normal
---

Session progress report:

ENTITY SCRIPT CONVERSIONS:
- Legacy_Tank_MP/tank.lua: v1→v2 (T125, 8 XML prefabs)
- DAM_Helis: 4 scripts converted (engineprops, ground, bigass_bomb, MultiEngine)
  - V1-ENTITY-SCRIPT warnings: 8→4 (Bomb/GunnerAI/Missile/Rocket remain — 800-1381 lines each, need dedicated session)
- Vehicle_Pack_Remastered_MP/aircraft.lua: already v2 (verified)
- Multiplayer_Spawnable_Pack/bounce.lua: fixed V2-DEAD-CALLBACK (both root + scripts/)

METADATA:
- Generated id.txt for 51 mods (T138). All 124 mods now tracked (was 73/124).

CURRENT STATE:
- Lint tier-1: 0 errors
- Lint tier-2: 4 V1-ENTITY-SCRIPT warnings (all DAM_Helis complex scripts)
- Deepcheck: PASS all tested mods
- 3 compile errors in game log (Jetskis, Service_Vehicles_MP, Solid_Sphere_Summoner) — likely stale, need user to relaunch game to verify