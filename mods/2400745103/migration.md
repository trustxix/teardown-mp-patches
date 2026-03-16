# Migration Report: crestaoptions.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/crestaoptions.lua
+++ patched/crestaoptions.lua
@@ -1,12 +1,5 @@
-function init()
+#version 2
+function server.init()
     optionsOpen = GetBool("savegame.mod.optionsopen")
 end
 
-function tick()
-
-end
-
--- One copy of the same options file in each tool mod, it checks for all enabled tools by me, lists them and displays options for them
--- This file is read not for each mod.
--- Is it possible to have all tool mods call the same options file but once and not for each enabled tool?
--- I want to be able to have only one settings button like "My Cresta Tools" which would open a menu and display a dynamic menu for all my enabled tools, without having an external settings mod?

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
@@ -1,67 +1,4 @@
-ak47projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false,
-		aliveTimer = 0
-	},
-}
-
-ak47shellHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false,
-		aliveTimer = 0,
-		bounces = 0
-	},
-}
-
-function init()
-	RegisterTool("ak47", "AK-47", "MOD/vox/ak47.vox", 3)
-	SetBool("game.tool.ak47.enabled", true)
-	SetString("game.tool.ak47.ammo.display","")
-	SetFloat("game.tool.ak47.ammo", 101)
-	realisticdamage = GetBool("savegame.mod.realisticdamage")
-
-	damage = realisticdamage and 0.25 or 0.6
-	gravity = Vec(0, -1, 0)
-	shellGravity = Vec(0, -50, 0)
-	velocity = 1.5
-
-	gunsound = LoadSound("MOD/snd/ak0.ogg")
-	cocksound = LoadSound("MOD/snd/guncock.ogg")
-	reloadsound = LoadSound("MOD/snd/reload.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-	shellsound = LoadSound("MOD/snd/shellground.ogg")
-
-	reloadTime = 1.7
-	shotDelay = 0.085
-	spreadTimer = 0
-	ammo = 30
-	mags = 7
-	reloading = false
-	ironsight = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	for i=1, 200 do
-		ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
-	end
-
-	for i=1, 100 do
-		ak47shellHandler.shells[i] = deepcopy(ak47shellHandler.defaultShell)
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
@@ -150,7 +87,7 @@
 	ak47projectileHandler.shellNum = (ak47projectileHandler.shellNum%#ak47projectileHandler.shells) + 1
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(gunsound, GetPlayerTransform().pos, 1, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 1, false)
 
 	if not unlimitedammo then
 		ammo = ammo - 1
@@ -164,11 +101,11 @@
 function destructiblerobots(pos, damage, hitcounter)
     local hit, point, n, shape = QueryClosestPoint(pos, 0.3)
     if hit then 
-		SetFloat('level.destructible-bot.debug', false)
-        SetInt('level.destructible-bot.hitCounter', hitcounter)
-        SetInt('level.destructible-bot.hitShape', shape)
-        SetString('level.destructible-bot.weapon', "AK-47")
-        SetFloat('level.destructible-bot.damage', damage)
+		SetFloat('level.destructible-bot.debug', false, true)
+        SetInt('level.destructible-bot.hitCounter', hitcounter, true)
+        SetInt('level.destructible-bot.hitShape', shape, true)
+        SetString('level.destructible-bot.weapon', "AK-47", true)
+        SetFloat('level.destructible-bot.damage', damage, true)
     end 
 end
 
@@ -229,174 +166,217 @@
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
-	if GetString("game.player.tool") == "ak47" and GetBool("game.player.canusetool") then
-		if InputDown("usetool") and ammo > 0 and not reloading then
-			Shoot()
-		end
-
-		if InputPressed("usetool") and not reloading then
-			spreadTimer = 0
-			if ammo == 0 then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			end
-		end
-
-		if InputReleased("usetool") and ammo > 0 then
-			SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
-		end
-
-		if InputPressed("rmb") and not IsHandleValid(GetPlayerGrabBody()) then
-			ironsight = not ironsight
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local magoffset = Vec(0, 0, 0)
-			local magtimer = magoutTimer + maginTimer
-			local offset = Transform(Vec(0, heightOffset, 0))
-			local x, y, z, rot = 0, heightOffset, 0, 0
-			if ironsight then
-				x = 0.275
-				y = 0.45
-				z = 1
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
-			SetToolTransform(offset, ironsight and 0 or 0.5)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.275, -0.6, -2.6))
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
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.85)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(ak47projectileHandler.shells) do
-			if shell.aliveTimer > 0 then
-				shell.aliveTimer = shell.aliveTimer - dt
-				if shell.aliveTimer < 0.1 then
-					shell.active = false
-					shell.aliveTimer = 0
-				end
-			end
-			if shell.active then
-				ProjectileOperations(shell)
-			else
-				Delete(shell.voxBody)
-			end
-		end
-
-		for key, shell in ipairs(ak47shellHandler.shells) do
-			if shell.aliveTimer > 0 then
-				shell.aliveTimer = shell.aliveTimer - dt
-				if shell.aliveTimer < 0.1 then
-					shell.active = false
-				end
-			end
-			if shell.active then
-				ShellOperations(shell)
-			else
-				Delete(shell.voxBody)
-			end
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	else
-		ironsight = false
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "ak47" and GetPlayerVehicle() == 0 then
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
-					UiText(ammo.."/"..30*math.max(0, mags-1))
-				end
-			UiPop()
-		end
-	end
-end+function server.init()
+    RegisterTool("ak47", "AK-47", "MOD/vox/ak47.vox", 3)
+    SetBool("game.tool.ak47.enabled", true, true)
+    SetString("game.tool.ak47.ammo.display","", true)
+    SetFloat("game.tool.ak47.ammo", 101, true)
+    realisticdamage = GetBool("savegame.mod.realisticdamage")
+    damage = realisticdamage and 0.25 or 0.6
+    gravity = Vec(0, -1, 0)
+    shellGravity = Vec(0, -50, 0)
+    velocity = 1.5
+    reloadTime = 1.7
+    shotDelay = 0.085
+    spreadTimer = 0
+    ammo = 30
+    mags = 7
+    reloading = false
+    ironsight = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    for i=1, 200 do
+    	ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    end
+    for i=1, 100 do
+    	ak47shellHandler.shells[i] = deepcopy(ak47shellHandler.defaultShell)
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
+    gunsound = LoadSound("MOD/snd/ak0.ogg")
+    cocksound = LoadSound("MOD/snd/guncock.ogg")
+    reloadsound = LoadSound("MOD/snd/reload.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+    shellsound = LoadSound("MOD/snd/shellground.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "ak47" and GetBool("game.player.canusetool") then
+    	if InputDown("usetool") and ammo > 0 and not reloading then
+    		Shoot()
+    	end
+
+    	if InputPressed("usetool") and not reloading then
+    		spreadTimer = 0
+    		if ammo == 0 then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    	end
+
+    	if InputReleased("usetool") and ammo ~= 0 then
+    		SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
+    	end
+
+    	if InputPressed("rmb") and not IsHandleValid(GetPlayerGrabBody(playerId)) then
+    		ironsight = not ironsight
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local magoffset = Vec(0, 0, 0)
+    		local magtimer = magoutTimer + maginTimer
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		local x, y, z, rot = 0, heightOffset, 0, 0
+    		if ironsight then
+    			x = 0.275
+    			y = 0.45
+    			z = 1
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
+    		SetToolTransform(offset, ironsight and 0 or 0.5)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.275, -0.6, -2.6))
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
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.85)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(ak47projectileHandler.shells) do
+    		if shell.aliveTimer ~= 0 then
+    			shell.aliveTimer = shell.aliveTimer - dt
+    			if shell.aliveTimer < 0.1 then
+    				shell.active = false
+    				shell.aliveTimer = 0
+    			end
+    		end
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		else
+    			Delete(shell.voxBody)
+    		end
+    	end
+
+    	for key, shell in ipairs(ak47shellHandler.shells) do
+    		if shell.aliveTimer ~= 0 then
+    			shell.aliveTimer = shell.aliveTimer - dt
+    			if shell.aliveTimer < 0.1 then
+    				shell.active = false
+    			end
+    		end
+    		if shell.active then
+    			ShellOperations(shell)
+    		else
+    			Delete(shell.voxBody)
+    		end
+    	end
+
+    	if shootTimer > 0 or ammo == 0 then
+    		shootTimer = shootTimer - dt
+    	end
+    else
+    	ironsight = false
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "ak47" and GetPlayerVehicle(playerId) == 0 then
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
+    				UiText(ammo.."/"..30*math.max(0, mags-1))
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
@@ -1,60 +1,4 @@
-function init()
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	realisticdamage = GetBool("savegame.mod.realisticdamage")
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("AK-47")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Realistic bullet damage")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if realisticdamage then
-			if UiTextButton("Yes", 20, 20) then
-				realisticdamage = false
-				SetBool("savegame.mod.realisticdamage", realisticdamage)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				realisticdamage = true
-				SetBool("savegame.mod.realisticdamage", realisticdamage)
-			end
-		end
-	UiPop()
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
@@ -73,4 +17,62 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    realisticdamage = GetBool("savegame.mod.realisticdamage")
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("AK-47")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Realistic bullet damage")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if realisticdamage then
+    		if UiTextButton("Yes", 20, 20) then
+    			realisticdamage = false
+    			SetBool("savegame.mod.realisticdamage", realisticdamage, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			realisticdamage = true
+    			SetBool("savegame.mod.realisticdamage", realisticdamage, true)
+    		end
+    	end
+    UiPop()
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
