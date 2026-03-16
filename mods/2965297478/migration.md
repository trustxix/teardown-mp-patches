# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,3 +1,4 @@
+#version 2
 local keyBinds = {
 	shoot = "usetool",
 	switchCamera = "grab",
@@ -24,112 +25,6 @@
 	dPadDown = "scroll_down",
 }
 
-function init()
-	RegisterTool("cresta-drone", "High Tech Drone", "MOD/vox/remote.vox", 2)
-	SetBool("game.tool.cresta-drone.enabled", true)
-	SetString("game.tool.cresta-drone.ammo.display","")
-	SetFloat("game.tool.cresta-drone.ammo", 101)
-
-	if GetInt("game.fire.maxcount") < 1000 then
-		SetInt("game.fire.maxcount", 1000)
-	end
-
-	if not HasKey("savegame.mod.gun-type") then
-		SetInt("savegame.mod.gun-type", 5)
-	end
-	if not HasKey("savegame.mod.drone-speed") then
-		SetInt("savegame.mod.drone-speed", 40)
-	end
-	if not HasKey("savegame.mod.volume") then
-		SetInt("savegame.mod.volume", 50)
-	end
-	if not HasKey("savegame.mod.shots-fired") then
-		SetInt("savegame.mod.shots-fired", 0)
-	end
-	if not HasKey("savegame.mod.show-controls") then
-		SetBool("savegame.mod.show-controls", true)
-	end
-
-	DroneGunTypes = {
-		[1] = "Machine Gun",
-		[2] = "Rocket Launcher",
-		[3]	= "Bombs",
-		[4] = "Flamethrower",
-		[5] = "Grapple Hook",
-		[6]	= "Magnet"
-	}
-
-	ToolActive = false
-	FlyCamOn = false
-	DroneEnabled = false
-	SettingsOpen = false
-	IsFiring = false
-	RopeHooked = false
-	MagnetActive = false
-
-	InteractiveAlpha = 0
-	SmoothMove = 0
-
-	ZoomLevel = 15
-	MaxZoom = 20
-	MinZoom = 3
-
-	ShotDelay = 0.08
-	LightTimer = 0
-	ShootTimer = 0
-
-	RotorSpeed = 0
-	DroneHeight = 10
-	AverageSurroundingHeight = 0
-	DroneVel = Vec()
-	DroneBarrelTip = Vec()
-	DroneTargetPos = Vec()
-	DroneBarrelTransform = Transform()
-	CamPos = {}
-	Barrel = {}
-	RopeInstance = {}
-	AllHitEntities = {}
-	HookedPos = Vec()
-	HookedShape = 0
-	FireHandler = {}
-
-	Reticle1 = LoadSprite("MOD/img/reticle1.png")
-
-	DroneGunSound = LoadSound("MOD/snd/gun0.ogg")
-	DroneRocketSound = LoadSound("MOD/snd/rocket.ogg")
-	DroneBombSound = LoadSound("MOD/snd/bomb.ogg")
-	DroneGrappleSound = LoadSound("MOD/snd/grapple.ogg")
-	DroneReelSound = LoadSound("MOD/snd/reel.ogg")
-	DroneSound = LoadLoop("MOD/snd/drone.ogg")
-	FireLoop = LoadLoop("MOD/snd/fireloop.ogg")
-
-	local lights = FindLights('', true)
-	for i=1, #lights do
-		local light = lights[i]
-		local trans = GetLightTransform(light)
-		local pos = trans.pos
-		local rot = trans.rot
-		if (
-			pos[1] == 0
-			and pos[2] == 0
-			and pos[3] == 0
-			and rot[1] == 0
-			and rot[2] == 0
-			and rot[3] == 0
-			and rot[4] == 1
-		) then
-			PlayerFlashlight = light
-			break
-		end
-	end
-
-	local showLargeUI = GetBool("game.largeui")
-	UiScaleUpFactor = 1.0
-    if showLargeUI then
-		UiScaleUpFactor = 1.3
-	end
-end
-
 local function aorb(a, b, d)
 	return (a and d or 0) - (b and d or 0)
 end
@@ -276,12 +171,12 @@
 	end
 	local camTrans = Transform(CamPos, Barrel.rot)
 	SetCameraTransform(camTrans, ZoomLevel <= 9 and ZoomLevel*10 or 90)
