# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,4 +1,4 @@
--- RINGRAZOR m-- breach params - tweak as needed
+#version 2
 local config = {
     radius = 1.2,        -- cut size (Q/E keys)
     depth = 1.0,         -- how deep it goes (R/T)
@@ -7,36 +7,22 @@
     shape = "circle",    -- current shape (F key cycles)
     shapeIndex = 1       -- current shape index
 }
-
--- Available shapes
 local SHAPES = {
     {name = "circle", displayName = "Circle"},
     {name = "square", displayName = "Square"}, 
     {name = "triangle", displayName = "Triangle"},
     {name = "door", displayName = "Door"}
 }
-
--- cuts clean holes through anythin, even yo mama (probably)
-
--- MANY MANY THANKS to that sweet sweet being of "Punished Bernadetta" because I took ""inspiration"" for some of the stuff from his mod because it works so damn nicely
-
--- Tool config
 local TOOL_ID = "vectorrazor"
 local TOOL_NAME = "VectorRazor"
-
--- Sound handles
 local sounds = {}
-local globalSoundPlaying = false  -- STOP OVERLAPS
-local soundStopTime = 0           -- Time to fucking stop
--- Skin refresh state
+local globalSoundPlaying = false
+local soundStopTime = 0
 local pendingSkinRefresh = false
 local skinRefreshTries = 0
-local maxSkinRefreshTries = 6  -- spread over a few frames
--- Forced re-equip phases to guarantee visual update
-local skinReequipPhase = 0      -- 0=idle,1=unequip,2=reequip
+local maxSkinRefreshTries = 6
+local skinReequipPhase = 0
 local skinReequipDeadline = 0
-
--- breach params tweak as needed
 local config = {
     radius = 1.2,        -- cut size (Q/E keys)
     depth = 1.0,         -- how deep it goes (Z/X)
@@ -45,265 +31,22 @@
     shape = "circle",    -- current shape (G key cycles)
     shapeIndex = 1       -- current shape index
 }
-
--- States
 local placedMines = {}
 local lastPlaceTime = 0
 local placementCooldown = 0.3
