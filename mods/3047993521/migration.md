# Migration Report: ALS.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/ALS.lua
+++ patched/ALS.lua
@@ -1,27 +1,21 @@
-#include "ALSlibrary.lua"
-
-function init()
-    --DebugPrint("text")
-    --normal lights
+#version 2
+function server.init()
     findvehicle = FindShape("ALShorn")
     lightShapes = FindShapes("ALSlight")
     ALSVehicle = FindVehicle("ALS")
-
     --turn all the lights off when spawned
-
-
     currentKmh = 0
     correntKmh = 0
     counter=0
     frame2 = 0
-
     reset = {}
     reset[#reset+1] = {false}
     reset[#reset+1] = {false}
-
     em = {0,0,0,0,0,0,0,0,0}
-
     --emergency lights
+end
+
+function client.init()
     if HasTag(ALSVehicle, "emergency") then
         lightShapesEM = FindShapes("ALSem")
         GiroflexLight = FindShapes("ALSGF")
@@ -90,17 +84,12 @@
             ter = {5,5,4,5,4,5,2,5,5}
             SetTag(ALSVehicle, "ter", string.format("%02d", ter[1])..string.format("%02d", ter[2])..string.format("%02d", ter[3])..string.format("%02d", ter[4])..string.format("%02d", ter[5])..string.format("%02d", ter[6])..string.format("%02d", ter[7])..string.format("%02d", ter[8])..string.format("%02d", ter[9]))
         end
-        
+
     end
 end
 
-
---fix the lights so call the function only one time when changing mode
---every time it calls clean the normal lights not the emergency lights
---only clean the emergency lights when turned off
---call every update if it has an animation (blinkers and emergency lights)
-function update(dt)
-
+function client.update(dt)
+    local playerId = GetLocalPlayer()
     if not destroyed and GetBool("level.ALS.enabled") then
             blinker = HasTag(ALSVehicle, "p")
             di = GetTagValue(ALSVehicle, "p") == "1"
@@ -112,8 +101,7 @@
             fadm = HasTag(ALSVehicle, "fa")
             ad = HasTag(ALSVehicle, "ad")
 
-
-            if GetPlayerVehicle() == ALSVehicle then
+            if GetPlayerVehicle(playerId) == ALSVehicle then
                 brake = InputDown("down")
                 brake2 = InputDown("up")
                 brake3= InputDown("handbrake")
@@ -143,8 +131,6 @@
                 brake2=false
                 brake3=false
             end
-
-            
 
             --emergency lights
             if HasTag(ALSVehicle, "emergency") then
@@ -199,10 +185,9 @@
                         }
                         RemoveTag(ALSVehicle, "update")
                     end
-                        
 
                     lightsOptions()
-                    
+
                     frame = frame + dt*60
                     local period = 120
                     local t = math.ceil(frame) % period
@@ -211,7 +196,7 @@
                         frame = 0
                     end
                 end
-        
+
                 if  HasTag(ALSVehicle, "GF") then
                     if reset[1]~=lightsOn then giroflexemergencia() end
                 end
@@ -231,7 +216,6 @@
                     SetShapeEmissiveScale(lightShapes[i], 0)
                 end
         end
-
 
             --normal lights
             --fix this call only one time when changing mode
@@ -248,14 +232,12 @@
                     NormalLights() 
                 end
             end
-            
+
             --pop up headlights
             --call one time when turning lights on and off
             if HasTag(ALSVehicle, "UP") then
                     popupheadlights()
             end
-
-
 
         --if the life reach 0
         if GetVehicleHealth(ALSVehicle) == 0 then
@@ -269,22 +251,5 @@
         end
 
     end
-    
-
-    
-    --deletes vehicle when live reachs 0
-    --[[
-    if HasTag(findvehicle, "delete") then
-        if GetVehicleHealth(ALSVehicle) == 0 then
-            for i = 1, #lightShapes do Delete(lightShapes[i]) end
-            if HasTag(ALSVehicle, "emergency") then
-            for i = 1, #lightShapesEM do Delete(lightShapesEM[i]) end
-            end
-            Delete(ALSVehicle)
-            Delete(crane)
-            Delete(findvehicle)
-            DeleteVehicle()
-        end
-    end
-    ]]--
 end
+

```

---

# Migration Report: building\ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/building\ground.lua
+++ patched/building\ground.lua
@@ -1,35 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
+    matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
+    matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
+    matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h do
+    	local y1 = y0 + maxSize
+    	if y1 > h then y1 = h end
 
-function init()
-	matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
-	matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
-	matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
-	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
-	
-	LoadImage(file)
-	
-	w,h = GetImageSize()
+    	local x0 = 0
+    	while x0 < w do
+    		local x1 = x0 + maxSize
+    		if x1 > w then x1 = w end
+    		Vox(x0, 0, y0)
+    		Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
+    		x0 = x1
+    	end
+    	y0 = y1
+    end
+end
 
-	local maxSize = tileSize
-	
-	local y0 = 0
-	while y0 < h do
-		local y1 = y0 + maxSize
-		if y1 > h then y1 = h end
-
-		local x0 = 0
-		while x0 < w do
-			local x1 = x0 + maxSize
-			if x1 > w then x1 = w end
-			Vox(x0, 0, y0)
-			Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
-			x0 = x1
-		end
-		y0 = y1
-	end
-end

```

---

# Migration Report: copcar.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/copcar.lua
+++ patched/copcar.lua
@@ -1,218 +1,5 @@
-#include "math.lua"
-#include "als.lua"
-
-local hackedCars = {}
-
-local enabledAll = false
-
-function init()
-    car1 = FindBody("car1")
-	copcar = FindVehicle("car1")
-
-	disp = LoadSound("MOD/snd/dis0.ogg", 9.0)
-	PlaySound(disp, GetPlayerTransform().pos, 0.5)
-	
-	box1 = FindShape("box1")
-	box2 = FindShape("box2")
-	box3 = FindShape("box3")
-	box4 = FindShape("box4")
-	box5 = FindShape("box5")
-	
-	test = FindBody("test")
-	
-	siren = LoadLoop("MOD/snd/siren.ogg", 15.0)
-	broken = LoadSound("MOD/snd/broken.ogg", 15.0)
-	
-    local list = QueryAabbBodies(Vec(-10, -10, -10), Vec(10, 10, 10))
-    for i=1, #list do
-        local body = car1
-        local vehicle = GetBodyVehicle(body)
-        if vehicle ~= 0 then
-            table.insert(hackedCars, {v = vehicle, stucktime = 0.0, isBack = false, rnd = math.random(-1.0, 1.0), isStopped = false, distance = 0.0})
-        end
-    end
-	
-end
-
-function tick(dt)
-
-    checkALS()
-
-        if hit then
-            local hitPoint = VecAdd(camTransform.pos, VecScale(dir, d))
-            local body = GetShapeBody(s)
-            local vehicle = GetBodyVehicle(body)
-            if vehicle ~= 0 then
-                DrawBodyOutline(body,1,1,1,0.5)
-            end
-            if InputPressed("usetool") then
-                if vehicle ~= 0 then
-                    local isRemoving = false
-                    for i=1,#hackedCars do
-                        if hackedCars[i] ~= nil and hackedCars[i].v == vehicle then
-                            removeVehicle(i)
-                            isRemoving = true
-                            return
-                        end
-                    end
-                    if isRemoving == false then
-                        changeLight(vehicle, true)
-                        table.insert(hackedCars, {v = vehicle, stucktime = 0.0, isBack = false, rnd = math.random(-1.0, 1.0), isStopped = false, distance = 0.0})
-                    end
-                end
-            end
-        end
-
-    for i=1,#hackedCars do
-        updateAI(i, dt)
-    end	
-end
-
-function draw()
-    if GetString("game.player.tool") == "vhack" then
-        UiAlign("center")
-        UiTranslate(UiCenter(),UiHeight()-60)
-        UiFont("bold.ttf", 24)
-        UiText("LMB to hack car / R to hack all cars")
-    end
-end
-
-function changeLight(vehicle, t)
-    local shapes = GetBodyShapes(GetVehicleBody(vehicle))
-    for i=1, #shapes do
-        local lights = GetShapeLights(shapes[i])
-        for j=1, #lights do
-            if t then
-             SetLightColor(lights[j], 1, 0, 0)
-             SetLightIntensity(lights[j],1)
-            else
-             SetLightColor(lights[j], 1, 1, 1)
-             SetLightIntensity(lights[j],1)
-            end
-        end
-    end
-end
-
-function updateAI(i, dt)
-    if hackedCars == nil or hackedCars[i] == nil or hackedCars[i].v == nil or i > #hackedCars then
-        return
-    end
-    local vehicle = hackedCars[i].v
-    local t = GetVehicleTransform(vehicle)
-    local vehicleToWaypoint = VecSub(t.pos,GetPlayerPos())
-	--PlayLoop(siren, t.pos, 0.3)
-
-    local forward = TransformToParentVec(t, Vec(0,0,1))
-    local steerCross = VecCross(VecNormalize(vehicleToWaypoint), forward);
-    local steerDirection = VecDot(VecNormalize(steerCross), Vec(0,1,0));
-    local steer = VecLength(steerCross) * steerDirection;
-    local lights = GetShapeLights(shape)
-
-    local distToTarget = dist(t.pos, GetPlayerPos())
-
-    local diffDistance = distToTarget - hackedCars[i].distance
-    
-    local speed = 1
-
-    local vel = VecLength(GetBodyVelocity(GetVehicleBody(vehicle)))
-
-    updateALS(vehicle) -- ALS Support
-
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local tr = Transform(VecAdd(t.pos,Vec(0,1,0)),t.rot)
-    
-    local leftTest = TransformToParentVec(tr, Vec(0.5,0,-1))
-    local hit, d = QueryRaycast(tr.pos, leftTest, 12)
-    --DrawLine(tr.pos, VecAdd(tr.pos, leftTest))
-
-    if hit then
-        steer = -1
-        speed = 0.1
-    end
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local rightTest = TransformToParentVec(tr, Vec(-0.5,0,-1))
-    local hit, d = QueryRaycast(tr.pos, rightTest, 12)
-    --DrawLine(tr.pos, VecAdd(tr.pos, rightTest))
-
-    if hit then
-        steer = 1
-        speed = 0.1
-    end
-    --[[
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local stopTest = TransformToParentVec(tr, Vec(0,0,-1))
-    local hit, d = QueryRaycast(tr.pos, stopTest, 3)
-
-    local velstop = GetBodyVelocity(GetVehicleBody(vehicle))
-
-    if hit then
-        speed = 0.0
-        if hackedCars[i].isBack == false then
-           -- SetBodyVelocity(GetVehicleBody(vehicle), VecScale(velstop,0.98))
-        end
-    end
-    --]]
-    
-    if hackedCars[i].isBack == false then
-        if vel < 0.5 then
-            hackedCars[i].stucktime = hackedCars[i].stucktime + dt
-        else
-            hackedCars[i].stucktime = 0.0
-        end
-        if hackedCars[i].stucktime > 0.6 then
-            hackedCars[i].stucktime = 1.0
-            hackedCars[i].isBack = true
-            hackedCars[i].isStopped = false
-        end
-    else
-        hackedCars[i].stucktime = hackedCars[i].stucktime - dt
-        if hackedCars[i].stucktime <= 0.0 then
-            hackedCars[i].isBack = false
-            hackedCars[i].stucktime = 0.0
-        end
-    end
-
-    hackedCars[i].rnd = hackedCars[i].rnd + dt*1.0
-
-    if hackedCars[i].isStopped == false then
-        if hackedCars[i].isBack == false then
-            DriveVehicle(vehicle, speed, -steer, false)
-        else
-            DriveVehicle(vehicle, -1, steer, false)
-        end
-    else
-        DriveVehicle(vehicle, 0, 0, true)
-    end
-            
-    if diffDistance > 0.32 and vel > 10.0 then
-        --hackedCars[i].isStopped = true
-        DriveVehicle(vehicle, 1, -1, true)
-    end
-
-    hackedCars[i].distance = distToTarget
-
-    local health = GetVehicleHealth(vehicle)
-    if health <= 0.6 then
-	    --PlaySound(broken, t.pos, 0.1)
-        removeVehicle(i)		
-    end
-	
-    if health > 0 then
-        PlayLoop(siren, t.pos, 0.3)
-    end
-	
-	if GetPlayerVehicle() == copcar then
-	    removeVehicle(i)	
-	end	
-	
-	--if GetPlayerHealth() <= 0 then
-		--removeVehicle(i)
-	--end		
-	
-end
+#version 2
+local health = GetVehicleHealth(vehicle)
 
 function removeVehicle(i)
     changeLight(hackedCars[i].v, false)
@@ -220,5 +7,3 @@
     table.remove(hackedCars, i)
 end
 
-
-

```

---

# Migration Report: elevator\elevator-screen.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/elevator\elevator-screen.lua
+++ patched/elevator\elevator-screen.lua
@@ -1,140 +1,4 @@
-
--- Constants
-BUTTON_SIZE = 45
-BUTTON_PADDING = 10
-NUMBER_Y = 140
-BUTTON_Y = 480
-NUMBER_FONT_SIZE = 100
-BUTTON_FONT_SIZE = 25
-ARROW_X = 145
-ARROW_WIDTH = 105
-MAX_DIGITS = 1
-
-numberBuffer = ""   -- Keep track of what digits the player is pressing
-keyPressTimeout = 0 -- For if a single digit is pressed
-
-function tick()	
-	screen = UiGetScreen()
-    elevatorId = GetTagValue(screen, "id")
-end
-
-function draw()
-	if screen == 0 then
-		return
-	end
-	
-	if GetPlayerScreen() ~= screen then
-		resetBuffer()
-	end
-
-	UiButtonHoverColor(0.8, 0.8, 0.8)
-	UiButtonPressColor(1.0, 0.78, 0.3)
-	
-	UiTranslate(0, 0)
-	UiImage("MOD/elevator/panel-background.png")
-	
-	UiAlign("center middle")
-	
-	-- Buttons
-	UiPush()
-	UiTranslate(UiCenter() - BUTTON_SIZE - BUTTON_PADDING, BUTTON_Y)
-	UiFont("MOD/elevator/bahnschrift.ttf", BUTTON_FONT_SIZE)
-	UiColor(0, 0, 0)
-	UiButtonImageBox("MOD/elevator/button.png", 25, 25)
-	local sizeAndPadding = BUTTON_SIZE + BUTTON_PADDING
-	--[[for y=0,2 do
-		for x=0,2 do
-			local i = (y * 3) + x + 1
-			UiPush()
-			UiTranslate(x * sizeAndPadding, y * sizeAndPadding)
-			if button(i) then
-				keyPressTimeout = GetTime() + 2
-				addToBuffer(i)
-			end
-			UiPop()
-		end
-	end]]--
-	UiTranslate(-30, -260)
-	if button("") then
-		numberBuffer = "14"
-	end
-	UiTranslate(sizeAndPadding+110, sizeAndPadding)
-	if button("") then
-		numberBuffer = "13"
-	end
-	UiTranslate(-sizeAndPadding-110, 0)
-	if button("") then
-		numberBuffer = "12"
-	end
-	UiTranslate(sizeAndPadding+110, sizeAndPadding)
-	if button("") then
-		numberBuffer = "11"
-	end
-	UiTranslate(-sizeAndPadding-110, 0)
-	if button("") then
-		numberBuffer = "10"
-	end
-	UiTranslate(sizeAndPadding+110, sizeAndPadding)
-	if button("") then
-		numberBuffer = "9"
-	end
-	UiTranslate(-sizeAndPadding-110, 0)
-	if button("") then
-		numberBuffer = "8"
-	end
-	UiTranslate(sizeAndPadding+110, sizeAndPadding)
-	if button("") then
-		numberBuffer = "7"
-	end
-	UiTranslate(-sizeAndPadding-110, 0)
-	if button("") then
-		numberBuffer = "6"
-	end
-	UiTranslate(sizeAndPadding+110, sizeAndPadding)
-	if button("3") then
-		numberBuffer = "5"
-	end
-	UiTranslate(-sizeAndPadding-110, 0)
-	if button("2") then
-		numberBuffer = "4"
-	end
-	UiTranslate(sizeAndPadding+110, sizeAndPadding)
-	if button("1") then
-		numberBuffer = "3"
-	end
-	UiTranslate(-sizeAndPadding-110, 0)
-	if button("SC") then
-		numberBuffer = "2"
-	end
-	UiTranslate(sizeAndPadding+110, sizeAndPadding)
-	if button("M") then
-		numberBuffer = "1"
-	end
-	UiTranslate(-sizeAndPadding-110, 0)
-	if button("DR") then
-		numberBuffer = "G"
-	end
-	UiTranslate(83, 180)
-	if button(" ") then
-
-	end
-	UiPop()
-	
-	-- Floor number
-	
-	-- Check if ok to set destination
-	if GetPlayerScreen() == screen and (numberBuffer == "G" or #numberBuffer >= MAX_DIGITS or (keyPressTimeout > 0 and GetTime() > keyPressTimeout)) then
-		keyPressTimeout = 0
-		if numberBuffer == "G" then
-			setDestinationFloor(0)
-		else
-			setDestinationFloor(tonumber(numberBuffer))
-		end
-		SetPlayerScreen(0)
-	end
-end
-
-
+#version 2
 function getCurrentFloor()
 	return GetInt("level.elevator" .. elevatorId .. ".currentFloor")
 end
@@ -148,7 +12,7 @@
 end
 
 function setDestinationFloor(num)
-	SetInt("level.elevator" .. elevatorId .. ".destinationFloor", num)
+	SetInt("level.elevator" .. elevatorId .. ".destinationFloor", num, true)
 end
 
 function button(label)
@@ -161,4 +25,128 @@
 
 function resetBuffer()
 	numberBuffer = ""
-end+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        screen = UiGetScreen()
+           elevatorId = GetTagValue(screen, "id")
+    end
+end
+
+function client.draw()
+    if screen == 0 then
+    	return
+    end
+
+    if GetPlayerScreen() ~= screen then
+    	resetBuffer()
+    end
+
+    UiButtonHoverColor(0.8, 0.8, 0.8)
+    UiButtonPressColor(1.0, 0.78, 0.3)
+
+    UiTranslate(0, 0)
+    UiImage("MOD/elevator/panel-background.png")
+
+    UiAlign("center middle")
+
+    -- Buttons
+    UiPush()
+    UiTranslate(UiCenter() - BUTTON_SIZE - BUTTON_PADDING, BUTTON_Y)
+    UiFont("MOD/elevator/bahnschrift.ttf", BUTTON_FONT_SIZE)
+    UiColor(0, 0, 0)
+    UiButtonImageBox("MOD/elevator/button.png", 25, 25)
+    local sizeAndPadding = BUTTON_SIZE + BUTTON_PADDING
+    --[[for y=0,2 do
+    	for x=0,2 do
+    		local i = (y * 3) + x + 1
+    		UiPush()
+    		UiTranslate(x * sizeAndPadding, y * sizeAndPadding)
+    		if button(i) then
+    			keyPressTimeout = GetTime() + 2
+    			addToBuffer(i)
+    		end
+    		UiPop()
+    	end
+    end]]--
+    UiTranslate(-30, -260)
+    if button("") then
+    	numberBuffer = "14"
+    end
+    UiTranslate(sizeAndPadding+110, sizeAndPadding)
+    if button("") then
+    	numberBuffer = "13"
+    end
+    UiTranslate(-sizeAndPadding-110, 0)
+    if button("") then
+    	numberBuffer = "12"
+    end
+    UiTranslate(sizeAndPadding+110, sizeAndPadding)
+    if button("") then
+    	numberBuffer = "11"
+    end
+    UiTranslate(-sizeAndPadding-110, 0)
+    if button("") then
+    	numberBuffer = "10"
+    end
+    UiTranslate(sizeAndPadding+110, sizeAndPadding)
+    if button("") then
+    	numberBuffer = "9"
+    end
+    UiTranslate(-sizeAndPadding-110, 0)
+    if button("") then
+    	numberBuffer = "8"
+    end
+    UiTranslate(sizeAndPadding+110, sizeAndPadding)
+    if button("") then
+    	numberBuffer = "7"
+    end
+    UiTranslate(-sizeAndPadding-110, 0)
+    if button("") then
+    	numberBuffer = "6"
+    end
+    UiTranslate(sizeAndPadding+110, sizeAndPadding)
+    if button("3") then
+    	numberBuffer = "5"
+    end
+    UiTranslate(-sizeAndPadding-110, 0)
+    if button("2") then
+    	numberBuffer = "4"
+    end
+    UiTranslate(sizeAndPadding+110, sizeAndPadding)
+    if button("1") then
+    	numberBuffer = "3"
+    end
+    UiTranslate(-sizeAndPadding-110, 0)
+    if button("SC") then
+    	numberBuffer = "2"
+    end
+    UiTranslate(sizeAndPadding+110, sizeAndPadding)
+    if button("M") then
+    	numberBuffer = "1"
+    end
+    UiTranslate(-sizeAndPadding-110, 0)
+    if button("DR") then
+    	numberBuffer = "G"
+    end
+    UiTranslate(83, 180)
+    if button(" ") then
+
+    end
+    UiPop()
+
+    -- Floor number
+
+    -- Check if ok to set destination
+    if GetPlayerScreen() == screen and (numberBuffer == "G" or #numberBuffer >= MAX_DIGITS or (keyPressTimeout > 0 and GetTime() > keyPressTimeout)) then
+    	keyPressTimeout = 0
+    	if numberBuffer == "G" then
+    		setDestinationFloor(0)
+    	else
+    		setDestinationFloor(tonumber(numberBuffer))
+    	end
+    	SetPlayerScreen(0)
+    end
+end
+

```

---

# Migration Report: elevator\elevator.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/elevator\elevator.lua
+++ patched/elevator\elevator.lua
@@ -1,93 +1,4 @@
--- Controls an elevator on a prismatic joint with two buttons
-
-
--- States
-IDLE          = 1  -- Stationary and awaiting input
-NUMPAD        = 2  -- Floor number is being entered into numpad
-BUTTON_DOWN   = 3  -- Button has been pressed down
-DOORS_CLOSING = 4  -- Doors closing
-ACCELERATING  = 5  -- Moving up or down
-DECELERATING  = 6  -- Slowing down, approaching destination
-DOORS_OPENING = 7  -- Doors opening
-
--- Door commands
-OPEN  = 1
-CLOSE = 2
-
-elevatorId = GetStringParam("id", "NO_ID_SET")
-
--- Constants
-MAX_SPEED = 2.5          -- Meters/second.
-INS_SPEED = 0.5        -- m/s
-ACCEL_TIME = 0.5         -- Seconds. Time needed to accelerate up to full speed.
-DECEL_DIST = 1.5        -- Meters. Start to decelerate this distance away from destination.
-MIN_DECEL_SPEED = 0.85  -- Meters/second. Don't go slower than this when decelerating.
-STOP_THRESHOLD = 0.01  -- Meters. When cabin is +/- this distance it will be considered to have stopped.
-BUTTON_DOWN_TIME = 0.75 -- Seconds. Amount of time that button should stay pressed.
-
-function init()
-	debug = false
-	firstTime = true
-	time = 0
-	currentState = IDLE
-	currentButtonPressed = nil
-	currentFloorPressed = 0
-	speed = 0
-	oldSpeed = 0
-	direction = 1  -- 1 for up, -1 for down
-	decelPos = 0   -- Position at which to start decellerating before reaching destination
-	
-	INS = false
-	maxspeed = MAX_SPEED
-
-	setCurrentFloor(0)
-	setDestinationFloor(0)
-
-	clickUp = LoadSound("clickup.ogg")
-	clickDown = LoadSound("clickdown.ogg")
-	motorSound = LoadLoop("MOD/elevator/sound/motor.ogg")
-	
-	stopButton = FindShape("emergency-stop")
-	insButton = FindShape("ins-toggle")
-	ins_upButton = FindShape("ins-up")
-	ins_dnButton = FindShape("ins-dn")
-	motor = FindJoint("motor")
-	cwmotor = FindJoint("cwmotor")
-	cabin = GetShapeBody(FindShape("cabin"))
-	numpad = FindShape("numpad")
-	numpadScreen = FindScreen("numpad")
-	upButtons = findButtons()
-	if #upButtons == 0 then
-		selfDebugPrint("Cannot find buttons")
-	end
-	floorPositions = findFloors()
-	if #floorPositions == 0 then
-		selfDebugPrint("Cannot find floors")
-	end
-	if debug then
-		selfDebugPrint("Found " .. #upButtons .. " up buttons and " .. #downButtons .. " down buttons")
-		selfDebugPrint("Found " .. #floorPositions .. " floor positions")
-		selfDebugPrint("Found " .. #doors .. " door pairs")
-	end
-
-	SetTag(stopButton, "interact", "Stop")
-	SetTag(insButton, "interact", "Inspection Mode")
-	SetTag(ins_upButton, "interact", "Up")
-	SetTag(ins_dnButton, "interact", "Down")
-	for i=1, #upButtons do
-		SetTag(upButtons[i], "interact", "Call")
-		buttonLightOff(upButtons[i])
-	end
-end
-
-
-
----------------------------
---                       --
---   State functions     --
---                       --
----------------------------
-
+#version 2
 function changeState(newState)
 	time = 0     -- Reset time counter
 	currentState = newState
@@ -98,7 +9,7 @@
 	SetTag(numpad, "interact", "Enter floor")
 
 	if InputPressed("interact") then
-		local thing = GetPlayerInteractShape()
+		local thing = GetPlayerInteractShape(playerId)
 		if thing == numpad then
 			RemoveTag(numpad, "interact")
 			SetPlayerScreen(numpadScreen)
@@ -179,7 +90,6 @@
 	end
 end
 
-
 function stop()
 	speed = 0
 	oldSpeed = 0
@@ -214,7 +124,6 @@
 	end
 end
 
-
 function press(button)
 	local t = GetShapeLocalTransform(button)
 	PlaySound(clickDown, TransformToParentPoint(GetBodyTransform(GetShapeBody(button)), t.pos))
@@ -227,14 +136,6 @@
 	buttonLightOff(button)
 end
 
-
-
----------------------------
---                       --
---   Getters/Setters     --
---                       --
----------------------------
-
 function getCurrentFloor()
 	return GetInt("level.elevator" .. elevatorId .. ".currentFloor")
 end
@@ -244,33 +145,23 @@
 end
 
 function setInspection(num)
-	SetInt("level.elevator" .. elevatorId .. ".ins", num)
+	SetInt("level.elevator" .. elevatorId .. ".ins", num, true)
 end
 
 function setCurrentFloor(num)
-	SetInt("level.elevator" .. elevatorId .. ".currentFloor", num)
+	SetInt("level.elevator" .. elevatorId .. ".currentFloor", num, true)
 end
 
 function setDestinationFloor(num)
-	SetInt("level.elevator" .. elevatorId .. ".destinationFloor", num)
-end
-
-
-
----------------------------
---                       --
---   Misc functions      --
---                       --
----------------------------
-
--- Returns two arrays of buttons (up and down), sorted from lowest to highest
+	SetInt("level.elevator" .. elevatorId .. ".destinationFloor", num, true)
+end
+
 function findButtons()
 	local upButtons = FindShapes("up")
 	table.sort(upButtons, sortShapeByPos)
 	return upButtons
 end
 
--- Returns an array of vertical positions of each floor, sorted from lowest to highest
 function findFloors()
 	local locations = FindLocations("floor")
 	local positions = {}
@@ -281,10 +172,6 @@
 	return positions
 end
 
--- Returns an array of tables representing the left and right doors for each floor
-
-
--- Find floor closest to current cabin position
 function findClosestFloor()
 	local i = 1
 	while i < #floorPositions and getCabinBottomPos() > (floorPositions[i] + floorPositions[i+1]) / 2 do
@@ -293,11 +180,9 @@
 	return i - 1  -- Floor numbers are zero-based (ground is zero)
 end
 
-
 function sortShapeByPos(a, b)
 	return GetShapeWorldTransform(a).pos[2] < GetShapeWorldTransform(b).pos[2]
 end
-
 
 function getDestinationPos()
 	return floorPositions[getDestinationFloor() + 1]
@@ -311,6 +196,7 @@
 function buttonLightOn(button)
 	SetShapeEmissiveScale(button, 1)
 end
+
 function buttonLightOff(button)
 	SetShapeEmissiveScale(button, 0.02)
 end
@@ -319,7 +205,6 @@
 	return (number > 0 and 1) or (number == 0 and 0) or -1
 end
 
-
 function selfDebugPrint(message)
 	DebugPrint("Elevator " .. elevatorId .. ": " .. message)
 end
@@ -328,71 +213,111 @@
 	DebugWatch("Elevator " .. elevatorId .. ": " .. name, value)
 end
 
-
-
----------------------------
---                       --
---   Main loop           --
---                       --
----------------------------
-
-stateFuncMap = {
-	[IDLE]          = doIdle,
-	[NUMPAD]        = doNumpad,
-	[BUTTON_DOWN]   = doButtonDown,
-	[DOORS_CLOSING] = doDoorsClosing,
-	[ACCELERATING]  = doAccelerating,
-	[DECELERATING]  = doDecelerating,
-	[DOORS_OPENING] = doDoorsOpening
-}
-
-function tick(timeDelta)
-	time = time + timeDelta
-
-	if debug then
-		selfDebugWatch("time", string.format("%.2f", time))
-		selfDebugWatch("state", currentState)
-		selfDebugWatch("current floor", getCurrentFloor())
-		selfDebugWatch("destination floor", getDestinationFloor())
-	end
-	if InputPressed("interact") then
-		if GetPlayerInteractShape() == stopButton then
-			changeState(IDLE)
-		end
-		if GetPlayerInteractShape() == insButton then
-			if INS == false then
-				changeState(IDLE)
-				INS = true
-				MAX_SPEED = INS_SPEED
-				setInspection(1)
-				SetTag(insButton, "interact", "Normal Mode")
-			else
-				INS = false
-				MAX_SPEED = maxspeed
-				setInspection(0)
-				SetTag(insButton, "interact", "Inspection Mode")
-			end
-		end
-		if GetPlayerInteractShape() == ins_upButton then
-			if INS == true then
-				setDestinationFloor(#upButtons-1)
-				changeState(DOORS_CLOSING)
-			end
-		end
-		if GetPlayerInteractShape() == ins_dnButton then
-			if INS == true then
-				setDestinationFloor("G")
-				changeState(DOORS_CLOSING)
-			end
-		end
-	end
-	local func = stateFuncMap[currentState]
-	if func then
-		func()
-	else
-		-- Somehow got into trouble, reset
-		DebugPrint("Elevator "..elevatorId.." got into an Unknown state: "..currentState)
-		changeState(IDLE)
-	end
-end
-
+function server.init()
+    debug = false
+    firstTime = true
+    time = 0
+    currentState = IDLE
+    currentButtonPressed = nil
+    currentFloorPressed = 0
+    speed = 0
+    oldSpeed = 0
+    direction = 1  -- 1 for up, -1 for down
+    decelPos = 0   -- Position at which to start decellerating before reaching destination
+    INS = false
+    maxspeed = MAX_SPEED
+    setCurrentFloor(0)
+    setDestinationFloor(0)
+    motorSound = LoadLoop("MOD/elevator/sound/motor.ogg")
+    stopButton = FindShape("emergency-stop")
+    insButton = FindShape("ins-toggle")
+    ins_upButton = FindShape("ins-up")
+    ins_dnButton = FindShape("ins-dn")
+    motor = FindJoint("motor")
+    cwmotor = FindJoint("cwmotor")
+    cabin = GetShapeBody(FindShape("cabin"))
+    numpad = FindShape("numpad")
+    numpadScreen = FindScreen("numpad")
+    upButtons = findButtons()
+    if #upButtons == 0 then
+    	selfDebugPrint("Cannot find buttons")
+    end
+    floorPositions = findFloors()
+    if #floorPositions == 0 then
+    	selfDebugPrint("Cannot find floors")
+    end
+    if debug then
+    	selfDebugPrint("Found " .. #upButtons .. " up buttons and " .. #downButtons .. " down buttons")
+    	selfDebugPrint("Found " .. #floorPositions .. " floor positions")
+    	selfDebugPrint("Found " .. #doors .. " door pairs")
+    end
+    SetTag(stopButton, "interact", "Stop")
+    SetTag(insButton, "interact", "Inspection Mode")
+    SetTag(ins_upButton, "interact", "Up")
+    SetTag(ins_dnButton, "interact", "Down")
+    for i=1, #upButtons do
+    	SetTag(upButtons[i], "interact", "Call")
+    	buttonLightOff(upButtons[i])
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        time = time + timeDelta
+        if debug then
+        	selfDebugWatch("time", string.format("%.2f", time))
+        	selfDebugWatch("state", currentState)
+        	selfDebugWatch("current floor", getCurrentFloor())
+        	selfDebugWatch("destination floor", getDestinationFloor())
+        end
+        local func = stateFuncMap[currentState]
+        if func then
+        	func()
+        else
+        	-- Somehow got into trouble, reset
+        	DebugPrint("Elevator "..elevatorId.." got into an Unknown state: "..currentState)
+        	changeState(IDLE)
+        end
+    end
+end
+
+function client.init()
+    clickUp = LoadSound("clickup.ogg")
+    clickDown = LoadSound("clickdown.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("interact") then
+    	if GetPlayerInteractShape(playerId) == stopButton then
+    		changeState(IDLE)
+    	end
+    	if GetPlayerInteractShape(playerId) == insButton then
+    		if INS == false then
+    			changeState(IDLE)
+    			INS = true
+    			MAX_SPEED = INS_SPEED
+    			setInspection(1)
+    			SetTag(insButton, "interact", "Normal Mode")
+    		else
+    			INS = false
+    			MAX_SPEED = maxspeed
+    			setInspection(0)
+    			SetTag(insButton, "interact", "Inspection Mode")
+    		end
+    	end
+    	if GetPlayerInteractShape(playerId) == ins_upButton then
+    		if INS == true then
+    			setDestinationFloor(#upButtons-1)
+    			changeState(DOORS_CLOSING)
+    		end
+    	end
+    	if GetPlayerInteractShape(playerId) == ins_dnButton then
+    		if INS == true then
+    			setDestinationFloor("G")
+    			changeState(DOORS_CLOSING)
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: flag.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/flag.lua
+++ patched/flag.lua
@@ -1,75 +1,77 @@
-function init()
-flags = FindBodies("flag")
-flag1 = FindBody("flag2")
-flag2 = FindBody("flag3")
-pole = FindBody("pole")
-
-edges = FindBodies("edge")
-deattime= 2
-deadflag = false
-wait = 8
-wait2 = 0
-wait3 = 5
-wait4 = 0
+#version 2
+function server.init()
+    flags = FindBodies("flag")
+    flag1 = FindBody("flag2")
+    flag2 = FindBody("flag3")
+    pole = FindBody("pole")
+    edges = FindBodies("edge")
+    deattime= 2
+    deadflag = false
+    wait = 8
+    wait2 = 0
+    wait3 = 5
+    wait4 = 0
 end
 
-function update(dt)
-if IsBodyBroken(pole) then
-deattime = deattime - dt
-if deattime < 0 then
-deadflag = false
-end
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsBodyBroken(pole) then
+        deattime = deattime - dt
+        if deattime < 0 then
+        deadflag = false
+        end
+        end
+        if not deadflag then
+
+        for i=1,#edges do      
+        local edge = edges[i] 
+        local t = GetBodyTransform(edge)
+        local force1 = .8
+        local fwd1 = Vec(0,1,0)
+        local fwd2 = TransformToParentVec(t,Vec(1,0,0))
+        ApplyBodyImpulse(edge, t.pos, VecScale(fwd1,force1))
+        end
+
+        wait = wait + dt
+        wait3 = wait3 + dt
+
+        if wait > 3 then 
+        local number = math.random(1,2)
+        if number == 1 then
+        local t = GetBodyTransform(flag1)
+        local force2 = math.random(-1,1)-.2
+        local up = math.random(-6,6)
+        local side = math.random(-6,6)
+        local fwd2 = TransformToParentVec(t,Vec(side,0,up))
+
+        ApplyBodyImpulse(flag1, t.pos, VecScale(fwd2,force2))
+        wait2 = wait2 + dt
+        if wait2 > 10 then
+        wait = 0
+        wait2 = math.random(5,8)
+        end
+        end
+        end
+        --------------------------------
+
+        if wait > 3 then 
+        local number = math.random(1,2)
+        if number == 1 then
+        local t = GetBodyTransform(flag2)
+        local force2 = math.random(-1,1)-.2
+        local up = math.random(-6,6)
+        local side = math.random(-6,6)
+        local fwd2 = TransformToParentVec(t,Vec(side,0,up))
+
+        ApplyBodyImpulse(flag2, t.pos, VecScale(fwd2,force3))
+        wait4 = wait4 + dt
+        if wait4 > 10 then
+        wait3 = 0
+        wait4 = math.random(5,8)
+        end
+        end
+        end
+        end
+    end
 end
 
-if not deadflag then
-
-for i=1,#edges do      
-local edge = edges[i] 
-local t = GetBodyTransform(edge)
-local force1 = .8
-local fwd1 = Vec(0,1,0)
-local fwd2 = TransformToParentVec(t,Vec(1,0,0))
-ApplyBodyImpulse(edge, t.pos, VecScale(fwd1,force1))
-end
-
-wait = wait + dt
-wait3 = wait3 + dt
-
-if wait > 3 then 
-local number = math.random(1,2)
-if number == 1 then
-local t = GetBodyTransform(flag1)
-local force2 = math.random(-1,1)-.2
-local up = math.random(-6,6)
-local side = math.random(-6,6)
-local fwd2 = TransformToParentVec(t,Vec(side,0,up))
-
-ApplyBodyImpulse(flag1, t.pos, VecScale(fwd2,force2))
-wait2 = wait2 + dt
-if wait2 > 10 then
-wait = 0
-wait2 = math.random(5,8)
-end
-end
-end
---------------------------------
-
-if wait > 3 then 
-local number = math.random(1,2)
-if number == 1 then
-local t = GetBodyTransform(flag2)
-local force2 = math.random(-1,1)-.2
-local up = math.random(-6,6)
-local side = math.random(-6,6)
-local fwd2 = TransformToParentVec(t,Vec(side,0,up))
-
-ApplyBodyImpulse(flag2, t.pos, VecScale(fwd2,force3))
-wait4 = wait4 + dt
-if wait4 > 10 then
-wait3 = 0
-wait4 = math.random(5,8)
-end
-end
-end
-end
-end

```

---

# Migration Report: Gate.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Gate.lua
+++ patched/Gate.lua
@@ -1,39 +1,45 @@
-function init()
-    Door = FindJoint("motor")
-	Door2 = FindJoint("motor2")
-    btn = FindShape("btn")
-    btn2 = FindShape("btn2")
-    SetJointMotor(Door, 3.5)
-    min, max = GetJointLimits(Door)     
-    --DebugPrint("Load")
-   -- DebugPrint(btn)
-    --DebugPrint(btn2)
-	strength = GetFloatParam("strength", 5000)
-	buzzer = LoadSound("MOD/snd/gate.ogg")
-	loc = FindLocation("sound")
-	u = GetLocationTransform(loc)
-	pos = u.pos
-	
+#version 2
+function server.init()
+       Door = FindJoint("motor")
+    Door2 = FindJoint("motor2")
+       btn = FindShape("btn")
+       btn2 = FindShape("btn2")
+       SetJointMotor(Door, 3.5)
+       min, max = GetJointLimits(Door)     
+       --DebugPrint("Load")
+      -- DebugPrint(btn)
+       --DebugPrint(btn2)
+    strength = GetFloatParam("strength", 5000)
+    loc = FindLocation("sound")
+    u = GetLocationTransform(loc)
+    pos = u.pos
+end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+          if lit then
+              SetTag(btn, "interact", "Close")   
+              SetTag(btn2, "interact", "Close")   
+              SetJointMotorTarget(Door, max, 1, strength)
+        SetJointMotorTarget(Door2, max, 1, strength)
+          else
+              SetTag(btn, "interact", "Open")
+              SetTag(btn2, "interact", "Open")
+              SetJointMotorTarget(Door, min, 1, strength)
+        SetJointMotorTarget(Door2, min, 1, strength)
+          end
+    end
 end
-lit = false
 
+function client.init()
+    buzzer = LoadSound("MOD/snd/gate.ogg")
+end
 
-function tick(dt)
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+      if (GetPlayerInteractShape(playerId) == btn2 or GetPlayerInteractShape(playerId) == btn) and InputPressed("interact") then
+          lit = not lit
+    PlaySound(buzzer, pos, 0.5)
+      end
+end
 
-    if (GetPlayerInteractShape() == btn2 or GetPlayerInteractShape() == btn) and InputPressed("interact") then
-        lit = not lit
-		PlaySound(buzzer, pos, 0.5)
-    end
-    if lit then
-        SetTag(btn, "interact", "Close")   
-        SetTag(btn2, "interact", "Close")   
-        SetJointMotorTarget(Door, max, 1, strength)
-		SetJointMotorTarget(Door2, max, 1, strength)
-    else
-        SetTag(btn, "interact", "Open")
-        SetTag(btn2, "interact", "Open")
-        SetJointMotorTarget(Door, min, 1, strength)
-		SetJointMotorTarget(Door2, min, 1, strength)
-    end
-end
```

---

# Migration Report: Gate2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Gate2.lua
+++ patched/Gate2.lua
@@ -1,36 +1,42 @@
-function init()
-    Door = FindJoint("motor")
-    btn = FindShape("btn")
-    btn2 = FindShape("btn2")
-    SetJointMotor(Door, 3.5)
-    min, max = GetJointLimits(Door)     
-    --DebugPrint("Load")
-   -- DebugPrint(btn)
-    --DebugPrint(btn2)
-	strength = GetFloatParam("strength", 5000)
-	buzzer = LoadSound("MOD/snd/gate.ogg")
-	loc = FindLocation("sound")
-	u = GetLocationTransform(loc)
-	pos = u.pos
-	
+#version 2
+function server.init()
+       Door = FindJoint("motor")
+       btn = FindShape("btn")
+       btn2 = FindShape("btn2")
+       SetJointMotor(Door, 3.5)
+       min, max = GetJointLimits(Door)     
+       --DebugPrint("Load")
+      -- DebugPrint(btn)
+       --DebugPrint(btn2)
+    strength = GetFloatParam("strength", 5000)
+    loc = FindLocation("sound")
+    u = GetLocationTransform(loc)
+    pos = u.pos
+end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if lit then
+            SetTag(btn, "interact", "Close")   
+            SetTag(btn2, "interact", "Close")   
+            SetJointMotorTarget(Door, max, 1, strength)
+        else
+            SetTag(btn, "interact", "Open")
+            SetTag(btn2, "interact", "Open")
+            SetJointMotorTarget(Door, min, 1, strength)
+        end
+    end
 end
-lit = false
 
+function client.init()
+    buzzer = LoadSound("MOD/snd/gate.ogg")
+end
 
-function tick(dt)
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+      if (GetPlayerInteractShape(playerId) == btn2 or GetPlayerInteractShape(playerId) == btn) and InputPressed("interact") then
+          lit = not lit
+    PlaySound(buzzer, pos, 0.5)
+      end
+end
 
-    if (GetPlayerInteractShape() == btn2 or GetPlayerInteractShape() == btn) and InputPressed("interact") then
-        lit = not lit
-		PlaySound(buzzer, pos, 0.5)
-    end
-    if lit then
-        SetTag(btn, "interact", "Close")   
-        SetTag(btn2, "interact", "Close")   
-        SetJointMotorTarget(Door, max, 1, strength)
-    else
-        SetTag(btn, "interact", "Open")
-        SetTag(btn2, "interact", "Open")
-        SetJointMotorTarget(Door, min, 1, strength)
-    end
-end
```

---

# Migration Report: ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/ground.lua
+++ patched/ground.lua
@@ -1,10 +1,5 @@
-file = GetString("file", "testground.png", "script png")
-grassMap = GetString("grass", "", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
-hollow = GetInt("hollow", 0)
-
-function init()
+#version 2
+function server.init()
     matRock = CreateMaterial("rock", 0.41569, 0.40784, 0.37647)
     matDirt = CreateMaterial("dirt", 0.34118, 0.30588, 0.25098, 1, 0, 0.1)
     matGrass1 = CreateMaterial("unphysical", 0.27451, 0.34510, 0.23137, 1, 0, 0.2)
@@ -12,7 +7,6 @@
     matTarmac = CreateMaterial("masonry", 0.39608, 0.39216, 0.38824, 1, 0, 0.4)
     matTarmacTrack = CreateMaterial("masonry", 0.3, 0.3, 0.3, 1, 0, 0.3)
     matTarmacLine = CreateMaterial("masonry", 0.7, 0.7, 0.7, 1, 0, 0.6)
-
     if grassMap == "" then
         LoadImage(file)
     else
@@ -27,12 +21,8 @@
         end
         LoadImage(file, grassMap)
     end
-    
-    
     w,h = GetImageSize()
-
     local maxSize = tileSize
-    
     local y0 = 0
     while y0 < h-1 do
         local y1 = y0 + maxSize
@@ -49,3 +39,4 @@
         y0 = y1
     end
 end
+

```

---

# Migration Report: Labor.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Labor.lua
+++ patched/Labor.lua
@@ -1,35 +1,42 @@
-function init()
-    Door = FindJoint("motor")
-    btn = FindShape("btn")
-    btn2 = FindShape("btn2")
-    SetJointMotor(Door, 3.5)
-    min, max = GetJointLimits(Door)     
-    --DebugPrint("Load")
-   -- DebugPrint(btn)
-    --DebugPrint(btn2)
-	strength = GetFloatParam("strength", 5000)
-	buzzer = LoadSound("MOD/snd/buzzer2.ogg")
-	loc = FindLocation("sound")
-	u = GetLocationTransform(loc)
-	pos = u.pos
-	
+#version 2
+function server.init()
+       Door = FindJoint("motor")
+       btn = FindShape("btn")
+       btn2 = FindShape("btn2")
+       SetJointMotor(Door, 3.5)
+       min, max = GetJointLimits(Door)     
+       --DebugPrint("Load")
+      -- DebugPrint(btn)
+       --DebugPrint(btn2)
+    strength = GetFloatParam("strength", 5000)
+    loc = FindLocation("sound")
+    u = GetLocationTransform(loc)
+    pos = u.pos
+end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if lit then
+            SetTag(btn, "interact", "Close")   
+            SetTag(btn2, "interact", "Close")   
+            SetJointMotorTarget(Door, max, 0.5, strength)
+        else
+            SetTag(btn, "interact", "Open")
+            SetTag(btn2, "interact", "Open")
+            SetJointMotorTarget(Door, min, 0.5, strength)
+        end
+    end
 end
-lit = false
 
+function client.init()
+    buzzer = LoadSound("MOD/snd/buzzer2.ogg")
+end
 
-function tick(dt)
-    if (GetPlayerInteractShape() == btn2 or GetPlayerInteractShape() == btn) and InputPressed("interact") then
-        lit = not lit
-		PlaySound(buzzer, pos, 0.5)
-    end
-    if lit then
-        SetTag(btn, "interact", "Close")   
-        SetTag(btn2, "interact", "Close")   
-        SetJointMotorTarget(Door, max, 0.5, strength)
-    else
-        SetTag(btn, "interact", "Open")
-        SetTag(btn2, "interact", "Open")
-        SetJointMotorTarget(Door, min, 0.5, strength)
-    end
-end+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+      if (GetPlayerInteractShape(playerId) == btn2 or GetPlayerInteractShape(playerId) == btn) and InputPressed("interact") then
+          lit = not lit
+    PlaySound(buzzer, pos, 0.5)
+      end
+end
+

```

---

# Migration Report: main\realistic_house\script\lightswitch2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\realistic_house\script\lightswitch2.lua
+++ patched/main\realistic_house\script\lightswitch2.lua
@@ -1,41 +1,43 @@
-function init()
-	lightswitch = FindShape("lightswitch")
-	SetTag(lightswitch, "interact","FLOODLIGHTS")
-	
-    lightShape = FindShapes("light")
-	lights = FindLights("lockdown")
-	
-    joint = FindJoint("switch")
-	
-	switch = false
+#version 2
+function server.init()
+    lightswitch = FindShape("lightswitch")
+    SetTag(lightswitch, "interact","FLOODLIGHTS")
+       lightShape = FindShapes("light")
+    lights = FindLights("lockdown")
+       joint = FindJoint("switch")
+    switch = false
 end
 
-function tick(dt)
-	master = GetBool("level.master2")
-	override = GetBool("level.override2")
-	broken = IsShapeBroken(lightShape[i])
-	if GetPlayerInteractShape() == lightswitch and InputPressed("interact") then
-		if switch then
-			switch = false
-		else
-			switch = true
-		end
-	end
-	
-	for i=1,#lights do
-		if not broken then	
-			if override then
-				SetLightEnabled(lights[i], master)
-			else
-				SetLightEnabled(lights[i], switch)
-			end
-			if switch or master then
-				SetJointMotorTarget(joint, 1, 1)
-			elseif not switch and not master then
-				SetJointMotorTarget(joint, -1, 1)
-			end
-		end
-	end
-	
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        master = GetBool("level.master2")
+        override = GetBool("level.override2")
+        broken = IsShapeBroken(lightShape[i])
+        for i=1,#lights do
+        	if not broken then	
+        		if override then
+        			SetLightEnabled(lights[i], master)
+        		else
+        			SetLightEnabled(lights[i], switch)
+        		end
+        		if switch or master then
+        			SetJointMotorTarget(joint, 1, 1)
+        		elseif not switch and not master then
+        			SetJointMotorTarget(joint, -1, 1)
+        		end
+        	end
+        end
+    end
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == lightswitch and InputPressed("interact") then
+    	if switch then
+    		switch = false
+    	else
+    		switch = true
+    	end
+    end
+end
+

```

---

# Migration Report: main\script\robot.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\script\robot.lua
+++ patched/main\script\robot.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,35 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 3.5)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 25
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 100.0
-config.aggressive = false
-config.stepSound = "m"
-config.practice = false
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -180,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -197,42 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.health = 100.0
-robot.headDamageScale = 3.0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -240,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 	robot.body = FindBody("body")
@@ -260,22 +115,18 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
-
 
 function robotUpdate(dt)
 	robotSetAxes()
@@ -291,7 +142,7 @@
 			robot.playerPos = Vec(0, -100, 0)
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	local vel = GetBodyVelocity(robot.body)
@@ -303,7 +154,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -333,7 +184,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -348,31 +199,19 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 0.3
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	QueryRequire("physical large")
@@ -385,9 +224,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -395,10 +233,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -417,7 +251,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -434,7 +267,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -447,7 +279,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -463,8 +294,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -527,7 +356,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -536,7 +365,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -547,15 +376,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -572,11 +392,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -585,12 +405,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -623,7 +437,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -651,9 +464,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -698,7 +510,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -740,13 +552,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -787,13 +592,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -820,7 +623,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -828,7 +630,6 @@
 		weapons[i].fire = 0
 	end
 end
-
 
 function weaponEmitFire(weapon, t, amount)
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -849,7 +650,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -862,22 +663,21 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 5.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
 				rejectAllBodies(robot.allBodies)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.015 * weapon.strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.015 * weapon.strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -901,7 +701,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -966,15 +766,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -984,7 +776,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1009,22 +800,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1063,32 +842,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1112,7 +871,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1159,7 +918,7 @@
 				head.alarmTimer = head.alarmTimer + dt
 				PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetBool("level.alarm", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1188,26 +947,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(0, -100, 0)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1243,35 +993,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1363,7 +1094,7 @@
 		end
 
 		local targetRadius = 1.0
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 4.0
 		end
 	
@@ -1394,9 +1125,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1406,7 +1136,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1456,12 +1186,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1510,7 +1234,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1519,8 +1243,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1536,7 +1258,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1551,7 +1272,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1559,7 +1279,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1570,7 +1289,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1589,441 +1307,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
-	turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("robot/alert.ogg", 9.0)
-	huntSound = LoadSound("robot/hunt.ogg", 9.0)
-	idleSound = LoadSound("robot/idle.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(fdeath, robot.bodyCenter, 9.0, false)
-		PlaySound(insound, robot.bodyCenter, 0.3, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		PlaySound(disableSound, robot.bodyCenter)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 8.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			--PlaySound(idleSound, robot.bodyCenter)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			--PlaySound(idleSound, robot.bodyCenter)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			--PlaySound(huntSound, robot.bodyCenter)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2032,64 +1315,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2114,14 +1339,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2146,19 +1370,15 @@
 	end
 end
 
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2176,8 +1396,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2204,3 +1422,471 @@
 	end
 end
 
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 8.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "investigate" then
+        	if not state.nextAction then
+        		local pos = state.pos
+        		robotTurnTowards(state.pos)
+        		headTurnTowards(state.pos)
+        		local nav = stackPush("navigate")
+        		nav.pos = state.pos
+        		nav.timeout = 5.0
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "done"
+        	elseif state.nextAction == "done" then
+        		--PlaySound(idleSound, robot.bodyCenter)
+        		stackPop()
+        	end	
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        if state.id == "huntlost" then
+        	if not state.timer then
+        		state.timer = 6
+        		state.turnTimer = 1
+        	end
+        	state.timer = state.timer - dt
+        	head.dir = VecCopy(robot.dir)
+        	if state.timer < 0 then
+        		--PlaySound(idleSound, robot.bodyCenter)
+        		stackPop()
+        	else
+        		state.turnTimer = state.turnTimer - dt
+        		if state.turnTimer < 0 then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turnTimer = rnd(0.5, 1.5)
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+        if state.id == "navigate" then
+        	if not state.initialized then
+        		if not state.timeout then state.timeout = 30 end
+        		navigationClear()
+        		navigationSetTarget(state.pos, state.timeout)
+        		state.initialized = true
+        	else
+        		head.dir = VecCopy(robot.dir)
+        		navigationUpdate(dt)
+        		if navigation.state == "done" or navigation.state == "fail" then
+        			stackPop()
+        		end
+        	end
+        end
+
+        --React to sound
+        if not stackHas("hunt") then
+        	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+        		stackClear()
+        		--PlaySound(alertSound, robot.bodyCenter)
+        		local s = stackPush("investigate")
+        		s.pos = hearing.lastSoundPos	
+        		hearingConsumeSound()
+        	end
+        end
+
+        --Seen player
+        if config.huntPlayer and not stackHas("hunt") then
+        	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+        		stackClear()
+        		--PlaySound(huntSound, robot.bodyCenter)
+        		stackPush("hunt")
+        	end
+        end
+
+        --Seen player
+        if config.avoidPlayer and not stackHas("avoid") then
+        	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+        		stackClear()
+        		stackPush("avoid")
+        	end
+        end
+
+        --Get up
+        if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+        	stackPush("getup")
+        end
+
+        if IsShapeBroken(GetLightShape(head.eye)) then
+        	config.hasVision = false
+        	config.canSeePlayer = false
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
+    turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("robot/alert.ogg", 9.0)
+    huntSound = LoadSound("robot/hunt.ogg", 9.0)
+    idleSound = LoadSound("robot/idle.ogg", 9.0)
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(fdeath, robot.bodyCenter, 9.0, false)
+    	PlaySound(insound, robot.bodyCenter, 0.3, false)
+    end
+    if IsPointInWater(robot.bodyCenter) then
+    	PlaySound(disableSound, robot.bodyCenter)
+    	for i=1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    end
+end
+

```

---

# Migration Report: main\scripts\AutoGate1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\AutoGate1.lua
+++ patched/main\scripts\AutoGate1.lua
@@ -1,97 +1,98 @@
-function init()
-	gate1_open = FindShapes("gate1_open", true)
-	gate1_close = FindShapes("gate1_close", true)
-	
-	for i=1,#gate1_open do
-		SetTag(gate1_open[i], "interact", "OPEN")
-	end
-	for i=1,#gate1_close do
-		SetTag(gate1_close[i], "interact", "CLOSE")
-	end
-	
-	gate1_door = FindJoints("gate1_door",true)
-	gate1_door_min, gate1_door_max = GetJointLimits(gate1_door[1])
-	gate1_door_spd = 1
-	SetJointMotor(gate1_door, 0)
-	
-	gate1_wrlt = FindJoints("gate1_warning",true)
-	gate1_lt = FindLights("gate1_wnlt",true)
-	gate1_open_lt = FindLights("gate1_open_lt",true)
-	gate1_close_lt = FindLights("gate1_close_lt",true)
-	gate1_wrlt_spd = 5
-	for i=1,#gate1_wrlt do
-		SetJointMotor(gate1_wrlt[i], 0)
-	end
-	for i=1,#gate1_lt do
-		SetLightEnabled(gate1_lt[i], false)
-	end
-	for i=1,#gate1_open_lt do
-		SetLightEnabled(gate1_open_lt[i], false)
-	end
-	for i=1,#gate1_close_lt do
-		SetLightEnabled(gate1_close_lt[i], false)
-	end
+#version 2
+function server.init()
+    gate1_open = FindShapes("gate1_open", true)
+    gate1_close = FindShapes("gate1_close", true)
+    for i=1,#gate1_open do
+    	SetTag(gate1_open[i], "interact", "OPEN")
+    end
+    for i=1,#gate1_close do
+    	SetTag(gate1_close[i], "interact", "CLOSE")
+    end
+    gate1_door = FindJoints("gate1_door",true)
+    gate1_door_min, gate1_door_max = GetJointLimits(gate1_door[1])
+    gate1_door_spd = 1
+    SetJointMotor(gate1_door, 0)
+    gate1_wrlt = FindJoints("gate1_warning",true)
+    gate1_lt = FindLights("gate1_wnlt",true)
+    gate1_open_lt = FindLights("gate1_open_lt",true)
+    gate1_close_lt = FindLights("gate1_close_lt",true)
+    gate1_wrlt_spd = 5
+    for i=1,#gate1_wrlt do
+    	SetJointMotor(gate1_wrlt[i], 0)
+    end
+    for i=1,#gate1_lt do
+    	SetLightEnabled(gate1_lt[i], false)
+    end
+    for i=1,#gate1_open_lt do
+    	SetLightEnabled(gate1_open_lt[i], false)
+    end
+    for i=1,#gate1_close_lt do
+    	SetLightEnabled(gate1_close_lt[i], false)
+    end
 end
 
-function update(dt)
-	gate1_door_stat = GetJointMovement(gate1_door[1])
-	for i=1,#gate1_open do
-		if GetPlayerInteractShape() == gate1_open[i] and InputPressed("interact") then
-			gate1_openPressed = true
-			gate1_closePressed = false
-		end
-	end
-	for i=1,#gate1_close do
-		if GetPlayerInteractShape() == gate1_close[i] and InputPressed("interact") then
-			gate1_closePressed = true
-			gate1_openPressed = false
-		end
-	end
-	
-	if gate1_openPressed then
-		for i=1,#gate1_open_lt do
-			SetLightEnabled(gate1_open_lt[i], true)
-		end
-		for i=1,#gate1_close_lt do
-			SetLightEnabled(gate1_close_lt[i], false)
-		end
-		for i=1,#gate1_door do
-			SetJointMotor(gate1_door[i], -gate1_door_spd)
-		end
-	end
-	if gate1_closePressed then
-		for i=1,#gate1_open_lt do
-			SetLightEnabled(gate1_open_lt[i], false)
-		end
-		for i=1,#gate1_close_lt do
-			SetLightEnabled(gate1_close_lt[i], true)
-		end
-		for i=1,#gate1_door do
-			SetJointMotor(gate1_door[i], gate1_door_spd)
-		end
-	end
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        gate1_door_stat = GetJointMovement(gate1_door[1])
+        if gate1_openPressed then
+        	for i=1,#gate1_open_lt do
+        		SetLightEnabled(gate1_open_lt[i], true)
+        	end
+        	for i=1,#gate1_close_lt do
+        		SetLightEnabled(gate1_close_lt[i], false)
+        	end
+        	for i=1,#gate1_door do
+        		SetJointMotor(gate1_door[i], -gate1_door_spd)
+        	end
+        end
+        if gate1_closePressed then
+        	for i=1,#gate1_open_lt do
+        		SetLightEnabled(gate1_open_lt[i], false)
+        	end
+        	for i=1,#gate1_close_lt do
+        		SetLightEnabled(gate1_close_lt[i], true)
+        	end
+        	for i=1,#gate1_door do
+        		SetJointMotor(gate1_door[i], gate1_door_spd)
+        	end
+        end
+        if gate1_door_stat > gate1_door_min+0.01 and gate1_door_stat < gate1_door_max-0.01 then
+        	for i=1,#gate1_wrlt do
+        		SetJointMotor(gate1_wrlt[i], gate1_wrlt_spd)
+        	end
+        	for i=1,#gate1_lt do
+        		SetLightEnabled(gate1_lt[i], true)
+        	end
+        else
+        	for i=1,#gate1_wrlt do
+        		SetJointMotor(gate1_wrlt[i], 0)
+        	end
+        	for i=1,#gate1_lt do
+        		SetLightEnabled(gate1_lt[i], false)
+        	end
+        	for i=1,#gate1_open_lt do
+        		SetLightEnabled(gate1_open_lt[i], false)
+        	end
+        	for i=1,#gate1_close_lt do
+        		SetLightEnabled(gate1_close_lt[i], false)
+        	end
+        end
+    end
+end
 
-	if gate1_door_stat > gate1_door_min+0.01 and gate1_door_stat < gate1_door_max-0.01 then
-		for i=1,#gate1_wrlt do
-			SetJointMotor(gate1_wrlt[i], gate1_wrlt_spd)
-		end
-		for i=1,#gate1_lt do
-			SetLightEnabled(gate1_lt[i], true)
-		end
-	else
-		for i=1,#gate1_wrlt do
-			SetJointMotor(gate1_wrlt[i], 0)
-		end
-		for i=1,#gate1_lt do
-			SetLightEnabled(gate1_lt[i], false)
-		end
-		for i=1,#gate1_open_lt do
-			SetLightEnabled(gate1_open_lt[i], false)
-		end
-		for i=1,#gate1_close_lt do
-			SetLightEnabled(gate1_close_lt[i], false)
-		end
-	end
-	
-	--DebugPrint(gate1_door_stat)
-end+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    for i=1,#gate1_open do
+    	if GetPlayerInteractShape(playerId) == gate1_open[i] and InputPressed("interact") then
+    		gate1_openPressed = true
+    		gate1_closePressed = false
+    	end
+    end
+    for i=1,#gate1_close do
+    	if GetPlayerInteractShape(playerId) == gate1_close[i] and InputPressed("interact") then
+    		gate1_closePressed = true
+    		gate1_openPressed = false
+    	end
+    end
+end
+

```

---

# Migration Report: main\scripts\AutoGate2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\AutoGate2.lua
+++ patched/main\scripts\AutoGate2.lua
@@ -1,108 +1,108 @@
-function init()
-	gate2_open = FindShapes("gate2_open", true)
-	gate2_close = FindShapes("gate2_close", true)
-	
-	for i=1,#gate2_open do
-		SetTag(gate2_open[i], "interact", "OPEN")
-	end
-	for i=1,#gate2_close do
-		SetTag(gate2_close[i], "interact", "CLOSE")
-	end
-	
-	gate2_doorMain = FindJoint("gate2_door_main",true)
-	gate2_doorInter = FindJoints("gate2_door_inter",true)
-	gate2_doorMain_min, gate2_doorMain_max = GetJointLimits(gate2_doorMain)
-	gate2_doorInter_min, gate2_doorInter_max = GetJointLimits(gate2_doorInter[3])
-	gate2_doorMain_ords = 0.5
-	gate2_doorMain_crds = 0.2
-	gate2_doorInter_ords = 0.8
-	gate2_doorInter_crds = 0.6
-	SetJointMotor(gate2_doorMain, 0)
-	for i=1,#gate2_doorInter do
-		SetJointMotor(gate2_doorInter[i], 0)
-	end
-	
-	
-	gate2_wrlt = FindJoints("gate2_warning",true)
-	gate2_lt = FindLights("gate2_wnlt",true)
-	gate2_open_lt = FindLights("gate2_open_lt",true)
-	gate2_close_lt = FindLights("gate2_close_lt",true)
-	gate2_wrlt_spd = 5
-	for i=1,#gate2_wrlt do
-		SetJointMotor(gate2_wrlt[i], 0)
-	end
-	for i=1,#gate2_lt do
-		SetLightEnabled(gate2_lt[i], false)
-	end
-	for i=1,#gate2_open_lt do
-		SetLightEnabled(gate2_open_lt[i], false)
-	end
-	for i=1,#gate2_close_lt do
-		SetLightEnabled(gate2_close_lt[i], false)
-	end
+#version 2
+function server.init()
+    gate2_open = FindShapes("gate2_open", true)
+    gate2_close = FindShapes("gate2_close", true)
+    for i=1,#gate2_open do
+    	SetTag(gate2_open[i], "interact", "OPEN")
+    end
+    for i=1,#gate2_close do
+    	SetTag(gate2_close[i], "interact", "CLOSE")
+    end
+    gate2_doorMain = FindJoint("gate2_door_main",true)
+    gate2_doorInter = FindJoints("gate2_door_inter",true)
+    gate2_doorMain_min, gate2_doorMain_max = GetJointLimits(gate2_doorMain)
+    gate2_doorInter_min, gate2_doorInter_max = GetJointLimits(gate2_doorInter[3])
+    gate2_doorMain_ords = 0.5
+    gate2_doorMain_crds = 0.2
+    gate2_doorInter_ords = 0.8
+    gate2_doorInter_crds = 0.6
+    SetJointMotor(gate2_doorMain, 0)
+    for i=1,#gate2_doorInter do
+    	SetJointMotor(gate2_doorInter[i], 0)
+    end
+    gate2_wrlt = FindJoints("gate2_warning",true)
+    gate2_lt = FindLights("gate2_wnlt",true)
+    gate2_open_lt = FindLights("gate2_open_lt",true)
+    gate2_close_lt = FindLights("gate2_close_lt",true)
+    gate2_wrlt_spd = 5
+    for i=1,#gate2_wrlt do
+    	SetJointMotor(gate2_wrlt[i], 0)
+    end
+    for i=1,#gate2_lt do
+    	SetLightEnabled(gate2_lt[i], false)
+    end
+    for i=1,#gate2_open_lt do
+    	SetLightEnabled(gate2_open_lt[i], false)
+    end
+    for i=1,#gate2_close_lt do
+    	SetLightEnabled(gate2_close_lt[i], false)
+    end
 end
 
-function update(dt)
-	gate2_door_stat = GetJointMovement(gate2_doorInter[3])
-	for i=1,#gate2_open do
-		if GetPlayerInteractShape() == gate2_open[i] and InputPressed("interact") then
-			gate2_openPressed = true
-			gate2_closePressed = false
-		end
-	end
-	for i=1,#gate2_close do
-		if GetPlayerInteractShape() == gate2_close[i] and InputPressed("interact") then
-			gate2_closePressed = true
-			gate2_openPressed = false
-		end
-	end
-	
-	if gate2_openPressed then
-		for i=1,#gate2_open_lt do
-			SetLightEnabled(gate2_open_lt[i], true)
-		end
-		for i=1,#gate2_close_lt do
-			SetLightEnabled(gate2_close_lt[i], false)
-		end
-		SetJointMotorTarget(gate2_doorMain, gate2_doorMain_max, -gate2_doorMain_ords)
-		for i=1,#gate2_doorInter do
-			SetJointMotorTarget(gate2_doorInter[i], gate2_doorInter_max, -gate2_doorInter_ords)
-		end
-	end
-	if gate2_closePressed then
-		for i=1,#gate2_open_lt do
-			SetLightEnabled(gate2_open_lt[i], false)
-		end
-		for i=1,#gate2_close_lt do
-			SetLightEnabled(gate2_close_lt[i], true)
-		end
-		SetJointMotorTarget(gate2_doorMain, gate2_doorMain_min, gate2_doorMain_crds)
-		for i=1,#gate2_doorInter do
-			SetJointMotorTarget(gate2_doorInter[i], gate2_doorInter_min, gate2_doorInter_crds)
-		end
-	end
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        gate2_door_stat = GetJointMovement(gate2_doorInter[3])
+        if gate2_openPressed then
+        	for i=1,#gate2_open_lt do
+        		SetLightEnabled(gate2_open_lt[i], true)
+        	end
+        	for i=1,#gate2_close_lt do
+        		SetLightEnabled(gate2_close_lt[i], false)
+        	end
+        	SetJointMotorTarget(gate2_doorMain, gate2_doorMain_max, -gate2_doorMain_ords)
+        	for i=1,#gate2_doorInter do
+        		SetJointMotorTarget(gate2_doorInter[i], gate2_doorInter_max, -gate2_doorInter_ords)
+        	end
+        end
+        if gate2_closePressed then
+        	for i=1,#gate2_open_lt do
+        		SetLightEnabled(gate2_open_lt[i], false)
+        	end
+        	for i=1,#gate2_close_lt do
+        		SetLightEnabled(gate2_close_lt[i], true)
+        	end
+        	SetJointMotorTarget(gate2_doorMain, gate2_doorMain_min, gate2_doorMain_crds)
+        	for i=1,#gate2_doorInter do
+        		SetJointMotorTarget(gate2_doorInter[i], gate2_doorInter_min, gate2_doorInter_crds)
+        	end
+        end
+        if gate2_door_stat > gate2_doorInter_min+2.5 and gate2_door_stat < gate2_doorInter_max-2.5 then
+        	for i=1,#gate2_wrlt do
+        		SetJointMotor(gate2_wrlt[i], gate2_wrlt_spd)
+        	end
+        	for i=1,#gate2_lt do
+        		SetLightEnabled(gate2_lt[i], true)
+        	end
+        else
+        	for i=1,#gate2_wrlt do
+        		SetJointMotor(gate2_wrlt[i], 0)
+        	end
+        	for i=1,#gate2_lt do
+        		SetLightEnabled(gate2_lt[i], false)
+        	end
+        	for i=1,#gate2_open_lt do
+        		SetLightEnabled(gate2_open_lt[i], false)
+        	end
+        	for i=1,#gate2_close_lt do
+        		SetLightEnabled(gate2_close_lt[i], false)
+        	end
+        end
+    end
+end
 
-	if gate2_door_stat > gate2_doorInter_min+2.5 and gate2_door_stat < gate2_doorInter_max-2.5 then
-		for i=1,#gate2_wrlt do
-			SetJointMotor(gate2_wrlt[i], gate2_wrlt_spd)
-		end
-		for i=1,#gate2_lt do
-			SetLightEnabled(gate2_lt[i], true)
-		end
-	else
-		for i=1,#gate2_wrlt do
-			SetJointMotor(gate2_wrlt[i], 0)
-		end
-		for i=1,#gate2_lt do
-			SetLightEnabled(gate2_lt[i], false)
-		end
-		for i=1,#gate2_open_lt do
-			SetLightEnabled(gate2_open_lt[i], false)
-		end
-		for i=1,#gate2_close_lt do
-			SetLightEnabled(gate2_close_lt[i], false)
-		end
-	end
-	
-	--DebugPrint(gate2_door_stat)
-end+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    for i=1,#gate2_open do
+    	if GetPlayerInteractShape(playerId) == gate2_open[i] and InputPressed("interact") then
+    		gate2_openPressed = true
+    		gate2_closePressed = false
+    	end
+    end
+    for i=1,#gate2_close do
+    	if GetPlayerInteractShape(playerId) == gate2_close[i] and InputPressed("interact") then
+    		gate2_closePressed = true
+    		gate2_openPressed = false
+    	end
+    end
+end
+

```

---

# Migration Report: main\scripts\AutoGate2_2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\AutoGate2_2.lua
+++ patched/main\scripts\AutoGate2_2.lua
@@ -1,108 +1,108 @@
-function init()
-	gate2_2_open = FindShapes("gate2_2_open", true)
-	gate2_2_close = FindShapes("gate2_2_close", true)
-	
-	for i=1,#gate2_2_open do
-		SetTag(gate2_2_open[i], "interact", "OPEN")
-	end
-	for i=1,#gate2_2_close do
-		SetTag(gate2_2_close[i], "interact", "CLOSE")
-	end
-	
-	gate2_2_doorMain = FindJoint("gate2_2_door_main",true)
-	gate2_2_doorInter = FindJoints("gate2_2_door_inter",true)
-	gate2_2_doorMain_min, gate2_2_doorMain_max = GetJointLimits(gate2_2_doorMain)
-	gate2_2_doorInter_min, gate2_2_doorInter_max = GetJointLimits(gate2_2_doorInter[3])
-	gate2_2_doorMain_ords = 0.5
-	gate2_2_doorMain_crds = 0.2
-	gate2_2_doorInter_ords = 0.8
-	gate2_2_doorInter_crds = 0.6
-	SetJointMotor(gate2_2_doorMain, 0)
-	for i=1,#gate2_2_doorInter do
-		SetJointMotor(gate2_2_doorInter[i], 0)
-	end
-	
-	
-	gate2_2_wrlt = FindJoints("gate2_2_warning",true)
-	gate2_2_lt = FindLights("gate2_2_wnlt",true)
-	gate2_2_open_lt = FindLights("gate2_2_open_lt",true)
-	gate2_2_close_lt = FindLights("gate2_2_close_lt",true)
-	gate2_2_wrlt_spd = 5
-	for i=1,#gate2_2_wrlt do
-		SetJointMotor(gate2_2_wrlt[i], 0)
-	end
-	for i=1,#gate2_2_lt do
-		SetLightEnabled(gate2_2_lt[i], false)
-	end
-	for i=1,#gate2_2_open_lt do
-		SetLightEnabled(gate2_2_open_lt[i], false)
-	end
-	for i=1,#gate2_2_close_lt do
-		SetLightEnabled(gate2_2_close_lt[i], false)
-	end
+#version 2
+function server.init()
+    gate2_2_open = FindShapes("gate2_2_open", true)
+    gate2_2_close = FindShapes("gate2_2_close", true)
+    for i=1,#gate2_2_open do
+    	SetTag(gate2_2_open[i], "interact", "OPEN")
+    end
+    for i=1,#gate2_2_close do
+    	SetTag(gate2_2_close[i], "interact", "CLOSE")
+    end
+    gate2_2_doorMain = FindJoint("gate2_2_door_main",true)
+    gate2_2_doorInter = FindJoints("gate2_2_door_inter",true)
+    gate2_2_doorMain_min, gate2_2_doorMain_max = GetJointLimits(gate2_2_doorMain)
+    gate2_2_doorInter_min, gate2_2_doorInter_max = GetJointLimits(gate2_2_doorInter[3])
+    gate2_2_doorMain_ords = 0.5
+    gate2_2_doorMain_crds = 0.2
+    gate2_2_doorInter_ords = 0.8
+    gate2_2_doorInter_crds = 0.6
+    SetJointMotor(gate2_2_doorMain, 0)
+    for i=1,#gate2_2_doorInter do
+    	SetJointMotor(gate2_2_doorInter[i], 0)
+    end
+    gate2_2_wrlt = FindJoints("gate2_2_warning",true)
+    gate2_2_lt = FindLights("gate2_2_wnlt",true)
+    gate2_2_open_lt = FindLights("gate2_2_open_lt",true)
+    gate2_2_close_lt = FindLights("gate2_2_close_lt",true)
+    gate2_2_wrlt_spd = 5
+    for i=1,#gate2_2_wrlt do
+    	SetJointMotor(gate2_2_wrlt[i], 0)
+    end
+    for i=1,#gate2_2_lt do
+    	SetLightEnabled(gate2_2_lt[i], false)
+    end
+    for i=1,#gate2_2_open_lt do
+    	SetLightEnabled(gate2_2_open_lt[i], false)
+    end
+    for i=1,#gate2_2_close_lt do
+    	SetLightEnabled(gate2_2_close_lt[i], false)
+    end
 end
 
-function update(dt)
-	gate2_2_door_stat = GetJointMovement(gate2_2_doorInter[3])
-	for i=1,#gate2_2_open do
-		if GetPlayerInteractShape() == gate2_2_open[i] and InputPressed("interact") then
-			gate2_2_openPressed = true
-			gate2_2_closePressed = false
-		end
-	end
-	for i=1,#gate2_2_close do
-		if GetPlayerInteractShape() == gate2_2_close[i] and InputPressed("interact") then
-			gate2_2_closePressed = true
-			gate2_2_openPressed = false
-		end
-	end
-	
-	if gate2_2_openPressed then
-		for i=1,#gate2_2_open_lt do
-			SetLightEnabled(gate2_2_open_lt[i], true)
-		end
-		for i=1,#gate2_2_close_lt do
-			SetLightEnabled(gate2_2_close_lt[i], false)
-		end
-		SetJointMotorTarget(gate2_2_doorMain, gate2_2_doorMain_max, -gate2_2_doorMain_ords)
-		for i=1,#gate2_2_doorInter do
-			SetJointMotorTarget(gate2_2_doorInter[i], gate2_2_doorInter_max, -gate2_2_doorInter_ords)
-		end
-	end
-	if gate2_2_closePressed then
-		for i=1,#gate2_2_open_lt do
-			SetLightEnabled(gate2_2_open_lt[i], false)
-		end
-		for i=1,#gate2_2_close_lt do
-			SetLightEnabled(gate2_2_close_lt[i], true)
-		end
-		SetJointMotorTarget(gate2_2_doorMain, gate2_2_doorMain_min, gate2_2_doorMain_crds)
-		for i=1,#gate2_2_doorInter do
-			SetJointMotorTarget(gate2_2_doorInter[i], gate2_2_doorInter_min, gate2_2_doorInter_crds)
-		end
-	end
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        gate2_2_door_stat = GetJointMovement(gate2_2_doorInter[3])
+        if gate2_2_openPressed then
+        	for i=1,#gate2_2_open_lt do
+        		SetLightEnabled(gate2_2_open_lt[i], true)
+        	end
+        	for i=1,#gate2_2_close_lt do
+        		SetLightEnabled(gate2_2_close_lt[i], false)
+        	end
+        	SetJointMotorTarget(gate2_2_doorMain, gate2_2_doorMain_max, -gate2_2_doorMain_ords)
+        	for i=1,#gate2_2_doorInter do
+        		SetJointMotorTarget(gate2_2_doorInter[i], gate2_2_doorInter_max, -gate2_2_doorInter_ords)
+        	end
+        end
+        if gate2_2_closePressed then
+        	for i=1,#gate2_2_open_lt do
+        		SetLightEnabled(gate2_2_open_lt[i], false)
+        	end
+        	for i=1,#gate2_2_close_lt do
+        		SetLightEnabled(gate2_2_close_lt[i], true)
+        	end
+        	SetJointMotorTarget(gate2_2_doorMain, gate2_2_doorMain_min, gate2_2_doorMain_crds)
+        	for i=1,#gate2_2_doorInter do
+        		SetJointMotorTarget(gate2_2_doorInter[i], gate2_2_doorInter_min, gate2_2_doorInter_crds)
+        	end
+        end
+        if gate2_2_door_stat > gate2_2_doorInter_min+2.5 and gate2_2_door_stat < gate2_2_doorInter_max-2.5 then
+        	for i=1,#gate2_2_wrlt do
+        		SetJointMotor(gate2_2_wrlt[i], gate2_2_wrlt_spd)
+        	end
+        	for i=1,#gate2_2_lt do
+        		SetLightEnabled(gate2_2_lt[i], true)
+        	end
+        else
+        	for i=1,#gate2_2_wrlt do
+        		SetJointMotor(gate2_2_wrlt[i], 0)
+        	end
+        	for i=1,#gate2_2_lt do
+        		SetLightEnabled(gate2_2_lt[i], false)
+        	end
+        	for i=1,#gate2_2_open_lt do
+        		SetLightEnabled(gate2_2_open_lt[i], false)
+        	end
+        	for i=1,#gate2_2_close_lt do
+        		SetLightEnabled(gate2_2_close_lt[i], false)
+        	end
+        end
+    end
+end
 
-	if gate2_2_door_stat > gate2_2_doorInter_min+2.5 and gate2_2_door_stat < gate2_2_doorInter_max-2.5 then
-		for i=1,#gate2_2_wrlt do
-			SetJointMotor(gate2_2_wrlt[i], gate2_2_wrlt_spd)
-		end
-		for i=1,#gate2_2_lt do
-			SetLightEnabled(gate2_2_lt[i], true)
-		end
-	else
-		for i=1,#gate2_2_wrlt do
-			SetJointMotor(gate2_2_wrlt[i], 0)
-		end
-		for i=1,#gate2_2_lt do
-			SetLightEnabled(gate2_2_lt[i], false)
-		end
-		for i=1,#gate2_2_open_lt do
-			SetLightEnabled(gate2_2_open_lt[i], false)
-		end
-		for i=1,#gate2_2_close_lt do
-			SetLightEnabled(gate2_2_close_lt[i], false)
-		end
-	end
-	
-	--DebugPrint(gate2_2_door_stat)
-end+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    for i=1,#gate2_2_open do
+    	if GetPlayerInteractShape(playerId) == gate2_2_open[i] and InputPressed("interact") then
+    		gate2_2_openPressed = true
+    		gate2_2_closePressed = false
+    	end
+    end
+    for i=1,#gate2_2_close do
+    	if GetPlayerInteractShape(playerId) == gate2_2_close[i] and InputPressed("interact") then
+    		gate2_2_closePressed = true
+    		gate2_2_openPressed = false
+    	end
+    end
+end
+

```

---

# Migration Report: main\scripts\AutoGate2_3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\AutoGate2_3.lua
+++ patched/main\scripts\AutoGate2_3.lua
@@ -1,108 +1,108 @@
-function init()
-	gate2_3_open = FindShapes("gate2_3_open", true)
-	gate2_3_close = FindShapes("gate2_3_close", true)
-	
-	for i=1,#gate2_3_open do
-		SetTag(gate2_3_open[i], "interact", "OPEN")
-	end
-	for i=1,#gate2_3_close do
-		SetTag(gate2_3_close[i], "interact", "CLOSE")
-	end
-	
-	gate2_3_doorMain = FindJoint("gate2_3_door_main",true)
-	gate2_3_doorInter = FindJoints("gate2_3_door_inter",true)
-	gate2_3_doorMain_min, gate2_3_doorMain_max = GetJointLimits(gate2_3_doorMain)
-	gate2_3_doorInter_min, gate2_3_doorInter_max = GetJointLimits(gate2_3_doorInter[3])
-	gate2_3_doorMain_ords = 0.5
-	gate2_3_doorMain_crds = 0.2
-	gate2_3_doorInter_ords = 0.8
-	gate2_3_doorInter_crds = 0.6
-	SetJointMotor(gate2_3_doorMain, 0)
-	for i=1,#gate2_3_doorInter do
-		SetJointMotor(gate2_3_doorInter[i], 0)
-	end
-	
-	
-	gate2_3_wrlt = FindJoints("gate2_3_warning",true)
-	gate2_3_lt = FindLights("gate2_3_wnlt",true)
-	gate2_3_open_lt = FindLights("gate2_3_open_lt",true)
-	gate2_3_close_lt = FindLights("gate2_3_close_lt",true)
-	gate2_3_wrlt_spd = 5
-	for i=1,#gate2_3_wrlt do
-		SetJointMotor(gate2_3_wrlt[i], 0)
-	end
-	for i=1,#gate2_3_lt do
-		SetLightEnabled(gate2_3_lt[i], false)
-	end
-	for i=1,#gate2_3_open_lt do
-		SetLightEnabled(gate2_3_open_lt[i], false)
-	end
-	for i=1,#gate2_3_close_lt do
-		SetLightEnabled(gate2_3_close_lt[i], false)
-	end
+#version 2
+function server.init()
+    gate2_3_open = FindShapes("gate2_3_open", true)
+    gate2_3_close = FindShapes("gate2_3_close", true)
+    for i=1,#gate2_3_open do
+    	SetTag(gate2_3_open[i], "interact", "OPEN")
+    end
+    for i=1,#gate2_3_close do
+    	SetTag(gate2_3_close[i], "interact", "CLOSE")
+    end
+    gate2_3_doorMain = FindJoint("gate2_3_door_main",true)
+    gate2_3_doorInter = FindJoints("gate2_3_door_inter",true)
+    gate2_3_doorMain_min, gate2_3_doorMain_max = GetJointLimits(gate2_3_doorMain)
+    gate2_3_doorInter_min, gate2_3_doorInter_max = GetJointLimits(gate2_3_doorInter[3])
+    gate2_3_doorMain_ords = 0.5
+    gate2_3_doorMain_crds = 0.2
+    gate2_3_doorInter_ords = 0.8
+    gate2_3_doorInter_crds = 0.6
+    SetJointMotor(gate2_3_doorMain, 0)
+    for i=1,#gate2_3_doorInter do
+    	SetJointMotor(gate2_3_doorInter[i], 0)
+    end
+    gate2_3_wrlt = FindJoints("gate2_3_warning",true)
+    gate2_3_lt = FindLights("gate2_3_wnlt",true)
+    gate2_3_open_lt = FindLights("gate2_3_open_lt",true)
+    gate2_3_close_lt = FindLights("gate2_3_close_lt",true)
+    gate2_3_wrlt_spd = 5
+    for i=1,#gate2_3_wrlt do
+    	SetJointMotor(gate2_3_wrlt[i], 0)
+    end
+    for i=1,#gate2_3_lt do
+    	SetLightEnabled(gate2_3_lt[i], false)
+    end
+    for i=1,#gate2_3_open_lt do
+    	SetLightEnabled(gate2_3_open_lt[i], false)
+    end
+    for i=1,#gate2_3_close_lt do
+    	SetLightEnabled(gate2_3_close_lt[i], false)
+    end
 end
 
-function update(dt)
-	gate2_3_door_stat = GetJointMovement(gate2_3_doorInter[3])
-	for i=1,#gate2_3_open do
-		if GetPlayerInteractShape() == gate2_3_open[i] and InputPressed("interact") then
-			gate2_3_openPressed = true
-			gate2_3_closePressed = false
-		end
-	end
-	for i=1,#gate2_3_close do
-		if GetPlayerInteractShape() == gate2_3_close[i] and InputPressed("interact") then
-			gate2_3_closePressed = true
-			gate2_3_openPressed = false
-		end
-	end
-	
-	if gate2_3_openPressed then
-		for i=1,#gate2_3_open_lt do
-			SetLightEnabled(gate2_3_open_lt[i], true)
-		end
-		for i=1,#gate2_3_close_lt do
-			SetLightEnabled(gate2_3_close_lt[i], false)
-		end
-		SetJointMotorTarget(gate2_3_doorMain, gate2_3_doorMain_max, -gate2_3_doorMain_ords)
-		for i=1,#gate2_3_doorInter do
-			SetJointMotorTarget(gate2_3_doorInter[i], gate2_3_doorInter_max, -gate2_3_doorInter_ords)
-		end
-	end
-	if gate2_3_closePressed then
-		for i=1,#gate2_3_open_lt do
-			SetLightEnabled(gate2_3_open_lt[i], false)
-		end
-		for i=1,#gate2_3_close_lt do
-			SetLightEnabled(gate2_3_close_lt[i], true)
-		end
-		SetJointMotorTarget(gate2_3_doorMain, gate2_3_doorMain_min, gate2_3_doorMain_crds)
-		for i=1,#gate2_3_doorInter do
-			SetJointMotorTarget(gate2_3_doorInter[i], gate2_3_doorInter_min, gate2_3_doorInter_crds)
-		end
-	end
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        gate2_3_door_stat = GetJointMovement(gate2_3_doorInter[3])
+        if gate2_3_openPressed then
+        	for i=1,#gate2_3_open_lt do
+        		SetLightEnabled(gate2_3_open_lt[i], true)
+        	end
+        	for i=1,#gate2_3_close_lt do
+        		SetLightEnabled(gate2_3_close_lt[i], false)
+        	end
+        	SetJointMotorTarget(gate2_3_doorMain, gate2_3_doorMain_max, -gate2_3_doorMain_ords)
+        	for i=1,#gate2_3_doorInter do
+        		SetJointMotorTarget(gate2_3_doorInter[i], gate2_3_doorInter_max, -gate2_3_doorInter_ords)
+        	end
+        end
+        if gate2_3_closePressed then
+        	for i=1,#gate2_3_open_lt do
+        		SetLightEnabled(gate2_3_open_lt[i], false)
+        	end
+        	for i=1,#gate2_3_close_lt do
+        		SetLightEnabled(gate2_3_close_lt[i], true)
+        	end
+        	SetJointMotorTarget(gate2_3_doorMain, gate2_3_doorMain_min, gate2_3_doorMain_crds)
+        	for i=1,#gate2_3_doorInter do
+        		SetJointMotorTarget(gate2_3_doorInter[i], gate2_3_doorInter_min, gate2_3_doorInter_crds)
+        	end
+        end
+        if gate2_3_door_stat > gate2_3_doorInter_min+2.5 and gate2_3_door_stat < gate2_3_doorInter_max-2.5 then
+        	for i=1,#gate2_3_wrlt do
+        		SetJointMotor(gate2_3_wrlt[i], gate2_3_wrlt_spd)
+        	end
+        	for i=1,#gate2_3_lt do
+        		SetLightEnabled(gate2_3_lt[i], true)
+        	end
+        else
+        	for i=1,#gate2_3_wrlt do
+        		SetJointMotor(gate2_3_wrlt[i], 0)
+        	end
+        	for i=1,#gate2_3_lt do
+        		SetLightEnabled(gate2_3_lt[i], false)
+        	end
+        	for i=1,#gate2_3_open_lt do
+        		SetLightEnabled(gate2_3_open_lt[i], false)
+        	end
+        	for i=1,#gate2_3_close_lt do
+        		SetLightEnabled(gate2_3_close_lt[i], false)
+        	end
+        end
+    end
+end
 
-	if gate2_3_door_stat > gate2_3_doorInter_min+2.5 and gate2_3_door_stat < gate2_3_doorInter_max-2.5 then
-		for i=1,#gate2_3_wrlt do
-			SetJointMotor(gate2_3_wrlt[i], gate2_3_wrlt_spd)
-		end
-		for i=1,#gate2_3_lt do
-			SetLightEnabled(gate2_3_lt[i], true)
-		end
-	else
-		for i=1,#gate2_3_wrlt do
-			SetJointMotor(gate2_3_wrlt[i], 0)
-		end
-		for i=1,#gate2_3_lt do
-			SetLightEnabled(gate2_3_lt[i], false)
-		end
-		for i=1,#gate2_3_open_lt do
-			SetLightEnabled(gate2_3_open_lt[i], false)
-		end
-		for i=1,#gate2_3_close_lt do
-			SetLightEnabled(gate2_3_close_lt[i], false)
-		end
-	end
-	
-	--DebugPrint(gate2_3_door_stat)
-end+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    for i=1,#gate2_3_open do
+    	if GetPlayerInteractShape(playerId) == gate2_3_open[i] and InputPressed("interact") then
+    		gate2_3_openPressed = true
+    		gate2_3_closePressed = false
+    	end
+    end
+    for i=1,#gate2_3_close do
+    	if GetPlayerInteractShape(playerId) == gate2_3_close[i] and InputPressed("interact") then
+    		gate2_3_closePressed = true
+    		gate2_3_openPressed = false
+    	end
+    end
+end
+

```

---

# Migration Report: main\scripts\elevator.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\elevator.lua
+++ patched/main\scripts\elevator.lua
@@ -1,65 +1,4 @@
---PARAM PARADIGM
---aaaa_bbbb	:	tags in the map
---aaaa_Bbbb	:	local medium param in functions (usually returned outcomes)
---aaaaBbbb	:	working params
-
-STOP_THRESHOLD = 0.1  -- Meters. When cabin is +/- this distance it will be considered to have stopped.
-DOOR_SPEED = 2         -- Meters/second. How fast to open/close the doors
-MOTOR_SPEED = 2        -- Meters/second. How fast to move the cabin
-DOOR_STRENGTH = 400    -- Strength parameter when setting door joint motor.
-DOOR_THRESHOLD = 0.01  -- Meters. When door position is less than this it will be considered closed.
-
--- Door commands
-OPEN  = 1
-CLOSE = 2
-
----------------------------------------
--- 									 --
--- 			Initialization			 --
--- 									 --
----------------------------------------
-function init()
-	elevatorId = GetStringParam("id", "NO_ID_SET")
-	basementCount = GetStringParam("basement_count", "NO_BASEMENT_SET")
-	
-	cabinDoors, floorDoors = findDoors()
-	floorPositions = findFloors()
-	floorButtons = findFloorButtons()
-	cabinButtons = findCabinButtons()
-	
-	doorsInitialize()
-	
-	cabin = GetShapeBody(FindShape("cabin"))
-	
-	cabinMotor = FindJoint("cabin_motor")
-	
-	motorInitialize()
-	
-	cabinMotorSound = LoadLoop("MOD/main/sounds/elevator_motor.ogg")
-	chimeSound = LoadSound("elevator-chime.ogg")
-	
-	INITIAL_FLOOR = 1
-	setCurrentFloor(basementCount + INITIAL_FLOOR)
-	setTargetFloor(basementCount + INITIAL_FLOOR)
-	
-	ARRIVED = true
-	DOOR_CLOSED = false
-	
-	TIMER = 10
-	
-	SetInt("level.elevator" .. elevatorId .. ".displayDirection", 3)	--1 for up, 2 for down, 3 for idle. ONLY FOR FLOOR DISPLAY USE. NOT REAL DIRECTION
-	
-	setFloorDisplays()	--record the attached floor display handles for script communication
-end
-
-
-
----------------------------------------
--- 									 --
---	Position Retrieving Functions	 --
--- 									 --
----------------------------------------
---table sorting rule
+#version 2
 function sortShapeByWorldPos(a, b)
 	return GetShapeWorldTransform(a).pos[2] < GetShapeWorldTransform(b).pos[2]
 end
@@ -72,9 +11,6 @@
 	return a.num < b.num
 end
 
-
-
--- Returns an array of buttons, sorted from lowest to highest
 function findFloorButtons()
 	local floor_Buttons = FindShapes("floor_button")
 	table.sort(floor_Buttons, sortShapeByWorldPos)
@@ -90,7 +26,6 @@
 	return floor_Buttons
 end
 
--- Returns an array of buttons, sorted from lowest to highest; also sets button tags after their corresponding floor number by rows starting from bottom left of the control panel
 function findCabinButtons()
 	local cabin_buttons_crude = FindShapes("cabin_button")
 	table.sort(cabin_buttons_crude, sortShapeByLocalPos)
@@ -126,9 +61,6 @@
 	return cabin_Buttons	--i.e. cabin_Buttons(sequential) ==> {button_handle, ...}
 end
 
-
-
--- Returns an array of vertical positions of each floor, sorted from lowest to highest
 function findFloors()
 	local floor_locations = FindLocations("floor")
 	local floor_Positions = {}
@@ -139,9 +71,6 @@
 	return floor_Positions
 end
 
-
-
--- Returns an array of tables representing the left and right doors for each floor
 function findDoors()
 	local floor_Doors = FindShapes("floor_door")
 	table.sort(floor_Doors, sortShapeByWorldPos)
@@ -174,21 +103,17 @@
 	--i.e.	floor_DoorsArray(sequential) ==> {{'left': door_handle; 'right' : door_handle}; {...}}
 end
 
-
--- Find position of cabin bottom
 function getCabinBottomPos()
 	local min, max = GetBodyBounds(cabin)
 	return min[2]
 end
 
-
--- Find floor closest to current cabin position
 function findClosestFloor()	--only used to display floor number
 	local i = 1
 	while i < #floorPositions and getCabinBottomPos() > (floorPositions[i] + floorPositions[i + 1]) / 2 do
 		i = i + 1
 	end
-	SetInt("level.elevator" .. elevatorId .. ".closestFloor", i)
+	SetInt("level.elevator" .. elevatorId .. ".closestFloor", i, true)
 	return i  -- Floor numbers are 1-based (ground is 1)
 end
 
@@ -201,12 +126,6 @@
 	return false
 end
 
----------------------------------------
--- 									 --
---			Dynamic Operation	 	 --
--- 									 --
----------------------------------------
---Basic
 function moveShape(shape_handle, direction)
 	local shape_motor = GetShapeJoints(shape_handle)[1]	--this "[1]" assumes that each shape, say a door, has only 1 joint
 	local min, max = GetJointLimits(shape_motor)
@@ -217,7 +136,6 @@
 	end
 end
 
---Operational
 function openDoors(targetFloor)
 	moveShape(floorDoors[targetFloor].left, OPEN)
 	moveShape(floorDoors[targetFloor].right, OPEN)
@@ -258,7 +176,6 @@
 	PlayLoop(cabinMotorSound, GetBodyTransform(cabin).pos, 0.3)
 end
 
-
 function controlButtonsLightInitialize()
 	for i=1, #floorButtons do
 		buttonLightOff(floorButtons[i])
@@ -273,18 +190,12 @@
 	buttonLightOn(cabinButtons[targetFloor])
 end
 
----------------------------------------
--- 									 --
---		Status Configuration		 --
--- 									 --
----------------------------------------
--- Floor info basic
 function setCurrentFloor(num)
-	SetInt("level.elevator" .. elevatorId .. ".currentFloor", num)
+	SetInt("level.elevator" .. elevatorId .. ".currentFloor", num, true)
 end
 
 function setTargetFloor(num)
-	SetInt("level.elevator" .. elevatorId .. ".targetFloor", num)
+	SetInt("level.elevator" .. elevatorId .. ".targetFloor", num, true)
 end
 
 function setDisplayFloor()
@@ -293,7 +204,7 @@
 		floor_num = floor_num - 1
 	end
 	local display_floor = floor_num
-	SetInt("level.elevator" .. elevatorId .. ".displayFloor", display_floor)
+	SetInt("level.elevator" .. elevatorId .. ".displayFloor", display_floor, true)
 end
 
 function setDisplayDirection()
@@ -306,18 +217,16 @@
 	else
 		DIRECTION = 3	--3 for idle
 	end
-	SetInt("level.elevator" .. elevatorId .. ".displayDirection", DIRECTION)
+	SetInt("level.elevator" .. elevatorId .. ".displayDirection", DIRECTION, true)
 end
 
 function setFloorDisplays()
 	local floorDisplays = FindScreens("floor_display")
 	for i=1, #floorDisplays do
-		SetInt("level.elevator_displays." .. floorDisplays[i], elevatorId)	--i.e. level.elevator_displays.screen_handle ==> 1
-	end
-end
-
-
--- Floor info operational
+		SetInt("level.elevator_displays." .. floorDisplays[i], elevatorId, true)	--i.e. level.elevator_displays.screen_handle ==> 1
+	end
+end
+
 function getCurrentFloor()
 	local currentCabinPos = getCabinBottomPos()
 	for i=1, #floorPositions do
@@ -330,7 +239,7 @@
 
 function getTargetFloor()
 	if InputPressed("interact") then
-		local targetHandle = GetPlayerInteractShape()
+		local targetHandle = GetPlayerInteractShape(playerId)
 		--floor buttons scan
 		for i=1, #floorButtons do
 			if targetHandle == floorButtons[i] then
@@ -361,7 +270,6 @@
 	return ARRIVED
 end
 
--- Button light status basic
 function buttonLightOn(button_handle)
 	SetShapeEmissiveScale(button_handle, 1)
 end
@@ -370,54 +278,76 @@
 	SetShapeEmissiveScale(button_handle, 0)
 end
 
-
--- Sound effect
 function playChimeSound()
 	PlaySound(chimeSound, GetBodyTransform(cabin).pos)
 end
 
----------------------------------------
--- 									 --
---				Main Loop			 --
--- 									 --
----------------------------------------
-function tick(dt)
-	local currentFloor = getCurrentFloor()
-	local targetFloor = getTargetFloor()
-	
-	setDisplayFloor()
-	setDisplayDirection()
-	
-	TIMER = TIMER + dt
-	if currentFloor ~= targetFloor then
-		controlButtonsLightOn(targetFloor)
-		closeDoors(currentFloor)
-		if DOOR_CLOSED then
-			goToFloor(targetFloor)
-		end
-	end
-	
-	if hasArrived(targetFloor) then
-		controlButtonsLightInitialize()
-		openDoors(targetFloor)
-		if TIMER >= 0.01 and TIMER <= 0.02 then
-			playChimeSound()
-		end
-		if TIMER >= 5 then
-			closeDoors(currentFloor)
-		end
-	else
-		TIMER = 0
-	end
-	
-	if InputPressed("interact") then
-		local pressed_handle = GetPlayerInteractShape()
-		if isInArray(floorButtons, pressed_handle) or isInArray(cabinButtons, pressed_handle) then
-			controlButtonsLightInitialize()
-			if currentFloor == targetFloor then
-				openDoors(currentFloor)
-				TIMER = 0
-			end
-		end
-	end
-end+function server.init()
+    elevatorId = GetStringParam("id", "NO_ID_SET")
+    basementCount = GetStringParam("basement_count", "NO_BASEMENT_SET")
+    cabinDoors, floorDoors = findDoors()
+    floorPositions = findFloors()
+    floorButtons = findFloorButtons()
+    cabinButtons = findCabinButtons()
+    doorsInitialize()
+    cabin = GetShapeBody(FindShape("cabin"))
+    cabinMotor = FindJoint("cabin_motor")
+    motorInitialize()
+    cabinMotorSound = LoadLoop("MOD/main/sounds/elevator_motor.ogg")
+    INITIAL_FLOOR = 1
+    setCurrentFloor(basementCount + INITIAL_FLOOR)
+    setTargetFloor(basementCount + INITIAL_FLOOR)
+    ARRIVED = true
+    DOOR_CLOSED = false
+    TIMER = 10
+    SetInt("level.elevator" .. elevatorId .. ".displayDirection", 3, true)	--1 for up, 2 for down, 3 for idle. ONLY FOR FLOOR DISPLAY USE. NOT REAL DIRECTION
+    setFloorDisplays()	--record the attached floor display handles for script communication
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local currentFloor = getCurrentFloor()
+        local targetFloor = getTargetFloor()
+        setDisplayFloor()
+        setDisplayDirection()
+        TIMER = TIMER + dt
+        if currentFloor ~= targetFloor then
+        	controlButtonsLightOn(targetFloor)
+        	closeDoors(currentFloor)
+        	if DOOR_CLOSED then
+        		goToFloor(targetFloor)
+        	end
+        end
+        if hasArrived(targetFloor) then
+        	controlButtonsLightInitialize()
+        	openDoors(targetFloor)
+        	if TIMER >= 0.01 and TIMER <= 0.02 then
+        		playChimeSound()
+        	end
+        	if TIMER >= 5 then
+        		closeDoors(currentFloor)
+        	end
+        else
+        	TIMER = 0
+        end
+    end
+end
+
+function client.init()
+    chimeSound = LoadSound("elevator-chime.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("interact") then
+    	local pressed_handle = GetPlayerInteractShape(playerId)
+    	if isInArray(floorButtons, pressed_handle) or isInArray(cabinButtons, pressed_handle) then
+    		controlButtonsLightInitialize()
+    		if currentFloor == targetFloor then
+    			openDoors(currentFloor)
+    			TIMER = 0
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: math.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/math.lua
+++ patched/math.lua
@@ -1,8 +1,9 @@
-
+#version 2
 function dist(a, b)
 	return VecLength(VecSub(a,b))
 end
 
 function clamp(n, low, high)
     return math.min(math.max(n, low), high)
-end+end
+

```

---

# Migration Report: menu\menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/menu\menu.lua
+++ patched/menu\menu.lua
@@ -1,43 +1,13 @@
--- MAIN MENU
--- Description: Main Menu for A Business Center
---
--- ORGINALLY WRITTEN BY CENNYCOAST (ELI)
--- @elir on discord - https://steamcommunity.com/id/EliRickard/ on steam.
--- VALIDATED BY JOAN -- PROD READY
--- FEEL FREE TO USE... BUT PLEASE KEEP THE CREDIT HEADER
-
-
--- IF YOU USE THIS SCRIPT: REMOVE LINES 228-246
-
-
-#include "version-data.lua" -- THIS CONTAINS YOUR LEVEL INFO
-
-debugMode = false -- DEBUG MODE SHOWS YOUR CURRENT OUTPUT LAYER STRING AND MOTION PROPERTIES
-
--- LEVEL XML
+#version 2
 local levelXML = "MOD/level.xml"
-
--- LOGO
 local levelLogo = "MOD/menu/logo.png"
 local levelLogo2 = "MOD/menu/logo2.png"
-
---LAUNCH LAYER STRING
 local launchLayerString = ""
-
---AUTO SELECT FPS MODE -- THIS IS DEPRECATED (GET LOGIC IS STILL IN PLACE, USE LOGIC HAS BEEN REMOVED)
 local useAutomaticSelection = false
 local resolutionFrame = 0
 local gfxFrame = 0
-
--- PROVIDE INIT VALUE FOR THE LAUNCH LAYER STRING
 local launchLayerInit = "building"
-
--- GENERAL LAYER NAMES
-
-
 local timeElapsed = 0
-
--- SPECIFIC FPS LAYERS
 local additionalLayers = {
    ["AIPatrolCar"] = false,
    ["AIRagdollsYard"] = false,
@@ -46,7 +16,6 @@
    ["nolights"] = false,
 
 }
-
 local additionalNames = {
    ["AIPatrolCar"] = "*AI Patrol Car",
    ["AIRagdollsYard"] = "*AI Prisoners Yard",
@@ -57,71 +26,43 @@
    
 
 }
-
---BUTTONS AND FONTS
 local fontBoldItalic = "MOD/common/fonts/Montserrat-BoldItalic.ttf"
 local fontBold = "MOD/common/fonts/Montserrat-Bold.ttf"
 local fontBlack = "MOD/common/fonts/Montserrat-Black.ttf"
 local fontNormal = "MOD/common/fonts/Montserrat-SemiBold.ttf"
-
 local onLight = "MOD/common/on.png"
 local offLight = "MOD/common/off.png"
-
-local buttonInfo1 = "MOD/common/button-norm.png" 
-local buttonInfo2 = "MOD/common/norm-status.png" 
-local buttonDanger = "MOD/common/button-red.png" 
-local buttonOption = "MOD/common/black-button.png" 
+local buttonInfo1 = "MOD/common/button-norm.png"
+local buttonInfo2 = "MOD/common/norm-status.png"
+local buttonDanger = "MOD/common/button-red.png"
+local buttonOption = "MOD/common/black-button.png"
 local buttonRounded = "MOD/common/box-solid-6.png"
 local buttonPopOver = "MOD/common/pop.png"
-
--- 3D BG
-local backgroundImagePath1 = "MOD/menu/sunny.png" -- THIS IS BEHIND EVERYTHING
-
-
--- MUSIC AND SOUND [THE CURRENT TRACK IS A LICENSED TRACK -- YOU CANNOT USE IT IN YOUR OWN MODS]
+local backgroundImagePath1 = "MOD/menu/sunny.png"
 local musicPath = "MOD/sounds/licensed-tracks/WB_THE_COVER_UP.ogg"
 local musicTrackName = "The Cover-Up"
 local musicTrackArtist = "White Bones - Mambo Light"
 local musicTrackArt = "MOD/menu/record.png"
-local musicDelay = 0 -- USED IF THERE IS A SPLASH SCREEN
-
+local musicDelay = 0
 local selectPath = "MOD/sounds/select.ogg"
-
--- OVERRIDE LAYER STRING
-
-local sandboxStarterString = " sandbox" -- ADD STARTER STRING FOR SANDBOX
-
--- MOTION DATA [DON'T CHANGE]
-local motionSpeed = 6.25 
-
-
+local sandboxStarterString = " sandbox"
+local motionSpeed = 6.25
 local recordRotate = 0
-
 local motionType_1 = false
 local motionType_2 = false
 local motionMoving_1 = false
 local motionMoving_2 = false
-
 local motionCurrent_1 = 0
 local motionCurrent_2 = -1200
 local motionTarget_1 = 0
 local motionTarget_2 = 0
-
 local cos1 = ">"
 local cos2 = "show"
 
-function init()
-   snd = LoadSound(selectPath)
-   resolutionFrame = GetDisplayResolution(GetInt("options.display.mode"), GetInt("options.display.resolution"))
-   gfxFrame = GetInt("options.gfx.quality")
-end
-
-
 function setLayerChanges() 
    local launchLayerSetting = launchLayerInit
 
  
-
 
    for key, value in pairs(additionalLayers) do
 
@@ -130,14 +71,9 @@
       end
    end
 
-
    
    return launchLayerSetting
-end 
-
-
-
-
+end
 
 function motion(motionTarget,motionCurrent,motionType)
       if motionType == true then 
@@ -162,266 +98,246 @@
 	return math.floor(num * mult + 0.5) / mult
   end
 
-function tick(dt)
-   timeElapsed = timeElapsed + dt
-   
-   local fps = round(1 / dt, NUM_DECIMAL_FIGURES)
-   local fpsn = 1 / fps 
-   
-   if fps > 60 then
-      fps=60
-   end
-      motionSpeed = fps / 2
-
-   if motionMoving_1 == true then
-      if motionCurrent_1 == motionTarget_1 then
-         motionMoving_1 = false
-      else
-         motionCurrent_1 = motion(motionTarget_1,motionCurrent_1,motionType_1)
-      end
-   end
-
-   if motionMoving_2 == true then
-      if motionCurrent_2 == motionTarget_2 then
-         motionMoving_2 = false
-      else
-         motionCurrent_2 = motion(motionTarget_2,motionCurrent_2,motionType_2)
-      end
-   end
-
-   launchLayerString = setLayerChanges()
-
-   if debugMode then
-   DebugWatch("motion1-Current", motionCurrent_1)
-   DebugWatch("motion1-target", motionTarget_1)
-   DebugWatch("motion1-moving", motionMoving_1)
-   DebugWatch("motion1-type(open)", motionType_1)
-
-   DebugWatch("motion2-Current", motionCurrent_2)
-   DebugWatch("motion2-target", motionTarget_2)
-   DebugWatch("motion2-moving", motionMoving_2)
-   DebugWatch("motion2-type(open)", motionType_2)
-
-   DebugWatch("current-gfx", gfxFrame)
-   DebugWatch("current-res", resolutionFrame)
-   DebugWatch("blank", "blank")
-   DebugWatch("fps", fps)
-   DebugWatch("fpsn", fpsn)
-
-   DebugWatch("LaunchString",launchLayerString)
-   end
-
-   if recordRotate < 360 then
-   recordRotate = recordRotate + 0.5
-   else  
-      recordRotate = 0
-   end
-   
-end
-
-
-function draw()
-   if timeElapsed > musicDelay then
-   UiMakeInteractive()
-   SetBool('hud.aimdot', true)
-  
-   else
-   SetBool('hud.aimdot', false)
-   end
-   -- BG IMAGE AND INITIALIZATION
-   UiAlign("center middle")
-   UiFont(fontNormal, 26)
-   UiButtonImageBox(buttonInfo1, 29, 8)
-   UiButtonHoverColor(0.502, 0.529, 0.541)
-
-   UiPush()
-      local scale = (UiWidth()-0)/3200
-      UiTranslate(UiWidth()/2,UiHeight()/2)
-      UiAlign("center middle")
-      UiScale(scale)
-
-
-      UiImage(backgroundImagePath1,UiWidth())
-
-      if motionType_2 and not motionMoving_2 then
-
-
-         -------------------------------------------------------------------- REMOVE THIS SECTION IF YOU USE THIS SCRIPT ↓↓↓↓↓↓
-
-         -------------------------------------------------------------------- REMOVE THIS SECTION IF YOU USE THIS SCRIPT ↑↑↑↑↑↑
-
-      end
-
-   UiPop()
-
-
-   -- DRAW DETAIL CONTROLS
-   UiPush()
-      UiAlign("left top")
-      UiTranslate(motionCurrent_2,UiHeight()-390)
-      UiFont(fontBlack, 30)
-      UiColor(0.792, 0.859, 0.890)
-      UiColorFilter(1, 1, 1, 1)
-      UiText(" ")
-
-      UiPush()
-         UiAlign("center top")
-         UiButtonImageBox(buttonOption, 29, 8)
-         UiAlign("left top")
-         UiTranslate(0,40)
-         UiPush()  
-
-         for key, value in pairs(additionalLayers) do
-            -- CUSTOM ITEM START
-            UiPush()
-               UiAlign("left middle")
-               UiFont(fontNormal, 26)
-               UiText(additionalNames[key])
-               UiTranslate(0,40)
-
-               if additionalLayers[key] then
-                  if UiTextButton("Enabled", 200, 55) then
-                     PlaySound(snd)
-                     additionalLayers[key] = not additionalLayers[key] 
-                  end
-                  UiTranslate(20,0)
-                  UiImageBox(onLight, 20, 20, 0, 0)
-                  UiTranslate(-20,0)
-               else 
-                  if UiTextButton("Disabled", 200, 55) then
-                     PlaySound(snd)
-                     additionalLayers[key] = not additionalLayers[key] 
-                  end
-                  UiTranslate(20,0)
-                  UiImageBox(offLight, 20, 20, 0, 0)
-                  UiTranslate(-20,0)
-               end
-
-            UiPop()
-            -- CUSTOM ITEM END
-            UiTranslate(220, 0)
-         end
-            
-         UiPop()
-      
-      UiPop()
-   UiPop()
-
-
-   UiPush()
-   UiTranslate(0,0)
-   UiAlign("left top")
-   UiColor(0,0,0,0.75)
-   UiRect(270, UiHeight())
-   UiPop()
-
-   -- MENU OVERLAY 1
-   UiPush()
-      UiTranslate(UiWidth()/2,UiHeight()/2)
-      UiAlign("center middle")
-      UiScale(scale)
-
-
-     
-
-   UiPop()
-
-
-   -- DRAW CONTROL BUTTONS
-
-   UiPush()
-   UiTranslate(0, 50)
-   UiAlign("left middle")
-   UiTranslate(50, 100)
-   UiImageBox(levelLogo2, 170, 170, 0, 0)
-   UiTranslate(-50, 100)
-   UiImageBox(levelLogo, 270, 130, 0, 0)
-   UiAlign("center middle")
-   UiTranslate(135, 90)
-
-
-
-   UiPush()
-   UiColor(0.753, 0.784, 0.800)
-   UiFont(fontBlack, 30)
-   -- TITLE START
-   UiTranslate(-100,0)
-   UiAlign("left middle")
-   UiText("")
-   UiAlign("center middle")
-   UiTranslate(100,0)
-   -- TITLE END
-   UiColor(1, 1, 1)
-   UiPop()
-
-   UiTranslate(0, 150)
-   if UiTextButton("Sandbox", 200, 55) then
-      PlaySound(snd)
-      StartLevel("Sandbox", levelXML,launchLayerString .. sandboxStarterString)
-   end
- 
-
-
-   UiTranslate(0, 85)
-   UiButtonImageBox(buttonDanger, 29, 8)
-   if UiTextButton("Exit", 200, 55) then
-      PlaySound(snd)
-      Menu()
-   end
-
-   
-
-   -- DRAW FPS STATE CHANGER
-
-   UiTranslate(0, 80)
-   UiPush()
-   UiColor(0.753, 0.784, 0.800)
-   UiFont(fontBlack, 30)
-   -- TITLE START
-   
-   -- TITLE END
-   UiColor(1, 1, 1)
-   UiPop()
-   UiTranslate(0, 50)
-   
-
-   -- DRAW QUICK CREDIT
-   UiTranslate(0, 70)
-
-   
-   UiText("FPS OPTIONS")
-   UiTranslate(135+15,0)
-   UiFont(fontBold, 40)
-   UiButtonImageBox(buttonPopOver, 0, 0)
-   if motionType_2 == false then
-       cos1 = ">"
-   else
-       cos1 = "<"
-   end
-   if UiTextButton(cos1, 30, 55) then
-      PlaySound(snd)
-      if motionType_2 == false then
-         motionType_2 = true
-         motionTarget_2 = 320
-         motionCurrent_2 = -1200
-         motionMoving_2 = true
-      else
-         motionType_2 = false
-         motionTarget_2 = -1200
-         motionCurrent_2 = 320
-         motionMoving_2 = true
-      end
-   end
-   UiPop()
-
-   
-   UiTranslate(40, 830)
-   UiAlign("left middle")
-   UiText("* = CPU Intensive")
-   
-
-   
-
-
-end
-
+function server.init()
+    resolutionFrame = GetDisplayResolution(GetInt("options.display.mode"), GetInt("options.display.resolution"))
+    gfxFrame = GetInt("options.gfx.quality")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        timeElapsed = timeElapsed + dt
+        local fps = round(1 / dt, NUM_DECIMAL_FIGURES)
+        local fpsn = 1 / fps 
+        if fps > 60 then
+           fps=60
+        end
+           motionSpeed = fps / 2
+        if motionMoving_1 == true then
+           if motionCurrent_1 == motionTarget_1 then
+              motionMoving_1 = false
+           else
+              motionCurrent_1 = motion(motionTarget_1,motionCurrent_1,motionType_1)
+           end
+        end
+        if motionMoving_2 == true then
+           if motionCurrent_2 == motionTarget_2 then
+              motionMoving_2 = false
+           else
+              motionCurrent_2 = motion(motionTarget_2,motionCurrent_2,motionType_2)
+           end
+        end
+        launchLayerString = setLayerChanges()
+        if debugMode then
+        DebugWatch("motion1-Current", motionCurrent_1)
+        DebugWatch("motion1-target", motionTarget_1)
+        DebugWatch("motion1-moving", motionMoving_1)
+        DebugWatch("motion1-type(open)", motionType_1)
+
+        DebugWatch("motion2-Current", motionCurrent_2)
+        DebugWatch("motion2-target", motionTarget_2)
+        DebugWatch("motion2-moving", motionMoving_2)
+        DebugWatch("motion2-type(open)", motionType_2)
+
+        DebugWatch("current-gfx", gfxFrame)
+        DebugWatch("current-res", resolutionFrame)
+        DebugWatch("blank", "blank")
+        DebugWatch("fps", fps)
+        DebugWatch("fpsn", fpsn)
+
+        DebugWatch("LaunchString",launchLayerString)
+        end
+        if recordRotate < 360 then
+        recordRotate = recordRotate + 0.5
+        else  
+           recordRotate = 0
+        end
+    end
+end
+
+function client.init()
+    snd = LoadSound(selectPath)
+end
+
+function client.draw()
+    if timeElapsed > musicDelay then
+    UiMakeInteractive()
+    SetBool('hud.aimdot', true, true)
+
+    else
+    SetBool('hud.aimdot', false, true)
+    end
+    -- BG IMAGE AND INITIALIZATION
+    UiAlign("center middle")
+    UiFont(fontNormal, 26)
+    UiButtonImageBox(buttonInfo1, 29, 8)
+    UiButtonHoverColor(0.502, 0.529, 0.541)
+
+    UiPush()
+       local scale = (UiWidth()-0)/3200
+       UiTranslate(UiWidth()/2,UiHeight()/2)
+       UiAlign("center middle")
+       UiScale(scale)
+
+       UiImage(backgroundImagePath1,UiWidth())
+
+       if motionType_2 and not motionMoving_2 then
+
+          -------------------------------------------------------------------- REMOVE THIS SECTION IF YOU USE THIS SCRIPT ↓↓↓↓↓↓
+
+          -------------------------------------------------------------------- REMOVE THIS SECTION IF YOU USE THIS SCRIPT ↑↑↑↑↑↑
+
+       end
+
+    UiPop()
+
+    -- DRAW DETAIL CONTROLS
+    UiPush()
+       UiAlign("left top")
+       UiTranslate(motionCurrent_2,UiHeight()-390)
+       UiFont(fontBlack, 30)
+       UiColor(0.792, 0.859, 0.890)
+       UiColorFilter(1, 1, 1, 1)
+       UiText(" ")
+
+       UiPush()
+          UiAlign("center top")
+          UiButtonImageBox(buttonOption, 29, 8)
+          UiAlign("left top")
+          UiTranslate(0,40)
+          UiPush()  
+
+          for key, value in pairs(additionalLayers) do
+             -- CUSTOM ITEM START
+             UiPush()
+                UiAlign("left middle")
+                UiFont(fontNormal, 26)
+                UiText(additionalNames[key])
+                UiTranslate(0,40)
+
+                if additionalLayers[key] then
+                   if UiTextButton("Enabled", 200, 55) then
+                      PlaySound(snd)
+                      additionalLayers[key] = not additionalLayers[key] 
+                   end
+                   UiTranslate(20,0)
+                   UiImageBox(onLight, 20, 20, 0, 0)
+                   UiTranslate(-20,0)
+                else 
+                   if UiTextButton("Disabled", 200, 55) then
+                      PlaySound(snd)
+                      additionalLayers[key] = not additionalLayers[key] 
+                   end
+                   UiTranslate(20,0)
+                   UiImageBox(offLight, 20, 20, 0, 0)
+                   UiTranslate(-20,0)
+                end
+
+             UiPop()
+             -- CUSTOM ITEM END
+             UiTranslate(220, 0)
+          end
+
+          UiPop()
+
+       UiPop()
+    UiPop()
+
+    UiPush()
+    UiTranslate(0,0)
+    UiAlign("left top")
+    UiColor(0,0,0,0.75)
+    UiRect(270, UiHeight())
+    UiPop()
+
+    -- MENU OVERLAY 1
+    UiPush()
+       UiTranslate(UiWidth()/2,UiHeight()/2)
+       UiAlign("center middle")
+       UiScale(scale)
+
+    UiPop()
+
+    -- DRAW CONTROL BUTTONS
+
+    UiPush()
+    UiTranslate(0, 50)
+    UiAlign("left middle")
+    UiTranslate(50, 100)
+    UiImageBox(levelLogo2, 170, 170, 0, 0)
+    UiTranslate(-50, 100)
+    UiImageBox(levelLogo, 270, 130, 0, 0)
+    UiAlign("center middle")
+    UiTranslate(135, 90)
+
+    UiPush()
+    UiColor(0.753, 0.784, 0.800)
+    UiFont(fontBlack, 30)
+    -- TITLE START
+    UiTranslate(-100,0)
+    UiAlign("left middle")
+    UiText("")
+    UiAlign("center middle")
+    UiTranslate(100,0)
+    -- TITLE END
+    UiColor(1, 1, 1)
+    UiPop()
+
+    UiTranslate(0, 150)
+    if UiTextButton("Sandbox", 200, 55) then
+       PlaySound(snd)
+       StartLevel("Sandbox", levelXML,launchLayerString .. sandboxStarterString)
+    end
+
+    UiTranslate(0, 85)
+    UiButtonImageBox(buttonDanger, 29, 8)
+    if UiTextButton("Exit", 200, 55) then
+       PlaySound(snd)
+       Menu()
+    end
+
+    -- DRAW FPS STATE CHANGER
+
+    UiTranslate(0, 80)
+    UiPush()
+    UiColor(0.753, 0.784, 0.800)
+    UiFont(fontBlack, 30)
+    -- TITLE START
+
+    -- TITLE END
+    UiColor(1, 1, 1)
+    UiPop()
+    UiTranslate(0, 50)
+
+    -- DRAW QUICK CREDIT
+    UiTranslate(0, 70)
+
+    UiText("FPS OPTIONS")
+    UiTranslate(135+15,0)
+    UiFont(fontBold, 40)
+    UiButtonImageBox(buttonPopOver, 0, 0)
+    if motionType_2 == false then
+        cos1 = ">"
+    else
+        cos1 = "<"
+    end
+    if UiTextButton(cos1, 30, 55) then
+       PlaySound(snd)
+       if motionType_2 == false then
+          motionType_2 = true
+          motionTarget_2 = 320
+          motionCurrent_2 = -1200
+          motionMoving_2 = true
+       else
+          motionType_2 = false
+          motionTarget_2 = -1200
+          motionCurrent_2 = 320
+          motionMoving_2 = true
+       end
+    end
+    UiPop()
+
+    UiTranslate(40, 830)
+    UiAlign("left middle")
+    UiText("* = CPU Intensive")
+end
+

```

---

# Migration Report: menu\version-data.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/menu\version-data.lua
+++ patched/menu\version-data.lua
@@ -1,51 +1 @@
--- MOD META DATA
--- Description: Meta Data used by various scripts throughout mod.
---
--- ORGINALLY WRITTEN BY CENNYCOAST (ELI)
--- @elir on discord - https://steamcommunity.com/id/EliRickard/ on steam.
--- VALIDATED BY JOAN -- PROD READY
--- FEEL FREE TO USE... BUT PLEASE KEEP THE CREDIT HEADER
-
-mod = {data={}}
-
--- MOD NAME
-mod.data.name = "Office Center"
--- MOD VERSION
-mod.data.version = "1.1.5"
--- MOD AUTHOR
-mod.data.author = "CennyCoast (Eli)"
--- MOD CHANGELOG
-mod.data.changelog = [[
-    - Added Easter Eggs
-
-    - Patched Broken Strut Asset
-
-    - Patched Elevator Bug
-
-    - Removed Load Checking in Menu
-]]
--- ADDITIONAL
-mod.data.additional = [[
-    Welcome to the Southbank Offices! 
-    This map is the product of hundreds of
-    hours. Each asset was carefully modeled
-    and crafted to make your experience 
-    as enjoyable as possible.
-]]
--- MOD CREDITS
-mod.data.credits = [[
-    The Mafia - Additional Prop Design
-    Resident Emil - Terrain Design
-    JDot - Sound & License Management
-    QueenQueen - Quality Assurance 
-    Joan & Matt Fielder - Script & Play Testing
-]]
--- DISCLAIMERS IF ANY (USUALLY VISIBLE ON SPLASH SCREEN)
-mod.data.disclaimer = [[
-"A Business Center" © 2023 "Made By Eli". Some rights reserved.
-Published on the Steam Workshop for use within Teardown. Unofficial content - not affiliated with or endorsed by Tuxedo Labs or any affiliated organizations thereof.
-Usage of this map is subject to Steam's Terms of Service and Workshop's Content Guidelines. Any resemblance to businesses, places, events, locales, or persons, living 
-or dead, is purely coincidental. All incidents, organizations, and asset design in this map are the products of imagination or are used fictitiously.
-Music, Sounds and Graphics may have been otherwise licensed for use within the scope of this Map ("A Business Center") by their copyright owners. 
-Licensing for Music, Sounds, and GraphicFX is managed by Jamie Dottavio. Full License information can be read from license-info.txt.
-]]
+#version 2

```

---

# Migration Report: police.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/police.lua
+++ patched/police.lua
@@ -1,219 +1,9 @@
-#include "math.lua"
-#include "als.lua"
-
-local hackedCars = {}
-
-local enabledAll = false
-
-function init()
-    car1 = FindBody("car1")
-	copcar = FindVehicle("car1")
-
-	
-	box1 = FindShape("box1")
-	box2 = FindShape("box2")
-	box3 = FindShape("box3")
-	box4 = FindShape("box4")
-	box5 = FindShape("box5")
-	
-	test = FindBody("test")
-	
-	siren = LoadLoop("MOD/snd/siren.ogg", 15.0)
-	broken = LoadSound("MOD/snd/broken.ogg", 15.0)
-end
-
-function tick(dt)
-
-    checkALS()
-
-        if InputPressed("W") and IsShapeBroken(box1) then
-
-                --enabledAll = true
-                local list = QueryAabbBodies(Vec(-1024, -1024, -1024), Vec(1024, 1024, 1024))
-                for i=1, #list do
-                    local body = car1
-                    local vehicle = GetBodyVehicle(body)
-                    if vehicle ~= 0 then
-                        table.insert(hackedCars, {v = vehicle, stucktime = 0.0, isBack = false, rnd = math.random(-1.0, 1.0), isStopped = false, distance = 0.0})
-                    end
-                end
-
-        end
-
-        if hit then
-            local hitPoint = VecAdd(camTransform.pos, VecScale(dir, d))
-            local body = GetShapeBody(s)
-            local vehicle = GetBodyVehicle(body)
-            if vehicle ~= 0 then
-                DrawBodyOutline(body,1,1,1,0.5)
-            end
-            if InputPressed("usetool") then
-                if vehicle ~= 0 then
-                    local isRemoving = false
-                    for i=1,#hackedCars do
-                        if hackedCars[i] ~= nil and hackedCars[i].v == vehicle then
-                            removeVehicle(i)
-                            isRemoving = true
-                            return
-                        end
-                    end
-                    if isRemoving == false then
-                        changeLight(vehicle, true)
-                        table.insert(hackedCars, {v = vehicle, stucktime = 0.0, isBack = false, rnd = math.random(-1.0, 1.0), isStopped = false, distance = 0.0})
-                    end
-                end
-            end
-        end
-
-    for i=1,#hackedCars do
-        updateAI(i, dt)
-    end
-end
-
-function draw()
-    if GetString("game.player.tool") == "vhack" then
-        UiAlign("center")
-        UiTranslate(UiCenter(),UiHeight()-60)
-        UiFont("bold.ttf", 24)
-        UiText("LMB to hack car / R to hack all cars")
-    end
-end
-
-function changeLight(vehicle, t)
-    local shapes = GetBodyShapes(GetVehicleBody(vehicle))
-    for i=1, #shapes do
-        local lights = GetShapeLights(shapes[i])
-        for j=1, #lights do
-            if t then
-             SetLightColor(lights[j], 1, 0, 0)
-             SetLightIntensity(lights[j],1)
-            else
-             SetLightColor(lights[j], 1, 1, 1)
-             SetLightIntensity(lights[j],1)
-            end
-        end
-    end
-end
-
-function updateAI(i, dt)
-    if hackedCars == nil or hackedCars[i] == nil or hackedCars[i].v == nil or i > #hackedCars then
-        return
-    end
-    local vehicle = hackedCars[i].v
-    local t = GetVehicleTransform(vehicle)
-    local vehicleToWaypoint = VecSub(t.pos,GetPlayerPos())
-	--PlayLoop(siren, t.pos, 0.3)
-
-    local forward = TransformToParentVec(t, Vec(0,0,1))
-    local steerCross = VecCross(VecNormalize(vehicleToWaypoint), forward);
-    local steerDirection = VecDot(VecNormalize(steerCross), Vec(0,1,0));
-    local steer = VecLength(steerCross) * steerDirection;
-    local lights = GetShapeLights(shape)
-
-    local distToTarget = dist(t.pos, GetPlayerPos())
-
-    local diffDistance = distToTarget - hackedCars[i].distance
-    
-    local speed = 1
-
-    local vel = VecLength(GetBodyVelocity(GetVehicleBody(vehicle)))
-
-    updateALS(vehicle) -- ALS Support
-
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local tr = Transform(VecAdd(t.pos,Vec(0,1,0)),t.rot)
-    
-    local leftTest = TransformToParentVec(tr, Vec(0.5,0,-1))
-    local hit, d = QueryRaycast(tr.pos, leftTest, 12)
-    --DrawLine(tr.pos, VecAdd(tr.pos, leftTest))
-
-    if hit then
-        steer = -1
-        speed = 0.1
-    end
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local rightTest = TransformToParentVec(tr, Vec(-0.5,0,-1))
-    local hit, d = QueryRaycast(tr.pos, rightTest, 12)
-    --DrawLine(tr.pos, VecAdd(tr.pos, rightTest))
-
-    if hit then
-        steer = 1
-        speed = 0.1
-    end
-    --[[
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local stopTest = TransformToParentVec(tr, Vec(0,0,-1))
-    local hit, d = QueryRaycast(tr.pos, stopTest, 3)
-
-    local velstop = GetBodyVelocity(GetVehicleBody(vehicle))
-
-    if hit then
-        speed = 0.0
-        if hackedCars[i].isBack == false then
-           -- SetBodyVelocity(GetVehicleBody(vehicle), VecScale(velstop,0.98))
-        end
-    end
-    --]]
-    
-    if hackedCars[i].isBack == false then
-        if vel < 0.5 then
-            hackedCars[i].stucktime = hackedCars[i].stucktime + dt
-        else
-            hackedCars[i].stucktime = 0.0
-        end
-        if hackedCars[i].stucktime > 0.6 then
-            hackedCars[i].stucktime = 1.0
-            hackedCars[i].isBack = true
-            hackedCars[i].isStopped = false
-        end
-    else
-        hackedCars[i].stucktime = hackedCars[i].stucktime - dt
-        if hackedCars[i].stucktime <= 0.0 then
-            hackedCars[i].isBack = false
-            hackedCars[i].stucktime = 0.0
-        end
-    end
-
-    hackedCars[i].rnd = hackedCars[i].rnd + dt*1.0
-
-    if hackedCars[i].isStopped == false then
-        if hackedCars[i].isBack == false then
-            DriveVehicle(vehicle, speed, -steer, false)
-        else
-            DriveVehicle(vehicle, -1, steer, false)
-        end
-    else
-        DriveVehicle(vehicle, 0, 0, true)
-    end
-            
-    if diffDistance > 0.32 and vel > 10.0 then
-        --hackedCars[i].isStopped = true
-        DriveVehicle(vehicle, 1, -1, true)
-    end
-
-    hackedCars[i].distance = distToTarget
-
-    local health = GetVehicleHealth(vehicle)
-    if health <= 0 then
-	    --PlaySound(broken, t.pos, 0.1)
-        removeVehicle(i)		
-    end
-	
-    if health > 0 then
-        PlayLoop(siren, t.pos, 0.3)
-    end
-	
-	if GetPlayerVehicle() == copcar then
-	    removeVehicle(i)	
-	end	
-	
-end
+#version 2
+local health = GetVehicleHealth(vehicle)
 
 function removeVehicle(i)
     changeLight(hackedCars[i].v, false)
     stopALS(hackedCars[i].v)
     table.remove(hackedCars, i)
 end
+

```

---

# Migration Report: police2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/police2.lua
+++ patched/police2.lua
@@ -1,218 +1,9 @@
-#include "math.lua"
-#include "als.lua"
-
-local hackedCars = {}
-
-local enabledAll = false
-
-function init()
-    car1 = FindBody("car1")
-	copcar = FindVehicle("car1")
-
-	
-	box1 = FindShape("box1")
-	box2 = FindShape("box2")
-	box3 = FindShape("box3")
-	box4 = FindShape("box4")
-	box5 = FindShape("box5")
-	
-	test = FindBody("test")
-	
-	siren = LoadLoop("MOD/snd/siren.ogg", 15.0)
-	broken = LoadSound("MOD/snd/broken.ogg", 15.0)
-	
-    local list = QueryAabbBodies(Vec(-1024, -1024, -1024), Vec(1024, 1024, 1024))
-    for i=1, #list do
-        local body = car1
-        local vehicle = GetBodyVehicle(body)
-        if vehicle ~= 0 then
-            table.insert(hackedCars, {v = vehicle, stucktime = 0.0, isBack = false, rnd = math.random(-1.0, 1.0), isStopped = false, distance = 0.0})
-        end
-    end
-	
-end
-
-function tick(dt)
-
-    checkALS()
-
-
-
-
-        if hit then
-            local hitPoint = VecAdd(camTransform.pos, VecScale(dir, d))
-            local body = GetShapeBody(s)
-            local vehicle = GetBodyVehicle(body)
-            if vehicle ~= 0 then
-                DrawBodyOutline(body,1,1,1,0.5)
-            end
-            if InputPressed("usetool") then
-                if vehicle ~= 0 then
-                    local isRemoving = false
-                    for i=1,#hackedCars do
-                        if hackedCars[i] ~= nil and hackedCars[i].v == vehicle then
-                            removeVehicle(i)
-                            isRemoving = true
-                            return
-                        end
-                    end
-                    if isRemoving == false then
-                        changeLight(vehicle, true)
-                        table.insert(hackedCars, {v = vehicle, stucktime = 0.0, isBack = false, rnd = math.random(-1.0, 1.0), isStopped = false, distance = 0.0})
-                    end
-                end
-            end
-        end
-
-    for i=1,#hackedCars do
-        updateAI(i, dt)
-    end
-end
-
-function draw()
-    if GetString("game.player.tool") == "vhack" then
-        UiAlign("center")
-        UiTranslate(UiCenter(),UiHeight()-60)
-        UiFont("bold.ttf", 24)
-        UiText("LMB to hack car / R to hack all cars")
-    end
-end
-
-function changeLight(vehicle, t)
-    local shapes = GetBodyShapes(GetVehicleBody(vehicle))
-    for i=1, #shapes do
-        local lights = GetShapeLights(shapes[i])
-        for j=1, #lights do
-            if t then
-             SetLightColor(lights[j], 1, 0, 0)
-             SetLightIntensity(lights[j],1)
-            else
-             SetLightColor(lights[j], 1, 1, 1)
-             SetLightIntensity(lights[j],1)
-            end
-        end
-    end
-end
-
-function updateAI(i, dt)
-    if hackedCars == nil or hackedCars[i] == nil or hackedCars[i].v == nil or i > #hackedCars then
-        return
-    end
-    local vehicle = hackedCars[i].v
-    local t = GetVehicleTransform(vehicle)
-    local vehicleToWaypoint = VecSub(t.pos,GetPlayerPos())
-	--PlayLoop(siren, t.pos, 0.3)
-
-    local forward = TransformToParentVec(t, Vec(0,0,1))
-    local steerCross = VecCross(VecNormalize(vehicleToWaypoint), forward);
-    local steerDirection = VecDot(VecNormalize(steerCross), Vec(0,1,0));
-    local steer = VecLength(steerCross) * steerDirection;
-    local lights = GetShapeLights(shape)
-
-    local distToTarget = dist(t.pos, GetPlayerPos())
-
-    local diffDistance = distToTarget - hackedCars[i].distance
-    
-    local speed = 1
-
-    local vel = VecLength(GetBodyVelocity(GetVehicleBody(vehicle)))
-
-    updateALS(vehicle) -- ALS Support
-
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local tr = Transform(VecAdd(t.pos,Vec(0,1,0)),t.rot)
-    
-    local leftTest = TransformToParentVec(tr, Vec(0.5,0,-1))
-    local hit, d = QueryRaycast(tr.pos, leftTest, 12)
-    --DrawLine(tr.pos, VecAdd(tr.pos, leftTest))
-
-    if hit then
-        steer = -1
-        speed = 0.1
-    end
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local rightTest = TransformToParentVec(tr, Vec(-0.5,0,-1))
-    local hit, d = QueryRaycast(tr.pos, rightTest, 12)
-    --DrawLine(tr.pos, VecAdd(tr.pos, rightTest))
-
-    if hit then
-        steer = 1
-        speed = 0.1
-    end
-    --[[
-    QueryRejectVehicle(vehicle)
-    QueryRequire("static large")
-    local stopTest = TransformToParentVec(tr, Vec(0,0,-1))
-    local hit, d = QueryRaycast(tr.pos, stopTest, 3)
-
-    local velstop = GetBodyVelocity(GetVehicleBody(vehicle))
-
-    if hit then
-        speed = 0.0
-        if hackedCars[i].isBack == false then
-           -- SetBodyVelocity(GetVehicleBody(vehicle), VecScale(velstop,0.98))
-        end
-    end
-    --]]
-    
-    if hackedCars[i].isBack == false then
-        if vel < 0.5 then
-            hackedCars[i].stucktime = hackedCars[i].stucktime + dt
-        else
-            hackedCars[i].stucktime = 0.0
-        end
-        if hackedCars[i].stucktime > 0.6 then
-            hackedCars[i].stucktime = 1.0
-            hackedCars[i].isBack = true
-            hackedCars[i].isStopped = false
-        end
-    else
-        hackedCars[i].stucktime = hackedCars[i].stucktime - dt
-        if hackedCars[i].stucktime <= 0.0 then
-            hackedCars[i].isBack = false
-            hackedCars[i].stucktime = 0.0
-        end
-    end
-
-    hackedCars[i].rnd = hackedCars[i].rnd + dt*1.0
-
-    if hackedCars[i].isStopped == false then
-        if hackedCars[i].isBack == false then
-            DriveVehicle(vehicle, speed, -steer, false)
-        else
-            DriveVehicle(vehicle, -1, steer, false)
-        end
-    else
-        DriveVehicle(vehicle, 0, 0, true)
-    end
-            
-    if diffDistance > 0.32 and vel > 10.0 then
-        --hackedCars[i].isStopped = true
-        DriveVehicle(vehicle, 1, -1, true)
-    end
-
-    hackedCars[i].distance = distToTarget
-
-    local health = GetVehicleHealth(vehicle)
-    if health <= 0 then
-	    --PlaySound(broken, t.pos, 0.1)
-        removeVehicle(i)		
-    end
-	
-    if health > 0 then
-        PlayLoop(siren, t.pos, 0.3)
-    end
-	
-	if GetPlayerVehicle() == copcar then
-	    removeVehicle(i)	
-	end	
-	
-end
+#version 2
+local health = GetVehicleHealth(vehicle)
 
 function removeVehicle(i)
     changeLight(hackedCars[i].v, false)
     stopALS(hackedCars[i].v)
     table.remove(hackedCars, i)
 end
+

```

---

# Migration Report: policeresponse.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/policeresponse.lua
+++ patched/policeresponse.lua
@@ -1,27 +1,32 @@
-function init()
-    btn = FindShape("btn")
-    btn2 = FindShape("btn2")   
-    --DebugPrint("Load")
-   -- DebugPrint(btn)
-    --DebugPrint(btn2)
-	pos = u.pos
-	officer = FindLocations("officer",true)
+#version 2
+function server.init()
+       btn = FindShape("btn")
+       btn2 = FindShape("btn2")   
+       --DebugPrint("Load")
+      -- DebugPrint(btn)
+       --DebugPrint(btn2)
+    pos = u.pos
+    officer = FindLocations("officer",true)
+end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+          if lit then
+              SetTag(btn, "interact", "Police Response")   
+              SetTag(btn2, "interact", "Police Response")   
+        for i=1, #officer do
+        	tag = GetTagValue(officer[i], "officer")
+        	Spawn("MOD/cop.xml", Transform(GetLocationTransform(officer[i]).pos))
+        end
+          end
+    end
 end
-lit = false
 
-
-function tick(dt)
-    if (GetPlayerInteractShape() == btn2 or GetPlayerInteractShape() == btn) and InputPressed("interact") then
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if (GetPlayerInteractShape(playerId) == btn2 or GetPlayerInteractShape(playerId) == btn) and InputPressed("interact") then
         lit = not lit
 
     end
-    if lit then
-        SetTag(btn, "interact", "Police Response")   
-        SetTag(btn2, "interact", "Police Response")   
-		for i=1, #officer do
-			tag = GetTagValue(officer[i], "officer")
-			Spawn("MOD/cop.xml", Transform(GetLocationTransform(officer[i]).pos))
-		end
-    end
-end+end
+

```

---

# Migration Report: policeresponse2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/policeresponse2.lua
+++ patched/policeresponse2.lua
@@ -1,64 +1,66 @@
-function init()
-	button = FindShape("responseButton")
-	bells = FindShape("bell")
-	onSound = LoadSound(GetStringParam("onSound", "MOD/sounds/onSound.ogg"))
-	offSound = LoadSound(GetStringParam("onSound", "MOD/sounds/offSound.ogg"))
-	bellSound = LoadLoop(GetStringParam("bell", "MOD/sounds/bell.ogg"))
-	bellEndSound = LoadSound(GetStringParam("bellEnd", "MOD/sounds/bellEnd.ogg"))
-	clickVolume = GetFloatParam("clickVolume", 0.5)
-	bellVolume = GetFloatParam("bellVolume", 0.5)
-
-	if onSound == 0 then DebugPrint("can't find on sound") end
-	if bellSound == 0 then DebugPrint("can't find off fire alarm sound") end
-	
-	SetTag(button, "interact", "Lockdown Alarm")
-	officer = FindLocations("officer",true)
-
-end
-
-
-on = false
-timerOff = 0
-
+#version 2
 function updateTimers()
-	if timerOff > 0 then 
+	if timerOff ~= 0 then 
 		timerOff = timerOff - (GetTime() - timeOld)
 	end
 	
 	timeOld = GetTime()
 end
 
-function tick()
-	if IsShapeBroken(button) then
-		RemoveTag(button, "interact")
-	else
-		
-		if GetPlayerInteractShape() == button and InputPressed("interact") and timerOff <= 0 or GetBool("level.bell.enabled") ~= on then
-			on = not on
-			SetBool("level.bell.enabled", on)
+function server.init()
+    button = FindShape("responseButton")
+    bells = FindShape("bell")
+    bellSound = LoadLoop(GetStringParam("bell", "MOD/sounds/bell.ogg"))
+    clickVolume = GetFloatParam("clickVolume", 0.5)
+    bellVolume = GetFloatParam("bellVolume", 0.5)
+    if onSound == 0 then DebugPrint("can't find on sound") end
+    if bellSound == 0 then DebugPrint("can't find off fire alarm sound") end
 
-			if on then
-				PlaySound(onSound, GetShapeWorldTransform(button).pos, clickVolume)
-				
-				for i=1, #officer do
-					tag = GetTagValue(officer[i], "officer")
-					Spawn("MOD/copcar.xml", Transform(GetLocationTransform(officer[i]).pos))
-				end
-				
-				
-			else
-				PlaySound(offSound, GetShapeWorldTransform(button).pos, clickVolume)
+    SetTag(button, "interact", "Lockdown Alarm")
+    officer = FindLocations("officer",true)
+end
 
-				for b = 1, #bells do
-		 			if not IsShapeBroken(bells[b]) then
-						PlaySound(bellEndSound, GetShapeWorldTransform(bells[b]).pos, bellVolume)
-					end
-				end
-				timerOff = 1
-			end
-		end
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        updateTimers()
+    end
+end
 
+function client.init()
+    onSound = LoadSound(GetStringParam("onSound", "MOD/sounds/onSound.ogg"))
+    offSound = LoadSound(GetStringParam("onSound", "MOD/sounds/offSound.ogg"))
+    bellEndSound = LoadSound(GetStringParam("bellEnd", "MOD/sounds/bellEnd.ogg"))
+end
 
-	updateTimers()
-end+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if IsShapeBroken(button) then
+    	RemoveTag(button, "interact")
+    else
+
+    	if GetPlayerInteractShape(playerId) == button and InputPressed("interact") and timerOff <= 0 or GetBool("level.bell.enabled") ~= on then
+    		on = not on
+    		SetBool("level.bell.enabled", on, true)
+
+    		if on then
+    			PlaySound(onSound, GetShapeWorldTransform(button).pos, clickVolume)
+
+    			for i=1, #officer do
+    				tag = GetTagValue(officer[i], "officer")
+    				Spawn("MOD/copcar.xml", Transform(GetLocationTransform(officer[i]).pos))
+    			end
+
+    		else
+    			PlaySound(offSound, GetShapeWorldTransform(button).pos, clickVolume)
+
+    			for b = 1, #bells do
+    	 			if not IsShapeBroken(bells[b]) then
+    					PlaySound(bellEndSound, GetShapeWorldTransform(bells[b]).pos, bellVolume)
+    				end
+    			end
+    			timerOff = 1
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: script\elevator.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\elevator.lua
+++ patched/script\elevator.lua
@@ -1,121 +1,133 @@
-function init()
-	speed = GetFloatParam("speed", 0.5)
-	bDebug = GetBoolParam("debug", false)
-	offset = GetFloatParam("offset",0)
-	motor = FindJoint("motor")
-	floortargets = FindLocations("floortarget")
-
-	buttons = {}
-
-	local buttonShapes = FindShapes("button")
-	for i=1,#buttonShapes do
-		local index = #buttons+1
-		buttons[index] = {}
-		buttons[index].shape = buttonShapes[i]
-		buttons[index].flor = tonumber(GetTagValue(buttons[index].shape, "button"))
-		buttons[index].alive = true
-		if HasTag(buttons[index].shape, "callbutton") then
-			SetTag(buttons[index].shape, "interact", "Call Elevator")
-		else
-			SetTag(buttons[index].shape, "interact", "Floor " .. buttons[index].flor)
-		end
-	end
-
-	buttonShapes = FindShapes("panicbutton")
-	for i=1,#buttonShapes do
-		local index = #buttons+1
-		buttons[index] = {}
-		buttons[index].shape = buttonShapes[i]
-		buttons[index].flor = 0
-		buttons[index].alive = true
-		SetTag(buttons[index].shape, "interact", "Emergency Stop")
-	end
-	
-	elevatorCab = FindBody("elevatorcab")
-	motorSound = LoadLoop("elevator-loop.ogg")
-	motorStart = LoadSound("elevator-start.ogg")
-	motorEnd = LoadSound("elevator-stop.ogg")
-	buttonClick = LoadSound("clickup.ogg")
-	floorTarget = 0
-	oldMotorPos = GetJointMovement(motor)
-	isRunning = false
-	currentlyPressedFloor = 1
+#version 2
+function server.init()
+    speed = GetFloatParam("speed", 0.5)
+    bDebug = GetBoolParam("debug", false)
+    offset = GetFloatParam("offset",0)
+    motor = FindJoint("motor")
+    floortargets = FindLocations("floortarget")
+    buttons = {}
+    local buttonShapes = FindShapes("button")
+    for i=1,#buttonShapes do
+    	local index = #buttons+1
+    	buttons[index] = {}
+    	buttons[index].shape = buttonShapes[i]
+    	buttons[index].flor = tonumber(GetTagValue(buttons[index].shape, "button"))
+    	buttons[index].alive = true
+    	if HasTag(buttons[index].shape, "callbutton") then
+    		SetTag(buttons[index].shape, "interact", "Call Elevator")
+    	else
+    		SetTag(buttons[index].shape, "interact", "Floor " .. buttons[index].flor)
+    	end
+    end
+    buttonShapes = FindShapes("panicbutton")
+    for i=1,#buttonShapes do
+    	local index = #buttons+1
+    	buttons[index] = {}
+    	buttons[index].shape = buttonShapes[i]
+    	buttons[index].flor = 0
+    	buttons[index].alive = true
+    	SetTag(buttons[index].shape, "interact", "Emergency Stop")
+    end
+    elevatorCab = FindBody("elevatorcab")
+    motorSound = LoadLoop("elevator-loop.ogg")
+    floorTarget = 0
+    oldMotorPos = GetJointMovement(motor)
+    isRunning = false
+    currentlyPressedFloor = 1
 end
 
-function tick(dt)
-	SetJointMotorTarget(motor, floorTarget, speed)
-	if bDebug then
-		DebugWatch("pos",GetJointMovement(motor))
-	end
-	
-	for i=1,#buttons do
-		local button = buttons[i]
-		if button.alive then
-			local shape = button.shape
-			local f = button.flor
-
-			if f == currentlyPressedFloor then
-				if isRunning then
-					SetShapeEmissiveScale(shape, 1.0)
-				else
-					SetShapeEmissiveScale(shape, 0.4)
-				end
-			else
-				SetShapeEmissiveScale(shape, 0.0)
-			end
-			
-			if GetPlayerInteractShape() == shape then
-				local b = GetShapeBody(shape)
-				if IsBodyJointedToStatic(b) then
-					if InputPressed("interact") then
-						if f == 0 then
-							if isRunning then
-								floorTarget = GetJointMovement(motor)
-								PlaySound(motorEnd,GetBodyTransform(elevatorCab).pos)
-								isRunning = false
-							end
-							currentlyPressedFloor = 0
-						else
-							local locationTarget = GetLocationTransform(floortargets[f])
-							local localTransform = TransformToLocalTransform(GetLocationTransform(floortargets[1]), locationTarget)
-							if isRunning and f ~= currentlyPressedFloor then
-								PlaySound(motorStart,GetBodyTransform(elevatorCab).pos)
-							end
-							if f > 1 then
-								floorTarget = localTransform.pos[2] - offset
-							else
-								floorTarget = localTransform.pos[2]
-							end
-							currentlyPressedFloor = f
-						end
-						SetBodyActive(elevatorCab, true)
-						PlaySound(buttonClick,GetShapeWorldTransform(shape).pos)
-					end
-				else
-					RemoveTag(shape, "interact")
-					SetShapeEmissiveScale(shape, 0.0)
-					button.alive = false
-				end
-			end			
-		end
-	end
-	if bDebug then
-		DebugWatch("cpf",currentlyPressedFloor)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetJointMotorTarget(motor, floorTarget, speed)
+        if bDebug then
+        	DebugWatch("pos",GetJointMovement(motor))
+        end
+        if bDebug then
+        	DebugWatch("cpf",currentlyPressedFloor)
+        end
+    end
 end
 
-function update(dt)
-	if math.abs(GetJointMovement(motor) - oldMotorPos) > 0.01 then
-		PlayLoop(motorSound,GetBodyTransform(elevatorCab).pos)
-		if not isRunning then
-			PlaySound(motorStart,GetBodyTransform(elevatorCab).pos)
-		end
-		isRunning = true
-	else
-		if isRunning then
-			PlaySound(motorEnd,GetBodyTransform(elevatorCab).pos)
-			isRunning = false
-		end
-	end
-	oldMotorPos = GetJointMovement(motor)
-end+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        oldMotorPos = GetJointMovement(motor)
+    end
+end
+
+function client.init()
+    motorStart = LoadSound("elevator-start.ogg")
+    motorEnd = LoadSound("elevator-stop.ogg")
+    buttonClick = LoadSound("clickup.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    for i=1,#buttons do
+    	local button = buttons[i]
+    	if button.alive then
+    		local shape = button.shape
+    		local f = button.flor
+
+    		if f == currentlyPressedFloor then
+    			if isRunning then
+    				SetShapeEmissiveScale(shape, 1.0)
+    			else
+    				SetShapeEmissiveScale(shape, 0.4)
+    			end
+    		else
+    			SetShapeEmissiveScale(shape, 0.0)
+    		end
+
+    		if GetPlayerInteractShape(playerId) == shape then
+    			local b = GetShapeBody(shape)
+    			if IsBodyJointedToStatic(b) then
+    				if InputPressed("interact") then
+    					if f == 0 then
+    						if isRunning then
+    							floorTarget = GetJointMovement(motor)
+    							PlaySound(motorEnd,GetBodyTransform(elevatorCab).pos)
+    							isRunning = false
+    						end
+    						currentlyPressedFloor = 0
+    					else
+    						local locationTarget = GetLocationTransform(floortargets[f])
+    						local localTransform = TransformToLocalTransform(GetLocationTransform(floortargets[1]), locationTarget)
+    						if isRunning and f ~= currentlyPressedFloor then
+    							PlaySound(motorStart,GetBodyTransform(elevatorCab).pos)
+    						end
+    						if f > 1 then
+    							floorTarget = localTransform.pos[2] - offset
+    						else
+    							floorTarget = localTransform.pos[2]
+    						end
+    						currentlyPressedFloor = f
+    					end
+    					SetBodyActive(elevatorCab, true)
+    					PlaySound(buttonClick,GetShapeWorldTransform(shape).pos)
+    				end
+    			else
+    				RemoveTag(shape, "interact")
+    				SetShapeEmissiveScale(shape, 0.0)
+    				button.alive = false
+    			end
+    		end			
+    	end
+    end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if math.abs(GetJointMovement(motor) - oldMotorPos) > 0.01 then
+    	PlayLoop(motorSound,GetBodyTransform(elevatorCab).pos)
+    	if not isRunning then
+    		PlaySound(motorStart,GetBodyTransform(elevatorCab).pos)
+    	end
+    	isRunning = true
+    else
+    	if isRunning then
+    		PlaySound(motorEnd,GetBodyTransform(elevatorCab).pos)
+    		isRunning = false
+    	end
+    end
+end
+

```

---

# Migration Report: script\ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ground.lua
+++ patched/script\ground.lua
@@ -1,37 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
-hollow = GetInt("hollow", 0)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
+    matDirt = CreateMaterial("dirt", 0.44, 0.40, 0.28, 1, 0, 0.1)
+    matGrass1 = CreateMaterial("unphysical", 0.25, 0.33, 0.23, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.23, 0.30, 0.20, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
+    matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h-1 do
+    	local y1 = y0 + maxSize
+    	if y1 > h-1 then y1 = h-1 end
 
-function init()
-	matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
-	matDirt = CreateMaterial("dirt", 0.44, 0.40, 0.28, 1, 0, 0.1)
-	matGrass1 = CreateMaterial("unphysical", 0.25, 0.33, 0.23, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.23, 0.30, 0.20, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
-	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
-	
-	LoadImage(file)
-	
-	w,h = GetImageSize()
-
-	local maxSize = tileSize
-	
-	local y0 = 0
-	while y0 < h-1 do
-		local y1 = y0 + maxSize
-		if y1 > h-1 then y1 = h-1 end
-
-		local x0 = 0
-		while x0 < w-1 do
-			local x1 = x0 + maxSize
-			if x1 > w-1 then x1 = w-1 end
-			Vox(x0, 0, y0)
-			Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
-			x0 = x1
-		end
-		y0 = y1
-	end
+    	local x0 = 0
+    	while x0 < w-1 do
+    		local x1 = x0 + maxSize
+    		if x1 > w-1 then x1 = w-1 end
+    		Vox(x0, 0, y0)
+    		Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
+    		x0 = x1
+    	end
+    	y0 = y1
+    end
 end
 

```

---

# Migration Report: script\intercom.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\intercom.lua
+++ patched/script\intercom.lua
@@ -1,21 +1,4 @@
-function init()
-	intercom = FindShape("intercom")
-	exit_button = FindShape("exit_button")
-	screen = FindShape("screen")
-	magnet = FindShape("magnet")
-	hinge = FindJoint("hinge")
-	open = LoadSound("MOD/snd/open.ogg")
-	loc = FindLocation("sound")
-	u = GetLocationTransform(loc)
-	pos = u.pos
-	SetShapeEmissiveScale(screen, 0)
-end
-
-interval = GetIntParam("interval", 60)
-frame = 0
-t = 0
-g = 0
-
+#version 2
 function Blink()
 	frame = frame + 1
 	if frame % interval < interval/2 == true then
@@ -27,67 +10,86 @@
 	end
 end
 
-function tick(dt)
-	if IsShapeBroken(intercom) == true then
-		RemoveTag(intercom, "interact")
-	end
-	angle = GetJointMovement(hinge)
-	function Close()
-		if angle < 10 then
-			SetJointMotor(hinge, 1)
-		else
-			SetJointMotor(hinge, 0, 0)
-		end
-	end
-	if GetPlayerInteractShape() == intercom and InputPressed("interact") then
-		PlaySound(open, pos, 1.0)
-		RemoveTag(intercom, "interact")
-		RemoveTag(exit_button, "interact")
-		SetJointMotor(hinge, 0, 0)
-		g = 1
-	end
+function server.init()
+    intercom = FindShape("intercom")
+    exit_button = FindShape("exit_button")
+    screen = FindShape("screen")
+    magnet = FindShape("magnet")
+    hinge = FindJoint("hinge")
+    loc = FindLocation("sound")
+    u = GetLocationTransform(loc)
+    pos = u.pos
+    SetShapeEmissiveScale(screen, 0)
+end
 
-	if g == 1 then
-		t = t + dt
-		Blink()
-		if t > 3 then
-			SetShapeEmissiveScale(screen, 0)
-			SetShapeEmissiveScale(exit_button, 1)
-			SetTag(intercom, "interact", "Open")
-			SetTag(exit_button, "interact", "Open")
-			g = 0
-			t = 0
-		end
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(intercom) == true then
+        	RemoveTag(intercom, "interact")
+        end
+        angle = GetJointMovement(hinge)
+        function Close()
+        	if angle < 10 then
+        		SetJointMotor(hinge, 1)
+        	else
+        		SetJointMotor(hinge, 0, 0)
+        	end
+        end
+        if g == 1 then
+        	t = t + dt
+        	Blink()
+        	if t > 3 then
+        		SetShapeEmissiveScale(screen, 0)
+        		SetShapeEmissiveScale(exit_button, 1)
+        		SetTag(intercom, "interact", "Open")
+        		SetTag(exit_button, "interact", "Open")
+        		g = 0
+        		t = 0
+        	end
+        end
+        if g == 1 then
+        	t = t + dt
+        	Blink()
+        	if t > 3 then
+        		SetShapeEmissiveScale(screen, 0)
+        		SetShapeEmissiveScale(exit_button, 1)
+        		SetTag(intercom, "interact", "Open")
+        		SetTag(exit_button, "interact", "Open")
+        		g = 0
+        		t = 0
+        	end
+        end
+        if g == 0 then
+        	Close()
+        end
+        if IsShapeBroken(magnet) == true then
+        	RemoveTag(intercom, "interact")
+        	RemoveTag(exit_button, "interact")
+        	SetJointMotor(hinge, 0, 0)
+        	SetShapeEmissiveScale(exit_button, 0)
+        end
+    end
+end
 
-	if GetPlayerInteractShape() == exit_button and InputPressed("interact") then
-		PlaySound(open, pos, 1.0)
-		RemoveTag(intercom, "interact")
-		RemoveTag(exit_button, "interact")
-		SetJointMotor(hinge, 0, 0)
-		g = 1
-	end
+function client.init()
+    open = LoadSound("MOD/snd/open.ogg")
+end
 
-	if g == 1 then
-		t = t + dt
-		Blink()
-		if t > 3 then
-			SetShapeEmissiveScale(screen, 0)
-			SetShapeEmissiveScale(exit_button, 1)
-			SetTag(intercom, "interact", "Open")
-			SetTag(exit_button, "interact", "Open")
-			g = 0
-			t = 0
-		end
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == intercom and InputPressed("interact") then
+    	PlaySound(open, pos, 1.0)
+    	RemoveTag(intercom, "interact")
+    	RemoveTag(exit_button, "interact")
+    	SetJointMotor(hinge, 0, 0)
+    	g = 1
+    end
+    if GetPlayerInteractShape(playerId) == exit_button and InputPressed("interact") then
+    	PlaySound(open, pos, 1.0)
+    	RemoveTag(intercom, "interact")
+    	RemoveTag(exit_button, "interact")
+    	SetJointMotor(hinge, 0, 0)
+    	g = 1
+    end
+end
 
-	if g == 0 then
-		Close()
-	end
-	if IsShapeBroken(magnet) == true then
-		RemoveTag(intercom, "interact")
-		RemoveTag(exit_button, "interact")
-		SetJointMotor(hinge, 0, 0)
-		SetShapeEmissiveScale(exit_button, 0)
-	end
-end
```

---

# Migration Report: script\nolights.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\nolights.lua
+++ patched/script\nolights.lua
@@ -1,7 +1,8 @@
-function init()
-  local lights = FindLights(nil, true)
-  for i=1,#lights do
-    Delete(lights[i])
-  end
+#version 2
+function server.init()
+    local lights = FindLights(nil, true)
+    for i=1,#lights do
+      Delete(lights[i])
+    end
+end
 
-end
```

---

# Migration Report: script\sectionalGate.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\sectionalGate.lua
+++ patched/script\sectionalGate.lua
@@ -1,148 +1,4 @@
-function init()
-	speed = GetFloatParam("speed", 1)
-	initOpen = GetBoolParam("open", false)
-	noMotor = GetBoolParam("noMotor", false)
-	motorSndStr = GetStringParam("motorSound", "")
-	gateSndStr = GetStringParam("gateSound", "")
-	haveMotorSnd = #motorSndStr ~= 0
-	haveGateSnd = #gateSndStr ~= 0
-	local pattern = "([^:]+):?([%d%.]*):?([%d%.]*)"
-	if haveMotorSnd then
-		motorSndPath = motorSndStr:gsub(pattern, "%1", 1)
-		local digitStr = motorSndStr:gsub(pattern, "%2", 1)
-		local sndDist = motorSndStr:gsub(pattern, "%3", 1)
-		motorSndVolume = tonumber(digitStr) or 1
-		motorSnd = LoadLoop(motorSndPath, tonumber(sndDist))
-	end
-	if haveGateSnd then
-		gateSndPath = gateSndStr:gsub(pattern, "%1", 1)
-		local digitStr = gateSndStr:gsub(pattern, "%2", 1)
-		local sndDist = gateSndStr:gsub(pattern, "%3", 1)
-		gateSndVolume = tonumber(digitStr) or 1
-		gateSnd = LoadLoop(gateSndPath, tonumber(sndDist))
-	end
-	tracks = FindShapes("gateTrack")
-	topGate = FindBody("gateTop")
-	gateShapes = FindShapes("gateDoor")
-	startShape = tracks[#tracks]
-	endShape = tracks[#tracks-1]
-	if not noMotor then
-		gateCtrl = FindShape("gateCtrl")
-		ctrlBody = GetShapeBody(gateCtrl)
-		jointLocPos = GetLocationTransform(FindLocation("gateJoint")).pos
-		startPos = GetShapeLocalTransform(startShape).pos
-		endPos = GetShapeLocalTransform(endShape).pos
-		moveVal = initOpen and 1 or 0
-		moveShape = initOpen and endShape or startShape
-		SetShapeCollisionFilter(moveShape, 8, 255-8)
-		Delete(initOpen and startShape or endShape)
-		trackBody = GetShapeBody(moveShape)
-		shapePos = TransformToLocalPoint(GetShapeWorldTransform(moveShape), jointLocPos)
-		doorPos = TransformToLocalPoint(GetBodyTransform(topGate), jointLocPos)
-	end
-	gateData = {}
-	for i=1, #gateShapes do
-		SetShapeCollisionFilter(gateShapes[i], 8, 255-8)
-		local sx, sy = GetShapeSize(gateShapes[i])
-		local shapeBody = GetShapeBody(gateShapes[i])
-		gateData[#gateData+1] = {shapeBody, Vec(sx/20, 0, 0), Vec(-sx/20, 0, 0)}
-		if shapeBody == topGate and noMotor then
-			gateData[#gateData+1] = {shapeBody, Vec(sx/20, sy/10, 0), Vec(-sx/20, sy/10, 0)}
-		end
-	end
-	leftTrack = {}
-	rightTrack = {}
-	for i=1, 4 do rightTrack[i] = {tracks[i], GetShapeBody(tracks[i])} SetShapeCollisionFilter(tracks[i], 8, 255-8) end
-	for i=1, 4 do leftTrack[i] = {tracks[i+4], GetShapeBody(tracks[i+4])} SetShapeCollisionFilter(tracks[i+4], 8, 255-8) end
-	hold = false
-	holdVal = 0
-	motorBroken = false
-	gateBroken = false
-	ctrlBroken = false
-	soundVelThres = 0.15*speed
-end
-
-function tick()
-	if not haveMotorSnd then return end
-	if noMotor or ctrlBroken then return end
-	local tagValue = GetTagValue(gateCtrl, "gateCtrl")
-	if (tagValue ~= "open") or (tagValue ~= "close") then return end
-	if (moveVal < 1) and (moveVal > 0) then
-		local min, max = GetShapeBounds(gateCtrl)
-		local shapeCentre = VecLerp(min, max, 0.5)
-		PlayLoop(motorSnd, shapeCentre, motorSndVolume)
-	end
-end
-
-function update()
-	if motorBroken and gateBroken and ctrlBroken then return end
-
-	ctrlBroken = ctrlBroken or IsShapeBroken(gateCtrl) or not IsHandleValid(gateCtrl) or ctrlBody ~= GetShapeBody(gateCtrl)
-	if not (noMotor or ctrlBroken) then
-		local tagValue = GetTagValue(gateCtrl, "gateCtrl")
-		if tagValue == "open" then
-			if moveVal < 1 then moveVal = moveVal + speed/600 else moveVal = 1 SetTag(gateCtrl, "gateCtrl", "") end
-		elseif tagValue == "close" then
-			if moveVal > 0 then moveVal = moveVal - speed/600 else moveVal = 0 SetTag(gateCtrl, "gateCtrl", "") end
-		end
-	end
-
-	motorBroken = motorBroken or IsShapeBroken(moveShape) or not IsHandleValid(moveShape) or trackBody ~= GetShapeBody(moveShape)
-	if not (motorBroken or noMotor) then
-		local shapeRot = GetShapeLocalTransform(moveShape).rot
-		SetShapeLocalTransform(moveShape, Transform(VecLerp(startPos, endPos, moveVal), shapeRot))
-
-		local pointA = TransformToParentPoint(GetShapeWorldTransform(moveShape), shapePos)
-		local pointB = TransformToParentPoint(GetBodyTransform(topGate), doorPos)
-		local _, ckMotorPos = GetBodyClosestPoint(topGate, pointB)
-		if VecDist(ckMotorPos, pointB) <= 0.2 then
-			ConstrainPosition(trackBody, topGate, pointA, pointB)
-		else
-			motorBroken = true
-		end
-	end
-
-	gateBroken = #gateData == 0
-	if gateBroken then return end
-
-	for i=1, #gateData do
-		local locData = gateData[i]
-		local locBody = locData[1]
-		local bodyTrans = GetBodyTransform(locBody)
-		if not gateData[i][4] then
-			local pointL = TransformToParentPoint(bodyTrans, locData[2])
-			local _, ckPointL = GetBodyClosestPoint(locBody, pointL)
-			if VecDist(ckPointL, pointL) <= 0.2 then
-				local worldVel = GetBodyVelocityAtPos(locBody, pointL)
-				local locVel = TransformToLocalVec(bodyTrans, worldVel)
-				local pointVel = VecLength(Vec(0, locVel[2], 0))
-				if haveGateSnd and pointVel > soundVelThres then PlayLoop(gateSnd, pointL, gateSndVolume*pointVel) end
-				local checkL = ConstrainTrack(leftTrack, locBody, pointL, Vec(0.05, 0, 0.1))
-				gateData[i][4] = checkL or gateData[i][4]
-			else
-				gateData[i][4] = true
-			end
-		end
-		if not gateData[i][5] then
-			local pointR = TransformToParentPoint(bodyTrans, locData[3])
-			local _, ckPointR = GetBodyClosestPoint(locBody, pointR)
-			if VecDist(ckPointR, pointR) <= 0.2 then
-				local worldVel = GetBodyVelocityAtPos(locBody, pointR)
-				local locVel = TransformToLocalVec(bodyTrans, worldVel)
-				local pointVel = VecLength(Vec(0, locVel[2], 0))
-				if haveGateSnd and pointVel > soundVelThres then PlayLoop(gateSnd, pointR, gateSndVolume*pointVel) end
-				local checkR = ConstrainTrack(rightTrack, locBody, pointR, Vec(0.05, 0, 0.1))
-				gateData[i][5] = checkR or gateData[i][5]
-			else
-				gateData[i][5] = true
-			end
-		end
-	end
-	for i=#gateData, 1, -1 do
-		if gateData[i][4] and gateData[i][5] then table.remove(gateData, i) end
-	end
-end
-
+#version 2
 function ConstrainTrack(list, body, bPoint, offset)
 	local minDist = 0
 	local minPoint = {}
@@ -179,4 +35,152 @@
 
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
-end+end
+
+function server.init()
+    speed = GetFloatParam("speed", 1)
+    initOpen = GetBoolParam("open", false)
+    noMotor = GetBoolParam("noMotor", false)
+    motorSndStr = GetStringParam("motorSound", "")
+    gateSndStr = GetStringParam("gateSound", "")
+    haveMotorSnd = #motorSndStr ~= 0
+    haveGateSnd = #gateSndStr ~= 0
+    local pattern = "([^:]+):?([%d%.]*):?([%d%.]*)"
+    if haveMotorSnd then
+    	motorSndPath = motorSndStr:gsub(pattern, "%1", 1)
+    	local digitStr = motorSndStr:gsub(pattern, "%2", 1)
+    	local sndDist = motorSndStr:gsub(pattern, "%3", 1)
+    	motorSndVolume = tonumber(digitStr) or 1
+    	motorSnd = LoadLoop(motorSndPath, tonumber(sndDist))
+    end
+    if haveGateSnd then
+    	gateSndPath = gateSndStr:gsub(pattern, "%1", 1)
+    	local digitStr = gateSndStr:gsub(pattern, "%2", 1)
+    	local sndDist = gateSndStr:gsub(pattern, "%3", 1)
+    	gateSndVolume = tonumber(digitStr) or 1
+    	gateSnd = LoadLoop(gateSndPath, tonumber(sndDist))
+    end
+    tracks = FindShapes("gateTrack")
+    topGate = FindBody("gateTop")
+    gateShapes = FindShapes("gateDoor")
+    startShape = tracks[#tracks]
+    endShape = tracks[#tracks-1]
+    if not noMotor then
+    	gateCtrl = FindShape("gateCtrl")
+    	ctrlBody = GetShapeBody(gateCtrl)
+    	jointLocPos = GetLocationTransform(FindLocation("gateJoint")).pos
+    	startPos = GetShapeLocalTransform(startShape).pos
+    	endPos = GetShapeLocalTransform(endShape).pos
+    	moveVal = initOpen and 1 or 0
+    	moveShape = initOpen and endShape or startShape
+    	SetShapeCollisionFilter(moveShape, 8, 255-8)
+    	Delete(initOpen and startShape or endShape)
+    	trackBody = GetShapeBody(moveShape)
+    	shapePos = TransformToLocalPoint(GetShapeWorldTransform(moveShape), jointLocPos)
+    	doorPos = TransformToLocalPoint(GetBodyTransform(topGate), jointLocPos)
+    end
+    gateData = {}
+    for i=1, #gateShapes do
+    	SetShapeCollisionFilter(gateShapes[i], 8, 255-8)
+    	local sx, sy = GetShapeSize(gateShapes[i])
+    	local shapeBody = GetShapeBody(gateShapes[i])
+    	gateData[#gateData+1] = {shapeBody, Vec(sx/20, 0, 0), Vec(-sx/20, 0, 0)}
+    	if shapeBody == topGate and noMotor then
+    		gateData[#gateData+1] = {shapeBody, Vec(sx/20, sy/10, 0), Vec(-sx/20, sy/10, 0)}
+    	end
+    end
+    leftTrack = {}
+    rightTrack = {}
+    for i=1, 4 do rightTrack[i] = {tracks[i], GetShapeBody(tracks[i])} SetShapeCollisionFilter(tracks[i], 8, 255-8) end
+    for i=1, 4 do leftTrack[i] = {tracks[i+4], GetShapeBody(tracks[i+4])} SetShapeCollisionFilter(tracks[i+4], 8, 255-8) end
+    hold = false
+    holdVal = 0
+    motorBroken = false
+    gateBroken = false
+    ctrlBroken = false
+    soundVelThres = 0.15*speed
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if not haveMotorSnd then return end
+    if noMotor or ctrlBroken then return end
+    local tagValue = GetTagValue(gateCtrl, "gateCtrl")
+    if (tagValue ~= "open") or (tagValue ~= "close") then return end
+    if (moveVal < 1) and (moveVal > 0) then
+    	local min, max = GetShapeBounds(gateCtrl)
+    	local shapeCentre = VecLerp(min, max, 0.5)
+    	PlayLoop(motorSnd, shapeCentre, motorSndVolume)
+    end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if motorBroken and gateBroken and ctrlBroken then return end
+
+    ctrlBroken = ctrlBroken or IsShapeBroken(gateCtrl) or not IsHandleValid(gateCtrl) or ctrlBody ~= GetShapeBody(gateCtrl)
+    if not (noMotor or ctrlBroken) then
+    	local tagValue = GetTagValue(gateCtrl, "gateCtrl")
+    	if tagValue == "open" then
+    		if moveVal < 1 then moveVal = moveVal + speed/600 else moveVal = 1 SetTag(gateCtrl, "gateCtrl", "") end
+    	elseif tagValue == "close" then
+    		if moveVal ~= 0 then moveVal = moveVal - speed/600 else moveVal = 0 SetTag(gateCtrl, "gateCtrl", "") end
+    	end
+    end
+
+    motorBroken = motorBroken or IsShapeBroken(moveShape) or not IsHandleValid(moveShape) or trackBody ~= GetShapeBody(moveShape)
+    if not (motorBroken or noMotor) then
+    	local shapeRot = GetShapeLocalTransform(moveShape).rot
+    	SetShapeLocalTransform(moveShape, Transform(VecLerp(startPos, endPos, moveVal), shapeRot))
+
+    	local pointA = TransformToParentPoint(GetShapeWorldTransform(moveShape), shapePos)
+    	local pointB = TransformToParentPoint(GetBodyTransform(topGate), doorPos)
+    	local _, ckMotorPos = GetBodyClosestPoint(topGate, pointB)
+    	if VecDist(ckMotorPos, pointB) <= 0.2 then
+    		ConstrainPosition(trackBody, topGate, pointA, pointB)
+    	else
+    		motorBroken = true
+    	end
+    end
+
+    gateBroken = #gateData == 0
+    if gateBroken then return end
+
+    for i=1, #gateData do
+    	local locData = gateData[i]
+    	local locBody = locData[1]
+    	local bodyTrans = GetBodyTransform(locBody)
+    	if not gateData[i][4] then
+    		local pointL = TransformToParentPoint(bodyTrans, locData[2])
+    		local _, ckPointL = GetBodyClosestPoint(locBody, pointL)
+    		if VecDist(ckPointL, pointL) <= 0.2 then
+    			local worldVel = GetBodyVelocityAtPos(locBody, pointL)
+    			local locVel = TransformToLocalVec(bodyTrans, worldVel)
+    			local pointVel = VecLength(Vec(0, locVel[2], 0))
+    			if haveGateSnd and pointVel > soundVelThres then PlayLoop(gateSnd, pointL, gateSndVolume*pointVel) end
+    			local checkL = ConstrainTrack(leftTrack, locBody, pointL, Vec(0.05, 0, 0.1))
+    			gateData[i][4] = checkL or gateData[i][4]
+    		else
+    			gateData[i][4] = true
+    		end
+    	end
+    	if not gateData[i][5] then
+    		local pointR = TransformToParentPoint(bodyTrans, locData[3])
+    		local _, ckPointR = GetBodyClosestPoint(locBody, pointR)
+    		if VecDist(ckPointR, pointR) <= 0.2 then
+    			local worldVel = GetBodyVelocityAtPos(locBody, pointR)
+    			local locVel = TransformToLocalVec(bodyTrans, worldVel)
+    			local pointVel = VecLength(Vec(0, locVel[2], 0))
+    			if haveGateSnd and pointVel > soundVelThres then PlayLoop(gateSnd, pointR, gateSndVolume*pointVel) end
+    			local checkR = ConstrainTrack(rightTrack, locBody, pointR, Vec(0.05, 0, 0.1))
+    			gateData[i][5] = checkR or gateData[i][5]
+    		else
+    			gateData[i][5] = true
+    		end
+    	end
+    end
+    for i=#gateData, 1, -1 do
+    	if gateData[i][4] and gateData[i][5] then table.remove(gateData, i) end
+    end
+end
+

```

---

# Migration Report: script\sectionalGateVoxscript.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\sectionalGateVoxscript.lua
+++ patched/script\sectionalGateVoxscript.lua
@@ -1,80 +1,64 @@
-brushFile = GetString("brush", "", "object vox")
-width = GetInt("width", 40)
-height = GetInt("height", 24)
-offset = GetInt("offset", 1)
-gateCount = GetInt("gates", 4)
-noMotorStr = GetString("noMotor", "")
-noMotor = noMotorStr ~= ""
-constc = 0.732
+#version 2
+function server.init()
+    local Mfloor = math.floor
+    local Mceil = math.ceil
+    local Mabs = math.abs
+    width = Mabs(width-1)
+    height = Mabs(height)
+    offset = Mabs(offset)
+    gateCount = gateCount ~= 0 and Mabs(gateCount) or 1
+    gateH = Mceil(height/gateCount)
+    height = gateH*gateCount
+    trackOff = offset-1
+    gateMid = Mceil(width/2)-width%2
+    motorWidth = 2+width%2
+    curveL = Mceil(constc*gateH)+1
+    trackBR = brushFile..":track"
+    -- gatesBR = brushFile..":gates"
+    track = CreateBrush(trackBR, true)
+    -- gates = CreateBrush(gatesBR, true)
+    -- for i=1, gateCount do
+    -- 	Vox(0, gateH*(i-1), 0)
+    -- 	Material(gates)
+    -- 	Box(0, 0, 0, width, gateH, offset)
+    -- end
+    Vox(0, 0, 0)
+    Material(track)
+    Box(0, 0, trackOff, -1, height-gateH, offset)
+    Vox(0, height, gateH+offset, 90, 0, 0)
+    Material(track)
+    Box(0, 0, 0, -1, height+1, -1)
+    Vox(0, height-gateH, offset-1, 30, 0, 0)
+    Material(track)
+    Box(0, 0, 0, -1, curveL, 1)
+    Vox(0, height+1, gateH+trackOff+1, 60, 0, 0)
+    Material(track)
+    Box(0, 0, 0, -1, -curveL, 1)
+    Vox(width, 0, 0)
+    Material(track)
+    Box(0, 0, trackOff, 1, height-gateH, offset)
+    Vox(width, height, gateH+offset, 90, 0, 0)
+    Material(track)
+    Box(0, 0, 0, 1, height+1, -1)
+    Vox(width, height-gateH, offset-1, 30, 0, 0)
+    Material(track)
+    Box(0, 0, 0, 1, curveL, 1)
+    Vox(width, height+1, gateH+trackOff+1, 60, 0, 0)
+    Material(track)
+    Box(0, 0, 0, 1, -curveL, 1)
+    Vox(0, height, height+offset+gateH+2)
+    Material(track)
+    Box(-1, 0, 0, width+1, 1, -1)
+    if not noMotor then
+    	Vox(gateMid, height+offset+1, 0)
+    	Material(track)
+    	Box(-1, 0, 0, motorWidth-1, 1, height+gateH*2+offset)
+    	Vox(gateMid, height+1, offset+height+gateH)
+    	Material(track)
+    	Box(-1, -2, 0, motorWidth-1, offset, 1)
+    	Vox(gateMid, height+1, offset)
+    	Material(track)
+    	Box(-1, -2, 0, motorWidth-1, offset, 1)
+    end
+end
 
-function init()
-	local Mfloor = math.floor
-	local Mceil = math.ceil
-	local Mabs = math.abs
-
-	width = Mabs(width-1)
-	height = Mabs(height)
-	offset = Mabs(offset)
-	gateCount = gateCount ~= 0 and Mabs(gateCount) or 1
-	gateH = Mceil(height/gateCount)
-	height = gateH*gateCount
-
-	trackOff = offset-1
-	gateMid = Mceil(width/2)-width%2
-	motorWidth = 2+width%2
-	curveL = Mceil(constc*gateH)+1
-
-	trackBR = brushFile..":track"
-	-- gatesBR = brushFile..":gates"
-
-	track = CreateBrush(trackBR, true)
-	-- gates = CreateBrush(gatesBR, true)
-
-	-- for i=1, gateCount do
-	-- 	Vox(0, gateH*(i-1), 0)
-	-- 	Material(gates)
-	-- 	Box(0, 0, 0, width, gateH, offset)
-	-- end
-
-	Vox(0, 0, 0)
-	Material(track)
-	Box(0, 0, trackOff, -1, height-gateH, offset)
-	Vox(0, height, gateH+offset, 90, 0, 0)
-	Material(track)
-	Box(0, 0, 0, -1, height+1, -1)
-	Vox(0, height-gateH, offset-1, 30, 0, 0)
-	Material(track)
-	Box(0, 0, 0, -1, curveL, 1)
-	Vox(0, height+1, gateH+trackOff+1, 60, 0, 0)
-	Material(track)
-	Box(0, 0, 0, -1, -curveL, 1)
-
-	Vox(width, 0, 0)
-	Material(track)
-	Box(0, 0, trackOff, 1, height-gateH, offset)
-	Vox(width, height, gateH+offset, 90, 0, 0)
-	Material(track)
-	Box(0, 0, 0, 1, height+1, -1)
-	Vox(width, height-gateH, offset-1, 30, 0, 0)
-	Material(track)
-	Box(0, 0, 0, 1, curveL, 1)
-	Vox(width, height+1, gateH+trackOff+1, 60, 0, 0)
-	Material(track)
-	Box(0, 0, 0, 1, -curveL, 1)
-	
-	Vox(0, height, height+offset+gateH+2)
-	Material(track)
-	Box(-1, 0, 0, width+1, 1, -1)
-
-	if not noMotor then
-		Vox(gateMid, height+offset+1, 0)
-		Material(track)
-		Box(-1, 0, 0, motorWidth-1, 1, height+gateH*2+offset)
-		Vox(gateMid, height+1, offset+height+gateH)
-		Material(track)
-		Box(-1, -2, 0, motorWidth-1, offset, 1)
-		Vox(gateMid, height+1, offset)
-		Material(track)
-		Box(-1, -2, 0, motorWidth-1, offset, 1)
-	end
-end

```

---

# Migration Report: script\speed.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\speed.lua
+++ patched/script\speed.lua
@@ -1,9 +1,11 @@
-function init()
-  local motors = FindJoints("motor",true) -- Find all joints in the level that have tag "motor"
-  for i=1,#motors do -- for every motor do the following
-    local motor = motors[i] --Take value from the motors list and save it as motor
-    local speed = GetTagValue(motor,"speed") -- Get speed number of tag. For example speed=2 would output 2
-    if speed == "" then speed = 0.5 end -- if there is no speed tag the value will be "". We will use 0.5 if that happened
-    SetJointMotor(motor,speed) -- Let the joint spinn
-  end -- repeat loop until we reach end of list of motors
-end+#version 2
+function server.init()
+    local motors = FindJoints("motor",true) -- Find all joints in the level that have tag "motor"
+    for i=1,#motors do -- for every motor do the following
+      local motor = motors[i] --Take value from the motors list and save it as motor
+      local speed = GetTagValue(motor,"speed") -- Get speed number of tag. For example speed=2 would output 2
+      if speed == "" then speed = 0.5 end -- if there is no speed tag the value will be "". We will use 0.5 if that happened
+      SetJointMotor(motor,speed) -- Let the joint spinn
+    end -- repeat loop until we reach end of list of motors
+end
+

```

---

# Migration Report: script\vehicleAI-old.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\vehicleAI-old.lua
+++ patched/script\vehicleAI-old.lua
@@ -1,45 +1,4 @@
-
-
-
-MAX_THINK_TIME = 1.0
-MIN_COOLDOWN_TIME = 0.1
-
-
-function init()
-	AIvehicle = FindVehicle(nil, false)
-    clearance = GetFloatParam("clearance", 0.6)
-    length = GetFloatParam("length", 4.6)
-    width = GetFloatParam("width", 2)
-	
-
-
-    minDist = 5
-	lastPath = {}
-    vehiclePath = {}
-    coolDown = 0
-    sleep = false
-    neverDriven = true
-    count = 0
-    countMax = 2
-
-    speedLimit = 0
-
-    front = {}
-    front.hit = {}
-    front.dist = {}
-    front.normal = {}
-    front.shape = {}
-
-    back = {}
-    back.hit = {}
-    back.dist = {}
-    back.normal = {}
-    back.shape = {}
-    
-    SetTag(AIvehicle, "DestAI", 0)
-end
-
-
+#version 2
 function retrievePath()
 	local path = {}
 	local length = GetPathLength()
@@ -68,276 +27,6 @@
     return route
 end
 
-
-function tick(dt)
-
-    if GetPlayerVehicle() ~= AIvehicle or neverDriven then
-
-        local recalc = false
-        local state = GetPathState()
-        local AIactive = true
-
-        if state == "idle" then
-            
-            recalc = true
-
-        elseif state == "done" or state == "fail" then
-
-            if state == "fail" then AIactive = true end
-
-            if sleep then
-                if coolDown > MAX_THINK_TIME then
-                    recalc = true
-                    failed = false
-                    coolDown = 0
-                else
-                    if lastPath ~= {} then
-                        lastPath = retrievePath()
-                        vehiclePath = routeCalc(0.2)
-                    end
-                    coolDown = coolDown + dt
-                end
-            else
-                if coolDown > MIN_COOLDOWN_TIME then
-                    recalc = true
-                    failed = false
-                    coolDown = 0
-                else
-                    if lastPath ~= {} then
-                        lastPath = retrievePath()
-                        vehiclePath = routeCalc(0.2)
-                    end
-                    coolDown = coolDown + dt
-                end
-            end
-
-        else
-            
-            thinkTime = thinkTime + dt
-
-            if thinkTime > MAX_THINK_TIME then
-                AbortPath()
-                recalc = true
-                failed = true
-                lastPath = retrievePath()
-                vehiclePath = routeCalc(0.2)
-            end
-
-            AIactive = true
-
-        end
-
-        vehicleTrans = GetVehicleTransform(AIvehicle)
-        vehicleSpeed = -TransformToLocalVec(vehicleTrans, GetBodyVelocity(GetVehicleBody(AIvehicle)))[3]
-
-        if recalc then
-
-            count = count + 1
-            sleep = false
-
-            SetTag(AIvehicle, "DestAI", 0)
-
-            DestLoc = FindLocation(nil, false)
-            goalPos = GetLocationTransform(DestLoc).pos
-            speedLimit = tonumber(GetTagValue(DestLoc, "SpeedLimit")) or 0
-
-            --goalPos = GetPlayerPos()
-
-            vehiclePos = VecAdd(vehicleTrans.pos, TransformToParentVec(vehicleTrans, Vec(0, clearance, -length*0.5)))
-            vehicleReversePos = VecAdd(vehicleTrans.pos, TransformToParentVec(vehicleTrans, Vec(0, clearance, length*0.5)))
-
-            if VecLength(VecSub(goalPos, vehiclePos)) <= math.max(vehicleSpeed, 2.5*minDist) then
-                Delete(DestLoc)
-                DestLoc = FindLocation(nil, false)
-                goalPos = GetLocationTransform(DestLoc).pos
-            end
-
-            if DestLoc == 0 then
-                goalPos = vehiclePos
-
-                local shapes = FindShapes("Ysiren", false)
-                for i=1, #shapes do
-                    RemoveTag(shapes[i], "Ysiren")
-                end
-            end
-
-            if count == countMax then
-                
-                QueryRejectVehicle(AIvehicle)
-                QueryPath(vehiclePos, goalPos, 1000, minDist)
-
-                thinkTime = 0
-                count = 0
-
-            elseif not (VecLength(VecSub(goalPos, vehiclePos)) <= minDist*2 and math.abs(vehicleSpeed) < 0.01 ) then
-            
-                local frVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.3, clearance, 0)))
-                local flVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.3, clearance, 0)))
-                local brVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.3, clearance, length)))
-                local blVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.3, clearance, length)))
-            
-                local frontDist = -math.max(4, length*0.5) - math.max(0, vehicleSpeed)*0.4
-                local reverseDist = math.max(4, length*1.5) - math.min(0, vehicleSpeed)*0.4
-                
-                local frDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.7, clearance, frontDist)))
-                local flDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.7, clearance, frontDist)))
-                local brDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.7, clearance, reverseDist)))
-                local blDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.7, clearance, reverseDist)))
-                local downVec1 = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(0, -1, 0)))
-                local downVec2 = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(0, -1, length)))
-        
-                local frDirection = VecNormalize(VecSub(frDireVec, frVec))
-                local flDirection = VecNormalize(VecSub(flDireVec, flVec))
-                local brDirection = VecNormalize(VecSub(brDireVec, brVec))
-                local blDirection = VecNormalize(VecSub(blDireVec, blVec))
-                local downDirection1 = VecNormalize(VecSub(downVec1, vehiclePos))
-                local downDirection2 = VecNormalize(VecSub(downVec2, vehiclePos))
-
-                local frontCheck = math.max(width*0.5, vehicleSpeed)
-                local reverseCheck = math.min(width*0.5, math.max(0.3, -vehicleSpeed*0.4))
-                local checkRadius = math.min(clearance, width*0.5)
-
-                local down = {}
-                down.hit = {}
-                down.dist = {}
-                down.normal = {}
-                down.shape = {}
-
-                QueryRequire("large")
-                QueryRejectVehicle(AIvehicle)
-                down.hit[1], down.dist[1], down.normal, down.shape[1] = QueryRaycast(vehiclePos, downDirection1, clearance*1.5)
-                
-                QueryRequire("large")
-                QueryRejectVehicle(AIvehicle)
-                down.hit[2], down.dist[2], down.normal, down.shape[2] = QueryRaycast(vehicleReversePos, downDirection2, clearance*1.5)
-        
-                QueryRequire("large")
-                QueryRejectVehicle(AIvehicle)
-                QueryRejectShape(down.shape[1])
-                QueryRejectShape(down.shape[2])
-                front.hit[1], front.dist[1], front.normal, front.shape[1] = QueryRaycast(frVec, frDirection, frontCheck, checkRadius)
-                
-                QueryRequire("large")
-                QueryRejectVehicle(AIvehicle)
-                QueryRejectShape(down.shape[1])
-                QueryRejectShape(down.shape[2])
-                front.hit[2], front.dist[2], front.normal, front.shape[2] = QueryRaycast(flVec, flDirection, frontCheck, checkRadius)
-
-                QueryRequire("large")
-                QueryRejectVehicle(AIvehicle)
-                QueryRejectShape(down.shape[1])
-                QueryRejectShape(down.shape[2])
-                back.hit[1], back.dist[1], back.normal, back.shape[1] = QueryRaycast(brVec, brDirection, reverseCheck, checkRadius)
-
-                QueryRequire("large")
-                QueryRejectVehicle(AIvehicle)
-                QueryRejectShape(down.shape[1])
-                QueryRejectShape(down.shape[2])
-                back.hit[2], back.dist[2], back.normal, back.shape[2] = QueryRaycast(blVec, blDirection, reverseCheck, checkRadius)
-            else
-                sleep = true
-            end
-
-        end
-
-        --drawPath(lastPath)
-
-        currentDest = tonumber(GetTagValue(AIvehicle, "DestAI"))
-
-        if currentDest == 0 then
-            currentDest = math.min(5, #vehiclePath)
-        end
-
-        local destDist = VecLength(VecSub(vehiclePath[#vehiclePath], vehiclePos))
-        local direDist = VecLength(VecSub(vehiclePath[currentDest], vehiclePos))
-
-        local THdist = length + math.max(1, 0.5*vehicleSpeed)
-
-        if direDist < THdist then
-            currentDest = math.min(currentDest+1, #vehiclePath)
-        end
-
-        SetTag(AIvehicle, "DestAI", currentDest)
-
-        local LocDirection = TransformToLocalVec(vehicleTrans, VecNormalize(VecSub(vehiclePath[currentDest], vehiclePos)))
-        local LocFinal = TransformToLocalVec(vehicleTrans, VecNormalize(VecSub(vehiclePath[#vehiclePath], vehiclePos)))
-        local direction = Vec(-LocDirection[1], LocDirection[2], -LocDirection[3])
-        local final = Vec(-LocFinal[1], LocFinal[2], -LocFinal[3])
-
-        braking = false
-
-        if AIactive then
-            if destDist >= 3*length then
-
-                throttle = math.max(0.1, math.abs(destDist/vehicleSpeed))
-                steering = direction[1]
-
-                if math.abs(direction[1]) < 0.1 and direction[3] < 0 then
-                    steering = direction[1]*20
-                    throttle = destDist/2*vehicleSpeed
-                elseif direction[1]*direction[1] > 0.64 then
-                    throttle = math.max(0.3, destDist/5*vehicleSpeed)
-                end
-
-                throttle, braking, steering = AIcontrol(front, back, vehicleSpeed, throttle, braking, steering)
-
-                if math.abs(steering) > 0.7 and vehicleSpeed > 10 then throttle = 0 end
-                if destDist < direDist*10 then throttle = 0.1*throttle end
-
-                if speedLimit > 0 then
-                    if vehicleSpeed > speedLimit then
-                        throttle = 0
-                    end
-                end
-
-                DriveVehicle(AIvehicle, throttle, steering, braking)
-
-            elseif destDist >= length then
-
-                throttle = final[3]*destDist/vehicleSpeed*1.5
-                steering = final[1]
-
-                if math.abs(final[1]) < 0.1 and final[3] < 0 then
-                    steering = final[1]*20
-                    throttle = destDist/2*vehicleSpeed
-                elseif final[1]*final[1] > 0.64 then
-                    throttle = math.max(0.3, destDist/5*vehicleSpeed)
-                end
-
-                throttle, braking, steering = AIcontrol(front, back, vehicleSpeed, throttle, braking, steering)
-
-                if vehicleSpeed > 10 then throttle = math.max(0.1, 1-math.abs(steering)) end
-                if destDist < direDist*10 then throttle = 0.2*throttle end
-
-                if speedLimit > 0 then
-                    if vehicleSpeed > speedLimit then
-                        throttle = 0
-                    end
-                end
-
-                DriveVehicle(AIvehicle, throttle, steering, braking)
-
-            else
-                SetTag(AIvehicle, "DestAI", math.min(currentDest+1, #vehiclePath))
-                DriveVehicle(AIvehicle, 0, 0, false)
-            end
-        else
-            throttle, braking, steering = AIcontrol(front, back, vehicleSpeed, 0, braking, steering)
-
-            if speedLimit > 0 then
-                if vehicleSpeed > speedLimit then
-                    throttle = 0
-                end
-            end
-
-            DriveVehicle(AIvehicle, throttle, steering, braking)
-        end
-    else
-        neverDriven = false
-    end
-end
-
-
 function drawPath(path)
 	for i=1, #path-1 do
         if math.fmod(i, 2) == 1 then
@@ -346,14 +35,13 @@
 	end
 end
 
-
 function AIcontrol(front, back, speed, throttle, braking, steering)
 
     if speed >= 0 then
 
         if front.hit[1] and front.hit[2] then
             throttle = -1
-            if speed > 0 then
+            if speed ~= 0 then
                 braking = true
             end
         elseif front.hit[1] then
@@ -397,3 +85,299 @@
     return throttle, braking, steering
 end
 
+function server.init()
+    AIvehicle = FindVehicle(nil, false)
+       clearance = GetFloatParam("clearance", 0.6)
+       length = GetFloatParam("length", 4.6)
+       width = GetFloatParam("width", 2)
+       minDist = 5
+    lastPath = {}
+       vehiclePath = {}
+       coolDown = 0
+       sleep = false
+       neverDriven = true
+       count = 0
+       countMax = 2
+       speedLimit = 0
+       front = {}
+       front.hit = {}
+       front.dist = {}
+       front.normal = {}
+       front.shape = {}
+       back = {}
+       back.hit = {}
+       back.dist = {}
+       back.normal = {}
+       back.shape = {}
+       SetTag(AIvehicle, "DestAI", 0)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) ~= AIvehicle or neverDriven then
+
+            local recalc = false
+            local state = GetPathState()
+            local AIactive = true
+
+            if state == "idle" then
+
+                recalc = true
+
+            elseif state == "done" or state == "fail" then
+
+                if state == "fail" then AIactive = true end
+
+                if sleep then
+                    if coolDown > MAX_THINK_TIME then
+                        recalc = true
+                        failed = false
+                        coolDown = 0
+                    else
+                        if lastPath ~= {} then
+                            lastPath = retrievePath()
+                            vehiclePath = routeCalc(0.2)
+                        end
+                        coolDown = coolDown + dt
+                    end
+                else
+                    if coolDown > MIN_COOLDOWN_TIME then
+                        recalc = true
+                        failed = false
+                        coolDown = 0
+                    else
+                        if lastPath ~= {} then
+                            lastPath = retrievePath()
+                            vehiclePath = routeCalc(0.2)
+                        end
+                        coolDown = coolDown + dt
+                    end
+                end
+
+            else
+
+                thinkTime = thinkTime + dt
+
+                if thinkTime > MAX_THINK_TIME then
+                    AbortPath()
+                    recalc = true
+                    failed = true
+                    lastPath = retrievePath()
+                    vehiclePath = routeCalc(0.2)
+                end
+
+                AIactive = true
+
+            end
+
+            vehicleTrans = GetVehicleTransform(AIvehicle)
+            vehicleSpeed = -TransformToLocalVec(vehicleTrans, GetBodyVelocity(GetVehicleBody(AIvehicle)))[3]
+
+            if recalc then
+
+                count = count + 1
+                sleep = false
+
+                SetTag(AIvehicle, "DestAI", 0)
+
+                DestLoc = FindLocation(nil, false)
+                goalPos = GetLocationTransform(DestLoc).pos
+                speedLimit = tonumber(GetTagValue(DestLoc, "SpeedLimit")) or 0
+
+                --goalPos = GetPlayerPos(playerId)
+
+                vehiclePos = VecAdd(vehicleTrans.pos, TransformToParentVec(vehicleTrans, Vec(0, clearance, -length*0.5)))
+                vehicleReversePos = VecAdd(vehicleTrans.pos, TransformToParentVec(vehicleTrans, Vec(0, clearance, length*0.5)))
+
+                if VecLength(VecSub(goalPos, vehiclePos)) <= math.max(vehicleSpeed, 2.5*minDist) then
+                    Delete(DestLoc)
+                    DestLoc = FindLocation(nil, false)
+                    goalPos = GetLocationTransform(DestLoc).pos
+                end
+
+                if DestLoc == 0 then
+                    goalPos = vehiclePos
+
+                    local shapes = FindShapes("Ysiren", false)
+                    for i=1, #shapes do
+                        RemoveTag(shapes[i], "Ysiren")
+                    end
+                end
+
+                if count == countMax then
+
+                    QueryRejectVehicle(AIvehicle)
+                    QueryPath(vehiclePos, goalPos, 1000, minDist)
+
+                    thinkTime = 0
+                    count = 0
+
+                elseif not (VecLength(VecSub(goalPos, vehiclePos)) <= minDist*2 and math.abs(vehicleSpeed) < 0.01 ) then
+
+                    local frVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.3, clearance, 0)))
+                    local flVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.3, clearance, 0)))
+                    local brVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.3, clearance, length)))
+                    local blVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.3, clearance, length)))
+
+                    local frontDist = -math.max(4, length*0.5) - math.max(0, vehicleSpeed)*0.4
+                    local reverseDist = math.max(4, length*1.5) - math.min(0, vehicleSpeed)*0.4
+
+                    local frDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.7, clearance, frontDist)))
+                    local flDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.7, clearance, frontDist)))
+                    local brDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(width*0.7, clearance, reverseDist)))
+                    local blDireVec = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(-width*0.7, clearance, reverseDist)))
+                    local downVec1 = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(0, -1, 0)))
+                    local downVec2 = VecAdd(vehiclePos, TransformToParentVec(vehicleTrans, Vec(0, -1, length)))
+
+                    local frDirection = VecNormalize(VecSub(frDireVec, frVec))
+                    local flDirection = VecNormalize(VecSub(flDireVec, flVec))
+                    local brDirection = VecNormalize(VecSub(brDireVec, brVec))
+                    local blDirection = VecNormalize(VecSub(blDireVec, blVec))
+                    local downDirection1 = VecNormalize(VecSub(downVec1, vehiclePos))
+                    local downDirection2 = VecNormalize(VecSub(downVec2, vehiclePos))
+
+                    local frontCheck = math.max(width*0.5, vehicleSpeed)
+                    local reverseCheck = math.min(width*0.5, math.max(0.3, -vehicleSpeed*0.4))
+                    local checkRadius = math.min(clearance, width*0.5)
+
+                    local down = {}
+                    down.hit = {}
+                    down.dist = {}
+                    down.normal = {}
+                    down.shape = {}
+
+                    QueryRequire("large")
+                    QueryRejectVehicle(AIvehicle)
+                    down.hit[1], down.dist[1], down.normal, down.shape[1] = QueryRaycast(vehiclePos, downDirection1, clearance*1.5)
+
+                    QueryRequire("large")
+                    QueryRejectVehicle(AIvehicle)
+                    down.hit[2], down.dist[2], down.normal, down.shape[2] = QueryRaycast(vehicleReversePos, downDirection2, clearance*1.5)
+
+                    QueryRequire("large")
+                    QueryRejectVehicle(AIvehicle)
+                    QueryRejectShape(down.shape[1])
+                    QueryRejectShape(down.shape[2])
+                    front.hit[1], front.dist[1], front.normal, front.shape[1] = QueryRaycast(frVec, frDirection, frontCheck, checkRadius)
+
+                    QueryRequire("large")
+                    QueryRejectVehicle(AIvehicle)
+                    QueryRejectShape(down.shape[1])
+                    QueryRejectShape(down.shape[2])
+                    front.hit[2], front.dist[2], front.normal, front.shape[2] = QueryRaycast(flVec, flDirection, frontCheck, checkRadius)
+
+                    QueryRequire("large")
+                    QueryRejectVehicle(AIvehicle)
+                    QueryRejectShape(down.shape[1])
+                    QueryRejectShape(down.shape[2])
+                    back.hit[1], back.dist[1], back.normal, back.shape[1] = QueryRaycast(brVec, brDirection, reverseCheck, checkRadius)
+
+                    QueryRequire("large")
+                    QueryRejectVehicle(AIvehicle)
+                    QueryRejectShape(down.shape[1])
+                    QueryRejectShape(down.shape[2])
+                    back.hit[2], back.dist[2], back.normal, back.shape[2] = QueryRaycast(blVec, blDirection, reverseCheck, checkRadius)
+                else
+                    sleep = true
+                end
+
+            end
+
+            --drawPath(lastPath)
+
+            currentDest = tonumber(GetTagValue(AIvehicle, "DestAI"))
+
+            if currentDest == 0 then
+                currentDest = math.min(5, #vehiclePath)
+            end
+
+            local destDist = VecLength(VecSub(vehiclePath[#vehiclePath], vehiclePos))
+            local direDist = VecLength(VecSub(vehiclePath[currentDest], vehiclePos))
+
+            local THdist = length + math.max(1, 0.5*vehicleSpeed)
+
+            if direDist < THdist then
+                currentDest = math.min(currentDest+1, #vehiclePath)
+            end
+
+            SetTag(AIvehicle, "DestAI", currentDest)
+
+            local LocDirection = TransformToLocalVec(vehicleTrans, VecNormalize(VecSub(vehiclePath[currentDest], vehiclePos)))
+            local LocFinal = TransformToLocalVec(vehicleTrans, VecNormalize(VecSub(vehiclePath[#vehiclePath], vehiclePos)))
+            local direction = Vec(-LocDirection[1], LocDirection[2], -LocDirection[3])
+            local final = Vec(-LocFinal[1], LocFinal[2], -LocFinal[3])
+
+            braking = false
+
+            if AIactive then
+                if destDist >= 3*length then
+
+                    throttle = math.max(0.1, math.abs(destDist/vehicleSpeed))
+                    steering = direction[1]
+
+                    if math.abs(direction[1]) < 0.1 and direction[3] < 0 then
+                        steering = direction[1]*20
+                        throttle = destDist/2*vehicleSpeed
+                    elseif direction[1]*direction[1] > 0.64 then
+                        throttle = math.max(0.3, destDist/5*vehicleSpeed)
+                    end
+
+                    throttle, braking, steering = AIcontrol(front, back, vehicleSpeed, throttle, braking, steering)
+
+                    if math.abs(steering) > 0.7 and vehicleSpeed > 10 then throttle = 0 end
+                    if destDist < direDist*10 then throttle = 0.1*throttle end
+
+                    if speedLimit ~= 0 then
+                        if vehicleSpeed > speedLimit then
+                            throttle = 0
+                        end
+                    end
+
+                    DriveVehicle(AIvehicle, throttle, steering, braking)
+
+                elseif destDist >= length then
+
+                    throttle = final[3]*destDist/vehicleSpeed*1.5
+                    steering = final[1]
+
+                    if math.abs(final[1]) < 0.1 and final[3] < 0 then
+                        steering = final[1]*20
+                        throttle = destDist/2*vehicleSpeed
+                    elseif final[1]*final[1] > 0.64 then
+                        throttle = math.max(0.3, destDist/5*vehicleSpeed)
+                    end
+
+                    throttle, braking, steering = AIcontrol(front, back, vehicleSpeed, throttle, braking, steering)
+
+                    if vehicleSpeed > 10 then throttle = math.max(0.1, 1-math.abs(steering)) end
+                    if destDist < direDist*10 then throttle = 0.2*throttle end
+
+                    if speedLimit ~= 0 then
+                        if vehicleSpeed > speedLimit then
+                            throttle = 0
+                        end
+                    end
+
+                    DriveVehicle(AIvehicle, throttle, steering, braking)
+
+                else
+                    SetTag(AIvehicle, "DestAI", math.min(currentDest+1, #vehiclePath))
+                    DriveVehicle(AIvehicle, 0, 0, false)
+                end
+            else
+                throttle, braking, steering = AIcontrol(front, back, vehicleSpeed, 0, braking, steering)
+
+                if speedLimit ~= 0 then
+                    if vehicleSpeed > speedLimit then
+                        throttle = 0
+                    end
+                end
+
+                DriveVehicle(AIvehicle, throttle, steering, braking)
+            end
+        else
+            neverDriven = false
+        end
+    end
+end
+

```

---

# Migration Report: script\vehicleAI.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\vehicleAI.lua
+++ patched/script\vehicleAI.lua
@@ -1,133 +1,4 @@
---Written by: GGProGaming
-
-detectRange = 5--2.5--3
-VEHICLE_ACTIVE = true
-vehicle = {}
-maxSpeed = 20
-goalOrigPos = Vec(0,0,0) 
-goalPos = 	goalOrigPos
-SPOTMARKED = false
-gCost = 1
-testHeight = 5
-drivePower = 3
-detectPoints = {
-	[1] = Vec(0,0,-detectRange),
-	[2] = Vec(detectRange,0,-detectRange),
-	[3] = Vec(-detectRange,0,-detectRange),
-	[4] = Vec(-detectRange,0,0),
-	[5] = Vec(detectRange,0,0),
-	[6] = Vec(0,0,detectRange),
-}
-weights = {
-	[1] = 0.85,
-	[2] = 0.85,
-	[3] = 0.85,
-	[4] = 0.5,
-	[5] = 0.5,
-	[6] = 0.25,
-}
-ai = {
-	commands = {
-	[1] = Vec(0,0,-detectRange*4),
-	[2] = Vec(detectRange*1.5,0,-detectRange*2.5),
-	[3] = Vec(-detectRange*1.5,0,-detectRange*2.5),
-	[4] = Vec(-detectRange,0,0),
-	[5] = Vec(detectRange,0,0),
-	[6] = Vec(0,0,detectRange),
-	},
-	weights = {
-	[1] = 0.860,
-	[2] = 0.85,
-	[3] = 0.85,
-	[4] = 0.8,
-	[5] = 0.8,
-	[6] = 0.7,
-			} ,
-	directions = {
-		forward = Vec(0,0,1),
-		back = Vec(0,0,-1),
-		left = Vec(1,0,0),
-		right = Vec(-1,0,0),
-	},
-	numScans = 7,
-	scanThreshold = 0.5,
-	--altChecks = Vec(0.25,0.4,-0.6),
-	altChecks = {
-				[1] = -2,
-				[2] =0.2,
-				[3] = 0.4
-			},
-	altWeight ={
-			[1] = 1,
-			[2] =1,
-			[3] = -1,
-			[4] = -1,
-	},
-}
-targetMoves = {
-	list        = {},
-	target      = Vec(0,0,0),
-	targetIndex = 1
-}
-scan = 0
-scanCount = 5
-hitColour = Vec(1,0,0)
-detectColour = Vec(1,1,0)
-clearColour = Vec(0,1,0)
-RACESTARTED = false
-raceCheckpoint = 1
-currentCheckpoint = nil
-RESETMAX = 1
-resetTimer = RESETMAX 
-function init()
-	for i=1,10 do 
-		targetMoves.list[i] = Vec(0,0,0)
-	end
-	for i = 1,#ai.commands*1 do 
-		detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
-		if(i> #ai.commands) then
-			detectPoints[i] = VecScale(detectPoints[i],0.5)
-			detectPoints[i][2] = ai.altChecks[2]
-		else 
-			detectPoints[i][2] = ai.altChecks[1]
-		end
-		weights[i] = ai.weights[(i%#ai.commands)+1]--*ai.altWeight[math.floor(i/#ai.commands)+1]
-	end
-	vehicle.id = FindVehicle("cfg")
-	local value = GetTagValue(vehicle.id, "cfg")
-	checkpoints = FindTriggers("checkpoint",true)
-	for key,value in ipairs(checkpoints) do
-		if(tonumber(GetTagValue(value, "checkpoint"))==raceCheckpoint) then 
-			currentCheckpoint = value
-		end
-	end
-end
--- Improved cost system and pathfinding
-function tick(dt)
-    markLoc()
-    ripUpdate()
-    if RACESTARTED and VEHICLE_ACTIVE then
-        local targetCost = vehicleDetection5()
-        targetCost.target = MAV(targetCost.target)
-        controlVehicle(targetCost)
-        local vehiclePos = GetVehicleTransform(vehicle.id).pos
-        local distToGoal = VecLength(VecSub(vehiclePos, goalPos))
-        if distToGoal < 2 then
-            raceCheckpoint = (raceCheckpoint % #checkpoints) + 1
-            for key, value in ipairs(checkpoints) do
-                if tonumber(GetTagValue(value, "checkpoint")) == raceCheckpoint then
-                    currentCheckpoint = value
-					goalOrigPos = GetTriggerTransform(currentCheckpoint).pos
-					goalPos = goalOrigPos
-				end
-			end
-		end
-
-	end
-	if VEHICLE_ACTIVE and (GetVehicleHealth(vehicle.id) < 0.1 or IsPointInWater(GetVehicleTransform(vehicle.id).pos)) then
-		VEHICLE_ACTIVE = false
-	end
-end
+#version 2
 function markLoc()
 	if GetTime() <= 5 then
 		RACESTARTED = true
@@ -152,7 +23,6 @@
 	end
 end
 
--- Improved reset mechanism
 function ripUpdate()
 	if RACESTARTED and VEHICLE_ACTIVE and VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id))) < 1 then
 	resetTimer = resetTimer - 1
@@ -181,7 +51,6 @@
 	return cost
 end
 
--- Improved collision detection with 8 rays
 function vehicleDetection5()
     local vehicleBody = GetVehicleBody(vehicle.id)
     local vehicleTransform = GetVehicleTransform(vehicle.id)
@@ -219,7 +88,6 @@
     return bestCost
 end
 
--- Improved vehicle movement based on collision detection
 function controlVehicle(targetCost)
     local targetMove = VecNormalize(targetCost.target)
     local drivePower = 3
@@ -228,7 +96,6 @@
     DriveVehicle(vehicle.id, throttle * drivePower, steer, false)
 end
 
--- Improved pathfinding using Moving Average Vector (MAV)
 function MAV(targetCost)
 	targetMoves.targetIndex = (targetMoves.targetIndex % #targetMoves.list) + 1
 	targetMoves.target = VecSub(targetMoves.target, targetMoves.list[targetMoves.targetIndex])
@@ -241,6 +108,7 @@
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
+
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -254,4 +122,57 @@
         copy = orig
     end
     return copy
-end+end
+
+function server.init()
+    for i=1,10 do 
+    	targetMoves.list[i] = Vec(0,0,0)
+    end
+    for i = 1,#ai.commands*1 do 
+    	detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
+    	if(i> #ai.commands) then
+    		detectPoints[i] = VecScale(detectPoints[i],0.5)
+    		detectPoints[i][2] = ai.altChecks[2]
+    	else 
+    		detectPoints[i][2] = ai.altChecks[1]
+    	end
+    	weights[i] = ai.weights[(i%#ai.commands)+1]--*ai.altWeight[math.floor(i/#ai.commands)+1]
+    end
+    vehicle.id = FindVehicle("cfg")
+    local value = GetTagValue(vehicle.id, "cfg")
+    checkpoints = FindTriggers("checkpoint",true)
+    for key,value in ipairs(checkpoints) do
+    	if(tonumber(GetTagValue(value, "checkpoint"))==raceCheckpoint) then 
+    		currentCheckpoint = value
+    	end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           markLoc()
+           ripUpdate()
+           if RACESTARTED and VEHICLE_ACTIVE then
+               local targetCost = vehicleDetection5()
+               targetCost.target = MAV(targetCost.target)
+               controlVehicle(targetCost)
+               local vehiclePos = GetVehicleTransform(vehicle.id).pos
+               local distToGoal = VecLength(VecSub(vehiclePos, goalPos))
+               if distToGoal < 2 then
+                   raceCheckpoint = (raceCheckpoint % #checkpoints) + 1
+                   for key, value in ipairs(checkpoints) do
+                       if tonumber(GetTagValue(value, "checkpoint")) == raceCheckpoint then
+                           currentCheckpoint = value
+        				goalOrigPos = GetTriggerTransform(currentCheckpoint).pos
+        				goalPos = goalOrigPos
+        			end
+        		end
+        	end
+
+        end
+        if VEHICLE_ACTIVE and (GetVehicleHealth(vehicle.id) < 0.1 or IsPointInWater(GetVehicleTransform(vehicle.id).pos)) then
+        	VEHICLE_ACTIVE = false
+        end
+    end
+end
+

```

---

# Migration Report: script\windfarm.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\windfarm.lua
+++ patched/script\windfarm.lua
@@ -1,12 +1,15 @@
-function init()
-	hinge = FindJoint("hinge")
-	hinge2 = FindJoint("hinge2")
-	hinge3 = FindJoint("hinge3")
+#version 2
+function server.init()
+    hinge = FindJoint("hinge")
+    hinge2 = FindJoint("hinge2")
+    hinge3 = FindJoint("hinge3")
 end
 
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetJointMotor(hinge, 0.7)
+        SetJointMotor(hinge2, 0.6)
+        SetJointMotor(hinge3, 0.5)
+    end
+end
 
-function update(dt)
-	SetJointMotor(hinge, 0.7)
-	SetJointMotor(hinge2, 0.6)
-	SetJointMotor(hinge3, 0.5)
-end

```

---

# Migration Report: scripts\ALS.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ALS.lua
+++ patched/scripts\ALS.lua
@@ -1,12 +1,11 @@
-#include "ALSlibrary.lua"
-
-function init()
-    --DebugPrint("text")
-    --normal lights
+#version 2
+function server.init()
     lightShapes = FindShapes("ALSlight")
     ALSVehicle = FindVehicle("ALS")
-
     --turn all the lights off when spawned
+end
+
+function client.init()
     for i = 1, #lightShapes do SetShapeEmissiveScale(lightShapes[i], 0) end
 
     currentKmh = 0
@@ -89,17 +88,12 @@
             ter = {5,5,4,5,4,5,2,5,5}
             SetTag(ALSVehicle, "ter", string.format("%02d", ter[1])..string.format("%02d", ter[2])..string.format("%02d", ter[3])..string.format("%02d", ter[4])..string.format("%02d", ter[5])..string.format("%02d", ter[6])..string.format("%02d", ter[7])..string.format("%02d", ter[8])..string.format("%02d", ter[9]))
         end
-        
+
     end
 end
 
-
---fix the lights so call the function only one time when changing mode
---every time it calls clean the normal lights not the emergency lights
---only clean the emergency lights when turned off
---call every update if it has an animation (blinkers and emergency lights)
-function update(dt)
-
+function client.update(dt)
+    local playerId = GetLocalPlayer()
     if not destroyed and GetBool("level.ALS.enabled") then
             blinker = HasTag(ALSVehicle, "p")
             di = GetTagValue(ALSVehicle, "p") == "1"
@@ -111,8 +105,7 @@
             fadm = HasTag(ALSVehicle, "fa")
             ad = HasTag(ALSVehicle, "ad")
 
-
-            if GetPlayerVehicle() == ALSVehicle then
+            if GetPlayerVehicle(playerId) == ALSVehicle then
                 brake = InputDown("down")
                 brake2 = InputDown("up")
                 brake3= InputDown("handbrake")
@@ -142,8 +135,6 @@
                 brake2=false
                 brake3=false
             end
-
-            
 
             --emergency lights
             if HasTag(ALSVehicle, "emergency") then
@@ -198,10 +189,9 @@
                         }
                         RemoveTag(ALSVehicle, "update")
                     end
-                        
 
                     lightsOptions()
-                    
+
                     frame = frame + dt*60
                     local period = 120
                     local t = math.ceil(frame) % period
@@ -210,7 +200,7 @@
                         frame = 0
                     end
                 end
-        
+
                 if  HasTag(ALSVehicle, "GF") then
                     giroflexemergencia()
                 end
@@ -230,7 +220,6 @@
                     SetShapeEmissiveScale(lightShapes[i], 0)
                 end
         end
-
 
             --normal lights
             --fix this call only one time when changing mode
@@ -247,14 +236,12 @@
                     NormalLights() 
                 end
             end
-            
+
             --pop up headlights
             --call one time when turning lights on and off
             if HasTag(ALSVehicle, "UP") then
                     popupheadlights()
             end
-
-
 
         --if the life reach 0
         if GetVehicleHealth(ALSVehicle) == 0 then
@@ -278,3 +265,4 @@
         end
     end
 end
+

```

---

# Migration Report: scripts\ALSlibrary.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ALSlibrary.lua
+++ patched/scripts\ALSlibrary.lua
@@ -1,3 +1,4 @@
+#version 2
 function LightShapeUpdate(lightShapes, shapelight, LightIntensity)
     SetShapeEmissiveScale(lightShapes, shapelight)
     for j = 1, #lights do
@@ -20,12 +21,11 @@
     end
 end
 
---normal lights
 function NormalLights(time)
     --if inside the vehicle
-    if GetPlayerVehicle() == ALSVehicle then
+    if GetPlayerVehicle(playerId) == ALSVehicle then
         --vehicle velocity
-        local v = GetPlayerVehicle()
+        local v = GetPlayerVehicle(playerId)
         if v ~= 0 then
             local b = GetVehicleBody(v)
             local t = GetVehicleTransform(v)
@@ -230,7 +230,6 @@
                     LightShapeUpdate(lightShapes[i], 0.4, GetFloat("lightst")/50)
                 end
 
-
             elseif typeValue == "5" then
                 --acender pisca da dipry[9]ta
                 if tagValue == "LFN_R" and di or alerta then
@@ -297,8 +296,6 @@
         end
     end
 end
-
-
 
 function popupheadlights()
     for i = 1, #lightShapes do
@@ -602,7 +599,6 @@
     end
 end
 
---fix this
 function giroflexemergencia()
     for i = 1, #GiroflexLight do
         tagValue = GetTagValue(GiroflexLight[i], "ALSGF")
@@ -629,43 +625,12 @@
     end
 end
 
-function draw()
-    if not close then
-        if GetBool("level.ALS.enabled") and not close then
-            close=true
-        end
-    if GetPlayerVehicle() == ALSVehicle then
-        if InputPressed("esc")then
-            close=true
-        end
-            SetBool("game.disablepause", true)
-        UiPush()
-            local w = UiWidth()
-            local h = UiHeight()
-            UiTranslate(w-20, h/1.5)
-            UiAlign("right bottom")
-            UiImage("MOD/images/missing.png")
-            UiFont("regular.ttf", 20)
-            UiWordWrap(250)
-            UiTranslate(-5, 0)
-            UiText("Press (ESC) to hide this message")
-            UiTranslate(0, -60)
-            UiText("Please make sure that you have Advanced light system installed and enabled, otherwise the lights and sirens won't work.")
-        UiPop()
-        end
-    end
-end
-
-
-
---fix this execute only one time every time the mode changes
 function lightsOptions()
     if lights1 then
 
         for i=1, #pry do
             em[i]=pry[i]
         end
-
 
     elseif lights2 then
             for i=1, #sec do
@@ -678,11 +643,9 @@
             end
         end
 
-
         lightsPatter()
 end
 
---fix this
 function lightsPatter()
     if em[1] ==0 then 
         FTE1 = 0        FTD1 = 0
@@ -915,13 +878,6 @@
 
 end
 
-
-
-
-
-
-
---fix this /create permutation/
 function patter(t)
 
     if t == 0 then
@@ -1060,3 +1016,31 @@
         EmergencyLights()
     end
 end
+
+function client.draw()
+    if not close then
+        if GetBool("level.ALS.enabled") and not close then
+            close=true
+        end
+    if GetPlayerVehicle(playerId) == ALSVehicle then
+        if InputPressed("esc")then
+            close=true
+        end
+            SetBool("game.disablepause", true, true)
+        UiPush()
+            local w = UiWidth()
+            local h = UiHeight()
+            UiTranslate(w-20, h/1.5)
+            UiAlign("right bottom")
+            UiImage("MOD/images/missing.png")
+            UiFont("regular.ttf", 20)
+            UiWordWrap(250)
+            UiTranslate(-5, 0)
+            UiText("Press (ESC) to hide this message")
+            UiTranslate(0, -60)
+            UiText("Please make sure that you have Advanced light system installed and enabled, otherwise the lights and sirens won't work.")
+        UiPop()
+        end
+    end
+end
+

```

---

# Migration Report: scripts\ALSsiren\ALSsiren_MOD.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ALSsiren\ALSsiren_MOD.lua
+++ patched/scripts\ALSsiren\ALSsiren_MOD.lua
@@ -1,95 +1,90 @@
-#include "library.lua"
-#include "setup.lua"
-
-function init()
-	SoundShape = FindShapes("ALShorn_MOD")
-	
-	Setup()
-	ReloadKeys()
-	
-	SetString("emergency.primary", GetString(pathKey.."primary"))
-    SetString("emergency.secondary", GetString(pathKey.."secondary"))
-    SetString("emergency.tertiary", GetString(pathKey.."tertiary"))
-	
-	-- sonds inits--
-	honkList = {}
-    honkList[#honkList + 1] = LoadLoop("sound/honk01.ogg")
-
-    sirenPrimary = {}
-    sirenPrimary[#sirenPrimary + 1] = LoadLoop("sound/sirenP01.ogg")
-
-    sirenSecondary = {}
-    sirenSecondary[#sirenSecondary + 1] = LoadLoop("sound/sirenS01.ogg")
-
-    sirenTertiary = {}
-    sirenTertiary[#sirenTertiary + 1] = LoadLoop("sound/sirenT01.ogg")
-
-    sirenFourth = {}
-    sirenFourth[#sirenFourth + 1] = LoadLoop("sound/sirenQ01.ogg")
+#version 2
+function server.init()
+    SoundShape = FindShapes("ALShorn_MOD")
+    Setup()
+    ReloadKeys()
+    SetString("emergency.primary", GetString(pathKey.."primary"), true)
+       SetString("emergency.secondary", GetString(pathKey.."secondary"), true)
+       SetString("emergency.tertiary", GetString(pathKey.."tertiary"), true)
+    -- sonds inits--
+    honkList = {}
+       honkList[#honkList + 1] = LoadLoop("sound/honk01.ogg")
+       sirenPrimary = {}
+       sirenPrimary[#sirenPrimary + 1] = LoadLoop("sound/sirenP01.ogg")
+       sirenSecondary = {}
+       sirenSecondary[#sirenSecondary + 1] = LoadLoop("sound/sirenS01.ogg")
+       sirenTertiary = {}
+       sirenTertiary[#sirenTertiary + 1] = LoadLoop("sound/sirenT01.ogg")
+       sirenFourth = {}
+       sirenFourth[#sirenFourth + 1] = LoadLoop("sound/sirenQ01.ogg")
 end
 
-function tick(dt)
-	local veh = GetPlayerVehicle()
-	
-	 --find shapes where the siren will play
-    SoundShape = FindShapes("ALShorn_MOD")
-	
-	 --//binds enable only when on vehicle//--
-    if HasTag(veh, "ALS") then
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local veh = GetPlayerVehicle(playerId)
+         --find shapes where the siren will play
+           SoundShape = FindShapes("ALShorn_MOD")
+         --//binds enable only when on vehicle//--
+        --//play audio//--
+           ALS_PlaySound(SoundShape, sirenPrimary, sirenSecondary, sirenTertiary, sirenFourth, honkList)
+    end
+end
 
-    --//binds enable only when on emergency vehicle//--
-    if HasTag(veh, "emergency") then
-	
-	--==========--
-    --  Sounds  --
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+       if HasTag(veh, "ALS") then
+
+       --//binds enable only when on emergency vehicle//--
+       if HasTag(veh, "emergency") then
+
     --==========--
-	--//sirens//--
-        if InputPressed(honksCtrl[1]) then
-			for i=1, #SoundShape do
-				if GetPlayerVehicle() == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
-					ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "1", "ALSsiren_MOD", "1")
-				end
-			end
-        elseif InputPressed(honksCtrl[2]) then
-			for i=1, #SoundShape do
-				if GetPlayerVehicle() == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
-					ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "2", "ALSsiren_MOD", "2")
-				end
-			end
-        elseif InputPressed(honksCtrl[3]) then
-			for i=1, #SoundShape do
-				if GetPlayerVehicle() == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
-					ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "3", "ALSsiren_MOD", "3")
-				end
-			end
-        elseif InputPressed(honksCtrl[7]) then
-			for i=1, #SoundShape do
-				if GetPlayerVehicle() == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
-					ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "4", "ALSsiren_MOD", "4")
-				end
-			end
-        end
-		
-	--//horn//--
-		if InputPressed(honksCtrl[4]) then
-			for i=1, #SoundShape do
-				if GetPlayerVehicle() == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
-					SetTag(SoundShape[i], "Horn")
-					--DebugPrint("Horn")
-				end
-			end
-		elseif InputReleased(honksCtrl[4]) then
-			for i=1, #SoundShape do
-				if GetPlayerVehicle() == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
-					RemoveTag(SoundShape[i], "Horn")
-					--DebugPrint("deleted")
-				end
-			end
-		end
-		
-	end
-	end
-	
-	--//play audio//--
-    ALS_PlaySound(SoundShape, sirenPrimary, sirenSecondary, sirenTertiary, sirenFourth, honkList)
-end+       --  Sounds  --
+       --==========--
+    --//sirens//--
+           if InputPressed(honksCtrl[1]) then
+    		for i=1, #SoundShape do
+    			if GetPlayerVehicle(playerId) == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
+    				ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "1", "ALSsiren_MOD", "1")
+    			end
+    		end
+           elseif InputPressed(honksCtrl[2]) then
+    		for i=1, #SoundShape do
+    			if GetPlayerVehicle(playerId) == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
+    				ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "2", "ALSsiren_MOD", "2")
+    			end
+    		end
+           elseif InputPressed(honksCtrl[3]) then
+    		for i=1, #SoundShape do
+    			if GetPlayerVehicle(playerId) == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
+    				ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "3", "ALSsiren_MOD", "3")
+    			end
+    		end
+           elseif InputPressed(honksCtrl[7]) then
+    		for i=1, #SoundShape do
+    			if GetPlayerVehicle(playerId) == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
+    				ALS_ChangeSound(SoundShape[i], GetTagValue(SoundShape[i], "ALSsiren_MOD") == "4", "ALSsiren_MOD", "4")
+    			end
+    		end
+           end
+
+    --//horn//--
+    	if InputPressed(honksCtrl[4]) then
+    		for i=1, #SoundShape do
+    			if GetPlayerVehicle(playerId) == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
+    				SetTag(SoundShape[i], "Horn")
+    				--DebugPrint("Horn")
+    			end
+    		end
+    	elseif InputReleased(honksCtrl[4]) then
+    		for i=1, #SoundShape do
+    			if GetPlayerVehicle(playerId) == GetBodyVehicle(GetShapeBody(SoundShape[i])) then
+    				RemoveTag(SoundShape[i], "Horn")
+    				--DebugPrint("deleted")
+    			end
+    		end
+    	end
+
+    end
+    end
+end
+

```

---

# Migration Report: scripts\ALSsiren\library.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ALSsiren\library.lua
+++ patched/scripts\ALSsiren\library.lua
@@ -1,9 +1,4 @@
---==========--
---  sirens  --
---==========--
-
-GLOBAL_VOLUME = 500
-
+#version 2
 function ALS_ChangeSound(SoundShape, turnOn, tag, value)
     if turnOn then
         RemoveTag(SoundShape, tag)
@@ -11,7 +6,6 @@
         SetTag(SoundShape, tag, value)
     end
 end
-
 
 function ALS_PlaySound(SoundShape, sirens1, sirens2, sirens3, sirens4, honks)
     if SoundShape ~= empty then
@@ -72,4 +66,5 @@
             end
         end
     end
-end+end
+

```

---

# Migration Report: scripts\ALSsiren\setup.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ALSsiren\setup.lua
+++ patched/scripts\ALSsiren\setup.lua
@@ -1,28 +1,7 @@
-pathKey = "savegame.mod.key_MOD."
-
-setupKey = {}
-setupKey[#setupKey+1] = {"siren1", "1"}
-setupKey[#setupKey+1] = {"siren2", "2"}
-setupKey[#setupKey+1] = {"siren3", "3"}
-setupKey[#setupKey+1] = {"siren4", "4"}
-setupKey[#setupKey+1] = {"sirenhold1", "V"}
-setupKey[#setupKey+1] = {"sirenhold2", "B"}
-setupKey[#setupKey+1] = {"horn", "G"}
-
----- Key Binding ----
-KeyList = {}
-KeyList[#KeyList+1] = {"Sounds", "Sounds"}
-KeyList[#KeyList+1] = {"Siren/Sound primary", GetString(pathKey.."siren1"), "siren1"}
-KeyList[#KeyList+1] = {"Siren/Sound secondary", GetString(pathKey.."siren2"), "siren2"}
-KeyList[#KeyList+1] = {"Siren/Sound tertiary", GetString(pathKey.."siren3"), "siren3"}
-KeyList[#KeyList+1] = {"Siren/Sound fourth", GetString(pathKey.."siren4"), "siren4"}
-KeyList[#KeyList+1] = {"Siren/Sound Play/Change Tone", GetString(pathKey.."sirenhold1"), "sirenhold1"}
-KeyList[#KeyList+1] = {"siren/Sound Change Tone", GetString(pathKey.."sirenhold2"), "sirenhold2"}
-KeyList[#KeyList+1] = {"Horn", GetString(pathKey.."horn"), "horn"}
-
+#version 2
 function Setup()
 	for i=1, #setupKey do
-		SetString(pathKey..setupKey[i][1], setupKey[i][2])
+		SetString(pathKey..setupKey[i][1], setupKey[i][2], true)
 	end
 end
 
@@ -35,4 +14,5 @@
     honksCtrl[#honksCtrl+1] = GetString(pathKey.."sirenhold1")
     honksCtrl[#honksCtrl+1] = GetString(pathKey.."sirenhold2")
     honksCtrl[#honksCtrl+1] = GetString(pathKey.."siren4")
-end+end
+

```

---

# Migration Report: scripts\bell.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\bell.lua
+++ patched/scripts\bell.lua
@@ -1,63 +1,66 @@
-function init()
-	button = FindShape("bellButton")
-	bells = FindShapes("bell", true)
-	onSound = LoadSound(GetStringParam("onSound", "MOD/sounds/onSound.ogg"))
-	offSound = LoadSound(GetStringParam("onSound", "MOD/sounds/offSound.ogg"))
-	bellSound = LoadLoop(GetStringParam("bell", "MOD/sounds/bell.ogg"))
-	bellEndSound = LoadSound(GetStringParam("bellEnd", "MOD/sounds/bellEnd.ogg"))
-	clickVolume = GetFloatParam("clickVolume", 0.5)
-	bellVolume = GetFloatParam("bellVolume", 0.5)
-
-	if onSound == 0 then DebugPrint("can't find on sound") end
-	if bellSound == 0 then DebugPrint("can't find off fire alarm sound") end
-	
-	SetTag(button, "interact", "Lockdown Alarm")
-
-
-end
-
-
-on = false
-timerOff = 0
-
+#version 2
 function updateTimers()
-	if timerOff > 0 then 
+	if timerOff ~= 0 then 
 		timerOff = timerOff - (GetTime() - timeOld)
 	end
 	
 	timeOld = GetTime()
 end
 
-function tick()
-	if IsShapeBroken(button) then
-		RemoveTag(button, "interact")
-	else
-		if GetPlayerInteractShape() == button and InputPressed("interact") and timerOff <= 0 or GetBool("level.bell.enabled") ~= on then
-			on = not on
-			SetBool("level.bell.enabled", on)
+function server.init()
+    button = FindShape("bellButton")
+    bells = FindShapes("bell", true)
+    bellSound = LoadLoop(GetStringParam("bell", "MOD/sounds/bell.ogg"))
+    clickVolume = GetFloatParam("clickVolume", 0.5)
+    bellVolume = GetFloatParam("bellVolume", 0.5)
+    if onSound == 0 then DebugPrint("can't find on sound") end
+    if bellSound == 0 then DebugPrint("can't find off fire alarm sound") end
 
-			if on then
-				PlaySound(onSound, GetShapeWorldTransform(button).pos, clickVolume)
-				
-			else
-				PlaySound(offSound, GetShapeWorldTransform(button).pos, clickVolume)
+    SetTag(button, "interact", "Lockdown Alarm")
+end
 
-				for b = 1, #bells do
-		 			if not IsShapeBroken(bells[b]) then
-						PlaySound(bellEndSound, GetShapeWorldTransform(bells[b]).pos, bellVolume)
-					end
-				end
-				timerOff = 1
-			end
-		end
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        updateTimers()
+    end
+end
 
-	if on then
-		for b = 1, #bells do
-			if not IsShapeBroken(bells[b]) then
-				PlayLoop(bellSound, GetShapeWorldTransform(bells[b]).pos, bellVolume)
-			end
-		end
-	end
-	updateTimers()
-end+function client.init()
+    onSound = LoadSound(GetStringParam("onSound", "MOD/sounds/onSound.ogg"))
+    offSound = LoadSound(GetStringParam("onSound", "MOD/sounds/offSound.ogg"))
+    bellEndSound = LoadSound(GetStringParam("bellEnd", "MOD/sounds/bellEnd.ogg"))
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if IsShapeBroken(button) then
+    	RemoveTag(button, "interact")
+    else
+    	if GetPlayerInteractShape(playerId) == button and InputPressed("interact") and timerOff <= 0 or GetBool("level.bell.enabled") ~= on then
+    		on = not on
+    		SetBool("level.bell.enabled", on, true)
+
+    		if on then
+    			PlaySound(onSound, GetShapeWorldTransform(button).pos, clickVolume)
+
+    		else
+    			PlaySound(offSound, GetShapeWorldTransform(button).pos, clickVolume)
+
+    			for b = 1, #bells do
+    	 			if not IsShapeBroken(bells[b]) then
+    					PlaySound(bellEndSound, GetShapeWorldTransform(bells[b]).pos, bellVolume)
+    				end
+    			end
+    			timerOff = 1
+    		end
+    	end
+    end
+    if on then
+    	for b = 1, #bells do
+    		if not IsShapeBroken(bells[b]) then
+    			PlayLoop(bellSound, GetShapeWorldTransform(bells[b]).pos, bellVolume)
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: scripts\button.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\button.lua
+++ patched/scripts\button.lua
@@ -1,67 +1,65 @@
-enableAllOld = false
-disableAllOld = false
-
-function init()
-	triggerTag = GetStringParam("triggerTag")
-	button = FindShape(triggerTag)
-
-	lightTrig = HasTag(button, "lightTrig")
-
-	onSound = LoadSound(GetStringParam("onSound", "MOD/sounds/onSound.ogg"))
-	offSound = LoadSound(GetStringParam("offSound", "MOD/sounds/offSound.ogg"))
-	volume = GetFloatParam("volume", 0.5)
-
-	if button == 0 then 
-		DebugPrint("can't find trigger")
-		DebugPrint(triggerTag)
-	end
-	if onSound == 0 then DebugPrint("can't find on sound") end
-	if offSound == 0 then DebugPrint("can't find off sound") end
-	SetTag(button, "interact", "light on")
-
-	enableAllOld = GetBool("level.light.enableAll")
-	disableAllOld = GetBool("level.light.disableAll")
-
-	SetBool("level.light."..triggerTag..".enabled", false)
-end
-
-isOn = false
-
+#version 2
 function on()
 	SetTag(button, "interact", "Light off")
-	SetBool("level.light."..triggerTag..".enabled", true)
+	SetBool("level.light."..triggerTag..".enabled", true, true)
 end
 
 function off()
 	SetTag(button, "interact", "Light on")
-	SetBool("level.light."..triggerTag..".enabled", false)
+	SetBool("level.light."..triggerTag..".enabled", false, true)
 end
 
-function tick()
-	if not IsShapeBroken(button) then
-		if GetPlayerInteractShape() == button and InputPressed("interact") then
-			isOn = not isOn
-			if isOn then
-				PlaySound(onSound, GetShapeWorldTransform(button).pos, volume)
-				on()
-			else
-				PlaySound(offSound, GetShapeWorldTransform(button).pos, volume)
-				off()
-			end
-		end
+function server.init()
+    triggerTag = GetStringParam("triggerTag")
+    button = FindShape(triggerTag)
+    lightTrig = HasTag(button, "lightTrig")
+    volume = GetFloatParam("volume", 0.5)
+    if button == 0 then 
+    	DebugPrint("can't find trigger")
+    	DebugPrint(triggerTag)
+    end
+    if onSound == 0 then DebugPrint("can't find on sound") end
+    if offSound == 0 then DebugPrint("can't find off sound") end
+    SetTag(button, "interact", "light on")
 
-		if lightTrig then
-			if GetBool("level.light.enableAll") ~= enableAllOld then
-				enableAllOld = not enableAllOld
-				isOn = true
-				on()
-			elseif GetBool("level.light.disableAll") ~= disableAllOld then
-				disableAllOld = not disableAllOld
-				isOn = false
-				off()
-			end
-		end
-	else
-		RemoveTag(button, "interact")
-	end
-end+    enableAllOld = GetBool("level.light.enableAll")
+    disableAllOld = GetBool("level.light.disableAll")
+
+    SetBool("level.light."..triggerTag..".enabled", false, true)
+end
+
+function client.init()
+    onSound = LoadSound(GetStringParam("onSound", "MOD/sounds/onSound.ogg"))
+    offSound = LoadSound(GetStringParam("offSound", "MOD/sounds/offSound.ogg"))
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if not IsShapeBroken(button) then
+    	if GetPlayerInteractShape(playerId) == button and InputPressed("interact") then
+    		isOn = not isOn
+    		if isOn then
+    			PlaySound(onSound, GetShapeWorldTransform(button).pos, volume)
+    			on()
+    		else
+    			PlaySound(offSound, GetShapeWorldTransform(button).pos, volume)
+    			off()
+    		end
+    	end
+
+    	if lightTrig then
+    		if GetBool("level.light.enableAll") ~= enableAllOld then
+    			enableAllOld = not enableAllOld
+    			isOn = true
+    			on()
+    		elseif GetBool("level.light.disableAll") ~= disableAllOld then
+    			disableAllOld = not disableAllOld
+    			isOn = false
+    			off()
+    		end
+    	end
+    else
+    	RemoveTag(button, "interact")
+    end
+end
+

```

---

# Migration Report: scripts\consolelights.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\consolelights.lua
+++ patched/scripts\consolelights.lua
@@ -1,11 +1,12 @@
-interval = GetIntParam("interval", 60)
-
-function init()
-	console = FindLight("console")
+#version 2
+function server.init()
+    console = FindLight("console")
 end
 
-frame = 0
-function tick()
-	frame = frame + 1
-	SetLightEnabled(console, frame % interval < interval/2)
-end+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        frame = frame + 1
+        SetLightEnabled(console, frame % interval < interval/2)
+    end
+end
+

```

---

# Migration Report: scripts\cop.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\cop.lua
+++ patched/scripts\cop.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 3.2)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 250
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = 20
-config.huntPlayer = false
-config.huntSpeedScale = 0.7
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 10.0
-config.maxSoundDist = 15.0
-config.aggressive = true
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 10.0
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -181,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -198,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 10.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -248,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -285,18 +132,15 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
@@ -309,7 +153,7 @@
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -328,14 +172,14 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 
 	if not robot.enabled then
 		return
 	end
 	
-    if GetPlayerVehicle()~=0 and getDist(robot.bodyCenter,GetPlayerPos()) < 4 then
+    if GetPlayerVehicle(playerId)~=0 and getDist(robot.bodyCenter,GetPlayerPos(playerId)) < 4 then
 		robot.enabled = false
 		feetCollideLegs(true)
 		Delete(j1)
@@ -353,7 +197,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -383,7 +227,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -398,20 +242,20 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 	
-	--if GetPlayerHealth() <= 0 then
+	--if GetPlayerHealth(playerId) <= 0 then
 		--robot.enabled = false
 		--feetCollideLegs(true)
 		--Delete(joint1)
@@ -419,21 +263,9 @@
 	
 end
 
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
-
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -453,9 +285,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -463,10 +294,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -485,7 +312,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -502,7 +328,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -515,7 +340,6 @@
 	local f = robot.mass*15.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -531,8 +355,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -595,7 +417,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -604,7 +426,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -615,15 +437,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -640,11 +453,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -653,12 +466,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -691,7 +498,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -719,9 +525,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -766,7 +571,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -808,13 +613,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -855,13 +653,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -888,7 +684,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -897,9 +692,8 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -920,7 +714,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -933,22 +727,21 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 6.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
 				rejectAllBodies(robot.allBodies)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -972,7 +765,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1037,15 +830,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1055,7 +840,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1080,22 +864,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1134,32 +906,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1183,7 +935,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1230,8 +982,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1260,26 +1012,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1315,35 +1058,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1435,7 +1159,7 @@
 		end
 
 		local targetRadius = 10.0
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 10.0
 		end
 	
@@ -1466,9 +1190,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1478,7 +1201,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1541,12 +1264,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1595,7 +1312,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1604,8 +1321,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1621,7 +1336,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1636,7 +1350,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1644,7 +1357,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1655,7 +1367,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1674,448 +1385,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-	
-	--copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
-	copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos	
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-        fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			Delete(lightsaber)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(mdeath, robot.bodyCenter, 0.6, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 0.7
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 1, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 1.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2124,64 +1393,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	if not robot.enabled then
@@ -2208,15 +1419,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
-
 
 function hitByShot(strength, pos, dir)
 
@@ -2252,77 +1461,15 @@
 	end
 end
 
-function tick()
-
-		if not robot.enabled then
-			return
-		end
-
-        if IsShapeBroken(box1) or IsShapeBroken(box2) then 
-		    --Spawn("MOD/copcar.xml", Transform(copspawnPos))
-			--Spawn("MOD/cop.xml", Transform(copspawn2Pos))		
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(j1)
-			Delete(j2)
-        end
-        if IsShapeBroken(box2) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box3) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box4) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box5) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box6) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box7) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box8) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end		
-        if IsShapeBroken(box9) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end	
-		
-end
-
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2340,8 +1487,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2368,3 +1513,475 @@
 	end
 end
 
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    --copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
+    copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos	
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 0.7
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+           fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		Delete(lightsaber)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(mdeath, robot.bodyCenter, 0.6, false)
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 1, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "huntlost" then
+    	if not state.timer then
+    		state.timer = 6
+    		state.turnTimer = 1
+    	end
+    	state.timer = state.timer - dt
+    	head.dir = VecCopy(robot.dir)
+    	if state.timer < 0 then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	else
+    		state.turnTimer = state.turnTimer - dt
+    		if state.turnTimer < 0 then
+    			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+    			state.turnTimer = rnd(0.5, 1.5)
+    		end
+    	end
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 1.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: scripts\elevator.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\elevator.lua
+++ patched/scripts\elevator.lua
@@ -1,90 +1,83 @@
-motorSpeed = 1.0		-- How fast the elevator is going
-motorStrength = 1000	-- How strong the motor is
-epsilon = 0.01			-- Stop elevator when within 1 cm from target position
-
-
-function init()	
-	--Find handles
-	up = FindShape("up")
-	down = FindShape("down")
-	joint = FindJoint("joint")
-	elevator = FindBody("elevator")
-
-	--This is how far the elevator can travel down and up
-	limitDown, limitUp = GetJointLimits(joint)
-
-	--Load sounds
-	clickSound = LoadSound("clickdown.ogg")
-	motorSound = LoadLoop("heavy_motor")
-
-	stuckTimer = 0.0
-	motor = 0
-	avgSpeed = 0
-end
-
-
-function tick(dt)
-	--Up button
-	if GetPlayerInteractShape() == up and InputPressed("interact") then
-		PlaySound(clickSound)
-		if motor == 1 then
-			motor = 0
-		else
-			motor = 1
-		end
-	end
-	
-	--Down button
-	if GetPlayerInteractShape() == down and InputPressed("interact") then
-		PlaySound(clickSound)
-		if motor == -1 then
-			motor = 0
-		else
-			motor = -1
-		end
-	end
-
-	--Measure sliding average elevator speed to see if elevator is stuck
-	--A sliding average will filter out spikes that can occur due to physics glitches
-	avgSpeed = avgSpeed*0.9 + math.abs(GetBodyVelocity(elevator)[2])*0.1
-	if motor ~= 0 and avgSpeed < motorSpeed*0.5 then
-		stuckTimer = stuckTimer + dt
-		if stuckTimer > 1.0 then
-			stop()
-		end
-	else
-		stuckTimer = 0
-	end
-	
-	--Joint control
-	if motor == 1 then
-		--Elevator is going up. Stop if we're at the top.
-		SetJointMotorTarget(joint, limitUp, motorSpeed, motorStrength)
-		PlayLoop(motorSound, GetBodyTransform(elevator).pos)
-		if GetJointMovement(joint) > limitUp-epsilon then
-			stop()
-		end
-	elseif motor == -1 then
-		--Elevator is going down. Stop if we're at the bottom.
-		SetJointMotorTarget(joint, limitDown, motorSpeed, motorStrength)
-		PlayLoop(motorSound, GetBodyTransform(elevator).pos)
-		if GetJointMovement(joint) < limitDown+epsilon then
-			stop()
-		end
-	else
-		--Elevator not moving. Hold in position.
-		SetJointMotor(joint, 0, motorStrength)
-	end
-	
-	--Make buttons light up when going up/down
-	if motor == 1 then SetShapeEmissiveScale(up, 1) else SetShapeEmissiveScale(up, 0) end
-	if motor == -1 then SetShapeEmissiveScale(down, 1) else SetShapeEmissiveScale(down, 0) end
-end
-
-
+#version 2
 function stop()
 	PlaySound(clickSound)
 	motor = 0
 end
 
+function server.init()
+    up = FindShape("up")
+    down = FindShape("down")
+    joint = FindJoint("joint")
+    elevator = FindBody("elevator")
+    --This is how far the elevator can travel down and up
+    limitDown, limitUp = GetJointLimits(joint)
+    --Load sounds
+    motorSound = LoadLoop("heavy_motor")
+    stuckTimer = 0.0
+    motor = 0
+    avgSpeed = 0
+end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        --Down button
+        --Measure sliding average elevator speed to see if elevator is stuck
+        --A sliding average will filter out spikes that can occur due to physics glitches
+        avgSpeed = avgSpeed*0.9 + math.abs(GetBodyVelocity(elevator)[2])*0.1
+        if motor ~= 0 and avgSpeed < motorSpeed*0.5 then
+        	stuckTimer = stuckTimer + dt
+        	if stuckTimer > 1.0 then
+        		stop()
+        	end
+        else
+        	stuckTimer = 0
+        end
+        --Joint control
+        --Make buttons light up when going up/down
+        if motor == 1 then SetShapeEmissiveScale(up, 1) else SetShapeEmissiveScale(up, 0) end
+        if motor == -1 then SetShapeEmissiveScale(down, 1) else SetShapeEmissiveScale(down, 0) end
+    end
+end
+
+function client.init()
+    clickSound = LoadSound("clickdown.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == up and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if motor == 1 then
+    		motor = 0
+    	else
+    		motor = 1
+    	end
+    end
+    if GetPlayerInteractShape(playerId) == down and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if motor == -1 then
+    		motor = 0
+    	else
+    		motor = -1
+    	end
+    end
+    if motor == 1 then
+    	--Elevator is going up. Stop if we're at the top.
+    	SetJointMotorTarget(joint, limitUp, motorSpeed, motorStrength)
+    	PlayLoop(motorSound, GetBodyTransform(elevator).pos)
+    	if GetJointMovement(joint) > limitUp-epsilon then
+    		stop()
+    	end
+    elseif motor == -1 then
+    	--Elevator is going down. Stop if we're at the bottom.
+    	SetJointMotorTarget(joint, limitDown, motorSpeed, motorStrength)
+    	PlayLoop(motorSound, GetBodyTransform(elevator).pos)
+    	if GetJointMovement(joint) < limitDown+epsilon then
+    		stop()
+    	end
+    else
+    	--Elevator not moving. Hold in position.
+    	SetJointMotor(joint, 0, motorStrength)
+    end
+end
+

```

---

# Migration Report: scripts\fireplacecandle.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\fireplacecandle.lua
+++ patched/scripts\fireplacecandle.lua
@@ -1,40 +1,46 @@
+#version 2
 function rnd(mi, ma)
 	return math.random()*(ma-mi) + mi
 end
-function init()
-    if not GetBool("savegame.mod.fire") then
-        lareira = FindShapes("lareira",true)
-	    fumaca = FindLocations("fumaca",true)
-	    fogo = FindLocations("fogo",true)
+
+function server.init()
+       if not GetBool("savegame.mod.fire") then
+           lareira = FindShapes("lareira",true)
+        fumaca = FindLocations("fumaca",true)
+        fogo = FindLocations("fogo",true)
+       end
+       if not GetBool("savegame.mod.candle") then
+           velas = FindBodies("vela",true)
+           Luzes = FindLights("luz",true)
+       end
+       frame = math.random(0, 60)
+       lenha = FindLocations("lenha",true)
+    for j=1, #lenha do
+    	tag = GetTagValue(lenha[j], "lenha")
+    	Spawn("MOD/prefab/lenha"..tag..".xml", Transform(GetLocationTransform(lenha[j]).pos,GetLocationTransform(lenha[j]).rot))
     end
-    if not GetBool("savegame.mod.candle") then
-        velas = FindBodies("vela",true)
-        Luzes = FindLights("luz",true)
-    end
-    frame = math.random(0, 60)
-
-    lenha = FindLocations("lenha",true)
-	for j=1, #lenha do
-		tag = GetTagValue(lenha[j], "lenha")
-		Spawn("MOD/prefab/lenha"..tag..".xml", Transform(GetLocationTransform(lenha[j]).pos,GetLocationTransform(lenha[j]).rot))
-	end
 end
 
-function update(dt)
-    if not GetBool("savegame.mod.fire") or not GetBool("savegame.mod.candle") then   
-    tempo2 = frame % 1400
-    tempo = frame % 5
-    frame = frame + 1
-    end
-
-    if not GetBool("savegame.mod.fire") then
-        if tempo2 == 1399 then
-            for i=1, #lenha do
-                tag = GetTagValue(lenha[i], "lenha")
-                Spawn("MOD/prefab/lenha"..tag..".xml", Transform(GetLocationTransform(lenha[i]).pos,GetLocationTransform(lenha[i]).rot))
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not GetBool("savegame.mod.fire") or not GetBool("savegame.mod.candle") then   
+        tempo2 = frame % 1400
+        tempo = frame % 5
+        frame = frame + 1
+        end
+        if not GetBool("savegame.mod.fire") then
+            if tempo2 == 1399 then
+                for i=1, #lenha do
+                    tag = GetTagValue(lenha[i], "lenha")
+                    Spawn("MOD/prefab/lenha"..tag..".xml", Transform(GetLocationTransform(lenha[i]).pos,GetLocationTransform(lenha[i]).rot))
+                end
             end
         end
     end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
         if tempo == 1 then
             if not GetBool("savegame.mod.fire") then
                 for j=1, #lareira do

```

---

# Migration Report: scripts\light.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\light.lua
+++ patched/scripts\light.lua
@@ -1,35 +1,12 @@
-on = false
-timerOn = 0.0
-timerOff = 0.0
-blinksTimer = 0.0
-trigerOn = false
-
-timeOld = 0.0
-
-function init()
-	triggerTag = GetStringParam("buttonTag")
-
-	light = FindLight("light")
-	body = FindShape("body")
-	startVolume = GetFloatParam("volume", 0.2)
-	workVolume = GetFloatParam("volume", 0.1)
-
-	SetLightEnabled(light, false)
-
-	local r = math.random(1, 6)
-	startSound = LoadLoop(string.format("MOD/sounds/lampStarts%d.ogg", r))
-	workSound = LoadLoop(GetStringParam("lampWorkSound", "MOD/sounds/lampWorks.ogg"), 1.5)
-end
-
-
+#version 2
 function updateTimers()
-	if blinksTimer > 0 then 
+	if blinksTimer ~= 0 then 
 		blinksTimer = blinksTimer - (GetTime() - timeOld)
 	end
-	if timerOn > 0 then 
+	if timerOn ~= 0 then 
 		timerOn = timerOn - (GetTime() - timeOld)
 	end
-	if timerOff > 0 then 
+	if timerOff ~= 0 then 
 		timerOff = timerOff - (GetTime() - timeOld)
 	end
 	
@@ -63,6 +40,7 @@
 		if GetBool("level.light.noiseEnabled") then PlayLoop(workSound, GetLightTransform(light).pos, workVolume) end
 	end
 end
+
 function lightOff()
 	SetLightEnabled(light, false)
 	on = false
@@ -71,15 +49,30 @@
 	blinksTimer = -100
 end
 
-function tick()
-	if IsShapeBroken(body) then
-		lightOff()
-	else
-		if GetBool("level.light."..triggerTag..".enabled") then
-			lightOn()
-		else
-			lightOff()
-		end
-	end
-	updateTimers()
-end+function server.init()
+    triggerTag = GetStringParam("buttonTag")
+    light = FindLight("light")
+    body = FindShape("body")
+    startVolume = GetFloatParam("volume", 0.2)
+    workVolume = GetFloatParam("volume", 0.1)
+    SetLightEnabled(light, false)
+    local r = math.random(1, 6)
+    startSound = LoadLoop(string.format("MOD/sounds/lampStarts%d.ogg", r))
+    workSound = LoadLoop(GetStringParam("lampWorkSound", "MOD/sounds/lampWorks.ogg"), 1.5)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(body) then
+        	lightOff()
+        else
+        	if GetBool("level.light."..triggerTag..".enabled") then
+        		lightOn()
+        	else
+        		lightOff()
+        	end
+        end
+        updateTimers()
+    end
+end
+

```

---

# Migration Report: scripts\nocull.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\nocull.lua
+++ patched/scripts\nocull.lua
@@ -1,9 +1,7 @@
-function init()
+#version 2
+function server.init()
     for index, s in ipairs(FindShapes('', true)) do
         SetTag(s, 'nocull')
     end
 end
 
-function tick()
-	
-end
```

---

# Migration Report: scripts\npc.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\npc.lua
+++ patched/scripts\npc.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 2.2)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 25
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 0.7
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 15.0
-config.aggressive = false
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 10.0
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -181,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -198,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 10.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -248,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -283,18 +130,15 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
@@ -303,12 +147,11 @@
 	return VecLength(VecSub(v1,v2))
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -327,10 +170,10 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
-    if GetPlayerVehicle()~=0 and getDist(robot.bodyCenter,GetPlayerPos()) < 4 then
+    if GetPlayerVehicle(playerId)~=0 and getDist(robot.bodyCenter,GetPlayerPos(playerId)) < 4 then
 		robot.enabled = false
 		feetCollideLegs(true)
 		Delete(joint1)		
@@ -346,7 +189,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -376,7 +219,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -391,35 +234,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -439,9 +270,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -449,10 +279,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -471,7 +297,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -488,7 +313,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -501,7 +325,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -517,8 +340,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -581,7 +402,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -590,7 +411,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -601,15 +422,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -626,11 +438,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -639,12 +451,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -677,7 +483,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -705,9 +510,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -752,7 +556,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -794,13 +598,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -841,13 +638,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -874,7 +669,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -883,9 +677,8 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -906,7 +699,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -919,22 +712,21 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 6.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
 				rejectAllBodies(robot.allBodies)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -958,7 +750,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1023,15 +815,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1041,7 +825,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1066,22 +849,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1120,32 +891,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1169,7 +920,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1216,8 +967,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1246,26 +997,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1301,35 +1043,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1421,7 +1144,7 @@
 		end
 
 		local targetRadius = 4.0
-		if GetPlayerVehicle()~=0 then		
+		if GetPlayerVehicle(playerId)~=0 then		
 			targetRadius = 4.0
 		end
 		
@@ -1452,9 +1175,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1464,7 +1186,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1527,12 +1249,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1581,7 +1297,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1590,8 +1306,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1607,7 +1321,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1622,7 +1335,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1630,7 +1342,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1641,7 +1352,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1660,448 +1370,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-	
-	--copspawn = FindLocation("copspawn")
-	copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-        fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			Delete(lightsaber)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(mdeath, robot.bodyCenter, 0.6, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 0.7
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 1, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 1.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2110,64 +1378,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	if not robot.enabled then
@@ -2194,15 +1404,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
-
 
 function hitByShot(strength, pos, dir)
 
@@ -2238,75 +1446,15 @@
 	end
 end
 
-function tick()
-
-		if not robot.enabled then
-			return
-		end
-
-        if IsShapeBroken(box1) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-			Spawn("MOD/copcar.xml", Transform(copspawnPos))
-        end
-        if IsShapeBroken(box2) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box3) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box4) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box5) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box6) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box7) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box8) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end		
-        if IsShapeBroken(box9) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end	
-		
-end
-
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2324,8 +1472,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2352,3 +1498,475 @@
 	end
 end
 
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    --copspawn = FindLocation("copspawn")
+    copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 0.7
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+           fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		Delete(lightsaber)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(mdeath, robot.bodyCenter, 0.6, false)
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 1, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "huntlost" then
+    	if not state.timer then
+    		state.timer = 6
+    		state.turnTimer = 1
+    	end
+    	state.timer = state.timer - dt
+    	head.dir = VecCopy(robot.dir)
+    	if state.timer < 0 then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	else
+    		state.turnTimer = state.turnTimer - dt
+    		if state.turnTimer < 0 then
+    			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+    			state.turnTimer = rnd(0.5, 1.5)
+    		end
+    	end
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 1.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: scripts\npc2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\npc2.lua
+++ patched/scripts\npc2.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 2.2)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 25
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 0.7
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 15.0
-config.aggressive = false
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 10.0
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -181,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -198,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 10.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -248,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -283,18 +130,15 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
@@ -303,12 +147,11 @@
 	return VecLength(VecSub(v1,v2))
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -327,14 +170,14 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	if not robot.enabled then
 		return
 	end	
 	
