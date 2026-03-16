# Migration Report: main\BillBoards\images\nothing to see here\easteregg.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\BillBoards\images\nothing to see here\easteregg.lua
+++ patched/main\BillBoards\images\nothing to see here\easteregg.lua
@@ -1,5 +1,7 @@
-function draw()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("MOD/main/BillBoards/images/nothing to see here/hugh.jpg")
-end+#version 2
+function client.draw()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("MOD/main/BillBoards/images/nothing to see here/hugh.jpg")
+end
+

```

---

# Migration Report: main\BillBoards\scripts\HW_1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\BillBoards\scripts\HW_1.lua
+++ patched/main\BillBoards\scripts\HW_1.lua
@@ -1,5 +1,7 @@
-function draw()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("MOD/main/BillBoards/images/HW_1.jpg")
-end+#version 2
+function client.draw()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("MOD/main/BillBoards/images/HW_1.jpg")
+end
+

```

---

# Migration Report: main\BillBoards\scripts\HW_2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\BillBoards\scripts\HW_2.lua
+++ patched/main\BillBoards\scripts\HW_2.lua
@@ -1,5 +1,7 @@
-function draw()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("MOD/main/BillBoards/images/HW_2.jpg")
-end+#version 2
+function client.draw()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("MOD/main/BillBoards/images/HW_2.jpg")
+end
+

```

---

# Migration Report: main\BillBoards\scripts\HW_3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\BillBoards\scripts\HW_3.lua
+++ patched/main\BillBoards\scripts\HW_3.lua
@@ -1,5 +1,7 @@
-function draw()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("MOD/main/BillBoards/images/HW_3.jpg")
-end+#version 2
+function client.draw()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("MOD/main/BillBoards/images/HW_3.jpg")
+end
+

```

---

# Migration Report: main\BillBoards\scripts\HW_4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\BillBoards\scripts\HW_4.lua
+++ patched/main\BillBoards\scripts\HW_4.lua
@@ -1,5 +1,7 @@
-function draw()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("MOD/main/BillBoards/images/HW_4.jpg")
-end+#version 2
+function client.draw()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("MOD/main/BillBoards/images/HW_4.jpg")
+end
+

```

---

# Migration Report: main\plane\plane.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\plane\plane.lua
+++ patched/main\plane\plane.lua
@@ -1,60 +1,53 @@
-function init()
-	LR = FindLight("LR")
-	LG = FindLight("LG")
-	LW = FindLight("LW")
-
-	Plane = FindShape("plane")
-
-	windows = FindShapes("window")
-	shield = FindShape("shield")
-
-	Snd = LoadLoop("MOD/main/plane/plane.ogg")
-	boom = LoadSound("MOD/main/plane/boom.ogg")
-
-	time = 0
-
-	--broken = false
-
-	played = false
+#version 2
+function server.init()
+    LR = FindLight("LR")
+    LG = FindLight("LG")
+    LW = FindLight("LW")
+    Plane = FindShape("plane")
+    windows = FindShapes("window")
+    shield = FindShape("shield")
+    Snd = LoadLoop("MOD/main/plane/plane.ogg")
+    time = 0
+    --broken = false
+    played = false
 end
 
-function tick(dt)
-	
-	time = time + dt
+function server.tick(dt)
+    time = time + dt
+    PlaneT = GetShapeWorldTransform(Plane)
+    --if broken == false then
+    	--PlayLoop(Snd, PlaneT.pos, 0.25)
+    --end
+    if time < 0.1 then
+    	SetLightEnabled(LR, true)
+    	SetLightEnabled(LG, true)
+    	SetLightEnabled(LW, true)
+    end
+    if time > 0.1 and time < 1 then
+    	SetLightEnabled(LR, false)
+    	SetLightEnabled(LG, false)
+    	SetLightEnabled(LW, false)
+    end
+    if time > 1 then
+    	time = 0
+    end
+end
 
-	PlaneT = GetShapeWorldTransform(Plane)
-	
-	--if broken == false then
-		--PlayLoop(Snd, PlaneT.pos, 0.25)
-	--end
+function client.init()
+    boom = LoadSound("MOD/main/plane/boom.ogg")
+end
 
-	if IsShapeBroken(Plane) == true then
-		--broken = true
-		if played == false then
-			PlaySound(boom)
-			played = true
-		end
-		SetShapeEmissiveScale(shield, 0)
-		for i=1, #windows do
-			Delete(windows[i])
-		end
-	end
+function client.tick(dt)
+    if IsShapeBroken(Plane) == true then
+    	--broken = true
+    	if played == false then
+    		PlaySound(boom)
+    		played = true
+    	end
+    	SetShapeEmissiveScale(shield, 0)
+    	for i=1, #windows do
+    		Delete(windows[i])
+    	end
+    end
+end
 
-	if time < 0.1 then
-		SetLightEnabled(LR, true)
-		SetLightEnabled(LG, true)
-		SetLightEnabled(LW, true)
-	end
-	if time > 0.1 and time < 1 then
-		SetLightEnabled(LR, false)
-		SetLightEnabled(LG, false)
-		SetLightEnabled(LW, false)
-	end
-	if time > 1 then
-		time = 0
-	end
-
-	--DebugWatch("time", time)
-	--DebugWatch("on", IsLightActive(LR))
-	--DebugWatch("plane_pos", GetShapeWorldTransform("plane").pos)
-end
```

