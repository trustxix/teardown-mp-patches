# Migration Report: main — копия.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main — копия.lua
+++ patched/main — копия.lua
@@ -1,3 +1,4 @@
+#version 2
 function _Module(class, deps)
     _G[class] = _G[class] or {}
     _G[class]._ms_deps = deps or {}
@@ -11,7 +12,6 @@
     end
 end
 
-_Module("Constants")
 function ConstantsLoader()
     Constants.TOOLID = "winch"
     Constants.PLAYER_RANGE = 5
@@ -19,7 +19,6 @@
     Constants.FORCE_MULT = 5.0
 end
 
-_Module("Actions")
 function ActionsLoader()
     Actions._queue = {}
     Actions.IDS = { ATTACH_BEGIN = 1, ATTACH_END = 2, SHRINK = 3, EXTEND = 4, DELETE = 5 }
@@ -32,7 +31,6 @@
     function Actions:Get() return table.remove(self._queue, 1) end
 end
 
-_Module("Winch", {"Constants"})
 function WinchLoader()
     Winch.__index = Winch
     function Winch:New()
@@ -55,7 +53,7 @@
         local p2 = TransformToParentPoint(GetBodyTransform(b2), self._attachments[2].point)
         local cur_len = VecLength(VecSub(p1, p2))
         local delta = cur_len - self._desired_length
-        if delta > 0 then
+        if delta ~= 0 then
             local m = math.min(GetBodyMass(b1) > 0 and GetBodyMass(b1) or 200, GetBodyMass(b2) > 0 and GetBodyMass(b2) or 200)
             local dir = VecNormalize(VecSub(p2, p1))
             local force = VecScale(dir, delta * m * Constants.FORCE_MULT) 
@@ -79,14 +77,13 @@
     end
 end
 
-_Module("WinchTool", {"Actions", "Winch", "Constants"})
 function WinchToolLoader()
     WinchTool.winches = {}
     local winchSnd = nil
 
     function WinchTool:Init()
         RegisterTool("winch", "Winch", "game/tools/wire.vox", 6)
-        SetBool("game.tool.winch.enabled", true)
+        SetBool("game.tool.winch.enabled", true, true)
         winchSnd = LoadLoop("winch.ogg") -- Загрузка петли звука
     end
 
@@ -150,7 +147,7 @@
         end
 
         -- Включаем звук только если нажаты кнопки и есть хотя бы один трос
-        if moving and #self.winches > 0 then
+        if moving and #self.winches ~= 0 then
             PlayLoop(winchsnd, GetCameraTransform().pos, 1.0)
         end
 
@@ -164,5 +161,8 @@
 
 function init() Load("WinchTool") WinchTool:Init() end
 function tick(dt) WinchTool:Tick() end
-function update(dt) WinchTool:Update(dt) end
+function update(dt) Winch
+
+ol:Update(dt) end
 function draw() WinchTool:Draw() end
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
@@ -1,3 +1,4 @@
+#version 2
 function _Module(class, deps)
     _G[class] = _G[class] or {}
     _G[class]._ms_deps = deps or {}
@@ -11,7 +12,6 @@
     end
 end
 
-_Module("Constants")
 function ConstantsLoader()
     Constants.TOOLID = "winch"
     Constants.PLAYER_RANGE = 5
@@ -19,7 +19,6 @@
     Constants.FORCE_MULT = 5.0
 end
 
-_Module("Actions")
 function ActionsLoader()
     Actions._queue = {}
     Actions.IDS = { ATTACH_BEGIN = 1, ATTACH_END = 2, SHRINK = 3, EXTEND = 4, DELETE = 5 }
@@ -32,7 +31,6 @@
     function Actions:Get() return table.remove(self._queue, 1) end
 end
 
-_Module("Winch", {"Constants"})
 function WinchLoader()
     Winch.__index = Winch
     function Winch:New()
@@ -55,7 +53,7 @@
         local p2 = TransformToParentPoint(GetBodyTransform(b2), self._attachments[2].point)
         local cur_len = VecLength(VecSub(p1, p2))
         local delta = cur_len - self._desired_length
-        if delta > 0 then
+        if delta ~= 0 then
             local m = math.min(GetBodyMass(b1) > 0 and GetBodyMass(b1) or 200, GetBodyMass(b2) > 0 and GetBodyMass(b2) or 200)
             local dir = VecNormalize(VecSub(p2, p1))
             local force = VecScale(dir, delta * m * Constants.FORCE_MULT) 