-    if GetPlayerVehicle()~=0 and getDist(robot.bodyCenter,GetPlayerPos()) < 3 then
+    if GetPlayerVehicle(playerId)~=0 and getDist(robot.bodyCenter,GetPlayerPos(playerId)) < 3 then
 		robot.enabled = false
 		feetCollideLegs(true)
 		Delete(joint1)		
@@ -351,7 +194,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -381,7 +224,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -396,35 +239,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -444,9 +275,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -454,10 +284,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -476,7 +302,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -493,7 +318,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -506,7 +330,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -522,8 +345,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -586,7 +407,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -595,7 +416,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -606,15 +427,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -631,11 +443,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -644,12 +456,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -682,7 +488,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -710,9 +515,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -757,7 +561,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -799,13 +603,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -846,13 +643,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -879,7 +674,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -888,9 +682,8 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -911,7 +704,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -924,22 +717,21 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 6.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
 				rejectAllBodies(robot.allBodies)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -963,7 +755,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1028,15 +820,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1046,7 +830,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1071,22 +854,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1125,32 +896,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1174,7 +925,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1221,8 +972,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1251,26 +1002,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1306,35 +1048,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1426,7 +1149,7 @@
 		end
 
 		local targetRadius = 4.0
-		if GetPlayerVehicle()~=0 then		
+		if GetPlayerVehicle(playerId)~=0 then		
 			targetRadius = 4.0
 		end
 		
