# Multiplayer Testing Guide

Structured workflow for testing Teardown mods in real MP. Dual Steam via Sandboxie (see `docs/TESTING_SETUP.md`).

---

## Before You Start

1. Both Teardown installs synced: `python sync_installs.py --check` (should say ALL MATCH)
2. No game running: `tasklist | grep -i teardown`
3. Lint clean: `python -m tools.status` → 0 FAIL
4. Have `docs/MP_TEST_LOG.md` open to record results

## Testing Priority Order

Test highest-risk mods first. Priority based on: deep analysis result, mod type, and complexity.

### Tier 1 — Deep Analysis FAIL (test first, most likely broken)

These have known structural issues detected by semantic analysis.

| Mod | Type | Why It Failed | What to Watch For |
|-----|------|---------------|-------------------|
| Light_Saber | weapon | Effect chain FAIL | Sword swings not visible to other player |
| ODM_Gear | tool | Effect chain FAIL | Grapple hook visuals missing for others |
| DAM_MP_Optimized | vehicle | Effect chain FAIL | Aircraft explosion effects missing for non-host |
| Spawnable_Missiles_MP | weapon | Effect chain FAIL | Missile trails/explosions not visible |
| Chebyrmansk_Town_MP | map | Entity effects | Lights, sirens, radios not working |
| Russian_Town_5_MP | map | Entity effects | Vehicles, helicopters, turrets not working |
| Russian_Town_5_Winter_MP | map | Entity effects | Same as RT5 |
| Russian_Town_6_Summer_MP | map | Entity effects | Same as RT5 |
| SVERLOVSK_TOWN_2_MP | map | Entity effects | Lights, intercom, vehicles |
| Toyota_Supra_MP | map | Entity effects | Vehicle scripts |
| Jetskis | map | v1 content | Entity scripts may be disabled |
| quilezsecurity | map | Effect chain FAIL | Laser visuals not visible |

### Tier 2 — Deep Analysis WARN (likely works, minor issues)

| Mod | Type | Warning | What to Watch For |
|-----|------|---------|-------------------|
| Charge_Shotgun | weapon | No HUD guard | HUD showing when other tool equipped |
| minigun | weapon | Timer double-process | Firing rate different on host vs client |
| lasergun | weapon | No HUD guard | Beam visible to both players? |
| Jackhammer | tool | No HUD guard | Tool works for both players? |
| Fire_Fighter_MP | tool | No HUD guard | Water stream visible? |
| Tripmine | tool | No HUD guard | Tripmine laser beam visible? |
| islaestocastica | map | Effect warnings | Map entity scripts |

### Tier 3 — Deep Analysis PASS (should work, verify)

Prioritize tools/weapons over maps (tools have more desync surface area).

**Weapons (test in combat):**
AC130_Airstrike_MP, ARM_AK47, ARM_Glock, ARM_M4A4, Asteroid_Strike, Black_Hole, Bunker_Buster_MP, C4, CnC_Weather_Machine, Desert_Eagle, Exploding_Star, FPV_Drone_Tool, Hook_Shotgun, Laser_Cutter, Light_Katana_MP, Molotov_Cocktail, Multiple_Grenade_Launcher, Predator_Missile_MP, Rods_from_Gods, Thruster_Tool_Multiplayer, VectorRazor

**Utilities:** All_In_One_Utilities, Performance_Mod, Tool_Menu, Hide_Gamertags_MP, MP_Hide_Multiplayer_Names

**Maps:** Russian_Town_4_MP, gm_construct_MP, Haul_Truck_MP, and other content mods

---

## Per-Mod Test Procedure

### For Every Mod (30 seconds each)

1. **Host equips the tool/weapon**
2. **Client equips the same tool**
3. Check: Does the tool appear in both players' toolbars?
4. Check: Can both players switch to it?

### Weapon Mods (1-2 minutes each)

| Test | How | Pass If |
|------|-----|---------|
| **Fire** | Both players fire at terrain | Both see bullet holes/explosions |
| **Sound** | Listen from both perspectives | Both hear firing sounds with correct position |
| **Damage** | Shoot each other | Damage registers, kill feed shows correct weapon name |
| **Reload** | Press R (if applicable) | Reload animation plays for both perspectives |
| **Visual effects** | Fire and watch from other player | Muzzle flash, tracers, particles visible to other player |
| **Recoil** | Fire while watching other player's gun | Tool model doesn't float away or glitch |
| **Ammo HUD** | Check bottom of screen | Ammo count visible only when this tool is equipped |
| **Camera mods** | Enter special camera mode (AC-130, drone, missile) | Camera sensitivity feels natural, both players can control |

