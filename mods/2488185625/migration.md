# Migration Report: main\ambu\ambulance.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\ambu\ambulance.lua
+++ patched/main\ambu\ambulance.lua
@@ -1,784 +1,739 @@
-function init()
-    shapes = setmetatable({},{
-        __index = function(t, k)
-            local shape = FindShape(k)
-            rawset(t, k, shape)
-            return shape
-        end
-    })
-
-    lights = setmetatable({},{
-        __index = function(m, n)
-            local light = FindLight(n)
-            rawset(m, n, light)
-            return light
-        end
-    })
-
-    dl = FindJoint("dl")
-    dl1 = FindJoint("dl1")
-    dl2 = FindJoint("dl2")
-    dl3 = FindJoint("dl3")
-    dl4 = FindJoint("dl4")
-    dl5 = FindJoint("dl5")
-    dr = FindJoint("dr")
-    dr1 = FindJoint("dr1")
-    dr2 = FindJoint("dr2")
-    dr3 = FindJoint("dr3")
-	vehicle = FindVehicle("ambulancia")
-
-    limmdl, limxdl = GetJointLimits(dl)
-	loop = LoadLoop("LEVEL/ambu/police.ogg")
-	loop2 = LoadLoop("LEVEL/ambu/police2.ogg")
-	loop4 = LoadLoop("LEVEL/ambu/police3.ogg")
-	loop3 = LoadLoop("LEVEL/ambu/horn.ogg")
-    frame = math.random(0, 60)
-    lightOn = false
-    mlo = false
-    hlo = false
-    note = false
-    tl = false
-    tr = false
-    warning = false
-    flash = false
-    temp = false
-    adt = false
-    elight = false
-    elight2 = false
-    siren = false
-    siren2 = false
-    di = 0
-    es = 0
-    fa1 = 0 
-    fa2 = 0
-    fa3 = 0 
-    fa4 = 0
-    am1 = 0
-    am2 = 0
-    am3 = 0
-    am4 = 0
-    am5 = 0
-    am6 = 0
-    am7 = 0
-    am8 = 0
-    am9 = 0
+#version 2
+function server.init()
+       shapes = setmetatable({},{
+           __index = function(t, k)
+               local shape = FindShape(k)
+               rawset(t, k, shape)
+               return shape
+           end
+       })
+       lights = setmetatable({},{
+           __index = function(m, n)
+               local light = FindLight(n)
+               rawset(m, n, light)
+               return light
+           end
+       })
+       dl = FindJoint("dl")
+       dl1 = FindJoint("dl1")
+       dl2 = FindJoint("dl2")
+       dl3 = FindJoint("dl3")
+       dl4 = FindJoint("dl4")
+       dl5 = FindJoint("dl5")
+       dr = FindJoint("dr")
+       dr1 = FindJoint("dr1")
+       dr2 = FindJoint("dr2")
+       dr3 = FindJoint("dr3")
+    vehicle = FindVehicle("ambulancia")
+       limmdl, limxdl = GetJointLimits(dl)
+    loop = LoadLoop("LEVEL/ambu/police.ogg")
+    loop2 = LoadLoop("LEVEL/ambu/police2.ogg")
+    loop4 = LoadLoop("LEVEL/ambu/police3.ogg")
+    loop3 = LoadLoop("LEVEL/ambu/horn.ogg")
+       frame = math.random(0, 60)
+       lightOn = false
+       mlo = false
+       hlo = false
+       note = false
+       tl = false
+       tr = false
+       warning = false
+       flash = false
+       temp = false
+       adt = false
+       elight = false
+       elight2 = false
+       siren = false
+       siren2 = false
+       di = 0
+       es = 0
+       fa1 = 0 
+       fa2 = 0
+       fa3 = 0 
+       fa4 = 0
+       am1 = 0
+       am2 = 0
+       am3 = 0
+       am4 = 0
+       am5 = 0
+       am6 = 0
+       am7 = 0
+       am8 = 0
+       am9 = 0
 end
 
-function tick(dt)
-
-
-    if GetBool("game.player.usevehicle") then
-        dLocked = true
-        if note then
-        else
-            SetString("hud.notification", "'L'\t \t \t Light Mode \n 'K'\t \t \t Main-beam Headlights \n '  ,  (<)' & '  .  (>)'\t \t \t Blinkers \n 'O' \t \t \t Warning Lights \n 'J' \t \t \t Light Signal \n 'p''u' \t \t \t emergence light \n '1''2''g' \t \t \t sounds ")
-            note = true
-        end
-	else
-        dLocked = false
-    end
-
-    if dLocked then
-        if GetJointMovement(dl) > limmdl + 0.5 then
-            SetJointMotor(dl, 1)
-        else
-            SetJointMotor(dl, 0)
-        end
-        if GetJointMovement(dl1) > limmdl + 0.5 then
-            SetJointMotor(dl1, 2)
-        else
-            SetJointMotor(dl1, 0)
-        end
-        if GetJointMovement(dl2) > limmdl + 0.5 then
-            SetJointMotor(dl2, 2)
-        else
-            SetJointMotor(dl2, 0)
-        end
-        if GetJointMovement(dl3) > limmdl + 0.5 then
-            SetJointMotor(dl3, 2)
-        else
-            SetJointMotor(dl3, 0)
-        end
-        if GetJointMovement(dl4) > limmdl + 0.5 then
-            SetJointMotor(dl4, 2)
-        else
-            SetJointMotor(dl4, 0)
-        end
-        if GetJointMovement(dl5) > limmdl + 0.5 then
-            SetJointMotor(dl5, 2)
-        else
-            SetJointMotor(dl5, 0)
-        end
-        if GetJointMovement(dr) > limmdl + 0.5 then
-            SetJointMotor(dr, 2)
-        else
-            SetJointMotor(dr, 0)
-        end
-        if GetJointMovement(dr1) > limmdl + 0.5 then
-            SetJointMotor(dr1, 2)
-        else
-            SetJointMotor(dr1, 0)
-        end
-        if GetJointMovement(dr2) > limmdl + 0.5 then
-            SetJointMotor(dr2, 2)
-        else
-            SetJointMotor(dr2, 0)
-        end
-        if GetJointMovement(dr3) > limmdl + 0.5 then
-            SetJointMotor(dr3, 2)
-        else
-            SetJointMotor(dr3, 0)
-        end
-    else
-        SetJointMotor(dl, 0, 0)
-        SetJointMotor(dl1, 0, 0)
-        SetJointMotor(dl2, 0, 0)
-        SetJointMotor(dl3, 0, 0)
-        SetJointMotor(dl4, 0, 0)
-        SetJointMotor(dl5, 0, 0)
-        SetJointMotor(dr, 0, 0)
-        SetJointMotor(dr1, 0, 0)
-        SetJointMotor(dr2, 0, 0)
-        SetJointMotor(dr3, 0, 0)
-    end
-
-    if GetBool("game.player.useVehicle") and InputPressed("j") then
-        mlo = not mlo
-    end
-
-    if GetBool("game.player.useVehicle") and InputPressed("k") then
-        hlo = not hlo
-    end
-
-
-    if GetBool("game.player.useVehicle") and InputPressed(",") then
-        tl = not tl
-        tr = false
-        warning = false
-        to = GetTime()
-    end
-
-    if GetBool("game.player.useVehicle") and InputPressed(".") then
-        tr = not tr
-        tl = false
-        warning = false
-        to = GetTime()
-    end
-
-    if GetBool("game.player.useVehicle") and InputPressed("u") then
-        warning = not warning
-        tl = false
-        tr = false
-        to = GetTime()
-    end
-
-
-
-    if GetBool("game.player.useVehicle") and InputDown("l") then
-        flash = true
-    else
-        flash = false
-    end
-
-
-    if GetBool("game.player.useVehicle") and InputDown("g") then
-        PlayLoop(loop3)
-    end
-    if GetBool("game.player.useVehicle") and InputPressed("i") then
-        elight = not elight
-        elight2 = false
-        elight3 = false
-        to = GetTime()
-    end
-    if GetBool("game.player.useVehicle") and InputPressed("o") then
-        elight2 = not elight2
-        elight = false
-        elight3 = false
-    end
-    if GetBool("game.player.useVehicle") and InputPressed("1") then
-        siren = not siren
-        siren2 = false
-    end
-    if GetBool("game.player.useVehicle") and InputPressed("2") then
-        siren2 = not siren2
-        siren = false
-end
-
-
-
-
-if siren then
-
-PlayLoop(loop)
-
-end
-if siren2 then
-
-PlayLoop(loop2)
-
-end
-
-    if tl or tr or warning then
-        a = math.cos((GetTime()-to)*9)
-        if a >= 0 then
-            tli = 1
-        else
-            tli = 0.0001
-        end
-
-
-
-        if warning then
-            SetShapeEmissiveScale(shapes.tlfl2, tli)
-            SetShapeEmissiveScale(shapes.tlbl2, tli)
-            SetShapeEmissiveScale(shapes.tlfr2, tli)
-            SetShapeEmissiveScale(shapes.tlbr2, tli)
-        SetLightIntensity(lights.tlflp2, tli)
-        SetLightIntensity(lights.tlblp2, tli)
-        SetLightIntensity(lights.tlfrp2, tli)
-        SetLightIntensity(lights.tlbrp2, tli)
-
-
-
-        else
-            if tl then
-                SetShapeEmissiveScale(shapes.tlfl2, tli)
-                SetShapeEmissiveScale(shapes.tlbl2, tli)
-                SetShapeEmissiveScale(shapes.tlfr2, 0)
-                SetShapeEmissiveScale(shapes.tlbr2, 0)
-        SetLightIntensity(lights.tlflp2, tli)
-        SetLightIntensity(lights.tlblp2, tli)
-        SetLightIntensity(lights.tlfrp2, 0)
-        SetLightIntensity(lights.tlbrp2, 0)
-
-            elseif tr then
-                SetShapeEmissiveScale(shapes.tlfr2, tli)
-                SetShapeEmissiveScale(shapes.tlbr2, tli)
-                SetShapeEmissiveScale(shapes.tlfl2, 0)
-                SetShapeEmissiveScale(shapes.tlbl2, 0)
-        SetLightIntensity(lights.tlflp2, 0)
-        SetLightIntensity(lights.tlblp2, 0)
-        SetLightIntensity(lights.tlfrp2, tli)
-        SetLightIntensity(lights.tlbrp2, tli)
-
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+            if GetBool("game.player.usevehicle") then
+                dLocked = true
+                if note then
+                else
+                    SetString("hud.notification", "'L'\t \t \t Light Mode \n 'K'\t \t \t Main-beam Headlights \n '  ,  (<)' & '  .  (>)'\t \t \t Blinkers \n 'O' \t \t \t Warning Lights \n 'J' \t \t \t Light Signal \n 'p''u' \t \t \t emergence light \n '1''2''g' \t \t \t sounds ")
+                    note = true
+                end
+        	else
+                dLocked = false
+            end
+            if dLocked then
+                if GetJointMovement(dl) > limmdl + 0.5 then
+                    SetJointMotor(dl, 1)
+                else
+                    SetJointMotor(dl, 0)
+                end
+                if GetJointMovement(dl1) > limmdl + 0.5 then
+                    SetJointMotor(dl1, 2)
+                else
+                    SetJointMotor(dl1, 0)
+                end
+                if GetJointMovement(dl2) > limmdl + 0.5 then
+                    SetJointMotor(dl2, 2)
+                else
+                    SetJointMotor(dl2, 0)
+                end
+                if GetJointMovement(dl3) > limmdl + 0.5 then
+                    SetJointMotor(dl3, 2)
+                else
+                    SetJointMotor(dl3, 0)
+                end
+                if GetJointMovement(dl4) > limmdl + 0.5 then
+                    SetJointMotor(dl4, 2)
+                else
+                    SetJointMotor(dl4, 0)
+                end
+                if GetJointMovement(dl5) > limmdl + 0.5 then
+                    SetJointMotor(dl5, 2)
+                else
+                    SetJointMotor(dl5, 0)
+                end
+                if GetJointMovement(dr) > limmdl + 0.5 then
+                    SetJointMotor(dr, 2)
+                else
+                    SetJointMotor(dr, 0)
+                end
+                if GetJointMovement(dr1) > limmdl + 0.5 then
+                    SetJointMotor(dr1, 2)
+                else
+                    SetJointMotor(dr1, 0)
+                end
+                if GetJointMovement(dr2) > limmdl + 0.5 then
+                    SetJointMotor(dr2, 2)
+                else
+                    SetJointMotor(dr2, 0)
+                end
+                if GetJointMovement(dr3) > limmdl + 0.5 then
+                    SetJointMotor(dr3, 2)
+                else
+                    SetJointMotor(dr3, 0)
+                end
+            else
+                SetJointMotor(dl, 0, 0)
+                SetJointMotor(dl1, 0, 0)
+                SetJointMotor(dl2, 0, 0)
+                SetJointMotor(dl3, 0, 0)
+                SetJointMotor(dl4, 0, 0)
+                SetJointMotor(dl5, 0, 0)
+                SetJointMotor(dr, 0, 0)
+                SetJointMotor(dr1, 0, 0)
+                SetJointMotor(dr2, 0, 0)
+                SetJointMotor(dr3, 0, 0)
+            end
+            if tl or tr or warning then
+                a = math.cos((GetTime()-to)*9)
+                if a >= 0 then
+                    tli = 1
+                else
+                    tli = 0.0001
+                end
+
+                if warning then
+                    SetShapeEmissiveScale(shapes.tlfl2, tli)
+                    SetShapeEmissiveScale(shapes.tlbl2, tli)
+                    SetShapeEmissiveScale(shapes.tlfr2, tli)
+                    SetShapeEmissiveScale(shapes.tlbr2, tli)
+                SetLightIntensity(lights.tlflp2, tli)
+                SetLightIntensity(lights.tlblp2, tli)
+                SetLightIntensity(lights.tlfrp2, tli)
+                SetLightIntensity(lights.tlbrp2, tli)
+
+                else
+                    if tl then
+                        SetShapeEmissiveScale(shapes.tlfl2, tli)
+                        SetShapeEmissiveScale(shapes.tlbl2, tli)
+                        SetShapeEmissiveScale(shapes.tlfr2, 0)
+                        SetShapeEmissiveScale(shapes.tlbr2, 0)
+                SetLightIntensity(lights.tlflp2, tli)
+                SetLightIntensity(lights.tlblp2, tli)
+                SetLightIntensity(lights.tlfrp2, 0)
+                SetLightIntensity(lights.tlbrp2, 0)
+
+                    elseif tr then
+                        SetShapeEmissiveScale(shapes.tlfr2, tli)
+                        SetShapeEmissiveScale(shapes.tlbr2, tli)
+                        SetShapeEmissiveScale(shapes.tlfl2, 0)
+                        SetShapeEmissiveScale(shapes.tlbl2, 0)
+                SetLightIntensity(lights.tlflp2, 0)
+                SetLightIntensity(lights.tlblp2, 0)
+                SetLightIntensity(lights.tlfrp2, tli)
+                SetLightIntensity(lights.tlbrp2, tli)
+
+                    else
+                        SetShapeEmissiveScale(shapes.tlfl2, 0)
+                        SetShapeEmissiveScale(shapes.tlbl2, 0)
+                        SetShapeEmissiveScale(shapes.tlfr2, 0)
+                        SetShapeEmissiveScale(shapes.tlbr2, 0)
+                SetLightIntensity(lights.tlflp2, 0)
+                SetLightIntensity(lights.tlblp2, 0)
+                SetLightIntensity(lights.tlfrp2, 0)
+                SetLightIntensity(lights.tlbrp2, 0)
+
+                 end
+              end
             else
                 SetShapeEmissiveScale(shapes.tlfl2, 0)
                 SetShapeEmissiveScale(shapes.tlbl2, 0)
                 SetShapeEmissiveScale(shapes.tlfr2, 0)
                 SetShapeEmissiveScale(shapes.tlbr2, 0)
