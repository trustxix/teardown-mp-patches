# Migration Report: main - Copy.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main - Copy.lua
+++ patched/main - Copy.lua
@@ -1,16 +1,7 @@
-if not HasKey("savegame.mod.vox") then
-    SetInt("savegame.mod.vox", 1)
-end
-if not HasKey("savegame.mod.sound") then
-    SetInt("savegame.mod.sound", 1)
-end
-
-----------------------------------------------------------------------------------------------------------
-
+#version 2
 function randomVec()
     return Vec(math.random() - 0.5, math.random() - 0.5, math.random() - 0.5)
 end
-
 
 function playRandomSound(handles, pos, volume)
     local snd = handles[math.random(#handles)]
@@ -354,7 +345,6 @@
 
 end
 
----Force Crush---
 function forcecrush()
     PlaySound(forcepush, toolPos, .6)
     local t = GetCameraTransform()
@@ -463,66 +453,230 @@
         end
     end
 end
--- Force Jump --
+
 function Boost()
-	local pt = GetPlayerTransform()
+	local pt = GetPlayerTransform(playerId)
 	local d = TransformToParentVec(pt, Vec(0, 6, 0))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	vel[2] = 0
 	vel = VecAdd(vel, d)
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
     PlaySound(forcepush, playerPos, .3)
 end
 
-function init()
-   saberVoxes = {
-        "MOD/vox/lightsword_double1.vox",
-        "MOD/vox/lightsword_double2.vox",
-        "MOD/vox/lightsword_red.vox",
-        "MOD/vox/lightsword_green.vox",
-        "MOD/vox/lightsword_blue.vox",
-        "MOD/vox/lightsword_purple.vox",
-        "MOD/vox/lightsword_yellow.vox",
-        "MOD/vox/lightsword_orange.vox",
-        "MOD/vox/lightsword_white.vox"
-    }
-
-    saberColors = {
-        {1, 0, 0},
-        {1, 0, 0},
-        {1, 0, 0},
-        {0, 1, 0},
-        {0, 0, 1},
-        {1, 0, 1},
-        {1, 1, 0},
-        {1, .3, 0},
-        {1, 1, 1}
-    }
-
-    saberSoundGroups = {
-        1, 2, 3, 2, 1, 2, 3, 2
-    }
-
-    voxIndex = GetInt("savegame.mod.vox")
-    vox = saberVoxes[voxIndex]
-    color = saberColors[voxIndex]
-    soundGroup = saberSoundGroups[voxIndex]
-
-    --Register tool and enable it
-    RegisterTool("sithsaber", "Sith Saber", vox)
-    SetBool("game.tool.sithsaber.enabled", true)
-    SetFloat("game.tool.sithsaber.ammo", 10000)
-
-    ready = 0
-    fireTime = 0
-
+function server.init()
+    saberVoxes = {
+         "MOD/vox/lightsword_double1.vox",
+         "MOD/vox/lightsword_double2.vox",
+         "MOD/vox/lightsword_red.vox",
+         "MOD/vox/lightsword_green.vox",
+         "MOD/vox/lightsword_blue.vox",
+         "MOD/vox/lightsword_purple.vox",
+         "MOD/vox/lightsword_yellow.vox",
+         "MOD/vox/lightsword_orange.vox",
+         "MOD/vox/lightsword_white.vox"
+     }
+     saberColors = {
+         {1, 0, 0},
+         {1, 0, 0},
+         {1, 0, 0},
+         {0, 1, 0},
+         {0, 0, 1},
+         {1, 0, 1},
+         {1, 1, 0},
+         {1, .3, 0},
+         {1, 1, 1}
+     }
+     saberSoundGroups = {
+         1, 2, 3, 2, 1, 2, 3, 2
+     }
+     voxIndex = GetInt("savegame.mod.vox")
+     vox = saberVoxes[voxIndex]
+     color = saberColors[voxIndex]
+     soundGroup = saberSoundGroups[voxIndex]
+     --Register tool and enable it
+     RegisterTool("sithsaber", "Sith Saber", vox)
+     SetBool("game.tool.sithsaber.enabled", true, true)
+     SetFloat("game.tool.sithsaber.ammo", 10000, true)
+     ready = 0
+     fireTime = 0
+     laserSnd = LoadLoop("MOD/snd/laser.ogg")
+     hitSnd = LoadLoop("MOD/snd/hit.ogg")
+     humSnd = LoadLoop("MOD/snd/hum01.ogg")
+     electro = LoadLoop("MOD/snd/electro.ogg")
+     crushSnds = {
+     }
+     sparkSnds = {
+     }
+     swingSnds = {
+     }
+     clashSnds = {
+     }
+     spinSnds = {
+     }
+     outSnds = {
+     }
+     inSnds = {
+     }
+     idleTransform = Transform(Vec(0.5, -0.5, -1), QuatEuler(80, 5, -5))
+     swingAnimation1 = animation()
+     addKeyframe(swingAnimation1, 0.1, Transform(Vec(-0.6, -0.2, -0.5), QuatEuler(30, 75, 0)))
+     addKeyframe(swingAnimation1, 0.2, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
+     addKeyframe(swingAnimation1, 0.3, Transform(Vec(0.8, -0.6, -0.5), QuatEuler(-30, -120, 0)))
+     swingAnimation2 = animation()
+     addKeyframe(swingAnimation2, 0.1, Transform(Vec(0.9, -0.2, -0.5), QuatEuler(45, -75, 0)))
+     addKeyframe(swingAnimation2, 0.15, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
+     addKeyframe(swingAnimation2, 0.25, Transform(Vec(-0.6, -0.6, -0.5), QuatEuler(-50, 120, 0)))
+     swingAnimation3 = animation()
+     addKeyframe(swingAnimation3, 0.1, Transform(Vec(0.2, 0.2, -0.5), QuatEuler(150, 0, -30)))
+     addKeyframe(swingAnimation3, 0.15, Transform(Vec(0, -0.5, -1), QuatEuler(10, 0, 0)))
+     addKeyframe(swingAnimation3, 0.25, Transform(Vec(-0.2, -1.5, -0.5), QuatEuler(-90, 0, -30)))
+     swingAnimations = {
+         swingAnimation1,
+         swingAnimation2,
+         swingAnimation3
+     }
+     swingDirections = {
+         Vec(1, 0, 0),
+         Vec(-1, 0, 0),
+         Vec(0, -1, 0)
+     }
+     swingAnimation = swingAnimation1
+     swingDirection = Vec()
+     transform = Transform()
+     on = true
+     swinging = false
+     clash = false
+     throwing = false
+     throwReturn = false
+     swingT = 0
+     hitT = 0
+     onT = 0
+     forceVelocity = Vec()
+     torqueVelocity = Vec()
+     throwDirection = Vec()
+     throwTarget = Vec()
+     throwTransform = Transform()
+     swordOffsetTransform = Transform(Vec(-0.1, -0.3, -0.1))
+     shapeLocalTransform = Transform(Vec(-0.15, -0.1, 0.45), Quat(-0.70711, 0, 0, 0.70711))
+     impulseBatch = {}
+     impulseApplyPos = Vec()
+     impulse = Vec()
+     theta = 0
+     cooldownTimer1 = 1
+     cooldownTimer2 = 0
+     playerTransform = Transform()
+     playerPos = Vec()
+     cameraTransform = Transform()
+     cameraDir = Vec()
+     toolBody = 0
+     toolTransform = Transform()
+     toolPos = Vec()
+     targetTransform = Transform()
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+            playerTransform = GetPlayerTransform(playerId)
+            playerPos = VecAdd(playerTransform.pos, Vec(0, 1, 0))
+            cameraTransform = GetPlayerCameraTransform(playerId)
+            cameraDir = TransformToParentVec(cameraTransform, Vec(0, 0, -1))
+        function push(pos)
+        QueryRequire("physical dynamic")
+        	local max = 8.5
+            local maxDist1 = 35
+            local maxMass1 = 500
+            local maxMass2 = 2500
+            local objectbodies = QueryAabbBodies( VecAdd(pos, Vec(-1, -1, -1)), VecAdd(pos, Vec(1, 1, 1)))
+            for i = 1, #objectbodies do
+                local objectbodies2 = objectbodies[i]
+                if IsBodyDynamic(objectbodies2) then
+                    local bb, bbba = GetBodyBounds(objectbodies2)
+                    local direction = VecSub(VecLerp(bb, bbba, 0.5), pos)
+                    local distance = VecLength(direction)
+                    local mass = GetBodyMass(objectbodies2)
+                    direction = VecScale(direction, 1 / distance)
+                    if distance < maxDist1 and IsBodyVisible(objectbodies2, max * 35) and mass > maxMass1 and mass < maxMass2 then 
+                        local distScale = 1 - math.min(distance / max, 1.0)
+                        local vel = GetBodyVelocity(objectbodies2)
+                        vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 11 * distScale))
+                        SetBodyVelocity(objectbodies2, vel)
+                    end
+                end
+            end
+        end
+        function get_bodys(pos)
+                QueryRequire("physical")
+        	local bods = QueryAabbBodies( VecAdd(pos, Vec(-3, -3, -3)), VecAdd(pos, Vec(3, 3, 3)))
+        end
+        function get_bodys1(pos)
+        	QueryRejectVehicle(vehicle)
+        	QueryRequire("physical")
+        	local bods = QueryAabbBodies( VecAdd(pos, Vec(-2, -2, -2)), VecAdd(pos, Vec(2, 2, 2)))
+        	for i=1, #bods do
+        		local body = bods[i]
+        		local com = GetBodyCenterOfMass(body)
+                        local mass = GetBodyMass(body)
+                        local voxelCount = GetShapeVoxelCount(shape)
+        		local t = TransformToParentPoint(GetBodyTransform(body), com)
+        		rv1 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
+
+        		local fwd = TransformToParentVec(com, Vec(0, 0, -1))
+        		local hit, dist, normal, shape = QueryRaycast(t, fwd, .15)
+        	end
+        end
+        function lookpos()
+          local t = GetCameraTransform()
+          local transform = TransformToParentVec(t, Vec(0, 0, -1))
+          hit, dist, normal, shape = QueryRaycast(t.pos, transform, 35)
+          if hit then
+              local pos = VecAdd(t.pos, VecScale(transform, dist))
+              return pos
+            else
+              return false
+            end
+        end
+        		-- Force Lift/Push/Pull
+            end
+        	--Check if light saber is selected
+            if throwing then
+                saberThrowUpdate(dt)
+            end
+            if on then
+                onT = math.min(onT + dt * 4, 1)
+            else
+                onT = math.max(onT - dt * 4, 0)
+            end
+            if swinging then
+                swingT = swingT + dt
+            end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if #impulseBatch ~= 0 then
+            for i, body in pairs(impulseBatch) do
+                local mass = GetBodyMass(body)
+                local bodyImpulse = VecScale(impulse, 1 / (mass + 50) * mass)
+                ApplyBodyImpulse(body, impulseApplyPos, bodyImpulse)
+            end
+            impulseBatch = {}
+        end
+        if cooldownTimer2 ~= 0 then
+            cooldownTimer1 = cooldownTimer1 - dt
+            cooldownTimer2 = cooldownTimer2 - dt
+        end
+        if cooldownTimer2 <= 0 then
+            cooldownTimer1 = 1
+        end
+    end
+end
+
+function client.init()
     openSnd = LoadSound("MOD/snd/open.ogg")
     closeSnd = LoadSound("MOD/snd/close.ogg")
     forcepush = LoadSound("MOD/snd/forcepush.ogg")
-    laserSnd = LoadLoop("MOD/snd/laser.ogg")
-    hitSnd = LoadLoop("MOD/snd/hit.ogg")
-    humSnd = LoadLoop("MOD/snd/hum01.ogg")
-    electro = LoadLoop("MOD/snd/electro.ogg")
     electro2 = LoadSound("MOD/snd/electro2.ogg")
     lightning1 = LoadSound("MOD/snd/lightning1.ogg")
     lightning2 = LoadSound("MOD/snd/lightning2.ogg")
@@ -531,16 +685,11 @@
     lightning5 = LoadSound("MOD/snd/lightning5.ogg")
     spark = LoadSound("thunder3.ogg")
     lightning = LoadSound("thunder-strike.ogg")
-    
-    crushSnds = {
         LoadSound("MOD/snd/crush1.ogg"),
         LoadSound("MOD/snd/crush2.ogg"),
         LoadSound("MOD/snd/crush3.ogg"),
         LoadSound("MOD/snd/crush4.ogg"),
         LoadSound("MOD/snd/crush5.ogg")
-    }
-
-    sparkSnds = {
         LoadSound("MOD/snd/spark0.ogg"),
         LoadSound("MOD/snd/spark1.ogg"),
         LoadSound("MOD/snd/spark2.ogg"),
@@ -548,9 +697,6 @@
         LoadSound("MOD/snd/spark4.ogg"),
         LoadSound("MOD/snd/spark5.ogg"),
         LoadSound("MOD/snd/spark6.ogg")
-    }
-
-    swingSnds = {
         LoadSound("MOD/snd/swng01.ogg"),
         LoadSound("MOD/snd/swng02.ogg"),
         LoadSound("MOD/snd/swng03.ogg"),
@@ -559,9 +705,6 @@
         LoadSound("MOD/snd/swng06.ogg"),
         LoadSound("MOD/snd/swng07.ogg"),
         LoadSound("MOD/snd/swng08.ogg")
-    }
-
-    clashSnds = {
         LoadSound("MOD/snd/clsh01.ogg"),
         LoadSound("MOD/snd/clsh02.ogg"),
         LoadSound("MOD/snd/clsh03.ogg"),
@@ -570,655 +713,471 @@
         LoadSound("MOD/snd/clsh06.ogg"),
         LoadSound("MOD/snd/clsh07.ogg"),
         LoadSound("MOD/snd/clsh08.ogg")
-    }
-
-    spinSnds = {
         LoadSound("MOD/snd/spin01.ogg"),
         LoadSound("MOD/snd/spin02.ogg")
-    }
-
-    outSnds = {
         LoadSound("MOD/snd/out04.ogg"),
         LoadSound("MOD/snd/out04.ogg")
-    }
-
-    inSnds = {
         LoadSound("MOD/snd/in04.ogg"),
         LoadSound("MOD/snd/in04.ogg")
-    }
-
-    idleTransform = Transform(Vec(0.5, -0.5, -1), QuatEuler(80, 5, -5))
-    
-    swingAnimation1 = animation()
-    addKeyframe(swingAnimation1, 0.1, Transform(Vec(-0.6, -0.2, -0.5), QuatEuler(30, 75, 0)))
-    addKeyframe(swingAnimation1, 0.2, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
-    addKeyframe(swingAnimation1, 0.3, Transform(Vec(0.8, -0.6, -0.5), QuatEuler(-30, -120, 0)))
-
-    swingAnimation2 = animation()
-    addKeyframe(swingAnimation2, 0.1, Transform(Vec(0.9, -0.2, -0.5), QuatEuler(45, -75, 0)))
-    addKeyframe(swingAnimation2, 0.15, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
-    addKeyframe(swingAnimation2, 0.25, Transform(Vec(-0.6, -0.6, -0.5), QuatEuler(-50, 120, 0)))
-
-    swingAnimation3 = animation()
-    addKeyframe(swingAnimation3, 0.1, Transform(Vec(0.2, 0.2, -0.5), QuatEuler(150, 0, -30)))
-    addKeyframe(swingAnimation3, 0.15, Transform(Vec(0, -0.5, -1), QuatEuler(10, 0, 0)))
-    addKeyframe(swingAnimation3, 0.25, Transform(Vec(-0.2, -1.5, -0.5), QuatEuler(-90, 0, -30)))
-
-    swingAnimations = {
-        swingAnimation1,
-        swingAnimation2,
-        swingAnimation3
-    }
-
-    swingDirections = {
-        Vec(1, 0, 0),
-        Vec(-1, 0, 0),
-        Vec(0, -1, 0)
-    }
-
-    swingAnimation = swingAnimation1
-    swingDirection = Vec()
-
-    transform = Transform()
-
-    on = true
-    swinging = false
-    clash = false
-    throwing = false
-    throwReturn = false
-    swingT = 0
-    hitT = 0
-    onT = 0
-
-    forceVelocity = Vec()
-    torqueVelocity = Vec()
-
-    throwDirection = Vec()
-    throwTarget = Vec()
-    throwTransform = Transform()
-
-    swordOffsetTransform = Transform(Vec(-0.1, -0.3, -0.1))
-    
-    shapeLocalTransform = Transform(Vec(-0.15, -0.1, 0.45), Quat(-0.70711, 0, 0, 0.70711))
-
-    impulseBatch = {}
-    impulseApplyPos = Vec()
-    impulse = Vec()
-
-    theta = 0
-
-    cooldownTimer1 = 1
-    cooldownTimer2 = 0
-
-    playerTransform = Transform()
-    playerPos = Vec()
-    cameraTransform = Transform()
-    cameraDir = Vec()
-
-    toolBody = 0
-    toolTransform = Transform()
-    toolPos = Vec()
-
-    targetTransform = Transform()
-end
-
-
-      
-function tick(dt)
-    playerTransform = GetPlayerTransform()
-    playerPos = VecAdd(playerTransform.pos, Vec(0, 1, 0))
-    cameraTransform = GetPlayerCameraTransform()
-    cameraDir = TransformToParentVec(cameraTransform, Vec(0, 0, -1))
-    
-	if GetString("game.player.tool") == "sithsaber" and GetPlayerVehicle() == 0 then
-
-        if vox == "MOD/vox/lightsword_double1.vox" then
-            idleTransform = Transform(Vec(0.2, -1.1, -1), QuatEuler(80, 5, -45))
-            swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
-        end
-        if on == false and vox == "MOD/vox/lightsword_double1.vox" then
-            idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
-        end
-        if vox == "MOD/vox/lightsword_double2.vox" then
-            idleTransform = Transform(Vec(0.5, -.9, -1), QuatEuler(80, 5, -5))
-            swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
-        end
-        if on == false and vox == "MOD/vox/lightsword_double2.vox" then
-            idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
-        end
-        if InputDown("space") and cooldownTimer1 > 0 then
-            Boost()
-            cooldownTimer2 = 3 
-        end
-        -- Force Crush
-        if InputDown("c") then 
-            forcecrush()
-        end
-        -- Force Lightning
-        if InputDown("e") then
-            SetPlayerHealth(1)  
-            PlayLoop(electro, toolPos, 1)
-            local t = GetCameraTransform()
-		    local pos = t.pos
-		    local dir = TransformToParentVec(t, Vec(0, 0, -1))
-		    local hit, dist, normal, shape = QueryRaycast(pos, dir, 35)
-            local hitpoint = VecAdd(pos, VecScale(dir, dist))
-            local hitpoint1 = VecAdd(pos, VecScale(dir, dist-1))
-            local hitpoint2 = VecAdd(pos, VecScale(dir, dist+1.5))
-            MakeHole(hitpoint, math.random(6, 15)*0.1, math.random(3, 9)*0.1, math.random(2, 6)*0.1, "silent")
-            get_bodys(hitpoint)
-            get_bodys(hipoint2)
-            if hit and math.random(1,3) == 3 then
-                --PointLight(hitpoint, color[1], color[2], color[3], math.random(10,30)) 
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    	if GetString("game.player.tool") == "sithsaber" and GetPlayerVehicle(playerId) == 0 then
+
+            if vox == "MOD/vox/lightsword_double1.vox" then
+                idleTransform = Transform(Vec(0.2, -1.1, -1), QuatEuler(80, 5, -45))
+                swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
+            end
+            if on == false and vox == "MOD/vox/lightsword_double1.vox" then
+                idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
+            end
+            if vox == "MOD/vox/lightsword_double2.vox" then
+                idleTransform = Transform(Vec(0.5, -.9, -1), QuatEuler(80, 5, -5))
+                swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
+            end
+            if on == false and vox == "MOD/vox/lightsword_double2.vox" then
+                idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
+            end
+            if InputDown("space") and cooldownTimer1 ~= 0 then
+                Boost()
+                cooldownTimer2 = 3 
+            end
+            -- Force Crush
+            if InputDown("c") then 
+                forcecrush()
+            end
+            -- Force Lightning
+            if InputDown("e") then
+                SetPlayerHealth(playerId, 1)  
+                PlayLoop(electro, toolPos, 1)
+                local t = GetCameraTransform()
+    		    local pos = t.pos
+    		    local dir = TransformToParentVec(t, Vec(0, 0, -1))
+    		    local hit, dist, normal, shape = QueryRaycast(pos, dir, 35)
+                local hitpoint = VecAdd(pos, VecScale(dir, dist))
+                local hitpoint1 = VecAdd(pos, VecScale(dir, dist-1))
+                local hitpoint2 = VecAdd(pos, VecScale(dir, dist+1.5))
+                MakeHole(hitpoint, math.random(6, 15)*0.1, math.random(3, 9)*0.1, math.random(2, 6)*0.1, "silent")
+                get_bodys(hitpoint)
+                get_bodys(hipoint2)
+                if hit and math.random(1,3) == 3 then
+                    --PointLight(hitpoint, color[1], color[2], color[3], math.random(10,30)) 
+                    ParticleReset()
+                    ParticleEmissive(1, 0, "easein")
+                    ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
+                    ParticleRadius(math.random(20, 30)*.001, 0, "smooth")
+                    ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
+                    ParticleTile(4)
+                    ParticleCollide(1)
+                    ParticleSticky(1)
+                    for i = 1, math.random(32, 64) do
+                        local vel = VecScale(randomVec(), math.random(1,2))
+                        SpawnParticle(hitpoint, vel, math.random(4,6))
+                    end
+                    ParticleReset()
+                    ParticleEmissive(1, 0, "easein")
+                    ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
+                    ParticleRadius(math.random(15, 25)*.001, 0, "smooth")
+                    ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
+                    ParticleTile(4)
+                    ParticleCollide(0, 1, "easeout")
+                    ParticleSticky(1, .3)
+                    for i = 1, math.random(32, 64) do
+                        local vel = VecScale(randomVec(), math.random(3,5))
+                        SpawnParticle(hitpoint, vel, math.random(4,5))
+                    end
+                    ParticleReset()
+                    ParticleEmissive(1, 0, "easein")
+                    ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
+                    ParticleRadius(math.random(10, 20)*.001, 0, "smooth")
+                    ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
+                    ParticleTile(4)
+                    ParticleCollide(0, 1, "easeout")
+                    ParticleSticky(1, .3)
+
+                    for i = 1, math.random(32, 64) do
+                        local vel = VecScale(randomVec(), math.random(7,10))
+                        SpawnParticle(hitpoint, vel, math.random(4,6))
+                    end
+                end
+               if hit and math.random(1,20) == 11 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1)
+                end
+
+                if hit and math.random(1,20) == 13 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1) 
+                end
+
+                if hit and math.random(1,20) == 14 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1)
+            end
+
+                if hit and math.random(1,20) == 15 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1) 		   
+            end
+
+              if InputPressed("e") then
+                   PlaySound(electro2, toolPos, 1)
+                end
+    end
+
+    function clearAllFires()
+        RemoveAabbFires(Vec(-10000, -10000, -10000), Vec(10000, 10000, 10000))
+    end
+    	    for i=1, #bods do
+    		local body = bods[i]
+    		local com = GetBodyCenterOfMass(body)
+    		local maxMass1 = 500
+            	local maxMass2 = 3500
+                  	local mass = GetBodyMass(body)
+                    local broken = IsBodyBroken(body)
+                    local voxelcount = GetShapeVoxelCount(shape)
+                    if mass < maxMass1 and mass < maxMass2 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then 
+    		local t = TransformToParentPoint(GetBodyTransform(body), com)
+    		rv = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
+                    rv2 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
+
+                    if math.random(1,4) == 4 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then
+                    SpawnFire(rv)
+                    QueryRejectVehicle(vehicle)               
+                    end
+
+            local fwd = TransformToParentVec(com, Vec(0, 0, -1))
+    		local hit, dist, normal, shape = QueryRaycast(t, fwd, 3)
+
+    		local e = VecAdd(t, VecScale(fwd, dist))
+
+    		local last = pos
+
+             if IsBodyActive(body, 40) and IsBodyVisible(body, 40) then	 
+    		for i=1, 14 do
+    			local t = i/10
+    			local p = VecLerp(pos, e, t)
+    			p = VecAdd(p, VecScale(VecNormalize(Vec(math.random(-3,3), math.random(-3,3), math.random(-3,3))), 0.2*t))
+                            DrawLine(last, p, 1.0, 1.0, 1.0, 1)
+    			last = p
+               	end
+    		end
+    	end
+       end
+    		if InputDown("q") and not InputDown("w") and not InputDown("s") then
+
+                PlaySound(forcepush, toolPos, .6)
+                strength = 1.3	--Strength of Force Lift
+                maxMass = 1000000	--The maximum mass for a body to be affected
+                maxDist = 35	--The maximum distance for bodies to be affected
+
+    			--Get all physical and dynamic bodies in front of camera
+    			local t = GetCameraTransform()
+    			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
+                local f = TransformToParentPoint(t, Vec(0, 0, -1))
+    			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
+    			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
+    			QueryRequire("physical dynamic")
+    			local bodies = QueryAabbBodies(mi, ma)
+
+    			--Loop through bodies and push them
+    			for i=1,#bodies do
+    				local b = bodies[i]
+
+    				--Compute body center point and distance
+    				local bmi, bma = GetBodyBounds(b)
+    				local bc = VecLerp(bmi, bma, 0.5)
+    				local dir = VecSub(bc, t.pos)
+    				local dist = VecLength(dir)
+    				dir = VecScale(dir, 1.0/dist)
+
+    				--Get body mass
+    				local mass = GetBodyMass(b)
+
+    				--Check if body is should be affected
+    				if dist < maxDist and mass < maxMass then
+    					--Make sure direction is always pointing slightly upwards
+    					--dir[2] = .5
+    					--dir = VecNormalize(dir)
+                        dir = Vec(0,.6,0)
+    					--Compute how much velocity to add
+    					local massScale = 1 - math.min(mass/maxMass, 1.0)
+    					local distScale = 1 - math.min(dist/maxDist, 1.0)
+    					local add = VecScale(dir, strength * massScale * distScale)
+
+    					--Add velocity to body
+    					local vel = GetBodyVelocity(b)
+    					vel = VecAdd(vel, add)
+    					SetBodyVelocity(b, vel)
+    				end
+    			end
+                -- Blue Force Effect
                 ParticleReset()
