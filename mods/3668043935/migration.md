# Migration Report: lua\gore v25.12.22.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v25.12.22.lua
+++ patched/lua\gore v25.12.22.lua
@@ -1,3 +1,4 @@
+#version 2
 local cached_struggle_joints = {
     knees = {},
     hips = {},
@@ -52,7 +53,338 @@
 local currentOxygen = 100
 local MAX_OXYGEN = 100
 
-function init()
+local function checkTags()
+    local resFound = false
+    local bandFound = false
+    local sedFound = false
+    for _, body in pairs(bodyParts) do
+        if body ~= 0 then
+            if HasTag(body, "resurrected") then resFound = true end
+            if HasTag(body, "bandaged") then bandFound = true end
+            if HasTag(body, "sedated") then sedFound = true end
+        end
+    end
+    isResurrected = resFound
+    isBandaged = bandFound
+    isSedated = sedFound
+end
+
+local function handleSpecialStatus()
+    if isBandaged then
+        for key, body in pairs(bodyParts) do
+            if body ~= 0 then
+                initialMass[key] = GetBodyMass(body)
+                RemoveTag(body, "bandaged")
+            end
+        end
+        isBandaged = false
+    end
+
+    if isResurrected then
+        local canBeSaved = (ragdollState ~= STATE_DEAD and ragdollState ~= STATE_DISABLED)
+        
+        if not permanentDeath and canBeSaved then
+            local healthMap = {
+                head = 50, torso = 350,
+                lArm = 75, lLowerArm = 75,
+                rArm = 75, rLowerArm = 75,
+                lLeg = 75, lLowerLeg = 75,
+                rLeg = 75, rLowerLeg = 75}
+            for key, body in pairs(bodyParts) do
+                if body ~= 0 then
+                    initialMass[key] = GetBodyMass(body)
+                    currentHealth[key] = healthMap[key]
+                    brokenParts[key] = false
+                end
+            end
+
+            for k, v in pairs(cached_struggle_joints) do
+                if type(v) == "table" then
+                    for _, j in ipairs(v) do 
+                        if not IsJointBroken(j) then SetJointMotor(j, 0, 0) end 
+                    end
+                elseif type(v) == "number" and v ~= 0 then
+                    if not IsJointBroken(v) then SetJointMotor(v, 0, 0) end
+                end
+            end
+            
+            ragdollState = STATE_STANDING
+        end
+        
+        for _, body in pairs(bodyParts) do
+            if body ~= 0 then RemoveTag(body, "resurrected") end
+        end
+        isResurrected = false
+    end
+end
+
+local function calculateBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local partWeights = {}
+
+    for key, body in pairs(bodyParts) do
+        if body ~= 0 and initialMass[key] then
+            local currentMass = GetBodyMass(body)
+            local damagePercent = (initialMass[key] - currentMass) / initialMass[key]
+            partDamagePercent[key] = damagePercent
+
+            if (key == "lLowerLeg" or key == "rLowerLeg") and damagePercent > 0.25 then
+                permanentCripple[key] = true
+            end
+
+            if not brokenParts[key] and damagePercent > 0.05 then
+                if key == "head" then
+                    currentHealth[key] = 0
+                    brokenParts[key] = true
+                    permanentDeath = true
+                    eventHeadBroken = true
+                elseif key == "torso" then
+                    currentHealth[key] = currentHealth[key] * 0.5
+                    brokenParts[key] = true
+                    permanentDeath = true
+                    eventTorsoBroken = true
+                end
+            end
+
+            if damagePercent > 0.02 then
+                local initialHealth = (key == "head" and 50 or (key == "torso" and 350 or 75))
+                local healthToDrain = damagePercent * initialHealth * baseMultiplier
+                
+                if currentHealth[key] > 0 then
+                    local actualDrain = math.min(currentHealth[key], healthToDrain)
+                    currentHealth[key] = currentHealth[key] - actualDrain
+                    overflowPool = overflowPool + (healthToDrain - actualDrain)
+                else
+                    overflowPool = overflowPool + healthToDrain
+                end
+            end
+
+            if currentHealth[key] > 0 then
+                local weight = (key == "head") and 0.2 or 1.0
+                partWeights[key] = weight
+                weightSum = weightSum + weight
+            end
+        end
+    end
+
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(partWeights) do
+            currentHealth[key] = math.max(0, currentHealth[key] - (damagePerUnit * weight))
+        end
+    end
+end
+
+local function checkStateMachine()
+    local totalH = 0
+    for _, h in pairs(currentHealth) do totalH = totalH + h end
+    
+    local judgeHealth = totalH
+    if causeOfDeath == "Head Trauma" or causeOfDeath == "Torso Trauma" then
+        judgeHealth = 50 
+    end
+    local isAnyPartBleeding = false
+    for key, percent in pairs(partDamagePercent) do
+        if percent > 0.02 then
+            isAnyPartBleeding = true
+            break
+        end
+    end
+
+    if totalH <= 0 then
+        ragdollState = STATE_DISABLED
+    elseif judgeHealth < 100 then
+        ragdollState = STATE_DEAD
+    elseif judgeHealth < 400 then
+        ragdollState = STATE_CRITICAL
+    elseif judgeHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        ragdollState = STATE_STRUGGLING
+    else
+        ragdollState = STATE_STANDING
+    end
+end
+
+local function handleHeadBurstEffect()
+    local head = bodyParts.head
+    if head ~= 0 then
+        PlaySound(headsplat, GetBodyTransform(head).pos, 1.0)
+        local headTrans = GetBodyTransform(head)
+        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
+    end
+    if causeOfDeath == "none" then
+        causeOfDeath = "Head Trauma"
+    end
+end
+
+local function handleTorsoBurstEffect()
+    local torso = bodyParts.torso
+    if torso ~= 0 then
+        PlaySound(goresplat, GetBodyTransform(torso).pos, 1.0)
+        
+        local torsoTrans = GetBodyTransform(torso)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, 0)))
+
+        if math.random() > 0.3 then 
+            Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) 
+        end
+        if math.random() > 0.5 then 
+            Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) 
+        end
+        if math.random() > 0.4 then 
+            Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) 
+        end
+        if math.random() > 0.5 then 
+            Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) 
+        end
+    end
+    if causeOfDeath == "none" then
+        causeOfDeath = "Torso Trauma"
+    end
+end
+
+local function handleStanding(body, cachedTrans, cachedVel)
+    local legsBroken = permanentCripple.lLowerLeg or permanentCripple.rLowerLeg
+    
+    if body == bodyParts.head and not legsBroken then
+        SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, HEAD_LIFT_VEL, 0)))
+    end
+    
+    if (body == bodyParts.lLowerLeg or body == bodyParts.rLowerLeg) then
+        local key = (body == bodyParts.lLowerLeg) and "lLowerLeg" or "rLowerLeg"
+        if not permanentCripple[key] and (partDamagePercent[key] or 0) < 0.1 then
+            SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, FOOT_PUSH_VEL, 0)))
+        end
+    end
+end
+
+local function handleStruggling()
+    if isSedated then
+        handleCritical()
+        return
+    end
+
+    local head = bodyParts.head
+    if head ~= 0 and criticalcough then
+        PlayLoop(criticalcough, GetBodyTransform(head).pos)
+    end
+    panictim = panictim + 0.01
+    actualpanictim = actualpanictim + 0.01
+    if panictim > 2 and actualpanictim > 0.05 then
+        local roll = math.random(1, 6)
+        if roll <= 5 then rj[roll] = math.random(-sretractjoint, sretractjoint) end
+        actualpanictim = 0
+    end
+    for i=1, #cached_struggle_joints.shoulders do
+        local j = cached_struggle_joints.shoulders[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[1], jointstrength) end
+    end
+    for i=1, #cached_struggle_joints.hips do
+        local j = cached_struggle_joints.hips[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[2], jointstrength) end
+    end
+    for i=1, #cached_struggle_joints.knees do
+        local j = cached_struggle_joints.knees[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[3], jointstrength) end
+    end
+    if cached_struggle_joints.hand1 ~= 0 and not IsJointBroken(cached_struggle_joints.hand1) then
+        SetJointMotor(cached_struggle_joints.hand1, -rj[4], jointstrength)
+    end
+    if cached_struggle_joints.hand2 ~= 0 and not IsJointBroken(cached_struggle_joints.hand2) then
+        SetJointMotor(cached_struggle_joints.hand2, rj[5], jointstrength)
+    end
+end
+
+local function handleCritical()
+    for k, v in pairs(cached_struggle_joints) do
+        if type(v) == "table" then
+            for _, j in ipairs(v) do SetJointMotor(j, 0, 0) end
+        elseif type(v) == "number" and v ~= 0 then
+            SetJointMotor(v, 0, 0)
+        end
+    end
+end
+
+local function handleDead()
+    handleCritical()
+    if causeOfDeath == "none" then
+        causeOfDeath = "Blood Loss" 
+    end
+end
+
+local function handleBleedingParticles(body, intensity, trans)
+    if intensity < 0.1 then return end
+    ParticleType("smoke")
+    local darkRed = 0.15 + (math.random() * 0.1) 
+    ParticleColor(darkRed, 0.0, 0.0)
+    ParticleRadius(0.05, 0.005)
+    ParticleAlpha(1, 0)
+    ParticleGravity(-14)
+    ParticleDrag(0.1)
+    
+    local pos = trans.pos
+    local count = math.min(10, math.floor(intensity * 10))
+    for i=1, count do
+        local vel = Vec(math.random(-10,10)/10, math.random(0,20)/10, math.random(-10,10)/10)
+        SpawnParticle(pos, vel, math.random(5, 15)/10)
+    end
+end
+
+local function handleBleedingPaint(body, trans)
+    if math.random() > 0.5 then return end
+
+    local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+    
+    if hit then
+        local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+        local bloodIntensity = 0.5
+        local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+        PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+        
+        local splashCount = math.random(1, 3)
+        local maxRadius = 0.6
+        
+        for i = 1, splashCount do
+            local angle = math.random() * 2 * math.pi
+            local radius = math.sqrt(math.random()) * maxRadius
+            local offsetX = math.cos(angle) * radius
+            local offsetZ = math.sin(angle) * radius
+            local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+            local splashSize = mainSize * (math.random(3, 5) / 10)
+            PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+        end
+    end
+end
+
+local function handleDrowningLogic()
+    local head = bodyParts.head
+    if head == 0 then return end
+
+    if IsPointInWater(GetBodyTransform(head).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+        
+        if currentOxygen <= 0 then
+            if causeOfDeath == "none" then
+                causeOfDeath = "Drowning"
+            end
+            for key, _ in pairs(currentHealth) do
+                currentHealth[key] = 0
+            end
+            for k, v in pairs(cached_struggle_joints) do
+                if type(v) == "table" then
+                    for _, j in ipairs(v) do SetJointMotor(j, 0, 0) end
+                elseif type(v) == "number" and v ~= 0 then
+                    SetJointMotor(v, 0, 0)
+                end
+            end
+        end
+    else
+        currentOxygen = math.min(MAX_OXYGEN, currentOxygen + 20)
+    end
+end
+
+function server.init()
     local tagMap = {
         head = "Head", torso = "Torso",
         lArm = "LARM", lLowerArm = "LLARM",
@@ -80,342 +412,9 @@
     cached_struggle_joints.hand1 = FindJoint("hand1")
     cached_struggle_joints.hand2 = FindJoint("hand2")
     criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-end
-
-local function checkTags()
-    local resFound = false
-    local bandFound = false
-    local sedFound = false
-    for _, body in pairs(bodyParts) do
-        if body ~= 0 then
-            if HasTag(body, "resurrected") then resFound = true end
-            if HasTag(body, "bandaged") then bandFound = true end
-            if HasTag(body, "sedated") then sedFound = true end
-        end
-    end
-    isResurrected = resFound
-    isBandaged = bandFound
-    isSedated = sedFound
-end
-
-local function handleSpecialStatus()
-    if isBandaged then
-        for key, body in pairs(bodyParts) do
-            if body ~= 0 then
-                initialMass[key] = GetBodyMass(body)
-                RemoveTag(body, "bandaged")
-            end
-        end
-        isBandaged = false
-    end
-
-    if isResurrected then
-        local canBeSaved = (ragdollState ~= STATE_DEAD and ragdollState ~= STATE_DISABLED)
-        
-        if not permanentDeath and canBeSaved then
-            local healthMap = {
-                head = 50, torso = 350,
-                lArm = 75, lLowerArm = 75,
-                rArm = 75, rLowerArm = 75,
-                lLeg = 75, lLowerLeg = 75,
-                rLeg = 75, rLowerLeg = 75}
-            for key, body in pairs(bodyParts) do
-                if body ~= 0 then
-                    initialMass[key] = GetBodyMass(body)
-                    currentHealth[key] = healthMap[key]
-                    brokenParts[key] = false
-                end
-            end
-
-            for k, v in pairs(cached_struggle_joints) do
-                if type(v) == "table" then
-                    for _, j in ipairs(v) do 
-                        if not IsJointBroken(j) then SetJointMotor(j, 0, 0) end 
-                    end
-                elseif type(v) == "number" and v ~= 0 then
-                    if not IsJointBroken(v) then SetJointMotor(v, 0, 0) end
-                end
-            end
-            
-            ragdollState = STATE_STANDING
-        end
-        
-        for _, body in pairs(bodyParts) do
-            if body ~= 0 then RemoveTag(body, "resurrected") end
-        end
-        isResurrected = false
-    end
-end
-
-local function calculateBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local partWeights = {}
-
-    for key, body in pairs(bodyParts) do
-        if body ~= 0 and initialMass[key] then
-            local currentMass = GetBodyMass(body)
-            local damagePercent = (initialMass[key] - currentMass) / initialMass[key]
-            partDamagePercent[key] = damagePercent
-
-            if (key == "lLowerLeg" or key == "rLowerLeg") and damagePercent > 0.25 then
-                permanentCripple[key] = true
-            end
-
-            if not brokenParts[key] and damagePercent > 0.05 then
-                if key == "head" then
-                    currentHealth[key] = 0
-                    brokenParts[key] = true
-                    permanentDeath = true
-                    eventHeadBroken = true
-                elseif key == "torso" then
-                    currentHealth[key] = currentHealth[key] * 0.5
-                    brokenParts[key] = true
-                    permanentDeath = true
-                    eventTorsoBroken = true
-                end
-            end
-
-            if damagePercent > 0.02 then
-                local initialHealth = (key == "head" and 50 or (key == "torso" and 350 or 75))
-                local healthToDrain = damagePercent * initialHealth * baseMultiplier
-                
-                if currentHealth[key] > 0 then
-                    local actualDrain = math.min(currentHealth[key], healthToDrain)
-                    currentHealth[key] = currentHealth[key] - actualDrain
-                    overflowPool = overflowPool + (healthToDrain - actualDrain)
-                else
-                    overflowPool = overflowPool + healthToDrain
-                end
-            end
-
-            if currentHealth[key] > 0 then
-                local weight = (key == "head") and 0.2 or 1.0
-                partWeights[key] = weight
-                weightSum = weightSum + weight
-            end
-        end
-    end
-
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(partWeights) do
-            currentHealth[key] = math.max(0, currentHealth[key] - (damagePerUnit * weight))
-        end
-    end
-end
-
-local function checkStateMachine()
-    local totalH = 0
-    for _, h in pairs(currentHealth) do totalH = totalH + h end
-    
-    local judgeHealth = totalH
-    if causeOfDeath == "Head Trauma" or causeOfDeath == "Torso Trauma" then
-        judgeHealth = 50 
-    end
-    local isAnyPartBleeding = false
-    for key, percent in pairs(partDamagePercent) do
-        if percent > 0.02 then
-            isAnyPartBleeding = true
-            break
-        end
-    end
-
-    if totalH <= 0 then
-        ragdollState = STATE_DISABLED
-    elseif judgeHealth < 100 then
-        ragdollState = STATE_DEAD
-    elseif judgeHealth < 400 then
-        ragdollState = STATE_CRITICAL
-    elseif judgeHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        ragdollState = STATE_STRUGGLING
-    else
-        ragdollState = STATE_STANDING
-    end
-end
-
-local function handleHeadBurstEffect()
-    local head = bodyParts.head
-    if head ~= 0 then
-        PlaySound(headsplat, GetBodyTransform(head).pos, 1.0)
-        local headTrans = GetBodyTransform(head)
-        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
-    end
-    if causeOfDeath == "none" then
-        causeOfDeath = "Head Trauma"
-    end
-end
-
-local function handleTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso ~= 0 then
-        PlaySound(goresplat, GetBodyTransform(torso).pos, 1.0)
-        
-        local torsoTrans = GetBodyTransform(torso)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, 0)))
-
-        if math.random() > 0.3 then 
-            Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) 
-        end
-        if math.random() > 0.5 then 
-            Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) 
-        end
-        if math.random() > 0.4 then 
-            Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) 
-        end
-        if math.random() > 0.5 then 
-            Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) 
-        end
-    end
-    if causeOfDeath == "none" then
-        causeOfDeath = "Torso Trauma"
-    end
-end
-
-local function handleStanding(body, cachedTrans, cachedVel)
-    local legsBroken = permanentCripple.lLowerLeg or permanentCripple.rLowerLeg
-    
-    if body == bodyParts.head and not legsBroken then
-        SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, HEAD_LIFT_VEL, 0)))
-    end
-    
-    if (body == bodyParts.lLowerLeg or body == bodyParts.rLowerLeg) then
-        local key = (body == bodyParts.lLowerLeg) and "lLowerLeg" or "rLowerLeg"
-        if not permanentCripple[key] and (partDamagePercent[key] or 0) < 0.1 then
-            SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, FOOT_PUSH_VEL, 0)))
-        end
-    end
-end
-
-local function handleStruggling()
-    if isSedated then
-        handleCritical()
-        return
-    end
-
-    local head = bodyParts.head
-    if head ~= 0 and criticalcough then
-        PlayLoop(criticalcough, GetBodyTransform(head).pos)
-    end
-    panictim = panictim + 0.01
-    actualpanictim = actualpanictim + 0.01
-    if panictim > 2 and actualpanictim > 0.05 then
-        local roll = math.random(1, 6)
-        if roll <= 5 then rj[roll] = math.random(-sretractjoint, sretractjoint) end
-        actualpanictim = 0
-    end
-    for i=1, #cached_struggle_joints.shoulders do
-        local j = cached_struggle_joints.shoulders[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[1], jointstrength) end
-    end
-    for i=1, #cached_struggle_joints.hips do
-        local j = cached_struggle_joints.hips[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[2], jointstrength) end
-    end
-    for i=1, #cached_struggle_joints.knees do
-        local j = cached_struggle_joints.knees[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[3], jointstrength) end
-    end
-    if cached_struggle_joints.hand1 ~= 0 and not IsJointBroken(cached_struggle_joints.hand1) then
-        SetJointMotor(cached_struggle_joints.hand1, -rj[4], jointstrength)
-    end
-    if cached_struggle_joints.hand2 ~= 0 and not IsJointBroken(cached_struggle_joints.hand2) then
-        SetJointMotor(cached_struggle_joints.hand2, rj[5], jointstrength)
-    end
-end
-
-local function handleCritical()
-    for k, v in pairs(cached_struggle_joints) do
-        if type(v) == "table" then
-            for _, j in ipairs(v) do SetJointMotor(j, 0, 0) end
-        elseif type(v) == "number" and v ~= 0 then
-            SetJointMotor(v, 0, 0)
-        end
-    end
-end
-
-local function handleDead()
-    handleCritical()
-    if causeOfDeath == "none" then
-        causeOfDeath = "Blood Loss" 
-    end
-end
-
-local function handleBleedingParticles(body, intensity, trans)
-    if intensity < 0.1 then return end
-    ParticleType("smoke")
-    local darkRed = 0.15 + (math.random() * 0.1) 
-    ParticleColor(darkRed, 0.0, 0.0)
-    ParticleRadius(0.05, 0.005)
-    ParticleAlpha(1, 0)
-    ParticleGravity(-14)
-    ParticleDrag(0.1)
-    
-    local pos = trans.pos
-    local count = math.min(10, math.floor(intensity * 10))
-    for i=1, count do
-        local vel = Vec(math.random(-10,10)/10, math.random(0,20)/10, math.random(-10,10)/10)
-        SpawnParticle(pos, vel, math.random(5, 15)/10)
-    end
-end
-
-local function handleBleedingPaint(body, trans)
-    if math.random() > 0.5 then return end
-
-    local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-    
-    if hit then
-        local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-        local bloodIntensity = 0.5
-        local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-        PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-        
-        local splashCount = math.random(1, 3)
-        local maxRadius = 0.6
-        
-        for i = 1, splashCount do
-            local angle = math.random() * 2 * math.pi
-            local radius = math.sqrt(math.random()) * maxRadius
-            local offsetX = math.cos(angle) * radius
-            local offsetZ = math.sin(angle) * radius
-            local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-            local splashSize = mainSize * (math.random(3, 5) / 10)
-            PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-        end
-    end
-end
-
-local function handleDrowningLogic()
-    local head = bodyParts.head
-    if head == 0 then return end
-
-    if IsPointInWater(GetBodyTransform(head).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-        
-        if currentOxygen <= 0 then
-            if causeOfDeath == "none" then
-                causeOfDeath = "Drowning"
-            end
-            for key, _ in pairs(currentHealth) do
-                currentHealth[key] = 0
-            end
-            for k, v in pairs(cached_struggle_joints) do
-                if type(v) == "table" then
-                    for _, j in ipairs(v) do SetJointMotor(j, 0, 0) end
-                elseif type(v) == "number" and v ~= 0 then
-                    SetJointMotor(v, 0, 0)
-                end
-            end
-        end
-    else
-        currentOxygen = math.min(MAX_OXYGEN, currentOxygen + 20)
-    end
-end
-
-function update(dt)
+end
+
+function server.update(dt)
     if ragdollState == STATE_DISABLED then return end
 
     checkTimer = checkTimer + dt
@@ -466,12 +465,17 @@
     end
 end
 
-function draw(dt)
+function client.init()
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+
+function client.draw()
     if ragdollState == STATE_DISABLED then return end
 
-    local cam = GetPlayerCameraTransform()
+    local cam = GetPlayerCameraTransform(playerId)
     local hit, dist, norm, shape = QueryRaycast(cam.pos, TransformToParentVec(cam, Vec(0, 0, -1)), 5.0)
-    
+
     local isLookingAtMe = false
     if hit and shape ~= 0 then
         local hitBody = GetShapeBody(shape)
@@ -551,7 +555,7 @@
         UiTranslate(0, 20)
         UiColor(1, 1, 1, 0.8)
         UiText(string.format("TAGS: RES:%s BND:%s", tostring(isResurrected), tostring(isBandaged)))
-        
+
         UiTranslate(0, 25)
         for key, data in pairs(bodyState.parts) do
             UiPush()
@@ -561,7 +565,7 @@
                 UiTranslate(25, 12)
                 UiColor(1, 1, 1, 1)
                 UiFont("regular.ttf", 16)
-                
+
                 local displayText = data.name .. ": " .. math.floor(h)
                 if permanentCripple and permanentCripple[key] then
                     displayText = displayText .. " [CRIPPLED]"
@@ -576,7 +580,7 @@
         UiFont("bold.ttf", 18)
         UiColor(1, 1, 1, 1)
         UiText("Total Blood: " .. math.floor(totalH))
-        
+
         if permanentDeath then
             UiTranslate(0, 25)
             UiColor(1, 0, 0, 1)
@@ -584,4 +588,5 @@
             UiText("FATAL DAMAGE - NO RES")
         end
     UiPop()
-end+end
+

```

---

# Migration Report: lua\gore v25.12.25.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v25.12.25.lua
+++ patched/lua\gore v25.12.25.lua
@@ -1,60 +1,330 @@
-cached_struggle_joints = {
-    knees = {},
-    hips = {},
-    shoulders = {},
-    hand1 = 0,
-    hand2 = 0}
-bodyState = {
-    parts = {
-        head = { color = GREEN, name = "Head", type = "head" },
-        torso = { color = GREEN, name = "Torso", type = "torso" },
-        lArm = { color = GREEN, name = "L Arm", type = "limb" },
-        lLowerArm = { color = GREEN, name = "L L-Arm", type = "limb" },
-        rArm = { color = GREEN, name = "R Arm", type = "limb" },
-        rLowerArm = { color = GREEN, name = "R L-Arm", type = "limb" },
-        lLeg = { color = GREEN, name = "L Leg", type = "limb" },
-        lLowerLeg = { color = GREEN, name = "L L-Leg", type = "limb" },
-        rLeg = { color = GREEN, name = "R Leg", type = "limb" },
-        rLowerLeg = { color = GREEN, name = "R L-Leg", type = "limb" }}}
-permanentCripple = {
-    lLowerLeg = false,
-    rLowerLeg = false}
-bodyParts = {}
-initialMass = {}
-currentHealth = {}
-brokenParts = {}
-STATE_STANDING = "STANDING"
-STATE_STRUGGLING = "STRUGGLING"
-STATE_CRITICAL = "CRITICAL"
-STATE_DEAD = "DEAD"
-STATE_DISABLED = "DISABLED"
-ragdollState = STATE_STANDING
-causeOfDeath = nil
-permanentDeath = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-checkTimer = 0
-criticalcough = nil
-goresplat = nil
-headsplat = nil
-GREEN = {r=0, g=1, b=0}
-RED   = {r=1, g=0, b=0}
-HEAD_LIFT_VEL = 0.5
-FOOT_PUSH_VEL = -2.0
-sretractjoint = 12
-jointstrength = 3
-rj = {12, 12, 12, 12, 12}
-panictim = 0
-actualpanictim = 0
-eventHeadBroken = false
-eventTorsoBroken = false
-partDamagePercent = {}
-currentOxygen = 100
-MAX_OXYGEN = 100
-bandagedParts = {}
-
-function init()
+#version 2
+function checkTags()
+    local resFound = false
+    local bandFound = false
+    local sedFound = false
+    for _, body in pairs(bodyParts) do
+        if body ~= 0 then
+            if HasTag(body, "resurrected") then resFound = true end
+            if HasTag(body, "bandaged") then bandFound = true end
+            if HasTag(body, "sedated") then sedFound = true end
+        end
+    end
+    isResurrected = resFound
+    isBandaged = bandFound
+    isSedated = sedFound
+end
+
+function handleSpecialStatus()
+    if isBandaged then
+        for key, body in pairs(bodyParts) do
+            if body ~= 0 then
+                initialMass[key] = GetBodyMass(body)
+                if (partDamagePercent[key] or 0) > 0.02 then
+                    bandagedParts[key] = true
+                end
+                RemoveTag(body, "bandaged")
+            end
+        end
+        isBandaged = false
+    end
+
+    if isResurrected then
+        local canBeSaved = (ragdollState ~= STATE_DEAD and ragdollState ~= STATE_DISABLED)
+
+        if not permanentDeath and canBeSaved then
+            local healthMap = {
+                head = 50, torso = 350,
+                lArm = 75, lLowerArm = 75,
+                rArm = 75, rLowerArm = 75,
+                lLeg = 75, lLowerLeg = 75,
+                rLeg = 75, rLowerLeg = 75
+            }
+            for key, body in pairs(bodyParts) do
+                if body ~= 0 then
+                    initialMass[key] = GetBodyMass(body)
+                    currentHealth[key] = healthMap[key]
+                    brokenParts[key] = false
+                end
+            end
+            ragdollState = STATE_STANDING
+        end
+
+        for _, body in pairs(bodyParts) do
+            if body ~= 0 then RemoveTag(body, "resurrected") end
+        end
+        isResurrected = false
+    end
+end
+
+function calculateBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local partWeights = {}
+
+    for key, body in pairs(bodyParts) do
+        if body ~= 0 and initialMass[key] then
+            local currentMass = GetBodyMass(body)
+            local damagePercent = (initialMass[key] - currentMass) / initialMass[key]
+            if bandagedParts[key] and damagePercent > 0.01 then
+                bandagedParts[key] = nil
+            end
+            partDamagePercent[key] = damagePercent
+
+            if (key == "lLowerLeg" or key == "rLowerLeg") and damagePercent > 0.25 then permanentCripple[key] = true end
+
+            if not brokenParts[key] and damagePercent > 0.05 then
+                if key == "head" then
+                    currentHealth[key] = 0
+                    brokenParts[key] = true
+                    permanentDeath = true
+                    eventHeadBroken = true
+                elseif key == "torso" then
+                    currentHealth[key] = currentHealth[key] * 0.5
+                    brokenParts[key] = true
+                    permanentDeath = true
+                    eventTorsoBroken = true
+                end
+            end
+
+            if damagePercent > 0.02 then
+                local initialHealth = (key == "head" and 50 or (key == "torso" and 350 or 75))
+                local healthToDrain = damagePercent * initialHealth * baseMultiplier
+
+                if currentHealth[key] > 0 then
+                    local actualDrain = math.min(currentHealth[key], healthToDrain)
+                    currentHealth[key] = currentHealth[key] - actualDrain
+                    overflowPool = overflowPool + (healthToDrain - actualDrain)
+                else
+                    overflowPool = overflowPool + healthToDrain
+                end
+            end
+
+            if currentHealth[key] > 0 then
+                local weight = (key == "head") and 0.2 or 1.0
+                partWeights[key] = weight
+                weightSum = weightSum + weight
+            end
+        end
+    end
+
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(partWeights) do currentHealth[key] = math.max(0, currentHealth[key] - (damagePerUnit * weight)) end
+    end
+end
+
+function checkStateMachine()
+    local totalH = 0
+    
+    for _, h in pairs(currentHealth) do totalH = totalH + h end
+
+    local judgeHealth = totalH
+    if causeOfDeath == "Head Trauma" or causeOfDeath == "Torso Trauma" then judgeHealth = 50 end
+    local isAnyPartBleeding = false
+    for key, percent in pairs(partDamagePercent) do
+        if percent > 0.02 then isAnyPartBleeding = true break end
+    end
+
+    if totalH <= 0 then
+        ragdollState = STATE_DISABLED
+        syncDataToRegistry(true)
+    elseif judgeHealth < 100 then
+        ragdollState = STATE_DEAD
+    elseif judgeHealth < 400 then
+        ragdollState = STATE_CRITICAL
+    elseif judgeHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        ragdollState = STATE_STRUGGLING
+    else
+        ragdollState = STATE_STANDING
+    end
+end
+
+function handleHeadBurstEffect()
+    local head = bodyParts.head
+    if head ~= 0 then
+        PlaySound(headsplat, GetBodyTransform(head).pos, 1.0)
+        local headTrans = GetBodyTransform(head)
+        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
+    end
+    causeOfDeath = causeOfDeath and causeOfDeath or "Head Trauma"
+end
+
+function handleTorsoBurstEffect()
+    local torso = bodyParts.torso
+    if torso ~= 0 then
+        PlaySound(goresplat, GetBodyTransform(torso).pos, 1.0)
+
+        local torsoTrans = GetBodyTransform(torso)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+
+        if math.random() > 0.3 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
+        if math.random() > 0.4 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
+    end
+    causeOfDeath = causeOfDeath and causeOfDeath or "Torso Trauma"
+end
+
+function handleStanding(body, cachedTrans, cachedVel)
+    local legsBroken = permanentCripple.lLowerLeg or permanentCripple.rLowerLeg
+    if body == bodyParts.head and not legsBroken then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, HEAD_LIFT_VEL, 0))) end
+    if (body == bodyParts.lLowerLeg or body == bodyParts.rLowerLeg) then
+        local key = (body == bodyParts.lLowerLeg) and "lLowerLeg" or "rLowerLeg"
+        if not permanentCripple[key] and (partDamagePercent[key] or 0) < 0.1 then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, FOOT_PUSH_VEL, 0))) end
+    end
+end
+
+function handleStruggling()
+    if isSedated then handleCritical() return end
+
+    local head = bodyParts.head
+    if head ~= 0 and criticalcough then PlayLoop(criticalcough, GetBodyTransform(head).pos) end
+    panictim = panictim + 0.01
+    actualpanictim = actualpanictim + 0.01
+    if panictim > 2 and actualpanictim > 0.05 then
+        local roll = math.random(1, 6)
+        if roll <= 5 then rj[roll] = math.random(-sretractjoint, sretractjoint) end
+        actualpanictim = 0
+    end
+    for i=1, #cached_struggle_joints.shoulders do
+        local j = cached_struggle_joints.shoulders[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[1], jointstrength) end
+    end
+    for i=1, #cached_struggle_joints.hips do
+        local j = cached_struggle_joints.hips[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[2], jointstrength) end
+    end
+    for i=1, #cached_struggle_joints.knees do
+        local j = cached_struggle_joints.knees[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[3], jointstrength) end
+    end
+    if cached_struggle_joints.hand1 ~= 0 and not IsJointBroken(cached_struggle_joints.hand1) then SetJointMotor(cached_struggle_joints.hand1, -rj[4], jointstrength) end
+    if cached_struggle_joints.hand2 ~= 0 and not IsJointBroken(cached_struggle_joints.hand2) then SetJointMotor(cached_struggle_joints.hand2, rj[5], jointstrength) end
+end
+
+function handleCritical()
+    --GLanDoSS & Yulun & Gemini3 made this mod
+end
+
+function handleDead()
+    if causeOfDeath ~= nil and causeOfDeath ~= "Blood Loss" then 
+        return 
+    end
+
+    if currentOxygen <= 0 then
+        causeOfDeath = "Drowned"
+    else
+        causeOfDeath = causeOfDeath or "Blood Loss"
+    end
+end
+
+function handleBleedingParticles(body, intensity, trans)
+    if intensity < 0.1 then return end
+    ParticleType("smoke")
+    local darkRed = 0.15 + (math.random() * 0.1)
+    ParticleColor(darkRed, 0.0, 0.0)
+    ParticleRadius(0.05, 0.005)
+    ParticleAlpha(1, 0)
+    ParticleGravity(-14)
+    ParticleDrag(0.1)
+
+    local pos = trans.pos
+    local count = math.min(10, math.floor(intensity * 10))
+    for i=1, count do
+        local vel = Vec(math.random(-10,10)/10, math.random(0,20)/10, math.random(-10,10)/10)
+        SpawnParticle(pos, vel, math.random(5, 15)/10)
+    end
+end
+
+function handleBleedingPaint(body, trans)
+    local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+
+    if hit then
+        local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+        local bloodIntensity = 0.5
+        local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+        PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+
+        local splashCount = math.random(3, 6)
+        local maxRadius = 0.7
+
+        for i = 1, splashCount do
+            local angle = math.random() * 2 * math.pi
+            local radius = math.sqrt(math.random()) * maxRadius
+            local offsetX = math.cos(angle) * radius
+            local offsetZ = math.sin(angle) * radius
+            local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+            local splashSize = mainSize * (math.random(3, 5) / 10)
+            PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+        end
+    end
+end
+
+function handleDrowningLogic()
+    local head = bodyParts.head
+    if head == 0 then return end
+
+    if IsPointInWater(GetBodyTransform(head).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+
+        if currentOxygen <= 0 then
+            for key, _ in pairs(currentHealth) do
+                currentHealth[key] = math.max(0, currentHealth[key] - 30)
+            end
+        end
+    else
+        currentOxygen = math.min(MAX_OXYGEN, currentOxygen + 20)
+    end
+end
+
+function syncDataToRegistry(finalStatus)
+    if not bodyParts or not bodyParts.torso or bodyParts.torso == 0 then return end
+
+    local dollId = tostring(bodyParts.torso)
+    local path = "temp.goredolls."..dollId
+
+    SetString(path..".state", ragdollState or "UNKNOWN", true)
+    SetString(path..".cause", causeOfDeath or "none", true)
+    SetFloat(path..".oxy", currentOxygen or 100, true)
+    SetBool(path..".sedated", isSedated == true, true)
+    SetString(path..".bandages", table.fullConcat(bandagedParts, ",", true, true, ":"), true)
+    SetFloat(path..".update", GetFloat("temp.goredollsClock"), true)
+    SetString(path..".healths", table.fullConcat(currentHealth, ",", true, true, ":"), true)
+    SetString(path..".cripples", table.fullConcat(permanentCripple, ",", true, true, ":"), true)
+    SetString(path..".bodies", table.fullConcat(bodyParts, ",", true), true)
+    if finalStatus then SetBool(path..".final", true, true) end
+end
+
+function table.fullConcat(table, separator, ignoreNil, includeKey, keySeparator)
+    local tempStr = ""
+    for key, value in pairs(table) do
+        if (ignoreNil and type(value) ~= "nil") or not ignoreNil then
+            if not includeKey then
+                tempStr = tempStr..tostring(value)..(next(table, key) and separator or "")
+            else
+                tempStr = tempStr..tostring(key)..(keySeparator and keySeparator or "")..tostring(value)..(next(table, key) and separator or "")
+            end
+        end
+    end
+    return tempStr
+end
+
+function resetJointMotors()
+    for _, v in pairs(cached_struggle_joints) do
+        if type(v) == "table" then
+            for i = 1, #v do
+                local j = v[i]
+                if not IsJointBroken(j) then SetJointMotor(j, 0, 0) end
+            end
+        elseif type(v) == "number" and v ~= 0 then
+            if not IsJointBroken(v) then SetJointMotor(v, 0, 0) end
+        end
+    end
+end
+
+function server.init()
     local tagMap = {
         head = "Head", torso = "Torso",
         lArm = "LARM", lLowerArm = "LLARM",
@@ -86,336 +356,9 @@
     cached_struggle_joints.hand1 = FindJoint("hand1")
     cached_struggle_joints.hand2 = FindJoint("hand2")
     criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-end
-
-function checkTags()
-    local resFound = false
-    local bandFound = false
-    local sedFound = false
-    for _, body in pairs(bodyParts) do
-        if body ~= 0 then
-            if HasTag(body, "resurrected") then resFound = true end
-            if HasTag(body, "bandaged") then bandFound = true end
-            if HasTag(body, "sedated") then sedFound = true end
-        end
-    end
-    isResurrected = resFound
-    isBandaged = bandFound
-    isSedated = sedFound
-end
-
-function handleSpecialStatus()
-    if isBandaged then
-        for key, body in pairs(bodyParts) do
-            if body ~= 0 then
-                initialMass[key] = GetBodyMass(body)
-                if (partDamagePercent[key] or 0) > 0.02 then
-                    bandagedParts[key] = true
-                end
-                RemoveTag(body, "bandaged")
-            end
-        end
-        isBandaged = false
-    end
-
-    if isResurrected then
-        local canBeSaved = (ragdollState ~= STATE_DEAD and ragdollState ~= STATE_DISABLED)
-
-        if not permanentDeath and canBeSaved then
-            local healthMap = {
-                head = 50, torso = 350,
-                lArm = 75, lLowerArm = 75,
-                rArm = 75, rLowerArm = 75,
-                lLeg = 75, lLowerLeg = 75,
-                rLeg = 75, rLowerLeg = 75
-            }
-            for key, body in pairs(bodyParts) do
-                if body ~= 0 then
-                    initialMass[key] = GetBodyMass(body)
-                    currentHealth[key] = healthMap[key]
-                    brokenParts[key] = false
-                end
-            end
-            ragdollState = STATE_STANDING
-        end
-
-        for _, body in pairs(bodyParts) do
-            if body ~= 0 then RemoveTag(body, "resurrected") end
-        end
-        isResurrected = false
-    end
-end
-
-function calculateBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local partWeights = {}
-
-    for key, body in pairs(bodyParts) do
-        if body ~= 0 and initialMass[key] then
-            local currentMass = GetBodyMass(body)
-            local damagePercent = (initialMass[key] - currentMass) / initialMass[key]
-            if bandagedParts[key] and damagePercent > 0.01 then
-                bandagedParts[key] = nil
-            end
-            partDamagePercent[key] = damagePercent
-
-            if (key == "lLowerLeg" or key == "rLowerLeg") and damagePercent > 0.25 then permanentCripple[key] = true end
-
-            if not brokenParts[key] and damagePercent > 0.05 then
-                if key == "head" then
-                    currentHealth[key] = 0
-                    brokenParts[key] = true
-                    permanentDeath = true
-                    eventHeadBroken = true
-                elseif key == "torso" then
-                    currentHealth[key] = currentHealth[key] * 0.5
-                    brokenParts[key] = true
-                    permanentDeath = true
-                    eventTorsoBroken = true
-                end
-            end
-
-            if damagePercent > 0.02 then
-                local initialHealth = (key == "head" and 50 or (key == "torso" and 350 or 75))
-                local healthToDrain = damagePercent * initialHealth * baseMultiplier
-
-                if currentHealth[key] > 0 then
-                    local actualDrain = math.min(currentHealth[key], healthToDrain)
-                    currentHealth[key] = currentHealth[key] - actualDrain
-                    overflowPool = overflowPool + (healthToDrain - actualDrain)
-                else
-                    overflowPool = overflowPool + healthToDrain
-                end
-            end
-
-            if currentHealth[key] > 0 then
-                local weight = (key == "head") and 0.2 or 1.0
-                partWeights[key] = weight
-                weightSum = weightSum + weight
-            end
-        end
-    end
-
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(partWeights) do currentHealth[key] = math.max(0, currentHealth[key] - (damagePerUnit * weight)) end
-    end
-end
-
-function checkStateMachine()
-    local totalH = 0
-    
-    for _, h in pairs(currentHealth) do totalH = totalH + h end
-
-    local judgeHealth = totalH
-    if causeOfDeath == "Head Trauma" or causeOfDeath == "Torso Trauma" then judgeHealth = 50 end
-    local isAnyPartBleeding = false
-    for key, percent in pairs(partDamagePercent) do
-        if percent > 0.02 then isAnyPartBleeding = true break end
-    end
-
-    if totalH <= 0 then
-        ragdollState = STATE_DISABLED
-        syncDataToRegistry(true)
-    elseif judgeHealth < 100 then
-        ragdollState = STATE_DEAD
-    elseif judgeHealth < 400 then
-        ragdollState = STATE_CRITICAL
-    elseif judgeHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        ragdollState = STATE_STRUGGLING
-    else
-        ragdollState = STATE_STANDING
-    end
-end
-
-function handleHeadBurstEffect()
-    local head = bodyParts.head
-    if head ~= 0 then
-        PlaySound(headsplat, GetBodyTransform(head).pos, 1.0)
-        local headTrans = GetBodyTransform(head)
-        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
-    end
-    causeOfDeath = causeOfDeath and causeOfDeath or "Head Trauma"
-end
-
-function handleTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso ~= 0 then
-        PlaySound(goresplat, GetBodyTransform(torso).pos, 1.0)
-
-        local torsoTrans = GetBodyTransform(torso)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-
-        if math.random() > 0.3 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
-        if math.random() > 0.4 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
-    end
-    causeOfDeath = causeOfDeath and causeOfDeath or "Torso Trauma"
-end
-
-function handleStanding(body, cachedTrans, cachedVel)
-    local legsBroken = permanentCripple.lLowerLeg or permanentCripple.rLowerLeg
-    if body == bodyParts.head and not legsBroken then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, HEAD_LIFT_VEL, 0))) end
-    if (body == bodyParts.lLowerLeg or body == bodyParts.rLowerLeg) then
-        local key = (body == bodyParts.lLowerLeg) and "lLowerLeg" or "rLowerLeg"
-        if not permanentCripple[key] and (partDamagePercent[key] or 0) < 0.1 then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, FOOT_PUSH_VEL, 0))) end
-    end
-end
-
-function handleStruggling()
-    if isSedated then handleCritical() return end
-
-    local head = bodyParts.head
-    if head ~= 0 and criticalcough then PlayLoop(criticalcough, GetBodyTransform(head).pos) end
-    panictim = panictim + 0.01
-    actualpanictim = actualpanictim + 0.01
-    if panictim > 2 and actualpanictim > 0.05 then
-        local roll = math.random(1, 6)
-        if roll <= 5 then rj[roll] = math.random(-sretractjoint, sretractjoint) end
-        actualpanictim = 0
-    end
-    for i=1, #cached_struggle_joints.shoulders do
-        local j = cached_struggle_joints.shoulders[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[1], jointstrength) end
-    end
-    for i=1, #cached_struggle_joints.hips do
-        local j = cached_struggle_joints.hips[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[2], jointstrength) end
-    end
-    for i=1, #cached_struggle_joints.knees do
-        local j = cached_struggle_joints.knees[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[3], jointstrength) end
-    end
-    if cached_struggle_joints.hand1 ~= 0 and not IsJointBroken(cached_struggle_joints.hand1) then SetJointMotor(cached_struggle_joints.hand1, -rj[4], jointstrength) end
-    if cached_struggle_joints.hand2 ~= 0 and not IsJointBroken(cached_struggle_joints.hand2) then SetJointMotor(cached_struggle_joints.hand2, rj[5], jointstrength) end
-end
-
-function handleCritical()
-    --GLanDoSS & Yulun & Gemini3 made this mod
-end
-
-function handleDead()
-    if causeOfDeath ~= nil and causeOfDeath ~= "Blood Loss" then 
-        return 
-    end
-
-    if currentOxygen <= 0 then
-        causeOfDeath = "Drowned"
-    else
-        causeOfDeath = causeOfDeath or "Blood Loss"
-    end
-end
-
-function handleBleedingParticles(body, intensity, trans)
-    if intensity < 0.1 then return end
-    ParticleType("smoke")
-    local darkRed = 0.15 + (math.random() * 0.1)
-    ParticleColor(darkRed, 0.0, 0.0)
-    ParticleRadius(0.05, 0.005)
-    ParticleAlpha(1, 0)
-    ParticleGravity(-14)
-    ParticleDrag(0.1)
-
-    local pos = trans.pos
-    local count = math.min(10, math.floor(intensity * 10))
-    for i=1, count do
-        local vel = Vec(math.random(-10,10)/10, math.random(0,20)/10, math.random(-10,10)/10)
-        SpawnParticle(pos, vel, math.random(5, 15)/10)
-    end
-end
-
-function handleBleedingPaint(body, trans)
-    local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-
-    if hit then
-        local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-        local bloodIntensity = 0.5
-        local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-        PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-
-        local splashCount = math.random(3, 6)
-        local maxRadius = 0.7
-
-        for i = 1, splashCount do
-            local angle = math.random() * 2 * math.pi
-            local radius = math.sqrt(math.random()) * maxRadius
-            local offsetX = math.cos(angle) * radius
-            local offsetZ = math.sin(angle) * radius
-            local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-            local splashSize = mainSize * (math.random(3, 5) / 10)
-            PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-        end
-    end
-end
-
-function handleDrowningLogic()
-    local head = bodyParts.head
-    if head == 0 then return end
-
-    if IsPointInWater(GetBodyTransform(head).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-
-        if currentOxygen <= 0 then
-            for key, _ in pairs(currentHealth) do
-                currentHealth[key] = math.max(0, currentHealth[key] - 30)
-            end
-        end
-    else
-        currentOxygen = math.min(MAX_OXYGEN, currentOxygen + 20)
-    end
-end
-
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso == 0 then return end
-
-    local dollId = tostring(bodyParts.torso)
-    local path = "temp.goredolls."..dollId
-
-    SetString(path..".state", ragdollState or "UNKNOWN")
-    SetString(path..".cause", causeOfDeath or "none")
-    SetFloat(path..".oxy", currentOxygen or 100)
-    SetBool(path..".sedated", isSedated == true)
-    SetString(path..".bandages", table.fullConcat(bandagedParts, ",", true, true, ":"))
-    SetFloat(path..".update", GetFloat("temp.goredollsClock"))
-    SetString(path..".healths", table.fullConcat(currentHealth, ",", true, true, ":"))
-    SetString(path..".cripples", table.fullConcat(permanentCripple, ",", true, true, ":"))
-    SetString(path..".bodies", table.fullConcat(bodyParts, ",", true))
-    if finalStatus then SetBool(path..".final", true) end
-end
-
-function table.fullConcat(table, separator, ignoreNil, includeKey, keySeparator)
-    local tempStr = ""
-    for key, value in pairs(table) do
-        if (ignoreNil and type(value) ~= "nil") or not ignoreNil then
-            if not includeKey then
-                tempStr = tempStr..tostring(value)..(next(table, key) and separator or "")
-            else
-                tempStr = tempStr..tostring(key)..(keySeparator and keySeparator or "")..tostring(value)..(next(table, key) and separator or "")
-            end
-        end
-    end
-    return tempStr
-end
-
-function resetJointMotors()
-    for _, v in pairs(cached_struggle_joints) do
-        if type(v) == "table" then
-            for i = 1, #v do
-                local j = v[i]
-                if not IsJointBroken(j) then SetJointMotor(j, 0, 0) end
-            end
-        elseif type(v) == "number" and v ~= 0 then
-            if not IsJointBroken(v) then SetJointMotor(v, 0, 0) end
-        end
-    end
-end
-
-function update(dt)
+end
+
+function server.update(dt)
     if ragdollState == STATE_DISABLED then return end
 
     checkTimer = checkTimer + dt
@@ -468,3 +411,9 @@
     handleDead()
     end
 end
+
+function client.init()
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+

```

---

# Migration Report: lua\gore v25.12.31.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v25.12.31.lua
+++ patched/lua\gore v25.12.31.lua
@@ -1,60 +1,330 @@
-cached_struggle_joints = {
-    knees = {},
-    hips = {},
-    shoulders = {},
-    hand1 = 0,
-    hand2 = 0}
-bodyState = {
-    parts = {
-        head = { color = GREEN, name = "Head", type = "head" },
-        torso = { color = GREEN, name = "Torso", type = "torso" },
-        lArm = { color = GREEN, name = "L Arm", type = "limb" },
-        lLowerArm = { color = GREEN, name = "L L-Arm", type = "limb" },
-        rArm = { color = GREEN, name = "R Arm", type = "limb" },
-        rLowerArm = { color = GREEN, name = "R L-Arm", type = "limb" },
-        lLeg = { color = GREEN, name = "L Leg", type = "limb" },
-        lLowerLeg = { color = GREEN, name = "L L-Leg", type = "limb" },
-        rLeg = { color = GREEN, name = "R Leg", type = "limb" },
-        rLowerLeg = { color = GREEN, name = "R L-Leg", type = "limb" }}}
-permanentCripple = {
-    lLowerLeg = false,
-    rLowerLeg = false}
-bodyParts = {}
-initialMass = {}
-currentHealth = {}
-brokenParts = {}
-STATE_STANDING = "STANDING"
-STATE_STRUGGLING = "STRUGGLING"
-STATE_CRITICAL = "CRITICAL"
-STATE_DEAD = "DEAD"
-STATE_DISABLED = "DISABLED"
-ragdollState = STATE_STANDING
-causeOfDeath = nil
-permanentDeath = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-checkTimer = 0
-criticalcough = nil
-goresplat = nil
-headsplat = nil
-GREEN = {r=0, g=1, b=0}
-RED   = {r=1, g=0, b=0}
-HEAD_LIFT_VEL = 0.5
-FOOT_PUSH_VEL = -2.0
-sretractjoint = 12
-jointstrength = 3
-rj = {12, 12, 12, 12, 12}
-panictim = 0
-actualpanictim = 0
-eventHeadBroken = false
-eventTorsoBroken = false
-partDamagePercent = {}
-currentOxygen = 100
-MAX_OXYGEN = 100
-bandagedParts = {}
-
-function init()
+#version 2
+function checkTags()
+    local resFound = false
+    local bandFound = false
+    local sedFound = false
+    for _, body in pairs(bodyParts) do
+        if body ~= 0 then
+            if HasTag(body, "resurrected") then resFound = true end
+            if HasTag(body, "bandaged") then bandFound = true end
+            if HasTag(body, "sedated") then sedFound = true end
+        end
+    end
+    isResurrected = resFound
+    isBandaged = bandFound
+    isSedated = sedFound
+end
+
+function handleSpecialStatus()
+    if isBandaged then
+        for key, body in pairs(bodyParts) do
+            if body ~= 0 then
+                initialMass[key] = GetBodyMass(body)
+                if (partDamagePercent[key] or 0) > 0.02 then
+                    bandagedParts[key] = true
+                end
+                RemoveTag(body, "bandaged")
+            end
+        end
+        isBandaged = false
+    end
+
+    if isResurrected then
+        local canBeSaved = (ragdollState ~= STATE_DEAD and ragdollState ~= STATE_DISABLED)
+
+        if not permanentDeath and canBeSaved then
+            local healthMap = {
+                head = 50, torso = 350,
+                lArm = 75, lLowerArm = 75,
+                rArm = 75, rLowerArm = 75,
+                lLeg = 75, lLowerLeg = 75,
+                rLeg = 75, rLowerLeg = 75
+            }
+            for key, body in pairs(bodyParts) do
+                if body ~= 0 then
+                    initialMass[key] = GetBodyMass(body)
+                    currentHealth[key] = healthMap[key]
+                    brokenParts[key] = false
+                end
+            end
+            ragdollState = STATE_STANDING
+        end
+
+        for _, body in pairs(bodyParts) do
+            if body ~= 0 then RemoveTag(body, "resurrected") end
+        end
+        isResurrected = false
+    end
+end
+
+function calculateBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local partWeights = {}
+
+    for key, body in pairs(bodyParts) do
+        if body ~= 0 and initialMass[key] then
+            local currentMass = GetBodyMass(body)
+            local damagePercent = (initialMass[key] - currentMass) / initialMass[key]
+            if bandagedParts[key] and damagePercent > 0.01 then
+                bandagedParts[key] = nil
+            end
+            partDamagePercent[key] = damagePercent
+
+            if (key == "lLowerLeg" or key == "rLowerLeg") and damagePercent > 0.25 then permanentCripple[key] = true end
+
+            if not brokenParts[key] and damagePercent > 0.1 then
+                if key == "head" then
+                    currentHealth[key] = 0
+                    brokenParts[key] = true
+                    permanentDeath = true
+                    eventHeadBroken = true
+                elseif key == "torso" then
+                    currentHealth[key] = currentHealth[key] * 0.5
+                    brokenParts[key] = true
+                    permanentDeath = true
+                    eventTorsoBroken = true
+                end
+            end
+
+            if damagePercent > 0.02 then
+                local initialHealth = (key == "head" and 50 or (key == "torso" and 350 or 75))
+                local healthToDrain = damagePercent * initialHealth * baseMultiplier
+
+                if currentHealth[key] > 0 then
+                    local actualDrain = math.min(currentHealth[key], healthToDrain)
+                    currentHealth[key] = currentHealth[key] - actualDrain
+                    overflowPool = overflowPool + (healthToDrain - actualDrain)
+                else
+                    overflowPool = overflowPool + healthToDrain
+                end
+            end
+
+            if currentHealth[key] > 0 then
+                local weight = (key == "head") and 0.2 or 1.0
+                partWeights[key] = weight
+                weightSum = weightSum + weight
+            end
+        end
+    end
+
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(partWeights) do currentHealth[key] = math.max(0, currentHealth[key] - (damagePerUnit * weight)) end
+    end
+end
+
+function checkStateMachine()
+    local totalH = 0
+    
+    for _, h in pairs(currentHealth) do totalH = totalH + h end
+
+    local judgeHealth = totalH
+    if causeOfDeath == "Head Trauma" or causeOfDeath == "Torso Trauma" then judgeHealth = 50 end
+    local isAnyPartBleeding = false
+    for key, percent in pairs(partDamagePercent) do
+        if percent > 0.02 then isAnyPartBleeding = true break end
+    end
+
+    if totalH <= 0 then
+        ragdollState = STATE_DISABLED
+        syncDataToRegistry(true)
+    elseif judgeHealth < 100 then
+        ragdollState = STATE_DEAD
+    elseif judgeHealth < 400 then
+        ragdollState = STATE_CRITICAL
+    elseif judgeHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        ragdollState = STATE_STRUGGLING
+    else
+        ragdollState = STATE_STANDING
+    end
+end
+
+function handleHeadBurstEffect()
+    local head = bodyParts.head
+    if head ~= 0 then
+        PlaySound(headsplat, GetBodyTransform(head).pos, 1.0)
+        local headTrans = GetBodyTransform(head)
+        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
+    end
+    causeOfDeath = causeOfDeath and causeOfDeath or "Head Trauma"
+end
+
+function handleTorsoBurstEffect()
+    local torso = bodyParts.torso
+    if torso ~= 0 then
+        PlaySound(goresplat, GetBodyTransform(torso).pos, 1.0)
+
+        local torsoTrans = GetBodyTransform(torso)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+
+        if math.random() > 0.3 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
+        if math.random() > 0.4 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
+    end
+    causeOfDeath = causeOfDeath and causeOfDeath or "Torso Trauma"
+end
+
+function handleStanding(body, cachedTrans, cachedVel)
+    local legsBroken = permanentCripple.lLowerLeg or permanentCripple.rLowerLeg
+    if body == bodyParts.head and not legsBroken then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, HEAD_LIFT_VEL, 0))) end
+    if (body == bodyParts.lLowerLeg or body == bodyParts.rLowerLeg) then
+        local key = (body == bodyParts.lLowerLeg) and "lLowerLeg" or "rLowerLeg"
+        if not permanentCripple[key] and (partDamagePercent[key] or 0) < 0.1 then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, FOOT_PUSH_VEL, 0))) end
+    end
+end
+
+function handleStruggling()
+    if isSedated then handleCritical() return end
+
+    local head = bodyParts.head
+    if head ~= 0 and criticalcough then PlayLoop(criticalcough, GetBodyTransform(head).pos) end
+    panictim = panictim + 0.01
+    actualpanictim = actualpanictim + 0.01
+    if panictim > 2 and actualpanictim > 0.05 then
+        local roll = math.random(1, 6)
+        if roll <= 5 then rj[roll] = math.random(-sretractjoint, sretractjoint) end
+        actualpanictim = 0
+    end
+    for i=1, #cached_struggle_joints.shoulders do
+        local j = cached_struggle_joints.shoulders[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[1], jointstrength) end
+    end
+    for i=1, #cached_struggle_joints.hips do
+        local j = cached_struggle_joints.hips[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[2], jointstrength) end
+    end
+    for i=1, #cached_struggle_joints.knees do
+        local j = cached_struggle_joints.knees[i]
+        if not IsJointBroken(j) then SetJointMotor(j, rj[3], jointstrength) end
+    end
+    if cached_struggle_joints.hand1 ~= 0 and not IsJointBroken(cached_struggle_joints.hand1) then SetJointMotor(cached_struggle_joints.hand1, -rj[4], jointstrength) end
+    if cached_struggle_joints.hand2 ~= 0 and not IsJointBroken(cached_struggle_joints.hand2) then SetJointMotor(cached_struggle_joints.hand2, rj[5], jointstrength) end
+end
+
+function handleCritical()
+    --GLanDoSS & Yulun & Gemini3 made this mod
+end
+
+function handleDead()
+    if causeOfDeath ~= nil and causeOfDeath ~= "Blood Loss" then 
+        return 
+    end
+
+    if currentOxygen <= 0 then
+        causeOfDeath = "Drowned"
+    else
+        causeOfDeath = causeOfDeath or "Blood Loss"
+    end
+end
+
+function handleBleedingParticles(body, intensity, trans)
+    if intensity < 0.1 then return end
+    ParticleType("smoke")
+    local darkRed = 0.15 + (math.random() * 0.1)
+    ParticleColor(darkRed, 0.0, 0.0)
+    ParticleRadius(0.05, 0.005)
+    ParticleAlpha(1, 0)
+    ParticleGravity(-14)
+    ParticleDrag(0.1)
+
+    local pos = trans.pos
+    local count = math.min(10, math.floor(intensity * 10))
+    for i=1, count do
+        local vel = Vec(math.random(-10,10)/10, math.random(0,20)/10, math.random(-10,10)/10)
+        SpawnParticle(pos, vel, math.random(5, 15)/10)
+    end
+end
+
+function handleBleedingPaint(body, trans)
+    local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+
+    if hit then
+        local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+        local bloodIntensity = 0.5
+        local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+        PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+
+        local splashCount = math.random(3, 6)
+        local maxRadius = 0.7
+
+        for i = 1, splashCount do
+            local angle = math.random() * 2 * math.pi
+            local radius = math.sqrt(math.random()) * maxRadius
+            local offsetX = math.cos(angle) * radius
+            local offsetZ = math.sin(angle) * radius
+            local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+            local splashSize = mainSize * (math.random(3, 5) / 10)
+            PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+        end
+    end
+end
+
+function handleDrowningLogic()
+    local head = bodyParts.head
+    if head == 0 then return end
+
+    if IsPointInWater(GetBodyTransform(head).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+
+        if currentOxygen <= 0 then
+            for key, _ in pairs(currentHealth) do
+                currentHealth[key] = math.max(0, currentHealth[key] - 30)
+            end
+        end
+    else
+        currentOxygen = math.min(MAX_OXYGEN, currentOxygen + 20)
+    end
+end
+
+function syncDataToRegistry(finalStatus)
+    if not bodyParts or not bodyParts.torso or bodyParts.torso == 0 then return end
+
+    local dollId = tostring(bodyParts.torso)
+    local path = "temp.goredolls."..dollId
+
+    SetString(path..".state", ragdollState or "UNKNOWN", true)
+    SetString(path..".cause", causeOfDeath or "none", true)
+    SetFloat(path..".oxy", currentOxygen or 100, true)
+    SetBool(path..".sedated", isSedated == true, true)
+    SetString(path..".bandages", table.fullConcat(bandagedParts, ",", true, true, ":"), true)
+    SetFloat(path..".update", GetFloat("temp.goredollsClock"), true)
+    SetString(path..".healths", table.fullConcat(currentHealth, ",", true, true, ":"), true)
+    SetString(path..".cripples", table.fullConcat(permanentCripple, ",", true, true, ":"), true)
+    SetString(path..".bodies", table.fullConcat(bodyParts, ",", true), true)
+    if finalStatus then SetBool(path..".final", true, true) end
+end
+
+function table.fullConcat(table, separator, ignoreNil, includeKey, keySeparator)
+    local tempStr = ""
+    for key, value in pairs(table) do
+        if (ignoreNil and type(value) ~= "nil") or not ignoreNil then
+            if not includeKey then
+                tempStr = tempStr..tostring(value)..(next(table, key) and separator or "")
+            else
+                tempStr = tempStr..tostring(key)..(keySeparator and keySeparator or "")..tostring(value)..(next(table, key) and separator or "")
+            end
+        end
+    end
+    return tempStr
+end
+
+function resetJointMotors()
+    for _, v in pairs(cached_struggle_joints) do
+        if type(v) == "table" then
+            for i = 1, #v do
+                local j = v[i]
+                if not IsJointBroken(j) then SetJointMotor(j, 0, 0) end
+            end
+        elseif type(v) == "number" and v ~= 0 then
+            if not IsJointBroken(v) then SetJointMotor(v, 0, 0) end
+        end
+    end
+end
+
+function server.init()
     local tagMap = {
         head = "Head", torso = "Torso",
         lArm = "LARM", lLowerArm = "LLARM",
@@ -84,336 +354,9 @@
     cached_struggle_joints.hand1 = FindJoint("hand1")
     cached_struggle_joints.hand2 = FindJoint("hand2")
     criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-end
-
-function checkTags()
-    local resFound = false
-    local bandFound = false
-    local sedFound = false
-    for _, body in pairs(bodyParts) do
-        if body ~= 0 then
-            if HasTag(body, "resurrected") then resFound = true end
-            if HasTag(body, "bandaged") then bandFound = true end
-            if HasTag(body, "sedated") then sedFound = true end
-        end
-    end
-    isResurrected = resFound
-    isBandaged = bandFound
-    isSedated = sedFound
-end
-
-function handleSpecialStatus()
-    if isBandaged then
-        for key, body in pairs(bodyParts) do
-            if body ~= 0 then
-                initialMass[key] = GetBodyMass(body)
-                if (partDamagePercent[key] or 0) > 0.02 then
-                    bandagedParts[key] = true
-                end
-                RemoveTag(body, "bandaged")
-            end
-        end
-        isBandaged = false
-    end
-
-    if isResurrected then
-        local canBeSaved = (ragdollState ~= STATE_DEAD and ragdollState ~= STATE_DISABLED)
-
-        if not permanentDeath and canBeSaved then
-            local healthMap = {
-                head = 50, torso = 350,
-                lArm = 75, lLowerArm = 75,
-                rArm = 75, rLowerArm = 75,
-                lLeg = 75, lLowerLeg = 75,
-                rLeg = 75, rLowerLeg = 75
-            }
-            for key, body in pairs(bodyParts) do
-                if body ~= 0 then
-                    initialMass[key] = GetBodyMass(body)
-                    currentHealth[key] = healthMap[key]
-                    brokenParts[key] = false
-                end
-            end
-            ragdollState = STATE_STANDING
-        end
-
-        for _, body in pairs(bodyParts) do
-            if body ~= 0 then RemoveTag(body, "resurrected") end
-        end
-        isResurrected = false
-    end
-end
-
-function calculateBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local partWeights = {}
-
-    for key, body in pairs(bodyParts) do
-        if body ~= 0 and initialMass[key] then
-            local currentMass = GetBodyMass(body)
-            local damagePercent = (initialMass[key] - currentMass) / initialMass[key]
-            if bandagedParts[key] and damagePercent > 0.01 then
-                bandagedParts[key] = nil
-            end
-            partDamagePercent[key] = damagePercent
-
-            if (key == "lLowerLeg" or key == "rLowerLeg") and damagePercent > 0.25 then permanentCripple[key] = true end
-
-            if not brokenParts[key] and damagePercent > 0.1 then
-                if key == "head" then
-                    currentHealth[key] = 0
-                    brokenParts[key] = true
-                    permanentDeath = true
-                    eventHeadBroken = true
-                elseif key == "torso" then
-                    currentHealth[key] = currentHealth[key] * 0.5
-                    brokenParts[key] = true
-                    permanentDeath = true
-                    eventTorsoBroken = true
-                end
-            end
-
-            if damagePercent > 0.02 then
-                local initialHealth = (key == "head" and 50 or (key == "torso" and 350 or 75))
-                local healthToDrain = damagePercent * initialHealth * baseMultiplier
-
-                if currentHealth[key] > 0 then
-                    local actualDrain = math.min(currentHealth[key], healthToDrain)
-                    currentHealth[key] = currentHealth[key] - actualDrain
-                    overflowPool = overflowPool + (healthToDrain - actualDrain)
-                else
-                    overflowPool = overflowPool + healthToDrain
-                end
-            end
-
-            if currentHealth[key] > 0 then
-                local weight = (key == "head") and 0.2 or 1.0
-                partWeights[key] = weight
-                weightSum = weightSum + weight
-            end
-        end
-    end
-
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(partWeights) do currentHealth[key] = math.max(0, currentHealth[key] - (damagePerUnit * weight)) end
-    end
-end
-
-function checkStateMachine()
-    local totalH = 0
-    
-    for _, h in pairs(currentHealth) do totalH = totalH + h end
-
-    local judgeHealth = totalH
-    if causeOfDeath == "Head Trauma" or causeOfDeath == "Torso Trauma" then judgeHealth = 50 end
-    local isAnyPartBleeding = false
-    for key, percent in pairs(partDamagePercent) do
-        if percent > 0.02 then isAnyPartBleeding = true break end
-    end
-
-    if totalH <= 0 then
-        ragdollState = STATE_DISABLED
-        syncDataToRegistry(true)
-    elseif judgeHealth < 100 then
-        ragdollState = STATE_DEAD
-    elseif judgeHealth < 400 then
-        ragdollState = STATE_CRITICAL
-    elseif judgeHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        ragdollState = STATE_STRUGGLING
-    else
-        ragdollState = STATE_STANDING
-    end
-end
-
-function handleHeadBurstEffect()
-    local head = bodyParts.head
-    if head ~= 0 then
-        PlaySound(headsplat, GetBodyTransform(head).pos, 1.0)
-        local headTrans = GetBodyTransform(head)
-        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
-    end
-    causeOfDeath = causeOfDeath and causeOfDeath or "Head Trauma"
-end
-
-function handleTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso ~= 0 then
-        PlaySound(goresplat, GetBodyTransform(torso).pos, 1.0)
-
-        local torsoTrans = GetBodyTransform(torso)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-
-        if math.random() > 0.3 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
-        if math.random() > 0.4 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
-    end
-    causeOfDeath = causeOfDeath and causeOfDeath or "Torso Trauma"
-end
-
-function handleStanding(body, cachedTrans, cachedVel)
-    local legsBroken = permanentCripple.lLowerLeg or permanentCripple.rLowerLeg
-    if body == bodyParts.head and not legsBroken then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, HEAD_LIFT_VEL, 0))) end
-    if (body == bodyParts.lLowerLeg or body == bodyParts.rLowerLeg) then
-        local key = (body == bodyParts.lLowerLeg) and "lLowerLeg" or "rLowerLeg"
-        if not permanentCripple[key] and (partDamagePercent[key] or 0) < 0.1 then SetBodyVelocity(body, VecAdd(cachedVel, Vec(0, FOOT_PUSH_VEL, 0))) end
-    end
-end
-
-function handleStruggling()
-    if isSedated then handleCritical() return end
-
-    local head = bodyParts.head
-    if head ~= 0 and criticalcough then PlayLoop(criticalcough, GetBodyTransform(head).pos) end
-    panictim = panictim + 0.01
-    actualpanictim = actualpanictim + 0.01
-    if panictim > 2 and actualpanictim > 0.05 then
-        local roll = math.random(1, 6)
-        if roll <= 5 then rj[roll] = math.random(-sretractjoint, sretractjoint) end
-        actualpanictim = 0
-    end
-    for i=1, #cached_struggle_joints.shoulders do
-        local j = cached_struggle_joints.shoulders[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[1], jointstrength) end
-    end
-    for i=1, #cached_struggle_joints.hips do
-        local j = cached_struggle_joints.hips[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[2], jointstrength) end
-    end
-    for i=1, #cached_struggle_joints.knees do
-        local j = cached_struggle_joints.knees[i]
-        if not IsJointBroken(j) then SetJointMotor(j, rj[3], jointstrength) end
-    end
-    if cached_struggle_joints.hand1 ~= 0 and not IsJointBroken(cached_struggle_joints.hand1) then SetJointMotor(cached_struggle_joints.hand1, -rj[4], jointstrength) end
-    if cached_struggle_joints.hand2 ~= 0 and not IsJointBroken(cached_struggle_joints.hand2) then SetJointMotor(cached_struggle_joints.hand2, rj[5], jointstrength) end
-end
-
-function handleCritical()
-    --GLanDoSS & Yulun & Gemini3 made this mod
-end
-
-function handleDead()
-    if causeOfDeath ~= nil and causeOfDeath ~= "Blood Loss" then 
-        return 
-    end
-
-    if currentOxygen <= 0 then
-        causeOfDeath = "Drowned"
-    else
-        causeOfDeath = causeOfDeath or "Blood Loss"
-    end
-end
-
-function handleBleedingParticles(body, intensity, trans)
-    if intensity < 0.1 then return end
-    ParticleType("smoke")
-    local darkRed = 0.15 + (math.random() * 0.1)
-    ParticleColor(darkRed, 0.0, 0.0)
-    ParticleRadius(0.05, 0.005)
-    ParticleAlpha(1, 0)
-    ParticleGravity(-14)
-    ParticleDrag(0.1)
-
-    local pos = trans.pos
-    local count = math.min(10, math.floor(intensity * 10))
-    for i=1, count do
-        local vel = Vec(math.random(-10,10)/10, math.random(0,20)/10, math.random(-10,10)/10)
-        SpawnParticle(pos, vel, math.random(5, 15)/10)
-    end
-end
-
-function handleBleedingPaint(body, trans)
-    local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-
-    if hit then
-        local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-        local bloodIntensity = 0.5
-        local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-        PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-
-        local splashCount = math.random(3, 6)
-        local maxRadius = 0.7
-
-        for i = 1, splashCount do
-            local angle = math.random() * 2 * math.pi
-            local radius = math.sqrt(math.random()) * maxRadius
-            local offsetX = math.cos(angle) * radius
-            local offsetZ = math.sin(angle) * radius
-            local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-            local splashSize = mainSize * (math.random(3, 5) / 10)
-            PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-        end
-    end
-end
-
-function handleDrowningLogic()
-    local head = bodyParts.head
-    if head == 0 then return end
-
-    if IsPointInWater(GetBodyTransform(head).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-
-        if currentOxygen <= 0 then
-            for key, _ in pairs(currentHealth) do
-                currentHealth[key] = math.max(0, currentHealth[key] - 30)
-            end
-        end
-    else
-        currentOxygen = math.min(MAX_OXYGEN, currentOxygen + 20)
-    end
-end
-
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso == 0 then return end
-
-    local dollId = tostring(bodyParts.torso)
-    local path = "temp.goredolls."..dollId
-
-    SetString(path..".state", ragdollState or "UNKNOWN")
-    SetString(path..".cause", causeOfDeath or "none")
-    SetFloat(path..".oxy", currentOxygen or 100)
-    SetBool(path..".sedated", isSedated == true)
-    SetString(path..".bandages", table.fullConcat(bandagedParts, ",", true, true, ":"))
-    SetFloat(path..".update", GetFloat("temp.goredollsClock"))
-    SetString(path..".healths", table.fullConcat(currentHealth, ",", true, true, ":"))
-    SetString(path..".cripples", table.fullConcat(permanentCripple, ",", true, true, ":"))
-    SetString(path..".bodies", table.fullConcat(bodyParts, ",", true))
-    if finalStatus then SetBool(path..".final", true) end
-end
-
-function table.fullConcat(table, separator, ignoreNil, includeKey, keySeparator)
-    local tempStr = ""
-    for key, value in pairs(table) do
-        if (ignoreNil and type(value) ~= "nil") or not ignoreNil then
-            if not includeKey then
-                tempStr = tempStr..tostring(value)..(next(table, key) and separator or "")
-            else
-                tempStr = tempStr..tostring(key)..(keySeparator and keySeparator or "")..tostring(value)..(next(table, key) and separator or "")
-            end
-        end
-    end
-    return tempStr
-end
-
-function resetJointMotors()
-    for _, v in pairs(cached_struggle_joints) do
-        if type(v) == "table" then
-            for i = 1, #v do
-                local j = v[i]
-                if not IsJointBroken(j) then SetJointMotor(j, 0, 0) end
-            end
-        elseif type(v) == "number" and v ~= 0 then
-            if not IsJointBroken(v) then SetJointMotor(v, 0, 0) end
-        end
-    end
-end
-
-function update(dt)
+end
+
+function server.update(dt)
     if ragdollState == STATE_DISABLED then return end
 
     checkTimer = checkTimer + dt
@@ -466,3 +409,9 @@
     handleDead()
     end
 end
+
+function client.init()
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+

```

---

# Migration Report: lua\gore v26.1.2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v26.1.2.lua
+++ patched/lua\gore v26.1.2.lua
@@ -1,23 +1,316 @@
-bodyParts = {}
-ragdollState = "STANDING"
-STATE_STANDING = "STANDING"
-STATE_STRUGGLING = "STRUGGLING"
-STATE_CRITICAL = "CRITICAL"
-STATE_DEAD = "DEAD"
-STATE_DISABLED = "DISABLED"
-STATE_CRIPPLED = "CRIPPLED"
-causeOfDeath = ""
-eventHeadBroken = false
-eventTorsoBroken = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-timerA = 0
-timerB = 0
-currentOxygen = 100
-totalHealth = 1000
-
-function init()
+#version 2
+function updatePhysicalStats()
+    local tempTotal = 0
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            part.currentMass = GetBodyMass(part.handle)
+            part.baseMassRatio = part.currentMass / part.baseMass
+            part.initialMassRatio = part.currentMass / part.initialMass
+            part.healthRatio = part.health / part.maxHealth
+            tempTotal = tempTotal + (part.health or 0)
+        end
+    end
+    totalHealth = tempTotal
+end
+
+function checkCriticalTrauma()
+    local head = bodyParts.head
+    if not eventHeadBroken and head.initialMassRatio < 0.95 then
+        head.health = 0
+        playHeadBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
+        eventHeadBroken = true
+    end
+    local torso = bodyParts.torso
+    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
+        torso.health = torso.health * 0.5
+        playTorsoBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
+        eventTorsoBroken = true
+    end
+end
+
+function processBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local viableParts = {}
+
+    for key, part in pairs(bodyParts) do
+        local damagePercent = 1.0 - part.baseMassRatio
+        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
+        if damagePercent > 0.02 then
+            part.isBleeding = true
+            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
+            if part.health ~= 0 then
+                local actualDrain = math.min(part.health, healthToDrain)
+                part.health = part.health - actualDrain
+                overflowPool = overflowPool + (healthToDrain - actualDrain)
+            else
+                overflowPool = overflowPool + healthToDrain
+            end
+        else
+            part.isBleeding = false
+        end
+        if part.health ~= 0 then
+            local weight = (key == "head") and 0.2 or 1.0
+            viableParts[key] = weight
+            weightSum = weightSum + weight
+        end
+    end
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(viableParts) do
+            local part = bodyParts[key]
+            part.health = math.max(0, part.health - (damagePerUnit * weight))
+        end
+    end
+end
+
+function playHeadBurstEffect()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local headTrans = GetBodyTransform(head.handle)
+        PlaySound(headsplat, headTrans.pos, 1.0)
+        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
+    end
+end
+
+function playTorsoBurstEffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local torsoTrans = GetBodyTransform(torso.handle)
+        PlaySound(goresplat, torsoTrans.pos, 1.0)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
+    end
+end
+
+function handleStanding()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local vel = GetBodyVelocity(head.handle)
+        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.5, 0)))
+    end
+    local lLeg = bodyParts.lLowerLeg
+    if lLeg and lLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(lLeg.handle)
+        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -2.0, 0)))
+    end
+    local rLeg = bodyParts.rLowerLeg
+    if rLeg and rLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(rLeg.handle)
+        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -2.0, 0)))
+    end
+end
+
+function handleStruggling()
+    local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local dependency = {
+        lLowerArm = "lArm",
+        rLowerArm = "rArm",
+        lLowerLeg = "lLeg",
+        rLowerLeg = "rLeg"}
+    for key, p in pairs(bodyParts) do
+        if p.handle ~= 0 and p.initialMassRatio > 0.9 and key ~= "torso" and key ~= "head" then
+            local parentKey = dependency[key]
+            local canStruggle = true
+            if parentKey then
+                local parent = bodyParts[parentKey]
+                if not parent or parent.initialMassRatio < 0.9 then
+                    canStruggle = false
+                end
+            end
+            if canStruggle and math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCritical()
+    local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local parts = {
+        bodyParts.head, bodyParts.torso, 
+        bodyParts.lArm, bodyParts.rArm, 
+        bodyParts.lLeg, bodyParts.rLeg}
+    for i = 1, #parts do
+        local p = parts[i]
+        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
+            if math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function checkTags()
+    isResurrected = false
+    isBandaged = false
+    isSedated = false
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            if HasTag(part.handle, "resurrected") then 
+                isResurrected = true 
+                RemoveTag(part.handle, "resurrected")
+            end
+            if HasTag(part.handle, "bandaged") then 
+                isBandaged = true 
+                RemoveTag(part.handle, "bandaged")
+            end
+            if HasTag(part.handle, "sedated") then 
+                isSedated = true 
+                RemoveTag(part.handle, "sedated") 
+            end
+        end
+    end
+end
+
+function handleSpecialStatus()
+    if isBandaged then
+        for _, part in pairs(bodyParts) do
+            if part.handle ~= 0 then
+                if part.baseMassRatio < 0.99 then
+                    part.isBandaged = true
+                    part.baseMass = GetBodyMass(part.handle)
+                    part.baseMassRatio = 1.0 
+                end
+            end
+        end
+        isBandaged = false
+    end
+    if isResurrected then
+        if ragdollState ~= STATE_DEAD then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then
+                    part.health = part.maxHealth
+                    part.isBandaged = false
+                    part.baseMass = GetBodyMass(part.handle)
+                end
+            end
+        end
+        isResurrected = false
+    end
+end
+
+function handleDrowningLogic()
+    local head = bodyParts.head
+    if not head or head.handle == 0 then return end
+    if IsPointInWater(GetBodyTransform(head.handle).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+        if currentOxygen <= 0 then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
+            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
+        end
+    else
+        currentOxygen = math.min(100, currentOxygen + 20)
+    end
+end
+
+function drawBleedingParticles()
+end
+
+function drawBleedingPaint()
+    if GetFps() < 40 or totalHealth < 400 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local bloodIntensity = 0.5
+                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+                local splashCount = math.random(1, 3)
+                local maxRadius = 0.6
+                for i = 1, splashCount do
+                    local angle = math.random() * 2 * math.pi
+                    local radius = math.sqrt(math.random()) * maxRadius
+                    local offsetX = math.cos(angle) * radius
+                    local offsetZ = math.sin(angle) * radius
+                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+                    local splashSize = mainSize * (math.random(3, 5) / 10)
+                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+                end
+            end
+        end
+    end
+end
+
+function syncDataToRegistry(finalStatus)
+    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
+    local dollId = tostring(bodyParts.torso.handle)
+    local path = "temp.goredolls." .. dollId
+    SetString(path .. ".state", ragdollState or "UNKNOWN", true)
+    SetString(path .. ".cause", causeOfDeath or "none", true)
+    SetFloat(path .. ".oxy", currentOxygen or 100, true)
+    SetBool(path .. ".sedated", isSedated == true, true)
+    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"), true)
+    if finalStatus then SetBool(path .. ".final", true, true) end
+    local hList, bList, cList = {}, {}, {}
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            table.insert(hList, key .. ":" .. part.health)
+            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
+            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
+            table.insert(cList, key .. ":" .. isCripple)
+        end
+    end
+    SetString(path .. ".healths", table.concat(hList, ","), true)
+    SetString(path .. ".bandages", table.concat(bList, ","), true)
+    SetString(path .. ".cripples", table.concat(cList, ","), true)
+end
+
+function checkStateMachine()
+    local isAnyPartBleeding = false
+    for _, part in pairs(bodyParts) do
+        if part.isBleeding then 
+            isAnyPartBleeding = true 
+        end
+    end
+    local legsBroken = false
+    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
+    for _, key in ipairs(legKeys) do
+        local part = bodyParts[key]
+        if part and part.initialMassRatio < 0.75 then
+            legsBroken = true
+            break
+        end
+    end
+    if totalHealth <= 0 then
+        ragdollState = STATE_DISABLED
+        syncDataToRegistry(true)
+    elseif totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
+        ragdollState = STATE_DEAD
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
+    elseif totalHealth < 400 then
+        ragdollState = STATE_CRITICAL
+    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        ragdollState = STATE_STRUGGLING
+    elseif legsBroken then
+        ragdollState = STATE_CRIPPLED
+    else
+        ragdollState = STATE_STANDING
+    end
+end
+
+function server.init()
     local config = {
         head = { tag = "Head", maxH = 50 },
         torso = { tag = "Torso", maxH = 350 },
@@ -51,322 +344,9 @@
         end
     end
     criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-end
-
-function updatePhysicalStats()
-    local tempTotal = 0
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            part.currentMass = GetBodyMass(part.handle)
-            part.baseMassRatio = part.currentMass / part.baseMass
-            part.initialMassRatio = part.currentMass / part.initialMass
-            part.healthRatio = part.health / part.maxHealth
-            tempTotal = tempTotal + (part.health or 0)
-        end
-    end
-    totalHealth = tempTotal
-end
-
-function checkCriticalTrauma()
-    local head = bodyParts.head
-    if not eventHeadBroken and head.initialMassRatio < 0.95 then
-        head.health = 0
-        playHeadBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
-        eventHeadBroken = true
-    end
-    local torso = bodyParts.torso
-    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
-        torso.health = torso.health * 0.5
-        playTorsoBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
-        eventTorsoBroken = true
-    end
-end
-
-function processBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local viableParts = {}
-
-    for key, part in pairs(bodyParts) do
-        local damagePercent = 1.0 - part.baseMassRatio
-        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
-        if damagePercent > 0.02 then
-            part.isBleeding = true
-            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
-            if part.health > 0 then
-                local actualDrain = math.min(part.health, healthToDrain)
-                part.health = part.health - actualDrain
-                overflowPool = overflowPool + (healthToDrain - actualDrain)
-            else
-                overflowPool = overflowPool + healthToDrain
-            end
-        else
-            part.isBleeding = false
-        end
-        if part.health > 0 then
-            local weight = (key == "head") and 0.2 or 1.0
-            viableParts[key] = weight
-            weightSum = weightSum + weight
-        end
-    end
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(viableParts) do
-            local part = bodyParts[key]
-            part.health = math.max(0, part.health - (damagePerUnit * weight))
-        end
-    end
-end
-
-function playHeadBurstEffect()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local headTrans = GetBodyTransform(head.handle)
-        PlaySound(headsplat, headTrans.pos, 1.0)
-        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
-    end
-end
-
-function playTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local torsoTrans = GetBodyTransform(torso.handle)
-        PlaySound(goresplat, torsoTrans.pos, 1.0)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
-    end
-end
-
-function handleStanding()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local vel = GetBodyVelocity(head.handle)
-        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.5, 0)))
-    end
-    local lLeg = bodyParts.lLowerLeg
-    if lLeg and lLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(lLeg.handle)
-        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -2.0, 0)))
-    end
-    local rLeg = bodyParts.rLowerLeg
-    if rLeg and rLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(rLeg.handle)
-        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -2.0, 0)))
-    end
-end
-
-function handleStruggling()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local dependency = {
-        lLowerArm = "lArm",
-        rLowerArm = "rArm",
-        lLowerLeg = "lLeg",
-        rLowerLeg = "rLeg"}
-    for key, p in pairs(bodyParts) do
-        if p.handle ~= 0 and p.initialMassRatio > 0.9 and key ~= "torso" and key ~= "head" then
-            local parentKey = dependency[key]
-            local canStruggle = true
-            if parentKey then
-                local parent = bodyParts[parentKey]
-                if not parent or parent.initialMassRatio < 0.9 then
-                    canStruggle = false
-                end
-            end
-            if canStruggle and math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCritical()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local parts = {
-        bodyParts.head, bodyParts.torso, 
-        bodyParts.lArm, bodyParts.rArm, 
-        bodyParts.lLeg, bodyParts.rLeg}
-    for i = 1, #parts do
-        local p = parts[i]
-        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
-            if math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function checkTags()
-    isResurrected = false
-    isBandaged = false
-    isSedated = false
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            if HasTag(part.handle, "resurrected") then 
-                isResurrected = true 
-                RemoveTag(part.handle, "resurrected")
-            end
-            if HasTag(part.handle, "bandaged") then 
-                isBandaged = true 
-                RemoveTag(part.handle, "bandaged")
-            end
-            if HasTag(part.handle, "sedated") then 
-                isSedated = true 
-                RemoveTag(part.handle, "sedated") 
-            end
-        end
-    end
-end
-
-function handleSpecialStatus()
-    if isBandaged then
-        for _, part in pairs(bodyParts) do
-            if part.handle ~= 0 then
-                if part.baseMassRatio < 0.99 then
-                    part.isBandaged = true
-                    part.baseMass = GetBodyMass(part.handle)
-                    part.baseMassRatio = 1.0 
-                end
-            end
-        end
-        isBandaged = false
-    end
-    if isResurrected then
-        if ragdollState ~= STATE_DEAD then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then
-                    part.health = part.maxHealth
-                    part.isBandaged = false
-                    part.baseMass = GetBodyMass(part.handle)
-                end
-            end
-        end
-        isResurrected = false
-    end
-end
-
-function handleDrowningLogic()
-    local head = bodyParts.head
-    if not head or head.handle == 0 then return end
-    if IsPointInWater(GetBodyTransform(head.handle).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-        if currentOxygen <= 0 then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
-            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
-        end
-    else
-        currentOxygen = math.min(100, currentOxygen + 20)
-    end
-end
-
-function drawBleedingParticles()
-end
-
-function drawBleedingPaint()
-    if GetFps() < 40 or totalHealth < 400 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            local hit, dist, normal = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local bloodIntensity = 0.5
-                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-                local splashCount = math.random(1, 3)
-                local maxRadius = 0.6
-                for i = 1, splashCount do
-                    local angle = math.random() * 2 * math.pi
-                    local radius = math.sqrt(math.random()) * maxRadius
-                    local offsetX = math.cos(angle) * radius
-                    local offsetZ = math.sin(angle) * radius
-                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-                    local splashSize = mainSize * (math.random(3, 5) / 10)
-                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-                end
-            end
-        end
-    end
-end
-
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
-    local dollId = tostring(bodyParts.torso.handle)
-    local path = "temp.goredolls." .. dollId
-    SetString(path .. ".state", ragdollState or "UNKNOWN")
-    SetString(path .. ".cause", causeOfDeath or "none")
-    SetFloat(path .. ".oxy", currentOxygen or 100)
-    SetBool(path .. ".sedated", isSedated == true)
-    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"))
-    if finalStatus then SetBool(path .. ".final", true) end
-    local hList, bList, cList = {}, {}, {}
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            table.insert(hList, key .. ":" .. part.health)
-            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
-            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
-            table.insert(cList, key .. ":" .. isCripple)
-        end
-    end
-    SetString(path .. ".healths", table.concat(hList, ","))
-    SetString(path .. ".bandages", table.concat(bList, ","))
-    SetString(path .. ".cripples", table.concat(cList, ","))
-end
-
-function checkStateMachine()
-    local isAnyPartBleeding = false
-    for _, part in pairs(bodyParts) do
-        if part.isBleeding then 
-            isAnyPartBleeding = true 
-        end
-    end
-    local legsBroken = false
-    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
-    for _, key in ipairs(legKeys) do
-        local part = bodyParts[key]
-        if part and part.initialMassRatio < 0.75 then
-            legsBroken = true
-            break
-        end
-    end
-    if totalHealth <= 0 then
-        ragdollState = STATE_DISABLED
-        syncDataToRegistry(true)
-    elseif totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
-        ragdollState = STATE_DEAD
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
-    elseif totalHealth < 400 then
-        ragdollState = STATE_CRITICAL
-    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        ragdollState = STATE_STRUGGLING
-    elseif legsBroken then
-        ragdollState = STATE_CRIPPLED
-    else
-        ragdollState = STATE_STANDING
-    end
-end
-
-function update(dt)
+end
+
+function server.update(dt)
     if ragdollState == STATE_DISABLED then return end
     timerA = timerA + 1
     if timerA >= 10 then
@@ -375,7 +355,7 @@
         processBleeding()
         checkStateMachine()
         drawBleedingParticles()
-        
+
         timerA = 0
         timerB = timerB + 1
         if timerB >= 10 then
@@ -398,4 +378,10 @@
     elseif ragdollState == STATE_DEAD then 
         handleDead()
     end
-end+end
+
+function client.init()
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+

```

---

# Migration Report: lua\gore v26.1.21.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v26.1.21.lua
+++ patched/lua\gore v26.1.21.lua
@@ -1,29 +1,425 @@
-bodyParts = {}
-allShapes = {}
-COND_NORMAL = "NORMAL"
-COND_INJURED = "INJURED"
-COND_CRITICAL = "CRITICAL"
-COND_DEAD = "DEAD"
-COND_DISABLED = "DISABLED"
-BEH_STANDING = "STANDING"
-BEH_STRUGGLING = "STRUGGLING"
-BEH_CONVULSING = "CONVULSING"
-BEH_STILL = "STILL"
-currentCondition = COND_NORMAL
-currentBehavior = BEH_STANDING
-causeOfDeath = ""
-eventHeadBroken = false
-eventTorsoBroken = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-timerA = 0
-timerB = 0
-currentOxygen = 100
-totalHealth = 1000
-currentFps = 0
-
-function init()
+#version 2
+calculateStateMachine()
+    local isAnyPartBleeding = false
+    for _, part in pairs(bodyParts) do
+        if part.isBleeding then 
+            isAnyPartBleeding = true 
+        end
+    end
+    local legsBroken = false
+    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
+    for _, key in ipairs(legKeys) do
+        local part = bodyParts[key]
+        if part and part.initialMassRatio < 0.75 then
+            legsBroken = true
+            break
+        end
+    end
+
+    if totalHealth <= 0 then
+        currentCondition = COND_DISABLED
+    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
+        currentCondition = COND_DEAD
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
+    elseif totalHealth < 400 then
+        currentCondition = COND_CRITICAL
+    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        currentCondition = COND_INJURED
+    else
+        currentCondition = COND_NORMAL
+    end
+
+    if currentCondition == COND_DEAD or currentCondition == COND_DISABLED then
+        currentBehavior = BEH_STILL
+    elseif isSedated and currentCondition ~= COND_NORMAL then
+        currentBehavior = BEH_STILL
+    elseif currentCondition == COND_CRITICAL then
+        currentBehavior = BEH_CONVULSING
+    elseif currentCondition == COND_INJURED then
+        currentBehavior = BEH_STRUGGLING
+    elseif legsBroken then
+        currentBehavior = BEH_STILL
+    else
+        currentBehavior = BEH_STANDING
+    end
+end
+
+functi
+
+ calculateBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local viableParts = {}
+    for key, part in pairs(bodyParts) do
+        local damagePercent = 1.0 - part.baseMassRatio
+        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
+        if damagePercent > 0.02 then
+            part.isBleeding = true
+            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
+            if part.health ~= 0 then
+                local actualDrain = math.min(part.health, healthToDrain)
+                part.health = part.health - actualDrain
+                overflowPool = overflowPool + (healthToDrain - actualDrain)
+            else
+                overflowPool = overflowPool + healthToDrain
+            end
+        else
+            part.isBleeding = false
+        end
+        if part.health ~= 0 then
+            local weight = (key == "head") and 0.2 or 1.0
+            viableParts[key] = weight
+            weightSum = weightSum + weight
+        end
+    end
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(viableParts) do
+            local part = bodyParts[key]
+            part.health = math.max(0, part.health - (damagePerUnit * weight))
+        end
+    end
+end
+
+functi
+
+ calculateDrowning()
+    local head = bodyParts.head
+    if not head or head.handle == 0 then return end
+    if IsPointInWater(GetBodyTransform(head.handle).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+        if currentOxygen <= 0 then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
+            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
+        end
+    else
+        currentOxygen = math.min(100, currentOxygen + 20)
+    end
+end
+
+-- 检查函
+
+ysicalStats()
+    local tempTotal = 0
+    currentFps = GetFps()
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            part.currentMass = GetBodyMass(part.handle)
+            part.baseMassRatio = part.currentMass / part.baseMass
+            part.initialMassRatio = part.currentMass / part.initialMass
+            part.healthRatio = part.health / part.maxHealth
+            tempTotal = tempTotal + (part.health or 0)
+        end
+    end
+    totalHealth = tempTotal
+end
+
+function check
+
+iticalTrauma()
+    local head = bodyParts.head
+    if not eventHeadBroken and head.initialMassRatio < 0.95 then
+        head.health = head.health * 0.8
+        playHeadBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
+        eventHeadBroken = true
+    end
+    local torso = bodyParts.torso
+    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
+        torso.health = torso.health * 0.5
+        playTorsoBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
+        eventTorsoBroken = true
+    end
+end
+
+function check
+
+gs()
+    isResurrected = false
+    isBandaged = false
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            if HasTag(part.handle, "resurrected") then 
+                isResurrected = true 
+                RemoveTag(part.handle, "resurrected")
+            end
+            if HasTag(part.handle, "bandaged") then 
+                isBandaged = true 
+                RemoveTag(part.handle, "bandaged")
+            end
+            if HasTag(part.handle, "sedated") then 
+                isSedated = true 
+                RemoveTag(part.handle, "sedated") 
+            end
+        end
+    end
+end
+
+function check
+
+ecialStatus()
+    if isBandaged then
+        for _, part in pairs(bodyParts) do
+            if part.handle ~= 0 then
+                if part.baseMassRatio < 0.99 then
+                    part.isBandaged = true
+                    part.baseMass = GetBodyMass(part.handle)
+                    part.baseMassRatio = 1.0 
+                end
+            end
+        end
+        isBandaged = false
+    end
+    if isResurrected then
+        if currentCondition ~= COND_DEAD then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then
+                    part.health = part.maxHealth
+                    part.isBandaged = false
+                    part.baseMass = GetBodyMass(part.handle)
+                end
+            end
+        end
+        isResurrected = false
+    end
+end
+
+-- 效果函数
+functi
+
+fect()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local headTrans = GetBodyTransform(head.handle)
+        PlaySound(headsplat, headTrans.pos, 1.0)
+        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
+        drawBleedingExplosion(headTrans.pos)
+    end
+end
+
+function playTorsoBurs
+
+ffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local torsoTrans = GetBodyTransform(torso.handle)
+        PlaySound(goresplat, torsoTrans.pos, 1.0)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
+        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
+        drawBleedingExplosion(torsoTrans.pos)
+    end
+end
+
+-- 行为函数
+function handl
+
+cal head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local vel = GetBodyVelocity(head.handle)
+        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.5 * headUpwardForce, 0)))
+    end
+    local lLeg = bodyParts.lLowerLeg
+    if lLeg and lLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(lLeg.handle)
+        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
+    end
+    local rLeg = bodyParts.rLowerLeg
+    if rLeg and rLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(rLeg.handle)
+        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
+    end
+end
+
+function handleStruggling()
+  
+
+local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local dependency = {
+        lLowerArm = "lArm",
+        rLowerArm = "rArm",
+        lLowerLeg = "lLeg",
+        rLowerLeg = "rLeg"}
+    for key, p in pairs(bodyParts) do
+        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
+            local parentKey = dependency[key]
+            local canStruggle = true
+            if parentKey then
+                local parent = bodyParts[parentKey]
+                if not parent or parent.initialMassRatio < 0.95 then
+                    canStruggle = false
+                end
+            end
+            if canStruggle and math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCritical()
+    
+
+cal torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local parts = {
+        bodyParts.head, bodyParts.torso, 
+        bodyParts.lArm, bodyParts.rArm, 
+        bodyParts.lLeg, bodyParts.rLeg}
+    for i = 1, #parts do
+        local p = parts[i]
+        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
+            if math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+-- 绘制函数
+function drawBleedingP
+
+currentFps < 40 or math.random() < 0.8 then return end
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            local intensity = 1.0 - part.baseMassRatio
+            ParticleType("smoke")
+            ParticleColor(0.3, 0.0, 0.0)
+            ParticleRadius(0.05)
+            ParticleGravity(-50)
+            ParticleDrag(1)
+            local count = math.floor(intensity * 10)
+            for i = 1, count do
+                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
+            end
+        end
+    end
+end
+
+function drawBleedingPaint()
+    if cu
+
+entFps < 40 or totalHealth < 400 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local bloodIntensity = 0.5
+                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+                local splashCount = math.random(1, 3)
+                local maxRadius = 0.6
+                for i = 1, splashCount do
+                    local angle = math.random() * 2 * math.pi
+                    local radius = math.sqrt(math.random()) * maxRadius
+                    local offsetX = math.cos(angle) * radius
+                    local offsetZ = math.sin(angle) * radius
+                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+                    local splashSize = mainSize * (math.random(3, 5) / 10)
+                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+                end
+            end
+        end
+    end
+end
+
+function drawBleedingDripping()
+    if
+
+urrentFps < 40 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local dripSize = math.random(1, 3) / 10
+                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
+            end
+        end
+    end
+end
+
+function drawBleedingExplosion(pos)
+  
+
+if currentFps < 40 then return end
+    local camTrans = GetCameraTransform()
+    local camPos = camTrans.pos
+    local baseDir = VecNormalize(VecSub(pos, camPos))
+    local rayCount = 8
+    for i = 1, rayCount do
+        local spread = 0.3
+        local scatterDir = VecNormalize(Vec(
+            baseDir[1] + (math.random() - 0.5) * spread,
+            baseDir[2] + (math.random() - 0.5) * spread,
+            baseDir[3] + (math.random() - 0.5) * spread))
+        QueryRejectShapes(allShapes)
+        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
+        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
+        if hit and shape ~= 0 then
+            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
+            local dotsPerHit = math.random(3, 6)
+            for j = 1, dotsPerHit do
+                local finalPos = VecAdd(hitPos, Vec(
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5))
+                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
+            end
+        end
+    end
+end
+
+-- 注册信息
+function syncDataToRegistry(fi
+
+not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
+    local dollId = tostring(bodyParts.torso.handle)
+    local path = "temp.goredolls." .. dollId
+    SetString(path .. ".state", currentCondition or "UNKNOWN", true)
+    SetString(path .. ".behavior", currentBehavior or "STILL", true)
+    SetString(path .. ".cause", causeOfDeath or "none", true)
+    SetFloat(path .. ".oxy", currentOxygen or 100, true)
+    SetBool(path .. ".sedated", isSedated == true, true)
+    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"), true)
+    if finalStatus then SetBool(path .. ".final", true, true) end
+    local hList, bList, cList = {}, {}, {}
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            table.insert(hList, key .. ":" .. part.health)
+            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
+            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
+            table.insert(cList, key .. ":" .. isCripple)
+        end
+    end
+    SetString(path .. ".healths", table.concat(hList, ","), true)
+    SetString(path .. ".bandages", table.concat(bList, ","), true)
+    SetString(path .. ".cripples", table.concat(cList, ","), true)
+end
+
+function server.init()
     local config = {
         head = { tag = "Head", maxH = 50 },
         torso = { tag = "Torso", maxH = 350 },
@@ -65,18 +461,9 @@
         end
     end
     local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local calculatedForce = 3.0 - (head.initialMass * 0.03)
-        headUpwardForce = math.max(0.5, math.min(3.0, calculatedForce))
-    else
-        if head then headUpwardForce = 1.0 end
-    end
-    criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-end
-
-function update(dt)
+end
+
+function server.update(dt)
     if currentCondition == COND_DISABLED then return end
     timerA = timerA + 1
     if timerA >= 10 then
@@ -97,7 +484,7 @@
     end
     drawBleedingParticles()
     syncDataToRegistry()
-    
+
     if currentBehavior == BEH_STANDING then
         handleStanding() 
     elseif currentBehavior == BEH_STRUGGLING then
@@ -109,398 +496,15 @@
     end
 end
 
--- 计算函数
-function calculateStateMachine()
-    local isAnyPartBleeding = false
-    for _, part in pairs(bodyParts) do
-        if part.isBleeding then 
-            isAnyPartBleeding = true 
-        end
-    end
-    local legsBroken = false
-    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
-    for _, key in ipairs(legKeys) do
-        local part = bodyParts[key]
-        if part and part.initialMassRatio < 0.75 then
-            legsBroken = true
-            break
-        end
-    end
-
-    if totalHealth <= 0 then
-        currentCondition = COND_DISABLED
-    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
-        currentCondition = COND_DEAD
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
-    elseif totalHealth < 400 then
-        currentCondition = COND_CRITICAL
-    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        currentCondition = COND_INJURED
+function client.init()
+    if head and head.handle ~= 0 then
+        local calculatedForce = 3.0 - (head.initialMass * 0.03)
+        headUpwardForce = math.max(0.5, math.min(3.0, calculatedForce))
     else
-        currentCondition = COND_NORMAL
-    end
-
-    if currentCondition == COND_DEAD or currentCondition == COND_DISABLED then
-        currentBehavior = BEH_STILL
-    elseif isSedated and currentCondition ~= COND_NORMAL then
-        currentBehavior = BEH_STILL
-    elseif currentCondition == COND_CRITICAL then
-        currentBehavior = BEH_CONVULSING
-    elseif currentCondition == COND_INJURED then
-        currentBehavior = BEH_STRUGGLING
-    elseif legsBroken then
-        currentBehavior = BEH_STILL
-    else
-        currentBehavior = BEH_STANDING
-    end
-end
-
-function calculateBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local viableParts = {}
-    for key, part in pairs(bodyParts) do
-        local damagePercent = 1.0 - part.baseMassRatio
-        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
-        if damagePercent > 0.02 then
-            part.isBleeding = true
-            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
-            if part.health > 0 then
-                local actualDrain = math.min(part.health, healthToDrain)
-                part.health = part.health - actualDrain
-                overflowPool = overflowPool + (healthToDrain - actualDrain)
-            else
-                overflowPool = overflowPool + healthToDrain
-            end
-        else
-            part.isBleeding = false
-        end
-        if part.health > 0 then
-            local weight = (key == "head") and 0.2 or 1.0
-            viableParts[key] = weight
-            weightSum = weightSum + weight
-        end
-    end
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(viableParts) do
-            local part = bodyParts[key]
-            part.health = math.max(0, part.health - (damagePerUnit * weight))
-        end
-    end
-end
-
-function calculateDrowning()
-    local head = bodyParts.head
-    if not head or head.handle == 0 then return end
-    if IsPointInWater(GetBodyTransform(head.handle).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-        if currentOxygen <= 0 then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
-            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
-        end
-    else
-        currentOxygen = math.min(100, currentOxygen + 20)
-    end
-end
-
--- 检查函数
-function checkPhysicalStats()
-    local tempTotal = 0
-    currentFps = GetFps()
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            part.currentMass = GetBodyMass(part.handle)
-            part.baseMassRatio = part.currentMass / part.baseMass
-            part.initialMassRatio = part.currentMass / part.initialMass
-            part.healthRatio = part.health / part.maxHealth
-            tempTotal = tempTotal + (part.health or 0)
-        end
-    end
-    totalHealth = tempTotal
-end
-
-function checkCriticalTrauma()
-    local head = bodyParts.head
-    if not eventHeadBroken and head.initialMassRatio < 0.95 then
-        head.health = head.health * 0.8
-        playHeadBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
-        eventHeadBroken = true
-    end
-    local torso = bodyParts.torso
-    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
-        torso.health = torso.health * 0.5
-        playTorsoBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
-        eventTorsoBroken = true
-    end
-end
-
-function checkTags()
-    isResurrected = false
-    isBandaged = false
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            if HasTag(part.handle, "resurrected") then 
-                isResurrected = true 
-                RemoveTag(part.handle, "resurrected")
-            end
-            if HasTag(part.handle, "bandaged") then 
-                isBandaged = true 
-                RemoveTag(part.handle, "bandaged")
-            end
-            if HasTag(part.handle, "sedated") then 
-                isSedated = true 
-                RemoveTag(part.handle, "sedated") 
-            end
-        end
-    end
-end
-
-function checkSpecialStatus()
-    if isBandaged then
-        for _, part in pairs(bodyParts) do
-            if part.handle ~= 0 then
-                if part.baseMassRatio < 0.99 then
-                    part.isBandaged = true
-                    part.baseMass = GetBodyMass(part.handle)
-                    part.baseMassRatio = 1.0 
-                end
-            end
-        end
-        isBandaged = false
-    end
-    if isResurrected then
-        if currentCondition ~= COND_DEAD then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then
-                    part.health = part.maxHealth
-                    part.isBandaged = false
-                    part.baseMass = GetBodyMass(part.handle)
-                end
-            end
-        end
-        isResurrected = false
-    end
-end
-
--- 效果函数
-function playHeadBurstEffect()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local headTrans = GetBodyTransform(head.handle)
-        PlaySound(headsplat, headTrans.pos, 1.0)
-        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
-        drawBleedingExplosion(headTrans.pos)
-    end
-end
-
-function playTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local torsoTrans = GetBodyTransform(torso.handle)
-        PlaySound(goresplat, torsoTrans.pos, 1.0)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
-        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
-        drawBleedingExplosion(torsoTrans.pos)
-    end
-end
-
--- 行为函数
-function handleStanding()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local vel = GetBodyVelocity(head.handle)
-        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.5 * headUpwardForce, 0)))
-    end
-    local lLeg = bodyParts.lLowerLeg
-    if lLeg and lLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(lLeg.handle)
-        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
-    end
-    local rLeg = bodyParts.rLowerLeg
-    if rLeg and rLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(rLeg.handle)
-        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
-    end
-end
-
-function handleStruggling()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local dependency = {
-        lLowerArm = "lArm",
-        rLowerArm = "rArm",
-        lLowerLeg = "lLeg",
-        rLowerLeg = "rLeg"}
-    for key, p in pairs(bodyParts) do
-        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
-            local parentKey = dependency[key]
-            local canStruggle = true
-            if parentKey then
-                local parent = bodyParts[parentKey]
-                if not parent or parent.initialMassRatio < 0.95 then
-                    canStruggle = false
-                end
-            end
-            if canStruggle and math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCritical()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local parts = {
-        bodyParts.head, bodyParts.torso, 
-        bodyParts.lArm, bodyParts.rArm, 
-        bodyParts.lLeg, bodyParts.rLeg}
-    for i = 1, #parts do
-        local p = parts[i]
-        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
-            if math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
--- 绘制函数
-function drawBleedingParticles()
-    if currentFps < 40 or math.random() < 0.8 then return end
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            local intensity = 1.0 - part.baseMassRatio
-            ParticleType("smoke")
-            ParticleColor(0.3, 0.0, 0.0)
-            ParticleRadius(0.05)
-            ParticleGravity(-50)
-            ParticleDrag(1)
-            local count = math.floor(intensity * 10)
-            for i = 1, count do
-                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
-            end
-        end
-    end
-end
-
-function drawBleedingPaint()
-    if currentFps < 40 or totalHealth < 400 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local bloodIntensity = 0.5
-                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-                local splashCount = math.random(1, 3)
-                local maxRadius = 0.6
-                for i = 1, splashCount do
-                    local angle = math.random() * 2 * math.pi
-                    local radius = math.sqrt(math.random()) * maxRadius
-                    local offsetX = math.cos(angle) * radius
-                    local offsetZ = math.sin(angle) * radius
-                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-                    local splashSize = mainSize * (math.random(3, 5) / 10)
-                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-                end
-            end
-        end
-    end
-end
-
-function drawBleedingDripping()
-    if currentFps < 40 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local dripSize = math.random(1, 3) / 10
-                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
-            end
-        end
-    end
-end
-
-function drawBleedingExplosion(pos)
-    if currentFps < 40 then return end
-    local camTrans = GetCameraTransform()
-    local camPos = camTrans.pos
-    local baseDir = VecNormalize(VecSub(pos, camPos))
-    local rayCount = 8
-    for i = 1, rayCount do
-        local spread = 0.3
-        local scatterDir = VecNormalize(Vec(
-            baseDir[1] + (math.random() - 0.5) * spread,
-            baseDir[2] + (math.random() - 0.5) * spread,
-            baseDir[3] + (math.random() - 0.5) * spread))
-        QueryRejectShapes(allShapes)
-        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
-        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
-        if hit and shape ~= 0 then
-            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
-            local dotsPerHit = math.random(3, 6)
-            for j = 1, dotsPerHit do
-                local finalPos = VecAdd(hitPos, Vec(
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5))
-                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
-            end
-        end
-    end
-end
-
--- 注册信息
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
-    local dollId = tostring(bodyParts.torso.handle)
-    local path = "temp.goredolls." .. dollId
-    SetString(path .. ".state", currentCondition or "UNKNOWN")
-    SetString(path .. ".behavior", currentBehavior or "STILL")
-    SetString(path .. ".cause", causeOfDeath or "none")
-    SetFloat(path .. ".oxy", currentOxygen or 100)
-    SetBool(path .. ".sedated", isSedated == true)
-    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"))
-    if finalStatus then SetBool(path .. ".final", true) end
-    local hList, bList, cList = {}, {}, {}
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            table.insert(hList, key .. ":" .. part.health)
-            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
-            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
-            table.insert(cList, key .. ":" .. isCripple)
-        end
-    end
-    SetString(path .. ".healths", table.concat(hList, ","))
-    SetString(path .. ".bandages", table.concat(bList, ","))
-    SetString(path .. ".cripples", table.concat(cList, ","))
-end
-
-
-
+        if head then headUpwardForce = 1.0 end
+    end
+    criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+