-        SetLightIntensity(lights.tlflp2, 0)
-        SetLightIntensity(lights.tlblp2, 0)
-        SetLightIntensity(lights.tlfrp2, 0)
-        SetLightIntensity(lights.tlbrp2, 0)
-
-         end
-      end
-    else
-        SetShapeEmissiveScale(shapes.tlfl2, 0)
-        SetShapeEmissiveScale(shapes.tlbl2, 0)
-        SetShapeEmissiveScale(shapes.tlfr2, 0)
-        SetShapeEmissiveScale(shapes.tlbr2, 0)
-        SetLightIntensity(lights.tlflp2, 0)
-        SetLightIntensity(lights.tlblp2, 0)
-        SetLightIntensity(lights.tlfrp2, 0)
-        SetLightIntensity(lights.tlbrp2, 0)
-
+                SetLightIntensity(lights.tlflp2, 0)
+                SetLightIntensity(lights.tlblp2, 0)
+                SetLightIntensity(lights.tlfrp2, 0)
+                SetLightIntensity(lights.tlbrp2, 0)
+
+            end
+            if flash then
+                SetLightIntensity(lights.lflmr2, 100)
+                SetLightIntensity(lights.lflml2, 100)
+                SetLightIntensity(lights.lfrmr2, 100)
+                SetLightIntensity(lights.lfrml2, 100)
+                    SetLightIntensity(lights.lflmrt2, 0.2)
+                    SetLightIntensity(lights.lflmlt2, 0.2)
+                    SetLightIntensity(lights.lfrmrt2, 0.2)
+                    SetLightIntensity(lights.lfrmlt2, 0.2)
+            else
+
+                if mlo then
+                    SetShapeEmissiveScale(shapes.lflm2, 1)
+                    SetShapeEmissiveScale(shapes.lfrm2, 1)
+                    SetShapeEmissiveScale(shapes.lflmt2, 1)
+                    SetShapeEmissiveScale(shapes.lfrmt2, 1)
+                else
+                    SetShapeEmissiveScale(shapes.lflm2, 0)
+                    SetShapeEmissiveScale(shapes.lfrm2, 0)
+                    SetShapeEmissiveScale(shapes.lflmt2, 0)
+                    SetShapeEmissiveScale(shapes.lfrmt2, 0)
+                end
+
+                if mlo and hlo then
+                    SetLightIntensity(lights.lflmr2, 100)
+                    SetLightIntensity(lights.lflml2, 100)
+                    SetLightIntensity(lights.lfrmr2, 100)
+                    SetLightIntensity(lights.lfrml2, 100)
+                    SetLightIntensity(lights.lflmrt2, 0.2)
+                    SetLightIntensity(lights.lflmlt2, 0.2)
+                    SetLightIntensity(lights.lfrmrt2, 0.2)
+                    SetLightIntensity(lights.lfrmlt2, 0.2)
+                elseif mlo then
+                    SetLightIntensity(lights.lflmr2, 10)
+                    SetLightIntensity(lights.lflml2, 10)
+                    SetLightIntensity(lights.lfrmr2, 10)
+                    SetLightIntensity(lights.lfrml2, 10)
+                    SetLightIntensity(lights.lflmrt2, 0.2)
+                    SetLightIntensity(lights.lflmlt2, 0.2)
+                    SetLightIntensity(lights.lfrmrt2, 0.2)
+                    SetLightIntensity(lights.lfrmlt2, 0.2)
+                else
+                    SetLightIntensity(lights.lflmr2, 0.0001)
+                    SetLightIntensity(lights.lflml2, 0.0001)
+                    SetLightIntensity(lights.lfrmr2, 0.0001)
+                    SetLightIntensity(lights.lfrml2, 0.0001)
+                    SetLightIntensity(lights.lflmrt2, 0.0001)
+                    SetLightIntensity(lights.lflmlt2, 0.0001)
+                    SetLightIntensity(lights.lfrmrt2, 0.0001)
+                    SetLightIntensity(lights.lfrmlt2, 0.0001)
+                end
+            end
+        	frame = frame + 1
+        	if elight then
+        			local period = 60
+        			local t = frame%period
+
+        			--toplights
+        			if t == 0 then 	am1 = 1 end
+        			if t == 10 then am1 = 0 end
+        			if t == 5 then am2 = 1 end
+        			if t == 15 then am2 = 0 end
+        			if t == 10 then am3 = 1 end
+        			if t == 20 then am3 = 0 end
+        			if t == 15 then am4 = 1 end
+        			if t == 25 then am4 = 0 end
+        			if t == 20 then am5 = 1 end
+        			if t == 15 then am6 = 1 end
+        			if t == 25 then am6 = 0 end
+        			if t == 10 then am7 = 1 end
+        			if t == 20 then am7 = 0 end
+        			if t == 5 then am8 = 1 end
+        			if t == 15 then am8 = 0 end
+        			if t == 0 then am9 = 1 end
+        			if t == 10 then am9 = 0 end
+
+        			if t == 45 then am1 = 1 end
+        			if t == 55 then am1 = 0 end
+        			if t == 40 then am2 = 1 end
+        			if t == 50 then am2 = 0 end
+        			if t == 35 then am3 = 1 end
+        			if t == 45 then am3 = 0 end
+        			if t == 30 then am4 = 1 end
+        			if t == 40 then am4 = 0 end
+        			if t == 35 then am5 = 0 end
+        			if t == 30 then am6 = 1 end
+        			if t == 40 then am6 = 0 end
+        			if t == 35 then am7 = 1 end
+        			if t == 45 then am7 = 0 end
+        			if t == 40 then am8 = 1 end
+        			if t == 50 then am8 = 0 end
+        			if t == 45 then am9 = 1 end
+        			if t == 55 then am9 = 0 end
+
+        			--Red
+        			if t == 0 then 	es = 1 	end
+        			if t == 15 then es = 0	end
+        			if t == 30 then es = 1	end
+        			if t == 45 then es = 0	end
+
+        			--Blue
+        			if t == 15 then di = 1 	end
+        			if t == 30 then di = 0	end
+        			if t == 45 then di = 1 	end
+        			if t == 59 then di = 0	end
+
+        			--farol
+        			if t == 0 then 	fa1 = 1 end
+        			if t == 15 then fa1 = 0 end
+        			if t == 30 then fa1 = 1 end
+        			if t == 45 then fa1 = 0 end
+
+        			if t == 15 then fa2 = 1 end
+        			if t == 30 then fa2 = 0	end
+        			if t == 45 then fa2 = 1 end
+        			if t == 59 then fa2 = 0	end
+
+        			--farol luz
+        			if t == 0 then 	fa3 = 10 end
+        			if t == 15 then fa3 = 0 end
+        			if t == 30 then fa3 = 10 end
+        			if t == 45 then fa3 = 0 end
+
+        			if t == 15 then fa4 = 10 end
+        			if t == 30 then fa4 = 0	end
+        			if t == 45 then fa4 = 10 end
+        			if t == 59 then fa4 = 0	end
+
+        			if t == 0 then 	fa5 = 1 end
+        			if t == 15 then fa5 = 0 end
+        			if t == 30 then fa5 = 1 end
+        			if t == 45 then fa5 = 0 end
+
+        			if t == 15 then fa6 = 1 end
+        			if t == 30 then fa6 = 0	end
+        			if t == 45 then fa6 = 1 end
+        			if t == 59 then fa6 = 0	end
+
+        SetShapeEmissiveScale(shapes.ab1, am1)
+        SetShapeEmissiveScale(shapes.ab2, am2)
+        SetShapeEmissiveScale(shapes.ab3, am3)
+        SetShapeEmissiveScale(shapes.ab4, am4)
+        SetShapeEmissiveScale(shapes.ab5, am5)
+        SetShapeEmissiveScale(shapes.ab6, am6)
+        SetShapeEmissiveScale(shapes.ab7, am7)
+        SetShapeEmissiveScale(shapes.ab8, am8)
+        SetShapeEmissiveScale(shapes.ab9, am9)
+        SetShapeEmissiveScale(shapes.ab10, am1)
+        SetShapeEmissiveScale(shapes.ab11, am2)
+        SetShapeEmissiveScale(shapes.ab12, am3)
+        SetShapeEmissiveScale(shapes.ab13, am4)
+        SetShapeEmissiveScale(shapes.ab14, am5)
+        SetShapeEmissiveScale(shapes.ab15, am6)
+        SetShapeEmissiveScale(shapes.ab16, am7)
+        SetShapeEmissiveScale(shapes.ab17, am8)
+        SetShapeEmissiveScale(shapes.ab18, am9)
+
+        SetShapeEmissiveScale(shapes.td, di)
+        SetShapeEmissiveScale(shapes.te, es)
+        SetShapeEmissiveScale(shapes.td2, di)
+        SetShapeEmissiveScale(shapes.te2, es)
+        SetShapeEmissiveScale(shapes.rd, di)
+        SetShapeEmissiveScale(shapes.re, es)
+        SetShapeEmissiveScale(shapes.rtd, di)
+        SetShapeEmissiveScale(shapes.rte, es)
+        SetShapeEmissiveScale(shapes.fd, di)
+        SetShapeEmissiveScale(shapes.fe, es)
+        SetShapeEmissiveScale(shapes.fd2, di)
+        SetShapeEmissiveScale(shapes.fe2, es)
+
+        SetLightIntensity(lights.ab1, am1)
+        SetLightIntensity(lights.ab2, am2)
+        SetLightIntensity(lights.ab3, am3)
+        SetLightIntensity(lights.ab4, am4)
+        SetLightIntensity(lights.ab5, am5)
+        SetLightIntensity(lights.ab6, am6)
+        SetLightIntensity(lights.ab7, am7)
+        SetLightIntensity(lights.ab8, am8)
+        SetLightIntensity(lights.ab9, am9)
+        SetLightIntensity(lights.ab10, am1)
+        SetLightIntensity(lights.ab11, am2)
+        SetLightIntensity(lights.ab12, am3)
+        SetLightIntensity(lights.ab13, am4)
+        SetLightIntensity(lights.ab14, am5)
+        SetLightIntensity(lights.ab15, am6)
+        SetLightIntensity(lights.ab16, am7)
+        SetLightIntensity(lights.ab17, am8)
+        SetLightIntensity(lights.ab18, am9)
+
+        SetLightIntensity(lights.td, di)
+        SetLightIntensity(lights.te, es)
+        SetLightIntensity(lights.td2, di)
+        SetLightIntensity(lights.te2, es)
+        SetLightIntensity(lights.td3, di)
+        SetLightIntensity(lights.te3, es)
+        SetLightIntensity(lights.td4, di)
+        SetLightIntensity(lights.te4, di)
+        SetLightIntensity(lights.td5, di)
+        SetLightIntensity(lights.te5, es)
+        SetLightIntensity(lights.rd, di)
+        SetLightIntensity(lights.rd2, di)
+        SetLightIntensity(lights.re, es)
+        SetLightIntensity(lights.rtd, di)
+        SetLightIntensity(lights.rte, es)
+        SetLightIntensity(lights.rte2, es)
+        SetLightIntensity(lights.fd, di)
+        SetLightIntensity(lights.fe, es)
+        SetLightIntensity(lights.fd2, di)
+        SetLightIntensity(lights.fe2, es)
+        SetShapeEmissiveScale(shapes.lflm2, fa1)
+        SetLightIntensity(lights.lflml2, fa3)
+        SetShapeEmissiveScale(shapes.lfrm2, fa2)
+        SetLightIntensity(lights.lflmr2, fa4)
+        SetShapeEmissiveScale(shapes.lflmt2, fa1)
+        SetLightIntensity(lights.lflmlt2, fa5)
+        SetShapeEmissiveScale(shapes.lfrmt2, fa2)
+        SetLightIntensity(lights.lfrmrt2, fa6)
+
+        else
+
+        SetShapeEmissiveScale(shapes.ab1, 0)
+        SetShapeEmissiveScale(shapes.ab2, 0)
+        SetShapeEmissiveScale(shapes.ab3, 0)
+        SetShapeEmissiveScale(shapes.ab4, 0)
+        SetShapeEmissiveScale(shapes.ab5, 0)
+        SetShapeEmissiveScale(shapes.ab6, 0)
+        SetShapeEmissiveScale(shapes.ab7, 0)
+        SetShapeEmissiveScale(shapes.ab8, 0)
+        SetShapeEmissiveScale(shapes.ab9, 0)
+        SetShapeEmissiveScale(shapes.ab10, 0)
+        SetShapeEmissiveScale(shapes.ab11, 0)
+        SetShapeEmissiveScale(shapes.ab12, 0)
+        SetShapeEmissiveScale(shapes.ab13, 0)
+        SetShapeEmissiveScale(shapes.ab14, 0)
+        SetShapeEmissiveScale(shapes.ab15, 0)
+        SetShapeEmissiveScale(shapes.ab16, 0)
+        SetShapeEmissiveScale(shapes.ab17, 0)
+        SetShapeEmissiveScale(shapes.ab18, 0)
+        SetShapeEmissiveScale(shapes.td, 0)
+        SetShapeEmissiveScale(shapes.te, 0)
+        SetShapeEmissiveScale(shapes.td2, 0)
+        SetShapeEmissiveScale(shapes.te2, 0)
+        SetShapeEmissiveScale(shapes.rd, 0)
+        SetShapeEmissiveScale(shapes.re, 0)
+        SetShapeEmissiveScale(shapes.rtd, 0)
+        SetShapeEmissiveScale(shapes.rte, 0)
+        SetShapeEmissiveScale(shapes.fd, 0)
+        SetShapeEmissiveScale(shapes.fe, 0)
+        SetShapeEmissiveScale(shapes.fd2, 0)
+        SetShapeEmissiveScale(shapes.fe2, 0)
+
+        SetLightIntensity(lights.ab1, 0)
+        SetLightIntensity(lights.ab2, 0)
+        SetLightIntensity(lights.ab3, 0)
+        SetLightIntensity(lights.ab4, 0)
+        SetLightIntensity(lights.ab5, 0)
+        SetLightIntensity(lights.ab6, 0)
+        SetLightIntensity(lights.ab7, 0)
+        SetLightIntensity(lights.ab8, 0)
+        SetLightIntensity(lights.ab9, 0)
+        SetLightIntensity(lights.ab10, 0)
+        SetLightIntensity(lights.ab11, 0)
+        SetLightIntensity(lights.ab12, 0)
+        SetLightIntensity(lights.ab13, 0)
+        SetLightIntensity(lights.ab14, 0)
+        SetLightIntensity(lights.ab15, 0)
+        SetLightIntensity(lights.ab16, 0)
+        SetLightIntensity(lights.ab17, 0)
+        SetLightIntensity(lights.ab18, 0)
+        SetLightIntensity(lights.td, 0)
+        SetLightIntensity(lights.te, 0)
+        SetLightIntensity(lights.td2, 0)
+        SetLightIntensity(lights.te2, 0)
+        SetLightIntensity(lights.td3, 0)
+        SetLightIntensity(lights.te3, 0)
+        SetLightIntensity(lights.td4, 0)
+        SetLightIntensity(lights.te4, 0)
+        SetLightIntensity(lights.td5, 0)
+        SetLightIntensity(lights.te5, 0)
+        SetLightIntensity(lights.rd, 0)
+        SetLightIntensity(lights.rd2, 0)
+        SetLightIntensity(lights.re, 0)
+        SetLightIntensity(lights.rtd, 0)
+        SetLightIntensity(lights.rte, 0)
+        SetLightIntensity(lights.rte2, 0)
+        SetLightIntensity(lights.fd, 0)
+        SetLightIntensity(lights.fe, 0)
+        SetLightIntensity(lights.fd2, 0)
+        SetLightIntensity(lights.fe2, 0)
+
+        	end
+
+        	if elight2 then
+        			local period = 60
+        			local t = frame%period
+        			--toplights
+        			if t == 0 then 	am1 = 1 end
+        			if t == 5 then am1 = 0 end
+        			if t == 10 then am1 = 1 end
+        			if t == 15 then am1 = 0 end
+        			if t == 20 then am1 = 1 end
+        			if t == 25 then am1 = 0 end
+
+        			if t == 5 then am2 = 1 end
+        			if t == 15 then am2 = 0 end
+        			if t == 10 then am3 = 1 end
+        			if t == 20 then am3 = 0 end
+        			if t == 40 then am2 = 1 end
+        			if t == 50 then am2 = 0 end
+        			if t == 35 then am3 = 1 end
+        			if t == 45 then am3 = 0 end
+
+        			if t == 30 then am4 = 1 end
+        			if t == 35 then am4 = 0 end
+        			if t == 40 then am4 = 1 end
+        			if t == 45 then am4 = 0 end
+        			if t == 50 then am4 = 1 end
+        			if t == 55 then am4 = 0 end
+
+        			if t == 20 then am5 = 1 end
+        			if t == 35 then am5 = 0 end
+
+        			if t == 30 then am6 = 1 end
+        			if t == 35 then am6 = 0 end
+        			if t == 40 then am6 = 1 end
+        			if t == 45 then am6 = 0 end
+        			if t == 50 then am6 = 1 end
+        			if t == 55 then am6 = 0 end
+
+        			if t == 10 then am7 = 1 end
+        			if t == 20 then am7 = 0 end
+        			if t == 5 then am8 = 1 end
+        			if t == 15 then am8 = 0 end
+        			if t == 35 then am7 = 1 end
+        			if t == 45 then am7 = 0 end
+        			if t == 40 then am8 = 1 end
+        			if t == 50 then am8 = 0 end
+
+        			if t == 0 then am9 = 1 end
+        			if t == 5 then am9 = 0 end
+        			if t == 10 then am9 = 1 end
+        			if t == 15 then am9 = 0 end
+        			if t == 20 then am9 = 1 end
+        			if t == 25 then am9 = 0 end
+
+        			--Red
+        			if t == 0 then 	es = 1	end
+        			if t == 5 then es = 0	end
+        			if t == 10 then es = 1 	end
+        			if t == 30 then es = 0	end
+
+        			--Blue
+        			if t == 30 then di = 1 	end
+        			if t == 35 then di = 0	end
+        			if t == 40 then di = 1 	end
+        			if t == 59 then di = 0	end
+
+        			--farol
+        			if t == 0 then 	fa1 = 1 end
+        			if t == 5 then fa1 = 0 end
+        			if t == 10 then fa1 = 1 end
+        			if t == 30 then fa1 = 0 end
+
+        			if t == 30 then fa2 = 1 end
+        			if t == 35 then fa2 = 0	end
+        			if t == 40 then fa2 = 1 end
+        			if t == 59 then fa2 = 0	end
+
+        			--farol luz
+        			if t == 0 then 	fa3 = 10 end
+        			if t == 5 then fa3 = 0 end
+        			if t == 10 then fa3 = 10 end
+        			if t == 30 then fa3 = 0 end
+
+        			if t == 30 then fa4 = 10 end
+        			if t == 35 then fa4 = 0	end
+        			if t == 40 then fa4 = 10 end
+        			if t == 59 then fa4 = 0	end
+
+        			if t == 0 then 	fa5 = 1 end
+        			if t == 5 then fa5 = 0 end
+        			if t == 10 then fa5 = 1 end
+        			if t == 30 then fa5 = 0 end
+
+        			if t == 30 then fa6 = 1 end
+        			if t == 35 then fa6 = 0	end
+        			if t == 40 then fa6 = 1 end
+        			if t == 59 then fa6 = 0	end
+
+        SetShapeEmissiveScale(shapes.ab1, am1)
+        SetShapeEmissiveScale(shapes.ab2, am2)
+        SetShapeEmissiveScale(shapes.ab3, am3)
+        SetShapeEmissiveScale(shapes.ab4, am4)
+        SetShapeEmissiveScale(shapes.ab5, am5)
+        SetShapeEmissiveScale(shapes.ab6, am6)
+        SetShapeEmissiveScale(shapes.ab7, am7)
+        SetShapeEmissiveScale(shapes.ab8, am8)
+        SetShapeEmissiveScale(shapes.ab9, am9)
+        SetShapeEmissiveScale(shapes.ab10, am1)
+        SetShapeEmissiveScale(shapes.ab11, am2)
+        SetShapeEmissiveScale(shapes.ab12, am3)
+        SetShapeEmissiveScale(shapes.ab13, am4)
+        SetShapeEmissiveScale(shapes.ab14, am5)
+        SetShapeEmissiveScale(shapes.ab15, am6)
+        SetShapeEmissiveScale(shapes.ab16, am7)
+        SetShapeEmissiveScale(shapes.ab17, am8)
+        SetShapeEmissiveScale(shapes.ab18, am9)
+
+        SetShapeEmissiveScale(shapes.td, di)
+        SetShapeEmissiveScale(shapes.te, es)
+        SetShapeEmissiveScale(shapes.td2, di)
+        SetShapeEmissiveScale(shapes.te2, es)
+        SetShapeEmissiveScale(shapes.rd, di)
+        SetShapeEmissiveScale(shapes.re, es)
+        SetShapeEmissiveScale(shapes.rtd, di)
+        SetShapeEmissiveScale(shapes.rte, es)
+        SetShapeEmissiveScale(shapes.fd, di)
+        SetShapeEmissiveScale(shapes.fe, es)
+        SetShapeEmissiveScale(shapes.fd2, di)
+        SetShapeEmissiveScale(shapes.fe2, es)
+
+        SetLightIntensity(lights.ab1, am1)
+        SetLightIntensity(lights.ab2, am2)
+        SetLightIntensity(lights.ab3, am3)
+        SetLightIntensity(lights.ab4, am4)
+        SetLightIntensity(lights.ab5, am5)
+        SetLightIntensity(lights.ab6, am6)
+        SetLightIntensity(lights.ab7, am7)
+        SetLightIntensity(lights.ab8, am8)
+        SetLightIntensity(lights.ab9, am9)
+        SetLightIntensity(lights.ab10, am1)
+        SetLightIntensity(lights.ab11, am2)
+        SetLightIntensity(lights.ab12, am3)
+        SetLightIntensity(lights.ab13, am4)
+        SetLightIntensity(lights.ab14, am5)
+        SetLightIntensity(lights.ab15, am6)
+        SetLightIntensity(lights.ab16, am7)
+        SetLightIntensity(lights.ab17, am8)
+        SetLightIntensity(lights.ab18, am9)
+
+        SetLightIntensity(lights.td, di)
+        SetLightIntensity(lights.te, es)
+        SetLightIntensity(lights.td2, di)
+        SetLightIntensity(lights.te2, es)
+        SetLightIntensity(lights.td3, di)
+        SetLightIntensity(lights.te3, es)
+        SetLightIntensity(lights.td4, di)
+        SetLightIntensity(lights.te4, di)
+        SetLightIntensity(lights.td5, di)
+        SetLightIntensity(lights.te5, es)
+        SetLightIntensity(lights.rd, di)
+        SetLightIntensity(lights.rd2, di)
+        SetLightIntensity(lights.re, es)
+        SetLightIntensity(lights.rtd, di)
+        SetLightIntensity(lights.rte, es)
+        SetLightIntensity(lights.rte2, es)
+        SetLightIntensity(lights.fd, di)
+        SetLightIntensity(lights.fe, es)
+        SetLightIntensity(lights.fd2, di)
+        SetLightIntensity(lights.fe2, es)
+        SetShapeEmissiveScale(shapes.lflm2, fa1)
+        SetLightIntensity(lights.lflml2, fa3)
+        SetShapeEmissiveScale(shapes.lfrm2, fa2)
+        SetLightIntensity(lights.lflmr2, fa4)
+        SetShapeEmissiveScale(shapes.lflmt2, fa1)
+        SetLightIntensity(lights.lflmlt2, fa5)
+        SetShapeEmissiveScale(shapes.lfrmt2, fa2)
+        SetLightIntensity(lights.lfrmrt2, fa6)
+
+        	end
     end