@@ -1457,9 +1180,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1469,7 +1191,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1532,12 +1254,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1586,7 +1302,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1595,8 +1311,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1612,7 +1326,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1627,7 +1340,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1635,7 +1347,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1646,7 +1357,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1665,450 +1375,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-	
-	--copspawn = FindLocation("copspawn")
-	copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
-	copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
-	copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-        fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			Delete(lightsaber)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(mdeath, robot.bodyCenter, 0.6, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 0.7
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 1, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 1.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2117,64 +1383,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	if not robot.enabled then
@@ -2201,15 +1409,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
-
 
 function hitByShot(strength, pos, dir)
 
@@ -2245,77 +1451,15 @@
 	end
 end
 
-function tick()
-
-		if not robot.enabled then
-			return
-		end
-
-        if IsShapeBroken(box1) or IsShapeBroken(box2) then 
-		    Spawn("MOD/copcar.xml", Transform(copspawnPos))
-			Spawn("MOD/cop.xml", Transform(copspawn2Pos))
-			Spawn("MOD/cop.xml", Transform(copspawn3Pos))
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box2) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box3) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box4) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box5) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box6) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box7) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box8) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end		
-        if IsShapeBroken(box9) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end	
-		
-end
-
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2333,8 +1477,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2361,3 +1503,477 @@
 	end
 end
 
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    --copspawn = FindLocation("copspawn")
+    copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
+    copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
+    copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 0.7
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+           fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		Delete(lightsaber)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(mdeath, robot.bodyCenter, 0.6, false)
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 1, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "huntlost" then
+    	if not state.timer then
+    		state.timer = 6
+    		state.turnTimer = 1
+    	end
+    	state.timer = state.timer - dt
+    	head.dir = VecCopy(robot.dir)
+    	if state.timer < 0 then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	else
+    		state.turnTimer = state.turnTimer - dt
+    		if state.turnTimer < 0 then
+    			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+    			state.turnTimer = rnd(0.5, 1.5)
+    		end
+    	end
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 1.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: scripts\npc3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\npc3.lua
+++ patched/scripts\npc3.lua
@@ -1,30 +1,30 @@
-
-function init()
-
-    frame1 = math.random(0, 30)
-	box1 = FindShape("box1")
-	trig = FindTrigger("trig")
-	copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
-	copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
-	copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
-	copspawn4Pos = GetLocationTransform(FindLocation("copspawn4")).pos
-	copspawn5Pos = GetLocationTransform(FindLocation("copspawn5")).pos
+#version 2
+function server.init()
+       frame1 = math.random(0, 30)
+    box1 = FindShape("box1")
+    trig = FindTrigger("trig")
+    copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
+    copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
+    copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
+    copspawn4Pos = GetLocationTransform(FindLocation("copspawn4")).pos
+    copspawn5Pos = GetLocationTransform(FindLocation("copspawn5")).pos
 end
 