@@ -79,7 +77,6 @@
     end
 end
 
-_Module("WinchTool", {"Actions", "Winch", "Constants"})
 function WinchToolLoader()
     WinchTool.winches = {}
     local winchSnd = nil
@@ -90,7 +87,7 @@
         if slot == 0 then slot = 6 end
 
         RegisterTool("winch", "Winch", "game/tools/wire.vox", slot)
-        SetBool("game.tool.winch.enabled", true)
+        SetBool("game.tool.winch.enabled", true, true)
         winchSnd = LoadLoop("winch.ogg")
     end
 
@@ -152,7 +149,7 @@
             elseif a.id == Actions.IDS.DELETE then self.winches = {} end
         end
 
-        if moving and #self.winches > 0 then
+        if moving and #self.winches ~= 0 then
             PlayLoop(winchSnd, GetCameraTransform().pos, 1.0)
         end
 
@@ -164,7 +161,16 @@
     end
 end
 
-function init() Load("WinchTool") WinchTool:Init() end
-function tick(dt) WinchTool:Tick() end
-function update(dt) WinchTool:Update(dt) end
-function draw() WinchTool:Draw() end
+function init() Loa
+
+"WinchTool") WinchTool:Init() end
+function tick(dt) Wi
+
+chTool:Tick() end
+function update(dt) 
+
+inchTool:Update(dt) end
+function draw() Winc
+
+Tool:Draw() end
+