-
-
-    if flash then
-        SetLightIntensity(lights.lflmr2, 100)
-        SetLightIntensity(lights.lflml2, 100)
-        SetLightIntensity(lights.lfrmr2, 100)
-        SetLightIntensity(lights.lfrml2, 100)
-            SetLightIntensity(lights.lflmrt2, 0.2)
-            SetLightIntensity(lights.lflmlt2, 0.2)
-            SetLightIntensity(lights.lfrmrt2, 0.2)
-            SetLightIntensity(lights.lfrmlt2, 0.2)
-    else
-
-
-        if mlo then
-            SetShapeEmissiveScale(shapes.lflm2, 1)
-            SetShapeEmissiveScale(shapes.lfrm2, 1)
-            SetShapeEmissiveScale(shapes.lflmt2, 1)
-            SetShapeEmissiveScale(shapes.lfrmt2, 1)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+        if GetBool("game.player.useVehicle") and InputPressed("j") then
+            mlo = not mlo
+        end
+        if GetBool("game.player.useVehicle") and InputPressed("k") then
+            hlo = not hlo
+        end
+        if GetBool("game.player.useVehicle") and InputPressed(",") then
+            tl = not tl
+            tr = false
+            warning = false
+            to = GetTime()
+        end
+        if GetBool("game.player.useVehicle") and InputPressed(".") then
+            tr = not tr
+            tl = false
+            warning = false
+            to = GetTime()
+        end
+        if GetBool("game.player.useVehicle") and InputPressed("u") then
+            warning = not warning
+            tl = false
+            tr = false
+            to = GetTime()
+        end
+        if GetBool("game.player.useVehicle") and InputDown("l") then
+            flash = true
         else
-            SetShapeEmissiveScale(shapes.lflm2, 0)
-            SetShapeEmissiveScale(shapes.lfrm2, 0)
-            SetShapeEmissiveScale(shapes.lflmt2, 0)
-            SetShapeEmissiveScale(shapes.lfrmt2, 0)
-        end
-
-        if mlo and hlo then
-            SetLightIntensity(lights.lflmr2, 100)
-            SetLightIntensity(lights.lflml2, 100)
-            SetLightIntensity(lights.lfrmr2, 100)
-            SetLightIntensity(lights.lfrml2, 100)
-            SetLightIntensity(lights.lflmrt2, 0.2)
-            SetLightIntensity(lights.lflmlt2, 0.2)
-            SetLightIntensity(lights.lfrmrt2, 0.2)
-            SetLightIntensity(lights.lfrmlt2, 0.2)
-        elseif mlo then
-            SetLightIntensity(lights.lflmr2, 10)
-            SetLightIntensity(lights.lflml2, 10)
-            SetLightIntensity(lights.lfrmr2, 10)
-            SetLightIntensity(lights.lfrml2, 10)
-            SetLightIntensity(lights.lflmrt2, 0.2)
-            SetLightIntensity(lights.lflmlt2, 0.2)
-            SetLightIntensity(lights.lfrmrt2, 0.2)
-            SetLightIntensity(lights.lfrmlt2, 0.2)
-        else
-            SetLightIntensity(lights.lflmr2, 0.0001)
-            SetLightIntensity(lights.lflml2, 0.0001)
-            SetLightIntensity(lights.lfrmr2, 0.0001)
-            SetLightIntensity(lights.lfrml2, 0.0001)
-            SetLightIntensity(lights.lflmrt2, 0.0001)
-            SetLightIntensity(lights.lflmlt2, 0.0001)
-            SetLightIntensity(lights.lfrmrt2, 0.0001)
-            SetLightIntensity(lights.lfrmlt2, 0.0001)
-        end
+            flash = false
+        end
+        if GetBool("game.player.useVehicle") and InputDown("g") then
+            PlayLoop(loop3)
+        end
+        if GetBool("game.player.useVehicle") and InputPressed("i") then
+            elight = not elight
+            elight2 = false
+            elight3 = false
+            to = GetTime()
+        end
+        if GetBool("game.player.useVehicle") and InputPressed("o") then
+            elight2 = not elight2
+            elight = false
+            elight3 = false
+        end
+        if GetBool("game.player.useVehicle") and InputPressed("1") then
+            siren = not siren
+            siren2 = false
+        end
+        if GetBool("game.player.useVehicle") and InputPressed("2") then
+            siren2 = not siren2
+            siren = false
     end