-                ParticleEmissive(1, 0, "easein")
-                ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
-                ParticleRadius(math.random(20, 30)*.001, 0, "smooth")
-                ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
-                ParticleTile(4)
-                ParticleCollide(1)
-                ParticleSticky(1)
-                for i = 1, math.random(32, 64) do
-                    local vel = VecScale(randomVec(), math.random(1,2))
-                    SpawnParticle(hitpoint, vel, math.random(4,6))
+                ParticleAlpha(.1, 0.05, "smooth")
+    			ParticleEmissive(1, .5, "smooth")
+    			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
+                --ParticleColor(color[1], color[2], color[3]) 
+    			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
+    			ParticleTile(14)
+    			ParticleCollide(0, 1, "smooth")
+                for i = 1, math.random(4, 8) do
+                    local vel = VecScale(randomVec(), math.random(7,10))
+                    SpawnParticle(f, vel, math.random(10,20)*.1)
                 end
+            end
+            if InputDown("q") and InputDown("w") and not InputDown("s") then
+
+                --SetPlayerVelocity(playerId, 0,0,0)
+                PlaySound(forcepush, toolPos, .6)
+                strength = 1	--Strength of Force Push
+                maxMass = 1000000	--The maximum mass for a body to be affected
+                maxDist = 35	--The maximum distance for bodies to be affected
+
+    			--Get all physical and dynamic bodies in front of camera
+    			local t = GetCameraTransform()
+    			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
+                local f = TransformToParentPoint(t, Vec(0, 0, -2.5))
+    			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
+    			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
+    			QueryRequire("physical dynamic")
+    			local bodies = QueryAabbBodies(mi, ma)
+
+    			--Loop through bodies and push them
+    			for i=1,#bodies do
+    				local b = bodies[i]
+
+    				--Compute body center point and distance
+    				local bmi, bma = GetBodyBounds(b)
+    				local bc = VecLerp(bmi, bma, 0.5)
+    				local dir = VecSub(bc, t.pos)
+    				local dist = VecLength(dir)
+    				dir = VecScale(dir, 1.0/dist)
+
+    				--Get body mass
+    				local mass = GetBodyMass(b)
+
+    				--Check if body is should be affected
+    				if dist < maxDist and mass < maxMass then
+    					--Make sure direction is always pointing slightly upwards
+    					dir[2] = 1
+    					dir = VecNormalize(dir)
+
+    					--Compute how much velocity to add
+    					local massScale = 1 - math.min(mass/maxMass, 1.0)
+    					local distScale = 1 - math.min(dist/maxDist, 1.0)
+    					local add = VecScale(dir, strength * massScale * distScale)
+
+    					--Add velocity to body
+    					local vel = GetBodyVelocity(b)
+    					vel = VecAdd(vel, add)
+    					SetBodyVelocity(b, vel)
+    				end
+    			end
+                -- Blue Force Effect
                 ParticleReset()
