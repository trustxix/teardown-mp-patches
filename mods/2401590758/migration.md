# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,46 +1,4 @@
-m4a1projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("m4a1", "M4A1", "MOD/vox/m4a1.vox")
-	SetBool("game.tool.m4a1.enabled", true)
-	SetFloat("game.tool.m4a1.ammo", 101)
-
-	damage = 0.5
-	gravity = Vec(0, 0, 0)
-	velocity = 1.5
-
-	gunsound = LoadSound("MOD/snd/m4.ogg")
-	cocksound = LoadSound("MOD/snd/guncock.ogg")
-	reloadsound = LoadSound("MOD/snd/reload.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-
-	reloadTime = 1.6
-	shotDelay = 0.075
-	spreadTimer = 0
-	ammo = 30
-	mags = 8
-	reloading = false
-	ironsight = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	for i=1, ammo do
-		m4a1projectileHandler.shells[i] = deepcopy(m4a1projectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-
-	magoutTimer = 0
-	maginTimer = 0
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -94,7 +52,7 @@
 	m4a1projectileHandler.shellNum = (m4a1projectileHandler.shellNum%#m4a1projectileHandler.shells) + 1
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(gunsound, GetPlayerTransform().pos, 1, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 1, false)
 
 	if not unlimitedammo then
 		ammo = ammo - 1
@@ -129,147 +87,183 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	magoutTimer = 0.6
 	mags = mags - 1
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "m4a1" and GetPlayerVehicle() == 0 then
-		if InputDown("lmb") and ammo > 0 and not reloading then
-			Shoot()
-		end
-
-		if InputPressed("lmb") and not reloading then
-			spreadTimer = 0
-			if ammo == 0 then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			end
-		end
-
-		if InputReleased("lmb") and ammo > 0 then
-			SpawnParticle("darksmoke", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
-		end
-
-		if InputPressed("rmb") then
-			ironsight = not ironsight
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.25 or 0.2
-			local magoffset = Vec(0, 0, 0)
-			local magtimer = magoutTimer + maginTimer
-			local offset = Transform(Vec(0, heightOffset, 0))
-			local x, y, z, rot = 0, heightOffset, 0, 0
-			if ironsight then
-				x = 0.32
-				y = 0.355
-				z = 0.3
-				rot = 2.5
-				offset = Transform(Vec(-x, y, z), QuatEuler(-rot, 0, 0))
-			end
-
-			if magtimer > 0 then
-				offset.rot = QuatEuler(10, 0, -10)
-				offset.pos = VecAdd(offset.pos, Vec(0.2, 0.2, 0))
-				magoffset = Vec(-0.6, -0.6, 0.6)
-			end
-
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.35))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(-x, y, recoilTimer+z)
-				ironrot = ironsight and rot or -recoilTimer*50-rot
-				t.rot = QuatEuler(-ironrot, 0, 0)
-				SetToolTransform(t)
-
-				recoilTimer = recoilTimer - dt
-			end
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 1, 1, 0.5)
-				lightTimer = lightTimer - dt
-			end
-			
-			if magoutTimer > 0 then
-				magoffset = Vec(-0.3+magoutTimer/2, -0.6+magoutTimer, 0.9-magoutTimer*1.5)
-				magoutTimer = magoutTimer - dt
-				if magoutTimer < 0 then
-					maginTimer = 0.6
-				end
-			end
-
-			if maginTimer > 0 then
-				magoffset = Vec(-maginTimer/2, -maginTimer, maginTimer*1.5)
-				maginTimer = maginTimer - dt
-			end
-			
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				mag = shapes[2]
-				magTrans = GetShapeLocalTransform(mag)
-			end
-
-			mt = TransformCopy(magTrans)
-			mt.pos = VecAdd(mt.pos, magoffset)
-			mt.rot = QuatRotateQuat(mt.rot, QuatEuler(-magtimer*30, magtimer*30, 0))
-			SetShapeLocalTransform(mag, mt)
-		end
-
-		if not unlimitedammo then
-			if ammo < 30 and mags > 1 and InputPressed("R") then
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
-				ironsight = false
-				reloadTimer = reloadTimer - dt
-				if reloadTimer < 0 then
-					ammo = 30
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(m4a1projectileHandler.shells) do
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
-	if GetString("game.player.tool") == "m4a1" and GetPlayerVehicle() == 0 and not unlimitedammo then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				UiText(ammo.."/"..30*math.max(0, mags-1))
-			end
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("m4a1", "M4A1", "MOD/vox/m4a1.vox")
+    SetBool("game.tool.m4a1.enabled", true, true)
+    SetFloat("game.tool.m4a1.ammo", 101, true)
+    damage = 0.5
+    gravity = Vec(0, 0, 0)
+    velocity = 1.5
+    reloadTime = 1.6
+    shotDelay = 0.075
+    spreadTimer = 0
+    ammo = 30
+    mags = 8
+    reloading = false
+    ironsight = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    for i=1, ammo do
+    	m4a1projectileHandler.shells[i] = deepcopy(m4a1projectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+    magoutTimer = 0
+    maginTimer = 0
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/m4.ogg")
+    cocksound = LoadSound("MOD/snd/guncock.ogg")
+    reloadsound = LoadSound("MOD/snd/reload.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "m4a1" and GetPlayerVehicle(playerId) == 0 then
+    	if InputDown("lmb") and ammo > 0 and not reloading then
+    		Shoot()
+    	end
+
+    	if InputPressed("lmb") and not reloading then
+    		spreadTimer = 0
+    		if ammo == 0 then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    	end
+
+    	if InputReleased("lmb") and ammo ~= 0 then
+    		SpawnParticle("darksmoke", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
+    	end
+
+    	if InputPressed("rmb") then
+    		ironsight = not ironsight
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.25 or 0.2
+    		local magoffset = Vec(0, 0, 0)
+    		local magtimer = magoutTimer + maginTimer
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		local x, y, z, rot = 0, heightOffset, 0, 0
+    		if ironsight then
+    			x = 0.32
+    			y = 0.355
+    			z = 0.3
+    			rot = 2.5
+    			offset = Transform(Vec(-x, y, z), QuatEuler(-rot, 0, 0))
+    		end
+
+    		if magtimer ~= 0 then
+    			offset.rot = QuatEuler(10, 0, -10)
+    			offset.pos = VecAdd(offset.pos, Vec(0.2, 0.2, 0))
+    			magoffset = Vec(-0.6, -0.6, 0.6)
+    		end
+
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.35))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(-x, y, recoilTimer+z)
+    			ironrot = ironsight and rot or -recoilTimer*50-rot
+    			t.rot = QuatEuler(-ironrot, 0, 0)
+    			SetToolTransform(t)
+
+    			recoilTimer = recoilTimer - dt
+    		end
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 1, 1, 0.5)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if magoutTimer ~= 0 then
+    			magoffset = Vec(-0.3+magoutTimer/2, -0.6+magoutTimer, 0.9-magoutTimer*1.5)
+    			magoutTimer = magoutTimer - dt
+    			if magoutTimer < 0 then
+    				maginTimer = 0.6
+    			end
+    		end
+
+    		if maginTimer ~= 0 then
+    			magoffset = Vec(-maginTimer/2, -maginTimer, maginTimer*1.5)
+    			maginTimer = maginTimer - dt
+    		end
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			mag = shapes[2]
+    			magTrans = GetShapeLocalTransform(mag)
+    		end
+
+    		mt = TransformCopy(magTrans)
+    		mt.pos = VecAdd(mt.pos, magoffset)
+    		mt.rot = QuatRotateQuat(mt.rot, QuatEuler(-magtimer*30, magtimer*30, 0))
+    		SetShapeLocalTransform(mag, mt)
+    	end
+
+    	if not unlimitedammo then
+    		if ammo < 30 and mags > 1 and InputPressed("R") then
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
+    			ironsight = false
+    			reloadTimer = reloadTimer - dt
+    			if reloadTimer < 0 then
+    				ammo = 30
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(m4a1projectileHandler.shells) do
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
+    if GetString("game.player.tool") == "m4a1" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			UiText(ammo.."/"..30*math.max(0, mags-1))
+    		end
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
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	if unlimitedammo == 0 then unlimitedammo = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("M4A1")
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
+    UiText("M4A1")
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
