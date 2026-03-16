# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,22 +1,4 @@
---[[
--- Libraries
-#include "scripts/lib/input.lua"
-#include "scripts/lib/engine.lua"
-#include "scripts/lib/debug.lua"
-
--- Entities
-#include "scripts/entities/flame.lua"
-
--- Managers
-#include "scripts/managers/soundManager.lua"
-
--- Base
-#include "scripts/flamethrower.lua"
-#include "scripts/knob.lua"
-#include "scripts/nozzle.lua"
-#include "scripts/fireStarter.lua"
-]]
-
+#version 2
 local initialized = false
 
 function initializeDependencies()
@@ -36,31 +18,29 @@
     initialized = true
 end
 
-function init()
+function server.init()
     initializeDependencies()
-
     if GetBool('savegame.mod.features.fire_limit.enabled') then
-        SetInt("game.fire.maxcount", GetInt('savegame.mod.features.fire_limit.value') or 1000000)
+        SetInt("game.fire.maxcount", GetInt('savegame.mod.features.fire_limit.value') or 1000000, true)
     end
 end
 
-function tick()
+function server.tick(dt)
     if not initialized then
         initializeDependencies()
     end
-
     if GetString("game.player.tool") == "hypnotox_flamethrower" then
         Debug:tick()
         Flamethrower:tick()
     end
 end
 
-function update()
+function server.update(dt)
     if not initialized then
         initializeDependencies()
     end
-
     if GetString("game.player.tool") == "hypnotox_flamethrower" and GetBool("game.player.canusetool") then
         Flamethrower:update()
     end
 end
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
@@ -1,56 +1,4 @@
----@class Options
----@field valueToSet string?
----@field inputBuffer number|string|nil
-Options = {
-    keyToSet = nil,
-    inputBuffer = nil,
-}
-
-function init()
-    local isInitialized = GetBool('savegame.mod.general.is_initialized')
-
-    if not isInitialized then
-        SetBool('savegame.mod.features.fire_limit.enabled', true)
-        SetInt('savegame.mod.features.fire_limit.value', 1000000)
-        SetInt('savegame.mod.features.inventory.slot', 6)
-        SetString('savegame.mod.features.nozzle.keybinds.decrease', 'leftarrow')
-        SetString('savegame.mod.features.nozzle.keybinds.increase', 'rightarrow')
-
-        SetBool('savegame.mod.general.is_initialized', true)
-    end
-end
-
-function draw()
-    UiTranslate(UiCenter(), 50)
-    UiAlign('center middle')
-    UiFont('regular.ttf', 24)
-
-    --Title
-    UiPush()
-    UiFont('bold.ttf', 48)
-    UiText('Flamethrower mod options')
-    UiPop()
-    UiTranslate(0, 100)
-
-    -- Subtitle nozzle
-    Options:subtitle('Nozzle adjustment')
-    Options:value('Decrease nozzle velocity', 'savegame.mod.features.nozzle.keybinds.decrease')
-    Options:value('Increase nozzle velocity', 'savegame.mod.features.nozzle.keybinds.increase')
-
-    -- Inventory slot
-    Options:subtitle('Inventory slot')
-    Options:value('Set inventory slot (1-6)', 'savegame.mod.features.inventory.slot', 6, true)
-
-    -- Subtitle fire limit
-    Options:subtitle('Fire limit')
-    Options:toggle('Enable unlimited fire', 'savegame.mod.features.fire_limit.enabled')
-
-    UiTranslate(0, 100)
-    if UiTextButton('Close', 200, 40) then
-        Menu()
-    end
-end
-
+#version 2
 function Options:title(title)
     UiPush()
     UiFont('bold.ttf', 48)
@@ -67,10 +15,6 @@
     UiTranslate(0, 100)
 end
 
----@param title string
----@param key string
----@param default number|string|nil
----@param isInventorySlot boolean|nil
 function Options:value(title, key, default, isInventorySlot)
     UiPush()
     UiFont('regular.ttf', 26)
@@ -117,7 +61,7 @@
             return
         end
 
-        SetString(self.keyToSet, lastPressedKey)
+        SetString(self.keyToSet, lastPressedKey, true)
         self.keyToSet = nil
     end
 end
@@ -145,7 +89,7 @@
     end
 
     if UiTextButton(label, 80, 40) then
-        SetBool(key, not GetBool(key))
+        SetBool(key, not GetBool(key), true)
     end
     UiPop()
 
@@ -190,9 +134,54 @@
         if lastPressedKey == 'enter' then
             Options.keyToSet = nil
             local inputBuffer = Options.inputBuffer
