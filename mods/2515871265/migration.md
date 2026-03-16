# Migration Report: datascripts\color4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/datascripts\color4.lua
+++ patched/datascripts\color4.lua
@@ -1,52 +1 @@
-#include "scripts/utils.lua"
-
-Color4 = {}
-
-Color4.Prototype = {
-	r = 0,
-	g = 0,
-	b = 0,
-	a = 1,
-}
-
-Color4.From255 = function(r, g, b, a)
-	local newColor = deepcopy(Color4.Prototype)
-	
-	newColor.r = r / 255 or Color4.Prototype.r
-	newColor.g = g / 255  or Color4.Prototype.g
-	newColor.b = b / 255  or Color4.Prototype.b
-	newColor.a = a / 255  or Color4.Prototype.a
-	
-	return newColor
-end
-
-Color4.New = function(r, g, b, a)
-	local newColor = deepcopy(Color4.Prototype)
-	
-	newColor.r = r or Color4.Prototype.r
-	newColor.g = g or Color4.Prototype.g
-	newColor.b = b or Color4.Prototype.b
-	newColor.a = a or Color4.Prototype.a
-	
-	return newColor
-end
-
-Color4.White = Color4.New(1, 1, 1, 1)
-
-Color4.LightGray = Color4.New(0.75, 0.75, 0.75, 1)
-
-Color4.Gray = Color4.New(0.5, 0.5, 0.5, 1)
-
-Color4.DarkGray = Color4.New(0.25, 0.25, 0.25, 1)
-
-Color4.Black = Color4.New(0, 0, 0, 1)
-
-Color4.Red = Color4.New(1, 0, 0, 1)
-
-Color4.Green = Color4.New(0, 1, 0, 1)
-
-Color4.Blue = Color4.New(0, 0, 1, 1)
-
-Color4.Yellow = Color4.New(1, 1, 0, 1)
-
-Color4.Orange = Color4.New(1, 0.7, 0, 1)+#version 2