-	SetPlayerTransform(GetPlayerTransform())
-	SetPlayerVelocity(Vec())
+	SetPlayerTransform(playerId, GetPlayerTransform(playerId))
+	SetPlayerVelocity(playerId, Vec())
 end
 
 local function shootDrone()
-	if ShootTimer > 0 then
+	if ShootTimer ~= 0 then
 		return
 	end
 	local droneBarrelForwardPos = TransformToParentPoint(DroneBarrelTransform, Vec(0.05, 0.05, DroneGunType == 1 and -7 or -14))
@@ -295,7 +190,7 @@
 	local shotType = DroneGunType == 1 and "bullet" or "rocket"
 	Shoot(DroneBarrelTip, dir, shotType, 0.4, 500)
 	local shotsFired = GetInt("savegame.mod.shots-fired")
-	SetInt("savegame.mod.shots-fired", shotsFired + 1)
+	SetInt("savegame.mod.shots-fired", shotsFired + 1, true)
 
 	if DroneGunType == 1 then
 		PlaySound(DroneGunSound, DroneBarrelTip, DroneVolume)
@@ -308,7 +203,7 @@
 end
 
 local function dropBomb()
-	if ShootTimer > 0 then
+	if ShootTimer ~= 0 then
 		return
 	end
 	local droneTurretTransform = GetShapeWorldTransform(DroneTurretShape)
@@ -319,7 +214,7 @@
 	SetBodyVelocity(bomb[1], bombVel)
 
 	local shotsFired = GetInt("savegame.mod.shots-fired")
-	SetInt("savegame.mod.shots-fired", shotsFired + 1)
+	SetInt("savegame.mod.shots-fired", shotsFired + 1, true)
 
 	PlaySound(DroneBombSound, turretEndPos, DroneVolume)
 	ShootTimer = ShotDelay*4
@@ -327,7 +222,7 @@
 end
 
 local function shootFlamethrower()
-	if ShootTimer > 0 then
+	if ShootTimer ~= 0 then
 		return
 	end
 	local droneBarrelDir = TransformToParentPoint(DroneBarrelTransform, Vec(0, 0, -20))
@@ -378,7 +273,7 @@
 end
 
 local function droneMovement(dt)
-	local hoverPos = VecCopy(GetPlayerPos())
+	local hoverPos = VecCopy(GetPlayerPos(playerId))
 	local radius = clamp(10, 10, 10)
 	if not HoverAngle then HoverAngle = 0 end
 	HoverAngle = HoverAngle + dt*0.25
@@ -533,7 +428,7 @@
 end
 
 local function initDrone()
-	local droneInstance = Spawn("MOD/prefab/drone.xml", Transform(TransformToParentPoint(GetPlayerTransform(), Vec(0, 0.5, -2.5)), Quat()))
+	local droneInstance = Spawn("MOD/prefab/drone.xml", Transform(TransformToParentPoint(GetPlayerTransform(playerId), Vec(0, 0.5, -2.5)), Quat()))
 	DroneBody = droneInstance[1] --[[@as body_handle]]
 	DroneRotors = FindShapes("drone-rotor")
 	RotorJoints = FindJoints("drone-rotor-joint")
@@ -541,7 +436,7 @@
 	DroneTurretShape = FindShape("drone-turret")
 	DroneBarrelJoint = FindJoint("drone-barrel-joint")
 	DroneTurretJoint = FindJoint("drone-turret-joint")
-	DroneTargetPos = GetPlayerTransform().pos
+	DroneTargetPos = GetPlayerTransform(playerId).pos
 	DroneEnabled = true
 	RotorSpeed = 30
 end
@@ -555,172 +450,6 @@
 	jointMovement()
 	droneMovement(dt)
 	SetBodyVelocity(DroneBody, DroneVel)
