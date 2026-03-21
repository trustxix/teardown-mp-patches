# Desync Pattern Scan Results — 2026-03-20

Scanned all 125 installed mods (at time of scan; now 112 as of 2026-03-21) for the 5 desync patterns found in Bunker Buster.
Awaiting single-player test on Bunker Buster fixes before applying to other mods.

---

## Pattern 1: shared table bloat (unbounded growth)

Large shared tables sync to all clients every frame. Growth = more bandwidth = lag.

| Mod | Table | Risk | Notes |
|-----|-------|------|-------|
| AC130_Airstrike_MP | `shared.projectiles[i]` | REVIEW | Projectile tracking — may clean up via entity lifecycle, needs manual check |
| All_In_One_Utilities | `shared.playerData[playerID]` | REVIEW | Per-player data — may clean up in PlayersRemoved, needs check |
| Bunker_Buster_MP | `shared.spawnTargets` | **FIXED** | Cleanup added (entries >60s removed) |
| FPV_Drone_Tool | `shared.Players[i]` | REVIEW | Player tracking — may clean up in PlayersRemoved |
| Gwel_Mall | `shared.sprinklers[zoneId]` | LOW | Map content mod, fixed number of zones |

**Verdict:** Only 4 mods besides Bunker Buster. All need manual review because cleanup might exist in code the scanner couldn't detect (PlayersRemoved, entity scripts, etc.).

---

## Pattern 2: Stale aim (raycast in update, input in tick)

No other mods found with this pattern. Most mods do their raycast in the same function as input handling. Bunker Buster was the only one that split them.

**Verdict:** No action needed on other mods.

---

## Pattern 3: Redundant GetString("game.player.tool") calls

| Mod | Calls | Action |
|-----|-------|--------|
| Bunker_Buster_MP | 3 remaining (getFirstPersonAim + client.draw) | **FIXED** (8→3, rest are in separate scopes) |

Only Bunker Buster had 3+ calls. All other mods either cache it or call it 1-2 times.

**Verdict:** No action needed on other mods.

---

## Pattern 4: v1 fallback loops (SAFE TO FIX)

These mods iterate `for id = 1, N` to find players instead of using `Players()`. In v2, `Players()` is always available. These loops waste CPU iterating up to 300 phantom IDs per frame.

### Results after manual verification (2026-03-20):

**15 of 16 findings were FALSE POSITIVES.** The `for i = 1, N` loops in AK-47, Asteroid_Strike, Attack_Drone, Dual_Berettas, Dual_Miniguns, Exploding_Star, HADOUKEN, Hook_Shotgun, M249, M4A1, Minigun, Multi_Grenade_Launcher, Multiple_Grenade_Launcher, Nova_Shotgun, and P90 are **projectile shell array initializers** (`data.projectileHandler.shells[i] = deepcopy(...)`) — NOT player iteration loops. All already use `Players()` for player iteration.

**1 real fix applied:**

| Mod | Fix | Status |
|-----|-----|--------|
| Hide_and_Seek | Removed `type(Players) == "function"` guard in `hs/infra/players.lua` | FIXED, lint clean |

**Lesson:** The scanner pattern `for id = 1, N` + `GetPlayerTool` elsewhere in file produces false positives. Must verify loop body before fixing.

---

## Pattern 5: Per-tick RPC (MOSTLY FALSE POSITIVES)

The scanner flagged 272 RPC calls as "per-tick" but **most are false positives** — they're inside `InputPressed()` guards (one-shot events), not actually called every tick. The scanner detected them because they're inside a `Players()` loop in `client.tick`, but they only fire on button press.

### Actually per-tick (called every frame, not input-guarded):

These need manual review because they send RPCs continuously while a button is held or a state is active:

| Mod | Line | Call | Concern |
|-----|------|------|---------|
| Thruster_Tool | L323 | `server.setFiringState` | Sends thruster on/off state every tick while active |
| ODM_Gear | L583/586 | `server.setReeling` | Sends reel state while holding key |
| Guided_Missile | L353 | `server.setBoosting` | Sends boost state change (may be edge-triggered) |
| Dual_Miniguns | L349/354 | `server.setRmbDown`/`setCtrlDown` | Sends hold state change |
| Vacuum_Cleaner | L428 | `server.setRmbDown` | Sends hold state change |
| Dragonslayer | L172 | `server.setRmbDown` | Sends hold state change |
| Minigun | L279 | `server.setCtrlDown` | Sends hold state change |
| Control | L329 | `server.setHover` | Sends hover state toggle while airborne |

**These are edge-triggered** (only fire when state changes, not every frame) — the code checks `if wantHover ~= data.hoverActive` or `if rmbNow ~= data.rmbWas` before sending. So they're actually fine for most use cases.

**True per-tick RPCs that should use registry sync instead:**
- None confirmed. All detected RPCs are either one-shot (InputPressed) or edge-triggered (state change detection).

### Not per-tick (InputPressed-guarded, safe as-is):

Everything else in the list (setOptionsOpen, reload, shoot, grab, etc.) — these only fire once when a button is pressed. They're inside the `Players()` loop but gated by `InputPressed()` which returns true for exactly one frame. **No fix needed.**

---

## Summary & Action Plan

| Pattern | Mods affected | Fix type | Priority |
|---------|--------------|----------|----------|
| P1: shared bloat | 4 (need review) | MANUAL REVIEW | Medium — only causes lag in long sessions |
| P2: stale aim | 0 (only Bunker Buster, fixed) | N/A | Done |
| P3: redundant tool check | 0 (only Bunker Buster, fixed) | N/A | Done |
| P4: v1 fallback loops | 1 (15 were false positives — shell arrays, not player loops) | FIXED (Hide_and_Seek) | Done |
| P5: per-tick RPC | 0 confirmed (all edge-triggered) | N/A | None needed |

### Next steps:
1. **Test Bunker Buster fixes in single player** — confirm all 5 fixes work
2. **Fix P4 (v1 loops) in 16 mods** — safe, mechanical replacement, user approved
3. **Manually review P1 (shared bloat) in 4 mods** — user needs to check if cleanup exists in entity scripts
4. **MP test when available** — verify bandwidth improvement from P1+P4 fixes
