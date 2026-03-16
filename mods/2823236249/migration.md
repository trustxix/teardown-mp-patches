# Migration Report: script\helper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\helper.lua
+++ patched/script\helper.lua
@@ -1,7 +1,4 @@
-----------------------------------------------------------------------------------------------------
--- Arithmetic
-----------------------------------------------------------------------------------------------------
-
+#version 2
 function clamp(val, min, max)
 	if val < min then
 		return min
@@ -75,12 +72,7 @@
 	return a[1] * b[1] + a[2] * b[2] + a[3] * b[3]
 end
 
--- Challenge by @TallTim and @1ssnl to make the smallest rounding function
 function Round(n,d)x=1/d return math.floor(n*x+.5)/x end
-
-----------------------------------------------------------------------------------------------------
--- Getters
-----------------------------------------------------------------------------------------------------
 
 function jointdata(name)
     local t = {}
@@ -111,13 +103,13 @@
 function GetKeyWithDefault(type, path, default)
 	if not HasKey(path) then
 		if type == 'float' then
-			SetFloat(path, value)
+			SetFloat(path, value, true)
 		elseif type == 'int' then
-			SetInt(path, value)
+			SetInt(path, value, true)
 		elseif type == 'bool' then
-			SetBool(path, value)
+			SetBool(path, value, true)
 		elseif type == 'string' then
-			SetString(path, value)
+			SetString(path, value, true)
 		else
 			DebugPrint('GetKeyWithDefault: Invalid type ['..type..']')
 		end
@@ -146,10 +138,6 @@
 	end
 end
 
-----------------------------------------------------------------------------------------------------
--- Debugging
-----------------------------------------------------------------------------------------------------
-
 function WatchTable(Table, prefix)
 	prefix = prefix or 'Table'
 	
@@ -162,20 +150,12 @@
 	end
 end
 
-----------------------------------------------------------------------------------------------------
--- Other
-----------------------------------------------------------------------------------------------------
-
 function NoGrav(body, dt)
 	local nograv = VecScale(Vec(0, 10, 0), dt)
 	local com = TransformToParentPoint(GetBodyTransform(body), GetBodyCenterOfMass(body))
 	DebugCross(com)
 	ApplyBodyImpulse(body, com, VecScale(nograv, GetBodyMass(body)))
 end
-
-----------------------------------------------------------------------------------------------------
--- User Interface
-----------------------------------------------------------------------------------------------------
 
 function UiGetSliderDot()
 	local width, height = UiGetImageSize("ui/common/dot.png")
@@ -265,7 +245,7 @@
 		value = math.min(value, max)
 
 		if type(pathorvalue) == "string" then
-			SetFloat(pathorvalue, value)
+			SetFloat(pathorvalue, value, true)
 		end
 	UiPop()
 
@@ -320,7 +300,7 @@
 	UiPop()
 
 	if type(pathorvalue) == "string" then
-		SetBool(pathorvalue, value)
+		SetBool(pathorvalue, value, true)
 	end
 
 	return {value = value, hover = hover, hoveroption = hoveroption, rect = {w = rw, h = rh}}
@@ -442,4 +422,5 @@
 	UiPop()
 
 	return {w = rectw, h = recth}
-end+end
+

