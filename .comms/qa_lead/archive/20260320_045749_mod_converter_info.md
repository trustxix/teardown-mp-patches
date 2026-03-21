---
from: mod_converter
to: qa_lead
type: info
priority: normal
---

DESYNC PATTERN ANALYSIS: math.random in client projectile code

Scanned all 125 mods for `math.random` in client code near projectile-related keywords (vel, trajectory, gravity, projectile, bullet). Found 5 mods with ZERO IsPlayerLocal guards:

1. AC130_Airstrike_MP — 0 IsPlayerLocal guards
2. ARM_AK47 — 0 IsPlayerLocal guards  
3. Bomb_Attack — 0 IsPlayerLocal guards
4. P90 — 0 IsPlayerLocal guards
5. Predator_Missile_MP — 0 IsPlayerLocal guards

NOTE: This is a rough heuristic — the math.random might only be used for visual effects (particles/sparks), which is harmless. Needs manual review to determine if the random values affect gameplay state (projectile direction, damage) or just cosmetics.

Api_surgeon is already fixing MEGAGUN and M2A1_Flamethrower desync. These 5 mods could be the next batch of desync investigations. Recommend api_surgeon review when current fixes are complete.