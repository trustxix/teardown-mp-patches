# Migration Report: DESPAWNPOTIONEFFECT.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/DESPAWNPOTIONEFFECT.lua
+++ patched/DESPAWNPOTIONEFFECT.lua
@@ -1,21 +1,20 @@
-start_time = 0
-body = 0
-shape = 0
-
-function init()
-	body = FindBody("NPC_VOXBOX_EFFECT")
-	shape = FindShape("NPC_VOXBOX_EFFECT")
+#version 2
+function server.init()
+    body = FindBody("NPC_VOXBOX_EFFECT")
+    shape = FindShape("NPC_VOXBOX_EFFECT")
 end
 
-function tick(dt)
-	start_time = start_time + dt
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        start_time = start_time + dt
+        if start_time > 1 then
+        	if body ~= 0 then
+        		Delete(body)
+        	end
+        	if shape ~= 0 then
+        		Delete(shape)
+        	end
+        end
+    end
+end
 
-	if start_time > 1 then
-		if body ~= 0 then
-			Delete(body)
-		end
-		if shape ~= 0 then
-			Delete(shape)
-		end
-	end
-end

```

---

# Migration Report: gorelaunchExplode.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/gorelaunchExplode.lua
+++ patched/gorelaunchExplode.lua
@@ -1,55 +1,6 @@
+#version 2
 function rnd(mi, ma)
     return math.random() * (ma - mi) + mi
-end
-
-function init()
-    force = 5
-    tim = 0
-    maxPaintTime = math.random(15, 30)
-
-    body = FindBody("gore")
-    gore = FindShape("gore")
-    if body == 0 or gore == 0 then return end
-
-    local imp = Vec(
-        rnd(-force, force),
-        rnd(force * 0.33, force),
-        rnd(-force, force)
-    )
-    SetBodyVelocity(body, imp)
-    SetBodyAngularVelocity(body, imp)
-
-    -- local shapes = GetBodyShapes(body)
-    -- for i=1,#shapes do
-        -- SetShapeCollisionFilter(shapes[i], 0, 255)
-    -- end
-	
-	gore_trans = GetBodyTransform(body)
-	for i=1, 100 do
-		ParticleReset()
-		ParticleTile(rnd(0, 10))
-		ParticleType("plain")
-		ParticleRadius(rnd(0.05,-0.1))
-		ParticleSticky(0.15)
-		ParticleEmissive(0, 0)
-		ParticleCollide(1)
-		ParticleColor(rnd(.60,.05,.0, .35,.05,.0))
-		ParticleGravity(rnd(-8,-9))
-		ParticleAlpha(1, 0.0)
-		SpawnParticle(VecAdd(gore_trans.pos, Vec(rnd(-0.0,0.0),rnd(-0.0,0.0),rnd(-0.0,0.0))), Vec(rnd(-2,2),rnd(2,2),rnd(-2,2)), 15)
-	end
-end
-
-function update(dt)
-    tim = tim + 1
-    if tim < maxPaintTime and not IsShapeBroken(gore) then
-        local p = GetAimPos()
-        if p and math.random(1, 3) == 3 then
-            PaintRGBA(p, 0.2, rnd(0.30, 0.45), 0, 0, 1, 0.75)
-        end
-    else
-        Delete(body)
-    end
 end
 
 function GetAimPos()
@@ -74,3 +25,58 @@
         return VecAdd(t.pos, VecScale(dir, dist))
     end
 end
+
+function server.init()
+    force = 5
+    tim = 0
+    maxPaintTime = math.random(15, 30)
+    body = FindBody("gore")
+    gore = FindShape("gore")
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        tim = tim + 1
+        if tim < maxPaintTime and not IsShapeBroken(gore) then
+            local p = GetAimPos()
+            if p and math.random(1, 3) == 3 then
+                PaintRGBA(p, 0.2, rnd(0.30, 0.45), 0, 0, 1, 0.75)
+            end
+        else
+            Delete(body)
+        end
+    end
+end
+
+function client.init()
+       if body == 0 or gore == 0 then return end
+
+       local imp = Vec(
+           rnd(-force, force),
+           rnd(force * 0.33, force),
+           rnd(-force, force)
+       )
+       SetBodyVelocity(body, imp)
+       SetBodyAngularVelocity(body, imp)
+
+       -- local shapes = GetBodyShapes(body)
+       -- for i=1,#shapes do
+           -- SetShapeCollisionFilter(shapes[i], 0, 255)
+       -- end
+
+    gore_trans = GetBodyTransform(body)
+    for i=1, 100 do
+    	ParticleReset()
+    	ParticleTile(rnd(0, 10))
+    	ParticleType("plain")
+    	ParticleRadius(rnd(0.05,-0.1))
+    	ParticleSticky(0.15)
+    	ParticleEmissive(0, 0)
+    	ParticleCollide(1)
+    	ParticleColor(rnd(.60,.05,.0, .35,.05,.0))
+    	ParticleGravity(rnd(-8,-9))
+    	ParticleAlpha(1, 0.0)
+    	SpawnParticle(VecAdd(gore_trans.pos, Vec(rnd(-0.0,0.0),rnd(-0.0,0.0),rnd(-0.0,0.0))), Vec(rnd(-2,2),rnd(2,2),rnd(-2,2)), 15)
+    end
+end
+

```

---

# Migration Report: gorelaunchExplodePurple.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/gorelaunchExplodePurple.lua
+++ patched/gorelaunchExplodePurple.lua
@@ -1,55 +1,6 @@
+#version 2
 function rnd(mi, ma)
     return math.random() * (ma - mi) + mi
-end
-
-function init()
-    force = 5
-    tim = 0
-    maxPaintTime = math.random(15, 30)
-
-    body = FindBody("gore")
-    gore = FindShape("gore")
-    if body == 0 or gore == 0 then return end
-
-    local imp = Vec(
-        rnd(-force, force),
-        rnd(force * 0.33, force),
-        rnd(-force, force)
-    )
-    SetBodyVelocity(body, imp)
-    SetBodyAngularVelocity(body, imp)
-
-    -- local shapes = GetBodyShapes(body)
-    -- for i=1,#shapes do
-        -- SetShapeCollisionFilter(shapes[i], 0, 255)
-    -- end
-	
-	gore_trans = GetBodyTransform(body)
-	for i=1, 100 do
-		ParticleReset()
-		ParticleTile(rnd(0, 10))
-		ParticleType("plain")
-		ParticleRadius(rnd(0.05,-0.1))
-		ParticleSticky(0.15)
-		ParticleEmissive(0, 0)
-		ParticleCollide(1)
-		ParticleColor(rnd(.30,.05,.40, .35,.05,.50))
-		ParticleGravity(rnd(-8,-9))
-		ParticleAlpha(1, 0.0)
-		SpawnParticle(VecAdd(gore_trans.pos, Vec(rnd(-0.0,0.0),rnd(-0.0,0.0),rnd(-0.0,0.0))), Vec(rnd(-2,2),rnd(2,2),rnd(-2,2)), 15)
-	end
-end
-
-function update(dt)
-    tim = tim + 1
-    if tim < maxPaintTime and not IsShapeBroken(gore) then
-        local p = GetAimPos()
-        if p and math.random(1, 3) == 3 then
-            PaintRGBA(p, 0.2, rnd(0.25, 0.35), 0, 0.70, 1, 0.75)
-        end
-    else
-        Delete(body)
-    end
 end
 
 function GetAimPos()
@@ -74,3 +25,58 @@
         return VecAdd(t.pos, VecScale(dir, dist))
     end
 end
+
+function server.init()
+    force = 5
+    tim = 0
+    maxPaintTime = math.random(15, 30)
+    body = FindBody("gore")
+    gore = FindShape("gore")
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        tim = tim + 1
+        if tim < maxPaintTime and not IsShapeBroken(gore) then
+            local p = GetAimPos()
+            if p and math.random(1, 3) == 3 then
+                PaintRGBA(p, 0.2, rnd(0.25, 0.35), 0, 0.70, 1, 0.75)
+            end
+        else
+            Delete(body)
+        end
+    end
+end
+
+function client.init()
+       if body == 0 or gore == 0 then return end
+
+       local imp = Vec(
+           rnd(-force, force),
+           rnd(force * 0.33, force),
+           rnd(-force, force)
+       )
+       SetBodyVelocity(body, imp)
+       SetBodyAngularVelocity(body, imp)
+
+       -- local shapes = GetBodyShapes(body)
+       -- for i=1,#shapes do
+           -- SetShapeCollisionFilter(shapes[i], 0, 255)
+       -- end
+
+    gore_trans = GetBodyTransform(body)
+    for i=1, 100 do
+    	ParticleReset()
+    	ParticleTile(rnd(0, 10))
+    	ParticleType("plain")
+    	ParticleRadius(rnd(0.05,-0.1))
+    	ParticleSticky(0.15)
+    	ParticleEmissive(0, 0)
+    	ParticleCollide(1)
+    	ParticleColor(rnd(.30,.05,.40, .35,.05,.50))
+    	ParticleGravity(rnd(-8,-9))
+    	ParticleAlpha(1, 0.0)
+    	SpawnParticle(VecAdd(gore_trans.pos, Vec(rnd(-0.0,0.0),rnd(-0.0,0.0),rnd(-0.0,0.0))), Vec(rnd(-2,2),rnd(2,2),rnd(-2,2)), 15)
+    end
+end
+

```

---

# Migration Report: Nextbot_visuals.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Nextbot_visuals.lua
+++ patched/Nextbot_visuals.lua
@@ -1,54 +1,5 @@
-local function clamp(v, a, b) return math.min(math.max(v, a), b) end
-function rnd(min, max) return math.random() * (max - min) + min end
-function VecDist(a, b) return VecLength(VecSub(a, b)) end
-function lerp(a, b, t) if a == nil then a = b end if b == nil then b = a end return a + (b - a) * (t or 0) end
-function VecToString(v) return string.format("%.2f_%.2f_%.2f", v[1], v[2], v[3]) end
-
+#version 2
 local _QueryRaycast = QueryRaycast
-local function QueryRaycastSilent(origin, direction, maxDist, radius, rejectTransparent)
-    return _QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
-end
-function QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
-    local hit, dist, normal, shape = _QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
-    local endpoint = VecAdd(origin, VecScale(direction, maxDist))
-    local hitpoint = hit and VecAdd(origin, VecScale(direction, dist)) or endpoint
-    if hit then
-        DebugLine(origin, hitpoint, 1, 0, 0, 1)
-        DebugLine(hitpoint, endpoint, 1, 0.5, 0, 0.4)
-        DebugCross(hitpoint, 1, 0, 0, 1)
-    else
-        DebugLine(origin, endpoint, 0, 1, 0, 1)
-    end
-
-    DebugCross(origin, 0, 0.5, 1, 1)
-    return hit, dist, normal, shape
-end
-
-bodyTag = GetStringParam("bodyTag", "NPC_NEXTBOT_CHASE")
-lightTag = GetStringParam("lightTag", "")
-lightBreakRange = GetFloatParam("lightBreakRange", 1.0)
-visualFadeSpeed = GetFloatParam("visualFadeSpeed", 0.035)
-farMaxVol = GetFloatParam("farMaxVol", 5.0)
-nearMaxVol = GetFloatParam("nearMaxVol", 1.75)
-fadeSpeed = GetFloatParam("fadeSpeed", 0.015)
-backgroundLoopPath = GetStringParam("backgroundLoopPath", "MOD/SM64_Slider.ogg")
-backgroundLoopProgress = 0
-backgroundLoopVolumeMul = GetFloatParam("backgroundLoopVolumeMul", 1.0)
-nearLoopPath = GetStringParam("nearLoopPath", "MOD/near_loop.ogg")
-mainSoundPath = GetStringParam("mainSoundPath", "MOD/sm64_mario_snd_0.ogg")
-mainSoundVolume = GetFloatParam("mainSoundVolume", 1.0)
-mainSoundMinDelay = GetIntParam("mainSoundMinDelay", 0)
-mainSoundMaxDelay = GetIntParam("mainSoundMaxDelay", 1)
-mainSoundChanceMin = GetIntParam("mainSoundChanceMin", 1)
-mainSoundChanceMax = GetIntParam("mainSoundChanceMax", 20)
-spritePath = GetStringParam("spritePath", "MOD/sprite.png")
-spriteScaleBase = GetFloatParam("spriteScaleBase", 3.0)
-spriteAlphaBase = GetFloatParam("spriteAlphaBase", 1)
-spriteJitterBase = GetFloatParam("spriteJitterBase", 0.0)
-jitterStrengthMul = GetFloatParam("jitterStrengthMul", 1.0)
-UnstuckBreaking = GetBoolParam("UnstuckBreaking", true)
-mainSoundSequential = GetBoolParam("mainSoundSequential", false)
-
 local CFG = {
     cellSize = 1.5,
     agentHeight = 2.0,
@@ -76,7 +27,6 @@
     maxLayers = 8,
     minLayerGap = 0.2,
 }
-
 local nm = {
     nodes = {},
     grid = {},
@@ -105,13 +55,42 @@
     expandConnectStart = 1,
     blockedEdges = {},
 }
-
 local navPath = nil
 local rawPath = nil
 local goalPos = nil
 local pathTimer = 0.0
 local npcWaypointIdx = 1
 local npcMoveDir = Vec(0, 0, 1)
+
+local function clamp(v, a, b) return math.min(math.max(v, a), b) end
+
+function rnd(min, max) return math.random() * (max - min) + min end
+
+function VecDist(a, b) return VecLength(VecSub(a, b)) end
+
+function lerp(a, b, t) if a == nil then a = b end if b == nil then b = a end return a + (b - a) * (t or 0) end
+
+function VecToString(v) return string.format("%.2f_%.2f_%.2f", v[1], v[2], v[3]) end
+
+local function QueryRaycastSilent(origin, direction, maxDist, radius, rejectTransparent)
+    return _QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
+end
+
+function QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
+    local hit, dist, normal, shape = _QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
+    local endpoint = VecAdd(origin, VecScale(direction, maxDist))
+    local hitpoint = hit and VecAdd(origin, VecScale(direction, dist)) or endpoint
+    if hit then
+        DebugLine(origin, hitpoint, 1, 0, 0, 1)
+        DebugLine(hitpoint, endpoint, 1, 0.5, 0, 0.4)
+        DebugCross(hitpoint, 1, 0, 0, 1)
+    else
+        DebugLine(origin, endpoint, 0, 1, 0, 1)
+    end
+
+    DebugCross(origin, 0, 0.5, 1, 1)
+    return hit, dist, normal, shape
+end
 
 local function toGrid(pos)
     return math.floor(pos[1] / CFG.cellSize + 0.5), math.floor(pos[3] / CFG.cellSize + 0.5)
@@ -218,7 +197,7 @@
         cols, rows, cols * rows, CFG.maxLayers))
 end
 
-local function buildTick()
+cal function buildTick()
     if not nm.building then return end
 
     if nm.phase == "sample" then
@@ -357,7 +336,9 @@
     end
 end
 
-local function dynamicCheckTick()
+local func
+
+on dynamicCheckTick()
     if not nm.built or #nm.edgeList == 0 then return end
 
     for _ = 1, CFG.dynamicCheckPerFrame do
@@ -388,7 +369,7 @@
                         local bt = GetBodyTransform(bodyHandle)
                         rebuildPos = TransformToParentPoint(bt, GetBodyCenterOfMass(bodyHandle))
                     else
-                        rebuildPos = GetPlayerPos()
+                        rebuildPos = GetPlayerPos(playerId)
                     end
                     StartNavMeshBuild(rebuildPos, CFG.scanRadius)
                     return
@@ -400,7 +381,9 @@
     end
 end
 
-local function ExpandNavMesh(centerPos, radius)
+local func
+
+on ExpandNavMesh(centerPos, radius)
     if nm.building then return end
     local cs = CFG.cellSize
     local newMinX = math.floor((centerPos[1] - radius) / cs)
@@ -436,7 +419,9 @@
     DebugPrint(string.format("[NavMesh] Expanding — %d new cells queued", #queue))
 end
 
-local function expansionCheckTick()
+local functi
+
+ expansionCheckTick()
     if nm.building then return end
     local cs = CFG.cellSize
     local margin = CFG.expandEdgeMargin
@@ -448,7 +433,7 @@
             or pos[3] > nm.covMaxZ * cs - margin
     end
 
-    local playerPos = GetPlayerPos()
+    local playerPos = GetPlayerPos(playerId)
     if needsExpand(playerPos) then
         DebugPrint("[NavMesh] Player near edge — expanding")
         ExpandNavMesh(playerPos, CFG.scanRadius)
@@ -465,7 +450,9 @@
     end
 end
 
-local function nearestNode(pos)
+local function n
+
+restNode(pos)
     local gx, gz = toGrid(pos)
     local best, bestDist = nil, math.huge
 
@@ -487,7 +474,9 @@
     return best
 end
 
-local function astar(startIdx, goalIdx)
+local function a
+
+ar(startIdx, goalIdx)
     if startIdx == goalIdx then return { nm.nodes[startIdx].pos } end
 
     local goalPos3 = nm.nodes[goalIdx].pos
@@ -540,7 +529,9 @@
     return nil
 end
 
-local function smoothPath(path)
+local function s
+
+othPath(path)
     if not path or #path < 3 then return path end
     local result = { path[1] }
     local i = 1
@@ -565,7 +556,9 @@
     return result
 end
 
-function NavMeshQuery(fromPos, toPos)
+function NavMesh
+
+ery(fromPos, toPos)
     if not nm.built then DebugPrint("[NavMesh] Not built yet."); return nil end
     local si = nearestNode(fromPos)
     local gi = nearestNode(toPos)
@@ -576,7 +569,9 @@
     return path
 end
 
-local function drawMesh()
+local function d
+
+wMesh()
     if not nm.built then return end
     local cam = GetCameraTransform()
     local cx = cam.pos[1]
@@ -675,7 +670,9 @@
     end
 end
 
-local function drawPath()
+local function d
+
+wPath()
     if not navPath then return end
     if rawPath then
         for i = 1, #rawPath - 1 do
@@ -697,7 +694,9 @@
     end
 end
 
-local function buildProgress()
+local function b
+
+ldProgress()
     local total = (nm.bMaxX - nm.bMinX + 1) * (nm.bMaxZ - nm.bMinZ + 1)
     if total == 0 then return 0 end
     local done = (nm.bX - nm.bMinX) * (nm.bMaxZ - nm.bMinZ + 1) + (nm.bZ - nm.bMinZ)
@@ -705,7 +704,8 @@
 end
 
 function init()
-    bodyHandle = FindBody(bodyTag)
+
+  bodyHandle = FindBody(bodyTag)
     if bodyHandle == 0 then return end
     spriteHandle = LoadSprite(spritePath)
     aboveTimer = 0.0
@@ -728,7 +728,9 @@
     end
 end
 
-local function handleSounds(pos)
+local function h
+
+dleSounds(pos)
     local farTarget, nearTarget = 0.0, 0.0
     if visualFade > 0.02 then
         farTarget, nearTarget = 0.75 * backgroundLoopVolumeMul, 0.75
@@ -739,7 +741,9 @@
     PlayLoop(nearLoop, pos, nearFade * nearMaxVol, false)
 end
 
-function breakNearbyLights()
+function breakNe
+
+byLights()
     local lights = FindLights(lightTag, true)
     local bodyPos = TransformToParentPoint(GetBodyTransform(bodyHandle), GetBodyCenterOfMass(bodyHandle))
     for i = 1, #lights do
@@ -767,14 +771,16 @@
     end
 end
 
-local function tryPlayMainSound(pos)
+local function t
+
+PlayMainSound(pos)
     if not mainSoundLoaded then return end
     if mainSoundSequential then
         if IsSoundPlaying(mainSoundHandle) then return end
         mainSoundHandle = PlaySound(mainSoundLoaded, pos, mainSoundVolume, false)
         mainSoundStartTime = GetTime()
     else
-        if mainSoundTimer > 0 then return end
+        if mainSoundTimer ~= 0 then return end
         local roll = math.random(mainSoundChanceMin, mainSoundChanceMax)
         if roll == mainSoundChanceMin then
             mainSoundHandle = PlaySound(mainSoundLoaded, pos, mainSoundVolume, false)
@@ -783,7 +789,8 @@
     end
 end
 
-function tick(dt)
+function tick(dt
+
 	--[[
     buildTick()
     dynamicCheckTick()
@@ -798,7 +805,7 @@
             local bt = GetBodyTransform(bodyHandle)
             rebuildPos = TransformToParentPoint(bt, GetBodyCenterOfMass(bodyHandle))
         else
-            rebuildPos = GetPlayerPos()
+            rebuildPos = GetPlayerPos(playerId)
         end
         StartNavMeshBuild(rebuildPos, CFG.scanRadius)
         navPath = nil
@@ -812,7 +819,7 @@
         local hit, dist = QueryRaycast(cam.pos, fwd, 150)
         if hit then
             goalPos = VecAdd(cam.pos, VecScale(fwd, dist))
-            rawPath = NavMeshQuery(GetPlayerPos(), goalPos)
+            rawPath = NavMeshQuery(GetPlayerPos(playerId), goalPos)
             navPath = smoothPath(rawPath)
             local wp = navPath and #navPath or 0
             local rp = rawPath and #rawPath or 0
@@ -851,7 +858,7 @@
             pathTimer = 0.0
             local bt = GetBodyTransform(bodyHandle)
             local npcPos = TransformToParentPoint(bt, GetBodyCenterOfMass(bodyHandle))
-            local playerPos = GetPlayerTransform().pos
+            local playerPos = GetPlayerTransform(playerId).pos
             rawPath = NavMeshQuery(npcPos, playerPos)
             navPath = smoothPath(rawPath)
             goalPos = playerPos
@@ -870,7 +877,7 @@
     end
 
     local t = GetBodyTransform(bodyHandle)
-    local playerPos = GetPlayerTransform().pos
+    local playerPos = GetPlayerTransform(playerId).pos
     local bodyCenter = TransformToParentPoint(t, GetBodyCenterOfMass(bodyHandle))
     local closestPos = playerPos
     local closestDist = VecDist(bodyCenter, playerPos)
@@ -909,7 +916,7 @@
         end
     end
 
-    if not mainSoundSequential and mainSoundTimer > 0 then mainSoundTimer = mainSoundTimer - 1 end
+    if not mainSoundSequential and mainSoundTimer ~= 0 then mainSoundTimer = mainSoundTimer - 1 end
     tryPlayMainSound(t.pos)
 
     if bodyHandle == 0 or not IsHandleValid(bodyHandle) then return end
@@ -938,43 +945,5 @@
 end
 
 --[[
-function update(dt)
-    if bodyHandle == 0 or not IsHandleValid(bodyHandle) then return end
-    if not HasTag(bodyHandle, bodyTag) then return end
-    if not IsBodyDynamic(bodyHandle) then SetBodyDynamic(bodyHandle, true) end
-    if not navPath or #navPath < 2 then return end
-
-    local bt = GetBodyTransform(bodyHandle)
-    local bodyCenter = TransformToParentPoint(bt, GetBodyCenterOfMass(bodyHandle))
-
-    if npcWaypointIdx > #navPath then npcWaypointIdx = #navPath end
-
-    local target = navPath[npcWaypointIdx]
-    local toTarget = VecSub(target, bodyCenter)
-    local flatDist = math.sqrt(toTarget[1]*toTarget[1] + toTarget[3]*toTarget[3])
-
-    if flatDist < CFG.waypointReachDist and npcWaypointIdx < #navPath then
-        npcWaypointIdx = npcWaypointIdx + 1
-        target = navPath[npcWaypointIdx]
-        toTarget = VecSub(target, bodyCenter)
-        flatDist = math.sqrt(toTarget[1]*toTarget[1] + toTarget[3]*toTarget[3])
-    end
-
-    local moveTarget = Vec(
-        bodyCenter[1] + toTarget[1],
-        target[2],
-        bodyCenter[3] + toTarget[3]
-    )
-
-    ConstrainPosition(bodyHandle, 0, bodyCenter, VecAdd(moveTarget,Vec(0, 1.7, 0)), CFG.constrainMaxVel, CFG.constrainMaxImpulse)
-
-    if flatDist > 0.1 then
-        npcMoveDir = Vec(toTarget[1] / flatDist, 0, toTarget[3] / flatDist)
-    end
-
-    local targetRot = QuatLookAt(Vec(0,0,0), npcMoveDir)
-    local uprightRot = QuatAlignXZ(Vec(0,1,0), npcMoveDir)
-    ConstrainOrientation(bodyHandle, 0, bt.rot, uprightRot, CFG.rotMaxVel, CFG.rotMaxImpulse)
-	
-	SetShapeCollisionFilter(FindShape(""), 0, 0)
-end --]]+function update(d
+

```

---

# Migration Report: NPC_POTION_EFFECT.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/NPC_POTION_EFFECT.lua
+++ patched/NPC_POTION_EFFECT.lua
@@ -1,3 +1,4 @@
+#version 2
 local potion_data = {
     body = 0,
     spawned = false,
@@ -6,7 +7,6 @@
     broken = false,
     effect_transform = nil
 }
-
 local speed_potion = GetBoolParam("speed_potion", false)
 local jump_potion = GetBoolParam("jump_potion", false)
 local poison_potion = GetBoolParam("poison_potion", false)
@@ -19,104 +19,6 @@
 local nausea_potion = GetBoolParam("nausea_potion", false)
 local paint_potion = GetBoolParam("paint_potion", false)
 
