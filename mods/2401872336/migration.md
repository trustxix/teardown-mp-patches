# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,50 +1,7 @@
+#version 2
 local TOOL = {}
-
-TOOL.printname = "Desert Eagle"
-TOOL.order = 2
-TOOL.base = "gun"
-
-TOOL.suppress_default = true
-
 local STATE_READY = 0
 local STATE_RELOADING = 2
-
-deagleprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("deagle", "Desert Eagle", "MOD/vox/deagle.vox")
-	SetBool("game.tool.deagle.enabled", true)
-	SetFloat("game.tool.deagle.ammo", 101)
-
-	damage = 1
-	gravity = Vec(0, 0, 0)
-	velocity = 1.6
-	reloadTime = 0.9
-	shotDelay = 0.2
-	ammo = 7
-	mags = 6
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	for i=1, ammo do
-		deagleprojectileHandler.shells[i] = deepcopy(deagleprojectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-
-	gunsound = LoadSound("MOD/snd/deagle_shot.ogg")
-	cocksound = LoadSound("MOD/snd/pistolcock.ogg")
-	reloadsound = LoadSound("MOD/snd/deagle_reload.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-end
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -92,7 +49,7 @@
 	deagleprojectileHandler.shellNum = (deagleprojectileHandler.shellNum%#deagleprojectileHandler.shells) +1
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.1)
 	SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.4, 1.5)
-	PlaySound(gunsound, GetPlayerTransform().pos, 0.9, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.9, false)
 	if not unlimitedammo then
 		ammo = ammo - 1
 	end
@@ -124,93 +81,129 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "deagle" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			if not reloading then
-				if mags == 0 or ammo == 0 then
-					PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-				else
-					Shoot()
-				end
-			end
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.1, 0.1, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.45, -2.4))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0.1, 0.1, recoilTimer*3)
-				t.rot = QuatEuler(recoilTimer*100, 0, 0)
-				SetToolTransform(t)
-
-				recoilTimer = recoilTimer - dt
-			end
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 1, 1, 0.5)
-
-				lightTimer = lightTimer - dt
-			end
-		end
-
-		if not unlimitedammo then
-			if ammo < 7 and mags > 1 and InputPressed("R") then
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
-					ammo = 7
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	end
-	
-	for key, shell in ipairs(deagleprojectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "deagle" and GetPlayerVehicle() == 0 and not unlimitedammo then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				UiText(ammo.."/"..7*math.max(0, mags-1))
-			end
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("deagle", "Desert Eagle", "MOD/vox/deagle.vox")
+    SetBool("game.tool.deagle.enabled", true, true)
+    SetFloat("game.tool.deagle.ammo", 101, true)
+    damage = 1
+    gravity = Vec(0, 0, 0)
+    velocity = 1.6
+    reloadTime = 0.9
+    shotDelay = 0.2
+    ammo = 7
+    mags = 6
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    for i=1, ammo do
+    	deagleprojectileHandler.shells[i] = deepcopy(deagleprojectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(deagleprojectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
+        end
+    end
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/deagle_shot.ogg")
+    cocksound = LoadSound("MOD/snd/pistolcock.ogg")
+    reloadsound = LoadSound("MOD/snd/deagle_reload.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "deagle" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		if not reloading then
+    			if mags == 0 or ammo == 0 then
+    				PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    			else
+    				Shoot()
+    			end
+    		end
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.1, 0.1, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.45, -2.4))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0.1, 0.1, recoilTimer*3)
+    			t.rot = QuatEuler(recoilTimer*100, 0, 0)
+    			SetToolTransform(t)
+
+    			recoilTimer = recoilTimer - dt
+    		end
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 1, 1, 0.5)
+
+    			lightTimer = lightTimer - dt
+    		end
+    	end
+
+    	if not unlimitedammo then
+    		if ammo < 7 and mags > 1 and InputPressed("R") then
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
+    				ammo = 7
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
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
+    if GetString("game.player.tool") == "deagle" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			UiText(ammo.."/"..7*math.max(0, mags-1))
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
-	UiText("Desert Eagle")
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
+    UiText("Desert Eagle")
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
