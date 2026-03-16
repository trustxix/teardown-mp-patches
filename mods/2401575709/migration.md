# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,97 +1,4 @@
-airstrikeprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active=false,
-		aliveTimer = 0
-	}
-}
-
-function init()
-	RegisterTool("airstrike", "Air Strike", "MOD/vox/airstrike.vox")
-	SetBool("game.tool.airstrike.enabled", true)
-	SetString("game.tool.airstrike.ammo.display","")
-	SetFloat("game.tool.airstrike.ammo", 101)
-	if GetInt("game.fire.maxcount") < 1000 then
-		SetInt("game.fire.maxcount", 1000)
-	end
-
-	nocd = GetBool("savegame.mod.nocd")
-
-	for i=1, 500 do
-		airstrikeprojectileHandler.shells[i] = deepcopy(airstrikeprojectileHandler.defaultShell)
-	end
-
-	fogStart, fogEnd, fogAmount, fogExp = GetEnvironmentProperty("fogParams")
-	flyFogStart, flyFogEnd, flyFogAmount, flyFogExp = 80, 300, 1, 5
-
-	fogChange = false
-	flycamenabled = false
-	airstrikeenabled = false
-	firing = false
-	radioactivated = false
-	
-	damage = 1
-	gravity = Vec(0, 0, 0)
-	clustergravity = Vec(0, -35, 0)
-	clusterAmount = 20
-	velocity = 0.6
-	shotDelay = 0.05
-
-	shockwave = {
-		strength = 3,
-		maxDist = 4,
-		maxMass = 2000
-	}
-
-	zoomlevel = 6
-	maxzoom = 12
-	minzoom = 0.5
-
-	lightTimer = 0
-	equipTimer = 0
-
-	selectedshell = 1
-	shoottimers = {}
-	for i=1, 7 do
-		shoottimers[i] = 0
-	end
-
-	shellsprites = {}
-	shellsprites[1] = LoadSprite("MOD/img/25mm.png")
-	shellsprites[2] = LoadSprite("MOD/img/40mm.png")
-	shellsprites[3] = LoadSprite("MOD/img/105mm.png")
-	shellsprites[4] = LoadSprite("MOD/img/cluster.png")
-
-	gunsounds = {}
-	gunsounds[1] = LoadLoop("MOD/snd/gun1.ogg")
-	gunsounds[2] = LoadSound("MOD/snd/gun2.ogg")
-	gunsounds[3] = LoadSound("MOD/snd/gun3.ogg")
-	planesound = LoadLoop("MOD/snd/planeloop.ogg")
-
-	splashsound = LoadSound("MOD/snd/splash0.ogg")
-	firesound = LoadSound("MOD/snd/fire0.ogg")
-
-	fireloop = LoadLoop("MOD/snd/fireloop.ogg")
-	waterloop = LoadLoop("MOD/snd/water.ogg")
-
-	explosionsounds = {}
-	explosionsounds[1] = LoadSound("explosion/s0.ogg")
-
-	switchsound = LoadSound("MOD/snd/switch.ogg")
-	beepsound = LoadSound("MOD/snd/radiobeep.ogg")
-
-	plane = {}
-	plane.pos = Vec(0, 0 ,0)
-	plane.rot = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0))
-
-	plane.barrel = {}
-	plane.barrel.rot = Quat()
-
-	plane.pos[2] = 100
-	plane.pos[1] = plane.pos[1] + 100
-end
-
+#version 2
 function clamp(value, mi, ma)
 	if value < mi then value = mi end
 	if value > ma then value = ma end
@@ -289,7 +196,7 @@
 
 	local newT = Transform(plane.barrel.pos, CameraRot)
 	SetCameraTransform(newT, zoomlevel*10)
-	SetPlayerTransform(GetPlayerTransform())
+	SetPlayerTransform(playerId, GetPlayerTransform(playerId))
 	PlayLoop(planesound, GetCameraTransform().pos, 0.5)
 end
 
