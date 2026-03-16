# Migration Report: script\car_mechanics\car_lift.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\car_mechanics\car_lift.lua
+++ patched/script\car_mechanics\car_lift.lua
@@ -1,20 +1,4 @@
-function init()
-    PLATFORM_VELOCITY = 0.6
-
-    platform_body = FindBody("platform")
-    platform_joints = FindJoints("platform")
-    btn_up = FindShape("up")
-    btn_down = FindShape("down")
-
-    min, max = GetJointLimits(platform_joints[1])
-    state = 0
-    stateTime = 0.0
-
-    clickUp = LoadSound("clickup.ogg")
-	clickDown = LoadSound("clickdown.ogg")
-	motorSound = LoadLoop("vehicle/hydraulic-loop.ogg")
-end
-
+#version 2
 function setState(s)
     state = s
     stateTime = 0.0
@@ -24,35 +8,54 @@
     return stateTime > 10.0
 end
 
-function tick(dt)
+function server.init()
+       PLATFORM_VELOCITY = 0.6
+       platform_body = FindBody("platform")
+       platform_joints = FindJoints("platform")
+       btn_up = FindShape("up")
+       btn_down = FindShape("down")
+       min, max = GetJointLimits(platform_joints[1])
+       state = 0
+       stateTime = 0.0
+    motorSound = LoadLoop("vehicle/hydraulic-loop.ogg")
+end
 
-    stateTime = stateTime + dt
-
-    if state == 1 then
-        local m = GetJointMovement(platform_joints[1])
-        if m >= (max - 0.01) or timedOut() then
-            setState(0)
-        end
-    elseif state == 2 then
-        local m = GetJointMovement(platform_joints[1])
-        if m <= 0.01 or timedOut() then
-            setState(0)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        stateTime = stateTime + dt
+        if state == 1 then
+            local m = GetJointMovement(platform_joints[1])
+            if m >= (max - 0.01) or timedOut() then
+                setState(0)
+            end
+        elseif state == 2 then
+            local m = GetJointMovement(platform_joints[1])
+            if m <= 0.01 or timedOut() then
+                setState(0)
+            end
         end
     end
+end
 
