---
from: mod_converter
to: maintainer
type: info
priority: low
---

FINISHED: deepcheck.py false-positive cleanup — 3 categories of fixes: (1) options.lua shadow in HUD check, (2) auxiliary ServerCall targets in firing chain, (3) auxiliary ClientCall targets in effect chain + deduped servercall_targets. Batch results: 77→135 PASS, 101→43 WARN, 0 FAIL. All 545 pytest tests pass. The remaining 43 WARNs are all genuine "no ClientCall for remote effects" — cosmetic but real.