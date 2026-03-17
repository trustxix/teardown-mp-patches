# Task Queue — Managed by QA Lead

> Other terminals: pick up tasks assigned to your role, mark them `IN PROGRESS` with your terminal name, and `DONE` when complete. Run `python -m tools.lint --mod "ModName"` after every edit.

---

## Terminal 1 (API Surgeon) — Queue

### Task A1: MISSING-TOOL-AMMO (6 mods) — Priority: HIGH
**Status:** DONE
Added `SetToolAmmo("toolid", 101, p)` in PlayersAdded for: Dragonslayer, Dual_Miniguns, HADOUKEN, Lightkatana, Minigun, Vacuum_Cleaner. All linted clean.

### Task A2: MISSING-AMMO-PICKUP (.500_Magnum) — Priority: HIGH
**Status:** DONE
Added `SetToolAmmoPickupAmount("500magnum", 5)` to `.500_Magnum/main.lua` server.init().

### Task A3: MANUAL-AIM migration (16 mods) — Priority: MEDIUM
**Status:** DONE
Migrated 3 weapon mods to GetPlayerAimInfo:
- [x] Airstrike_Arsenal — client fire designator aim
- [x] Lava_Gun — server beam + client beam visual
- [x] Lightning_Gun — server beam + client beam visual
Analyzed remaining 13 — no manual aim patterns to swap:
- [x] AC130_Airstrike_MP — plane camera aim, not player aim
- [x] Acid_Gun — particle physics launch, not aim
- [x] Asteroid_Strike — orbital strike raycast, not weapon aim
- [x] Bee_Gun — projectile launch direction, not aim
- [x] C4 — 4m placement raycast, not weapon aim
- [x] Charge_Shotgun — recoil direction, not aim
- [x] High_Tech_Drone — drone camera aim, not player aim
- [x] Holy_Grenade — grenade bounce physics, not aim
- [x] Lightsaber — melee arc raycasts, not aim
- [x] Magic_Bag — object picker raycast, not weapon aim
- [x] Multiple_Grenade_Launcher — grenade launch physics, not aim
- [x] Thruster_Tool — physics tool raycast, not weapon aim
- [x] Vacuum_Cleaner — suction direction, not weapon aim

### Task A4: Player damage migration (29 gun mods) — Priority: LOW
**Status:** DONE (via QueryShot pattern)
All gun mods already have player damage via `QueryShot + ApplyPlayerDamage` (applied in prior session). The audit shows Shoot=X because it checks for literal `Shoot()` calls, but `QueryShot` is the correct API for projectile-based guns with custom physics (travel time, gravity, penetration). Using `Shoot()` (hitscan) would require removing each mod's projectile system — that's restructuring, which the role forbids.
Mods with player damage enabled: 500_Magnum, AK-47, AWP, Bee_Gun, Charge_Shotgun, Desert_Eagle, Dual_Berettas, Dual_Miniguns, Exploding_Star, Guided_Missile, Hook_Shotgun, Laser_Cutter, Lava_Gun, Lightkatana, Lightning_Gun, Lightsaber, M1_Garand, M249, M2A1_Flamethrower, M4A1, Minigun, Nova_Shotgun, P90, SCAR-20, SG553, AC130_Airstrike_MP, Attack_Drone, Scorpion

---

## Terminal 2 (Mod Converter) — Queue

### Task B1: MISSING-KEYBIND-HINTS (9 mods) — Priority: MEDIUM
**Status:** OPEN
Add keybind hint text in `client.draw()` showing controls. Follow AWP/Dual_Berettas pattern:
```lua
UiPush()
UiTranslate(10, UiHeight() - 100)
UiAlign("left bottom")
UiColor(1, 1, 1, 0.8)
UiFont("bold.ttf", 20)
UiTextOutline(0, 0, 0, 1, 0.1)
UiText("LMB - Fire\nR - Reload\nO - Options")
UiPop()
```
Mods needing hints (check each mod's actual keybinds first):
- [ ] 500_Magnum
- [ ] AK-47
- [ ] C4
- [ ] Desert_Eagle
- [ ] M249
- [ ] M4A1
- [ ] Nova_Shotgun
- [ ] SCAR-20
- [ ] SG553
- [ ] Thruster_Tool

---

## QA Lead — Active

### Task Q1: MISSING-OPTIONS-SYNC (5 mods) — Priority: HIGH
**Status:** DONE
All 5 mods fixed: Lava_Gun, Lightning_Gun, M2A1_Flamethrower, Welding_Tool, Winch.
Added server.setOptionsOpen() + usetool guards. All lint clean.

### Task Q2: Rich-settings options menus (7 mods) — Priority: MEDIUM
**Status:** DONE
All 7 mods complete:
- [x] C4 (explosionSize +/- buttons + timer delay cycle)
- [x] High_Tech_Drone (already had full settings panel, added server sync + usetool guards)
- [x] Vacuum_Cleaner (already had slider UI, added server sync + O-key + usetool guards)
- [x] AC130_Airstrike_MP (nocd toggle)
- [x] Lava_Gun (fireamount big/small toggle)
- [x] Multiple_Grenade_Launcher (3 toggles: unlimitedammo, norecoil, noreticle)
- [x] Revengeance_Katana (OptionsGuard added)

---

## Completed Tasks

- **A1** MISSING-TOOL-AMMO — 6 mods fixed (Dragonslayer, Dual_Miniguns, HADOUKEN, Lightkatana, Minigun, Vacuum_Cleaner)
- **A2** MISSING-AMMO-PICKUP — .500_Magnum fixed
- **A3** MANUAL-AIM — 3 weapon mods migrated (Airstrike_Arsenal, Lava_Gun, Lightning_Gun); 13 analyzed as non-applicable
- **A4** Player damage — 28 gun mods have QueryShot+ApplyPlayerDamage for PvP damage