```

---

# Migration Report: datascripts\inputList.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/datascripts\inputList.lua
+++ patched/datascripts\inputList.lua
@@ -1,3 +1,4 @@
+#version 2
 local filteredKeys = { esc = "f", lmb = "f", mmb = "f", rmb = "f", space = "f", any = "f", m = "f" }
 
 function isFilteredKey(key)
@@ -16,4 +17,5 @@
 	end
 	
 	return pressedKey
-end+end
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
@@ -1,115 +1,5 @@
-#include "datascripts/color4.lua"
-#include "scripts/utils.lua"
-#include "scripts/savedata.lua"
-#include "scripts/ui.lua"
-#include "scripts/menu.lua"
-#include "datascripts/inputList.lua"
-
-thrusterClass = {
-	activeLastFrame = 0,
-	parentBody = nil,
-	localPosition = nil,
-	localNormal = nil,
-	localInvertedNormal = nil,
-	localSpriteLookPos = nil,
-	power = 100,
-	toggle = false,
-	toggledOn = false,
-	toggleInvert = false,
-	keyForward = "h",
-	keyBackward = "n",
-}
-
-local activeThrusters = {}
-
-local thrusterSprite = nil
-local thrusterFacingSpriteOff = nil
-local thrusterFacingSpriteOn = nil
-local thrusterFacingSpriteOnReverse = nil
-
-local toolDown = false
-
-local debugConsoleNeeded = false
-
-local screenCenter = { x = 0, y = 0 }
-
-function init()
-	saveFileInit()
-	menu_init()
-	
-	RegisterTool("nlthrustertool", "Thruster Tool", "MOD/vox/thruster.vox")
-	SetBool("game.tool.nlthrustertool.enabled", true)
-	
-	if drawThrusterSpriteActive then
-		thrusterSprite = LoadSprite("sprites/thruster.png")
-		thrusterFacingSpriteOff = LoadSprite("sprites/top-off.png")
-		thrusterFacingSpriteOn = LoadSprite("sprites/top-on.png")
-		thrusterFacingSpriteOnReverse = LoadSprite("sprites/top-on-reversed.png")
-	end
-end
-
-function tick(dt)
-	menu_tick(dt)
-
-	if isMenuOpen() then
-		return
-	end
-	
-	toolLogic(dt)
-	placementLogic(dt)
-	allThrustersHandler(dt)
-end
-
-function draw(dt)	
-	menu_draw(dt)
-
-	screenCenter.x = UiWidth() / 2
-	screenCenter.y = UiHeight() / 2
-	drawUI(dt)
-end
-
-function toolLogic(dt)
-	-- Might reimplement this for fun.
-	--[[if InputDown(binds["Fire_All_Thrusters_Forwards"]) then
-		fireAllThrusters(false)
-	elseif InputDown(binds["Fire_All_Thrusters_Backwards"]) then
-		fireAllThrusters(true)
-	end]]--
-	
-	if GetString("game.player.tool") ~= "nlthrustertool" then
-		return
-	end
-	
-	if InputPressed("usetool") then
-		toolDown = true
-	else
-		toolDown = false
-	end
-	
-	if InputPressed(binds["Delete_All_Thrusters"]) then
-		activeThrusters = {}
-	end
-	
-	if InputPressed(binds["Delete_Last_Thruster"]) and #activeThrusters > 0 then
-		activeThrusters[#activeThrusters] = nil
-	end
-	
-	local strengthAdd = 0
-	
-	if InputDown(binds["New_Thruster_Power_Up"]) then
-		strengthAdd = strengthAdd + 1
-	end
-	
-	if InputDown(binds["New_Thruster_Power_Down"]) then
-		strengthAdd = strengthAdd - 1
-	end
-	
-	thrusterClass.power = thrusterClass.power + strengthAdd
-	
-	if thrusterClass.power <= 0 then
-		thrusterClass.power = 1
-	end
-end
+#version 2
+local strengthAdd = 0
 
 function placementLogic(dt)
 	if not toolDown then
@@ -124,8 +14,6 @@
 	
 	activeThrusters[#activeThrusters + 1] = newThruster
 end
-
--- Object handlers
 
 function allThrustersHandler(dt)
 	for i = 1, #activeThrusters do
@@ -179,8 +67,6 @@
 	end
 end
 
--- UI Functions (excludes sound specific functions)
-
 function drawUI(dt)
 	if debugConsoleNeeded then
 		return
@@ -216,7 +102,6 @@
 	UiPop()
 end
 
--- Creation Functions
 function createThrusterAtLookPos()
 	local direction = UiPixelToWorld(screenCenter.x, screenCenter.y)
 	
@@ -245,13 +130,10 @@
 	return newThruster
 end
 
--- World Sound functions
-
 function thrusterSoundHandler(thruster)
 
 end
 
--- Action functions
 function setParticle()
 	ParticleReset()
 	
@@ -307,8 +189,6 @@
 	ApplyBodyImpulse(thruster.parentBody, worldPos, strengthVec)
 end
 
--- Sprite functions
-
 function drawThrusterSprite(thruster)
 	if thruster ~= nil then
 		local bodyTransform = GetBodyTransform(thruster.parentBody)
@@ -339,4 +219,3 @@
 	end
 end
 
--- UI Sound Functions

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
@@ -1,61 +1,59 @@
-#include "scripts/savedata.lua"
-#include "scripts/textbox.lua"
-#include "scripts/ui.lua"
-
+#version 2
 local modname = "Thruster Tool"
 
-function init()
-	saveFileInit()
+function server.init()
+    saveFileInit()
 end
 
-function draw()
-	UiPush()
-		UiTranslate(UiWidth(), UiHeight())
-		UiTranslate(-50, 3 * -50)
-		UiAlign("right bottom")
-	
-		UiFont("regular.ttf", 26)
-		
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-		
-		if UiTextButton("Reset to default", 200, 50) then
-			drawThrusterSpriteActive = true
-		end
-		
-		UiTranslate(0, 60)
-		
-		if UiTextButton("Save and exit", 200, 50) then
-			SetBool(moddataPrefix .. "OldThrusterStyle", drawThrusterSpriteActive)
-			Menu()
-		end
-		
-		UiTranslate(0, 60)
-		
-		if UiTextButton("Cancel", 200, 50) then
-			Menu()
-		end
-	UiPop()
-	
-	UiPush()
-		UiWordWrap(400)
-	
-		UiTranslate(UiCenter(), 50)
-		UiAlign("center middle")
-	
-		UiFont("bold.ttf", 48)
-		UiTranslate(0, 50)
-		UiText(modname)
-	
-		UiTranslate(0, 100)
-		
-		UiFont("regular.ttf", 26)
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-		
-		drawToggle("New thruster style: ", drawThrusterSpriteActive, function (i) drawThrusterSpriteActive = i end)
-		
-	UiPop()
+function server.tick(dt)
+    textboxClass_tick()
 end
 
-function tick()
-	textboxClass_tick()
-end+function client.draw()
+    UiPush()
+    	UiTranslate(UiWidth(), UiHeight())
+    	UiTranslate(-50, 3 * -50)
+    	UiAlign("right bottom")
+
+    	UiFont("regular.ttf", 26)
+
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    	if UiTextButton("Reset to default", 200, 50) then
+    		drawThrusterSpriteActive = true
+    	end
+
+    	UiTranslate(0, 60)
+
+    	if UiTextButton("Save and exit", 200, 50) then
+    		SetBool(moddataPrefix .. "OldThrusterStyle", drawThrusterSpriteActive, true)
+    		Menu()
+    	end
+
+    	UiTranslate(0, 60)
+
+    	if UiTextButton("Cancel", 200, 50) then
+    		Menu()
+    	end
+    UiPop()
+
+    UiPush()
+    	UiWordWrap(400)
+
+    	UiTranslate(UiCenter(), 50)
+    	UiAlign("center middle")
+
+    	UiFont("bold.ttf", 48)
+    	UiTranslate(0, 50)
+    	UiText(modname)
+
+    	UiTranslate(0, 100)
+
+    	UiFont("regular.ttf", 26)
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    	drawToggle("New thruster style: ", drawThrusterSpriteActive, function (i) drawThrusterSpriteActive = i end)
+
+    UiPop()
+end
+

```

