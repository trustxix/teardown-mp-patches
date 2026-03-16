# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,216 +1,4 @@
--- MAIN FUNCTIONS --
-
-function init()
-    RegisterTool("liquify", "Liquify", "MOD/vox/hand.vox")
-    SetBool("game.tool.liquify.enabled", true)
-    drawOptions = false
-
-    -- weapon variables
-    voxels = {}
-    limit = 10000
-    drawModel = true
-    gravity = true
-
-    -- saved variables
-    if HasKey("savegame.mod.liquify.limit") then limit = GetFloat("savegame.mod.liquify.limit") end
-    if HasKey("savegame.mod.liquify.drawModel") then drawModel = GetBool("savegame.mod.liquify.drawModel") end
-
-    -- sound variables
-    snap = LoadSound("MOD/snd/snap.ogg")
-
-    -- animation variables
-    liquifying = false
-    called = false
-    liquifyT = 0
-    animations = {}
-    armAnimation = animation()
-    armFrontT = Transform(Vec(-1,-0.8,-0.9), QuatRotateQuat(QuatEuler(50,-10, 0), QuatEuler(0,0,140)))
-    armInvisibleT = Transform(Vec(110,110,100), QuatEuler(-90, 0,0))
-    addKeyframe(armAnimation, 0.0, armFrontT)
-    addKeyframe(armAnimation, 0.7, armFrontT)
-    snapKeyframes = {
-        {
-            Transform(Vec(-0.15,0.004,-0.75), Quat(-0.98953,0,0,0.14436)),
-            Transform(Vec(-0.15,0.004,-0.75), Quat(-0.88982,-0.1368,0.07039,-0.45787)),
-            Transform(Vec(-0.15,0.004,-0.75), Quat(-0.88982,-0.1368,0.07039,-0.45787)),
-        },
-        {
-            Transform(Vec(-0.15,-0.082,-0.775), Quat(-0.99981,-0.0,0.0,0.00262)),
-            Transform(Vec(-0.132,-0.045,-0.714), Quat(-0.63992,-0.15483,0.02337,-0.75232)),
-            Transform(Vec(-0.132,-0.045,-0.714), Quat(-0.63992,-0.15483,0.02337,-0.75232)),
-        },
-        {
-            Transform(Vec(-0.05,0.004,-0.75), Quat(-0.97398,0,0,0.22665)),
-            Transform(Vec(-0.05,0.004,-0.75), Quat(-0.87781,-0.0526,0.03738,-0.47363)),
-            Transform(Vec(-0.05,0.004,-0.75), Quat(-0.87781,-0.0526,0.03738,-0.47363)),
-        },
-        {
-            Transform(Vec(-0.05,-0.072,-0.785), Quat(-0.99951,0,0,0.03141)),
-            Transform(Vec(-0.042,-0.044,-0.718), Quat(-0.67511,-0.04771,0.02282,-0.73582)),
-            Transform(Vec(-0.042,-0.044,-0.718), Quat(-0.67511,-0.04771,0.02282,-0.73582)),
-        },
-        {
-            Transform(Vec(0.05,0.004,-0.75), Quat(-0.95956,0,0,0.2815)),
-            Transform(Vec(0.05,0.004,-0.75), Quat(-0.99973,0,0,-0.0227)),
-            Transform(Vec(0.05,0.004,-0.75), Quat(-0.93451,0,0,-0.35593)),
-        },
-        {
-            Transform(Vec(0.05,-0.09,-0.82), Quat(0.99956,-0.0,0.0,0.02957)),
-            Transform(Vec(0.046,-0.124,-0.754), Quat(0.93547,0.13036,-0.03103,0.32702)),
-            Transform(Vec(0.05,-0.104,-0.704), Quat(0.55344,-0.00836,0.0063,0.83282)),
-        },
-        {
-            Transform(Vec(0.15,0.004,-0.75), Quat(-0.91283,0,0,0.40833)),
-            Transform(Vec(0.15,0.004,-0.75), Quat(-0.91283,0,0,0.40833)),
-            Transform(Vec(0.15,0.004,-0.75), Quat(-0.91283,0,0,0.40833)),
-        },
-        {
-            Transform(Vec(0.15,-0.046,-0.81), Quat(-0.95579,0,0,0.20404)),
-            Transform(Vec(0.15,-0.046,-0.81), Quat(-0.95579,0,0,0.20404)),
-            Transform(Vec(0.15,-0.046,-0.81), Quat(-0.95579,0,0,0.20404)),
-        },
-        {
-            Transform(Vec(0.145,-0.014,-0.5), Quat(-0.30224,0.55452,-0.14649,0.76138)),
-            Transform(Vec(0.159,-0.002,-0.493), Quat(-0.45852,0.70536,-0.19247,0.50517)),
-            Transform(Vec(0.145,-0.014,-0.5), Quat(-0.30224,0.55452,-0.14649,0.76138)),
-        },
-        {
-            Transform(Vec(0.192,-0.096,-0.604), Quat(-0.2241,0.60819,-0.05006,0.75985)),
-            Transform(Vec(0.149,-0.125,-0.569), Quat(-0.46199,0.7175,-0.25505,0.4545)),
-            Transform(Vec(0.192,-0.096,-0.604), Quat(-0.2241,0.60819,-0.05006,0.75985)),
-        }
-    }
-end
-
-function tick(dt)
-    if GetString("game.player.tool") == "liquify" then
-        if GetBool("game.player.canusetool") then
-            input(dt)
-            animate(dt)
-        else
-            SetToolTransform(armInvisibleT)
-        end
-
-        if InputPressed("c") then
-            gravity = not gravity
-        end
-
-        if PauseMenuButton("Liquify Options") then
-            drawOptions = true
-        end
-    end
-end
-
-function update(dt)
-    if not gravity then
-        bodies = FindBodies(nil, true)
-        SetPlayerVelocity(VecAdd(GetPlayerVelocity(),Vec(0, dt * 10, 0)))
-        for i, body in pairs(bodies) do
-            if IsBodyActive(body) then
-                ApplyBodyImpulse(body, TransformToParentPoint(GetBodyTransform(body), GetBodyCenterOfMass(body)), Vec(0, GetBodyMass(body) * dt * 10, 0))
-            end
-        end
-    end
-end
-
-function draw()
-    if GetString("game.player.tool") == "liquify" and drawOptions then
-        UiMakeInteractive()
-        UiTranslate(UiCenter() - 325, UiMiddle() - 370)
-        UiAlign("top left")
-        UiColor(0,0,0,0.8)
-        UiImageBox("ui/common/box-solid-6.png", 650, 740, 6, 6)
-        UiTranslate(300, 40)
-        UiColor(1, 1, 1)
-        UiFont("regular.ttf", 33)
-        UiAlign("center middle")
-        UiPush()
-            UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-            if UiTextButton("Reset to Defaults") then
-                limit = 10000
-                drawModel = true
-                SetInt("savegame.mod.liquify.limit", limit)
-                SetBool("savegame.mod.liquify.drawModel", drawModel)
-            end
-        UiPop()
-
-        UiPush()
-            UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-            UiTranslate(270, 0)
-            if UiTextButton("Close") then
-                drawOptions = false
-            end
-        UiPop()
-
-        UiAlign("left middle")
-
-        UiTranslate(-260, 90)
-        UiPush()
-            UiText("Voxel limit")
-            UiAlign("right")
-            UiTranslate(350, 8)
-            limit, done = optionsSlider(limit, 10000, 500000)
-            UiTranslate(40, 0)
-            UiAlign("left")
-            UiColor(0.7, 0.6, 0.1)
-            UiText(limit.." voxels")
-            SetInt("savegame.mod.liquify.limit", limit)
-        UiPop()
-
-        UiTranslate(0, 45)
-        UiPush()
-            UiText("Draw Hand Model")
-            UiTranslate(300, 10)
-            UiAlign("right")
-            UiColor(0.5, 0.8, 1)
-            if drawModel then
-                UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-                if UiTextButton("Yes") then
-                    drawModel = false
-                    SetBool("savegame.mod.liquify.drawModel", drawModel)
-                end
-            else
-                UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-                if UiTextButton("No") then
-                    drawModel = true
-                    SetBool("savegame.mod.liquify.drawModel", drawModel)
-                end
-            end
-        UiPop()
-
-        UiTranslate(0, 60)
-        UiPush()
-            UiText("Controls:")
-            UiFont("regular.ttf", 25)
-            UiTranslate(0, 60)
-            UiAlign("left")
-            UiColor(0.5, 0.8, 1)
-            UiText("{RMB} = Right Mouse Button")
-            UiTranslate(0, 30)
-            UiText("{LMB} = Left Mouse Button")
-            UiTranslate(0, 30)
-            UiText("{MMB} = Middle Mouse Button")
-            UiTranslate(0, 30)
-            UiText("Press {LMB} or {MMB} to liquify.")
-            UiTranslate(0, 30)
-            UiText("Press {RMB} to grab and {LMB} to throw things.")
-            UiTranslate(0, 30)
-            UiText("Press {R} to remove all current liquid single voxels.")
-            UiTranslate(0, 30)
-            UiText("Press {C} to toggle gravity on/off. This effect now stays active for\n any weapon, not just while holding liquify tool.")
-        UiPop()
-        
-        if drawModel then
-            SetToolTransform(armFrontT)
-        else
-            SetToolTransform(armInvisibleT)
-        end
-    end
-end
-
--- HELPER FUNCTIONS --
-
+#version 2
 function input(dt)
     local ct = GetCameraTransform()
     local fwd = TransformToParentVec(ct, Vec(0,0,-1))
