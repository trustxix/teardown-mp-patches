# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,48 +1,4 @@
-sg553projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("sg553", "SG-553", "MOD/vox/sg553.vox")
-	SetBool("game.tool.sg553.enabled", true)
-	SetFloat("game.tool.sg553.ammo", 101)
-
-	damage = 0.65
-	gravity = Vec(0, 0, 0)
-	velocity = 1.5
-
-	gunsound = LoadSound("MOD/snd/sg0.ogg")
-	cocksound = LoadSound("MOD/snd/guncock.ogg")
-	reloadsound = LoadSound("MOD/snd/reload.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-
-	reloadTime = 1.6
-	shotDelay = 0.095
-	spreadTimer = 0
-	ammo = 30
-	mags = 6
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	zoomsense = 15000
-	zoomlevel = 5
-	maxzoom = 8
-	minzoom = 3
-	sg_iszoomed = false
-
-	for i=1, ammo do
-		sg553projectileHandler.shells[i] = deepcopy(sg553projectileHandler.defaultShell)
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
@@ -109,7 +65,7 @@
 
 	sg553projectileHandler.shellNum = (sg553projectileHandler.shellNum%#sg553projectileHandler.shells) + 1
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(gunsound, GetPlayerTransform().pos, 0.4, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.4, false)
 	
 	if not unlimitedammo then
 		ammo = ammo - 1
@@ -144,144 +100,186 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
-function tick(dt)
-	if sg_iszoomed then
-		SetString("game.player.tool", "sg553")
-	end
-
-	if GetString("game.player.tool") == "sg553" and GetPlayerVehicle() == 0 then
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
-		if InputPressed("rmb") then sg_iszoomed = not sg_iszoomed end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0, heightOffset, 0))
-			SetToolTransform(offset)
-			toolPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.355, -0.55, -2.2))
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
-		for key, shell in ipairs(sg553projectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
-			end
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	end
-
-	if sg_iszoomed then
-		toolPos = GetPlayerCameraTransform().pos
-		local mousewheel = InputValue("mousewheel")
-		if mousewheel ~= 0 then
-			zoomlevel = clamp(zoomlevel - mousewheel/2, minzoom, maxzoom)
-		end
-
-		local pvel = GetPlayerVelocity()
-		local mx, my = InputValue("mousedx"), -InputValue("mousedy")
-
-		local ct = GetCameraTransform()
-		local pt = GetPlayerTransform()
-		
-		local upAngle = orientation(Transform(pt.pos, ct.rot), 1)
-		local downAngle = orientation(Transform(pt.pos, ct.rot), -1)
-		if ((upAngle > 0.98 and my > 0) or (downAngle > 0.98 and my < 0)) then
-		  my = 0
-		end
-
-		pt.pos[2] = pt.pos[2] + 1.8
-		local target = Vec(mx/(zoomsense/zoomlevel), my/(zoomsense/zoomlevel), -1)
-		target = TransformToParentVec(ct, target)
-		ct.rot = QuatLookAt(ct, target)
-
-		SetCameraTransform(Transform(pt.pos, ct.rot), zoomlevel*10)
-		SetPlayerTransform(Transform(GetPlayerTransform().pos, ct.rot))
-
-		SetPlayerVelocity(pvel)
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "sg553" and GetPlayerVehicle() == 0 then
-		if sg_iszoomed then
-			UiPush()
-				UiTranslate(UiCenter(), UiMiddle())
-				UiAlign("center middle")
-				UiImage("MOD/img/scope.png")
-			UiPop()
-		end
-
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
+    RegisterTool("sg553", "SG-553", "MOD/vox/sg553.vox")
+    SetBool("game.tool.sg553.enabled", true, true)
+    SetFloat("game.tool.sg553.ammo", 101, true)
+    damage = 0.65
+    gravity = Vec(0, 0, 0)
+    velocity = 1.5
+    reloadTime = 1.6
+    shotDelay = 0.095
+    spreadTimer = 0
+    ammo = 30
+    mags = 6
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    zoomsense = 15000
+    zoomlevel = 5
+    maxzoom = 8
+    minzoom = 3
+    sg_iszoomed = false
+    for i=1, ammo do
+    	sg553projectileHandler.shells[i] = deepcopy(sg553projectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if sg_iszoomed then
+        	SetString("game.player.tool", "sg553", true)
+        end
+    end
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/sg0.ogg")
+    cocksound = LoadSound("MOD/snd/guncock.ogg")
+    reloadsound = LoadSound("MOD/snd/reload.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "sg553" and GetPlayerVehicle(playerId) == 0 then
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
+    	if InputPressed("rmb") then sg_iszoomed = not sg_iszoomed end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.355, -0.55, -2.2))
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
+    	for key, shell in ipairs(sg553projectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		end
+    	end
+
+    	if shootTimer > 0 or ammo == 0 then
+    		shootTimer = shootTimer - dt
+    	end
+    end
+
+    if sg_iszoomed then
+    	toolPos = GetPlayerCameraTransform(playerId).pos
+    	local mousewheel = InputValue("mousewheel")
+    	if mousewheel ~= 0 then
+    		zoomlevel = clamp(zoomlevel - mousewheel/2, minzoom, maxzoom)
+    	end
+
+    	local pvel = GetPlayerVelocity(playerId)
+    	local mx, my = InputValue("mousedx"), -InputValue("mousedy")
+
+    	local ct = GetCameraTransform()
+    	local pt = GetPlayerTransform(playerId)
+
+    	local upAngle = orientation(Transform(pt.pos, ct.rot), 1)
+    	local downAngle = orientation(Transform(pt.pos, ct.rot), -1)
+    	if ((upAngle > 0.98 and my > 0) or (downAngle > 0.98 and my < 0)) then
+    	  my = 0
+    	end
+
+    	pt.pos[2] = pt.pos[2] + 1.8
+    	local target = Vec(mx/(zoomsense/zoomlevel), my/(zoomsense/zoomlevel), -1)
+    	target = TransformToParentVec(ct, target)
+    	ct.rot = QuatLookAt(ct, target)
+
+    	SetCameraTransform(Transform(pt.pos, ct.rot), zoomlevel*10)
+    	SetPlayerTransform(playerId, Transform(GetPlayerTransform(playerId).pos, ct.rot))
+
+    	SetPlayerVelocity(playerId, pvel)
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "sg553" and GetPlayerVehicle(playerId) == 0 then
+    	if sg_iszoomed then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiMiddle())
+    			UiAlign("center middle")
+    			UiImage("MOD/img/scope.png")
+    		UiPop()
+    	end
+
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
-	UiText("SG-553")
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
+    UiText("SG-553")
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