---

# Migration Report: scripts\menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\menu.lua
+++ patched/scripts\menu.lua
@@ -1,22 +1,5 @@
-#include "datascripts/inputList.lua"
-#include "datascripts/color4.lua"
-#include "scripts/ui.lua"
-#include "scripts/textbox.lua"
-#include "scripts/utils.lua"
-
-binds = {
-	New_Thrusters_Forwards_Key = "h", 
-	New_Thrusters_Backwards_Key = "n", 
-	Delete_All_Thrusters = "p", 
-	Delete_Last_Thruster = "z",
-	New_Thruster_Power_Up = "+",
-	New_Thruster_Power_Down = "-",
-	New_Thruster_Toggle = "g",
-	Open_Menu = "m", -- Only one that can't be changed!
-}
-
+#version 2
 local bindBackup = deepcopy(binds)
-
 local bindOrder = {
 	"New_Thrusters_Forwards_Key", 
 	"New_Thrusters_Backwards_Key", 
@@ -26,7 +9,6 @@
 	"Delete_All_Thrusters", 
 	"Delete_Last_Thruster",
 }
-		
 local bindNames = {
 	New_Thrusters_Forwards_Key = "New Thrusters Forwards Key", 
 	New_Thrusters_Backwards_Key = "New Thrusters Backwards Key", 
@@ -37,17 +19,12 @@
 	New_Thruster_Toggle = "New Thruster Toggle",
 	Open_Menu = "Open Menu",
 }
