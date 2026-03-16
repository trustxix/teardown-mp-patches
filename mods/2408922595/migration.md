# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,50 +1,4 @@
-m1garandprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("cresta-m1garand", "M1 Garand", "MOD/vox/m1garand.vox", 3)
-	SetBool("game.tool.cresta-m1garand.enabled", true)
-	SetString("game.tool.cresta-m1garand.ammo.display","")
-	SetFloat("game.tool.cresta-m1garand.ammo", 101)
-	realisticdamage = GetBool("savegame.mod.realisticdamage")
-
-	damage = realisticdamage and 0.35 or 1.1
-	penetration = 2
-	gravity = Vec(0, 0, 0)
-	velocity = 1.7
-	reloadTime = 1.5
-	shotDelay = 0.3
-	ammo = 8
-	mags = 10
-	reloading = false
-	ironsight = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	withreload = GetBool("savegame.mod.withreload")
-
-	for i=1, ammo do
-		m1garandprojectileHandler.shells[i] = deepcopy(m1garandprojectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-	magoutTimer = 0
-	maginTimer = 0
-	clipoutTimer = 0
-
-	gunsound = LoadSound("MOD/snd/garandshot.ogg")
-	cocksound = LoadSound("MOD/snd/garandcock.ogg")
-	reloadsound = LoadSound("MOD/snd/garandmag.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-	pingsound = LoadSound("MOD/snd/garandping.ogg")
-	slidesound = LoadSound("MOD/snd/garandslide.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -109,9 +63,9 @@
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.15)
 	SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.35, 0.8)
-	PlaySound(gunsound, GetPlayerTransform().pos, 0.75, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.75, false)
 	if last then
-		PlaySound(pingsound, GetPlayerTransform().pos)
+		PlaySound(pingsound, GetPlayerTransform(playerId).pos)
 		clipoutTimer = 0.4
 	end
 	if not unlimitedammo or withreload then
@@ -124,11 +78,11 @@
 function destructiblerobots(pos, damage, hitcounter)
     local hit, point, n, shape = QueryClosestPoint(pos, 0.3)
     if hit then 
-		SetFloat('level.destructible-bot.debug', false)
-        SetInt('level.destructible-bot.hitCounter', hitcounter)
-        SetInt('level.destructible-bot.hitShape', shape)
-        SetString('level.destructible-bot.weapon', "M1 Garand")
-        SetFloat('level.destructible-bot.damage', damage)
+		SetFloat('level.destructible-bot.debug', false, true)
+        SetInt('level.destructible-bot.hitCounter', hitcounter, true)
+        SetInt('level.destructible-bot.hitShape', shape, true)
+        SetString('level.destructible-bot.weapon', "M1 Garand", true)
+        SetFloat('level.destructible-bot.damage', damage, true)
     end 
 end
 
@@ -163,13 +117,13 @@
 	if reloading then
 		return
 	end
-	if ammo > 0 then
-		PlaySound(pingsound, GetPlayerTransform().pos)
+	if ammo ~= 0 then
+		PlaySound(pingsound, GetPlayerTransform(playerId).pos)
 		clipoutTimer = 0.4
 	end
 	reloading = true
 	reloadTimer = reloadTime
-	PlaySound(slidesound, GetPlayerTransform().pos)
+	PlaySound(slidesound, GetPlayerTransform(playerId).pos)
 	mags = mags - 1
 	magoutTimer = 0.6
 end
@@ -191,7 +145,7 @@
 			offset = Transform(Vec(-x, y, z), QuatEuler(-rot, 0, 0))
 		end
 
-		if magtimer > 0 then
+		if magtimer ~= 0 then
 			offset.rot = QuatEuler(-5, 0, 10)
 			offset.pos = VecAdd(offset.pos, Vec(-0.2, -0.2, 0))
 			magoffset = Vec(-0.6, -0.6, 0.6)
@@ -201,7 +155,7 @@
 		toolTrans = GetBodyTransform(b)
 		toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.6, -2.75))
 
