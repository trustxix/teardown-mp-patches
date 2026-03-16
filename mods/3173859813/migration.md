# Migration Report: main before third person.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main before third person.lua
+++ patched/main before third person.lua
@@ -1,28 +1,4 @@
---Laser Gun example mod
-
-muzzleflash = LoadSprite("MOD/img/glare1.png")
-
-muzzleflash3 = LoadSprite("gfx/glare.png")
-
-function init()
-	--Register tool and enable it
-	RegisterTool("lightningun", "Lightning Gun", "MOD/vox/lightningun.vox")
-	SetBool("game.tool.lightningun.enabled", true)
-	
-	ready = 0
-	fireTime = 0
-	
-	dtOld = 0
-	oldTransform = Transform() 
-	
-	openSnd = LoadSound("MOD/snd/open.ogg")
-	closeSnd = LoadSound("MOD/snd/close.ogg")
-	laserSnd = LoadLoop("MOD/snd/laser.ogg")
-	hitSnd = LoadLoop("MOD/snd/hit.ogg")
-end
-
---Return a random vector of desired length
-
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -34,7 +10,7 @@
 
 function randomVec(t)
 	return Vec(random(-t, t), random(-t, t), random(-t, t))
-end 
+end
 
 function clearAllFires()
     RemoveAabbFires(Vec(-10000, -10000, -10000), Vec(10000, 10000, 10000))
@@ -50,7 +26,6 @@
 function Random()
     return math.random(0, 1000) / 1000
 end
-
 
 function randPointInSphere(position, innerRadius, outerRadius)
   local r = math.random() * (outerRadius - innerRadius) + innerRadius
@@ -60,150 +35,6 @@
   local y = r * math.sin(theta) * math.sin(phi)
   local z = r * math.cos(theta)
   return VecAdd(position, Vec(x, y, z))
