# Migration Report: scripts\bunny_ai.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\bunny_ai.lua
+++ patched/scripts\bunny_ai.lua
@@ -1,86 +1,4 @@
-#include "utility.lua"
-
-isDead = false
-actionTimer = 0
-deathSound = LoadSound('MOD/snd/death.ogg')
-biteSound = LoadLoop('MOD/snd/bite.ogg')
-squeakSound = LoadLoop('MOD/snd/squeak.ogg')
-growlSound = LoadLoop('MOD/snd/growl.ogg')
-bunnyBody = FindBody("bunny")
-allActions = {"hop", "turn", "eat", "poop"}
-isAggressive = false
-bunnyTr = Vec()
-bunnyVel = Vec()
-bunnyCenterPos = Vec()
-bunnyMouthPos = Vec()
-bunnyButtPos = Vec()
-bunnyOnGround = false
-bunnyInWater = false
-playerFeetPos = Vec()
-playerEyePos = Vec()
-biteRadius = 1.5
-stomachSize = 100
-stomachContent = 0
-foodToPoopRatio = 0.65
-eatRadius = 0.5
-facingDir = Vec()
-jumpSpeed = 10
-playerFound = false
-
-
-function init()
-    --DebugWatch("bunnyVox", GetShapeVoxelCount(GetBodyShapes(bunnyBody)[1]))
-    turn()
-end
-
-function tick(dt)
-    if isDead then
-        return
-    end
-
-    bunnyCenterPos = AabbGetBodyCenterPos(bunnyBody)
-    if (not IsBodyValid(bunnyBody)) or IsBodyBroken(bunnyBody) then
-        PlaySound(deathSound, bunnyCenterPos, 1)
-        isDead = true
-        return
-    end
-
-    bunnyTr = GetBodyTransform(bunnyBody)
-    bunnyVel = GetBodyVelocity(bunnyBody)
-    bunnyMouthPos = getBunnyAxisPos(Vec(-0.7, -0.3, 0))
-    bunnyButtPos = getBunnyAxisPos(Vec(0.7, -0.3, 0))
-    bunnyOnGround = isOnGround(bunnyCenterPos, 0.8) or isOnGround(bunnyMouthPos, 0.8) or isOnGround(bunnyButtPos, 0.8)
-    bunnyInWater = IsPointInWater(bunnyButtPos)
-    bunnyCanDoStuff = bunnyOnGround or bunnyInWater or bunnyStopped()
-    --DebugWatch("bunnyVel", bunnyVel)
-    --DebugWatch("bunnyCanDoStuff", bunnyCanDoStuff)
-    --DebugLine(bunnyCenterPos, bunnyMouthPos, 0, 1, 0)
-    --DebugLine(bunnyCenterPos, bunnyButtPos, 1, 0, 0)
-    playerFeetPos = GetPlayerTransform().pos
-    playerEyePos = GetPlayerCameraTransform().pos
-    --DebugWatch("stomachContent", stomachContent)
-
-    isAggressive = HasTag(bunnyBody, "aggressive")
-    if isAggressive then
-        tryBitePlayer(dt)
-        -- If bunny saw player and is no longer moving, act immediately
-        if (bunnyStopped() or IsPointInWater(bunnyCenterPos)) and playerFound then
-            actionTimer = 0
-        end
-    end
-    
-    squeekOnScratch()
-    updateRot()
-
-    --DebugWatch("actionTimer", actionTimer)
-    if actionTimer > 0 then
-        actionTimer = actionTimer - dt
-        return
-    end
-
-    actionTimer = doSomething()
-end
-
+#version 2
 function bunnyStopped()
     return VecLength(bunnyVel) < 0.1
 end
@@ -93,7 +11,7 @@
     if canBitePlayer() then
         --DebugPrint("BITE")
         PlayLoop(biteSound, bunnyCenterPos, 1)
-        SetPlayerHealth(GetPlayerHealth() - (0.2 * dt))
+        SetPlayerHealth(playerId, GetPlayerHealth(playerId) - (0.2 * dt))
     end
 end
 
@@ -113,7 +31,7 @@
 end
 
 function squeekOnScratch()
-    if GetPlayerGrabBody() == bunnyBody then
+    if GetPlayerGrabBody(playerId) == bunnyBody then
         if isAggressive then
             PlayLoop(growlSound, bunnyCenterPos, 1)
         else
@@ -121,7 +39,7 @@
             local dy = InputValue("mousedy")
             local travelDist = VecLength(Vec(dx, dy, 0))
             --DebugWatch("travelDist", travelDist)
-            if travelDist > 0 then
+            if travelDist ~= 0 then
                 PlayLoop(squeakSound, bunnyCenterPos, 1)
             end
         end
@@ -155,7 +73,7 @@
 function trackPlayer()
     -- Check if player visible
     QueryRejectBody(bunnyBody)
-    QueryRejectVehicle(GetPlayerVehicle())
+    QueryRejectVehicle(GetPlayerVehicle(playerId))
     local toPlayer = VecSub(playerEyePos, bunnyCenterPos)
     local distToPlayer = VecLength(toPlayer)
     if QueryRaycast(bunnyCenterPos, VecNormalize(toPlayer), distToPlayer, 0, true) then -- Not blocked
@@ -333,4 +251,57 @@
 	QueryRequire("physical")
 	local hit, dist, normal, shape = QueryRaycast(pos,dir,maxDist)
 	return hit
