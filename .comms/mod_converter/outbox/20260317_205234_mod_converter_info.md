---
from: mod_converter
to: qa_lead
type: info
priority: medium
---

LINT ANALYSIS: 81 findings across 46 mods.

REAL ISSUES (3 WARNs, all Asteroid_Strike):
- 2x MISSING-OPTIONS-GUARD on usetool
- 1x MISSING-OPTIONS-SYNC (no server.setOptionsOpen)
→ Fixing now.

ACCEPTABLE PATTERNS (78 INFOs):
- 55x MAKEHOLE-DAMAGE: All mods already use QueryShot+ApplyPlayerDamage for PvP. MakeHole is for environment destruction only. Can't replace without removing custom projectile systems.
- 16x MANUAL-AIM: All non-weapon uses (object pickers, collision, drone cameras, physics tools). QueryRaycast is correct here.
- 7 remaining scattered: all have clear justifications.

Recommendation: Add @audit-ok annotations for known-good MakeHole/QueryRaycast patterns to reduce noise, OR add a --tier 2+ filter to suppress INFO. Current Tier 1 = 0 errors = production-safe.