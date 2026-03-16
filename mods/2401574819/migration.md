# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,57 +1,4 @@
-blackholeprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false,
-		fuseTimer = 0, 
-		growTimer = 0,
-		gravStrength = 3,
-		maxMass = 100,
-		maxDist = 5,
-	},
-}
-
-function init()
-	RegisterTool("blackhole", "Black Hole", "MOD/vox/blackhole.vox")
-	SetBool("game.tool.blackhole.enabled", true)
-	SetFloat("game.tool.blackhole.ammo", 101)
-
-	maxDistance = GetFloat("savegame.mod.maxdist")
-	maxStrength = GetFloat("savegame.mod.maxstr")
-	maxMass = GetFloat("savegame.mod.maxmass")
-	fuseTime = GetFloat("savegame.mod.maxtime")
-	growSpeed = GetFloat("savegame.mod.growspeed")
-	breakStuff = GetBool("savegame.mod.breakstuff")
-	deleteMass = GetFloat("savegame.mod.deletemass")
-	deleteSmall = GetBool("savegame.mod.deletesmall")
-	deleteRadius = GetFloat("savegame.mod.deletedist")
-	optionsOpen = false
-
-	if not HasKey("savegame.mod.maxdist") then
-		maxDistance = 75
-		maxStrength = 1
-		maxMass = 15000
-		fuseTime = 60
-		growSpeed = 75
-		deleteMass = 50
-		deleteRadius = 3
-	end
-
-	gravity = Vec(0, 0, 0)
-	velocity = 0.1
-	angle = 10
-
-	for i=1, 5 do
-		blackholeprojectileHandler.shells[i] = deepcopy(blackholeprojectileHandler.defaultShell)
-	end
-
-	throwsound = LoadSound("MOD/snd/throw2.ogg")
-
-	fuseTimer = 0
-	shootTimer = 0
-	breakTimer = 0
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -180,253 +127,6 @@
 			vel = VecAdd(vel, add)
 			SetBodyVelocity(b, vel)
 		end