-end+end
+
+function server.init()
+    turn()
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if isDead then
+            return
+        end
+        bunnyCenterPos = AabbGetBodyCenterPos(bunnyBody)
+        bunnyTr = GetBodyTransform(bunnyBody)
+        bunnyVel = GetBodyVelocity(bunnyBody)
+        bunnyMouthPos = getBunnyAxisPos(Vec(-0.7, -0.3, 0))
+        bunnyButtPos = getBunnyAxisPos(Vec(0.7, -0.3, 0))
+        bunnyOnGround = isOnGround(bunnyCenterPos, 0.8) or isOnGround(bunnyMouthPos, 0.8) or isOnGround(bunnyButtPos, 0.8)
+        bunnyInWater = IsPointInWater(bunnyButtPos)
+        bunnyCanDoStuff = bunnyOnGround or bunnyInWater or bunnyStopped()
+        --DebugWatch("bunnyVel", bunnyVel)
+        --DebugWatch("bunnyCanDoStuff", bunnyCanDoStuff)
+        --DebugLine(bunnyCenterPos, bunnyMouthPos, 0, 1, 0)
+        --DebugLine(bunnyCenterPos, bunnyButtPos, 1, 0, 0)
+        playerFeetPos = GetPlayerTransform(playerId).pos
+        playerEyePos = GetPlayerCameraTransform(playerId).pos
+        --DebugWatch("stomachContent", stomachContent)
+        isAggressive = HasTag(bunnyBody, "aggressive")
+        if isAggressive then
+            tryBitePlayer(dt)
+            -- If bunny saw player and is no longer moving, act immediately
+            if (bunnyStopped() or IsPointInWater(bunnyCenterPos)) and playerFound then
+                actionTimer = 0
+            end
+        end
+        squeekOnScratch()
+        updateRot()
+        --DebugWatch("actionTimer", actionTimer)
+        if actionTimer ~= 0 then
+            actionTimer = actionTimer - dt
+            return
+        end
+        actionTimer = doSomething()
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if (not IsBodyValid(bunnyBody)) or IsBodyBroken(bunnyBody) then
+        PlaySound(deathSound, bunnyCenterPos, 1)
+        isDead = true
+        return
+    end
+end
+

```

---

# Migration Report: scripts\poop.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\poop.lua
+++ patched/scripts\poop.lua
@@ -1,20 +1,18 @@
-deleted = false
-deleteTimer = 60
-poopBody = FindBody("poop")
-poopShape = GetBodyShapes(poopBody)[1]
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if deleted then
+            return
+        end
+        if deleteTimer ~= 0 then
+            deleteTimer = deleteTimer - dt
+            return
+        end
+        -- Poop is not visible and too old, remove it
+        if not IsShapeVisible(poopShape, 1000000, true) then
+            Delete(poopBody)
+            deleted = true
+        end
+    end
+end
 
-function tick(dt)
-    if deleted then
-        return
-    end
-
-    if deleteTimer > 0 then
-        deleteTimer = deleteTimer - dt
-        return
-    end
-    -- Poop is not visible and too old, remove it
-    if not IsShapeVisible(poopShape, 1000000, true) then
-        Delete(poopBody)
-        deleted = true
-    end
-end
```

---

# Migration Report: scripts\utility.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\utility.lua
+++ patched/scripts\utility.lua
@@ -1,76 +1,85 @@
-
-table.unpack = table.unpack or unpack
---[[VECTORS]]
-    -- Distance between two vectors.
-    function VecDist(vec1, vec2) return VecLength(VecSub(vec1, vec2)) end
-    -- Divide a vector by another vector.
-    function VecDiv(v, n) n = n or 1 return Vec(v[1] / n, v[2] / n, v[3] / n) end
-    -- Add all vectors in a table together.
-    function VecAddAll(vectorsTable) local v = Vec(0,0,0) for i = 1, #vectorsTable do VecAdd(v, vectorsTable[i]) end return v end
-    --- Returns a vector with random values.
-    function rdmVec(min, max) return Vec(rdm(min, max),rdm(min, max),rdm(min, max)) end
-    ---Print QuatEulers or vectors.
-    function VecPrint(vec, decimals, label)
+#version 2
+local debugSounds = {
+        beep = LoadSound("warning-beep"),
+        buzz = LoadSound("light/spark0"),
+        chime = LoadSound("elevator-chime"),
+        valu = LoadSound("valuable.ogg"),}
+
+function VecDist(vec1, vec2) return VecLength(VecSub(vec1, vec2)) end
+
+function VecDiv(v, n) n = n or 1 return Vec(v[1] / n, v[2] / n, v[3] / n) end
+
+function VecAddAll(vectorsTable) local v = Vec(0,0,0) for i = 1, #vectorsTable do VecAdd(v, vectorsTable[i]) end return v end
+
+function rdmVec(min, max) return Vec(rdm(min, max),rdm(min, max),rdm(min, max)) end
+
+function VecPrint(vec, decimals, label)
         DebugPrint(VecToStr(vec, decimals, label))
     end
-    function VecToStr(vec, decimals, label)
+
+function VecToStr(vec, decimals, label)
         return (label or "") .. 
             "  " .. sfn(vec[1], decimals or 2) ..
             "  " .. sfn(vec[2], decimals or 2) ..
             "  " .. sfn(vec[3], decimals or 2)
     end
-    function VecToTag(vec, decimals)
+
+function VecToTag(vec, decimals)
         return  sfn(vec[1], decimals or 2) ..
         "_" .. sfn(vec[2], decimals or 2) ..
         "_" .. sfn(vec[3], decimals or 2)
     end
-    function VecFromTag(tag)
+
+function VecFromTag(tag)
         local splitted = sSplit(tag, "_")
         return Vec(tonumber(splitted[1]), tonumber(splitted[2]), tonumber(splitted[3]))
     end
-    function QuatToTag(quat, decimals)
+
+function QuatToTag(quat, decimals)
         return  sfn(quat[1], decimals or 2) ..
         "_" .. sfn(quat[2], decimals or 2) ..
         "_" .. sfn(quat[3], decimals or 2) ..
         "_" .. sfn(quat[4], decimals or 2)
     end
-    function QuatFromTag(tag)
+
+function QuatFromTag(tag)
         local splitted = sSplit(tag, "_")
         return Quat(tonumber(splitted[1]), tonumber(splitted[2]), tonumber(splitted[3]), tonumber(splitted[4]))
     end
-    function TransformToTag(tr, decimals)
+
+function TransformToTag(tr, decimals)
         return  VecToTag(tr.pos, decimals) ..
         "/" .. QuatToTag(tr.rot, decimals)
     end
-    function TransformFromTag(tag)
+
+function TransformFromTag(tag)
         local splitted = sSplit(tag, "/")
         return Transform(VecFromTag(splitted[1]), QuatFromTag(splitted[2]))
     end
