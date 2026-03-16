# Migration Report: script\monsterfreya.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\monsterfreya.lua
+++ patched/script\monsterfreya.lua
@@ -1,54 +1,48 @@
-#include "script/common.lua"
-
-enabled = false
-fade = 0
-
-gTime = 0
-gMusicVol = 1
-
-function init()
-	vehicle = FindVehicle("epamonstertruck", true)
+#version 2
+function server.init()
+    vehicle = FindVehicle("epamonstertruck", true)
 end
 
-function tick(dt)
-	local inVehicle = GetPlayerVehicle() == vehicle
-	if inVehicle then
-		enabled = true
-	end
-	
-	if inVehicle then
-		SetBool("hud.disable", true)
-		gTime = gTime + dt
-		if fade == 0 then
-			SetValue("fade", 1.0, "easeout", 0.3)
-		end
-	else
-		local dist = VecLength(VecSub(GetPlayerTransform().pos, GetVehicleTransform(vehicle).pos))
-		dist = math.max(dist, 1.0)*0.1;
-		gMusicVol = clamp(1.05/(dist*dist)-0.05, 0.0, 1.0)
-		if fade == 1 then
-			SetValue("fade", 0.0, "easein", 0.3)
-		end
-	end
-
-	local vol = fade + gMusicVol*(1-fade)
-	if vol > 0.01 then
-		PlayMusic("MOD/music/ending.ogg")
-	end
-	SetFloat("game.music.volume", vol)
-	SetFloat("game.music.lowpass", 1.0-fade)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local inVehicle = GetPlayerVehicle(playerId) == vehicle
+        if inVehicle then
+        	enabled = true
+        end
+        if inVehicle then
+        	SetBool("hud.disable", true, true)
+        	gTime = gTime + dt
+        	if fade == 0 then
+        		SetValue("fade", 1.0, "easeout", 0.3)
+        	end
+        else
+        	local dist = VecLength(VecSub(GetPlayerTransform(playerId).pos, GetVehicleTransform(vehicle).pos))
+        	dist = math.max(dist, 1.0)*0.1;
+        	gMusicVol = clamp(1.05/(dist*dist)-0.05, 0.0, 1.0)
+        	if fade == 1 then
+        		SetValue("fade", 0.0, "easein", 0.3)
+        	end
+        end
+        local vol = fade + gMusicVol*(1-fade)
+        if vol > 0.01 then
+        	PlayMusic("MOD/music/ending.ogg")
+        end
+        SetFloat("game.music.volume", vol, true)
+        SetFloat("game.music.lowpass", 1.0-fade, true)
+    end
 end
 
-function draw()
-	if enabled then
-		UiPush()
-			UiColorFilter(1,1,1,fade)
-		UiPop()
-		UiPush()
-			UiColor(0,0,0)
-			UiRect(UiWidth(), 80*fade)
-			UiTranslate(0, UiHeight()-80*fade)
-			UiRect(UiWidth(), 80)
-		UiPop()
-	end
+function client.draw()
+    if enabled then
+    	UiPush()
+    		UiColorFilter(1,1,1,fade)
+    	UiPop()
+    	UiPush()
+    		UiColor(0,0,0)
+    		UiRect(UiWidth(), 80*fade)
+    		UiTranslate(0, UiHeight()-80*fade)
+    		UiRect(UiWidth(), 80)
+    	UiPop()
+    end
 end
+

```
