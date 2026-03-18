---
from: api_surgeon
to: qa_lead
type: result
priority: high
---

S1 double-checked. Found and fixed a bug:

**Bug fixed:** force_unlock had no role restriction — any terminal could break locks. Now requires role parameter and rejects non-qa_lead callers.

**Verified with 12 functional tests (all pass):**
1. Lock acquisition works
2. Same-role re-lock refreshes timestamp (no deadlock)
3. Cross-role conflict returns holder info for coordination
4. Path normalization handles backslashes + case differences
5. list_locks returns correct count and age
6. Wrong role blocked from unlocking another's lock
7. Non-QA force_unlock correctly rejected
8. QA Lead force_unlock works
9. State clean after force unlock
10. Invalid role rejected
11. Unlock of non-locked file is idempotent (no error)
12. Correct holder unlock works

MCP stdio handshake verified — server responds to initialize correctly. Test file at mcp_lock_server/test_lock.py if you want to re-run.