-
-function tick(dt)
-	t1 = frame1 % 3000
-    if IsTriggerEmpty(trig) then 
-	    frame1 = frame1 + 1
-		if t1 == 40 then
-		    Spawn("MOD/copcar.xml", Transform(copspawnPos))
-		    Spawn("MOD/cop.xml", Transform(copspawn2Pos))
-			Spawn("MOD/cop.xml", Transform(copspawn3Pos))
-			Spawn("MOD/cop.xml", Transform(copspawn4Pos))
-			--Spawn("MOD/copter.xml", Transform(copspawn5Pos))
-		elseif t1 == 2900 then	
-		    Spawn("MOD/copter.xml", Transform(copspawn5Pos))
-		end	
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        t1 = frame1 % 3000
+           if IsTriggerEmpty(trig) then 
+            frame1 = frame1 + 1
+        	if t1 == 40 then
+        	    Spawn("MOD/copcar.xml", Transform(copspawnPos))
+        	    Spawn("MOD/cop.xml", Transform(copspawn2Pos))
+        		Spawn("MOD/cop.xml", Transform(copspawn3Pos))
+        		Spawn("MOD/cop.xml", Transform(copspawn4Pos))
+        		--Spawn("MOD/copter.xml", Transform(copspawn5Pos))
+        	elseif t1 == 2900 then	
+        	    Spawn("MOD/copter.xml", Transform(copspawn5Pos))
+        	end	
+        end
+    end
 end
 

