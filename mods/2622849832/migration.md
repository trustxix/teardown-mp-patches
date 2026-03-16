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
@@ -1,18 +1,5 @@
-#include "scripts/utils.lua"
-
-binds = {
-	--Disable_Sphere = "r",
-}
-
+#version 2
 local bindBackup = deepcopy(binds)
-
-bindOrder = {
-	--"Disable_Sphere",
-}
-		
-bindNames = {
-	--Disable_Sphere = "Disable Sphere",
-}
 
 function resetKeybinds()
 	binds = deepcopy(bindBackup)
@@ -20,4 +7,5 @@
 
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
@@ -1,83 +1,9 @@
-#include "scripts/utils.lua"
-#include "scripts/savedata.lua"
-#include "scripts/menu.lua"
-#include "datascripts/keybinds.lua"
-#include "datascripts/inputList.lua"
-
-toolName = "firelocator"
-toolReadableName = "Fire Locator"
-
+#version 2
 local menu_disabled = false
 local fireCount = 0
 local fires = {}
-
-range = 100
 local steps = 50
-
-refreshRate = 1
 local currentRefreshTimer = 0
-
-alwaysActive = false
-
-function init()
-	saveFileInit()
-	menu_init()
-	
-	RegisterTool(toolName, toolReadableName, "MOD/vox/tool.vox")
-	SetBool("game.tool." .. toolName .. ".enabled", true)
-	--SetFloat("game.tool." .. toolName .. ".ammo", 100)
-end
-
-function tick(dt)
-	if not menu_disabled then
-		menu_tick(dt)
-	end
-	
-	local isMenuOpenRightNow = isMenuOpen()
-	
-	if isMenuOpenRightNow then
-		return
-	end
-	
-	if (GetString("game.player.tool") ~= toolName or GetPlayerVehicle() ~= 0) and not alwaysActive then
-		return
-	end
-	
-	if GetFireCount() <= 0 then
-		fireCount = 0
-		return
-	end
-	
-	currentRefreshTimer = currentRefreshTimer - dt
-	
-	if currentRefreshTimer <= 0 then
-		currentRefreshTimer = refreshRate
-		
-		fires, fireCount = QueryFires()
-	end
-end
-
-function draw(dt)
-	menu_draw(dt)
-	
-	local isMenuOpenRightNow = isMenuOpen()
-	
-	if isMenuOpenRightNow then
-		return
-	end
-	
-	if (GetString("game.player.tool") ~= toolName or GetPlayerVehicle() ~= 0) and not alwaysActive then
-		return
-	end
-	
-	if fireCount <= 0 then
-		return
-	end
-	
-	drawFireIcons()
-end
-
--- UI Functions (excludes sound specific functions)
 
 function drawFireIcons()
 	UiPush()
@@ -86,7 +12,7 @@
 		for key, value in pairs(fires) do
 			UiPush()
 				local xPos, yPos, dist = UiWorldToPixel(value)
-				if dist > 0 then
+				if dist ~= 0 then
 					UiTranslate(xPos, yPos)
 					UiImageBox("MOD/sprites/fire.png", 50, 50, 0, 0)
 				end
@@ -95,19 +21,9 @@
 	UiPop()
 end
 
--- Creation Functions
-
--- Object handlers
-
--- Tool Functions
-
--- Particle Functions
-
--- Action functions
-
 function QueryFires()
 	local fires = {}
-	local playerPos = GetPlayerTransform().pos
+	local playerPos = GetPlayerTransform(playerId).pos
 	
 	ParticleReset()
 	ParticleColor(0, 0, 1)
@@ -137,8 +53,55 @@
 	return fires, fireCount
 end
 
--- Sprite Functions
+function server.init()
+    saveFileInit()
+    menu_init()
+    RegisterTool(toolName, toolReadableName, "MOD/vox/tool.vox")
+    SetBool("game.tool." .. toolName .. ".enabled", true, true)
+end
 
--- UI Sound Functions
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not menu_disabled then
+        	menu_tick(dt)
+        end
+        local isMenuOpenRightNow = isMenuOpen()
+        if isMenuOpenRightNow then
+        	return
+        end
+        if (GetString("game.player.tool") ~= toolName or GetPlayerVehicle(playerId) ~= 0) and not alwaysActive then
+        	return
+        end
+        if GetFireCount() <= 0 then
+        	fireCount = 0
+        	return
+        end
+        currentRefreshTimer = currentRefreshTimer - dt
+        if currentRefreshTimer <= 0 then
+        	currentRefreshTimer = refreshRate
 
--- Misc Functions+        	fires, fireCount = QueryFires()
+        end
+    end
+end
+
+function client.draw()
+    menu_draw(dt)
+
+    local isMenuOpenRightNow = isMenuOpen()
+
+    if isMenuOpenRightNow then
+    	return
+    end
+
+    if (GetString("game.player.tool") ~= toolName or GetPlayerVehicle(playerId) ~= 0) and not alwaysActive then
+    	return
+    end
+
+    if fireCount <= 0 then
+    	return
+    end
+
+    drawFireIcons()
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
@@ -1,120 +1,8 @@
-#include "scripts/ui.lua"
-#include "scripts/savedata.lua"
-#include "scripts/textbox.lua"
-#include "datascripts/keybinds.lua"
-#include "datascripts/inputList.lua"
-#include "datascripts/color4.lua"
-
+#version 2
 local modname = "Pixelated"