-		if recoilTimer > 0 then
+		if recoilTimer ~= 0 then
 			local t = Transform()
 			t.pos = Vec(-x, y, recoilTimer+z)
 			ironrot = ironsight and rot or -recoilTimer*50-rot
@@ -211,25 +165,25 @@
 			recoilTimer = recoilTimer - dt
 		end
 
-		if lightTimer > 0 then
+		if lightTimer ~= 0 then
 			PointLight(toolPos, 1, 1, 1, 0.5)
 			lightTimer = lightTimer - dt
 		end
 		
-		if magoutTimer > 0 then
+		if magoutTimer ~= 0 then
 			magoutTimer = magoutTimer - dt
 			if magoutTimer < 0 then
 				maginTimer = 0.6
-				PlaySound(reloadsound, GetPlayerTransform().pos)
+				PlaySound(reloadsound, GetPlayerTransform(playerId).pos)
 			end
 		end
 
-		if maginTimer > 0 then
+		if maginTimer ~= 0 then
 			magoffset = Vec(-maginTimer/2, maginTimer*2, maginTimer)
 			maginTimer = maginTimer - dt
 		end
 
-		if clipoutTimer > 0 then
+		if clipoutTimer ~= 0 then
 			cliptime = 0.41 - clipoutTimer
 			clipoffset = Vec(-0.05+cliptime*2, 0+cliptime*4, 0+cliptime)
 			clipoutTimer = clipoutTimer - dt
