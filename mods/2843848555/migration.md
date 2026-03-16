# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,87 +1,4 @@
-#include "snippets.lua"
-
-
-function init()
-
-    toolname = "lightning_stick"
-
-    RegisterTool(toolname, "Lightning Stick", "MOD/vox/" .. toolname .. ".vox")
-	SetBool("game.tool." .. toolname .. ".enabled", true)
-
-    --[[
-        animations
-            [i]
-                state
-                [j]
-                    {time, pos, rot}
-    ]]
-
-    -- default pos = Vec(0.4, -0.8, -0.35), QuatEuler(-30, 0, 10)
-    animations = {}
-    animations[#animations + 1] = {
-        state = 1,
-        timeLeft = nil,
-        name = "ignite",
-        effect = {false, false, true, true},
-        pos = {makeAnimation(0.3, Vec(-0.15, 0.3, -0.35), Vec(-50, 0, 0)),
-               makeAnimation(0.6, Vec(0.0, 0.0, 0.0), Vec(0, 0, 0)),
-               makeAnimation(0.3, Vec(0.15, -0.3, 0.35), Vec(50, 0, 0))}
-    }
-
-    animation = nil
-
-    first = true
-
-    tt = defaultTransform()
-
-    balls = {}
-
-end
-
-function tick(dt)
-
-    if animation ~= nil and isDoingEffect(animation) then
-        SetBool("level.bombard.ignite", true)
-    else
-        SetBool("level.bombard.ignite", false)
-    end
-
-    if isToolInHand() then
-        if InputPressed("usetool") then
-            if animation == nil then
-                tt = defaultTransform()
-                animation = deepcopy(animations[1])
-            end
-        end
-
-        if animation ~= nil then
-            handleAnimation(dt)
-        else
-            tt = defaultTransform()
-        end
-
-        SetToolTransform(tt)
-    end
-end
-
-function update(dt)
-    if first then
-        first = false
-    end
-
-    balls = FindBodies("", true)--FindBodies("bombardball", true)
-
-    if isToolInHand() then
-        
-    end
-end
-
-function draw(dt)
-    if isToolInHand() then
-        
-    end
-end
-
+#version 2
 function isDoingEffect(a)
     if a ~= nil then
         return (animation.effect[animation.state] ~= nil and animation.effect[animation.state] == true)
@@ -194,45 +111,74 @@
 	end
 end
 
+function server.init()
+       toolname = "lightning_stick"
+       RegisterTool(toolname, "Lightning Stick", "MOD/vox/" .. toolname .. ".vox")
+    SetBool("game.tool." .. toolname .. ".enabled", true, true)
+       --[[
+           animations
+               [i]
+                   state
+                   [j]
+                       {time, pos, rot}
+       ]]
+       -- default pos = Vec(0.4, -0.8, -0.35), QuatEuler(-30, 0, 10)
+       animations = {}
+       animations[#animations + 1] = {
+           state = 1,
+           timeLeft = nil,
+           name = "ignite",
+           effect = {false, false, true, true},
+           pos = {makeAnimation(0.3, Vec(-0.15, 0.3, -0.35), Vec(-50, 0, 0)),
+                  makeAnimation(0.6, Vec(0.0, 0.0, 0.0), Vec(0, 0, 0)),
+                  makeAnimation(0.3, Vec(0.15, -0.3, 0.35), Vec(50, 0, 0))}
+       }
+       animation = nil
+       first = true
+       tt = defaultTransform()
+       balls = {}
+end
 
+function server.tick(dt)
+    if animation ~= nil and isDoingEffect(animation) then
+        SetBool("level.bombard.ignite", true, true)
+    else
+        SetBool("level.bombard.ignite", false, true)
+    end
+end
 
+function server.update(dt)
+    if first then
+        first = false
+    end
+    balls = FindBodies("", true)--FindBodies("bombardball", true)
+    if isToolInHand() then
 
+    end
+end
 
+function client.tick(dt)
+    if isToolInHand() then
+        if InputPressed("usetool") then
+            if animation == nil then
+                tt = defaultTransform()
+                animation = deepcopy(animations[1])
+            end
+        end
 
+        if animation ~= nil then
+            handleAnimation(dt)
+        else
+            tt = defaultTransform()
+        end
 
+        SetToolTransform(tt)
+    end
+end
 
+function client.draw()
+    if isToolInHand() then
 
