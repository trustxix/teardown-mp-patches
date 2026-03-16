# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,44 +1,4 @@
-magnumprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("500magnum", "500 Magnum", "MOD/vox/magnum.vox")
-	SetBool("game.tool.500magnum.enabled", true)
-	SetString("game.tool.500magnum.ammo.display","")
-	SetFloat("game.tool.500magnum.ammo", 10000000)
-
-	damage = 1.2
-	penetration = 4
-	gravity = Vec(0, 0, 0)
-	velocity = 1.7
-	reloadTime = 1.5
-	shotDelay = 0.4
-	ammo = 5
-	mags = 10
-	angle = 0
-	angVel = 0
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	for i=1, 15 do
-		magnumprojectileHandler.shells[i] = deepcopy(magnumprojectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-
-	gunsound = LoadSound("snd/magnum0.ogg")
-	cocksound = LoadSound("snd/magnumcock.ogg")
-	reloadsound = LoadSound("snd/magnumreload.ogg")
-	casingsound = LoadSound("snd/magnumcase.ogg")
-	dryfiresound = LoadSound("snd/dryfire.ogg")
-	refillsound = LoadSound("snd/refill.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -100,15 +60,15 @@
 	end
 
 	local recoildir = TransformToParentVec(ct, Vec(0, 0, 5))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local oldvel = VecCopy(vel)
 	vel = VecAdd(vel, recoildir)
 	if VecLength(vel) > 10 then vel = oldvel end
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.15)
 	SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.35, 0.8)
-	PlaySound(gunsound, GetPlayerTransform().pos, 0.9, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.9, false)
 	if not unlimitedammo then
 		ammo = ammo - 1
 	end
