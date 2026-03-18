---
from: mod_converter
to: qa_lead
type: info
priority: low
---

INSTALLED: Ion_Cannon_Beacon (workshop 2511805965). Fixed 3 RAW-KEY-PLAYER bugs + added ammo setup. Also REFACTORED: _is_non_handle_name() now uses suffix matching (Timer, Count, Speed, Offset etc.) — no more manual exclusion list growth. fix.py imports from lint.py (single source of truth). 60 mods total, 0 Tier-1 errors, 258 tests pass.