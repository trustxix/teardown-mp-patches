# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,30 +1,9 @@
---C4
---Setting default values, just in case
-if GetString("savegame.mod.increaseKey") == "" then
-	SetString("savegame.mod.increaseKey", "p")
-end
-if GetString("savegame.mod.decreaseKey") == "" then
-	SetString("savegame.mod.decreaseKey", "l")
-end
-if GetString("savegame.mod.timerKey") == "" then
-	SetString("savegame.mod.timerKey", "o")
-end
-if GetString("savegame.mod.detonateKey") == "" then
-	SetString("savegame.mod.detonateKey", "k")
-end
-
+#version 2
 local increaseKey = GetString("savegame.mod.increaseKey")
 local decreaseKey = GetString("savegame.mod.decreaseKey")
 local timerKey = GetString("savegame.mod.timerKey")
 local detonateKey = GetString("savegame.mod.detonateKey")
-
 local timerPresets = { 0, 0.1, 0.25, 0.5, 1, 2, 5 }
-
-Bombs = {}
-TimerTime = 0
-BombsToExplode = 0
-Sound = LoadSound("MOD/snd/c4plant.ogg")
-
 local CONTROLS = {
 	['increaseKey'] = {
 		[1] = increaseKey,
@@ -43,25 +22,24 @@
 		[2] = 'extra0'
 	}
 }
-
-local function getDeviceId()
-	return LastInputDevice() or 1 -- We assume deviceId 0 is keyboard
-end
-
-local function getKey(key)
-	return CONTROLS[key][getDeviceId()]
-end
-
-local function formatIcon(icon)
-	return '[[' .. icon .. ';iconsize=40,40]]'
-end
-
 local DEFAULT_EXTRA_KEYS = {
 	['extra0'] = {'gamepad_button_r3', 'gamepad_dpad_up'},
 	['extra1'] = {'gamepad_button_r3', 'gamepad_dpad_right'},
 	['extra2'] = {'gamepad_button_r3', 'gamepad_dpad_left'},
 	['extra3'] = {'gamepad_button_r3', 'gamepad_dpad_down'},
 }
+
+local function getDeviceId()
+	return LastInputDevice() or 1 -- We assume deviceId 0 is keyboard
+end
+
+local function getKey(key)
+	return CONTROLS[key][getDeviceId()]
+end
+
+local function formatIcon(icon)
+	return '[[' .. icon .. ';iconsize=40,40]]'
+end
 
 local function getKeyText(key)
 	if key == 'usetool' then
@@ -92,7 +70,6 @@
 	end
 end
 
-
 local function CalculateQuat(normal, dir)
 	local quat = QuatLookAt(Vec(), normal)
 	if VecLength(VecCross(normal, Vec(0, 1, 0))) == 0 then
@@ -101,31 +78,6 @@
 	return quat
 end
 
-function init()
-	--Register tool and enable it
-	RegisterTool("cfour", "C4", "MOD/vox/c4.vox")
-	SetBool("game.tool.cfour.enabled", true)
-	if GetBool("savegame.mod.usetool") then
-		RegisterTool("cfourdetonate", "Detonate C4", "")
-		SetBool("game.tool.cfourdetonate.enabled", true)
-	end
-
-	--Setting ammo if limited ammo is... Disabled? Oh god, i messed it up
-	if not GetBool("savegame.mod.limitedammo") then
-		SetFloat("game.tool.cfour.ammo", 36)
-	end
-
-	--Setting the default explosion size value
-	if GetFloat("savegame.mod.explosionSize") == 0 then
-		SetFloat("savegame.mod.explosionSize", 2)
-	end
-	--Setting the default delay between explosions
-	if GetInt("savegame.mod.explosionTimer") == 0 then
-		SetInt("savegame.mod.explosionTimer", 1)
-	end
-end
-
----@param bombId number | nil
 local function explodeBomb(bombId)
 	--if bombId was not provided, set it to 1
 	bombId = bombId or 1
@@ -145,126 +97,152 @@
 	return GetString("game.player.tool") == "cfourdetonate" and InputDown("usetool")
 end
 