-function init()
-    local b = FindBody("NPC_VOXBOX_EFFECT")
-    while b ~= 0 do
-        Delete(b)
-        b = FindBody("NPC_VOXBOX_EFFECT")
-    end
-    potion_data.body = FindBody("NPC_POTION_EFFECT")
-end
-
-function tick()
-    local current_time = GetTime()
-    
-    if not IsHandleValid(potion_data.body) then
-        if #potion_data.voxboxes > 0 and potion_data.effect_transform then
-            local elapsed = current_time - potion_data.spawn_time
-            
-            if elapsed < 5 then
-                spawnContinuousParticles(potion_data.effect_transform)
-            end
-            
-            if elapsed >= 5 then
-                spawnParticleBurst(potion_data.effect_transform)
-                
-                for i = 1, #potion_data.voxboxes do
-                    local voxbox = potion_data.voxboxes[i]
-                    if IsHandleValid(voxbox) then
-                        Delete(voxbox)
-                    end
-                end
-                potion_data.voxboxes = {}
-                potion_data.effect_transform = nil
-            end
-        end
-        return
-    end
-    
-    if IsBodyBroken(potion_data.body) then
-        potion_data.broken = true
-    end
-    
-    if not potion_data.spawned and potion_data.broken then
-        potion_data.spawned = true
-        
-        local body_transform = GetBodyTransform(potion_data.body)
-        potion_data.effect_transform = TransformCopy(body_transform)
-        
-        local effects = getActiveEffects()
-        
-        for i = 1, #effects do
-            local effect = effects[i]
-            local tags = "invisible nocull NPC_VOXBOX_EFFECT " .. effect.tag
-            
-            local xml = '<script file="MOD/DESPAWNPOTIONEFFECT.lua"><body dynamic="false" tags="' .. tags .. '"><voxbox size="10 10 10" pos="-0.5 -0.5 -0.5" material="glass" tags="' .. tags .. '" collide="false"/></body></script>'
-            local voxbox_body = Spawn(xml, potion_data.effect_transform, true, false)
-            
-            if voxbox_body ~= 0 and IsHandleValid(voxbox_body) then
-                local shapes = GetBodyShapes(voxbox_body)
-                for j = 1, #shapes do
-                    SetShapeCollisionFilter(shapes[j], 255, 0)
-                end
-                
-                local voxbox_pos = potion_data.effect_transform.pos
-                PaintRGBA(voxbox_pos, 0.5, effect.color[1], effect.color[2], effect.color[3], 1.0, 1.0)
-                
-                table.insert(potion_data.voxboxes, voxbox_body)
-            end
-        end
-        
-        potion_data.spawn_time = current_time
-        
-        spawnParticleBurst(potion_data.effect_transform)
-        
-        Delete(potion_data.body)
-        potion_data.body = 0
-    end
-    
-    if #potion_data.voxboxes > 0 and potion_data.effect_transform then
-        local elapsed = current_time - potion_data.spawn_time
-        
-        if elapsed < 3 then
-            spawnContinuousParticles(potion_data.effect_transform)
-        end
-        
-        if elapsed >= 3 then
-            spawnParticleBurst(potion_data.effect_transform)
-            
-            for i = 1, #potion_data.voxboxes do
-                local voxbox = potion_data.voxboxes[i]
-                if IsHandleValid(voxbox) then
-                    Delete(voxbox)
-                end
-            end
-            potion_data.voxboxes = {}
-            potion_data.effect_transform = nil
-        end
-    end
-end
-
 function getActiveEffects()
     local effects = {}
     
@@ -279,51 +181,147 @@
     end
 end
 
-function draw()
+function server.init()
+    local b = FindBody("NPC_VOXBOX_EFFECT")
+    while b ~= 0 do
+        Delete(b)
+        b = FindBody("NPC_VOXBOX_EFFECT")
+    end
+    potion_data.body = FindBody("NPC_POTION_EFFECT")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local current_time = GetTime()
+        if not IsHandleValid(potion_data.body) then
+            if #potion_data.voxboxes > 0 and potion_data.effect_transform then
+                local elapsed = current_time - potion_data.spawn_time
+
+                if elapsed < 5 then
+                    spawnContinuousParticles(potion_data.effect_transform)
+                end
+
+                if elapsed >= 5 then
+                    spawnParticleBurst(potion_data.effect_transform)
+
+                    for i = 1, #potion_data.voxboxes do
+                        local voxbox = potion_data.voxboxes[i]
+                        if IsHandleValid(voxbox) then
+                            Delete(voxbox)
+                        end
+                    end
+                    potion_data.voxboxes = {}
+                    potion_data.effect_transform = nil
+                end
+            end
+            return
+        end
+        if IsBodyBroken(potion_data.body) then
+            potion_data.broken = true
+        end
+        if not potion_data.spawned and potion_data.broken then
+            potion_data.spawned = true
+
+            local body_transform = GetBodyTransform(potion_data.body)
+            potion_data.effect_transform = TransformCopy(body_transform)
+
+            local effects = getActiveEffects()
+
+            for i = 1, #effects do
+                local effect = effects[i]
+                local tags = "invisible nocull NPC_VOXBOX_EFFECT " .. effect.tag
+
+                local xml = '<script file="MOD/DESPAWNPOTIONEFFECT.lua"><body dynamic="false" tags="' .. tags .. '"><voxbox size="10 10 10" pos="-0.5 -0.5 -0.5" material="glass" tags="' .. tags .. '" collide="false"/></body></script>'
+                local voxbox_body = Spawn(xml, potion_data.effect_transform, true, false)
+
+                if voxbox_body ~= 0 and IsHandleValid(voxbox_body) then
+                    local shapes = GetBodyShapes(voxbox_body)
+                    for j = 1, #shapes do
+                        SetShapeCollisionFilter(shapes[j], 255, 0)
+                    end
+
+                    local voxbox_pos = potion_data.effect_transform.pos
+                    PaintRGBA(voxbox_pos, 0.5, effect.color[1], effect.color[2], effect.color[3], 1.0, 1.0)
+
+                    table.insert(potion_data.voxboxes, voxbox_body)
+                end
+            end
+
+            potion_data.spawn_time = current_time
+
+            spawnParticleBurst(potion_data.effect_transform)
+
+            Delete(potion_data.body)
+            potion_data.body = 0
+        end
+        if #potion_data.voxboxes > 0 and potion_data.effect_transform then
+            local elapsed = current_time - potion_data.spawn_time
+
+            if elapsed < 3 then
+                spawnContinuousParticles(potion_data.effect_transform)
+            end
+
+            if elapsed >= 3 then
+                spawnParticleBurst(potion_data.effect_transform)
+
+                for i = 1, #potion_data.voxboxes do
+                    local voxbox = potion_data.voxboxes[i]
+                    if IsHandleValid(voxbox) then
+                        Delete(voxbox)
+                    end
+                end
+                potion_data.voxboxes = {}
+                potion_data.effect_transform = nil
+            end
+        end
+    end
+end
+
+function client.draw()
     if not IsHandleValid(potion_data.body) then
         return
     end
-    
+
     if potion_data.broken then
         return
     end
-    
+
     local transform = GetBodyTransform(potion_data.body)
     local cam_transform = GetCameraTransform()
-    
+
     local to_object = VecNormalize(VecSub(transform.pos, cam_transform.pos))
     local cam_forward = TransformToParentVec(cam_transform, Vec(0, 0, -1))
     local dot = VecDot(to_object, cam_forward)
-    
+
     if dot < 0.3 then
         return
     end
-    
+
     local distance = VecLength(VecSub(transform.pos, cam_transform.pos))
-    
+
     if distance > 25 then
         return
     end
-    
+
     local text_pos = VecAdd(transform.pos, Vec(0, 0.7, 0))
     local text_rot = QuatLookAt(text_pos, cam_transform.pos)
     local text_transform = Transform(text_pos, text_rot)
-    
+
     local effects = getActiveEffects()
     local r, g, b = 0.5, 0.5, 0.5
-    if #effects > 0 then
+    if #effects ~= 0 then
         r, g, b = effects[1].color[1], effects[1].color[2], effects[1].color[3]
     end
-    
+
     local name = getPotionName()
     local alpha = math.min(1.0, (25 - distance) / 25)
-    
+
     UiPush()
         UiTranslate(UiCenter(), UiMiddle())
         local x, y = UiWorldToPixel(text_pos)
         if x then
             UiTranslate(x, y)
-            
+
             UiPush()
                 UiColor(0, 0, 0, alpha * 0.7)
                 UiAlign("center middle")
@@ -331,7 +329,7 @@
                 UiFont("bold.ttf", 26)
                 UiText(name)
             UiPop()
-            
+
             UiPush()
                 UiColor(r, g, b, alpha)
                 UiAlign("center middle")
@@ -341,3 +339,4 @@
         end
     UiPop()
 end
+

```

---

# Migration Report: NPC_SPAWNER.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/NPC_SPAWNER.lua
+++ patched/NPC_SPAWNER.lua
@@ -1,9 +1,9 @@
+#version 2
 local enabled = false
 local spawnInterval = 0.5
 local timer = 0
 local maxNPCs = 200
 local spawnerBody
-
 local npcFiles = {
 	"MOD/characters/player/player_billy_bones_jones.xml",
 	"MOD/characters/player/player_chris_seabranch.xml",
@@ -25,36 +25,6 @@
 	"MOD/characters/player/player_parisa.xml",
 	"MOD/characters/player/player_sven_lagom.xml",
 }
-
-weaponsFiles = {
-	"MOD/prefab/NPC_Weapon_shooter.xml",
-	"MOD/prefab/NPC_Weapon_shooter_2.xml",
-	"MOD/prefab/NPC_Weapon_shooter_3.xml",
-	"MOD/prefab/NPC_Weapon_sledge.xml",
-}
-
-nextbotFiles = {
-	"MOD/characters/player/WeirdMario.xml",
-	"MOD/characters/player/Rush.xml",
-	"MOD/characters/player/PretzelNextbot.xml",
-	"MOD/characters/player/AngryMunciNextbot.xml",
-	"MOD/characters/player/SteveNextbot.xml",
-}
-
-potionFiles = {
-	"MOD/prefab/POTION_FIRE.xml",
-	"MOD/prefab/POTION_IMMORTAL.xml",
-	"MOD/prefab/POTION_JUMP.xml",
-	"MOD/prefab/POTION_LOWGRAV.xml",
-	"MOD/prefab/POTION_NAUSEA.xml",
-	"MOD/prefab/POTION_PAINT.xml",
-	"MOD/prefab/POTION_POISON.xml",
-	"MOD/prefab/POTION_RAGDOLL.xml",
-	"MOD/prefab/POTION_SLOWNESS.xml",
-	"MOD/prefab/POTION_SPEED.xml",
-	"MOD/prefab/POTION_UNZOMBIE.xml",
-}
-
 local baseMaxTime = 1
 local perSpawnerIncrease = 1
 local maxTimerCap = 50
@@ -63,76 +33,78 @@
 	return a + math.random() * (b - a)
 end
 
-function init()
-	spawnerBody = FindBody("NPC_SPAWNER_BODY")
-	if type(weaponsFiles) ~= "table" then weaponsFiles = {} end
+function server.init()
+    spawnerBody = FindBody("NPC_SPAWNER_BODY")
+    if type(weaponsFiles) ~= "table" then weaponsFiles = {} end
 end
 
-function tick(dt)
-	if InputPressed("f2") then
-		enabled = not enabled
-		if spawnerBody then SetBodyDynamic(spawnerBody, not enabled) end
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("f2") then
+    	enabled = not enabled
+    	if spawnerBody then SetBodyDynamic(spawnerBody, not enabled) end
+    end
 
-	if not enabled or not spawnerBody then return end
+    if not enabled or not spawnerBody then return end
 
-	timer = timer - dt
-	if timer > 0 then return end
+    timer = timer - dt
+    if timer ~= 0 then return end
 
-	local bodies = FindBodies("npc_base", true)
-	if #bodies >= maxNPCs then
-		timer = spawnInterval
-		return
-	end
+    local bodies = FindBodies("npc_base", true)
+    if #bodies >= maxNPCs then
+    	timer = spawnInterval
+    	return
+    end
 
-	local tr = GetBodyTransform(spawnerBody)
+    local tr = GetBodyTransform(spawnerBody)
 
-	if not HasTag(spawnerBody, "NO_NPC_SPAWN") then
-		local npc_choice
-		if HasTag(spawnerBody, "NPC_SPAWNER_NEXTBOTS") then
-			npc_choice = nextbotFiles[math.random(1, #nextbotFiles)]
-		else
-			npc_choice = npcFiles[math.random(1, #npcFiles)]
-		end
-		local spawned = Spawn(npc_choice, tr)
-		
-		local npc_list = {}
-		if type(spawned) == "table" then
-			npc_list = spawned
-		elseif spawned and spawned ~= 0 then
-			npc_list = { spawned }
-		end
+    if not HasTag(spawnerBody, "NO_NPC_SPAWN") then
+    	local npc_choice
+    	if HasTag(spawnerBody, "NPC_SPAWNER_NEXTBOTS") then
+    		npc_choice = nextbotFiles[math.random(1, #nextbotFiles)]
+    	else
+    		npc_choice = npcFiles[math.random(1, #npcFiles)]
+    	end
+    	local spawned = Spawn(npc_choice, tr)
 
-		for _, ent in ipairs(npc_list) do
-			if ent and ent ~= 0 then
-				if HasTag(spawnerBody, "NPC_SPAWNER_ZOMBIE_MODE") then SetTag(ent, "NPC_ZOMBIE_MODE") end
-				if HasTag(spawnerBody, "TEAM_RED") then SetTag(ent, "TEAM_RED") end
-				if HasTag(spawnerBody, "TEAM_BLUE") then SetTag(ent, "TEAM_BLUE") end
-			end
-		end
-	end
-	
-	if HasTag(spawnerBody, "NPC_SPAWNER_POTIONS") and type(potionFiles) == "table" and #potionFiles > 0 then
-		local potion_choice = potionFiles[math.random(1, #potionFiles)]
-		local potion_tr = GetBodyTransform(spawnerBody)
-		potion_tr.pos = VecAdd(potion_tr.pos, Vec(0, 1.0, 0))
-		Spawn(potion_choice, potion_tr)
-	end
+    	local npc_list = {}
+    	if type(spawned) == "table" then
+    		npc_list = spawned
+    	elseif spawned and spawned ~= 0 then
+    		npc_list = { spawned }
+    	end
 
-	if HasTag(spawnerBody, "NPC_SPAWNER_WEAPONS") and type(weaponsFiles) == "table" and #weaponsFiles > 0 then
-		local weapon_choice = weaponsFiles[math.random(1, #weaponsFiles)]
-		local weapon_tr = GetBodyTransform(spawnerBody)
-		weapon_tr.pos = VecAdd(weapon_tr.pos, Vec(0, 1.0, 0))
-		Spawn(weapon_choice, weapon_tr)
-	end
+    	for _, ent in ipairs(npc_list) do
+    		if ent and ent ~= 0 then
+    			if HasTag(spawnerBody, "NPC_SPAWNER_ZOMBIE_MODE") then SetTag(ent, "NPC_ZOMBIE_MODE") end
+    			if HasTag(spawnerBody, "TEAM_RED") then SetTag(ent, "TEAM_RED") end
+    			if HasTag(spawnerBody, "TEAM_BLUE") then SetTag(ent, "TEAM_BLUE") end
+    		end
+    	end
+    end
 
-	local spawner_list = FindBodies("NPC_SPAWNER_BODY", true) or {}
-	local spawner_count = #spawner_list
-	if spawner_count < 1 then spawner_count = 1 end
+    if HasTag(spawnerBody, "NPC_SPAWNER_POTIONS") and type(potionFiles) == "table" and #potionFiles ~= 0 then
+    	local potion_choice = potionFiles[math.random(1, #potionFiles)]
+    	local potion_tr = GetBodyTransform(spawnerBody)
+    	potion_tr.pos = VecAdd(potion_tr.pos, Vec(0, 1.0, 0))
+    	Spawn(potion_choice, potion_tr)
+    end
 
-	local baseRandom = randFloat(spawnInterval, baseMaxTime)
+    if HasTag(spawnerBody, "NPC_SPAWNER_WEAPONS") and type(weaponsFiles) == "table" and #weaponsFiles ~= 0 then
+    	local weapon_choice = weaponsFiles[math.random(1, #weaponsFiles)]
+    	local weapon_tr = GetBodyTransform(spawnerBody)
+    	weapon_tr.pos = VecAdd(weapon_tr.pos, Vec(0, 1.0, 0))
+    	Spawn(weapon_choice, weapon_tr)
+    end
 
-	local multiplier = 1 + (spawner_count - 1) * perSpawnerIncrease
-	
-	timer = math.min(baseRandom * multiplier, maxTimerCap)
+    local spawner_list = FindBodies("NPC_SPAWNER_BODY", true) or {}
+    local spawner_count = #spawner_list
+    if spawner_count < 1 then spawner_count = 1 end
+
+    local baseRandom = randFloat(spawnInterval, baseMaxTime)
+
+    local multiplier = 1 + (spawner_count - 1) * perSpawnerIncrease
+
+    timer = math.min(baseRandom * multiplier, maxTimerCap)
 end
+

```

---

# Migration Report: NPC_SPAWNEROLD.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/NPC_SPAWNEROLD.lua
+++ patched/NPC_SPAWNEROLD.lua
@@ -1,9 +1,9 @@
+#version 2
 local enabled = false
 local spawnInterval = 0.05
 local timer = 0
 local maxNPCs = 200
 local spawnerBody
-
 local npcFiles = {
 	"MOD/characters/player/player_billy_bones_jones.xml",
 	"MOD/characters/player/player_chris_seabranch.xml",
@@ -26,64 +26,58 @@
 	"MOD/characters/player/player_sven_lagom.xml",
 }
 
-weaponsFiles = {
-	"MOD/prefab/NPC_Weapon_shooter.xml",
-	"MOD/prefab/NPC_Weapon_shooter_2.xml",
-	"MOD/prefab/NPC_Weapon_shooter_3.xml",
-	"MOD/prefab/NPC_Weapon_sledge.xml",
-}
-
-function init()
-	spawnerBody = FindBody("NPC_SPAWNER_BODY")
-	if type(weaponsFiles) ~= "table" then weaponsFiles = {} end
+function server.init()
+    spawnerBody = FindBody("NPC_SPAWNER_BODY")
+    if type(weaponsFiles) ~= "table" then weaponsFiles = {} end
 end
 
-function tick(dt)
-	if InputPressed("f2") then
-		enabled = not enabled
-		if spawnerBody then SetBodyDynamic(spawnerBody, not enabled) end
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("f2") then
+    	enabled = not enabled
+    	if spawnerBody then SetBodyDynamic(spawnerBody, not enabled) end
+    end
 
-	if not enabled or not spawnerBody then return end
+    if not enabled or not spawnerBody then return end
 
-	timer = timer - dt
-	if timer > 0 then return end
+    timer = timer - dt
+    if timer ~= 0 then return end
 
-	local bodies = FindBodies("npc_base", true)
-	if #bodies >= maxNPCs then
-		timer = spawnInterval
-		return
-	end
+    local bodies = FindBodies("npc_base", true)
+    if #bodies >= maxNPCs then
+    	timer = spawnInterval
+    	return
+    end
 
-	local tr = GetBodyTransform(spawnerBody)
+    local tr = GetBodyTransform(spawnerBody)
 
