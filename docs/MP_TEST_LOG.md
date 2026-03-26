# MP Test Log

Real multiplayer testing results. Tools passing != game works. Only entries here are confirmed in actual MP.

---

## Session 1 — 2026-03-23 (2 accounts, same machine)

### CONFIRMED WORKING
| Mod | Status | Notes |
|-----|--------|-------|
| AC130_Airstrike_MP | FIXED | Desync and performance issues fixed. Pool 500->30, cached sounds. Camera sensitivity matched to game settings. |

### CONFIRMED BROKEN
| Mod | Symptom | Root cause |
|-----|---------|-----------|
| FPV_Drone_Tool | Works for host. Clients can't move camera in drone view. | Likely: mousedx/mousedy with player param, or drone camera logic gated behind host-only check. Needs investigation. |

### BUGS FOUND & FIXED
| Mod | Bug | Fix |
|-----|-----|-----|
| FPV_Drone_Tool | Client can't move camera or control drone | Added clientInput system — client sends input via ServerCall, server reads from clientInput instead of raw keys |
| Thruster_Tool_Multiplayer | Scroll wheel switches tools while holding G to adjust power | Moved locktool to top of tool block so it takes effect before engine processes scroll |

### NEEDS INVESTIGATION
| Mod | Issues |
|-----|--------|
| Predator_Missile_MP | 1. Missile camera sensitivity too slow (needs to match ground sensitivity). 2. Camera cuts back to character while missile still in flight (both host and client). 3. Black/white filter persists after camera cuts. 4. Client has better UI (green targeting boxes, thermal/NV cycling) than host — host may be missing client-side UI code. |

### UNTESTED
All other mods — need testing in future sessions.

---

## Session 2 — 2026-03-26 (2 accounts, same machine, Workshop sync)

### CONFIRMED WORKING
| Mod | Notes |
|-----|-------|
| Jackhammer | Perfect — all sounds, animations, effects, destruction sync on both client and host. Charge power light syncs. |
| Tripmine | Working great for both client and host. |

### CONFIRMED WORKING (minor issues)
| Mod | Issues |
|-----|--------|
| Thruster_Tool_Multiplayer | Works well. C to change mode visually toggles between toggle/hold but always behaves as toggle. User wants power cap at 300. |
| VectorRazor | Works for HOST only. Client: not in toolbar. Host: inconsistent cut depth at max 5.0m on brick. Client can't see laser line from tool center. UI in top left conflicts — needs moving to bottom left per UI_STANDARDS.md. |

### NOT IN TOOLBAR (RegisterTool changes not yet published)
20 mods had RegisterTool added to working directory but changes weren't uploaded to Workshop yet. Need to run update.bat again.

AC130_Airstrike_MP, Asteroid_Strike, Black_Hole, Bunker_Buster_MP, C4, Charge_Shotgun, CnC_Weather_Machine, Desert_Eagle, Exploding_Star, Fire_Fighter_MP, High_Tech_Drone, Hook_Shotgun, Laser_Cutter, Light_Saber, Molotov_Cocktail, Multiple_Grenade_Launcher, ODM_Gear, Predator_Missile_MP, Rods_from_Gods

### BUGS FOUND
| Mod | Bug | Perspective |
|-----|-----|-------------|
| ARM_AK47 | No animation/effects visible when watching other player. Can't reload with R — only reloads on empty magazine. | Both |
| ARM_Glock | Same as AK47 — no animation/effects watching other, can't manual reload | Both |
| ARM_M4A4 | No animation/effects when watching other player use it | Both |
| Light_Katana_MP | Tool model is MASSIVE. No terrain/building damage (player damage works). Q dash does nothing. Animations look wrong due to oversized model. | Both |
| VectorRazor | Not in toolbar for CLIENT. Laser line from tool center invisible to other player. | Client |
| FPV_Drone_Tool | Too many issues to document — deferred to separate session | Both |

### UNTESTED
Maps, vehicles, utilities — testing tools first.

---

## How to update this log

After each MP test session:
1. Add results under the session heading
2. Move mods from UNTESTED to CONFIRMED WORKING or CONFIRMED BROKEN
3. Include specific symptoms for broken mods
4. Run `python -m tools.logparse` and note any errors