-                ParticleEmissive(1, 0, "easein")
-                ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
-                ParticleRadius(math.random(15, 25)*.001, 0, "smooth")
-                ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
-                ParticleTile(4)
-                ParticleCollide(0, 1, "easeout")
-                ParticleSticky(1, .3)
-                for i = 1, math.random(32, 64) do
-                    local vel = VecScale(randomVec(), math.random(3,5))
-                    SpawnParticle(hitpoint, vel, math.random(4,5))
+                ParticleAlpha(.1, 0.05, "smooth")
+    			ParticleEmissive(1, .5, "smooth")
+    			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
+                --ParticleColor(color[1], color[2], color[3])
+    			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
+    			ParticleTile(14)
+    			ParticleCollide(0, 1, "smooth")
+                for i = 1, math.random(4, 8) do
+                    local vel = VecScale(randomVec(), math.random(7,10))
+                    SpawnParticle(f, vel, math.random(10,20)*.1)
                 end
+            end
+            if InputDown("q") and InputDown("s") and not InputDown("w") then
+
+                --SetPlayerVelocity(playerId, 0,0,0)
+                PlaySound(forcepush, toolPos, .6)
+                strength = 1	--Strength of Force Pull
+                maxMass = 1000000	--The maximum mass for a body to be affected
+                maxDist = 35	--The maximum distance for bodies to be affected
+
+    			--Get all physical and dynamic bodies in front of camera
+    			local t = GetCameraTransform()
+    			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
+                local f = TransformToParentPoint(t, Vec(0, 0, 0))
+    			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
+    			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
+    			QueryRequire("physical dynamic")
+    			local bodies = QueryAabbBodies(mi, ma)
+
+    			--Loop through bodies and push them
+    			for i=1,#bodies do
+    				local b = bodies[i]
+
+    				--Compute body center point and distance
+    				local bmi, bma = GetBodyBounds(b)
+    				local bc = VecLerp(bmi, bma, 0.5)
+    				local dir = VecSub(bc, t.pos)
+    				local dist = VecLength(dir)
+    				dir = VecScale(dir, 1.0/dist)
+
+    				--Get body mass
+    				local mass = GetBodyMass(b)
+
+    				--Check if body is should be affected
+    				if dist < maxDist and mass < maxMass then
+    					--Make sure direction is always pointing slightly upwards
+    					dir[2] = -1
+    					dir = VecNormalize(dir)
+
+    					--Compute how much velocity to add
+    					local massScale = 1 - math.min(mass/maxMass, 1.0)
+    					local distScale = 1 - math.min(dist/maxDist, 1.0)
+    					local add = VecScale(dir, strength * massScale * distScale)
+
+    					--Add velocity to body
+    					local vel = GetBodyVelocity(b)
+    					vel = VecSub(vel, add)
+    					SetBodyVelocity(b, vel)
+    				end
+    			end
+                -- Blue Force Effect
                 ParticleReset()
-                ParticleEmissive(1, 0, "easein")
-                ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
-                ParticleRadius(math.random(10, 20)*.001, 0, "smooth")
-                ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
-                ParticleTile(4)
-                ParticleCollide(0, 1, "easeout")
-                ParticleSticky(1, .3)
-                     
-                for i = 1, math.random(32, 64) do
+                ParticleAlpha(.1, 0.05, "smooth")
+    			ParticleEmissive(1, .5, "smooth")
+    			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
+                --ParticleColor(color[1], color[2], color[3])
+    			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
+    			ParticleTile(14)
+    			ParticleCollide(0, 1, "smooth")
+                for i = 1, math.random(4, 8) do
                     local vel = VecScale(randomVec(), math.random(7,10))
-                    SpawnParticle(hitpoint, vel, math.random(4,6))
+                    SpawnParticle(f, vel, math.random(10,20)*.1)
                 end
             end
-           if hit and math.random(1,20) == 11 then 
-                Explosion(hitpoint, math.random(5, 8)*.1)
-            end
-
-            if hit and math.random(1,20) == 13 then 
-                Explosion(hitpoint, math.random(5, 8)*.1) 
-            end
-        
-            if hit and math.random(1,20) == 14 then 
-                Explosion(hitpoint, math.random(5, 8)*.1)
-        end
-         
-            if hit and math.random(1,20) == 15 then 
-                Explosion(hitpoint, math.random(5, 8)*.1) 		   
-        end
-
-          if InputPressed("e") then
-               PlaySound(electro2, toolPos, 1)
-            end
-end
-
-function clearAllFires()
-    RemoveAabbFires(Vec(-10000, -10000, -10000), Vec(10000, 10000, 10000))
-end
-
-function push(pos)
-QueryRequire("physical dynamic")
-	local max = 8.5
-    local maxDist1 = 35
-    local maxMass1 = 500
-    local maxMass2 = 2500
-    local objectbodies = QueryAabbBodies( VecAdd(pos, Vec(-1, -1, -1)), VecAdd(pos, Vec(1, 1, 1)))
-    for i = 1, #objectbodies do
-        local objectbodies2 = objectbodies[i]
-        if IsBodyDynamic(objectbodies2) then
-            local bb, bbba = GetBodyBounds(objectbodies2)
-            local direction = VecSub(VecLerp(bb, bbba, 0.5), pos)
-            local distance = VecLength(direction)
-            local mass = GetBodyMass(objectbodies2)
-            direction = VecScale(direction, 1 / distance)
-            if distance < maxDist1 and IsBodyVisible(objectbodies2, max * 35) and mass > maxMass1 and mass < maxMass2 then 
-                local distScale = 1 - math.min(distance / max, 1.0)
-                local vel = GetBodyVelocity(objectbodies2)
-                vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 11 * distScale))
-                SetBodyVelocity(objectbodies2, vel)
-            end
-        end
-    end
-end
-
-function get_bodys(pos)
-        QueryRequire("physical")
-	local bods = QueryAabbBodies( VecAdd(pos, Vec(-3, -3, -3)), VecAdd(pos, Vec(3, 3, 3)))
-	    for i=1, #bods do
-		local body = bods[i]
-		local com = GetBodyCenterOfMass(body)
-		local maxMass1 = 500
-        	local maxMass2 = 3500
-              	local mass = GetBodyMass(body)
-                local broken = IsBodyBroken(body)
-                local voxelcount = GetShapeVoxelCount(shape)
-                if mass < maxMass1 and mass < maxMass2 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then 
-		local t = TransformToParentPoint(GetBodyTransform(body), com)
-		rv = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
-                rv2 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
-                
-                if math.random(1,4) == 4 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then
-                SpawnFire(rv)
-                QueryRejectVehicle(vehicle)               
+    	if GetString("game.player.tool") == "sithsaber" then        
+            toolBody = GetToolBody()
+            toolTransform = GetBodyTransform(toolBody)
+            toolPos = toolTransform.pos
+
+            local shapes = GetBodyShapes(toolBody)
+
+            local handleShape = shapes[1]
+            local bladeShape = shapes[2]
+
+            SetTag(handleShape, "nocull", "true")
+            SetTag(bladeShape, "nocull", "true")
+
+            targetTransform = idleTransform
+
+    		--Check if tool is firing
+            if GetBool("game.player.canusetool") then
+                if InputDown("lmb") and not InputDown("rmb") then
+                    saberSwingStart()
                 end