-end
-
-function tick(dt)
-	if GetString("game.player.tool") == "cresta-drone" and GetPlayerVehicle() == 0 and not GetBool("game.player.grabbing") and not GetBool("game.map.enabled") then
-		if not DroneEnabled then
-			initDrone()
-		end
-		ToolActive = true
-		SetBool("game.input.locktool", FlyCamOn)
-		DroneGunType = GetInt("savegame.mod.gun-type")
-		DroneVolume = GetInt("savegame.mod.volume")/100
-		PlayLoop(DroneSound, GetBodyTransform(DroneBody).pos, DroneVolume-0.1)
-
-		AimPos, HitShape, ShootDistance = getAimPos(FlyCamOn and Barrel or GetCameraTransform())
-		DroneBarrelTransform = GetShapeWorldTransform(DroneBarrelShape)
-		DroneBarrelTip = TransformToParentPoint(DroneBarrelTransform, Vec(0, 0.05, -0.3))
-		Barrel.pos = TransformToParentPoint(GetBodyTransform(DroneBody), Vec(0, -0.25, -0.1))
-
-		jointMovement()
-		SetBodyVelocity(DroneBody, DroneVel)
-
-		if DroneGunType < 3 then
-			drawReticleSprite()
-		end
-
-		if SettingsOpen then
-			local fovScale = GetInt("options.gfx.fov")/90.0
-			local interactiveTransform = TransformToParentTransform(GetPlayerCameraTransform(), Transform(Vec(0.0, -0.2, -0.2/fovScale), QuatEuler(-5, 0, 0)))
-			local t = Transform()
-			if not ToolPos then ToolPos = interactiveTransform.pos end
-			t.pos = VecLerp(ToolPos, interactiveTransform.pos, InteractiveAlpha)
-			t.rot = QuatSlerp(ToolTrans.rot, interactiveTransform.rot, InteractiveAlpha)
-			SetBodyTransform(RemoteBody, t)
-		end
-
-		if InputPressed(keyBinds.pause) or InputPressed(keyBinds.map) then
-			if SettingsOpen then
-				SettingsOpen = false
-				SetPlayerScreen(0)
-				SetValue("InteractiveAlpha", 0, "bounce", 0.6)
-				for i=1, #RemoteEntities do
-					Delete(RemoteEntities[i])
-				end
-			end
-		end
-
-		if InputPressed(keyBinds.toggleSettings) and not GetBool("game.player.caninteract") and not GetBool("game.player.usevehicle") then
-			FlyCamOn = false
-			SettingsOpen = not SettingsOpen
-			if SettingsOpen then
-				spawnRemote()
-			else
-				despawnRemote()
-			end
-		end
-
-		if InputPressed(keyBinds.shoot) and DroneGunTypes[DroneGunType] == "Grapple Hook" and not SettingsOpen then
-			if RopeHooked then
-				RopeHooked = false
-				HookedShape = 0
-				destroyRope(RopeInstance)
-				PlaySound(DroneReelSound, DroneBarrelTip, DroneVolume)
-			else
-				local droneTurretTransform = GetShapeWorldTransform(DroneTurretShape)
-				local turretEndPos = TransformToParentPoint(droneTurretTransform, Vec(0.075, 0.1, 0.1))
-				RopeInstance = spawnRope(turretEndPos, AimPos)
-				if RopeInstance and HitShape then
-					HookedShape = HitShape
-					HitBody = GetShapeBody(HitShape)
-					local hookPos = TransformToLocalPoint(GetBodyTransform(HitBody), AimPos)
-					HookedPos = hookPos
-					getAllHitShapes()
-					RopeHooked = true
-					PlaySound(DroneGrappleSound, DroneBarrelTip, DroneVolume)
-				end
-			end
-		end
-
-		if InputPressed(keyBinds.switchCamera) and not GetBool("game.player.cangrab") and not SettingsOpen then FlyCamOn = not FlyCamOn end
-
-		if FlyCamOn then
-			flyCam()
-			controlDrone()
-			if InputPressed(keyBinds.switchWeapon) then
-				if DroneGunType == #DroneGunTypes then DroneGunType = 1 else DroneGunType = DroneGunType + 1 end
-				SetInt("savegame.mod.gun-type", DroneGunType)
-			end
-			SetBool("game.disablemap", true)
-			if PlayerFlashlight ~= 0 then
-				SetLightEnabled(PlayerFlashlight, false)
-			end
-		else
-			droneMovement(dt)
-			SetBool("game.disablemap", false)
-		end
-
-		local isFiring = InputDown(keyBinds.shoot) and not SettingsOpen and DroneGunTypes[DroneGunType] ~= "Grapple Hook"
-		if isFiring then
-			if RopeHooked then
-				destroyRope(RopeInstance)
-				RopeHooked = false
-				PlaySound(DroneReelSound, DroneBarrelTip, DroneVolume)
-			end
-			if DroneGunType < 3 then
- 				shootDrone()
-			elseif DroneGunTypes[DroneGunType] == "Flamethrower" then
-				shootFlamethrower()
-				PlayLoop(FireLoop, DroneBarrelTip, 0.25)
-			elseif DroneGunTypes[DroneGunType] == "Bombs" then
-				dropBomb()
-			elseif DroneGunTypes[DroneGunType] == "Magnet" then
-				magnet()
-			end
-		elseif MagnetActive then
-			MagnetActive = false
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			ToolTrans = GetBodyTransform(b)
-			ToolPos = TransformToParentPoint(ToolTrans, Vec(0, -0.4, -0.5))
-
-			if LightTimer > 0 then
-				PointLight(DroneBarrelTip, 1, 1, 1, 1)
-				LightTimer = LightTimer - dt
-			end
-
-			if ToolBody ~= b then
-				ToolBody = b
-				local shapes = GetBodyShapes(b)
-				ControlShape = shapes[1]
-				ControlTransform = GetShapeLocalTransform(ControlShape)
-			end
-
-			local ct = TransformCopy(ControlTransform)
-			ct.rot = QuatRotateQuat(ct.rot, QuatEuler(-25, 0, 0))
-			SetShapeLocalTransform(ControlShape, ct)
-		end
-	else
-		if ToolActive then ToolActive = false end
-	end
-
-	if DroneEnabled and GetBool("savegame.mod.keep-alive") and not ToolActive then
-		droneTick(dt)
-	end
-
-	if DroneEnabled and ShootTimer > 0 then
-		ShootTimer = ShootTimer - dt
-	end
-
-	if DroneEnabled and #FireHandler > 0 then
-		for i=1, #FireHandler do
-			if FireHandler[i].aliveTimer < 0.1 then
-				Delete(FireHandler[i].body)
-				table.remove(FireHandler, i)
-				return
-			end
-			if FireHandler[i].aliveTimer > 0 then
-				FireHandler[i].aliveTimer = FireHandler[i].aliveTimer - dt
-			end
-			local fireBody = FireHandler[i].body
-			local fireTransform = GetBodyTransform(fireBody)
-			SpawnFire(fireTransform.pos)
-			spawnFireParticles(fireTransform.pos, Vec(0, 1, 0), 3, 0.5, "ground")
-		end
-	end
 end
 
 local function hoverUpright()
