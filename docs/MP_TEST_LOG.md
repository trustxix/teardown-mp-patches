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

## How to update this log

After each MP test session:
1. Add results under the session heading
2. Move mods from UNTESTED to CONFIRMED WORKING or CONFIRMED BROKEN
3. Include specific symptoms for broken mods
4. Run `python -m tools.logparse` and note any errors