-end
-
-function tick(dt)
-	--Check if laser gun is selected
-	if GetString("game.player.tool") == "lightningun" then
-
-if InputPressed("grab") then
-clearAllFires()
-end
-
-		--Check if tool is firing
-		if GetBool("game.player.canusetool") and InputDown("usetool") then
-			if ready == 0 then 
-				PlaySound(openSnd) 
-			end
-			ready = math.min(1.0, ready + dt*4)
-			if ready == 1.0 then
-			--if fireTime > 0.1 and fireTime < 0.12 then
-				PlayLoop(laserSnd)
-				local t = GetCameraTransform()
-				local fwd = TransformToParentVec(t, Vec(math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), -1))
-				local maxDist = 40
-				local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist, .15)
-				local raycast_shape_breakable = not HasTag(raycast_shape, "unbreakable")
-				if not hit or not raycast_shape_breakable then
-					dist = maxDist
-				end
-				
-				
-				
---Laser line start and end points
-
-local playerTransform = GetPlayerCameraTransform()
-local ct = GetCameraTransform()
-local origin = TransformToParentPoint(ct, Vec(0.35, -0.35, 1))
-local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
-
-local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
-deltaTransform.rot = QuatSlerp(Quat(0,0,0,1), deltaTransform.rot, dt / dtOld * 0.1)
-local predictedPlayerTransform = TransformToParentTransform(playerTransform, deltaTransform)
-
-local gunpos = VecAdd(QuatRotateVec(predictedPlayerTransform.rot, Vec(0.35, -0.35, 1)), VecAdd(GetCameraTransform().pos, VecScale(GetPlayerVelocity(), GetTimeStep()*1)))
-
-dtOld = dt
-oldTransform = GetPlayerCameraTransform()
-
-local s = VecAdd(VecAdd(gunpos, Vec(0, 0, 0)), VecScale(fwd, 1.5))
-local e = VecAdd(gunpos, VecScale(fwd, dist))
---Draw laser line in ten segments with random offset
-local last = s
-local particleSize = math.random(10, 125)/1500
-local particleStepAdjustment = 2.5
-for i=1, 10 do
-    local t = i/10
-    --DebugPrint(t)
-    local p = VecLerp(s, e, t)
-    local offset_length = 1 / (t + 2.5)
-    p = VecAdd(p, rndVec(offset_length))
-    local dir = VecNormalize(VecSub(p, last))
-    local distance = VecLength(VecSub(p, last))
-    local stepDistance = particleSize*particleStepAdjustment--distance/500
-    for x=0, distance/stepDistance do
-      local newDistance = stepDistance * x
-      local newStartingPoint = VecAdd(last, VecScale(dir, newDistance))
-      --howManyParticles = howManyParticles + 1
-	local spriteDistance = VecLength(VecSub(newStartingPoint, s))
-	local size = (0.085 + 0.45 * (1 / (spriteDistance + 1))) * (math.random() + 0.5)
-	DrawSprite(muzzleflash,{pos=newStartingPoint,rot=QuatRotateQuat(GetPlayerCameraTransform().rot, QuatEuler(0, 0, math.random() * 360))},size,size, 1,1,1,1,1,1,0.1,false,true)
-	end	
-    ---DrawLine(last, p, 1, 0.5, 0.7)
-    last = p
-end
-
-				--Make damage and spawn particles
-				if hit then
-					---PlayLoop(hitSnd)
-					
-					Paint(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2),math.random(-2,2))), 1.07, "explosion")	
-
-
-if math.random(1,2) <= 2 then
-get_bodys(e)
-
-MakeHole(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2), math.random(-2,2))), math.random(1, 3000)/1000, math.random(1, 2750)/1000, math.random(1, 2500)/1000, true)
-end
-
-clearDebris(125, 450, e, 3, true, 1, false)
-
-
-				end
-				--end
-				fireTime = fireTime + dt
-				if fireTime > 0.2 then
-				fireTime = 0
-				end
-			end
-		else
-			fireTime = 0
-			if ready == 1 then
-				PlaySound(closeSnd)
-			end
-			ready = math.max(0.0, ready - dt*4)
-		end
-	--DebugPrint(fireTime)
-		local b = GetToolBody()
-		if b ~= 0 then
-			local shapes = GetBodyShapes(b)
-
-			--Control emissiveness
-			for i=1, #shapes do
-				SetShapeEmissiveScale(shapes[i], ready)
-			end
-	
-			--Add some light
-			if ready > 0 then
-				local p = TransformToParentPoint(GetBodyTransform(body), Vec(0, 0, -2))
-				PointLight(p, 1, 1, 1, ready * math.random(10, 15) / 20)
-			end
-								
-			--Move tool
-			local offset = VecScale(rndVec(0.1), ready*math.min(fireTime/5, 1.0))
-			SetToolTransform(Transform(offset))
-			
-			--Animate 
-			local t	= 1-ready
-			t = t*t
-			local offset = t*0.15
-			
-			if b ~= body then
-				body = b
-				--Get default transforms
-				t0 = GetShapeLocalTransform(shapes[2])
-				t1 = GetShapeLocalTransform(shapes[3])
-			end
-
-			t = TransformCopy(t0)
-			t.pos = VecAdd(t.pos, Vec(offset))
-			SetShapeLocalTransform(shapes[2], t)
-
-			t = TransformCopy(t1)
-			t.pos = VecAdd(t.pos, Vec(-offset))
-			SetShapeLocalTransform(shapes[3], t)
-		end
-	end
 end
 
 function clearDebris(minSize, maxSize, location, clearDistance, clearOnlyBroken, clearPercent, clearFire)
@@ -252,7 +83,6 @@
     SpawnParticle(origin, velocity, (0.25 + 4 * math.random() ^ 3) * strength)
 end
 
-
 function get_bodys(pos)
         QueryRequire("physical dynamic")
 	local bods = QueryAabbBodies( VecAdd(pos, Vec(-3, -3, -3)), VecAdd(pos, Vec(3, 3, 3)))
@@ -322,10 +152,165 @@
 	end
 
     if hit then 
-        SetFloat('level.destructible-bot.hitCounter',hitcounter)
-        SetInt('level.destructible-bot.hitShape',shape)
-        SetString('level.destructible-bot.weapon',"weapon-name")
-        SetFloat('level.destructible-bot.damage',damage)
+        SetFloat('level.destructible-bot.hitCounter',hitcounter, true)
+        SetInt('level.destructible-bot.hitShape',shape, true)
+        SetString('level.destructible-bot.weapon',"weapon-name", true)
+        SetFloat('level.destructible-bot.damage',damage, true)
     end 
 end
 
