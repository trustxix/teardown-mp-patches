# Migration Report: script\ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ground.lua
+++ patched/script\ground.lua
@@ -1,36 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.41, 0.41, 0.41)
+    matDirt = CreateMaterial("dirt", 0.31, 0.44, 0.21, 1, 0, 0.1)
+    matGrass1 = CreateMaterial("unphysical", 0.31, 0.44, 0.21, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.34, 0.41, 0.23, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.41, 0.41, 0.41, 1, 0, 0.4)
+    matTarmacTrack = CreateMaterial("masonry", 0.32, 0.33, 0.34, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("masonry", 0.54, 0.54, 0.54, 1, 0, 0.6)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h do
+    	local y1 = y0 + maxSize
+    	if y1 > h then y1 = h end
 
-function init()
-	matRock = CreateMaterial("rock", 0.41, 0.41, 0.41)
-	matDirt = CreateMaterial("dirt", 0.31, 0.44, 0.21, 1, 0, 0.1)
-	matGrass1 = CreateMaterial("unphysical", 0.31, 0.44, 0.21, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.34, 0.41, 0.23, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.41, 0.41, 0.41, 1, 0, 0.4)
-	matTarmacTrack = CreateMaterial("masonry", 0.32, 0.33, 0.34, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("masonry", 0.54, 0.54, 0.54, 1, 0, 0.6)
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

# Migration Report: script\menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\menu.lua
+++ patched/script\menu.lua
@@ -1,116 +1,116 @@
-function init()
-
-	snd = LoadSound("MOD/snd/tool-select.ogg")
-	
-	if GetString("savegame.mod.weather") == "" then
-		SetString("savegame.mod.weather", "sunny")
-	end
-
-	lvl = GetString("savegame.mod.weather")
-	
+#version 2
+function server.init()
+    if GetString("savegame.mod.weather") == "" then
+    	SetString("savegame.mod.weather", "sunny", true)
+    end
+    lvl = GetString("savegame.mod.weather")
 end
 
-function tick(dt)
-	PlayMusic("[MUSIC FILE OF YOUR CHOICE, CAN USE VANILLA GAME ONES IN FILES]")
-	UiMakeInteractive()
+function server.tick(dt)
+    PlayMusic("[MUSIC FILE OF YOUR CHOICE, CAN USE VANILLA GAME ONES IN FILES]")
 end
 
-function draw()
+function client.init()
+    snd = LoadSound("MOD/snd/tool-select.ogg")
+end
 
+function client.tick(dt)
+    UiMakeInteractive()
+end
 
-	--Ui
-	UiAlign("center middle")
-	UiFont("regular.ttf", 26)
-	UiButtonImageBox("MOD/common/box-outline-6.png", 6, 6)
-	UiButtonHoverColor(1,1,0.6)
+function client.draw()
+    	UiAlign("center middle")
+    	UiFont("regular.ttf", 26)
+    	UiButtonImageBox("MOD/common/box-outline-6.png", 6, 6)
+    	UiButtonHoverColor(1,1,0.6)
 
-	UiPush()
-	scale=(UiWidth()-0)/1300
-	UiTranslate(UiWidth()-0,0)
-	UiAlign("right top")
-	UiScale(scale)
-	
-	if GetBool("savegame.mod.rain") then
-	UiImage("MOD/image/2021-10-02-03-09-03.png")
-	else
-	UiImage("MOD/image/2021-10-02-03-09-03.png")
-	end
+    	UiPush()
+    	scale=(UiWidth()-0)/1300
+    	UiTranslate(UiWidth()-0,0)
+    	UiAlign("right top")
+    	UiScale(scale)
 
-UiPop()
+    	if GetBool("savegame.mod.rain") then
+    	UiImage("MOD/image/2021-10-02-03-09-03.png")
+    	else
+    	UiImage("MOD/image/2021-10-02-03-09-03.png")
+    	end
 
-UiPush()
-UiTranslate(100, 90)
-UiAlign("left top")
-UiImageBox("MOD/common/sign-01.png", 270, 900, 75, 75)
-UiPop()
-	
-	--Draw buttons
-	UiPush()
-		UiTranslate(239, 160)
-		UiText("[SECTION TITLE]")
-		UiTranslate(0, 50)
-		if GetBool("wtc_new") then
-			UiPush()
-				UiColor(1, 0.4, 0.1, 0.5)
-				UiImageBox("MOD/common/box-solid-6.png", 200, 40, 6, 6)
-			UiPop()
-		end
-		if UiTextButton("New WTC", 200, 40) then
-			PlaySound(snd)
-			SetBool("wtc_new", true)
-			SetBool("wtc_old", false)
-		end
+    UiPop()
 
-		UiTranslate(0, 50)
-		if GetBool("wtc_old") then
-			UiPush()
-				UiColor(1, 0.4, 0.1, 0.5)
-				UiImageBox("MOD/common/box-solid-6.png", 200, 40, 6, 6)
-			UiPop()
-		end
-		if UiTextButton("Old WTC", 200, 40) then
-			PlaySound(snd)
-			SetBool("wtc_old", true)
-			SetBool("wtc_new", false)
-		end
+    UiPush()
+    UiTranslate(100, 90)
+    UiAlign("left top")
+    UiImageBox("MOD/common/sign-01.png", 270, 900, 75, 75)
+    UiPop()
 
-		UiTranslate(0, 50)
-		if GetBool("wtc_both") then
-			UiPush()
-				UiColor(1, 0.4, 0.1, 0.5)
-				UiImageBox("MOD/common/box-solid-6.png", 200, 40, 6, 6)
-			UiPop()
-		end
-		if UiTextButton("Both", 200, 40) then
-			PlaySound(snd)
-			SetBool("wtc_new", true)
-			SetBool("wtc_old", true)
-		end
-			
-		if not GetBool("wtc_new") and not GetBool("wtc_old") then
-			SetBool("wtc_new", true)
-			end
-		
-		UiTranslate(0, 200)
-		if UiTextButton("Ready", 200, 40) then
-			PlaySound(snd)
-			if GetBool("wtc_new") then
-				lvl = lvl.." wtc_new"
-			end
-			if GetBool("wtc_old") then
-				lvl = lvl.." wtc_old"
-			end
-			StartLevel("", "MOD/lvl.xml", lvl)
-		end
+    	--Draw buttons
+    	UiPush()
+    		UiTranslate(239, 160)
+    		UiText("[SECTION TITLE]")
+    		UiTranslate(0, 50)
+    		if GetBool("wtc_new") then
+    			UiPush()
+    				UiColor(1, 0.4, 0.1, 0.5)
+    				UiImageBox("MOD/common/box-solid-6.png", 200, 40, 6, 6)
+    			UiPop()
+    		end
+    		if UiTextButton("New WTC", 200, 40) then
+    			PlaySound(snd)
+    			SetBool("wtc_new", true, true)
+    			SetBool("wtc_old", false, true)
+    		end
 
-				
-		UiTranslate(0, 50)
-		if UiTextButton("Exit", 200, 40) then
-			PlaySound(snd)
-			Menu()
-		end
-		UiTranslate(0, 65)
-		UiTranslate(-110, 0)
-		UiColor(0.5, 1, 0.1, 1)
-	UiPop()
-	end
+    		UiTranslate(0, 50)
+    		if GetBool("wtc_old") then
+    			UiPush()
+    				UiColor(1, 0.4, 0.1, 0.5)
+    				UiImageBox("MOD/common/box-solid-6.png", 200, 40, 6, 6)
+    			UiPop()
+    		end
+    		if UiTextButton("Old WTC", 200, 40) then
+    			PlaySound(snd)
+    			SetBool("wtc_old", true, true)
+    			SetBool("wtc_new", false, true)
+    		end
+
+    		UiTranslate(0, 50)
+    		if GetBool("wtc_both") then
+    			UiPush()
+    				UiColor(1, 0.4, 0.1, 0.5)
+    				UiImageBox("MOD/common/box-solid-6.png", 200, 40, 6, 6)
+    			UiPop()
+    		end
+    		if UiTextButton("Both", 200, 40) then
+    			PlaySound(snd)
+    			SetBool("wtc_new", true, true)
+    			SetBool("wtc_old", true, true)
+    		end
+
+    		if not GetBool("wtc_new") and not GetBool("wtc_old") then
+    			SetBool("wtc_new", true, true)
+    			end
+
+    		UiTranslate(0, 200)
+    		if UiTextButton("Ready", 200, 40) then
+    			PlaySound(snd)
+    			if GetBool("wtc_new") then
+    				lvl = lvl.." wtc_new"
+    			end
+    			if GetBool("wtc_old") then
+    				lvl = lvl.." wtc_old"
+    			end
+    			StartLevel("", "MOD/lvl.xml", lvl)
+    		end
+
+    		UiTranslate(0, 50)
+    		if UiTextButton("Exit", 200, 40) then
+    			PlaySound(snd)
+    			Menu()
+    		end
+    		UiTranslate(0, 65)
+    		UiTranslate(-110, 0)
+    		UiColor(0.5, 1, 0.1, 1)
+    	UiPop()
+end
+

```

---

# Migration Report: script\small_player.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\small_player.lua
+++ patched/script\small_player.lua
@@ -1,11 +1,12 @@
-function init()
-    camera = TransformCopy(GetPlayerCameraTransform())
+#version 2
+function server.init()
+    camera = TransformCopy(GetPlayerCameraTransform(playerId))
     Local_camera = TransformToLocalPoint(camera)
     camera_pos = Local_camera.pos
 end
 
-function update(dt)
-    camera = TransformCopy(GetPlayerCameraTransform())
+function server.update(dt)
+    camera = TransformCopy(GetPlayerCameraTransform(playerId))
+    SetCameraTransform(GetPlayerCameraTransform(playerId)[1], GetPlayerCameraTransform(playerId)[2])
+end
 
-    SetCameraTransform(GetPlayerCameraTransform()[1], GetPlayerCameraTransform()[2])
-end

```