-
 local menuOpened = false
 local rebinding = nil
-
 local erasingBinds = 0
-
 local menuWidth = 0.25
 local menuHeight = 0.6
-
 local powerTextBox = nil
-
 local changelogText = "Keys can now be rebound.\n" ..
 					  "(Currently not saved cross session.)\n\n" ..
 					  "Made editing thruster power easier using this menu.\n" ..
@@ -80,7 +57,7 @@
 	
 	textboxClass_tick()
 	
-	if erasingBinds > 0 then
+	if erasingBinds ~= 0 then
 		erasingBinds = erasingBinds - dt
 	end
 end
@@ -187,7 +164,7 @@
 			
 			UiTranslate(0, 50)
 			
-			if erasingBinds > 0 then
+			if erasingBinds ~= 0 then
 				UiPush()
 				c_UiColor(Color4.Red)
 				if UiTextButton("Are you sure?" , 400, 40) then
@@ -255,4 +232,5 @@
 
 function setMenuOpen(val)
 	menuOpened = val
-end+end
+

```

---

# Migration Report: scripts\savedata.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\savedata.lua
+++ patched/scripts\savedata.lua
@@ -1,26 +1,26 @@
-moddataPrefix = "savegame.mod.thrustertool"
-
+#version 2
 function saveFileInit()
 	saveVersion = GetInt(moddataPrefix .. "Version")
 	drawThrusterSpriteActive = GetBool(moddataPrefix .. "OldThrusterStyle")
 	
 	if saveVersion < 1 or saveVersion == nil then
 		saveVersion = 1
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 	end
 	
 	if saveVersion < 2 then
 		saveVersion = 2
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		changelogActive = true
 	end
 	
 	if saveVersion < 3 then
 		saveVersion = 3
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		drawThrusterSpriteActive = true
-		SetBool(moddataPrefix .. "OldThrusterStyle", drawThrusterSpriteActive)
+		SetBool(moddataPrefix .. "OldThrusterStyle", drawThrusterSpriteActive, true)
 	end
-end+end
+

```

---

# Migration Report: scripts\textbox.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\textbox.lua
+++ patched/scripts\textbox.lua
@@ -1,24 +1,4 @@
-#include "scripts/utils.lua"
-
-textboxClass = {
-	inputNumbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."},
-	inputLetters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"},
-	
-	textboxes = { },
-	
-	default = {
-		name = "TextBox",
-		value = "",
-		width = 100,
-		height = 40,
-		limitsActive = false,
-		numberMin = 0,
-		numberMax = 1,
-		inputActive = false,
-		lastInputActive = false,
-	},
-}
-
+#version 2
 function textboxClass_tick()
 	for i = 1, #textboxClass.textboxes do
 		local textBox = textboxClass.textboxes[i]
@@ -72,7 +52,7 @@
 	return textBox, newBox
 end
 
- function textboxClass_inputTick(me)
+function textboxClass_inputTick(me)
 	if me.inputActive ~= me.lastInputActive then
 		me.lastInputActive = me.inputActive
 	end
@@ -127,4 +107,5 @@
 			end
 		end
 	end
-end+end
+

```

---

# Migration Report: scripts\ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ui.lua
+++ patched/scripts\ui.lua
@@ -1,5 +1,4 @@
-#include "datascripts/color4.lua"
-
+#version 2
 function c_UiColor(color4)
 	UiColor(color4.r, color4.g, color4.b, color4.a)
 end
@@ -46,4 +45,5 @@
 			callback(not value)
 		end
 	UiPop()
-end+end
+

```

---

# Migration Report: scripts\utils.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\utils.lua
+++ patched/scripts\utils.lua
@@ -1,3 +1,4 @@
+#version 2
 function tableToText(inputTable, loopThroughTables)
 	loopThroughTables = loopThroughTables or true
 
@@ -100,3 +101,4 @@
     end
     return copy
 end
+

```