-
--- utils
-local function vec3(x, y, z)
-    return {x, y, z}
-end
-
-local function vecAdd(a, b)
-    return {a[1] + b[1], a[2] + b[2], a[3] + b[3]}
-end
-
-local function vecSub(a, b)
-    return {a[1] - b[1], a[2] - b[2], a[3] - b[3]}
-end
-
-local function vecScale(v, s)
-    return {v[1] * s, v[2] * s, v[3] * s}
-end
-
-local function vecLength(v)
-    return math.sqrt(v[1]*v[1] + v[2]*v[2] + v[3]*v[3])
-end
-
-local function vecNormalize(v)
-    local len = vecLength(v)
-    if len == 0 then return {0, 0, 0} end
-    return {v[1]/len, v[2]/len, v[3]/len}
-end
-
-local function vecCross(a, b)
-    return {
-        a[2]*b[3] - a[3]*b[2],
-        a[3]*b[1] - a[1]*b[3],
-        a[1]*b[2] - a[2]*b[1]
-    }
-end
-
--- calc where emitter should be on the circle
-local function angleToCirclePos(center, tangent, bitangent, angle, radius)
-    -- circle math
-    local cosAngle = math.cos(angle)
-    local sinAngle = math.sin(angle)
-    
-    return vecAdd(center, vecAdd(
-        vecScale(tangent, cosAngle * radius),
-        vecScale(bitangent, sinAngle * radius)
-    ))
-end
-
--- Generate cutting points for different shapes
-local function generateShapePoints(shape, center, tangent, bitangent, radius, numPoints)
-    local points = {}
-    
-    if shape == "circle" then
-        -- Original circle logic
-        for i = 0, numPoints - 1 do
-            local angle = (i / numPoints) * 2 * math.pi
-            local point = angleToCirclePos(center, tangent, bitangent, angle, radius)
-            table.insert(points, point)
-        end
-        
-    elseif shape == "square" then
-        -- Square with 4 sides and proper corner cutting
-        local corners = {
-            {radius, radius},   -- top-right
-            {-radius, radius},  -- top-left  
-            {-radius, -radius}, -- bottom-left
-            {radius, -radius}   -- bottom-right
-        }
-        
-        local pointsPerSide = math.floor(numPoints / 4)
-        for side = 1, 4 do
-            local startCorner = corners[side]
-            local endCorner = corners[(side % 4) + 1]
-            
-            -- Add extra points at each corner for better cutting
-            for i = 0, pointsPerSide do  -- Changed to include endpoint
-                local t = i / pointsPerSide
-                local x = startCorner[1] + (endCorner[1] - startCorner[1]) * t
-                local y = startCorner[2] + (endCorner[2] - startCorner[2]) * t
-                local point = vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
-                table.insert(points, point)
-                
-                -- Add extra cutting points near corners (within 10% of corner)
-                if t <= 0.1 or t >= 0.9 then
-                    table.insert(points, point)  -- Duplicate corner area points for thorough cutting
-                end
-            end
-        end
-        
-    elseif shape == "triangle" then
-        -- Equilateral triangle
-        local corners = {
-            {0, radius},                    -- top
-            {radius * 0.866, -radius * 0.5}, -- bottom-right
-            {-radius * 0.866, -radius * 0.5}  -- bottom-left  
-        }
-        
-        local pointsPerSide = math.floor(numPoints / 3)
-        for side = 1, 3 do
-            local startCorner = corners[side]
-            local endCorner = corners[(side % 3) + 1]
-            
-            for i = 0, pointsPerSide - 1 do
-                local t = i / pointsPerSide
-                local x = startCorner[1] + (endCorner[1] - startCorner[1]) * t
-                local y = startCorner[2] + (endCorner[2] - startCorner[2]) * t
-                local point = vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
-                table.insert(points, point)
-            end
-        end
-        
-    elseif shape == "door" then
-        -- Vertical rectangle door (taller than wide)
-        local doorWidth = radius * 0.7   -- 60% of radius for width
-        local doorHeight = radius * 1.2  -- 140% of radius for height
-        
-        local corners = {
-            {doorWidth, doorHeight},   -- top-right
-            {-doorWidth, doorHeight},  -- top-left  
-            {-doorWidth, -doorHeight}, -- bottom-left
-            {doorWidth, -doorHeight}   -- bottom-right
-        }
-        
-        local pointsPerSide = math.floor(numPoints / 4)
-        for side = 1, 4 do
-            local startCorner = corners[side]
-            local endCorner = corners[(side % 4) + 1]
-            
-            -- Add extra points at each corner for better cutting
-            for i = 0, pointsPerSide do  -- Include endpoint
-                local t = i / pointsPerSide
-                local x = startCorner[1] + (endCorner[1] - startCorner[1]) * t
-                local y = startCorner[2] + (endCorner[2] - startCorner[2]) * t
-                local point = vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
-                table.insert(points, point)
-                
-                -- Add extra cutting points near corners for thorough cutting
-                if t <= 0.1 or t >= 0.9 then
-                    table.insert(points, point)  -- Duplicate corner area points
-                end
-            end
-        end
-        
-    end
-    
-    return points
-end
-
-local function vecDot(a, b)
-    return a[1]*b[1] + a[2]*b[2] + a[3]*b[3]
-end
-
-local function clamp(value, min, max)
-    if value < min then return min end
-    if value > max then return max end
-    return value
-end
-
--- Color utils (stored as 'r;g;b' under savegame.mod.vectorrazor.*)
-local function parseColorString(s, def)
-    if not s or s == '' then return def[1], def[2], def[3] end
-    local r,g,b = s:match("([%d.]+);([%d.]+);([%d.]+)")
-    r = tonumber(r) or def[1]
-    g = tonumber(g) or def[2]
-    b = tonumber(b) or def[3]
-    return clamp(r,0,1), clamp(g,0,1), clamp(b,0,1)
-end
-local function getColor3(key, def)
-    local s = GetString('savegame.mod.vectorrazor.'..key)
-    return {parseColorString(s, def)}
-end
-local function mixColor(c, t)
-    -- mix towards white by t
-    return { c[1] + (1 - c[1]) * t, c[2] + (1 - c[2]) * t, c[3] + (1 - c[3]) * t }
-end
-
--- thank god I studied for my linear algebra exam (I DID NOT) 
-
--- gen surface coords for the cutter
-local function createSurfaceFrame(normal)
-    -- Choose an arbitrary up vector that's not parallel to normal
-    local up = math.abs(normal[2]) < 0.99 and {0, 1, 0} or {1, 0, 0}
-    
-    -- Create tangent vectors
-    local tangent = vecNormalize(vecCross(up, normal))
-    local bitangent = vecNormalize(vecCross(normal, tangent))
-    
-    return tangent, bitangent
-end
-
--- Convert angle to position on circle
-local function angleToCirclePos(center, tangent, bitangent, angle, radius)
-    local x = math.cos(angle) * radius
-    local y = math.sin(angle) * radius
-    return vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
-end
-
--- Calculate proper orientation using C4's yoinkedTM method
-local function calculateSurfaceQuat(normal, dir)
-    local quat = QuatLookAt(Vec(), normal)
-    if VecLength(VecCross(normal, Vec(0, 1, 0))) == 0 then
-        quat = QuatRotateQuat(QuatEuler(0, math.deg(math.atan2(dir[1], dir[3])) + 180, 0), quat)
-    end
-    return quat
-end
-
--- (Initial init removed; final init defined later after skin system)
-
--- Delay adjustment presets & keybinds (declare BEFORE input handler so variables exist when function compiles)
--- Default mapping intentionally: O = decrease (left), P = increase (right)
--- Ensure desired mapping: O = decrease, P = increase
 local savedInc = GetString('savegame.mod.vectorrazor.delayIncKey')
 local savedDec = GetString('savegame.mod.vectorrazor.delayDecKey')
-if savedInc == '' and savedDec == '' then
-    SetString('savegame.mod.vectorrazor.delayIncKey','p')
-    SetString('savegame.mod.vectorrazor.delayDecKey','o')
-    savedInc, savedDec = 'p','o'
-end
--- Auto-correct if user previously had them flipped
-if savedInc == 'o' and savedDec == 'p' then
-    SetString('savegame.mod.vectorrazor.delayIncKey','p')
-    SetString('savegame.mod.vectorrazor.delayDecKey','o')
-    if not GetBool('savegame.mod.vectorrazor.reportedKeySwap') then
-        DebugPrint('[VectorRazor] Swapped O/P so O decreases and P increases delay')
-        SetBool('savegame.mod.vectorrazor.reportedKeySwap', true)
-    end
-end
 local delayIncKey = GetString('savegame.mod.vectorrazor.delayIncKey')
 local delayDecKey = GetString('savegame.mod.vectorrazor.delayDecKey')