@@ -143,127 +103,163 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
-	PlaySound(casingsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
+	PlaySound(casingsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "500magnum" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			if not reloading then
-				if mags == 0 or ammo == 0 then
-					PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-				else
-					Shoot(false)
-				end
-			end
-		end
-
-		if InputDown("rmb") then
-			if not reloading then
-				Shoot(true)
-			end
-		end
-
-		SetBool("hud.aimdot", false)
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.1, 0.1, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.65, -2.4))
-
-			if recoilTimer > 0 then
-				PointLight(toolPos, 1, 1, 1, 1)
-
-				local t = Transform()
-				t.pos = Vec(0.1, 0.1, recoilTimer*3)
-				t.rot = QuatEuler(recoilTimer*100, 0, 0)
-				SetToolTransform(t)
-				angVel = 2.5
-				recoilTimer = recoilTimer - dt
-			else
-				angVel = 0
-			end
-
-			if reloading then
-				angVel = -10
-			end
-
-			angle = angle + angVel
-			
-			local voxSize = 0.1
-			local attach = Transform(Vec(2.75*voxSize, -6.3*voxSize, 0))
-			if body ~= b then
-				body = b
-				-- Barrel is the second shape in vox file. Remember original position in attachment frame
-				local shapes = GetBodyShapes(b)
-				barrel = shapes[2]
-				barrelTransform = TransformToLocalTransform(attach, GetShapeLocalTransform(barrel))	
-			end
-
-			attach.rot = QuatEuler(0, 0, -angle)
-			t = TransformToParentTransform(attach, barrelTransform)
-			SetShapeLocalTransform(barrel, t)
-		end
-
-		if not unlimitedammo then
-			if ammo < 5 and mags > 1 and InputPressed("R") then
-				Reload()
-			end
-			
-			if GetBool("ammobox.refill") then
-				SetBool("ammobox.refill", false)
-				mags = mags + 1
-				PlaySound(refillsound, GetPlayerTransform().pos, 1, false)
-			end
-
-			if reloading then
-				reloadTimer = reloadTimer - dt
-				if reloadTimer < 0 then
-					ammo = 5
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(magnumprojectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
-			end
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "500magnum" and GetPlayerVehicle() == 0 then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle")
-			UiImage("MOD/img/crosshair1.png")
-		UiPop()
-		if not unlimitedammo then
-			UiPush()
-				UiTranslate(UiCenter(), UiHeight()-60)
-				UiAlign("center middle")
-				UiColor(1, 1, 1)
-				UiFont("bold.ttf", 32)
-				UiTextOutline(0,0,0,1,0.1)
-				if reloading then
-					UiText("Reloading")
-				else
-					UiText(ammo.."/"..5*math.max(0, mags-1))
-				end
-			UiPop()
-		end
-	end
-end+function server.init()
+    RegisterTool("500magnum", "500 Magnum", "MOD/vox/magnum.vox")
+    SetBool("game.tool.500magnum.enabled", true, true)
+    SetString("game.tool.500magnum.ammo.display","", true)
+    SetFloat("game.tool.500magnum.ammo", 10000000, true)
+    damage = 1.2
+    penetration = 4
+    gravity = Vec(0, 0, 0)
+    velocity = 1.7
+    reloadTime = 1.5
+    shotDelay = 0.4
+    ammo = 5
+    mags = 10
+    angle = 0
+    angVel = 0
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    for i=1, 15 do
+    	magnumprojectileHandler.shells[i] = deepcopy(magnumprojectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+end
+
+function client.init()
+    gunsound = LoadSound("snd/magnum0.ogg")
+    cocksound = LoadSound("snd/magnumcock.ogg")
+    reloadsound = LoadSound("snd/magnumreload.ogg")
+    casingsound = LoadSound("snd/magnumcase.ogg")
+    dryfiresound = LoadSound("snd/dryfire.ogg")
+    refillsound = LoadSound("snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "500magnum" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		if not reloading then
+    			if mags == 0 or ammo == 0 then
+    				PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    			else
+    				Shoot(false)
+    			end
+    		end
+    	end
+
+    	if InputDown("rmb") then
+    		if not reloading then
+    			Shoot(true)
+    		end
+    	end
+
+    	SetBool("hud.aimdot", false, true)
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.1, 0.1, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.65, -2.4))
+
+    		if recoilTimer ~= 0 then
+    			PointLight(toolPos, 1, 1, 1, 1)
+
+    			local t = Transform()
+    			t.pos = Vec(0.1, 0.1, recoilTimer*3)
+    			t.rot = QuatEuler(recoilTimer*100, 0, 0)
+    			SetToolTransform(t)
+    			angVel = 2.5
+    			recoilTimer = recoilTimer - dt
+    		else
+    			angVel = 0
+    		end
+
+    		if reloading then
+    			angVel = -10
+    		end
+
+    		angle = angle + angVel
+
+    		local voxSize = 0.1
+    		local attach = Transform(Vec(2.75*voxSize, -6.3*voxSize, 0))
+    		if body ~= b then
+    			body = b
+    			-- Barrel is the second shape in vox file. Remember original position in attachment frame
+    			local shapes = GetBodyShapes(b)
+    			barrel = shapes[2]
+    			barrelTransform = TransformToLocalTransform(attach, GetShapeLocalTransform(barrel))	
+    		end
+
+    		attach.rot = QuatEuler(0, 0, -angle)
+    		t = TransformToParentTransform(attach, barrelTransform)
+    		SetShapeLocalTransform(barrel, t)
+    	end
+
+    	if not unlimitedammo then
+    		if ammo < 5 and mags > 1 and InputPressed("R") then
+    			Reload()
+    		end
+
+    		if GetBool("ammobox.refill") then
+    			SetBool("ammobox.refill", false, true)
+    			mags = mags + 1
+    			PlaySound(refillsound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+
+    		if reloading then
+    			reloadTimer = reloadTimer - dt
+    			if reloadTimer < 0 then
+    				ammo = 5
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(magnumprojectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		end
+    	end
+
+    	if shootTimer > 0 or ammo == 0 then
+    		shootTimer = shootTimer - dt
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "500magnum" and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle")
+    		UiImage("MOD/img/crosshair1.png")
+    	UiPop()
+    	if not unlimitedammo then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			if reloading then
+    				UiText("Reloading")
+    			else
+    				UiText(ammo.."/"..5*math.max(0, mags-1))
+    			end
+    		UiPop()
+    	end
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
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	if unlimitedammo == 0 then unlimitedammo = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("500 Magnum")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Unlimited Ammo")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if unlimitedammo then
-			if UiTextButton("Yes", 20, 20) then
-				unlimitedammo = false
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				unlimitedammo = true
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
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
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    if unlimitedammo == 0 then unlimitedammo = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("500 Magnum")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Unlimited Ammo")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if unlimitedammo then
+    		if UiTextButton("Yes", 20, 20) then
+    			unlimitedammo = false
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			unlimitedammo = true
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
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