@@ -741,28 +470,6 @@
 		local spinVel = f/15
 		ConstrainAngularVelocity(DroneBody, 0, axes[a], v, -f , f)
 		ConstrainAngularVelocity(DroneBody, 0, axes[2], v, -spinVel , spinVel)
-	end
-end
-
-function update(dt)
-	if GetString("game.player.tool") == "cresta-drone" and DroneEnabled and (ToolActive or GetBool("savegame.mod.keep-alive")) then
-		local droneTransform = GetBodyTransform(DroneBody)
-		if FlyCamOn then
-			local vel = VecSub(DroneTargetPos, droneTransform.pos)
-			vel = VecScale(vel, SmoothMove)
-			local vecLength = VecLength(vel)
-			if vecLength < 0.35 then
-				vel = Vec(0, 0.35, 0)
-			end
-			DroneVel = vel
-			RotorSpeed = clamp(RotorSpeed + (vecLength*20 - RotorSpeed) * 0.9, 30, 300)
-		else
-			local acc = VecSub(DroneTargetPos, droneTransform.pos)
-			DroneVel = VecAdd(DroneVel, VecScale(acc, dt))
-			DroneVel = VecScale(DroneVel, 0.98)
-		end
-
-		hoverUpright()
 	end
 end
 
@@ -891,20 +598,309 @@
 	UiPop()
 end
 