-
-        local fwd = TransformToParentVec(com, Vec(0, 0, -1))
-		local hit, dist, normal, shape = QueryRaycast(t, fwd, 3)
-								
-		local e = VecAdd(t, VecScale(fwd, dist))
-
-		local last = pos
- 
-         if IsBodyActive(body, 40) and IsBodyVisible(body, 40) then	 
-		for i=1, 14 do
-			local t = i/10
-			local p = VecLerp(pos, e, t)
-			p = VecAdd(p, VecScale(VecNormalize(Vec(math.random(-3,3), math.random(-3,3), math.random(-3,3))), 0.2*t))
-                        DrawLine(last, p, 1.0, 1.0, 1.0, 1)
-			last = p
-           	end
-		end
-	end
-   end
-end
-
-
-function get_bodys1(pos)
-	QueryRejectVehicle(vehicle)
-	QueryRequire("physical")
-	local bods = QueryAabbBodies( VecAdd(pos, Vec(-2, -2, -2)), VecAdd(pos, Vec(2, 2, 2)))
-	for i=1, #bods do
-		local body = bods[i]
-		local com = GetBodyCenterOfMass(body)
-                local mass = GetBodyMass(body)
-                local voxelCount = GetShapeVoxelCount(shape)
-		local t = TransformToParentPoint(GetBodyTransform(body), com)
-		rv1 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
-
-		local fwd = TransformToParentVec(com, Vec(0, 0, -1))
-		local hit, dist, normal, shape = QueryRaycast(t, fwd, .15)
-	end
-end
-
-function lookpos()
-  local t = GetCameraTransform()
-  local transform = TransformToParentVec(t, Vec(0, 0, -1))
-  hit, dist, normal, shape = QueryRaycast(t.pos, transform, 35)
-  if hit then
-      local pos = VecAdd(t.pos, VecScale(transform, dist))
-      return pos
-    else
-      return false
-    end
-end
-   
-		-- Force Lift/Push/Pull
-		if InputDown("q") and not InputDown("w") and not InputDown("s") then
-
-            PlaySound(forcepush, toolPos, .6)
-            strength = 1.3	--Strength of Force Lift
-            maxMass = 1000000	--The maximum mass for a body to be affected
-            maxDist = 35	--The maximum distance for bodies to be affected
-
-			--Get all physical and dynamic bodies in front of camera
-			local t = GetCameraTransform()
-			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
-            local f = TransformToParentPoint(t, Vec(0, 0, -1))
-			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
-			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
-			QueryRequire("physical dynamic")
-			local bodies = QueryAabbBodies(mi, ma)
-
-			--Loop through bodies and push them
-			for i=1,#bodies do
-				local b = bodies[i]
-
-				--Compute body center point and distance
-				local bmi, bma = GetBodyBounds(b)
-				local bc = VecLerp(bmi, bma, 0.5)
-				local dir = VecSub(bc, t.pos)
-				local dist = VecLength(dir)
-				dir = VecScale(dir, 1.0/dist)
-
-				--Get body mass
-				local mass = GetBodyMass(b)
-				
-				--Check if body is should be affected
-				if dist < maxDist and mass < maxMass then
-					--Make sure direction is always pointing slightly upwards
-					--dir[2] = .5
-					--dir = VecNormalize(dir)
-                    dir = Vec(0,.6,0)
-					--Compute how much velocity to add
-					local massScale = 1 - math.min(mass/maxMass, 1.0)
-					local distScale = 1 - math.min(dist/maxDist, 1.0)
-					local add = VecScale(dir, strength * massScale * distScale)
-					
-					--Add velocity to body
-					local vel = GetBodyVelocity(b)
-					vel = VecAdd(vel, add)
-					SetBodyVelocity(b, vel)
-				end
-			end
-            -- Blue Force Effect
-            ParticleReset()
-            ParticleAlpha(.1, 0.05, "smooth")
-			ParticleEmissive(1, .5, "smooth")
-			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
-            --ParticleColor(color[1], color[2], color[3]) 
-			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
-			ParticleTile(14)
-			ParticleCollide(0, 1, "smooth")
-            for i = 1, math.random(4, 8) do
-                local vel = VecScale(randomVec(), math.random(7,10))
-                SpawnParticle(f, vel, math.random(10,20)*.1)
-            end
-        end
-
-        if InputDown("q") and InputDown("w") and not InputDown("s") then
-
-            --SetPlayerVelocity(0,0,0)
-            PlaySound(forcepush, toolPos, .6)
-            strength = 1	--Strength of Force Push
-            maxMass = 1000000	--The maximum mass for a body to be affected
-            maxDist = 35	--The maximum distance for bodies to be affected
-
-			--Get all physical and dynamic bodies in front of camera
-			local t = GetCameraTransform()
-			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
-            local f = TransformToParentPoint(t, Vec(0, 0, -2.5))
-			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
-			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
-			QueryRequire("physical dynamic")
-			local bodies = QueryAabbBodies(mi, ma)
-
-			--Loop through bodies and push them
-			for i=1,#bodies do
-				local b = bodies[i]
-
-				--Compute body center point and distance
-				local bmi, bma = GetBodyBounds(b)
-				local bc = VecLerp(bmi, bma, 0.5)
-				local dir = VecSub(bc, t.pos)
-				local dist = VecLength(dir)
-				dir = VecScale(dir, 1.0/dist)
-
-				--Get body mass
-				local mass = GetBodyMass(b)
-				
-				--Check if body is should be affected
-				if dist < maxDist and mass < maxMass then
-					--Make sure direction is always pointing slightly upwards
-					dir[2] = 1
-					dir = VecNormalize(dir)
-			
-					--Compute how much velocity to add
-					local massScale = 1 - math.min(mass/maxMass, 1.0)
-					local distScale = 1 - math.min(dist/maxDist, 1.0)
-					local add = VecScale(dir, strength * massScale * distScale)
-					
-					--Add velocity to body
-					local vel = GetBodyVelocity(b)
-					vel = VecAdd(vel, add)
-					SetBodyVelocity(b, vel)
-				end
-			end
-            -- Blue Force Effect
-            ParticleReset()
-            ParticleAlpha(.1, 0.05, "smooth")
-			ParticleEmissive(1, .5, "smooth")
-			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
-            --ParticleColor(color[1], color[2], color[3])
-			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
-			ParticleTile(14)
-			ParticleCollide(0, 1, "smooth")
-            for i = 1, math.random(4, 8) do
-                local vel = VecScale(randomVec(), math.random(7,10))
-                SpawnParticle(f, vel, math.random(10,20)*.1)
-            end
-        end
-
-        if InputDown("q") and InputDown("s") and not InputDown("w") then
-
-            --SetPlayerVelocity(0,0,0)
-            PlaySound(forcepush, toolPos, .6)
-            strength = 1	--Strength of Force Pull
-            maxMass = 1000000	--The maximum mass for a body to be affected
-            maxDist = 35	--The maximum distance for bodies to be affected
-
-			--Get all physical and dynamic bodies in front of camera
-			local t = GetCameraTransform()
-			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
-            local f = TransformToParentPoint(t, Vec(0, 0, 0))
-			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
-			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
-			QueryRequire("physical dynamic")
-			local bodies = QueryAabbBodies(mi, ma)
-
-			--Loop through bodies and push them
-			for i=1,#bodies do
-				local b = bodies[i]
-
-				--Compute body center point and distance
-				local bmi, bma = GetBodyBounds(b)
-				local bc = VecLerp(bmi, bma, 0.5)
-				local dir = VecSub(bc, t.pos)
-				local dist = VecLength(dir)
-				dir = VecScale(dir, 1.0/dist)
-
-				--Get body mass
-				local mass = GetBodyMass(b)
-				
-				--Check if body is should be affected
-				if dist < maxDist and mass < maxMass then
-					--Make sure direction is always pointing slightly upwards
-					dir[2] = -1
-					dir = VecNormalize(dir)
-			
-					--Compute how much velocity to add
-					local massScale = 1 - math.min(mass/maxMass, 1.0)
-					local distScale = 1 - math.min(dist/maxDist, 1.0)
-					local add = VecScale(dir, strength * massScale * distScale)
-					
-					--Add velocity to body
-					local vel = GetBodyVelocity(b)
-					vel = VecSub(vel, add)
-					SetBodyVelocity(b, vel)
-				end
-			end
-            -- Blue Force Effect
-            ParticleReset()
-            ParticleAlpha(.1, 0.05, "smooth")
-			ParticleEmissive(1, .5, "smooth")
-			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
-            --ParticleColor(color[1], color[2], color[3])
-			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
-			ParticleTile(14)
-			ParticleCollide(0, 1, "smooth")
-            for i = 1, math.random(4, 8) do
-                local vel = VecScale(randomVec(), math.random(7,10))
-                SpawnParticle(f, vel, math.random(10,20)*.1)
-            end
-        end
-    end
-
-	--Check if light saber is selected
-	if GetString("game.player.tool") == "sithsaber" then        
-        toolBody = GetToolBody()
-        toolTransform = GetBodyTransform(toolBody)
-        toolPos = toolTransform.pos
-
-        local shapes = GetBodyShapes(toolBody)
-          
-        local handleShape = shapes[1]
-        local bladeShape = shapes[2]
-
-        SetTag(handleShape, "nocull", "true")
-        SetTag(bladeShape, "nocull", "true")
-
-        targetTransform = idleTransform
-        
-		--Check if tool is firing
-        if GetBool("game.player.canusetool") then
-            if InputDown("lmb") and not InputDown("rmb") then
-                saberSwingStart()
-            end
-            if InputDown("rmb") and not InputDown("lmb") then
-                saberThrowStart()
-            end
-            if not swinging and not throwing and InputPressed("z") then
-                if on then
-                    saberOff()
-                    clearAllFires()
-                else
-                    saberOn()
+                if InputDown("rmb") and not InputDown("lmb") then
+                    saberThrowStart()
                 end
-            end
-            if swinging then
-                saberSwingUpdate(dt)
-            end
-		end
-
-        if throwing then
-            local rotationTransform = TransformToParentTransform(throwTransform, Transform(Vec(), QuatEuler(-90, GetTime() * 1200, 0)))
-            rotationTransform.rot = QuatRotateQuat(QuatAxisAngle(throwDirection, -theta), rotationTransform.rot)
-            local swordThrowTransform = TransformToParentTransform(rotationTransform, swordOffsetTransform)
-            local localTransform = TransformToLocalTransform(toolTransform, swordThrowTransform)
-
-            SetShapeLocalTransform(handleShape, localTransform)
-            SetShapeLocalTransform(bladeShape, TransformToParentTransform(localTransform, Transform(Vec(0.05, 0.5, 0.05))))
-        else
-            local pos = transform.pos
-            local rot = transform.rot
-
-            local bladeLength = 2 * onT - 1.5
-
-            transform = Transform(VecLerp(pos, targetTransform.pos, dt * 20), QuatSlerp(rot, targetTransform.rot, dt * 20))
-            
-            SetShapeLocalTransform(handleShape, shapeLocalTransform)
-            SetShapeLocalTransform(bladeShape, TransformToParentTransform(shapeLocalTransform, Transform(Vec(0.05, bladeLength, 0.05)))) 
-            SetToolTransform(transform, 1)
-
-            PointLight(VecAdd(toolPos, TransformToParentVec(toolTransform, Vec(0, 1, 0))), color[1], color[2], color[3], 4 * onT)
-            PlayLoop(humSnd, toolPos, onT)
-
-        end
-	end
-
-    if throwing then
-        saberThrowUpdate(dt)
-    end
-
-    if on then
-        onT = math.min(onT + dt * 4, 1)
-    else
-        onT = math.max(onT - dt * 4, 0)
-    end
-
-    if swinging then
-        swingT = swingT + dt
-    end
-end
-
-function update(dt)
-    if #impulseBatch > 0 then
-        for i, body in pairs(impulseBatch) do
-            local mass = GetBodyMass(body)
-            local bodyImpulse = VecScale(impulse, 1 / (mass + 50) * mass)
-            ApplyBodyImpulse(body, impulseApplyPos, bodyImpulse)
-        end
-        impulseBatch = {}
-    end
-    if cooldownTimer2 > 0 then
-        cooldownTimer1 = cooldownTimer1 - dt
-        cooldownTimer2 = cooldownTimer2 - dt
-    end
-    if cooldownTimer2 <= 0 then
-        cooldownTimer1 = 1
-    end
-    if InputDown("e") then SetPlayerHealth(1) end
-end
-
-function draw() -- Force Lightning Effects and Hands
-	if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 10 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock1.png")
-		UiPop()
-	end
+                if not swinging and not throwing and InputPressed("z") then
+                    if on then
+                        saberOff()
+                        clearAllFires()
+                    else
+                        saberOn()
+                    end
+                end
+                if swinging then
+                    saberSwingUpdate(dt)
+                end
+    		end
+
+            if throwing then
+                local rotationTransform = TransformToParentTransform(throwTransform, Transform(Vec(), QuatEuler(-90, GetTime() * 1200, 0)))
+                rotationTransform.rot = QuatRotateQuat(QuatAxisAngle(throwDirection, -theta), rotationTransform.rot)
+                local swordThrowTransform = TransformToParentTransform(rotationTransform, swordOffsetTransform)
+                local localTransform = TransformToLocalTransform(toolTransform, swordThrowTransform)
+
+                SetShapeLocalTransform(handleShape, localTransform)
+                SetShapeLocalTransform(bladeShape, TransformToParentTransform(localTransform, Transform(Vec(0.05, 0.5, 0.05))))
+            else
+                local pos = transform.pos
+                local rot = transform.rot
+
+                local bladeLength = 2 * onT - 1.5
+
+                transform = Transform(VecLerp(pos, targetTransform.pos, dt * 20), QuatSlerp(rot, targetTransform.rot, dt * 20))
+
+                SetShapeLocalTransform(handleShape, shapeLocalTransform)
+                SetShapeLocalTransform(bladeShape, TransformToParentTransform(shapeLocalTransform, Transform(Vec(0.05, bladeLength, 0.05)))) 
+                SetToolTransform(transform, 1)
+
+                PointLight(VecAdd(toolPos, TransformToParentVec(toolTransform, Vec(0, 1, 0))), color[1], color[2], color[3], 4 * onT)
+                PlayLoop(humSnd, toolPos, onT)
+
+            end
+    	end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if InputDown("e") then SetPlayerHealth(playerId, 1) end
+end
+
+function client.draw()
     if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 11 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock2.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 12 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock3.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 13 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock4.png")
-		UiPop()
-	end
-     if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 14 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock5.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("q") and not InputDown("lmb") and not InputDown("rmb") then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/hand_force.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("c") and not InputDown("lmb") and not InputDown("rmb") then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/hand_force.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/hand_lightning.png")
-		UiPop()
-	end
-end+           InputDown("e") and math.random(1,20) == 10 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock1.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 11 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock2.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 12 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock3.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 13 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock4.png")
+    	UiPop()
+    end
+        if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 14 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock5.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("q") and not InputDown("lmb") and not InputDown("rmb") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/hand_force.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("c") and not InputDown("lmb") and not InputDown("rmb") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/hand_force.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/hand_lightning.png")
+    	UiPop()
+    end
+end
+

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
@@ -1,16 +1,7 @@
-if not HasKey("savegame.mod.vox") then
-    SetInt("savegame.mod.vox", 1)
-end
-if not HasKey("savegame.mod.sound") then
-    SetInt("savegame.mod.sound", 1)
-end
-
-----------------------------------------------------------------------------------------------------------
-
+#version 2
 function randomVec()
     return Vec(math.random() - 0.5, math.random() - 0.5, math.random() - 0.5)
 end
