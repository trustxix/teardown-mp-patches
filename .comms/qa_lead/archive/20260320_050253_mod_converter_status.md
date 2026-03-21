---
from: mod_converter
to: qa_lead
type: status
priority: normal
---

OPTIONS.LUA V2 CONVERSION — Batch 1 of 3 COMPLETE

Changed 3 files (options.lua only, main.lua untouched):
- Desert_Eagle/options.lua: lines 1-6 (added #version 2 header, renamed init→client.init, draw→client.draw)
- GYM_Ragdoll/options.lua: lines 1-13 (same pattern)
- Multiple_Grenade_Launcher/options.lua: lines 1-10 (same pattern)

Results:
- Desert_Eagle: lint clean, deepcheck PASS
- GYM_Ragdoll: lint clean, deepcheck PASS
- Multiple_Grenade_Launcher: lint clean, deepcheck PASS

These mods' Mod Manager settings pages will now load in MP sessions. 6 more options.lua files remain for future batches (T158).

Ready for user to test. Recommend launching game and checking Mod Manager → Desert Eagle/GYM Ragdoll/MGL settings pages work.