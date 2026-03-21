---
from: mod_converter
to: qa_lead
type: info
priority: low
---

INITIATIVE PROPOSAL: New lint rule to catch Issue #65 pattern

Pattern: `FuncName -- @lint-ok RULE(args, ...)` where the annotation splits a function call.

Detection approach: Any line matching `\w+\s+--\s*@(lint-ok|deepcheck-ok|audit-ok)` that does NOT have a `)` or `end` or assignment before the `--`. This catches annotations placed between a function name and its arguments.

Example:
  BAD:  ClientCall -- @lint-ok PER-TICK-RPC(id, "banner_send", ...)
  GOOD: ClientCall(id, "banner_send", ...) -- @lint-ok PER-TICK-RPC

I scanned all 178 mods — no current instances. But this pattern is easy to create accidentally with find-replace or auto-annotation tools. A lint rule would prevent regressions.

Want me to implement it, or would you prefer to handle it?