# What Doesn't Work

Failed approaches and mistakes to never repeat. Check this BEFORE attempting any fix.

---

## Don't: Change `initBool` defaults to fix savegame-cached options
**What we tried:** Changed `initBool("control.toolOnly", false)` to `initBool("control.toolOnly", true)` in Control mod.
**What happened:** No effect — player's savegame already had `false` stored. `initBool` only writes if the key doesn't exist.
**Lesson:** `initBool`/`initFloat`/`initInt` are write-once. They set defaults for NEW saves only. To change behavior for existing saves, either hardcode the logic or use `SetBool` (but that prevents user toggling).

---

## Don't: Use soft option gates for safety-critical behavior
**What we tried:** Relying on `getBool("control.toolOnly")` to gate abilities behind tool selection.
**What happened:** Option defaulted to off, meaning all abilities fired globally. Users who never opened the options menu had ungated superpowers on every tool.
**Lesson:** If a behavior MUST be gated (like "only fire when this tool is equipped"), hardcode it. Options are for preferences, not safety.

---

## Known limitation: No clean way to disable grab for ADS weapons
**What we tried:** `SetBool("game.player.cangrab", false)` — no effect. `ReleasePlayerGrab(p)` every tick — caused hand flash and may interfere with tool body attachment.
**Root cause:** No Teardown API exists to prevent the grab from starting. The engine processes grab input before mod code runs.
**Status:** No fix applied. RMB grab can conflict with ADS on gun mods.

---