-
-
-
-
-
-
-
-
-	frame = frame + 1
-	if elight then
-			local period = 60
-			local t = frame%period
-
-			--toplights
-			if t == 0 then 	am1 = 1 end
-			if t == 10 then am1 = 0 end
-			if t == 5 then am2 = 1 end
-			if t == 15 then am2 = 0 end
-			if t == 10 then am3 = 1 end
-			if t == 20 then am3 = 0 end
-			if t == 15 then am4 = 1 end
-			if t == 25 then am4 = 0 end
-			if t == 20 then am5 = 1 end
-			if t == 15 then am6 = 1 end
-			if t == 25 then am6 = 0 end
-			if t == 10 then am7 = 1 end
-			if t == 20 then am7 = 0 end
-			if t == 5 then am8 = 1 end
-			if t == 15 then am8 = 0 end
-			if t == 0 then am9 = 1 end
-			if t == 10 then am9 = 0 end
-
-			if t == 45 then am1 = 1 end
-			if t == 55 then am1 = 0 end
-			if t == 40 then am2 = 1 end
-			if t == 50 then am2 = 0 end
-			if t == 35 then am3 = 1 end
-			if t == 45 then am3 = 0 end
-			if t == 30 then am4 = 1 end
-			if t == 40 then am4 = 0 end
-			if t == 35 then am5 = 0 end
-			if t == 30 then am6 = 1 end
-			if t == 40 then am6 = 0 end
-			if t == 35 then am7 = 1 end
-			if t == 45 then am7 = 0 end
-			if t == 40 then am8 = 1 end
-			if t == 50 then am8 = 0 end
-			if t == 45 then am9 = 1 end
-			if t == 55 then am9 = 0 end
-
-
-			--Red
-			if t == 0 then 	es = 1 	end
-			if t == 15 then es = 0	end
-			if t == 30 then es = 1	end
-			if t == 45 then es = 0	end
-
-			--Blue
-			if t == 15 then di = 1 	end
-			if t == 30 then di = 0	end
-			if t == 45 then di = 1 	end
-			if t == 59 then di = 0	end
-
-
-			--farol
-			if t == 0 then 	fa1 = 1 end
-			if t == 15 then fa1 = 0 end
-			if t == 30 then fa1 = 1 end
-			if t == 45 then fa1 = 0 end
-
-			if t == 15 then fa2 = 1 end
-			if t == 30 then fa2 = 0	end
-			if t == 45 then fa2 = 1 end
-			if t == 59 then fa2 = 0	end
-
-			--farol luz
-			if t == 0 then 	fa3 = 10 end
-			if t == 15 then fa3 = 0 end
-			if t == 30 then fa3 = 10 end
-			if t == 45 then fa3 = 0 end
-
-			if t == 15 then fa4 = 10 end
-			if t == 30 then fa4 = 0	end
-			if t == 45 then fa4 = 10 end
-			if t == 59 then fa4 = 0	end
-
-			if t == 0 then 	fa5 = 1 end
-			if t == 15 then fa5 = 0 end
-			if t == 30 then fa5 = 1 end
-			if t == 45 then fa5 = 0 end
-
-			if t == 15 then fa6 = 1 end
-			if t == 30 then fa6 = 0	end
-			if t == 45 then fa6 = 1 end
-			if t == 59 then fa6 = 0	end
-
-
-
-
-SetShapeEmissiveScale(shapes.ab1, am1)
-SetShapeEmissiveScale(shapes.ab2, am2)
-SetShapeEmissiveScale(shapes.ab3, am3)
-SetShapeEmissiveScale(shapes.ab4, am4)
-SetShapeEmissiveScale(shapes.ab5, am5)
-SetShapeEmissiveScale(shapes.ab6, am6)
-SetShapeEmissiveScale(shapes.ab7, am7)
-SetShapeEmissiveScale(shapes.ab8, am8)
-SetShapeEmissiveScale(shapes.ab9, am9)
-SetShapeEmissiveScale(shapes.ab10, am1)
-SetShapeEmissiveScale(shapes.ab11, am2)
-SetShapeEmissiveScale(shapes.ab12, am3)
-SetShapeEmissiveScale(shapes.ab13, am4)
-SetShapeEmissiveScale(shapes.ab14, am5)
-SetShapeEmissiveScale(shapes.ab15, am6)
-SetShapeEmissiveScale(shapes.ab16, am7)
-SetShapeEmissiveScale(shapes.ab17, am8)
-SetShapeEmissiveScale(shapes.ab18, am9)
-
-SetShapeEmissiveScale(shapes.td, di)
-SetShapeEmissiveScale(shapes.te, es)
-SetShapeEmissiveScale(shapes.td2, di)
-SetShapeEmissiveScale(shapes.te2, es)
-SetShapeEmissiveScale(shapes.rd, di)
-SetShapeEmissiveScale(shapes.re, es)
-SetShapeEmissiveScale(shapes.rtd, di)
-SetShapeEmissiveScale(shapes.rte, es)
-SetShapeEmissiveScale(shapes.fd, di)
-SetShapeEmissiveScale(shapes.fe, es)
-SetShapeEmissiveScale(shapes.fd2, di)
-SetShapeEmissiveScale(shapes.fe2, es)
-
-SetLightIntensity(lights.ab1, am1)
-SetLightIntensity(lights.ab2, am2)
-SetLightIntensity(lights.ab3, am3)
-SetLightIntensity(lights.ab4, am4)
-SetLightIntensity(lights.ab5, am5)
-SetLightIntensity(lights.ab6, am6)
-SetLightIntensity(lights.ab7, am7)
-SetLightIntensity(lights.ab8, am8)
-SetLightIntensity(lights.ab9, am9)
-SetLightIntensity(lights.ab10, am1)
-SetLightIntensity(lights.ab11, am2)
-SetLightIntensity(lights.ab12, am3)
-SetLightIntensity(lights.ab13, am4)
-SetLightIntensity(lights.ab14, am5)
-SetLightIntensity(lights.ab15, am6)
-SetLightIntensity(lights.ab16, am7)
-SetLightIntensity(lights.ab17, am8)
-SetLightIntensity(lights.ab18, am9)
-
-SetLightIntensity(lights.td, di)
-SetLightIntensity(lights.te, es)
-SetLightIntensity(lights.td2, di)
-SetLightIntensity(lights.te2, es)
-SetLightIntensity(lights.td3, di)
-SetLightIntensity(lights.te3, es)
-SetLightIntensity(lights.td4, di)
-SetLightIntensity(lights.te4, di)
-SetLightIntensity(lights.td5, di)
-SetLightIntensity(lights.te5, es)
-SetLightIntensity(lights.rd, di)
-SetLightIntensity(lights.rd2, di)
-SetLightIntensity(lights.re, es)
-SetLightIntensity(lights.rtd, di)
-SetLightIntensity(lights.rte, es)
-SetLightIntensity(lights.rte2, es)
-SetLightIntensity(lights.fd, di)
-SetLightIntensity(lights.fe, es)
-SetLightIntensity(lights.fd2, di)
-SetLightIntensity(lights.fe2, es)
-SetShapeEmissiveScale(shapes.lflm2, fa1)
-SetLightIntensity(lights.lflml2, fa3)
-SetShapeEmissiveScale(shapes.lfrm2, fa2)
-SetLightIntensity(lights.lflmr2, fa4)
-SetShapeEmissiveScale(shapes.lflmt2, fa1)
-SetLightIntensity(lights.lflmlt2, fa5)
-SetShapeEmissiveScale(shapes.lfrmt2, fa2)
-SetLightIntensity(lights.lfrmrt2, fa6)
-
-else
-
-SetShapeEmissiveScale(shapes.ab1, 0)
-SetShapeEmissiveScale(shapes.ab2, 0)
-SetShapeEmissiveScale(shapes.ab3, 0)
-SetShapeEmissiveScale(shapes.ab4, 0)
-SetShapeEmissiveScale(shapes.ab5, 0)
-SetShapeEmissiveScale(shapes.ab6, 0)
-SetShapeEmissiveScale(shapes.ab7, 0)
-SetShapeEmissiveScale(shapes.ab8, 0)
-SetShapeEmissiveScale(shapes.ab9, 0)
-SetShapeEmissiveScale(shapes.ab10, 0)
-SetShapeEmissiveScale(shapes.ab11, 0)
-SetShapeEmissiveScale(shapes.ab12, 0)
-SetShapeEmissiveScale(shapes.ab13, 0)
-SetShapeEmissiveScale(shapes.ab14, 0)
-SetShapeEmissiveScale(shapes.ab15, 0)
-SetShapeEmissiveScale(shapes.ab16, 0)
-SetShapeEmissiveScale(shapes.ab17, 0)
-SetShapeEmissiveScale(shapes.ab18, 0)
-SetShapeEmissiveScale(shapes.td, 0)
-SetShapeEmissiveScale(shapes.te, 0)
-SetShapeEmissiveScale(shapes.td2, 0)
-SetShapeEmissiveScale(shapes.te2, 0)
-SetShapeEmissiveScale(shapes.rd, 0)
-SetShapeEmissiveScale(shapes.re, 0)
-SetShapeEmissiveScale(shapes.rtd, 0)
-SetShapeEmissiveScale(shapes.rte, 0)
-SetShapeEmissiveScale(shapes.fd, 0)
-SetShapeEmissiveScale(shapes.fe, 0)
-SetShapeEmissiveScale(shapes.fd2, 0)
-SetShapeEmissiveScale(shapes.fe2, 0)
-
-SetLightIntensity(lights.ab1, 0)
-SetLightIntensity(lights.ab2, 0)
-SetLightIntensity(lights.ab3, 0)
-SetLightIntensity(lights.ab4, 0)
-SetLightIntensity(lights.ab5, 0)
-SetLightIntensity(lights.ab6, 0)
-SetLightIntensity(lights.ab7, 0)
-SetLightIntensity(lights.ab8, 0)
-SetLightIntensity(lights.ab9, 0)
-SetLightIntensity(lights.ab10, 0)
-SetLightIntensity(lights.ab11, 0)
-SetLightIntensity(lights.ab12, 0)
-SetLightIntensity(lights.ab13, 0)
-SetLightIntensity(lights.ab14, 0)
-SetLightIntensity(lights.ab15, 0)
-SetLightIntensity(lights.ab16, 0)
-SetLightIntensity(lights.ab17, 0)
-SetLightIntensity(lights.ab18, 0)
-SetLightIntensity(lights.td, 0)
-SetLightIntensity(lights.te, 0)
-SetLightIntensity(lights.td2, 0)
-SetLightIntensity(lights.te2, 0)
-SetLightIntensity(lights.td3, 0)
-SetLightIntensity(lights.te3, 0)
-SetLightIntensity(lights.td4, 0)
-SetLightIntensity(lights.te4, 0)
-SetLightIntensity(lights.td5, 0)
-SetLightIntensity(lights.te5, 0)
-SetLightIntensity(lights.rd, 0)
-SetLightIntensity(lights.rd2, 0)
-SetLightIntensity(lights.re, 0)
-SetLightIntensity(lights.rtd, 0)
-SetLightIntensity(lights.rte, 0)
-SetLightIntensity(lights.rte2, 0)
-SetLightIntensity(lights.fd, 0)
-SetLightIntensity(lights.fe, 0)
-SetLightIntensity(lights.fd2, 0)
-SetLightIntensity(lights.fe2, 0)
-
-
-	end
-
-
-	if elight2 then
-			local period = 60
-			local t = frame%period
-			--toplights
-			if t == 0 then 	am1 = 1 end
-			if t == 5 then am1 = 0 end
-			if t == 10 then am1 = 1 end
-			if t == 15 then am1 = 0 end
-			if t == 20 then am1 = 1 end
-			if t == 25 then am1 = 0 end
-
-			if t == 5 then am2 = 1 end
-			if t == 15 then am2 = 0 end
-			if t == 10 then am3 = 1 end
-			if t == 20 then am3 = 0 end
-			if t == 40 then am2 = 1 end
-			if t == 50 then am2 = 0 end
-			if t == 35 then am3 = 1 end
-			if t == 45 then am3 = 0 end
-
-
-			if t == 30 then am4 = 1 end
-			if t == 35 then am4 = 0 end
-			if t == 40 then am4 = 1 end
-			if t == 45 then am4 = 0 end
-			if t == 50 then am4 = 1 end
-			if t == 55 then am4 = 0 end
-
-			if t == 20 then am5 = 1 end
-			if t == 35 then am5 = 0 end
-
-			if t == 30 then am6 = 1 end
-			if t == 35 then am6 = 0 end
-			if t == 40 then am6 = 1 end
-			if t == 45 then am6 = 0 end
-			if t == 50 then am6 = 1 end
-			if t == 55 then am6 = 0 end
-
-			if t == 10 then am7 = 1 end
-			if t == 20 then am7 = 0 end
-			if t == 5 then am8 = 1 end
-			if t == 15 then am8 = 0 end
-			if t == 35 then am7 = 1 end
-			if t == 45 then am7 = 0 end
-			if t == 40 then am8 = 1 end
-			if t == 50 then am8 = 0 end
-
-			if t == 0 then am9 = 1 end
-			if t == 5 then am9 = 0 end
-			if t == 10 then am9 = 1 end
-			if t == 15 then am9 = 0 end
-			if t == 20 then am9 = 1 end
-			if t == 25 then am9 = 0 end
-
-
-
-
-			--Red
-			if t == 0 then 	es = 1	end
-			if t == 5 then es = 0	end
-			if t == 10 then es = 1 	end
-			if t == 30 then es = 0	end
-
-			--Blue
-			if t == 30 then di = 1 	end
-			if t == 35 then di = 0	end
-			if t == 40 then di = 1 	end
-			if t == 59 then di = 0	end
-
-
-
-			--farol
-			if t == 0 then 	fa1 = 1 end
-			if t == 5 then fa1 = 0 end
-			if t == 10 then fa1 = 1 end
-			if t == 30 then fa1 = 0 end
-
-			if t == 30 then fa2 = 1 end
-			if t == 35 then fa2 = 0	end
-			if t == 40 then fa2 = 1 end
-			if t == 59 then fa2 = 0	end
-
-			--farol luz
-			if t == 0 then 	fa3 = 10 end
-			if t == 5 then fa3 = 0 end
-			if t == 10 then fa3 = 10 end
-			if t == 30 then fa3 = 0 end
-
-			if t == 30 then fa4 = 10 end
-			if t == 35 then fa4 = 0	end
-			if t == 40 then fa4 = 10 end
-			if t == 59 then fa4 = 0	end
-
-			if t == 0 then 	fa5 = 1 end
-			if t == 5 then fa5 = 0 end
-			if t == 10 then fa5 = 1 end
-			if t == 30 then fa5 = 0 end
-
-			if t == 30 then fa6 = 1 end
-			if t == 35 then fa6 = 0	end
-			if t == 40 then fa6 = 1 end
-			if t == 59 then fa6 = 0	end
-
-
-
-SetShapeEmissiveScale(shapes.ab1, am1)
-SetShapeEmissiveScale(shapes.ab2, am2)
-SetShapeEmissiveScale(shapes.ab3, am3)
-SetShapeEmissiveScale(shapes.ab4, am4)
-SetShapeEmissiveScale(shapes.ab5, am5)
-SetShapeEmissiveScale(shapes.ab6, am6)
-SetShapeEmissiveScale(shapes.ab7, am7)
-SetShapeEmissiveScale(shapes.ab8, am8)
-SetShapeEmissiveScale(shapes.ab9, am9)
-SetShapeEmissiveScale(shapes.ab10, am1)
-SetShapeEmissiveScale(shapes.ab11, am2)
-SetShapeEmissiveScale(shapes.ab12, am3)
-SetShapeEmissiveScale(shapes.ab13, am4)
-SetShapeEmissiveScale(shapes.ab14, am5)
-SetShapeEmissiveScale(shapes.ab15, am6)
-SetShapeEmissiveScale(shapes.ab16, am7)
-SetShapeEmissiveScale(shapes.ab17, am8)
-SetShapeEmissiveScale(shapes.ab18, am9)
-
-SetShapeEmissiveScale(shapes.td, di)
-SetShapeEmissiveScale(shapes.te, es)
-SetShapeEmissiveScale(shapes.td2, di)
-SetShapeEmissiveScale(shapes.te2, es)
-SetShapeEmissiveScale(shapes.rd, di)
-SetShapeEmissiveScale(shapes.re, es)
-SetShapeEmissiveScale(shapes.rtd, di)
-SetShapeEmissiveScale(shapes.rte, es)
-SetShapeEmissiveScale(shapes.fd, di)
-SetShapeEmissiveScale(shapes.fe, es)
-SetShapeEmissiveScale(shapes.fd2, di)
-SetShapeEmissiveScale(shapes.fe2, es)
-
-SetLightIntensity(lights.ab1, am1)
-SetLightIntensity(lights.ab2, am2)
-SetLightIntensity(lights.ab3, am3)
-SetLightIntensity(lights.ab4, am4)
-SetLightIntensity(lights.ab5, am5)
-SetLightIntensity(lights.ab6, am6)
-SetLightIntensity(lights.ab7, am7)
-SetLightIntensity(lights.ab8, am8)
-SetLightIntensity(lights.ab9, am9)
-SetLightIntensity(lights.ab10, am1)
-SetLightIntensity(lights.ab11, am2)
-SetLightIntensity(lights.ab12, am3)
-SetLightIntensity(lights.ab13, am4)
-SetLightIntensity(lights.ab14, am5)
-SetLightIntensity(lights.ab15, am6)
-SetLightIntensity(lights.ab16, am7)
-SetLightIntensity(lights.ab17, am8)
-SetLightIntensity(lights.ab18, am9)
-
-SetLightIntensity(lights.td, di)
-SetLightIntensity(lights.te, es)
-SetLightIntensity(lights.td2, di)
-SetLightIntensity(lights.te2, es)
-SetLightIntensity(lights.td3, di)
-SetLightIntensity(lights.te3, es)
-SetLightIntensity(lights.td4, di)
-SetLightIntensity(lights.te4, di)
-SetLightIntensity(lights.td5, di)
-SetLightIntensity(lights.te5, es)
-SetLightIntensity(lights.rd, di)
-SetLightIntensity(lights.rd2, di)
-SetLightIntensity(lights.re, es)
-SetLightIntensity(lights.rtd, di)
-SetLightIntensity(lights.rte, es)
-SetLightIntensity(lights.rte2, es)
-SetLightIntensity(lights.fd, di)
-SetLightIntensity(lights.fe, es)
-SetLightIntensity(lights.fd2, di)
-SetLightIntensity(lights.fe2, es)
-SetShapeEmissiveScale(shapes.lflm2, fa1)
-SetLightIntensity(lights.lflml2, fa3)
-SetShapeEmissiveScale(shapes.lfrm2, fa2)
-SetLightIntensity(lights.lflmr2, fa4)
-SetShapeEmissiveScale(shapes.lflmt2, fa1)
-SetLightIntensity(lights.lflmlt2, fa5)
-SetShapeEmissiveScale(shapes.lfrmt2, fa2)
-SetLightIntensity(lights.lfrmrt2, fa6)
-
-
-	end
+    if siren then
+
+    PlayLoop(loop)
+
+    end
+    if siren2 then
+
+    PlayLoop(loop2)
+
+    end
 end
