---
from: api_surgeon
to: qa_lead
type: result
priority: high
---

Completed API upgrade audit of all 48 mods. Key finding: 26/29 "missing Shoot()" flags were FALSE POSITIVES — these mods already use QueryShot+ApplyPlayerDamage (the projectile-weapon equivalent). The audit tool only checks for literal `Shoot(` string.

4 mods actually needed and received QueryShot+ApplyPlayerDamage upgrades:
- Dragonslayer (melee sword): QueryShot on swing path, radius 1.0
- HADOUKEN (energy ball): QueryShot on projectile movement path, radius 0.5
- Revengeance_Katana (slash beam): QueryShot on both slash arms with per-slash hit tracking
- Scorpion (punch/hook): QueryShot on punch and hook projectile

All 49 mods pass tier 1 lint. MakeHole retained where appropriate for voxel damage. Recommend testing these 4 mods in PvP to verify damage registration.