```

---

# Migration Report: scripts\npcheli.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\npcheli.lua
+++ patched/scripts\npcheli.lua
@@ -1,28 +1,28 @@
-
-function init()
-
-    frame1 = math.random(0, 30)
-	b1 = FindShape("b1")
-	b2 = FindShape("b2")
-	--copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
-	--copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
-	--copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
-	--copspawn4Pos = GetLocationTransform(FindLocation("copspawn4")).pos
-	copspawn5Pos = GetLocationTransform(FindLocation("copspawn5")).pos
+#version 2
+function server.init()
+       frame1 = math.random(0, 30)
+    b1 = FindShape("b1")
+    b2 = FindShape("b2")
+    --copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
+    --copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
+    --copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
+    --copspawn4Pos = GetLocationTransform(FindLocation("copspawn4")).pos
+    copspawn5Pos = GetLocationTransform(FindLocation("copspawn5")).pos
 end
 
-
-function update(dt)
-	t1 = frame1 % 3500
-    if IsShapeBroken(b1) and IsShapeBroken(b2) then 
-	    frame1 = frame1 + 1
-		if t1 == 60 then
-		    --Spawn("MOD/copcar.xml", Transform(copspawnPos))
-		    --Spawn("MOD/cop.xml", Transform(copspawn2Pos))
-			--Spawn("MOD/cop.xml", Transform(copspawn3Pos))
-			--Spawn("MOD/cop.xml", Transform(copspawn4Pos))
-			Spawn("MOD/copter.xml", Transform(copspawn5Pos))
-		end	
-	end
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        t1 = frame1 % 3500
+           if IsShapeBroken(b1) and IsShapeBroken(b2) then 
+            frame1 = frame1 + 1
+        	if t1 == 60 then
+        	    --Spawn("MOD/copcar.xml", Transform(copspawnPos))
+        	    --Spawn("MOD/cop.xml", Transform(copspawn2Pos))
+        		--Spawn("MOD/cop.xml", Transform(copspawn3Pos))
+        		--Spawn("MOD/cop.xml", Transform(copspawn4Pos))
+        		Spawn("MOD/copter.xml", Transform(copspawn5Pos))
+        	end	
+        end
+    end
 end
 

```

