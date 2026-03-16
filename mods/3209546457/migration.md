# Migration Report: animation.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/animation.lua
+++ patched/animation.lua
@@ -1,16 +1,11 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------
-model = {}
-model.animator = 0
-
-
-------------------------------------------------------------------------
-function init()
-	model.animator = FindAnimator()
+#version 2
+function server.init()
+    model.animator = FindAnimator()
 end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        MakeRagdoll(model.animator)
+    end
+end
 
-function tick(dt)
-    MakeRagdoll(model.animator)
-end

```

---

# Migration Report: assets\poopwizard\wizardboss.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/assets\poopwizard\wizardboss.lua
+++ patched/assets\poopwizard\wizardboss.lua
@@ -1,129 +1,4 @@
----@diagnostic disable: lowercase-global
-
--- I have no idea what I'm doing, but it's working - KBD2
-
---[[
-#include "../../scripts/libraries/Automatic.lua"
-]]
-
-ARENA_RADIUS = 20
-FLOAT_HEIGHT = 8
-
-WIZ_OFFSET = 3
-
-NUM_ATTACKS = 8
-
-WIZ_MAX_HEALTH = 75
-
-WEAPON_DAMAGE = 1
-
-STATES = {
-    WAITING = -1;
-    FLOATING = 0;
-    CIRCLING = 1;
-    GOSTRAIGHT = 2;
-    NOANIM = 3;
-    FACEPLAYER = 4;
-    FACEPLAYERNOPITCH = 5;
-}
-
-FIGHTPROGRESS = {
-    PREFIGHT = -1;
-    CHARGING = 0;
-    EASY = 1;
-    MEDIUM = 2;
-    HARD = 3;
-    ENDGAME = 4;
-    DEAD = 5;
-}
-
-STATE = {}
-
-function init()
-    SetBool("level.isInSpace", true)
-    RegisterListenerTo("wizardhit", "damageHandler")
-    endCameraT = GetLocationTransform(FindLocation("endCameraPos",true))
-    endCamTimer = 0
-
--- Important entities
-    STATE.anchor = GetLocationTransform(FindLocation("wizard_anchor", true))
-    STATE.body = FindBody("wizard_body")
-    STATE.spellSpawnLocal = TransformToLocalPoint(GetBodyTransform(STATE.body), GetLocationTransform(FindLocation("spell_spawn")).pos)
-    STATE.arenaBoundaryShape = FindShape("arena_boundary", true)
-    STATE.dialogueTrigger = FindTrigger("dialogue", true)
-    STATE.waveTriggers = FindTriggers("hordetrigger", true)
-
--- Brain/Animation
-    STATE.actionTimer = 0
-    STATE.move = {}
-    STATE.physState = STATES.WAITING
-    STATE.velocity = Vec()
-    STATE.lastPosition = Vec()
-
--- Sound
-    STATE.currentSpeechHandle = nil
-    STATE.currentSpeechTime = 0
-    STATE.musicPlayed = false
-
--- Level progression
-    STATE.progress = FIGHTPROGRESS.PREFIGHT
-    STATE.health = 1
-    STATE.preambleTP = not GetBool("savegame.mod.skipdialogue")
-
--- Attacks
-    STATE.coroutines = {}
-    STATE.lastAttack = 0
-    STATE.forcedAttacksLeft = {1, 2, 3, 4}
-    STATE.isHatActive = false
-
--- Movement sounds
-    SOUND_LOOP_WIZ_FLYING = LoadLoop("MOD/assets/poopwizard/sounds/WizardFlyLoop01")
-
--- Attack-controlled sounds
-    SOUND_BOOK_BITE = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardBookBite01.ogg")
-    SOUND_CRYSTAL_LAUNCH = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardCrystalLaunch01.ogg")
-    SOUND_CRYSTAL_TRIGGER = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardCrystalSetOff01.ogg")
-    SOUND_MAGIC_EXPLODE = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardMagicExplodeLayer01.ogg")
-    SOUND_MISSILE_SHOOT = LoadSound("MOD/assets/poopwizard/sounds/attacks/WIzardMissileShoot01.ogg")
-    SOUND_RUBBLE_RING = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardRubbleRingEmit01.ogg")
-    SOUND_GNOME_SCREAM = LoadSound("MOD/snd/GnomeScream0.ogg")
-    finaleSound = LoadSound("MOD/snd/finale.ogg")
-
-    SOUND_LOOP_WIZ_HAT_SPIN = LoadLoop("MOD/assets/poopwizard/sounds/attacks/WizardHatSpin01.ogg")
-    SOUND_LOOP_LASER_SHOOT = LoadLoop("MOD/assets/poopwizard/sounds/attacks/LaserLoop01.ogg")
-    SOUND_LOOP_LASER_HIT = LoadLoop("MOD/assets/poopwizard/sounds/attacks/LightningLoopStrike01.ogg")
-
--- Physical voicelines
-    SOUND_VL_OW = LoadSound("MOD/assets/poopwizard/sounds/voicelines/ow0.ogg")
-
--- Dialogue played over the speech system
-    SOUND_VL_DEATH = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/death.ogg")
-    SOUND_VL_DOIT1 = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/doit1.ogg")
-    SOUND_VL_DOIT2 = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/doit2.ogg")
-    SOUND_VL_REFLECTING = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/reflecting.ogg")
-    SOUND_VL_MONOLOGUE = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/monologue.ogg")
-
--- UI voiceline
-    SOUND_VL_UI_DEADGNOMES = "MOD/assets/poopwizard/sounds/attack_voicelines/deadgnomes.ogg"
-    SOUND_VL_UI_HYPERHAT = "MOD/assets/poopwizard/sounds/attack_voicelines/hyperhat.ogg"
-    SOUND_VL_UI_MAGICMINES = "MOD/assets/poopwizard/sounds/attack_voicelines/magicmines.ogg"
-    SOUND_VL_UI_RUBBLERING = "MOD/assets/poopwizard/sounds/attack_voicelines/rubblering.ogg"
-    SOUND_VL_UI_BOOKBITE = "MOD/assets/poopwizard/sounds/attack_voicelines/bookbite.ogg"
-    SOUND_VL_UI_PEW_0 = "MOD/assets/poopwizard/sounds/attack_voicelines/pew0.ogg"
-    SOUND_VL_UI_PEW_1 = "MOD/assets/poopwizard/sounds/attack_voicelines/pew1.ogg"
-    SOUND_VL_UI_RAY_CAST = "MOD/assets/poopwizard/sounds/attack_voicelines/ray cast.ogg"
-    SOUND_VL_UI_BUSTERBOMBS = "MOD/assets/poopwizard/sounds/attack_voicelines/busterbombs.ogg"
-
-    SOUND_VL_UI_LAUGH = "MOD/assets/poopwizard/sounds/voicelines/laugh.ogg"
-    SOUND_VL_UI_STOPOW = "MOD/assets/poopwizard/sounds/voicelines/stopow.ogg"
-    SOUND_VL_UI_THATHURT = "MOD/assets/poopwizard/sounds/voicelines/thathurt.ogg"
-    SOUND_VL_UI_GETFUCKED = "MOD/assets/poopwizard/sounds/voicelines/getfucked.ogg"
-
--- Music
-    MUSIC_FIGHT = "MOD/assets/poopwizard/sounds/Far_From_Gnome_1.ogg"
-    if not GetBool("savegame.mod.skipdialogue") then SetBool("level.cantDashJump",true) end
-end
-
+#version 2
 function damageHandler(data)
     if STATE.progress == FIGHTPROGRESS.PREFIGHT or STATE.progress == FIGHTPROGRESS.CHARGING then
         return
@@ -132,7 +7,7 @@
 
     if STATE.health == 0 and not startTitleCardSequence then
         startTitleCardSequence = true
-        SetBool("level.startTitleCardSequence",true)
+        SetBool("level.startTitleCardSequence",true, true)
         PlaySound(finaleSound,GetCameraTransform().pos,1.5)
     end
 
@@ -177,7 +52,6 @@
     end
 end
 
--- Needed because we do a passthrough level start now
 function creditsTimer()
     coRun(0.01)
     wizardShot = true
@@ -194,134 +68,6 @@
     ParticleDrag(0.1)
 end
 
-function tick(dt)
-    -- DebugCross(STATE.anchor.pos, 0, 1, 0, 1)
-    -- DebugWatch("state", STATE.state)
-    -- DebugWatch("timer", STATE.actionTimer)
-    -- DebugWatch("num coroutines", #STATE.coroutines)
-    -- DebugWatch("Health", STATE.health)
-    -- DebugWatch("Forced attacks left", STATE.forcedAttacksLeft)
-    -- DebugWatch("Progress", STATE.progress)
-
-    if not STATE.preambleTP and GetBool("savegame.mod.skipdialogue") then
-        SetPlayerTransform(GetLocationTransform(FindLocation("preamble_skip", true)))
-        STATE.preambleTP = true
-    end
-
-    handleRotation()
-    handlePosition(dt)
-
-    if STATE.currentSpeechHandle ~= nil and not startTitleCardSequence then
-        if STATE.currentSpeechHandle == SOUND_VL_MONOLOGUE then
-            PlayLoop(STATE.currentSpeechHandle, GetPlayerCameraTransform().pos, 8)
-        else
-            PlayLoop(STATE.currentSpeechHandle, STATE.anchor.pos, 16)
-        end
-        STATE.currentSpeechTime = STATE.currentSpeechTime + dt
-
-        if STATE.currentSpeechHandle == SOUND_VL_REFLECTING and STATE.currentSpeechTime > 11 and not STATE.musicPlayed then
-            STATE.musicPlayed = true
-            PlayMusic(MUSIC_FIGHT)
-        end
-
-        if 
-        (STATE.currentSpeechHandle == SOUND_VL_DEATH and STATE.currentSpeechTime > 37)
-        or (STATE.currentSpeechHandle == SOUND_VL_DOIT1 and STATE.currentSpeechTime > 18)
-        or (STATE.currentSpeechHandle == SOUND_VL_DOIT2 and STATE.currentSpeechTime > 16)
-        or (STATE.currentSpeechHandle == SOUND_VL_REFLECTING and STATE.currentSpeechTime > 27)
-        or (STATE.currentSpeechHandle == SOUND_VL_MONOLOGUE and STATE.currentSpeechTime > 25)
-        then
-            if STATE.currentSpeechHandle == SOUND_VL_REFLECTING then
-                SetBool("savegame.mod.skipdialogue", true)
-                SetBool("level.cantDashJump",false)
-                startTransitionHandler()
-            end
-
-            STATE.currentSpeechHandle = nil
-            STATE.currentSpeechTime = 0
-        end
-    end
-end
-
-function update(dt)
-    if STATE.progress == FIGHTPROGRESS.CHARGING then
-        STATE.health = math.min(STATE.health + WIZ_MAX_HEALTH * (GetTimeStep() / 3), WIZ_MAX_HEALTH)
-        if STATE.health == WIZ_MAX_HEALTH then
-            STATE.progress = FIGHTPROGRESS.EASY
-        end
-    end
-
-    if 
-    STATE.progress == FIGHTPROGRESS.PREFIGHT 
-    and not HasTag(STATE.dialogueTrigger, "triggered") 
-    and IsPointInTrigger(STATE.dialogueTrigger, GetPlayerCameraTransform().pos)
-    and not GetBool("savegame.mod.skipdialogue")
-     then
-        SetTag(STATE.dialogueTrigger, "triggered")
-        STATE.currentSpeechHandle = SOUND_VL_MONOLOGUE
-    end
-
-
-    if STATE.physState == STATES.WAITING and STATE.currentSpeechHandle == nil and AutoVecDist(GetBodyTransform(STATE.body).pos, GetPlayerTransform(false).pos) < 30 then
-        if GetBool("savegame.mod.skipdialogue") then
-            PlayMusic(MUSIC_FIGHT)
-            startTransitionHandler()
-        else
-            STATE.currentSpeechTime = 0
-            STATE.currentSpeechHandle = SOUND_VL_REFLECTING
-        end
-        SetShapeLocalTransform(STATE.arenaBoundaryShape, Transform(GetShapeLocalTransform(STATE.arenaBoundaryShape).pos, Quat()))
-    end
-
-    if STATE.health == 0 then
-        if STATE.progress ~= FIGHTPROGRESS.DEAD then
-            STATE.physState = STATES.NOANIM
-            STATE.deathTimer = 0
-            SetBodyTransform(STATE.body, STATE.anchor)
-            STATE.currentSpeechHandle = SOUND_VL_DEATH
-
-            STATE.playedFirst = false
-            STATE.playedSecond = false
-
-            STATE.progress = FIGHTPROGRESS.DEAD
-
-            local shapes = GetBodyShapes(STATE.body)
-            for i = 1, #shapes do
-                SetTag(shapes[i], "invisible")
-            end
-            SetLightEnabled(FindLight(), false)
-            Spawn("MOD/assets/poopwizard/wizard_beaten.xml", TransformToParentTransform(STATE.anchor, Transform(Vec(0, -1, 0), Quat())), true)
-            STATE.hatSmokeLoc = GetLocationTransform(FindLocation("wiz_defeated_smoke", true)).pos
-            StopMusic()
-        else
-            STATE.deathTimer = STATE.deathTimer + GetTimeStep()
-            if STATE.deathTimer > 45 and not STATE.playedFirst then
-                STATE.playedFirst = true
-                STATE.currentSpeechHandle = SOUND_VL_DOIT1
-            end
-            if STATE.deathTimer > 75 and not STATE.playedSecond then
-                STATE.playedSecond = true
-                STATE.currentSpeechHandle = SOUND_VL_DOIT2
-            end
-            if math.random() < 0.2 then
-                defeatedSmokeParticle()
-                SpawnParticle(VecAdd(STATE.hatSmokeLoc, Vec(rand(-0.2, 0.2), 0, rand(-0.2, 0.2))), QuatRotateVec(AutoRandomQuat(20), Vec(0, 0.3, 0)), rand(2, 3))
-            end
-        end
-    else
-        handleBrainCell(dt)
-    end
-
-    for i = 1, #STATE.coroutines do
-        coroutine.resume(STATE.coroutines[i])
-    end
-    for i = #STATE.coroutines, 1, -1 do
-        if coroutine.status(STATE.coroutines[i]) == "dead" then
-            table.remove(STATE.coroutines, i)
-        end
-    end
-end
-
 function defeatedSmokeParticle()
     ParticleReset()
     ParticleTile(0)
@@ -332,54 +78,6 @@
     ParticleRadius(rand(0.1, 0.3))
 end
 
-function draw(dt)
-    if startTitleCardSequence then
-        endCamTimer = endCamTimer + dt
-        SetCameraTransform(Transform(endCameraT.pos,QuatRotateQuat(endCameraT.rot,QuatEuler(40-endCamTimer,0,0))),70)
-        UiPush()
-            UiTranslate(UiCenter(), UiMiddle())
-            UiAlign("center middle")
-            UiColor(0,0,0,1)
-            UiPush()
-                backgroundOpacity = 0
-                if endCamTimer < 2.511 and endCamTimer < 10 then backgroundOpacity = 1 end
-                if endCamTimer > 10 then backgroundOpacity = endCamTimer-10 end
-                    UiColor(0,0,0,backgroundOpacity)
-                    UiRect(UiWidth(),UiHeight())
-            UiPop()
-            if endCamTimer >= 2.511 then UiImageBox("MOD/assets/endCard.png",UiWidth(),UiHeight()) end
-        UiPop()
-        if endCamTimer > 11.5 then
-            SetInt("savegame.mod.stats.score.inRun", GetInt("level.score"))
-            SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"))
-            SetInt("savegame.mod.stats.levelOrder",4)
-            SetBool("savegame.mod.skipdialogue", false)
-            StartLevel("credits", "MOD/main.xml", "credits", true)
-            return
-        end
-    else
-        UiPush()
-            if STATE.physState ~= STATES.WAITING then
-                UiPush()
-                    UiTranslate(460, 835)
-                    UiFont("MOD/assets/Gemstone.ttf", 24)
-                    UiAlign("left middle")
-                    UiText("Paul, High Hogwash Wizard of the Gnown Universe")
-                UiPop()
-                UiPush()
-                    UiTranslate(460, 850)
-                    UiImageBox("ui/common/box-outline-6.png", 1000, 15, 6, 6)
-                    if STATE.health > 0 then
-                        UiTranslate(1, 1)
-                        UiImageBox("MOD/assets/poopwizard/box-solid-4.png", (998 / WIZ_MAX_HEALTH) * STATE.health, 13, 4, 4)
-                    end
-                UiPop()
-            end
-        UiPop()
-    end
-end
-
--- My mate Bazza was born with one brain cell, true story
 function handleBrainCell(dt)
     STATE.actionTimer = math.max(0, STATE.actionTimer - dt)
     if STATE.actionTimer == 0 and STATE.physState ~= STATES.WAITING then
@@ -428,7 +126,7 @@
     end
 
     local bodyTransform = GetBodyTransform(STATE.body)
-    local playerTransform = GetPlayerTransform(false)
+    local playerTransform = GetPlayerTransform(playerId, false)
     local targetRot = Quat()
 
     if STATE.physState == STATES.FLOATING or STATE.physState == STATES.WAITING or STATE.physState == STATES.FACEPLAYER or STATE.physState == STATES.FACEPLAYERNOPITCH then
@@ -456,7 +154,6 @@
     SetBodyTransform(STATE.body, Transform(bodyTransform.pos, AutoSM_Get(STATE.rot)))
 end
 
--- Dense ass code
 function handlePosition(dt)
     local bodyTransform = GetBodyTransform(STATE.body)
     if STATE.physState == STATES.WAITING then
@@ -490,9 +187,8 @@
     STATE.lastPosition = newPos
 end
 
--- This kicks everything off
 function startTransitionHandler()
-    local playerPos = GetPlayerTransform(false).pos
+    local playerPos = GetPlayerTransform(playerId, false).pos
     -- We make the wizard fly off to the circle *away from the player*
     local angle = 2 * math.pi - math.atan2(-STATE.anchor.pos[3] + playerPos[3], STATE.anchor.pos[1] - playerPos[1])
     UiSound(SOUND_VL_UI_LAUGH, 1.5)
@@ -517,7 +213,7 @@
     
     if STATE.progress == FIGHTPROGRESS.ENDGAME then
         chosenAttack = 8
-    elseif #STATE.forcedAttacksLeft > 0 then
+    elseif #STATE.forcedAttacksLeft ~= 0 then
         local pick = math.random(1, #STATE.forcedAttacksLeft)
         chosenAttack = STATE.forcedAttacksLeft[pick]
         table.remove(STATE.forcedAttacksLeft, pick)
@@ -569,17 +265,6 @@
     STATE.lastAttack = chosenAttack
 end
 
---[[ Attack ideas:
-- Coloured balls
-- Lightning
-- Carpet bomb
-- Floor spikes
-- Laser
-]]
-
---- MAGIC MISSILE ATTACK
-
--- Wizard balls
 function doBallsAttack()
     local colours = {Vec(1, 0, 0), Vec(0, 1, 0), Vec(0, 0, 1), Vec(1, 0, 1), Vec(1, 1, 0), Vec(0, 1, 1), Vec(1, 1, 1)}
     coRun(1, glowyHeldThing)
@@ -616,7 +301,7 @@
 function ball(col)
     local bodyTransform = GetBodyTransform(STATE.body)
     local pos = TransformToParentPoint(bodyTransform, STATE.spellSpawnLocal)
-    local playerPos = GetPlayerTransform(false).pos
+    local playerPos = GetPlayerTransform(playerId, false).pos
     local vel = VecNormalize(VecSub(Vec(playerPos[1], FLOAT_HEIGHT * 2, playerPos[3]), bodyTransform.pos))
     vel = QuatRotateVec(QuatEuler(0, math.random() * 180 - 90, 0), vel)
 
@@ -624,7 +309,7 @@
 
     PlaySound(SOUND_MISSILE_SHOOT, pos, 1)
 
-    local goalPos = GetPlayerTransform().pos
+    local goalPos = GetPlayerTransform(playerId).pos
 
     while true do
         pos = VecAdd(pos, VecScale(vel, 30 * GetTimeStep()))
@@ -652,7 +337,7 @@
         SpawnParticle(pos, Vec(), 2)
 
         QueryRejectBody(STATE.body)
-        if QueryClosestPoint(pos, 0.6) or AutoVecDist(goalPos, pos) < 0.3 or AutoVecDist(pos, GetPlayerCameraTransform().pos) < 0.7 then
+        if QueryClosestPoint(pos, 0.6) or AutoVecDist(goalPos, pos) < 0.3 or AutoVecDist(pos, GetPlayerCameraTransform(playerId).pos) < 0.7 then
             Explosion(pos, 0.1)
             Delete(light)
             PlaySound(SOUND_MAGIC_EXPLODE, pos, 1)
@@ -688,8 +373,6 @@
     ParticleTile(6)
 end
 
---- SPINNING HAT ATTACK
-
 function doSpinnyHatAttack()
     local startTime = GetTime()
     local spinVel = 0
@@ -732,7 +415,7 @@
 
     local hurtCooldown = 0
 
-    local dir = VecNormalize(VecSub(GetPlayerTransform(false).pos, GetBodyTransform(hatBody).pos))
+    local dir = VecNormalize(VecSub(GetPlayerTransform(playerId, false).pos, GetBodyTransform(hatBody).pos))
     dir[2] = 0
     dir = QuatRotateVec(QuatEuler(0, rand(-30, 30), 0), dir)
 
@@ -749,7 +432,7 @@
 
         AutoQueryRejectBodies({hatBody, STATE.body})
         if not QueryRaycast(hatPos, Vec(0, -1, 0), 0.5) then
-            dir = VecNormalize(VecSub(GetPlayerTransform(false).pos, GetBodyTransform(hatBody).pos))
+            dir = VecNormalize(VecSub(GetPlayerTransform(playerId, false).pos, GetBodyTransform(hatBody).pos))
             dir[2] = 0
             dir = QuatRotateVec(QuatEuler(0, rand(-30, 30), 0), dir)
         else
@@ -761,10 +444,10 @@
             PlayLoop(SOUND_LOOP_WIZ_HAT_SPIN, hatPos, 1)
         end
 
-        local playerTransform = GetPlayerTransform(false)
+        local playerTransform = GetPlayerTransform(playerId, false)
 
         local nextPos
-        if hurtCooldown > 0 then 
+        if hurtCooldown ~= 0 then 
             nextPos = VecAdd(hatPos, VecScale(dir, 0.05))
         elseif endgame then
             nextPos = VecAdd(hatPos, VecScale(dir, 0.15))
@@ -789,13 +472,13 @@
 
         if math.pow(hatPos[1] - playerTransform.pos[1], 2) + math.pow(hatPos[3] - playerTransform.pos[3], 2) < 2.25 and playerTransform.pos[2] - nextPos[2] < 2 then
             if hurtCooldown == 0 then
-                --SetPlayerHealth(GetPlayerHealth() - 0.2)
-                SetPlayerHealth(GetPlayerHealth() - 0.5)
+                --SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.2)
+                SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.5)
                 hurtCooldown = 0.5
             end
             local dir = VecNormalize(VecSub(playerTransform.pos, hatPos))
             local vel = Vec(40 * dir[1], 8, 40 * dir[3])
-            SetPlayerVelocity(vel)
+            SetPlayerVelocity(playerId, vel)
             dir = QuatRotateVec(QuatEuler(0, rand(135, 225), 0), dir)
         end
 
@@ -813,7 +496,7 @@
     end
     local spawnPos = GetBodyTransform(hatBody).pos
     Delete(hatBody)
-    if STATE.progress ~= FIGHTPROGRESS.ENDGAME and STATE.health > 0 then
+    if STATE.progress ~= FIGHTPROGRESS.ENDGAME and STATE.health ~= 0 then
         RemoveTag(hatShape, "invisible")
     end
     hatSmokeParticle()
@@ -858,8 +541,6 @@
     ParticleGravity(0)
 end
 
---- EXPANDING RINGS ATTACK
-
 function doRingsAttack()
     local startPos = GetBodyTransform(STATE.body).pos
     coRun(0.2)
@@ -898,7 +579,7 @@
             radius = radius + 0.1
         end
 
-        local playerPos = GetPlayerTransform(false).pos
+        local playerPos = GetPlayerTransform(playerId, false).pos
 
         local circumference = 2 * math.pi * radius
         local numParticles = circumference / 0.4
@@ -931,7 +612,7 @@
             end
 
             if AutoVecDist(spawnPos, playerPos) < 0.7 and not damagedThisTick then
-                SetPlayerHealth(GetPlayerHealth() - 0.5)
+                SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.5)
                 damagedThisTick = true
             end
 
@@ -960,13 +641,13 @@
         theta = theta + dT
     end
 
-    local playerPos = GetPlayerTransform(false).pos
+    local playerPos = GetPlayerTransform(playerId, false).pos
     local playerPos2D = Vec(playerPos[1], 0, playerPos[3])
     local arenaPos2D = Vec(STATE.anchor.pos[1], 0, STATE.anchor.pos[3])
     if AutoVecDist(playerPos2D, arenaPos2D) > ARENA_RADIUS * 0.9 then
         local dir = VecNormalize(VecSub(playerPos2D, arenaPos2D))
         local edgePos = VecAdd(arenaPos2D, VecScale(dir, ARENA_RADIUS * 0.89))
-        SetPlayerTransform(Transform(Vec(edgePos[1], playerPos[2], edgePos[3]), GetPlayerTransform(true).rot))
+        SetPlayerTransform(playerId, Transform(Vec(edgePos[1], playerPos[2], edgePos[3]), GetPlayerTransform(playerId, true).rot))
     end
 end
 
@@ -1002,8 +683,6 @@
     ParticleDrag(0.1)
 end
 
---- CRYSTAL MINES ATTACK
-
 function doMinesAttack()
     UiSound(SOUND_VL_UI_MAGICMINES, 1.5)
     coRun(1)
@@ -1012,7 +691,7 @@
         local normalisedDelta = (GetTime() - startTime) / 15
         local bodyTransform = GetBodyTransform(STATE.body)
         local pos = TransformToParentPoint(bodyTransform, STATE.spellSpawnLocal)
-        local playerPos = GetPlayerTransform(false).pos
+        local playerPos = GetPlayerTransform(playerId, false).pos
         local vel = VecNormalize(VecSub(Vec(playerPos[1], STATE.anchor.pos[2] + FLOAT_HEIGHT * 2, playerPos[3]), bodyTransform.pos))
         vel = QuatRotateVec(QuatEuler(0, (math.random() * 130 - 65) * math.max(0.3, (1 - normalisedDelta)), 0), vel)
         vel = VecScale(vel, rand(10, 20))
@@ -1065,7 +744,7 @@
             SetBodyVelocity(body, vel)
         end
 
-        if fuseTime == -1 and (GetTime() - startTime > 30 or AutoVecDist(VecAdd(GetPlayerCameraTransform().pos, Vec(0, -0.9, 0)), lastPos) < 2.5) then
+        if fuseTime == -1 and (GetTime() - startTime > 30 or AutoVecDist(VecAdd(GetPlayerCameraTransform(playerId).pos, Vec(0, -0.9, 0)), lastPos) < 2.5) then
             fuseTime = GetTime()
         end
 
@@ -1106,15 +785,11 @@
     ParticleGravity(-3)
 end
 
---- GNOME SPAWN ATTACK
-
--- I'm gnot a gnelf, I'm gnot a gnoblin, I'm a gnome! And you've been gnomed!
--- Thankfully this one's pretty simple code-wise.
 function doGnomesAttack()
     UiSound(SOUND_VL_UI_DEADGNOMES, 1.5)
     local trigger = STATE.waveTriggers[math.random(1, #STATE.waveTriggers)]
     RemoveTag(trigger, "triggered")
-    SetTriggerTransform(trigger, GetPlayerTransform())
+    SetTriggerTransform(trigger, GetPlayerTransform(playerId))
 
     local startTime = GetTime()
     while GetTime() - startTime < 3 do
@@ -1126,10 +801,9 @@
 
     trigger = STATE.waveTriggers[math.random(1, #STATE.waveTriggers)]
     RemoveTag(trigger, "triggered")
-    SetTriggerTransform(trigger, GetPlayerTransform())
-end
-
---- HUNGRY BOOK ATTACK
+    SetTriggerTransform(trigger, GetPlayerTransform(playerId))
+end
+
 function doChompBookAttack()
     UiSound(SOUND_VL_UI_BOOKBITE, 1.5)
     coRun(1)
@@ -1153,7 +827,7 @@
     local pos = GetBodyTransform(STATE.body).pos
     pos[2] = STATE.anchor.pos[2] - WIZ_OFFSET
 
-    local delta = VecSub(GetPlayerTransform(false).pos, pos)
+    local delta = VecSub(GetPlayerTransform(playerId, false).pos, pos)
     delta[2] = 0;
 
     local dir = VecNormalize(delta)
@@ -1163,7 +837,7 @@
     local doSound = true
 
     while GetTime() - startTime < chaseTime do
-        local delta = VecSub(GetPlayerTransform(false).pos, pos)
+        local delta = VecSub(GetPlayerTransform(playerId, false).pos, pos)
         delta[2] = 0;
 
         dir = VecLerp(dir, VecNormalize(delta), 0.2)
@@ -1220,8 +894,8 @@
         SpawnParticle(VecAdd(particlePos, VecScale(particleDir, rand(-0.85, 0.85))), QuatRotateVec(AutoRandomQuat(90), Vec(0, rand(3, 7), 0)), rand(0.5, 1))
     end
 
-    if GetPlayerTransform(false).pos[2] < particlePos[2] and AutoVecDist(particlePos, GetPlayerTransform(false).pos) < 1.6 then
-        SetPlayerHealth(GetPlayerHealth() - 0.5)
+    if GetPlayerTransform(playerId, false).pos[2] < particlePos[2] and AutoVecDist(particlePos, GetPlayerTransform(playerId, false).pos) < 1.6 then
+        SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.5)
     end
 
     coRun(0.2)
@@ -1251,7 +925,7 @@
     ParticleGravity(-20)
     ParticleDrag(0.1)
 end
---- LASER
+
 function doLaserAttack()
     local colours = {Vec(1, 0, 0), Vec(0, 1, 0), Vec(0, 0, 1), Vec(1, 0, 1), Vec(1, 1, 0), Vec(0, 1, 1), Vec(1, 1, 1)}
 
@@ -1299,7 +973,7 @@
 
             laserTargetPosns[i] = VecAdd(laserTargetPosns[i], VecScale(laserVels[i], 3))
 
-            local dirToPlayer = VecSub(GetPlayerCameraTransform().pos, laserTargetPosns[i])
+            local dirToPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, laserTargetPosns[i])
             dirToPlayer[2] = 0
             dirToPlayer = VecNormalize(dirToPlayer)
             laserVels[i] = VecLerp(laserVels[i], dirToPlayer, 0.003)
@@ -1339,10 +1013,10 @@
     ParticleRadius(0.3 * dTNormalised + 0.2)
     local hurtPlayer = false
     while true do
-        if AutoVecDist(pos, GetPlayerCameraTransform().pos) < 1 and not hurtPlayer then
-            --SetPlayerHealth(GetPlayerHealth() - 0.014 * dTNormalised)
+        if AutoVecDist(pos, GetPlayerCameraTransform(playerId).pos) < 1 and not hurtPlayer then
+            --SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.014 * dTNormalised)
             hurtPlayer = true
-            SetPlayerHealth(GetPlayerHealth() - 0.5)
+            SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.5)
         end
 
         SpawnParticle(pos, Vec(), 0.1)
@@ -1403,8 +1077,6 @@
     ParticleAlpha(1, 0.3)
 end
 
---- CARPET BOMB
-
 function doCarpetBombAttack()
     if STATE.progress ~= FIGHTPROGRESS.ENDGAME then
         coRun(0.5)
@@ -1433,7 +1105,7 @@
         end
 
         local startPos = GetBodyTransform(STATE.body).pos
-        local deltaPlayer = VecSub(GetPlayerTransform(false).pos, GetBodyTransform(STATE.body).pos)
+        local deltaPlayer = VecSub(GetPlayerTransform(playerId, false).pos, GetBodyTransform(STATE.body).pos)
         deltaPlayer[2] = 0
         local dirToPlayer = VecNormalize(deltaPlayer)
         local distToPlayer = VecLength(deltaPlayer)
@@ -1510,15 +1182,6 @@
     end
 end
 
---- UTILITY
---[[ 
-Runs the given function every update until the specified duration
-in seconds has passed.
-The runnable is given the time in seconds this function started at.
-If no function is given, this acts as a sleep(seconds) call.
-Runs longer than around half a second should not use this, as it
-can't handle the transition to endgame.
-]]
 function coRun(seconds, runnable)
     local startTime = GetTime()
     while GetTime() - startTime < seconds do
@@ -1535,4 +1198,252 @@
 
 function lerp(a, b, t)
     return (1 - t) * a + t * b
-end+end
+
+function server.init()
+        SetBool("level.isInSpace", true, true)
+        RegisterListenerTo("wizardhit", "damageHandler")
+        endCameraT = GetLocationTransform(FindLocation("endCameraPos",true))
+        endCamTimer = 0
+    -- Important entities
+        STATE.anchor = GetLocationTransform(FindLocation("wizard_anchor", true))
+        STATE.body = FindBody("wizard_body")
+        STATE.spellSpawnLocal = TransformToLocalPoint(GetBodyTransform(STATE.body), GetLocationTransform(FindLocation("spell_spawn")).pos)
+        STATE.arenaBoundaryShape = FindShape("arena_boundary", true)
+        STATE.dialogueTrigger = FindTrigger("dialogue", true)
+        STATE.waveTriggers = FindTriggers("hordetrigger", true)
+    -- Brain/Animation
+        STATE.actionTimer = 0
+        STATE.move = {}
+        STATE.physState = STATES.WAITING
+        STATE.velocity = Vec()
+        STATE.lastPosition = Vec()
+    -- Sound
+        STATE.currentSpeechHandle = nil
+        STATE.currentSpeechTime = 0
+        STATE.musicPlayed = false
+    -- Level progression
+        STATE.progress = FIGHTPROGRESS.PREFIGHT
+        STATE.health = 1
+        STATE.preambleTP = not GetBool("savegame.mod.skipdialogue")
+    -- Attacks
+        STATE.coroutines = {}
+        STATE.lastAttack = 0
+        STATE.forcedAttacksLeft = {1, 2, 3, 4}
+        STATE.isHatActive = false
+    -- Movement sounds
+        SOUND_LOOP_WIZ_FLYING = LoadLoop("MOD/assets/poopwizard/sounds/WizardFlyLoop01")
+    -- Attack-controlled sounds
+        SOUND_LOOP_WIZ_HAT_SPIN = LoadLoop("MOD/assets/poopwizard/sounds/attacks/WizardHatSpin01.ogg")
+        SOUND_LOOP_LASER_SHOOT = LoadLoop("MOD/assets/poopwizard/sounds/attacks/LaserLoop01.ogg")
+        SOUND_LOOP_LASER_HIT = LoadLoop("MOD/assets/poopwizard/sounds/attacks/LightningLoopStrike01.ogg")
+    -- Physical voicelines
+    -- Dialogue played over the speech system
+        SOUND_VL_DEATH = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/death.ogg")
+        SOUND_VL_DOIT1 = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/doit1.ogg")
+        SOUND_VL_DOIT2 = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/doit2.ogg")
+        SOUND_VL_REFLECTING = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/reflecting.ogg")
+        SOUND_VL_MONOLOGUE = LoadLoop("MOD/assets/poopwizard/sounds/voicelines/monologue.ogg")
+    -- UI voiceline
+        SOUND_VL_UI_DEADGNOMES = "MOD/assets/poopwizard/sounds/attack_voicelines/deadgnomes.ogg"
+        SOUND_VL_UI_HYPERHAT = "MOD/assets/poopwizard/sounds/attack_voicelines/hyperhat.ogg"
+        SOUND_VL_UI_MAGICMINES = "MOD/assets/poopwizard/sounds/attack_voicelines/magicmines.ogg"
+        SOUND_VL_UI_RUBBLERING = "MOD/assets/poopwizard/sounds/attack_voicelines/rubblering.ogg"
+        SOUND_VL_UI_BOOKBITE = "MOD/assets/poopwizard/sounds/attack_voicelines/bookbite.ogg"
+        SOUND_VL_UI_PEW_0 = "MOD/assets/poopwizard/sounds/attack_voicelines/pew0.ogg"
+        SOUND_VL_UI_PEW_1 = "MOD/assets/poopwizard/sounds/attack_voicelines/pew1.ogg"
+        SOUND_VL_UI_RAY_CAST = "MOD/assets/poopwizard/sounds/attack_voicelines/ray cast.ogg"
+        SOUND_VL_UI_BUSTERBOMBS = "MOD/assets/poopwizard/sounds/attack_voicelines/busterbombs.ogg"
+        SOUND_VL_UI_LAUGH = "MOD/assets/poopwizard/sounds/voicelines/laugh.ogg"
+        SOUND_VL_UI_STOPOW = "MOD/assets/poopwizard/sounds/voicelines/stopow.ogg"
+        SOUND_VL_UI_THATHURT = "MOD/assets/poopwizard/sounds/voicelines/thathurt.ogg"
+        SOUND_VL_UI_GETFUCKED = "MOD/assets/poopwizard/sounds/voicelines/getfucked.ogg"
+    -- Music
+        MUSIC_FIGHT = "MOD/assets/poopwizard/sounds/Far_From_Gnome_1.ogg"
+        if not GetBool("savegame.mod.skipdialogue") then SetBool("level.cantDashJump",true, true) end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not STATE.preambleTP and GetBool("savegame.mod.skipdialogue") then
+            SetPlayerTransform(playerId, GetLocationTransform(FindLocation("preamble_skip", true)))
+            STATE.preambleTP = true
+        end
+        handleRotation()
+        handlePosition(dt)
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if STATE.progress == FIGHTPROGRESS.CHARGING then
+            STATE.health = math.min(STATE.health + WIZ_MAX_HEALTH * (GetTimeStep() / 3), WIZ_MAX_HEALTH)
+            if STATE.health == WIZ_MAX_HEALTH then
+                STATE.progress = FIGHTPROGRESS.EASY
+            end
+        end
+        if 
+        STATE.progress == FIGHTPROGRESS.PREFIGHT 
+        and not HasTag(STATE.dialogueTrigger, "triggered") 
+        and IsPointInTrigger(STATE.dialogueTrigger, GetPlayerCameraTransform(playerId).pos)
+        and not GetBool("savegame.mod.skipdialogue")
+         then
+            SetTag(STATE.dialogueTrigger, "triggered")
+            STATE.currentSpeechHandle = SOUND_VL_MONOLOGUE
+        end
+        if STATE.physState == STATES.WAITING and STATE.currentSpeechHandle == nil and AutoVecDist(GetBodyTransform(STATE.body).pos, GetPlayerTransform(playerId, false).pos) < 30 then
+            if GetBool("savegame.mod.skipdialogue") then
+                PlayMusic(MUSIC_FIGHT)
+                startTransitionHandler()
+            else
+                STATE.currentSpeechTime = 0
+                STATE.currentSpeechHandle = SOUND_VL_REFLECTING
+            end
+            SetShapeLocalTransform(STATE.arenaBoundaryShape, Transform(GetShapeLocalTransform(STATE.arenaBoundaryShape).pos, Quat()))
+        end
+        for i = 1, #STATE.coroutines do
+            coroutine.resume(STATE.coroutines[i])
+        end
+        for i = #STATE.coroutines, 1, -1 do
+            if coroutine.status(STATE.coroutines[i]) == "dead" then
+                table.remove(STATE.coroutines, i)
+            end
+        end
+    end
+end
+
+function client.init()
+    SOUND_BOOK_BITE = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardBookBite01.ogg")
+    SOUND_CRYSTAL_LAUNCH = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardCrystalLaunch01.ogg")
+    SOUND_CRYSTAL_TRIGGER = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardCrystalSetOff01.ogg")
+    SOUND_MAGIC_EXPLODE = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardMagicExplodeLayer01.ogg")
+    SOUND_MISSILE_SHOOT = LoadSound("MOD/assets/poopwizard/sounds/attacks/WIzardMissileShoot01.ogg")
+    SOUND_RUBBLE_RING = LoadSound("MOD/assets/poopwizard/sounds/attacks/WizardRubbleRingEmit01.ogg")
+    SOUND_GNOME_SCREAM = LoadSound("MOD/snd/GnomeScream0.ogg")
+    finaleSound = LoadSound("MOD/snd/finale.ogg")
+    SOUND_VL_OW = LoadSound("MOD/assets/poopwizard/sounds/voicelines/ow0.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if STATE.currentSpeechHandle ~= nil and not startTitleCardSequence then
+        if STATE.currentSpeechHandle == SOUND_VL_MONOLOGUE then
+            PlayLoop(STATE.currentSpeechHandle, GetPlayerCameraTransform(playerId).pos, 8)
+        else
+            PlayLoop(STATE.currentSpeechHandle, STATE.anchor.pos, 16)
+        end
+        STATE.currentSpeechTime = STATE.currentSpeechTime + dt
+
+        if STATE.currentSpeechHandle == SOUND_VL_REFLECTING and STATE.currentSpeechTime > 11 and not STATE.musicPlayed then
+            STATE.musicPlayed = true
+            PlayMusic(MUSIC_FIGHT)
+        end
+
+        if 
+        (STATE.currentSpeechHandle == SOUND_VL_DEATH and STATE.currentSpeechTime > 37)
+        or (STATE.currentSpeechHandle == SOUND_VL_DOIT1 and STATE.currentSpeechTime > 18)
+        or (STATE.currentSpeechHandle == SOUND_VL_DOIT2 and STATE.currentSpeechTime > 16)
+        or (STATE.currentSpeechHandle == SOUND_VL_REFLECTING and STATE.currentSpeechTime > 27)
+        or (STATE.currentSpeechHandle == SOUND_VL_MONOLOGUE and STATE.currentSpeechTime > 25)
+        then
+            if STATE.currentSpeechHandle == SOUND_VL_REFLECTING then
+                SetBool("savegame.mod.skipdialogue", true, true)
+                SetBool("level.cantDashJump",false, true)
+                startTransitionHandler()
+            end
+
+            STATE.currentSpeechHandle = nil
+            STATE.currentSpeechTime = 0
+        end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if STATE.health == 0 then
+        if STATE.progress ~= FIGHTPROGRESS.DEAD then
+            STATE.physState = STATES.NOANIM
+            STATE.deathTimer = 0
+            SetBodyTransform(STATE.body, STATE.anchor)
+            STATE.currentSpeechHandle = SOUND_VL_DEATH
+
+            STATE.playedFirst = false
+            STATE.playedSecond = false
+
+            STATE.progress = FIGHTPROGRESS.DEAD
+
+            local shapes = GetBodyShapes(STATE.body)
+            for i = 1, #shapes do
+                SetTag(shapes[i], "invisible")
+            end
+            SetLightEnabled(FindLight(), false)
+            Spawn("MOD/assets/poopwizard/wizard_beaten.xml", TransformToParentTransform(STATE.anchor, Transform(Vec(0, -1, 0), Quat())), true)
+            STATE.hatSmokeLoc = GetLocationTransform(FindLocation("wiz_defeated_smoke", true)).pos
+            StopMusic()
+        else
+            STATE.deathTimer = STATE.deathTimer + GetTimeStep()
+            if STATE.deathTimer > 45 and not STATE.playedFirst then
+                STATE.playedFirst = true
+                STATE.currentSpeechHandle = SOUND_VL_DOIT1
+            end
+            if STATE.deathTimer > 75 and not STATE.playedSecond then
+                STATE.playedSecond = true
+                STATE.currentSpeechHandle = SOUND_VL_DOIT2
+            end
+            if math.random() < 0.2 then
+                defeatedSmokeParticle()
+                SpawnParticle(VecAdd(STATE.hatSmokeLoc, Vec(rand(-0.2, 0.2), 0, rand(-0.2, 0.2))), QuatRotateVec(AutoRandomQuat(20), Vec(0, 0.3, 0)), rand(2, 3))
+            end
+        end
+    else
+        handleBrainCell(dt)
+    end
+end
+
+function client.draw()
+    if startTitleCardSequence then
+        endCamTimer = endCamTimer + dt
+        SetCameraTransform(Transform(endCameraT.pos,QuatRotateQuat(endCameraT.rot,QuatEuler(40-endCamTimer,0,0))),70)
+        UiPush()
+            UiTranslate(UiCenter(), UiMiddle())
+            UiAlign("center middle")
+            UiColor(0,0,0,1)
+            UiPush()
+                backgroundOpacity = 0
+                if endCamTimer < 2.511 and endCamTimer < 10 then backgroundOpacity = 1 end
+                if endCamTimer > 10 then backgroundOpacity = endCamTimer-10 end
+                    UiColor(0,0,0,backgroundOpacity)
+                    UiRect(UiWidth(),UiHeight())
+            UiPop()
+            if endCamTimer >= 2.511 then UiImageBox("MOD/assets/endCard.png",UiWidth(),UiHeight()) end
+        UiPop()
+        if endCamTimer > 11.5 then
+            SetInt("savegame.mod.stats.score.inRun", GetInt("level.score"), true)
+            SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"), true)
+            SetInt("savegame.mod.stats.levelOrder",4, true)
+            SetBool("savegame.mod.skipdialogue", false, true)
+            StartLevel("credits", "MOD/main.xml", "credits", true)
+            return
+        end
+    else
+        UiPush()
+            if STATE.physState ~= STATES.WAITING then
+                UiPush()
+                    UiTranslate(460, 835)
+                    UiFont("MOD/assets/Gemstone.ttf", 24)
+                    UiAlign("left middle")
+                    UiText("Paul, High Hogwash Wizard of the Gnown Universe")
+                UiPop()
+                UiPush()
+                    UiTranslate(460, 850)
+                    UiImageBox("ui/common/box-outline-6.png", 1000, 15, 6, 6)
+                    if STATE.health ~= 0 then
+                        UiTranslate(1, 1)
+                        UiImageBox("MOD/assets/poopwizard/box-solid-4.png", (998 / WIZ_MAX_HEALTH) * STATE.health, 13, 4, 4)
+                    end
+                UiPop()
+            end
+        UiPop()
+    end
+end
+

```

---

# Migration Report: ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/ground.lua
+++ patched/ground.lua
@@ -1,46 +1,39 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
-lava = GetInt("setTo10orAboveIfLava",1)
+#version 2
+function server.init()
+    if lava < 9 then
+    	matRock = CreateMaterial("rock", 0.24, 0.2, 0.16)
+    	matDirt = CreateMaterial("dirt", 0.31, 0.23, 0.15, 1, 0, 0.1)
+    	matGrass1 = CreateMaterial("unphysical", 0.29, 0.37, 0.13, 1, 0, 0.2)
+    	matGrass2 = CreateMaterial("unphysical", 0.28, 0.3, 0.18, 1, 0, 0.2)
+    	matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
+    	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    	matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
+    else
+    	matRock = CreateMaterial("rock", 0.2, 0.2, 0.2)
+    	matDirt = CreateMaterial("dirt", 0.4, 0.4, 0.4, 1, 0, 0.1)
+    	--[[matGrass1 = CreateMaterial("unphysical", 0.29, 0.37, 0.13, 1, 0, 0.2)
+    	matGrass2 = CreateMaterial("unphysical", 0.28, 0.3, 0.18, 1, 0, 0.2)]]
+    	matTarmac = CreateMaterial("masonry", 0.1, 0.1, 0.1, 1, 0, 0.4)
+    	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    	matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
+    end
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h do
+    	local y1 = y0 + maxSize
+    	if y1 > h then y1 = h end
 
-function init()
-	if lava < 9 then
-		matRock = CreateMaterial("rock", 0.24, 0.2, 0.16)
-		matDirt = CreateMaterial("dirt", 0.31, 0.23, 0.15, 1, 0, 0.1)
-		matGrass1 = CreateMaterial("unphysical", 0.29, 0.37, 0.13, 1, 0, 0.2)
-		matGrass2 = CreateMaterial("unphysical", 0.28, 0.3, 0.18, 1, 0, 0.2)
-		matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
-		matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-		matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
-	else
-		matRock = CreateMaterial("rock", 0.2, 0.2, 0.2)
-		matDirt = CreateMaterial("dirt", 0.4, 0.4, 0.4, 1, 0, 0.1)
-		--[[matGrass1 = CreateMaterial("unphysical", 0.29, 0.37, 0.13, 1, 0, 0.2)
-		matGrass2 = CreateMaterial("unphysical", 0.28, 0.3, 0.18, 1, 0, 0.2)]]
-		matTarmac = CreateMaterial("masonry", 0.1, 0.1, 0.1, 1, 0, 0.4)
-		matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-		matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
-	end
-	
-	LoadImage(file)
-	
-	w,h = GetImageSize()
+    	local x0 = 0
+    	while x0 < w do
+    		local x1 = x0 + maxSize
+    		if x1 > w then x1 = w end
+    		Vox(x0, 0, y0)
+    		Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
+    		x0 = x1
+    	end
+    	y0 = y1
+    end
+end
 
-	local maxSize = tileSize
-	
-	local y0 = 0
-	while y0 < h do
-		local y1 = y0 + maxSize
-		if y1 > h then y1 = h end
-
-		local x0 = 0
-		while x0 < w do
-			local x1 = x0 + maxSize
-			if x1 > w then x1 = w end
-			Vox(x0, 0, y0)
-			Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
-			x0 = x1
-		end
-		y0 = y1
-	end
-end

```

---

# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,8 +1,4 @@
---[[
-#include scripts/libraries/Automatic.lua
-#include scripts/libraries/loader.lua
-]]
-
+#version 2
 local file_path = 'scripts/F.lua'
 local reload_times = 0
 
@@ -17,33 +13,28 @@
     end
 end
 
-function init( ... )
+function handleCommand( ... )
+    rawcall(F, 'handleCommand', ... )
+end
+
+function server.init()
     _, F = Loader.File(file_path)
     rawcall(F, 'init', reload_times, ... )
 end
 
-function handleCommand( ... )
-    rawcall(F, 'handleCommand', ... )
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        rawcall(F, 'tick', ... )
+    end
 end
 
-function tick( ... )
-    --[[if InputPressed 'f1' then
-        reload_times = reload_times + 1
-        print(string.format('[%s Reloaded] : [File %s] : [Script Id %s] : [Reload %s]', Loader.mod_id, file_path, AutoGetScriptHandle(), reload_times))
-
-        rawcall(F, 'reload', reload_times)
-        init(true)
-        
-        return
-    end]]
-
-    rawcall(F, 'tick', ... )
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        rawcall(F, 'update', ... )
+    end
 end
 
-function update( ... )
-    rawcall(F, 'update', ... )
+function client.draw()
+    rawcall(F, 'draw', ... )
 end
 
-function draw( ... )
-    rawcall(F, 'draw', ... )
-end
```

---

# Migration Report: merlin\merlin\animation.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/merlin\merlin\animation.lua
+++ patched/merlin\merlin\animation.lua
@@ -1,16 +1,11 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------
-model = {}
-model.animator = 0
-
-
-------------------------------------------------------------------------
-function init()
-	model.animator = FindAnimator()
+#version 2
+function server.init()
+    model.animator = FindAnimator()
 end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        MakeRagdoll(model.animator)
+    end
+end
 
-function tick(dt)
-    MakeRagdoll(model.animator)
-end

```

---

# Migration Report: radio\radio.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/radio\radio.lua
+++ patched/radio\radio.lua
@@ -1,128 +1,4 @@
-radioAlive = true
-radioOn = false
-songToPlay = 1
-volume = 0.5
-
-textcooldown = 300
-counter = 0
---                                            JUST ADD "SONG.OGG" FILES BELOW AND COPY THE FILE IN THE "RADIO" FOLDER THE SCRIPT HANDLES THE REST
-songs ={"gnome_radio_1.ogg",
-        "gnome_radio_2.ogg",
-        "gnome_radio_3.ogg"
-		}
-
-function init()
-  channels = {}
-  for i=1, #songs do
-    channels[i] = LoadLoop(songs[i])
-  end
-  --songToPlay = math.random(#songs)
-  breakSound = LoadSound("radioBreaksSound.ogg")
-  nextSongSound = LoadSound("RadioNextSongSound.ogg")
-  OnOffSound = LoadSound("RadioOnOffSound.ogg")
-  
-  myRadio = FindBody("myradio", false)
-  myButtonRed = FindBody("radioButtonRed", false)
-  myButtonGreen = FindBody("radioButtonGreen", false)
-  myVolUp = FindBody("radioButtonVolUp", false)
-  myVolDown = FindBody("radioButtonVolDown", false)
-  myRandom = FindBody("radioButtonRandom", false)
-  mylast = FindBody("radioButtonUndo", false)
-  songToPlay = math.random(#songs)
-end
-
-
-
-function tick()
-  if radioAlive then
-    t = GetBodyTransform(myRadio)
-    if InputPressed("interact") and GetPlayerInteractBody() == myButtonGreen then
-      PlaySound(nextSongSound, t.pos, 0.2)
-      if radioOn then
-        DrawBodyOutline(myRadio, 1, 1, 1, 1)
-        songToPlay = songToPlay + 1
-        StopMusic()
-        
-        if songToPlay > #songs then
-          songToPlay = 1
-        end
-        --schreib(songs[songToPlay])
-      end
-    end
-    
-    if InputPressed("interact") and GetPlayerInteractBody() == myButtonRed then
-      PlaySound(OnOffSound, t.pos, 0.2)
-      DrawBodyOutline(myRadio, 1, 1, 1, 1)
-      if radioOn then
-        radioOn = false
-        StopMusic()
-      else
-        radioOn = true
-        --schreib(songs[songToPlay])
-      end
-    end
-    
-    if InputPressed("interact") and GetPlayerInteractBody() == myVolUp then
-      PlaySound(nextSongSound, t.pos, 0.2)
-      volume = volume + 0.1
-    end
-    
-    if InputPressed("interact") and GetPlayerInteractBody() == myVolDown then
-      PlaySound(nextSongSound, t.pos, 0.2)
-      volume = volume - 0.1
-    end
-    
-    if volume > 1 then
-      volume = 1
-    end
-    if volume < 0.1 then
-      volume = 0.1
-    end
-    
-    if InputPressed("interact") and GetPlayerInteractBody() == mylast then
-      PlaySound(nextSongSound, t.pos, 0.2)
-      if radioOn then
-        DrawBodyOutline(myRadio, 1, 1, 1, 1)
-        songToPlay = songToPlay - 1
-        StopMusic()
-        if songToPlay < 1 then
-          songToPlay = #songs
-        end
-        --schreib(songs[songToPlay])
-      end
-    end
-    
-    if InputPressed("interact") and GetPlayerInteractBody() == myRandom then
-      if radioOn then
-        playRandom()
-        DrawBodyOutline(myRadio, 1, 1, 1, 1)
-      end
-      PlaySound(nextSongSound, t.pos, 0.2)
-    end
-  
-    if radioOn then
-      PlayLoop(channels[songToPlay], t.pos, volume)
-    end
-    
-    if IsBodyBroken(myRadio) then
-        killRadio()
-        radioAlive = false
-    end
-  end
-  
-  if counter == 0 then
-    for i=0 , 50 do
-      DebugPrint(" ")
-    end
-  end
-    
-  
-  if counter >= 0 then
-    counter = counter - 1
-  end
-end  
-  
-
+#version 2
 function killRadio()
   StopMusic()
   PlaySound(breakSound, t.pos, 0.4)
@@ -130,7 +6,6 @@
     spawnParticles()
   end
 end
-
 
 function spawnParticles()
 
@@ -148,6 +23,7 @@
   ParticleTile(4)
   SpawnParticle(t.pos, v, life)
 end
+
 function playRandom()
   local rand = math.random(#songs)
   while rand == songToPlay do
@@ -165,3 +41,117 @@
   DebugPrint("Now Playing:  " .. text)
 end
 
+function server.init()
+    channels = {}
+    for i=1, #songs do
+      channels[i] = LoadLoop(songs[i])
+    end
+    --songToPlay = math.random(#songs)
+    myRadio = FindBody("myradio", false)
+    myButtonRed = FindBody("radioButtonRed", false)
+    myButtonGreen = FindBody("radioButtonGreen", false)
+    myVolUp = FindBody("radioButtonVolUp", false)
+    myVolDown = FindBody("radioButtonVolDown", false)
+    myRandom = FindBody("radioButtonRandom", false)
+    mylast = FindBody("radioButtonUndo", false)
+    songToPlay = math.random(#songs)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if counter == 0 then
+          for i=0 , 50 do
+            DebugPrint(" ")
+          end
+        end
+        if counter >= 0 then
+          counter = counter - 1
+        end
+    end
+end
+
+function client.init()
+    breakSound = LoadSound("radioBreaksSound.ogg")
+    nextSongSound = LoadSound("RadioNextSongSound.ogg")
+    OnOffSound = LoadSound("RadioOnOffSound.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if radioAlive then
+      t = GetBodyTransform(myRadio)
+      if InputPressed("interact") and GetPlayerInteractBody(playerId) == myButtonGreen then
+        PlaySound(nextSongSound, t.pos, 0.2)
+        if radioOn then
+          DrawBodyOutline(myRadio, 1, 1, 1, 1)
+          songToPlay = songToPlay + 1
+          StopMusic()
+
+          if songToPlay > #songs then
+            songToPlay = 1
+          end
+          --schreib(songs[songToPlay])
+        end
+      end
+
+      if InputPressed("interact") and GetPlayerInteractBody(playerId) == myButtonRed then
+        PlaySound(OnOffSound, t.pos, 0.2)
+        DrawBodyOutline(myRadio, 1, 1, 1, 1)
+        if radioOn then
+          radioOn = false
+          StopMusic()
+        else
+          radioOn = true
+          --schreib(songs[songToPlay])
+        end
+      end
+
+      if InputPressed("interact") and GetPlayerInteractBody(playerId) == myVolUp then
+        PlaySound(nextSongSound, t.pos, 0.2)
+        volume = volume + 0.1
+      end
+
+      if InputPressed("interact") and GetPlayerInteractBody(playerId) == myVolDown then
+        PlaySound(nextSongSound, t.pos, 0.2)
+        volume = volume - 0.1
+      end
+
+      if volume > 1 then
+        volume = 1
+      end
+      if volume < 0.1 then
+        volume = 0.1
+      end
+
+      if InputPressed("interact") and GetPlayerInteractBody(playerId) == mylast then
+        PlaySound(nextSongSound, t.pos, 0.2)
+        if radioOn then
+          DrawBodyOutline(myRadio, 1, 1, 1, 1)
+          songToPlay = songToPlay - 1
+          StopMusic()
+          if songToPlay < 1 then
+            songToPlay = #songs
+          end
+          --schreib(songs[songToPlay])
+        end
+      end
+
+      if InputPressed("interact") and GetPlayerInteractBody(playerId) == myRandom then
+        if radioOn then
+          playRandom()
+          DrawBodyOutline(myRadio, 1, 1, 1, 1)
+        end
+        PlaySound(nextSongSound, t.pos, 0.2)
+      end
+
+      if radioOn then
+        PlayLoop(channels[songToPlay], t.pos, volume)
+      end
+
+      if IsBodyBroken(myRadio) then
+          killRadio()
+          radioAlive = false
+      end
+    end
+end
+

```

---

# Migration Report: scripts\alarm.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\alarm.lua
+++ patched/scripts\alarm.lua
@@ -1,35 +1,43 @@
-enabled = GetBoolParam("enabled", true)
-
-function init()
+#version 2
+function server.init()
     alarms = FindShapes("alarm")
-
     spinny = FindBodies("spinnyalarm")
     spinnyshapes = FindShapes("spinnyshape")
     speed = 360
     alarmLoop = LoadLoop("alarm3-loop.ogg")
     GnomesDetected = LoadLoop("MOD/snd/GnomesDetected.ogg")
     StopMusic()
-
     lamps = FindShapes("lamp", true)
-    SetInt("level.currentLevelInt",2)
+    SetInt("level.currentLevelInt",2, true)
 end
 
-function tick()
-    for i=1, #alarms do
-        --DrawShapeOutline(alarms[i], 1, 0, 0, 1)
-        if enabled then
-            SetShapeEmissiveScale(alarms[i], math.sin(GetTime()*2*i))
-        else
-            SetShapeEmissiveScale(alarms[i], 0)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for i=1, #alarms do
+            --DrawShapeOutline(alarms[i], 1, 0, 0, 1)
+            if enabled then
+                SetShapeEmissiveScale(alarms[i], math.sin(GetTime()*2*i))
+            else
+                SetShapeEmissiveScale(alarms[i], 0)
+            end
+        end
+        for i=1, #spinnyshapes do
+            if not enabled then
+                SetShapeEmissiveScale(spinnyshapes[i], 0)
+            end
+        end
+        for i=1, #lamps do
+            if not enabled then
+                SetShapeEmissiveScale(lamps[i], 1)
+            else
+                SetShapeEmissiveScale(lamps[i], 0)
+            end
         end
     end
+end
 
-    for i=1, #spinnyshapes do
-        if not enabled then
-            SetShapeEmissiveScale(spinnyshapes[i], 0)
-        end
-    end
-
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if enabled then
         for i=1, #spinny do
             local t = GetBodyTransform(spinny[i])
@@ -40,13 +48,5 @@
             end
         end
     end
+end
 
-    
-    for i=1, #lamps do
-        if not enabled then
-            SetShapeEmissiveScale(lamps[i], 1)
-        else
-            SetShapeEmissiveScale(lamps[i], 0)
-        end
-    end
-end
```

---

# Migration Report: scripts\autumn_tool_setup.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\autumn_tool_setup.lua
+++ patched/scripts\autumn_tool_setup.lua
@@ -1,41 +1,13 @@
----@module "shape_anim"
+#version 2
 local shape_anim = Loader.File('scripts/shape_anim.lua')
-
 local module = {}
-
-module.configuration = {
-    tool_body_tag_prefix = 'AUTUMN-TOOL-SETUP-'
-}
-
-module.memory = {}
-
----@type tool[]
-module.memory.tools = {}
----@type string
-module.memory.player_current_tool_id = GetString('game.player.tool')
-module.memory.player_switched_tool_id = false
-module.memory.player_tool_body = GetToolBody()
-module.memory.player_new_tool_body = false
-
---#region Meta
-
----@class tool: { memory:{ anim:shape_animation, [any]:any } }
 local tool_class = {}
-tool_class.__index = tool_class
-    
---#endregion
-
---#region Extra
 
 local function getLastPathComponent(filePath)
     local lastSlashIndex = filePath:match("^.*/()")
     return (lastSlashIndex and filePath:sub(lastSlashIndex) or filePath):sub(1, -3)
 end
 
---#endregion
-
---#region Module
-
 function module.log(title)
     local f = DebugPrint
 
@@ -45,8 +17,6 @@
     f(str)
 end
 
----@return tool
----@nodiscard
 function module.Create()
     local tool = {}
 
@@ -97,9 +67,6 @@
     return new
 end
 
----comment
----@param local_transform transform
----@return transform
 function module.TransformJiggle(local_transform)
     local new_tranform = TransformCopy(local_transform)
     local add_transform = Transform()
@@ -117,7 +84,7 @@
     local walking_bob_rot_ratio_normalized = AutoNormalize(configuration.walking_bob_rot_ratio)
 
     local player_avg_speed = GetPlayerWalkingSpeed()
-    local player_velocity = GetPlayerVelocity()
+    local player_velocity = GetPlayerVelocity(playerId)
     local player_walking_speed_01 = math.min(VecLength(player_velocity), player_avg_speed) / player_avg_speed
 
     local step = GetTime() * math.pi * player_avg_speed * configuration.walking_bob_cycle_scalar
@@ -152,7 +119,7 @@
     return new_tranform
 
     -- local walking_speed = GetPlayerWalkingSpeed()
-    -- local p_vel_raw = GetPlayerVelocity()
+    -- local p_vel_raw = GetPlayerVelocity(playerId)
     -- local p_speed = math.min(VecLength(p_vel_raw), walking_speed) / walking_speed                                                              -- Player Velocity Length scaled from 0 to 1, with 1 being the default movement speed
     -- local p_vel_rel_limit = AutoSwizzle(TransformToLocalVec(GetCameraTransform(), AutoVecRescale(p_vel_raw, p_speed)), 'yxx') -- Removes the z axis and swaps the x and y
     
@@ -175,10 +142,6 @@
     -- return return_velocity
 end
 
----comment
----@param local_transform transform
----@param configuration { camera_sway_pos:vector, camera_sway_rot:vector, movement_bob_pos:vector, movement_bob_rot_x:number, movement_bob_rot_y:number, movement_sway_rot:vector }
----@return transform
 function module.TransformJiggleVelocity(local_transform, configuration)
     local return_velocity = Transform()
     local inverse = AutoQuatInverse(local_transform.rot)
@@ -193,7 +156,7 @@
     end
 
     local walking_speed = GetPlayerWalkingSpeed()
-    local p_vel_raw = GetPlayerVelocity()
+    local p_vel_raw = GetPlayerVelocity(playerId)
     local p_speed = math.min(VecLength(p_vel_raw), walking_speed) / walking_speed                                                              -- Player Velocity Length scaled from 0 to 1, with 1 being the default movement speed
     local p_vel_rel_limit = AutoSwizzle(TransformToLocalVec(GetCameraTransform(), AutoVecRescale(p_vel_raw, p_speed)), 'yxx') -- Removes the z axis and swaps the x and y
     
@@ -216,13 +179,6 @@
     return return_velocity
 end
 
---#endregion
-
---#region Tool Class
-
----comment
----@param information { identification:string?, group:1|2|3|4|5|6|nil, display_name:string?, armature_xml:td_path?, armature_scale:number? }?
----@return tool
 function tool_class:Initialize(information)
     information = information or {}
 
@@ -253,9 +209,9 @@
         self.information.group
     )
 
-    if not start_disabled then SetBool(AutoKey(self.information.registry_key, 'enabled'), true) end
-
-    SetString(AutoKey(self.information.registry_key, 'autumn-ts'), '')
+    if not start_disabled then SetBool(AutoKey(self.information.registry_key, 'enabled'), true, true) end
+
+    SetString(AutoKey(self.information.registry_key, 'autumn-ts'), '', true)
 
     return self
 end
@@ -316,7 +272,7 @@
 end
 
 function tool_class:Useable()
-    return GetPlayerVehicle() == 0 and GetBool('game.player.interactive') and GetBool('game.player.canusetool')
+    return GetPlayerVehicle(playerId) == 0 and GetBool('game.player.interactive') and GetBool('game.player.canusetool')
 end
 
 function tool_class:ChangeSkin(new_xml_path)
@@ -325,6 +281,3 @@
     self:Spawn()
 end
 
---#endregion
-
-return module
```

---

# Migration Report: scripts\credits.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\credits.lua
+++ patched/scripts\credits.lua
@@ -1,4 +1,28 @@
-function init()
+#version 2
+function finishAndSave(xml,layers)
+    if HasKey("savegame.mod.stats.score.Best") then
+        if GetInt("savegame.mod.stats.score.Best") < GetInt("savegame.mod.stats.score.inRun") then
+            SetInt("savegame.mod.stats.score.Best",GetInt("savegame.mod.stats.score.inRun"), true)
+        end
+    else
+        SetInt("savegame.mod.stats.score.Best",GetInt("savegame.mod.stats.score.inRun"), true)
+    end
+    if HasKey("savegame.mod.stats.time.Best") then
+        if GetFloat("savegame.mod.stats.time.Best") < GetFloat("savegame.mod.stats.time.inRun") then
+            SetFloat("savegame.mod.stats.time.Best",GetFloat("savegame.mod.stats.time.inRun"), true)
+        end
+    else
+        SetFloat("savegame.mod.stats.time.Best",GetFloat("savegame.mod.stats.time.inRun"), true)
+    end
+
+    ClearKey("savegame.mod.stats.score.inRun")
+    ClearKey("savegame.mod.stats.time.inRun")
+    ClearKey("savegame.mod.stats.adventureBegun")
+    ClearKey("savegame.mod.stats.levelOrder")
+    StartLevel("", xml,layers)
+end
+
+function server.init()
     camTrans = GetLocationTransform(FindLocation("menucam"))
     credits = {
         "GNOME ZONE",
@@ -19,7 +43,6 @@
         "Teardown Destruction Clips\n\nHe bought me a pizza once. Not a joke.\nSubscribe to his YT.",
         "Thanks for playing!"
     }
-
     options = {
         {id="weaponSway", init_value=1, min=0, max=5, text="Weapon Sway Strength", scoreMult = 1},
         {id="healMult", init_value=1, min=0.2, max=2, text="Healing Multiplier", scoreMult = 1},
@@ -29,7 +52,6 @@
         {id="hitboxSize", init_value=1, min=0.5, max=5, text="Enemy Hitbox Size", scoreMult = -1},
         {id="enemySpeed", init_value=1, min=0.5, max=5, text="Enemy Speed Multiplier", scoreMult = 1},
     }
-
     modifierTable ={
         {name="Dashless",desc="You cannot dash.",multiplier=1.3},
         {name="Glass",desc="Take damage, start over.",multiplier=1.5},
@@ -39,16 +61,14 @@
         {name="Kickback",desc="Gun launches you back when shot.",multiplier=0.8},
         {name="Blackout",desc="Environment is completely dark on all levels. Only artificial lights illuminate.",multiplier=1.1},
     }
-
-    
     lineTime = 5
     line = 0
     timer = 0
-    initT = GetPlayerTransform()
+    initT = GetPlayerTransform(playerId)
 end
 
-function draw(dt)
-    SetPlayerTransform(initT)
+function client.draw()
+    SetPlayerTransform(playerId, initT)
     --SetPlayerZoom(0, 0)
     PlayMusic("MOD/music/credits.ogg")
     SetCameraTransform(camTrans)
@@ -119,31 +139,9 @@
     end
     UiText(credits[line])
 
-    SetBool("game.disablepause",true)
+    SetBool("game.disablepause",true, true)
     if InputPressed("pause") then
         finishAndSave("MOD/main.xml","")
     end
 end
 
-function finishAndSave(xml,layers)
-    if HasKey("savegame.mod.stats.score.Best") then
-        if GetInt("savegame.mod.stats.score.Best") < GetInt("savegame.mod.stats.score.inRun") then
-            SetInt("savegame.mod.stats.score.Best",GetInt("savegame.mod.stats.score.inRun"))
-        end
-    else
-        SetInt("savegame.mod.stats.score.Best",GetInt("savegame.mod.stats.score.inRun"))
-    end
-    if HasKey("savegame.mod.stats.time.Best") then
-        if GetFloat("savegame.mod.stats.time.Best") < GetFloat("savegame.mod.stats.time.inRun") then
-            SetFloat("savegame.mod.stats.time.Best",GetFloat("savegame.mod.stats.time.inRun"))
-        end
-    else
-        SetFloat("savegame.mod.stats.time.Best",GetFloat("savegame.mod.stats.time.inRun"))
-    end
-
-    ClearKey("savegame.mod.stats.score.inRun")
-    ClearKey("savegame.mod.stats.time.inRun")
-    ClearKey("savegame.mod.stats.adventureBegun")
-    ClearKey("savegame.mod.stats.levelOrder")
-    StartLevel("", xml,layers)
-end
```

---

# Migration Report: scripts\dash.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\dash.lua
+++ patched/scripts\dash.lua
@@ -1,139 +1,4 @@
-#include "libraries/Automatic.lua"
-
-function init()
-    cooldown = 1
-    dashSpeed = 30
-    dashSpeed2 = dashSpeed
-
-    maxCharges = 4
-    currentCharges = maxCharges
-    maxCooldown = 1.8
-
-    iSeconds = 0.2
-    iSecond = 0
-
-    dashSound = LoadSound("MOD/snd/Dash0.ogg")
-    munchSound = LoadSound("MOD/snd/munch0.ogg")
-    dashJump = LoadSound("MOD/snd/dashJump.ogg")
-    dashingTimerMax = 1
-    dashingTimer = dashingTimerMax
-
-    jumpframes = 0
-
-    isChargeOn = {}
-    for i=1, maxCharges do
-        table.insert(isChargeOn,true) 
-    end
-end
-
-function tick(dt)
-    if HasVersion('1.5.4') then
-        SetPlayerParam("JumpSpeed", 7)
-    else
-        if floorhit() and InputPressed("jump") and jumpframes <= 0 then
-            jumpframes = 0.25
-        end
-        if jumpframes > 0 then
-            jumpframes = jumpframes - dt
-            local pVel = GetPlayerVelocity()
-            pVel[2] = 0
-            SetPlayerVelocity(VecAdd(pVel,Vec(0,6,0)))
-        end
-    end
-
-    if not GetBool("savegame.mod.modifiers.Dashless") then
-        if GetBool("level.cantDashJump") and maxCooldown == 1.8 then
-            maxCooldown = 6
-        elseif not GetBool("level.cantDashJump") and maxCooldown == 6 then
-            maxCooldown = 1.8
-        end
-        --[[ground pound
-        if currentCharges >= 2 and not downwards then
-            if InputPressed("crouch") and HasVersion('1.5.4') and not IsPlayerGrounded() or InputPressed("crouch") and not HasVersion('1.5.4') and not floorhit() then
-                currentCharges = currentCharges - 2
-                originalSlamPos = GetPlayerCameraTransform().pos
-                downwards = true
-            end
-        end
-        if downwards then
-            if HasVersion('1.5.4') then
-                if not IsPlayerGrounded() then
-                    SetPlayerVelocity(Vec(0,-40,0))
-                else
-                    SetPlayerHealth(1)
-                    local hit, dist, normal, shape = QueryRaycast(GetPlayerCameraTransform().pos, Vec(0,-1,0), 5)
-                    refDir = VecSub(Vec(0,-1,0), VecScale(normal, VecDot(normal, Vec(0,-1,0))*2))
-                    SetPlayerVelocity(VecScale(refDir,30))
-                    downwards = false
-                end
-            end
-        end
-        DebugPrint(downwards)]]
-
-        --dash
-        if LastInputDevice() == 2 then
-            dashInput = "interact"
-            notInteracting = false
-        else
-            dashInput = "shift"
-            if GetPlayerInteractBody() == 0 then
-                notInteracting = true
-            else
-                notInteracting = false
-            end
-        end
-
-        if currentCharges >= 1 then
-            if InputPressed(dashInput) and notInteracting then
-                currentCharges = currentCharges - 1
-                axis = AutoPlayerInputDir(1)
-                dashSpeed2 = dashSpeed
-                playerTrans = GetPlayerTransform()
-                currentLocalVel = TransformToLocalVec(playerTrans, GetPlayerVelocity())
-                PlaySound(dashSound)
-                PlaySound(munchSound,GetCameraTransform().pos,0.65)
-                dashTime = true
-                dashingTimer = dashingTimerMax
-                iSecond = iSeconds*GetFloat("savegame.mod.options.iFrameMult")
-                --eating particles
-                --silly way to replace only needed part
-                for i=1, 3 do
-                    if axis[i] ~= 0 then
-                        currentLocalVel[i] = axis[i] * dashSpeed2
-                    end
-                end
-                newVel = TransformToParentVec(playerTrans, currentLocalVel)
-                --playerParticles(newVel,false)
-            end
-        end
-        if iSecond > 0 then
-            iSecond = iSecond - dt
-            SetBool("level.dashIframesOn",true)
-        elseif iSecond < 0 then
-            iSecond = 0
-            SetBool("level.dashIframesOn",false)
-        end
-        currentCharges = math.min(currentCharges + dt/maxCooldown, maxCharges)
-        if dashTime then
-            if dashingTimer > 0 then
-                dashingTimer = dashingTimer - dt*4
-            else
-                dashTime = false
-            end
-            if dashingTimer > dashingTimerMax/4 then
-                dash(dashSpeed2,dt)
-
-                if InputPressed("jump") and currentCharges >= 2 and not GetBool("level.cantDashJump") then
-                    dashingTimer = -0.01
-                    SetPlayerVelocity(VecScale(GetPlayerVelocity(),1.1))
-                    PlaySound(dashJump)
-                    currentCharges = currentCharges - 2
-                end
-            end
-        end
-    end
-end
-
+#version 2
 function dash(speed,dt)
     playeranimator = GetPlayerAnimator()
     bonenames = GetBoneNames(playeranimator)
@@ -149,17 +14,17 @@
         end
     end
     newVel = TransformToParentVec(playerTrans, currentLocalVel)
-    SetPlayerVelocity(VecScale(newVel,dashingTimer))
+    SetPlayerVelocity(playerId, VecScale(newVel,dashingTimer))
     ShakeCamera(0.35)
 
-    local pVel = VecLength(VecScale(GetPlayerVelocity(),dt/2))
-    local raycastOrigin = VecAdd(GetPlayerTransform().pos,Vec(0,0.5,0))
+    local pVel = VecLength(VecScale(GetPlayerVelocity(playerId),dt/2))
+    local raycastOrigin = VecAdd(GetPlayerTransform(playerId).pos,Vec(0,0.5,0))
     local hit, dist, normal, shape = QueryRaycast(VecAdd(raycastOrigin,Vec(0,0.5,0)), newVel, pVel,0.1)
     --[[local hitpos = VecAdd(raycastOrigin, VecScale(newVel, dist))
     DrawLine(raycastOrigin,hitpos)]]
     if hit then
         dashingTimer = -0.01
-        SetPlayerVelocity(Vec(0,0,0))
+        SetPlayerVelocity(playerId, Vec(0,0,0))
     end
     playerParticles(VecScale(newVel,dashingTimer),true)
 
@@ -182,13 +47,13 @@
     ParticleCollide(1)
     if isDashing then
         for i=1,3 do
-            SpawnParticle(VecAdd(GetPlayerTransform().pos,Vec(mathParticlePos(),mathParticlePos()+i/2,mathParticlePos())), VecAdd(VecScale(playerVel,-1),Vec(mathParticleVel(1),mathParticleVel(1),mathParticleVel(1))), 0.3)
+            SpawnParticle(VecAdd(GetPlayerTransform(playerId).pos,Vec(mathParticlePos(),mathParticlePos()+i/2,mathParticlePos())), VecAdd(VecScale(playerVel,-1),Vec(mathParticleVel(1),mathParticleVel(1),mathParticleVel(1))), 0.3)
         end
     else
         if GetBool("game.thirdperson") then
             ParticleGravity(-5,-64)
             ParticleDrag(0)
-            particlePos = TransformToParentPoint(GetPlayerTransform(),Vec(0,1.6,-0.2))
+            particlePos = TransformToParentPoint(GetPlayerTransform(playerId),Vec(0,1.6,-0.2))
             for i=1,30 do
                 SpawnParticle(VecAdd(particlePos,Vec(0,0,0)), VecScale(Vec(mathParticleVel(5),mathParticleVel(5)+8,mathParticleVel(5)),0.025), 3)
             end
@@ -197,9 +62,149 @@
 end
 
 function mathParticlePos() local value = math.random(-10,10)/60 return value end
+
 function mathParticleVel(multiplier) local value = math.random(-10*multiplier,10*multiplier)/2*multiplier return value end
 
-function draw(dt)
+function floorhit()
+    --QueryRequire("physical static large")
+    --local hit = QueryClosestPoint(GetPlayerTransform(playerId).pos, radius)
+    local hit = QueryRaycast(GetPlayerTransform(playerId).pos, Vec(0, -1, 0), 0.3)
+    return hit
+end
+
+function server.init()
+    cooldown = 1
+    dashSpeed = 30
+    dashSpeed2 = dashSpeed
+    maxCharges = 4
+    currentCharges = maxCharges
+    maxCooldown = 1.8
+    iSeconds = 0.2
+    iSecond = 0
+    dashingTimerMax = 1
+    dashingTimer = dashingTimerMax
+    jumpframes = 0
+    isChargeOn = {}
+    for i=1, maxCharges do
+        table.insert(isChargeOn,true) 
+    end
+end
+
+function client.init()
+    dashSound = LoadSound("MOD/snd/Dash0.ogg")
+    munchSound = LoadSound("MOD/snd/munch0.ogg")
+    dashJump = LoadSound("MOD/snd/dashJump.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if HasVersion('1.5.4') then
+        SetPlayerParam("JumpSpeed", 7)
+    else
+        if floorhit() and InputPressed("jump") and jumpframes <= 0 then
+            jumpframes = 0.25
+        end
+        if jumpframes ~= 0 then
+            jumpframes = jumpframes - dt
+            local pVel = GetPlayerVelocity(playerId)
+            pVel[2] = 0
+            SetPlayerVelocity(playerId, VecAdd(pVel,Vec(0,6,0)))
+        end
+    end
+    if not GetBool("savegame.mod.modifiers.Dashless") then
+        if GetBool("level.cantDashJump") and maxCooldown == 1.8 then
+            maxCooldown = 6
+        elseif not GetBool("level.cantDashJump") and maxCooldown == 6 then
+            maxCooldown = 1.8
+        end
+        --[[ground pound
+        if currentCharges >= 2 and not downwards then
+            if InputPressed("crouch") and HasVersion('1.5.4') and not IsPlayerGrounded() or InputPressed("crouch") and not HasVersion('1.5.4') and not floorhit() then
+                currentCharges = currentCharges - 2
+                originalSlamPos = GetPlayerCameraTransform(playerId).pos
+                downwards = true
+            end
+        end
+        if downwards then
+            if HasVersion('1.5.4') then
+                if not IsPlayerGrounded() then
+                    SetPlayerVelocity(playerId, Vec(0,-40,0))
+                else
+                    SetPlayerHealth(playerId, 1)
+                    local hit, dist, normal, shape = QueryRaycast(GetPlayerCameraTransform(playerId).pos, Vec(0,-1,0), 5)
+                    refDir = VecSub(Vec(0,-1,0), VecScale(normal, VecDot(normal, Vec(0,-1,0))*2))
+                    SetPlayerVelocity(playerId, VecScale(refDir,30))
+                    downwards = false
+                end
+            end
+        end
+        DebugPrint(downwards)]]
+
+        --dash
+        if LastInputDevice() == 2 then
+            dashInput = "interact"
+            notInteracting = false
+        else
+            dashInput = "shift"
+            if GetPlayerInteractBody(playerId) == 0 then
+                notInteracting = true
+            else
+                notInteracting = false
+            end
+        end
+
+        if currentCharges >= 1 then
+            if InputPressed(dashInput) and notInteracting then
+                currentCharges = currentCharges - 1
+                axis = AutoPlayerInputDir(1)
+                dashSpeed2 = dashSpeed
+                playerTrans = GetPlayerTransform(playerId)
+                currentLocalVel = TransformToLocalVec(playerTrans, GetPlayerVelocity(playerId))
+                PlaySound(dashSound)
+                PlaySound(munchSound,GetCameraTransform().pos,0.65)
+                dashTime = true
+                dashingTimer = dashingTimerMax
+                iSecond = iSeconds*GetFloat("savegame.mod.options.iFrameMult")
+                --eating particles
+                --silly way to replace only needed part
+                for i=1, 3 do
+                    if axis[i] ~= 0 then
+                        currentLocalVel[i] = axis[i] * dashSpeed2
+                    end
+                end
+                newVel = TransformToParentVec(playerTrans, currentLocalVel)
+                --playerParticles(newVel,false)
+            end
+        end
+        if iSecond ~= 0 then
+            iSecond = iSecond - dt
+            SetBool("level.dashIframesOn",true, true)
+        elseif iSecond < 0 then
+            iSecond = 0
+            SetBool("level.dashIframesOn",false, true)
+        end
+        currentCharges = math.min(currentCharges + dt/maxCooldown, maxCharges)
+        if dashTime then
+            if dashingTimer ~= 0 then
+                dashingTimer = dashingTimer - dt*4
+            else
+                dashTime = false
+            end
+            if dashingTimer > dashingTimerMax/4 then
+                dash(dashSpeed2,dt)
+
+                if InputPressed("jump") and currentCharges >= 2 and not GetBool("level.cantDashJump") then
+                    dashingTimer = -0.01
+                    SetPlayerVelocity(playerId, VecScale(GetPlayerVelocity(playerId),1.1))
+                    PlaySound(dashJump)
+                    currentCharges = currentCharges - 2
+                end
+            end
+        end
+    end
+end
+
+function client.draw()
     if not GetBool("level.titleCardLoad") and not GetBool("savegame.mod.playerIsDead") and not GetBool("savegame.mod.modifiers.Dashless") then
         --[[UiPush()
             local barWidth = 60
@@ -208,7 +213,7 @@
             UiPush()
                 UiTranslate(0,20)
                 UiText(UiFont("MOD/assets/Gemstone.ttf",20))
-                if currentCharges > 0 then
+                if currentCharges ~= 0 then
                     UiColor(0.8,0.4,0.4)
                 else
                     UiColor(0.4,0.4,0.4)
@@ -280,9 +285,3 @@
     end
 end
 
-function floorhit()
-    --QueryRequire("physical static large")
-    --local hit = QueryClosestPoint(GetPlayerTransform().pos, radius)
-    local hit = QueryRaycast(GetPlayerTransform().pos, Vec(0, -1, 0), 0.3)
-    return hit
-end
```

---

# Migration Report: scripts\F.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\F.lua
+++ patched/scripts\F.lua
@@ -1,136 +1,292 @@
-function init( ... )
-    ---@module "gnome"
+#version 2
+local waveBodies = FindBodies("wave", true)
+
+function reload( ... )
+    TOOL.reload( ... )
+
+    if ToolPickup and type(ToolPickup) == "table" then Delete(ToolPickup.body) end
+
+    for _, g in pairs(GNOMES.gnomes) do
+        g:kill()
+    end
+end
+
+function horde.startWave(wave)
+    --DebugPrint("starting wave "..wave)
+
+    for _, gnomeloc in ipairs(horde.waves[wave]) do
+        --[[local coolPos = VecAdd(GetLocationTransform(gnomeloc).pos, Vec(0, 1, 0))
+        GNOMES.create_gnome(coolPos, ListTags(gnomeloc)[1])
+        PlaySound(TractorBeamZap,coolPos)
+        beamParticle(GetLocationTransform(gnomeloc).pos)]]
+        gnomesSpawn = true
+        spawnNumber = 0
+        spawnTimer = 0.1
+    end
+
+    PlaySound(GNOMES.snd.laugh, GetPlayerTransform(playerId).pos, 0.75, false, 1)
+end
+
+function handleCommand(command)
+
+    local strength, x, y, z = string.match(command, "^explosion ([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+)$")
+    if strength == nil then
+        return
+    end
+    strength = assert(tonumber(strength))
+    x = assert(tonumber(x))
+    y = assert(tonumber(y))
+    z = assert(tonumber(z))
+
+    SetInt("level.lastexplosion.strength", strength, true)
+    SetInt("level.lastexplosion.x", x, true)
+    SetInt("level.lastexplosion.y", y, true)
+    SetInt("level.lastexplosion.z", z, true)
+    --DebugPrint(string.format("explosion with strength %s at Vec(%s, %s, %s)", strength, x, y, z))
+end
+
+function beamParticle(spawnLoc)
+    ParticleReset()
+    ParticleTile(6)
+    ParticleColor(0.5,1,0.5,0,1,0)
+    ParticleRadius(0.4,0)
+    ParticleAlpha(1,0)
+    ParticleGravity(0)
+    ParticleDrag(0,1)
+    ParticleEmissive(5)
+    ParticleRotation(0)
+    ParticleStretch(10)
+    ParticleCollide(0)
+
+    for i=1,550 do
+        local shootT = TransformToParentPoint(Transform(spawnLoc,QuatLookAt(spawnLoc,GetLocationTransform(beamorigin).pos)),Vec(0,0,-i/2))
+        SpawnParticle(shootT,Vec(0,0,0),math.random(1,3)/2)
+    end
+end
+
+function beamParticlePrep(spawnLoc)
+    ParticleReset()
+    ParticleTile(6)
+    ParticleColor(0.5,1,0.5,0,1,0)
+    ParticleRadius(0.1,0)
+    ParticleAlpha(1,0)
+    ParticleGravity(0)
+    ParticleDrag(0,1)
+    ParticleEmissive(5)
+    ParticleRotation(0)
+    ParticleStretch(10)
+    ParticleCollide(0)
+
+    local shootT = TransformToParentVec(Transform(spawnLoc,QuatLookAt(spawnLoc,GetLocationTransform(beamorigin).pos)),Vec(math.random(-20,20)/12,math.random(-20,20)/12,-100))
+    SpawnParticle(spawnLoc,shootT,math.random(1,3)/2)
+end
+
+function server.init()
     GNOMES = Loader.File 'scripts/gnome.lua'
-
     ---@module "shape_anim"
     shape_anim = Loader.File('scripts/shape_anim.lua')
-
     Predicted_Player_Position = Vec()
-
     _, TOOL = Loader.File 'scripts/tool.lua'
     TOOL.init( ... )
     beamorigin = FindLocation("beamorigin",true)
-    TractorBeamZap = LoadSound("MOD/snd/TractorBeamZap.ogg",20)
-    SetInt("level.currentWaveHorde.spawning",1)
-
-    SetString("level.toolKey",TOOL.Tool.information.identification)
-    SetBool(AutoKey('game.tool', TOOL.Tool.information.identification, 'enabled'), false)
-
+    SetInt("level.currentWaveHorde.spawning",1, true)
+    SetString("level.toolKey",TOOL.Tool.information.identification, true)
+    SetBool(AutoKey('game.tool', TOOL.Tool.information.identification, 'enabled'), false, true)
     ---@type false|shape_animation
     ToolPickup = false
 end
 
-function reload( ... )
-    TOOL.reload( ... )
-
-    if ToolPickup and type(ToolPickup) == "table" then Delete(ToolPickup.body) end
-
-    for _, g in pairs(GNOMES.gnomes) do
-        g:kill()
-    end
-end
-
-function tick(dt)
-
-    SetBool('hud.aimdot', false)
-    
-    do -- Disable tools
-        local keys = ListKeys('game.tool')
-        for i=1, #keys do
-            local id = keys[i]
-            if id ~= TOOL.Tool.information.identification then
-                local fk = AutoKey('game.tool', id, 'enabled')
-                SetBool(fk, false)
-            end
-        end
-
-        if not ToolPickup then
-            local l = FindLocation('leveraction_pickup', true)
-            if l > 0 then
-                SetString('game.player.tool', 'none')
-                
-                local t = GetLocationTransform(l)
-                
-                local b = Spawn('<body/>', t, false, false) --[[@as body_handle]] [1]
-                ToolPickup = shape_anim.Create('MOD/assets/leveraction.xml', b, Transform(), 0.4)
-                shape_anim.FakeScaledPhysics(ToolPickup.shapes, b, GetBodyTransform(b), 1)
-                SetTag(b, 'interact')
-                SetBodyDynamic(b, true)
-                SetBodyActive(b, true)
-            else
-                ToolPickup = true
-                SetString('game.player.tool', TOOL.Tool.information.identification)
-            end
-        elseif type(ToolPickup) ~= "boolean" then
-            local alpha = AutoSmoothStep(AutoVecDist(AutoBodyCenter(ToolPickup.body), GetCameraTransform().pos), 8, 3)
-            for i = 1, #ToolPickup.shapes do
-                DrawShapeOutline(ToolPickup.shapes[i], 1, 1, 1, alpha)
-            end
-            
-            if GetPlayerInteractBody() == ToolPickup.body then
-                if InputPressed 'interact' then
-                    SetString('game.player.tool', TOOL.Tool.information.identification)
-                    
-                    local camera = GetCameraTransform()
-                    
-                    local t = TransformToLocalTransform(camera, GetBodyTransform(ToolPickup.body))
-                    local v = QuatRotateVec(camera.rot, GetBodyVelocity(ToolPickup.body))
-
-                    AutoSM_Set(TOOL.Tool.memory.flavor.transform.pos, t.pos)
-                    AutoSM_Set(TOOL.Tool.memory.flavor.transform.rot, t.rot)
-                    AutoSM_SetVelocity(TOOL.Tool.memory.flavor.transform.pos, v)
-
-                    Delete(ToolPickup.body)
-                end
-            end
-        end
-    end
-    
-    local walkingBonus = 0
-    if GetFloat("level.scoreMultiplier") >= 6 then
-        walkingBonus = math.min(GetFloat("level.scoreMultiplier")-6,14)/4
-    end
-    SetPlayerWalkingSpeed(5+walkingBonus)
-    
-    TOOL.tick(dt)
-
-    local camera_transform = GetCameraTransform()
-    local camera_fwd = AutoTransformFwd(camera_transform)
-
-    QueryRequire('physical')
-
-    --[[if InputPressed 'mmb' or (InputDown 'shift' and InputDown 'mmb') then -- REMOVE
-        local choices = {"basic", "lunge", "jump", "explosive", "fat", "big", "small", "spirit"}
-        GNOMES.create_gnome(AutoVecMove(camera_transform.pos, camera_fwd, 8), choices[math.random(#choices)])
-    end]]
-    --DebugWatch('Gnomes', #GNOMES.gnomes)
-    
-    --[[if InputPressed("k") then -- REMOVE
-        horde.active = not horde.active
-    end]]
-
-    playerTrans = GetPlayerTransform()
-    for _, trigger in ipairs(horde.triggers) do
-        if IsPointInTrigger(trigger, playerTrans.pos) then
-            --if has tag "wave" then start only associated wave, else start time based wave system
-            if HasTag(trigger, "wave") then
-                if not HasTag(trigger, "triggered") then
-                    horde.current_wave = tonumber(GetTagValue(trigger, "wave"))
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetBool('hud.aimdot', false, true)
+        do -- Disable tools
+            local keys = ListKeys('game.tool')
+            for i=1, #keys do
+                local id = keys[i]
+                if id ~= TOOL.Tool.information.identification then
+                    local fk = AutoKey('game.tool', id, 'enabled')
+                    SetBool(fk, false, true)
+                end
+            end
+            if not ToolPickup then
+                local l = FindLocation('leveraction_pickup', true)
+                if l ~= 0 then
+                    SetString('game.player.tool', 'none', true)
+
+                    local t = GetLocationTransform(l)
+
+                    local b = Spawn('<body/>', t, false, false) --[[@as body_handle]] [1]
+                    ToolPickup = shape_anim.Create('MOD/assets/leveraction.xml', b, Transform(), 0.4)
+                    shape_anim.FakeScaledPhysics(ToolPickup.shapes, b, GetBodyTransform(b), 1)
+                    SetTag(b, 'interact')
+                    SetBodyDynamic(b, true)
+                    SetBodyActive(b, true)
+                else
+                    ToolPickup = true
+                    SetString('game.player.tool', TOOL.Tool.information.identification, true)
+                end
+            elseif type(ToolPickup) ~= "boolean" then
+                local alpha = AutoSmoothStep(AutoVecDist(AutoBodyCenter(ToolPickup.body), GetCameraTransform().pos), 8, 3)
+                for i = 1, #ToolPickup.shapes do
+                    DrawShapeOutline(ToolPickup.shapes[i], 1, 1, 1, alpha)
+                end
+
+                if GetPlayerInteractBody(playerId) == ToolPickup.body then
+                    if InputPressed 'interact' then
+                        SetString('game.player.tool', TOOL.Tool.information.identification, true)
+
+                        local camera = GetCameraTransform()
+
+                        local t = TransformToLocalTransform(camera, GetBodyTransform(ToolPickup.body))
+                        local v = QuatRotateVec(camera.rot, GetBodyVelocity(ToolPickup.body))
+
+                        AutoSM_Set(TOOL.Tool.memory.flavor.transform.pos, t.pos)
+                        AutoSM_Set(TOOL.Tool.memory.flavor.transform.rot, t.rot)
+                        AutoSM_SetVelocity(TOOL.Tool.memory.flavor.transform.pos, v)
+
+                        Delete(ToolPickup.body)
+                    end
+                end
+            end
+        end
+        local walkingBonus = 0
+        if GetFloat("level.scoreMultiplier") >= 6 then
+            walkingBonus = math.min(GetFloat("level.scoreMultiplier")-6,14)/4
+        end
+        SetPlayerWalkingSpeed(5+walkingBonus)
+        TOOL.tick(dt)
+        local camera_transform = GetCameraTransform()
+        local camera_fwd = AutoTransformFwd(camera_transform)
+        QueryRequire('physical')
+        --[[if InputPressed 'mmb' or (InputDown 'shift' and InputDown 'mmb') then -- REMOVE
+            local choices = {"basic", "lunge", "jump", "explosive", "fat", "big", "small", "spirit"}
+            GNOMES.create_gnome(AutoVecMove(camera_transform.pos, camera_fwd, 8), choices[math.random(#choices)])
+        end]]
+        --DebugWatch('Gnomes', #GNOMES.gnomes)
+        --[[if InputPressed("k") then -- REMOVE
+            horde.active = not horde.active
+        end]]
+        playerTrans = GetPlayerTransform(playerId)
+        for _, trigger in ipairs(horde.triggers) do
+            if IsPointInTrigger(trigger, playerTrans.pos) then
+                --if has tag "wave" then start only associated wave, else start time based wave system
+                if HasTag(trigger, "wave") then
+                    if not HasTag(trigger, "triggered") then
+                        horde.current_wave = tonumber(GetTagValue(trigger, "wave"))
+                        horde.startWave(horde.current_wave)
+                        SetTag(trigger, "triggered")
+                    end
+                else
+                    SetBool("level.searchlight", true, true)
+                    horde.active = true
+                end
+                if not gnomeSoundPlayed2 and not GetBool("level.isInSpace") and not GetBool("savegame.mod.endless") then
+                    --PlaySound(LoadSound("MOD/assets/poopwizard/sounds/voicelines/wave ("..horde.current_wave..").ogg"))
+                    UiSound("MOD/assets/poopwizard/sounds/voicelines/wave (1).ogg",8)
+                    gnomeSoundPlayed2 = true
+                end
+            end
+        end
+        if horde.active and (horde.current_wave <= #horde.waves or horde.endless) then
+            -- DebugWatch("Wave", horde.current_wave)
+
+            if horde.endless and horde.current_wave == #horde.waves then
+
+                local amount = math.min((horde.current_wave + 1) * 2, 35) --limit gnomes because it gets pretty laggy
+                newWaveLocs = {}
+                for i=1, amount do
+                    table.insert(newWaveLocs, horde.allSpawns[math.random(#horde.allSpawns)])
+                end
+
+                table.insert(horde.waves, newWaveLocs)
+                --DebugPrint("added wave")
+            end
+
+            gnomeamount = 0
+            for _, gnome in pairs(GNOMES.gnomes) do
+                gnomeamount = gnomeamount + 1
+            end
+            -- DebugWatch("gnomeamount", gnomeamount)
+            --DebugWatch("horde.timer", horde.timer)
+
+            --highlight remaining gnomes
+            SetInt("level.gnomeCurrentAmount",gnomeamount, true)
+            if gnomeamount <= 5 or GetBool("savegame.mod.options.enemyOutlines") then
+                for _, gnome in pairs(GNOMES.gnomes) do
+                    for i=1, #gnome.memory.anim.shapes do
+                        DrawShapeOutline(gnome.memory.anim.shapes[i], 0, 1, 1, 0.35)
+                    end
+                end
+            end
+
+            if gnomeamount == 0 then
+                horde.timer = horde.timer + dt
+
+                --show spawn positions
+                if horde.current_wave < #horde.waves then
+                    local hordeCurrent = horde.current_wave + 1
+
+                    local waveLocations = horde.waves[hordeCurrent]
+                    for i=1, #waveLocations do
+                        local gnomeloc = waveLocations[i]
+                        beamParticlePrep(GetLocationTransform(gnomeloc).pos)
+                        PointLight(GetLocationTransform(gnomeloc).pos,1,1,1,5)
+                    end
+                end
+            end
+
+            --start next wave
+            if horde.timer >= horde.wave_time then
+                horde.timer = 0
+                horde.current_wave = horde.current_wave + 1
+                SetInt("level.currentWaveHorde.spawning",horde.current_wave, true)
+
+                if horde.current_wave == horde.beam_start_wave then
+                    local t = Transform(VecAdd(playerTrans.pos, Vec(0, -15, 0)), Quat())
+                    SetTriggerTransform(FindTrigger("startbeam", true), t)
+                elseif horde.current_wave == horde.beam_end_wave then
+                    local t = Transform(VecAdd(playerTrans.pos, Vec(0, -15, 0)), Quat())
+                    SetTriggerTransform(FindTrigger("stopbeam", true), t) 
+                end
+
+                if horde.current_wave <= #horde.waves then
                     horde.startWave(horde.current_wave)
-                    SetTag(trigger, "triggered")
-                end
-            else
-                SetBool("level.searchlight", true)
-                horde.active = true
-            end
-            if not gnomeSoundPlayed2 and not GetBool("level.isInSpace") and not GetBool("savegame.mod.endless") then
-                --PlaySound(LoadSound("MOD/assets/poopwizard/sounds/voicelines/wave ("..horde.current_wave..").ogg"))
-                UiSound("MOD/assets/poopwizard/sounds/voicelines/wave (1).ogg",8)
-                gnomeSoundPlayed2 = true
-            end
-        end
-    end
-
+                end
+            end
+            SetInt("level.hordeCurrentWave",horde.current_wave, true)
+
+            --DebugPrint(horde.current_wave)
+            --DebugPrint(#horde.waves)
+
+            if horde.current_wave > #horde.waves then
+                SetBool("level.searchlight", false, true)
+                TriggerEvent("hordeover")
+                --DebugPrint("horde over")
+            end
+        end
+        do
+            local log = AutoPredictPlayerPosition(0.5, false)
+            Predicted_Player_Position = VecCopy(log[#log])
+        end
+        GNOMES.tick(dt)
+        -- AutoInspectWatch(GNOMES.gnomes, 'GNOMES', 0.01, 3)
+        SetInt("level.lastexplosion.strength", 0, true)
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        TOOL.update(dt)
+        GNOMES.update(dt)
+    end
+end
+
+function client.init()
+    TractorBeamZap = LoadSound("MOD/snd/TractorBeamZap.ogg",20)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if not gnomesSpawn then
         local gnomeamount = 0
         for _, gnome in pairs(GNOMES.gnomes) do
@@ -163,247 +319,12 @@
             end
         end
     end
-
-
-    if horde.active and (horde.current_wave <= #horde.waves or horde.endless) then
-        -- DebugWatch("Wave", horde.current_wave)
-
-        if horde.endless and horde.current_wave == #horde.waves then
-
-            local amount = math.min((horde.current_wave + 1) * 2, 35) --limit gnomes because it gets pretty laggy
-            newWaveLocs = {}
-            for i=1, amount do
-                table.insert(newWaveLocs, horde.allSpawns[math.random(#horde.allSpawns)])
-            end
-
-            table.insert(horde.waves, newWaveLocs)
-            --DebugPrint("added wave")
-        end
-
-        gnomeamount = 0
-        for _, gnome in pairs(GNOMES.gnomes) do
-            gnomeamount = gnomeamount + 1
-        end
-        -- DebugWatch("gnomeamount", gnomeamount)
-        --DebugWatch("horde.timer", horde.timer)
-
-        --highlight remaining gnomes
-        SetInt("level.gnomeCurrentAmount",gnomeamount)
-        if gnomeamount <= 5 or GetBool("savegame.mod.options.enemyOutlines") then
-            for _, gnome in pairs(GNOMES.gnomes) do
-                for i=1, #gnome.memory.anim.shapes do
-                    DrawShapeOutline(gnome.memory.anim.shapes[i], 0, 1, 1, 0.35)
-                end
-            end
-        end
-
-        if gnomeamount == 0 then
-            horde.timer = horde.timer + dt
-
-            --show spawn positions
-            if horde.current_wave < #horde.waves then
-                local hordeCurrent = horde.current_wave + 1
-                
-                local waveLocations = horde.waves[hordeCurrent]
-                for i=1, #waveLocations do
-                    local gnomeloc = waveLocations[i]
-                    beamParticlePrep(GetLocationTransform(gnomeloc).pos)
-                    PointLight(GetLocationTransform(gnomeloc).pos,1,1,1,5)
-                end
-            end
-        end
-
-        --start next wave
-        if horde.timer >= horde.wave_time then
-            horde.timer = 0
-            horde.current_wave = horde.current_wave + 1
-            SetInt("level.currentWaveHorde.spawning",horde.current_wave)
-
-            if horde.current_wave == horde.beam_start_wave then
-                local t = Transform(VecAdd(playerTrans.pos, Vec(0, -15, 0)), Quat())
-                SetTriggerTransform(FindTrigger("startbeam", true), t)
-            elseif horde.current_wave == horde.beam_end_wave then
-                local t = Transform(VecAdd(playerTrans.pos, Vec(0, -15, 0)), Quat())
-                SetTriggerTransform(FindTrigger("stopbeam", true), t) 
-            end
-
-            if horde.current_wave <= #horde.waves then
-                horde.startWave(horde.current_wave)
-            end
-        end
-        SetInt("level.hordeCurrentWave",horde.current_wave)
-
-        --DebugPrint(horde.current_wave)
-        --DebugPrint(#horde.waves)
-
-        if horde.current_wave > #horde.waves then
-            SetBool("level.searchlight", false)
-            TriggerEvent("hordeover")
-            --DebugPrint("horde over")
-        end
-    end
-
-    do
-        local log = AutoPredictPlayerPosition(0.5, false)
-        Predicted_Player_Position = VecCopy(log[#log])
-    end
-    
-    GNOMES.tick(dt)
-    -- AutoInspectWatch(GNOMES.gnomes, 'GNOMES', 0.01, 3)
-
-    SetInt("level.lastexplosion.strength", 0)
-    
-end
-
---[[if gnomesSpawn then
-    spawnNumber = spawnNumber + 1
-    local waveLocations = horde.waves[horde.current_wave]
-    DebugPrint(spawnNumber)
-    for i=1, #waveLocations do
-        if i == spawnNumber then
-            GNOMES.create_gnome(VecAdd(GetLocationTransform(waveLocations[i]).pos, Vec(0, 1, 0)), ListTags(waveLocations[i])[1])
-            beamParticle(GetLocationTransform(waveLocations[i]).pos)
-        end
-    end
-    if spawnNumber >= #waveLocations then
-        gnomesSpawn = false
-    end
-end]]
-
-function update(dt)
-    TOOL.update(dt)
-
-    GNOMES.update(dt)
-end
-
-function draw(dt)
+end
+
+function client.draw()
     if horde.current_wave < 12 then
-        
+
     end
     TOOL.draw(dt)
 end
 
---horde wave stuff
-horde = {}
-horde.wave_time = 3.5
-horde.beam_start_wave = 10
-horde.beam_end_wave = 12
-SetBool("savegame.mod.endless", false)
-horde.endless = GetBool("savegame.mod.endless")
-
-horde.active = false
-horde.timer = horde.wave_time
-horde.current_wave = 0
-horde.waves = {}
-horde.triggers = FindTriggers("hordetrigger", true)
-horde.allSpawns = {}
-local waveBodies = FindBodies("wave", true)
-
-for _, bodyindex in ipairs(waveBodies) do
-
-    wave = tonumber(GetTagValue(bodyindex, "wave"))
-    horde.waves[wave] = {}
-
-    i = bodyindex
-    while true do
-        i = i + 1
-        if GetEntityType(i) == "location" and IsHandleValid(i) then
-            table.insert(horde.waves[wave], i)
-            table.insert(horde.allSpawns, i)
-        else
-            break
-        end
-    end
-end
-
-function horde.startWave(wave)
-    --DebugPrint("starting wave "..wave)
-
-    for _, gnomeloc in ipairs(horde.waves[wave]) do
-        --[[local coolPos = VecAdd(GetLocationTransform(gnomeloc).pos, Vec(0, 1, 0))
-        GNOMES.create_gnome(coolPos, ListTags(gnomeloc)[1])
-        PlaySound(TractorBeamZap,coolPos)
-        beamParticle(GetLocationTransform(gnomeloc).pos)]]
-        gnomesSpawn = true
-        spawnNumber = 0
-        spawnTimer = 0.1
-    end
-
-    PlaySound(GNOMES.snd.laugh, GetPlayerTransform().pos, 0.75, false, 1)
-end
-
---stole from thomasims
-function handleCommand(command)
-
-    local strength, x, y, z = string.match(command, "^explosion ([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+)$")
-    if strength == nil then
-        return
-    end
-    strength = assert(tonumber(strength))
-    x = assert(tonumber(x))
-    y = assert(tonumber(y))
-    z = assert(tonumber(z))
-
-    SetInt("level.lastexplosion.strength", strength)
-    SetInt("level.lastexplosion.x", x)
-    SetInt("level.lastexplosion.y", y)
-    SetInt("level.lastexplosion.z", z)
-    --DebugPrint(string.format("explosion with strength %s at Vec(%s, %s, %s)", strength, x, y, z))
-end
---DebugPrint(horde)
-
-function beamParticle(spawnLoc)
-    ParticleReset()
-    ParticleTile(6)
-    ParticleColor(0.5,1,0.5,0,1,0)
-    ParticleRadius(0.4,0)
-    ParticleAlpha(1,0)
-    ParticleGravity(0)
-    ParticleDrag(0,1)
-    ParticleEmissive(5)
-    ParticleRotation(0)
-    ParticleStretch(10)
-    ParticleCollide(0)
-
-    for i=1,550 do
-        local shootT = TransformToParentPoint(Transform(spawnLoc,QuatLookAt(spawnLoc,GetLocationTransform(beamorigin).pos)),Vec(0,0,-i/2))
-        SpawnParticle(shootT,Vec(0,0,0),math.random(1,3)/2)
-    end
-end
-
-function beamParticlePrep(spawnLoc)
-    ParticleReset()
-    ParticleTile(6)
-    ParticleColor(0.5,1,0.5,0,1,0)
-    ParticleRadius(0.1,0)
-    ParticleAlpha(1,0)
-    ParticleGravity(0)
-    ParticleDrag(0,1)
-    ParticleEmissive(5)
-    ParticleRotation(0)
-    ParticleStretch(10)
-    ParticleCollide(0)
-
-    local shootT = TransformToParentVec(Transform(spawnLoc,QuatLookAt(spawnLoc,GetLocationTransform(beamorigin).pos)),Vec(math.random(-20,20)/12,math.random(-20,20)/12,-100))
-    SpawnParticle(spawnLoc,shootT,math.random(1,3)/2)
-end
-
-if not HasVersion('1.5.4') then
-    function IsPlayerGrounded()
-        return AutoRaycast(GetPlayerTransform().pos, Vec(0, -1), 0.025, 0.1).hit
-    end
-
-    function UiCircle(r)
-        UiRect(r*2, r*2)
-    end
-
-    function GetPlayerParam() -- Adjust to set default values based on param
-        return 3
-    end  
-
-    function QueryRejectShapes(shapes)
-        for i=1, #shapes do
-            QueryRejectShape(shapes[i])
-        end
-    end
-end
```

---

# Migration Report: scripts\gnome.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\gnome.lua
+++ patched/scripts\gnome.lua
@@ -1,169 +1,8 @@
+#version 2
 local module = {}
-
----@module "shape_anim"
 local shape_anim = Loader.File 'scripts/shape_anim.lua'
-
----@type gnome[]
-module.gnomes = {}
-module.index = 0
-
-module.snd = {
-    death = LoadSound('MOD/snd/GnomeDeath0.ogg'),
-    charge = LoadSound('MOD/snd/GnomeScream0.ogg'),
-    hop = LoadSound('MOD/snd/GnomeHop.ogg'),
-    land = LoadSound('MOD/snd/GnomeLand.ogg'),
-
-    bite = LoadSound('MOD/snd/GnomeBite.ogg'),
-    laugh = LoadSound('MOD/snd/GnomeLaugh0.ogg'),
-    hurt = LoadSound('MOD/snd/GnomeHurt0.ogg'),
-    killstreakSnd = LoadSound('MOD/snd/killstreak.ogg'),
-}
-
----@type table<string, gnome_config>
-module.gnome_configs = {
-    spirit = {
-        xml = 'MOD/assets/gnome_spirit.xml',
-        health = 1,
-        radius = 0.45,
-        friction = 7.5,
-        jump_randomization = 25,
-        jump_force = { 8, 4.5 },
-        charge_force = { 8, 7 },
-        charging_distance = 4.5,
-        timing = { -- in seconds
-            jump_delay = 1/3,
-            charge_delay = 2/3,
-        },
-        points = 5
-    },
-
-    basic = {
-        xml = 'MOD/assets/gnome_chompski.xml',
-        health = 1,
-        radius = 0.45,
-        friction = 7.5,
-        jump_randomization = 25,
-        jump_force = { 8, 4.5 },
-        charge_force = { 10, 7 },
-        charging_distance = 5,
-        timing = { -- in seconds
-            jump_delay = 1/3,
-            charge_delay = 2/3,
-        },
-        points = 5
-    },
-
-    jump = {
-        xml = 'MOD/assets/gnome_jumpski.xml',
-        health = 1,
-        radius = 0.45,
-        friction = 2.5,
-        jump_randomization = 25,
-        jump_force = { 7.5, 17 },
-        charge_force = { 5.5, 9 },
-        charging_distance = 8,
-        timing = { -- in seconds
-            jump_delay = 0.05,
-            charge_delay = 2/10,
-        },
-        points = 7
-    },
-
-    lunge = {
-        xml = 'MOD/assets/gnome_lungski.xml',
-        health = 1,
-        radius = 0.45,
-        friction = 4,
-        jump_randomization = 25,
-        jump_force = { 4.5, 4 },
-        charge_force = { 14, 8.5 },
-        charging_distance = 16,
-        timing = { -- in seconds
-            jump_delay = 1/2,
-            charge_delay = 1.35,
-        },
-        points = 10
-    },
-
-    small = {
-        xml = 'MOD/assets/gnome_smallski.xml',
-        health = 1,
-        radius = 0.32,
-        friction = 2,
-        jump_randomization = 8,
-        jump_force = { 6.5, 4.5 },
-        charge_force = { 8, 7 },
-        charging_distance = 4.5,
-        timing = { -- in seconds
-            jump_delay = 0.45,
-            charge_delay = 0.55,
-        },
-        points = 12
-    },
-
-    explosive = {
-        xml = 'MOD/assets/gnome_splodeski.xml',
-        health = 1,
-        radius = 0.45,
-        friction = 7.5,
-        jump_randomization = 40,
-        jump_force = { 11, 4.5 },
-        charge_force = { 8, 4.5 },
-        charging_distance = 1,
-        explosive = 1.5,
-        timing = { -- in seconds
-            jump_delay = 1,
-            charge_delay = 1,
-        },
-        points = 15
-    },
-
-    fat = {
-        xml = 'MOD/assets/gnome_chonkski.xml',
-        health = 4,
-        radius = 1.1,
-        friction = 0,
-        jump_randomization = 25,
-        jump_force = { 5, 2 },
-        charge_force = { 13, 4.5 },
-        charging_distance = 1,
-        fat = true,
-        roll = 250, --deg per second
-        timing = { -- in seconds
-            jump_delay = 0,
-            charge_delay = 1,
-        },
-        points = 20
-    },
-
-    big = {
-        xml = 'MOD/assets/gnome_bigski.xml',
-        health = 3,
-        radius = 0.65,
-        friction = 10,
-        jump_randomization = 25,
-        jump_force = { 10, 6.5 },
-        charge_force = { 10, 7 },
-        charging_distance = 4.5,
-        fat = true,
-        timing = { -- in seconds
-            jump_delay = 0.7,
-            charge_delay = 0.65,
-        },
-        points = 15
-    },
-}
-
----@alias gnome_state 'transition'|'startjump'|'jump'|'startcharge'|'charge'
----@alias gnome_config { xml:td_path, health:number, radius:number, friction:number, jump_force: { [1]:number, [2]:number }, charge_force: { [1]:number, [2]:number }, charging_distance:number, timing:{ jump_delay:number, charge_delay:number } }
----@class gnome: { [any]:any, config:gnome_config, memory:{ anim:shape_animation, position:vector, velocity:vector, state:gnome_state, health:number, [any]:any } }
 local gnome_class = {}
-gnome_class.__index = gnome_class
-
----@param origin vector
----@param config_name string
----@param velocity vector?
----@return gnome
+
 function module.create_gnome(origin, config_name, velocity)
     module.index = module.index + 1
 
@@ -218,7 +57,6 @@
         g:tick(dt)
     end
 
-
     -- local eyes = FindShapes('gnome_eye', true)
     -- for i=1, #eyes do
     --     DrawShapeHighlight(eyes[i], 10)
@@ -231,11 +69,6 @@
     end
 end
 
----@param origin any
----@param direction any
----@param distance any
----@return gnome? gnome
----@return { hit:boolean, intersections:{ [1]:vector, [2]:vector }, normals:{ [1]:vector, [2]:vector }, dists:{ [1]:number, [2]:number } } raycast_data
 function module.raycast(origin, direction, distance)
     local gnome_sorted = module.gnomes_by_distance(origin)
     
@@ -261,8 +94,6 @@
     end
 end
 
----@param origin any
----@return { gnome:gnome, distance:number, position:vector }[]
 function module.gnomes_by_distance(origin)
     local gnome_sorted = {}
     local index = 0
@@ -382,7 +213,7 @@
         end
     end
 
-    if division > 0 then
+    if division ~= 0 then
         self:set_position(AutoVecMove(pos, total_position_resolvement, 1))
         self:set_velocity(AutoVecMove(vel, total_velocity_resolvement, 1))
     end
@@ -397,7 +228,7 @@
     local state_change_time = Time - self.memory.time.state_change
 
     local gnome_pos = self:get_position()
-    local diff_to_player = VecSub(GetPlayerTransform().pos, gnome_pos)
+    local diff_to_player = VecSub(GetPlayerTransform(playerId).pos, gnome_pos)
     local diff_to_player_no_y = AutoVecSubsituteY(diff_to_player, 0)
 
     local diff_to_prediction = VecSub(Predicted_Player_Position, gnome_pos)
@@ -457,11 +288,11 @@
     end
 
     do
-        local player_center = VecAdd(GetPlayerTransform().pos, Vec(0, 1.8/2))
+        local player_center = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1.8/2))
         if Time - self.memory.time.bite >= 0.5 and AutoVecDistNoY(pos, player_center) < 1 + self.config.radius and AutoDist(pos[2], player_center[2]) < 1.8/2 + self.config.radius then
             self.memory.time.bite = Time
 
-            SetPlayerHealth(0.5)
+            SetPlayerHealth(playerId, 0.5)
 
             PlaySound(module.snd.bite, self:get_position(), 0.75, false, 1/ (self.config.radius / 0.45))
 
@@ -479,34 +310,26 @@
     if self:get_position()[2] < -5 then self:kill() end
 end
 
----@return vector
 function gnome_class:get_position()
     return VecCopy(self.memory.position)
 end
 
----@param position vector
 function gnome_class:set_position(position)
     self.memory.position = VecCopy(position)
 end
 
----@param add vector
----@param scalar number?
 function gnome_class:add_position(add, scalar)
     self.memory.position = AutoVecMove(self.memory.position, add, scalar or 1)
 end
 
----@return vector
 function gnome_class:get_velocity()
     return VecCopy(self.memory.velocity)
 end
 
----@param velocity vector
 function gnome_class:set_velocity(velocity)
     self.memory.velocity = VecCopy(velocity)
 end
 
----@param add vector
----@param scalar number?
 function gnome_class:add_velocity(add, scalar)
     self.memory.velocity = AutoVecMove(self.memory.velocity, add, scalar or 1)
 end
@@ -547,7 +370,7 @@
 end
 
 function gnome_class:kill()
-    SetInt("level.gnomesKilled",GetInt("level.gnomesKilled")+1)
+    SetInt("level.gnomesKilled",GetInt("level.gnomesKilled")+1, true)
     --shard gibs
     if self.config.fat then
         minGib = 6
@@ -624,10 +447,6 @@
     end
 end
 
---#region collision
-
----@param origin vector
----@return { angle:number, origin:vector, query:{ hit:boolean, point:vector, normal:vector, shape:shape_handle, body:body_handle, dist:number, dir:vector, dot:number, reflection:vector }}
 function createCollision(origin, radius)
     local collision_information = {}
     
@@ -651,9 +470,6 @@
     return collision_information
 end
 
----@param correction_scaler number Usually a multiple offset `dt`, however in a perfect world `1` would be ideal.
----@return vector positional_resolvement
----@return vector velocity_resolvement
 function resolveCollision(current_velocity, collision_information, correction_scaler, friction)
     local positional_resolvement, velocity_resolvement = Vec(), Vec()
     
@@ -683,6 +499,3 @@
     return positional_resolvement, velocity_resolvement
 end
 
---#endregion
-
-return module
```

---

# Migration Report: scripts\gnome_beam.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\gnome_beam.lua
+++ patched/scripts\gnome_beam.lua
@@ -1,154 +1,5 @@
-#include "/libraries/Automatic.lua"
-
+#version 2
 local enabled = GetBoolParam('Enabled', true)
-baseAccel = GetFloatParam("baseAccel", 0.185)
-maxSpeed = GetFloatParam("maxSpeed", 0.28)
-laserRadius = GetFloatParam("laserRadius", 1)
-doIntroExplosion = GetBoolParam("explosion", true)
-screenshotMode = GetBoolParam("screenshotMode", false)
-
-function init()
-	--baseAccel = 0.175
-	--maxSpeed = 0.3
-	--laserRadius = 1
-	
-
-	startTrigger = FindTrigger("startbeam")
-	stopTrigger = FindTrigger("stopbeam")
-	envTrigger = FindTrigger("envChange")
-	laserPos = GetLocationTransform(FindLocation("beamstartpoint")).pos
-	gnomeShipPos = GetLocationTransform(FindLocation("beamorigin")).pos
-	gnomeship = FindShape("gnomeship",true)
-	laserSprite = LoadSprite("MOD/assets/laser.png")
-	introDone = false
-	active = false
-	allowMusicToggle = false
-	laserVel = Vec(0, 0, 0)
-
-	laserLoop = LoadLoop("MOD/snd/GnomeBeamLoop.ogg", 500.0)
-	laserActivate = LoadSound("MOD/snd/GnomeBeamActivated.ogg", 100)
-	beamPrime = LoadSound("MOD/snd/GnomeBeamInitialFire.ogg", 100)
-	laserActivateExplode = LoadSound("MOD/snd/ElectricalTowerExplosion1.ogg", 100.0)
-	herehumans = LoadSound("MOD/assets/poopwizard/sounds/voicelines/herehumans.ogg", 500.0)
-
-	beamLight = FindBody("beamLight")
-	realLight4Beam = FindLight("realLight4Beam")
-
-	thunderSound = LoadSound("thunder-strike.ogg")
-
-	hasPlayedIntroExplosion = false
-
-	primeTimer = 4
-	if screenshotMode then
-		active = true
-		SetValue("primeTimer",-1,"linear",primeTimer)
-		PlaySound(laserActivate)
-		SetLightIntensity(realLight4Beam, 500)
-	end
-end
-
-function tick(dt)
-	if not enabled then return end
-	
-	playerTrans = GetPlayerTransform()
-
-	if active then
-		allowMusicToggle = true
-		if primeTimer < 0 then 
-			if not hasPlayedIntroExplosion and doIntroExplosion then
-				--DebugPrint("Playing intro explosion")
-				introExplosionFX()
-				local light = FindLight("laseractivated", true)
-				SetLightEnabled(light, true)
-				--DebugPrint(light)
-				PlaySound(beamPrime)
-				hasPlayedIntroExplosion = true
-			end
-			fireLaser() 
-		end
-
-		if IsPointInTrigger(stopTrigger, playerTrans.pos) then
-			active = false
-			allowMusicToggle = false
-			SetBodyTransform(beamLight, Transform(Vec(1000,1000,1000), QuatEuler(0,0,0)))
-			SetLightIntensity(realLight4Beam,0)
-			Delete(stopTrigger)
-		end
-		
-	else
-		if IsPointInTrigger(startTrigger, playerTrans.pos) then
-			active = true
-			SetValue("primeTimer",-1,"linear",primeTimer)
-			PlaySound(laserActivate)
-			SetLightIntensity(realLight4Beam, 500)
-			Delete(startTrigger)
-		end
-	end
-	if not weatherChanged then
-		--SetBool("hud.disable",true)
-		if IsPointInTrigger(envTrigger, playerTrans.pos) then
-			--SetBool("hud.disable",false)
-			if not GetBool("savegame.mod.modifiers.Blackout") then
-				local Environment = {
-					ambience = { "outdoor/rain_heavy.ogg", 1 },
-					ambient = 1,
-					ambientexponent = 1.25,
-					brightness = 1,
-					constant = {0, 0, 0},
-					exposure = {1, 5},
-					fogcolor = {0.02, 0.03, 0.04},
-					fogparams = {-50, 150, 0.5, 4},
-					fogscale = 1,
-					nightlight = true,
-					puddleamount = 0.3,
-					puddlesize = 0.5,
-					rain = 0.75,
-					skybox = "cloudy.dds",
-					skyboxbrightness = 0.1,
-					skyboxrot = 0,
-					skyboxtint = {0.02, 0.03, 0.04},
-					slippery = 0,
-					sunbrightness = 0,
-					suncolortint = {1,1,1},
-					sundir = {0,0,0},
-					sunfogscale = 1,
-					sunglare = 1,
-					sunlength = 32,
-					sunspread = 0,
-					waterhurt = 0,
-					wetness = 0,
-					wind = {0,0,0},
-				}
-				AutoSetEnvironment(Environment)
-			end
-			weatherChanged = true
-			SetBool("level.weatherActivated",weatherChanged)
-			ShakeCamera(0.8)
-			--PlaySound(herehumans,GetPlayerCameraTransform().pos,15)
-			UiSound("thunder-strike.ogg",2)
-			UiSound("MOD/assets/poopwizard/sounds/voicelines/herehumans.ogg",4)
-			RemoveTag(gnomeship,"invisible")
-		end
-	end
-	if allowMusicToggle and GetBool("level.carChase") then
-		if not introStarted then
-			introStarted = true
-			introtimer = 0
-		end
-
-		if not introDone then
-			PlayMusic("MOD/music/chaseIntro.ogg")
-			if GetMusicProgress() >= 10.23 then
-				introDone = true
-			end
-		else
-			PlayMusic("MOD/music/chase.ogg")
-		end
-	end
-end
-
-function draw()
-end
 
 function introExplosionFX()
 	-- Find the location for the explosion
@@ -193,7 +44,7 @@
 	local dir = VecNormalize(toPlayer)
 	local dist = VecLength(toPlayer)
 
-	if VecLength(GetPlayerVelocity()) < 6 then --make it so you cant just sit in place
+	if VecLength(GetPlayerVelocity(playerId)) < 6 then --make it so you cant just sit in place
 		laserAccel = baseAccel * 3
 	else
 		laserAccel = baseAccel
@@ -202,7 +53,6 @@
 	laserVel = VecAdd(laserVel, VecScale(dir, laserAccel * GetTimeStep()))
 	laserVel = clampVec(laserVel, 0, maxSpeed)
 	laserPos = VecAdd(laserPos, laserVel)
-
 
 	QueryRejectBody(beamLight)
 	--do other laser stuff
@@ -231,7 +81,7 @@
 		DrawSpriteLine(laserSprite, gnomeShipPos, VecAdd(hitPoint, VecScale(laserDir, 10)), ((laserRadius*3)+(math.random()*5)), 1, 3, 3, 1, true, true)
 
 		if VecLength(VecSub(hitPoint, playerTrans.pos)) < laserRadius*2 then
-			SetPlayerHealth(GetPlayerHealth()-0.4)
+			SetPlayerHealth(playerId, GetPlayerHealth(playerId)-0.4)
 		end
 	end
 end
@@ -293,4 +143,139 @@
     local length = VecLength(VecSub(p0, p1))
     local w, h = diameter or 1, length
     return DrawSprite(sprite, trans, w, h, r or 0.5, g or 0.5, b or 0.5, a or 1, depth == nil and true or depth, additive)
-end+end
+
+function server.init()
+    startTrigger = FindTrigger("startbeam")
+    stopTrigger = FindTrigger("stopbeam")
+    envTrigger = FindTrigger("envChange")
+    laserPos = GetLocationTransform(FindLocation("beamstartpoint")).pos
+    gnomeShipPos = GetLocationTransform(FindLocation("beamorigin")).pos
+    gnomeship = FindShape("gnomeship",true)
+    laserSprite = LoadSprite("MOD/assets/laser.png")
+    introDone = false
+    active = false
+    allowMusicToggle = false
+    laserVel = Vec(0, 0, 0)
+    laserLoop = LoadLoop("MOD/snd/GnomeBeamLoop.ogg", 500.0)
+    beamLight = FindBody("beamLight")
+    realLight4Beam = FindLight("realLight4Beam")
+    hasPlayedIntroExplosion = false
+    primeTimer = 4
+end
+
+function client.init()
+    laserActivate = LoadSound("MOD/snd/GnomeBeamActivated.ogg", 100)
+    beamPrime = LoadSound("MOD/snd/GnomeBeamInitialFire.ogg", 100)
+    laserActivateExplode = LoadSound("MOD/snd/ElectricalTowerExplosion1.ogg", 100.0)
+    herehumans = LoadSound("MOD/assets/poopwizard/sounds/voicelines/herehumans.ogg", 500.0)
+    thunderSound = LoadSound("thunder-strike.ogg")
+    if screenshotMode then
+    	active = true
+    	SetValue("primeTimer",-1,"linear",primeTimer)
+    	PlaySound(laserActivate)
+    	SetLightIntensity(realLight4Beam, 500)
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if not enabled then return end
+
+    playerTrans = GetPlayerTransform(playerId)
+
+    if active then
+    	allowMusicToggle = true
+    	if primeTimer < 0 then 
+    		if not hasPlayedIntroExplosion and doIntroExplosion then
+    			--DebugPrint("Playing intro explosion")
+    			introExplosionFX()
+    			local light = FindLight("laseractivated", true)
+    			SetLightEnabled(light, true)
+    			--DebugPrint(light)
+    			PlaySound(beamPrime)
+    			hasPlayedIntroExplosion = true
+    		end
+    		fireLaser() 
+    	end
+
+    	if IsPointInTrigger(stopTrigger, playerTrans.pos) then
+    		active = false
+    		allowMusicToggle = false
+    		SetBodyTransform(beamLight, Transform(Vec(1000,1000,1000), QuatEuler(0,0,0)))
+    		SetLightIntensity(realLight4Beam,0)
+    		Delete(stopTrigger)
+    	end
+
+    else
+    	if IsPointInTrigger(startTrigger, playerTrans.pos) then
+    		active = true
+    		SetValue("primeTimer",-1,"linear",primeTimer)
+    		PlaySound(laserActivate)
+    		SetLightIntensity(realLight4Beam, 500)
+    		Delete(startTrigger)
+    	end
+    end
+    if not weatherChanged then
+    	--SetBool("hud.disable",true, true)
+    	if IsPointInTrigger(envTrigger, playerTrans.pos) then
+    		--SetBool("hud.disable",false, true)
+    		if not GetBool("savegame.mod.modifiers.Blackout") then
+    			local Environment = {
+    				ambience = { "outdoor/rain_heavy.ogg", 1 },
+    				ambient = 1,
+    				ambientexponent = 1.25,
+    				brightness = 1,
+    				constant = {0, 0, 0},
+    				exposure = {1, 5},
+    				fogcolor = {0.02, 0.03, 0.04},
+    				fogparams = {-50, 150, 0.5, 4},
+    				fogscale = 1,
+    				nightlight = true,
+    				puddleamount = 0.3,
+    				puddlesize = 0.5,
+    				rain = 0.75,
+    				skybox = "cloudy.dds",
+    				skyboxbrightness = 0.1,
+    				skyboxrot = 0,
+    				skyboxtint = {0.02, 0.03, 0.04},
+    				slippery = 0,
+    				sunbrightness = 0,
+    				suncolortint = {1,1,1},
+    				sundir = {0,0,0},
+    				sunfogscale = 1,
+    				sunglare = 1,
+    				sunlength = 32,
+    				sunspread = 0,
+    				waterhurt = 0,
+    				wetness = 0,
+    				wind = {0,0,0},
+    			}
+    			AutoSetEnvironment(Environment)
+    		end
+    		weatherChanged = true
+    		SetBool("level.weatherActivated",weatherChanged, true)
+    		ShakeCamera(0.8)
+    		--PlaySound(herehumans,GetPlayerCameraTransform(playerId).pos,15)
+    		UiSound("thunder-strike.ogg",2)
+    		UiSound("MOD/assets/poopwizard/sounds/voicelines/herehumans.ogg",4)
+    		RemoveTag(gnomeship,"invisible")
+    	end
+    end
+    if allowMusicToggle and GetBool("level.carChase") then
+    	if not introStarted then
+    		introStarted = true
+    		introtimer = 0
+    	end
+
+    	if not introDone then
+    		PlayMusic("MOD/music/chaseIntro.ogg")
+    		if GetMusicProgress() >= 10.23 then
+    			introDone = true
+    		end
+    	else
+    		PlayMusic("MOD/music/chase.ogg")
+    	end
+    end
+end
+

```

---

# Migration Report: scripts\gnome_light.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\gnome_light.lua
+++ patched/scripts\gnome_light.lua
@@ -1,36 +1,4 @@
-baseAccel = GetFloatParam("baseAccel", 0.1)
-maxSpeed = GetFloatParam("maxSpeed", 0.1)
-
-function init()
-    distFromCamera = 15
-
-    body = FindBody("lightbody")
-    origin = FindLocation("fakeorigin")
-    targetPos = GetLocationTransform(FindLocation("lightstartpos")).pos
-    lightVel = Vec(0, 0, 0)
-end
-
-function tick()
-    if GetBool("level.searchlight") and GetInt("level.currentWaveHorde.spawning") >= 7 then
-        local camPos = GetPlayerCameraTransform().pos
-        local originPos = GetLocationTransform(origin).pos
-
-        --calculate where light is pointing
-        local toPlayer = VecNormalize(VecSub(camPos, targetPos))
-        lightVel = VecAdd(lightVel, VecScale(toPlayer, baseAccel * GetTimeStep()))
-        lightVel = clampVec(lightVel, 0, maxSpeed)
-        targetPos = VecAdd(targetPos, lightVel)
-
-        --calculate where light entity is
-        local toOrigin = VecNormalize(VecSub(originPos, camPos))
-        local pos = VecAdd(camPos, VecScale(toOrigin, distFromCamera))
-
-        SetBodyTransform(body, Transform(pos, QuatLookAt(targetPos, pos)))
-    else
-        SetBodyTransform(body, Transform(Vec(0, -100, 0)))
-    end
-end
-
+#version 2
 function clampVec(vec, minlen, maxlen)
 	local dir = VecNormalize(vec)
 	local len = VecLength(vec)
@@ -38,4 +6,36 @@
 	len = math.max(math.min(maxlen, len), minlen)
 
 	return VecScale(dir, len)
-end+end
+
+function server.init()
+    distFromCamera = 15
+    body = FindBody("lightbody")
+    origin = FindLocation("fakeorigin")
+    targetPos = GetLocationTransform(FindLocation("lightstartpos")).pos
+    lightVel = Vec(0, 0, 0)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetBool("level.searchlight") and GetInt("level.currentWaveHorde.spawning") >= 7 then
+            local camPos = GetPlayerCameraTransform(playerId).pos
+            local originPos = GetLocationTransform(origin).pos
+
+            --calculate where light is pointing
+            local toPlayer = VecNormalize(VecSub(camPos, targetPos))
+            lightVel = VecAdd(lightVel, VecScale(toPlayer, baseAccel * GetTimeStep()))
+            lightVel = clampVec(lightVel, 0, maxSpeed)
+            targetPos = VecAdd(targetPos, lightVel)
+
+            --calculate where light entity is
+            local toOrigin = VecNormalize(VecSub(originPos, camPos))
+            local pos = VecAdd(camPos, VecScale(toOrigin, distFromCamera))
+
+            SetBodyTransform(body, Transform(pos, QuatLookAt(targetPos, pos)))
+        else
+            SetBodyTransform(body, Transform(Vec(0, -100, 0)))
+        end
+    end
+end
+

```

---

# Migration Report: scripts\health.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\health.lua
+++ patched/scripts\health.lua
@@ -1,113 +1,223 @@
-#include "/mainmenu.lua"
-scoreBoard = GetBoolParam("scoreboard",true)
-
-function init()
-    maxHealth = 5
-    iSeconds = 1
-
-    health = maxHealth
-    iSecond = 0
-
-    --score
-    multiplierDecay = 0.32 	--per second
-    multiplierIncrease = 0.425 --per kill
-	pauseTime = 5			--how long to stop decay after kill
-    pointsToHealInit = 20
-
-    multtext = {}
-    multtext[0] = ""
-    multtext[2] = "gnot bad"
-    multtext[4] = "Gnice."
-    multtext[6] = "Gnometacular.."
-    multtext[8] = "GNASTY!"
-    multtext[10] = "GNOMERGENCY!!"
-    multtext[12] = "RECKGNOMING!!!"
-    multtext[14] = "JUDGNOMENT DAY!!!!"
-    multtext[16] = "GNOMAGEDDON!!!!!"
-    multtext[18] = "APOCGNOMYPSE!!!!!!"
-    multtext[20] = "GNOMECIDE!!!!!!!"
-
-	RegisterListenerTo("gnomeHurt", "AddScore")
-
-
-    if GetInt("savegame.mod.stats.levelOrder")+1 == GetInt("level.currentLevelInt") and GetBool("savegame.mod.stats.adventureBegun") then
-        fraud = false
-    else
-        fraud = true
-    end
-
-    if fraud then
-        score = 0
-    else
-        score = GetInt("savegame.mod.stats.score.inRun")
-        --SetInt("savegame.mod.stats.score.inRun", 0)
-    end
-
-	multiplier = 1
+#version 2
+function hurtPlayer()
+    if GetBool("savegame.mod.modifiers.Glass") then StartLevel("","MOD/main.xml") end
+    health = health - 1
+    iSecond = iSeconds*GetFloat("savegame.mod.options.iFrameMult")
+    ShakeCamera(0.5)
+
+    multiplier = 0
     combo = 0
-	pauseTimer = pauseTime
-
-    MaxhitTimer = 1
-    hitTimer = MaxhitTimer
-
-    pointsSinceHeal = 0
-    dead = false
-end
-
-function tick(dt)
-    SetInt("level.score", score)
-    pointsToHeal = pointsToHealInit
-    pointsToHeal = pointsToHeal*GetFloat("savegame.mod.options.healMult")
-
-    local playerTool = GetString("game.player.tool")
-    SetFloat("game.tool.gnome-weapon.ammo",99999)
-
-    --SetBool("level.gnomeInstakillAll",false)
-    --if InputPressed("i") then SetBool("level.gnomeInstakillAll",true) end
-    SetInt("game.fire.maxcount", 30)
-
-    hp = GetPlayerHealth()
-
+    pointsSinceHeal = 0 --reset heal progress
+end
+
+function AddScore(args)
     if not dead then
-        if health > 0 then
-            if not GetBool("level.dashIframesOn") then
-                if iSecond <= 0 then
-                    if hp < 0.8 then
-                        hurtPlayer()
-                    end
-                else
-                    iSecond = iSecond - dt
+        gnomePoints = tonumber(args)
+
+        combo = combo + 1
+	    multiplier = multiplier + multiplierIncrease
+
+	    score = score + (gnomePoints * multiplier)
+        pointsSinceHeal = pointsSinceHeal + gnomePoints
+
+        if pointsSinceHeal >= pointsToHeal then
+            health = math.min(health + 1, maxHealth)
+            pointsSinceHeal = pointsSinceHeal - pointsToHeal
+        end
+
+	    pauseTimer = 0
+    end
+end
+
+function drawScoreThing()
+    UiPush()
+        UiTranslate(UiCenter(), UiHeight() * 0.04)
+        UiAlign("center middle")
+        UiTranslate(-125)
+        UiPush()
+            --UiText(combo)
+            UiTranslate(0, 50)
+            UiPush()
+                UiFont("MOD/assets/aaaiight-fat.ttf", 70)
+
+                UiTranslate(-1,-1)
+                UiColor(1,0.07,0.42)
+                UiText(tostring(math.floor(score)))
+
+                UiTranslate(-1,-1)
+                UiColor(1,0.66,0.18)
+                UiText(tostring(math.floor(score)))
+
+                UiTranslate(-1,-1)
+                UiColor(0,1,1)
+                UiText(tostring(math.floor(score)))
+
+                UiTranslate(-1,-1)
+                UiColor(1,1,1)
+                UiText(tostring(math.floor(score)))
+            UiPop()
+
+            if multiplier > 1 then
+                UiPush()
+                    UiTranslate(0, -50)
+                    UiRotate(5)
+                    UiFont("MOD/assets/aaaiight.ttf", 40)
+                    UiColor(0.4,0.9,0.4)
+                    UiText(string.format("%.1f", multiplier).."x")
+                UiPop()
+            end
+
+            biggestMultText = 0
+            for m, text in pairs(multtext) do
+                --DebugPrint(m..", "..text)
+                if multiplier >= m and m > biggestMultText then
+                    biggestMultText = m
                 end
             end
+
+            UiTranslate(0, 50)
+            UiFont("MOD/assets/aaaiight.ttf", 30)
+            UiText(multtext[biggestMultText])
+        UiPop()
+    UiPop()
+end
+
+function drawDeathScreen()
+    UiMakeInteractive()
+        
+
+    UiBlur(1)
+    UiColor(0.5, 0, 0, 0.5)
+    UiRect(UiWidth(), UiHeight())
+    UiBlur(0)
+
+    UiTranslate(UiWidth() * 0.5, UiHeight() * 0.3)
+    UiAlign("center middle")
+    UiColor(1, 0.1, 0.1, 1)
+    UiFont("MOD/assets/aaaiight.ttf", 120)
+    UiTextShadow(1, 1, 1, 1, 5, 0.5)
+    UiText("YOU GOT GNOMED")
+
+    UiTextShadow(0, 0, 0, 1, 2.4, 1)
+    UiColor(1, 1, 1, 1)
+    UiFont("MOD/assets/aaaiight.ttf", 90)
+    UiTranslate(0, UiHeight() * 0.2)
+    if UiTextButton("RETRY") then
+        Restart()
+        --[[local coolString = GetString("game.levelPath")
+        StartLevel("", GetString("game.levelPath"),"nomainmenu",true)]]
+    end
+
+    UiTranslate(0, UiHeight() * 0.1)
+    if UiTextButton("MENU") then
+        StartLevel("", "MOD/main.xml")
+    end
+
+    UiTranslate(0, UiHeight() * 0.1)
+    if UiTextButton("QUIT") then
+        Menu()
+    end
+    if GetBool("savegame.mod.endless") then
+        UiFont("MOD/assets/Gemstone.ttf", 40)
+        UiColor(0.8,0.8,0.4)
+        UiTranslate(0, UiHeight() * 0.04)
+        UiText("GMOMES KILLED:")
+        UiTranslate(0, UiHeight() * 0.04)
+        UiText("SHOTS FIRED:")
+        UiTranslate(0, UiHeight() * 0.04)
+        UiText("SHOTS HIT:")
+        UiTranslate(0, UiHeight() * 0.04)
+        UiText("TIMES DASHED:")
+    end
+end
+
+function server.init()
+       maxHealth = 5
+       iSeconds = 1
+       health = maxHealth
+       iSecond = 0
+       --score
+       multiplierDecay = 0.32 	--per second
+       multiplierIncrease = 0.425 --per kill
+    pauseTime = 5			--how long to stop decay after kill
+       pointsToHealInit = 20
+       multtext = {}
+       multtext[0] = ""
+       multtext[2] = "gnot bad"
+       multtext[4] = "Gnice."
+       multtext[6] = "Gnometacular.."
+       multtext[8] = "GNASTY!"
+       multtext[10] = "GNOMERGENCY!!"
+       multtext[12] = "RECKGNOMING!!!"
+       multtext[14] = "JUDGNOMENT DAY!!!!"
+       multtext[16] = "GNOMAGEDDON!!!!!"
+       multtext[18] = "APOCGNOMYPSE!!!!!!"
+       multtext[20] = "GNOMECIDE!!!!!!!"
+    RegisterListenerTo("gnomeHurt", "AddScore")
+       if GetInt("savegame.mod.stats.levelOrder")+1 == GetInt("level.currentLevelInt") and GetBool("savegame.mod.stats.adventureBegun") then
+           fraud = false
+       else
+           fraud = true
+       end
+       if fraud then
+           score = 0
+       else
+           score = GetInt("savegame.mod.stats.score.inRun")
+           --SetInt("savegame.mod.stats.score.inRun", 0, true)
+       end
+    multiplier = 1
+       combo = 0
+    pauseTimer = pauseTime
+       MaxhitTimer = 1
+       hitTimer = MaxhitTimer
+       pointsSinceHeal = 0
+       dead = false
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           SetInt("level.score", score, true)
+           pointsToHeal = pointsToHealInit
+           pointsToHeal = pointsToHeal*GetFloat("savegame.mod.options.healMult")
+           local playerTool = GetString("game.player.tool")
+           SetFloat("game.tool.gnome-weapon.ammo",99999, true)
+           --SetBool("level.gnomeInstakillAll",false, true)
+           --if InputPressed("i") then SetBool("level.gnomeInstakillAll",true, true) end
+           SetInt("game.fire.maxcount", 30, true)
+           hp = GetPlayerHealth(playerId)
+           if not dead then
+               if health ~= 0 then
+                   if not GetBool("level.dashIframesOn") then
+                       if iSecond <= 0 then
+                           if hp < 0.8 then
+                               hurtPlayer()
+                           end
+                       else
+                           iSecond = iSecond - dt
+                       end
+                   end
+               else
+                   scoreBoard = false
+                   deathCamTrans = GetPlayerCameraTransform(playerId)
+                   dead = true
+                   SetBool("level.playerIsDead",true, true)
+               end
+           else
+               SetCameraTransform(deathCamTrans)
+               SetPlayerTransform(playerId, Transform(VecAdd(deathCamTrans.pos, Vec(0, -50, 0))))
+           end
+           SetPlayerHealth(playerId, 1)
+           --score
+           if pauseTimer >= pauseTime then
+        	multiplier = math.max(multiplier - (multiplierDecay * dt), 1)
         else
-            scoreBoard = false
-            deathCamTrans = GetPlayerCameraTransform()
-            dead = true
-            SetBool("level.playerIsDead",true)
-        end
-    else
-        SetCameraTransform(deathCamTrans)
-        SetPlayerTransform(Transform(VecAdd(deathCamTrans.pos, Vec(0, -50, 0))))
-    end
-
-    SetPlayerHealth(1)
-
-    --score
-    if pauseTimer >= pauseTime then
-		multiplier = math.max(multiplier - (multiplierDecay * dt), 1)
-	else
-		pauseTimer = pauseTimer + dt
-	end
-    SetFloat("level.scoreMultiplier",multiplier)
-    
-
-	--DebugWatch("score", score)
-    --DebugWatch("combo", combo)
-	--DebugWatch("multiplier", multiplier)
-    --DebugWatch("pointsSinceHeal", pointsSinceHeal)
-end
-
-function draw()
+        	pauseTimer = pauseTimer + dt
+        end
+           SetFloat("level.scoreMultiplier",multiplier, true)
+    end
+end
+
+function client.draw()
     if not GetBool("level.titleCardLoad") and not GetBool("level.playerIsDead") then
         UiPush()
             UiTranslate(UiWidth() * 0.025, UiHeight() * 0.85)
@@ -134,155 +244,24 @@
                 end
             end
         UiPop()
-        
+
         if scoreBoard and not GetBool("level.playerIsDead") and not GetBool("savegame.mod.options.scoreboardToggled") then
             drawScoreThing()
         end
     end
-    if iSecond > 0 then
+    if iSecond ~= 0 then
         UiColor(0.6,0,0,(iSecond/(iSeconds*GetFloat("savegame.mod.options.iFrameMult")))/4)
         UiRect(UiWidth(),UiHeight())
     end
 
     if health <= 0 then
         if not setDeathStats then
-            SetInt("savegame.mod.stats.score.inRun", GetInt("level.score"))
-            SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"))
+            SetInt("savegame.mod.stats.score.inRun", GetInt("level.score"), true)
+            SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"), true)
         end
         --drawDeathScreen()
-        SetBool("level.settingsOpened",true)
-        SetBool("level.deadOptionsScreen",true)
-    end
-end
-
-function hurtPlayer()
-    if GetBool("savegame.mod.modifiers.Glass") then StartLevel("","MOD/main.xml") end
-    health = health - 1
-    iSecond = iSeconds*GetFloat("savegame.mod.options.iFrameMult")
-    ShakeCamera(0.5)
-
-    multiplier = 0
-    combo = 0
-    pointsSinceHeal = 0 --reset heal progress
-end
-
-function AddScore(args)
-    if not dead then
-        gnomePoints = tonumber(args)
-
-        combo = combo + 1
-	    multiplier = multiplier + multiplierIncrease
-
-	    score = score + (gnomePoints * multiplier)
-        pointsSinceHeal = pointsSinceHeal + gnomePoints
-
-        if pointsSinceHeal >= pointsToHeal then
-            health = math.min(health + 1, maxHealth)
-            pointsSinceHeal = pointsSinceHeal - pointsToHeal
-        end
-
-	    pauseTimer = 0
-    end
-end
-
-function drawScoreThing()
-    UiPush()
-        UiTranslate(UiCenter(), UiHeight() * 0.04)
-        UiAlign("center middle")
-        UiTranslate(-125)
-        UiPush()
-            --UiText(combo)
-            UiTranslate(0, 50)
-            UiPush()
-                UiFont("MOD/assets/aaaiight-fat.ttf", 70)
-
-                UiTranslate(-1,-1)
-                UiColor(1,0.07,0.42)
-                UiText(tostring(math.floor(score)))
-
-                UiTranslate(-1,-1)
-                UiColor(1,0.66,0.18)
-                UiText(tostring(math.floor(score)))
-
-                UiTranslate(-1,-1)
-                UiColor(0,1,1)
-                UiText(tostring(math.floor(score)))
-
-                UiTranslate(-1,-1)
-                UiColor(1,1,1)
-                UiText(tostring(math.floor(score)))
-            UiPop()
-
-            if multiplier > 1 then
-                UiPush()
-                    UiTranslate(0, -50)
-                    UiRotate(5)
-                    UiFont("MOD/assets/aaaiight.ttf", 40)
-                    UiColor(0.4,0.9,0.4)
-                    UiText(string.format("%.1f", multiplier).."x")
-                UiPop()
-            end
-
-            biggestMultText = 0
-            for m, text in pairs(multtext) do
-                --DebugPrint(m..", "..text)
-                if multiplier >= m and m > biggestMultText then
-                    biggestMultText = m
-                end
-            end
-
-            UiTranslate(0, 50)
-            UiFont("MOD/assets/aaaiight.ttf", 30)
-            UiText(multtext[biggestMultText])
-        UiPop()
-    UiPop()
-end
-
-function drawDeathScreen()
-    UiMakeInteractive()
-        
-
-    UiBlur(1)
-    UiColor(0.5, 0, 0, 0.5)
-    UiRect(UiWidth(), UiHeight())
-    UiBlur(0)
-
-    UiTranslate(UiWidth() * 0.5, UiHeight() * 0.3)
-    UiAlign("center middle")
-    UiColor(1, 0.1, 0.1, 1)
-    UiFont("MOD/assets/aaaiight.ttf", 120)
-    UiTextShadow(1, 1, 1, 1, 5, 0.5)
-    UiText("YOU GOT GNOMED")
-
-    UiTextShadow(0, 0, 0, 1, 2.4, 1)
-    UiColor(1, 1, 1, 1)
-    UiFont("MOD/assets/aaaiight.ttf", 90)
-    UiTranslate(0, UiHeight() * 0.2)
-    if UiTextButton("RETRY") then
-        Restart()
-        --[[local coolString = GetString("game.levelPath")
-        StartLevel("", GetString("game.levelPath"),"nomainmenu",true)]]
-    end
-
-    UiTranslate(0, UiHeight() * 0.1)
-    if UiTextButton("MENU") then
-        StartLevel("", "MOD/main.xml")
-    end
-
-    UiTranslate(0, UiHeight() * 0.1)
-    if UiTextButton("QUIT") then
-        Menu()
-    end
-    if GetBool("savegame.mod.endless") then
-        UiFont("MOD/assets/Gemstone.ttf", 40)
-        UiColor(0.8,0.8,0.4)
-        UiTranslate(0, UiHeight() * 0.04)
-        UiText("GMOMES KILLED:")
-        UiTranslate(0, UiHeight() * 0.04)
-        UiText("SHOTS FIRED:")
-        UiTranslate(0, UiHeight() * 0.04)
-        UiText("SHOTS HIT:")
-        UiTranslate(0, UiHeight() * 0.04)
-        UiText("TIMES DASHED:")
-    end
-end+        SetBool("level.settingsOpened",true, true)
+        SetBool("level.deadOptionsScreen",true, true)
+    end
+end
+

```

---

# Migration Report: scripts\libraries\Automatic.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\libraries\Automatic.lua
+++ patched/scripts\libraries\Automatic.lua
@@ -1,80 +1,76 @@
--- VERSION 4.1
--- I ask that you please do not rename Automatic.lua - Thankyou
-
---#region Documentation
-
----Documentation Assumes that TDTD's library is in the environemnt
-
---#endregion
---#region Shortcuts
-
-AutoFlatSprite = LoadSprite('ui/menu/white_32.png')
-AutoPalette = {
-    vfchill = {
-		background_dark =  { 0.28627450980392, 0.25490196078431,  0.38039215686275 },
-		background_light = { 0.41960784313725, 0.39607843137255,  0.58823529411765 },
-		wood_dark =        { 0.6,              0.33725490196078,  0.42352941176471 },
-		wood_light =       { 0.78039215686275, 0.53333333333333,  0.56470588235294 },
-		rock_dark =        { 0.41960784313725, 0.38039215686275,  0.46666666666667 },
-		rock_light =       { 0.49803921568627, 0.46274509803922,  0.55686274509804 },
-		green_dark =       { 0.3843137254902,  0.76078431372549,  0.76078431372549 },
-		green_light =      { 0.4156862745098,  0.90980392156863,  0.63529411764706 },
-		jade_dark =        { 0.33725490196078, 0.52156862745098,  0.6              },
-		jade_light =       { 0.29411764705882, 0.68627450980392,  0.69019607843137 },
-		aqua_dark =        { 0.28627450980392, 0.46666666666667,  0.58039215686275 },
-		aqua_light =       { 0.32156862745098, 0.60392156862745,  0.78039215686275 },
-		pastel_dark =      { 1,                0.7921568627451,   0.83137254901961 },
-		pastel_light =     { 0.80392156862745, 0.70588235294118,  0.85882352941176 },
-		pink_dark =        { 0.70196078431373, 0.45098039215686,  0.64313725490196 },
-		pink_light =       { 0.94901960784314, 0.57647058823529,  0.86274509803922 },
-		purple_dark =      { 0.56470588235294, 0.34117647058824,  0.63921568627451 },
-		purple_light =     { 0.77647058823529, 0.45098039215686,  0.8156862745098  },
-		yellow_dark =      { 0.7921568627451,  0.65490196078431,  0.32156862745098 },
-		yellow_light =     { 0.89803921568627, 0.75686274509804,  0.36862745098039 },
-		amber_dark =       { 0.7843137254902,  0.50196078431373,  0.28627450980392 },
-		amber_light =      { 0.96470588235294, 0.63921568627451,  0.18039215686275 },
-		red_dark =         { 0.72549019607843, 0.35686274509804,  0.48627450980392 },
-		red_light =        { 0.84313725490196, 0.33333333333333,  0.41960784313725 },
-		white_dark =       { 0.84705882352941, 0.74509803921569,  0.61960784313725 },
-		white_light =      { 0.96470588235294, 0.91372549019608,  0.80392156862745 },
-		blue_dark =        { 0.2078431372549,  0.31372549019608,  0.43921568627451 },
-		blue_light =       { 0.19607843137255, 0.61176470588235,  0.78823529411765 },
-		alert_dark =       { 0.22352941176471, 0.098039215686275, 0.2              },
-		alert_light =      { 0.74901960784314, 0.21960784313725,  0.49019607843137 },
-    },
-	catppuccin = { -- macchiato
-		rosewater = { 0.95686274509804,  0.85882352941176,  0.83921568627451 },
-		flamingo =  { 0.94117647058824,  0.77647058823529,  0.77647058823529 },
-		pink =      { 0.96078431372549,  0.74117647058824,  0.90196078431373 },
-		mauve =     { 0.77647058823529,  0.62745098039216,  0.96470588235294 },
-		red =       { 0.92941176470588,  0.52941176470588,  0.58823529411765 },
-		maroon =    { 0.93333333333333,  0.6,               0.62745098039216 },
-		peach =     { 0.96078431372549,  0.66274509803922,  0.49803921568627 },
-		yellow =    { 0.93333333333333,  0.83137254901961,  0.62352941176471 },
-		green =     { 0.65098039215686,  0.85490196078431,  0.5843137254902  },
-		teal =      { 0.54509803921569,  0.83529411764706,  0.7921568627451  },
-		sky =       { 0.56862745098039,  0.84313725490196,  0.89019607843137 },
-		sapphire =  { 0.49019607843137,  0.76862745098039,  0.89411764705882 },
-		blue =      { 0.54117647058824,  0.67843137254902,  0.95686274509804 },
-		lavender =  { 0.71764705882353,  0.74117647058824,  0.97254901960784 },
-		text =      { 0.7921568627451,   0.82745098039216,  0.96078431372549 },
-		subtext1 =  { 0.72156862745098,  0.75294117647059,  0.87843137254902 },
-		subtext0 =  { 0.64705882352941,  0.67843137254902,  0.79607843137255 },
-		overlay2 =  { 0.57647058823529,  0.60392156862745,  0.71764705882353 },
-		overlay1 =  { 0.50196078431373,  0.52941176470588,  0.63529411764706 },
-		overlay0 =  { 0.43137254901961,  0.45098039215686,  0.55294117647059 },
-		surface2 =  { 0.35686274509804,  0.37647058823529,  0.47058823529412 },
-		surface1 =  { 0.28627450980392,  0.30196078431373,  0.3921568627451  },
-		surface0 =  { 0.21176470588235,  0.22745098039216,  0.30980392156863 },
-		base =      { 0.14117647058824,  0.15294117647059,  0.22745098039216 },
-		mantle =    { 0.11764705882353,  0.12549019607843,  0.18823529411765 },
-		crust =     { 0.094117647058824, 0.098039215686275, 0.14901960784314 },
-	}
+#version 2
+local RegistryTableMeta = {
+	__index = function(self, key)
+		key = key:lower()
+		local path = AutoKey(rawget(self, '__path'), key)
+		if not HasKey(path) then
+			return nil
+		end
+		
+		local type = GetString(AutoKey(path, '__type'))
+		
+		if type == 'table' then
+			return AutoRegistryBindedTable(path)
+		else
+			local str = GetString(path)
+			
+			if type == 'number' then
+				return tonumber(str)
+			end
+			
+			return str
+		end
+	end,
+	__newindex = function(self, key, value)
+		key = key:lower()
+		local path = AutoKey(rawget(self, '__path'), key)
+		
+		local function dive(p, v)
+			if type(v) ~= "table" then
+				SetString(p, v, true)
+				
+				if type(v) ~= "nil" then
+					SetString(AutoKey(p, '__type'), type(v), true)
+				end
+			else
+				SetString(AutoKey(p, '__type'), 'table', true)
+				for k, set in pairs(v) do
+					dive(AutoKey(p, k), set)
+				end
+			end
+		end
+		
+		dive(path, value)
+	end,
+	__call = function(self)
+		local path = rawget(self, '__path')
+		
+		local function dive(p)
+			local keys = ListKeys(p)
+			local full = {}
+			
+			for i = 1, #keys do
+				local child = AutoKey(p, keys[i])
+				
+				if keys[i] ~= '__type' then
+					local t = GetString(AutoKey(child, '__type'))
+					if t == 'table' then
+						full[keys[i]] = dive(child)
+					else
+						local str = GetString(child)
+						local num = tonumber(str)
+						full[keys[i]] = num or str
+					end
+				end
+			end
+			
+			return full
+		end
+		
+		return dive(path)
+	end
 }
 
----Creates pitch frequencies for UiSound
----@param baseline string
----@return { C:number, Cs:number, D:number, Ds:number, E:number, F:number, Fs:number, G:number, Gs:number, A:number, As:number, B:number }
 function AutoNoteFrequency(baseline)
 	local f = {
 		C  = 261.63,
@@ -99,55 +95,16 @@
 	return tuned
 end
 
---#endregion
---#region Arithmetic
-
----Sigmoid function, Can be used for juicy UI and smooth easing among other things.
----
----https://www.desmos.com/calculator/cmmwrjtyit?invertedColors
----@param v number? Input number, if nil then it will be a Random number between 0 and 1
----@param max number The Maximum value
----@param steep number How steep the curve is
----@param offset number The horizontal offset of the middle of the curve
----@return number
 function AutoSigmoid(v, max, steep, offset)
 	v = AutoDefault(v, math.random(0, 10000) / 10000)
 	return (max or 1) / (1 + math.exp((v - (offset or 0.5)) * (steep or -10)))
 end
 
----Returns a smoothed value from 0 to 1,
----
----If `x` is less than `edge_1`, output `0`.
----
----If `x` is more than `edge_2`, output `1`.
----
----If `x` is between, interpolate between the two edges
----
----This is the "smootherstep" varation
----@param x number
----@param edge_1 number
----@param edge_2 number
----@return number
 function AutoSmoothStep(x, edge_1, edge_2)
 	x = AutoClamp((x - edge_1) / (edge_2 - edge_1))
 	return x ^ 3 * (x * (6.0 * x - 15.0) + 10.0)
 end
 
----Basically smooth step between `edge_1` and `edge_2`, then smooth step between `edge_2` and `edge_3`
----
----If `x` is less than `edge_1`, output `0`.
----
----If `x` is `edge_2`, output `1`
----
----If `x` is more than `edge_3`, output `0`.
----
----If `x` is between, interpolate between the two closest edges
----
----@param x number
----@param edge_1 number
----@param edge_2 number
----@param edge_3 number
----@return number
 function AutoSmoothStep3(x, edge_1, edge_2, edge_3)
     local t
     if x < edge_2 then
@@ -158,12 +115,6 @@
     return t
 end
 
----Rounds a number.
----
----This was a Challenge by @TallTim and @1ssnl to make the smallest rounding function, but I expanded it to make it easier to read and a little more efficent
----@param v number Input number
----@param increment number? The lowest increment. A Step of 1 will round the number to 1, A step of 5 will round it to the closest increment of 5, A step of 0.1 will round to the tenth. Default is 1
----@return number
 function AutoRound(v, increment)
 	increment = AutoDefault(increment, 1)
 	if increment == 0 then return v end
@@ -171,14 +122,6 @@
 	return math.floor(v * s + 0.5) / s
 end
 
----Maps a value from range a1-a2 to range b1-b2
----@param v number Input number
----@param a1 number Goes from the range of number a1
----@param a2 number To number a2
----@param b1 number To the range of b1
----@param b2 number To number b2
----@param clamp boolean? Clamp the number between b1 and b2, Default is false
----@return number
 function AutoMap(v, a1, a2, b1, b2, clamp)
 	clamp = AutoDefault(clamp, false)
 	if a1 == a2 then return b2 end
@@ -186,21 +129,12 @@
 	return clamp and AutoClamp(mapped, math.min(b1, b2), math.max(b1, b2)) or mapped
 end
 
----Limits a value from going below the min and above the max
----@param v number The number to clamp
----@param min number? The minimum the number can be, Default is 0
----@param max number? The maximum the number can be, Default is 1
----@return number
 function AutoClamp(v, min, max)
 	min = AutoDefault(min, 0)
 	max = AutoDefault(max, 1)
 	return math.max(math.min(v, max), min)
 end
 
----Limits a value from going below the min and above the max
----@param v number The number to clamp
----@param max number? The maximum the length of the number can be, Default is 1
----@return number
 function AutoClampLength(v, max)
 	max = AutoDefault(max, 1)
 	if v < -max then
@@ -240,11 +174,6 @@
     return maxAbsValue
 end
 
----Wraps a value inbetween a range, Thank you iaobardar for the Optimization
----@param v number The number to wrap
----@param min number? The minimum range
----@param max number? The maximum range
----@return number
 function AutoWrap(v, min, max)
 	min = AutoDefault(min, 0)
 	max = AutoDefault(max, 1)
@@ -252,25 +181,10 @@
 	return (v - min) % ((max + 1) - min) + min
 end
 
----Linerarly Iterpolates between `a` and `b` by fraction `t`
----
----Does not clamp
----@param a number Goes from number A
----@param b number To number B
----@param t number Interpolated by T
----@return number
 function AutoLerp(a, b, t)
 	return (1 - t) * a + t * b
 end
 
----Spherically Iterpolates between `a` and `b` by fraction `t`.
----
----Basically Lerp but with wrapping
----@param a number Goes from number A
----@param b number To number B
----@param t number Interpolated by T
----@param w number Wraps at
----@return number
 function AutoLerpWrap(a, b, t, w)
 	local m = w
 	local da = (b - a) % m
@@ -278,13 +192,6 @@
 	return a + n * t
 end
 
----Moves `a` towards `b` by amount `t`
----
----Will clamp as to not overshoot
----@param a number Goes from number A
----@param b number To number B
----@param t number Moved by T
----@return number
 function AutoMove(a, b, t)
 	output = a
 	if a == b then
@@ -298,19 +205,10 @@
 	return output
 end
 
----Return the Distance between the numbers `a` and `b`
----@param a number
----@param b number
----@return number
 function AutoDist(a, b)
 	return math.abs(a - b)
 end
 
----Normalizes all values in a table to have a magnitude of 1 - Scales every number to still represent the same "direction"
----@param t table<number>
----@param scale number?
----@param zero_compatability boolean? If the length is zero, do not normalize values
----@return table
 function AutoNormalize(t, scale, zero_compatability)
 	local norm = {}
 	local maxabs = 0
@@ -327,13 +225,6 @@
 	return norm
 end
 
----Takes a table of weights, like {1, 2, 0.5, 0.5}, and produces a table of how much space each weight would take up if it were to span over a given length.
----If given the weights {1, 2, 0.5, 0.5}, with a span length of 100, the resulting table would be = {25, 50, 12.5, 12.5}.
----A padding parameter can also be added which can be used to make Ui easier. Iterate through the resulting table, after each UiRect, move the width + the padding parameter
----@param weights table<number>|number weights
----@param span number
----@param padding number?
----@return table
 function AutoFlex(weights, span, padding)
 	local istable = type(weights) == "table"
 	weights = not istable and (function()
@@ -363,9 +254,6 @@
 	return flexxed
 end
 
----Returns index of the selected weight using a bias based on the weight values. Good for Biased Randomness
----@param weights table<number>
----@return number selected
 function AutoBias(weights)
 	local T = {}
 	local max = 0
@@ -389,27 +277,7 @@
 		end
 	end
 end
---#endregion
---#region Vector Functions
-
----Rebuilds a table in a given order, also known as Swizzling
----
----| Swizzle | Result |
----| --- | --- |
----| `xyz` | { x, y, z } |
----| `zxy` | { z, x, y } |
----| `xy` | { x, y } |
----| `xz` | { x, z } |
----| `xxx` | { x, x, x } |
----| `xyzw` | { x, y, z, w } |
----| `wxyz` | { w, x, y, z } |
----| `rgba` | { r, g, b, a } |
----| `bgra` | { b, g, r, a } |
----| `aaaa` | { a, a, a, a } |
----
----@param vec vector|table
----@param swizzle string
----@return table
+
 function AutoSwizzle(vec, swizzle)
 	local swizzleMap = { x = 1, y = 2, z = 3, w = 4, r = 1, g = 2, b = 3, a = 4 }
 	local built = {}
@@ -421,10 +289,6 @@
 	return built
 end
 
----Returns true if each axis of vector `a` is equal to each axis of vector `b`
----@param a vector
----@param b vector
----@return boolean
 function AutoVecEquals(a, b)
 	for i, va in pairs(a) do
 		if va ~= b[i] then return false end
@@ -433,18 +297,6 @@
 	return true
 end
 
----Return a Random Vector with an optional offset and scale
----
----Not equally distributed! Uses `AutoVecRndSpherical` instead!
----
----```
----AutoVecRnd()
----AutoVecRnd(2)
----AutoVecRnd(Vec(0, 1), 0.5)
----```
----@param param1 number|vector?
----@param param2 number?
----@return vector
 function AutoVecRnd(param1, param2)
 	local offset, scale
 	if type(param1) == "table" then
@@ -464,18 +316,6 @@
 	return VecAdd(offset, VecScale(rndVec, scale))
 end
 
----Return ask Random Vector on a Sphere with an optional offset and scale
----
----Ensures more even distribution
----
----```
----AutoVecRndSpherical()
----AutoVecRndSpherical(2)
----AutoVecRndSpherical(Vec(0, 1), 0.5)
----```
----@param param1 number|vector?
----@param param2 number?
----@return vector
 function AutoVecRndSpherical(param1, param2)
 	local offset, scale
 	if type(param1) == "table" then
@@ -498,11 +338,6 @@
 	return VecAdd(offset, VecScale(v, scale))
 end
 
----Return a random vector within a Hemisphere, pointing towrads the negative Z axis
----
----Ensures even distribution within the specified angle range
----
----@return vector
 function AutoVecRndHemi(from_dot, to_dot)
     local phi = math.acos(AutoMap(math.random(), 0, 1, from_dot or 0, to_dot or 1))
     local theta = math.random() * 2 * math.pi
@@ -516,89 +351,42 @@
     return v
 end
 
-
----Return the Distance between Two Vectors
----@param a vector
----@param b vector
----@return number
 function AutoVecDist(a, b)
 	return VecLength(VecSub(b, a))
 end
 
----Return the Distance between Two Vectors, without considering the X component
----@param a vector
----@param b vector
----@return number
 function AutoVecDistNoX(a, b)
 	return math.sqrt((b[2] - a[2])^2 + (b[3] - a[3])^2)
 end
 
----Return the Distance between Two Vectors, without considering the Y component
----@param a vector
----@param b vector
----@return number
 function AutoVecDistNoY(a, b)
 	return math.sqrt((b[1] - a[1])^2 + (b[3] - a[3])^2)
 end
 
----Return the Distance between Two Vectors, without considering the Z component
----@param a vector
----@param b vector
----@return number
 function AutoVecDistNoZ(a, b)
 	return math.sqrt((b[1] - a[1])^2 + (b[2] - a[2])^2)
 end
 
----Moves a vector in a direction by a given amount
----
----Equivalent to `VecAdd(vec, VecScale(dir, dist))`
----@param vec any
----@param dir any
----@param dist any
----@return vector
 function AutoVecMove(vec, dir, dist)
 	return VecAdd(vec, VecScale(dir, dist))
 end
 
----Returns a Vector Rounded to a number
----@param vec vector
----@param r number?
----@return vector
 function AutoVecRound(vec, r)
 	return Vec(AutoRound(vec[1], r), AutoRound(vec[2], r), AutoRound(vec[3], r))
 end
 
----Returns a Vector where all numbers are floored
----@param vec vector
----@return vector
 function AutoVecFloor(vec)
 	return Vec(math.floor(vec[1]), math.floor(vec[2]), math.floor(vec[3]))
 end
 
----Returns a Vector where all numbers are ceiled
----@param vec vector
----@return vector
 function AutoVecCeil(vec)
 	return Vec(math.ceil(vec[1]), math.ceil(vec[2]), math.ceil(vec[3]))
 end
 
----Return a vector that has the magnitude of `b`, but with the direction of `a`
----
----Equivalent to `VecScale(VecNormalize(a), b)`
----@param a vector
----@param b number
----@return vector
 function AutoVecRescale(a, b)
 	return VecScale(VecNormalize(a), b)
 end
 
----Maps a Vector from range a1-a2 to range b1-b2
----@param v vector Input Vector
----@param a1 number Goes from the range of number a1
----@param a2 number To number a2
----@param b1 number To the range of b1
----@param b2 number To number b2
----@return vector
 function AutoVecMap(v, a1, a2, b1, b2)
 	if a1 == a2 then return AutoVecRescale(v, b2) end
 	local out = {
@@ -609,11 +397,6 @@
 	return out
 end
 
----Limits the magnitude of a vector to be between min and max
----@param v vector The Vector to clamp
----@param min number? The minimum the magnitude can be, Default is 0
----@param max number? The maximum the magnitude can be, Default is 1
----@return vector
 function AutoVecClampMagnitude(v, min, max)
 	min, max = AutoDefault(min, 0), AutoDefault(max, 1)
 	local l = VecLength(v)
@@ -626,11 +409,6 @@
 	end
 end
 
----Limits a vector to be between min and max
----@param v vector The Vector to clamp
----@param min number? The minimum, Default is 0
----@param max number? The maximum, Default is 1
----@return vector
 function AutoVecClamp(v, min, max)
 	min, max = AutoDefault(min, 0), AutoDefault(max, 1)
 	return {
@@ -640,11 +418,6 @@
 	}
 end
 
----Limits a vector to be between min and max vector
----@param v vector The Vector to clamp
----@param min vector The minimum
----@param max vector The maximum
----@return vector
 function AutoVecClampVec(v, min, max)
 	return {
 		AutoClamp(v[1], min[1], max[1]),
@@ -653,28 +426,15 @@
 	}
 end
 
----Return Vec(1, 1, 1) scaled by length
----@param length number return the vector of size length, Default is 1
----@return vector
 function AutoVecOne(length)
 	local l = length or 1
 	return Vec(l, l, l)
 end
 
----Returns the midpoint between two vectors
----
----Equivalent to `VecScale(VecAdd(a, b), 0.5)`
----@param a any
----@param b any
----@return vector
 function AutoVecMidpoint(a, b)
 	return VecScale(VecAdd(a, b), 0.5)
 end
 
----Return Vec `a` multiplied by Vec `b`
----@param a vector
----@param b vector
----@return vector
 function AutoVecMulti(a, b)
 	return {
 		(a[1] or 0) * (b[1] or 0),
@@ -683,10 +443,6 @@
 	}
 end
 
----Return Vec `a` divided by Vec `b`
----@param a vector
----@param b vector
----@return vector
 function AutoVecDiv(a, b)
 	return {
 		(a[1] or 0) / (b[1] or 0),
@@ -695,10 +451,6 @@
 	}
 end
 
----Return Vec `a` to the Power of `b`
----@param a vector
----@param b number
----@return vector
 function AutoVecPow(a, b)
 	return {
 		(a[1] or 0) ^ (b or 0),
@@ -707,10 +459,6 @@
 	}
 end
 
----Return Vec `a` to the Power of Vec `b`
----@param a vector
----@param b vector
----@return vector
 function AutoVecPowVec(a, b)
 	return {
 		a[1] ^ b[1],
@@ -719,9 +467,6 @@
 	}
 end
 
----Returns the absolute value of an vector
----@param v vector
----@return vector
 function AutoVecAbs(v)
 	return {
 		math.abs(v[1]),
@@ -730,62 +475,37 @@
 	}
 end
 
----Equivalent to `math.min(unpack(v))`
----@param v vector
----@return number
 function AutoVecMin(v)
 	return math.min(unpack(v))
 end
 
----Equivalent to `math.max(unpack(v))`
----@param v vector
----@return number
 function AutoVecMax(v)
 	return math.max(unpack(v))
 end
 
---- Rotates a vector around an axis by a given angle
---- @param vec vector The vector to rotate
---- @param axis vector The rotation axis, a unit vector
---- @param angle number The rotation angle in degrees
---- @return vector vec The rotated vector
 function AutoVecRotate(vec, axis, angle)
 	local quat = QuatAxisAngle(axis, angle)
 	return QuatRotateVec(quat, vec)
 end
 
----Return `v` with it's `x` value replaced by `subx`
----@param v vector
----@param subx number
 function AutoVecSubsituteX(v, subx)
 	local new = VecCopy(v)
 	new[1] = subx
 	return new
 end
 
----Return `v` with it's `y` value replaced by `suby`
----@param v vector
----@param suby number
 function AutoVecSubsituteY(v, suby)
 	local new = VecCopy(v)
 	new[2] = suby
 	return new
 end
 
----Return `v` with it's `z` value replaced by `subz`
----@param v vector
----@param subz number
 function AutoVecSubsituteZ(v, subz)
 	local new = VecCopy(v)
 	new[3] = subz
 	return new
 end
 
---- Projects a vector onto a plane defined by its normal.
----@param vector vector The vector to be projected.
----@param planeNormal vector The normal vector of the plane.
----@param rescale boolean? Rescale the projected vector to be the same length as the provided vector
----@return vector projectedVector The projected vector.
 function AutoVecProjectOntoPlane(vector, planeNormal, rescale)
     local dotProduct = VecDot(vector, planeNormal)
     local projection = VecScale(planeNormal, dotProduct)
@@ -793,28 +513,14 @@
 	if rescale then return AutoVecRescale(projectedVector, VecLength(vector)) else return projectedVector end
 end
 
-
-
----Converts the output of VecDot with normalized vectors to an angle
----@param dot number
----@return number
 function AutoDotToAngle(dot)
 	return math.deg(math.acos(dot))
 end
 
---#endregion
---#region Quat Functions
-
----Equivalent to `QuatRotateVec(rot, Vec(0, 0, 1))`
----@param rot quaternion
----@return vector
 function AutoQuatFwd(rot)
 	return QuatRotateVec(rot, Vec(0, 0, 1))
 end
 
----Returns a random quaternion
----@param angle number degrees
----@return quaternion
 function AutoRandomQuat(angle)
 	local axis = { math.random() - 0.5, math.random() - 0.5, math.random() - 0.5 }
 	local sinHalfAngle = math.sin(math.rad(angle) / 2)
@@ -827,56 +533,32 @@
 )
 end
 
----Computes the dot product of two quaternions.
----@param a quaternion
----@param b quaternion
----@return number
 function AutoQuatDot(a, b)
 	return a[1] * b[1] + a[2] * b[2] + a[3] * b[3] + a[4] * b[4]
 end
 
----Returns the Conjugate of the given quaternion.
----@param quat quaternion
----@return quaternion quat
 function AutoQuatConjugate(quat)
 	return { -quat[1], -quat[2], -quat[3], quat[4] }
 end
 
----Returns the Inverse of the given quaternion.
----@param quat quaternion
----@return quaternion quat
 function AutoQuatInverse(quat)
 	local norm = quat[1] ^ 2 + quat[2] ^ 2 + quat[3] ^ 2 + quat[4] ^ 2
 	local inverse = { -quat[1] / norm, -quat[2] / norm, -quat[3] / norm, quat[4] / norm }
 	return inverse
 end
 
----@param quat_to_inverse quaternion
----@param quat quaternion
----@return quaternion
 function AutoQuatInverseRotate(quat_to_inverse, quat)
 	return QuatRotateQuat(AutoQuatInverse(quat_to_inverse), quat)
 end
 
----@param quat quaternion
----@param scalar number
 function AutoQuatScale(quat, scalar)
 	return QuatSlerp(Quat(), quat, scalar)
 end
 
----Between -a and a, picks the quaternion nearest to b
----@param a quaternion
----@param b quaternion
----@return quaternion
----
----Thankyou to Mathias for this function
 function AutoQuatNearest(a, b)
 	return AutoQuatDot(a, b) < 0 and { -a[1], -a[2], -a[3], -a[4] } or { a[1], a[2], a[3], a[4] }
 end
 
---- Returns the angle of which a quaternion is rotated about a given axis
----
---- Credit goes to Mathias, thank you!
 function AutoQuatAngleAboutAxis(q, axis)
     local qXYZ = Vec(q[1], q[2], q[3])
     local co = q[4]
@@ -893,11 +575,6 @@
     return math.deg(2.0 * math.atan2(si, co))
 end
 
----Same as `QuatAxisAngle()` but takes a single vector instead of a unit vector + an angle, for convenience
----
----Thankyou to Mathias for this function
----@param v any
----@return quaternion
 function AutoQuatFromAxisAngle(v)
 	local xyz = VecScale(v, 0.5)
 	local angle = VecLength(xyz)
@@ -912,10 +589,6 @@
 	return Quat(qXYZ[1], qXYZ[2], qXYZ[3], co)
 end
 
----Converts a quaternion to an axis angle representation
----Returns a rotation vector where axis is the direction and angle is the length
----
----Thankyou to Mathias for this function
 function AutoQuatToAxisAngle(q)
 	local qXYZ = Vec(q[1], q[2], q[3])
 	local co = q[4]
@@ -929,31 +602,16 @@
 	return VecScale(qXYZ, 2.0 * angle / si)
 end
 
---#endregion
---#region AABB Bounds Functions
-
----Get the center of a body's bounds
----@param body body_handle
----@return vector
 function AutoBodyCenter(body)
 	local aa, bb = GetBodyBounds(body)
 	return VecScale(VecAdd(aa, bb), 0.5)
 end
 
----Get the center of a shapes's bounds
----@param shape shape_handle
----@return vector
 function AutoShapeCenter(shape)
 	local aa, bb = GetShapeBounds(shape)
 	return VecScale(VecAdd(aa, bb), 0.5)
 end
 
----Expands a given boudns to include a point
----@param aa vector
----@param bb vector
----@param ... vector Points, can be one or multiple
----@return vector
----@return vector
 function AutoAABBInclude(aa, bb, ...)
 	for _, point in ipairs(arg) do
 		aa, bb = {
@@ -970,11 +628,6 @@
 	return aa, bb
 end
 
----Returns a Axis ALigned Bounding Box with the center of pos
----@param pos vector
----@param halfextents vector|number
----@return vector lower-bound
----@return vector upper-bound
 function AutoAABBBoxFromPoint(pos, halfextents)
 	if type(halfextents) == "number" then
 		halfextents = AutoVecOne(halfextents)
@@ -983,11 +636,6 @@
 	return VecSub(pos, halfextents), VecAdd(pos, halfextents)
 end
 
----Takes two vectors and modifys them so they can be used in other bound functions
----@param aa vector
----@param bb vector
----@return vector
----@return vector
 function AutoAABBCorrection(aa, bb)
 	local min, max = VecCopy(aa), VecCopy(bb)
 	
@@ -1007,11 +655,6 @@
 	return min, max
 end
 
----Get a position inside or on the Input Bounds
----@param aa vector lower-bound
----@param bb vector upper-bound
----@param vec vector? A normalized Vector pointing towards the position that should be retrieved, Default is Vec(0, 0, 0)
----@return vector
 function AutoAABBGetPos(aa, bb, vec)
 	vec = AutoDefault(vec, Vec(0, 0, 0))
 	
@@ -1023,10 +666,6 @@
 	return VecAdd(scaled, aa)
 end
 
----Get the corners of the given Bounds
----@param aa vector lower-bound
----@param bb vector upper-bound
----@return table
 function AutoAABBGetCorners(aa, bb)
 	local mid = {}
 	for i = 1, 3 do
@@ -1047,12 +686,6 @@
 	return corners
 end
 
----Get data about the size of the given Bounds
----@param aa vector lower-bound
----@param bb vector upper-bound
----@return table representing the size of the Bounds
----@return number smallest smallest edge size of the Bounds
----@return number longest longest edge size of the Bounds
 function AutoAABBSize(aa, bb)
 	local size = VecSub(bb, aa)
 	local minval = math.min(unpack(size))
@@ -1061,11 +694,6 @@
 	return size, minval, maxval
 end
 
----Takes a given AABB and subdivides into new AABBs
----@param aa vector lower-bound
----@param bb vector upper-bound
----@param levels number?
----@return table
 function AutoAABBSubdivideBounds(aa, bb, levels)
 	levels = levels or 1
 	local bounds = { { aa, bb } }
@@ -1095,10 +723,6 @@
 	return bounds
 end
 
----@param point vector
----@param lower_bound vector
----@param upper_bound vector
----@return boolean
 function AutoAABBInside(lower_bound, upper_bound, point)
     for i = 1, 3 do
         if point[i] < lower_bound[i] or point[i] > upper_bound[i] then
@@ -1109,13 +733,6 @@
     return true
 end
 
-
----@param lower_bound vector
----@param upper_bound vector
----@param start_pos vector
----@param direction vector
----@param trigger_inside boolean
----@return { hit:boolean, intersection:vector, normal:vector, dist:number }
 function AutoRaycastAABB(lower_bound, upper_bound, start_pos, direction, trigger_inside)
     local t1 = (lower_bound[1] - start_pos[1]) / direction[1]
     local t2 = (upper_bound[1] - start_pos[1]) / direction[1]
@@ -1163,16 +780,6 @@
     return { hit = false }
 end
 
-
----Draws a given Axis Aligned Bounding Box
----@param aa vector lower-bound
----@param bb vector upper-bound
----@param colorR number?
----@param colorG number?
----@param colorB number?
----@param alpha number?
----@param rgbcolors boolean?
----@param draw boolean?
 function AutoDrawAABB(aa, bb, colorR, colorG, colorB, alpha, rgbcolors, draw)
 	colorR = AutoDefault(colorR, 0)
 	colorG = AutoDefault(colorG, 0)
@@ -1224,26 +831,12 @@
 	end
 end
 
---#endregion
---#region OBB Bounds Functions
-
----@class OBB: { pos:vector, rot:quaternion, size:vector }|transform
-
----Converts an Axis Aligned Bounding Box to a Oriented Bounding Box
----@param aa vector
----@param bb vector
----@return OBB
 function AutoAABBToOBB(aa, bb)
 	local center = VecLerp(bb, aa, 0.5)
 	local size = VecSub(bb, aa)
 	return { pos = center, rot = QuatEuler(), size = size }
 end
 
----Defines a Oriented Bounding Box
----@param center vector
----@param rot quaternion
----@param size vector|number?
----@return table
 function AutoOBB(center, rot, size)
 	return {
 		pos = center or Vec(),
@@ -1252,9 +845,6 @@
 	}
 end
 
----Returns the corners of a Oriented Bounding Box
----@param obb OBB
----@return { xyz:table, Xyz:table, xYz:table, xyZ:table, XYz:table, XyZ:table, xYZ:table, XYZ:table }
 function AutoGetOBBCorners(obb)
 	local corners = {}
 	
@@ -1272,10 +862,6 @@
 	return corners
 end
 
----Returns the planes and corners representing the faces of a Oriented Bounding Box
----@param obb OBB
----@return { z:plane, zn:plane, x:plane, xn:plane, y:plane, yn:plane }
----@return { xyz:table, Xyz:table, xYz:table, xyZ:table, XYz:table, XyZ:table, xYZ:table, XYZ:table }
 function AutoGetOBBFaces(obb)
 	local corners = AutoGetOBBCorners(obb)
 	
@@ -1314,9 +900,6 @@
 	return faces, corners
 end
 
----Returns a table representing the lines connecting the sides of a Oriented Bounding Box
----@param obb OBB
----@return table<{ [1]:vector, [2]:vector }>
 function AutoOBBLines(obb)
 	local c = AutoGetOBBCorners(obb)
 	
@@ -1338,8 +921,6 @@
 	}
 end
 
----@param shape shape_handle
----@return OBB
 function AutoGetShapeOBB(shape, local_space)
 	local transform = local_space and Transform() or GetShapeWorldTransform(shape)
 	local x, y, z, scale = GetShapeSize(shape)
@@ -1349,13 +930,6 @@
 	return AutoOBB(center, transform.rot, size)
 end
 
----Draws a given Oriented Bounding Box
----@param obb OBB
----@param red number? Default is 0
----@param green number? Default is 0
----@param blue number? Default is 0
----@param alpha number? Default is 1
----@param linefunction function? Default is DebugLine
 function AutoDrawOBB(obb, red, green, blue, alpha, linefunction)
 	local lines = AutoOBBLines(obb)
 	
@@ -1365,21 +939,10 @@
 	end
 end
 
---#endregion
---#region Plane Functions
-
----@class plane: { pos:vector, rot:quaternion, size:{ [1]:number, [2]:number } }|transform
-
----@param pos vector
----@param rot quaternion
----@param size { [1]:number, [2]:number }
----@return plane
 function AutoPlane(pos, rot, size)
 	return { pos = pos or Vec(), rot = rot or Quat(), size = size or { 1, 1 } }
 end
 
----@param plane plane
----@return { [1]:vector, [2]:vector, [3]:vector, [4]:vector }
 function AutoGetPlaneCorners(plane)
 	local size = VecScale(plane.size, 0.5)
 	
@@ -1397,11 +960,6 @@
 	return { corner1, corner2, corner3, corner4 }
 end
 
----@param plane plane
----@param startPos vector
----@param direction vector
----@param oneway boolean?
----@return { hit:boolean, intersection:vector, normal:vector, dist:number, dot:number }
 function AutoRaycastPlane(plane, startPos, direction, oneway)
 	local pos = plane.pos or Vec(0, 0, 0)
 	local rot = plane.rot or Quat()
@@ -1458,15 +1016,6 @@
 	end
 end
 
----@param plane plane
----@param pattern 0|1|2|3
----@param patternstrength number
----@param oneway boolean?
----@param r number?
----@param g number?
----@param b number?
----@param a number?
----@param linefunction function?
 function AutoDrawPlane(plane, pattern, patternstrength, oneway, r, g, b, a, linefunction)
 	local pos = plane.pos or Vec(0, 0, 0)
 	local rot = plane.rot or Quat()
@@ -1506,7 +1055,7 @@
 			linefunction(subH1, subH2, r, g, b, a)
 			linefunction(subV1, subV2, r, g, b, a)
 		end
-	elseif pattern > 0 then
+	elseif pattern ~= 0 then
 		linefunction(corner1, corner2, r, g, b, a)
 		linefunction(corner2, corner3, r, g, b, a)
 		linefunction(corner3, corner4, r, g, b, a)
@@ -1541,9 +1090,6 @@
 	end
 end
 
---#endregion
---#region Sphere Functions
-
 function AutoFibonacciSphere(numPoints, sphere_origin, sphere_radius, y_multi)
     local points = {}
     local phi = math.pi * (3.0 - math.sqrt(5.0)) -- Golden angle in radians
@@ -1566,11 +1112,6 @@
     return points
 end
 
----@param sphere_origin vector Origin of the sphere
----@param sphere_radius number Radius of the sphere
----@param quality number? Default is 1
----@param draw_function function? Function used for drawing. Default is `DebugLine`
----@vararg any draw_parameters Parameters fed into `draw_function`
 function AutoDrawSphereTangent(sphere_origin, sphere_radius, quality, draw_function, ... )
 	local camera = GetCameraTransform()
 	local camera_up = AutoTransformUp(camera)
@@ -1591,11 +1132,6 @@
 	draw_function(last_point, VecAdd(sphere_origin, VecScale(cross, sphere_radius)), ... )
 end
 
----@param sphere_origin vector
----@param sphere_radius number
----@param startPos vector
----@param direction vector
----@return { hit:boolean, intersections:{ [1]:vector, [2]:vector }, normals:{ [1]:vector, [2]:vector }, dists:{ [1]:number, [2]:number } }
 function AutoRaycastSphere(sphere_origin, sphere_radius, startPos, direction)
     local center = sphere_origin or Vec(0, 0, 0)
     local radius = sphere_radius or 1
@@ -1645,16 +1181,6 @@
     }
 end
 
---#endregion
---#region Octree Functions
-
----Undocumented
----@param BoundsAA vector
----@param BoundsBB vector
----@param Layers number
----@param conditionalFuction function
----@param _layer number?
----@return table
 function AutoProcessOctree(BoundsAA, BoundsBB, Layers, conditionalFuction, _layer)
 	_layer = _layer or 1
 	if _layer >= (Layers or 5) + 1 then return end
@@ -1681,11 +1207,6 @@
 	return node
 end
 
----Undocumented
----@param aa vector
----@param bb vector
----@return boolean
----@return table
 function AutoQueryBoundsForBody(aa, bb)
 	QueryRequire('physical large')
 	local mid = VecLerp(aa, bb, 0.5)
@@ -1694,10 +1215,6 @@
 	return hit, { pos = point, normal = normal, shape }
 end
 
----Draws the Octree from AutoProcessOctree
----@param node table
----@param layer number
----@param drawfunction function?
 function AutoDrawOctree(node, layer, drawfunction)
 	if node == nil then return end
 	
@@ -1721,10 +1238,6 @@
 	end
 end
 
---#endregion
---#region Point Physics
-
----Creates a Point Physics Simulation Instance
 function AutoSimInstance()
 	local t = {
 		Points = {
@@ -1895,21 +1408,6 @@
 	return t
 end
 
---#endregion
---#region Secondary Motion
-
---Previously known as Second Order System
---Huge Thanks to Mathias#1325 for work on the Quaternion Functions
-
----@class Secondary_Motion_Data: table
-
----Returns a table representing a Second Order System (SOS) that can be used to make secondary motion
----@param initial number|table<number>
----@param frequency number
----@param dampening number
----@param response number
----@param raw_k boolean?
----@return Secondary_Motion_Data
 function AutoSM_Define(initial, frequency, dampening, response, raw_k)
 	local sosdata = {
 		type = type(initial) == 'table' and 'table' or 'single',
@@ -1941,13 +1439,6 @@
 	return sosdata
 end
 
----Returns a table representing a Second Order System (SOS) that can be used to make secondary motion
----@param initial number|table<number>
----@param frequency number
----@param dampening number
----@param response number
----@param raw_k boolean?
----@return Secondary_Motion_Data
 function AutoSM_DefineQuat(initial, frequency, dampening, response, raw_k)
 	local sosdata = {
 		type = 'quaternion',
@@ -1966,11 +1457,6 @@
 	return sosdata
 end
 
----Updates the state of the Second Order System (SOS) towards the target value, over the specified timestep.
----This function is used in conjunction with the AutoSM_Define
----@param sm Secondary_Motion_Data
----@param target number|table<number>
----@param timestep number?
 function AutoSM_Update(sm, target, timestep)
 	timestep = timestep or GetTimeStep()
 	
@@ -2016,9 +1502,6 @@
 	end
 end
 
----Returns the current value of a Second Order System
----@param sm Secondary_Motion_Data
----@return unknown
 function AutoSM_Get(sm)
 	if sm.type ~= 'table' then
 		return sm.data.current
@@ -2032,9 +1515,6 @@
 	end
 end
 
----Returns the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@return unknown
 function AutoSM_GetVelocity(sm)
 	if sm.type ~= 'table' then
 		return sm.data.velocity
@@ -2043,10 +1523,6 @@
 	end
 end
 
----Sets the current values of a Second Order System
----@param sm Secondary_Motion_Data
----@param target number|table<number>|quaternion
----@param keep_velocity boolean?
 function AutoSM_Set(sm, target, keep_velocity, keep_previous)
 	if sm.type ~= 'table' then
 		sm.data.current = target
@@ -2063,9 +1539,6 @@
 	end
 end
 
----Sets the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@param velocity number|table<number>
 function AutoSM_SetVelocity(sm, velocity)
 	if sm.type == 'single' then
 		sm.data.velocity = velocity
@@ -2078,9 +1551,6 @@
 	end
 end
 
----Adds a amount to the current velocity of a Second Order System
----@param sm Secondary_Motion_Data
----@param velocity number|table<number>
 function AutoSM_AddVelocity(sm, velocity)
 	if sm.type == 'single' then
 		sm.data.velocity = sm.data.velocity + velocity
@@ -2093,12 +1563,6 @@
 	end
 end
 
----Recalculates The K values for a Second Order System
----@param sm Secondary_Motion_Data
----@param frequency number
----@param dampening number
----@param response number
----@param raw_k boolean?
 function AutoSM_RecalculateK(sm, frequency, dampening, response, raw_k)
 	sm.k_values = {
 		raw_k and frequency or (dampening / (math.pi * frequency)),
@@ -2107,12 +1571,6 @@
 	}
 end
 
---#endregion
---#region Table Functions
-
----Returns the amount of elements in the given list.
----@param t table
----@return integer
 function AutoTableCount(t)
 	local c = 0
 	for i in pairs(t) do
@@ -2130,10 +1588,6 @@
 	return returns
 end
 
----Repeats a value `v`, `r` amount of times
----@param v any
----@param r integer
----@return table
 function AutoTableRepeatValue(v, r)
 	local t = {}
 	for i=1,r do
@@ -2142,18 +1596,12 @@
 	return t
 end
 
----Concats Table 2 onto the end of Table 1, does not return anything
----@param t1 table
----@param t2 table
 function AutoTableConcat(t1, t2)
 	for i = 1, #t2 do
 		t1[#t1 + 1] = t2[i]
 	end
 end
 
----Merges two tables together, does not return anything
----@param base table
----@param overwrite table
 function AutoTableMerge(base, overwrite)
 	for k, v in pairs(overwrite) do
 		if type(v) == "table" then
@@ -2168,10 +1616,6 @@
 	end
 end
 
----A lambda like function for returning a table's key's values.
----@param t table
----@param key any
----@return table
 function AutoTableSub(t, key)
 	local _t = {}
 	for i, v in pairs(t) do
@@ -2180,11 +1624,6 @@
 	return _t
 end
 
----A lambda like function for returning a table's key's values.
----Same as AutoTableSub, but uses ipairs instead
----@param t table
----@param key any
----@return table
 function AutoTableSubi(t, key)
 	local _t = {}
 	for i, v in ipairs(t) do
@@ -2193,9 +1632,6 @@
 	return _t
 end
 
----Swaps the keys and the values of a table
----@param t table
----@return table
 function AutoTableSwapKeysAndValues(t)
 	local _t = {}
 	for k, v in pairs(t) do
@@ -2204,25 +1640,12 @@
 	return _t
 end
 
----Equivalent to
----```
----for i, v in pairs(t) do
----    v[key] = tset[i]
----end
----```
----@param t table
----@param key any
----@param tset table
 function AutoTableAppend(t, key, tset)
 	for i, v in pairs(t) do
 		v[key] = tset[i]
 	end
 end
 
----Returns true and the index if the v is in t, otherwise returns false and nil
----@param t table
----@param v any
----@return boolean, unknown
 function AutoTableContains(t, v)
 	for i, v2 in ipairs(t) do
 		if v == v2 then
@@ -2232,18 +1655,10 @@
 	return false, nil
 end
 
----Returns the Last item of a given list
----@param t table
----@return any
 function AutoTableLast(t)
 	return t[AutoTableCount(t)]
 end
 
----Copy a Table Recursivly Stolen from http://lua-users.org/wiki/CopyTable
----@generic T : table
----@param orig T
----@param copies table?
----@return T
 function AutoTableDeepCopy(orig, copies)
 	copies = copies or {}
 	local orig_type = type(orig)
@@ -2265,20 +1680,10 @@
 	return copy
 end
 
---#endregion
---#region Utility Functions
-
----If val is nil, return default instead
----@param v any
----@param default any
----@return any
 function AutoDefault(v, default)
 	if v == nil then return default else return v end
 end
 
----Calls function or table of functions `f` and gives `...` as input parameters
----@param f function|table<function>
----@vararg any
 function AutoExecute(f, ...)
 	if not f then return end
 	
@@ -2293,11 +1698,6 @@
 	end
 end
 
----Calls VecLerp on a table of Vectors
----@param a table A table of Vectors
----@param b table A table of Vectors the same size of a
----@param t number
----@return table
 function AutoVecTableLerp(a, b, t)
 	local c = {}
 	for k, _ in pairs(a) do
@@ -2306,11 +1706,6 @@
 	return c
 end
 
----Calls VecLerp on a table of Vectors
----@param a table A table of values
----@param b table A table of values the same size of a
----@param t number
----@return table
 function AutoTableLerp(a, b, t)
 	local c = {}
 	for k, _ in pairs(a) do
@@ -2319,21 +1714,10 @@
 	return c
 end
 
----Scales a transform, is the equivelent of (s)lerping the position and rotation from Vec(), Quat()
----@param t transform
----@param s number
----@param s2 number?
----@return transform
 function AutoTransformScale(t, s, s2)
 	return AutoTransformLerp(Transform(Vec(), Quat()), t, s, s2)
 end
 
----Returns a Linear Interpolated Transform, Interpolated by t.
----@param a transform
----@param b transform
----@param t number
----@param t2 number?
----@return table
 function AutoTransformLerp(a, b, t, t2)
 	if t2 == nil then
 		t2 = t
@@ -2344,43 +1728,22 @@
 )
 end
 
----Equivalent to `QuatRotateVec(t.rot, Vec(0, 0, -(scale or 1)))`
----@param t transform
----@param scale number?
----@return vector
 function AutoTransformFwd(t, scale)
 	return QuatRotateVec(t.rot, Vec(0, 0, -(scale or 1)))
 end
 
----Equivalent to `QuatRotateVec(t.rot, Vec(0, scale or 1))`
----@param t transform
----@param scale number?
----@return vector
 function AutoTransformUp(t, scale)
 	return QuatRotateVec(t.rot, Vec(0, scale or 1))
 end
 
----Equivalent to `QuatRotateVec(t.rot, Vec(scale or 1))`
----@param t transform
----@param scale number?
----@return vector
 function AutoTransformRight(t, scale)
 	return QuatRotateVec(t.rot, Vec(scale or 1))
 end
 
----Equivalent to `Transform(TransformToParentPoint(t, offset), t.rot)`
----@param t transform
----@param offset vector
----@return transform
 function AutoTransformOffset(t, offset)
 	return Transform(TransformToParentPoint(t, offset), t.rot)
 end
 
---- Rotates a transform around a given point
----@param transform transform The original transform
----@param point vector The point around which to rotate
----@param rotation quaternion The rotation to apply
----@return transform rotated_transform The rotated transform
 function AutoTransformRotateAroundPoint(transform, point, rotation)
 	local transform_relative_to_point = Transform(VecSub(transform.pos, point), transform.rot)
 	local rotated_transform = TransformToParentTransform(Transform(Vec(), rotation), transform_relative_to_point)
@@ -2389,26 +1752,15 @@
     return rotated_transform
 end
 
----Equivalent to `{ GetQuatEuler(quat) }`
----@param quat quaternion
----@return vector
 function AutoEulerTable(quat)
 	return { GetQuatEuler(quat) }
 end
 
----Returns a Vector for easy use when put into a parameter for xml
----@param vec any
----@param round number
----@return string
 function AutoVecToXML(vec, round)
 	round = AutoDefault(round, 0)
 	return AutoRound(vec[1], round) .. ' ' .. AutoRound(vec[2], round) .. ' ' .. AutoRound(vec[3], round)
 end
 
----Splits a string by a separator
----@param inputstr string
----@param sep string
----@return table
 function AutoSplit(inputstr, sep, number)
 	if sep == nil then
 		sep = "%s"
@@ -2420,19 +1772,11 @@
 	return t
 end
 
----Converts a string to be capitalized following the Camel Case pattern
----@param str string
----@return string
 function AutoCamelCase(str)
 	local subbed = str:gsub('_', ' ')
 	return string.gsub(" " .. subbed, "%W%l", string.upper):sub(2)
 end
 
----Returns 3 values from HSV color space from RGB color space
----@param hue number? The hue from 0 to 1
----@param sat number? The saturation from 0 to 1
----@param val number? The value from 0 to 1
----@return number, number, number Returns the red, green, blue of the given hue, saturation, value
 function AutoHSVToRGB(hue, sat, val)
 	local r, g, b
 	
@@ -2455,11 +1799,6 @@
 	return r, g, b
 end
 
----Returns 3 values from RGB color space from HSV color space
----@param r number? The red from 0 to 1
----@param g number? The green from 0 to 1
----@param b number? The blue from 0 to 1
----@return number, number, number Returns the hue, the saturation, and the value
 function AutoRGBToHSV(r, g, b)
 	r, g, b = r, g, b
 	local max, min = math.max(r, g, b), math.min(r, g, b)
@@ -2484,9 +1823,6 @@
 	return h, s, v
 end
 
----Converts a hex code or a table of hex codes to RGB color space
----@param hex string|table<string>
----@return number|table
 function AutoHEXtoRGB(hex)
 	local function f(x, p)
 		x = x:gsub("#", "")
@@ -2504,11 +1840,6 @@
 	end
 end
 
----Converts an RGB color code or a table of RGB color codes to hexadecimal color space
----@param r number|table<number> Red component (0-1) or table of RGB color codes
----@param g number Green component (0-1) (optional)
----@param b number Blue component (0-1) (optional)
----@return string|table<string> Hexadecimal color code or table of hex codes
 function AutoRGBtoHEX(r, g, b)
 	local function f(x)
 		local hx = string.format("%02X", math.floor(x * 255))
@@ -2528,9 +1859,6 @@
 	end
 end
 
----Performs `:byte()` on each character of a given string
----@param str string
----@return table<number>
 function AutoStringToByteTable(str)
 	local t = {}
 	for i = 1, #str do
@@ -2539,11 +1867,6 @@
 	return t
 end
 
----Performs `:char()` on each number of a given table, returning a string
----
----The inverse of AutoStringToByteTable
----@param t table<number>
----@return string
 function AutoByteTableToString(t)
 	local str = ''
 	for i, b in ipairs(t) do
@@ -2552,18 +1875,12 @@
 	return str
 end
 
---#endregion
---#region Game Functions
-
----Usually, the Primary Menu Button only is suppose to work in the mod's level, this is a work around to have it work in any level.
----@param title string
----@return boolean
 function AutoPrimaryMenuButton(title)
 	local value = PauseMenuButton(title, true)
 	
 	for _, item in pairs(ListKeys('game.pausemenu.items')) do
 		if GetString(AutoKey('game.pausemenu.items', item)) == title then
-			SetInt('game.pausemenu.primary', item)
+			SetInt('game.pausemenu.primary', item, true)
 			break
 		end
 	end
@@ -2571,10 +1888,6 @@
 	return value
 end
 
----Goes through a table and performs Delete() on each element
----@param t table<entity_handle>
----@param CheckIfValid boolean?
----@return table<{handle:entity_handle, type:entity_type, valid:boolean}>
 function AutoDeleteHandles(t, CheckIfValid)
 	local list = {}
 	for k, v in pairs(t) do
@@ -2605,10 +1918,6 @@
 	end
 end
 
-
----Creates a list from a table of entity handles, containing the handle and it's type. If the handle is invalid then the type will be false.
----@param t table<entity_handle>
----@return table<{handle:entity_handle, type:entity_type}>
 function AutoListHandleTypes(t)
 	local nt = {}
 	for key, value in pairs(t) do
@@ -2617,30 +1926,17 @@
 	return nt
 end
 
----Spawn in a script node in the game world.
----@param path td_path
----@param ... string|number?
----@return script_handle
 function AutoSpawnScript(path, ...)
 	local f = [[<script file="%s" param0="%s" param1="%s" param2="%s" param3="%s"/>]]
 	local param = { arg[1] or '', arg[2] or '', arg[3] or '', arg[4] or '' }
 	return Spawn((f):format(path, unpack(param)), Transform())[1]
 end
 
----Spawn in a voxscript node in the game world. No parameters
----@param path td_path
----@return script_handle
 function AutoSpawnVoxScript(path)
 	local f = [[<voxscript file="%s"/>]]
 	return Spawn((f):format(path), Transform())[1]
 end
 
----Attempts to get the handle of the current script by abusing pause menu item keys
----
----May not work if a pause menu button is already being created from the script
----
----Original coded from Thomasims
----@return script_handle
 function AutoGetScriptHandle()
 	local id = tostring(math.random())
 	PauseMenuButton(id)
@@ -2655,13 +1951,6 @@
 	return 0 -- Compatability for scripts run in a ui environment like Command('game.startui')
 end
 
----A Wrapper for QueryRaycast; comes with some extra features.
----@param origin vector
----@param direction vector
----@param maxDist number
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, intersection:vector, dist:number, normal:vector, shape:shape_handle, body:body_handle, dir:vector, dot:number, reflection:vector }
 function AutoRaycast(origin, direction, maxDist, radius, rejectTransparent)
 	direction = direction and VecNormalize(direction) or nil
 	
@@ -2676,38 +1965,19 @@
 	return data
 end
 
----AutoRaycast from point A to point B. The distance will default to the distance between the points, but can be set.
----@param pointA vector
----@param pointB vector
----@param manualDistance number?
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, dist:number, normal:vector, shape:shape_handle, intersection:vector, body:body_handle, dir:vector, dot:number, reflection:vector }
 function AutoRaycastTo(pointA, pointB, manualDistance, radius, rejectTransparent)
 	local diff = VecSub(pointB, pointA)
 	local distance_between_points = VecLength(diff)
 	return AutoRaycast(pointA, diff, manualDistance or distance_between_points, radius, rejectTransparent), distance_between_points
 end
 
----AutoRaycast using the camera or player camera as the origin and direction
----@param usePlayerCamera boolean
----@param maxDist number
----@param radius number?
----@param rejectTransparent boolean?
----@return { hit:boolean, dist:number, normal:vector, shape:shape_handle, intersection:vector, body:body_handle, dir:vector, dot:number, reflection:vector }
----@return transform cameraTransform
----@return vector cameraForward
 function AutoRaycastCamera(usePlayerCamera, maxDist, radius, rejectTransparent)
-	local trans = usePlayerCamera and GetPlayerCameraTransform() or GetCameraTransform()
+	local trans = usePlayerCamera and GetPlayerCameraTransform(playerId) or GetCameraTransform()
 	local fwd = AutoTransformFwd(trans)
 	
 	return AutoRaycast(trans.pos, fwd, maxDist, radius, rejectTransparent), trans, fwd
 end
 
----A Wrapper for QueryClosestPoint; comes with some extra features.
----@param origin vector
----@param maxDist number
----@return { hit:boolean, point:vector, normal:vector, shape:shape_handle, body:body_handle, dist:number, dir:vector, dot:number, reflection:vector }
 function AutoQueryClosest(origin, maxDist)
 	local data = {}
 	data.hit, data.point, data.normal, data.shape = QueryClosestPoint(origin, maxDist)
@@ -2729,10 +1999,6 @@
 	return data
 end
 
----A Wrapper for GetBodyClosestPoint; comes with some extra features.
----@param body body_handle
----@param origin vector
----@return { hit:boolean, point:vector, normal:vector, shape:shape_handle, body:body_handle, dist:number, dir:vector, dot:number, reflection:vector }
 function AutoQueryClosestBody(body, origin)
 	local data = {}
 	data.hit, data.point, data.normal, data.shape = GetBodyClosestPoint(body, origin)
@@ -2752,10 +2018,6 @@
 	return data
 end
 
----A Wrapper for GetShapeClosestPoint; comes with some extra features.
----@param shape shape_handle
----@param origin vector
----@return { hit:boolean, point:vector, normal:vector, dist:number, dir:vector, dot:number, reflection:vector, shape:shape_handle, body:body_handle }
 function AutoQueryClosestShape(shape, origin)
 	local data = {}
 	data.hit, data.point, data.normal = GetShapeClosestPoint(shape, origin)
@@ -2776,13 +2038,6 @@
 	return data
 end
 
----Unsteps a query from QueryClosestPoint
----
----Thank you Dima and Thomasims.
----@param shape shape_handle
----@param query_origin vector
----@param voxel_stepped_point vector
----@return vector
 function AutoResolveUnsteppedPoint(shape, query_origin, voxel_stepped_point)
     local shape_world_transform = GetShapeWorldTransform(shape)
     local relative_query_origin = TransformToLocalPoint(shape_world_transform, query_origin)
@@ -2795,9 +2050,6 @@
     return TransformToParentPoint(shape_world_transform, applied_offset) -- Extrapolated
 end
 
----@param shapes_a shape_handle[]
----@param shapes_b shape_handle[]
----@return boolean
 function AutoIsShapesTouchingShapes(shapes_a, shapes_b)
 	for i=1, #shapes_a do
 		local sa = shapes_a[i]
@@ -2810,9 +2062,6 @@
 	return false
 end
 
----Goes through each shape on a body and adds up their voxel count
----@param body body_handle
----@return integer
 function AutoGetBodyVoxels(body)
 	local v = 0
 	for _, s in pairs(GetBodyShapes(body)) do
@@ -2821,11 +2070,6 @@
 	return v
 end
 
----Scales the velocity of a body by `scale`
----@param body body_handle
----@param scale number
----@return vector scaled
----@return vector orginal
 function AutoScaleBodyVelocity(body, scale)
 	local orginal = GetBodyVelocity(body)
 	local scaled = VecScale(orginal, scale)
@@ -2833,11 +2077,6 @@
 	return scaled, orginal
 end
 
----Scales the angular velocity of a body by `scale`
----@param body body_handle
----@param scale number
----@return vector scaled
----@return vector orginal
 function AutoScaleBodyAngularVelocity(body, scale)
 	local current = GetBodyAngularVelocity(body)
 	local scaled = VecScale(current, scale)
@@ -2845,10 +2084,6 @@
 	return scaled, current
 end
 
----Gets the angle from a point to the forward direction of a transform
----@param point vector
----@param fromtrans transform
----@return number
 function AutoPointToAngle(point, fromtrans)
 	fromtrans = AutoDefault(fromtrans, GetCameraTransform())
 	
@@ -2859,14 +2094,6 @@
 	return math.deg(math.acos(dot))
 end
 
----Checks if a point is in the view using a transform acting as the "Camera"
----@param point vector
----@param from_transform transform? The Transform acting as the camera, Default is the Player's Camera
----@param angle number? The Angle at which the point can be seen from, Default is the Player's FOV set in the options menu
----@param raycastcheck boolean? Check to make sure that the point is not obscured, Default is true
----@return boolean seen If the point is in View
----@return number? angle The Angle the point is away from the center of the looking direction
----@return number? distance The Distance from the point to fromtrans
 function AutoPointInView(point, from_transform, angle, raycastcheck, raycasterror)
 	from_transform = AutoDefault(from_transform, GetCameraTransform())
 	angle = AutoDefault(angle, GetInt('options.gfx.fov'))
@@ -2890,7 +2117,7 @@
 		if raycastcheck then
 			local hit, hitdist = QueryRaycast(from_transform.pos, fromtopointdir, distance, 0, true)
 			if hit then
-				if raycasterror > 0 then
+				if raycasterror ~= 0 then
 					local hitpoint = VecAdd(from_transform.pos, VecScale(fromtopointdir, hitdist))
 					if AutoVecDist(hitpoint, point) > raycasterror then
 						seen = false
@@ -2905,11 +2132,6 @@
 	return seen, dotangle, distance
 end
 
----Gets the direction the player is inputting and creates a vector.
----
----`{ horizontal, 0, vertical }`
----@param length number?
----@return vector
 function AutoPlayerInputDir(length)
 	return VecScale({
 		-InputValue('left') + InputValue('right'),
@@ -2918,10 +2140,6 @@
 	}, length or 1)
 end
 
----Get the last Path Query as a path of points
----@param precision number The Accuracy
----@return table<vector>
----@return vector "Last Point"
 function AutoRetrievePath(precision)
 	precision = AutoDefault(precision, 0.2)
 	
@@ -2936,8 +2154,6 @@
 	return path, path[#path]
 end
 
----Reject a table of bodies for the next Query
----@param bodies body_handle[]
 function AutoQueryRejectBodies(bodies)
 	for _, h in pairs(bodies) do
 		if h then
@@ -2946,8 +2162,6 @@
 	end
 end
 
----Reject a table of shapes for the next Query
----@param shapes shape_handle[]
 function AutoQueryRejectShapes(shapes)
 	for _, h in pairs(shapes) do
 		if h then
@@ -2956,8 +2170,6 @@
 	end
 end
 
----Finds and rejects all shapes that do not have a given tag
----@param tag string
 function AutoRejectShapesWithoutTag(tag, global)
 	local all = FindShapes(nil, global)
 	local keepers = FindShapes(tag, global)
@@ -2971,10 +2183,6 @@
 	end
 end
 
----Set the collision filter for the shapes owned by a body
----@param body body_handle
----@param layer number
----@param masknummber number bitmask
 function AutoSetBodyCollisionFilter(body, layer, masknummber)
 	local shapes = GetBodyShapes(body)
 	for i in pairs(shapes) do
@@ -2982,30 +2190,16 @@
 	end
 end
 
----Get the Center of Mass of a body in World space
----@param body body_handle
----@return vector
 function AutoWorldCenterOfMass(body)
 	local trans = GetBodyTransform(body)
 	local pos = TransformToParentPoint(trans, GetBodyCenterOfMass(body))
 	return pos
 end
 
----Adds the velocity and angualr velocity of a body
----@param body body_handle
----@return number
 function AutoSpeed(body)
 	return VecLength(GetBodyVelocity(body)) + VecLength(GetBodyAngularVelocity(body))
 end
 
----Attempt to predict the position of a body in time
----@param body body_handle
----@param time number
----@param raycast boolean? Check and Halt on Collision, Default is false
----@param funcbefore function?
----@return table<vector> log
----@return vector vel
----@return vector normal
 function AutoPredictPosition(body, time, raycast, funcbefore)
 	raycast = AutoDefault(raycast, false)
 	local point = {
@@ -3039,17 +2233,11 @@
 	return log, point.vel, normal
 end
 
----Attempt to predict the position of the player in time
----@param time number
----@param raycast boolean? Check and Halt on Collision, Default is false
----@return table<vector> log
----@return vector vel
----@return vector normal
 function AutoPredictPlayerPosition(time, raycast)
 	raycast = AutoDefault(raycast, false)
-	local player = GetPlayerTransform(true)
+	local player = GetPlayerTransform(playerId, true)
 	local pos = player.pos
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local log = { VecCopy(pos) }
 	local normal = Vec(0, 1, 0)
 	
@@ -3070,9 +2258,6 @@
 	return log, vel, normal
 end
 
---#endregion
---#region Shape Utility
-
 function AutoWorldToShapeVoxelIndex(shape, world_point)
 	local shape_size = { GetShapeSize(shape) }
 	local shape_transform = GetShapeWorldTransform(shape)
@@ -3104,11 +2289,6 @@
 	return body
 end
 
----SplitShape with some extra stuff to put each shape under a dynamic body - copying the velocity of the original shape.
----@param shape shape_handle
----@param removeResidual boolean?
----@param static boolean?
----@return body_handle[]
 function AutoSplitShapeIntoBodies(shape, removeResidual, static)
 	local new_bodies = {}
 
@@ -3119,14 +2299,6 @@
 	return new_bodies
 end
 
----Creates a new shape offset a 1x1x1 voxel in place of an existing voxel.
----@param shape shape_handle
----@param voxel_position vector
----@param keep_original boolean?
----@param no_body boolean?
----@param reject_materials material[]?
----@return body_handle|false
----@return shape_handle|false
 function AutoPopVoxel(shape, voxel_position, keep_original, no_body, reject_materials)
 	local material = { GetShapeMaterialAtIndex(shape, unpack(voxel_position)) }
 	if material[1] == '' or (reject_materials and AutoTableContains(reject_materials, material[1])) then return false, false end
@@ -3166,13 +2338,6 @@
 	return body, new_shape
 end
 
----A function inspired by the Liquify Mod.
----@param shape shape_handle
----@param keep_original boolean?
----@param inherit_tags boolean?
----@param no_bodies boolean?
----@return body_handle[]
----@return shape_handle[]
 function AutoLiquifyShape(shape, keep_original, inherit_tags, no_bodies)
 	local shape_size = { GetShapeSize(shape) }
 
@@ -3210,16 +2375,6 @@
 	return bodies, shapes
 end
 
----@param shape shape_handle
----@param world_point vector
----@param inner_radius number
----@param outer_radius number
----@param pop_voxels boolean
----@param pop_reject_materials any
----@param pop_voxels_inherit_tags boolean
----@param pop_voxels_no_bodies boolean
----@return body_handle[]
----@return shape_handle[]
 function AutoCarveSphere(shape, world_point, inner_radius, outer_radius, pop_voxels, pop_reject_materials, pop_voxels_inherit_tags, pop_voxels_no_bodies)
     local popped_bodies = {}
     local popped_shapes = {}
@@ -3275,46 +2430,6 @@
     return popped_bodies, popped_shapes
 end
 
---#endregion
---#region Environment
-
----@class environment
----@field ambience { [1]:td_path, [2]:number }
----@field ambient number
----@field ambientexponent number
----@field brightness number
----@field constant { [1]:number, [2]:number, [3]:number }
----@field exposure { [1]:number, [2]:number }
----@field fogcolor { [1]:number, [2]:number, [3]:number }
----@field fogparams { [1]:number, [2]:number, [3]:number, [4]:number }
----@field fogscale number
----@field nightlight boolean
----@field puddleamount number
----@field puddlesize number
----@field rain number
----@field skybox td_path
----@field skyboxbrightness number
----@field skyboxrot number
----@field skyboxtint { [1]:number, [2]:number, [3]:number }
----@field slippery number
----@field snowamount { [1]:number, [2]:number }
----@field snowdir { [1]:number, [2]:number, [3]:number, [4]:number }
----@field snowonground boolean
----@field sunbrightness number
----@field suncolortint { [1]:number, [2]:number, [3]:number }
----@field sundir { [1]:number, [2]:number, [3]:number }|'auto'|0
----@field sunfogscale number
----@field sunglare number
----@field sunlength number
----@field sunspread number
----@field waterhurt number
----@field wetness number
----@field wind { [1]:number, [2]:number, [3]:number }
-
----@type environment_property
-
----Returns a table of every property of the current environment
----@return environment
 function AutoGetEnvironment()
 	local params = {
 		"ambient",
@@ -3358,8 +2473,6 @@
 	return assembled
 end
 
----Sets every environment property of AutoGetEnvironment
----@param Environment environment
 function AutoSetEnvironment(Environment)
 	for k, v in pairs(Environment) do
 		if type(v) == 'table' then
@@ -3370,12 +2483,6 @@
 	end
 end
 
----Draws Sprites around the camera to provide the illusion of a flat background
----@param r number
----@param g number
----@param b number
----@param a number
----@param sprite sprite_handle? Defaults to TD's 'ui/menu/white-32.png'
 function AutoFlatBackground(r, g, b, a, sprite, distance)
 	r = AutoDefault(r, 0)
 	g = AutoDefault(g, 0)
@@ -3401,11 +2508,6 @@
 end
 end
 
----Returns and environemnt that eliminates as much lighting as possible, making colors look flat.
----
----Requires a flat DDS file.
----@param pathToDDS td_path
----@return environment
 function AutoFlatEnvironment(pathToDDS)
 	return {
 		ambience = { "outdoor/field.ogg", 0 },
@@ -3442,18 +2544,6 @@
 	}
 end
 
---#endregion
---#region Post Processing
-
----@class postprocessing
----@field saturation number
----@field colorbalance { [1]:number, [2]:number, [3]:number }
----@field brightness number
----@field gamma number
----@field bloom number
-
----Returns a table of every property of the current post-processing
----@return postprocessing
 function AutoGetPostProcessing()
 	local params = {
 		'saturation',
@@ -3472,8 +2562,6 @@
 	return assembled
 end
 
----Sets every post-processing property of AutoGetPostProcessing
----@param PostProcessing postprocessing
 function AutoSetPostProcessing(PostProcessing)
 	for k, v in pairs(PostProcessing) do
 		if type(v) == 'table' then
@@ -3484,45 +2572,18 @@
 	end
 end
 
---#endregion
---#region Debug
-
---- Returns the current Line Number.
----
---- This function is adapted from the UMF Framework
----
---- https://github.com/Thomasims/TeardownUMF/blob/master/src/util/debug.lua
----@param level integer? Optional
----@return integer
 function AutoGetCurrentLine(level)
 	level = (level or 0)
 	local _, line = pcall(error, '', level + 3) -- The level + 3 is to get out of error, then out of pcall, then out of this function
 	return tonumber(AutoSplit(line, ':')[2])
 end
 
---- Returns the current Line Number.
----
---- This function is adapted from the UMF Framework
----
---- https://github.com/Thomasims/TeardownUMF/blob/master/src/util/debug.lua
----@param level integer? Optional
----@return string?
 function AutoGetStackTrace(level)
 	level = (level or 0)
 	local _, line = pcall(error, '', level + 3) -- The level + 3 is to get out of error, then out of pcall, then out of this function
 	return line
 end
 
----Creates a neatly formatted string given any value of any type, including tables
----@param t any
----@param round_numbers number|false?
----@param singleline_at number?
----@param show_number_keys boolean?
----@param ignore_keys any[]?
----@param lua_compatible boolean?
----@param indents number?
----@param visited_tables table?
----@return string
 function AutoToString(t, round_numbers, singleline_at, show_number_keys, ignore_keys, lua_compatible, indents, visited_tables)
 	singleline_at = singleline_at or 1
 	indents = indents or 0
@@ -3581,15 +2642,6 @@
 	return str
 end
 
----A Alternative to DebugPrint that uses AutoToString(), works with tables. Returns the value
----@param value any
----@param format_output string?
----@param round_numbers number|false?
----@param singleline_at number?
----@param show_number_keys boolean?
----@param ignore_keys any[]?
----@param lua_compatible boolean?
----@return any
 function AutoInspect(value, format_output, round_numbers, singleline_at, show_number_keys, ignore_keys, lua_compatible)
 	local text = AutoToString(value, round_numbers, singleline_at or 3, show_number_keys, ignore_keys, lua_compatible)
 	local formatted_text = format_output and (string.match(format_output, "%%s") ~= nil and string.format(format_output, text) or format_output .. text) or text
@@ -3605,14 +2657,6 @@
 	return value
 end
 
----AutoInspect that prints to console
----@param value any
----@param singleline_at number?
----@param round_numbers number|false?
----@param show_number_keys boolean?
----@param lua_compatible boolean?
----@param ignore_keys any[]?
----@return any
 function AutoInspectConsole(value, format_output, round_numbers, singleline_at, show_number_keys, ignore_keys, lua_compatible)
 	local text = AutoToString(value, round_numbers, singleline_at or 3, show_number_keys, ignore_keys, lua_compatible)
 	local formatted_text = format_output and (string.match(format_output, "%%s") ~= nil and string.format(format_output, text) or format_output .. text) or text
@@ -3621,33 +2665,15 @@
 	return value
 end
 
----AutoInspect that prints to DebugWatch.
----
----Name will default to current line number
----@param value any
----@param name string?
----@param singleline_at number?
----@param round_numbers number|false?
----@param show_number_keys boolean?
----@param lua_compatible boolean?
----@param ignore_keys any[]?
 function AutoInspectWatch(value, name, round_numbers, singleline_at, show_number_keys, ignore_keys, lua_compatible)
 	if not name then name = 'Inspecting Line ' .. AutoGetCurrentLine(1) end
 	DebugWatch(name, AutoToString(value, round_numbers, singleline_at, show_number_keys, ignore_keys, lua_compatible))
 end
 
----Prints 24 blank lines to quote on quote, "clear the console"
 function AutoClearConsole()
 	for i = 1, 24 do DebugPrint('') end
 end
 
----Draws a Transform
----@generic T : transform|vector
----@param transform T
----@param size number? the size in meters, Default is 0.5
----@param alpha number? Default is 1
----@param draw boolean? Whether to use DebugLine or DrawLine, Default is false (DebugLine)
----@return T
 function AutoDrawTransform(transform, size, alpha, draw)
 	if not transform then return end
 	if not transform['pos'] then
@@ -3681,15 +2707,6 @@
 	return transform
 end
 
----Simply draws a box given a center and the half size.
----@param point vector
----@param halfextents number|vector
----@param r number
----@param g number
----@param b number
----@param a number
----@return vector aa lower bounds point
----@return vector bb upper point
 function AutoDrawBox(point, halfextents, r, g, b, a)
 	local aa, bb = AutoAABBBoxFromPoint(point, halfextents)
 	AutoDrawAABB(aa, bb, r, g, b, a)
@@ -3697,13 +2714,6 @@
 	return aa, bb
 end
 
----Draws a Transform as a Cone
----@param transform transform
----@param sides number? the amount of sides on the cone, Default is 12
----@param angle number? how wide the cone is in degrees, Default is 25
----@param size number? the size in meters, Default is 0.5
----@param color table? Default is 1
----@param draw boolean? Whether to use DebugLine or DrawLine, Default is false (DebugLine)
 function AutoDrawCone(transform, sides, angle, size, color, draw)
 	if not transform['pos'] then
 		DebugPrint('AutoDrawCone given input not a transform')
@@ -3745,15 +2755,6 @@
 	return transform
 end
 
---#endregion
---#region Graphing
-
-AutoGraphs = {}
-
----Creates a Continuous Graph that can be drawn. The given value is added into the graph as the previous ones are kept in memory.
----@param id string
----@param value number
----@param range number? Default is 64
 function AutoGraphContinuous(id, value, range)
 	local Graph = AutoDefault(AutoGraphs[id], {
 		scan = 0,
@@ -3767,12 +2768,6 @@
 	AutoGraphs[id] = Graph
 end
 
----Creates a Graph with values within a range fed into a given function.
----@param id string
----@param rangemin number? Default is 0
----@param rangemax number? Default is 1
----@param func function? Is fed one parameter, a number ranging from rangemin to rangemax, Defaults to a Logisitc Function
----@param steps number? How many steps, or the interval of values taken from the range.
 function AutoGraphFunction(id, rangemin, rangemax, func, steps)
 	rangemin = AutoDefault(rangemin, 0)
 	rangemax = AutoDefault(rangemax, 1)
@@ -3794,13 +2789,6 @@
 	AutoGraphs[id] = Graph
 end
 
----Draws a given graph with some parameters
----@param id string
----@param sizex number width of the graph, Default is 128
----@param sizey number height of the graph, Default is 64
----@param rangemin number? If left nil, then the graph will automatically stretch the values to fill the bottom of the graph. Default is nil
----@param rangemax number? If left nil, then the graph will automatically stretch the values to fill the top of the graph. Default is nil
----@param linewidth number? The line width, Default is 2
 function AutoGraphDraw(id, sizex, sizey, rangemin, rangemax, linewidth)
 	local Graph = AutoGraphs[id]
 	if Graph == nil then error("Graph Doesn't exist, nil") end
@@ -3852,26 +2840,17 @@
 	UiPop()
 end
 
---#endregion
---#region Registry
-
----Concats any amount of strings by adding a single period between them
----@vararg string
----@return string
 function AutoKey(...)
 	return table.concat(arg, '.')
 end
 
----One out of the many methods to convert a registry key to a table
----@param key string
----@return table
 function AutoExpandRegistryKey(key)
 	local t = {}
 	local function delve(k, current)
 		local subkeys = ListKeys(k)
 		local splitkey = AutoSplit(k, '.')
 		local neatkey = splitkey[#splitkey]
-		if #subkeys > 0 then
+		if #subkeys ~= 0 then
 			current[neatkey] = {}
 			for _, subkey in ipairs(subkeys) do
 				delve(AutoKey(k, subkey), current[neatkey])
@@ -3888,137 +2867,46 @@
 	return t
 end
 
----Gets a Int from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default integer
----@return integer
 function AutoKeyDefaultInt(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetInt(path, default)
 	else
-		SetInt(path, default)
+		SetInt(path, default, true)
 		return default
 	end
 end
 
----Gets a Float from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default number
----@return number
 function AutoKeyDefaultFloat(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetFloat(path, default)
 	else
-		SetFloat(path, default)
+		SetFloat(path, default, true)
 		return default
 	end
 end
 
----Gets a String from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default string
----@return string
 function AutoKeyDefaultString(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetString(path, default)
 	else
-		SetString(path, default)
+		SetString(path, default, true)
 		return default
 	end
 end
 
----Gets a Bool from the registry, if the key does not exist, then set the key to the default value and return it.
----@param path string
----@param default boolean
----@return boolean
 function AutoKeyDefaultBool(path, default)
 	if path == nil then error("path nil") end
 	if HasKey(path) then
 		return GetBool(path)
 	else
-		SetBool(path, default)
+		SetBool(path, default, true)
 		return default
 	end
 end
 
-local RegistryTableMeta = {
-	__index = function(self, key)
-		key = key:lower()
-		local path = AutoKey(rawget(self, '__path'), key)
-		if not HasKey(path) then
-			return nil
-		end
-		
-		local type = GetString(AutoKey(path, '__type'))
-		
-		if type == 'table' then
-			return AutoRegistryBindedTable(path)
-		else
-			local str = GetString(path)
-			
-			if type == 'number' then
-				return tonumber(str)
-			end
-			
-			return str
-		end
-	end,
-	__newindex = function(self, key, value)
-		key = key:lower()
-		local path = AutoKey(rawget(self, '__path'), key)
-		
-		local function dive(p, v)
-			if type(v) ~= "table" then
-				SetString(p, v)
-				
-				if type(v) ~= "nil" then
-					SetString(AutoKey(p, '__type'), type(v))
-				end
-			else
-				SetString(AutoKey(p, '__type'), 'table')
-				for k, set in pairs(v) do
-					dive(AutoKey(p, k), set)
-				end
-			end
-		end
-		
-		dive(path, value)
-	end,
-	__call = function(self)
-		local path = rawget(self, '__path')
-		
-		local function dive(p)
-			local keys = ListKeys(p)
-			local full = {}
-			
-			for i = 1, #keys do
-				local child = AutoKey(p, keys[i])
-				
-				if keys[i] ~= '__type' then
-					local t = GetString(AutoKey(child, '__type'))
-					if t == 'table' then
-						full[keys[i]] = dive(child)
-					else
-						local str = GetString(child)
-						local num = tonumber(str)
-						full[keys[i]] = num or str
-					end
-				end
-			end
-			
-			return full
-		end
-		
-		return dive(path)
-	end
-}
-
----Attempts to create a table that when written to, will update the registry, and when read from, will pull from the registry
----@param path string
----@return table
 function AutoRegistryBindedTable(path)
 	local t = {}
 	t.__path = path
@@ -4027,15 +2915,6 @@
 	return t
 end
 
---#endregion
---#region User Interface
-
----Raycasts to an imaginary plane, useful for getting a point in which UIWorldToPixel will not work
----@param origin vector
----@param direction vector
----@param plane_distance number
----@param camera_fov number
----@return number, number
 function AutoUIRaycastPlane(origin, direction, plane_distance, camera_fov)
     local vertical_fov_rad = math.rad(camera_fov)
     local tan_vertical_fov_rad = math.tan(vertical_fov_rad / 2)
@@ -4050,35 +2929,21 @@
     return -intersection[1] * (bounds_x / 2), intersection[2] * (bounds_x / 2)
 end
 
----UiTranslate and UiAlign to the Center
 function AutoUiCenter()
 	UiTranslate(UiCenter(), UiMiddle())
 	UiAlign('center middle')
 end
 
----Returns the bounds, optionally subtracted by some amount
----@param subtract number?
----@return number
----@return number
 function AutoUiBounds(subtract)
 	subtract = subtract or 0
 	return UiWidth() - subtract, UiHeight() - subtract
 end
 
----@param a table
----@param b table?
----@return number
 function AutoUiDistance(a, b)
 	b = b or { 0, 0 }
     return VecLength(VecSub(Vec(a[1], a[2]), Vec(b[1], b[2])))
 end
 
----Draws a line between two points in screen space
----
----Relative to current cursor position
----@param p1 { [1]:number, [2]:number }
----@param p2 { [1]:number, [2]:number }
----@param width integer? Default is 2
 function AutoUiLine(p1, p2, width)
 	width = AutoDefault(width, 2)
 	local angle = math.atan2(p2[1] - p1[1], p2[2] - p1[2]) * 180 / math.pi
@@ -4093,12 +2958,6 @@
 	UiPop()
 end
 
----Draws a cricle out of lines in screen space
----
----Relative to current cursor position
----@param radius number
----@param width integer? Default is 2
----@param steps integer?
 function AutoUiCircle(radius, width, steps)
 	width = width or 2
 	steps = steps or 16
@@ -4122,13 +2981,6 @@
 	end
 end
 
----Draws a Fancy looking Arrow between two points on the screen
----
----Relative to current cursor position
----@param p1 { [1]: number, [2]:number }
----@param p2 { [1]: number, [2]:number }
----@param line_width integer
----@param radius integer
 function AutoUIArrow(p1, p2, line_width, radius)
 	local dir = VecNormalize(VecSub(p2, p1))
 	local angle = math.atan2(unpack(AutoSwizzle(dir, 'yx')))
@@ -4138,7 +2990,7 @@
 	
 	UiPush()
 	
-	if radius > 0 then
+	if radius ~= 0 then
 		UiPush()
 		UiTranslate(unpack(p1))
 		AutoUiCircle(radius, line_width, 32)
@@ -4163,13 +3015,6 @@
 	UiPop()
 end
 
----Draws a Fancy looking Arrow between two points in the world
----
----Relative to current cursor position
----@param p1 vector
----@param p2 vector
----@param line_width integer
----@param radius integer
 function AutoUIArrowInWorld(p1, p2, line_width, radius)
 	local s_p1 = { UiWorldToPixel(p1) }
 	local s_p2 = { UiWorldToPixel(p2) }
@@ -4179,477 +3024,6 @@
 	end
 end
 
----OLD
----UI
----FUNCTIONS
-
--- AutoPad = { none = 0, atom = 4, micro = 6, thin = 12, thick = 24, heavy = 48, beefy = 128 }
-
--- AutoPrimaryColor = { 0.95, 0.95, 0.95, 1 }
--- AutoSpecialColor = { 1, 1, 0.55, 1 }
--- AutoSecondaryColor = { 0, 0, 0, 0.55 }
--- AutoFont = 'regular.ttf'
--- local SpreadStack = {}
-
--- ---Draws some text at a world position.
--- ---@param text string|number? Text Displayed, Default is 'nil'
--- ---@param position vector The WorldSpace Position
--- ---@param occlude boolean? Hides the tooltip behind walls, Default is false
--- ---@param fontsize number? Fontsize, Default is 24
--- ---@param alpha number? Alpha, Default is 0.75
--- function AutoTooltip(text, position, occlude, fontsize, alpha)
--- 	text = AutoDefault(text or "nil")
--- 	occlude = AutoDefault(occlude or false)
--- 	fontsize = AutoDefault(fontsize or 24)
--- 	alpha = AutoDefault(alpha or 0.75)
--- 	bold = AutoDefault(bold or false)
-
--- 	if occlude then if not AutoPointInView(position, nil, nil, occlude) then return end end
-
--- 	UiPush()
--- 	UiAlign('center middle')
--- 	local x, y, dist = UiWorldToPixel(position)
--- 	if dist > 0 then
--- 		UiTranslate(x, y)
--- 		UiWordWrap(UiMiddle())
-
--- 		UiFont(AutoFont, fontsize)
--- 		UiColor(0, 0, 0, 0)
--- 		local rw, rh = UiText(text)
-
--- 		UiColorFilter(1, 1, 1, alpha)
--- 		UiColor(unpack(AutoSecondaryColor))
--- 		UiRect(rw, rh)
-
--- 		UiColor(unpack(AutoPrimaryColor))
--- 		UiText(text)
--- 		UiPop()
--- 	end
--- end
-
--- ---Takes an alignment and returns a Vector representation.
--- ---@param alignment string
--- ---@return table
--- function AutoAlignmentToPos(alignment)
--- 	str, y = 0, 0
--- 	if string.find(alignment, 'left') then str = -1 end
--- 	if string.find(alignment, 'center') then str = 0 end
--- 	if string.find(alignment, 'right') then str = 1 end
--- 	if string.find(alignment, 'bottom') then y = -1 end
--- 	if string.find(alignment, 'middle') then y = 0 end
--- 	if string.find(alignment, 'top') then y = 1 end
--- 	return { x = str, y = y }
--- end
-
--- ---The next Auto Ui functions will be spread Down until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadDown(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'down', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Up until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadUp(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'up', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Right until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadRight(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'right', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Left until AutoSpreadEnd() is called
--- ---@param padding number? The amount of padding that will be used, Default is AutoPad.thin
--- function AutoSpreadLeft(padding)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'left', padding = AutoDefault(padding, AutoPad.thin) })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Verticlely across the Height of the Bounds until AutoSpreadEnd() is called
--- ---@param count number? The amount of Auto Ui functions until AutoSpreadEnd()
--- function AutoSpreadVerticle(count)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'verticle', length = UiHeight(), count = count })
--- 	UiPush()
--- end
-
--- ---The next Auto Ui functions will be spread Horizontally across the Width of the Bounds until AutoSpreadEnd() is called
--- ---@param count number? The amount of Auto Ui functions until AutoSpreadEnd()
--- function AutoSpreadHorizontal(count)
--- 	table.insert(SpreadStack, { type = 'spread', direction = 'horizontal', length = UiWidth(), count = count })
--- 	UiPush()
--- end
-
--- function AutoGetSpread()
--- 	local _l = 0
--- 	local count = AutoTableCount(SpreadStack)
--- 	if count <= 0 then return nil end
--- 	for i = count, 1, -1 do
--- 		if SpreadStack[i].type == 'spread' then
--- 			_l = _l + 1
--- 			if _l >= 1 then
--- 				return SpreadStack[i], _l
--- 			end
--- 		end
--- 	end
--- 	return nil
--- end
-
--- function AutoSetSpread(Spread)
--- 	local count = AutoTableCount(SpreadStack)
--- 	for i = count, 1, -1 do
--- 		if SpreadStack[i].type == 'spread' then
--- 			str = SpreadStack[i]
--- 		end
--- 	end
-
--- 	str = Spread
--- end
-
--- ---Stop the last known Spread
--- ---@return table a table with information about the transformations used
--- function AutoSpreadEnd()
--- 	local unitdata = { comb = { w = 0, h = 0 }, max = { w = 0, h = 0 } }
--- 	-- local _, LastSpread = AutoGetSpread(1)
-
--- 	while true do
--- 		local count = #SpreadStack
-
--- 		if SpreadStack[count].type ~= 'spread' then
--- 			if SpreadStack[count].data.rect then
--- 				local rect = SpreadStack[count].data.rect
--- 				unitdata.comb.w, unitdata.comb.h = unitdata.comb.w + rect.w, unitdata.comb.h + rect.h
--- 				unitdata.max.w, unitdata.max.h = math.max(unitdata.max.w, rect.w), math.max(unitdata.max.h, rect.h)
--- 			end
-
--- 			table.remove(SpreadStack, count)
--- 		else
--- 			UiPop()
--- 			table.remove(SpreadStack, count)
-
--- 			return unitdata
--- 		end
--- 		if count <= 0 then
--- 			return unitdata
--- 		end
--- 	end
--- end
-
--- function AutoHandleSpread(gs, data, type, spreadpad)
--- 	spreadpad = AutoDefault(spreadpad, false)
-
--- 	if not AutoGetSpread() then return end
-
--- 	if gs ~= nil then
--- 		if not spreadpad then pad = 0 else pad = gs.padding end
--- 		if gs.direction == 'down' then
--- 			UiTranslate(0, data.rect.h + pad)
--- 		elseif gs.direction == 'up' then
--- 			UiTranslate(0, -(data.rect.h + pad))
--- 		elseif gs.direction == 'right' then
--- 			UiTranslate(data.rect.w + pad, 0)
--- 		elseif gs.direction == 'left' then
--- 			UiTranslate(-(data.rect.w + pad), 0)
--- 		elseif gs.direction == 'verticle' then
--- 			UiTranslate(0, gs.length / gs.count * 1.5 + gs.length / gs.count)
--- 		elseif gs.direction == 'horizontal' then
--- 			UiTranslate(gs.length / gs.count, 0)
--- 		end
--- 	end
-
--- 	if type ~= nil then
--- 		table.insert(SpreadStack, { type = type, data = data })
--- 	end
--- end
-
--- ---Given the current string, will return a modified string based on the input of the user. It's basically just a text box. Has a few options.
--- ---@param current any
--- ---@param maxlength any
--- ---@param allowlowercase any
--- ---@param allowspecial any
--- ---@param forcekey any
--- ---@return any
--- ---@return any
--- ---@return boolean
--- function AutoTextInput(current, maxlength, allowlowercase, allowspecial, forcekey)
--- 	current = AutoDefault(current, '')
--- 	maxlength = AutoDefault(maxlength, 1 / 0)
--- 	allowlowercase = AutoDefault(allowlowercase, true)
--- 	allowspecial = AutoDefault(allowspecial, true)
--- 	forcekey = AutoDefault(forcekey, nil)
-
--- 	local modified = current
-
--- 	local special = {
--- 		['1'] = '!',
--- 		['2'] = '@',
--- 		['3'] = '#',
--- 		['4'] = '$',
--- 		['5'] = '%',
--- 		['6'] = '^',
--- 		['7'] = '&',
--- 		['8'] = '*',
--- 		['9'] = '(',
--- 		['0'] = ')',
--- 	}
--- 	local lpk = forcekey or InputLastPressedKey()
-
--- 	if lpk == 'backspace' then
--- 		modified = modified:sub(1, #modified - 1)
--- 	elseif lpk == 'delete' then
--- 		modified = ''
--- 	elseif #modified < maxlength then
--- 		if lpk == 'space' then
--- 			modified = modified .. ' '
--- 		elseif #lpk == 1 then
--- 			if not InputDown('shift') then
--- 				if allowlowercase then
--- 					lpk = lpk:lower()
--- 				end
--- 			else
--- 				if allowspecial and special[lpk] then
--- 					lpk = special[lpk]
--- 				end
--- 			end
-
--- 			modified = modified .. lpk
--- 		end
--- 	end
-
--- 	return modified, lpk ~= '' and lpk or nil, modified ~= current
--- end
-
--- -- local keys = {
--- -- 	"lmb", "mmb", "rmb", -- mouse
--- -- 	"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", -- numerical
--- -- 	"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
--- -- 	"y", "z", -- alphabatical
--- -- 	"f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", -- function key
--- -- 	"uparrow", "downarrow", "leftarrow", "rightarrow", -- arrow key
--- -- 	"backspace", "alt", "delete", "home", "end", "pgup", "pgdown", "insert", "return", "space", "shift", "ctrl", "tab",
--- -- 	"esc", --random key
--- -- 	",", ".", "-", "+", -- undocumented key (yes, '=' key is '+' key)
--- -- }
-
--- -------------------------------------------------------------------------------------------------------------------------------------------------------
--- ----------------User Interface Creation Functions------------------------------------------------------------------------------------------------------
--- -------------------------------------------------------------------------------------------------------------------------------------------------------
-
--- ---Create a Container with new bounds
--- ---@param width number
--- ---@param height number
--- ---@param padding number? The Amount of padding against sides of the container, Default is AutoPad.micro
--- ---@param clip boolean? Whether  to clip stuff outside of the container, Default is false
--- ---@param draw boolean? Draws the container's background, otherwise it will be invisible, Default is true
--- ---@return table containerdata
--- function AutoContainer(width, height, padding, clip, draw)
--- 	width = AutoDefault(width, 300)
--- 	height = AutoDefault(height, 400)
--- 	padding = math.max(AutoDefault(padding, AutoPad.micro), 0)
--- 	clip = AutoDefault(clip, false)
--- 	draw = AutoDefault(draw, true)
-
--- 	local paddingwidth = math.max(width - padding * 2, padding * 2)
--- 	local paddingheight = math.max(height - padding * 2, padding * 2)
-
--- 	UiWindow(width, height, clip)
-
--- 	UiAlign('left top')
--- 	if draw then
--- 		UiPush()
--- 		UiColor(unpack(AutoSecondaryColor))
--- 		UiImageBox("ui/common/box-solid-10.png", UiWidth(), UiHeight(), 10, 10)
--- 		UiPop()
--- 	end
-
--- 	hover = UiIsMouseInRect(UiWidth(), UiHeight())
-
--- 	UiTranslate(padding, padding)
--- 	UiWindow(paddingwidth, paddingheight, false)
-
--- 	local offset = { x = 0, y = 0 }
-
--- 	UiTranslate(offset.x, offset.y)
-
--- 	return { rect = { w = paddingwidth, h = paddingheight }, hover = hover }
--- end
-
--- ---Creates a Button
--- ---@param name string
--- ---@param fontsize number
--- ---@param paddingwidth number Amount of padding used Horizontally
--- ---@param paddingheight number Amount of padding used Vertically
--- ---@param draw boolean Draws the Button
--- ---@param spreadpad boolean Adds padding when used with AutoSpread...()
--- ---@return boolean Pressed
--- ---@return table ButtonData
--- function AutoButton(name, fontsize, color, paddingwidth, paddingheight, draw, spreadpad)
--- 	fontsize = AutoDefault(fontsize, 28)
--- 	color = AutoDefault(color, AutoPrimaryColor)
--- 	paddingwidth = AutoDefault(paddingwidth, AutoPad.thick)
--- 	paddingheight = AutoDefault(paddingheight, AutoPad.thin)
--- 	draw = AutoDefault(draw, true)
--- 	spreadpad = AutoDefault(spreadpad, true)
-
--- 	UiPush()
--- 	UiWordWrap(UiWidth() - AutoPad.thick)
--- 	UiFont(AutoFont, fontsize)
--- 	UiButtonHoverColor(unpack(AutoSpecialColor))
--- 	UiButtonPressColor(0.75, 0.75, 0.75, 1)
--- 	UiButtonPressDist(0.25)
-
--- 	UiColor(0, 0, 0, 0)
--- 	local rw, rh = UiText(name)
--- 	local padrw, padrh = rw + paddingwidth * 2, rh + paddingheight * 2
-
--- 	if draw then
--- 		hover = UiIsMouseInRect(padrw, padrh)
--- 		UiColor(unpack(color))
-
--- 		UiButtonImageBox('ui/common/box-outline-6.png', 6, 6, unpack(color))
--- 		pressed = UiTextButton(name, padrw, padrh)
--- 	end
--- 	UiPop()
-
--- 	local data = { pressed = pressed, hover = hover, rect = { w = padrw, h = padrh } }
--- 	if draw then AutoHandleSpread(AutoGetSpread(), data, 'draw', spreadpad) end
-
--- 	return pressed, data
--- end
-
--- ---Draws some Text
--- ---@param name string
--- ---@param fontsize number
--- ---@param draw boolean Draws the Text
--- ---@param spread boolean Adds padding when used with AutoSpread...()
--- ---@return table TextData
--- function AutoText(name, fontsize, color, draw, spread)
--- 	fontsize = AutoDefault(fontsize, 28)
--- 	draw = AutoDefault(draw, true)
--- 	spread = AutoDefault(spread, true)
-
--- 	UiPush()
--- 	UiWordWrap(UiWidth() - AutoPad.thick)
--- 	UiFont(AutoFont, fontsize)
-
--- 	UiColor(0, 0, 0, 0)
--- 	local rw, rh = UiText(name)
-
--- 	if draw then
--- 		UiPush()
--- 		UiWindow(rw, rh)
--- 		AutoCenter()
-
--- 		UiColor(unpack(color or AutoPrimaryColor))
--- 		UiText(name)
--- 		UiPop()
--- 	end
--- 	UiPop()
-
--- 	local data = { rect = { w = rw, h = rh }, hover = UiIsMouseInRect(rw, rh) }
--- 	if spread then AutoHandleSpread(AutoGetSpread(), data, 'draw', true) end
-
--- 	return data
--- end
-
--- ---Creates a Slider
--- ---@param set number The Current Value
--- ---@param min number The Minimum
--- ---@param max number The Maximum
--- ---@param lockincrement number The increment
--- ---@param paddingwidth Amount of padding used Horizontally
--- ---@param paddingheight Amount of padding used Vertically
--- ---@param spreadpad boolean Adds padding when used with AutoSpread...()
--- ---@return number NewValue
--- ---@return table SliderData
--- function AutoSlider(set, min, max, lockincrement, paddingwidth, paddingheight, spreadpad)
--- 	min = AutoDefault(min, 0)
--- 	max = AutoDefault(max, 1)
--- 	set = AutoDefault(set, min)
--- 	lockincrement = AutoDefault(lockincrement, 0)
--- 	paddingwidth = AutoDefault(paddingwidth, AutoPad.thick)
--- 	paddingheight = AutoDefault(paddingheight, AutoPad.micro)
--- 	spreadpad = AutoDefault(spreadpad, true)
-
--- 	local width = UiWidth() - paddingwidth * 2
--- 	local dotwidth, dotheight = UiGetImageSize("MOD/slider.png")
-
--- 	local screen = AutoMap(set, min, max, 0, width)
-
--- 	UiPush()
--- 	UiTranslate(paddingwidth, paddingheight)
--- 	UiColor(unpack(AutoSpecialColor))
-
--- 	UiPush()
--- 	UiTranslate(0, dotheight / 2)
--- 	UiRect(width, 2)
--- 	UiPop()
-
--- 	UiTranslate(-dotwidth / 2, 0)
-
--- 	screen, released = UiSlider('MOD/slider.png', "x", screen, 0, width)
--- 	screen = AutoMap(screen, 0, width, min, max)
--- 	screen = AutoRound(screen, lockincrement)
--- 	screen = AutoClamp(screen, min, max)
--- 	set = screen
--- 	UiPop()
-
--- 	local data = { value = set, released = released, rect = { w = width, h = paddingheight * 2 + dotheight } }
--- 	AutoHandleSpread(AutoGetSpread(), data, 'draw', spreadpad)
-
--- 	return set, data
--- end
-
--- ---Draws an Image
--- ---@param path string
--- ---@param width number
--- ---@param height number
--- ---@param alpha number
--- ---@param draw boolean Draws the Image
--- ---@param spreadpad boolean Adds padding when used with AutoSpread...()
--- ---@return table ImageData
--- function AutoImage(path, width, height, border, spreadpad)
--- 	local w, h = UiGetImageSize(path)
--- 	width = AutoDefault(width, (height == nil and UiWidth() or (height * (w / h))))
--- 	height = AutoDefault(height, width * (h / w))
--- 	border = AutoDefault(border, 0)
--- 	draw = AutoDefault(draw, true)
--- 	spreadpad = AutoDefault(spreadpad, true)
-
--- 	UiPush()
--- 	UiImageBox(path, width, height, border, border)
--- 	UiPop()
-
--- 	local hover = UiIsMouseInRect(width, height)
-
--- 	local data = { hover = hover, rect = { w = width, h = height } }
--- 	if draw then AutoHandleSpread(AutoGetSpread(), data, 'draw', spreadpad) end
-
--- 	return data
--- end
-
--- ---Creates a handy little marker, doesnt effect anything, purely visual
--- ---@param size number, Default is 1
--- function AutoMarker(size)
--- 	size = AutoDefault(size, 1) / 2
--- 	UiPush()
--- 	UiAlign('center middle')
--- 	UiScale(size, size)
--- 	UiColor(unpack(AutoSpecialColor))
--- 	UiImage('ui/common/dot.png')
--- 	UiPop()
--- end
-
---#endregion
---#region Cursed
-
----Loads a string as `return <lua_string>`
----@param lua_string string
----@return boolean success
----@return unknown? return_value
 function AutoParse(lua_string)
 	local formatted = 'return ' .. lua_string
 	local success, func = pcall(loadstring, formatted)
@@ -4663,21 +3037,13 @@
 	return false
 end
 
----A very sinful way to pipe raw code into the registry, use in combination with `AutoCMD_Parse`
----@param path string
----@param luastr string
 function AutoCMD_Pipe(path, luastr)
 	local keys = ListKeys(path)
 	local newkey = AutoKey(path, #keys + 1)
 	
-	SetString(newkey, luastr)
-end
-
----A very sinful way to parse raw code from the registry, use in combination with `AutoCMD_Pipe`
----
----_God is dead and we killed her._
----@param path string
----@return table<{ cmd:string, result:any }>
+	SetString(newkey, luastr, true)
+end
+
 function AutoCMD_Parse(path)
 	local results = {}
 	for index = 1, #ListKeys(path) do
@@ -4702,4 +3068,3 @@
 	Spawn '<vehicle/>'
 end
 
---#endregion
```

---

# Migration Report: scripts\libraries\loader.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\libraries\loader.lua
+++ patched/scripts\libraries\loader.lua
@@ -1,7 +1,8 @@
-Loader = {}
+#version 2
+local default_env_meta = {
+	__index = _G
+}
 
----Leave blank to find itself.
----@param set_mod_id string?
 function Loader.Set(set_mod_id)
 	if set_mod_id then
 		Loader.mod_id = set_mod_id
@@ -61,14 +62,6 @@
 	end
 end
 
-Loader.Set()
-
---------------------------------------------------------------------------------------------------------------------------------
-
----Converts a path relative to the root mod folder to a RAW: path
----@param relative_path string
----@return string absolute_path Absolute Path
----@return td_path td_path RAW: Path
 function Loader.ResolvePath(relative_path)
 	local absolute_path = Loader.mod_data.path .. '/' .. relative_path
 	local td_path = 'RAW:' .. absolute_path
@@ -78,15 +71,6 @@
 	return absolute_path, td_path
 end
 
-local default_env_meta = {
-	__index = _G
-}
-
----Relative Path
----@param path string
----@return any
----@return table
----@nodiscard
 function Loader.File(path, default_search_path, inherit_env)
 	local absolute_path, td_path = Loader.ResolvePath(path)
 	if not HasFile(td_path) then absolute_path, td_path = Loader.ResolvePath((default_search_path or '') .. path) end
@@ -105,4 +89,5 @@
 		print(('[LOADER] Error : [relative path] %s : [absolute_path] %s : [Error on next line ]\n%s'):format(path, absolute_path, error_object))
 		return nil, nil
 	end
-end+end
+

```

---

# Migration Report: scripts\lightupMurals.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\lightupMurals.lua
+++ patched/scripts\lightupMurals.lua
@@ -1,8 +1,7 @@
-function init()
+#version 2
+function server.init()
     switchOnTrigger = FindTriggers("switchOnTrigger")
     switchOnLight = FindLights("switchOnLight")
-    lightOn = LoadSound("MOD/snd/lightOn.ogg")
-    lightOff = LoadSound("MOD/snd/lightOff.ogg")
     isInTrigger = {}
     pitchScaling = 1
     for i=1,8 do
@@ -11,11 +10,17 @@
     end
 end
 
-function tick()
+function client.init()
+    lightOn = LoadSound("MOD/snd/lightOn.ogg")
+    lightOff = LoadSound("MOD/snd/lightOff.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     for i=1,8 do
         local trigger = switchOnTrigger[i]
         local light = switchOnLight[i]
-        if IsPointInTrigger(trigger,GetPlayerTransform().pos) then
+        if IsPointInTrigger(trigger,GetPlayerTransform(playerId).pos) then
             SetLightEnabled(light,true)
             if not isInTrigger[i] then PlaySound(lightOn,GetLightTransform(light).pos,1,false,pitchScaling) isInTrigger[i] = true pitchScaling = pitchScaling - 0.025 end
         --[[else
@@ -25,4 +30,5 @@
             end]]
         end
     end
-end+end
+

```

---

# Migration Report: scripts\loadFarm.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\loadFarm.lua
+++ patched/scripts\loadFarm.lua
@@ -1,28 +1,27 @@
-levelPath = GetStringParam("level", "MOD/bunker.xml")
-layers = GetStringParam("layers", "waves")
-isSpace = GetBoolParam("isSpace", false)
-
-function init()
+#version 2
+function server.init()
     trigger = FindTrigger("loadfarm")
-    SetString("game.player.tool","")
+    SetString("game.player.tool","", true)
     if not isSpace then
-        SetInt("level.currentLevelInt",1)
+        SetInt("level.currentLevelInt",1, true)
     else
-        SetInt("level.currentLevelInt",4)
+        SetInt("level.currentLevelInt",4, true)
     end
 end
 
-function tick()
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if not isSpace then
-        SetBool("level.carChase", true)
-        if IsPointInTrigger(trigger, GetPlayerTransform().pos) then
-            SetBool("savegame.mod.stats.adventureBegun",true)
-            SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"))
-            SetInt("savegame.mod.stats.levelOrder",1)
+        SetBool("level.carChase", true, true)
+        if IsPointInTrigger(trigger, GetPlayerTransform(playerId).pos) then
+            SetBool("savegame.mod.stats.adventureBegun",true, true)
+            SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"), true)
+            SetInt("savegame.mod.stats.levelOrder",1, true)
             StartLevel("", levelPath, layers, true)
         end
     else
-        SetBool("level.isInSpace", true)
+        SetBool("level.isInSpace", true, true)
         if not soundPlayed then PlaySound(LoadSound("MOD/snd/TractorBeamZap.ogg",20)) soundPlayed = true end
     end
-end+end
+

```

---

# Migration Report: scripts\mainmenu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\mainmenu.lua
+++ patched/scripts\mainmenu.lua
@@ -1,19 +1,196 @@
-function init()
+#version 2
+function draw_mainmenu()
+    UiButtonHoverColor(0.5, 0.5, 0.5, 1)
+    UiTextShadow(0, 0, 0, 1, 2.4, 1)
+
+    if HasKey("savegame.mod.stats.adventureBegun") then
+        UiPush()
+            UiTextOutline(0,0,0,1,0.1)
+            UiTranslate(UiWidth()*0.95, UiHeight()*0.2)
+            UiAlign("right middle")
+            UiColor(0.4,0.8,0.8)
+            UiFont("MOD/assets/aaaiight-fat.ttf", 50)
+            UiText("RUN IN PROGRESS:")
+            UiFont("MOD/assets/Boomerank.ttf", 32)
+            UiTextOutline(0,0,0,1,0)
+            UiTranslate(0,30)
+            UiText("Score: "..GetInt("savegame.mod.stats.score.inRun"))
+            UiTranslate(0,30)
+            UiText("Time: "..string.format("%0.2f",GetFloat("savegame.mod.stats.time.inRun")).."s")
+            UiTranslate(0,35)
+            UiFont("MOD/assets/aaaiight-fat.ttf", 35)
+            UiColor(0.8,0.4,0.4)
+            UiTextOutline(0,0,0,1,0.3)
+            if UiTextButton("RETURN TO RUN: "..levels[GetInt("savegame.mod.stats.levelOrder")+1].name) then
+                StartLevel("", "MOD/"..levels[GetInt("savegame.mod.stats.levelOrder")+1].xml, levels[GetInt("savegame.mod.stats.levelOrder")+1].layers)
+            end
+        UiPop()
+    end
+
+    if HasKey("savegame.mod.stats.time.Best") then
+        UiPush()
+            UiTextOutline(0,0,0,1,0.1)
+            UiTranslate(UiWidth()*0.5, UiHeight()*0.05)
+            UiAlign("center middle")
+            UiColor(0.85,0.74,0.23)
+            UiFont("MOD/assets/Gemstone.ttf", 50)
+            UiText("BEST SCORE: "..GetInt("savegame.mod.stats.score.Best"))
+            UiTranslate(0,40)
+            UiText("BEST TIME: "..string.format("%0.2f",GetFloat("savegame.mod.stats.time.Best")).." SECONDS")
+        UiPop()
+    end
+
+    UiTranslate(UiWidth()*0.2, UiHeight()*0.2)
+    UiAlign("left middle")
+    UiImageBox("MOD/assets/gnome.png",114*1.5, 150*1.5)
+    UiTranslate(-250,0)
+    UiFont("MOD/assets/aaaiight-fat.ttf", 90)
+    UiText("GNOME", true)
+    UiText("ZONE")
+    UiPush()
+        UiTranslate(0,75)
+        UiFont("MOD/assets/Boomerank.ttf", 31)
+        UiWordWrap(200)
+        UiText("enabling music within the teardown settings is recommended.")
+    UiPop()
+
+    UiFont("MOD/assets/aaaiight.ttf", 60)
+    UiTranslate(0, UiHeight() * 0.2)
+    if UiTextButton("PLAY", 200, 50) then
+        play()
+        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+    end
+
+    UiTranslate(0, UiHeight() * 0.1)
+    if UiTextButton("LEVEL SELECT", 200, 50) then
+        levelselect = not levelselect
+        modifiers = false
+        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+    end
+    UiPush()
+        if levelselect then
+            UiTranslate(300, 0)
+            UiTextShadow(0, 0, 0, 1, 3.4, 1)
+            UiTextOutline(0, 0, 0, 0.5, 0.3)
+        
+            UiFont("MOD/assets/aaaiight.ttf", 30)
+            if UiTextButton("All Roads Lead Gnome", 200, 50) then
+                StartLevel("", "MOD/cornchase.xml")
+                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+            end
+
+            UiTranslate(0, 50)
+            if UiTextButton("Bunker", 200, 50) then
+                StartLevel("", "MOD/bunker.xml")
+                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+            end
+
+            UiTranslate(0, 50)
+            if UiTextButton("Gnome Way Out", 200, 50) then
+                StartLevel("", "MOD/main.xml", "nomainmenu")
+                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+            end
+ 
+            UiTranslate(0, 50)
+            if UiTextButton("Far From Gnome", 200, 50) then
+                StartLevel("", "MOD/arena.xml")
+                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+            end
+
+            UiTranslate(0, 50)
+            if UiTextButton("Post-Credits Bunker", 200, 50) then
+                StartLevel("", "MOD/bunker.xml","postcredits")
+                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+            end
+        
+            UiTranslate(0, 50)
+            UiColor(0.8, 0.8, 0.4)
+            if UiTextButton("BACK", 200, 50) then
+                levelselect = false
+                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+            end
+        end
+    UiPop()
+
+    UiTranslate(0, UiHeight() * 0.1)
+    if UiTextButton("MODIFIERS", 200, 50) then
+        modifiers = not modifiers
+        levelselect = false
+        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+    end
+    UiPush()
+        if modifiers then
+            UiTranslate(300, 0)
+            UiTextShadow(0, 0, 0, 1, 3.4, 1)
+            UiTextOutline(0, 0, 0, 0.5, 0.3)
+        
+            UiFont("MOD/assets/aaaiight.ttf", 30)
+
+            for i=1,#modifierTable do
+                local registryString = "savegame.mod.modifiers."..modifierTable[i].name
+                UiColor(0,0,0,0)
+                local w, h = UiText(modifierTable[i].name)
+                if UiIsMouseInRect(w+5,h+5) then
+                    UiPush()
+                        UiTranslate(w+20)
+                        UiFont("MOD/assets/Boomerank.ttf", 28)
+                        UiColor(0.9,0.9,0.9)
+                        UiText(modifierTable[i].desc)
+                    UiPop()
+                end
+                if GetBool(registryString) then UiColor(0.4,0.8,0.4) else UiColor(0.8,0.4,0.4) end
+                if UiTextButton(modifierTable[i].name) then
+                    if GetBool(registryString) then SetBool(registryString,false, true) else SetBool(registryString,true) end
+                    PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+                end
+                UiTranslate(0, 50)
+            end
+        
+            UiTranslate(0, 50)
+            UiColor(0.8, 0.8, 0.4)
+            if UiTextButton("BACK", 200, 50) then
+                modifiers = false
+                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+            end
+        end
+    UiPop()
+
+    UiTranslate(0, UiHeight() * 0.1)
+    if UiTextButton("OPTIONS", 200, 50) then
+        SetBool("level.settingsOpened",true, true)
+        modifiers = false
+        levelselect = false
+        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+    end
+
+    UiTranslate(0, UiHeight() * 0.1)
+    if UiTextButton("QUIT", 200, 50) then
+        quit()
+        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
+    end
+end
+
+function play()
+    StartLevel("", "MOD/cornchase.xml", "")
+end
+
+function quit()
+    Menu()
+end
+
+function server.init()
     camTrans = GetLocationTransform(FindLocation("menucam"))
     levelselect = false
-    GnomeDeath = LoadSound("MOD/snd/GnomeDeath0.ogg")
     sway = 0
     maxSway = 40
     dtMultiplier = 3
     SetEnvironmentProperty("ambience", "outdoor/field.ogg")
-
     levels ={
         {name="All Roads Lead Gnome",xml="cornchase.xml",layers=""},
         {name="Bunker",xml="bunker.xml",layers=""},
         {name="Gnome Way Out",xml="main.xml",layers="nomainmenu"},
         {name="Far From Gnome",xml="arena.xml",layers=""},
     }
-
     modifierTable ={
         {name="Dashless",desc="You cannot dash.",multiplier=1.3},
         {name="Glass",desc="Take damage, start over.",multiplier=1.5},
@@ -23,31 +200,36 @@
         {name="Kickback",desc="Gun launches you back when shot.",multiplier=0.8},
         {name="Blackout",desc="Environment is completely dark on all levels. Only artificial lights illuminate.",multiplier=1.1},
     }
-    if not GetBool("savegame.mod.gameWiped") then ClearKey("savegame.mod") SetBool("savegame.mod.gameWiped",true) end
+    if not GetBool("savegame.mod.gameWiped") then ClearKey("savegame.mod") SetBool("savegame.mod.gameWiped",true, true) end
     for i=1,#modifierTable do
         local registryString = "savegame.mod.modifiers."..modifierTable[i].name
         if not HasKey(registryString) then
-            SetBool(registryString,false)
-        end
-    end
-end
-
-
-function tick(dt)
-    if not swayRecover then
-        sway = sway + dt*dtMultiplier
-        if sway > maxSway then
-            swayRecover = true
-        end
-    else
-        sway = sway - dt*dtMultiplier
-        if sway < -maxSway then
-            swayRecover = false
-        end
-    end
-end
-
-function draw()
+            SetBool(registryString,false, true)
+        end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not swayRecover then
+            sway = sway + dt*dtMultiplier
+            if sway > maxSway then
+                swayRecover = true
+            end
+        else
+            sway = sway - dt*dtMultiplier
+            if sway < -maxSway then
+                swayRecover = false
+            end
+        end
+    end
+end
+
+function client.init()
+    GnomeDeath = LoadSound("MOD/snd/GnomeDeath0.ogg")
+end
+
+function client.draw()
     SetCameraTransform(Transform(camTrans.pos,QuatRotateQuat(camTrans.rot,QuatEuler(0,sway,0))), 70)
     UiMakeInteractive()
 
@@ -76,188 +258,8 @@
         UiColor(0.4,0.8,0.4)
         UiFont("MOD/assets/Gemstone.ttf", 50)
         UiButtonHoverColor(0.4,0.4,0.4,1)
-        if UiTextButton("OK") then SetBool("savegame.mod.disclaimerClosed",true) PlaySound(GnomeDeath,GetCameraTransform().pos,0.6) end
+        if UiTextButton("OK") then SetBool("savegame.mod.disclaimerClosed",true, true) PlaySound(GnomeDeath,GetCameraTransform().pos,0.6) end
         SetMusicLowPass(1)
     end
 end
 
-function draw_mainmenu()
-    UiButtonHoverColor(0.5, 0.5, 0.5, 1)
-    UiTextShadow(0, 0, 0, 1, 2.4, 1)
-
-    if HasKey("savegame.mod.stats.adventureBegun") then
-        UiPush()
-            UiTextOutline(0,0,0,1,0.1)
-            UiTranslate(UiWidth()*0.95, UiHeight()*0.2)
-            UiAlign("right middle")
-            UiColor(0.4,0.8,0.8)
-            UiFont("MOD/assets/aaaiight-fat.ttf", 50)
-            UiText("RUN IN PROGRESS:")
-            UiFont("MOD/assets/Boomerank.ttf", 32)
-            UiTextOutline(0,0,0,1,0)
-            UiTranslate(0,30)
-            UiText("Score: "..GetInt("savegame.mod.stats.score.inRun"))
-            UiTranslate(0,30)
-            UiText("Time: "..string.format("%0.2f",GetFloat("savegame.mod.stats.time.inRun")).."s")
-            UiTranslate(0,35)
-            UiFont("MOD/assets/aaaiight-fat.ttf", 35)
-            UiColor(0.8,0.4,0.4)
-            UiTextOutline(0,0,0,1,0.3)
-            if UiTextButton("RETURN TO RUN: "..levels[GetInt("savegame.mod.stats.levelOrder")+1].name) then
-                StartLevel("", "MOD/"..levels[GetInt("savegame.mod.stats.levelOrder")+1].xml, levels[GetInt("savegame.mod.stats.levelOrder")+1].layers)
-            end
-        UiPop()
-    end
-
-    if HasKey("savegame.mod.stats.time.Best") then
-        UiPush()
-            UiTextOutline(0,0,0,1,0.1)
-            UiTranslate(UiWidth()*0.5, UiHeight()*0.05)
-            UiAlign("center middle")
-            UiColor(0.85,0.74,0.23)
-            UiFont("MOD/assets/Gemstone.ttf", 50)
-            UiText("BEST SCORE: "..GetInt("savegame.mod.stats.score.Best"))
-            UiTranslate(0,40)
-            UiText("BEST TIME: "..string.format("%0.2f",GetFloat("savegame.mod.stats.time.Best")).." SECONDS")
-        UiPop()
-    end
-
-    UiTranslate(UiWidth()*0.2, UiHeight()*0.2)
-    UiAlign("left middle")
-    UiImageBox("MOD/assets/gnome.png",114*1.5, 150*1.5)
-    UiTranslate(-250,0)
-    UiFont("MOD/assets/aaaiight-fat.ttf", 90)
-    UiText("GNOME", true)
-    UiText("ZONE")
-    UiPush()
-        UiTranslate(0,75)
-        UiFont("MOD/assets/Boomerank.ttf", 31)
-        UiWordWrap(200)
-        UiText("enabling music within the teardown settings is recommended.")
-    UiPop()
-
-
-    UiFont("MOD/assets/aaaiight.ttf", 60)
-    UiTranslate(0, UiHeight() * 0.2)
-    if UiTextButton("PLAY", 200, 50) then
-        play()
-        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-    end
-
-    UiTranslate(0, UiHeight() * 0.1)
-    if UiTextButton("LEVEL SELECT", 200, 50) then
-        levelselect = not levelselect
-        modifiers = false
-        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-    end
-    UiPush()
-        if levelselect then
-            UiTranslate(300, 0)
-            UiTextShadow(0, 0, 0, 1, 3.4, 1)
-            UiTextOutline(0, 0, 0, 0.5, 0.3)
-        
-            UiFont("MOD/assets/aaaiight.ttf", 30)
-            if UiTextButton("All Roads Lead Gnome", 200, 50) then
-                StartLevel("", "MOD/cornchase.xml")
-                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-            end
-
-            UiTranslate(0, 50)
-            if UiTextButton("Bunker", 200, 50) then
-                StartLevel("", "MOD/bunker.xml")
-                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-            end
-
-            UiTranslate(0, 50)
-            if UiTextButton("Gnome Way Out", 200, 50) then
-                StartLevel("", "MOD/main.xml", "nomainmenu")
-                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-            end
- 
-            UiTranslate(0, 50)
-            if UiTextButton("Far From Gnome", 200, 50) then
-                StartLevel("", "MOD/arena.xml")
-                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-            end
-
-            UiTranslate(0, 50)
-            if UiTextButton("Post-Credits Bunker", 200, 50) then
-                StartLevel("", "MOD/bunker.xml","postcredits")
-                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-            end
-        
-            UiTranslate(0, 50)
-            UiColor(0.8, 0.8, 0.4)
-            if UiTextButton("BACK", 200, 50) then
-                levelselect = false
-                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-            end
-        end
-    UiPop()
-
-    UiTranslate(0, UiHeight() * 0.1)
-    if UiTextButton("MODIFIERS", 200, 50) then
-        modifiers = not modifiers
-        levelselect = false
-        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-    end
-    UiPush()
-        if modifiers then
-            UiTranslate(300, 0)
-            UiTextShadow(0, 0, 0, 1, 3.4, 1)
-            UiTextOutline(0, 0, 0, 0.5, 0.3)
-        
-            UiFont("MOD/assets/aaaiight.ttf", 30)
-
-            for i=1,#modifierTable do
-                local registryString = "savegame.mod.modifiers."..modifierTable[i].name
-                UiColor(0,0,0,0)
-                local w, h = UiText(modifierTable[i].name)
-                if UiIsMouseInRect(w+5,h+5) then
-                    UiPush()
-                        UiTranslate(w+20)
-                        UiFont("MOD/assets/Boomerank.ttf", 28)
-                        UiColor(0.9,0.9,0.9)
-                        UiText(modifierTable[i].desc)
-                    UiPop()
-                end
-                if GetBool(registryString) then UiColor(0.4,0.8,0.4) else UiColor(0.8,0.4,0.4) end
-                if UiTextButton(modifierTable[i].name) then
-                    if GetBool(registryString) then SetBool(registryString,false) else SetBool(registryString,true) end
-                    PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-                end
-                UiTranslate(0, 50)
-            end
-        
-            UiTranslate(0, 50)
-            UiColor(0.8, 0.8, 0.4)
-            if UiTextButton("BACK", 200, 50) then
-                modifiers = false
-                PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-            end
-        end
-    UiPop()
-
-    UiTranslate(0, UiHeight() * 0.1)
-    if UiTextButton("OPTIONS", 200, 50) then
-        SetBool("level.settingsOpened",true)
-        modifiers = false
-        levelselect = false
-        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-    end
-
-
-    UiTranslate(0, UiHeight() * 0.1)
-    if UiTextButton("QUIT", 200, 50) then
-        quit()
-        PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
-    end
-end
-
-function play()
-    StartLevel("", "MOD/cornchase.xml", "")
-end
-
-function quit()
-    Menu()
-end
```

---

# Migration Report: scripts\noise.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\noise.lua
+++ patched/scripts\noise.lua
@@ -1,4 +1,4 @@
--- Permutation table
+#version 2
 local permutation = {151,160,137,91,90,15,
     131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
     190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
@@ -12,41 +12,14 @@
     251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,
     49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
     138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180}
-for i=1,255 do permutation[i] = permutation[i] - 1 end
-
--- Gradient vectors
 local grad = {{1, 1}, {-1, 1}, {1, -1}, {-1, -1},
               {1, 0}, {-1, 0}, {0, 1}, {0, -1}}
 
--- Function to compute dot product of gradient and distance vectors
 local function dot(grad, x, y)
     return grad[1] * x + grad[2] * y
 end
 
--- Helper function to calculate the hash
 local function hash(x, y)
     return permutation[(permutation[x % 256 + 1] + y) % 256 + 1]
 end
 
--- Simplex noise function
-return function (x, y)
-    local floorX = math.floor(x)
-    local floorY = math.floor(y)
-    local X = floorX % 256
-    local Y = floorY % 256
-    x = x - floorX
-    y = y - floorY
-    local u = x * x * (3 - 2 * x)
-    local v = y * y * (3 - 2 * y)
-    local g00 = hash(X, Y)
-    local g01 = hash(X, Y + 1)
-    local g10 = hash(X + 1, Y)
-    local g11 = hash(X + 1, Y + 1)
-    local n00 = dot(grad[g00 % 8 + 1], x, y)
-    local n01 = dot(grad[g01 % 8 + 1], x, y - 1)
-    local n10 = dot(grad[g10 % 8 + 1], x - 1, y)
-    local n11 = dot(grad[g11 % 8 + 1], x - 1, y - 1)
-    local n0 = n00 + u * (n10 - n00)
-    local n1 = n01 + u * (n11 - n01)
-    return (n0 + v * (n1 - n0)) * 0.5
-end

```

---

# Migration Report: scripts\options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\options.lua
+++ patched/scripts\options.lua
@@ -1,53 +1,4 @@
-function init()
-    enabled = false
-
-    options = {
-        {id="weaponSway", init_value=1, min=0, max=5, text="Weapon Sway Strength", scoreMult = 1},
-        {id="healMult", init_value=1, min=0.2, max=2, text="Healing Multiplier", scoreMult = 1},
-        {id="iFrameMult", init_value=1, min=0, max=2, text="I-Frame Multiplier", scoreMult = -1},
-        {id="timescale", init_value=1, min=0.25, max=2, text="Time Scale", scoreMult = 1},
-        {id="enemyJumpRandom", init_value=1, min=0, max=5, text="Enemy Jump Randomization", scoreMult = -1},
-        {id="hitboxSize", init_value=1, min=0.5, max=5, text="Enemy Hitbox Size", scoreMult = -1},
-        {id="enemySpeed", init_value=1, min=0.5, max=5, text="Enemy Speed Multiplier", scoreMult = 1},
-    }
-
-    optionBools = {
-        {id="scoreboardToggled", text="Hide Scoreboard UI",default=false},
-        {id="speedrunToggled", text="Hide Speedrun Timer UI",default=false},
-        {id="enemyOutlines", text="Enemy Outlines Enabled",default=false},
-        {id="cbHonkeyModel", text="Custom Playermodels Enabled",default=false},
-    }
-
-    for i=1,#optionBools do
-        if not HasKey("savegame.mod.options."..optionBools[i].id) then
-            SetBool("savegame.mod.options."..optionBools[i].id,optionBools[i].default)
-        end
-    end
-
-    for i, option in ipairs(options) do
-        local key = "savegame.mod.options."..option.id
-        if HasKey(key) then
-            option.value = GetFloat(key) --get saved value
-        else
-            option.value = option.init_value
-            SetFloat(key, option.init_value)  --set initial value into registry
-        end
-    end
-    GnomeDeath = LoadSound("MOD/snd/GnomeDeath0.ogg")
-end
-
-function draw()
-    --[[if InputPressed("k") then
-        enabled = not enabled
-        SetBool("level.settingsOpened",enabled)
-    end]]
-    if GetBool("level.settingsOpened") then
-        UiMakeInteractive()
-        drawDifficultyMenu()
-        saveOptions()
-    end
-end
-
+#version 2
 function drawDifficultyMenu()
     UiButtonHoverColor(0.5,0.5,0.5,1)
     UiPush()
@@ -94,7 +45,7 @@
 
                 if GetBool("savegame.mod.options."..optionBools[i].id) then UiColor(0,0.7,0) boxPath = "toggleX" else UiColor(0.7,0,0) boxPath = "toggleBox" end
                 if UiImageButton("MOD/assets/"..boxPath..".png") then
-                    SetBool("savegame.mod.options."..optionBools[i].id, not GetBool("savegame.mod.options."..optionBools[i].id))
+                    SetBool("savegame.mod.options."..optionBools[i].id, not GetBool("savegame.mod.options."..optionBools[i].id), true)
                     PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
                 end
                 UiTranslate(20, 0)
@@ -116,7 +67,7 @@
             end
         UiPop()
         UiTranslate(-650,0)
-        SetBool("game.disablepause",true)
+        SetBool("game.disablepause",true, true)
         if GetBool("level.deadOptionsScreen") then
             UiPush()
                 UiColor(0.05,0.7,0.7)
@@ -137,8 +88,8 @@
             end
         else
             if UiTextButton("CLOSE MENU") or InputPressed("pause") then
-                SetBool("level.settingsOpened",false)
-                SetBool("game.disablepause",false)
+                SetBool("level.settingsOpened",false, true)
+                SetBool("game.disablepause",false, true)
                 PlaySound(GnomeDeath,GetCameraTransform().pos,0.6)
             end
         end
@@ -173,9 +124,9 @@
 function saveOptions()
     for i, option in ipairs(options) do
         local key = "savegame.mod.options."..option.id
-        SetFloat(key, string.format("%.1f", option.value))
+        SetFloat(key, string.format("%.1f", option.value), true)
         if GetFloat(key) ~= option.init_value then
-            SetBool("savegame.mod.options.tweaked."..option.id,true)
+            SetBool("savegame.mod.options.tweaked."..option.id,true, true)
         else
             if HasKey("savegame.mod.options.tweaked."..option.id) then ClearKey("savegame.mod.options.tweaked."..option.id) end
         end
@@ -187,7 +138,7 @@
         option.value = option.init_value
     end
     for i=1,#optionBools do
-        SetBool("savegame.mod.options."..optionBools[i].id,optionBools[i].default)
+        SetBool("savegame.mod.options."..optionBools[i].id,optionBools[i].default, true)
     end
 end
 
@@ -201,7 +152,53 @@
         end
     end
     final_score_multiplier = math.max((final_score_multiplier),0.25)
-    SetFloat("savegame.mod.finalScoreMultiplier",final_score_multiplier)
+    SetFloat("savegame.mod.finalScoreMultiplier",final_score_multiplier, true)
 
     return math.max(final_score_multiplier, 0)
-end+end
+
+function server.init()
+    enabled = false
+    options = {
+        {id="weaponSway", init_value=1, min=0, max=5, text="Weapon Sway Strength", scoreMult = 1},
+        {id="healMult", init_value=1, min=0.2, max=2, text="Healing Multiplier", scoreMult = 1},
+        {id="iFrameMult", init_value=1, min=0, max=2, text="I-Frame Multiplier", scoreMult = -1},
+        {id="timescale", init_value=1, min=0.25, max=2, text="Time Scale", scoreMult = 1},
+        {id="enemyJumpRandom", init_value=1, min=0, max=5, text="Enemy Jump Randomization", scoreMult = -1},
+        {id="hitboxSize", init_value=1, min=0.5, max=5, text="Enemy Hitbox Size", scoreMult = -1},
+        {id="enemySpeed", init_value=1, min=0.5, max=5, text="Enemy Speed Multiplier", scoreMult = 1},
+    }
+    optionBools = {
+        {id="scoreboardToggled", text="Hide Scoreboard UI",default=false},
+        {id="speedrunToggled", text="Hide Speedrun Timer UI",default=false},
+        {id="enemyOutlines", text="Enemy Outlines Enabled",default=false},
+        {id="cbHonkeyModel", text="Custom Playermodels Enabled",default=false},
+    }
+    for i=1,#optionBools do
+        if not HasKey("savegame.mod.options."..optionBools[i].id) then
+            SetBool("savegame.mod.options."..optionBools[i].id,optionBools[i].default, true)
+        end
+    end
+    for i, option in ipairs(options) do
+        local key = "savegame.mod.options."..option.id
+        if HasKey(key) then
+            option.value = GetFloat(key) --get saved value
+        else
+            option.value = option.init_value
+            SetFloat(key, option.init_value, true)  --set initial value into registry
+        end
+    end
+end
+
+function client.init()
+    GnomeDeath = LoadSound("MOD/snd/GnomeDeath0.ogg")
+end
+
+function client.draw()
+    if GetBool("level.settingsOpened") then
+        UiMakeInteractive()
+        drawDifficultyMenu()
+        saveOptions()
+    end
+end
+

```

---

# Migration Report: scripts\projectile.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\projectile.lua
+++ patched/scripts\projectile.lua
@@ -1,47 +1,5 @@
+#version 2
 local module = {}
-
-module.index = 0
----@type projectile[]
-module.projectiles = {}
-
---#region Configuration
-
-module.configuration = {}
-module.configuration.movement_distance = 0.1
-module.configuration.life_time = 10
-module.configuration.life_time_without_collision = 2
-module.configuration.minumum_velocity = 1e-3
-module.configuration.elipson_distance = 1e-3
-
-module.configuration.penetrations = 5
-
-module.configuration.dampening_amount = 0.7
-
-module.configuration.reflection_scatter = 0 -- Angle from 0 to 360
-module.configuration.penetration_scatter = 0 -- Angle from 0 to 360
-
-
-module.preset = {}
-module.preset.damage = {
-    none        = { damage = true,  reflect = false, dampening = 0.0, scatter = 0.1,    penetration = 1.0,  spark = false },
-
-    glass       = { damage = true,  reflect = false, dampening = 0.0, scatter = 0.05,   penetration = 1.0,  spark = false },
-    foliage     = { damage = true,  reflect = false, dampening = 0.0, scatter = 0.1,    penetration = 1.0,  spark = false },
-    plastic     = { damage = true,  reflect = false, dampening = 0.1, scatter = 0.25,   penetration = 1.0,  spark = false },
-    plaster     = { damage = true,  reflect = false, dampening = 0.1, scatter = 0.375,  penetration = 1.0,  spark = false },
-    dirt        = { damage = true,  reflect = false, dampening = 0.2, scatter = 0.5,    penetration = 1.0,  spark = false },
-    ice         = { damage = true,  reflect = false, dampening = 0.0, scatter = 0.5,    penetration = 1.0,  spark = false },
-    wood        = { damage = true,  reflect = false, dampening = 0.3, scatter = 0.625,  penetration = 0.8,  spark = false },
-    metal       = { damage = true,  reflect = true,  dampening = 0.4, scatter = 0.75,   penetration = 0.65, spark = true  },
-    masonry     = { damage = true,  reflect = false, dampening = 0.6, scatter = 1,      penetration = 0.7,  spark = false },
-
-    heavymetal  = { damage = true,  reflect = true,  dampening = 1.0, scatter = 0.5,    penetration = 0.5,  spark = true  },
-    rock        = { damage = false, reflect = true,  dampening = 1.0, scatter = 0.5,    penetration = 0.5,  spark = false },
-    hardmetal   = { damage = false, reflect = true,  dampening = 1.0, scatter = 0.5,    penetration = 0.5,  spark = true  },
-    hardmasonry = { damage = false, reflect = true,  dampening = 1.0, scatter = 0.5,    penetration = 0.5,  spark = false },
-    unphysical  = { damage = false, reflect = true,  dampening = 0.0, scatter = 0.5,    penetration = 1.0,  spark = false },
-}
-
 local sound_lookup = {
     glass       = { small = 'glass/break-s0',      medium = 'glass/break-m0',      large = 'glass/break-l0'      },
     foliage     = { small = 'foliage/break-s0',    medium = 'foliage/break-m0',    large = 'foliage/break-l0'    },
@@ -58,23 +16,9 @@
     hardmasonry = { small = 'masonry/break-s0',    medium = 'masonry/break-m0',    large = 'masonry/break-l0'    },
     -- unphysical  = { small = LoadSound('unphysical/break-s0'), medium = LoadSound('unphysical/break-m0'), large = LoadSound('unphysical/break-l0') },
 }
-
 local sound_handles = {}
-
---#endregion
-
-
---#region Meta
-
----@class projectile: { position:vector, velocity:vector, last_position:vector, time:number, random:number, reference:integer, [any]:any }
 local projectile_class = {}
-projectile_class.__index = projectile_class
-
---#endregion
-
---#region Module
-
----@return projectile
+
 function module.create_projectile(origin, velocity)
     module.index = module.index + 1
 
@@ -102,11 +46,6 @@
     end
 end
 
----@param material material|''
----@param weight 'small'|'medium'|'large'
----@param position vector
----@param volume number
----@param register boolean
 function module.MaterialBreakSound(material, weight, position, volume, register)
     if material and material == '' or material == 'none' or material == 'unphysical' then return end
     local path = sound_lookup[material][weight]
@@ -118,10 +57,6 @@
     
     PlaySound(handle, position, volume, register)
 end
-
---#endregion
-
---#region Projectile Class
 
 function projectile_class:update(dt)
     local Time = GetTime()
@@ -161,9 +96,9 @@
         local gnome, qgnome_ray = GNOMES.raycast(self.last_position, direction, collision_raycast.dist)
     
         if gnome and qgnome_ray and qgnome_ray.dists[1] <= distance then
-            --[[SetFloat("level.poopGnomes.rifleHitVec.1",collision_raycast.intersection[1])
-            SetFloat("level.poopGnomes.rifleHitVec.2",collision_raycast.intersection[2])
-            SetFloat("level.poopGnomes.rifleHitVec.3",collision_raycast.intersection[3])]]
+            --[[SetFloat("level.poopGnomes.rifleHitVec.1",collision_raycast.intersection[1], true)
+            SetFloat("level.poopGnomes.rifleHitVec.2",collision_raycast.intersection[2], true)
+            SetFloat("level.poopGnomes.rifleHitVec.3",collision_raycast.intersection[3], true)]]
             local gnomeShapes = gnome.memory.anim.shapes
             for i=1,#gnomeShapes do
                 gnomeShape = gnomeShapes[i]
@@ -270,8 +205,6 @@
     module.projectiles[self.reference] = nil
 end
 
----@param event_data any
----@param ... string Events
 function projectile_class:send(event_data, ...)
     local serialized_data = AutoToString(event_data, false, 0, nil, nil, true)
     local return_function = string.format('return %s', serialized_data)
@@ -282,24 +215,3 @@
     end
 end
 
---[[ Parser, implied that this is in a script loaded by Autumn's loader.lua system
-function init( ... )
-    RegisterListenerTo('autumn-ts projectile collision', 'autumn_ts_projectile_collision')
-end
-
-local global = getfenv(0)
-
-function global.autumn_ts_projectile_collision(return_function)
-    local s, f = pcall(loadstring, return_function)
-
-    if s and f then
-        local data = f()
-        AutoInspect(data, 'Projectile = ', 0.01, 2)
-        AutoDrawSphereTangent(data.collision.intersection, 0.1, 2, DebugLine, 1, 0, 1, 1)
-    end
-end
-]]
-
---#endregion
-
-return module
```

---

# Migration Report: scripts\screenimage.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\screenimage.lua
+++ patched/scripts\screenimage.lua
@@ -1,9 +1,10 @@
-function init()
+#version 2
+function server.init()
     gotImg = false
     imgPath = ""
 end
 
-function draw()
+function client.draw()
     if not gotImg then
         screen = UiGetScreen()
         shape = GetScreenShape(screen)
@@ -14,10 +15,11 @@
             gotImg = true
             --DebugPrint(imgPath)
         end
-    
+
     else
         w,h = UiGetImageSize(imgPath)
         UiScale(UiWidth()/w, UiHeight()/h)
         UiImage(imgPath)
     end
-end+end
+

```

---

# Migration Report: scripts\shape_anim.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\shape_anim.lua
+++ patched/scripts\shape_anim.lua
@@ -1,18 +1,4 @@
---[[
-    Shape Animation Framework, provides tools for moving shapes within a body in a armature like fashion
-]]
-
---[[
-    This framework is meant to be loaded in as a file, not using #include.
-    
-    As of now this framework requires the latest version of the Automatic Framework.
-    The Automatic Framework should be present within the environment, either via injecting or metatables
-
-    CREATED BY AUTUMNAGNIFICENT / AUTUMNATIC / AUTUMN
-]]
-
-shape_anim = {}
-
+#version 2
 local getTransformTable = {
 	body = GetBodyTransform,
 	location = GetLocationTransform,
@@ -21,20 +7,12 @@
 	trigger = GetTriggerTransform,
     vehicle = GetVehicleTransform,
 }
-
----@class shape_animation_shape_bone:      { handle:shape_handle, transform:transform, tags:table<string, string> }
----@class shape_animation_bone:            { transform:transform, shape_bones:shape_animation_shape_bone[], tags:table<string, string>, dirty:boolean }
----@class shape_animation:                 { xml:string, body:body_handle, bones:table<string, shape_animation_bone>, shapes:shape_handle[], transformations:table<string, transform>, entities:entity_handle[], origin:transform, scale:number, external:table }
 local animation_class = {}
-animation_class.__index = animation_class
 
 function animation_class:Reject()
     AutoQueryRejectShapes(self.shapes)
 end
 
----@param id string
----@param custom_transformation_table table<string, transform>?
----@return transform
 function animation_class:GetBoneLocalTransform(id, custom_transformation_table)
 	local order = AutoSplit(id, '.')
 	local transform = Transform()
@@ -58,9 +36,6 @@
 	return TransformToParentTransform(self.origin, transform)
 end
 
----@param id string
----@param custom_transformation_table table<string, transform>?
----@return transform
 function animation_class:GetBoneWorldTransform(id, raw, custom_transformation_table)
     if self.external.dirty_world_transform then self:clean_world_transform() end
     
@@ -70,14 +45,10 @@
     return TransformToParentTransform(body_world_transform, bone_local_transform)
 end
 
----@param id string
----@return shape_handle[]
 function animation_class:GetShapesOfBone(id)
     return AutoTableSub(self.bones[id].shape_bones, 'handle')
 end
 
----@param id string
----@param transformation transform
 function animation_class:SetTransformation(id, transformation)
     self.transformations[id] = TransformCopy(transformation)
 
@@ -94,14 +65,12 @@
     end
 end
 
----@param transformations table<string, transform>
 function animation_class:SetTransformationTable(transformations)
     for bone_id, transformation in pairs(transformations) do
         self:SetTransformation(bone_id, transformation)
     end
 end
 
----This uses Thomasims' method of predicting the transform of a body
 function animation_class:clean_world_transform()
     local body_world_transform = GetBodyTransform(self.body)
 
@@ -157,13 +126,6 @@
     end
 end
 
---------------------------------------------------------------------------------------------------------------------------------
-
----@param xml string
----@param parent_body body_handle The Parent Body
----@param local_transform_origin transform?
----@param scale number?
----@return shape_animation
 function shape_anim.Create(xml, parent_body, local_transform_origin, scale, no_collision)
     if not xml then error('xml not defined, xml = ' .. AutoToString(xml)) end
 
@@ -277,10 +239,6 @@
     return anim
 end
 
----@param shapes shape_handle[]
----@param transform transform
----@param density number
----@return shape_handle[] colliders
 function shape_anim.FakeScaledPhysics(shapes, body, transform, density)
     colliders = {}
     
@@ -314,4 +272,3 @@
     return colliders
 end
 
-return shape_anim
```

---

# Migration Report: scripts\timeManager.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\timeManager.lua
+++ patched/scripts\timeManager.lua
@@ -1,90 +1,4 @@
-#include "/libraries/Automatic.lua"
-
-justButton = GetBoolParam("menuButtonOnly",false)
-function init()
-    modifierTable ={
-        {name="Dashless",desc="You cannot dash.",multiplier=1.3},
-        {name="Glass",desc="Take damage, start over.",multiplier=1.5},
-        {name="Beam",desc="The Gnome Beam is present at all times during Gnome Way Out & Far From Gnome",multiplier=1.2},
-        {name="Boom",desc="All gnomes explode on death. Explosive gnomes have a larger explosive radius.",multiplier=1},
-        --{name="Moon",desc="Lower gravity.",multiplier=0.8},
-        {name="Kickback",desc="Gun launches you back when shot.",multiplier=0.8},
-        {name="Blackout",desc="Environment is completely dark on all levels. Only artificial lights illuminate.",multiplier=1.1},
-    }
-
-    waspaused = false
-	pauseMenuAlpha = 0
-end
-
-function tick()
-    --if not GetBool("savegame.mod.options.cbHonkeyModel") then SetString("game.player.character","local-poop-gnomes"..'_'..'cb-honkey') end
-    if not GetBool("savegame.mod.options.cbHonkeyModel") then SetString("game.player.character","steam-3209546457"..'_'..'cb-honkey') end
-    --if not GetBool("savegame.mod.options.cbHonkeyModel") then SetString("game.player.character",Loader.mod_id..'_'..'cb-honkey') end
-    
-    SetTimeScale(GetFloat("savegame.mod.options.timescale"))
-    --[[if not HasVersion('1.5.4') then
-        if PauseMenuButton("GNOptions", true) then SetBool("level.settingsOpened",true) end
-    else
-        if PauseMenuButton("Back To GnoMenu", "main_top") then StartLevel("", "MOD/main.xml") end
-    end]]
-
-    if not HasVersion('1.5.4') then
-        if PauseMenuButton("Back To GnoMenu", true) then StartLevel("", "MOD/main.xml") end
-    else
-        if PauseMenuButton("Back To GnoMenu", "main_top") then StartLevel("", "MOD/main.xml") end
-    end
-
-    if not justButton then
-        if not fraudChecked then
-            if GetInt("savegame.mod.stats.levelOrder")+1 == GetInt("level.currentLevelInt") and GetBool("savegame.mod.stats.adventureBegun") then
-                fraud = false
-            else
-                fraud = true
-            end
-            
-            if fraud then
-                ClearKey("savegame.mod.stats.score.inRun")
-                ClearKey("savegame.mod.stats.time.inRun")
-                ClearKey("savegame.mod.stats.adventureBegun")
-                ClearKey("savegame.mod.stats.levelOrder")
-                mapTime = 0
-            else
-                mapTime = GetFloat("savegame.mod.stats.time.inRun")
-                --SetFloat("savegame.mod.stats.time.inRun", 0)
-            end
-            fraudChecked = true
-        end
-        if not GetBool("level.titleCardLoad") then
-            SetFloat("level.time", mapTime+GetTime())
-        end
-
-        --modifiers
-        if GetBool("savegame.mod.modifiers.Blackout") then
-			local Environment = {
-				ambient = 0,
-				ambientexponent = 5,
-				constant = {0, 0, 0},
-				exposure = {0, 20},
-				fogcolor = {0, 0, 0},
-				fogparams = {-0, 0, 0, 0},
-				nightlight = true,
-				skyboxbrightness = 0,
-				sunbrightness = 0,
-				suncolortint = {0,0,0},
-				sundir = {0,0,0},
-				sunfogscale = 1,
-				sunglare = 0,
-				sunlength = 0,
-			}
-			AutoSetEnvironment(Environment)
-			local postPros = {
-				bloom = 0,
-			}
-			AutoSetPostProcessing(postPros)
-        end
-    end
-end
-
+#version 2
 function render()
 	paused = GetBool("game.paused")
 	if waspaused and not paused then
@@ -97,11 +11,95 @@
 	waspaused = paused
 
 	if pauseMenuAlpha == 0 then
-		SetBool("hud.disable", true)
+		SetBool("hud.disable", true, true)
 	end
 end
 
-function draw()
+function server.init()
+       modifierTable ={
+           {name="Dashless",desc="You cannot dash.",multiplier=1.3},
+           {name="Glass",desc="Take damage, start over.",multiplier=1.5},
+           {name="Beam",desc="The Gnome Beam is present at all times during Gnome Way Out & Far From Gnome",multiplier=1.2},
+           {name="Boom",desc="All gnomes explode on death. Explosive gnomes have a larger explosive radius.",multiplier=1},
+           --{name="Moon",desc="Lower gravity.",multiplier=0.8},
+           {name="Kickback",desc="Gun launches you back when shot.",multiplier=0.8},
+           {name="Blackout",desc="Environment is completely dark on all levels. Only artificial lights illuminate.",multiplier=1.1},
+       }
+       waspaused = false
+    pauseMenuAlpha = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+         if not GetBool("savegame.mod.options.cbHonkeyModel") then SetString("game.player.character","steam-3209546457"..'_'..'cb-honkey', true) end
+         --if not GetBool("savegame.mod.options.cbHonkeyModel") then SetString("game.player.character",Loader.mod_id..'_'..'cb-honkey', true) end
+
+         SetTimeScale(GetFloat("savegame.mod.options.timescale"))
+         --[[if not HasVersion('1.5.4') then
+             if PauseMenuButton("GNOptions", true) then SetBool("level.settingsOpened",true, true) end
+         else
+             if PauseMenuButton("Back To GnoMenu", "main_top") then StartLevel("", "MOD/main.xml") end
+         end]]
+
+         if not HasVersion('1.5.4') then
+             if PauseMenuButton("Back To GnoMenu", true) then StartLevel("", "MOD/main.xml") end
+         else
+             if PauseMenuButton("Back To GnoMenu", "main_top") then StartLevel("", "MOD/main.xml") end
+         end
+
+         if not justButton then
+             if not fraudChecked then
+                 if GetInt("savegame.mod.stats.levelOrder")+1 == GetInt("level.currentLevelInt") and GetBool("savegame.mod.stats.adventureBegun") then
+                     fraud = false
+                 else
+                     fraud = true
+                 end
+
+                 if fraud then
+                     ClearKey("savegame.mod.stats.score.inRun")
+                     ClearKey("savegame.mod.stats.time.inRun")
+                     ClearKey("savegame.mod.stats.adventureBegun")
+                     ClearKey("savegame.mod.stats.levelOrder")
+                     mapTime = 0
+                 else
+                     mapTime = GetFloat("savegame.mod.stats.time.inRun")
+                     --SetFloat("savegame.mod.stats.time.inRun", 0, true)
+                 end
+                 fraudChecked = true
+             end
+             if not GetBool("level.titleCardLoad") then
+                 SetFloat("level.time", mapTime+GetTime(), true)
+             end
+
+             --modifiers
+             if GetBool("savegame.mod.modifiers.Blackout") then
+        local Environment = {
+        	ambient = 0,
+        	ambientexponent = 5,
+        	constant = {0, 0, 0},
+        	exposure = {0, 20},
+        	fogcolor = {0, 0, 0},
+        	fogparams = {-0, 0, 0, 0},
+        	nightlight = true,
+        	skyboxbrightness = 0,
+        	sunbrightness = 0,
+        	suncolortint = {0,0,0},
+        	sundir = {0,0,0},
+        	sunfogscale = 1,
+        	sunglare = 0,
+        	sunlength = 0,
+        }
+        AutoSetEnvironment(Environment)
+        local postPros = {
+        	bloom = 0,
+        }
+        AutoSetPostProcessing(postPros)
+             end
+         end
+    end
+end
+
+function client.draw()
     if not justButton then
         if not GetBool("level.titleCardLoad") and not GetBool("level.playerIsDead") and not GetBool("savegame.mod.options.speedrunToggled") then
             UiTranslate(UiCenter(), UiHeight() * 0.04)
@@ -119,8 +117,8 @@
         end
     end
 
-    --SetBool("hud.disable",true)
-    InteractBody = GetPlayerInteractBody()
+    --SetBool("hud.disable",true, true)
+    InteractBody = GetPlayerInteractBody(playerId)
     if InteractBody ~= 0 then
             --[[com = GetBodyCenterOfMass(InteractBody)
             worldPoint = TransformToParentPoint(GetBodyTransform(InteractBody), com)]]
@@ -140,15 +138,16 @@
                 UiTextShadow(0,0,0,1,0.1)
                 UiText(GetTagValue(InteractBody,"interact"))
             UiPop()
-        InteractBody3 = GetPlayerInteractBody()
+        InteractBody3 = GetPlayerInteractBody(playerId)
         if not soundHover or InteractBody3 ~= InteractBody2 then
             UiSound("clickup.ogg",0.25,1.25)
             soundHover = true
         end
-        InteractBody2 = GetPlayerInteractBody()
+        InteractBody2 = GetPlayerInteractBody(playerId)
     else
         if soundHover then
             soundHover = false
         end
     end
-end+end
+

```

---

# Migration Report: scripts\titleCard.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\titleCard.lua
+++ patched/scripts\titleCard.lua
@@ -1,131 +1,4 @@
-function init()
-	titleCardTimer = 0
-	titleCardTimer2 = 0
-	titleCardStuff = {
-		{text="BARELY DYSFUNCTIONAL PRESENTS",startTime=3,endTime=5.7},
-		{text="TEARDOWNS FIRST WAVE SHOOTER",startTime=8.4,endTime=11.1},
-		{text="GNOME ZONE",startTime=13.7,endTime=16.5},
-	}
-	if HasKey("savegame.mod.titleCardLoad") then
-		titleCard = true
-		ClearKey("savegame.mod.titleCardLoad")
-		SetBool("level.titleCardLoad",true)
-	end
-	initT = GetPlayerTransform()
-	cardSprite = LoadSprite("MOD/assets/titleCard.png")
-	notifTimer = 0
-	notifNumber = 0
-	hintString = {
-		"The gnomes in the bottom left represent your health. Each colored gnome = 1 HP. Kill enemies and get POINTS to replenish health.","The mushrooms represent your dashes. These replenish passively overtime."
-	}
-
-
-	basicEnemyCount = #FindLocations("basic",true)
-	smallEnemyCount = #FindLocations("small",true)
-	jumpEnemyCount = #FindLocations("jump",true)
-	lungeEnemyCount = #FindLocations("lunge",true)
-	bigEnemyCount = #FindLocations("big",true)
-	fatEnemyCount = #FindLocations("fat",true)
-	explosiveEnemyCount = #FindLocations("explosive",true)
-	totalEnemies = basicEnemyCount+smallEnemyCount+jumpEnemyCount+lungeEnemyCount+bigEnemyCount+fatEnemyCount+explosiveEnemyCount
-	SetInt("level.gnomesKilled",0)
-
-	SetInt("level.currentLevelInt",3)
-end
-
-function draw(dt)
-	UiPush()
-		if not done then
-			
-			UiPush()
-				UiTranslate(UiCenter(), UiHeight() * 0.04)
-				UiTranslate(0,0)
-				UiFont("MOD/assets/Boomerank.ttf",31)
-				UiColor(0.8,0.4,0.4)
-				UiAlign("center middle")
-				if not GetBool("savegame.mod.endless") then
-					local subtractValue = totalEnemies-GetInt("level.gnomesKilled")
-					if subtractValue > 0 then
-						UiText(subtractValue.." LEFT")
-					end
-				else
-					UiText("ENDLESS MODE")
-					UiTranslate(0,20)
-					UiText("WAVE "..GetInt("level.hordeCurrentWave"))
-					UiTranslate(0,20)
-					UiText(GetInt("level.gnomeCurrentAmount").." LEFT")
-				end
-			UiPop()
-
-			titleCardTimer = titleCardTimer + dt
-			if titleCard then
-				titleCardTimer2 = titleCardTimer + 3
-				SetBool("hud.disable",true)
-				UiTranslate(UiCenter(), UiMiddle())
-				UiAlign("center middle")
-				if titleCardTimer2 < titleCardStuff[3].startTime then
-					UiColor(0,0,0)
-					UiRect(UiWidth(),UiHeight())
-					SetPlayerTransform(initT)
-				end
-				UiColor(1,1,1)
-				UiFont("MOD/assets/Gemstone.ttf",120)
-				
-				for i=1,#titleCardStuff do
-					local startTime = titleCardStuff[i].startTime
-					local endTime = titleCardStuff[i].endTime
-					if titleCardTimer2 > startTime and titleCardTimer2 < endTime then
-						if i == 3 then
-							UiFont("MOD/assets/Gemstone.ttf",200)
-							--[[UiColor(1,1,1,0.025)
-							UiImageBox("MOD/assets/gnome.png",1140, 1500)]]
-							--DrawSprite(cardSprite, Transform(TransformToParentPoint(GetCameraTransform(),Vec(0,0,-3)),GetCameraTransform().rot), 7.25,2.5, 1, 1, 1, 0.7, true)
-						else
-							UiColor(1,1,1,1)
-							UiText(titleCardStuff[i].text)
-						end
-					end
-				end
-
-				if titleCardTimer2 > titleCardStuff[3].endTime then
-					titleCard = false
-					SetBool("level.titleCardLoad",false)
-					notifTimer = 1
-				end
-			end
-			if notifTimer == 1 and notifNumber < 2 then
-				SetValue("notifTimer",-0.1,"linear",4)
-				notifNumber = notifNumber + 1
-			end
-			if notifTimer < 0 then
-				SetString("hud.notification",hintString[notifNumber])
-				notifTimer = 1
-			end
-			
-			--if HasVersion('1.5.4') then
-			if HasKey("level.currentWaveHorde.spawning") then
-				currentThing = GetInt("level.currentWaveHorde.spawning")
-			else
-				currentThing = 1
-			end
-			if currentThing < 7 then
-				PlayMusic("MOD/music/fight.ogg")
-				track1playing = true
-			elseif currentThing >= 7 then
-				PlayMusic("MOD/music/fight2.ogg")
-				if track1playing then
-					UiSound("MOD/music/fightOutro.ogg")
-					track1playing = false
-				end
-			end
-			if currentThing == 13 and not GetBool("savegame.mod.endless") then
-				StopMusic()
-				done = true
-			end
-		end
-	UiPop()
-end
-
+#version 2
 function render()
 	for i=1,#titleCardStuff do
 		local startTime = titleCardStuff[i].startTime
@@ -139,4 +12,130 @@
 			end
 		end
 	end
-end+end
+
+function server.init()
+    titleCardTimer = 0
+    titleCardTimer2 = 0
+    titleCardStuff = {
+    	{text="BARELY DYSFUNCTIONAL PRESENTS",startTime=3,endTime=5.7},
+    	{text="TEARDOWNS FIRST WAVE SHOOTER",startTime=8.4,endTime=11.1},
+    	{text="GNOME ZONE",startTime=13.7,endTime=16.5},
+    }
+    if HasKey("savegame.mod.titleCardLoad") then
+    	titleCard = true
+    	ClearKey("savegame.mod.titleCardLoad")
+    	SetBool("level.titleCardLoad",true, true)
+    end
+    initT = GetPlayerTransform(playerId)
+    cardSprite = LoadSprite("MOD/assets/titleCard.png")
+    notifTimer = 0
+    notifNumber = 0
+    hintString = {
+    	"The gnomes in the bottom left represent your health. Each colored gnome = 1 HP. Kill enemies and get POINTS to replenish health.","The mushrooms represent your dashes. These replenish passively overtime."
+    }
+    basicEnemyCount = #FindLocations("basic",true)
+    smallEnemyCount = #FindLocations("small",true)
+    jumpEnemyCount = #FindLocations("jump",true)
+    lungeEnemyCount = #FindLocations("lunge",true)
+    bigEnemyCount = #FindLocations("big",true)
+    fatEnemyCount = #FindLocations("fat",true)
+    explosiveEnemyCount = #FindLocations("explosive",true)
+    totalEnemies = basicEnemyCount+smallEnemyCount+jumpEnemyCount+lungeEnemyCount+bigEnemyCount+fatEnemyCount+explosiveEnemyCount
+    SetInt("level.gnomesKilled",0, true)
+    SetInt("level.currentLevelInt",3, true)
+end
+
+function client.draw()
+    UiPush()
+    	if not done then
+
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight() * 0.04)
+    			UiTranslate(0,0)
+    			UiFont("MOD/assets/Boomerank.ttf",31)
+    			UiColor(0.8,0.4,0.4)
+    			UiAlign("center middle")
+    			if not GetBool("savegame.mod.endless") then
+    				local subtractValue = totalEnemies-GetInt("level.gnomesKilled")
+    				if subtractValue ~= 0 then
+    					UiText(subtractValue.." LEFT")
+    				end
+    			else
+    				UiText("ENDLESS MODE")
+    				UiTranslate(0,20)
+    				UiText("WAVE "..GetInt("level.hordeCurrentWave"))
+    				UiTranslate(0,20)
+    				UiText(GetInt("level.gnomeCurrentAmount").." LEFT")
+    			end
+    		UiPop()
+
+    		titleCardTimer = titleCardTimer + dt
+    		if titleCard then
+    			titleCardTimer2 = titleCardTimer + 3
+    			SetBool("hud.disable",true, true)
+    			UiTranslate(UiCenter(), UiMiddle())
+    			UiAlign("center middle")
+    			if titleCardTimer2 < titleCardStuff[3].startTime then
+    				UiColor(0,0,0)
+    				UiRect(UiWidth(),UiHeight())
+    				SetPlayerTransform(playerId, initT)
+    			end
+    			UiColor(1,1,1)
+    			UiFont("MOD/assets/Gemstone.ttf",120)
+
+    			for i=1,#titleCardStuff do
+    				local startTime = titleCardStuff[i].startTime
+    				local endTime = titleCardStuff[i].endTime
+    				if titleCardTimer2 > startTime and titleCardTimer2 < endTime then
+    					if i == 3 then
+    						UiFont("MOD/assets/Gemstone.ttf",200)
+    						--[[UiColor(1,1,1,0.025)
+    						UiImageBox("MOD/assets/gnome.png",1140, 1500)]]
+    						--DrawSprite(cardSprite, Transform(TransformToParentPoint(GetCameraTransform(),Vec(0,0,-3)),GetCameraTransform().rot), 7.25,2.5, 1, 1, 1, 0.7, true)
+    					else
+    						UiColor(1,1,1,1)
+    						UiText(titleCardStuff[i].text)
+    					end
+    				end
+    			end
+
+    			if titleCardTimer2 > titleCardStuff[3].endTime then
+    				titleCard = false
+    				SetBool("level.titleCardLoad",false, true)
+    				notifTimer = 1
+    			end
+    		end
+    		if notifTimer == 1 and notifNumber < 2 then
+    			SetValue("notifTimer",-0.1,"linear",4)
+    			notifNumber = notifNumber + 1
+    		end
+    		if notifTimer < 0 then
+    			SetString("hud.notification",hintString[notifNumber], true)
+    			notifTimer = 1
+    		end
+
+    		--if HasVersion('1.5.4') then
+    		if HasKey("level.currentWaveHorde.spawning") then
+    			currentThing = GetInt("level.currentWaveHorde.spawning")
+    		else
+    			currentThing = 1
+    		end
+    		if currentThing < 7 then
+    			PlayMusic("MOD/music/fight.ogg")
+    			track1playing = true
+    		elseif currentThing >= 7 then
+    			PlayMusic("MOD/music/fight2.ogg")
+    			if track1playing then
+    				UiSound("MOD/music/fightOutro.ogg")
+    				track1playing = false
+    			end
+    		end
+    		if currentThing == 13 and not GetBool("savegame.mod.endless") then
+    			StopMusic()
+    			done = true
+    		end
+    	end
+    UiPop()
+end
+

```

---

# Migration Report: scripts\tool.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\tool.lua
+++ patched/scripts\tool.lua
@@ -1,106 +1,4 @@
-function init(reload_times, is_reload)
-	---@module "autumn_tool_setup"
-	AUTUMNTOOLSETUP = Loader.File 'scripts/autumn_tool_setup.lua'
-	
-	---@module "noise"
-	NOISE = Loader.File 'scripts/noise.lua'
-
-	---@module "projectile"
-	PROJECTILE = Loader.File 'scripts/projectile.lua'
-	
-    Configuration = {
-        focal_dinner_plate_distance = 25,
-		focal_bone_for_offset = 'weapon.shoot',
-        focal_soft_fov_range = { 5, 5 },
-		focal_scale_range_with_fov = true,
-		focal_control_speed = 10,
-        focal_passive_recenter_speed = 1.5,
-		focal_limit_to_range_speed = 20,
-		focal_aiming_dampening = 3,
-
-		fire_rate = 3/3,
-
-		projectile_hole_size = { 0.375, 0.325, 0 },
-		
-		animation_lever_timings =         { 0.12, 0.16, 0.27, 0.21 },
-        animation_lever_handle_timings =  { 0.12, 0.16, 0.25, 0.05 },
-
-        k = {
-            default = {
-				pos = { 2.05, 0.76, 1 },
-				rot = { 2.45, 0.6, 1 },
-			},
-            just_grab = {
-				pos = { 1.2, 0.3, 0 },
-				rot = { 0.95, 0.3, 0 },
-			}
-		}
-	}
-	
-	Tool = AUTUMNTOOLSETUP.Create()
-	Tool:Initialize({ armature_xml = 'MOD/assets/leveraction.xml', armature_scale = 0.45, display_name = 'Mary', identification = 'gnome-weapon', group = 2 }):Register(true)
-	--MOD/leveraction-edited.xml
-	if is_reload then Tool:Spawn() end
-
-	Tool.memory.weights = {
-		aiming = 0,
-		movement = 0,
-        inspect = 0,
-		force_lever = 0.5,
-    }
-
-    Tool.memory.animation_flags = {}
-	
-	Tool.memory.post_processing_reset = true
-	Tool.memory.post_processing = AutoGetPostProcessing()
-
-	Tool.memory.focal = { 0, 0 }
-	Tool.memory.time = {
-		shoot = -1 / 0,
-        useable = -1 / 0,
-	}
-	Tool.memory.fov = GetFloat('options.gfx.fov')
-
-	Tool.memory.flavor = {
-		transform = {
-			pos = AutoSM_Define(Vec(), unpack(Configuration.k.default.pos)),
-			rot = AutoSM_DefineQuat(Quat(), unpack(Configuration.k.default.rot))
-		},
-	}
-	Tool.memory.snd = {
-		shoot = LoadSound('MOD/snd/weapon/famas_fire00.ogg', 15),
-		sub = LoadSound('MOD/snd/weapon/sub.ogg', 30),
-		tink = LoadSound('MOD/snd/weapon/tink0.ogg', 7.5),
-		leverstart = LoadSound('MOD/snd/ShotgunPumpStart0.ogg'),
-		leverend = LoadSound('MOD/snd/ShotgunPumpEnd0.ogg'),
-	}
-
-	Camera_Flavor = {
-		pos = AutoSM_Define(Vec(), 1.8, 0.6, 0.0),
-		rot = AutoSM_DefineQuat(Quat(), 1.8, 0.6, 0.0)
-	}
-	titleCardTimer = 0
-	titleCardStuff = {
-		{text="BARELY DYSFUNCTIONAL PRESENTS",startTime=3,endTime=5.7},
-		{text="AN EPIC TALE",startTime=8.4,endTime=11.1},
-		{text="POOP GNOMES",startTime=13.7,endTime=16.5},
-	}
-	leveraction_pickup = FindLocation("leveraction_pickup",true)
-	flashlightRifle = FindBody("flashlightRifle",true)
-	realFlashlightRifle = FindLight("realFlashlightRifle",true)
-	if IsHandleValid(realFlashlightRifle) then
-		flashlightoff()
-		flashlightToggled = false
-		SetLightEnabled(realFlashlightRifle,flashlightToggled)
-	end
-
-	toolThirdPersonOffsetX = 0
-	toolThirdPersonOffsetY = 0
-	toolThirdPersonOffsetZ = 0
-	cameraCooldown = 0
-	SetBool("level.gnomeZoneBeingPlayed",true)
-end
-
+#version 2
 function reload()
 	-- if Tool:Exists() then
     --     Tool:Remove()
@@ -114,469 +12,6 @@
 local function anim_01(v, d1, d2, d3, d4)
 	local e1, e2, e3, e4 = d1, d1+d2, d1+d2+d3, d1+d2+d3+d4
 	return (v < e2 and AutoSmoothStep(v, e1, e2) or AutoSmoothStep(v, e4, e3)), v > e4
-end
-
-function tick(dt)
-	AUTUMNTOOLSETUP.Tick(dt)
-
-	local Time = GetTime()
-	local original_fov = GetFloat('options.gfx.fov')
-	Tool.memory.fov = original_fov
-
-	local camera_target = Transform()
-
-	local lever_01 = 0
-	local shape_eject = false
-
-	do
-		local useable_and_equipped = Tool:Equipped() and Tool:Useable()
-		if not useable_and_equipped then
-            Tool.memory.time.useable = Time
-		end
-
-		--[[Configuration = {
-			focal_dinner_plate_distance = 25,
-			focal_bone_for_offset = 'weapon.shoot',
-			focal_soft_fov_range = { 5, 5 },
-			focal_scale_range_with_fov = true,
-			focal_control_speed = 10,
-			focal_passive_recenter_speed = 1.5,
-			focal_limit_to_range_speed = 20,
-			focal_aiming_dampening = 3,
-	
-			fire_rate = 3/3,
-	
-			projectile_hole_size = { 0.375, 0.325, 0 },
-			
-			animation_lever_timings =         { 0.12, 0.16, 0.27, 0.21 },
-			animation_lever_handle_timings =  { 0.12, 0.16, 0.25, 0.05 },
-	
-			k = {
-				default = {
-					pos = { 2.05, 0.76, 1 },
-					rot = { 2.45, 0.6, 1 },
-				},
-				just_grab = {
-					pos = { 1.2, 0.3, 0 },
-					rot = { 0.95, 0.3, 0 },
-				}
-			}
-		}
-
-		local xOffset = 0
-		local yOffset = 0
-		local zOffset = 0
-		local xADSPos = Configuration.k.default.pos[1]
-		local yADSPos = Configuration.k.default.pos[2]
-		local zADSPos = Configuration.k.default.pos[3]
-		currentThirdPerson = GetBool("game.thirdperson")
-		if currentThirdPerson then
-			xOffset = 2
-			yOffset = 2
-			zOffset = -2
-		end
-		Configuration.k.default.pos[1] = xADSPos+xOffset
-		Configuration.k.default.pos[2] = yADSPos+yOffset
-		Configuration.k.default.pos[3] = zADSPos+zOffset]]
-
-		local t = AutoSmoothStep(Time - Tool.memory.time.useable, 0, 1)
-		AutoSM_RecalculateK(Tool.memory.flavor.transform.pos, unpack(AutoTableLerp(Configuration.k.just_grab.pos, Configuration.k.default.pos, t)))
-		AutoSM_RecalculateK(Tool.memory.flavor.transform.rot, unpack(AutoTableLerp(Configuration.k.just_grab.rot, Configuration.k.default.rot, t)))
-	end
-
-	if Tool:Equipped() and Tool.memory.anim then
-		currentThirdPerson = GetBool("game.thirdperson")
-		if currentThirdPerson ~= lastThirdPerson then
-			if currentThirdPerson then
-				Tool:ChangeSkin('MOD/leveraction-edited.xml')
-			else
-				Tool:ChangeSkin('MOD/assets/leveraction.xml')
-			end
-		end
-		lastThirdPerson = GetBool("game.thirdperson")
-
-		local animation_speed_multi = 1
-		
-		Tool.memory.weights.aiming = AutoMove(Tool.memory.weights.aiming, InputDown 'grab' and 1 or 0, dt * 5 * animation_speed_multi)
-		Tool.memory.weights.movement = AutoMove(Tool.memory.weights.movement, VecLength(AutoPlayerInputDir()), dt * 2 * animation_speed_multi)
-
-		if Tool.memory.weights.aiming > 0 then
-			local gpws = GetPlayerWalkingSpeed()
-			SetPlayerWalkingSpeed(AutoMap(Tool.memory.weights.aiming, 0, 1, gpws, gpws * 1/2))
-			if currentThirdPerson then
-				fovReduction = 20
-			else
-				fovReduction = 10
-			end
-			Tool.memory.fov = AutoMap(Tool.memory.weights.aiming, 0, 1, original_fov, original_fov - fovReduction, true)
-		end
-		
-		do -- Focal Point Aiming
-            local control = { InputValue("camerax"), InputValue("cameray") }
-			
-			local mapping_multi = AutoMap(Tool.memory.weights.aiming, 0, 1, 1, 1) * (Configuration.focal_scale_range_with_fov and AutoMap(Tool.memory.fov, 60, 90, 2/3, 1) or 1)
-			local mapped_range = {
-				(Configuration.focal_soft_fov_range[1] * mapping_multi)*GetFloat("savegame.mod.options.weaponSway"),
-				(Configuration.focal_soft_fov_range[2] * mapping_multi)*GetFloat("savegame.mod.options.weaponSway"),
-			}
-
-			local control_multi = (Configuration.focal_control_speed*GetFloat("savegame.mod.options.weaponSway")) / (Configuration.focal_aiming_dampening * Tool.memory.weights.aiming + 1)
-			Tool.memory.focal[1] = AutoLerp(Tool.memory.focal[1], 0, math.min(1, dt * Configuration.focal_passive_recenter_speed)) + control[1] * control_multi
-			Tool.memory.focal[2] = AutoLerp(Tool.memory.focal[2], 0, math.min(1, dt * Configuration.focal_passive_recenter_speed)) + control[2] * control_multi
-
-			local function soft_clamp(v, len, speed)
-				if math.abs(v) > len then
-					local direction = v > 0 and 1 or -1
-					local edge = len * direction
-					return AutoLerp(v, edge, AutoClamp(dt * speed))
-				end
-
-				return v
-			end
-
-			Tool.memory.focal[1] = soft_clamp(Tool.memory.focal[1], mapped_range[1], Configuration.focal_limit_to_range_speed)
-			Tool.memory.focal[2] = soft_clamp(Tool.memory.focal[2], mapped_range[2], Configuration.focal_limit_to_range_speed)
-		end
-
-		local tool_local_transform = Transform()
-
-
-		do -- Sets the tool's local transform - The base animation layer
-			local xOffset = 0
-			local yOffset = 0
-			local zOffset = 0
-			local inspectCloserX = 0
-			local inspectCloserZ = 0
-			local ADSXOffset = 0
-			local ADSYOffset = 0
-			local ADSZOffset = 0
-			if currentThirdPerson then
-				xOffset = -0.175
-				yOffset = 0.1
-				zOffset = 0.38-(120-GetInt("options.gfx.fov"))/240
-				inspectCloserX = 0.2
-				inspectCloserZ = 0.4
-				ADSXOffset = 0.31
-				ADSYOffset = -0.15
-				ADSZOffset = -0.2
-
-				--[[if InputDown("o") then toolThirdPersonOffsetX = toolThirdPersonOffsetX + dt elseif InputDown("p") then toolThirdPersonOffsetX = toolThirdPersonOffsetX - dt end
-				if InputDown("k") then toolThirdPersonOffsetY = toolThirdPersonOffsetY + dt elseif InputDown("l") then toolThirdPersonOffsetY = toolThirdPersonOffsetY - dt end
-				if InputDown("n") then toolThirdPersonOffsetZ = toolThirdPersonOffsetZ + dt elseif InputDown("m") then toolThirdPersonOffsetZ = toolThirdPersonOffsetZ - dt end
-				DebugWatch("X",toolThirdPersonOffsetX)
-				DebugWatch("Y",toolThirdPersonOffsetY)
-				DebugWatch("Z",toolThirdPersonOffsetZ)]]
-
-				local lever_hand_transform_from_tool = TransformToParentTransform(Tool.memory.anim:GetBoneLocalTransform('weapon.lever'), Transform(Vec(-0.0324,-0.01, 0.1611),QuatEuler(90,180,0)))
-				local otherhand_transform_from_tool = TransformToParentTransform(Tool.memory.anim:GetBoneLocalTransform('weapon.otherhand'), Transform(Vec(0,0,0),QuatEuler(-90,0,0)))
-				--local otherhand_transform_from_tool = Transform(Vec(0.04,0,-0.3848),QuatEuler(-90,0,0))
-				
-				local handPositions = {lever_hand_transform_from_tool,otherhand_transform_from_tool}
-				local distFromPlayer = -(GetInt("options.gfx.fov")/100)-1
-
-				local anchorShape = Tool.memory.anim:GetShapesOfBone("weapon.camAnchor")
-
-				AttachCameraTo(anchorShape[1],true)
-				local camOffset = Transform(Vec(0.4869,0.0447,3.0923+distFromPlayer+toolThirdPersonOffsetZ))
-
-				local flavor_transform = { pos = AutoSM_Get(Tool.memory.flavor.transform.pos), rot = AutoSM_Get(Tool.memory.flavor.transform.rot) }
-                camOffset = TransformToParentTransform(camOffset, Transform(VecScale(flavor_transform.pos, -1)))
-
-				SetCameraOffsetTransform(camOffset, true)
-
-				local whereCamShouldBe = TransformToParentPoint(Transform(GetBodyTransform(GetToolBody()).pos,GetCameraTransform().rot),Vec(0.4869,0.0447,3.0923+distFromPlayer))
-				--local camCollideRaycastOrigin = TransformToParentPoint(Transform(whereCamShouldBe,GetCameraTransform().rot),Vec(0,0,-1))
-				--DrawLine(whereCamShouldBe,camCollideRaycastOrigin,1,1,1,0.5)
-
-				QueryRequire("physical")
-				local hit, dist, normal, shape = QueryRaycast(GetPlayerEyeTransform().pos, VecScale(VecNormalize(VecSub(GetPlayerEyeTransform().pos,whereCamShouldBe)),-1), 1.05)
-				if hit then
-					--DebugPrint(dist)
-					SetCameraOffsetTransform(Transform(Vec(0,0,(dist-1)-0.12)), true)
-					--DrawLine(GetCameraTransform().pos,camCollideRaycastOrigin,1,0,0)
-				end
-
-				SetToolHandPoseLocalTransform(handPositions[1],handPositions[2])
-			end
-
-			local lowered = Transform(Vec(0.35+xOffset, -0.315+yOffset, -0.62+zOffset), QuatEuler(-2.5, 0, 8))
-			local raised = Transform(Vec(0.322+xOffset, -0.26+yOffset, -0.58+zOffset), QuatEuler(-2.5, 0, 15))
-			local ads = Transform(Vec(0.0+xOffset+ADSXOffset, -0.185+yOffset+ADSYOffset, -0.4+zOffset+ADSZOffset), QuatEuler(-2.5, 0, 0))
-			local inspect = Transform(Vec(0.1+xOffset+inspectCloserX, -0.23+yOffset, -1+zOffset+inspectCloserZ), QuatEuler(8, 60, -20))
-			local inspect_middle = Transform(Vec(0.322+xOffset, -0.25+yOffset, -0.8+zOffset), QuatEuler(-5, 0, 15))
-			local cock = Transform(Vec(-0.1+xOffset+inspectCloserX, -0.2+yOffset, -0.6+zOffset), QuatEuler(30, -10, 60))
-            local cock_middle = Transform(Vec(0.1+xOffset+inspectCloserX, -0.45+yOffset, -0.5+zOffset), QuatEuler(-10, -10, 15))
-
-			tool_local_transform = AutoTransformLerp(lowered, raised, AutoSmoothStep(Tool.memory.weights.movement, 0, 1))
-			tool_local_transform = AutoTransformLerp(tool_local_transform, ads, AutoSmoothStep(Tool.memory.weights.aiming, 0, 1))
-
-			local shoot_01 = (Time - Tool.memory.time.shoot) / Configuration.fire_rate
-			lever_01 = anim_01(shoot_01, unpack(Configuration.animation_lever_handle_timings))
-			shell_eject = shoot_01 >= Configuration.animation_lever_timings[1] + Configuration.animation_lever_timings[2] + 0.1
-			local animation_exponent = 3
-
-			do -- Lever animation
-				tool_local_transform = lever_01 < 0.5 and
-					AutoTransformLerp(tool_local_transform, cock_middle, AutoMap(lever_01, 0.0, 0.5, 0, 1, true) ^ animation_exponent) or
-					AutoTransformLerp(cock_middle, cock, AutoMap(lever_01, 0.5, 1.0, 0, 1, true) ^ animation_exponent)
-			end
-			
-			do -- Inspect 2
-				local diff = Time - Tool.memory.time.useable
-
-                local c_ldel = 0.65
-				local c_ltim = 0.1
-                local c_ldur = 0.5
-				
-				local wt, inspect_end = anim_01(diff, 0.25, 0.15, 1.20, 0.20)
-				local lt = anim_01(diff, c_ldel, c_ltim, c_ldur, c_ltim)
-				
-
-				if wt > 0 then
-					tool_local_transform = AutoTransformLerp(tool_local_transform, inspect, wt)
-					lever_01 = lt
-
-                    tool_local_transform = TransformToParentTransform(tool_local_transform, AutoTransformScale(
-                        Transform(Vec(0, 0.01, 0.01), QuatEuler(5)),
-						lt
-					))
-
-                    tool_local_transform = TransformToParentTransform(tool_local_transform, AutoTransformScale(
-						Transform(Vec(0, -0.01, -0.08), QuatEuler(-2)),
-						anim_01(diff, c_ldel + c_ldur + c_ltim, 0.03, 0, 0.05)
-					))
-				end
-
-				if inspect_end then
-					titleCard = true
-					SetBool("level.titleCardEnabled",true)
-				end
-			end
-			
-			tool_local_transform = AUTUMNTOOLSETUP.OffsetTransformByFOV(tool_local_transform, 0.6)
-		end
-
-		do -- Lever sound
-			if (not Tool.memory.animation_flags.lever_out) and lever_01 >= 1 then
-				Tool.memory.animation_flags.lever_out = true
-				Tool.memory.animation_flags.lever_in = false
-				Tool.memory.animation_flags.eject = false
-                if not GetBool("level.startTitleCardSequence") then PlaySound(Tool.memory.snd.leverstart) end
-			end
-			
-			if (not Tool.memory.animation_flags.lever_in) and lever_01 < 1 then
-				Tool.memory.animation_flags.lever_in = true
-				if not GetBool("level.startTitleCardSequence") then PlaySound(Tool.memory.snd.leverend) end
-			end
-		end
-
-		do -- Shell ejection
-			if (not Tool.memory.animation_flags.eject) and shell_eject then
-				Tool.memory.animation_flags.eject = true
-
-				local T = Tool.memory.anim:GetBoneWorldTransform('weapon.shell')
-				local b = Spawn('MOD/assets/shell.xml', T, true, false) --[[@as body_handle]] [1]
-				shape_anim.FakeScaledPhysics(GetBodyShapes(b), b, T, 1)
-				SetBodyDynamic(b, true)
-				SetBodyActive(b, true)
-				
-				-- DIRECTION CHANGE
-				SetBodyVelocity(b, AutoTransformUp(T, 3)) -- transform up
-				ApplyBodyImpulse(b, AutoTransformOffset(GetBodyTransform(b), Vec(0, 0, -0.5)).pos, AutoTransformUp(T, 0.5)) -- gives it spin
-			end
-		end
-
-		do -- Apply Focal to local transform
-			tool_local_transform.pos[1] = tool_local_transform.pos[1] + Tool.memory.focal[1] / Tool.memory.fov * 0.5
-			tool_local_transform.rot = QuatRotateQuat(QuatEuler(-Tool.memory.focal[2], -Tool.memory.focal[1]), tool_local_transform.rot)
-		end
-
-		do -- Tool Jiggles
-            tool_local_transform = AutoTransformLerp(
-				tool_local_transform,
-                AUTUMNTOOLSETUP.TransformJiggle(tool_local_transform),
-                AutoMap(Tool.memory.weights.aiming, 0, 1, 1, 0.1)*GetFloat("savegame.mod.options.weaponSway")
-			)
-		end
-
-		local barrel_middle_t = Tool.memory.anim:GetBoneWorldTransform('weapon.shoot')
-		local barrel_middle = VecCopy(barrel_middle_t.pos)
-		local barrel_fwd = AutoTransformFwd(barrel_middle_t)
-		barrel_middle2 = VecCopy(barrel_middle)
-		barrel_fwd2 = VecCopy(barrel_fwd)
-
-		--- Draw actual aim
-		-- do
-		-- 	local g, ray = GNOMES.raycast(barrel_middle, barrel_fwd, Configuration.focal_dinner_plate_distance)
-		-- 	if g then
-		-- 		DebugLine(barrel_middle, ray.intersections[1], 1, 0, 0, 1)
-		-- 	end
-		-- end
-		-- QueryRequire('physical')
-		-- AutoDrawPlane(AutoPlane(AutoRaycast(barrel_middle, barrel_fwd, 50).intersection, barrel_middle_t.rot, { 0.5, 0.5 }), 0, 2, false, unpack(AutoPalette.vfchill.blue_light))
-		-- QueryRequire('physical')
-		-- AutoDrawPlane(AutoPlane(AutoVecMove(barrel_middle, barrel_fwd, Configuration.focal_dinner_plate_distance), barrel_middle_t.rot, { 0.5, 0.5, }), 0, 2, false, unpack(AutoPalette.vfchill.red_light))
-
-		if InputDown 'usetool' and Tool:Useable() and Time - Tool.memory.time.shoot >= Configuration.fire_rate then
-			AutoSM_AddVelocity(Tool.memory.flavor.transform.pos, Vec(0, 1, 4))
-			AutoSM_AddVelocity(Tool.memory.flavor.transform.rot, QuatEuler(3.5, -2, 0))
-			AutoSM_AddVelocity(Camera_Flavor.pos,                Vec(0, 0, 1.75))
-			AutoSM_AddVelocity(Camera_Flavor.rot,                QuatEuler(0.8, math.random() * -0.35))
-			ShakeCamera(0.5)
-
-			PlaySound(Tool.memory.snd.shoot, barrel_middle, 0.8)
-
-			Fx(barrel_middle, barrel_fwd, 0.4, 0.5)
-
-			Tool.memory.time.shoot = Time
-			Tool.memory.animation_flags.lever_out = false
-
-			do
-				local direction = VecCopy(barrel_fwd)
-				local quat = QuatLookAt(VecNormalize(direction), Vec())
-				
-				for i=1, 1 do
-					local randomized_direction = QuatRotateVec(quat, AutoVecRndHemi(1 - (0.025 / 360), 1))
-					AutumnShoot(barrel_middle, randomized_direction)
-				end
-				if GetBool("savegame.mod.modifiers.Kickback") then
-					SetPlayerVelocity(VecScale(barrel_fwd,-20))
-				end
-			end
-		end
-
-		do -- Muzzle Flash
-			local t = 1 - AutoSmoothStep(Time - Tool.memory.time.shoot, 0, 0.3)
-			if t > 0 then
-				PointLight(barrel_middle, 1, 0.45, 0.1, t * 8)
-			end
-		end
-
-		AutoSM_Update(Tool.memory.flavor.transform.pos, tool_local_transform.pos, dt * animation_speed_multi)
-		AutoSM_Update(Tool.memory.flavor.transform.rot, tool_local_transform.rot, dt * animation_speed_multi)
-
-		do
-			flavor_transform = { pos = AutoSM_Get(Tool.memory.flavor.transform.pos), rot = AutoSM_Get(Tool.memory.flavor.transform.rot) }
-
-			--Tool.memory.anim:SetTransformation('weapon', flavor_transform)
-
-			local shoot_01 = (Time - Tool.memory.time.shoot) / Configuration.fire_rate
-			
-            Tool.memory.anim:SetTransformation('weapon.lever', Transform(Vec(),
-                QuatEuler(lever_01 * 90)
-			))
-
-            Tool.memory.anim:SetTransformation('weapon.chamber', Transform(Vec(0, 0, lever_01 * 0.12), Quat()))
-            Tool.memory.anim:SetTransformation('weapon.pin', Transform(Vec(),
-				QuatEuler(math.min(AutoSmoothStep(shoot_01, 0.1, 0) * -90, lever_01 * -85))
-			))
-
-			Tool.memory.anim:ApplyRig()
-		end
-		barrel_middle2 = VecCopy(barrel_middle)
-		barrel_fwd2 = VecCopy(barrel_fwd)
-
-		if IsHandleValid(flashlightRifle) then
-			if InputPressed("flashlight") then
-				flashlightToggled = not flashlightToggled
-				SetLightEnabled(realFlashlightRifle,flashlightToggled)
-			end
-			local dir = QuatLookAt(VecNormalize(VecScale(barrel_fwd2,-1)), Vec())
-			local toolT = Transform(barrel_middle2,dir)
-			toolT.pos = TransformToParentPoint(toolT,Vec(0.03,-0.08,0.125))
-			SetBodyTransform(flashlightRifle,toolT)
-		end
-		
-		SetToolTransform(flavor_transform)
-	else
-		Tool.memory.weights.aiming = AutoLerp(Tool.memory.weights.aiming, 0, math.max(0, 1 - dt * 5))
-		Tool.memory.weights.movement = AutoLerp(Tool.memory.weights.movement, 0, math.max(0, 1 - dt * 5))
-		
-		Tool.memory.animation_flags.lever_out = false
-		
-		Tool.memory.focal[1] = AutoLerp(Tool.memory.focal[1], 0, math.max(0, 1 - dt * 5))
-		Tool.memory.focal[2] = AutoLerp(Tool.memory.focal[2], 0, math.max(0, 1 - dt * 5))
-	end
-	
-	AutoSM_Update(Camera_Flavor.pos, camera_target.pos, dt)
-	AutoSM_Update(Camera_Flavor.rot, camera_target.rot, dt)
-
-	local flavor_transform = { pos = AutoSM_Get(Camera_Flavor.pos), rot = AutoSM_Get(Camera_Flavor.rot) }
-	SetCameraOffsetTransform(flavor_transform, true)
-
-	if Tool.memory.fov ~= original_fov then
-		SetCameraFov(Tool.memory.fov)
-	end
-
-	if not Tool:Equipped() and GetInt("level.currentLevelInt") == 3 or not Tool:Equipped() and GetInt("level.currentLevelInt") == 4 then
-		SetString("game.player.tool",GetString("level.toolKey"))
-		SetBool(AutoKey('game.tool', GetString("level.toolKey"), 'enabled'), true)
-	end
-end
-
-function update(dt)
-	PROJECTILE.update(dt)
-end
-
-function draw(dt)
-	if Tool:Equipped() and Tool:Useable() and not GetBool("level.titleCardLoad") then
-		do -- Crosshair
-			local equip_t = AutoSmoothStep(GetTime() - Tool.memory.time.useable, 0, 0.25)
-
-			UiPush()
-			AutoUiCenter()
-
-			local x, y = AutoUIRaycastPlane(Tool.memory.anim:GetBoneLocalTransform(Configuration.focal_bone_for_offset).pos, AutoQuatFwd(AutoSM_Get(Tool.memory.flavor.transform.rot)), Configuration.focal_dinner_plate_distance, Tool.memory.fov)
-	
-
-			UiPush()
-			UiTranslate(x * equip_t, y * equip_t)
-			--UiColorFilter(1, 1, 1, AutoMap(AutoSmoothStep(Tool.memory.weights.aiming, 0, 1), 0, 1, 2, 0.56))
-			UiColorFilter(1, 1, 1, 1)
-			Crosshair(equip_t)
-			UiPop()
-
-			UiPop()
-			UiPush()
-				if IsHandleValid(leveraction_pickup) then
-					titleCardTimer = titleCardTimer + dt
-					if titleCard then
-						StartLevel("","MOD/main.xml","nomainmenu",true)
-						SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"))
-						SetInt("savegame.mod.stats.levelOrder",2)
-
-						SetBool("savegame.mod.titleCardLoad",true)
-						SetBool("hud.disable",true)
-						UiTranslate(UiCenter(), UiMiddle())
-						UiAlign("center middle")
-						if titleCardTimer > titleCardStuff[1].startTime then
-							--PlayMusic("MOD/music/fight.ogg")
-						end
-						UiColor(0,0,0)
-						UiRect(UiWidth(),UiHeight())
-						UiColor(1,1,1)
-						UiFont("MOD/assets/Gemstone.ttf",120)
-						for i=1,#titleCardStuff do
-							local startTime = titleCardStuff[i].startTime
-							local endTime = titleCardStuff[i].endTime
-							if titleCardTimer > startTime and titleCardTimer < endTime then
-								if i == 3 then
-									UiFont("MOD/assets/Gemstone.ttf",200)
-									UiColor(1,1,1,0.025)
-									UiImageBox("MOD/assets/gnome.png",1140, 1500)
-								end
-								UiColor(1,1,1,1)
-								UiText(titleCardStuff[i].text)
-							end
-						end
-					end
-					--[[if titleCardTimer > titleCardStuff[3].endTime then
-						StartLevel("","MOD/main.xml","nomainmenu",true)
-					end]]
-				end
-			UiPop()
-		end
-	end
 end
 
 function Crosshair(expand_t)
@@ -783,4 +218,532 @@
 			break
 		end
 	end
-end+end
+
+function server.init()
+    AUTUMNTOOLSETUP = Loader.File 'scripts/autumn_tool_setup.lua'
+    ---@module "noise"
+    NOISE = Loader.File 'scripts/noise.lua'
+    ---@module "projectile"
+    PROJECTILE = Loader.File 'scripts/projectile.lua'
+       Configuration = {
+           focal_dinner_plate_distance = 25,
+    	focal_bone_for_offset = 'weapon.shoot',
+           focal_soft_fov_range = { 5, 5 },
+    	focal_scale_range_with_fov = true,
+    	focal_control_speed = 10,
+           focal_passive_recenter_speed = 1.5,
+    	focal_limit_to_range_speed = 20,
+    	focal_aiming_dampening = 3,
+    	fire_rate = 3/3,
+    	projectile_hole_size = { 0.375, 0.325, 0 },
+    	animation_lever_timings =         { 0.12, 0.16, 0.27, 0.21 },
+           animation_lever_handle_timings =  { 0.12, 0.16, 0.25, 0.05 },
+           k = {
+               default = {
+    			pos = { 2.05, 0.76, 1 },
+    			rot = { 2.45, 0.6, 1 },
+    		},
+               just_grab = {
+    			pos = { 1.2, 0.3, 0 },
+    			rot = { 0.95, 0.3, 0 },
+    		}
+    	}
+    }
+    Tool = AUTUMNTOOLSETUP.Create()
+    Tool:Initialize({ armature_xml = 'MOD/assets/leveraction.xml', armature_scale = 0.45, display_name = 'Mary', identification = 'gnome-weapon', group = 2 }):Register(true)
+    --MOD/leveraction-edited.xml
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        AUTUMNTOOLSETUP.Tick(dt)
+        local Time = GetTime()
+        local original_fov = GetFloat('options.gfx.fov')
+        Tool.memory.fov = original_fov
+        local camera_target = Transform()
+        local lever_01 = 0
+        local shape_eject = false
+        do
+        	local useable_and_equipped = Tool:Equipped() and Tool:Useable()
+        	if not useable_and_equipped then
+                   Tool.memory.time.useable = Time
+        	end
+        	--[[Configuration = {
+        		focal_dinner_plate_distance = 25,
+        		focal_bone_for_offset = 'weapon.shoot',
+        		focal_soft_fov_range = { 5, 5 },
+        		focal_scale_range_with_fov = true,
+        		focal_control_speed = 10,
+        		focal_passive_recenter_speed = 1.5,
+        		focal_limit_to_range_speed = 20,
+        		focal_aiming_dampening = 3,
+        		fire_rate = 3/3,
+        		projectile_hole_size = { 0.375, 0.325, 0 },
+        		animation_lever_timings =         { 0.12, 0.16, 0.27, 0.21 },
+        		animation_lever_handle_timings =  { 0.12, 0.16, 0.25, 0.05 },
+        		k = {
+        			default = {
+        				pos = { 2.05, 0.76, 1 },
+        				rot = { 2.45, 0.6, 1 },
+        			},
+        			just_grab = {
+        				pos = { 1.2, 0.3, 0 },
+        				rot = { 0.95, 0.3, 0 },
+        			}
+        		}
+        	}
+        	local xOffset = 0
+        	local yOffset = 0
+        	local zOffset = 0
+        	local xADSPos = Configuration.k.default.pos[1]
+        	local yADSPos = Configuration.k.default.pos[2]
+        	local zADSPos = Configuration.k.default.pos[3]
+        	currentThirdPerson = GetBool("game.thirdperson")
+        	if currentThirdPerson then
+        		xOffset = 2
+        		yOffset = 2
+        		zOffset = -2
+        	end
+        	Configuration.k.default.pos[1] = xADSPos+xOffset
+        	Configuration.k.default.pos[2] = yADSPos+yOffset
+        	Configuration.k.default.pos[3] = zADSPos+zOffset]]
+        	local t = AutoSmoothStep(Time - Tool.memory.time.useable, 0, 1)
+        	AutoSM_RecalculateK(Tool.memory.flavor.transform.pos, unpack(AutoTableLerp(Configuration.k.just_grab.pos, Configuration.k.default.pos, t)))
+        	AutoSM_RecalculateK(Tool.memory.flavor.transform.rot, unpack(AutoTableLerp(Configuration.k.just_grab.rot, Configuration.k.default.rot, t)))
+        end
+        		Tool.memory.focal[1] = soft_clamp(Tool.memory.focal[1], mapped_range[1], Configuration.focal_limit_to_range_speed)
+        		Tool.memory.focal[2] = soft_clamp(Tool.memory.focal[2], mapped_range[2], Configuration.focal_limit_to_range_speed)
+        	end
+        	local tool_local_transform = Transform()
+        	do -- Sets the tool's local transform - The base animation layer
+        		local xOffset = 0
+        		local yOffset = 0
+        		local zOffset = 0
+        		local inspectCloserX = 0
+        		local inspectCloserZ = 0
+        		local ADSXOffset = 0
+        		local ADSYOffset = 0
+        		local ADSZOffset = 0
+        		tool_local_transform = AUTUMNTOOLSETUP.OffsetTransformByFOV(tool_local_transform, 0.6)
+        	end
+        	do -- Lever sound
+        	do -- Apply Focal to local transform
+        		tool_local_transform.pos[1] = tool_local_transform.pos[1] + Tool.memory.focal[1] / Tool.memory.fov * 0.5
+        		tool_local_transform.rot = QuatRotateQuat(QuatEuler(-Tool.memory.focal[2], -Tool.memory.focal[1]), tool_local_transform.rot)
+        	end
+        	do -- Tool Jiggles
+                   tool_local_transform = AutoTransformLerp(
+        			tool_local_transform,
+                       AUTUMNTOOLSETUP.TransformJiggle(tool_local_transform),
+                       AutoMap(Tool.memory.weights.aiming, 0, 1, 1, 0.1)*GetFloat("savegame.mod.options.weaponSway")
+        		)
+        	end
+        	local barrel_middle_t = Tool.memory.anim:GetBoneWorldTransform('weapon.shoot')
+        	local barrel_middle = VecCopy(barrel_middle_t.pos)
+        	local barrel_fwd = AutoTransformFwd(barrel_middle_t)
+        	barrel_middle2 = VecCopy(barrel_middle)
+        	barrel_fwd2 = VecCopy(barrel_fwd)
+        	--- Draw actual aim
+        	-- do
+        	-- 	local g, ray = GNOMES.raycast(barrel_middle, barrel_fwd, Configuration.focal_dinner_plate_distance)
+        	-- 	if g then
+        	-- 		DebugLine(barrel_middle, ray.intersections[1], 1, 0, 0, 1)
+        	-- 	end
+        	-- end
+        	-- QueryRequire('physical')
+        	-- AutoDrawPlane(AutoPlane(AutoRaycast(barrel_middle, barrel_fwd, 50).intersection, barrel_middle_t.rot, { 0.5, 0.5 }), 0, 2, false, unpack(AutoPalette.vfchill.blue_light))
+        	-- QueryRequire('physical')
+        	-- AutoDrawPlane(AutoPlane(AutoVecMove(barrel_middle, barrel_fwd, Configuration.focal_dinner_plate_distance), barrel_middle_t.rot, { 0.5, 0.5, }), 0, 2, false, unpack(AutoPalette.vfchill.red_light))
+        	end
+        	do -- Muzzle Flash
+        		local t = 1 - AutoSmoothStep(Time - Tool.memory.time.shoot, 0, 0.3)
+        		if t ~= 0 then
+        			PointLight(barrel_middle, 1, 0.45, 0.1, t * 8)
+        		end
+        	end
+        	AutoSM_Update(Tool.memory.flavor.transform.pos, tool_local_transform.pos, dt * animation_speed_multi)
+        	AutoSM_Update(Tool.memory.flavor.transform.rot, tool_local_transform.rot, dt * animation_speed_multi)
+        	do
+        		flavor_transform = { pos = AutoSM_Get(Tool.memory.flavor.transform.pos), rot = AutoSM_Get(Tool.memory.flavor.transform.rot) }
+        		--Tool.memory.anim:SetTransformation('weapon', flavor_transform)
+        		local shoot_01 = (Time - Tool.memory.time.shoot) / Configuration.fire_rate
+                   Tool.memory.anim:SetTransformation('weapon.lever', Transform(Vec(),
+                       QuatEuler(lever_01 * 90)
+        		))
+                   Tool.memory.anim:SetTransformation('weapon.chamber', Transform(Vec(0, 0, lever_01 * 0.12), Quat()))
+                   Tool.memory.anim:SetTransformation('weapon.pin', Transform(Vec(),
+        			QuatEuler(math.min(AutoSmoothStep(shoot_01, 0.1, 0) * -90, lever_01 * -85))
+        		))
+        		Tool.memory.anim:ApplyRig()
+        	end
+        	barrel_middle2 = VecCopy(barrel_middle)
+        	barrel_fwd2 = VecCopy(barrel_fwd)
+        	SetToolTransform(flavor_transform)
+        else
+        	Tool.memory.weights.aiming = AutoLerp(Tool.memory.weights.aiming, 0, math.max(0, 1 - dt * 5))
+        	Tool.memory.weights.movement = AutoLerp(Tool.memory.weights.movement, 0, math.max(0, 1 - dt * 5))
+        	Tool.memory.animation_flags.lever_out = false
+        	Tool.memory.focal[1] = AutoLerp(Tool.memory.focal[1], 0, math.max(0, 1 - dt * 5))
+        	Tool.memory.focal[2] = AutoLerp(Tool.memory.focal[2], 0, math.max(0, 1 - dt * 5))
+        end
+        AutoSM_Update(Camera_Flavor.pos, camera_target.pos, dt)
+        AutoSM_Update(Camera_Flavor.rot, camera_target.rot, dt)
+        local flavor_transform = { pos = AutoSM_Get(Camera_Flavor.pos), rot = AutoSM_Get(Camera_Flavor.rot) }
+        SetCameraOffsetTransform(flavor_transform, true)
+        if Tool.memory.fov ~= original_fov then
+        	SetCameraFov(Tool.memory.fov)
+        end
+        if not Tool:Equipped() and GetInt("level.currentLevelInt") == 3 or not Tool:Equipped() and GetInt("level.currentLevelInt") == 4 then
+        	SetString("game.player.tool",GetString("level.toolKey"), true)
+        	SetBool(AutoKey('game.tool', GetString("level.toolKey"), 'enabled'), true, true)
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        PROJECTILE.update(dt)
+    end
+end
+
+function client.init()
+    if is_reload then Tool:Spawn() end
+
+    Tool.memory.weights = {
+    	aiming = 0,
+    	movement = 0,
+           inspect = 0,
+    	force_lever = 0.5,
+       }
+
+       Tool.memory.animation_flags = {}
+
+    Tool.memory.post_processing_reset = true
+    Tool.memory.post_processing = AutoGetPostProcessing()
+
+    Tool.memory.focal = { 0, 0 }
+    Tool.memory.time = {
+    	shoot = -1 / 0,
+           useable = -1 / 0,
+    }
+    Tool.memory.fov = GetFloat('options.gfx.fov')
+
+    Tool.memory.flavor = {
+    	transform = {
+    		pos = AutoSM_Define(Vec(), unpack(Configuration.k.default.pos)),
+    		rot = AutoSM_DefineQuat(Quat(), unpack(Configuration.k.default.rot))
+    	},
+    }
+    Tool.memory.snd = {
+    	shoot = LoadSound('MOD/snd/weapon/famas_fire00.ogg', 15),
+    	sub = LoadSound('MOD/snd/weapon/sub.ogg', 30),
+    	tink = LoadSound('MOD/snd/weapon/tink0.ogg', 7.5),
+    	leverstart = LoadSound('MOD/snd/ShotgunPumpStart0.ogg'),
+    	leverend = LoadSound('MOD/snd/ShotgunPumpEnd0.ogg'),
+    }
+
+    Camera_Flavor = {
+    	pos = AutoSM_Define(Vec(), 1.8, 0.6, 0.0),
+    	rot = AutoSM_DefineQuat(Quat(), 1.8, 0.6, 0.0)
+    }
+    titleCardTimer = 0
+    titleCardStuff = {
+    	{text="BARELY DYSFUNCTIONAL PRESENTS",startTime=3,endTime=5.7},
+    	{text="AN EPIC TALE",startTime=8.4,endTime=11.1},
+    	{text="POOP GNOMES",startTime=13.7,endTime=16.5},
+    }
+    leveraction_pickup = FindLocation("leveraction_pickup",true)
+    flashlightRifle = FindBody("flashlightRifle",true)
+    realFlashlightRifle = FindLight("realFlashlightRifle",true)
+    if IsHandleValid(realFlashlightRifle) then
+    	flashlightoff()
+    	flashlightToggled = false
+    	SetLightEnabled(realFlashlightRifle,flashlightToggled)
+    end
+
+    toolThirdPersonOffsetX = 0
+    toolThirdPersonOffsetY = 0
+    toolThirdPersonOffsetZ = 0
+    cameraCooldown = 0
+    SetBool("level.gnomeZoneBeingPlayed",true, true)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if Tool:Equipped() and Tool.memory.anim then
+    	currentThirdPerson = GetBool("game.thirdperson")
+    	if currentThirdPerson ~= lastThirdPerson then
+    		if currentThirdPerson then
+    			Tool:ChangeSkin('MOD/leveraction-edited.xml')
+    		else
+    			Tool:ChangeSkin('MOD/assets/leveraction.xml')
+    		end
+    	end
+    	lastThirdPerson = GetBool("game.thirdperson")
+
+    	local animation_speed_multi = 1
+
+    	Tool.memory.weights.aiming = AutoMove(Tool.memory.weights.aiming, InputDown 'grab' and 1 or 0, dt * 5 * animation_speed_multi)
+    	Tool.memory.weights.movement = AutoMove(Tool.memory.weights.movement, VecLength(AutoPlayerInputDir()), dt * 2 * animation_speed_multi)
+
+    	if Tool.memory.weights.aiming ~= 0 then
+    		local gpws = GetPlayerWalkingSpeed()
+    		SetPlayerWalkingSpeed(AutoMap(Tool.memory.weights.aiming, 0, 1, gpws, gpws * 1/2))
+    		if currentThirdPerson then
+    			fovReduction = 20
+    		else
+    			fovReduction = 10
+    		end
+    		Tool.memory.fov = AutoMap(Tool.memory.weights.aiming, 0, 1, original_fov, original_fov - fovReduction, true)
+    	end
+
+    	do -- Focal Point Aiming
+               local control = { InputValue("camerax"), InputValue("cameray") }
+
+    		local mapping_multi = AutoMap(Tool.memory.weights.aiming, 0, 1, 1, 1) * (Configuration.focal_scale_range_with_fov and AutoMap(Tool.memory.fov, 60, 90, 2/3, 1) or 1)
+    		local mapped_range = {
+    			(Configuration.focal_soft_fov_range[1] * mapping_multi)*GetFloat("savegame.mod.options.weaponSway"),
+    			(Configuration.focal_soft_fov_range[2] * mapping_multi)*GetFloat("savegame.mod.options.weaponSway"),
+    		}
+
+    		local control_multi = (Configuration.focal_control_speed*GetFloat("savegame.mod.options.weaponSway")) / (Configuration.focal_aiming_dampening * Tool.memory.weights.aiming + 1)
+    		Tool.memory.focal[1] = AutoLerp(Tool.memory.focal[1], 0, math.min(1, dt * Configuration.focal_passive_recenter_speed)) + control[1] * control_multi
+    		Tool.memory.focal[2] = AutoLerp(Tool.memory.focal[2], 0, math.min(1, dt * Configuration.focal_passive_recenter_speed)) + control[2] * control_multi
+
+    		local function soft_clamp(v, len, speed)
+    			if math.abs(v) > len then
+    				local direction = v > 0 and 1 or -1
+    				local edge = len * direction
+    				return AutoLerp(v, edge, AutoClamp(dt * speed))
+    			end
+
+    			return v
+    		end
+    		if currentThirdPerson then
+    			xOffset = -0.175
+    			yOffset = 0.1
+    			zOffset = 0.38-(120-GetInt("options.gfx.fov"))/240
+    			inspectCloserX = 0.2
+    			inspectCloserZ = 0.4
+    			ADSXOffset = 0.31
+    			ADSYOffset = -0.15
+    			ADSZOffset = -0.2
+
+    			--[[if InputDown("o") then toolThirdPersonOffsetX = toolThirdPersonOffsetX + dt elseif InputDown("p") then toolThirdPersonOffsetX = toolThirdPersonOffsetX - dt end
+    			if InputDown("k") then toolThirdPersonOffsetY = toolThirdPersonOffsetY + dt elseif InputDown("l") then toolThirdPersonOffsetY = toolThirdPersonOffsetY - dt end
+    			if InputDown("n") then toolThirdPersonOffsetZ = toolThirdPersonOffsetZ + dt elseif InputDown("m") then toolThirdPersonOffsetZ = toolThirdPersonOffsetZ - dt end
+    			DebugWatch("X",toolThirdPersonOffsetX)
+    			DebugWatch("Y",toolThirdPersonOffsetY)
+    			DebugWatch("Z",toolThirdPersonOffsetZ)]]
+
+    			local lever_hand_transform_from_tool = TransformToParentTransform(Tool.memory.anim:GetBoneLocalTransform('weapon.lever'), Transform(Vec(-0.0324,-0.01, 0.1611),QuatEuler(90,180,0)))
+    			local otherhand_transform_from_tool = TransformToParentTransform(Tool.memory.anim:GetBoneLocalTransform('weapon.otherhand'), Transform(Vec(0,0,0),QuatEuler(-90,0,0)))
+    			--local otherhand_transform_from_tool = Transform(Vec(0.04,0,-0.3848),QuatEuler(-90,0,0))
+
+    			local handPositions = {lever_hand_transform_from_tool,otherhand_transform_from_tool}
+    			local distFromPlayer = -(GetInt("options.gfx.fov")/100)-1
+
+    			local anchorShape = Tool.memory.anim:GetShapesOfBone("weapon.camAnchor")
+
+    			AttachCameraTo(anchorShape[1],true)
+    			local camOffset = Transform(Vec(0.4869,0.0447,3.0923+distFromPlayer+toolThirdPersonOffsetZ))
+
+    			local flavor_transform = { pos = AutoSM_Get(Tool.memory.flavor.transform.pos), rot = AutoSM_Get(Tool.memory.flavor.transform.rot) }
+                   camOffset = TransformToParentTransform(camOffset, Transform(VecScale(flavor_transform.pos, -1)))
+
+    			SetCameraOffsetTransform(camOffset, true)
+
+    			local whereCamShouldBe = TransformToParentPoint(Transform(GetBodyTransform(GetToolBody()).pos,GetCameraTransform().rot),Vec(0.4869,0.0447,3.0923+distFromPlayer))
+    			--local camCollideRaycastOrigin = TransformToParentPoint(Transform(whereCamShouldBe,GetCameraTransform().rot),Vec(0,0,-1))
+    			--DrawLine(whereCamShouldBe,camCollideRaycastOrigin,1,1,1,0.5)
+
+    			QueryRequire("physical")
+    			local hit, dist, normal, shape = QueryRaycast(GetPlayerEyeTransform().pos, VecScale(VecNormalize(VecSub(GetPlayerEyeTransform().pos,whereCamShouldBe)),-1), 1.05)
+    			if hit then
+    				--DebugPrint(dist)
+    				SetCameraOffsetTransform(Transform(Vec(0,0,(dist-1)-0.12)), true)
+    				--DrawLine(GetCameraTransform().pos,camCollideRaycastOrigin,1,0,0)
+    			end
+
+    			SetToolHandPoseLocalTransform(handPositions[1],handPositions[2])
+    		end
+
+    		local lowered = Transform(Vec(0.35+xOffset, -0.315+yOffset, -0.62+zOffset), QuatEuler(-2.5, 0, 8))
+    		local raised = Transform(Vec(0.322+xOffset, -0.26+yOffset, -0.58+zOffset), QuatEuler(-2.5, 0, 15))
+    		local ads = Transform(Vec(0.0+xOffset+ADSXOffset, -0.185+yOffset+ADSYOffset, -0.4+zOffset+ADSZOffset), QuatEuler(-2.5, 0, 0))
+    		local inspect = Transform(Vec(0.1+xOffset+inspectCloserX, -0.23+yOffset, -1+zOffset+inspectCloserZ), QuatEuler(8, 60, -20))
+    		local inspect_middle = Transform(Vec(0.322+xOffset, -0.25+yOffset, -0.8+zOffset), QuatEuler(-5, 0, 15))
+    		local cock = Transform(Vec(-0.1+xOffset+inspectCloserX, -0.2+yOffset, -0.6+zOffset), QuatEuler(30, -10, 60))
+               local cock_middle = Transform(Vec(0.1+xOffset+inspectCloserX, -0.45+yOffset, -0.5+zOffset), QuatEuler(-10, -10, 15))
+
+    		tool_local_transform = AutoTransformLerp(lowered, raised, AutoSmoothStep(Tool.memory.weights.movement, 0, 1))
+    		tool_local_transform = AutoTransformLerp(tool_local_transform, ads, AutoSmoothStep(Tool.memory.weights.aiming, 0, 1))
+
+    		local shoot_01 = (Time - Tool.memory.time.shoot) / Configuration.fire_rate
+    		lever_01 = anim_01(shoot_01, unpack(Configuration.animation_lever_handle_timings))
+    		shell_eject = shoot_01 >= Configuration.animation_lever_timings[1] + Configuration.animation_lever_timings[2] + 0.1
+    		local animation_exponent = 3
+
+    		do -- Lever animation
+    			tool_local_transform = lever_01 < 0.5 and
+    				AutoTransformLerp(tool_local_transform, cock_middle, AutoMap(lever_01, 0.0, 0.5, 0, 1, true) ^ animation_exponent) or
+    				AutoTransformLerp(cock_middle, cock, AutoMap(lever_01, 0.5, 1.0, 0, 1, true) ^ animation_exponent)
+    		end
+
+    		do -- Inspect 2
+    			local diff = Time - Tool.memory.time.useable
+
+                   local c_ldel = 0.65
+    			local c_ltim = 0.1
+                   local c_ldur = 0.5
+
+    			local wt, inspect_end = anim_01(diff, 0.25, 0.15, 1.20, 0.20)
+    			local lt = anim_01(diff, c_ldel, c_ltim, c_ldur, c_ltim)
+
+    			if wt ~= 0 then
+    				tool_local_transform = AutoTransformLerp(tool_local_transform, inspect, wt)
+    				lever_01 = lt
+
+                       tool_local_transform = TransformToParentTransform(tool_local_transform, AutoTransformScale(
+                           Transform(Vec(0, 0.01, 0.01), QuatEuler(5)),
+    					lt
+    				))
+
+                       tool_local_transform = TransformToParentTransform(tool_local_transform, AutoTransformScale(
+    					Transform(Vec(0, -0.01, -0.08), QuatEuler(-2)),
+    					anim_01(diff, c_ldel + c_ldur + c_ltim, 0.03, 0, 0.05)
+    				))
+    			end
+
+    			if inspect_end then
+    				titleCard = true
+    				SetBool("level.titleCardEnabled",true, true)
+    			end
+    		end
+    		if (not Tool.memory.animation_flags.lever_out) and lever_01 >= 1 then
+    			Tool.memory.animation_flags.lever_out = true
+    			Tool.memory.animation_flags.lever_in = false
+    			Tool.memory.animation_flags.eject = false
+                   if not GetBool("level.startTitleCardSequence") then PlaySound(Tool.memory.snd.leverstart) end
+    		end
+
+    		if (not Tool.memory.animation_flags.lever_in) and lever_01 < 1 then
+    			Tool.memory.animation_flags.lever_in = true
+    			if not GetBool("level.startTitleCardSequence") then PlaySound(Tool.memory.snd.leverend) end
+    		end
+    	end
+
+    	do -- Shell ejection
+    		if (not Tool.memory.animation_flags.eject) and shell_eject then
+    			Tool.memory.animation_flags.eject = true
+
+    			local T = Tool.memory.anim:GetBoneWorldTransform('weapon.shell')
+    			local b = Spawn('MOD/assets/shell.xml', T, true, false) --[[@as body_handle]] [1]
+    			shape_anim.FakeScaledPhysics(GetBodyShapes(b), b, T, 1)
+    			SetBodyDynamic(b, true)
+    			SetBodyActive(b, true)
+
+    			-- DIRECTION CHANGE
+    			SetBodyVelocity(b, AutoTransformUp(T, 3)) -- transform up
+    			ApplyBodyImpulse(b, AutoTransformOffset(GetBodyTransform(b), Vec(0, 0, -0.5)).pos, AutoTransformUp(T, 0.5)) -- gives it spin
+    		end
+    	end
+    	if InputDown 'usetool' and Tool:Useable() and Time - Tool.memory.time.shoot >= Configuration.fire_rate then
+    		AutoSM_AddVelocity(Tool.memory.flavor.transform.pos, Vec(0, 1, 4))
+    		AutoSM_AddVelocity(Tool.memory.flavor.transform.rot, QuatEuler(3.5, -2, 0))
+    		AutoSM_AddVelocity(Camera_Flavor.pos,                Vec(0, 0, 1.75))
+    		AutoSM_AddVelocity(Camera_Flavor.rot,                QuatEuler(0.8, math.random() * -0.35))
+    		ShakeCamera(0.5)
+
+    		PlaySound(Tool.memory.snd.shoot, barrel_middle, 0.8)
+
+    		Fx(barrel_middle, barrel_fwd, 0.4, 0.5)
+
+    		Tool.memory.time.shoot = Time
+    		Tool.memory.animation_flags.lever_out = false
+
+    		do
+    			local direction = VecCopy(barrel_fwd)
+    			local quat = QuatLookAt(VecNormalize(direction), Vec())
+
+    			for i=1, 1 do
+    				local randomized_direction = QuatRotateVec(quat, AutoVecRndHemi(1 - (0.025 / 360), 1))
+    				AutumnShoot(barrel_middle, randomized_direction)
+    			end
+    			if GetBool("savegame.mod.modifiers.Kickback") then
+    				SetPlayerVelocity(playerId, VecScale(barrel_fwd,-20))
+    			end
+    		end
+    	if IsHandleValid(flashlightRifle) then
+    		if InputPressed("flashlight") then
+    			flashlightToggled = not flashlightToggled
+    			SetLightEnabled(realFlashlightRifle,flashlightToggled)
+    		end
+    		local dir = QuatLookAt(VecNormalize(VecScale(barrel_fwd2,-1)), Vec())
+    		local toolT = Transform(barrel_middle2,dir)
+    		toolT.pos = TransformToParentPoint(toolT,Vec(0.03,-0.08,0.125))
+    		SetBodyTransform(flashlightRifle,toolT)
+    	end
+end
+
+function client.draw()
+    if Tool:Equipped() and Tool:Useable() and not GetBool("level.titleCardLoad") then
+    	do -- Crosshair
+    		local equip_t = AutoSmoothStep(GetTime() - Tool.memory.time.useable, 0, 0.25)
+
+    		UiPush()
+    		AutoUiCenter()
+
+    		local x, y = AutoUIRaycastPlane(Tool.memory.anim:GetBoneLocalTransform(Configuration.focal_bone_for_offset).pos, AutoQuatFwd(AutoSM_Get(Tool.memory.flavor.transform.rot)), Configuration.focal_dinner_plate_distance, Tool.memory.fov)
+
+    		UiPush()
+    		UiTranslate(x * equip_t, y * equip_t)
+    		--UiColorFilter(1, 1, 1, AutoMap(AutoSmoothStep(Tool.memory.weights.aiming, 0, 1), 0, 1, 2, 0.56))
+    		UiColorFilter(1, 1, 1, 1)
+    		Crosshair(equip_t)
+    		UiPop()
+
+    		UiPop()
+    		UiPush()
+    			if IsHandleValid(leveraction_pickup) then
+    				titleCardTimer = titleCardTimer + dt
+    				if titleCard then
+    					StartLevel("","MOD/main.xml","nomainmenu",true)
+    					SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"), true)
+    					SetInt("savegame.mod.stats.levelOrder",2, true)
+
+    					SetBool("savegame.mod.titleCardLoad",true, true)
+    					SetBool("hud.disable",true, true)
+    					UiTranslate(UiCenter(), UiMiddle())
+    					UiAlign("center middle")
+    					if titleCardTimer > titleCardStuff[1].startTime then
+    						--PlayMusic("MOD/music/fight.ogg")
+    					end
+    					UiColor(0,0,0)
+    					UiRect(UiWidth(),UiHeight())
+    					UiColor(1,1,1)
+    					UiFont("MOD/assets/Gemstone.ttf",120)
+    					for i=1,#titleCardStuff do
+    						local startTime = titleCardStuff[i].startTime
+    						local endTime = titleCardStuff[i].endTime
+    						if titleCardTimer > startTime and titleCardTimer < endTime then
+    							if i == 3 then
+    								UiFont("MOD/assets/Gemstone.ttf",200)
+    								UiColor(1,1,1,0.025)
+    								UiImageBox("MOD/assets/gnome.png",1140, 1500)
+    							end
+    							UiColor(1,1,1,1)
+    							UiText(titleCardStuff[i].text)
+    						end
+    					end
+    				end
+    				--[[if titleCardTimer > titleCardStuff[3].endTime then
+    					StartLevel("","MOD/main.xml","nomainmenu",true)
+    				end]]
+    			end
+    		UiPop()
+    	end
+    end
+end
+

```

---

# Migration Report: scripts\tractorbeam.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\tractorbeam.lua
+++ patched/scripts\tractorbeam.lua
@@ -1,44 +1,55 @@
-tractorFile = GetStringParam("tractorFile", "MOD/snd/GnomesDetected.ogg")
-
-function init()
-    distFromCamera = 15
-    monologueTime = 5.5
-    windupTime = 25
-    windupTimer = windupTime
-
-    body = FindBody("lightbody")
-    origin = FindLocation("fakeorigin")
-    active = false
-    timer = 0
-    RegisterListenerTo("hordeover", "start")
-    TractorBeamZap = LoadSound("MOD/snd/TractorBeamZap.ogg",20)
-    PlaySound(TractorBeamZap)
-
-    speech = LoadSound(speechFile)
-end
+#version 2
 function start()
     active = true
     StopMusic()
     UiSound("MOD/assets/poopwizard/sounds/voicelines/oh my god they died.ogg",8)
 end
 
-function tick(dt)
+function clampVec(vec, minlen, maxlen)
+	local dir = VecNormalize(vec)
+	local len = VecLength(vec)
+
+	len = math.max(math.min(maxlen, len), minlen)
+
+	return VecScale(dir, len)
+end
+
+function server.init()
+    distFromCamera = 15
+    monologueTime = 5.5
+    windupTime = 25
+    windupTimer = windupTime
+    body = FindBody("lightbody")
+    origin = FindLocation("fakeorigin")
+    active = false
+    timer = 0
+    RegisterListenerTo("hordeover", "start")
+end
+
+function client.init()
+    TractorBeamZap = LoadSound("MOD/snd/TractorBeamZap.ogg",20)
+    PlaySound(TractorBeamZap)
+    speech = LoadSound(speechFile)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if active then
         if windupTimer <= 0 then
             if not soundPlayed then PlaySound(TractorBeamZap) soundPlayed = true end
-            local camPos = GetPlayerCameraTransform().pos
+            local camPos = GetPlayerCameraTransform(playerId).pos
             local originPos = GetLocationTransform(origin).pos
             local toOrigin = VecNormalize(VecSub(originPos, camPos))
             local pos = VecAdd(camPos, VecScale(toOrigin, distFromCamera))
             SetBodyTransform(body, Transform(pos, QuatLookAt(camPos, pos)))
-            
+
             --PlayMusic(tractorFile) --fuck you stop overriding my beam sounds
             timer = timer + dt
             if timer > monologueTime then
                 StartLevel("", "MOD/arena.xml", "", true)
-                SetInt("savegame.mod.stats.score.inRun", GetInt("level.score"))
-                SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"))
-                SetInt("savegame.mod.stats.levelOrder",3)
+                SetInt("savegame.mod.stats.score.inRun", GetInt("level.score"), true)
+                SetFloat("savegame.mod.stats.time.inRun", GetFloat("level.time"), true)
+                SetInt("savegame.mod.stats.levelOrder",3, true)
             end
         else
             windupTimer = windupTimer - dt
@@ -48,14 +59,3 @@
     end
 end
 
-function draw(dt)
-end
-
-function clampVec(vec, minlen, maxlen)
-	local dir = VecNormalize(vec)
-	local len = VecLength(vec)
-
-	len = math.max(math.min(maxlen, len), minlen)
-
-	return VecScale(dir, len)
-end
```

---

# Migration Report: war props\flame.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/war props\flame.lua
+++ patched/war props\flame.lua
@@ -1,22 +1,17 @@
-torch = FindShape("torch")
-firelight = FindLight("torchlight")
-t1 = GetFloatParam("t1", 3.7)
-t2 = GetFloatParam("t2", 5.12)
-timer = 0
-broken = false
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if broken then
+        	return
+        end
+        if IsShapeBroken(torch) then
+        	SetShapeEmissiveScale(torch, 0)
+        	broken= true
+        end
+        local intensity = 0.25 + ((math.sin(timer/2)+1)/8)+((math.sin(timer*t1)+1)/4)+((math.sin(timer*t2)+1)/4)
+        SetShapeEmissiveScale(torch, intensity)
+        --SetLightIntensity(firelight, intensity)
+        timer = timer + dt
+    end
+end
 
-function tick(dt)
-	if broken then
-		return
-	end
-
-	if IsShapeBroken(torch) then
-		SetShapeEmissiveScale(torch, 0)
-		broken= true
-	end
-
-	local intensity = 0.25 + ((math.sin(timer/2)+1)/8)+((math.sin(timer*t1)+1)/4)+((math.sin(timer*t2)+1)/4)
-	SetShapeEmissiveScale(torch, intensity)
-	--SetLightIntensity(firelight, intensity)
-	timer = timer + dt
-end
```
