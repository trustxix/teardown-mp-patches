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
@@ -1,32 +1,5 @@
-#include "scripts/utils.lua"
-
-binds = {
-	Toggle_Scale = "c",
-	Jump = "jump",
-	Forwards = "up",
-	Backwards = "down",
-	Left = "left",
-	Right = "right",
-	LookX = "camerax",
-	LookY = "cameraY",
-	UseTool = "usetool",
-	Scroll = "mousewheel",
-}
-
+#version 2
 local bindBackup = deepcopy(binds)
-
-bindOrder = {
-	"Toggle_Scale",
-}
-		
-bindNames = {
-	Toggle_Scale = "Toggle Scale",
-	Jump = "Iump",
-	Forwards = "Forwards",
-	Backwards = "Backwards",
-	Left = "Left",
-	Right = "Right",
-}
 
 function resetKeybinds()
 	binds = deepcopy(bindBackup)
@@ -34,4 +7,5 @@
 
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
@@ -1,138 +1,4 @@
-#include "scripts/utils.lua"
-#include "scripts/savedata.lua"
-#include "scripts/menu.lua"
-#include "datascripts/keybinds.lua"
-#include "datascripts/inputList.lua"
-#include "toolscripts/tool_main.lua"
-
-toolName = "playerscaler"
-toolReadableName = "Player Scaler"
-
-local menu_disabled = false
-
-local currentLerpSize = 1 --Default size = 1
-local scalingActive = false
-local lerpActive = false
-local startTime = 1
-local currentTime = 1
-local targetTime = 1
-local lerpTime = 0
-
-local lerpSpeed = 2
-
-local cameraRotEulerStartLerp = nil
-local lerpStartValue = 1 -- Lerp value
-lerpEndValue = 0.12
-
-local normalPlayerHeight = 1.8 -- Actual height
-local normalPlayerSpeed = 7
-
-local playerGravity = 0.75
-local playerJumpStrength = 0.75
-
-local customPlayerTransform = nil
-local jumpLength = 0
-local maxJumpLength = 14
-
-local lastPlayerVehicle = 0
-
-local playerCameraRotEuler = nil
-
-local sensitivity = GetFloat("options.input.sensitivity")
-
-damageMultiplier = 1
-speedMultiplier = 1
-
-if SetPlayerHidden == nil then -- For people running stable.
-	SetPlayerHidden = function() end
-end
-
-function init()
-	saveFileInit()
-	menu_init()
-	tool_init()
-end
-
-function tick(dt)
-	if not menu_disabled then
-		menu_tick(dt)
-		
-		--[[if isMenuOpen() then
-			return
-		end]]--
-	end
-	
-	--[[ DEBUG
-	
-	local pct = GetPlayerCameraTransform()
-	local orig = pct.pos
-	local dir = TransformToParentVec(pct, Vec(0, 0, -1))
-	
-	local hit, hitPoint, dist = raycast(orig, dir)
-	
-	if hit then
-		DebugWatch("dist", dist)
-	end
-	
-	--]]-- END DEBUG
-	
-	local isMenuOpenRightNow = isMenuOpen()
-	
-	local currentPlayerVehicle = GetPlayerVehicle()
-	
-	if InputPressed(binds["Toggle_Scale"]) and currentPlayerVehicle == 0 and not isMenuOpenRightNow then
-		toggleScaling()
-	end
-	
-	if lerpActive then
-		handleLerp(dt)
-	end
-	
-	if currentPlayerVehicle ~= 0 then
-		lastPlayerVehicle = currentPlayerVehicle
-		return
-	elseif lastPlayerVehicle ~= 0 then
-		customPlayerTransform = GetPlayerTransform()
-		lastPlayerVehicle = 0
-	end
-	
-	if currentLerpSize ~= lerpStartValue then
-		if GetString("game.player.tool") ~= "sledge" then
-			SetString("game.player.tool", "sledge")
-		end
-		
-		--[[local cameraOffset = GetPlayerCameraTransform()
-	
-		cameraOffset.pos = Vec(0, normalPlayerHeight - currentLerpSize * normalPlayerHeight, 0)--VecAdd(cameraOffset.pos, VecSub(newCameraTransform.pos, cameraOffset.pos))
-		cameraOffset.rot = Quat()
-		
-		SetPlayerCameraOffsetTransform(cameraOffset)]]--
-		
-		SetPlayerHidden()
-		
-		if not isMenuOpenRightNow then
-			tool_tick(dt)
-			handlePlayerMovement(dt)
-		end
-		
-		handleCameraMovement()
-		
-		handlePlayerSpeed()
-	end
-end
-
-function draw(dt)
-	drawUI(dt)
-	
-	if currentLerpSize ~= lerpStartValue and lastPlayerVehicle == 0 then
-		tool_draw()
-	end
-	
-	menu_draw(dt)
-end
-
--- UI Functions (excludes sound specific functions)
-
+#version 2
 function drawUI(dt)
 	if not headbobWarned then
 		UiPush()
