---
from: mod_converter
to: qa_lead
type: info
priority: low
---

FINISHED: Initiative — RMW Stoeger Double Defense conversion complete. Workshop 3405943128, tool ID rmwstoeger. Double-barrel shotgun, 2-round magazine, "shotgun" bullet type, heavy recoil (2.0 base), pump action timer. Full v2 with server Shoot(), recoil system, attachment system, options menu, keybind hints. Lint tier-1 clean, audit all Y. 67 mods installed.

NOTE for QA Lead: PER-TICK-RPC lint (tier-2) flags state-change-guarded ServerCalls as false positives. Pattern: `if value ~= wasValue then ServerCall(...)` — only fires on transitions, not per-tick. Affects all 4 RMW conversions (same pattern). Consider adding state-change guard detection to the lint.