-function draw()
-	if GetString("game.player.tool") == "cresta-drone" and GetPlayerVehicle() == 0 then
-		if GetBool("savegame.mod.show-controls") then
-			drawDroneControls()
-		end
-		drawDroneGunType()
-		if FlyCamOn and GetBool("savegame.mod.show-crosshair") then
-			UiPush()
-				UiTranslate(UiCenter(), UiMiddle())
-				UiColor(1, 1, 1, 0.5)
-				UiAlign("center middle")
-				UiImage("MOD/img/crosshair.png")
-			UiPop()
-		end
-
-	end
-end+function server.init()
+    RegisterTool("cresta-drone", "High Tech Drone", "MOD/vox/remote.vox", 2)
+    SetBool("game.tool.cresta-drone.enabled", true, true)
+    SetString("game.tool.cresta-drone.ammo.display","", true)
+    SetFloat("game.tool.cresta-drone.ammo", 101, true)
+    if GetInt("game.fire.maxcount") < 1000 then
+    	SetInt("game.fire.maxcount", 1000, true)
+    end
+    if not HasKey("savegame.mod.gun-type") then
+    	SetInt("savegame.mod.gun-type", 5, true)
+    end
+    if not HasKey("savegame.mod.drone-speed") then
+    	SetInt("savegame.mod.drone-speed", 40, true)
+    end
+    if not HasKey("savegame.mod.volume") then
+    	SetInt("savegame.mod.volume", 50, true)
+    end
+    if not HasKey("savegame.mod.shots-fired") then
+    	SetInt("savegame.mod.shots-fired", 0, true)
+    end
+    if not HasKey("savegame.mod.show-controls") then
+    	SetBool("savegame.mod.show-controls", true, true)
+    end
+    DroneGunTypes = {
+    	[1] = "Machine Gun",
+    	[2] = "Rocket Launcher",
+    	[3]	= "Bombs",
+    	[4] = "Flamethrower",
+    	[5] = "Grapple Hook",
+    	[6]	= "Magnet"
+    }
+    ToolActive = false
+    FlyCamOn = false
+    DroneEnabled = false
+    SettingsOpen = false
+    IsFiring = false
+    RopeHooked = false
+    MagnetActive = false
+    InteractiveAlpha = 0
+    SmoothMove = 0
+    ZoomLevel = 15
+    MaxZoom = 20
+    MinZoom = 3
+    ShotDelay = 0.08
+    LightTimer = 0
+    ShootTimer = 0
+    RotorSpeed = 0
+    DroneHeight = 10
+    AverageSurroundingHeight = 0
+    DroneVel = Vec()
+    DroneBarrelTip = Vec()
+    DroneTargetPos = Vec()
+    DroneBarrelTransform = Transform()
+    CamPos = {}
+    Barrel = {}
+    RopeInstance = {}
+    AllHitEntities = {}
+    HookedPos = Vec()
+    HookedShape = 0
+    FireHandler = {}
+    Reticle1 = LoadSprite("MOD/img/reticle1.png")
+    DroneSound = LoadLoop("MOD/snd/drone.ogg")
+    FireLoop = LoadLoop("MOD/snd/fireloop.ogg")
+    local lights = FindLights('', true)
+    for i=1, #lights do
+    	local light = lights[i]
+    	local trans = GetLightTransform(light)
+    	local pos = trans.pos
+    	local rot = trans.rot
+    	if (
+    		pos[1] == 0
+    		and pos[2] == 0
+    		and pos[3] == 0
+    		and rot[1] == 0
+    		and rot[2] == 0
+    		and rot[3] == 0
+    		and rot[4] == 1
+    	) then
+    		PlayerFlashlight = light
+    		break
+    	end
+    end
+    local showLargeUI = GetBool("game.largeui")
+    UiScaleUpFactor = 1.0
+       if showLargeUI then
+    	UiScaleUpFactor = 1.3
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetString("game.player.tool") == "cresta-drone" and DroneEnabled and (ToolActive or GetBool("savegame.mod.keep-alive")) then
+        	local droneTransform = GetBodyTransform(DroneBody)
+        	if FlyCamOn then
+        		local vel = VecSub(DroneTargetPos, droneTransform.pos)
+        		vel = VecScale(vel, SmoothMove)
+        		local vecLength = VecLength(vel)
+        		if vecLength < 0.35 then
+        			vel = Vec(0, 0.35, 0)
+        		end
+        		DroneVel = vel
+        		RotorSpeed = clamp(RotorSpeed + (vecLength*20 - RotorSpeed) * 0.9, 30, 300)
+        	else
+        		local acc = VecSub(DroneTargetPos, droneTransform.pos)
+        		DroneVel = VecAdd(DroneVel, VecScale(acc, dt))
+        		DroneVel = VecScale(DroneVel, 0.98)
+        	end
+
+        	hoverUpright()
+        end
+    end
+end
+
+function client.init()
+    DroneGunSound = LoadSound("MOD/snd/gun0.ogg")
+    DroneRocketSound = LoadSound("MOD/snd/rocket.ogg")
+    DroneBombSound = LoadSound("MOD/snd/bomb.ogg")
+    DroneGrappleSound = LoadSound("MOD/snd/grapple.ogg")
+    DroneReelSound = LoadSound("MOD/snd/reel.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "cresta-drone" and GetPlayerVehicle(playerId) == 0 and not GetBool("game.player.grabbing") and not GetBool("game.map.enabled") then
+    	if not DroneEnabled then
+    		initDrone()
+    	end
+    	ToolActive = true
+    	SetBool("game.input.locktool", FlyCamOn, true)
+    	DroneGunType = GetInt("savegame.mod.gun-type")
+    	DroneVolume = GetInt("savegame.mod.volume")/100
+    	PlayLoop(DroneSound, GetBodyTransform(DroneBody).pos, DroneVolume-0.1)
+
+    	AimPos, HitShape, ShootDistance = getAimPos(FlyCamOn and Barrel or GetCameraTransform())
+    	DroneBarrelTransform = GetShapeWorldTransform(DroneBarrelShape)
+    	DroneBarrelTip = TransformToParentPoint(DroneBarrelTransform, Vec(0, 0.05, -0.3))
+    	Barrel.pos = TransformToParentPoint(GetBodyTransform(DroneBody), Vec(0, -0.25, -0.1))
+
+    	jointMovement()
+    	SetBodyVelocity(DroneBody, DroneVel)
+
+    	if DroneGunType < 3 then
+    		drawReticleSprite()
+    	end
+
+    	if SettingsOpen then
+    		local fovScale = GetInt("options.gfx.fov")/90.0
+    		local interactiveTransform = TransformToParentTransform(GetPlayerCameraTransform(playerId), Transform(Vec(0.0, -0.2, -0.2/fovScale), QuatEuler(-5, 0, 0)))
+    		local t = Transform()
+    		if not ToolPos then ToolPos = interactiveTransform.pos end
+    		t.pos = VecLerp(ToolPos, interactiveTransform.pos, InteractiveAlpha)
+    		t.rot = QuatSlerp(ToolTrans.rot, interactiveTransform.rot, InteractiveAlpha)
+    		SetBodyTransform(RemoteBody, t)
+    	end
+
+    	if InputPressed(keyBinds.pause) or InputPressed(keyBinds.map) then
+    		if SettingsOpen then
+    			SettingsOpen = false
+    			SetPlayerScreen(0)
+    			SetValue("InteractiveAlpha", 0, "bounce", 0.6)
+    			for i=1, #RemoteEntities do
+    				Delete(RemoteEntities[i])
+    			end
+    		end
+    	end
+
+    	if InputPressed(keyBinds.toggleSettings) and not GetBool("game.player.caninteract") and not GetBool("game.player.usevehicle") then
+    		FlyCamOn = false
+    		SettingsOpen = not SettingsOpen
+    		if SettingsOpen then
+    			spawnRemote()
+    		else
+    			despawnRemote()
+    		end
+    	end
+
+    	if InputPressed(keyBinds.shoot) and DroneGunTypes[DroneGunType] == "Grapple Hook" and not SettingsOpen then
+    		if RopeHooked then
+    			RopeHooked = false
+    			HookedShape = 0
+    			destroyRope(RopeInstance)
+    			PlaySound(DroneReelSound, DroneBarrelTip, DroneVolume)
+    		else
+    			local droneTurretTransform = GetShapeWorldTransform(DroneTurretShape)
+    			local turretEndPos = TransformToParentPoint(droneTurretTransform, Vec(0.075, 0.1, 0.1))
+    			RopeInstance = spawnRope(turretEndPos, AimPos)
+    			if RopeInstance and HitShape then
+    				HookedShape = HitShape
+    				HitBody = GetShapeBody(HitShape)
+    				local hookPos = TransformToLocalPoint(GetBodyTransform(HitBody), AimPos)
+    				HookedPos = hookPos
+    				getAllHitShapes()
+    				RopeHooked = true
+    				PlaySound(DroneGrappleSound, DroneBarrelTip, DroneVolume)
+    			end
+    		end
+    	end
+
+    	if InputPressed(keyBinds.switchCamera) and not GetBool("game.player.cangrab") and not SettingsOpen then FlyCamOn = not FlyCamOn end
+
+    	if FlyCamOn then
+    		flyCam()
+    		controlDrone()
+    		if InputPressed(keyBinds.switchWeapon) then
+    			if DroneGunType == #DroneGunTypes then DroneGunType = 1 else DroneGunType = DroneGunType + 1 end
+    			SetInt("savegame.mod.gun-type", DroneGunType, true)
+    		end
+    		SetBool("game.disablemap", true, true)
+    		if PlayerFlashlight ~= 0 then
+    			SetLightEnabled(PlayerFlashlight, false)
+    		end
+    	else
+    		droneMovement(dt)
+    		SetBool("game.disablemap", false, true)
+    	end
+
+    	local isFiring = InputDown(keyBinds.shoot) and not SettingsOpen and DroneGunTypes[DroneGunType] ~= "Grapple Hook"
+    	if isFiring then
+    		if RopeHooked then
+    			destroyRope(RopeInstance)
+    			RopeHooked = false
+    			PlaySound(DroneReelSound, DroneBarrelTip, DroneVolume)
+    		end
+    		if DroneGunType < 3 then
+    				shootDrone()
+    		elseif DroneGunTypes[DroneGunType] == "Flamethrower" then
+    			shootFlamethrower()
+    			PlayLoop(FireLoop, DroneBarrelTip, 0.25)
+    		elseif DroneGunTypes[DroneGunType] == "Bombs" then
+    			dropBomb()
+    		elseif DroneGunTypes[DroneGunType] == "Magnet" then
+    			magnet()
+    		end
+    	elseif MagnetActive then
+    		MagnetActive = false
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		ToolTrans = GetBodyTransform(b)
+    		ToolPos = TransformToParentPoint(ToolTrans, Vec(0, -0.4, -0.5))
+
+    		if LightTimer ~= 0 then
+    			PointLight(DroneBarrelTip, 1, 1, 1, 1)
+    			LightTimer = LightTimer - dt
+    		end
+
+    		if ToolBody ~= b then
+    			ToolBody = b
+    			local shapes = GetBodyShapes(b)
+    			ControlShape = shapes[1]
+    			ControlTransform = GetShapeLocalTransform(ControlShape)
+    		end
+
+    		local ct = TransformCopy(ControlTransform)
+    		ct.rot = QuatRotateQuat(ct.rot, QuatEuler(-25, 0, 0))
+    		SetShapeLocalTransform(ControlShape, ct)
+    	end
+    else
+    	if ToolActive then ToolActive = false end
+    end
+
+    if DroneEnabled and GetBool("savegame.mod.keep-alive") and not ToolActive then
+    	droneTick(dt)
+    end
+
+    if DroneEnabled and ShootTimer ~= 0 then
+    	ShootTimer = ShootTimer - dt
+    end
+
+    if DroneEnabled and #FireHandler ~= 0 then
+    	for i=1, #FireHandler do
+    		if FireHandler[i].aliveTimer < 0.1 then
+    			Delete(FireHandler[i].body)
+    			table.remove(FireHandler, i)
+    			return
+    		end
+    		if FireHandler[i].aliveTimer ~= 0 then
+    			FireHandler[i].aliveTimer = FireHandler[i].aliveTimer - dt
+    		end
+    		local fireBody = FireHandler[i].body
+    		local fireTransform = GetBodyTransform(fireBody)
+    		SpawnFire(fireTransform.pos)
+    		spawnFireParticles(fireTransform.pos, Vec(0, 1, 0), 3, 0.5, "ground")
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "cresta-drone" and GetPlayerVehicle(playerId) == 0 then
+    	if GetBool("savegame.mod.show-controls") then
+    		drawDroneControls()
+    	end
+    	drawDroneGunType()
+    	if FlyCamOn and GetBool("savegame.mod.show-crosshair") then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiMiddle())
+    			UiColor(1, 1, 1, 0.5)
+    			UiAlign("center middle")
+    			UiImage("MOD/img/crosshair.png")
+    		UiPop()
+    	end
+
+    end
+end
+

