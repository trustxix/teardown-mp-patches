# Migration Report: assets\vehicle\military\bridge_launcher.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/assets\vehicle\military\bridge_launcher.lua
+++ patched/assets\vehicle\military\bridge_launcher.lua
@@ -1,32 +1,36 @@
-FOLD_SPEED = 0.4
-
-function init()
+#version 2
+function server.init()
     bridge_attached = true
     bridge_launcher = FindVehicle("bridge_launcher")
-
     placer_joints = FindJoints("placer_j")
     placer_body = FindBody("placer_body")
     placer = FindShape("placer")
-    
     extend_joint = FindJoint("extend_joint")
     bridge_hinges = FindJoints("bridge")
     hook1 = FindJoint("hook1")
     hook2 = FindJoint("hook2")
-
-    attachSound = LoadSound("MOD/snd/metal_grab.ogg")
     hydraulic = LoadLoop("MOD/snd/hydraulic.ogg")
 end
 
-function tick(dt)
-    if GetPlayerVehicle() ~= bridge_launcher then
-        return
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) ~= bridge_launcher then
+            return
+        end
+        if hook1 ~= 0 and hook2 ~= 0 and GetJointOtherShape(hook1, placer) ~= 0 and GetJointOtherShape(hook2, placer) ~= 0 then
+            bridge_attached = true
+        else
+            bridge_attached = false
+        end
     end
-    if hook1 ~= 0 and hook2 ~= 0 and GetJointOtherShape(hook1, placer) ~= 0 and GetJointOtherShape(hook2, placer) ~= 0 then
-        bridge_attached = true
-    else
-        bridge_attached = false
-    end
-    
+end
+
+function client.init()
+    attachSound = LoadSound("MOD/snd/metal_grab.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if InputDown("lmb") then
         PlayLoop(hydraulic, GetBodyTransform(placer_body).pos, 0.25)
         for i=1, #placer_joints do
@@ -64,7 +68,6 @@
         end
         SetJointMotor(extend_joint, 0)
     end
-
     if InputPressed("x") then
         if hook1 ~= 0 and hook2 ~= 0 then
             Delete(hook1)
@@ -91,54 +94,55 @@
     end
 end
 
-function draw()
-	local keys = {}
-	if GetPlayerVehicle() == bridge_launcher then
-		keys[#keys+1] = {"LMB", "Unfold"}
-		keys[#keys+1] = {"RMB", "Fold"}
-		keys[#keys+1] = {"X", "Attach/Detach"}
+function client.draw()
+    local keys = {}
+    if GetPlayerVehicle(playerId) == bridge_launcher then
+    	keys[#keys+1] = {"LMB", "Unfold"}
+    	keys[#keys+1] = {"RMB", "Fold"}
+    	keys[#keys+1] = {"X", "Attach/Detach"}
 
-		UiPush()
-		UiAlign("top left")
-		local width = 230
-		local height = #keys * 23 + 30
-		UiTranslate(UiWidth() - width - 250, UiHeight() - height - 15)
-		UiColor(0, 0, 0, 0.5)
-		UiImageBox("ui/common/box-solid-6.png", width, height - 5, 6, 6)
-		UiTranslate(70, 32)
-		UiColor(1, 1, 1)
-		for i=1, #keys do
-			UiFont("bold.ttf", 22)
-			UiAlign("right")
-			UiText(keys[i][1])
-			UiTranslate(10, 0)
-			UiFont("regular.ttf", 22)
-			UiAlign("left")
-			UiText(keys[i][2])
-			UiTranslate(-10, 22)
-		end
-		UiPop()
+    	UiPush()
+    	UiAlign("top left")
+    	local width = 230
+    	local height = #keys * 23 + 30
+    	UiTranslate(UiWidth() - width - 250, UiHeight() - height - 15)
+    	UiColor(0, 0, 0, 0.5)
+    	UiImageBox("ui/common/box-solid-6.png", width, height - 5, 6, 6)
+    	UiTranslate(70, 32)
+    	UiColor(1, 1, 1)
+    	for i=1, #keys do
+    		UiFont("bold.ttf", 22)
+    		UiAlign("right")
+    		UiText(keys[i][1])
+    		UiTranslate(10, 0)
+    		UiFont("regular.ttf", 22)
+    		UiAlign("left")
+    		UiText(keys[i][2])
+    		UiTranslate(-10, 22)
+    	end
+    	UiPop()
 
-        UiPush()
-        local width = 160
-        UiTranslate(UiWidth() - width - 495, UiHeight() - 56)
-        UiColor(0, 0, 0, 0.5)
-        UiImageBox("ui/common/box-solid-6.png", width, 36, 6, 6)
-        if bridge_attached then
-            UiTranslate(12, 24)
-            UiAlign("top left")
-            UiFont("regular.ttf", 22)
-			UiAlign("left")
-            UiColor(1, 1, 1)
-            UiText("Bridge attached")
-        else
-            UiTranslate(20, 24)
-            UiAlign("top left")
-            UiFont("regular.ttf", 22)
-			UiAlign("left")
-            UiColor(1, 1, 1)
-            UiText("Bridge detach")
-        end
-        UiPop()
-	end
-end+           UiPush()
+           local width = 160
+           UiTranslate(UiWidth() - width - 495, UiHeight() - 56)
+           UiColor(0, 0, 0, 0.5)
+           UiImageBox("ui/common/box-solid-6.png", width, 36, 6, 6)
+           if bridge_attached then
+               UiTranslate(12, 24)
+               UiAlign("top left")
+               UiFont("regular.ttf", 22)
+    		UiAlign("left")
+               UiColor(1, 1, 1)
+               UiText("Bridge attached")
+           else
+               UiTranslate(20, 24)
+               UiAlign("top left")
+               UiFont("regular.ttf", 22)
+    		UiAlign("left")
+               UiColor(1, 1, 1)
+               UiText("Bridge detach")
+           end
+           UiPop()
+    end
+end
+

```
