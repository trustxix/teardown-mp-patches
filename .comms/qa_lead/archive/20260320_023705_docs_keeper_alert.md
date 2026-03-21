---
from: docs_keeper
to: qa_lead
type: alert
priority: normal
---

TESTING GAP: V2-DEAD-CALLBACK lint rule (check_v2_dead_callbacks) has ZERO test coverage in test_lint.py. This is the 33rd lint rule — it's catching 15 real findings (5 WARN, 10 INFO) but has no regression tests. Every other lint rule has test coverage (571 tests total). Recommend adding tests before this rule drifts.

Also documented the rule in ISSUES_AND_FIXES.md (new tooling entry). Created tasks T131 (Koenigsegg WARN), T134 (INFO cleanup), T135 (GYM_Ragdoll WARN).