-	end
-end
-
-function tick(dt)
-	if GetString("game.player.tool") == "blackhole" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") and not optionsOpen then
-			Shoot()
-		end
-
-		if InputPressed("O") then optionsOpen = not optionsOpen end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			angle = angle + math.random(2, 10)
-			local t = Transform()
-			t.pos = Vec(0.3, -0.4, -0.7)
-			t.rot = QuatEuler(angle, angle/3, angle/2)
-			SetToolTransform(t)
-
-			local p = TransformToParentPoint(GetBodyTransform(b), Vec(0, 0, -2))
-			PointLight(p, 0, 0, 0, 0.5)
-		end
-	end
-
-	for key, shell in ipairs(blackholeprojectileHandler.shells) do
-		if shell.active then
-			BlackholeOperations(shell)
-			shell.growTimer = shell.growTimer + (dt/2)*(growSpeed/50)
-		end
-
-		if shell.fuseTimer > 0 then
-			shell.fuseTimer = shell.fuseTimer - dt
-			if shell.fuseTimer < 0.01 then
-				shell.fuseTimer = 0
-				shell.growTimer = 0
-			end
-			if InputPressed("c") then
-				BlackHolePush(shell)
-				shell.fuseTimer = 0
-				shell.growTimer = 0
-			end
-			shell.growTimer = shell.growTimer + (dt/2)*(growSpeed/50)
-			shell.maxDist = math.min(maxDistance, shell.maxDist + (dt*2)*(growSpeed/50))
-			shell.gravStrength = math.min(maxStrength, shell.gravStrength + (dt/7)*(growSpeed/50))
-			shell.maxMass = math.min(maxMass, shell.maxMass + (dt*2000)*(growSpeed/50))
-			fuseTimer = math.floor(shell.fuseTimer)
-			BlackHole(shell)
-			SpawnParticle("darksmoke", shell.pos, Vec(0, 0, 0), math.min(1*shell.growTimer, 3), 0.2)
-
-			if breakStuff then
-				breakTimer = breakTimer + dt
-				local t = math.mod(breakTimer, 1.0)
-				if t < 0.5 then
-					MakeHole(shell.pos, deleteRadius, deleteRadius, deleteRadius)
-				end
-			end
-		end
-	end
-end
-
-function draw()
-	if optionsOpen then
-		UiMakeInteractive()
-		UiTranslate(20, UiMiddle()-200)
-		UiAlign("top left")
-		UiColor(0,0,0,0.75)
-		UiImageBox("ui/common/box-solid-6.png", 650, 650, 6, 6)
-		UiTranslate(300, 40)
-		UiColor(1, 1, 1)
-		UiFont("regular.ttf", 26)
-		UiAlign("center middle")
-		UiPush()
-			UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-			if UiTextButton("Default", 100, 40) then
-				SetFloat("savegame.mod.maxdist", 75)
-				SetFloat("savegame.mod.maxstr", 1)
-				SetFloat("savegame.mod.maxmass", 50000)
-				SetFloat("savegame.mod.maxtime", 300)
-				SetFloat("savegame.mod.growspeed", 150)
-				SetBool("savegame.mod.deletesmall", true)
-				SetFloat("savegame.mod.deletemass", 25)
-				SetFloat("savegame.mod.deletedist", 3)
-				maxDistance = 75
-				maxStrength = 1
-				maxMass = 15000
-				fuseTime = 60
-				growSpeed = 75
-				deleteMass = 50
-				deleteRadius = 3
-				breakStuff = false
-				deleteSmall = true
-			end
-		UiPop()
-
-		UiPush()
-			UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-			UiTranslate(100, 0)
-			if UiTextButton("Close", 80, 40) then
-				optionsOpen = false
-			end
-		UiPop()
-
-		UiTranslate(-150, 50)
-		UiPush()
-			UiText("Max Pull Distance")
-			UiAlign("right")
-			UiTranslate(330, 10)
-			maxDistance, done = optionsSlider(maxDistance, 1, 500)
-			UiTranslate(40, 0)
-			UiAlign("left")
-			UiColor(0.7, 0.6, 0.1)
-			UiText(maxDistance.."m")
-			SetFloat("savegame.mod.maxdist", maxDistance)
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Max Pull Strength")
-			UiAlign("right")
-			UiTranslate(330, 10)
-			maxStrength, done = optionsSlider(maxStrength, 0.1, 300)
-			UiTranslate(40, 0)
-			UiAlign("left")
-			UiColor(0.7, 0.6, 0.1)
-			UiText(maxStrength)
-			SetFloat("savegame.mod.maxstr", maxStrength)
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Max Pull Mass")
-			UiAlign("right")
-			UiTranslate(330, 10)
-			maxMass, done = optionsSlider(maxMass, 100, 100000)
-			UiTranslate(-210, 0)
-			if UiTextButton("-", 10, 10) then
-				maxMass = math.max(100, maxMass - 5)
-			end
-			UiTranslate(240, 0)
-			if UiTextButton("+", 10, 10) then
-				maxMass = math.min(100000, maxMass + 5)
-			end
-			UiAlign("left")
-			UiTranslate(10, 0)
-			UiColor(0.7, 0.6, 0.1)
-			UiText(maxMass)
-			SetFloat("savegame.mod.maxmass", maxMass)
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Black Hole Life Timer")
-			UiAlign("right")
-			UiTranslate(330, 10)
-			fuseTime, done = optionsSlider(fuseTime, 5, 1800)
-			UiTranslate(40, 0)
-			UiAlign("left")
-			UiColor(0.7, 0.6, 0.1)
-			UiText(fuseTime.."s")
-			SetFloat("savegame.mod.maxtime", fuseTime)
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Black Hole Grow Speed")
-			UiAlign("right")
-			UiTranslate(330, 10)
-			growSpeed, done = optionsSlider(growSpeed, 5, 500)
-			UiTranslate(40, 0)
-			UiAlign("left")
-			UiColor(0.7, 0.6, 0.1)
-			UiText(growSpeed)
-			SetFloat("savegame.mod.growspeed", growSpeed)
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Break Stuff in Center")
-			UiTranslate(180, 5)
-			UiAlign("right")
-			UiColor(0.5, 0.8, 1)
-			if breakStuff then
-				if UiTextButton("Yes", 20, 20) then
-					breakStuff = false
-					SetBool("savegame.mod.breakstuff", breakStuff)
-				end
-			else
-				if UiTextButton("No", 20, 20) then
-					breakStuff = true
-					SetBool("savegame.mod.breakstuff", breakStuff)
-				end
-			end
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Delete Objects in Center")
-			UiTranslate(180, 0)
-			UiAlign("right")
-			UiColor(0.5, 0.8, 1)
-			if deleteSmall then
-				if UiTextButton("Yes", 20, 20) then
-					deleteSmall = false
-					SetBool("savegame.mod.deletesmall", deleteSmall)
-				end
-			else
-				if UiTextButton("No", 20, 20) then
-					deleteSmall = true
-					SetBool("savegame.mod.deletesmall", deleteSmall)
-				end
-			end
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Max Mass to Delete")
-			UiAlign("right")
-			UiTranslate(330, 5)
-			deleteMass, done = optionsSlider(deleteMass, 5, 100000)
-			UiTranslate(-210, 0)
-			if UiTextButton("-", 10, 10) then
-				deleteMass = math.max(5, deleteMass - 5)
-			end
-			UiTranslate(240, 0)
-			if UiTextButton("+", 10, 10) then
-				deleteMass = math.min(100000, deleteMass + 5)
-			end
-			UiAlign("left")
-			UiTranslate(10, 0)
-			UiColor(0.7, 0.6, 0.1)
-			UiText(deleteMass)
-			SetFloat("savegame.mod.deletemass", deleteMass)
-		UiPop()
-
-		UiTranslate(0, 60)
-		UiPush()
-			UiText("Delete Distance")
-			UiAlign("right")
-			UiTranslate(330, 10)
-			deleteRadius, done = optionsSlider(deleteRadius, 1, 50)
-			UiTranslate(40, 0)
-			UiAlign("left")
-			UiColor(0.7, 0.6, 0.1)
-			UiText(deleteRadius.."m")
-			SetFloat("savegame.mod.deletedist", deleteRadius)
-		UiPop()
 	end
 end
 
