# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,56 +1,4 @@
-
-
-dualminigunprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("dualminiguns", "Dual Miniguns", "MOD/vox/dualminiguns.vox")
-	SetBool("game.tool.dualminiguns.enabled", true)
-	SetFloat("game.tool.dualminiguns.ammo", 101)
-
-	STATE_READY = 0
-	STATE_FIRING = 1
-	STATE_WINDING = 2
-	STATE_UNWINDING = 3
-
-	damage = 1
-	gravity = Vec(0, 0, 0)
-	velocity = 1.5
-
-	bulletsFired = 0
-	maxVel = 0
-
-	for i=1, 300 do
-		dualminigunprojectileHandler.shells[i] = deepcopy(dualminigunprojectileHandler.defaultShell)
-	end
-
-	gun1 = {}
-	gun1.startDelay = 0.6
-	gun1.spreadTimer = 0
-	gun1.smokeTimer = 0
-	gun1.simulBullets = 0
-	gun1.angle = 0
-	gun1.angVel = 0
-	gun1.state = STATE_READY
-
-	gun2 = {}
-	gun2.startDelay = 0.6
-	gun2.spreadTimer = 0
-	gun2.smokeTimer = 0
-	gun2.simulBullets = 0
-	gun2.angle = 0
-	gun2.angVel = 0
-	gun2.state = STATE_READY
-
-	gunsound = LoadLoop("MOD/snd/gunloop.ogg")
-	cocksound = LoadSound("MOD/snd/m249_cock.ogg")
-	windupsound = LoadSound("MOD/snd/windup.ogg")
-	winddownsound = LoadSound("MOD/snd/winddown.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -85,11 +33,11 @@
 	local aimpos, hit, distance = GetAimPos()
 
 	local recoildir = TransformToParentVec(ct, Vec(0, 0, 0.25))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local oldvel = VecCopy(vel)
 	vel = VecAdd(vel, recoildir)
 	if VecLength(vel) > maxVel then vel = oldvel end
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
 	
 	local p = rightPos
 	local dir = VecSub(aimpos, p)
@@ -120,11 +68,11 @@
 	local aimpos, hit, distance = GetAimPos()
 
 	local recoildir = TransformToParentVec(ct, Vec(0, 0, 0.25))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local oldvel = VecCopy(vel)
 	vel = VecAdd(vel, recoildir)
 	if VecLength(vel) > maxVel then vel = oldvel end
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
 	
 	local p = leftPos
 	local dir = VecSub(aimpos, p)
@@ -168,175 +116,222 @@
 	projectile.pos = point2
 end
 
-function tick(dt)
-	local timeStep = GetTimeStep()
-	for key, shell in ipairs(dualminigunprojectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-
-	if GetString("game.player.tool") == "dualminiguns" and GetPlayerVehicle() == 0 then
-		if InputDown("lmb") then
-			if gun1.state == STATE_READY or gun1.state == STATE_UNWINDING then
-				gun1.state = STATE_WINDING
-				PlaySound(windupsound, GetPlayerTransform().pos, 0.5, false)
-			end
-			gun1.angVel = math.min(500, gun1.angVel + dt*1000)
-		else
-			gun1.angVel = math.max(0, gun1.angVel - dt*250)
-		end
-
-		if InputDown("lmb") and InputDown("rmb") then
-			maxVel = 9
-		else
-			maxVel = 6.5
-		end
-
-		if InputReleased("lmb") then
-			if gun1.state == STATE_FIRING or gun1.state == STATE_WINDING then
-				gun1.state = STATE_UNWINDING
-				gun1.spreadTimer = 0
-				if gun1.simulBullets > 3 then
-					SpawnParticle("darksmoke", leftPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
-					SpawnParticle("smoke", leftPos, Vec(0, 1.0+math.random(1,3)*0.1, 0), 1, 2)
-				end
-				if gun1.simulBullets > 100 then
-					gun1.smokeTimer = 1
-				end
-				gun1.simulBullets = 0
-				PlaySound(winddownsound, GetPlayerTransform().pos, 0.5, false)
-			end
-		end
-
-		if InputDown("rmb") then
-			if gun2.state == STATE_READY or gun2.state == STATE_UNWINDING then
-				gun2.state = STATE_WINDING
-				PlaySound(windupsound, GetPlayerTransform().pos, 0.5, false)
-			end
-			gun2.angVel = math.min(500, gun2.angVel + dt*1000)
-		else
-			gun2.angVel = math.max(0, gun2.angVel - dt*250)
-		end
-
-		if InputReleased("rmb") then
-			if gun2.state == STATE_FIRING or gun2.state == STATE_WINDING then
-				gun2.state = STATE_UNWINDING
-				gun2.spreadTimer = 0
-				if gun2.simulBullets > 3 then
-					SpawnParticle("darksmoke", rightPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
-					SpawnParticle("smoke", rightPos, Vec(0, 1.0+math.random(1,3)*0.1, 0), 1, 2)
-				end
-				if gun2.simulBullets > 100 then
-					gun2.smokeTimer = 1
-				end
-				gun2.simulBullets = 0
-				PlaySound(winddownsound, GetPlayerTransform().pos, 0.5, false)
-			end
-		end
-
-		if gun1.state == STATE_WINDING then
-			gun1.startDelay = gun1.startDelay - timeStep
-			if gun1.startDelay <= 0 then
-				gun1.state = STATE_FIRING
-			end
-		end
-		if gun2.state == STATE_WINDING then
-			gun2.startDelay = gun2.startDelay - timeStep
-			if gun2.startDelay <= 0 then
-				gun2.state = STATE_FIRING
-			end
-		end
-	
-		if gun1.state == STATE_UNWINDING then
-			gun1.startDelay = gun1.startDelay + timeStep
-			if gun1.startDelay > 0.6 then
-				gun1.state = STATE_READY
-				gun1.startDelay = 0.6
-			end
-		end
-		if gun2.state == STATE_UNWINDING then
-			gun2.startDelay = gun2.startDelay + timeStep
-			if gun2.startDelay > 0.6 then
-				gun2.state = STATE_READY
-				gun2.startDelay = 0.6
-			end
-		end
-	
-		if gun1.state == STATE_FIRING then
-			Shoot2(gun1)
-			PlayLoop(gunsound, GetPlayerTransform().pos, 0.6, false)
-		end
-	
-		if gun2.state == STATE_FIRING then
-			Shoot1(gun2)
-			PlayLoop(gunsound, GetPlayerTransform().pos, 0.6, false)
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0.1, heightOffset, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			leftPos = TransformToParentPoint(toolTrans, Vec(-0.55, -0.7, -2))
-			rightPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.7, -2))
-
-			gun1.angle = gun1.angle + gun1.angVel * dt * 5
-			gun2.angle = gun2.angle + gun2.angVel * dt * 5
-
-			local voxSize = 0.1
-			local attach1 = Transform(Vec(2.8*voxSize, -7.3*voxSize, 0))
-			local attach2 = Transform(Vec(-5.3*voxSize, -7.3*voxSize, 0))
-			if body ~= b then
-				body = b
-				-- Barrel is the second shape in vox file. Remember original position in attachment frame
-				local shapes = GetBodyShapes(b)
-				barrel1 = shapes[1]
-				barrel2 = shapes[3]
-				barrelTransform1 = TransformToLocalTransform(attach1, GetShapeLocalTransform(barrel1))
-				barrelTransform2 = TransformToLocalTransform(attach2, GetShapeLocalTransform(barrel2))	
-			end
-
-			local t = Transform()
-			local t2 = Transform()
-
-			attach1.rot = QuatEuler(0, 0, -gun2.angle)
-			t = TransformToParentTransform(attach1, barrelTransform1)
-			SetShapeLocalTransform(barrel1, t)
-
-			attach2.rot = QuatEuler(0, 0, -gun1.angle)
-			t2 = TransformToParentTransform(attach2, barrelTransform2)
-			SetShapeLocalTransform(barrel2, t2)
-		end
-
-		if gun1.smokeTimer >= 0 then
-			local smokepos = TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.65, -1))
-			SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), .5, 1.5)
-			gun1.smokeTimer = gun1.smokeTimer - timeStep
-		end
-		if gun2.smokeTimer >= 0 then
-			local smokepos = TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.65, -1))
-			SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), .5, 1.5)
-			gun2.smokeTimer = gun2.smokeTimer - timeStep
-		end
-	else
-		gun1.state = STATE_READY
-		gun2.state = STATE_READY
-		gun1.startDelay = 0.6
-		gun2.startDelay = 0.6
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "dualminiguns" and GetPlayerVehicle() == 0 then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(bulletsFired)
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("dualminiguns", "Dual Miniguns", "MOD/vox/dualminiguns.vox")
+    SetBool("game.tool.dualminiguns.enabled", true, true)
+    SetFloat("game.tool.dualminiguns.ammo", 101, true)
+    STATE_READY = 0
+    STATE_FIRING = 1
+    STATE_WINDING = 2
+    STATE_UNWINDING = 3
+    damage = 1
+    gravity = Vec(0, 0, 0)
+    velocity = 1.5
+    bulletsFired = 0
+    maxVel = 0
+    for i=1, 300 do
+    	dualminigunprojectileHandler.shells[i] = deepcopy(dualminigunprojectileHandler.defaultShell)
+    end
+    gun1 = {}
+    gun1.startDelay = 0.6
+    gun1.spreadTimer = 0
+    gun1.smokeTimer = 0
+    gun1.simulBullets = 0
+    gun1.angle = 0
+    gun1.angVel = 0
+    gun1.state = STATE_READY
+    gun2 = {}
+    gun2.startDelay = 0.6
+    gun2.spreadTimer = 0
+    gun2.smokeTimer = 0
+    gun2.simulBullets = 0
+    gun2.angle = 0
+    gun2.angVel = 0
+    gun2.state = STATE_READY
+    gunsound = LoadLoop("MOD/snd/gunloop.ogg")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local timeStep = GetTimeStep()
+        for key, shell in ipairs(dualminigunprojectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
+        end
+    end
+end
+
+function client.init()
+    cocksound = LoadSound("MOD/snd/m249_cock.ogg")
+    windupsound = LoadSound("MOD/snd/windup.ogg")
+    winddownsound = LoadSound("MOD/snd/winddown.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "dualminiguns" and GetPlayerVehicle(playerId) == 0 then
+    	if InputDown("lmb") then
+    		if gun1.state == STATE_READY or gun1.state == STATE_UNWINDING then
+    			gun1.state = STATE_WINDING
+    			PlaySound(windupsound, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    		gun1.angVel = math.min(500, gun1.angVel + dt*1000)
+    	else
+    		gun1.angVel = math.max(0, gun1.angVel - dt*250)
+    	end
+
+    	if InputDown("lmb") and InputDown("rmb") then
+    		maxVel = 9
+    	else
+    		maxVel = 6.5
+    	end
+
+    	if InputReleased("lmb") then
+    		if gun1.state == STATE_FIRING or gun1.state == STATE_WINDING then
+    			gun1.state = STATE_UNWINDING
+    			gun1.spreadTimer = 0
+    			if gun1.simulBullets > 3 then
+    				SpawnParticle("darksmoke", leftPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
+    				SpawnParticle("smoke", leftPos, Vec(0, 1.0+math.random(1,3)*0.1, 0), 1, 2)
+    			end
+    			if gun1.simulBullets > 100 then
+    				gun1.smokeTimer = 1
+    			end
+    			gun1.simulBullets = 0
+    			PlaySound(winddownsound, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    	end
+
+    	if InputDown("rmb") then
+    		if gun2.state == STATE_READY or gun2.state == STATE_UNWINDING then
+    			gun2.state = STATE_WINDING
+    			PlaySound(windupsound, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    		gun2.angVel = math.min(500, gun2.angVel + dt*1000)
+    	else
+    		gun2.angVel = math.max(0, gun2.angVel - dt*250)
+    	end
+
+    	if InputReleased("rmb") then
+    		if gun2.state == STATE_FIRING or gun2.state == STATE_WINDING then
+    			gun2.state = STATE_UNWINDING
+    			gun2.spreadTimer = 0
+    			if gun2.simulBullets > 3 then
+    				SpawnParticle("darksmoke", rightPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
+    				SpawnParticle("smoke", rightPos, Vec(0, 1.0+math.random(1,3)*0.1, 0), 1, 2)
+    			end
+    			if gun2.simulBullets > 100 then
+    				gun2.smokeTimer = 1
+    			end
+    			gun2.simulBullets = 0
+    			PlaySound(winddownsound, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    	end
+
+    	if gun1.state == STATE_WINDING then
+    		gun1.startDelay = gun1.startDelay - timeStep
+    		if gun1.startDelay <= 0 then
+    			gun1.state = STATE_FIRING
+    		end
+    	end
+    	if gun2.state == STATE_WINDING then
+    		gun2.startDelay = gun2.startDelay - timeStep
+    		if gun2.startDelay <= 0 then
+    			gun2.state = STATE_FIRING
+    		end
+    	end
+
+    	if gun1.state == STATE_UNWINDING then
+    		gun1.startDelay = gun1.startDelay + timeStep
+    		if gun1.startDelay > 0.6 then
+    			gun1.state = STATE_READY
+    			gun1.startDelay = 0.6
+    		end
+    	end
+    	if gun2.state == STATE_UNWINDING then
+    		gun2.startDelay = gun2.startDelay + timeStep
+    		if gun2.startDelay > 0.6 then
+    			gun2.state = STATE_READY
+    			gun2.startDelay = 0.6
+    		end
+    	end
+
+    	if gun1.state == STATE_FIRING then
+    		Shoot2(gun1)
+    		PlayLoop(gunsound, GetPlayerTransform(playerId).pos, 0.6, false)
+    	end
+
+    	if gun2.state == STATE_FIRING then
+    		Shoot1(gun2)
+    		PlayLoop(gunsound, GetPlayerTransform(playerId).pos, 0.6, false)
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0.1, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		leftPos = TransformToParentPoint(toolTrans, Vec(-0.55, -0.7, -2))
+    		rightPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.7, -2))
+
+    		gun1.angle = gun1.angle + gun1.angVel * dt * 5
+    		gun2.angle = gun2.angle + gun2.angVel * dt * 5
+
+    		local voxSize = 0.1
+    		local attach1 = Transform(Vec(2.8*voxSize, -7.3*voxSize, 0))
+    		local attach2 = Transform(Vec(-5.3*voxSize, -7.3*voxSize, 0))
+    		if body ~= b then
+    			body = b
+    			-- Barrel is the second shape in vox file. Remember original position in attachment frame
+    			local shapes = GetBodyShapes(b)
+    			barrel1 = shapes[1]
+    			barrel2 = shapes[3]
+    			barrelTransform1 = TransformToLocalTransform(attach1, GetShapeLocalTransform(barrel1))
+    			barrelTransform2 = TransformToLocalTransform(attach2, GetShapeLocalTransform(barrel2))	
+    		end
+
+    		local t = Transform()
+    		local t2 = Transform()
+
+    		attach1.rot = QuatEuler(0, 0, -gun2.angle)
+    		t = TransformToParentTransform(attach1, barrelTransform1)
+    		SetShapeLocalTransform(barrel1, t)
+
+    		attach2.rot = QuatEuler(0, 0, -gun1.angle)
+    		t2 = TransformToParentTransform(attach2, barrelTransform2)
+    		SetShapeLocalTransform(barrel2, t2)
+    	end
+
+    	if gun1.smokeTimer >= 0 then
+    		local smokepos = TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.65, -1))
+    		SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), .5, 1.5)
+    		gun1.smokeTimer = gun1.smokeTimer - timeStep
+    	end
+    	if gun2.smokeTimer >= 0 then
+    		local smokepos = TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.65, -1))
+    		SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), .5, 1.5)
+    		gun2.smokeTimer = gun2.smokeTimer - timeStep
+    	end
+    else
+    	gun1.state = STATE_READY
+    	gun2.state = STATE_READY
+    	gun1.startDelay = 0.6
+    	gun2.startDelay = 0.6
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "dualminiguns" and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText(bulletsFired)
+    	UiPop()
+    end
+end
+

```