+

```

---

# Migration Report: main\ball_crane\arm.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\ball_crane\arm.lua
+++ patched/main\ball_crane\arm.lua
@@ -1,30 +1,35 @@
-function init()
-	arm = nil
-	speed = 0
+#version 2
+function server.init()
+    arm = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"arm") then	
-		if arm == nil then
-			arm = FindJoint(GetTagValue(GetPlayerVehicle(),"arm"),true)
-			SetJointMotor(arm, speed)	
-		end
-	else
-		arm = nil
-	end
-	
-	local lmb, rmb = InputPressed("x"), InputPressed("c")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"arm") then	
+        	if arm == nil then
+        		arm = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"arm"),true)
+        		SetJointMotor(arm, speed)	
+        	end
+        else
+        	arm = nil
+        end
+        	if lmb then
+        		if speed < .1 then
+        			speed = speed + .1
+        			SetJointMotor(arm, speed)	
+        		end
+        	elseif rmb then
+        		if speed > -.1 then
+        			speed = speed - .1
+        			SetJointMotor(arm, speed)	
+        		end
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .1 then
-				speed = speed + .1
-				SetJointMotor(arm, speed)	
-			end
-		elseif rmb then
-			if speed > -.1 then
-				speed = speed - .1
-				SetJointMotor(arm, speed)	
-			end
-		end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputPressed("x"), InputPressed("c")
 end
-	+

```

---

# Migration Report: main\ball_crane\ball.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\ball_crane\ball.lua
+++ patched/main\ball_crane\ball.lua
@@ -1,30 +1,35 @@
-function init()
-	ball = nil
-	speed = 0
+#version 2
+function server.init()
+    ball = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"ball") then	
-		if ball == nil then
-			ball = FindJoint(GetTagValue(GetPlayerVehicle(),"ball"),true)
-			SetJointMotor(ball, speed)	
-		end
-	else
-		ball = nil
-	end
-	
-	local lmb, rmb = InputPressed("lmb"), InputPressed("rmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"ball") then	
+        	if ball == nil then
+        		ball = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"ball"),true)
+        		SetJointMotor(ball, speed)	
+        	end
+        else
+        	ball = nil
+        end
+        	if lmb then
+        		if speed < 2 then
+        			speed = speed + .5
+        			SetJointMotor(ball, speed)	
+        		end
+        	elseif rmb then
+        		if speed > -2 then
+        			speed = speed - .5
+        			SetJointMotor(ball, speed)	
+        		end
+        	end
+    end
+end
 
-		if lmb then
-			if speed < 2 then
-				speed = speed + .5
-				SetJointMotor(ball, speed)	
-			end
-		elseif rmb then
-			if speed > -2 then
-				speed = speed - .5
-				SetJointMotor(ball, speed)	
-			end
-		end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputPressed("lmb"), InputPressed("rmb")
 end
-	+

```

---

# Migration Report: main\ball_crane\crane.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\ball_crane\crane.lua
+++ patched/main\ball_crane\crane.lua
@@ -1,34 +1,36 @@
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "arm") then
-		local info = {}
-        info[#info+1] = {"Wrecking Ball", "Arm Control"}
-		info[#info+1] = {"X", "Arm Lower"}
-		info[#info+1] = {"C", "Arm Raise"}
-        info[#info+1] = {"LMB", "Rotate Left"}
-		info[#info+1] = {"RMB", "Rotate Right"}
-		info[#info+1] = {"Press Again", "Change Speed"}
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
-	end
-end+#version 2
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "arm") then
+    	local info = {}
+           info[#info+1] = {"Wrecking Ball", "Arm Control"}
+    	info[#info+1] = {"X", "Arm Lower"}
+    	info[#info+1] = {"C", "Arm Raise"}
+           info[#info+1] = {"LMB", "Rotate Left"}
+    	info[#info+1] = {"RMB", "Rotate Right"}
+    	info[#info+1] = {"Press Again", "Change Speed"}
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
+    end
+end
+

```

---

# Migration Report: main\bull_dozer\blade.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\blade.lua
+++ patched/main\bull_dozer\blade.lua
@@ -1,30 +1,35 @@
-function init()
-	blade = nil
-	speed = 0
+#version 2
+function server.init()
+    blade = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"blade") then	
-		if blade == nil then
-			blade = FindJoint(GetTagValue(GetPlayerVehicle(),"blade"),true)
-			SetJointMotor(blade, speed)	
-		end
-	else
-		blade = nil
-	end
-	
-	local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"blade") then	
+        	if blade == nil then
+        		blade = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"blade"),true)
+        		SetJointMotor(blade, speed)	
+        	end
+        else
+        	blade = nil
+        end
+        	if lmb then
+        		if speed < .3 then
+        			speed = speed + .3
+        			SetJointMotor(blade, speed)	
+        		end	
+        	elseif rmb then
+        		if speed > -.3 then
+        			speed = speed - .3
+        			SetJointMotor(blade, speed)	
+        		end	
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .3 then
-				speed = speed + .3
-				SetJointMotor(blade, speed)	
-			end	
-		elseif rmb then
-			if speed > -.3 then
-				speed = speed - .3
-				SetJointMotor(blade, speed)	
-			end	
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+end
+

```

---

# Migration Report: main\bull_dozer\blade2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\blade2.lua
+++ patched/main\bull_dozer\blade2.lua
@@ -1,30 +1,35 @@
-function init()
-	blade2 = nil
-	speed = 0
+#version 2
+function server.init()
+    blade2 = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"blade2") then	
-		if blade2 == nil then
-			blade2 = FindJoint(GetTagValue(GetPlayerVehicle(),"blade2"),true)
-			SetJointMotor(blade2, speed)	
-		end
-	else
-		blade2 = nil
-	end
-	
-	local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"blade2") then	
+        	if blade2 == nil then
+        		blade2 = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"blade2"),true)
+        		SetJointMotor(blade2, speed)	
+        	end
+        else
+        	blade2 = nil
+        end
+        	if lmb then
+        		if speed < .2 then
+        			speed = speed + .2
+        			SetJointMotor(blade2, speed)	
+        		end	
+        	elseif rmb then
+        		if speed > -.2 then
+        			speed = speed - .2
+        			SetJointMotor(blade2, speed)	
+        		end	
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .2 then
-				speed = speed + .2
-				SetJointMotor(blade2, speed)	
-			end	
-		elseif rmb then
-			if speed > -.2 then
-				speed = speed - .2
-				SetJointMotor(blade2, speed)	
-			end	
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+end
+

```

---

# Migration Report: main\bull_dozer\blade3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\blade3.lua
+++ patched/main\bull_dozer\blade3.lua
@@ -1,30 +1,35 @@
-function init()
-	blade3 = nil
-	speed = 0
+#version 2
+function server.init()
+    blade3 = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"blade3") then	
-		if blade3 == nil then
-			blade3 = FindJoint(GetTagValue(GetPlayerVehicle(),"blade3"),true)
-			SetJointMotor(blade3, speed)	
-		end
-	else
-		blade3 = nil
-	end
-	
-	local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"blade3") then	
+        	if blade3 == nil then
+        		blade3 = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"blade3"),true)
+        		SetJointMotor(blade3, speed)	
+        	end
+        else
+        	blade3 = nil
+        end
+        	if lmb then
+        		if speed < .3 then
+        			speed = speed + .3
+        			SetJointMotor(blade3, speed)	
+        		end	
+        	elseif rmb then
+        		if speed > -.3 then
+        			speed = speed - .3
+        			SetJointMotor(blade3, speed)	
+        		end	
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .3 then
-				speed = speed + .3
-				SetJointMotor(blade3, speed)	
-			end	
-		elseif rmb then
-			if speed > -.3 then
-				speed = speed - .3
-				SetJointMotor(blade3, speed)	
-			end	
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+end
+