```

---

# Migration Report: lua\gore v26.1.25.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v26.1.25.lua
+++ patched/lua\gore v26.1.25.lua
@@ -1,38 +1,486 @@
--- GYM Ragdoll Framework v26.1.25 (Public Version 1)
--- Made by GLaDOSS, Yulun & Please Pick a Name
--- Programming assisted by Gemini 3
--- Vibe coding is the best programming method in the world
-
-bodyParts = {}
-allShapes = {}
-COND_NORMAL = "NORMAL"
-COND_INJURED = "INJURED"
-COND_CRITICAL = "CRITICAL"
-COND_DEAD = "DEAD"
-COND_DISABLED = "DISABLED"
-BEH_STANDING = "STANDING"
-BEH_STRUGGLING = "STRUGGLING"
-BEH_CONVULSING = "CONVULSING"
-BEH_STILL = "STILL"
-BEH_FALLING = "FALLING"
-currentCondition = COND_NORMAL
-currentBehavior = BEH_STANDING
-causeOfDeath = ""
-eventHeadBroken = false
-eventTorsoBroken = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-isFalling = false
-timerA = 0
-timerB = 0
-currentOxygen = 100
-totalHealth = 1000
-currentFps = 0
-fallTimer = 0
-standingStrength = 1
-
-function init()
+#version 2
+calculateStateMachine()
+    local isAnyPartBleeding = false
+    for _, part in pairs(bodyParts) do
+        if part.isBleeding then 
+            isAnyPartBleeding = true 
+        end
+    end
+    local legsBroken = false
+    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
+    for _, key in ipairs(legKeys) do
+        local part = bodyParts[key]
+        if part and part.initialMassRatio < 0.75 then
+            legsBroken = true
+            break
+        end
+    end
+
+    if totalHealth <= 0 then
+        currentCondition = COND_DISABLED
+    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
+        currentCondition = COND_DEAD
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
+    elseif totalHealth < 400 then
+        currentCondition = COND_CRITICAL
+    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        currentCondition = COND_INJURED
+    else
+        currentCondition = COND_NORMAL
+    end
+
+    if currentCondition == COND_DEAD or currentCondition == COND_DISABLED then
+        currentBehavior = BEH_STILL
+    elseif isFalling then
+        currentBehavior = BEH_FALLING
+    elseif isSedated and currentCondition ~= COND_NORMAL then
+        currentBehavior = BEH_STILL
+    elseif currentCondition == COND_CRITICAL then
+        currentBehavior = BEH_CONVULSING
+    elseif currentCondition == COND_INJURED then
+        currentBehavior = BEH_STRUGGLING
+    elseif legsBroken then
+        currentBehavior = BEH_STILL
+    else
+        currentBehavior = BEH_STANDING
+    end
+end
+
+functi
+
+ calculateBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local viableParts = {}
+    for key, part in pairs(bodyParts) do
+        local damagePercent = 1.0 - part.baseMassRatio
+        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
+        if damagePercent > 0.02 then
+            part.isBleeding = true
+            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
+            if part.health ~= 0 then
+                local actualDrain = math.min(part.health, healthToDrain)
+                part.health = part.health - actualDrain
+                overflowPool = overflowPool + (healthToDrain - actualDrain)
+            else
+                overflowPool = overflowPool + healthToDrain
+            end
+        else
+            part.isBleeding = false
+        end
+        if part.health ~= 0 then
+            local weight = (key == "head") and 0.2 or 1.0
+            viableParts[key] = weight
+            weightSum = weightSum + weight
+        end
+    end
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(viableParts) do
+            local part = bodyParts[key]
+            part.health = math.max(0, part.health - (damagePerUnit * weight))
+        end
+    end
+end
+
+functi
+
+ calculateDrowning()
+    local head = bodyParts.head
+    if not head or head.handle == 0 then return end
+    if IsPointInWater(GetBodyTransform(head.handle).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+        if currentOxygen <= 0 then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
+            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
+        end
+    else
+        currentOxygen = math.min(100, currentOxygen + 20)
+    end
+end
+
+-- 检查函
+
+ysicalStats()
+    local tempTotal = 0
+    currentFps = GetFps()
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            part.currentMass = GetBodyMass(part.handle)
+            part.baseMassRatio = part.currentMass / part.baseMass
+            part.initialMassRatio = part.currentMass / part.initialMass
+            part.healthRatio = part.health / part.maxHealth
+            tempTotal = tempTotal + (part.health or 0)
+        end
+    end
+    totalHealth = tempTotal
+end
+
+function check
+
+iticalTrauma()
+    local head = bodyParts.head
+    if not eventHeadBroken and head.initialMassRatio < 0.99 then
+        head.health = head.health * 0.8
+        playHeadBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
+        eventHeadBroken = true
+    end
+    local torso = bodyParts.torso
+    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
+        torso.health = torso.health * 0.5
+        playTorsoBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
+        eventTorsoBroken = true
+    end
+end
+
+function check
+
+gs()
+    isResurrected = false
+    isBandaged = false
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            if HasTag(part.handle, "resurrected") then 
+                isResurrected = true 
+                RemoveTag(part.handle, "resurrected")
+            end
+            if HasTag(part.handle, "bandaged") then 
+                isBandaged = true 
+                RemoveTag(part.handle, "bandaged")
+            end
+            if HasTag(part.handle, "sedated") then 
+                isSedated = true 
+                RemoveTag(part.handle, "sedated") 
+            end
+        end
+    end
+end
+
+function check
+
+ecialStatus()
+    if isBandaged then
+        for _, part in pairs(bodyParts) do
+            if part.handle ~= 0 then
+                if part.baseMassRatio < 0.99 then
+                    part.isBandaged = true
+                    part.baseMass = GetBodyMass(part.handle)
+                    part.baseMassRatio = 1.0 
+                end
+            end
+        end
+        isBandaged = false
+    end
+    if isResurrected then
+        if currentCondition ~= COND_DEAD then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then
+                    part.health = part.maxHealth
+                    part.isBandaged = false
+                    part.baseMass = GetBodyMass(part.handle)
+                end
+            end
+        end
+        isResurrected = false
+    end
+end
+
+function check
+
+lling()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local velocity = GetBodyVelocity(torso.handle)
+        local verticalSpeed = velocity[2]
+
+        if verticalSpeed < -8 then
+            isFalling = true
+            fallTimer = fallTimer + 1
+        else
+            if isFalling and fallTimer > 5 then
+                playFallDamageEffect()
+            end
+            isFalling = false
+            fallTimer = 0
+        end
+    end
+end
+
+-- 效果函数
+functi
+
+fect()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local headTrans = GetBodyTransform(head.handle)
+        PlaySound(headsplat, headTrans.pos, 1.0)
+        Spawn("MOD/xml/organBrain.xml", headTrans)
+        drawBleedingExplosion(headTrans.pos)
+    end
+end
+
+function playTorsoBurs
+
+ffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local torsoTrans = GetBodyTransform(torso.handle)
+        PlaySound(goresplat, torsoTrans.pos, 1.0)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+        if math.random() > 0.7 then Spawn("MOD/xml/organEntrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/xml/organHeart.xml", torsoTrans) end
+        if math.random() > 0.7 then Spawn("MOD/xml/organSpine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/xml/organLung.xml", torsoTrans) end
+        drawBleedingExplosion(torsoTrans.pos)
+    end
+end
+
+function playFallDamag
+
+ffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local bodyTrans = GetBodyTransform(torso.handle)
+        local localCOM = GetBodyCenterOfMass(torso.handle)
+        local worldCOM = TransformToParentPoint(bodyTrans, localCOM)
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "High Fall" end
+        MakeHole(worldCOM, 0.2, 0.2, 0.2)
+        PlaySound(hitground, GetBodyTransform(torso.handle).pos, 1)
+        drawBleedingExplosion(worldCOM)
+        torso.health = torso.health * 0.2
+    end
+end
+
+-- 行为函数
+function handl
+
+cal kHead = 40
+    local kLeg  = 25
+
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local force = kHead / head.initialMass
+        local vel = GetBodyVelocity(head.handle)
+        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, force * standingStrength, 0)))
+    end
+
+    local lLeg = bodyParts.lLowerLeg
+    if lLeg and lLeg.handle ~= 0 then
+        local force = kLeg / lLeg.initialMass
+        local vel = GetBodyVelocity(lLeg.handle)
+        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
+    end
+
+    local rLeg = bodyParts.rLowerLeg
+    if rLeg and rLeg.handle ~= 0 then
+        local force = kLeg / rLeg.initialMass
+        local vel = GetBodyVelocity(rLeg.handle)
+        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
+    end
+end
+
+function handleStruggling()
+  
+
+local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local dependency = {
+        lLowerArm = "lArm",
+        rLowerArm = "rArm",
+        lLowerLeg = "lLeg",
+        rLowerLeg = "rLeg"}
+    for key, p in pairs(bodyParts) do
+        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
+            local parentKey = dependency[key]
+            local canStruggle = true
+            if parentKey then
+                local parent = bodyParts[parentKey]
+                if not parent or parent.initialMassRatio < 0.95 then
+                    canStruggle = false
+                end
+            end
+            if canStruggle and math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCritical()
+    
+
+cal torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local parts = {
+        bodyParts.head, bodyParts.torso, 
+        bodyParts.lArm, bodyParts.rArm, 
+        bodyParts.lLeg, bodyParts.rLeg}
+    for i = 1, #parts do
+        local p = parts[i]
+        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
+            if math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleFalling()
+    l
+
+al torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if fallscream then
+        PlayLoop(fallscream, GetBodyTransform(torso.handle).pos, 10)
+        if not tempEverPrinted then
+            tempEverPrinted = true
+            SetSoundLoopProgress(fallscream, 0)
+        end
+    end
+end
+
+-- 绘制函数
+function drawBleedingP
+
+currentFps < 40 or math.random() < 0.8 then return end
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            local intensity = 1.0 - part.baseMassRatio
+            ParticleType("smoke")
+            ParticleColor(0.3, 0.0, 0.0)
+            ParticleRadius(0.05)
+            ParticleGravity(-50)
+            ParticleDrag(1)
+            local count = math.floor(intensity * 10)
+            for i = 1, count do
+                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
+            end
+        end
+    end
+end
+
+function drawBleedingPaint()
+    if cu
+
+entFps < 40 or totalHealth < 400 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local bloodIntensity = 0.5
+                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+                local splashCount = math.random(1, 3)
+                local maxRadius = 0.6
+                for i = 1, splashCount do
+                    local angle = math.random() * 2 * math.pi
+                    local radius = math.sqrt(math.random()) * maxRadius
+                    local offsetX = math.cos(angle) * radius
+                    local offsetZ = math.sin(angle) * radius
+                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+                    local splashSize = mainSize * (math.random(3, 5) / 10)
+                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+                end
+            end
+        end
+    end
+end
+
+function drawBleedingDripping()
+    if
+
+urrentFps < 40 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local dripSize = math.random(1, 3) / 10
+                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
+            end
+        end
+    end
+end
+
+function drawBleedingExplosion(pos)
+  
+
+if currentFps < 40 then return end
+    local camTrans = GetCameraTransform()
+    local camPos = camTrans.pos
+    local baseDir = VecNormalize(VecSub(pos, camPos))
+    local rayCount = 8
+    for i = 1, rayCount do
+        local spread = 0.3
+        local scatterDir = VecNormalize(Vec(
+            baseDir[1] + (math.random() - 0.5) * spread,
+            baseDir[2] + (math.random() - 0.5) * spread,
+            baseDir[3] + (math.random() - 0.5) * spread))
+        QueryRejectShapes(allShapes)
+        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
+        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
+        if hit and shape ~= 0 then
+            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
+            local dotsPerHit = math.random(3, 6)
+            for j = 1, dotsPerHit do
+                local finalPos = VecAdd(hitPos, Vec(
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5))
+                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
+            end
+        end
+    end
+end
+
+-- 注册信息
+function syncDataToRegistry(fi
+
+not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
+    local dollId = tostring(bodyParts.torso.handle)
+    local path = "temp.goredolls." .. dollId
+    SetString(path .. ".state", currentCondition or "UNKNOWN", true)
+    SetString(path .. ".behavior", currentBehavior or "STILL", true)
+    SetString(path .. ".cause", causeOfDeath or "none", true)
+    SetFloat(path .. ".oxy", currentOxygen or 100, true)
+    SetBool(path .. ".sedated", isSedated == true, true)
+    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"), true)
+    if finalStatus then SetBool(path .. ".final", true, true) end
+    local hList, bList, cList = {}, {}, {}
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            table.insert(hList, key .. ":" .. part.health)
+            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
+            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
+            table.insert(cList, key .. ":" .. isCripple)
+        end
+    end
+    SetString(path .. ".healths", table.concat(hList, ","), true)
+    SetString(path .. ".bandages", table.concat(bList, ","), true)
+    SetString(path .. ".cripples", table.concat(cList, ","), true)
+end
+
+function server.init()
     local config = {
         head = { tag = "Head", maxH = 50 },
         torso = { tag = "Torso", maxH = 350 },
@@ -74,9 +522,6 @@
         end
     end
     standingStrength = GetFloatParam("standingStrength",1)
-    goresplat = LoadSound("MOD/ogg/goresplat.ogg")
-    headsplat = LoadSound("MOD/ogg/headsplat.ogg")
-    hitground = LoadSound("MOD/ogg/hittheground.ogg")
     if GetBoolParam("male", true) then
         criticalcough = LoadLoop("MOD/ogg/criticalcondition.ogg")
         fallscream = LoadLoop("MOD/ogg/fallscream.ogg")
@@ -86,7 +531,7 @@
     end
 end
 
-function update(dt)
+function server.update(dt)
     if currentCondition == COND_DISABLED then return end
     timerA = timerA + 1
     if timerA >= 10 then
@@ -108,7 +553,7 @@
     end
     drawBleedingParticles()
     syncDataToRegistry()
-    
+
     if currentBehavior == BEH_STANDING then handleStanding() 
     elseif currentBehavior == BEH_STRUGGLING then handleStruggling()
     elseif currentBehavior == BEH_CONVULSING then handleCritical()
@@ -118,450 +563,9 @@
     end
 end
 
--- 计算函数
-function calculateStateMachine()
-    local isAnyPartBleeding = false
-    for _, part in pairs(bodyParts) do
-        if part.isBleeding then 
-            isAnyPartBleeding = true 
-        end
-    end
-    local legsBroken = false
-    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
-    for _, key in ipairs(legKeys) do
-        local part = bodyParts[key]
-        if part and part.initialMassRatio < 0.75 then
-            legsBroken = true
-            break
-        end
-    end
-
-    if totalHealth <= 0 then
-        currentCondition = COND_DISABLED
-    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
-        currentCondition = COND_DEAD
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
-    elseif totalHealth < 400 then
-        currentCondition = COND_CRITICAL
-    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        currentCondition = COND_INJURED
-    else
-        currentCondition = COND_NORMAL
-    end
-
-    if currentCondition == COND_DEAD or currentCondition == COND_DISABLED then
-        currentBehavior = BEH_STILL
-    elseif isFalling then
-        currentBehavior = BEH_FALLING
-    elseif isSedated and currentCondition ~= COND_NORMAL then
-        currentBehavior = BEH_STILL
-    elseif currentCondition == COND_CRITICAL then
-        currentBehavior = BEH_CONVULSING
-    elseif currentCondition == COND_INJURED then
-        currentBehavior = BEH_STRUGGLING
-    elseif legsBroken then
-        currentBehavior = BEH_STILL
-    else
-        currentBehavior = BEH_STANDING
-    end
-end
-
-function calculateBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local viableParts = {}
-    for key, part in pairs(bodyParts) do
-        local damagePercent = 1.0 - part.baseMassRatio
-        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
-        if damagePercent > 0.02 then
-            part.isBleeding = true
-            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
-            if part.health > 0 then
-                local actualDrain = math.min(part.health, healthToDrain)
-                part.health = part.health - actualDrain
-                overflowPool = overflowPool + (healthToDrain - actualDrain)
-            else
-                overflowPool = overflowPool + healthToDrain
-            end
-        else
-            part.isBleeding = false
-        end
-        if part.health > 0 then
-            local weight = (key == "head") and 0.2 or 1.0
-            viableParts[key] = weight
-            weightSum = weightSum + weight
-        end
-    end
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(viableParts) do
-            local part = bodyParts[key]
-            part.health = math.max(0, part.health - (damagePerUnit * weight))
-        end
-    end
-end
-
-function calculateDrowning()
-    local head = bodyParts.head
-    if not head or head.handle == 0 then return end
-    if IsPointInWater(GetBodyTransform(head.handle).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-        if currentOxygen <= 0 then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
-            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
-        end
-    else
-        currentOxygen = math.min(100, currentOxygen + 20)
-    end
-end
-
--- 检查函数
-function checkPhysicalStats()
-    local tempTotal = 0
-    currentFps = GetFps()
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            part.currentMass = GetBodyMass(part.handle)
-            part.baseMassRatio = part.currentMass / part.baseMass
-            part.initialMassRatio = part.currentMass / part.initialMass
-            part.healthRatio = part.health / part.maxHealth
-            tempTotal = tempTotal + (part.health or 0)
-        end
-    end
-    totalHealth = tempTotal
-end
-
-function checkCriticalTrauma()
-    local head = bodyParts.head
-    if not eventHeadBroken and head.initialMassRatio < 0.99 then
-        head.health = head.health * 0.8
-        playHeadBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
-        eventHeadBroken = true
-    end
-    local torso = bodyParts.torso
-    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
-        torso.health = torso.health * 0.5
-        playTorsoBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
-        eventTorsoBroken = true
-    end
-end
-
-function checkTags()
-    isResurrected = false
-    isBandaged = false
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            if HasTag(part.handle, "resurrected") then 
-                isResurrected = true 
-                RemoveTag(part.handle, "resurrected")
-            end
-            if HasTag(part.handle, "bandaged") then 
-                isBandaged = true 
-                RemoveTag(part.handle, "bandaged")
-            end
-            if HasTag(part.handle, "sedated") then 
-                isSedated = true 
-                RemoveTag(part.handle, "sedated") 
-            end
-        end
-    end
-end
-
-function checkSpecialStatus()
-    if isBandaged then
-        for _, part in pairs(bodyParts) do
-            if part.handle ~= 0 then
-                if part.baseMassRatio < 0.99 then
-                    part.isBandaged = true
-                    part.baseMass = GetBodyMass(part.handle)
-                    part.baseMassRatio = 1.0 
-                end
-            end
-        end
-        isBandaged = false
-    end
-    if isResurrected then
-        if currentCondition ~= COND_DEAD then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then
-                    part.health = part.maxHealth
-                    part.isBandaged = false
-                    part.baseMass = GetBodyMass(part.handle)
-                end
-            end
-        end
-        isResurrected = false
-    end
-end
-
-function checkFalling()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local velocity = GetBodyVelocity(torso.handle)
-        local verticalSpeed = velocity[2]
-
-        if verticalSpeed < -8 then
-            isFalling = true
-            fallTimer = fallTimer + 1
-        else
-            if isFalling and fallTimer > 5 then
-                playFallDamageEffect()
-            end
-            isFalling = false
-            fallTimer = 0
-        end
-    end
-end
-
--- 效果函数
-function playHeadBurstEffect()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local headTrans = GetBodyTransform(head.handle)
-        PlaySound(headsplat, headTrans.pos, 1.0)
-        Spawn("MOD/xml/organBrain.xml", headTrans)
-        drawBleedingExplosion(headTrans.pos)
-    end
-end
-
-function playTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local torsoTrans = GetBodyTransform(torso.handle)
-        PlaySound(goresplat, torsoTrans.pos, 1.0)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-        if math.random() > 0.7 then Spawn("MOD/xml/organEntrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/xml/organHeart.xml", torsoTrans) end
-        if math.random() > 0.7 then Spawn("MOD/xml/organSpine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/xml/organLung.xml", torsoTrans) end
-        drawBleedingExplosion(torsoTrans.pos)
-    end
-end
-
-function playFallDamageEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local bodyTrans = GetBodyTransform(torso.handle)
-        local localCOM = GetBodyCenterOfMass(torso.handle)
-        local worldCOM = TransformToParentPoint(bodyTrans, localCOM)
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "High Fall" end
-        MakeHole(worldCOM, 0.2, 0.2, 0.2)
-        PlaySound(hitground, GetBodyTransform(torso.handle).pos, 1)
-        drawBleedingExplosion(worldCOM)
-        torso.health = torso.health * 0.2
-    end
-end
-
--- 行为函数
-function handleStanding()
-    local kHead = 40
-    local kLeg  = 25
-
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local force = kHead / head.initialMass
-        local vel = GetBodyVelocity(head.handle)
-        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, force * standingStrength, 0)))
-    end
-
-    local lLeg = bodyParts.lLowerLeg
-    if lLeg and lLeg.handle ~= 0 then
-        local force = kLeg / lLeg.initialMass
-        local vel = GetBodyVelocity(lLeg.handle)
-        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
-    end
-
-    local rLeg = bodyParts.rLowerLeg
-    if rLeg and rLeg.handle ~= 0 then
-        local force = kLeg / rLeg.initialMass
-        local vel = GetBodyVelocity(rLeg.handle)
-        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
-    end
-end
-
-function handleStruggling()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local dependency = {
-        lLowerArm = "lArm",
-        rLowerArm = "rArm",
-        lLowerLeg = "lLeg",
-        rLowerLeg = "rLeg"}
-    for key, p in pairs(bodyParts) do
-        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
-            local parentKey = dependency[key]
-            local canStruggle = true
-            if parentKey then
-                local parent = bodyParts[parentKey]
-                if not parent or parent.initialMassRatio < 0.95 then
-                    canStruggle = false
-                end
-            end
-            if canStruggle and math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCritical()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local parts = {
-        bodyParts.head, bodyParts.torso, 
-        bodyParts.lArm, bodyParts.rArm, 
-        bodyParts.lLeg, bodyParts.rLeg}
-    for i = 1, #parts do
-        local p = parts[i]
-        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
-            if math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleFalling()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if fallscream then
-        PlayLoop(fallscream, GetBodyTransform(torso.handle).pos, 10)
-        if not tempEverPrinted then
-            tempEverPrinted = true
-            SetSoundLoopProgress(fallscream, 0)
-        end
-    end
-end
-
--- 绘制函数
-function drawBleedingParticles()
-    if currentFps < 40 or math.random() < 0.8 then return end
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            local intensity = 1.0 - part.baseMassRatio
-            ParticleType("smoke")
-            ParticleColor(0.3, 0.0, 0.0)
-            ParticleRadius(0.05)
-            ParticleGravity(-50)
-            ParticleDrag(1)
-            local count = math.floor(intensity * 10)
-            for i = 1, count do
-                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
-            end
-        end
-    end
-end
-
-function drawBleedingPaint()
-    if currentFps < 40 or totalHealth < 400 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local bloodIntensity = 0.5
-                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-                local splashCount = math.random(1, 3)
-                local maxRadius = 0.6
-                for i = 1, splashCount do
-                    local angle = math.random() * 2 * math.pi
-                    local radius = math.sqrt(math.random()) * maxRadius
-                    local offsetX = math.cos(angle) * radius
-                    local offsetZ = math.sin(angle) * radius
-                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-                    local splashSize = mainSize * (math.random(3, 5) / 10)
-                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-                end
-            end
-        end
-    end
-end
-
-function drawBleedingDripping()
-    if currentFps < 40 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local dripSize = math.random(1, 3) / 10
-                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
-            end
-        end
-    end
-end
-
-function drawBleedingExplosion(pos)
-    if currentFps < 40 then return end
-    local camTrans = GetCameraTransform()
-    local camPos = camTrans.pos
-    local baseDir = VecNormalize(VecSub(pos, camPos))
-    local rayCount = 8
-    for i = 1, rayCount do
-        local spread = 0.3
-        local scatterDir = VecNormalize(Vec(
-            baseDir[1] + (math.random() - 0.5) * spread,
-            baseDir[2] + (math.random() - 0.5) * spread,
-            baseDir[3] + (math.random() - 0.5) * spread))
-        QueryRejectShapes(allShapes)
-        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
-        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
-        if hit and shape ~= 0 then
-            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
-            local dotsPerHit = math.random(3, 6)
-            for j = 1, dotsPerHit do
-                local finalPos = VecAdd(hitPos, Vec(
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5))
-                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
-            end
-        end
-    end
-end
-
--- 注册信息
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
-    local dollId = tostring(bodyParts.torso.handle)
-    local path = "temp.goredolls." .. dollId
-    SetString(path .. ".state", currentCondition or "UNKNOWN")
-    SetString(path .. ".behavior", currentBehavior or "STILL")
-    SetString(path .. ".cause", causeOfDeath or "none")
-    SetFloat(path .. ".oxy", currentOxygen or 100)
-    SetBool(path .. ".sedated", isSedated == true)
-    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"))
-    if finalStatus then SetBool(path .. ".final", true) end
-    local hList, bList, cList = {}, {}, {}
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            table.insert(hList, key .. ":" .. part.health)
-            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
-            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
-            table.insert(cList, key .. ":" .. isCripple)
-        end
-    end
-    SetString(path .. ".healths", table.concat(hList, ","))
-    SetString(path .. ".bandages", table.concat(bList, ","))
-    SetString(path .. ".cripples", table.concat(cList, ","))
-end+function client.init()
+    goresplat = LoadSound("MOD/ogg/goresplat.ogg")
+    headsplat = LoadSound("MOD/ogg/headsplat.ogg")
+    hitground = LoadSound("MOD/ogg/hittheground.ogg")
+end
+

```

