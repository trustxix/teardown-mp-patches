# Migration Report: vox\bike\bike_jump.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\bike\bike_jump.lua
+++ patched/vox\bike\bike_jump.lua
@@ -1,138 +1,112 @@
-
-function init()
-
-
-bike = FindVehicle("bike")
-cooldown_jump = 0
-cooldown_wheelie = 300
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/bike/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("bike")
+    cooldown_jump = 0
+    cooldown_wheelie = 300
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-
-
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-		
-								
-					
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift")then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,7, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q")then  --if driving
-			local vel2 = Vec(0 ,14, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				cooldown_wheelie = cooldown_wheelie - 1 
-				else if InputDown("shift") and cooldown_wheelie == 0 then
-				cooldown_wheelie = 0
-				else if cooldown_wheelie < 300 then
-				cooldown_wheelie = cooldown_wheelie + 10
-				end
-			end
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-8, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-				
-			
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        	end
+        end 
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/bike/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift")then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,7, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q")then  --if driving
+    	local vel2 = Vec(0 ,14, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
+    		cooldown_wheelie = cooldown_wheelie - 1 
+    		else if InputDown("shift") and cooldown_wheelie == 0 then
+    		cooldown_wheelie = 0
+    		else if cooldown_wheelie < 300 then
+    		cooldown_wheelie = cooldown_wheelie + 10
+    		end
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-8, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "bike") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Wheelie"}
+    	info[#info+1] = {"Control", "Air Trick"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "bike") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Wheelie"}
-		info[#info+1] = {"Control", "Air Trick"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	
-	end
-end+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+    	UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+
+    end
+end
+

```

---

# Migration Report: vox\bike_blue\bike_jump_blue.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\bike_blue\bike_jump_blue.lua
+++ patched/vox\bike_blue\bike_jump_blue.lua
@@ -1,138 +1,112 @@
-
-function init()
-
-
-bike = FindVehicle("bike_blue")
-cooldown_jump = 0
-cooldown_wheelie = 300
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/bike_blue/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("bike_blue")
+    cooldown_jump = 0
+    cooldown_wheelie = 300
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-				
-		
-		
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-			
-				
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-		
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,7, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
-			local vel2 = Vec(0 ,5.9, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				cooldown_wheelie = cooldown_wheelie - 1 
-				else if InputDown("shift") and cooldown_wheelie == 0 then
-				cooldown_wheelie = 0
-				else if cooldown_wheelie < 300 then
-				cooldown_wheelie = cooldown_wheelie + 10
-				end
-			end
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-8, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-						
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        	end
+        end 
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/bike_blue/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,7, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
+    	local vel2 = Vec(0 ,5.9, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
+    		cooldown_wheelie = cooldown_wheelie - 1 
+    		else if InputDown("shift") and cooldown_wheelie == 0 then
+    		cooldown_wheelie = 0
+    		else if cooldown_wheelie < 300 then
+    		cooldown_wheelie = cooldown_wheelie + 10
+    		end
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-8, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "bike_blue") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Wheelie"}
+    	info[#info+1] = {"Control", "Air Trick"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "bike_blue") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Wheelie"}
-		info[#info+1] = {"Control", "Air Trick"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		
-			UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	end
-end+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+
+    		UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: vox\bike_blue no wheel\bike_jump_blue.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\bike_blue no wheel\bike_jump_blue.lua
+++ patched/vox\bike_blue no wheel\bike_jump_blue.lua
@@ -1,138 +1,112 @@
-
-function init()
-
-
-bike = FindVehicle("bike_blue")
-cooldown_jump = 0
-cooldown_wheelie = 300
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/bike_blue/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("bike_blue")
+    cooldown_jump = 0
+    cooldown_wheelie = 300
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-				
-		
-		
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-			
-				
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-		
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,7, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
-			local vel2 = Vec(0 ,5.5, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				cooldown_wheelie = cooldown_wheelie - 1 
-				else if InputDown("shift") and cooldown_wheelie == 0 then
-				cooldown_wheelie = 0
-				else if cooldown_wheelie < 300 then
-				cooldown_wheelie = cooldown_wheelie + 10
-				end
-			end
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-8, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-						
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        	end
+        end 
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/bike_blue/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,7, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
+    	local vel2 = Vec(0 ,5.5, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
+    		cooldown_wheelie = cooldown_wheelie - 1 
+    		else if InputDown("shift") and cooldown_wheelie == 0 then
+    		cooldown_wheelie = 0
+    		else if cooldown_wheelie < 300 then
+    		cooldown_wheelie = cooldown_wheelie + 10
+    		end
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-8, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "bike_blue") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Wheelie"}
+    	info[#info+1] = {"Control", "Air Trick"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "bike_blue") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Wheelie"}
-		info[#info+1] = {"Control", "Air Trick"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		
-			UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	end
-end+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+
+    		UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: vox\bike_dude\bike_jump_blue.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\bike_dude\bike_jump_blue.lua
+++ patched/vox\bike_dude\bike_jump_blue.lua
@@ -1,138 +1,112 @@
-
-function init()
-
-
-bike = FindVehicle("bike_blue")
-cooldown_jump = 0
-cooldown_wheelie = 300
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/bike_dude/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("bike_blue")
+    cooldown_jump = 0
+    cooldown_wheelie = 300
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-				
-		
-		
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-			
-				
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-		
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,7, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
-			local vel2 = Vec(0 ,8, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				cooldown_wheelie = cooldown_wheelie - 1 
-				else if InputDown("shift") and cooldown_wheelie == 0 then
-				cooldown_wheelie = 0
-				else if cooldown_wheelie < 300 then
-				cooldown_wheelie = cooldown_wheelie + 10
-				end
-			end
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-8, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-						
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        	end
+        end 
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/bike_dude/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,7, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
+    	local vel2 = Vec(0 ,8, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
+    		cooldown_wheelie = cooldown_wheelie - 1 
+    		else if InputDown("shift") and cooldown_wheelie == 0 then
+    		cooldown_wheelie = 0
+    		else if cooldown_wheelie < 300 then
+    		cooldown_wheelie = cooldown_wheelie + 10
+    		end
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-8, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "bike_blue") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Wheelie"}
+    	info[#info+1] = {"Control", "Air Trick"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "bike_blue") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Wheelie"}
-		info[#info+1] = {"Control", "Air Trick"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		
-			UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	end
-end+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+
+    		UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: vox\bike_trike\bike_trike_jump.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\bike_trike\bike_trike_jump.lua
+++ patched/vox\bike_trike\bike_trike_jump.lua
@@ -1,131 +1,105 @@
-
-function init()
-
-
-bike = FindVehicle("bike_trike")
-cooldown_jump = 0
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/bike_trike/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("bike_trike")
+    cooldown_jump = 0
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-				
-		
-		
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-			
-				
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-		
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,7, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and not InputDown("q") then  --if driving
-			local vel2 = Vec(0 ,18, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-8, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-						
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/bike_trike/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,7, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and not InputDown("q") then  --if driving
+    	local vel2 = Vec(0 ,18, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
 
+    end 
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-8, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "bike_trike") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Fly"}
-		info[#info+1] = {"Control", "Air Trick"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		
-			UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	end
-end+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "bike_trike") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Fly"}
+    	info[#info+1] = {"Control", "Air Trick"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
+
+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+
+    		UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: vox\double_bike\double_bike_jump.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\double_bike\double_bike_jump.lua
+++ patched/vox\double_bike\double_bike_jump.lua
@@ -1,138 +1,112 @@
-
-function init()
-
-
-bike = FindVehicle("double_bike")
-cooldown_jump = 0
-cooldown_wheelie = 300
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/double_bike/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("double_bike")
+    cooldown_jump = 0
+    cooldown_wheelie = 300
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-				
-		
-		
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-			
-				
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-		
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,7, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q")then  --if driving
-			local vel2 = Vec(0 ,10, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				cooldown_wheelie = cooldown_wheelie - 1 
-				else if InputDown("shift") and cooldown_wheelie == 0 then
-				cooldown_wheelie = 0
-				else if cooldown_wheelie < 300 then
-				cooldown_wheelie = cooldown_wheelie + 10
-				end
-			end
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-8, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-						
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        	end
+        end 
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/double_bike/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,7, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q")then  --if driving
+    	local vel2 = Vec(0 ,10, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
+    		cooldown_wheelie = cooldown_wheelie - 1 
+    		else if InputDown("shift") and cooldown_wheelie == 0 then
+    		cooldown_wheelie = 0
+    		else if cooldown_wheelie < 300 then
+    		cooldown_wheelie = cooldown_wheelie + 10
+    		end
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-8, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "double_bike") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Wheelie"}
+    	info[#info+1] = {"Control", "Air Trick"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "double_bike") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Wheelie"}
-		info[#info+1] = {"Control", "Air Trick"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		
-			UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	end
-end+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+
+    		UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: vox\double_bike_dudes\double_bike_jump.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\double_bike_dudes\double_bike_jump.lua
+++ patched/vox\double_bike_dudes\double_bike_jump.lua
@@ -1,137 +1,111 @@
-
-function init()
-
-
-bike = FindVehicle("double_bike")
-cooldown_jump = 0
-cooldown_wheelie = 300
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/double_bike/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("double_bike")
+    cooldown_jump = 0
+    cooldown_wheelie = 300
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-				
-		
-		
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-			
-				
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-		
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,15, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q")then  --if driving
-			local vel2 = Vec(0 ,26, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				cooldown_wheelie = cooldown_wheelie - 1 
-				else if InputDown("shift") and cooldown_wheelie == 0 then
-				cooldown_wheelie = 0
-				else if cooldown_wheelie < 300 then
-				cooldown_wheelie = cooldown_wheelie + 10
-				end
-			end
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-22, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-						
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5.3,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5.3,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        	end
+        end 
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/double_bike/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,15, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q")then  --if driving
+    	local vel2 = Vec(0 ,26, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
+    		cooldown_wheelie = cooldown_wheelie - 1 
+    		else if InputDown("shift") and cooldown_wheelie == 0 then
+    		cooldown_wheelie = 0
+    		else if cooldown_wheelie < 300 then
+    		cooldown_wheelie = cooldown_wheelie + 10
+    		end
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-22, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5.3,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5.3,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "double_bike") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Wheelie/Pick Up"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "double_bike") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Wheelie/Pick Up"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		
-			UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	end
-end+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+
+    		UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: vox\gentleman_bike\gentleman_bike_jump.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vox\gentleman_bike\gentleman_bike_jump.lua
+++ patched/vox\gentleman_bike\gentleman_bike_jump.lua
@@ -1,138 +1,112 @@
-
-function init()
-
-
-bike = FindVehicle("gentleman_bike")
-cooldown_jump = 0
-cooldown_wheelie = 300
-wheel_point = FindBody("wheel_point")
-horn = LoadSound("MOD/vox/gentleman_bike/bike-horn.ogg")
-
+#version 2
+function server.init()
+    bike = FindVehicle("gentleman_bike")
+    cooldown_jump = 0
+    cooldown_wheelie = 300
+    wheel_point = FindBody("wheel_point")
 end
 
-
-
-function tick(dt)
-		
-		local body = GetVehicleBody(bike)
-		local vehicle = GetPlayerVehicle()
-				
-		
-		
-		local wheel_point_loc = GetBodyTransform(wheel_point)
-		local camera = GetCameraTransform()  
-
-		
-		local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
-		local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
-		start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
-			direction1 = VecSub(goal_Pos,start_pos)
-				direction1 = VecScale(direction1,4)			
-		goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
-			
-				
-		if InputPressed("mmb") and vehicle == bike then
-		Shoot(start_pos, direction1, "shotgun", 8,200)
-		PlaySound(horn, start_pos, 0.5)	
-		end
-
-		
-
-
-
-		if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
-			local linVel = GetBodyVelocity(body)
-			local vel = Vec(0 ,7, 0)
-				SetBodyVelocity(body, VecAdd(vel,linVel))
-				cooldown_jump = 60
-			end
-
-		if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
-			local vel2 = Vec(0 ,11.5, 0)
-			local linVel = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
-				cooldown_wheelie = cooldown_wheelie - 1 
-				else if InputDown("shift") and cooldown_wheelie == 0 then
-				cooldown_wheelie = 0
-				else if cooldown_wheelie < 300 then
-				cooldown_wheelie = cooldown_wheelie + 10
-				end
-			end
-		end 
-
-		if InputDown("ctrl") and vehicle == bike then  --if driving
-			local vel3 = Vec(0 ,-8, 0)
-			local linVel3 = GetBodyVelocity(body)
-				SetBodyVelocity(wheel_point, vel3)
-				
-						
-		end 
-		
-		
-		if InputDown("lmb") and vehicle == bike then  --if driving
-				 angVel = Vec(0,5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if InputDown("rmb") and vehicle == bike then  --if driving
-								 angVel = Vec(0,-5,0)
-				SetBodyAngularVelocity(body, angVel)
-				end 
-
-		if cooldown_jump ~= 0 then
-			cooldown_jump = cooldown_jump - 1
-			end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local body = GetVehicleBody(bike)
+        local vehicle = GetPlayerVehicle(playerId)
+        local wheel_point_loc = GetBodyTransform(wheel_point)
+        local camera = GetCameraTransform()  
+        local aim_pos = TransformToParentPoint(camera, Vec(0, 0, -7))
+        local hit, dist, normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aim_pos, camera.pos)), 50,0, true)
+        start_pos = TransformToParentPoint(camera, Vec(0, 0, 0))	 
+        	direction1 = VecSub(goal_Pos,start_pos)
+        		direction1 = VecScale(direction1,4)			
+        goal_Pos = TransformToParentPoint(camera, Vec(0, 0, -dist))  
+        	end
+        end 
+        if cooldown_jump ~= 0 then
+        	cooldown_jump = cooldown_jump - 1
+        	end
+    end
 end
 
-
-
-
-
-
-function update(dt)
+function client.init()
+    horn = LoadSound("MOD/vox/gentleman_bike/bike-horn.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("mmb") and vehicle == bike then
+    Shoot(start_pos, direction1, "shotgun", 8,200)
+    PlaySound(horn, start_pos, 0.5)	
+    end
+    if InputPressed("q") and vehicle == bike and cooldown_jump == 0 and not InputDown("shift") then  --if driving
+    	local linVel = GetBodyVelocity(body)
+    	local vel = Vec(0 ,7, 0)
+    		SetBodyVelocity(body, VecAdd(vel,linVel))
+    		cooldown_jump = 60
+    	end
+    if InputDown("shift") and vehicle == bike and cooldown_wheelie ~= 0 and not InputDown("q") then  --if driving
+    	local vel2 = Vec(0 ,11.5, 0)
+    	local linVel = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, VecAdd(vel2,linVel))
+    		cooldown_wheelie = cooldown_wheelie - 1 
+    		else if InputDown("shift") and cooldown_wheelie == 0 then
+    		cooldown_wheelie = 0
+    		else if cooldown_wheelie < 300 then
+    		cooldown_wheelie = cooldown_wheelie + 10
+    		end
+    if InputDown("ctrl") and vehicle == bike then  --if driving
+    	local vel3 = Vec(0 ,-8, 0)
+    	local linVel3 = GetBodyVelocity(body)
+    		SetBodyVelocity(wheel_point, vel3)
 
+    end 
+    if InputDown("lmb") and vehicle == bike then  --if driving
+    		 angVel = Vec(0,5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+    if InputDown("rmb") and vehicle == bike then  --if driving
+    						 angVel = Vec(0,-5,0)
+    		SetBodyAngularVelocity(body, angVel)
+    		end 
+end
 
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "gentleman_bike") then
+    	local info = {}
+           info[#info+1] = {"Q", "Jump"}
+    	info[#info+1] = {"Shift", "Wheelie"}
+    	info[#info+1] = {"Control", "Air Trick"}
+    	info[#info+1] = {"LMB", "Spin Left"}
+    	info[#info+1] = {"RMB", "Spin Right"}
+    	info[#info+1] = {"MMB", "Horn"}
 
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "gentleman_bike") then
-		local info = {}
-        info[#info+1] = {"Q", "Jump"}
-		info[#info+1] = {"Shift", "Wheelie"}
-		info[#info+1] = {"Control", "Air Trick"}
-		info[#info+1] = {"LMB", "Spin Left"}
-		info[#info+1] = {"RMB", "Spin Right"}
-		info[#info+1] = {"MMB", "Horn"}
-		
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(150, 32)
-			UiColor(1,1,1)
-			for i=1, #info do
-				local key = info[i][1]
-				local func = info[i][2]
-				UiFont("bold.ttf", 22)
-				UiAlign("right")
-				UiText(key)
-				UiTranslate(10, 0)
-				UiFont("regular.ttf", 22)
-				UiAlign("left")
-				UiText(func)
-				UiTranslate(-10, 22)
-			end
-		UiPop()
-		
-			UiPush()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("dot.png")
-		UiPop()
-	end
-end+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(150, 32)
+    		UiColor(1,1,1)
+    		for i=1, #info do
+    			local key = info[i][1]
+    			local func = info[i][2]
+    			UiFont("bold.ttf", 22)
+    			UiAlign("right")
+    			UiText(key)
+    			UiTranslate(10, 0)
+    			UiFont("regular.ttf", 22)
+    			UiAlign("left")
+    			UiText(func)
+    			UiTranslate(-10, 22)
+    		end
+    	UiPop()
+
+    		UiPush()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("dot.png")
+    	UiPop()
+    end
+end
+

```