@@ -185,31 +51,21 @@
 			
 			if UiTextButton("Okay", 60, 40) then
 				headbobWarned = true
-				SetBool(moddataPrefix.. "HeadBobWarned", headbobWarned)
+				SetBool(moddataPrefix.. "HeadBobWarned", headbobWarned, true)
 			end
 		UiPop()
 	end
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
 function toggleScaling()
 	scalingActive = not scalingActive
 	
 	if scalingActive then
-		customPlayerTransform = GetPlayerTransform()
+		customPlayerTransform = GetPlayerTransform(playerId)
 		customPlayerTransform.pos[2] = customPlayerTransform.pos[2] + 0.075
-		SetPlayerTransform(customPlayerTransform)
-
-		playerCameraRotEuler = GetQuatEulerVec(GetPlayerCameraTransform().rot)
+		SetPlayerTransform(playerId, customPlayerTransform)
+
+		playerCameraRotEuler = GetQuatEulerVec(GetPlayerCameraTransform(playerId).rot)
 		startScaleToCustomSize()
 	else
 		startScaleToNormal()
@@ -245,7 +101,7 @@
 
 	currentLerpSize = Lerp(startTime, targetTime, currentLerpTime)
 	if cameraRotEulerStartLerp ~= nil then
-		playerCameraRotEuler = VecLerp(cameraRotEulerStartLerp, GetQuatEulerVec(GetPlayerCameraTransform().rot), currentLerpTime)
+		playerCameraRotEuler = VecLerp(cameraRotEulerStartLerp, GetQuatEulerVec(GetPlayerCameraTransform(playerId).rot), currentLerpTime)
 		
 		if currentLerpTime == 1 then
 			cameraRotEulerStartLerp = nil
@@ -295,7 +151,7 @@
 	local xMov, zMov, jumped =  getMovementInput()
 	
 	local cameraTransform = GetCameraTransform()
-	local playerCameraTransform = GetPlayerCameraTransform()
+	local playerCameraTransform = GetPlayerCameraTransform(playerId)
 	
 	if xMov ~= 0 or zMov ~= 0 then
 		local localForwardMovementVec = Vec(0, 0, zMov)
@@ -333,8 +189,8 @@
 		customPlayerTransform.pos = VecAdd(customPlayerTransform.pos, Vec(0, sizeDiff * dt * 10, 0))
 	end
 	
-	if (playerOnGround and jumped) or jumpLength > 0 then
-		if jumpLength > 0 then
+	if (playerOnGround and jumped) or jumpLength ~= 0 then
+		if jumpLength ~= 0 then
 			jumpLength = jumpLength - 1
 		elseif playerOnGround and jumped and jumpLength <= 0 then
 			jumpLength = maxJumpLength
@@ -345,7 +201,7 @@
 		customPlayerTransform.pos = VecAdd(customPlayerTransform.pos, Vec(0, -getPlayerGravity() * dt, 0))
 	end
 	
-	SetPlayerTransform(Transform(customPlayerTransform.pos, playerCameraTransform.rot), true)
+	SetPlayerTransform(playerId, Transform(customPlayerTransform.pos, playerCameraTransform.rot), true)
 end
 
 function getPlayerHeight()
@@ -416,12 +272,12 @@
 end
 
 function handlePlayerSpeed()
-	local velocity = GetPlayerVelocity()
+	local velocity = GetPlayerVelocity(playerId)
 	local speed = VecMag(velocity)
 	
 	if speed > currentLerpSize * normalPlayerSpeed then
 		local adjustedVelocity = VecScale(velocity, currentLerpSize)
-		SetPlayerVelocity(adjustedVelocity)
+		SetPlayerVelocity(playerId, adjustedVelocity)
 	end
 end
 
@@ -458,8 +314,13 @@
 	return QuatEuler(vec[1], vec[2], vec[3])
 end
 
