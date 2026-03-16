# Migration Report: fire.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/fire.lua
+++ patched/fire.lua
@@ -1,16 +1,17 @@
-
-
-function init()
-	
-	body = FindBody("")
-	SpawnFire(GetBodyTransform(body).pos)
-	firetime = 0
+#version 2
+function server.init()
+    body = FindBody("")
+    firetime = 0
 end
 
+function client.init()
+    SpawnFire(GetBodyTransform(body).pos)
+end
 
-function tick(dt)
-	if firetime < 1 and not IsBodyBroken(body) then
-		firetime = firetime + dt
-		SpawnFire(GetBodyTransform(body).pos)
-	end	
-end+function client.tick(dt)
+    if firetime < 1 and not IsBodyBroken(body) then
+    	firetime = firetime + dt
+    	SpawnFire(GetBodyTransform(body).pos)
+    end	
+end
+

```

---

# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,119 +1,7 @@
-#include "registry.lua"
-
+#version 2
 function rnd(mi,ma)
 	return math.random(0,1000)/1000*(ma-mi)+mi
 end
-
-
-
-function init()
-	
-	vehicle_status = {}
-	fueltank_list={}
-
-	--regGetFloat('reinforce.strength')
-	
-	fuelfire = regGetFloat('effect.fuel') --40	
-	enginefire = regGetFloat('effect.engine') --40	
-	ammorackfire = regGetFloat('effect.ammorack') --70
-	destroyhealth = regGetFloat('effect.health')/100 --0.85
-	
-end
-
-
-function tick(dt)
-
-	--DebugPrint(fuelfire)
-	--DebugPrint(enginefire)	
-
-
-	all_tabs_vehicles = FindVehicles("TABS", true)
-		
-	for i=1,#all_tabs_vehicles do
-		local v = all_tabs_vehicles[i]
-		
-		if IsHandleValid(v) and not HasTag(v,"burning_end") then			
-			if vehicle_status[v] == nil and not HasTag(v,"nodrive") and #GetEntityChildren(v, "", true, "wheel") > 0 then -- nodrive added
-				eachvehicle(v)
-			end
-	
-			local vInfo = vehicle_status[v]	
-			if vInfo ~= nil then
-				working(v,vInfo,dt)
-			end		
-		end					
-	end	
-
-
-
-
-	fueltanks = FindShapes("Fuel_Size",true)			
-	for i=1, #fueltanks do
-		local fueltank = fueltanks[i]
-		if tonumber(GetTagValue(fueltank,"Fuel_Size")) > 20 then
-			if not IsShapeBroken(fueltank) then
-				local exists = false
-				for _, entry in ipairs(fueltank_list) do
-					if entry.shape == fueltank then
-						exists = true
-						break
-					end
-				end
-				if not exists then
-					table.insert(fueltank_list, { shape = fueltank, burntime = 0 })
-				end
-			end						
-		end
-	end
-
-
-
-	if #fueltank_list > 0 then
-
-		for i = #fueltank_list, 1, -1 do
-			local entry = fueltank_list[i]
-			local fueltank = entry.shape
-			if IsShapeBroken(fueltank) then
-				if entry.burntime < fuelfire then
-					entry.burntime = entry.burntime + dt					
-					local min, max = GetShapeBounds(fueltank)
-					local center = VecLerp(min, max, 0.5)
-					QueryRejectVehicle(GetBodyVehicle(GetShapeBody(fueltank)))
-					local lookdir = Vec(0,-1,0)--TransformToLocalVec(Transform(center),Vec(0,-1,0))
-					local hit, dist, normal, shape = QueryRaycast(center, lookdir, 10)	
-					
-					local hit_pos = VecAdd(center, VecScale(lookdir, dist))
-
-
-					if entry.lastspawn == nil then
-						entry.lastspawn = 0
-					end
-
-					if entry.burntime - entry.lastspawn >= 0.1 then
-						entry.lastspawn = entry.burntime 	
-
-						if hit and not HasTag(shape,"firewood") then
-							local fire = Spawn("MOD/xml/fire.xml", Transform(hit_pos))[3]
-							SetShapeCollisionFilter(fire, 2, 255-2)					
-						end						
-					end
-					
-				else				
-					table.remove(fueltank_list, i)				
-				end
-			end
-		end	
-	
-	end
-
-
-
-
-
-end
-
-
-
 
 function working(v,vInfo,dt)
 
@@ -178,7 +66,6 @@
 		
 		-- if fuel size is over than 100 than -> buring fuel drops
 
-
 		if HasTag(v,"nodrive") or GetVehicleHealth(v) < destroyhealth and not HasTag(v,"nodrive") then 
 			if vInfo.burning_time < ammorackfire then
 				vInfo.burning_time = vInfo.burning_time + dt
@@ -202,9 +89,7 @@
 	
 end
 
-
 function eachvehicle(v)
-
 
 	vehicle_status[v]={
 		vehicle = nil,
@@ -214,12 +99,6 @@
 		burning_time = 0,
 	}
 end
-
---DebugPrint
-
-
-
-
 
 function firesetting(pos,dt) --for engine
 			local shapeCenter1 = pos			
@@ -238,7 +117,6 @@
 			end				
 end
 
-
 function firesetting_V(pos,dt) --for vehicle
 			local shapeCenter1 = pos			
 			--SpawnFire(shapeCenter1)
@@ -293,5 +171,87 @@
 			end
 			--PointLight(shapeCenter1.pos, 255, .20, .0130, 5)					
 
-
-end+end
+
+function server.init()
+    vehicle_status = {}
+    fueltank_list={}
+    --regGetFloat('reinforce.strength')
+    fuelfire = regGetFloat('effect.fuel') --40	
+    enginefire = regGetFloat('effect.engine') --40	
+    ammorackfire = regGetFloat('effect.ammorack') --70
+    destroyhealth = regGetFloat('effect.health')/100 --0.85
+end
+
+function server.tick(dt)
+    all_tabs_vehicles = FindVehicles("TABS", true)
+    for i=1,#all_tabs_vehicles do
+    	local v = all_tabs_vehicles[i]
+
+    	if IsHandleValid(v) and not HasTag(v,"burning_end") then			
+    		if vehicle_status[v] == nil and not HasTag(v,"nodrive") and #GetEntityChildren(v, "", true, "wheel") > 0 then -- nodrive added
+    			eachvehicle(v)
+    		end
+
+    		local vInfo = vehicle_status[v]	
+    		if vInfo ~= nil then
+    			working(v,vInfo,dt)
+    		end		
+    	end					
+    end	
+    fueltanks = FindShapes("Fuel_Size",true)			
+    for i=1, #fueltanks do
+    	local fueltank = fueltanks[i]
+    	if tonumber(GetTagValue(fueltank,"Fuel_Size")) > 20 then
+    		if not IsShapeBroken(fueltank) then
+    			local exists = false
+    			for _, entry in ipairs(fueltank_list) do
+    				if entry.shape == fueltank then
+    					exists = true
+    					break
+    				end
+    			end
+    			if not exists then
+    				table.insert(fueltank_list, { shape = fueltank, burntime = 0 })
+    			end
+    		end						
+    	end
+    end
+    if #fueltank_list ~= 0 then
+
+    	for i = #fueltank_list, 1, -1 do
+    		local entry = fueltank_list[i]
+    		local fueltank = entry.shape
+    		if IsShapeBroken(fueltank) then
+    			if entry.burntime < fuelfire then
+    				entry.burntime = entry.burntime + dt					
+    				local min, max = GetShapeBounds(fueltank)
+    				local center = VecLerp(min, max, 0.5)
+    				QueryRejectVehicle(GetBodyVehicle(GetShapeBody(fueltank)))
+    				local lookdir = Vec(0,-1,0)--TransformToLocalVec(Transform(center),Vec(0,-1,0))
+    				local hit, dist, normal, shape = QueryRaycast(center, lookdir, 10)	
+
+    				local hit_pos = VecAdd(center, VecScale(lookdir, dist))
+
+    				if entry.lastspawn == nil then
+    					entry.lastspawn = 0
+    				end
+
+    				if entry.burntime - entry.lastspawn >= 0.1 then
+    					entry.lastspawn = entry.burntime 	
+
+    					if hit and not HasTag(shape,"firewood") then
+    						local fire = Spawn("MOD/xml/fire.xml", Transform(hit_pos))[3]
+    						SetShapeCollisionFilter(fire, 2, 255-2)					
+    					end						
+    				end
+
+    			else				
+    				table.remove(fueltank_list, i)				
+    			end
+    		end
+    	end	
+
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
@@ -1,76 +1,4 @@
-#include "registry.lua"
-
-function init()
-	checkRegInitialized()
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-	UiColor(1, 1, 1)
-	UiFont("bold.ttf", 48)
-	UiText("TABS Effect")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	local done = false
-	UiPush()
-		UiText("Fuel leak time")
-		UiTranslate(0, 40)
-		local val = regGetFloat('effect.fuel')
-		val, done = optionsSlider(val, 1, 200)
-		if done then
-			regSetFloat('effect.fuel', val)
-		end
-
-		UiTranslate(0, 40)
-		
-		UiColor(1, 1, 1)
-		UiText("Engine smoke time")
-		UiTranslate(0, 40)
-		local val2 = regGetFloat('effect.engine')
-		val2, done = optionsSlider(val2, 1, 200)
-		if done then
-			regSetFloat('effect.engine', val2)
-		end		
-
-
-		UiTranslate(0, 40)
-		
-		UiColor(1, 1, 1)
-		UiText("Destroyed hull fire time")
-		UiTranslate(0, 40)
-		local val3 = regGetFloat('effect.ammorack')
-		val3, done = optionsSlider(val3, 1, 200)
-		if done then
-			regSetFloat('effect.ammorack', val3)
-		end	
-
-		UiTranslate(0, 40)
-
-		
-		UiColor(1, 1, 1)
-		UiText("Vehicle HP to Start Fire (%)")
-		UiTranslate(0, 40)
-		local val4 = regGetFloat('effect.health')
-		val4, done = optionsSlider(val4, 1, 100)
-		if done then
-			regSetFloat('effect.health', val4)
-		end	
-		
-	
-		UiTranslate(0, 40)
-		
-
-		UiColor(1, 1, 1)
-		UiText("ESC = Exit from the option")
-		UiTranslate(0, 40)
-	UiPop()
-	
-end
-
-
-	
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	local w = 300 --195
@@ -95,4 +23,68 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    checkRegInitialized()
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+    UiColor(1, 1, 1)
+    UiFont("bold.ttf", 48)
+    UiText("TABS Effect")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    local done = false
+    UiPush()
+    	UiText("Fuel leak time")
+    	UiTranslate(0, 40)
+    	local val = regGetFloat('effect.fuel')
+    	val, done = optionsSlider(val, 1, 200)
+    	if done then
+    		regSetFloat('effect.fuel', val, true)
+    	end
+
+    	UiTranslate(0, 40)
+
+    	UiColor(1, 1, 1)
+    	UiText("Engine smoke time")
+    	UiTranslate(0, 40)
+    	local val2 = regGetFloat('effect.engine')
+    	val2, done = optionsSlider(val2, 1, 200)
+    	if done then
+    		regSetFloat('effect.engine', val2, true)
+    	end		
+
+    	UiTranslate(0, 40)
+
+    	UiColor(1, 1, 1)
+    	UiText("Destroyed hull fire time")
+    	UiTranslate(0, 40)
+    	local val3 = regGetFloat('effect.ammorack')
+    	val3, done = optionsSlider(val3, 1, 200)
+    	if done then
+    		regSetFloat('effect.ammorack', val3, true)
+    	end	
+
+    	UiTranslate(0, 40)
+
+    	UiColor(1, 1, 1)
+    	UiText("Vehicle HP to Start Fire (%)")
+    	UiTranslate(0, 40)
+    	local val4 = regGetFloat('effect.health')
+    	val4, done = optionsSlider(val4, 1, 100)
+    	if done then
+    		regSetFloat('effect.health', val4, true)
+    	end	
+
+    	UiTranslate(0, 40)
+
+    	UiColor(1, 1, 1)
+    	UiText("ESC = Exit from the option")
+    	UiTranslate(0, 40)
+    UiPop()
+end
+

```