+    end
+end
 
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
-
-
-
-
-
-
-
-
-

```

---

# Migration Report: scripts\ball.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ball.lua
+++ patched/scripts\ball.lua
@@ -1,35 +1,4 @@
-
-function init()
-    body = FindBody("bombardball")
-    radius = 1.0
-
-    trigger1 = false
-    trigger2 = false
-    breaking = 500
-    ratio = {
-        soft = 0.1,
-        medium = 0.1,
-        hard = 3
-    }
-end
-
-function tick(dt)
-    local vel = GetBodyVelocity(body)
-    sparks(GetBodyTransform(body).pos)
-
-    if VecLength(vel) >= 30 then
-        local count = 0
-        local pos = VecAdd(GetBodyTransform(body).pos, VecScale(vel, dt))
-        local radius = 1
-        count = count + MakeHole(pos, radius, radius, radius / 2) * ratio.soft
-        breaking = breaking - count
-        if breaking <= 0 then
-            Delete(body)
-            trigger1 = false
-        end
-    end
-end
-
+#version 2
 function randVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -83,4 +52,34 @@
 
 		SpawnParticle(p, v, l)
 	end
-end+end
+
+function server.init()
+    body = FindBody("bombardball")
+    radius = 1.0
+    trigger1 = false
+    trigger2 = false
+    breaking = 500
+    ratio = {
+        soft = 0.1,
+        medium = 0.1,
+        hard = 3
+    }
+end
+
+function server.tick(dt)
+    local vel = GetBodyVelocity(body)
+    sparks(GetBodyTransform(body).pos)
+    if VecLength(vel) >= 30 then
+        local count = 0
+        local pos = VecAdd(GetBodyTransform(body).pos, VecScale(vel, dt))
+        local radius = 1
+        count = count + MakeHole(pos, radius, radius, radius / 2) * ratio.soft
+        breaking = breaking - count
+        if breaking <= 0 then
+            Delete(body)
+            trigger1 = false
+        end
+    end
+end
+

```

---

# Migration Report: scripts\bombard.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\bombard.lua
+++ patched/scripts\bombard.lua
@@ -1,79 +1,4 @@
-#include "../snippets.lua"
-
-function init()
-    joint = FindJoint("pitch")
-    jointLock = GetJointMovement(joint)
-    speed = 80
-
-    local barrelShape = FindShape("barrelShape")
-    local barrelBody = FindBody("barrelBody")
-
-    local barrelTrigger = FindTrigger("barrel")
-    local t = GetTriggerTransform(barrelTrigger)
-    bt = GetBodyTransform(barrelBody)
-    barrel = {}
-    barrel.trigger = barrelTrigger
-    barrel.localTransform = TransformToLocalTransform(bt, t)
-    barrel.body = barrelBody
-    barrel.shape = barrelShape
-
-    big = HasTag(barrelBody, "big")
-
-    canon = {
-        loaded = false,
-        time = {
-            value = 0,
-            default = 2.5
-        },
-        ignited = false
-    }
-
-    meshSprite = LoadSprite("MOD/img/mesh.png")
-    meshSize = 0.3
-    if big then
-        meshSize = meshSize * 2
-    end
-
-    sndBoom = LoadSound("MOD/snd/boom.ogg")
-    sndIgnite = LoadLoop("MOD/snd/ignite.ogg")
-end
-
-function tick(dt)
-
-    bt = GetBodyTransform(barrel.body)
-    movement()
-
-    if canon.ignited then
-        canon.time.value = canon.time.value - dt
-    end
-
-    drawMesh()
-
-    if GetBool("level.bombard.ignite") then
-        local ct = GetPlayerCameraTransform()
-        local dir = TransformToParentVec(ct, Vec(0, 0, -1))
-        local hit, dist, normal, shape = QueryRaycast(ct.pos, dir, 3)
-        if barrel.shape == shape then
-            if canon.loaded then
-                canon.ignited = true
-            end
-        end
-    end
-
-    if canon.time.value <= 0 and canon.ignited then
-        fire()
-        smoke()
-    end
-
-    canon.loaded = isLoaded()
-    if canon.loaded and not canon.ignited then
-        canon.time.value = canon.time.default
-    end
-    if not canon.loaded then
-        canon.time.value = 0
-    end
-end
-
+#version 2
 function movement()
     local bt = GetBodyTransform(barrel.body)
     local t  = TransformToParentTransform(bt, barrel.localTransform)