### Vehicle/Map Mods (2-3 minutes each)

| Test | How | Pass If |
|------|-----|---------|
| **Entity scripts** | Walk near interactive objects (radios, lights, doors) | They respond, sounds play, effects visible |
| **Vehicle entry** | Both players enter vehicles | Both can drive, vehicle syncs position |
| **Vehicle weapons** | Fire mounted weapons | Projectiles, sounds, damage work for both |
| **Map hazards** | Trigger any traps/hazards | Effects visible and damage applies to both |

### Utility Mods

| Test | How | Pass If |
|------|-----|---------|
| **All_In_One_Utilities** | Toggle fly, godmode, noclip | Works for client, not just host |
| **Tool_Menu** | Open menu, switch tools | All tools listed, switching works for both |
| **Performance_Mod** | Check FPS impact | No crash, no desync from optimization changes |

---

## What to Look For (Desync Symptoms)

### Visual Desync
- Other player's tool is invisible or stuck in T-pose
- Particles/explosions only visible to the shooter
- Tool model floating away from player's hands after shooting
- Camera stuck in wrong position after using a special mode

### Audio Desync
- No sound for other player when someone fires
- Sound plays at wrong position (world origin instead of gun)
- Looping sounds don't stop when they should

### Logic Desync
- Weapon fires for host but not for client (or vice versa)
- Damage only registers from one direction
- Kill feed shows wrong weapon name or "unknown"
- Ammo count different between host and client
- Timer-based effects run 2x speed on host (cooldowns, reloads)
- Tool abilities work with any tool equipped (not gated behind tool check)

### Crashes
- Game crashes when a specific mod is used
- Game crashes when player joins with mod active
- Engine error in log after specific action

---

## How to Report Results

After each mod test, tell me:

```
MOD: [name]
RESULT: WORKS / BROKEN / PARTIAL
SYMPTOMS: [what went wrong, from whose perspective]
STEPS: [what you did to trigger it]
```

I'll update `docs/MP_TEST_LOG.md` and if it's a code issue, fix it immediately.

### Quick shorthand:
- **WORKS** — fire, sound, damage, visuals all good from both perspectives
- **PARTIAL** — mostly works, one specific thing broken
- **BROKEN** — fundamental desync, crashes, or tool doesn't function

---

## Session Flow

```
1. Launch main Steam + Teardown
2. Launch sandboxed Steam + Teardown
3. Host creates lobby (main account)
4. Client joins (sandboxed account)
5. Load a sandbox map (Lee Chemicals or Marina for open space)

6. Test Tier 1 mods first (FAIL mods — 12 mods)
   → Report each result to me
   → I fix broken mods between tests if possible
   → Re-sync installs after fixes

7. Test Tier 2 mods (WARN mods — 7 mods)
   → Same flow

8. Test Tier 3 weapons (21 mods)
   → Can batch these faster — equip, fire, check both perspectives

9. Test Tier 3 utilities (5 mods)
10. Test Tier 3 maps (load each, check entity scripts)

11. After all testing:
    → python -m tools.logparse (check for errors in game log)
    → Report any issues not caught during play
```

---

## DEF Framework Tracking

During testing, note which mods would benefit from DEF conversion:

| Signal | Action |
|--------|--------|
| Mod has desync that separate server/client state would fix | Flag for DEF conversion |
| Mod has inline damage code that desyncs | Flag for ballistics framework |
| Mod works perfectly with manual v2 code | Low priority for DEF |
| Entity script works but effects missing for non-host | Flag for client-side effect refactor |

After testing, we update:
- `docs/MP_TEST_LOG.md` — all results
- `ISSUES_AND_FIXES.md` — any new bugs discovered
- `docs/KNOWN_LIMITATIONS.md` — any new engine quirks found
- DEF framework if new patterns emerge

---

## Estimated Time

| Phase | Mods | Time |
|-------|------|------|
| Tier 1 (FAIL) | 12 | ~25 min |
| Tier 2 (WARN) | 7 | ~10 min |
| Tier 3 weapons | 21 | ~25 min |
| Tier 3 utilities | 5 | ~10 min |
| Tier 3 maps | ~10 | ~15 min |
| Log parsing + reporting | — | ~5 min |
| **Total** | **~55** | **~90 min** |
