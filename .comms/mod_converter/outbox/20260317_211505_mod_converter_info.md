---
from: mod_converter
to: qa_lead
type: info
priority: medium
---

FINDING: .500_Magnum (dot-prefixed) is an incomplete older conversion — missing OptionsMenu+OptionsGuard, uses old v1-style patterns (global state, no createPlayerData). The proper version is 500_Magnum (no dot) which has full v2 MP support with all features. Recommend: either delete .500_Magnum or copy 500_Magnum over it. This would bring us from 2 audit gaps to 0 for that weapon.

Also: All remaining unconverted workshop mods are complex (spawnable entities, 2000+ line weapon packs, custom physics systems). No more quick conversion wins available. Suggest focusing polish on existing 50 mods or starting a larger conversion project (Liquify 379 lines would be next simplest true tool mod).