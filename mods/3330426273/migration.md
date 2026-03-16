# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,11 +1,527 @@
--- MAIN FUNCTIONS --
-
-function init()
+#version 2
+function updateSlashes(dt)
+    for i, slash in ipairs(slashes) do
+        if slash.active then
+            slash.point1 = VecAdd(slash.point1, VecScale(slash.dir1, dt * dt * 2000))
+            slash.point2 = VecAdd(slash.point2, VecScale(slash.dir2, dt * dt * 2000))
+            local distance = VecLength(VecSub(slash.point2, slash.origin))
+            local fwd = VecAdd(slash.dir1, slash.dir2)
+            local normalDir = VecCross(slash.dir1, slash.dir2)
+            local length = VecLength(VecSub(slash.point1, slash.point2)) / (0.42 / 2)
+
+            DrawLine(slash.point1, slash.point2, math.random(), math.random(), math.random())
+
+            for i = 1, length do
+                local p = VecAdd(VecLerp(slash.point1, slash.point2, i / length),
+                    VecScale(fwd, math.sin(i * math.pi / length) * 1))
+
+                local hitFwd, distFwd, normalFwd, shapeFwd = QueryRaycast(p, fwd, 0.42 * 5)
+                if hitFwd then
+                    local body = GetShapeBody(shapeFwd)
+                    if IsBodyDynamic(body) then
+                        slashedDynamicBodies[body] = { hit = 1, body = body }
+                        SetBodyDynamic(body, false)
+                        SetBodyVelocity(body, Vec(0, 0, 0))
+                        SetBodyAngularVelocity(body, Vec(0, 0, 0))
+                    elseif slashedDynamicBodies[body] then
+                        slashedDynamicBodies[body].hit = slashedDynamicBodies[body].hit + 1
+                    end
+                end
+
+                MakeHole(p, 0.42, 0.42, 0.42, true)
+
+                QueryRequire("physical dynamic")
+                local hitLeft, distLeft, normalLeft, shapeLeft = QueryRaycast(p, VecSub(normalDir, fwd), 0.42 * 5)
+                QueryRequire("physical dynamic")
+                local hitRight, distRight, normalRight, shapeRight = QueryRaycast(p, VecSub(VecScale(normalDir, -1), fwd),
+                    0.42 * 5)
+
+                if hitLeft then
+                    local body = GetShapeBody(shapeLeft)
+                    local vel = GetBodyVelocity(body)
+                    SetBodyVelocity(body, VecAdd(vel, VecScale(normalDir, 50 * dt)))
+                end
+                if hitRight then
+                    local body = GetShapeBody(shapeRight)
+                    local vel = GetBodyVelocity(body)
+                    SetBodyVelocity(body, VecAdd(vel, VecScale(normalDir, -50 * dt)))
+                end
+            end
+
+            if distance > 100 then
+                table.remove(slashes, i)
+            end
+        end
+    end
+
+    if slashedDynamicBodies then
+        for bodyhash, record in pairs(slashedDynamicBodies) do
+            if record and record.hit then
+                if record.hit > 4 then
+                    slashedDynamicBodies[bodyhash].hit = 1
+                else
+                    SetBodyDynamic(record.body, true)
+                    slashedDynamicBodies[bodyhash] = nil
+                end
+            end
+        end
+    end
+end
+
+function updateFrozenBodies(dt)
+    for bodyhash, record in pairs(frozen) do
+        if not grabbed or (grabbed and not grabbed.bodies[record.body]) then
+            SetBodyVelocity(record.body, Vec(0, 0, 0))
+            SetBodyAngularVelocity(record.body, Vec(0, 0, 0))
+            ApplyBodyImpulse(record.body,
+                TransformToParentPoint(GetBodyTransform(record.body), GetBodyCenterOfMass(record.body)),
+                Vec(0, GetBodyMass(record.body) * dt * 10, 0))
+        end
+    end
+end
+
+function updateWeightlessBodies(dt)
+    for bodyhash, record in pairs(weightless) do
+        if record then
+            ApplyBodyImpulse(record.body,
+                TransformToParentPoint(GetBodyTransform(record.body), GetBodyCenterOfMass(record.body)),
+                Vec(0, GetBodyMass(record.body) * dt * 10, 0))
+        end
+    end
+end
+
+function input(dt)
+    if clearing then
+        for i, voxel in ipairs(voxels) do
+            Delete(voxel)
+        end
+
+        for bodyhash, record in pairs(frozen) do
+            SetBodyVelocity(record.body, record.velocity)
+            SetBodyAngularVelocity(record.body, record.angVelocity)
+        end
+
+        frozen = {}
+        weightless = {}
+        voxels = {}
+        slashes = {}
+    end
+
+    if outlining then
+        for bodyhash, record in pairs(frozen) do
+            if outlining then
+                DrawBodyOutline(record.body, 0, 0, 1, 1)
+            end
+        end
+
+        for bodyhash, record in pairs(weightless) do
+            if outlining then
+                DrawBodyOutline(record.body, 1, 1, 0, 1)
+            end
+        end
+    end
+
+    local ct = GetCameraTransform()
+
+    if slashing and not slashed then
+        PlaySound(cuttingSound)
+
+        local slash = {
+            active = true,
+            dir1 = VecNormalize(VecSub(getSlashPoint(false, slashLength, slashAngle), ct.pos)),
+            dir2 = VecNormalize(VecSub(getSlashPoint(true, slashLength, slashAngle), ct.pos)),
+            point1 = ct.pos,
+            point2 = ct.pos,
+            origin = ct.pos,
+        }
+        table.insert(slashes, slash)
+
+        slashedDynamicBodies[slash] = {}
+
+        slashed = true
+    end
+
+    if InputReleased("lmb") then
+        slashed = false
+    end
+
+    local fwd = TransformToParentVec(ct, Vec(0, 0, -1))
+    local h, d, n, s = QueryRaycast(ct.pos, fwd, 1000)
+    local radius = points / 420
+
+    if h then
+        local hitPos = VecAdd(VecScale(fwd, d), ct.pos)
+
+        if alting and not showing then
+            if not IsBodyDynamic(GetShapeBody(s)) then
+                DrawShapeOutline(s, 1, 0, 0, 1)
+
+                if grab then
+                    PlaySound(detachingSound)
+                    detach(s)
+                end
+            end
+
+            radius = 0.1
+        end
+
+        if showing and not shifting and not alting then
+            SetBool("game.input.locktool", true, true)
+            local prevPoint = nil
+            for i = 1, points do
+                local theta = i * math.pi / points
+                local c = radius * 10
+                local spiralPoint = Vec(radius * math.sin(theta) * math.cos(theta * c + time * math.sqrt(radius) * 5),
+                    radius * math.sin(theta) * math.sin(theta * c + time * math.sqrt(radius) * 5),
+                    radius * math.cos(theta))
+                local point = VecAdd(hitPos, spiralPoint)
+
+                if prevPoint then
+                    DrawLine(prevPoint, point, 1, 0, 0, 0.5)
+                end
+
+                prevPoint = point
+            end
+
+            points = clamp(points + InputValue("mousewheel") * 300, 100, 10000)
+        end
+
+        if not grabbed and not slashing then
+            local dir = Vec(radius, radius, radius)
+            local min = VecSub(hitPos, dir)
+            local max = VecAdd(hitPos, dir)
+            QueryRequire("physical dynamic")
+            local bodies = QueryAabbBodies(min, max)
+            local player = GetPlayerTransform(playerId)
+
+            local inside = {}
+            local relatives = {}
+
+            local count = 0
+            for i, body in ipairs(bodies) do
+                local hit, point, normal = GetBodyClosestPoint(body, hitPos)
+
+                if hit and VecLength(VecSub(point, hitPos)) <= radius then
+                    if outlining then
+                        DrawBodyOutline(body, 0, 1, 0.42, 1)
+                    end
+
+                    local tr = GetBodyTransform(body)
+                    relatives[body] = {
+                        position = TransformToLocalPoint(tr, hitPos),
+                        rotation =
+                            TransformToLocalTransform(player, tr)
+                    }
+                    inside[body] = body
+                    count = count + 1
+                end
+            end
+
+            if count > 0 and (grabbing or pulling or pushing or freezing or rotating or liquifying or imploding or explode or floating or explodeOnNextFrame) then
+                grabbed = { bodies = inside, dist = d, relatives = relatives }
+            end
+        end
+    end
+
+    if showing and (shifting or alting) then
+        SetBool("game.input.locktool", true, true)
+        DebugLine(getSlashPoint(false, slashLength, slashAngle), getSlashPoint(true, slashLength, slashAngle), 1, 0, 0)
+
+        if alting then
+            slashAngle = slashAngle + InputValue("mousewheel") * dt * 25
+            slashAngle = slashAngle % math.pi
+        else
+            slashLength = clamp(slashLength + InputValue("mousewheel") * 10, 10, 200)
+        end
+    end
+
+    if grabbed then
+        SetBool("game.disableinteract", true, true)
+
+        if outlining then
+            for i, body in pairs(grabbed.bodies) do
+                DrawBodyOutline(body, math.random(), math.random(), math.random(), 1)
+            end
+        end
+
+        if pulling then
+            if grabbed.dist - 1 > radius * 1.5 then grabbed.dist = grabbed.dist - 1 end
+        end
+
+        if pushing then
+            grabbed.dist = grabbed.dist + 1
+        end
+
+        if push then
+            PlaySound(pushingSound)
+        end
+
+        if pull then
+            PlaySound(pullingSound)
+        end
+
+        if rotating then
+            SetBool("game.player.disableinput", true, true)
+
+            for i, relative in pairs(grabbed.relatives) do
+                relative.rotation.rot = QuatRotateQuat(
+                    QuatEuler(InputValue("mousedy") * 0.1, InputValue("mousedx") * 0.1, 0), relative.rotation.rot)
+            end
+        end
+
+        -- grabbing
+        if not floating and not exploding and not liquifying and released and not freezing then
+            PlayLoop(grabbingLoop)
+
+            local origin = VecAdd(VecScale(fwd, grabbed.dist), ct.pos)
+            local player = GetPlayerTransform(playerId)
+            for i, body in pairs(grabbed.bodies) do
+                local tr = GetBodyTransform(body)
+                local rotation = TransformToParentTransform(player, grabbed.relatives[i].rotation).rot
+                local x, y, z = GetQuatEuler(QuatRotateQuat(tr.rot,
+                    Quat(-rotation[1], -rotation[2], -rotation[3], rotation[4])))
+
+                SetBodyVelocity(body,
+                    VecScale(VecSub(origin, TransformToParentPoint(tr, grabbed.relatives[i].position)), 8))
+                SetBodyAngularVelocity(body, VecScale(Vec(x, y, z), -0.1))
+            end
+        end
+
+        if imploding and not exploding then
+            PlayLoop(implodingLoop)
+
+            local origin = VecAdd(VecScale(fwd, grabbed.dist), ct.pos)
+            for i, body in pairs(grabbed.bodies) do
+                local dir = VecScale(
+                    VecNormalize(VecSub(TransformToParentPoint(GetBodyTransform(body), GetBodyCenterOfMass(body)), origin)),
+                    -30)
+                SetBodyVelocity(body, dir)
+            end
+
+            -- recalculate grabbed
+            local dir = Vec(radius, radius, radius)
+            local min = VecSub(origin, dir)
+            local max = VecAdd(origin, dir)
+            QueryRequire("physical dynamic")
+            local bodies = QueryAabbBodies(min, max)
+
+            local relatives = {}
+            for i, body in pairs(bodies) do
+                local tr = GetBodyTransform(body)
+                table.insert(relatives,
+                    {
+                        position = TransformToLocalPoint(tr, origin),
+                        rotation = TransformToLocalTransform(
+                            GetPlayerTransform(playerId), tr)
+                    })
+            end
+
+            grabbed.relatives = relatives
+            grabbed.bodies = bodies
+        end
+
+        if explode or explodeOnNextFrame then
+            if explode then
+                PlaySound(explodingSound)
+            end
+
+            local origin = VecAdd(VecScale(fwd, grabbed.dist), ct.pos)
+            for i, body in pairs(grabbed.bodies) do
+                local dir = VecScale(
+                    VecNormalize(VecSub(TransformToParentPoint(GetBodyTransform(body), GetBodyCenterOfMass(body)), origin)),
+                    100)
+                SetBodyVelocity(body, VecAdd(GetBodyVelocity(body), dir))
+            end
+
+            if explode then
+                MakeHole(origin, radius, radius, radius)
+            end
+
+            if explodeOnNextFrame then
+                explodeOnNextFrame = false
+            end
+
+            if explode then
+                explodeOnNextFrame = true
+            end
+
+            grabbed = nil
+            return
+        end
+
+        if floating then
+            PlaySound(floatingSound)
+
+            for i, body in pairs(grabbed.bodies) do
+                if weightless[body] then
+                    weightless[body] = nil
+                else
+                    weightless[body] = { body = body }
+                end
+            end
+
+            grabbed = nil
+            return
+        end
+
+        if liquifying then
+            PlaySound(liquifyingSound)
+
+            for i, body in pairs(grabbed.bodies) do
+                local shapes = GetBodyShapes(body)
+
+                for j, shape in ipairs(shapes) do
+                    liquify(shape)
+                end
+            end
+
+            grabbed = nil
+            released = false
+            return
+        end
+
+        if freezing then
+            PlaySound(freezingSound)
+
+            for i, body in pairs(grabbed.bodies) do
+                if frozen[body] then
+                    local record = frozen[body]
+                    SetBodyVelocity(body, record.velocity)
+                    SetBodyAngularVelocity(body, record.angVelocity)
+
+                    frozen[body] = nil
+                else
+                    frozen[body] = {
+                        velocity = GetBodyVelocity(body),
+                        angVelocity = GetBodyAngularVelocity(body),
+                        body =
+                            body
+                    }
+                end
+            end
+
+            grabbed = nil
+            return
+        end
+
+        -- release
+        if not grabbing and not pushing and not pulling and not freezing and not rotating and not imploding then
+            grabbed = nil
+        end
+    end
+end
+
+function liquify(shape)
+    local object = {}
+
+    local x, y, z = GetShapeSize(shape)
+    local t = GetShapeWorldTransform(shape)
+    local body = GetShapeBody(shape)
+    for i = 0, x do
+        for j = 0, y do
+            for k = 0, z do
+                local m, r, g, b, a = GetShapeMaterialAtIndex(shape, i, j, k)
+                if a ~= 0 then
+                    local pos = TransformToParentPoint(t, Vec(i / 10, j / 10, k / 10))
+                    local vel = GetBodyVelocityAtPos(body, pos)
+                    table.insert(object, { m = m, r = r, g = g, b = b, a = a, pos = pos, rot = t.rot, vel = vel })
+                end
+            end
+        end
+    end
+
+    local spawnOdds = math.ceil(GetShapeVoxelCount(shape) / 10000)
+    if spawnOdds < 1 then spawnOdds = 1 end
+
+    Delete(shape)
+
+    for i, voxel in ipairs(object) do
+        if math.random(1, spawnOdds) == spawnOdds then
+            local vox = Spawn(
+                "<voxbox size='1 1 1' prop='true' material='" ..
+                voxel.m .. "' color='" .. voxel.r .. " " .. voxel.g .. " " .. voxel.b .. " " .. voxel.a .. "'/>",
+                Transform(voxel.pos, t.rot))
+            SetBodyVelocity(vox[1], voxel.vel)
+
+            table.insert(voxels, vox[1])
+        end
+    end
+end
+
+function detach(shape)
+    function hole(p, center)
+        local h, d, n, s = QueryRaycast(p, VecSub(p, center), 0.1)
+        if h and not IsBodyDynamic(GetShapeBody(s)) then
+            MakeHole(p, 0.15, 0.15, 0.15, true)
+        end
+    end
+
+    if GetShapeVoxelCount(shape) < 1000000 then
+        min, max = GetShapeBounds(shape)
+    end
+
+    if min and max then
+        local center = VecLerp(min, max, 0.5)
+        local length1 = max[1] - min[1]
+        local length2 = max[2] - min[2]
+        local length3 = max[3] - min[3]
+        local count1 = length1 / 0.1
+        local count2 = length2 / 0.1
+        local count3 = length3 / 0.1
+        local faces = {
+            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), length2 * (j / count2), 0)), center) end,       c1 = count1, c2 = count2 },
+            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), length2 * (j / count2), length3)), center) end, c1 = count1, c2 = count2 },
+            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), 0, length3 * (j / count3))), center) end,       c1 = count1, c2 = count3 },
+            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), length2, length3 * (j / count3))), center) end, c1 = count1, c2 = count3 },
+            { p = function(i, j) hole(VecAdd(min, Vec(0, length2 * (i / count2), length3 * (j / count3))), center) end,       c1 = count2, c2 = count3 },
+            { p = function(i, j) hole(VecAdd(min, Vec(length1, length2 * (i / count2), length3 * (j / count3))), center) end, c1 = count2, c2 = count3 }
+        }
+
+        for f = 1, #faces do
+            for i = 1, faces[f].c1 do
+                for j = 1, faces[f].c2 do
+                    faces[f].p(i, j)
+                end
+            end
+        end
+    end
+end
+
+function clamp(n, min, max) return math.min(math.max(n, min), max) end
+
+function getSlashPoint(negative, length, angle)
+    local sign = 1
+    if negative then sign = -1 end
+    return VecAdd(GetCameraTransform().pos,
+        TransformToParentVec(GetCameraTransform(),
+            Vec(length * math.cos(angle) * sign, length * math.sin(angle) * sign, -250)))
+end
+
+function optionsSlider(val, min, max)
+    UiColor(0.2, 0.6, 1)
+    UiPush()
+    UiTranslate(0, -8)
+    val = (val - min) / (max - min)
+    local w = 195
+    local done = false
+    UiRect(w, 3)
+    UiAlign("center middle")
+    UiTranslate(-195, 1)
+    val, done = UiSlider("ui/common/dot.png", "x", val * w, 0, w) / w
+    val = round((val * (max - min) + min), 2)
+    UiPop()
+    return val, done
+end
+
+function round(number, decimals)
+    local power = 10 ^ decimals
+    return math.floor(number * power) / power
+end
+
+function server.init()
     RegisterTool("telekinesis-stringie", "Telekinesis")
