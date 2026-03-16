# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,36 +1,4 @@
-shurikenprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false, spriteTimer = 0},
-}
-
-function init()
-	RegisterTool("explodingstar", "Exploding Star", "MOD/vox/explodingstar.vox")
-	SetBool("game.tool.explodingstar.enabled", true)
-	SetFloat("game.tool.explodingstar.ammo", 101)
-
-	fuseTime = GetFloat("savegame.mod.fusetime")
-	if fuseTime == 0 then fuseTime = 1 end
-	explosionpower = GetFloat("savegame.mod.boomsize")
-	if explosionpower == 0 then explosionpower = 0.5 end
-	
-	gravity = Vec(0, -10, 0)
-	velocity = 0.3
-	damage = 0.1
-	shotDelay = 0.125
-
-	for i=1, 100 do
-		shurikenprojectileHandler.shells[i] = deepcopy(shurikenprojectileHandler.defaultShell)
-	end
-
-	throwsound = LoadSound("MOD/snd/throw2.ogg")
-	beepsound = LoadSound("MOD/snd/beep.ogg")
-	shurikensprite = LoadSprite("MOD/img/shuriken.png")
-
-	shootTimer = 0
-	swingTimer = 0
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -61,7 +29,7 @@
 end
 
 function Shoot()
-	if shootTimer > 0 then
+	if shootTimer ~= 0 then
 		return
 	end
 
@@ -113,49 +81,84 @@
 	projectile.pos = point2
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "explodingstar" and GetPlayerVehicle() == 0 then
-		if InputDown("lmb") then
-			Shoot()
-		end
+function server.init()
+    RegisterTool("explodingstar", "Exploding Star", "MOD/vox/explodingstar.vox")
+    SetBool("game.tool.explodingstar.enabled", true, true)
+    SetFloat("game.tool.explodingstar.ammo", 101, true)
+    fuseTime = GetFloat("savegame.mod.fusetime")
+end
 
-		if shootTimer > 0 then
-			shootTimer = shootTimer - GetTimeStep()
-		end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(shurikenprojectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
 
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
-			SetToolTransform(offset)
+        	if shell.spriteTimer ~= 0 then
+        		shell.spriteTimer = shell.spriteTimer - GetTimeStep()
+        		if shell.spriteTimer < 0.001 then
+        			Explosion(shell.pos, explosionpower)
+        			shell.spriteTimer = 0
+        		end
+        		DrawSprite(shurikensprite, shell, 0.4, 0.4, 0, 0, 0, 1, 0, false)
+        	end
 
-			if swingTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, swingTimer*2)
-				t.rot = QuatEuler(swingTimer*50, 0, 0)
-				SetToolTransform(t)
+        	if shell.explode then
+        		Explosion(shell.pos, explosionpower)
+        		shell.explode = false
+        	end
+        end
+    end
+end
 
-				swingTimer = swingTimer - dt
-			end
-		end
-	end
+function client.init()
+    if fuseTime == 0 then fuseTime = 1 end
+    explosionpower = GetFloat("savegame.mod.boomsize")
+    if explosionpower == 0 then explosionpower = 0.5 end
 
-	for key, shell in ipairs(shurikenprojectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
+    gravity = Vec(0, -10, 0)
+    velocity = 0.3
+    damage = 0.1
+    shotDelay = 0.125
 
-		if shell.spriteTimer > 0 then
-			shell.spriteTimer = shell.spriteTimer - GetTimeStep()
-			if shell.spriteTimer < 0.001 then
-				Explosion(shell.pos, explosionpower)
-				shell.spriteTimer = 0
-			end
-			DrawSprite(shurikensprite, shell, 0.4, 0.4, 0, 0, 0, 1, 0, false)
-		end
-		
-		if shell.explode then
-			Explosion(shell.pos, explosionpower)
-			shell.explode = false
-		end
-	end
-end+    for i=1, 100 do
+    	shurikenprojectileHandler.shells[i] = deepcopy(shurikenprojectileHandler.defaultShell)
+    end
+
+    throwsound = LoadSound("MOD/snd/throw2.ogg")
+    beepsound = LoadSound("MOD/snd/beep.ogg")
+    shurikensprite = LoadSprite("MOD/img/shuriken.png")
+
+    shootTimer = 0
+    swingTimer = 0
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "explodingstar" and GetPlayerVehicle(playerId) == 0 then
+    	if InputDown("lmb") then
+    		Shoot()
+    	end
+
+    	if shootTimer ~= 0 then
+    		shootTimer = shootTimer - GetTimeStep()
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
+    		SetToolTransform(offset)
+
+    		if swingTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, swingTimer*2)
+    			t.rot = QuatEuler(swingTimer*50, 0, 0)
+    			SetToolTransform(t)
+
+    			swingTimer = swingTimer - dt
+    		end
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
@@ -1,50 +1,4 @@
-function init()
-	boomSize = GetFloat("savegame.mod.boomsize")
-	if boomSize == 0 then boomSize = 0.5 end
-	fuseTime = GetFloat("savegame.mod.fusetime")
-	if fuseTime == 0 then fuseTime = 1 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Exploding Star")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 40)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Explosion Size")
-		UiAlign("right")
-		UiTranslate(95, 40)
-		boomSize = optionsSlider(boomSize, 0.5, 4)
-		UiTranslate(-75, 20)
-		UiColor(0.2, 0.6, 1)
-		UiText(boomSize)
-		SetFloat("savegame.mod.boomsize", boomSize)
-	UiPop()
-
-	UiTranslate(0, 110)
-	UiPush()
-		UiText("Fuse Time")
-		UiAlign("right")
-		UiTranslate(95, 40)
-		fuseTime = optionsSlider(fuseTime, 0, 10)
-		UiTranslate(-75, 20)
-		UiColor(0.2, 0.6, 1)
-		UiText(fuseTime)
-		SetFloat("savegame.mod.fusetime", fuseTime)
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
@@ -63,4 +17,52 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    boomSize = GetFloat("savegame.mod.boomsize")
+    if boomSize == 0 then boomSize = 0.5 end
+    fuseTime = GetFloat("savegame.mod.fusetime")
+    if fuseTime == 0 then fuseTime = 1 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Exploding Star")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 40)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Explosion Size")
+    	UiAlign("right")
+    	UiTranslate(95, 40)
+    	boomSize = optionsSlider(boomSize, 0.5, 4)
+    	UiTranslate(-75, 20)
+    	UiColor(0.2, 0.6, 1)
+    	UiText(boomSize)
+    	SetFloat("savegame.mod.boomsize", boomSize, true)
+    UiPop()
+
+    UiTranslate(0, 110)
+    UiPush()
+    	UiText("Fuse Time")
+    	UiAlign("right")
+    	UiTranslate(95, 40)
+    	fuseTime = optionsSlider(fuseTime, 0, 10)
+    	UiTranslate(-75, 20)
+    	UiColor(0.2, 0.6, 1)
+    	UiText(fuseTime)
+    	SetFloat("savegame.mod.fusetime", fuseTime, true)
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