---

# Migration Report: lua\gore v26.1.3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v26.1.3.lua
+++ patched/lua\gore v26.1.3.lua
@@ -1,25 +1,386 @@
-bodyParts = {}
-allShapes = {}
-ragdollState = "STANDING"
-STATE_STANDING = "STANDING"
-STATE_STRUGGLING = "STRUGGLING"
-STATE_CRITICAL = "CRITICAL"
-STATE_DEAD = "DEAD"
-STATE_DISABLED = "DISABLED"
-STATE_CRIPPLED = "CRIPPLED"
-causeOfDeath = ""
-eventHeadBroken = false
-eventTorsoBroken = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-timerA = 0
-timerB = 0
-currentOxygen = 100
-totalHealth = 1000
-currentFps = 0
-
-function init()
+#version 2
+function updatePhysicalStats()
+    local tempTotal = 0
+    currentFps = GetFps()
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            part.currentMass = GetBodyMass(part.handle)
+            part.baseMassRatio = part.currentMass / part.baseMass
+            part.initialMassRatio = part.currentMass / part.initialMass
+            part.healthRatio = part.health / part.maxHealth
+            tempTotal = tempTotal + (part.health or 0)
+        end
+    end
+    totalHealth = tempTotal
+end
+
+function checkCriticalTrauma()
+    local head = bodyParts.head
+    if not eventHeadBroken and head.initialMassRatio < 0.95 then
+        head.health = head.health * 0.8
+        playHeadBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
+        eventHeadBroken = true
+    end
+    local torso = bodyParts.torso
+    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
+        torso.health = torso.health * 0.5
+        playTorsoBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
+        eventTorsoBroken = true
+    end
+end
+
+function processBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local viableParts = {}
+    for key, part in pairs(bodyParts) do
+        local damagePercent = 1.0 - part.baseMassRatio
+        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
+        if damagePercent > 0.02 then
+            part.isBleeding = true
+            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
+            if part.health ~= 0 then
+                local actualDrain = math.min(part.health, healthToDrain)
+                part.health = part.health - actualDrain
+                overflowPool = overflowPool + (healthToDrain - actualDrain)
+            else
+                overflowPool = overflowPool + healthToDrain
+            end
+        else
+            part.isBleeding = false
+        end
+        if part.health ~= 0 then
+            local weight = (key == "head") and 0.2 or 1.0
+            viableParts[key] = weight
+            weightSum = weightSum + weight
+        end
+    end
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(viableParts) do
+            local part = bodyParts[key]
+            part.health = math.max(0, part.health - (damagePerUnit * weight))
+        end
+    end
+end
+
+function playHeadBurstEffect()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local headTrans = GetBodyTransform(head.handle)
+        PlaySound(headsplat, headTrans.pos, 1.0)
+        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
+        drawBleedingExplosion(headTrans.pos)
+    end
+end
+
+function playTorsoBurstEffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local torsoTrans = GetBodyTransform(torso.handle)
+        PlaySound(goresplat, torsoTrans.pos, 1.0)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
+        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
+        drawBleedingExplosion(torsoTrans.pos)
+    end
+end
+
+function handleStanding()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local vel = GetBodyVelocity(head.handle)
+        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.8 * headUpwardForce, 0)))
+    end
+    local lLeg = bodyParts.lLowerLeg
+    if lLeg and lLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(lLeg.handle)
+        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -1.5 * headUpwardForce, 0)))
+    end
+    local rLeg = bodyParts.rLowerLeg
+    if rLeg and rLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(rLeg.handle)
+        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -1.5 * headUpwardForce, 0)))
+    end
+end
+
+function handleStruggling()
+    local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local dependency = {
+        lLowerArm = "lArm",
+        rLowerArm = "rArm",
+        lLowerLeg = "lLeg",
+        rLowerLeg = "rLeg"}
+    for key, p in pairs(bodyParts) do
+        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
+            local parentKey = dependency[key]
+            local canStruggle = true
+            if parentKey then
+                local parent = bodyParts[parentKey]
+                if not parent or parent.initialMassRatio < 0.95 then
+                    canStruggle = false
+                end
+            end
+            if canStruggle and math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCritical()
+    local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local parts = {
+        bodyParts.head, bodyParts.torso, 
+        bodyParts.lArm, bodyParts.rArm, 
+        bodyParts.lLeg, bodyParts.rLeg}
+    for i = 1, #parts do
+        local p = parts[i]
+        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
+            if math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCrippled()
+end
+
+function handleDead()
+end
+
+function checkTags()
+    isResurrected = false
+    isBandaged = false
+    isSedated = false
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            if HasTag(part.handle, "resurrected") then 
+                isResurrected = true 
+                RemoveTag(part.handle, "resurrected")
+            end
+            if HasTag(part.handle, "bandaged") then 
+                isBandaged = true 
+                RemoveTag(part.handle, "bandaged")
+            end
+            if HasTag(part.handle, "sedated") then 
+                isSedated = true 
+                RemoveTag(part.handle, "sedated") 
+            end
+        end
+    end
+end
+
+function handleSpecialStatus()
+    if isBandaged then
+        for _, part in pairs(bodyParts) do
+            if part.handle ~= 0 then
+                if part.baseMassRatio < 0.99 then
+                    part.isBandaged = true
+                    part.baseMass = GetBodyMass(part.handle)
+                    part.baseMassRatio = 1.0 
+                end
+            end
+        end
+        isBandaged = false
+    end
+    if isResurrected then
+        if ragdollState ~= STATE_DEAD then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then
+                    part.health = part.maxHealth
+                    part.isBandaged = false
+                    part.baseMass = GetBodyMass(part.handle)
+                end
+            end
+        end
+        isResurrected = false
+    end
+end
+
+function handleDrowningLogic()
+    local head = bodyParts.head
+    if not head or head.handle == 0 then return end
+    if IsPointInWater(GetBodyTransform(head.handle).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+        if currentOxygen <= 0 then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
+            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
+        end
+    else
+        currentOxygen = math.min(100, currentOxygen + 20)
+    end
+end
+
+function drawBleedingParticles()
+    if currentFps < 40 or math.random() < 0.8 then return end
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            local intensity = 1.0 - part.baseMassRatio
+            ParticleType("smoke")
+            ParticleColor(0.3, 0.0, 0.0)
+            ParticleRadius(0.05)
+            ParticleGravity(-50)
+            ParticleDrag(1)
+            local count = math.floor(intensity * 10)
+            for i = 1, count do
+                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
+            end
+        end
+    end
+end
+
+function drawBleedingPaint()
+    if currentFps < 40 or totalHealth < 400 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local bloodIntensity = 0.5
+                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+                local splashCount = math.random(1, 3)
+                local maxRadius = 0.6
+                for i = 1, splashCount do
+                    local angle = math.random() * 2 * math.pi
+                    local radius = math.sqrt(math.random()) * maxRadius
+                    local offsetX = math.cos(angle) * radius
+                    local offsetZ = math.sin(angle) * radius
+                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+                    local splashSize = mainSize * (math.random(3, 5) / 10)
+                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+                end
+            end
+        end
+    end
+end
+
+function drawBleedingDripping()
+    if currentFps < 40 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local dripSize = math.random(1, 3) / 10
+                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
+            end
+        end
+    end
+end
+
+function drawBleedingExplosion(pos)
+    if currentFps < 40 then return end
+    local camTrans = GetCameraTransform()
+    local camPos = camTrans.pos
+    local baseDir = VecNormalize(VecSub(pos, camPos))
+    local rayCount = 8
+    for i = 1, rayCount do
+        local spread = 0.3
+        local scatterDir = VecNormalize(Vec(
+            baseDir[1] + (math.random() - 0.5) * spread,
+            baseDir[2] + (math.random() - 0.5) * spread,
+            baseDir[3] + (math.random() - 0.5) * spread))
+        QueryRejectShapes(allShapes)
+        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
+        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
+        if hit and shape ~= 0 then
+            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
+            local dotsPerHit = math.random(3, 6)
+            for j = 1, dotsPerHit do
+                local finalPos = VecAdd(hitPos, Vec(
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5))
+                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
+            end
+        end
+    end
+end
+
+function syncDataToRegistry(finalStatus)
+    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
+    local dollId = tostring(bodyParts.torso.handle)
+    local path = "temp.goredolls." .. dollId
+    SetString(path .. ".state", ragdollState or "UNKNOWN", true)
+    SetString(path .. ".cause", causeOfDeath or "none", true)
+    SetFloat(path .. ".oxy", currentOxygen or 100, true)
+    SetBool(path .. ".sedated", isSedated == true, true)
+    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"), true)
+    if finalStatus then SetBool(path .. ".final", true, true) end
+    local hList, bList, cList = {}, {}, {}
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            table.insert(hList, key .. ":" .. part.health)
+            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
+            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
+            table.insert(cList, key .. ":" .. isCripple)
+        end
+    end
+    SetString(path .. ".healths", table.concat(hList, ","), true)
+    SetString(path .. ".bandages", table.concat(bList, ","), true)
+    SetString(path .. ".cripples", table.concat(cList, ","), true)
+end
+
+function checkStateMachine()
+    local isAnyPartBleeding = false
+    for _, part in pairs(bodyParts) do
+        if part.isBleeding then 
+            isAnyPartBleeding = true 
+        end
+    end
+    local legsBroken = false
+    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
+    for _, key in ipairs(legKeys) do
+        local part = bodyParts[key]
+        if part and part.initialMassRatio < 0.75 then
+            legsBroken = true
+            break
+        end
+    end
+    if totalHealth <= 0 then
+        ragdollState = STATE_DISABLED
+        syncDataToRegistry(true)
+    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
+        ragdollState = STATE_DEAD
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
+    elseif totalHealth < 400 then
+        ragdollState = STATE_CRITICAL
+    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        ragdollState = STATE_STRUGGLING
+    elseif legsBroken then
+        ragdollState = STATE_CRIPPLED
+    else
+        ragdollState = STATE_STANDING
+    end
+end
+
+function server.init()
     local config = {
         head = { tag = "Head", maxH = 50 },
         torso = { tag = "Torso", maxH = 350 },
@@ -61,399 +422,9 @@
         end
     end
     local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local calculatedForce = 3.0 - (head.initialMass * 0.03)
-        headUpwardForce = math.max(0.5, math.min(3.0, calculatedForce))
-    else
-        if head then headUpwardForce = 1.0 end
-    end
-    criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-end
-
-function updatePhysicalStats()
-    local tempTotal = 0
-    currentFps = GetFps()
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            part.currentMass = GetBodyMass(part.handle)
-            part.baseMassRatio = part.currentMass / part.baseMass
-            part.initialMassRatio = part.currentMass / part.initialMass
-            part.healthRatio = part.health / part.maxHealth
-            tempTotal = tempTotal + (part.health or 0)
-        end
-    end
-    totalHealth = tempTotal
-end
-
-function checkCriticalTrauma()
-    local head = bodyParts.head
-    if not eventHeadBroken and head.initialMassRatio < 0.95 then
-        head.health = head.health * 0.8
-        playHeadBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
-        eventHeadBroken = true
-    end
-    local torso = bodyParts.torso
-    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
-        torso.health = torso.health * 0.5
-        playTorsoBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
-        eventTorsoBroken = true
-    end
-end
-
-function processBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local viableParts = {}
-    for key, part in pairs(bodyParts) do
-        local damagePercent = 1.0 - part.baseMassRatio
-        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
-        if damagePercent > 0.02 then
-            part.isBleeding = true
-            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
-            if part.health > 0 then
-                local actualDrain = math.min(part.health, healthToDrain)
-                part.health = part.health - actualDrain
-                overflowPool = overflowPool + (healthToDrain - actualDrain)
-            else
-                overflowPool = overflowPool + healthToDrain
-            end
-        else
-            part.isBleeding = false
-        end
-        if part.health > 0 then
-            local weight = (key == "head") and 0.2 or 1.0
-            viableParts[key] = weight
-            weightSum = weightSum + weight
-        end
-    end
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(viableParts) do
-            local part = bodyParts[key]
-            part.health = math.max(0, part.health - (damagePerUnit * weight))
-        end
-    end
-end
-
-function playHeadBurstEffect()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local headTrans = GetBodyTransform(head.handle)
-        PlaySound(headsplat, headTrans.pos, 1.0)
-        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
-        drawBleedingExplosion(headTrans.pos)
-    end
-end
-
-function playTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local torsoTrans = GetBodyTransform(torso.handle)
-        PlaySound(goresplat, torsoTrans.pos, 1.0)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
-        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
-        drawBleedingExplosion(torsoTrans.pos)
-    end
-end
-
-function handleStanding()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local vel = GetBodyVelocity(head.handle)
-        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.8 * headUpwardForce, 0)))
-    end
-    local lLeg = bodyParts.lLowerLeg
-    if lLeg and lLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(lLeg.handle)
-        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -1.5 * headUpwardForce, 0)))
-    end
-    local rLeg = bodyParts.rLowerLeg
-    if rLeg and rLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(rLeg.handle)
-        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -1.5 * headUpwardForce, 0)))
-    end
-end
-
-function handleStruggling()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local dependency = {
-        lLowerArm = "lArm",
-        rLowerArm = "rArm",
-        lLowerLeg = "lLeg",
-        rLowerLeg = "rLeg"}
-    for key, p in pairs(bodyParts) do
-        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
-            local parentKey = dependency[key]
-            local canStruggle = true
-            if parentKey then
-                local parent = bodyParts[parentKey]
-                if not parent or parent.initialMassRatio < 0.95 then
-                    canStruggle = false
-                end
-            end
-            if canStruggle and math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCritical()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local parts = {
-        bodyParts.head, bodyParts.torso, 
-        bodyParts.lArm, bodyParts.rArm, 
-        bodyParts.lLeg, bodyParts.rLeg}
-    for i = 1, #parts do
-        local p = parts[i]
-        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
-            if math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCrippled()
-end
-
-function handleDead()
-end
-
-function checkTags()
-    isResurrected = false
-    isBandaged = false
-    isSedated = false
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            if HasTag(part.handle, "resurrected") then 
-                isResurrected = true 
-                RemoveTag(part.handle, "resurrected")
-            end
-            if HasTag(part.handle, "bandaged") then 
-                isBandaged = true 
-                RemoveTag(part.handle, "bandaged")
-            end
-            if HasTag(part.handle, "sedated") then 
-                isSedated = true 
-                RemoveTag(part.handle, "sedated") 
-            end
-        end
-    end
-end
-
-function handleSpecialStatus()
-    if isBandaged then
-        for _, part in pairs(bodyParts) do
-            if part.handle ~= 0 then
-                if part.baseMassRatio < 0.99 then
-                    part.isBandaged = true
-                    part.baseMass = GetBodyMass(part.handle)
-                    part.baseMassRatio = 1.0 
-                end
-            end
-        end
-        isBandaged = false
-    end
-    if isResurrected then
-        if ragdollState ~= STATE_DEAD then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then
-                    part.health = part.maxHealth
-                    part.isBandaged = false
-                    part.baseMass = GetBodyMass(part.handle)
-                end
-            end
-        end
-        isResurrected = false
-    end
-end
-
-function handleDrowningLogic()
-    local head = bodyParts.head
-    if not head or head.handle == 0 then return end
-    if IsPointInWater(GetBodyTransform(head.handle).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-        if currentOxygen <= 0 then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
-            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
-        end
-    else
-        currentOxygen = math.min(100, currentOxygen + 20)
-    end
-end
-
-function drawBleedingParticles()
-    if currentFps < 40 or math.random() < 0.8 then return end
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            local intensity = 1.0 - part.baseMassRatio
-            ParticleType("smoke")
-            ParticleColor(0.3, 0.0, 0.0)
-            ParticleRadius(0.05)
-            ParticleGravity(-50)
-            ParticleDrag(1)
-            local count = math.floor(intensity * 10)
-            for i = 1, count do
-                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
-            end
-        end
-    end
-end
-
-function drawBleedingPaint()
-    if currentFps < 40 or totalHealth < 400 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local bloodIntensity = 0.5
-                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-                local splashCount = math.random(1, 3)
-                local maxRadius = 0.6
-                for i = 1, splashCount do
-                    local angle = math.random() * 2 * math.pi
-                    local radius = math.sqrt(math.random()) * maxRadius
-                    local offsetX = math.cos(angle) * radius
-                    local offsetZ = math.sin(angle) * radius
-                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-                    local splashSize = mainSize * (math.random(3, 5) / 10)
-                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-                end
-            end
-        end
-    end
-end
-
-function drawBleedingDripping()
-    if currentFps < 40 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local dripSize = math.random(1, 3) / 10
-                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
-            end
-        end
-    end
-end
-
-function drawBleedingExplosion(pos)
-    if currentFps < 40 then return end
-    local camTrans = GetCameraTransform()
-    local camPos = camTrans.pos
-    local baseDir = VecNormalize(VecSub(pos, camPos))
-    local rayCount = 8
-    for i = 1, rayCount do
-        local spread = 0.3
-        local scatterDir = VecNormalize(Vec(
-            baseDir[1] + (math.random() - 0.5) * spread,
-            baseDir[2] + (math.random() - 0.5) * spread,
-            baseDir[3] + (math.random() - 0.5) * spread))
-        QueryRejectShapes(allShapes)
-        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
-        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
-        if hit and shape ~= 0 then
-            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
-            local dotsPerHit = math.random(3, 6)
-            for j = 1, dotsPerHit do
-                local finalPos = VecAdd(hitPos, Vec(
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5))
-                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
-            end
-        end
-    end
-end
-
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
-    local dollId = tostring(bodyParts.torso.handle)
-    local path = "temp.goredolls." .. dollId
-    SetString(path .. ".state", ragdollState or "UNKNOWN")
-    SetString(path .. ".cause", causeOfDeath or "none")
-    SetFloat(path .. ".oxy", currentOxygen or 100)
-    SetBool(path .. ".sedated", isSedated == true)
-    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"))
-    if finalStatus then SetBool(path .. ".final", true) end
-    local hList, bList, cList = {}, {}, {}
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            table.insert(hList, key .. ":" .. part.health)
-            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
-            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
-            table.insert(cList, key .. ":" .. isCripple)
-        end
-    end
-    SetString(path .. ".healths", table.concat(hList, ","))
-    SetString(path .. ".bandages", table.concat(bList, ","))
-    SetString(path .. ".cripples", table.concat(cList, ","))
-end
-
-function checkStateMachine()
-    local isAnyPartBleeding = false
-    for _, part in pairs(bodyParts) do
-        if part.isBleeding then 
-            isAnyPartBleeding = true 
-        end
-    end
-    local legsBroken = false
-    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
-    for _, key in ipairs(legKeys) do
-        local part = bodyParts[key]
-        if part and part.initialMassRatio < 0.75 then
-            legsBroken = true
-            break
-        end
-    end
-    if totalHealth <= 0 then
-        ragdollState = STATE_DISABLED
-        syncDataToRegistry(true)
-    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
-        ragdollState = STATE_DEAD
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
-    elseif totalHealth < 400 then
-        ragdollState = STATE_CRITICAL
-    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        ragdollState = STATE_STRUGGLING
-    elseif legsBroken then
-        ragdollState = STATE_CRIPPLED
-    else
-        ragdollState = STATE_STANDING
-    end
-end
-
-function update(dt)
+end
+
+function server.update(dt)
     if ragdollState == STATE_DISABLED then return end
     timerA = timerA + 1
     if timerA >= 10 then
@@ -485,4 +456,17 @@
     elseif ragdollState == STATE_DEAD then 
         handleDead()
     end
-end+end
+
+function client.init()
+    if head and head.handle ~= 0 then
+        local calculatedForce = 3.0 - (head.initialMass * 0.03)
+        headUpwardForce = math.max(0.5, math.min(3.0, calculatedForce))
+    else
+        if head then headUpwardForce = 1.0 end
+    end
+    criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+

```

---

# Migration Report: lua\gore v26.1.5.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore v26.1.5.lua
+++ patched/lua\gore v26.1.5.lua
@@ -1,25 +1,387 @@
-bodyParts = {}
-allShapes = {}
-ragdollState = "STANDING"
-STATE_STANDING = "STANDING"
-STATE_STRUGGLING = "STRUGGLING"
-STATE_CRITICAL = "CRITICAL"
-STATE_DEAD = "DEAD"
-STATE_DISABLED = "DISABLED"
-STATE_CRIPPLED = "CRIPPLED"
-causeOfDeath = ""
-eventHeadBroken = false
-eventTorsoBroken = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-timerA = 0
-timerB = 0
-currentOxygen = 100
-totalHealth = 1000
-currentFps = 0
-
-function init()
+#version 2
+function updatePhysicalStats()
+    local tempTotal = 0
+    currentFps = GetFps()
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            part.currentMass = GetBodyMass(part.handle)
+            part.baseMassRatio = part.currentMass / part.baseMass
+            part.initialMassRatio = part.currentMass / part.initialMass
+            part.healthRatio = part.health / part.maxHealth
+            tempTotal = tempTotal + (part.health or 0)
+        end
+    end
+    totalHealth = tempTotal
+end
+
+function checkCriticalTrauma()
+    local head = bodyParts.head
+    if not eventHeadBroken and head.initialMassRatio < 0.95 then
+        head.health = head.health * 0.8
+        playHeadBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
+        eventHeadBroken = true
+    end
+    local torso = bodyParts.torso
+    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
+        torso.health = torso.health * 0.5
+        playTorsoBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
+        eventTorsoBroken = true
+    end
+end
+
+function processBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local viableParts = {}
+    for key, part in pairs(bodyParts) do
+        local damagePercent = 1.0 - part.baseMassRatio
+        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
+        if damagePercent > 0.02 then
+            part.isBleeding = true
+            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
+            if part.health ~= 0 then
+                local actualDrain = math.min(part.health, healthToDrain)
+                part.health = part.health - actualDrain
+                overflowPool = overflowPool + (healthToDrain - actualDrain)
+            else
+                overflowPool = overflowPool + healthToDrain
+            end
+        else
+            part.isBleeding = false
+        end
+        if part.health ~= 0 then
+            local weight = (key == "head") and 0.2 or 1.0
+            viableParts[key] = weight
+            weightSum = weightSum + weight
+        end
+    end
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(viableParts) do
+            local part = bodyParts[key]
+            part.health = math.max(0, part.health - (damagePerUnit * weight))
+        end
+    end
+end
+
+function playHeadBurstEffect()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local headTrans = GetBodyTransform(head.handle)
+        PlaySound(headsplat, headTrans.pos, 1.0)
+        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
+        drawBleedingExplosion(headTrans.pos)
+    end
+end
+
+function playTorsoBurstEffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local torsoTrans = GetBodyTransform(torso.handle)
+        PlaySound(goresplat, torsoTrans.pos, 1.0)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
+        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
+        drawBleedingExplosion(torsoTrans.pos)
+    end
+end
+
+function handleStanding()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local vel = GetBodyVelocity(head.handle)
+        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.5 * headUpwardForce, 0)))
+    end
+    local lLeg = bodyParts.lLowerLeg
+    if lLeg and lLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(lLeg.handle)
+        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
+    end
+    local rLeg = bodyParts.rLowerLeg
+    if rLeg and rLeg.handle ~= 0 then
+        local vel = GetBodyVelocity(rLeg.handle)
+        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
+    end
+end
+
+function handleStruggling()
+    if isSedated then return end
+    local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local dependency = {
+        lLowerArm = "lArm",
+        rLowerArm = "rArm",
+        lLowerLeg = "lLeg",
+        rLowerLeg = "rLeg"}
+    for key, p in pairs(bodyParts) do
+        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
+            local parentKey = dependency[key]
+            local canStruggle = true
+            if parentKey then
+                local parent = bodyParts[parentKey]
+                if not parent or parent.initialMassRatio < 0.95 then
+                    canStruggle = false
+                end
+            end
+            if canStruggle and math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCritical()
+    if isSedated then return end
+    local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local parts = {
+        bodyParts.head, bodyParts.torso, 
+        bodyParts.lArm, bodyParts.rArm, 
+        bodyParts.lLeg, bodyParts.rLeg}
+    for i = 1, #parts do
+        local p = parts[i]
+        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
+            if math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCrippled()
+end
+
+function handleDead()
+end
+
+function checkTags()
+    isResurrected = false
+    isBandaged = false
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            if HasTag(part.handle, "resurrected") then 
+                isResurrected = true 
+                RemoveTag(part.handle, "resurrected")
+            end
+            if HasTag(part.handle, "bandaged") then 
+                isBandaged = true 
+                RemoveTag(part.handle, "bandaged")
+            end
+            if HasTag(part.handle, "sedated") then 
+                isSedated = true 
+                RemoveTag(part.handle, "sedated") 
+            end
+        end
+    end
+end
+
+function handleSpecialStatus()
+    if isBandaged then
+        for _, part in pairs(bodyParts) do
+            if part.handle ~= 0 then
+                if part.baseMassRatio < 0.99 then
+                    part.isBandaged = true
+                    part.baseMass = GetBodyMass(part.handle)
+                    part.baseMassRatio = 1.0 
+                end
+            end
+        end
+        isBandaged = false
+    end
+    if isResurrected then
+        if ragdollState ~= STATE_DEAD then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then
+                    part.health = part.maxHealth
+                    part.isBandaged = false
+                    part.baseMass = GetBodyMass(part.handle)
+                end
+            end
+        end
+        isResurrected = false
+    end
+end
+
+function handleDrowningLogic()
+    local head = bodyParts.head
+    if not head or head.handle == 0 then return end
+    if IsPointInWater(GetBodyTransform(head.handle).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+        if currentOxygen <= 0 then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
+            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
+        end
+    else
+        currentOxygen = math.min(100, currentOxygen + 20)
+    end
+end
+
+function drawBleedingParticles()
+    if currentFps < 40 or math.random() < 0.8 then return end
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            local intensity = 1.0 - part.baseMassRatio
+            ParticleType("smoke")
+            ParticleColor(0.3, 0.0, 0.0)
+            ParticleRadius(0.05)
+            ParticleGravity(-50)
+            ParticleDrag(1)
+            local count = math.floor(intensity * 10)
+            for i = 1, count do
+                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
+            end
+        end
+    end
+end
+
+function drawBleedingPaint()
+    if currentFps < 40 or totalHealth < 400 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local bloodIntensity = 0.5
+                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+                local splashCount = math.random(1, 3)
+                local maxRadius = 0.6
+                for i = 1, splashCount do
+                    local angle = math.random() * 2 * math.pi
+                    local radius = math.sqrt(math.random()) * maxRadius
+                    local offsetX = math.cos(angle) * radius
+                    local offsetZ = math.sin(angle) * radius
+                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+                    local splashSize = mainSize * (math.random(3, 5) / 10)
+                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+                end
+            end
+        end
+    end
+end
+
+function drawBleedingDripping()
+    if currentFps < 40 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local dripSize = math.random(1, 3) / 10
+                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
+            end
+        end
+    end
+end
+
+function drawBleedingExplosion(pos)
+    if currentFps < 40 then return end
+    local camTrans = GetCameraTransform()
+    local camPos = camTrans.pos
+    local baseDir = VecNormalize(VecSub(pos, camPos))
+    local rayCount = 8
+    for i = 1, rayCount do
+        local spread = 0.3
+        local scatterDir = VecNormalize(Vec(
+            baseDir[1] + (math.random() - 0.5) * spread,
+            baseDir[2] + (math.random() - 0.5) * spread,
+            baseDir[3] + (math.random() - 0.5) * spread))
+        QueryRejectShapes(allShapes)
+        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
+        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
+        if hit and shape ~= 0 then
+            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
+            local dotsPerHit = math.random(3, 6)
+            for j = 1, dotsPerHit do
+                local finalPos = VecAdd(hitPos, Vec(
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5))
+                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
+            end
+        end
+    end
+end
+
+function syncDataToRegistry(finalStatus)
+    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
+    local dollId = tostring(bodyParts.torso.handle)
+    local path = "temp.goredolls." .. dollId
+    SetString(path .. ".state", ragdollState or "UNKNOWN", true)
+    SetString(path .. ".cause", causeOfDeath or "none", true)
+    SetFloat(path .. ".oxy", currentOxygen or 100, true)
+    SetBool(path .. ".sedated", isSedated == true, true)
+    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"), true)
+    if finalStatus then SetBool(path .. ".final", true, true) end
+    local hList, bList, cList = {}, {}, {}
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            table.insert(hList, key .. ":" .. part.health)
+            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
+            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
+            table.insert(cList, key .. ":" .. isCripple)
+        end
+    end
+    SetString(path .. ".healths", table.concat(hList, ","), true)
+    SetString(path .. ".bandages", table.concat(bList, ","), true)
+    SetString(path .. ".cripples", table.concat(cList, ","), true)
+end
+
+function checkStateMachine()
+    local isAnyPartBleeding = false
+    for _, part in pairs(bodyParts) do
+        if part.isBleeding then 
+            isAnyPartBleeding = true 
+        end
+    end
+    local legsBroken = false
+    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
+    for _, key in ipairs(legKeys) do
+        local part = bodyParts[key]
+        if part and part.initialMassRatio < 0.75 then
+            legsBroken = true
+            break
+        end
+    end
+    if totalHealth <= 0 then
+        ragdollState = STATE_DISABLED
+        syncDataToRegistry(true)
+    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
+        ragdollState = STATE_DEAD
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
+    elseif totalHealth < 400 then
+        ragdollState = STATE_CRITICAL
+    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        ragdollState = STATE_STRUGGLING
+    elseif legsBroken then
+        ragdollState = STATE_CRIPPLED
+    else
+        ragdollState = STATE_STANDING
+    end
+end
+
+function server.init()
     local config = {
         head = { tag = "Head", maxH = 50 },
         torso = { tag = "Torso", maxH = 350 },
@@ -61,400 +423,9 @@
         end
     end
     local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local calculatedForce = 3.0 - (head.initialMass * 0.03)
-        headUpwardForce = math.max(0.5, math.min(3.0, calculatedForce))
-    else
-        if head then headUpwardForce = 1.0 end
-    end
-    criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-end
-
-function updatePhysicalStats()
-    local tempTotal = 0
-    currentFps = GetFps()
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            part.currentMass = GetBodyMass(part.handle)
-            part.baseMassRatio = part.currentMass / part.baseMass
-            part.initialMassRatio = part.currentMass / part.initialMass
-            part.healthRatio = part.health / part.maxHealth
-            tempTotal = tempTotal + (part.health or 0)
-        end
-    end
-    totalHealth = tempTotal
-end
-
-function checkCriticalTrauma()
-    local head = bodyParts.head
-    if not eventHeadBroken and head.initialMassRatio < 0.95 then
-        head.health = head.health * 0.8
-        playHeadBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
-        eventHeadBroken = true
-    end
-    local torso = bodyParts.torso
-    if not eventTorsoBroken and torso.initialMassRatio < 0.9 then
-        torso.health = torso.health * 0.5
-        playTorsoBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
-        eventTorsoBroken = true
-    end
-end
-
-function processBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local viableParts = {}
-    for key, part in pairs(bodyParts) do
-        local damagePercent = 1.0 - part.baseMassRatio
-        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
-        if damagePercent > 0.02 then
-            part.isBleeding = true
-            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
-            if part.health > 0 then
-                local actualDrain = math.min(part.health, healthToDrain)
-                part.health = part.health - actualDrain
-                overflowPool = overflowPool + (healthToDrain - actualDrain)
-            else
-                overflowPool = overflowPool + healthToDrain
-            end
-        else
-            part.isBleeding = false
-        end
-        if part.health > 0 then
-            local weight = (key == "head") and 0.2 or 1.0
-            viableParts[key] = weight
-            weightSum = weightSum + weight
-        end
-    end
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(viableParts) do
-            local part = bodyParts[key]
-            part.health = math.max(0, part.health - (damagePerUnit * weight))
-        end
-    end
-end
-
-function playHeadBurstEffect()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local headTrans = GetBodyTransform(head.handle)
-        PlaySound(headsplat, headTrans.pos, 1.0)
-        Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", headTrans)
-        drawBleedingExplosion(headTrans.pos)
-    end
-end
-
-function playTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local torsoTrans = GetBodyTransform(torso.handle)
-        PlaySound(goresplat, torsoTrans.pos, 1.0)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", torsoTrans) end
-        if math.random() > 0.7 then Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", torsoTrans) end
-        drawBleedingExplosion(torsoTrans.pos)
-    end
-end
-
-function handleStanding()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local vel = GetBodyVelocity(head.handle)
-        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, 0.5 * headUpwardForce, 0)))
-    end
-    local lLeg = bodyParts.lLowerLeg
-    if lLeg and lLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(lLeg.handle)
-        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
-    end
-    local rLeg = bodyParts.rLowerLeg
-    if rLeg and rLeg.handle ~= 0 then
-        local vel = GetBodyVelocity(rLeg.handle)
-        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -1 * headUpwardForce, 0)))
-    end
-end
-
-function handleStruggling()
-    if isSedated then return end
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local dependency = {
-        lLowerArm = "lArm",
-        rLowerArm = "rArm",
-        lLowerLeg = "lLeg",
-        rLowerLeg = "rLeg"}
-    for key, p in pairs(bodyParts) do
-        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
-            local parentKey = dependency[key]
-            local canStruggle = true
-            if parentKey then
-                local parent = bodyParts[parentKey]
-                if not parent or parent.initialMassRatio < 0.95 then
-                    canStruggle = false
-                end
-            end
-            if canStruggle and math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCritical()
-    if isSedated then return end
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local parts = {
-        bodyParts.head, bodyParts.torso, 
-        bodyParts.lArm, bodyParts.rArm, 
-        bodyParts.lLeg, bodyParts.rLeg}
-    for i = 1, #parts do
-        local p = parts[i]
-        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
-            if math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCrippled()
-end
-
-function handleDead()
-end
-
-function checkTags()
-    isResurrected = false
-    isBandaged = false
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            if HasTag(part.handle, "resurrected") then 
-                isResurrected = true 
-                RemoveTag(part.handle, "resurrected")
-            end
-            if HasTag(part.handle, "bandaged") then 
-                isBandaged = true 
-                RemoveTag(part.handle, "bandaged")
-            end
-            if HasTag(part.handle, "sedated") then 
-                isSedated = true 
-                RemoveTag(part.handle, "sedated") 
-            end
-        end
-    end
-end
-
-function handleSpecialStatus()
-    if isBandaged then
-        for _, part in pairs(bodyParts) do
-            if part.handle ~= 0 then
-                if part.baseMassRatio < 0.99 then
-                    part.isBandaged = true
-                    part.baseMass = GetBodyMass(part.handle)
-                    part.baseMassRatio = 1.0 
-                end
-            end
-        end
-        isBandaged = false
-    end
-    if isResurrected then
-        if ragdollState ~= STATE_DEAD then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then
-                    part.health = part.maxHealth
-                    part.isBandaged = false
-                    part.baseMass = GetBodyMass(part.handle)
-                end
-            end
-        end
-        isResurrected = false
-    end
-end
-
-function handleDrowningLogic()
-    local head = bodyParts.head
-    if not head or head.handle == 0 then return end
-    if IsPointInWater(GetBodyTransform(head.handle).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-        if currentOxygen <= 0 then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
-            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
-        end
-    else
-        currentOxygen = math.min(100, currentOxygen + 20)
-    end
-end
-
-function drawBleedingParticles()
-    if currentFps < 40 or math.random() < 0.8 then return end
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            local intensity = 1.0 - part.baseMassRatio
-            ParticleType("smoke")
-            ParticleColor(0.3, 0.0, 0.0)
-            ParticleRadius(0.05)
-            ParticleGravity(-50)
-            ParticleDrag(1)
-            local count = math.floor(intensity * 10)
-            for i = 1, count do
-                SpawnParticle(trans.pos, Vec(0, 1, 0), 5)
-            end
-        end
-    end
-end
-
-function drawBleedingPaint()
-    if currentFps < 40 or totalHealth < 400 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local bloodIntensity = 0.5
-                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-                local splashCount = math.random(1, 3)
-                local maxRadius = 0.6
-                for i = 1, splashCount do
-                    local angle = math.random() * 2 * math.pi
-                    local radius = math.sqrt(math.random()) * maxRadius
-                    local offsetX = math.cos(angle) * radius
-                    local offsetZ = math.sin(angle) * radius
-                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-                    local splashSize = mainSize * (math.random(3, 5) / 10)
-                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-                end
-            end
-        end
-    end
-end
-
-function drawBleedingDripping()
-    if currentFps < 40 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local dripSize = math.random(1, 3) / 10
-                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
-            end
-        end
-    end
-end
-
-function drawBleedingExplosion(pos)
-    if currentFps < 40 then return end
-    local camTrans = GetCameraTransform()
-    local camPos = camTrans.pos
-    local baseDir = VecNormalize(VecSub(pos, camPos))
-    local rayCount = 8
-    for i = 1, rayCount do
-        local spread = 0.3
-        local scatterDir = VecNormalize(Vec(
-            baseDir[1] + (math.random() - 0.5) * spread,
-            baseDir[2] + (math.random() - 0.5) * spread,
-            baseDir[3] + (math.random() - 0.5) * spread))
-        QueryRejectShapes(allShapes)
-        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
-        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
-        if hit and shape ~= 0 then
-            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
-            local dotsPerHit = math.random(3, 6)
-            for j = 1, dotsPerHit do
-                local finalPos = VecAdd(hitPos, Vec(
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5))
-                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
-            end
-        end
-    end
-end
-
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
-    local dollId = tostring(bodyParts.torso.handle)
-    local path = "temp.goredolls." .. dollId
-    SetString(path .. ".state", ragdollState or "UNKNOWN")
-    SetString(path .. ".cause", causeOfDeath or "none")
-    SetFloat(path .. ".oxy", currentOxygen or 100)
-    SetBool(path .. ".sedated", isSedated == true)
-    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"))
-    if finalStatus then SetBool(path .. ".final", true) end
-    local hList, bList, cList = {}, {}, {}
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            table.insert(hList, key .. ":" .. part.health)
-            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
-            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
-            table.insert(cList, key .. ":" .. isCripple)
-        end
-    end
-    SetString(path .. ".healths", table.concat(hList, ","))
-    SetString(path .. ".bandages", table.concat(bList, ","))
-    SetString(path .. ".cripples", table.concat(cList, ","))
-end
-
-function checkStateMachine()
-    local isAnyPartBleeding = false
-    for _, part in pairs(bodyParts) do
-        if part.isBleeding then 
-            isAnyPartBleeding = true 
-        end
-    end
-    local legsBroken = false
-    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
-    for _, key in ipairs(legKeys) do
-        local part = bodyParts[key]
-        if part and part.initialMassRatio < 0.75 then
-            legsBroken = true
-            break
-        end
-    end
-    if totalHealth <= 0 then
-        ragdollState = STATE_DISABLED
-        syncDataToRegistry(true)
-    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or eventHeadBroken or eventTorsoBroken then
-        ragdollState = STATE_DEAD
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
-    elseif totalHealth < 400 then
-        ragdollState = STATE_CRITICAL
-    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        ragdollState = STATE_STRUGGLING
-    elseif legsBroken then
-        ragdollState = STATE_CRIPPLED
-    else
-        ragdollState = STATE_STANDING
-    end
-end
-
-function update(dt)
+end
+
+function server.update(dt)
     if ragdollState == STATE_DISABLED then return end
     timerA = timerA + 1
     if timerA >= 10 then
@@ -486,4 +457,17 @@
     elseif ragdollState == STATE_DEAD then 
         handleDead()
     end
-end+end
+
+function client.init()
+    if head and head.handle ~= 0 then
+        local calculatedForce = 3.0 - (head.initialMass * 0.03)
+        headUpwardForce = math.max(0.5, math.min(3.0, calculatedForce))
+    else
+        if head then headUpwardForce = 1.0 end
+    end
+    criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+

```

---

# Migration Report: lua\gore.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\gore.lua
+++ patched/lua\gore.lua
@@ -1,39 +1,535 @@
--- GYM Ragdoll Framework v26.2.21 (Public Version 2)
--- Made by GLaDOSS, Yulun & Please Pick a Name
--- Programming assisted by Gemini 3
--- Vibe coding is the best programming method in the world
-
-bodyParts = {}
-allShapes = {}
-COND_NORMAL = "NORMAL"
-COND_INJURED = "INJURED"
-COND_CRITICAL = "CRITICAL"
-COND_DEAD = "DEAD"
-COND_DISABLED = "DISABLED"
-BEH_STANDING = "STANDING"
-BEH_STRUGGLING = "STRUGGLING"
-BEH_CONVULSING = "CONVULSING"
-BEH_STILL = "STILL"
-BEH_FALLING = "FALLING"
-currentCondition = COND_NORMAL
-currentBehavior = BEH_STANDING
-causeOfDeath = ""
-isFatalTrauma = false
-isResurrected = false
-isBandaged = false
-isSedated = false
-isFalling = false
-timerA = 0
-timerB = 0
-currentOxygen = 100
-totalHealth = 1000
-currentFps = 0
-fallTimer = 0
-standingStrength = 1
-neckJoint = 0
-pref_fpsThreshold = 40
-
-function init()
+#version 2
+calculateStateMachine()
+    local isAnyPartBleeding = false
+    for _, part in pairs(bodyParts) do
+        if part.isBleeding then 
+            isAnyPartBleeding = true 
+        end
+    end
+    local legsBroken = false
+    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
+    for _, key in ipairs(legKeys) do
+        local part = bodyParts[key]
+        if part and part.initialMassRatio < 0.75 then
+            legsBroken = true
+            break
+        end
+    end
+
+    if totalHealth <= 0 then
+        currentCondition = COND_DISABLED
+    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or isFatalTrauma then
+        currentCondition = COND_DEAD
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
+    elseif totalHealth < 400 then
+        currentCondition = COND_CRITICAL
+    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
+        currentCondition = COND_INJURED
+    else
+        currentCondition = COND_NORMAL
+    end
+
+    if currentCondition == COND_DEAD or currentCondition == COND_DISABLED then
+        currentBehavior = BEH_STILL
+    elseif isFalling then
+        currentBehavior = BEH_FALLING
+    elseif isSedated and currentCondition ~= COND_NORMAL then
+        currentBehavior = BEH_STILL
+    elseif currentCondition == COND_CRITICAL then
+        currentBehavior = BEH_CONVULSING
+    elseif currentCondition == COND_INJURED then
+        currentBehavior = BEH_STRUGGLING
+    elseif legsBroken then
+        currentBehavior = BEH_STILL
+    else
+        currentBehavior = BEH_STANDING
+    end
+end
+
+functi
+
+ calculateBleeding()
+    local baseMultiplier = 0.05
+    local overflowPool = 0
+    local weightSum = 0
+    local viableParts = {}
+    for key, part in pairs(bodyParts) do
+        local damagePercent = 1.0 - part.baseMassRatio
+        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
+        if damagePercent > 0.02 then
+            part.isBleeding = true
+            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
+            if part.health ~= 0 then
+                local actualDrain = math.min(part.health, healthToDrain)
+                part.health = part.health - actualDrain
+                overflowPool = overflowPool + (healthToDrain - actualDrain)
+            else
+                overflowPool = overflowPool + healthToDrain
+            end
+        else
+            part.isBleeding = false
+        end
+        if part.health ~= 0 then
+            local weight = (key == "head") and 0.2 or 1.0
+            viableParts[key] = weight
+            weightSum = weightSum + weight
+        end
+    end
+    if overflowPool > 0 and weightSum ~= 0 then
+        local damagePerUnit = overflowPool / weightSum
+        for key, weight in pairs(viableParts) do
+            local part = bodyParts[key]
+            part.health = math.max(0, part.health - (damagePerUnit * weight))
+        end
+    end
+end
+
+functi
+
+ calculateDrowning()
+    local head = bodyParts.head
+    if not head or head.handle == 0 then return end
+    if IsPointInWater(GetBodyTransform(head.handle).pos) then
+        currentOxygen = math.max(0, currentOxygen - 5)
+        if currentOxygen <= 0 then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
+            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
+        end
+    else
+        currentOxygen = math.min(100, currentOxygen + 20)
+    end
+end
+
+-- 检查函
+
+ysicalStats()
+    local tempTotal = 0
+    if bodyParts.head then tempTotal = tempTotal + (bodyParts.head.health or 0) end
+    if bodyParts.torso then tempTotal = tempTotal + (bodyParts.torso.health or 0) end
+    for key, part in pairs(bodyParts) do
+        if key ~= "head" and key ~= "torso" then
+            if part.handle ~= 0 then
+                part.currentMass = GetBodyMass(part.handle)
+                part.baseMassRatio = part.currentMass / part.baseMass
+                part.initialMassRatio = part.currentMass / part.initialMass
+                part.healthRatio = part.health / part.maxHealth
+                tempTotal = tempTotal + (part.health or 0)
+            end
+        end
+    end
+    totalHealth = tempTotal
+end
+
+function check
+
+rePhysicalStats()
+    local coreKeys = {"head", "torso"}
+    for _, key in ipairs(coreKeys) do
+        local part = bodyParts[key]
+        if part and part.handle ~= 0 then
+            part.currentMass = GetBodyMass(part.handle)
+            part.baseMassRatio = part.currentMass / part.baseMass
+            part.initialMassRatio = part.currentMass / part.initialMass
+            part.healthRatio = part.health / part.maxHealth
+        end
+    end
+end
+
+function check
+
+iticalTrauma()
+    local head = bodyParts.head
+    if not isFatalTrauma and head.initialMassRatio < 0.99 then
+        head.health = head.health * 0.8
+        playHeadBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
+        isFatalTrauma = true
+    end
+    local torso = bodyParts.torso
+    if not isFatalTrauma and torso.initialMassRatio < 0.8 then
+        torso.health = torso.health * 0.5
+        playTorsoBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
+        isFatalTrauma = true
+    end
+    if not isFatalTrauma and neckJoint ~= 0 and IsJointBroken(neckJoint) then
+        if head then head.health = head.health * 0.8 end
+        playNeckBurstEffect() 
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Neck Trauma" end
+        isFatalTrauma = true
+    end
+end
+
+function check
+
+gs()
+    isResurrected = false
+    isBandaged = false
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            if HasTag(part.handle, "resurrected") then 
+                isResurrected = true 
+                RemoveTag(part.handle, "resurrected")
+            end
+            if HasTag(part.handle, "bandaged") then 
+                isBandaged = true 
+                RemoveTag(part.handle, "bandaged")
+            end
+            if HasTag(part.handle, "sedated") then 
+                isSedated = true 
+                RemoveTag(part.handle, "sedated") 
+            end
+        end
+    end
+end
+
+function check
+
+ecialStatus()
+    if isBandaged then
+        for _, part in pairs(bodyParts) do
+            if part.handle ~= 0 then
+                if part.baseMassRatio < 0.99 then
+                    part.isBandaged = true
+                    part.baseMass = GetBodyMass(part.handle)
+                    part.baseMassRatio = 1.0 
+                end
+            end
+        end
+        isBandaged = false
+    end
+    if isResurrected then
+        if currentCondition ~= COND_DEAD then
+            for _, part in pairs(bodyParts) do
+                if part.handle ~= 0 then
+                    part.health = part.maxHealth
+                    part.isBandaged = false
+                    part.baseMass = GetBodyMass(part.handle)
+                end
+            end
+        end
+        isResurrected = false
+    end
+end
+
+function check
+
+lling()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local velocity = GetBodyVelocity(torso.handle)
+        local verticalSpeed = velocity[2]
+
+        if verticalSpeed < -8 then
+            isFalling = true
+            fallTimer = fallTimer + 1
+        else
+            if isFalling and fallTimer > 5 then
+                playFallDamageEffect()
+            end
+            isFalling = false
+            fallTimer = 0
+        end
+    end
+end
+
+-- 效果函数
+functi
+
+fect()
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local headTrans = GetBodyTransform(head.handle)
+        PlaySound(headsplat, headTrans.pos, 1.0)
+        Spawn("MOD/xml/organBrain.xml", headTrans)
+        drawBleedingExplosion(headTrans.pos)
+    end
+end
+
+function playTorsoBurs
+
+ffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local torsoTrans = GetBodyTransform(torso.handle)
+        PlaySound(goresplat, torsoTrans.pos, 1.0)
+        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
+        if math.random() > 0.7 then Spawn("MOD/xml/organEntrails.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/xml/organHeart.xml", torsoTrans) end
+        if math.random() > 0.7 then Spawn("MOD/xml/organSpine.xml", torsoTrans) end
+        if math.random() > 0.5 then Spawn("MOD/xml/organLung.xml", torsoTrans) end
+        drawBleedingExplosion(torsoTrans.pos)
+    end
+end
+
+function playNeckBurst
+
+fect()
+        local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local headTrans = GetBodyTransform(head.handle)
+        PlaySound(headsplat, headTrans.pos, 1.0)
+        drawBleedingExplosion(headTrans.pos)
+    end
+end
+
+function playFallDamag
+
+ffect()
+    local torso = bodyParts.torso
+    if torso and torso.handle ~= 0 then
+        local bodyTrans = GetBodyTransform(torso.handle)
+        local localCOM = GetBodyCenterOfMass(torso.handle)
+        local worldCOM = TransformToParentPoint(bodyTrans, localCOM)
+        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "High Fall" end
+        MakeHole(worldCOM, 0.2, 0.2, 0.2)
+        PlaySound(hitground, GetBodyTransform(torso.handle).pos, 1)
+        drawBleedingExplosion(worldCOM)
+        torso.health = torso.health * 0.2
+    end
+end
+
+-- 行为函数
+function handl
+
+cal kHead = 40
+    local kLeg  = 25
+
+    local head = bodyParts.head
+    if head and head.handle ~= 0 then
+        local force = kHead / head.initialMass
+        local vel = GetBodyVelocity(head.handle)
+        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, force * standingStrength, 0)))
+    end
+
+    local lLeg = bodyParts.lLowerLeg
+    if lLeg and lLeg.handle ~= 0 then
+        local force = kLeg / lLeg.initialMass
+        local vel = GetBodyVelocity(lLeg.handle)
+        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
+    end
+
+    local rLeg = bodyParts.rLowerLeg
+    if rLeg and rLeg.handle ~= 0 then
+        local force = kLeg / rLeg.initialMass
+        local vel = GetBodyVelocity(rLeg.handle)
+        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
+    end
+end
+
+function handleStruggling()
+  
+
+local torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local dependency = {
+        lLowerArm = "lArm",
+        rLowerArm = "rArm",
+        lLowerLeg = "lLeg",
+        rLowerLeg = "rLeg"}
+    for key, p in pairs(bodyParts) do
+        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
+            local parentKey = dependency[key]
+            local canStruggle = true
+            if parentKey then
+                local parent = bodyParts[parentKey]
+                if not parent or parent.initialMassRatio < 0.95 then
+                    canStruggle = false
+                end
+            end
+            if canStruggle and math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleCritical()
+    
+
+cal torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
+    local parts = {
+        bodyParts.head, bodyParts.torso, 
+        bodyParts.lArm, bodyParts.rArm, 
+        bodyParts.lLeg, bodyParts.rLeg}
+    for i = 1, #parts do
+        local p = parts[i]
+        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
+            if math.random() < 0.05 then
+                local randVec = Vec(
+                    (math.random() - 0.5) * 50, 
+                    (math.random() - 0.2) * 50, 
+                    (math.random() - 0.5) * 50)
+                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
+            end
+        end
+    end
+end
+
+function handleFalling()
+    l
+
+al torso = bodyParts.torso
+    if not torso or torso.handle == 0 then return end
+    if fallscream then
+        PlayLoop(fallscream, GetBodyTransform(torso.handle).pos, 10)
+        if not tempEverPrinted then
+            tempEverPrinted = true
+            SetSoundLoopProgress(fallscream, 0)
+        end
+    end
+end
+
+-- 绘制函数
+function drawBleedingP
+
+currentFps < pref_fpsThreshold or math.random() < 0.3 then return end 
+
+    for _, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health > 0 and part.baseMassRatio > 0.05 then
+            local trans = GetBodyTransform(part.handle)
+            local intensity = 1.0 - part.baseMassRatio
+            local effectiveIntensity = math.max(intensity, 0.1)
+
+            ParticleReset()
+            ParticleType("spark")
+            ParticleRadius(0.04 + (0.04 * effectiveIntensity), 0.01)
+            ParticleStretch(2.5)
+            ParticleSticky(0.2)
+            ParticleGravity(-12)
+            
+            local w = math.random(7, 10) / 10
+            ParticleColor(0.4 * w, 0.0, 0.0)
+            
+            local count = math.floor(effectiveIntensity * 25)
+            for i = 1, count do
+                local dir = Vec(
+                    (math.random() - 0.5) * 0.8, 
+                    0.8 + (math.random() * 0.4), 
+                    (math.random() - 0.5) * 0.8
+                )
+                local vel = VecScale(dir, 2.5 * effectiveIntensity) 
+                SpawnParticle(trans.pos, vel, math.random(0.8, 1.5))
+            end
+        end
+    end
+end
+
+function drawBleedingPaint()
+    if cu
+
+entFps < pref_fpsThreshold or totalHealth < 400 then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local bloodIntensity = 0.5
+                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
+                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
+                local splashCount = math.random(1, 3)
+                local maxRadius = 0.6
+                for i = 1, splashCount do
+                    local angle = math.random() * 2 * math.pi
+                    local radius = math.sqrt(math.random()) * maxRadius
+                    local offsetX = math.cos(angle) * radius
+                    local offsetZ = math.sin(angle) * radius
+                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
+                    local splashSize = mainSize * (math.random(3, 5) / 10)
+                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
+                end
+            end
+        end
+    end
+end
+
+function drawBleedingDripping()
+    if
+
+urrentFps < pref_fpsThreshold then return end
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 and part.isBleeding and part.health ~= 0 then
+            local trans = GetBodyTransform(part.handle)
+            QueryRejectShapes(allShapes)
+            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
+            if hit and shape ~= 0 then
+                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
+                local dripSize = math.random(1, 3) / 10
+                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
+            end
+        end
+    end
+end
+
+function drawBleedingExplosion(pos)
+  
+
+if currentFps < pref_fpsThreshold then return end
+    local camTrans = GetCameraTransform()
+    local camPos = camTrans.pos
+    local baseDir = VecNormalize(VecSub(pos, camPos))
+    local rayCount = 8
+    for i = 1, rayCount do
+        local spread = 0.3
+        local scatterDir = VecNormalize(Vec(
+            baseDir[1] + (math.random() - 0.5) * spread,
+            baseDir[2] + (math.random() - 0.5) * spread,
+            baseDir[3] + (math.random() - 0.5) * spread))
+        QueryRejectShapes(allShapes)
+        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
+        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
+        if hit and shape ~= 0 then
+            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
+            local dotsPerHit = math.random(3, 6)
+            for j = 1, dotsPerHit do
+                local finalPos = VecAdd(hitPos, Vec(
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5,
+                    (math.random() - 0.5) * 0.5))
+                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
+            end
+        end
+    end
+end
+
+-- 注册信息
+function syncDataToRegistry(fi
+
+not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
+    local dollId = tostring(bodyParts.torso.handle)
+    local path = "temp.goredolls." .. dollId
+    SetString(path .. ".state", currentCondition or "UNKNOWN", true)
+    SetString(path .. ".behavior", currentBehavior or "STILL", true)
+    SetString(path .. ".cause", causeOfDeath or "none", true)
+    SetFloat(path .. ".oxy", currentOxygen or 100, true)
+    SetBool(path .. ".sedated", isSedated == true, true)
+    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"), true)
+    if finalStatus then SetBool(path .. ".final", true, true) end
+    local hList, bList, cList = {}, {}, {}
+    for key, part in pairs(bodyParts) do
+        if part.handle ~= 0 then
+            table.insert(hList, key .. ":" .. part.health)
+            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
+            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
+            table.insert(cList, key .. ":" .. isCripple)
+        end
+    end
+    SetString(path .. ".healths", table.concat(hList, ","), true)
+    SetString(path .. ".bandages", table.concat(bList, ","), true)
+    SetString(path .. ".cripples", table.concat(cList, ","), true)
+end
+
+function server.init()
     local config = {
         head = { tag = "Head", maxH = 50 },
         torso = { tag = "Torso", maxH = 350 },
@@ -76,9 +572,6 @@
         end
     end
     standingStrength = GetFloatParam("standingStrength",1)
-    goresplat = LoadSound("MOD/ogg/goresplat.ogg")
-    headsplat = LoadSound("MOD/ogg/headsplat.ogg")
-    hitground = LoadSound("MOD/ogg/hittheground.ogg")
     if GetBoolParam("male", true) then
         criticalcough = LoadLoop("MOD/ogg/criticalcondition.ogg")
         fallscream = LoadLoop("MOD/ogg/fallscream.ogg")
@@ -89,7 +582,7 @@
     pref_fpsThreshold = GetInt("savegame.mod.fps_threshold") or 40
 end
 
-function update(dt)
+function server.update(dt)
     if currentCondition == COND_DISABLED then return end
     currentFps = GetFps()
     timerA = timerA + 1
@@ -126,495 +619,9 @@
     end
 end
 
--- 计算函数
-function calculateStateMachine()
-    local isAnyPartBleeding = false
-    for _, part in pairs(bodyParts) do
-        if part.isBleeding then 
-            isAnyPartBleeding = true 
-        end
-    end
-    local legsBroken = false
-    local legKeys = {"lLeg", "lLowerLeg", "rLeg", "rLowerLeg"}
-    for _, key in ipairs(legKeys) do
-        local part = bodyParts[key]
-        if part and part.initialMassRatio < 0.75 then
-            legsBroken = true
-            break
-        end
-    end
-
-    if totalHealth <= 0 then
-        currentCondition = COND_DISABLED
-    elseif (bodyParts.head and bodyParts.head.health <= 0) or (bodyParts.torso and bodyParts.torso.health <= 0) or totalHealth < 100 or isFatalTrauma then
-        currentCondition = COND_DEAD
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Blood Loss" end
-    elseif totalHealth < 400 then
-        currentCondition = COND_CRITICAL
-    elseif totalHealth < 700 or currentOxygen < 100 or isAnyPartBleeding then
-        currentCondition = COND_INJURED
-    else
-        currentCondition = COND_NORMAL
-    end
-
-    if currentCondition == COND_DEAD or currentCondition == COND_DISABLED then
-        currentBehavior = BEH_STILL
-    elseif isFalling then
-        currentBehavior = BEH_FALLING
-    elseif isSedated and currentCondition ~= COND_NORMAL then
-        currentBehavior = BEH_STILL
-    elseif currentCondition == COND_CRITICAL then
-        currentBehavior = BEH_CONVULSING
-    elseif currentCondition == COND_INJURED then
-        currentBehavior = BEH_STRUGGLING
-    elseif legsBroken then
-        currentBehavior = BEH_STILL
-    else
-        currentBehavior = BEH_STANDING
-    end
-end
-
-function calculateBleeding()
-    local baseMultiplier = 0.05
-    local overflowPool = 0
-    local weightSum = 0
-    local viableParts = {}
-    for key, part in pairs(bodyParts) do
-        local damagePercent = 1.0 - part.baseMassRatio
-        if part.isBandaged and damagePercent > 0.02 then part.isBandaged = false end
-        if damagePercent > 0.02 then
-            part.isBleeding = true
-            local healthToDrain = damagePercent * part.maxHealth * baseMultiplier
-            if part.health > 0 then
-                local actualDrain = math.min(part.health, healthToDrain)
-                part.health = part.health - actualDrain
-                overflowPool = overflowPool + (healthToDrain - actualDrain)
-            else
-                overflowPool = overflowPool + healthToDrain
-            end
-        else
-            part.isBleeding = false
-        end
-        if part.health > 0 then
-            local weight = (key == "head") and 0.2 or 1.0
-            viableParts[key] = weight
-            weightSum = weightSum + weight
-        end
-    end
-    if overflowPool > 0 and weightSum > 0 then
-        local damagePerUnit = overflowPool / weightSum
-        for key, weight in pairs(viableParts) do
-            local part = bodyParts[key]
-            part.health = math.max(0, part.health - (damagePerUnit * weight))
-        end
-    end
-end
-
-function calculateDrowning()
-    local head = bodyParts.head
-    if not head or head.handle == 0 then return end
-    if IsPointInWater(GetBodyTransform(head.handle).pos) then
-        currentOxygen = math.max(0, currentOxygen - 5)
-        if currentOxygen <= 0 then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then part.health = math.max(0, part.health - 30) end end
-            if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Drowned" end
-        end
-    else
-        currentOxygen = math.min(100, currentOxygen + 20)
-    end
-end
-
--- 检查函数
-function checkPhysicalStats()
-    local tempTotal = 0
-    if bodyParts.head then tempTotal = tempTotal + (bodyParts.head.health or 0) end
-    if bodyParts.torso then tempTotal = tempTotal + (bodyParts.torso.health or 0) end
-    for key, part in pairs(bodyParts) do
-        if key ~= "head" and key ~= "torso" then
-            if part.handle ~= 0 then
-                part.currentMass = GetBodyMass(part.handle)
-                part.baseMassRatio = part.currentMass / part.baseMass
-                part.initialMassRatio = part.currentMass / part.initialMass
-                part.healthRatio = part.health / part.maxHealth
-                tempTotal = tempTotal + (part.health or 0)
-            end
-        end
-    end
-    totalHealth = tempTotal
-end
-
-function checkCorePhysicalStats()
-    local coreKeys = {"head", "torso"}
-    for _, key in ipairs(coreKeys) do
-        local part = bodyParts[key]
-        if part and part.handle ~= 0 then
-            part.currentMass = GetBodyMass(part.handle)
-            part.baseMassRatio = part.currentMass / part.baseMass
-            part.initialMassRatio = part.currentMass / part.initialMass
-            part.healthRatio = part.health / part.maxHealth
-        end
-    end
-end
-
-function checkCriticalTrauma()
-    local head = bodyParts.head
-    if not isFatalTrauma and head.initialMassRatio < 0.99 then
-        head.health = head.health * 0.8
-        playHeadBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Head Trauma" end
-        isFatalTrauma = true
-    end
-    local torso = bodyParts.torso
-    if not isFatalTrauma and torso.initialMassRatio < 0.8 then
-        torso.health = torso.health * 0.5
-        playTorsoBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Torso Trauma" end
-        isFatalTrauma = true
-    end
-    if not isFatalTrauma and neckJoint ~= 0 and IsJointBroken(neckJoint) then
-        if head then head.health = head.health * 0.8 end
-        playNeckBurstEffect() 
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "Neck Trauma" end
-        isFatalTrauma = true
-    end
-end
-
-function checkTags()
-    isResurrected = false
-    isBandaged = false
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            if HasTag(part.handle, "resurrected") then 
-                isResurrected = true 
-                RemoveTag(part.handle, "resurrected")
-            end
-            if HasTag(part.handle, "bandaged") then 
-                isBandaged = true 
-                RemoveTag(part.handle, "bandaged")
-            end
-            if HasTag(part.handle, "sedated") then 
-                isSedated = true 
-                RemoveTag(part.handle, "sedated") 
-            end
-        end
-    end
-end
-
-function checkSpecialStatus()
-    if isBandaged then
-        for _, part in pairs(bodyParts) do
-            if part.handle ~= 0 then
-                if part.baseMassRatio < 0.99 then
-                    part.isBandaged = true
-                    part.baseMass = GetBodyMass(part.handle)
-                    part.baseMassRatio = 1.0 
-                end
-            end
-        end
-        isBandaged = false
-    end
-    if isResurrected then
-        if currentCondition ~= COND_DEAD then
-            for _, part in pairs(bodyParts) do
-                if part.handle ~= 0 then
-                    part.health = part.maxHealth
-                    part.isBandaged = false
-                    part.baseMass = GetBodyMass(part.handle)
-                end
-            end
-        end
-        isResurrected = false
-    end
-end
-
-function checkFalling()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local velocity = GetBodyVelocity(torso.handle)
-        local verticalSpeed = velocity[2]
-
-        if verticalSpeed < -8 then
-            isFalling = true
-            fallTimer = fallTimer + 1
-        else
-            if isFalling and fallTimer > 5 then
-                playFallDamageEffect()
-            end
-            isFalling = false
-            fallTimer = 0
-        end
-    end
-end
-
--- 效果函数
-function playHeadBurstEffect()
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local headTrans = GetBodyTransform(head.handle)
-        PlaySound(headsplat, headTrans.pos, 1.0)
-        Spawn("MOD/xml/organBrain.xml", headTrans)
-        drawBleedingExplosion(headTrans.pos)
-    end
-end
-
-function playTorsoBurstEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local torsoTrans = GetBodyTransform(torso.handle)
-        PlaySound(goresplat, torsoTrans.pos, 1.0)
-        torsoTrans.pos = VecAdd(torsoTrans.pos, TransformToParentVec(torsoTrans, Vec(0, -0.3, -0.2)))
-        if math.random() > 0.7 then Spawn("MOD/xml/organEntrails.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/xml/organHeart.xml", torsoTrans) end
-        if math.random() > 0.7 then Spawn("MOD/xml/organSpine.xml", torsoTrans) end
-        if math.random() > 0.5 then Spawn("MOD/xml/organLung.xml", torsoTrans) end
-        drawBleedingExplosion(torsoTrans.pos)
-    end
-end
-
-function playNeckBurstEffect()
-        local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local headTrans = GetBodyTransform(head.handle)
-        PlaySound(headsplat, headTrans.pos, 1.0)
-        drawBleedingExplosion(headTrans.pos)
-    end
-end
-
-function playFallDamageEffect()
-    local torso = bodyParts.torso
-    if torso and torso.handle ~= 0 then
-        local bodyTrans = GetBodyTransform(torso.handle)
-        local localCOM = GetBodyCenterOfMass(torso.handle)
-        local worldCOM = TransformToParentPoint(bodyTrans, localCOM)
-        if causeOfDeath == "" or causeOfDeath == "none" then causeOfDeath = "High Fall" end
-        MakeHole(worldCOM, 0.2, 0.2, 0.2)
-        PlaySound(hitground, GetBodyTransform(torso.handle).pos, 1)
-        drawBleedingExplosion(worldCOM)
-        torso.health = torso.health * 0.2
-    end
-end
-
--- 行为函数
-function handleStanding()
-    local kHead = 40
-    local kLeg  = 25
-
-    local head = bodyParts.head
-    if head and head.handle ~= 0 then
-        local force = kHead / head.initialMass
-        local vel = GetBodyVelocity(head.handle)
-        SetBodyVelocity(head.handle, VecAdd(vel, Vec(0, force * standingStrength, 0)))
-    end
-
-    local lLeg = bodyParts.lLowerLeg
-    if lLeg and lLeg.handle ~= 0 then
-        local force = kLeg / lLeg.initialMass
-        local vel = GetBodyVelocity(lLeg.handle)
-        SetBodyVelocity(lLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
-    end
-
-    local rLeg = bodyParts.rLowerLeg
-    if rLeg and rLeg.handle ~= 0 then
-        local force = kLeg / rLeg.initialMass
-        local vel = GetBodyVelocity(rLeg.handle)
-        SetBodyVelocity(rLeg.handle, VecAdd(vel, Vec(0, -force * standingStrength, 0)))
-    end
-end
-
-function handleStruggling()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local dependency = {
-        lLowerArm = "lArm",
-        rLowerArm = "rArm",
-        lLowerLeg = "lLeg",
-        rLowerLeg = "rLeg"}
-    for key, p in pairs(bodyParts) do
-        if p.handle ~= 0 and p.initialMassRatio > 0.95 and key ~= "torso" and key ~= "head" then
-            local parentKey = dependency[key]
-            local canStruggle = true
-            if parentKey then
-                local parent = bodyParts[parentKey]
-                if not parent or parent.initialMassRatio < 0.95 then
-                    canStruggle = false
-                end
-            end
-            if canStruggle and math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleCritical()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if criticalcough then PlayLoop(criticalcough, GetBodyTransform(torso.handle).pos) end
-    local parts = {
-        bodyParts.head, bodyParts.torso, 
-        bodyParts.lArm, bodyParts.rArm, 
-        bodyParts.lLeg, bodyParts.rLeg}
-    for i = 1, #parts do
-        local p = parts[i]
-        if p and p.handle ~= 0 and p.initialMassRatio > 0.8 then
-            if math.random() < 0.05 then
-                local randVec = Vec(
-                    (math.random() - 0.5) * 50, 
-                    (math.random() - 0.2) * 50, 
-                    (math.random() - 0.5) * 50)
-                ApplyBodyImpulse(p.handle, GetBodyTransform(p.handle).pos, randVec)
-            end
-        end
-    end
-end
-
-function handleFalling()
-    local torso = bodyParts.torso
-    if not torso or torso.handle == 0 then return end
-    if fallscream then
-        PlayLoop(fallscream, GetBodyTransform(torso.handle).pos, 10)
-        if not tempEverPrinted then
-            tempEverPrinted = true
-            SetSoundLoopProgress(fallscream, 0)
-        end
-    end
-end
-
--- 绘制函数
-function drawBleedingParticles()
-    if currentFps < pref_fpsThreshold or math.random() < 0.3 then return end 
-
-    for _, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 and part.baseMassRatio > 0.05 then
-            local trans = GetBodyTransform(part.handle)
-            local intensity = 1.0 - part.baseMassRatio
-            local effectiveIntensity = math.max(intensity, 0.1)
-
-            ParticleReset()
-            ParticleType("spark")
-            ParticleRadius(0.04 + (0.04 * effectiveIntensity), 0.01)
-            ParticleStretch(2.5)
-            ParticleSticky(0.2)
-            ParticleGravity(-12)
-            
-            local w = math.random(7, 10) / 10
-            ParticleColor(0.4 * w, 0.0, 0.0)
-            
-            local count = math.floor(effectiveIntensity * 25)
-            for i = 1, count do
-                local dir = Vec(
-                    (math.random() - 0.5) * 0.8, 
-                    0.8 + (math.random() * 0.4), 
-                    (math.random() - 0.5) * 0.8
-                )
-                local vel = VecScale(dir, 2.5 * effectiveIntensity) 
-                SpawnParticle(trans.pos, vel, math.random(0.8, 1.5))
-            end
-        end
-    end
-end
-
-function drawBleedingPaint()
-    if currentFps < pref_fpsThreshold or totalHealth < 400 then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local bloodIntensity = 0.5
-                local mainSize = (math.random(6, 10) / 10) * bloodIntensity
-                PaintRGBA(centerPos, mainSize, 0.25, 0.0, 0.0, 0.8, 1.0)
-                local splashCount = math.random(1, 3)
-                local maxRadius = 0.6
-                for i = 1, splashCount do
-                    local angle = math.random() * 2 * math.pi
-                    local radius = math.sqrt(math.random()) * maxRadius
-                    local offsetX = math.cos(angle) * radius
-                    local offsetZ = math.sin(angle) * radius
-                    local splashPos = VecAdd(centerPos, Vec(offsetX, 0, offsetZ))
-                    local splashSize = mainSize * (math.random(3, 5) / 10)
-                    PaintRGBA(splashPos, splashSize, 0.22, 0.0, 0.0, 0.6, 1.0)
-                end
-            end
-        end
-    end
-end
-
-function drawBleedingDripping()
-    if currentFps < pref_fpsThreshold then return end
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 and part.isBleeding and part.health > 0 then
-            local trans = GetBodyTransform(part.handle)
-            QueryRejectShapes(allShapes)
-            local hit, dist, normal, shape = QueryRaycast(trans.pos, Vec(0, -1, 0), 2.0)
-            if hit and shape ~= 0 then
-                local centerPos = VecAdd(trans.pos, VecScale(Vec(0, -1, 0), dist))
-                local dripSize = math.random(1, 3) / 10
-                PaintRGBA(centerPos, dripSize, 0.3, 0.0, 0.0, 0.95, 1.0)
-            end
-        end
-    end
-end
-
-function drawBleedingExplosion(pos)
-    if currentFps < pref_fpsThreshold then return end
-    local camTrans = GetCameraTransform()
-    local camPos = camTrans.pos
-    local baseDir = VecNormalize(VecSub(pos, camPos))
-    local rayCount = 8
-    for i = 1, rayCount do
-        local spread = 0.3
-        local scatterDir = VecNormalize(Vec(
-            baseDir[1] + (math.random() - 0.5) * spread,
-            baseDir[2] + (math.random() - 0.5) * spread,
-            baseDir[3] + (math.random() - 0.5) * spread))
-        QueryRejectShapes(allShapes)
-        local rayStart = VecAdd(pos, VecScale(scatterDir, 0.2))
-        local hit, dist, normal, shape = QueryRaycast(rayStart, scatterDir, 8.0)
-        if hit and shape ~= 0 then
-            local hitPos = VecAdd(rayStart, VecScale(scatterDir, dist))
-            local dotsPerHit = math.random(3, 6)
-            for j = 1, dotsPerHit do
-                local finalPos = VecAdd(hitPos, Vec(
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5,
-                    (math.random() - 0.5) * 0.5))
-                PaintRGBA(finalPos, 0.2, 0.3, 0, 0, 1, 1)
-            end
-        end
-    end
-end
-
--- 注册信息
-function syncDataToRegistry(finalStatus)
-    if not bodyParts or not bodyParts.torso or bodyParts.torso.handle == 0 then return end
-    local dollId = tostring(bodyParts.torso.handle)
-    local path = "temp.goredolls." .. dollId
-    SetString(path .. ".state", currentCondition or "UNKNOWN")
-    SetString(path .. ".behavior", currentBehavior or "STILL")
-    SetString(path .. ".cause", causeOfDeath or "none")
-    SetFloat(path .. ".oxy", currentOxygen or 100)
-    SetBool(path .. ".sedated", isSedated == true)
-    SetFloat(path .. ".update", GetFloat("temp.goredollsClock"))
-    if finalStatus then SetBool(path .. ".final", true) end
-    local hList, bList, cList = {}, {}, {}
-    for key, part in pairs(bodyParts) do
-        if part.handle ~= 0 then
-            table.insert(hList, key .. ":" .. part.health)
-            table.insert(bList, key .. ":" .. (part.isBandaged and "true" or "false"))
-            local isCripple = (part.initialMassRatio < 0.75) and "true" or "false"
-            table.insert(cList, key .. ":" .. isCripple)
-        end
-    end
-    SetString(path .. ".healths", table.concat(hList, ","))
-    SetString(path .. ".bandages", table.concat(bList, ","))
-    SetString(path .. ".cripples", table.concat(cList, ","))
-end+function client.init()
+    goresplat = LoadSound("MOD/ogg/goresplat.ogg")
+    headsplat = LoadSound("MOD/ogg/headsplat.ogg")
+    hitground = LoadSound("MOD/ogg/hittheground.ogg")
+end
+

```

---

# Migration Report: lua\main v26.1.2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\main v26.1.2.lua
+++ patched/lua\main v26.1.2.lua
@@ -1,20 +1,4 @@
-C_GREEN  = {r=0, g=1, b=0}
-C_YELLOW = {r=1, g=1, b=0}
-C_ORANGE = {r=1, g=0.5, b=0}
-C_RED    = {r=1, g=0, b=0}
-C_DARK   = {r=0.3, g=0, b=0}
-C_BLACK  = {r=0.1, g=0.1, b=0.1}
-C_BLUE   = {r=0.2, g=0.5, b=1}
-HEAD_SIZE = 30
-BODY_WIDTH = 38
-BODY_HEIGHT = 60
-ARM_WIDTH = 18
-
-showGoreUI = true
-displayTimer = 0
-lastData = nil
-uiAlpha = 0
-
+#version 2
 function lerpColor(c1, c2, t)
     return { r = c1.r + (c2.r - c1.r) * t, g = c1.g + (c2.g - c1.g) * t, b = c1.b + (c2.b - c1.b) * t }
 end
@@ -41,7 +25,7 @@
     UiPush()
         UiColor(color.r, color.g, color.b, alpha)
         UiRect(w, h)
-        if isCrippled and health > 0 then
+        if isCrippled and health ~= 0 then
             UiPush()
                 UiColor(0, 0, 0, 0.8 * alpha)
                 local lineH = 3
@@ -85,39 +69,6 @@
         for k, v in string.gmatch(bStr, "([^,:]+):([^,]+)") do if v == "true" then data.bandagedParts[k] = true end end
     end
     return data
-end
-
-function update(dt)
-    if InputPressed("h") then
-        showGoreUI = not showGoreUI
-    end
-
-    local cam = GetPlayerCameraTransform()
-    local hit, _, _, shape = QueryRaycast(cam.pos, TransformToParentVec(cam, Vec(0, 0, -1)), 7)
-    local lookingAtTarget = false
-
-    if hit and shape ~= 0 then
-        local b = GetShapeBody(shape)
-        local id = tonumber(GetTagValue(b, "goreTorsoLookup")) or 0
-        if id ~= 0 then
-            local data = fetchTargetData("temp.goredolls."..id)
-            if data then 
-                lastData = data
-                displayTimer = 2
-                lookingAtTarget = true
-            end
-        end
-    end
-
-    if lookingAtTarget then
-        uiAlpha = math.min(1, uiAlpha + dt * 4)
-    elseif displayTimer > 0 then
-        displayTimer = displayTimer - dt
-        uiAlpha = math.max(0, displayTimer / 2)
-    else
-        uiAlpha = 0
-        lastData = nil
-    end
 end
 
 function renderUI(data, alpha)
@@ -206,7 +157,41 @@
     UiPop()
 end
 
-function draw(dt)
+function server.update(dt)
+    local cam = GetPlayerCameraTransform(playerId)
+    local hit, _, _, shape = QueryRaycast(cam.pos, TransformToParentVec(cam, Vec(0, 0, -1)), 7)
+    local lookingAtTarget = false
+    if hit and shape ~= 0 then
+        local b = GetShapeBody(shape)
+        local id = tonumber(GetTagValue(b, "goreTorsoLookup")) or 0
+        if id ~= 0 then
+            local data = fetchTargetData("temp.goredolls."..id)
+            if data then 
+                lastData = data
+                displayTimer = 2
+                lookingAtTarget = true
+            end
+        end
+    end
+    if lookingAtTarget then
+        uiAlpha = math.min(1, uiAlpha + dt * 4)
+    elseif displayTimer ~= 0 then
+        displayTimer = displayTimer - dt
+        uiAlpha = math.max(0, displayTimer / 2)
+    else
+        uiAlpha = 0
+        lastData = nil
+    end
+end
+
+function client.update(dt)
+    if InputPressed("h") then
+        showGoreUI = not showGoreUI
+    end
+end
+
+function client.draw()
     if not showGoreUI or not lastData or uiAlpha <= 0 then return end
     renderUI(lastData, uiAlpha)
-end+end
+

```

---

# Migration Report: lua\main v26.1.3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\main v26.1.3.lua
+++ patched/lua\main v26.1.3.lua
@@ -1,20 +1,4 @@
-C_GREEN  = {r=0, g=1, b=0}
-C_YELLOW = {r=1, g=1, b=0}
-C_ORANGE = {r=1, g=0.5, b=0}
-C_RED    = {r=1, g=0, b=0}
-C_DARK   = {r=0.3, g=0, b=0}
-C_BLACK  = {r=0.1, g=0.1, b=0.1}
-C_BLUE   = {r=0.2, g=0.5, b=1}
-HEAD_SIZE = 30
-BODY_WIDTH = 38
-BODY_HEIGHT = 60
-ARM_WIDTH = 18
-
-showGoreUI = true
-displayTimer = 0
-lastData = nil
-uiAlpha = 0
-
+#version 2
 function lerpColor(c1, c2, t)
     return { r = c1.r + (c2.r - c1.r) * t, g = c1.g + (c2.g - c1.g) * t, b = c1.b + (c2.b - c1.b) * t }
 end
@@ -41,7 +25,7 @@
     UiPush()
         UiColor(color.r, color.g, color.b, alpha)
         UiRect(w, h)
-        if isCrippled and health > 0 then
+        if isCrippled and health ~= 0 then
             UiPush()
                 UiColor(0, 0, 0, 0.8 * alpha)
                 local lineH = 3
@@ -96,11 +80,13 @@
     return data
 end
 function update(dt)
-    if InputPressed("h") then
+    if InputPress
+
+d("h") then
         showGoreUI = not showGoreUI
     end
 
-    local cam = GetPlayerCameraTransform()
+    local cam = GetPlayerCameraTransform(playerId)
     local hit, _, _, shape = QueryRaycast(cam.pos, TransformToParentVec(cam, Vec(0, 0, -1)), 7)
     local lookingAtTarget = false
 
@@ -119,7 +105,7 @@
 
     if lookingAtTarget then
         uiAlpha = math.min(1, uiAlpha + dt * 4)
-    elseif displayTimer > 0 then
+    elseif displayTimer ~= 0 then
         displayTimer = displayTimer - dt
         uiAlpha = math.max(0, displayTimer / 2)
     else
@@ -129,7 +115,9 @@
 end
 
 function renderUI(data, alpha)
-    local currentTotal = 0
+    l
+
+al currentTotal = 0
     for _, v in pairs(data.currentHealth) do currentTotal = currentTotal + v end
     
     local displayState = "NORMAL"
@@ -215,6 +203,9 @@
 end
 
 function draw(dt)
-    if not showGoreUI or not lastData or uiAlpha <= 0 then return end
+    if not showGor
+
+I or not lastData or uiAlpha <= 0 then return end
     renderUI(lastData, uiAlpha)
-end+end
+

```

---

# Migration Report: lua\main v26.1.4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\main v26.1.4.lua
+++ patched/lua\main v26.1.4.lua
@@ -1,76 +1,8 @@
-C_GREEN  = {r=0, g=1, b=0}
-C_YELLOW = {r=1, g=1, b=0}
-C_ORANGE = {r=1, g=0.5, b=0}
-C_RED    = {r=1, g=0, b=0}
-C_DARK   = {r=0.3, g=0, b=0}
-C_BLACK  = {r=0.1, g=0.1, b=0.1}
-C_BLUE   = {r=0.2, g=0.5, b=1}
-HEAD_SIZE = 30
-BODY_WIDTH = 38
-BODY_HEIGHT = 60
-ARM_WIDTH = 18
+#version 2
 local medicalTools = {
     bandages = { snd = LoadSound("MOD/snd/bandage.ogg"), tag = "bandaged", color = {0, 1, 0, 0.5} },
     resurrect = { snd = LoadSound("MOD/snd/resurrect.ogg"), tag = "resurrected", color = {0, 0, 1, 0.5} },
     sedatives = { snd = LoadSound("MOD/snd/sedative.ogg"), tag = "sedated", color = {1, 1, 1, 0.5} }}
-showGoreUI = true
-displayTimer = 0
-lastData = nil
-uiAlpha = 0
-
-function init()
-    local toolNames = { bandages = "Bandages", resurrect = "Resurrect", sedatives = "Sedatives" }
-    for id, name in pairs(toolNames) do
-        RegisterTool(id, name, "MOD/vox/" .. id .. ".vox",5)
-        SetBool("game.tool." .. id .. ".enabled", true)
-    end
-end
-
-function update(dt)
-    if InputPressed("h") then showGoreUI = not showGoreUI end
-
-    local currentTool = GetString("game.player.tool")
-    local toolConfig = medicalTools[currentTool]
-    
-    local cam = GetPlayerCameraTransform()
-    local dir = TransformToParentVec(cam, Vec(0, 0, -1))
-    local hit, dist, normal, shape = QueryRaycast(cam.pos, dir, 7)
-    
-    local lookingAtTarget = false
-
-    if hit and shape ~= 0 then
-        local b = GetShapeBody(shape)
-        
-        local lookupId = tonumber(GetTagValue(b, "goreTorsoLookup")) or 0
-        if lookupId ~= 0 then
-            local data = fetchTargetData("temp.goredolls."..lookupId)
-            if data then 
-                lastData = data
-                displayTimer = 2
-                lookingAtTarget = true
-            end
-        end
-
-        if toolConfig then
-            if HasTag(b, "bodypart") or HasTag(shape, "bodypart") then
-                if GetBool("game.player.canusetool") and InputPressed("lmb") then
-                    SetTag(b, toolConfig.tag)
-                    PlaySound(toolConfig.snd)
-                end
-            end
-        end
-    end
-
-    if lookingAtTarget then
-        uiAlpha = math.min(1, uiAlpha + dt * 4)
-    elseif displayTimer > 0 then
-        displayTimer = displayTimer - dt
-        uiAlpha = math.max(0, displayTimer / 2)
-    else
-        uiAlpha = 0
-        lastData = nil
-    end
-end
 
 function fetchTargetData(path)
     if not HasKey(path .. ".state") then return nil end
@@ -118,7 +50,7 @@
     UiPush()
         UiColor(color.r, color.g, color.b, alpha)
         UiRect(w, h)
-        if isCrippled and health > 0 then
+        if isCrippled and health ~= 0 then
             UiPush()
                 UiColor(0, 0, 0, 0.8 * alpha)
                 local lineH = 3
@@ -227,7 +159,62 @@
     UiPop()
 end
 
-function draw(dt)
+function server.init()
+    local toolNames = { bandages = "Bandages", resurrect = "Resurrect", sedatives = "Sedatives" }
+    for id, name in pairs(toolNames) do
+        RegisterTool(id, name, "MOD/vox/" .. id .. ".vox",5)
+        SetBool("game.tool." .. id .. ".enabled", true, true)
+    end
+end
+
+function client.update(dt)
+    if InputPressed("h") then showGoreUI = not showGoreUI end
+
+    local currentTool = GetString("game.player.tool")
+    local toolConfig = medicalTools[currentTool]
+
+    local cam = GetPlayerCameraTransform(playerId)
+    local dir = TransformToParentVec(cam, Vec(0, 0, -1))
+    local hit, dist, normal, shape = QueryRaycast(cam.pos, dir, 7)
+
+    local lookingAtTarget = false
+
+    if hit and shape ~= 0 then
+        local b = GetShapeBody(shape)
+
+        local lookupId = tonumber(GetTagValue(b, "goreTorsoLookup")) or 0
+        if lookupId ~= 0 then
+            local data = fetchTargetData("temp.goredolls."..lookupId)
+            if data then 
+                lastData = data
+                displayTimer = 2
+                lookingAtTarget = true
+            end
+        end
+
+        if toolConfig then
+            if HasTag(b, "bodypart") or HasTag(shape, "bodypart") then
+                if GetBool("game.player.canusetool") and InputPressed("lmb") then
+                    SetTag(b, toolConfig.tag)
+                    PlaySound(toolConfig.snd)
+                end
+            end
+        end
+    end
+
+    if lookingAtTarget then
+        uiAlpha = math.min(1, uiAlpha + dt * 4)
+    elseif displayTimer ~= 0 then
+        displayTimer = displayTimer - dt
+        uiAlpha = math.max(0, displayTimer / 2)
+    else
+        uiAlpha = 0
+        lastData = nil
+    end
+end
+
+function client.draw()
     if not showGoreUI or not lastData or uiAlpha <= 0 then return end
     renderUI(lastData, uiAlpha)
-end+end
+

```

---

# Migration Report: lua\toolQuickerSpawner.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/lua\toolQuickerSpawner.lua
+++ patched/lua\toolQuickerSpawner.lua
@@ -1,26 +1,31 @@
-function init()
-	counter = 0
-	checkPath = "local-gym-ragdoll-framework"
-	totalCount = #ListKeys("spawn."..checkPath)
-	checkData = {}
+#version 2
+function server.init()
+    counter = 0
+    checkPath = "local-gym-ragdoll-framework"
+    totalCount = #ListKeys("spawn."..checkPath)
+    checkData = {}
 end
 
-function tick()
-	DebugWatch("check spawn", checkData[1])
-	DebugWatch("spawn #", checkData[2])
-	DebugWatch("name", checkData[3])
-	DebugWatch("path", checkData[4])
-	DebugWatch("progress", checkData[5])
-	if InputPressed("p") or InputPressed("o") then
-		counter = counter + (InputValue("p") - InputValue("o"))*(InputDown("shift") and 10 or 1)
-		counter = math.max(0, math.min(counter, totalCount))
-		local tempCheckSpawn = "spawn."..checkPath.."."..counter
-		local spawnPath = GetString(tempCheckSpawn..".path")
-		checkData[1] = checkPath
-		checkData[2] = counter
-		checkData[3] = GetString(tempCheckSpawn)
-		checkData[4] = spawnPath
-		checkData[5] = counter.."/"..totalCount
-		Spawn(spawnPath, TransformToParentTransform(GetPlayerTransform(), Transform(Vec(0, 0.5, -2.5))), false, false)
-	end
-end+function server.tick(dt)
+    DebugWatch("check spawn", checkData[1])
+    DebugWatch("spawn #", checkData[2])
+    DebugWatch("name", checkData[3])
+    DebugWatch("path", checkData[4])
+    DebugWatch("progress", checkData[5])
+end
+
+function client.tick(dt)
+    if InputPressed("p") or InputPressed("o") then
+    	counter = counter + (InputValue("p") - InputValue("o"))*(InputDown("shift") and 10 or 1)
+    	counter = math.max(0, math.min(counter, totalCount))
+    	local tempCheckSpawn = "spawn."..checkPath.."."..counter
+    	local spawnPath = GetString(tempCheckSpawn..".path")
+    	checkData[1] = checkPath
+    	checkData[2] = counter
+    	checkData[3] = GetString(tempCheckSpawn)
+    	checkData[4] = spawnPath
+    	checkData[5] = counter.."/"..totalCount
+    	Spawn(spawnPath, TransformToParentTransform(GetPlayerTransform(playerId), Transform(Vec(0, 0.5, -2.5))), false, false)
+    end
+end
+

```

---

# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,135 +1,4 @@
-C_GREEN  = {r=0, g=1, b=0}
-C_YELLOW = {r=1, g=1, b=0}
-C_ORANGE = {r=1, g=0.5, b=0}
-C_RED    = {r=1, g=0, b=0}
-C_DARK   = {r=0.3, g=0, b=0}
-C_BLACK  = {r=0.1, g=0.1, b=0.1}
-C_BLUE   = {r=0.2, g=0.5, b=1}
-HEAD_SIZE = 30
-BODY_WIDTH = 38
-BODY_HEIGHT = 60
-ARM_WIDTH = 18
-medicalTools = {
-    bandages = { snd = LoadSound("MOD/ogg/bandage.ogg"), tag = "bandaged", color = {0, 1, 0, 0.5} },
-    resurrect = { snd = LoadSound("MOD/ogg/resurrect.ogg"), tag = "resurrected", color = {0, 0, 1, 0.5} },
-    sedatives = { snd = LoadSound("MOD/ogg/sedative.ogg"), tag = "sedated", color = {1, 1, 1, 0.5} }}
-showGoreUI = true
-displayTimer = 0
-lastData = nil
-uiAlpha = 0
-use_timer = 0.4
-use_value = 0
-use_offset = Vec(0, -0.2, 0)
-
-function init()
-    local toolNames = { bandages = "Bandages", resurrect = "Resurrect", sedatives = "Sedatives" }
-    for id, name in pairs(toolNames) do
-        RegisterTool(id, name, "MOD/vox/" .. id .. ".vox",5)
-        SetBool("game.tool." .. id .. ".enabled", true)
-    end
-end
-
-function update(dt)
-    if InputPressed("h") then showGoreUI = not showGoreUI end
-
-    local currentTool = GetString("game.player.tool")
-    local toolConfig = medicalTools[currentTool]
-    
-    if use_value > 0 then
-        use_value = math.max(0, use_value - dt / use_timer)
-    end
-
-    if toolConfig then
-        local currentPos = VecLerp(Vec(0, 0, 0), use_offset, use_value)
-        local currentRot = QuatEuler(use_value * -15, 0, 0)
-        SetToolTransform(Transform(currentPos, currentRot))
-    end
-
-    local cam = GetPlayerCameraTransform()
-    local dir = TransformToParentVec(cam, Vec(0, 0, -1))
-    local hit, dist, normal, shape = QueryRaycast(cam.pos, dir, 7)
-    
-    local lookingAtTarget = false
-
-    if hit and shape ~= 0 then
-        local b = GetShapeBody(shape)
-        local lookupId = tonumber(GetTagValue(b, "goreTorsoLookup")) or 0
-        
-        if lookupId ~= 0 then
-            local data = fetchTargetData("temp.goredolls."..lookupId)
-            if data then 
-                lastData = data
-                displayTimer = 2
-                lookingAtTarget = true
-            end
-        end
-
-        if toolConfig then
-            if HasTag(b, "bodypart") or HasTag(shape, "bodypart") or lookupId ~= 0 then
-                local c = toolConfig.color or {1, 1, 1}
-                
-                DrawBodyOutline(b, c[1], c[2], c[3], 1.0)
-
-                if GetBool("game.player.canusetool") and InputPressed("lmb") then
-                    use_value = 1.0
-                    SetTag(b, toolConfig.tag)
-                    PlaySound(toolConfig.snd)
-                end
-            end
-        end
-    end
-
-    if lookingAtTarget then
-        uiAlpha = math.min(1, uiAlpha + dt * 4)
-    elseif displayTimer > 0 then
-        displayTimer = displayTimer - dt
-        uiAlpha = math.max(0, displayTimer / 2)
-    else
-        uiAlpha = 0
-        lastData = nil
-    end
-end
-
-function tick(dt)
-    local currentTool = GetString("game.player.tool")
-    local toolConfig = medicalTools[currentTool]
-    
-    if use_value > 0 then
-        use_value = math.max(0, use_value - dt / use_timer)
-    end
-
-    if toolConfig then
-        local currentPos = VecLerp(Vec(0, 0, 0), use_offset, use_value)
-        local currentRot = QuatEuler(use_value * -15, 0, 0)
-        SetToolTransform(Transform(currentPos, currentRot))
-    end
-
-    local cam = GetPlayerCameraTransform()
-    local dir = TransformToParentVec(cam, Vec(0, 0, -1))
-    local hit, dist, normal, shape = QueryRaycast(cam.pos, dir, 5)
-
-    if hit and shape ~= 0 and toolConfig then
-        local b = GetShapeBody(shape)
-        local lookupId = GetTagValue(b, "goreTorsoLookup")
-        
-        if HasTag(b, "bodypart") or HasTag(shape, "bodypart") or lookupId ~= "" then
-            local c = toolConfig.color or {1, 1, 1}
-            DrawShapeOutline(shape, c[1], c[2], c[3], 0.8)
-
-            if GetBool("game.player.canusetool") and InputPressed("lmb") then
-                use_value = 1.0 
-                SetTag(b, toolConfig.tag)
-                PlaySound(toolConfig.snd)
-            end
-        end
-    end
-end
-
-function draw(dt)
-    if not showGoreUI or not lastData or uiAlpha <= 0 then return end
-    renderUI(lastData, uiAlpha)
-end
-
+#version 2
 function fetchTargetData(path)
     if not HasKey(path .. ".state") then return nil end
     local data = {
@@ -177,7 +46,7 @@
     UiPush()
         UiColor(color.r, color.g, color.b, alpha)
         UiRect(w, h)
-        if isCrippled and health > 0 then
+        if isCrippled and health ~= 0 then
             UiPush()
                 UiColor(0, 0, 0, 0.8 * alpha)
                 local lineH = 3
@@ -290,5 +159,111 @@
     UiPop()
 end
 
-
-
+function server.init()
+    local toolNames = { bandages = "Bandages", resurrect = "Resurrect", sedatives = "Sedatives" }
+    for id, name in pairs(toolNames) do
+        RegisterTool(id, name, "MOD/vox/" .. id .. ".vox",5)
+        SetBool("game.tool." .. id .. ".enabled", true, true)
+    end
+end
+
+function server.tick(dt)
+    local currentTool = GetString("game.player.tool")
+    local toolConfig = medicalTools[currentTool]
+    if use_value ~= 0 then
+        use_value = math.max(0, use_value - dt / use_timer)
+    end
+    if toolConfig then
+        local currentPos = VecLerp(Vec(0, 0, 0), use_offset, use_value)
+        local currentRot = QuatEuler(use_value * -15, 0, 0)
+        SetToolTransform(Transform(currentPos, currentRot))
+    end
+    local cam = GetPlayerCameraTransform(playerId)
+    local dir = TransformToParentVec(cam, Vec(0, 0, -1))
+    local hit, dist, normal, shape = QueryRaycast(cam.pos, dir, 5)
+end
+
+function client.tick(dt)
+    if hit and shape ~= 0 and toolConfig then
+        local b = GetShapeBody(shape)
+        local lookupId = GetTagValue(b, "goreTorsoLookup")
+
+        if HasTag(b, "bodypart") or HasTag(shape, "bodypart") or lookupId ~= "" then
+            local c = toolConfig.color or {1, 1, 1}
+            DrawShapeOutline(shape, c[1], c[2], c[3], 0.8)
+
+            if GetBool("game.player.canusetool") and InputPressed("lmb") then
+                use_value = 1.0 
+                SetTag(b, toolConfig.tag)
+                PlaySound(toolConfig.snd)
+            end
+        end
+    end
+end
+
+function client.update(dt)
+    if InputPressed("h") then showGoreUI = not showGoreUI end
+
+    local currentTool = GetString("game.player.tool")
+    local toolConfig = medicalTools[currentTool]
+
+    if use_value ~= 0 then
+        use_value = math.max(0, use_value - dt / use_timer)
+    end
+
+    if toolConfig then
+        local currentPos = VecLerp(Vec(0, 0, 0), use_offset, use_value)
+        local currentRot = QuatEuler(use_value * -15, 0, 0)
+        SetToolTransform(Transform(currentPos, currentRot))
+    end
+
+    local cam = GetPlayerCameraTransform(playerId)
+    local dir = TransformToParentVec(cam, Vec(0, 0, -1))
+    local hit, dist, normal, shape = QueryRaycast(cam.pos, dir, 7)
+
+    local lookingAtTarget = false
+
+    if hit and shape ~= 0 then
+        local b = GetShapeBody(shape)
+        local lookupId = tonumber(GetTagValue(b, "goreTorsoLookup")) or 0
+
+        if lookupId ~= 0 then
+            local data = fetchTargetData("temp.goredolls."..lookupId)
+            if data then 
+                lastData = data
+                displayTimer = 2
+                lookingAtTarget = true
+            end
+        end
+
+        if toolConfig then
+            if HasTag(b, "bodypart") or HasTag(shape, "bodypart") or lookupId ~= 0 then
+                local c = toolConfig.color or {1, 1, 1}
+
+                DrawBodyOutline(b, c[1], c[2], c[3], 1.0)
+
+                if GetBool("game.player.canusetool") and InputPressed("lmb") then
+                    use_value = 1.0
+                    SetTag(b, toolConfig.tag)
+                    PlaySound(toolConfig.snd)
+                end
+            end
+        end
+    end
+
+    if lookingAtTarget then
+        uiAlpha = math.min(1, uiAlpha + dt * 4)
+    elseif displayTimer ~= 0 then
+        displayTimer = displayTimer - dt
+        uiAlpha = math.max(0, displayTimer / 2)
+    else
+        uiAlpha = 0
+        lastData = nil
+    end
+end
+
+function client.draw()
+    if not showGoreUI or not lastData or uiAlpha <= 0 then return end
+    renderUI(lastData, uiAlpha)
+end
+

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
@@ -1,46 +1,4 @@
--- options.lua
-
-function init()
-	-- Initialize default values in the registry
-	if not HasKey("savegame.mod.fps_threshold") then
-		SetInt("savegame.mod.fps_threshold", 40)
-	end
-	if not HasKey("savegame.mod.particle_multiplier") then
-		SetFloat("savegame.mod.particle_multiplier", 1.0)
-	end
-end
-
-function draw()
-	UiPush()
-		UiFont("regular.ttf", 26)
-		UiAlign("center middle")
-		UiTranslate(UiCenter(), 200)
-		
-		-- Header
-		UiPush()
-			UiFont("bold.ttf", 44)
-			UiText("GYM RAGDOLL FRAMEWORK SETTINGS")
-		UiPop()
-		
-		UiTranslate(0, 120)
-
-		-- Setting 1: FPS Threshold
-		local fpsVal = GetInt("savegame.mod.fps_threshold")
-		drawStandardSlider("Disable Blood Effect Below", fpsVal, 0, 120, function(v)
-			SetInt("savegame.mod.fps_threshold", math.floor(v))
-		end, " FPS")
-		
-		UiTranslate(0, 150)
-
-		-- Setting 2: Particle Density
-		--local densityVal = GetFloat("savegame.mod.particle_multiplier")
-		--drawStandardSlider("Blood Particle Density", densityVal, 0.1, 5.0, function(v)
-		--	SetFloat("savegame.mod.particle_multiplier", v)
-		--end, "x", "%.1f")
-
-	UiPop()
-end
-
+#version 2
 function drawStandardSlider(label, currentVal, minVal, maxVal, saveFunc, unit, format)
 	UiPush()
 		-- 1. 文字标签居中显示
@@ -78,4 +36,45 @@
 			end
 		UiPop()
 	UiPop()
-end+end
+
+function server.init()
+    if not HasKey("savegame.mod.fps_threshold") then
+    	SetInt("savegame.mod.fps_threshold", 40, true)
+    end
+    if not HasKey("savegame.mod.particle_multiplier") then
+    	SetFloat("savegame.mod.particle_multiplier", 1.0, true)
+    end
+end
+
+function client.draw()
+    UiPush()
+    	UiFont("regular.ttf", 26)
+    	UiAlign("center middle")
+    	UiTranslate(UiCenter(), 200)
+
+    	-- Header
+    	UiPush()
+    		UiFont("bold.ttf", 44)
+    		UiText("GYM RAGDOLL FRAMEWORK SETTINGS")
+    	UiPop()
+
+    	UiTranslate(0, 120)
+
+    	-- Setting 1: FPS Threshold
+    	local fpsVal = GetInt("savegame.mod.fps_threshold")
+    	drawStandardSlider("Disable Blood Effect Below", fpsVal, 0, 120, function(v)
+    		SetInt("savegame.mod.fps_threshold", math.floor(v), true)
+    	end, " FPS")
+
+    	UiTranslate(0, 150)
+
+    	-- Setting 2: Particle Density
+    	--local densityVal = GetFloat("savegame.mod.particle_multiplier")
+    	--drawStandardSlider("Blood Particle Density", densityVal, 0.1, 5.0, function(v)
+    	--	SetFloat("savegame.mod.particle_multiplier", v, true)
+    	--end, "x", "%.1f")
+
+    UiPop()
+end
+

```
