# Migration Report: datascripts\color4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/datascripts\color4.lua
+++ patched/datascripts\color4.lua
@@ -1,58 +1 @@
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
-Color4.Copy = function(color)
-	local newColor = deepcopy(color)
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
 local filteredKeys = { esc = "f", 
 					   lmb = "f", 
 					   mmb = "f", 
@@ -27,4 +28,5 @@
 	end
 	
 	return pressedKey
-end+end
+

```

---

# Migration Report: datascripts\keybinds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/datascripts\keybinds.lua
+++ patched/datascripts\keybinds.lua
@@ -1,21 +1,5 @@
-#include "scripts/utils.lua"
-
-binds = {
-	Clear_All_Fires = "l",
-	Toggle_No_Fire = "k",
-}
-
+#version 2
 local bindBackup = deepcopy(binds)
-
-bindOrder = {
-	"Clear_All_Fires",
-	"Toggle_No_Fire",
-}
-		
-bindNames = {
-	Clear_All_Fires = "Clear All Fires",
-	Toggle_No_Fire = "Toggle No Fire",
-}
 
 function resetKeybinds()
 	binds = deepcopy(bindBackup)
@@ -23,4 +7,5 @@
 
 function getFromBackup(id)
 	return bindBackup[id]
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
@@ -1,110 +1,81 @@
-#include "scripts/utils.lua"
-#include "scripts/savedata.lua"
-#include "scripts/menu.lua"
-#include "datascripts/keybinds.lua"
-#include "datascripts/inputList.lua"
-
-toolName = "adjustablefire"
-toolReadableName = "Adjustable Fire"
-
+#version 2
 local menu_disabled = false
-
-fireSpread = 1
-maxFires = 200
-
 local fireClearActive = false
 
-function init()
-	saveFileInit()
-	menu_init()
-	
-	SetInt("game.fire.maxcount", maxFires)
-	SetFloat("game.fire.spread", fireSpread)
+function server.init()
+    saveFileInit()
+    menu_init()
+    SetInt("game.fire.maxcount", maxFires, true)
+    SetFloat("game.fire.spread", fireSpread, true)
 end
 
-function tick(dt)
-	if not menu_disabled then
-		menu_tick(dt)
-	end
-	
-	if InputPressed(binds["Toggle_No_Fire"]) and not isMenuOpen() then
-		fireClearActive = not fireClearActive
-	end
-	
-	if InputPressed(binds["Clear_All_Fires"]) or (fireClearActive and GetFireCount() > 0) then
-		local playerPos = GetPlayerTransform().pos
-		local range = 500
-		local minVec = VecAdd(playerPos, Vec(-range, -range, -range))
-		local maxVec = VecAdd(playerPos, Vec(range, range, range))
-		
-		RemoveAabbFires(minVec, maxVec)
-	end
+function server.tick(dt)
+    if not menu_disabled then
+    	menu_tick(dt)
+    end
 end
 
-function draw(dt)
-	menu_draw(dt)
-	
-	
-	UiPush()
-		UiAlign("left top")
-		
-		UiTranslate(UiHeight() * 0.02, UiHeight() * 0.02)
-		
-		UiFont("regular.ttf", 26)
-		
-		UiAlign("left top")
-		
-		local margin = 20
-		
-		if showFireCount then
-			local fireCountText = "Fire count: " .. GetFireCount()
-			local fireTextWidth, fireTextHeight = UiGetTextSize(fireCountText)
-			UiColor(0, 0, 0, 0.75)
-		
-			UiRect(fireTextWidth + margin, fireTextHeight + margin / 2)
-			
-			UiTranslate(margin / 2, margin / 4)
-			
-			UiColor(1, 1, 1, 1)
-		
-			UiText(fireCountText)
-			
-			UiTranslate(-margin / 2, -margin / 4)
-			
-			UiTranslate(0, fireTextHeight + margin)
-		end
-		
-		if fireClearActive then
-			local text = "No fire active!"
-			
-			local textWidth, textHeight = UiGetTextSize(text)
-			
-			UiColor(0, 0, 0, 0.75)
-			
-			UiRect(textWidth + margin, textHeight + margin / 2)
-			
-			UiTranslate(margin / 2, margin / 4)
-			
-			UiColor(1, 1, 1, 1)
-			
-			UiText(text)
-		end
-	UiPop()
+function client.tick(dt)
+    if InputPressed(binds["Toggle_No_Fire"]) and not isMenuOpen() then
+    	fireClearActive = not fireClearActive
+    end
+    if InputPressed(binds["Clear_All_Fires"]) or (fireClearActive and GetFireCount() > 0) then
+    	local playerPos = GetPlayerTransform(playerId).pos
+    	local range = 500
+    	local minVec = VecAdd(playerPos, Vec(-range, -range, -range))
+    	local maxVec = VecAdd(playerPos, Vec(range, range, range))
+
+    	RemoveAabbFires(minVec, maxVec)
+    end
 end
 
--- UI Functions (excludes sound specific functions)
--- Creation Functions
+function client.draw()
+    menu_draw(dt)
 
--- Object handlers
+    UiPush()
+    	UiAlign("left top")
 
--- Tool Functions
+    	UiTranslate(UiHeight() * 0.02, UiHeight() * 0.02)
 
--- Particle Functions
+    	UiFont("regular.ttf", 26)
 
--- Action functions
+    	UiAlign("left top")
 
--- Sprite Functions
+    	local margin = 20
 
--- UI Sound Functions
+    	if showFireCount then
+    		local fireCountText = "Fire count: " .. GetFireCount()
+    		local fireTextWidth, fireTextHeight = UiGetTextSize(fireCountText)
+    		UiColor(0, 0, 0, 0.75)
 
--- Misc Functions+    		UiRect(fireTextWidth + margin, fireTextHeight + margin / 2)
+
+    		UiTranslate(margin / 2, margin / 4)
+
+    		UiColor(1, 1, 1, 1)
+
+    		UiText(fireCountText)
+
+    		UiTranslate(-margin / 2, -margin / 4)
+
+    		UiTranslate(0, fireTextHeight + margin)
+    	end
+
+    	if fireClearActive then
+    		local text = "No fire active!"
+
+    		local textWidth, textHeight = UiGetTextSize(text)
+
+    		UiColor(0, 0, 0, 0.75)
+
+    		UiRect(textWidth + margin, textHeight + margin / 2)
+
+    		UiTranslate(margin / 2, margin / 4)
+
+    		UiColor(1, 1, 1, 1)
+
+    		UiText(text)
+    	end
+    UiPop()
+end
+

```

---

# Migration Report: options_disabled.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/options_disabled.lua
+++ patched/options_disabled.lua
@@ -1,136 +1,4 @@
-#include "scripts/ui.lua"
-#include "scripts/savedata.lua"
-#include "scripts/textbox.lua"
-#include "datascripts/keybinds.lua"
-#include "datascripts/inputList.lua"
-#include "datascripts/color4.lua"
-
-local modname = "Adjustable Fire"
-
-local resettingBinds = 0
-local rebinding = nil
-
-function init()
-	saveFileInit()
-	textboxClass_setTextBoxBg()
-	textboxClass_setDescBoxBg()
-end
-
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
-			-- DEFAULTS
-			resetKeybinds()
-		end
-		
-		UiTranslate(0, 60)
-		
-		if UiTextButton("Save and exit", 200, 50) then
-			saveKeyBinds()
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
-		
-		setupTextBoxes()
-		
-		UiPush()
-			UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-			
-			if resettingBinds > 0 then
-				UiColor(1, 0, 0, 1)
-				if UiTextButton("Are you sure?") then
-					resetKeybinds()
-					resettingBinds = 0
-				end
-			else
-				if UiTextButton("Reset Keybinds") then
-					resettingBinds = 5
-				end
-			end
-		UiPop()
-		
-		UiTranslate(0, 50)
-		
-		UiPush()
-			UiTranslate(0, 50)
-			for i = 1, #bindOrder do
-				local id = bindOrder[i]
-				local key = binds[id]
-				drawRebindable(id, key)
-				UiTranslate(0, 50)
-			end
-		UiPop()
-		
-		UiTranslate(0, 50 * (#bindOrder + 1))
-		
-		--textboxClass_render(resolutionBox)
-	UiPop()
-	
-	textboxClass_drawDescriptions()
-end
-
-function tick(dt)
-	textboxClass_tick()
-	
-	if resettingBinds > 0 then
-		resettingBinds = resettingBinds - dt
-	end
-	
-	if rebinding ~= nil then
-		local lastKeyPressed = getKeyPressed()
-		
-		if lastKeyPressed ~= nil then
-			binds[rebinding] = lastKeyPressed
-			rebinding = nil
-		end
-	end
-end
-
-function setupTextBoxes()
-	--[[local textBox01, newBox01 = textboxClass_getTextBox(1)
-	
-	if newBox01 then
-		textBox01.name = "Resolution"
-		textBox01.value = resolution .. ""
-		textBox01.numbersOnly = true
-		textBox01.limitsActive = true
-		textBox01.numberMin = 1
-		textBox01.numberMax = 500
-		textBox01.description = "The amount of pixels wide and high.\n Min: 1\nDefault: 50\nMax: 500"
-		textBox01.onInputFinished = function(v) resolution = tonumber(v) end
-		
-		resolutionBox = textBox01
-	end]]--
-end
-
+#version 2
 function drawRebindable(id, key)
 	UiPush()
 		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
@@ -154,4 +22,5 @@
 			rebinding = id
 		end
 	UiPop()
-end+end
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
@@ -1,285 +1,4 @@
-#include "datascripts/inputList.lua"
-#include "datascripts/keybinds.lua"
-#include "scripts/ui.lua"
-#include "scripts/utils.lua"
-#include "scripts/textbox.lua"
-
-local menuOpened = false
-local menuOpenLastFrame = false
-
-local rebinding = nil
-
-local erasingBinds = 0
-local erasingValues = 0
-
-local menuWidth = 0.20
-local menuHeight = 0.35
-
-local fireSpreadBox = nil
-local maxFiresBox = nil
-
-function menu_init()
-	
-end
-
-function menu_tick(dt)
-	if PauseMenuButton(toolReadableName .. " Settings") then
-		menuOpened = true
-	end
-	
-	if menuOpened and not menuOpenLastFrame then
-		menuUpdateActions()
-		menuOpenActions()
-	end
-	
-	menuOpenLastFrame = menuOpened
-	
-	if rebinding ~= nil then
-		local lastKeyPressed = getKeyPressed()
-		
-		if lastKeyPressed ~= nil then
-			binds[rebinding] = lastKeyPressed
-			rebinding = nil
-		end
-	end
-	
-	textboxClass_tick()
-	
-	if erasingBinds > 0 then
-		erasingBinds = erasingBinds - dt
-	end
-end
-
-function drawTitle()
-	UiPush()
-		UiFont("bold.ttf", 45)
-		
-		local titleText = toolReadableName .. " Settings"
-		
-		local titleBoxWidth, titleBoxHeight = UiGetTextSize(titleText)
-		
-		UiTranslate(0, -40 - titleBoxHeight / 2)
-		
-		UiPush()
-			UiColorFilter(0, 0, 0, 0.25)
-			UiImageBox("MOD/sprites/square.png", titleBoxWidth + 20, titleBoxHeight + 20, 10, 10)
-		UiPop()
-		
-		UiAlign("center middle")
-		
-		UiText(titleText)
-	UiPop()
-end
-
-function bottomMenuButtons()
-	UiPush()
-		UiFont("regular.ttf", 26)
-	
-		UiButtonImageBox("MOD/sprites/square.png", 6, 6, 0, 0, 0, 0.5)
-		
-		UiAlign("center bottom")
-		
-		local buttonWidth = 250
-		
-		UiPush()
-			UiTranslate(0, -50)
-			if erasingValues > 0 then
-				UiPush()
-				c_UiColor(Color4.Red)
-				if UiTextButton("Are you sure?" , buttonWidth, 40) then
-					resetValues()
-					erasingValues = 0
-				end
-				UiPop()
-			else
-				if UiTextButton("Reset values to defaults" , buttonWidth, 40) then
-					erasingValues = 5
-				end
-			end
-		UiPop()
-		
-		
-		--[[UiPush()
-			--UiAlign("right bottom")
-			--UiTranslate(230, 0)
-			UiTranslate(0, -50)
-			if erasingBinds > 0 then
-				UiPush()
-				c_UiColor(Color4.Red)
-				if UiTextButton("Are you sure?" , buttonWidth, 40) then
-					resetKeybinds()
-					erasingBinds = 0
-				end
-				UiPop()
-			else
-				if UiTextButton("Reset binds to defaults" , buttonWidth, 40) then
-					erasingBinds = 5
-				end
-			end
-		UiPop()]]--
-		
-		
-		UiPush()
-			--UiAlign("left bottom")
-			--UiTranslate(-230, 0)
-			if UiTextButton("Close" , buttonWidth, 40) then
-				menuCloseActions()
-			end
-		UiPop()
-	UiPop()
-end
-
-function disableButtonStyle()
-	UiButtonImageBox("MOD/sprites/square.png", 6, 6, 0, 0, 0, 0.5)
-	UiButtonPressColor(1, 1, 1)
-	UiButtonHoverColor(1, 1, 1)
-	UiButtonPressDist(0)
-end
-
-function greenAttentionButtonStyle()
-	local greenStrength = math.sin(GetTime() * 5) - 0.5
-	local otherStrength = 0.5 - greenStrength
-	
-	if greenStrength < otherStrength then
-		greenStrength = otherStrength
-	end
-	
-	UiButtonImageBox("MOD/sprites/square.png", 6, 6, otherStrength, greenStrength, otherStrength, 0.5)
-end
-
-function menu_draw(dt)
-	if not isMenuOpen() then
-		return
-	end
-	
-	UiMakeInteractive()
-	
-	UiPush()
-		UiBlur(0.75)
-		
-		UiAlign("center middle")
-		UiTranslate(UiWidth() * 0.5, UiHeight() * 0.5)
-		
-		UiPush()
-			UiColorFilter(0, 0, 0, 0.25)
-			UiImageBox("MOD/sprites/square.png", UiWidth() * menuWidth, UiHeight() * menuHeight, 10, 10)
-		UiPop()
-		
-		UiWordWrap(UiWidth() * menuWidth)
-		
-		UiTranslate(0, -UiHeight() * (menuHeight / 2))
-		
-		drawTitle()
-		
-		UiTranslate(UiWidth() * (menuWidth / 10), 0)
-		
-		--UiTranslate(0, 30)
-		
-		UiFont("regular.ttf", 26)
-		UiAlign("left middle")
-		
-		UiPush()
-			UiTranslate(0, 50)
-			for i = 1, #bindOrder do
-				local id = bindOrder[i]
-				local key = binds[id]
-				drawRebindable(id, key)
-				UiTranslate(0, 50)
-			end
-		UiPop()
-		
-		setupTextBoxes()
-		
-		UiTranslate(0, 50 * (#bindOrder + 1))
-		
-		textboxClass_render(maxFiresBox)
-		
-		UiTranslate(0, 50)
-		
-		textboxClass_render(fireSpreadBox)
-		
-		UiTranslate(-150, 50)
-		
-		drawToggle("Show fire count: ", showFireCount, function(i) showFireCount = i end)
-	UiPop()
-	
-	UiPush()
-		UiTranslate(UiWidth() * 0.5, UiHeight() * 0.5)
-		--UiTranslate(0, -UiHeight() * (menuHeight / 2))
-		UiTranslate(0, UiHeight() * (menuHeight / 2) - 10)
-		
-		bottomMenuButtons()
-	UiPop()
-
-	textboxClass_drawDescriptions()
-end
-
-function setupTextBoxes()
-	local textBox01, newBox01 = textboxClass_getTextBox(1)
-	local textBox02, newBox02 = textboxClass_getTextBox(2)
-	
-	if newBox01 then
-		textBox01.name = "Fire Spread"
-		textBox01.value = fireSpread .. ""
-		textBox01.numbersOnly = true
-		textBox01.limitsActive = true
-		textBox01.numberMin = 0
-		textBox01.numberMax = 99999999999
-		textBox01.description = "How fast the fire spreads.\nMin: 0\nDefault: 1\nMax: 99999999999"
-		textBox01.onInputFinished = function(v) SetFloat("game.fire.spread", tonumber(v)) fireSpread = tonumber(v) end
-		
-		fireSpreadBox = textBox01
-	end
-	
-	if newBox02 then
-		textBox02.name = "Max Fires"
-		textBox02.value = maxFires .. ""
-		textBox02.numbersOnly = true
-		textBox02.limitsActive = true
-		textBox02.numberMin = 0
-		textBox02.numberMax = 1215752192
-		textBox02.description = "Max amount of fires.\nSetting to 0 doesn't actually disable fires.\nEngine tries to limit to 1400.\nMin: 0\nDefault: 200\nMax: 1215752192"
-		textBox02.onInputFinished = function(v) SetInt("game.fire.maxcount", tonumber(v)) maxFires = tonumber(v) end
-		
-		maxFiresBox = textBox02
-	end
-end
-
-function drawRebindable(id, key)
-	UiPush()
-		UiButtonImageBox("MOD/sprites/square.png", 6, 6, 0, 0, 0, 0.5)
-	
-		--UiTranslate(UiWidth() * menuWidth / 1.5, 0)
-	
-		UiAlign("right middle")
-		UiText(bindNames[id] .. "")
-		
-		--UiTranslate(UiWidth() * menuWidth * 0.1, 0)
-		
-		UiAlign("left middle")
-		
-		if rebinding == id then
-			c_UiColor(Color4.Green)
-		else
-			c_UiColor(Color4.Yellow)
-		end
-		
-		if UiTextButton(key:upper(), 40, 40) then
-			rebinding = id
-		end
-	UiPop()
-end
-
-function menuOpenActions()
-	
-end
-
-function menuUpdateActions()
-	--[[if resolutionBox ~= nil then
-		resolutionBox.value = resolution .. ""
-	end]]--
-end
-
+#version 2
 function menuCloseActions()
 	menuOpened = false
 	rebinding = nil
@@ -296,8 +15,8 @@
 	fireSpreadBox.value = 1
 	showFireCount = false
 	
-	SetInt("game.fire.maxcount", 200)
-	SetFloat("game.fire.spread", 1)
+	SetInt("game.fire.maxcount", 200, true)
+	SetFloat("game.fire.spread", 1, true)
 end
 
 function isMenuOpen()
@@ -306,4 +25,5 @@
 
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
@@ -1,7 +1,4 @@
-#include "datascripts/keybinds.lua"
-
-moddataPrefix = "savegame.mod.adjustablefire"
-
+#version 2
 function saveFileInit()
 	saveVersion = GetInt(moddataPrefix .. "Version")
 	
@@ -13,21 +10,21 @@
 	
 	if saveVersion < 1 or saveVersion == nil then
 		saveVersion = 1
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		maxFires = 200
-		SetInt(moddataPrefix .. "MaxFires", maxFires)
+		SetInt(moddataPrefix .. "MaxFires", maxFires, true)
 		
 		fireSpread = 1
-		SetFloat(moddataPrefix .. "FireSpread", fireSpread)
+		SetFloat(moddataPrefix .. "FireSpread", fireSpread, true)
 	end
 	
 	if saveVersion < 2 or saveVersion == nil then
 		saveVersion = 2
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		showFireCount = false
-		SetBool(moddataPrefix .. "ShowFireCount", showFireCount)
+		SetBool(moddataPrefix .. "ShowFireCount", showFireCount, true)
 	end
 end
 
@@ -49,12 +46,13 @@
 		local currBindID = bindOrder[i]
 		local boundKey = binds[currBindID]
 		
-		SetString(moddataPrefix .. "Keybind" .. currBindID, boundKey)
+		SetString(moddataPrefix .. "Keybind" .. currBindID, boundKey, true)
 	end
 end
 
 function saveFloatValues()
-	SetInt(moddataPrefix .. "MaxFires", maxFires)
-	SetFloat(moddataPrefix .. "FireSpread", fireSpread)
-	SetBool(moddataPrefix .. "ShowFireCount", showFireCount)
-end+	SetInt(moddataPrefix .. "MaxFires", maxFires, true)
+	SetFloat(moddataPrefix .. "FireSpread", fireSpread, true)
+	SetBool(moddataPrefix .. "ShowFireCount", showFireCount, true)
+end
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
@@ -1,3 +1,4 @@
+#version 2
 local textboxClass = {
 	name = "TextBox",
 	disabled = false,
@@ -13,38 +14,24 @@
 	lastInputActive = false,
 	onInputFinished = nil,
 }
-
 local inputNumbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "-"}
 local inputLetters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "space"}
-
 local textboxes = {}
-
--- STYLE CONFIG
-
 local font = "regular.ttf"
-
 local descriptionBoxMargin = 20
-
 local defaultTextSize = 26
 local defaultDescriptionTextSize = 26
-
-local textBoxBg = "MOD/sprites/square.png" -- "ui/common/box-outline-6.png"
-local descBoxBg = "MOD/sprites/square.png" -- "ui/hud/infobox.png"
-
+local textBoxBg = "MOD/sprites/square.png"
+local descBoxBg = "MOD/sprites/square.png"
 local textBoxBgBorderWidth = 0
 local textBoxBgBorderHeight = 0
-
 local textBoxDefaultTextColor = {1, 1, 1, 1}
 local textBoxHoverTextColor = {1, 1, 0, 1}
 local textBoxActiveTextColor = {0, 1, 0, 1}
-
 local textBoxBgColor = {0, 0, 0, 0.5}
 local textBoxDisabledBgColor = {0, 0, 0, 0.25}
-
 local descBoxBgColor = {0, 0, 0, 0.75}
 local descBoxTextColor = {1, 1, 1, 1}
-
--- END STYLE CONFIG
 
 function textboxClass_tick()
 	for i = 1, #textboxes do
@@ -178,7 +165,7 @@
 	return textBox, newBox
 end
 
- function textboxClass_inputTick(me)
+function textboxClass_inputTick(me)
 	if me == nil then
 		return
 	end
@@ -312,4 +299,5 @@
 function textboxClass_setDescBoxBg(bg, color)
 	descBoxBg = bg or "ui/hud/infobox.png"
 	descBoxBgColor = color or {1, 1, 1, 0.75}
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
@@ -65,7 +64,6 @@
 	UiPop()
 end
 
-
 function c_DrawBodyOutline(handle, color4)
 	DrawBodyOutline(handle, color4.r, color4.g, color4.b, color4.a)
 end
@@ -84,4 +82,5 @@
 
 function c_DebugLine(a, b, color4)
 	DebugLine(a, b, color4.r, color4.g, color4.b, color4.a)
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
 function tableToText(inputTable, loopThroughTables, useIPairs, addIndex, addNewLine)
 	loopThroughTables = loopThroughTables or true
 	useIPairs = useIPairs or false
@@ -143,3 +144,4 @@
     end
     return copy
 end
+

```
