# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,59 +1,4 @@
-attackdroneprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active=false}
-}
-
-pSpeed = GetFloatParam("speed", 7)
-
-function init()
-	RegisterTool("attackdrone", "Attack Drone", "MOD/vox/attackdrone.vox")
-	SetBool("game.tool.attackdrone.enabled", true)
-	SetString("game.tool.attackdrone.ammo.display","")
-	SetFloat("game.tool.attackdrone.ammo", 101)
-
-	for i=1, 100 do
-		attackdroneprojectileHandler.shells[i] = deepcopy(attackdroneprojectileHandler.defaultShell)
-	end
-
-	flycamenabled = false
-	attackdroneenabled = false
-	firing = false
-	magnet = false
-	lockCam = false
-	hideSight = false
-
-	damage = 1
-	gravity = Vec()
-	velocity = 1
-	shotDelay = 0.08
-	
-	droneVel = Vec()
-	angle = 0.0
-	distanceToGround = 0
-	droneHeight = 10
-	averageSurroundingHeight = 0
-	droneSpeed = 15
-
-	maxDist = 25
-	maxMass = 5000
-	gravStrength = 0.5
-
-	lightTimer = 0
-	equipTimer = 0
-	shoottimer = 0
-
-	gunsound = LoadSound("MOD/snd/gun0.ogg")
-	dronesound = LoadLoop("MOD/snd/drone.ogg")
-
-	drone = {}
-	drone.barrel = {}
-	drone.barrel.rot = Quat()
-
-	droneTargetPos = Vec()
-	droneTargetRot = Quat()
-end
-
+#version 2
 function aorb(a, b, d)
 	return (a and d or 0) - (b and d or 0)
 end
@@ -148,7 +93,7 @@
 	drone.barrel.rot = QuatRotateQuat(drone.barrel.rot, QuatEuler(my/rotdiv, -mx/rotdiv, 0))
 	local newT = Transform(drone.barrel.pos, drone.barrel.rot)
 	SetCameraTransform(newT)
-	SetPlayerTransform(GetPlayerTransform())
+	SetPlayerTransform(playerId, GetPlayerTransform(playerId))
 
 	if a or d or w or s or ctrl or space then
 		droneTargetPos = TransformToParentPoint(newT, Vec(aorb(a, d, -droneSpeed), aorb(ctrl, space, -droneSpeed), aorb(w, s, -droneSpeed)))
@@ -158,7 +103,7 @@
 end
 
 function Shoot()
-	if shoottimer > 0 then
+	if shoottimer ~= 0 then
 		return
 	end
 
@@ -212,7 +157,7 @@
 function droneMovement(dt)
 	angle = angle + 0.6
 
-	targetPos = GetPlayerPos()
+	targetPos = GetPlayerPos(playerId)
 
 	local hoverPos = VecCopy(targetPos)
 	local radius = clamp(10, 10, 10)