-
 
 function playRandomSound(handles, pos, volume)
     local snd = handles[math.random(#handles)]
@@ -354,7 +345,6 @@
 
 end
 
----Force Crush---
 function forcecrush()
     PlaySound(forcepush, toolPos, .6)
     local t = GetCameraTransform()
@@ -463,68 +453,232 @@
         end
     end
 end
--- Force Jump --
+
 function Boost()
-	local pt = GetPlayerTransform()
+	local pt = GetPlayerTransform(playerId)
 	local d = TransformToParentVec(pt, Vec(0, 6, 0))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	vel[2] = 0
 	vel = VecAdd(vel, d)
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
     PlaySound(forcepush, playerPos, .3)
 end
 
-function init()
-   saberVoxes = {
-        "MOD/vox/lightsword_double1.vox",
-        "MOD/vox/lightsword_double2.vox",
-        "MOD/vox/lightsword_red.vox",
-        "MOD/vox/lightsword_green.vox",
-        "MOD/vox/lightsword_blue.vox",
-        "MOD/vox/lightsword_purple.vox",
-        "MOD/vox/lightsword_yellow.vox",
-        "MOD/vox/lightsword_orange.vox",
-        "MOD/vox/lightsword_white.vox",
-        "MOD/vox/lightsword_dark.vox"
-    }
-
-    saberColors = {
-        {1, 0, 0},
-        {1, 0, 0},
-        {1, 0, 0},
-        {0, 1, 0},
-        {0, 0, 1},
-        {1, 0, 1},
-        {1, 1, 0},
-        {1, .3, 0},
-        {1, 1, 1},
-        {1, 1, 1}
-    }
-
-    saberSoundGroups = {
-        1, 2, 3, 2, 1, 2, 3, 2
-    }
-
-    voxIndex = GetInt("savegame.mod.vox")
-    vox = saberVoxes[voxIndex]
-    color = saberColors[voxIndex]
-    soundGroup = saberSoundGroups[voxIndex]
-
-    --Register tool and enable it
-    RegisterTool("sithsaber", "Sith Saber", vox)
-    SetBool("game.tool.sithsaber.enabled", true)
-    SetFloat("game.tool.sithsaber.ammo", 10000)
-
-    ready = 0
-    fireTime = 0
-
+function server.init()
+    saberVoxes = {
+         "MOD/vox/lightsword_double1.vox",
+         "MOD/vox/lightsword_double2.vox",
+         "MOD/vox/lightsword_red.vox",
+         "MOD/vox/lightsword_green.vox",
+         "MOD/vox/lightsword_blue.vox",
+         "MOD/vox/lightsword_purple.vox",
+         "MOD/vox/lightsword_yellow.vox",
+         "MOD/vox/lightsword_orange.vox",
+         "MOD/vox/lightsword_white.vox",
+         "MOD/vox/lightsword_dark.vox"
+     }
+     saberColors = {
+         {1, 0, 0},
+         {1, 0, 0},
+         {1, 0, 0},
+         {0, 1, 0},
+         {0, 0, 1},
+         {1, 0, 1},
+         {1, 1, 0},
+         {1, .3, 0},
+         {1, 1, 1},
+         {1, 1, 1}
+     }
+     saberSoundGroups = {
+         1, 2, 3, 2, 1, 2, 3, 2
+     }
+     voxIndex = GetInt("savegame.mod.vox")
+     vox = saberVoxes[voxIndex]
+     color = saberColors[voxIndex]
+     soundGroup = saberSoundGroups[voxIndex]
+     --Register tool and enable it
+     RegisterTool("sithsaber", "Sith Saber", vox)
+     SetBool("game.tool.sithsaber.enabled", true, true)
+     SetFloat("game.tool.sithsaber.ammo", 10000, true)
+     ready = 0
+     fireTime = 0
+     laserSnd = LoadLoop("MOD/snd/laser.ogg")
+     hitSnd = LoadLoop("MOD/snd/hit.ogg")
+     humSnd = LoadLoop("MOD/snd/hum01.ogg")
+     electro = LoadLoop("MOD/snd/electro.ogg")
+     crushSnds = {
+     }
+     sparkSnds = {
+     }
+     swingSnds = {
+     }
+     clashSnds = {
+     }
+     spinSnds = {
+     }
+     outSnds = {
+     }
+     inSnds = {
+     }
+     idleTransform = Transform(Vec(0.5, -0.5, -1), QuatEuler(80, 5, -5))
+     swingAnimation1 = animation()
+     addKeyframe(swingAnimation1, 0.1, Transform(Vec(-0.6, -0.2, -0.5), QuatEuler(30, 75, 0)))
+     addKeyframe(swingAnimation1, 0.2, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
+     addKeyframe(swingAnimation1, 0.3, Transform(Vec(0.8, -0.6, -0.5), QuatEuler(-30, -120, 0)))
+     swingAnimation2 = animation()
+     addKeyframe(swingAnimation2, 0.1, Transform(Vec(0.9, -0.2, -0.5), QuatEuler(45, -75, 0)))
+     addKeyframe(swingAnimation2, 0.15, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
+     addKeyframe(swingAnimation2, 0.25, Transform(Vec(-0.6, -0.6, -0.5), QuatEuler(-50, 120, 0)))
+     swingAnimation3 = animation()
+     addKeyframe(swingAnimation3, 0.1, Transform(Vec(0.2, 0.2, -0.5), QuatEuler(150, 0, -30)))
+     addKeyframe(swingAnimation3, 0.15, Transform(Vec(0, -0.5, -1), QuatEuler(10, 0, 0)))
+     addKeyframe(swingAnimation3, 0.25, Transform(Vec(-0.2, -1.5, -0.5), QuatEuler(-90, 0, -30)))
+     swingAnimations = {
+         swingAnimation1,
+         swingAnimation2,
+         swingAnimation3
+     }
+     swingDirections = {
+         Vec(1, 0, 0),
+         Vec(-1, 0, 0),
+         Vec(0, -1, 0)
+     }
+     swingAnimation = swingAnimation1
+     swingDirection = Vec()
+     transform = Transform()
+     on = true
+     swinging = false
+     clash = false
+     throwing = false
+     throwReturn = false
+     swingT = 0
+     hitT = 0
+     onT = 0
+     forceVelocity = Vec()
+     torqueVelocity = Vec()
+     throwDirection = Vec()
+     throwTarget = Vec()
+     throwTransform = Transform()
+     swordOffsetTransform = Transform(Vec(-0.1, -0.3, -0.1))
+     shapeLocalTransform = Transform(Vec(-0.15, -0.1, 0.45), Quat(-0.70711, 0, 0, 0.70711))
+     impulseBatch = {}
+     impulseApplyPos = Vec()
+     impulse = Vec()
+     theta = 0
+     cooldownTimer1 = 1
+     cooldownTimer2 = 0
+     playerTransform = Transform()
+     playerPos = Vec()
+     cameraTransform = Transform()
+     cameraDir = Vec()
+     toolBody = 0
+     toolTransform = Transform()
+     toolPos = Vec()
+     targetTransform = Transform()
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+            playerTransform = GetPlayerTransform(playerId)
+            playerPos = VecAdd(playerTransform.pos, Vec(0, 1, 0))
+            cameraTransform = GetPlayerCameraTransform(playerId)
+            cameraDir = TransformToParentVec(cameraTransform, Vec(0, 0, -1))
+        function push(pos)
+        QueryRequire("physical dynamic")
+        	local max = 8.5
+            local maxDist1 = 35
+            local maxMass1 = 500
+            local maxMass2 = 2500
+            local objectbodies = QueryAabbBodies( VecAdd(pos, Vec(-1, -1, -1)), VecAdd(pos, Vec(1, 1, 1)))
+            for i = 1, #objectbodies do
+                local objectbodies2 = objectbodies[i]
+                if IsBodyDynamic(objectbodies2) then
+                    local bb, bbba = GetBodyBounds(objectbodies2)
+                    local direction = VecSub(VecLerp(bb, bbba, 0.5), pos)
+                    local distance = VecLength(direction)
+                    local mass = GetBodyMass(objectbodies2)
+                    direction = VecScale(direction, 1 / distance)
+                    if distance < maxDist1 and IsBodyVisible(objectbodies2, max * 35) and mass > maxMass1 and mass < maxMass2 then 
+                        local distScale = 1 - math.min(distance / max, 1.0)
+                        local vel = GetBodyVelocity(objectbodies2)
+                        vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 11 * distScale))
+                        SetBodyVelocity(objectbodies2, vel)
+                    end
+                end
+            end
+        end
+        function get_bodys(pos)
+                QueryRequire("physical")
+        	local bods = QueryAabbBodies( VecAdd(pos, Vec(-3, -3, -3)), VecAdd(pos, Vec(3, 3, 3)))
+        end
+        function get_bodys1(pos)
+        	QueryRejectVehicle(vehicle)
+        	QueryRequire("physical")
+        	local bods = QueryAabbBodies( VecAdd(pos, Vec(-2, -2, -2)), VecAdd(pos, Vec(2, 2, 2)))
+        	for i=1, #bods do
+        		local body = bods[i]
+        		local com = GetBodyCenterOfMass(body)
+                        local mass = GetBodyMass(body)
+                        local voxelCount = GetShapeVoxelCount(shape)
+        		local t = TransformToParentPoint(GetBodyTransform(body), com)
+        		rv1 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
+
+        		local fwd = TransformToParentVec(com, Vec(0, 0, -1))
+        		local hit, dist, normal, shape = QueryRaycast(t, fwd, .15)
+        	end
+        end
+        function lookpos()
+          local t = GetCameraTransform()
+          local transform = TransformToParentVec(t, Vec(0, 0, -1))
+          hit, dist, normal, shape = QueryRaycast(t.pos, transform, 35)
+          if hit then
+              local pos = VecAdd(t.pos, VecScale(transform, dist))
+              return pos
+            else
+              return false
+            end
+        end
+        		-- Force Lift/Push/Pull
+            end
+        	--Check if light saber is selected
+            if throwing then
+                saberThrowUpdate(dt)
+            end
+            if on then
+                onT = math.min(onT + dt * 4, 1)
+            else
+                onT = math.max(onT - dt * 4, 0)
+            end
+            if swinging then
+                swingT = swingT + dt
+            end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if #impulseBatch ~= 0 then
+            for i, body in pairs(impulseBatch) do
+                local mass = GetBodyMass(body)
+                local bodyImpulse = VecScale(impulse, 1 / (mass + 50) * mass)
+                ApplyBodyImpulse(body, impulseApplyPos, bodyImpulse)
+            end
+            impulseBatch = {}
+        end
+        if cooldownTimer2 ~= 0 then
+            cooldownTimer1 = cooldownTimer1 - dt
+            cooldownTimer2 = cooldownTimer2 - dt
+        end
+        if cooldownTimer2 <= 0 then
+            cooldownTimer1 = 1
+        end
+    end
+end
+
+function client.init()
     openSnd = LoadSound("MOD/snd/open.ogg")
     closeSnd = LoadSound("MOD/snd/close.ogg")
     forcepush = LoadSound("MOD/snd/forcepush.ogg")
-    laserSnd = LoadLoop("MOD/snd/laser.ogg")
-    hitSnd = LoadLoop("MOD/snd/hit.ogg")
-    humSnd = LoadLoop("MOD/snd/hum01.ogg")
-    electro = LoadLoop("MOD/snd/electro.ogg")
     electro2 = LoadSound("MOD/snd/electro2.ogg")
     lightning1 = LoadSound("MOD/snd/lightning1.ogg")
     lightning2 = LoadSound("MOD/snd/lightning2.ogg")
@@ -533,16 +687,11 @@
     lightning5 = LoadSound("MOD/snd/lightning5.ogg")
     spark = LoadSound("thunder3.ogg")
     lightning = LoadSound("thunder-strike.ogg")
-    
-    crushSnds = {
         LoadSound("MOD/snd/crush1.ogg"),
         LoadSound("MOD/snd/crush2.ogg"),
         LoadSound("MOD/snd/crush3.ogg"),
         LoadSound("MOD/snd/crush4.ogg"),
         LoadSound("MOD/snd/crush5.ogg")
-    }
-
-    sparkSnds = {
         LoadSound("MOD/snd/spark0.ogg"),
         LoadSound("MOD/snd/spark1.ogg"),
         LoadSound("MOD/snd/spark2.ogg"),
@@ -550,9 +699,6 @@
         LoadSound("MOD/snd/spark4.ogg"),
         LoadSound("MOD/snd/spark5.ogg"),
         LoadSound("MOD/snd/spark6.ogg")
-    }
-
-    swingSnds = {
         LoadSound("MOD/snd/swng01.ogg"),
         LoadSound("MOD/snd/swng02.ogg"),
         LoadSound("MOD/snd/swng03.ogg"),
@@ -561,9 +707,6 @@
         LoadSound("MOD/snd/swng06.ogg"),
         LoadSound("MOD/snd/swng07.ogg"),
         LoadSound("MOD/snd/swng08.ogg")
-    }
-
-    clashSnds = {
         LoadSound("MOD/snd/clsh01.ogg"),
         LoadSound("MOD/snd/clsh02.ogg"),
         LoadSound("MOD/snd/clsh03.ogg"),
@@ -572,655 +715,471 @@
         LoadSound("MOD/snd/clsh06.ogg"),
         LoadSound("MOD/snd/clsh07.ogg"),
         LoadSound("MOD/snd/clsh08.ogg")
-    }
-
-    spinSnds = {
         LoadSound("MOD/snd/spin01.ogg"),
         LoadSound("MOD/snd/spin02.ogg")
-    }
-
-    outSnds = {
         LoadSound("MOD/snd/out04.ogg"),
         LoadSound("MOD/snd/out04.ogg")
-    }
-
-    inSnds = {
         LoadSound("MOD/snd/in04.ogg"),
         LoadSound("MOD/snd/in04.ogg")
-    }
-
-    idleTransform = Transform(Vec(0.5, -0.5, -1), QuatEuler(80, 5, -5))
-    
-    swingAnimation1 = animation()
-    addKeyframe(swingAnimation1, 0.1, Transform(Vec(-0.6, -0.2, -0.5), QuatEuler(30, 75, 0)))
-    addKeyframe(swingAnimation1, 0.2, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
-    addKeyframe(swingAnimation1, 0.3, Transform(Vec(0.8, -0.6, -0.5), QuatEuler(-30, -120, 0)))
-
-    swingAnimation2 = animation()
-    addKeyframe(swingAnimation2, 0.1, Transform(Vec(0.9, -0.2, -0.5), QuatEuler(45, -75, 0)))
-    addKeyframe(swingAnimation2, 0.15, Transform(Vec(0.2, -0.45, -1), QuatEuler(10, 0, 0)))
-    addKeyframe(swingAnimation2, 0.25, Transform(Vec(-0.6, -0.6, -0.5), QuatEuler(-50, 120, 0)))
-
-    swingAnimation3 = animation()
-    addKeyframe(swingAnimation3, 0.1, Transform(Vec(0.2, 0.2, -0.5), QuatEuler(150, 0, -30)))
-    addKeyframe(swingAnimation3, 0.15, Transform(Vec(0, -0.5, -1), QuatEuler(10, 0, 0)))
-    addKeyframe(swingAnimation3, 0.25, Transform(Vec(-0.2, -1.5, -0.5), QuatEuler(-90, 0, -30)))
-
-    swingAnimations = {
-        swingAnimation1,
-        swingAnimation2,
-        swingAnimation3
-    }
-
-    swingDirections = {
-        Vec(1, 0, 0),
-        Vec(-1, 0, 0),
-        Vec(0, -1, 0)
-    }
-
-    swingAnimation = swingAnimation1
-    swingDirection = Vec()
-
-    transform = Transform()
-
-    on = true
-    swinging = false
-    clash = false
-    throwing = false
-    throwReturn = false
-    swingT = 0
-    hitT = 0
-    onT = 0
-
-    forceVelocity = Vec()
-    torqueVelocity = Vec()
-
-    throwDirection = Vec()
-    throwTarget = Vec()
-    throwTransform = Transform()
-
-    swordOffsetTransform = Transform(Vec(-0.1, -0.3, -0.1))
-    
-    shapeLocalTransform = Transform(Vec(-0.15, -0.1, 0.45), Quat(-0.70711, 0, 0, 0.70711))
-
-    impulseBatch = {}
-    impulseApplyPos = Vec()
-    impulse = Vec()
-
-    theta = 0
-
-    cooldownTimer1 = 1
-    cooldownTimer2 = 0
-
-    playerTransform = Transform()
-    playerPos = Vec()
-    cameraTransform = Transform()
-    cameraDir = Vec()
-
-    toolBody = 0
-    toolTransform = Transform()
-    toolPos = Vec()
-
-    targetTransform = Transform()
-end
-
-
-      
-function tick(dt)
-    playerTransform = GetPlayerTransform()
-    playerPos = VecAdd(playerTransform.pos, Vec(0, 1, 0))
-    cameraTransform = GetPlayerCameraTransform()
-    cameraDir = TransformToParentVec(cameraTransform, Vec(0, 0, -1))
-    
-	if GetString("game.player.tool") == "sithsaber" and GetPlayerVehicle() == 0 then
-
-        if vox == "MOD/vox/lightsword_double1.vox" then
-            idleTransform = Transform(Vec(0.2, -1.1, -1), QuatEuler(80, 5, -45))
-            swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
-        end
-        if on == false and vox == "MOD/vox/lightsword_double1.vox" then
-            idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
-        end
-        if vox == "MOD/vox/lightsword_double2.vox" then
-            idleTransform = Transform(Vec(0.5, -.9, -1), QuatEuler(80, 5, -5))
-            swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
-        end
-        if on == false and vox == "MOD/vox/lightsword_double2.vox" then
-            idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
-        end
-        if InputDown("space") and cooldownTimer1 > 0 then
-            Boost()
-            cooldownTimer2 = 3 
-        end
-        -- Force Crush
-        if InputDown("c") then 
-            forcecrush()
-        end
-        -- Force Lightning
-        if InputDown("e") then
-            SetPlayerHealth(1)  
-            PlayLoop(electro, toolPos, 1)
-            local t = GetCameraTransform()
-		    local pos = t.pos
-		    local dir = TransformToParentVec(t, Vec(0, 0, -1))
-		    local hit, dist, normal, shape = QueryRaycast(pos, dir, 35)
-            local hitpoint = VecAdd(pos, VecScale(dir, dist))
-            local hitpoint1 = VecAdd(pos, VecScale(dir, dist-1))
-            local hitpoint2 = VecAdd(pos, VecScale(dir, dist+1.5))
-            MakeHole(hitpoint, math.random(6, 15)*0.1, math.random(3, 9)*0.1, math.random(2, 6)*0.1, "silent")
-            get_bodys(hitpoint)
-            get_bodys(hipoint2)
-            if hit and math.random(1,3) == 3 then
-                --PointLight(hitpoint, color[1], color[2], color[3], math.random(10,30)) 
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    	if GetString("game.player.tool") == "sithsaber" and GetPlayerVehicle(playerId) == 0 then
+
+            if vox == "MOD/vox/lightsword_double1.vox" then
+                idleTransform = Transform(Vec(0.2, -1.1, -1), QuatEuler(80, 5, -45))
+                swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
+            end
+            if on == false and vox == "MOD/vox/lightsword_double1.vox" then
+                idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
+            end
+            if vox == "MOD/vox/lightsword_double2.vox" then
+                idleTransform = Transform(Vec(0.5, -.9, -1), QuatEuler(80, 5, -5))
+                swordOffsetTransform = Transform(Vec(-0.1, -1.1, -0.1))
+            end
+            if on == false and vox == "MOD/vox/lightsword_double2.vox" then
+                idleTransform = Transform(Vec(0.4, -1.1, 3), QuatEuler(80, 5, -45))
+            end
+            if InputDown("space") and cooldownTimer1 ~= 0 then
+                Boost()
+                cooldownTimer2 = 3 
+            end
+            -- Force Crush
+            if InputDown("c") then 
+                forcecrush()
+            end
+            -- Force Lightning
+            if InputDown("e") then
+                SetPlayerHealth(playerId, 1)  
+                PlayLoop(electro, toolPos, 1)
+                local t = GetCameraTransform()
+    		    local pos = t.pos
+    		    local dir = TransformToParentVec(t, Vec(0, 0, -1))
+    		    local hit, dist, normal, shape = QueryRaycast(pos, dir, 35)
+                local hitpoint = VecAdd(pos, VecScale(dir, dist))
+                local hitpoint1 = VecAdd(pos, VecScale(dir, dist-1))
+                local hitpoint2 = VecAdd(pos, VecScale(dir, dist+1.5))
+                MakeHole(hitpoint, math.random(6, 15)*0.1, math.random(3, 9)*0.1, math.random(2, 6)*0.1, "silent")
+                get_bodys(hitpoint)
+                get_bodys(hipoint2)
+                if hit and math.random(1,3) == 3 then
+                    --PointLight(hitpoint, color[1], color[2], color[3], math.random(10,30)) 
+                    ParticleReset()
+                    ParticleEmissive(1, 0, "easein")
+                    ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
+                    ParticleRadius(math.random(20, 30)*.001, 0, "smooth")
+                    ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
+                    ParticleTile(4)
+                    ParticleCollide(1)
+                    ParticleSticky(1)
+                    for i = 1, math.random(32, 64) do
+                        local vel = VecScale(randomVec(), math.random(1,2))
+                        SpawnParticle(hitpoint, vel, math.random(4,6))
+                    end
+                    ParticleReset()
+                    ParticleEmissive(1, 0, "easein")
+                    ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
+                    ParticleRadius(math.random(15, 25)*.001, 0, "smooth")
+                    ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
+                    ParticleTile(4)
+                    ParticleCollide(0, 1, "easeout")
+                    ParticleSticky(1, .3)
+                    for i = 1, math.random(32, 64) do
+                        local vel = VecScale(randomVec(), math.random(3,5))
+                        SpawnParticle(hitpoint, vel, math.random(4,5))
+                    end
+                    ParticleReset()
+                    ParticleEmissive(1, 0, "easein")
+                    ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
+                    ParticleRadius(math.random(10, 20)*.001, 0, "smooth")
+                    ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
+                    ParticleTile(4)
+                    ParticleCollide(0, 1, "easeout")
+                    ParticleSticky(1, .3)
+
+                    for i = 1, math.random(32, 64) do
+                        local vel = VecScale(randomVec(), math.random(7,10))
+                        SpawnParticle(hitpoint, vel, math.random(4,6))
+                    end
+                end
+               if hit and math.random(1,20) == 11 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1)
+                end
+
+                if hit and math.random(1,20) == 13 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1) 
+                end
+
+                if hit and math.random(1,20) == 14 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1)
+            end
+
+                if hit and math.random(1,20) == 15 then 
+                    Explosion(hitpoint, math.random(5, 8)*.1) 		   
+            end
+
+              if InputPressed("e") then
+                   PlaySound(electro2, toolPos, 1)
+                end
+    end
+
+    function clearAllFires()
+        RemoveAabbFires(Vec(-10000, -10000, -10000), Vec(10000, 10000, 10000))
+    end
+    	    for i=1, #bods do
+    		local body = bods[i]
+    		local com = GetBodyCenterOfMass(body)
+    		local maxMass1 = 500
+            	local maxMass2 = 3500
+                  	local mass = GetBodyMass(body)
+                    local broken = IsBodyBroken(body)
+                    local voxelcount = GetShapeVoxelCount(shape)
+                    if mass < maxMass1 and mass < maxMass2 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then 
+    		local t = TransformToParentPoint(GetBodyTransform(body), com)
+    		rv = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
+                    rv2 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
+
+                    if math.random(1,4) == 4 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then
+                    SpawnFire(rv)
+                    QueryRejectVehicle(vehicle)               
+                    end
+
+            local fwd = TransformToParentVec(com, Vec(0, 0, -1))
+    		local hit, dist, normal, shape = QueryRaycast(t, fwd, 3)
+
+    		local e = VecAdd(t, VecScale(fwd, dist))
+
+    		local last = pos
+
+             if IsBodyActive(body, 40) and IsBodyVisible(body, 40) then	 
+    		for i=1, 14 do
+    			local t = i/10
+    			local p = VecLerp(pos, e, t)
+    			p = VecAdd(p, VecScale(VecNormalize(Vec(math.random(-3,3), math.random(-3,3), math.random(-3,3))), 0.2*t))
+                            DrawLine(last, p, 1.0, 1.0, 1.0, 1)
+    			last = p
+               	end
+    		end
+    	end
+       end
+    		if InputDown("q") and not InputDown("w") and not InputDown("s") then
+
+                PlaySound(forcepush, toolPos, .6)
+                strength = 1.3	--Strength of Force Lift
+                maxMass = 1000000	--The maximum mass for a body to be affected
+                maxDist = 35	--The maximum distance for bodies to be affected
+
+    			--Get all physical and dynamic bodies in front of camera
+    			local t = GetCameraTransform()
+    			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
+                local f = TransformToParentPoint(t, Vec(0, 0, -1))
+    			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
+    			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
+    			QueryRequire("physical dynamic")
+    			local bodies = QueryAabbBodies(mi, ma)
+
+    			--Loop through bodies and push them
+    			for i=1,#bodies do
+    				local b = bodies[i]
+
+    				--Compute body center point and distance
+    				local bmi, bma = GetBodyBounds(b)
+    				local bc = VecLerp(bmi, bma, 0.5)
+    				local dir = VecSub(bc, t.pos)
+    				local dist = VecLength(dir)
+    				dir = VecScale(dir, 1.0/dist)
+
+    				--Get body mass
+    				local mass = GetBodyMass(b)
+
+    				--Check if body is should be affected
+    				if dist < maxDist and mass < maxMass then
+    					--Make sure direction is always pointing slightly upwards
+    					--dir[2] = .5
+    					--dir = VecNormalize(dir)
+                        dir = Vec(0,.6,0)
+    					--Compute how much velocity to add
+    					local massScale = 1 - math.min(mass/maxMass, 1.0)
+    					local distScale = 1 - math.min(dist/maxDist, 1.0)
+    					local add = VecScale(dir, strength * massScale * distScale)
+
+    					--Add velocity to body
+    					local vel = GetBodyVelocity(b)
+    					vel = VecAdd(vel, add)
+    					SetBodyVelocity(b, vel)
+    				end
+    			end
+                -- Blue Force Effect
                 ParticleReset()
