# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,17 +1,109 @@
--- MAIN FUNCTIONS --
-
-function init()
-    -- tool setup
+#version 2
+function slash(length, angle) 
+    local origin = GetCameraTransform().pos
+    local slash = {
+        active = true, 
+        dir1 = VecNormalize(VecSub(getSlashPoint(false, length, angle), origin)),
+        dir2 = VecNormalize(VecSub(getSlashPoint(true, length, angle), origin)),
+        point1 = origin,
+        point2 = origin,
+        origin = origin,
+    }
+
+    table.insert(slashes, slash)
+    slashedDynamicBodies[slash] = {}
+    
+    PlaySound(swingSound, origin, 1)
+    PlaySound(getsugaSound, origin, 1)
+end
+
+function endAnimation()
+    slashT = 0
+    slashing = false
+    slashSwings = {}
+    slashAnimation.currentKeyframe = 1
+end
+
+function addKeyframe(anim, time, transform, event)
+    local keyframe = {}
+    keyframe.time = time
+    keyframe.transform = transform
+    keyframe.event = event or function () end
+    table.insert(anim.keyframes, keyframe)
+end
+
+function animation()
+    local anim = {}
+    anim.currentKeyframe = 1
+    anim.keyframes = {}
+    return anim
+end
+
+function playAnimation(anim, time, endEvent)
+    local currentKeyframe = anim.keyframes[anim.currentKeyframe]
+    local nextKeyframe = anim.keyframes[anim.currentKeyframe + 1]
+
+    if time > nextKeyframe.time then
+        if anim.currentKeyframe + 2 <= #anim.keyframes then
+            currentKeyframe = nextKeyframe
+            anim.currentKeyframe = anim.currentKeyframe + 1
+            nextKeyframe = anim.keyframes[anim.currentKeyframe + 1]
+
+            currentKeyframe.event()
+        else
+            endEvent()
+        end
+    end
+
+    local t = (time - currentKeyframe.time) / (nextKeyframe.time - currentKeyframe.time)
+    local pos = VecLerp(currentKeyframe.transform.pos, nextKeyframe.transform.pos, t)
+    local rot = QuatSlerp(currentKeyframe.transform.rot, nextKeyframe.transform.rot, t)
+
+    return Transform(pos, rot)
+end
+
+function optionsSlider(val, min, max)
+	UiColor(0.2, 0.6, 1)
+	UiPush()
+		UiTranslate(0, -8)
+		val = (val-min) / (max-min)
+		local w = 195
+		local done = false
+		UiRect(w, 3)
+		UiAlign("center middle")
+		UiTranslate(-195, 1)
+		val, done = UiSlider("ui/common/dot.png", "x", val*w, 0, w) / w
+		val = round((val*(max-min)+min), 2)
+	UiPop()
+	return val, done
+end
+
+function round(number, decimals)
+    local power = 10^decimals
+    return math.floor(number * power) / power
+end
+
+function activation(x, slope)
+	return (1.0 / (1.0 + (x/(1-x)) ^ (-slope)))
+end
+
+function getSlashPoint(negative, length, angle)
+    local sign = 1
+    if negative then sign = -1 end
+    return VecAdd(GetCameraTransform().pos, TransformToParentVec(GetCameraTransform(), Vec(length * math.cos(angle) * sign, length * math.sin(angle) * sign, -250)))
+end
+
+function rot(q, strength)
+    return QuatRotateQuat(q, QuatEuler(-5 * strength, 0, 0))
+end
+
+function clamp(n, min, max) return math.min(math.max(n, min), max) end
+
+function server.init()
     RegisterTool("revengeance", "Revengeance Katana", "MOD/vox/katana.vox")
-    SetBool("game.tool.revengeance.enabled", true)
-    
+    SetBool("game.tool.revengeance.enabled", true, true)
     -- sound variables
-    swingSound = LoadSound("MOD/snd/swing.ogg")
-    drawSound = LoadSound("MOD/snd/draw.ogg")
-    sheathSound = LoadSound("MOD/snd/sheath.ogg")
-    getsugaSound = LoadSound("MOD/snd/getsuga.ogg")
     drawn = false
-
     -- settings variables
     hidden = false
     slashOptions = false
@@ -47,7 +139,14 @@
     idleTransform = Transform(Vec(math.cos(slashAngle), -0.45, -2.5), QuatSlerp(rightRightRot, leftIdleRot, activation(slashAngle / math.pi, 4)))
 end
 