---

# Migration Report: main\plane\plane_travel.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\plane\plane_travel.lua
+++ patched/main\plane\plane_travel.lua
@@ -1,127 +1,4 @@
-function init()
-
-	Pos1A = FindLocation("1A")
-	Pos2A = FindLocation("2A")
-
-	Pos1B = FindLocation("1B")
-	Pos2B = FindLocation("2B")
-
-	Snd = LoadLoop("MOD/main/plane/plane.ogg")
-
-	broken = false
-
-	canbreak = true
-
-	spawnTable = {
-		"MOD/main/plane/prefabs/Blue_plane.xml",
-		"MOD/main/plane/prefabs/Grey_plane.xml",
-		"MOD/main/plane/prefabs/Red_plane.xml"
-	}
-
-	pick = true
-
-	explode = true
-
-	flythroughs_last = 0
-	flythroughs = 1
-
-	FireTime = 0
-
-end
-
-function tick(dt)
-
-	PlaneBody = FindBody("PB")
-	PlaneShape = FindShape("plane")
-
-	PlaneBodyT = GetBodyTransform(PlaneBody)
-	PlaneShapeT = GetShapeWorldTransform(PlaneShape)
-
-	Pos1TA = GetLocationTransform(Pos1A)
-	Pos2TA = GetLocationTransform(Pos2A)
-
-	Pos1TB = GetLocationTransform(Pos1B)
-	Pos2TB = GetLocationTransform(Pos2B)
-
-	if pick == true then
-		randomSpawnIndex = math.random(1, 3)
-		randomRouteIndex = math.random(1, 2)
-		pick = false
-	end
-
-	if broken == false and IsHandleValid(PlaneBody) == true then
-		trail()
-		PlayLoop(Snd, PlaneBodyT.pos, 0.25)
-		SetBodyDynamic(PlaneBody, false)
-	end
-
-
-	if canbreak == false then
-		broken = false
-		canbreak = true
-	end
-
-	if pick == false then
-		if randomRouteIndex == 1 then
-			travel1()
-		end
-
-		if randomRouteIndex == 2 then
-			travel2()
-		end
-	end
-
-	if canbreak == true then
-		if IsShapeBroken(PlaneShape) == true then
-			broken = true
-			canbreak = false
-			SetBodyDynamic(PlaneBody, true)
-
-			SetBodyAngularVelocity(PlaneBody, Vec(0, 0, 5))
-			ApplyBodyImpulse(PlaneBody, PlaneBodyT.pos, QuatRotateVec(PlaneBodyT.rot, Vec(0, 0, -600)))
-
-			QueryRejectBody(PlaneBody)
-			QueryRejectShape(PlaneShape)
-
-			local hit, point, normal, shape = QueryClosestPoint(PlaneShapeT.pos, 0.7)
-
-			--DebugCross(point, 1, 0, 0, 1)
-			--DebugWatch('hitpoint', point)
-
-			if hit == true and GetShapeVoxelCount(shape) > 100 and explode == true then
-				Explosion(PlaneShapeT.pos, 1)
-				explode = false
-			end
-
-			RemoveTag(PlaneBody, "PB")
-			pick = true
-			smoke()
-
-
-			FireTime = FireTime + dt
-			if FireTime > 5 then
-				RemoveTag(PlaneShape, "plane")
-				explode = true
-				FireTime = 0
-			end
-		end
-	end
-
-	--DebugCross(point, 1, 0, 0, 1)
-	--DebugWatch('hitpoint', point)
-	--DebugWatch('explode', explode)
-	--DebugWatch("PlanePos", GetBodyTransform(PlaneBody))
-	--DebugWatch("pick", pick)
-	--DebugWatch("randomRouteIndex", randomRouteIndex)
-	--DebugWatch("randomSpawnIndex", randomSpawnIndex)
-	--DebugWatch("PlaneActualPos", PlaneBodyT.pos)
-	--DebugWatch("validEntity", IsHandleValid(PlaneBody))
-	--DebugWatch("broken", broken)
-	--DebugWatch("canbreak", canbreak)
-	--DebugWatch("IsShapeBroken(PlaneShape)", IsShapeBroken(PlaneShape))
-
-end
-
+#version 2
 function travel1()
 
     local fraction = GetTime()/65