-	if not HasTag(spawnerBody, "NO_NPC_SPAWN") then
-		local npc_choice = npcFiles[math.random(1, #npcFiles)]
-		local spawned = Spawn(npc_choice, tr)
-		
-		local npc_list = {}
-		if type(spawned) == "table" then
-			npc_list = spawned
-		elseif spawned and spawned ~= 0 then
-			npc_list = { spawned }
-		end
+    if not HasTag(spawnerBody, "NO_NPC_SPAWN") then
+    	local npc_choice = npcFiles[math.random(1, #npcFiles)]
+    	local spawned = Spawn(npc_choice, tr)
 
-		for _, ent in ipairs(npc_list) do
-			if ent and ent ~= 0 then
-				if HasTag(spawnerBody, "NPC_SPAWNER_ZOMBIE_MODE") then SetTag(ent, "NPC_ZOMBIE_MODE") end
-				if HasTag(spawnerBody, "TEAM_RED") then SetTag(ent, "TEAM_RED") end
-				if HasTag(spawnerBody, "TEAM_BLUE") then SetTag(ent, "TEAM_BLUE") end
-			end
-		end
-	end
+    	local npc_list = {}
+    	if type(spawned) == "table" then
+    		npc_list = spawned
+    	elseif spawned and spawned ~= 0 then
+    		npc_list = { spawned }
+    	end
 
+    	for _, ent in ipairs(npc_list) do
+    		if ent and ent ~= 0 then
+    			if HasTag(spawnerBody, "NPC_SPAWNER_ZOMBIE_MODE") then SetTag(ent, "NPC_ZOMBIE_MODE") end
+    			if HasTag(spawnerBody, "TEAM_RED") then SetTag(ent, "TEAM_RED") end
+    			if HasTag(spawnerBody, "TEAM_BLUE") then SetTag(ent, "TEAM_BLUE") end
+    		end
+    	end
+    end
 
-	if HasTag(spawnerBody, "NPC_SPAWNER_WEAPONS") and type(weaponsFiles) == "table" and #weaponsFiles > 0 then
-		local weapon_choice = weaponsFiles[math.random(1, #weaponsFiles)]
-		local weapon_tr = GetBodyTransform(spawnerBody)
-		weapon_tr.pos = VecAdd(weapon_tr.pos, Vec(0, 1.0, 0))
-		Spawn(weapon_choice, weapon_tr)
-	end
+    if HasTag(spawnerBody, "NPC_SPAWNER_WEAPONS") and type(weaponsFiles) == "table" and #weaponsFiles ~= 0 then
+    	local weapon_choice = weaponsFiles[math.random(1, #weaponsFiles)]
+    	local weapon_tr = GetBodyTransform(spawnerBody)
+    	weapon_tr.pos = VecAdd(weapon_tr.pos, Vec(0, 1.0, 0))
+    	Spawn(weapon_choice, weapon_tr)
+    end
 
-	timer = spawnInterval + math.random(-0.04, 50)
-end+    timer = spawnInterval + math.random(-0.04, 50)
+end
+

```

---

# Migration Report: NPC_ZOMBIE_VIRUS.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/NPC_ZOMBIE_VIRUS.lua
+++ patched/NPC_ZOMBIE_VIRUS.lua
@@ -1,29 +1,33 @@
-function tick(dt)
-	local src = FindBody("NPC_BACTERIA")
-	if src == 0 then return end
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local src = FindBody("NPC_BACTERIA")
+        if src == 0 then return end
 
-	local spos = GetBodyTransform(src).pos
-	local bodies = FindBodies("npc_base", true)
+        local spos = GetBodyTransform(src).pos
+        local bodies = FindBodies("npc_base", true)
 
-	for i = 1, #bodies do
-		local b = bodies[i]
-		local bpos = GetBodyTransform(b).pos
-		local dist = VecLength(VecSub(bpos, spos))
+        for i = 1, #bodies do
+        	local b = bodies[i]
+        	local bpos = GetBodyTransform(b).pos
+        	local dist = VecLength(VecSub(bpos, spos))
 
-		if dist < 1.5 then
-			if HasTag(src, "TEAM_BLUE") then
-				SetTag(b, "TEAM_BLUE")
-			end
+        	if dist < 1.5 then
+        		if HasTag(src, "TEAM_BLUE") then
+        			SetTag(b, "TEAM_BLUE")
+        		end
 
-			if HasTag(src, "TEAM_RED") then
-				SetTag(b, "TEAM_RED")
-			end
+        		if HasTag(src, "TEAM_RED") then
+        			SetTag(b, "TEAM_RED")
+        		end
 
-			if HasTag(src, "NPC_BACTERIA") then
-				if not HasTag(src, "TEAM_BLUE") and not HasTag(src, "TEAM_RED") and not HasTag(b, "NPC_NOINFECTABLE") then
-					SetTag(b, "NPC_ZOMBIE_MODE")
-				end
-			end
-		end
-	end
+        		if HasTag(src, "NPC_BACTERIA") then
+        			if not HasTag(src, "TEAM_BLUE") and not HasTag(src, "TEAM_RED") and not HasTag(b, "NPC_NOINFECTABLE") then
+        				SetTag(b, "NPC_ZOMBIE_MODE")
+        			end
+        		end
+        	end
+        end
+    end
 end
+

```

---

# Migration Report: PlayerAiTest.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/PlayerAiTest.lua
+++ patched/PlayerAiTest.lua
@@ -1,3 +1,4 @@
+#version 2
 local CONFIG = {
     tags = {
         npc = "",
@@ -86,7 +87,6 @@
         fade_slow = 0.35
     }
 }
-
 local State = {
     npc_animator = 0,
     base_body = 0,
@@ -160,7 +160,6 @@
     disable_ai = false,
     disable_hear = false
 }
-
 local AnimCtrl = {
     crouch = 0.0,
     jump_falling = 0.0,
@@ -170,8 +169,200 @@
     last_local_vel = Vec(0,0,0),
     last_pos = Vec(0,0,0)
 }
-
 local _QueryRaycast = QueryRaycast
+local FaceManager = {
+    tags = {"Neutral", "Blink", "Angry", "Happy", "Surprised", "Fall", "Look", "Lookr", "Lookl"},
+    next_face = nil,
+    last_applied = nil
+}
+local SoundSystem = {
+    material_folders = {
+        wood = "wood", masonry = "masonry", metal = "metal",
+        glass = "glass", plastic = "plastic", foliage = "foliage",
+        dirt = "dirt", snow = "snow", water = "water", ice = "ice"
+    },
+    step_phase = 0.0,
+    STEP_TRIGGER_A = 0.25,
+    STEP_TRIGGER_B = 0.75,
+    last_trigger_a = false,
+    last_trigger_b = false,
+}
+local FallDamage = {
+    last_fall_velocity = 0,
+    fall_threshold = -15.0,
+    damage_multiplier = 0.15,
+    min_damage_hole = 0.1,
+    max_damage_hole = 0.5
+}
+local MovementController = {
+    steer_dir = Vec(0, 0, 1),
+    steer_target_dir = Vec(0, 0, 1),
+    steer_fade = 0.0,
+    speed_fade = 0.0,
+    move_dir_smoothed = Vec(0, 0, 0),
+    speed_smoothed = 0,
+    brake_fade = 0.0,
+    target_speed = 0.
+}
+local ObstaclePush = {
+    probe_len = 1,
+    num_rays = 3,
+    spread = 1.2,
+    layer_heights = {0.3, 0.75, 1.35},
+    large_size = 40.0,
+    large_mass = 60.0
+}
+local FIRE_AVOID_RADIUS = 3.5
+local FIRE_AVOID_MAX_STRENGTH = 5.0
+local FIRE_PANIC_RADIUS = 1.0
+local nauseaCount = 0
+local PathfindingManager = {
+    active_paths = {}
+}
+cal VehicleState = {
+    handle = 0,
+    body = 0,
+    in_vehicle = false,
+    exit_cooldown = 0.0,
+    last_vel = Vec(0, 0, 0),
+    impact_dv_threshold = 8.0,
+    entry_range = 3.2,
+    seat_local = Vec(0.0, 0.5, 0.05),
+    wheel_local = Vec(0.0, 1.0, 0.62),
+    lfoot_local = Vec(-0.18, 0.0, 0.68),
+    rfoot_local = Vec(0.12, 0.0, 0.60),
+}
+
+cal WeaponState = {
+    held_gun = 0,
+    is_holding_gun = false,
+    gun_grip_strength = 0,
+    gun_aim_mode = false,
+    gun_shoot_cooldown = 0,
+    gun_shoot_delay = 0.35,
+    gun_target = nil,
+    player_aggro = false,
+    player_aggro_timer = 0,
+    
+    held_melee = 0,
+    is_holding_melee = false,
+    melee_grip_strength = 0,
+    melee_swing_stroke = 0.0,
+    melee_swing_hit = false,
+    melee_attack_cooldown = 0,
+    melee_attack_delay = 0.6,
+    melee_target = nil,
+    
+    last_scan_time = 0,
+    scan_interval = 0.2,
+    
+    rest_transform = Transform(Vec(0.35, 1.10, 0.40),QuatEuler(15, 10, -160)),
+    swing_start_transform = Transform(Vec(0.25, 1.60, 0.5),QuatEuler(70, 30.0, -170)),
+    swing_end_transform = Transform(Vec(0.40, 0.65, 0.50),QuatEuler(-40, 40, 165)),
+    
+    SWING_UP = 0.2,
+    SWING_DOWN = 0.3,
+    HIT_THRESHOLD = 0.45,
+    ATTACK_RANGE = 4.0,
+    SWING_SPEED_NORMAL = 2.45,
+    SWING_SPEED_HIT = 1.3
+}
+
+cal SOUND_EXPOSE_INTERVAL = 0.1
+
+cal __wander_mem = {}
+
+cal TeamCombat = {damage_registry = {}}
+
+cal __combat_mem = {}
+
+cal FlashlightState = {
+    light = 0,
+    is_on = false,
+    target_on = false,
+    switch_timer = 0,
+    cache_timer = 0,
+    all_lights_cache = {}
+}
+
+cal FL_DARK_THRESHOLD = 0.30
+l
+cal FL_SWITCH_DELAY = 0.5
+l
+cal FL_LIGHT_CACHE_INT = 2.0
+l
+cal FL_SUN_RAY_DIST = 400
+l
+cal FL_LIGHT_BASE_RANGE = 6.0
+l
+cal FL_SUN_NIGHT = 0.15
+l
+cal FL_SUN_DIM = 0.45
+l
+cal FL_RAIN_THRESH = 0.05
+l
+cal FL_SNOW_THRESH = 0.05
+
+cal NPCFlashlight = {
+    is_on = false,
+    target_on = false,
+    switch_timer = 0,
+    cache_timer = 0,
+    all_lights_cache = {},
+    intensity = 0.0,
+    head_pos = nil,
+    forward = nil
+}
+
+cal __zombie_mem = {}
+
+cal __follow_mem = {}
+
+cal _orig_updateAI = updateAI
+f
+cal _throttle = {
+    offset = math.random() * 0.25,
+    ai_next = 0,
+    ground_next = 0,
+    dead_next = 0,
+    obs_next = 0,
+    sound_next = 0,
+    wither_next = 0,
+    flashlight_next = 0,
+    radiation_next = 0,
+    potion_next = 0,
+    push_next = 0,
+    weapon_scan_next = 0,
+
+    grounded = false,
+    in_water = false,
+    water_depth = 0,
+    pos = Vec(0,0,0),
+    bt = nil,
+}
+
+cal AI_RATE = 0.0001
+l
+cal GROUND_RATE = 0.05
+l
+cal DEAD_RATE = 0.25
+l
+cal OBS_RATE = 0.05
+l
+cal SOUND_RATE = 0.0001
+l
+cal WITHER_RATE = 0.2
+l
+cal FLASHLIGHT_RATE = 0.2
+l
+cal RADIATION_RATE = 0.15
+l
+cal POTION_RATE = 0.1
+l
+cal PUSH_RATE = 0.08
+l
+cal WEAPON_SCAN_RATE = 0.2
+
 function QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
     local hit, dist, normal, shape = _QueryRaycast(origin, direction, maxDist, radius, rejectTransparent)
 
@@ -237,12 +428,6 @@
     d[2] = 0
     return VecLength(d)
 end
-
-local FaceManager = {
-    tags = {"Neutral", "Blink", "Angry", "Happy", "Surprised", "Fall", "Look", "Lookr", "Lookl"},
-    next_face = nil,
-    last_applied = nil
-}
 
 function FaceManager:set(face_tag)
     self.next_face = face_tag
@@ -336,19 +521,6 @@
     
     return hits >= 3
 end
-
-local SoundSystem = {
-    material_folders = {
-        wood = "wood", masonry = "masonry", metal = "metal",
-        glass = "glass", plastic = "plastic", foliage = "foliage",
-        dirt = "dirt", snow = "snow", water = "water", ice = "ice"
-    },
-    step_phase = 0.0,
-    STEP_TRIGGER_A = 0.25,
-    STEP_TRIGGER_B = 0.75,
-    last_trigger_a = false,
-    last_trigger_b = false,
-}
 
 function SoundSystem:getGroundMaterial()
     if State.base_body == 0 then return "masonry" end
@@ -471,14 +643,6 @@
     end
 end
 
-local FallDamage = {
-    last_fall_velocity = 0,
-    fall_threshold = -15.0,
-    damage_multiplier = 0.15,
-    min_damage_hole = 0.1,
-    max_damage_hole = 0.5
-}
-
 function updateFallDamage(dt)
     if not State.base_body or State.base_body == 0 or State.ragdoll_active then 
         FallDamage.last_fall_velocity = 0
@@ -505,7 +669,7 @@
             local damage_severity = (impact_force - math.abs(FallDamage.fall_threshold)) * FallDamage.damage_multiplier
             damage_severity = clamp(damage_severity, 0, 1.5)
             
-            if damage_severity > 0 then
+            if damage_severity ~= 0 then
                 local impact_pos = VecAdd(bt.pos, Vec(0, 0.1, 0))
                 
                 local hole_size = clamp(
@@ -536,37 +700,6 @@
         FallDamage.last_fall_velocity = 0
     end
 end
-
- PotionState = {
-    speed_boost = 0,
-    jump_boost = 0,
-    poison_timer = 0,
-    slowness_level = 0,
-    ragdoll_potion_timer = 0,
-    ragdoll_potion_active = false,
-    low_gravity_active = false,
-    low_gravity_timer = 0,
-    immortal_active = false,
-    nausea_timer = 0,
-    nausea_offset = Vec(0, 0, 0),
-    paint_timer = 0,
-    paint_hue = 0,
-    checked_blocks = {},
-	ragdoll_potion_timer = 0,
-    ragdoll_potion_active = false,
-    ragdoll_started = false,
-}
-
-local MovementController = {
-    steer_dir = Vec(0, 0, 1),
-    steer_target_dir = Vec(0, 0, 1),
-    steer_fade = 0.0,
-    speed_fade = 0.0,
-    move_dir_smoothed = Vec(0, 0, 0),
-    speed_smoothed = 0,
-    brake_fade = 0.0,
-    target_speed = 0.
-}
 
 function MovementController:steerToward(dir_world, speed_min, speed_max, target_pos, strength, dt)
     if State.base_body == 0 then return end
@@ -824,20 +957,11 @@
     
     local jump_multiplier = PotionState.jump_potion_multiplier or 1.0
     
-    if best_height_diff > 0 then
+    if best_height_diff ~= 0 then
         local push_vel = best_height_diff * 10.5 * jump_multiplier
         ConstrainVelocity(State.base_body, 0, t.pos, Vec(0, 10.5 * jump_multiplier, 0), push_vel * jump_multiplier, 5.5 * jump_multiplier)
     end
 end
-
-local ObstaclePush = {
-    probe_len = 1,
-    num_rays = 3,
-    spread = 1.2,
-    layer_heights = {0.3, 0.75, 1.35},
-    large_size = 40.0,
-    large_mass = 60.0
-}
 
 local function BodyHasTag(body, tag)
     for _, s in ipairs(GetBodyShapes(body)) do
@@ -881,13 +1005,6 @@
         end
     end
 end
-
-local FIRE_AVOID_RADIUS = 3.5
-local FIRE_AVOID_MAX_STRENGTH = 5.0
-local FIRE_PANIC_RADIUS = 1.0
-DEBUG_OBSTACLE = false
-State.current_move_dir = State.current_move_dir or Vec(0,0,0)
-State.sidestep_strength = State.sidestep_strength or 0.0
 
 function MovementController:obstacleAvoidance(dt)
 	if not State.base_body or State.base_body == 0 or OBSTACLE_AVOID_BLOCKED then return end
@@ -965,7 +1082,7 @@
 		return false
 	end
 
-	if fireAvoidDir and fireAvoidStrength > 0 then
+	if fireAvoidDir and fireAvoidStrength ~= 0 then
 		local blend = math.min(fireAvoidStrength / FIRE_AVOID_MAX_STRENGTH, 1.0)
 		moveDir = VecNormalize(VecAdd(
 			VecScale(moveDir, 1.0 - blend * 0.6),
@@ -1016,12 +1133,6 @@
     
     State.ai_state = "falling"
 end
-
-State.radiation_dose = 0
-State.radiation_damage_timer = 0
-State.radiation_paint_timer = 0
-State.radiation_last_check = 0
-State.radiation_sources = {}
 
 local function hueToRGB(hue)
     local h = hue % 360
@@ -1127,7 +1238,7 @@
 end
 
 local function updateSpeedPotion(dt)
-    if PotionState.speed_boost > 0 then
+    if PotionState.speed_boost ~= 0 then
         State.speed_multiplier = (State.speed_multiplier or 1.0) * (1.0 + (PotionState.speed_boost * 0.3))
         PotionState.speed_boost = PotionState.speed_boost - (dt * 0.1)
         if PotionState.speed_boost < 0 then
@@ -1137,7 +1248,7 @@
 end
 
 local function updateJumpPotion(dt)
-    if PotionState.jump_boost > 0 then
+    if PotionState.jump_boost ~= 0 then
         PotionState.jump_boost = PotionState.jump_boost - (dt * 0.1)
         if PotionState.jump_boost < 0 then
             PotionState.jump_boost = 0
@@ -1176,7 +1287,7 @@
 end
 
 local function updatePoisonPotion(dt)
-    if PotionState.poison_timer > 0 then
+    if PotionState.poison_timer ~= 0 then
         PotionState.poison_timer = PotionState.poison_timer - dt
         
         local bt = GetBodyTransform(State.base_body)
@@ -1197,7 +1308,7 @@
 end
 
 local function updateSlownessPotion(dt)
-    if PotionState.slowness_level > 0 then
+    if PotionState.slowness_level ~= 0 then
         State.speed_multiplier = (State.speed_multiplier or 1.0) * (1.0 / (1.0 + (PotionState.slowness_level * 0.3)))
         PotionState.slowness_level = PotionState.slowness_level - (dt * 0.1)
         if PotionState.slowness_level < 0 then
@@ -1244,7 +1355,7 @@
 end
 
 local function updateLowGravityPotion(dt)
-    if PotionState.low_gravity_active and PotionState.low_gravity_timer > 0 then
+    if PotionState.low_gravity_active and PotionState.low_gravity_timer ~= 0 then
         PotionState.low_gravity_timer = PotionState.low_gravity_timer - dt
         
         if State.base_body ~= 0 then
@@ -1263,10 +1374,8 @@
     end
 end
 
-local nauseaCount = 0
-
 local function updateNauseaPotion(dt)
-    if PotionState.nausea_timer > 0 then
+    if PotionState.nausea_timer ~= 0 then
         PotionState.nausea_timer = PotionState.nausea_timer - dt
         
         if not PotionState.nausea_painted then
@@ -1346,7 +1455,7 @@
 end
 
 local function updatePaintPotion(dt)
-    if PotionState.paint_timer > 0 then
+    if PotionState.paint_timer ~= 0 then
         PotionState.paint_timer = PotionState.paint_timer - dt
         PotionState.paint_hue = (PotionState.paint_hue + dt * 120) % 360
         
@@ -1405,15 +1514,6 @@
         end
     end
 end
-
-Pathfinding = {
-    path = {},
-    recovery_mode = false,
-    recovery_target = nil,
-    original_path = {},
-    last_check_pos = nil,
-    deviation_timer = 0
-}
 
 function Pathfinding:samplePath(step)
     step = step or 0.25
@@ -1696,10 +1796,6 @@
     State.path_timeout = timeout or 2.0
 end
 
-local PathfindingManager = {
-    active_paths = {}
-}
-
 function PathfindingManager:moveTo(body, target_pos, speed_min, speed_max, allow_direct)
     if not body or body == 0 or not target_pos then return false end
 
@@ -1834,7 +1930,7 @@
         if st == "done" then
             local pts = samplePlanner(mem.planner_main)
             trimToForward(pts)
-            if #pts > 0 then
+            if #pts ~= 0 then
                 mem.path_pts = pts
             end
             mem.main_busy = false
@@ -1854,7 +1950,7 @@
             mem.detour_busy = false
             mem.detour_timeout = 0
             local detour_pts = samplePlanner(mem.planner_detour)
-            if #detour_pts > 0 then
+            if #detour_pts ~= 0 then
                 if mem.detour_is_recovery then
                     local ti = mem.detour_to_idx
                     local new_pts = {}
@@ -1886,7 +1982,7 @@
         end
     end
 
-    if #mem.path_pts > 0 then
+    if #mem.path_pts ~= 0 then
         local closest_idx = 1
         local closest_dist = math.huge
         local scan = math.min(#mem.path_pts, 32)
@@ -1988,7 +2084,7 @@
 
     if now - mem.last_stuck_time > 2.0 then
         local moved = vecFlatDist(pos, mem.last_stuck_pos)
-        if moved < 0.8 and #mem.path_pts > 0 then
+        if moved < 0.8 and #mem.path_pts ~= 0 then
             mem.stuck_timer = mem.stuck_timer + 2.0
         else
             mem.stuck_timer = 0
@@ -2006,7 +2102,7 @@
         end
     end
 
-    if #mem.path_pts > 0 then
+    if #mem.path_pts ~= 0 then
         local wp = mem.path_pts[1]
         local lookahead = #mem.path_pts > 1 and mem.path_pts[2] or wp
         local blend_dist = VecLength(flatten(VecSub(wp, pos)))
@@ -2042,7 +2138,7 @@
     return false
 end
 
-local function getCrouchTarget()
+cal function getCrouchTarget()
     if State.base_body == 0 then return 0.0 end
     
     local t = GetBodyTransform(State.base_body)
@@ -2063,13 +2159,13 @@
     return clamp(crouch_amount, 0.0, 1.0)
 end
 
-local function ensureIdleBase(animator)
+cal function ensureIdleBase(animator)
     if animator == 0 or animator == nil then return end
     PlayAnimationLoop(animator, CONFIG.animations.main_idle, 1.0)
     SetAnimationClipFade(animator, CONFIG.animations.main_idle, CONFIG.animation.fade_slow, CONFIG.animation.fade_slow)
 end
 
-local function isInWater(body)
+cal function isInWater(body)
     if not body or body == 0 then return false, 0 end
     local bt = GetBodyTransform(body)
     if not bt then return false, 0 end
@@ -2082,31 +2178,17 @@
     return depth > 0.08, depth
 end
 
-local function npcInWater(pos)
+cal function npcInWater(pos)
     return IsPointInWater(VecAdd(pos, Vec(0, 0.8, 0)))
 end
 
-local VehicleState = {
-    handle = 0,
-    body = 0,
-    in_vehicle = false,
-    exit_cooldown = 0.0,
-    last_vel = Vec(0, 0, 0),
-    impact_dv_threshold = 8.0,
-    entry_range = 3.2,
-    seat_local = Vec(0.0, 0.5, 0.05),
-    wheel_local = Vec(0.0, 1.0, 0.62),
-    lfoot_local = Vec(-0.18, 0.0, 0.68),
-    rfoot_local = Vec(0.12, 0.0, 0.60),
-}
-
-local function isVehicleValid(veh)
+cal function isVehicleValid(veh)
     if not veh or veh == 0 then return false end
     local ok = pcall(GetVehicleTransform, veh)
     return ok
 end
 
-local function findNPCVehicle(pos)
+cal function findNPCVehicle(pos)
     local veh = FindVehicle("NPC_VEHICLE", true)
     if not veh or veh == 0 then return 0 end
     local ok, vt = pcall(GetVehicleTransform, veh)
@@ -2117,7 +2199,7 @@
     return 0
 end
 
-local function enterNPCVehicle(veh)
+cal function enterNPCVehicle(veh)
     local vb = GetVehicleBody(veh)
     if not vb or vb == 0 then return end
     VehicleState.handle = veh
@@ -2134,7 +2216,7 @@
     MovementController.speed_fade = 0
 end
 
-local function exitNPCVehicle(fling)
+cal function exitNPCVehicle(fling)
     if not VehicleState.in_vehicle then return end
     local shapes = GetBodyShapes(State.base_body)
     for i = 1, #shapes do
@@ -2154,7 +2236,7 @@
     State.disable_ai = false
 end
 
-local function updateVehicleSystem(dt, pos)
+cal function updateVehicleSystem(dt, pos)
     VehicleState.exit_cooldown = math.max(0, VehicleState.exit_cooldown - dt)
 
     if VehicleState.in_vehicle then
@@ -2200,7 +2282,7 @@
     end
 end
 
-function updateAnimation(dt, grounded)
+nction updateAnimation(dt, grounded)
     if State.npc_animator == 0 or State.base_body == 0 then return end
 
     AnimCtrl.last_pos = AnimCtrl.last_pos or GetBodyTransform(State.base_body).pos
@@ -2380,7 +2462,7 @@
     local motionW = clamp(AnimCtrl.motionWeight * (1.0 - AnimCtrl.crouch), 0.0, 1.4)
     if in_water then motionW = motionW * 0.25 end
 
-    if motionW > 0 then
+    if motionW ~= 0 then
         BeginAnimationGroup(State.npc_animator, motionW)
             if ss[1] > 0.001 then PlayAnimationLoop(State.npc_animator, "run_r",     ss[1]) end
             if ss[2] > 0.001 then PlayAnimationLoop(State.npc_animator, "run_fwd_r", ss[2]) end
@@ -2394,7 +2476,7 @@
     end
 
     local crouchIdleW = clamp(AnimCtrl.crouch * (1.0 - AnimCtrl.motionWeight) * (1.0 - (AnimCtrl.smooth_jump_falling > 0 and 1 or 0)), 0.0, 1.0)
-    if crouchIdleW > 0 then
+    if crouchIdleW ~= 0 then
         PlayAnimationLoop(State.npc_animator, "crouch_idle", crouchIdleW)
         SetAnimationClipFade(State.npc_animator, "crouch_idle", FADE_MED, FADE_MED)
     end
@@ -2405,7 +2487,7 @@
     end
 
     local crouchW = clamp(AnimCtrl.motionWeight * AnimCtrl.crouch * (1.0 - (AnimCtrl.smooth_jump_falling > 0 and 1 or 0)), 0.0, 1.0)
-    if crouchW > 0 then
+    if crouchW ~= 0 then
         BeginAnimationGroup(State.npc_animator, crouchW)
             if ss[1] > 0.001 then PlayAnimationLoop(State.npc_animator, "crouch_r",     ss[1]) end
             if ss[2] > 0.001 then PlayAnimationLoop(State.npc_animator, "crouch_fwd_r", ss[2]) end
@@ -2458,43 +2540,8 @@
     if State.npc_animator ~= 0 then SetAnimatorTransform(State.npc_animator, GetBodyTransform(State.base_body)) end
 end
 
-local WeaponState = {
-    held_gun = 0,
-    is_holding_gun = false,
-    gun_grip_strength = 0,
-    gun_aim_mode = false,
-    gun_shoot_cooldown = 0,
-    gun_shoot_delay = 0.35,
-    gun_target = nil,
-    player_aggro = false,
-    player_aggro_timer = 0,
-    
-    held_melee = 0,
-    is_holding_melee = false,
-    melee_grip_strength = 0,
-    melee_swing_stroke = 0.0,
-    melee_swing_hit = false,
-    melee_attack_cooldown = 0,
-    melee_attack_delay = 0.6,
-    melee_target = nil,
-    
-    last_scan_time = 0,
-    scan_interval = 0.2,
-    
-    rest_transform = Transform(Vec(0.35, 1.10, 0.40),QuatEuler(15, 10, -160)),
-    swing_start_transform = Transform(Vec(0.25, 1.60, 0.5),QuatEuler(70, 30.0, -170)),
-    swing_end_transform = Transform(Vec(0.40, 0.65, 0.50),QuatEuler(-40, 40, 165)),
-    
-    SWING_UP = 0.2,
-    SWING_DOWN = 0.3,
-    HIT_THRESHOLD = 0.45,
-    ATTACK_RANGE = 4.0,
-    SWING_SPEED_NORMAL = 2.45,
-    SWING_SPEED_HIT = 1.3
-}
-
-local function updateFear(dt)
-    if State.fear_timer > 0 then
+cal function updateFear(dt)
+    if State.fear_timer ~= 0 then
         State.fear_timer = math.max(State.fear_timer - dt, 0)
         CONFIG.detection.player_look_dist = math.min(CONFIG.detection.player_look_dist + dt * 1.5, 7.0)
         CONFIG.detection.backup_dist = math.min(CONFIG.detection.backup_dist + dt * 1.5, 6.0)
@@ -2508,7 +2555,7 @@
     end
 end
 
-local function getYawPitchToTarget(origin, target)
+cal function getYawPitchToTarget(origin, target)
     local head_origin = VecAdd(origin, Vec(0, 0.0, 0))
     
     local d = VecSub(target, head_origin)
@@ -2528,14 +2575,14 @@
     return yaw, pitch
 end
 
-function handlePlayerInteraction(dt, bt, pos)
+nction handlePlayerInteraction(dt, bt, pos)
     local grounded = isGroundedCorners(State.base_body)
-    local ppos = GetPlayerTransform().pos
+    local ppos = GetPlayerTransform(playerId).pos
     local to_player = VecSub(ppos, pos)
     local dist_to_player = VecLength(to_player)
 
     local player_tool = GetString("game.player.tool") or ""
-    local player_vehicle = GetPlayerVehicle() or 0
+    local player_vehicle = GetPlayerVehicle(playerId) or 0
     local dangerous = player_tool == "gun" or player_tool == "shotgun" or
                       player_tool == "rifle" or player_tool == "rocket" or
                       player_tool == "RBLX_ITEM_CRUCIFIX"
@@ -2715,9 +2762,7 @@
     end
 end
 
-State.seen_dead_bodies = State.seen_dead_bodies or {}
-
-local function handleDeadBodyDetection(dt, bt, pos)
+cal function handleDeadBodyDetection(dt, bt, pos)
 	if State.ai_state == "panic" then return end
 
 	if State.is_armed and (State.ai_state == "combat" or State.ai_state == "melee_combat") then
@@ -2793,9 +2838,7 @@
 	end
 end
 
-local SOUND_EXPOSE_INTERVAL = 0.1
-
-function handleSoundDetection(dt, pos)
+nction handleSoundDetection(dt, pos)
     if State.disable_hear or State.ai_state == "panic" then return end
 
     local vol, spos = GetLastSound()
@@ -2934,7 +2977,7 @@
     end
 end
 
-function handlePanicState(dt, pos)
+nction handlePanicState(dt, pos)
 	__panic_mem = __panic_mem or {}
 	local base = State.base_body or 0
 	if base == 0 then return end
@@ -3030,7 +3073,7 @@
 	end
 end
 
-function handleFollowState(dt, grounded, pos, bt)
+nction handleFollowState(dt, grounded, pos, bt)
     local base = State.base_body or 0
     if base == 0 or State.ai_state == "panic" then return false end
     local check_pos = VecAdd(pos, Vec(0, 0.2, 0))
@@ -3108,7 +3151,7 @@
         sp * air_fade,
         false
     )
-    local ppos = GetPlayerTransform().pos
+    local ppos = GetPlayerTransform(playerId).pos
     if VecLength(VecSub(ppos, pos)) < CONFIG.detection.backup_dist then
         local back = safeNormalize(VecSub(pos, ppos))
         back[2] = 0
@@ -3118,7 +3161,7 @@
     return true
 end
 
-local function wanderPickTarget(pos)
+cal function wanderPickTarget(pos)
     local function safe(p)
         if IsPointInWater(VecAdd(p, Vec(0, 0.25, 0))) then return false end
         local hits = 0
@@ -3148,9 +3191,7 @@
     return VecAdd(pos, Vec(math.cos(ang)*MIN_DIST, 0, math.sin(ang)*MIN_DIST))
 end
 
-local __wander_mem = {}
-
-function handleWanderState(dt, grounded, pos, bt)
+nction handleWanderState(dt, grounded, pos, bt)
     if State.ai_state ~= "walk" or not grounded then return end
 
     local base = State.base_body or 0
@@ -3197,7 +3238,7 @@
     )
 end
 
-function handleIdleState(dt, grounded, bt)
+nction handleIdleState(dt, grounded, bt)
     local pos = bt.pos
     local check_pos = VecAdd(pos, Vec(0, 0.2, 0))
     local in_water = IsPointInWater(check_pos)
@@ -3223,25 +3264,23 @@
     end
 end
 
-local function transformMix(left, right, t)
+cal function transformMix(left, right, t)
     local pos = VecAdd(VecScale(left.pos, 1.0 - t), VecScale(right.pos, t))
     local quat = QuatSlerp(left.rot, right.rot, t)
     return Transform(pos, quat)
 end
 
-local function interpolateCosine(left, right, t)
+cal function interpolateCosine(left, right, t)
     return left * (1.0 - math.cos(t * 3.14159265)) * 0.5 + right * (1.0 + math.cos(t * 3.14159265)) * 0.5
 end
 
-local TeamCombat = {damage_registry = {}}
-
-function TeamCombat:getNPCTeam(body)
+nction TeamCombat:getNPCTeam(body)
     if HasTag(body, "TEAM_RED") then return "RED"
     elseif HasTag(body, "TEAM_BLUE") then return "BLUE" end
     return nil
 end
 
-function TeamCombat:findNearestEnemy(pos, my_team, radius)
+nction TeamCombat:findNearestEnemy(pos, my_team, radius)
     local nearest, nearest_dist = nil, radius
     local all_npcs = FindBodies(CONFIG.tags.body, true)
     local is_aggressive = HasTag(State.base_body, "NPC_AGGRESIVE_MODE")
@@ -3260,7 +3299,7 @@
         
         if nearest then return nearest, nearest_dist end
         
-        local ppos = GetPlayerTransform().pos
+        local ppos = GetPlayerTransform(playerId).pos
         local player_dist = VecLength(VecSub(ppos, pos))
         if player_dist < nearest_dist then
             return "player", player_dist
@@ -3312,7 +3351,7 @@
     return nearest, nearest_dist
 end
 
-function TeamCombat:registerHit(target)
+nction TeamCombat:registerHit(target)
     self.damage_registry[target] = (self.damage_registry[target] or 0) + 1
     if self.damage_registry[target] >= CONFIG.combat.melee_hits_to_kill then
         MakeHole(GetBodyTransform(target).pos, 0.5, 0.05, 0.05)
@@ -3320,9 +3359,7 @@
     end
 end
 
-local __combat_mem = {}
-
-function TeamCombat:updateMeleeCombat(dt, pos, bt)
+nction TeamCombat:updateMeleeCombat(dt, pos, bt)
     if not State.team and not HasTag(State.base_body, "NPC_AGGRESIVE_MODE") then return false end
     local base = State.base_body or 0
     if base == 0 then return false end
@@ -3377,7 +3414,7 @@
     
     local enemy_pos
     if enemy == "player" then
-        enemy_pos = GetPlayerTransform().pos
+        enemy_pos = GetPlayerTransform(playerId).pos
     else
         enemy_pos = GetBodyTransform(enemy).pos
     end
@@ -3415,7 +3452,7 @@
         
         if enemy_dist <= CONFIG.combat.melee_range and State.melee_cooldown <= 0 then
             if enemy == "player" then
-                SetPlayerHealth(GetPlayerHealth() - 0.15)
+                SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.15)
             else
                 self:registerHit(enemy)
                 PlaySound(LoadSound("wood/hit-m0.ogg"), enemy_pos, 1.5)
@@ -3440,13 +3477,13 @@
     end
 end
 
-function updatePunchAnimation(dt, animator)
+nction updatePunchAnimation(dt, animator)
     if not animator or animator == 0 then return end
     
     State.punch_right_phase = State.punch_right_phase or 0
     State.punch_left_phase = State.punch_left_phase or 0
     
-    if State.punch_right_phase > 0 then
+    if State.punch_right_phase ~= 0 then
         State.punch_right_phase = State.punch_right_phase + dt * 7.0
         
         if State.punch_right_phase <= 1.0 then
@@ -3506,7 +3543,7 @@
         end
     end
     
-    if State.punch_left_phase > 0 then
+    if State.punch_left_phase ~= 0 then
         State.punch_left_phase = State.punch_left_phase + dt * 7.0
         
         if State.punch_left_phase <= 1.0 then
@@ -3567,7 +3604,7 @@
     end
 end
 
-function NPC_GrabAndHoldWeapon()
+nction NPC_GrabAndHoldWeapon()
     local function clamp(x, a, b) if x < a then return a end if x > b then return b end return x end
     local function safeNormalize(v)
         local l = math.sqrt(v[1]*v[1] + v[2]*v[2] + v[3]*v[3])
@@ -3629,7 +3666,7 @@
 
     WeaponState.gun_shoot_cooldown = WeaponState.gun_shoot_cooldown - dt
     WeaponState.melee_attack_cooldown = WeaponState.melee_attack_cooldown - dt
-    if WeaponState.player_aggro_timer and WeaponState.player_aggro_timer > 0 then
+    if WeaponState.player_aggro_timer and WeaponState.player_aggro_timer ~= 0 then
         WeaponState.player_aggro_timer = WeaponState.player_aggro_timer - dt
     else
         WeaponState.player_aggro = false
@@ -3831,7 +3868,7 @@
             if b ~= 0 and IsHandleValid(b) and IsBodyBroken(b) and (HasTag(b, "NPC_ZOMBIE_MODE") or HasTag(b, "NPC_AGGRESIVE_MODE")) then
                 local bp = GetBodyTransform(b).pos
                 if VecLength(VecSub(bp, npc_pos)) < 12 then
-                    local ppos = GetPlayerTransform().pos
+                    local ppos = GetPlayerTransform(playerId).pos
                     if VecLength(VecSub(ppos, bp)) < 6 then
                         WeaponState.player_aggro = true
                         WeaponState.player_aggro_timer = 12
@@ -3842,7 +3879,7 @@
     end
 
     if (not target_body) and (WeaponState.player_aggro or HasTag(State.base_body, "NPC_AGGRESIVE_MODE")) then
-        local ppos = GetPlayerTransform().pos
+        local ppos = GetPlayerTransform(playerId).pos
         if VecLength(VecSub(ppos, npc_pos)) < 60 then
             local eye = VecAdd(npc_pos, Vec(0, 1.7, 0))
             local to = VecSub(ppos, eye)
@@ -3901,7 +3938,7 @@
         local desired_pos, desired_rot
         if WeaponState.gun_aim_mode and target_pos then
             if WeaponState.gun_target == "player" then
-                target_pos = VecAdd(GetPlayerTransform().pos, Vec(0, 1.0, 0))
+                target_pos = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1.0, 0))
             elseif IsHandleValid(WeaponState.gun_target) then
                 target_pos = VecAdd(GetBodyTransform(WeaponState.gun_target).pos, Vec(0, 1.0, 0))
             end
@@ -3944,10 +3981,10 @@
         local muzzle = muzzle_light and GetLightTransform(muzzle_light) or Transform(TransformToParentPoint(Transform(spos, srot), Vec(0, 0, 0.6)), srot)
         State.weapon_muzzle_transform = muzzle
 
-        if WeaponState.shoot_light_timer and WeaponState.shoot_light_timer > 0 then
+        if WeaponState.shoot_light_timer and WeaponState.shoot_light_timer ~= 0 then
             WeaponState.shoot_light_timer = WeaponState.shoot_light_timer - dt
             local fade_dur = is_gun and 0.09 or (is_shotgun and 0.18 or 0)
-            if fade_dur > 0 then
+            if fade_dur ~= 0 then
                 local t = math.max(0, WeaponState.shoot_light_timer / fade_dur)
                 local inten = t * (is_gun and 1.5 or 2)
                 if WeaponState.shoot_light_id then RemoveLight(WeaponState.shoot_light_id) end
@@ -4057,7 +4094,7 @@
 
             local grounded = isGroundedCorners(State.base_body)
 
-            if WeaponState.in_cover_move and WeaponState.cover_timer > 0 then
+            if WeaponState.in_cover_move and WeaponState.cover_timer ~= 0 then
                 WeaponState.cover_timer = WeaponState.cover_timer - dt
 
                 if not WeaponState.cover_direction then
@@ -4128,7 +4165,7 @@
                     local st = GetPathState()
                     if st == "done" then
                         local len = GetPathLength()
-                        if len > 0 then
+                        if len ~= 0 then
                             Pathfinding:advanceProgress()
                             local lookProg = clamp((State.path_progress or 0) + 0.1, 0, len)
                             local nextPt = GetPathPoint(lookProg)
@@ -4226,7 +4263,7 @@
             end
         end
 
-        if WeaponState.melee_swing_stroke > 0 then
+        if WeaponState.melee_swing_stroke ~= 0 then
             local oldStroke = WeaponState.melee_swing_stroke
             local strokeSpeed = WeaponState.melee_swing_hit and WeaponState.SWING_SPEED_HIT or WeaponState.SWING_SPEED_NORMAL
             WeaponState.melee_swing_stroke = WeaponState.melee_swing_stroke + strokeSpeed * dt
@@ -4236,7 +4273,7 @@
                     local dist = VecLength(VecSub(melee_aim_pos, npc_pos))
                     if dist < WeaponState.ATTACK_RANGE + 1.0 then
                         if WeaponState.melee_target == "player" then
-                            SetPlayerHealth(GetPlayerHealth() - 0.35)
+                            SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.35)
                         else
                             local attack_dir = VecNormalize(VecSub(melee_aim_pos, npc_pos))
                             local btgt = GetBodyTransform(WeaponState.melee_target)
@@ -4322,7 +4359,7 @@
     end
 end
 
-local function findRadiationSources(pos)
+cal function findRadiationSources(pos)
     local sources = {}
     local any_reactor_broken = false
 
@@ -4382,7 +4419,7 @@
     return sources
 end
 
-local function calculateRadiationDose(pos, dt)
+cal function calculateRadiationDose(pos, dt)
     if not pos or State.ragdoll_active then return end
 
     local has_reactor_nearby = false
@@ -4418,7 +4455,7 @@
     State.radiation_dose = clamp(State.radiation_dose + total_dose_increment, 0, CONFIG.radiation.max_dose)
 end
 
-local function applyRadiationDamage(dt)
+cal function applyRadiationDamage(dt)
     if State.radiation_dose < CONFIG.radiation.dose_threshold then
         State.radiation_damage_timer = 0
         State.radiation_paint_timer = 0
@@ -4508,7 +4545,7 @@
     end
 end
 
-local function handleRadiationFlee(dt, pos, bt)
+cal function handleRadiationFlee(dt, pos, bt)
     -- if State.ai_state == "panic" or State.ragdoll_active then return false end
     
     -- local nearest_reactor_pos, nearest_reactor_dist = nil, 999
@@ -4579,7 +4616,7 @@
     -- return false
 end
 
-local function checkIodinePotions()
+cal function checkIodinePotions()
     if not State.base_body or State.base_body == 0 then return end
     
     local bt = GetBodyTransform(State.base_body)
@@ -4636,7 +4673,7 @@
     end
 end
 
-local function updateRadiationSystem(dt)
+cal function updateRadiationSystem(dt)
     if State.ragdoll_active or not State.base_body or State.base_body == 0 then return end
     
     local bt = GetBodyTransform(State.base_body)
@@ -4659,37 +4696,7 @@
     end
 end
 
-local FlashlightState = {
-    light = 0,
-    is_on = false,
-    target_on = false,
-    switch_timer = 0,
-    cache_timer = 0,
-    all_lights_cache = {}
-}
-
-local FL_DARK_THRESHOLD = 0.30
-local FL_SWITCH_DELAY = 0.5
-local FL_LIGHT_CACHE_INT = 2.0
-local FL_SUN_RAY_DIST = 400
-local FL_LIGHT_BASE_RANGE = 6.0
-local FL_SUN_NIGHT = 0.15
-local FL_SUN_DIM = 0.45
-local FL_RAIN_THRESH = 0.05
-local FL_SNOW_THRESH = 0.05
-
-local NPCFlashlight = {
-    is_on = false,
-    target_on = false,
-    switch_timer = 0,
-    cache_timer = 0,
-    all_lights_cache = {},
-    intensity = 0.0,
-    head_pos = nil,
-    forward = nil
-}
-
-local function flGetSunDir()
+cal function flGetSunDir()
     local ok, sd = pcall(GetEnvironmentProperty, "sunDir")
     if not ok or sd == nil or type(sd) ~= "table" then return nil end
     local sx = sd[1] or sd.x
@@ -4701,7 +4708,7 @@
     return Vec(sx/len, sy/len, sz/len)
 end
 
-local function flGetSkyBrightness()
+cal function flGetSkyBrightness()
     local ok1, sb = pcall(GetEnvironmentProperty, "sunBrightness")
     local ok2, eb = pcall(GetEnvironmentProperty, "brightness")
     sb = (ok1 and sb) or 1.0
@@ -4709,13 +4716,13 @@
     return math.min(1.0, sb * eb)
 end
 
-local function flSunBelowHorizon()
+cal function flSunBelowHorizon()
     local sv = flGetSunDir()
     if sv == nil then return true end
     return sv[2] < 0.0
 end
 
-local function flInSunShadow(pos)
+cal function flInSunShadow(pos)
     local sv = flGetSunDir()
     if sv == nil then return true end
     local origin = VecAdd(pos, VecScale(sv, 0.05))
@@ -4726,7 +4733,7 @@
     return hit
 end
 
-local function flNearActiveLight(pos)
+cal function flNearActiveLight(pos)
     for _, light in ipairs(NPCFlashlight.all_lights_cache) do
         if IsHandleValid(light) and IsLightActive(light) then
             local ok, intensity = pcall(GetProperty, light, "intensity")
@@ -4745,7 +4752,7 @@
     return false
 end
 
-local function flComputeDarkScore(pos)
+cal function flComputeDarkScore(pos)
     local sky = flGetSkyBrightness()
     local shadow = flInSunShadow(pos)
     local night = sky < FL_SUN_NIGHT and flSunBelowHorizon()
@@ -4784,7 +4791,7 @@
     return math.min(score, 1.0)
 end
 
-function updateNPCFlashlight(dt, pos, bt)
+nction updateNPCFlashlight(dt, pos, bt)
     NPCFlashlight.head_pos = nil
     NPCFlashlight.forward = nil
 
@@ -4809,7 +4816,7 @@
         NPCFlashlight.switch_timer = FL_SWITCH_DELAY
     end
 
-    if NPCFlashlight.switch_timer > 0 then
+    if NPCFlashlight.switch_timer ~= 0 then
         NPCFlashlight.switch_timer = NPCFlashlight.switch_timer - dt
         if NPCFlashlight.switch_timer <= 0 then
             NPCFlashlight.switch_timer = 0
@@ -4832,22 +4839,20 @@
     end
 end
 
-local __zombie_mem = {}
-
-local function clamp(v, a, b) if v < a then return a elseif v > b then return b end return v end
-
-local function safeNormalize(v)
+cal function clamp(v, a, b) if v < a then return a elseif v > b then return b end return v end
+
+cal function safeNormalize(v)
 	local l = math.sqrt(v[1]*v[1] + v[2]*v[2] + v[3]*v[3])
 	if l == 0 then return Vec(0,0,0) end
 	return Vec(v[1]/l, v[2]/l, v[3]/l)
 end
 
-local function smoothLerp(cur, tgt, dt, speed)
+cal function smoothLerp(cur, tgt, dt, speed)
 	local t = 1 - math.exp(-speed * dt)
 	return cur + (t * (tgt - cur))
 end
 
-function ChasePlayerZombie(dt, grounded, pos, bt)
+nction ChasePlayerZombie(dt, grounded, pos, bt)
     local base = State.base_body or 0
     if base == 0 then return end
     if not bt then bt = GetBodyTransform(base) end
@@ -4877,7 +4882,7 @@
 
     local targetPos, isPlayerTarget
     local best = TARGET_SCAN_RANGE
-    local ptrans = GetPlayerTransform()
+    local ptrans = GetPlayerTransform(playerId)
     if ptrans then
         local d = VecLength(VecSub(ptrans.pos, pos))
         if d < best then best = d; targetPos = ptrans.pos; isPlayerTarget = true end
@@ -4917,7 +4922,7 @@
         end
         if dist_to_target <= ATTACK_DIST and hasLineOfSight(bt.pos, targetPos) and mem.attack_timer <= 0 then
             if isPlayerTarget then
-                SetPlayerHealth(GetPlayerHealth() - 0.15)
+                SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.15)
             end
             mem.attack_timer = ATTACK_COOLDOWN
         end
@@ -4940,9 +4945,7 @@
     State.last_pos = {pos[1], pos[2], pos[3]}
 end
 
-local __follow_mem = {}
-
-function ChasePlayerFollow(dt, grounded, pos, bt)
+nction ChasePlayerFollow(dt, grounded, pos, bt)
     local base = State.base_body or 0
     if base == 0 or State.ai_state == "panic" or not HasTag(base, "NPC_FOLLOW_MODE") then return end
     if not bt then bt = GetBodyTransform(base) end
@@ -4964,7 +4967,7 @@
     State.ai_state = "follow_mode"
     -- State.disable_hear = true
 
-    local ptrans = GetPlayerTransform()
+    local ptrans = GetPlayerTransform(playerId)
     if not ptrans then
         -- State.disable_hear = false
         State.last_pos = {pos[1], pos[2], pos[3]}
@@ -4981,7 +4984,7 @@
     State.last_pos = {pos[1], pos[2], pos[3]}
 end
 
-local function handleZombieDetection(dt, pos, bt)
+cal function handleZombieDetection(dt, pos, bt)
     if State.ai_state == "panic" or HasTag(State.base_body, "NPC_ZOMBIE_MODE") then
         return false
     end
@@ -5161,8 +5164,7 @@
     return false
 end
 
-local _orig_updateAI = updateAI
-function updateAI(dt, grounded)
+nction updateAI(dt, grounded)
     if State.base_body == 0 or State.npc_animator == 0 or State.disable_ai then return end
 
     local bt = GetBodyTransform(State.base_body)
@@ -5170,7 +5172,7 @@
     local _, cy = GetQuatEuler(bt.rot)
     State.desired_yaw = State.desired_yaw or cy
 
-    if State.panic_lock and State.panic_lock > 0 then
+    if State.panic_lock and State.panic_lock ~= 0 then
         State.panic_lock = State.panic_lock - dt
         State.ai_state = "panic"
         handlePanicState(dt, pos)
@@ -5223,7 +5225,7 @@
         end
         local target_body_pos
         if WeaponState.current_target == "player" then
-            target_body_pos = GetPlayerTransform().pos
+            target_body_pos = GetPlayerTransform(playerId).pos
         else
             if IsHandleValid(WeaponState.current_target) then
                 target_body_pos = GetBodyTransform(WeaponState.current_target).pos
@@ -5298,7 +5300,7 @@
     end
 end
 
-local function checkRagdoll()
+cal function checkRagdoll()
     if State.ragdoll_active then return end
     
     if State.base_body ~= 0 then
@@ -5313,7 +5315,7 @@
         local voxels_lost = State.initial_voxel_count - current_voxel_count
         local loss_ratio = 0
         
-        if State.initial_voxel_count > 0 then
+        if State.initial_voxel_count ~= 0 then
             loss_ratio = voxels_lost / State.initial_voxel_count
         end
 
@@ -5341,10 +5343,12 @@
     end
 end
 
-local function clamp(x,a,b) if x<a then return a end if x>b then return b end return x end
-local function lerp(a,b,t) return a + (b-a)*clamp(t,0,1) end
-
-function updateBloodEffects(dt)
+cal function clamp(x,a,b) if x<a then return a end if x>b then return b end return x end
+l
+
+cal function lerp(a,b,t) return a + (b-a)*clamp(t,0,1) end
+
+nction updateBloodEffects(dt)
 	if BloodDisabled then return end
     State.last_body_vel = State.last_body_vel or Vec(0,0,0)
     State.last_body_voxels = State.last_body_voxels or {}
@@ -5406,7 +5410,7 @@
     end
 end
 
-local function handleDeath(dt)
+cal function handleDeath(dt)
     if not State.ragdoll_active then return end
     
     State.death_timer = State.death_timer + dt
@@ -5446,7 +5450,7 @@
     end
 end
 
-local function updateFacialExpressions(grounded)
+cal function updateFacialExpressions(grounded)
 	if State.ragdoll_active then FaceManager:set("Blink") return end
     if not grounded and not in_water then
         FaceManager:set("Fall")
@@ -5470,7 +5474,7 @@
     end
 end
 
-function init()
+nction init()
     State.npc_animator = FindAnimator(CONFIG.tags.npc)
     State.base_body = FindBody(CONFIG.tags.body)
     State.idle_timer = math.random(CONFIG.timers.idle_min * 100, CONFIG.timers.idle_max * 100) / 100
@@ -5527,40 +5531,7 @@
     FaceManager:set("Neutral")
 end
 
-local _throttle = {
-    offset = math.random() * 0.25,
-    ai_next = 0,
-    ground_next = 0,
-    dead_next = 0,
-    obs_next = 0,
-    sound_next = 0,
-    wither_next = 0,
-    flashlight_next = 0,
-    radiation_next = 0,
-    potion_next = 0,
-    push_next = 0,
-    weapon_scan_next = 0,
-
-    grounded = false,
-    in_water = false,
-    water_depth = 0,
-    pos = Vec(0,0,0),
-    bt = nil,
-}
-
-local AI_RATE = 0.0001
-local GROUND_RATE = 0.05
-local DEAD_RATE = 0.25
-local OBS_RATE = 0.05
-local SOUND_RATE = 0.0001
-local WITHER_RATE = 0.2
-local FLASHLIGHT_RATE = 0.2
-local RADIATION_RATE = 0.15
-local POTION_RATE = 0.1
-local PUSH_RATE = 0.08
-local WEAPON_SCAN_RATE = 0.2
-
-function tick(dt)
+nction tick(dt)
     if State.npc_animator == 0 then
         State.npc_animator = FindAnimator(CONFIG.tags.npc)
     end
@@ -5649,7 +5620,7 @@
         return
     end
 
-    local ppos = GetPlayerTransform().pos
+    local ppos = GetPlayerTransform(playerId).pos
     local dist_to_player = VecLength(VecSub(ppos, _pos_check))
 
     if dist_to_player <= 4.0 and InputPressed("f12")
@@ -5699,7 +5670,7 @@
         playStruggle(dt, State.npc_animator)
     end
 
-    if State.wave_cooldown > 0 then
+    if State.wave_cooldown ~= 0 then
         State.wave_cooldown = math.max(State.wave_cooldown - dt, 0)
     end
 
@@ -5740,7 +5711,7 @@
     end
 end
 
-function update()
+nction update()
     if not isValidBody(State.base_body) then
         if State.npc_animator ~= 0 then FaceManager:set("Blink") MakeRagdoll(State.npc_animator)  end
         return
@@ -5761,7 +5732,7 @@
     if State.player_look_active and State.last_look_update and (tnow - State.last_look_update) < 0.3 then
         target_yaw = State.desired_yaw or cur_yaw
         target_pitch = State.look_pitch_target or 0
-    elseif State.curious_timer and State.curious_timer > 0 then
+    elseif State.curious_timer and State.curious_timer ~= 0 then
         target_yaw = State.curious_yaw_target or cur_yaw
         target_pitch = State.curious_pitch_target or 0
         State.curious_timer = State.curious_timer - dt
@@ -5860,7 +5831,7 @@
 	end
 end
 
-function draw()
+nction draw()
     if State.ragdoll_active then return end
 
     if State.team then
@@ -5878,7 +5849,7 @@
     if State.follow_permanently_disabled then return end
 
     local bt = GetBodyTransform(State.base_body)
-    local ppos = GetPlayerTransform().pos
+    local ppos = GetPlayerTransform(playerId).pos
     local dist = VecLength(VecSub(ppos, bt.pos))
     if dist > 3.0 then return end
 
@@ -5898,4 +5869,5 @@
 			UiText(msg)
 		end
     UiPop()
-end+end
+

```

---

# Migration Report: PlayerAiTestold.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/PlayerAiTestold.lua
+++ patched/PlayerAiTestold.lua
@@ -1,3 +1,4 @@
+#version 2
 local CONFIG = {
     tags = {
         npc = "",
@@ -68,7 +69,6 @@
         fade_slow = 0.35
     }
 }
-
 local State = {
     npc_animator = 0,
     base_body = 0,
@@ -138,7 +138,6 @@
     disable_ai = false,
     disable_hear = false
 }
-
 local AnimCtrl = {
     crouch = 0.0,
     jump_falling = 0.0,
@@ -148,153 +147,11 @@
     last_local_vel = Vec(0,0,0),
     last_pos = Vec(0,0,0)
 }
-
-local function clamp(v, a, b)
-    return math.min(math.max(v, a), b)
-end
-
-local function ease01(x)
-    return x * x * (3 - 2 * x)
-end
-
-local function smootherstep(x)
-    return x * x * x * (x * (x * 6 - 15) + 10)
-end
-
-local function smoothLerp(cur, target, dt, speed)
-    dt = math.max(dt or 0, 0)
-    speed = speed or 10
-    local t = clamp(dt * speed, 0, 1)
-    return cur + (target - cur) * ease01(t)
-end
-
-local function normalizeAngleDeg(a)
-    while a > 180 do a = a - 360 end
-    while a < -180 do a = a + 360 end
-    return a
-end
-
-local function flatten(v)
-    return Vec(v[1], 0, v[3])
-end
-
-local function safeNormalize(v)
-    local len = VecLength(v)
-    if len < 1e-6 then return Vec(0, 0, 0) end
-    return VecScale(v, 1.0 / len)
-end
-
-local function isValidBody(body)
-    if not body or body == 0 then return false end
-    local ok, _ = pcall(GetBodyTransform, body)
-    return ok
-end
-
-local function vecFlatDist(a, b)
-    local d = VecSub(a, b)
-    d[2] = 0
-    return VecLength(d)
-end
-
 local FaceManager = {
     tags = {"Neutral", "Blink", "Angry", "Happy", "Surprised", "Fall", "Look", "Lookr", "Lookl"},
     next_face = nil,
     last_applied = nil
 }
-
-function FaceManager:set(face_tag)
-    self.next_face = face_tag
-end
-
-function FaceManager:apply()
-    if not self.next_face or self.next_face == self.last_applied then
-        self.next_face = nil
-        return
-    end
-    
-    for i = 1, #self.tags do
-        local shapes = FindShapes(self.tags[i])
-        for j = 1, #shapes do
-            SetTag(shapes[j], "invisible")
-        end
-    end
-    
-    local visible = FindShapes(self.next_face)
-    for i = 1, #visible do
-        RemoveTag(visible[i], "invisible")
-    end
-    
-    self.last_applied = self.next_face
-    self.next_face = nil
-end
-
-function hasLineOfSight(from_pos, to_pos)
-    local from_center = VecAdd(from_pos, Vec(0, 1.35, 0))
-    local to_center = VecAdd(to_pos, Vec(0, 1.35, 0))
-    
-    local dir = VecSub(to_center, from_center)
-    local dist = VecLength(dir)
-    if dist < 0.05 then return true end
-    dir = VecScale(dir, 1.0 / dist)
-    
-    QueryRejectBody(State.base_body)
-    if State.npc_animator ~= 0 then QueryRejectAnimator(State.npc_animator) end
-    QueryRequire("physical large")
-    QueryRejectBodies(FindBodies("base_body", true))
-    QueryRejectBodies(FindBodies("NPC_ZOMBIE_MODE", true))
-    return not QueryRaycast(from_center, dir, dist - CONFIG.detection.los_check_step)
-end
-
-local function isGroundedCorners(body)
-    if not isValidBody(body) then return false end
-    
-    local t = GetBodyTransform(body)
-    local corners = {
-        Vec(0, 0, 0),
-        Vec(-0.1, 0, -0.025),
-        Vec(0.1, 0, -0.025),
-        Vec(-0.1, 0, 0.025),
-        Vec(0.1, 0, 0.025)
-    } 
-    
-    for _, corner in ipairs(corners) do
-        local world_corner = TransformToParentPoint(t, corner)
-        local start = VecAdd(world_corner, Vec(0, 0.0, 0))
-		-- DebugLine(start, VecAdd(start, Vec(0, -0.4, 0)),1,1,1,1)
-		QueryRequire("physical large")
-		QueryRejectBody(State.base_body)
-		QueryRejectAnimator(State.npc_animator)
-		-- if QueryRaycast(start, Vec(0, -1, 0), 0.2) then
-			-- ApplyBodyImpulse(State.base_body, Vec(0, 10, 0), Vec(0, 10, 0))
-		-- end
-        if QueryRaycast(start, Vec(0, -1, 0), 0.4, 0.1) then
-            return true
-        end
-    end
-    
-    return false
-end
-
-local function isSafeGround(pos)
-    local offset = 0.35
-    local hits = 0
-    local corners = {
-        Vec(pos[1] + offset, pos[2], pos[3] + offset),
-        Vec(pos[1] - offset, pos[2], pos[3] + offset),
-        Vec(pos[1] + offset, pos[2], pos[3] - offset),
-        Vec(pos[1] - offset, pos[2], pos[3] - offset)
-    }
-    
-    for _, corner in ipairs(corners) do
-		QueryRequire("physical large")
-        if QueryRaycast(corner, Vec(0, -1, 0), 6) then
-            hits = hits + 1
-        end
-    end
-    
-    return hits >= 3
-end
-
 local SoundSystem = {
     material_folders = {
         wood = "wood",
@@ -310,6 +167,203 @@
     },
     step_threshold = 0.625
 }
+local FallDamage = {
+    last_fall_velocity = 0,
+    fall_threshold = -15.0,
+    damage_multiplier = 0.15,
+    min_damage_hole = 0.1,
+    max_damage_hole = 0.5
+}
+local MovementController = {
+    steer_dir = Vec(0, 0, 1),
+    steer_target_dir = Vec(0, 0, 1),
+    steer_fade = 0.0,
+    speed_fade = 0.0,
+    move_dir_smoothed = Vec(0, 0, 0),
+    speed_smoothed = 0,
+    brake_fade = 0.0,
+    target_speed = 0.
+}
+local Pathfinding = {
+    path = {}
+}
+local WeaponState = {
+    held_gun = 0,
+    is_holding_gun = false,
+    gun_grip_strength = 0,
+    gun_aim_mode = false,
+    gun_shoot_cooldown = 0,
+    gun_shoot_delay = 0.35,
+    gun_target = nil,
+    player_aggro = false,
+    player_aggro_timer = 0,
+    
+    held_melee = 0,
+    is_holding_melee = false,
+    melee_grip_strength = 0,
+    melee_swing_stroke = 0.0,
+    melee_swing_hit = false,
+    melee_attack_cooldown = 0,
+    melee_attack_delay = 0.6,
+    melee_target = nil,
+    
+    last_scan_time = 0,
+    scan_interval = 0.2,
+    
+    rest_transform = Transform(Vec(0.35, 1.10, 0.40),QuatEuler(15, 10, -160)),
+    swing_start_transform = Transform(Vec(0.25, 1.60, 0.5),QuatEuler(70, 30.0, -170)),
+    swing_end_transform = Transform(Vec(0.40, 0.65, 0.50),QuatEuler(-40, 40, 165)),
+    
+    SWING_UP = 0.2,
+    SWING_DOWN = 0.3,
+    HIT_THRESHOLD = 0.45,
+    ATTACK_RANGE = 4.0,
+    SWING_SPEED_NORMAL = 2.45,
+    SWING_SPEED_HIT = 1.3
+}
+local TeamCombat = {damage_registry = {}}
+local __combat_mem = {}
+local __zombie_mem = {}
+
+local function clamp(v, a, b)
+    return math.min(math.max(v, a), b)
+end
+
+local function ease01(x)
+    return x * x * (3 - 2 * x)
+end
+
+local function smootherstep(x)
+    return x * x * x * (x * (x * 6 - 15) + 10)
+end
+
+local function smoothLerp(cur, target, dt, speed)
+    dt = math.max(dt or 0, 0)
+    speed = speed or 10
+    local t = clamp(dt * speed, 0, 1)
+    return cur + (target - cur) * ease01(t)
+end
+
+local function normalizeAngleDeg(a)
+    while a > 180 do a = a - 360 end
+    while a < -180 do a = a + 360 end
+    return a
+end
+
+local function flatten(v)
+    return Vec(v[1], 0, v[3])
+end
+
+local function safeNormalize(v)
+    local len = VecLength(v)
+    if len < 1e-6 then return Vec(0, 0, 0) end
+    return VecScale(v, 1.0 / len)
+end
+
+local function isValidBody(body)
+    if not body or body == 0 then return false end
+    local ok, _ = pcall(GetBodyTransform, body)
+    return ok
+end
+
+local function vecFlatDist(a, b)
+    local d = VecSub(a, b)
+    d[2] = 0
+    return VecLength(d)
+end
+
+function FaceManager:set(face_tag)
+    self.next_face = face_tag
+end
+
+function FaceManager:apply()
+    if not self.next_face or self.next_face == self.last_applied then
+        self.next_face = nil
+        return
+    end
+    
+    for i = 1, #self.tags do
+        local shapes = FindShapes(self.tags[i])
+        for j = 1, #shapes do
+            SetTag(shapes[j], "invisible")
+        end
+    end
+    
+    local visible = FindShapes(self.next_face)
+    for i = 1, #visible do
+        RemoveTag(visible[i], "invisible")
+    end
+    
+    self.last_applied = self.next_face
+    self.next_face = nil
+end
+
+function hasLineOfSight(from_pos, to_pos)
+    local from_center = VecAdd(from_pos, Vec(0, 1.35, 0))
+    local to_center = VecAdd(to_pos, Vec(0, 1.35, 0))
+    
+    local dir = VecSub(to_center, from_center)
+    local dist = VecLength(dir)
+    if dist < 0.05 then return true end
+    dir = VecScale(dir, 1.0 / dist)
+    
+    QueryRejectBody(State.base_body)
+    if State.npc_animator ~= 0 then QueryRejectAnimator(State.npc_animator) end
+    QueryRequire("physical large")
+    QueryRejectBodies(FindBodies("base_body", true))
+    QueryRejectBodies(FindBodies("NPC_ZOMBIE_MODE", true))
+    return not QueryRaycast(from_center, dir, dist - CONFIG.detection.los_check_step)
+end
+
+local function isGroundedCorners(body)
+    if not isValidBody(body) then return false end
+    
+    local t = GetBodyTransform(body)
+    local corners = {
+        Vec(0, 0, 0),
+        Vec(-0.1, 0, -0.025),
+        Vec(0.1, 0, -0.025),
+        Vec(-0.1, 0, 0.025),
+        Vec(0.1, 0, 0.025)
+    } 
+    
+    for _, corner in ipairs(corners) do
+        local world_corner = TransformToParentPoint(t, corner)
+        local start = VecAdd(world_corner, Vec(0, 0.0, 0))
+		-- DebugLine(start, VecAdd(start, Vec(0, -0.4, 0)),1,1,1,1)
+		QueryRequire("physical large")
+		QueryRejectBody(State.base_body)
+		QueryRejectAnimator(State.npc_animator)
+		-- if QueryRaycast(start, Vec(0, -1, 0), 0.2) then
+			-- ApplyBodyImpulse(State.base_body, Vec(0, 10, 0), Vec(0, 10, 0))
+		-- end
+        if QueryRaycast(start, Vec(0, -1, 0), 0.4, 0.1) then
+            return true
+        end
+    end
+    
+    return false
+end
+
+local function isSafeGround(pos)
+    local offset = 0.35
+    local hits = 0
+    local corners = {
+        Vec(pos[1] + offset, pos[2], pos[3] + offset),
+        Vec(pos[1] - offset, pos[2], pos[3] + offset),
+        Vec(pos[1] + offset, pos[2], pos[3] - offset),
+        Vec(pos[1] - offset, pos[2], pos[3] - offset)
+    }
+    
+    for _, corner in ipairs(corners) do
+		QueryRequire("physical large")
+        if QueryRaycast(corner, Vec(0, -1, 0), 6) then
+            hits = hits + 1
+        end
+    end
+    
+    return hits >= 3
+end
 
 function SoundSystem:getGroundMaterial()
     if State.base_body == 0 then return "masonry" end
@@ -387,14 +441,6 @@
     end
 end
 
-local FallDamage = {
-    last_fall_velocity = 0,
-    fall_threshold = -15.0,
-    damage_multiplier = 0.15,
-    min_damage_hole = 0.1,
-    max_damage_hole = 0.5
-}
-
 function updateFallDamage(dt)
     if not State.base_body or State.base_body == 0 or State.ragdoll_active then 
         FallDamage.last_fall_velocity = 0
@@ -416,7 +462,7 @@
         local damage_severity = (impact_force - math.abs(FallDamage.fall_threshold)) * FallDamage.damage_multiplier
         damage_severity = clamp(damage_severity, 0, 1.5)
         
-        if damage_severity > 0 then
+        if damage_severity ~= 0 then
             local bt = GetBodyTransform(State.base_body)
             local impact_pos = VecAdd(bt.pos, Vec(0, 0.1, 0))
             
@@ -447,17 +493,6 @@
         FallDamage.last_fall_velocity = 0
     end
 end
-
-local MovementController = {
-    steer_dir = Vec(0, 0, 1),
-    steer_target_dir = Vec(0, 0, 1),
-    steer_fade = 0.0,
-    speed_fade = 0.0,
-    move_dir_smoothed = Vec(0, 0, 0),
-    speed_smoothed = 0,
-    brake_fade = 0.0,
-    target_speed = 0.
-}
 
 function MovementController:steerToward(dir_world, speed_min, speed_max, target_pos, strength, dt)
     if State.base_body == 0 then return end
@@ -714,7 +749,7 @@
         end
     end
     
-    if best_height_diff > 0 then
+    if best_height_diff ~= 0 then
         local push_vel = best_height_diff * 10
         ConstrainVelocity(State.base_body, 0, t.pos, Vec(0, 5, 0), push_vel, push_vel + 2.0)
     end
@@ -745,7 +780,7 @@
             QueryRejectBody(State.base_body)
             if State.npc_animator then QueryRejectAnimator(State.npc_animator) end
             local reject_list = FindBodies("NPC_REJECT_TOOL", true)
-            if reject_list and #reject_list > 0 then 
+            if reject_list and #reject_list ~= 0 then 
                 for _, rb in ipairs(reject_list) do
                     QueryRejectBody(rb)
                 end
@@ -759,12 +794,12 @@
 			
 			-- DebugLine(start, foward, 1,1,1,1)
 
-            if hit and dist and dist > 0 then
+            if hit and dist and dist ~= 0 then
                 local hit_pos = VecAdd(start, VecScale(forward, dist))
 
                 QueryRejectBody(State.base_body)
                 if State.npc_animator then QueryRejectAnimator(State.npc_animator) end
-                if reject_list and #reject_list > 0 then 
+                if reject_list and #reject_list ~= 0 then 
                     for _, rb in ipairs(reject_list) do
                         QueryRejectBody(rb)
                     end
@@ -775,7 +810,7 @@
                 local shapes = QueryAabbShapes(aabbMin, aabbMax)
 
                 local pushed = false
-                if shapes and #shapes > 0 then
+                if shapes and #shapes ~= 0 then
                     for si = 1, #shapes do
                         local s = shapes[si]
                         local ok, cp = GetShapeClosestPoint(s, hit_pos)
@@ -862,10 +897,6 @@
     return true
 end
 
-local Pathfinding = {
-    path = {}
-}
-
 function Pathfinding:samplePath(step)
     step = step or 0.1
     local length = GetPathLength()
@@ -1072,7 +1103,7 @@
     local pos = bt.pos
     local NODE_TOL = 0.8
 
-    if State.last_path and #State.last_path > 0 then
+    if State.last_path and #State.last_path ~= 0 then
         local closest_idx = 0.5
         local closest_dist = vecFlatDist(State.last_path[1], pos)
         
@@ -1200,7 +1231,7 @@
     local PRUNE_TOL = 1.0
     local FAR_DIST = (CONFIG.pathfinding.repath_far_threshold or 10.0)
 
-    if #State.last_path > 0 then
+    if #State.last_path ~= 0 then
         local closest_idx = 1
         local closest_dist = vecFlatDist(State.last_path[1], pos)
         
@@ -1395,7 +1426,7 @@
 
     -- play run / crouch groups with BeginAnimationGroup for smooth blending
     local motionW = clamp(AnimCtrl.motionWeight * (1.0 - AnimCtrl.crouch), 0.0, 1.4)
-    if motionW > 0 then
+    if motionW ~= 0 then
         BeginAnimationGroup(State.npc_animator, motionW)
             if slots[1] > 0 then PlayAnimationLoop(State.npc_animator, "run_r", slots[1]) end
             if slots[2] > 0 then PlayAnimationLoop(State.npc_animator, "run_fwd_r", slots[2]) end
@@ -1409,7 +1440,7 @@
     end
 
     local crouchW = clamp(AnimCtrl.motionWeight * AnimCtrl.crouch * (1.0 - (AnimCtrl.jump_falling > 0 and 1 or 0)), 0.0, 1.0)
-    if crouchW > 0 then
+    if crouchW ~= 0 then
         BeginAnimationGroup(State.npc_animator, crouchW)
             if slots[1] > 0 then PlayAnimationLoop(State.npc_animator, "crouch_r", slots[1]) end
             if slots[2] > 0 then PlayAnimationLoop(State.npc_animator, "crouch_fwd_r", slots[2]) end
@@ -1463,7 +1494,7 @@
 end
 
 local function updateFear(dt)
-    if State.fear_timer > 0 then
+    if State.fear_timer ~= 0 then
         State.fear_timer = math.max(State.fear_timer - dt, 0)
         CONFIG.detection.player_look_dist = math.min(CONFIG.detection.player_look_dist + dt * 1.5, 7.0)
         CONFIG.detection.backup_dist = math.min(CONFIG.detection.backup_dist + dt * 1.5, 6.0)
@@ -1499,12 +1530,12 @@
 
 function handlePlayerInteraction(dt, bt, pos)
     local grounded = isGroundedCorners(State.base_body)
-    local ppos = GetPlayerTransform().pos
+    local ppos = GetPlayerTransform(playerId).pos
     local to_player = VecSub(ppos, pos)
     local dist_to_player = VecLength(to_player)
 
     local player_tool = GetString("game.player.tool") or ""
-    local player_vehicle = GetPlayerVehicle() or 0
+    local player_vehicle = GetPlayerVehicle(playerId) or 0
     local dangerous = player_vehicle ~= 0 or 
                       player_tool == "gun" or player_tool == "shotgun" or
                       player_tool == "rifle" or player_tool == "rocket" or
@@ -1539,8 +1570,6 @@
         State.player_look_active = false
     end
 end
-
-State.seen_dead_bodies = State.seen_dead_bodies or {}
 
 local function handleDeadBodyDetection(dt, bt, pos)
     if State.ai_state == "panic" or not State.ai_state == "follow" then return end
@@ -1721,7 +1750,6 @@
     State.sound_awareness_timer = max_care_time
 end
 
-
 function handlePanicState(dt, pos)
     __panic_mem = __panic_mem or {}
     local base = State.base_body or 0
@@ -1734,7 +1762,7 @@
     end
 
     State.panic_timer = (State.panic_timer or 0) - dt
-    local src = State.panic_source_pos or GetPlayerTransform().pos
+    local src = State.panic_source_pos or GetPlayerTransform(playerId).pos
 
     local away = VecSub(pos, src)
     away[2] = 0
@@ -1794,7 +1822,7 @@
 
     local grounded = isGroundedCorners(State.base_body)
 
-    if #mem.path_stack > 0 then
+    if #mem.path_stack ~= 0 then
         local lookahead_idx = math.min(3, #mem.path_stack)
         local target_pt = mem.path_stack[lookahead_idx]
 
@@ -1923,7 +1951,7 @@
 
         if ps == "done" then
             local new_points = Pathfinding:samplePath(0.3)
-            if #State.follow_stack > 0 then
+            if #State.follow_stack ~= 0 then
                 for i = 1, #new_points do
                     State.follow_stack[#State.follow_stack + 1] = new_points[i]
                 end
@@ -1967,7 +1995,7 @@
     if priority_type == "medium" then sp = sp - 0.85
     elseif priority_type == "low" then sp = sp - 1.5 end
 
-    if #State.follow_stack > 0 then
+    if #State.follow_stack ~= 0 then
         local next_point = State.follow_stack[1]
         local dir = VecSub(next_point, pos)
         dir[2] = 0
@@ -2015,7 +2043,7 @@
     State.look_pitch_target = clamp(pitch_full, -20, 20)
     State.last_look_update = GetTime()
 
-    local ppos = GetPlayerTransform().pos
+    local ppos = GetPlayerTransform(playerId).pos
     local dist_to_player = VecLength(VecSub(ppos, pos))
     if dist_to_player < CONFIG.detection.backup_dist then
         local back = safeNormalize(VecSub(pos, ppos))
@@ -2090,7 +2118,7 @@
         else
             if ps == "done" then
                 local new_points = Pathfinding:samplePath(0.3) or {}
-                if #mem.path_stack > 0 then
+                if #mem.path_stack ~= 0 then
                     for i = 1, #new_points do
                         mem.path_stack[#mem.path_stack + 1] = new_points[i]
                     end
@@ -2164,10 +2192,10 @@
             end
         end
     end
-    if mem.path_stack and #mem.path_stack > 0 then
+    if mem.path_stack and #mem.path_stack ~= 0 then
         consumeReached(mem.path_stack, pos)
     end
-    if mem.path_stack and #mem.path_stack > 0 then
+    if mem.path_stack and #mem.path_stack ~= 0 then
         local next_point = mem.path_stack[1]
         local to_next = VecSub(next_point, pos)
         to_next[2] = 0
@@ -2220,41 +2248,6 @@
     end
 end
 
-local WeaponState = {
-    held_gun = 0,
-    is_holding_gun = false,
-    gun_grip_strength = 0,
-    gun_aim_mode = false,
-    gun_shoot_cooldown = 0,
-    gun_shoot_delay = 0.35,
-    gun_target = nil,
-    player_aggro = false,
-    player_aggro_timer = 0,
-    
-    held_melee = 0,
-    is_holding_melee = false,
-    melee_grip_strength = 0,
-    melee_swing_stroke = 0.0,
-    melee_swing_hit = false,
-    melee_attack_cooldown = 0,
-    melee_attack_delay = 0.6,
-    melee_target = nil,
-    
-    last_scan_time = 0,
-    scan_interval = 0.2,
-    
-    rest_transform = Transform(Vec(0.35, 1.10, 0.40),QuatEuler(15, 10, -160)),
-    swing_start_transform = Transform(Vec(0.25, 1.60, 0.5),QuatEuler(70, 30.0, -170)),
-    swing_end_transform = Transform(Vec(0.40, 0.65, 0.50),QuatEuler(-40, 40, 165)),
-    
-    SWING_UP = 0.2,
-    SWING_DOWN = 0.3,
-    HIT_THRESHOLD = 0.45,
-    ATTACK_RANGE = 4.0,
-    SWING_SPEED_NORMAL = 2.45,
-    SWING_SPEED_HIT = 1.3
-}
-
 local function transformMix(left, right, t)
     local pos = VecAdd(VecScale(left.pos, 1.0 - t), VecScale(right.pos, t))
     local quat = QuatSlerp(left.rot, right.rot, t)
@@ -2264,8 +2257,6 @@
 local function interpolateCosine(left, right, t)
     return left * (1.0 - math.cos(t * 3.14159265)) * 0.5 + right * (1.0 + math.cos(t * 3.14159265)) * 0.5
 end
-
-local TeamCombat = {damage_registry = {}}
 
 function TeamCombat:getNPCTeam(body)
     if HasTag(body, "TEAM_RED") then return "RED"
@@ -2292,7 +2283,7 @@
         
         if nearest then return nearest, nearest_dist end
         
-        local ppos = GetPlayerTransform().pos
+        local ppos = GetPlayerTransform(playerId).pos
         local player_dist = VecLength(VecSub(ppos, pos))
         if player_dist < nearest_dist then
             return "player", player_dist
@@ -2351,8 +2342,6 @@
         self.damage_registry[target] = nil
     end
 end
-
-local __combat_mem = {}
 
 function TeamCombat:updateMeleeCombat(dt, pos, bt)
     if not State.team and not HasTag(State.base_body, "NPC_AGGRESIVE_MODE") then return false end
@@ -2445,7 +2434,7 @@
         
         local grounded = isGroundedCorners(State.base_body)
         
-        if #mem.path_stack > 0 then
+        if #mem.path_stack ~= 0 then
             local nextPt = mem.path_stack[1]
             local dir    = VecSub(nextPt, pos); dir[2] = 0
             if VecLength(dir) > 0.01 then
@@ -2569,7 +2558,7 @@
     
     local enemy_pos
     if enemy == "player" then
-        enemy_pos = GetPlayerTransform().pos
+        enemy_pos = GetPlayerTransform(playerId).pos
     else
         enemy_pos = GetBodyTransform(enemy).pos
     end
@@ -2633,7 +2622,7 @@
         
         if enemy_dist <= CONFIG.combat.melee_range and State.melee_cooldown <= 0 then
             if enemy == "player" then
-                SetPlayerHealth(GetPlayerHealth() - 0.15)
+                SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.15)
             else
                 self:registerHit(enemy)
                 PlaySound(LoadSound("wood/hit-m0.ogg"),    enemy_pos, 1.5)
@@ -2670,7 +2659,7 @@
     State.punch_right_phase = State.punch_right_phase or 0
     State.punch_left_phase = State.punch_left_phase or 0
     
-    if State.punch_right_phase > 0 then
+    if State.punch_right_phase ~= 0 then
         State.punch_right_phase = State.punch_right_phase + GetTime() * 4.5
         
         if State.punch_right_phase <= 1.0 then
@@ -2720,7 +2709,7 @@
         end
     end
     
-    if State.punch_left_phase > 0 then
+    if State.punch_left_phase ~= 0 then
         State.punch_left_phase = State.punch_left_phase + GetTime() * 4.5
         
         if State.punch_left_phase <= 1.0 then
@@ -2833,7 +2822,7 @@
 
     WeaponState.gun_shoot_cooldown = WeaponState.gun_shoot_cooldown - dt
     WeaponState.melee_attack_cooldown = WeaponState.melee_attack_cooldown - dt
-    if WeaponState.player_aggro_timer and WeaponState.player_aggro_timer > 0 then
+    if WeaponState.player_aggro_timer and WeaponState.player_aggro_timer ~= 0 then
         WeaponState.player_aggro_timer = WeaponState.player_aggro_timer - dt
     else
         WeaponState.player_aggro = false
@@ -2971,7 +2960,7 @@
             if b ~= 0 and IsHandleValid(b) and IsBodyBroken(b) and (HasTag(b, "NPC_ZOMBIE_MODE") or HasTag(b, "NPC_AGGRESIVE_MODE")) then
                 local bp = GetBodyTransform(b).pos
                 if VecLength(VecSub(bp, npc_pos)) < 12 then
-                    local ppos = GetPlayerTransform().pos
+                    local ppos = GetPlayerTransform(playerId).pos
                     if VecLength(VecSub(ppos, bp)) < 6 then
                         WeaponState.player_aggro = true
                         WeaponState.player_aggro_timer = 12
@@ -2982,7 +2971,7 @@
     end
 
     if (not target_body) and (WeaponState.player_aggro or HasTag(State.base_body, "NPC_AGGRESIVE_MODE")) then
-        local ppos = GetPlayerTransform().pos
+        local ppos = GetPlayerTransform(playerId).pos
         if VecLength(VecSub(ppos, npc_pos)) < 60 then
             local eye = VecAdd(npc_pos, Vec(0, 1.5, 0))
             local to = VecSub(ppos, eye)
@@ -3035,7 +3024,7 @@
         local desired_pos, desired_rot
         if WeaponState.gun_aim_mode and target_pos then
             if WeaponState.gun_target == "player" then
-                target_pos = VecAdd(GetPlayerTransform().pos, Vec(0, 1.5, 0))
+                target_pos = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1.5, 0))
             elseif IsHandleValid(WeaponState.gun_target) then
                 target_pos = VecAdd(GetBodyTransform(WeaponState.gun_target).pos, Vec(0, 1.5, 0))
             end
@@ -3079,10 +3068,10 @@
         local muzzle = muzzle_light and GetLightTransform(muzzle_light) or Transform(TransformToParentPoint(Transform(spos, srot), Vec(0, 0, 0.6)), srot)
         State.weapon_muzzle_transform = muzzle
         
-        if WeaponState.shoot_light_timer and WeaponState.shoot_light_timer > 0 then
+        if WeaponState.shoot_light_timer and WeaponState.shoot_light_timer ~= 0 then
             WeaponState.shoot_light_timer = WeaponState.shoot_light_timer - dt
             local fade_dur = is_gun and 0.09 or (is_shotgun and 0.18 or 0)
-            if fade_dur > 0 then
+            if fade_dur ~= 0 then
                 local t = math.max(0, WeaponState.shoot_light_timer / fade_dur)
                 local inten = t * (is_gun and 1.5 or 2)
                 if WeaponState.shoot_light_id then RemoveLight(WeaponState.shoot_light_id) end
@@ -3175,7 +3164,7 @@
 
             local grounded = isGroundedCorners(State.base_body)
             
-            if WeaponState.in_cover_move and WeaponState.cover_timer > 0 then
+            if WeaponState.in_cover_move and WeaponState.cover_timer ~= 0 then
                 WeaponState.cover_timer = WeaponState.cover_timer - dt
                 
                 if not WeaponState.cover_direction then
@@ -3248,7 +3237,7 @@
                     local st = GetPathState()
                     if st == "done" then
                         local len = GetPathLength()
-                        if len > 0 then
+                        if len ~= 0 then
                             Pathfinding:advanceProgress()
                             
                             local lookProg = clamp((State.path_progress or 0) + 0.1, 0, len)
@@ -3354,7 +3343,7 @@
             end
         end
 
-        if WeaponState.melee_swing_stroke > 0 then
+        if WeaponState.melee_swing_stroke ~= 0 then
             local oldStroke = WeaponState.melee_swing_stroke
             local strokeSpeed = WeaponState.melee_swing_hit and WeaponState.SWING_SPEED_HIT or WeaponState.SWING_SPEED_NORMAL
             WeaponState.melee_swing_stroke = WeaponState.melee_swing_stroke + strokeSpeed * dt
@@ -3364,7 +3353,7 @@
                     local dist = VecLength(VecSub(target_pos, npc_pos))
                     if dist < WeaponState.ATTACK_RANGE + 1.0 then
                         if WeaponState.melee_target == "player" then
-                            SetPlayerHealth(GetPlayerHealth() - 0.2)
+                            SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.2)
                         else
                             local attack_dir = VecNormalize(VecSub(target_pos, npc_pos))
                             local btgt = GetBodyTransform(WeaponState.melee_target)
@@ -3451,8 +3440,6 @@
     end
 end
 
-local __zombie_mem = {}
-
 local function clamp(v, a, b) if v < a then return a elseif v > b then return b end return v end
 
 local function safeNormalize(v)
@@ -3505,7 +3492,7 @@
     local targetPos, isPlayerTarget
     local best = TARGET_SCAN_RANGE
 
-    local ptrans = GetPlayerTransform()
+    local ptrans = GetPlayerTransform(playerId)
     if ptrans then
         local d = VecLength(VecSub(ptrans.pos, pos))
         if d < best then best = d; targetPos = ptrans.pos; isPlayerTarget = true end
@@ -3540,7 +3527,7 @@
 
         if ps == "done" then
             local new_points = Pathfinding:samplePath(0.3)
-            if #mem.path_stack > 0 then
+            if #mem.path_stack ~= 0 then
                 for i = 1, #new_points do
                     mem.path_stack[#mem.path_stack + 1] = new_points[i]
                 end
@@ -3594,7 +3581,7 @@
             end
         end
 
-    elseif #mem.path_stack > 0 then
+    elseif #mem.path_stack ~= 0 then
         local next_point = mem.path_stack[1]
         local dir = VecSub(next_point, pos)
         dir[2] = 0
@@ -3645,7 +3632,7 @@
         end
         if dist_to_target <= ATTACK_DIST and mem.attack_timer <= 0 then
             if isPlayerTarget then
-                SetPlayerHealth(GetPlayerHealth() - 0.15)
+                SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.15)
             end
             mem.attack_timer = ATTACK_COOLDOWN
         end
@@ -3746,7 +3733,7 @@
         consumeReached(mem.path_stack, pos)
 
         local grounded = isGroundedCorners(State.base_body)
-        if #mem.path_stack > 0 then
+        if #mem.path_stack ~= 0 then
             local nextPt = mem.path_stack[1]
             local dir    = VecSub(nextPt, pos); dir[2] = 0
             if VecLength(dir) > 0.01 then
@@ -4177,7 +4164,7 @@
     local _, cy = GetQuatEuler(bt.rot)
     State.desired_yaw = State.desired_yaw or cy
 
-    if State.panic_lock and State.panic_lock > 0 then
+    if State.panic_lock and State.panic_lock ~= 0 then
         State.panic_lock = State.panic_lock - dt
         State.ai_state = "panic"
         handlePanicState(dt, pos)
@@ -4235,7 +4222,7 @@
 
         local target_body_pos
         if WeaponState.current_target == "player" then
-            target_body_pos = GetPlayerTransform().pos
+            target_body_pos = GetPlayerTransform(playerId).pos
         else
             if IsHandleValid(WeaponState.current_target) then
                 target_body_pos = GetBodyTransform(WeaponState.current_target).pos
@@ -4381,7 +4368,7 @@
         local voxels_lost = State.initial_voxel_count - current_voxel_count
         local loss_ratio = 0
         
-        if State.initial_voxel_count > 0 then
+        if State.initial_voxel_count ~= 0 then
             loss_ratio = voxels_lost / State.initial_voxel_count
         end
 
@@ -4410,6 +4397,7 @@
 end
 
 local function clamp(x,a,b) if x<a then return a end if x>b then return b end return x end
+
 local function lerp(a,b,t) return a + (b-a)*clamp(t,0,1) end
 
 function updateBloodEffects(dt)
@@ -4539,288 +4527,284 @@
     end
 end
 
-function init()
-    State.npc_animator = FindAnimator(CONFIG.tags.npc)
-    State.base_body = FindBody(CONFIG.tags.body)
-    State.idle_timer = math.random(CONFIG.timers.idle_min * 100, CONFIG.timers.idle_max * 100) / 100
-    
-   -- small preload tweaks (replace preload block inside init)
-	if State.npc_animator ~= 0 then
-		local preload_anims = {
-			"idle_1", "idle_2", "idle_3", "idle_4", "idle_5",
-			CONFIG.animations.default_idle, "crouch_idle",
-			"run_fwd", "run_bwd", "run_l", "run_r",
-			"run_fwd_l", "run_fwd_r", "run_bwd_l", "run_bwd_r",
-			"crouch_fwd", "crouch_bwd", "crouch_l", "crouch_r",
-			"turn_l", "turn_r",
-			"jump_start", "jump_loop", "jump_land",
-			"swim", "emote_1"
-		}
-		for _, a in ipairs(preload_anims) do
-			PlayAnimationLoop(State.npc_animator, a, 0)
-			SetAnimationClipFade(State.npc_animator, a, CONFIG.animation.fade_fast, CONFIG.animation.fade_fast)
-		end
-		-- randomize idle loop start to avoid synced snaps
-		SetAnimationClipLoopPosition(State.npc_animator, "idle_1", math.random(0,1000) * 0.01)
-		SetAnimationClipLoopPosition(State.npc_animator, "idle_2", math.random(0,1000) * 0.01)
-		SetAnimationClipLoopPosition(State.npc_animator, "idle_3", math.random(0,1000) * 0.01)
-		SetAnimationClipLoopPosition(State.npc_animator, "idle_4", math.random(0,1000) * 0.01)
-		SetAnimationClipLoopPosition(State.npc_animator, "idle_5", math.random(0,1000) * 0.01)
-		SetAnimationClipLoopPosition(State.npc_animator, "crouch_idle", math.random(0,1000) * 0.01)
-	end
-	
-	local shapes = GetBodyShapes(State.base_body)
-	for i=1,#shapes do
-		local s = shapes[i]
-		local sx, sy, sz = GetShapeSize(s)
-		if sx and sy and sz then
-			ResizeShape(s, 0, 0, 0, sx, 16, sz)
-		end
-	end
-	
-	Zombified = false
-	BloodDisabled = false
-	tim = 0
-	
-	State.sprite_handle = LoadSprite("ui/common/dot.png")
-	
-	if State.base_body ~= 0 then
-		local shapes = GetBodyShapes(State.base_body)
-		State.initial_voxel_count = 0
-		for i = 1, #shapes do
-			local x, y, z = GetShapeSize(shapes[i])
-			State.initial_voxel_count = State.initial_voxel_count + (x * y * z * 10 * 10 * 10)
-		end
-	end
-    
-    FaceManager:set("Neutral")
-end
-
-function tick(dt)
-    if State.npc_animator == 0 then State.npc_animator = FindAnimator(CONFIG.tags.npc) end
-    if State.base_body == 0 then State.base_body = FindBody(CONFIG.tags.body) end
-	
-	if not HasTag(State.base_body, "NPC_NOT_HUMAN") then
-		updateBloodEffects(dt)
-	end
-    checkRagdoll()
-    if State.ragdoll_active then
-        handleDeath(dt)
-        return
-    end
-	
-	updateFallDamage(dt)
-	
-	local base = State.base_body
-	local bt = GetBodyTransform(State.base_body)
-	local r = math.random
-	if HasTag(base, "NPC_ZOMBIE_MODE") and not Zombified and not HasTag(base, "NPC_NOINFECTABLE") then
-		PaintRGBA(VecAdd(bt.pos, Vec(r(-0.2, 0.2),r(0.25, 2.0),r(-0.2, 0.2))), 0.5+r(-0.25, 0.25), 0.25, 0.02, 0.0, 1, 1)
-		PaintRGBA(VecAdd(bt.pos, Vec(r(-0.5, 0.5),r(0.0, 2.0),r(-0.5, 0.5))), 1.5+r(-0.15, 0.15), 0.4+r(-0.15, 0.15), 0.6+r(-0.15, 0.15), 0.15+r(-0.15, 0.15), 1, 0.15+r(-0.15, 0.15))
-		PaintRGBA(VecAdd(bt.pos, Vec(r(-0.5, 0.5),1.25,r(-0.5, 0.5))), 2.5+r(-0.15, 0.15), 0.4+r(-0.15, 0.15), 0.6+r(-0.15, 0.15), 0.5+r(-0.15, 0.15), 0.4, 1)
-		State.disable_ai = true
-		Zombified = true
-		local shapes = GetBodyShapes(State.base_body)
-		for i=1,#shapes do
-			local shape = shapes[i]
-			-- SetShapeDensity(shapes[i], 5)
-			SetTag(shape, "invisible")
-		end
-	end
-	
-	if Zombified then
-		ChasePlayerZombie(dt, grounded, pos, bt)
-		if State.npc_animator ~= 0 then
-			RotateBone(State.npc_animator, "arm_upper_l", QuatEuler(-75, 0, 15), 1)
-			RotateBone(State.npc_animator, "arm_lower_l", QuatEuler(-45, 0, 10), 1)
-			RotateBone(State.npc_animator, "arm_upper_r", QuatEuler(-75, 0, -15), 1)
-			RotateBone(State.npc_animator, "arm_lower_r", QuatEuler(-45, 0, -10), 1)
-		end
-	end
-    
-    local grounded = isGroundedCorners(State.base_body)
-	local in_water, water_depth = isInWater(State.base_body)
-
-	updateFear(dt)
-
-	if not State.disable_ai then
-		updateAI(dt, grounded)
-	end
-
-	updateFacialExpressions(grounded, in_water)
-	updateAnimation(dt, grounded, in_water)
-	NPC_GrabAndHoldWeapon()
-    
-    if HasTag(State.base_body, "Crucifixed") then
-        playStruggle(dt, State.npc_animator)
-    end
-    
-    -- Wave cooldown
-    if State.wave_cooldown > 0 then
-        State.wave_cooldown = math.max(State.wave_cooldown - dt, 0)
-    end
-    
-    if State.is_waving then
-        State.waving_timer = State.waving_timer - dt
-        if State.waving_timer <= 0 then
-            State.is_waving = false
-            State.waving_timer = 0
-            State.ai_state = "idle"
-            State.idle_timer = math.random(CONFIG.timers.idle_min * 100, CONFIG.timers.idle_max * 100) / 100
-        else
-            FaceManager:set("Happy")
-        end
-    end
-    
-    -- Footsteps
-    local vel = GetBodyVelocity(State.base_body)
-    vel[2] = 0
-    local speed = VecLength(vel)
-    local anim_mult = clamp(speed / 3.5, 0.5, 2.0)
-    
-    SoundSystem:updateFootsteps(dt, grounded, anim_mult)
-    
-    State.was_grounded = grounded
-    
-    -- Wither storm interaction
-    if HasTag(FindBody("WITHER_STORM", true), "WITHER_STORM") then
-        FaceManager:set("Surprised")
-        if State.disable_ai and math.random(1, 1500) == 1500 then
-            local messages = {
-                "HELP!",
-                "I CAN'T MOVE!!",
-                "PLEASE TURN ON MY AI!",
-                "WITHER IS ATTACKING, TURN ON MY AI!!!",
-                "I'M IN DANGER!"
-            }
-            DebugPrint(messages[math.random(1, #messages)])
-        end
-    end
-end
-
-function update()
-    if not isValidBody(State.base_body) then
-        if State.npc_animator ~= 0 then FaceManager:set("Blink") MakeRagdoll(State.npc_animator)  end
-        return
-    end
-    local bt = GetBodyTransform(State.base_body)
-    FaceManager:apply()
-
-    local tnow = GetTime()
-    local _, cur_yaw, _ = GetQuatEuler(bt.rot)
-    
-    local npc_head_pos = VecAdd(bt.pos, Vec(0, 1.625, 0))
-    
-    local target_yaw = cur_yaw
-    local target_pitch = 0
-
-    if State.player_look_active and State.last_look_update and (tnow - State.last_look_update) < 0.3 then
-        target_yaw = State.desired_yaw or cur_yaw
-        target_pitch = State.look_pitch_target or 0
-    elseif State.curious_timer and State.curious_timer > 0 then
-        target_yaw = State.curious_yaw_target or cur_yaw
-        target_pitch = State.curious_pitch_target or 0
-        State.curious_timer = State.curious_timer - GetTimeStep()
-        
-        if State.curious_face then
-            local relative_yaw = normalizeAngleDeg(target_yaw - cur_yaw)
-            
-            if relative_yaw < -25 then
-                FaceManager:set("Lookl")
-            elseif relative_yaw > 25 then
-                FaceManager:set("Lookr")
-            else
-                FaceManager:set("Look")
-            end
-        end
-        
-        if State.curious_timer <= 0 then
-            State.curious_face = nil
-        end
-    else
-        target_yaw = State.desired_yaw or cur_yaw
-        target_pitch = 0
-    end
-    
-    local yaw_diff = normalizeAngleDeg(target_yaw - cur_yaw)
-
-    local max_head = 45
-    State.head_yaw = State.head_yaw or 0
-    local head_target = clamp(yaw_diff, -max_head, max_head)
-    State.head_yaw = smoothLerp(State.head_yaw, head_target, GetTimeStep(), 6.0)
-
-    State.look_pitch = State.look_pitch or 0
-    State.look_pitch = smoothLerp(State.look_pitch, target_pitch, GetTimeStep(), 6.0)
-
+function server.init()
+       State.npc_animator = FindAnimator(CONFIG.tags.npc)
+       State.base_body = FindBody(CONFIG.tags.body)
+       State.idle_timer = math.random(CONFIG.timers.idle_min * 100, CONFIG.timers.idle_max * 100) / 100
+      -- small preload tweaks (replace preload block inside init)
     if State.npc_animator ~= 0 then
-        local head_pitch_factor = 1.5
-        local chest_pitch_factor = 0.5
-        
-        RotateBone(State.npc_animator, "head", 
-                   QuatEuler(State.head_yaw, 0, State.look_pitch * head_pitch_factor), 1.0)
-        RotateBone(State.npc_animator, "chest", 
-                   QuatEuler(State.head_yaw * 0.5, 0, State.look_pitch * chest_pitch_factor), 1.0)
-    end
-	
-	if HasTag(State.base_body, "TEAM_RED") and not HasTag(State.base_body, "TEAM_BLUE") then
-		State.team = "RED"
-	end
-	
-	if HasTag(State.base_body, "TEAM_BLUE") and not HasTag(State.base_body, "TEAM_RED") then
-		State.team = "BLUE"
-	end
-	
-	updatePunchAnimation(dt, State.npc_animator)
-
-    local head_gap = math.abs(State.head_yaw - yaw_diff)
-    local body_speed = (head_gap < 6) and CONFIG.movement.rot_speed or (CONFIG.movement.rot_speed * 0.28)
-    ConstrainOrientation(State.base_body, 0, bt.rot, QuatEuler(0, target_yaw, 0), body_speed)
-	
-	if State.npc_animator == 0 then return end
-	local dt = GetTimeStep()
-	local mem = __zombie_mem[State.base_body] or {}
-	mem.head_weight = smoothLerp(mem.head_weight or 0, 1.0, dt, 6.0)
-
-	local head_yaw = State.head_yaw or 0
-	local head_pitch = State.look_pitch or 0
-
-	-- apply to bones (weights tuned small)
-	RotateBone(State.npc_animator, "head", QuatEuler(-head_yaw * 0.9, head_pitch * 0.7, 0), mem.head_weight)
-	RotateBone(State.npc_animator, "neck", QuatEuler(-head_yaw * 0.5, head_pitch * 0.35, 0), mem.head_weight * 0.85)
-	RotateBone(State.npc_animator, "chest", QuatEuler(-head_yaw * 0.15, head_pitch * 0.15, 0), mem.head_weight * 0.5)
-
-    if State.npc_animator ~= 0 then SetAnimatorTransform(State.npc_animator, GetBodyTransform(State.base_body)) end
-
-    SetTag(State.npc_animator, "NPC_SECRET_DOOR_COMPATIBILITY")
-    SetTag(State.npc_animator, "NPC_SECRET_TOOL_COMPATIBILITY")
-    SetTag(State.npc_animator, "npc_animator")
-    SetTag(State.base_body, "NPC_SECRET_DOOR_COMPATIBILITY")
-    SetTag(State.base_body, "npc_base")
-    SetTag(State.base_body, "inherittags")
-    SetTag(State.base_body, "NPC_SECRET_TOOL_COMPATIBILITY")
-	
-	if State.ragdoll_active then
-		FaceManager:set("Blink")
-		SetTag(State.base_body, "attachment")
-
-		local stomach = FindBody("stomach")
-		if stomach ~= 0 then
-			local t = GetBodyTransform(stomach)
-			local com = GetBodyCenterOfMass(stomach)
-			t.pos = TransformToParentPoint(t, com)
-			SetBodyTransform(State.base_body, t)
-		end
-	end
-	
-	local Shapes = GetBodyShapes(State.base_body)
-	for i=1,#Shapes do
-		SetProperty(Shapes[i], "strength", 4.0)
-	end
-	
-	-- SetProperty(State.base_body, "friction", 2)
-end
-
-function draw()
+    	local preload_anims = {
+    		"idle_1", "idle_2", "idle_3", "idle_4", "idle_5",
+    		CONFIG.animations.default_idle, "crouch_idle",
+    		"run_fwd", "run_bwd", "run_l", "run_r",
+    		"run_fwd_l", "run_fwd_r", "run_bwd_l", "run_bwd_r",
+    		"crouch_fwd", "crouch_bwd", "crouch_l", "crouch_r",
+    		"turn_l", "turn_r",
+    		"jump_start", "jump_loop", "jump_land",
+    		"swim", "emote_1"
+    	}
+    	for _, a in ipairs(preload_anims) do
+    		PlayAnimationLoop(State.npc_animator, a, 0)
+    		SetAnimationClipFade(State.npc_animator, a, CONFIG.animation.fade_fast, CONFIG.animation.fade_fast)
+    	end
+    	-- randomize idle loop start to avoid synced snaps
+    	SetAnimationClipLoopPosition(State.npc_animator, "idle_1", math.random(0,1000) * 0.01)
+    	SetAnimationClipLoopPosition(State.npc_animator, "idle_2", math.random(0,1000) * 0.01)
+    	SetAnimationClipLoopPosition(State.npc_animator, "idle_3", math.random(0,1000) * 0.01)
+    	SetAnimationClipLoopPosition(State.npc_animator, "idle_4", math.random(0,1000) * 0.01)
+    	SetAnimationClipLoopPosition(State.npc_animator, "idle_5", math.random(0,1000) * 0.01)
+    	SetAnimationClipLoopPosition(State.npc_animator, "crouch_idle", math.random(0,1000) * 0.01)
+    end
+    local shapes = GetBodyShapes(State.base_body)
+    for i=1,#shapes do
+    	local s = shapes[i]
+    	local sx, sy, sz = GetShapeSize(s)
+    	if sx and sy and sz then
+    		ResizeShape(s, 0, 0, 0, sx, 16, sz)
+    	end
+    end
+    Zombified = false
+    BloodDisabled = false
+    tim = 0
+    State.sprite_handle = LoadSprite("ui/common/dot.png")
+    if State.base_body ~= 0 then
+    	local shapes = GetBodyShapes(State.base_body)
+    	State.initial_voxel_count = 0
+    	for i = 1, #shapes do
+    		local x, y, z = GetShapeSize(shapes[i])
+    		State.initial_voxel_count = State.initial_voxel_count + (x * y * z * 10 * 10 * 10)
+    	end
+    end
+       FaceManager:set("Neutral")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           if State.npc_animator == 0 then State.npc_animator = FindAnimator(CONFIG.tags.npc) end
+           if State.base_body == 0 then State.base_body = FindBody(CONFIG.tags.body) end
+
+        if not HasTag(State.base_body, "NPC_NOT_HUMAN") then
+        	updateBloodEffects(dt)
+        end
+           checkRagdoll()
+           if State.ragdoll_active then
+               handleDeath(dt)
+               return
+           end
+
+        updateFallDamage(dt)
+
+        local base = State.base_body
+        local bt = GetBodyTransform(State.base_body)
+        local r = math.random
+        if HasTag(base, "NPC_ZOMBIE_MODE") and not Zombified and not HasTag(base, "NPC_NOINFECTABLE") then
+        	PaintRGBA(VecAdd(bt.pos, Vec(r(-0.2, 0.2),r(0.25, 2.0),r(-0.2, 0.2))), 0.5+r(-0.25, 0.25), 0.25, 0.02, 0.0, 1, 1)
+        	PaintRGBA(VecAdd(bt.pos, Vec(r(-0.5, 0.5),r(0.0, 2.0),r(-0.5, 0.5))), 1.5+r(-0.15, 0.15), 0.4+r(-0.15, 0.15), 0.6+r(-0.15, 0.15), 0.15+r(-0.15, 0.15), 1, 0.15+r(-0.15, 0.15))
+        	PaintRGBA(VecAdd(bt.pos, Vec(r(-0.5, 0.5),1.25,r(-0.5, 0.5))), 2.5+r(-0.15, 0.15), 0.4+r(-0.15, 0.15), 0.6+r(-0.15, 0.15), 0.5+r(-0.15, 0.15), 0.4, 1)
+        	State.disable_ai = true
+        	Zombified = true
+        	local shapes = GetBodyShapes(State.base_body)
+        	for i=1,#shapes do
+        		local shape = shapes[i]
+        		-- SetShapeDensity(shapes[i], 5)
+        		SetTag(shape, "invisible")
+        	end
+        end
+
+        if Zombified then
+        	ChasePlayerZombie(dt, grounded, pos, bt)
+        	if State.npc_animator ~= 0 then
+        		RotateBone(State.npc_animator, "arm_upper_l", QuatEuler(-75, 0, 15), 1)
+        		RotateBone(State.npc_animator, "arm_lower_l", QuatEuler(-45, 0, 10), 1)
+        		RotateBone(State.npc_animator, "arm_upper_r", QuatEuler(-75, 0, -15), 1)
+        		RotateBone(State.npc_animator, "arm_lower_r", QuatEuler(-45, 0, -10), 1)
+        	end
+        end
+
+           local grounded = isGroundedCorners(State.base_body)
+        local in_water, water_depth = isInWater(State.base_body)
+
+        updateFear(dt)
+
+        if not State.disable_ai then
+        	updateAI(dt, grounded)
+        end
+
+        updateFacialExpressions(grounded, in_water)
+        updateAnimation(dt, grounded, in_water)
+        NPC_GrabAndHoldWeapon()
+
+           if HasTag(State.base_body, "Crucifixed") then
+               playStruggle(dt, State.npc_animator)
+           end
+
+           -- Wave cooldown
+           if State.wave_cooldown ~= 0 then
+               State.wave_cooldown = math.max(State.wave_cooldown - dt, 0)
+           end
+
+           if State.is_waving then
+               State.waving_timer = State.waving_timer - dt
+               if State.waving_timer <= 0 then
+                   State.is_waving = false
+                   State.waving_timer = 0
+                   State.ai_state = "idle"
+                   State.idle_timer = math.random(CONFIG.timers.idle_min * 100, CONFIG.timers.idle_max * 100) / 100
+               else
+                   FaceManager:set("Happy")
+               end
+           end
+
+           -- Footsteps
+           local vel = GetBodyVelocity(State.base_body)
+           vel[2] = 0
+           local speed = VecLength(vel)
+           local anim_mult = clamp(speed / 3.5, 0.5, 2.0)
+
+           SoundSystem:updateFootsteps(dt, grounded, anim_mult)
+
+           State.was_grounded = grounded
+
+           -- Wither storm interaction
+           if HasTag(FindBody("WITHER_STORM", true), "WITHER_STORM") then
+               FaceManager:set("Surprised")
+               if State.disable_ai and math.random(1, 1500) == 1500 then
+                   local messages = {
+                       "HELP!",
+                       "I CAN'T MOVE!!",
+                       "PLEASE TURN ON MY AI!",
+                       "WITHER IS ATTACKING, TURN ON MY AI!!!",
+                       "I'M IN DANGER!"
+                   }
+                   DebugPrint(messages[math.random(1, #messages)])
+               end
+           end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           if not isValidBody(State.base_body) then
+               if State.npc_animator ~= 0 then FaceManager:set("Blink") MakeRagdoll(State.npc_animator)  end
+               return
+           end
+           local bt = GetBodyTransform(State.base_body)
+           FaceManager:apply()
+
+           local tnow = GetTime()
+           local _, cur_yaw, _ = GetQuatEuler(bt.rot)
+
+           local npc_head_pos = VecAdd(bt.pos, Vec(0, 1.625, 0))
+
+           local target_yaw = cur_yaw
+           local target_pitch = 0
+
+           if State.player_look_active and State.last_look_update and (tnow - State.last_look_update) < 0.3 then
+               target_yaw = State.desired_yaw or cur_yaw
+               target_pitch = State.look_pitch_target or 0
+           elseif State.curious_timer and State.curious_timer ~= 0 then
+               target_yaw = State.curious_yaw_target or cur_yaw
+               target_pitch = State.curious_pitch_target or 0
+               State.curious_timer = State.curious_timer - GetTimeStep()
+
+               if State.curious_face then
+                   local relative_yaw = normalizeAngleDeg(target_yaw - cur_yaw)
+
+                   if relative_yaw < -25 then
+                       FaceManager:set("Lookl")
+                   elseif relative_yaw > 25 then
+                       FaceManager:set("Lookr")
+                   else
+                       FaceManager:set("Look")
+                   end
+               end
+
+               if State.curious_timer <= 0 then
+                   State.curious_face = nil
+               end
+           else
+               target_yaw = State.desired_yaw or cur_yaw
+               target_pitch = 0
+           end
+
+           local yaw_diff = normalizeAngleDeg(target_yaw - cur_yaw)
+
+           local max_head = 45
+           State.head_yaw = State.head_yaw or 0
+           local head_target = clamp(yaw_diff, -max_head, max_head)
+           State.head_yaw = smoothLerp(State.head_yaw, head_target, GetTimeStep(), 6.0)
+
+           State.look_pitch = State.look_pitch or 0
+           State.look_pitch = smoothLerp(State.look_pitch, target_pitch, GetTimeStep(), 6.0)
+
+           if State.npc_animator ~= 0 then
+               local head_pitch_factor = 1.5
+               local chest_pitch_factor = 0.5
+
+               RotateBone(State.npc_animator, "head", 
+                          QuatEuler(State.head_yaw, 0, State.look_pitch * head_pitch_factor), 1.0)
+               RotateBone(State.npc_animator, "chest", 
+                          QuatEuler(State.head_yaw * 0.5, 0, State.look_pitch * chest_pitch_factor), 1.0)
+           end
+
+        if HasTag(State.base_body, "TEAM_RED") and not HasTag(State.base_body, "TEAM_BLUE") then
+        	State.team = "RED"
+        end
+
+        if HasTag(State.base_body, "TEAM_BLUE") and not HasTag(State.base_body, "TEAM_RED") then
+        	State.team = "BLUE"
+        end
+
+        updatePunchAnimation(dt, State.npc_animator)
+
+           local head_gap = math.abs(State.head_yaw - yaw_diff)
+           local body_speed = (head_gap < 6) and CONFIG.movement.rot_speed or (CONFIG.movement.rot_speed * 0.28)
+           ConstrainOrientation(State.base_body, 0, bt.rot, QuatEuler(0, target_yaw, 0), body_speed)
+
+        if State.npc_animator == 0 then return end
+        local dt = GetTimeStep()
+        local mem = __zombie_mem[State.base_body] or {}
+        mem.head_weight = smoothLerp(mem.head_weight or 0, 1.0, dt, 6.0)
+
+        local head_yaw = State.head_yaw or 0
+        local head_pitch = State.look_pitch or 0
+
+        -- apply to bones (weights tuned small)
+        RotateBone(State.npc_animator, "head", QuatEuler(-head_yaw * 0.9, head_pitch * 0.7, 0), mem.head_weight)
+        RotateBone(State.npc_animator, "neck", QuatEuler(-head_yaw * 0.5, head_pitch * 0.35, 0), mem.head_weight * 0.85)
+        RotateBone(State.npc_animator, "chest", QuatEuler(-head_yaw * 0.15, head_pitch * 0.15, 0), mem.head_weight * 0.5)
+
+           if State.npc_animator ~= 0 then SetAnimatorTransform(State.npc_animator, GetBodyTransform(State.base_body)) end
+
+           SetTag(State.npc_animator, "NPC_SECRET_DOOR_COMPATIBILITY")
+           SetTag(State.npc_animator, "NPC_SECRET_TOOL_COMPATIBILITY")
+           SetTag(State.npc_animator, "npc_animator")
+           SetTag(State.base_body, "NPC_SECRET_DOOR_COMPATIBILITY")
+           SetTag(State.base_body, "npc_base")
+           SetTag(State.base_body, "inherittags")
+           SetTag(State.base_body, "NPC_SECRET_TOOL_COMPATIBILITY")
+
+        if State.ragdoll_active then
+        	FaceManager:set("Blink")
+        	SetTag(State.base_body, "attachment")
+
+        	local stomach = FindBody("stomach")
+        	if stomach ~= 0 then
+        		local t = GetBodyTransform(stomach)
+        		local com = GetBodyCenterOfMass(stomach)
+        		t.pos = TransformToParentPoint(t, com)
+        		SetBodyTransform(State.base_body, t)
+        	end
+        end
+
+        local Shapes = GetBodyShapes(State.base_body)
+        for i=1,#Shapes do
+        	SetProperty(Shapes[i], "strength", 4.0)
+        end
+    end
+end
+
+function client.draw()
     if State.ragdoll_active or not State.team then return end
 
     local body_t = GetBodyTransform(State.base_body)
@@ -4837,4 +4821,5 @@
     local a = 1.0
 
     DrawSprite(State.sprite_handle, sprite_transform, 0.125, 0.125, r, g, b, a, false, false, false)
-end+end
+

```

---

# Migration Report: PlayerAiTestoldest.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/PlayerAiTestoldest.lua
+++ patched/PlayerAiTestoldest.lua
@@ -1,4 +1,4 @@
--- CONFIG
+#version 2
 local NPC_TAG = ""
 local BODY_TAG = "npc_base"
 local IDLE_POOL = {"idle_1", "idle_2", "idle_3", "idle_4", "idle_5"}
@@ -6,7 +6,6 @@
 local tim = 0
 local timer = 0
 local particleDeath = false
-
 local SPEED_RUN = 7.0
 local SPEED_WALK = 0.01
 local ANGULAR_TURN = 15.0
@@ -14,9 +13,7 @@
 local FADE_FAST = 0.15
 local FADE_SLOW = 0.35
 local PLAYER_LOOK_DIST = 3.0
-
 local WALK_SPEED = -7.0
-
 local wanderTimer = 0
 local WANDER_TIME_MIN = 3
 local WANDER_TIME_MAX = 7
@@ -24,7 +21,6 @@
 local IDLE_MAX = 60
 local ROT_SPEED = 9.0
 local LOOK_TURN_THRESHOLD = 4.0
-
 local BACKUP_DIST = 2.0
 local BACKUP_MARGIN = 0.3
 local RANDOM_WALK_RADIUS = 10.0
@@ -33,39 +29,31 @@
 local LOOK_UPWARD_BIAS = 0.1
 local PATH_LOOKAHEAD = 0.5
 local LOS_CHECK_STEP = 0.2
-
 local rotatingToRandomYaw = false
 local randomYawTarget = 0
 local GroundSound = nil
-
 local NPC_HEIGHT = 1.0
 local CROUCH_TRIGGER_GAP = 0.5
 local CROUCH_SMOOTH = 6.0
 local TURN_MIN_SPEED = 1.0
 local TURN_WEIGHT_SCALE = 1.0
-
 local npc_animator = 0
 local base_body = 0
-
 local waveCooldown = 0
 local wavingTimer = 0
 local isWaving = false
 local lastWaveTarget = 0
-
 local faceTargetBody = 0
 local faceLookTimer = 0
-
 local FACE_YAW_THRESHOLD = 12
 local FACE_HOLD_TIME = 0.35
 local WAVING_TAG = "WAVING"
 local WAVING_TIME = 3.5
-
 local fearTimer = 0
 local waveLink = 0
 local lastDeathCheck = 0
 local trust = 1
 local deathCount = 0
-
 local air_state = "ground"
 local ragdollActive = false
 local aiState = "idle"
@@ -77,35 +65,16 @@
 local stepTimer = 0
 local strafeTimer = 0
 local strafeDir = nil
-
 local pathPlannerId = 0
 local pathTarget = nil
 local pathProgress = 0
 local pathLength = 0
 local repathTimer = 0
-
 local struggleTimer  = 0.0
 local struggleWeight = 0.0
-
-local function ease01(x) return x*x*(3-2*x) end
-
-local function smoothLerp(cur, target, dt, speed)
-    dt = tonumber(dt) or 0
-    if dt < 0 then dt = 0 end
-    speed = tonumber(speed) or 0
-    local t = dt * speed
-    if t > 1 then t = 1 end
-    return cur + (target - cur) * ease01(t)
-end
-
-local function clamp(v,a,b)
-	if v<a then return a elseif v>b then return b else return v end
-end
-
 local GroundSound = false
 local stepPhase = 0.0
 local stepThreshold = 0.625
-
 local materialSounds = {
     wood     = "wood",
     masonry  = "masonry",
@@ -118,6 +87,45 @@
     water    = "water",
     ice      = "ice"
 }
+local animCtrl = {
+	crouch = 0.0,
+	jumpFalling = 0.0,
+	turnWeight = 0.0,
+	lastGrounded = true,
+	animSpeedMult = 1.0
+}
+local faceTags = {"Neutral", "Blink", "Angry", "Happy", "Surprised", "Fall", "Look", "Lookr", "Lookl"}
+local nextFace = nil
+local lastAppliedFace = nil
+local steerDir = Vec(0,0,1)
+local steerFade = 0.0
+local sidestepStrength = 0.0
+local lastObstacleCheck = 0
+local path = {}
+local lastRepathTime = 0
+local repathInterval = 0.3
+local path = {}
+local lastRepathTime = 0
+local repathInterval = 0.3
+local USE_DIAGONALS = true
+local VEL_SMOOTH_HZ = 100.0
+local RUN_IN_MIN = 0.01
+local RUN_IN_MAX = 0.01
+
+local function ease01(x) return x*x*(3-2*x) end
+
+local function smoothLerp(cur, target, dt, speed)
+    dt = tonumber(dt) or 0
+    if dt < 0 then dt = 0 end
+    speed = tonumber(speed) or 0
+    local t = dt * speed
+    if t > 1 then t = 1 end
+    return cur + (target - cur) * ease01(t)
+end
+
+local function clamp(v,a,b)
+	if v<a then return a elseif v>b then return b else return v end
+end
 
 local function getGroundMaterial()
     if base_body == 0 then return "masonry" end
@@ -221,7 +229,7 @@
 end
 
 function updateFear(dt)
-    if fearTimer > 0 then
+    if fearTimer ~= 0 then
         fearTimer = math.max(fearTimer - dt, 0)
         PLAYER_LOOK_DIST = math.min(PLAYER_LOOK_DIST + 1.5, 7.0)
         BACKUP_DIST = math.min(BACKUP_DIST + 1.5, 6.0)
@@ -236,14 +244,6 @@
     return PLAYER_LOOK_DIST, BACKUP_DIST
 end
 
-local animCtrl = {
-	crouch = 0.0,
-	jumpFalling = 0.0,
-	turnWeight = 0.0,
-	lastGrounded = true,
-	animSpeedMult = 1.0
-}
-
 local function normalizeAngleDeg(a)
 	while a>180 do a=a-360 end
 	while a<-180 do a=a+360 end
@@ -267,13 +267,10 @@
 	return VecNormalize(v)
 end
 
-local faceTags = {"Neutral", "Blink", "Angry", "Happy", "Surprised", "Fall", "Look", "Lookr", "Lookl"}
-
-local nextFace = nil
-local lastAppliedFace = nil
 function SetFace(faceTag)
     nextFace = faceTag
 end
+
 local function applyBufferedFace()
     if not nextFace then return end
     if nextFace == lastAppliedFace then nextFace = nil; return end
@@ -335,11 +332,6 @@
 	return grounded
 end
 
-local steerDir = Vec(0,0,1)
-moveDirSmoothed = moveDirSmoothed or Vec(0,0,0)
-speedSmoothed = speedSmoothed or 0
-local steerFade = 0.0
-
 function steerToward(dirWorld, speedMin, speedMax, targetPos, strength)
 	if base_body == 0 then return end
 	local bt = GetBodyTransform(base_body)
@@ -436,7 +428,7 @@
 		DebugLine(pos, goalPos, 1, 1, 0)
 	end
 
-	if path and #path > 0 then
+	if path and #path ~= 0 then
 		local prev = pos
 		for i, wp in ipairs(path) do
 			if currentPathIndex and i == currentPathIndex then
@@ -519,7 +511,7 @@
 		end
 	end
 
-	if bestHeightDiff > 0 then
+	if bestHeightDiff ~= 0 then
 		local pushVel = bestHeightDiff * 10
 		ConstrainVelocity(base_body, 0, t.pos, Vec(0, 5, 0), pushVel, 2.0)
 	end
@@ -529,12 +521,6 @@
 		ConstrainVelocity(base_body, 0, t.pos, Vec(0,5,0), 1.5, 0.4)
 	end
 end
-
-local sidestepStrength = 0.0
-DEBUG_OBSTACLE = false
-
-currentMoveDir = currentMoveDir or Vec(0,0,0)
-local lastObstacleCheck = 0
 
 function obstacleAvoidance(dt)
 	if not base_body or base_body == 0 or OBSTACLE_AVOID_BLOCKED then return end
@@ -612,10 +598,6 @@
 	return true
 end
 
-local path = {}
-local lastRepathTime = 0
-local repathInterval = 0.3
-
 function computePath(startPos, goalPos)
 	local offset = VecNormalize(VecCross(Vec(0,1,0), VecSub(goalPos, startPos)))
 	local mid = VecAdd(VecLerp(startPos, goalPos, 0.5), VecScale(offset, 1.5))
@@ -631,7 +613,7 @@
 		lastRepathTime = GetTime()
 	end
 
-	if #path > 0 then
+	if #path ~= 0 then
 		local wp = path[1]
 		local dist = VecLength(VecSub(wp, pos))
 		if dist < 2.0 then
@@ -650,10 +632,6 @@
 	obstacleAvoidance(dt)
 end
 
-local path = {}
-local lastRepathTime = 0
-local repathInterval = 0.3
-
 function computePath(startPos, goalPos)
 	local offset = VecNormalize(VecCross(Vec(0,1,0), VecSub(goalPos, startPos)))
 	local mid = VecAdd(VecLerp(startPos, goalPos, 0.5), VecScale(offset, 1.5))
@@ -669,7 +647,7 @@
 		lastRepathTime = GetTime()
 	end
 
-	if #path > 0 then
+	if #path ~= 0 then
 		local wp = path[1]
 		local dist = VecLength(VecSub(wp, pos))
 		if dist < 2.0 then
@@ -688,19 +666,10 @@
 	obstacleAvoidance(dt)
 end
 
-MAX_THINK_TIME = 1.0
-REPATH_MIN_DELTA = 0.5
-PATH_LOOKAHEAD = 1.0
-
-pathTarget = nil
-pathProgress = 0
-pathFailed = false
-pathThinkTime = 0
-lastPath = {}
-lastRepathTime = 0
-
 local function clamp2(v,a,b) if v<a then return a elseif v>b then return b end return v end
+
 local function vecFlatDist(a,b) local d=VecSub(a,b); d[2]=0; return VecLength(d) end
+
 local function SafeIsBody(b) return b ~= nil and b ~= 0 end
 
 function PathPlannerRejectBody(planner)
@@ -735,7 +704,7 @@
 
 local function drawPath()
     for i=1,#lastPath-1 do DrawLine(lastPath[i], lastPath[i+1]) end
-    if pathFailed and #lastPath>0 then DebugCross(lastPath[#lastPath], 1, 0, 0) end
+    if pathFailed and #lastPath ~= 0 then DebugCross(lastPath[#lastPath], 1, 0, 0) end
 end
 
 local function ensurePath(targetPos, force)
@@ -779,7 +748,7 @@
     local st = GetPathState()
     if st == "done" or st == "fail" then
         local length = GetPathLength()
-        if length > 0 then
+        if length ~= 0 then
             local nextDist = clamp(pathProgress + 0.1, 0, length)
             local nextPoint = GetPathPoint(nextDist)
             return nextPoint, false
@@ -921,9 +890,6 @@
 	return origin
 end
 
-panicPathTarget = panicPathTarget or nil
-panicPathTimeout = panicPathTimeout or 0
-
 function updateAI(dt, grounded)
 	if base_body == 0 or npc_animator == 0 then return end
 
@@ -933,12 +899,12 @@
 
 	local bt = GetBodyTransform(base_body)
 	local pos = bt.pos
-	local ppos = GetPlayerTransform().pos
+	local ppos = GetPlayerTransform(playerId).pos
 	local toPlayer = VecSub(ppos, pos)
 	local distToPlayer = VecLength(toPlayer)
 	
 	local playerTool = GetString("game.player.tool") or ""
-	local playerVehicle = GetPlayerVehicle() or 0
+	local playerVehicle = GetPlayerVehicle(playerId) or 0
 	local dangerous = playerVehicle ~= 0 or playerTool == "gun" or playerTool == "shotgun"
 	or playerTool == "rifle" or playerTool == "rocket" or playerTool == "RBLX_ITEM_CRUCIFIX"
 	
@@ -1080,7 +1046,7 @@
 		local st = GetPathState()
 		if st == "done" then
 			local len = GetPathLength()
-			if len > 0 then
+			if len ~= 0 then
 				local nd = clamp(pathProgress + 0.2, 0, len)
 				local np = GetPathPoint(nd)
 				local dir = VecSub(np, pos); dir[2] = 0
@@ -1177,7 +1143,7 @@
 			local st = GetPathState()
 			if st == "done" then
 				local length = GetPathLength()
-				if length > 0 then
+				if length ~= 0 then
 					local nextDist = clamp(pathProgress + 0.1, 0, length)
 					local nextPoint = GetPathPoint(nextDist)
 
@@ -1319,7 +1285,7 @@
 				toNext[2] = 0
 
 				local flat = VecLength(toNext)
-				if flat > 0 then
+				if flat ~= 0 then
 					local dir = VecNormalize(toNext)
 					smoothDir = smoothDir and VecNormalize(VecLerp(smoothDir, dir, 0.15)) or dir
 
@@ -1481,11 +1447,6 @@
     SetAnimationClipFade(animator, name, fade or FADE_FAST, fade or FADE_FAST)
 end
 
-local USE_DIAGONALS = true
-local VEL_SMOOTH_HZ = 100.0
-local RUN_IN_MIN = 0.01
-local RUN_IN_MAX = 0.01
-
 local function smooth01(x)
     return x <= 0 and 0 or (x >= 1 and 1 or x*x*(3 - 2*x))
 end
@@ -1503,8 +1464,6 @@
     PlayAnimationLoop(npc_animator, animName, animWeight or 1.0)
     SetAnimationClipFade(npc_animator, animName, animFade or FADE_FAST, animFade or FADE_FAST)
 end
-
-animCtrl.lastLocalVel = animCtrl.lastLocalVel or Vec(0,0,0)
 
 local function NPC_AnimationUpdate(dt, grounded)
 	if npc_animator == 0 or base_body == 0 then return end
@@ -1524,7 +1483,6 @@
 	frameVel[2] = 0
 	local frameSpeed = VecLength(frameVel) / dt
 	animCtrl.lastPos = currPos
-
 
 	local rawLocal = TransformToLocalVec(bt, horiz)
 	animCtrl.lastLocalVel = animCtrl.lastLocalVel or Vec(0,0,0)
@@ -1683,127 +1641,6 @@
 			if animCtrl.turnWeight > 0.5 and grounded then SetFace("Lookr") end
 		end
 	end
-end
-
-function init()
-	npc_animator = FindAnimator(NPC_TAG)
-	base_body = FindBody(BODY_TAG)
-	idleTimer = math.random(IDLE_MIN*100, IDLE_MAX*100) / 100
-	pathPlannerId = CreatePathPlanner()
-
-	if npc_animator ~= 0 then
-		local preloadAnims = {
-			"idle_1","idle_2","idle_3","idle_4","idle_5", DEFAULT_IDLE, "crouch_idle",
-			"run_fwd","run_bwd","run_l","run_r",
-			"crouch_fwd","crouch_bwd","crouch_l","crouch_r",
-			"turn_l","turn_r",
-			"jump_start","jump_loop","jump_land",
-			"swim","emote_1"
-		}
-		for _,a in ipairs(preloadAnims) do PlayAnimationLoop(npc_animator, a, 0) end
-	end
-	
-	if body == 0 then return end
-	local shapes = GetBodyShapes(FindBody("npc_base"))
-	for i=1,#shapes do
-		local s = shapes[i]
-		local sx, sy, sz = GetShapeSize(s)
-		if sx and sy and sz then
-			ResizeShape(s, 0, 0, 0, sx, 16, sz)
-		end
-	end
-	
-	SetFace("Neutral")
-	tim = 0
-end
-
-bleedingShapes = {}
-
-DisableAI = false
-function tick(dt)
-	if npc_animator == 0 then npc_animator = FindAnimator(NPC_TAG) end
-	if base_body == 0 then base_body = FindBody(BODY_TAG) end
-
-	checkRagdoll()
-	if ragdollActive then return end
-
-	local grounded = isGroundedCorners(base_body)
-	
-	if not DisableAI then
-		updateAI(dt, grounded)
-	end
-	
-	updateFear(dt)
-	
-	if not grounded then
-		SetFace("Fall")
-	end
-	
-	if aiState == "idle" or aiState == "look" and not aiState == "falling" or not aiState == "avoid" and not aiState == "follow" and grounded then
-		if math.random(1, 90) == 90 then
-			SetFace("Neutral")
-		elseif math.random(1, 250) == 250 then
-			SetFace("Blink")
-		end
-		
-		if math.random(1, 300) == 300 then
-			SetFace("Lookl")
-		elseif math.random(1, 100) == 100 then
-			SetFace("Lookr")
-		end
-	end
-	
-	if aiState == "waving" then
-		SetFace("Happy")
-	end
-
-	NPC_AnimationUpdate(dt, grounded)
-	
-	if HasTag(base_body, "Crucifixed") then
-		playStruggle(dt, npc_animator)
-	end
-
-	if waveCooldown > 0 then
-		waveCooldown = math.max(waveCooldown - dt, 0)
-	end
-	if isWaving then
-		wavingTimer = wavingTimer - dt
-		if wavingTimer <= 0 then
-			stopWave()
-		else
-			SetFace("Happy")
-		end
-	end
-	
-	if HasTag(FindBody("WITHER_STORM", true), "WITHER_STORM") then
-		SetFace("Surprised")
-		if DisableAI then
-			if math.random(1, 1500) == 1500 then
-				DebugPrint("HELP!")
-			end
-			if math.random(1, 1500) == 1500 then
-				DebugPrint("I CAN'T MOVE!!")
-			end
-			if math.random(1, 1500) == 1500 then
-				DebugPrint("PLEASE TURN ON MY AI!")
-			end
-			if math.random(1, 1500) == 1500 then
-				DebugPrint("WITHER IS ATTACKING, TURN ON MY AI!!!")
-			end
-			if math.random(1, 1500) == 1500 then
-				DebugPrint("I'M ON DANGER!")
-			end
-		end
-	end
-	
-	local vel = GetBodyVelocity(base_body)
-    vel[2] = 0
-    local speed = VecLength(vel)
-    local animMult = clamp(speed / 3.5, 0.5, 2.0)
-
-    updateFootsteps(dt, grounded, animMult)
-	
-	wasGrounded = grounded
 end
 
 function GetAimPos(shape)
@@ -1824,180 +1661,297 @@
 	return forwardPos, hit, distance
 end
 
-function update()
-	local bt = GetBodyTransform(base_body)
-	applyBufferedFace()
-
-	local _, curYaw, _ = GetQuatEuler(bt.rot)
-	local targetYaw = desiredYaw or curYaw
-	local targetQuat = QuatEuler(0, targetYaw, 0)
-
-	ConstrainOrientation(base_body, 0, bt.rot, targetQuat, 4.0)
-	SetAnimatorTransform(npc_animator, GetBodyTransform(base_body))
-	
-	local bodies = FindBodies("N-P-C--B-L-O-O-D--M-O-D-E") -- 
-	for b=1, #bodies do
-		if IsBodyBroken(bodies[b]) then
-			local shapes = GetBodyShapes(bodies[b])
-			for i=1, #shapes do
-				if not bleedingShapes[shapes[i]] then
-					bleedingShapes[shapes[i]] = {timer = 0, count = 0}
-				end
-			end
-		end
-		local shapes = GetBodyShapes(bodies[b])
-		for i=1, #shapes do
-			RemoveTag(shapes[i], "unbreakable")
-			SetTag(shapes[i], "attachment")
-		end
-	end
-
-	for shape, data in pairs(bleedingShapes) do
-		data.timer = data.timer + 1
-		if data.count < 1 and data.timer % 1 == 0 then
-
-			local tr = GetShapeWorldTransform(shape)
-			local p = VecCopy(tr.pos)
-
-			p[1] = p[1] + math.random(-4,4)*0.1
-			p[2] = p[2] + math.random(-2,6)*0.1
-			p[3] = p[3] + math.random(-4,4)*0.1
-
-			local dir = VecNormalize(Vec(math.random(-1,1), -10, math.random(-1,1)))
-			local hit,dist,nrm = QueryRaycast(p, dir, 8)
-
-			local splatPos = p
-			local splatNrm = Vec(0,-1,0)
-			local puddleDelay = 1
-
-			if hit then
-				splatPos = VecAdd(p, VecScale(dir, dist))
-				splatNrm = nrm
-				puddleDelay = math.min(2, dist*0.4)
-			end
-
-			ParticleReset()
-			ParticleColor(0.45,0,0)
-			ParticleGravity(-9)
-			ParticleRadius(0.15,0.01)
-			ParticleAlpha(1,0)
-			ParticleTile(5)
-			ParticleCollide(0)
-			ParticleStretch(5)
-
-			for i=1,6 do
-				SpawnParticle(tr.pos,Vec(math.random(-4,4)*0.45,math.random(3,10)*0.25,math.random(-4,4)*0.45),1.0)
-			end
-
-			for i=1,4 do
-				ParticleReset()
-				ParticleColor(0.45,0,0)
-				ParticleGravity(-9)
-				ParticleRadius(0.3,0.0)
-				ParticleAlpha(0.8,0)
-				ParticleCollide(0)
-				ParticleTile(14)
-				SpawnParticle(tr.pos,Vec(math.random(-4,4)*0.2, math.random(1,5)*0.15, math.random(-4,4)*0.2),4)
-			end
-
-			-- timed splats
-			local tNow = GetTime()
-			local spawnT = tNow + puddleDelay
-
-			bloodTimed = bloodTimed or {}
-			bloodTimed[#bloodTimed+1] = {
-				pos = VecCopy(splatPos),
-				nrm = VecCopy(splatNrm),
-				time = spawnT
-			}
-
-			data.count = data.count + 1
-
-			PlaySound(LoadSound("MOD/Gore_h0.ogg",1),  p, 0.4, true,2.35)
-			PlaySound(LoadSound("MOD/Gore_h0.ogg",3), p, 0.5,false,1.9)
-			PaintRGBA(tr.pos, 0.45, 0.40,0,0, 1, 0.5)
-		end
-	end
-
-	-- delayed puddle painting
-	if bloodTimed then
-		local t = GetTime()
-		for i=#bloodTimed,1,-1 do
-			local b = bloodTimed[i]
-			if t >= b.time then
-
-				local sp = b.pos
-				for k=1,4 do
-					local ox = math.random(-3,3)*0.06
-					local oz = math.random(-3,3)*0.06
-					local p2 = Vec(sp[1]+ox, sp[2], sp[3]+oz)
-					PaintRGBA(p2, 0.15, 0.40,0,0, 1, 0.92)
-					PaintRGBA(p2, 0.2, 0.40,0,0, 1, 0.65)
-				end
-
-				if b.nrm[2] < 0.55 then
-					local d1 = VecAdd(sp, VecScale(b.nrm,-0.14))
-					local d2 = Vec(d1[1], d1[2]-0.12, d1[3])
-					local d3 = Vec(d2[1], d2[2]-0.10, d2[3])
-					PaintRGBA(d1, 0.15, 0.40,0,0, 1, 0.75)
-					PaintRGBA(d2, 0.2, 0.40,0,0, 1, 0.55)
-					PaintRGBA(d3, 0.225, 0.40,0,0, 1, 0.40)
-				end
-
-				table.remove(bloodTimed,i)
-			end
-		end
-	end
-
-	SetAnimatorTransform(npc_animator, bt)
-	
-	SetTag(npc_animator, "NPC_SECRET_DOOR_COMPATIBILITY")
-	SetTag(npc_animator, "NPC_SECRET_TOOL_COMPATIBILITY")
-	SetTag(npc_animator, "npc_animator")
-	SetTag(base_body, "NPC_SECRET_DOOR_COMPATIBILITY")
-	SetTag(base_body, "npc_base")
-	SetTag(base_body, "NPC_SECRET_TOOL_COMPATIBILITY")
-	
-	if ragdollActive then
-		tim = tim + 0.01
-		if tim > 86400 then
-			local bodies = FindBodies("")
-			for b=1, #bodies do
-				local shapes = GetBodyShapes(bodies[b])
-				local spawnPos
-
-				for i=1, #shapes do
-					if not particleDeath then
-						spawnPos = GetShapeWorldTransform(shapes[i]).pos
-
-						ParticleReset()
-						ParticleType("smoke")
-						ParticleColor(0.9, 0.9, 0.9)
-						ParticleRadius(0.45, 0.0)
-						ParticleAlpha(0.9, 0.0)
-						ParticleGravity(2.5)
-						ParticleStretch(5)
-						ParticleCollide(0)
-
-						for n=1, 10 do
-							SpawnParticle(spawnPos, Vec(math.random(-10,10)/3, 2, math.random(-10,10)/3), 1)
-						end
-						particleDeath = true
-					end
-
-					timer = timer + 1
-					if timer > 30 then
-						Delete(shapes[i])
-					end
-				end
-
-				shapes = GetBodyShapes(bodies[b])
-				for i=1, #shapes do
-					RemoveTag(shapes[i], "unbreakable")
-				end
-			end
-		end
-	end
-	
-	if base_body == 0 then MakeRagdoll(npc_animator) end
-end+function server.init()
+    npc_animator = FindAnimator(NPC_TAG)
+    base_body = FindBody(BODY_TAG)
+    idleTimer = math.random(IDLE_MIN*100, IDLE_MAX*100) / 100
+    pathPlannerId = CreatePathPlanner()
+    if npc_animator ~= 0 then
+    	local preloadAnims = {
+    		"idle_1","idle_2","idle_3","idle_4","idle_5", DEFAULT_IDLE, "crouch_idle",
+    		"run_fwd","run_bwd","run_l","run_r",
+    		"crouch_fwd","crouch_bwd","crouch_l","crouch_r",
+    		"turn_l","turn_r",
+    		"jump_start","jump_loop","jump_land",
+    		"swim","emote_1"
+    	}
+    	for _,a in ipairs(preloadAnims) do PlayAnimationLoop(npc_animator, a, 0) end
+    end
+
+    if body == 0 then return end
+    local shapes = GetBodyShapes(FindBody("npc_base"))
+    for i=1,#shapes do
+    	local s = shapes[i]
+    	local sx, sy, sz = GetShapeSize(s)
+    	if sx and sy and sz then
+    		ResizeShape(s, 0, 0, 0, sx, 16, sz)
+    	end
+    end
+
+    SetFace("Neutral")
+    tim = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if npc_animator == 0 then npc_animator = FindAnimator(NPC_TAG) end
+        if base_body == 0 then base_body = FindBody(BODY_TAG) end
+
+        checkRagdoll()
+        if ragdollActive then return end
+
+        local grounded = isGroundedCorners(base_body)
+
+        if not DisableAI then
+        	updateAI(dt, grounded)
+        end
+
+        updateFear(dt)
+
+        if not grounded then
+        	SetFace("Fall")
+        end
+
+        if aiState == "idle" or aiState == "look" and not aiState == "falling" or not aiState == "avoid" and not aiState == "follow" and grounded then
+        	if math.random(1, 90) == 90 then
+        		SetFace("Neutral")
+        	elseif math.random(1, 250) == 250 then
+        		SetFace("Blink")
+        	end
+
+        	if math.random(1, 300) == 300 then
+        		SetFace("Lookl")
+        	elseif math.random(1, 100) == 100 then
+        		SetFace("Lookr")
+        	end
+        end
+
+        if aiState == "waving" then
+        	SetFace("Happy")
+        end
+
+        NPC_AnimationUpdate(dt, grounded)
+
+        if HasTag(base_body, "Crucifixed") then
+        	playStruggle(dt, npc_animator)
+        end
+
+        if waveCooldown ~= 0 then
+        	waveCooldown = math.max(waveCooldown - dt, 0)
+        end
+        if isWaving then
+        	wavingTimer = wavingTimer - dt
+        	if wavingTimer <= 0 then
+        		stopWave()
+        	else
+        		SetFace("Happy")
+        	end
+        end
+
+        if HasTag(FindBody("WITHER_STORM", true), "WITHER_STORM") then
+        	SetFace("Surprised")
+        	if DisableAI then
+        		if math.random(1, 1500) == 1500 then
+        			DebugPrint("HELP!")
+        		end
+        		if math.random(1, 1500) == 1500 then
+        			DebugPrint("I CAN'T MOVE!!")
+        		end
+        		if math.random(1, 1500) == 1500 then
+        			DebugPrint("PLEASE TURN ON MY AI!")
+        		end
+        		if math.random(1, 1500) == 1500 then
+        			DebugPrint("WITHER IS ATTACKING, TURN ON MY AI!!!")
+        		end
+        		if math.random(1, 1500) == 1500 then
+        			DebugPrint("I'M ON DANGER!")
+        		end
+        	end
+        end
+
+        local vel = GetBodyVelocity(base_body)
+           vel[2] = 0
+           local speed = VecLength(vel)
+           local animMult = clamp(speed / 3.5, 0.5, 2.0)
+
+           updateFootsteps(dt, grounded, animMult)
+
+        wasGrounded = grounded
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local bt = GetBodyTransform(base_body)
+        applyBufferedFace()
+        local _, curYaw, _ = GetQuatEuler(bt.rot)
+        local targetYaw = desiredYaw or curYaw
+        local targetQuat = QuatEuler(0, targetYaw, 0)
+        ConstrainOrientation(base_body, 0, bt.rot, targetQuat, 4.0)
+        SetAnimatorTransform(npc_animator, GetBodyTransform(base_body))
+        local bodies = FindBodies("N-P-C--B-L-O-O-D--M-O-D-E") -- 
+        for b=1, #bodies do
+        	if IsBodyBroken(bodies[b]) then
+        		local shapes = GetBodyShapes(bodies[b])
+        		for i=1, #shapes do
+        			if not bleedingShapes[shapes[i]] then
+        				bleedingShapes[shapes[i]] = {timer = 0, count = 0}
+        			end
+        		end
+        	end
+        	local shapes = GetBodyShapes(bodies[b])
+        	for i=1, #shapes do
+        		RemoveTag(shapes[i], "unbreakable")
+        		SetTag(shapes[i], "attachment")
+        	end
+        end
+        -- delayed puddle painting
+        if bloodTimed then
+        	local t = GetTime()
+        	for i=#bloodTimed,1,-1 do
+        		local b = bloodTimed[i]
+        		if t >= b.time then
+
+        			local sp = b.pos
+        			for k=1,4 do
+        				local ox = math.random(-3,3)*0.06
+        				local oz = math.random(-3,3)*0.06
+        				local p2 = Vec(sp[1]+ox, sp[2], sp[3]+oz)
+        				PaintRGBA(p2, 0.15, 0.40,0,0, 1, 0.92)
+        				PaintRGBA(p2, 0.2, 0.40,0,0, 1, 0.65)
+        			end
+
+        			if b.nrm[2] < 0.55 then
+        				local d1 = VecAdd(sp, VecScale(b.nrm,-0.14))
+        				local d2 = Vec(d1[1], d1[2]-0.12, d1[3])
+        				local d3 = Vec(d2[1], d2[2]-0.10, d2[3])
+        				PaintRGBA(d1, 0.15, 0.40,0,0, 1, 0.75)
+        				PaintRGBA(d2, 0.2, 0.40,0,0, 1, 0.55)
+        				PaintRGBA(d3, 0.225, 0.40,0,0, 1, 0.40)
+        			end
+
+        			table.remove(bloodTimed,i)
+        		end
+        	end
+        end
+        SetAnimatorTransform(npc_animator, bt)
+        SetTag(npc_animator, "NPC_SECRET_DOOR_COMPATIBILITY")
+        SetTag(npc_animator, "NPC_SECRET_TOOL_COMPATIBILITY")
+        SetTag(npc_animator, "npc_animator")
+        SetTag(base_body, "NPC_SECRET_DOOR_COMPATIBILITY")
+        SetTag(base_body, "npc_base")
+        SetTag(base_body, "NPC_SECRET_TOOL_COMPATIBILITY")
+        if base_body == 0 then MakeRagdoll(npc_animator) end
+    end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    for shape, data in pairs(bleedingShapes) do
+    	data.timer = data.timer + 1
+    	if data.count < 1 and data.timer % 1 == 0 then
+
+    		local tr = GetShapeWorldTransform(shape)
+    		local p = VecCopy(tr.pos)
+
+    		p[1] = p[1] + math.random(-4,4)*0.1
+    		p[2] = p[2] + math.random(-2,6)*0.1
+    		p[3] = p[3] + math.random(-4,4)*0.1
+
+    		local dir = VecNormalize(Vec(math.random(-1,1), -10, math.random(-1,1)))
+    		local hit,dist,nrm = QueryRaycast(p, dir, 8)
+
+    		local splatPos = p
+    		local splatNrm = Vec(0,-1,0)
+    		local puddleDelay = 1
+
+    		if hit then
+    			splatPos = VecAdd(p, VecScale(dir, dist))
+    			splatNrm = nrm
+    			puddleDelay = math.min(2, dist*0.4)
+    		end
+
+    		ParticleReset()
+    		ParticleColor(0.45,0,0)
+    		ParticleGravity(-9)
+    		ParticleRadius(0.15,0.01)
+    		ParticleAlpha(1,0)
+    		ParticleTile(5)
+    		ParticleCollide(0)
+    		ParticleStretch(5)
+
+    		for i=1,6 do
+    			SpawnParticle(tr.pos,Vec(math.random(-4,4)*0.45,math.random(3,10)*0.25,math.random(-4,4)*0.45),1.0)
+    		end
+
+    		for i=1,4 do
+    			ParticleReset()
+    			ParticleColor(0.45,0,0)
+    			ParticleGravity(-9)
+    			ParticleRadius(0.3,0.0)
+    			ParticleAlpha(0.8,0)
+    			ParticleCollide(0)
+    			ParticleTile(14)
+    			SpawnParticle(tr.pos,Vec(math.random(-4,4)*0.2, math.random(1,5)*0.15, math.random(-4,4)*0.2),4)
+    		end
+
+    		-- timed splats
+    		local tNow = GetTime()
+    		local spawnT = tNow + puddleDelay
+
+    		bloodTimed = bloodTimed or {}
+    		bloodTimed[#bloodTimed+1] = {
+    			pos = VecCopy(splatPos),
+    			nrm = VecCopy(splatNrm),
+    			time = spawnT
+    		}
+
+    		data.count = data.count + 1
+
+    		PlaySound(LoadSound("MOD/Gore_h0.ogg",1),  p, 0.4, true,2.35)
+    		PlaySound(LoadSound("MOD/Gore_h0.ogg",3), p, 0.5,false,1.9)
+    		PaintRGBA(tr.pos, 0.45, 0.40,0,0, 1, 0.5)
+    	end
+    end
+    if ragdollActive then
+    	tim = tim + 0.01
+    	if tim > 86400 then
+    		local bodies = FindBodies("")
+    		for b=1, #bodies do
+    			local shapes = GetBodyShapes(bodies[b])
+    			local spawnPos
+
+    			for i=1, #shapes do
+    				if not particleDeath then
+    					spawnPos = GetShapeWorldTransform(shapes[i]).pos
+
+    					ParticleReset()
+    					ParticleType("smoke")
+    					ParticleColor(0.9, 0.9, 0.9)
+    					ParticleRadius(0.45, 0.0)
+    					ParticleAlpha(0.9, 0.0)
+    					ParticleGravity(2.5)
+    					ParticleStretch(5)
+    					ParticleCollide(0)
+
+    					for n=1, 10 do
+    						SpawnParticle(spawnPos, Vec(math.random(-10,10)/3, 2, math.random(-10,10)/3), 1)
+    					end
+    					particleDeath = true
+    				end
+
+    				timer = timer + 1
+    				if timer > 30 then
+    					Delete(shapes[i])
+    				end
+    			end
+
+    			shapes = GetBodyShapes(bodies[b])
+    			for i=1, #shapes do
+    				RemoveTag(shapes[i], "unbreakable")
+    			end
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: propC.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/propC.lua
+++ patched/propC.lua
@@ -1,6 +1,10 @@
-function tick()
-	Prop = GetBodyShapes(FindBody("Prop"))
-	for i=1,#Prop do
-	    SetShapeCollisionFilter(Prop[i], 1, 255-0)
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        Prop = GetBodyShapes(FindBody("Prop"))
+        for i=1,#Prop do
+            SetShapeCollisionFilter(Prop[i], 1, 255-0)
+           end
     end
-end+end
+

```

---

# Migration Report: RushVisuals.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/RushVisuals.lua
+++ patched/RushVisuals.lua
@@ -1,18 +1,16 @@
+#version 2
 local bodyTag = "RBLX_Rush_Move"
 local lightTag = ""
 local lightBreakRange = 4.5
-
 local visualFade = 0.0
 local visualFadeSpeed = 0.015
 local Crucifixed = false
 local tim = 0
-
 local farMaxVol = 4.0
 local nearMaxVol = 7.5
 local farFade = 0.0
 local nearFade = 0.0
 local fadeSpeed = 0.015
-
 local rushBody = nil
 local rushSprite = nil
 local rushAuraSprite = nil
@@ -20,28 +18,12 @@
 local nearLoop = nil
 
 local function rnd(min, max) return math.random() * (max - min) + min end
+
 local function VecDist(a, b) return VecLength(VecSub(a, b)) end
+
 local function lerp(a, b, t) return a + (b - a) * t end
+
 local function VecToString(v) return string.format("%.2f_%.2f_%.2f", v[1], v[2], v[3]) end
-
-function init()
-	rushBody = FindBody(bodyTag)
-	if rushBody == 0 then
-		DebugPrint("Rush body not found!")
-		return
-	end
-
-	rushSprite = LoadSprite("MOD/rush.png")
-	rushAuraSprite = LoadSprite("MOD/Rush_Aura.png")
-
-	farLoop = LoadLoop("MOD/RushFar.ogg", 12)
-	nearLoop = LoadLoop("MOD/RushNear.ogg", 3)
-	SetSoundLoopProgress(farLoop, 0)
-	SetSoundLoopProgress(nearLoop, 0)
-
-	tim = 0
-	visualFade = 0.0
-end
 
 local function drawRushAuraSprites(t)
 	local comLocal = GetBodyCenterOfMass(rushBody)
@@ -123,67 +105,82 @@
 	end
 end
 
-function tick(dt)
-	if rushBody == 0 or not IsHandleValid(rushBody) or not HasTag(rushBody, bodyTag) then
-		return
-	end
+function server.init()
+    rushBody = FindBody(bodyTag)
+    if rushBody == 0 then
+    	DebugPrint("Rush body not found!")
+    	return
+    end
+    rushSprite = LoadSprite("MOD/rush.png")
+    rushAuraSprite = LoadSprite("MOD/Rush_Aura.png")
+    farLoop = LoadLoop("MOD/RushFar.ogg", 12)
+    nearLoop = LoadLoop("MOD/RushNear.ogg", 3)
+    SetSoundLoopProgress(farLoop, 0)
+    SetSoundLoopProgress(nearLoop, 0)
+    tim = 0
+    visualFade = 0.0
+end
 
-	tim = tim + 1
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if rushBody == 0 or not IsHandleValid(rushBody) or not HasTag(rushBody, bodyTag) then
+        	return
+        end
+        tim = tim + 1
+        if visualFade < 0.05 and not HasTag(rushBody, bodyTag) then
+        	Delete(rushBody)
+        	return
+        end
+        local t = GetBodyTransform(rushBody)
+        if not HasTag(rushBody, "Crucifixed") then
+        	handleSounds(t.pos)
+        end
+        breakNearbyLights()
+        local lights = FindLights(lightTag, true)
+        if lights then
+        	for i = 1, #lights do
+        		if tim < 100 then
+        			SetTag(lights[i], "fxflicker", "2")
+        		else
+        			RemoveTag(lights[i], "fxflicker")
+        		end
+        	end
+        end
+        if rushBody == 0 or not IsHandleValid(rushBody) then return end
+        if not rushSprite or not rushAuraSprite then return end
+        if visualFade <= 0.01 then return end
+        if not HasTag(rushBody, bodyTag) then return end
 
-	if HasTag(rushBody, "Crucifixed") then
-		if not Crucifixed then
-			PlaySound(LoadSound("MOD/RushCrucifixed.ogg", 5), GetBodyTransform(rushBody).pos, 1, false)
-			Crucifixed = true
-		end
-	else
-		visualFade = lerp(visualFade, 1.0, visualFadeSpeed)
-	end
+        local t = GetBodyTransform(rushBody)
 
-	if visualFade < 0.05 and not HasTag(rushBody, bodyTag) then
-		Delete(rushBody)
-		return
-	end
+        drawRushAuraSprites(t)
 
-	local t = GetBodyTransform(rushBody)
-	
-	if not HasTag(rushBody, "Crucifixed") then
-		handleSounds(t.pos)
-	end
+        local comLocal = GetBodyCenterOfMass(rushBody)
+        local center = TransformToParentPoint(t, comLocal)
+        center = VecAdd(center, Vec(0, 0.5, 0))
 
-	breakNearbyLights()
+        local look = QuatLookAt(center, GetCameraTransform().pos)
+        local facing = QuatRotateQuat(look, QuatEuler(0, 180, 0))
 
-	local lights = FindLights(lightTag, true)
-	if lights then
-		for i = 1, #lights do
-			if tim < 100 then
-				SetTag(lights[i], "fxflicker", "2")
-			else
-				RemoveTag(lights[i], "fxflicker")
-			end
-		end
-	end
-	
-	if rushBody == 0 or not IsHandleValid(rushBody) then return end
-	if not rushSprite or not rushAuraSprite then return end
-	if visualFade <= 0.01 then return end
-	if not HasTag(rushBody, bodyTag) then return end
+        local scale = 2.25 * visualFade
+        local alpha = 0.4 * visualFade
+        local jitterStrength = 0.025 * visualFade
+        local offset = Vec(rnd(-jitterStrength, jitterStrength), rnd(-jitterStrength, jitterStrength), rnd(-jitterStrength, jitterStrength))
 
-	local t = GetBodyTransform(rushBody)
-	
-	drawRushAuraSprites(t)
+        DrawSprite(rushSprite, Transform(VecAdd(center, offset), facing), scale, scale, alpha, alpha, alpha + rnd(0.0, 0.5), rnd(0.2, 0.7), true, true, false)
+        DrawSprite(rushSprite, Transform(VecAdd(center, offset), facing), scale, scale, alpha, alpha, alpha + rnd(0.0, 0.5), rnd(0.2, 0.7), true, false, false)
+    end
+end
 
-	local comLocal = GetBodyCenterOfMass(rushBody)
-	local center = TransformToParentPoint(t, comLocal)
-	center = VecAdd(center, Vec(0, 0.5, 0))
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if HasTag(rushBody, "Crucifixed") then
+    	if not Crucifixed then
+    		PlaySound(LoadSound("MOD/RushCrucifixed.ogg", 5), GetBodyTransform(rushBody).pos, 1, false)
+    		Crucifixed = true
+    	end
+    else
+    	visualFade = lerp(visualFade, 1.0, visualFadeSpeed)
+    end
+end
 
-	local look = QuatLookAt(center, GetCameraTransform().pos)
-	local facing = QuatRotateQuat(look, QuatEuler(0, 180, 0))
-
-	local scale = 2.25 * visualFade
-	local alpha = 0.4 * visualFade
-	local jitterStrength = 0.025 * visualFade
-	local offset = Vec(rnd(-jitterStrength, jitterStrength), rnd(-jitterStrength, jitterStrength), rnd(-jitterStrength, jitterStrength))
-
-	DrawSprite(rushSprite, Transform(VecAdd(center, offset), facing), scale, scale, alpha, alpha, alpha + rnd(0.0, 0.5), rnd(0.2, 0.7), true, true, false)
-	DrawSprite(rushSprite, Transform(VecAdd(center, offset), facing), scale, scale, alpha, alpha, alpha + rnd(0.0, 0.5), rnd(0.2, 0.7), true, false, false)
-end
```