-
 local resettingBinds = 0
 local rebinding = nil
-
 local resolutionBox = nil
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
-		textboxClass_render(resolutionBox)
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
 
 function setupTextBoxes()
 	local textBox01, newBox01 = textboxClass_getTextBox(1)
@@ -156,4 +44,109 @@
 			rebinding = id
 		end
 	UiPop()
-end+end
+
+function server.init()
+    saveFileInit()
+    textboxClass_setTextBoxBg()
+    textboxClass_setDescBoxBg()
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        textboxClass_tick()
+        if resettingBinds ~= 0 then
+        	resettingBinds = resettingBinds - dt
+        end
+        if rebinding ~= nil then
+        	local lastKeyPressed = getKeyPressed()
+
+        	if lastKeyPressed ~= nil then
+        		binds[rebinding] = lastKeyPressed
+        		rebinding = nil
+        	end
+        end
+    end
+end
+
+function client.draw()
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
+    		-- DEFAULTS
+    		resetKeybinds()
+    	end
+
+    	UiTranslate(0, 60)
+
+    	if UiTextButton("Save and exit", 200, 50) then
+    		saveKeyBinds()
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
+
+    	setupTextBoxes()
+
+    	UiPush()
+    		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    		if resettingBinds ~= 0 then
+    			UiColor(1, 0, 0, 1)
+    			if UiTextButton("Are you sure?") then
+    				resetKeybinds()
+    				resettingBinds = 0
+    			end
+    		else
+    			if UiTextButton("Reset Keybinds") then
+    				resettingBinds = 5
+    			end
+    		end
+    	UiPop()
+
+    	UiTranslate(0, 50)
+
+    	UiPush()
+    		UiTranslate(0, 50)
+    		for i = 1, #bindOrder do
+    			local id = bindOrder[i]
+    			local key = binds[id]
+    			drawRebindable(id, key)
+    			UiTranslate(0, 50)
+    		end
+    	UiPop()
+
+    	UiTranslate(0, 50 * (#bindOrder + 1))
+
+    	textboxClass_render(resolutionBox)
+    UiPop()
+
+    textboxClass_drawDescriptions()
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
-local menuHeight = 0.25
-
-local refreshRateBox = nil
-local rangeBox = nil
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
-		UiTranslate(0, 30)
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
-		--UiTranslate(0, 50 * (#bindOrder + 1))
-		
-		textboxClass_render(refreshRateBox)
-		
-		UiTranslate(0, 50)
-		
-		textboxClass_render(rangeBox)
-		
-		UiPush()
-			UiTranslate(-165, 50)
-			
-			drawToggle("Always active:", alwaysActive, function(v) alwaysActive = v end)
-		UiPop()
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
-		textBox01.name = "Refresh Rate"
-		textBox01.value = refreshRate .. ""
-		textBox01.numbersOnly = true
-		textBox01.limitsActive = true
-		textBox01.numberMin = 0.01
-		textBox01.numberMax = 100
-		textBox01.description = "How fast the tool refreshes.\nMin: 0.01\nDefault: 1\nMax: 100"
-		textBox01.onInputFinished = function(v) refreshRate = tonumber(v) end
-		
-		refreshRateBox = textBox01
-	end
-	
-	if newBox02 then
-		textBox02.name = "Range"
-		textBox02.value = range .. ""
-		textBox02.numbersOnly = true
-		textBox02.limitsActive = true
-		textBox02.numberMin = 0.01
-		textBox02.numberMax = 500
-		textBox02.description = "Range of the tool.\nHigher numbers might cause frame drops.\nMin: 0.01\nDefault: 1\nMax: 500"
-		textBox02.onInputFinished = function(v) range = tonumber(v) end
-		
-		rangeBox = textBox02
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
@@ -305,4 +24,5 @@
 
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
-moddataPrefix = "savegame.mod.firelocator"
-
+#version 2
 function saveFileInit()
 	saveVersion = GetInt(moddataPrefix .. "Version")
 	
@@ -11,21 +8,22 @@
 	
 	if saveVersion < 1 or saveVersion == nil then
 		saveVersion = 1
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		refreshRate = 1
 		GetFloat(moddataPrefix .. "RefreshRate", refreshRate)
 		
 		alwaysActive = false
-		SetBool(moddataPrefix .. "AlwaysActive", alwaysActive)
+		SetBool(moddataPrefix .. "AlwaysActive", alwaysActive, true)
 		
 		range = 100
-		SetFloat(moddataPrefix .. "Range", range)
+		SetFloat(moddataPrefix .. "Range", range, true)
 	end
 end
 
 function saveDataValues()
-	SetFloat(moddataPrefix .. "RefreshRate", refreshRate)
-	SetFloat(moddataPrefix .. "Range", range)
-	SetBool(moddataPrefix .. "AlwaysActive", alwaysActive)
-end+	SetFloat(moddataPrefix .. "RefreshRate", refreshRate, true)
+	SetFloat(moddataPrefix .. "Range", range, true)
+	SetBool(moddataPrefix .. "AlwaysActive", alwaysActive, true)
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