-function tick(dt)
+function client.init()
+    swingSound = LoadSound("MOD/snd/swing.ogg")
+    drawSound = LoadSound("MOD/snd/draw.ogg")
+    sheathSound = LoadSound("MOD/snd/sheath.ogg")
+    getsugaSound = LoadSound("MOD/snd/getsuga.ogg")
+end
+
+function client.tick(dt)
     if GetString("game.player.tool") == "revengeance" and GetBool("game.player.canusetool") then
         if InputPressed("m") and not slashOptions  then
             slashOptions = true
@@ -63,10 +162,10 @@
         end
 
         if InputDown("rmb") then
-            SetBool("game.input.locktool", true)    
-            SetBool("hud.aimdot", false)
+            SetBool("game.input.locktool", true, true)    
+            SetBool("hud.aimdot", false, true)
             SetTimeScale(timeScale)
-            
+
             if InputValue("mousewheel") ~= 0 and not slashing then
                 if InputDown("shift") then
                     slashLength = clamp(slashLength + InputValue("mousewheel") * 10, 10, 200)
@@ -86,7 +185,7 @@
                 table.insert(slashSwings, {angle = slashAngle, length = slashLength})
             end
         end
-        
+
         if InputReleased("rmb") then
             if not slashing then
                 slashSwings = {}
@@ -97,7 +196,7 @@
             slashing = true
             slashAnimation = animation()
             addKeyframe(slashAnimation, 0.0, idleTransform)
-            
+
             if #slashSwings == 0 then
                 table.insert(slashSwings, 1, {angle = slashAngle, length = slashLength})
             end
@@ -112,7 +211,7 @@
                 local slashRot = QuatEuler(-40 * sign, math.cos(slashA) * 35 * sign, -math.cos(slashA) * 90)
                 if i % 2 == 0 then slashRot = QuatRotateQuat(slashRot, QuatEuler(0, 0, 180)) end
                 local keyframes = {}
-                
+
                 slashRot = rot(slashRot, -30 * sign)
                 table.insert(keyframes, Transform(Vec(slashL * math.cos(slashA), slashL * math.sin(slashA), -0.2), slashRot))
                 slashRot = rot(slashRot, 15 * sign)
@@ -123,7 +222,7 @@
                 table.insert(keyframes, Transform(Vec(-slashL * math.cos(slashA) / 2, -slashL * math.sin(slashA) / 2, -2.5), slashRot))
                 slashRot = rot(slashRot, -8 * sign)
                 table.insert(keyframes, Transform(Vec(-slashL * math.cos(slashA), -slashL * math.sin(slashA), -1), slashRot))
-                
+
                 for j=1, #keyframes do
                     if j == 3 then
                         addKeyframe(slashAnimation, keyframeT, keyframes[j], function () slash(slashSwings[i].length, slashSwings[i].angle) end)
@@ -157,7 +256,7 @@
             t = Transform(VecLerp(prevIdleTransform.pos, idleTransform.pos, dt * 10), QuatSlerp(prevIdleTransform.rot, idleTransform.rot, dt * 10))
             prevIdleTransform = t
         end
-        
+
         SetToolTransform(t)
     else
         if drawn then
@@ -167,7 +266,7 @@
     end
 end
 
-function update(dt)
+function client.update(dt)
     ParticleReset()
     ParticleType("plain")
     ParticleTile(5)
@@ -179,7 +278,6 @@
     ParticleGravity(0)
     ParticleDrag(0)
     ParticleEmissive(4)
-    
     for i, slash in ipairs(slashes) do
         if slash.active then
             slash.point1 = VecAdd(slash.point1, VecScale(slash.dir1, dt * dt * 2000))
@@ -192,7 +290,7 @@
             if not slashDrawParticles then
                 DrawLine(slash.point1, slash.point2)
             end
-            
+
             for i=1, length do
                 local p = VecAdd(VecLerp(slash.point1, slash.point2, i/length), VecScale(fwd, math.sin(i * math.pi / length) * 1))
 
@@ -217,7 +315,7 @@
                 end
 
                 MakeHole(p, slashRadius, slashRadius, slashRadius, true)
-                
+
                 if slashSpawnFire then
                     SpawnFire(p)
                 end
@@ -261,7 +359,7 @@
     end
 end
 