```

---

# Migration Report: script\machine.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\machine.lua
+++ patched/script\machine.lua
@@ -1,5 +1,4 @@
-#include helper.lua
-
+#version 2
 local function disablecol(dt)
     local bs = FindShapes(nil)
     local norep = {}
@@ -19,12 +18,96 @@
     end
 end
 
-function init()
-
+function supportUpdate()
+
+    if GetPlayerGrabBody(playerId) == supportBody or GetPlayerGrabBody(playerId) == railBody then 
+        -- DebugPrint(JointDict.yaw.joint)
+        SetJointMotorTarget(JointDict.pitch.joint, 0,5,1000)
+        SetJointMotorTarget(JointDict.rail.joint, 0,5,0)
+        SetJointMotorTarget(JointDict.support1.joint, JointDict.support1.lockangle,0,0)
+        SetJointMotorTarget(JointDict.support2.joint, JointDict.support2.lockangle,0,0)
+
+        DrawShapeOutline(supportBody, 1, 1, 1, 1)
+        JointDict.rail.lockangle = GetJointMovement(JointDict.rail.joint)
+        JointDict.support1.lockangle = GetJointMovement(JointDict.support1.joint)
+        JointDict.support2.lockangle = GetJointMovement(JointDict.support1.joint)
+        JointDict.pitch.lockangle = GetJointMovement(JointDict.pitch.joint)
+    else
+        SetJointMotorTarget(JointDict.rail.joint, JointDict.rail.lockangle,80)
+        SetJointMotorTarget(JointDict.support1.joint, JointDict.support1.lockangle,10)
+        --SetJointMotorTarget(JointDict.support2.joint, JointDict.support2.lockangle,10)
+        SetJointMotorTarget(JointDict.pitch.joint, JointDict.pitch.lockangle,10)
+    end
+end
+
+function IsBodyMachine(body)
+    if body == 0 then 
+        return false
+    end
+
+    local bodies = FindBodies()
+    for i in pairs(bodies) do
+        if bodies[i] == body then
+            return true
+        end
+    end
+    return false 
+end
+
+function RejectAllBodies(list)
+    for i=1,#list do
+        QueryRejectBody(list[i])
+    end
+end
+
+function Align()
+    local t = TransformToParentTransform(GetBodyTransform(launcher), launcherTip)
+    local dir = TransformToParentVec(t, Vec(0, 0, -1))
+    RejectAllBodies(FindBodies())
+    local rayhit, raydist, raynormal, rayshape = QueryRaycast(t.pos, dir, 3, 0.1, false)
+
+    if rayhit and rayshape ~= FindShape("pully") and HasTag(GetShapeBody(rayshape),"projectile") then
+        local proj = GetShapeBody(rayshape)
+        ConstrainOrientation(proj, 0, GetBodyTransform(proj).rot , GetBodyTransform(launcher).rot,2,1000)
+    end
+end
+
+function predictPath()
+    local launcherPos = GetBodyTransform(launcher).pos
+    local launcherTransform = Transform(VecAdd(launcherPos,Vec(0,2,0)), GetBodyTransform(launcher).rot)
+
+    local t = TransformToParentTransform(launcherTransform, launcherTip)
+    local dir = TransformToParentVec(t, Vec(0, 0, -1))
+    local vel = VecScale(dir,70)
+    local gravity = -10
+
+    for i=1,300 do
+        time = 0.03*i
+        local vX = vel[1]
+        local vY = vel[2]
+        local vZ = vel[3]
+        local x = vX * time
+        local z = vZ * time
+        local y = vY * time + 0.5 * gravity * time * time
+
+        local pos = Vec(x,y,z)
+        local ppos = VecAdd(t.pos,pos)
+
+        if 3 < i then
+            DebugLine(prev,ppos,1,1,1,1)
+            local hit,point = QueryClosestPoint(ppos,1.5)
+            if hit or IsPointInWater(ppos) then
+                DebugCross(point)
+                break
+            end
+        end
+        prev = ppos
+    end
+end
+
+function server.init()
     launcher = FindBody('launcher')
     launcherTip = TransformToLocalTransform(GetBodyTransform(launcher), GetLocationTransform(FindLocation('launcher', false)))
-
-
     JointDict = {
         shoot = jointdata('shoot'),
         pully = jointdata('pullyJoint'),
@@ -36,48 +119,108 @@
         support1 = jointdata('support1'),
         support2 = jointdata('support2')
     }
-    
     PulledBack = false
     Disabled = false
-
-
     armShapes = FindShapes('arm')
     pullyBody = FindBody("pully",false)
     supportBody = FindBody("support")
     railBody = FindBody("rail")
-
     FireCheckTime = -1
-
-end
-
-function tick(dt)
-    if not Disabled then
-        for k, v in pairs(JointDict.ropes) do
-            if IsJointBroken(v.joint) then 
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not Disabled then
+            for k, v in pairs(JointDict.ropes) do
+                if IsJointBroken(v.joint) then 
+                    Disabled = true
+                    PulledBack = false
+                    -- DebugPrint("Rope broken : "..v.joint)
+                    FireCheckTime = 0.25
+                    break
+                end
+            end
+        end
+        for k, v in ipairs(armShapes) do
+            -- DrawShapeHighlight(v,1)
+            if IsShapeBroken(v) then 
                 Disabled = true
                 PulledBack = false
-                -- DebugPrint("Rope broken : "..v.joint)
                 FireCheckTime = 0.25
                 break
             end
         end
-    end
-    for k, v in ipairs(armShapes) do
-        -- DrawShapeHighlight(v,1)
-        if IsShapeBroken(v) then 
-            Disabled = true
-            PulledBack = false
-            FireCheckTime = 0.25
-            break
-        end
-    end
-
-    if Disabled then
-        RemoveTag(pullyBody, 'interact')
-    end
-
-    if GetPlayerInteractBody() == pullyBody and not Disabled then
-        local interacted = GetPlayerInteractBody()
+        if Disabled then
+            RemoveTag(pullyBody, 'interact')
+        end
+        if PulledBack and not Disabled then
+            SetJointMotorTarget(JointDict.shoot.joint, JointDict.shoot.max - 0.5, 8)
+            SetJointMotorTarget(JointDict.pully.joint, JointDict.pully.max, 8)
+            predictPath()
+        else
+            SetJointMotorTarget(JointDict.shoot.joint, JointDict.shoot.min, 25)
+            SetJointMotorTarget(JointDict.pully.joint, JointDict.pully.min, 25)
+        end
+        if IsBodyMachine(GetPlayerGrabBody(playerId)) and GetPlayerGrabBody(playerId) ~= supportBody and GetPlayerGrabBody(playerId) ~= railBody then 
+            SetJointMotor(JointDict.yaw.joint, 0,0)
+            JointDict.yaw.lockangle = GetJointMovement(JointDict.yaw.joint)
+        else
+            SetJointMotorTarget(JointDict.yaw.joint, JointDict.yaw.lockangle,0.5)
+        end
+        supportUpdate()
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not Disabled then
+            for k, v in ipairs(JointDict.arms) do
+                SetJointMotorTarget(v.joint, v.max, 3, 10000)
+            end
+        else 
+            for k, v in ipairs(JointDict.arms) do
+                SetJointMotorTarget(v.joint, v.max, 0, 0)
+            end
+        end
+        -- FIRE!!!!
+        if FireCheckTime ~= 0 then
+            disablecol(dt)
+
+            local t = TransformToParentTransform(GetBodyTransform(launcher), launcherTip)
+            local dir = TransformToParentVec(t, Vec(0, 0, -1))
+
+            RejectAllBodies(FindBodies())
+            local rayhit, raydist, raynormal, rayshape = QueryRaycast(t.pos, dir, 0.5, 0.1, false)
+            -- DebugWatch('rayhit', rayhit)
+            -- DebugWatch('raydist', raydist)
+            -- DebugWatch('rayshape', rayshape)
+            -- DebugWatch('raynormal', raynormal)
+
+            if rayhit and rayshape ~= FindShape("pully") then
+                local proj = GetShapeBody(rayshape)
+                -- DebugWatch('proj', proj)
+                if HasTag(proj, 'projectile') then
+                    ConstrainVelocity(proj, 0, t.pos, dir, 70)
+                    SetTag(rayshape,'shot',"1")
+                else
+                    ConstrainVelocity(proj, 0, t.pos, dir, 120)
+                end
+            end
+
+            FireCheckTime = FireCheckTime - dt
+        else
+           enablecol()
+        end
+        if GetPlayerGrabBody(playerId) ~= supportBody and GetPlayerGrabBody(playerId) ~= railBody then 
+            Align()
+        end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractBody(playerId) == pullyBody and not Disabled then
+        local interacted = GetPlayerInteractBody(playerId)
         DrawBodyOutline(interacted, 1, 1, 1, 1)
 
         if InputPressed('interact') then
@@ -93,175 +236,22 @@
             end
         end
     end
-
-    if PulledBack and not Disabled then
-        SetJointMotorTarget(JointDict.shoot.joint, JointDict.shoot.max - 0.5, 8)
-        SetJointMotorTarget(JointDict.pully.joint, JointDict.pully.max, 8)
-        predictPath()
-    else
-        SetJointMotorTarget(JointDict.shoot.joint, JointDict.shoot.min, 25)
-        SetJointMotorTarget(JointDict.pully.joint, JointDict.pully.min, 25)
-    end
-
-
-    if IsBodyMachine(GetPlayerGrabBody()) and GetPlayerGrabBody() ~= supportBody and GetPlayerGrabBody() ~= railBody then 
-        SetJointMotor(JointDict.yaw.joint, 0,0)
-        JointDict.yaw.lockangle = GetJointMovement(JointDict.yaw.joint)
-    else
-        SetJointMotorTarget(JointDict.yaw.joint, JointDict.yaw.lockangle,0.5)
-    end
-
-
-    supportUpdate()
-end
-
-function supportUpdate()
-
-    if GetPlayerGrabBody() == supportBody or GetPlayerGrabBody() == railBody then 
-        -- DebugPrint(JointDict.yaw.joint)
-        SetJointMotorTarget(JointDict.pitch.joint, 0,5,1000)
-        SetJointMotorTarget(JointDict.rail.joint, 0,5,0)
-        SetJointMotorTarget(JointDict.support1.joint, JointDict.support1.lockangle,0,0)
-        SetJointMotorTarget(JointDict.support2.joint, JointDict.support2.lockangle,0,0)
-
-        DrawShapeOutline(supportBody, 1, 1, 1, 1)
-        JointDict.rail.lockangle = GetJointMovement(JointDict.rail.joint)
-        JointDict.support1.lockangle = GetJointMovement(JointDict.support1.joint)
-        JointDict.support2.lockangle = GetJointMovement(JointDict.support1.joint)
-        JointDict.pitch.lockangle = GetJointMovement(JointDict.pitch.joint)
-    else
-        SetJointMotorTarget(JointDict.rail.joint, JointDict.rail.lockangle,80)
-        SetJointMotorTarget(JointDict.support1.joint, JointDict.support1.lockangle,10)
-        --SetJointMotorTarget(JointDict.support2.joint, JointDict.support2.lockangle,10)
-        SetJointMotorTarget(JointDict.pitch.joint, JointDict.pitch.lockangle,10)
-    end
-end
-
-function IsBodyMachine(body)
-    if body == 0 then 
-        return false
-    end
-
-    local bodies = FindBodies()
-    for i in pairs(bodies) do
-        if bodies[i] == body then
-            return true
-        end
-    end
-    return false 
-end
-
-function update(dt)
-    -- Applies tension to the arm joints
-    if not Disabled then
-        for k, v in ipairs(JointDict.arms) do
-            SetJointMotorTarget(v.joint, v.max, 3, 10000)
-        end
-    else 
-        for k, v in ipairs(JointDict.arms) do
-            SetJointMotorTarget(v.joint, v.max, 0, 0)
-        end
-    end
-
-    -- FIRE!!!!
-    if FireCheckTime > 0 then
-        disablecol(dt)
-
-        local t = TransformToParentTransform(GetBodyTransform(launcher), launcherTip)
-        local dir = TransformToParentVec(t, Vec(0, 0, -1))
-
-        RejectAllBodies(FindBodies())
-        local rayhit, raydist, raynormal, rayshape = QueryRaycast(t.pos, dir, 0.5, 0.1, false)
-        -- DebugWatch('rayhit', rayhit)
-        -- DebugWatch('raydist', raydist)
-        -- DebugWatch('rayshape', rayshape)
-        -- DebugWatch('raynormal', raynormal)
-
-        if rayhit and rayshape ~= FindShape("pully") then
-            local proj = GetShapeBody(rayshape)
-            -- DebugWatch('proj', proj)
-            if HasTag(proj, 'projectile') then
-                ConstrainVelocity(proj, 0, t.pos, dir, 70)
-                SetTag(rayshape,'shot',"1")
-            else
-                ConstrainVelocity(proj, 0, t.pos, dir, 120)
-            end
-        end
-
-        FireCheckTime = FireCheckTime - dt
-    else
-       enablecol()
-    end
-
-    if GetPlayerGrabBody() ~= supportBody and GetPlayerGrabBody() ~= railBody then 
-        Align()
-    end
-end
-
-function RejectAllBodies(list)
-    for i=1,#list do
-        QueryRejectBody(list[i])
-    end
-end
-
-function Align()
-    local t = TransformToParentTransform(GetBodyTransform(launcher), launcherTip)
-    local dir = TransformToParentVec(t, Vec(0, 0, -1))
-    RejectAllBodies(FindBodies())
-    local rayhit, raydist, raynormal, rayshape = QueryRaycast(t.pos, dir, 3, 0.1, false)
-
-    if rayhit and rayshape ~= FindShape("pully") and HasTag(GetShapeBody(rayshape),"projectile") then
-        local proj = GetShapeBody(rayshape)
-        ConstrainOrientation(proj, 0, GetBodyTransform(proj).rot , GetBodyTransform(launcher).rot,2,1000)
-    end
-end
-
-function predictPath()
-    local launcherPos = GetBodyTransform(launcher).pos
-    local launcherTransform = Transform(VecAdd(launcherPos,Vec(0,2,0)), GetBodyTransform(launcher).rot)
-
-    local t = TransformToParentTransform(launcherTransform, launcherTip)
-    local dir = TransformToParentVec(t, Vec(0, 0, -1))
-    local vel = VecScale(dir,70)
-    local gravity = -10
-
-    for i=1,300 do
-        time = 0.03*i
-        local vX = vel[1]
-        local vY = vel[2]
-        local vZ = vel[3]
-        local x = vX * time
-        local z = vZ * time
-        local y = vY * time + 0.5 * gravity * time * time
-
-        local pos = Vec(x,y,z)
-        local ppos = VecAdd(t.pos,pos)
-
-        if 3 < i then
-            DebugLine(prev,ppos,1,1,1,1)
-            local hit,point = QueryClosestPoint(ppos,1.5)
-            if hit or IsPointInWater(ppos) then
-                DebugCross(point)
-                break
-            end
-        end
-        prev = ppos
-    end
-end
-
-function draw()
+end
+
+function client.draw()
     if not disabled then
-        local distSupport = VecDist(GetBodyTransform(supportBody).pos, GetPlayerTransform().pos)
+        local distSupport = VecDist(GetBodyTransform(supportBody).pos, GetPlayerTransform(playerId).pos)
         if distSupport < 6 and IsBodyVisible(supportBody,5,false) then 
             local t = GetBodyTransform(supportBody)
             local x, y = UiWorldToPixel(t.pos)
             UiTooltip("Grab to change angle",1.2, "center", {x, y}, 0.5)
         end 
-        local pullyDist = VecDist(GetBodyTransform(pullyBody).pos, GetPlayerTransform().pos)
+        local pullyDist = VecDist(GetBodyTransform(pullyBody).pos, GetPlayerTransform(playerId).pos)
         if pullyDist < 6 and IsBodyVisible(pullyBody,5,false) then 
             local t = GetBodyTransform(pullyBody)
             local x, y = UiWorldToPixel(VecAdd(t.pos,Vec(0,-0.5,0)))
             UiTooltip("Grab to aim",1.2, "center", {x, y}, 0.5)
         end 
     end
-end+end
+

```