---

# Migration Report: registry.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/registry.lua
+++ patched/registry.lua
@@ -1,9 +1,10 @@
+#version 2
 function modReset()
 
-    regSetFloat('effect.fuel'  , 40)
-    regSetFloat('effect.engine'  , 40)
-    regSetFloat('effect.ammorack'  , 70)
-    regSetFloat('effect.health'  , 85)	
+    regSetFloat('effect.fuel'  , 40, true)
+    regSetFloat('effect.engine'  , 40, true)
+    regSetFloat('effect.ammorack'  , 70, true)
+    regSetFloat('effect.health'  , 85, true)	
 end
 
 function modSoftReset()
@@ -28,21 +29,22 @@
         -- Soft reset (only initialize registries that are not yet defined)
         modSoftReset()
     end
-    regSetString('savegame.mod.verison', currentVersion)
+    regSetString('savegame.mod.verison', currentVersion, true)
 end
 
 function regGetFloat(path)
     local p = 'savegame.mod.' .. path
     return GetFloat(p)
 end
-function regSetFloat(path, value)
+
+function regSetFloat(path, value, true)
     local p = 'savegame.mod.' .. path
     if softReset then
         if not HasKey(p) then
-            SetFloat(p, value)
+            SetFloat(p, value, true)
         end
     else
