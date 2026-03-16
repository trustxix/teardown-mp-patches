# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,43 +1,4 @@
-projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false, 
-		smokeTime = 2,
-		freeTimer = 0,
-		bounces = 0,
-	},
-}
-
-function init()
-	RegisterTool("beegun", "Bee Gun", "MOD/vox/beegun.vox")
-	SetBool("game.tool.beegun.enabled", true)
-	SetFloat("game.tool.beegun.ammo", 101)
-
-	gravity = Vec(0, 0, 0)
-	velocity = 50
-	angle = 0
-	angVel = 0
-
-	activebees = 0
-	recoilTimer = 0
-	lightTimer = 0
-	holeMode = false
-	primed = false
-
-	for i=1, 50 do
-		projectileHandler.shells[i] = deepcopy(projectileHandler.defaultShell)
-	end
-
-	beeshotsound = LoadSound("MOD/snd/beeshot.ogg")
-	bouncesound = LoadSound("MOD/snd/bounce.ogg")
-	chompsound = LoadSound("MOD/snd/chomp0.ogg")
-	kamisound = LoadSound("MOD/snd/beekami.ogg")
-	ripsound = LoadSound("MOD/snd/beerip.ogg")
-	beeloop = LoadLoop("MOD/snd/beeloop.ogg")
-	beegunloop = LoadLoop("MOD/snd/beegunloop.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -114,7 +75,7 @@
 		toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.45, -2.2))
 		PlayLoop(beegunloop, toolPos)
 
-		if recoilTimer > 0 then
+		if recoilTimer ~= 0 then
 			local t = Transform()
 			t.pos = Vec(0.1, 0.1, recoilTimer)
 			t.rot = QuatEuler(recoilTimer*50, 0, 0)
@@ -123,7 +84,7 @@
 			recoilTimer = recoilTimer - dt
 		end
 
-		if lightTimer > 0 then
+		if lightTimer ~= 0 then
 			PointLight(toolPos, 1, 1, 1, 0.5)
 			lightTimer = lightTimer - dt
 		end
@@ -158,62 +119,96 @@
 	end
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "beegun" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then 
-			Shoot()
-			angVel = math.min(500, angVel + dt*9500)
-		else
-			angVel = math.max(0, angVel - dt*175)
-		end
-
-		if InputPressed("R") then
-			holeMode = not holeMode
-			SetString("hud.notification", "Hungry Bees "..(holeMode and "on" or "off"))
-		end
-
-		AnimateTool(dt)
-	end
-
-	local bees = 0
-	for key, shell in ipairs(projectileHandler.shells) do
-		if shell.active then
-			bees = bees + 1
-			if GetString("game.player.tool") == "beegun" and InputPressed("E") and not shell.explosive then
-				shell.explosive = true
-				PlaySound(kamisound, shell.pos, 1, false)
-				SetString("hud.notification", "Kamikaze Bees enabled!!!")
-			end
-			if InputPressed("C") then
-				if shell.explosive then
-					Explosion(shell.pos, 0.5)
-				end
-				shell.active = false
-				PlaySound(ripsound, shell.pos, 1, false)
-				SetString("hud.notification", "All bees dead!!!")
-			end
-			ProjectileOperations(shell)
-			shell.freeTimer = shell.freeTimer + dt
-			if shell.freeTimer > 20 then
-				if shell.explosive then
-					Explosion(shell.pos, 0.5)
-				end
-				shell.active = false
-			end
-		end
-	end
-	activebees = bees
-end
-
-function draw()
-	if GetString("game.player.tool") == "beegun" and GetPlayerVehicle() == 0 then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(activebees)
-		UiPop()
-	end
-end+function server.init()
+    RegisterTool("beegun", "Bee Gun", "MOD/vox/beegun.vox")
+    SetBool("game.tool.beegun.enabled", true, true)
+    SetFloat("game.tool.beegun.ammo", 101, true)
+    gravity = Vec(0, 0, 0)
+    velocity = 50
+    angle = 0
+    angVel = 0
+    activebees = 0
+    recoilTimer = 0
+    lightTimer = 0
+    holeMode = false
+    primed = false
+    for i=1, 50 do
+    	projectileHandler.shells[i] = deepcopy(projectileHandler.defaultShell)
+    end
+    beeloop = LoadLoop("MOD/snd/beeloop.ogg")
+    beegunloop = LoadLoop("MOD/snd/beegunloop.ogg")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local bees = 0
+        activebees = bees
+    end
+end
+
+function client.init()
+    beeshotsound = LoadSound("MOD/snd/beeshot.ogg")
+    bouncesound = LoadSound("MOD/snd/bounce.ogg")
+    chompsound = LoadSound("MOD/snd/chomp0.ogg")
+    kamisound = LoadSound("MOD/snd/beekami.ogg")
+    ripsound = LoadSound("MOD/snd/beerip.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "beegun" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then 
+    		Shoot()
+    		angVel = math.min(500, angVel + dt*9500)
+    	else
+    		angVel = math.max(0, angVel - dt*175)
+    	end
+
+    	if InputPressed("R") then
+    		holeMode = not holeMode
+    		SetString("hud.notification", "Hungry Bees "..(holeMode and "on" or "off"), true)
+    	end
+
+    	AnimateTool(dt)
+    end
+    for key, shell in ipairs(projectileHandler.shells) do
+    	if shell.active then
+    		bees = bees + 1
+    		if GetString("game.player.tool") == "beegun" and InputPressed("E") and not shell.explosive then
+    			shell.explosive = true
+    			PlaySound(kamisound, shell.pos, 1, false)
+    			SetString("hud.notification", "Kamikaze Bees enabled!!!", true)
+    		end
+    		if InputPressed("C") then
+    			if shell.explosive then
+    				Explosion(shell.pos, 0.5)
+    			end
+    			shell.active = false
+    			PlaySound(ripsound, shell.pos, 1, false)
+    			SetString("hud.notification", "All bees dead!!!", true)
+    		end
+    		ProjectileOperations(shell)
+    		shell.freeTimer = shell.freeTimer + dt
+    		if shell.freeTimer > 20 then
+    			if shell.explosive then
+    				Explosion(shell.pos, 0.5)
+    			end
+    			shell.active = false
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "beegun" and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText(activebees)
+    	UiPop()
+    end
+end
+

```
