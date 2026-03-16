# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,57 +1,4 @@
-#include "options.lua"
-
-hookShootgunMenuOpen = false
-hookshotgunprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("cresta-hookshotgun", "Hook Shotgun", "MOD/vox/hookshotgun.vox")
-	SetBool("game.tool.cresta-hookshotgun.enabled", true)
-	SetString("game.tool.cresta-hookshotgun.ammo.display","")
-	SetFloat("game.tool.cresta-hookshotgun.ammo", 101)
-
-	STATE_READY = 0
-	STATE_THROWN = 1
-	STATE_HOOKED = 2
-	STATE_PULLING = 3
-	state = STATE_READY
-
-	line = {}
-	line.active = false
-
-	pellets = GetFloat("savegame.mod.pellets")
-	if pellets == 0 then pellets = 50 end
-	pelletdamage = GetFloat("savegame.mod.pelletdamage")
-	if pelletdamage == 0 then pelletdamage = 50 end
-	pullpower = GetFloat("savegame.mod.pullpower")
-	if pullpower == 0 then pullpower = 120 end
-	kickbackpower = GetFloat("savegame.mod.kickbackpower")
-	if kickbackpower == 0 then kickbackpower = 40 end
-
-	damage = pelletdamage/100
-	gravity = Vec(0, 0, 0)
-	velocity = 75
-	hookvelocity = 1
-	shotDelay = 0.1
-
-	for i=1, 1500 do
-		hookshotgunprojectileHandler.shells[i] = deepcopy(hookshotgunprojectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	recoilTimer = 0
-	lightTimer = 0
-	pullTimer = 0
-
-	shootsound = LoadSound("MOD/snd/gunshot.ogg")
-	shoothooksound = LoadSound("MOD/snd/shoothook.ogg")
-	hookhitsound = LoadSound("MOD/snd/hookhit.ogg")
-	pullsound = LoadSound("MOD/snd/hookpull.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -93,7 +40,7 @@
 end
 
 function Shoot()
-	if shootTimer > 0 then
+	if shootTimer ~= 0 then
 		return
 	end
 
@@ -122,15 +69,15 @@
 	end
 
 	local recoildir = TransformToParentVec(ct, Vec(0, 0, kickbackpower/6))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	local oldvel = VecCopy(vel)
 	vel = VecAdd(vel, recoildir)
 	if VecLength(vel) > kickbackpower/3 then vel = oldvel end
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
 
 	SpawnParticle("fire", toolPos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.15)
 	SpawnParticle("darksmoke", toolPos, Vec(0, 1.0+math.random(1,5)*0.1, 0), 0.5, 2.5)
-	PlaySound(shootsound, GetPlayerTransform().pos, 0.75)
+	PlaySound(shootsound, GetPlayerTransform(playerId).pos, 0.75)
 
 	shootTimer = shotDelay
 	recoilTimer = shotDelay
@@ -141,7 +88,7 @@
 	local aimpos, dist = GetAimPos()
 	local startPos = TransformToParentPoint(GetCameraTransform(), Vec(0.45, -0.15, -1))
 	local direction = VecSub(aimpos, startPos)
-	PlaySound(shoothooksound, GetPlayerTransform().pos, 0.6)
+	PlaySound(shoothooksound, GetPlayerTransform(playerId).pos, 0.6)
 
 	line.gravity = gravity
 	line.pos = VecCopy(startPos)
@@ -149,7 +96,7 @@
 end
 
 function Pull()
-	PlaySound(pullsound, GetPlayerTransform().pos, 0.5)
+	PlaySound(pullsound, GetPlayerTransform(playerId).pos, 0.5)
 	local s = InputDown("s")
 	pullTimer = 0.45
 
@@ -205,7 +152,7 @@
 		
 		movedir = VecScale(movedir, scale*dirscale)
 		movedir = VecScale(movedir, pullpower)
-		SetPlayerVelocity(movedir)
+		SetPlayerVelocity(playerId, movedir)
 	end
 end
 
@@ -248,110 +195,156 @@
 	line.pos = point2
 end
 
-function draw()
-	if GetString("game.player.tool") == "cresta-hookshotgun" and hookShootgunMenuOpen then
-		drawHookShootgunOptions()
-	end
-end
-
-function tick(dt)
-	if GetString("game.player.tool") == "cresta-hookshotgun" and InputPressed("r") then hookShootgunMenuOpen = not hookShootgunMenuOpen end
-	if GetString("game.player.tool") == "cresta-hookshotgun" and GetBool("game.player.canusetool") then
-		if InputPressed("lmb") then
-			Shoot()
-		end
-		if PauseMenuButton("Hook Shootgun") then
-			hookShootgunMenuOpen = true
-		end
-		if InputPressed("esc") then hookShootgunMenuOpen = false end
-
-		if InputPressed("rmb") then
-			if state == STATE_READY then
-				line.active = true
-				Hook()
-				state = STATE_THROWN
-			elseif state == STATE_HOOKED then
-				Pull()
-				state = STATE_READY
-				line.active = false
-			elseif state == STATE_THROWN then
-				state = STATE_READY
-				line.active = false
-			end
-		end
-
-		if line.active then
-			handPos = TransformToParentPoint(GetCameraTransform(), Vec(0.35, -0.45, -2))
-			if state == STATE_THROWN then
-				HookOperations(line)
-			elseif state == STATE_HOOKED then
-				hookpos = TransformToParentPoint(GetBodyTransform(hookbody), localhookpos)
-				DrawLine(handPos, hookpos, 0, 0, 0)
-				DrawBodyOutline(GetShapeBody(hookbody), 0.5)
-			end
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local heightOffset = InputDown("ctrl") and 0.3 or 0.2
-			local offset = Transform(Vec(0, heightOffset, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.1))
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, heightOffset, recoilTimer*2)
-				t.rot = QuatEuler(recoilTimer*90, 0, 0)
-				SetToolTransform(t)
-				recoilTimer = recoilTimer - dt
-			end
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 1, 1, 0.5)
-				lightTimer = lightTimer - dt
-			end
-
-			if pullTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, pullTimer)
-				t.rot = QuatEuler(pullTimer*60, 0, 0)
-				SetToolTransform(t)
-
-				pullTimer = pullTimer - dt
-			end
-
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				hook = shapes[2]
-				hookTrans = GetShapeLocalTransform(hook)
-			end
-
-			bt = TransformCopy(hookTrans)
-			if line.active then
-				if state == STATE_HOOKED then
-					bt.pos = hookpos
-					bt.rot = QuatLookAt(GetCameraTransform().pos, hookpos)
-				else
-					bt.pos = line.pos
-					bt.rot = QuatLookAt(GetCameraTransform().pos, line.pos)
-				end
-				bt.rot = QuatRotateQuat(bt.rot, QuatEuler(-90, 0, 0))
-				SetShapeLocalTransform(hook, TransformToLocalTransform(GetBodyTransform(GetToolBody()), bt))
-			else
-				SetShapeLocalTransform(hook, bt)
-			end
-		end
-		
-		if shootTimer > 0 then
-			shootTimer = shootTimer - GetTimeStep()
-		end
-	end
-
-	for key, shell in ipairs(hookshotgunprojectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-end+function server.init()
+    RegisterTool("cresta-hookshotgun", "Hook Shotgun", "MOD/vox/hookshotgun.vox")
+    SetBool("game.tool.cresta-hookshotgun.enabled", true, true)
+    SetString("game.tool.cresta-hookshotgun.ammo.display","", true)
+    SetFloat("game.tool.cresta-hookshotgun.ammo", 101, true)
+    STATE_READY = 0
+    STATE_THROWN = 1
+    STATE_HOOKED = 2
+    STATE_PULLING = 3
+    state = STATE_READY
+    line = {}
+    line.active = false
+    pellets = GetFloat("savegame.mod.pellets")
+end
+
+function client.init()
+    if pellets == 0 then pellets = 50 end
+    pelletdamage = GetFloat("savegame.mod.pelletdamage")
+    if pelletdamage == 0 then pelletdamage = 50 end
+    pullpower = GetFloat("savegame.mod.pullpower")
+    if pullpower == 0 then pullpower = 120 end
+    kickbackpower = GetFloat("savegame.mod.kickbackpower")
+    if kickbackpower == 0 then kickbackpower = 40 end
+
+    damage = pelletdamage/100
+    gravity = Vec(0, 0, 0)
+    velocity = 75
+    hookvelocity = 1
+    shotDelay = 0.1
+
+    for i=1, 1500 do
+    	hookshotgunprojectileHandler.shells[i] = deepcopy(hookshotgunprojectileHandler.defaultShell)
+    end
+
+    shootTimer = 0
+    recoilTimer = 0
+    lightTimer = 0
+    pullTimer = 0
+
+    shootsound = LoadSound("MOD/snd/gunshot.ogg")
+    shoothooksound = LoadSound("MOD/snd/shoothook.ogg")
+    hookhitsound = LoadSound("MOD/snd/hookhit.ogg")
+    pullsound = LoadSound("MOD/snd/hookpull.ogg")
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "cresta-hookshotgun" and InputPressed("r") then hookShootgunMenuOpen = not hookShootgunMenuOpen end
+    if GetString("game.player.tool") == "cresta-hookshotgun" and GetBool("game.player.canusetool") then
+    	if InputPressed("lmb") then
+    		Shoot()
+    	end
+    	if PauseMenuButton("Hook Shootgun") then
+    		hookShootgunMenuOpen = true
+    	end
+    	if InputPressed("esc") then hookShootgunMenuOpen = false end
+
+    	if InputPressed("rmb") then
+    		if state == STATE_READY then
+    			line.active = true
+    			Hook()
+    			state = STATE_THROWN
+    		elseif state == STATE_HOOKED then
+    			Pull()
+    			state = STATE_READY
+    			line.active = false
+    		elseif state == STATE_THROWN then
+    			state = STATE_READY
+    			line.active = false
+    		end
+    	end
+
+    	if line.active then
+    		handPos = TransformToParentPoint(GetCameraTransform(), Vec(0.35, -0.45, -2))
+    		if state == STATE_THROWN then
+    			HookOperations(line)
+    		elseif state == STATE_HOOKED then
+    			hookpos = TransformToParentPoint(GetBodyTransform(hookbody), localhookpos)
+    			DrawLine(handPos, hookpos, 0, 0, 0)
+    			DrawBodyOutline(GetShapeBody(hookbody), 0.5)
+    		end
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local heightOffset = InputDown("ctrl") and 0.3 or 0.2
+    		local offset = Transform(Vec(0, heightOffset, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.6, -2.1))
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, heightOffset, recoilTimer*2)
+    			t.rot = QuatEuler(recoilTimer*90, 0, 0)
+    			SetToolTransform(t)
+    			recoilTimer = recoilTimer - dt
+    		end
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 1, 1, 0.5)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if pullTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, pullTimer)
+    			t.rot = QuatEuler(pullTimer*60, 0, 0)
+    			SetToolTransform(t)
+
+    			pullTimer = pullTimer - dt
+    		end
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			hook = shapes[2]
+    			hookTrans = GetShapeLocalTransform(hook)
+    		end
+
+    		bt = TransformCopy(hookTrans)
+    		if line.active then
+    			if state == STATE_HOOKED then
+    				bt.pos = hookpos
+    				bt.rot = QuatLookAt(GetCameraTransform().pos, hookpos)
+    			else
+    				bt.pos = line.pos
+    				bt.rot = QuatLookAt(GetCameraTransform().pos, line.pos)
+    			end
+    			bt.rot = QuatRotateQuat(bt.rot, QuatEuler(-90, 0, 0))
+    			SetShapeLocalTransform(hook, TransformToLocalTransform(GetBodyTransform(GetToolBody()), bt))
+    		else
+    			SetShapeLocalTransform(hook, bt)
+    		end
+    	end
+
+    	if shootTimer ~= 0 then
+    		shootTimer = shootTimer - GetTimeStep()
+    	end
+    end
+
+    for key, shell in ipairs(hookshotgunprojectileHandler.shells) do
+    	if shell.active then
+    		ProjectileOperations(shell)
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "cresta-hookshotgun" and hookShootgunMenuOpen then
+    	drawHookShootgunOptions()
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
@@ -1,18 +1,4 @@
-function init()
-	pellets = GetFloat("savegame.mod.pellets")
-	if pellets == 0 then pellets = 50 end
-	pelletdamage = GetFloat("savegame.mod.pelletdamage")
-	if pelletdamage == 0 then pelletdamage = 50 end
-	pullpower = GetFloat("savegame.mod.pullpower")
-	if pullpower == 0 then pullpower = 120 end
-	kickbackpower = GetFloat("savegame.mod.kickbackpower")
-	if kickbackpower == 0 then kickbackpower = 40 end
-end
-
-function draw()
-	drawHookShootgunOptions()
-end
-
+#version 2
 function drawHookShootgunOptions()
 	UiMakeInteractive()
 	UiTranslate(UiCenter(), 350)