@@ -197,4 +74,96 @@
 	ParticleRadius(0.05, 0.3)
 	ParticleStretch(1.0)
 	SpawnParticle(PlaneBodyT.pos, Vec(0, 0, 0), 10.0)
-end+end
+
+function server.init()
+    Pos1A = FindLocation("1A")
+    Pos2A = FindLocation("2A")
+    Pos1B = FindLocation("1B")
+    Pos2B = FindLocation("2B")
+    Snd = LoadLoop("MOD/main/plane/plane.ogg")
+    broken = false
+    canbreak = true
+    spawnTable = {
+    	"MOD/main/plane/prefabs/Blue_plane.xml",
+    	"MOD/main/plane/prefabs/Grey_plane.xml",
+    	"MOD/main/plane/prefabs/Red_plane.xml"
+    }
+    pick = true
+    explode = true
+    flythroughs_last = 0
+    flythroughs = 1
+    FireTime = 0
+end
+
+function server.tick(dt)
+    PlaneBody = FindBody("PB")
+    PlaneShape = FindShape("plane")
+    PlaneBodyT = GetBodyTransform(PlaneBody)
+    PlaneShapeT = GetShapeWorldTransform(PlaneShape)
+    Pos1TA = GetLocationTransform(Pos1A)
+    Pos2TA = GetLocationTransform(Pos2A)
+    Pos1TB = GetLocationTransform(Pos1B)
+    Pos2TB = GetLocationTransform(Pos2B)
+    if pick == true then
+    	randomSpawnIndex = math.random(1, 3)
+    	randomRouteIndex = math.random(1, 2)
+    	pick = false
+    end
+    if canbreak == false then
+    	broken = false
+    	canbreak = true
+    end
+    if pick == false then
+    	if randomRouteIndex == 1 then
+    		travel1()
+    	end
+
+    	if randomRouteIndex == 2 then
+    		travel2()
+    	end
+    end
+    if canbreak == true then
+    	if IsShapeBroken(PlaneShape) == true then
+    		broken = true
+    		canbreak = false
+    		SetBodyDynamic(PlaneBody, true)
+
+    		SetBodyAngularVelocity(PlaneBody, Vec(0, 0, 5))
+    		ApplyBodyImpulse(PlaneBody, PlaneBodyT.pos, QuatRotateVec(PlaneBodyT.rot, Vec(0, 0, -600)))
+
+    		QueryRejectBody(PlaneBody)
+    		QueryRejectShape(PlaneShape)
+
+    		local hit, point, normal, shape = QueryClosestPoint(PlaneShapeT.pos, 0.7)
+
+    		--DebugCross(point, 1, 0, 0, 1)
+    		--DebugWatch('hitpoint', point)
+
+    		if hit == true and GetShapeVoxelCount(shape) > 100 and explode == true then
+    			Explosion(PlaneShapeT.pos, 1)
+    			explode = false
+    		end
+
+    		RemoveTag(PlaneBody, "PB")
+    		pick = true
+    		smoke()
+
+    		FireTime = FireTime + dt
+    		if FireTime > 5 then
+    			RemoveTag(PlaneShape, "plane")
+    			explode = true
+    			FireTime = 0
+    		end
+    	end
+    end
+end
+
+function client.tick(dt)
+    if broken == false and IsHandleValid(PlaneBody) == true then
+    	trail()
+    	PlayLoop(Snd, PlaneBodyT.pos, 0.25)
+    	SetBodyDynamic(PlaneBody, false)
+    end
+end
+