+function client.init()
+       clickUp = LoadSound("clickup.ogg")
+    clickDown = LoadSound("clickdown.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if state ~= 0 then
         SetBodyActive(platform_body, true)
         PlayLoop(motorSound, GetBodyTransform(platform_body).pos)
     end
-
-    if GetPlayerInteractShape() == btn_up and InputPressed("interact") then
+    if GetPlayerInteractShape(playerId) == btn_up and InputPressed("interact") then
         setState(1)
         PlaySound(clickUp)
         for i=1, #platform_joints do
             local joint = platform_joints[i]
             SetJointMotorTarget(joint, max, PLATFORM_VELOCITY)
         end
-    elseif GetPlayerInteractShape() == btn_down and InputPressed("interact") then
+    elseif GetPlayerInteractShape(playerId) == btn_down and InputPressed("interact") then
         setState(2)
         PlaySound(clickDown)
         for i=1, #platform_joints do
@@ -61,3 +64,4 @@
         end
     end
 end
+

```

---

# Migration Report: script\car_mechanics\door_auto.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\car_mechanics\door_auto.lua
+++ patched/script\car_mechanics\door_auto.lua
@@ -1,26 +1,4 @@
-function init()
-    DOORS_1_VELOCITY = 1.0
-    DOORS_2_VELOCITY = 2.0
-
-    doors1 = FindJoints("door1")
-    doors2 = FindJoints("door2")
-
-    local shapes = FindShapes("dcoll")
-    for i=1, #shapes do
-        local shape = shapes[i]
-        SetShapeCollisionFilter(shape, 2, 255-2)
-    end
-
-    btn_open = FindShape("open")
-    btn_close = FindShape("close")
-
-    state = 0
-    stateTime = 0.0
-
-    clickUp = LoadSound("clickup.ogg")
-	clickDown = LoadSound("clickdown.ogg")
-end
-
+#version 2
 function setState(s)
     state = s
     stateTime = 0.0
@@ -30,90 +8,113 @@
     return stateTime > 10.0
 end
 
-function tick(dt)
+function server.init()
+    DOORS_1_VELOCITY = 1.0
+    DOORS_2_VELOCITY = 2.0
+    doors1 = FindJoints("door1")
+    doors2 = FindJoints("door2")
+    local shapes = FindShapes("dcoll")
+    for i=1, #shapes do
+        local shape = shapes[i]
+        SetShapeCollisionFilter(shape, 2, 255-2)
+    end
+    btn_open = FindShape("open")
+    btn_close = FindShape("close")
+    state = 0
+    stateTime = 0.0
+end
 
-    stateTime = stateTime + dt
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        stateTime = stateTime + dt
+        if state == 1 then
 
-    if state == 1 then
+            local atTarget = true
 
-        local atTarget = true
+            for i=1, #doors1 do
+                local joint = doors1[i]
+                local min, _ = GetJointLimits(joint)
+                local m = GetJointMovement(joint)
 
-        for i=1, #doors1 do
-            local joint = doors1[i]
-            local min, _ = GetJointLimits(joint)
-            local m = GetJointMovement(joint)
+                if m > min + 1 and not timedOut() then
+                    atTarget = false
+                end
 
-            if m > min + 1 and not timedOut() then
-                atTarget = false
+            end
+            for i=1, #doors2 do
+                local joint = doors2[i]
+                local min, _ = GetJointLimits(joint)
+                local m = GetJointMovement(joint)
+
+                if m > min + 1 and not timedOut() then
+                    atTarget = false
+                end
             end
 
-        end
-        for i=1, #doors2 do
-            local joint = doors2[i]
-            local min, _ = GetJointLimits(joint)
-            local m = GetJointMovement(joint)
+            if atTarget then
+                setState(0)
+            end
 
-            if m > min + 1 and not timedOut() then
-                atTarget = false
+        elseif state == 2 then
+            local atTarget = true
+
+            for i=1, #doors1 do
+                local joint = doors1[i]
+                local _, max = GetJointLimits(joint)
+                local m = GetJointMovement(joint)
+
+                if m < max - 4 and not timedOut() then
+                    atTarget = false
+                end
+
+            end
+            for i=1, #doors2 do
+                local joint = doors2[i]
+                local _, max = GetJointLimits(joint)
+                local m = GetJointMovement(joint)
+
+                if m < max - 4 and not timedOut() then
+                    atTarget = false
+                end
+            end
+
+            if atTarget then
+                setState(0)
             end
         end
-
-        if atTarget then
-            setState(0)
-        end
-
-    elseif state == 2 then
-        local atTarget = true
-
-        for i=1, #doors1 do
-            local joint = doors1[i]
-            local _, max = GetJointLimits(joint)
-            local m = GetJointMovement(joint)
-
-            if m < max - 4 and not timedOut() then
-                atTarget = false
-            end
-
-        end
-        for i=1, #doors2 do
-            local joint = doors2[i]
-            local _, max = GetJointLimits(joint)
-            local m = GetJointMovement(joint)
-
-            if m < max - 4 and not timedOut() then
-                atTarget = false
-            end
-        end
-
-        if atTarget then
-            setState(0)
-        end
-    end
-
-    if state ~= 0 then
-        for i=1, #doors1 do
-            local joint = doors1[i]
-            local shapes = GetJointShapes(joint)
-            for j = 1, #shapes do
-                local body = GetShapeBody(shapes[j])
-                if IsBodyDynamic(body) then
-                    SetBodyActive(body, true)
+        if state ~= 0 then
+            for i=1, #doors1 do
+                local joint = doors1[i]
+                local shapes = GetJointShapes(joint)
+                for j = 1, #shapes do
+                    local body = GetShapeBody(shapes[j])
+                    if IsBodyDynamic(body) then
+                        SetBodyActive(body, true)
+                    end
                 end
             end
-        end
-        for i=1, #doors2 do
-            local joint = doors2[i]
-            local shapes = GetJointShapes(joint)
-            for j = 1, #shapes do
-                local body = GetShapeBody(shapes[j])
-                if IsBodyDynamic(body) then
-                    SetBodyActive(body, true)
+            for i=1, #doors2 do
+                local joint = doors2[i]
+                local shapes = GetJointShapes(joint)
+                for j = 1, #shapes do
+                    local body = GetShapeBody(shapes[j])
+                    if IsBodyDynamic(body) then
+                        SetBodyActive(body, true)
+                    end
                 end
             end
         end
     end
+end
 
-    if GetPlayerInteractShape() == btn_close and InputPressed("interact") then
+function client.init()
+       clickUp = LoadSound("clickup.ogg")
+    clickDown = LoadSound("clickdown.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == btn_close and InputPressed("interact") then
         setState(1)
         PlaySound(clickDown)
         for i=1, #doors1 do
@@ -126,7 +127,7 @@
             local min, _ = GetJointLimits(joint)
             SetJointMotorTarget(joint, min, DOORS_2_VELOCITY)
         end
-    elseif GetPlayerInteractShape() == btn_open and InputPressed("interact") then
+    elseif GetPlayerInteractShape(playerId) == btn_open and InputPressed("interact") then
         setState(2)
         PlaySound(clickUp)
         for i=1, #doors1 do
@@ -140,6 +141,5 @@
             SetJointMotorTarget(joint, max, DOORS_2_VELOCITY)
         end
     end
+end
 
-    
-end

```

---

# Migration Report: script\Radio_Samara.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\Radio_Samara.lua
+++ patched/script\Radio_Samara.lua
@@ -1,45 +1,45 @@
-on = false
-function init()	
-	--Find handle to radio
-	radio = FindShape("radio")
-	
-	--Make sure the light is turned off and make interactable
-	SetShapeEmissiveScale(radio, 0)
-	SetTag(radio, "interact", "loc@RADIO_ON")
-	
-	--Load click sound and music from game assets
-	clickSound = LoadSound("MOD/Sounds/Radio_Interact.ogg")
-	musicLoop = LoadLoop("MOD/Sounds/Radio.ogg")
-	
+#version 2
+function server.init()
+    radio = FindShape("radio")
+    --Make sure the light is turned off and make interactable
+    SetShapeEmissiveScale(radio, 0)
+    SetTag(radio, "interact", "loc@RADIO_ON")
+    --Load click sound and music from game assets
+    musicLoop = LoadLoop("MOD/Sounds/Radio.ogg")
 end
 
-
-function tick(dt)
-	--If radio is broken it should not be interactable and not function
-	if IsShapeBroken(radio) then
-		RemoveTag(radio, "interact")
-		return
-	end
-
-	--Turn on/off radio
-	if GetPlayerInteractShape() == radio and InputPressed("interact") then
-		PlaySound(clickSound)
-		if on then
-			on = false
-			SetShapeEmissiveScale(radio, 0)
-			SetTag(radio, "interact", "loc@RADIO_ON")			
-		else
-			on = true
-			SetShapeEmissiveScale(radio, 1)
-			SetTag(radio, "interact", "loc@RADIO_OFF")			
-		end
-	end
-
-	--If radio is on, play music at the world position
-	if on then 
-		local pos = GetShapeWorldTransform(radio).pos
-		PlayLoop(musicLoop, pos)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(radio) then
+        	RemoveTag(radio, "interact")
+        	return
+        end
+        --Turn on/off radio
+        --If radio is on, play music at the world position
+    end
 end
 
+function client.init()
+    clickSound = LoadSound("MOD/Sounds/Radio_Interact.ogg")
+end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == radio and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if on then
+    		on = false
+    		SetShapeEmissiveScale(radio, 0)
+    		SetTag(radio, "interact", "loc@RADIO_ON")			
+    	else
+    		on = true
+    		SetShapeEmissiveScale(radio, 1)
+    		SetTag(radio, "interact", "loc@RADIO_OFF")			
+    	end
+    end
+    if on then 
+    	local pos = GetShapeWorldTransform(radio).pos
+    	PlayLoop(musicLoop, pos)
+    end
+end
+

```

---

# Migration Report: script\trexroar.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\trexroar.lua
+++ patched/script\trexroar.lua
@@ -1,33 +1,27 @@
-
-function init()
-	sniffer = FindJoint("sniffer")
-	radar = FindJoint("radar")
-	SetJointMotor(radar, 0.01)
-	body = FindBody("target")
-
-	board = FindShape("board")
-	
-	spring = FindJoint("spring")
-	
-	body = FindBody("springboard")
-
+#version 2
+function server.init()
+    sniffer = FindJoint("sniffer")
+    radar = FindJoint("radar")
+    SetJointMotor(radar, 0.01)
+    body = FindBody("target")
+    board = FindShape("board")
+    spring = FindJoint("spring")
+    body = FindBody("springboard")
 end
 
-Timer = 0
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        Timer = Timer + 1
+        if Timer <= 90 then
+        --SetFloat("springboard.timer", 2, true)
+        SetJointMotorTarget(sniffer, -60, 1)
+        elseif Timer == 130 then
+        --SetFloat("springboard.timer", GetFloat("springboard.timer") - dt, true)
+        SetJointMotorTarget(sniffer, 60, 0.3)
+        --Delete(sniffer)
+        elseif Timer == 130 then
+        Timer = 0
+        end
+    end
+end
 
-function tick(dt)
-
-	--local timer = GetFloat("springboard.timer")
-
-	Timer = Timer + 1
-	if Timer <= 90 then
-	--SetFloat("springboard.timer", 2)
-	SetJointMotorTarget(sniffer, -60, 1)
-	elseif Timer == 130 then
-	--SetFloat("springboard.timer", GetFloat("springboard.timer") - dt)
-	SetJointMotorTarget(sniffer, 60, 0.3)
-	--Delete(sniffer)
-	elseif Timer == 130 then
-	Timer = 0
-	end
-end
```

---

# Migration Report: script\trextest.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\trextest.lua
+++ patched/script\trextest.lua
@@ -1,92 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-function init()
-
-	frame = FindShape("frame")
-	
-	motor = FindJoint("motor")
-	
-	timer = 1
-end
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -118,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 3.5)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 300
-config.viewFov = 250
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5
-config.maxSoundDist = 100.0
-config.aggressive = true
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 2099999999999999999999999999999
-
-PATH_NODE_TOLERANCE = 0.99
 
 function configInit()
 	local eye = FindLight("eye")
@@ -189,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -206,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 100.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -256,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -301,23 +140,20 @@
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
 
-
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -336,7 +172,7 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	local vel = GetBodyVelocity(robot.body)
@@ -348,7 +184,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 0.02
 	end
 
@@ -378,7 +214,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -393,35 +229,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 0.0
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -455,7 +279,7 @@
 end
 
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10 --climb
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -463,10 +287,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 7		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -485,7 +305,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -502,7 +321,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -515,7 +333,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -531,8 +348,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -595,7 +410,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -604,7 +419,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -615,15 +430,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -640,11 +446,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -653,12 +459,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -691,7 +491,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -719,9 +518,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -766,7 +564,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -811,13 +609,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -877,13 +668,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -910,7 +699,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -924,7 +712,7 @@
 end
 
 function weaponEmitFire(weapon, t, amount)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -947,7 +735,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 2)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -960,17 +748,17 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 3.5, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.2 or distToPlayer < 0.1 then
 				rejectAllBodies(robot.allBodies)
 				--SetJointMotor(saber, 10)			
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.2 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength)
 					--SetJointMotor(saber, -15)
 					RemoveTag(robot.allJoints, "sniffer")
 					SetBodyVelocity(body11, Vec(0, -3 * weapon.strength, 0))