-            SetString(Options.keyToSet, tostring(inputBuffer))
+            SetString(Options.keyToSet, tostring(inputBuffer), true)
         else
             Options.inputBuffer = Options.inputBuffer .. lastPressedKey
         end
     end
 end
+
+function server.init()
+    local isInitialized = GetBool('savegame.mod.general.is_initialized')
+    if not isInitialized then
+        SetBool('savegame.mod.features.fire_limit.enabled', true, true)
+        SetInt('savegame.mod.features.fire_limit.value', 1000000, true)
+        SetInt('savegame.mod.features.inventory.slot', 6, true)
+        SetString('savegame.mod.features.nozzle.keybinds.decrease', 'leftarrow', true)
+        SetString('savegame.mod.features.nozzle.keybinds.increase', 'rightarrow', true)
+
+        SetBool('savegame.mod.general.is_initialized', true, true)
+    end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 50)
+    UiAlign('center middle')
+    UiFont('regular.ttf', 24)
+
+    --Title
+    UiPush()
+    UiFont('bold.ttf', 48)
+    UiText('Flamethrower mod options')
+    UiPop()
+    UiTranslate(0, 100)
+
+    -- Subtitle nozzle
+    Options:subtitle('Nozzle adjustment')
+    Options:value('Decrease nozzle velocity', 'savegame.mod.features.nozzle.keybinds.decrease')
+    Options:value('Increase nozzle velocity', 'savegame.mod.features.nozzle.keybinds.increase')
+
+    -- Inventory slot
+    Options:subtitle('Inventory slot')
+    Options:value('Set inventory slot (1-6)', 'savegame.mod.features.inventory.slot', 6, true)
+
+    -- Subtitle fire limit
+    Options:subtitle('Fire limit')
+    Options:toggle('Enable unlimited fire', 'savegame.mod.features.fire_limit.enabled')
+
+    UiTranslate(0, 100)
+    if UiTextButton('Close', 200, 40) then
+        Menu()
+    end
+end
+

```

---

# Migration Report: scripts\entities\flame.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\entities\flame.lua
+++ patched/scripts\entities\flame.lua
@@ -1,3 +1,4 @@
+#version 2
 function initFlame()
     Flame = {}
 
@@ -57,3 +58,4 @@
         return VecAdd(self.transform.pos, QuatRotateVec(offsetRotation, Vec(0, 0, offsetLength)))
     end
 end
+

```

---

# Migration Report: scripts\fireStarter.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\fireStarter.lua
+++ patched/scripts\fireStarter.lua
@@ -1,3 +1,4 @@
+#version 2
 function initFireStarter()
     FireStarter = {}
 
@@ -77,4 +78,5 @@
 
         PointLight(fireStarter.pos, 1, 0.3, 0.1, 0.2)
     end
-end+end
+

```

---

# Migration Report: scripts\flamethrower.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\flamethrower.lua
+++ patched/scripts\flamethrower.lua
@@ -1,3 +1,4 @@
+#version 2
 function initFlamethrower()
     Flamethrower = {
         maxAmmo = 100,
@@ -19,11 +20,11 @@
     Debug:dump(inventorySlot, 'Slot')
 
     RegisterTool('hypnotox_flamethrower', 'Flamethrower', modelPath, inventorySlot)
-    SetBool('game.tool.hypnotox_flamethrower.enabled', true)
-    SetFloat('game.tool.hypnotox_flamethrower.ammo', Flamethrower.maxAmmo)
+    SetBool('game.tool.hypnotox_flamethrower.enabled', true, true)
+    SetFloat('game.tool.hypnotox_flamethrower.ammo', Flamethrower.maxAmmo, true)
 
     function Flamethrower:tick()
-        SetBool('hud.aimdot', false)
+        SetBool('hud.aimdot', false, true)
         self:setToolPosition()
 
         SoundManager:tick()
@@ -70,7 +71,7 @@
         local ammoUsed = self.ammoPerSecond * GetTimeStep()
         local ammoLeft = GetFloat('game.tool.hypnotox_flamethrower.ammo') - ammoUsed
 
-        SetFloat('game.tool.hypnotox_flamethrower.ammo', ammoLeft)
+        SetFloat('game.tool.hypnotox_flamethrower.ammo', ammoLeft, true)
     end
 
     function Flamethrower:setToolPosition()
@@ -83,3 +84,4 @@
         end
     end
 end
+

```

---