## RESOLVED: Weapons float away after shooting
**Symptom:** After left-clicking to fire, the weapon model floats out of the player's hands in zero gravity. Affected 21+ mods.
**Root cause found:** Two related causes, both involving timer-based position changes to the tool body:
1. `SetToolTransform` with recoilTimer Z offset (`Vec(0, 0.2, recoilTimer)`) — pushes tool body forward/backward, clips into player physics, gets ejected
2. `SetShapeLocalTransform` with position offset (`Vec(0, 1, -t)`) — same effect, slides shapes within the body causing physics collision
**Why v1 didn't have this:** In v1, everything runs in one context with no server/client physics split. The single-context physics kept the body stable. In v2, the split creates competing physics states.
**Why `~= 0` timer check made it worse:** The `~= 0` check (vs `> 0` in v1 originals) let the timer go negative, pushing the tool behind the player indefinitely.
**Fix:** Remove ALL timer-based position offsets from SetToolTransform AND SetShapeLocalTransform. Use static positions only. Keep timer decrements clamped to 0 for other logic.
**What we tried that DIDN'T work:**
- `ReleasePlayerGrab(p)` every tick — wrong hypothesis (grab is RMB, not LMB), removed from all 45 mods
- `SetBool("game.player.cangrab", false)` — no effect
- Merging multiple SetToolTransform calls into one — still floated with position offset
- Changing smooth parameter (0.5 vs 1.0) — no effect
- Removing GetToolBody from server code — no effect
- Emptying server.tickPlayer entirely — still floated (proved it's client-side)
**What DID work:**
- Stripping client.tickPlayer to ONLY `SetToolTransform(Transform(Vec(0, 0.2, 0)), 1.0, p)` — no float, confirmed the recoil offset was the cause
- Adding back shooting/sound/particles without recoil offset — no float
- Adding back recoil offset — float returned, confirmed
**Status:** FIXED across 21 mods. Dual_Berettas required separate fix (SetShapeLocalTransform position offset instead of SetToolTransform).

---

## Known limitation: XML prefab tools can't be switched programmatically
**Symptom:** `SetString("game.player.tool")` and `SetPlayerTool()` can't properly load tools registered with XML prefab files. Tool body is invisible, can't shoot.
**Affected tools:** ARM M4A4, ARM AK-47, ARM Glock, Light Saber [GP] — all register with `.xml` instead of `.vox`.
**What we tried:** SetString (v1), SetPlayerTool via ServerCall (v2), deferred tick switching, SetToolEnabled + SetToolAmmo re-initialization. None worked.
**Resolution:** These tools are now hidden from the Tool Menu via case-insensitive ID filtering. Use the toolbar (1-6 keys) to switch to them.

---

## Don't: Use hardcoded case-sensitive table lookup for tool ID filtering
**What we tried:** `local xml_prefab_tools = { ["ARM-Ak47"] = true }` with exact key match.
**What happened:** No tools were filtered — `ListKeys('game.tool')` returned IDs in different case than RegisterTool specified.
**Fix:** Use `tool_id:lower():find("arm-")` for case-insensitive prefix matching instead of table lookup.
**Lesson:** Teardown's `ListKeys` may return keys in different case. Always use case-insensitive comparison for tool ID matching.

---

## Known limitation: Custom characters don't work in multiplayer
**What we tried:** Added `version = 2` to RPM Military Playermodels info.txt, converted both animation.lua scripts to v2 callbacks.
**What happened:** Game still says "character not supported in multiplayer." Only the 6 built-in Lagom family characters work in MP.
**Root cause:** Built-in MP characters are defined in the engine's encrypted `characters.lua.tde` in `data/script/`. The `characters.txt` modding system appears to be single-player only — the MP character picker ignores it entirely. No workshop character mod has `version = 2` either, suggesting this is an engine limitation, not a mod configuration issue.
**Status:** Cannot fix from mod side. Waiting for Tuxedo Labs to add characters.txt support to the MP character picker.

---

## Don't: Put PauseMenuButton in draw()
**What we tried:** Added `PauseMenuButton("Toggle Fly")` etc. inside `client.draw()` for All_In_One_Utilities and `draw()` for Debug Scanner.
**What happened:** Buttons didn't appear in the pause menu at all.
**Lesson:** `PauseMenuButton()` must be called from `tick()` / `client.tick()`. The `draw()` function is for UI rendering only — `PauseMenuButton` registers buttons during the tick phase.

---

## Don't: Assume `for i = 1, N` loops are player iteration
**What we tried:** Scanner flagged 15 mods with `for i = 1, 100`/`200`/`300`/`1500` loops as v1 player iteration fallbacks that should be replaced with `Players()`.
**What actually happened:** All 15 were projectile shell array initializers (`data.projectileHandler.shells[i] = deepcopy(defaultShell)`). The scanner matched them because `GetPlayerTool` existed elsewhere in the file.
**Lesson:** Always verify loop BODY before replacing. Pattern `for i = 1, N` + player API in same file ≠ player iteration. Check if the loop variable is used as a player ID or an array index.

---

## Don't: Add early return to client.tick without checking for remote player rendering
**What we almost did:** Added `return` at top of Bunker_Buster_MP's `client.tick` when wrong tool equipped — would have killed remote player tool transforms (other players' bunker busters wouldn't render correctly).
**Lesson:** Before adding early returns, scan the ENTIRE function for code that must run regardless of local tool (remote player rendering, global timers, shared state reads). Move that code above the gate.

---

## Don't: Use ClientCall to play game sounds
**What it looks like:** `ClientCall(0, "client.playFireSound", pos)` or `ClientCall(p, "client.playSound", snd, pos)`
**Why it's wrong:** The base game never does this. `PlaySound(snd, pos)` called on the server is automatically replicated to all clients by the engine with correct positional audio. ClientCall adds unnecessary RPC overhead and latency.
**What to do instead:** Call `PlaySound()` directly on the server. Use `UiSound()` for client-only UI feedback (button clicks, menu sounds).
**Source:** Confirmed by analyzing official snowball.lua, tank.lua, mpcampaign/tools.lua — all use server-side PlaySound.

---

## Don't: Call ToolAnimator only for the local player
**What it looks like:**
```lua
-- WRONG:
if IsPlayerLocal(p) then
    tickToolAnimator(animator, dt, nil, p)
end
```
**Why it's wrong:** `tickToolAnimator` internally handles FP vs TP rendering based on `IsPlayerLocal(p)`. If you only call it for the local player, remote players see a static, unanimated tool model — no recoil, no run pose, no swim pose.
**What to do instead:** Call `tickToolAnimator` for ALL players inside a `for p in Players()` loop. Create per-player animators in `PlayersAdded()`, clean up in `PlayersRemoved()`.
**Source:** Confirmed by analyzing official snowball.lua — calls tickToolAnimator for every player.

---

## Don't: Use per-tick ServerCall/ClientCall for continuous state
**What it looks like:**
```lua
-- WRONG — fires 60 RPCs per second:
function client.update(dt)
    ServerCall("server.syncAmmo", GetLocalPlayer(), ammo)
end
```
**Why it's wrong:** The base game uses ZERO per-tick RPCs for state sync. Registry broadcast (`SetInt(key, val, true)`) and `shared.*` tables handle all continuous state. RPCs are reserved for discrete one-time events (button press, tool pickup, team join).
**What to do instead:** Use `SetInt/SetFloat/SetBool(key, value, true)` for state changes. Use `shared.*` tables for server→client state. Use ServerCall/ClientCall only for discrete events.
**Source:** Confirmed by analyzing all mpcampaign scripts — ServerCall only used for button clicks (team join, play, unstuck).

---

## Don't: Poll GetPlayerHealth() every tick for death detection
**What it looks like:**
```lua
-- WRONG:
if GetPlayerHealth(p) <= 0 and wasAlive[p] then
    -- handle death
    wasAlive[p] = false
end
```
**Why it's wrong:** Requires maintaining a `wasAlive` table and can miss deaths between ticks. The base game uses the event system instead.
**What to do instead:**
```lua
local c = GetEventCount("playerdied")
for i = 1, c do
    local victim, attacker = GetEvent("playerdied", i)
    -- process exactly once, no tracking table needed
end
```
**Source:** Confirmed by analyzing official mpcampaign/stats.lua, tools.lua — all use GetEventCount/GetEvent.

---

## CORRECTED (2026-03-21): PlaySound on server is NOT wrong
**What we believed:** `PlaySound()` is client-only and should never be called in server.* functions. Our SERVER-EFFECT lint rule flagged it and told devs to "use ClientCall() to play effects on all clients."
**What actually happens:** The base game calls `PlaySound()` directly on the server in snowball.lua, tank.lua, and mpcampaign/tools.lua. The engine auto-syncs the sound to all clients with positional audio.
**Impact:** Our lint rule created a self-fulfilling cycle — it flagged PlaySound on server → devs wrapped sounds in ClientCall → our new CLIENTCALL-SOUND rule caught 30 unnecessary RPCs across 8 mods. The original lint rule caused the problem the new lint rule found.
**Fix:** Removed PlaySound from the SERVER-EFFECT regex. PlaySound on server is now CLEAN. SpawnParticle/PointLight/SetShapeEmissiveScale are still correctly flagged as client-only.
**Lesson:** Always verify lint assumptions against the base game source code. A reasonable-sounding rule can create real bugs if the underlying assumption is wrong.

---

## Don't: Replace mousedx/mousedy with camerax/cameray for script-controlled cameras
**What we tried:** Replaced `InputValue("mousedx")` / `InputValue("mousedy")` with `InputValue("camerax")` / `InputValue("cameray")` in AC-130 fly cam, FPV Drone, Light Katana, Light Saber.
**What happened:** Camera stopped responding to mouse movement entirely. Player sees only clouds/sky.
**Root cause:** When a mod calls `SetCameraTransform()` to override the camera, the engine suppresses `camerax`/`cameray` (returns 0) because it considers the camera script-controlled. `mousedx`/`mousedy` give raw mouse delta that always works regardless of camera state.
**Lesson:** `mousedx`/`mousedy` ARE valid in v2 for custom camera control. Only use `camerax`/`cameray` when the engine controls the camera (normal gameplay). If the mod uses `SetCameraTransform`, keep `mousedx`/`mousedy`.

---
