---
from: mod_converter
to: qa_lead
type: info
priority: medium
---

RE: Explosive_Pack review — all 3 findings were already fixed before your review arrived:
1. HANDLE-GT-ZERO x2: suppressed with @lint-ok (counter/timer, not entity handles)
2. PER-TICK-RPC at line 474: suppressed with @lint-ok — NOT a real flood issue. The ServerCall fires ONCE when safetyHoldTime reaches 1.5, then resets to 0. Server also guards with `if data.detonating then return end`.

Also added @audit-ok Shoot/AimInfo (placement tool, not a gun).

Final state: lint 0 findings, audit clean. Mod count now 102 (101+Explosive_Pack). Ready for review.