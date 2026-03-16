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
-novashotgunprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("novashotgun", "Nova Shotgun", "MOD/vox/novashotgun.vox")
-	SetBool("game.tool.novashotgun.enabled", true)
-	SetFloat("game.tool.novashotgun.ammo", 101)
-
-	damage = 0.35
-	gravity = Vec(0, 0, 0)
-	velocity = 1.5
-	reloadTime = 0.5
-	shotDelay = 0.6
-	ammo = 8
-	mags = 41
-	pellets = 25
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	for i=1, 50 do
-		novashotgunprojectileHandler.shells[i] = deepcopy(novashotgunprojectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-	cockTimer = 0
-
-	shootSound = LoadSound("MOD/snd/nova_shot.ogg")
-	cocksound = LoadSound("MOD/snd/nova_cock.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-	loadsound = LoadSound("MOD/snd/nova_load.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -96,7 +58,7 @@
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.15)
 	SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
-	PlaySound(shootSound, GetPlayerTransform().pos, 0.8, false)
+	PlaySound(shootSound, GetPlayerTransform(playerId).pos, 0.8, false)
 	if not unlimitedammo then
 		ammo = ammo - 1
 	end
@@ -130,127 +92,165 @@
 	reloadTimer = reloadTime
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "novashotgun" and GetPlayerVehicle() == 0 then
-		if InputDown("lmb") and ammo > 0 and not reloading then
-			Shoot()
-		end
-
-		if InputPressed("lmb") and not reloading then
-			if ammo == 0 then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			end
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0, heightOffset, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.55, -2.4))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, heightOffset, recoilTimer*2)
-				t.rot = QuatEuler(recoilTimer*70, 0, 0)
-				SetToolTransform(t)
-				recoilTimer = recoilTimer - dt
-				if recoilTimer < 0.0001 then
-					cockTimer = 0.4
-				end
-			end
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 1, 1, 0.5)
-				lightTimer = lightTimer - dt
-			end
-
-			local shelloffset = Vec(0, 0, 0)
-			if cockTimer > 0 then
-				cockTimer = cockTimer - dt
-				shelloffset = Vec(0.4-cockTimer, 0.6-cockTimer*1.5, 0.4-cockTimer)
-			end
-			
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				barrel = shapes[2]
-				shell = shapes[3]
-				barrelTrans = GetShapeLocalTransform(barrel)
-				shellTrans = GetShapeLocalTransform(shell)
-			end
-
-			bt = TransformCopy(barrelTrans)
-			bt.pos = VecAdd(bt.pos, Vec(0, 0, cockTimer*0.75))
-			SetShapeLocalTransform(barrel, bt)
-
-			local cockinv = 0.4 - cockTimer
-
-			st = TransformCopy(shellTrans)
-			st.pos = VecAdd(st.pos, shelloffset)
-			st.rot = QuatRotateQuat(st.rot, QuatEuler(0, -cockinv*250, -cockinv*500))
-			SetShapeLocalTransform(shell, st)
-		end
-
-		if not unlimitedammo then
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
-				if InputDown("lmb") then 
-					reloading = false
-					Shoot()
-					return 
-				end
-				reloadTimer = reloadTimer - GetTimeStep()
-				if reloadTimer < 0 then
-					ammo = ammo + 1
-					mags = mags - 1
-					PlaySound(refillsound, GetPlayerTransform().pos, 1, false)
-					if ammo < 8 then
-						reloadTimer = reloadTime
-						return
-					end
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-		
-		if shootTimer > 0 then
-			shootTimer = shootTimer - GetTimeStep()
-		end
-	end
-
-	for key, shell in ipairs(novashotgunprojectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "novashotgun" and GetPlayerVehicle() == 0 and not unlimitedammo then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				UiText(ammo.."/"..1*math.max(0,(mags-1)))
-			end
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("novashotgun", "Nova Shotgun", "MOD/vox/novashotgun.vox")
+    SetBool("game.tool.novashotgun.enabled", true, true)
+    SetFloat("game.tool.novashotgun.ammo", 101, true)
+    damage = 0.35
+    gravity = Vec(0, 0, 0)
+    velocity = 1.5
+    reloadTime = 0.5
+    shotDelay = 0.6
+    ammo = 8
+    mags = 41
+    pellets = 25
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    for i=1, 50 do
+    	novashotgunprojectileHandler.shells[i] = deepcopy(novashotgunprojectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+    cockTimer = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(novashotgunprojectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("MOD/snd/nova_shot.ogg")
+    cocksound = LoadSound("MOD/snd/nova_cock.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+    loadsound = LoadSound("MOD/snd/nova_load.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "novashotgun" and GetPlayerVehicle(playerId) == 0 then
+    	if InputDown("lmb") and ammo > 0 and not reloading then
+    		Shoot()
+    	end
+
+    	if InputPressed("lmb") and not reloading then
+    		if ammo == 0 then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.55, -2.4))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, heightOffset, recoilTimer*2)
+    			t.rot = QuatEuler(recoilTimer*70, 0, 0)
+    			SetToolTransform(t)
+    			recoilTimer = recoilTimer - dt
+    			if recoilTimer < 0.0001 then
+    				cockTimer = 0.4
+    			end
+    		end
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 1, 1, 0.5)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		local shelloffset = Vec(0, 0, 0)
+    		if cockTimer ~= 0 then
+    			cockTimer = cockTimer - dt
+    			shelloffset = Vec(0.4-cockTimer, 0.6-cockTimer*1.5, 0.4-cockTimer)
+    		end
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			barrel = shapes[2]
+    			shell = shapes[3]
+    			barrelTrans = GetShapeLocalTransform(barrel)
+    			shellTrans = GetShapeLocalTransform(shell)
+    		end
+
+    		bt = TransformCopy(barrelTrans)
+    		bt.pos = VecAdd(bt.pos, Vec(0, 0, cockTimer*0.75))
+    		SetShapeLocalTransform(barrel, bt)
+
+    		local cockinv = 0.4 - cockTimer
+
+    		st = TransformCopy(shellTrans)
+    		st.pos = VecAdd(st.pos, shelloffset)
+    		st.rot = QuatRotateQuat(st.rot, QuatEuler(0, -cockinv*250, -cockinv*500))
+    		SetShapeLocalTransform(shell, st)
+    	end
+
+    	if not unlimitedammo then
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
+    			if InputDown("lmb") then 
+    				reloading = false
+    				Shoot()
+    				return 
+    			end
+    			reloadTimer = reloadTimer - GetTimeStep()
+    			if reloadTimer < 0 then
+    				ammo = ammo + 1
+    				mags = mags - 1
+    				PlaySound(refillsound, GetPlayerTransform(playerId).pos, 1, false)
+    				if ammo < 8 then
+    					reloadTimer = reloadTime
+    					return
+    				end
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	if shootTimer ~= 0 then
+    		shootTimer = shootTimer - GetTimeStep()
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "novashotgun" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			UiText(ammo.."/"..1*math.max(0,(mags-1)))
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
-	UiText("Nova Shotgun")
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
+    UiText("Nova Shotgun")
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