---

# Migration Report: script\projectile.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\projectile.lua
+++ patched/script\projectile.lua
@@ -1,5 +1,4 @@
-#include helper.lua
-
+#version 2
 local function lengthToWorld(body, length)
 	local loc = TransformToParentPoint(GetBodyTransform(body), {0, 0, -length})
 	return loc
@@ -44,69 +43,6 @@
     end
     
     return ClosestLauncher, LowestDistance
-end
-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------
-
-function init()
-	TrackedProjectiles = {}
-
-	MinimumVelocity = 20
-	TimeGainMulti = 2
-	SkewerOpenVelocity = 20
-    RaycastDistance = 0.25
-
-	ShowDebug = false
-    timer = 0
-    cameraTimer = 0
-
-    trajectoryOrigin = 0
-    projectileHit = 0
-    highestPoint = -1
-    stopFollow = false
-
-    Proj = FindBody('projectile', false)
-    ProjTrans = GetBodyTransform(Proj)
-    ProjShapes = GetBodyShapes(Proj)
-    for i=1,#ProjShapes do
-        local shape = ProjShapes[i]
-        DrawShapeOutline(shape, 1, 1, 1, 1)
-        SetShapeCollisionFilter(shape, 2, 255-2)
-    end
-
-    tipvec = locvec('tip')
-    maxdt = tonumber(GetTagValue(Proj - 1, 'maxdt')) or 1
-    dacc = tonumber(GetTagValue(Proj - 1, 'dacc')) or 1
-    homing = tonumber(GetTagValue(Proj - 1, 'homing')) or 0
-    explosive = HasTag(Proj - 1, 'explosive')
-    skewer = HasTag(Proj - 1, 'skewer')
-    gunpowder = HasTag(Proj - 1, 'gunpowder')
-
-    _drilltime = -1
-    _speedmulti = 1
-    _activated = false
-
-    _track = {
-        rot = ProjTrans.rot,
-        vel = Vec(0,0,0)
-    }
-
-    -- DebugWatch('tipvec', tipvec)
-    -- DebugWatch('maxdt', maxdt)
-    -- DebugWatch('dacc', dacc)
-    -- DebugWatch('homing', homing)
-    -- DebugWatch('explosive', explosive)
-    -- DebugWatch('skewer', skewer)
-
-end
-
-function tick(dt)
-	if InputPressed("f1") then ShowDebug = not ShowDebug end
-
-    local tippos = vectoloc(tipvec).pos
-    local speed = speedAtPos(Proj, tippos)
-
-    SetCamera(dt)
 end
 
 function SetCamera(dt)