```

---

# Migration Report: options — копия.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/options — копия.lua
+++ patched/options — копия.lua
@@ -1,20 +1,20 @@
+#version 2
 local STRENGTH_KEY = "savegame.mod.winch.strength"
 local SPEED_KEY    = "savegame.mod.winch.speed"
-
 local activeField = nil
 local inputBuffer = ""
 local animTime = 0
 local lastAlarm = 0
 
-function init()
-    if not HasKey(STRENGTH_KEY) then SetFloat(STRENGTH_KEY, 3.0) end
-    if not HasKey(SPEED_KEY) then SetFloat(SPEED_KEY, 0.05) end
+function server.init()
+    if not HasKey(STRENGTH_KEY) then SetFloat(STRENGTH_KEY, 3.0, true) end
+    if not HasKey(SPEED_KEY) then SetFloat(SPEED_KEY, 0.05, true) end
 end
 
-function draw()
+function client.draw()
     animTime = animTime + GetTimeStep()
     local alpha = math.min(animTime * 2, 1)
-    
+
     UiPush()
         UiColor(0, 0, 0, 0.75 * alpha)
         UiRect(UiWidth(), UiHeight())
@@ -38,17 +38,17 @@
         local val = GetFloat(key)
         local isSelected = (activeField == id)
         local display = isSelected and (inputBuffer .. "|") or string.format("%.3f", val)
-        
+
         UiPush()
             UiTranslate(0, y)
             local isHovered = UiIsMouseInRect(550, 65)
             local bgAlpha = isSelected and 0.25 or (isHovered and 0.15 or 0.1)
-            
+
             UiColor(0.1, 0.1, 0.15, alpha)
             UiImageBox("ui/common/box-solid-6.png", 550, 65, 6, 6)
             UiColor(0, 0.5, 1, bgAlpha * alpha)
             UiImageBox("ui/common/box-outline-6.png", 550, 65, 6, 6)
-            
+
             UiPush()
                 UiTranslate(-250, 0)
                 UiAlign("left middle")
@@ -88,8 +88,8 @@
             UiColor(1, 0.4, 0.4, alpha)
             UiFont("bold.ttf", 24)
             if UiTextButton("RESTORE DEFAULTS", 280, 50) then
-                SetFloat(STRENGTH_KEY, 3.0)
-                SetFloat(SPEED_KEY, 0.05)
+                SetFloat(STRENGTH_KEY, 3.0, true)
+                SetFloat(SPEED_KEY, 0.05, true)
                 UiSound("warning-beep.ogg")
             end
         UiPop()
@@ -116,7 +116,7 @@
             UiFont("bold.ttf", 22)
             UiText("WARNING: HIGH VALUES MAY BREAK THE MOD!")
         UiPop()
-        
+
         -- Пищим раз в 2 секунды, если значение > 5
         if animTime > lastAlarm + 2.0 then
             UiSound("alarm1.ogg")
@@ -144,7 +144,7 @@
         end
         if InputPressed("return") or InputPressed("enter") then
             local n = tonumber(inputBuffer)
-            if n then SetFloat(activeField == "s" and STRENGTH_KEY or SPEED_KEY, n) end
+            if n then SetFloat(activeField == "s" and STRENGTH_KEY or SPEED_KEY, n, true) end
             activeField = nil
             UiSound("valuable.ogg")
         end
@@ -152,3 +152,4 @@
         if InputPressed("esc") then activeField = nil end
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
@@ -1,20 +1,20 @@
+#version 2
 local STRENGTH_KEY = "savegame.mod.winch.strength"
 local SPEED_KEY    = "savegame.mod.winch.speed"
 local SLOT_KEY     = "savegame.mod.winch.slot"
-
 local activeField, inputBuffer, animTime, lastAlarm = nil, "", 0, 0
 
-function init()
-    if not HasKey(STRENGTH_KEY) then SetFloat(STRENGTH_KEY, 3.0) end
-    if not HasKey(SPEED_KEY) then SetFloat(SPEED_KEY, 0.05) end
-    if not HasKey(SLOT_KEY) then SetInt(SLOT_KEY, 6) end
+function server.init()
+    if not HasKey(STRENGTH_KEY) then SetFloat(STRENGTH_KEY, 3.0, true) end
+    if not HasKey(SPEED_KEY) then SetFloat(SPEED_KEY, 0.05, true) end
+    if not HasKey(SLOT_KEY) then SetInt(SLOT_KEY, 6, true) end
 end
 
-function draw()
+function client.draw()
     if UiHeight() > 0 then
         animTime = animTime + GetTimeStep()
         local alpha = math.min(animTime * 2, 1)
-        
+
         -- Фон меню
         UiPush()
             UiColor(0, 0, 0, 0.85 * alpha) 
@@ -24,7 +24,7 @@
         UiAlign("center middle")
         UiPush()
             UiTranslate(UiCenter(), UiMiddle())
-            
+
             -- ЗАГОЛОВОК
             UiPush() 
                 UiTranslate(0, -250) 
@@ -39,7 +39,7 @@
                     UiTranslate(0, y)
                     UiColor(0.15, 0.15, 0.15, alpha) 
                     UiImageBox("ui/common/box-solid-6.png", 650, 85, 6, 6)
-                    
+
                     UiPush() 
                         UiTranslate(-290, 0) 
                         UiAlign("left middle") 
@@ -47,7 +47,7 @@
                         UiColor(0.9, 0.9, 0.9, alpha) 
                         UiText(label) 
                     UiPop()
-                    
+
                     UiPush() 
                         UiTranslate(290, 0) 
                         UiAlign("right middle") 
@@ -91,7 +91,7 @@
                     if UiTextButton("SLOT " .. s, 250, 75) then
                         s = s + 1 
                         if s > 6 then s = 1 end
-                        SetInt(SLOT_KEY, s) 
+                        SetInt(SLOT_KEY, s, true) 
                         UiSound("grab0.ogg")
                     end 
                 UiPop()
@@ -104,9 +104,9 @@
                 UiFont("bold.ttf", 50)
                 -- Растянута на ту же ширину, что и поля ввода (650)
                 if UiTextButton("RESET TO DEFAULTS", 650, 90) then 
-                    SetFloat(STRENGTH_KEY, 3.0) 
-                    SetFloat(SPEED_KEY, 0.05) 
-                    SetInt(SLOT_KEY, 6) 
+                    SetFloat(STRENGTH_KEY, 3.0, true) 
+                    SetFloat(SPEED_KEY, 0.05, true) 
+                    SetInt(SLOT_KEY, 6, true) 
                     UiSound("warning-beep.ogg") 
                 end 
             UiPop()
@@ -138,7 +138,7 @@
             end
             if InputPressed("enter") or InputPressed("return") then
                 local n = tonumber(inputBuffer) 
-                if n then SetFloat(activeField == "str" and STRENGTH_KEY or SPEED_KEY, n) end
+                if n then SetFloat(activeField == "str" and STRENGTH_KEY or SPEED_KEY, n, true) end
                 activeField = nil 
                 UiSound("error.ogg")
             end
@@ -147,3 +147,4 @@
         end
     end
 end
+

```
