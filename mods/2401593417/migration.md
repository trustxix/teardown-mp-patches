# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,27 +1,5 @@
-#include "options.lua"
-
-mjolneroptionsvisible = false
-
-function init()
-	RegisterTool("mjolner", "Mjölner", "MOD/vox/mjolner2.vox")
-	SetBool("game.tool.mjolner.enabled", true)
-	SetString("game.tool.mjolner.ammo.display","")
-	SetFloat("game.tool.mjolner.ammo", 101)
-
-	electricitySound = LoadSound("MOD/snd/electricity.ogg")
-	lightningSound = LoadSound("thunder-strike.ogg")
-	lightningTimer = 0
-	swingTimer = 0
-	swingCooldown = 0
-	strength = 25
-	maxMass = 2000000
-	maxDist = 15
-
-	explosionSize = GetFloat("savegame.mod.explosion")
-	if explosionSize == 0 then explosionSize = 2 end
-end
-
-function GetAimPos()
+#version 2
+unction GetAimPos()
 	local player = GetCameraTransform()
 	local forwardPos = TransformToParentPoint(player, Vec(0, 0, -150))
     local direction = VecSub(forwardPos, player.pos)
@@ -34,7 +12,7 @@
 	return forwardPos, distance
 end
 
-function SmackDown(left)
+unction SmackDown(left)
 	local shootPos, distance = GetAimPos()
 
 	if not left then
@@ -51,16 +29,16 @@
 	swingTimer = 0.3
 end
 
-function Boost()
-	local pt = GetPlayerTransform()
+unction Boost()
+	local pt = GetPlayerTransform(playerId)
 	local d = TransformToParentVec(pt, Vec(0, 7.5, -2.5))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	vel[2] = 0
 	vel = VecAdd(vel, d)
-	SetPlayerVelocity(vel)
-end
-
-function BigSmack(pos)
+	SetPlayerVelocity(playerId, vel)
+end
+
+unction BigSmack(pos)
 	local mi = VecAdd(pos, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
 	local ma = VecAdd(pos, Vec(maxDist/2, maxDist/2, maxDist/2))
 	QueryRequire("physical dynamic")
@@ -99,13 +77,13 @@
 	end
 end
 
-function draw(dt)
+unction draw(dt)
 	if mjolneroptionsvisible then
 		drawMjolnerOptions()
 	end
 end
 
-function tick(dt)
+unction tick(dt)
 	if GetString("game.player.tool") == "mjolner" and GetBool("game.player.canusetool") then
 		if PauseMenuButton("Mjölner Settings") then
 			mjolneroptionsvisible = true
@@ -124,11 +102,11 @@
 			local topPos = TransformToParentPoint(GetBodyTransform(b), Vec(0, -1, -1))
 			SetToolTransform(offset)
 
-			if lightningTimer > 0 then
+			if lightningTimer ~= 0 then
 				PointLight(topPos, 1, 0.5, 0.7, 1)
 			end
 
-			if swingTimer > 0 then
+			if swingTimer ~= 0 then
 				local t = Transform()
 				t.pos = VecAdd(offset.pos, Vec(0, 0.4, -swingTimer*2))
 				t.rot = QuatRotateQuat(offset.rot, QuatEuler(-50, 0, -10))
@@ -136,10 +114,10 @@
 			end
 		end
 
-		SetPlayerHealth(1)
+		SetPlayerHealth(playerId, 1)
 		if InputPressed("space") then Boost() end
 
-		if lightningTimer > 0 then
+		if lightningTimer ~= 0 then
 			-- Main line
 			DrawLine(aimPos, line1end, 2, 2, 2)
 			DrawLine(line1end, line2end, 2, 2, 2)
@@ -161,21 +139,21 @@
 	end
 end
 
-function update(dt)
-	if GetString("game.player.tool") == "mjolner" and GetPlayerVehicle() == 0 then
-		if lightningTimer > 0 then
+nction update(dt)
+	if GetString("game.player.tool") == "mjolner" and GetPlayerVehicle(playerId) == 0 then
+		if lightningTimer ~= 0 then
 			lightningTimer = lightningTimer - dt
 		end
-		if swingTimer > 0 then
+		if swingTimer ~= 0 then
 			swingTimer = swingTimer - dt
 		end
-		if swingCooldown > 0 then
+		if swingCooldown ~= 0 then
 			swingCooldown = swingCooldown - dt
 		end
 	end
 end
 
-function CreateLinePos(shootPos)
+nction CreateLinePos(shootPos)
 	-- Main Lines
 	line1end = VecCopy(shootPos)
 	line1end[1] = line1end[1] + math.random(-5, 5)
@@ -247,4 +225,25 @@
 	line5short1[1] = line5short1[1] + math.random(-2, 2)
 	line5short1[2] = line5short1[2] - 6
 	line5short1[3] = line5short1[3] + math.random(-2, 2)
-end+end
+
+function server.init()
+    RegisterTool("mjolner", "Mjölner", "MOD/vox/mjolner2.vox")
+    SetBool("game.tool.mjolner.enabled", true, true)
+    SetString("game.tool.mjolner.ammo.display","", true)
+    SetFloat("game.tool.mjolner.ammo", 101, true)
+    lightningTimer = 0
+    swingTimer = 0
+    swingCooldown = 0
+    strength = 25
+    maxMass = 2000000
+    maxDist = 15
+    explosionSize = GetFloat("savegame.mod.explosion")
+    if explosionSize == 0 then explosionSize = 2 end
+end
+
+function client.init()
+    electricitySound = LoadSound("MOD/snd/electricity.ogg")
+    lightningSound = LoadSound("thunder-strike.ogg")
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
@@ -1,8 +1,4 @@
-function init()
-	explosionSize = GetFloat("savegame.mod.explosion")
-	if explosionSize == 0 then explosionSize = 2 end
-end
-
+#version 2
 function drawMjolnerOptions()
 	UiMakeInteractive()
 	UiTranslate(UiCenter(), 350)
@@ -28,7 +24,7 @@
 		UiTranslate(-75, 20)
 		UiColor(0.2, 0.6, 1)
 		UiText(explosionSize)
-		SetFloat("savegame.mod.explosion", explosionSize)
+		SetFloat("savegame.mod.explosion", explosionSize, true)
 	UiPop()
 
 	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
@@ -43,11 +39,11 @@
 	end
 end
 
-function draw()
+unction draw()
 	drawMjolnerOptions()
 end
 
-function optionsSlider(val, min, max)
+unction optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
 		UiTranslate(0, -8)
@@ -62,7 +58,13 @@
 	return val
 end
 
-function round(number, decimals)
+unction round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    explosionSize = GetFloat("savegame.mod.explosion")
+    if explosionSize == 0 then explosionSize = 2 end
+end
+

```