-function draw()
+function client.draw()
     if GetString("game.player.tool") == "revengeance" then
         if InputDown("rmb") and not slashing then
             DebugLine(getSlashPoint(false, slashLength, slashAngle), getSlashPoint(true, slashLength, slashAngle), 1, 0, 0)
@@ -306,13 +404,13 @@
                     slashSpawnFire = true
                     slashDrawParticles = true
                     slashOptimization = true
-                    SetInt("savegame.mod.revengeance.slashDistance", slashDistance)
-                    SetInt("savegame.mod.revengeance.slashForce", slashForce)
-                    SetFloat("savegame.mod.revengeance.timeScale", timeScale)
-                    SetFloat("savegame.mod.revengeance.slashRadius", slashRadius)
-                    SetBool("savegame.mod.revengeance.slashSpawnFire", slashSpawnFire)
-                    SetBool("savegame.mod.revengeance.slashDrawParticles", slashDrawParticles)
-                    SetBool("savegame.mod.revengeance.slashOptimization", slashOptimization)
+                    SetInt("savegame.mod.revengeance.slashDistance", slashDistance, true)
+                    SetInt("savegame.mod.revengeance.slashForce", slashForce, true)
+                    SetFloat("savegame.mod.revengeance.timeScale", timeScale, true)
+                    SetFloat("savegame.mod.revengeance.slashRadius", slashRadius, true)
+                    SetBool("savegame.mod.revengeance.slashSpawnFire", slashSpawnFire, true)
+                    SetBool("savegame.mod.revengeance.slashDrawParticles", slashDrawParticles, true)
+                    SetBool("savegame.mod.revengeance.slashOptimization", slashOptimization, true)
                 end
             UiPop()
 
@@ -335,7 +433,7 @@
                 UiAlign("left")
                 UiColor(0.7, 0.6, 0.1)
                 UiText(slashDistance.."m")
-                SetInt("savegame.mod.revengeance.slashDistance", slashDistance)
+                SetInt("savegame.mod.revengeance.slashDistance", slashDistance, true)
             UiPop()
 
             UiTranslate(0, 50)
@@ -348,7 +446,7 @@
                 UiAlign("left")
                 UiColor(0.7, 0.6, 0.1)
                 UiText(slashRadius.."m")
-                SetFloat("savegame.mod.revengeance.slashRadius", slashRadius)
+                SetFloat("savegame.mod.revengeance.slashRadius", slashRadius, true)
             UiPop()
 
             UiTranslate(0, 50)
@@ -361,7 +459,7 @@
                 UiAlign("left")
                 UiColor(0.7, 0.6, 0.1)
                 UiText(slashForce)
-                SetInt("savegame.mod.revengeance.slashForce", slashForce)
+                SetInt("savegame.mod.revengeance.slashForce", slashForce, true)
             UiPop()
 
             UiTranslate(0, 50)
@@ -374,7 +472,7 @@
                 UiAlign("left")
                 UiColor(0.7, 0.6, 0.1)
                 UiText(timeScale)
-                SetFloat("savegame.mod.revengeance.timeScale", timeScale)
+                SetFloat("savegame.mod.revengeance.timeScale", timeScale, true)
             UiPop()
 
             UiTranslate(0, 50)
@@ -386,12 +484,12 @@
                 if slashSpawnFire then
                     if UiTextButton("Yes", 20, 20) then
                         slashSpawnFire = false
-                        SetBool("savegame.mod.revengeance.slashSpawnFire", slashSpawnFire)
+                        SetBool("savegame.mod.revengeance.slashSpawnFire", slashSpawnFire, true)
                     end
                 else
                     if UiTextButton("No", 20, 20) then
                         slashSpawnFire = true
-                        SetBool("savegame.mod.revengeance.slashSpawnFire", slashSpawnFire)
+                        SetBool("savegame.mod.revengeance.slashSpawnFire", slashSpawnFire, true)
                     end
                 end
             UiPop()
@@ -405,12 +503,12 @@
                 if slashDrawParticles then
                     if UiTextButton("Yes", 20, 20) then
                         slashDrawParticles = false
-                        SetBool("savegame.mod.revengeance.slashDrawParticles", slashDrawParticles)
+                        SetBool("savegame.mod.revengeance.slashDrawParticles", slashDrawParticles, true)
                     end
                 else
                     if UiTextButton("No", 20, 20) then
                         slashDrawParticles = true
