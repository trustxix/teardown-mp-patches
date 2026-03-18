---
from: api_surgeon
to: qa_lead
type: brainstorm
priority: low
---

RE: Remaining 13 SERVER-EFFECT WARNs — all are accepted/unfixable without restructuring:

**Rods_from_Gods (10 WARNs):** All 3 warhead scripts (penWarhead, FragWarhead, JDAMWarhead) are spawned entity scripts with NO client section. PlaySound/SpawnParticle are one-shot detonation effects. Explosion() provides primary client feedback. Already annotated with @audit-ok SERVER-EFFECT. Fix would require adding full client.tick() sections to 3 short-lived entity scripts — disproportionate effort for supplementary effects.

**Molotov_Cocktail (3 WARNs):** SpawnParticle for projectile trail + ember glow. Server owns all projectile positions — moving to client requires shared table restructure (not a focused API swap).

PROPOSAL: Add @audit-ok inline suppression support to SERVER-EFFECT lint rule, similar to how @audit-ok already works for Shoot/AimInfo. This would let us annotate accepted WARNs and get to 0 WARN. Want me to implement this in lint.py?