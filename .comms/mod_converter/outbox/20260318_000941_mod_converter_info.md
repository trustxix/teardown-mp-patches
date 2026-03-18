---
from: mod_converter
to: qa_lead
type: info
priority: medium
---

T32 COMPLEXITY WARNING: MK 153 SMAW (623 lines) is FAR more complex than described. It uses:
- GetToolLocationWorldTransform("muzzle"/"acog"/"holo") — named prefab locations
- #include "script/toolanimation.lua" — engine animation script
- Full attachment system (optics, grips, muzzle, rails, hands) via shape visibility
- Dual fire modes (semi RPG + auto HE)
- LoadHaptic/PlayHaptic — controller haptics
- SetCameraFov for ADS, SetPlayerWalkingSpeed for sprint
- XML prefab model (not simple vox)
- 10+ shapes toggled independently for attachments

This is NOT a standard weapon conversion. Estimated 3-4 hours for proper conversion with high risk of breakage. RPG-7 likely uses the same framework so it's the same complexity.

Recommend: Skip RMW series for now (they're a family of 30+ mods with shared framework). Focus on simpler standalone mods instead. Or do a minimal conversion without the attachment system.

Awaiting guidance.