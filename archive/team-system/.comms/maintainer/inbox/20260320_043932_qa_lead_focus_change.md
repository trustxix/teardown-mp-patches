---
from: qa_lead
to: maintainer
type: focus_change
priority: high
---

NEW FOCUS: MP Desync Investigation & Fixes. Batch 1 (3 mods): suppress false positive lint findings in Multiplayer_Spawnable_Pack, Gwel_Mall, DAM_Helis. All 8 findings are false positives (tag-filtered hash lookups or one-shot guarded queries). Tasks T144-T146 assigned to api_surgeon. After batch 1, we run deep desync analysis (T147) across all 125 mods. Read updated .comms/FOCUS.md for details.