---

# Migration Report: scripts\npcspawn1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\npcspawn1.lua
+++ patched/scripts\npcspawn1.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 2.2)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 25
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 0.7
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 15.0
-config.aggressive = false
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 10.0
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -181,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -198,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 10.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -248,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -283,18 +130,15 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
@@ -303,12 +147,11 @@
 	return VecLength(VecSub(v1,v2))
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -327,14 +170,14 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	if not robot.enabled then
 		return
 	end	
 	
-    if GetPlayerVehicle()~=0 and getDist(robot.bodyCenter,GetPlayerPos()) < 3 then
+    if GetPlayerVehicle(playerId)~=0 and getDist(robot.bodyCenter,GetPlayerPos(playerId)) < 3 then
 		robot.enabled = false
 		feetCollideLegs(true)
 		Delete(joint1)		
@@ -351,7 +194,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -369,7 +212,7 @@
 
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -384,35 +227,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -432,9 +263,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -442,10 +272,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -464,7 +290,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -481,7 +306,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -494,7 +318,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -510,8 +333,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -574,7 +395,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -583,7 +404,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -594,15 +415,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -619,11 +431,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -632,12 +444,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -670,7 +476,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -698,9 +503,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -745,7 +549,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -787,13 +591,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -834,13 +631,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -867,7 +662,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -876,9 +670,8 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -899,7 +692,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -912,22 +705,21 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 6.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
 				rejectAllBodies(robot.allBodies)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -951,7 +743,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1016,15 +808,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1034,7 +818,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1059,22 +842,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1113,32 +884,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1162,7 +913,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1209,8 +960,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1239,26 +990,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1294,35 +1036,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1414,7 +1137,7 @@
 		end
 
 		local targetRadius = 4.0