+function server.init()
+    RegisterTool("lightningun", "Lightning Gun", "MOD/vox/lightningun.vox")
+    SetBool("game.tool.lightningun.enabled", true, true)
+    ready = 0
+    fireTime = 0
+    dtOld = 0
+    oldTransform = Transform() 
+    laserSnd = LoadLoop("MOD/snd/laser.ogg")
+    hitSnd = LoadLoop("MOD/snd/hit.ogg")
+end
+
+function client.init()
+    openSnd = LoadSound("MOD/snd/open.ogg")
+    closeSnd = LoadSound("MOD/snd/close.ogg")
+end
+
+function client.tick(dt)
+    	if GetString("game.player.tool") == "lightningun" then
+
+    if InputPressed("grab") then
+    clearAllFires()
+    end
+
+    		--Check if tool is firing
+    		if GetBool("game.player.canusetool") and InputDown("usetool") then
+    			if ready == 0 then 
+    				PlaySound(openSnd) 
+    			end
+    			ready = math.min(1.0, ready + dt*4)
+    			if ready == 1.0 then
+    			--if fireTime > 0.1 and fireTime < 0.12 then
+    				PlayLoop(laserSnd)
+    				local t = GetCameraTransform()
+    				local fwd = TransformToParentVec(t, Vec(math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), -1))
+    				local maxDist = 40
+    				local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist, .15)
+    				local raycast_shape_breakable = not HasTag(raycast_shape, "unbreakable")
+    				if not hit or not raycast_shape_breakable then
+    					dist = maxDist
+    				end
+
+    --Laser line start and end points
+
+    local playerTransform = GetPlayerCameraTransform(playerId)
+    local ct = GetCameraTransform()
+    local origin = TransformToParentPoint(ct, Vec(0.35, -0.35, 1))
+    local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
+
+    local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
+    deltaTransform.rot = QuatSlerp(Quat(0,0,0,1), deltaTransform.rot, dt / dtOld * 0.1)
+    local predictedPlayerTransform = TransformToParentTransform(playerTransform, deltaTransform)
+
+    local gunpos = VecAdd(QuatRotateVec(predictedPlayerTransform.rot, Vec(0.35, -0.35, 1)), VecAdd(GetCameraTransform().pos, VecScale(GetPlayerVelocity(playerId), GetTimeStep()*1)))
+
+    dtOld = dt
+    oldTransform = GetPlayerCameraTransform(playerId)
+
+    local s = VecAdd(VecAdd(gunpos, Vec(0, 0, 0)), VecScale(fwd, 1.5))
+    local e = VecAdd(gunpos, VecScale(fwd, dist))
+    --Draw laser line in ten segments with random offset
+    local last = s
+    local particleSize = math.random(10, 125)/1500
+    local particleStepAdjustment = 2.5
+    for i=1, 10 do
+        local t = i/10
+        --DebugPrint(t)
+        local p = VecLerp(s, e, t)
+        local offset_length = 1 / (t + 2.5)
+        p = VecAdd(p, rndVec(offset_length))
+        local dir = VecNormalize(VecSub(p, last))
+        local distance = VecLength(VecSub(p, last))
+        local stepDistance = particleSize*particleStepAdjustment--distance/500
+        for x=0, distance/stepDistance do
+          local newDistance = stepDistance * x
+          local newStartingPoint = VecAdd(last, VecScale(dir, newDistance))
+          --howManyParticles = howManyParticles + 1
+    	local spriteDistance = VecLength(VecSub(newStartingPoint, s))
+    	local size = (0.085 + 0.45 * (1 / (spriteDistance + 1))) * (math.random() + 0.5)
+    	DrawSprite(muzzleflash,{pos=newStartingPoint,rot=QuatRotateQuat(GetPlayerCameraTransform(playerId).rot, QuatEuler(0, 0, math.random() * 360))},size,size, 1,1,1,1,1,1,0.1,false,true)
+    	end	
+        ---DrawLine(last, p, 1, 0.5, 0.7)
+        last = p
+    end
+
+    				--Make damage and spawn particles
+    				if hit then
+    					---PlayLoop(hitSnd)
+
+    					Paint(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2),math.random(-2,2))), 1.07, "explosion")	
+
+    if math.random(1,2) <= 2 then
+    get_bodys(e)
+
+    MakeHole(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2), math.random(-2,2))), math.random(1, 3000)/1000, math.random(1, 2750)/1000, math.random(1, 2500)/1000, true)
+    end
+
+    clearDebris(125, 450, e, 3, true, 1, false)
+
+    				end
+    				--end
+    				fireTime = fireTime + dt
+    				if fireTime > 0.2 then
+    				fireTime = 0
+    				end
+    			end
+    		else
+    			fireTime = 0
+    			if ready == 1 then
+    				PlaySound(closeSnd)
+    			end
+    			ready = math.max(0.0, ready - dt*4)
+    		end
+    	--DebugPrint(fireTime)
+    		local b = GetToolBody()
+    		if b ~= 0 then
+    			local shapes = GetBodyShapes(b)
+
+    			--Control emissiveness
+    			for i=1, #shapes do
+    				SetShapeEmissiveScale(shapes[i], ready)
+    			end
+
+    			--Add some light
+    			if ready ~= 0 then
+    				local p = TransformToParentPoint(GetBodyTransform(body), Vec(0, 0, -2))
+    				PointLight(p, 1, 1, 1, ready * math.random(10, 15) / 20)
+    			end
+
+    			--Move tool
+    			local offset = VecScale(rndVec(0.1), ready*math.min(fireTime/5, 1.0))
+    			SetToolTransform(Transform(offset))
+
+    			--Animate 
+    			local t	= 1-ready
+    			t = t*t
+    			local offset = t*0.15
+
+    			if b ~= body then
+    				body = b
+    				--Get default transforms
+    				t0 = GetShapeLocalTransform(shapes[2])
+    				t1 = GetShapeLocalTransform(shapes[3])
+    			end
+
+    			t = TransformCopy(t0)
+    			t.pos = VecAdd(t.pos, Vec(offset))
+    			SetShapeLocalTransform(shapes[2], t)
+
+    			t = TransformCopy(t1)
+    			t.pos = VecAdd(t.pos, Vec(-offset))
+    			SetShapeLocalTransform(shapes[3], t)
+    		end
+    	end
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
@@ -1,28 +1,4 @@
---Laser Gun example mod
-
-muzzleflash = LoadSprite("MOD/img/glare1.png")
-
-muzzleflash3 = LoadSprite("gfx/glare.png")
-
-function init()
-	--Register tool and enable it
-	RegisterTool("lightningun", "Lightning Gun", "MOD/vox/lightningun.vox")
-	SetBool("game.tool.lightningun.enabled", true)
-	
-	ready = 0
-	fireTime = 0
-	
-	dtOld = 0
-	oldTransform = Transform() 
-	
-	openSnd = LoadSound("MOD/snd/open.ogg")
-	closeSnd = LoadSound("MOD/snd/close.ogg")
-	laserSnd = LoadLoop("MOD/snd/laser.ogg")
-	hitSnd = LoadLoop("MOD/snd/hit.ogg")
-end
-
---Return a random vector of desired length
-
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -34,7 +10,7 @@
 
 function randomVec(t)
 	return Vec(random(-t, t), random(-t, t), random(-t, t))