-                ParticleEmissive(1, 0, "easein")
-                ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
-                ParticleRadius(math.random(20, 30)*.001, 0, "smooth")
-                ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
-                ParticleTile(4)
-                ParticleCollide(1)
-                ParticleSticky(1)
-                for i = 1, math.random(32, 64) do
-                    local vel = VecScale(randomVec(), math.random(1,2))
-                    SpawnParticle(hitpoint, vel, math.random(4,6))
+                ParticleAlpha(.1, 0.05, "smooth")
+    			ParticleEmissive(1, .5, "smooth")
+    			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
+                --ParticleColor(color[1], color[2], color[3]) 
+    			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
+    			ParticleTile(14)
+    			ParticleCollide(0, 1, "smooth")
+                for i = 1, math.random(4, 8) do
+                    local vel = VecScale(randomVec(), math.random(7,10))
+                    SpawnParticle(f, vel, math.random(10,20)*.1)
                 end
+            end
+            if InputDown("q") and InputDown("w") and not InputDown("s") then
+
+                --SetPlayerVelocity(playerId, 0,0,0)
+                PlaySound(forcepush, toolPos, .6)
+                strength = 1	--Strength of Force Push
+                maxMass = 1000000	--The maximum mass for a body to be affected
+                maxDist = 35	--The maximum distance for bodies to be affected
+
+    			--Get all physical and dynamic bodies in front of camera
+    			local t = GetCameraTransform()
+    			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
+                local f = TransformToParentPoint(t, Vec(0, 0, -2.5))
+    			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
+    			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
+    			QueryRequire("physical dynamic")
+    			local bodies = QueryAabbBodies(mi, ma)
+
+    			--Loop through bodies and push them
+    			for i=1,#bodies do
+    				local b = bodies[i]
+
+    				--Compute body center point and distance
+    				local bmi, bma = GetBodyBounds(b)
+    				local bc = VecLerp(bmi, bma, 0.5)
+    				local dir = VecSub(bc, t.pos)
+    				local dist = VecLength(dir)
+    				dir = VecScale(dir, 1.0/dist)
+
+    				--Get body mass
+    				local mass = GetBodyMass(b)
+
+    				--Check if body is should be affected
+    				if dist < maxDist and mass < maxMass then
+    					--Make sure direction is always pointing slightly upwards
+    					dir[2] = 1
+    					dir = VecNormalize(dir)
+
+    					--Compute how much velocity to add
+    					local massScale = 1 - math.min(mass/maxMass, 1.0)
+    					local distScale = 1 - math.min(dist/maxDist, 1.0)
+    					local add = VecScale(dir, strength * massScale * distScale)
+
+    					--Add velocity to body
+    					local vel = GetBodyVelocity(b)
+    					vel = VecAdd(vel, add)
+    					SetBodyVelocity(b, vel)
+    				end
+    			end
+                -- Blue Force Effect
                 ParticleReset()
