# Migration Report: robots\fightingRobot.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/robots\fightingRobot.lua
+++ patched/robots\fightingRobot.lua
@@ -1,9 +1,4 @@
-
-robot = {}
-
-ACTIVE =1
-INACTIVE = 0
-
+#version 2
 function robot:initRobot(vehicle) 
 
 	if unexpected_condition then error() end
@@ -67,6 +62,7 @@
 		end
 	end
 end
+
 function robot:weaponFunctions(weapon) 
 	if(weapon.state == ACTIVE) then
 		SetJointMotor(weapon.joint, weapon.rpm)
@@ -76,25 +72,27 @@
 	end
 end
 
-
 function inVehicle(  )
 
 end
 
-function init()
-	DebugPrint("start")
-	vehicle = FindVehicle("cfg")
-	fightingRobot = robot
-	---robot:initRobot(robot)
-	fightingRobot:initRobot(vehicle)
-	 -- status,retVal = pcall(,vehicle)
-	DebugPrint("started")
+function server.init()
+    DebugPrint("start")
+    vehicle = FindVehicle("cfg")
+    fightingRobot = robot
+    ---robot:initRobot(robot)
+    fightingRobot:initRobot(vehicle)
+     -- status,retVal = pcall(,vehicle)
+    DebugPrint("started")
 end
 
-function tick(dt)
-	DebugWatch("vehicle:",fightingRobot.id)
-	if(fightingRobot.id~= 0 and GetPlayerVehicle()==fightingRobot.id)then
-		-- DebugPrint("test")
-		fightingRobot:tick(dt)
-	end
-end+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        DebugWatch("vehicle:",fightingRobot.id)
+        if(fightingRobot.id~= 0 and GetPlayerVehicle(playerId)==fightingRobot.id)then
+        	-- DebugPrint("test")
+        	fightingRobot:tick(dt)
+        end
+    end
+end
+

```

---

# Migration Report: scripts\AStarSearch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\AStarSearch.lua
+++ patched/scripts\AStarSearch.lua
@@ -1,184 +1,4 @@
-#include "priorityQueue.lua"
-#include "mapNode.lua"
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        AStarSearch.lua             
-*
-* DESCRIPTION :
-*       Implements A Star search in Teardown 2020
-*
-*       
-*
-*
-* NOTES :
-*
-*       Yes, i know while loops are bad. This can be optimised by 
-*       using for loops and making it async       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-*                            Release Date :    29 Nov 2021 
-*
-]]
-
-AStar = {
-    maxChecks = 1000,
-    cameFrom = {},
-    costSoFar = {},
-    maxIterations = 10,
-    currentIteration = 0,
-
-    heuristicWeight = 1
-
-}
-
-
-
-
-
-function AStar:Heuristic(a, b)
-      return (math.abs(a[1] - b[1]) + math.abs(a[2] - b[2])) * self.heuristicWeight
- end 
-
-
-
-function AStar:AStarSearch(graph, start, goal)
-    
-        frontier =  deepcopy(PriorityQueue)
-        frontier:init(#graph,#graph[1])
-        frontier:put(deepcopy(start), 0);
-
-        local startIndex = start:getIndex()
-        -- DebugPrint(type(start:getIndex()).." | "..type(start:getIndex()[2]))
-        -- DebugPrint("Val = " ..startIndex[1]..startIndex[2])
-        local cameFrom = {}
-        cameFrom[startIndex[2]] = {}
-        cameFrom[startIndex[2]][startIndex[1]] = start;
-        local lastIndex = nil
-        local costSoFar = {}
-        costSoFar[startIndex[2]] = {}
-        costSoFar[startIndex[2]][startIndex[1]] = start:getCost();
-
-        local current = nil
-        local currentIndex = nil
-        local nextNode = nil
-        local newCost = 0
-        local priority = 0
-        local currentIndex = nil
-        local nodeExists = false
-
-        local totalNodes = 0
-        -- DebugPrint(frontier:empty())
-        -- for i=1,self.maxChecks do 
-        local checks = 0
-        for i=1,frontier:size() do 
-       --- while not frontier:empty() do
-            checks = checks + 1
-        
-            current = deepcopy(frontier:get()) 
-
-            totalNodes = totalNodes + 1
-            if (type(current)~="table" or not current or  current:Equals(goal)) then
-                -- DebugPrint("goal found")
-                break
-            end  
-            currentIndex = current:getIndex()
-             for key, val in ipairs(current:getNeighbors()) do
-                    nextNode =  deepcopy(graph[val.y][val.x])
-                
-                    newCost = costSoFar[currentIndex[2]][currentIndex[1]] + nextNode:getCost()
-                    nodeExists = ( self:nodeExists(costSoFar,val.y,val.x) )
-                    if(nextNode.validTerrain and( not nodeExists or (not (cameFrom[currentIndex[2]][currentIndex[1]]:indexEquals({val.y,val.x}))  and 
-                                        newCost < costSoFar[val.y][val.x])) )
-                    then 
-                        if(not nodeExists) then 
-                            if(not costSoFar[val.y]) then 
-                                costSoFar[val.y] = {}
-                                cameFrom[val.y] = {}
-                            end
-                        end
-                        costSoFar[val.y][val.x] = newCost
-                        priority =   newCost +  self:Heuristic(nextNode:getIndex(),goal:getIndex())
-                        frontier:put(nextNode, priority)
-                        cameFrom[val.y][val.x] = deepcopy(current)
-
-                        -- DebugPrint(newCost.." | "..val.y.." | "..val.x.." | ")
-                        -- lastIndex = deepcopy(val)
-                        
-                        -- DebugPrint(nextNode:getIndex()[1].." | "..nextNode:getIndex()[2])
-                    --+ graph.Cost(current, next);
-                    end
-             end
-         end
-         -- DebugPrint("total checks = "..checks)
-         
-         local path = self:reconstructPath(graph,cameFrom,current,start,totalNodes)
-         -- DebugPrint("total nodes: "..totalNodes)
-         return path
- end
-
- function AStar:nodeExists(listVar,y,x)
-     if(listVar[y] and listVar[y][x]) then
-        return true
-    else
-        return false
-    end
- end
-
-function AStar:reconstructPath(graph,cameFrom,current,start,totalNodes)
-    local path = {}
-    local index = current:getIndex()
-    -- for i=1,100 do 
-    while not current:Equals(start) do
-    -- DebugPrint("came from: "..index[1].." | "..index[2])
-        path[#path+1] = index
-        index = cameFrom[current:getIndex()[2]][current:getIndex()[1]]:getIndex()
-        current = deepcopy(graph[index[2]][index[1]])
-        
-        if(current:Equals(start)) then
-                -- DebugPrint("found, nodes: "..totalNodes) 
-
-            break
-
-        end
-
-
-    end
-    local tmp = {}
-    for i = #path, 1, -1 do
-        tmp[#tmp+1] = path[i]
-    end
-    path = tmp
-    return path
-
-
-end
-
-
- function AStar:drawPath(graph,path)
-    local node1,node2 = nil,nil
-    for i = 1, #path-1 do
-        node1 = graph[path[i][2]][path[i][1]]:getPos()
-        node2 = graph[path[i+1][2]][path[i+1][1]]:getPos()
-        DebugLine(node1,node2, 1, 0, 0)
-    end
- end
-
- function AStar:drawPath2(graph,path,colours)
-    local node1,node2 = nil,nil
-
-    for i = 1, #path-1 do
-        node1 = graph[path[i][2]][path[i][1]]:getPos()
-        node2 = graph[path[i+1][2]][path[i+1][1]]:getPos()
-        DebugLine(node1,node2, 1,0,0)
-    end
- end
-
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -193,3 +13,4 @@
     end
     return copy
 end
+

```

---

# Migration Report: scripts\AVF_AI - Copy (2).lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\AVF_AI - Copy (2).lua
+++ patched/scripts\AVF_AI - Copy (2).lua
@@ -1,144 +1,4 @@
-
-detectRange = 4--2.5--3
-
-vehicle = 
-
-			{
-
-			}
-
-maxSpeed = 20
-
-
-goalPos = Vec(0,0,0)
-SPOTMARKED = false
-
-gCost = 1
-
-testHeight = 1
-drivePower = 0.75
-
-
-detectPoints ={
-
-}
-
-detectPoints = {
-	[1] = Vec(0,0,-detectRange*2),
-	[2] = Vec(detectRange,0,-detectRange),
-	[3] = Vec(-detectRange,0,-detectRange),
-	[4] = Vec(-detectRange,0,0),
-	[5] = Vec(detectRange,0,0),
-	[6] = Vec(0,0,detectRange),
-
-}
-
-weights = {}
-
-ai = {
-
-	commands = {
-	[1] = Vec(0,0,-detectRange*2),
-	[2] = Vec(detectRange*.7,0,-detectRange*1),
-	[3] = Vec(-detectRange*.7,0,-detectRange*1),
-	[4] = Vec(-detectRange,0,0),
-	[5] = Vec(detectRange,0,0),
-	[6] = Vec(0,0,detectRange*2),
-
-	},
-
-	weights = {
-
-	[1] = 0.845,
-	[2] = 0.85,
-	[3] = 0.85,
-	[4] = 0.5,
-	[5] = 0.5,
-	[6] = 0.6,
-
-			} ,
-
-	altChecks = Vec(00,0.4,-0.6),
-
-	altWeight ={
-			[1] = 1,
-			[2] =1,
-			[3] = -1,
-			[4] = -1,
-
-	}
-	--Vec(0.5,0,0.9)
-
-}
-weights = {
-
-	[1] = 0.845,
-	[2] = 0.85,
-	[3] = 0.85,
-	[4] = 0.5,
-	[5] = 0.5,
-	[6] = 0.25,
-
-}
-
-
-targetMoves = {
-	list        = {},
-	target      = Vec(0,0,0),
-	targetIndex = 1
-}
-
-
-
-
-hitColour = Vec(1,0,0)
-detectColour = Vec(1,1,0)
-clearColour = Vec(0,1,0)
-
-function init()
-
-	for i=1,10 do 
-		targetMoves.list[i] = Vec(0,0,0)
-
-	end
-
-	-- for i = 1,#ai.commands*1 do 
-	-- 	detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
-	-- 	detectPoints[i][2] = ai.altChecks[math.floor(i/#ai.commands)+1]
-	-- 	weights[i] = ai.weights[(i%#ai.commands)+1]*ai.altWeight[math.floor(i/#ai.commands)+1]
-
-	-- end
-
-	vehicle.id = FindVehicle("cfg")
-	local value = GetTagValue(vehicle.id, "cfg")
-	if(value == "ai") then
-
-		-- local status,retVal = pcall(initVehicle)
-		-- if status then 
-		-- 	DebugPrint("no errors")
-		-- else
-		-- 	DebugPrint(retVal)
-		-- end
-
-	end
-				
-end
-
-
-function tick(dt)
-
-		hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
-	if hit then
-	--local hitPoint = VecAdd(pos, VecScale(dir, dist))
-		local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
-		DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
-	end
-
-
-	markLoc()
-
-end
-
+#version 2
 function markLoc()
 	
 	if InputPressed("g") then
@@ -161,24 +21,6 @@
 		SpawnParticle("fire", goalPos, Vec(0,5,0), 0.5, 1)
 	end
 end
-
-function update(dt)
-
-
-	targetCost = vehicleDetection3()
-	-- DebugWatch("targetCost:",VecStr(targetCost.target ))
-
-	targetCost.target = MAV(targetCost.target)
-
-	DebugWatch("targetCost 2 :",VecStr(targetCost.target ))
-	controlVehicle(targetCost)
-
-	-- DebugWatch("Vehicle ",vehicle.id)
-	
-
-	-- DebugWatch("velocity:", VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id))))
-end
-
 
 function vehicleDetection4( )
 
@@ -293,7 +135,6 @@
 
 		    DebugLine(vehiclePos, fwdPos, lineColour[1], lineColour[2], lineColour[3])
 
-
 		end
 	end
 	return bestCost
@@ -364,7 +205,6 @@
 		    end
 		    DebugLine(vehicleTransform.pos, fwdPos, lineColour[1], lineColour[2], lineColour[3])
 
-
 		end
 	end
 	return bestCost
@@ -374,8 +214,6 @@
 	-- DebugLine(vehicleTransform.pos, fwdR, 1, 0, 0)
 
 end
-
-
 
 function vehicleDetection2( )
 
@@ -464,7 +302,6 @@
 
 end
 
-
 function MAV(targetCost)
 	targetMoves.targetIndex = (targetMoves.targetIndex%#targetMoves.list)+1 
 	targetMoves.target = VecSub(targetMoves.target,targetMoves.list[targetMoves.targetIndex])
@@ -499,7 +336,6 @@
 	end
 end
 
-
 function costFunc(testPos,hit,key)
 	local cost = 100 
 	if(not hit) then 
@@ -523,13 +359,6 @@
 	SetBodyAngularVelocity(vehicle.body, VecAdd(currentAngVel,targetAngVel))
 
 end
-
--- SetBodyVelocity(handle, velocity)
--- SetBodyAngularVelocity(body, angVel)
-
-
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -544,4 +373,51 @@
         copy = orig
     end
     return copy
-end+end
+
+function server.init()
+    for i=1,10 do 
+    	targetMoves.list[i] = Vec(0,0,0)
+
+    end
+    -- for i = 1,#ai.commands*1 do 
+    -- 	detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
+    -- 	detectPoints[i][2] = ai.altChecks[math.floor(i/#ai.commands)+1]
+    -- 	weights[i] = ai.weights[(i%#ai.commands)+1]*ai.altWeight[math.floor(i/#ai.commands)+1]
+    -- end
+    vehicle.id = FindVehicle("cfg")
+    local value = GetTagValue(vehicle.id, "cfg")
+    if(value == "ai") then
+
+    	-- local status,retVal = pcall(initVehicle)
+    	-- if status then 
+    	-- 	DebugPrint("no errors")
+    	-- else
+    	-- 	DebugPrint(retVal)
+    	-- end
+
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        	hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
+        if hit then
+        --local hitPoint = VecAdd(pos, VecScale(dir, dist))
+        	local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
+        	DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
+        end
+        markLoc()
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        targetCost = vehicleDetection3()
+        -- DebugWatch("targetCost:",VecStr(targetCost.target ))
+        targetCost.target = MAV(targetCost.target)
+        DebugWatch("targetCost 2 :",VecStr(targetCost.target ))
+        controlVehicle(targetCost)
+    end
+end
+

```

---

# Migration Report: scripts\AVF_AI - Copy.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\AVF_AI - Copy.lua
+++ patched/scripts\AVF_AI - Copy.lua
@@ -1,74 +1,4 @@
-
-detectRange = 5
-
-vehicle = 
-
-			{
-
-			}
-
-maxSpeed = 20
-
-
-goalPos = Vec(0,0,0)
-SPOTMARKED = false
-
-gCost = 1
-
-testHeight = 1
-drivePower = 0.5
-
-detectPoints = {
-	[1] = Vec(0,-0.2,-detectRange*1.2),
-	[2] = Vec(detectRange,-0.2,-detectRange),
-	[3] = Vec(-detectRange,-0.2,-detectRange),
-	[4] = Vec(-detectRange,-0.2,0),
-	[5] = Vec(detectRange,-0.2,0),
-	[6] = Vec(0,-0.2,detectRange*.5),
-
-}
-
-
-targetMoves = {
-	list        = {},
-	target      = Vec(0,0,0),
-	targetIndex = 1
-}
-
-
-
-
-hitColour = Vec(1,0,0)
-clearColour = Vec(0,1,0)
-
-function init()
-
-	for i=1,10 do 
-		targetMoves.list[i] = Vec(0,0,0)
-
-	end
-
-	vehicle.id = FindVehicle("cfg")
-	local value = GetTagValue(vehicle.id, "cfg")
-	if(value == "ai") then
-
-		-- local status,retVal = pcall(initVehicle)
-		-- if status then 
-		-- 	DebugPrint("no errors")
-		-- else
-		-- 	DebugPrint(retVal)
-		-- end
-
-	end
-				
-end
-
-
-function tick(dt)
-	markLoc()
-
-end
-
+#version 2
 function markLoc()
 	
 	if InputPressed("g") then
@@ -91,24 +21,6 @@
 		SpawnParticle("smoke", goalPos, Vec(0,5,0), 0.5, 1)
 	end
 end
-
-function update(dt)
-
-
-	targetCost = vehicleDetection2( )
-	DebugWatch("targetCost:",VecStr(targetCost ))
-
-	targetCost.target = MAV(targetCost.target)
-
-	DebugWatch("targetCost 2 :",VecStr(targetCost ))
-	controlVehicle(targetCost)
-
-	DebugWatch("Vehicle ",vehicle.id)
-	
-
-	DebugWatch("velocity:", VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id))))
-end
-
 
 function vehicleDetection2( )
 
@@ -197,7 +109,6 @@
 
 end
 
-
 function MAV(targetCost)
 	targetMoves.targetIndex = (targetMoves.targetIndex%#targetMoves.list)+1 
 	targetMoves.target = VecSub(targetMoves.target,targetMoves.list[targetMoves.targetIndex])
@@ -230,7 +141,6 @@
 	end
 end
 
-
 function costFunc(testPos,hit)
 	local cost = 100 
 	if(not hit) then 
@@ -255,5 +165,40 @@
 
 end
 
--- SetBodyVelocity(handle, velocity)
--- SetBodyAngularVelocity(body, angVel)+function server.init()
+    for i=1,10 do 
+    	targetMoves.list[i] = Vec(0,0,0)
+
+    end
+    vehicle.id = FindVehicle("cfg")
+    local value = GetTagValue(vehicle.id, "cfg")
+    if(value == "ai") then
+
+    	-- local status,retVal = pcall(initVehicle)
+    	-- if status then 
+    	-- 	DebugPrint("no errors")
+    	-- else
+    	-- 	DebugPrint(retVal)
+    	-- end
+
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        markLoc()
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        targetCost = vehicleDetection2( )
+        DebugWatch("targetCost:",VecStr(targetCost ))
+        targetCost.target = MAV(targetCost.target)
+        DebugWatch("targetCost 2 :",VecStr(targetCost ))
+        controlVehicle(targetCost)
+        DebugWatch("Vehicle ",vehicle.id)
+        DebugWatch("velocity:", VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id))))
+    end
+end
+

```

---

# Migration Report: scripts\AVF_AI.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\AVF_AI.lua
+++ patched/scripts\AVF_AI.lua
@@ -1,199 +1,4 @@
-
-
-detectRange = 4--2.5--3
-
-
-
-DEBUG 			= true
-VEHICLE_ACTIVE = true
-
-vehicle = 
-
-			{
-
-			}
-
-maxSpeed = 20
-
-goalOrigPos = Vec(0,0,0)
-goalPos = goalOrigPos
-
-maxLastCheckpoints = 1
-
-SPOTMARKED = false
-
-gCost = 1
-
-testHeight = 6
-drivePower = 5
-cornerDrivePower = 1
-steerPower  	= 3
-
-
-detectPoints = {
-	[1] = Vec(0,0,-detectRange),
-	[2] = Vec(detectRange,0,-detectRange),
-	[3] = Vec(-detectRange,0,-detectRange),
-	[4] = Vec(-detectRange,0,0),
-	[5] = Vec(detectRange,0,0),
-	[6] = Vec(0,0,detectRange),
-
-}
-
-weights = {
-
-	[1] = 0.85,
-	[2] = 0.85,
-	[3] = 0.85,
-	[4] = 0.5,
-	[5] = 0.5,
-	[6] = 0.25,
-
-}
-
-
-ai = {
-
-	commands = {
-	[1] = Vec(0,0,-detectRange*3),
-	[2] = Vec(detectRange*0.8,0,-detectRange*1.5),
-	[3] = Vec(-detectRange*0.8,0,-detectRange*1.5),
-	[4] = Vec(-detectRange,0,0),
-	[5] = Vec(detectRange,0,0),
-	[6] = Vec(0,0,detectRange),
-
-	},
-
-	weights = {
-
-	[1] = 0.870,
-	[2] = 0.86,
-	[3] = 0.86,
-	[4] = 0.84,
-	[5] = 0.84,
-	[6] = 0.80,
-
-			} ,
-
-	directions = {
-		forward = Vec(0,0,1),
-
-		back = Vec(0,0,-1),
-
-		left = Vec(1,0,0),
-
-		right = Vec(-1,0,0),
-	},
-
-	numScans = 7,
-	scanThreshold = 0.5,
-
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
-
-
-	validSurfaceColours ={ 
-			[1] = {
-				r = 0.20,
-				g = 0.20,
-				b = 0.20,
-				range = 0.02
-			},
-		}
-}
-targetMoves = {
-	list        = {},
-	target      = Vec(0,0,0),
-	targetIndex = 1
-}
-
-
-scan = 0
-scanCount = 5
-
-
-hitColour = Vec(1,0,0)
-detectColour = Vec(1,1,0)
-clearColour = Vec(0,1,0)
-
-
-RACESTARTED = false
-raceCheckpoint = 1
-currentCheckpoint = nil
-
-
-RESETMAX = 5
-resetTimer = RESETMAX 
-
-function init()
-
-	for i=1,3 do 
-		targetMoves.list[i] = Vec(0,0,0)
-
-	end
-
-	for i = 1,#ai.commands*1 do 
-		detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
-		if(i> #ai.commands) then
-			detectPoints[i] = VecScale(detectPoints[i],0.5)
-			detectPoints[i][2] = ai.altChecks[2]
-
-
-		else 
-			detectPoints[i][2] = ai.altChecks[1]
-		end
-		weights[i] = ai.weights[(i%#ai.commands)+1]--*ai.altWeight[math.floor(i/#ai.commands)+1]
-
-	end
-
-	vehicle.id = FindVehicle("cfg")
-	local value = GetTagValue(vehicle.id, "cfg")
-	if(value == "ai") then
-
-		-- local status,retVal = pcall(initVehicle)
-		-- if status then 
-		-- 	DebugPrint("no errors")
-		-- else
-		-- 	DebugPrint(retVal)
-		-- end
-
-	end
-				
-
-	checkpoints = FindTriggers("checkpoint",true)
-
-	for key,value in ipairs(checkpoints) do
-		if(tonumber(GetTagValue(value, "checkpoint"))==raceCheckpoint) then 
-			currentCheckpoint = value
-		end
-	end
-end
-
-
-function tick(dt)
-
-		hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
-	if hit then
-	--local hitPoint = VecAdd(pos, VecScale(dir, dist))
-		local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
-		DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
-	end
-
-
-	markLoc()
-
-end
-
+#version 2
 function markLoc()
 	
 	if InputPressed("g") and not RACESTARTED then
@@ -247,92 +52,7 @@
 
 	end
 
-
-end
-
-function update(dt)
-
-	if(VEHICLE_ACTIVE) then 
-		targetCost,onTrack = vehicleDetection7()
-		-- DebugWatch("targetCost:",VecStr(targetCost.target ))
-
-		targetCost.target = MAV(targetCost.target)
-
-		-- DebugWatch("targetCost 2 :",VecStr(targetCost.target ))
-
-		if(onTrack) then
-			controlVehicle(targetCost)
-		end
-	end
-
-	-- 	if(VEHICLE_ACTIVE) then 
-	-- 	targetCost = vehicleDetection3()
-	-- 	-- DebugWatch("targetCost:",VecStr(targetCost.target ))
-
-	-- 	targetCost.target = MAV(targetCost.target)
-
-	-- 	DebugWatch("targetCost 2 :",VecStr(targetCost.target ))
-	-- 	controlVehicle(targetCost)
-	-- end
-
-	 if(RACESTARTED and VEHICLE_ACTIVE and VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id)))<1) then
-	 	resetTimer = resetTimer -dt
-	 	if(resetTimer <=0 )then
-	 		local lastCheckpoint = raceCheckpoint-1
-			if(lastCheckpoint<=0) then
-				lastCheckpoint = 1
-			end
-				
-			for key,value in ipairs(checkpoints) do 
-				
-				if(tonumber(GetTagValue(value, "checkpoint"))== lastCheckpoint) then 
-					local resetTrigger = GetTriggerTransform(value)
-					resetTrigger.pos = TransformToParentPoint(resetTrigger,Vec(math.random(-7,7),0,math.random(-7,7)))   
-					SetBodyTransform(GetVehicleBody(vehicle.id),resetTrigger)
-					resetTimer = RESETMAX
-				end
-			end
-	 		
-
-	 	end
-	 elseif RACESTARTED and VEHICLE_ACTIVE and   resetTimer<RESETMAX then
-	 	resetTimer = RESETMAX
-	 elseif(RACESTARTED and VEHICLE_ACTIVE) then
-
-	 		local lastCheckpoint = raceCheckpoint-1
-			if(lastCheckpoint<=0) then
-				lastCheckpoint = #checkpoints
-			end
-
-	 		for key,value in ipairs(checkpoints) do 
-
-
-
-				DebugWatch("checkpoint",math.abs(lastCheckpoint-key))
-		 		if(raceCheckpoint ~=1 and IsVehicleInTrigger(value,vehicle.id) and math.abs(lastCheckpoint-tonumber(GetTagValue(value, "checkpoint")))>maxLastCheckpoints) then
-					for key,value in ipairs(checkpoints) do 
-				
-						if(tonumber(GetTagValue(value, "checkpoint"))== lastCheckpoint) then 
-							local resetTrigger = GetTriggerTransform(value)
-							resetTrigger.pos = TransformToParentPoint(resetTrigger,Vec(math.random(-7,7),0,math.random(-7,7)))   
-							SetBodyTransform(GetVehicleBody(vehicle.id),resetTrigger)
-							SetBodyVelocity(GetVehicleBody(vehicle.id),Vec(0,0,0))
-							resetTimer = RESETMAX
-						end
-					end
-				end
-
-			end
-
-	 end
-
-	-- DebugWatch("Vehicle ",vehicle.id)
-	
-
-	DebugWatch("velocity:", VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id))))
-end
-
-
+end
 
 function vehicleDetection7( )
 	onTrack = false
@@ -449,9 +169,6 @@
 
 end
 
-
-
-
 function vehicleDetection6( )
 	local vehicleBody = GetVehicleBody(vehicle.id)
 	local vehicleTransform = GetVehicleTransform(vehicle.id)
@@ -545,7 +262,6 @@
 		    
 		    DebugLine(vehicleTransform.pos, fwdPos, lineColour[1], lineColour[2], lineColour[3])
 
-
 		end
 	end
 	return bestCost
@@ -573,17 +289,12 @@
 
 	-- for i = 1,ai.numScans do 
 
-
 	-- end
 	return hit,dist,normal, shape
 
 end
 
-
-
 function costFunc2(testPos,hit,dist,shape,key)
-
-
 
 	local cost = 10000 
 	if(not hit) then
@@ -591,8 +302,6 @@
 	end
 	return cost
 end
-
-
 
 function vehicleDetection5( )
 
@@ -615,7 +324,6 @@
 	if(VecLength(goalPos)> 0.5 and VecLength(
 									VecSub(GetVehicleTransform(vehicle.id).pos,goalPos))>3) then	
 		for key,detect in ipairs(detectPoints) do 
-
 
 			--detect = VecScale(detect ,1+(clamp(0,100,math.log(VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id))))))*.5)
 