-end 
+end
 
 function clearAllFires()
     RemoveAabbFires(Vec(-10000, -10000, -10000), Vec(10000, 10000, 10000))
@@ -50,7 +26,6 @@
 function Random()
     return math.random(0, 1000) / 1000
 end
-
 
 function randPointInSphere(position, innerRadius, outerRadius)
   local r = math.random() * (outerRadius - innerRadius) + innerRadius
@@ -60,155 +35,6 @@
   local y = r * math.sin(theta) * math.sin(phi)
   local z = r * math.cos(theta)
   return VecAdd(position, Vec(x, y, z))
-end
-
-function tick(dt)
-	--Check if laser gun is selected
-	if GetString("game.player.tool") == "lightningun" then
-
-if InputPressed("grab") then
-clearAllFires()
-end
-
-		--Check if tool is firing
-		if GetBool("game.player.canusetool") and InputDown("usetool") then
-			if ready == 0 then 
-				PlaySound(openSnd) 
-			end
-			ready = math.min(1.0, ready + dt*4)
-			if ready == 1.0 then
-			--if fireTime > 0.1 and fireTime < 0.12 then
-				PlayLoop(laserSnd)
-				local t = GetCameraTransform()
-				local fwd = TransformToParentVec(t, Vec(math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), -1))
-				local maxDist = 40
-				local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist, .15)
-				local raycast_shape_breakable = not HasTag(raycast_shape, "unbreakable")
-				if not hit or not raycast_shape_breakable then
-					dist = maxDist
-				end
-				
-				
-				
---Laser line start and end points
-
-local playerTransform = GetPlayerCameraTransform()
-local ct = GetCameraTransform()
-local origin = TransformToParentPoint(ct, Vec(0.35, -0.35, 1))
-local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
-
-local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
-deltaTransform.rot = QuatSlerp(Quat(0,0,0,1), deltaTransform.rot, dt / dtOld * 0.1)
-local predictedPlayerTransform = TransformToParentTransform(playerTransform, deltaTransform)
-
-if GetBool("game.thirdperson") then
-gunpos = TransformToParentPoint(GetCameraTransform(), Vec(0.01, -0.35, -3))
-else
-gunpos = VecAdd(QuatRotateVec(predictedPlayerTransform.rot, Vec(0.35, -0.35, 1)), VecAdd(GetCameraTransform().pos, VecScale(GetPlayerVelocity(), GetTimeStep()*1)))
-end
-
-dtOld = dt
-oldTransform = GetPlayerCameraTransform()
-
-local s = VecAdd(VecAdd(gunpos, Vec(0, 0, 0)), VecScale(fwd, 1.5))
-local e = VecAdd(gunpos, VecScale(fwd, dist))
---Draw laser line in ten segments with random offset
-local last = s
-local particleSize = math.random(10, 125)/1500
-local particleStepAdjustment = 2.5
-for i=1, 10 do
-    local t = i/10
-    --DebugPrint(t)
-    local p = VecLerp(s, e, t)
-    local offset_length = 1 / (t + 2.5)
-    p = VecAdd(p, rndVec(offset_length))
-    local dir = VecNormalize(VecSub(p, last))
-    local distance = VecLength(VecSub(p, last))
-    local stepDistance = particleSize*particleStepAdjustment--distance/500
-    for x=0, distance/stepDistance do
-      local newDistance = stepDistance * x
-      local newStartingPoint = VecAdd(last, VecScale(dir, newDistance))
-      --howManyParticles = howManyParticles + 1
-	local spriteDistance = VecLength(VecSub(newStartingPoint, s))
-	local size = (0.085 + 0.45 * (1 / (spriteDistance + 1))) * (math.random() + 0.5)
-	DrawSprite(muzzleflash,{pos=newStartingPoint,rot=QuatRotateQuat(GetPlayerCameraTransform().rot, QuatEuler(0, 0, math.random() * 360))},size,size, 1,1,1,1,1,1,0.1,false,true)
-	end	
-    ---DrawLine(last, p, 1, 0.5, 0.7)
-    last = p
-end
-
-				--Make damage and spawn particles
-				if hit then
-					---PlayLoop(hitSnd)
-					
-					Paint(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2),math.random(-2,2))), 1.07, "explosion")	
-
-
-if math.random(1,2) <= 2 then
-get_bodys(e)
-
-MakeHole(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2), math.random(-2,2))), math.random(1, 3000)/1000, math.random(1, 2750)/1000, math.random(1, 2500)/1000, true)
-end
-
-clearDebris(125, 450, e, 3, true, 1, false)
-
-
-				end
-				--end
-				fireTime = fireTime + dt
-				if fireTime > 0.2 then
-				fireTime = 0
-				end
-			end
-		else
-			fireTime = 0
-			if ready == 1 then
-				PlaySound(closeSnd)
-			end
-			ready = math.max(0.0, ready - dt*4)
-		end
-	--DebugPrint(fireTime)
-		local b = GetToolBody()
-		if b ~= 0 then
-			local shapes = GetBodyShapes(b)
-
-			--Control emissiveness
-			for i=1, #shapes do
-				SetShapeEmissiveScale(shapes[i], ready)
-			end
-	
-			--Add some light
-			if ready > 0 then
-				local p = TransformToParentPoint(GetBodyTransform(body), Vec(0, 0, -2))
-				PointLight(p, 1, 1, 1, ready * math.random(10, 15) / 20)
-			end
-								
-			--Move tool
-			local offset = VecScale(rndVec(0.1), ready*math.min(fireTime/5, 1.0))
-			SetToolTransform(Transform(offset))
-			
-
-			--Animate 
-			local t	= 1-ready
-			t = t*t
-			local offset = t*0.15
-			
-			if b ~= body then
-				body = b
-				--Get default transforms
-				t0 = GetShapeLocalTransform(shapes[2])
-				t1 = GetShapeLocalTransform(shapes[3])
-			end
-
-			t = TransformCopy(t0)
-			t.pos = VecAdd(t.pos, Vec(offset))
-			SetShapeLocalTransform(shapes[2], t)
-
-			t = TransformCopy(t1)
-			t.pos = VecAdd(t.pos, Vec(-offset))
-			SetShapeLocalTransform(shapes[3], t)
-		end
-	end
 end
 
 function clearDebris(minSize, maxSize, location, clearDistance, clearOnlyBroken, clearPercent, clearFire)