-                ParticleEmissive(1, 0, "easein")
-                ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
-                ParticleRadius(math.random(15, 25)*.001, 0, "smooth")
-                ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
-                ParticleTile(4)
-                ParticleCollide(0, 1, "easeout")
-                ParticleSticky(1, .3)
-                for i = 1, math.random(32, 64) do
-                    local vel = VecScale(randomVec(), math.random(3,5))
-                    SpawnParticle(hitpoint, vel, math.random(4,5))
+                ParticleAlpha(.1, 0.05, "smooth")
+    			ParticleEmissive(1, .5, "smooth")
+    			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
+                --ParticleColor(color[1], color[2], color[3])
+    			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
+    			ParticleTile(14)
+    			ParticleCollide(0, 1, "smooth")
+                for i = 1, math.random(4, 8) do
+                    local vel = VecScale(randomVec(), math.random(7,10))
+                    SpawnParticle(f, vel, math.random(10,20)*.1)
                 end
+            end
+            if InputDown("q") and InputDown("s") and not InputDown("w") then
+
+                --SetPlayerVelocity(playerId, 0,0,0)
+                PlaySound(forcepush, toolPos, .6)
+                strength = 1	--Strength of Force Pull
+                maxMass = 1000000	--The maximum mass for a body to be affected
+                maxDist = 35	--The maximum distance for bodies to be affected
+
+    			--Get all physical and dynamic bodies in front of camera
+    			local t = GetCameraTransform()
+    			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
+                local f = TransformToParentPoint(t, Vec(0, 0, 0))
+    			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
+    			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
+    			QueryRequire("physical dynamic")
+    			local bodies = QueryAabbBodies(mi, ma)
+
+    			--Loop through bodies and push them
+    			for i=1,#bodies do
+    				local b = bodies[i]
+
+    				--Compute body center point and distance
+    				local bmi, bma = GetBodyBounds(b)
+    				local bc = VecLerp(bmi, bma, 0.5)
+    				local dir = VecSub(bc, t.pos)
+    				local dist = VecLength(dir)
+    				dir = VecScale(dir, 1.0/dist)
+
+    				--Get body mass
+    				local mass = GetBodyMass(b)
+
+    				--Check if body is should be affected
+    				if dist < maxDist and mass < maxMass then
+    					--Make sure direction is always pointing slightly upwards
+    					dir[2] = -1
+    					dir = VecNormalize(dir)
+
+    					--Compute how much velocity to add
+    					local massScale = 1 - math.min(mass/maxMass, 1.0)
+    					local distScale = 1 - math.min(dist/maxDist, 1.0)
+    					local add = VecScale(dir, strength * massScale * distScale)
+
+    					--Add velocity to body
+    					local vel = GetBodyVelocity(b)
+    					vel = VecSub(vel, add)
+    					SetBodyVelocity(b, vel)
+    				end
+    			end
+                -- Blue Force Effect
                 ParticleReset()
-                ParticleEmissive(1, 0, "easein")
-                ParticleGravity(math.random(5, 8)*-1, math.random(8, 10)*-1, "smooth")
-                ParticleRadius(math.random(10, 20)*.001, 0, "smooth")
-                ParticleColor(1,math.random(75, 85)*0.01,math.random(55, 65)*0.01, 1,.4,0, "smooth")          
-                ParticleTile(4)
-                ParticleCollide(0, 1, "easeout")
-                ParticleSticky(1, .3)
-                     
-                for i = 1, math.random(32, 64) do
+                ParticleAlpha(.1, 0.05, "smooth")
+    			ParticleEmissive(1, .5, "smooth")
+    			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
+                --ParticleColor(color[1], color[2], color[3])
+    			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
+    			ParticleTile(14)
+    			ParticleCollide(0, 1, "smooth")
+                for i = 1, math.random(4, 8) do
                     local vel = VecScale(randomVec(), math.random(7,10))
-                    SpawnParticle(hitpoint, vel, math.random(4,6))
+                    SpawnParticle(f, vel, math.random(10,20)*.1)
                 end
             end
-           if hit and math.random(1,20) == 11 then 
-                Explosion(hitpoint, math.random(5, 8)*.1)
-            end
-
-            if hit and math.random(1,20) == 13 then 
-                Explosion(hitpoint, math.random(5, 8)*.1) 
-            end
-        
-            if hit and math.random(1,20) == 14 then 
-                Explosion(hitpoint, math.random(5, 8)*.1)
-        end
-         
-            if hit and math.random(1,20) == 15 then 
-                Explosion(hitpoint, math.random(5, 8)*.1) 		   
-        end
-
-          if InputPressed("e") then
-               PlaySound(electro2, toolPos, 1)
-            end
-end
-
-function clearAllFires()
-    RemoveAabbFires(Vec(-10000, -10000, -10000), Vec(10000, 10000, 10000))
-end
-
-function push(pos)
-QueryRequire("physical dynamic")
-	local max = 8.5
-    local maxDist1 = 35
-    local maxMass1 = 500
-    local maxMass2 = 2500
-    local objectbodies = QueryAabbBodies( VecAdd(pos, Vec(-1, -1, -1)), VecAdd(pos, Vec(1, 1, 1)))
-    for i = 1, #objectbodies do
-        local objectbodies2 = objectbodies[i]
-        if IsBodyDynamic(objectbodies2) then
-            local bb, bbba = GetBodyBounds(objectbodies2)
-            local direction = VecSub(VecLerp(bb, bbba, 0.5), pos)
-            local distance = VecLength(direction)
-            local mass = GetBodyMass(objectbodies2)
-            direction = VecScale(direction, 1 / distance)
-            if distance < maxDist1 and IsBodyVisible(objectbodies2, max * 35) and mass > maxMass1 and mass < maxMass2 then 
-                local distScale = 1 - math.min(distance / max, 1.0)
-                local vel = GetBodyVelocity(objectbodies2)
-                vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 11 * distScale))
-                SetBodyVelocity(objectbodies2, vel)
-            end
-        end
-    end
-end
-
-function get_bodys(pos)
-        QueryRequire("physical")
-	local bods = QueryAabbBodies( VecAdd(pos, Vec(-3, -3, -3)), VecAdd(pos, Vec(3, 3, 3)))
-	    for i=1, #bods do
-		local body = bods[i]
-		local com = GetBodyCenterOfMass(body)
-		local maxMass1 = 500
-        	local maxMass2 = 3500
-              	local mass = GetBodyMass(body)
-                local broken = IsBodyBroken(body)
-                local voxelcount = GetShapeVoxelCount(shape)
-                if mass < maxMass1 and mass < maxMass2 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then 
-		local t = TransformToParentPoint(GetBodyTransform(body), com)
-		rv = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
-                rv2 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
-                
-                if math.random(1,4) == 4 and IsBodyActive(body, 35) and IsBodyVisible(body, 35) then
-                SpawnFire(rv)
-                QueryRejectVehicle(vehicle)               
+    	if GetString("game.player.tool") == "sithsaber" then        
+            toolBody = GetToolBody()
+            toolTransform = GetBodyTransform(toolBody)
+            toolPos = toolTransform.pos
+
+            local shapes = GetBodyShapes(toolBody)
+
+            local handleShape = shapes[1]
+            local bladeShape = shapes[2]
+
+            SetTag(handleShape, "nocull", "true")
+            SetTag(bladeShape, "nocull", "true")
+
+            targetTransform = idleTransform
+
+    		--Check if tool is firing
+            if GetBool("game.player.canusetool") then
+                if InputDown("lmb") and not InputDown("rmb") then
+                    saberSwingStart()
                 end
-
-        local fwd = TransformToParentVec(com, Vec(0, 0, -1))
-		local hit, dist, normal, shape = QueryRaycast(t, fwd, 3)
-								
-		local e = VecAdd(t, VecScale(fwd, dist))
-
-		local last = pos
- 
-         if IsBodyActive(body, 40) and IsBodyVisible(body, 40) then	 
-		for i=1, 14 do
-			local t = i/10
-			local p = VecLerp(pos, e, t)
-			p = VecAdd(p, VecScale(VecNormalize(Vec(math.random(-3,3), math.random(-3,3), math.random(-3,3))), 0.2*t))
-                        DrawLine(last, p, 1.0, 1.0, 1.0, 1)
-			last = p
-           	end
-		end
-	end
-   end
-end
-
-
-function get_bodys1(pos)
-	QueryRejectVehicle(vehicle)
-	QueryRequire("physical")
-	local bods = QueryAabbBodies( VecAdd(pos, Vec(-2, -2, -2)), VecAdd(pos, Vec(2, 2, 2)))
-	for i=1, #bods do
-		local body = bods[i]
-		local com = GetBodyCenterOfMass(body)
-                local mass = GetBodyMass(body)
-                local voxelCount = GetShapeVoxelCount(shape)
-		local t = TransformToParentPoint(GetBodyTransform(body), com)
-		rv1 = VecAdd(t, Vec(math.random(-2, 2), math.random(-2, 2), math.random(-2, 2)))
-
-		local fwd = TransformToParentVec(com, Vec(0, 0, -1))
-		local hit, dist, normal, shape = QueryRaycast(t, fwd, .15)
-	end
-end
-
-function lookpos()
-  local t = GetCameraTransform()
-  local transform = TransformToParentVec(t, Vec(0, 0, -1))
-  hit, dist, normal, shape = QueryRaycast(t.pos, transform, 35)
-  if hit then
-      local pos = VecAdd(t.pos, VecScale(transform, dist))
-      return pos
-    else
-      return false
-    end
-end
-   
-		-- Force Lift/Push/Pull
-		if InputDown("q") and not InputDown("w") and not InputDown("s") then
-
-            PlaySound(forcepush, toolPos, .6)
-            strength = 1.3	--Strength of Force Lift
-            maxMass = 1000000	--The maximum mass for a body to be affected
-            maxDist = 35	--The maximum distance for bodies to be affected
-
-			--Get all physical and dynamic bodies in front of camera
-			local t = GetCameraTransform()
-			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
-            local f = TransformToParentPoint(t, Vec(0, 0, -1))
-			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
-			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
-			QueryRequire("physical dynamic")
-			local bodies = QueryAabbBodies(mi, ma)
-
-			--Loop through bodies and push them
-			for i=1,#bodies do
-				local b = bodies[i]
-
-				--Compute body center point and distance
-				local bmi, bma = GetBodyBounds(b)
-				local bc = VecLerp(bmi, bma, 0.5)
-				local dir = VecSub(bc, t.pos)
-				local dist = VecLength(dir)
-				dir = VecScale(dir, 1.0/dist)
-
-				--Get body mass
-				local mass = GetBodyMass(b)
-				
-				--Check if body is should be affected
-				if dist < maxDist and mass < maxMass then
-					--Make sure direction is always pointing slightly upwards
-					--dir[2] = .5
-					--dir = VecNormalize(dir)
-                    dir = Vec(0,.6,0)
-					--Compute how much velocity to add
-					local massScale = 1 - math.min(mass/maxMass, 1.0)
-					local distScale = 1 - math.min(dist/maxDist, 1.0)
-					local add = VecScale(dir, strength * massScale * distScale)
-					
-					--Add velocity to body
-					local vel = GetBodyVelocity(b)
-					vel = VecAdd(vel, add)
-					SetBodyVelocity(b, vel)
-				end
-			end
-            -- Blue Force Effect
-            ParticleReset()
-            ParticleAlpha(.1, 0.05, "smooth")
-			ParticleEmissive(1, .5, "smooth")
-			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
-            --ParticleColor(color[1], color[2], color[3]) 
-			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
-			ParticleTile(14)
-			ParticleCollide(0, 1, "smooth")
-            for i = 1, math.random(4, 8) do
-                local vel = VecScale(randomVec(), math.random(7,10))
-                SpawnParticle(f, vel, math.random(10,20)*.1)
-            end
-        end
-
-        if InputDown("q") and InputDown("w") and not InputDown("s") then
-
-            --SetPlayerVelocity(0,0,0)
-            PlaySound(forcepush, toolPos, .6)
-            strength = 1	--Strength of Force Push
-            maxMass = 1000000	--The maximum mass for a body to be affected
-            maxDist = 35	--The maximum distance for bodies to be affected
-
-			--Get all physical and dynamic bodies in front of camera
-			local t = GetCameraTransform()
-			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
-            local f = TransformToParentPoint(t, Vec(0, 0, -2.5))
-			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
-			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
-			QueryRequire("physical dynamic")
-			local bodies = QueryAabbBodies(mi, ma)
-
-			--Loop through bodies and push them
-			for i=1,#bodies do
-				local b = bodies[i]
-
-				--Compute body center point and distance
-				local bmi, bma = GetBodyBounds(b)
-				local bc = VecLerp(bmi, bma, 0.5)
-				local dir = VecSub(bc, t.pos)
-				local dist = VecLength(dir)
-				dir = VecScale(dir, 1.0/dist)
-
-				--Get body mass
-				local mass = GetBodyMass(b)
-				
-				--Check if body is should be affected
-				if dist < maxDist and mass < maxMass then
-					--Make sure direction is always pointing slightly upwards
-					dir[2] = 1
-					dir = VecNormalize(dir)
-			
-					--Compute how much velocity to add
-					local massScale = 1 - math.min(mass/maxMass, 1.0)
-					local distScale = 1 - math.min(dist/maxDist, 1.0)
-					local add = VecScale(dir, strength * massScale * distScale)
-					
-					--Add velocity to body
-					local vel = GetBodyVelocity(b)
-					vel = VecAdd(vel, add)
-					SetBodyVelocity(b, vel)
-				end
-			end
-            -- Blue Force Effect
-            ParticleReset()
-            ParticleAlpha(.1, 0.05, "smooth")
-			ParticleEmissive(1, .5, "smooth")
-			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
-            --ParticleColor(color[1], color[2], color[3])
-			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
-			ParticleTile(14)
-			ParticleCollide(0, 1, "smooth")
-            for i = 1, math.random(4, 8) do
-                local vel = VecScale(randomVec(), math.random(7,10))
-                SpawnParticle(f, vel, math.random(10,20)*.1)
-            end
-        end
-
-        if InputDown("q") and InputDown("s") and not InputDown("w") then
-
-            --SetPlayerVelocity(0,0,0)
-            PlaySound(forcepush, toolPos, .6)
-            strength = 1	--Strength of Force Pull
-            maxMass = 1000000	--The maximum mass for a body to be affected
-            maxDist = 35	--The maximum distance for bodies to be affected
-
-			--Get all physical and dynamic bodies in front of camera
-			local t = GetCameraTransform()
-			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/1.9))
-            local f = TransformToParentPoint(t, Vec(0, 0, 0))
-			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
-			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
-			QueryRequire("physical dynamic")
-			local bodies = QueryAabbBodies(mi, ma)
-
-			--Loop through bodies and push them
-			for i=1,#bodies do
-				local b = bodies[i]
-
-				--Compute body center point and distance
-				local bmi, bma = GetBodyBounds(b)
-				local bc = VecLerp(bmi, bma, 0.5)
-				local dir = VecSub(bc, t.pos)
-				local dist = VecLength(dir)
-				dir = VecScale(dir, 1.0/dist)
-
-				--Get body mass
-				local mass = GetBodyMass(b)
-				
-				--Check if body is should be affected
-				if dist < maxDist and mass < maxMass then
-					--Make sure direction is always pointing slightly upwards
-					dir[2] = -1
-					dir = VecNormalize(dir)
-			
-					--Compute how much velocity to add
-					local massScale = 1 - math.min(mass/maxMass, 1.0)
-					local distScale = 1 - math.min(dist/maxDist, 1.0)
-					local add = VecScale(dir, strength * massScale * distScale)
-					
-					--Add velocity to body
-					local vel = GetBodyVelocity(b)
-					vel = VecSub(vel, add)
-					SetBodyVelocity(b, vel)
-				end
-			end
-            -- Blue Force Effect
-            ParticleReset()
-            ParticleAlpha(.1, 0.05, "smooth")
-			ParticleEmissive(1, .5, "smooth")
-			ParticleRadius(math.random(10, 20)*.1, 0, "smooth")
-            --ParticleColor(color[1], color[2], color[3])
-			ParticleColor(0,0,math.random(80, 100)*0.01, 0,0,math.random(70, 90)*0.01, "smooth")          
-			ParticleTile(14)
-			ParticleCollide(0, 1, "smooth")
-            for i = 1, math.random(4, 8) do
-                local vel = VecScale(randomVec(), math.random(7,10))
-                SpawnParticle(f, vel, math.random(10,20)*.1)
-            end
-        end
-    end
-
-	--Check if light saber is selected
-	if GetString("game.player.tool") == "sithsaber" then        
-        toolBody = GetToolBody()
-        toolTransform = GetBodyTransform(toolBody)
-        toolPos = toolTransform.pos
-
-        local shapes = GetBodyShapes(toolBody)
-          
-        local handleShape = shapes[1]
-        local bladeShape = shapes[2]
-
-        SetTag(handleShape, "nocull", "true")
-        SetTag(bladeShape, "nocull", "true")
-
-        targetTransform = idleTransform
-        
-		--Check if tool is firing
-        if GetBool("game.player.canusetool") then
-            if InputDown("lmb") and not InputDown("rmb") then
-                saberSwingStart()
-            end
-            if InputDown("rmb") and not InputDown("lmb") then
-                saberThrowStart()
-            end
-            if not swinging and not throwing and InputPressed("z") then
-                if on then
-                    saberOff()
-                    clearAllFires()
-                else
-                    saberOn()
+                if InputDown("rmb") and not InputDown("lmb") then
+                    saberThrowStart()
                 end