@@ -82,7 +7,7 @@
     t.pos = VecAdd(t.pos, VecScale(tFwd, 0.15))
     SetTriggerTransform(barrel.trigger,t)
 
-    if GetPlayerGrabBody() == barrel.body then 
+    if GetPlayerGrabBody(playerId) == barrel.body then 
         SetJointMotor(joint, 0, 0)
         jointLock = GetJointMovement(joint)
     else
@@ -101,10 +26,10 @@
             --return
         end
     end
-    local t = GetPlayerTransform()
+    local t = GetPlayerTransform(playerId)
     if IsPointInTrigger(barrel.trigger,t.pos) then
         PlaySound(sndBoom, t.pos, 0.6)
-        SetPlayerVelocity(TransformToParentVec(GetBodyTransform(barrel.body), Vec(0, 0, -speed)))
+        SetPlayerVelocity(playerId, TransformToParentVec(GetBodyTransform(barrel.body), Vec(0, 0, -speed)))
     end
 end
 
@@ -116,7 +41,7 @@
             return true
         end
     end
-    local t = GetPlayerTransform()
+    local t = GetPlayerTransform(playerId)
     if IsPointInTrigger(barrel.trigger,t.pos) then
         return true
     end
@@ -235,4 +160,70 @@
 
 		SpawnParticle(p, v, l)
 	end
-end+end
+
+function server.init()
+    joint = FindJoint("pitch")
+    jointLock = GetJointMovement(joint)
+    speed = 80
+    local barrelShape = FindShape("barrelShape")
+    local barrelBody = FindBody("barrelBody")
+    local barrelTrigger = FindTrigger("barrel")
+    local t = GetTriggerTransform(barrelTrigger)
+    bt = GetBodyTransform(barrelBody)
+    barrel = {}
+    barrel.trigger = barrelTrigger
+    barrel.localTransform = TransformToLocalTransform(bt, t)
+    barrel.body = barrelBody
+    barrel.shape = barrelShape
+    big = HasTag(barrelBody, "big")
+    canon = {
+        loaded = false,
+        time = {
+            value = 0,
+            default = 2.5
+        },
+        ignited = false
+    }
+    meshSprite = LoadSprite("MOD/img/mesh.png")
+    meshSize = 0.3
+    if big then
+        meshSize = meshSize * 2
+    end
+    sndIgnite = LoadLoop("MOD/snd/ignite.ogg")
+end
+
+function server.tick(dt)
+    bt = GetBodyTransform(barrel.body)
+    movement()
+    if canon.ignited then
+        canon.time.value = canon.time.value - dt
+    end
+    drawMesh()
+    if GetBool("level.bombard.ignite") then
+        local ct = GetPlayerCameraTransform(playerId)
+        local dir = TransformToParentVec(ct, Vec(0, 0, -1))
+        local hit, dist, normal, shape = QueryRaycast(ct.pos, dir, 3)
+        if barrel.shape == shape then
+            if canon.loaded then
+                canon.ignited = true
+            end
+        end
+    end
+    if canon.time.value <= 0 and canon.ignited then
+        fire()
+        smoke()
+    end
+    canon.loaded = isLoaded()
+    if canon.loaded and not canon.ignited then
+        canon.time.value = canon.time.default
+    end
+    if not canon.loaded then
+        canon.time.value = 0
+    end
+end
+
+function client.init()
+    sndBoom = LoadSound("MOD/snd/boom.ogg")
+end
+