@@ -983,7 +771,6 @@
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -1007,7 +794,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1072,15 +859,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1090,7 +869,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1115,22 +893,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1169,32 +935,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer =false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 1	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1218,7 +964,7 @@
 			local limit = math.cos(config.viewFov * 10 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1265,8 +1011,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1295,26 +1041,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(0, -100, 0)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1350,35 +1087,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 0.1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "high"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 10, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1470,7 +1188,7 @@
 		end
 
 		local targetRadius = 0.1
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 0.1
 		end
 	
@@ -1501,9 +1219,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1513,7 +1230,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1576,12 +1293,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1630,7 +1341,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1639,8 +1350,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1656,7 +1365,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1671,7 +1379,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1679,7 +1386,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1690,7 +1396,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1707,72 +1412,6 @@
 	DebugWatch("navigation.unblockTimer", navigation.unblockTimer)
 	DebugWatch("navigation.thinkTime", navigation.thinkTime)
 	DebugWatch("GetPathState()", GetPathState())
-end
-
-
-function init()
-
-	sniffer = FindJoint("sniffer")
-	radar = FindJoint("radar")
-	SetJointMotor(radar, 0.01)
-	body = FindBody("target")
-
-	board = FindShape("board")
-	
-	spring = FindJoint("spring")
-	
-	body = FindBody("springboard")
-	
-	core = FindShape("core") --the weakspot, breakable after shields down
-	corebody = GetShapeBody(core)	
-
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("MOD/main/snd/blaster2.ogg", 20.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("--robot/head-loop.ogg", 7.0)
-	turnLoop = LoadLoop("--robot/turn-loop.ogg", 7.0)
-	walkLoop = LoadLoop("MOD/main/snd/atst.ogg", 14.0)
-	rollLoop = LoadLoop("--robot/roll-loop.ogg", 7.0)
-	chargeLoop = LoadLoop("--robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("--robot/alert.ogg", 9.0)
-	huntSound = LoadSound("MOD/snd/roar.ogg", 25.0)
-	idleSound = LoadSound("--robot/idle.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("--robot/disable0.ogg")
-	biteSound = LoadSound("MOD/snd/bite.ogg", 9.0)
-	biteSound2 = LoadSound("MOD/snd/bite2.ogg", 9.0)
-	atom = LoadLoop("MOD/snd/atom.ogg", 15.0)
-	dbm = LoadLoop("MOD/snd/DeathBeam.ogg", 20.0)
-	dbm2 = LoadLoop("MOD/snd/jet.ogg", 15.0)
-	step = LoadSound("MOD/snd/step.ogg", 3.0)
-	stepbass = LoadSound("MOD/snd/stepbass.ogg", 150.0)
-	death = LoadSound("MOD/snd/gdeath2.ogg", 100.0)
-	sb = FindShape("target11")
-	smokeSpeed = 180
-	lasersize = 0.7
-	lasersize2 = 0.7
-	debvel = 5
-	debvel2 = 20
-	trimer = 0
-	heldtimer = 0
-	
 end
 
 function Laser()
@@ -1897,511 +1536,15 @@
     if hit then
         forwardPos = TransformToParentPoint(ct, Vec(0, 0, -hitDistance))
         distance = hitDistance
-        --SetPlayerHealth(GetPlayerHealth() - 0.02)		
+        --SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02)		
 		
     end
     return forwardPos, hit, distance
 end
 
---function hurt()
-	--QueryRejectVehicle(GetPlayerVehicle())
-	--hit, dist = QueryRaycast(sbtrans, GetPlayerCameraTransform().pos, 100, 0.2)
-	--if hit then
-		--SetPlayerHealth(GetPlayerHealth() - 0.02)
-	--end
---end
-
 function getDist(v1, v2)
 	return VecLength(VecSub(v1,v2))
 end
-
-function update(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	sbtrans = GetShapeWorldTransform(sb)
-    	direction = TransformToParentVec(sbtrans, Vec(0, 0, -1))
-    	if InputDown("K") then
-    	Laser()
-    	PointLight(sbtrans.pos, 0.2,0.5,0.9, 60 )
-    	PointLight(GetAimPos(), 0.2,0.5,0.9, 40 )
-    	MakeHole(GetAimPos(), 2, 2, 2)
-		SpawnFire(GetAimPos())
-    	pummel()
-    	PlayLoop(dbm, sbtrans.pos, 12)
-		PlayLoop(dbm2, sbtrans.pos, 2)
-		SetJointMotorTarget(sniffer, -60, 3)
-		--ShakeCamera(0.5)
-		--SetPlayerHealth(GetPlayerHealth() - 0.02)
-		end
-		trimer = trimer + dt
-		if(GetPlayerHealth() > 0.0 and getDist(GetAimPos(),GetPlayerPos()) < 4) then
-            SetPlayerHealth(GetPlayerHealth() - 0.004)
-			ShakeCamera(0.5)
-        end			
-		if trimer > 10 then
-			lol = true
-		end
-
-		if lol == true then
-			heldtimer = heldtimer + dt
-			Laser()
-    		PointLight(sbtrans.pos, 0.2,0.5,0.9, 60 )
-    		PointLight(GetAimPos(), 0.2,0.5,0.9, 40 )
-    		MakeHole(GetAimPos(), 2, 2, 2)
-			SpawnFire(GetAimPos())
-    		pummel()
-    	    PlayLoop(dbm, sbtrans.pos, 12)
-			--PlayLoop(atom, sbtrans.pos, 10)
-		    PlayLoop(dbm2, sbtrans.pos, 2)
-			SetJointMotorTarget(sniffer, -60, 3)
-			--ShakeCamera(0.5)
-			--SetPlayerHealth(GetPlayerHealth() - 0.02)
-			if(GetPlayerHealth() > 0.0 and getDist(GetAimPos(),GetPlayerPos()) < 4) then
-                SetPlayerHealth(GetPlayerHealth() - 0.004)
-				ShakeCamera(0.5)
-            end	
-    		if heldtimer > 5 then
-			    SetJointMotorTarget(sniffer, 60, 0.5)
-    			lol = false
-    			heldtimer = 0
-    			trimer = 0
-    		end
-		end
-		
-    tipPos = TransformToParentPoint(GetBodyTransform(corebody), Vec(0, -0.3, -1.2))
-    --tipPos2 = TransformToParentPoint(GetBodyTransform(corebody), Vec(-0, -0.2, -1.2))
-
-	ParticleReset()
-	ParticleType("smoke")
-	ParticleTile(5)
-	ParticleColor(0.95, 0.9, 1)
-	ParticleRadius(0.7, 0)
-	ParticleStretch(2, 20)
-	ParticleAlpha(0.7, 0.0)
-	ParticleDrag(0)
-	ParticleCollide(0)
-	ParticleGravity(-400)
-	ParticleSticky(0.0, 0.0)
-
-    for i=1,1 do 
-        MakeHole(tipPos, 2, 2, 2)	
-		--SpawnParticle(tipPos, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
-		--SpawnParticle(tipPos2, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
-	end		
-		
-
-	trexparts = FindShapes("")
-	for i=1,#trexparts do
-		SetShapeCollisionFilter(trexparts[i], 2, 255-2)
-	end
-
-	local timer = GetFloat("springboard.timer")
-
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			--RemoveTag(robot.allShapes[i], "unbreakable")
-		end
-		SetTag(robot.body, "disabled")
-		Delete(sb)
-		Delete(sniffer)
-		robot.enabled = false
-		PlaySound(death, robot.playerPos, 200.0, false)
-	end	
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			--SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		--SetTag(robot.body, "disabled")
-		--robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 0.2)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 9.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			PlaySound(alertSound, robot.bodyCenter, 1.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.playerPos, 50.0, false)
-			SetBodyVelocity(body11, Vec(0, -60, 0))
-			--SetBodyVelocity(body33, Vec(0, 5 * 1, 0))
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3000.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
 
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
@@ -2411,64 +1554,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end	
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2496,14 +1581,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2528,68 +1612,15 @@
 	end
 end
 
-
-function tick()
-
-	if not robot.enabled then
-		return
-	end
-
-    if IsShapeBroken(target1) then 
-		robot.enabled = false
-	    feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end
-    if IsShapeBroken(target2) then 
-		robot.enabled = false
-		feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end
-    if IsShapeBroken(target3) then 
-		robot.enabled = false
-		feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end
-    if IsShapeBroken(target4) then 
-		robot.enabled = false
-	    feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end
-    if IsShapeBroken(target5) then 
-		robot.enabled = false
-		feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end
-    if IsShapeBroken(target6) then 
-		robot.enabled = false
-		feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end
-    if IsShapeBroken(target7) then 
-		robot.enabled = false
-		feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end
-    if IsShapeBroken(target8) then 
-		robot.enabled = false
-		feetCollideLegs(true)
-		PlaySound(death, robot.bodyCenter, 15.0, false)
-    end		
-end
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2607,8 +1638,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2633,4 +1662,522 @@
 			hitByShot(strength, Vec(x,y,z), Vec(dx,dy,dz))
 		end
 	end
-end+end
+
+function server.init()
+    frame = FindShape("frame")
+    motor = FindJoint("motor")
+    timer = 1
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end	
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        sbtrans = GetShapeWorldTransform(sb)
+           	direction = TransformToParentVec(sbtrans, Vec(0, 0, -1))
+        	trimer = trimer + dt
+        	if(GetPlayerHealth(playerId) > 0.0 and getDist(GetAimPos(),GetPlayerPos(playerId)) < 4) then
+                   SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.004)
+        		ShakeCamera(0.5)
+               end			
+        	if trimer > 10 then
+        		lol = true
+        	end
+           tipPos = TransformToParentPoint(GetBodyTransform(corebody), Vec(0, -0.3, -1.2))
+           --tipPos2 = TransformToParentPoint(GetBodyTransform(corebody), Vec(-0, -0.2, -1.2))
+           for i=1,1 do 
+               MakeHole(tipPos, 2, 2, 2)	
+        	--SpawnParticle(tipPos, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
+        	--SpawnParticle(tipPos2, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
+        end		
+        trexparts = FindShapes("")
+        for i=1,#trexparts do
+        	SetShapeCollisionFilter(trexparts[i], 2, 255-2)
+        end
+        local timer = GetFloat("springboard.timer")
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		--SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	--SetTag(robot.body, "disabled")
+        	--robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 0.2)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 9.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+       	if InputDown("K") then
+       	Laser()
+       	PointLight(sbtrans.pos, 0.2,0.5,0.9, 60 )
+       	PointLight(GetAimPos(), 0.2,0.5,0.9, 40 )
+       	MakeHole(GetAimPos(), 2, 2, 2)
+    	SpawnFire(GetAimPos())
+       	pummel()
+       	PlayLoop(dbm, sbtrans.pos, 12)
+    	PlayLoop(dbm2, sbtrans.pos, 2)
+    	SetJointMotorTarget(sniffer, -60, 3)
+    	--ShakeCamera(0.5)
+    	--SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02)
+    	end
+    	if lol == true then
+    		heldtimer = heldtimer + dt
+    		Laser()
+       		PointLight(sbtrans.pos, 0.2,0.5,0.9, 60 )
+       		PointLight(GetAimPos(), 0.2,0.5,0.9, 40 )
+       		MakeHole(GetAimPos(), 2, 2, 2)
+    		SpawnFire(GetAimPos())
+       		pummel()
+       	    PlayLoop(dbm, sbtrans.pos, 12)
+    		--PlayLoop(atom, sbtrans.pos, 10)
+    	    PlayLoop(dbm2, sbtrans.pos, 2)
+    		SetJointMotorTarget(sniffer, -60, 3)
+    		--ShakeCamera(0.5)
+    		--SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02)
+    		if(GetPlayerHealth(playerId) > 0.0 and getDist(GetAimPos(),GetPlayerPos(playerId)) < 4) then
+                   SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.004)
+    			ShakeCamera(0.5)
+               end	
+       		if heldtimer > 5 then
+    		    SetJointMotorTarget(sniffer, 60, 0.5)
+       			lol = false
+       			heldtimer = 0
+       			trimer = 0
+       		end
+    	end
+    ParticleReset()
+    ParticleType("smoke")
+    ParticleTile(5)
+    ParticleColor(0.95, 0.9, 1)
+    ParticleRadius(0.7, 0)
+    ParticleStretch(2, 20)
+    ParticleAlpha(0.7, 0.0)
+    ParticleDrag(0)
+    ParticleCollide(0)
+    ParticleGravity(-400)
+    ParticleSticky(0.0, 0.0)
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		--RemoveTag(robot.allShapes[i], "unbreakable")
+    	end
+    	SetTag(robot.body, "disabled")
+    	Delete(sb)
+    	Delete(sniffer)
+    	robot.enabled = false
+    	PlaySound(death, robot.playerPos, 200.0, false)
+    end	
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "huntlost" then
+    	if not state.timer then
+    		state.timer = 6
+    		state.turnTimer = 1
+    	end
+    	state.timer = state.timer - dt
+    	head.dir = VecCopy(robot.dir)
+    	if state.timer < 0 then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	else
+    		state.turnTimer = state.turnTimer - dt
+    		if state.turnTimer < 0 then
+    			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+    			state.turnTimer = rnd(0.5, 1.5)
+    		end
+    	end
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		PlaySound(alertSound, robot.bodyCenter, 1.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.playerPos, 50.0, false)
+    		SetBodyVelocity(body11, Vec(0, -60, 0))
+    		--SetBodyVelocity(body33, Vec(0, 5 * 1, 0))
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3000.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: Scripts\EVF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\EVF.lua
+++ patched/Scripts\EVF.lua
@@ -1,9 +1,4 @@
---script version 1.1
-doorvolume = 0.4                                                                --if you reading this, get ready for yanderecode
-beep = GetBoolParam("doornotification")
-trunklift = GetBoolParam("trunklift")
-hoodlift = GetBoolParam("hoodlift")
-sounddir = GetStringParam("sounddir")
+#version 2
 function indexshapes()
     local doors = FindShapes("door")
     d1 = doors[1]
@@ -91,45 +86,12 @@
     end
 end
 
-function init()
-    if sounddir == "" then
-        sounddir = "MOD/EVF/snd"
-    end
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
@@ -165,9 +127,9 @@
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
@@ -228,8 +190,81 @@
     end
 end
 
-function update()
-    if GetPlayerVehicle() == veh then
+function server.init()
+    if sounddir == "" then
+        sounddir = "MOD/EVF/snd"
+    end
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
+    for i = 1, 8 do
+        GenerateSoundTable(i)
+    end
+    --[[indexjoints(ml)
+    indexjoints(mr)]]--
+    indexjoints(steer)
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        else
+            SetJointMotorTarget(steer_j, 0, 4.5)
+            --[[if fold then
+                SetJointMotorTarget(ml_j, -90, 1.5)
+                SetJointMotorTarget(mr_j, 90, 1.5)
+            end]]--
+        end
+        if d1_valid then
+            doorlatchsystem(d1,d1_j,1)
+        end
+        if d2_valid then
+            doorlatchsystem(d2,d2_j,2)
+        end
+        if d3_valid then
+            doorlatchsystem(d3,d3_j,3)
+        end
+        if d4_valid then
+            doorlatchsystem(d4,d4_j,4)
+        end
+        if d5_valid then
+            doorlatchsystem(d5,d5_j,5)
+        end
+        if d6_valid then
+            doorlatchsystem(d6,d6_j,6)
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
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerVehicle(playerId) == veh then
         if InputDown("left") or InputDown("right") then
             if InputDown("left") then
                 SetJointMotorTarget(steer_j, 130  , 4.5)
@@ -249,35 +284,5 @@
                 PlayLoop(doorbeep, pos, doorvolume)
             end
         end
-    else
-        SetJointMotorTarget(steer_j, 0, 4.5)
-        --[[if fold then
-            SetJointMotorTarget(ml_j, -90, 1.5)
-            SetJointMotorTarget(mr_j, 90, 1.5)
-        end]]--
-    end
-    if d1_valid then
-        doorlatchsystem(d1,d1_j,1)
-    end
-    if d2_valid then
-        doorlatchsystem(d2,d2_j,2)
-    end
-    if d3_valid then
-        doorlatchsystem(d3,d3_j,3)
-    end
-    if d4_valid then
-        doorlatchsystem(d4,d4_j,4)
-    end
-    if d5_valid then
-        doorlatchsystem(d5,d5_j,5)
-    end
-    if d6_valid then
-        doorlatchsystem(d6,d6_j,6)
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

# Migration Report: Scripts\flying_car.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\flying_car.lua
+++ patched/Scripts\flying_car.lua
@@ -1,13 +1,82 @@
---This script will run on all levels when mod is active.
---Modding documentation: http://teardowngame.com/modding
---API reference: http://teardowngame.com/modding/api.html
-
-function init()
+#version 2
+function RejectBodies()
+    QueryRejectBody(body) 
+    for i=1, thrusterCount do
+        QueryRejectBody(thrusters[i])
+    end
+end
+
+function RandomVector(size)
+    return VecScale(VecNormalize(Vec(Random(true), Random(true), Random(true))), size)
+end
+
+function Random(negative)
+    if negative then return math.random(-1000, 1000) / 1000 end
+    return math.random(0, 1000) / 1000
+end
+
+function Lerp(a, b, x)
+    return (a * (1 - x)) + (b * x)
+end
+
+function Particle(particleType, size)
+    if particleType == "colour" then
+        ParticleReset()
+        ParticleColor(vehicleColour[1], vehicleColour[2], vehicleColour[3])
+        ParticleEmissive(16)
+        ParticleRadius(size, size / 2)
+        ParticleCollide(0)
+    end
+    if particleType == "thrust" then
+        ParticleReset()
+        ParticleColor(0, 1, 1)
+        ParticleEmissive(16)
+        ParticleRadius(size, size / 2)
+        ParticleCollide(0)
+    end
+    if particleType == "spark" then
+        ParticleReset()
+        ParticleTile(6)
+        ParticleColor(1, 0.8, 0.6)
+        ParticleEmissive(2)
+        ParticleRadius(size, size / 2)
+        ParticleCollide(0)
+    end
+    if particleType == "dust" then
+        ParticleReset()
+        ParticleTile(6)
+        ParticleColor(0, 0, 0)
+        ParticleEmissive(0)
+        ParticleRadius(size, 0)
+        ParticleGravity(-9.81)
+        ParticleCollide(1)
+    end
+    if particleType == "smoke" then
+        ParticleReset()
+        ParticleType("smoke")
+        ParticleColor(1, 1, 1)
+        ParticleEmissive(0)
+        ParticleRadius(size, 0)
+        ParticleGravity(0.4)
+        ParticleDrag(0.8)
+        ParticleCollide(0)
+    end
+        if particleType == "water" then
+        ParticleReset()
+        ParticleTile(1)
+        ParticleColor(0.7, 0.8, 1)
+        ParticleEmissive(0)
+        ParticleRadius(size, 0)
+        ParticleGravity(-2)
+        ParticleDrag(0.2)
+        ParticleCollide(0)
+    end
+end
+
+function server.init()
     pi = math.pi
-
     vehicle = FindVehicle("flyingcar")
     vehicleType = GetTagValue(vehicle, "type")
-
     vehicleColour = {1, 1, 1} --Thruster smoke colour
     hoverDist = 0 --How far the vehicle hovers from the ground
     maxPower = 0 --The maximum force the thrusters can use to keep vehicle at the hover height
@@ -21,7 +90,6 @@
     angularDamping = 0 --Vehicle's angular drag
     sideDamping = 0 --The higher this value is the less the vehicle will move sideways
     thrusterCount = 0 --How many thrusters the vehicle has
-
     if vehicleType == "basic" then
         vehicleColour = {0, 1, 1}
         hoverDist = 1.2
@@ -79,7 +147,6 @@
         sideDamping = 0.03
         thrusterCount = 6
     end
-
     body = FindBody("vehiclebody")
     wheelJoint = FindJoint("wheelJoint")
     gearJointL = FindJoint("gearl")
@@ -110,15 +177,15 @@
     boosts = maxBoosts
     activeBefore = true
     thrusterVoxCount = GetShapeVoxelCount(GetBodyShapes(thrusters[1])[1])
-
-end
-
-function tick(dt) 
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if active then
         local bodyTransform = GetBodyTransform(body)
         local hits = false
         if (GetVehicleHealth(vehicle) == 0 and active) then 
-            SetPlayerVehicle(0)
+            SetPlayerVehicle(playerId, 0)
             SetTag(vehicle, "nodrive")
             active = false 
             for i=1, thrusterCount do SetShapeEmissiveScale(GetBodyShapes(thrusters[i])[1], 0) end
@@ -166,8 +233,6 @@
                         SetJointMotorTarget(thrusterJoints[i], driveSpeed * -20 + turning * 10, 1)
                     end
 
-
-
                     local transform = GetBodyTransform(thrusters[i])
                     PointLight(transform.pos, 0, 1, 1, 0.3 * thrustMultiplier)
                     Particle("thrust", 0.2)
@@ -226,7 +291,7 @@
             --if rot[4] < 0 then reverse = 1 else
             --local correction = {rot[1] * stabilisation * reverse, rot[3] * stabilisation * reverse}
             --SetBodyAngularVelocity(body, VecAdd(Vec(correction[1], 0, correction[2]), VecScale(GetBodyAngularVelocity(body), 0.2)))
-            if GetPlayerVehicle() == vehicle then
+            if GetPlayerVehicle(playerId) == vehicle then
                 local airMove = 0
                 if InputDown("up") then airMove = 0.1 end
                 if InputDown("down") then airMove = -0.1 end
@@ -236,7 +301,7 @@
             SetBodyAngularVelocity(body, VecScale(GetBodyAngularVelocity(body), 1 - angularDamping))
             sideVel = TransformToLocalVec(bodyTransform, GetBodyVelocity(body))[1]
             SetBodyVelocity(body, VecAdd(GetBodyVelocity(body), TransformToParentVec(bodyTransform, Vec(sideVel * -sideDamping, 0, 0))))
-            
+
             if hits and InputDown("jump") then
                 SetBodyVelocity(body, VecScale(GetBodyVelocity(body), 1 - (damping * 5)))
                 driveSpeed = driveSpeed * 0.8
@@ -244,7 +309,7 @@
                 SetBodyVelocity(body, VecScale(GetBodyVelocity(body), 1 - damping))
             end
         end
-        if vehicle == GetPlayerVehicle() then 
+        if vehicle == GetPlayerVehicle(playerId) then 
             local invertTurn = 1
             if InputDown("up") then driveSpeed = driveSpeed + acceleration end
             if InputDown("down") then 
@@ -279,7 +344,7 @@
             end
             driveTime = driveTime + dt
         else
-            if driveTime > 0 then
+            if driveTime ~= 0 then
                 driveTime = 0
             end
             driveTime = driveTime - dt
@@ -323,76 +388,3 @@
     end
 end
 
-function RejectBodies()
-    QueryRejectBody(body) 
-    for i=1, thrusterCount do
-        QueryRejectBody(thrusters[i])
-    end
-end
-
-function RandomVector(size)
-    return VecScale(VecNormalize(Vec(Random(true), Random(true), Random(true))), size)
-end
-
-function Random(negative)
-    if negative then return math.random(-1000, 1000) / 1000 end
-    return math.random(0, 1000) / 1000
-end
-
-function Lerp(a, b, x)
-    return (a * (1 - x)) + (b * x)
-end
-
-function Particle(particleType, size)
-    if particleType == "colour" then
-        ParticleReset()
-        ParticleColor(vehicleColour[1], vehicleColour[2], vehicleColour[3])
-        ParticleEmissive(16)
-        ParticleRadius(size, size / 2)
-        ParticleCollide(0)
-    end
-    if particleType == "thrust" then
-        ParticleReset()
-        ParticleColor(0, 1, 1)
-        ParticleEmissive(16)
-        ParticleRadius(size, size / 2)
-        ParticleCollide(0)
-    end
-    if particleType == "spark" then
-        ParticleReset()
-        ParticleTile(6)
-        ParticleColor(1, 0.8, 0.6)
-        ParticleEmissive(2)
-        ParticleRadius(size, size / 2)
-        ParticleCollide(0)
-    end
-    if particleType == "dust" then
-        ParticleReset()
-        ParticleTile(6)
-        ParticleColor(0, 0, 0)
-        ParticleEmissive(0)
-        ParticleRadius(size, 0)
-        ParticleGravity(-9.81)
-        ParticleCollide(1)
-    end
-    if particleType == "smoke" then
-        ParticleReset()
-        ParticleType("smoke")
-        ParticleColor(1, 1, 1)
-        ParticleEmissive(0)
-        ParticleRadius(size, 0)
-        ParticleGravity(0.4)
-        ParticleDrag(0.8)
-        ParticleCollide(0)
-    end
-        if particleType == "water" then
-        ParticleReset()
-        ParticleTile(1)
-        ParticleColor(0.7, 0.8, 1)
-        ParticleEmissive(0)
-        ParticleRadius(size, 0)
-        ParticleGravity(-2)
-        ParticleDrag(0.2)
-        ParticleCollide(0)
-    end
-end
```

---

# Migration Report: Scripts\Lamp.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\Lamp.lua
+++ patched/Scripts\Lamp.lua
@@ -1,36 +1,36 @@
-function init()	
-	--Find handles to the light switch and and lamp
-	switch = FindShape("switch")
-	lamp = FindLight("lamp")
-
-	--The light should start turned off
-	on = false
-	SetLightEnabled(lamp, false)
-	SetTag(switch, "interact", "Turn on")
-
-	--Load sounds from the game asset folder (data/snd)
-	onSound = LoadSound("MOD/Sounds/LightOn.ogg")
-	offSound = LoadSound("MOD/Sounds/LightOff.ogg")
+#version 2
+function server.init()
+    switch = FindShape("switch")
+    lamp = FindLight("lamp")
+    --The light should start turned off
+    on = false
+    SetLightEnabled(lamp, false)
+    SetTag(switch, "interact", "Turn on")
+    --Load sounds from the game asset folder (data/snd)
 end
 
-
-function tick()
-	--Check if player interacts with light switch and presses interact button
-	if GetPlayerInteractShape() == switch and InputPressed("interact") then
-
-		--Turn light on or off, depending on the current state
-		if on then
-			on = false
-			PlaySound(offSound)
-			SetLightEnabled(lamp, false)
-			SetTag(switch, "interact", "Turn on")
-		else
-			on = true
-			PlaySound(onSound)
-			SetLightEnabled(lamp, true)
-			SetTag(switch, "interact", "Turn off")
-		end
-		
-	end
+function client.init()
+    onSound = LoadSound("MOD/Sounds/LightOn.ogg")
+    offSound = LoadSound("MOD/Sounds/LightOff.ogg")
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == switch and InputPressed("interact") then
+
+    	--Turn light on or off, depending on the current state
+    	if on then
+    		on = false
+    		PlaySound(offSound)
+    		SetLightEnabled(lamp, false)
+    		SetTag(switch, "interact", "Turn on")
+    	else
+    		on = true
+    		PlaySound(onSound)
+    		SetLightEnabled(lamp, true)
+    		SetTag(switch, "interact", "Turn off")
+    	end
+
+    end
+end
+

```

---

# Migration Report: Scripts\pine.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\pine.lua
+++ patched/Scripts\pine.lua
@@ -1,3 +1,4 @@
+#version 2
 function clamp(a, mi, ma)
 	if a < mi then return mi
 	elseif a > ma then return ma
@@ -5,69 +6,16 @@
 	end
 end
 
-pRandom = GetInt("random", 1)
-pSize = clamp(GetFloat("size", 1), 0.1, 3)
-pTrunkBrush = GetString("brush", "MOD/textures/tree/trunk-pine.vox")
-pTwisted = clamp(GetFloat("twisted", 0.5), 0, 3)
-pTrunkHeight = GetFloat("trunkheight", 2.0)*10
-pDensity = clamp(GetFloat("branchdensity", 1), 0, 3)
-pBranchLength = clamp(GetFloat("branchlength", 1), 0, 3)
-pBranchDir = clamp(GetFloat("branchdir", -0.5), -5, 5)
-pLeaves = clamp(GetFloat("leaves", 1), 0, 2)
-pDarknessFactor = clamp(GetFloat("darkness", 0.65), 0.1, 2.0)
-pBrightnessFactor = clamp(GetFloat("brightness", 0.8), 0.1, 2.0)
-
-pTrunkWidth = pSize*3.5
-pBranchLength = pBranchLength*pSize*20
-pMaxIter = math.floor(100*pSize / 5)
-pSize = 5
-pTwisted = pTwisted/pMaxIter
-pDensity =pDensity * 30
-
-gLeaves = {}
-
 function normalize(x,y,z)
 	local l = math.sqrt(x*x + y*y + z*z);
 	return x/l, y/l, z/l
 end
-
-
-function init()
-	if pRandom ~= 0 then
-		Randomize(pRandom)
-	end
-
-	wood = CreateBrush(pTrunkBrush)
-
-	leaves = {}
-	local rD = RandomFloat(0.30, 0.34)*pDarknessFactor
-	local gD = RandomFloat(0.37, 0.42)*pDarknessFactor
-	local bD = RandomFloat(0.28, 0.32)*pDarknessFactor
-	local rB = (RandomFloat(0.41, 0.46)*pBrightnessFactor-rD)/8
-	local gB = (RandomFloat(0.50, 0.56)*pBrightnessFactor-gD)/8
-	local bB = (RandomFloat(0.39, 0.44)*pBrightnessFactor-bD)/8
-
-	for i=1, 8 do
-		--leaves[i] = CreateMaterial("foliage", t*0.9, t*RandomFloat(0.8, 1.3), t)
-		leaves[i] = CreateMaterial("foliage", rD+rB*i, gD+gB*i, bD+bB*i)
-		--leaves[i] = CreateMaterial("foliage", rB*8, gB*8, bB*8)
-	end
-
-	Vox()
-
-	generateBranches(0, 0, 0, 0, 1, 0, 1)
-	generateLeaves()
-	Material(0)
-	Box(-pTrunkWidth, -pTrunkWidth, -pTrunkWidth, pTrunkWidth, 0, pTrunkWidth)
-end
-
 
 function getBranchSize(iter)
 	local t = (iter-1)/pMaxIter
 	t = t * t
 	return (1-t)*pTrunkWidth
 end
-
 
 function branch(x, y, z, dx, dy, dz, l)
 	local steps = math.ceil(l/3)
@@ -167,3 +115,27 @@
 	end
 end
 
+function server.init()
+    if pRandom ~= 0 then
+    	Randomize(pRandom)
+    end
+    wood = CreateBrush(pTrunkBrush)
+    leaves = {}
+    local rD = RandomFloat(0.30, 0.34)*pDarknessFactor
+    local gD = RandomFloat(0.37, 0.42)*pDarknessFactor
+    local bD = RandomFloat(0.28, 0.32)*pDarknessFactor
+    local rB = (RandomFloat(0.41, 0.46)*pBrightnessFactor-rD)/8
+    local gB = (RandomFloat(0.50, 0.56)*pBrightnessFactor-gD)/8
+    local bB = (RandomFloat(0.39, 0.44)*pBrightnessFactor-bD)/8
+    for i=1, 8 do
+    	--leaves[i] = CreateMaterial("foliage", t*0.9, t*RandomFloat(0.8, 1.3), t)
+    	leaves[i] = CreateMaterial("foliage", rD+rB*i, gD+gB*i, bD+bB*i)
+    	--leaves[i] = CreateMaterial("foliage", rB*8, gB*8, bB*8)
+    end
+    Vox()
+    generateBranches(0, 0, 0, 0, 1, 0, 1)
+    generateLeaves()
+    Material(0)
+    Box(-pTrunkWidth, -pTrunkWidth, -pTrunkWidth, pTrunkWidth, 0, pTrunkWidth)
+end
+

```

---

# Migration Report: Scripts\PoliceLightsF.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\PoliceLightsF.lua
+++ patched/Scripts\PoliceLightsF.lua
@@ -1,31 +1,33 @@
-function init()
-	lights = FindShapes("blink")
-	pLights = false
-	vehicle = FindVehicle()
+#version 2
+function server.init()
+    lights = FindShapes("blink")
+    pLights = false
+    vehicle = FindVehicle()
 end
 
-function draw()
-	if InputPressed("f") then
-		if GetPlayerVehicle() == vehicle then
-		 	if pLights == false then
-				pLights = true
-			else
-				pLights = false
-			end
-		end
-	end
-	if pLights then
-		for i=1, #lights do
-			local l = lights[i]
-			local p = tonumber(GetTagValue(l, "blink"))
-			if p then
-				local s = math.sin((GetTime()+i) * p)
-				SetShapeEmissiveScale(l, s > 0 and 1 or 0)
-			end
-		end
-	else
-		for i=1, #lights do
-			SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
-		end
-	end
+function client.draw()
+    if InputPressed("f") then
+    	if GetPlayerVehicle(playerId) == vehicle then
+    	 	if pLights == false then
+    			pLights = true
+    		else
+    			pLights = false
+    		end
+    	end
+    end
+    if pLights then
+    	for i=1, #lights do
+    		local l = lights[i]
+    		local p = tonumber(GetTagValue(l, "blink"))
+    		if p then
+    			local s = math.sin((GetTime()+i) * p)
+    			SetShapeEmissiveScale(l, s > 0 and 1 or 0)
+    		end
+    	end
+    else
+    	for i=1, #lights do
+    		SetShapeEmissiveScale(lights[i], 0 > 0 and 1 or 0)
+    	end
+    end
 end
+

```

---

# Migration Report: Scripts\radio.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\radio.lua
+++ patched/Scripts\radio.lua
@@ -1,45 +1,45 @@
-on = true
-function init()	
-	--Find handle to radio
-	radio = FindShape("radio")
-	
-	--Make sure the light is turned off and make interactable
-	SetShapeEmissiveScale(radio, 0)
-	SetTag(radio, "interact", "Turn on")
-	
-	--Load click sound and music from game assets
-	clickSound = LoadSound("clickdown.ogg")
-	musicLoop = LoadLoop("MOD/sounds/radios/nebo_kazhe_idy_syda.ogg")
-	
+#version 2
+function server.init()
+    radio = FindShape("radio")
+    --Make sure the light is turned off and make interactable
+    SetShapeEmissiveScale(radio, 0)
+    SetTag(radio, "interact", "Turn on")
+    --Load click sound and music from game assets
+    musicLoop = LoadLoop("MOD/sounds/radios/nebo_kazhe_idy_syda.ogg")
 end
 
-
-function tick(dt)
-	--If radio is broken it should not be interactable and not function
-	if IsShapeBroken(radio) then
-		RemoveTag(radio, "interact")
-		return
-	end
-
-	--Turn on/off radio
-	if GetPlayerInteractShape() == radio and InputPressed("interact") then
-		PlaySound(clickSound)
-		if on then
-			on = false
-			SetShapeEmissiveScale(radio, 0)
-			SetTag(radio, "interact", "Turn on")			
-		else
-			on = true
-			SetShapeEmissiveScale(radio, 0.1)
-			SetTag(radio, "interact", "Turn off")			
-		end
-	end
-
-	--If radio is on, play music at the world position
-	if on then 
-		local pos = GetShapeWorldTransform(radio).pos
-		PlayLoop(musicLoop, pos)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(radio) then
+        	RemoveTag(radio, "interact")
+        	return
+        end
+        --Turn on/off radio
+        --If radio is on, play music at the world position
+    end
 end
 
+function client.init()
+    clickSound = LoadSound("clickdown.ogg")
+end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == radio and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if on then
+    		on = false
+    		SetShapeEmissiveScale(radio, 0)
+    		SetTag(radio, "interact", "Turn on")			
+    	else
+    		on = true
+    		SetShapeEmissiveScale(radio, 0.1)
+    		SetTag(radio, "interact", "Turn off")			
+    	end
+    end
+    if on then 
+    	local pos = GetShapeWorldTransform(radio).pos
+    	PlayLoop(musicLoop, pos)
+    end
+end
+

```

---

# Migration Report: Scripts\Radio_Car.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\Radio_Car.lua
+++ patched/Scripts\Radio_Car.lua
@@ -1,45 +1,45 @@
-on = false
-function init()	
-	--Find handle to radio
-	radio = FindShape("radio")
-	
-	--Make sure the light is turned off and make interactable
-	SetShapeEmissiveScale(radio, 0)
-	SetTag(radio, "interact", "Turn on")
-	
-	--Load click sound and music from game assets
-	clickSound = LoadSound("MOD/Sounds/RadioInteract.ogg")
-	musicLoop = LoadLoop("MOD/Sounds/Radio_Volvo.ogg")
-	
+#version 2
+function server.init()
+    radio = FindShape("radio")
+    --Make sure the light is turned off and make interactable
+    SetShapeEmissiveScale(radio, 0)
+    SetTag(radio, "interact", "Turn on")
+    --Load click sound and music from game assets
+    musicLoop = LoadLoop("MOD/Sounds/Radio_Volvo.ogg")
 end
 
-
-function tick(dt)
-	--If radio is broken it should not be interactable and not function
-	if IsShapeBroken(radio) then
-		RemoveTag(radio, "interact")
-		return
-	end
-
-	--Turn on/off radio
-	if GetPlayerInteractShape() == radio and InputPressed("interact") then
-		PlaySound(clickSound)
-		if on then
-			on = false
-			SetShapeEmissiveScale(radio, 0)
-			SetTag(radio, "interact", "Turn on")			
-		else
-			on = true
-			SetShapeEmissiveScale(radio, 1)
-			SetTag(radio, "interact", "Turn off")			
-		end
-	end
-
-	--If radio is on, play music at the world position
-	if on then 
-		local pos = GetShapeWorldTransform(radio).pos
-		PlayLoop(musicLoop, pos)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(radio) then
+        	RemoveTag(radio, "interact")
+        	return
+        end
+        --Turn on/off radio
+        --If radio is on, play music at the world position
+    end
 end
 
+function client.init()
+    clickSound = LoadSound("MOD/Sounds/RadioInteract.ogg")
+end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == radio and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if on then
+    		on = false
+    		SetShapeEmissiveScale(radio, 0)
+    		SetTag(radio, "interact", "Turn on")			
+    	else
+    		on = true
+    		SetShapeEmissiveScale(radio, 1)
+    		SetTag(radio, "interact", "Turn off")			
+    	end
+    end
+    if on then 
+    	local pos = GetShapeWorldTransform(radio).pos
+    	PlayLoop(musicLoop, pos)
+    end
+end
+

```

---

# Migration Report: Scripts\tree.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Scripts\tree.lua
+++ patched/Scripts\tree.lua
@@ -1,3 +1,6 @@
+#version 2
+local size = 150*pSize/pMaxIter
+
 function clamp(a, mi, ma)
 	if a < mi then return mi
 	elseif a > ma then return ma
@@ -5,44 +8,10 @@
 	end
 end
 
-pRandom = GetInt("randomseed", 1)
-pMaxIter = clamp(GetInt("iterations", 12), 5, 15)
-pTrunkBrush = GetString("trunkbrush", "MOD/textures/tree/trunk-oak.vox")
-pLeafBrush = GetString("leafbrush", "MOD/textures/tree/leaf.vox")
-pSize = clamp(GetFloat("size", 1), 0.1, 3.0)
-pTrunkSize = clamp(GetFloat("trunksize", 1), 0.1, 3)
-pWide = clamp(GetFloat("wide", 0.5), 0.0, 1.0)
-pSpread = clamp(GetFloat("spread", 0.5), 0.0, 1.0)
-pTwisted = clamp(GetFloat("twisted", 0.5), 0.0, 1.0)
-pLeaves = clamp(GetFloat("leaves", 1), 0.0, 3.0)
-pGravity = clamp(GetFloat("gravity", 0), -1.0, 1.0)
-
-local size = 150*pSize/pMaxIter
-gTrunkSize = pTrunkSize * pSize * 6
-gBranchLength0 = size*(1-pWide)
-gBranchLength1 = size*pWide
-gTrunk = true
-gLeaves = {}
-
 function normalize(x,y,z)
 	local l = math.sqrt(x*x + y*y + z*z);
 	return x/l, y/l, z/l
 end
-
-
-function init()
-	if pRandom ~= 0 then
-		Randomize(pRandom)
-	end
-
-	matWood = CreateBrush(pTrunkBrush)
-	matLeaf = CreateBrush(pLeafBrush)
-
-	Vox()
-	generateBranches(0, 0, 0, 0, 1, 0, 1)
-	generateLeaves()
-end
-
 
 function getBranchSize(iter)
 	local t = (iter-1)/pMaxIter
@@ -148,3 +117,15 @@
 	
 	end
 end
+
+function server.init()
+    if pRandom ~= 0 then
+    	Randomize(pRandom)
+    end
+    matWood = CreateBrush(pTrunkBrush)
+    matLeaf = CreateBrush(pLeafBrush)
+    Vox()
+    generateBranches(0, 0, 0, 0, 1, 0, 1)
+    generateLeaves()
+end
+

```

---

# Migration Report: Sounds\Radio_bass.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Sounds\Radio_bass.lua
+++ patched/Sounds\Radio_bass.lua
@@ -1,45 +1,45 @@
-on = false
-function init()	
-	--Find handle to radio
-	radio = FindShape("radio")
-	
-	--Make sure the light is turned off and make interactable
-	SetShapeEmissiveScale(radio, 0)
-	SetTag(radio, "interact", "Turn on")
-	
-	--Load click sound and music from game assets
-	clickSound = LoadSound("MOD/Sounds/LightOn.ogg")
-	musicLoop = LoadLoop("MOD/Sounds/BassRadio.ogg")
-	
+#version 2
+function server.init()
+    radio = FindShape("radio")
+    --Make sure the light is turned off and make interactable
+    SetShapeEmissiveScale(radio, 0)
+    SetTag(radio, "interact", "Turn on")
+    --Load click sound and music from game assets
+    musicLoop = LoadLoop("MOD/Sounds/BassRadio.ogg")
 end
 
-
-function tick(dt)
-	--If radio is broken it should not be interactable and not function
-	if IsShapeBroken(radio) then
-		RemoveTag(radio, "interact")
-		return
-	end
-
-	--Turn on/off radio
-	if GetPlayerInteractShape() == radio and InputPressed("interact") then
-		PlaySound(clickSound)
-		if on then
-			on = false
-			SetShapeEmissiveScale(radio, 0)
-			SetTag(radio, "interact", "Turn on")			
-		else
-			on = true
-			SetShapeEmissiveScale(radio, 1)
-			SetTag(radio, "interact", "Turn off")			
-		end
-	end
-
-	--If radio is on, play music at the world position
-	if on then 
-		local pos = GetShapeWorldTransform(radio).pos
-		PlayLoop(musicLoop, pos)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(radio) then
+        	RemoveTag(radio, "interact")
+        	return
+        end
+        --Turn on/off radio
+        --If radio is on, play music at the world position
+    end
 end
 
+function client.init()
+    clickSound = LoadSound("MOD/Sounds/LightOn.ogg")
+end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == radio and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if on then
+    		on = false
+    		SetShapeEmissiveScale(radio, 0)
+    		SetTag(radio, "interact", "Turn on")			
+    	else
+    		on = true
+    		SetShapeEmissiveScale(radio, 1)
+    		SetTag(radio, "interact", "Turn off")			
+    	end
+    end
+    if on then 
+    	local pos = GetShapeWorldTransform(radio).pos
+    	PlayLoop(musicLoop, pos)
+    end
+end
+

```

---

# Migration Report: Sounds\Radio_Car.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Sounds\Radio_Car.lua
+++ patched/Sounds\Radio_Car.lua
@@ -1,45 +1,45 @@
-on = false
-function init()	
-	--Find handle to radio
-	radio = FindShape("radio")
-	
-	--Make sure the light is turned off and make interactable
-	SetShapeEmissiveScale(radio, 0)
-	SetTag(radio, "interact", "Turn on")
-	
-	--Load click sound and music from game assets
-	clickSound = LoadSound("MOD/Sounds/LightOn.ogg")
-	musicLoop = LoadLoop("MOD/Sounds/Radio.ogg")
-	
+#version 2
+function server.init()
+    radio = FindShape("radio")
+    --Make sure the light is turned off and make interactable
+    SetShapeEmissiveScale(radio, 0)
+    SetTag(radio, "interact", "Turn on")
+    --Load click sound and music from game assets
+    musicLoop = LoadLoop("MOD/Sounds/Radio.ogg")
 end
 
-
-function tick(dt)
-	--If radio is broken it should not be interactable and not function
-	if IsShapeBroken(radio) then
-		RemoveTag(radio, "interact")
-		return
-	end
-
-	--Turn on/off radio
-	if GetPlayerInteractShape() == radio and InputPressed("interact") then
-		PlaySound(clickSound)
-		if on then
-			on = false
-			SetShapeEmissiveScale(radio, 0)
-			SetTag(radio, "interact", "Turn on")			
-		else
-			on = true
-			SetShapeEmissiveScale(radio, 1)
-			SetTag(radio, "interact", "Turn off")			
-		end
-	end
-
-	--If radio is on, play music at the world position
-	if on then 
-		local pos = GetShapeWorldTransform(radio).pos
-		PlayLoop(musicLoop, pos)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(radio) then
+        	RemoveTag(radio, "interact")
+        	return
+        end
+        --Turn on/off radio
+        --If radio is on, play music at the world position
+    end
 end
 
+function client.init()
+    clickSound = LoadSound("MOD/Sounds/LightOn.ogg")
+end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == radio and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if on then
+    		on = false
+    		SetShapeEmissiveScale(radio, 0)
+    		SetTag(radio, "interact", "Turn on")			
+    	else
+    		on = true
+    		SetShapeEmissiveScale(radio, 1)
+    		SetTag(radio, "interact", "Turn off")			
+    	end
+    end
+    if on then 
+    	local pos = GetShapeWorldTransform(radio).pos
+    	PlayLoop(musicLoop, pos)
+    end
+end
+

```

---

# Migration Report: Sounds\Radio_siren.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Sounds\Radio_siren.lua
+++ patched/Sounds\Radio_siren.lua
@@ -1,45 +1,45 @@
-on = false
-function init()	
-	--Find handle to radio
-	radio = FindShape("radio")
-	
-	--Make sure the light is turned off and make interactable
-	SetShapeEmissiveScale(radio, 0)
-	SetTag(radio, "interact", "Turn on")
-	
-	--Load click sound and music from game assets
-	clickSound = LoadSound("MOD/Sounds/LightOn.ogg")
-	musicLoop = LoadLoop("MOD/Sounds/Siren.ogg")
-	
+#version 2
+function server.init()
+    radio = FindShape("radio")
+    --Make sure the light is turned off and make interactable
+    SetShapeEmissiveScale(radio, 0)
+    SetTag(radio, "interact", "Turn on")
+    --Load click sound and music from game assets
+    musicLoop = LoadLoop("MOD/Sounds/Siren.ogg")
 end
 
-
-function tick(dt)
-	--If radio is broken it should not be interactable and not function
-	if IsShapeBroken(radio) then
-		RemoveTag(radio, "interact")
-		return
-	end
-
-	--Turn on/off radio
-	if GetPlayerInteractShape() == radio and InputPressed("interact") then
-		PlaySound(clickSound)
-		if on then
-			on = false
-			SetShapeEmissiveScale(radio, 0)
-			SetTag(radio, "interact", "Turn on")			
-		else
-			on = true
-			SetShapeEmissiveScale(radio, 1)
-			SetTag(radio, "interact", "Turn off")			
-		end
-	end
-
-	--If radio is on, play music at the world position
-	if on then 
-		local pos = GetShapeWorldTransform(radio).pos
-		PlayLoop(musicLoop, pos)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsShapeBroken(radio) then
+        	RemoveTag(radio, "interact")
+        	return
+        end
+        --Turn on/off radio
+        --If radio is on, play music at the world position
+    end
 end
 
+function client.init()
+    clickSound = LoadSound("MOD/Sounds/LightOn.ogg")
+end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == radio and InputPressed("interact") then
+    	PlaySound(clickSound)
+    	if on then
+    		on = false
+    		SetShapeEmissiveScale(radio, 0)
+    		SetTag(radio, "interact", "Turn on")			
+    	else
+    		on = true
+    		SetShapeEmissiveScale(radio, 1)
+    		SetTag(radio, "interact", "Turn off")			
+    	end
+    end
+    if on then 
+    	local pos = GetShapeWorldTransform(radio).pos
+    	PlayLoop(musicLoop, pos)
+    end
+end
+

```