```

---

# Migration Report: main\scripts\blink.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\blink.lua
+++ patched/main\scripts\blink.lua
@@ -1,13 +1,10 @@
-function init()
-
-	radio = FindShape("radio")
-	
+#version 2
+function server.init()
+    radio = FindShape("radio")
 end
 
-function tick()
+function server.tick(dt)
+    local scale = math.sin(GetTime())*0.5 + 0.5
+    SetShapeEmissiveScale(radio, scale)
+end
 
-	local scale = math.sin(GetTime())*0.5 + 0.5
-	
-	SetShapeEmissiveScale(radio, scale)
-
-end
```

---

# Migration Report: main\scripts\Color_cycle-1ssnl.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\Color_cycle-1ssnl.lua
+++ patched/main\scripts\Color_cycle-1ssnl.lua
@@ -1,3 +1,4 @@
+#version 2
 local function hsl_to_rgb(hue, saturation, lightness)
 	-- https://en.wikipedia.org/wiki/HSL_and_HSV#To_RGB
 	hue = hue % 360
@@ -21,20 +22,23 @@
 	local m = lightness-chroma/2
 	return red+m, green+m, blue+m
 end
-function init()
-	lights = FindLights("hue")
+
+function server.init()
+    lights = FindLights("hue")
 end
-function tick()
-	for i=1, #lights do
-	local light = lights[i]
-		local h, s, l = (GetTime()*90)%360, 1, 0.5
-		local r, g, b = hsl_to_rgb(h, s, l)
-		SetLightColor(light, r, g, b)
-		--DebugWatch("h", h)
-		--DebugWatch("s", s)
-		--DebugWatch("l", l)
-		--DebugWatch("r", r)
-		--DebugWatch("g", g)
-		--DebugWatch("b", b)
-	end
-end+
+function server.tick(dt)
+    for i=1, #lights do
+    local light = lights[i]
+    	local h, s, l = (GetTime()*90)%360, 1, 0.5
+    	local r, g, b = hsl_to_rgb(h, s, l)
+    	SetLightColor(light, r, g, b)
+    	--DebugWatch("h", h)
+    	--DebugWatch("s", s)
+    	--DebugWatch("l", l)
+    	--DebugWatch("r", r)
+    	--DebugWatch("g", g)
+    	--DebugWatch("b", b)
+    end
+end
+