--- Sprite Functions
-
--- UI Sound Functions
-
--- Misc Functions+function client.draw()
+    drawUI(dt)
+
+    if currentLerpSize ~= lerpStartValue and lastPlayerVehicle == 0 then
+    	tool_draw()
+    end
+
+    menu_draw(dt)
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
@@ -1,109 +1,7 @@
-#include "scripts/ui.lua"
-#include "scripts/savedata.lua"
-#include "scripts/textbox.lua"
-#include "datascripts/keybinds.lua"
-#include "datascripts/inputList.lua"
-#include "datascripts/color4.lua"
-
+#version 2
 local modname = "Player Scaler"
-
 local resettingBinds = 0
 local rebinding = nil
-
-function init()
-	saveFileInit()
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
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-		
-		UiPush()
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
-	UiPop()
-end
-
-function tick(dt)
-	--textboxClass.tick()
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
 
 function drawRebindable(id, key)
 	UiPush()
@@ -128,4 +26,97 @@
 			rebinding = id
 		end
 	UiPop()
-end+end
+
+function server.init()
+    saveFileInit()
+end
+
+function server.tick(dt)
+    if resettingBinds ~= 0 then
+    	resettingBinds = resettingBinds - dt
+    end
+    if rebinding ~= nil then
+    	local lastKeyPressed = getKeyPressed()
+
+    	if lastKeyPressed ~= nil then
+    		binds[rebinding] = lastKeyPressed
+    		rebinding = nil
+    	end
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
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    	UiPush()
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
@@ -1,20 +1,11 @@
-#include "datascripts/inputList.lua"
-#include "datascripts/keybinds.lua"
-#include "scripts/ui.lua"
-#include "scripts/utils.lua"
-#include "scripts/textbox.lua"
-
+#version 2
 local menuOpened = false
 local menuOpenLastFrame = false
-
 local rebinding = nil
-
 local erasingBinds = 0
 local erasingValues = 0
-
 local menuWidth = 0.20
 local menuHeight = 0.45
-
 local lerpEndValueBox = nil
 local damageMultiplierBox = nil
 local speedMultiplierBox = nil
@@ -46,7 +37,7 @@
 	
 	textboxClass_tick()
 	
-	if erasingBinds > 0 then
+	if erasingBinds ~= 0 then
 		erasingBinds = erasingBinds - dt
 	end
 end
@@ -81,7 +72,7 @@
 		
 		UiPush()
 			UiTranslate(0, -100)
-			if erasingValues > 0 then
+			if erasingValues ~= 0 then
 				UiPush()
 				c_UiColor(Color4.Red)
 				if UiTextButton("Are you sure?" , buttonWidth, 40) then
@@ -101,7 +92,7 @@
 			--UiAlign("right bottom")
 			--UiTranslate(230, 0)
 			UiTranslate(0, -50)
-			if erasingBinds > 0 then
+			if erasingBinds ~= 0 then
 				UiPush()
 				c_UiColor(Color4.Red)
 				if UiTextButton("Are you sure?" , buttonWidth, 40) then
@@ -321,4 +312,5 @@
 
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
-moddataPrefix = "savegame.mod.playerscaler"
-
+#version 2
 function saveFileInit()
 	saveVersion = GetInt(moddataPrefix .. "Version")
 	
@@ -16,55 +13,56 @@
 	
 	if saveVersion < 1 or saveVersion == nil then
 		saveVersion = 1
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 	end
 	
 	if saveVersion < 3 then --Skip v2 due to broken keybind data
 		saveVersion = 3
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		binds["Toggle_Scale"] = getFromBackup("Toggle_Scale")
-		SetString(moddataPrefix.. "ToggleScaleKey", binds["Toggle_Scale"])
+		SetString(moddataPrefix.. "ToggleScaleKey", binds["Toggle_Scale"], true)
 		
 		binds["Open_Menu"] = getFromBackup("Open_Menu")
-		SetString(moddataPrefix.. "OpenMenuKey", binds["Open_Menu"])
+		SetString(moddataPrefix.. "OpenMenuKey", binds["Open_Menu"], true)
 	end
 	
 	if saveVersion < 4 then
 		saveVersion = 4
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		headbobWarned = false
-		SetBool(moddataPrefix.. "HeadBobWarned", headbobWarned)
+		SetBool(moddataPrefix.. "HeadBobWarned", headbobWarned, true)
 	end
 	
 	if saveVersion < 5 then
 		saveVersion = 5
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		lerpEndValue = 0.12  -- Prevent floating point issues, set as string
-		SetString(moddataPrefix .. "LerpEndValue", lerpEndValue .. "")
+		SetString(moddataPrefix .. "LerpEndValue", lerpEndValue .. "", true)
 		
 		damageMultiplier = 1
