# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,58 +1,4 @@
--- #include "common.lua"
-
-awpprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("awp", "AWP", "MOD/vox/AWP.vox")
-	SetBool("game.tool.awp.enabled", true)
-	SetFloat("game.tool.awp.ammo", 101)
-
-	awp_roundtype = 1
-	awp_roundtypes = {
-		[1] = "N",
-		[2] = "AP",
-		[3] = "IC",
-		[4] = "EX",
-	}
-
-	damage = 1.3
-	penetration = 6
-	gravity = Vec(0, 0, 0)
-	velocity = 1.7
-	reloadTime = 2.4
-	shotDelay = 1
-	ammo = 10
-	mags = 4
-	reloading = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	zoomsense = 15000
-	zoomlevel = 5
-	maxzoom = 7
-	minzoom = 0.5
-	awp_iszoomed = false
-
-	for i=1, 15 do
-		awpprojectileHandler.shells[i] = deepcopy(awpprojectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-
-	gunsound = LoadSound("MOD/snd/awp_shot.ogg")
-	cocksound = LoadSound("MOD/snd/awp_cock.ogg")
-	reloadsound = LoadSound("MOD/snd/awp_reload.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-	zoomsound = LoadSound("MOD/snd/awp_zoom.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -135,7 +81,7 @@
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.15)
 	SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.25, 0.8)
-	PlaySound(gunsound, GetPlayerTransform().pos, 0.9, false)
+	PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.9, false)
 	if not unlimitedammo then
 		ammo = ammo - 1
 	end
@@ -182,158 +128,208 @@
 		return
 	end
 	reloading = true
-	PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	reloadTimer = reloadTime
 	mags = mags - 1
 end
 
 function Zoom()
 	awp_iszoomed = not awp_iszoomed