```

---

# Migration Report: main\scripts\Color_cycle.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\Color_cycle.lua
+++ patched/main\scripts\Color_cycle.lua
@@ -1,24 +1,23 @@
-function init()
-	lights = FindLights("hue")
-
+#version 2
+function server.init()
+    lights = FindLights("hue")
 end
 
-function tick()
+function server.tick(dt)
+    for i=1, #lights do
 
-	for i=1, #lights do
+    	local light = lights[i]
 
-		local light = lights[i]
-		
-		local r = Vec(1, 0, 0)
-		local g = Vec(0, 1, 0)
-		local b = Vec(0, 0, 1)
+    	local r = Vec(1, 0, 0)
+    	local g = Vec(0, 1, 0)
+    	local b = Vec(0, 0, 1)
 
-		R = VecLerp(r, g, 0.5)
-		G = VecLerp(g, b, 0.5)
-		B = VecLerp(b, r, 0.5)
+    	R = VecLerp(r, g, 0.5)
+    	G = VecLerp(g, b, 0.5)
+    	B = VecLerp(b, r, 0.5)
 
-		SetLightColor(light, R, G, B)
+    	SetLightColor(light, R, G, B)
 
-	end
+    end
+end
 
-end
```

---

# Migration Report: main\scripts\smoke.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\smoke.lua
+++ patched/main\scripts\smoke.lua
@@ -1,20 +1,22 @@
-function init()
-	build = FindShape("build")
-	loc = FindLight("loc")
-	time = 0
+#version 2
+function server.init()
+    build = FindShape("build")
+    loc = FindLight("loc")
+    time = 0
 end
 
-function tick(dt)
-	if IsShapeBroken(build) == false then
-		loct = GetLightTransform(loc)
-		time = time + dt
-		ParticleType("smoke")
-		ParticleColor(1.0, 1.0, 1.0)
-		ParticleCollide(0)
-		ParticleAlpha(0.5, 0.0)
-		ParticleGravity(0.1)
-		ParticleRadius(0.05, 0.1)
-		ParticleStretch(1.0)
-		SpawnParticle(loct.pos, Vec(0, 0.01, 0), 4)
-	end
-end+function client.tick(dt)
+    if IsShapeBroken(build) == false then
+    	loct = GetLightTransform(loc)
+    	time = time + dt
+    	ParticleType("smoke")
+    	ParticleColor(1.0, 1.0, 1.0)
+    	ParticleCollide(0)
+    	ParticleAlpha(0.5, 0.0)
+    	ParticleGravity(0.1)
+    	ParticleRadius(0.05, 0.1)
+    	ParticleStretch(1.0)
+    	SpawnParticle(loct.pos, Vec(0, 0.01, 0), 4)
+    end
+end
+

```

---

# Migration Report: main\scripts\WindTurbine.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\scripts\WindTurbine.lua
+++ patched/main\scripts\WindTurbine.lua
@@ -1,11 +1,8 @@
-function init()
-	
-	blades = FindShape("blade")
+#version 2
+function server.init()
+    blades = FindShape("blade")
+    body = GetShapeBody(blades)
+    hinge = FindJoint("hinge")
+    SetJointMotor(hinge, 5, 100)
+end
 
-	body = GetShapeBody(blades)
-
-	hinge = FindJoint("hinge")
-
-	SetJointMotor(hinge, 5, 100)
-
-end
```

---

# Migration Report: main\TurbineLogos\TL.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\TurbineLogos\TL.lua
+++ patched/main\TurbineLogos\TL.lua
@@ -1,5 +1,7 @@
-function draw()
-	UiTranslate(UiCenter(), UiMiddle())
-	UiAlign("center middle")
-	UiImage("MOD/main/TurbineLogos/logo.jpg")
-end+#version 2
+function client.draw()
+    UiTranslate(UiCenter(), UiMiddle())
+    UiAlign("center middle")
+    UiImage("MOD/main/TurbineLogos/logo.jpg")
+end
+