-                        SetBool("savegame.mod.revengeance.slashDrawParticles", slashDrawParticles)
+                        SetBool("savegame.mod.revengeance.slashDrawParticles", slashDrawParticles, true)
                     end
                 end
             UiPop()
@@ -424,12 +522,12 @@
                 if slashOptimization then
                     if UiTextButton("Yes", 20, 20) then
                         slashOptimization = false
-                        SetBool("savegame.mod.revengeance.slashOptimization", slashOptimization)
+                        SetBool("savegame.mod.revengeance.slashOptimization", slashOptimization, true)
                     end
                 else
                     if UiTextButton("No", 20, 20) then
                         slashOptimization = true
-                        SetBool("savegame.mod.revengeance.slashOptimization", slashOptimization)
+                        SetBool("savegame.mod.revengeance.slashOptimization", slashOptimization, true)
                     end
                 end
             UiPop()
@@ -476,106 +574,3 @@
     end
 end
 
-function slash(length, angle) 
-    local origin = GetCameraTransform().pos
-    local slash = {
-        active = true, 
-        dir1 = VecNormalize(VecSub(getSlashPoint(false, length, angle), origin)),
-        dir2 = VecNormalize(VecSub(getSlashPoint(true, length, angle), origin)),
-        point1 = origin,
-        point2 = origin,
-        origin = origin,
-    }
-
-    table.insert(slashes, slash)
-    slashedDynamicBodies[slash] = {}
-    
-    PlaySound(swingSound, origin, 1)
-    PlaySound(getsugaSound, origin, 1)
-end
-
-function endAnimation()
-    slashT = 0
-    slashing = false
-    slashSwings = {}
-    slashAnimation.currentKeyframe = 1
-end
-
--- ANIMATION FUNCTIONS --
-
-function addKeyframe(anim, time, transform, event)
-    local keyframe = {}
-    keyframe.time = time
-    keyframe.transform = transform
-    keyframe.event = event or function () end
-    table.insert(anim.keyframes, keyframe)
-end
-
-function animation()
-    local anim = {}
-    anim.currentKeyframe = 1
-    anim.keyframes = {}
-    return anim
-end
-
-function playAnimation(anim, time, endEvent)
-    local currentKeyframe = anim.keyframes[anim.currentKeyframe]
-    local nextKeyframe = anim.keyframes[anim.currentKeyframe + 1]
-
-    if time > nextKeyframe.time then
-        if anim.currentKeyframe + 2 <= #anim.keyframes then
-            currentKeyframe = nextKeyframe
-            anim.currentKeyframe = anim.currentKeyframe + 1
-            nextKeyframe = anim.keyframes[anim.currentKeyframe + 1]
-
-            currentKeyframe.event()
-        else
-            endEvent()
-        end
-    end
-
-    local t = (time - currentKeyframe.time) / (nextKeyframe.time - currentKeyframe.time)
-    local pos = VecLerp(currentKeyframe.transform.pos, nextKeyframe.transform.pos, t)
-    local rot = QuatSlerp(currentKeyframe.transform.rot, nextKeyframe.transform.rot, t)
-
-    return Transform(pos, rot)
-end
-
--- UTILITY FUNCTIONS --
-
-function optionsSlider(val, min, max)
-	UiColor(0.2, 0.6, 1)
-	UiPush()
-		UiTranslate(0, -8)
-		val = (val-min) / (max-min)
-		local w = 195
-		local done = false
-		UiRect(w, 3)
-		UiAlign("center middle")
-		UiTranslate(-195, 1)
-		val, done = UiSlider("ui/common/dot.png", "x", val*w, 0, w) / w
-		val = round((val*(max-min)+min), 2)
-	UiPop()
-	return val, done
-end
-
-function round(number, decimals)
-    local power = 10^decimals
-    return math.floor(number * power) / power
-end
-
-function activation(x, slope)
-	return (1.0 / (1.0 + (x/(1-x)) ^ (-slope)))
-end
-
-function getSlashPoint(negative, length, angle)
-    local sign = 1
-    if negative then sign = -1 end
-    return VecAdd(GetCameraTransform().pos, TransformToParentVec(GetCameraTransform(), Vec(length * math.cos(angle) * sign, length * math.sin(angle) * sign, -250)))
-end
-
-function rot(q, strength)
-    return QuatRotateQuat(q, QuatEuler(-5 * strength, 0, 0))
-end
-
-function clamp(n, min, max) return math.min(math.max(n, min), max) end
```