-    SetBool("game.tool.telekinesis-stringie.enabled", true)
-
+    SetBool("game.tool.telekinesis-stringie.enabled", true, true)
     time = 0
-
     -- weapon variables
     limit = 1000000
     released = true
@@ -18,13 +534,27 @@
     weightless = {}
     frozen = {}
     voxels = {}
-
     -- saved variables
     outlining = true
-
     -- sound variables
     grabbingLoop = LoadLoop("MOD/sound/grabbing.ogg")
     implodingLoop = LoadLoop("MOD/sound/imploding.ogg")
+    -- ui variables
+    hidden = false
+    options = false
+    optionsT = 0
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        updateWeightlessBodies(dt)
+        updateFrozenBodies(dt)
+        updateSlashes(dt)
+        time = GetTime()
+    end
+end
+
+function client.init()
     cuttingSound = LoadSound("MOD/sound/cutting.ogg")
     explodingSound = LoadSound("MOD/sound/exploding.ogg")
     pullingSound = LoadSound("MOD/sound/pulling.ogg")
@@ -33,14 +563,10 @@
     floatingSound = LoadSound("MOD/sound/floating.ogg")
     liquifyingSound = LoadSound("MOD/sound/liquidifying.ogg")
     detachingSound = LoadSound("MOD/sound/detaching.ogg")