-	PlaySound(zoomsound, GetPlayerTransform().pos, 0.5, false)
-end
-
-function tick(dt)
-	if awp_iszoomed then
-		SetString("game.player.tool", "awp")
-	end
-
-	if GetString("game.player.tool") == "awp" and GetPlayerVehicle() == 0 then
-		if InputPressed("esc") then awp_iszoomed = false end
-
-		if InputPressed("lmb") and not reloading then
-			if mags == 0 or ammo == 0 then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			else
-				Shoot()
-			end
-		end
-		
-		if InputPressed("rmb") then Zoom() end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0, heightOffset, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.55, -3.5))
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
-			if ammo < 10 and mags > 1 and InputPressed("R") then
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
-					ammo = 10
-					reloadTimer = 0
-					PlaySound(cocksound)
-					reloading = false
-				end
-			end
-		end
-
-		for key, shell in ipairs(awpprojectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
-			end
-		end
-
-		if InputPressed("C") then 
-			if awp_roundtype == 4 then awp_roundtype = 1 else awp_roundtype = awp_roundtype + 1 end
-		end
-	
-		if awp_iszoomed then
-			toolPos = GetPlayerCameraTransform().pos
-			local mousewheel = InputValue("mousewheel")
-			if mousewheel ~= 0 then
-				zoomlevel = clamp(zoomlevel - mousewheel/2, minzoom, maxzoom)
-			end
-
-			local pvel = GetPlayerVelocity()
-			local mx, my = InputValue("mousedx"), -InputValue("mousedy")
-	
-			local ct = GetCameraTransform()
-			local pt = GetPlayerTransform()
-			
-			local upAngle = orientation(Transform(pt.pos, ct.rot), 1)
-			local downAngle = orientation(Transform(pt.pos, ct.rot), -1)
-			if ((upAngle > 0.98 and my > 0) or (downAngle > 0.98 and my < 0)) then
-			  my = 0
-			end
-	
-			pt.pos[2] = pt.pos[2] + 1.8
-			local target = Vec(mx/(zoomsense/zoomlevel), my/(zoomsense/zoomlevel), -1)
-			target = TransformToParentVec(ct, target)
-			ct.rot = QuatLookAt(ct, target)
-	
-			SetCameraTransform(Transform(pt.pos, ct.rot), zoomlevel*10)
-			SetPlayerTransform(Transform(GetPlayerTransform().pos, ct.rot))
-	
-			SetPlayerVelocity(pvel)
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "awp" and GetPlayerVehicle() == 0 then
-		if awp_iszoomed then
-			UiPush()
-				UiTranslate(UiCenter(), UiMiddle())
-				UiAlign("center middle")
-				UiImage("MOD/img/awpscope.png")
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
-					UiText(ammo.."/"..10*math.max(0,(mags-1)).." ("..awp_roundtypes[awp_roundtype]..")")
-				end
-			UiPop()
-		else
-			UiPush()
-				UiTranslate(UiCenter(), UiHeight()-60)
-				UiAlign("center middle")
-				UiColor(1, 1, 1)
-				UiFont("bold.ttf", 32)
-				UiTextOutline(0,0,0,1,0.1)
-				UiText(awp_roundtypes[awp_roundtype])
-			UiPop()
-		end
-	end
-end+	PlaySound(zoomsound, GetPlayerTransform(playerId).pos, 0.5, false)
+end
+
+function server.init()
+    RegisterTool("awp", "AWP", "MOD/vox/AWP.vox")
+    SetBool("game.tool.awp.enabled", true, true)
+    SetFloat("game.tool.awp.ammo", 101, true)
+    awp_roundtype = 1
+    awp_roundtypes = {
+    	[1] = "N",
+    	[2] = "AP",
+    	[3] = "IC",
+    	[4] = "EX",
+    }
+    damage = 1.3
+    penetration = 6
+    gravity = Vec(0, 0, 0)
+    velocity = 1.7
+    reloadTime = 2.4
+    shotDelay = 1
+    ammo = 10
+    mags = 4
+    reloading = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    zoomsense = 15000
+    zoomlevel = 5
+    maxzoom = 7
+    minzoom = 0.5
+    awp_iszoomed = false
+    for i=1, 15 do
+    	awpprojectileHandler.shells[i] = deepcopy(awpprojectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if awp_iszoomed then
+        	SetString("game.player.tool", "awp", true)
+        end
+    end
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/awp_shot.ogg")
+    cocksound = LoadSound("MOD/snd/awp_cock.ogg")
+    reloadsound = LoadSound("MOD/snd/awp_reload.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+    zoomsound = LoadSound("MOD/snd/awp_zoom.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "awp" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("esc") then awp_iszoomed = false end
+
+    	if InputPressed("lmb") and not reloading then
+    		if mags == 0 or ammo == 0 then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		else
+    			Shoot()
+    		end
+    	end
+
+    	if InputPressed("rmb") then Zoom() end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.55, -3.5))
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
+    		if ammo < 10 and mags > 1 and InputPressed("R") then
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
+    				ammo = 10
+    				reloadTimer = 0
+    				PlaySound(cocksound)
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	for key, shell in ipairs(awpprojectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		end
+    	end
+
+    	if InputPressed("C") then 
+    		if awp_roundtype == 4 then awp_roundtype = 1 else awp_roundtype = awp_roundtype + 1 end
+    	end
+
+    	if awp_iszoomed then
+    		toolPos = GetPlayerCameraTransform(playerId).pos
+    		local mousewheel = InputValue("mousewheel")
+    		if mousewheel ~= 0 then
+    			zoomlevel = clamp(zoomlevel - mousewheel/2, minzoom, maxzoom)
+    		end
+
+    		local pvel = GetPlayerVelocity(playerId)
+    		local mx, my = InputValue("mousedx"), -InputValue("mousedy")
+
+    		local ct = GetCameraTransform()
+    		local pt = GetPlayerTransform(playerId)
+
+    		local upAngle = orientation(Transform(pt.pos, ct.rot), 1)
+    		local downAngle = orientation(Transform(pt.pos, ct.rot), -1)
+    		if ((upAngle > 0.98 and my > 0) or (downAngle > 0.98 and my < 0)) then
+    		  my = 0
+    		end
+
+    		pt.pos[2] = pt.pos[2] + 1.8
+    		local target = Vec(mx/(zoomsense/zoomlevel), my/(zoomsense/zoomlevel), -1)
+    		target = TransformToParentVec(ct, target)
+    		ct.rot = QuatLookAt(ct, target)
+
+    		SetCameraTransform(Transform(pt.pos, ct.rot), zoomlevel*10)
+    		SetPlayerTransform(playerId, Transform(GetPlayerTransform(playerId).pos, ct.rot))
+
+    		SetPlayerVelocity(playerId, pvel)
+    	end
+
+    	if shootTimer > 0 or ammo == 0 then
+    		shootTimer = shootTimer - dt
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "awp" and GetPlayerVehicle(playerId) == 0 then
+    	if awp_iszoomed then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiMiddle())
+    			UiAlign("center middle")
+    			UiImage("MOD/img/awpscope.png")
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
+    				UiText(ammo.."/"..10*math.max(0,(mags-1)).." ("..awp_roundtypes[awp_roundtype]..")")
+    			end
+    		UiPop()
+    	else
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			UiText(awp_roundtypes[awp_roundtype])
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
-	UiText("AWP")
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
+    UiText("AWP")
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