@@ -291,102 +236,148 @@
 	end
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "attackdrone" and GetPlayerVehicle() == 0 then
-		PlayLoop(dronesound, drone.pos, 0.6)
-
-		firing = InputDown("lmb")
-		if InputPressed("m") then 
-			magnet = not magnet
-			SetString("hud.notification", "Magnet "..(magnet and "on" or "off"))
-		end
-
-		if InputPressed("n") then
-			hideSight = not hideSight
-			SetString("hud.notification", "Hide crosshair "..(hideSight and "on" or "off"))
-		end
-		
-		if InputPressed("r") then
-			lockCam = not lockCam
-			SetString("hud.notification", "Lock cam "..(lockCam and "on" or "off"))
-		end
-		if InputPressed("rmb") then flycamenabled = not flycamenabled end
-		if InputPressed("esc") then flycamenabled = false end
-		
-		if flycamenabled then FlyCam() end
-		if firing then Shoot() end
-		if magnet then Magnet() end
-
-		aimpos = flycamenabled and GetCamLookPos() or GetAimPos()
-
-		if not attackdroneenabled then
-			attackdroneenabled = true
-			droneTargetPos = GetPlayerTransform().pos
-			drone.pos = TransformToParentPoint(GetPlayerTransform(), Vec(0, 0, -3))
-			drone.rot = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0))
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.1))
-
-			if lightTimer > 0 then
-				PointLight(drone.barrel.pos, 1, 1, 1, 1)
-				lightTimer = lightTimer - dt
-			end
-
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				droneshape = shapes[1]
-				controlshape = shapes[2]
-				dronetransformation = GetShapeLocalTransform(droneshape)
-				controltransformation = GetShapeLocalTransform(controlshape)
-			end
-
-			ct = TransformCopy(controltransformation)
-			ct.rot = QuatRotateQuat(ct.rot, QuatEuler(-25, 0, 0))
-			SetShapeLocalTransform(controlshape, ct)
-
-			SetShapeLocalTransform(droneshape, TransformToLocalTransform(GetBodyTransform(GetToolBody()), drone))
-		end
-
-		if not flycamenabled then droneMovement(dt) end
-		drone.barrel.pos = TransformToParentPoint(drone, Vec(0.5, 0.25, -0.2))
-
-		for key, shell in ipairs(attackdroneprojectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell, dt)
-			end
-		end
-	else
-		attackdroneenabled = false
-		flycamenabled = false
-	end
-
-	if shoottimer > 0 then
-		shoottimer = shoottimer - dt
-	end
-end
-
-function update(dt)
-	if GetString("game.player.tool") == "attackdrone" and GetPlayerVehicle() == 0 then
-		local acc = VecSub(droneTargetPos, drone.pos)
-		droneVel = VecAdd(droneVel, VecScale(acc, dt))
-		droneVel = VecScale(droneVel, 0.98)
-		drone.pos = VecAdd(drone.pos, VecScale(droneVel, dt))
-		drone.rot = QuatSlerp(drone.rot, droneTargetRot, 0.02)
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "attackdrone" and GetPlayerVehicle() == 0 and flycamenabled and not hideSight then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiColor(1, 1, 1, 0.5)
-			UiAlign("center middle")
-			UiImage("MOD/img/crosshair.png")
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("attackdrone", "Attack Drone", "MOD/vox/attackdrone.vox")
+    SetBool("game.tool.attackdrone.enabled", true, true)
+    SetString("game.tool.attackdrone.ammo.display","", true)
+    SetFloat("game.tool.attackdrone.ammo", 101, true)
+    for i=1, 100 do
+    	attackdroneprojectileHandler.shells[i] = deepcopy(attackdroneprojectileHandler.defaultShell)
+    end
+    flycamenabled = false
+    attackdroneenabled = false
+    firing = false
+    magnet = false
+    lockCam = false
+    hideSight = false
+    damage = 1
+    gravity = Vec()
+    velocity = 1
+    shotDelay = 0.08
+    droneVel = Vec()
+    angle = 0.0
+    distanceToGround = 0
+    droneHeight = 10
+    averageSurroundingHeight = 0
+    droneSpeed = 15
+    maxDist = 25
+    maxMass = 5000
+    gravStrength = 0.5
+    lightTimer = 0
+    equipTimer = 0
+    shoottimer = 0
+    dronesound = LoadLoop("MOD/snd/drone.ogg")
+    drone = {}
+    drone.barrel = {}
+    drone.barrel.rot = Quat()
+    droneTargetPos = Vec()
+    droneTargetRot = Quat()
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetString("game.player.tool") == "attackdrone" and GetPlayerVehicle(playerId) == 0 then
+        	local acc = VecSub(droneTargetPos, drone.pos)
+        	droneVel = VecAdd(droneVel, VecScale(acc, dt))
+        	droneVel = VecScale(droneVel, 0.98)
+        	drone.pos = VecAdd(drone.pos, VecScale(droneVel, dt))
+        	drone.rot = QuatSlerp(drone.rot, droneTargetRot, 0.02)
+        end
+    end
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/gun0.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "attackdrone" and GetPlayerVehicle(playerId) == 0 then
+    	PlayLoop(dronesound, drone.pos, 0.6)
+
+    	firing = InputDown("lmb")
+    	if InputPressed("m") then 
+    		magnet = not magnet
+    		SetString("hud.notification", "Magnet "..(magnet and "on" or "off"), true)
+    	end
+
+    	if InputPressed("n") then
+    		hideSight = not hideSight
+    		SetString("hud.notification", "Hide crosshair "..(hideSight and "on" or "off"), true)
+    	end
+
+    	if InputPressed("r") then
+    		lockCam = not lockCam
+    		SetString("hud.notification", "Lock cam "..(lockCam and "on" or "off"), true)
+    	end
+    	if InputPressed("rmb") then flycamenabled = not flycamenabled end
+    	if InputPressed("esc") then flycamenabled = false end
+
+    	if flycamenabled then FlyCam() end
+    	if firing then Shoot() end
+    	if magnet then Magnet() end
+
+    	aimpos = flycamenabled and GetCamLookPos() or GetAimPos()
+
+    	if not attackdroneenabled then
+    		attackdroneenabled = true
+    		droneTargetPos = GetPlayerTransform(playerId).pos
+    		drone.pos = TransformToParentPoint(GetPlayerTransform(playerId), Vec(0, 0, -3))
+    		drone.rot = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0))
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.1))
+
+    		if lightTimer ~= 0 then
+    			PointLight(drone.barrel.pos, 1, 1, 1, 1)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			droneshape = shapes[1]
+    			controlshape = shapes[2]
+    			dronetransformation = GetShapeLocalTransform(droneshape)
+    			controltransformation = GetShapeLocalTransform(controlshape)
+    		end
+
+    		ct = TransformCopy(controltransformation)
+    		ct.rot = QuatRotateQuat(ct.rot, QuatEuler(-25, 0, 0))
+    		SetShapeLocalTransform(controlshape, ct)
+
+    		SetShapeLocalTransform(droneshape, TransformToLocalTransform(GetBodyTransform(GetToolBody()), drone))
+    	end
+
+    	if not flycamenabled then droneMovement(dt) end
+    	drone.barrel.pos = TransformToParentPoint(drone, Vec(0.5, 0.25, -0.2))
+
+    	for key, shell in ipairs(attackdroneprojectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell, dt)
+    		end
+    	end
+    else
+    	attackdroneenabled = false
+    	flycamenabled = false
+    end
+
+    if shoottimer ~= 0 then
+    	shoottimer = shoottimer - dt
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "attackdrone" and GetPlayerVehicle(playerId) == 0 and flycamenabled and not hideSight then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiColor(1, 1, 1, 0.5)
+    		UiAlign("center middle")
+    		UiImage("MOD/img/crosshair.png")
+    	UiPop()
+    end
+end
+

```