-    -- Tells if two vectors face in the same direction
-    function VecSameDir(vec1, vec2)
+
+function VecSameDir(vec1, vec2)
         return VecDot(vec1, vec2) >= 0
     end
-    -- Align a vector to face in the same direction as a reference vector
-    -- (negate its direction if needed)
-    function VecAlign(vec, vecRef)
+
+function VecAlign(vec, vecRef)
         return VecSameDir(vec, vecRef) and vec or VecScale(vec, -1)
     end
-    -- Redirect a vector to face in the same direction as a reference vector
-    function VecRedirect(vec, vecRef)
+
+function VecRedirect(vec, vecRef)
         return VecResize(vecRef, VecLength(vec))
     end
-    -- Set the length of a vector without changing its orientation
-    function VecResize(vec, size) return VecScale(VecNormalize(vec), size) end
-    -- Project a vec1 on vec2 and return the length of vec1 projected
-    function VecProjToVecLen(vec1, vec2) return VecDot(vec1, vec2) / VecLength(vec2) end
-    -- Reflect a vector on a surface
-    function VecReflect(vec, normal) return VecSub(vec, VecScale(normal, 2 * VecDot(vec, normal))) end
-    -- Removed the vertical component of a vector
-    function VecFlatten(vec) return Vec(vec[1], 0, vec[3]) end
-    -- Gets the minimal angle in degree between two vectors
-    function VecAngleBetween(vec1, vec2) return math.deg(math.acos(VecDot(vec1, vec2)/(VecLength(vec1)*VecLength(vec2)))) end
-    -- Gets a 2D vector ignoring given axis
-    function Vec3DTo2D(vec, axis)
+
+function VecResize(vec, size) return VecScale(VecNormalize(vec), size) end
+
+function VecProjToVecLen(vec1, vec2) return VecDot(vec1, vec2) / VecLength(vec2) end
+
+function VecReflect(vec, normal) return VecSub(vec, VecScale(normal, 2 * VecDot(vec, normal))) end
+
+function VecFlatten(vec) return Vec(vec[1], 0, vec[3]) end
+
+function VecAngleBetween(vec1, vec2) return math.deg(math.acos(VecDot(vec1, vec2)/(VecLength(vec1)*VecLength(vec2)))) end
+
+function Vec3DTo2D(vec, axis)
         if axis == "x" then
             return {vec[2], vec[3]}
         elseif axis == "y" then
@@ -80,14 +89,14 @@
         end
         return nil
     end
-    -- Gets the minimal angle in degree between two 2D vectors
-    function Vec2DOrientedAngleBetween(vec1, vec2)
+
+function Vec2DOrientedAngleBetween(vec1, vec2)
         local dot = vec1[1]*vec2[1] + vec1[2]*vec2[2]
         local det = vec1[1]*vec2[2] - vec1[2]*vec2[1]
         return math.deg(math.atan2(det, dot))
     end
-    -- Rotate a vector on a given world axis
-    function VecRotate(vec, axis, angle)
+
+function VecRotate(vec, axis, angle)
         local radAngle = math.rad(angle)
         if axis == "x" then
             local newY = (math.cos(radAngle)*vec[2])-(math.sin(radAngle)*vec[3])
@@ -104,21 +113,21 @@
         end
         return vec
     end
-    -- Rotate a vector to be vertically aligned with another vector
-    function VecAlignOnAxis(vec, vecRef, axis)
+
+function VecAlignOnAxis(vec, vecRef, axis)
         local vec1 = Vec3DTo2D(vec, axis)
         local vec2 = Vec3DTo2D(vecRef, axis)
         local angle = Vec2DOrientedAngleBetween(vec1, vec2)
         return VecRotate(vec, axis, angle)
     end
-    -- Return a vector pointing in the direction of the given quaternion (opposite operation of QuatLookAt())
-    function VecForward(quat) return QuatRotateVec(quat, Vec(0, 0, -1)) end
-    -- Return a vector pointing up based on the direction of the given quaternion
-    function VecUp(quat) return QuatRotateVec(quat, Vec(0, 1, 0)) end
-    -- Return a vector pointing right based on the direction of the given quaternion
-    function VecRight(quat) return QuatRotateVec(quat, Vec(-1, 0, 0)) end
-    -- Returns the oriented pitch and yaw angles to get vec pointing in the exact same direction as vecRef
-    function VecAimAtYawPitch(vec, vecRef)
+
+function VecForward(quat) return QuatRotateVec(quat, Vec(0, 0, -1)) end
+
+function VecUp(quat) return QuatRotateVec(quat, Vec(0, 1, 0)) end
+
+function VecRight(quat) return QuatRotateVec(quat, Vec(-1, 0, 0)) end
+
+function VecAimAtYawPitch(vec, vecRef)
         -- Compute yaw angle
         local normalVec = VecNormalize(vec)
         local normalVecRef = VecNormalize(vecRef)
@@ -134,8 +143,8 @@
         local pitchAngle = Vec2DOrientedAngleBetween(vertVec2D, vertVecRef2D)
         return yawAngle, pitchAngle
     end
-    -- Rotate vec to point in the same direction as vecRef with a max angle in degrees
-    function VecInterpAngleTorward(vec, vecRef, maxAngle)
+
+function VecInterpAngleTorward(vec, vecRef, maxAngle)
         local vecToVecRefAngle = VecAngleBetween(vec, vecRef)
         -- Angle is lower than the max angle? Just point vecotr in the right direction
         if vecToVecRefAngle <= maxAngle then
@@ -156,30 +165,36 @@
         end
     end
 