-
-    -- ui variables
-    hidden = false
-    options = false
-    optionsT = 0
-end
-
-function tick(dt)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if GetString("game.player.tool") == "telekinesis-stringie" then
         if InputPressed("m") then
             options = not options
@@ -76,8 +602,8 @@
     end
 end
 
-function draw()
-    if GetString("game.player.tool") == "telekinesis-stringie" and GetPlayerVehicle() == 0 then
+function client.draw()
+    if GetString("game.player.tool") == "telekinesis-stringie" and GetPlayerVehicle(playerId) == 0 then
         if (not options and optionsT <= 0) and not hidden then
             UiTranslate(0, UiHeight() - 30)
             UiAlign("top left")
@@ -265,532 +791,3 @@
     end
 end
 
-function update(dt)
-    updateWeightlessBodies(dt)
-    updateFrozenBodies(dt)
-    updateSlashes(dt)
-
-    time = GetTime()
-end
-
--- HELPER FUNCTIONS --
-
-function updateSlashes(dt)
-    for i, slash in ipairs(slashes) do
-        if slash.active then
-            slash.point1 = VecAdd(slash.point1, VecScale(slash.dir1, dt * dt * 2000))
-            slash.point2 = VecAdd(slash.point2, VecScale(slash.dir2, dt * dt * 2000))
-            local distance = VecLength(VecSub(slash.point2, slash.origin))
-            local fwd = VecAdd(slash.dir1, slash.dir2)
-            local normalDir = VecCross(slash.dir1, slash.dir2)
-            local length = VecLength(VecSub(slash.point1, slash.point2)) / (0.42 / 2)
-
-            DrawLine(slash.point1, slash.point2, math.random(), math.random(), math.random())
-
-            for i = 1, length do
-                local p = VecAdd(VecLerp(slash.point1, slash.point2, i / length),
-                    VecScale(fwd, math.sin(i * math.pi / length) * 1))
-
-                local hitFwd, distFwd, normalFwd, shapeFwd = QueryRaycast(p, fwd, 0.42 * 5)
-                if hitFwd then
-                    local body = GetShapeBody(shapeFwd)
-                    if IsBodyDynamic(body) then
-                        slashedDynamicBodies[body] = { hit = 1, body = body }
-                        SetBodyDynamic(body, false)
-                        SetBodyVelocity(body, Vec(0, 0, 0))
-                        SetBodyAngularVelocity(body, Vec(0, 0, 0))
-                    elseif slashedDynamicBodies[body] then
-                        slashedDynamicBodies[body].hit = slashedDynamicBodies[body].hit + 1
-                    end
-                end
-
-                MakeHole(p, 0.42, 0.42, 0.42, true)
-
-                QueryRequire("physical dynamic")
-                local hitLeft, distLeft, normalLeft, shapeLeft = QueryRaycast(p, VecSub(normalDir, fwd), 0.42 * 5)
-                QueryRequire("physical dynamic")
-                local hitRight, distRight, normalRight, shapeRight = QueryRaycast(p, VecSub(VecScale(normalDir, -1), fwd),
-                    0.42 * 5)
-
-                if hitLeft then
-                    local body = GetShapeBody(shapeLeft)
-                    local vel = GetBodyVelocity(body)
-                    SetBodyVelocity(body, VecAdd(vel, VecScale(normalDir, 50 * dt)))
-                end
-                if hitRight then
-                    local body = GetShapeBody(shapeRight)
-                    local vel = GetBodyVelocity(body)
-                    SetBodyVelocity(body, VecAdd(vel, VecScale(normalDir, -50 * dt)))
-                end
-            end
-
-            if distance > 100 then
-                table.remove(slashes, i)
-            end
-        end
-    end
-
-    if slashedDynamicBodies then
-        for bodyhash, record in pairs(slashedDynamicBodies) do
-            if record and record.hit then
-                if record.hit > 4 then
-                    slashedDynamicBodies[bodyhash].hit = 1
-                else
-                    SetBodyDynamic(record.body, true)
-                    slashedDynamicBodies[bodyhash] = nil
-                end
-            end
-        end
-    end
-end
-
-function updateFrozenBodies(dt)
-    for bodyhash, record in pairs(frozen) do
-        if not grabbed or (grabbed and not grabbed.bodies[record.body]) then
-            SetBodyVelocity(record.body, Vec(0, 0, 0))
-            SetBodyAngularVelocity(record.body, Vec(0, 0, 0))
-            ApplyBodyImpulse(record.body,
-                TransformToParentPoint(GetBodyTransform(record.body), GetBodyCenterOfMass(record.body)),
-                Vec(0, GetBodyMass(record.body) * dt * 10, 0))
-        end
-    end
-end
-
-function updateWeightlessBodies(dt)
-    for bodyhash, record in pairs(weightless) do
-        if record then
-            ApplyBodyImpulse(record.body,
-                TransformToParentPoint(GetBodyTransform(record.body), GetBodyCenterOfMass(record.body)),
-                Vec(0, GetBodyMass(record.body) * dt * 10, 0))
-        end
-    end
-end
-
-function input(dt)
-    if clearing then
-        for i, voxel in ipairs(voxels) do
-            Delete(voxel)
-        end
-
-        for bodyhash, record in pairs(frozen) do
-            SetBodyVelocity(record.body, record.velocity)
-            SetBodyAngularVelocity(record.body, record.angVelocity)
-        end
-
-        frozen = {}
-        weightless = {}
-        voxels = {}
-        slashes = {}
-    end
-
-    if outlining then
-        for bodyhash, record in pairs(frozen) do
-            if outlining then
-                DrawBodyOutline(record.body, 0, 0, 1, 1)
-            end
-        end
-
-        for bodyhash, record in pairs(weightless) do
-            if outlining then
-                DrawBodyOutline(record.body, 1, 1, 0, 1)
-            end
-        end
-    end
-
-    local ct = GetCameraTransform()
-
-    if slashing and not slashed then
-        PlaySound(cuttingSound)
-
-        local slash = {
-            active = true,
-            dir1 = VecNormalize(VecSub(getSlashPoint(false, slashLength, slashAngle), ct.pos)),
-            dir2 = VecNormalize(VecSub(getSlashPoint(true, slashLength, slashAngle), ct.pos)),
-            point1 = ct.pos,
-            point2 = ct.pos,
-            origin = ct.pos,
-        }
-        table.insert(slashes, slash)
-
-        slashedDynamicBodies[slash] = {}
-
-        slashed = true
-    end
-
-    if InputReleased("lmb") then
-        slashed = false
-    end
-
-    local fwd = TransformToParentVec(ct, Vec(0, 0, -1))
-    local h, d, n, s = QueryRaycast(ct.pos, fwd, 1000)
-    local radius = points / 420
-
-    if h then
-        local hitPos = VecAdd(VecScale(fwd, d), ct.pos)
-
-        if alting and not showing then
-            if not IsBodyDynamic(GetShapeBody(s)) then
-                DrawShapeOutline(s, 1, 0, 0, 1)
-
-                if grab then
-                    PlaySound(detachingSound)
-                    detach(s)
-                end
-            end
-
-            radius = 0.1
-        end
-
-        if showing and not shifting and not alting then
-            SetBool("game.input.locktool", true)
-            local prevPoint = nil
-            for i = 1, points do
-                local theta = i * math.pi / points
-                local c = radius * 10
-                local spiralPoint = Vec(radius * math.sin(theta) * math.cos(theta * c + time * math.sqrt(radius) * 5),
-                    radius * math.sin(theta) * math.sin(theta * c + time * math.sqrt(radius) * 5),
-                    radius * math.cos(theta))
-                local point = VecAdd(hitPos, spiralPoint)
-
-                if prevPoint then
-                    DrawLine(prevPoint, point, 1, 0, 0, 0.5)
-                end
-
-                prevPoint = point
-            end
-
-            points = clamp(points + InputValue("mousewheel") * 300, 100, 10000)
-        end
-
-
-        if not grabbed and not slashing then
-            local dir = Vec(radius, radius, radius)
-            local min = VecSub(hitPos, dir)
-            local max = VecAdd(hitPos, dir)
-            QueryRequire("physical dynamic")
-            local bodies = QueryAabbBodies(min, max)
-            local player = GetPlayerTransform()
-
-            local inside = {}
-            local relatives = {}
-
-            local count = 0
-            for i, body in ipairs(bodies) do
-                local hit, point, normal = GetBodyClosestPoint(body, hitPos)
-
-                if hit and VecLength(VecSub(point, hitPos)) <= radius then
-                    if outlining then
-                        DrawBodyOutline(body, 0, 1, 0.42, 1)
-                    end
-
-                    local tr = GetBodyTransform(body)
-                    relatives[body] = {
-                        position = TransformToLocalPoint(tr, hitPos),
-                        rotation =
-                            TransformToLocalTransform(player, tr)
-                    }
-                    inside[body] = body
-                    count = count + 1
-                end
-            end
-
-            if count > 0 and (grabbing or pulling or pushing or freezing or rotating or liquifying or imploding or explode or floating or explodeOnNextFrame) then
-                grabbed = { bodies = inside, dist = d, relatives = relatives }
-            end
-        end
-    end
-
-    if showing and (shifting or alting) then
-        SetBool("game.input.locktool", true)
-        DebugLine(getSlashPoint(false, slashLength, slashAngle), getSlashPoint(true, slashLength, slashAngle), 1, 0, 0)
-
-        if alting then
-            slashAngle = slashAngle + InputValue("mousewheel") * dt * 25
-            slashAngle = slashAngle % math.pi
-        else
-            slashLength = clamp(slashLength + InputValue("mousewheel") * 10, 10, 200)
-        end
-    end
-
-    if grabbed then
-        SetBool("game.disableinteract", true)
-
-        if outlining then
-            for i, body in pairs(grabbed.bodies) do
-                DrawBodyOutline(body, math.random(), math.random(), math.random(), 1)
-            end
-        end
-
-        if pulling then
-            if grabbed.dist - 1 > radius * 1.5 then grabbed.dist = grabbed.dist - 1 end
-        end
-
-        if pushing then
-            grabbed.dist = grabbed.dist + 1
-        end
-
-        if push then
-            PlaySound(pushingSound)
-        end
-
-        if pull then
-            PlaySound(pullingSound)
-        end
-
-        if rotating then
-            SetBool("game.player.disableinput", true)
-
-            for i, relative in pairs(grabbed.relatives) do
-                relative.rotation.rot = QuatRotateQuat(
-                    QuatEuler(InputValue("mousedy") * 0.1, InputValue("mousedx") * 0.1, 0), relative.rotation.rot)
-            end
-        end
-
-        -- grabbing
-        if not floating and not exploding and not liquifying and released and not freezing then
-            PlayLoop(grabbingLoop)
-
-            local origin = VecAdd(VecScale(fwd, grabbed.dist), ct.pos)
-            local player = GetPlayerTransform()
-            for i, body in pairs(grabbed.bodies) do
-                local tr = GetBodyTransform(body)
-                local rotation = TransformToParentTransform(player, grabbed.relatives[i].rotation).rot
-                local x, y, z = GetQuatEuler(QuatRotateQuat(tr.rot,
-                    Quat(-rotation[1], -rotation[2], -rotation[3], rotation[4])))
-
-                SetBodyVelocity(body,
-                    VecScale(VecSub(origin, TransformToParentPoint(tr, grabbed.relatives[i].position)), 8))
-                SetBodyAngularVelocity(body, VecScale(Vec(x, y, z), -0.1))
-            end
-        end
-
-        if imploding and not exploding then
-            PlayLoop(implodingLoop)
-
-            local origin = VecAdd(VecScale(fwd, grabbed.dist), ct.pos)
-            for i, body in pairs(grabbed.bodies) do
-                local dir = VecScale(
-                    VecNormalize(VecSub(TransformToParentPoint(GetBodyTransform(body), GetBodyCenterOfMass(body)), origin)),
-                    -30)
-                SetBodyVelocity(body, dir)
-            end
-
-            -- recalculate grabbed
-            local dir = Vec(radius, radius, radius)
-            local min = VecSub(origin, dir)
-            local max = VecAdd(origin, dir)
-            QueryRequire("physical dynamic")
-            local bodies = QueryAabbBodies(min, max)
-
-            local relatives = {}
-            for i, body in pairs(bodies) do
-                local tr = GetBodyTransform(body)
-                table.insert(relatives,
-                    {
-                        position = TransformToLocalPoint(tr, origin),
-                        rotation = TransformToLocalTransform(
-                            GetPlayerTransform(), tr)
-                    })
-            end
-
-            grabbed.relatives = relatives
-            grabbed.bodies = bodies
-        end
-
-        if explode or explodeOnNextFrame then
-            if explode then
-                PlaySound(explodingSound)
-            end
-
-            local origin = VecAdd(VecScale(fwd, grabbed.dist), ct.pos)
-            for i, body in pairs(grabbed.bodies) do
-                local dir = VecScale(
-                    VecNormalize(VecSub(TransformToParentPoint(GetBodyTransform(body), GetBodyCenterOfMass(body)), origin)),
-                    100)
-                SetBodyVelocity(body, VecAdd(GetBodyVelocity(body), dir))
-            end
-
-            if explode then
-                MakeHole(origin, radius, radius, radius)
-            end
-
-            if explodeOnNextFrame then
-                explodeOnNextFrame = false
-            end
-
-            if explode then
-                explodeOnNextFrame = true
-            end
-
-            grabbed = nil
-            return
-        end
-
-        if floating then
-            PlaySound(floatingSound)
-
-            for i, body in pairs(grabbed.bodies) do
-                if weightless[body] then
-                    weightless[body] = nil
-                else
-                    weightless[body] = { body = body }
-                end
-            end
-
-            grabbed = nil
-            return
-        end
-
-        if liquifying then
-            PlaySound(liquifyingSound)
-
-            for i, body in pairs(grabbed.bodies) do
-                local shapes = GetBodyShapes(body)
-
-                for j, shape in ipairs(shapes) do
-                    liquify(shape)
-                end
-            end
-
-            grabbed = nil
-            released = false
-            return
-        end
-
-        if freezing then
-            PlaySound(freezingSound)
-
-            for i, body in pairs(grabbed.bodies) do
-                if frozen[body] then
-                    local record = frozen[body]
-                    SetBodyVelocity(body, record.velocity)
-                    SetBodyAngularVelocity(body, record.angVelocity)
-
-                    frozen[body] = nil
-                else
-                    frozen[body] = {
-                        velocity = GetBodyVelocity(body),
-                        angVelocity = GetBodyAngularVelocity(body),
-                        body =
-                            body
-                    }
-                end
-            end
-
-            grabbed = nil
-            return
-        end
-
-        -- release
-        if not grabbing and not pushing and not pulling and not freezing and not rotating and not imploding then
-            grabbed = nil
-        end
-    end
-end
-
-function liquify(shape)
-    local object = {}
-
-    local x, y, z = GetShapeSize(shape)
-    local t = GetShapeWorldTransform(shape)
-    local body = GetShapeBody(shape)
-    for i = 0, x do
-        for j = 0, y do
-            for k = 0, z do
-                local m, r, g, b, a = GetShapeMaterialAtIndex(shape, i, j, k)
-                if a > 0 then
-                    local pos = TransformToParentPoint(t, Vec(i / 10, j / 10, k / 10))
-                    local vel = GetBodyVelocityAtPos(body, pos)
-                    table.insert(object, { m = m, r = r, g = g, b = b, a = a, pos = pos, rot = t.rot, vel = vel })
-                end
-            end
-        end
-    end
-
-    local spawnOdds = math.ceil(GetShapeVoxelCount(shape) / 10000)
-    if spawnOdds < 1 then spawnOdds = 1 end
-
-    Delete(shape)
-
-    for i, voxel in ipairs(object) do
-        if math.random(1, spawnOdds) == spawnOdds then
-            local vox = Spawn(
-                "<voxbox size='1 1 1' prop='true' material='" ..
-                voxel.m .. "' color='" .. voxel.r .. " " .. voxel.g .. " " .. voxel.b .. " " .. voxel.a .. "'/>",
-                Transform(voxel.pos, t.rot))
-            SetBodyVelocity(vox[1], voxel.vel)
-
-            table.insert(voxels, vox[1])
-        end
-    end
-end
-
-function detach(shape)
-    function hole(p, center)
-        local h, d, n, s = QueryRaycast(p, VecSub(p, center), 0.1)
-        if h and not IsBodyDynamic(GetShapeBody(s)) then
-            MakeHole(p, 0.15, 0.15, 0.15, true)
-        end
-    end
-
-    if GetShapeVoxelCount(shape) < 1000000 then
-        min, max = GetShapeBounds(shape)
-    end
-
-    if min and max then
-        local center = VecLerp(min, max, 0.5)
-        local length1 = max[1] - min[1]
-        local length2 = max[2] - min[2]
-        local length3 = max[3] - min[3]
-        local count1 = length1 / 0.1
-        local count2 = length2 / 0.1
-        local count3 = length3 / 0.1
-        local faces = {
-            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), length2 * (j / count2), 0)), center) end,       c1 = count1, c2 = count2 },
-            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), length2 * (j / count2), length3)), center) end, c1 = count1, c2 = count2 },
-            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), 0, length3 * (j / count3))), center) end,       c1 = count1, c2 = count3 },
-            { p = function(i, j) hole(VecAdd(min, Vec(length1 * (i / count1), length2, length3 * (j / count3))), center) end, c1 = count1, c2 = count3 },
-            { p = function(i, j) hole(VecAdd(min, Vec(0, length2 * (i / count2), length3 * (j / count3))), center) end,       c1 = count2, c2 = count3 },
-            { p = function(i, j) hole(VecAdd(min, Vec(length1, length2 * (i / count2), length3 * (j / count3))), center) end, c1 = count2, c2 = count3 }
-        }
-
-        for f = 1, #faces do
-            for i = 1, faces[f].c1 do
-                for j = 1, faces[f].c2 do
-                    faces[f].p(i, j)
-                end
-            end
-        end
-    end
-end
-
-function clamp(n, min, max) return math.min(math.max(n, min), max) end
-
-function getSlashPoint(negative, length, angle)
-    local sign = 1
-    if negative then sign = -1 end
-    return VecAdd(GetCameraTransform().pos,
-        TransformToParentVec(GetCameraTransform(),
-            Vec(length * math.cos(angle) * sign, length * math.sin(angle) * sign, -250)))
-end
-
-function optionsSlider(val, min, max)
-    UiColor(0.2, 0.6, 1)
-    UiPush()
-    UiTranslate(0, -8)
-    val = (val - min) / (max - min)
-    local w = 195
-    local done = false
-    UiRect(w, 3)
-    UiAlign("center middle")
-    UiTranslate(-195, 1)
-    val, done = UiSlider("ui/common/dot.png", "x", val * w, 0, w) / w
-    val = round((val * (max - min) + min), 2)
-    UiPop()
-    return val, done
-end
-
-function round(number, decimals)
-    local power = 10 ^ decimals
-    return math.floor(number * power) / power
-end

```