```

---

# Migration Report: scripts\explosiveball.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\explosiveball.lua
+++ patched/scripts\explosiveball.lua
@@ -1,32 +1,4 @@
-
-function init()
-    body = FindBody("bombardball")
-    radius = 1.0
-
-    trigger1 = false
-    trigger2 = false
-end
-
-function tick(dt)
-    local vel = GetBodyVelocity(body)
-    sparks(GetBodyTransform(body).pos)
-    if VecLength(vel) > 30 then
-        trigger1 = true
-    end
-    if trigger1 then
-        QueryRejectBody(body)
-        --local hit, point, normal, shape = QueryClosestPoint(GetBodyTransform(body).pos, radius)
-        local hit = VecLength(vel) <= 10
-        if trigger2 and hit then
-            Explosion(GetBodyTransform(body).pos, 2)
-            Delete(body)
-            trigger1 = false
-        elseif trigger1 and not hit then
-            trigger2 = true
-        end
-    end
-end
-
+#version 2
 function randVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -82,3 +54,31 @@
 		SpawnParticle(p, v, l)
 	end
 end
+
+function server.init()
+    body = FindBody("bombardball")
+    radius = 1.0
+    trigger1 = false
+    trigger2 = false
+end
+
+function server.tick(dt)
+    local vel = GetBodyVelocity(body)
+    sparks(GetBodyTransform(body).pos)
+    if VecLength(vel) > 30 then
+        trigger1 = true
+    end
+    if trigger1 then
+        QueryRejectBody(body)
+        --local hit, point, normal, shape = QueryClosestPoint(GetBodyTransform(body).pos, radius)
+        local hit = VecLength(vel) <= 10
+        if trigger2 and hit then
+            Explosion(GetBodyTransform(body).pos, 2)
+            Delete(body)
+            trigger1 = false
+        elseif trigger1 and not hit then
+            trigger2 = true
+        end
+    end
+end
+

```

---

# Migration Report: scripts\fireball.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\fireball.lua
+++ patched/scripts\fireball.lua
@@ -1,40 +1,4 @@
-
-function init()
-    body = FindBody("bombardball")
-    radius = 1.0
-
-    trigger1 = false
-    trigger2 = false
-    breaking = 500
-    ratio = {
-        soft = 0.1,
-        medium = 0.1,
-        hard = 3
-    }
-end
-
-function tick(dt)
-    local vel = GetBodyVelocity(body)
-    sparks(GetBodyTransform(body).pos)
-
-    if VecLength(vel) >= 30 then
-        local count = 0
-        local pos = VecAdd(GetBodyTransform(body).pos, VecScale(vel, dt))
-        local radius = 1
-        count = count + MakeHole(pos, radius, radius, radius / 2) * ratio.soft
-        if count > 0 then
-            for i=1, 20 do
-                SpawnFire(VecAdd(randVec(randFloat(0.5, 1 * radius)), pos))
-            end
-        end
-        breaking = breaking - count
-        if breaking <= 0 then
-            Delete(body)
-            trigger1 = false
-        end
-    end
-end
-
+#version 2
 function randVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -89,4 +53,42 @@
 
 		SpawnParticle(p, v, l)
 	end
-end+end
+
+function server.init()
+    body = FindBody("bombardball")
+    radius = 1.0
+    trigger1 = false
+    trigger2 = false
+    breaking = 500
+    ratio = {
+        soft = 0.1,
+        medium = 0.1,
+        hard = 3
+    }
+end
+
+function server.tick(dt)
+    local vel = GetBodyVelocity(body)
+    sparks(GetBodyTransform(body).pos)
+end
+
+function client.tick(dt)
+    if VecLength(vel) >= 30 then
+        local count = 0
+        local pos = VecAdd(GetBodyTransform(body).pos, VecScale(vel, dt))
+        local radius = 1
+        count = count + MakeHole(pos, radius, radius, radius / 2) * ratio.soft
+        if count ~= 0 then
+            for i=1, 20 do
+                SpawnFire(VecAdd(randVec(randFloat(0.5, 1 * radius)), pos))
+            end
+        end
+        breaking = breaking - count
+        if breaking <= 0 then
+            Delete(body)
+            trigger1 = false
+        end
+    end
+end
+

```

---

# Migration Report: snippets.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/snippets.lua
+++ patched/snippets.lua
@@ -1,9 +1,4 @@
---This script will run on all levels when mod is active.
---Modding documentation: http://teardowngame.com/modding
---API reference: http://teardowngame.com/modding/api.html
-
----------------------------------
-
+#version 2
 function clearConsole()
 	for i=1, 25 do
 		DebugPrint("")
@@ -22,12 +17,10 @@
 	return math.random(minv, maxv)
 end
 
---Helper to return a random number in range mi to ma
 function randFloat(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
 
---Return a random vector of desired length
 function randVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -48,7 +41,6 @@
     return copy
 end
 
-
 function floorVec(v)
 	return Vec(math.floor(v[1]), math.floor(v[2]), math.floor(v[3]))
 end
@@ -65,44 +57,3 @@
 	return "Vec(" .. v[1] .. ", " .. v[2] .. ", " .. v[3] .. ")"
 end
 
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
-
-
-
-
-

```