--- Additional configurable keybinds and HUD options
--- Defaults for movement/shape controls
-if GetString('savegame.mod.vectorrazor.radiusDecKey') == '' then SetString('savegame.mod.vectorrazor.radiusDecKey','q') end
-if GetString('savegame.mod.vectorrazor.radiusIncKey') == '' then SetString('savegame.mod.vectorrazor.radiusIncKey','e') end
-if GetString('savegame.mod.vectorrazor.depthDecKey') == '' then SetString('savegame.mod.vectorrazor.depthDecKey','z') end
-if GetString('savegame.mod.vectorrazor.depthIncKey') == '' then SetString('savegame.mod.vectorrazor.depthIncKey','x') end
-if GetString('savegame.mod.vectorrazor.shapeCycleKey') == '' then SetString('savegame.mod.vectorrazor.shapeCycleKey','g') end
--- Options menu toggle default
-if GetString('savegame.mod.vectorrazor.toggleOptionsKey') == '' then SetString('savegame.mod.vectorrazor.toggleOptionsKey','f1') end
--- HUD corner option default
-if GetString('savegame.mod.vectorrazor.hudCorner') == '' then SetString('savegame.mod.vectorrazor.hudCorner','top-left') end
-
--- Locals holding current effective keybinds
 local radiusDecKey = GetString('savegame.mod.vectorrazor.radiusDecKey')
 local radiusIncKey = GetString('savegame.mod.vectorrazor.radiusIncKey')
 local depthDecKey = GetString('savegame.mod.vectorrazor.depthDecKey')
 local depthIncKey = GetString('savegame.mod.vectorrazor.depthIncKey')
 local shapeCycleKey = GetString('savegame.mod.vectorrazor.shapeCycleKey')
 local toggleOptionsKey = GetString('savegame.mod.vectorrazor.toggleOptionsKey')
-local hudCorner = GetString('savegame.mod.vectorrazor.hudCorner') -- 'top-left'|'top-right'|'bottom-left'|'bottom-right'
-
--- Options UI state
+local hudCorner = GetString('savegame.mod.vectorrazor.hudCorner')
 local optionsOpen = false
-local capturingAction = '' -- when non-empty, we're waiting for next key press to bind to this action id
--- Include a special remote preset. Each preset entry: {label, delaySeconds or nil, remote=true?}
+local capturingAction = ''
 local delayPresets = {
     {label="0s", value=0},
     {label="0.1s", value=0.1},
@@ -315,106 +58,7 @@
     {label="5s", value=5},
     {label="REMOTE", remote=true, value=0.0} -- remote preset: immediate deployment after arming
 }
