# Migration Report: evf\EVF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/evf\EVF.lua
+++ patched/evf\EVF.lua
@@ -1,130 +1,4 @@
---script version 5.0.4     https://steamcommunity.com/sharedfiles/filedetails/?id=3009223120
-doorvolume = 0.4
-beep = GetBoolParam("chime")
-trunklift = GetBoolParam("trunklift")
-hoodlift = GetBoolParam("hoodlift")
-sounddir = GetStringParam("sounddir")
-chimevar = GetStringParam("chimevar")
-smoothInteriorLight = GetBoolParam("smoothIntLight")
-function init()
-    doors = FindShapes("door")
-    hood = FindShape("hood")
-    trunk = FindShape("trunk")
-    trunk_down = FindShape("trunk_down")
-    steer = FindShape("steer")
-    spoiler = FindShape("spoiler")
-    intlights = FindShapes("interiorlight")
-    for i = 1, #intlights do
-        SetTag(intlights[i], "interact", "Mode: Active")
-    end
-    vehicle = FindVehicle("vehicle")
-    if not IsHandleValid(vehicle) then
-        vehicle = FindVehicle("vehicle")
-    end
-    vehicle_body = GetVehicleBody(vehicle)
-    vehicle_body_shape = GetBodyShapes(vehicle_body)[1]
-    if sounddir == "" then
-        sounddir = "MOD/EVF/snd"
-    end
-    if chimevar == "" then
-        doorchime = LoadLoop(sounddir .. "/chime1.ogg")
-    else
-        doorchime = LoadLoop(sounddir .. "/chime" .. chimevar .. ".ogg")
-    end
-    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
-    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
-    door_c = LoadSound(sounddir .. "/door_c.ogg")
-    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
-    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
-    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
-    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
-    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
-    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
-    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
-    lightclicksound = LoadSound(sounddir .. "/click.ogg")
-    doorjoint = {}
-    playeddoor = {}
-    playedhood = {}
-    smoothLightValue = 0
-    if vehicle ~= 0 then
-        for i = 1, #doors do
-            local index = 1
-            doorjoint[i] = GetShapeJoints(doors[i])[index]
-            while GetJointOtherShape(doorjoint[i], doors[i]) ~= vehicle_body_shape do
-                index = index + 1
-                doorjoint[i] = GetShapeJoints(doors[i])[index]
-            end
-            playeddoor[i] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(hood) then
-            local index = 1
-            hoodjoint = GetShapeJoints(hood)[index]
-            while GetJointOtherShape(hoodjoint, hood) ~= vehicle_body_shape do
-                index = index + 1
-                hoodjoint = GetShapeJoints(hood)[index]
-            end
-            playedhood[1] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["played3o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(trunk) then
-            local index = 1
-            trunkjoint = GetShapeJoints(trunk)[index]
-            while GetJointOtherShape(trunkjoint, trunk) ~= vehicle_body_shape do
-                index = index + 1
-                trunkjoint = GetShapeJoints(trunk)[index]
-            end
-            playedhood[2] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["played3o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(trunk_down) then
-            local index = 1
-            trunk_down_joint = GetShapeJoints(trunk_down)[index]
-            while GetJointOtherShape(trunk_down_joint, trunk_down) ~= vehicle_body_shape do
-                index = index + 1
-                trunk_down_joint = GetShapeJoints(trunk_down)[index]
-            end
-            playedhood[3] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["played3o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(spoiler) then
-            local index = 1
-            spoilerjoint = GetShapeJoints(spoiler)[index]
-            while GetJointOtherShape(spoilerjoint, spoiler) ~= vehicle_body_shape do
-                index = index + 1
-                spoilerjoint = GetShapeJoints(spoiler)[index]
-            end
-            spmin, spmax = GetJointLimits(spoilerjoint)
-        end
-        if IsHandleValid(steer) then
-            steerjoint = GetShapeJoints(steer)[1]
-        end
-    else 
-        DebugPrint("Vehicle node with tag 'EVF' is not found!")
-    end
-    grabshape = GetPlayerGrabShape()
-    grabbody = GetPlayerGrabBody()
-end
-
+#version 2
 function doorlatchsystem(shape, joint, ID)
     if not IsJointBroken(joint) then
         local jointmovement = GetJointMovement(joint)
@@ -246,26 +120,193 @@
     end
 end
 
-function tick()
-    grabshape = GetPlayerGrabShape()
-    grabbody = GetPlayerGrabBody()
-    for i = 1, #doors do
-        if HasTag(doors[i], "doorlift") then
-            hoodlatchsystem(doors[i], doorjoint[i], i, door_o1, door_c, true, playeddoor, trunk_o2)
-        else
-            doorlatchsystem(doors[i], doorjoint[i], i)
-        end
-    end
-    if IsHandleValid(hood) then
-        hoodlatchsystem(hood, hoodjoint, 1, hood_o, hood_c, hoodlift, playedhood)
-    end
-    if IsHandleValid(trunk) then
-        hoodlatchsystem(trunk, trunkjoint, 2, trunk_o1, trunk_c, trunklift, playedhood, trunk_o2)
-    end
-    if IsHandleValid(trunk_down) then
-        hoodlatchsystem(trunk_down, trunk_down_joint, 3, trunk_o1, trunk_c, false, playedhood, trunk_o2)
-    end
-    if GetPlayerVehicle() == vehicle then
+function server.init()
+    doors = FindShapes("door")
+    hood = FindShape("hood")
+    trunk = FindShape("trunk")
+    trunk_down = FindShape("trunk_down")
+    steer = FindShape("steer")
+    spoiler = FindShape("spoiler")
+    intlights = FindShapes("interiorlight")
+    for i = 1, #intlights do
+        SetTag(intlights[i], "interact", "Mode: Active")
+    end
+    vehicle = FindVehicle("vehicle")
+    if not IsHandleValid(vehicle) then
+        vehicle = FindVehicle("vehicle")
+    end
+    vehicle_body = GetVehicleBody(vehicle)
+    vehicle_body_shape = GetBodyShapes(vehicle_body)[1]
+    if sounddir == "" then
+        sounddir = "MOD/EVF/snd"
+    end
+    if chimevar == "" then
+        doorchime = LoadLoop(sounddir .. "/chime1.ogg")
+    else
+        doorchime = LoadLoop(sounddir .. "/chime" .. chimevar .. ".ogg")
+    end
+    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
+    doorjoint = {}
+    playeddoor = {}
+    playedhood = {}
+    smoothLightValue = 0
+    if vehicle ~= 0 then
+        for i = 1, #doors do
+            local index = 1
+            doorjoint[i] = GetShapeJoints(doors[i])[index]
+            while GetJointOtherShape(doorjoint[i], doors[i]) ~= vehicle_body_shape do
+                index = index + 1
+                doorjoint[i] = GetShapeJoints(doors[i])[index]
+            end
+            playeddoor[i] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(hood) then
+            local index = 1
+            hoodjoint = GetShapeJoints(hood)[index]
+            while GetJointOtherShape(hoodjoint, hood) ~= vehicle_body_shape do
+                index = index + 1
+                hoodjoint = GetShapeJoints(hood)[index]
+            end
+            playedhood[1] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["played3o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(trunk) then
+            local index = 1
+            trunkjoint = GetShapeJoints(trunk)[index]
+            while GetJointOtherShape(trunkjoint, trunk) ~= vehicle_body_shape do
+                index = index + 1
+                trunkjoint = GetShapeJoints(trunk)[index]
+            end
+            playedhood[2] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["played3o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(trunk_down) then
+            local index = 1
+            trunk_down_joint = GetShapeJoints(trunk_down)[index]
+            while GetJointOtherShape(trunk_down_joint, trunk_down) ~= vehicle_body_shape do
+                index = index + 1
+                trunk_down_joint = GetShapeJoints(trunk_down)[index]
+            end
+            playedhood[3] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["played3o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(spoiler) then
+            local index = 1
+            spoilerjoint = GetShapeJoints(spoiler)[index]
+            while GetJointOtherShape(spoilerjoint, spoiler) ~= vehicle_body_shape do
+                index = index + 1
+                spoilerjoint = GetShapeJoints(spoiler)[index]
+            end
+            spmin, spmax = GetJointLimits(spoilerjoint)
+        end
+        if IsHandleValid(steer) then
+            steerjoint = GetShapeJoints(steer)[1]
+        end
+    else 
+        DebugPrint("Vehicle node with tag 'EVF' is not found!")
+    end
+    grabshape = GetPlayerGrabShape(playerId)
+    grabbody = GetPlayerGrabBody(playerId)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        grabshape = GetPlayerGrabShape(playerId)
+        grabbody = GetPlayerGrabBody(playerId)
+        for i = 1, #doors do
+            if HasTag(doors[i], "doorlift") then
+                hoodlatchsystem(doors[i], doorjoint[i], i, door_o1, door_c, true, playeddoor, trunk_o2)
+            else
+                doorlatchsystem(doors[i], doorjoint[i], i)
+            end
+        end
+        if IsHandleValid(hood) then
+            hoodlatchsystem(hood, hoodjoint, 1, hood_o, hood_c, hoodlift, playedhood)
+        end
+        if IsHandleValid(trunk) then
+            hoodlatchsystem(trunk, trunkjoint, 2, trunk_o1, trunk_c, trunklift, playedhood, trunk_o2)
+        end
+        if IsHandleValid(trunk_down) then
+            hoodlatchsystem(trunk_down, trunk_down_joint, 3, trunk_o1, trunk_c, false, playedhood, trunk_o2)
+        end
+        if vehicle ~= 0 then
+            for i = 1, #doors do
+                if playeddoor[i]["open"] and not HasTag(doors[i], "nolight") then
+                    doorsopen = true
+                    break
+                else
+                    doorsopen = false
+                end
+            end
+            if doorsopen then
+                for i = 1, #intlights do
+                    if not lightmodecheck(intlights[i], "Mode: Off") and not IsShapeBroken(intlights[i]) then
+                        if smoothInteriorLight then
+                            SetValue("smoothLightValue", 0.5, "linear", 1)
+                        else
+                            smoothLightValue = 0.5
+                        end
+                        if (smoothLightValue > 0.47) then
+                            smoothLightValue = 0.5
+                        end
+                        SetShapeEmissiveScale(intlights[i], smoothLightValue)
+                    end
+                end
+            else
+                for i = 1, #intlights do
+                    if not lightmodecheck(intlights[i], "Mode: On") then
+                        if smoothInteriorLight then
+                            SetValue("smoothLightValue", 0, "linear", 1)
+                        else
+                            smoothLightValue = 0
+                        end
+                        if (smoothLightValue < 0.03) then
+                            smoothLightValue = 0
+                        end
+                        SetShapeEmissiveScale(intlights[i], smoothLightValue)
+                    end
+                end
+            end
+        end
+    end
+end
+
+function client.init()
+    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
+    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
+    door_c = LoadSound(sounddir .. "/door_c.ogg")
+    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
+    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
+    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
+    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
+    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
+    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
+    lightclicksound = LoadSound(sounddir .. "/click.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerVehicle(playerId) == vehicle then
         local t = GetVehicleTransform(vehicle)
         local vel = TransformToLocalVec(t, GetBodyVelocity(vehicle_body))
         local speed = -vel[3]
@@ -295,7 +336,7 @@
     end
     for i = 1, #intlights do
         if not IsShapeBroken(intlights[i]) then
-            if GetPlayerInteractShape() == intlights[i] and InputPressed("interact") then
+            if GetPlayerInteractShape(playerId) == intlights[i] and InputPressed("interact") then
                 if lightmodecheck(intlights[i], "Mode: Active") then
                     PlaySound(lightclicksound, GetShapeWorldTransform(intlights[i]).pos, 0.5)
                     SetTag(intlights[i], "interact", "Mode: On")
@@ -314,44 +355,5 @@
             SetShapeEmissiveScale(intlights[i], 0)
         end
     end
-
-    if vehicle ~= 0 then
-        for i = 1, #doors do
-            if playeddoor[i]["open"] and not HasTag(doors[i], "nolight") then
-                doorsopen = true
-                break
-            else
-                doorsopen = false
-            end
-        end
-        if doorsopen then
-            for i = 1, #intlights do
-                if not lightmodecheck(intlights[i], "Mode: Off") and not IsShapeBroken(intlights[i]) then
-                    if smoothInteriorLight then
-                        SetValue("smoothLightValue", 0.5, "linear", 1)
-                    else
-                        smoothLightValue = 0.5
-                    end
-                    if (smoothLightValue > 0.47) then
-                        smoothLightValue = 0.5
-                    end
-                    SetShapeEmissiveScale(intlights[i], smoothLightValue)
-                end
-            end
-        else
-            for i = 1, #intlights do
-                if not lightmodecheck(intlights[i], "Mode: On") then
-                    if smoothInteriorLight then
-                        SetValue("smoothLightValue", 0, "linear", 1)
-                    else
-                        smoothLightValue = 0
-                    end
-                    if (smoothLightValue < 0.03) then
-                        smoothLightValue = 0
-                    end
-                    SetShapeEmissiveScale(intlights[i], smoothLightValue)
-                end
-            end
-        end
-    end
-end+end
+

```

---

# Migration Report: evf\EVF2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/evf\EVF2.lua
+++ patched/evf\EVF2.lua
@@ -1,9 +1,4 @@
---script version 3.0.2
-doorvolume = 0.4                                                                --if you reading this, get ready for yanderecode
-beep = GetBoolParam("doornotification")
-trunklift = GetBoolParam("trunklift")
-hoodlift = GetBoolParam("hoodlift")
-sounddir = GetStringParam("sounddir")
+#version 2
 function indexshapes()
     local doors = FindShapes("door")
     d1 = doors[1]
@@ -96,47 +91,12 @@
     }
 end
 
-function init()
-    if sounddir == "" then
-        sounddir = "MOD/EVF/snd"
-    end
-    --airbagsound = LoadSound(sounddir .. "/airbag.ogg")
-    doorbeep = LoadLoop(sounddir .. "/doorbeep.ogg")
-    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
-    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
-    door_c = LoadSound(sounddir .. "/door_c.ogg")
-    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
-    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
-    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
-    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
-    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
-    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
-    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
-    indexshapes()
-    played = {}
-    indexjoints(ho)
-    indexjoints(tr)
-    indexjoints(d1)
-    indexjoints(d2)
-    indexjoints(d3)
-    indexjoints(d4)
-    indexjoints(d5)
-    indexjoints(d6)
-    indexjoints(spoiler)
-    for i = 1, 8 do
-        GenerateSoundTable(i)
-    end
-    --[[indexjoints(ml)
-    indexjoints(mr)]]--
-    indexjoints(steer)
-end
-
 function doorlatchsystem(shape, joint, ID)
     if not IsJointBroken(joint) then
         local a = GetJointMovement(joint)
-        local grabshape = GetPlayerGrabShape()
+        local grabshape = GetPlayerGrabShape(playerId)
         local body1 = GetShapeBody(shape)
-        local grabbody = GetPlayerGrabBody()
+        local grabbody = GetPlayerGrabBody(playerId)
         local pos = GetShapeWorldTransform(shape).pos
         if not IsJointBroken(joint) then
             if grabshape == shape or grabbody == body1 then
@@ -173,9 +133,9 @@
 function hoodlatchsystem(shape, joint, ID, sound_o1, sound_c, lift, sound_o2)
     if not IsJointBroken(joint) then
         local a = GetJointMovement(joint)
-        local grabshape = GetPlayerGrabShape()
+        local grabshape = GetPlayerGrabShape(playerId)
         local body1 = GetShapeBody(shape)
-        local grabbody = GetPlayerGrabBody()
+        local grabbody = GetPlayerGrabBody(playerId)
         local pos = GetShapeWorldTransform(shape).pos
         local min, max = GetJointLimits(joint)
         local b = max / 2 - 15
@@ -236,13 +196,111 @@
     end
 end
 
-function tick()
-    local t = GetVehicleTransform(veh)
-    local vel = TransformToLocalVec(t, GetBodyVelocity(veh_body))
-    local speed = -vel[3]
-    local speedside = -vel[1]
-
-    if GetPlayerVehicle() == veh then
+function server.init()
+    if sounddir == "" then
+        sounddir = "MOD/EVF/snd"
+    end
+    --airbagsound = LoadSound(sounddir .. "/airbag.ogg")
+    doorbeep = LoadLoop(sounddir .. "/doorbeep.ogg")
+    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
+    indexshapes()
+    played = {}
+    indexjoints(ho)
+    indexjoints(tr)
+    indexjoints(d1)
+    indexjoints(d2)
+    indexjoints(d3)
+    indexjoints(d4)
+    indexjoints(d5)
+    indexjoints(d6)
+    indexjoints(spoiler)
+    for i = 1, 8 do
+        GenerateSoundTable(i)
+    end
+    --[[indexjoints(ml)
+    indexjoints(mr)]]--
+    indexjoints(steer)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local t = GetVehicleTransform(veh)
+        local vel = TransformToLocalVec(t, GetBodyVelocity(veh_body))
+        local speed = -vel[3]
+        local speedside = -vel[1]
+        else
+            --[[if IsBodyBroken(veh_body) and not airbag then
+                airbagdeployed = true
+            end]]--
+            SetJointMotorTarget(steer_j, 0, 4.5)
+            SetJointMotorTarget(spoiler_j, spmin, 2)
+        end
+        if d1_valid then
+            if d1lift then
+                hoodlatchsystem(d1,d1_j,1,door_o1, door_c, trunklift, trunk_o2)
+            else
+                doorlatchsystem(d1,d1_j,1)
+            end
+        end
+        if d2_valid then
+            if d2lift then
+                hoodlatchsystem(d2,d2_j,2,door_o1, door_c, trunklift, trunk_o2)
+            else
+                doorlatchsystem(d2,d2_j,2)
+            end
+        end
+        if d3_valid then
+            if d3lift then
+                hoodlatchsystem(d3,d3_j,3,door_o1, door_c, trunklift, trunk_o2)
+            else
+                doorlatchsystem(d3,d3_j,3)
+            end
+        end
+        if d4_valid then
+            if d4lift then
+                hoodlatchsystem(d4,d4_j,4,door_o1, door_c, trunklift, trunk_o2)
+            else
+                doorlatchsystem(d4,d4_j,4)
+            end
+        end
+        if d5_valid then
+            if d5lift then
+                hoodlatchsystem(d5,d5_j,5,door_o1, door_c, trunklift, trunk_o2)
+            else
+                doorlatchsystem(d5,d5_j,5)
+            end
+        end
+        if d6_valid then
+            if d6lift then
+                hoodlatchsystem(d6,d6_j,6,door_o1, door_c, trunklift, trunk_o2)
+            else
+                doorlatchsystem(d6,d6_j,6)
+            end
+        end
+        if ho_valid then
+            hoodlatchsystem(ho,ho_j,7,hood_o, hood_c, hoodlift)
+        end
+        if tr_valid then
+            hoodlatchsystem(tr,tr_j,8,trunk_o1, trunk_c, trunklift, trunk_o2)
+        end
+    end
+end
+
+function client.init()
+    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
+    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
+    door_c = LoadSound(sounddir .. "/door_c.ogg")
+    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
+    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
+    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
+    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
+    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
+    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerVehicle(playerId) == veh then
         if InputDown("left") or InputDown("right") then
             if InputDown("left") then
                 SetJointMotorTarget(steer_j, 130  , 4.5)
@@ -276,59 +334,5 @@
                 airbagdeployed = true
             end
         end]]--
-    else
-        --[[if IsBodyBroken(veh_body) and not airbag then
-            airbagdeployed = true
-        end]]--
-        SetJointMotorTarget(steer_j, 0, 4.5)
-        SetJointMotorTarget(spoiler_j, spmin, 2)
-    end
-    if d1_valid then
-        if d1lift then
-            hoodlatchsystem(d1,d1_j,1,door_o1, door_c, trunklift, trunk_o2)
-        else
-            doorlatchsystem(d1,d1_j,1)
-        end
-    end
-    if d2_valid then
-        if d2lift then
-            hoodlatchsystem(d2,d2_j,2,door_o1, door_c, trunklift, trunk_o2)
-        else
-            doorlatchsystem(d2,d2_j,2)
-        end
-    end
-    if d3_valid then
-        if d3lift then
-            hoodlatchsystem(d3,d3_j,3,door_o1, door_c, trunklift, trunk_o2)
-        else
-            doorlatchsystem(d3,d3_j,3)
-        end
-    end
-    if d4_valid then
-        if d4lift then
-            hoodlatchsystem(d4,d4_j,4,door_o1, door_c, trunklift, trunk_o2)
-        else
-            doorlatchsystem(d4,d4_j,4)
-        end
-    end
-    if d5_valid then
-        if d5lift then
-            hoodlatchsystem(d5,d5_j,5,door_o1, door_c, trunklift, trunk_o2)
-        else
-            doorlatchsystem(d5,d5_j,5)
-        end
-    end
-    if d6_valid then
-        if d6lift then
-            hoodlatchsystem(d6,d6_j,6,door_o1, door_c, trunklift, trunk_o2)
-        else
-            doorlatchsystem(d6,d6_j,6)
-        end
-    end
-    if ho_valid then
-        hoodlatchsystem(ho,ho_j,7,hood_o, hood_c, hoodlift)
-    end
-    if tr_valid then
-        hoodlatchsystem(tr,tr_j,8,trunk_o1, trunk_c, trunklift, trunk_o2)
-    end
-end+end
+

```

---

# Migration Report: evf\EVF3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/evf\EVF3.lua
+++ patched/evf\EVF3.lua
@@ -1,121 +1,4 @@
---script version 5.0.0     https://steamcommunity.com/sharedfiles/filedetails/?id=3009223120
-doorvolume = 0.4
-beep = GetBoolParam("chime")
-trunklift = GetBoolParam("trunklift")
-hoodlift = GetBoolParam("hoodlift")
-sounddir = GetStringParam("sounddir")
-chimevar = GetStringParam("chimevar")
-function init()
-    doors = FindShapes("door")
-    hood = FindShape("hood")
-    trunk = FindShape("trunk")
-    trunk_down = FindShape("trunk_down")
-    steer = FindShape("steer")
-    spoiler = FindShape("spoiler")
-    intlights = FindShapes("interiorlight")
-    for i = 1, #intlights do
-        SetTag(intlights[i], "interact", "Mode: Active")
-    end
-    vehicle = FindVehicle("vehicle")
-    vehicle_body = GetVehicleBody(vehicle)
-    vehicle_body_shape = GetBodyShapes(vehicle_body)[1]
-    if sounddir == "" then
-        sounddir = "MOD/EVF/snd"
-    end
-    if chimevar == "" then
-        doorchime = LoadLoop(sounddir .. "/chime1.ogg")
-    else
-        doorchime = LoadLoop(sounddir .. "/chime" .. chimevar .. ".ogg")
-    end
-    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
-    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
-    door_c = LoadSound(sounddir .. "/door_c.ogg")
-    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
-    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
-    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
-    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
-    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
-    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
-    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
-    lightclicksound = LoadSound(sounddir .. "/click.ogg")
-    doorjoint = {}
-    playeddoor = {}
-    playedhood = {}
-    for i = 1, #doors do
-        local index = 1
-        doorjoint[i] = GetShapeJoints(doors[i])[index]
-        while GetJointOtherShape(doorjoint[i], doors[i]) ~= vehicle_body_shape do
-            index = index + 1
-            doorjoint[i] = GetShapeJoints(doors[i])[index]
-        end
-        playeddoor[i] = {
-            ["played1o"] = false,
-            ["played2o"] = true,
-            ["playedc"] = true,
-            ["open"] = false
-        }
-    end
-    if IsHandleValid(hood) then
-        local index = 1
-        hoodjoint = GetShapeJoints(hood)[index]
-        while GetJointOtherShape(hoodjoint, hood) ~= vehicle_body_shape do
-            index = index + 1
-            hoodjoint = GetShapeJoints(hood)[index]
-        end
-        playedhood[1] = {
-            ["played1o"] = false,
-            ["played2o"] = true,
-            ["played3o"] = true,
-            ["playedc"] = true,
-            ["open"] = false
-        }
-    end
-    if IsHandleValid(trunk) then
-        local index = 1
-        trunkjoint = GetShapeJoints(trunk)[index]
-        while GetJointOtherShape(trunkjoint, trunk) ~= vehicle_body_shape do
-            index = index + 1
-            trunkjoint = GetShapeJoints(trunk)[index]
-        end
-        playedhood[2] = {
-            ["played1o"] = false,
-            ["played2o"] = true,
-            ["played3o"] = true,
-            ["playedc"] = true,
-            ["open"] = false
-        }
-    end
-    if IsHandleValid(trunk_down) then
-        local index = 1
-        trunk_down_joint = GetShapeJoints(trunk_down)[index]
-        while GetJointOtherShape(trunk_down_joint, trunk_down) ~= vehicle_body_shape do
-            index = index + 1
-            trunk_down_joint = GetShapeJoints(trunk_down)[index]
-        end
-        playedhood[3] = {
-            ["played1o"] = false,
-            ["played2o"] = true,
-            ["played3o"] = true,
-            ["playedc"] = true,
-            ["open"] = false
-        }
-    end
-    if IsHandleValid(spoiler) then
-        local index = 1
-        spoilerjoint = GetShapeJoints(spoiler)[index]
-        while GetJointOtherShape(spoilerjoint, spoiler) ~= vehicle_body_shape do
-            index = index + 1
-            spoilerjoint = GetShapeJoints(spoiler)[index]
-        end
-        spmin, spmax = GetJointLimits(spoilerjoint)
-    end
-    if IsHandleValid(steer) then
-        steerjoint = GetShapeJoints(steer)[1]
-    end
-    grabshape = GetPlayerGrabShape()
-    grabbody = GetPlayerGrabBody()
-end
-
+#version 2
 function doorlatchsystem(shape, joint, ID)
     if not IsJointBroken(joint) then
         local jointmovement = GetJointMovement(joint)
@@ -225,26 +108,172 @@
     end
 end
 
-function tick()
-    grabshape = GetPlayerGrabShape()
-    grabbody = GetPlayerGrabBody()
+function server.init()
+    doors = FindShapes("door")
+    hood = FindShape("hood")
+    trunk = FindShape("trunk")
+    trunk_down = FindShape("trunk_down")
+    steer = FindShape("steer")
+    spoiler = FindShape("spoiler")
+    intlights = FindShapes("interiorlight")
+    for i = 1, #intlights do
+        SetTag(intlights[i], "interact", "Mode: Active")
+    end
+    vehicle = FindVehicle("vehicle")
+    vehicle_body = GetVehicleBody(vehicle)
+    vehicle_body_shape = GetBodyShapes(vehicle_body)[1]
+    if sounddir == "" then
+        sounddir = "MOD/EVF/snd"
+    end
+    if chimevar == "" then
+        doorchime = LoadLoop(sounddir .. "/chime1.ogg")
+    else
+        doorchime = LoadLoop(sounddir .. "/chime" .. chimevar .. ".ogg")
+    end
+    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
+    doorjoint = {}
+    playeddoor = {}
+    playedhood = {}
     for i = 1, #doors do
-        if HasTag(doors[i], "doorlift") then
-            hoodlatchsystem(doors[i], doorjoint[i], i, door_o1, door_c, true, playeddoor, trunk_o2)
+        local index = 1
+        doorjoint[i] = GetShapeJoints(doors[i])[index]
+        while GetJointOtherShape(doorjoint[i], doors[i]) ~= vehicle_body_shape do
+            index = index + 1
+            doorjoint[i] = GetShapeJoints(doors[i])[index]
+        end
+        playeddoor[i] = {
+            ["played1o"] = false,
+            ["played2o"] = true,
+            ["playedc"] = true,
+            ["open"] = false
+        }
+    end
+    if IsHandleValid(hood) then
+        local index = 1
+        hoodjoint = GetShapeJoints(hood)[index]
+        while GetJointOtherShape(hoodjoint, hood) ~= vehicle_body_shape do
+            index = index + 1
+            hoodjoint = GetShapeJoints(hood)[index]
+        end
+        playedhood[1] = {
+            ["played1o"] = false,
+            ["played2o"] = true,
+            ["played3o"] = true,
+            ["playedc"] = true,
+            ["open"] = false
+        }
+    end
+    if IsHandleValid(trunk) then
+        local index = 1
+        trunkjoint = GetShapeJoints(trunk)[index]
+        while GetJointOtherShape(trunkjoint, trunk) ~= vehicle_body_shape do
+            index = index + 1
+            trunkjoint = GetShapeJoints(trunk)[index]
+        end
+        playedhood[2] = {
+            ["played1o"] = false,
+            ["played2o"] = true,
+            ["played3o"] = true,
+            ["playedc"] = true,
+            ["open"] = false
+        }
+    end
+    if IsHandleValid(trunk_down) then
+        local index = 1
+        trunk_down_joint = GetShapeJoints(trunk_down)[index]
+        while GetJointOtherShape(trunk_down_joint, trunk_down) ~= vehicle_body_shape do
+            index = index + 1
+            trunk_down_joint = GetShapeJoints(trunk_down)[index]
+        end
+        playedhood[3] = {
+            ["played1o"] = false,
+            ["played2o"] = true,
+            ["played3o"] = true,
+            ["playedc"] = true,
+            ["open"] = false
+        }
+    end
+    if IsHandleValid(spoiler) then
+        local index = 1
+        spoilerjoint = GetShapeJoints(spoiler)[index]
+        while GetJointOtherShape(spoilerjoint, spoiler) ~= vehicle_body_shape do
+            index = index + 1
+            spoilerjoint = GetShapeJoints(spoiler)[index]
+        end
+        spmin, spmax = GetJointLimits(spoilerjoint)
+    end
+    if IsHandleValid(steer) then
+        steerjoint = GetShapeJoints(steer)[1]
+    end
+    grabshape = GetPlayerGrabShape(playerId)
+    grabbody = GetPlayerGrabBody(playerId)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        grabshape = GetPlayerGrabShape(playerId)
+        grabbody = GetPlayerGrabBody(playerId)
+        for i = 1, #doors do
+            if HasTag(doors[i], "doorlift") then
+                hoodlatchsystem(doors[i], doorjoint[i], i, door_o1, door_c, true, playeddoor, trunk_o2)
+            else
+                doorlatchsystem(doors[i], doorjoint[i], i)
+            end
+        end
+        if IsHandleValid(hood) then
+            hoodlatchsystem(hood, hoodjoint, 1, hood_o, hood_c, hoodlift, playedhood)
+        end
+        if IsHandleValid(trunk) then
+            hoodlatchsystem(trunk, trunkjoint, 2, trunk_o1, trunk_c, trunklift, playedhood, trunk_o2)
+        end
+        if IsHandleValid(trunk_down) then
+            hoodlatchsystem(trunk_down, trunk_down_joint, 3, trunk_o1, trunk_c, false, playedhood, trunk_o2)
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for i = 1, #doors do
+            if playeddoor[i]["open"] and not HasTag(doors[i], "nolight") then
+                doorsopen = true
+                break
+            else
+                doorsopen = false
+            end
+        end
+        if doorsopen then
+            for i = 1, #intlights do
+                if not lightmodecheck(intlights[i], "Mode: Off") and not IsShapeBroken(intlights[i]) then
+                    SetShapeEmissiveScale(intlights[i], 0.5)
+                end
+            end
         else
-            doorlatchsystem(doors[i], doorjoint[i], i)
-        end
-    end
-    if IsHandleValid(hood) then
-        hoodlatchsystem(hood, hoodjoint, 1, hood_o, hood_c, hoodlift, playedhood)
-    end
-    if IsHandleValid(trunk) then
-        hoodlatchsystem(trunk, trunkjoint, 2, trunk_o1, trunk_c, trunklift, playedhood, trunk_o2)
-    end
-    if IsHandleValid(trunk_down) then
-        hoodlatchsystem(trunk_down, trunk_down_joint, 3, trunk_o1, trunk_c, false, playedhood, trunk_o2)
-    end
-    if GetPlayerVehicle() == vehicle then
+            for i = 1, #intlights do
+                if not lightmodecheck(intlights[i], "Mode: On") then
+                    SetShapeEmissiveScale(intlights[i], 0)
+                end
+            end
+        end
+    end
+end
+
+function client.init()
+    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
+    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
+    door_c = LoadSound(sounddir .. "/door_c.ogg")
+    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
+    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
+    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
+    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
+    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
+    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
+    lightclicksound = LoadSound(sounddir .. "/click.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerVehicle(playerId) == vehicle then
         local t = GetVehicleTransform(vehicle)
         if IsHandleValid(spoiler) then
             local vel = TransformToLocalVec(t, GetBodyVelocity(vehicle_body))
@@ -274,7 +303,7 @@
     end
     for i = 1, #intlights do
         if not IsShapeBroken(intlights[i]) then
-            if GetPlayerInteractShape() == intlights[i] and InputPressed("interact") then
+            if GetPlayerInteractShape(playerId) == intlights[i] and InputPressed("interact") then
                 if lightmodecheck(intlights[i], "Mode: Active") then
                     PlaySound(lightclicksound, GetShapeWorldTransform(intlights[i]).pos, 0.5)
                     SetTag(intlights[i], "interact", "Mode: On")
@@ -295,26 +324,3 @@
     end
 end
 
-function update()
-    for i = 1, #doors do
-        if playeddoor[i]["open"] and not HasTag(doors[i], "nolight") then
-            doorsopen = true
-            break
-        else
-            doorsopen = false
-        end
-    end
-    if doorsopen then
-        for i = 1, #intlights do
-            if not lightmodecheck(intlights[i], "Mode: Off") and not IsShapeBroken(intlights[i]) then
-                SetShapeEmissiveScale(intlights[i], 0.5)
-            end
-        end
-    else
-        for i = 1, #intlights do
-            if not lightmodecheck(intlights[i], "Mode: On") then
-                SetShapeEmissiveScale(intlights[i], 0)
-            end
-        end
-    end
-end
```

---

# Migration Report: evf\EVF_firetruck.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/evf\EVF_firetruck.lua
+++ patched/evf\EVF_firetruck.lua
@@ -1,16 +1,5 @@
---script version 3.0.2
-doorvolume = 0.4  --if you reading this, get ready for yanderecode
-beep = GetBoolParam("doornotification")
-trunklift = GetBoolParam("trunklift")
-hoodlift = GetBoolParam("hoodlift")
-sounddir = GetStringParam("sounddir")
-
--- Variablen für die Utility-Objekte (maximal 9 Utility-Objekte)
-utility1, utility2, utility3, utility4, utility5, utility6, utility7, utility8, utility9 = nil, nil, nil, nil, nil, nil, nil, nil, nil
-utility1_j, utility2_j, utility3_j, utility4_j, utility5_j, utility6_j, utility7_j, utility8_j, utility9_j = nil, nil, nil, nil, nil, nil, nil, nil, nil
-
--- Hilfsfunktion zum Überprüfen, ob ein Joint validiert ist
-function isValidJoint(joint)
+#version 2
+ction isValidJoint(joint)
     if joint == nil then
         print("Joint is nil!")
         return false
@@ -18,7 +7,9 @@
     return true
 end
 
-function indexshapes()
+f
+
+ction indexshapes()
     -- Türen
     local doors = FindShapes("door")
     if doors[1] then d1 = doors[1] end
@@ -49,7 +40,9 @@
     if #utilities >= 9 then utility9 = utilities[9] end
 end
 
-function indexjoints(shape, ID)
+fu
+
+tion indexjoints(shape, ID)
     local joints = GetShapeJoints(shape)
     if shape == ho then
         ho_j = joints[1]
@@ -97,7 +90,9 @@
     if not isValidJoint(d1_j) then print("Door 1 joint invalid!") end
 end
 
-function GenerateSoundTable(ID)
+fun
+
+ion GenerateSoundTable(ID)
     played[ID] = {
         ["played1o"] = false,
         ["played2o"] = true,
@@ -107,7 +102,9 @@
     }
 end
 
-function init()
+fun
+
+ion init()
     if sounddir == "" then
         sounddir = "MOD/EVF/snd"
     end
@@ -140,17 +137,18 @@
     indexjoints(steer)
 end
 
--- Gemeinsame Funktion für die Handhabung von Türen und Utility-Objekten
-function latchsystem(shape, joint, ID, sound_o1, sound_c, lift, sound_o2)
+-- G
+
+ latchsystem(shape, joint, ID, sound_o1, sound_c, lift, sound_o2)
     if not isValidJoint(joint) then
         print("Joint for " .. shape .. " is invalid!")
         return
     end
     
     local a = GetJointMovement(joint)
-    local grabshape = GetPlayerGrabShape()
+    local grabshape = GetPlayerGrabShape(playerId)
     local body1 = GetShapeBody(shape)
-    local grabbody = GetPlayerGrabBody()
+    local grabbody = GetPlayerGrabBody(playerId)
     local pos = GetShapeWorldTransform(shape).pos
     local min, max = GetJointLimits(joint)
     local b = max / 2 - 15
@@ -185,13 +183,15 @@
     end
 end
 
-function tick()
+functi
+
+ tick()
     local t = GetVehicleTransform(veh)
     local vel = TransformToLocalVec(t, GetBodyVelocity(veh_body))
     local speed = -vel[3]
     local speedside = -vel[1]
 
-    if GetPlayerVehicle() == veh then
+    if GetPlayerVehicle(playerId) == veh then
         if InputDown("left") or InputDown("right") then
             if InputDown("left") then
                 SetJointMotorTarget(steer_j, 130, 4.5)
@@ -273,3 +273,4 @@
         latchsystem(utility9, utility9_j, 17, trunk_o1, trunk_c, trunklift, trunk_o2)
     end
 end
+

```

---

# Migration Report: evf\EVF_prop.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/evf\EVF_prop.lua
+++ patched/evf\EVF_prop.lua
@@ -1,126 +1,4 @@
---script version 5.0.3     https://steamcommunity.com/sharedfiles/filedetails/?id=3009223120
-doorvolume = 0.4
-beep = GetBoolParam("doornotification")
-trunklift = GetBoolParam("trunklift")
-hoodlift = GetBoolParam("hoodlift")
-sounddir = GetStringParam("sounddir")
-chimevar = GetStringParam("chimevar")
-function init()
-    doors = FindShapes("door")
-    hood = FindShape("hood")
-    trunk = FindShape("trunk")
-    trunk_down = FindShape("trunk_down")
-    steer = FindShape("steer")
-    spoiler = FindShape("spoiler")
-    intlights = FindShapes("interiorlight")
-    for i = 1, #intlights do
-        SetTag(intlights[i], "interact", "Mode: Active")
-    end
-    vehicle = FindBody("prop")
-    if not IsHandleValid(vehicle) then
-        vehicle = Find("prop")
-    end
-    vehicle_body = FindBody("propbody")
-    vehicle_body_shape = GetBodyShapes(vehicle_body)[1]
-    if sounddir == "" then
-        sounddir = "MOD/EVF/snd"
-    end
-    if chimevar == "" then
-        doorchime = LoadLoop(sounddir .. "/chime1.ogg")
-    else
-        doorchime = LoadLoop(sounddir .. "/chime" .. chimevar .. ".ogg")
-    end
-    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
-    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
-    door_c = LoadSound(sounddir .. "/door_c.ogg")
-    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
-    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
-    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
-    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
-    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
-    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
-    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
-    lightclicksound = LoadSound(sounddir .. "/click.ogg")
-    doorjoint = {}
-    playeddoor = {}
-    playedhood = {}
-    if vehicle ~= 0 then
-        for i = 1, #doors do
-            local index = 1
-            doorjoint[i] = GetShapeJoints(doors[i])[index]
-            while GetJointOtherShape(doorjoint[i], doors[i]) ~= vehicle_body_shape do
-                index = index + 1
-                doorjoint[i] = GetShapeJoints(doors[i])[index]
-            end
-            playeddoor[i] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(hood) then
-            local index = 1
-            hoodjoint = GetShapeJoints(hood)[index]
-            while GetJointOtherShape(hoodjoint, hood) ~= vehicle_body_shape do
-                index = index + 1
-                hoodjoint = GetShapeJoints(hood)[index]
-            end
-            playedhood[1] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["played3o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(trunk) then
-            local index = 1
-            trunkjoint = GetShapeJoints(trunk)[index]
-            while GetJointOtherShape(trunkjoint, trunk) ~= vehicle_body_shape do
-                index = index + 1
-                trunkjoint = GetShapeJoints(trunk)[index]
-            end
-            playedhood[2] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["played3o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(trunk_down) then
-            local index = 1
-            trunk_down_joint = GetShapeJoints(trunk_down)[index]
-            while GetJointOtherShape(trunk_down_joint, trunk_down) ~= vehicle_body_shape do
-                index = index + 1
-                trunk_down_joint = GetShapeJoints(trunk_down)[index]
-            end
-            playedhood[3] = {
-                ["played1o"] = false,
-                ["played2o"] = true,
-                ["played3o"] = true,
-                ["playedc"] = true,
-                ["open"] = false
-            }
-        end
-        if IsHandleValid(spoiler) then
-            local index = 1
-            spoilerjoint = GetShapeJoints(spoiler)[index]
-            while GetJointOtherShape(spoilerjoint, spoiler) ~= vehicle_body_shape do
-                index = index + 1
-                spoilerjoint = GetShapeJoints(spoiler)[index]
-            end
-            spmin, spmax = GetJointLimits(spoilerjoint)
-        end
-        if IsHandleValid(steer) then
-            steerjoint = GetShapeJoints(steer)[1]
-        end
-    end
-    grabshape = GetPlayerGrabShape()
-    grabbody = GetPlayerGrabBody()
-end
-
+#version 2
 function doorlatchsystem(shape, joint, ID)
     if not IsJointBroken(joint) then
         local jointmovement = GetJointMovement(joint)
@@ -230,26 +108,179 @@
     end
 end
 
-function tick()
-    grabshape = GetPlayerGrabShape()
-    grabbody = GetPlayerGrabBody()
-    for i = 1, #doors do
-        if HasTag(doors[i], "doorlift") then
-            hoodlatchsystem(doors[i], doorjoint[i], i, door_o1, door_c, true, playeddoor, trunk_o2)
-        else
-            doorlatchsystem(doors[i], doorjoint[i], i)
-        end
-    end
-    if IsHandleValid(hood) then
-        hoodlatchsystem(hood, hoodjoint, 1, hood_o, hood_c, hoodlift, playedhood)
-    end
-    if IsHandleValid(trunk) then
-        hoodlatchsystem(trunk, trunkjoint, 2, trunk_o1, trunk_c, trunklift, playedhood, trunk_o2)
-    end
-    if IsHandleValid(trunk_down) then
-        hoodlatchsystem(trunk_down, trunk_down_joint, 3, trunk_o1, trunk_c, false, playedhood, trunk_o2)
-    end
-    if GetPlayerVehicle() == vehicle then
+function server.init()
+    doors = FindShapes("door")
+    hood = FindShape("hood")
+    trunk = FindShape("trunk")
+    trunk_down = FindShape("trunk_down")
+    steer = FindShape("steer")
+    spoiler = FindShape("spoiler")
+    intlights = FindShapes("interiorlight")
+    for i = 1, #intlights do
+        SetTag(intlights[i], "interact", "Mode: Active")
+    end
+    vehicle = FindBody("prop")
+    if not IsHandleValid(vehicle) then
+        vehicle = Find("prop")
+    end
+    vehicle_body = FindBody("propbody")
+    vehicle_body_shape = GetBodyShapes(vehicle_body)[1]
+    if sounddir == "" then
+        sounddir = "MOD/EVF/snd"
+    end
+    if chimevar == "" then
+        doorchime = LoadLoop(sounddir .. "/chime1.ogg")
+    else
+        doorchime = LoadLoop(sounddir .. "/chime" .. chimevar .. ".ogg")
+    end
+    hood_lift_loop = LoadLoop(sounddir .. "/hood_lift_loop.ogg")
+    doorjoint = {}
+    playeddoor = {}
+    playedhood = {}
+    if vehicle ~= 0 then
+        for i = 1, #doors do
+            local index = 1
+            doorjoint[i] = GetShapeJoints(doors[i])[index]
+            while GetJointOtherShape(doorjoint[i], doors[i]) ~= vehicle_body_shape do
+                index = index + 1
+                doorjoint[i] = GetShapeJoints(doors[i])[index]
+            end
+            playeddoor[i] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(hood) then
+            local index = 1
+            hoodjoint = GetShapeJoints(hood)[index]
+            while GetJointOtherShape(hoodjoint, hood) ~= vehicle_body_shape do
+                index = index + 1
+                hoodjoint = GetShapeJoints(hood)[index]
+            end
+            playedhood[1] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["played3o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(trunk) then
+            local index = 1
+            trunkjoint = GetShapeJoints(trunk)[index]
+            while GetJointOtherShape(trunkjoint, trunk) ~= vehicle_body_shape do
+                index = index + 1
+                trunkjoint = GetShapeJoints(trunk)[index]
+            end
+            playedhood[2] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["played3o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(trunk_down) then
+            local index = 1
+            trunk_down_joint = GetShapeJoints(trunk_down)[index]
+            while GetJointOtherShape(trunk_down_joint, trunk_down) ~= vehicle_body_shape do
+                index = index + 1
+                trunk_down_joint = GetShapeJoints(trunk_down)[index]
+            end
+            playedhood[3] = {
+                ["played1o"] = false,
+                ["played2o"] = true,
+                ["played3o"] = true,
+                ["playedc"] = true,
+                ["open"] = false
+            }
+        end
+        if IsHandleValid(spoiler) then
+            local index = 1
+            spoilerjoint = GetShapeJoints(spoiler)[index]
+            while GetJointOtherShape(spoilerjoint, spoiler) ~= vehicle_body_shape do
+                index = index + 1
+                spoilerjoint = GetShapeJoints(spoiler)[index]
+            end
+            spmin, spmax = GetJointLimits(spoilerjoint)
+        end
+        if IsHandleValid(steer) then
+            steerjoint = GetShapeJoints(steer)[1]
+        end
+    end
+    grabshape = GetPlayerGrabShape(playerId)
+    grabbody = GetPlayerGrabBody(playerId)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        grabshape = GetPlayerGrabShape(playerId)
+        grabbody = GetPlayerGrabBody(playerId)
+        for i = 1, #doors do
+            if HasTag(doors[i], "doorlift") then
+                hoodlatchsystem(doors[i], doorjoint[i], i, door_o1, door_c, true, playeddoor, trunk_o2)
+            else
+                doorlatchsystem(doors[i], doorjoint[i], i)
+            end
+        end
+        if IsHandleValid(hood) then
+            hoodlatchsystem(hood, hoodjoint, 1, hood_o, hood_c, hoodlift, playedhood)
+        end
+        if IsHandleValid(trunk) then
+            hoodlatchsystem(trunk, trunkjoint, 2, trunk_o1, trunk_c, trunklift, playedhood, trunk_o2)
+        end
+        if IsHandleValid(trunk_down) then
+            hoodlatchsystem(trunk_down, trunk_down_joint, 3, trunk_o1, trunk_c, false, playedhood, trunk_o2)
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if vehicle ~= 0 then
+            for i = 1, #doors do
+                if playeddoor[i]["open"] and not HasTag(doors[i], "nolight") then
+                    doorsopen = true
+                    break
+                else
+                    doorsopen = false
+                end
+            end
+            if doorsopen then
+                for i = 1, #intlights do
+                    if not lightmodecheck(intlights[i], "Mode: Off") and not IsShapeBroken(intlights[i]) then
+                        SetShapeEmissiveScale(intlights[i], 0.5)
+                    end
+                end
+            else
+                for i = 1, #intlights do
+                    if not lightmodecheck(intlights[i], "Mode: On") then
+                        SetShapeEmissiveScale(intlights[i], 0)
+                    end
+                end
+            end
+        end
+    end
+end
+
+function client.init()
+    door_o1 = LoadSound(sounddir .. "/door_o1.ogg")
+    door_o2 = LoadSound(sounddir .. "/door_o2.ogg")
+    door_c = LoadSound(sounddir .. "/door_c.ogg")
+    hood_o = LoadSound(sounddir .. "/hood_o.ogg")
+    hood_o1 = LoadSound(sounddir .. "/hood_o1.ogg")
+    hood_c = LoadSound(sounddir .. "/hood_c.ogg")
+    trunk_o1 = LoadSound(sounddir .. "/trunk_o1.ogg")
+    trunk_o2 = LoadSound(sounddir .. "/trunk_o2.ogg")
+    trunk_c = LoadSound(sounddir .. "/trunk_c.ogg")
+    lightclicksound = LoadSound(sounddir .. "/click.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerVehicle(playerId) == vehicle then
         local t = GetVehicleTransform(vehicle)
         if IsHandleValid(spoiler) then
             local vel = TransformToLocalVec(t, GetBodyVelocity(vehicle_body))
@@ -279,7 +310,7 @@
     end
     for i = 1, #intlights do
         if not IsShapeBroken(intlights[i]) then
-            if GetPlayerInteractShape() == intlights[i] and InputPressed("interact") then
+            if GetPlayerInteractShape(playerId) == intlights[i] and InputPressed("interact") then
                 if lightmodecheck(intlights[i], "Mode: Active") then
                     PlaySound(lightclicksound, GetShapeWorldTransform(intlights[i]).pos, 0.5)
                     SetTag(intlights[i], "interact", "Mode: On")
@@ -300,28 +331,3 @@
     end
 end
 
-function update()
-    if vehicle ~= 0 then
-        for i = 1, #doors do
-            if playeddoor[i]["open"] and not HasTag(doors[i], "nolight") then
-                doorsopen = true
-                break
-            else
-                doorsopen = false
-            end
-        end
-        if doorsopen then
-            for i = 1, #intlights do
-                if not lightmodecheck(intlights[i], "Mode: Off") and not IsShapeBroken(intlights[i]) then
-                    SetShapeEmissiveScale(intlights[i], 0.5)
-                end
-            end
-        else
-            for i = 1, #intlights do
-                if not lightmodecheck(intlights[i], "Mode: On") then
-                    SetShapeEmissiveScale(intlights[i], 0)
-                end
-            end
-        end
-    end
-end
```

---

# Migration Report: example.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/example.lua
+++ patched/example.lua
@@ -1,16 +1 @@
-test = "Test"
-if test == "Test" then
-    DebugPrint("Test")
-end
-
-list = [1,2,3,4]
-for i=1,#list do
-    DebugPrint("List")
-end
-
--- Test
-
-DebugPrint("Printings")
-
-DebugPrint("Print")
-
+#version 2

```

---

# Migration Report: lightscript.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lightscript.lua
+++ patched/lightscript.lua
@@ -1,215 +1,205 @@
-function init()
-	switch = FindShape("switch")
-	lights = FindShapes("blink")
-	SetTag(switch, "interact", "Attach")
-	jointlocation = FindShape("jointlocation")
-	attached = false
-	check = true
-	frame = FindShape("frame")
-	vehiclefound = false
-	isplayerinvehicle = false
-	psiren = false
-	plights = false
-	sound = GetStringParam("sound")
-	loop = LoadLoop("MOD/snd/siren.ogg")
-	checkvehicle = true
-	jointedvehicle = 0
-	attachsound = LoadSound("MOD/snd/caseopen.ogg")
-	detachsound = LoadSound("MOD/snd/closecase.ogg")
-	attachedtovehicle = false 
-
-end
-
-function draw()
-	if attached == true and GetPlayerVehicle() == jointedvehicle and GetPlayerVehicle() ~=0 then
-		local info = {}
-		info[#info+1] = {"F", "Siren"}
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 250, h, 6, 6)
-			UiTranslate(100, 32)
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
-		local transform = GetShapeWorldTransform(frame)
-		local lastvehicleposition = transform
-			if psiren == true then 
-				PlayLoop(loop, transform.pos, 1.0)
-			end
-		if pLights == true then
-			for i=1, #lights do
-				local l = lights[i]
-				local p = tonumber(GetTagValue(l, "blink"))
-				if p then
-					local s = math.sin((GetTime()+i) * p)
-					SetShapeEmissiveScale(l, s > 0 and 1 or 0)
-				end
-			end
-		else
-			for i=1, #lights do
-				SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
-			end
-		end
-	end
-end
-
-
-function tick()
-	if attached == false then 
-		for i=1, #lights do
-			SetShapeEmissiveScale(lights[i], 0)
-			jointedvehicle = 0
-		end
-	end
-	if GetPlayerVehicle() == 0 then 
-		pLights = false
-		psiren = false 
-		for i=1, #lights do
-			SetShapeEmissiveScale(lights[i], 0)
-		end
-	end
-	--DebugWatch("siren", psiren)
-	--DebugWatch("lights", plights)
-	pos = GetShapeWorldTransform(jointlocation).pos
-	--DebugWatch("attached", attached)
-	currentshape = GetPlayerInteractShape()
-	if currentshape == switch and InputPressed("interact") then
-		--DebugPrint("Manmoth")
-		if attached == false then
-			Spawn("MOD/joint.xml", Transform(pos), true, true)
-			--DebugPrint("moth")
-			check=false 
-			attached = true
-			
-			checkjoint = FindJoint("vehiclejoint")
-			jointshapes = GetJointShapes(checkjoint)
-			
-			for i=1, #jointshapes do
-				bodycheck = GetShapeBody(jointshapes[i])
-				vehiclecheck = GetBodyVehicle(bodycheck)
-					if vehiclecheck ~= 0 then
-						--DebugPrint("vehiclecheck true")
-						attachedtovehicle = true
-						RemoveTag(switch, "interact", "Attach")
-						SetTag(switch, "interact", "Detach")
-						PlaySound(attachsound)
-					end
-			end
-			if attachedtovehicle == false then
-				Delete(checkjoint)
-				check=true
-				attached = false
-			end
-			
-			
-			
-			
-			
-			
-			
-			
-			
-			
-			
-
-		end
-		if attached == true and check == true then 
-			vehiclejoint = FindJoint("vehiclejoint")
-			Delete(vehiclejoint)
-			attached = false
-			pLights = false
-			psiren = false
-			--DebugPrint("deletejoint")
-			RemoveTag(switch, "interact", "Detach")
-			SetTag(switch, "interact", "Attach")
-			PlaySound(detachsound)
-			attachedtovehicle = false
-		end
-	end
-	--DebugWatch("howmany", howmany)
-	check = true
-	--^^^^ ATTACH AND REATTACH THE SHAPE 
-	
-	
-	currentvehicle = GetPlayerVehicle()
-	vehiclebody = GetVehicleBody(currentvehicle)
-	vehicleshapes = GetBodyShapes(vehiclebody)
-	checkjoint = FindJoint("vehiclejoint")
-	jointshapes = GetJointShapes(checkjoint)
-	
-	for i=1, #vehicleshapes do
-		for b=1, #jointshapes do 
-			if jointshapes[b] == vehicleshapes[i] then
-				isplayerinvehicle = true
-				--DebugPrint("PLAYER IS IN THE RIGHT VEHICLE")
-				--DebugWatch("isplayerinvehicle", isplayerinvehicle)
-				jointedvehicle = GetPlayerVehicle()
-				--DebugWatch("jointed vehicle", jointedvehicle)
-				checkvehicle = false
-			end
-		end
-	end
-	
-	if checkvehicle == true then 
-		for i=1, #vehicleshapes do
-			for b=1, #jointshapes do 
-				if jointshapes[b] == vehicleshapes[i] then
-					isplayerinvehicle = true
-					--DebugPrint("PLAYER IS IN THE RIGHT VEHICLE")
-					--DebugWatch("isplayerinvehicle", isplayerinvehicle)
-					jointedvehicle = GetPlayerVehicle()
-					--DebugWatch("jointed vehicle", jointedvehicle)
-					checkvehicle = false
-				end
-			end
-		end
-	end
-	--DebugWatch("playervehicle", currentvehicle)
-	--DebugWatch("in vehicle?", isplayerinvehicle)
-	
-
-	if InputPressed("f") then
-	if pLights == false then
-		pLights = true
-		psiren = true
-	else
-		pLights = false
-		psiren = false
-	end
-		--if psiren == false then
-			--psiren = true 
-		--else 
-			--psiren = false 
-		--end
-	end
-	--if InputPressed("g") then
-		 --if psiren == false then
-			--psiren = true
-		--else
-		--psiren = false
-		--end
-	--end
-
-	--if GetPlayerVehicle() == 0 then
-		--isplayerinvehicle = false
-	--end
-	if attached == false then 
-		checkvehicle = true 
-	end
-	
-end+#version 2
+function server.init()
+    switch = FindShape("switch")
+    lights = FindShapes("blink")
+    SetTag(switch, "interact", "Attach")
+    jointlocation = FindShape("jointlocation")
+    attached = false
+    check = true
+    frame = FindShape("frame")
+    vehiclefound = false
+    isplayerinvehicle = false
+    psiren = false
+    plights = false
+    sound = GetStringParam("sound")
+    loop = LoadLoop("MOD/snd/siren.ogg")
+    checkvehicle = true
+    jointedvehicle = 0
+    attachedtovehicle = false 
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if attached == false then 
+        	for i=1, #lights do
+        		SetShapeEmissiveScale(lights[i], 0)
+        		jointedvehicle = 0
+        	end
+        end
+        if GetPlayerVehicle(playerId) == 0 then 
+        	pLights = false
+        	psiren = false 
+        	for i=1, #lights do
+        		SetShapeEmissiveScale(lights[i], 0)
+        	end
+        end
+        --DebugWatch("siren", psiren)
+        --DebugWatch("lights", plights)
+        pos = GetShapeWorldTransform(jointlocation).pos
+        --DebugWatch("attached", attached)
+        currentshape = GetPlayerInteractShape(playerId)
+        --DebugWatch("howmany", howmany)
+        check = true
+        --^^^^ ATTACH AND REATTACH THE SHAPE 
+        currentvehicle = GetPlayerVehicle(playerId)
+        vehiclebody = GetVehicleBody(currentvehicle)
+        vehicleshapes = GetBodyShapes(vehiclebody)
+        checkjoint = FindJoint("vehiclejoint")
+        jointshapes = GetJointShapes(checkjoint)
+        for i=1, #vehicleshapes do
+        	for b=1, #jointshapes do 
+        		if jointshapes[b] == vehicleshapes[i] then
+        			isplayerinvehicle = true
+        			--DebugPrint("PLAYER IS IN THE RIGHT VEHICLE")
+        			--DebugWatch("isplayerinvehicle", isplayerinvehicle)
+        			jointedvehicle = GetPlayerVehicle(playerId)
+        			--DebugWatch("jointed vehicle", jointedvehicle)
+        			checkvehicle = false
+        		end
+        	end
+        end
+        if checkvehicle == true then 
+        	for i=1, #vehicleshapes do
+        		for b=1, #jointshapes do 
+        			if jointshapes[b] == vehicleshapes[i] then
+        				isplayerinvehicle = true
+        				--DebugPrint("PLAYER IS IN THE RIGHT VEHICLE")
+        				--DebugWatch("isplayerinvehicle", isplayerinvehicle)
+        				jointedvehicle = GetPlayerVehicle(playerId)
+        				--DebugWatch("jointed vehicle", jointedvehicle)
+        				checkvehicle = false
+        			end
+        		end
+        	end
+        end
+        --DebugWatch("playervehicle", currentvehicle)
+        --DebugWatch("in vehicle?", isplayerinvehicle)
+        --if InputPressed("g") then
+        	 --if psiren == false then
+        		--psiren = true
+        	--else
+        	--psiren = false
+        	--end
+        --end
+        --if GetPlayerVehicle(playerId) == 0 then
+        	--isplayerinvehicle = false
+        --end
+        if attached == false then 
+        	checkvehicle = true 
+        end
+    end
+end
+
+function client.init()
+    attachsound = LoadSound("MOD/snd/caseopen.ogg")
+    detachsound = LoadSound("MOD/snd/closecase.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if currentshape == switch and InputPressed("interact") then
+    	--DebugPrint("Manmoth")
+    	if attached == false then
+    		Spawn("MOD/joint.xml", Transform(pos), true, true)
+    		--DebugPrint("moth")
+    		check=false 
+    		attached = true
+
+    		checkjoint = FindJoint("vehiclejoint")
+    		jointshapes = GetJointShapes(checkjoint)
+
+    		for i=1, #jointshapes do
+    			bodycheck = GetShapeBody(jointshapes[i])
+    			vehiclecheck = GetBodyVehicle(bodycheck)
+    				if vehiclecheck ~= 0 then
+    					--DebugPrint("vehiclecheck true")
+    					attachedtovehicle = true
+    					RemoveTag(switch, "interact", "Attach")
+    					SetTag(switch, "interact", "Detach")
+    					PlaySound(attachsound)
+    				end
+    		end
+    		if attachedtovehicle == false then
+    			Delete(checkjoint)
+    			check=true
+    			attached = false
+    		end
+
+    	end
+    	if attached == true and check == true then 
+    		vehiclejoint = FindJoint("vehiclejoint")
+    		Delete(vehiclejoint)
+    		attached = false
+    		pLights = false
+    		psiren = false
+    		--DebugPrint("deletejoint")
+    		RemoveTag(switch, "interact", "Detach")
+    		SetTag(switch, "interact", "Attach")
+    		PlaySound(detachsound)
+    		attachedtovehicle = false
+    	end
+    end
+    if InputPressed("f") then
+    if pLights == false then
+    	pLights = true
+    	psiren = true
+    else
+    	pLights = false
+    	psiren = false
+    end
+    	--if psiren == false then
+    		--psiren = true 
+    	--else 
+    		--psiren = false 
+    	--end
+    end
+end
+
+function client.draw()
+    if attached == true and GetPlayerVehicle(playerId) == jointedvehicle and GetPlayerVehicle(playerId) ~=0 then
+    	local info = {}
+    	info[#info+1] = {"F", "Siren"}
+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 250, h, 6, 6)
+    		UiTranslate(100, 32)
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
+    	local transform = GetShapeWorldTransform(frame)
+    	local lastvehicleposition = transform
+    		if psiren == true then 
+    			PlayLoop(loop, transform.pos, 1.0)
+    		end
+    	if pLights == true then
+    		for i=1, #lights do
+    			local l = lights[i]
+    			local p = tonumber(GetTagValue(l, "blink"))
+    			if p then
+    				local s = math.sin((GetTime()+i) * p)
+    				SetShapeEmissiveScale(l, s > 0 and 1 or 0)
+    			end
+    		end
+    	else
+    		for i=1, #lights do
+    			SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: main\script\heightmap.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\script\heightmap.lua
+++ patched/main\script\heightmap.lua
@@ -1,42 +1,29 @@
-file = GetString("file", "")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
+    matDirt1 = CreateMaterial("dirt", 0.10, 0.08, 0.08, 1, 0, 0)
+    matGrass1 = CreateMaterial("unphysical", 0.3, 0.30, 0.12, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.2, 0.28, 0.10, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.1, 0.1, 0.1, 1, 0, 0.05)
+    matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("masonry", 0.40, 0.38, 0.0, 1, 0, 0.6)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h do
+    	local y1 = y0 + maxSize
+    	if y1 > h then y1 = h end
 
-function init()
-	-- Must be mounted into a voxscript!!
-	
-	-- The lines below set material and colors, as well as pbr settings, for the heightmap.
-	-- The formula is as follows:
-	-- handle = CreateMaterial("material", r, g, b, [alpha], [reflect], [siny], [metal], [emissive]) | square bracket values are optional.
-	
-	
-	matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
-	matDirt1 = CreateMaterial("dirt", 0.10, 0.08, 0.08, 1, 0, 0)
-	matGrass1 = CreateMaterial("unphysical", 0.3, 0.30, 0.12, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.2, 0.28, 0.10, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.1, 0.1, 0.1, 1, 0, 0.05)
-	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("masonry", 0.40, 0.38, 0.0, 1, 0, 0.6)
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

# Migration Report: main\script\lightswitch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\script\lightswitch.lua
+++ patched/main\script\lightswitch.lua
@@ -1,4 +1,5 @@
-function init()
+#version 2
+function server.init()
     light_switch = FindShape("light_switch")
     lights = FindLights("switchlight")
     LIT = false
@@ -7,16 +8,23 @@
     end
 end
 
-function tick()
-    if LIT then
-        SetTag(light_switch, "interact", "Off")
-    else
-        SetTag(light_switch, "interact", "On")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if LIT then
+            SetTag(light_switch, "interact", "Off")
+        else
+            SetTag(light_switch, "interact", "On")
+        end
+        for i=1, #lights do
+            SetLightEnabled(lights[i], LIT)
+        end
     end
-    if GetPlayerInteractShape() == light_switch and InputPressed("interact") then
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == light_switch and InputPressed("interact") then
         LIT = not LIT
     end
-    for i=1, #lights do
-        SetLightEnabled(lights[i], LIT)
-    end
-end+end
+

```

---

# Migration Report: main\script\sectionalGate.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\script\sectionalGate.lua
+++ patched/main\script\sectionalGate.lua
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

# Migration Report: main\script\sectionalGateControl.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\script\sectionalGateControl.lua
+++ patched/main\script\sectionalGateControl.lua
@@ -1,88 +1,10 @@
-
--- This is a sample script demostrating how to control garage door with external scripts.
--- You may modify this script as your wish.
-
-function init()
-	openShape = FindShape("open")
-	closeShape = FindShape("close")
-	stopShape = FindShape("stop")
-	checkTriggers = FindTriggers("enterCheck")
-	SetTag(openShape, "interact", "Open")
-	SetTag(closeShape, "interact", "Close")
-	SetTag(stopShape, "interact", "Stop")
-	toggle = GetBoolParam("open", false)
-	triggerToggle = toggle
-	inTimer = 0
-	maxTimer = 2
-	overflow = false
-	showInfo = false
-
-	ctrlUnit = FindShape("gateCtrl") -- this is the control unit for garage door, setting tag values would open/close door
-	SetTag(ctrlUnit, "gateCtrl", toggle and "open" or toggle == false and "close" or 0) -- "open" for open, "close" for close, all other values for stopped
-end
-
-function tick(dt)
-	showInfo = false
-	if InputPressed("interact") then
-		if GetPlayerInteractShape() == closeShape then toggle = false end
-		if GetPlayerInteractShape() == openShape then toggle = true end
-		if GetPlayerInteractShape() == stopShape then toggle = nil end
-		if toggle ~= nil then triggerToggle = toggle end
-
-		SetTag(ctrlUnit, "gateCtrl", toggle and "open" or toggle == false and "close" or 0)
-	end
-	local cond1 = false
-	local cond2 = InputDown("handbrake")
-	for i=1, #checkTriggers do
-		cond1 = cond1 or IsVehicleInTrigger(checkTriggers[i], GetPlayerVehicle())
-	end
-	if cond1 and cond2 then
-		showInfo = not overflow
-		inTimer = inTimer+dt
-		if inTimer > maxTimer and not overflow then
-			triggerToggle = not triggerToggle
-			toggle = triggerToggle
-			overflow = true
-
-			SetTag(ctrlUnit, "gateCtrl", toggle and "open" or toggle == false and "close" or 0)
-		end
-	elseif cond1 or cond2 then
-		inTimer = 0
-	else
-		inTimer = 0
-		overflow = false
-	end
-	SetShapeEmissiveScale(openShape, toggle and 1 or 0)
-	SetShapeEmissiveScale(closeShape, toggle == false and 1 or 0)
-	SetShapeEmissiveScale(stopShape, toggle == nil and 1 or 0)
-	local tagValue = GetTagValue(ctrlUnit, "gateCtrl")
-	if tagValue == "open" then toggle = true
-	elseif tagValue == "close" then toggle = false
-	else toggle = nil end
-	if toggle ~= nil then triggerToggle = toggle end
-end
-
-function draw()
-	if not showInfo then return end
-	UiPush()
-		UiFont("bold.ttf", 22)
-		UiTranslate(UiCenter(), UiHeight()-90)
-		UiTranslate(-100, 0)
-		progressBar(200, 20, inTimer/maxTimer)
-		UiColor(1,1,1)
-		UiTranslate(100, -12)
-		UiAlign("center middle")
-		UiTextOutline(0.2, 0.2, 0.2, 0.75, 0.5)
-		UiText(triggerToggle and "Close Gate" or "Open Gate")
-	UiPop()
-end
-
+#version 2
 function progressBar(w, h, t)
 	UiPush()
 		UiAlign("left top")
 		UiColor(0, 0, 0, 0.5)
 		UiImageBox("ui/common/box-solid-10.png", w, h, 6, 6)
-		if t > 0 then
+		if t ~= 0 then
 			UiTranslate(2, 2)
 			w = (w-4)*t
 			if w < 12 then w = 12 end
@@ -91,4 +13,85 @@
 			UiImageBox("ui/common/box-solid-6.png", w, h, 6, 6)
 		end
 	UiPop()
-end+end
+
+function server.init()
+    openShape = FindShape("open")
+    closeShape = FindShape("close")
+    stopShape = FindShape("stop")
+    checkTriggers = FindTriggers("enterCheck")
+    SetTag(openShape, "interact", "Open")
+    SetTag(closeShape, "interact", "Close")
+    SetTag(stopShape, "interact", "Stop")
+    toggle = GetBoolParam("open", false)
+    triggerToggle = toggle
+    inTimer = 0
+    maxTimer = 2
+    overflow = false
+    showInfo = false
+    ctrlUnit = FindShape("gateCtrl") -- this is the control unit for garage door, setting tag values would open/close door
+    SetTag(ctrlUnit, "gateCtrl", toggle and "open" or toggle == false and "close" or 0) -- "open" for open, "close" for close, all other values for stopped
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        showInfo = false
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("interact") then
+    	if GetPlayerInteractShape(playerId) == closeShape then toggle = false end
+    	if GetPlayerInteractShape(playerId) == openShape then toggle = true end
+    	if GetPlayerInteractShape(playerId) == stopShape then toggle = nil end
+    	if toggle ~= nil then triggerToggle = toggle end
+
+    	SetTag(ctrlUnit, "gateCtrl", toggle and "open" or toggle == false and "close" or 0)
+    end
+    local cond1 = false
+    local cond2 = InputDown("handbrake")
+    for i=1, #checkTriggers do
+    	cond1 = cond1 or IsVehicleInTrigger(checkTriggers[i], GetPlayerVehicle(playerId))
+    end
+    if cond1 and cond2 then
+    	showInfo = not overflow
+    	inTimer = inTimer+dt
+    	if inTimer > maxTimer and not overflow then
+    		triggerToggle = not triggerToggle
+    		toggle = triggerToggle
+    		overflow = true
+
+    		SetTag(ctrlUnit, "gateCtrl", toggle and "open" or toggle == false and "close" or 0)
+    	end
+    elseif cond1 or cond2 then
+    	inTimer = 0
+    else
+    	inTimer = 0
+    	overflow = false
+    end
+    SetShapeEmissiveScale(openShape, toggle and 1 or 0)
+    SetShapeEmissiveScale(closeShape, toggle == false and 1 or 0)
+    SetShapeEmissiveScale(stopShape, toggle == nil and 1 or 0)
+    local tagValue = GetTagValue(ctrlUnit, "gateCtrl")
+    if tagValue == "open" then toggle = true
+    elseif tagValue == "close" then toggle = false
+    else toggle = nil end
+    if toggle ~= nil then triggerToggle = toggle end
+end
+
+function client.draw()
+    if not showInfo then return end
+    UiPush()
+    	UiFont("bold.ttf", 22)
+    	UiTranslate(UiCenter(), UiHeight()-90)
+    	UiTranslate(-100, 0)
+    	progressBar(200, 20, inTimer/maxTimer)
+    	UiColor(1,1,1)
+    	UiTranslate(100, -12)
+    	UiAlign("center middle")
+    	UiTextOutline(0.2, 0.2, 0.2, 0.75, 0.5)
+    	UiText(triggerToggle and "Close Gate" or "Open Gate")
+    UiPop()
+end
+

```

---

# Migration Report: main\script\sectionalGateVoxscript.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\script\sectionalGateVoxscript.lua
+++ patched/main\script\sectionalGateVoxscript.lua
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

# Migration Report: options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/options.lua
+++ patched/options.lua
@@ -1,14 +1,4 @@
-#include "slf/keybinds.lua"
-function init()
-    initialize_keybinds()
-    -- Button list
-    buttons = keybinds
-    for i=1, #buttons do
-        buttons[i].waiting = false
-    end
-end
--- Format for keys: IEV.keys.[type].*
-
+#version 2
 function drawKeybindButton(btn, width, height, border_width, padding)
     -- Default values
     if width == nil then width = 100 end
@@ -55,8 +45,8 @@
     if v.waiting then
         local keybind = InputLastPressedKey()
         if keybind ~= "" then
-            SetString(v.key,keybind)
-            --SetString(r, keybind)
+            SetString(v.key,keybind, true)
+            --SetString(r, keybind, true)
             v.waiting = false
         end
     end
@@ -65,7 +55,7 @@
 function resetKeybinds()
     for i=1, #buttons do
         local v = buttons[i]
-        SetString(v.key,v.default)
+        SetString(v.key,v.default, true)
     end
     DebugPrint("Keybind reset to default")
 end
@@ -101,7 +91,16 @@
     UiTranslate(-(border_width+padding), -(border_width+padding))
 end
 
-function draw()
+function server.init()
+    initialize_keybinds()
+    -- Button list
+    buttons = keybinds
+    for i=1, #buttons do
+        buttons[i].waiting = false
+    end
+end
+
+function client.draw()
     UiColor(1,1,1)
     UiAlign("top left")
     UiFont("regular.ttf",24)
@@ -130,4 +129,5 @@
         UiPop()
         ypos = ypos + 1
     end
-end+end
+

```

---

# Migration Report: props\script\attachable_light.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/props\script\attachable_light.lua
+++ patched/props\script\attachable_light.lua
@@ -1,3 +1,4 @@
+#version 2
 function split(input, separator)
     if separator == nil then
         separator = "%s"
@@ -9,7 +10,7 @@
     return result
 end
 
-function init()
+function server.init()
     lightshapes = FindShapes("blink")
     jointshape = FindShape("jointshape")
     jointbody = FindBody("jointbody")
@@ -20,136 +21,138 @@
     active = false
 end
 
-function tick()
-    if GetPlayerInteractShape() == jointshape and InputPressed("interact") then
-        attached = not attached
-    end
-    joint = FindJoints("spawnjoint")
-    if attached then
-        -- Set Tag to Detach when attached
-        SetTag(jointshape, "interact", "Detach")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        joint = FindJoints("spawnjoint")
+        if attached then
+            -- Set Tag to Detach when attached
+            SetTag(jointshape, "interact", "Detach")
 
-        -- Check if joint exists and spawn new one if false
-        if #joint == 0 then
-            Spawn("MOD/props/assets/misc/joint-1.xml", GetShapeWorldTransform(jointshape), false, true)
+            -- Check if joint exists and spawn new one if false
+            if #joint == 0 then
+                Spawn("MOD/props/assets/misc/joint-1.xml", GetShapeWorldTransform(jointshape), false, true)
+            end
+        else
+            SetTag(jointshape, "interact", "Attach")
+            if #joint ~= 0 then
+                for i=1, #joint do
+                    Delete(joint[i])
+                end
+            end
         end
-    else
-        SetTag(jointshape, "interact", "Attach")
-        if #joint ~= 0 then
-            for i=1, #joint do
-                Delete(joint[i])
+        joint = FindJoints("spawnjoint")
+        -- Get jointed bodies and check for one with a vehicle -> get jointedbody, jointedvehicle, check=true
+        jointbodies = GetJointedBodies(jointbody)
+        check = false
+        if #jointbodies >= 1 then
+            for i=1, #jointbodies do
+                if GetBodyVehicle(jointbodies[i]) ~= 0 then
+                    jointedbody = jointbodies[i]
+                    jointedvehicle = GetBodyVehicle(jointbodies[i])
+                    check = true
+                end
+            end
+        end
+        if not check then
+            attached = false
+        end
+        if (not attached) then
+            active = false
+        end
+        if active then
+            for i = 1, #lightshapes, 2 do
+                local l1 = lightshapes[i]
+                local l2 = lightshapes[i + 1]
+
+                if l1 then
+                    local bp1Str = GetTagValue(l1, "blink") or "2,0.075,0.15,0.1,1"
+                    local bp2Str = l2 and GetTagValue(l2, "blink") or "2,0.075,0.15,0.1,1"
+
+                    local bp1 = split(bp1Str, ",")
+                    local bp2 = split(bp2Str, ",")
+
+                    for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
+                    for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
+
+                    local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
+                    local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
+
+                    local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
+                    local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
+
+                    local t = GetTime() + (i * 0.05)
+                    local cD = math.max(cD1, cD2)
+                    local c = t % cD
+
+                    local s1, s2 = 0, 0
+
+                    if simultaneous1 == 1 and simultaneous2 == 1 then
+                        for j = 0, fC1 - 1 do
+                            local fS1 = j * (fD1 + pB1)
+                            if c >= fS1 and c < (fS1 + fD1) then
+                                s1 = 1
+                            end
+                        end
+
+                        for j = 0, fC2 - 1 do
+                            local fS2 = j * (fD2 + pB2)
+                            if c >= fS2 and c < (fS2 + fD2) then
+                                s2 = 1
+                            end
+                        end
+                    else
+                        for j = 0, fC1 - 1 do
+                            local fS1 = j * (fD1 + pB1)
+                            if c >= fS1 and c < (fS1 + fD1) then
+                                s1 = 1
+                            end
+                        end
+
+                        for j = 0, fC2 - 1 do
+                            local fS2 = (j * (fD2 + pB2)) + (cD / 2)
+                            if c >= fS2 and c < (fS2 + fD2) then
+                                s2 = 1
+                            end
+                        end
+                    end
+
+                    s1 = HasTag(l1, "reverseblink") and (1-s1) or s1
+                    s2 = HasTag(l2, "reverseblink") and (1-s2) or s2
+
+                    local altl1 = HasTag(l1,"blinka")
+                    if not pLightsA or altl1 then
+                        SetShapeEmissiveScale(l1, s1)
+                    else
+                        SetShapeEmissiveScale(l1, 0)
+                    end
+                    if l2 then
+                        local altl2 = HasTag(l2,"blinka")
+                        if not pLightsA or altl2 then
+                            SetShapeEmissiveScale(l2, s2)
+                        else
+                            SetShapeEmissiveScale(l2, 0)
+                        end
+                    end
+                end
+            end
+        else
+            for i = 1, #lightshapes do
+                SetShapeEmissiveScale(lightshapes[i], 0)
             end
         end
     end
-    joint = FindJoints("spawnjoint")
-    -- Get jointed bodies and check for one with a vehicle -> get jointedbody, jointedvehicle, check=true
-    jointbodies = GetJointedBodies(jointbody)
-    check = false
-    if #jointbodies >= 1 then
-        for i=1, #jointbodies do
-            if GetBodyVehicle(jointbodies[i]) ~= 0 then
-                jointedbody = jointbodies[i]
-                jointedvehicle = GetBodyVehicle(jointbodies[i])
-                check = true
-            end
-        end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == jointshape and InputPressed("interact") then
+        attached = not attached
     end
-
-    if not check then
-        attached = false
-    end
-
-    if GetPlayerVehicle() == jointedvehicle then
+    if GetPlayerVehicle(playerId) == jointedvehicle then
         if InputPressed("f") then
             active = not active
             DebugPrint("TOGGLE")
         end
     end
-    
-    if (not attached) then
-        active = false
-    end
+end
 
-    if active then
-        for i = 1, #lightshapes, 2 do
-            local l1 = lightshapes[i]
-            local l2 = lightshapes[i + 1]
-
-            if l1 then
-                local bp1Str = GetTagValue(l1, "blink") or "2,0.075,0.15,0.1,1"
-                local bp2Str = l2 and GetTagValue(l2, "blink") or "2,0.075,0.15,0.1,1"
-
-                local bp1 = split(bp1Str, ",")
-                local bp2 = split(bp2Str, ",")
-
-                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
-                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
-
-                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
-                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
-
-                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
-                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
-
-                local t = GetTime() + (i * 0.05)
-                local cD = math.max(cD1, cD2)
-                local c = t % cD
-
-                local s1, s2 = 0, 0
-
-                if simultaneous1 == 1 and simultaneous2 == 1 then
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = j * (fD2 + pB2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                else
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                end
-                
-                s1 = HasTag(l1, "reverseblink") and (1-s1) or s1
-                s2 = HasTag(l2, "reverseblink") and (1-s2) or s2
-
-                local altl1 = HasTag(l1,"blinka")
-                if not pLightsA or altl1 then
-                    SetShapeEmissiveScale(l1, s1)
-                else
-                    SetShapeEmissiveScale(l1, 0)
-                end
-                if l2 then
-                    local altl2 = HasTag(l2,"blinka")
-                    if not pLightsA or altl2 then
-                        SetShapeEmissiveScale(l2, s2)
-                    else
-                        SetShapeEmissiveScale(l2, 0)
-                    end
-                end
-            end
-        end
-    else
-        for i = 1, #lightshapes do
-            SetShapeEmissiveScale(lightshapes[i], 0)
-        end
-    end
-
-end
```

---

# Migration Report: props\script\euroblitzer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/props\script\euroblitzer.lua
+++ patched/props\script\euroblitzer.lua
@@ -1,3 +1,4 @@
+#version 2
 local flashDuration = 0.1
 local interval = 1.5
 
@@ -12,7 +13,7 @@
     return result
 end
 
-function init()
+function server.init()
     body = FindShape("body")
     button = FindShape("button")
     light_shape = FindShape("light")
@@ -21,24 +22,28 @@
     mode = false
 end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetTag(button, "interact", mode and "Mode : Normal" or "Mode : Off")
+        if mode then
+            local t = GetTime()
+            local modRest = t % interval
 
-function tick()
-    if InputPressed("interact") and (GetPlayerInteractShape() == button) then
-        mode = not mode
-    end
-    SetTag(button, "interact", mode and "Mode : Normal" or "Mode : Off")
-
-    if mode then
-        local t = GetTime()
-        local modRest = t % interval
-
-        if modRest < flashDuration then
-            SetShapeEmissiveScale(light_shape, 1)
+            if modRest < flashDuration then
+                SetShapeEmissiveScale(light_shape, 1)
+            else
+                SetShapeEmissiveScale(light_shape, 0)
+            end
         else
             SetShapeEmissiveScale(light_shape, 0)
         end
-    else
-        SetShapeEmissiveScale(light_shape, 0)
     end
+end
 
-end+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("interact") and (GetPlayerInteractShape(playerId) == button) then
+        mode = not mode
+    end
+end
+

```

---

# Migration Report: props\script\patient_monitor_functions.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/props\script\patient_monitor_functions.lua
+++ patched/props\script\patient_monitor_functions.lua
@@ -1,13 +1,18 @@
-function init()
+#version 2
+function server.init()
     body = FindShape("pmbody")
     button = FindShape("pmbutton")
     screen = FindScreen("pmscreen")
-    sound = LoadSound("MOD/props/snd/patient_monitor_sound.ogg")
     active = false
     soundPlay = nil
 end
 
-function tick()
+function client.init()
+    sound = LoadSound("MOD/props/snd/patient_monitor_sound.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if not IsShapeBroken(body) then
         if active then
             SetTag(button, "interact", "Turn off monitor")
@@ -24,8 +29,9 @@
                 SetScreenEnabled(screen, false)
             end
         end
-        if InputPressed("interact") and GetPlayerInteractShape() == button then
+        if InputPressed("interact") and GetPlayerInteractShape(playerId) == button then
             active = not active
         end
     end
-end+end
+

```

---

# Migration Report: props\script\patient_monitor_screen.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/props\script\patient_monitor_screen.lua
+++ patched/props\script\patient_monitor_screen.lua
@@ -1,11 +1,10 @@
-function init()
-end
-
-function draw()
+#version 2
+function client.draw()
     UiPush()
         UiColor(1,1,1,1)
         UiAlign("center middle")
         UiTranslate(UiWidth()/2,UiHeight()/2)
         UiImage("MOD/props/img/patient_monitor.png")
     UiPop()
-end+end
+

```

---

# Migration Report: script\blitzer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\blitzer.lua
+++ patched/script\blitzer.lua
@@ -1,15 +1,37 @@
-function init()
+#version 2
+function server.init()
     blitzer_buttons = FindShapes("blitzer_button")
     DebugPrint(blitzer_button)
     blitzer_lights = FindShapes("blitzer_light")
-    blitzer_sounds = { LoadSound("MOD/snd/button.ogg"), LoadSound("MOD/snd/blitzer.ogg") }
     active = falses
 end
 
-function tick()
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if active then
+            for i=1, #blitzer_lights do
+                local lgt = blitzer_lights[i]
+                SetShapeEmissiveScale(lgt, 1)
+            end
+        else
+            for i=1, #blitzer_lights do
+                local lgt = blitzer_lights[i]
+                SetShapeEmissiveScale(lgt, 0)
+            end
+        end
+        active = false
+    end
+end
+
+function client.init()
+    blitzer_sounds = { LoadSound("MOD/snd/button.ogg"), LoadSound("MOD/snd/blitzer.ogg") }
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     for i=1, #blitzer_buttons do
         local btn = blitzer_buttons[i]
-        if (GetPlayerInteractShape() == btn and InputPressed("interact")) or InputPressed("q") then
+        if (GetPlayerInteractShape(playerId) == btn and InputPressed("interact")) or InputPressed("q") then
             for i=1,#blitzer_sounds do
                 local snd = blitzer_sounds[i]
                 PlaySound(snd, GetShapeWorldTransform(btn).pos, 1)
@@ -17,18 +39,5 @@
             active = true
         end
     end
+end
 
-    if active then
-        for i=1, #blitzer_lights do
-            local lgt = blitzer_lights[i]
-            SetShapeEmissiveScale(lgt, 1)
-        end
-    else
-        for i=1, #blitzer_lights do
-            local lgt = blitzer_lights[i]
-            SetShapeEmissiveScale(lgt, 0)
-        end
-    end
-
-    active = false
-end
```

---

# Migration Report: script\Cleaner.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Cleaner.lua
+++ patched/script\Cleaner.lua
@@ -1,25 +1,29 @@
-function tick()
-	local shapes = FindShapes('clear')
-	if #shapes>0 then
-		for _,shape in ipairs(shapes)do
-			local body = GetShapeBody(shape)
-			local bodyShapes = GetBodyShapes(body)
-			if #bodyShapes==1 then
-				Delete(shape)
-			else
-				local dontDelete=false
-				for i,v in ipairs(bodyShapes)do
-					if not HasTag(v,'clear')then
-						if GetShapeVoxelCount(v)>0 then
-							dontDelete=true
-							break
-						end
-					end
-				end
-				if not dontDelete then
-					Delete(shape)
-				end
-			end
-		end
-	end
-end+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local shapes = FindShapes('clear')
+        if #shapes ~= 0 then
+        	for _,shape in ipairs(shapes)do
+        		local body = GetShapeBody(shape)
+        		local bodyShapes = GetBodyShapes(body)
+        		if #bodyShapes==1 then
+        			Delete(shape)
+        		else
+        			local dontDelete=false
+        			for i,v in ipairs(bodyShapes)do
+        				if not HasTag(v,'clear')then
+        					if GetShapeVoxelCount(v)>0 then
+        						dontDelete=true
+        						break
+        					end
+        				end
+        			end
+        			if not dontDelete then
+        				Delete(shape)
+        			end
+        		end
+        	end
+        end
+    end
+end
+

```

---

# Migration Report: script\combine.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\combine.lua
+++ patched/script\combine.lua
@@ -1,52 +1,50 @@
-function init()
-    -- Config
+#version 2
+function bool_to_number(value)
+    return value and 1 or 0
+end
+
+function server.init()
     THRESHERVELOCITY = 8.0
-
     thisVehicle = FindVehicle("dumptruck")
     mainBody = GetVehicleBody(thisVehicle)
     thresherJoints = FindJoints("thresher")
-
     broken = false
 end
 
-function tick(dt)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not broken then
 
-    if not broken then
+            -- Vehicle check
+            isPlayerInVehicle = GetPlayerVehicle(playerId) == thisVehicle
 
-        -- Vehicle check
-        isPlayerInVehicle = GetPlayerVehicle() == thisVehicle
+            -- Update motor and check if it is intact
+            local numConnected = 0
+            for i=1, #thresherJoints do
+                local joint = thresherJoints[i]
+                local shapes = GetJointShapes(joint)
 
-        -- Update motor and check if it is intact
-        local numConnected = 0
-        for i=1, #thresherJoints do
-            local joint = thresherJoints[i]
-            local shapes = GetJointShapes(joint)
+                local connected = false
+                for j = 1, #shapes do
+                    local body = GetShapeBody(shapes[j])
 
-            local connected = false
-            for j = 1, #shapes do
-                local body = GetShapeBody(shapes[j])
+                    local jointedBodies = GetJointedBodies(body)
 
-                local jointedBodies = GetJointedBodies(body)
-
-                for k = 1, #jointedBodies do
-                    if jointedBodies[k] == mainBody  then
-                        connected = true
-                        numConnected = numConnected + 1
+                    for k = 1, #jointedBodies do
+                        if jointedBodies[k] == mainBody  then
+                            connected = true
+                            numConnected = numConnected + 1
+                        end
                     end
                 end
+
+                SetJointMotor(joint, bool_to_number(isPlayerInVehicle and connected) * THRESHERVELOCITY)
             end
 
-            SetJointMotor(joint, bool_to_number(isPlayerInVehicle and connected) * THRESHERVELOCITY)
-        end
-
-        if numConnected == 0 then
-            broken = true
+            if numConnected == 0 then
+                broken = true
+            end
         end
     end
-
-
 end
 
-function bool_to_number(value)
-    return value and 1 or 0
-end
```

---

# Migration Report: script\dlkbottom.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\dlkbottom.lua
+++ patched/script\dlkbottom.lua
@@ -1,8 +1,5 @@
-sound1 = GetStringParam("primarySound")
-sound2 = GetStringParam("secondarySound")
-sound3 = GetStringParam("tertiarySound")
-
-function init()
+#version 2
+function server.init()
     body = FindBodies("dlkbottom")
     joints = FindJoints("dlksupport")
     extendButton = FindShape("extend")
@@ -12,15 +9,16 @@
     loop3 = LoadLoop(sound3)
 end
 
-function tick()
-    if InputDown("interact") and GetPlayerInteractShape() == extendButton then
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputDown("interact") and GetPlayerInteractShape(playerId) == extendButton then
         for i=1, #joints do
             SetJointMotor(joints[i],-0.5)
             PlayLoop(loop1,GetShapeWorldTransform(extendButton).pos,0.5)
             PlayLoop(loop2,GetShapeWorldTransform(extendButton).pos,0.5)
             PlayLoop(loop3,GetShapeWorldTransform(extendButton).pos,1.0)
         end
-    elseif InputDown("interact") and GetPlayerInteractShape() == retractButton then
+    elseif InputDown("interact") and GetPlayerInteractShape(playerId) == retractButton then
         for i=1, #joints do
             SetJointMotor(joints[i],0.5)
             PlayLoop(loop1,GetShapeWorldTransform(retractButton).pos,0.5)
@@ -32,4 +30,5 @@
             SetJointMotor(joints[i],0)
         end
     end
-end+end
+

```

---

# Migration Report: script\dlkbottom_auto.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\dlkbottom_auto.lua
+++ patched/script\dlkbottom_auto.lua
@@ -1,43 +1,49 @@
-sound1 = GetStringParam("primarySound")
-sound2 = GetStringParam("secondarySound")
-sound3 = GetStringParam("tertiarySound")
-
+#version 2
 function round(num, numDecimalPlaces)
   local mult = 10^(numDecimalPlaces or 0)
   return math.floor(num * mult + 0.5) / mult
 end
 
-function init()
+function server.init()
     body = FindBodies("dlkbottom")
     joints = FindJoints("dlksupport")
     extendButton = FindShape("extend")
     retractButton = FindShape("retract")
     loop1 = LoadLoop(sound1)
     loop2 = LoadLoop(sound2)
-    loop3 = LoadSound(sound3)
     extend = false
 end
 
-function tick()
-    local joint_min, joint_max = GetJointLimits(joints[1])
-    if InputPressed("interact") and GetPlayerInteractShape() == extendButton then
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local joint_min, joint_max = GetJointLimits(joints[1])
+        if extend then
+            for i=1, #joints do
+                SetJointMotor(joints[i],-0.5)
+            end
+        else
+            for i=1, #joints do
+                SetJointMotor(joints[i],0.5)
+            end
+        end
+    end
+end
+
+function client.init()
+    loop3 = LoadSound(sound3)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("interact") and GetPlayerInteractShape(playerId) == extendButton then
         extend = true
         if round(joint_max,2) == round(GetJointMovement(joints[1]),2) then
             PlaySound(loop3,GetShapeWorldTransform(extendButton).pos,1.0)
         end
-    elseif InputPressed("interact") and GetPlayerInteractShape() == retractButton then
+    elseif InputPressed("interact") and GetPlayerInteractShape(playerId) == retractButton then
         extend = false
         if round(joint_min,2) == round(GetJointMovement(joints[1]),2) then
             PlaySound(loop3,GetShapeWorldTransform(extendButton).pos,1.0)
-        end
-    end
-    if extend then
-        for i=1, #joints do
-            SetJointMotor(joints[i],-0.5)
-        end
-    else
-        for i=1, #joints do
-            SetJointMotor(joints[i],0.5)
         end
     end
     if (round(GetJointMovement(joints[1]),2) ~= round(joint_max,2)) and extend then
@@ -54,4 +60,5 @@
         SetShapeEmissiveScale(extendButton,0)
         SetShapeEmissiveScale(retractButton,0)
     end
-end+end
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

# Migration Report: script\firetruck-eu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\firetruck-eu.lua
+++ patched/script\firetruck-eu.lua
@@ -1,120 +1,122 @@
-function init()
-	lights = FindShapes("blink")
-	pLights = false
-	vehicle = FindVehicle()
-	pSiren = false
-	sirensound = LoadLoop("MOD/snd/firetruck-eu.ogg")
-end
-
+#version 2
 function playSiren()
 	local pos = GetVehicleTransform(vehicle).pos
 	PlayLoop(sirensound, pos, 2)
 end
 
-function draw()
-if GetPlayerVehicle() == vehicle then
-		local lightinfo = {}
-		lightinfo[#lightinfo+1] = {"F", "Lights"}
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #lightinfo*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 250, h, 6, 6)
-			UiTranslate(100, 32)
-			UiColor(1,1,1)
-			for i=1, #lightinfo do
-				local key = lightinfo[i][1]
-				local func = lightinfo[i][2]
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
-		local sireninfo = {}
-		sireninfo[#sireninfo+1] = {"G", "Siren"}
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #sireninfo*22 + 30
-			UiTranslate(290, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 250, h, 6, 6)
-			UiTranslate(100, 32)
-			UiColor(1,1,1)
-			for i=1, #sireninfo do
-				local key = sireninfo[i][1]
-				local func = sireninfo[i][2]
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
-	end
--- To whoever is reading this: I'm really sorry (about the code).
-	lightBar = FindBody("lightbar")
-	lightBarJR = FindJoint("lightbarJR")
-	lightBarJL = FindJoint("lightbarJL")
-	lightBroken1 = IsBodyBroken(lightBar1)
-	lightBroken2 = IsJointBroken(lightBarJR)
-	lightBroken3 = IsJointBroken(lightBarJL)
-	
-	if InputPressed("f") then
-		if GetPlayerVehicle() == vehicle then
-		 	if pLights == false then
-				pLights = true
-			else
-				pLights = false
-			end
-		end
-	end
-	
-	if InputPressed("g") then
-		if GetPlayerVehicle() == vehicle then
-		 	if pSiren == false then
-				pSiren = true
-			else
-				pSiren = false
-			end
-		end
-	end
-	
-	if lightBroken1 == false and lightBroken2 == false and lightBroken3 == false then
-		if pLights then
-			for i=1, #lights do
-				local l = lights[i]
-				local p = tonumber(GetTagValue(l, "blink"))
-				if p then
-					local s = math.sin((GetTime()+i) * p)
-					SetShapeEmissiveScale(l, s > 0 and 1 or 0)
-				end
-			end
-		else
-			for i=1, #lights do
-				SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
-			end
-		end
-	else
-		for i=1, #lights do
-			SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
-		end
-	end
-	
-	if lightBroken1 == false and lightBroken2 == false and lightBroken3 == false then
-		if pSiren == true and pLights == true then
-			playSiren()
-		end
-	end
-end+function server.init()
+    lights = FindShapes("blink")
+    pLights = false
+    vehicle = FindVehicle()
+    pSiren = false
+    sirensound = LoadLoop("MOD/snd/firetruck-eu.ogg")
+end
+
+function client.draw()
+    if GetPlayerVehicle(playerId) == vehicle then
+    		local lightinfo = {}
+    		lightinfo[#lightinfo+1] = {"F", "Lights"}
+    		UiPush()
+    			UiAlign("top left")
+    			local w = 200
+    			local h = #lightinfo*22 + 30
+    			UiTranslate(20, UiHeight()-h-20)
+    			UiColor(0,0,0,0.5)
+    			UiImageBox("common/box-solid-6.png", 250, h, 6, 6)
+    			UiTranslate(100, 32)
+    			UiColor(1,1,1)
+    			for i=1, #lightinfo do
+    				local key = lightinfo[i][1]
+    				local func = lightinfo[i][2]
+    				UiFont("bold.ttf", 22)
+    				UiAlign("right")
+    				UiText(key)
+    				UiTranslate(10, 0)
+    				UiFont("regular.ttf", 22)
+    				UiAlign("left")
+    				UiText(func)
+    				UiTranslate(-10, 22)
+    			end
+    		UiPop()
+
+    		local sireninfo = {}
+    		sireninfo[#sireninfo+1] = {"G", "Siren"}
+    		UiPush()
+    			UiAlign("top left")
+    			local w = 200
+    			local h = #sireninfo*22 + 30
+    			UiTranslate(290, UiHeight()-h-20)
+    			UiColor(0,0,0,0.5)
+    			UiImageBox("common/box-solid-6.png", 250, h, 6, 6)
+    			UiTranslate(100, 32)
+    			UiColor(1,1,1)
+    			for i=1, #sireninfo do
+    				local key = sireninfo[i][1]
+    				local func = sireninfo[i][2]
+    				UiFont("bold.ttf", 22)
+    				UiAlign("right")
+    				UiText(key)
+    				UiTranslate(10, 0)
+    				UiFont("regular.ttf", 22)
+    				UiAlign("left")
+    				UiText(func)
+    				UiTranslate(-10, 22)
+    			end
+    		UiPop()
+    	end
+    -- To whoever is reading this: I'm really sorry (about the code).
+    	lightBar = FindBody("lightbar")
+    	lightBarJR = FindJoint("lightbarJR")
+    	lightBarJL = FindJoint("lightbarJL")
+    	lightBroken1 = IsBodyBroken(lightBar1)
+    	lightBroken2 = IsJointBroken(lightBarJR)
+    	lightBroken3 = IsJointBroken(lightBarJL)
+
+    	if InputPressed("f") then
+    		if GetPlayerVehicle(playerId) == vehicle then
+    		 	if pLights == false then
+    				pLights = true
+    			else
+    				pLights = false
+    			end
+    		end
+    	end
+
+    	if InputPressed("g") then
+    		if GetPlayerVehicle(playerId) == vehicle then
+    		 	if pSiren == false then
+    				pSiren = true
+    			else
+    				pSiren = false
+    			end
+    		end
+    	end
+
+    	if lightBroken1 == false and lightBroken2 == false and lightBroken3 == false then
+    		if pLights then
+    			for i=1, #lights do
+    				local l = lights[i]
+    				local p = tonumber(GetTagValue(l, "blink"))
+    				if p then
+    					local s = math.sin((GetTime()+i) * p)
+    					SetShapeEmissiveScale(l, s > 0 and 1 or 0)
+    				end
+    			end
+    		else
+    			for i=1, #lights do
+    				SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
+    			end
+    		end
+    	else
+    		for i=1, #lights do
+    			SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
+    		end
+    	end
+
+    	if lightBroken1 == false and lightBroken2 == false and lightBroken3 == false then
+    		if pSiren == true and pLights == true then
+    			playSiren()
+    		end
+    	end
+end
+

```

---

# Migration Report: script\generator.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\generator.lua
+++ patched/script\generator.lua
@@ -1,22 +1,26 @@
-function init()
-
+#version 2
+function server.init()
     generator = FindShape("generator")
     sound = LoadLoop("MOD/snd/motor.ogg")
     powered = False
-
 end
 
-function tick()
-    transform = GetShapeWorldTransform(generator).pos
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        transform = GetShapeWorldTransform(generator).pos
+    end
+end
 
-    if GetPlayerInteractShape() == generator and InputPressed("interact") then
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == generator and InputPressed("interact") then
         powered = not powered
     end
-
     if powered then
         SetTag(generator, "interact", "Turn off")
         PlayLoop(sound, transform, 0.5)
     else
         SetTag(generator, "interact", "Turn on")
     end
-end+end
+

```

---

# Migration Report: script\hingelock.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\hingelock.lua
+++ patched/script\hingelock.lua
@@ -1,27 +1,30 @@
-
-function init()
-	Joints = FindJoints("hingelock")
-	for i = 1, #Joints do
-		local min, max = GetJointLimits(Joints[i])
-		Joints[i] = {
-			handle = Joints[i],
-			strength = tonumber(GetTagValue(Joints[i], "hingelock")) or 10,
-			min = min,
-			max = max
-		}
-	end
+#version 2
+function server.init()
+    Joints = FindJoints("hingelock")
+    for i = 1, #Joints do
+    	local min, max = GetJointLimits(Joints[i])
+    	Joints[i] = {
+    		handle = Joints[i],
+    		strength = tonumber(GetTagValue(Joints[i], "hingelock")) or 10,
+    		min = min,
+    		max = max
+    	}
+    end
 end
 
-function update()
-	for i = 1, #Joints do
-		local joint = Joints[i]
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for i = 1, #Joints do
+        	local joint = Joints[i]
 
-		local val = GetJointMovement(joint.handle)
+        	local val = GetJointMovement(joint.handle)
 
-		local t = (val - joint.min) / (joint.max - joint.min)
-		local target = t > 0.5 and joint.max or joint.min
-		local strength_mult = (t * 2 - 1) ^ 2
+        	local t = (val - joint.min) / (joint.max - joint.min)
+        	local target = t > 0.5 and joint.max or joint.min
+        	local strength_mult = (t * 2 - 1) ^ 2
 
-		SetJointMotorTarget(joint.handle, target, math.huge, strength_mult * joint.strength)
-	end
-end+        	SetJointMotorTarget(joint.handle, target, math.huge, strength_mult * joint.strength)
+        end
+    end
+end
+

```

---

# Migration Report: script\hingelock180.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\hingelock180.lua
+++ patched/script\hingelock180.lua
@@ -1,32 +1,35 @@
-
-function init()
-	Joints = FindJoints("hingelock")
-	for i = 1, #Joints do
-		local strength = tonumber(GetTagValue(Joints[i], "hingelock")) or 10
-		local min, max = GetJointLimits(Joints[i])
-		Joints[i] = {
-			handle = Joints[i],
-			strength = strength,
-			min = strength < 0 and min or 0,
-			max = strength < 0 and 0 or max
-		}
-	end
+#version 2
+function server.init()
+    Joints = FindJoints("hingelock")
+    for i = 1, #Joints do
+    	local strength = tonumber(GetTagValue(Joints[i], "hingelock")) or 10
+    	local min, max = GetJointLimits(Joints[i])
+    	Joints[i] = {
+    		handle = Joints[i],
+    		strength = strength,
+    		min = strength < 0 and min or 0,
+    		max = strength < 0 and 0 or max
+    	}
+    end
 end
 
-function update()
-	for i = 1, #Joints do
-		local joint = Joints[i]
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for i = 1, #Joints do
+        	local joint = Joints[i]
 
-		local val = GetJointMovement(joint.handle)
+        	local val = GetJointMovement(joint.handle)
 
-		local t = math.abs((val - joint.min) / (joint.max - joint.min))
-		local target = t > 0.5 and joint.max or joint.min
-		local strength_mult = (t * 2 - 1) ^ 2
-		if val * joint.strength < 0 then
-			target = -target
-			strength_mult = strength_mult * 1000
-		end
+        	local t = math.abs((val - joint.min) / (joint.max - joint.min))
+        	local target = t > 0.5 and joint.max or joint.min
+        	local strength_mult = (t * 2 - 1) ^ 2
+        	if val * joint.strength < 0 then
+        		target = -target
+        		strength_mult = strength_mult * 1000
+        	end
 
-		SetJointMotorTarget(joint.handle, target, 10, strength_mult * math.abs(joint.strength))
-	end
-end+        	SetJointMotorTarget(joint.handle, target, 10, strength_mult * math.abs(joint.strength))
+        end
+    end
+end
+

```

---

# Migration Report: script\lightpole.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\lightpole.lua
+++ patched/script\lightpole.lua
@@ -1,20 +1,23 @@
-function init()
+#version 2
+function server.init()
     turnjoint = FindJoint("turn")
     extendjoint = FindJoint("extend")
     updownjoint = FindJoint("updown")
     lights = FindShapes("light")
-
     turnleftbutton = FindShape("turnleftbutton")
     turnrightbutton = FindShape("turnrightbutton")
     extendbutton = FindShape("extendbutton")
     retractbutton = FindShape("retractbutton")
 end
 
-function tick()
-    DebugPrint(turnjoint)
-    DebugPrint(extendjoint)
-    DebugPrint(updownjoint)
-    SetJointMotor(turnjoint,0.5)
-    SetJointMotor(updownjoint,0.5)
-    SetJointMotor(extendjoint,0.5)
-end+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        DebugPrint(turnjoint)
+        DebugPrint(extendjoint)
+        DebugPrint(updownjoint)
+        SetJointMotor(turnjoint,0.5)
+        SetJointMotor(updownjoint,0.5)
+        SetJointMotor(extendjoint,0.5)
+    end
+end
+

```

---

# Migration Report: script\lightswitch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\lightswitch.lua
+++ patched/script\lightswitch.lua
@@ -1,4 +1,5 @@
-function init()
+#version 2
+function server.init()
     light_switch = FindShape("light_switch")
     lights = FindLights("switchlight")
     LIT = false
@@ -7,16 +8,23 @@
     end
 end
 
-function tick()
-    if LIT then
-        SetTag(light_switch, "interact", "Off")
-    else
-        SetTag(light_switch, "interact", "On")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if LIT then
+            SetTag(light_switch, "interact", "Off")
+        else
+            SetTag(light_switch, "interact", "On")
+        end
+        for i=1, #lights do
+            SetLightEnabled(lights[i], LIT)
+        end
     end
-    if GetPlayerInteractShape() == light_switch and InputPressed("interact") then
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == light_switch and InputPressed("interact") then
         LIT = not LIT
     end
-    for i=1, #lights do
-        SetLightEnabled(lights[i], LIT)
-    end
-end+end
+

```

---

# Migration Report: script\matrix_textbased.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\matrix_textbased.lua
+++ patched/script\matrix_textbased.lua
@@ -1,3 +1,7 @@
+#version 2
+local section
+local freq
+
 function split(input, separator)
     if separator == nil then
         separator = "%s"
@@ -9,34 +13,30 @@
     return result
 end
 
-local section
-local freq
-function init()
+function server.init()
     section = 1
-
 end
 
-function draw()
-    -- info tag structure: `timing:int,r:float,g:float,b:float,a:float,fontsize:int,opt/rbg:int,gbg:int,bbg:int,abg:int;text1:str,text2:str,...,textn:str`
-    screen = UiGetScreen()
-    info = {split(split(GetTagValue(screen, "matrixscreen"),";")[1], ",")}
-    for i=1, 6 do
-        info[1][i] = tonumber(info[1][i])
-    end
-    table.insert(info, split(split(string.gsub(GetTagValue(screen, "matrixscreen"),'"'," "),";")[2],","))
+function client.draw()
+        screen = UiGetScreen()
+        info = {split(split(GetTagValue(screen, "matrixscreen"),";")[1], ",")}
+        for i=1, 6 do
+            info[1][i] = tonumber(info[1][i])
+        end
+        table.insert(info, split(split(string.gsub(GetTagValue(screen, "matrixscreen"),'"'," "),";")[2],","))
 
-    section = (math.floor(GetTime() / info[1][1]) % #info[2]) + 1
+        section = (math.floor(GetTime() / info[1][1]) % #info[2]) + 1
 
-    local rx, ry, rz = GetQuatEuler(GetShapeLocalTransform(GetScreenShape(screen)).rot)
+        local rx, ry, rz = GetQuatEuler(GetShapeLocalTransform(GetScreenShape(screen)).rot)
 
-    UiPush()
-        UiColor(info[1][2], info[1][3], info[1][4], info[1][5])
-        UiFont("MOD/fonts/matrixboard_rounded.ttf", info[1][6])
-        UiAlign("center middle")
-        UiTranslate(UiWidth()/2, UiHeight()/2)
-        UiText((((math.abs(ry) > 90) and (math.abs(ry) <= 270)) and info[2][section]:gsub("[<>]", function(c)
-  return (c == "<") and ">" or "<"
-end) or info[2][section]))
-    UiPop()
+        UiPush()
+            UiColor(info[1][2], info[1][3], info[1][4], info[1][5])
+            UiFont("MOD/fonts/matrixboard_rounded.ttf", info[1][6])
+            UiAlign("center middle")
+            UiTranslate(UiWidth()/2, UiHeight()/2)
+            UiText((((math.abs(ry) > 90) and (math.abs(ry) <= 270)) and info[2][section]:gsub("[<>]", function(c)
+      return (c == "<") and ">" or "<"
+    end) or info[2][section]))
+        UiPop()
+end
 
-end
```

---

# Migration Report: script\matrixboard.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\matrixboard.lua
+++ patched/script\matrixboard.lua
@@ -1,7 +1,5 @@
-function init()
-end
-
-function draw()
+#version 2
+function client.draw()
     UiFont("default.ttf", 14)
     UiColor(1, 1, 1, 1)
     switchsin = math.sin(GetTime()*4) > 0
@@ -15,4 +13,5 @@
         UiPush()
         UiPop()
     end
-end+end
+

```

---

# Migration Report: script\mountedmissile.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\mountedmissile.lua
+++ patched/script\mountedmissile.lua
@@ -1,152 +1,4 @@
-function init()
-	body = FindBody("body")
-	vehicle = FindVehicle("car")
-	gun = FindBody("gun")
-
-	reticle = LoadSprite("MOD/sprite/reticle4.png")
-
-	upright = true
-	--------------------------------------------------
-	shootSnd = {}
-	for i=0, 5 do
-		shootSnd[i] = LoadSound("tools/launcher"..i..".ogg")
-	end
-	coolDown = 0
-
-	muzzle = Vec(0,0,0)
-	ammo = 40
-	reach = 500
-
-	reloadTime = 0
-	recoil = 1500
-
-	isShooting = false
-	burstMax = 18
-	burst = 18
-	timeBetweenShots = 0.1
-	shootTimer = 0
-
-	missiles = FindShapes("m")
-	missilesReset = true
-end
-
-function tick(dt)
-	if GetPlayerVehicle() ~= vehicle and not isShooting then
-		return
-	end
-
-	local t = GetBodyTransform(body)
-	local gt = GetBodyTransform(gun)
-
-	local gunDirection = Vec(0,-1.5,-8)
-	gunDirection = TransformToParentVec(gt, gunDirection)		
-
-	muzzle = Vec(0,0.8,0)
-	muzzle = TransformToParentVec(gt, muzzle)		
-	muzzle = VecAdd(muzzle,VecAdd(gt.pos,VecScale(gunDirection,0.3)))
-	
-	checkUpright()
-	local health = GetVehicleHealth(vehicle)
-
-	local camPos = GetCameraTransform().pos
-	local turretPos = GetBodyTransform(gun).pos
-
-	local dir = VecSub(camPos,turretPos)
-	dir = VecNormalize(dir)
-
-	local tilt = VecAdd(turretPos,dir)
-	local dist = VecLength(VecSub(camPos,turretPos))
-	
-	heightDiff = tilt[2] - turretPos[2]
-	heightDiff = 0.3 - heightDiff
-	heightDiff = math.max(-0.25,heightDiff)
-
-	if dist < 2 then
-		-- Direction when inside vehicle		
-		local ct = GetCameraTransform()
-
-		local x = 2 * (ct.rot[1]*ct.rot[3] + ct.rot[4]*ct.rot[2])
-		local y = 2 * (ct.rot[2]*ct.rot[3] - ct.rot[4]*ct.rot[1])
-		local z = 1 - 2 * (ct.rot[1]*ct.rot[1] + ct.rot[2]*ct.rot[2])
-
-		shootDir = Vec(-x,-y,-z)
-	else
-		camPos[2] = 0
-		turretPos[2] = 0
-		shootDir = VecSub(turretPos,camPos)
-		shootDir = VecNormalize(shootDir)
-		shootDir[2] = heightDiff
-		shootDir = VecNormalize(shootDir)
-	end
-
-	if upright and health > 0 then
-		local nt = Transform()
-		local lookDir =  VecAdd(gt.pos,VecScale(shootDir,10))
-		nt.rot = QuatLookAt(gt.pos,lookDir)
-		nt.pos = VecCopy(gt.pos)
-		nt.rot = QuatSlerp(gt.rot, nt.rot, 0.04)
-		SetBodyTransform(gun, nt)
-		shoot(dt)
-	end
-
-	if isShooting then
-		shootTimer = shootTimer - dt
-		if shootTimer <= 0 then 
-			missilesReset = false
-			
-			shootTimer = timeBetweenShots
-
-			PlaySound(shootSnd[math.random(0,#shootSnd)])
-			
-			SpawnParticle("smoke", muzzle, VecScale(direction,3), 2, 5)
-			ApplyBodyImpulse(body, t.pos, VecScale(direction,-recoil))
-
-			x = 2 * (gt.rot[1]*gt.rot[3] + gt.rot[4]*gt.rot[2])
-			y = 2 * (gt.rot[2]*gt.rot[3] - gt.rot[4]*gt.rot[1])
-			z = 1 - 2 * (gt.rot[1]*gt.rot[1] + gt.rot[2]*gt.rot[2])
-
-			local launchDir = Vec(-x,-y,-z)
-			
-			launchDir = VecAdd(launchDir, rndVec(0.08))
-			launchDir[2] = launchDir[2] + 0.1
-			launchDir = VecNormalize(launchDir)
-
-			s = GetShapeLocalTransform(missiles[burst])
-			d = TransformToParentVec(s, Vec(0,-.6,0))
-			s.pos = VecAdd(s.pos, d)
-			SetShapeLocalTransform(missiles[burst], s)
-
-			burst = burst - 1
-			
-			Shoot(muzzle, launchDir, 1)
-			--Shoot(muzzle, shootDir, 1)
-
-			if burst == 0 then
-				isShooting = false
-			end
-		end
-	end
-
-
-	local tmpDir = VecCopy(shootDir)
-	--tmpDir[2] = muzzle[2]
-	tmpDir = VecNormalize(tmpDir)
-
-	QueryRejectBody(body)
-	QueryRejectBody(gun)
-	local hit, dist, normal, shape = QueryRaycast(muzzle, tmpDir, reach)
-
-	projectileHitPos = VecAdd(muzzle,VecScale(tmpDir, dist))
-	drawReticle = hit
-
-	if drawReticle and GetPlayerVehicle() == vehicle and ammo > 0 then
-		local t = Quat()
-		t.pos = projectileHitPos
-		drawReticleSprite(t)
-	end
-	
-end
-
+#version 2
 function checkUpright()
 	local t = GetBodyTransform(body)
 	upright = true
@@ -158,7 +10,6 @@
 	end	
 end
 
---Return a random vector of desired length
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -171,10 +22,10 @@
 	local muzzle = Vec(0,1.2,0)
 	muzzle = VecAdd(muzzle,VecAdd(t.pos,VecScale(direction,4.9)))
 
-	if reloadTime > 0 then
+	if reloadTime ~= 0 then
 		reloadTime = reloadTime - dt
 		return
-	elseif not missilesReset and ammo > 0 then 
+	elseif not missilesReset and ammo ~= 0 then 
 		missilesReset = true
 		for i=1, #missiles do
 			s = GetShapeLocalTransform(missiles[i])
@@ -185,7 +36,7 @@
 	end
 
 	if InputDown("lmb") then
-		if ammo > 0 then
+		if ammo ~= 0 then
 			if not isShooting then
 				isShooting = true
 				shootTimer = 0				
@@ -194,12 +45,6 @@
 				burst = burstMax				
 			end
 		end
-	end
-end
-
-function draw(dt)
-	if GetPlayerVehicle() == vehicle and GetString("level.state") == "" then
-		drawTool()
 	end
 end
 
@@ -229,4 +74,146 @@
 		UiPop()
 		UiTranslate(150, 0)
 	UiPop()
-end+end
+
+function server.init()
+    body = FindBody("body")
+    vehicle = FindVehicle("car")
+    gun = FindBody("gun")
+    reticle = LoadSprite("MOD/sprite/reticle4.png")
+    upright = true
+    --------------------------------------------------
+    shootSnd = {}
+    coolDown = 0
+    muzzle = Vec(0,0,0)
+    ammo = 40
+    reach = 500
+    reloadTime = 0
+    recoil = 1500
+    isShooting = false
+    burstMax = 18
+    burst = 18
+    timeBetweenShots = 0.1
+    shootTimer = 0
+    missiles = FindShapes("m")
+    missilesReset = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) ~= vehicle and not isShooting then
+        	return
+        end
+        local t = GetBodyTransform(body)
+        local gt = GetBodyTransform(gun)
+        local gunDirection = Vec(0,-1.5,-8)
+        gunDirection = TransformToParentVec(gt, gunDirection)		
+        muzzle = Vec(0,0.8,0)
+        muzzle = TransformToParentVec(gt, muzzle)		
+        muzzle = VecAdd(muzzle,VecAdd(gt.pos,VecScale(gunDirection,0.3)))
+        checkUpright()
+        local health = GetVehicleHealth(vehicle)
+        local camPos = GetCameraTransform().pos
+        local turretPos = GetBodyTransform(gun).pos
+        local dir = VecSub(camPos,turretPos)
+        dir = VecNormalize(dir)
+        local tilt = VecAdd(turretPos,dir)
+        local dist = VecLength(VecSub(camPos,turretPos))
+        heightDiff = tilt[2] - turretPos[2]
+        heightDiff = 0.3 - heightDiff
+        heightDiff = math.max(-0.25,heightDiff)
+        if dist < 2 then
+        	-- Direction when inside vehicle		
+        	local ct = GetCameraTransform()
+
+        	local x = 2 * (ct.rot[1]*ct.rot[3] + ct.rot[4]*ct.rot[2])
+        	local y = 2 * (ct.rot[2]*ct.rot[3] - ct.rot[4]*ct.rot[1])
+        	local z = 1 - 2 * (ct.rot[1]*ct.rot[1] + ct.rot[2]*ct.rot[2])
+
+        	shootDir = Vec(-x,-y,-z)
+        else
+        	camPos[2] = 0
+        	turretPos[2] = 0
+        	shootDir = VecSub(turretPos,camPos)
+        	shootDir = VecNormalize(shootDir)
+        	shootDir[2] = heightDiff
+        	shootDir = VecNormalize(shootDir)
+        end
+        if upright and health ~= 0 then
+        	local nt = Transform()
+        	local lookDir =  VecAdd(gt.pos,VecScale(shootDir,10))
+        	nt.rot = QuatLookAt(gt.pos,lookDir)
+        	nt.pos = VecCopy(gt.pos)
+        	nt.rot = QuatSlerp(gt.rot, nt.rot, 0.04)
+        	SetBodyTransform(gun, nt)
+        	shoot(dt)
+        end
+        local tmpDir = VecCopy(shootDir)
+        --tmpDir[2] = muzzle[2]
+        tmpDir = VecNormalize(tmpDir)
+        QueryRejectBody(body)
+        QueryRejectBody(gun)
+        local hit, dist, normal, shape = QueryRaycast(muzzle, tmpDir, reach)
+        projectileHitPos = VecAdd(muzzle,VecScale(tmpDir, dist))
+        drawReticle = hit
+        if drawReticle and GetPlayerVehicle(playerId) == vehicle and ammo ~= 0 then
+        	local t = Quat()
+        	t.pos = projectileHitPos
+        	drawReticleSprite(t)
+        end
+    end
+end
+
+function client.init()
+    for i=0, 5 do
+    	shootSnd[i] = LoadSound("tools/launcher"..i..".ogg")
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if isShooting then
+    	shootTimer = shootTimer - dt
+    	if shootTimer <= 0 then 
+    		missilesReset = false
+
+    		shootTimer = timeBetweenShots
+
+    		PlaySound(shootSnd[math.random(0,#shootSnd)])
+
+    		SpawnParticle("smoke", muzzle, VecScale(direction,3), 2, 5)
+    		ApplyBodyImpulse(body, t.pos, VecScale(direction,-recoil))
+
+    		x = 2 * (gt.rot[1]*gt.rot[3] + gt.rot[4]*gt.rot[2])
+    		y = 2 * (gt.rot[2]*gt.rot[3] - gt.rot[4]*gt.rot[1])
+    		z = 1 - 2 * (gt.rot[1]*gt.rot[1] + gt.rot[2]*gt.rot[2])
+
+    		local launchDir = Vec(-x,-y,-z)
+
+    		launchDir = VecAdd(launchDir, rndVec(0.08))
+    		launchDir[2] = launchDir[2] + 0.1
+    		launchDir = VecNormalize(launchDir)
+
+    		s = GetShapeLocalTransform(missiles[burst])
+    		d = TransformToParentVec(s, Vec(0,-.6,0))
+    		s.pos = VecAdd(s.pos, d)
+    		SetShapeLocalTransform(missiles[burst], s)
+
+    		burst = burst - 1
+
+    		Shoot(muzzle, launchDir, 1)
+    		--Shoot(muzzle, shootDir, 1)
+
+    		if burst == 0 then
+    			isShooting = false
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    if GetPlayerVehicle(playerId) == vehicle and GetString("level.state") == "" then
+    	drawTool()
+    end
+end
+

```

---

# Migration Report: script\mrap_turret.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\mrap_turret.lua
+++ patched/script\mrap_turret.lua
@@ -1,163 +1,4 @@
-#include "script/common.lua"
-pAmmo = GetIntParam("ammo",3)
-pGun = GetBoolParam("gun",false)
-
-function init()
-    cabmotor = FindJoint("cabmotor")
-    armmotor = FindJoint("armmotor")    
-
-	armSnd = LoadLoop("snd/turretarm.ogg")
-	hutSnd = LoadLoop("snd/turrethut.ogg")
-	
-    armTurn = 0    
-    armSpeed = 0.3
-
-    hutTurn = 0
-    hutSpeed = 0.6
-
-	armAngleMin, armAngleMax = GetJointLimits(armmotor)
-	armAngle = GetJointMovement(armmotor)
-    SetJointMotorTarget(armmotor, armAngle, 1.0, 1000.0)
-    SetJointMotorTarget(cabmotor, 0, 1000.0)
-	
-	armCurrent = GetJointMovement(armmotor)
-	hutCurrent = GetJointMovement(cabmotor)
-
-    --tank
-    ammo = pAmmo
-	reach = 2500
-	reloadTime = 0
-
-	explosionSize = 1.5
-
-	didImpact = false
-	impactPoint = Vec(0,0,0)
-
-	projectileTime = 0.0
-	projectileTimeMax = 0.3
-	projectilePos = Vec(0,0,0)
-	projectileStartPos = Vec(0,0,0)
-	projectileHitPos = Vec(0,0,0)
-
-    direction = Vec(0,0,0)
-
-    armBody = FindBody("arm")    
-    armTransform = GetBodyTransform(armBody)
-	
-	SetTag(armBody, "interact", "Operate")
-
-    muzzleLocation = FindLocation("muzzle")
-    muzzleTransform = GetLocationTransform(muzzleLocation)
-    localMuzzlePos = TransformToLocalPoint(armTransform, muzzleTransform.pos)
-
-    
-    directionLocation = FindLocation("direction")
-    directionTransform = GetLocationTransform(directionLocation)
-    localDirectionPos = TransformToLocalPoint(armTransform, directionTransform.pos)
-
-	if pGun then
-		shootSnd = LoadSound("MOD/snd/gunshot1.ogg")
-	else
-		shootSnd = LoadSound("tools/tankgun0.ogg")
-	end
-	
-	active = false
-	
-	localCameraTransform = GetLocationTransform(FindLocation("camera"))
-	localCameraTransform = TransformToLocalTransform(GetBodyTransform(armBody), localCameraTransform)
-	cameraAnim = 0
-	recoil = 0
-end
-    
-function tick(dt)
-    if active then  
-		SetBool("game.disablemap", true)
-		SetBool("game.disablepause", true)
-		SetBool("game.player.disableinput", true)
-		
-		if InputPressed("interact") or InputPressed("esc") then
-			active = false
-			SetTag(armBody, "interact", "Operate")
-			SetValue("cameraAnim", 0.0, "cosine", 0.5)
-			local t = GetPlayerTransform()
-			t.rot = GetBodyTransform(armBody).rot
-			SetPlayerTransform(t)
-		end
-        armTransform = GetBodyTransform(armBody)
-        worldMuzzlePos = TransformToParentPoint(armTransform,localMuzzlePos)
-        worldDirectionPos = TransformToParentPoint(armTransform,localDirectionPos)
-
-        direction = VecSub(worldDirectionPos, worldMuzzlePos)
-        direction = VecNormalize(direction)
-
-        shoot(dt)
-        if projectileTime > 0 then
-            projectileTime = projectileTime - dt
-            projectTilePos = VecLerp(projectileHitPos, projectileStartPos, projectileTime/projectileTimeMax)
-            SpawnParticle("smoke", projectTilePos, VecScale(VecNormalize(VecSub(projectTilePos,projectileHitPos)),2), 1, 0.5)
-            PointLight(projectTilePos, 0.5, 0.5, 0.5, math.random(1,15))
-        elseif didImpact then
-            didImpact = false
-            Explosion(impactPoint,explosionSize)
-        end
-	else
-		if GetPlayerInteractBody() == armBody and InputPressed("interact") then
-			active = true
-			RemoveTag(armBody, "interact")
-			SetValue("cameraAnim", 1.0, "cosine", 0.5)
-		end
-    end
-
-	if cameraAnim > 0 then
-		local pt = GetPlayerCameraTransform()
-		local lt = TransformCopy(localCameraTransform)
-		lt.pos = VecAdd(lt.pos, Vec(0, 0, -0.5*recoil))
-		local ct = TransformToParentTransform(GetBodyTransform(armBody), lt)
-		SetCameraTransform(Transform(VecLerp(pt.pos, ct.pos, cameraAnim), QuatSlerp(pt.rot, ct.rot, cameraAnim)))
-	end
-	
-end
-
-function update(dt)
-	if active then
-		local armTurnTarget = 0
-		if InputDown("down") then            
-			armTurnTarget = -1.0
-		elseif InputDown("up") then            
-			armTurnTarget = 1.0
-		end
-		armTurn = armTurn + clamp(armTurnTarget-armTurn, -0.06, 0.06)
-
-		local current = GetJointMovement(armmotor)
-		armAngle = clamp(armAngle, current-5, current+5)
-		armAngle = clamp(armAngle + armTurn*armSpeed*180.0/math.pi*dt, armAngleMin, armAngleMax)
-		
-		local hutTurnTarget = 0
-		if InputDown("right") then            
-			hutTurnTarget = 1.0
-		elseif InputDown("left") then            
-			hutTurnTarget = -1.0
-		end
-		hutTurn = hutTurn + clamp(hutTurnTarget-hutTurn, -0.06, 0.06)
-		
-		local ac = GetJointMovement(armmotor)
-		local av = math.abs(armCurrent - ac)
-		armCurrent = ac
-		local hc = GetJointMovement(cabmotor)
-		local hv = math.abs(hutCurrent - hc)
-		hutCurrent = hc
-
-		if av > 0.1 then PlayLoop(armSnd, GetPlayerPos(), av*3) end
-		if hv > 0.1 then PlayLoop(hutSnd, GetPlayerPos(), hv*3) end
-
-		SetJointMotorTarget(armmotor, armAngle, 1.0, 1000)
-		SetJointMotor(cabmotor, hutTurn * hutSpeed, 1000)        
-	else
-		SetJointMotorTarget(armmotor, armAngle, 1.0, 1000)
-		SetJointMotor(cabmotor, 0, 1000)        
-	end
-end
--- Firerate (realoadTime) --
+#version 2
 function shoot(dt)
 	if pGun then
 		if reloadTime > -0.05 then
@@ -191,11 +32,10 @@
 			DrawLine(worldMuzzlePos, VecAdd(worldMuzzlePos,VecScale(direction, reach)), 1, 0, 0, 0.2)
 		end
 
-		if reloadTime > 0 then
+		if reloadTime ~= 0 then
 			reloadTime = reloadTime - dt
 			return
 		end
-
 
 		if InputPressed("usetool") then
 			if ammo > 0 or GetInt("level.sandbox") == 1 then	
@@ -226,12 +66,6 @@
 			end
 		end
 	end	
-end
-
-function draw(dt)
-	if active and GetString("level.state") == "" then
-		drawTool()
-	end
 end
 
 function drawTool()
@@ -256,3 +90,155 @@
 	UiPop()
 end
 
+function server.init()
+       cabmotor = FindJoint("cabmotor")
+       armmotor = FindJoint("armmotor")    
+    armSnd = LoadLoop("snd/turretarm.ogg")
+    hutSnd = LoadLoop("snd/turrethut.ogg")
+       armTurn = 0    
+       armSpeed = 0.3
+       hutTurn = 0
+       hutSpeed = 0.6
+    armAngleMin, armAngleMax = GetJointLimits(armmotor)
+    armAngle = GetJointMovement(armmotor)
+       SetJointMotorTarget(armmotor, armAngle, 1.0, 1000.0)
+       SetJointMotorTarget(cabmotor, 0, 1000.0)
+    armCurrent = GetJointMovement(armmotor)
+    hutCurrent = GetJointMovement(cabmotor)
+       --tank
+       ammo = pAmmo
+    reach = 2500
+    reloadTime = 0
+    explosionSize = 1.5
+    didImpact = false
+    impactPoint = Vec(0,0,0)
+    projectileTime = 0.0
+    projectileTimeMax = 0.3
+    projectilePos = Vec(0,0,0)
+    projectileStartPos = Vec(0,0,0)
+    projectileHitPos = Vec(0,0,0)
+       direction = Vec(0,0,0)
+       armBody = FindBody("arm")    
+       armTransform = GetBodyTransform(armBody)
+    SetTag(armBody, "interact", "Operate")
+       muzzleLocation = FindLocation("muzzle")
+       muzzleTransform = GetLocationTransform(muzzleLocation)
+       localMuzzlePos = TransformToLocalPoint(armTransform, muzzleTransform.pos)
+       directionLocation = FindLocation("direction")
+       directionTransform = GetLocationTransform(directionLocation)
+       localDirectionPos = TransformToLocalPoint(armTransform, directionTransform.pos)
+    active = false
+    localCameraTransform = GetLocationTransform(FindLocation("camera"))
+    localCameraTransform = TransformToLocalTransform(GetBodyTransform(armBody), localCameraTransform)
+    cameraAnim = 0
+    recoil = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if cameraAnim ~= 0 then
+        	local pt = GetPlayerCameraTransform(playerId)
+        	local lt = TransformCopy(localCameraTransform)
+        	lt.pos = VecAdd(lt.pos, Vec(0, 0, -0.5*recoil))
+        	local ct = TransformToParentTransform(GetBodyTransform(armBody), lt)
+        	SetCameraTransform(Transform(VecLerp(pt.pos, ct.pos, cameraAnim), QuatSlerp(pt.rot, ct.rot, cameraAnim)))
+        end
+    end
+end
+
+function client.init()
+    if pGun then
+    	shootSnd = LoadSound("MOD/snd/gunshot1.ogg")
+    else
+    	shootSnd = LoadSound("tools/tankgun0.ogg")
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+       if active then  
+    	SetBool("game.disablemap", true, true)
+    	SetBool("game.disablepause", true, true)
+    	SetBool("game.player.disableinput", true, true)
+
+    	if InputPressed("interact") or InputPressed("esc") then
+    		active = false
+    		SetTag(armBody, "interact", "Operate")
+    		SetValue("cameraAnim", 0.0, "cosine", 0.5)
+    		local t = GetPlayerTransform(playerId)
+    		t.rot = GetBodyTransform(armBody).rot
+    		SetPlayerTransform(playerId, t)
+    	end
+           armTransform = GetBodyTransform(armBody)
+           worldMuzzlePos = TransformToParentPoint(armTransform,localMuzzlePos)
+           worldDirectionPos = TransformToParentPoint(armTransform,localDirectionPos)
+
+           direction = VecSub(worldDirectionPos, worldMuzzlePos)
+           direction = VecNormalize(direction)
+
+           shoot(dt)
+           if projectileTime ~= 0 then
+               projectileTime = projectileTime - dt
+               projectTilePos = VecLerp(projectileHitPos, projectileStartPos, projectileTime/projectileTimeMax)
+               SpawnParticle("smoke", projectTilePos, VecScale(VecNormalize(VecSub(projectTilePos,projectileHitPos)),2), 1, 0.5)
+               PointLight(projectTilePos, 0.5, 0.5, 0.5, math.random(1,15))
+           elseif didImpact then
+               didImpact = false
+               Explosion(impactPoint,explosionSize)
+           end
+    else
+    	if GetPlayerInteractBody(playerId) == armBody and InputPressed("interact") then
+    		active = true
+    		RemoveTag(armBody, "interact")
+    		SetValue("cameraAnim", 1.0, "cosine", 0.5)
+    	end
+       end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if active then
+    	local armTurnTarget = 0
+    	if InputDown("down") then            
+    		armTurnTarget = -1.0
+    	elseif InputDown("up") then            
+    		armTurnTarget = 1.0
+    	end
+    	armTurn = armTurn + clamp(armTurnTarget-armTurn, -0.06, 0.06)
+
+    	local current = GetJointMovement(armmotor)
+    	armAngle = clamp(armAngle, current-5, current+5)
+    	armAngle = clamp(armAngle + armTurn*armSpeed*180.0/math.pi*dt, armAngleMin, armAngleMax)
+
+    	local hutTurnTarget = 0
+    	if InputDown("right") then            
+    		hutTurnTarget = 1.0
+    	elseif InputDown("left") then            
+    		hutTurnTarget = -1.0
+    	end
+    	hutTurn = hutTurn + clamp(hutTurnTarget-hutTurn, -0.06, 0.06)
+
+    	local ac = GetJointMovement(armmotor)
+    	local av = math.abs(armCurrent - ac)
+    	armCurrent = ac
+    	local hc = GetJointMovement(cabmotor)
+    	local hv = math.abs(hutCurrent - hc)
+    	hutCurrent = hc
+
+    	if av > 0.1 then PlayLoop(armSnd, GetPlayerPos(playerId), av*3) end
+    	if hv > 0.1 then PlayLoop(hutSnd, GetPlayerPos(playerId), hv*3) end
+
+    	SetJointMotorTarget(armmotor, armAngle, 1.0, 1000)
+    	SetJointMotor(cabmotor, hutTurn * hutSpeed, 1000)        
+    else
+    	SetJointMotorTarget(armmotor, armAngle, 1.0, 1000)
+    	SetJointMotor(cabmotor, 0, 1000)        
+    end
+end
+
+function client.draw()
+    if active and GetString("level.state") == "" then
+    	drawTool()
+    end
+end
+

```

---

# Migration Report: script\pc_screen.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\pc_screen.lua
+++ patched/script\pc_screen.lua
@@ -1,7 +1,5 @@
-function init()
-end
-
-function draw()
+#version 2
+function client.draw()
     local screen = UiGetScreen()
     local file = string.format("MOD/img/pc/%s", GetTagValue(screen, "pc"))
     UiPush()
@@ -10,4 +8,5 @@
         UiTranslate(UiWidth()/2, UiHeight()/2)
         UiImage(file)
     UiPop()
-end+end
+

```

---

# Migration Report: script\policelightsF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\policelightsF.lua
+++ patched/script\policelightsF.lua
@@ -1,24 +1,24 @@
-function init()
-    -- Find shapes for the different light tags
+#version 2
+function server.init()
     lights = FindShapes("blink")
     lightsR = FindShapes("blinkr")  -- For "blinkr"
     lightsM = FindShapes("blinkm")  -- For "blinkm"
     lightsS = FindShapes("blinks")  -- For "blinks"
-    
     -- States to track whether each light group is on or off
     pLights = false
     pLightsR = false
     pLightsM = false
     pLightsS = false
-
     -- Vehicle and sound setup
     vehicle = FindVehicle()
+end
+
+function client.init()
     sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function draw()
-    -- UI only when the player is in the vehicle
-    if GetPlayerVehicle() == vehicle then
+function client.draw()
+    if GetPlayerVehicle(playerId) == vehicle then
         -- Define the control information for the UI
         local info = {
             {"[F]", "Lights"},
@@ -38,7 +38,7 @@
 
             UiTranslate(100, 32)
             UiColor(1, 1, 1)
-            
+
             -- Loop to draw each control item in the UI
             for i = 1, #info do
                 local key = info[i][1]
@@ -57,7 +57,7 @@
 
     -- Toggle the lights based on inputs
     if InputPressed("f") then
-        if GetPlayerVehicle() == vehicle then
+        if GetPlayerVehicle(playerId) == vehicle then
             local pos = GetVehicleTransform(vehiclepos).pos
             PlaySound(sound_beep, pos, 100)
 
@@ -67,7 +67,7 @@
     end
 
     if InputPressed("r") then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
+        if GetPlayerVehicle(playerId) == vehicle then
             local pos = GetVehicleTransform(vehiclepos).pos
             PlaySound(sound_beep, pos, 100)
 
@@ -77,7 +77,7 @@
     end
 
     if InputPressed("4") then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
+        if GetPlayerVehicle(playerId) == vehicle then
             local pos = GetVehicleTransform(vehiclepos).pos
             PlaySound(sound_beep, pos, 100)
 
@@ -87,7 +87,7 @@
     end
 
     if InputPressed("g") then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
+        if GetPlayerVehicle(playerId) == vehicle then
             local pos = GetVehicleTransform(vehiclepos).pos
             PlaySound(sound_beep, pos, 100)
 
@@ -155,3 +155,4 @@
         end
     end
 end
+

```

---

# Migration Report: script\policesirensF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\policesirensF.lua
+++ patched/script\policesirensF.lua
@@ -0,0 +1 @@
+#version 2

```

---

# Migration Report: script\rollershutter.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\rollershutter.lua
+++ patched/script\rollershutter.lua
@@ -0,0 +1 @@
+#version 2

```

---

# Migration Report: script\Sirens\Fire\Dutch\f_siren_dutch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\Fire\Dutch\f_siren_dutch.lua
+++ patched/script\Sirens\Fire\Dutch\f_siren_dutch.lua
@@ -1,61 +1,65 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	pSirens3 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Dutch/f_dutch1.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Dutch/dutch2.ogg")
-	sound_three = LoadSound("MOD/snd/Sirens/Russia/russia3.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    pSirens3 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Dutch/f_dutch1.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Dutch/dutch2.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-				pSirens3 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-				pSirens3 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
-	if InputPressed("3") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_three, pos, 15)
-		end
-	end
+function client.init()
+    sound_three = LoadSound("MOD/snd/Sirens/Russia/russia3.ogg")
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    			pSirens3 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    			pSirens3 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+    if InputPressed("3") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_three, pos, 15)
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\Fire\Germany\siren_germany_heavy.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\Fire\Germany\siren_germany_heavy.lua
+++ patched/script\Sirens\Fire\Germany\siren_germany_heavy.lua
@@ -1,61 +1,65 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	pSirens3 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Germany/german_fire_heavy.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Germany/german_stadt.ogg")
-	sound_three = LoadSound("MOD/snd/Sirens/Russia/russia3.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    pSirens3 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Germany/german_fire_heavy.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Germany/german_stadt.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-				pSirens3 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-				pSirens3 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
-	if InputPressed("3") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_three, pos, 15)
-		end
-	end
+function client.init()
+    sound_three = LoadSound("MOD/snd/Sirens/Russia/russia3.ogg")
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    			pSirens3 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    			pSirens3 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+    if InputPressed("3") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_three, pos, 15)
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_austria.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_austria.lua
+++ patched/script\Sirens\siren_austria.lua
@@ -1,70 +1,74 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	pSirens3 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Austria/austria1.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Austria/austria2.ogg")
-	loop_three = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    pSirens3 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Austria/austria1.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Austria/austria2.ogg")
+    loop_three = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-				pSirens3 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-				pSirens3 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
-	if InputPressed("3") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens3 == false then
-				pSirens3 = true
-				pSirens2 = false
-				pSirens1 = false
-			else
-				pSirens3 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 30)
-	end
-	if pSirens3 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_three, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 30)
+    end
+    if pSirens3 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_three, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    			pSirens3 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    			pSirens3 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+    if InputPressed("3") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens3 == false then
+    			pSirens3 = true
+    			pSirens2 = false
+    			pSirens1 = false
+    		else
+    			pSirens3 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_dutch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_dutch.lua
+++ patched/script\Sirens\siren_dutch.lua
@@ -1,70 +1,74 @@
-	function init()
-	pSirens1 = false
-	pSirens2 = false
-	pSirens3 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Dutch/dutch2.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Dutch/dutch1.ogg")
-	loop_three = LoadLoop("MOD/snd/Sirens/Germany/german_stadt.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    pSirens3 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Dutch/dutch2.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Dutch/dutch1.ogg")
+    loop_three = LoadLoop("MOD/snd/Sirens/Germany/german_stadt.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-				pSirens3 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-				pSirens3 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
-	if InputPressed("3") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens3 == false then
-				pSirens3 = true
-				pSirens2 = false
-				pSirens1 = false
-			else
-				pSirens3 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 30)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 30)
-	end
-	if pSirens3 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_three, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 30)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 30)
+    end
+    if pSirens3 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_three, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    			pSirens3 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    			pSirens3 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+    if InputPressed("3") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens3 == false then
+    			pSirens3 = true
+    			pSirens2 = false
+    			pSirens1 = false
+    		else
+    			pSirens3 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_gendamerie.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_gendamerie.lua
+++ patched/script\Sirens\siren_gendamerie.lua
@@ -1,49 +1,53 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/France/gendamerie.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/France/gendamerie.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_germany.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_germany.lua
+++ patched/script\Sirens\siren_germany.lua
@@ -1,70 +1,74 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	pSirens3 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Germany/german_stadt.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Germany/german_land.ogg")
-	loop_three = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    pSirens3 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Germany/german_stadt.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Germany/german_land.ogg")
+    loop_three = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-				pSirens3 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-				pSirens3 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
-	if InputPressed("3") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens3 == false then
-				pSirens3 = true
-				pSirens2 = false
-				pSirens1 = false
-			else
-				pSirens3 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 30)
-	end
-	if pSirens3 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_three, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 30)
+    end
+    if pSirens3 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_three, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    			pSirens3 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    			pSirens3 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+    if InputPressed("3") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens3 == false then
+    			pSirens3 = true
+    			pSirens2 = false
+    			pSirens1 = false
+    		else
+    			pSirens3 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_italia.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_italia.lua
+++ patched/script\Sirens\siren_italia.lua
@@ -1,49 +1,53 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Germany/german_land.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Germany/german_land.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_poland.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_poland.lua
+++ patched/script\Sirens\siren_poland.lua
@@ -1,70 +1,74 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	pSirens3 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Poland/poland1.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Poland/poland2.ogg")
-	loop_three = LoadLoop("MOD/snd/Sirens/Poland/poland3.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    pSirens3 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Poland/poland1.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Poland/poland2.ogg")
+    loop_three = LoadLoop("MOD/snd/Sirens/Poland/poland3.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-				pSirens3 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-				pSirens3 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
-	if InputPressed("3") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens3 == false then
-				pSirens3 = true
-				pSirens2 = false
-				pSirens1 = false
-			else
-				pSirens3 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 30)
-	end
-	if pSirens3 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_three, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 30)
+    end
+    if pSirens3 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_three, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    			pSirens3 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    			pSirens3 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+    if InputPressed("3") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens3 == false then
+    			pSirens3 = true
+    			pSirens2 = false
+    			pSirens1 = false
+    		else
+    			pSirens3 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_russia.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_russia.lua
+++ patched/script\Sirens\siren_russia.lua
@@ -1,61 +1,65 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	pSirens3 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Russia/russia1.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Russia/russia2.ogg")
-	sound_three = LoadSound("MOD/snd/Sirens/Russia/russia3.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    pSirens3 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Russia/russia1.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Russia/russia2.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-				pSirens3 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-				pSirens3 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
-	if InputPressed("3") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_three, pos, 15)
-		end
-	end
+function client.init()
+    sound_three = LoadSound("MOD/snd/Sirens/Russia/russia3.ogg")
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    			pSirens3 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    			pSirens3 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+    if InputPressed("3") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_three, pos, 15)
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_sweden.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_sweden.lua
+++ patched/script\Sirens\siren_sweden.lua
@@ -1,49 +1,53 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Sweden/sweden.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Sweden/sweden.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\Sirens\siren_wail.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Sirens\siren_wail.lua
+++ patched/script\Sirens\siren_wail.lua
@@ -1,49 +1,53 @@
-function init()
-	pSirens1 = false
-	pSirens2 = false
-	vehicle = FindVehicle()
-	loop_primary = LoadLoop("MOD/snd/Sirens/Wail/wail.ogg")
-	loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
-	sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens1 = false
+    pSirens2 = false
+    vehicle = FindVehicle()
+    loop_primary = LoadLoop("MOD/snd/Sirens/Wail/wail.ogg")
+    loop_secondary = LoadLoop("MOD/snd/Sirens/Wail/yelp.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens1 == false then
-				pSirens1 = true
-				pSirens2 = false
-			else
-				pSirens1 = false
-			end
-		end
-	end
-	if InputPressed("2") then
-		if GetPlayerVehicle() == vehicle then
-			local pos = GetVehicleTransform(vehiclepos).pos
-			PlaySound(sound_beep, pos, 100)
-		 	if pSirens2 == false then
-				pSirens2 = true
-				pSirens1 = false
-			else
-				pSirens2 = false
-			end
-		end
-	end
+function client.init()
+    sound_beep = LoadSound("MOD/snd/Vehicle Systems/Sirens/siren_beep.ogg")
 end
 
-function tick()
-	if pSirens1 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_primary, pos, 15)
-	end
-	if pSirens2 then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop_secondary, pos, 15)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens1 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_primary, pos, 15)
+    end
+    if pSirens2 then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop_secondary, pos, 15)
+    end
 end
 
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens1 == false then
+    			pSirens1 = true
+    			pSirens2 = false
+    		else
+    			pSirens1 = false
+    		end
+    	end
+    end
+    if InputPressed("2") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    		local pos = GetVehicleTransform(vehiclepos).pos
+    		PlaySound(sound_beep, pos, 100)
+    	 	if pSirens2 == false then
+    			pSirens2 = true
+    			pSirens1 = false
+    		else
+    			pSirens2 = false
+    		end
+    	end
+    end
+end
 

```

---

# Migration Report: script\slidingShutterDoorScript.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\slidingShutterDoorScript.lua
+++ patched/script\slidingShutterDoorScript.lua
@@ -1,38 +1,7 @@
+#version 2
 local mMax = math.max
 local mAbs = math.abs
 local tRemove = table.remove
-
-function init()
-	local slidingShutterDoors = FindBodies("slidingShutterDoorBody")
-	totalDoors = #slidingShutterDoors
-	matchList = {}
-	for i=1, #slidingShutterDoors do
-		local tempDoor = slidingShutterDoors[i]
-		local jointList = {}
-		local range = 0
-		local voxRange = 0
-		local doorShapes = GetBodyShapes(tempDoor)
-		local totalShapes = #doorShapes
-		for s=1, totalShapes do
-			local shape = doorShapes[s]
-			SetTag(shape, "inherittags")
-			if not HasTag(shape, "slidingShutterDoorIdx") then SetTag(shape, "slidingShutterDoorIdx", s) end
-			local joints = GetShapeJoints(shape)
-			for j=1, #joints do
-				if HasTag(joints[j], "slidingShutterDoorJoint") then
-					local joint = joints[j]
-					jointList[#jointList+1] = joint
-					if range ~= 0 then break end
-					local limMin, limMax = GetJointLimits(joint)
-					range = limMax-limMin
-					voxRange = tostring(string.format("%d", range*10))
-					break
-				end
-			end
-		end
-		matchList[i] = {tempDoor, jointList, range, voxRange, totalShapes, totalShapes-voxRange}
-	end
-end
 
 function postUpdate()
 	for i=1, totalDoors do
@@ -91,4 +60,37 @@
 		tRemove(newList, inverseRemove[i])
 	end
 	return returnJoint, newList
-end+end
+
+function server.init()
+    local slidingShutterDoors = FindBodies("slidingShutterDoorBody")
+    totalDoors = #slidingShutterDoors
+    matchList = {}
+    for i=1, #slidingShutterDoors do
+    	local tempDoor = slidingShutterDoors[i]
+    	local jointList = {}
+    	local range = 0
+    	local voxRange = 0
+    	local doorShapes = GetBodyShapes(tempDoor)
+    	local totalShapes = #doorShapes
+    	for s=1, totalShapes do
+    		local shape = doorShapes[s]
+    		SetTag(shape, "inherittags")
+    		if not HasTag(shape, "slidingShutterDoorIdx") then SetTag(shape, "slidingShutterDoorIdx", s) end
+    		local joints = GetShapeJoints(shape)
+    		for j=1, #joints do
+    			if HasTag(joints[j], "slidingShutterDoorJoint") then
+    				local joint = joints[j]
+    				jointList[#jointList+1] = joint
+    				if range ~= 0 then break end
+    				local limMin, limMax = GetJointLimits(joint)
+    				range = limMax-limMin
+    				voxRange = tostring(string.format("%d", range*10))
+    				break
+    			end
+    		end
+    	end
+    	matchList[i] = {tempDoor, jointList, range, voxRange, totalShapes, totalShapes-voxRange}
+    end
+end
+

```

---

# Migration Report: script\slidingShutterDoorVoxscript.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\slidingShutterDoorVoxscript.lua
+++ patched/script\slidingShutterDoorVoxscript.lua
@@ -1,16 +1,12 @@
-brushFile = GetString("brush", "", "object vox")
-doorObj = GetString("door_object", "")
-width = GetInt("width", 6)
-height = GetInt("height", 8)
+#version 2
+function server.init()
+    width = math.abs(width)
+    height = math.max(height)
+    doors = CreateBrush(brushFile..":"..doorObj)
+    for i=1, height do
+    	Vox(0, 0, 0)
+    	Material(doors)
+    	Box(0, i-1, 0, width, i, 1)
+    end
+end
 
-function init()
-	width = math.abs(width)
-	height = math.max(height)
-	doors = CreateBrush(brushFile..":"..doorObj)
-
-	for i=1, height do
-		Vox(0, 0, 0)
-		Material(doors)
-		Box(0, i-1, 0, width, i, 1)
-	end
-end

```

---

# Migration Report: script\tank.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\tank.lua
+++ patched/script\tank.lua
@@ -1,59 +1,4 @@
-strength = 2000	--Strength of shockwave impulse
-maxDist = 15	--The maximum distance for bodies to be affected
-maxMass = 1000	--The maximum mass for a body to be affected
-
-function init()
-    tank = FindVehicle("tank")
-	body = FindBody("body")
-
-	reticle1 = LoadSprite("MOD/sprite/reticle1.png")
-	reticle2 = LoadSprite("MOD/sprite/reticle2.png")
-	reticle3 = LoadSprite("MOD/sprite/reticle3.png")
-
-	ammo = 50
-	reach = 500
-	reloadTime = 1
-
-	recoil = 150000
-	explosionSize = 3
-
-	drawReticle = false
-	didImpact = false
-	impactPoint = Vec(0,0,0)
-
-	projectileTime = 0.0
-	projectileTimeMax = 0.3
-	projectilePos = Vec(0,0,0)
-	projectileStartPos = Vec(0,0,0)
-	projectileHitPos = Vec(0,0,0)
-
-	shootSnd = {}
-	for i=0, 3 do
-		shootSnd[i] = LoadSound("tools/tankgun"..i..".ogg")
-	end
-end
-    
-function tick(dt)	
-    if GetPlayerVehicle() == tank then
-		shoot(dt)
-	end
-	if projectileTime > 0 then
-		projectileTime = projectileTime - dt
-		projectTilePos = VecLerp(projectileHitPos, projectileStartPos, projectileTime/projectileTimeMax)
-		SpawnParticle("smoke", projectTilePos, VecScale(VecNormalize(VecSub(projectTilePos,projectileHitPos)),2), 1, 0.5)
-		PointLight(projectTilePos, 0.5, 0.5, 0.5, math.random(1,15))
-	elseif didImpact then
-		didImpact = false
-		Explosion(impactPoint,explosionSize)
-	end
-
-	if drawReticle and GetPlayerVehicle() == tank and ammo > 0 then
-		local t = Quat()
-		t.pos = projectileHitPos
-		drawReticleSprite(t)
-	end
-end
-
+#version 2
 function drawReticleSprite(t)
 	--t.rot = QuatLookAt(t.pos, GetCameraTransform().pos)
 	t.rot = QuatLookAt(t.pos, GetBodyTransform(body).pos)
@@ -90,7 +35,7 @@
 	hitPoint = VecAdd(muzzle, VecScale(direction, dist))
 	projectileHitPos = VecCopy(hitPoint)
 
-	if reloadTime > 0 then
+	if reloadTime ~= 0 then
 		reloadTime = reloadTime - dt
 		return
 	end
@@ -103,7 +48,7 @@
 		--DebugCross(t.pos, 0, 1, 0)        
 		--DebugCross(VecAdd(t.pos, direction), 0, 0, 1)
 		--DebugLine(t.pos, VecAdd(t.pos, VecScale(direction, 1)), 1, 0, 0)
-		if ammo > 0 then		
+		if ammo ~= 0 then		
 			--animate projectile light
 			projectileTime = projectileTimeMax				
 			projectilePos = VecCopy(muzzle)
@@ -161,12 +106,6 @@
 		local add = VecScale(dir, strength * massScale * distScale)
 
 		ApplyBodyImpulse(b, bc, add)
-	end
-end
-
-function draw(dt)
-	if GetPlayerVehicle() == tank and GetString("level.state") == "" then
-		drawTool()
 	end
 end
 
@@ -192,7 +131,6 @@
 	UiPop()
 end
 
-
 function drawAABB(mi,ma)
 	DebugLine(Vec(mi[1],mi[2],mi[3]), Vec(ma[1],mi[2],mi[3]), 1, 0, 0)
 	DebugLine(Vec(mi[1],mi[2],mi[3]), Vec(mi[1],mi[2],ma[3]), 1, 0, 0)
@@ -208,4 +146,65 @@
 	DebugLine(Vec(mi[1],mi[2],ma[3]), Vec(mi[1],ma[2],ma[3]), 0, 0, 1)
 	DebugLine(Vec(ma[1],mi[2],mi[3]), Vec(ma[1],ma[2],mi[3]), 0, 0, 1)
 	DebugLine(Vec(ma[1],mi[2],ma[3]), Vec(ma[1],ma[2],ma[3]), 0, 0, 1)
-end+end
+
+function server.init()
+       tank = FindVehicle("tank")
+    body = FindBody("body")
+    reticle1 = LoadSprite("MOD/sprite/reticle1.png")
+    reticle2 = LoadSprite("MOD/sprite/reticle2.png")
+    reticle3 = LoadSprite("MOD/sprite/reticle3.png")
+    ammo = 50
+    reach = 500
+    reloadTime = 1
+    recoil = 150000
+    explosionSize = 3
+    drawReticle = false
+    didImpact = false
+    impactPoint = Vec(0,0,0)
+    projectileTime = 0.0
+    projectileTimeMax = 0.3
+    projectilePos = Vec(0,0,0)
+    projectileStartPos = Vec(0,0,0)
+    projectileHitPos = Vec(0,0,0)
+    shootSnd = {}
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           if GetPlayerVehicle(playerId) == tank then
+        	shoot(dt)
+        end
+        if drawReticle and GetPlayerVehicle(playerId) == tank and ammo ~= 0 then
+        	local t = Quat()
+        	t.pos = projectileHitPos
+        	drawReticleSprite(t)
+        end
+    end
+end
+
+function client.init()
+    for i=0, 3 do
+    	shootSnd[i] = LoadSound("tools/tankgun"..i..".ogg")
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if projectileTime ~= 0 then
+    	projectileTime = projectileTime - dt
+    	projectTilePos = VecLerp(projectileHitPos, projectileStartPos, projectileTime/projectileTimeMax)
+    	SpawnParticle("smoke", projectTilePos, VecScale(VecNormalize(VecSub(projectTilePos,projectileHitPos)),2), 1, 0.5)
+    	PointLight(projectTilePos, 0.5, 0.5, 0.5, math.random(1,15))
+    elseif didImpact then
+    	didImpact = false
+    	Explosion(impactPoint,explosionSize)
+    end
+end
+
+function client.draw()
+    if GetPlayerVehicle(playerId) == tank and GetString("level.state") == "" then
+    	drawTool()
+    end
+end
+

```

---

# Migration Report: script\trailer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\trailer.lua
+++ patched/script\trailer.lua
@@ -1,33 +1,36 @@
-function init()
+#version 2
+function server.init()
     hitchposition = FindShape("hingepos")
-    
     attach = FindShape("attach")
     attached = false
-
     standjoint = FindJoint("stand")
     standshape = FindShape("standshape")
     stand = false
 end
 
-function tick()
-    hingejoints = FindJoints("spawned_hingejoint")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        hingejoints = FindJoints("spawned_hingejoint")
+        if attached then
+            SetTag(attach, "interact", "Detach")
+        else
+            SetTag(attach, "interact", "Attach")
+        end
+        if attached and (#hingejoints == 0) then
+            Spawn("MOD/assets/misc/hingejoint_prefab.xml", GetShapeWorldTransform(hitchposition), false, true)
+        end
+        if (not attached) and (#hingejoints > 0) then
+            for i=1, #hingejoints do
+                Delete(hingejoints[i])
+            end
+        end
+    end
+end
 
-    if GetPlayerInteractShape() == attach and InputPressed("interact") then
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == attach and InputPressed("interact") then
         attached = not attached
     end
+end
 
-    if attached then
-        SetTag(attach, "interact", "Detach")
-    else
-        SetTag(attach, "interact", "Attach")
-    end
-
-    if attached and (#hingejoints == 0) then
-        Spawn("MOD/assets/misc/hingejoint_prefab.xml", GetShapeWorldTransform(hitchposition), false, true)
-    end
-    if (not attached) and (#hingejoints > 0) then
-        for i=1, #hingejoints do
-            Delete(hingejoints[i])
-        end
-    end
-end
```

---

# Migration Report: script\wailsirenF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\wailsirenF.lua
+++ patched/script\wailsirenF.lua
@@ -1,28 +1,28 @@
-function init()
-	pSirens = false
-	vehicle = FindVehicle()
-	loop = LoadLoop("MOD/snd/police-siren2.ogg")
-	vehiclepos = FindVehicle("sirenpos")
+#version 2
+function server.init()
+    pSirens = false
+    vehicle = FindVehicle()
+    loop = LoadLoop("MOD/snd/police-siren2.ogg")
+    vehiclepos = FindVehicle("sirenpos")
 end
 
-function draw()
-	
-	if InputPressed("1") then
-		if GetPlayerVehicle() == vehicle then
-		 	if pSirens == false then
-				pSirens = true
-			else
-				pSirens = false
-			end
-		end
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pSirens then
+    	local pos = GetVehicleTransform(vehiclepos).pos
+    	PlayLoop(loop, pos, 15)
+    end
 end
 
-function tick()
-	if pSirens then
-		local pos = GetVehicleTransform(vehiclepos).pos
-		PlayLoop(loop, pos, 15)
-	end
+function client.draw()
+    if InputPressed("1") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    	 	if pSirens == false then
+    			pSirens = true
+    		else
+    			pSirens = false
+    		end
+    	end
+    end
 end
 
-

```

---

# Migration Report: slf\keybinds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/slf\keybinds.lua
+++ patched/slf\keybinds.lua
@@ -1,3 +1,4 @@
+#version 2
 function initialize_keybinds()
     keybinds = {
         { label="Lights", key="savegame.mod.keys.els.blink", default="F" },
@@ -22,7 +23,8 @@
     for i=1, #keybinds do
         local v = keybinds[i]
         if GetString(v.key) == "" then
-            SetString(v.key,v.default)
+            SetString(v.key,v.default, true)
         end
     end
-end+end
+

```

---

# Migration Report: slf\SLF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/slf\SLF.lua
+++ patched/slf\SLF.lua
@@ -1,47 +1,4 @@
-#include "keybinds.lua"
--- Load parameters
--- Sirens
-vehicletype = GetStringParam("type","car")
-siren_bool = GetBoolParam("siren?")
-siren = GetStringParam("sirenCountry")
-if siren == "" then
-    siren_bool = false
-end
-
-
-siren_variant = GetStringParam("sirenVariant","default")
-
-siren1_loop = GetBoolParam("loopSiren1?")
-siren2_loop = GetBoolParam("loopSiren2?")
-siren3_loop = GetBoolParam("loopSiren3?")
-
-siren1_vol = tonumber(GetStringParam("siren1Volume","1"))
-siren2_vol = tonumber(GetStringParam("siren2Volume","1"))
-siren3_vol = tonumber(GetStringParam("siren3Volume","1"))
-
--- ELS
-hastoplights = GetBoolParam("topLights?")
-hasrearlights = GetBoolParam("rearLights?")
-hasinfolights = GetBoolParam("infoLights?")
-hassurroundlights = GetBoolParam("surroundLights?")
-haspowerlights = GetBoolParam("powerLights?")
-hasaltlights = GetBoolParam("altLights?")
-altlightcolor_r, altlightcolor_g, altlightcolor_b = GetColorParam("altLightColor",0.9,0.7,0.2)
-if not hastoplights then
-    siren_bool = false
-    haspowerlights = false
-end
-
-matrixscreens = FindScreens("matrixscreen")
-matrixjoints = FindJoints("matrixjoint")
-emotor_loop = LoadLoop("robot/turn-loop.ogg")
-
--- Civilian
-blinkdeactivate = GetBoolParam("blinkdeactivate")
-
--- Diff. Lighting
-switchlights = GetBoolParam("switchlights")
-
+#version 2
 function split(input, separator)
     if separator == nil then
         separator = "%s"
@@ -66,7 +23,1255 @@
     return false
 end
 
-function init()
+f GetPlayerVehicle(playerId) == vehicle then
+        if ui_stage == 1 then
+            -- Define the control information for the UI
+            local info = {
+                {"-- Car --",""},
+                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkh")), "Headlights"},
+                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkhb")), "High-Beams"},
+                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkdt")), "Daytime Lights"},
+                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkbr")), "Right Blinker"},
+                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkbl")), "Left Blinker"},
+                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkbh")), "Hazard Lights"},
+                {string.format("[%s]",GetString("savegame.mod.keys.civ.horn")), "Horn"},
+                {"", ""},
+                {"-- UI --",""},
+                {string.format("[%s]",GetString("savegame.mod.keys.ui.cycleui")), "Cycle UI"},
+                {string.format("[%s]",GetString("savegame.mod.keys.ui.togglecfg")), "Config Menu"}
+            }
+            if hastoplights or siren_bool or hasinfolights or hassurroundlights or hasrearlights or hasaltlights then
+                table.insert(info, {"", ""})
+                table.insert(info, {"-- ELS --", ""})
+            end
+            if hastoplights then
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blink")), "Lights"})
+            end
+            if haspowerlights then
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinkp")), "Additional"})
+            end
+            if siren_bool then
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.siren1")), "Siren 1"})
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.siren2")), "Siren 2"})
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.siren3")), "Siren 3"})
+            end
+            if hasinfolights then
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinkm")), "Signal"})
+            end
+            if hassurroundlights then
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinks")), "Scene"})
+            end
+            if hasrearlights then
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinkr")), "Directional"})
+            end
+            if hasaltlights then
+                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinka")), "Toggle Color"})
+            end
+
+            UiPush()
+                UiAlign("top left")
+                local w = 200
+                local h = #info * 22 + 30
+                UiTranslate(20, UiHeight() - h - 20)
+                UiColor(0, 0, 0, 0.5)
+                UiImageBox("common/box-solid-6.png", 250, h, 6, 6)  -- Background box
+
+                UiTranslate(100, 32)
+                UiColor(1, 1, 1)
+                
+                -- Loop to draw each control item in the UI
+                for i = 1, #info do
+                    local key = info[i][1]
+                    local func = info[i][2]
+                    UiFont("bold.ttf", 22)
+                    UiAlign("right")
+                    UiText(key) 
+                    UiTranslate(10, 0)
+                    UiFont("regular.ttf", 22)
+                    UiAlign("left")
+                    UiText(func)
+                    UiTranslate(-10, 22)
+                end
+            UiPop()
+        elseif ui_stage == 3 then
+            UiColor(1, 1, 1, 1)
+            UiFont("regular.ttf", 26)
+            UiAlign("left top")
+            UiPush()
+                UiAlign("left bottom")
+                UiTranslate(10, UiHeight())
+                UiImage("MOD/slf/ui/interior/base/bg_base.png")
+            UiPop()
+            UiPush()
+                UiAlign("right bottom")
+                UiTranslate(300,UiHeight()-7)
+                if cLightsBL and cLightsBR then
+                    local activation = math.sin(GetTime() * tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
+                    if activation then
+                        UiImage("MOD/slf/ui/interior/base/hazard_on.png")
+                    else
+                        UiImage("MOD/slf/ui/interior/base/hazard_off.png")
+                    end
+                else
+                    UiImage("MOD/slf/ui/interior/base/hazard_off.png")
+                end
+            UiPop()
+            UiPush()
+                UiAlign("right bottom")
+                UiTranslate(197,UiHeight()-13)
+                if cLightsHB then
+                    UiImage("MOD/slf/ui/interior/base/headlight_highbeam.png")
+                elseif cLightsH then
+                    UiImage("MOD/slf/ui/interior/base/headlight_head.png")
+                elseif clightsDTL or clightsDTR then
+                    UiImage("MOD/slf/ui/interior/base/headlight_daylight.png")
+                else
+                    UiImage("MOD/slf/ui/interior/base/headlight_off.png")
+                end
+            UiPop()
+            UiPush()
+                UiAlign("right bottom")
+                UiTranslate(142,UiHeight()-11)
+                if cLightsBR then
+                    local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBR[1],"blinkbr"))) > 0
+                    if activation then
+                        UiImage("MOD/slf/ui/interior/base/indicator_right_on.png")
+                    else
+                        UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
+                    end
+                else
+                    UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
+                end
+                UiTranslate(-43, 0)
+                if cLightsBL then
+                    local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
+                    if activation then
+                        UiImage("MOD/slf/ui/interior/base/indicator_left_on.png")
+                    else
+                        UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
+                    end
+                else
+                    UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
+                end
+            UiPop()
+            UiPush()
+                UiTranslate(5,5)
+                UiAlign("left top")
+                UiFont("regular.ttf",24)
+                UiColor(1,1,1,0.75)
+                UiText(string.format("[%s] - Cycle UI",GetString("savegame.mod.keys.ui.cycleui")))
+                UiTranslate(0,20)
+                UiText(string.format("[%s] - Config Menu",GetString("savegame.mod.keys.ui.togglecfg")))
+            UiPop()
+        elseif ui_stage == 2 then
+            UiColor(1,1,1,1)
+            UiAlign("left top")
+            UiFont("regular.ttf",26)
+            local buttons = 0
+            if siren_bool then
+                buttons = buttons + 2
+            end
+            if hastoplights then
+                buttons = buttons + 1
+            end
+            if hasrearlights then
+                buttons = buttons + 1
+            end
+            if hasinfolights then
+                buttons = buttons + 1
+            end
+            if hassurroundlights then
+                buttons = buttons + 1
+            end
+            if haspowerlights then
+                buttons = buttons + 1
+            end
+            if hasaltlights then
+                buttons = buttons + 1
+            end
+            local rows = math.ceil(buttons/4)
+            if rows == 0 then
+                ui_stage = 3
+            else
+                UiPush()
+                    UiAlign("left bottom")
+                    UiTranslate(10,UiHeight()-10)
+                    UiImage(string.format("MOD/slf/ui/interior/els/bg_els_rows%s.png",tostring(rows)))
+                UiPop()
+
+                -- Civilian Vehicle Functions
+                UiColor(1, 1, 1, 1)
+                UiFont("regular.ttf", 26)
+                UiAlign("left top")
+                UiPush()
+                    UiAlign("right bottom")
+                    UiTranslate(300,UiHeight()-7-((rows*(60+10))+10+35+10+5))
+                    if cLightsBL and cLightsBR then
+                        local activation = math.sin(GetTime() * tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
+                        if activation then
+                            UiImage("MOD/slf/ui/interior/base/hazard_on.png")
+                        else
+                            UiImage("MOD/slf/ui/interior/base/hazard_off.png")
+                        end
+                    else
+                        UiImage("MOD/slf/ui/interior/base/hazard_off.png")
+                    end
+                UiPop()
+                UiPush()
+                    UiAlign("right bottom")
+                    UiTranslate(197,UiHeight()-13-((rows*(60+10))+10+35+10+5))
+                    if cLightsHB then
+                        UiImage("MOD/slf/ui/interior/base/headlight_highbeam.png")
+                    elseif cLightsH then
+                        UiImage("MOD/slf/ui/interior/base/headlight_head.png")
+                    elseif clightsDTL or clightsDTR then
+                        UiImage("MOD/slf/ui/interior/base/headlight_daylight.png")
+                    else
+                        UiImage("MOD/slf/ui/interior/base/headlight_off.png")
+                    end
+                UiPop()
+                UiPush()
+                    UiAlign("right bottom")
+                    UiTranslate(142,UiHeight()-11-((rows*(60+10))+10+35+10+5))
+                    if cLightsBR then
+                        local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBR[1],"blinkbr"))) > 0
+                        if activation then
+                            UiImage("MOD/slf/ui/interior/base/indicator_right_on.png")
+                        else
+                            UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
+                        end
+                    else
+                        UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
+                    end
+                    UiTranslate(-43, 0)
+                    if cLightsBL then
+                        local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
+                        if activation then
+                            UiImage("MOD/slf/ui/interior/base/indicator_left_on.png")
+                        else
+                            UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
+                        end
+                    else
+                        UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
+                    end
+                UiPop()
+
+                -- Cycle Sign
+                UiPush()
+                    UiTranslate(25,UiHeight()-((rows*(60+10))+15+35+10))
+                    UiAlign("left top")
+                    UiFont("regular.ttf",18)
+                    UiColor(0.8,0.8,0.8,0.5)
+                    UiText(string.format("[%s] - Cycle UI",GetString("savegame.mod.keys.ui.cycleui")))
+                    UiTranslate(0,18)
+                    UiText(string.format("[%s] - Config Menu",GetString("savegame.mod.keys.ui.togglecfg")))
+                UiPop()
+                local functions = {
+                    { siren_bool, (pSirens1 or pSirens2 or pSirens3) and "MOD/slf/ui/interior/els/button_siren_on.png" or "MOD/slf/ui/interior/els/button_siren_off.png", 2, {1,1,1,1}},
+                    { hastoplights, pLights and "MOD/slf/ui/interior/els/button_toplight_on.png" or "MOD/slf/ui/interior/els/button_toplight_off.png", 1, {1,1,1,1}},
+                    { hasrearlights, pLightsR and "MOD/slf/ui/interior/els/button_directional_on.png" or "MOD/slf/ui/interior/els/button_directional_off.png", 1, {1,1,1,1}},
+                    { hassurroundlights, pLightsS and "MOD/slf/ui/interior/els/button_scene_on.png" or "MOD/slf/ui/interior/els/button_scene_off.png", 1, {1,1,1,1}},
+                    { hasinfolights, pLightsM and "MOD/slf/ui/interior/els/button_signal_on.png" or "MOD/slf/ui/interior/els/button_signal_off.png", 1, {1,1,1,1}},
+                    { haspowerlights, pLightsP and "MOD/slf/ui/interior/els/button_additional_on.png" or "MOD/slf/ui/interior/els/button_additional_off.png", 1, {1,1,1,1}},
+                    { hasaltlights, pLightsA and "MOD/slf/ui/interior/els/button_altcolor_on.png" or "MOD/slf/ui/interior/els/button_altcolor_off.png", 1, pLightsA and {altlightcolor_r,altlightcolor_g,altlightcolor_b,1} or {1,1,1,1}},
+                }
+                local deltapos = 0
+                local position = 1
+                for i=1, #functions do
+                    local info = functions[i]
+                    if info[1] then
+                        local row = math.ceil(position/4)
+                        local column = position-((row-1)*(row>1 and 4 or 0))
+                        UiPush()
+                            UiTranslate(25,UiHeight()-((rows*(60+10))+10+5))
+                            UiAlign("left top")
+                            UiColor(info[4][1],info[4][2],info[4][3],info[4][4])
+                            UiTranslate((column-1)*70,(row-1)*70)
+                            UiTranslate(-10,-10)
+                            UiImage(info[2])
+                            position = position + info[3]
+                            deltapos = info[3]
+                            UiColor(1,1,1,1)
+                        UiPop()
+                    end
+                end
+
+                UiPush()
+                UiPop()
+            end
+        end
+    end
+    if (GetPlayerVehicle(playerId) == vehicle) and config_menu_open then
+        -- Column 1 : Sirens
+        UiMakeInteractive()
+        UiPush()
+            UiAlign("left top")
+            UiColor(1,1,1,1)
+            UiFont("regular.ttf",24)
+            UiTranslate(10,10)
+            UiText("Sirens")
+            UiTranslate(0,20)
+            for i=1, #siren_list do
+                if siren == siren_list[i][1] then
+                    UiColor(0,1,0,1)
+                end
+                if UiTextButton(siren_list[i][1]:gsub("^%l", string.upper), 50, 20) then
+                    siren = siren_list[i][1]
+                    siren_variant = siren_list[i][2][1]
+                    reloadSirens()
+                end
+                UiColor(1,1,1,1)
+                UiTranslate(0, 30)
+            end
+        UiPop()
+        -- Column 2 : Siren Variants
+        UiPush()
+            UiAlign("left top")
+            UiColor(1,1,1,1)
+            UiFont("regular.ttf",24)
+            UiTranslate(110,10)
+            UiText("Siren Variants")
+            UiTranslate(0,20)
+            for i=1, #siren_list do
+                if siren == siren_list[i][1] then
+                    for x=1, #siren_list[i][2] do
+                        if siren_variant == siren_list[i][2][x] then
+                            UiColor(0,1,0,1)
+                        end
+                        if UiTextButton(siren_list[i][2][x]:gsub("^%l", string.upper), 50, 20) then
+                            siren_variant = siren_list[i][2][x]
+                            reloadSirens()
+                        end
+                        UiColor(1,1,1,1)
+                        UiTranslate(0, 30)
+                    end
+                end
+            end
+        UiPop()
+        -- Column 3 : Loop Sirens
+        UiPush()
+            UiAlign("left top")
+            UiColor(1,1,1,1)
+            UiFont("regular.ttf",24)
+            UiTranslate(310,10)
+            UiText("Siren Loops")
+            UiTranslate(0,20)
+            -- Siren 1
+            if siren1_loop then UiColor(0,1,0,1) end
+            if UiTextButton("Loop Siren 1", 50, 20) then
+                siren1_loop = not siren1_loop
+                reloadSirens()
+            end
+            UiColor(1,1,1,1)
+            UiTranslate(0, 30)
+            -- Siren 2
+            if siren2_loop then UiColor(0,1,0,1) end
+            if UiTextButton("Loop Siren 2", 50, 20) then
+                siren2_loop = not siren2_loop
+                reloadSirens()
+            end
+            UiColor(1,1,1,1)
+            UiTranslate(0, 30)
+            -- Siren 3
+            if siren3_loop then UiColor(0,1,0,1) end
+            if UiTextButton("Loop Siren 3", 50, 20) then
+                siren3_loop = not siren3_loop
+                reloadSirens()
+            end
+            UiColor(1,1,1,1)
+            UiTranslate(0, 30)
+        UiPop()
+        -- Column 4 : Matrix Display
+        -- Language
+        UiPush()
+            UiAlign("left top")
+            UiColor(1,1,1,1)
+            UiFont("regular.ttf",24)
+            UiTranslate(510,10)
+            UiText("Matrix Language")
+            UiTranslate(0,20)
+            for i=1, #matrix_options_textbased do
+                if matrix_options_textbased[i][1] == matrix_ln then UiColor(0,1,0,1) end
+                if UiTextButton(matrix_options_textbased[i][1]:gsub("^%l", string.upper)) then
+                    matrix_ln = matrix_options_textbased[i][1]
+                end
+                UiColor(1,1,1,1)
+                UiTranslate(0, 30)
+            end
+        UiPop()
+        -- Select
+        matrix_ln_options = nil
+        for i=1, #matrix_options_textbased do
+            if matrix_ln == matrix_options_textbased[i][1] then
+                matrix_ln_options = matrix_options_textbased[i][2]
+            end
+        end
+        UiPush()
+            UiAlign("left top")
+            UiColor(1,1,1,1)
+            UiFont("regular.ttf",24)
+            UiTranslate(710,10)
+            UiText("Matrix Options")
+            UiTranslate(0,20)
+            for i=1, #matrix_ln_options do
+                if matrix_options_current == matrix_ln_options[i][1] then UiColor(0,1,0,1) end
+                if UiTextButton(matrix_ln_options[i][1]) then
+                    for x=1, #matrixscreens do
+                        local screen = matrixscreens[x]
+                        if not (HasTag(screen, "matrixboard") or HasTag(screen, "screenignore"))then
+                            local info = split(GetTagValue(screen, "matrixscreen"),";")
+                            info[2] = matrix_ln_options[i][2]
+                            SetTag(screen, "matrixscreen", table.concat(info, ";"))
+                            
+                        end
+                    end
+                    matrix_options_current = matrix_ln_options[i][1]
+                    
+                end
+                UiColor(1,1,1,1)
+                UiTranslate(0,30)
+            end
+        UiPop()
+
+        -- Column 5 : Matrixboard Image
+        UiPush()
+            UiAlign("left top")
+            UiColor(1,1,1,1)
+            UiFont("regular.ttf",24)
+            UiTranslate(910,10)
+            UiText("Matrix Options")
+            UiTranslate(0,20)
+            for i=1, #matrixboard_options do
+                if matrixboard_options_current == matrixboard_options[i] then UiColor(0,1,0,1) end
+                if UiTextButton(matrixboard_options[i]) then
+                    for x=1, #matrixscreens do
+                        screen = matrixscreens[x]
+                        if HasTag(screen, "matrixboard") then
+                            SetTag(screen, "matrixscreen", string.format("MOD/slf/img/matrixboard/%s.png",matrixboard_options[i]))
+                        end
+                    end
+                    matrixboard_options_current = matrixboard_options[i]
+                    
+                end
+                UiColor(1,1,1,1)
+                UiTranslate(0,30)
+            end
+        UiPop()
+
+        -- (Column 6 : Matrixboard Behaviour)
+    end
+end
+
+function tick(dt)
+ 
+
+ -- Toggle the lights based on inputs
+    if InputPressed(GetString("savegame.mod.keys.ui.cycleui")) then
+        if GetPlayerVehicle(playerId) == vehicle then
+            if ui_stage < 3 then
+                ui_stage = ui_stage + 1
+            else
+                ui_stage = 1
+            end
+        end
+    end
+    -- ELS functions
+    if hastoplights then
+        if InputPressed(GetString("savegame.mod.keys.els.blink")) then
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+
+                -- Toggle "blink" lights
+                pLights = not pLights
+                if switchlights then
+                    pLightsR = false
+                end
+            end
+        end
+    end
+
+    if hasrearlights then
+        if InputPressed(GetString("savegame.mod.keys.els.blinkr")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+
+                -- Toggle "blinkr" lights
+                pLightsR = not pLightsR
+                if switchlights then
+                    pLights = false
+                end
+            end
+        end
+    end
+
+    if hasinfolights then
+        if InputPressed(GetString("savegame.mod.keys.els.blinkm")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+
+                -- Toggle "blinkm" lights
+                pLightsM = not pLightsM
+            end
+        end
+    end
+
+    if hassurroundlights then
+        if InputPressed(GetString("savegame.mod.keys.els.blinks")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+
+                -- Toggle "blinks" lights
+                pLightsS = not pLightsS
+            end
+        end
+    end
+
+    if haspowerlights then
+        if pLights or pLightsM then
+            if InputPressed(GetString("savegame.mod.keys.els.blinkp")) then
+                if GetPlayerVehicle(playerId) == vehicle then
+                    local pos = GetVehicleTransform(vehicle).pos
+                    PlaySound(sound_beep, pos, 100)
+
+                    -- Toggle "blinkp" lights
+                    pLightsP = not pLightsP
+                end
+            end
+        else
+            pLightsP = false
+        end
+    end
+
+    if hasaltlights then
+        if InputPressed(GetString("savegame.mod.keys.els.blinka")) then
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+
+                pLights = true
+                pLightsA = not pLightsA
+            end
+        end
+    end
+    -- Civilian functions
+    if cLightsDTM then
+        if InputPressed(GetString("savegame.mod.keys.civ.blinkh")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_click, pos, 100)
+
+                -- Toggle "blinkh" lights
+                cLightsH = not cLightsH
+
+            end
+        end
+    else
+        cLightsH = false
+    end
+    if cLightsH then
+        if InputPressed(GetString("savegame.mod.keys.civ.blinkhb")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_click, pos, 100)
+
+                -- Toggle "blinkhb" lights
+                cLightsHB = not cLightsHB
+
+            end
+        end
+    else
+        cLightsHB = false
+    end
+    if GetPlayerVehicle(playerId) == vehicle then
+        -- Toggle "blinkdt" lights
+        if cLightsDTM then
+            if blinkdeactivate then
+                if cLightsBL then
+                    clightsDTL = false
+                else
+                    clightsDTL = true
+                end
+                if cLightsBR then
+                    clightsDTR = false
+                else
+                    clightsDTR = true
+                end
+            else
+                clightsDTL = true
+                clightsDTR = true
+            end
+        else
+            clightsDTL = false
+            clightsDTR = false
+        end
+    end
+    if InputPressed(GetString("savegame.mod.keys.civ.blinkdt")) then  -- You can change this keybinding to suit your preferences
+        if GetPlayerVehicle(playerId) == vehicle then
+            local pos = GetVehicleTransform(vehicle).pos
+            PlaySound(sound_click, pos, 100)
+
+            cLightsDTM = not cLightsDTM
+        end
+    end
+
+    if InputPressed(GetString("savegame.mod.keys.civ.blinkbr")) then  -- You can change this keybinding to suit your preferences
+        if GetPlayerVehicle(playerId) == vehicle then
+            local pos = GetVehicleTransform(vehicle).pos
+            PlaySound(sound_click, pos, 100)
+
+            -- Toggle "blinkbr" lights
+            if not (cLightsBL and cLightsBR) then
+                cLightsBL = false
+                cLightsBR = not cLightsBR
+            else
+                cLightsBL = false
+                cLightsBR = true
+            end
+        end
+    end
+    if InputPressed(GetString("savegame.mod.keys.civ.blinkbl")) then  -- You can change this keybinding to suit your preferences
+        if GetPlayerVehicle(playerId) == vehicle then
+            local pos = GetVehicleTransform(vehicle).pos
+            PlaySound(sound_click, pos, 100)
+
+            -- Toggle "blinkbl" lights
+            if not (cLightsBL and cLightsBR) then
+                cLightsBR = false
+                cLightsBL = not cLightsBL
+            else
+                cLightsBR = false
+                cLightsBL = true
+            end
+            reloadHeadlights()
+        end
+    end
+    if InputPressed(GetString("savegame.mod.keys.civ.blinkbh")) then  -- You can change this keybinding to suit your preferences
+        if GetPlayerVehicle(playerId) == vehicle then
+            local pos = GetVehicleTransform(vehicle).pos
+            PlaySound(sound_click, pos, 100)
+
+            -- Toggle "blinkbr and bl" lights
+            if cLightsBR and cLightsBL then
+                cLightsBL = false
+                cLightsBR = false
+            else
+                cLightsBL = true
+                cLightsBR = true
+            end
+            reloadHeadlights()
+        end
+    end
+    if InputDown(GetString("savegame.mod.keys.civ.horn")) then  -- You can change this keybinding to suit your preferences
+        if GetPlayerVehicle(playerId) == vehicle then
+            local pos = GetVehicleTransform(vehicle).pos
+            
+            PlayLoop(honksound, pos, 100)
+        end
+    end
+    -- Sirens detection
+    if siren_bool and pLights then
+        if InputPressed(GetString("savegame.mod.keys.els.siren1")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+                if siren1_loop then
+                    pSirens1 = not pSirens1
+                    pSirens2 = false
+                    pSirens3 = false
+                else
+                    pSirens1 = true
+                end
+            end
+        end
+        if InputPressed(GetString("savegame.mod.keys.els.siren2")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+                if siren2_loop then
+                    pSirens2 = not pSirens2
+                    pSirens1 = false
+                    pSirens3 = false
+                else
+                    pSirens2 = true
+                end
+            end
+        end
+        if InputPressed(GetString("savegame.mod.keys.els.siren3")) then  -- You can change this keybinding to suit your preferences
+            if GetPlayerVehicle(playerId) == vehicle then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(sound_beep, pos, 100)
+                if siren3_loop then
+                    pSirens3 = not pSirens3
+                    pSirens2 = false
+                    pSirens1 = false
+                else
+                    pSirens3 = true
+                end
+            end
+        end
+    end
+    
+    -- Light behaviour
+
+    if pLights then
+        for i = 1, #lights, 2 do
+            local l1 = lights[i]
+            local l2 = lights[i + 1]
+
+            if l1 then
+                local bp1Str = GetTagValue(l1, "blink") or "2,0.075,0.15,0.1,1"
+                local bp2Str = l2 and GetTagValue(l2, "blink") or "2,0.075,0.15,0.1,1"
+
+                local bp1 = split(bp1Str, ",")
+                local bp2 = split(bp2Str, ",")
+
+                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
+                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
+
+                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
+                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
+
+                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
+                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
+
+                local t = GetTime() + (i * 0.05)
+                local cD = math.max(cD1, cD2)
+                local c = t % cD
+
+                local s1, s2 = 0, 0
+
+                if simultaneous1 == 1 and simultaneous2 == 1 then
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = j * (fD2 + pB2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                else
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                end
+                
+                s1 = HasTag(l1, "reverseblink") and (1-s1) or s1
+                s2 = HasTag(l2, "reverseblink") and (1-s2) or s2
+
+                local altl1 = HasTag(l1,"blinka")
+                if not pLightsA or altl1 then
+                    SetShapeEmissiveScale(l1, s1)
+                else
+                    SetShapeEmissiveScale(l1, 0)
+                end
+                if l2 then
+                    local altl2 = HasTag(l2,"blinka")
+                    if not pLightsA or altl2 then
+                        SetShapeEmissiveScale(l2, s2)
+                    else
+                        SetShapeEmissiveScale(l2, 0)
+                    end
+                end
+            end
+        end
+        for i=1, #lightsT do
+            SetShapeEmissiveScale(lightsT[i], 1)
+        end
+    else
+        for i = 1, #lights do
+            SetShapeEmissiveScale(lights[i], 0)
+        end
+        for i=1, #lightsT do
+            SetShapeEmissiveScale(lightsT[i], 0)
+        end
+    end
+    for i=1, #blinkturnjoints do
+        SetJointMotor(blinkturnjoints[i], 10+i)
+    end
+
+    if pLightsA then
+        for i=1, #lightingA do
+            local l = lightingA[i]
+            local c = altlightcolor
+            SetLightColor(l,c[1],c[2],c[3])
+        end
+    else
+        for i=1, #lightingA do
+            local l = lightingA[i]
+            local c = altlightoriginalc[i]
+            SetLightColor(l,c[1],c[2],c[3])
+        end
+    end
+
+    if pLightsP then
+        for i = 1, #lightsP, 2 do
+            local l1 = lightsP[i]
+            local l2 = lightsP[i + 1]
+
+            if l1 then
+                local bp1Str = GetTagValue(l1, "blinkp") or "2,0.075,0.15,0.1,1"
+                local bp2Str = l2 and GetTagValue(l2, "blinkp") or "2,0.075,0.15,0.1,1"
+
+                local bp1 = split(bp1Str, ",")
+                local bp2 = split(bp2Str, ",")
+
+                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
+                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
+
+                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
+                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
+
+                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
+                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
+
+                local t = GetTime() + (i * 0.05)
+                local cD = math.max(cD1, cD2)
+                local c = t % cD
+
+                local s1, s2 = 0, 0
+
+                if simultaneous1 == 1 and simultaneous2 == 1 then
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = j * (fD2 + pB2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                else
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                end
+
+                SetShapeEmissiveScale(l1, s1)
+                if l2 then
+                    SetShapeEmissiveScale(l2, s2)
+                end
+            end
+        end
+    else
+        for i = 1, #lightsP do
+            SetShapeEmissiveScale(lightsP[i], 0)
+        end
+    end
+
+    if pLightsR then
+        for i = 1, #lightsR, 2 do
+            local l1 = lightsR[i]
+            local l2 = lightsR[i + 1]
+
+            if l1 then
+                local bp1Str = GetTagValue(l1, "blinkr") or "2,0.075,0.15,0.1,1"
+                local bp2Str = l2 and GetTagValue(l2, "blinkr") or "2,0.075,0.15,0.1,1"
+
+                local bp1 = split(bp1Str, ",")
+                local bp2 = split(bp2Str, ",")
+
+                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
+                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
+
+                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
+                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
+
+                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
+                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
+
+                local t = GetTime() + (i * 0.05)
+                local cD = math.max(cD1, cD2)
+                local c = t % cD
+
+                local s1, s2 = 0, 0
+
+                if simultaneous1 == 1 and simultaneous2 == 1 then
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = j * (fD2 + pB2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                else
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                end
+
+                SetShapeEmissiveScale(l1, s1)
+                if l2 then
+                    SetShapeEmissiveScale(l2, s2)
+                end
+            end
+        end
+    else
+        for i = 1, #lightsR do
+            SetShapeEmissiveScale(lightsR[i], 0)
+        end
+    end
+
+    if pLightsM then
+        for i = 1, #lightsM, 2 do
+            local l1 = lightsM[i]
+            local l2 = lightsM[i + 1]
+
+            if l1 then
+                local bp1Str = GetTagValue(l1, "blinkm") or "2,0.075,0.15,0.1,1"
+                local bp2Str = l2 and GetTagValue(l2, "blinkm") or "2,0.075,0.15,0.1,1"
+
+                local bp1 = split(bp1Str, ",")
+                local bp2 = split(bp2Str, ",")
+
+                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
+                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
+
+                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
+                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
+
+                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
+                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
+
+                local t = GetTime() + (i * 0.05)
+                local cD = math.max(cD1, cD2)
+                local c = t % cD
+
+                local s1, s2 = 0, 0
+
+                if simultaneous1 == 1 and simultaneous2 == 1 then
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = j * (fD2 + pB2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                else
+                    for j = 0, fC1 - 1 do
+                        local fS1 = j * (fD1 + pB1)
+                        if c >= fS1 and c < (fS1 + fD1) then
+                            s1 = 1
+                        end
+                    end
+
+                    for j = 0, fC2 - 1 do
+                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
+                        if c >= fS2 and c < (fS2 + fD2) then
+                            s2 = 1
+                        end
+                    end
+                end
+
+                SetShapeEmissiveScale(l1, s1)
+                if l2 then
+                    SetShapeEmissiveScale(l2, s2)
+                end
+            end
+        end
+        for i=1, #matrixscreens do
+            local h = matrixscreens[i]
+            if not IsScreenEnabled(h) then
+                SetScreenEnabled(h, true)
+            end
+        end
+        for i=1, #matrixjoints do
+            local j = matrixjoints[i]
+            SetJointMotor(j, -0.5)
+        end
+    else
+        for i = 1, #lightsM do
+            SetShapeEmissiveScale(lightsM[i], 0)
+        end
+        for i=1, #matrixscreens do
+            local h = matrixscreens[i]
+            if IsScreenEnabled(h) then
+                SetScreenEnabled(h, false)
+            end
+        end
+        for i=1, #matrixjoints do
+            local j = matrixjoints[i]
+            SetJointMotor(j, 0.5)
+        end
+    end
+    
+
+    -- Handle "blinks" lights behavior
+    if pLightsS then
+        for i = 1, #lightsS do
+            SetShapeEmissiveScale(lightsS[i], 3)  -- Set emission power to 3 when on
+        end
+    else
+        for i = 1, #lightsS do
+            SetShapeEmissiveScale(lightsS[i], 0)  -- Turn off the light
+        end
+    end
+
+    -- Handle "blinkh" lights behavior
+    if cLightsH then
+        for i = 1, #headlights do
+            SetShapeEmissiveScale(headlights[i], 3)  -- Set emission power to 3 when on
+        end
+    else
+        for i = 1, #headlights do
+            SetShapeEmissiveScale(headlights[i], 0)  -- Turn off the light
+        end
+    end
+
+    if cLightsHB then
+        for i = 1, #highbeamlights do
+            SetShapeEmissiveScale(highbeamlights[i], 3)  -- Set emission power to 3 when on
+        end
+    else
+        for i = 1, #highbeamlights do
+            SetShapeEmissiveScale(highbeamlights[i], 0)  -- Turn off the light
+        end
+    end
+
+    if clightsDTL then
+        if not (blinkdeactivate and cLightsBL) then
+            for i = 1, #daytimelights_l do
+                SetShapeEmissiveScale(daytimelights_l[i], 3)  -- Set emission power to 3 when on
+            end
+        end
+    else
+        for i = 1, #daytimelights_l do
+            SetShapeEmissiveScale(daytimelights_l[i], 0)  -- Turn off the light
+        end
+    end
+
+    if clightsDTR then
+        if not (blinkdeactivate and cLightsBR) then
+            for i = 1, #daytimelights_r do
+                SetShapeEmissiveScale(daytimelights_r[i], 3)  -- Set emission power to 3 when on
+            end
+        end
+    else
+        for i = 1, #daytimelights_r do
+            SetShapeEmissiveScale(daytimelights_r[i], 0)  -- Turn off the light
+        end
+    end
+    -- Handle "blinkb" lights behavior
+    if cLightsBL then
+        for i = 1, #daytimelights_l_l do
+            local l = daytimelights_l_l[i]
+            SetLightColor(l, 0.9, 0.7, 0.2)
+        end
+        for i = 1, #lightsBL do
+            local l = lightsBL[i]
+            local p = tonumber(GetTagValue(l, "blinkbl"))
+            if p then
+                local s = math.sin(GetTime() * p)
+                SetShapeEmissiveScale(l, s > 0 and 1 or 0)
+            end
+        end
+    else
+        if blinkdeactivate then
+            for i = 1, #daytimelights_l_l do
+                local l = daytimelights_l_l[i]
+                local c = colorDict[l]
+                SetLightColor(l, c[1], c[2], c[3])
+            end
+            for i = 1, #lightsBL do
+                if not (HasTag(lightsBL[i], "blinkdtr") or HasTag(lightsBL[i], "blinkdtl")) then
+                    SetShapeEmissiveScale(lightsBL[i], 0 > 0 and 1 or 0)
+                end
+            end
+        else
+            for i = 1, #lightsBL do
+                SetShapeEmissiveScale(lightsBL[i], 0 > 0 and 1 or 0)
+            end
+        end
+    end
+    if cLightsBR then
+        for i = 1, #daytimelights_r_l do
+            local l = daytimelights_r_l[i]
+            SetLightColor(l, 0.9, 0.7, 0.2)
+        end
+        for i = 1, #lightsBR do
+            local l = lightsBR[i]
+            local p = tonumber(GetTagValue(l, "blinkbr"))
+            if p then
+                local s = math.sin(GetTime() * p)
+                SetShapeEmissiveScale(l, s > 0 and 1 or 0)
+            end
+        end
+    else
+        if blinkdeactivate then
+            for i = 1, #daytimelights_r_l do
+                local l = daytimelights_r_l[i]
+                local c = colorDict[l]
+                SetLightColor(l, c[1], c[2], c[3])
+            end
+            for i = 1, #lightsBR do
+                if not (HasTag(lightsBR[i], "blinkdtr") or HasTag(lightsBR[i], "blinkdtr")) then
+                    SetShapeEmissiveScale(lightsBR[i], 0 > 0 and 1 or 0)
+                end
+            end
+        else
+            for i = 1, #lightsBR do
+                SetShapeEmissiveScale(lightsBR[i], 0 > 0 and 1 or 0)
+            end
+        end
+    end
+
+    -- Sirens behaviour
+    if siren_bool then
+        if pSirens1 and pLights then
+            if siren1_loop then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlayLoop(siren1, pos, siren1_vol)
+            else
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(siren1, pos, siren1_vol)
+                pSirens1 = false
+            end
+        elseif not pLights then
+            pSirens1 = false
+        end
+        if pSirens2 and pLights then
+            if siren2_loop then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlayLoop(siren2, pos, siren2_vol)
+            else
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(siren2, pos, siren2_vol)
+                pSirens2 = false
+            end
+        elseif not pLights then
+            pSirens2 = false
+        end
+        if pSirens3 and pLights then
+            if siren3_loop then
+                local pos = GetVehicleTransform(vehicle).pos
+                PlayLoop(siren3, pos, siren3_vol)
+            else
+                local pos = GetVehicleTransform(vehicle).pos
+                PlaySound(siren3, pos, siren3_vol)
+                pSirens3 = false
+            end
+        elseif not pLights then
+            pSirens3 = false
+        end
+    end
+
+    -- Config menu
+    if InputPressed(GetString("savegame.mod.keys.ui.togglecfg")) and (GetPlayerVehicle(playerId) == vehicle) then
+        config_menu_open = not config_menu_open
+    end
+end
+
+function reloadHead
+
+ghts()
+    if blinkdeactivate then
+        if cLightsBL and cLightsBR then
+            cLightsHFR = cLightsH
+            cLightsHFL = cLightsH
+        else
+            if cLightsBL then
+                cLightsHFL = false
+            else
+                cLightsHFL = cLightsH
+            end
+            if cLightsBR then
+                cLightsHFR = false
+            else
+                cLightsHFR = cLightsH
+            end
+        end
+    else
+        cLightsHFR = cLightsH
+        cLightsHFL = cLightsH
+    end
+end
+
+function addColorCo
+
+(handle, r, g, b)
+    colorDict[handle] = {r, g, b}
+end
+
+function reloadSire
+
+()
+    if siren_bool then
+        pSirens1 = false
+        pSirens2 = false
+        pSirens3 = false
+        if siren1_loop == true then
+            siren1 = LoadLoop(string.format("MOD/slf/snd/siren/snd/%s/%s/1.ogg", siren, siren_variant))
+        elseif siren1_loop == false then
+            siren1 = LoadSound(string.format("MOD/slf/snd/siren/snd/%s/%s/1.ogg", siren, siren_variant))
+        end
+        if siren2_loop == true then
+            siren2 = LoadLoop(string.format("MOD/slf/snd/siren/snd/%s/%s/2.ogg", siren, siren_variant))
+        elseif siren2_loop == false then
+            siren2 = LoadSound(string.format("MOD/slf/snd/siren/snd/%s/%s/2.ogg", siren, siren_variant))
+        end
+        if siren3_loop == true then
+            siren3 = LoadLoop(string.format("MOD/slf/snd/siren/snd/%s/%s/3.ogg", siren, siren_variant))
+        elseif siren3_loop == false then
+            siren3 = LoadSound(string.format("MOD/slf/snd/siren/snd/%s/%s/3.ogg", siren, siren_variant))
+        end
+    end
+end
+
+function server.init()
     initialize_keybinds()
     altlightcolor = Vec(altlightcolor_r,altlightcolor_g,altlightcolor_b)
     lightbody = FindBody("lightbody")
@@ -104,9 +1309,7 @@
     lightsP = FindShapes("blinkp")
     lightsA = FindShapes("blinka")
     lightingA = FindLights("altlight")
-
     blinkturnjoints = FindJoints("blinkturn")
-
     -- States to track whether each light group is on or off
     pLights = false
     pLightsR = false
@@ -124,24 +1327,17 @@
     pSirens1 = false
     pSirens2 = false
     pSirens3 = false
-
     -- Vehicle and sound setup
     vehicle = FindVehicle()
-    sound_beep = LoadSound("MOD/slf/snd/siren/siren_beep.ogg")
-    sound_click = LoadSound("MOD/slf/snd/button_click.ogg")
     reloadSirens()
     siren_list = {
-        
     }
-
-
     altlightoriginalc = {}
     for i=1, #lightingA do
         local l = lightingA[i]
         local c = GetProperty(l,"color")
         table.insert(altlightoriginalc,c)
     end
-
     -- voxshapes = GetEntityChildren(vehicle,"",true,"shape")
     -- voxshapes2 = GetEntityChildren(lightbody,"",true,"shape")
     -- for i=1, #voxshapes2 do
@@ -153,7 +1349,6 @@
     --     l = voxshapes[i]
     --     SetShapeCollisionFilter(l,2,253)
     -- end
-
     -- Honk vars
     if vehicletype == "car" then
         honksound = LoadLoop("MOD/slf/snd/car/horn/automobile.ogg")
@@ -162,11 +1357,8 @@
     else
         honksound = LoadLoop("MOD/slf/snd/car/horn/automobile.ogg")
     end
-
     -- UI initialization
     ui_stage = 2
-
-
     -- Configuration menu
     config_menu_open = false
     siren_list = {
@@ -308,1255 +1500,17 @@
         "road_closed",
         "arrow_right",
         "arrow_left",
-        
+
         "emergency_lane",
 
         "mtw",
-        
+
     }
     matrixboard_options_current = nil
 end
 
-function draw()
-    if GetPlayerVehicle() == vehicle then
-        if ui_stage == 1 then
-            -- Define the control information for the UI
-            local info = {
-                {"-- Car --",""},
-                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkh")), "Headlights"},
-                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkhb")), "High-Beams"},
-                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkdt")), "Daytime Lights"},
-                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkbr")), "Right Blinker"},
-                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkbl")), "Left Blinker"},
-                {string.format("[%s]",GetString("savegame.mod.keys.civ.blinkbh")), "Hazard Lights"},
-                {string.format("[%s]",GetString("savegame.mod.keys.civ.horn")), "Horn"},
-                {"", ""},
-                {"-- UI --",""},
-                {string.format("[%s]",GetString("savegame.mod.keys.ui.cycleui")), "Cycle UI"},
-                {string.format("[%s]",GetString("savegame.mod.keys.ui.togglecfg")), "Config Menu"}
-            }
-            if hastoplights or siren_bool or hasinfolights or hassurroundlights or hasrearlights or hasaltlights then
-                table.insert(info, {"", ""})
-                table.insert(info, {"-- ELS --", ""})
-            end
-            if hastoplights then
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blink")), "Lights"})
-            end
-            if haspowerlights then
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinkp")), "Additional"})
-            end
-            if siren_bool then
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.siren1")), "Siren 1"})
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.siren2")), "Siren 2"})
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.siren3")), "Siren 3"})
-            end
-            if hasinfolights then
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinkm")), "Signal"})
-            end
-            if hassurroundlights then
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinks")), "Scene"})
-            end
-            if hasrearlights then
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinkr")), "Directional"})
-            end
-            if hasaltlights then
-                table.insert(info, {string.format("[%s]",GetString("savegame.mod.keys.els.blinka")), "Toggle Color"})
-            end
-
-            UiPush()
-                UiAlign("top left")
-                local w = 200
-                local h = #info * 22 + 30
-                UiTranslate(20, UiHeight() - h - 20)
-                UiColor(0, 0, 0, 0.5)
-                UiImageBox("common/box-solid-6.png", 250, h, 6, 6)  -- Background box
-
-                UiTranslate(100, 32)
-                UiColor(1, 1, 1)
-                
-                -- Loop to draw each control item in the UI
-                for i = 1, #info do
-                    local key = info[i][1]
-                    local func = info[i][2]
-                    UiFont("bold.ttf", 22)
-                    UiAlign("right")
-                    UiText(key) 
-                    UiTranslate(10, 0)
-                    UiFont("regular.ttf", 22)
-                    UiAlign("left")
-                    UiText(func)
-                    UiTranslate(-10, 22)
-                end
-            UiPop()
-        elseif ui_stage == 3 then
-            UiColor(1, 1, 1, 1)
-            UiFont("regular.ttf", 26)
-            UiAlign("left top")
-            UiPush()
-                UiAlign("left bottom")
-                UiTranslate(10, UiHeight())
-                UiImage("MOD/slf/ui/interior/base/bg_base.png")
-            UiPop()
-            UiPush()
-                UiAlign("right bottom")
-                UiTranslate(300,UiHeight()-7)
-                if cLightsBL and cLightsBR then
-                    local activation = math.sin(GetTime() * tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
-                    if activation then
-                        UiImage("MOD/slf/ui/interior/base/hazard_on.png")
-                    else
-                        UiImage("MOD/slf/ui/interior/base/hazard_off.png")
-                    end
-                else
-                    UiImage("MOD/slf/ui/interior/base/hazard_off.png")
-                end
-            UiPop()
-            UiPush()
-                UiAlign("right bottom")
-                UiTranslate(197,UiHeight()-13)
-                if cLightsHB then
-                    UiImage("MOD/slf/ui/interior/base/headlight_highbeam.png")
-                elseif cLightsH then
-                    UiImage("MOD/slf/ui/interior/base/headlight_head.png")
-                elseif clightsDTL or clightsDTR then
-                    UiImage("MOD/slf/ui/interior/base/headlight_daylight.png")
-                else
-                    UiImage("MOD/slf/ui/interior/base/headlight_off.png")
-                end
-            UiPop()
-            UiPush()
-                UiAlign("right bottom")
-                UiTranslate(142,UiHeight()-11)
-                if cLightsBR then
-                    local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBR[1],"blinkbr"))) > 0
-                    if activation then
-                        UiImage("MOD/slf/ui/interior/base/indicator_right_on.png")
-                    else
-                        UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
-                    end
-                else
-                    UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
-                end
-                UiTranslate(-43, 0)
-                if cLightsBL then
-                    local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
-                    if activation then
-                        UiImage("MOD/slf/ui/interior/base/indicator_left_on.png")
-                    else
-                        UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
-                    end
-                else
-                    UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
-                end
-            UiPop()
-            UiPush()
-                UiTranslate(5,5)
-                UiAlign("left top")
-                UiFont("regular.ttf",24)
-                UiColor(1,1,1,0.75)
-                UiText(string.format("[%s] - Cycle UI",GetString("savegame.mod.keys.ui.cycleui")))
-                UiTranslate(0,20)
-                UiText(string.format("[%s] - Config Menu",GetString("savegame.mod.keys.ui.togglecfg")))
-            UiPop()
-        elseif ui_stage == 2 then
-            UiColor(1,1,1,1)
-            UiAlign("left top")
-            UiFont("regular.ttf",26)
-            local buttons = 0
-            if siren_bool then
-                buttons = buttons + 2
-            end
-            if hastoplights then
-                buttons = buttons + 1
-            end
-            if hasrearlights then
-                buttons = buttons + 1
-            end
-            if hasinfolights then
-                buttons = buttons + 1
-            end
-            if hassurroundlights then
-                buttons = buttons + 1
-            end
-            if haspowerlights then
-                buttons = buttons + 1
-            end
-            if hasaltlights then
-                buttons = buttons + 1
-            end
-            local rows = math.ceil(buttons/4)
-            if rows == 0 then
-                ui_stage = 3
-            else
-                UiPush()
-                    UiAlign("left bottom")
-                    UiTranslate(10,UiHeight()-10)
-                    UiImage(string.format("MOD/slf/ui/interior/els/bg_els_rows%s.png",tostring(rows)))
-                UiPop()
-
-                -- Civilian Vehicle Functions
-                UiColor(1, 1, 1, 1)
-                UiFont("regular.ttf", 26)
-                UiAlign("left top")
-                UiPush()
-                    UiAlign("right bottom")
-                    UiTranslate(300,UiHeight()-7-((rows*(60+10))+10+35+10+5))
-                    if cLightsBL and cLightsBR then
-                        local activation = math.sin(GetTime() * tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
-                        if activation then
-                            UiImage("MOD/slf/ui/interior/base/hazard_on.png")
-                        else
-                            UiImage("MOD/slf/ui/interior/base/hazard_off.png")
-                        end
-                    else
-                        UiImage("MOD/slf/ui/interior/base/hazard_off.png")
-                    end
-                UiPop()
-                UiPush()
-                    UiAlign("right bottom")
-                    UiTranslate(197,UiHeight()-13-((rows*(60+10))+10+35+10+5))
-                    if cLightsHB then
-                        UiImage("MOD/slf/ui/interior/base/headlight_highbeam.png")
-                    elseif cLightsH then
-                        UiImage("MOD/slf/ui/interior/base/headlight_head.png")
-                    elseif clightsDTL or clightsDTR then
-                        UiImage("MOD/slf/ui/interior/base/headlight_daylight.png")
-                    else
-                        UiImage("MOD/slf/ui/interior/base/headlight_off.png")
-                    end
-                UiPop()
-                UiPush()
-                    UiAlign("right bottom")
-                    UiTranslate(142,UiHeight()-11-((rows*(60+10))+10+35+10+5))
-                    if cLightsBR then
-                        local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBR[1],"blinkbr"))) > 0
-                        if activation then
-                            UiImage("MOD/slf/ui/interior/base/indicator_right_on.png")
-                        else
-                            UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
-                        end
-                    else
-                        UiImage("MOD/slf/ui/interior/base/indicator_right_off.png")
-                    end
-                    UiTranslate(-43, 0)
-                    if cLightsBL then
-                        local activation = math.sin(GetTime()*tonumber(GetTagValue(lightsBL[1],"blinkbl"))) > 0
-                        if activation then
-                            UiImage("MOD/slf/ui/interior/base/indicator_left_on.png")
-                        else
-                            UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
-                        end
-                    else
-                        UiImage("MOD/slf/ui/interior/base/indicator_left_off.png")
-                    end
-                UiPop()
-
-                -- Cycle Sign
-                UiPush()
-                    UiTranslate(25,UiHeight()-((rows*(60+10))+15+35+10))
-                    UiAlign("left top")
-                    UiFont("regular.ttf",18)
-                    UiColor(0.8,0.8,0.8,0.5)
-                    UiText(string.format("[%s] - Cycle UI",GetString("savegame.mod.keys.ui.cycleui")))
-                    UiTranslate(0,18)
-                    UiText(string.format("[%s] - Config Menu",GetString("savegame.mod.keys.ui.togglecfg")))
-                UiPop()
-                local functions = {
-                    { siren_bool, (pSirens1 or pSirens2 or pSirens3) and "MOD/slf/ui/interior/els/button_siren_on.png" or "MOD/slf/ui/interior/els/button_siren_off.png", 2, {1,1,1,1}},
-                    { hastoplights, pLights and "MOD/slf/ui/interior/els/button_toplight_on.png" or "MOD/slf/ui/interior/els/button_toplight_off.png", 1, {1,1,1,1}},
-                    { hasrearlights, pLightsR and "MOD/slf/ui/interior/els/button_directional_on.png" or "MOD/slf/ui/interior/els/button_directional_off.png", 1, {1,1,1,1}},
-                    { hassurroundlights, pLightsS and "MOD/slf/ui/interior/els/button_scene_on.png" or "MOD/slf/ui/interior/els/button_scene_off.png", 1, {1,1,1,1}},
-                    { hasinfolights, pLightsM and "MOD/slf/ui/interior/els/button_signal_on.png" or "MOD/slf/ui/interior/els/button_signal_off.png", 1, {1,1,1,1}},
-                    { haspowerlights, pLightsP and "MOD/slf/ui/interior/els/button_additional_on.png" or "MOD/slf/ui/interior/els/button_additional_off.png", 1, {1,1,1,1}},
-                    { hasaltlights, pLightsA and "MOD/slf/ui/interior/els/button_altcolor_on.png" or "MOD/slf/ui/interior/els/button_altcolor_off.png", 1, pLightsA and {altlightcolor_r,altlightcolor_g,altlightcolor_b,1} or {1,1,1,1}},
-                }
-                local deltapos = 0
-                local position = 1
-                for i=1, #functions do
-                    local info = functions[i]
-                    if info[1] then
-                        local row = math.ceil(position/4)
-                        local column = position-((row-1)*(row>1 and 4 or 0))
-                        UiPush()
-                            UiTranslate(25,UiHeight()-((rows*(60+10))+10+5))
-                            UiAlign("left top")
-                            UiColor(info[4][1],info[4][2],info[4][3],info[4][4])
-                            UiTranslate((column-1)*70,(row-1)*70)
-                            UiTranslate(-10,-10)
-                            UiImage(info[2])
-                            position = position + info[3]
-                            deltapos = info[3]
-                            UiColor(1,1,1,1)
-                        UiPop()
-                    end
-                end
-
-                UiPush()
-                UiPop()
-            end
-        end
-    end
-    if (GetPlayerVehicle() == vehicle) and config_menu_open then
-        -- Column 1 : Sirens
-        UiMakeInteractive()
-        UiPush()
-            UiAlign("left top")
-            UiColor(1,1,1,1)
-            UiFont("regular.ttf",24)
-            UiTranslate(10,10)
-            UiText("Sirens")
-            UiTranslate(0,20)
-            for i=1, #siren_list do
-                if siren == siren_list[i][1] then
-                    UiColor(0,1,0,1)
-                end
-                if UiTextButton(siren_list[i][1]:gsub("^%l", string.upper), 50, 20) then
-                    siren = siren_list[i][1]
-                    siren_variant = siren_list[i][2][1]
-                    reloadSirens()
-                end
-                UiColor(1,1,1,1)
-                UiTranslate(0, 30)
-            end
-        UiPop()
-        -- Column 2 : Siren Variants
-        UiPush()
-            UiAlign("left top")
-            UiColor(1,1,1,1)
-            UiFont("regular.ttf",24)
-            UiTranslate(110,10)
-            UiText("Siren Variants")
-            UiTranslate(0,20)
-            for i=1, #siren_list do
-                if siren == siren_list[i][1] then
-                    for x=1, #siren_list[i][2] do
-                        if siren_variant == siren_list[i][2][x] then
-                            UiColor(0,1,0,1)
-                        end
-                        if UiTextButton(siren_list[i][2][x]:gsub("^%l", string.upper), 50, 20) then
-                            siren_variant = siren_list[i][2][x]
-                            reloadSirens()
-                        end
-                        UiColor(1,1,1,1)
-                        UiTranslate(0, 30)
-                    end
-                end
-            end
-        UiPop()
-        -- Column 3 : Loop Sirens
-        UiPush()
-            UiAlign("left top")
-            UiColor(1,1,1,1)
-            UiFont("regular.ttf",24)
-            UiTranslate(310,10)
-            UiText("Siren Loops")
-            UiTranslate(0,20)
-            -- Siren 1
-            if siren1_loop then UiColor(0,1,0,1) end
-            if UiTextButton("Loop Siren 1", 50, 20) then
-                siren1_loop = not siren1_loop
-                reloadSirens()
-            end
-            UiColor(1,1,1,1)
-            UiTranslate(0, 30)
-            -- Siren 2
-            if siren2_loop then UiColor(0,1,0,1) end
-            if UiTextButton("Loop Siren 2", 50, 20) then
-                siren2_loop = not siren2_loop
-                reloadSirens()
-            end
-            UiColor(1,1,1,1)
-            UiTranslate(0, 30)
-            -- Siren 3
-            if siren3_loop then UiColor(0,1,0,1) end
-            if UiTextButton("Loop Siren 3", 50, 20) then
-                siren3_loop = not siren3_loop
-                reloadSirens()
-            end
-            UiColor(1,1,1,1)
-            UiTranslate(0, 30)
-        UiPop()
-        -- Column 4 : Matrix Display
-        -- Language
-        UiPush()
-            UiAlign("left top")
-            UiColor(1,1,1,1)
-            UiFont("regular.ttf",24)
-            UiTranslate(510,10)
-            UiText("Matrix Language")
-            UiTranslate(0,20)
-            for i=1, #matrix_options_textbased do
-                if matrix_options_textbased[i][1] == matrix_ln then UiColor(0,1,0,1) end
-                if UiTextButton(matrix_options_textbased[i][1]:gsub("^%l", string.upper)) then
-                    matrix_ln = matrix_options_textbased[i][1]
-                end
-                UiColor(1,1,1,1)
-                UiTranslate(0, 30)
-            end
-        UiPop()
-        -- Select
-        matrix_ln_options = nil
-        for i=1, #matrix_options_textbased do
-            if matrix_ln == matrix_options_textbased[i][1] then
-                matrix_ln_options = matrix_options_textbased[i][2]
-            end
-        end
-        UiPush()
-            UiAlign("left top")
-            UiColor(1,1,1,1)
-            UiFont("regular.ttf",24)
-            UiTranslate(710,10)
-            UiText("Matrix Options")
-            UiTranslate(0,20)
-            for i=1, #matrix_ln_options do
-                if matrix_options_current == matrix_ln_options[i][1] then UiColor(0,1,0,1) end
-                if UiTextButton(matrix_ln_options[i][1]) then
-                    for x=1, #matrixscreens do
-                        local screen = matrixscreens[x]
-                        if not (HasTag(screen, "matrixboard") or HasTag(screen, "screenignore"))then
-                            local info = split(GetTagValue(screen, "matrixscreen"),";")
-                            info[2] = matrix_ln_options[i][2]
-                            SetTag(screen, "matrixscreen", table.concat(info, ";"))
-                            
-                        end
-                    end
-                    matrix_options_current = matrix_ln_options[i][1]
-                    
-                end
-                UiColor(1,1,1,1)
-                UiTranslate(0,30)
-            end
-        UiPop()
-
-        -- Column 5 : Matrixboard Image
-        UiPush()
-            UiAlign("left top")
-            UiColor(1,1,1,1)
-            UiFont("regular.ttf",24)
-            UiTranslate(910,10)
-            UiText("Matrix Options")
-            UiTranslate(0,20)
-            for i=1, #matrixboard_options do
-                if matrixboard_options_current == matrixboard_options[i] then UiColor(0,1,0,1) end
-                if UiTextButton(matrixboard_options[i]) then
-                    for x=1, #matrixscreens do
-                        screen = matrixscreens[x]
-                        if HasTag(screen, "matrixboard") then
-                            SetTag(screen, "matrixscreen", string.format("MOD/slf/img/matrixboard/%s.png",matrixboard_options[i]))
-                        end
-                    end
-                    matrixboard_options_current = matrixboard_options[i]
-                    
-                end
-                UiColor(1,1,1,1)
-                UiTranslate(0,30)
-            end
-        UiPop()
-
-
-        -- (Column 6 : Matrixboard Behaviour)
-    end
+function client.init()
+    sound_beep = LoadSound("MOD/slf/snd/siren/siren_beep.ogg")
+    sound_click = LoadSound("MOD/slf/snd/button_click.ogg")
 end
 
-function tick(dt)
-    -- Toggle the lights based on inputs
-    if InputPressed(GetString("savegame.mod.keys.ui.cycleui")) then
-        if GetPlayerVehicle() == vehicle then
-            if ui_stage < 3 then
-                ui_stage = ui_stage + 1
-            else
-                ui_stage = 1
-            end
-        end
-    end
-    -- ELS functions
-    if hastoplights then
-        if InputPressed(GetString("savegame.mod.keys.els.blink")) then
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-
-                -- Toggle "blink" lights
-                pLights = not pLights
-                if switchlights then
-                    pLightsR = false
-                end
-            end
-        end
-    end
-
-    if hasrearlights then
-        if InputPressed(GetString("savegame.mod.keys.els.blinkr")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-
-                -- Toggle "blinkr" lights
-                pLightsR = not pLightsR
-                if switchlights then
-                    pLights = false
-                end
-            end
-        end
-    end
-
-    if hasinfolights then
-        if InputPressed(GetString("savegame.mod.keys.els.blinkm")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-
-                -- Toggle "blinkm" lights
-                pLightsM = not pLightsM
-            end
-        end
-    end
-
-    if hassurroundlights then
-        if InputPressed(GetString("savegame.mod.keys.els.blinks")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-
-                -- Toggle "blinks" lights
-                pLightsS = not pLightsS
-            end
-        end
-    end
-
-    if haspowerlights then
-        if pLights or pLightsM then
-            if InputPressed(GetString("savegame.mod.keys.els.blinkp")) then
-                if GetPlayerVehicle() == vehicle then
-                    local pos = GetVehicleTransform(vehicle).pos
-                    PlaySound(sound_beep, pos, 100)
-
-                    -- Toggle "blinkp" lights
-                    pLightsP = not pLightsP
-                end
-            end
-        else
-            pLightsP = false
-        end
-    end
-
-    if hasaltlights then
-        if InputPressed(GetString("savegame.mod.keys.els.blinka")) then
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-
-                pLights = true
-                pLightsA = not pLightsA
-            end
-        end
-    end
-    -- Civilian functions
-    if cLightsDTM then
-        if InputPressed(GetString("savegame.mod.keys.civ.blinkh")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_click, pos, 100)
-
-                -- Toggle "blinkh" lights
-                cLightsH = not cLightsH
-
-            end
-        end
-    else
-        cLightsH = false
-    end
-    if cLightsH then
-        if InputPressed(GetString("savegame.mod.keys.civ.blinkhb")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_click, pos, 100)
-
-                -- Toggle "blinkhb" lights
-                cLightsHB = not cLightsHB
-
-            end
-        end
-    else
-        cLightsHB = false
-    end
-    if GetPlayerVehicle() == vehicle then
-        -- Toggle "blinkdt" lights
-        if cLightsDTM then
-            if blinkdeactivate then
-                if cLightsBL then
-                    clightsDTL = false
-                else
-                    clightsDTL = true
-                end
-                if cLightsBR then
-                    clightsDTR = false
-                else
-                    clightsDTR = true
-                end
-            else
-                clightsDTL = true
-                clightsDTR = true
-            end
-        else
-            clightsDTL = false
-            clightsDTR = false
-        end
-    end
-    if InputPressed(GetString("savegame.mod.keys.civ.blinkdt")) then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
-            local pos = GetVehicleTransform(vehicle).pos
-            PlaySound(sound_click, pos, 100)
-
-            cLightsDTM = not cLightsDTM
-        end
-    end
-
-    if InputPressed(GetString("savegame.mod.keys.civ.blinkbr")) then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
-            local pos = GetVehicleTransform(vehicle).pos
-            PlaySound(sound_click, pos, 100)
-
-            -- Toggle "blinkbr" lights
-            if not (cLightsBL and cLightsBR) then
-                cLightsBL = false
-                cLightsBR = not cLightsBR
-            else
-                cLightsBL = false
-                cLightsBR = true
-            end
-        end
-    end
-    if InputPressed(GetString("savegame.mod.keys.civ.blinkbl")) then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
-            local pos = GetVehicleTransform(vehicle).pos
-            PlaySound(sound_click, pos, 100)
-
-            -- Toggle "blinkbl" lights
-            if not (cLightsBL and cLightsBR) then
-                cLightsBR = false
-                cLightsBL = not cLightsBL
-            else
-                cLightsBR = false
-                cLightsBL = true
-            end
-            reloadHeadlights()
-        end
-    end
-    if InputPressed(GetString("savegame.mod.keys.civ.blinkbh")) then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
-            local pos = GetVehicleTransform(vehicle).pos
-            PlaySound(sound_click, pos, 100)
-
-            -- Toggle "blinkbr and bl" lights
-            if cLightsBR and cLightsBL then
-                cLightsBL = false
-                cLightsBR = false
-            else
-                cLightsBL = true
-                cLightsBR = true
-            end
-            reloadHeadlights()
-        end
-    end
-    if InputDown(GetString("savegame.mod.keys.civ.horn")) then  -- You can change this keybinding to suit your preferences
-        if GetPlayerVehicle() == vehicle then
-            local pos = GetVehicleTransform(vehicle).pos
-            
-            PlayLoop(honksound, pos, 100)
-        end
-    end
-    -- Sirens detection
-    if siren_bool and pLights then
-        if InputPressed(GetString("savegame.mod.keys.els.siren1")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-                if siren1_loop then
-                    pSirens1 = not pSirens1
-                    pSirens2 = false
-                    pSirens3 = false
-                else
-                    pSirens1 = true
-                end
-            end
-        end
-        if InputPressed(GetString("savegame.mod.keys.els.siren2")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-                if siren2_loop then
-                    pSirens2 = not pSirens2
-                    pSirens1 = false
-                    pSirens3 = false
-                else
-                    pSirens2 = true
-                end
-            end
-        end
-        if InputPressed(GetString("savegame.mod.keys.els.siren3")) then  -- You can change this keybinding to suit your preferences
-            if GetPlayerVehicle() == vehicle then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(sound_beep, pos, 100)
-                if siren3_loop then
-                    pSirens3 = not pSirens3
-                    pSirens2 = false
-                    pSirens1 = false
-                else
-                    pSirens3 = true
-                end
-            end
-        end
-    end
-    
-    -- Light behaviour
-
-    if pLights then
-        for i = 1, #lights, 2 do
-            local l1 = lights[i]
-            local l2 = lights[i + 1]
-
-            if l1 then
-                local bp1Str = GetTagValue(l1, "blink") or "2,0.075,0.15,0.1,1"
-                local bp2Str = l2 and GetTagValue(l2, "blink") or "2,0.075,0.15,0.1,1"
-
-                local bp1 = split(bp1Str, ",")
-                local bp2 = split(bp2Str, ",")
-
-                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
-                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
-
-                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
-                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
-
-                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
-                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
-
-                local t = GetTime() + (i * 0.05)
-                local cD = math.max(cD1, cD2)
-                local c = t % cD
-
-                local s1, s2 = 0, 0
-
-                if simultaneous1 == 1 and simultaneous2 == 1 then
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = j * (fD2 + pB2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                else
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                end
-                
-                s1 = HasTag(l1, "reverseblink") and (1-s1) or s1
-                s2 = HasTag(l2, "reverseblink") and (1-s2) or s2
-
-                local altl1 = HasTag(l1,"blinka")
-                if not pLightsA or altl1 then
-                    SetShapeEmissiveScale(l1, s1)
-                else
-                    SetShapeEmissiveScale(l1, 0)
-                end
-                if l2 then
-                    local altl2 = HasTag(l2,"blinka")
-                    if not pLightsA or altl2 then
-                        SetShapeEmissiveScale(l2, s2)
-                    else
-                        SetShapeEmissiveScale(l2, 0)
-                    end
-                end
-            end
-        end
-        for i=1, #lightsT do
-            SetShapeEmissiveScale(lightsT[i], 1)
-        end
-    else
-        for i = 1, #lights do
-            SetShapeEmissiveScale(lights[i], 0)
-        end
-        for i=1, #lightsT do
-            SetShapeEmissiveScale(lightsT[i], 0)
-        end
-    end
-    for i=1, #blinkturnjoints do
-        SetJointMotor(blinkturnjoints[i], 10+i)
-    end
-
-    if pLightsA then
-        for i=1, #lightingA do
-            local l = lightingA[i]
-            local c = altlightcolor
-            SetLightColor(l,c[1],c[2],c[3])
-        end
-    else
-        for i=1, #lightingA do
-            local l = lightingA[i]
-            local c = altlightoriginalc[i]
-            SetLightColor(l,c[1],c[2],c[3])
-        end
-    end
-
-    if pLightsP then
-        for i = 1, #lightsP, 2 do
-            local l1 = lightsP[i]
-            local l2 = lightsP[i + 1]
-
-
-            if l1 then
-                local bp1Str = GetTagValue(l1, "blinkp") or "2,0.075,0.15,0.1,1"
-                local bp2Str = l2 and GetTagValue(l2, "blinkp") or "2,0.075,0.15,0.1,1"
-
-                local bp1 = split(bp1Str, ",")
-                local bp2 = split(bp2Str, ",")
-
-                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
-                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
-
-                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
-                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
-
-                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
-                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
-
-                local t = GetTime() + (i * 0.05)
-                local cD = math.max(cD1, cD2)
-                local c = t % cD
-
-                local s1, s2 = 0, 0
-
-                if simultaneous1 == 1 and simultaneous2 == 1 then
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = j * (fD2 + pB2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                else
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                end
-
-                SetShapeEmissiveScale(l1, s1)
-                if l2 then
-                    SetShapeEmissiveScale(l2, s2)
-                end
-            end
-        end
-    else
-        for i = 1, #lightsP do
-            SetShapeEmissiveScale(lightsP[i], 0)
-        end
-    end
-
-    if pLightsR then
-        for i = 1, #lightsR, 2 do
-            local l1 = lightsR[i]
-            local l2 = lightsR[i + 1]
-
-            if l1 then
-                local bp1Str = GetTagValue(l1, "blinkr") or "2,0.075,0.15,0.1,1"
-                local bp2Str = l2 and GetTagValue(l2, "blinkr") or "2,0.075,0.15,0.1,1"
-
-                local bp1 = split(bp1Str, ",")
-                local bp2 = split(bp2Str, ",")
-
-                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
-                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
-
-                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
-                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
-
-                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
-                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
-
-                local t = GetTime() + (i * 0.05)
-                local cD = math.max(cD1, cD2)
-                local c = t % cD
-
-                local s1, s2 = 0, 0
-
-                if simultaneous1 == 1 and simultaneous2 == 1 then
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = j * (fD2 + pB2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                else
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                end
-
-                SetShapeEmissiveScale(l1, s1)
-                if l2 then
-                    SetShapeEmissiveScale(l2, s2)
-                end
-            end
-        end
-    else
-        for i = 1, #lightsR do
-            SetShapeEmissiveScale(lightsR[i], 0)
-        end
-    end
-
-
-    if pLightsM then
-        for i = 1, #lightsM, 2 do
-            local l1 = lightsM[i]
-            local l2 = lightsM[i + 1]
-
-            if l1 then
-                local bp1Str = GetTagValue(l1, "blinkm") or "2,0.075,0.15,0.1,1"
-                local bp2Str = l2 and GetTagValue(l2, "blinkm") or "2,0.075,0.15,0.1,1"
-
-                local bp1 = split(bp1Str, ",")
-                local bp2 = split(bp2Str, ",")
-
-                for k = 1, #bp1 do bp1[k] = tonumber(bp1[k]) end
-                for k = 1, #bp2 do bp2[k] = tonumber(bp2[k]) end
-
-                local fC1, fD1, pB1, pG1, simultaneous1 = bp1[1], bp1[2], bp1[3], bp1[4], bp1[5] or 0
-                local fC2, fD2, pB2, pG2, simultaneous2 = l2 and bp2[1] or 0, l2 and bp2[2] or 0, l2 and bp2[3] or 0, l2 and bp2[4] or 0, l2 and bp2[5] or 0
-
-                local cD1 = (fC1 * (fD1 + pB1) * 2) + (2 * pG1)
-                local cD2 = (fC2 * (fD2 + pB2) * 2) + (2 * pG2)
-
-                local t = GetTime() + (i * 0.05)
-                local cD = math.max(cD1, cD2)
-                local c = t % cD
-
-                local s1, s2 = 0, 0
-
-                if simultaneous1 == 1 and simultaneous2 == 1 then
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = j * (fD2 + pB2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                else
-                    for j = 0, fC1 - 1 do
-                        local fS1 = j * (fD1 + pB1)
-                        if c >= fS1 and c < (fS1 + fD1) then
-                            s1 = 1
-                        end
-                    end
-
-                    for j = 0, fC2 - 1 do
-                        local fS2 = (j * (fD2 + pB2)) + (cD / 2)
-                        if c >= fS2 and c < (fS2 + fD2) then
-                            s2 = 1
-                        end
-                    end
-                end
-
-                SetShapeEmissiveScale(l1, s1)
-                if l2 then
-                    SetShapeEmissiveScale(l2, s2)
-                end
-            end
-        end
-        for i=1, #matrixscreens do
-            local h = matrixscreens[i]
-            if not IsScreenEnabled(h) then
-                SetScreenEnabled(h, true)
-            end
-        end
-        for i=1, #matrixjoints do
-            local j = matrixjoints[i]
-            SetJointMotor(j, -0.5)
-        end
-    else
-        for i = 1, #lightsM do
-            SetShapeEmissiveScale(lightsM[i], 0)
-        end
-        for i=1, #matrixscreens do
-            local h = matrixscreens[i]
-            if IsScreenEnabled(h) then
-                SetScreenEnabled(h, false)
-            end
-        end
-        for i=1, #matrixjoints do
-            local j = matrixjoints[i]
-            SetJointMotor(j, 0.5)
-        end
-    end
-    
-
-    -- Handle "blinks" lights behavior
-    if pLightsS then
-        for i = 1, #lightsS do
-            SetShapeEmissiveScale(lightsS[i], 3)  -- Set emission power to 3 when on
-        end
-    else
-        for i = 1, #lightsS do
-            SetShapeEmissiveScale(lightsS[i], 0)  -- Turn off the light
-        end
-    end
-
-    -- Handle "blinkh" lights behavior
-    if cLightsH then
-        for i = 1, #headlights do
-            SetShapeEmissiveScale(headlights[i], 3)  -- Set emission power to 3 when on
-        end
-    else
-        for i = 1, #headlights do
-            SetShapeEmissiveScale(headlights[i], 0)  -- Turn off the light
-        end
-    end
-
-    if cLightsHB then
-        for i = 1, #highbeamlights do
-            SetShapeEmissiveScale(highbeamlights[i], 3)  -- Set emission power to 3 when on
-        end
-    else
-        for i = 1, #highbeamlights do
-            SetShapeEmissiveScale(highbeamlights[i], 0)  -- Turn off the light
-        end
-    end
-
-    if clightsDTL then
-        if not (blinkdeactivate and cLightsBL) then
-            for i = 1, #daytimelights_l do
-                SetShapeEmissiveScale(daytimelights_l[i], 3)  -- Set emission power to 3 when on
-            end
-        end
-    else
-        for i = 1, #daytimelights_l do
-            SetShapeEmissiveScale(daytimelights_l[i], 0)  -- Turn off the light
-        end
-    end
-
-    if clightsDTR then
-        if not (blinkdeactivate and cLightsBR) then
-            for i = 1, #daytimelights_r do
-                SetShapeEmissiveScale(daytimelights_r[i], 3)  -- Set emission power to 3 when on
-            end
-        end
-    else
-        for i = 1, #daytimelights_r do
-            SetShapeEmissiveScale(daytimelights_r[i], 0)  -- Turn off the light
-        end
-    end
-    -- Handle "blinkb" lights behavior
-    if cLightsBL then
-        for i = 1, #daytimelights_l_l do
-            local l = daytimelights_l_l[i]
-            SetLightColor(l, 0.9, 0.7, 0.2)
-        end
-        for i = 1, #lightsBL do
-            local l = lightsBL[i]
-            local p = tonumber(GetTagValue(l, "blinkbl"))
-            if p then
-                local s = math.sin(GetTime() * p)
-                SetShapeEmissiveScale(l, s > 0 and 1 or 0)
-            end
-        end
-    else
-        if blinkdeactivate then
-            for i = 1, #daytimelights_l_l do
-                local l = daytimelights_l_l[i]
-                local c = colorDict[l]
-                SetLightColor(l, c[1], c[2], c[3])
-            end
-            for i = 1, #lightsBL do
-                if not (HasTag(lightsBL[i], "blinkdtr") or HasTag(lightsBL[i], "blinkdtl")) then
-                    SetShapeEmissiveScale(lightsBL[i], 0 > 0 and 1 or 0)
-                end
-            end
-        else
-            for i = 1, #lightsBL do
-                SetShapeEmissiveScale(lightsBL[i], 0 > 0 and 1 or 0)
-            end
-        end
-    end
-    if cLightsBR then
-        for i = 1, #daytimelights_r_l do
-            local l = daytimelights_r_l[i]
-            SetLightColor(l, 0.9, 0.7, 0.2)
-        end
-        for i = 1, #lightsBR do
-            local l = lightsBR[i]
-            local p = tonumber(GetTagValue(l, "blinkbr"))
-            if p then
-                local s = math.sin(GetTime() * p)
-                SetShapeEmissiveScale(l, s > 0 and 1 or 0)
-            end
-        end
-    else
-        if blinkdeactivate then
-            for i = 1, #daytimelights_r_l do
-                local l = daytimelights_r_l[i]
-                local c = colorDict[l]
-                SetLightColor(l, c[1], c[2], c[3])
-            end
-            for i = 1, #lightsBR do
-                if not (HasTag(lightsBR[i], "blinkdtr") or HasTag(lightsBR[i], "blinkdtr")) then
-                    SetShapeEmissiveScale(lightsBR[i], 0 > 0 and 1 or 0)
-                end
-            end
-        else
-            for i = 1, #lightsBR do
-                SetShapeEmissiveScale(lightsBR[i], 0 > 0 and 1 or 0)
-            end
-        end
-    end
-
-    -- Sirens behaviour
-    if siren_bool then
-        if pSirens1 and pLights then
-            if siren1_loop then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlayLoop(siren1, pos, siren1_vol)
-            else
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(siren1, pos, siren1_vol)
-                pSirens1 = false
-            end
-        elseif not pLights then
-            pSirens1 = false
-        end
-        if pSirens2 and pLights then
-            if siren2_loop then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlayLoop(siren2, pos, siren2_vol)
-            else
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(siren2, pos, siren2_vol)
-                pSirens2 = false
-            end
-        elseif not pLights then
-            pSirens2 = false
-        end
-        if pSirens3 and pLights then
-            if siren3_loop then
-                local pos = GetVehicleTransform(vehicle).pos
-                PlayLoop(siren3, pos, siren3_vol)
-            else
-                local pos = GetVehicleTransform(vehicle).pos
-                PlaySound(siren3, pos, siren3_vol)
-                pSirens3 = false
-            end
-        elseif not pLights then
-            pSirens3 = false
-        end
-    end
-
-    -- Config menu
-    if InputPressed(GetString("savegame.mod.keys.ui.togglecfg")) and (GetPlayerVehicle() == vehicle) then
-        config_menu_open = not config_menu_open
-    end
-end
-
-function reloadHeadlights()
-    if blinkdeactivate then
-        if cLightsBL and cLightsBR then
-            cLightsHFR = cLightsH
-            cLightsHFL = cLightsH
-        else
-            if cLightsBL then
-                cLightsHFL = false
-            else
-                cLightsHFL = cLightsH
-            end
-            if cLightsBR then
-                cLightsHFR = false
-            else
-                cLightsHFR = cLightsH
-            end
-        end
-    else
-        cLightsHFR = cLightsH
-        cLightsHFL = cLightsH
-    end
-end
-
-function addColorCode(handle, r, g, b)
-    colorDict[handle] = {r, g, b}
-end
-
-function reloadSirens()
-    if siren_bool then
-        pSirens1 = false
-        pSirens2 = false
-        pSirens3 = false
-        if siren1_loop == true then
-            siren1 = LoadLoop(string.format("MOD/slf/snd/siren/snd/%s/%s/1.ogg", siren, siren_variant))
-        elseif siren1_loop == false then
-            siren1 = LoadSound(string.format("MOD/slf/snd/siren/snd/%s/%s/1.ogg", siren, siren_variant))
-        end
-        if siren2_loop == true then
-            siren2 = LoadLoop(string.format("MOD/slf/snd/siren/snd/%s/%s/2.ogg", siren, siren_variant))
-        elseif siren2_loop == false then
-            siren2 = LoadSound(string.format("MOD/slf/snd/siren/snd/%s/%s/2.ogg", siren, siren_variant))
-        end
-        if siren3_loop == true then
-            siren3 = LoadLoop(string.format("MOD/slf/snd/siren/snd/%s/%s/3.ogg", siren, siren_variant))
-        elseif siren3_loop == false then
-            siren3 = LoadSound(string.format("MOD/slf/snd/siren/snd/%s/%s/3.ogg", siren, siren_variant))
-        end
-    end
-end
```
