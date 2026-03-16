# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,51 +1,4 @@
-berettasprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("berettas", "Dual Berettas", "MOD/vox/berettas.vox")
-	SetBool("game.tool.berettas.enabled", true)
-	SetFloat("game.tool.berettas.ammo", 101)
-
-	damage = 0.6
-	gravity = Vec(0, 0, 0)
-	velocity = 1.4
-	reloadTime = 1.7
-	shotDelay = 0.1
-	mags = 11
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	beretta1 = {}
-	beretta1.left = true
-	beretta1.ammo = 15
-	beretta1.shootTimer = 0
-	beretta1.recoilTimer = 0
-
-	beretta2 = {}
-	beretta2.left = false
-	beretta2.ammo = 15
-	beretta2.shootTimer = 0
-	beretta2.recoilTimer = 0
-
-	ammo = beretta1.ammo + beretta2.ammo
-
-	reloadTimer = 0
-	lightTimer = 0
-
-	for i=1, ammo do
-		berettasprojectileHandler.shells[i] = deepcopy(berettasprojectileHandler.defaultShell)
-	end
-
-	gunsound = LoadSound("MOD/snd/gun_shot.ogg")
-	cocksound = LoadSound("MOD/snd/pistolcock.ogg")
-	reloadsound = LoadSound("MOD/snd/deagle_reload.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -89,7 +42,7 @@
 
 	SpawnParticle("fire", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
 	SpawnParticle("darksmoke", gunpos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.3, 1)
-	PlaySound(gunsound, GetPlayerTransform().pos, 0.7, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.7, false)
 	if not unlimitedammo then
 		beretta.ammo = beretta.ammo - 1
 	end
@@ -130,136 +83,179 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "berettas" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			if not reloading then
-				if mags == 0 or beretta1.ammo == 0 then
-					PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-				else
-					Shoot(beretta1)
-				end
-			end
-		end
-
-		if InputPressed("rmb") then
-			if not reloading then
-				if mags == 0 or beretta2.ammo == 0 then
-					PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-				else
-					Shoot(beretta2)
-				end
-			end
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.1, -0.9, 0.9))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			leftPos = TransformToParentPoint(toolTrans, Vec(-0.6, 0.4, -3.2))
-			rightPos = TransformToParentPoint(toolTrans, Vec(0.45, 0.4, -3.2))
-
-			local voxSize = 0.05
-			local attach = Transform(Vec(0, 0, 0))
-			local shapes = GetBodyShapes(b)
-			leftgun = shapes[1]
-			rightgun = shapes[2]
-
-			if b ~= body then
-				body = b
-				tl = GetShapeLocalTransform(leftgun)
-				tr = GetShapeLocalTransform(rightgun)
-			end
-
-			local t1 = 1-beretta1.recoilTimer
-			local t2 = 1-beretta2.recoilTimer
-			t1 = t1*t1
-			t2 = t2*t2
-			local offset1 = t1
-			local offset2 = t2
-
-			t = TransformCopy(tl)
-			t.pos = VecAdd(t.pos, Vec(0, 1, -offset1))
-			t.rot = QuatEuler(-90+beretta1.recoilTimer*90, 0, 0)
-			SetShapeLocalTransform(leftgun, t)
-
-			t = TransformCopy(tr)
-			t.pos = VecAdd(t.pos, Vec(0, 1, -offset2))
-			t.rot = QuatEuler(-90+beretta2.recoilTimer*90, 0, 0)
-			SetShapeLocalTransform(rightgun, t)
-
-			if beretta1.recoilTimer > 0 then
-				beretta1.recoilTimer = beretta1.recoilTimer - dt
-			end
-
-			if beretta2.recoilTimer > 0 then
-				beretta2.recoilTimer = beretta2.recoilTimer - dt
-			end
-
-			if lightTimer > 0 then
-				local p = TransformToParentPoint(GetBodyTransform(b), Vec(0, 0, -2))
-				PointLight(p, 1, 1, 1, 0.5)
-
-				lightTimer = lightTimer - dt
-			end
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
-				reloadTimer = reloadTimer - GetTimeStep()
-				if reloadTimer < 0 then
-					beretta1.ammo = 15
-					beretta2.ammo = 15
-					ammo = 30
-					reloadTimer = 0
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.6, false)
-					reloading = false
-				end
-			end
-		end
-	end
-
-	for key, shell in ipairs(berettasprojectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-
-	if beretta1.shootTimer > 0 or beretta2.shootTimer > 0 then
-		beretta1.shootTimer = beretta1.shootTimer - GetTimeStep()
-		beretta2.shootTimer = beretta2.shootTimer - GetTimeStep()
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "berettas" and GetPlayerVehicle() == 0 and not unlimitedammo then
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
+    RegisterTool("berettas", "Dual Berettas", "MOD/vox/berettas.vox")
+    SetBool("game.tool.berettas.enabled", true, true)
+    SetFloat("game.tool.berettas.ammo", 101, true)
+    damage = 0.6
+    gravity = Vec(0, 0, 0)
+    velocity = 1.4
+    reloadTime = 1.7
+    shotDelay = 0.1
+    mags = 11
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    beretta1 = {}
+    beretta1.left = true
+    beretta1.ammo = 15
+    beretta1.shootTimer = 0
+    beretta1.recoilTimer = 0
+    beretta2 = {}
+    beretta2.left = false
+    beretta2.ammo = 15
+    beretta2.shootTimer = 0
+    beretta2.recoilTimer = 0
+    ammo = beretta1.ammo + beretta2.ammo
+    reloadTimer = 0
+    lightTimer = 0
+    for i=1, ammo do
+    	berettasprojectileHandler.shells[i] = deepcopy(berettasprojectileHandler.defaultShell)
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(berettasprojectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
+        end
+        if beretta1.shootTimer > 0 or beretta2.shootTimer ~= 0 then
+        	beretta1.shootTimer = beretta1.shootTimer - GetTimeStep()
+        	beretta2.shootTimer = beretta2.shootTimer - GetTimeStep()
+        end
+    end
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/gun_shot.ogg")
+    cocksound = LoadSound("MOD/snd/pistolcock.ogg")
+    reloadsound = LoadSound("MOD/snd/deagle_reload.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "berettas" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		if not reloading then
+    			if mags == 0 or beretta1.ammo == 0 then
+    				PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    			else
+    				Shoot(beretta1)
+    			end
+    		end
+    	end
+
+    	if InputPressed("rmb") then
+    		if not reloading then
+    			if mags == 0 or beretta2.ammo == 0 then
+    				PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    			else
+    				Shoot(beretta2)
+    			end
+    		end
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.1, -0.9, 0.9))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		leftPos = TransformToParentPoint(toolTrans, Vec(-0.6, 0.4, -3.2))
+    		rightPos = TransformToParentPoint(toolTrans, Vec(0.45, 0.4, -3.2))
+
+    		local voxSize = 0.05
+    		local attach = Transform(Vec(0, 0, 0))
+    		local shapes = GetBodyShapes(b)
+    		leftgun = shapes[1]
+    		rightgun = shapes[2]
+
+    		if b ~= body then
+    			body = b
+    			tl = GetShapeLocalTransform(leftgun)
+    			tr = GetShapeLocalTransform(rightgun)
+    		end
+
+    		local t1 = 1-beretta1.recoilTimer
+    		local t2 = 1-beretta2.recoilTimer
+    		t1 = t1*t1
+    		t2 = t2*t2
+    		local offset1 = t1
+    		local offset2 = t2
+
+    		t = TransformCopy(tl)
+    		t.pos = VecAdd(t.pos, Vec(0, 1, -offset1))
+    		t.rot = QuatEuler(-90+beretta1.recoilTimer*90, 0, 0)
+    		SetShapeLocalTransform(leftgun, t)
+
+    		t = TransformCopy(tr)
+    		t.pos = VecAdd(t.pos, Vec(0, 1, -offset2))
+    		t.rot = QuatEuler(-90+beretta2.recoilTimer*90, 0, 0)
+    		SetShapeLocalTransform(rightgun, t)
+
+    		if beretta1.recoilTimer ~= 0 then
+    			beretta1.recoilTimer = beretta1.recoilTimer - dt
+    		end
+
+    		if beretta2.recoilTimer ~= 0 then
+    			beretta2.recoilTimer = beretta2.recoilTimer - dt
+    		end
+
+    		if lightTimer ~= 0 then
+    			local p = TransformToParentPoint(GetBodyTransform(b), Vec(0, 0, -2))
+    			PointLight(p, 1, 1, 1, 0.5)
+
+    			lightTimer = lightTimer - dt
+    		end
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
+    			reloadTimer = reloadTimer - GetTimeStep()
+    			if reloadTimer < 0 then
+    				beretta1.ammo = 15
+    				beretta2.ammo = 15
+    				ammo = 30
+    				reloadTimer = 0
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.6, false)
+    				reloading = false
+    			end
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "berettas" and GetPlayerVehicle(playerId) == 0 and not unlimitedammo then
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
-	UiText("Dual Berettas")
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
+    UiText("Dual Berettas")
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