-
-
---[[QUAT]]
-    function QuatLookDown(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, -1, 0))) end
-    function QuatLookUp(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, 1, 0))) end
-    function QuatTrLookDown(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,-1,0))) end
-    function QuatDir(dir) return QuatLookAt(Vec(0, 0, 0), dir) end -- Quat to 3d worldspace dir.
-    function GetQuatEulerVec(quat) local x,y,z = GetQuatEuler(quat) return Vec(x,y,z) end
-    function QuatConjugate(quat)
+function QuatLookDown(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, -1, 0))) end
+
+function QuatLookUp(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, 1, 0))) end
+
+function QuatTrLookDown(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,-1,0))) end
+
+function QuatDir(dir) return QuatLookAt(Vec(0, 0, 0), dir) end
+
+function GetQuatEulerVec(quat) local x,y,z = GetQuatEuler(quat) return Vec(x,y,z) end
+
+function QuatConjugate(quat)
         return Quat(quat[1], -quat[2], -quat[3], -quat[4])
     end
-    function QuatMagnitude(quat)
+
+function QuatMagnitude(quat)
         return math.sqrt(math.pow(quat[1], 2) + math.pow(quat[2], 2) + math.pow(quat[3], 2) + math.pow(quat[4], 2))
     end
-    function QuatNormalize(quat)
+
+function QuatNormalize(quat)
         local mag = QuatMagnitude(quat)
         return Quat(quat[1]/mag, quat[2]/mag, quat[3]/mag, quat[4]/mag)
     end
-    function QuatInverse(quat)
+
+function QuatInverse(quat)
         local conjugate = QuatConjugate(quat)
         local squaredMagnitude = math.pow(QuatMagnitude(quat), 2)
         return Quat(conjugate[1]/squaredMagnitude, conjugate[2]/squaredMagnitude, conjugate[3]/squaredMagnitude, conjugate[4]/squaredMagnitude)
     end
-    function QuatWorldRotateQuat(a, b)
+
+function QuatWorldRotateQuat(a, b)
         -- Store current quat for later
         local initialQuat = QuatCopy(a)
         -- Negate current quat
@@ -189,7 +204,8 @@
         -- Re-apply old quat
         return QuatRotateQuat(tmpQuat, initialQuat)
     end
-    function QuatWorldRotateVec(a, vec)
+
+function QuatWorldRotateVec(a, vec)
         -- Get quat from vec
         local initialQuat = QuatDir(vec)
         -- Negate quat on vec
@@ -199,7 +215,8 @@
         -- Apply quat to vec
         return QuatRotateVec(tmpQuat, tmpVec)
     end
-    function QuatFlip(quat, keepRoll)
+
+function QuatFlip(quat, keepRoll)
         local forward = Vec(0, 0, -1)
         local dir = VecForward(quat)
         local flippedDir = VecScale(dir, -1)
@@ -213,7 +230,8 @@
         end
         return flippedQuat
     end
-    function QuatAlign(quat, localVector, worldVector)
+
+function QuatAlign(quat, localVector, worldVector)
         local parentVector = QuatRotateVec(quat, localVector)
         local axis = VecCross(parentVector, worldVector)
         local angle = math.deg(math.atan2(VecLength(axis), VecDot(parentVector, worldVector)))
@@ -222,19 +240,18 @@
 
         return alignedRot, offsetRot
     end
-    function TransformToParentQuat(parentT, quat)
+
+function TransformToParentQuat(parentT, quat)
         local childT = Transform(Vec(), quat)
         local t = TransformToParentTransform(parentT, childT)
         return t.rot
     end
-    function QuatRotateAroundAxis(rot, axisVec, angle)
+
+function QuatRotateAroundAxis(rot, axisVec, angle)
         return QuatRotateQuat(rot, QuatAxisAngle(axisVec, angle))
     end
 
-
-
---[[AABB]]
-    function AabbDraw(v1, v2, r, g, b, a)
+function AabbDraw(v1, v2, r, g, b, a)
         r = r or 1
         g = g or 1
         b = b or 1
@@ -263,19 +280,22 @@
         DebugLine(Vec(x1,y1,z2), Vec(x1,y1,z1), r, g, b, a)
         DebugLine(Vec(x1,y2,z2), Vec(x1,y2,z1), r, g, b, a)
     end
-    function AabbCheckOverlap(aMin, aMax, bMin, bMax)
+
+function AabbCheckOverlap(aMin, aMax, bMin, bMax)
         return 
         (aMin[1] <= bMax[1] and aMax[1] >= bMin[1]) and
         (aMin[2] <= bMax[2] and aMax[2] >= bMin[2]) and
         (aMin[3] <= bMax[3] and aMax[3] >= bMin[3])
     end
-    function AabbCheckPointInside(aMin, aMax, p)
+
+function AabbCheckPointInside(aMin, aMax, p)
         return 
         (p[1] <= aMax[1] and p[1] >= aMin[1]) and
         (p[2] <= aMax[2] and p[2] >= aMin[2]) and
         (p[3] <= aMax[3] and p[3] >= aMin[3])
     end
-    function AabbClosestEdge(pos, shape)
+
+function AabbClosestEdge(pos, shape)
 
         local shapeAabbMin, shapeAabbMax = GetShapeBounds(shape)
         local bCenterY = VecLerp(shapeAabbMin, shapeAabbMax, 0.5)[2]
@@ -300,8 +320,8 @@
         end
         return closestEdge, index
     end
-    --- Sort edges by closest to startPos and closest to endPos. Return sorted table.
-    function AabbSortEdges(startPos, endPos, edges)
+
+function AabbSortEdges(startPos, endPos, edges)
         local s, startIndex = aabbClosestEdge(startPos, edges)
         local e, endIndex = aabbClosestEdge(endPos, edges)
         -- Swap first index with startPos and last index with endPos. Everything between stays same.
