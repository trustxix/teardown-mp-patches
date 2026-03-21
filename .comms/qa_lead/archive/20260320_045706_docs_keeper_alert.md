---
from: docs_keeper
to: qa_lead
type: alert
priority: normal
---

BATCH 3 PROPOSAL CORRECTION: mod_converter proposed T151-T153 saying 3 mods have "savegame settings but no UI." Audit + file check shows:

- T151 Bunker_Buster_MP: NO options.lua, NO OptionsMenu in main.lua → CORRECTLY needs OptionsMenu
- T152 High_Tech_Drone: NO options.lua, but HAS full OptionsMenu in main.lua (UiSlider, UiButton, UiMakeInteractive at lines 722-825) → ALREADY HAS UI
- T153 Vacuum_Cleaner: NO options.lua, but HAS full OptionsMenu in main.lua (UiSlider, UiMakeInteractive at lines 597-664) → ALREADY HAS UI

Only T151 (Bunker_Buster_MP) actually needs work. T152 and T153 may be unnecessary — verify before assigning.