-		if GetPlayerVehicle()~=0 then		
+		if GetPlayerVehicle(playerId)~=0 then		
 			targetRadius = 4.0
 		end
 		
@@ -1445,9 +1168,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1457,7 +1179,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1520,12 +1242,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1574,7 +1290,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1583,8 +1299,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1600,7 +1314,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1615,7 +1328,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1623,7 +1335,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1634,7 +1345,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1653,450 +1363,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-	
-	--copspawn = FindLocation("copspawn")
-	copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
-	copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
-	copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-        fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			Delete(lightsaber)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(mdeath, robot.bodyCenter, 0.6, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 0.7
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 1, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 1.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2105,64 +1371,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	if not robot.enabled then
@@ -2189,15 +1397,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
-
 
 function hitByShot(strength, pos, dir)
 
@@ -2233,77 +1439,15 @@
 	end
 end
 
-function tick()
-
-		if not robot.enabled then
-			return
-		end
-
-        if IsShapeBroken(box1) or IsShapeBroken(box2) then 
-		    --Spawn("MOD/copcar.xml", Transform(copspawnPos))
-			--Spawn("MOD/cop.xml", Transform(copspawn2Pos))
-			--Spawn("MOD/cop.xml", Transform(copspawn3Pos))
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box2) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box3) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box4) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box5) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box6) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box7) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end
-        if IsShapeBroken(box8) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end		
-        if IsShapeBroken(box9) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-			Delete(joint1)
-        end	
-		
-end
-
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2321,8 +1465,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2349,3 +1491,477 @@
 	end
 end
 
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    --copspawn = FindLocation("copspawn")
+    copspawnPos = GetLocationTransform(FindLocation("copspawn")).pos
+    copspawn2Pos = GetLocationTransform(FindLocation("copspawn2")).pos
+    copspawn3Pos = GetLocationTransform(FindLocation("copspawn3")).pos
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 0.7
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/sounds/midle0.ogg", 9.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    huntSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    idleSound = LoadSound("MOD/sounds/midle0.ogg", 9.0)
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+           fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		Delete(lightsaber)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(mdeath, robot.bodyCenter, 0.6, false)
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 1, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "huntlost" then
+    	if not state.timer then
+    		state.timer = 6
+    		state.turnTimer = 1
+    	end
+    	state.timer = state.timer - dt
+    	head.dir = VecCopy(robot.dir)
+    	if state.timer < 0 then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	else
+    		state.turnTimer = state.turnTimer - dt
+    		if state.turnTimer < 0 then
+    			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+    			state.turnTimer = rnd(0.5, 1.5)
+    		end
+    	end
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 1.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: scripts\skin.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\skin.lua
+++ patched/scripts\skin.lua
@@ -1,24 +1,25 @@
-function init()	
-	body = FindShapes("body")
-	skin = FindShapes("skin")
+#version 2
+function server.init()
+    body = FindShapes("body")
+    skin = FindShapes("skin")
 end
 