-            end
-            if swinging then
-                saberSwingUpdate(dt)
-            end
-		end
-
-        if throwing then
-            local rotationTransform = TransformToParentTransform(throwTransform, Transform(Vec(), QuatEuler(-90, GetTime() * 1200, 0)))
-            rotationTransform.rot = QuatRotateQuat(QuatAxisAngle(throwDirection, -theta), rotationTransform.rot)
-            local swordThrowTransform = TransformToParentTransform(rotationTransform, swordOffsetTransform)
-            local localTransform = TransformToLocalTransform(toolTransform, swordThrowTransform)
-
-            SetShapeLocalTransform(handleShape, localTransform)
-            SetShapeLocalTransform(bladeShape, TransformToParentTransform(localTransform, Transform(Vec(0.05, 0.5, 0.05))))
-        else
-            local pos = transform.pos
-            local rot = transform.rot
-
-            local bladeLength = 2 * onT - 1.5
-
-            transform = Transform(VecLerp(pos, targetTransform.pos, dt * 20), QuatSlerp(rot, targetTransform.rot, dt * 20))
-            
-            SetShapeLocalTransform(handleShape, shapeLocalTransform)
-            SetShapeLocalTransform(bladeShape, TransformToParentTransform(shapeLocalTransform, Transform(Vec(0.05, bladeLength, 0.05)))) 
-            SetToolTransform(transform, 1)
-
-            PointLight(VecAdd(toolPos, TransformToParentVec(toolTransform, Vec(0, 1, 0))), color[1], color[2], color[3], 4 * onT)
-            PlayLoop(humSnd, toolPos, onT)
-
-        end
-	end
-
-    if throwing then
-        saberThrowUpdate(dt)
-    end
-
-    if on then
-        onT = math.min(onT + dt * 4, 1)
-    else
-        onT = math.max(onT - dt * 4, 0)
-    end
-
-    if swinging then
-        swingT = swingT + dt
-    end
-end
-
-function update(dt)
-    if #impulseBatch > 0 then
-        for i, body in pairs(impulseBatch) do
-            local mass = GetBodyMass(body)
-            local bodyImpulse = VecScale(impulse, 1 / (mass + 50) * mass)
-            ApplyBodyImpulse(body, impulseApplyPos, bodyImpulse)
-        end
-        impulseBatch = {}
-    end
-    if cooldownTimer2 > 0 then
-        cooldownTimer1 = cooldownTimer1 - dt
-        cooldownTimer2 = cooldownTimer2 - dt
-    end
-    if cooldownTimer2 <= 0 then
-        cooldownTimer1 = 1
-    end
-    if InputDown("e") then SetPlayerHealth(1) end
-end
-
-function draw() -- Force Lightning Effects and Hands
-	if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 10 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock1.png")
-		UiPop()
-	end
+                if not swinging and not throwing and InputPressed("z") then
+                    if on then
+                        saberOff()
+                        clearAllFires()
+                    else
+                        saberOn()
+                    end
+                end
+                if swinging then
+                    saberSwingUpdate(dt)
+                end
+    		end
+
+            if throwing then
+                local rotationTransform = TransformToParentTransform(throwTransform, Transform(Vec(), QuatEuler(-90, GetTime() * 1200, 0)))
+                rotationTransform.rot = QuatRotateQuat(QuatAxisAngle(throwDirection, -theta), rotationTransform.rot)
+                local swordThrowTransform = TransformToParentTransform(rotationTransform, swordOffsetTransform)
+                local localTransform = TransformToLocalTransform(toolTransform, swordThrowTransform)
+
+                SetShapeLocalTransform(handleShape, localTransform)
+                SetShapeLocalTransform(bladeShape, TransformToParentTransform(localTransform, Transform(Vec(0.05, 0.5, 0.05))))
+            else
+                local pos = transform.pos
+                local rot = transform.rot
+
+                local bladeLength = 2 * onT - 1.5
+
+                transform = Transform(VecLerp(pos, targetTransform.pos, dt * 20), QuatSlerp(rot, targetTransform.rot, dt * 20))
+
+                SetShapeLocalTransform(handleShape, shapeLocalTransform)
+                SetShapeLocalTransform(bladeShape, TransformToParentTransform(shapeLocalTransform, Transform(Vec(0.05, bladeLength, 0.05)))) 
+                SetToolTransform(transform, 1)
+
+                PointLight(VecAdd(toolPos, TransformToParentVec(toolTransform, Vec(0, 1, 0))), color[1], color[2], color[3], 4 * onT)
+                PlayLoop(humSnd, toolPos, onT)
+
+            end
+    	end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if InputDown("e") then SetPlayerHealth(playerId, 1) end
+end
+
+function client.draw()
     if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 11 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock2.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 12 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock3.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 13 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock4.png")
-		UiPop()
-	end
-     if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") and math.random(1,20) == 14 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/shock5.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("q") and not InputDown("lmb") and not InputDown("rmb") then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/hand_force.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("c") and not InputDown("lmb") and not InputDown("rmb") then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/hand_force.png")
-		UiPop()
-	end
-    if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
-        InputDown("e") then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle") 
-			UiImage("img/hand_lightning.png")
-		UiPop()
-	end
-end+           InputDown("e") and math.random(1,20) == 10 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock1.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 11 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock2.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 12 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock3.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 13 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock4.png")
+    	UiPop()
+    end
+        if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") and math.random(1,20) == 14 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/shock5.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("q") and not InputDown("lmb") and not InputDown("rmb") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/hand_force.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("c") and not InputDown("lmb") and not InputDown("rmb") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/hand_force.png")
+    	UiPop()
+    end
+       if GetString("game.player.tool") == "sithsaber" and GetBool("game.player.canusetool") and 
+           InputDown("e") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle") 
+    		UiImage("img/hand_lightning.png")
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/options.lua
+++ patched/options.lua
@@ -1,9 +1,16 @@
-if not HasKey("savegame.mod.vox") then
-    SetInt("savegame.mod.vox", 1)
-end
-if not HasKey("savegame.mod.sound") then
-    SetInt("savegame.mod.sound", 1)
-end
+#version 2
+local saberVoxNames = {
+    "Double-/",
+	"Double-|",
+    "Red",
+    "Green",
+    "Blue",
+    "Purple",
+    "Yellow",
+    "Orange",
+    "White",
+	"Dark",
+}
 
 function round(x, d)
 	d = d or 1
@@ -23,80 +30,58 @@
     return lerp(oMin, oMax, t)
 end
 
+function client.draw()
+    local mouseX, mouseY = UiGetMousePos()
+    UiPush()
+    	UiTranslate(UiCenter(), 100)
+    	UiAlign("center middle")
 
-local saberVoxNames = {
-    "Double-/",
-	"Double-|",
-    "Red",
-    "Green",
-    "Blue",
-    "Purple",
-    "Yellow",
-    "Orange",
-    "White",
-	"Dark",
-}
+    	--Title
+    	UiFont("bold.ttf", 48)
+    	UiText("Lightsaber options")
 
+    	--Draw image
+    	UiTranslate(0, 250)
+    	UiPush()
+    		UiImage("MOD/img/saber.png")
+    	UiPop()
 
+    	--Draw buttons
+    	UiFont("regular.ttf", 26)
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
 
-function draw()
-	local mouseX, mouseY = UiGetMousePos()
-	UiPush()
-		UiTranslate(UiCenter(), 100)
-		UiAlign("center middle")
+           UiTranslate(0, 250)
 
-		--Title
-		UiFont("bold.ttf", 48)
-		UiText("Lightsaber options")
+    	--Saber color
+    	UiTranslate(0, 40)
+    	UiPush()
+    		UiPush()
+    			UiTranslate(-20, 0)
+    			UiAlign("right middle")
+    			UiText("Lightsaber color")
+    		UiPop()
+    		UiPush()
+    			UiTranslate(20, 0)
+    			UiAlign("left middle")
+    			UiColor(1, 1, 0.5)
+    			UiButtonImageBox()
 
-		--Draw image
-		UiTranslate(0, 250)
-		UiPush()
-			UiImage("MOD/img/saber.png")
-		UiPop()
-		
-		--Draw buttons
-		UiFont("regular.ttf", 26)
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    			local vox = GetInt("savegame.mod.vox")
+                   local name = saberVoxNames[vox]
+    			if UiTextButton(name) then
+                       vox = vox + 1
+                       if vox > 10 then
+                           vox = 1
+                       end
+    				SetInt("savegame.mod.vox", vox, true)
+    			end
+    		UiPop()
+    	UiPop()
 
-        UiTranslate(0, 250)
-
-		
-
-		--Saber color
-		UiTranslate(0, 40)
-		UiPush()
-			UiPush()
-				UiTranslate(-20, 0)
-				UiAlign("right middle")
-				UiText("Lightsaber color")
-			UiPop()
-			UiPush()
-				UiTranslate(20, 0)
-				UiAlign("left middle")
-				UiColor(1, 1, 0.5)
-				UiButtonImageBox()
-
-				local vox = GetInt("savegame.mod.vox")
-                local name = saberVoxNames[vox]
-				if UiTextButton(name) then
-                    vox = vox + 1
-                    if vox > 10 then
-                        vox = 1
-                    end
-					SetInt("savegame.mod.vox", vox)
-				end
-			UiPop()
-		UiPop()
-        
-        
-
-        UiTranslate(0, 80)
-		if UiTextButton("Close", 200, 40) then
-			Menu()
-		end
-	UiPop()
-
-    
+           UiTranslate(0, 80)
+    	if UiTextButton("Close", 200, 40) then
+    		Menu()
+    	end
+    UiPop()
 end
 

```