-        SetFloat(p, value)
+        SetFloat(p, value, true)
     end
 end
 
@@ -50,14 +52,15 @@
     local p = 'savegame.mod.' .. path
     return GetInt(p)
 end
-function regSetInt(path, value)
+
+function regSetInt(path, value, true)
     local p = 'savegame.mod.' .. path
     if softReset then
         if not HasKey(p) then
-            SetInt(p, value)
+            SetInt(p, value, true)
         end
     else
-        SetInt(p, value)
+        SetInt(p, value, true)
     end
 end
 
@@ -65,14 +68,15 @@
     local p = 'savegame.mod.' .. path
     return GetBool(p)
 end
-function regSetBool(path, value)
+
+function regSetBool(path, value, true)
     local p = 'savegame.mod.' .. path
     if softReset then
         if not HasKey(p) then
-            SetBool(p, value)
+            SetBool(p, value, true)
         end
     else
-        SetBool(p, value)
+        SetBool(p, value, true)
     end
 end
 
@@ -80,25 +84,26 @@
     local p = 'savegame.mod.' .. path
     return GetString(p)
 end
-function regSetString(path, value)
+
+function regSetString(path, value, true)
     local p = 'savegame.mod.' .. path
     if softReset then
         if not HasKey(p) then
-            SetString(p, value)
+            SetString(p, value, true)
         end
     else
-        SetString(p, value)
+        SetString(p, value, true)
     end
 end
 
 function regInitKey(path, key)
     if softReset then
         if not HasKey(path) then
-            regSetString(path, key)
+            regSetString(path, key, true)
         end
     else
         if regGetString(path) == "" then
-            regSetString(path, key)
+            regSetString(path, key, true)
         end
     end
 end
@@ -130,14 +135,16 @@
     end
     return nil
 end
+
 function regSet(type, path, value)
     if type == "float" then
-        regSetFloat(path, value)
+        regSetFloat(path, value, true)
     elseif type == "int" then
-        regSetInt(path, value)
+        regSetInt(path, value, true)
     elseif type == "bool" then
-        regSetBool(path, value)
+        regSetBool(path, value, true)
     elseif type == "string" then
-        regSetString(path, value)
+        regSetString(path, value, true)
     end
-end+end
+

```
