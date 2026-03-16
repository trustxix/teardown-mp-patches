# Migration Report: ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/ground.lua
+++ patched/ground.lua
@@ -1,36 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
+    matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
+    matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
+    matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h do
+    	local y1 = y0 + maxSize
+    	if y1 > h then y1 = h end
 
-function init()
-	matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
-	matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
-	matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
-	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("masonry", 0.6, 0.6, 0.6, 1, 0, 0.6)
-	
-	LoadImage(file)
-	
-	w,h = GetImageSize()
-
-	local maxSize = tileSize
-	
-	local y0 = 0
-	while y0 < h do
-		local y1 = y0 + maxSize
-		if y1 > h then y1 = h end
-
-		local x0 = 0
-		while x0 < w do
-			local x1 = x0 + maxSize
-			if x1 > w then x1 = w end
-			Vox(x0, 0, y0)
-			Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
-			x0 = x1
-		end
-		y0 = y1
-	end
+    	local x0 = 0
+    	while x0 < w do
+    		local x1 = x0 + maxSize
+    		if x1 > w then x1 = w end
+    		Vox(x0, 0, y0)
+    		Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
+    		x0 = x1
+    	end
+    	y0 = y1
+    end
 end
 

```

---

# Migration Report: towerLift.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/towerLift.lua
+++ patched/towerLift.lua
@@ -1,33 +1,4 @@
-function init()
-	up = FindShapes("ap", true)
-	down = FindShapes("dawn", true)
-	motor = FindJoint("matar", true)
-	cabin = FindShape("caban", true)
-	
-	liftTop = FindTrigger("tap", true)
-	liftBottom = FindTrigger("battam", true)
-	
-	motorRun = LoadLoop("vehicle/hydraulic-loop.ogg")
-	chime = LoadSound("elevator-chime.ogg")
-	
-	
-	doorSpeed = 0
-	speed = 0
-	
-	
-	for i=1,#up do
-		SetTag(up[i], "interact", "Up")
-	end
-
-	for i=1,#down do
-		SetTag(down[i], "interact", "Down")
-	end
-
-	movingUp = false
-	movingDown = false
-
-end
-
+#version 2
 function moveUp()
 	movingDown = false
 	SetJointMotor(motor, speed + 20) --lift speed, up.
@@ -46,38 +17,57 @@
 	PlaySound(chime, motorPos) --Plays a chime when the elevator stops.
 end
 
-function tick(dt)
-local motorPos = GetShapeWorldTransform(cabin).pos
-
-	for i=1,#up do
-		if GetPlayerInteractShape() == up[i] and InputPressed("interact") then
-			movingUp = true
-			moveUp()
-		end
-	end
-
-	for i=1,#down do
-		if GetPlayerInteractShape() == down[i] and InputPressed("interact") then
-			movingDown = true
-			moveDown()
-		end
-	end
-	
-	if movingUp or movingDown then
-		PlayLoop(motorRun, motorPos)
-	end
-	
-	if IsPointInTrigger(liftTop, motorPos) and movingUp then
-		stopMoving()
-	elseif IsPointInTrigger(liftBottom, motorPos) and movingDown then
-		stopMoving()
-	end
-	
-	if GetPlayerHealth() < 1 then --invincibility
-		SetPlayerHealth(1)
-	end
+function server.init()
+    up = FindShapes("ap", true)
+    down = FindShapes("dawn", true)
+    motor = FindJoint("matar", true)
+    cabin = FindShape("caban", true)
+    liftTop = FindTrigger("tap", true)
+    liftBottom = FindTrigger("battam", true)
+    motorRun = LoadLoop("vehicle/hydraulic-loop.ogg")
+    doorSpeed = 0
+    speed = 0
+    for i=1,#up do
+    	SetTag(up[i], "interact", "Up")
+    end
+    for i=1,#down do
+    	SetTag(down[i], "interact", "Down")
+    end
+    movingUp = false
+    movingDown = false
 end
 
+function server.tick(dt)
+    local motorPos = GetShapeWorldTransform(cabin).pos
+    	if IsPointInTrigger(liftTop, motorPos) and movingUp then
+    		stopMoving()
+    	elseif IsPointInTrigger(liftBottom, motorPos) and movingDown then
+    		stopMoving()
+    	end
+    	if GetPlayerHealth(playerId) < 1 then --invincibility
+    		SetPlayerHealth(playerId, 1)
+    	end
+end
 
+function client.init()
+    chime = LoadSound("elevator-chime.ogg")
+end
 
---work in progress.+function client.tick(dt)
+    for i=1,#up do
+    	if GetPlayerInteractShape(playerId) == up[i] and InputPressed("interact") then
+    		movingUp = true
+    		moveUp()
+    	end
+    end
+    for i=1,#down do
+    	if GetPlayerInteractShape(playerId) == down[i] and InputPressed("interact") then
+    		movingDown = true
+    		moveDown()
+    	end
+    end
+    if movingUp or movingDown then
+    	PlayLoop(motorRun, motorPos)
+    end
+end
+

```