@@ -436,215 +343,291 @@
     projectile.pos = point2
 end
 
-function tick(dt)
-	for key, shell in ipairs(airstrikeprojectileHandler.shells) do
-		if shell.type == 5 and shell.aliveTimer > 0 then
-			shell.aliveTimer = shell.aliveTimer - dt
-			if shell.aliveTimer < 0.1 then
-				Delete(shell.voxBody)
-				shell.aliveTimer = 0
-			end
-		end
-
-		if shell.active then
-			ProjectileOperations(shell, dt)
-		end
-	end
-
-	if GetString("game.player.tool") == "airstrike" and GetPlayerVehicle() == 0 then
-		SetBool("game.input.locktool", flycamenabled)
-		firing = InputDown("usetool")
-		airstrikeenabled = true
-		if equipTimer < 1 then
-			equipTimer = equipTimer + dt * 2
-		end
-
-		if firing then
-			Shoot()
-			if selectedshell == 1 then PlayLoop(gunsounds[selectedshell], plane.barrel.pos, 0.4) end
-			if selectedshell == 5 or selectedshell == 7 then PlayLoop(fireloop, plane.barrel.pos, 0.2) end
-			if selectedshell == 6 then PlayLoop(waterloop, plane.barrel.pos, 0.8) end
-		end
-
-		if InputPressed("R") then
-			PlaySound(switchsound, GetCameraTransform().pos, 0.4)
-			if selectedshell == 7 then selectedshell = 1 else selectedshell = selectedshell + 1 end
-		end
-
-		if InputPressed("rmb") then 
-			flycamenabled = not flycamenabled
-			if flycamenabled then
-				fogChange = true
-				SetEnvironmentProperty("fogParams", flyFogStart, flyFogEnd, flyFogAmount, flyFogExp)
-			end
-		end
-		if InputPressed("esc") then flycamenabled = false end
-		if flycamenabled then 
-			FlyCam()
-		elseif fogChange then
-			fogChange = false
-			SetEnvironmentProperty("fogParams", fogStart, fogEnd, fogAmount, fogExp)
-		end
-
-		aimpos = flycamenabled and GetCamLookPos() or GetAimPos()
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.1))
-
-			if lightTimer > 0 then
-				PointLight(plane.barrel.pos, 1, 1, 1, 1)
-				lightTimer = lightTimer - dt
-			end
-
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				radioshape = shapes[1]
-				antennashape = shapes[2]
-				planeshape = shapes[3]
-				blinkshape = shapes[4]
-				radiotransformation = GetShapeLocalTransform(radioshape)
-				antennatransformation = GetShapeLocalTransform(antennashape)
-				planetransformation = GetShapeLocalTransform(planeshape)
-				blinktransformation = GetShapeLocalTransform(blinkshape)
-			end
-			
-			if equipTimer > 1 and not radioactivated then
-				PlaySound(beepsound, GetCameraTransform().pos, 0.4)
-				radioactivated = true
-			end
-
-			if radioactivated then
-				SetShapeEmissiveScale(radioshape, 0.5)
-			else
-				SetShapeEmissiveScale(radioshape, 0)
-			end
-
-			if InputDown("lmb") then
-				SetShapeEmissiveScale(blinkshape, 5)
-			else
-				SetShapeEmissiveScale(blinkshape, 0)
-			end
-
-			rt = TransformCopy(radiotransformation)
-			rt.rot = QuatRotateQuat(rt.rot, QuatEuler(0, 0, -15))
-			SetShapeLocalTransform(radioshape, rt)
-
-			bt = TransformCopy(blinktransformation)
-			bt.rot = QuatRotateQuat(bt.rot, QuatEuler(0, 0, -15))
-			SetShapeLocalTransform(blinkshape, bt)
-
-			at = TransformCopy(antennatransformation)
-			at.pos = VecAdd(at.pos, Vec(0, equipTimer*0.4, 0))
-			at.rot = QuatRotateQuat(at.rot, QuatEuler(0, 0, -15))
-			SetShapeLocalTransform(antennashape, at)
-
-			SetShapeLocalTransform(planeshape, TransformToLocalTransform(GetBodyTransform(GetToolBody()), plane))
-		end
-
-		planefwdpos = TransformToParentPoint(plane, Vec(-0.15, 0, 0))
-		planerotation = QuatRotateQuat(plane.rot, QuatEuler(0, 0, 0.1))
-		plane.pos = planefwdpos
-		plane.rot = planerotation
-		plane.barrel.pos = TransformToParentPoint(plane, Vec(2.5, 4.5, 0))
-	else
-		airstrikeenabled = false
-		radioactivated = false
-		flycamenabled = false
-		equipTimer = 0
-		if fogChange then
-			fogChange = false
-			SetEnvironmentProperty("fogParams", fogStart, fogEnd, fogAmount, fogExp)
-		end
-	end
-
-	for i=1, #shoottimers do
-		if shoottimers[i] > 0 then
-			shoottimers[i] = shoottimers[i] - dt
-		else
-			shoottimers[i] = 0
-		end
-	end
-end
-
-function draw()
-	if flycamenabled and GetPlayerVehicle() == 0 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiColor(1, 1, 1, 0.5)
-			UiAlign("center middle")
-			local crosshairid = selectedshell > 3 and 2 or selectedshell
-			UiImage("MOD/img/AC130crosshair"..crosshairid..".png")
-		UiPop()
-
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle()+UiMiddle()/2+50)
-			UiColor(1, 1, 1)
-			UiAlign("center")
-			UiFont("regular.ttf", 26)
-			if selectedshell ~= 3 or shoottimers[selectedshell] == 0 then
-				UiText("Ready")
-			else
-				UiText(tostring(math.ceil(shoottimers[selectedshell])))
-			end
-		UiPop()
-	end
-	if airstrikeenabled and GetPlayerVehicle() == 0 then
-		UiPush()
-			UiTranslate(80, UiMiddle()+UiMiddle()/2)
-			UiColor(0.4, 0.4, 0.4)
-			UiAlign("left")
-			UiFont("regular.ttf", 26)
-			UiTextOutline(0,0,0,1,0.2)
-
-			UiPush()
-				UiColor(1, 1, 1)
-				UiText("R: Change ammo")
-				UiTranslate(0, 30)
-				UiText("Right-Click: Plane-view")
-			UiPop()
-
-			UiTranslate(0, 70)
-			UiPush()
-				if selectedshell == 1 then UiColor(1, 1, 1) end
-				UiText("25mm")
-			UiPop()
-
-			UiTranslate(0, 30)
-			UiPush()
-				if selectedshell == 2 then UiColor(1, 1, 1) end
-				UiText("40mm")
-			UiPop()
-
-			UiTranslate(0, 30)
-			UiPush()
-				if selectedshell == 3 then UiColor(1, 1, 1) end
-				UiText("105mm")
-			UiPop()
-
-			UiTranslate(0, 30)
-			UiPush()
-				if selectedshell == 4 then UiColor(1, 1, 1) end
-				UiText("Cluster bomb")
-			UiPop()
-
-			UiTranslate(0, 30)
-			UiPush()
-				if selectedshell == 5 then UiColor(1, 1, 1) end
-				UiText("Napalm")
-			UiPop()
-			UiTranslate(0, 30)
-			UiPush()
-				if selectedshell == 6 then UiColor(1, 1, 1) end
-				UiText("Water Cannon")
-			UiPop()
-			UiTranslate(0, 30)
-			UiPush()
-				if selectedshell == 7 then UiColor(1, 1, 1) end
-				UiText("Acid")
-			UiPop()
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("airstrike", "Air Strike", "MOD/vox/airstrike.vox")
+    SetBool("game.tool.airstrike.enabled", true, true)
+    SetString("game.tool.airstrike.ammo.display","", true)
+    SetFloat("game.tool.airstrike.ammo", 101, true)
+    if GetInt("game.fire.maxcount") < 1000 then
+    	SetInt("game.fire.maxcount", 1000, true)
+    end
+    nocd = GetBool("savegame.mod.nocd")
+    for i=1, 500 do
+    	airstrikeprojectileHandler.shells[i] = deepcopy(airstrikeprojectileHandler.defaultShell)
+    end
+    fogStart, fogEnd, fogAmount, fogExp = GetEnvironmentProperty("fogParams")
+    flyFogStart, flyFogEnd, flyFogAmount, flyFogExp = 80, 300, 1, 5
+    fogChange = false
+    flycamenabled = false
+    airstrikeenabled = false
+    firing = false
+    radioactivated = false
+    damage = 1
+    gravity = Vec(0, 0, 0)
+    clustergravity = Vec(0, -35, 0)
+    clusterAmount = 20
+    velocity = 0.6
+    shotDelay = 0.05
+    shockwave = {
+    	strength = 3,
+    	maxDist = 4,
+    	maxMass = 2000
+    }
+    zoomlevel = 6
+    maxzoom = 12
+    minzoom = 0.5
+    lightTimer = 0
+    equipTimer = 0
+    selectedshell = 1
+    shoottimers = {}
+    for i=1, 7 do
+    	shoottimers[i] = 0
+    end
+    shellsprites = {}
+    shellsprites[1] = LoadSprite("MOD/img/25mm.png")
+    shellsprites[2] = LoadSprite("MOD/img/40mm.png")
+    shellsprites[3] = LoadSprite("MOD/img/105mm.png")
+    shellsprites[4] = LoadSprite("MOD/img/cluster.png")
+    gunsounds = {}
+    gunsounds[1] = LoadLoop("MOD/snd/gun1.ogg")
+    planesound = LoadLoop("MOD/snd/planeloop.ogg")
+    fireloop = LoadLoop("MOD/snd/fireloop.ogg")
+    waterloop = LoadLoop("MOD/snd/water.ogg")
+    explosionsounds = {}
+    plane = {}
+    plane.pos = Vec(0, 0 ,0)
+    plane.rot = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0))
+    plane.barrel = {}
+    plane.barrel.rot = Quat()
+    plane.pos[2] = 100
+    plane.pos[1] = plane.pos[1] + 100
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(airstrikeprojectileHandler.shells) do
+        	if shell.type == 5 and shell.aliveTimer ~= 0 then
+        		shell.aliveTimer = shell.aliveTimer - dt
+        		if shell.aliveTimer < 0.1 then
+        			Delete(shell.voxBody)
+        			shell.aliveTimer = 0
+        		end
+        	end
+
+        	if shell.active then
+        		ProjectileOperations(shell, dt)
+        	end
+        end
+    end
+end
+
+function client.init()
+    gunsounds[2] = LoadSound("MOD/snd/gun2.ogg")
+    gunsounds[3] = LoadSound("MOD/snd/gun3.ogg")
+    splashsound = LoadSound("MOD/snd/splash0.ogg")
+    firesound = LoadSound("MOD/snd/fire0.ogg")
+    explosionsounds[1] = LoadSound("explosion/s0.ogg")
+    switchsound = LoadSound("MOD/snd/switch.ogg")
+    beepsound = LoadSound("MOD/snd/radiobeep.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "airstrike" and GetPlayerVehicle(playerId) == 0 then
+    	SetBool("game.input.locktool", flycamenabled, true)
+    	firing = InputDown("usetool")
+    	airstrikeenabled = true
+    	if equipTimer < 1 then
+    		equipTimer = equipTimer + dt * 2
+    	end
+
+    	if firing then
+    		Shoot()
+    		if selectedshell == 1 then PlayLoop(gunsounds[selectedshell], plane.barrel.pos, 0.4) end
+    		if selectedshell == 5 or selectedshell == 7 then PlayLoop(fireloop, plane.barrel.pos, 0.2) end
+    		if selectedshell == 6 then PlayLoop(waterloop, plane.barrel.pos, 0.8) end
+    	end
+
+    	if InputPressed("R") then
+    		PlaySound(switchsound, GetCameraTransform().pos, 0.4)
+    		if selectedshell == 7 then selectedshell = 1 else selectedshell = selectedshell + 1 end
+    	end
+
+    	if InputPressed("rmb") then 
+    		flycamenabled = not flycamenabled
+    		if flycamenabled then
+    			fogChange = true
+    			SetEnvironmentProperty("fogParams", flyFogStart, flyFogEnd, flyFogAmount, flyFogExp)
+    		end
+    	end
+    	if InputPressed("esc") then flycamenabled = false end
+    	if flycamenabled then 
+    		FlyCam()
+    	elseif fogChange then
+    		fogChange = false
+    		SetEnvironmentProperty("fogParams", fogStart, fogEnd, fogAmount, fogExp)
+    	end
+
+    	aimpos = flycamenabled and GetCamLookPos() or GetAimPos()
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.1))
+
+    		if lightTimer ~= 0 then
+    			PointLight(plane.barrel.pos, 1, 1, 1, 1)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			radioshape = shapes[1]
+    			antennashape = shapes[2]
+    			planeshape = shapes[3]
+    			blinkshape = shapes[4]
+    			radiotransformation = GetShapeLocalTransform(radioshape)
+    			antennatransformation = GetShapeLocalTransform(antennashape)
+    			planetransformation = GetShapeLocalTransform(planeshape)
+    			blinktransformation = GetShapeLocalTransform(blinkshape)
+    		end
+
+    		if equipTimer > 1 and not radioactivated then
+    			PlaySound(beepsound, GetCameraTransform().pos, 0.4)
+    			radioactivated = true
+    		end
+
+    		if radioactivated then
+    			SetShapeEmissiveScale(radioshape, 0.5)
+    		else
+    			SetShapeEmissiveScale(radioshape, 0)
+    		end
+
+    		if InputDown("lmb") then
+    			SetShapeEmissiveScale(blinkshape, 5)
+    		else
+    			SetShapeEmissiveScale(blinkshape, 0)
+    		end
+
+    		rt = TransformCopy(radiotransformation)
+    		rt.rot = QuatRotateQuat(rt.rot, QuatEuler(0, 0, -15))
+    		SetShapeLocalTransform(radioshape, rt)
+
+    		bt = TransformCopy(blinktransformation)
+    		bt.rot = QuatRotateQuat(bt.rot, QuatEuler(0, 0, -15))
+    		SetShapeLocalTransform(blinkshape, bt)
+
+    		at = TransformCopy(antennatransformation)
+    		at.pos = VecAdd(at.pos, Vec(0, equipTimer*0.4, 0))
+    		at.rot = QuatRotateQuat(at.rot, QuatEuler(0, 0, -15))
+    		SetShapeLocalTransform(antennashape, at)
+
+    		SetShapeLocalTransform(planeshape, TransformToLocalTransform(GetBodyTransform(GetToolBody()), plane))
+    	end
+
+    	planefwdpos = TransformToParentPoint(plane, Vec(-0.15, 0, 0))
+    	planerotation = QuatRotateQuat(plane.rot, QuatEuler(0, 0, 0.1))
+    	plane.pos = planefwdpos
+    	plane.rot = planerotation
+    	plane.barrel.pos = TransformToParentPoint(plane, Vec(2.5, 4.5, 0))
+    else
+    	airstrikeenabled = false
+    	radioactivated = false
+    	flycamenabled = false
+    	equipTimer = 0
+    	if fogChange then
+    		fogChange = false
+    		SetEnvironmentProperty("fogParams", fogStart, fogEnd, fogAmount, fogExp)
+    	end
+    end
+
+    for i=1, #shoottimers do
+    	if shoottimers[i] > 0 then
+    		shoottimers[i] = shoottimers[i] - dt
+    	else
+    		shoottimers[i] = 0
+    	end
+    end
+end
+
+function client.draw()
+    if flycamenabled and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiColor(1, 1, 1, 0.5)
+    		UiAlign("center middle")
+    		local crosshairid = selectedshell > 3 and 2 or selectedshell
+    		UiImage("MOD/img/AC130crosshair"..crosshairid..".png")
+    	UiPop()
+
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle()+UiMiddle()/2+50)
+    		UiColor(1, 1, 1)
+    		UiAlign("center")
+    		UiFont("regular.ttf", 26)
+    		if selectedshell ~= 3 or shoottimers[selectedshell] == 0 then
+    			UiText("Ready")
+    		else
+    			UiText(tostring(math.ceil(shoottimers[selectedshell])))
+    		end
+    	UiPop()
+    end
+    if airstrikeenabled and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+    		UiTranslate(80, UiMiddle()+UiMiddle()/2)
+    		UiColor(0.4, 0.4, 0.4)
+    		UiAlign("left")
+    		UiFont("regular.ttf", 26)
+    		UiTextOutline(0,0,0,1,0.2)
+
+    		UiPush()
+    			UiColor(1, 1, 1)
+    			UiText("R: Change ammo")
+    			UiTranslate(0, 30)
+    			UiText("Right-Click: Plane-view")
+    		UiPop()
+
+    		UiTranslate(0, 70)
+    		UiPush()
+    			if selectedshell == 1 then UiColor(1, 1, 1) end
+    			UiText("25mm")
+    		UiPop()
+
+    		UiTranslate(0, 30)
+    		UiPush()
+    			if selectedshell == 2 then UiColor(1, 1, 1) end
+    			UiText("40mm")
+    		UiPop()
+
+    		UiTranslate(0, 30)
+    		UiPush()
+    			if selectedshell == 3 then UiColor(1, 1, 1) end
+    			UiText("105mm")
+    		UiPop()
+
+    		UiTranslate(0, 30)
+    		UiPush()
+    			if selectedshell == 4 then UiColor(1, 1, 1) end
+    			UiText("Cluster bomb")
+    		UiPop()
+
+    		UiTranslate(0, 30)
+    		UiPush()
+    			if selectedshell == 5 then UiColor(1, 1, 1) end
+    			UiText("Napalm")
+    		UiPop()
+    		UiTranslate(0, 30)
+    		UiPush()
+    			if selectedshell == 6 then UiColor(1, 1, 1) end
+    			UiText("Water Cannon")
+    		UiPop()
+    		UiTranslate(0, 30)
+    		UiPush()
+    			if selectedshell == 7 then UiColor(1, 1, 1) end
+    			UiText("Acid")
+    		UiPop()
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
@@ -1,42 +1,4 @@
-function init()
-	nocd = GetBool("savegame.mod.nocd")
-	if nocd == 0 then nocd = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("AC-130 Airtstrike")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("No Cooldown")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if nocd then
-			if UiTextButton("Yes", 20, 20) then
-				nocd = false
-				SetBool("savegame.mod.nocd", nocd)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				nocd = true
-				SetBool("savegame.mod.nocd", nocd)
-			end
-		end
-	UiPop()
-
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -55,4 +17,44 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    nocd = GetBool("savegame.mod.nocd")
+    if nocd == 0 then nocd = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("AC-130 Airtstrike")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("No Cooldown")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if nocd then
+    		if UiTextButton("Yes", 20, 20) then
+    			nocd = false
+    			SetBool("savegame.mod.nocd", nocd, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			nocd = true
+    			SetBool("savegame.mod.nocd", nocd, true)
+    		end
+    	end
+    UiPop()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```