@@ -449,4 +149,291 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    RegisterTool("blackhole", "Black Hole", "MOD/vox/blackhole.vox")
+    SetBool("game.tool.blackhole.enabled", true, true)
+    SetFloat("game.tool.blackhole.ammo", 101, true)
+    maxDistance = GetFloat("savegame.mod.maxdist")
+    maxStrength = GetFloat("savegame.mod.maxstr")
+    maxMass = GetFloat("savegame.mod.maxmass")
+    fuseTime = GetFloat("savegame.mod.maxtime")
+    growSpeed = GetFloat("savegame.mod.growspeed")
+    breakStuff = GetBool("savegame.mod.breakstuff")
+    deleteMass = GetFloat("savegame.mod.deletemass")
+    deleteSmall = GetBool("savegame.mod.deletesmall")
+    deleteRadius = GetFloat("savegame.mod.deletedist")
+    optionsOpen = false
+    if not HasKey("savegame.mod.maxdist") then
+    	maxDistance = 75
+    	maxStrength = 1
+    	maxMass = 15000
+    	fuseTime = 60
+    	growSpeed = 75
+    	deleteMass = 50
+    	deleteRadius = 3
+    end
+    gravity = Vec(0, 0, 0)
+    velocity = 0.1
+    angle = 10
+    for i=1, 5 do
+    	blackholeprojectileHandler.shells[i] = deepcopy(blackholeprojectileHandler.defaultShell)
+    end
+    fuseTimer = 0
+    shootTimer = 0
+    breakTimer = 0
+end
+
+function client.init()
+    throwsound = LoadSound("MOD/snd/throw2.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "blackhole" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") and not optionsOpen then
+    		Shoot()
+    	end
+
+    	if InputPressed("O") then optionsOpen = not optionsOpen end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		angle = angle + math.random(2, 10)
+    		local t = Transform()
+    		t.pos = Vec(0.3, -0.4, -0.7)
+    		t.rot = QuatEuler(angle, angle/3, angle/2)
+    		SetToolTransform(t)
+
+    		local p = TransformToParentPoint(GetBodyTransform(b), Vec(0, 0, -2))
+    		PointLight(p, 0, 0, 0, 0.5)
+    	end
+    end
+
+    for key, shell in ipairs(blackholeprojectileHandler.shells) do
+    	if shell.active then
+    		BlackholeOperations(shell)
+    		shell.growTimer = shell.growTimer + (dt/2)*(growSpeed/50)
+    	end
+
+    	if shell.fuseTimer ~= 0 then
+    		shell.fuseTimer = shell.fuseTimer - dt
+    		if shell.fuseTimer < 0.01 then
+    			shell.fuseTimer = 0
+    			shell.growTimer = 0
+    		end
+    		if InputPressed("c") then
+    			BlackHolePush(shell)
+    			shell.fuseTimer = 0
+    			shell.growTimer = 0
+    		end
+    		shell.growTimer = shell.growTimer + (dt/2)*(growSpeed/50)
+    		shell.maxDist = math.min(maxDistance, shell.maxDist + (dt*2)*(growSpeed/50))
+    		shell.gravStrength = math.min(maxStrength, shell.gravStrength + (dt/7)*(growSpeed/50))
+    		shell.maxMass = math.min(maxMass, shell.maxMass + (dt*2000)*(growSpeed/50))
+    		fuseTimer = math.floor(shell.fuseTimer)
+    		BlackHole(shell)
+    		SpawnParticle("darksmoke", shell.pos, Vec(0, 0, 0), math.min(1*shell.growTimer, 3), 0.2)
+
+    		if breakStuff then
+    			breakTimer = breakTimer + dt
+    			local t = math.mod(breakTimer, 1.0)
+    			if t < 0.5 then
+    				MakeHole(shell.pos, deleteRadius, deleteRadius, deleteRadius)
+    			end
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    if optionsOpen then
+    	UiMakeInteractive()
+    	UiTranslate(20, UiMiddle()-200)
+    	UiAlign("top left")
+    	UiColor(0,0,0,0.75)
+    	UiImageBox("ui/common/box-solid-6.png", 650, 650, 6, 6)
+    	UiTranslate(300, 40)
+    	UiColor(1, 1, 1)
+    	UiFont("regular.ttf", 26)
+    	UiAlign("center middle")
+    	UiPush()
+    		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    		if UiTextButton("Default", 100, 40) then
+    			SetFloat("savegame.mod.maxdist", 75, true)
+    			SetFloat("savegame.mod.maxstr", 1, true)
+    			SetFloat("savegame.mod.maxmass", 50000, true)
+    			SetFloat("savegame.mod.maxtime", 300, true)
+    			SetFloat("savegame.mod.growspeed", 150, true)
+    			SetBool("savegame.mod.deletesmall", true, true)
+    			SetFloat("savegame.mod.deletemass", 25, true)
+    			SetFloat("savegame.mod.deletedist", 3, true)
+    			maxDistance = 75
+    			maxStrength = 1
+    			maxMass = 15000
+    			fuseTime = 60
+    			growSpeed = 75
+    			deleteMass = 50
+    			deleteRadius = 3
+    			breakStuff = false
+    			deleteSmall = true
+    		end
+    	UiPop()
+
+    	UiPush()
+    		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    		UiTranslate(100, 0)
+    		if UiTextButton("Close", 80, 40) then
+    			optionsOpen = false
+    		end
+    	UiPop()
+
+    	UiTranslate(-150, 50)
+    	UiPush()
+    		UiText("Max Pull Distance")
+    		UiAlign("right")
+    		UiTranslate(330, 10)
+    		maxDistance, done = optionsSlider(maxDistance, 1, 500)
+    		UiTranslate(40, 0)
+    		UiAlign("left")
+    		UiColor(0.7, 0.6, 0.1)
+    		UiText(maxDistance.."m")
+    		SetFloat("savegame.mod.maxdist", maxDistance, true)
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Max Pull Strength")
+    		UiAlign("right")
+    		UiTranslate(330, 10)
+    		maxStrength, done = optionsSlider(maxStrength, 0.1, 300)
+    		UiTranslate(40, 0)
+    		UiAlign("left")
+    		UiColor(0.7, 0.6, 0.1)
+    		UiText(maxStrength)
+    		SetFloat("savegame.mod.maxstr", maxStrength, true)
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Max Pull Mass")
+    		UiAlign("right")
+    		UiTranslate(330, 10)
+    		maxMass, done = optionsSlider(maxMass, 100, 100000)
+    		UiTranslate(-210, 0)
+    		if UiTextButton("-", 10, 10) then
+    			maxMass = math.max(100, maxMass - 5)
+    		end
+    		UiTranslate(240, 0)
+    		if UiTextButton("+", 10, 10) then
+    			maxMass = math.min(100000, maxMass + 5)
+    		end
+    		UiAlign("left")
+    		UiTranslate(10, 0)
+    		UiColor(0.7, 0.6, 0.1)
+    		UiText(maxMass)
+    		SetFloat("savegame.mod.maxmass", maxMass, true)
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Black Hole Life Timer")
+    		UiAlign("right")
+    		UiTranslate(330, 10)
+    		fuseTime, done = optionsSlider(fuseTime, 5, 1800)
+    		UiTranslate(40, 0)
+    		UiAlign("left")
+    		UiColor(0.7, 0.6, 0.1)
+    		UiText(fuseTime.."s")
+    		SetFloat("savegame.mod.maxtime", fuseTime, true)
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Black Hole Grow Speed")
+    		UiAlign("right")
+    		UiTranslate(330, 10)
+    		growSpeed, done = optionsSlider(growSpeed, 5, 500)
+    		UiTranslate(40, 0)
+    		UiAlign("left")
+    		UiColor(0.7, 0.6, 0.1)
+    		UiText(growSpeed)
+    		SetFloat("savegame.mod.growspeed", growSpeed, true)
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Break Stuff in Center")
+    		UiTranslate(180, 5)
+    		UiAlign("right")
+    		UiColor(0.5, 0.8, 1)
+    		if breakStuff then
+    			if UiTextButton("Yes", 20, 20) then
+    				breakStuff = false
+    				SetBool("savegame.mod.breakstuff", breakStuff, true)
+    			end
+    		else
+    			if UiTextButton("No", 20, 20) then
+    				breakStuff = true
+    				SetBool("savegame.mod.breakstuff", breakStuff, true)
+    			end
+    		end
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Delete Objects in Center")
+    		UiTranslate(180, 0)
+    		UiAlign("right")
+    		UiColor(0.5, 0.8, 1)
+    		if deleteSmall then
+    			if UiTextButton("Yes", 20, 20) then
+    				deleteSmall = false
+    				SetBool("savegame.mod.deletesmall", deleteSmall, true)
+    			end
+    		else
+    			if UiTextButton("No", 20, 20) then
+    				deleteSmall = true
+    				SetBool("savegame.mod.deletesmall", deleteSmall, true)
+    			end
+    		end
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Max Mass to Delete")
+    		UiAlign("right")
+    		UiTranslate(330, 5)
+    		deleteMass, done = optionsSlider(deleteMass, 5, 100000)
+    		UiTranslate(-210, 0)
+    		if UiTextButton("-", 10, 10) then
+    			deleteMass = math.max(5, deleteMass - 5)
+    		end
+    		UiTranslate(240, 0)
+    		if UiTextButton("+", 10, 10) then
+    			deleteMass = math.min(100000, deleteMass + 5)
+    		end
+    		UiAlign("left")
+    		UiTranslate(10, 0)
+    		UiColor(0.7, 0.6, 0.1)
+    		UiText(deleteMass)
+    		SetFloat("savegame.mod.deletemass", deleteMass, true)
+    	UiPop()
+
+    	UiTranslate(0, 60)
+    	UiPush()
+    		UiText("Delete Distance")
+    		UiAlign("right")
+    		UiTranslate(330, 10)
+    		deleteRadius, done = optionsSlider(deleteRadius, 1, 50)
+    		UiTranslate(40, 0)
+    		UiAlign("left")
+    		UiColor(0.7, 0.6, 0.1)
+    		UiText(deleteRadius.."m")
+    		SetFloat("savegame.mod.deletedist", deleteRadius, true)
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
@@ -1,219 +1,4 @@
-function init()
-	bMaxDist = GetFloat("savegame.mod.maxdist")
-	bMaxStr = GetFloat("savegame.mod.maxstr")
-	bMaxMass = GetFloat("savegame.mod.maxmass")
-	bMaxTime = GetFloat("savegame.mod.maxtime")
-	bGrowSpeed = GetFloat("savegame.mod.growspeed")
-	bBreakStuff = GetBool("savegame.mod.breakstuff")
-	bDeleteSmall = GetBool("savegame.mod.deletesmall")
-	bDeleteMass = GetFloat("savegame.mod.deletemass")
-	bDeleteDist = GetFloat("savegame.mod.deletedist")
-	if not HasKey("savegame.mod.maxdist") then
-		maxDistance = 75
-		maxStrength = 1
-		maxMass = 15000
-		fuseTime = 60
-		growSpeed = 75
-		deleteMass = 50
-		deleteRadius = 3
-	end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 50)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Black Hole")
-	UiTranslate(0, 50)
-	UiFont("regular.ttf", 26)
-	UiText("The Black Hole will grow over time, here you can set the max values it will grow")
-	UiTranslate(0, 30)
-	UiColor(1, 1, 0.2)
-	UiText("Higher than default values will probably make it lag alot")
-	UiTranslate(0, 30)
-	UiText("You can cancel black holes any time by pressing 'C'")
-	UiColor(1, 1, 1)
-	UiTranslate(0, 30)
-
-	UiText("Reset to default (Recommended settings)")
-	UiTranslate(0, 40)
-	UiPush()
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-		if UiTextButton("Default", 100, 40) then
-			SetFloat("savegame.mod.maxdist", 75)
-			SetFloat("savegame.mod.maxstr", 1)
-			SetFloat("savegame.mod.maxmass", 50000)
-			SetFloat("savegame.mod.maxtime", 300)
-			SetFloat("savegame.mod.growspeed", 150)
-			SetBool("savegame.mod.deletesmall", true)
-			SetFloat("savegame.mod.deletemass", 25)
-			SetFloat("savegame.mod.deletedist", 3)
-			bMaxDist = 75
-			bMaxStr = 1
-			bMaxMass = 50000
-			bMaxTime = 300
-			bGrowSpeed = 150
-			bDeleteMass = 25
-			bBreakStuff = false
-			bDeleteSmall = true
-			bDeleteDist = 3
-		end
-	UiPop()
-
-	UiTranslate(-150, 80)
-	UiPush()
-		UiText("Max Pull Distance")
-		UiAlign("right")
-		UiTranslate(330, 10)
-		bMaxDist, done = optionsSlider(bMaxDist, 1, 500)
-		UiTranslate(40, 0)
-		UiAlign("left")
-		UiColor(0.7, 0.6, 0.1)
-		UiText(bMaxDist.."m")
-		SetFloat("savegame.mod.maxdist", bMaxDist)
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Max Pull Strength")
-		UiAlign("right")
-		UiTranslate(330, 10)
-		bMaxStr, done = optionsSlider(bMaxStr, 0.1, 300)
-		UiTranslate(40, 0)
-		UiAlign("left")
-		UiColor(0.7, 0.6, 0.1)
-		UiText(bMaxStr)
-		SetFloat("savegame.mod.maxstr", bMaxStr)
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Max Pull Mass")
-		UiAlign("right")
-		UiTranslate(330, 10)
-		bMaxMass, done = optionsSlider(bMaxMass, 100, 100000)
-		UiTranslate(-210, 0)
-		if UiTextButton("-", 10, 10) then
-			bMaxMass = math.max(100, bMaxMass - 5)
-		end
-		UiTranslate(240, 0)
-		if UiTextButton("+", 10, 10) then
-			bMaxMass = math.min(100000, bMaxMass + 5)
-		end
-		UiAlign("left")
-		UiTranslate(10, 0)
-		UiColor(0.7, 0.6, 0.1)
-		UiText(bMaxMass)
-		SetFloat("savegame.mod.maxmass", bMaxMass)
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Black Hole Life Timer")
-		UiAlign("right")
-		UiTranslate(330, 10)
-		bMaxTime, done = optionsSlider(bMaxTime, 5, 1800)
-		UiTranslate(40, 0)
-		UiAlign("left")
-		UiColor(0.7, 0.6, 0.1)
-		UiText(bMaxTime.."s")
-		SetFloat("savegame.mod.maxtime", bMaxTime)
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Black Hole Grow Speed")
-		UiAlign("right")
-		UiTranslate(330, 10)
-		bGrowSpeed, done = optionsSlider(bGrowSpeed, 5, 500)
-		UiTranslate(40, 0)
-		UiAlign("left")
-		UiColor(0.7, 0.6, 0.1)
-		UiText(bGrowSpeed)
-		SetFloat("savegame.mod.growspeed", bGrowSpeed)
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Break Stuff in Center")
-		UiTranslate(180, 5)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if bBreakStuff then
-			if UiTextButton("Yes", 20, 20) then
-				bBreakStuff = false
-				SetBool("savegame.mod.breakstuff", bBreakStuff)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				bBreakStuff = true
-				SetBool("savegame.mod.breakstuff", bBreakStuff)
-			end
-		end
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Delete Objects in Center")
-		UiTranslate(180, 0)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if bDeleteSmall then
-			if UiTextButton("Yes", 20, 20) then
-				bDeleteSmall = false
-				SetBool("savegame.mod.deletesmall", bDeleteSmall)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				bDeleteSmall = true
-				SetBool("savegame.mod.deletesmall", bDeleteSmall)
-			end
-		end
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Max Mass to Delete")
-		UiAlign("right")
-		UiTranslate(330, 5)
-		bDeleteMass, done = optionsSlider(bDeleteMass, 5, 100000)
-		UiTranslate(-210, 0)
-		if UiTextButton("-", 10, 10) then
-			bDeleteMass = math.max(5, bDeleteMass - 5)
-		end
-		UiTranslate(240, 0)
-		if UiTextButton("+", 10, 10) then
-			bDeleteMass = math.min(100000, bDeleteMass + 5)
-		end
-		UiAlign("left")
-		UiTranslate(10, 0)
-		UiColor(0.7, 0.6, 0.1)
-		UiText(bDeleteMass)
-		SetFloat("savegame.mod.deletemass", bDeleteMass)
-	UiPop()
-
-	UiTranslate(0, 60)
-	UiPush()
-		UiText("Delete Distance")
-		UiAlign("right")
-		UiTranslate(330, 10)
-		bDeleteDist, done = optionsSlider(bDeleteDist, 1, 50)
-		UiTranslate(40, 0)
-		UiAlign("left")
-		UiColor(0.7, 0.6, 0.1)
-		UiText(bDeleteDist.."m")
-		SetFloat("savegame.mod.deletedist", bDeleteDist)
-	UiPop()
-
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(130, 100)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -233,4 +18,221 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    bMaxDist = GetFloat("savegame.mod.maxdist")
+    bMaxStr = GetFloat("savegame.mod.maxstr")
+    bMaxMass = GetFloat("savegame.mod.maxmass")
+    bMaxTime = GetFloat("savegame.mod.maxtime")
+    bGrowSpeed = GetFloat("savegame.mod.growspeed")
+    bBreakStuff = GetBool("savegame.mod.breakstuff")
+    bDeleteSmall = GetBool("savegame.mod.deletesmall")
+    bDeleteMass = GetFloat("savegame.mod.deletemass")
+    bDeleteDist = GetFloat("savegame.mod.deletedist")
+    if not HasKey("savegame.mod.maxdist") then
+    	maxDistance = 75
+    	maxStrength = 1
+    	maxMass = 15000
+    	fuseTime = 60
+    	growSpeed = 75
+    	deleteMass = 50
+    	deleteRadius = 3
+    end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 50)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Black Hole")
+    UiTranslate(0, 50)
+    UiFont("regular.ttf", 26)
+    UiText("The Black Hole will grow over time, here you can set the max values it will grow")
+    UiTranslate(0, 30)
+    UiColor(1, 1, 0.2)
+    UiText("Higher than default values will probably make it lag alot")
+    UiTranslate(0, 30)
+    UiText("You can cancel black holes any time by pressing 'C'")
+    UiColor(1, 1, 1)
+    UiTranslate(0, 30)
+
+    UiText("Reset to default (Recommended settings)")
+    UiTranslate(0, 40)
+    UiPush()
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    	if UiTextButton("Default", 100, 40) then
+    		SetFloat("savegame.mod.maxdist", 75, true)
+    		SetFloat("savegame.mod.maxstr", 1, true)
+    		SetFloat("savegame.mod.maxmass", 50000, true)
+    		SetFloat("savegame.mod.maxtime", 300, true)
+    		SetFloat("savegame.mod.growspeed", 150, true)
+    		SetBool("savegame.mod.deletesmall", true, true)
+    		SetFloat("savegame.mod.deletemass", 25, true)
+    		SetFloat("savegame.mod.deletedist", 3, true)
+    		bMaxDist = 75
+    		bMaxStr = 1
+    		bMaxMass = 50000
+    		bMaxTime = 300
+    		bGrowSpeed = 150
+    		bDeleteMass = 25
+    		bBreakStuff = false
+    		bDeleteSmall = true
+    		bDeleteDist = 3
+    	end
+    UiPop()
+
+    UiTranslate(-150, 80)
+    UiPush()
+    	UiText("Max Pull Distance")
+    	UiAlign("right")
+    	UiTranslate(330, 10)
+    	bMaxDist, done = optionsSlider(bMaxDist, 1, 500)
+    	UiTranslate(40, 0)
+    	UiAlign("left")
+    	UiColor(0.7, 0.6, 0.1)
+    	UiText(bMaxDist.."m")
+    	SetFloat("savegame.mod.maxdist", bMaxDist, true)
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Max Pull Strength")
+    	UiAlign("right")
+    	UiTranslate(330, 10)
+    	bMaxStr, done = optionsSlider(bMaxStr, 0.1, 300)
+    	UiTranslate(40, 0)
+    	UiAlign("left")
+    	UiColor(0.7, 0.6, 0.1)
+    	UiText(bMaxStr)
+    	SetFloat("savegame.mod.maxstr", bMaxStr, true)
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Max Pull Mass")
+    	UiAlign("right")
+    	UiTranslate(330, 10)
+    	bMaxMass, done = optionsSlider(bMaxMass, 100, 100000)
+    	UiTranslate(-210, 0)
+    	if UiTextButton("-", 10, 10) then
+    		bMaxMass = math.max(100, bMaxMass - 5)
+    	end
+    	UiTranslate(240, 0)
+    	if UiTextButton("+", 10, 10) then
+    		bMaxMass = math.min(100000, bMaxMass + 5)
+    	end
+    	UiAlign("left")
+    	UiTranslate(10, 0)
+    	UiColor(0.7, 0.6, 0.1)
+    	UiText(bMaxMass)
+    	SetFloat("savegame.mod.maxmass", bMaxMass, true)
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Black Hole Life Timer")
+    	UiAlign("right")
+    	UiTranslate(330, 10)
+    	bMaxTime, done = optionsSlider(bMaxTime, 5, 1800)
+    	UiTranslate(40, 0)
+    	UiAlign("left")
+    	UiColor(0.7, 0.6, 0.1)
+    	UiText(bMaxTime.."s")
+    	SetFloat("savegame.mod.maxtime", bMaxTime, true)
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Black Hole Grow Speed")
+    	UiAlign("right")
+    	UiTranslate(330, 10)
+    	bGrowSpeed, done = optionsSlider(bGrowSpeed, 5, 500)
+    	UiTranslate(40, 0)
+    	UiAlign("left")
+    	UiColor(0.7, 0.6, 0.1)
+    	UiText(bGrowSpeed)
+    	SetFloat("savegame.mod.growspeed", bGrowSpeed, true)
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Break Stuff in Center")
+    	UiTranslate(180, 5)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if bBreakStuff then
+    		if UiTextButton("Yes", 20, 20) then
+    			bBreakStuff = false
+    			SetBool("savegame.mod.breakstuff", bBreakStuff, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			bBreakStuff = true
+    			SetBool("savegame.mod.breakstuff", bBreakStuff, true)
+    		end
+    	end
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Delete Objects in Center")
+    	UiTranslate(180, 0)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if bDeleteSmall then
+    		if UiTextButton("Yes", 20, 20) then
+    			bDeleteSmall = false
+    			SetBool("savegame.mod.deletesmall", bDeleteSmall, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			bDeleteSmall = true
+    			SetBool("savegame.mod.deletesmall", bDeleteSmall, true)
+    		end
+    	end
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Max Mass to Delete")
+    	UiAlign("right")
+    	UiTranslate(330, 5)
+    	bDeleteMass, done = optionsSlider(bDeleteMass, 5, 100000)
+    	UiTranslate(-210, 0)
+    	if UiTextButton("-", 10, 10) then
+    		bDeleteMass = math.max(5, bDeleteMass - 5)
+    	end
+    	UiTranslate(240, 0)
+    	if UiTextButton("+", 10, 10) then
+    		bDeleteMass = math.min(100000, bDeleteMass + 5)
+    	end
+    	UiAlign("left")
+    	UiTranslate(10, 0)
+    	UiColor(0.7, 0.6, 0.1)
+    	UiText(bDeleteMass)
+    	SetFloat("savegame.mod.deletemass", bDeleteMass, true)
+    UiPop()
+
+    UiTranslate(0, 60)
+    UiPush()
+    	UiText("Delete Distance")
+    	UiAlign("right")
+    	UiTranslate(330, 10)
+    	bDeleteDist, done = optionsSlider(bDeleteDist, 1, 50)
+    	UiTranslate(40, 0)
+    	UiAlign("left")
+    	UiColor(0.7, 0.6, 0.1)
+    	UiText(bDeleteDist.."m")
+    	SetFloat("savegame.mod.deletedist", bDeleteDist, true)
+    UiPop()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(130, 100)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```
