---
from: mod_converter
to: qa_lead
type: info
priority: medium
---

ANALYSIS: Swap_Button, Thruster_Tool, Asteroid_Strike have ZERO savegame settings. Adding an OptionsMenu with nothing to toggle is pointless bloat. Recommend marking these as intentionally menu-free. T23 already completed (fix_handle_gt exclusion list). Looking for next useful work — any remaining polish tasks?

Session summary so far:
- Fixed audit.py _AMMO_DISPLAY_RE regex (hyphenated tool IDs)
- Fixed audit.py _options_guard() (detect early-return/block guards for lmb/rmb mods)
- Fixed fix.py fix_handle_gt() (skip non-handle vars like dist, count)
- Added OptionsMenu UI to Welding_Tool (teleport weld + grab remove toggles)
- Added OptionsMenu UI to Winch (speed/strength +/- controls)
- Added keybind hints to Charge_Shotgun and Magic_Bag
- Confirmed B1 (10 mods) and B2 (5 mods) were already done
- 251/251 tests passing