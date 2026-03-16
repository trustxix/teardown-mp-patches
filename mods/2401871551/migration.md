# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,42 +1,4 @@
-p90projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("p90", "P90", "MOD/vox/p90.vox")
-	SetBool("game.tool.p90.enabled", true)
-	SetFloat("game.tool.p90.ammo", 101)
-
-	damage = 0.5
-	gravity = Vec(0, 0, 0)
-	velocity = 1.5
-
-	gunsound = LoadSound("MOD/snd/p90.ogg")
-	cocksound = LoadSound("MOD/snd/p90cock.ogg")
-	reloadsound = LoadSound("MOD/snd/p90reload.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-
-	reloadTime = 1.8
-	shotDelay = 0.05
-	spreadTimer = 0
-	ammo = 50
-	mags = 6
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	for i=1, ammo do
-		p90projectileHandler.shells[i] = deepcopy(p90projectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -89,7 +51,7 @@
 	p90projectileHandler.shellNum = (p90projectileHandler.shellNum%#p90projectileHandler.shells) + 1
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(gunsound, GetPlayerTransform().pos, 1, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 1, false)
 
 	if not unlimitedammo then
 		ammo = ammo - 1
@@ -124,99 +86,132 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "p90" and GetPlayerVehicle() == 0 then
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
-			SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0, heightOffset, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -1.45))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, heightOffset, recoilTimer)
-				t.rot = QuatEuler(recoilTimer*50, 0, 0)
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
-			if ammo < 50 and mags > 1 and InputPressed("R") then
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
-					ammo = 50
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(p90projectileHandler.shells) do
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
-	if GetString("game.player.tool") == "p90" and GetPlayerVehicle() == 0 and not unlimitedammo then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				UiText(ammo.."/"..50*math.max(0, mags-1))
-			end
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("p90", "P90", "MOD/vox/p90.vox")
+    SetBool("game.tool.p90.enabled", true, true)
+    SetFloat("game.tool.p90.ammo", 101, true)
+    damage = 0.5
+    gravity = Vec(0, 0, 0)
+    velocity = 1.5
+    reloadTime = 1.8
+    shotDelay = 0.05
+    spreadTimer = 0
+    ammo = 50
+    mags = 6
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    for i=1, ammo do
+    	p90projectileHandler.shells[i] = deepcopy(p90projectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/p90.ogg")
+    cocksound = LoadSound("MOD/snd/p90cock.ogg")
+    reloadsound = LoadSound("MOD/snd/p90reload.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "p90" and GetPlayerVehicle(playerId) == 0 then
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
+    		SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.5)
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -1.45))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, heightOffset, recoilTimer)
+    			t.rot = QuatEuler(recoilTimer*50, 0, 0)
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
+    		if ammo < 50 and mags > 1 and InputPressed("R") then
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
+    				ammo = 50
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(p90projectileHandler.shells) do
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
+    if GetString("game.player.tool") == "p90" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			UiText(ammo.."/"..50*math.max(0, mags-1))
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
-	UiText("P90")
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
+    UiText("P90")
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