@@ -257,7 +83,6 @@
     SpawnParticle(origin, velocity, (0.25 + 4 * math.random() ^ 3) * strength)
 end
 
-
 function get_bodys(pos)
         QueryRequire("physical dynamic")
 	local bods = QueryAabbBodies( VecAdd(pos, Vec(-3, -3, -3)), VecAdd(pos, Vec(3, 3, 3)))
@@ -327,10 +152,169 @@
 	end
 
     if hit then 
-        SetFloat('level.destructible-bot.hitCounter',hitcounter)
-        SetInt('level.destructible-bot.hitShape',shape)
-        SetString('level.destructible-bot.weapon',"weapon-name")
-        SetFloat('level.destructible-bot.damage',damage)
+        SetFloat('level.destructible-bot.hitCounter',hitcounter, true)
+        SetInt('level.destructible-bot.hitShape',shape, true)
+        SetString('level.destructible-bot.weapon',"weapon-name", true)
+        SetFloat('level.destructible-bot.damage',damage, true)
     end 
 end
 
+function server.init()
+    RegisterTool("lightningun", "Lightning Gun", "MOD/vox/lightningun.vox")
+    SetBool("game.tool.lightningun.enabled", true, true)
+    ready = 0
+    fireTime = 0
+    dtOld = 0
+    oldTransform = Transform() 
+    laserSnd = LoadLoop("MOD/snd/laser.ogg")
+    hitSnd = LoadLoop("MOD/snd/hit.ogg")
+end
+
+function client.init()
+    openSnd = LoadSound("MOD/snd/open.ogg")
+    closeSnd = LoadSound("MOD/snd/close.ogg")
+end
+
+function client.tick(dt)
+    	if GetString("game.player.tool") == "lightningun" then
+
+    if InputPressed("grab") then
+    clearAllFires()
+    end
+
+    		--Check if tool is firing
+    		if GetBool("game.player.canusetool") and InputDown("usetool") then
+    			if ready == 0 then 
+    				PlaySound(openSnd) 
+    			end
+    			ready = math.min(1.0, ready + dt*4)
+    			if ready == 1.0 then
+    			--if fireTime > 0.1 and fireTime < 0.12 then
+    				PlayLoop(laserSnd)
+    				local t = GetCameraTransform()
+    				local fwd = TransformToParentVec(t, Vec(math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), math.min(2 * math.random() * 0.02, 0.2) - math.min(2 * math.random() * 0.02, 0.2), -1))
+    				local maxDist = 40
+    				local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist, .15)
+    				local raycast_shape_breakable = not HasTag(raycast_shape, "unbreakable")
+    				if not hit or not raycast_shape_breakable then
+    					dist = maxDist
+    				end
+
+    --Laser line start and end points
+
+    local playerTransform = GetPlayerCameraTransform(playerId)
+    local ct = GetCameraTransform()
+    local origin = TransformToParentPoint(ct, Vec(0.35, -0.35, 1))
+    local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
+
+    local deltaTransform = TransformToLocalTransform(oldTransform, playerTransform)
+    deltaTransform.rot = QuatSlerp(Quat(0,0,0,1), deltaTransform.rot, dt / dtOld * 0.1)
+    local predictedPlayerTransform = TransformToParentTransform(playerTransform, deltaTransform)
+
+    if GetBool("game.thirdperson") then
+    gunpos = TransformToParentPoint(GetCameraTransform(), Vec(0.01, -0.35, -3))
+    else
+    gunpos = VecAdd(QuatRotateVec(predictedPlayerTransform.rot, Vec(0.35, -0.35, 1)), VecAdd(GetCameraTransform().pos, VecScale(GetPlayerVelocity(playerId), GetTimeStep()*1)))
+    end
+
+    dtOld = dt
+    oldTransform = GetPlayerCameraTransform(playerId)
+
+    local s = VecAdd(VecAdd(gunpos, Vec(0, 0, 0)), VecScale(fwd, 1.5))
+    local e = VecAdd(gunpos, VecScale(fwd, dist))
+    --Draw laser line in ten segments with random offset
+    local last = s
+    local particleSize = math.random(10, 125)/1500
+    local particleStepAdjustment = 2.5
+    for i=1, 10 do
+        local t = i/10
+        --DebugPrint(t)
+        local p = VecLerp(s, e, t)
+        local offset_length = 1 / (t + 2.5)
+        p = VecAdd(p, rndVec(offset_length))
+        local dir = VecNormalize(VecSub(p, last))
+        local distance = VecLength(VecSub(p, last))
+        local stepDistance = particleSize*particleStepAdjustment--distance/500
+        for x=0, distance/stepDistance do
+          local newDistance = stepDistance * x
+          local newStartingPoint = VecAdd(last, VecScale(dir, newDistance))
+          --howManyParticles = howManyParticles + 1
+    	local spriteDistance = VecLength(VecSub(newStartingPoint, s))
+    	local size = (0.085 + 0.45 * (1 / (spriteDistance + 1))) * (math.random() + 0.5)
+    	DrawSprite(muzzleflash,{pos=newStartingPoint,rot=QuatRotateQuat(GetPlayerCameraTransform(playerId).rot, QuatEuler(0, 0, math.random() * 360))},size,size, 1,1,1,1,1,1,0.1,false,true)
+    	end	
+        ---DrawLine(last, p, 1, 0.5, 0.7)
+        last = p
+    end
+
+    				--Make damage and spawn particles
+    				if hit then
+    					---PlayLoop(hitSnd)
+
+    					Paint(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2),math.random(-2,2))), 1.07, "explosion")	
+
+    if math.random(1,2) <= 2 then
+    get_bodys(e)
+
+    MakeHole(VecAdd(e, Vec(math.random(-2,2),math.random(-2,2), math.random(-2,2))), math.random(1, 3000)/1000, math.random(1, 2750)/1000, math.random(1, 2500)/1000, true)
+    end
+
+    clearDebris(125, 450, e, 3, true, 1, false)
+
+    				end
+    				--end
+    				fireTime = fireTime + dt
+    				if fireTime > 0.2 then
+    				fireTime = 0
+    				end
+    			end
+    		else
+    			fireTime = 0
+    			if ready == 1 then
+    				PlaySound(closeSnd)
+    			end
+    			ready = math.max(0.0, ready - dt*4)
+    		end
+    	--DebugPrint(fireTime)
+    		local b = GetToolBody()
+    		if b ~= 0 then
+    			local shapes = GetBodyShapes(b)
+
+    			--Control emissiveness
+    			for i=1, #shapes do
+    				SetShapeEmissiveScale(shapes[i], ready)
+    			end
+
+    			--Add some light
+    			if ready ~= 0 then
+    				local p = TransformToParentPoint(GetBodyTransform(body), Vec(0, 0, -2))
+    				PointLight(p, 1, 1, 1, ready * math.random(10, 15) / 20)
+    			end
+
+    			--Move tool
+    			local offset = VecScale(rndVec(0.1), ready*math.min(fireTime/5, 1.0))
+    			SetToolTransform(Transform(offset))
+
+    			--Animate 
+    			local t	= 1-ready
+    			t = t*t
+    			local offset = t*0.15
+
+    			if b ~= body then
+    				body = b
+    				--Get default transforms
+    				t0 = GetShapeLocalTransform(shapes[2])
+    				t1 = GetShapeLocalTransform(shapes[3])
+    			end
+
+    			t = TransformCopy(t0)
+    			t.pos = VecAdd(t.pos, Vec(offset))
+    			SetShapeLocalTransform(shapes[2], t)
+
+    			t = TransformCopy(t1)
+    			t.pos = VecAdd(t.pos, Vec(-offset))
+    			SetShapeLocalTransform(shapes[3], t)
+    		end
+    	end
+end
+

```
