# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,94 +1,93 @@
+#version 2
 local bleeding = false
 local bandageTimer = 0
 local isBandaging = false
-local BANDAGE_TIME = 4.0 -- seconds
+local BANDAGE_TIME = 4.0
 local medkitTimer = 0
 local isAiding = false
-local MEDKIT_TIME = 5.0 -- seconds
-local hasBledAlready = false -- to avoid re-triggering
+local MEDKIT_TIME = 5.0
+local hasBledAlready = false
 
-function draw(dt)
-	if GetPlayerHealth() == 1 then
-		SetPlayerRegenerationState(false)
-	end
-	if isBandaging then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-90)
-			UiAlign("center middle")
-			UiColor(0.8, 0.8, 0.8)
-			UiFont("bold.ttf", 31)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText("Applying Bandage...")
-				
-			end
-	if isAiding then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-90)
-			UiAlign("center middle")
-			UiColor(0.8, 0.8, 0.8)
-			UiFont("bold.ttf", 31)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText("Administering Aid...")
-				
-			end
-	if bleeding then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-120)
-			UiAlign("center middle")
-			UiColor(1, 0.8, 0.8)
-			UiFont("bold.ttf", 31)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText("Bleeding!")
-				
-			end
+function server.tick(dt)
+    local health = GetPlayerHealth(playerId)
+    -- Start bandaging when B is pressed
+    -- Bandaging countdown
+    if isBandaging then
+    	bandageTimer = bandageTimer - dt
+    	if bandageTimer <= 0 then
+    		SetPlayerHealth(playerId, 0.66)
+    		bleeding = false
+    		isBandaging = false
+
+    	end
+    end
+    if isAiding then
+    	medkitTimer = medkitTimer - dt
+    	if medkitTimer <= 0 then
+    		SetPlayerHealth(playerId, 1)
+    		isAiding = false
+
+    	end
+    end
+    -- Bleed effect
+    if bleeding then
+    	SetPlayerHealth(playerId, health - 0.0002)
+
+    end
+    -- Emergency test heal
+    if health < 0.65 then
+    	bleeding = true
+    else
+    	bleeding = false
+    end
 end
 
-function tick(dt)
-	local health = GetPlayerHealth()
+function client.tick(dt)
+    if InputPressed("b") and not isBandaging and bleeding then
+    	bandageTimer = BANDAGE_TIME
+    	isBandaging = true
 
-	-- Start bandaging when B is pressed
-	if InputPressed("b") and not isBandaging and bleeding then
-		bandageTimer = BANDAGE_TIME
-		isBandaging = true
-		
-	end
-	
-	if InputPressed("n") and not isAiding and not bleeding and health < 1 and 0.65 < health then
-		medkitTimer = MEDKIT_TIME
-		isAiding = true
-		
-	end
+    end
+    if InputPressed("n") and not isAiding and not bleeding and health < 1 and 0.65 < health then
+    	medkitTimer = MEDKIT_TIME
+    	isAiding = true
 
-	-- Bandaging countdown
-	if isBandaging then
-		bandageTimer = bandageTimer - dt
-		if bandageTimer <= 0 then
-			SetPlayerHealth(0.66)
-			bleeding = false
-			isBandaging = false
-			
-		end
-	end
-	
-	if isAiding then
-		medkitTimer = medkitTimer - dt
-		if medkitTimer <= 0 then
-			SetPlayerHealth(1)
-			isAiding = false
-			
-		end
-	end
+    end
+end
 
-	-- Bleed effect
-	if bleeding then
-		SetPlayerHealth(health - 0.0002)
-		
-	end
+function client.draw()
+    if GetPlayerHealth(playerId) == 1 then
+    	SetPlayerRegenerationState(false)
+    end
+    if isBandaging then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-90)
+    		UiAlign("center middle")
+    		UiColor(0.8, 0.8, 0.8)
+    		UiFont("bold.ttf", 31)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText("Applying Bandage...")
 
-	-- Emergency test heal
-	if health < 0.65 then
-		bleeding = true
-	else
-		bleeding = false
-	end
-end+    		end
+    if isAiding then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-90)
+    		UiAlign("center middle")
+    		UiColor(0.8, 0.8, 0.8)
+    		UiFont("bold.ttf", 31)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText("Administering Aid...")
+
+    		end
+    if bleeding then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-120)
+    		UiAlign("center middle")
+    		UiColor(1, 0.8, 0.8)
+    		UiFont("bold.ttf", 31)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText("Bleeding!")
+
+    		end
+end
+

```