-function tick(dt)
-	--////////////////Explosion//////////////
-	TimerTime = TimerTime + dt
-
-	--Making the actual explosion happen
-	if ((isDetonateKeyPressed() or isDetonateToolUsed()) and #Bombs > 0) then
-		local temp = BombsToExplode
-		BombsToExplode = #Bombs
-		if (temp == 0) then
-			TimerTime = 0
-			explodeBomb()
-			BombsToExplode = BombsToExplode - 1
-		end
-	end
-	if BombsToExplode > 0 then
-		if GetInt("savegame.mod.explosionTimer") == 1 then
-			while BombsToExplode > 0 do
-				explodeBomb()
-				BombsToExplode = BombsToExplode - 1
-			end
-		elseif TimerTime > timerPresets[GetInt("savegame.mod.explosionTimer")] then
-			TimerTime = 0
-			explodeBomb()
-			BombsToExplode = BombsToExplode - 1
-		end
-	end
-	--////////////////Planting//////////////
-	--Check if C4 is selected
-	if GetString("game.player.tool") == "cfour" then
-		SetToolHandPoseLocalTransform(Transform(Vec(0.1, 0, 0.0), QuatEuler(90, 180, 0)),
-			Transform(Vec(-0.1, 0, 0.0), QuatEuler(-90, 0, 0)))
-		SetToolTransform(Transform(Vec(0, -0.3, -0.5), QuatEuler(40, 0, 0)))
-
-		--Check if tool is firing
-		if GetBool("game.player.canusetool") and InputPressed("usetool") and checkAmmo() then
-			if not GetBool("savegame.mod.limitedammo") then
-				SetFloat("game.tool.cfour.ammo", GetFloat("game.tool.cfour.ammo") - 1)
-			end
-			local t = GetPlayerCameraTransform()
-			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
-			-- Camera is further away in third person
-			local maxDist = GetBool("game.thirdperson") and 8 or 4
-			-- Making sure raycast collides with everything but the player and tool
-			QueryInclude("physical dynamic static large small visible animator")
-			if not GetBool('savegame.mod.collide') then
-				for _, listOfObjects in ipairs(Bombs) do
-					for _, handle in ipairs(listOfObjects) do
-						QueryRejectShape(handle)
-					end
-				end
-			end
-			local hit, dist, normal = QueryRaycast(t.pos, fwd, maxDist)
-			if hit then
-				--Adding new bomb
-				local hitVec = VecAdd(t.pos, VecScale(fwd, dist))
-				local bombTransform = Transform(hitVec,
-					QuatRotateQuat(CalculateQuat(normal, fwd), QuatEuler(-90, 0, 180)))
-				local spawnedObjects = Spawn('MOD/c4.xml', bombTransform, true, true)
-				if not GetBool('savegame.mod.collide') then
-					for _, handle in ipairs(spawnedObjects) do
-						SetShapeCollisionFilter(handle, 2, 255 - 2)
-					end
-				end
-				Bombs[#Bombs + 1] = spawnedObjects
-
-				--Playing the sounds
-				PlaySound(Sound)
-			end
-		end
-
-		--Making explosion bigger
-		if InputDown(getKey('increaseKey')) then
-			SetFloat("savegame.mod.explosionSize", GetFloat("savegame.mod.explosionSize") + 0.5 * dt)
-			if (GetFloat("savegame.mod.explosionSize") > 4.0) then
-				SetFloat("savegame.mod.explosionSize", 4.0)
-			end
-		end
-
-		--Making explosion smaller
-		if InputDown(getKey('decreaseKey')) then
-			SetFloat("savegame.mod.explosionSize", GetFloat("savegame.mod.explosionSize") - 0.5 * dt)
-			if (GetFloat("savegame.mod.explosionSize") < 0.5) then
-				SetFloat("savegame.mod.explosionSize", 0.5)
-			end
-		end
-
-		--Changing the timer
-		if InputPressed(getKey('timerKey')) then
-			SetInt("savegame.mod.explosionTimer", GetInt("savegame.mod.explosionTimer") + 1)
-			if GetInt("savegame.mod.explosionTimer") > #timerPresets then
-				SetInt("savegame.mod.explosionTimer", 1)
-			end
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "cfour" and GetPlayerVehicle() == 0 then --I don't want it to draw this thing when player is in a car
-		UiPush()
-		UiTranslate(0, UiHeight() - 100)
-		UiAlign("left bottom")
-		UiFont("bold.ttf", 24)
-
-		--I separated it into multiple lines for convenience
-		local text = ""
-		text = text .. "Active charges of C4: " .. #Bombs .. "\n"
-		text = text ..
-			"Explosion size: " ..
-			math.floor(GetFloat("savegame.mod.explosionSize") * 100) /
-			100 -- This math is needed to only leave 2 numbers after the decimal point
-		text = text .. " (" .. math.floor((GetFloat("savegame.mod.explosionSize") - 0.5) / 3.5 * 100) .. "%)\n"
-		text = text .. "Time between explosions: " .. timerPresets[GetInt("savegame.mod.explosionTimer")] .. "s\n"
-		text = text .. "Press " .. getKeyText('usetool') .. " to plant a charge\n"
-		if not GetBool("savegame.mod.usetool") then
-			text = text .. "Press " .. getKeyText('detonateKey') .. " to detonate the charges\n"
-		end
-		text = text ..
-			"Hold " .. getKeyText('increaseKey') .. "/" .. getKeyText('decreaseKey') .. " to change the size of explosion\n"
-		text = text .. "Press " .. getKeyText('timerKey') .. " to change time between explosions"
-		UiText(text)
-		UiPop()
-	end
-end
+function server.init()
+    RegisterTool("cfour", "C4", "MOD/vox/c4.vox")
+    SetBool("game.tool.cfour.enabled", true, true)
+    if GetBool("savegame.mod.usetool") then
+    	RegisterTool("cfourdetonate", "Detonate C4", "")
+    	SetBool("game.tool.cfourdetonate.enabled", true, true)
+    end
+    --Setting ammo if limited ammo is... Disabled? Oh god, i messed it up
+    if not GetBool("savegame.mod.limitedammo") then
+    	SetFloat("game.tool.cfour.ammo", 36, true)
+    end
+    --Setting the default explosion size value
+    if GetFloat("savegame.mod.explosionSize") == 0 then
+    	SetFloat("savegame.mod.explosionSize", 2, true)
+    end
+    --Setting the default delay between explosions
+    if GetInt("savegame.mod.explosionTimer") == 0 then
+    	SetInt("savegame.mod.explosionTimer", 1, true)
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        TimerTime = TimerTime + dt
+        --Making the actual explosion happen
+        if ((isDetonateKeyPressed() or isDetonateToolUsed()) and #Bombs > 0) then
+        	local temp = BombsToExplode
+        	BombsToExplode = #Bombs
+        	if (temp == 0) then
+        		TimerTime = 0
+        		explodeBomb()
+        		BombsToExplode = BombsToExplode - 1
+        	end
+        end
+        if BombsToExplode ~= 0 then
+        	if GetInt("savegame.mod.explosionTimer") == 1 then
+        		while BombsToExplode > 0 do
+        			explodeBomb()
+        			BombsToExplode = BombsToExplode - 1
+        		end
+        	elseif TimerTime > timerPresets[GetInt("savegame.mod.explosionTimer")] then
+        		TimerTime = 0
+        		explodeBomb()
+        		BombsToExplode = BombsToExplode - 1
+        	end
+        end
+        --////////////////Planting//////////////
+        --Check if C4 is selected
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "cfour" then
+    	SetToolHandPoseLocalTransform(Transform(Vec(0.1, 0, 0.0), QuatEuler(90, 180, 0)),
+    		Transform(Vec(-0.1, 0, 0.0), QuatEuler(-90, 0, 0)))
+    	SetToolTransform(Transform(Vec(0, -0.3, -0.5), QuatEuler(40, 0, 0)))
+
+    	--Check if tool is firing
+    	if GetBool("game.player.canusetool") and InputPressed("usetool") and checkAmmo() then
+    		if not GetBool("savegame.mod.limitedammo") then
+    			SetFloat("game.tool.cfour.ammo", GetFloat("game.tool.cfour.ammo") - 1, true)
+    		end
+    		local t = GetPlayerCameraTransform(playerId)
+    		local fwd = TransformToParentVec(t, Vec(0, 0, -1))
+    		-- Camera is further away in third person
+    		local maxDist = GetBool("game.thirdperson") and 8 or 4
+    		-- Making sure raycast collides with everything but the player and tool
+    		QueryInclude("physical dynamic static large small visible animator")
+    		if not GetBool('savegame.mod.collide') then
+    			for _, listOfObjects in ipairs(Bombs) do
+    				for _, handle in ipairs(listOfObjects) do
+    					QueryRejectShape(handle)
+    				end
+    			end
+    		end
+    		local hit, dist, normal = QueryRaycast(t.pos, fwd, maxDist)
+    		if hit then
+    			--Adding new bomb
+    			local hitVec = VecAdd(t.pos, VecScale(fwd, dist))
+    			local bombTransform = Transform(hitVec,
+    				QuatRotateQuat(CalculateQuat(normal, fwd), QuatEuler(-90, 0, 180)))
+    			local spawnedObjects = Spawn('MOD/c4.xml', bombTransform, true, true)
+    			if not GetBool('savegame.mod.collide') then
+    				for _, handle in ipairs(spawnedObjects) do
+    					SetShapeCollisionFilter(handle, 2, 255 - 2)
+    				end
+    			end
+    			Bombs[#Bombs + 1] = spawnedObjects
+
+    			--Playing the sounds
+    			PlaySound(Sound)
+    		end
+    	end
+
+    	--Making explosion bigger
+    	if InputDown(getKey('increaseKey')) then
+    		SetFloat("savegame.mod.explosionSize", GetFloat("savegame.mod.explosionSize") + 0.5 * dt, true)
+    		if (GetFloat("savegame.mod.explosionSize") > 4.0) then
+    			SetFloat("savegame.mod.explosionSize", 4.0, true)
+    		end
+    	end
+
+    	--Making explosion smaller
+    	if InputDown(getKey('decreaseKey')) then
+    		SetFloat("savegame.mod.explosionSize", GetFloat("savegame.mod.explosionSize") - 0.5 * dt, true)
+    		if (GetFloat("savegame.mod.explosionSize") < 0.5) then
+    			SetFloat("savegame.mod.explosionSize", 0.5, true)
+    		end
+    	end
+
+    	--Changing the timer
+    	if InputPressed(getKey('timerKey')) then
+    		SetInt("savegame.mod.explosionTimer", GetInt("savegame.mod.explosionTimer") + 1, true)
+    		if GetInt("savegame.mod.explosionTimer") > #timerPresets then
+    			SetInt("savegame.mod.explosionTimer", 1, true)
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "cfour" and GetPlayerVehicle(playerId) == 0 then --I don't want it to draw this thing when player is in a car
+    	UiPush()
+    	UiTranslate(0, UiHeight() - 100)
+    	UiAlign("left bottom")
+    	UiFont("bold.ttf", 24)
+
+    	--I separated it into multiple lines for convenience
+    	local text = ""
+    	text = text .. "Active charges of C4: " .. #Bombs .. "\n"
+    	text = text ..
+    		"Explosion size: " ..
+    		math.floor(GetFloat("savegame.mod.explosionSize") * 100) /
+    		100 -- This math is needed to only leave 2 numbers after the decimal point
+    	text = text .. " (" .. math.floor((GetFloat("savegame.mod.explosionSize") - 0.5) / 3.5 * 100) .. "%)\n"
+    	text = text .. "Time between explosions: " .. timerPresets[GetInt("savegame.mod.explosionTimer")] .. "s\n"
+    	text = text .. "Press " .. getKeyText('usetool') .. " to plant a charge\n"
+    	if not GetBool("savegame.mod.usetool") then
+    		text = text .. "Press " .. getKeyText('detonateKey') .. " to detonate the charges\n"
+    	end
+    	text = text ..
+    		"Hold " .. getKeyText('increaseKey') .. "/" .. getKeyText('decreaseKey') .. " to change the size of explosion\n"
+    	text = text .. "Press " .. getKeyText('timerKey') .. " to change time between explosions"
+    	UiText(text)
+    	UiPop()
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
@@ -1,26 +1,10 @@
+#version 2
 local changeKey = nil
-
 local keyboard = { { "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12" },
 	{ "1",   "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0" },
 	{ "tab", "q",  "w",  "e",  "r",  "t",  "y",  "u",  "i",  "o",   "p" },
 	{ "a",   "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l" },
 	{ "z",   "x",  "c",  "v",  "b",  "n",  "m",  ",",  "." } }
-
---Setting default values, just in case
-if GetString("savegame.mod.increaseKey") == "" then
-	SetString("savegame.mod.increaseKey", "p")
-end
-if GetString("savegame.mod.decreaseKey") == "" then
-	SetString("savegame.mod.decreaseKey", "l")
-end
-if GetString("savegame.mod.timerKey") == "" then
-	SetString("savegame.mod.timerKey", "o")
-end
-if GetString("savegame.mod.detonateKey") == "" then
-	SetString("savegame.mod.detonateKey", "k")
-end
-
-
 local keys = {
 	["increaseKey"] = "Increase Explosion Size key",
 	["decreaseKey"] = "Decrease Explosion Size key",
@@ -28,16 +12,10 @@
 	["detonateKey"] = "Detonation key"
 }
 
-
----@param str string
----@return string, integer
 local function firstToUpper(str)
 	return str:gsub("%a", string.upper, 1)
 end
 
----@param title string
----@param position number
----@param size number | nil
 local function drawTitle(title, position, size)
 	size = size or 30
 	UiPush()
@@ -48,11 +26,6 @@
 	UiPop()
 end
 
----@param x number
----@param y number
----@param text string
----@param active boolean
----@param onClick function
 local function drawButton(x, y, text, active, onClick)
 	UiPush() --Keyboard Key
 	UiTranslate(x, y)
@@ -71,9 +44,6 @@
 	UiPop()
 end
 
----@param y number
----@param key string
----@param inactive boolean | nil
 local function drawRemappingLabel(y, key, inactive)
 	UiPush()
 	UiTranslate(UiCenter() + 45, y)
@@ -98,13 +68,6 @@
 	UiPop()
 end
 
----@param x number
----@param y number
----@param keyToChange string
----@param key string
----@param width number | nil
----@param height number | nil
----@param text string | nil
 local function drawKeyboardButton(x, y, keyToChange, key, width, height, text)
 	width = width or 50
 	height = height or 50
@@ -118,106 +81,107 @@
 		UiPop()
 	end
 	if UiTextButton(text, width, height) then
-		SetString("savegame.mod." .. keyToChange, key)
+		SetString("savegame.mod." .. keyToChange, key, true)
 	end
 	UiPop()
 end
 
-function draw()
-	if changeKey == nil then
-		drawTitle("C4 Options", 100, 48)
-		--Draw buttons
-		--Tool/Keyboard Key Switch
-		drawTitle('Detonate C4 using', 180)
-		drawButton(UiCenter() - 110, 230, "Keyboard key", not GetBool("savegame.mod.usetool"), function()
-			SetBool("savegame.mod.usetool", false)
-		end)
-		drawButton(UiCenter() + 110, 230, "'Detonate C4' tool", GetBool("savegame.mod.usetool"), function()
-			SetBool("savegame.mod.usetool", true)
-		end)
+function client.draw()
+    if changeKey == nil then
+    	drawTitle("C4 Options", 100, 48)
+    	--Draw buttons
+    	--Tool/Keyboard Key Switch
+    	drawTitle('Detonate C4 using', 180)
+    	drawButton(UiCenter() - 110, 230, "Keyboard key", not GetBool("savegame.mod.usetool"), function()
+    		SetBool("savegame.mod.usetool", false, true)
+    	end)
+    	drawButton(UiCenter() + 110, 230, "'Detonate C4' tool", GetBool("savegame.mod.usetool"), function()
+    		SetBool("savegame.mod.usetool", true, true)
+    	end)
 
-		--Tool/Keyboard Key Switch
-		drawTitle('Should C4 charges collide with each other', 300)
-		drawButton(UiCenter() - 110, 350, "Yes", GetBool("savegame.mod.collide"), function()
-			SetBool("savegame.mod.collide", true)
-		end)
-		drawButton(UiCenter() + 110, 350, "No", not GetBool("savegame.mod.collide"), function()
-			SetBool("savegame.mod.collide", false)
-		end)
+    	--Tool/Keyboard Key Switch
+    	drawTitle('Should C4 charges collide with each other', 300)
+    	drawButton(UiCenter() - 110, 350, "Yes", GetBool("savegame.mod.collide"), function()
+    		SetBool("savegame.mod.collide", true, true)
+    	end)
+    	drawButton(UiCenter() + 110, 350, "No", not GetBool("savegame.mod.collide"), function()
+    		SetBool("savegame.mod.collide", false, true)
+    	end)
 
-		--Limited/Unlimited ammo Switch
-		drawTitle("Ammo", 420)
-		drawButton(UiCenter() - 110, 470, "Limited", not GetBool("savegame.mod.limitedammo"), function()
-			SetBool("savegame.mod.limitedammo", false)
-		end)
-		drawButton(UiCenter() + 110, 470, "Unlimited", GetBool("savegame.mod.limitedammo"), function()
-			SetBool("savegame.mod.limitedammo", true)
-		end)
+    	--Limited/Unlimited ammo Switch
+    	drawTitle("Ammo", 420)
+    	drawButton(UiCenter() - 110, 470, "Limited", not GetBool("savegame.mod.limitedammo"), function()
+    		SetBool("savegame.mod.limitedammo", false, true)
+    	end)
+    	drawButton(UiCenter() + 110, 470, "Unlimited", GetBool("savegame.mod.limitedammo"), function()
+    		SetBool("savegame.mod.limitedammo", true, true)
+    	end)
 
-		--Key remapping
-		drawTitle("Key remapping", 550)
-		drawRemappingLabel(650, "increaseKey")
-		drawRemappingLabel(700, "decreaseKey")
-		drawRemappingLabel(750, "timerKey")
-		drawRemappingLabel(800, "detonateKey", GetBool("savegame.mod.usetool"))
+    	--Key remapping
+    	drawTitle("Key remapping", 550)
+    	drawRemappingLabel(650, "increaseKey")
+    	drawRemappingLabel(700, "decreaseKey")
+    	drawRemappingLabel(750, "timerKey")
+    	drawRemappingLabel(800, "detonateKey", GetBool("savegame.mod.usetool"))
 
-		--Close
-		drawButton(UiCenter(), 1000, "Close", false, function()
-			Menu()
-		end)
-		--------------------------KEYBOARD CUSTOMIZATION STARTS HERE
-	else
-		UiAlign("center middle")
-		UiFont("regular.ttf", 26)
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-		UiPush()
-		--F1-F12 key row
-		UiTranslate(UiCenter() - 200, 350)
-		for i = 1, #keyboard[1] do
-			drawKeyboardButton(-330 + (i - 1) * 55, 0, changeKey, keyboard[1][i])
-		end
-		--Number key row
-		UiTranslate(0, 55)
-		for i = 1, #keyboard[2] do
-			drawKeyboardButton(-350 + (i - 1) * 55, 0, changeKey, keyboard[2][i])
-		end
-		drawKeyboardButton(240, 0, changeKey, 'backspace', 125)
-		--First key row
-		UiTranslate(0, 55)
-		for i = 1, #keyboard[3] do
-			drawKeyboardButton(-380 + (i - 1) * 55, 0, changeKey, keyboard[3][i])
-		end
-		--Second key row
-		UiTranslate(0, 55)
-		for i = 1, #keyboard[4] do
-			drawKeyboardButton(-290 + (i - 1) * 55, 0, changeKey, keyboard[4][i])
-		end
-		drawKeyboardButton(240, 0, changeKey, "return", 125)
-		--Third key row
-		UiTranslate(0, 55)
-		for i = 1, #keyboard[5] do
-			drawKeyboardButton(-260 + (i - 1) * 55, 0, changeKey, keyboard[5][i])
-		end
-		UiPop()
-		--Some other keys
-		UiPush()
-		UiFont("regular.ttf", 18)
-		UiTranslate(UiCenter() + 200, 405)
-		--First row
-		drawKeyboardButton(0, 0, changeKey, "insert", 60, 60)
-		drawKeyboardButton(65, 0, changeKey, "home", 60, 60)
-		drawKeyboardButton(130, 0, changeKey, "pgup", 60, 60, "Page\nup")
-		--Second row
-		UiTranslate(0, 65)
-		drawKeyboardButton(0, 0, changeKey, "delete", 60, 60)
-		drawKeyboardButton(65, 0, changeKey, "end", 60, 60)
-		drawKeyboardButton(130, 0, changeKey, "pgdown", 60, 60, "Page\ndown")
-		UiPop()
-		--Text above and actually the entire logic of this thing
-		drawTitle("Remapping: " .. keys[changeKey], 100, 48)
-		--Cancel
-		drawButton(UiCenter(), 1000, "Cancel", false, function()
-			changeKey = nil
-		end)
-	end
+    	--Close
+    	drawButton(UiCenter(), 1000, "Close", false, function()
+    		Menu()
+    	end)
+    	--------------------------KEYBOARD CUSTOMIZATION STARTS HERE
+    else
+    	UiAlign("center middle")
+    	UiFont("regular.ttf", 26)
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    	UiPush()
+    	--F1-F12 key row
+    	UiTranslate(UiCenter() - 200, 350)
+    	for i = 1, #keyboard[1] do
+    		drawKeyboardButton(-330 + (i - 1) * 55, 0, changeKey, keyboard[1][i])
+    	end
+    	--Number key row
+    	UiTranslate(0, 55)
+    	for i = 1, #keyboard[2] do
+    		drawKeyboardButton(-350 + (i - 1) * 55, 0, changeKey, keyboard[2][i])
+    	end
+    	drawKeyboardButton(240, 0, changeKey, 'backspace', 125)
+    	--First key row
+    	UiTranslate(0, 55)
+    	for i = 1, #keyboard[3] do
+    		drawKeyboardButton(-380 + (i - 1) * 55, 0, changeKey, keyboard[3][i])
+    	end
+    	--Second key row
+    	UiTranslate(0, 55)
+    	for i = 1, #keyboard[4] do
+    		drawKeyboardButton(-290 + (i - 1) * 55, 0, changeKey, keyboard[4][i])
+    	end
+    	drawKeyboardButton(240, 0, changeKey, "return", 125)
+    	--Third key row
+    	UiTranslate(0, 55)
+    	for i = 1, #keyboard[5] do
+    		drawKeyboardButton(-260 + (i - 1) * 55, 0, changeKey, keyboard[5][i])
+    	end
+    	UiPop()
+    	--Some other keys
+    	UiPush()
+    	UiFont("regular.ttf", 18)
+    	UiTranslate(UiCenter() + 200, 405)
+    	--First row
+    	drawKeyboardButton(0, 0, changeKey, "insert", 60, 60)
+    	drawKeyboardButton(65, 0, changeKey, "home", 60, 60)
+    	drawKeyboardButton(130, 0, changeKey, "pgup", 60, 60, "Page\nup")
+    	--Second row
+    	UiTranslate(0, 65)
+    	drawKeyboardButton(0, 0, changeKey, "delete", 60, 60)
+    	drawKeyboardButton(65, 0, changeKey, "end", 60, 60)
+    	drawKeyboardButton(130, 0, changeKey, "pgdown", 60, 60, "Page\ndown")
+    	UiPop()
+    	--Text above and actually the entire logic of this thing
+    	drawTitle("Remapping: " .. keys[changeKey], 100, 48)
+    	--Cancel
+    	drawButton(UiCenter(), 1000, "Cancel", false, function()
+    		changeKey = nil
+    	end)
+    end
 end
+

```