```

---

# Migration Report: prefab\remotescreen.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/prefab\remotescreen.lua
+++ patched/prefab\remotescreen.lua
@@ -1,3 +1,4 @@
+#version 2
 local optionKeys = {
 	gunType = "gun-type",
 	showCrosshair = "show-crosshair",
@@ -6,7 +7,6 @@
 	droneSpeed = "drone-speed",
 	showControls = "show-controls"
 }
-
 local drone_guntypes = {
 	[1] = "Machine Gun",
 	[2] = "Rocket Launcher",
@@ -32,7 +32,7 @@
 		UiTranslate(140, 0)
 		UiFont("regular.ttf", 40)
 		UiText(val --[[@as string]])
-		SetInt("savegame.mod."..key, val)
+		SetInt("savegame.mod."..key, val, true)
 	UiPop()
 end
 
@@ -46,12 +46,12 @@
 		if value then
 			if UiTextButton("Enabled", 100, 32) then
 				value = false
-				SetBool("savegame.mod."..key, value)
+				SetBool("savegame.mod."..key, value, true)
 			end
 		else
 			if UiTextButton("Disabled", 100, 32) then
 				value = true
-				SetBool("savegame.mod."..key, value)
+				SetBool("savegame.mod."..key, value, true)
 			end
 		end
 	UiPop()
@@ -69,54 +69,53 @@
 			if value > #values then
 				value = 1
 			end
-			SetInt("savegame.mod."..key, value)
+			SetInt("savegame.mod."..key, value, true)
 		end
 	UiPop()
 end
 
-function init()
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        RemoteScreen = UiGetScreen()
+           ScreenName = GetTagValue(RemoteScreen, "name")
+    end
 end
 
-function tick()
-	RemoteScreen = UiGetScreen()
-    ScreenName = GetTagValue(RemoteScreen, "name")
+function client.draw()
+    if RemoteScreen ~= 0 and ScreenName == "remotescreen" then
+    	UiTranslate(UiCenter(), 50)
+    	UiAlign("center middle")
+    	UiColor(1,1,1)
+    	UiFont("bold.ttf", 48)
+    	UiText("Drone Settings")
+    	UiTranslate(0, 60)
+
+    	UiPush()
+    		local info = {}
+    		info[#info+1] = {"Gun Type", toggleMultiButton(optionKeys.gunType, drone_guntypes, #info)}
+    		info[#info+1] = {"Crosshair", toggleBoolButton(optionKeys.showCrosshair, #info)}
+    		info[#info+1] = {"Keep drone alive", toggleBoolButton(optionKeys.keepAlive, #info)}
+    		info[#info+1] = {"Display Controls", toggleBoolButton(optionKeys.showControls, #info)}
+    		info[#info+1] = {"Drone Speed", optionsSlider(optionKeys.droneSpeed, 20, 100, #info)}
+    		info[#info+1] = {"Drone Volume", optionsSlider(optionKeys.volume, 0, 100, #info)}
+    		info[#info+1] = {"Total shots fired", GetInt("savegame.mod.shots-fired")}
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiPush()
+    				UiColor(1,1,1)
+    				UiFont("bold.ttf", 32)
+    				UiAlign("right")
+    				UiText(key)
+    				UiTranslate(10, 0)
+    				UiColor(0.2, 0.6, 1)
+    				UiAlign("left")
+    				UiFont("regular.ttf", 32)
+    				UiText(func)
+    			UiPop()
+    			UiTranslate(0, 40)
+    		end
+    	UiPop()
+    end
 end
 
-function draw()
-	if RemoteScreen ~= 0 and ScreenName == "remotescreen" then
-		UiTranslate(UiCenter(), 50)
-		UiAlign("center middle")
-		UiColor(1,1,1)
-		UiFont("bold.ttf", 48)
-		UiText("Drone Settings")
-		UiTranslate(0, 60)
-
-		UiPush()
-			local info = {}
-			info[#info+1] = {"Gun Type", toggleMultiButton(optionKeys.gunType, drone_guntypes, #info)}
-			info[#info+1] = {"Crosshair", toggleBoolButton(optionKeys.showCrosshair, #info)}
-			info[#info+1] = {"Keep drone alive", toggleBoolButton(optionKeys.keepAlive, #info)}
-			info[#info+1] = {"Display Controls", toggleBoolButton(optionKeys.showControls, #info)}
-			info[#info+1] = {"Drone Speed", optionsSlider(optionKeys.droneSpeed, 20, 100, #info)}
-			info[#info+1] = {"Drone Volume", optionsSlider(optionKeys.volume, 0, 100, #info)}
-			info[#info+1] = {"Total shots fired", GetInt("savegame.mod.shots-fired")}
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiPush()
-					UiColor(1,1,1)
-					UiFont("bold.ttf", 32)
-					UiAlign("right")
-					UiText(key)
-					UiTranslate(10, 0)
-					UiColor(0.2, 0.6, 1)
-					UiAlign("left")
-					UiFont("regular.ttf", 32)
-					UiText(func)
-				UiPop()
-				UiTranslate(0, 40)
-			end
-		UiPop()
-	end
-end
-

```