@@ -309,47 +329,54 @@
         edges = tableSwapIndex(edges, #edges, endIndex)
         return edges
     end
-    function AabbDimensions(min, max) return Vec(max[1] - min[1], max[2] - min[2], max[3] - min[3]) end
-    function AabbGetShapeCenterPos(shape)
+
+function AabbDimensions(min, max) return Vec(max[1] - min[1], max[2] - min[2], max[3] - min[3]) end
+
+function AabbGetShapeCenterPos(shape)
         local mi, ma = GetShapeBounds(shape)
         return VecLerp(mi,ma,0.5)
     end
-    function AabbGetBodyCenterPos(body)
+
+function AabbGetBodyCenterPos(body)
         local mi, ma = GetBodyBounds(body)
         return VecLerp(mi,ma,0.5)
     end
-    function AabbGetShapeCenterTopPos(shape, addY)
+
+function AabbGetShapeCenterTopPos(shape, addY)
         addY = addY or 0
         local mi, ma = GetShapeBounds(shape)
         local v =  VecLerp(mi,ma,0.5)
         v[2] = ma[2] + addY
         return v
     end
-    function AabbGetBodyCenterTopPos(body, addY)
+
+function AabbGetBodyCenterTopPos(body, addY)
         addY = addY or 0
         local mi, ma = GetBodyBounds(body)
         local v =  VecLerp(mi,ma,0.5)
         v[2] = ma[2] + addY
         return v
     end
-    function AabbGetBodyHeight(body)
+
+function AabbGetBodyHeight(body)
         local mi, ma = GetBodyBounds(body)
         return ma[2] - mi[2]
     end
-    function AabbGetShapeHeight(shape)
+
+function AabbGetShapeHeight(shape)
         local mi, ma = GetShapeBounds(shape)
         return ma[2] - mi[2]
     end
-    -- Get center point of the player
-    function AabbGetPlayerCenter()
-        local playerEyeTr = GetPlayerCameraTransform()
-        local playerFeetTr = GetPlayerTransform()
+
+function AabbGetPlayerCenter()
+        local playerEyeTr = GetPlayerCameraTransform(playerId)
+        local playerFeetTr = GetPlayerTransform(playerId)
         return VecAdd(playerFeetTr.pos, VecScale(VecSub(playerEyeTr.pos, playerFeetTr.pos), 0.5))
     end
-    -- Get bounding box of the player
-    function AabbGetPlayerBounds()
-        local playerEyeTr = GetPlayerCameraTransform()
-        local playerFeetTr = GetPlayerTransform()
+
+function AabbGetPlayerBounds()
+        local playerEyeTr = GetPlayerCameraTransform(playerId)
+        local playerFeetTr = GetPlayerTransform(playerId)
         local playerWidth = 1
         local minX = playerFeetTr.pos[1] - (playerWidth / 2)
         local maxX = playerEyeTr.pos[1] + (playerWidth / 2)
@@ -360,8 +387,6 @@
         return Vec(minX, minY, minZ), Vec(maxX, maxY, maxZ)
     end
 
-
---[[OBB]]
 function GetShapeObb(shape)
     local xsize, ysize, zsize, scale = GetShapeSize(shape)
     local min = Vec(0, 0, 0)
@@ -369,6 +394,7 @@
     local tr = GetShapeWorldTransform(shape)
     return tr, min, max
 end
+
 function GetBodyObb(body)
     local shapes = GetBodyShapes(body)
     local min = nil
@@ -401,6 +427,7 @@
     end
     return tr, min, max
 end
+
 function GetObbCorners(tr, min, max)
     local corners = {}
     local localCorners = {
@@ -418,6 +445,7 @@
     end
     return corners
 end
+
 function ObbDraw(c, r, g, b, a)
     r = r or 1
     g = g or 1
@@ -440,22 +468,20 @@
     DebugLine(c[4], c[8], r, g, b, a)
 end
 
-
---[[TABLES]]
-    function TableSwapIndex(t, i1, i2)
+function TableSwapIndex(t, i1, i2)
         local temp = t[i1]
         t[i1] = t[i2]
         t[i2] = temp
         return t
     end
 
-    function TableClone(tb)
+function TableClone(tb)
         local tbc = {}
         for k,v in pairs(tb) do tbc[k] = v end
         return tbc
     end
 
-    function TableRemove(t, fnKeep)
+function TableRemove(t, fnKeep)
         local j, n = 1, #t
     
         for i=1,n do
@@ -474,15 +500,15 @@
         return t
     end
 
-    function TableAppend(t, elem)
+function TableAppend(t, elem)
         t[#t+1] = elem
     end
 
-    function TableClear(t)
+function TableClear(t)
         for i=1,#t do t[i]=nil end
     end
 
-    function DeepCopy(orig)
+function DeepCopy(orig)
         local orig_type = type(orig)
         local copy
         if orig_type == 'table' then
@@ -497,16 +523,15 @@
         return copy
     end
 
-    function TableConcat(t1,t2)
+function TableConcat(t1,t2)
         local t3 = {table.unpack(t1)}
         for i=1,#t2 do
             t3[#t3+1] = t2[i]
         end
         return t3
     end
-    
-
-    function TableEqual(t1, t2)
+
+function TableEqual(t1, t2)
         -- Check length, or else the loop isn't valid.
         if #t1 ~= #t2 then
             return false
@@ -521,7 +546,7 @@
         return true
     end
 
-    function TableToSet(t)
+function TableToSet(t)
         local set = {}
         for i=1, #t do
             set[t[i]] = true
@@ -529,7 +554,7 @@
         return set
     end
 
-    function TableFind(t, elem)
+function TableFind(t, elem)
         -- Check each element.
         for i, v in ipairs(t) do
             if v == elem then
@@ -540,7 +565,7 @@
         return nil
     end
 
-    function TableBinarySearch(t, x)
+function TableBinarySearch(t, x)
         local lo = 1
         local hi = #t
         while lo < hi do
@@ -554,7 +579,7 @@
         return lo
      end
 
-    function TableIndexOf(t, cond)
+function TableIndexOf(t, cond)
         local elem = nil
         local elemIndex = nil
         -- Check each element.
@@ -568,15 +593,15 @@
         return elemIndex
     end
 
-    function TableIndexOfMax(t)
+function TableIndexOfMax(t)
         return TableIndexOf(t, function(elem, max) return elem > max end)
     end
 
-    function TableIndexOfMin(t)
+function TableIndexOfMin(t)
         return TableIndexOf(t, function(elem, min) return elem < min end)
     end
 
-    function TablePushFront(t, elem, maxLength)
+function TablePushFront(t, elem, maxLength)
         maxLength = maxLength or #t
         -- Move each element one step back (remove last one)
         for i=maxLength-1,1,-1 do
@@ -586,8 +611,7 @@
         t[1] = elem
     end
 
-    -- Multiply each value of the same index of two tables
-    function TableMultiply(t1, t2)
+function TableMultiply(t1, t2)
         local res = {}
         for i, v in pairs(t2) do
             table.insert(res, t1[i] * t2[i])
@@ -595,8 +619,7 @@
         return res
     end
 
-    -- Transpose a matrix (2D table)
-    function Matrixranspose(t)
+function Matrixranspose(t)
         local transposed = {}
         for i=1,#t do
             local line = t[i]
@@ -610,8 +633,7 @@
         return transposed
     end
 
-    -- Multiple 2 matrices (2D tables)
-    function MatrixMultiply(t1, t2)
+function MatrixMultiply(t1, t2)
         local multiplied = {}
         for i=1,#t1 do
             if not multiplied[i] then
@@ -628,19 +650,8 @@
         end
         return multiplied
     end
-      
-    
-
-
-
---[[RAYCASTING]]
----comment
----@param tr table
----@param distance number
----@param rad number
----@param rejectBodies table
----@param rejectShapes table
-    function RaycastFromTransform(tr, distance, rad, rejectBodies, rejectShapes)
+
+function RaycastFromTransform(tr, distance, rad, rejectBodies, rejectShapes)
 
         if distance ~= nil then distance = -distance else distance = -300 end
 
@@ -662,7 +673,7 @@
         end
     end
 
-    function QueryRequireTag(tag, value)
+function QueryRequireTag(tag, value)
         if not queryRequiredTags then
             queryRequiredTags = {}
             queryRequiredValues = {}
@@ -671,7 +682,7 @@
         queryRequiredValues[tag] = value
     end
 
-    function QueryRejectTag(tag, value)
+function QueryRejectTag(tag, value)
         if not queryRejectedTags then
             queryRejectedTags = {}
             queryRejectedValues = {}
@@ -680,14 +691,14 @@
         queryRejectedValues[tag] = value
     end
 
-    function QueryClearTags()
+function QueryClearTags()
         queryRequiredTags = {}
         queryRequiredValues = {}
         queryRejectedTags = {}
         queryRejectedValues = {}
     end
 
-    function HasRequiredTag(handle)
+function HasRequiredTag(handle)
         if not queryRequiredTags then
             queryRequiredTags = {}
             queryRequiredValues = {}
@@ -716,7 +727,7 @@
         return true
     end
 
-    function HasRejectedTag(handle)
+function HasRejectedTag(handle)
         if not queryRejectedTags then
             queryRejectedTags = {}
             queryRejectedValues = {}
@@ -745,11 +756,11 @@
         return false
     end
 
-    function MatchesTagFilter(handle)
+function MatchesTagFilter(handle)
         return HasRequiredTag(handle) and not HasRejectedTag(handle)
     end
 
-    function QueryXRaycast(origin, direction, maxDist, radius, rejectTransparent, rejectShapes)
+function QueryXRaycast(origin, direction, maxDist, radius, rejectTransparent, rejectShapes)
         direction = VecNormalize(direction)
         if rejectShapes == nil then
             rejectShapes = {}
@@ -777,7 +788,7 @@
         return {}, {}, {}
     end
 
-    function QueryRaycastClosest(origin, direction, maxDist, radius, rejectTransparent, target, bestDistToTarget, rejectShapes)
+function QueryRaycastClosest(origin, direction, maxDist, radius, rejectTransparent, target, bestDistToTarget, rejectShapes)
         direction = VecNormalize(direction)
         if rejectShapes == nil then
             rejectShapes = {}
@@ -808,25 +819,27 @@
         end
     end
 
-
---[[PHYSICS]]
-    function diminishBodyAngVel(body, rate)
+function diminishBodyAngVel(body, rate)
         local angVel = GetBodyAngularVelocity(body)
         local dRate = rate or 0.99
         local diminishedAngVel = Vec(angVel[1]*dRate, angVel[2]*dRate, angVel[3]*dRate)
         SetBodyAngularVelocity(body, diminishedAngVel)
     end
-    function IsMaterialUnbreakable(mat, shape)
+
+function IsMaterialUnbreakable(mat, shape)
         return mat == 'rock' or mat == 'heavymetal' or mat == 'unbreakable' or mat == 'hardmasonry' or
             HasTag(shape,'unbreakable') or HasTag(GetShapeBody(shape),'unbreakable')
     end
-    function IsBodyValid(body)
+
+function IsBodyValid(body)
         return IsHandleValid(body) and (GetBodyMass(body) > 0)
     end
-    function IsShapeValid(shape)
+
+function IsShapeValid(shape)
         return IsHandleValid(shape) and (GetShapeVoxelCount(shape) > 0)
     end
-    function IsFullBodyValid(body)
+
+function IsFullBodyValid(body)
         if not IsBodyValid(body) then
             return false
         end
@@ -838,7 +851,8 @@
         end
         return true
     end
-    function GetFullBodyMass(body)
+
+function GetFullBodyMass(body)
         local mass = 0
         local jointedBodies = GetJointedBodies(body)
         for i=1,#jointedBodies do
@@ -846,13 +860,15 @@
         end
         return mass
     end
-    function HighlightFullBody(body, r, g, b, a)
+
+function HighlightFullBody(body, r, g, b, a)
         local jointedBodies = GetJointedBodies(body)
         for i=1,#jointedBodies do
             DrawBodyOutline(jointedBodies[i], r, g, b, a)
         end
     end
-    function GetMainBody(body)
+
+function GetMainBody(body)
         local jointedBodies = GetJointedBodies(body)
         local maxMass = GetBodyMass(body)
         local mainBody = body
@@ -866,7 +882,8 @@
         end
         return mainBody
     end
-    function GetMainShape(body)
+
+function GetMainShape(body)
         local shapes = GetBodyShapes(body)
         local maxVoxels = 0
         local mainShape = nil
@@ -881,52 +898,45 @@
         return mainShape
     end
 
---[[VFX]]
-    colors = {
-        white = Vec(1,1,1),
-        black = Vec(0,0,0),
-        grey = Vec(0,0,0),
-        red = Vec(1,0,0),
-        blue = Vec(0,0,1),
-        yellow = Vec(1,1,0),
-        purple = Vec(1,0,1),
-        green = Vec(0,1,0),
-        orange = Vec(1,0.5,0),
-    }
-    function DrawDot(pos, l, w, r, g, b, a, dt)
+function DrawDot(pos, l, w, r, g, b, a, dt)
         local dot = LoadSprite("ui/hud/dot-small.png")
         local spriteRot = QuatLookAt(pos, GetCameraTransform().pos)
         local spriteTr = Transform(pos, spriteRot)
         if dt == nil then dt = true end
         DrawSprite(dot, spriteTr, l or 0.2, w or 0.2, r or 1, g or 1, b or 1, a or 1, dt and true)
     end
-    function RGBTosRGBChannel(channel)
+
+function RGBTosRGBChannel(channel)
         if channel < 0.0031308 then
             return channel * 12.92
         else
             return (1.055 * (channel ^ (1/2.4))) - 0.055
         end
     end
-    function RGBTosRGB(rgb)
+
+function RGBTosRGB(rgb)
         local sr = RGBTosRGBChannel(rgb[1])
         local sg = RGBTosRGBChannel(rgb[2])
         local sb = RGBTosRGBChannel(rgb[3])
         return Vec(sr, sg, sb)
     end
-    function sRGBToRGBChannel(channel)
+
+function sRGBToRGBChannel(channel)
         if channel < 0.04045 then
             return channel / 12.92
         else
             return ((channel + 0.055) / 1.055) ^ 2.4
         end
     end
-    function sRGBToRGB(srgb)
+
+function sRGBToRGB(srgb)
         local r = sRGBToRGBChannel(srgb[1])
         local g = sRGBToRGBChannel(srgb[2])
         local b = sRGBToRGBChannel(srgb[3])
         return Vec(r, g, b)
     end
-    function HSVToRGB(hsv)
+
+function HSVToRGB(hsv)
         local H = ratio(hsv[1], 0, 1, 0, 360)
         local S = hsv[2]
         local V = hsv[3]
@@ -949,7 +959,8 @@
         end
         return VecAdd(rgbPrime, Vec(m, m, m))
     end
-    function RGBToHSV(rgb)
+
+function RGBToHSV(rgb)
         local R = rgb[1]
         local G = rgb[2]
         local B = rgb[3]
@@ -974,8 +985,8 @@
         local V = Cmax
         return Vec(H, S, V)
     end
-    -- Moves the saturation and value components of color to make it move the same way as moving from templateOrigin to templateTarget
-    function offsetColor(color, templateOrigin, templateTarget)
+
+function offsetColor(color, templateOrigin, templateTarget)
         local colorHSV = RGBToHSV(color)
         local templateOriginHSV = RGBToHSV(templateOrigin)
         local templateTargetHSV = RGBToHSV(templateTarget)
@@ -988,8 +999,8 @@
         end
         return finalColor
     end
-    -- Interpolate between two RGB colors in sRBG space
-    function interpColor(color0, color1, percent)
+
+function interpColor(color0, color1, percent)
         -- Use sRGB space for interpolation
         local sRGBStart = RGBTosRGB(color0)
         local sRGBEnd = RGBTosRGB(color1)
@@ -998,64 +1009,59 @@
         return newRGB
     end
 
-
-
---[[SOUND]]
-    local debugSounds = {
-        beep = LoadSound("warning-beep"),
-        buzz = LoadSound("light/spark0"),
-        chime = LoadSound("elevator-chime"),
-        valu = LoadSound("valuable.ogg"),}
-    function beep(pos, vol) PlaySound(debugSounds.beep, pos or GetCameraTransform().pos, vol or 0.3) end
-    function buzz(pos, vol) PlaySound(debugSounds.buzz, pos or GetCameraTransform().pos, vol or 0.3) end
-    function chime(pos, vol) PlaySound(debugSounds.chime, pos or GetCameraTransform().pos, vol or 0.3) end
-    function valu(pos, vol) PlaySound(debugSounds.valu, pos or GetCameraTransform().pos, vol or 0.3) end
-
-
-
---[[MATH]]
-    function round(n, dec) local pow = 10^dec return math.floor(n * pow) / pow end
-    --- return number if > 0, else return 0.00000001
-    function gtZero(n) if n <= 0 then return 0.00000001 end return n end
-    --- return number if not = 0, else return 0.00000001
-    function nZero(n) if n == 0 then return 0.00000001 end return n end
-    --- return random float between min and max
-    function rdmf(min, max)
+function beep(pos, vol) PlaySound(debugSounds.beep, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function buzz(pos, vol) PlaySound(debugSounds.buzz, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function chime(pos, vol) PlaySound(debugSounds.chime, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function valu(pos, vol) PlaySound(debugSounds.valu, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function round(n, dec) local pow = 10^dec return math.floor(n * pow) / pow end
+
+function gtZero(n) if n <= 0 then return 0.00000001 end return n end
+
+function nZero(n) if n == 0 then return 0.00000001 end return n end
+
+function rdmf(min, max)
         min = min or 0
         max = max or 1
         return min + (math.random() * (max-min))
     end
-    --- return random int between min and max
-    function rdm(min, max) return math.random(min or 0, max or 1) end
-    --- return a random number following a standard normal distribution (mean of 0 and standard deviation of 1)
-    function rdmsd()
+
+function rdm(min, max) return math.random(min or 0, max or 1) end
+
+function rdmsd()
         return math.sqrt(-2*math.log(rdmf()))*math.cos(2*math.pi*rdmf())
     end
-    function clamp(value, min, max)
+
+function clamp(value, min, max)
         min = min or 0
         max = max or 1
         if value < min then value = min end
         if value > max then value = max end
         return value
     end
-    function wrap(value, min, max)
+
+function wrap(value, min, max)
         min = min or 0
         max = max or 1
         return (value - min) % ((max + 1) - min) + min
     end
-    -- Brings a value from range [mi, ma] to range [nmi, nma]
-    function ratio(value, mi, ma, nmi, nma)
+
+function ratio(value, mi, ma, nmi, nma)
         nmi = nmi or 0
         nma = nma or 1
         return (value - mi) * (nma - nmi) / (ma - mi) + nmi
     end
-    function oscillate(time)
+
+function oscillate(time)
         local a = (GetTime() / (time or 1)) % 1
         a = a * math.pi
         return math.sin(a)
     end
-    -- return a random point on the surface of a sphere centered on center and of radius radius
-    function getRandPointOnSphere(center, radius)
+
+function getRandPointOnSphere(center, radius)
         local lambda = rdmf(-180, 180)
         local phi = math.acos(2 * rdmf() - 1)
         local x = math.cos(lambda) * math.cos(phi)
@@ -1063,10 +1069,12 @@
         local z = math.sin(lambda)
         return VecAdd(center, Vec(x * radius, y * radius, z * radius))
     end
-    function floatToInt(float)
+
+function floatToInt(float)
         return math.floor(float + .5)
     end
-    function getMinDistBetweenSpherePoints(transform, radius, samples)
+
+function getMinDistBetweenSpherePoints(transform, radius, samples)
 		local points = {}
 		local sqrt, sin, cos = math.sqrt, math.sin, math.cos
 		radius = radius or 1
@@ -1089,8 +1097,8 @@
         -- dbp("getMinDistBetweenSpherePoints radius="..radius..", samples="..samples..", dist="..dist)
 		return dist
 	end
-    -- Interpolate linearly between current value and target value at given speed
-    function linearInterp(startVal, endVal, speed)
+
+function linearInterp(startVal, endVal, speed)
         if endVal < startVal then
             return math.max(startVal - speed, endVal)
         else
@@ -1098,31 +1106,28 @@
         end
     end
 
-
---[[LOGIC]]
-    function ternary ( cond , T , F )
+function ternary ( cond , T , F )
         if cond then return T else return F end
     end
 
-
-
---[[FORMATTING]]
-    --- string format. default 2 decimals.
-    function sfn(numberToFormat, dec)
+function sfn(numberToFormat, dec)
         local s = (tostring(dec or 2))
         return string.format("%."..s.."f", numberToFormat)
     end
-    function sfnTime(dec) return sfn(' '..GetTime(), dec or 4) end
-    function sfnCommas(dec)
+
+function sfnTime(dec) return sfn(' '..GetTime(), dec or 4) end
+
+function sfnCommas(dec)
         return tostring(math.floor(dec)):reverse():gsub("(%d%d%d)","%1,"):gsub(",(%-?)$","%1"):reverse()
         -- https://stackoverflow.com/questions/10989788/format-integer-in-lua
     end
-    function TransformStrDeg(tr)
+
+function TransformStrDeg(tr)
         local x, y, z = GetQuatEuler(tr.rot)
         return VecStr(tr.pos)..'/'..VecStr(Vec(x, y, z))
     end
 
-    function sSplit(inputstr, sep)
+function sSplit(inputstr, sep)
         if sep == nil then
             sep = "%s"
         end
@@ -1132,10 +1137,12 @@
         end
         return t
     end
-    function BoolToStr(bool)
+
+function BoolToStr(bool)
         return bool and "true" or "false"
     end
-    function hasWord(list, word)
+
+function hasWord(list, word)
         local words = sSplit(list)
         for i=1,#words do
             if words[i] == word then
@@ -1144,7 +1151,8 @@
         end
         return false
     end
-    function StrToTable(str, isNum, delim)
+
+function StrToTable(str, isNum, delim)
         delim = delim or ","
         local splittedStr = sSplit(str, delim)
         local out = {}
@@ -1161,7 +1169,8 @@
         end
         return out
     end
-    function TableToStr(tab, delim)
+
+function TableToStr(tab, delim)
         delim = delim or ","
         local sepTab = {}
         for i=1,#tab do
@@ -1173,16 +1182,7 @@
         return table.concat(sepTab)
     end
 
-
-
-
---[[TIMERS]]
-
-    ---Run a timer and a table of functions.
-    ---@param timer table -- = {time, delay}
-    ---@param functions table -- Table of functions that are called when time = 0.
-    ---@param runTime boolean -- Decrement time when calling this function.
-    function TimerRunTimer(timer, functions, runTime)
+function TimerRunTimer(timer, functions, runTime)
         if timer.time <= 0 then
             TimerResetTime(timer)
 
@@ -1195,42 +1195,33 @@
         end
     end
 
-    -- Only runs the timer countdown if there is time left.
-    function TimerRunTime(timer)
-        if timer.time > 0 then
+function TimerRunTime(timer)
+        if timer.time ~= 0 then
             timer.time = timer.time - GetTimeStep()
         end
     end
 
-    -- Set time left to 0.
-    function TimerEndTime(timer)
+function TimerEndTime(timer)
         timer.time = 0
     end
 
-    -- Reset time to start delay.
-    function TimerResetTime(timer)
+function TimerResetTime(timer)
         timer.time = timer.delay
     end
 
---[[PLAYER]]
-
-    -- Get center point of the player
-    function GetPlayerCenter()
-        local playerEyeTr = GetPlayerCameraTransform()
-        local playerFeetTr = GetPlayerTransform()
+function GetPlayerCenter()
+        local playerEyeTr = GetPlayerCameraTransform(playerId)
+        local playerFeetTr = GetPlayerTransform(playerId)
         return VecAdd(playerFeetTr.pos, VecScale(VecSub(playerEyeTr.pos, playerFeetTr.pos), 0.5))
     end
 
-    -- Get direction the player is looking
-    function GetPlayerLookDir()
+function GetPlayerLookDir()
         local playerTr = GetCameraTransform()
         return TransformToParentVec(playerTr, Vec(0, 0, -1))
     end
 
-    -- Returns true if the given position is "inside" the player
-    function IsPointInPlayer(pos)
+function IsPointInPlayer(pos)
         local min, max = AabbGetPlayerBounds()
         return AabbCheckPointInside(min, max, pos)
     end
 
-    
```
