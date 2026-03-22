# Current Team Focus

## Focus: Polish & Remaining Gaps
**Set by:** qa_lead
**Date:** 2026-03-22

### Current State (verified 2026-03-22)
- **102 mods** installed (19 added, 29 removed in 2026-03-21 sync; +1 Fire_Fighter_MP #72 fix)
- **0 tier-1 hard errors** across all 102 mods
- **100 PASS, 2 WARN, 0 FAIL** deepcheck
- **5 mods with game log compile errors** (GLARE, High_Tech_Drone, Spells, Thermite_Cannon, Winch)
- **10/53 gun mods** need AimInfo (mostly map entity scripts — may be @audit-ok)
- **1/52 tool mods** needs AmmoPickup
- **All 19 new mods triaged and tier-1 clean**

### WARN Mods
- **Robot_Vehicles** — missing SetToolEnabled/SetToolAmmo for z-glock18, z-m4a1
- **Voxel_Plaza** — entity script firing chain issues, missing SetToolEnabled for p90

### Priority (descending)
1. **Fix compile errors** (T265) — 5 mods non-functional in MP
2. **Fix deepcheck WARNs** (T266, T267) — Robot_Vehicles, Voxel_Plaza
3. **AimInfo conversions** (T268-T270) — 10 mods in 3 batches, investigate applicability
4. **User testing** — verify fixes in-game between batches

### Key Reminders
- Follow BASE_GAME_MP_PATTERNS for ALL conversions
- Read WHAT_WORKS and WHAT_DOESNT_WORK before fixing anything
- Follow Idle Protocol when queue empties
- Max 3 mods per batch
- Tools passing ≠ game works — only user in-game test is final word