@@ -688,7 +396,6 @@
 		    end
 		    DebugLine(vehicleTransform.pos, fwdPos, lineColour[1], lineColour[2], lineColour[3])
 
-
 		end
 	end
 	return bestCost
@@ -699,8 +406,6 @@
 
 end
 
-
----QueryAabbShapes
 function vehicleDetection4( )
 
 	local vehicleBody = GetVehicleBody(vehicle.id)
@@ -814,7 +519,6 @@
 
 		    DebugLine(vehiclePos, fwdPos, lineColour[1], lineColour[2], lineColour[3])
 
-
 		end
 	end
 	return bestCost
@@ -824,8 +528,6 @@
 	-- DebugLine(vehicleTransform.pos, fwdR, 1, 0, 0)
 
 end
-
---- shapecast
 
 function vehicleDetection3( )
 
@@ -887,7 +589,6 @@
 		    end
 		    DebugLine(vehicleTransform.pos, fwdPos, lineColour[1], lineColour[2], lineColour[3])
 
-
 		end
 	end
 	return bestCost
@@ -897,8 +598,6 @@
 	-- DebugLine(vehicleTransform.pos, fwdR, 1, 0, 0)
 
 end
-
-
 
 function vehicleDetection2( )
 
@@ -987,7 +686,6 @@
 
 end
 