```

---

# Migration Report: main\bull_dozer\blade4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\blade4.lua
+++ patched/main\bull_dozer\blade4.lua
@@ -1,30 +1,35 @@
-function init()
-	blade4 = nil
-	speed = 0
+#version 2
+function server.init()
+    blade4 = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"blade4") then	
-		if blade4 == nil then
-			blade4 = FindJoint(GetTagValue(GetPlayerVehicle(),"blade4"),true)
-			SetJointMotor(blade4, speed)	
-		end
-	else
-		blade4 = nil
-	end
-	
-	local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"blade4") then	
+        	if blade4 == nil then
+        		blade4 = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"blade4"),true)
+        		SetJointMotor(blade4, speed)	
+        	end
+        else
+        	blade4 = nil
+        end
+        	if lmb then
+        		if speed < .2 then
+        			speed = speed + .2
+        			SetJointMotor(blade4, speed)	
+        		end	
+        	elseif rmb then
+        		if speed > -.2 then
+        			speed = speed - .2
+        			SetJointMotor(blade4, speed)	
+        		end	
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .2 then
-				speed = speed + .2
-				SetJointMotor(blade4, speed)	
-			end	
-		elseif rmb then
-			if speed > -.2 then
-				speed = speed - .2
-				SetJointMotor(blade4, speed)	
-			end	
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputDown("rmb"), InputDown("lmb")
+end
+

```

---

# Migration Report: main\bull_dozer\dozer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\dozer.lua
+++ patched/main\bull_dozer\dozer.lua
@@ -1,33 +1,35 @@
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "dozer") then
-		local info = {}
-        info[#info+1] = {"Blade & Ripper", "Control"}
-		info[#info+1] = {"LMB", "Blade Up"}
-		info[#info+1] = {"RMB", "Blade Down"}
-        info[#info+1] = {"X", "Ripper Up"}
-		info[#info+1] = {"C", "Ripper Down"}
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
-	end
-end+#version 2
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "dozer") then
+    	local info = {}
+           info[#info+1] = {"Blade & Ripper", "Control"}
+    	info[#info+1] = {"LMB", "Blade Up"}
+    	info[#info+1] = {"RMB", "Blade Down"}
+           info[#info+1] = {"X", "Ripper Up"}
+    	info[#info+1] = {"C", "Ripper Down"}
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
+    end
+end
+

```

---

# Migration Report: main\bull_dozer\rip.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\rip.lua
+++ patched/main\bull_dozer\rip.lua
@@ -1,30 +1,35 @@
-function init()
-	rip = nil
-	speed = 0
+#version 2
+function server.init()
+    rip = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"rip") then	
-		if rip == nil then
-			rip = FindJoint(GetTagValue(GetPlayerVehicle(),"rip"),true)
-			SetJointMotor(rip, speed)	
-		end
-	else
-		rip = nil
-	end
-	
-	local lmb, rmb = InputDown("c"), InputDown("x")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"rip") then	
+        	if rip == nil then
+        		rip = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"rip"),true)
+        		SetJointMotor(rip, speed)	
+        	end
+        else
+        	rip = nil
+        end
+        	if lmb then
+        		if speed < .3 then
+        			speed = speed + .3
+        			SetJointMotor(rip, speed)	
+        		end	
+        	elseif rmb then
+        		if speed > -.3 then
+        			speed = speed - .3
+        			SetJointMotor(rip, speed)	
+        		end	
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .3 then
-				speed = speed + .3
-				SetJointMotor(rip, speed)	
-			end	
-		elseif rmb then
-			if speed > -.3 then
-				speed = speed - .3
-				SetJointMotor(rip, speed)	
-			end	
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputDown("c"), InputDown("x")
+end
+

```

---

# Migration Report: main\bull_dozer\rip2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\rip2.lua
+++ patched/main\bull_dozer\rip2.lua
@@ -1,30 +1,35 @@
-function init()
-	rip2 = nil
-	speed = 0
+#version 2
+function server.init()
+    rip2 = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"rip2") then	
-		if rip2 == nil then
-			rip2 = FindJoint(GetTagValue(GetPlayerVehicle(),"rip2"),true)
-			SetJointMotor(rip2, speed)	
-		end
-	else
-		rip2 = nil
-	end
-	
-	local lmb, rmb = InputDown("c"), InputDown("x")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"rip2") then	
+        	if rip2 == nil then
+        		rip2 = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"rip2"),true)
+        		SetJointMotor(rip2, speed)	
+        	end
+        else
+        	rip2 = nil
+        end
+        	if lmb then
+        		if speed < .3 then
+        			speed = speed + .3
+        			SetJointMotor(rip2, speed)	
+        		end	
+        	elseif rmb then
+        		if speed > -.3 then
+        			speed = speed - .3
+        			SetJointMotor(rip2, speed)	
+        		end	
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .3 then
-				speed = speed + .3
-				SetJointMotor(rip2, speed)	
-			end	
-		elseif rmb then
-			if speed > -.3 then
-				speed = speed - .3
-				SetJointMotor(rip2, speed)	
-			end	
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputDown("c"), InputDown("x")
+end
+

```

---

# Migration Report: main\bull_dozer\rip3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\bull_dozer\rip3.lua
+++ patched/main\bull_dozer\rip3.lua
@@ -1,30 +1,35 @@
-function init()
-	rip3 = nil
-	speed = 0
+#version 2
+function server.init()
+    rip3 = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"rip3") then	
-		if rip3 == nil then
-			rip3 = FindJoint(GetTagValue(GetPlayerVehicle(),"rip3"),true)
-			SetJointMotor(rip, speed)	
-		end
-	else
-		rip3 = nil
-	end
-	
-	local lmb, rmb = InputDown("c"), InputDown("x")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"rip3") then	
+        	if rip3 == nil then
+        		rip3 = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"rip3"),true)
+        		SetJointMotor(rip, speed)	
+        	end
+        else
+        	rip3 = nil
+        end
+        	if lmb then
+        		if speed < .35 then
+        			speed = speed + .35
+        			SetJointMotor(rip3, speed)	
+        		end	
+        	elseif rmb then
+        		if speed > -.35 then
+        			speed = speed - .35
+        			SetJointMotor(rip3, speed)	
+        		end	
+        	end
+    end
+end
 
-		if lmb then
-			if speed < .35 then
-				speed = speed + .35
-				SetJointMotor(rip3, speed)	
-			end	
-		elseif rmb then
-			if speed > -.35 then
-				speed = speed - .35
-				SetJointMotor(rip3, speed)	
-			end	
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputDown("c"), InputDown("x")
+end
+

```

---

# Migration Report: main\chopper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\chopper.lua
+++ patched/main\chopper.lua
@@ -1,17 +1,4 @@
-GroundProximityDetection = true
-
-config = {
-	["ah_64"] = {},
-	["mh_60"] = {},
-	["mi_17"] = {},
-	["mi_24"] = {weaponLoc = Vec(-0.05, 0.95, -9), music = "MOD/katyusha.ogg"},
-	["uh_1"] = {weaponLoc = Vec(0.0, -0.9, -3.3), music = "MOD/fortunate_son.ogg"},
-	["ka_50"] = {weaponLoc = Vec(0.85, 1.1, -3.9), music = "MOD/soviet_anthem.ogg", rotors = "coaxial"},
-	["av_8"] = {weaponLoc = Vec(-0.55, 0.65, -2.5)},
-	["mh_60medic"] = {},
-	["delorean"] = {}
-}
-
+#version 2
 function EulerQuat(q, k)
 	local x, y, z, w = q[1], q[2], q[3], q[4]
 	local bank, heading, attitude
@@ -51,7 +38,7 @@
 function sign(x)
 	if x < 0 then
 		return -1
-	elseif x > 0 then
+	elseif x ~= 0 then
 		return 1
 	else
 		return 0
@@ -74,231 +61,217 @@
 	return yaw
 end
 
-function init()
-	chopper = {}
-	chopper.body = FindBody("chopper")
-	chopper.transform = GetBodyTransform(chopper.body)
-
-	chopper.mainRotor = FindBody("mainrotor")
-	chopper.mainRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.mainRotor))
-
-	chopper.tailRotor = FindBody("tailrotor")
-	chopper.tailRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.tailRotor))
-
-	chopper.angle = 0.0
-	chopper.mass = GetBodyMass(chopper.body)
-	chopper.sound = LoadLoop("chopper-loop.ogg")
-
-	shootSound = LoadSound("chopper-shoot0.ogg")
-	rocketSound = LoadSound("tools/launcher0.ogg")
-
-	pitch = 0
-	yaw = 0
-	roll = 0
-	collective = chopper.transform.pos[2] + 0.5 -- Starting altitude
-
-	cameraX = 0
-	cameraY = 0
-	zoom = 20
-
-	vehicleType = GetTagValue(chopper.body, "chopper")
-	if config[vehicleType].music then
-		music = config[vehicleType].music
-	end
-	if not HasTag(chopper.body, "avf") and config[vehicleType].weaponLoc then
-		weaponLoc = config[vehicleType].weaponLoc
-	end
-	if HasTag(chopper.body, "avf") then
-		isAVF = true
-	end
-	isCoaxial = false
-	if config[vehicleType].rotors then
-		isCoaxial = true
-	end
-
-	playing = true -- Default: false
-	aimMode = false
-	hover = false
-	dynamicRotor = true
-end
-
-
-function tick(dt)
-	local vehicle = GetPlayerVehicle()
-	if vehicle ~= FindVehicle("helicopter") then
-		if not dynamicRotor then -- Player leaves the chopper
-			dynamicRotor = true
-			SetBodyDynamic(chopper.mainRotor, true)
-			SetBodyAngularVelocity(chopper.body, Vec())
-			SetPlayerVehicle(0)
-			pitch = 0
-			roll = 0
-			cameraY = pitch
-			local playerSpawn = TransformToParentPoint(chopper.transform, Vec(2, 0, -4))
-			local playerRot = QuatEuler(pitch, yaw, roll)
-			SetPlayerTransform(Transform(playerSpawn, playerRot))
-		end
-		return
-	elseif GetBodyMass(chopper.body) < chopper.mass * 0.66 then
-		if not dynamicRotor then -- Helicopter is too damaged
-			dynamicRotor = true
-			SetBodyDynamic(chopper.mainRotor, true)
-		end
-		return
-	else
-		if dynamicRotor then -- Player enter the chopper
-			dynamicRotor = false
-			SetBodyDynamic(chopper.mainRotor, false)
-			chopper.transform.pos = GetBodyTransform(chopper.body).pos -- Update chopper position
-			local unused = 0
-			unused, yaw = EulerQuat(GetBodyTransform(chopper.body).rot) -- Update yaw rotation
-			cameraX = yaw
-			collective = chopper.transform.pos[2] + 0.5
-		end
-		if music and not playing then
-			playing = true
-			PlayMusic(music)
-		end
-	end
-
-	if InputDown("w") then
-		collective = collective + 0.1
-	end
-	if InputDown("s") and collective > 0 then
-		collective = collective - 0.1
-	end
-
-	if InputDown("a") and roll < 30 then
-		roll = roll + 0.5
-	end
-	if InputDown("d") and roll > -30 then
-		roll = roll - 0.5
-	end
-
-	if weaponLoc then
-		local firePos = TransformToParentPoint(chopper.transform, weaponLoc)
-		local fireDir = TransformToParentVec(chopper.transform, Vec(0, 0, -1))
-		if vehicleType == "mh_60" then
-			fireDir = VecNormalize(TransformToParentVec(chopper.transform, Vec(2, -1, 0)))
-			if InputDown("lmb") then
-				PlaySound(shootSound, chopper.transform.pos, 5)
-				Shoot(firePos, fireDir, 0)
-			end
-		else
-			if InputPressed("lmb") then
-				PlaySound(shootSound, chopper.transform.pos, 5)
-				Shoot(firePos, fireDir, 0)
-			end
-			if InputPressed("rmb") then
-				PlaySound(rocketSound, chopper.transform.pos, 5)
-				Shoot(firePos, fireDir, 1)
-			end
-		end
-	elseif isAVF then
-		if InputPressed("rmb") then
-			aimMode = not aimMode
-		end
-	end
-	if InputPressed("h") then
-		hover = not hover
-	end
-
-	local prevYaw = yaw
-
-	if not aimMode then
-		local x, y = EulerQuat(GetCameraTransform().rot)
-
-		if x < pitch and pitch > -45 then
-			pitch = pitch - 0.5
-		end
-		if x > pitch and pitch < 15 then
-			pitch = pitch + 0.5
-		end
-
-		if y < yaw and not (y < yaw - 180) then
-			yaw = YawRight(yaw)
-		elseif y < yaw - 180 then
-			yaw = YawLeft(yaw)
-		end
-
-		if y > yaw and not (y > yaw + 180) then
-			yaw = YawLeft(yaw)
-		elseif y > yaw + 180 then
-			yaw = YawRight(yaw)
-		end
-	else
-		local mouseX = -InputValue("mousedx")
-		local mouseY = -InputValue("mousedy")
-
-		if sign(mouseY) < 0 and pitch > -45 then
-			pitch = pitch - 0.5
-		elseif sign(mouseY) > 0 and pitch < 15 then
-			pitch = pitch + 0.5
-		end
-
-		if sign(mouseX) < 0 then
-			yaw = YawRight(yaw)
-		elseif sign(mouseX) > 0 then
-			yaw = YawLeft(yaw)
-		end
-	end
-
-	if hover then
-		if pitch ~= 0 then
-			pitch = pitch - sign(pitch)
-		end
-		yaw = prevYaw
-	end
-
-	local moveDir = Vec(0.01 * -roll, 0, 0.01 * pitch)
-	local pos = TransformToParentPoint(chopper.transform, moveDir)
-
-	if GroundProximityDetection then
-		pos[2] = pos[2] - 0.1
-		local dir = VecNormalize(VecSub(pos, chopper.transform.pos))
-		local maxDist = 0.5 + math.abs(pitch / 5) + math.abs(roll / 10)
-		QueryRejectBody(chopper.body)
-		QueryRequire("physical large")
-		local hit, dist = QueryRaycast(chopper.transform.pos, dir, maxDist)
-		--local posEnd = VecAdd(chopper.transform.pos, VecScale(dir, maxDist))
-		if hit then
-			collective = collective + (maxDist - dist) / (2 * maxDist)
-		end
-	end
-	pos[2] = collective
-
-	chopper.angle = chopper.angle + 0.6
-	local rot = QuatEuler(math.sin(chopper.angle*0.053)*5 + pitch, math.sin(chopper.angle*0.04)*5 + yaw, roll)
-
-	if aimMode then
-		rot = QuatEuler(pitch, yaw, roll)
-	end
-
-	chopper.transform.pos = pos
-	chopper.transform.rot = rot
-	SetBodyTransform(chopper.body, chopper.transform)
-
-	chopper.mainRotorLocalTransform.rot = QuatEuler(0, chopper.angle * 57, 0)
-	SetBodyTransform(chopper.mainRotor, TransformToParentTransform(chopper.transform, chopper.mainRotorLocalTransform))
-
-	if isCoaxial then
-		chopper.tailRotorLocalTransform.rot = QuatEuler(0, -chopper.angle * 57, 0)
-	else
-		chopper.tailRotorLocalTransform.rot = QuatEuler(chopper.angle * 57, 0, 0)
-	end
-	SetBodyTransform(chopper.tailRotor, TransformToParentTransform(chopper.transform, chopper.tailRotorLocalTransform))
-
-	PlayLoop(chopper.sound, chopper.transform.pos, 10)
-
-	local mx, my = InputValue("mousedx"), InputValue("mousedy")
-	cameraX = cameraX - mx / 10
-	cameraY = cameraY - my / 10
-	cameraY = clamp(cameraY, -90, 90)
-	local cameraRot = QuatEuler(cameraY, cameraX, 0)
-	local cameraT = Transform(chopper.transform.pos, cameraRot)
-	zoom = zoom - InputValue("mousewheel")
-	zoom = clamp(zoom, 10, 30)
-	local cameraPos = TransformToParentPoint(cameraT, Vec(0, 5, zoom))
-	local camera = Transform(cameraPos, cameraRot)
-	SetCameraTransform(camera)
-end
+function server.init()
+    chopper = {}
+    chopper.body = FindBody("chopper")
+    chopper.transform = GetBodyTransform(chopper.body)
+    chopper.mainRotor = FindBody("mainrotor")
+    chopper.mainRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.mainRotor))
+    chopper.tailRotor = FindBody("tailrotor")
+    chopper.tailRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.tailRotor))
+    chopper.angle = 0.0
+    chopper.mass = GetBodyMass(chopper.body)
+    chopper.sound = LoadLoop("chopper-loop.ogg")
+    pitch = 0
+    yaw = 0
+    roll = 0
+    collective = chopper.transform.pos[2] + 0.5 -- Starting altitude
+    cameraX = 0
+    cameraY = 0
+    zoom = 20
+    vehicleType = GetTagValue(chopper.body, "chopper")
+    if config[vehicleType].music then
+    	music = config[vehicleType].music
+    end
+    if not HasTag(chopper.body, "avf") and config[vehicleType].weaponLoc then
+    	weaponLoc = config[vehicleType].weaponLoc
+    end
+    if HasTag(chopper.body, "avf") then
+    	isAVF = true
+    end
+    isCoaxial = false
+    if config[vehicleType].rotors then
+    	isCoaxial = true
+    end
+    playing = true -- Default: false
+    aimMode = false
+    hover = false
+    dynamicRotor = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local vehicle = GetPlayerVehicle(playerId)
+        if vehicle ~= FindVehicle("helicopter") then
+        	if not dynamicRotor then -- Player leaves the chopper
+        		dynamicRotor = true
+        		SetBodyDynamic(chopper.mainRotor, true)
+        		SetBodyAngularVelocity(chopper.body, Vec())
+        		SetPlayerVehicle(playerId, 0)
+        		pitch = 0
+        		roll = 0
+        		cameraY = pitch
+        		local playerSpawn = TransformToParentPoint(chopper.transform, Vec(2, 0, -4))
+        		local playerRot = QuatEuler(pitch, yaw, roll)
+        		SetPlayerTransform(playerId, Transform(playerSpawn, playerRot))
+        	end
+        	return
+        elseif GetBodyMass(chopper.body) < chopper.mass * 0.66 then
+        	if not dynamicRotor then -- Helicopter is too damaged
+        		dynamicRotor = true
+        		SetBodyDynamic(chopper.mainRotor, true)
+        	end
+        	return
+        else
+        	if dynamicRotor then -- Player enter the chopper
+        		dynamicRotor = false
+        		SetBodyDynamic(chopper.mainRotor, false)
+        		chopper.transform.pos = GetBodyTransform(chopper.body).pos -- Update chopper position
+        		local unused = 0
+        		unused, yaw = EulerQuat(GetBodyTransform(chopper.body).rot) -- Update yaw rotation
+        		cameraX = yaw
+        		collective = chopper.transform.pos[2] + 0.5
+        	end
+        	if music and not playing then
+        		playing = true
+        		PlayMusic(music)
+        	end
+        end
+        local prevYaw = yaw
+        if hover then
+        	if pitch ~= 0 then
+        		pitch = pitch - sign(pitch)
+        	end
+        	yaw = prevYaw
+        end
+        local moveDir = Vec(0.01 * -roll, 0, 0.01 * pitch)
+        local pos = TransformToParentPoint(chopper.transform, moveDir)
+        if GroundProximityDetection then
+        	pos[2] = pos[2] - 0.1
+        	local dir = VecNormalize(VecSub(pos, chopper.transform.pos))
+        	local maxDist = 0.5 + math.abs(pitch / 5) + math.abs(roll / 10)
+        	QueryRejectBody(chopper.body)
+        	QueryRequire("physical large")
+        	local hit, dist = QueryRaycast(chopper.transform.pos, dir, maxDist)
+        	--local posEnd = VecAdd(chopper.transform.pos, VecScale(dir, maxDist))
+        	if hit then
+        		collective = collective + (maxDist - dist) / (2 * maxDist)
+        	end
+        end
+        pos[2] = collective
+        chopper.angle = chopper.angle + 0.6
+        local rot = QuatEuler(math.sin(chopper.angle*0.053)*5 + pitch, math.sin(chopper.angle*0.04)*5 + yaw, roll)
+        if aimMode then
+        	rot = QuatEuler(pitch, yaw, roll)
+        end
+        chopper.transform.pos = pos
+        chopper.transform.rot = rot
+        SetBodyTransform(chopper.body, chopper.transform)
+        chopper.mainRotorLocalTransform.rot = QuatEuler(0, chopper.angle * 57, 0)
+        SetBodyTransform(chopper.mainRotor, TransformToParentTransform(chopper.transform, chopper.mainRotorLocalTransform))
+        if isCoaxial then
+        	chopper.tailRotorLocalTransform.rot = QuatEuler(0, -chopper.angle * 57, 0)
+        else
+        	chopper.tailRotorLocalTransform.rot = QuatEuler(chopper.angle * 57, 0, 0)
+        end
+        SetBodyTransform(chopper.tailRotor, TransformToParentTransform(chopper.transform, chopper.tailRotorLocalTransform))
+        cameraX = cameraX - mx / 10
+        cameraY = cameraY - my / 10
+        cameraY = clamp(cameraY, -90, 90)
+        local cameraRot = QuatEuler(cameraY, cameraX, 0)
+        local cameraT = Transform(chopper.transform.pos, cameraRot)
+        zoom = clamp(zoom, 10, 30)
+        local cameraPos = TransformToParentPoint(cameraT, Vec(0, 5, zoom))
+        local camera = Transform(cameraPos, cameraRot)
+        SetCameraTransform(camera)
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("chopper-shoot0.ogg")
+    rocketSound = LoadSound("tools/launcher0.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputDown("w") then
+    	collective = collective + 0.1
+    end
+    if InputDown("s") and collective ~= 0 then
+    	collective = collective - 0.1
+    end
+    if InputDown("a") and roll < 30 then
+    	roll = roll + 0.5
+    end
+    if InputDown("d") and roll > -30 then
+    	roll = roll - 0.5
+    end
+    if weaponLoc then
+    	local firePos = TransformToParentPoint(chopper.transform, weaponLoc)
+    	local fireDir = TransformToParentVec(chopper.transform, Vec(0, 0, -1))
+    	if vehicleType == "mh_60" then
+    		fireDir = VecNormalize(TransformToParentVec(chopper.transform, Vec(2, -1, 0)))
+    		if InputDown("lmb") then
+    			PlaySound(shootSound, chopper.transform.pos, 5)
+    			Shoot(firePos, fireDir, 0)
+    		end
+    	else
+    		if InputPressed("lmb") then
+    			PlaySound(shootSound, chopper.transform.pos, 5)
+    			Shoot(firePos, fireDir, 0)
+    		end
+    		if InputPressed("rmb") then
+    			PlaySound(rocketSound, chopper.transform.pos, 5)
+    			Shoot(firePos, fireDir, 1)
+    		end
+    	end
+    elseif isAVF then
+    	if InputPressed("rmb") then
+    		aimMode = not aimMode
+    	end
+    end
+    if InputPressed("h") then
+    	hover = not hover
+    end
+    if not aimMode then
+    	local x, y = EulerQuat(GetCameraTransform().rot)
+
+    	if x < pitch and pitch > -45 then
+    		pitch = pitch - 0.5
+    	end
+    	if x > pitch and pitch < 15 then
+    		pitch = pitch + 0.5
+    	end
+
+    	if y < yaw and not (y < yaw - 180) then
+    		yaw = YawRight(yaw)
+    	elseif y < yaw - 180 then
+    		yaw = YawLeft(yaw)
+    	end
+
+    	if y > yaw and not (y > yaw + 180) then
+    		yaw = YawLeft(yaw)
+    	elseif y > yaw + 180 then
+    		yaw = YawRight(yaw)
+    	end
+    else
+    	local mouseX = -InputValue("mousedx")
+    	local mouseY = -InputValue("mousedy")
+
+    	if sign(mouseY) < 0 and pitch > -45 then
+    		pitch = pitch - 0.5
+    	elseif sign(mouseY) > 0 and pitch < 15 then
+    		pitch = pitch + 0.5
+    	end
+
+    	if sign(mouseX) < 0 then
+    		yaw = YawRight(yaw)
+    	elseif sign(mouseX) > 0 then
+    		yaw = YawLeft(yaw)
+    	end
+    end
+    PlayLoop(chopper.sound, chopper.transform.pos, 10)
+    local mx, my = InputValue("mousedx"), InputValue("mousedy")
+    zoom = zoom - InputValue("mousewheel")
+end
+

```

---

# Migration Report: main\kill_dozer\kill.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\kill_dozer\kill.lua
+++ patched/main\kill_dozer\kill.lua
@@ -1,36 +1,41 @@
-function init()
-	kill = nil
-	speed = 0
+#version 2
+function server.init()
+    kill = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"kill") then	
-		if kill == nil then
-			kill = FindJoint(GetTagValue(GetPlayerVehicle(),"kill"),true)
-			SetJointMotor(kill, speed)	
-		end
-	else
-		kill = nil
-	end
-	
-	local lmb1, rmb1, lmb2, rmb2 = InputDown("lmb"), InputDown("rmb"), InputReleased("lmb"), InputReleased("rmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"kill") then	
+        	if kill == nil then
+        		kill = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"kill"),true)
+        		SetJointMotor(kill, speed)	
+        	end
+        else
+        	kill = nil
+        end
+        	if lmb1 then
+        		if speed < 10 then
+        			speed = speed + 1
+        			SetJointMotor(kill, speed)	
+        		end	
+        	elseif rmb1 then
+        		if speed > -4 then
+        			speed = speed - .5
+        			SetJointMotor(kill, speed)	
+        		end	
+        	elseif lmb2 then
+        	    speed = 0
+        		SetJointMotor(kill, speed)
+        	elseif rmb2 then
+        	    speed = 0
+        		SetJointMotor(kill, speed)
+        	end
+    end
+end
 
-		if lmb1 then
-			if speed < 10 then
-				speed = speed + 1
-				SetJointMotor(kill, speed)	
-			end	
-		elseif rmb1 then
-			if speed > -4 then
-				speed = speed - .5
-				SetJointMotor(kill, speed)	
-			end	
-		elseif lmb2 then
-		    speed = 0
-			SetJointMotor(kill, speed)
-		elseif rmb2 then
-		    speed = 0
-			SetJointMotor(kill, speed)
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb1, rmb1, lmb2, rmb2 = InputDown("lmb"), InputDown("rmb"), InputReleased("lmb"), InputReleased("rmb")
+end
+

```

---

# Migration Report: main\kill_dozer\kill2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\kill_dozer\kill2.lua
+++ patched/main\kill_dozer\kill2.lua
@@ -1,36 +1,41 @@
-function init()
-	kill2 = nil
-	speed = 0
+#version 2
+function server.init()
+    kill2 = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"kill2") then	
-		if kill2 == nil then
-			kill2 = FindJoint(GetTagValue(GetPlayerVehicle(),"kill2"),true)
-			SetJointMotor(kill2, speed)	
-		end
-	else
-		kill2 = nil
-	end
-	
-	local lmb1, rmb1, lmb2, rmb2 = InputDown("lmb"), InputDown("rmb"), InputReleased("lmb"), InputReleased("rmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"kill2") then	
+        	if kill2 == nil then
+        		kill2 = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"kill2"),true)
+        		SetJointMotor(kill2, speed)	
+        	end
+        else
+        	kill2 = nil
+        end
+        	if lmb1 then
+        		if speed < 10 then
+        			speed = speed + 1
+        			SetJointMotor(kill2, speed)	
+        		end	
+        	elseif rmb1 then
+        		if speed > -4 then
+        			speed = speed - .5
+        			SetJointMotor(kill2, speed)	
+        		end	
+        	elseif lmb2 then
+        	    speed = 0
+        		SetJointMotor(kill2, speed)
+        	elseif rmb2 then
+        	    speed = 0
+        		SetJointMotor(kill2, speed)
+        	end
+    end
+end
 