@@ -134,7 +70,7 @@
     end
     
     -- if projectile was set(meaning the calculationw as already done) speed is larger 1 
-    if projectileHit ~= 0 and speed > 1 and stopFollow ~= true or cameraTimer > 0 then 
+    if projectileHit ~= 0 and speed > 1 and stopFollow ~= true or cameraTimer ~= 0 then 
         if InputDown('interact') then
             if highestPoint ~= -1 then
                 -- there are two camera angles in a trajectory. 
@@ -194,7 +130,6 @@
         end
         prev = ppos
 
-
         if 1 ~= i then
             QueryRejectBody(Proj)
             QueryRequire("physical large")
@@ -210,141 +145,182 @@
     return 0,0,highestPoint
 end
 
-function update(dt)
-    ProjTrans = GetBodyTransform(Proj)
-    local tippos = vectoloc(tipvec).pos
-    local speed = speedAtPos(Proj, tippos)
-    local dir = TransformToParentVec(ProjTrans, {0, 0, -1})
-
-    local grabbed = (GetPlayerGrabBody() == Proj)
-
-
-    -- Projectile Damage, Drilling, and Destruction System
-    local additionaldist = 0
-    if speed > MinimumVelocity then
-        for k,v in ipairs(ProjShapes) do
-            QueryRejectShape(v)
-        end
-        local rayhit, raydist, rayshape, raynormal = QueryRaycast(tippos, dir, RaycastDistance, 0, false)
-        
-        if rayhit then
-            -- Check if this is something that can be broken
-            if true then
-                if _drilltime == -1 then
-                    _drilltime = 0
-                    _speedmulti = 1
-                    _track.rot = ProjTrans.rot
-                    _track.vel = speedAtPos(Proj, Vec(0,0,0))
-                    additionaldist = raydist
-                else
-                    _drilltime = _drilltime - (dt * (maxdt * TimeGainMulti))
-                    _drilltime = math.max(_drilltime, 0)
-
-                    _speedmulti = _speedmulti - (dt * dacc)
-                    _speedmulti = math.max(_speedmulti, 0)
-                end
-            else
-                _drilltime = -1
-            end
-        end
-    end
-
-    -- Drilling
-    if _drilltime >= 0 and not _activated then
-        ConstrainVelocity(Proj, 0, tippos, dir, _speedmulti * _track.vel)
-        SetBodyAngularVelocity(Proj, Vec(0,0,0))
-        
-        local nograv = VecScale(Vec(0, 1, 0), 10 * dt * 1)
-        local com = GetBodyCenterOfMass(Proj)
-        ApplyBodyImpulse(Proj, com, VecScale(nograv, GetBodyMass(Proj)))
-        
-        _drilltime = _drilltime + dt
-
-        if gunpowder and not _activated then
-            for i = 1, 5 do
-                RemoveTagFrom(FindShapes(),"unbreakable")
-                Explosion(VecAdd(ProjTrans.pos, rndVec(math.random(0, 2))), 0)
-            end
-        end
-        
-        if _drilltime > maxdt then
-            if explosive and not _activated then
-                -- DebugPrint("Explosive")
-                RemoveTagFrom(FindShapes(),"unbreakable")
-                Explosion(tippos, 2.25)
-                -- RemoveTag('projectile')
-                -- Delete(Proj - 1)
-            end
-
-            if skewer then
-                local i = 2
-                while GetEntityType(Proj + i) == "joint" do
-                    Delete(Proj + i)
-                    i = i + 1
-                end
-                -- RemoveTag('projectile')
-                -- Delete(Proj - 1)
-            end
-
-            _drilltime = -1
-            _activated = true
-        end
-
-    else
-        _drilltime = -1
-    end
-
-    -- Homing (Points Towards Velocity at higher speeds)
-    if homing > 0 and not _activated and not grabbed then
-        local curvel = GetBodyVelocity(Proj)
-        local ideal = QuatLookAt(Vec(0,0,0), curvel)
-        local impact = logistic(speed, homing, -0.2, 20)
-        
-        local slerped = QuatSlerp(ProjTrans.rot, ideal, logistic(speed, 1, -0.6, 20))
-        
-
-        ConstrainOrientation(Proj, 0, ProjTrans.rot, slerped, impact, impact * 1000)
-    end
-    
-    -- skewer Extend
-    if skewer and not grabbed then
-        local i = 2
-        while GetEntityType(Proj + i) == "joint" do
-            local min, max = GetJointLimits(Proj + i)
-            local tar = (_activated or speed > SkewerOpenVelocity) and big(min, max) or small(min, max)
-            SetJointMotorTarget(Proj + i, tar, 8)
-            
-            i = i + 1
-        end
-    end
-
-    -- Grabbing Alignment
-    if grabbed then
-        local Launcher, Distance = FindClosestLauncher()
-
-        if Launcher ~= nil then
-            local LTrans = GetBodyTransform(Launcher)
-
-            -- LOGISTIC EXPLANATION
-            -- https://www.desmos.com/calculator/vwal5m5mbi
-            -- DebugPrint(Distance)
-            local impact = logistic(Distance, 1, 0.5, 6)
-            impact = impact * math.max(0.1, (VecDot(TransformToParentVec(ProjTrans, Vec(0, 0, -1)), TransformToParentVec(LTrans, Vec(0, 0, -1)))))
-            ConstrainOrientation(Proj, 0, ProjTrans.rot, LTrans.rot, impact)
-            -- SetBodyTransform(Proj, Transform(ProjTrans.pos, LTrans.rot))
-
-            NoGrav(Proj, dt)
-        end
-    end
-end
-
 function RemoveTagFrom(handles,tag)
     for i=1, #handles do 
         RemoveTag(handles[i],tag)
     end
 end
 
