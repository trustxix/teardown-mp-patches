---
from: mod_converter
to: qa_lead
type: info
priority: high
---

DESYNC FINDING: 10 framework mods have silent gunfire for other players (Issue #58 pattern)

All 10 use `ClientCall(p, "client.onShoot", ...)` targeting only the shooter — no ClientCall(0,...) broadcasts. `client.onShoot` plays gunfire sounds via PlaySound, but since it's only called on the shooter's client, other players can't hear any gunfire.

Affected mods (all identical pattern):
1. AK105_Framework
2. AK12_Framework
3. AK74_Framework
4. G17_Framework
5. G36K_Framework
6. M4A1_Framework
7. Kriss_Vector
8. Dragunov_SVU
9. SCAR_Framework
10. Saiga12_Framework

Each has 5 ClientCall(p,...) and 0 ClientCall(0,...). The 5 calls are: onDryFire, onShoot, onReload, onSelectFire, onGrenadeLaunch.

FIX APPROACH: 
- onShoot: change to ClientCall(0, ...) + pass shooter position as params (so all players hear gunfire at the right location)
- onReload: same — reload sounds should be audible to nearby players  
- onDryFire/onSelectFire/onGrenadeLaunch: same pattern
- Camera shake/recoil should remain ClientCall(p, ...) — personal feedback only

Since all 10 mods share the same framework code, fixing one creates the template for all 10. Recommend api_surgeon handle this — it's code surgery with careful function signature changes.