-		if lmb1 then
-			if speed < 10 then
-				speed = speed + 1
-				SetJointMotor(kill2, speed)	
-			end	
-		elseif rmb1 then
-			if speed > -4 then
-				speed = speed - .5
-				SetJointMotor(kill2, speed)	
-			end	
-		elseif lmb2 then
-		    speed = 0
-			SetJointMotor(kill2, speed)
-		elseif rmb2 then
-		    speed = 0
-			SetJointMotor(kill2, speed)
-		end
-end	
-	+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb1, rmb1, lmb2, rmb2 = InputDown("lmb"), InputDown("rmb"), InputReleased("lmb"), InputReleased("rmb")
+end
+

```

---

# Migration Report: main\kill_dozer\killer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\kill_dozer\killer.lua
+++ patched/main\kill_dozer\killer.lua
@@ -1,33 +1,35 @@
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "killer") then
-		local info = {}
-        info[#info+1] = {"Blade", "Control"}
-		info[#info+1] = {"Hold LMB", "Blade Forward"}
-		info[#info+1] = {"Hold RMB", "Blade Reverse"}
-        info[#info+1] = {"Keep Holding", "Blade Vibrate"}
-		info[#info+1] = {"Release", "Blade Stop"}
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
-	end
-end+#version 2
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "killer") then
+    	local info = {}
+           info[#info+1] = {"Blade", "Control"}
+    	info[#info+1] = {"Hold LMB", "Blade Forward"}
+    	info[#info+1] = {"Hold RMB", "Blade Reverse"}
+           info[#info+1] = {"Keep Holding", "Blade Vibrate"}
+    	info[#info+1] = {"Release", "Blade Stop"}
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
+    end
+end
+

```

