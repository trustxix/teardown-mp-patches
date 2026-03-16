# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,26 +1,4 @@
-#include "options.lua"
-
-laserCutterMenuOpen = false
-
-function init()
-	RegisterTool("lasercutter", "Laser Cutter", "MOD/vox/lasercutter.vox", 2)
-	SetBool("game.tool.lasercutter.enabled", true)
-	SetString("game.tool.lasercutter.ammo.display","")
-	SetFloat("game.tool.lasercutter.ammo", 101)
-
-	laserHitLoop = LoadLoop("MOD/snd/laser-hit-loop.ogg")
-	laserSound = LoadLoop("MOD/snd/laser-loop.ogg")
-	zoomMultiplier = 0.75
-	FOV = GetInt("options.gfx.fov")
-	zoomLevel = 0
-
-	startFire = GetBool("savegame.mod.startfire")
-	holeSize = GetFloat("savegame.mod.holesize")
-	if holeSize == 0 then holeSize = 0.15 end
-	laserRange = GetFloat("savegame.mod.range")
-	if laserRange == 0 then laserRange = 5 end
-end
-
+#version 2
 function rnd(mi, ma)
 	return math.random()*(ma-mi) + mi
 end
@@ -40,11 +18,11 @@
 end
 
 function zoomAim()
-	if InputDown("rmb") and not IsHandleValid(GetPlayerGrabBody()) then
+	if InputDown("rmb") and not IsHandleValid(GetPlayerGrabBody(playerId)) then
 		if(zoomLevel==0) then  
 			SetValue("zoomLevel", 1, "linear", 0.5)
 		end	
-	elseif((InputReleased("rmb") and not IsHandleValid(GetPlayerGrabBody())) ) then
+	elseif((InputReleased("rmb") and not IsHandleValid(GetPlayerGrabBody(playerId))) ) then
 		SetValue("zoomLevel", 0, "linear", 0.25)
 	end
 	if zoomLevel ~=0 then
@@ -90,36 +68,53 @@
 	end
 end
 
-function draw()
-	if GetString("game.player.tool") == "lasercutter" and laserCutterMenuOpen then
-		drawLaserCutterOptions()
-	end
+function server.init()
+    RegisterTool("lasercutter", "Laser Cutter", "MOD/vox/lasercutter.vox", 2)
+    SetBool("game.tool.lasercutter.enabled", true, true)
+    SetString("game.tool.lasercutter.ammo.display","", true)
+    SetFloat("game.tool.lasercutter.ammo", 101, true)
+    laserHitLoop = LoadLoop("MOD/snd/laser-hit-loop.ogg")
+    laserSound = LoadLoop("MOD/snd/laser-loop.ogg")
+    zoomMultiplier = 0.75
+    FOV = GetInt("options.gfx.fov")
+    zoomLevel = 0
+    startFire = GetBool("savegame.mod.startfire")
+    holeSize = GetFloat("savegame.mod.holesize")
+    if holeSize == 0 then holeSize = 0.15 end
+    laserRange = GetFloat("savegame.mod.range")
+    if laserRange == 0 then laserRange = 5 end
 end
 
-function update()
-	if GetString("game.player.tool") == "lasercutter" and GetBool("game.player.canusetool") then
-		if InputDown("usetool") then
-			DrawLine(toolPos, aimpos, 1, 0.3, 0.3)
-		end
-	end
+function client.tick(dt)
+    if GetString("game.player.tool") == "lasercutter" then
+    	setToolPosition()
+    	if InputPressed("R") then laserCutterMenuOpen = not laserCutterMenuOpen end
+    	if PauseMenuButton("Laser Cutter Settings") then
+    		laserCutterMenuOpen = true
+    	end
+
+    	if GetBool("game.player.canusetool") then
+    		zoomAim()
+
+    		if InputDown("usetool") then
+    			ShootLaser()
+    			PlayLoop(laserSound)
+    		end
+    	end
+    end
 end
 
-function tick()
-	if GetString("game.player.tool") == "lasercutter" then
-		setToolPosition()
-		if InputPressed("R") then laserCutterMenuOpen = not laserCutterMenuOpen end
-		if PauseMenuButton("Laser Cutter Settings") then
-			laserCutterMenuOpen = true
-		end
-		
-		if GetBool("game.player.canusetool") then
-			zoomAim()
-			
-			if InputDown("usetool") then
-				ShootLaser()
-				PlayLoop(laserSound)
-			end
-		end
-	end
+function client.update(dt)
+    if GetString("game.player.tool") == "lasercutter" and GetBool("game.player.canusetool") then
+    	if InputDown("usetool") then
+    		DrawLine(toolPos, aimpos, 1, 0.3, 0.3)
+    	end
+    end
 end
 
+function client.draw()
+    if GetString("game.player.tool") == "lasercutter" and laserCutterMenuOpen then
+    	drawLaserCutterOptions()
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
@@ -1,15 +1,4 @@
-function init()
-	startFire = GetBool("savegame.mod.startfire")
-	holeSize = GetFloat("savegame.mod.holesize")
-	if holeSize == 0 then holeSize = 0.15 end
-	laserRange = GetFloat("savegame.mod.range")
-	if laserRange == 0 then laserRange = 5 end
-end
-
-function draw()
-	drawLaserCutterOptions()
-end
-
+#version 2
 function drawLaserCutterOptions()
 	UiMakeInteractive()
 	UiTranslate(UiCenter(), 350)
@@ -32,12 +21,12 @@
 		if startFire then
 			if UiTextButton("Yes", 20, 20) then
 				startFire = false
-				SetBool("savegame.mod.startfire", startFire)
+				SetBool("savegame.mod.startfire", startFire, true)
 			end
 		else
 			if UiTextButton("No", 20, 20) then
 				startFire = true
-				SetBool("savegame.mod.startfire", startFire)
+				SetBool("savegame.mod.startfire", startFire, true)
 			end
 		end
 	UiPop()
@@ -51,7 +40,7 @@
 		UiTranslate(-75, 20)
 		UiColor(0.2, 0.6, 1)
 		UiText(laserRange)
-		SetFloat("savegame.mod.range", laserRange)
+		SetFloat("savegame.mod.range", laserRange, true)
 	UiPop()
 
 	UiTranslate(0, 100)
@@ -63,7 +52,7 @@
 		UiTranslate(-75, 20)
 		UiColor(0.2, 0.6, 1)
 		UiText(holeSize)
-		SetFloat("savegame.mod.holesize", holeSize)
+		SetFloat("savegame.mod.holesize", holeSize, true)
 	UiPop()
 
 	UiTranslate(0, 120)
@@ -95,4 +84,17 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    startFire = GetBool("savegame.mod.startfire")
+    holeSize = GetFloat("savegame.mod.holesize")
+    if holeSize == 0 then holeSize = 0.15 end
+    laserRange = GetFloat("savegame.mod.range")
+    if laserRange == 0 then laserRange = 5 end
+end
+
+function client.draw()
+    drawLaserCutterOptions()
+end
+

```