```

---

# Migration Report: menu\menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/menu\menu.lua
+++ patched/menu\menu.lua
@@ -1,60 +1,58 @@
+#version 2
+function client.draw()
+    local w = UiWidth()
+    local h = UiHeight()
 
-function draw()
---	if GetBool("level.menuCancel") then
---		return
---	end
-	local w = UiWidth()
-	local h = UiHeight()
-	
-	UiMakeInteractive()
-	
-	UiPush()
-		UiColor(0,0,0,1)
-		UiRect(w,h)
-		UiColor(1,1,1)
-		local iw, ih = UiGetImageSize("MOD/menu/background2.jpg")
-		UiScale(w/iw)
-		UiImage("MOD/menu/background2.jpg")
-	UiPop()
-	
-	UiPush()
-		UiAlign("center middle")
-		UiFont("bold.ttf",36)
-		
-		UiTranslate(w*0.3,(h*0.5)+100)
-		UiColor(1,1,1)
-		
-		UiPush()
-			
-			local iw, ih = UiGetImageSize("MOD/menu/day.png")
-			UiScale(800/iw)
-			
-			if UiImageButton("MOD/menu/day.png",400,30) then
-				StartLevel("level1","MOD/day.xml")
-			end
-		UiPop()
-		
-		--UiPush()
-		--	UiTranslate(0,UiFontHeight()+200)
-		--	UiText("Day")
-		--UiPop()
-		
-		UiTranslate(w*0.4,0)
-		
-		UiPush()
-			
-			local iw, ih = UiGetImageSize("MOD/menu/night.png")
-			UiScale(800/iw)
-			
-			if UiImageButton("MOD/menu/night.png",400,30) then
-				StartLevel("level2","MOD/night.xml")
-			end
-		UiPop()
-		
-		--UiPush()
-		--	UiTranslate(0,UiFontHeight()+200)
-		--	UiText("Night")
-		--UiPop()
-		
-	UiPop()
+    UiMakeInteractive()
+
+    UiPush()
+    	UiColor(0,0,0,1)
+    	UiRect(w,h)
+    	UiColor(1,1,1)
+    	local iw, ih = UiGetImageSize("MOD/menu/background2.jpg")
+    	UiScale(w/iw)
+    	UiImage("MOD/menu/background2.jpg")
+    UiPop()
+
+    UiPush()
+    	UiAlign("center middle")
+    	UiFont("bold.ttf",36)
+
+    	UiTranslate(w*0.3,(h*0.5)+100)
+    	UiColor(1,1,1)
+
+    	UiPush()
+
+    		local iw, ih = UiGetImageSize("MOD/menu/day.png")
+    		UiScale(800/iw)
+
+    		if UiImageButton("MOD/menu/day.png",400,30) then
+    			StartLevel("level1","MOD/day.xml")
+    		end
+    	UiPop()
+
+    	--UiPush()
+    	--	UiTranslate(0,UiFontHeight()+200)
+    	--	UiText("Day")
+    	--UiPop()
+
+    	UiTranslate(w*0.4,0)
+
+    	UiPush()
+
+    		local iw, ih = UiGetImageSize("MOD/menu/night.png")
+    		UiScale(800/iw)
+
+    		if UiImageButton("MOD/menu/night.png",400,30) then
+    			StartLevel("level2","MOD/night.xml")
+    		end
+    	UiPop()
+
+    	--UiPush()
+    	--	UiTranslate(0,UiFontHeight()+200)
+    	--	UiText("Night")
+    	--UiPop()
+
+    UiPop()
 end
+

```

---

# Migration Report: menu\menuCancel.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/menu\menuCancel.lua
+++ patched/menu\menuCancel.lua
@@ -1,3 +1,5 @@
-function init()
-	SetBool("level.menuCancel",true)
-end+#version 2
+function server.init()
+    SetBool("level.menuCancel",true, true)
+end
+

```