# Migration Report: scripts\knob.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\knob.lua
+++ patched/scripts\knob.lua
@@ -1,3 +1,4 @@
+#version 2
 function initKnob()
     Knob = {
         flameVelocity = 15,
@@ -68,4 +69,5 @@
 
         return shapes[2]
     end
-end+end
+

```

---

# Migration Report: scripts\lib\debug.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\lib\debug.lua
+++ patched/scripts\lib\debug.lua
@@ -1,3 +1,4 @@
+#version 2
 function initDebug()
     Debug = {
         enabled = false,
@@ -22,7 +23,7 @@
     end
 
     function Debug:tick()
-        local playerTransform = GetPlayerTransform()
+        local playerTransform = GetPlayerTransform(playerId)
         local cameraTransform = GetCameraTransform()
         local toolTransform = GetBodyTransform(GetToolBody())
 
@@ -204,3 +205,4 @@
         return toDump
     end
 end
+

```

---

# Migration Report: scripts\lib\engine.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\lib\engine.lua
+++ patched/scripts\lib\engine.lua
@@ -1,3 +1,4 @@
+#version 2
 function initEngine()
     -- Holds game engine constants
     Engine = {
@@ -7,4 +8,5 @@
     function Engine:voxelCenterOffset()
         return Transform(Vec(Engine.voxelSize * 0.5, Engine.voxelSize * 0.5, -Engine.voxelSize * 0.5))
     end
-end+end
+

```

---

# Migration Report: scripts\lib\input.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\lib\input.lua
+++ patched/scripts\lib\input.lua
@@ -1,3 +1,4 @@
+#version 2
 function initInput()
     Input = {}
 
@@ -264,4 +265,5 @@
     function Input.cameraY()
         return 'cameraY'
     end
-end+end
+

```

---

# Migration Report: scripts\managers\soundManager.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\managers\soundManager.lua
+++ patched/scripts\managers\soundManager.lua
@@ -1,3 +1,4 @@
+#version 2
 function initSoundManager()
     SoundManager = {
         soundVolume = 0.5,
@@ -9,21 +10,22 @@
 
     function SoundManager:tick()
         if InputPressed('usetool') and GetInt('game.tool.hypnotox_flamethrower.ammo') > 0 then
-            PlaySound(self.soundFlamethrowerStart, GetPlayerTransform().pos, self.soundVolume)
-            PlaySound(self.soundFlamethrowerActive, GetPlayerTransform().pos, self.soundVolume)
+            PlaySound(self.soundFlamethrowerStart, GetPlayerTransform(playerId).pos, self.soundVolume)
+            PlaySound(self.soundFlamethrowerActive, GetPlayerTransform(playerId).pos, self.soundVolume)
         end
 
         if InputReleased('usetool') and GetInt('game.tool.hypnotox_flamethrower.ammo') > 0 then
-            PlaySound(self.soundFlamethrowerEnd, GetPlayerTransform().pos, self.soundVolume)
+            PlaySound(self.soundFlamethrowerEnd, GetPlayerTransform(playerId).pos, self.soundVolume)
         end
 
         if InputDown('usetool') and GetInt('game.tool.hypnotox_flamethrower.ammo') > 0 then
-            PlayLoop(self.soundFlamethrowerActive, GetPlayerTransform().pos, self.soundVolume)
+            PlayLoop(self.soundFlamethrowerActive, GetPlayerTransform(playerId).pos, self.soundVolume)
         end
 
         if not self.outOfAmmo and GetInt('game.tool.hypnotox_flamethrower.ammo') == 0 then
-            PlaySound(self.soundFlamethrowerEnd, GetPlayerTransform().pos, self.soundVolume)
+            PlaySound(self.soundFlamethrowerEnd, GetPlayerTransform(playerId).pos, self.soundVolume)
             self.outOfAmmo = true
         end
     end
-end+end
+

```

---

# Migration Report: scripts\nozzle.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\nozzle.lua
+++ patched/scripts\nozzle.lua
@@ -1,3 +1,4 @@
+#version 2
 function initNozzle()
     Nozzle = {}
 
@@ -52,7 +53,7 @@
     function Nozzle:getFlameVelocity()
         local nozzle = self:getNozzleTransform()
         local direction = TransformToParentVec(nozzle, Vec(0, 0, -1))
-        direction = VecAdd(direction, GetPlayerTransform())
+        direction = VecAdd(direction, GetPlayerTransform(playerId))
 
         return VecScale(direction, Knob.flameVelocity * 2)
     end
@@ -90,4 +91,5 @@
             spawnParticles(flameVelocity, lifetime)
         end
     end
-end+end
+

```
