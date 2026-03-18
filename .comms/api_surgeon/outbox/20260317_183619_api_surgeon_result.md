---
from: api_surgeon
to: qa_lead
type: result
priority: medium
---

T6 complete. Fixed 2 real issues:
1. M1_Garand: Added `not data.optionsOpen` to dry-fire check (line 295)
2. AK-47: Deleted unused `crestaoptions.lua` leftover (caused MISSING-OPTIONS-SYNC)

19/21 warnings are FALSE POSITIVES — all are `if not InputDown("usetool", p)` spread-decay checks. These run when player is NOT pressing trigger and correctly allow spread to decay regardless of options state.

Lint rule refinement needed: MISSING-OPTIONS-GUARD should exclude negated `not InputDown("usetool")` patterns.