---

# Migration Report: main\scorpionking.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scorpionking.lua
+++ patched/main\scorpionking.lua
@@ -1,3 +1,4 @@
+#version 2
 function clamp(value, mi, ma)
 	if value < mi then value = mi end
 	if value > ma then value = ma end
@@ -8,41 +9,44 @@
 	return x > 0 and 1 or (x < 0 and -1 or 0)
 end
 
-function init()
-	ScorpionKing = FindVehicle("ponsse")
-
-	steer = FindJoints("steer")
-	armJoint = FindJoints("arm1")
-	center = FindJoint("center")
-	movement = 0
-	armAngle = 0
+function server.init()
+    ScorpionKing = FindVehicle("ponsse")
+    steer = FindJoints("steer")
+    armJoint = FindJoints("arm1")
+    center = FindJoint("center")
+    movement = 0
+    armAngle = 0
 end
 
-function tick(dt)
-	if GetPlayerVehicle() ~= ScorpionKing then
-		return
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) ~= ScorpionKing then
+        	return
+        end
+        for i = 1, #steer do
+        	local min, max = GetJointLimits(steer[i])
+        	if direction == 0 then
+        		movement = movement - sign(movement) * 2 * dt
+        	else
+        		movement = movement + direction
+        	end
+        	movement = clamp(movement, min, max)
+        	--DebugWatch("steer["..i.."]", math.floor(movement))
+        	SetJointMotorTarget(steer[i], movement)
+        end
+        for i = 1, #armJoint do
+        	local min, max = GetJointLimits(armJoint[i])
+        	armAngle = armAngle + armDir
+        	armAngle = clamp(armAngle, min, max)
+        	SetJointMotorTarget(armJoint[i], armAngle, 0.5)
+        end
+    end
+end
 
-	local direction = (InputDown("a") and 10 * dt or 0) - (InputDown("d") and 10 * dt or 0)
-	for i = 1, #steer do
-		local min, max = GetJointLimits(steer[i])
-		if direction == 0 then
-			movement = movement - sign(movement) * 2 * dt
-		else
-			movement = movement + direction
-		end
-		movement = clamp(movement, min, max)
-		--DebugWatch("steer["..i.."]", math.floor(movement))
-		SetJointMotorTarget(steer[i], movement)
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local direction = (InputDown("a") and 10 * dt or 0) - (InputDown("d") and 10 * dt or 0)
+    local armDir = (InputDown("lmb") and 0.25 or 0) - (InputDown("rmb") and 0.25 or 0)
+    SetJointMotor(center, (InputDown("r") and 0.5 or 0) - (InputDown("f") and 0.5 or 0))
+end
 
-	local armDir = (InputDown("lmb") and 0.25 or 0) - (InputDown("rmb") and 0.25 or 0)
-	for i = 1, #armJoint do
-		local min, max = GetJointLimits(armJoint[i])
-		armAngle = armAngle + armDir
-		armAngle = clamp(armAngle, min, max)
-		SetJointMotorTarget(armJoint[i], armAngle, 0.5)
-	end
-
-	SetJointMotor(center, (InputDown("r") and 0.5 or 0) - (InputDown("f") and 0.5 or 0))
-end

```

---

# Migration Report: main\shred_dozer\shred.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\shred_dozer\shred.lua
+++ patched/main\shred_dozer\shred.lua
@@ -1,30 +1,35 @@
-function init()
-	shred = nil
-	speed = 0
+#version 2
+function server.init()
+    shred = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"shred") then	
-		if shred == nil then
-			shred = FindJoint(GetTagValue(GetPlayerVehicle(),"shred"),true)
-			SetJointMotor(shred, speed)	
-		end
-	else
-		shred = nil
-	end
-	
-	local lmb, rmb = InputPressed("lmb"), InputPressed("rmb")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"shred") then	
+        	if shred == nil then
+        		shred = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"shred"),true)
+        		SetJointMotor(shred, speed)	
+        	end
+        else
+        	shred = nil
+        end
+        	if lmb then
+        		if speed < 10 then
+        			speed = speed + 2.5
+        			SetJointMotor(shred, speed)	
+        		end
+        	elseif rmb then
+        		if speed > -15 then
+        			speed = speed - 2.5
+        			SetJointMotor(shred, speed)	
+        		end
+        	end
+    end
+end
 
-		if lmb then
-			if speed < 10 then
-				speed = speed + 2.5
-				SetJointMotor(shred, speed)	
-			end
-		elseif rmb then
-			if speed > -15 then
-				speed = speed - 2.5
-				SetJointMotor(shred, speed)	
-			end
-		end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb = InputPressed("lmb"), InputPressed("rmb")
 end
-	+

```

---

# Migration Report: main\shred_dozer\shredder.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\shred_dozer\shredder.lua
+++ patched/main\shred_dozer\shredder.lua
@@ -1,32 +1,34 @@
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "shred") then
-		local info = {}
-        info[#info+1] = {"Shredder", "Rotation Control"}
-        info[#info+1] = {"LMB", "Forward 4-Speeds"}
-		info[#info+1] = {"RMB", "Reverse 6-Speeds"}
-		info[#info+1] = {"Press Again", "Change Speed"}
-		UiPush()
-			UiAlign("top left")
-			local w = 200
-			local h = #info*22 + 30
-			UiTranslate(20, UiHeight()-h-20)
-			UiColor(0,0,0,0.5)
-			UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
-			UiTranslate(125, 32)
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
-	end
-end+#version 2
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "shred") then
+    	local info = {}
+           info[#info+1] = {"Shredder", "Rotation Control"}
+           info[#info+1] = {"LMB", "Forward 4-Speeds"}
+    	info[#info+1] = {"RMB", "Reverse 6-Speeds"}
+    	info[#info+1] = {"Press Again", "Change Speed"}
+    	UiPush()
+    		UiAlign("top left")
+    		local w = 200
+    		local h = #info*22 + 30
+    		UiTranslate(20, UiHeight()-h-20)
+    		UiColor(0,0,0,0.5)
+    		UiImageBox("common/box-solid-6.png", 300, h, 6, 6)
+    		UiTranslate(125, 32)
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
+    end
+end
+

```

---

# Migration Report: main\shredder3000\rotate_arm.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\shredder3000\rotate_arm.lua
+++ patched/main\shredder3000\rotate_arm.lua
@@ -1,11 +1,10 @@
-function init()   
-	-- Change speed of rotating
-	speed = 5
-	
-    SetJointMotor(FindJoint("rotate_arm1", true) , speed)
-	SetJointMotor(FindJoint("rotate_arm2", true) , speed)
-	SetJointMotor(FindJoint("rotate_arm3", true) , speed+10)
-	SetJointMotor(FindJoint("rotate_arm4", true) , speed-3)
-	SetJointMotor(FindJoint("rotate_arm5", true) , speed-3)
+#version 2
+function server.init()
+    speed = 5
+       SetJointMotor(FindJoint("rotate_arm1", true) , speed)
+    SetJointMotor(FindJoint("rotate_arm2", true) , speed)
+    SetJointMotor(FindJoint("rotate_arm3", true) , speed+10)
+    SetJointMotor(FindJoint("rotate_arm4", true) , speed-3)
+    SetJointMotor(FindJoint("rotate_arm5", true) , speed-3)
 end
 

```

---

# Migration Report: main\tornado\lift.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\tornado\lift.lua
+++ patched/main\tornado\lift.lua
@@ -1,50 +1,48 @@
-strength = 50	--Strength of Tornado Updraft
-maxMass = 5000	--The maximum mass for a body to be lifted
-maxDist = 17	--The maximum distance for bodies to be lifted
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"nado") then
 
-function tick()
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"nado") then
+        		--Get all physical and dynamic bodies in front of camera
+        		local t = GetCameraTransform()
+        		local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/2))
+        		local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
+        		local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
+        		QueryRequire("physical dynamic")
+        		local bodies = QueryAabbBodies(mi, ma)
 
-			--Get all physical and dynamic bodies in front of camera
-			local t = GetCameraTransform()
-			local c = TransformToParentPoint(t, Vec(0, 0, -maxDist/2))
-			local mi = VecAdd(c, Vec(-maxDist/2, -maxDist/2, -maxDist/2))
-			local ma = VecAdd(c, Vec(maxDist/2, maxDist/2, maxDist/2))
-			QueryRequire("physical dynamic")
-			local bodies = QueryAabbBodies(mi, ma)
+        		--Loop through bodies and push them
+        		for i=1,#bodies do
+        			local b = bodies[i]
 
-			--Loop through bodies and push them
-			for i=1,#bodies do
-				local b = bodies[i]
+        			--Compute body center point and distance
+        			local bmi, bma = GetBodyBounds(b)
+        			local bc = VecLerp(bmi, bma, 0.5)
+        			local dir = VecSub(bc, t.pos)
+        			local dist = VecLength(dir)
+        			dir = VecScale(dir, 1.0/dist)
 
-				--Compute body center point and distance
-				local bmi, bma = GetBodyBounds(b)
-				local bc = VecLerp(bmi, bma, 0.5)
-				local dir = VecSub(bc, t.pos)
-				local dist = VecLength(dir)
-				dir = VecScale(dir, 1.0/dist)
+        			--Get body mass
+        			local mass = GetBodyMass(b)
 
-				--Get body mass
-				local mass = GetBodyMass(b)
-				
-				--Check if body is should be affected
-				if dist < maxDist and mass < maxMass then
-					--Make sure direction is always pointing slightly upwards
-					dir[2] = 1
-					dir = VecNormalize(dir)
-			
-					--Compute how much velocity to add
-					local massScale = 1 - math.min(mass/maxMass, 1.0)
-					local distScale = 1 - math.min(dist/maxDist, 1.0)
-					local add = VecScale(dir, strength * massScale * distScale)
-					
-					--Add velocity to body
-					local vel = GetBodyVelocity(b)
-					vel = VecAdd(vel, add)
-					SetBodyVelocity(b, vel)
-				end
-			end
-	end
+        			--Check if body is should be affected
+        			if dist < maxDist and mass < maxMass then
+        				--Make sure direction is always pointing slightly upwards
+        				dir[2] = 1
+        				dir = VecNormalize(dir)
+
+        				--Compute how much velocity to add
+        				local massScale = 1 - math.min(mass/maxMass, 1.0)
+        				local distScale = 1 - math.min(dist/maxDist, 1.0)
+        				local add = VecScale(dir, strength * massScale * distScale)
+
+        				--Add velocity to body
+        				local vel = GetBodyVelocity(b)
+        				vel = VecAdd(vel, add)
+        				SetBodyVelocity(b, vel)
+        			end
+        		end
+        end
+    end
 end
 
-

```

---

# Migration Report: main\tornado\nado.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\tornado\nado.lua
+++ patched/main\tornado\nado.lua
@@ -1,33 +1,38 @@
-function init()
-	nado = nil
-	speed = 0
+#version 2
+function server.init()
+    nado = nil
+    speed = 0
 end
 
-function tick(dt)	
-	if GetPlayerVehicle() > 0 and HasTag(GetPlayerVehicle(),"nado") then	
-		if nado == nil then
-			nado = FindJoint(GetTagValue(GetPlayerVehicle(),"nado"),true)
-			SetJointMotor(nado, speed)
-			PlayMusic("LEVEL/tornado/tornado.ogg")		
-		end
-	else
-		nado = nil
-	end
-	
-	local lmb, rmb, m = InputPressed("lmb"), InputPressed("rmb"), InputPressed("m")
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) > 0 and HasTag(GetPlayerVehicle(playerId),"nado") then	
+        	if nado == nil then
+        		nado = FindJoint(GetTagValue(GetPlayerVehicle(playerId),"nado"),true)
+        		SetJointMotor(nado, speed)
+        		PlayMusic("LEVEL/tornado/tornado.ogg")		
+        	end
+        else
+        	nado = nil
+        end
+        	if lmb then
+        		if speed < 12 then
+        			speed = speed + .5
+        			SetJointMotor(nado, speed)	
+        		end
+        	elseif rmb then
+        		if speed > -12 then
+        			speed = speed - .5
+        			SetJointMotor(nado, speed)	
+        		end
+        	elseif m then
+        		StopMusic()
+        	end
+    end
+end
 
-		if lmb then
-			if speed < 12 then
-				speed = speed + .5
-				SetJointMotor(nado, speed)	
-			end
-		elseif rmb then
-			if speed > -12 then
-				speed = speed - .5
-				SetJointMotor(nado, speed)	
-			end
-		elseif m then
-			StopMusic()
-		end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    local lmb, rmb, m = InputPressed("lmb"), InputPressed("rmb"), InputPressed("m")
 end
-	+

```

---

# Migration Report: main\tornado\tornado.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\tornado\tornado.lua
+++ patched/main\tornado\tornado.lua
@@ -1,33 +1,35 @@
-function draw()
-	local vehicle = GetPlayerVehicle()
-	if HasTag(vehicle, "nado") then
-		local info = {}
-        info[#info+1] = {"Tornado", "Spin Control"}
-        info[#info+1] = {"LMB", "Rotate Left"}
-		info[#info+1] = {"RMB", "Rotate Right"}
-		info[#info+1] = {"Press Again", "Change Speed"}
-		info[#info+1] = {"M", "Stop Music"}
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
-	end
-end+#version 2
+function client.draw()
+    local vehicle = GetPlayerVehicle(playerId)
+    if HasTag(vehicle, "nado") then
+    	local info = {}
+           info[#info+1] = {"Tornado", "Spin Control"}
+           info[#info+1] = {"LMB", "Rotate Left"}
+    	info[#info+1] = {"RMB", "Rotate Right"}
+    	info[#info+1] = {"Press Again", "Change Speed"}
+    	info[#info+1] = {"M", "Stop Music"}
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
+    end
+end
+

```
