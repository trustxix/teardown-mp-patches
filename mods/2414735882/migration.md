# Migration Report: changeLog.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/changeLog.lua
+++ patched/changeLog.lua
@@ -1,22 +1 @@
-
---[[05-18-2023 (mm-dd-yyyy) version 0.9.4]]--
-
-reload = false
-
-changeLog = {}
--- changeLog[#changeLog+1] = {"Gameplay"}
-changeLog[#changeLog+1] = {"User Interface"}
-changeLog[#changeLog+1] = {"sub", "Removed vehicle packs listing in options menu"}
-changeLog[#changeLog+1] = {"sub", "Minor UI changes"}
--- changeLog[#changeLog+1] = {"Performance"}
--- changeLog[#changeLog+1] = {"Spawning Toolkit"}
--- changeLog[#changeLog+1] = {"sub", "Version 2.3 update (more info -> workshop page)"}
-changeLog[#changeLog+1] = {"Other"}
-changeLog[#changeLog+1] = {"sub", "Internal improvements"}
-changeLog[#changeLog+1] = {"sub", "Fixed broken hood debug outline"}
-
--- toolkit minor internal changes & fixed incorrect xml handling
-
-updateDate = "May 18 2023"
-updateVersion = "0.9.4"
-toolkitVersion = "2.2"+#version 2

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
@@ -1,713 +1,4 @@
+#version 2
+local newBody = GetPlayerPickBody(playerId)
+local newShape = GetPlayerPickShape(playerId)
 
---[[05-18-2023 (mm-dd-yyyy) version 0.9.4]]--
-
-#include "library.zip"
-#include "changeLog.lua"
-#include "setup.zip"
-#include "pauseMenu.lua"
-#include "spawnPanel.lua"
-
-function init()
-	SetBool("NoLocalBranch", true)
-
-	updateInfo = SetupYLVF()
-	initNormal(colorSlotNum)
-	SetString("YLVF.toolkit.version", toolkitVersion)
-	
-	localJointTable = {}
-	empty = {}
-	vehicleOperationList = {}
-	lightSigal = true
-
-	showDyna = false
-	canUseDyna = false
-	pauseFade = 0
-
-	ChangeRegistry()
-	ReloadKeys()
-
-	hookConnect = false
-	storage = false
-
-	hookMatch = NewHookInit()
-	cabinLockInit = FindShapes("Ycabin", true)
-	lightShapesInit = FindShapes("Ylight", true)
-	honksInit = FindShapes("Yhorn", true)
-	craneInit = FindVehicles("Ycrane", true)
-	nozzleInit = FindBodies("Yfire", true)
-	
-	newDoorsInit = FindBodies("Ydoor", true)
-	newHoodsInit = FindBodies("Yhood", true)
-	newCabinBody = FindBodies("Ycabin", true)
-	newPasdoor = FindBodies("YMtE", true)
-	newCabinMatch, unmatchedCabinList = NewCabinSetup(cabinLockInit, newCabinBody)
-	newDynamicInit = FindBodies("Ydyna", true)
-
-	YLVFVehicles = FindVehicles("YLVF", true)
-	
-	sirenList = {}
-	sirenList[#sirenList+1] = LoadLoop("sound/siren01.ogg")
-	sirenList[#sirenList+1] = LoadLoop("sound/siren02.ogg")
-	sirenList[#sirenList+1] = LoadLoop("sound/siren03.ogg")
-	sirenList[#sirenList+1] = LoadLoop("sound/siren04.ogg")
-	sirenList[#sirenList+1] = LoadLoop("sound/siren05.ogg")
-	sirenList[#sirenList+1] = LoadLoop("sound/siren06.ogg")
-
-	honkList = {}
-	honkList[#honkList+1] = LoadLoop("sound/honk01.ogg")
-	honkList[#honkList+1] = LoadLoop("sound/honk02.ogg")
-	honkList[#honkList+1] = LoadLoop("sound/honk03.ogg")
-	honkList[#honkList+1] = LoadLoop("sound/honk04.ogg")
-	honkList[#honkList+1] = LoadLoop("sound/honk05.ogg")
-	honkList[#honkList+1] = LoadLoop("sound/honk06.ogg")
-	
-	blinkerSound = {}
-	blinkerSound[1] = LoadSound("clickup.ogg", 1)
-	blinkerSound[2] = LoadSound("clickdown.ogg", 1)
-
-	showUpdate = GetBool(pathUi.."showUpdate")
-
-	for v=1, #YLVFVehicles do
-		if GetTagValue(YLVFVehicles[v], "nodrive") == "mod" then
-			RemoveTag(YLVFVehicles[v], "nodrive")
-			local t = 1
-			repeat
-				if GetJointType(YLVFVehicles[v]+t) == "" and GetLightShape(YLVFVehicles[v]+t) == 0 and GetBodyShapes(YLVFVehicles[v]+t) ~= empty then
-					if GetShapeBody(YLVFVehicles[v]+t) == 0 then
-						check = GetBodyVehicle(YLVFVehicles[v]+t) ~= YLVFVehicles[v] and GetBodyVehicle(YLVFVehicles[v]+t) ~= 0
-						SetDescription(YLVFVehicles[v]+t, "")
-					else
-						if GetBodyVehicle(GetShapeBody(YLVFVehicles[v]+t)) == YLVFVehicles[v] then
-							SetDescription(YLVFVehicles[v]+t, "")
-						end
-					end
-				end
-				t = t + 1
-			until (check or t>5000)
-		end
-	end
-
-	if GetBool(pathVehicle.."autoFM") then
-		if GetBool(pathVehicle.."advFM") then
-			if GetEnvironmentProperty("nightlight") then
-				SetInt(pathVehicle.."FMinit", 2)
-			else
-				SetInt(pathVehicle.."FMinit", 1)
-			end
-		else
-			SetInt(pathVehicle.."FMinit", 2)
-		end
-	end
-
-	lightStatus = {}
-	pauseInit()
-end
-
-
-function tick(df)
-	
-	interAssist = GetBool(pathUi.."interAssist")
-	SetString("YLVF.pack.key", GetString(pathKey.."spawn"))
-	CheckColorEdit()
-
-	local allVehicle = FindVehicles("YLVF", true)
-	local unready = {}
-	local allReady = true
-	local enableControl = not GetBool("YLVF.pack.menu") and not GetBool("YLVF.pack.sub")
-
-	for i=1, #allVehicle do
-		if not HasTag(allVehicle[i], "Yready") then
-			allReady = false
-			table.insert(unready, allVehicle[i])
-		end
-	end
-
-	if not allReady then
-		for i=1, #unready do
-			SetTag(unready[i], "Yready")
-		end
-
-		hookMatch = NewHookInit()
-		cabinLockInit = FindShapes("Ycabin", true)
-		lightShapesInit = FindShapes("Ylight", true)
-		honksInit = FindShapes("Yhorn", true)
-		craneInit = FindVehicles("Ycrane", true)
-		nozzleInit = FindBodies("Yfire", true)
-		
-		newDoorsInit = FindBodies("Ydoor", true)
-		newHoodsInit = FindBodies("Yhood", true)
-		newCabinBody = FindBodies("Ycabin", true)
-		newPasdoor = FindBodies("YMtE", true)
-		newCabinMatch, unmatchedCabinList = NewCabinSetup(cabinLockInit, newCabinBody)
-		newDynamicInit = FindBodies("Ydyna", true)
-	end
-
-	if GetBool(pathVehicle.."autoFM") then
-		if GetBool(pathVehicle.."advFM") then
-			if GetEnvironmentProperty("nightlight") then
-				if GetInt(pathVehicle.."FMinit") ~= 2 then
-					lightStatus = ReloadLights(lightStatus, allVehicle, 1, 2)
-					SetInt(pathVehicle.."FMinit", 2)
-				end
-			else
-				if GetInt(pathVehicle.."FMinit") ~= 1 then
-					lightStatus = ReloadLights(lightStatus, allVehicle, 2, 1)
-					SetInt(pathVehicle.."FMinit", 1)
-				end
-			end
-		else
-			if GetInt(pathVehicle.."FMinit") ~= 2 then
-				SetInt(pathVehicle.."FMinit", 2)
-			end
-		end
-	else
-		if GetInt(pathVehicle.."FMinit") ~= 0 then
-			SetInt(pathVehicle.."FMinit", 0)
-		end
-	end
-	
-	NewDoor("open", "close", newDoorsInit)
-	NewHood("open", "close", newHoodsInit)
-	NewCabinTick("lift cabin", "close cabin", newCabinMatch)
-	NewPassengerDoor("open", "close", newPasdoor, pasdoorOperation, enableControl)
-	canUseDyna = NewDynamic(newDynamicInit, dynamicKeys, enableControl)
-
-	lightStatus = lightControl(lightKeys, lightStatus, enableControl)
-	lightOperate(lightShapesInit, blinkerSound, lightStatus)
-	if enableControl then
-		hookMatch = NewHookControl(craneControlKeys, hookMatch)
-		craneDrive(craneInit)
-		honkNsiren(honksInit, sirenList, honkList, honksCtrl)
-		fireEngineNozzle(nozzleInit, fireOperation)
-	end
-
-	if not GetBool("YLVF.pack.menu") and not GetBool("YLVF.pack.sub") then
-		if HasTag(GetPlayerVehicle(), "Yndrive") and HasTag(GetPlayerVehicle(), "YLVF") then
-			SetTag(GetPlayerVehicle(), "nodrive")
-		end
-	end
-		
-	if HasTag(GetPlayerVehicle(), "nodrive") and HasTag(GetPlayerVehicle(), "YLVF") then
-		SetPlayerVehicle(0)
-	end
-
-	if PauseMenuButton("YLVF Settings") then
-		pauseMenuEnable = true
-	end
-
-	if pauseMenuEnable then
-		SetValue("pauseFade", 1, "linear", 0.1)
-	elseif not pauseMenuEnable then
-		SetValue("pauseFade", 0, "linear", 0.1)
-	end
-
-	info = {}
-	uilight = false
-	uilightex = false
-	uiblinker = false
-	uiadmain = false
-	uiadmainex = false
-	uibeacon = false
-
-	if lightShape then
-		lightShapes = lightShapesInit
-		for i=1, #lightShapes do
-			if thisVehDetect(lightShapes[i]) then
-				if GetTagValue(lightShapes[i], "Ylight") == "FM" then
-					uilight = true
-					lights = GetShapeLights(lightShapes[i])
-					if lights ~= empty then
-						uilightex = true
-					end
-				end
-				if GetTagValue(lightShapes[i], "Ylight") == "BR" or GetTagValue(lightShapes[i], "Ylight") == "BL" then
-					uiblinker = true
-				end
-				if GetTagValue(lightShapes[i], "Ylight") == "ADM" then
-					uiadmain = true
-					lights = GetShapeLights(lightShapes[i])
-					if lights ~= empty then
-						uiadmainex = true
-					end
-				end
-				if GetTagValue(lightShapes[i], "Ylight") == "BCN" then
-					uibeacon = true
-				end
-			end
-		end
-	end
-	if uilight then
-		info[#info+1] = {lightKeys[1], "Light Mode"}
-		if uilightex then
-			info[#info+1] = {lightKeys[2], "Main Beam Headlights"}
-			info[#info+1] = {lightKeys[3], "Light Signal"}
-		end
-	end
-	if uiblinker then
-		info[#info+1] = {lightKeys[7].." & "..lightKeys[8], "Left & Right Blinker"}
-		info[#info+1] = {lightKeys[6], "Warning Lights"}
-	end
-	if uiadmain then
-		info[#info+1] = {lightKeys[5], "Additional Lights"}
-		info[#info+1] = {lightKeys[2], "Change Illumination"}
-	end
-	if uibeacon then
-		info[#info+1] = {lightKeys[4], "Beacon"}
-	end
-
-	local hornSet = false
-	local sirenSet = false
-
-	if honksInit ~= empty then
-		for i=1, #honksInit do
-			if thisVehDetect(honksInit[i]) then
-				if not hornSet then
-					info[#info+1] = {honksCtrl[2], "Horn"}
-					hornSet = true
-				end
-				if string.len(GetTagValue(honksInit[i], "Yhorn")) == 4 and not sirenSet then
-					info[#info+1] = {honksCtrl[1], "Siren"}
-					sirenSet = true
-				end
-			end
-		end
-	end
-
-	local vehiBodies = GetJointedBodies(GetVehicleBody(GetPlayerVehicle()))
-	local pasdoorSet = false
-	local pasdoorNoName = false
-	local pasdoorList = {}
-	local fireNozzle = false
-	local fireNozzleList = {}
-
-	for i=1, #vehiBodies do
-		local vehiBody = vehiBodies[i]
-		if HasTag(vehiBody, "YMtE") and GetBodyVehicle(vehiBody) == GetPlayerVehicle() then
-			pasdoorSet = true
-			local MtEgroup = tonumber(GetTagValue(vehiBody, "YMtE"))
-			if not pasdoorList[MtEgroup] then
-				pasdoorList[MtEgroup] = {group = MtEgroup, name = nil}
-			end
-			local MtEname = pasdoorList[MtEgroup].name or ((HasTag(vehiBody, "Yname") and GetTagValue(vehiBody, "Yname")) or "Unnamed Group")
-			pasdoorList[MtEgroup] = {group = MtEgroup, name = MtEname}
-		end
-
-		if HasTag(vehiBody, "Yfire") and GetBodyVehicle(vehiBody) == GetPlayerVehicle() then
-			fireNozzle = true
-			local nozzleShapes = GetBodyShapes(vehiBody)
-			for k=1, #nozzleShapes do
-				local nzShape = nozzleShapes[k]
-				if HasTag(nzShape, "Yfire") then
-					local fireGroup = tonumber(GetTagValue(nzShape, "Yfire"))
-					if not fireNozzleList[fireGroup] then
-						fireNozzleList[fireGroup] = {group = fireGroup, name = nil}
-					end
-					local fireName = fireNozzleList[fireGroup].name or ((HasTag(nzShape, "Yname") and GetTagValue(nzShape, "Yname")) or "Unnamed Group")
-					fireNozzleList[fireGroup] = {group = fireGroup, name = fireName}
-				end
-			end
-		end
-	end
-
-	if pasdoorSet or fireNozzle then
-
-		info[#info+1] = {"", ""}
-
-		if pasdoorSet then
-			info[#info+1] = {extraControlKeys[1], "All MtE Parts"}
-			for i=1, 10 do
-				local list = pasdoorList[i]
-				if list then
-					info[#info+1] = {string.sub(list.group, -1), string.gsub(list.name, "_", " ")}
-				end
-			end
-		end
-		
-		if fireNozzle then
-			info[#info+1] = {"Num + "..extraControlKeys[2], "Nozzles"}
-			for i=1, 10 do
-				local list = fireNozzleList[i]
-				if list then
-					info[#info+1] = {string.format("%s + %s", string.sub(list.group, -1), extraControlKeys[2]), string.gsub(list.name, "_", " ")}
-				end
-			end
-		end
-	end
-	
-	for i=1, #hookMatch do
-		local currGroup = hookMatch[i]
-		if thisVehDetect(currGroup.hook) then
-			if #info > 0 then
-				info[#info+1] = {"", ""}
-			end
-			info[#info+1] = {craneControlKeys[1], "Hook"}
-			if currGroup.arm then
-				info[#info+1] = {craneControlKeys[2].." & "..craneControlKeys[3], "Rope (Extend & Shorten)"}
-			end
-		end
-	end
-
-	if #info < 1 then
-		info[#info+1] = {"NOTICE", "No Operable Elements Found"}
-	end
-
-	info[#info+1] = {"", ""}
-	info[#info+1] = {string.upper(uiKeys[1]), "Collapse"}
-		
-	dynamicGroup = {}
-	dynamicGroup[1] = {false, "Group 1"}
-	dynamicGroup[2] = {false, "Group 2"}
-	dynamicGroup[3] = {false, "Group 3"}
-	dynamicGroup[4] = {false, "Group 4"}
-	dynamicGroup[5] = {false, "Group 5"}
-
-	dynaCount = 0
-	groupNameW = 0
-	groupOperationW = 0
-	
-	for i=1, #newDynamicInit do
-
-		local dynaBody = newDynamicInit[i]
-		local shapes = GetBodyShapes(dynaBody)
-		local indexBody = tonumber(GetTagValue(dynaBody, "Ydyna")) or 1
-		local nameTag = tostring(GetTagValue(dynaBody, "Yname"))
-
-		for s=1, #shapes do    
-			local joints = GetShapeJoints(shapes[s])
-			if thisVehDetect(shapes[s]) then
-				for j=1, #joints do
-					if HasTag(joints[j], "Ydyna") then
-						local indexJoint = tonumber(GetTagValue(joints[j], "Ydyna")) or indexBody
-						dynamicGroup[indexJoint][1] = true
-					end
-				end
-			end
-		end
-
-		if HasTag(dynaBody, "Yname") and nameTag then
-
-			local spacePos = string.find(nameTag, "_")
-			local newString = ""
-
-			while (spacePos ~= nil) do
-				if newString ~= "" then
-					newString = newString.." "..string.sub(nameTag, 1, spacePos-1)
-				else
-					newString = string.sub(nameTag, 1, spacePos-1)
-				end
-				nameTag = string.sub(nameTag, spacePos+1, string.len(nameTag))
-				spacePos = string.find(nameTag, "_")
-			end
-
-			if newString ~= "" then
-				newString = newString.." "..nameTag
-			else
-				newString = nameTag
-			end
-
-			if thisVehDetectBody(dynaBody) then
-				dynamicGroup[indexBody][2] = newString
-			end
-		end
-	end
-
-	for i=1, #dynamicGroup do
-		if dynamicGroup[i][1] then
-			dynaCount = dynaCount + 1
-			
-			UiFont("bold.ttf", 22)
-			groupNameW = math.max(groupNameW, UiGetTextSize(dynamicGroup[i][2]))
-			
-			UiFont("regular.ttf", 22)
-			groupOperationW = math.max(groupOperationW, UiGetTextSize(dynamicKeys[2*i-1].." & "..dynamicKeys[2*i]))
-		end
-	end
-end
-
-
-function update()
-	hookMatch = NewHookContrain(hookMatch)
-end
-
-
-function draw(dt)
-	if pauseMenuEnable or pauseFade > 0.1 then
-		SetTimeScale(math.max(0.1, 1-pauseFade))
-
-		UiPush()
-			UiBlur(pauseFade)
-			UiColorFilter(1, 1, 1, pauseFade)
-			UiColor(0, 0, 0, 0.8)
-			UiRect(UiWidth(), UiHeight())
-			if pauseMenuEnable then
-				UiMakeInteractive()
-			end
-			tempPause = not pauseDraw()
-			if pauseMenuEnable then pauseMenuEnable = tempPause end
-			if not tempPause then ReloadKeys() end
-		UiPop()
-	else
-		if updateInfo and showUpdate then
-			UiMakeInteractive()
-			SetTimeScale(0.1)
-	
-			local wid = 320
-			local hig = 180
-	
-			UiPush()
-				for i=1, #changeLog do
-					if changeLog[i][1] ~= "sub" then
-						UiFont("regular.ttf", 32)
-						UiWordWrap(440)
-						local width, height = UiGetTextSize(changeLog[i][1])
-						wid = math.max(wid, width)
-						hig = hig + height + 5
-					else
-						UiFont("regular.ttf", 26)
-						UiWordWrap(400)
-						local width, height = UiGetTextSize(changeLog[i][2])
-						wid = math.max(wid, width)
-						hig = hig + height + 8
-					end
-				end
-			UiPop()
-	
-			wid = wid + 160
-			hig = hig + 60
-	
-			UiPush()
-				UiAlign("center middle")
-				UiTranslate(UiCenter(), UiMiddle())
-				UiColor(0, 0, 0, 0.8)
-				UiImageBox("ui/common/box-solid-6.png", wid, hig, 6, 6)
-				UiPush()
-					UiTranslate(0, -hig/2+50)
-					UiColor(1, 1, 1)
-					UiFont("bold.ttf", 50)
-					UiText("New in YLVF "..updateVersion)
-					UiTranslate(0, 60)
-					UiPush()
-						UiAlign("left")
-						UiTranslate(-wid/2+60, 0)
-						for i=1, #changeLog do
-							if changeLog[i][1] ~= "sub" then
-								UiFont(FontList(10), 32)
-								UiWordWrap(440)
-								UiTranslate(0, 16)
-								local width, height = UiGetTextSize(changeLog[i][1])
-								UiText(changeLog[i][1])
-								UiTranslate(0, height+8)
-							else
-								UiFont("regular.ttf", 26)
-								UiWordWrap(400)
-								local width, height = UiGetTextSize(changeLog[i][2])
-								UiTranslate(10, 0)
-								UiText("--")
-								UiTranslate(25, 0)
-								UiText(changeLog[i][2])
-								UiTranslate(-35, height+5)
-							end
-						end
-					UiPop()
-				UiPop()
-				UiAlign("center middle")
-				UiTranslate(0, hig/2-55)
-				local press, condition = DrawColoredTextButtons(not updateInfo, "Got it!", 220, 50, 2, 36, 1, 1, 1)
-				updateInfo = not condition
-			UiPop()
-		else
-			if InputPressed(GetString(pathKey.."spawn")) then
-				if GetPlayerVehicle() == 0 then
-					SetBool("YLVF.pack.menu", not GetBool("YLVF.pack.menu"))
-				else
-					SetString("hud.notification", "YLVF Customizable Spawning Not Available While Driving")
-				end
-			end
-			
-			if GetBool("YLVF.pack.menu") and not spawnPanelDone then
-				spawnPanelWidth = GetSpawnPanelWidth()
-				spawnPanelDone = true
-			end
-
-			SpawnPanelMain(spawnPanelWidth)
-
-			if not GetBool("YLVF.pack.menu") and not GetBool("YLVF.pack.sub") then
-				if help then
-					--[[  TODO  ]]
-				end
-				
-				local newBody = GetPlayerPickBody()
-				if newBody ~= 0 then
-					if HasTag(newBody, "Yinter") and not HasTag(newBody, "Ynomanual") then
-						if interAssist then
-							DrawBodyOutline(newBody, 1, 1, 1, 0.4)
-						end
-						UiPush()
-							UiFont("bold.ttf", 22)
-							local str = string.upper(GetString("game.input.grab")).." to "..GetTagValue(newBody, "Yinter")
-							local w = 16 + UiGetTextSize(str)
-							UiAlign("center middle")
-							UiTranslate(UiCenter(), UiMiddle()+400)
-							UiColor(0.8, 1, 1, 0.6)
-							UiImageBox("ui/common/box-solid-6.png", w, 34, 6, 6)
-							UiColor(0, 0, 0)
-							UiText(str)
-						UiPop()
-					end
-				end
-				
-				local newShape = GetPlayerPickShape()
-				if newShape ~= 0 then
-					if HasTag(newShape, "Yinter") and HasTag(newShape, "Yctrl") then
-						if interAssist then
-							DrawShapeOutline(newShape, 1, 1, 1, 0.4)
-						end
-						UiPush()
-							UiFont("bold.ttf", 22)
-							local str = string.upper(GetString("game.input.grab")).." to "..GetTagValue(newShape, "Yinter")
-							local w = 16 + UiGetTextSize(str)
-							UiAlign("center middle")
-							UiTranslate(UiCenter(), UiMiddle()+400)
-							UiColor(0.8, 1, 1, 0.6)
-							UiImageBox("ui/common/box-solid-6.png", w, 34, 6, 6)
-							UiColor(0, 0, 0)
-							UiText(str)
-						UiPop()
-					end
-				end
-			
-				if lightShapesInit ~= empty then lightShape = true end
-			
-				autoHide = GetBool("savegame.mod.ui.autoHide")
-				autoHideTime = math.floor(GetInt("savegame.mod.ui.autoHideTime")*0.1+5)
-			
-				UiPush()
-					if HasTag(GetPlayerVehicle(), "YLVF") then
-						if autoHide then
-							if not timeGot then
-								uiTime = GetTime()
-								timeGot = true
-							end
-							if (GetTime() - uiTime) > autoHideTime then
-								uioption = true
-							end
-						end
-						if InputPressed(uiKeys[1]) then
-							uioption = not uioption
-							if timeGot then timeGot = false end
-						end
-						if InputPressed(uiKeys[2]) and canUseDyna then
-							showDyna = not showDyna
-						end
-						if (not canUseDyna) and showDyna then
-							showDyna = false
-						end
-						if canUseDyna then
-							info[#info+1] = {string.upper(uiKeys[2]), ((showDyna and "Switch to Basic") or "Switch to Dynamic")}
-						end
-
-						if not uioption then
-							if showDyna then
-								local uiwidth = math.max(340, groupNameW + groupOperationW + 75)
-								local uiheight = dynaCount*26 + 26*3 + 45
-
-								UiTranslate(20, 20)
-								UiAlign("left top")
-								UiColor(0, 0, 0, 0.4)
-								UiImageBox("ui/common/box-solid-6.png", uiwidth, uiheight, 6, 6)
-								UiTranslate(uiwidth/2, 24)
-								UiColor(0.9, 0.9, 0.9)
-								UiAlign("center middle")
-								UiFont("bold.ttf", 26)
-								UiText("Dynamic Parts Operation")
-
-								UiTranslate((groupNameW-groupOperationW)/2, 38)
-								UiPush()
-									UiTranslate(-8, 0)
-									UiAlign("right")
-									UiFont("bold.ttf", 22)
-									for g=1, #dynamicGroup do
-										if dynamicGroup[g][1] then
-											UiText(dynamicGroup[g][2], true)
-										end
-									end
-									UiTranslate(0, 26)
-									for g=#info-1, #info do
-										UiText(info[g][1], true)
-									end
-								UiPop()
-								UiPush()
-									UiTranslate(8, 0)
-									UiAlign("left")
-									UiFont("regular.ttf", 22)
-									for g=1, #dynamicGroup do
-										if dynamicGroup[g][1] then
-											UiText(dynamicKeys[2*g-1].." & "..dynamicKeys[2*g], true)
-										end
-									end
-									UiTranslate(0, 26)
-									for g=#info-1, #info do
-										UiText(info[g][2], true)
-									end
-								UiPop()
-							else
-								local kw = 0
-								local vw = 0
-								for i=1, #info do
-									UiFont("bold.ttf", 22)
-									local w0 = UiGetTextSize(info[i][1])
-									UiFont("regular.ttf", 22)
-									local w1 = UiGetTextSize(info[i][2])
-									kw = math.max(kw,w0)
-									vw = math.max(vw,w1)
-								end
-							
-								local uiwidth = kw + vw + 70
-								local uiheight = #info*22 + 64
-								if uiwidth <= 240 then uiwidth = 240 end
-				
-								UiAlign("left")
-								UiTranslate(20, 20)
-								UiColor(0,0,0,0.4)
-								UiImageBox("ui/common/box-solid-6.png", uiwidth, uiheight, 6, 6)
-								UiTranslate(uiwidth*0.5, 24)
-								UiAlign("center middle")
-								UiColor(0.9, 0.9, 0.9)
-								UiFont("bold.ttf", 26)
-								UiText("Basic Operation")
-
-								UiTranslate((kw-vw)/2, 38)
-								UiPush()
-									UiTranslate(-8, 0)
-									UiAlign("right middle")
-									UiFont("bold.ttf", 22)
-									for i=1, #info do
-										UiText(info[i][1], true)
-									end
-								UiPop()
-								UiPush()
-									UiTranslate(8, 0)
-									UiAlign("left middle")
-									UiFont("regular.ttf", 22)
-									for i=1, #info do
-										UiText(info[i][2], true)
-									end
-								UiPop()
-							end
-						else
-							UiAlign("left")
-							UiTranslate(20, 20)
-							UiColor(0,0,0,0.4)
-							UiImageBox("ui/common/box-solid-6.png", 190, 40, 6, 6)
-							UiTranslate(95, 20)
-							UiAlign("center middle")
-							UiColor(0.9, 0.9, 0.9)
-							UiFont("bold.ttf", 22)
-							UiText(string.upper(uiKeys[1]).." - YLVF Options")
-						end
-					end
-				UiPop()
-			end
-		end
-	end
-end
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
@@ -1,613 +1,600 @@
-#include "library.zip"
-#include "changeLog.lua"
-#include "setup.zip"
-
---[[04-22-2023 (mm-dd-yyyy) version 0.9.4]]--
-
-function init()
-	ClearKey(pathKey.."remote")
-
-	inputScrollFactor = 10
-	empty = {}
-	changeKey = {}
-	wheelMove = false
-	optionShown = "info"
-	slide = 0
-	slideInfo = 0
-	slideKey = 0
-	wheel = 0
-	factor = 0
-	wheelMoveTime = 0
-	tempWheel = 0
-	filter = GetFloat(pathUi.."filter")
-
-	ChangeRegistry()
-	SetupYLVF(true)
-
-	---- Option Regular ----
-
-	infoFeature = {
-		{"No Additional Script Required", "info"},
-		{"Now Integrated with TAT mod", "info"},
-
-		{"Ingame features", ""},
-
-		{"Interactive Doors:", "Auto detction through 'Tags'\nAuto close when player driving vehicle\nAuto open driver seat door when leave the vehicle\nControlled passenger door support"},
-		{"Interactive Hoods:", "Auto detction through 'Tags'\nMultiple usage: hood, trunk door, trailer door & ramp, etc."},
-		{"Interactive Tilting Cabins:", "Auto detection through 'Tags'\nVehicle with broken cabin joints are not able to drive"},
-		{"Controlled Vehicle Lights:", "Auto detction through 'Tags'\nCurrently support: 3 main light modes; (additional) headlights; light signal; blinkers & warnings (with sound); Beacons"},
-		{"Horns & Sirens:", "Auto detction through 'Tags'\n6 horns and 6 siren effects\nMore sound effects to add later on"},
-		{"Mechanical Arm Support:", "Auto detction through 'Tags'\nUpto 5 different groups of joints per vehicle"},
-		{"Fire Engine Support:", "Auto detction through 'Tags'\nUpto 10 different groups of nozzles per vehicle\nFire engine keep active when not driving"},
-		{"Hooks & Winches:", "Winch simulation\n'Hook Assist' option"},
-		{"Custom Spawning Support:", "Able to spawn customized vehicles\nNow support external vehicle packs (more info -> YLVF Toolkit)"},
-		
-		{"Mod Menu Contents", ""},
-
-		{"Key Binding:", "Ability to change keys in mod option"},
-		{"User Interface:", "Auto hide 'Avaliable Operation' menu option\nInteract Assist option\nUpdate information\nMenu Brightness Filter"},
-		{"Vehicle:", "Headlight initial state option\nSpawning panel related options"},
-		{"Debug Mode:", "Draw outline of different targets to help making vehicles"},
-	}
-
-	mainUi = {
-		{"About Mod",		"info",		45,	{0.2, 1, 1}},
-		{"Key Mapping",		"key",		45,	{1, 1, 1}},
-		{"User Interface",	"ui",		45,	{1, 1, 1}},
-		{"Vehicle",			"vehicle",	45,	{1, 1, 1}},
-		{"Debug",			"debug",	45,	{1, 0.7, 0}},
-		{"Exit",			"exit",		45,	{1, 1, 0.3}}
-	}
+#version 2
+function server.init()
+    ClearKey(pathKey.."remote")
+    inputScrollFactor = 10
+    empty = {}
+    changeKey = {}
+    wheelMove = false
+    optionShown = "info"
+    slide = 0
+    slideInfo = 0
+    slideKey = 0
+    wheel = 0
+    factor = 0
+    wheelMoveTime = 0
+    tempWheel = 0
+    filter = GetFloat(pathUi.."filter")
+    ChangeRegistry()
+    SetupYLVF(true)
+    ---- Option Regular ----
+    infoFeature = {
+    	{"No Additional Script Required", "info"},
+    	{"Now Integrated with TAT mod", "info"},
+    	{"Ingame features", ""},
+    	{"Interactive Doors:", "Auto detction through 'Tags'\nAuto close when player driving vehicle\nAuto open driver seat door when leave the vehicle\nControlled passenger door support"},
+    	{"Interactive Hoods:", "Auto detction through 'Tags'\nMultiple usage: hood, trunk door, trailer door & ramp, etc."},
+    	{"Interactive Tilting Cabins:", "Auto detection through 'Tags'\nVehicle with broken cabin joints are not able to drive"},
+    	{"Controlled Vehicle Lights:", "Auto detction through 'Tags'\nCurrently support: 3 main light modes; (additional) headlights; light signal; blinkers & warnings (with sound); Beacons"},
+    	{"Horns & Sirens:", "Auto detction through 'Tags'\n6 horns and 6 siren effects\nMore sound effects to add later on"},
+    	{"Mechanical Arm Support:", "Auto detction through 'Tags'\nUpto 5 different groups of joints per vehicle"},
+    	{"Fire Engine Support:", "Auto detction through 'Tags'\nUpto 10 different groups of nozzles per vehicle\nFire engine keep active when not driving"},
+    	{"Hooks & Winches:", "Winch simulation\n'Hook Assist' option"},
+    	{"Custom Spawning Support:", "Able to spawn customized vehicles\nNow support external vehicle packs (more info -> YLVF Toolkit)"},
+    	{"Mod Menu Contents", ""},
+    	{"Key Binding:", "Ability to change keys in mod option"},
+    	{"User Interface:", "Auto hide 'Avaliable Operation' menu option\nInteract Assist option\nUpdate information\nMenu Brightness Filter"},
+    	{"Vehicle:", "Headlight initial state option\nSpawning panel related options"},
+    	{"Debug Mode:", "Draw outline of different targets to help making vehicles"},
+    }
+    mainUi = {
+    	{"About Mod",		"info",		45,	{0.2, 1, 1}},
+    	{"Key Mapping",		"key",		45,	{1, 1, 1}},
+    	{"User Interface",	"ui",		45,	{1, 1, 1}},
+    	{"Vehicle",			"vehicle",	45,	{1, 1, 1}},
+    	{"Debug",			"debug",	45,	{1, 0.7, 0}},
+    	{"Exit",			"exit",		45,	{1, 1, 0.3}}
+    }
 end
 
-function draw()
-	wheelMove = false
-	wheelMoveTime = 0
-	tempWheel = 0
-
-	UiColorFilter(1, 1, 1, math.max(0.05, 1-(filter/500)))
-	
-	UiTranslate(UiCenter(), 90)
-	UiPush()
-		UiAlign("center middle")
-		UiColor(0, 0.8, 0.8)
-		UiFont(FontList(10), 70)
-		UiText("ylvf options")
-	UiPop()
-	UiTranslate(220-UiCenter(), 130)
-	UiAlign("center middle")
-	UiPush()
-		optionShown, quitMenu = DrawMainUi(300, 90, 130, mainUi, optionShown, 2)
-		if quitMenu then Menu() end
-		UiTranslate(0, #mainUi*130-40)
-		UiColor(0.3, 0.3, 0.3)
-		UiFont(FontList(2), 22)
-		UiText("Version "..updateVersion)
-		w1, h1 = UiGetTextSize("Version "..updateVersion)
-		UiTranslate(0, 26)
-		UiText(updateDate)
-		w2, h2 = UiGetTextSize(updateDate)
-	UiPop()
-	UiTranslate(235, -25)
-	UiAlign("left middle")
-	UiPush()
-		UiAlign("center top")
-		UiTranslate(-30, -25)
-		UiColor(0.3, 0.3, 0.3)
-		UiRect(2, #mainUi*130+(h1+h2)/2+26)
-	UiPop()
-	if optionShown == "debug" then
-		debug = GetBool("savegame.mod.debug")
-		help = GetBool(pathUi.."help")
-		
-		UiPush()
-			UiTranslate(-85, 544)
-			UiAlign("left middle")
-			UiScale(2)
-			UiImage("ui/common/play.png")
-		UiPop()
-
-		UiTranslate(60, 0)
-
-		DLpathDoor = string.format("%sdebugline.%s", pathDebug, "door")
-		DLpathHood = string.format("%sdebugline.%s", pathDebug, "hood")
-		DLpathCabin = string.format("%sdebugline.%s", pathDebug, "cabin")
-		DLpathLight = string.format("%sdebugline.%s", pathDebug, "light")
-		DLpathMTE = string.format("%sdebugline.%s", pathDebug, "MTE")
-		DLpathDynamic = string.format("%sdebugline.%s", pathDebug, "dynamic")
-
-		debugs = {}
-		debugs[#debugs+1] = {"Door DOC.",				GetString(DLpathDoor),		DLpathDoor}
-		debugs[#debugs+1] = {"Hood DOC.",				GetString(DLpathHood),		DLpathHood}
-		debugs[#debugs+1] = {"Cabin DOC.",				GetString(DLpathCabin),		DLpathCabin}
-		debugs[#debugs+1] = {"Light DOC.",				GetString(DLpathLight),		DLpathLight}
-		debugs[#debugs+1] = {"Move-to-End DOC.",		GetString(DLpathMTE),		DLpathMTE}
-		debugs[#debugs+1] = {"Dynamic Parts DOC.",		GetString(DLpathDynamic),	DLpathDynamic}
-
-		debugPressed, debug = DrawColoredTextButtons(debug, "Debug Mode", 300, 45, 2, 30, 0.2, 1, 0.2)
-		if debugPressed then
-			SetBool("savegame.mod.debug", debug)
-		end
-		if true then
-			UiPush()
-				UiTranslate(340, 0)
-				DrawNormalText("DOC. : Debug Outline Color", 1, 20, 0.6, 0.6, 0.6)
-			UiPop()
-			UiTranslate(-40, 70)
-			for i=1, #debugs do
-				UiPush()
-					UiTranslate(20, 0)
-					UiColor(1, 1, 1)
-					UiFont(FontList(2), 32)
-					UiText(debugs[i][1])
-					UiTranslate(-20, 65)
-					DrawRGBselecter(debugs[i][2], debugs[i][3])
-				UiPop()
-				if math.fmod(i, 3) == 0 then
-					UiTranslate(-960, 180)
-				else
-					UiTranslate(480, 0)
-				end
-			end
-			if math.fmod(#debugs, 3) == 1 then
-				UiTranslate(-480, 180)
-			elseif math.fmod(#debugs, 3) == 2 then
-				UiTranslate(-960, 180)
-			end
-			UiTranslate(40, -40)
-		end
-		UiTranslate(0, 66)
-
-		resetPressed, reset = DrawColoredTextButtons(false, "Reset", 300, 45, 2, 30, 0.2, 1, 0.2)
-		if resetPressed then
-			showResetDebug = true
-			fadeDebug = 0.7
-			for i=1, #setupDebug do
-				SetString(pathDebug..setupDebug[i][1], setupDebug[i][2])
-			end
-		end
-		if showResetDebug then
-			UiPush()
-				UiTranslate(400, 0)
-				SetValue("fadeDebug", 0, "easein", 5)
-				UiColor(1, 1, 1, fadeDebug)
-				UiFont(FontList(1), 22)
-				UiText("Settings Haas Been Reset")
-				if fadeDebug == 0 then showResetDebug = false end
-			UiPop()
-		end
-
-	elseif optionShown == "key" then
-
-		UiPush()
-			UiTranslate(-85, 154)
-			UiAlign("left middle")
-			UiScale(2)
-			UiImage("ui/common/play.png")
-		UiPop()
-
-		UiAlign("top left")
-		UiTranslate(0, 51)
-		UiPush()
-			local listLength = 0
-			for i=1, #KeyList do
-				if KeyList[i][1] == "title" then
-					listLength = listLength + 180
-				else
-					listLength = listLength + 45
-				end
-			end
-			UiTranslate(700, scrollAndDrag(1400, 750, listLength, 10, 16, {0.1, 0.1, 0.1}))
-			UiAlign("center middle")
-			UiPush()
-				for i=1, #KeyList do
-					if KeyList[i][1] == "title" then
-						UiTranslate(0, 75)
-						UiPush()
-							UiFont(FontList(10), 50)
-							UiColor(1, 1, 1)
-							UiText(KeyList[i][2])
-						UiPop()
-						UiTranslate(0, 105)
-					else
-						UiPush()
-							UiTranslate(-210, 0)
-							DrawColoredTextButtons(false, KeyList[i][1], 600, 48, 1, 35, 1, 1, 1)
-						UiPop()
-						UiPush()
-							UiTranslate(290, 0)
-							KeyList[i][2] = GetString(pathKey..KeyList[i][3])
-							if KeyList[i][2] ~= "" then
-								keyDisplay = KeyList[i][2]
-							else
-								keyDisplay = "Not Assigned"
-							end
-							change, changeKey[i] = DrawDynamicTextButtons(changeKey[i], keyDisplay, "Press A Key", 380, 48, 6, 35, 1, 1, 1)
-							if changeKey[i] then
-								if InputLastPressedKey() == "tab" or InputLastPressedKey() == "esc" then
-									changeKey[i] = false
-								else
-									if InputPressed(",") then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], ",")
-									elseif InputPressed(".") then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], ".")
-									elseif InputPressed("-") then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "-")
-									elseif InputPressed("+") then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "+")
-									elseif InputPressed("lmb") then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "LMB")
-									elseif InputPressed("rmb") then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "RMB")
-									elseif InputPressed("mmb") then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "MMB")
-									elseif InputLastPressedKey() ~= "" then
-										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], InputLastPressedKey())
-									end
-									KeyList[i] = {KeyList[i][1], GetString(pathKey..KeyList[i][3]), KeyList[i][3]}
-									n = 0
-									sameKey = false
-									repeat
-										n = n + 1
-										if n ~= i and KeyList[n][2] == GetString(pathKey..KeyList[i][3]) then
-											SetString(pathKey..KeyList[n][3], "")
-											KeyList[n] = {KeyList[n][1], GetString(pathKey..KeyList[n][3]), KeyList[n][3]}
-											sameKey = true
-										end
-									until (n == #KeyList or sameKey)
-								end
-							end
-						UiPop()
-						UiTranslate(0, 45)
-					end
-				end
-				UiTranslate(-15, 100)
-				resetPressed, reset = DrawColoredTextButtons(false, "Reset Keys to Default", 990, 80, 10, 48, 0.2, 1, 0.2)
-				if resetPressed then
-					showResetKey = true
-					fadeKey = 0.7
-					for i=1, #setupKey do
-						SetString(pathKey..setupKey[i][1], setupKey[i][2])
-					end
-			
-					for i=1, #setupKeyextra do
-						SetString(pathKey..setupKeyextra[i][1], setupKeyextra[i][2])
-					end
-				end
-				if showResetKey then
-					UiPush()
-						UiTranslate(0, 90)
-						SetValue("fadeKey", 0, "easein", 5)
-						UiColor(1, 1, 1, fadeKey)
-						UiFont(FontList(1), 32)
-						UiText("Settings Haas Been Reset")
-						if fadeKey == 0 then showResetKey = false end
-					UiPop()
-				end
-			UiPop()
-		UiPop()
-
-	elseif optionShown == "ui" then
-
-		autoHide = GetBool(pathUi.."autoHide")
-		autoHideTime = GetInt(pathUi.."autoHideTime")
-		hookAssist = GetBool(pathUi.."hookAssist")
-		interAssist = GetBool(pathUi.."interAssist")
-		showUpdate = GetBool(pathUi.."showUpdate")
-
-		UiPush()
-			UiTranslate(-85, 284)
-			UiAlign("left middle")
-			UiScale(2)
-			UiImage("ui/common/play.png")
-		UiPop()
-
-		UiTranslate(60, 0)
-
-		autoHidePressed, autoHide = DrawColoredTextButtons(autoHide, "Auto Hide", 300, 45, 1, 30, 0.2, 1, 0.2)
-		if autoHidePressed then
-			SetBool(pathUi.."autoHide", autoHide)
-		end
-		if autoHide then
-			UiPush()
-				UiTranslate(340, 0)
-				DrawValueText(math.floor(autoHideTime*0.1+5), "Seconds", 6, 24, 1, 1, 1)
-				UiTranslate(150, 0)
-				autoHideTime, slideDone = DrawSlider(autoHideTime, 300, 0.2, 0.2, 0.2, 0.2, 1, 0.2)
-			UiPop()
-			autoHideTime = math.floor(autoHideTime)
-			SetInt(pathUi.."autoHideTime", autoHideTime)
-		end
-		UiTranslate(0, 70)
-
-		hookAssistPressed, hookAssist = DrawColoredTextButtons(hookAssist, "Hook Assist", 300, 45, 1, 30, 0.2, 1, 0.2)
-		if hookAssistPressed then
-			SetBool(pathUi.."hookAssist", hookAssist)
-		end
-		UiPush()
-			UiTranslate(340, 0)
-			UiColor(0.7, 0.7, 0.7)
-			UiFont(FontList(1), 26)
-			UiText("Draw an orange dot at connecting point")
-		UiPop()
-		UiTranslate(0, 70)
-
-		interAssistPressed, interAssist = DrawColoredTextButtons(interAssist, "Interact Assist", 300, 45, 1, 30, 0.2, 1, 0.2)
-		if interAssistPressed then
-			SetBool(pathUi.."interAssist", interAssist)
-		end
-		UiPush()
-			UiTranslate(340, 0)
-			UiColor(0.7, 0.7, 0.7)
-			UiFont(FontList(1), 26)
-			UiText("Draw outline for interactive parts")
-		UiPop()
-		UiTranslate(0, 70)
-
-		showUpdatePressed, showUpdate = DrawColoredTextButtons(showUpdate, "Update Information", 300, 45, 1, 30, 0.2, 1, 0.2)
-		if showUpdatePressed then
-			SetBool(pathUi.."showUpdate", showUpdate)
-		end
-		UiPush()
-			UiTranslate(340, 0)
-			UiColor(0.7, 0.7, 0.7)
-			UiFont(FontList(1), 26)
-			UiText("Show update info when avaliable")
-		UiPop()
-		UiTranslate(0, 70)
-
-		DrawColoredTextButtons(true, "Brightness Filter", 300, 45, 1, 30, 0.2, 1, 0.2)
-		UiPush()
-			UiTranslate(340, 0)
-			UiFont(FontList(1), 30)
-			UiColor(0.9, 0.9, 0.9)
-			UiText("- "..math.ceil(filter/5)/10)
-			UiTranslate(80, 0)
-			filter, slideDone = DrawSlider(filter, 500, 0.2, 0.2, 0.2, 0.2, 1, 0.2)
-			SetFloat(pathUi.."filter", filter)
-		UiPop()
-		UiTranslate(0, 70)
-
-		resetPressed, reset = DrawColoredTextButtons(false, "Reset", 300, 45, 2, 30, 0.2, 1, 0.2)
-		if resetPressed then
-			showResetUi = true
-			fadeUi = 0.7
-			for i=1, #setupUi do
-				if setupUi[i][2] == "bool" then
-					SetBool(pathUi..setupUi[i][1], setupUi[i][3])
-				elseif setupUi[i][2] == "float" then
-					SetFloat(pathUi..setupUi[i][1], setupUi[i][3])
-				elseif setupUi[i][2] == "string" then
-					SetString(pathUi..setupUi[i][1], setupUi[i][3])
-				else
-					SetInt(pathUi..setupUi[i][1], setupUi[i][3])
-				end
-			end
-		end
-		if showResetUi then
-			UiPush()
-				UiTranslate(380, 0)
-				SetValue("fadeUi", 0, "easein", 5)
-				UiColor(1, 1, 1, fadeUi)
-				UiFont(FontList(1), 22)
-				UiText("Settings Haas Been Reset")
-				if fadeUi == 0 then showResetUi = false end
-			UiPop()
-		end
-	elseif optionShown == "vehicle" then
-		
-		autoFM = GetBool(pathVehicle.."autoFM")
-		advFM = GetBool(pathVehicle.."advFM")
-		autoPre = GetBool(pathVehicle.."autoPre")
-		advPre = GetBool(pathVehicle.."advPre")
-		lightPre = GetBool(pathVehicle.."lightPre")
-		shortCode = GetBool(pathVehicle.."shortCode")
-
-		UiPush()
-			UiTranslate(-85, 414)
-			UiAlign("left middle")
-			UiScale(2)
-			UiImage("ui/common/play.png")
-		UiPop()
-
-		UiTranslate(60, 0)
-
-		autoFMPressed, autoFM = DrawColoredTextButtons(autoFM, "Auto Headlight", 300, 45, 1, 30, 0.2, 1, 0.2)
-		if autoFMPressed then
-			SetBool(pathVehicle.."autoFM", autoFM)
-		end
-		if autoFM then
-			UiPush()
-				UiTranslate(340, 0)
-				advFMPressed, advFM = DrawColoredTextButtons(advFM, "Advanced Headlight", 300, 45, 1, 30, 0.2, 1, 0.2)
-				if advFMPressed then
-					SetBool(pathVehicle.."advFM", advFM)
-				end
-
-				UiPush()
-					UiTranslate(340, 0)
-					UiColor(0.7, 0.7, 0.7)
-					UiFont(FontList(1), 26)
-					UiText("Headlight initial state depends on time of map")
-				UiPop()
-			UiPop()
-		else
-			UiPush()
-				UiTranslate(340, 0)
-				UiColor(0.7, 0.7, 0.7)
-				UiFont(FontList(1), 26)
-				UiText("Headlights of vehicles automatically switch on (like vanilla)")
-			UiPop()
-		end
-		UiTranslate(0, 70)
-
-		autoPrePressed, autoPre = DrawColoredTextButtons(autoPre, "Auto Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
-		if autoPrePressed then
-			SetBool(pathVehicle.."autoPre", autoPre)
-		end
-		if autoPre then
-			UiPush()
-				UiTranslate(340, 0)
-				advPrePressed, advPre = DrawColoredTextButtons(advPre, "Rapid Color Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
-				if advPrePressed then
-					SetBool(pathVehicle.."advPre", advPre)
-				end
-
-				UiPush()
-					UiTranslate(340, 0)
-					UiColor(0.7, 0.7, 0.7)
-					UiFont(FontList(1), 26)
-					UiText("Constantly update paint color when adjusting")
-				UiPop()
-			UiPop()
-		else
-			UiPush()
-				UiTranslate(340, 0)
-				UiColor(0.7, 0.7, 0.7)
-				UiFont(FontList(1), 26)
-				UiText("Automatically update preview vehicle when possible")
-			UiPop()
-		end
-
-		UiTranslate(0, 70)
-
-		lightPrePressed, lightPre = DrawColoredTextButtons(lightPre, "Light Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
-		UiPush()
-			UiTranslate(340, 0)
-			UiColor(0.7, 0.7, 0.7)
-			UiFont(FontList(1), 26)
-			UiText("All lights on vehicle would turn on in freecam mode")
-		UiPop()
-		if lightPrePressed then
-			SetBool(pathVehicle.."lightPre", lightPre)
-		end
-
-		UiTranslate(0, 70)
-
-		shortCodePressed, shortCode = DrawColoredTextButtons(shortCode, "Vehicle Short Code", 300, 45, 1, 30, 0.2, 1, 0.2)
-		UiPush()
-			UiTranslate(340, 0)
-			UiColor(0.7, 0.7, 0.7)
-			UiFont(FontList(1), 26)
-			UiText("Show saved vehicle's short code when selected from spawn panel")
-		UiPop()
-		if shortCodePressed then
-			SetBool(pathVehicle.."shortCode", shortCode)
-		end
-
-		UiTranslate(0, 70)
-
-		resetPressed, reset = DrawColoredTextButtons(false, "Reset", 300, 45, 2, 30, 0.2, 1, 0.2)
-		if resetPressed then
-			showResetUi = true
-			fadeUi = 0.7
-
-			for i=1, #setupVehicle do
-				if setupVehicle[i][2] == "bool" then
-					SetBool(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
-				elseif setupVehicle[i][2] == "float" then
-					SetFloat(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
-				elseif setupVehicle[i][2] == "string" then
-					SetString(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
-				else
-					SetInt(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
-				end
-			end
-		end
-		if showResetUi then
-			UiPush()
-				UiTranslate(380, 0)
-				SetValue("fadeUi", 0, "easein", 5)
-				UiColor(1, 1, 1, fadeUi)
-				UiFont(FontList(1), 22)
-				UiText("Settings Haas Been Reset")
-				if fadeUi == 0 then showResetUi = false end
-			UiPop()
-		end
-
-	elseif optionShown == "info" then
-		UiPush()
-			UiTranslate(-85, 24)
-			UiAlign("left middle")
-			UiScale(2)
-			UiImage("ui/common/play.png")
-		UiPop()
-		UiPush()
-			UiTranslate(420, 0)
-			UiColor(1, 1, 1)
-			UiFont(FontList(2), 50)
-			UiText("Features")
-		UiPop()
-		UiPush()
-			UiAlign("top left")
-			UiTranslate(0, 51)
-			local listLength = 0
-			for i=1, #infoFeature do
-				if infoFeature[i][2] == "" then
-					listLength = listLength + 96
-				elseif infoFeature[i][2] == "info" then
-					listLength = listLength + 32
-				else
-					UiPush()
-						UiFont(FontList(1), 24)
-						local w, h = UiGetTextSize(infoFeature[i][2])
-					UiPop()
-					if h <= 10 then
-						listLength = listLength + 46
-					else
-						listLength = listLength + 16 + h
-					end
-				end
-			end
-			UiPush()
-				UiTranslate(700, scrollAndDrag(1400, 750, listLength, 10, 10, {0.1, 0.1, 0.1}))
-				UiAlign("center middle")
-				UiPush()
-					UiTranslate(-500, 40)
-					UiAlign("left top")
-					UiColor(1, 1, 1, 0.8)
-					for i=1, #infoFeature do
-						if infoFeature[i][2] == "" then
-							num = 0
-							UiTranslate(40, 16)
-							UiFont(FontList(10), 30)
-							UiWordWrap(650)
-							UiText(infoFeature[i][1])
-							UiTranslate(-40, 80)
-						elseif infoFeature[i][2] == "info" then
-							num = 0
-							UiTranslate(40, 0)
-							UiFont(FontList(2), 30)
-							UiText(infoFeature[i][1])
-							UiTranslate(-40, 32)
-						else
-							num = num + 1
-							UiFont(FontList(6), 30)
-							UiText(num)
-							UiTranslate(40, 0)
-							UiFont(FontList(2), 30)
-							UiText(infoFeature[i][1])
-							UiTranslate(380, 0)
-							UiFont(FontList(1), 24)
-							UiText(infoFeature[i][2])
-							w, h = UiGetTextSize(infoFeature[i][2])
-							if h <= 10 then
-								UiTranslate(-420, 46)
-							else
-								UiTranslate(-420, 16+h)
-							end
-						end
-					end
-				UiPop()
-			UiPop()
-		UiPop()
-	end
-end+function client.draw()
+    wheelMove = false
+    wheelMoveTime = 0
+    tempWheel = 0
+
+    UiColorFilter(1, 1, 1, math.max(0.05, 1-(filter/500)))
+
+    UiTranslate(UiCenter(), 90)
+    UiPush()
+    	UiAlign("center middle")
+    	UiColor(0, 0.8, 0.8)
+    	UiFont(FontList(10), 70)
+    	UiText("ylvf options")
+    UiPop()
+    UiTranslate(220-UiCenter(), 130)
+    UiAlign("center middle")
+    UiPush()
+    	optionShown, quitMenu = DrawMainUi(300, 90, 130, mainUi, optionShown, 2)
+    	if quitMenu then Menu() end
+    	UiTranslate(0, #mainUi*130-40)
+    	UiColor(0.3, 0.3, 0.3)
+    	UiFont(FontList(2), 22)
+    	UiText("Version "..updateVersion)
+    	w1, h1 = UiGetTextSize("Version "..updateVersion)
+    	UiTranslate(0, 26)
+    	UiText(updateDate)
+    	w2, h2 = UiGetTextSize(updateDate)
+    UiPop()
+    UiTranslate(235, -25)
+    UiAlign("left middle")
+    UiPush()
+    	UiAlign("center top")
+    	UiTranslate(-30, -25)
+    	UiColor(0.3, 0.3, 0.3)
+    	UiRect(2, #mainUi*130+(h1+h2)/2+26)
+    UiPop()
+    if optionShown == "debug" then
+    	debug = GetBool("savegame.mod.debug")
+    	help = GetBool(pathUi.."help")
+
+    	UiPush()
+    		UiTranslate(-85, 544)
+    		UiAlign("left middle")
+    		UiScale(2)
+    		UiImage("ui/common/play.png")
+    	UiPop()
+
+    	UiTranslate(60, 0)
+
+    	DLpathDoor = string.format("%sdebugline.%s", pathDebug, "door")
+    	DLpathHood = string.format("%sdebugline.%s", pathDebug, "hood")
+    	DLpathCabin = string.format("%sdebugline.%s", pathDebug, "cabin")
+    	DLpathLight = string.format("%sdebugline.%s", pathDebug, "light")
+    	DLpathMTE = string.format("%sdebugline.%s", pathDebug, "MTE")
+    	DLpathDynamic = string.format("%sdebugline.%s", pathDebug, "dynamic")
+
+    	debugs = {}
+    	debugs[#debugs+1] = {"Door DOC.",				GetString(DLpathDoor),		DLpathDoor}
+    	debugs[#debugs+1] = {"Hood DOC.",				GetString(DLpathHood),		DLpathHood}
+    	debugs[#debugs+1] = {"Cabin DOC.",				GetString(DLpathCabin),		DLpathCabin}
+    	debugs[#debugs+1] = {"Light DOC.",				GetString(DLpathLight),		DLpathLight}
+    	debugs[#debugs+1] = {"Move-to-End DOC.",		GetString(DLpathMTE),		DLpathMTE}
+    	debugs[#debugs+1] = {"Dynamic Parts DOC.",		GetString(DLpathDynamic),	DLpathDynamic}
+
+    	debugPressed, debug = DrawColoredTextButtons(debug, "Debug Mode", 300, 45, 2, 30, 0.2, 1, 0.2)
+    	if debugPressed then
+    		SetBool("savegame.mod.debug", debug, true)
+    	end
+    	if true then
+    		UiPush()
+    			UiTranslate(340, 0)
+    			DrawNormalText("DOC. : Debug Outline Color", 1, 20, 0.6, 0.6, 0.6)
+    		UiPop()
+    		UiTranslate(-40, 70)
+    		for i=1, #debugs do
+    			UiPush()
+    				UiTranslate(20, 0)
+    				UiColor(1, 1, 1)
+    				UiFont(FontList(2), 32)
+    				UiText(debugs[i][1])
+    				UiTranslate(-20, 65)
+    				DrawRGBselecter(debugs[i][2], debugs[i][3])
+    			UiPop()
+    			if math.fmod(i, 3) == 0 then
+    				UiTranslate(-960, 180)
+    			else
+    				UiTranslate(480, 0)
+    			end
+    		end
+    		if math.fmod(#debugs, 3) == 1 then
+    			UiTranslate(-480, 180)
+    		elseif math.fmod(#debugs, 3) == 2 then
+    			UiTranslate(-960, 180)
+    		end
+    		UiTranslate(40, -40)
+    	end
+    	UiTranslate(0, 66)
+
+    	resetPressed, reset = DrawColoredTextButtons(false, "Reset", 300, 45, 2, 30, 0.2, 1, 0.2)
+    	if resetPressed then
+    		showResetDebug = true
+    		fadeDebug = 0.7
+    		for i=1, #setupDebug do
+    			SetString(pathDebug..setupDebug[i][1], setupDebug[i][2], true)
+    		end
+    	end
+    	if showResetDebug then
+    		UiPush()
+    			UiTranslate(400, 0)
+    			SetValue("fadeDebug", 0, "easein", 5)
+    			UiColor(1, 1, 1, fadeDebug)
+    			UiFont(FontList(1), 22)
+    			UiText("Settings Haas Been Reset")
+    			if fadeDebug == 0 then showResetDebug = false end
+    		UiPop()
+    	end
+
+    elseif optionShown == "key" then
+
+    	UiPush()
+    		UiTranslate(-85, 154)
+    		UiAlign("left middle")
+    		UiScale(2)
+    		UiImage("ui/common/play.png")
+    	UiPop()
+
+    	UiAlign("top left")
+    	UiTranslate(0, 51)
+    	UiPush()
+    		local listLength = 0
+    		for i=1, #KeyList do
+    			if KeyList[i][1] == "title" then
+    				listLength = listLength + 180
+    			else
+    				listLength = listLength + 45
+    			end
+    		end
+    		UiTranslate(700, scrollAndDrag(1400, 750, listLength, 10, 16, {0.1, 0.1, 0.1}))
+    		UiAlign("center middle")
+    		UiPush()
+    			for i=1, #KeyList do
+    				if KeyList[i][1] == "title" then
+    					UiTranslate(0, 75)
+    					UiPush()
+    						UiFont(FontList(10), 50)
+    						UiColor(1, 1, 1)
+    						UiText(KeyList[i][2])
+    					UiPop()
+    					UiTranslate(0, 105)
+    				else
+    					UiPush()
+    						UiTranslate(-210, 0)
+    						DrawColoredTextButtons(false, KeyList[i][1], 600, 48, 1, 35, 1, 1, 1)
+    					UiPop()
+    					UiPush()
+    						UiTranslate(290, 0)
+    						KeyList[i][2] = GetString(pathKey..KeyList[i][3])
+    						if KeyList[i][2] ~= "" then
+    							keyDisplay = KeyList[i][2]
+    						else
+    							keyDisplay = "Not Assigned"
+    						end
+    						change, changeKey[i] = DrawDynamicTextButtons(changeKey[i], keyDisplay, "Press A Key", 380, 48, 6, 35, 1, 1, 1)
+    						if changeKey[i] then
+    							if InputLastPressedKey() == "tab" or InputLastPressedKey() == "esc" then
+    								changeKey[i] = false
+    							else
+    								if InputPressed(",") then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], ",")
+    								elseif InputPressed(".") then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], ".", true)
+    								elseif InputPressed("-") then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], "-", true)
+    								elseif InputPressed("+") then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], "+", true)
+    								elseif InputPressed("lmb") then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], "LMB", true)
+    								elseif InputPressed("rmb") then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], "RMB", true)
+    								elseif InputPressed("mmb") then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], "MMB", true)
+    								elseif InputLastPressedKey() ~= "" then
+    									changeKey[i] = false
+    									SetString(pathKey..KeyList[i][3], InputLastPressedKey(), true)
+    								end
+    								KeyList[i] = {KeyList[i][1], GetString(pathKey..KeyList[i][3]), KeyList[i][3]}
+    								n = 0
+    								sameKey = false
+    								repeat
+    									n = n + 1
+    									if n ~= i and KeyList[n][2] == GetString(pathKey..KeyList[i][3]) then
+    										SetString(pathKey..KeyList[n][3], "", true)
+    										KeyList[n] = {KeyList[n][1], GetString(pathKey..KeyList[n][3]), KeyList[n][3]}
+    										sameKey = true
+    									end
+    								until (n == #KeyList or sameKey)
+    							end
+    						end
+    					UiPop()
+    					UiTranslate(0, 45)
+    				end
+    			end
+    			UiTranslate(-15, 100)
+    			resetPressed, reset = DrawColoredTextButtons(false, "Reset Keys to Default", 990, 80, 10, 48, 0.2, 1, 0.2)
+    			if resetPressed then
+    				showResetKey = true
+    				fadeKey = 0.7
+    				for i=1, #setupKey do
+    					SetString(pathKey..setupKey[i][1], setupKey[i][2], true)
+    				end
+
+    				for i=1, #setupKeyextra do
+    					SetString(pathKey..setupKeyextra[i][1], setupKeyextra[i][2], true)
+    				end
+    			end
+    			if showResetKey then
+    				UiPush()
+    					UiTranslate(0, 90)
+    					SetValue("fadeKey", 0, "easein", 5)
+    					UiColor(1, 1, 1, fadeKey)
+    					UiFont(FontList(1), 32)
+    					UiText("Settings Haas Been Reset")
+    					if fadeKey == 0 then showResetKey = false end
+    				UiPop()
+    			end
+    		UiPop()
+    	UiPop()
+
+    elseif optionShown == "ui" then
+
+    	autoHide = GetBool(pathUi.."autoHide")
+    	autoHideTime = GetInt(pathUi.."autoHideTime")
+    	hookAssist = GetBool(pathUi.."hookAssist")
+    	interAssist = GetBool(pathUi.."interAssist")
+    	showUpdate = GetBool(pathUi.."showUpdate")
+
+    	UiPush()
+    		UiTranslate(-85, 284)
+    		UiAlign("left middle")
+    		UiScale(2)
+    		UiImage("ui/common/play.png")
+    	UiPop()
+
+    	UiTranslate(60, 0)
+
+    	autoHidePressed, autoHide = DrawColoredTextButtons(autoHide, "Auto Hide", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	if autoHidePressed then
+    		SetBool(pathUi.."autoHide", autoHide, true)
+    	end
+    	if autoHide then
+    		UiPush()
+    			UiTranslate(340, 0)
+    			DrawValueText(math.floor(autoHideTime*0.1+5), "Seconds", 6, 24, 1, 1, 1)
+    			UiTranslate(150, 0)
+    			autoHideTime, slideDone = DrawSlider(autoHideTime, 300, 0.2, 0.2, 0.2, 0.2, 1, 0.2)
+    		UiPop()
+    		autoHideTime = math.floor(autoHideTime)
+    		SetInt(pathUi.."autoHideTime", autoHideTime, true)
+    	end
+    	UiTranslate(0, 70)
+
+    	hookAssistPressed, hookAssist = DrawColoredTextButtons(hookAssist, "Hook Assist", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	if hookAssistPressed then
+    		SetBool(pathUi.."hookAssist", hookAssist, true)
+    	end
+    	UiPush()
+    		UiTranslate(340, 0)
+    		UiColor(0.7, 0.7, 0.7)
+    		UiFont(FontList(1), 26)
+    		UiText("Draw an orange dot at connecting point")
+    	UiPop()
+    	UiTranslate(0, 70)
+
+    	interAssistPressed, interAssist = DrawColoredTextButtons(interAssist, "Interact Assist", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	if interAssistPressed then
+    		SetBool(pathUi.."interAssist", interAssist, true)
+    	end
+    	UiPush()
+    		UiTranslate(340, 0)
+    		UiColor(0.7, 0.7, 0.7)
+    		UiFont(FontList(1), 26)
+    		UiText("Draw outline for interactive parts")
+    	UiPop()
+    	UiTranslate(0, 70)
+
+    	showUpdatePressed, showUpdate = DrawColoredTextButtons(showUpdate, "Update Information", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	if showUpdatePressed then
+    		SetBool(pathUi.."showUpdate", showUpdate, true)
+    	end
+    	UiPush()
+    		UiTranslate(340, 0)
+    		UiColor(0.7, 0.7, 0.7)
+    		UiFont(FontList(1), 26)
+    		UiText("Show update info when avaliable")
+    	UiPop()
+    	UiTranslate(0, 70)
+
+    	DrawColoredTextButtons(true, "Brightness Filter", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	UiPush()
+    		UiTranslate(340, 0)
+    		UiFont(FontList(1), 30)
+    		UiColor(0.9, 0.9, 0.9)
+    		UiText("- "..math.ceil(filter/5)/10)
+    		UiTranslate(80, 0)
+    		filter, slideDone = DrawSlider(filter, 500, 0.2, 0.2, 0.2, 0.2, 1, 0.2)
+    		SetFloat(pathUi.."filter", filter, true)
+    	UiPop()
+    	UiTranslate(0, 70)
+
+    	resetPressed, reset = DrawColoredTextButtons(false, "Reset", 300, 45, 2, 30, 0.2, 1, 0.2)
+    	if resetPressed then
+    		showResetUi = true
+    		fadeUi = 0.7
+    		for i=1, #setupUi do
+    			if setupUi[i][2] == "bool" then
+    				SetBool(pathUi..setupUi[i][1], setupUi[i][3], true)
+    			elseif setupUi[i][2] == "float" then
+    				SetFloat(pathUi..setupUi[i][1], setupUi[i][3], true)
+    			elseif setupUi[i][2] == "string" then
+    				SetString(pathUi..setupUi[i][1], setupUi[i][3], true)
+    			else
+    				SetInt(pathUi..setupUi[i][1], setupUi[i][3], true)
+    			end
+    		end
+    	end
+    	if showResetUi then
+    		UiPush()
+    			UiTranslate(380, 0)
+    			SetValue("fadeUi", 0, "easein", 5)
+    			UiColor(1, 1, 1, fadeUi)
+    			UiFont(FontList(1), 22)
+    			UiText("Settings Haas Been Reset")
+    			if fadeUi == 0 then showResetUi = false end
+    		UiPop()
+    	end
+    elseif optionShown == "vehicle" then
+
+    	autoFM = GetBool(pathVehicle.."autoFM")
+    	advFM = GetBool(pathVehicle.."advFM")
+    	autoPre = GetBool(pathVehicle.."autoPre")
+    	advPre = GetBool(pathVehicle.."advPre")
+    	lightPre = GetBool(pathVehicle.."lightPre")
+    	shortCode = GetBool(pathVehicle.."shortCode")
+
+    	UiPush()
+    		UiTranslate(-85, 414)
+    		UiAlign("left middle")
+    		UiScale(2)
+    		UiImage("ui/common/play.png")
+    	UiPop()
+
+    	UiTranslate(60, 0)
+
+    	autoFMPressed, autoFM = DrawColoredTextButtons(autoFM, "Auto Headlight", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	if autoFMPressed then
+    		SetBool(pathVehicle.."autoFM", autoFM, true)
+    	end
+    	if autoFM then
+    		UiPush()
+    			UiTranslate(340, 0)
+    			advFMPressed, advFM = DrawColoredTextButtons(advFM, "Advanced Headlight", 300, 45, 1, 30, 0.2, 1, 0.2)
+    			if advFMPressed then
+    				SetBool(pathVehicle.."advFM", advFM, true)
+    			end
+
+    			UiPush()
+    				UiTranslate(340, 0)
+    				UiColor(0.7, 0.7, 0.7)
+    				UiFont(FontList(1), 26)
+    				UiText("Headlight initial state depends on time of map")
+    			UiPop()
+    		UiPop()
+    	else
+    		UiPush()
+    			UiTranslate(340, 0)
+    			UiColor(0.7, 0.7, 0.7)
+    			UiFont(FontList(1), 26)
+    			UiText("Headlights of vehicles automatically switch on (like vanilla)")
+    		UiPop()
+    	end
+    	UiTranslate(0, 70)
+
+    	autoPrePressed, autoPre = DrawColoredTextButtons(autoPre, "Auto Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	if autoPrePressed then
+    		SetBool(pathVehicle.."autoPre", autoPre, true)
+    	end
+    	if autoPre then
+    		UiPush()
+    			UiTranslate(340, 0)
+    			advPrePressed, advPre = DrawColoredTextButtons(advPre, "Rapid Color Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
+    			if advPrePressed then
+    				SetBool(pathVehicle.."advPre", advPre, true)
+    			end
+
+    			UiPush()
+    				UiTranslate(340, 0)
+    				UiColor(0.7, 0.7, 0.7)
+    				UiFont(FontList(1), 26)
+    				UiText("Constantly update paint color when adjusting")
+    			UiPop()
+    		UiPop()
+    	else
+    		UiPush()
+    			UiTranslate(340, 0)
+    			UiColor(0.7, 0.7, 0.7)
+    			UiFont(FontList(1), 26)
+    			UiText("Automatically update preview vehicle when possible")
+    		UiPop()
+    	end
+
+    	UiTranslate(0, 70)
+
+    	lightPrePressed, lightPre = DrawColoredTextButtons(lightPre, "Light Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	UiPush()
+    		UiTranslate(340, 0)
+    		UiColor(0.7, 0.7, 0.7)
+    		UiFont(FontList(1), 26)
+    		UiText("All lights on vehicle would turn on in freecam mode")
+    	UiPop()
+    	if lightPrePressed then
+    		SetBool(pathVehicle.."lightPre", lightPre, true)
+    	end
+
+    	UiTranslate(0, 70)
+
+    	shortCodePressed, shortCode = DrawColoredTextButtons(shortCode, "Vehicle Short Code", 300, 45, 1, 30, 0.2, 1, 0.2)
+    	UiPush()
+    		UiTranslate(340, 0)
+    		UiColor(0.7, 0.7, 0.7)
+    		UiFont(FontList(1), 26)
+    		UiText("Show saved vehicle's short code when selected from spawn panel")
+    	UiPop()
+    	if shortCodePressed then
+    		SetBool(pathVehicle.."shortCode", shortCode, true)
+    	end
+
+    	UiTranslate(0, 70)
+
+    	resetPressed, reset = DrawColoredTextButtons(false, "Reset", 300, 45, 2, 30, 0.2, 1, 0.2)
+    	if resetPressed then
+    		showResetUi = true
+    		fadeUi = 0.7
+
+    		for i=1, #setupVehicle do
+    			if setupVehicle[i][2] == "bool" then
+    				SetBool(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
+    			elseif setupVehicle[i][2] == "float" then
+    				SetFloat(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
+    			elseif setupVehicle[i][2] == "string" then
+    				SetString(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
+    			else
+    				SetInt(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
+    			end
+    		end
+    	end
+    	if showResetUi then
+    		UiPush()
+    			UiTranslate(380, 0)
+    			SetValue("fadeUi", 0, "easein", 5)
+    			UiColor(1, 1, 1, fadeUi)
+    			UiFont(FontList(1), 22)
+    			UiText("Settings Haas Been Reset")
+    			if fadeUi == 0 then showResetUi = false end
+    		UiPop()
+    	end
+
+    elseif optionShown == "info" then
+    	UiPush()
+    		UiTranslate(-85, 24)
+    		UiAlign("left middle")
+    		UiScale(2)
+    		UiImage("ui/common/play.png")
+    	UiPop()
+    	UiPush()
+    		UiTranslate(420, 0)
+    		UiColor(1, 1, 1)
+    		UiFont(FontList(2), 50)
+    		UiText("Features")
+    	UiPop()
+    	UiPush()
+    		UiAlign("top left")
+    		UiTranslate(0, 51)
+    		local listLength = 0
+    		for i=1, #infoFeature do
+    			if infoFeature[i][2] == "" then
+    				listLength = listLength + 96
+    			elseif infoFeature[i][2] == "info" then
+    				listLength = listLength + 32
+    			else
+    				UiPush()
+    					UiFont(FontList(1), 24)
+    					local w, h = UiGetTextSize(infoFeature[i][2])
+    				UiPop()
+    				if h <= 10 then
+    					listLength = listLength + 46
+    				else
+    					listLength = listLength + 16 + h
+    				end
+    			end
+    		end
+    		UiPush()
+    			UiTranslate(700, scrollAndDrag(1400, 750, listLength, 10, 10, {0.1, 0.1, 0.1}))
+    			UiAlign("center middle")
+    			UiPush()
+    				UiTranslate(-500, 40)
+    				UiAlign("left top")
+    				UiColor(1, 1, 1, 0.8)
+    				for i=1, #infoFeature do
+    					if infoFeature[i][2] == "" then
+    						num = 0
+    						UiTranslate(40, 16)
+    						UiFont(FontList(10), 30)
+    						UiWordWrap(650)
+    						UiText(infoFeature[i][1])
+    						UiTranslate(-40, 80)
+    					elseif infoFeature[i][2] == "info" then
+    						num = 0
+    						UiTranslate(40, 0)
+    						UiFont(FontList(2), 30)
+    						UiText(infoFeature[i][1])
+    						UiTranslate(-40, 32)
+    					else
+    						num = num + 1
+    						UiFont(FontList(6), 30)
+    						UiText(num)
+    						UiTranslate(40, 0)
+    						UiFont(FontList(2), 30)
+    						UiText(infoFeature[i][1])
+    						UiTranslate(380, 0)
+    						UiFont(FontList(1), 24)
+    						UiText(infoFeature[i][2])
+    						w, h = UiGetTextSize(infoFeature[i][2])
+    						if h <= 10 then
+    							UiTranslate(-420, 46)
+    						else
+    							UiTranslate(-420, 16+h)
+    						end
+    					end
+    				end
+    			UiPop()
+    		UiPop()
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: pauseMenu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pauseMenu.lua
+++ patched/pauseMenu.lua
@@ -1,9 +1,4 @@
-#include "library.zip"
-#include "changeLog.lua"
-#include "setup.zip"
-
---[[05-18-2023 (mm-dd-yyyy) version 0.9.4]]--
-
+#version 2
 function pauseInit()
 
 	inputScrollFactor = 10
@@ -41,10 +36,9 @@
 	mainUi[#mainUi+1] = {"Back to Game", "exit", 45, {1, 1, 0.3}}
 end
 
-
 function pauseDraw()
 	
-	SetBool("game.disablepause", true)
+	SetBool("game.disablepause", true, true)
 
 	wheelMove = false
 	wheelMoveTime = 0
@@ -113,7 +107,7 @@
 
 		debugPressed, debug = DrawColoredTextButtons(debug, "Debug Mode", 300, 45, 2, 30, 0.2, 1, 0.2)
 		if debugPressed then
-			SetBool("savegame.mod.debug", debug)
+			SetBool("savegame.mod.debug", debug, true)
 		end
 		if true then
 			UiPush()
@@ -150,7 +144,7 @@
 			showResetDebug = true
 			fadeDebug = 0.7
 			for i=1, #setupDebug do
-				SetString(pathDebug..setupDebug[i][1], setupDebug[i][2])
+				SetString(pathDebug..setupDebug[i][1], setupDebug[i][2], true)
 			end
 		end
 		if showResetDebug then
@@ -220,25 +214,25 @@
 										SetString(pathKey..KeyList[i][3], ",")
 									elseif InputPressed(".") then
 										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], ".")
+										SetString(pathKey..KeyList[i][3], ".", true)
 									elseif InputPressed("-") then
 										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "-")
+										SetString(pathKey..KeyList[i][3], "-", true)
 									elseif InputPressed("+") then
 										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "+")
+										SetString(pathKey..KeyList[i][3], "+", true)
 									elseif InputPressed("lmb") then
 										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "LMB")
+										SetString(pathKey..KeyList[i][3], "LMB", true)
 									elseif InputPressed("rmb") then
 										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "RMB")
+										SetString(pathKey..KeyList[i][3], "RMB", true)
 									elseif InputPressed("mmb") then
 										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], "MMB")
+										SetString(pathKey..KeyList[i][3], "MMB", true)
 									elseif InputLastPressedKey() ~= "" then
 										changeKey[i] = false
-										SetString(pathKey..KeyList[i][3], InputLastPressedKey())
+										SetString(pathKey..KeyList[i][3], InputLastPressedKey(), true)
 									end
 									KeyList[i] = {KeyList[i][1], GetString(pathKey..KeyList[i][3]), KeyList[i][3]}
 									n = 0
@@ -246,7 +240,7 @@
 									repeat
 										n = n + 1
 										if n ~= i and KeyList[n][2] == GetString(pathKey..KeyList[i][3]) then
-											SetString(pathKey..KeyList[n][3], "")
+											SetString(pathKey..KeyList[n][3], "", true)
 											KeyList[n] = {KeyList[n][1], GetString(pathKey..KeyList[n][3]), KeyList[n][3]}
 											sameKey = true
 										end
@@ -263,11 +257,11 @@
 					showResetKey = true
 					fadeKey = 0.7
 					for i=1, #setupKey do
-						SetString(pathKey..setupKey[i][1], setupKey[i][2])
+						SetString(pathKey..setupKey[i][1], setupKey[i][2], true)
 					end
 			
 					for i=1, #setupKeyextra do
-						SetString(pathKey..setupKeyextra[i][1], setupKeyextra[i][2])
+						SetString(pathKey..setupKeyextra[i][1], setupKeyextra[i][2], true)
 					end
 				end
 				if showResetKey then
@@ -304,7 +298,7 @@
 
 		autoHidePressed, autoHide = DrawColoredTextButtons(autoHide, "Auto Hide", 300, 45, 1, 30, 0.2, 1, 0.2)
 		if autoHidePressed then
-			SetBool(pathUi.."autoHide", autoHide)
+			SetBool(pathUi.."autoHide", autoHide, true)
 		end
 		if autoHide then
 			UiPush()
@@ -314,13 +308,13 @@
 				autoHideTime, slideDone = DrawSlider(autoHideTime, 300, 0.2, 0.2, 0.2, 0.2, 1, 0.2)
 			UiPop()
 			autoHideTime = math.floor(autoHideTime)
-			SetInt(pathUi.."autoHideTime", autoHideTime)
+			SetInt(pathUi.."autoHideTime", autoHideTime, true)
 		end
 		UiTranslate(0, 70)
 
 		hookAssistPressed, hookAssist = DrawColoredTextButtons(hookAssist, "Hook Assist", 300, 45, 1, 30, 0.2, 1, 0.2)
 		if hookAssistPressed then
-			SetBool(pathUi.."hookAssist", hookAssist)
+			SetBool(pathUi.."hookAssist", hookAssist, true)
 		end
 		UiPush()
 			UiTranslate(340, 0)
@@ -332,7 +326,7 @@
 
 		interAssistPressed, interAssist = DrawColoredTextButtons(interAssist, "Interact Assist", 300, 45, 1, 30, 0.2, 1, 0.2)
 		if interAssistPressed then
-			SetBool(pathUi.."interAssist", interAssist)
+			SetBool(pathUi.."interAssist", interAssist, true)
 		end
 		UiPush()
 			UiTranslate(340, 0)
@@ -344,7 +338,7 @@
 
 		showUpdatePressed, showUpdate = DrawColoredTextButtons(showUpdate, "Update Information", 300, 45, 1, 30, 0.2, 1, 0.2)
 		if showUpdatePressed then
-			SetBool(pathUi.."showUpdate", showUpdate)
+			SetBool(pathUi.."showUpdate", showUpdate, true)
 		end
 		UiPush()
 			UiTranslate(340, 0)
@@ -362,7 +356,7 @@
 			UiText("- "..math.ceil(filter/5)/10)
 			UiTranslate(80, 0)
 			filter, slideDone = DrawSlider(filter, 500, 0.2, 0.2, 0.2, 0.2, 1, 0.2)
-			SetFloat(pathUi.."filter", filter)
+			SetFloat(pathUi.."filter", filter, true)
 		UiPop()
 		UiTranslate(0, 70)
 
@@ -372,13 +366,13 @@
 			fadeUi = 0.7
 			for i=1, #setupUi do
 				if setupUi[i][2] == "bool" then
-					SetBool(pathUi..setupUi[i][1], setupUi[i][3])
+					SetBool(pathUi..setupUi[i][1], setupUi[i][3], true)
 				elseif setupUi[i][2] == "float" then
-					SetFloat(pathUi..setupUi[i][1], setupUi[i][3])
+					SetFloat(pathUi..setupUi[i][1], setupUi[i][3], true)
 				elseif setupUi[i][2] == "string" then
-					SetString(pathUi..setupUi[i][1], setupUi[i][3])
+					SetString(pathUi..setupUi[i][1], setupUi[i][3], true)
 				else
-					SetInt(pathUi..setupUi[i][1], setupUi[i][3])
+					SetInt(pathUi..setupUi[i][1], setupUi[i][3], true)
 				end
 			end
 		end
@@ -413,14 +407,14 @@
 
 		autoFMPressed, autoFM = DrawColoredTextButtons(autoFM, "Auto Headlight", 300, 45, 1, 30, 0.2, 1, 0.2)
 		if autoFMPressed then
-			SetBool(pathVehicle.."autoFM", autoFM)
+			SetBool(pathVehicle.."autoFM", autoFM, true)
 		end
 		if autoFM then
 			UiPush()
 				UiTranslate(340, 0)
 				advFMPressed, advFM = DrawColoredTextButtons(advFM, "Advanced Headlight", 300, 45, 1, 30, 0.2, 1, 0.2)
 				if advFMPressed then
-					SetBool(pathVehicle.."advFM", advFM)
+					SetBool(pathVehicle.."advFM", advFM, true)
 				end
 
 				UiPush()
@@ -442,16 +436,16 @@
 
 		autoPrePressed, autoPre = DrawColoredTextButtons(autoPre, "Auto Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
 		if autoPrePressed then
-			SetBool(pathVehicle.."autoPre", autoPre)
-			SetBool("YLVF.options.autopre", autoPre)
+			SetBool(pathVehicle.."autoPre", autoPre, true)
+			SetBool("YLVF.options.autopre", autoPre, true)
 		end
 		if autoPre then
 			UiPush()
 				UiTranslate(340, 0)
 				advPrePressed, advPre = DrawColoredTextButtons(advPre, "Rapid Color Preview", 300, 45, 1, 30, 0.2, 1, 0.2)
 				if advPrePressed then
-					SetBool(pathVehicle.."advPre", advPre)
-					SetBool("YLVF.options.advpre", advPre)
+					SetBool(pathVehicle.."advPre", advPre, true)
+					SetBool("YLVF.options.advpre", advPre, true)
 				end
 
 				UiPush()
@@ -480,7 +474,7 @@
 			UiText("All lights on vehicle would turn on in freecam mode")
 		UiPop()
 		if lightPrePressed then
-			SetBool(pathVehicle.."lightPre", lightPre)
+			SetBool(pathVehicle.."lightPre", lightPre, true)
 		end
 
 		UiTranslate(0, 70)
@@ -493,8 +487,8 @@
 			UiText("Show saved vehicle's short code when selected from spawn panel")
 		UiPop()
 		if shortCodePressed then
-			SetBool(pathVehicle.."shortCode", shortCode)
-			SetBool("YLVF.options.shortCode", shortCode)
+			SetBool(pathVehicle.."shortCode", shortCode, true)
+			SetBool("YLVF.options.shortCode", shortCode, true)
 		end
 
 		UiTranslate(0, 70)
@@ -507,7 +501,7 @@
 			UiText("Open customizable vehicle spawning panel")
 		UiPop()
 		if spawnPanelPressed then
-			SetBool("YLVF.pack.menu", true)
+			SetBool("YLVF.pack.menu", true, true)
 			quitGame = true
 		end
 
@@ -520,13 +514,13 @@
 
 			for i=1, #setupVehicle do
 				if setupVehicle[i][2] == "bool" then
-					SetBool(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
+					SetBool(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
 				elseif setupVehicle[i][2] == "float" then
-					SetFloat(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
+					SetFloat(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
 				elseif setupVehicle[i][2] == "string" then
-					SetString(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
+					SetString(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
 				else
-					SetInt(pathVehicle..setupVehicle[i][1], setupVehicle[i][3])
+					SetInt(pathVehicle..setupVehicle[i][1], setupVehicle[i][3], true)
 				end
 			end
 		end
@@ -560,4 +554,5 @@
 	end
 
 	return quitGame
-end+end
+

```

---

# Migration Report: spawnPanel.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/spawnPanel.lua
+++ patched/spawnPanel.lua
@@ -1,13 +1,4 @@
-
---[[05-18-2023 (mm-dd-yyyy) version 0.9.4]]--
-
-#include "library.zip"
-
-panelTranslate = 0
-lightTranslate = 0
-slidePos = 0
-slideValue = 0
-
+#version 2
 function initRAW()
 	local fileName = "YLVF/YLVF.xml"
 	if not done then
@@ -23,7 +14,6 @@
 	end
 end
 
-
 function initNormal(num)
 	local packNum = 0
 	local fileName = "YLVF/YLVF.xml"
@@ -36,33 +26,30 @@
 			end
 		end
 		for i=1, num do
-			SetString("YLVF.colors.slot."..i, GetString("savegame.mod.colors."..i, "5A5A5A"))
+			SetString("YLVF.colors.slot."..i, GetString("savegame.mod.colors."..i, "5A5A5A"), true)
 		end
-		SetString("spawnRE.ext.YLVF.category", "YLVF")
-		SetString("spawnRE.ext.YLVF.name", "YLVF Spawning")
-		SetString("spawnRE.ext.YLVF.activate", "YLVF.pack.menu")
+		SetString("spawnRE.ext.YLVF.category", "YLVF", true)
+		SetString("spawnRE.ext.YLVF.name", "YLVF Spawning", true)
+		SetString("spawnRE.ext.YLVF.activate", "YLVF.pack.menu", true)
 
-		SetBool("YLVF.colors.done", true)
-		SetBool("YLVF.options.autopre", GetBool("savegame.mod.vehicle.autoPre"))
-		SetBool("YLVF.options.advpre", GetBool("savegame.mod.vehicle.advPre"))
-		SetBool("YLVF.options.shortCode", GetBool("savegame.mod.vehicle.shortCode"))
-		SetInt("YLVF.pack.totalnum", packNum)
-		SetBool("YLVF.pack.menu", false)
-		SetBool("YLVF.pack.sub", false)
+		SetBool("YLVF.colors.done", true, true)
+		SetBool("YLVF.options.autopre", GetBool("savegame.mod.vehicle.autoPre"), true)
+		SetBool("YLVF.options.advpre", GetBool("savegame.mod.vehicle.advPre"), true)
+		SetBool("YLVF.options.shortCode", GetBool("savegame.mod.vehicle.shortCode"), true)
+		SetInt("YLVF.pack.totalnum", packNum, true)
+		SetBool("YLVF.pack.menu", false, true)
+		SetBool("YLVF.pack.sub", false, true)
 		done = true
 	end
 end
 
-
 function CheckColorEdit()
 	if not GetBool("YLVF.colors.done") then
 		local changePos = GetInt("YLVF.colors.changePos")
-		SetString("savegame.mod.colors."..changePos, GetString("YLVF.colors.slot."..changePos))
-		SetBool("YLVF.colors.done", true)
+		SetString("savegame.mod.colors."..changePos, GetString("YLVF.colors.slot."..changePos), true)
+		SetBool("YLVF.colors.done", true, true)
 	end
 end
-
-
 
 function GetSpawnPanelWidth()
 	local allPacks = ListKeys("YLVF.packs")
@@ -78,7 +65,6 @@
 	return panelWidth
 end
 
-
 function SpawnPanelMain(width)
 	width = math.max(310, (width or 0))
 
@@ -87,18 +73,18 @@
 
 	if GetBool("YLVF.pack.menu") and panelTranslate == 0 then
 		SetValue("panelTranslate", width+20, "cosine", 0.1)
-		SetBool("YLVF.pack.sub", false)
+		SetBool("YLVF.pack.sub", false, true)
 		for p=1, packNum do
-			SetBool("YLVF.packs."..p..".active", false)
+			SetBool("YLVF.packs."..p..".active", false, true)
 		end
 	elseif not GetBool("YLVF.pack.menu") and panelTranslate == width+20 then
 		SetValue("panelTranslate", 0, "cosine", 0.1)
 	end
 
-	if panelTranslate > 0 then
-		SetBool("game.disablepause", true)
+	if panelTranslate ~= 0 then
+		SetBool("game.disablepause", true, true)
 		UiMakeInteractive()
-		if InputPressed("pause") then SetBool("YLVF.pack.menu", false) end
+		if InputPressed("pause") then SetBool("YLVF.pack.menu", false, true) end
 		UiPush()
 			UiColorFilter(1, 1, 1, 0.95)
 			UiAlign("middle left")
@@ -155,7 +141,6 @@
 	end
 end
 
-
 function DrawPackButtons(num, wid)
 	for p=1, num do
 		UiFont("bold.ttf", 26)
@@ -170,11 +155,12 @@
 		end
 
 		if UiTextButton(packName, wid-40, 40) then
-			SetBool("YLVF.packs."..p..".active", true)
-			SetBool("YLVF.pack.menu", false)
-			SetBool("YLVF.pack.sub", true)
+			SetBool("YLVF.packs."..p..".active", true, true)
+			SetBool("YLVF.pack.menu", false, true)
+			SetBool("YLVF.pack.sub", true, true)
 		end
 
 		UiTranslate(0, 50)
 	end
-end+end
+

```