-if GetInt('savegame.mod.vectorrazor.delayPresetIndex') == 0 then SetInt('savegame.mod.vectorrazor.delayPresetIndex',4) end -- default 0.5s
-local function applyDelayFromPreset()
-    local idx = clamp(GetInt('savegame.mod.vectorrazor.delayPresetIndex'),1,#delayPresets)
-    SetInt('savegame.mod.vectorrazor.delayPresetIndex', idx)
-    local p = delayPresets[idx]
-    -- Store numeric value for backward compatibility; remote preset stores its value (post-arm delay)
-    SetFloat('savegame.mod.vectorrazor.delay', p.value or 0.5)
-end
-applyDelayFromPreset()
-
--- keybinds n scheisse
-local function handleInput()
-    if GetString("game.player.tool") ~= TOOL_ID then return end
-    
-    -- Don't allow any tool input while in a vehicle
-    local playerVehicle = GetPlayerVehicle()
-    if playerVehicle ~= 0 then return end
-    
-    -- Toggle options menu (allowed regardless of vehicle state)
-    if InputPressed(toggleOptionsKey) then
-        optionsOpen = not optionsOpen
-    end
-
-    -- Don't allow any tool input while in a vehicle
-    local playerVehicle = GetPlayerVehicle()
-    if playerVehicle ~= 0 then return end
-
-    -- If options menu is open, block tool inputs
-    if optionsOpen then return end
-
-    -- size adjust (using 0.1 increments to avoid odd/even number lock)
-    if InputPressed(radiusDecKey) then
-        config.radius = clamp(config.radius - 0.1, 0.5, 10.0)
-    end
-    if InputPressed(radiusIncKey) then
-        config.radius = clamp(config.radius + 0.1, 0.5, 10.0)
-    end
-    
-        -- depth adjust
-    if InputPressed(depthDecKey) then
-        config.depth = clamp(config.depth - 0.1, 0.1, 5.0)
-    end
-    if InputPressed(depthIncKey) then
-        config.depth = clamp(config.depth + 0.1, 0.1, 5.0)
-    end
-    
-        -- shape cycling
-    if InputPressed(shapeCycleKey) then
-        config.shapeIndex = (config.shapeIndex % #SHAPES) + 1
-        config.shape = SHAPES[config.shapeIndex].name
-    end
-    
-    -- Delay preset adjust (independent of mode) using configured keys
-    if InputPressed(delayDecKey) then
-        local idx = GetInt('savegame.mod.vectorrazor.delayPresetIndex') - 1
-        if idx < 1 then idx = #delayPresets end
-        SetInt('savegame.mod.vectorrazor.delayPresetIndex', idx)
-        applyDelayFromPreset()
-    end
-    if InputPressed(delayIncKey) then
-        local idx = GetInt('savegame.mod.vectorrazor.delayPresetIndex') + 1
-        if idx > #delayPresets then idx = 1 end
-        SetInt('savegame.mod.vectorrazor.delayPresetIndex', idx)
-        applyDelayFromPreset()
-    end
-    
-    -- deploy mine (only if not in vehicle)
-    if InputPressed("lmb") and GetTime() > lastPlaceTime + placementCooldown then
-        local playerVehicle = GetPlayerVehicle()
-        if playerVehicle == 0 then  -- Only work when not in a vehicle
-            placeMine()
-            lastPlaceTime = GetTime()
-        end
-    end
-end
-
--- Add new configurable settings retrieval (placed near top after config declarations)
-if GetFloat("savegame.mod.vectorrazor.delay") == 0 then
-    SetFloat("savegame.mod.vectorrazor.delay", 0.5) -- default activation delay before deployment
-end
-if GetString("savegame.mod.vectorrazor.detonateKey") == "" then
-    SetString("savegame.mod.vectorrazor.detonateKey", "k")
-end
 local detonateKey = GetString("savegame.mod.vectorrazor.detonateKey")
-
--- Helper to read current delay each frame (so UI/Options adjustments apply live)
-local function currentPreset()
-    local idx = clamp(GetInt('savegame.mod.vectorrazor.delayPresetIndex'),1,#delayPresets)
-    return delayPresets[idx]
-end
-local function getActivationDelay()
-    local p = currentPreset()
-    return p.value or 0.5
-end
-local function isRemotePreset()
-    local p = currentPreset()
-    return p.remote == true
-end
-
--- Skin & sound variants
 local skins = {
   {
     id = "default",
@@ -433,15 +77,304 @@
     open = "MOD/snd/cookie_open.ogg"
   }
 }
+local secretSequence = {"c","o","o","k","i","e"}
+local seqIndex = 1
+local lastSeqTime = 0
+local seqTimeout = 3.0
+local _orig_init = init
+
+local function vec3(x, y, z)
+    return {x, y, z}
+end
+
+local function vecAdd(a, b)
+    return {a[1] + b[1], a[2] + b[2], a[3] + b[3]}
+end
+
+local function vecSub(a, b)
+    return {a[1] - b[1], a[2] - b[2], a[3] - b[3]}
+end
+
+local function vecScale(v, s)
+    return {v[1] * s, v[2] * s, v[3] * s}
+end
+
+local function vecLength(v)
+    return math.sqrt(v[1]*v[1] + v[2]*v[2] + v[3]*v[3])
+end
+
+local function vecNormalize(v)
+    local len = vecLength(v)
+    if len == 0 then return {0, 0, 0} end
+    return {v[1]/len, v[2]/len, v[3]/len}
+end
+
+local function vecCross(a, b)
+    return {
+        a[2]*b[3] - a[3]*b[2],
+        a[3]*b[1] - a[1]*b[3],
+        a[1]*b[2] - a[2]*b[1]
+    }
+end
+
+local function angleToCirclePos(center, tangent, bitangent, angle, radius)
+    -- circle math
+    local cosAngle = math.cos(angle)
+    local sinAngle = math.sin(angle)
+    
+    return vecAdd(center, vecAdd(
+        vecScale(tangent, cosAngle * radius),
+        vecScale(bitangent, sinAngle * radius)
+    ))
+end
+
+local function generateShapePoints(shape, center, tangent, bitangent, radius, numPoints)
+    local points = {}
+    
+    if shape == "circle" then
+        -- Original circle logic
+        for i = 0, numPoints - 1 do
+            local angle = (i / numPoints) * 2 * math.pi
+            local point = angleToCirclePos(center, tangent, bitangent, angle, radius)
+            table.insert(points, point)
+        end
+        
+    elseif shape == "square" then
+        -- Square with 4 sides and proper corner cutting
+        local corners = {
+            {radius, radius},   -- top-right
+            {-radius, radius},  -- top-left  
+            {-radius, -radius}, -- bottom-left
+            {radius, -radius}   -- bottom-right
+        }
+        
+        local pointsPerSide = math.floor(numPoints / 4)
+        for side = 1, 4 do
+            local startCorner = corners[side]
+            local endCorner = corners[(side % 4) + 1]
+            
+            -- Add extra points at each corner for better cutting
+            for i = 0, pointsPerSide do  -- Changed to include endpoint
+                local t = i / pointsPerSide
+                local x = startCorner[1] + (endCorner[1] - startCorner[1]) * t
+                local y = startCorner[2] + (endCorner[2] - startCorner[2]) * t
+                local point = vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
+                table.insert(points, point)
+                
+                -- Add extra cutting points near corners (within 10% of corner)
+                if t <= 0.1 or t >= 0.9 then
+                    table.insert(points, point)  -- Duplicate corner area points for thorough cutting
+                end
+            end
+        end
+        
+    elseif shape == "triangle" then
+        -- Equilateral triangle
+        local corners = {
+            {0, radius},                    -- top
+            {radius * 0.866, -radius * 0.5}, -- bottom-right
+            {-radius * 0.866, -radius * 0.5}  -- bottom-left  
+        }
+        
+        local pointsPerSide = math.floor(numPoints / 3)
+        for side = 1, 3 do
+            local startCorner = corners[side]
+            local endCorner = corners[(side % 3) + 1]
+            
+            for i = 0, pointsPerSide - 1 do
+                local t = i / pointsPerSide
+                local x = startCorner[1] + (endCorner[1] - startCorner[1]) * t
+                local y = startCorner[2] + (endCorner[2] - startCorner[2]) * t
+                local point = vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
+                table.insert(points, point)
+            end
+        end
+        
+    elseif shape == "door" then
+        -- Vertical rectangle door (taller than wide)
+        local doorWidth = radius * 0.7   -- 60% of radius for width
+        local doorHeight = radius * 1.2  -- 140% of radius for height
+        
+        local corners = {
+            {doorWidth, doorHeight},   -- top-right
+            {-doorWidth, doorHeight},  -- top-left  
+            {-doorWidth, -doorHeight}, -- bottom-left
+            {doorWidth, -doorHeight}   -- bottom-right
+        }
+        
+        local pointsPerSide = math.floor(numPoints / 4)
+        for side = 1, 4 do
+            local startCorner = corners[side]
+            local endCorner = corners[(side % 4) + 1]
+            
+            -- Add extra points at each corner for better cutting
+            for i = 0, pointsPerSide do  -- Include endpoint
+                local t = i / pointsPerSide
+                local x = startCorner[1] + (endCorner[1] - startCorner[1]) * t
+                local y = startCorner[2] + (endCorner[2] - startCorner[2]) * t
+                local point = vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
+                table.insert(points, point)
+                
+                -- Add extra cutting points near corners for thorough cutting
+                if t <= 0.1 or t >= 0.9 then
+                    table.insert(points, point)  -- Duplicate corner area points
+                end
+            end
+        end
+        
+    end
+    
+    return points
+end
+
+local function vecDot(a, b)
+    return a[1]*b[1] + a[2]*b[2] + a[3]*b[3]
+end
+
+local function clamp(value, min, max)
+    if value < min then return min end
+    if value > max then return max end
+    return value
+end
+
+local function parseColorString(s, def)
+    if not s or s == '' then return def[1], def[2], def[3] end
+    local r,g,b = s:match("([%d.]+);([%d.]+);([%d.]+)")
+    r = tonumber(r) or def[1]
+    g = tonumber(g) or def[2]
+    b = tonumber(b) or def[3]
+    return clamp(r,0,1), clamp(g,0,1), clamp(b,0,1)
+end
+
+local function getColor3(key, def)
+    local s = GetString('savegame.mod.vectorrazor.'..key)
+    return {parseColorString(s, def)}
+end
+
+local function mixColor(c, t)
+    -- mix towards white by t
+    return { c[1] + (1 - c[1]) * t, c[2] + (1 - c[2]) * t, c[3] + (1 - c[3]) * t }
+end
+
+local function createSurfaceFrame(normal)
+    -- Choose an arbitrary up vector that's not parallel to normal
+    local up = math.abs(normal[2]) < 0.99 and {0, 1, 0} or {1, 0, 0}
+    
+    -- Create tangent vectors
+    local tangent = vecNormalize(vecCross(up, normal))
+    local bitangent = vecNormalize(vecCross(normal, tangent))
+    
+    return tangent, bitangent
+end
+
+local function angleToCirclePos(center, tangent, bitangent, angle, radius)
+    local x = math.cos(angle) * radius
+    local y = math.sin(angle) * radius
+    return vecAdd(center, vecAdd(vecScale(tangent, x), vecScale(bitangent, y)))
+end
+
+local function calculateSurfaceQuat(normal, dir)
+    local quat = QuatLookAt(Vec(), normal)
+    if VecLength(VecCross(normal, Vec(0, 1, 0))) == 0 then
+        quat = QuatRotateQuat(QuatEuler(0, math.deg(math.atan2(dir[1], dir[3])) + 180, 0), quat)
+    end
+    return quat
+end
+
+local function applyDelayFromPreset()
+    local idx = clamp(GetInt('savegame.mod.vectorrazor.delayPresetIndex'),1,#delayPresets)
+    SetInt('savegame.mod.vectorrazor.delayPresetIndex', idx, true)
+    local p = delayPresets[idx]
+    -- Store numeric value for backward compatibility; remote preset stores its value (post-arm delay)
+    SetFloat('savegame.mod.vectorrazor.delay', p.value or 0.5, true)
+end
+
+local function handleInput()
+    if GetString("game.player.tool") ~= TOOL_ID then return end
+    
+    -- Don't allow any tool input while in a vehicle
+    local playerVehicle = GetPlayerVehicle(playerId)
+    if playerVehicle ~= 0 then return end
+    
+    -- Toggle options menu (allowed regardless of vehicle state)
+    if InputPressed(toggleOptionsKey) then
+        optionsOpen = not optionsOpen
+    end
+
+    -- Don't allow any tool input while in a vehicle
+    local playerVehicle = GetPlayerVehicle(playerId)
+    if playerVehicle ~= 0 then return end
+
+    -- If options menu is open, block tool inputs
+    if optionsOpen then return end
+
+    -- size adjust (using 0.1 increments to avoid odd/even number lock)
+    if InputPressed(radiusDecKey) then
+        config.radius = clamp(config.radius - 0.1, 0.5, 10.0)
+    end
+    if InputPressed(radiusIncKey) then
+        config.radius = clamp(config.radius + 0.1, 0.5, 10.0)
+    end
+    
+        -- depth adjust
+    if InputPressed(depthDecKey) then
+        config.depth = clamp(config.depth - 0.1, 0.1, 5.0)
+    end
+    if InputPressed(depthIncKey) then
+        config.depth = clamp(config.depth + 0.1, 0.1, 5.0)
+    end
+    
+        -- shape cycling
+    if InputPressed(shapeCycleKey) then
+        config.shapeIndex = (config.shapeIndex % #SHAPES) + 1
+        config.shape = SHAPES[config.shapeIndex].name
+    end
+    
+    -- Delay preset adjust (independent of mode) using configured keys
+    if InputPressed(delayDecKey) then
+        local idx = GetInt('savegame.mod.vectorrazor.delayPresetIndex') - 1
+        if idx < 1 then idx = #delayPresets end
+        SetInt('savegame.mod.vectorrazor.delayPresetIndex', idx, true)
+        applyDelayFromPreset()
+    end
+    if InputPressed(delayIncKey) then
+        local idx = GetInt('savegame.mod.vectorrazor.delayPresetIndex') + 1
+        if idx > #delayPresets then idx = 1 end
+        SetInt('savegame.mod.vectorrazor.delayPresetIndex', idx, true)
+        applyDelayFromPreset()
+    end
+    
+    -- deploy mine (only if not in vehicle)
+    if InputPressed("lmb") and GetTime() > lastPlaceTime + placementCooldown then
+        local playerVehicle = GetPlayerVehicle(playerId)
+        if playerVehicle == 0 then  -- Only work when not in a vehicle
+            placeMine()
+            lastPlaceTime = GetTime()
+        end
+    end
+end
+
+local function currentPreset()
+    local idx = clamp(GetInt('savegame.mod.vectorrazor.delayPresetIndex'),1,#delayPresets)
+    return delayPresets[idx]
+end
+
+local function getActivationDelay()
+    local p = currentPreset()
+    return p.value or 0.5
+end
+
+local function isRemotePreset()
+    local p = currentPreset()
+    return p.remote == true
+end
 
 local function clampSkinIndex(i)
   if i < 1 then return #skins end
   if i > #skins then return 1 end
   return i
 end
-if GetInt("savegame.mod.vectorrazor.skinIndex") == 0 then
-  SetInt("savegame.mod.vectorrazor.skinIndex", 1)
-end
+
 local function currentSkin()
   local idx = clampSkinIndex(GetInt("savegame.mod.vectorrazor.skinIndex"))
   return skins[idx], idx
@@ -451,7 +384,7 @@
   local sk = currentSkin()
   -- Re-register tool voxel (mine voxel used as tool model)
   RegisterTool(TOOL_ID, TOOL_NAME, sk.mine)
-  SetBool("game.tool." .. TOOL_ID .. ".enabled", true)
+  SetBool("game.tool." .. TOOL_ID .. ".enabled", true, true)
   -- Assign sounds for this skin
   sounds.laser = LoadLoop(sk.laser)
   sounds.open = LoadSound(sk.open)
@@ -464,12 +397,6 @@
             skinReequipDeadline = GetTime() + 1.0  -- give it up to 1 second
     end
 end
-
--- Secret activation: typing the word "cookie" cycles skin
-local secretSequence = {"c","o","o","k","i","e"}
-local seqIndex = 1
-local lastSeqTime = 0
-local seqTimeout = 3.0 -- seconds allowed between key presses
 
 local function handleSecretSequence()
   for code = string.byte('a'), string.byte('z') do
@@ -487,7 +414,7 @@
           local _, idx = currentSkin()
           idx = idx + 1
           if idx > #skins then idx = 1 end
-          SetInt("savegame.mod.vectorrazor.skinIndex", idx)
+          SetInt("savegame.mod.vectorrazor.skinIndex", idx, true)
           applySkin()
           DebugPrint('[VectorRazor] Skin: ' .. currentSkin().id)
           seqIndex = 1
@@ -505,22 +432,9 @@
   end
 end
 
--- Wrap original init to apply skin after default registration
-local _orig_init = init -- will be nil (we removed earlier init)
-function init()
-    -- register with default model first (ensures tool appears even if skin load fails)
-    RegisterTool(TOOL_ID, TOOL_NAME, "MOD/vox/mine.vox")
-    SetBool("game.tool." .. TOOL_ID .. ".enabled", true)
-    if _orig_init then _orig_init() end
-    applySkin()
-end
-
--- (Removed duplicate angleToCirclePos and calculateSurfaceQuat definitions)
-
--- Place a mine on the surface the player is looking at (using C4's yoinkedTM proven method)
 function placeMine()
     local sk = currentSkin()
-    local t = GetPlayerCameraTransform()
+    local t = GetPlayerCameraTransform(playerId)
     local fwd = TransformToParentVec(t, Vec(0, 0, -1))
     local maxDist = GetBool("game.thirdperson") and 8 or 4
     QueryInclude("physical dynamic static large small visible animator")
@@ -552,7 +466,7 @@
     local mineXML = '<?xml version="1.0"?><prefab><body dynamic="false"><vox pos="0 0 0" file="'..sk.mine..'"/></body></prefab>'
     local spawnedMineObjects = Spawn(mineXML, mineTransform, true, true)
     local mineBody = nil
-    if spawnedMineObjects and #spawnedMineObjects > 0 then
+    if spawnedMineObjects and #spawnedMineObjects ~= 0 then
         for _, handle in ipairs(spawnedMineObjects) do
             SetShapeCollisionFilter(handle, 2, 255 - 2)
         end
@@ -574,7 +488,7 @@
     local emitterXML = '<?xml version="1.0"?><prefab><body dynamic="false"><vox pos="0 0 0" file="'..sk.emitter..'"/></body></prefab>'
     local spawnedEmitterObjects = Spawn(emitterXML, emitterTransform, true, true)
     local emitterBody = nil
-    if spawnedEmitterObjects and #spawnedEmitterObjects > 0 then
+    if spawnedEmitterObjects and #spawnedEmitterObjects ~= 0 then
         for _, handle in ipairs(spawnedEmitterObjects) do
             SetShapeCollisionFilter(handle, 2, 255 - 2)
         end
@@ -619,7 +533,6 @@
     table.insert(placedMines, mine)
 end
 
--- Perform the actual cutting at a specific position
 local function cutAtPosition(pos, normal, depth)
     -- Cut in a line from surface into the material
     local stepSize = 0.1  
@@ -638,7 +551,6 @@
     MakeHole(pos, 0.15, 0.15, 0.15)
 end
 
--- Update all placed mines
 local function updateMines(dt)
     for i = #placedMines, 1, -1 do
         local mine = placedMines[i]
@@ -697,7 +609,7 @@
                         end
                         local activeEmitterXML = '<?xml version="1.0"?><prefab><body dynamic="false"><vox pos="0 0 0" file="'..currentSkin().emitterActive..'"/></body></prefab>'
                         local spawnedActiveObjects = Spawn(activeEmitterXML, currentTransform, true, true)
-                        if spawnedActiveObjects and #spawnedActiveObjects > 0 then
+                        if spawnedActiveObjects and #spawnedActiveObjects ~= 0 then
                             for _, handle in ipairs(spawnedActiveObjects) do
                                 SetShapeCollisionFilter(handle, 2, 255 - 2)
                             end
@@ -740,7 +652,7 @@
                 local t = mine.currentPointIndex - currentIndex  -- fractional part
                 
                 if currentIndex <= #mine.shapePoints then
-                    if nextIndex <= #mine.shapePoints and t > 0 then
+                    if nextIndex <= #mine.shapePoints and t ~= 0 then
                         -- Interpolate between current and next point for smooth movement
                         local currentPos = mine.shapePoints[currentIndex]
                         local nextPos = mine.shapePoints[nextIndex]
@@ -812,16 +724,15 @@
     end
 end
 
--- Draw cutting preview when aiming
 local function drawCuttingPreview()
     if GetString("game.player.tool") ~= TOOL_ID then return end
     
     -- hide EVERYTHING while in casr
-    local playerVehicle = GetPlayerVehicle()
+    local playerVehicle = GetPlayerVehicle(playerId)
     if playerVehicle ~= 0 then return end
     
     -- Aiming raycast
-    local t = GetPlayerCameraTransform()
+    local t = GetPlayerCameraTransform(playerId)
     local fwd = TransformToParentVec(t, Vec(0, 0, -1))
     local maxDist = GetBool("game.thirdperson") and 8 or 4
     
@@ -888,7 +799,6 @@
     DrawLine(vecSub(centerOffset, crossBitangent), vecAdd(centerOffset, crossBitangent), pc[1], pc[2], pc[3], 0.8)
 end
 
--- Draw visual indicators
 local function drawVisuals()
     for _, mine in ipairs(placedMines) do
         local segments = 64  -- Higher resolution for smoother circle
@@ -992,65 +902,6 @@
     end
 end
 
--- main loop
-function tick(dt)
-    if GetString("game.player.tool") == TOOL_ID then
-        SetToolTransform(Transform(Vec(0.30, -0.30, -0.65), QuatEuler(34, -16, 12)))
-    end
-    -- Attempt to force the held tool to update model a few frames after skin swap
-    if pendingSkinRefresh and GetString("game.player.tool") == TOOL_ID then
-        if skinRefreshTries < maxSkinRefreshTries then
-            -- Re-register repeatedly; some versions update the mesh after a couple frames
-            local sk = currentSkin()
-            RegisterTool(TOOL_ID, TOOL_NAME, sk.mine)
-            SetBool("game.tool." .. TOOL_ID .. ".enabled", true)
-            skinRefreshTries = skinRefreshTries + 1
-        else
-            pendingSkinRefresh = false
-        end
-    end
-    -- Forced re-equip fallback (more aggressive). Two-phase to avoid flicker.
-    if skinReequipPhase ~= 0 and GetTime() > skinReequipDeadline then
-        -- Timeout safety
-        skinReequipPhase = 0
-    end
-    if skinReequipPhase == 1 then
-        -- Phase 1: switch to a different tool & temporarily disable ours
-        if GetString("game.player.tool") == TOOL_ID then
-            -- Try sledge first, fallback to spraycan
-            SetString("game.player.tool", "sledge")
-            if GetString("game.player.tool") == TOOL_ID then
-                SetString("game.player.tool", "spraycan")
-            end
-        end
-        SetBool("game.tool." .. TOOL_ID .. ".enabled", false)
-        skinReequipPhase = 2
-    elseif skinReequipPhase == 2 then
-        -- Phase 2: re-enable and reselect our tool with new model
-        local sk = currentSkin()
-        RegisterTool(TOOL_ID, TOOL_NAME, sk.mine)
-        SetBool("game.tool." .. TOOL_ID .. ".enabled", true)
-        SetString("game.player.tool", TOOL_ID)
-        skinReequipPhase = 0
-        pendingSkinRefresh = false
-    end
-    if isRemotePreset() and InputPressed(detonateKey) then
-        for _, mine in ipairs(placedMines) do
-            if mine.waitingForRemote and not mine.deploying and not mine.active then
-                mine.waitingForRemote = false
-                mine.timer = 0
-            end
-        end
-    end
-    handleSecretSequence()
-    handleInput()
-    updateMines(dt)
-    drawCuttingPreview()
-    drawVisuals()
-end
-
--- ui stuff
--- Options UI helper: capture any pressed key (letters, digits, F1-F12, arrows, space)
 local function captureAnyKeyPressed()
     -- letters
     for code = string.byte('a'), string.byte('z') do
@@ -1115,7 +966,7 @@
                 if hudCorner == c.id then UiColor(0.9,0.9,0.2,1) else UiColor(0.8,0.8,0.8,1) end
                 if UiTextButton(c.label) then
                     hudCorner = c.id
-                    SetString('savegame.mod.vectorrazor.hudCorner', hudCorner)
+                    SetString('savegame.mod.vectorrazor.hudCorner', hudCorner, true)
                 end
             UiPop()
             UiTranslate(120,0)
@@ -1157,7 +1008,7 @@
             if pressed then
                 -- persist and update local variables
                 local keyBase = 'savegame.mod.vectorrazor.' .. capturingAction
-                SetString(keyBase, pressed)
+                SetString(keyBase, pressed, true)
                 if capturingAction == 'radiusDecKey' then radiusDecKey = pressed
                 elseif capturingAction == 'radiusIncKey' then radiusIncKey = pressed
                 elseif capturingAction == 'depthDecKey' then depthDecKey = pressed
@@ -1183,9 +1034,78 @@
     UiPop()
 end
 
-function draw()
+function server.init()
+    RegisterTool(TOOL_ID, TOOL_NAME, "MOD/vox/mine.vox")
+    SetBool("game.tool." .. TOOL_ID .. ".enabled", true, true)
+    if _orig_init then _orig_init() end
+    applySkin()
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetString("game.player.tool") == TOOL_ID then
+            SetToolTransform(Transform(Vec(0.30, -0.30, -0.65), QuatEuler(34, -16, 12)))
+        end
+        -- Attempt to force the held tool to update model a few frames after skin swap
+        if pendingSkinRefresh and GetString("game.player.tool") == TOOL_ID then
+            if skinRefreshTries < maxSkinRefreshTries then
+                -- Re-register repeatedly; some versions update the mesh after a couple frames
+                local sk = currentSkin()
+                RegisterTool(TOOL_ID, TOOL_NAME, sk.mine)
+                SetBool("game.tool." .. TOOL_ID .. ".enabled", true, true)
+                skinRefreshTries = skinRefreshTries + 1
+            else
+                pendingSkinRefresh = false
+            end
+        end
+        -- Forced re-equip fallback (more aggressive). Two-phase to avoid flicker.
+        if skinReequipPhase ~= 0 and GetTime() > skinReequipDeadline then
+            -- Timeout safety
+            skinReequipPhase = 0
+        end
+        if skinReequipPhase == 1 then
+            -- Phase 1: switch to a different tool & temporarily disable ours
+            if GetString("game.player.tool") == TOOL_ID then
+                -- Try sledge first, fallback to spraycan
+                SetString("game.player.tool", "sledge", true)
+                if GetString("game.player.tool") == TOOL_ID then
+                    SetString("game.player.tool", "spraycan", true)
+                end
+            end
+            SetBool("game.tool." .. TOOL_ID .. ".enabled", false, true)
+            skinReequipPhase = 2
+        elseif skinReequipPhase == 2 then
+            -- Phase 2: re-enable and reselect our tool with new model
+            local sk = currentSkin()
+            RegisterTool(TOOL_ID, TOOL_NAME, sk.mine)
+            SetBool("game.tool." .. TOOL_ID .. ".enabled", true, true)
+            SetString("game.player.tool", TOOL_ID, true)
+            skinReequipPhase = 0
+            pendingSkinRefresh = false
+        end
+        handleSecretSequence()
+        handleInput()
+        updateMines(dt)
+        drawCuttingPreview()
+        drawVisuals()
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if isRemotePreset() and InputPressed(detonateKey) then
+        for _, mine in ipairs(placedMines) do
+            if mine.waitingForRemote and not mine.deploying and not mine.active then
+                mine.waitingForRemote = false
+                mine.timer = 0
+            end
+        end
+    end
+end
+
+function client.draw()
     if GetString("game.player.tool") ~= TOOL_ID then return end
-    if GetPlayerVehicle() ~= 0 then return end
+    if GetPlayerVehicle(playerId) ~= 0 then return end
     UiPush()
         -- Position panel based on HUD corner
         local panelW, panelH = 325, 175
@@ -1249,12 +1169,12 @@
     drawOptionsMenu()
     -- When menu is open, show cursor and block tool/game input a bit
     if optionsOpen then
-        SetBool("hud.nocrosshair", true)
-        SetBool("game.disableinput", true)
+        SetBool("hud.nocrosshair", true, true)
+        SetBool("game.disableinput", true, true)
     else
         -- explicitly clear in case we toggled it
-        if GetBool("game.disableinput") then SetBool("game.disableinput", false) end
-        if GetBool("hud.nocrosshair") then SetBool("hud.nocrosshair", false) end
-    end
-end
-
+        if GetBool("game.disableinput") then SetBool("game.disableinput", false, true) end
+        if GetBool("hud.nocrosshair") then SetBool("hud.nocrosshair", false, true) end
+    end
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
@@ -1,31 +1,4 @@
--- VectorRazor Options Page (accessible from the in-game Mod Options screen)
--- This page lets you set HUD position and keybinds, saved under savegame.mod.vectorrazor.*
-
--- helpers
-local function getStr(key, def)
-    local full = 'savegame.mod.vectorrazor.' .. key
-    if HasKey(full) then return GetString(full) end
-    return def or ''
-end
-local function setStr(key, val)
-    local full = 'savegame.mod.vectorrazor.' .. key
-    if val == nil or val == '' then
-        ClearKey(full)
-    else
-        SetString(full, val)
-    end
-end
-local function getBool(key, def)
-    local full = 'savegame.mod.vectorrazor.' .. key
-    if HasKey(full) then return GetBool(full) end
-    return def or false
-end
-local function setBool(key, val)
-    local full = 'savegame.mod.vectorrazor.' .. key
-    SetBool(full, val and true or false)
-end
-
--- default values (mirrors in main.lua)
+#version 2
 local defaults = {
     hudCorner = 'top-left',
     radiusDecKey = 'q',
@@ -38,8 +11,33 @@
     detonateKey  = getStr('detonateKey', 'k'),
     toggleOptionsKey = getStr('toggleOptionsKey', 'f1'),
 }
-
 local capturing = ''
+
+local function getStr(key, def)
+    local full = 'savegame.mod.vectorrazor.' .. key
+    if HasKey(full) then return GetString(full) end
+    return def or ''
+end
+
+local function setStr(key, val)
+    local full = 'savegame.mod.vectorrazor.' .. key
+    if val == nil or val == '' then
+        ClearKey(full)
+    else
+        SetString(full, val, true)
+    end
+end
+
+local function getBool(key, def)
+    local full = 'savegame.mod.vectorrazor.' .. key
+    if HasKey(full) then return GetBool(full) end
+    return def or false
+end
+
+local function setBool(key, val)
+    local full = 'savegame.mod.vectorrazor.' .. key
+    SetBool(full, val and true or false, true)
+end
 
 local function title(text)
     UiFont('bold.ttf', 38)
@@ -193,7 +191,7 @@
         UiTranslate(0, 48)
 end
 
-function draw()
+function client.draw()
     UiPush()
         UiAlign('left top')
         UiTranslate(UiWidth()*0.15, 80)
@@ -252,3 +250,4 @@
         captureKeys()
     UiPop()
 end
+

```