-function draw()
+function server.init()
+    TrackedProjectiles = {}
+    MinimumVelocity = 20
+    TimeGainMulti = 2
+    SkewerOpenVelocity = 20
+       RaycastDistance = 0.25
+    ShowDebug = false
+       timer = 0
+       cameraTimer = 0
+       trajectoryOrigin = 0
+       projectileHit = 0
+       highestPoint = -1
+       stopFollow = false
+       Proj = FindBody('projectile', false)
+       ProjTrans = GetBodyTransform(Proj)
+       ProjShapes = GetBodyShapes(Proj)
+       for i=1,#ProjShapes do
+           local shape = ProjShapes[i]
+           DrawShapeOutline(shape, 1, 1, 1, 1)
+           SetShapeCollisionFilter(shape, 2, 255-2)
+       end
+       tipvec = locvec('tip')
+       maxdt = tonumber(GetTagValue(Proj - 1, 'maxdt')) or 1
+       dacc = tonumber(GetTagValue(Proj - 1, 'dacc')) or 1
+       homing = tonumber(GetTagValue(Proj - 1, 'homing')) or 0
+       explosive = HasTag(Proj - 1, 'explosive')
+       skewer = HasTag(Proj - 1, 'skewer')
+       gunpowder = HasTag(Proj - 1, 'gunpowder')
+       _drilltime = -1
+       _speedmulti = 1
+       _activated = false
+       _track = {
+           rot = ProjTrans.rot,
+           vel = Vec(0,0,0)
+       }
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        ProjTrans = GetBodyTransform(Proj)
+        local tippos = vectoloc(tipvec).pos
+        local speed = speedAtPos(Proj, tippos)
+        local dir = TransformToParentVec(ProjTrans, {0, 0, -1})
+        local grabbed = (GetPlayerGrabBody(playerId) == Proj)
+        -- Projectile Damage, Drilling, and Destruction System
+        local additionaldist = 0
+        if speed > MinimumVelocity then
+            for k,v in ipairs(ProjShapes) do
+                QueryRejectShape(v)
+            end
+            local rayhit, raydist, rayshape, raynormal = QueryRaycast(tippos, dir, RaycastDistance, 0, false)
+
+            if rayhit then
+                -- Check if this is something that can be broken
+                if true then
+                    if _drilltime == -1 then
+                        _drilltime = 0
+                        _speedmulti = 1
+                        _track.rot = ProjTrans.rot
+                        _track.vel = speedAtPos(Proj, Vec(0,0,0))
+                        additionaldist = raydist
+                    else
+                        _drilltime = _drilltime - (dt * (maxdt * TimeGainMulti))
+                        _drilltime = math.max(_drilltime, 0)
+
+                        _speedmulti = _speedmulti - (dt * dacc)
+                        _speedmulti = math.max(_speedmulti, 0)
+                    end
+                else
+                    _drilltime = -1
+                end
+            end
+        end
+        -- Drilling
+        if _drilltime >= 0 and not _activated then
+            ConstrainVelocity(Proj, 0, tippos, dir, _speedmulti * _track.vel)
+            SetBodyAngularVelocity(Proj, Vec(0,0,0))
+
+            local nograv = VecScale(Vec(0, 1, 0), 10 * dt * 1)
+            local com = GetBodyCenterOfMass(Proj)
+            ApplyBodyImpulse(Proj, com, VecScale(nograv, GetBodyMass(Proj)))
+
+            _drilltime = _drilltime + dt
+
+            if gunpowder and not _activated then
+                for i = 1, 5 do
+                    RemoveTagFrom(FindShapes(),"unbreakable")
+                    Explosion(VecAdd(ProjTrans.pos, rndVec(math.random(0, 2))), 0)
+                end
+            end
+
+            if _drilltime > maxdt then
+                if explosive and not _activated then
+                    -- DebugPrint("Explosive")
+                    RemoveTagFrom(FindShapes(),"unbreakable")
+                    Explosion(tippos, 2.25)
+                    -- RemoveTag('projectile')
+                    -- Delete(Proj - 1)
+                end
+
+                if skewer then
+                    local i = 2
+                    while GetEntityType(Proj + i) == "joint" do
+                        Delete(Proj + i)
+                        i = i + 1
+                    end
+                    -- RemoveTag('projectile')
+                    -- Delete(Proj - 1)
+                end
+
+                _drilltime = -1
+                _activated = true
+            end
+
+        else
+            _drilltime = -1
+        end
+        -- Homing (Points Towards Velocity at higher speeds)
+        if homing > 0 and not _activated and not grabbed then
+            local curvel = GetBodyVelocity(Proj)
+            local ideal = QuatLookAt(Vec(0,0,0), curvel)
+            local impact = logistic(speed, homing, -0.2, 20)
+
+            local slerped = QuatSlerp(ProjTrans.rot, ideal, logistic(speed, 1, -0.6, 20))
+
+            ConstrainOrientation(Proj, 0, ProjTrans.rot, slerped, impact, impact * 1000)
+        end
+        -- skewer Extend
+        if skewer and not grabbed then
+            local i = 2
+            while GetEntityType(Proj + i) == "joint" do
+                local min, max = GetJointLimits(Proj + i)
+                local tar = (_activated or speed > SkewerOpenVelocity) and big(min, max) or small(min, max)
+                SetJointMotorTarget(Proj + i, tar, 8)
+
+                i = i + 1
+            end
+        end
+        -- Grabbing Alignment
+        if grabbed then
+            local Launcher, Distance = FindClosestLauncher()
+
+            if Launcher ~= nil then
+                local LTrans = GetBodyTransform(Launcher)
+
+                -- LOGISTIC EXPLANATION
+                -- https://www.desmos.com/calculator/vwal5m5mbi
+                -- DebugPrint(Distance)
+                local impact = logistic(Distance, 1, 0.5, 6)
+                impact = impact * math.max(0.1, (VecDot(TransformToParentVec(ProjTrans, Vec(0, 0, -1)), TransformToParentVec(LTrans, Vec(0, 0, -1)))))
+                ConstrainOrientation(Proj, 0, ProjTrans.rot, LTrans.rot, impact)
+                -- SetBodyTransform(Proj, Transform(ProjTrans.pos, LTrans.rot))
+
+                NoGrav(Proj, dt)
+            end
+        end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("f1") then ShowDebug = not ShowDebug end
+
+       local tippos = vectoloc(tipvec).pos
+       local speed = speedAtPos(Proj, tippos)
+
+       SetCamera(dt)
+end
+
+function client.draw()
     if _drilltime >= 0 then
         DrawBodyOutline(Proj, 1, 1, 1, 0.1)
     end
@@ -361,17 +337,5 @@
         UiText("Continue Holding 'E' to follow projectile")
         UiPop()
     end
-
-	-- if ShowDebug then
-    --     local tip = vectoloc(tipvec)
-
-    --     local x, y = UiWorldToPixel(tip.pos)
-    --     local speed = Round(speedAtPos(Proj, tip.pos), 0.1)
-
-    --     local c = 1 - (_drilltime / maxdt)
-    --     DrawBodyOutline(Proj, 1 - c, c, 0, 1)
-    --     if _activated then DrawBodyHighlight(Proj, -10, -10, -10, 0.5) end
- 
-    --     UiTooltip(_activated, 1.1, "center", {x, y}, 0.4)
-	-- end
-end+end
+

```
