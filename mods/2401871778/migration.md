# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,47 +1,4 @@
-grenadelauncherprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false, 
-		grenadeTimer = 0, 
-		smokeTime = 2, 
-		bounces = 0,
-	},
-}
-
-function init()
-	RegisterTool("mgl", "MGL", "MOD/vox/mgl.vox")
-	SetBool("game.tool.mgl.enabled", true)
-	SetFloat("game.tool.mgl.ammo", 101)
-
-	sticky = false
-	gravity = Vec(0, -50, 0)
-	velocity = 80
-	reloadTime = 2
-	fuseTime = 5
-	ammo = 6
-	mags = 13
-	reloading = false
-	reloadTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-
-	for i=1, 250 do
-		grenadelauncherprojectileHandler.shells[i] = deepcopy(grenadelauncherprojectileHandler.defaultShell)
-	end
-
-	grenadelauncherrocketsound = LoadSound("MOD/snd/mgl.ogg")
-	grenadelauncherboomsound = LoadSound("MOD/snd/rpg_boom.ogg")
-	grenadelauncherreloadsound = LoadSound("MOD/snd/mgl_reload.ogg")
-	grenadelauncherdryfiresound = LoadSound("MOD/snd/mgl_dryfire.ogg")
-	grenadelaunchercocksound = LoadSound("MOD/snd/rpg_cock.ogg")
-	grenadelauncherbouncesound = LoadSound("MOD/snd/mgl_bounce.ogg")
-	grenadelauncherrefillsound = LoadSound("MOD/snd/refill.ogg")
-	grenadelauncherbeepsound = LoadSound("MOD/snd/beep.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -127,124 +84,157 @@
 	reloadTimer = reloadTime
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "mgl" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			if not reloading then
-				if ammo == 0 or mags == 0 then
-					PlaySound(grenadelauncherdryfiresound, GetPlayerTransform().pos, 1, false)
-				else
-					Shoot()
-				end
-			end
-		end
-
-		if InputPressed("rmb") then
-			for key, shell in ipairs(grenadelauncherprojectileHandler.shells) do
-				if shell.active then
-					shell.grenadeTimer = 0.15
-				end
-			end
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.1, 0.1, 0))
-			SetToolTransform(offset)
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0.1, 0.1, recoilTimer)
-				t.rot = QuatEuler(recoilTimer*50, 0, 0)
-				SetToolTransform(t)
-
-				recoilTimer = recoilTimer - dt
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
-			if ammo < 6 and mags > 1 and InputPressed("R") then
-				GrenadeReload()
-			end
-
-			if GetBool("ammobox.refill") then
-				SetBool("ammobox.refill", false)
-				mags = mags + 1
-				PlaySound(grenadelauncherrefillsound, GetCameraTransform().pos, 1, false)
-			end
-		
-			if reloading then
-				reloadTimer = reloadTimer - dt
-				if reloadTimer < 0 then
-					PlaySound(grenadelaunchercocksound, GetPlayerTransform().pos, 0.75, false)
-					ammo = 6
-					mags = mags - 1
-					reloadTimer = 0
-					reloading = false
-				end
-			end
-		end
-
-		if InputPressed("X") then
-			fuseTime = math.min(20, fuseTime + 1)
-		elseif InputPressed("Z") then
-			fuseTime = math.max(1, fuseTime - 1)
-		end
-
-		if InputPressed("C") then
-			sticky = not sticky
-			fuseTime = 5
-		end
-	end
-
-	for key, shell in ipairs(grenadelauncherprojectileHandler.shells) do
-		if shell.grenadeTimer > 0 then
-			shell.grenadeTimer = shell.grenadeTimer - dt
-			if shell.grenadeTimer < 0.1 then
-				shell.active = false
-				shell.grenadeTimer = 0
-				PlaySound(grenadelauncherboomsound, shell.grenadepos, 1, false)
-				Explosion(shell.grenadepos, 2)
-			end
-		end
-
-		if shell.active then
-			GrenadeLauncherOperations(shell)
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "mgl" then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle")
-			UiImage("ui/hud/crosshair-launcher.png")
-		UiPop()
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			if reloading then
-				UiText("Reloading")
-			else
-				local type = fuseTime.."Sec"
-				if sticky then type = "Sticky" end
-				if not unlimitedammo then
-					UiText(ammo.."/"..6*math.max(0,(mags-1)).."- "..type)
-				else
-					UiText(type)
-				end
-			end
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("mgl", "MGL", "MOD/vox/mgl.vox")
+    SetBool("game.tool.mgl.enabled", true, true)
+    SetFloat("game.tool.mgl.ammo", 101, true)
+    sticky = false
+    gravity = Vec(0, -50, 0)
+    velocity = 80
+    reloadTime = 2
+    fuseTime = 5
+    ammo = 6
+    mags = 13
+    reloading = false
+    reloadTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    for i=1, 250 do
+    	grenadelauncherprojectileHandler.shells[i] = deepcopy(grenadelauncherprojectileHandler.defaultShell)
+    end
+end
+
+function client.init()
+    grenadelauncherrocketsound = LoadSound("MOD/snd/mgl.ogg")
+    grenadelauncherboomsound = LoadSound("MOD/snd/rpg_boom.ogg")
+    grenadelauncherreloadsound = LoadSound("MOD/snd/mgl_reload.ogg")
+    grenadelauncherdryfiresound = LoadSound("MOD/snd/mgl_dryfire.ogg")
+    grenadelaunchercocksound = LoadSound("MOD/snd/rpg_cock.ogg")
+    grenadelauncherbouncesound = LoadSound("MOD/snd/mgl_bounce.ogg")
+    grenadelauncherrefillsound = LoadSound("MOD/snd/refill.ogg")
+    grenadelauncherbeepsound = LoadSound("MOD/snd/beep.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "mgl" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		if not reloading then
+    			if ammo == 0 or mags == 0 then
+    				PlaySound(grenadelauncherdryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    			else
+    				Shoot()
+    			end
+    		end
+    	end
+
+    	if InputPressed("rmb") then
+    		for key, shell in ipairs(grenadelauncherprojectileHandler.shells) do
+    			if shell.active then
+    				shell.grenadeTimer = 0.15
+    			end
+    		end
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.1, 0.1, 0))
+    		SetToolTransform(offset)
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0.1, 0.1, recoilTimer)
+    			t.rot = QuatEuler(recoilTimer*50, 0, 0)
+    			SetToolTransform(t)
+
+    			recoilTimer = recoilTimer - dt
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
+    		if ammo < 6 and mags > 1 and InputPressed("R") then
+    			GrenadeReload()
+    		end
+
+    		if GetBool("ammobox.refill") then
+    			SetBool("ammobox.refill", false, true)
+    			mags = mags + 1
+    			PlaySound(grenadelauncherrefillsound, GetCameraTransform().pos, 1, false)
+    		end
+
+    		if reloading then
+    			reloadTimer = reloadTimer - dt
+    			if reloadTimer < 0 then
+    				PlaySound(grenadelaunchercocksound, GetPlayerTransform(playerId).pos, 0.75, false)
+    				ammo = 6
+    				mags = mags - 1
+    				reloadTimer = 0
+    				reloading = false
+    			end
+    		end
+    	end
+
+    	if InputPressed("X") then
+    		fuseTime = math.min(20, fuseTime + 1)
+    	elseif InputPressed("Z") then
+    		fuseTime = math.max(1, fuseTime - 1)
+    	end
+
+    	if InputPressed("C") then
+    		sticky = not sticky
+    		fuseTime = 5
+    	end
+    end
+    for key, shell in ipairs(grenadelauncherprojectileHandler.shells) do
+    	if shell.grenadeTimer ~= 0 then
+    		shell.grenadeTimer = shell.grenadeTimer - dt
+    		if shell.grenadeTimer < 0.1 then
+    			shell.active = false
+    			shell.grenadeTimer = 0
+    			PlaySound(grenadelauncherboomsound, shell.grenadepos, 1, false)
+    			Explosion(shell.grenadepos, 2)
+    		end
+    	end
+
+    	if shell.active then
+    		GrenadeLauncherOperations(shell)
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "mgl" then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle")
+    		UiImage("ui/hud/crosshair-launcher.png")
+    	UiPop()
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if reloading then
+    			UiText("Reloading")
+    		else
+    			local type = fuseTime.."Sec"
+    			if sticky then type = "Sticky" end
+    			if not unlimitedammo then
+    				UiText(ammo.."/"..6*math.max(0,(mags-1)).."- "..type)
+    			else
+    				UiText(type)
+    			end
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
-	UiText("Multi Grenade Launcher")
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
+    UiText("Multi Grenade Launcher")
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