@@ -230,7 +18,7 @@
                     for j = 0, y do
                         for k = 0, z do
                             local m, r, g, b, a = GetShapeMaterialAtIndex(shape, i, j, k)
-                            if a > 0 then
+                            if a ~= 0 then
                                 local pos = TransformToParentPoint(t, Vec(i / 10, j / 10, k / 10))
                                 local vel = GetBodyVelocityAtPos(body, pos)
                                 table.insert(object, {m = m, r = r, g = g, b = b, a = a, pos = pos, rot = t.rot, vel = vel})
@@ -313,8 +101,6 @@
     armAnimation.currentKeyframe = 1
 end
 
--- ANIMATION FUNCTIONS --
-
 function addKeyframe(anim, time, transform, event)
     local keyframe = {}
     keyframe.time = time
@@ -355,8 +141,6 @@
 
     return Transform(pos, rot)
 end
-
--- UTILITY FUNCTIONS -- 
 
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
@@ -377,4 +161,215 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    RegisterTool("liquify", "Liquify", "MOD/vox/hand.vox")
+    SetBool("game.tool.liquify.enabled", true, true)
+    drawOptions = false
+    -- weapon variables
+    voxels = {}
+    limit = 10000
+    drawModel = true
+    gravity = true
+    -- saved variables
+end
+
+function server.update(dt)
+    if not gravity then
+        bodies = FindBodies(nil, true)
+        SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),Vec(0, dt * 10, 0)))
+        for i, body in pairs(bodies) do
+            if IsBodyActive(body) then
+                ApplyBodyImpulse(body, TransformToParentPoint(GetBodyTransform(body), GetBodyCenterOfMass(body)), Vec(0, GetBodyMass(body) * dt * 10, 0))
+            end
+        end
+    end
+end
+
+function client.init()
+    if HasKey("savegame.mod.liquify.limit") then limit = GetFloat("savegame.mod.liquify.limit") end
+    if HasKey("savegame.mod.liquify.drawModel") then drawModel = GetBool("savegame.mod.liquify.drawModel") end
+
+    -- sound variables
+    snap = LoadSound("MOD/snd/snap.ogg")
+
+    -- animation variables
+    liquifying = false
+    called = false
+    liquifyT = 0
+    animations = {}
+    armAnimation = animation()
+    armFrontT = Transform(Vec(-1,-0.8,-0.9), QuatRotateQuat(QuatEuler(50,-10, 0), QuatEuler(0,0,140)))
+    armInvisibleT = Transform(Vec(110,110,100), QuatEuler(-90, 0,0))
+    addKeyframe(armAnimation, 0.0, armFrontT)
+    addKeyframe(armAnimation, 0.7, armFrontT)
+    snapKeyframes = {
+        {
+            Transform(Vec(-0.15,0.004,-0.75), Quat(-0.98953,0,0,0.14436)),
+            Transform(Vec(-0.15,0.004,-0.75), Quat(-0.88982,-0.1368,0.07039,-0.45787)),
+            Transform(Vec(-0.15,0.004,-0.75), Quat(-0.88982,-0.1368,0.07039,-0.45787)),
+        },
+        {
+            Transform(Vec(-0.15,-0.082,-0.775), Quat(-0.99981,-0.0,0.0,0.00262)),
+            Transform(Vec(-0.132,-0.045,-0.714), Quat(-0.63992,-0.15483,0.02337,-0.75232)),
+            Transform(Vec(-0.132,-0.045,-0.714), Quat(-0.63992,-0.15483,0.02337,-0.75232)),
+        },
+        {
+            Transform(Vec(-0.05,0.004,-0.75), Quat(-0.97398,0,0,0.22665)),
+            Transform(Vec(-0.05,0.004,-0.75), Quat(-0.87781,-0.0526,0.03738,-0.47363)),
+            Transform(Vec(-0.05,0.004,-0.75), Quat(-0.87781,-0.0526,0.03738,-0.47363)),
+        },
+        {
+            Transform(Vec(-0.05,-0.072,-0.785), Quat(-0.99951,0,0,0.03141)),
+            Transform(Vec(-0.042,-0.044,-0.718), Quat(-0.67511,-0.04771,0.02282,-0.73582)),
+            Transform(Vec(-0.042,-0.044,-0.718), Quat(-0.67511,-0.04771,0.02282,-0.73582)),
+        },
+        {
+            Transform(Vec(0.05,0.004,-0.75), Quat(-0.95956,0,0,0.2815)),
+            Transform(Vec(0.05,0.004,-0.75), Quat(-0.99973,0,0,-0.0227)),
+            Transform(Vec(0.05,0.004,-0.75), Quat(-0.93451,0,0,-0.35593)),
+        },
+        {
+            Transform(Vec(0.05,-0.09,-0.82), Quat(0.99956,-0.0,0.0,0.02957)),
+            Transform(Vec(0.046,-0.124,-0.754), Quat(0.93547,0.13036,-0.03103,0.32702)),
+            Transform(Vec(0.05,-0.104,-0.704), Quat(0.55344,-0.00836,0.0063,0.83282)),
+        },
+        {
+            Transform(Vec(0.15,0.004,-0.75), Quat(-0.91283,0,0,0.40833)),
+            Transform(Vec(0.15,0.004,-0.75), Quat(-0.91283,0,0,0.40833)),
+            Transform(Vec(0.15,0.004,-0.75), Quat(-0.91283,0,0,0.40833)),
+        },
+        {
+            Transform(Vec(0.15,-0.046,-0.81), Quat(-0.95579,0,0,0.20404)),
+            Transform(Vec(0.15,-0.046,-0.81), Quat(-0.95579,0,0,0.20404)),
+            Transform(Vec(0.15,-0.046,-0.81), Quat(-0.95579,0,0,0.20404)),
+        },
+        {
+            Transform(Vec(0.145,-0.014,-0.5), Quat(-0.30224,0.55452,-0.14649,0.76138)),
+            Transform(Vec(0.159,-0.002,-0.493), Quat(-0.45852,0.70536,-0.19247,0.50517)),
+            Transform(Vec(0.145,-0.014,-0.5), Quat(-0.30224,0.55452,-0.14649,0.76138)),
+        },
+        {
+            Transform(Vec(0.192,-0.096,-0.604), Quat(-0.2241,0.60819,-0.05006,0.75985)),
+            Transform(Vec(0.149,-0.125,-0.569), Quat(-0.46199,0.7175,-0.25505,0.4545)),
+            Transform(Vec(0.192,-0.096,-0.604), Quat(-0.2241,0.60819,-0.05006,0.75985)),
+        }
+    }
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "liquify" then
+        if GetBool("game.player.canusetool") then
+            input(dt)
+            animate(dt)
+        else
+            SetToolTransform(armInvisibleT)
+        end
+
+        if InputPressed("c") then
+            gravity = not gravity
+        end
+
+        if PauseMenuButton("Liquify Options") then
+            drawOptions = true
+        end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "liquify" and drawOptions then
+        UiMakeInteractive()
+        UiTranslate(UiCenter() - 325, UiMiddle() - 370)
+        UiAlign("top left")
+        UiColor(0,0,0,0.8)
+        UiImageBox("ui/common/box-solid-6.png", 650, 740, 6, 6)
+        UiTranslate(300, 40)
+        UiColor(1, 1, 1)
+        UiFont("regular.ttf", 33)
+        UiAlign("center middle")
+        UiPush()
+            UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+            if UiTextButton("Reset to Defaults") then
+                limit = 10000
+                drawModel = true
+                SetInt("savegame.mod.liquify.limit", limit, true)
+                SetBool("savegame.mod.liquify.drawModel", drawModel, true)
+            end
+        UiPop()
+
+        UiPush()
+            UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+            UiTranslate(270, 0)
+            if UiTextButton("Close") then
+                drawOptions = false
+            end
+        UiPop()
+
+        UiAlign("left middle")
+
+        UiTranslate(-260, 90)
+        UiPush()
+            UiText("Voxel limit")
+            UiAlign("right")
+            UiTranslate(350, 8)
+            limit, done = optionsSlider(limit, 10000, 500000)
+            UiTranslate(40, 0)
+            UiAlign("left")
+            UiColor(0.7, 0.6, 0.1)
+            UiText(limit.." voxels")
+            SetInt("savegame.mod.liquify.limit", limit, true)
+        UiPop()
+
+        UiTranslate(0, 45)
+        UiPush()
+            UiText("Draw Hand Model")
+            UiTranslate(300, 10)
+            UiAlign("right")
+            UiColor(0.5, 0.8, 1)
+            if drawModel then
+                UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+                if UiTextButton("Yes") then
+                    drawModel = false
+                    SetBool("savegame.mod.liquify.drawModel", drawModel, true)
+                end
+            else
+                UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+                if UiTextButton("No") then
+                    drawModel = true
+                    SetBool("savegame.mod.liquify.drawModel", drawModel, true)
+                end
+            end
+        UiPop()
+
+        UiTranslate(0, 60)
+        UiPush()
+            UiText("Controls:")
+            UiFont("regular.ttf", 25)
+            UiTranslate(0, 60)
+            UiAlign("left")
+            UiColor(0.5, 0.8, 1)
+            UiText("{RMB} = Right Mouse Button")
+            UiTranslate(0, 30)
+            UiText("{LMB} = Left Mouse Button")
+            UiTranslate(0, 30)
+            UiText("{MMB} = Middle Mouse Button")
+            UiTranslate(0, 30)
+            UiText("Press {LMB} or {MMB} to liquify.")
+            UiTranslate(0, 30)
+            UiText("Press {RMB} to grab and {LMB} to throw things.")
+            UiTranslate(0, 30)
+            UiText("Press {R} to remove all current liquid single voxels.")
+            UiTranslate(0, 30)
+            UiText("Press {C} to toggle gravity on/off. This effect now stays active for\n any weapon, not just while holding liquify tool.")
+        UiPop()
+
+        if drawModel then
+            SetToolTransform(armFrontT)
+        else
+            SetToolTransform(armInvisibleT)
+        end
+    end
+end
+

```
