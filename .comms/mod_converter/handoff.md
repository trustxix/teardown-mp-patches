---
task_id: T178
saved_at: 2026-03-21T09:58:32.143672+00:00
---

## T178 — ClientCall-Sound Refactor (30 findings, 8 mods)

STATUS: Waiting for QA Lead batch approval. Sent 2 requests (094944 and 095526). All 8 mods fully pre-analyzed.

### T177 COMPLETED — PlayersRemoved cleanup
All 10 mods fixed in 4 batches. All PASS lint + deepcheck.

### T178 Pre-Analysis (COMPLETE — ready to code)

**Batch 1 (easy, 2 mods):**
- Magnetizer_V2 (1 fix): Line 253 `ClientCall(p, "client.onSelectSound")` → add `LoadSound("MOD/snd/select.ogg")` in server.init as srv_selectSnd, replace with `PlaySound(srv_selectSnd, GetPlayerPos(p), 1)`. Client handler at line 517.
- FPV_Drone_Tool (3 fixes): Lines 107/129 `ClientCall(0,"client.playExplosionSound",pos,15,"grenade")` → `PlaySound(grenade_sound, pos, 15)`. Line 279 same but "crash" type → `PlaySound(ex_sound, pos, 20)`. Server already has handles at lines 27-28. Client handler at line 1025 + duplicate loads at 46-47 can be removed.

**Batch 2 (annotation only, 1 mod):**
- CnC_Weather_Machine (2): Both route to UiSound() for non-positional atmospheric audio. Add @lint-ok CLIENTCALL-SOUND annotations. NOT code changes.

**Batch 3 (medium, 3 mods):**
- Multiplayer_Spawnable_Pack (2 real, 4 reported): scripts/bounce.lua entity script. Root bounce.lua is stale duplicate (identical, not referenced by any XML). Load snd in server.init, replace ClientCall(0,...) with PlaySound.
- Service_Vehicles_MP (6): script/door.lua. Same pattern as EVF — sounds table in client.init, dispatcher client.playDoorSound. Migrate sounds to server.init.
- Toyota_Supra_MP (2): script/door-lock.lua + door-lockbac.lua. serverPlayDoorSound wrapper around ClientCall. Load clientSounds in server.init instead.

**Later (complex):**
- Hurricanes_and_Blizzards (5): Custom SoundTable with stop_all (stopSoundOnClient) — can't be replaced by server PlaySound. May need @lint-ok for stop calls, refactor for play calls.
- Koenigsegg_Agera_MP (7): EVF.lua, same client sounds dispatch pattern as Service_Vehicles_MP but 7 findings. Straightforward but larger.

### Other findings
- T181 created: Thruster_Tool_Multiplayer missing SetToolAmmo + ammo.display (low priority)
- All workshop tool mods already converted — scanner confirmed no unconverted mods remain
- Deep analysis: 22 FAIL, 2 WARN. Most are vehicles/maps/NPCs with asset false positives (QA Lead handling via T176).