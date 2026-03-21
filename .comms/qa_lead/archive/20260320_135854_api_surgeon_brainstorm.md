---
from: api_surgeon
to: qa_lead
type: brainstorm
priority: high
---

SYSTEMIC BUG FOUND: Host double-processing of scalar fields (Rule 42 class)

T157/T163/T164 fixed projectile tables and scalar fields in M2A1_Flamethrower and MEGAGUN. But a full codebase scan reveals **38 more mods** with the same bug — both server.tickPlayer and client.tickPlayer modify the same scalar data fields via per-frame arithmetic (data.X = data.X +/- dt).

On host, shared players[p] means all these fields are modified TWICE per frame:
- Timers count down 2x faster (reloadTimer, shootTimer, cooldownTimer)
- Ammo drains 2x faster
- Spread/heat/charge accumulates 2x faster

HIGH SEVERITY (multiple fields, 18 mods): AK-47, AWP, Airstrike_Arsenal, ARM_AK47, ARM_Glock, ARM_M4A4, Desert_Eagle, Hook_Shotgun, M1_Garand, M249, M4A1, Minigun, Mjolner, Multiple_Grenade_Launcher, Multi_Grenade_Launcher, Nova_Shotgun, P90, SCAR-20

MEDIUM SEVERITY (1-2 fields, 20 mods): 9 framework mods (all just data.meleeTimer), Acid_Gun, Attack_Drone, Dual_Berettas, Exploding_Star, High_Tech_Drone, Lightning_Gun, Lightsaber, Magic_Bag, Revengeance_Katana, Scorpion, Charge_Shotgun

FIX PATTERN (proven on M2A1+MEGAGUN): Add `local localP = GetLocalPlayer(); local isHostClient = localP and IsPlayerHost(localP)` at top of client.tickPlayer, then wrap continuous state modifications with `if not isHostClient then ... end`. Visual reads and client-only effects stay ungated.

RECOMMENDATION: This needs a multi-batch pass. The fix is mechanical and safe — same pattern for every mod. Suggest batches of 3 mods, prioritizing high-severity first. Could also consider adding an auto-fix to tools/fix.py for the pattern.

I've already fixed M2A1_Flamethrower (T163) and MEGAGUN (T164) this session = 2 mods. Can do 1 more in this batch then need user checkpoint.