@@ -34,7 +20,7 @@
 		UiTranslate(-75, 20)
 		UiColor(0.2, 0.6, 1)
 		UiText(pellets)
-		SetFloat("savegame.mod.pellets", pellets)
+		SetFloat("savegame.mod.pellets", pellets, true)
 	UiPop()
 
 	UiTranslate(0, 80)
@@ -46,7 +32,7 @@
 		UiTranslate(-75, 20)
 		UiColor(0.2, 0.6, 1)
 		UiText(pelletdamage)
-		SetFloat("savegame.mod.pelletdamage", pelletdamage)
+		SetFloat("savegame.mod.pelletdamage", pelletdamage, true)
 	UiPop()
 
 	UiTranslate(0, 80)
@@ -58,7 +44,7 @@
 		UiTranslate(-75, 20)
 		UiColor(0.2, 0.6, 1)
 		UiText(pullpower)
-		SetFloat("savegame.mod.pullpower", pullpower)
+		SetFloat("savegame.mod.pullpower", pullpower, true)
 	UiPop()
 
 	UiTranslate(0, 80)
@@ -70,7 +56,7 @@
 		UiTranslate(-75, 20)
 		UiColor(0.2, 0.6, 1)
 		UiText(kickbackpower)
-		SetFloat("savegame.mod.kickbackpower", kickbackpower)
+		SetFloat("savegame.mod.kickbackpower", kickbackpower, true)
 	UiPop()
 
 	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
@@ -103,4 +89,20 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    pellets = GetFloat("savegame.mod.pellets")
+    if pellets == 0 then pellets = 50 end
+    pelletdamage = GetFloat("savegame.mod.pelletdamage")
+    if pelletdamage == 0 then pelletdamage = 50 end
+    pullpower = GetFloat("savegame.mod.pullpower")
+    if pullpower == 0 then pullpower = 120 end
+    kickbackpower = GetFloat("savegame.mod.kickbackpower")
+    if kickbackpower == 0 then kickbackpower = 40 end
+end
+
+function client.draw()
+    drawHookShootgunOptions()
+end
+

```
