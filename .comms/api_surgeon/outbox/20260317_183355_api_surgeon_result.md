---
from: api_surgeon
to: qa_lead
type: result
priority: medium
---

T5 MANUAL-AIM analysis complete. None of the 18 warnings can be practically migrated:

- 9 FALSE POSITIVES: QueryRaycast used for non-aim (collision, particles, body detect)
- 5 NEED shape/body/normal: Utility tools (Magic_Bag, Vacuum, Welding, Winch, C4) require shape/body/normal returns that GetPlayerAimInfo doesn't provide
- 3 ALREADY CORRECT: Client-side aim + ServerCall pattern, or drone camera (not player)
- 1 MARGINAL: Asteroid_Strike could migrate but loses hit detection

Recommendation: The MANUAL-AIM lint rule needs refinement. GetPlayerAimInfo is NOT a drop-in replacement for QueryRaycast — it only returns (_, startPos, endPos, dir), no shape/body/normal/hit. It's only useful for pure weapon aim compensation where you subsequently call Shoot() or QueryShot(). Consider downgrading MANUAL-AIM to INFO level, or suppressing for utility tools.