@@ -256,105 +210,147 @@
 	end
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "cresta-m1garand" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			if not reloading then
-				if ammo == 0 then
-					PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-				else
-					Shoot()
-				end
-			end
-		end
-
-		if InputPressed("rmb") then
-			ironsight = not ironsight
-		end
-
-		AnimateTool(dt)
-
-		if unlimitedammo and withreload then
-			if ammo < 8 and InputPressed("R") then
-				Reload()
-			end
-			if reloading then
-				ironsight = false
-				reloadTimer = reloadTimer - dt
-				if reloadTimer < 0 then
-					ammo = 8
-					reloadTimer = 0
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.75, false)
-					reloading = false
-				end
-			end
-		else
-			if ammo < 8 and mags > 1 and InputPressed("R") then
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
-					ammo = 8
-					reloadTimer = 0
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.75, false)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(m1garandprojectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
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
-	if GetString("game.player.tool") == "cresta-m1garand" and GetPlayerVehicle() == 0 then
-		if unlimitedammo then
-			if withreload then
-				UiPush()
-					UiTranslate(UiCenter(), UiHeight()-60)
-					UiAlign("center middle")
-					UiColor(1, 1, 1)
-					UiFont("bold.ttf", 32)
-					UiTextOutline(0,0,0,1,0.1)
-					if reloading then
-						UiText("Reloading")
-					else
-						UiText(ammo.."/ºº")
-					end
-				UiPop()
-			end
-		else
-			UiPush()
-				UiTranslate(UiCenter(), UiHeight()-60)
-				UiAlign("center middle")
-				UiColor(1, 1, 1)
-				UiFont("bold.ttf", 32)
-				UiTextOutline(0,0,0,1,0.1)
-				if reloading then
-					UiText("Reloading")
-				else
-					UiText(ammo.."/"..8*math.max(0, mags-1))
-				end
-			UiPop()
-		end
-	end
-end+function server.init()
+    RegisterTool("cresta-m1garand", "M1 Garand", "MOD/vox/m1garand.vox", 3)
+    SetBool("game.tool.cresta-m1garand.enabled", true, true)
+    SetString("game.tool.cresta-m1garand.ammo.display","", true)
+    SetFloat("game.tool.cresta-m1garand.ammo", 101, true)
+    realisticdamage = GetBool("savegame.mod.realisticdamage")
+    damage = realisticdamage and 0.35 or 1.1
+    penetration = 2
+    gravity = Vec(0, 0, 0)
+    velocity = 1.7
+    reloadTime = 1.5
+    shotDelay = 0.3
+    ammo = 8
+    mags = 10
+    reloading = false
+    ironsight = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    withreload = GetBool("savegame.mod.withreload")
+    for i=1, ammo do
+    	m1garandprojectileHandler.shells[i] = deepcopy(m1garandprojectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+    magoutTimer = 0
+    maginTimer = 0
+    clipoutTimer = 0
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/garandshot.ogg")
+    cocksound = LoadSound("MOD/snd/garandcock.ogg")
+    reloadsound = LoadSound("MOD/snd/garandmag.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+    pingsound = LoadSound("MOD/snd/garandping.ogg")
+    slidesound = LoadSound("MOD/snd/garandslide.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "cresta-m1garand" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		if not reloading then
+    			if ammo == 0 then
+    				PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    			else
+    				Shoot()
+    			end
+    		end
+    	end
+
+    	if InputPressed("rmb") then
+    		ironsight = not ironsight
+    	end
+
+    	AnimateTool(dt)
+
+    	if unlimitedammo and withreload then
+    		if ammo < 8 and InputPressed("R") then
+    			Reload()
+    		end
+    		if reloading then
+    			ironsight = false
+    			reloadTimer = reloadTimer - dt
+    			if reloadTimer < 0 then
+    				ammo = 8
+    				reloadTimer = 0
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.75, false)
+    				reloading = false
+    			end
+    		end
+    	else
+    		if ammo < 8 and mags > 1 and InputPressed("R") then
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
+    				ammo = 8
+    				reloadTimer = 0
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.75, false)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(m1garandprojectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
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
+    if GetString("game.player.tool") == "cresta-m1garand" and GetPlayerVehicle(playerId) == 0 then
+    	if unlimitedammo then
+    		if withreload then
+    			UiPush()
+    				UiTranslate(UiCenter(), UiHeight()-60)
+    				UiAlign("center middle")
+    				UiColor(1, 1, 1)
+    				UiFont("bold.ttf", 32)
+    				UiTextOutline(0,0,0,1,0.1)
+    				if reloading then
+    					UiText("Reloading")
+    				else
+    					UiText(ammo.."/ºº")
+    				end
+    			UiPop()
+    		end
+    	else
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			if reloading then
+    				UiText("Reloading")
+    			else
+    				UiText(ammo.."/"..8*math.max(0, mags-1))
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
@@ -1,82 +1,4 @@
-function init()
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	withreload = GetBool("savegame.mod.withreload")
-	realisticdamage = GetBool("savegame.mod.realisticdamage")
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("M1 Garand")
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
-	UiTranslate(0, 80)
-	if unlimitedammo then
-		UiPush()
-			UiText("With Reload")
-			UiTranslate(15, 40)
-			UiAlign("right")
-			UiColor(0.5, 0.8, 1)
-			if withreload then
-				if UiTextButton("Yes", 20, 20) then
-					withreload = false
-					SetBool("savegame.mod.withreload", withreload)
-				end
-			else
-				if UiTextButton("No", 20, 20) then
-					withreload = true
-					SetBool("savegame.mod.withreload", withreload)
-				end
-			end
-		UiPop()
-	end
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
@@ -95,4 +17,84 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    withreload = GetBool("savegame.mod.withreload")
+    realisticdamage = GetBool("savegame.mod.realisticdamage")
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("M1 Garand")
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
+    UiTranslate(0, 80)
+    if unlimitedammo then
+    	UiPush()
+    		UiText("With Reload")
+    		UiTranslate(15, 40)
+    		UiAlign("right")
+    		UiColor(0.5, 0.8, 1)
+    		if withreload then
+    			if UiTextButton("Yes", 20, 20) then
+    				withreload = false
+    				SetBool("savegame.mod.withreload", withreload, true)
+    			end
+    		else
+    			if UiTextButton("No", 20, 20) then
+    				withreload = true
+    				SetBool("savegame.mod.withreload", withreload, true)
+    			end
+    		end
+    	UiPop()
+    end
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