-		SetFloat(moddataPrefix .. "DamageMultiplier", damageMultiplier)
+		SetFloat(moddataPrefix .. "DamageMultiplier", damageMultiplier, true)
 	end
 	
 	if saveVersion < 6 then
 		saveVersion = 6
-		SetInt(moddataPrefix .. "Version", saveVersion)
+		SetInt(moddataPrefix .. "Version", saveVersion, true)
 		
 		speedMultiplier = 1
-		SetFloat(moddataPrefix .. "SpeedMultiplier", speedMultiplier)
+		SetFloat(moddataPrefix .. "SpeedMultiplier", speedMultiplier, true)
 	end
 end
 
 function saveKeyBinds()
-	SetString(moddataPrefix.. "ToggleScaleKey", binds["Toggle_Scale"])
-	SetString(moddataPrefix.. "OpenMenuKey", binds["Open_Menu"])
+	SetString(moddataPrefix.. "ToggleScaleKey", binds["Toggle_Scale"], true)
+	SetString(moddataPrefix.. "OpenMenuKey", binds["Open_Menu"], true)
 end
 
 function saveFloatValues()
-	SetString(moddataPrefix .. "LerpEndValue", lerpEndValue .. "")
-	SetFloat(moddataPrefix .. "DamageMultiplier", damageMultiplier)
-	SetFloat(moddataPrefix .. "SpeedMultiplier", speedMultiplier)
-end+	SetString(moddataPrefix .. "LerpEndValue", lerpEndValue .. "", true)
+	SetFloat(moddataPrefix .. "DamageMultiplier", damageMultiplier, true)
+	SetFloat(moddataPrefix .. "SpeedMultiplier", speedMultiplier, true)
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
@@ -299,4 +286,5 @@
 		end
 	UiPop()
 	return fontSize, fontSize > minFontSize
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

---

# Migration Report: toolscripts\tool_main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/toolscripts\tool_main.lua
+++ patched/toolscripts\tool_main.lua
@@ -1,44 +1,34 @@
-#include "scripts/utils.lua"
-
+#version 2
 local tools = {"Sledge", "Laser", "Shotgun", "Gun"}
-
 local toolAutoFire = { Sledge = false, 
 					   Laser = true, 
 					   Shotgun = false,
 					   Gun = false}
-
 local toolMaxDist = { Sledge = 3, 
 					  Laser = 100, 
 					  Shotgun = 100,
 					  Gun = 80}
-
 local toolDrawHitReticle = { Sledge = true, 
 							 Laser = true, 
 							 Shotgun = false,
 							 Gun = false}
-
 local toolSprite = { Sledge = "MOD/sprites/sledge.png", 
 					 Laser = "MOD/sprites/sledge.png", 
 					 Shotgun = "MOD/sprites/shotgun.png", 
 					 Gun = "MOD/sprites/gun.png"}
-
 local toolSpriteSize = { Sledge = 800, 
 						 Laser = 200, 
 						 Shotgun = 800, 
 						 Gun = 800}
-
 local toolSpriteOffset = { Sledge = {-50, 300}, 
 						   Laser = {200, 200}, 
 						   Shotgun = {-50, 540}, 
 						   Gun = {-50, 540}}
-
 local toolStrength = { Sledge = {1, 0, 0}, 
 					   Laser = {2, 2, 2}, 
 					   Shotgun = {1.2, 1, 1}, 
 					   Gun = {0.7, 0.5, 0.5}}
-
 local heldToolIndex = 1
-
 local hasScrolledOnce = false
 
 function tool_init()
@@ -54,7 +44,7 @@
 	
 	if scrollValue ~= 0 then
 		hasScrolledOnce = true
-		if scrollValue > 0 then
+		if scrollValue ~= 0 then
 			heldToolIndex = heldToolIndex + 1
 			
 			if heldToolIndex > #tools then
@@ -202,4 +192,5 @@
 	end
 	ParticleRotation(0.1)
 	ParticleCollide(0, 1)
-end+end
+

```
