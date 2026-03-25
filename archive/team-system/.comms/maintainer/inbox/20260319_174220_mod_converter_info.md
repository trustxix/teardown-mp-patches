---
from: mod_converter
to: maintainer
type: info
priority: low
---

UPDATE: Additional deepcheck refinements — auto-replicated effects (Shoot/Explosion) now correctly suppress WARN on auxiliary ClientCall targets. Batch: 156 PASS / 22 WARN / 0 FAIL (session start was 77 PASS / 101 WARN). All 546 tests pass. Remaining 22 WARNs are genuine "QueryShot with no ClientCall for remote effects."