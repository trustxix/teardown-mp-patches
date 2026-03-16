# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,45 +1,8 @@
+#version 2
 local STATE_READY = 0
 local STATE_FIRING = 1
 local STATE_WINDING = 2
 local STATE_UNWINDING = 3
-
-minigunprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("crestaminigun", "Minigun", "MOD/vox/crestaminigun.vox")
-	SetBool("game.tool.crestaminigun.enabled", true)
-	SetFloat("game.tool.crestaminigun.ammo", 101)
-
-	state = STATE_READY
-	damage = 1
-	gravity = Vec(0, 0, 0)
-	velocity = 1.5
-	angle = 0
-	angVel = 0
-
-	shotDelay = 0.00001
-	startDelay = 0.6
-	bulletsFired = 0
-	simulBullets = 0
-
-	for i=1, 300 do
-		minigunprojectileHandler.shells[i] = deepcopy(minigunprojectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	spreadTimer = 0
-	smokeTimer = 0
-	recoilTimer = 0
-
-	gunsound = LoadLoop("MOD/snd/gunloop.ogg")
-	cocksound = LoadSound("MOD/snd/m249_cock.ogg")
-	windupsound = LoadSound("MOD/snd/windup.ogg")
-	winddownsound = LoadSound("MOD/snd/winddown.ogg")
-end
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -71,7 +34,7 @@
 end
 
 function Shoot()
-	if shootTimer > 0 then
+	if shootTimer ~= 0 then
 		return
 	end
 
@@ -79,11 +42,11 @@
 	aimpos, hit, distance = GetAimPos()
 
 	local recoildir = TransformToParentVec(ct, Vec(0, 0, 0.25))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local oldvel = VecCopy(vel)
 	vel = VecAdd(vel, recoildir)
 	if VecLength(vel) > 6.5 then vel = oldvel end
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
 	
 	local p = toolPos
 	local dir = VecSub(aimpos, p)
@@ -129,117 +92,151 @@
 	projectile.pos = point2
 end
 
-function tick(dt)
-	for key, shell in ipairs(minigunprojectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-
-	if GetString("game.player.tool") == "crestaminigun" and GetPlayerVehicle() == 0 then
-		if InputDown("lmb") then
-			if state == STATE_READY or state == STATE_UNWINDING then
-				state = STATE_WINDING
-				PlaySound(windupsound, GetPlayerTransform().pos, 0.5, false)
-			end
-			angVel = math.min(500, angVel + dt*1000)
-		else
-			angVel = math.max(0, angVel - dt*250)
-		end
-
-		if InputReleased("lmb") then
-			if state == STATE_FIRING or state == STATE_WINDING then
-				state = STATE_UNWINDING
-				spreadTimer = 0
-				if simulBullets > 3 then
-					SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
-					SpawnParticle("smoke", toolPos, Vec(0, 1.0+math.random(1,3)*0.1, 0), 1, 2)
-				end
-				if simulBullets > 100 then
-					smokeTimer = 1
-				end
-				simulBullets = 0
-				PlaySound(winddownsound, GetPlayerTransform().pos, 0.5, false)
-			end
-		end
-
-		if state == STATE_WINDING then
-			startDelay = startDelay - dt
-			if startDelay <= 0 then
-				state = STATE_FIRING
-			end
-		end
-
-		if state == STATE_UNWINDING then
-			startDelay = startDelay + dt
-			if startDelay > 0.6 then
-				state = STATE_READY
-				startDelay = 0.6
-			end
-		end
-
-		if state == STATE_FIRING then
-			Shoot()
-			PlayLoop(gunsound, GetPlayerTransform().pos, 0.6, false)
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0.1, heightOffset, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.75, -2.1))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0.1, heightOffset, 0.01)
-				t.rot = QuatEuler(1, 0, 0)
-				SetToolTransform(t)
-				PointLight(toolPos, 1, 1, 1, 0.5)
-
-				recoilTimer = recoilTimer - dt
-			end
-
-			angle = angle + angVel * dt * 5
-			local voxSize = 0.1
-			local attach = Transform(Vec(2.8*voxSize, -7.3*voxSize, 0))
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				barrel = shapes[1]
-				barrelTransform = TransformToLocalTransform(attach, GetShapeLocalTransform(barrel))	
-			end
-
-			attach.rot = QuatEuler(0, 0, -angle)
-			t = TransformToParentTransform(attach, barrelTransform)
-			SetShapeLocalTransform(barrel, t)
-		end
-	else
-		state = STATE_READY
-		startDelay = 0.6
-	end
-	
-	if smokeTimer >= 0 then
-		local smokepos = TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.65, -1))
-		SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), .5, 1.5)
-		smokeTimer = smokeTimer - dt
-	end
-
-	if shootTimer > 0 then
-		shootTimer = shootTimer - dt
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "crestaminigun" and GetPlayerVehicle() == 0 then
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
+    RegisterTool("crestaminigun", "Minigun", "MOD/vox/crestaminigun.vox")
+    SetBool("game.tool.crestaminigun.enabled", true, true)
+    SetFloat("game.tool.crestaminigun.ammo", 101, true)
+    state = STATE_READY
+    damage = 1
+    gravity = Vec(0, 0, 0)
+    velocity = 1.5
+    angle = 0
+    angVel = 0
+    shotDelay = 0.00001
+    startDelay = 0.6
+    bulletsFired = 0
+    simulBullets = 0
+    for i=1, 300 do
+    	minigunprojectileHandler.shells[i] = deepcopy(minigunprojectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    spreadTimer = 0
+    smokeTimer = 0
+    recoilTimer = 0
+    gunsound = LoadLoop("MOD/snd/gunloop.ogg")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(minigunprojectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
+        end
+        if shootTimer ~= 0 then
+        	shootTimer = shootTimer - dt
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
+    if GetString("game.player.tool") == "crestaminigun" and GetPlayerVehicle(playerId) == 0 then
+    	if InputDown("lmb") then
+    		if state == STATE_READY or state == STATE_UNWINDING then
+    			state = STATE_WINDING
+    			PlaySound(windupsound, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    		angVel = math.min(500, angVel + dt*1000)
+    	else
+    		angVel = math.max(0, angVel - dt*250)
+    	end
+
+    	if InputReleased("lmb") then
+    		if state == STATE_FIRING or state == STATE_WINDING then
+    			state = STATE_UNWINDING
+    			spreadTimer = 0
+    			if simulBullets > 3 then
+    				SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
+    				SpawnParticle("smoke", toolPos, Vec(0, 1.0+math.random(1,3)*0.1, 0), 1, 2)
+    			end
+    			if simulBullets > 100 then
+    				smokeTimer = 1
+    			end
+    			simulBullets = 0
+    			PlaySound(winddownsound, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    	end
+
+    	if state == STATE_WINDING then
+    		startDelay = startDelay - dt
+    		if startDelay <= 0 then
+    			state = STATE_FIRING
+    		end
+    	end
+
+    	if state == STATE_UNWINDING then
+    		startDelay = startDelay + dt
+    		if startDelay > 0.6 then
+    			state = STATE_READY
+    			startDelay = 0.6
+    		end
+    	end
+
+    	if state == STATE_FIRING then
+    		Shoot()
+    		PlayLoop(gunsound, GetPlayerTransform(playerId).pos, 0.6, false)
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0.1, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.75, -2.1))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0.1, heightOffset, 0.01)
+    			t.rot = QuatEuler(1, 0, 0)
+    			SetToolTransform(t)
+    			PointLight(toolPos, 1, 1, 1, 0.5)
+
+    			recoilTimer = recoilTimer - dt
+    		end
+
+    		angle = angle + angVel * dt * 5
+    		local voxSize = 0.1
+    		local attach = Transform(Vec(2.8*voxSize, -7.3*voxSize, 0))
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			barrel = shapes[1]
+    			barrelTransform = TransformToLocalTransform(attach, GetShapeLocalTransform(barrel))	
+    		end
+
+    		attach.rot = QuatEuler(0, 0, -angle)
+    		t = TransformToParentTransform(attach, barrelTransform)
+    		SetShapeLocalTransform(barrel, t)
+    	end
+    else
+    	state = STATE_READY
+    	startDelay = 0.6
+    end
+    if smokeTimer >= 0 then
+    	local smokepos = TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.65, -1))
+    	SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), .5, 1.5)
+    	smokeTimer = smokeTimer - dt
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "crestaminigun" and GetPlayerVehicle(playerId) == 0 then
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
