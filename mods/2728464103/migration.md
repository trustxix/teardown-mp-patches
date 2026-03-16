# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,25 +1,7 @@
-------------------------------------------------
---- The Swap Button
---- By: Geneosis
-------------------------------------------------
-
-function init()
-	--Register tool and enable it
-	tool = "the_swap_button"
-	RegisterTool(tool, "The Swap Button", "MOD/vox/the_swap_button.vox")
-	SetBool("game.tool."..tool..".enabled", true)
-	
-	swapSnd = LoadSound("MOD/snd/swap0.ogg")
-
-	swapList = {}
-	swapListIndex = 1
-	
-end
-
--- Get bounding box of the player
+#version 2
 function getPlayerBbox()
-    local playerEyeTr = GetPlayerCameraTransform()
-    local playerFeetTr = GetPlayerTransform()
+    local playerEyeTr = GetPlayerCameraTransform(playerId)
+    local playerFeetTr = GetPlayerTransform(playerId)
     local playerWidth = 1
     local minX = playerFeetTr.pos[1] - (playerWidth / 2)
     local maxX = playerEyeTr.pos[1] + (playerWidth / 2)
@@ -30,17 +12,14 @@
     return Vec(minX, minY, minZ), Vec(maxX, maxY, maxZ)
 end
 
---- return random float betzeen min and max
 function rdmf(min, max)
 	min = min or 0
 	max = max or 1
 	return min + (math.random() * (max-min))
 end
 
---- return random int betzeen min and max
 function rdm(min, max) return math.random(min or 0, max or 1) end
 
---- efficiently remove more than one items from a table
 function TableRemove(t, fnKeep)
 	local j, n = 1, #t
 
@@ -60,7 +39,6 @@
 	return t
 end
 
-
 function getBodyInfos(body)
 	local tr = GetBodyTransform(body)
 	local pos = tr.pos
@@ -70,16 +48,14 @@
 	return tr, pos, center, halfHeight
 end
 
-
 function getPlayerInfos()
-	local tr = GetPlayerTransform()
+	local tr = GetPlayerTransform(playerId)
 	local pos = tr.pos
 	local min, max = getPlayerBbox()
 	local center = VecLerp(min,max,0.5)
 	local halfHeight = getHalfHeight(center, min)
 	return tr, pos, center, halfHeight
 end
-
 
 function teleportBody(body, tr)
 	local jointedBodies = GetJointedBodies(body)
@@ -93,7 +69,6 @@
 	end
 end
 
-
 function swapObject(targetBody)
 	-- If no target, nothing to do
 	if targetBody == nil then
@@ -102,7 +77,7 @@
 	local tr1, pos1, center1, halfHeight1 = getBodyInfos(targetBody)
 	-- If swap list is not empty, pick next body in swap list as otherBody
 	local otherBody = nil
-	if #swapList > 0 then
+	if #swapList ~= 0 then
 		otherBody = getNextSwapListBody()
 		-- Do nothing if we tried to swap target body with itself
 		if otherBody == targetBody then
@@ -116,7 +91,7 @@
 		local min = VecAdd(pos1, Vec(-radius, -radius, -radius))
 		local max = VecAdd(pos1, Vec(radius, radius, radius))
 		local otherBodies = QueryAabbBodies(min, max)
