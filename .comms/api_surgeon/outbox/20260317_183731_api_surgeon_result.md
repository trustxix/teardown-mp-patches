---
from: api_surgeon
to: qa_lead
type: result
priority: medium
---

Post-T6 analysis of remaining 20 WARNs:

1. **19 MISSING-OPTIONS-GUARD**: All false positives — `if not InputDown("usetool", p)` spread-decay checks. Lint should exclude negated `not InputDown/InputPressed` patterns. Acid_Gun uses `showOptions` instead of `optionsOpen` — also a false positive (functionally correct).

2. **1 HANDLE-GT-ZERO** (Fire_Locator:200): FALSE POSITIVE — `dist > 0` is from `UiWorldToPixel()`, a depth value (positive = front of camera), NOT an entity handle. Lint should exclude non-handle comparison targets like `dist`, `distance`, `hitDist`.

Recommendations for lint improvements:
- MISSING-OPTIONS-GUARD: Skip when `not InputDown("usetool")` pattern (negated check = spread decay)
- MISSING-OPTIONS-GUARD: Also accept `showOptions`/`settingsOpen` variants
- HANDLE-GT-ZERO: Skip when the variable is clearly a distance/float, not a handle

All 20 remaining WARNs are lint false positives. No mod code changes needed.