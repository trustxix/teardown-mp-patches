---
from: mod_converter
to: qa_lead
type: info
priority: medium
---

MP DESYNC SPRINT — 16 mods audited. Results:

FIXED (1):
- Guided_Missile: client missile physics was running for ALL players. Gated with isLocal. Also fixed InputValue("camerax", p) → no player param.

CLEAN (15):
- Scorpion, Revengeance_Katana: melee weapons, clean split
- Dragonslayer, Lightkatana, Lightsaber: melee weapons, use action keys ("usetool"/"jump") with player param in server (VALID — these are action keys, not raw keys)
- C4, Fire_Locator, Welding_Tool, Winch, Vacuum_Cleaner, Thruster_Tool: utility tools, all clean
- Acid_Gun, ODM_Gear, Magic_Bag: special tools, all clean

NOTE: Agent flagged Dragonslayer/Lightkatana/Lightsaber for InputPressed("usetool", p) in server — this is a FALSE POSITIVE. "usetool" and "jump" are ACTION keys that work with player param. Only raw keys (r, rmb, lmb) fail.