-		if #otherBodies > 0 then
+		if #otherBodies ~= 0 then
 			local rndIndex = rdm(1, #otherBodies)
 			local tryOtherBody = otherBodies[rdm(1, #otherBodies)]
 			while IsBodyJointedToStatic(tryOtherBody) do
@@ -144,7 +119,6 @@
 	end
 end
 
-
 function getNextSwapListBody()
 	if swapListIndex > #swapList then
 		swapListIndex = 1
@@ -153,7 +127,6 @@
 	swapListIndex = swapListIndex + 1
 	return body
 end
-
 
 function cleanupSwapList()
 	swapList = TableRemove(swapList, function(t, i, j)
@@ -162,7 +135,6 @@
         return IsHandleValid(body) and GetBodyMass(body) > 0
     end)
 end
-
 
 function swapMe(targetBody)
 	-- If no target and no body in swap list, nothing to do
@@ -180,15 +152,13 @@
 	tr1.pos = newPos1
 	tr2.pos = newPos2
 	teleportBody(targetBody, tr1)
-	SetPlayerTransform(tr2)
+	SetPlayerTransform(playerId, tr2)
 	doSwapEffect(center1, halfHeight1, center2, halfHeight2)
 end
-
 
 function getHalfHeight(center, min)
 	return center[2]-min[2]
 end
-
 
 function getDistToFloor(body, center, maxDist)
 	if body ~= nil then
@@ -202,8 +172,6 @@
 	end
 end
 
--- Get the expected position after swap, attempting to make objects
--- stay on the ground if they were already on the ground
 function getSwappedPos(pos1, center1, distToFloor1, pos2, center2, distToFloor2)
 	local foot1 = Vec(center1[1], center1[2] - distToFloor1, center1[3])
 	local foot2 = Vec(center2[1], center2[2] - distToFloor2, center2[3])
@@ -223,12 +191,10 @@
 	return newPos1, newPos2
 end
 
-
 function doSwapEffect(pos1, radius1, pos2, radius2)
 	doSwapEffectAt(pos1, radius1)
 	doSwapEffectAt(pos2, radius2)
 end
-
 
 function doSwapEffectAt(pos, radius)
 	PlaySound(swapSnd, pos, 0.5)
@@ -268,7 +234,6 @@
 	end
 end
 
-
 function getRandPosInCylinder(center, radius, height)
 	local s = rdmf()
 	local theta = rdmf(0, 2*math.pi)
@@ -279,14 +244,12 @@
 	return VecAdd(center, Vec(x, z, y))
 end
 
-
 function highlightFullBody(body, r, g, b, a)
 	local jointedBodies = GetJointedBodies(body)
 	for i=1,#jointedBodies do
 		DrawBodyOutline(jointedBodies[i], r, g, b, a)
 	end
 end
-
 
 function addToSwapList(targetBody)
 	-- If no target, nothing to do
@@ -304,97 +267,14 @@
 	swapList[#swapList+1] = targetBody
 end
 
-
 function clearSwapList()
 	swapList = {}
 end
 
-
-function tick(dt)
-	-- Check if the swap button is selected
-	if GetString("game.player.tool") == tool and (GetPlayerVehicle() == 0) then
-
-		local selectionMode = InputDown("rmb")
-		-- Move tool in position
-		local t = Transform()
-		t.pos = Vec(0.55, -0.55, -0.5)
-		t.rot = QuatEuler(10, 0, 0)
-		SetToolTransform(t)
-
-		-- Animate button pressed
-		local b = GetToolBody()
-		if body ~= b then
-			body = b
-			-- Button is the second shape in vox file. Remember original position in attachment frame
-			local shapes = GetBodyShapes(b)
-			button = shapes[2] 
-			buttonTransform = GetShapeLocalTransform(button)
-		end
-		t = Transform(buttonTransform.pos, buttonTransform.rot)
-		if InputDown("lmb") or InputDown("mmb") then
-			t.pos = VecAdd(t.pos, Vec(0, -0.04, 0))
-		else
-			t.pos = VecAdd(t.pos, Vec(0, -0.02, 0))
-		end
-		SetShapeLocalTransform(button, t)
-
-		-- Highlight object in front of player
-		local ct = GetCameraTransform()
-		QueryRequire("physical large")
-		local transform = TransformToParentVec(ct, Vec(0, 0, -1))
-		local hit, dist, normal, shape = QueryRaycast(ct.pos, transform, 1000000)
-		local targetBody = nil
-		if hit then
-			local tryTargetBody = GetShapeBody(shape)
-			if IsBodyDynamic(tryTargetBody) and not IsBodyJointedToStatic(tryTargetBody) then
-				targetBody = tryTargetBody
-				-- Draw highlight
-				local r = rdmf()
-				local g = rdmf()
-				local b = rdmf()
-				-- In selection mode only use gray outlines
-				if selectionMode then
-					g = r
-					b = r
-				end
-				highlightFullBody(targetBody, r, g, b, 0.5)
-				-- Force body active so that stacks of objects will fall
-				-- if you swap the item at the bottom of it.
-				SetBodyActive(targetBody, true)
-			end
-		end	
-		-- Remove from swap list object that no longer exist
-		cleanupSwapList()
-		-- Check if swap button activated
-		if selectionMode then
-			if InputPressed("lmb") then
-				addToSwapList(targetBody)
-			elseif InputPressed("mmb") then
-				clearSwapList()
-			end
-		else
-			if InputPressed("lmb") then
-				swapObject(targetBody)
-			elseif InputPressed("mmb") then
-				swapMe(targetBody)
-			end
-		end
-		-- In selection mode highlight all selected objects
-		if selectionMode then
-			for i=1,#swapList do
-				local greyShade = rdmf(0.5, 1)
-				highlightFullBody(swapList[i], greyShade, greyShade, greyShade, 1)
-			end
-		end
-	end
-end
-
-
 function padding(w, h)
     UiTranslate(w or 10, h or 10)
 end
 
---- Draw pad preview infos when in edition mode at bottom left
 function uiDrawKeyHint()
 
     UiPush()
@@ -419,17 +299,104 @@
 
 end
 
-
-function draw()
-
-    if GetString("game.player.tool") == tool then
-        -- Update key hint
-		hintTimer = hintTimer - GetTimeStep()
-		uiDrawKeyHint()
-    else
-		hintTimer = 6
-	end
-
-end
-
-
+function server.init()
+    tool = "the_swap_button"
+    RegisterTool(tool, "The Swap Button", "MOD/vox/the_swap_button.vox")
+    SetBool("game.tool."..tool..".enabled", true, true)
+    swapList = {}
+    swapListIndex = 1
+end
+
+function client.init()
+    swapSnd = LoadSound("MOD/snd/swap0.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == tool and (GetPlayerVehicle(playerId) == 0) then
+
+    	local selectionMode = InputDown("rmb")
+    	-- Move tool in position
+    	local t = Transform()
+    	t.pos = Vec(0.55, -0.55, -0.5)
+    	t.rot = QuatEuler(10, 0, 0)
+    	SetToolTransform(t)
+
+    	-- Animate button pressed
+    	local b = GetToolBody()
+    	if body ~= b then
+    		body = b
+    		-- Button is the second shape in vox file. Remember original position in attachment frame
+    		local shapes = GetBodyShapes(b)
+    		button = shapes[2] 
+    		buttonTransform = GetShapeLocalTransform(button)
+    	end
+    	t = Transform(buttonTransform.pos, buttonTransform.rot)
+    	if InputDown("lmb") or InputDown("mmb") then
+    		t.pos = VecAdd(t.pos, Vec(0, -0.04, 0))
+    	else
+    		t.pos = VecAdd(t.pos, Vec(0, -0.02, 0))
+    	end
+    	SetShapeLocalTransform(button, t)
+
+    	-- Highlight object in front of player
+    	local ct = GetCameraTransform()
+    	QueryRequire("physical large")
+    	local transform = TransformToParentVec(ct, Vec(0, 0, -1))
+    	local hit, dist, normal, shape = QueryRaycast(ct.pos, transform, 1000000)
+    	local targetBody = nil
+    	if hit then
+    		local tryTargetBody = GetShapeBody(shape)
+    		if IsBodyDynamic(tryTargetBody) and not IsBodyJointedToStatic(tryTargetBody) then
+    			targetBody = tryTargetBody
+    			-- Draw highlight
+    			local r = rdmf()
+    			local g = rdmf()
+    			local b = rdmf()
+    			-- In selection mode only use gray outlines
+    			if selectionMode then
+    				g = r
+    				b = r
+    			end
+    			highlightFullBody(targetBody, r, g, b, 0.5)
+    			-- Force body active so that stacks of objects will fall
+    			-- if you swap the item at the bottom of it.
+    			SetBodyActive(targetBody, true)
+    		end
+    	end	
+    	-- Remove from swap list object that no longer exist
+    	cleanupSwapList()
+    	-- Check if swap button activated
+    	if selectionMode then
+    		if InputPressed("lmb") then
+    			addToSwapList(targetBody)
+    		elseif InputPressed("mmb") then
+    			clearSwapList()
+    		end
+    	else
+    		if InputPressed("lmb") then
+    			swapObject(targetBody)
+    		elseif InputPressed("mmb") then
+    			swapMe(targetBody)
+    		end
+    	end
+    	-- In selection mode highlight all selected objects
+    	if selectionMode then
+    		for i=1,#swapList do
+    			local greyShade = rdmf(0.5, 1)
+    			highlightFullBody(swapList[i], greyShade, greyShade, greyShade, 1)
+    		end
+    	end
+    end
+end
+
+function client.draw()
+       if GetString("game.player.tool") == tool then
+           -- Update key hint
+    	hintTimer = hintTimer - GetTimeStep()
+    	uiDrawKeyHint()
+       else
+    	hintTimer = 6
+    end
+end
+

```