-
 function MAV(targetCost)
 	targetMoves.targetIndex = (targetMoves.targetIndex%#targetMoves.list)+1 
 	targetMoves.target = VecSub(targetMoves.target,targetMoves.list[targetMoves.targetIndex])
@@ -1025,7 +723,6 @@
 				targetMove[3] = targetMove[3] *2
 			end
 
-
 			DriveVehicle(vehicle.id, -targetMove[3]*drivePower,-targetMove[1], hBrake)
 			DebugWatch("post updated",VecStr(targetMove))
 			DebugWatch("motion2",VecStr(detectPoints[targetCost.key]))
@@ -1034,7 +731,6 @@
 		end
 	end
 end
-
 
 function costFunc(testPos,hit,key)
 	local cost = 10000 
@@ -1060,19 +756,10 @@
 
 end
 
--- SetBodyVelocity(handle, velocity)
--- SetBodyAngularVelocity(body, angVel)
-
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
-
-
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -1089,8 +776,6 @@
     return copy
 end
 
-
-
 function inRange(min,max,value)
 		if(min < value and value<=max) then 
 			return true
@@ -1099,4 +784,127 @@
 			return false
 		end
 
-end+end
+
+function server.init()
+    for i=1,3 do 
+    	targetMoves.list[i] = Vec(0,0,0)
+
+    end
+    for i = 1,#ai.commands*1 do 
+    	detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
+    	if(i> #ai.commands) then
+    		detectPoints[i] = VecScale(detectPoints[i],0.5)
+    		detectPoints[i][2] = ai.altChecks[2]
+
+    	else 
+    		detectPoints[i][2] = ai.altChecks[1]
+    	end
+    	weights[i] = ai.weights[(i%#ai.commands)+1]--*ai.altWeight[math.floor(i/#ai.commands)+1]
+
+    end
+    vehicle.id = FindVehicle("cfg")
+    local value = GetTagValue(vehicle.id, "cfg")
+    if(value == "ai") then
+
+    	-- local status,retVal = pcall(initVehicle)
+    	-- if status then 
+    	-- 	DebugPrint("no errors")
+    	-- else
+    	-- 	DebugPrint(retVal)
+    	-- end
+
+    end
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
+        	hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
+        if hit then
+        --local hitPoint = VecAdd(pos, VecScale(dir, dist))
+        	local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
+        	DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
+        end
+        markLoc()
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(VEHICLE_ACTIVE) then 
+        	targetCost,onTrack = vehicleDetection7()
+        	-- DebugWatch("targetCost:",VecStr(targetCost.target ))
+
+        	targetCost.target = MAV(targetCost.target)
+
+        	-- DebugWatch("targetCost 2 :",VecStr(targetCost.target ))
+
+        	if(onTrack) then
+        		controlVehicle(targetCost)
+        	end
+        end
+        -- 	if(VEHICLE_ACTIVE) then 
+        -- 	targetCost = vehicleDetection3()
+        -- 	-- DebugWatch("targetCost:",VecStr(targetCost.target ))
+        -- 	targetCost.target = MAV(targetCost.target)
+        -- 	DebugWatch("targetCost 2 :",VecStr(targetCost.target ))
+        -- 	controlVehicle(targetCost)
+        -- end
+         if(RACESTARTED and VEHICLE_ACTIVE and VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id)))<1) then
+         	resetTimer = resetTimer -dt
+         	if(resetTimer <=0 )then
+         		local lastCheckpoint = raceCheckpoint-1
+        		if(lastCheckpoint<=0) then
+        			lastCheckpoint = 1
+        		end
+
+        		for key,value in ipairs(checkpoints) do 
+
+        			if(tonumber(GetTagValue(value, "checkpoint"))== lastCheckpoint) then 
+        				local resetTrigger = GetTriggerTransform(value)
+        				resetTrigger.pos = TransformToParentPoint(resetTrigger,Vec(math.random(-7,7),0,math.random(-7,7)))   
+        				SetBodyTransform(GetVehicleBody(vehicle.id),resetTrigger)
+        				resetTimer = RESETMAX
+        			end
+        		end
+
+         	end
+         elseif RACESTARTED and VEHICLE_ACTIVE and   resetTimer<RESETMAX then
+         	resetTimer = RESETMAX
+         elseif(RACESTARTED and VEHICLE_ACTIVE) then
+
+         		local lastCheckpoint = raceCheckpoint-1
+        		if(lastCheckpoint<=0) then
+        			lastCheckpoint = #checkpoints
+        		end
+
+         		for key,value in ipairs(checkpoints) do 
+
+        			DebugWatch("checkpoint",math.abs(lastCheckpoint-key))
+        	 		if(raceCheckpoint ~=1 and IsVehicleInTrigger(value,vehicle.id) and math.abs(lastCheckpoint-tonumber(GetTagValue(value, "checkpoint")))>maxLastCheckpoints) then
+        				for key,value in ipairs(checkpoints) do 
+
+        					if(tonumber(GetTagValue(value, "checkpoint"))== lastCheckpoint) then 
+        						local resetTrigger = GetTriggerTransform(value)
+        						resetTrigger.pos = TransformToParentPoint(resetTrigger,Vec(math.random(-7,7),0,math.random(-7,7)))   
+        						SetBodyTransform(GetVehicleBody(vehicle.id),resetTrigger)
+        						SetBodyVelocity(GetVehicleBody(vehicle.id),Vec(0,0,0))
+        						resetTimer = RESETMAX
+        					end
+        				end
+        			end
+
+        		end
+
+         end
+        -- DebugWatch("Vehicle ",vehicle.id)
+        DebugWatch("velocity:", VecLength(GetBodyVelocity(GetVehicleBody(vehicle.id))))
+    end
+end
+

```

---

# Migration Report: scripts\AVF_AI_V2 - Copy.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\AVF_AI_V2 - Copy.lua
+++ patched/scripts\AVF_AI_V2 - Copy.lua
@@ -1,219 +1,4 @@
-#include "node.lua"
-
-
-RACESTARTED  = false
-
-aiVehicles = {
-
-
-
-	}
-
-ai = {
-	active = true,
-	goalPos= Vec(0,0,0),
-	detectRange = 3,
-	commands = {
-	[1] = Vec(0,0,-1),
-	[2] = Vec(1*0.8,0,-1*1.5),
-	[3] = Vec(-1*0.8,0,-1*1.5),
-	[4] = Vec(-1,0,0),
-	[5] = Vec(1,0,0),
-	[6] = Vec(0,0,1),
-
-	},
-
-	weights = {
-
-	[1] = 0.870,
-	[2] = 0.86,
-	[3] = 0.86,
-	[4] = 0.84,
-	[5] = 0.84,
-	[6] = 0.80,
-
-			} ,
-
-	targetMoves = {
-		list        = {},
-		target      = Vec(0,0,0),
-		targetIndex = 1
-	},
-
-
-	directions = {
-		forward = Vec(0,0,1),
-
-		back = Vec(0,0,-1),
-
-		left = Vec(1,0,0),
-
-		right = Vec(-1,0,0),
-	},
-
-	clustering = {
-		pass = 1,
-		maxPass = 10,
-		centroids = 6,
-		iterations = 5,
-		prior = 1,
-		dataSize = 100,
-		previousOutput = Vec(0,0,0),
-		clusters = {
-			centroids = {
-				pass = 1,
-				index = 1,
-				data = {},
-			},
-			current = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-			prior = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-		},
-
-	},
-
-	scanning = {
-		numScans = 7,
-		scanThreshold = 0.5,
-		maxScanLength = 5,
-		scanLength = 30,
-		scanDepths = 3,
-		vehicleHeight = 2,
-		cones = {
-			left   = {
-				startVec = Vec(1,0,0),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				size = 110,
-				startVec = Vec(-1,0,0),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-	},
-
-
-
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
-
-
-	validSurfaceColours ={ 
-			[1] = {
-				r = 0.20,
-				g = 0.20,
-				b = 0.20,
-				range = 0.02
-			},
-		},
-	hitColour = Vec(1,0,0),
-	detectColour = Vec(1,1,0),
-	clearColour = Vec(0,1,0),
-}
-
-
-
-function init()
-
-
-
-	-- for i = 1,#ai.commands*1 do 
-	-- 	detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
-	-- 	if(i> #ai.commands) then
-	-- 		detectPoints[i] = VecScale(detectPoints[i],0.5)
-	-- 		detectPoints[i][2] = ai.altChecks[2]
-
-
-	-- 	else 
-	-- 		detectPoints[i][2] = ai.altChecks[1]
-	-- 	end
-	-- 	weights[i] = ai.weights[(i%#ai.commands)+1]--*ai.altWeight[math.floor(i/#ai.commands)+1]
-
-	-- end
-
-	checkpoints = FindTriggers("checkpoint",true)
-
-	vehicles = FindVehicles("cfg",true)
-
-	for key,vehicle in pairs(vehicles) do 
-		local value = GetTagValue(vehicle, "cfg")
-		if(value == "ai") then
-			local index = #aiVehicles+1
-			aiVehicles[index] = deepcopy(ai)
-			aiVehicles[index]:initVehicle(vehicle) 
-
-
-		end
-	end
-
-
-
-
-end
-
-function tick(dt)
-
-	hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
-	if hit then
-	--local hitPoint = VecAdd(pos, VecScale(dir, dist))
-		local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
-		DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
-	end
-	for key,vehicle in pairs(aiVehicles) do 
-		vehicle:tick(dt)
-	end	
-
-
-	
-
-end
-
-
+#version 2
 function ai:initVehicle(vehicle) 
 
 	self.id = vehicle
@@ -237,10 +22,7 @@
 
 	self:initClusters()
 
-
-
-end
-
+end
 
 function ai:initClusters()
 	for cluster= 1,self.clustering.centroids do 
@@ -274,7 +56,6 @@
 
 	
 end
-
 
 function ai:markLoc()
 	
@@ -320,9 +101,7 @@
 		SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
 	end
 
-
-end
-
+end
 
 function ai:scanPos()
 
@@ -333,7 +112,6 @@
 	local boundsSize = VecSub(max, min)
 	local center = VecLerp(min, max, 0.5)
 
-
 	DebugWatch("boundsize",boundsSize)
 	DebugWatch("center",center)
 
@@ -343,10 +121,6 @@
 
 		for i=1,ai.scanning.scanDepths do 
 			local scanLength = self.scanning.scanLength * i
-
-
-
-
 
 			local projectionAngle =  (math.sin(math.rad(scan.size)) * ((scanLength)))
 			if(scan.startVec[1]>0) then
@@ -389,17 +163,13 @@
 
 	end
 
-
 	self:clusteringOperations()
-
 
 	self.clustering.clusters.current.pass = (self.clustering.clusters.current.pass%self.clustering.dataSize )+1 
 	self.clustering.clusters.current.index = 1
 
 end
 
-
---init clusters 
 function ai:clusteringCentroids()
 	local valRange = { min = { 100000, 100000, 100000},
 						max = {-100000 , -100000 , -100000 } 
@@ -433,7 +203,6 @@
 	--DebugPrint("min:"..valRange.min[1]..","..valRange.min[2]..","..valRange.min[2].."\nMax: "..valRange.max[1]..","..valRange.max[2]..","..valRange.max[3])
 end
 
---init clusters 
 function ai:clusteringUpdateCentroids()
 	local pos = Vec(0,0,0)
 	local inputData = nil
@@ -443,7 +212,6 @@
 		self.clustering.clusters.centroids.data[inputData:getMinID()]:growCluster(pos)
 	end
 
-
 	self:clusteringCentroids()
 
 	for i = 1,self.clustering.centroids do
@@ -451,12 +219,8 @@
 
 	end
 
-
-end
-
-
-
--- find euclidian distance of data to clusters and update centroid locations
+end
+
 function ai:clusteringCalculateClusters()
 	local pos = Vec(0,0,0)
 	local center = Vec(0,0,0)
@@ -477,11 +241,9 @@
 
 end
 
-
 function ai:clusteringOperations()
 	
 	self:clusteringCalculateClusters()
-
 
 	self:pseudoSNN()
 
@@ -492,14 +254,6 @@
 	end
 
 end
-
-
---- simulate an snn network slightly to get best node
-
--- if(SNNpspprev[j]<SNNpsp[i])
---  {
---      SNNweights[j][i]=tanh(gammaweights*SNNweights[j][i]+learningrateweights*SNNpspprev[j]*SNNpsp[i]);
---  }
 
 function ai:pseudoSNN()
 	local largestpsp = 0
@@ -510,7 +264,6 @@
 		inputData = self.clustering.clusters.current.data[index] 
 		self.clustering.clusters.centroids.data[inputData:getMinID()]:growPulse(inputData.value)
 	end
-
 
 	self:clusteringCentroids()
 
@@ -546,10 +299,8 @@
 	--DebugPrint("values: index: "..index.."\nhitpos:"..VecStr(hitPos).."\nhitval: "..hitValue.."\nClusterPos = "..VecStr(self.clustering.clusters.current.data[index]:getPos()))
 	self.clustering.clusters.current.data[index]:push(hitPos[1],hitPos[2],hitPos[3],hitValue) 
 
-
 	self.clustering.clusters.current.index = (self.clustering.clusters.current.index%self.clustering.dataSize )+1
 end
-
 
 function ai:MAV(targetCost)
 	self.targetMoves.targetIndex = (self.targetMoves.targetIndex%#self.targetMoves.list)+1 
@@ -560,11 +311,7 @@
 
 end
 
-
-
 function ai:costFunc(testPos,hit,dist,shape,key)
-
-
 
 	local cost = 10000 
 	if(not hit) then
@@ -572,8 +319,6 @@
 	end
 	return cost
 end
-
-
 
 function ai:controlVehicle( targetCost)
 	local hBrake = false
@@ -603,7 +348,6 @@
 				targetMove[3] = targetMove[3] *2
 			end
 
-
 			DriveVehicle(self.id, -targetMove[3]*drivePower,-targetMove[1], hBrake)
 			DebugWatch("post updated",VecStr(targetMove))
 			DebugWatch("motion2",VecStr(detectPoints[targetCost.key]))
@@ -613,18 +357,10 @@
 	end
 end
 
-
-
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
-
-
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -641,8 +377,6 @@
     return copy
 end
 
-
-
 function inRange(min,max,value)
 		if(min < value and value<=max) then 
 			return true
@@ -651,4 +385,33 @@
 			return false
 		end
 
-end+end
+
+function server.init()
+    checkpoints = FindTriggers("checkpoint",true)
+    vehicles = FindVehicles("cfg",true)
+    for key,vehicle in pairs(vehicles) do 
+    	local value = GetTagValue(vehicle, "cfg")
+    	if(value == "ai") then
+    		local index = #aiVehicles+1
+    		aiVehicles[index] = deepcopy(ai)
+    		aiVehicles[index]:initVehicle(vehicle) 
+
+    	end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
+        if hit then
+        --local hitPoint = VecAdd(pos, VecScale(dir, dist))
+        	local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
+        	DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
+        end
+        for key,vehicle in pairs(aiVehicles) do 
+        	vehicle:tick(dt)
+        end	
+    end
+end
+

```

---

# Migration Report: scripts\AVF_AI_V2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\AVF_AI_V2.lua
+++ patched/scripts\AVF_AI_V2.lua
@@ -1,279 +1,4 @@
-#include "node.lua"
-
-
-RACESTARTED  = false
-
-aiVehicles = {
-
-
-
-	}
-
-ai = {
-	active = true,
-	goalPos= Vec(0,0,0),
-
-	controller = {
-
-		accelerationValue = 0,
-		steeringValue = 0,
-		handbrake = false,
-	},
-
-
-	detectRange = 3,
-	commands = {
-	[1] = Vec(0,0,-1),
-	[2] = Vec(1*0.8,0,-1*1.5),
-	[3] = Vec(-1*0.8,0,-1*1.5),
-	[4] = Vec(-1,0,0),
-	[5] = Vec(1,0,0),
-	[6] = Vec(0,0,1),
-
-	},
-
-	weights = {
-
-	[1] = 0.870,
-	[2] = 0.86,
-	[3] = 0.86,
-	[4] = 0.84,
-	[5] = 0.84,
-	[6] = 0.80,
-
-			} ,
-
-	targetMoves = {
-		list        = {},
-		target      = Vec(0,0,0),
-		targetIndex = 1
-	},
-
-
-	directions = {
-		forward = Vec(0,0,1),
-
-		back = Vec(0,0,-1),
-
-		left = Vec(1,0,0),
-
-		right = Vec(-1,0,0),
-	},
-
-	maxVelocity = 0,
-
-	cornerCoef = 6,
-
-	accelerationCoef = 5.75,
-	steeringCoef = 1.55,
-
-	pidState = {
-
-			--- pid gain params
-		pGain = 2.165,
-		iGain = 0.3,
-		dGain = -2.3,
-
-		intergralTime = 5,
-
-		integralIndex = 1,
-		integralSum = 0,
-		integralData = {
-
-		},
-		lastCrossTrackError = 0,
-		lastPnt = Vec(0,0,0),
-
-			-- pid output value 
-		controllerValue = 0,
-
-
-			--- pid update and training params
-			training = false,
-		inputrate=0.0665,
-		learningrateweights=0.009,
-		learningrateThres = 0.02,
-	    bestrate=0.05,
-	    secondbestrate=0.01,
-	    gammasyn=0.9,
-	    gammaref=0.7,
-	    gammapsp=0.9,
-	},
-
-	clustering = {
-		pass = 1,
-		maxPass = 10,
-		centroids = 2,
-		iterations = 5,
-		prior = 1,
-		dataSize = 100,
-		mode = -1,
-		previousOutput = -1,
-		output = nil,
-		clusters = {
-			centroids = {
-				pass = 1,
-				index = 1,
-				data = {},
-			},
-			current = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-			prior = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-		},
-
-	},
-
-	scanning = {
-		numScans = 2,
-		scanThreshold = 0.5,
-		maxScanLength = 5,
-		scanLength = 50,
-		scanDepths = 2,
-		vehicleHeight = 2,
-		cones = {
-			left   = {
-				startVec = Vec(1,0,-0.1),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				size = 110,
-				startVec = Vec(-1,0,-0.1),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-	},
-
-
-
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
-
-
-	validSurfaceColours ={ 
-			[1] = {
-				r = 0.20,
-				g = 0.20,
-				b = 0.20,
-				range = 0.02
-			},
-		},
-	hitColour = Vec(1,0,0),
-	detectColour = Vec(1,1,0),
-	clearColour = Vec(0,1,0),
-}
-
-
-
-function init()
-
-
-
-	-- for i = 1,#ai.commands*1 do 
-	-- 	detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
-	-- 	if(i> #ai.commands) then
-	-- 		detectPoints[i] = VecScale(detectPoints[i],0.5)
-	-- 		detectPoints[i][2] = ai.altChecks[2]
-
-
-	-- 	else 
-	-- 		detectPoints[i][2] = ai.altChecks[1]
-	-- 	end
-	-- 	weights[i] = ai.weights[(i%#ai.commands)+1]--*ai.altWeight[math.floor(i/#ai.commands)+1]
-
-	-- end
-
-	checkpoints = FindTriggers("checkpoint",true)
-
-	vehicles = FindVehicles("cfg",true)
-
-	for key,vehicle in pairs(vehicles) do 
-		local value = GetTagValue(vehicle, "cfg")
-		if(value == "ai") then
-			local index = #aiVehicles+1
-			aiVehicles[index] = deepcopy(ai)
-			aiVehicles[index]:initVehicle(vehicle) 
-
-
-		end
-	end
-
-
-
-
-end
-
-function tick(dt)
-
-	hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
-	if hit then
-	--local hitPoint = VecAdd(pos, VecScale(dir, dist))
-		local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
-		-- DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
-	end
-	for key,vehicle in pairs(aiVehicles) do 
-		vehicle:tick(dt)
-	end	
-
-
-	
-
-end
-
-function update(dt )
-	for key,vehicle in pairs(aiVehicles) do 
-		vehicle:update(dt)
-	end	
-
-
-	
-end
-
-
+#version 2
 function ai:initVehicle(vehicle) 
 
 	self.id = vehicle
@@ -302,10 +27,7 @@
 
 	self:initClusters()
 
-
-
-end
-
+end
 
 function ai:initClusters()
 	for cluster= 1,self.clustering.centroids do 
@@ -342,7 +64,6 @@
 	end
 	
 end
-
 
 function ai:markLoc()
 	
@@ -388,9 +109,7 @@
 		SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
 	end
 
-
-end
-
+end
 
 function ai:controlActions()
 	self:scanPos()
@@ -404,7 +123,6 @@
 	self:controllerAugmentation()
 end
 
-
 function ai:controllerAugmentation()
 	local velocity =  VecLength(GetBodyVelocity(GetVehicleBody(self.id)))
 	if(velocity>self.cornerCoef) then
@@ -414,7 +132,6 @@
 	
 end
 
-
 function ai:scanPos()
 
 	self.scanning.scanLength = self.scanning.maxScanLength+(VecLength(GetBodyVelocity(GetVehicleBody(self.id))))
@@ -424,7 +141,6 @@
 	local boundsSize = VecSub(max, min)
 	local center = VecLerp(min, max, 0.5)
 
-
 	-- DebugWatch("boundsize",boundsSize)
 	-- DebugWatch("center",center)
 
@@ -434,8 +150,6 @@
 
 		for i=1,ai.scanning.scanDepths do 
 			local scanLength = self.scanning.scanLength * i
-
-
 
 			local projectionAngle =  (math.sin(math.rad(scan.size)) * ((scanLength)))
 			if(scan.startVec[1]>0) then
@@ -478,17 +192,13 @@
 
 	end
 
-
 	self:clusteringOperations()
-
 
 	self.clustering.clusters.current.pass = (self.clustering.clusters.current.pass%self.clustering.dataSize )+1 
 	self.clustering.clusters.current.index = 1
 
 end
 
-
---init clusters 
 function ai:clusteringCentroids()
 	local valRange = { min = { 100000, 100000, 100000},
 						max = {-100000 , -100000 , -100000 } 
@@ -522,7 +232,6 @@
 	--DebugPrint("min:"..valRange.min[1]..","..valRange.min[2]..","..valRange.min[2].."\nMax: "..valRange.max[1]..","..valRange.max[2]..","..valRange.max[3])
 end
 
---init clusters 
 function ai:clusteringUpdateCentroids()
 	local pos = Vec(0,0,0)
 	local inputData = nil
@@ -540,8 +249,6 @@
 	end
 end
 
-
--- find euclidian distance of data to clusters and update centroid locations
 function ai:clusteringCalculateClusters()
 	local pos = Vec(0,0,0)
 	local center = Vec(0,0,0)
@@ -562,11 +269,9 @@
 
 end
 
---- perform operations on clusters to extract target
 function ai:clusteringOperations()
 	
 	self:clusteringCalculateClusters()
-
 
 	self:pseudoSNN()
 
@@ -579,14 +284,6 @@
 	end
 
 end
-
-
---- simulate an snn network slightly to get best node
-
--- if(SNNpspprev[j]<SNNpsp[i])
---  {
---      SNNweights[j][i]=tanh(gammaweights*SNNweights[j][i]+learningrateweights*SNNpspprev[j]*SNNpsp[i]);
---  }
 
 function ai:pseudoSNN()
 	local bestpsp = 100000000
@@ -652,7 +349,6 @@
 	
 	--DebugPrint("values: index: "..index.."\nhitpos:"..VecStr(hitPos).."\nhitval: "..hitValue.."\nClusterPos = "..VecStr(self.clustering.clusters.current.data[index]:getPos()))
 	self.clustering.clusters.current.data[index]:push(hitPos[1],hitPos[2],hitPos[3],hitValue) 
-
 
 	self.clustering.clusters.current.index = (self.clustering.clusters.current.index%self.clustering.dataSize )+1
 end
@@ -676,7 +372,6 @@
 	self.pidState.controllerValue = output
 	DebugWatch("pid output: ",output)
 
-
 	if(RACESTARTED and  self.pidState.training) then
 		if math.abs(crossTrackErrorRate) > self.pidState.learningrateThres then 
 			if(crossTrackErrorRate>0) then 
@@ -695,7 +390,6 @@
 
 	return output
 end
-
 
 function ai:currentCrossTrackError()
 	local crossTrackErrorValue = 0
@@ -708,10 +402,7 @@
 	return targetNode, crossTrackErrorValue,sign
 end
 
---- calculate distance to target direction and apply steering by force
---- fill in the gap here related to the distance ebtween the aprrelel lines of target nod3e to vehicle pos to solve it all
 function ai:crossTrackError(pnt,vehicleTransform)
-
 
 		
 		vehicleTransform.pos[2] = pnt[2]
@@ -733,7 +424,6 @@
 			sign = 0
 		end
 
-
 		return d*sign,sign
 
 		-- Use the sign of the determinant of vectors (AB,AM), where M(X,Y) is the query point:	
@@ -752,12 +442,6 @@
 		-- DebugWatch("output pos : ",out)
 
 		-- DebugWatch("output value: ",VecSub(out,pnt))
-
-
-
-
-
-
 
 		-- local vehicleTransform = GetVehicleTransform(self.id)
 		-- vehicleTransform.pos[2] = targetNode:getPos()[2]
@@ -792,7 +476,6 @@
 	return verifyCrossCheckErrorVal
 end
 
-
 function ai:calculateSteadyStateError(crossTrackErrorValue)
 	local index = self.pidState.integralIndex
 
@@ -838,7 +521,6 @@
 		-- DebugWatch("point pos : ",pnt)
 		-- DebugWatch("output pos : ",out)
 
-
 	-- //linePnt - point the line passes through
 	-- //lineDir - unit vector in direction of line, either direction works
 	-- //pnt - the point to find nearest on line for
@@ -850,7 +532,6 @@
 	--     return linePnt + lineDir * d;
 	-- }
 end
- 
 
 function ai:vehicleController()
 	DriveVehicle(self.id, 0.05+self.controller.accelerationValue,
@@ -867,11 +548,7 @@
 
 end
 
-
-
 function ai:costFunc(testPos,hit,dist,shape,key)
-
-
 
 	local cost = 10000 
 	if(not hit) then
@@ -879,8 +556,6 @@
 	end
 	return cost
 end
-
-
 
 function ai:controlVehicle( targetCost)
 	local hBrake = false
@@ -910,7 +585,6 @@
 				targetMove[3] = targetMove[3] *2
 			end
 
-
 			DriveVehicle(self.id, -targetMove[3]*drivePower,-targetMove[1], hBrake)
 			DebugWatch("post updated",VecStr(targetMove))
 			DebugWatch("motion2",VecStr(detectPoints[targetCost.key]))
@@ -920,18 +594,10 @@
 	end
 end
 
-
-
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
-
-
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -948,8 +614,6 @@
     return copy
 end
 
-
-
 function inRange(min,max,value)
 		if(min < value and value<=max) then 
 			return true
@@ -958,4 +622,41 @@
 			return false
 		end
 
-end+end
+
+function server.init()
+    checkpoints = FindTriggers("checkpoint",true)
+    vehicles = FindVehicles("cfg",true)
+    for key,vehicle in pairs(vehicles) do 
+    	local value = GetTagValue(vehicle, "cfg")
+    	if(value == "ai") then
+    		local index = #aiVehicles+1
+    		aiVehicles[index] = deepcopy(ai)
+    		aiVehicles[index]:initVehicle(vehicle) 
+
+    	end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        hit, point, normal, shape = QueryClosestPoint(GetCameraTransform().pos, 10)
+        if hit then
+        --local hitPoint = VecAdd(pos, VecScale(dir, dist))
+        	local mat,r,g,b = GetShapeMaterialAtPosition(shape, point)
+        	-- DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
+        end
+        for key,vehicle in pairs(aiVehicles) do 
+        	vehicle:tick(dt)
+        end	
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key,vehicle in pairs(aiVehicles) do 
+        	vehicle:update(dt)
+        end	
+    end
+end
+

```

---

# Migration Report: scripts\AVF_AI_V3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\AVF_AI_V3.lua
+++ patched/scripts\AVF_AI_V3.lua
@@ -1,1906 +1,9 @@
-
-
-#include "node.lua"
-#include "race_Manager.lua"
-#include "names.lua"
-
----- RACE information / terrain control
-
-#include "trackDescriptions.lua"
-
----PATHFINDING LINKED
-
-#include "mapNode.lua"
-#include "AStarSearch.lua"
-
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        AVF_AI_3.lua             
-*
-* DESCRIPTION :
-*       File that implements racing AI inside teardown 2020, with PID controllers
-* 		to ensure cars respond to coordinates in a good fashion and can handle high speed
-*		Also includes simple goal achievement and collision avoidance 
-*		Including "driver ai" to make them more / less aggressive with speed, cornering
-*		overtaking, and driving. 
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-raceMap = GetStringParam("map", "teardownRacing")
-
-
-
-RACESTARTED = false
-
-RACECOUNTDOWN = false
-
-RACEENDED = false
-
-
-PLAYER_TOTALED = false
-
-PATHSET = false
-
-mapInitialized = false
-
-PLAYERRACING = true
-	
-DEBUG = false
-DEBUGCARS = false
-
-DEBUG_SAE = false
-
-
-STOPTHEMUSIC = true
-
-
-DEBUGCONTROLLERS = false
-
-DEFAULTRACETIME = 1000000
-
-map = {
-
-  xIndex = 0,
-  data = {
-
-  },
-  smoothingFactor = 3,
-  validMaterials = {
-  	[1] = {	
-  		material = "masonry",
-
-
-	  validSurfaceColours ={ 
-				[1] = {
-					r = 0.20,
-					g = 0.20,
-					b = 0.20,
-					range = 0.02
-				},
-				[2] = {
-					r = 0.80,
-					g = 0.60,
-					b = 0.60,
-					range = 0.02
-				},
-				[3] = {
-					r = 0.34,
-					g = 0.34,
-					b = 0.34,
-					range = 0.02
-				},
-			},
-		},
-	},
-}
-
--- negative grid pos is solved by simply showing 
-mapSize = {
-			x=400,
-			y=400,
-			grid = 6,
-      gridHeight = 3,
-      gridResolution = 1,
-      gridThres      = 0.6,
-
-      scanHeight = 100,
-
-      scanLength = 200,
-
-      weights = {
-          goodTerrain = 0.1,
-          badTerrain   = 10,
-          avoidTerrain = 25,
-          impassableTerrain = 50,
-      }
-		}
-    path = nil
-
-
---- AI LINKED
-
-
-
-RACESTARTED  = false
-
-aiVehicles = {
-
-
-
-	}
-
-playerConfig = {
-	name = "PLAYER ",
-	finished = false,
-	car = 0,
-	bestLap = 0,
-	playerLaps = 0,
-
-	hudInfo = {
-		lapInfo = {
-			[1] = {
-				name = "Race",
-				time = 0,
-			},
-
-			[2] = {
-				name = "Lap",
-				time = 0,
-			},
-
-			[3] = {
-				name = "Best",
-				time = 0,
-			},
-		},
-	},
-}
-
-
-aiPresets = {
-	
-	EASY = 1,
-	MEDIUM = 2,
-	HARD = 3,
-	INSANE = 4,	
-	DGAF = 5,
-	ROADRAGE = 6,
-
-	difficulties = {
-		[1] = {
-			name =  "easy", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.1, 
-			tenacity = 0.7,
-			errorCoef = 0.4,
-
-		}, 
-		[2] = {
-			name =  "medium", 
-			steeringThres = 0.2,
-			speedSteeringThres = 0.2, 
-			tenacity = 0.8,
-			errorCoef = 0.2,
-
-		}, 
-		[3] = {
-			name =  "hard", 
-			steeringThres = 0.4,
-			speedSteeringThres = 0.4, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-		[4] = {
-			name =  "insane", 
-			steeringThres = 0.6,
-			speedSteeringThres = 0.6, 
-			tenacity = 0.94,
-			errorCoef = 0.05,
-
-		}, 
-		[5] = {
-			name =  "DGAF", 
-			steeringThres = 0.9,
-			speedSteeringThres = 0.9, 
-			tenacity = 0.99,
-			errorCoef = 0.1,
-
-		}, 
-		[6] = {
-			name =  "road rage", 
-			steeringThres = 1,
-			speedSteeringThres = 0.2, 
-			tenacity = 1.1,
-			errorCoef = 0.1,
-
-		}, 
-		[7] = {
-			name =  "Never Overtakes - gentle", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.25, 
-			tenacity = 0.85,
-			errorCoef = 0.1,
-
-		}, 
-		[8] = {
-			name =  "Never Overtakes - speedDemon", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.9, 
-			tenacity = 0.85,
-			errorCoef = 0.1,
-
-		}, 
-		[9] = {
-			name =  "Medium corners, overtakes", 
-			steeringThres = 0.95,
-			speedSteeringThres = 0.5, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-
-		[10] = {
-			name =  "slower corners, overtakes", 
-			steeringThres = 0.7,
-			speedSteeringThres = 0.35, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-
-	},
-
-	difficulty_ranged = {
-		[1] = {
-			name =  "easy", 
-			steeringThres = {10,100},
-			speedSteeringThres = {10,90}, 
-			tenacity = {70,100},
-			errorCoef = {1,40},
-
-		}, 
-		[2] = {
-			name =  "medium", 
-			steeringThres = {20,100},
-			speedSteeringThres = {20,99}, 
-			tenacity = {80,100},
-			errorCoef = {1,20},
-
-		}, 
-		[3] = {
-			name =  "competative_medium", 
-			steeringThres = {60,100},
-			speedSteeringThres = {20,99}, 
-			tenacity = {80,100},
-			errorCoef = {1,10},
-
-		}, 
-		[4] = {
-			name =  "hard", 
-			steeringThres = {40,100},
-			speedSteeringThres = {40,100}, 
-			tenacity = {90,100},
-			errorCoef = {1,10},
-
-		}, 
-		[5] = {
-			name =  "insane", 
-			steeringThres = {60,110},
-			speedSteeringThres = {60,110}, 
-			tenacity = {90,110},
-			errorCoef = {1,5},
-
-		}, 
-		[6] = {
-			name =  "psycobilly_freakout", 
-			steeringThres = {80,130},
-			speedSteeringThres = {80,130}, 
-			tenacity = {95,130},
-			errorCoef = {0.5,2.5},
-
-		}, 
-
-		-- [7] = {
-		-- 	name =  "texas_psycobilly_freakout", 
-		-- 	steeringThres = {80,160},
-		-- 	speedSteeringThres = {80,160}, 
-		-- 	tenacity = {100,160},
-		-- 	errorCoef = {0.25,2},
-
-		-- }, 
-
-	}
-
-}
-
-
-ai = {
-	active = true,
-	goalPos= Vec(0,0,0),
-
-
-
-	raceValues = {
-		completedGoals  = 0,
-		targetNode 		= 1,
-		NextNode 		= 2,
-		passedCheckPoints = 0,
-		nextCheckpoint = 1,
-		completionRange = 4.5,--4.5,
-		lookAhead = 2,
-		laps = 0 	,
-		lastLap = 0,
-		splits = {},
-
-		bestLap = nil,
-
-	},
-
-	targetNode = nil,
-	NextNode =nil,
-
-	controller = {
-		aiType = "default",
-
-		accelerationValue = 0,
-		steeringValue = 0,
-		handbrake = false,
-
-		steeringThres  = aiPresets.HARD, --0.4
-		steeringForce  = 0.5,
-		speedSteeringThres = aiPresets.HARD,
-		tenacity 			= 0.9,
-		relativeThreshold = 0.8,
-		minDist = 2--.5,--5,
-	},
-
-	reversingController = {
-		reversing = false,
-		minVelocity = 1,
-		waitTime = 2.5,
-		currentWait = 3,
-		reverseTime = 2.5,
-		currentReverseTime = 2.5,
-	},
-
-
-	detectRange = 3,
-	commands = {
-	[1] = Vec(0,0,-1),
-	[2] = Vec(1*0.8,0,-1*1.5),
-	[3] = Vec(-1*0.8,0,-1*1.5),
-	[4] = Vec(-1,0,0),
-	[5] = Vec(1,0,0),
-	[6] = Vec(0,0,1),
-
-	},
-
-	weights = {
-
-	[1] = 0.870,
-	[2] = 0.86,
-	[3] = 0.86,
-	[4] = 0.84,
-	[5] = 0.84,
-	[6] = 0.80,
-
-			} ,
-
-	targetMoves = {
-		list        = {},
-		target      = Vec(0,0,0),
-		targetIndex = 1
-	},
-
-
-	directions = {
-		forward = Vec(0,0,1),
-
-		back = Vec(0,0,-1),
-
-		left = Vec(1,0,0),
-
-		right = Vec(-1,0,0),
-	},
-
-	maxVelocity = 0,
-
-	cornerCoef = 16,
-
-	accelerationCoef = 0.75,
-	steeringCoef = 2.55,
-
-	pidState = {
-
-			--- pid gain params
-		pGain = 0.765,
-		iGain = -0.08,
-		dGain = -1.3,
-
-		intergralTime = 5,
-
-		integralIndex = 1,
-		integralSum = 0,
-		integralData = {
-
-		},
-		lastCrossTrackError = 0,
-		lastPnt = Vec(0,0,0),
-
-			-- pid output value 
-		controllerValue = 0,
-
-
-			--- pid update and training params
-			training = false,
-		inputrate=0.0665,
-		learningrateweights=0.009,
-		learningrateThres = 0.02,
-	    bestrate=0.05,
-	    secondbestrate=0.01,
-	    gammasyn=0.9,
-	    gammaref=0.7,
-	    gammapsp=0.9,
-	},
-	usingClustering = false,
-
-	clustering = {
-		pass = 1,
-		maxPass = 10,
-		centroids = 2,
-		iterations = 5,
-		prior = 1,
-		dataSize = 100,
-		mode = -1,
-		previousOutput = -1,
-		output = nil,
-		clusters = {
-			centroids = {
-				pass = 1,
-				index = 1,
-				data = {},
-			},
-			current = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-			prior = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-		},
-
-	},
-
-	scanning = {
-		numScans = 2,
-		scanThreshold = 0.5,
-		maxScanLength = 10,
-		scanLength = 50,
-		scanDepths = 2,
-		vehicleHeight = 2,
-		cones = {
-			left   = {
-				direction = "left",
-				startVec = Vec(0.25,0,-1.5),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				direction = "centre",
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				direction = "right",
-				size = 110,
-				startVec = Vec(-0.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-		positions = {
-			left   = {
-				direction = "left",
-				startVec = Vec(0.25,0,-1.5),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			sideL  = {
-				direction = "sideL",
-				size = 110,
-				startVec = Vec(1.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				direction = "centre",
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				direction = "right",
-				size = 110,
-				startVec = Vec(-0.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			sideR  = {
-				direction = "sideR",
-				size = 110,
-				startVec = Vec(-1.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-
-	},
-
-
-
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
-
-
-	validSurfaceColours ={ 
-			[1] = {
-				r = 0.20,
-				g = 0.20,
-				b = 0.20,
-				range = 0.02
-			},
-			[2] = {
-				r = 0.60,
-				g = 0.60,
-				b = 0.60,
-				range = 0.02
-			},
-			[3] = {
-				r = 0.34,
-				g = 0.34,
-				b = 0.34,
-				range = 0.02
-			},
-		},
-	hitColour = Vec(1,0,0),
-	detectColour = Vec(1,1,0),
-	clearColour = Vec(0,1,0),
-}
-
-
-
-function init()
-
-
-	----------- stuff from drive 2 drive_to_survive
-	sndConfirm = LoadSound("MOD/sounds/confirm.ogg")
-	sndReject = LoadSound("MOD/sounds/reject.ogg")
-	sndWarning = LoadSound("MOD/sounds/warning-beep.ogg")
-	sndPickup = LoadSound("MOD/sounds/pickup.ogg")
-	sndRocket = LoadLoop("MOD/sounds/rocket.ogg")
-	sndFail = LoadSound("MOD/sounds/fail.ogg")
-	sndWin = LoadSound("MOD/sounds/win.ogg")
-	sndReady = LoadSound("MOD/sounds/ready.ogg")
-	sndStart = LoadSound("MOD/sounds/start.ogg")
-
-	--------------
-
-	STOPTHEMUSIC = GetBool("savegame.mod.play_race_music")
-
-
-	--initMap()
-
-  	-- local smoothingSum = {0,0}
-  	-- for i = 1,#path do
-  	-- 	smoothingSum = {0,0}
-  	-- 	for j = -1,1,1 do 
-  	-- 		if(i+j <=0) then
-  	-- 			smoothingSum[1] = smoothingSum[1]+path[#path+j][1] 
-  	-- 			smoothingSum[2] = smoothingSum[2]+path[#path+j][2]
-  	-- 		elseif(i+j >#path) then
-  	-- 			smoothingSum[1] = smoothingSum[1]+path[(i+j)-#path][1] 
-  	-- 			smoothingSum[2] = smoothingSum[2]+path[(i+j)-#path][2]
-  	-- 		else
-  	-- 			smoothingSum[1] = smoothingSum[1]+path[i+j][1] 
-  	-- 			smoothingSum[2] = smoothingSum[2]+path[i+j][2]
-  	-- 		end
-	  -- 	end
-	  -- 	path[i][1] = math.floor(smoothingSum[1]/map.smoothingFactor)
-	  -- 	path[i][2] = math.floor(smoothingSum[2]/map.smoothingFactor)
-  	-- end
-  	
-	-- for i = 1,#ai.commands*1 do 
-	-- 	detectPoints[i] = deepcopy(ai.commands[(i%#ai.commands)+1])
-	-- 	if(i> #ai.commands) then
-	-- 		detectPoints[i] = VecScale(detectPoints[i],0.5)
-	-- 		detectPoints[i][2] = ai.altChecks[2]
-
-
-	-- 	else 
-	-- 		detectPoints[i][2] = ai.altChecks[1]
-	-- 	end
-	-- 	weights[i] = ai.weights[(i%#ai.commands)+1]--*ai.altWeight[math.floor(i/#ai.commands)+1]
-
-	-- end
-
-	checkpoints = FindTriggers("checkpoint",true)
-
-	for i = 1,#checkpoints do 
-		if(GetTagValue(value, "checkpoint")=="") then 
-			SetTag(checkpoints[i],"checkpoint",i)
-		end
-
-	end
-
-	vehicles = FindVehicles("cfg",true)
-
-
-	--[[
-
-	set custom name info for trackDescriptions 
-
-	also grab fastest time for that track 
-
-	]]
-
-
-	playerState = FindLocation("player",true) 
-
-	if(IsHandleValid(playerState)and GetTagValue(playerState,"player")=="true") then
-		if(DEBUG) then 
-			DebugPrint("player in race")
-		end
-		PLAYERRACING = true
-	else
-		if(DEBUG) then
-			DebugPrint("player not in race")
-		end
-		PLAYERRACING = false
-	end
-
-	--- set custom track values
-	if(trackDescriptions[raceMap]) then
-		map.validMaterials = deepcopy(trackDescriptions[raceMap].validMaterials)
-		map.name = trackDescriptions[raceMap].name
-		map.lines = deepcopy(trackDescriptions[raceMap].lines)
-		raceManager.laps = trackDescriptions[raceMap].trackLaps
-		if(trackDescriptions[raceMap].grid ) then
-			mapSize.grid =  trackDescriptions[raceMap].grid
-		end
-		if(trackDescriptions[raceMap].grid ) then
-			ai.raceValues.completionRange =  trackDescriptions[raceMap].grid
-		end
-		if(trackDescriptions[raceMap].completionRange ) then
-			ai.raceValues.completionRange =  trackDescriptions[raceMap].completionRange 
-		end
-	else
-		raceMap = "teardownRacing"
-
-		map.validMaterials = deepcopy(trackDescriptions[raceMap].validMaterials)
-		map.name = trackDescriptions[raceMap].name
-		map.lines = deepcopy(trackDescriptions[raceMap].lines)
-		raceManager.laps = trackDescriptions[raceMap].trackLaps
-	end
-
-
-	 initMapArr()
-
-	roundCar = FindLocation("trackinfo",true)
-
-	if(PLAYERRACING and roundCar) then
-
-		if roundCar and HasKey("savegame.mod.besttime."..raceMap.."." .. GetTagValue(roundCar,"trackinfo")) then
-			firstRoundWithCar = false
-			savedBest = GetFloat("savegame.mod.besttime."..raceMap.."." .. GetTagValue(roundCar,"trackinfo"))
-		else
-			firstRoundWithCar = true
-			savedBest = DEFAULTRACETIME
-		end
-
-
-	end
-
-	--DebugPrint("saved best: "..savedBest.." roundcar: "..roundCar)
-	-- savedBest = DEFAULTRACETIME
-	--DebugPrint("saved best: "..savedBest.." roundcar: "..roundCar)
-
-	--[[
-	
-	prepare ai vehicles
-
-	]]
-
-	for key,vehicle in pairs(vehicles) do 
-		local value = GetTagValue(vehicle, "cfg")
-		if(value == "ai") then
-			local index = #aiVehicles+1
-			aiVehicles[index] = deepcopy(ai)
-			aiVehicles[index]:initVehicle(vehicle) 
-
-
-		end
-	end
-
-
-	if(PLAYERRACING) then
-
-		local playerCarPos = 1
-		if(#aiVehicles>1) then
-			playerCarPos = math.random(math.max(#aiVehicles/5,1),#aiVehicles)
-		end
-		playerConfig.car = playerCarPos
-		aiVehicles[playerConfig.car].playerName = playerConfig.name
-		SetPlayerVehicle(aiVehicles[playerConfig.car].id)
-	end
-
-
-
-	-- DebugPrint("started")
-
-end
-
-
-
-function initPlayer()
-	if roundCar and HasKey("savegame.mod.besttime.car" .. roundCar) then
-		firstRoundWithCar = false
-		savedBest = GetFloat("savegame.mod.besttime.car" .. roundCar)
-	else
-		firstRoundWithCar = true
-		savedBest = 0
-	end
-
-end
-
-
-function initMapArr()
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-	    pos = posToInt(Vec(0,0,y))
-	    map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        map.data[pos[3]][pos[1]] = nil 
-	    end
-	end
-end
-
-function initMap( )
-local pos = Vec(0,0,0)
-  local gridCost = 0
-  local maxVal  = {math.modf((mapSize.x)/mapSize.grid),math.modf((mapSize.y)/mapSize.grid)}
-
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-    pos = posToInt(Vec(0,0,y))
-    -- map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        gridCost,validTerrain,avgHeight =  scanGrid(x,y) 
-	        -- if(pos[3] ~= nil and pos[1]~= nil) then
-	          
-	          map.data[pos[3]][pos[1]] = deepcopy(mapNode) 
-	          map.data[pos[3]][pos[1]]:push(x,avgHeight,y,gridCost,pos[3],pos[1],validTerrain,maxVal )
-
-	        -- end
-	  		  -- DebugPrint(x.." | "..y)
-	    end
-	end
-
-
-	mapInitialized = true
-	
-
-end
-
-
-function initPaths()
-
-  pos = posToInt(GetPlayerPos())
-   goalPos = map.data[60][30]
-   startPos = map.data[55][72]
-  startPos = map.data[pos[3]][pos[1]]
-
-
-
-  paths = {}
-  gateState = {}
-  gates = {}
-  triggers = FindTriggers("gate",true)
-  for i=1,#triggers do
-    gateState[tonumber(GetTagValue(triggers[i], "gate"))] = 0
-    gates[tonumber(GetTagValue(triggers[i], "gate"))] = triggers[i]
-  end
-
-  for i =1,#triggers do 
-    startPos = posToInt(GetTriggerTransform(gates[i]).pos)
-    startPos = map.data[startPos[3]][startPos[1]]
-    if(i==#triggers) then 
-      goalPos = posToInt(GetTriggerTransform(gates[1]).pos )
-    else
-      goalPos = posToInt(GetTriggerTransform(gates[i+1]).pos )
-    end
-    goalPos = map.data[goalPos[3]][goalPos[1]]
-    paths[#paths+1] =  AStar:AStarSearch(map.data, startPos, goalPos)
-  end
-  	path = paths[#paths]
-  	for i = 1,#paths-1 do
-  		for j = 1,#paths[i] do 
-	  		path[#path+1] = paths[i][j]
-	  	end
-  	end
-end
-
-
-function tick(dt)
-
-	if(DEBUG) then 
-	  local playerTrans = GetPlayerTransform()
-	  playerTrans.pos,pos2 = posToInt(playerTrans.pos)
-	  DebugWatch("Player Pos: ",playerTrans.pos)
-
-	end
-
-
-	if(PATHSET) then 
-
-	  	if(DEBUG)then 
-
-		    AStar:drawPath(map.data,path)
-
-			local t = GetCameraTransform()
-			local dir = TransformToParentVec(t, {0, 0, -1})
-
-			local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 10)
-			DebugWatch("Hit", hit)
-			if hit then
-				--Visualize raycast hit and normal
-				local hitPoint = VecAdd(t.pos, VecScale(dir, dist))
-				local mat,r,g,b = GetShapeMaterialAtPosition(shape, hitPoint)
-				DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
-				DebugWatch("Terrain cost",checkIfTerrainValid(mat,r,g,b))
-				DebugWatch("body mass",GetBodyMass(GetShapeBody(shape)))
-			end
-
-		end
-
-
-
-		for key,vehicle in pairs(aiVehicles) do 
-			vehicle:tick(dt)
-		end	
-
-		raceManager:raceTick()
-		-- DebugWatch("time",math.floor(GetTime()/5))
-		-- DebugWatch("time",GetTime()%5)
-
-
-		if(raceManager.countdown>0 and   RACECOUNTDOWN) then
-			raceManager:raceCountdown()
-		elseif(raceManager.countdown<0)then
-
-			RACECOUNTDOWN = false
-		end
-
-
-
-	  if DEBUG and  InputPressed("r") and not RACESTARTED  then
-	    RACESTARTED = true
-	    -- DebugPrint("race started!")
-	    raceManager:startRace()
-	    PlaySound(sndStart)
-	    -- PlayMusic("MOD/sounds/drive_to_survive.ogg")
-	     -- path =  AStar:AStarSearch(map.data, startPos, goalPos)
-	  elseif(RACESTARTED and path)then 
-
-
-
-
-
-	    -- DebugWatch("running",#paths)
-	    -- for key,val in ipairs(paths) do  
-	    --    AStar:drawPath2(map.data,val)
-	    -- end
-	  end
-	  -- local playerTrans = GetPlayerTransform()
-	  -- playerTrans.pos,pos2 = posToInt(playerTrans.pos)
-	  -- DebugWatch("Player Pos: ",playerTrans.pos)
-	  -- -- --  DebugWatch("original Player Pos: ", GetPlayerTransform().pos)
-	  -- --  -- DebugWatch("Pos 2: ",pos2) 
-	  --  local pos = VecCopy(playerTrans.pos)
-	  --  if(pos[3] ~= nil and pos[1]~= nil) then
-	  --   	-- DebugPrint(pos[3].." | "..pos[1])
-	  --   	 DebugWatch("player Grid Cost: ",map.data[pos[3]][pos[1]]:getCost())
-
-	  --    DebugWatch("player Grid neighbors: ",#map.data[pos[3]][pos[1]].neighbors)
-
-	  --    local totalCost = 0
-	  --    for key, val in ipairs(map.data[pos[3]][pos[1]]:getNeighbors()) do
-	  --         totalCost = totalCost + map.data[val.y][val.x]:getCost()
-	  --    end
-
-	  --    DebugWatch("player Grid neighbor: ",totalCost)
-
-	  --    DebugWatch("player Grid VALID: ",map.data[pos[3]][pos[1]].validTerrain)
-	  -- -- else
-
-	  -- end
-
-	elseif not PATHSET and GetTime() >0.1 then 
-		if(not mapInitialized) then 
-			initMap()
-		end
-		-- DebugPrint("prepping paths")
-
-		
-			initPaths()
-
-
-			for key,vehicle in pairs(aiVehicles) do 
-				vehicle:initGoalPos()
-			end	
-			PATHSET = true
-		-- DebugPrint("Paths set")
-
-		-------
-
-		 --- init racing values
-
-		 -----
-
-
-			raceManager:init(aiVehicles,path)
-		
-	end
-
-
-
-	---- ----------------
-
-
-	------- handle player tick stuff
-
-
-	---------------
-
-	if(PLAYERRACING) then 
-		raceManager:playerHandler()
-		if((raceManager.countdown > 0 and  raceManager.preCountdown <=0) or playerConfig.finished  ) then
-	-- 		raceManager:StartCamPos()
-
-			 raceManager:cameraOperator(playerConfig.car)
-			-- CAMMODE = false
-		elseif(CAMMODE and raceManager.countdown<=0) then
-			-- CAMMODE = false
-		end
-
-	end
-
-
-	---------------------
-			---------- keypress stuff
-	---------------
-
-	if InputPressed("c") then 
-		CAMMODE = not CAMMODE
-
-	end
-
-	if(InputPressed("p")) then
-
-		raceManager:setDisplayRange()
-	end
-
-
-end
-
-function update(dt )
-	for key,vehicle in pairs(aiVehicles) do 
-		if(key ~= playerConfig.car) then 
-			vehicle:update(dt)
-		end
-	end	
-
-
-
-	if(RACESTARTED and CAMMODE) then 
-		raceManager:cameraManager()
-
-	end
-	raceManager:cameraControl()
-	
-end
-
-
-
-
-function ai:initVehicle(vehicle) 
-
-	self.id = vehicle
-	self.body = GetVehicleBody(self.id)
-	self.transform =  GetBodyTransform(self.body)
-	self.shapes = GetBodyShapes(self.body)
-
-
-
-	--- declare driver name 
-
-	if(math.random(0,200)<=1) then
-		self.driverName = uniqueNames[math.random(1,#uniqueNames)]
-	else
-		self.driverFName = fNames[math.random(1,#fNames)] 
-		self.driverSName = sNames[math.random(1,#sNames)]
-		self.driverName = self.driverFName.." "..self.driverSName
-	end
-		--- find largest shape and dclare that the main vehicle SpawnParticle
-
-	local largestKey = 0
-	local shapeVoxels = 0
-	local largestShapeVoxels = 0
-	for key,shape in ipairs(self.shapes) do
-		shapeVoxels = GetShapeVoxelCount(shape)
-		if(shapeVoxels> largestShapeVoxels) then
-			largestShapeVoxels = shapeVoxels
-			largestKey = key
-		end
-	end
-	self.mainBody = self.shapes[largestKey]
-	self.bodyXSize,self.bodyYSize ,self.bodyZSize  = GetShapeSize(self.mainBody)
-	-- DebugPrint("body Size: "..self.bodyXSize.." | "..self.bodyYSize.." | "..self.bodyZSize)
-
-
-	for i=1,3 do 
-		self.targetMoves.list[i] = Vec(0,0,0)
-	end
-
-	self.raceCheckpoint = 1
-	self.currentCheckpoint = nil
-
-	for key,value in ipairs(checkpoints) do
-		if(tonumber(GetTagValue(value, "checkpoint"))==self.raceCheckpoint) then 
-			self.currentCheckpoint = value
-		end
-	end	
-
-	for i = 1, self.pidState.intergralTime do
-		self.pidState.integralData[i] = 0
-
-	end
-
-
-	self.hudColour = {math.random(0,100)/100,math.random(0,100)/100,math.random(0,100)/100}
-
---	local aiLevel = aiPresets.difficulties[math.random(1,#aiPresets.difficulties)]
-	-- local aiLevel = aiPresets.difficulties[5]--math.random(3,5)]
-	
-	local aiLevel = deepcopy(aiPresets.difficulty_ranged[math.random(1,#aiPresets.difficulty_ranged)])--aiPresets.difficulty_ranged[4])
-	for key,val in pairs(aiLevel) do 
-		if(type(val)=="table") then
-			aiLevel[key] = math.random(val[1],val[2])/100 
-		end
-	end
-	-- for key,val in pairs(aiLevel) do 
-	-- 	if(type(val)=="table") then 
-	-- 		DebugPrint(key..": "..val[1].."-"..val[2]) 
-	-- 	else
-	-- 		DebugPrint(key..": "..val)
-	-- 	end
-
-
-	-- end
-	
-
-	self.controller.aiLevel = aiLevel.name
-
-	self.controller.steeringThres  = aiLevel.steeringThres --0.4
-
-	self.controller.speedSteeringThres = aiLevel.speedSteeringThres
-	self.controller.tenacity = aiLevel.tenacity
-
-	self.controller.errorCoef = aiLevel.errorCoef
-
-
-	self.scanning.maxScanLength = self.scanning.maxScanLength * (math.random(90,350)/100) 
-
-
-
-end
-
-function ai:initGoalPos()
-	self.goalPos = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]:getPos()
-	self.targetNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-
-
-
-	self.NextNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-	-- self:initClusters()
-
-
-end
-
-
-function ai:initClusters()
-	for cluster= 1,self.clustering.centroids do 
-		self.clustering.clusters.centroids.data[cluster] = deepcopy(node)
-
-		 self.clustering.clusters.centroids.data[cluster]:loadSprite()
-	end
-	for i = 1,self.clustering.dataSize do 
-		--clustering.clusters.current.data
-		self.clustering.clusters.current.data[i] = deepcopy(node)
-		self.clustering.clusters.prior.data[i] = deepcopy(node)
-		self.clustering.clusters.current.data[i]:loadSprite()
-	end
-
-	self:scanPos()
-	self:clusteringCentroids()
-
-end
-
-function ai:tick(dt)
-		-- DebugWatch("datasize = ",#self.clustering.clusters.centroids.data)
-
-		self:raceController()
-		-- self:controlActions()
-	if(RACESTARTED and (not PLAYERRACING or (self.id ~= aiVehicles[playerConfig.car].id or playerConfig.finished))) then 
-		self:vehicleController()
-
-		if(GetPlayerVehicle() == self.id and DEBUG) then
-			DebugWatch("current lap:",self.raceValues.laps)
-
-		end
-	end
-		-- DebugWatch("velocity:", VecLength(GetBodyVelocity(GetVehicleBody(self.id))))
-
-	
-end
-
-function ai:update(dt)
-	if(RACESTARTED) then
-
-		-- self:vehicleController()
-	end
-	
-end
-
-function ai:raceController()
-	if(RACESTARTED) then 
-		if(PLAYERRACING and self.id == aiVehicles[playerConfig.car].id) then 
-			self:player_raceController()
-		else
-
-			self:raceDetailsHandler()
-
-
-			self:controlActions()
-
-			local vehiclePos = GetVehicleTransform(self.id).pos
-			local indexVal = posToInt(vehiclePos)
-			-- DebugWatch("vec1: ",Vec(indexVal[1],0,indexVal[3]))
-			-- DebugWatch("vec2: ",Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2]))
-			-- 	DebugWatch("dist to goal",VecLength( VecSub(
-				-- 	Vec(indexVal[1],0,indexVal[3]),
-				-- 	Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-				-- )
-			if(VecLength( VecSub(
-					Vec(indexVal[1],0,indexVal[3]),
-					Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-			<self.raceValues.completionRange) then 
-				
-					self.raceValues.targetNode = self.raceValues.targetNode%#path +1
-					self.raceValues.NextNode = self.raceValues.targetNode%#path +1
-
-					self.goalPos = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]:getPos()
-					self.targetNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-					
-					self.NextNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-
-
-
-
-					self.raceValues.completedGoals = self.raceValues.completedGoals + 1
-
-					if(math.floor(self.raceValues.completedGoals/(#path+1))>self.raceValues.laps) then 
-
-						if(	not self.raceValues.bestLap) then
-							self.raceValues.bestLap = raceManager:lapTime()
-
-						elseif (raceManager:lapTime()-self.raceValues.lastLap < self.raceValues.bestLap )then
-							self.raceValues.bestLap = raceManager:lapTime()-self.raceValues.lastLap
-						end
-
-						--- add player lastlap if vehicle is player 
-						if(PLAYERRACING and (self.id == aiVehicles[playerConfig.car].id and not playerConfig.finished)) then 
-							playerConfig.bestLap = self.raceValues.bestLap 
-							playerConfig.hudInfo.lapInfo[3].time =  self.raceValues.bestLap 
-							-- DebugPrint(playerConfig.hudInfo.lapInfo[3].time)
-						end
-						self.raceValues.lastLap = raceManager:lapTime()
-						playerConfig.hudInfo.lapInfo[2].time = self.raceValues.lastLap 
-
-					end
-					self.raceValues.laps = math.floor(self.raceValues.completedGoals/(#path+1))
-			else
-				-- SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
-			end
-
-		end
-	end
-
-	-- DebugWatch("checkpoint: ",self.goalPos)
-
-
-
-end
-
-
-function ai:player_raceController()
-	if(RACESTARTED) then 
-
-		self:raceDetailsHandler()
-
-
-		self:controlActions()
-
-		local vehiclePos = GetVehicleTransform(self.id).pos
-		local indexVal = posToInt(vehiclePos)
-		-- DebugWatch("vec1: ",Vec(indexVal[1],0,indexVal[3]))
-		-- DebugWatch("vec2: ",Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2]))
-		-- 	DebugWatch("dist to goal",VecLength( VecSub(
-			-- 	Vec(indexVal[1],0,indexVal[3]),
-			-- 	Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-			-- )
-
-		local player_hit_range = self.raceValues.completionRange
-
-
-		if(self.raceValues.targetNode%#path +1 >2 ) then
-			player_hit_range = player_hit_range * 1
-		end
-		node_hit,new_node = self:player_check_future(player_hit_range)
-		if(DEBUG)then 
-			DebugPrint(tostring(node_hit).." | "..new_node)
-		end
-		if(node_hit) then 
-			
-				self.raceValues.targetNode = self.raceValues.targetNode%#path +1
-				self.raceValues.NextNode = self.raceValues.targetNode%#path +1
-
-				self.goalPos = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]:getPos()
-				self.targetNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-				
-				self.NextNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-
-
-
-
-				self.raceValues.completedGoals = self.raceValues.completedGoals + 1
-
-				if(math.floor(self.raceValues.completedGoals/(#path+1))>self.raceValues.laps) then 
-
-					if(	not self.raceValues.bestLap) then
-						self.raceValues.bestLap = raceManager:lapTime()
-
-					elseif (raceManager:lapTime()-self.raceValues.lastLap < self.raceValues.bestLap )then
-						self.raceValues.bestLap = raceManager:lapTime()-self.raceValues.lastLap
-					end
-
-					--- add player lastlap if vehicle is player 
-					if(PLAYERRACING and (self.id == aiVehicles[playerConfig.car].id and not playerConfig.finished)) then 
-						playerConfig.bestLap = self.raceValues.bestLap 
-						playerConfig.hudInfo.lapInfo[3].time =  self.raceValues.bestLap 
-						-- DebugPrint(playerConfig.hudInfo.lapInfo[3].time)
-					end
-					self.raceValues.lastLap = raceManager:lapTime()
-					playerConfig.hudInfo.lapInfo[2].time = self.raceValues.lastLap 
-
-				end
-				self.raceValues.laps = math.floor(self.raceValues.completedGoals/(#path+1))
-		elseif(VecLength( VecSub(
-					Vec(indexVal[1],0,indexVal[3]),
-					Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-			>(self.raceValues.completionRange*5)) then 
-			-- DebugPrint("test range: "..(self.raceValues.completionRange*30)..
-			-- 	"current len: "..VecLength( VecSub(
-			-- 		Vec(indexVal[1],0,indexVal[3]),
-			-- 		Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2]))))
-			SetString("hud.notification", "Too far from race track last location, look for flame on track")
-			SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
-		end
-
-
-	end
-
-	-- DebugWatch("checkpoint: ",self.goalPos)
-
-
-
-end
-
-function ai:player_check_future(player_hit_range)
-	local next_point = nil 
-	local vehiclePos = GetVehicleTransform(self.id).pos
-	local indexVal = posToInt(vehiclePos)
-	local target = 0
-	for i=0,15 do 
-		target =(((self.raceValues.targetNode-1) +i)%#path )+1
-		if(DEBUG) then 
-			DebugPrint("target pos is: "..target.." path length: "..#path)
-			SpawnParticle("fire", Vec(path[target][1],0,path[target][2]), Vec(0,5,0), 0.5, 1)
-		end
-		
-		if(VecLength( VecSub(
-							Vec(indexVal[1],0,indexVal[3]),
-							Vec(path[target][1],0,path[target][2])))
-							<player_hit_range)
-		then 
-			if(DEBUG) then 
-				DebugPrint(target.." id "..i)
-			end
-			return true, i
-		end
-	end
-	return false,0
- 
-end
-
---- handle race position / laps / checkpoints
-	-- raceValues = {
-	-- 	completedGoals  = 0,
-	-- 	targetNode 		= 1,
-	-- nextCheckpoint = 1,
-		-- passedCheckPoints = 0,
-	-- 	completionRange = 4,
-	-- 	lookAhead = 2,
-	-- 	laps = 0 	
-		-- splits = {}
-
-	-- },
-
-
-
-function ai:raceDetailsHandler()
-	
-	if IsVehicleInTrigger(self.raceValues.nextCheckpoint, self.id) then
-		
-
-	end
-
-
-	if (self.raceValues.targetNode%#path) == 0 then
-		
-
-	end
-	
-end
-
-
-function ai:goalDistance()
-	return VecLength( VecSub(self:getPos(),self.goalPos))
-end
-
-function ai:getPos()
-	return GetVehicleTransform(self.id).pos
-end
-
-function ai:markLoc()
-	
-	if InputPressed("g") and not RACESTARTED  then
-
-		RACESTARTED = true
-		DebugPrint("race Started")
-		self.currentCheckpoint = self.currentCheckpoint+1
-		self.goalOrigPos = GetTriggerTransform(self.currentCheckpoint).pos
-
-		self.goalPos = TransformToParentPoint(GetTriggerTransform(self.currentCheckpoint),Vec(math.random(-7,7),0,math.random(5,10)))
-
-		-- local camera = GetCameraTransform()
-		-- local aimpos = TransformToParentPoint(camera, Vec(0, 0, -300))
-		-- local hit, dist,normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aimpos, camera.pos)), 200,0)
-		-- if hit then
-			
-		-- 	self.goalPos = TransformToParentPoint(camera, Vec(0, 0, -dist))
-
-		-- end 	
-
-		-- DebugPrint("hitspot"..VecStr(goalPos).." | "..dist.." | "..VecLength(
-		-- 							VecSub(GetVehicleTransform(vehicle.id).pos,goalPos)))
-	end
-
-	if(RACESTARTED) then 
-		if(IsVehicleInTrigger(self.currentCheckpoint,self.id)) then
-			self.raceCheckpoint = (self.raceCheckpoint%#checkpoints)+1
-			for key,value in ipairs(checkpoints) do 
-				
-				if(tonumber(GetTagValue(value, "checkpoint"))==self.raceCheckpoint) then 
-					self.currentCheckpoint = value
-					self.goalOrigPos = GetTriggerTransform(self.currentCheckpoint).pos
-
-					self.goalPos =TransformToParentPoint(GetTriggerTransform(self.currentCheckpoint),Vec(math.random(-7,7),0,math.random(5,10)))
-				end
-			end
-
-			end
-
-		-- DebugWatch("checkpoint: ",raceCheckpoint)
-		-- DebugWatch("goalpos",VecLength(goalPos))
-		--SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
-	end
-
-
-end
-
-
-
-	-- reversingController = {
-	-- 	reversing = false,
-	-- 	minVelocity = 1,
-	-- 	waitTime = 3,
-	-- 	currentWait = 3,
-	-- 	reverseTime = 2,
-	-- 	currentReverseTime = 2,
-	-- },
-
-function ai:controlActions(dt)
-	if(not self.reversingController.reversing) then 
-		if(VecLength(GetBodyVelocity(GetVehicleBody(self.id)))<self.reversingController.minVelocity) then
-			if(self.reversingController.currentWait<0) then
-				self.reversingController.reversing = true
-			end
-			self.reversingController.currentWait = self.reversingController.currentWait - GetTimeStep()
-		elseif(self.reversingController.currentWait  ~= self.reversingController.waitTime) then
-			self.reversingController.currentWait  = self.reversingController.waitTime
-		end
-
-		if(self.usingClustering) then
-			self:scanPos()
-		end
-		local steeringValue = -self:pid()
-		local accelerationValue = self:accelerationError()
-		
-		
-		-- DebugWatch("pre acceletation: ",self.controller.accelerationValue)
-		-- DebugWatch("pre steering: ",self.controller.steeringValue)
-
-
-		self.controller.steeringValue = steeringValue * self.steeringCoef
-		self.controller.accelerationValue = accelerationValue*self.accelerationCoef
-
-		self:controllerAugmentation()
-		-- DebugWatch("post acceletation: ",self.controller.accelerationValue)
-		-- DebugWatch("post steering: ",self.controller.steeringValue)
-
-		self:obstacleAvoidance()
-
-
-
-		self:applyError()
-			
-			--- apply reversing error
-
-		local directionError =  self:directionError()
-		self.controller.accelerationValue = self.controller.accelerationValue * directionError
-		
-		    --- apply steering safety error
-		if(self.controller.accelerationValue>0)then 
-			local corneringErrorMagnitude = self:corneringError()
-			self.controller.accelerationValue = self.controller.accelerationValue * corneringErrorMagnitude
-		end
-		self.controller.steeringValue = self.controller.steeringValue  * directionError
-	else
-		if(self.reversingController.currentReverseTime >0) then
-			self.controller.accelerationValue = -1
-			self.controller.steeringValue = -self.controller.steeringValue 
-			self.reversingController.currentReverseTime = self.reversingController.currentReverseTime - GetTimeStep()
-		else
-			self.reversingController.reversing = false
-			self.reversingController.currentReverseTime = self.reversingController.reverseTime
-			self.reversingController.currentWait = self.reversingController.waitTime
-		end
-		
-	end
-end
-
-
-function ai:controllerAugmentation()
-	local velocity =  VecLength(GetBodyVelocity(GetVehicleBody(self.id)))
-
-	if(math.abs(self.controller.accelerationValue)>1.5 and velocity>self.cornerCoef and self.controller.accelerationValue*0.8 ~=0
-		and math.abs(self.controller.steeringValue) >= self.controller.speedSteeringThres) then
-		
-		self.controller.accelerationValue = (math.log(self.controller.accelerationValue*0.4)) - math.abs(self.controller.steeringValue*self.steeringCoef)
-	else 
-		self.controller.accelerationValue  = 1
-	end
-	
-	
-end
-
-function ai:obstacleAvoidance()
-	local scanResults = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
-	local scanShapes = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
-	local scanhitPos = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
-	local scanDists = {centre=0,left =0, sideL =0 , sideR =0, right = 0}
-	local vehicleTransform = GetVehicleTransform(self.id)
-
-	local front = self.bodyYSize/4 
-	local side = self.bodyXSize/4
-	local height = self.bodyZSize /6
-	-- DebugWatch("height",self.bodyZSize)
-	-- DebugWatch("width",self.bodyXSize)
-	-- DebugWatch("length",self.bodyYSize)
-	vehicleTransform.pos = TransformToParentPoint(vehicleTransform,Vec(0,height/4	,-front/4))
-	local testScanRot = nil
-	local fwdPos = nil
-	local direction = nil
-	local scanStartPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
-	local scanEndPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
-
-	local scanLength = 2+ self.scanning.maxScanLength*((VecLength(GetBodyVelocity(GetVehicleBody(self.id))))/self.scanning.maxScanLength)
-
-	for key,scan in pairs(self.scanning.positions) do 
-
-
-		if(scan.direction == "centre") then 
-			scanStartPos =VecCopy(vehicleTransform.pos)
-		elseif(scan.direction =="left") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/6,0,front/8))
-		elseif(scan.direction =="right") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/6,0,front/8))
-		elseif(scan.direction =="sideR") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/5,0,front/4))
-		elseif(scan.direction =="sideL") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/5,0,front/4))
-		end
-
-		scanEndPos = TransformToParentPoint(Transform(scanStartPos,vehicleTransform.rot),scan.startVec)
-		testScanRot = QuatLookAt(scanEndPos,scanStartPos)
-
-		fwdPos = TransformToParentPoint(Transform(scanStartPos,testScanRot),  
-				Vec(0,0,-scanLength))---self.scanning.maxScanLength))
-		direction = VecSub(scanStartPos,fwdPos)
-		direction = VecNormalize(direction)
-	    QueryRejectVehicle(self.id)
-	    QueryRequire("dynamic large")
-
-	    local hit,dist,normal, shape = QueryRaycast(scanStartPos, direction, scanLength)--self.scanning.maxScanLength)
-	    scanResults[key] = hit
-	    scanDists[key] = dist
-	    scanShapes[key] = shape
-	    scanhitPos[key]	= VecScale(direction,dist)
-	    if(hit and DEBUGCARS) then
-
-			 DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 1, 0, 0)
-		elseif(DEBUGCARS) then
-			DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 0, 1, 0)
-		end
-	end
-
-	local turnBias = math.random()
-
-	if(scanResults.centre ) then 
-		-- DebugWatch("pre val:",self.controller.accelerationValue )
-		self.controller.accelerationValue =self.controller.accelerationValue* (self:getRelativeSpeed(scanShapes.centre,scanhitPos.center))--/self.controller.tenacity)
-		-- self.controller.accelerationValue = self.controller.accelerationValue    * self.controller.tenacity
-
-		-- DebugWatch("post val:",self.controller.accelerationValue )
-		-- DebugWatch("relative val:",relative )
-		
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and not scanResults.centre and  
-				(scanResults.left or scanResults.right or scanResults.sideL or scanResults.sideR)	) then
-		self.controller.accelerationValue = self.controller.accelerationValue    * 2
-
-	end
-	if(scanResults.left and scanResults.right) then 
-
-		self.controller.accelerationValue = self.controller.accelerationValue    * 0.5
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.left) then
-
-		self.controller.steeringValue = self.controller.steeringForce +(scanDists.left/(self.scanning.maxScanLength/2)/2)
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.right) then 
-
-		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.right/(self.scanning.maxScanLength/2)/2)
-	
-
-	--- handle sides 
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideL) then
-
-		self.controller.steeringValue = self.controller.steeringForce +(scanDists.sideL/(self.scanning.maxScanLength/2)/4)
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideR) then
-
-		
-		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.sideR/(self.scanning.maxScanLength/2)/4)
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.centre ) then 
-		--- random moving vs best direction 
-
-		 -- sign((Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax))
-
-
-		if turnBias <0.5 then
-			self.controller.steeringValue = self.controller.steeringForce*2
-		else
-			self.controller.steeringValue = -self.controller.steeringForce*2
-		end
-
-	
-	end
-end
-
-
-
-
--- function ai:obstacleAvoidance()
--- 	local scanResults = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
--- 	local scanShapes = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
--- 	local scanhitPos = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
--- 	local scanDists = {centre=0,left =0, sideL =0 , sideR =0, right = 0}
--- 	local vehicleTransform = GetVehicleTransform(self.id)
-
--- 	local front = self.bodyYSize/4 
--- 	local side = self.bodyXSize/4
--- 	local height = self.bodyZSize /4
-
--- 	vehicleTransform.pos = TransformToParentPoint(vehicleTransform,Vec(0,height/4	,-front/4))
--- 	local testScanRot = nil
--- 	local fwdPos = nil
--- 	local direction = nil
--- 	local scanStartPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
--- 	local scanEndPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
-
--- 	local scanLength = 2+ self.scanning.maxScanLength*((VecLength(GetBodyVelocity(GetVehicleBody(self.id))))/self.scanning.maxScanLength)
-
--- 	for key,scan in pairs(self.scanning.positions) do 
-
-
--- 		if(scan.direction == "centre") then 
--- 			scanStartPos =VecCopy(vehicleTransform.pos)
--- 		elseif(scan.direction =="left") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/6,0,front/8))
--- 		elseif(scan.direction =="right") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/6,0,front/8))
--- 		elseif(scan.direction =="sideR") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/5,0,front/4))
--- 		elseif(scan.direction =="sideL") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/5,0,front/4))
--- 		end
-
--- 		scanEndPos = TransformToParentPoint(Transform(scanStartPos,vehicleTransform.rot),scan.startVec)
--- 		testScanRot = QuatLookAt(scanEndPos,scanStartPos)
-
--- 		fwdPos = TransformToParentPoint(Transform(scanStartPos,testScanRot),  
--- 				Vec(0,0,-scanLength))---self.scanning.maxScanLength))
--- 		direction = VecSub(scanStartPos,fwdPos)
--- 		direction = VecNormalize(direction)
--- 	    QueryRejectVehicle(self.id)
--- 	    QueryRequire("dynamic large")
-
--- 	    local hit,dist,normal, shape = QueryRaycast(scanStartPos, direction, scanLength)--self.scanning.maxScanLength)
--- 	    scanResults[key] = hit
--- 	    scanDists[key] = dist
--- 	    scanShapes[key] = shape
--- 	    scanhitPos[key]	= VecScale(direction,dist)
--- 	    if(hit and DEBUGCARS) then
-
--- 			 DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 1, 0, 0)
--- 		elseif(DEBUGCARS) then
--- 			DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 0, 1, 0)
--- 		end
--- 	end
-
--- 	local turnBias = math.random()
-
--- 	if(scanResults.centre ) then 
--- 		-- DebugWatch("pre val:",self.controller.accelerationValue )
--- 		self.controller.accelerationValue =self.controller.accelerationValue* (self:getRelativeSpeed(scanShapes.centre,scanhitPos.center))--/self.controller.tenacity)
--- 		-- self.controller.accelerationValue = self.controller.accelerationValue    * self.controller.tenacity
-
--- 		-- DebugWatch("post val:",self.controller.accelerationValue )
--- 		-- DebugWatch("relative val:",relative )
-		
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and not scanResults.centre and  
--- 				(scanResults.left or scanResults.right or scanResults.sideL or scanResults.sideR)	) then
--- 		self.controller.accelerationValue = self.controller.accelerationValue    * 2
-
--- 	end
--- 	if(scanResults.left and scanResults.right) then 
-
--- 		self.controller.accelerationValue = self.controller.accelerationValue    * 0.5
-
-
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.centre ) then 
--- 		--- random moving vs best direction 
-
--- 		 -- sign((Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax))
-
--- 		if(scanResults.left and not scanResults.right) then
--- 			self.controller.steeringValue = 0.5
--- 		elseif(not scanResults.left and scanResults.right) then
--- 			self.controller.steeringValue = -0.5
--- 		elseif(not scanResults.left and not scanResults.right) then 
-
--- 			if turnBias <0.5 then
--- 				self.controller.steeringValue = self.controller.steeringForce*2
--- 			else
--- 				self.controller.steeringValue = -(self.controller.steeringForce)*2
--- 			end
--- 		end
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.left) then
-
--- 		self.controller.steeringValue = self.controller.steeringForce +(scanDists.left/(self.scanning.maxScanLength/2)/2)
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.right) then 
-
--- 		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.right/(self.scanning.maxScanLength/2)/2)
-	
-
--- 	--- handle sides 
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideL) then
-
--- 		self.controller.steeringValue = self.controller.steeringForce +(scanDists.sideL/(self.scanning.maxScanLength/2)/4)
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideR) then
-
-		
--- 		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.sideR/(self.scanning.maxScanLength/2)/4)
-
--- 	end
--- end
-
-
-
---[[
-
-	calculate relative speed, if vehicle moving towards then stop / avoid. 
-
-	if movng faster than gap between then stop, otherwise move proportionally to the distance between vehicles vs speed
-
-]]
-
-function ai:getRelativeSpeed(shape,hitPos)
-	local otherShapeBody = GetShapeBody(shape)
-	local otherShapeBodyPos = GetBodyTransform(otherShapeBody).pos
-	local otherShapeVelocity =  GetBodyVelocity(otherShapeBody)
-	local vehicleBody = GetVehicleBody(self.id)
-	local vehicleBodyPos = GetBodyTransform(vehicleBody).pos
-	local vehicleVelocity = GetBodyVelocity(vehicleBody) 
-
-	local toPoint = VecSub(vehicleBodyPos,otherShapeBodyPos)
-	local movingTowards = false
-	---VecSub(vehicleVelocity,otherShapeVelocity)
-	-- DebugWatch("otherShapeVelocity",VecLength(otherShapeVelocity))
-	-- DebugWatch("vehicleVelocity",VecLength(vehicleVelocity))
-
-	local adjustmentValue = 0 
-
-	--[[
-		if crash likely then set adjustment to -1 (GTFO mode)
-		elseif speed greater than safe range then force slow down
-			else adjust speed to maintain safe distance 
-		else set to higher speed to get closer for overtaking
-	]]
-	local minDist = self.controller.minDist
-	if(VecLength(vehicleVelocity) >0) then 
-		 minDist = minDist / math.log(VecLength(vehicleVelocity))
-	end
-
-	
-	if(VecDot(toPoint,otherShapeVelocity)>0) then 
-		adjustmentValue = -1
-		if(DEBUG_SAE) then 
-			DebugWatch("slowing for safety",1)
-		end
-	elseif(VecLength(otherShapeVelocity)<VecLength(vehicleVelocity)) then 
-		local relativeSpeed = VecLength(vehicleVelocity)-VecLength(otherShapeVelocity) 
-		local relativeDistance = VecLength(VecSub(vehicleBodyPos,hitPos))
-			--- set mindist to be math.log of relative speed, relative speed is negative if they are faster
-			--- dist coef 
-		if(relativeSpeed ~=0) then 
-			 minDist =  math.log((relativeSpeed))*math.sign(relativeSpeed)
-		end
-		local distCoef = relativeDistance-minDist
-
-		if((relativeSpeed) > distCoef) then
-			adjustmentValue = -(distCoef/(relativeSpeed*2))
-		else
-			adjustmentValue = (relativeSpeed/distCoef)--(0.2) + relativeSpeed/(relativeDistance)--*self.controller.tenacity)
-			-- adjustmentValue=1
-		end
-		
-	else
-		adjustmentValue=2
-	end
-	if(DEBUG_SAE) then
-		DebugWatch("minDist",minDist)
-		DebugWatch("adjusting",adjustmentValue)
-	end
-	return adjustmentValue
-
-end
+#version 2
+local minDist = self.controller.minDist
 
 function ai:turnDirection()
 	
 end
-
 
 function ai:applyError()
 	local errorCoef = self.controller.errorCoef--0.1
@@ -1917,19 +20,15 @@
 	local boundsSize = VecSub(max, min)
 	local center = VecLerp(min, max, 0.5)
 
-
 	-- DebugWatch("boundsize",boundsSize)
 	-- DebugWatch("center",center)
 
 	vehicleTransform.pos = TransformToParentPoint(vehicleTransform,Vec(0,1.2	,0))
 
-
 	for key,scan in pairs(self.scanning.cones) do 
 
 		for i=1,ai.scanning.scanDepths do 
 			local scanLength = self.scanning.scanLength * i
-
-
 
 			local projectionAngle =  (math.sin(math.rad(scan.size)) * ((scanLength)))
 			if(scan.startVec[1]>0) then
@@ -1972,17 +71,13 @@
 
 	end
 
-
 	self:clusteringOperations()
-
 
 	self.clustering.clusters.current.pass = (self.clustering.clusters.current.pass%self.clustering.dataSize )+1 
 	self.clustering.clusters.current.index = 1
 
 end
 
-
---init clusters 
 function ai:clusteringCentroids()
 	local valRange = { min = { 100000, 100000, 100000},
 						max = {-100000 , -100000 , -100000 } 
@@ -2016,7 +111,6 @@
 	--DebugPrint("min:"..valRange.min[1]..","..valRange.min[2]..","..valRange.min[2].."\nMax: "..valRange.max[1]..","..valRange.max[2]..","..valRange.max[3])
 end
 
---init clusters 
 function ai:clusteringUpdateCentroids()
 	local pos = Vec(0,0,0)
 	local inputData = nil
@@ -2034,8 +128,6 @@
 	end
 end
 
-
--- find euclidian distance of data to clusters and update centroid locations
 function ai:clusteringCalculateClusters()
 	local pos = Vec(0,0,0)
 	local center = Vec(0,0,0)
@@ -2056,11 +148,9 @@
 
 end
 
---- perform operations on clusters to extract target
 function ai:clusteringOperations()
 	
 	self:clusteringCalculateClusters()
-
 
 	self:pseudoSNN()
 
@@ -2075,14 +165,6 @@
 	self.targetNode = self.clustering.clusters.centroids.data[self.clustering.mode]
 
 end
-
-
---- simulate an snn network slightly to get best node
-
--- if(SNNpspprev[j]<SNNpsp[i])
---  {
---      SNNweights[j][i]=tanh(gammaweights*SNNweights[j][i]+learningrateweights*SNNpspprev[j]*SNNpsp[i]);
---  }
 
 function ai:pseudoSNN()
 	local bestpsp = 100000000
@@ -2148,7 +230,6 @@
 	
 	--DebugPrint("values: index: "..index.."\nhitpos:"..VecStr(hitPos).."\nhitval: "..hitValue.."\nClusterPos = "..VecStr(self.clustering.clusters.current.data[index]:getPos()))
 	self.clustering.clusters.current.data[index]:push(hitPos[1],hitPos[2],hitPos[3],hitValue) 
-
 
 	self.clustering.clusters.current.index = (self.clustering.clusters.current.index%self.clustering.dataSize )+1
 end
@@ -2172,7 +253,6 @@
 	self.pidState.controllerValue = output
 	-- DebugWatch("pid output: ",output)
 
-
 	if(RACESTARTED and  self.pidState.training) then
 		if math.abs(crossTrackErrorRate) > self.pidState.learningrateThres then 
 			if(crossTrackErrorRate>0) then 
@@ -2191,7 +271,6 @@
 
 	return output
 end
-
 
 function ai:currentCrossTrackError()
 	local crossTrackErrorValue = 0
@@ -2204,10 +283,7 @@
 	return targetNode, crossTrackErrorValue,sign
 end
 
---- calculate distance to target direction and apply steering by force
---- fill in the gap here related to the distance ebtween the aprrelel lines of target nod3e to vehicle pos to solve it all
 function ai:crossTrackError(pnt,vehicleTransform)
-
 
 		
 		vehicleTransform.pos[2] = pnt[2]
@@ -2229,7 +305,6 @@
 			sign = 0
 		end
 
-
 		return d*sign,sign
 
 		-- Use the sign of the determinant of vectors (AB,AM), where M(X,Y) is the query point:	
@@ -2248,12 +323,6 @@
 		-- DebugWatch("output pos : ",out)
 
 		-- DebugWatch("output value: ",VecSub(out,pnt))
-
-
-
-
-
-
 
 		-- local vehicleTransform = GetVehicleTransform(self.id)
 		-- vehicleTransform.pos[2] = targetNode:getPos()[2]
@@ -2288,7 +357,6 @@
 	return verifyCrossCheckErrorVal
 end
 
-
 function ai:calculateSteadyStateError(crossTrackErrorValue)
 	local index = self.pidState.integralIndex
 
@@ -2332,13 +400,10 @@
 		-- DebugWatch("is forward",is_forward)
 		-- DebugWatch("local point  forwar", TransformToLocalPoint(vehicleTransform, pnt)[3])
 
-
 		return VecLength(VecSub(vehicleTransform.pos,out))
 	end	
 end
 
-
-	-- thanks to  iaobardar for help on getting the vecdot to work
 function ai:directionError()
 	local vehicleTransform = GetVehicleTransform(self.id)
 	local targetNode = self.targetNode
@@ -2394,13 +459,6 @@
 
 end
 
-
-
-
-
-
- 
-
 function ai:vehicleController()
 	DriveVehicle(self.id, 0.05+self.controller.accelerationValue,
 							self.controller.steeringValue,
@@ -2416,11 +474,7 @@
 
 end
 
-
-
 function ai:costFunc(testPos,hit,dist,shape,key)
-
-
 
 	local cost = 10000 
 	if(not hit) then
@@ -2428,8 +482,6 @@
 	end
 	return cost
 end
-
-
 
 function ai:controlVehicle( targetCost)
 	local hBrake = false
@@ -2459,7 +511,6 @@
 				targetMove[3] = targetMove[3] *2
 			end
 
-
 			DriveVehicle(self.id, -targetMove[3]*drivePower,-targetMove[1], hBrake)
 			-- DebugWatch("post updated",VecStr(targetMove))
 			-- DebugWatch("motion2",VecStr(detectPoints[targetCost.key]))
@@ -2468,34 +519,6 @@
 		end
 	end
 end
-
-
--- function ai:modulo(a,b )
--- 	return a - math.floor(a/b)*b
-	
--- end
-
-------------------------------------------------
-
-
----- PATHFINDING
-
-
------------------------------------------------------
-
-
-
----- 
-
-
-
----- use flood fill to comap[re to last neighbor  that was known and if neighbor foun and  track then 
-
----- compare the next based on known locations nd move outwards.]
-
-----
-
-
 
 function scanGrid(x,y)
   local pos = Vec(0,0,0)
@@ -2542,8 +565,6 @@
   return gridScore,validTerrain, minHeight
 end
 
-
-
 function getHeight(x,y)
 
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -2613,7 +634,6 @@
   return score
 
 end
-
 
 function getMaterialScore3(x,y)
   local score = 0
@@ -2682,14 +702,9 @@
   return pos,pos2
 end
 
-
 function Heuristic(a, b)
       return Math.Abs(a[1] - b[1]) + Math.Abs(a[3] - b[3]);
- end 
-
-
-
-
+ end
 
 function checkIfTerrainValid(mat,r,g,b)
 		local score = 0
@@ -2724,20 +739,6 @@
 	    return score
 end
 
-
-
-
-
-
-
----------------------------------------------------------
-
-
-
-
--------------------------------------------------------
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
@@ -2751,8 +752,6 @@
 	end
 
 end
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -2769,7 +768,6 @@
     return copy
 end
 
-
 function inRange(min,max,value)
 		if(tonumber(min) < tonumber(value) and tonumber(value)<=tonumber(max)) then 
 			return true
@@ -2780,40 +778,32 @@
 
 end
 
-
-
-
-function draw()
-
-
-	if(not RACESTARTED and not RACECOUNTDOWN) then
-		raceManager:drawIntro()
-		-- DebugWatch("TRYING",RACECOUNTDOWN)
-	end
-
-	if(PATHSET and not RACEENDED) then 
-
-		-- raceManager:testRect( )
-		raceManager:driverNameDisplay()
-		raceManager:draw()
-
-	end
-
-
-	if(raceManager.countdown > 0 and  raceManager.preCountdown <=0 ) then
-		raceManager:drawStart()
-	end
-	
-	for key,vehicle in pairs(aiVehicles) do 
-
-		if(RACESTARTED and PLAYERRACING and key == playerConfig.car  and not playerConfig.finished and not RACEENDED and not DEBUGCONTROLLERS ) then
-			raceManager:playerRaceStats(vehicle)
-			-- DebugPrint(key.. " | "..playerConfig.car )
-		elseif( PLAYERRACING and key == playerConfig.car and  RACEENDED) then
-			raceManager:endScreen(vehicle)
-		end
-	end	
-
-end
-
-
+function client.draw()
+    if(not RACESTARTED and not RACECOUNTDOWN) then
+    	raceManager:drawIntro()
+    	-- DebugWatch("TRYING",RACECOUNTDOWN)
+    end
+
+    if(PATHSET and not RACEENDED) then 
+
+    	-- raceManager:testRect( )
+    	raceManager:driverNameDisplay()
+    	raceManager:draw()
+
+    end
+
+    if(raceManager.countdown > 0 and  raceManager.preCountdown <=0 ) then
+    	raceManager:drawStart()
+    end
+
+    for key,vehicle in pairs(aiVehicles) do 
+
+    	if(RACESTARTED and PLAYERRACING and key == playerConfig.car  and not playerConfig.finished and not RACEENDED and not DEBUGCONTROLLERS ) then
+    		raceManager:playerRaceStats(vehicle)
+    		-- DebugPrint(key.. " | "..playerConfig.car )
+    	elseif( PLAYERRACING and key == playerConfig.car and  RACEENDED) then
+    		raceManager:endScreen(vehicle)
+    	end
+    end	
+end
+

```

---

# Migration Report: scripts\camera\smoothcam.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\camera\smoothcam.lua
+++ patched/scripts\camera\smoothcam.lua
@@ -1,188 +1,4 @@
-
--- emils camera script to make nice smooth floaty cameras 
-
-
-DEBUG = false
-
-cameraControlTag = "cameraController"
-cameraKeyword = "panCam" 
-
-function init()
-	cameraController = FindLocation(cameraControlTag,true)
-
-	lastCamKeyword = "nil"
-
-	speed = GetFloatParam("speed",5)
-	activateKey = GetStringParam("activateKey","m")
-	if string.len(activateKey) == 0 then
-		activateKey = "m"
-	end
-	if string.len(activateKey) > 1 then
-		activateKey = string.sub(activateKey,1,1)
-	end
-
-	fixedCamTransform = nil
-	feetToEye = 1.6933022737503
-	lastCamDirection = nil
-	lastPointSet = nil
-	pointSet = {}
-	nextPointSet = {}
-	fadePos = GetPlayerTransform().pos
-	fadeRot = GetPlayerTransform().rot
-	t = nil
-	tn = nil
-	active = false
-	fade = 0
-	pathTimer = 0
-	nextCam = -3
-	timeInt = -1
-
-	--##############
-
-	camlocations = FindLocations("camlocation", true)
-	if #camlocations < 4 then
-		DebugPrint("Too few camera locations setup for Smoothcam.")
-		return
-	end
-
-	-- Order the camlocations according to the value of their respective camlocation tag into the array smoothcams
-	smoothcams = {}
-	for i = 1, #camlocations do
-		--smoothcams[tonumber(GetTagValue(camlocations[i],"camlocation"))] = GetLocationTransform(camlocations[i])
-		smoothcams[i] = GetLocationTransform(camlocations[i])
-		-- local val = GetTagValue(camlocations[i],"camlocation")
-	end
-
-	-- Break if the number of smoothcams doesn't match the number of camlocations, indicating the camlocations ahs been wrongly numbered
-	if #smoothcams ~= #camlocations then
-		DebugPrint("Camera locations does not appear to be numbered correctly for Smoothcam.")
-		return
-	end
-	
-	-- Duplicate first 4 cameralocations to the last four
-	for i = 1, 4 do
-		smoothcams[#smoothcams+1] = smoothcams[i]
-	end
-
-	bezierPoints = {}
-	for i = 2, #smoothcams-1, 2 do
-		bezierPoints[#bezierPoints+1] = bezierCenter(smoothcams[i-1].pos, smoothcams[i].pos)
-		bezierPoints[#bezierPoints+1] = smoothcams[i].pos
-		bezierPoints[#bezierPoints+1] = smoothcams[i+1].pos
-
-		if i + 2 <= #smoothcams then
-			bezierPoints[#bezierPoints+1] = bezierCenter(smoothcams[i+1].pos, smoothcams[i+2].pos)
-		end
-	end
-end
-
-function tick(dt)
-	-- if InputPressed(activateKey) then
-	-- 	active = active ~= true -- toggle state of active on press of the activateKey
-	-- 	if active then
-	-- 		fixedCamTransform = GetCameraTransform()
-	-- 		DebugPrint("active is now: true")
-	-- 		SetValue("fade",1,"cosine",3*(1-fade))
-	-- 		fadePos = VecAdd(GetPlayerTransform().pos,Vec(0,feetToEye,0))
-	-- 		fadeRot = GetPlayerTransform().rot
-	-- 	else
-	-- 		DebugPrint("active is now: false")
-	-- 		SetValue("fade",0,"cosine",3*fade)
-	-- 	end
-	-- end
-
-	-- DebugWatch("cam tag val ", GetTagValue(cameraController, cameraControlTag))
-
-	local currentKeyword = GetTagValue(cameraController, cameraControlTag) 
-	if currentKeyword ~= lastCamKeyword and currentKeyword == cameraKeyword then
-		active =  true -- toggle state of active on press of the activateKey
-		fixedCamTransform = GetCameraTransform()
-		-- DebugPrint("active is now: true")
-		SetValue("fade",1,"cosine",3*(1-fade))
-		fadePos = VecAdd(GetPlayerTransform().pos,Vec(0,feetToEye,0))
-		fadeRot = GetPlayerTransform().rot
-			
-	elseif(currentKeyword ~= lastCamKeyword and currentKeyword ~= cameraKeyword) then
-		active = false -- toggle state of active on press of the activateKey
-			-- DebugPrint("active is now: false")
-			SetValue("fade",0,"cosine",3*fade)
-	end
-	
-	lastCamKeyword = currentKeyword
-	local subPathTimer = (pathTimer/speed) % 1
-	
-	if math.floor(pathTimer/speed) > timeInt then
-		nextCam = nextCam + 4
-		timeInt = math.floor(pathTimer/speed)
-		if nextCam > #bezierPoints-4 then
-			--print("loop")
-			nextCam = nextCam - #bezierPoints+4
-		end
-		--print("New pointSet")
-		local currentPoint = nextCam
-		local nextPointSetCurrentPoint = nextCam + 4
-		local setCounter = 1
-		for i = nextCam,nextCam+3 do
-			while currentPoint > #bezierPoints do
-				currentPoint = currentPoint - #bezierPoints
-			end
-			while nextPointSetCurrentPoint > #bezierPoints do
-				nextPointSetCurrentPoint = nextPointSetCurrentPoint - #bezierPoints
-			end
-			pointSet[setCounter] = bezierPoints[currentPoint]
-			nextPointSet[setCounter] = bezierPoints[nextPointSetCurrentPoint]
-			currentPoint = currentPoint + 1
-			nextPointSetCurrentPoint = nextPointSetCurrentPoint + 1
-			setCounter = setCounter + 1
-		end
-	end
-
-	if active then
-		t = cubicBezier(pointSet, subPathTimer) --bezierPoints[nextCam], bezierPoints[nextCam+1], bezierPoints[nextCam+2], bezierPoints[nextCam+3]
-		if subPathTimer + 0.1 >= 1 then
-			tn = cubicBezier(nextPointSet, subPathTimer + 0.1 - 1)
-		else
-			tn = cubicBezier(pointSet, subPathTimer + 0.1)
-		end
-
-		fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform().pos,Vec(0,feetToEye,0)),t,fade), 0.05)
-		fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform().rot,QuatLookAt(t, tn),fade),0.05)
-
-		if true then
-			local c = nextCam
-			while c+4 > #smoothcams do
-				c = c - #smoothcams
-			end
-		end
-		SetCameraTransform(Transform(fadePos,fadeRot))
-	else
-		if fade > 0 then
-			t = cubicBezier(pointSet, subPathTimer)
-			if subPathTimer + 0.1 >= 1 then
-				tn = cubicBezier(nextPointSet, subPathTimer + 0.1 - 1)
-			else
-				tn = cubicBezier(pointSet, subPathTimer + 0.1)
-			end
-			fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform().pos,Vec(0,feetToEye,0)),t,fade), 0.05)
-			fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform().rot,QuatLookAt(t, tn),fade),0.05)
-			SetCameraTransform(Transform(fadePos,fadeRot))
-		end
-	end
-	if(DEBUG) then
-		DebugWatch("bezierPoints: ", #bezierPoints)
-		DebugWatch("pathTimer: ", pathTimer)
-		DebugWatch("pathTimer/speed: ", (pathTimer/speed))
-		DebugWatch("subPathTimer: ", subPathTimer)
-		DebugWatch("fade: ", fade)
-		DebugWatch("timeInt: ", timeInt)
-		DebugWatch("dt: ", dt)
-		DebugWatch("subPathTimer % 0.25: ", (subPathTimer % 0.25))
-	end
-	if active or fade > 0 then
-		pathTimer = pathTimer + dt
-	end
-end
-
+#version 2
 function cubicBezier(ps,t)
 	local x = cubicBezierPoint(ps[1][1],ps[2][1],ps[3][1],ps[4][1],t)
 	local y = cubicBezierPoint(ps[1][2],ps[2][2],ps[3][2],ps[4][2],t)
@@ -202,4 +18,155 @@
 	local z = (a[3] + b[3]) / 2
 	local v = Vec(x,y,z)
 	return v
-end+end
+
+function server.init()
+    cameraController = FindLocation(cameraControlTag,true)
+    lastCamKeyword = "nil"
+    speed = GetFloatParam("speed",5)
+    activateKey = GetStringParam("activateKey","m")
+    if string.len(activateKey) == 0 then
+    	activateKey = "m"
+    end
+    if string.len(activateKey) > 1 then
+    	activateKey = string.sub(activateKey,1,1)
+    end
+    fixedCamTransform = nil
+    feetToEye = 1.6933022737503
+    lastCamDirection = nil
+    lastPointSet = nil
+    pointSet = {}
+    nextPointSet = {}
+    fadePos = GetPlayerTransform(playerId).pos
+    fadeRot = GetPlayerTransform(playerId).rot
+    t = nil
+    tn = nil
+    active = false
+    fade = 0
+    pathTimer = 0
+    nextCam = -3
+    timeInt = -1
+    --##############
+    camlocations = FindLocations("camlocation", true)
+    if #camlocations < 4 then
+    	DebugPrint("Too few camera locations setup for Smoothcam.")
+    	return
+    end
+    -- Order the camlocations according to the value of their respective camlocation tag into the array smoothcams
+    smoothcams = {}
+    for i = 1, #camlocations do
+    	--smoothcams[tonumber(GetTagValue(camlocations[i],"camlocation"))] = GetLocationTransform(camlocations[i])
+    	smoothcams[i] = GetLocationTransform(camlocations[i])
+    	-- local val = GetTagValue(camlocations[i],"camlocation")
+    end
+    -- Break if the number of smoothcams doesn't match the number of camlocations, indicating the camlocations ahs been wrongly numbered
+    if #smoothcams ~= #camlocations then
+    	DebugPrint("Camera locations does not appear to be numbered correctly for Smoothcam.")
+    	return
+    end
+    -- Duplicate first 4 cameralocations to the last four
+    for i = 1, 4 do
+    	smoothcams[#smoothcams+1] = smoothcams[i]
+    end
+    bezierPoints = {}
+    for i = 2, #smoothcams-1, 2 do
+    	bezierPoints[#bezierPoints+1] = bezierCenter(smoothcams[i-1].pos, smoothcams[i].pos)
+    	bezierPoints[#bezierPoints+1] = smoothcams[i].pos
+    	bezierPoints[#bezierPoints+1] = smoothcams[i+1].pos
+
+    	if i + 2 <= #smoothcams then
+    		bezierPoints[#bezierPoints+1] = bezierCenter(smoothcams[i+1].pos, smoothcams[i+2].pos)
+    	end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local currentKeyword = GetTagValue(cameraController, cameraControlTag) 
+        if currentKeyword ~= lastCamKeyword and currentKeyword == cameraKeyword then
+        	active =  true -- toggle state of active on press of the activateKey
+        	fixedCamTransform = GetCameraTransform()
+        	-- DebugPrint("active is now: true")
+        	SetValue("fade",1,"cosine",3*(1-fade))
+        	fadePos = VecAdd(GetPlayerTransform(playerId).pos,Vec(0,feetToEye,0))
+        	fadeRot = GetPlayerTransform(playerId).rot
+
+        elseif(currentKeyword ~= lastCamKeyword and currentKeyword ~= cameraKeyword) then
+        	active = false -- toggle state of active on press of the activateKey
+        		-- DebugPrint("active is now: false")
+        		SetValue("fade",0,"cosine",3*fade)
+        end
+        lastCamKeyword = currentKeyword
+        local subPathTimer = (pathTimer/speed) % 1
+        if math.floor(pathTimer/speed) > timeInt then
+        	nextCam = nextCam + 4
+        	timeInt = math.floor(pathTimer/speed)
+        	if nextCam > #bezierPoints-4 then
+        		--print("loop")
+        		nextCam = nextCam - #bezierPoints+4
+        	end
+        	--print("New pointSet")
+        	local currentPoint = nextCam
+        	local nextPointSetCurrentPoint = nextCam + 4
+        	local setCounter = 1
+        	for i = nextCam,nextCam+3 do
+        		while currentPoint > #bezierPoints do
+        			currentPoint = currentPoint - #bezierPoints
+        		end
+        		while nextPointSetCurrentPoint > #bezierPoints do
+        			nextPointSetCurrentPoint = nextPointSetCurrentPoint - #bezierPoints
+        		end
+        		pointSet[setCounter] = bezierPoints[currentPoint]
+        		nextPointSet[setCounter] = bezierPoints[nextPointSetCurrentPoint]
+        		currentPoint = currentPoint + 1
+        		nextPointSetCurrentPoint = nextPointSetCurrentPoint + 1
+        		setCounter = setCounter + 1
+        	end
+        end
+        if active then
+        	t = cubicBezier(pointSet, subPathTimer) --bezierPoints[nextCam], bezierPoints[nextCam+1], bezierPoints[nextCam+2], bezierPoints[nextCam+3]
+        	if subPathTimer + 0.1 >= 1 then
+        		tn = cubicBezier(nextPointSet, subPathTimer + 0.1 - 1)
+        	else
+        		tn = cubicBezier(pointSet, subPathTimer + 0.1)
+        	end
+
+        	fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform(playerId).pos,Vec(0,feetToEye,0)),t,fade), 0.05)
+        	fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform(playerId).rot,QuatLookAt(t, tn),fade),0.05)
+
+        	if true then
+        		local c = nextCam
+        		while c+4 > #smoothcams do
+        			c = c - #smoothcams
+        		end
+        	end
+        	SetCameraTransform(Transform(fadePos,fadeRot))
+        else
+        	if fade ~= 0 then
+        		t = cubicBezier(pointSet, subPathTimer)
+        		if subPathTimer + 0.1 >= 1 then
+        			tn = cubicBezier(nextPointSet, subPathTimer + 0.1 - 1)
+        		else
+        			tn = cubicBezier(pointSet, subPathTimer + 0.1)
+        		end
+        		fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform(playerId).pos,Vec(0,feetToEye,0)),t,fade), 0.05)
+        		fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform(playerId).rot,QuatLookAt(t, tn),fade),0.05)
+        		SetCameraTransform(Transform(fadePos,fadeRot))
+        	end
+        end
+        if(DEBUG) then
+        	DebugWatch("bezierPoints: ", #bezierPoints)
+        	DebugWatch("pathTimer: ", pathTimer)
+        	DebugWatch("pathTimer/speed: ", (pathTimer/speed))
+        	DebugWatch("subPathTimer: ", subPathTimer)
+        	DebugWatch("fade: ", fade)
+        	DebugWatch("timeInt: ", timeInt)
+        	DebugWatch("dt: ", dt)
+        	DebugWatch("subPathTimer % 0.25: ", (subPathTimer % 0.25))
+        end
+        if active or fade ~= 0 then
+        	pathTimer = pathTimer + dt
+        end
+    end
+end
+

```

---

# Migration Report: scripts\camera\smoothcamClass.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\camera\smoothcamClass.lua
+++ patched/scripts\camera\smoothcamClass.lua
@@ -1,15 +1,4 @@
-
--- emils camera script to make nice smooth floaty cameras 
-
-
-DEBUG = false
-
-
-smoothcam = {
-
-
-}
-
+#version 2
 function smoothcam:init()
 	speed = GetFloatParam("speed",5)
 	activateKey = GetStringParam("activateKey","m")
@@ -26,8 +15,8 @@
 	lastPointSet = nil
 	pointSet = {}
 	nextPointSet = {}
-	fadePos = GetPlayerTransform().pos
-	fadeRot = GetPlayerTransform().rot
+	fadePos = GetPlayerTransform(playerId).pos
+	fadeRot = GetPlayerTransform(playerId).rot
 	t = nil
 	tn = nil
 	active = false
@@ -82,8 +71,8 @@
 			fixedCamTransform = GetCameraTransform()
 			DebugPrint("active is now: true")
 			SetValue("fade",1,"cosine",3*(1-fade))
-			fadePos = VecAdd(GetPlayerTransform().pos,Vec(0,feetToEye,0))
-			fadeRot = GetPlayerTransform().rot
+			fadePos = VecAdd(GetPlayerTransform(playerId).pos,Vec(0,feetToEye,0))
+			fadeRot = GetPlayerTransform(playerId).rot
 		else
 			DebugPrint("active is now: false")
 			SetValue("fade",0,"cosine",3*fade)
@@ -125,8 +114,8 @@
 			tn = cubicBezier(pointSet, subPathTimer + 0.1)
 		end
 
-		fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform().pos,Vec(0,feetToEye,0)),t,fade), 0.05)
-		fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform().rot,QuatLookAt(t, tn),fade),0.05)
+		fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform(playerId).pos,Vec(0,feetToEye,0)),t,fade), 0.05)
+		fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform(playerId).rot,QuatLookAt(t, tn),fade),0.05)
 
 		if true then
 			local c = nextCam
@@ -136,15 +125,15 @@
 		end
 		SetCameraTransform(Transform(fadePos,fadeRot))
 	else
-		if fade > 0 then
+		if fade ~= 0 then
 			t = cubicBezier(pointSet, subPathTimer)
 			if subPathTimer + 0.1 >= 1 then
 				tn = cubicBezier(nextPointSet, subPathTimer + 0.1 - 1)
 			else
 				tn = cubicBezier(pointSet, subPathTimer + 0.1)
 			end
-			fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform().pos,Vec(0,feetToEye,0)),t,fade), 0.05)
-			fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform().rot,QuatLookAt(t, tn),fade),0.05)
+			fadePos = VecLerp(fadePos,VecLerp(VecAdd(GetPlayerTransform(playerId).pos,Vec(0,feetToEye,0)),t,fade), 0.05)
+			fadeRot = QuatSlerp(fadeRot,QuatSlerp(GetPlayerTransform(playerId).rot,QuatLookAt(t, tn),fade),0.05)
 			SetCameraTransform(Transform(fadePos,fadeRot))
 		end
 	end
@@ -158,7 +147,7 @@
 		DebugWatch("dt: ", dt)
 		DebugWatch("subPathTimer % 0.25: ", (subPathTimer % 0.25))
 	end
-	if active or fade > 0 then
+	if active or fade ~= 0 then
 		pathTimer = pathTimer + dt
 	end
 end
@@ -182,4 +171,5 @@
 	local z = (a[3] + b[3]) / 2
 	local v = Vec(x,y,z)
 	return v
-end+end
+

```

---

# Migration Report: scripts\found_secret.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\found_secret.lua
+++ patched/scripts\found_secret.lua
@@ -1,24 +1,14 @@
-
-
-
-function init()
-	trophy = FindShape("secret_trophy")
-
-
-
+#version 2
+function server.init()
+    trophy = FindShape("secret_trophy")
 end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(GetPlayerInteractShape(playerId, trophy)) then
+        	SetBool("savegame.mod.special_trophy",true, true)
 
+        end
+    end
+end
 
-
-function tick(dt)
-
-
-
-	if(GetPlayerInteractShape(trophy)) then
-		SetBool("savegame.mod.special_trophy",true)
-		
-	end
-
-
-end
```

---

# Migration Report: scripts\loadMapTst.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\loadMapTst.lua
+++ patched/scripts\loadMapTst.lua
@@ -1,155 +1,4 @@
-#include "mapNode.lua"
-#include "AStarSearch.lua"
-
-RACESTARTED = false
-map = {
-  xIndex = 0,
-  data = {
-
-  },
-
-  validSurfaceColours ={ 
-      [1] = {
-        r = 0.20,
-        g = 0.20,
-        b = 0.20,
-        range = 0.01
-      },
-    },
-}
-
--- negative grid pos is solved by simply showing 
-mapSize = {
-			x=400,
-			y=400,
-			grid = 5,
-      gridHeight = 1,
-      gridResolution = 0.5,
-      gridThres      = 0.2,
-
-      scanHeight = 100,
-
-      scanLength = 200,
-
-      weights = {
-          goodTerrain = 0.1,
-          badTerrain   = 10,
-          avoidTerrain = 25,
-          impassableTerrain = 50,
-      }
-		}
-    path = nil
-
-function init()
-  local pos = Vec(0,0,0)
-  local gridCost = 0
-  local maxVal  = {math.modf((mapSize.x)/mapSize.grid),math.modf((mapSize.y)/mapSize.grid)}
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-    pos = posToInt(Vec(0,0,y))
-    map.data[pos[3]] = {}
-    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-        pos = posToInt(Vec(x,0,y))
-        gridCost,validTerrain,avgHeight =  scanGrid(x,y) 
-        -- if(pos[3] ~= nil and pos[1]~= nil) then
-          
-          map.data[pos[3]][pos[1]] = deepcopy(mapNode) 
-          map.data[pos[3]][pos[1]]:push(x,avgHeight,y,gridCost,pos[3],pos[1],validTerrain,maxVal )
-
-        -- end
-  		  -- DebugPrint(x.." | "..y)
-    end
-	end
-	
-  --- AStar:AStarSearch(graph, start, goal)
-  pos = posToInt(GetPlayerPos())
-   goalPos = map.data[60][30]
-   startPos = map.data[55][72]
-  startPos = map.data[pos[3]][pos[1]]
- 
-  -- local cameFromIndex = cameFrom[current:getIndex()[2]][current:getIndex()[1]]:getIndex()
-end
-
-
-function scanMap( ... )
-	-- body
-end
-
-function scanGrid(x,y)
-  local pos = Vec(0,0,0)
-  local gridScore = 1
-  local spotScore = 0 
-  local hitHeight = mapSize.scanHeight
-  local heightOrigin = 1000000
-  local minHeight = heightOrigin
-  local maxHeight = -heightOrigin
-  local validTerrain  = true
-  for y1= y, y+mapSize.grid, mapSize.gridResolution do
-    for x1= x, x+mapSize.grid, mapSize.gridResolution do
-      spotScore,hitHeight,hit =  getMaterialScore3(x,y)
-      if(hitHeight == mapSize.scanHeight or IsPointInWater(Vec(x,hitHeight,y))or not hit) then
-        minHeight = -mapSize.scanLength
-        maxHeight = mapSize.scanLength
-        validTerrain = false
-      elseif(minHeight == heightOrigin or maxHeight == heightOrigin) then
-        minHeight = hitHeight
-        maxHeight = hitHeight
-      elseif(hitHeight < minHeight) then
-        minHeight = hitHeight
-      elseif(hitHeight > maxHeight) then
-        maxHeight = hitHeight
-      end
-
-      -- local hit,height,hitPos, shape = getHeight(x,y)
-      -- spotScore =  getMaterialScore2(hit,hitPos,shape)
-      gridScore = gridScore + spotScore
-
-    end
-  end
-  --DebugPrint("max: "..maxHeight.." min: "..minHeight.." sum: "..(((maxHeight - minHeight) / (mapSize.gridHeight*mapSize.gridThres)))  )  
-  if(((maxHeight - minHeight) /  (mapSize.gridHeight*mapSize.gridThres))>1) then
-    validTerrain = false
-  end  
-  if(((maxHeight) - (minHeight)) ~=0 ) then
-    gridScore = gridScore * (1+math.log(((maxHeight) - (minHeight)))*2)
-  end
-  return gridScore,validTerrain, minHeight
-end
-
-
-function tick(dt)
-  if InputPressed("r") and not RACESTARTED  then
-    RACESTARTED = true
-     cameFrom,current,path =  AStar:AStarSearch(map.data, startPos, goalPos)
-  elseif(RACESTARTED and path)then 
-    AStar:drawPath(map.data,path)
-  end
-  local playerTrans = GetPlayerTransform()
-  playerTrans.pos,pos2 = posToInt(playerTrans.pos)
-  -- DebugWatch("Player Pos: ",playerTrans.pos)
-  --  DebugWatch("original Player Pos: ", GetPlayerTransform().pos)
-   -- DebugWatch("Pos 2: ",pos2) 
-   local pos = VecCopy(playerTrans.pos)
-   if(pos[3] ~= nil and pos[1]~= nil) then
-    -- DebugPrint(pos[3].." | "..pos[1])
-     -- DebugWatch("player Grid Cost: ",map.data[pos[3]][pos[1]]:getCost())
-
-     -- DebugWatch("player Grid neighbors: ",#map.data[pos[3]][pos[1]].neighbors)
-
-     local totalCost = 0
-     for key, val in ipairs(map.data[pos[3]][pos[1]]:getNeighbors()) do
-          totalCost = totalCost + map.data[val.y][val.x]:getCost()
-     end
-
-     -- DebugWatch("player Grid neighbor: ",totalCost)
-
-     -- DebugWatch("player Grid VALID: ",map.data[pos[3]][pos[1]].validTerrain)
-  else
-
-  end
-
-  
-end
-
+#version 2
 function getHeight(x,y)
 
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -220,7 +69,6 @@
 
 end
 
-
 function getMaterialScore3(x,y)
   local score = 0
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -283,10 +131,9 @@
   return pos,pos2
 end
 
-
 function Heuristic(a, b)
       return Math.Abs(a[1] - b[1]) + Math.Abs(a[3] - b[3]);
- end 
+ end
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -303,8 +150,6 @@
     return copy
 end
 
-
-
 function inRange(min,max,value)
     if(min < value and value<=max) then 
       return true
@@ -313,4 +158,5 @@
       return false
     end
 
-end+end
+

```

---

# Migration Report: scripts\mapBuilder.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\mapBuilder.lua
+++ patched/scripts\mapBuilder.lua
@@ -1,208 +1,4 @@
-#include "mapNode.lua"
-#include "AStarSearch.lua"
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        mapBuilder.lua             
-*
-* DESCRIPTION :
-*   File that constructs the map based on scanning positions for materials
-*   Buidls a 2d array representing a weighted graph of every map location
-*   
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-*                Release Date :    29 Nov 2021 
-*
-]]
-
-
-RACESTARTED = false
-map = {
-  xIndex = 0,
-  data = {
-
-  },
-
-  validSurfaceColours ={ 
-      [1] = {
-        r = 0.20,
-        g = 0.20,
-        b = 0.20,
-        range = 0.01
-      },
-    },
-}
-
--- negative grid pos is solved by simply showing 
-mapSize = {
-			x=400,
-			y=400,
-			grid = 5,
-      gridHeight = 1,
-      gridResolution = 0.5,
-      gridThres      = 0.2,
-
-      scanHeight = 100,
-
-      scanLength = 200,
-
-      weights = {
-          goodTerrain = 0.1,
-          badTerrain   = 10,
-          avoidTerrain = 25,
-          impassableTerrain = 50,
-      }
-		}
-    path = nil
-
-function init()
-  local pos = Vec(0,0,0)
-  local gridCost = 0
-  local maxVal  = {math.modf((mapSize.x)/mapSize.grid),math.modf((mapSize.y)/mapSize.grid)}
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-    pos = posToInt(Vec(0,0,y))
-    map.data[pos[3]] = {}
-    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-        pos = posToInt(Vec(x,0,y))
-        gridCost,validTerrain,avgHeight =  scanGrid(x,y) 
-        -- if(pos[3] ~= nil and pos[1]~= nil) then
-          
-          map.data[pos[3]][pos[1]] = deepcopy(mapNode) 
-          map.data[pos[3]][pos[1]]:push(x,avgHeight,y,gridCost,pos[3],pos[1],validTerrain,maxVal )
-
-        -- end
-  		  -- DebugPrint(x.." | "..y)
-    end
-	end
-	
-
-  pos = posToInt(GetPlayerPos())
-   goalPos = map.data[60][30]
-   startPos = map.data[55][72]
-  startPos = map.data[pos[3]][pos[1]]
-
-
-
-  paths = {}
-  gateState = {}
-  gates = {}
-  triggers = FindTriggers("gate",true)
-  for i=1,#triggers do
-    gateState[tonumber(GetTagValue(triggers[i], "gate"))] = 0
-    gates[tonumber(GetTagValue(triggers[i], "gate"))] = triggers[i]
-  end
-
-  for i =1,#triggers do 
-    startPos = posToInt(GetTriggerTransform(gates[i]).pos)
-    startPos = map.data[startPos[3]][startPos[1]]
-    if(i==#triggers) then 
-      goalPos = posToInt(GetTriggerTransform(gates[1]).pos )
-    else
-      goalPos = posToInt(GetTriggerTransform(gates[i+1]).pos )
-    end
-    goalPos = map.data[goalPos[3]][goalPos[1]]
-    paths[#paths+1] =  AStar:AStarSearch(map.data, startPos, goalPos)
-  end
-
-  --- AStar:AStarSearch(graph, start, goal)
-
- 
-  -- local cameFromIndex = cameFrom[current:getIndex()[2]][current:getIndex()[1]]:getIndex()
-end
-
-
-function scanMap( ... )
-	-- body
-end
-
-function scanGrid(x,y)
-  local pos = Vec(0,0,0)
-  local gridScore = 1
-  local spotScore = 0 
-  local hitHeight = mapSize.scanHeight
-  local heightOrigin = 1000000
-  local minHeight = heightOrigin
-  local maxHeight = -heightOrigin
-  local validTerrain  = true
-  for y1= y, y+mapSize.grid, mapSize.gridResolution do
-    for x1= x, x+mapSize.grid, mapSize.gridResolution do
-      spotScore,hitHeight,hit =  getMaterialScore3(x,y)
-      if(hitHeight == mapSize.scanHeight or IsPointInWater(Vec(x,hitHeight,y))or not hit) then
-        minHeight = -mapSize.scanLength
-        maxHeight = mapSize.scanLength
-        validTerrain = false
-      elseif(minHeight == heightOrigin or maxHeight == heightOrigin) then
-        minHeight = hitHeight
-        maxHeight = hitHeight
-      elseif(hitHeight < minHeight) then
-        minHeight = hitHeight
-      elseif(hitHeight > maxHeight) then
-        maxHeight = hitHeight
-      end
-
-      -- local hit,height,hitPos, shape = getHeight(x,y)
-      -- spotScore =  getMaterialScore2(hit,hitPos,shape)
-      gridScore = gridScore + spotScore
-
-    end
-  end
-  --DebugPrint("max: "..maxHeight.." min: "..minHeight.." sum: "..(((maxHeight - minHeight) / (mapSize.gridHeight*mapSize.gridThres)))  )  
-  if(((maxHeight - minHeight) /  (mapSize.gridHeight*mapSize.gridThres))>1) then
-    validTerrain = false
-  end  
-  if(((maxHeight) - (minHeight)) ~=0 ) then
-    gridScore = gridScore * (1+math.log(((maxHeight) - (minHeight)))*2)
-  end
-  return gridScore,validTerrain, minHeight
-end
-
-
-function tick(dt)
-  if InputPressed("r") and not RACESTARTED  then
-    RACESTARTED = true
-     path =  AStar:AStarSearch(map.data, startPos, goalPos)
-  elseif(RACESTARTED and path)then 
-    -- AStar:drawPath(map.data,path)
-    DebugWatch("running",#paths)
-    for key,val in ipairs(paths) do  
-       AStar:drawPath2(map.data,val)
-    end
-  end
-  local playerTrans = GetPlayerTransform()
-  playerTrans.pos,pos2 = posToInt(playerTrans.pos)
-  -- DebugWatch("Player Pos: ",playerTrans.pos)
-  --  DebugWatch("original Player Pos: ", GetPlayerTransform().pos)
-   -- DebugWatch("Pos 2: ",pos2) 
-   local pos = VecCopy(playerTrans.pos)
-   if(pos[3] ~= nil and pos[1]~= nil) then
-    -- DebugPrint(pos[3].." | "..pos[1])
-     -- DebugWatch("player Grid Cost: ",map.data[pos[3]][pos[1]]:getCost())
-
-     -- DebugWatch("player Grid neighbors: ",#map.data[pos[3]][pos[1]].neighbors)
-
-     local totalCost = 0
-     for key, val in ipairs(map.data[pos[3]][pos[1]]:getNeighbors()) do
-          totalCost = totalCost + map.data[val.y][val.x]:getCost()
-     end
-
-     -- DebugWatch("player Grid neighbor: ",totalCost)
-
-     -- DebugWatch("player Grid VALID: ",map.data[pos[3]][pos[1]].validTerrain)
-  else
-
-  end
-
-  
-end
-
+#version 2
 function getHeight(x,y)
 
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -273,7 +69,6 @@
 
 end
 
-
 function getMaterialScore3(x,y)
   local score = 0
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -336,10 +131,9 @@
   return pos,pos2
 end
 
-
 function Heuristic(a, b)
       return Math.Abs(a[1] - b[1]) + Math.Abs(a[3] - b[3]);
- end 
+ end
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -356,8 +150,6 @@
     return copy
 end
 
-
-
 function inRange(min,max,value)
     if(min < value and value<=max) then 
       return true
@@ -366,4 +158,5 @@
       return false
     end
 
-end+end
+

```

---

# Migration Report: scripts\mapNode.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\mapNode.lua
+++ patched/scripts\mapNode.lua
@@ -1,45 +1,4 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        mapNode.lua             
-*
-* DESCRIPTION :
-*       File that implements a structure to represent map nodes and scores
-*		used for pathfinding 
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-mapNode = {
-	minID = -1,
-	secondMinID = -1,
-	MinDistance = 1000,
-	secondMinDistance = 999,
-	x = 0,
-	y = 0,
-	z = 0,
-	baseCost = 0,
-	validTerrain = false,
-	spriteColour = {1,1,0},
-	neighbors = {},
-	maxVal = {},
-	indexX = 0,
-	indexY = 0,
-
-}
-
-
-
-
+#version 2
 function mapNode:push(x,y,z,value,t_indexY,t_indexX,validTerrain,maxVal)
 	self.x, self.y, self.z, self.baseCost,self.indexX , self.indexY, self.validTerrain,self.maxVal = x,y,z,value,t_indexX,t_indexY,validTerrain,maxVal
 	-- local index = 0
@@ -67,7 +26,6 @@
 	return  {self.indexX, self.indexY}
 end
 
-
 function mapNode:Equals(node)
 	local nodeIndex = node:getIndex()
 	if(self.indexX==nodeIndex[1] and self.indexY==nodeIndex[2])  then 
@@ -77,7 +35,6 @@
 		return false
 	end
 end
-
 
 function mapNode:indexEquals(nodeIndex)
 	if(self.indexX==nodeIndex[1] and self.indexY==nodeIndex[2])  then 
@@ -91,7 +48,6 @@
 function mapNode:getDistance(altPos)
 	return VecLength(VecSub(self:getPos(),altPos))
 end
-
 
 function mapNode:computeNodeDistance(CentroidId,centroid)
 	local dist = self:getDistance(centroid:getPos())
@@ -112,10 +68,10 @@
 	self:setSecondMinID(-1)
 end
 
-
 function mapNode:loadSprite()
 	self.sprite = LoadSprite("MOD/images/dot.png")
 end
+
 function mapNode:showSprite()
 	if(not IsHandleValid(self.sprite)) then
 		DebugPrint("NO SPRITE FOUND")
@@ -128,15 +84,6 @@
 	DebugWatch("clusterPos",self:getPos())
 end
 
-
-
------
-
- ---- getters
-
------
-
-
 function mapNode:getMinDistance()
 	return self.MinDistance 
 end
@@ -145,14 +92,13 @@
 	return self.secondMinDistance
 end
 
-
 function mapNode:getMinID()
 	return self.minID 
 end
+
 function mapNode:getSecondMinID()
 	return self.secondMinID 
 end
-
 
 function mapNode:getCost()
 	return self.baseCost 
@@ -162,16 +108,9 @@
 	return self.neighbors
 end
 
---- 
-
- --- setters
-
----
-
 function mapNode:setPos(pos)
 	self.x,self.y,self.z = pos[1],pos[2],pos[3]
 end
-
 
 function mapNode:setMinDistance(dist)
 	self:setSecondMinDistance(self.MinDistance)
@@ -186,21 +125,13 @@
 	self:setSecondMinID(self.minID)
 	self.minID = id
 end
+
 function mapNode:setSecondMinID(id)
 	self.secondMinID = id
 end
 
-
-
-
----
-
-  --- helpers
-
-----
-
-
 function mapNode:clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
-end+end
+

```

---

# Migration Report: scripts\menu\camerasweep.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\menu\camerasweep.lua
+++ patched/scripts\menu\camerasweep.lua
@@ -1,60 +1,47 @@
--- Animate camera (both position and orientation) between two locataions in a given time
-
-
-pTime = GetFloatParam("time", 10)
-
-
-timeVal = 0
-
-function init()
-	locations  = FindLocations("f1_camLoc",true)
-
-	startTransform = GetLocationTransform(FindLocation("start"))
-	endTransform = GetLocationTransform(FindLocation("end"))
-	tim = 0.0
-	target =0
-	transitionTime = pTime/#locations
-
-	SetValue("timeVal", pTime-transitionTime, "cosine", pTime)
-
-
-	SetCameraTransform( GetLocationTransform(locations[2]))
-	lastTarget = -1
-	currentTarget = GetLocationTransform(locations[1])
-	nextTarget = GetLocationTransform(locations[2])	
-	lastTargetRot = Quat()
+#version 2
+function server.init()
+    locations  = FindLocations("f1_camLoc",true)
+    startTransform = GetLocationTransform(FindLocation("start"))
+    endTransform = GetLocationTransform(FindLocation("end"))
+    tim = 0.0
+    target =0
+    transitionTime = pTime/#locations
+    SetValue("timeVal", pTime-transitionTime, "cosine", pTime)
+    SetCameraTransform( GetLocationTransform(locations[2]))
+    lastTarget = -1
+    currentTarget = GetLocationTransform(locations[1])
+    nextTarget = GetLocationTransform(locations[2])	
+    lastTargetRot = Quat()
 end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local t = (timeVal%transitionTime) / transitionTime
+        local target = math.floor(timeVal/transitionTime)+1
+        local progress = timeVal%transitionTime
+        DebugWatch("t time",t)
+        DebugWatch("tiemval",(timeVal%transitionTime) )
+        DebugWatch("transitionTime",transitionTime)
+        DebugWatch("current point:",math.floor((timeVal/transitionTime)+1).." / "..#locations)
+        if(target~= lastTarget) then
+        	DebugPrint(VecStr(currentTarget.pos))
+        	lastTarget = target 
+        	currentTarget = GetLocationTransform(locations[target])
+        	DebugPrint(target.." | "..target+1)
+        	nextTarget = GetLocationTransform(locations[target+1])
+        	DebugPrint(tostring(IsHandleValid(locations[target])).." | "..tostring(IsHandleValid(locations[target+1])))
+        	lastTargetRot = QuatCopy(nextTargetRot)
+        	nextTargetRot = QuatLookAt(currentTarget.pos, nextTarget.pos)
 
-function tick(dt)
-
-	local t = (timeVal%transitionTime) / transitionTime
-	local target = math.floor(timeVal/transitionTime)+1
-	local progress = timeVal%transitionTime
-	DebugWatch("t time",t)
-	DebugWatch("tiemval",(timeVal%transitionTime) )
-	DebugWatch("transitionTime",transitionTime)
-	DebugWatch("current point:",math.floor((timeVal/transitionTime)+1).." / "..#locations)
-
-	if(target~= lastTarget) then
-		DebugPrint(VecStr(currentTarget.pos))
-		lastTarget = target 
-		currentTarget = GetLocationTransform(locations[target])
-		DebugPrint(target.." | "..target+1)
-		nextTarget = GetLocationTransform(locations[target+1])
-		DebugPrint(tostring(IsHandleValid(locations[target])).." | "..tostring(IsHandleValid(locations[target+1])))
-		lastTargetRot = QuatCopy(nextTargetRot)
-		nextTargetRot = QuatLookAt(currentTarget.pos, nextTarget.pos)
-
-	end
-	local pos = VecLerp(currentTarget.pos, nextTarget.pos, t)
-	local rot = QuatSlerp(lastTargetRot, nextTargetRot, t)
-	-- if t > 1.0 then t = 1.0 end
-	-- if()
-	-- local pos = VecLerp(startTransform.pos, endTransform.pos, t)
-	-- local rot = QuatSlerp(startTransform.rot, endTransform.rot, t)
-
-	DebugPrint(VecStr(pos))
-	SetCameraTransform(Transform(pos, rot))
+        end
+        local pos = VecLerp(currentTarget.pos, nextTarget.pos, t)
+        local rot = QuatSlerp(lastTargetRot, nextTargetRot, t)
+        -- if t > 1.0 then t = 1.0 end
+        -- if()
+        -- local pos = VecLerp(startTransform.pos, endTransform.pos, t)
+        -- local rot = QuatSlerp(startTransform.rot, endTransform.rot, t)
+        DebugPrint(VecStr(pos))
+        SetCameraTransform(Transform(pos, rot))
+    end
 end
 

```

---

# Migration Report: scripts\menu\Main_Menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\menu\Main_Menu.lua
+++ patched/scripts\menu\Main_Menu.lua
@@ -1,38 +1,4 @@
-
-#include "../trackDescriptions.lua"
-
-
-
-selectedMap = nil
-selected_map_num = nil
-STOP_THE_MUSIC = true
-selected_mode = nil
-selected_car = nil
-
-
-ui_font_s = 24
-ui_font_m = 40
-ui_font_l = 60
-
-
-function init()
-
-	camPos = FindLocation('camPos',true)
-
-	mapNames = {
-		[1] = "caveisland",
-		[2] = "frustrum",
-		[3] = "lee",
-		[4] = "mansion",
-		[5] = "marina",
-	}
-
-	menu_music = mapNames[math.random(1,#mapNames)].."-hunted.ogg"
-
-	STOP_THE_MUSIC = GetBool("savegame.mod.play_menu_music")
-
-end
-
+#version 2
 function getMapInfo(raceMap)
 	--- set custom track values
 	local map = {}
@@ -58,43 +24,6 @@
 	return map
 
 end
-
-function tick(dt)
-
-	-- DebugWatch('selectedMap', selectedMap)
-
-	-- if(GetTime()<5) then 
-	if(not STOP_THE_MUSIC)then 
-		PlayMusic(menu_music)
-	else
-		StopMusic()
-	end
---	DebugWatch("Camera valid:",	IsHandleValid(camPos))
---	DebugWatch("Camera pos:",	camPos)
-	SetCameraTransform(GetLocationTransform(camPos))
-
-end
-
-function draw()
-
-	window_width = UiWidth()
-	window_height =  UiHeight()
-	UiMakeInteractive()
-	UiModalBegin()
-
-	uiDrawBackground()
-	uiDrawTitle()
-	uiDrawMusicButtons()
-	uiDrawExitButton()
-
-	do UiPush()
-		UiTranslate(0, 300)
-		draw_menu()
-	UiPop() end
-
-	UiModalEnd()
-end
-
 
 function draw_menu()
 
@@ -312,7 +241,6 @@
 
 			UiTranslate(0,50)
 
-
 			local valid_cars = {
 				[1] = {name = "base Car", id = "base"}
 			}
@@ -347,9 +275,7 @@
 			end
 		UiPop() end
 
-
-	end
-
+	end
 
 end
 
@@ -372,7 +298,6 @@
 	local w, h = UiGetTextSize(t_text)
 	UiTranslate(0,30)
 
-
 	line = "Menu music: "
 	l_w, l_h = UiGetTextSize(line)
 	UiText(line)
@@ -380,7 +305,6 @@
 	UiButtonImageBox("ui/common/box-outline-6.png", 3, 3)
 	UiButtonHoverColor(0, 0, 1)
 
-
 	local menu_music_state = "Enabled"
 
 	-- DebugWatch("menu registry music: ",GetBool("savegame.mod.play_menu_music"))
@@ -392,11 +316,10 @@
 	l_w, l_h = UiGetTextSize(menu_music_state)
 	if UiTextButton(menu_music_state, l_w*1.5,l_h*1.5) then
 
-		SetBool("savegame.mod.play_menu_music", not GetBool("savegame.mod.play_menu_music"))
+		SetBool("savegame.mod.play_menu_music", not GetBool("savegame.mod.play_menu_music"), true)
 		STOP_THE_MUSIC = GetBool("savegame.mod.play_menu_music")
 	end	
 	UiTranslate(-w*1.5,h*2)
-
 
 	line = "Race music: "
 	l_w, l_h = UiGetTextSize(line)
@@ -405,7 +328,6 @@
 	UiButtonImageBox("ui/common/box-outline-6.png", 3, 3)
 	UiButtonHoverColor(0, 0, 1)
 
-
 	local race_music_state = "Enabled"
 
 	if(GetBool("savegame.mod.play_race_music")) then
@@ -414,7 +336,7 @@
 
 	l_w, l_h = UiGetTextSize(race_music_state)
 	if UiTextButton(race_music_state, l_w*1.5,l_h*1.5) then
-		SetBool("savegame.mod.play_race_music", not GetBool("savegame.mod.play_race_music"))
+		SetBool("savegame.mod.play_race_music", not GetBool("savegame.mod.play_race_music"), true)
 	end	
 	
 
@@ -436,9 +358,6 @@
 	StartLevel("race", "MOD/"..selectedMap..".xml", "ai3".." "..selected_mode.." "..selected_car.." playerState"..weather)
 
 end
-
-
--- ui functions
 
 function uiDrawBackground()
 	--- draw menu background
@@ -487,4 +406,50 @@
 		draw_player_name(window_width,window_height)
 
 	UiPop() end
-end+end
+
+function server.init()
+    camPos = FindLocation('camPos',true)
+    mapNames = {
+    	[1] = "caveisland",
+    	[2] = "frustrum",
+    	[3] = "lee",
+    	[4] = "mansion",
+    	[5] = "marina",
+    }
+    menu_music = mapNames[math.random(1,#mapNames)].."-hunted.ogg"
+    STOP_THE_MUSIC = GetBool("savegame.mod.play_menu_music")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        	if(not STOP_THE_MUSIC)then 
+        		PlayMusic(menu_music)
+        	else
+        		StopMusic()
+        	end
+        --	DebugWatch("Camera valid:",	IsHandleValid(camPos))
+        --	DebugWatch("Camera pos:",	camPos)
+        	SetCameraTransform(GetLocationTransform(camPos))
+    end
+end
+
+function client.draw()
+    window_width = UiWidth()
+    window_height =  UiHeight()
+    UiMakeInteractive()
+    UiModalBegin()
+
+    uiDrawBackground()
+    uiDrawTitle()
+    uiDrawMusicButtons()
+    uiDrawExitButton()
+
+    do UiPush()
+    	UiTranslate(0, 300)
+    	draw_menu()
+    UiPop() end
+
+    UiModalEnd()
+end
+

```

---

# Migration Report: scripts\names.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\names.lua
+++ patched/scripts\names.lua
@@ -1,201 +1 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        names.lua             
-*
-* DESCRIPTION :
-*       File that contains all racer names (and unique names) 
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-fNames = {
-		[1] = "Lewis",
-		[2] = "Jack",
-		[3] = "Ryan",
-		[4] = "James",
-		[5] = "Callum",
-		[6] = "Cameron",
-		[7] = "Daniel",
-		[8] = "Liam",
-		[9] = "Jamie",
-		[10] = "Kyle",
-		[11] = "Matthew",
-		[12] = "Logan",
-		[13] = "Finlay",
-		[14] = "Adam",
-		[15] = "Alexander",
-		[16] = "Dylan",
-		[17] = "Aiden",
-		[18] = "Andrew",
-		[19] = "Ben",
-		[20] = "Aaron",
-		[21] = "Connor",
-		[22] = "Thomas",
-		[23] = "Joshua",
-		[24] = "David",
-		[25] = "Ross",
-		[26] = "Luke",
-		[27] = "Nathan",
-		[28] = "Charlie",
-		[29] = "Ethan",
-		[30] = "Aidan",
-		[31] = "Michael",
-		[32] = "John",
-		[33] = "Calum",
-		[34] = "Scott",
-		[35] = "Josh",
-		[36] = "Samuel",
-		[37] = "Kieran",
-		[38] = "Fraser",
-		[39] = "William",
-		[40] = "Oliver",
-		[41] = "Rhys",
-		[42] = "Sean",
-		[43] = "Harry",
-		[44] = "Owen",
-		[45] = "Sam",
-		[46] = "Christopher",
-		[47] = "Euan",
-		[48] = "Robert",
-		[49] = "Kai",
-		[50] = "Jay",
-		[51] = "Jake",
-		[52] = "Lucas",
-		[53] = "Jayden",
-		[54] = "Tyler",
-		[55] = "Rory",
-		[56] = "Reece",
-		[57] = "Robbie",
-		[58] = "Joseph",
-		[59] = "Max",
-		[60] = "Benjamin",
-		[61] = "Ewan",
-		[62] = "Archie",
-		[63] = "Evan",
-		[64] = "Leo",
-		[65] = "Taylor",
-		[66] = "Alfie",
-		[67] = "Blair",
-		[68] = "Arran",
-		[69] = "Leon",
-		[70] = "Angus",
-		[71] = "Craig",
-		[72] = "Murray",
-		[73] = "Declan",
-		[74] = "Zak",
-		[75] = "Brandon",
-		[76] = "Harris",
-		[77] = "Finn",
-		[78] = "Lee",
-		[79] = "Lennon",
-		[80] = "Cole",
-		[81] = "George",
-		[82] = "Jacob",
-		[83] = "Mark",
-		[84] = "Hayden",
-		[85] = "Kenzie",
-		[86] = "Alex",
-		[87] = "Shaun",
-		[88] = "Louis",
-		[89] = "Caleb",
-		[90] = "Mason",
-		[91] = "Gregor",
-		[92] = "Mohammed",
-		[93] = "Luca",
-		[94] = "Harrison",
-		[95] = "Kian",
-		[96] = "Noah",
-		[97] = "Paul",
-		[98] = "Riley",
-		[99] = "Stuart",
-		[100] = "Joe",
-		[101] = "Jonathan",
-		[102] = "Stephen",
-
-}
-
-
-sNames = {
-[1] = "Smith",
-[2] = "Brown",
-[3] = "Wilson",
-[4] = "Stewart",
-[5] = "Thomson",
-[6] = "Robertson",
-[7] = "Campbell",
-[8] = "Anderson",
-[9] = "Murray",
-[10] = "Macdonald",
-[11] = "Taylor",
-[12] = "Scott",
-[13] = "Reid",
-[14] = "Clark",
-[15] = "Hamilton",
-[16] = "Morrison",
-[17] = "Walker",
-[18] = "Ross",
-[19] = "Watson",
-[20] = "Graham",
-[21] = "Fraser",
-[22] = "Young",
-[23] = "Hill",
-[24] = "Simpson",
-[25] = "Hunter",
-[26] = "Ferguson",
-[27] = "Douglas",
-[28] = "King",
-[29] = "Findlay",
-[30] = "Jamieson",
-[31] = "Macleod",
-[32] = "White Cresta",
-[33] = "Burns",
-[34] = "Kennedy",
-[35] = "Mckenzie",
-[36] = "Sutherland",
-[37] = "Wood",
-[38] = "Hughes",
-[39] = "Mcmillan",
-[40] = "Cunningham",
-[41] = "Boyle",
-[42] = "Gibson",
-[43] = "Gibson",
-}
-
-
-
-
-uniqueNames = {
-	[1] = 	"Dennis Gustafsson",
-	[2] =  	"Resident Emil",
-	[3] =	"Gordon Woo",
-	[4] =	"Lawrence Lee Jr.",
-	[5] =	"Gillian Johnson",
-	[6] =	"Tracy",
-	[7] =	"Parisa Terdiman",
-	[8] = "Elboydo",
-	[9] = "Spexta",
-	[10] = "Dima",
-	[11] = "Mafia",
-	[12] = "Anton Wolfe",
-	[13] = "iaobardar",
-	[14] = "Rubikow",
-	[15] = "PPAN",
-	[16] = "YuLun",
-	[17] = "ONSVRG",
-	[18] = "Larry Walsh",
-	[19] = "CoolJWB",
-
-
-
-
-}+#version 2

```

---

# Migration Report: scripts\node.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\node.lua
+++ patched/scripts\node.lua
@@ -1,47 +1,4 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        node.lua             
-*
-* DESCRIPTION :
-*       File that implements a node type structure for use in GNG/SNN networks 
-*		
-
-*
-* NOTES :
-* 
-* This was a rough implementation, I wouldn't put too much stock in it.  
-* makes for a cool experiment though.      
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-node = {
-	minID = -1,
-	secondMinID = -1,
-	MinDistance = 1000,
-	secondMinDistance = 999,
-	x = 0,
-	y = 0,
-	z = 0,
-	value = 0,
-	spriteColour = {1,1,0},
-	GNconnect = Vec(0,0,0),
-	GNnumber = 0,
-	SNNpulse = 0,
-	SNNstate = 0,
-	SNNSum = 0,
-	SNNNum = 0,
-	threshold = 0.6,
-	outputthreshold=0.2,
-	SNNpsp    = 0 
-
-}
-
+#version 2
 function node:push(x,y,z,value)
 	self.x, self.y, self.z, self.value = x,y,z,value
 end
@@ -105,7 +62,6 @@
 	self.SNNNum = 0
 end
 
-
 function node:computeNodeDistance(CentroidId,centroid)
 	local dist = self:getDistance(centroid:getPos())
 	if(dist<self.MinDistance) then
@@ -136,6 +92,7 @@
 function node:loadSprite()
 	self.sprite = LoadSprite("MOD/images/dot.png")
 end
+
 function node:showSprite()
 	if(not IsHandleValid(self.sprite)) then
 		DebugPrint("NO SPRITE FOUND")
@@ -148,15 +105,6 @@
 	DebugWatch("clusterPos",self:getPos())
 end
 
-
-
------
-
- ---- getters
-
------
-
-
 function node:getMinDistance()
 	return self.MinDistance 
 end
@@ -165,25 +113,17 @@
 	return self.secondMinDistance
 end
 
-
 function node:getMinID()
 	return self.minID 
 end
+
 function node:getSecondMinID()
 	return self.secondMinID 
 end
 
-
---- 
-
- --- setters
-
----
-
 function node:setPos(pos)
 	self.x,self.y,self.z = pos[1],pos[2],pos[3]
 end
-
 
 function node:setMinDistance(dist)
 	self:setSecondMinDistance(self.MinDistance)
@@ -198,21 +138,13 @@
 	self:setSecondMinID(self.minID)
 	self.minID = id
 end
+
 function node:setSecondMinID(id)
 	self.secondMinID = id
 end
 
-
-
-
----
-
-  --- helpers
-
-----
-
-
 function node:clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
-end+end
+

```

---

# Migration Report: scripts\PriorityQueue.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\PriorityQueue.lua
+++ patched/scripts\PriorityQueue.lua
@@ -1,34 +1,4 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        PriorityQeue.lua             
-*
-* DESCRIPTION :
-*       File that implements a priority queue data structure in lua. 
-* 		used for pathfinding in teardown 
-*		
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-
-PriorityQueue = {
-	queuelength = 0,
-	currentIndex = 0,
-	queueSize = 0,
-	elements = {
-
-	},
-}
-
-
+#version 2
 function PriorityQueue:init(x,y) 
 	local maxElements = (x)*(y)
 	for i=1, maxElements do
@@ -52,7 +22,6 @@
 	return true
 
 end
-
 
 function PriorityQueue:put(node,cost) 
 	
@@ -100,3 +69,4 @@
 	end
 
 end
+

```

---

# Migration Report: scripts\race_Manager.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\race_Manager.lua
+++ patched/scripts\race_Manager.lua
@@ -1,117 +1,9 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        race_Manager.lua             
-*
-* DESCRIPTION :
-*       File that manages racing game mode events, positions, and timings. 
-*		alongside hud elements and win / lose states
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-
-raceManager = {
-	raceStarted = false,
-	startTime = 0,
-	raceWon = false,
-	checkpoints = {},
-	path = {},
-	laps =1,
-	positionsUpdateTime = 0.100,
-	currentUpdateTime = 0,
-	positions = {
-
-	},
-	racers = {
-
-	},
-	preCountdown = 5,
-	countdown = 4,
-
-	defaultDisplayRange = 40,
-	maxDisplayRange = 4000,
-	displayRange = 40,
-
-
-
-
-	cameraControlTag = "cameraController",
-	cameraKeyword = "panCam" ,
-
-
-	preRaceCam = {
-		startCam = {x = 0,y = 1,z = -1},
-
-
-
-
-	},
-
-	font =	 "MOD/fonts/nk57-monospace.bold.ttf",
-
-
-	raceMusic = "MOD/sounds/caveisland-hunted.ogg",
-
-	mapNames = {
-		[1] = "caveisland",
-		[2] = "frustrum",
-		[3] = "lee",
-		[4] = "mansion",
-		[5] = "marina",
-
-
-
-
-	}
-
-}
-
-	
-
-	startPan = 0
-
-	xPanMax = 1
-	xPanMin = -1
-
-	yPanMax = 2.0
-	yPanMin = 0.5
-
-	zPanMax = 1
-	zPanMin = -1
-
-	camXPan = xPanMax
-	camYPan = yPanMax
-	camZPan = zPanMax
-
-
-	xtimerMin = 100
-	xtimerMax = 500
-	ytimerMin = 100
-	ytimerMax = 500
-	ztimerMin = 300
-	ztimerMax = 3000
-
-
-	cameraTargetVehicle = 1
-
-
+#version 2
 function raceManager:init(racers,path)
 	----- MORE DRIVE TO SURVIVE stuff
 
 	self.raceMusic = self.mapNames[math.random(1,#self.mapNames)].."-hunted.ogg"
 
-
-
 	self.laps = self.laps -1
 
 	self.sndWin = LoadSound("MOD/sounds/win.ogg")
@@ -119,11 +11,8 @@
 	self.sndFail = LoadSound("MOD/sounds/fail.ogg")
 	---------
 
-
 	self.cameraController = FindLocation(self.cameraControlTag,true)
 	self.lastCamKeyword = "nil"
-
-
 
 	self.path = path
 	for key,val in ipairs(racers) do 
@@ -134,8 +23,6 @@
 
 	self.currentUpdateTime = self.positionsUpdateTime
 
-
-
 		--- stuff for race prep and sounds and stuff
 
 	self.startTimerInt = math.floor(self.countdown)
@@ -150,18 +37,15 @@
 		self.trackType = "default"
 	end
 
-
 end
 
 function raceManager:startRace()
 	self.startTime = GetTime()
 end
 
-
 function raceManager:lapTime()
 	return GetTime() -  self.startTime 
 end
-
 
 function raceManager:cameraControl()
 	local currentKeyword = GetTagValue(self.cameraController, self.cameraControlTag) 
@@ -173,7 +57,6 @@
 		SetTag(self.cameraController,self.cameraControlTag,"raceStarted") 
 	end
 end
-
 
 function raceManager:raceCountdown()
 	if(self.preCountdown >0 ) then
@@ -205,10 +88,6 @@
 	end 
 end
 
-
-
---- handle player split times and lap tims - must use triggers instead of default optimal points
-
 function raceManager:playerHandler()
  	if (not playerConfig.finished and aiVehicles[playerConfig.car].raceValues.laps > self.laps) then
  		playerConfig.finished = true
@@ -217,10 +96,10 @@
  		RACEENDED = true
  		playerConfig.finalTime = self:lapTime()
  		if(playerConfig.finalTime < savedBest)then
- 			SetFloat("savegame.mod.besttime."..raceMap.."."..self.trackType.."." .. GetTagValue(roundCar,"trackinfo"),playerConfig.finalTime)
+ 			SetFloat("savegame.mod.besttime."..raceMap.."."..self.trackType.."." .. GetTagValue(roundCar,"trackinfo"),playerConfig.finalTime, true)
  		end
  		if(not bestLap or  playerConfig.bestLap < bestLap) then
-			SetFloat("savegame.mod.bestLap."..raceMap.."."..self.trackType.."." .. GetTagValue(roundCar,"trackinfo"),playerConfig.bestLap)
+			SetFloat("savegame.mod.bestLap."..raceMap.."."..self.trackType.."." .. GetTagValue(roundCar,"trackinfo"),playerConfig.bestLap, true)
  		end 
  	elseif( not playerConfig.finished and GetVehicleHealth(aiVehicles[playerConfig.car].id)<=0.05 ) then
  		playerConfig.finished = true
@@ -229,15 +108,7 @@
  		PLAYER_TOTALED = true 	
  		RACEENDED = true	
  	end
- end 
-
-	-- if(PLAYERRACING) then 
-	-- 	if(raceManager.countdown > 0 and  raceManager.preCountdown <=0 ) then
-	-- 		raceManager:StartCamPos()
-	-- 	end
-
-	-- end
-
+ end
 
 function raceManager:cameraManager()
 
@@ -255,12 +126,9 @@
 
 	local car = self.positions[cameraTargetVehicle].car
 
-
-
 	self:cameraOperator(car)
 	-- body
 end
-
 
 function raceManager:cameraOperator(car)
 	local leadCar = self.racers[car]
@@ -308,7 +176,6 @@
 	-- local height = self.bodyZSize /4
 end
 
-
 function raceManager:StartCamPos(countdown)
 	local leadCar = aiVehicles[playerConfig.car]
 	local vehicleTransform = GetVehicleTransform(aiVehicles[playerConfig.car].id)
@@ -319,7 +186,6 @@
 	-- local camRot = QuatLookAt(camPos,vehicleTransform.pos)
 	
 	-- SetCameraTransform(Transform(camPos,camRot))
-
 
 end
 
@@ -381,8 +247,6 @@
 	end
 end
 
-
-
 function raceManager:raceGates()
 
 	-- ###################################
@@ -393,7 +257,7 @@
 
 	inTrigger = 0
 	if not gameOver and not gameWin then
-		--if v > 0 then
+		--if v ~= 0 then
 			for i=1,#triggers do
 				if IsVehicleInTrigger(triggers[i], v) or IsVehicleInTrigger(triggers[i], startCar) then
 					if gateState[i] == 0 then
@@ -445,12 +309,10 @@
 	end
 end
 
-
 function raceManager:round(num, numDecimalPlaces)
   local mult = 10^(numDecimalPlaces or 0)
   return math.floor(num * mult + 0.5) / mult
 end
-
 
 function raceManager:formatTime(time)
 	minutes = math.floor(time/60)
@@ -465,11 +327,9 @@
 	return minutes..":"..seconds
 end
 
-
 function raceManager:draw()
 
 		-- DebugPrint(#self.positions)
-
 
 		if PLAYERRACING and (not RACESTARTED or playerConfig.finished) then
 			UiMakeInteractive()
@@ -486,7 +346,6 @@
 		-- 	self:displayPlayerPos()
 
 		-- end
-
 
 		UiAlign("top left")
 
@@ -532,7 +391,6 @@
 				UiColor(0,1,0)
 			end
 
-
 				
 			-- info[#info+1] = {key, self.racers[val.car].driverName,val.car}
 			-- DebugPrint(val.car.." | "..self.racers[val.car].driverName.." | "..key)
@@ -542,11 +400,9 @@
 				-- DebugPrint(string.sub(self.racers[val.car].driverFName, 1, 1))
 				func =   string.sub(self.racers[val.car].driverFName, 1, 1).."."..self.racers[val.car].driverSName
 
-
 			elseif(self.racers[val.car].playerName) then
 				func = self.racers[val.car].playerName
 			end
-
 
 			local driverNum = val.car
 			UiFont("bold.ttf", 22)
@@ -568,7 +424,6 @@
 			if(	 self.racers[val.car].raceValues.bestLap ) then
 				lapTime = self.racers[val.car].raceValues.bestLap 
 
-
 			elseif(RACESTARTED) then
 
 				lapTime= self:lapTime()
@@ -576,7 +431,6 @@
 			end
 			UiText(" | "..self:formatTime(lapTime))
 			UiTranslate(-dedentOffset, 22)
-
 
 			-- UiTranslate(10, 0)
 			-- UiFont("regular.ttf", 22)
@@ -586,8 +440,6 @@
 			-- UiTranslate(-10, 22)
 		end
 		UiPop()
-
-
 
 		-- info = {}
 		-- for key,val in ipairs(self.positions) do
@@ -627,8 +479,6 @@
 
 end
 
-
-
 function raceManager:displayPlayerPos(customSize)
 	local offset = {x = 100, y = 50}
 	local textSize = 64
@@ -640,14 +490,12 @@
 	UiFont("bold.ttf", textSize )
 
 	-- UiTranslate(0,yOffset)
-
 
 	for key,val in ipairs(self.positions) do
 			
 		if(self.racers[val.car].id == self.racers[playerConfig.car].id) then
 			
 			local position = self:ordinal_numbers(tostring(key))
-
 
 			UiTranslate(offset.x,0)
 			UiAlign("right middle")
@@ -666,9 +514,7 @@
 		end 
 	end
 
-
-end
-
+end
 
 function raceManager:ordinal_numbers(n)
 	local ordinal, digit = {"st", "nd", "rd"}, string.sub(n, -1)
@@ -696,7 +542,6 @@
 
 end
 
-
 function raceManager:setDisplayRange()
 	if(self.displayRange == self.maxDisplayRange) then
 		self.displayRange = self.defaultDisplayRange
@@ -706,11 +551,9 @@
 	end
 end
 
--- if possible plot an ai drviers name and number above their car if within range
 function raceManager:driverNameDisplay()
 	local displayRange = self.defaultDisplayRange
 
-
 	local uiScaleFactor = 0.6
 
 	local rectScale = 30
@@ -720,7 +563,6 @@
 
 	local namePlacardW = 170
 	local namePlacardH = 30
-
 
 	local letterSize = 11.8
 
@@ -740,8 +582,6 @@
 		pushVals = 0
 		local Car = nil
 
-
-
 		for Poskey,Posval in ipairs(self.positions) do
 			val = self.racers[Posval.car]
 			if(not PLAYERRACING or  ( 
@@ -760,11 +600,9 @@
 					-- UiTranslate(UiCenter(), UiMiddle())
 					UiPush()
 
-
-
 						local x, y, dist = UiWorldToPixel(vehicleTransform.pos)
 							
-						if dist > 0 then
+						if dist ~= 0 then
 
 							local func = val.driverName
 			
@@ -772,11 +610,9 @@
 								-- DebugPrint(string.sub(self.racers[val.car].driverFName, 1, 1))
 								func =   string.sub(val.driverFName, 1, 1).."."..val.driverSName
 
-
 							elseif(val.playerName) then
 								func = val.playerName
 							end
-
 
 							local driverNum = val.car
 
@@ -841,18 +677,14 @@
 		end
 	UiPop()
 
-
-
-
 	-- local x, y, dist = UiWorldToPixel(point)
-	-- if dist > 0 then
+	-- if dist ~= 0 then
 	-- 	UiTranslate(x, y)
 	-- 	UiText("Label")
 	-- end	
 
 	-- body
 end
-
 
 function raceManager:drawIntro()
 	UiPush()
@@ -913,8 +745,9 @@
 
 end
 
-
-function raceManager:drawStart()
+fu
+
+ion raceManager:drawStart()
 	UiPush()
 		UiTranslate(UiWidth()/2, UiHeight()/2)
 		UiAlign("center middle")
@@ -931,17 +764,17 @@
 	UiPop()
 end
 
-
-function raceManager:raceStats()
+fu
+
+ion raceManager:raceStats()
 	UiPush()
 
-
-
 	UiPop()
 end
 
-
-function raceManager:playerRaceStats(vehicle)
+fu
+
+ion raceManager:playerRaceStats(vehicle)
 	local offset = {x = 100, y = 70}
 	local textSize = 64
 	local infoTextSize = 24
@@ -970,7 +803,9 @@
 	UiPop()
 end
 
-function raceManager:drawPlayerLaptimeInfo(vehicle, cfg,textSize)
+fun
+
+ion raceManager:drawPlayerLaptimeInfo(vehicle, cfg,textSize)
 	local time = 0
 	local yOffset = 30
 	local xOffset = 0
@@ -1002,15 +837,11 @@
 			time =	self:formatTime(time)
 		end
 
-
 		UiAlign("right middle")
 		UiText(val.name.."|")
 
 		UiTranslate(xOffset,0)
 
-
-
-
 		UiAlign("left middle")
 
 		UiText(time)
@@ -1018,9 +849,9 @@
 	end
 end
 
-
-
-function raceManager:endScreen(vehicle)
+f
+
+ion raceManager:endScreen(vehicle)
 	local offset = {x = 200,y = UiHeight()/3}
 	local textSize = 128
 	local infoTextSize = 64
@@ -1036,22 +867,17 @@
 
 			Draw previous best time and inform player if new best lap is better
 
-
 			[3] = {
 				name = "Best",
 				time = 0,
 			},
 		]]
 
-
-
 		endGameInfo = {
 			[1] =  deepcopy(playerConfig.hudInfo.lapInfo[1]),
 			[2] =  deepcopy(playerConfig.hudInfo.lapInfo[3]),
 
 		}
-
-
 
 		local recordText = "Record Time : "
 		local recordTime = savedBest
@@ -1077,7 +903,6 @@
 		UiAlign("left middle")
 		UiText(recordTime)
 		UiTranslate(0,infoTextSize)
-
 
 		raceManager:drawPlayerLaptimeInfo(vehicle, endGameInfo,infoTextSize)
 --		UiTranslate(UiCenter(),UiMiddle())
@@ -1091,4 +916,5 @@
 		end
 
 	UiPop()
-end+end
+

```

---

# Migration Report: scripts\skiMode.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\skiMode.lua
+++ patched/scripts\skiMode.lua
@@ -1,80 +1,50 @@
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        skiMode.lua             
-*
-* DESCRIPTION :
-*       File made by Rav mahov For something super secret.
-*		
-*
-* NOTES :
-*       
-*
-* AUTHOR :    Rav Mahov        START DATE   :    N/A
-* 							 Release Date :    N/A 
-*
-]]
-
-SKI_MODE = false
-TARGET_ANGLE  =45
-
-
-leftThrust = Vec(-7.5, -1.5 ,0)
-
-rightThrust = Vec(14, 200 ,0)
-
-
-bodyMass  = 0
-imp = Vec(0,250,0)
-
-function init( )
-	
-	vehicle = FindVehicle("cfg")
-	body = GetVehicleBody(vehicle)
-	shapes = GetBodyShapes(body)
-
-	bodyMass =  GetBodyMass(body)
-	imp[2] = bodyMass
+#version 2
+function server.init()
+    vehicle = FindVehicle("cfg")
+    body = GetVehicleBody(vehicle)
+    shapes = GetBodyShapes(body)
+    bodyMass =  GetBodyMass(body)
+    imp[2] = bodyMass
 end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        bodyMass =  GetBodyMass(body)/100
+        imp[2] = bodyMass
+        DebugWatch("bodymass ",bodyMass)
+        local min, max = GetBodyBounds(body)
+        local boundsSize = VecSub(max, min)
+        DebugWatch("bounds",boundsSize)
+        if SKI_MODE then 
+        	targetAngle = (math.sin(math.rad(70)) * ((-7.5)))
+        	local rightWheelBase = TransformToParentPoint(GetVehicleTransform(vehicle),rightThrust)
 
-function tick()
-	bodyMass =  GetBodyMass(body)/100
-	imp[2] = bodyMass
+        	local leftWheelBase = TransformToParentPoint(GetVehicleTransform(vehicle),leftThrust)
+        	DebugWatch("targetAngle",targetAngle)
 
-	DebugWatch("bodymass ",bodyMass)
-	local min, max = GetBodyBounds(body)
-	local boundsSize = VecSub(max, min)
-	DebugWatch("bounds",boundsSize)
-	if InputPressed("g") then
-		if(not SKI_MODE) then 
-			ApplyBodyImpulse(body, leftWheelBase,VecScale(imp,-1.5))
-		end
+        	DebugWatch("left wheel base ",leftWheelBase)
+        	DebugWatch("right wheel base",rightWheelBase)
+        	DebugWatch("current pos",VecSub(rightWheelBase,leftWheelBase)[2])
+        	if((VecSub(leftWheelBase, rightWheelBase)[2])<targetAngle) then
+        		ApplyBodyImpulse(body, leftWheelBase,VecScale(imp,1.2))
+        		DebugWatch("applying impulse up",imp)
+        	else
+        		ApplyBodyImpulse(body, leftWheelBase,VecScale(imp,-1.2))
+        		DebugWatch("applying impulse down",VecScale(imp,-1))
+        	end
+        end
+    end
+end
 
-		SKI_MODE = not SKI_MODE
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("g") then
+    	if(not SKI_MODE) then 
+    		ApplyBodyImpulse(body, leftWheelBase,VecScale(imp,-1.5))
+    	end
 
-	end
+    	SKI_MODE = not SKI_MODE
 
+    end
+end
 
-	if SKI_MODE then 
-		targetAngle = (math.sin(math.rad(70)) * ((-7.5)))
-		local rightWheelBase = TransformToParentPoint(GetVehicleTransform(vehicle),rightThrust)
-
-		local leftWheelBase = TransformToParentPoint(GetVehicleTransform(vehicle),leftThrust)
-		DebugWatch("targetAngle",targetAngle)
-
-		DebugWatch("left wheel base ",leftWheelBase)
-		DebugWatch("right wheel base",rightWheelBase)
-		DebugWatch("current pos",VecSub(rightWheelBase,leftWheelBase)[2])
-		if((VecSub(leftWheelBase, rightWheelBase)[2])<targetAngle) then
-			ApplyBodyImpulse(body, leftWheelBase,VecScale(imp,1.2))
-			DebugWatch("applying impulse up",imp)
-		else
-			ApplyBodyImpulse(body, leftWheelBase,VecScale(imp,-1.2))
-			DebugWatch("applying impulse down",VecScale(imp,-1))
-		end
-	end
-end
```

---

# Migration Report: scripts\tests\gridlines.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\tests\gridlines.lua
+++ patched/scripts\tests\gridlines.lua
@@ -0,0 +1 @@
+#version 2

```

---

# Migration Report: scripts\trackDescriptions.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\trackDescriptions.lua
+++ patched/scripts\trackDescriptions.lua
@@ -1,412 +1 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        TrackDescriptions.lua             
-*
-* DESCRIPTION :
-*       File that holds all track descriptions and behaviors
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-trackDescriptions = {
-
-	teardownRacing = {
-			name = "Teardown Touring Cars",
-					lines = {
-							[1] = [[Teardown Touring Cars is the latest series of 
-							high octane entertainment, powered by elboydos AVF_AI]],
-							
-							[2] = [[Cars will be able to race at high speed around almost any given track 
-							]],
-							[3] = [[HAVE FUN! :)]],
-							},
-
-					trackLaps = 3,
-
-
-
-	  validMaterials = {
-	  	[1] = {	
-	  		material = "masonry",
-
-
-		  validSurfaceColours ={ 
-					[1] = {
-						r = 0.20,
-						g = 0.20,
-						b = 0.20,
-						range = 0.02
-					},
-					[2] = {
-						r = 0.80,
-						g = 0.60,
-						b = 0.60,
-						range = 0.02
-					},
-					[3] = {
-						r = 0.34,
-						g = 0.34,
-						b = 0.34,
-						range = 0.02
-					},
-				},
-			},
-		},
-
-	},
-
-	figureEight = {
-			name = "Lockelle Speedway",
-					lines = {
-							[1] = [[Lockelles finest crash filled figure 8 speedway!, powered by elboydos AVF_AI]],
-							
-							[2] = [[Cars will be able to race at high speed around almost any given track 
-							]],
-							[3] = [[HAVE FUN! :)]],
-							},
-
-					trackLaps = 6,
-			grid = 3,
-
-	  validMaterials = {
-	  	[1] = {	
-	  		material = "masonry",
-
-
-		  validSurfaceColours ={ 
-					[1] = {
-						r = 0.20,
-						g = 0.20,
-						b = 0.20,
-						range = 0.02
-					},
-					[2] = {
-						r = 0.80,
-						g = 0.60,
-						b = 0.60,
-						range = 0.02
-					},
-					[3] = {
-						r = 0.34,
-						g = 0.34,
-						b = 0.34,
-						range = 0.02
-					},
-				},
-			},
-		},
-
-	},
-
-
-	Norrbotten_raceway = {
-			name = "Norrbotten Hills Raceway",
-					lines = {
-							[1] = [[
-								Norrbotten Hills Raceway has over 50 years of motorsport history
-								 and is the fastest quarter-mile oval in Europe,
-							]],
-							
-							[2] = [[With the speeds many cars achieve around its fearsome steeply banked turns really having to be seen to be believed!  
-							]],
-							},
-
-					valid_cars = {
-						[1] = {name = "Bangers", id="ai3_bangers", unlocked=true},
-						[2] = {name = "Sprint Cars ", id="ai3_sprintCar", unlocked=true},
-						[3] = {name = "Blue Tide BT9", id="ai3_f1", unlocked=true},
-						[4] = {name = "Crownzygot XVC-alpha",id="ai3_raceCar",unlocked=true},
-						[5] = {name = "Eurus IV XXF",id="ai3_sportsCar",unlocked=true},
-						[6] = {name = "Bulletproof Bomb",id="ai3_wacky", unlocked=false,condition={[1]="indy_1_2"}},
-						[7] = {name = "Super Emil Racer", id= "ai3_emil", unlocked=false, condition = {[1]="f1_1_2",[2]="indy_1_2"}},
-					},
-
-
-					modes = {
-						[1] = {name = "Oval Circuit", id="oval"},
-
-					},
-
-
-					trackLaps = 4,
-			grid = 2,
-			completionRange = 13,
-
-	  validMaterials = {
-	  	[1] = {	
-	  		material = "masonry",
-
-
-		  validSurfaceColours ={ 
-					[1] = {
-						r = 0.20,
-						g = 0.20,
-						b = 0.20,
-						range = 0.02
-					},
-					[2] = {
-						r = 0.80,
-						g = 0.60,
-						b = 0.60,
-						range = 0.02
-					},
-					[3] = {
-						r = 0.34,
-						g = 0.34,
-						b = 0.34,
-						range = 0.02
-					},
-				},
-			},
-		},
-
-	},
-
-	skogsEntrada = {
-					name = "Löckelle: Skogs Entrada",
-					lines = {
-							[1] = "Löckelle's oldest race track. In it's history, it been the site of 12 runnings of the Löckelle Grand Prix between 1964 and 1986 and currently hosts many regional and International racing events.",
-							[2] = "Gordon Woo is said to have first raced on this track as a child, and has been a long term investor, saving it from closure after the incident of 1992...",
-							[3] = "Today you will race the track and perhaps it may make your fame..."
-							},
-
-
-
-					valid_cars = {
-						[1] = {name = "Blue Tide BT9", id="ai3_f1", unlocked=true},
-						[2] = {name = "Crownzygot XVC-alpha",id="ai3_raceCar",unlocked=true},
-						[3] = {name = "Eurus IV XXF",id="ai3_sportsCar",unlocked=true},
-						[4] = {name = "Bangers", id="ai3_bangers", unlocked=true},
-						[5] = {name = "Bulletproof Bomb",id="ai3_wacky", unlocked=true,condition={[1]="indy_1_2"}},
-						[6] = {name = "Super Emil Racer", id= "ai3_emil", unlocked=false, condition = {[1]="f1_1_2",[2]="indy_1_2"}},
-					},
-
-
-					modes = {
-						[1] = {name = "F1", id="f1"},
-						[2] = {name = "Indy Car", id="indyCircuit"}
-
-					},
-
-					trackLaps = 4,
-
-					validMaterials = {
-						[1] = {	
-							material = "masonry",
-
-
-					  validSurfaceColours ={ 
-								[1] = {
-									r = 0.20,
-									g = 0.20,
-									b = 0.20,
-									range = 0.02
-								},	
-								[2] = {
-									r = 0.80,
-									g = 0.60,
-									b = 0.60,
-									range = 0.02
-								},
-								[3] = {
-									r = 0.34,
-									g = 0.34,
-									b = 0.34,
-									range = 0.02
-								},
-							},
-						},
-					},
-
-	},
-
-
-
-
-	BlueTideRing = {
-					name = "Löckelle: Blue Tide Ring",
-					lines = {
-							[1] = [[Created By Blue Tide as a means to build cars capable of defeating Gordon Woo]],
-							[2] = [[This has been the founding of many promising young drivers, the Central Narwell considered a symbol of great luck]],
-							[3] = [[Filled with many tight corners and fast straights, "At that speed, it's so dangerous man!"]]
-							},
-
-					grid = 4,
-
-					completionRange = 5,
-
-					trackLaps = 4,
-
-
-
-					valid_cars = {
-						[1] = {name = "Blue Tide BT9", id="ai3_f1", unlocked=true},
-						[2] = {name = "Crownzygot XVC-alpha",id="ai3_raceCar",unlocked=true},
-						[3] = {name = "Eurus IV XXF",id="ai3_sportsCar",unlocked=true},
-						[4] = {name = "Bangers", id="ai3_bangers", unlocked=true},
-						[5] = {name = "Bulletproof Bomb",id="ai3_wacky", unlocked=false,condition={[1]="indy_1_2"}},
-						[6] = {name = "Super Emil Racer", id= "ai3_emil", unlocked=false, condition = {[1]="f1_1_2",[2]="indy_1_2"}},
-					},
-					modes = {
-						[1] = {name = "F1", id="f1"},
-						[2] = {name = "Indy Car", id="indyCircuit"}
-
-					},
-
-
-					validMaterials = {
-						[1] = {	
-							material = "masonry",
-
-
-					  validSurfaceColours ={ 
-								[1] = {
-									r = 0.20,
-									g = 0.20,
-									b = 0.20,
-									range = 0.02
-								},	
-								[2] = {
-									r = 0.80,
-									g = 0.60,
-									b = 0.60,
-									range = 0.02
-								},
-								[3] = {
-									r = 0.34,
-									g = 0.34,
-									b = 0.34,
-									range = 0.02
-								},
-							},
-						},
-					},
-
-	},
-
-	korsikanskElv = {
-		name = "Korsikansk Elv"
-
-
-
-	},
-
-	korpikselvanBellopete = {
-		name = "Korpikselvan bellopete "
-
-	},
-
-	kullgruveKanal = {
-		name = "Kullgruve Kanál"
-	},
-	--- thank you mr floppy jack
-	usfvenChauffuse = {
-		name = "Usfven Chauffuse"
-
-	} ,
-
-	moriSawa = {
-		name = "Mori Sawa",
-					lines = {
-							[1] = [[Founded in an old Lockelle Army airstrip, Motorsport has found a new home ]],
-							[2] = [[With a large stipend from BlueTide Corperation, this year lockelle welcomes the rallycross world tour]],
-							[3] = [[We hope you've tested your suspension, as things are about to get bumpy!]]
-							},
-
-
-
-					trackLaps = 4,
-
-					valid_cars = {
-						[1] = {name = "Rally Cross (mixed)", id="rallycross",unlocked=true},
-					},
-					modes = {
-						[1] = {name="RallyCross", id = "rallycross"},
-
-					},
-					
-					validMaterials = {
-						[1] = {	
-							material = "masonry",
-
-
-					  validSurfaceColours ={ 
-								[1] = {
-									r = 0.20,
-									g = 0.20,
-									b = 0.20,
-									range = 0.02
-								},	
-								[2] = {
-									r = 0.80,
-									g = 0.60,
-									b = 0.60,
-									range = 0.02
-								},
-								[3] = {
-									r = 0.34,
-									g = 0.34,
-									b = 0.34,
-									range = 0.02
-								},
-								[4] = {
-									r = 0.30,
-									g = 0.30,
-									b = 0.30,
-									range = 0.02
-								},
-							},
-						},
-						[2] = {	
-							material = "dirt",
-
-
-					  validSurfaceColours ={ 
-								[1] = {
-									r = 0.66,
-									g = 0.56,
-									b = 0.42,
-									range = 0.02
-								},	
-							},
-						},
-					},
-
-	}
-
-
-} 
-
-
-unlockConditions = {
-
-	indy_1_2 = {
-		info = "Beat the indy car world record on Skogs entrada and Blue tide ring",
-		maps = {
-			[1] = "skogsEntrada",
-			[2] = "BlueTideRing",
-
-		}
-	},
-
-	f1_1_2 = {
-		info = "Beat the f1 world record on Skogs entrada and Blue tide ring",
-		maps = {
-			[1] = "skogsEntrada",
-			[2] = "BlueTideRing",
-
-		}
-		
-	}
-
-}+#version 2

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

# Migration Report: voxscript\ground_default.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/voxscript\ground_default.lua
+++ patched/voxscript\ground_default.lua
@@ -1,37 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
-hollow = GetInt("hollow", 0)
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
+    while y0 < h-1 do
+    	local y1 = y0 + maxSize
+    	if y1 > h-1 then y1 = h-1 end
 
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

# Migration Report: voxscript\groundRallyCross.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/voxscript\groundRallyCross.lua
+++ patched/voxscript\groundRallyCross.lua
@@ -1,37 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
-hollow = GetInt("hollow", 0)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
+    matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
+    matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
+    matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("dirt", 0.66, 0.57, 0.42, 1, 0, 0.1)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h-1 do
+    	local y1 = y0 + maxSize
+    	if y1 > h-1 then y1 = h-1 end
 
-function init()
-	matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
-	matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
-	matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
-	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("dirt", 0.66, 0.57, 0.42, 1, 0, 0.1)
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