-
-function tick()
-	for i=1, #body do
-		if IsShapeBroken(body[i]) then
-			for i=1, #skin do
-			Delete(skin[i])
-			end
-		end
-	end
-	for i=1, #skin do
-		if IsShapeBroken(skin[i]) then
-			for i=1, #skin do
-			Delete(skin[i])
-			end
-		end
-	end
-	
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for i=1, #body do
+        	if IsShapeBroken(body[i]) then
+        		for i=1, #skin do
+        		Delete(skin[i])
+        		end
+        	end
+        end
+        for i=1, #skin do
+        	if IsShapeBroken(skin[i]) then
+        		for i=1, #skin do
+        		Delete(skin[i])
+        		end
+        	end
+        end
+    end
 end
 

```

---

# Migration Report: scripts\trooper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\trooper.lua
+++ patched/scripts\trooper.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,35 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 3.7)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 50
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 40.0
-config.aggressive = false
-config.stepSound = "m"
-config.practice = false
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -180,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -197,40 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -238,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -268,28 +125,24 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -308,7 +161,7 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	local vel = GetBodyVelocity(robot.body)
@@ -320,7 +173,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -350,7 +203,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -365,35 +218,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -413,9 +254,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -423,10 +263,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -445,7 +281,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -462,7 +297,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -475,7 +309,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -491,8 +324,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -555,7 +386,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -564,7 +395,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -575,15 +406,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -600,11 +422,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -613,12 +435,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -651,7 +467,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -679,9 +494,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -726,7 +540,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -768,13 +582,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -818,13 +625,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -851,7 +656,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -860,10 +664,9 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
 
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -884,7 +687,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -897,17 +700,17 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 2.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.2 or distToPlayer < 0.1 then
 				rejectAllBodies(robot.allBodies)
 				SetJointMotor(saber, 0)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.2 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength)
 					--SetJointMotor(saber, -15)
 					SetBodyAngularVelocity(body1, Vec(0, -100, 0))
 				end
@@ -915,7 +718,6 @@
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -939,7 +741,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1004,15 +806,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1022,7 +816,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1047,22 +840,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1101,32 +882,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1150,7 +911,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1197,8 +958,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1227,26 +988,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1282,35 +1034,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1402,7 +1135,7 @@
 		end
 
 		local targetRadius = 4
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 4.0
 		end
 	
@@ -1433,9 +1166,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1445,7 +1177,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1508,12 +1240,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1562,7 +1288,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1571,8 +1297,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1588,7 +1312,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1603,7 +1326,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1611,7 +1333,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1622,7 +1343,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1641,438 +1361,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("MOD/main/snd/blastersfx.ogg", 20.0)
-	deathSound = LoadSound("MOD/main/snd/stdeath.ogg", 9.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
-	huntSound = LoadSound("MOD/main/snd/trooper/storm0.ogg", 9.0)
-	idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-	crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
-	swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
-        fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 0.3, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 10.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2081,64 +1369,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2163,14 +1393,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2187,54 +1416,15 @@
 	end
 end
 
-function tick()
-        if IsShapeBroken(target1) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end
-        if IsShapeBroken(target2) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end
-        if IsShapeBroken(target3) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end
-        if IsShapeBroken(target4) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end
-        if IsShapeBroken(target5) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end
-        if IsShapeBroken(target6) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end
-        if IsShapeBroken(target7) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end
-        if IsShapeBroken(target8) then 
-		    robot.enabled = false
-			feetCollideLegs(true)
-        end						
-end
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2252,8 +1442,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2279,3 +1467,468 @@
 		end
 	end
 end
+
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        if state.id == "huntlost" then
+        	if not state.timer then
+        		state.timer = 6
+        		state.turnTimer = 1
+        	end
+        	state.timer = state.timer - dt
+        	head.dir = VecCopy(robot.dir)
+        	if state.timer < 0 then
+        		--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+        		stackPop()
+        	else
+        		state.turnTimer = state.turnTimer - dt
+        		if state.turnTimer < 0 then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turnTimer = rnd(0.5, 1.5)
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("MOD/main/snd/blastersfx.ogg", 20.0)
+    deathSound = LoadSound("MOD/main/snd/stdeath.ogg", 9.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
+    huntSound = LoadSound("MOD/main/snd/trooper/storm0.ogg", 9.0)
+    idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+    crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
+    swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
+           fdeath = LoadSound("MOD/main/snd/villager/fdeath0.ogg")
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 0.3, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 10.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: scripts\UDLF_Portable\UDLF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\UDLF_Portable\UDLF.lua
+++ patched/scripts\UDLF_Portable\UDLF.lua
@@ -1,22 +1,4 @@
---global variables
---bool debug
---bool verbose
---tabl latches[]
-
-
-function init()
-	debug = GetBool('savegame.mod.debug')
-	verbose = GetBool('savegame.mod.verbose')
-	local foundLatches = FindShapes("Latch", true) --Only used to get IDs. Indexes are discarded when transferred to Latches.
-	latches = {}
-	for _,ID in pairs(foundLatches) do
-		latches[ID] = 0
-	end
-	AppendLatchData()
-end
-
-
-
+#version 2
 function AppendLatchData() --Just an initialization step to put everything together.
 	for ID, _ in pairs(latches) do
 		local latchType = GetTagValue(ID, "Latch")
@@ -49,8 +31,6 @@
 	if debug then CheckLatchDataSanity() end
 end
 
-
-
 function CheckLatchDataSanity()
 	for ID,_ in pairs(latches) do
 		if latches[ID]["Type"] == nil then DebugPrint("Latch type is nil in shape: " .. ID .. " (No latch type was set. Check your tags: Latch=[Type])") end
@@ -65,31 +45,6 @@
 	end
 end
 
-
-
-function tick(dt)
-	local grabShape = GetPlayerGrabShape()
-	for latchShape,_ in pairs(latches) do
-		local shapeJoints = GetShapeJoints(latchShape)
-		local latchJoint = shapeJoints[1]
-		if IsJointBroken(latchJoint) == false then
-			if latchShape == grabShape and latches[latchShape]["isOpen"] == false then	--Unlatch if grabbed
-				SetJointMotor(latchJoint, 0, 0)
-				PlayIndexedSound(latchShape, true)
-				latches[latchShape]["isOpen"] = true
-			elseif GetJointMovement(latchJoint) < 0.01 and latches[latchShape]["isOpen"] == true and latchShape ~= grabShape then		--Latch if closed and not grabbed
-				SetJointMotorTarget(latchJoint, 0)
-				PlayIndexedSound(latchShape, false)
-				latches[latchShape]["isOpen"] = false
-			end
-		end
-	end
-end
-
-
-
----@param shape number Shape ID to play at.
----@param openQuery string Sound variant to play.
 function PlayIndexedSound(shape, openQuery)
 	local previousState = latches[shape]["isOpen"]
 	if openQuery ~= previousState then																													--Make sure not to play the sound if it was just played
@@ -109,4 +64,35 @@
 	end
 end
 
+function server.init()
+    debug = GetBool('savegame.mod.debug')
+    verbose = GetBool('savegame.mod.verbose')
+    local foundLatches = FindShapes("Latch", true) --Only used to get IDs. Indexes are discarded when transferred to Latches.
+    latches = {}
+    for _,ID in pairs(foundLatches) do
+    	latches[ID] = 0
+    end
+    AppendLatchData()
+end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local grabShape = GetPlayerGrabShape(playerId)
+        for latchShape,_ in pairs(latches) do
+        	local shapeJoints = GetShapeJoints(latchShape)
+        	local latchJoint = shapeJoints[1]
+        	if IsJointBroken(latchJoint) == false then
+        		if latchShape == grabShape and latches[latchShape]["isOpen"] == false then	--Unlatch if grabbed
+        			SetJointMotor(latchJoint, 0, 0)
+        			PlayIndexedSound(latchShape, true)
+        			latches[latchShape]["isOpen"] = true
+        		elseif GetJointMovement(latchJoint) < 0.01 and latches[latchShape]["isOpen"] == true and latchShape ~= grabShape then		--Latch if closed and not grabbed
+        			SetJointMotorTarget(latchJoint, 0)
+        			PlayIndexedSound(latchShape, false)
+        			latches[latchShape]["isOpen"] = false
+        		end
+        	end
+        end
+    end
+end
+

```

---

# Migration Report: scripts\waitingcar.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\waitingcar.lua
+++ patched/scripts\waitingcar.lua
@@ -1,14 +1,17 @@
-function init()	
-	whatsapp = FindVehicle("car2")
-end
-
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
 
-function tick()
-	--DebugPrint(GetPlayerVehicle())
-	local v = FindVehicle("car2")
-	DriveVehicle(v, 0.0, 0, false)
+function server.init()
+    whatsapp = FindVehicle("car2")
 end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local v = FindVehicle("car2")
+        DriveVehicle(v, 0.0, 0, false)
+    end
+end
+

```

---

# Migration Report: voxscript\ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/voxscript\ground.lua
+++ patched/voxscript\ground.lua
@@ -1,37 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
-hollow = GetInt("hollow", 0)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
+    matDirt = CreateMaterial("dirt", 0.66, 0.57, 0.42, 1, 0, 0.1)
+    matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
+    matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h-1 do
+    	local y1 = y0 + maxSize
+    	if y1 > h-1 then y1 = h-1 end
 
-function init()
-	matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
-	matDirt = CreateMaterial("dirt", 0.66, 0.57, 0.42, 1, 0, 0.1)
-	matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
-	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
-	
-	LoadImage(file)
-	
-	w,h = GetImageSize()
-
-	local maxSize = tileSize
-	
-	local y0 = 0
-	while y0 < h-1 do
-		local y1 = y0 + maxSize
-		if y1 > h-1 then y1 = h-1 end
-
-		local x0 = 0
-		while x0 < w-1 do
-			local x1 = x0 + maxSize
-			if x1 > w-1 then x1 = w-1 end
-			Vox(x0, 0, y0)
-			Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
-			x0 = x1
-		end
-		y0 = y1
-	end
+    	local x0 = 0
+    	while x0 < w-1 do
+    		local x1 = x0 + maxSize
+    		if x1 > w-1 then x1 = w-1 end
+    		Vox(x0, 0, y0)
+    		Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
+    		x0 = x1
+    	end
+    	y0 = y1
+    end
 end
 

```

---

# Migration Report: voxscriptText\voxscriptText.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/voxscriptText\voxscriptText.lua
+++ patched/voxscriptText\voxscriptText.lua
@@ -1,62 +1,4 @@
-
-picPath = GetString("file", "text.png", "script png")
-content = GetString("content", "Text")
-gapX, gapY = GetInt("spacing", 1, 2)
-wrapL = GetInt("warp", 0)
-matParam = GetString("material", "masonry")
-textR, textG, textB, textA = GetFloat("color", 1, 1, 1, 1)
-pbrR, pbrS, pbrM, pbrE = GetFloat("pbr", 0, 0, 0, 0)
-
-
-charList = {
-	"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
-	"abcdefghijklmnopqrstuvwxyz",
-	"0123456789",
-	")]{}:;,/\\'\"<>!?-_+=*#~&|@",
-	"([^.%"
-}
-
-
-function init()
-	if picPath ~= "" then
-		LoadImage(picPath)
-		picW, picH = GetImageSize()
-		GetFontSize()
-		picMat = CreateMaterial(matParam, textR, textG, textB, textA, pbrR, pbrS, pbrM, pbrE)
-
-		local contentLen = string.len(content)
-
-		for c=1, contentLen do
-			local char = string.sub(content, c, c)
-			local charPos
-			local textX, textY = ((c-1)%wrapL)*(gapX+fontW), -math.floor((c-1)/wrapL)*(fontH+gapY)
-			if wrapL == 0 then
-				textX, textY = (c-1)*(gapX+fontW), 0
-			end
-
-			if char ~= " " then
-				for l=1, #charList do
-					if char == "(" then charPos = 1 end
-					if char == "[" then charPos = 2 end
-					if char == "^" then charPos = 3 end
-					if char == "." then charPos = 4 end
-					if char == "%" then charPos = 5 end
-					if charPos then
-						CreateText(textX, textY, (charPos-1)*(fontW+1), (fontH+1)*5)
-						break
-					end
-					charPos = string.find(charList[l], char)
-					if charPos then
-						CreateText(textX, textY, (charPos-1)*(fontW+1), (fontH+1)*l)
-						break
-					end
-				end
-			end
-		end
-	end
-end
-
-
+#version 2
 function GetFontSize()
 	fontW, fontH = 0, 0
 	for x=0, picW do
@@ -88,4 +30,44 @@
 			end
 		end
 	end
-end+end
+
+function server.init()
+    if picPath ~= "" then
+    	LoadImage(picPath)
+    	picW, picH = GetImageSize()
+    	GetFontSize()
+    	picMat = CreateMaterial(matParam, textR, textG, textB, textA, pbrR, pbrS, pbrM, pbrE)
+
+    	local contentLen = string.len(content)
+
+    	for c=1, contentLen do
+    		local char = string.sub(content, c, c)
+    		local charPos
+    		local textX, textY = ((c-1)%wrapL)*(gapX+fontW), -math.floor((c-1)/wrapL)*(fontH+gapY)
+    		if wrapL == 0 then
+    			textX, textY = (c-1)*(gapX+fontW), 0
+    		end
+
+    		if char ~= " " then
+    			for l=1, #charList do
+    				if char == "(" then charPos = 1 end
+    				if char == "[" then charPos = 2 end
+    				if char == "^" then charPos = 3 end
+    				if char == "." then charPos = 4 end
+    				if char == "%" then charPos = 5 end
+    				if charPos then
+    					CreateText(textX, textY, (charPos-1)*(fontW+1), (fontH+1)*5)
+    					break
+    				end
+    				charPos = string.find(charList[l], char)
+    				if charPos then
+    					CreateText(textX, textY, (charPos-1)*(fontW+1), (fontH+1)*l)
+    					break
+    				end
+    			end
+    		end
+    	end
+    end
+end
+

```
