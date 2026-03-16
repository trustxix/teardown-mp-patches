# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,39 +1,19 @@
-#include "scripts/debug.lua"
-#include "scripts/alwaysup.lua"
-#include "scripts/registry.lua"
-#include "scripts/umf.lua"
-#include "scripts/ui.lua"
-#include "scripts/utility.lua"
-#include "scripts/shape_utils.lua"
-
-------------------------------------------------
---- Always Up!
---- By: Geneosis
-------------------------------------------------
-
-function init()
-
+#version 2
+function server.init()
     UI_GAME = false
     checkRegInitialized()
-
     initDebug()
     AlwaysUp.init()
-
 end
 
-
-function tick()
-
-    AlwaysUp.run()
-    debugMod()
-
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        AlwaysUp.run()
+        debugMod()
+    end
 end
 
-
-function draw()
-
+function client.draw()
     uiDrawScores()
-
 end
 
-UpdateQuickloadPatch()

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
@@ -1,15 +1,11 @@
-#include "scripts/umf.lua"
-#include "scripts/registry.lua"
-#include "scripts/ui.lua"
-#include "scripts/utility.lua"
-
-
-function init()
+#version 2
+function server.init()
     UI_OPTIONS = true
     checkRegInitialized()
     uiUpdateGalleryItems()
 end
 
-function draw()
+function client.draw()
     uiDrawOptions()
 end
+

```

---

# Migration Report: scripts\alwaysup.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\alwaysup.lua
+++ patched/scripts\alwaysup.lua
@@ -1,583 +1,15 @@
-#include "debug.lua"
-#include "registry.lua"
-#include "umf.lua"
-#include "ui.lua"
-#include "utility.lua"
-
-------------------------------------------------
---- Always Up!
---- By: Geneosis
-------------------------------------------------
-
-AlwaysUp = {}
-AlwaysUp.info = {
-    -- Generation
-    errorMsg = nil,
-    mapCenter = Vec(),
-    mapRadius = 0,
-    shapeModels = {},
-    orderedModelIndexes = {},
-    nbModels = 0,
-    startPos = Vec(),
-    currentPos = Vec(),
-    randIndex = 0,
-    randSeq = {},
-    randSeqLen = 0,
-    seed = regGetInt('always_up.seed'),
-    lastDir = Vec(),
-    generationDist = regGetInt('always_up.generationDist') * 100,
-    generationBufferSize = 50,
-    generationBuffering = true,
-    maxAngleWithoutSlide = 41,
-    failedSpawn = 0,
-    maxFailedSpawn = 10,
-    maxTotalFailedSpawn = 100,
-    lastBody = 0,
-    lastValidCurPos = Vec(),
-    lastValidDir = Vec(),
-    -- Score
-    score = 0,
-    bestScore = 0,
-    wasWalking = false,
-    validated = true,
-    lastValidPos = Vec(),
-    spawnCompleted = false,
-    lowPlacementAllowed = true,
-    highestPos = Vec(),
-    maxJumpHeight = 1.85, -- With bluetide
-    maxJumpLength = 14, -- With bluetide
-    maxWalkSpeed = 0.5, -- With bluetide
-    scoreKey = nil,
-    wasPaused = false,
-}
-
-
-function AlwaysUp.init()
-    local aui = AlwaysUp.info
-    dbp("Always Up!: Initializing...")
-    aui.bestScore = AlwaysUp.loadBestScore()
-    local min, max = GetBodyBounds(GetWorldBody())
-    -- Compute map center and outside radius
-    QueryRequire("physical visible dynamic")
-    dbp("Always Up!: Requesting all dynamic bodies")
-    local allDynBodies = QueryAabbBodies(min, max)
-    local nbDynBodies = #allDynBodies
-    if nbDynBodies > 0 then
-        local sum = Vec(0, 0, 0)
-        for i=1,nbDynBodies do
-            sum = VecAdd(sum, AabbGetBodyCenterPos(allDynBodies[i]))
-        end
-        aui.mapCenter = VecScale(sum, 1/nbDynBodies)
-    else
-        aui.mapCenter = AabbGetCenterPos(min,max)
-    end
-    local diagonal2D = VecFlatten(VecSub(max, min))
-    aui.mapRadius = VecLength(diagonal2D) / 2.0
-    -- Store all objects on the map for future copy
-    QueryRequire("physical large visible")
-    dbp("Always Up!: Requesting all shapes")
-    local allShapes = QueryAabbShapes(min, max)
-    local nbShapes = #allShapes
-    if nbShapes == 0 then
-        aui.errorMsg = "Always Up!: Not enough pieces to generate parkour for this map, please load another one"
-        return
-    end
-    local debrisSize = 10
-    local debrisVoxels = 200
-    dbp("Always Up!: Selecting model shapes...")
-    local progress = 0
-    for i=1,nbShapes do
-        if db then
-            local section = nbShapes / 10
-            local curProgress = math.floor(i/section)
-            if curProgress > progress then
-                progress = curProgress
-                dbp("Always Up!: - Progress "..progress.."0%")
-            end
-        end
-        local shape = allShapes[i]
-        local x, y, z, s = GetShapeSize(shape)
-        -- If shape is too small, skip it
-        local isDebris = (x < debrisSize) and (y < debrisSize) and (z < debrisSize) and GetShapeVoxelCount(shape) < debrisVoxels
-        if not isDebris then
-            local shapeTr = GetShapeWorldTransform(shape)
-            local body = GetShapeBody(shape)
-            local shapeModel = {
-                radius = AlwaysUp.getShapeRadius(shape),
-                content = GetShapeContent(shape),
-                palette = AlwaysUp.MakePaletteBreakable(GetShapePaletteContent(shape)),
-                size = {x = x, y = y, z = z, s = s},
-                localTr = TransformToLocalTransform(GetBodyTransform(body), shapeTr),
-                -- This is not yet implemented in game API, but prepare the structure for it
-                texture = {
-                    index = 0,
-                    opacity = 0
-                }
-            }
-            aui.nbModels = aui.nbModels + 1
-            aui.shapeModels[aui.nbModels] = shapeModel
-            aui.orderedModelIndexes[aui.nbModels] = aui.nbModels
-        end
-    end
-    dbp("Always Up!: - Progress 100%")
-    -- Sort all objects on the map by size
-    dbp("Always Up!: Sorting shapes indexes")
-    table.sort(aui.orderedModelIndexes, function(a,b) return aui.shapeModels[a].radius > aui.shapeModels[b].radius end)
-    -- Compute starting position
-    local traceStart = Vec(aui.mapCenter[1], max[2], aui.mapCenter[3])
-    local traceEnd = Vec(aui.mapCenter[1], min[2], aui.mapCenter[3])
-    local startToEnd = VecSub(traceEnd, traceStart)
-    local dir = VecNormalize(startToEnd)
-    local hit, dist, normal, shape = QueryRaycast(traceStart, dir, VecLength(startToEnd))
-    aui.startPos = aui.mapCenter
-    if hit then
-        aui.startPos = VecAdd(traceStart, VecResize(startToEnd, dist))
-    end
-    aui.currentPos = aui.startPos
-    aui.highestPos = aui.currentPos
-    aui.lastValidCurPos = aui.currentPos
-    aui.lastDir = VecRotate(Vec(1, 0, 0), "y", AlwaysUp.getNextRand(0, 360))
-    aui.lastValidDir = aui.lastDir
-    -- Generate initial parjour section while loading screen is active
-    local playerTr = GetPlayerTransform()
-    local totalFails = 0
-    if regGetBool('always_up.noInitialGen') then
-        dbp("Always Up!: Preloading disabled")
-        return
-    end
-    dbp("Always Up!: Generating initial parkour path...")
-    progress = 0
-    while aui.currentPos[2] < (playerTr.pos[2] + aui.generationDist) do
-        if db then
-            local section = (playerTr.pos[2] + aui.generationDist) / 10
-            local curProgress = math.floor(aui.currentPos[2]/section)
-            if curProgress > progress then
-                progress = curProgress
-                dbp("Always Up!: - Progress "..progress.."0%")
-            end
-        end
-        AlwaysUp.generateNextParkourSection()
-        -- Count total fails
-        if aui.failedSpawn > 0 then
-            totalFails = totalFails + 1
-        end
-        -- If too many fails, delete previous piece
-        if aui.failedSpawn >= aui.maxFailedSpawn then
-            if aui.lastBody > 0 then
-                Delete(aui.lastBody)
-                aui.currentPos = aui.lastValidCurPos
-                aui.lastDir = aui.lastValidDir
-                aui.failedSpawn = 0
-                aui.lastBody = 0
-            else
-                aui.errorMsg = "Always Up!: An error occured during map generation, please try with another seed"
-                return
-            end
-        end
-        -- If too many total fails, abort generation
-        if totalFails > aui.maxTotalFailedSpawn then
-            aui.errorMsg = "Always Up!: Failed to generate parkour for this map, please load another one"
-            return
-        end
-    end
-    dbp("Always Up!: - Progress 100%")
-end
-
-function AlwaysUp.MakePaletteBreakable(palette)
-    local breakableMaterials = {"glass", "dirt", "wood", "plaster", "metal", "masonry", "foliage", "plastic", "ice", "hardmetal", "hardmasonry"}
-    -- Make lookup table for breakable materials
-    local isMatBreakable = {}
-    for i=1,#breakableMaterials do
-        isMatBreakable[breakableMaterials[i]]=true
-    end
-    -- Replace any non breakable material by a breakable one
-    for i=1,#palette do
-        if not isMatBreakable[palette[i].material] then
-            if palette[i].material == "heavymetal" then
-                palette[i].material = "hardmetal"
-            elseif palette[i].material == "unphysical" then
-                palette[i].material = "foliage"
-            else
-                palette[i].material = "masonry"
-            end
-        end
-    end
-    return palette
-end
-
-function AlwaysUp.getShapeRadius(shape)
-    local tr, min, max = GetShapeObb(shape)
-    local corners = GetObbCorners(tr, min, max)
-    local diagonal = VecSub(corners[1], corners[7])
-    return VecLength(diagonal) / 2.0
-end
-
-function AlwaysUp.run()
-    local aui = AlwaysUp.info
-    if aui.errorMsg ~= nil then
-        return
-    end
-    -- Generate next part of the challenge if needed
-    AlwaysUp.generateParkour()
-    -- Compute current player score
-    AlwaysUp.computeScore()
-    -- If insta save disabled, only save when player enters pause menu
-    if not regGetBool('always_up.instaSave') then
-        SetBool("game.disablepause", true)
-        if InputDown("pause") then
-            if not aui.wasPaused then
-                AlwaysUp.saveBestScore(aui.bestScore)
-                aui.wasPaused = true
-                SetPaused(true)
-            end
-        else
-            aui.wasPaused = false
-        end
-    end
-end
-
-function AlwaysUp.getErrorMsg()
-    local aui = AlwaysUp.info
-    return aui.errorMsg
-end
-
-lastBody = 0
-endFlag = 20
-function AlwaysUp.generateParkour()
-    local aui = AlwaysUp.info
-    dbpt(aui.startPos, 1, 1, 0, 1)
-    dbpt(aui.currentPos, 1, 1, 1, 1)
-    if db then
-        local min, max = GetBodyBounds(GetWorldBody())
-        AabbDraw(min, max, 0, 0, 1, 1)
-        dbl(aui.currentPos, VecAdd(aui.currentPos, aui.lastDir), 1, 1, 1, 1)
-        if lastBody > 0 then
-            dbl(lastPos, VecAdd(lastPos, lastLastDir), 0, 0, 1, 1)
-            local center = AabbGetBodyCenterPos(lastBody)
-            local bodyTr = GetBodyTransform(lastBody)
-            local shapeTr = GetShapeWorldTransform(lastShape)
-            dbl(center, VecAdd(center, VecResize(TransformToParentVec(shapeTr, lastMainShape)), 1.5), 0.5, 1, 0.5, 1)
-            dbl(center, VecAdd(center, VecResize(TransformToParentVec(shapeTr, lastUpShape)), 1.5), 1, 0.5, 0.5, 1)
-            dbl(center, VecAdd(center, TransformToParentVec(bodyTr, lastMain)), 0, 1, 0, 1)
-            dbl(center, VecAdd(center, TransformToParentVec(bodyTr, lastUp)), 1, 0, 0, 1)
-            dbl(lastPos, VecAdd(lastPos, lastNewDir), 1, 1, 0, 1)
-            local tr, mi, ma = GetBodyObb(lastBody)
-            local corners = GetObbCorners(tr, mi, ma)
-            ObbDraw(corners, 0, 1, 0, 1)
-            DrawBodyOutline(lastBody, 1, 1, 0, 1)
-            dbl(lastPos, VecAdd(lastPos, lastVerticalDir), 0, 1, 1, 1)
-            dbl(lastTopStart, lastTopStartExt, 0.5, 0.5, 0, 1)
-            dbl(lastTopEnd, lastTopEndExt, 0.5, 0, 0.5, 1)
-            dbpt(TransformToParentPoint(bodyTr, lastLocalEntry), 1, 1, 0, 1)
-            dbpt(TransformToParentPoint(bodyTr, lastLocalExit), 1, 0, 1, 1)
-            dbl(lastPos, lastPlacementPos, 0.5, 0.5, 1, 1)
-        end
-    end
-    local playerTr = GetPlayerTransform()
-    -- Nothing to do if enough path is already generated
-    local offset = (playerTr.pos[2] + aui.generationDist) - aui.currentPos[2]
-    dbw("genOffset", offset)
-    dbw("buffering", BoolToStr(aui.generationBuffering))
-    if offset < 0 then
-        aui.generationBuffering = true
-        return
-    end
-    -- If buffering is active, do not generate until buffer value is reached
-    if aui.generationBuffering then
-        if offset > aui.generationBufferSize then
-            aui.generationBuffering = false
-        else
-            return
-        end
-    end
-    AlwaysUp.generateNextParkourSection()
-    -- If too many fails, delete previous piece
-    if aui.failedSpawn >= aui.maxFailedSpawn then
-        if aui.lastBody > 0 then
-            Delete(aui.lastBody)
-            aui.currentPos = aui.lastValidCurPos
-            aui.lastDir = aui.lastValidDir
-            aui.failedSpawn = 0
-            aui.lastBody = 0
-        else
-            aui.errorMsg = "Always Up!: An error occured during map generation, please try with another seed"
-            return
-        end
-    end
-end
-
-function AlwaysUp.isLoading()
-    local aui = AlwaysUp.info
-    return aui.generationBuffering == false
-end
-
-function AlwaysUp.getDistUntilNextLoading()
-    local aui = AlwaysUp.info
-    local playerTr = GetPlayerTransform()
-    local offset = (playerTr.pos[2] + aui.generationDist) - aui.currentPos[2]
-    return math.floor(aui.generationBufferSize - offset)
-end
-
-function AlwaysUp.generateNextParkourSection()
-    local aui = AlwaysUp.info
-    -- debug only
-    -- if endFlag == 0 then
-    --     return
-    -- end
-    -- endFlag = endFlag - 1
-    lastPos = aui.currentPos
-    lastLastDir = aui.lastDir
-
-    -- Compute difficulty level based on current height
-    local genAltitude = aui.currentPos[2] - aui.startPos[2]
-    local nbDifficultyLevels = 5
-    local difficultyLevel = 0
-    if genAltitude < 50 then
-        difficultyLevel = 0
-    elseif genAltitude < 100 then
-        difficultyLevel = 1
-    elseif genAltitude < 150 then
-        difficultyLevel = 2
-    elseif genAltitude < 200 then
-        difficultyLevel = 3
-    else
-        difficultyLevel = 4
-    end
-    dbw("level", difficultyLevel)
-
-    -- Spawn random shape for current level
-    local sectionSize = aui.nbModels / nbDifficultyLevels
-    dbw("nbModels", aui.nbModels)
-    dbw("sectionSize", sectionSize)
-    local randIndex = AlwaysUp.getNextRandInt(1, math.ceil(sectionSize * (difficultyLevel+1)))
-    dbw("randIndex", randIndex)
-    local parkourShape, parkourBody, shapeModel = AlwaysUp.spawnFromModel(randIndex)
-    if (parkourShape == nil) or (parkourBody == nil) then
-        dbp("failed to spawn parkour element...")
-        aui.failedSpawn = aui.failedSpawn + 1
-        return
-    end
-    local bodyTr = GetBodyTransform(parkourBody)
-    local shapeLocalTr = GetShapeLocalTransform(parkourShape)
-    lastBody = parkourBody
-    lastShape = parkourShape
-
-    -- Determine main axis and vector: Main axis is the axis with the longest dimension
-    local mainAxis = AlwaysUp.getMainAxis(parkourShape)
-    local mainAxisVec = AlwaysUp.getAxisVec(mainAxis)
-    if AlwaysUp.getNextRandInt(0, 1) == 1 then
-        mainAxisVec = VecScale(mainAxisVec, -1)
-    end
-    local bodyMainAxisVec = TransformToParentVec(shapeLocalTr, mainAxisVec)
-    lastMain = bodyMainAxisVec
-    lastMainShape = mainAxisVec
-    dbw("mainAxis", mainAxis)
-
-    -- Determine shape up axis and rotate shape around main axis to make it up
-    local upAxisVec = AlwaysUp.getUpAxisVec(mainAxisVec)
-    local bodyUpAxisVec = TransformToParentVec(shapeLocalTr, upAxisVec)
-    local upAxis = AlwaysUp.vecToAxis(upAxisVec)
-    bodyTr.rot = QuatAlign(bodyTr.rot, bodyUpAxisVec, Vec(0, 1, 0))
-    SetBodyTransform(parkourBody, bodyTr)
-    lastUp = bodyUpAxisVec
-    lastUpShape = upAxisVec
-    dbw("upAxis", upAxis)
-
-    -- Determine shape horizontal angle offset and direction: Angle more or less around world vertical axis based on difficultyLevel
-    local maxHorizontalAngle = 90
-    local minHorizontalAngle = 30
-    local horizontalAngleIncrement = (maxHorizontalAngle - minHorizontalAngle)/(nbDifficultyLevels-1)
-    local horizontalAngleLimit = minHorizontalAngle + (difficultyLevel * horizontalAngleIncrement)
-    local horizontalAngleOffset = AlwaysUp.getNextRand(-horizontalAngleLimit, horizontalAngleLimit)
-    local newDir = VecRotate(aui.lastDir, "y", horizontalAngleOffset)
-    dbw("horizontalAngle", horizontalAngleOffset)
-
-    -- Determine if the shape can go out of bounds and force angle to 90 if it can
-    local maxPlacementOffset = 14 -- Longest horizontal jump with bluetide
-    local diagonal = shapeModel.radius * 2
-    local tmpPlacementPoint = VecAdd(aui.currentPos, VecResize(aui.lastDir, maxPlacementOffset))
-    local borderDir = VecFlatten(VecSub(tmpPlacementPoint, aui.mapCenter))
-    local outsidePoint = VecAdd(tmpPlacementPoint, VecResize(borderDir, diagonal + maxPlacementOffset))
-    dbw("OutOfBounds", "False")
-    if not AlwaysUp.isInBouds(outsidePoint) then
-        dbw("OutOfBounds", "True")
-        newDir = VecRotate(aui.lastDir, "y", 90)
-        if VecSameDir(newDir, borderDir) then
-            newDir = VecScale(newDir, -1)
-        end
-    end
-
-    -- Set shape horizontal angle
-    bodyTr.rot = QuatAlign(bodyTr.rot, bodyMainAxisVec, newDir)
-    SetBodyTransform(parkourBody, bodyTr)
-    lastNewDir = newDir
-
-    -- Set shape roll rotation around main axis: Bank more or less around mainAxis based on difficultyLevel
-    local maxBankAngle = aui.maxAngleWithoutSlide
-    local bankAngleIncrement = maxBankAngle/(nbDifficultyLevels-1)
-    local bankAngleLimit = difficultyLevel * bankAngleIncrement
-    local bankAngleOffset = AlwaysUp.getNextRand(-bankAngleLimit, bankAngleLimit)
-
-    -- Set shape vertical angle: Angle more or less upward based on difficultyLevel
-    local maxVerticalAngle = aui.maxAngleWithoutSlide
-    local minVerticalAngle = 5
-    local verticalAngleIncrement = (maxVerticalAngle - minVerticalAngle)/nbDifficultyLevels
-    local verticalAngleLimit = minVerticalAngle + ((difficultyLevel+1) * verticalAngleIncrement)
-    local verticalAngleOffset = AlwaysUp.getNextRand(minVerticalAngle, verticalAngleLimit)
-    local worldMainAxisVec = TransformToParentVec(bodyTr, bodyMainAxisVec)
-    local verticalDir = VecInterpAngleTorward(worldMainAxisVec, Vec(0, 1, 0), verticalAngleOffset)
-    lastVerticalDir = verticalDir
-
-    -- Clamp roll angle so that sum of both angles never exceed maxAngleWithoutSlide
-    local absRoll = math.abs(bankAngleOffset)
-    local absPitch = math.abs(verticalAngleOffset)
-    if (absRoll + absPitch) > aui.maxAngleWithoutSlide then
-        local newAbsRoll = aui.maxAngleWithoutSlide - absPitch
-        bankAngleOffset = sign(bankAngleOffset) * newAbsRoll
-    end
-
-    dbw("rollAngle", bankAngleOffset)
-    dbw("verticalAngle", verticalAngleOffset)
-
-    -- Apply roll and vertical angles
-    bodyTr.rot = QuatRotateAroundAxis(bodyTr.rot, bodyMainAxisVec, bankAngleOffset)
-    bodyTr.rot = QuatAlign(bodyTr.rot, bodyMainAxisVec, verticalDir)
-    SetBodyTransform(parkourBody, bodyTr)
-    
-    -- debug only
-    --bodyTr.pos = VecAdd(bodyTr.pos, Vec(0, 100, 0))
-    --SetBodyTransform(parkourBody, bodyTr)
-
-    -- Determine shape entry and exit points: Take center of top face of OBB then pick extreme points on each side of mainAxis
-    local sizeByAxis = AlwaysUp.getShapeSizeByAxis(parkourShape)
-    local lateralAxis = AlwaysUp.getLateralAxis({[mainAxis]=true, [upAxis]=true})
-    local upSize = sizeByAxis[upAxis]
-    local mainSize = sizeByAxis[mainAxis]
-    local lateralSize = sizeByAxis[lateralAxis]
-    local center = AabbGetShapeCenterPos(parkourShape)
-    local worldUpAxisVec = TransformToParentVec(bodyTr, bodyUpAxisVec)
-    local centerTopPos = VecAdd(center, VecResize(worldUpAxisVec, upSize/2))
-    worldMainAxisVec = TransformToParentVec(bodyTr, bodyMainAxisVec)
-    local centerTopStartPos = VecAdd(centerTopPos, VecResize(worldMainAxisVec, -mainSize/2))
-    local centerTopEndPos = VecAdd(centerTopPos, VecResize(worldMainAxisVec, mainSize/2))
-    local centerTopStartExtendedPos = VecAdd(centerTopStartPos, VecResize(worldMainAxisVec, -lateralSize/2))
-    local centerTopEndExtendedPos = VecAdd(centerTopEndPos, VecResize(worldMainAxisVec, lateralSize/2))
-    local hit, entryPos = GetShapeClosestPoint(parkourShape, centerTopStartExtendedPos)
-    if not hit then
-        entryPos = centerTopStartPos
-    end
-    local localEntryPos = TransformToLocalPoint(bodyTr, entryPos)
-    local hit2, exitPos = GetShapeClosestPoint(parkourShape, centerTopEndExtendedPos)
-    if not hit2 then
-        exitPos = centerTopEndPos
-    end
-    local localExitPos = TransformToLocalPoint(bodyTr, exitPos)
-    dbw("size", Vec(sizeByAxis.x, sizeByAxis.y, sizeByAxis.z))
-    dbw("lateralAxis", lateralAxis)
-    dbw("center", center)
-    lastTopStart = centerTopStartPos
-    lastTopEnd = centerTopEndPos
-    lastTopStartExt = centerTopStartExtendedPos
-    lastTopEndExt = centerTopEndExtendedPos
-    lastLocalEntry = localEntryPos
-    lastLocalExit = localExitPos
-    
-    -- Determine shape placement location: aim in lastDir and eventually angle down based on difficultyLevel
-    local placmementOffsetIncrement = maxPlacementOffset/nbDifficultyLevels
-    local placementOffsetLimit = (difficultyLevel+1) * placmementOffsetIncrement
-    local placementOffset = AlwaysUp.getNextRand(0, placementOffsetLimit)
-    local maxPlacementOffsetAngle = 45
-    local placementOffsetAngleIncrement = maxPlacementOffsetAngle/nbDifficultyLevels
-    local placementOffsetAngleLimit = (difficultyLevel+1) * placementOffsetAngleIncrement
-    local placementOffsetAngle = AlwaysUp.getNextRand(0, placementOffsetAngleLimit)
-    local placementDir = VecResize(aui.lastDir, placementOffset)
-    local adjustedPlacementDir = VecInterpAngleTorward(placementDir, Vec(0, -1, 0), placementOffsetAngle)
-    local placementDist = VecLength(adjustedPlacementDir) / math.cos(math.rad(placementOffsetAngle))
-    local finalPlacementDir = VecResize(adjustedPlacementDir, placementDist)
-    local placementPos = VecAdd(aui.currentPos, finalPlacementDir)
-
-    -- Check if placement is lower than highest pos and react in consequences
-    local heightDiff = exitPos[2] - entryPos[2]
-    local isLowPlacement = ((placementPos[2] + heightDiff) < aui.highestPos[2])
-    if isLowPlacement then
-        if aui.lowPlacementAllowed then
-            -- Disable low placement until currentPos went higher than highestPos
-            aui.lowPlacementAllowed = false
-        else
-            -- Only keep forward vec (ignore down angle)
-            placementPos = VecAdd(aui.currentPos, placementDir)
-        end
-    end
-
-    -- Move shape to placement location
-    local movement = VecSub(placementPos, entryPos)
-    bodyTr.pos = VecAdd(bodyTr.pos, movement)
-    SetBodyTransform(parkourBody, bodyTr)
-    dbw("placementOffset", placementOffset)
-    dbw("placementOffsetAngle", placementOffsetAngle)
-    dbw("placementDist", placementDist)
-    lastPlacementPos = placementPos
-
-    -- If shape exit pos somehow ended up out of bounds anyway, delete it and pick another one
-    if not AlwaysUp.isInBouds(TransformToParentPoint(bodyTr, localExitPos)) then
-        Delete(parkourBody)
-        aui.failedSpawn = aui.failedSpawn + 1
-        return
-    end
-
-    -- Check if jump is impossible due to hole in the shape
-    local localUpCenter = VecLerp(localEntryPos,localExitPos,0.5)
-    local jumpCenter = TransformToParentPoint(bodyTr, localUpCenter)
-    local hit3, closestPoint = GetShapeClosestPoint(parkourShape, jumpCenter)
-    if (not hit3) or (VecDist(closestPoint, jumpCenter) > (aui.maxJumpLength / 2)) then
-        -- FIlls the gap with a smaller piece
-        AlwaysUp.fillGap(jumpCenter, bodyTr, randIndex, worldMainAxisVec, worldUpAxisVec)
-    end
-
-    -- Update current pos and last dir
-    aui.lastValidCurPos = aui.currentPos
-    aui.lastValidDir = aui.lastDir
-    aui.currentPos = TransformToParentPoint(bodyTr, localExitPos)
-    if aui.currentPos[2] > aui.highestPos[2] then
-        aui.highestPos = aui.currentPos
-        aui.lowPlacementAllowed = true
-    end
-    aui.lastDir = newDir
-    aui.lastBody = parkourBody
-    aui.failedSpawn = 0
-end
-
-function AlwaysUp.spawnFromModel(index)
-    local aui = AlwaysUp.info
-    local shapeModel = aui.shapeModels[aui.orderedModelIndexes[index]]
-    -- Spawn the new block
-    local jsonShapes = AlwaysUp.getShapeXML(shapeModel)
-    local xmlString = '<prefab version="1.2.0"> \
+#version 2
+local jsonShapes = AlwaysUp.getShapeXML(shapeModel)
+local xmlString = '<prefab version="1.2.0"> \
         <group name="" pos="0.0 0.0 0.0"> \
             <body pos="0.0 0.0 0.0" rot="0.0 0.0 0.0" dynamic="false"> \
                 '..jsonShapes..' \
             </body> \
         </group> \
     </prefab>'
-    local entities = Spawn(xmlString, Transform(aui.currentPos, Quat()), true)
-    -- Find new shapes and body
-    local parkourShape = nil
-    local parkourBody = nil
-    for i=1,#entities do
-        local entity = entities[i]
-        if GetEntityType(entity) == "shape" then
-            parkourShape = entity
-        end
-        if GetEntityType(entity) == "body" then
-            parkourBody = entity
-        end
-    end
-    if (parkourShape ~= nil) and (parkourBody ~= nil) then
-        -- Load shape information
-        AlwaysUp.loadShape(shapeModel, parkourShape)
-    end
-    return parkourShape, parkourBody, shapeModel
-end
+local entities = Spawn(xmlString, Transform(aui.currentPos, Quat()), true)
+local parkourShape = nil
+local parkourBody = nil
 
 function AlwaysUp.getShapeXML(shapeModel)
     local texture = shapeModel.texture
@@ -672,7 +104,6 @@
     }
 end
 
--- Initialize and store a custom sequence of seeded random numbers
 function AlwaysUp.generateRandomSequence(seed, length)
     local aui = AlwaysUp.info
     aui.randSeq = {}
@@ -691,7 +122,6 @@
 
 end
 
--- Get the next stored random number
 function AlwaysUp.getNextRand(min, max)
     local aui = AlwaysUp.info
     aui.randIndex = aui.randIndex + 1
@@ -706,7 +136,6 @@
 
 end
 
--- Get the next stored random number as an integer within range
 function AlwaysUp.getNextRandInt(min, max)
 
     -- local rnd = math.floor(AlwaysUp.getNextRand(min, max+1))
@@ -776,7 +205,7 @@
     local aui = AlwaysUp.info
 
     local isWalking = IsPlayerGrounded()
-    local playerTr = GetPlayerTransform()
+    local playerTr = GetPlayerTransform(playerId)
     local jumpDiagonal = math.sqrt(2) * aui.maxJumpLength
 
     -- Fix initial teleport breaking score validity
@@ -855,13 +284,13 @@
 end
 
 function AlwaysUp.saveBestScore(score)
-    regSetInt(AlwaysUp.getScoreKey(), score)
+    regSetInt(AlwaysUp.getScoreKey(), score, true)
 end
 
 function AlwaysUp.getUniqueMapName()
     local modName = GetString("game.mod")
     local mapName = GetString("game.levelid")
-    if #modName > 0 then
+    if #modName ~= 0 then
         mapName = modName.."-"..mapName
     end
     return mapName
@@ -874,3 +303,4 @@
     end
     return aui.scoreKey
 end
+

```

---

# Migration Report: scripts\debug.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\debug.lua
+++ patched/scripts\debug.lua
@@ -1,13 +1,18 @@
-
+#version 2
 function initDebug()
     db = regGetBool('always_up.debugMode')
 end
 
 function dbw(str, value) if db then DebugWatch(str, value) end end
+
 function dbp(str, newLine) if db then DebugPrint(str .. ternary(newLine, '\n', '')) print(str .. ternary(newLine, '\n', '')) end end
+
 function dbpt(p1, c1, c2, c3, a) if db then DebugCross(p1, c1, c2, c3, a) end end
+
 function dbl(p1, p2, c1, c2, c3, a) if db then DebugLine(p1, p2, c1, c2, c3, a) end end
+
 function dbdd(pos,w,l,r,g,b,a,dt) if db then DrawDot(pos,w,l,r,g,b,a,dt) end end
+
 function ddc(transform, radius, sides, info)
     if db then
         local tr1 = TransformCopy(transform)
@@ -16,6 +21,7 @@
         visual.drawpolygon( tr1, radius, nil, sides, info)
     end
 end
+
 function dds(transform, radius, sides, info)
     if db then
         local tr1 = TransformCopy(transform)
@@ -33,4 +39,5 @@
 
 function debugMod()
     db = regGetBool('always_up.debugMode')
-end+end
+

```

---

# Migration Report: scripts\registry.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\registry.lua
+++ patched/scripts\registry.lua
@@ -1,11 +1,12 @@
+#version 2
 function modReset()
 
     -- Always Up
-    regSetBool('always_up.debugMode'    , false)
-    regSetBool('always_up.noInitialGen' , false)
-    regSetInt('always_up.seed'          , 0)
-    regSetInt('always_up.generationDist', 4)
-    regSetBool('always_up.instaSave'    , false)
+    regSetBool('always_up.debugMode'    , false, true)
+    regSetBool('always_up.noInitialGen' , false, true)
+    regSetInt('always_up.seed'          , 0, true)
+    regSetInt('always_up.generationDist', 4, true)
+    regSetBool('always_up.instaSave'    , false, true)
 
 end
 
@@ -22,43 +23,47 @@
     if getMajorVersion(savedVersion) ~= getMajorVersion(currentVersion) then
         modReset()
     end
-    regSetString('version', currentVersion)
+    regSetString('version', currentVersion, true)
 end
 
 function regGetFloat(path)
     local p = 'savegame.mod.' .. path
     return GetFloat(p)
 end
-function regSetFloat(path, value)
+
+function regSetFloat(path, value, true)
     local p = 'savegame.mod.' .. path
-    SetFloat(p, value)
+    SetFloat(p, value, true)
 end
 
 function regGetInt(path)
     local p = 'savegame.mod.' .. path
     return GetInt(p)
 end
-function regSetInt(path, value)
+
+function regSetInt(path, value, true)
     local p = 'savegame.mod.' .. path
-    SetInt(p, value)
+    SetInt(p, value, true)
 end
 
 function regGetBool(path)
     local p = 'savegame.mod.' .. path
     return GetBool(p)
 end
-function regSetBool(path, value)
+
+function regSetBool(path, value, true)
     local p = 'savegame.mod.' .. path
-    SetBool(p, value)
+    SetBool(p, value, true)
 end
 
 function regGetString(path)
     local p = 'savegame.mod.' .. path
     return GetString(p)
 end
-function regSetString(path, value)
+
+function regSetString(path, value, true)
     local p = 'savegame.mod.' .. path
-    SetString(p, value)
+    SetString(p, value, true)
 end
 
 function regClearKey(path)
@@ -88,14 +93,16 @@
     end
     return nil
 end
+
 function regSet(type, path, value)
     if type == "float" then
-        regSetFloat(path, value)
+        regSetFloat(path, value, true)
     elseif type == "int" then
-        regSetInt(path, value)
+        regSetInt(path, value, true)
     elseif type == "bool" then
-        regSetBool(path, value)
+        regSetBool(path, value, true)
     elseif type == "string" then
-        regSetString(path, value)
+        regSetString(path, value, true)
     end
-end+end
+

```

---

# Migration Report: scripts\shape_utils.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\shape_utils.lua
+++ patched/scripts\shape_utils.lua
@@ -1,273 +1,3 @@
--- TODO: doc
-
--- This should be the mod path to THIS FILE
+#version 2
 local FILENAME = "MOD/scripts/shape_utils.lua"
 
-if ClearKey then -- <script>
-	local function voxscript( parameters )
-		local size = ""
-		local shapedata = ""
-		local palettedata = ""
-		if parameters.palette then
-			local palette = {}
-			for i = 1, #parameters.palette do
-				local p = parameters.palette[i]
-				palette[i] = string.format( "%d/%s/%d/%d/%d/%f/%f/%f/%f/%f", p.index, p.material or "none", math.floor( p.r * 255 ),
-				                            math.floor( p.g * 255 ), math.floor( p.b * 255 ),
-				                            p.a and p.a > 0 and p.a < 1 and 0.5 or 1, p.reflect, p.shiny, p.metal, p.emissive )
-			end
-			palettedata = string.format( "palette=\"%s\"", table.concat( palette, " " ) )
-		end
-		if parameters.shape then
-			local content = {}
-			for i = 1, #parameters.shape do
-				local index = parameters.shape[i]
-				content[i] = string.char( math.floor( index / 16 ) + 65, index % 16 + 65 )
-			end
-			shapedata = string.format( "shape=\"%s\"", table.concat( content, "" ) )
-		end
-		if parameters.size then
-			size = string.format( "size=\"%d %d %d\"", unpack( parameters.size ) )
-		end
-		return string.format( "<voxscript file=\"%s\"><parameters %s %s %s/></voxscript>", FILENAME, size, shapedata,
-		                      palettedata )
-	end
-
-	function CreatePalette( entries )
-		local palettexml = voxscript { palette = entries }
-		return Spawn( palettexml, Transform(), true, false )[1]
-	end
-
-	function SetShapePaletteContent( shape, entries )
-		local palette = CreatePalette( entries )
-		CopyShapePalette( palette, shape )
-		Delete( palette )
-	end
-
-	function SetShapesPaletteContent( shapes, entries )
-		local palette = CreatePalette( entries )
-		for i = 1, #shapes do
-			CopyShapePalette( palette, shapes[i] )
-		end
-		Delete( palette )
-	end
-
-	function PaletteContentEquals(c1, c2)
-		return (c1.material == c2.material)
-			and (c1.r == c2.r)
-			and (c1.g == c2.g)
-			and (c1.b == c2.b)
-			and (c1.a == c2.a)
-			and (c1.reflect == c2.reflect)
-			and (c1.shiny == c2.shiny)
-			and (c1.metal == c2.metal)
-			and (c1.emissive == c2.emissive)
-	end
-
-	function GetShapePaletteContent( shape )
-		local forward = GetShapePalette( shape )
-		local reverse = {}
-		for i = 1, #forward do
-			local mat, r, g, b, a, re, sh, me, em = GetShapeMaterial( shape, forward[i] )
-			local t = {
-				index = forward[i],
-				material = mat,
-				r = r,
-				g = g,
-				b = b,
-				a = a,
-				reflect = re,
-				shiny = sh,
-				metal = me,
-				emissive = em,
-			}
-			forward[i] = t
-			reverse[t.index] = t
-		end
-		return forward, reverse
-	end
-
-	function GetShapesPaletteContent( shapes )
-		local forward = {}
-		local reverse = {}
-		for i = 1, #shapes do
-			local shape = shapes[i]
-			local usedpalette = GetShapePalette( shape )
-			for j = 1, #usedpalette do
-				if not reverse[usedpalette[j]] then
-					local material, r, g, b, a, re, sh, me, em = GetShapeMaterial( shape, usedpalette[j] )
-					local t = {
-						index = usedpalette[j],
-						material = material,
-						r = r,
-						g = g,
-						b = b,
-						a = a,
-						reflect = re,
-						shiny = sh,
-						metal = me,
-						emissive = em,
-					}
-					forward[#forward + 1] = t
-					reverse[usedpalette[j]] = t
-				end
-			end
-		end
-		return forward, reverse
-	end
-
-	function CreateShapeFromContent( content, x2, y2, z2 )
-		if not x2 then
-			content, x2, y2, z2 = unpack( content )
-		end
-		local newdataxml = voxscript { shape = content, size = { x2, y2, z2 } }
-		local newdata = Spawn( newdataxml, Transform(), true, false )[1]
-		SetBrush( "cube", 1, content[1] )
-		DrawShapeBox( newdata, 0, 0, 0, 0, 0, 0 )
-		SetBrush( "cube", 1, content[#content] )
-		DrawShapeBox( newdata, x2 - 1, y2 - 1, z2 - 1, x2 - 1, y2 - 1, z2 - 1 )
-		return newdata
-	end
-
-	function SetShapeContent( shape, content )
-		local x2, y2, z2 = GetShapeSize( shape )
-		if type( content[1] ) == "table" then
-			content, x2, y2, z2 = unpack( content )
-		end
-		local newdata = CreateShapeFromContent( content, x2, y2, z2 )
-		CopyShapeContent( newdata, shape )
-		Delete( newdata )
-	end
-
-	function GetShapeContent( shape )
-		local content = {}
-		local x2, y2, z2 = GetShapeSize( shape )
-		for x = 0, x2 - 1 do
-			for y = 0, y2 - 1 do
-				for z = 0, z2 - 1 do
-					local _, _, _, _, _, index = GetShapeMaterialAtIndex( shape, x, y, z )
-					content[#content + 1] = index
-				end
-			end
-		end
-		return content, x2, y2, z2
-	end
-
-	function CarveShape( shape, carver, offset )
-		-- TODO: batch carving?
-		if type( carver ) == "number" then
-			carver = { GetShapeContent( carver ), GetShapeSize( carver ) }
-		end
-		local oP, oR = Vec( 0, 0, 0 ), Vec( 0, 0, 0 )
-		if offset then
-			if offset.pos then
-				oP = offset.pos
-				oR = Vec( GetQuatEuler( offset.rot ) )
-			else
-				oP = offset
-			end
-		end
-		local original = GetShapeContent( shape )
-		local positive = voxscript { shape = original, size = { GetShapeSize( shape ) } }
-		local negative = type( carver ) == "string" and string.format( [[<vox file="%s"/>]], carver ) or
-			                 voxscript { shape = carver[1], size = { select( 2, unpack( carver ) ) } }
-		local xml = string.format( [[
-			<body dynamic="true">
-				%s
-				<group pos="%f %f %f" rot="%f %f %f">
-					%s
-				</group>
-			</body>
-		]], positive, oP[1], oP[2], oP[3], oR[1], oR[2], oR[3], negative )
-		local body, resultShape, negativeShape = unpack( Spawn( xml, Transform(), false, false ) )
-		CopyShapeContent( resultShape, shape )
-		SetShapeLocalTransform( shape, TransformToParentTransform( GetShapeLocalTransform( shape ),
-		                                                           GetShapeWorldTransform( resultShape ) ) )
-		Delete( body )
-		Delete( resultShape )
-		Delete( negativeShape )
-		return shape
-	end
-
-	function CloneShape( shape )
-		local save = CreateShape()
-		CopyShapeContent( shape, save )
-		local x, y, z, scale = GetShapeSize( shape )
-		local start = GetShapeWorldTransform( shape )
-		ResizeShape( shape, 0, 0, 0, x - 1, y - 1, z + 1 )
-		SetBrush( "cube", 1, 1 )
-		DrawShapeBox( shape, 0, 0, z + 1, 0, 0, z + 1 )
-		local pieces = SplitShape( shape, false )
-		local moved = VecScale( TransformToLocalPoint( GetShapeWorldTransform( shape ), start.pos ), 1 / scale )
-		local mx, my, mz = math.floor( moved[1] + 0.5 ), math.floor( moved[2] + 0.5 ), math.floor( moved[3] + 0.5 )
-		ResizeShape( shape, mx, my, mz, 1, 1, 1 )
-		CopyShapeContent( save, shape )
-		local splitoffset = VecScale( TransformToLocalPoint( GetShapeWorldTransform( pieces[1] ), start.pos ), 1 / scale )
-		local sx, sy, sz = math.floor( splitoffset[1] + 0.5 ), math.floor( splitoffset[2] + 0.5 ),
-							math.floor( splitoffset[3] + 0.5 )
-		ResizeShape( pieces[1], sx, sy, sz, 1, 1, 1 )
-		CopyShapeContent( save, pieces[1] )
-		Delete( save )
-		for i = 2, #pieces do
-			Delete( pieces[i] )
-		end
-		return pieces[1], shape
-	end
-else -- <voxscript>
-	local sx, sy, sz = GetInt( "size", 1, 1, 1 )
-	local shapedata = GetString( "shape" )
-	local palettedata = GetString( "palette" )
-
-	local function getbyte( str, offset )
-		local a, b = string.byte( str, offset, offset + 1 )
-		return (a - 65) * 16 + b - 65
-	end
-
-	function init()
-		if palettedata and palettedata ~= "" then
-			local colors = {}
-			for index, m, r, g, b, a, re, sh, me, em in palettedata:gmatch(
-				                                            "(%d+)/(%w+)/(%d+)/(%d+)/(%d+)/([%d.]+)/([%d.]+)/([%d.]+)/([%d.]+)/([%d.]+)" ) do
-				colors[tonumber( index )] = {
-					m,
-					tonumber( r ) / 255,
-					tonumber( g ) / 255,
-					tonumber( b ) / 255,
-					tonumber( a ),
-					tonumber( re ),
-					tonumber( sh ),
-					tonumber( me ),
-					tonumber( em ),
-				}
-			end
-			for i = 1, 255 do
-				if colors[i] then
-					CreateMaterial( unpack( colors[i] ) )
-				else
-					CreateMaterial( "none" ) -- gaps in the palette can't be left out
-				end
-			end
-			if not shapedata or shapedata == "" then
-				Vox( 0, 0, 0, 0, 0, 0 )
-				for index in pairs( colors ) do
-					Material( index )
-					Box( index - 1, 0, 0, index, 1, 1 )
-				end
-			end
-		end
-		if shapedata and shapedata ~= "" then
-			Vox( 0, 0, 0, 0, 0, 0 )
-			for i = 0, #shapedata / 2 - 1 do
-				local index = getbyte( shapedata, i * 2 + 1 )
-				if index > 0 then
-					Material( index )
-					local x, y, z = math.floor( i / sy / sz ) % sx, math.floor( i / sz ) % sy, i % sz
-					Box( x, y, z, x + 1, y + 1, z + 1 )
-				end
-			end
-			Material( 1 ) -- ensure the shape size is as requested
-			Box( 0, 0, 0, 1, 1, 1 )
-			Box( sx - 1, sy - 1, sz - 1, sx, sy, sz )
-		end
-	end
-end

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
@@ -1,8 +1,4 @@
-------------------------------------------------------------------------------------------------
--- Please don't judge this code too heavily. It is a bit of a hack job but it works :)
-------------------------------------------------------------------------------------------------
-
-
+#version 2
 function uiDrawOptions()
 
     local w = UiWidth()
@@ -49,7 +45,6 @@
     ui.padding.create(padW, padH)
     ui.container.create(contW - title_w, title_h, ui.colors.g2, 1)
 
-
     -- Text: Title
     do UiPush()
 
@@ -75,7 +70,6 @@
         UiFont('bold.ttf', textHeight)
         UiText('By: Geneosis')
 
-
     UiPop() end
 
     -- Button: Exit
@@ -109,7 +103,6 @@
         UiAlign('middle center')
         UiText('X')
 
-
     UiPop() end
 
     ui.padding.create(0, title_w)
@@ -131,7 +124,6 @@
         UiText('Options')
     UiPop() end
 
-
     -- Button: Options reset
     do UiPush()
         ui.padding.create(contW - padW * 4, ((font_heading - font_normal * 1.5)/2))
@@ -161,13 +153,11 @@
 
     UiPop() end
 
-
     -- Options tab content container
     local tabContentH = contH - title_h - options_tabH - options_tabH - padH * 6.5
     ui.padding.create(0, options_tabH)
     ui.container.create(contW - padW*4, tabContentH, ui.colors.g3, 1)
 
-
     -- Tab content
     ui.padding.create(padW, padH2)
     ui.container.create(contW - padW*6, tabContentH - padH*3, ui.colors.g1, 1)
@@ -191,15 +181,6 @@
     UiPop() end
 
 end
-
-
-itemsPerPage = 7
-allItems = {}
-filteredIndexes = {}
-galleryPages = 1
-galleryPage = 1
-currentPageItemsCount = 0
-lastItemsCount = 0
 
 function uiUpdateGalleryItems()
     allItems = {}
@@ -246,14 +227,14 @@
     if galleryPage > galleryPages then
         galleryPage = galleryPages
     end
-    regSetInt("ui.galleryPage", galleryPage)
+    regSetInt("ui.galleryPage", galleryPage, true)
     uiUpdateCurrentPageItemsCount()
 end
 
 function uiUpdateCurrentPageItemsCount()
     currentPageItemsCount = 0
     local nbFilteredItems = #filteredIndexes
-    if nbFilteredItems > 0 then
+    if nbFilteredItems ~= 0 then
         local remain = nbFilteredItems % itemsPerPage
         if (galleryPage < galleryPages) or (remain == 0)then
             currentPageItemsCount = itemsPerPage
@@ -273,154 +254,6 @@
     end
 end
 
-
-options_tabs_render = {
-
-    Game = function()
-
-        do UiPush()
-
-            do UiPush()
-
-                ui.textInput.create('Seed', 'always_up.seed', '', nil, nil, nil, nil, "int")
-                ui.padding.create(0, 60)
-                ui.checkBox.create('Disable preloading', 'always_up.noInitialGen')
-                ui.padding.create(0, 64)
-                ui.slider.create('Generation distance', 'always_up.generationDist', '00m', 1, 10, nil, nil, nil, nil, true)
-                ui.padding.create(0, 40)
-                ui.checkBox.create('Save best score every change (may cause lag spikes)', 'always_up.instaSave')
-                ui.padding.create(0, 64)
-
-            UiPop() end
-
-            do UiPush()
-
-                ui.padding.create(600, 0)
-
-                ui.checkBox.create('Debug Mode', 'always_up.debugMode')
-                ui.padding.create(0, 64)
-
-            UiPop() end
-
-        UiPop() end
-
-    end,
-
-    Score = function()
-
-        do UiPush()
-
-            do UiPush()
-
-                local oldPage = regGetInt("ui.galleryPage")
-                ui.slider.create("Page", "ui.galleryPage", "/"..galleryPages, 1, galleryPages, nil, nil, nil, nil, true)
-                galleryPage = regGetInt("ui.galleryPage")
-                if oldPage ~= galleryPage then
-                    uiUpdateCurrentPageItemsCount()
-                end
-                ui.padding.create(0, 40)
-
-                -- Header
-                UiColor(1,1,1, 1)
-                UiFont('bold.ttf', 32)
-                UiAlign('left middle')
-                
-                do UiPush()
-                    ui.padding.create(1100, 0)
-                    UiText('SEED')
-                UiPop() end
-                do UiPush()
-                    ui.padding.create(400, 0)
-                    UiText('MAP')
-                UiPop() end
-                ui.padding.create(100, 0)
-                UiText('SCORE')
-
-    
-            UiPop() end
-
-            if #filteredIndexes == 0 then
-                local message = ""
-                if #allItems == 0 then
-                    message = "No score saved yet ):"
-                else
-                    message = "No score matches searched words"
-                end
-                do UiPush()
-
-                    ui.padding.create(800, 300)
-
-                    UiFont('regular.ttf', font_normal)
-                    UiColor(0.6,0.6,0.6, 1)
-                    UiAlign('center middle')
-                    UiText(message)
-
-                UiPop() end
-            end
-
-            ui.padding.create(0, 128)
-
-            local voffset = 60
-
-            do UiPush()
-
-                for i=1,itemsPerPage do
-                    uiAddListItem(i)
-                    ui.padding.create(0, voffset)
-                end
-    
-            UiPop() end
-
-        UiPop() end
-        
-    end,
-
-    Info = function()
-
-        UiColor(1,1,1, 1)
-        UiFont('bold.ttf', 32)
-        UiAlign('left middle')
-
-        do UiPush()
-
-            UiFont('bold.ttf', 32)
-            UiText('NOTES')
-            UiFont('regular.ttf', font_normal)
-            ui.padding.create(0, 50)
-            UiText('- This mod generates a procedural parkour challenge on any map', true)
-            UiText('    using the elements already present in the map at startup', true)
-            UiText('', true)
-            UiText('- Initial parkour generation may take some time, please be patient', true)
-            UiText('', true)
-            UiText('- The parkour difficulty increase every 50m of height, up to maximum difficulty at 200m', true)
-            UiText('', true)
-            UiText('- Your objective is to climb as high as possible', true)
-            UiText('', true)
-            UiText('- You are allowed to use any tool from the base game', true)
-            UiText('', true)
-            UiText('- All parkour pieces are destructible (some might require explosives)', true)
-            UiText('', true)
-            UiText('- Your score will be saved for every map and seed combination', true)
-            UiText('', true)
-            UiText('- If your score is greyed out while on the ground, it means the mod thinks you cheated,', true)
-            UiText('    as long as you are in this state your best score won\'t update,', true)
-            UiText('    try to walk to a lower point to get it back on tracks', true)
-            UiText('', true)
-
-        UiPop() end
-
-        do UiPush()
-
-            ui.padding.create(700, 0)
-
-
-        UiPop() end
-        
-    end,
-
-}
-
---- Draw current height and best height at top center
 function uiDrawScores()
 
     UiPush()
@@ -458,40 +291,15 @@
  
 end
 
-
-ui = {}
-
-ui.colors = {
-    white = Vec(1,1,1),
-    g3 = Vec(0.5,0.5,0.5),
-    g2 = Vec(0.35,0.35,0.35),
-    g1 = Vec(0.2,0.2,0.2),
-    black = Vec(0,0,0),
-}
-
-
-
-ui.container = {}
-
 function ui.container.create(w, h, c, a)
     if not c then c = Vec(0.5,0.5,0.5) end
     UiColor(c[1], c[2], c[3], a or 0.5)
     UiRect(w, h)
 end
 
-
-
-ui.padding = {}
-
 function ui.padding.create(w, h)
     UiTranslate(w or 10, h or 10)
 end
-
-
-
-ui.tabView = {}
-
-ui.tabView.tab = {}
 
 function ui.tabView.tab.create(text)
 
@@ -523,10 +331,6 @@
     UiPop() end
 
 end
-
-
-
-ui.slider = {}
 
 function ui.slider.create(title, registryPath, valueText, min, max, w, h, fontSize, inline, intSlider, stringChoices)
 
@@ -586,11 +390,11 @@
     if strSlider then val = stringChoices[floatToInt(val)] end
     if done then
         if strSlider then
-            regSetString(registryPath, val)
+            regSetString(registryPath, val, true)
         elseif intSlider then
-            regSetInt(registryPath, val)
-        else
-            regSetFloat(registryPath, val)
+            regSetInt(registryPath, val, true)
+        else
+            regSetFloat(registryPath, val, true)
         end
     end
 
@@ -610,9 +414,6 @@
     if hasTitle and inline then UiPop() end
 
 end
-
-
-ui.checkBox = {}
 
 function ui.checkBox.create(title, registryPath)
 
@@ -660,13 +461,11 @@
 
     UiButtonImageBox('ui/common/box-outline-6.png', 10,10, 0,0,0, a)
     if UiBlankButton(tglW, tglH) then
-        regSetBool(registryPath, not value)
+        regSetBool(registryPath, not value, true)
         PlaySound(LoadSound('clickdown.ogg'), GetCameraTransform().pos, 1)
     end
 
 end
-
-ui.colorPicker = {}
 
 function ui.colorPicker.create(title, registryPath, w, h, fontSize, useAlpha)
 
@@ -705,8 +504,6 @@
     end
 
 end
-
-ui.button = {}
 
 function ui.button.create(text, textColor, borderColor, bgColor, border, w, h)
     local button = nil
@@ -733,8 +530,6 @@
     return button
 end
 
-ui.imageButton = {}
-
 function ui.imageButton.create(imagePath, borderColor, border, w, h)
     local button = nil
     do UiPush()
@@ -755,9 +550,6 @@
     return button
 end
 
-
-ui.keyBinding = {}
-
 function ui.keyBinding.create(title, registryPath)
 
     local value = regGetString(registryPath)
@@ -782,7 +574,7 @@
         UiColor(0.6,0.6,0.6, 1)
         local keyPressed = InputLastPressedKey()
         if keyPressed ~= "" then
-            regSetString(registryPath, keyPressed)
+            regSetString(registryPath, keyPressed, true)
         end
     else
         text = string.upper(value)
@@ -805,17 +597,14 @@
     UiButtonImageBox('ui/common/box-outline-6.png', 10,10, 0,0,0, a)
     if UiBlankButton(tglW, tglH) then
         if editing then
-            regSetString(registryPath, "")
-        else
-            regSetString(registryPath, "-")
+            regSetString(registryPath, "", true)
+        else
+            regSetString(registryPath, "-", true)
         end
         PlaySound(LoadSound('clickdown.ogg'), GetCameraTransform().pos, 1)
     end
 
 end
-
-
-ui.textInput = {}
 
 function ui.textInput.create(title, registryPath, valueText, min, max, w, h, type, inline)
 
@@ -888,7 +677,7 @@
         end
         value = UiTextInput(value, tiW, tiH)
         if strText then
-            regSetString(registryPath, value)
+            regSetString(registryPath, value, true)
         else
             local valueAccepted = false
             local number = tonumber(value, 10)
@@ -908,13 +697,13 @@
                     if number == math.floor(number) then
                         number = math.floor(number)
                         if (min == nil or number >= min) and (max == nil or number <= max) then
-                            regSetInt(registryPath, number)
+                            regSetInt(registryPath, number, true)
                             valueAccepted = true
                         end
                     end
                 elseif floatText then
                     if (min == nil or number >= min) and (max == nil or number <= max) then
-                        regSetFloat(registryPath, number)
+                        regSetFloat(registryPath, number, true)
                         valueAccepted = true
                     end
                 end
@@ -922,7 +711,7 @@
             if valueAccepted then
                 regClearKey(registryPath..".dirty")
             else
-                regSetString(registryPath..".dirty", value)
+                regSetString(registryPath..".dirty", value, true)
             end
         end
 
@@ -939,40 +728,6 @@
     if hasTitle and inline then UiPop() end
 
 end
-
-
-ui.lineEdit = {}
-ui.lineEdit.editing = {}
-ui.lineEdit.cursorPos = {}
-ui.lineEdit.exitKeys = {
-    ["lmb"] = true,
-    ["mmb"] = true,
-    ["rmb"] = true,
-    ["return"] = true,
-    ["esc"] = true,
-}
-ui.lineEdit.blankKeys = {
-    ["shift"] = true,
-    ["ctrl"] = true,
-    ["alt"] = true,
-    ["home"] = true,
-    ["pgup"] = true,
-    ["pgdown"] = true,
-    ["end"] = true,
-    ["insert"] = true,
-    ["backspace"] = true,
-    ["delete"] = true,
-    ["leftarrow"] = true,
-    ["rightarrow"] = true,
-    ["uparrow"] = true,
-    ["downarrow"] = true,
-}
-ui.lineEdit.miscKeys = {
-    "lmb", "mmb", "rmb", "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/", "*","+", "~",
-    "!", "@", "#", "$","%", "^", "&", "(", ")", "_", "{", "}", "|", ":", '"', "<", ">", "?",
-}
-ui.lineEdit.holdTimers = {}
-ui.lineEdit.textOffsets = {}
 
 function ui.lineEdit.create(title, registryPath, w, h, inline)
 
@@ -1102,7 +857,7 @@
                 ui.lineEdit.cursorPos[registryPath] = ui.lineEdit.cursorPos[registryPath] + 1
             end
         end
-        regSetString(registryPath, value)
+        regSetString(registryPath, value, true)
     else
         UiColor(0.4,0.4,0.4, 1)
     end
@@ -1173,7 +928,6 @@
 
 end
 
-ui.listItem = {}
 function ui.listItem.create(uiIndex)
 
     do UiPush()

```

---

# Migration Report: scripts\umf.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\umf.lua
+++ patched/scripts\umf.lua
@@ -1,7935 +1,6 @@
--- UMF Package umf_complete_c v1.5.3 generated with:
--- build.lua -n "umf_complete_c v1.5.3" dist/umf_complete_c.lua src
---
-local __RUNLATER = {} local UMF_RUNLATER = function(code) __RUNLATER[#__RUNLATER + 1] = code end
-local __UMFLOADED = {["src/util/debug.lua"]=true,["src/core/hook.lua"]=true,["src/util/detouring.lua"]=true,["src/core/hooks_base.lua"]=true,["src/core/hooks_extra.lua"]=true,["src/util/registry.lua"]=true,["src/core/console_backend.lua"]=true,["src/core/_index.lua"]=true,["src/util/config.lua"]=true,["src/util/meta.lua"]=true,["src/util/constraint.lua"]=true,["src/util/resources.lua"]=true,["src/util/timer.lua"]=true,["src/util/visual.lua"]=true,["src/util/xml.lua"]=true,["src/vector/quat.lua"]=true,["src/vector/transform.lua"]=true,["src/vector/vector.lua"]=true,["src/entities/entity.lua"]=true,["src/entities/body.lua"]=true,["src/entities/joint.lua"]=true,["src/entities/light.lua"]=true,["src/entities/location.lua"]=true,["src/entities/player.lua"]=true,["src/entities/screen.lua"]=true,["src/entities/shape.lua"]=true,["src/entities/trigger.lua"]=true,["src/entities/vehicle.lua"]=true,["src/animation/animation.lua"]=true,["src/animation/armature.lua"]=true,["src/tool/tool.lua"]=true,["src/tdui/base.lua"]=true,["src/tdui/image.lua"]=true,["src/tdui/layout.lua"]=true,["src/tdui/panel.lua"]=true,["src/tdui/window.lua"]=true,["src/_index.lua"]=true,} local UMF_SOFTREQUIRE = function(name) return __UMFLOADED[name] end
---src/util/debug.lua
-(function() ----------------
--- Debug Utilities
--- @script util.debug
-util = util or {}
+#version 2
+local __RUNLATER = {}
+local UMF_RUNLATER = function(code) __RUNLATER[#__RUNLATER + 1] = code end
+local __UMFLOADED = {["src/util/debug.lua"]=true,["src/core/hook.lua"]=true,["src/util/detouring.lua"]=true,["src/core/hooks_base.lua"]=true,["src/core/hooks_extra.lua"]=true,["src/util/registry.lua"]=true,["src/core/console_backend.lua"]=true,["src/core/_index.lua"]=true,["src/util/config.lua"]=true,["src/util/meta.lua"]=true,["src/util/constraint.lua"]=true,["src/util/resources.lua"]=true,["src/util/timer.lua"]=true,["src/util/visual.lua"]=true,["src/util/xml.lua"]=true,["src/vector/quat.lua"]=true,["src/vector/transform.lua"]=true,["src/vector/vector.lua"]=true,["src/entities/entity.lua"]=true,["src/entities/body.lua"]=true,["src/entities/joint.lua"]=true,["src/entities/light.lua"]=true,["src/entities/location.lua"]=true,["src/entities/player.lua"]=true,["src/entities/screen.lua"]=true,["src/entities/shape.lua"]=true,["src/entities/trigger.lua"]=true,["src/entities/vehicle.lua"]=true,["src/animation/animation.lua"]=true,["src/animation/armature.lua"]=true,["src/tool/tool.lua"]=true,["src/tdui/base.lua"]=true,["src/tdui/image.lua"]=true,["src/tdui/layout.lua"]=true,["src/tdui/panel.lua"]=true,["src/tdui/window.lua"]=true,["src/_index.lua"]=true,}
+local UMF_SOFTREQUIRE = function(name) return __UMFLOADED[name] end
 
---- Gets the current line of code.
----
----@param level number stack depth
----@return string?
-function util.current_line( level )
-	level = (level or 0) + 3
-	local _, line = pcall( error, "-", level )
-	if line == "-" then
-		_, line = pcall( error, "-", level + 1 )
-		if line == "-" then
-			return
-		end
-		line = "[C]:?"
-	else
----@diagnostic disable-next-line: need-check-nil
-		line = line:sub( 1, -4 )
-	end
-	return line
-end
-
---- Gets the current stacktrack.
----
----@param start? number starting stack depth
----@return table
-function util.stacktrace( start )
-	start = (start or 0) + 3
-	local stack, last = {}, nil
-	for i = start, 32 do
-		local _, line = pcall( error, "-", i )
-		if line == "-" then
-			if last == "-" then
-				break
-			end
-		else
-			if last == "-" then
-				stack[#stack + 1] = "[C]:?"
-			end
----@diagnostic disable-next-line: need-check-nil
-			stack[#stack + 1] = line:sub( 1, -4 )
-		end
-		last = line
-	end
-	return stack
-end
-
- end)();
---src/core/hook.lua
-(function() ----------------
--- Hook library
--- @script core.hook
-
-if hook then
-	return
-end
-
-local hook_table = {}
-local hook_compiled = {}
-
-local function recompile( event )
-	local hooks = {}
-	for k, v in pairs( hook_table[event] ) do
-		hooks[#hooks + 1] = v
-	end
-	hook_compiled[event] = hooks
-end
-
-hook = { table = hook_table }
-
---- Hooks a function to the specified event.
----
----@param event string
----@param identifier any
----@param func function
----@overload fun(event: string, func: function)
-function hook.add( event, identifier, func )
-	assert( type( event ) == "string", "Event must be a string" )
-	if func then
-		assert( identifier ~= nil, "Identifier must not be nil" )
-		assert( type( func ) == "function", "Callback must be a function" )
-	else
-		assert( type( identifier ) == "function", "Callback must be a function" )
-	end
-	hook_table[event] = hook_table[event] or {}
-	hook_table[event][identifier] = func or identifier
-	recompile( event )
-	return identifier
-end
-
---- Removes a hook to an event by its identifier.
----
----@param event string
----@param identifier any
-function hook.remove( event, identifier )
-	assert( type( event ) == "string", "Event must be a string" )
-	assert( identifier ~= nil, "Identifier must not be nil" )
-	if hook_table[event] then
-		hook_table[event][identifier] = nil
-		if next( hook_table[event] ) == nil then
-			hook_table[event] = nil
-			hook_compiled[event] = nil
-		else
-			recompile( event )
-		end
-	end
-end
-
---- Executes all hooks associated to an event.
----
----@param event string
----@return any ...
-function hook.run( event, ... )
-	local hooks = hook_compiled[event]
-	if not hooks then
-		return
-	end
-	for i = 1, #hooks do
-		local a, b, c, d, e = hooks[i]( ... )
-		if a ~= nil then
-			return a, b, c, d, e
-		end
-	end
-end
-
---- Executes all hooks associated to an event with `pcall`.
----
----@param event string
----@return any ...
-function hook.saferun( event, ... )
-	local hooks = hook_compiled[event]
-	if not hooks then
-		return
-	end
-	for i = 1, #hooks do
-		local s, a, b, c, d, e = softassert( pcall( hooks[i], ... ) )
-		if s and a ~= nil then
-			return a, b, c, d, e
-		end
-	end
-end
-
---- Executes all hooks associated to an event with `xpcall`.
---- Prints the stacktrace as a warning.
----
----@param event string
----@return any ...
-function hook.saferun_debug( event, ... )
-	local hooks = hook_compiled[event]
-	if not hooks then
-		return
-	end
-	local args = { ... }
-	for i = 1, #hooks do
-		local s, a, b, c, d, e = xpcall( function()
-			return hooks[i]( unpack( args ) )
-		end, function( err )
-			warning( err, 2 )
-		end )
-		if s and a ~= nil then
-			return a, b, c, d, e
-		end
-	end
-end
-
---- Tests if an event has hooks attached.
----
----@param event string
----@return boolean
-function hook.used( event )
-	return hook_table[event]
-end
-
-
- end)();
---src/util/detouring.lua
-(function() if DETOUR then return end
-
-----------------
--- Detour Utilities
--- @script util.detouring
-local original = {}
-local function call_original( name, ... )
-	local fn = original[name]
-	if fn then
-		return fn( ... )
-	end
-end
-
-local detoured = {}
---- Detours a global function even it gets reassigned afterwards.
----
----@param name string
----@param generator fun(original: function): function
-function DETOUR( name, generator )
-	original[name] = original[name] or rawget( _G, name )
-	detoured[name] = generator( function( ... )
-		return call_original( name, ... )
-	end )
-	rawset( _G, name, nil )
-end
-
-setmetatable( _G, {
-	__index = detoured,
-	__newindex = function( self, k, v )
-		if detoured[k] then
-			original[k] = v
-		else
-			rawset( self, k, v )
-		end
-	end,
-} )
-
- end)();
---src/core/hooks_base.lua
-(function() ----------------
--- Default hooks
--- @script core.hooks_base
-UMF_RUNLATER "UpdateQuickloadPatch()"
-
-local hook = hook
-
-local function checkoriginal( b, ... )
-	if not b then
-		printerror( ... )
-		return
-	end
-	return ...
-end
-
-local function simple_detour( name )
-	local event = "base." .. name
-	DETOUR( name, function( original )
-		return function( ... )
-			hook.saferun( event, ... )
-			return checkoriginal( pcall( original, ... ) )
-		end
-
-	end )
-end
-
-local detours = {
-	"init", -- "base.init" (runs before init())
-	"tick", -- "base.tick" (runs before tick())
-	"update", -- "base.update" (runs before update())
-}
-for i = 1, #detours do
-	simple_detour( detours[i] )
-end
-
---- Tests if a UI element should be drawn.
----
----@param kind string
----@return boolean
-function shoulddraw( kind )
-	return hook.saferun( "api.shoulddraw", kind ) ~= false
-end
-
-DETOUR( "draw", function( original )
-	return function( dt )
-		if shoulddraw( "all" ) then
-			hook.saferun( "base.predraw", dt )
-			if shoulddraw( "original" ) then
-				checkoriginal( pcall( original, dt ) )
-			end
-			hook.saferun( "base.draw", dt )
-		end
-	end
-
-end )
-
-DETOUR( "Command", function( original )
-	return function( cmd, ... )
-		hook.saferun( "base.precmd", cmd, { ... } )
-		local a, b, c, d, e, f = original( cmd, ... )
-		hook.saferun( "base.postcmd", cmd, { ... }, { a, b, c, d, e, f } )
-	end
-
-end )
-
------- QUICKSAVE WORKAROUND -----
--- Quicksaving stores a copy of the global table without functions, so libraries get corrupted on quickload
--- This code prevents this by overriding them back
-
-local savedtypes = { ["function"] = true, ["userdata"] = true, ["thread"] = true }
-local saved
-
-local function searchtable(t, bck)
-	if bck[t] then return end
-	bck[t] = true
-	local rt, dosave = {}, false
-	for k, v in pairs(t) do
-		local vt = type(v)
-		if vt == "table" then
-			local st = searchtable(v, bck)
-			if st then
-				dosave = true
-				rt[k] = st
-			end
-		elseif savedtypes[vt] then
-			dosave = true
-			rt[k] = v
-		end
-	end
-	bck[t] = false
-	if dosave then
-		return rt
-	end
-end
-
-local function restoretable(t, dst)
-	if not t then return end
-	for k, v in pairs(t) do
-		if type(v) == "table" then
-			dst[k] = dst[k] or {}
-			restoretable(v, dst[k])
-		else
-			dst[k] = v
-		end
-	end
-end
-
---- Updates the list of libraries known by the Quickload Patch.
-function UpdateQuickloadPatch()
-	saved = searchtable(_G, {})
-end
-
-DETOUR( "handleCommand", function( original )
-	return function( command, ... )
-		if command == "quickload" then
-			restoretable(saved, _G)
-		end
-		hook.saferun( "base.command." .. command, ... )
-		return original( command, ... )
-	end
-end )
-
---------------------------------
-
-hook.add( "base.tick", "api.firsttick", function()
-	hook.remove( "base.tick", "api.firsttick" )
-	hook.saferun( "api.firsttick" )
-	if type( firsttick ) == "function" then
-		firsttick()
-	end
-end )
-
- end)();
---src/core/hooks_extra.lua
-(function() ----------------
--- @submodule core.hooks_base
-
---- Checks if the player is in a vehicle.
----
----@return boolean
-function IsPlayerInVehicle()
-	return GetBool( "game.player.usevehicle" )
-end
-
-local tool = GetString( "game.player.tool" )
-local invehicle = IsPlayerInVehicle()
-
-local keyboardkeys = { "esc", "up", "down", "left", "right", "space", "interact", "return" }
-for i = 97, 97 + 25 do
-	keyboardkeys[#keyboardkeys + 1] = string.char( i )
-end
-local function checkkeys( func, mousehook, keyhook )
-	if hook.used( keyhook ) and func( "any" ) then
-		for i = 1, #keyboardkeys do
-			if func( keyboardkeys[i] ) then
-				hook.saferun( keyhook, keyboardkeys[i] )
-			end
-		end
-	end
-	if hook.used( mousehook ) then
-		if func( "lmb" ) then
-			hook.saferun( mousehook, "lmb" )
-		end
-		if func( "rmb" ) then
-			hook.saferun( mousehook, "rmb" )
-		end
-	end
-end
-
-local mousekeys = { "lmb", "rmb", "mmb" }
-local logicalinputs = {
-	"up",
-	"down",
-	"left",
-	"right",
-	"interact",
-	"flashlight",
-	"jump",
-	"crouch",
-	"usetool",
-	"grab",
-	"handbrake",
-	"map",
-	"pause",
-	"vehicleraise",
-	"vehiclelower",
-	"vehicleaction",
-	"camerax",
-	"cameray",
-}
-local heldkeys = {}
-
-hook.add( "base.tick", "api.default_hooks", function()
-	if InputLastPressedKey then
-		if hook.used( "api.mouse.pressed" ) or hook.used( "api.mouse.released" ) then
-			for i = 1, #mousekeys do
-				local k = mousekeys[i]
-				if InputPressed( k ) then
-					hook.saferun( "api.mouse.pressed", k )
-				elseif InputReleased( k ) then
-					hook.saferun( "api.mouse.released", k )
-				end
-			end
-		end
-		if hook.used( "api.input.pressed" ) or hook.used( "api.input.released" ) then
-			for i = 1, #logicalinputs do
-				local k = logicalinputs[i]
-				if InputPressed( k ) then
-					hook.saferun( "api.input.pressed", k )
-				elseif InputReleased( k ) then
-					hook.saferun( "api.input.released", k )
-				end
-			end
-		end
-		if hook.used( "api.key.pressed" ) or hook.used( "api.key.released" ) then
-			local lastkey = InputLastPressedKey()
-			if lastkey ~= "" then
-				heldkeys[lastkey] = true
-				hook.saferun( "api.key.pressed", lastkey )
-			end
-			for key in pairs( heldkeys ) do
-				if not InputDown( key ) then
-					heldkeys[key] = nil
-					hook.saferun( "api.key.released", key )
-					break
-				end
-			end
-		end
-		if hook.used( "api.mouse.wheel" ) then
-			local wheel = InputValue( "mousewheel" )
-			if wheel ~= 0 then
-				hook.saferun( "api.mouse.wheel", wheel )
-			end
-		end
-		if hook.used( "api.mouse.move" ) then
-			local mousedx = InputValue( "mousedx" )
-			local mousedy = InputValue( "mousedy" )
-			if mousedx ~= 0 or mousedy ~= 0 then
-				hook.saferun( "api.mouse.move", mousedx, mousedy )
-			end
-		end
-		if hook.used( "api.input.camera" ) then
-			local camerax = InputValue( "camerax" )
-			local cameray = InputValue( "cameray" )
-			if camerax ~= 0 or cameray ~= 0 then
-				hook.saferun( "api.input.camera", camerax, cameray )
-			end
-		end
-	elseif InputPressed then
-		checkkeys( InputPressed, "api.mouse.pressed", "api.key.pressed" )
-		checkkeys( InputReleased, "api.mouse.released", "api.key.released" )
-		local wheel = InputValue( "mousewheel" )
-		if wheel ~= 0 then
-			hook.saferun( "api.mouse.wheel", wheel )
-		end
-		local mousedx = InputValue( "mousedx" )
-		local mousedy = InputValue( "mousedy" )
-		if mousedx ~= 0 or mousedy ~= 0 then
-			hook.saferun( "api.mouse.move", mousedx, mousedy )
-		end
-	end
-
-	local n_invehicle = IsPlayerInVehicle()
-	if invehicle ~= n_invehicle then
-		hook.saferun( n_invehicle and "api.player.enter_vehicle" or "api.player.exit_vehicle",
-		              n_invehicle and GetPlayerVehicle() )
-		invehicle = n_invehicle
-	end
-
-	local n_tool = GetString( "game.player.tool" )
-	if tool ~= n_tool then
-		hook.saferun( "api.player.switch_tool", n_tool, tool )
-		tool = n_tool
-	end
-end )
-
- end)();
---src/util/registry.lua
-(function() ----------------
--- Registry Utilities
--- @script util.registry
-local coreloaded = UMF_SOFTREQUIRE "src/core/_index.lua"
-
-util = util or {}
-
-do
-	local serialize_any, serialize_table
-
-	serialize_table = function( val, bck )
-		if bck[val] then
-			return "nil"
-		end
-		bck[val] = true
-		local entries = {}
-		for k, v in pairs( val ) do
-			entries[#entries + 1] = string.format( "[%s] = %s", serialize_any( k, bck ), serialize_any( v, bck ) )
-		end
-		return string.format( "{%s}", table.concat( entries, "," ) )
-	end
-
-	serialize_any = function( val, bck )
-		local vtype = type( val )
-		if vtype == "table" then
-			return serialize_table( val, bck )
-		elseif vtype == "string" then
-			return string.format( "%q", val )
-		elseif vtype == "function" or vtype == "userdata" then
-			return string.format( "nil --[[%s]]", tostring( val ) )
-		else
-			return tostring( val )
-		end
-	end
-
-	--- Serializes something to a lua-like string.
-	---
-	---@vararg any
-	---@return string
-	function util.serialize( ... )
-		local result = {}
-		for i = 1, select( "#", ... ) do
-			result[i] = serialize_any( select( i, ... ), {} )
-		end
-		return table.concat( result, "," )
-	end
-end
-
---- Unserializes something from a lua-like string.
----
----@param dt string
----@return ...
-function util.unserialize( dt )
-	local fn = loadstring( "return " .. dt )
-	if fn then
-		setfenv( fn, {} )
-		return fn()
-	end
-end
-
-do
-	local function serialize_any( val, bck )
-		local vtype = type( val )
-		if vtype == "table" then
-			if bck[val] then
-				return "{}"
-			end
-			bck[val] = true
-			local len = 0
-			for k, v in pairs( val ) do
-				len = len + 1
-			end
-			local rt = {}
-			if len == #val then
-				for i = 1, #val do
-					rt[i] = serialize_any( val[i], bck )
-				end
-				return string.format( "[%s]", table.concat( rt, "," ) )
-			else
-				for k, v in pairs( val ) do
-					if type( k ) == "string" or type( k ) == "number" then
-						rt[#rt + 1] = string.format( "%s: %s", serialize_any( k, bck ), serialize_any( v, bck ) )
-					end
-				end
-				return string.format( "{%s}", table.concat( rt, "," ) )
-			end
-		elseif vtype == "string" then
-			return string.format( "%q", val )
-		elseif vtype == "function" or vtype == "userdata" or vtype == "nil" then
-			return "null"
-		else
-			return tostring( val )
-		end
-	end
-
-	--- Serializes something to a JSON string.
-	---
-	---@param val any
-	---@return string
-	function util.serializeJSON( val )
-		return serialize_any( val, {} )
-	end
-end
-
---- Creates a buffer shared via the registry.
----
----@param name string
----@param max? number
----@return table
-function util.shared_buffer( name, max )
-	max = max or 64
-	return {
-		_pos_name = name .. ".position",
-		_list_name = name .. ".list.",
-		push = function( self, text )
-			local cpos = GetInt( self._pos_name )
-			SetString( self._list_name .. (cpos % max), text )
-			SetInt( self._pos_name, cpos + 1 )
-		end,
-		len = function( self )
-			return math.min( GetInt( self._pos_name ), max )
-		end,
-		pos = function( self )
-			return GetInt( self._pos_name )
-		end,
-		get = function( self, index )
-			local pos = GetInt( self._pos_name )
-			local len = math.min( pos, max )
-			if index >= len then
-				return
-			end
-			return GetString( self._list_name .. (pos + index - len) % max )
-		end,
-		iterator = function( self )
-			local pos = GetInt( self._pos_name )
-			local len = math.min( pos, max )
-			return function( _, i )
-				i = (i or 0) + 1
-				if i >= len then
-					return
-				end
-				return i, GetString( self._list_name .. (pos + i - len) % max )
-			end
-		end,
-		get_g = function( self, index )
-			return GetString( self._list_name .. (index % max) )
-		end,
-		clear = function( self )
-			SetInt( self._pos_name, 0 )
-			ClearKey( self._list_name:sub( 1, -2 ) )
-		end,
-	}
-end
-
-if coreloaded then
-	--- Creates a channel shared via the registry.
-	---
-	---@param name string Name of the channel.
-	---@param max? number Maximum amount of unread messages in the channel.
-	---@param local_realm? string Name to use to identify the local recipient.
-	---@return table
-	function util.shared_channel( name, max, local_realm )
-		max = max or 64
-		local channel = {
-			_buffer = util.shared_buffer( name, max ),
-			_offset = 0,
-			_hooks = {},
-			_ready_count = 0,
-			_ready = {},
-			broadcast = function( self, ... )
-				return self:send( "", ... )
-			end,
-			send = function( self, realm, ... )
-				self._buffer:push( string.format( ",%s,;%s",
-				                                  (type( realm ) == "table" and table.concat( realm, "," ) or tostring( realm )),
-				                                  util.serialize( ... ) ) )
-			end,
-			listen = function( self, callback )
-				if self._ready[callback] ~= nil then
-					return
-				end
-				self._hooks[#self._hooks + 1] = callback
-				self:ready( callback )
-				return callback
-			end,
-			unlisten = function( self, callback )
-				self:unready( callback )
-				self._ready[callback] = nil
-				for i = 1, #self._hooks do
-					if self._hooks[i] == callback then
-						table.remove( self._hooks, i )
-						return true
-					end
-				end
-			end,
-			ready = function( self, callback )
-				if not self._ready[callback] then
-					self._ready_count = self._ready_count + 1
-					self._ready[callback] = true
-				end
-			end,
-			unready = function( self, callback )
-				if self._ready[callback] then
-					self._ready_count = self._ready_count - 1
-					self._ready[callback] = false
-				end
-			end,
-		}
-		local_realm = "," .. (local_realm or "unknown") .. ","
-		local function receive( ... )
-			for i = 1, #channel._hooks do
-				local f = channel._hooks[i]
-				if channel._ready[f] then
-					f( channel, ... )
-				end
-			end
-		end
-		hook.add( "base.tick", name, function( dt )
-			if channel._ready_count > 0 then
-				local last_pos = channel._buffer:pos()
-				if last_pos > channel._offset then
-					for i = math.max( channel._offset, last_pos - max ), last_pos - 1 do
-						local message = channel._buffer:get_g( i )
-						local start = message:find( ";", 1, true )
-						local realms = message:sub( 1, start - 1 )
-						if realms == ",," or realms:find( local_realm, 1, true ) then
-							receive( util.unserialize( message:sub( start + 1 ) ) )
-							if channel._ready_count <= 0 then
-								channel._offset = i + 1
-								return
-							end
-						end
-					end
-					channel._offset = last_pos
-				end
-			end
-		end )
-		return channel
-	end
-
-	--- Creates an async reader on a channel for coroutines.
-	---
-	---@param channel table Name of the channel.
-	---@return table
-	function util.async_channel( channel )
-		local listener = {
-			_channel = channel,
-			_waiter = nil,
-			read = function( self )
-				self._waiter = coroutine.running()
-				if not self._waiter then
-					error( "async_channel:read() can only be used in a coroutine" )
-				end
-				self._channel:ready( self._handler )
-				return coroutine.yield()
-			end,
-			close = function( self )
-				if self._handler then
-					self._channel:unlisten( self._handler )
-				end
-			end,
-		}
-		listener._handler = listener._channel:listen( function( _, ... )
-			if listener._waiter then
-				local co = listener._waiter
-				listener._waiter = nil
-				listener._channel:unready( listener._handler )
-				return coroutine.resume( co, ... )
-			end
-		end )
-		listener._channel:unready( listener._handler )
-		return listener
-	end
-end
-
-do
-
-	local gets, sets = {}, {}
-
-	--- Registers a type unserializer.
-	---
-	---@param type string
-	---@param callback fun(data: string): any
-	function util.register_unserializer( type, callback )
-		gets[type] = function( key )
-			return callback( GetString( key ) )
-		end
-	end
-
-	if coreloaded then
-		hook.add( "api.newmeta", "api.createunserializer", function( name, meta )
-			gets[name] = function( key )
-				return setmetatable( {}, meta ):__unserialize( GetString( key ) )
-			end
-			sets[name] = function( key, value )
-				return SetString( key, meta.__serialize( value ) )
-			end
-		end )
-	end
-
-	--- Creates a table shared via the registry.
-	---
-	---@param name string
-	---@param base? table
-	---@return table
-	function util.shared_table( name, base )
-		return setmetatable( base or {}, {
-			__index = function( self, k )
-				local key = tostring( k )
-				local newtypekey = string.format( "%s.%s._type", name, key )
-				local newformat = HasKey( newtypekey )
-				local vtype = GetString( newformat and newtypekey or string.format( "%s.%s.type", name, key ) )
-				if vtype == "" then
-					return
-				end
-				return gets[vtype]( string.format( newformat and "%s.%s" or "%s.%s.val", name, key ) )
-			end,
-			__newindex = function( self, k, v )
-				local vtype = type( v )
-				local handler = sets[vtype]
-				if not handler then
-					return
-				end
-				local key = tostring( k )
-				if vtype == "table" then
-					local meta = getmetatable( v )
-					if meta and meta.__serialize and meta.__type then
-						vtype = meta.__type
-						v = meta.__serialize( v )
-						handler = sets.string
-					end
-				end
-				SetString( string.format( "%s.%s._type", name, key ), vtype )
-				handler( string.format( "%s.%s", name, key ), v )
-			end,
-		} )
-	end
-
-	--- Creates a table shared via the registry with a structure.
-	---
-	---@param name string
-	---@param base table
-	---@return table
-	---@overload fun(name: string): fun(base: table): table
-	function util.structured_table( name, base )
-		local function generate( base )
-			local root = {}
-			local keys = {}
-			for k, v in pairs( base ) do
-				local key = name .. "." .. tostring( k )
-				if type( v ) == "table" then
-					if #v == 0 then
-						root[k] = util.structured_table( key, v )
-					else
-						keys[k] = { type = v[1], key = key, default = v[2] }
-					end
-				elseif type( v ) == "string" then
-					keys[k] = { type = v, key = key }
-				else
-					root[k] = v
-				end
-			end
-			return setmetatable( root, {
-				__index = function( self, k )
-					local entry = keys[k]
-					if entry and gets[entry.type] then
-						if HasKey( entry.key ) then
-							return gets[entry.type]( entry.key )
-						else
-							return entry.default
-						end
-					end
-				end,
-				__newindex = function( self, k, v )
-					local entry = keys[k]
-					if entry and sets[entry.type] then
-						if v == nil then
-							ClearKey( entry.key )
-						else
-							sets[entry.type]( entry.key, v )
-						end
-					end
-				end,
-			} )
-		end
-		if type( base ) == "table" then
-			return generate( base )
-		end
-		return generate
-	end
-
-	gets.number = GetFloat
-	gets.integer = GetInt
-	gets.boolean = GetBool
-	gets.string = GetString
-	gets.table = util.shared_table
-
-	sets["nil"] = ClearKey
-	sets.number = SetFloat
-	sets.integer = SetInt
-	sets.boolean = SetBool
-	sets.string = SetString
-	sets.table = function( key, val )
-		local tab = util.shared_table( key )
-		for k, v in pairs( val ) do
-			tab[k] = v
-		end
-	end
-
-end
-
- end)();
---src/core/console_backend.lua
-(function() ----------------
--- Console related functions
--- @script core.console_backend
-
-local console_buffer = util.shared_buffer( "game.console", 128 )
-
--- Console backend --
-
-local function maketext( ... )
-	local text = ""
-	local len = select( "#", ... )
-	for i = 1, len do
-		local s = tostring( select( i, ... ) )
-		if i < len then
-			s = s .. string.rep( " ", 8 - #s % 8 )
-		end
-		text = text .. s
-	end
-	return text
-end
-
-_OLDPRINT = _OLDPRINT or print
---- Prints its arguments in the specified color to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
----
----@param r number
----@param g number
----@param b number
-function printcolor( r, g, b, ... )
-	local text = maketext( ... )
-	console_buffer:push( string.format( "%f;%f;%f;%s", r, g, b, text ) )
-	-- TODO: Use color
-	if PRINTTOSCREEN then
-		DebugPrint( text )
-	end
-	return _OLDPRINT( ... )
-end
-
---- Prints its arguments to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
-function print( ... )
-	printcolor( 1, 1, 1, ... )
-end
-
---- Prints its arguments to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
-function printinfo( ... )
-	printcolor( 0, .6, 1, ... )
-end
-
---- Prints a warning and the current stacktrace to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
----
----@param msg any
----@param level? number
-function warning( msg, level )
-	printcolor( 1, .7, 0, "[WARNING] " .. tostring( msg ) .. "\n  " .. table.concat( util.stacktrace( level or 1 ), "\n  " ) )
-end
-
-printwarning = warning
-
---- Prints its arguments to the console.
---- Also prints to the screen if global `PRINTTOSCREEN` is set to true.
-function printerror( ... )
-	printcolor( 1, .2, 0, ... )
-end
-
---- Clears the UMF console buffer.
-function clearconsole()
-	console_buffer:clear()
-end
-
---- To be used with `pcall`, checks success value and prints the error if necessary.
----
----@generic T
----@param b T
----@return T
----@return any ...
-function softassert( b, ... )
-	if not b then
-		printerror( ... )
-	end
-	return b, ...
-end
-
-function assert( b, msg, ... )
-	if not b then
-		local m = msg or "Assertion failed"
-		warning( m )
-		return error( m, ... )
-	end
-	return b, msg, ...
-end
-
-
- end)();
---src/core/_index.lua
-(function() 
-GLOBAL_CHANNEL = util.shared_channel( "game.umf_global_channel", 128 )
-
- end)();
---src/util/config.lua
-(function() ----------------
--- Config Library
--- @script util.config
-local registryloaded = UMF_SOFTREQUIRE "src/util/registry.lua"
-
-if registryloaded then
-	--- Creates a structured table for the mod config
-	---
-	---@param def table
-	function OptionsKeys( def )
-		return util.structured_table( "savegame.mod", def )
-	end
-end
-
-OptionsMenu = setmetatable( {}, {
-	__call = function( self, def )
-		def.title_size = def.title_size or 50
-		local pos = def.center or 0.5
-		local f = OptionsMenu.Group( def )
-		draw = function()
-			UiPush()
-			UiTranslate( UiWidth() * pos, 60 )
-			UiPush()
-			local fw, fh = f()
-			UiPop()
-			UiTranslate( 0, fh + 20 )
-			UiFont( "regular.ttf", 30 )
-			UiAlign( "center top" )
-			UiButtonImageBox( "ui/common/box-outline-6.png", 6, 6 )
-			if UiTextButton( "Close" ) then
-				Menu()
-			end
-			UiPop()
-		end
-		return f
-	end,
-} )
-
-----------------
--- Organizers --
-----------------
-
---- Groups multiple options together
----
----@param def table
-function OptionsMenu.Group( def )
-	local elements = {}
-	if def.title then
-		elements[#elements + 1] = OptionsMenu.Text( def.title, {
-			size = def.title_size or 40,
-			pad_bottom = def.title_pad or 15,
-			align = def.title_align or "center top",
-		} )
-	end
-	for i = 1, #def do
-		elements[#elements + 1] = def[i]
-	end
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		local mw, mh = 0, 0
-		for i = 1, #elements do
-			UiPush()
-			local w, h = elements[i]()
-			UiPop()
-			UiTranslate( 0, h )
-			mh = mh + h
-			mw = math.max( mw, w )
-		end
-		return mw, mh
-	end
-end
-
-function OptionsMenu.Columns( def )
-	local elements = {}
-	for i = 1, #def do
-		elements[#elements + 1] = def[i]
-	end
-
-	return function()
-		local mw, mh = def.width or UiWidth(), 0
-		UiPush()
-			UiTranslate(mw * ( - 0.5 + 0.5 / #elements ), 0)
-			for i = 1, #elements do
-				UiPush()
-					local _, gh = elements[i]()
-				UiPop()
-				UiTranslate(mw * ( 1 / #elements ), 0)
-				mh = math.max( mh, gh )
-			end
-		UiPop()
-		return mw, mh
-	end
-end
-
---- Text section
----
----@param text string
----@param options? table
-function OptionsMenu.Text( text, options )
-	options = options or {}
-	local size = options.size or 30
-	local align = options.align or "left top"
-	local offset = options.offset or (align:find( "left" ) and -400) or 0
-	local font = options.font or "regular.ttf"
-	local padt = options.pad_top or 0
-	local padb = options.pad_bottom or 5
-	local condition = options.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( offset, padt )
-		UiFont( font, size )
-		UiAlign( align )
-		UiWordWrap( 800 )
-		local tw, th = UiText( text )
-		return tw, th + padt + padb
-	end
-end
-
---- Spacer
----
----@param space number Vertical space
----@param spacew? number Horizontal space
----@param condition? function Condition function to enable this spacer
-function OptionsMenu.Spacer( space, spacew, condition )
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		return spacew or 0, space
-	end
-end
-
-----------------
----- Values ----
-----------------
-
-local function getvalue( id, def, func )
-	local key = "savegame.mod." .. id
-	if HasKey( key ) then
-		return (func or GetString)( key )
-	else
-		return def
-	end
-end
-
-local function setvalue( id, val, func )
-	local key = "savegame.mod." .. id
-	if val ~= nil then
-		(func or SetString)( key, val )
-	else
-		ClearKey( key )
-	end
-end
-
---- Keybind value
----
----@param def table
-function OptionsMenu.Keybind( def )
-	local text = def.name or def.id
-	local size = def.size or 30
-	local padt = def.pad_top or 0
-	local padb = def.pad_bottom or 5
-	local allowmouse = def.allowmouse or false
-	local value = string.upper( getvalue( def.id, def.default ) or "" )
-	if value == "" then
-		value = "<none>"
-	end
-	local pressed = false
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( -4, padt )
-		UiFont( "regular.ttf", size )
-		local fheight = UiFontHeight()
-		UiAlign( "right top" )
-		local lw, lh = UiText( text )
-		UiTranslate( 8, 0 )
-		UiAlign( "left top" )
-		UiColor( 1, 1, 0 )
-		local tempv = value
-		if pressed then
-			tempv = "<press a key>"
-			local k = InputLastPressedKey()
-			if k == "esc" then
-				pressed = false
-			elseif k ~= "" then
-				value = string.upper( k )
-				tempv = value
-				setvalue( def.id, k )
-				pressed = false
-			end
-		end
-		local rw, rh = UiGetTextSize( tempv )
-		if allowmouse then
-			local inrect = UiIsMouseInRect( rw, rh )
-			local mouse = InputPressed( "lmb" ) and "lmb" or InputPressed( "rmb" ) and "rmb" or InputPressed( "mmb" ) and "mmb"
-			if inrect and mouse == "lmb" then
-				pressed = not pressed
-			elseif pressed and mouse then
-				value = string.upper( mouse )
-				tempv = value
-				rw, rh = UiGetTextSize( tempv )
-				setvalue( def.id, mouse )
-				pressed = false
-			end
-			UiTextButton( tempv )
-		elseif UiTextButton( tempv ) then
-			pressed = not pressed
-		end
-		UiTranslate( rw, 0 )
-		if value ~= "<none>" then
-			UiColor( 1, 0, 0 )
-			if UiTextButton( "x" ) then
-				value = "<none>"
-				setvalue( def.id, "" )
-			end
-			UiTranslate( size * 0.8, 0 )
-		end
-		if getvalue( def.id ) then
-			UiColor( 0.5, 0.8, 1 )
-			if UiTextButton( "Reset" ) then
-				value = def.default and string.upper( def.default ) or "<none>"
-				setvalue( def.id )
-			end
-		end
-		return lw + 8 + rw, fheight + padt + padb
-	end
-end
-
---- Slider value
----
----@param def table
-function OptionsMenu.Slider( def )
-	local text = def.name or def.id
-	local size = def.size or 30
-	local padt = def.pad_top or 0
-	local padb = def.pad_bottom or 5
-	local min = def.min or 0
-	local max = def.max or 100
-	local range = max - min
-	local getter = def.getter or GetFloat
-	local setter = def.setter or SetFloat
-	local value = getvalue( def.id, def.default, getter )
-	local formatter = def.formatter
-	local format = string.format( "%%.%df", math.max( 0, math.floor( math.log10( 1000 / range ) ) ) )
-	local step = def.step
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( -4, padt )
-		UiFont( "regular.ttf", size )
-		local fheight = UiFontHeight()
-		UiAlign( "right top" )
-		local lw, lh = UiText( text )
-		UiTranslate( 16, lh / 2 )
-		UiAlign( "left middle" )
-		UiColor( 1, 1, 0.5 )
-		UiRect( 200, 2 )
-		UiTranslate( -8, 0 )
-		local prev = value
-		value = UiSlider( "ui/common/dot.png", "x", (value - min) * 200 / range, 0, 200 ) * range / 200 + min
-		if step then
-			value = math.floor( value / step + 0.5 ) * step
-		end
-		UiTranslate( 216, 0 )
-		UiText( formatter and formatter( value ) or string.format( format, value ) )
-		if value ~= prev then
-			setvalue( def.id, value, setter )
-		end
-		return lw + 224, fheight + padt + padb
-	end
-end
-
---- Toggle value
----
----@param def table
-function OptionsMenu.Toggle( def )
-	local text = def.name or def.id
-	local size = def.size or 30
-	local padt = def.pad_top or 0
-	local padb = def.pad_bottom or 5
-	local value = getvalue( def.id, def.default, GetBool )
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( -4, padt )
-		UiFont( "regular.ttf", size )
-		local fheight = UiFontHeight()
-		UiAlign( "right top" )
-		local lw, lh = UiText( text )
-		UiTranslate( 8, 0 )
-		UiAlign( "left top" )
-		UiColor( 1, 1, 0 )
-		if UiTextButton( value and "Enabled" or "Disabled" ) then
-			value = not value
-			setvalue( def.id, value, SetBool )
-		end
-		return lw + 100, fheight + padt + padb
-	end
-end
-
-local opened_color
---- Color value
----
----@param def table
-function OptionsMenu.Color( def )
-	local text = def.name or def.id
-	local size = def.size or 30
-	local padt = def.pad_top or 0
-	local padb = def.pad_bottom or 5
-	local value = getvalue( def.id, def.default, GetString )
-	local open = false
-	local condition = def.condition
-	return function()
-		if condition and not condition() then
-			return 0, 0
-		end
-		UiTranslate( -4, padt )
-		UiFont( "regular.ttf", size )
-		local fheight = UiFontHeight()
-		UiAlign( "right top" )
-		local lw, lh = UiText( text )
-		UiTranslate( 8, 0 )
-		UiAlign( "left top" )
-		local val = getvalue( def.id )
-		local r, g, b = (val or def.default):match("([%d.]+);([%d.]+);([%d.]+)")
-		r, g, b = tonumber(r) or 1, tonumber(g) or 1, tonumber(b) or 1
-		UiPush()
-			UiColor( r, g, b )
-			UiRect( size, size )
-		UiPop()
-		if val then
-			UiPush()
-				UiTranslate( size + 8, 0 )
-				UiColor( 0.5, 0.8, 1 )
-				if UiTextButton( "Reset" ) then
-					value = def.default
-					setvalue( def.id )
-				end
-			UiPop()
-		end
-		if UiBlankButton( size, size ) then
-			if opened_color == def.id then
-				opened_color = nil
-			else
-				opened_color = def.id
-			end
-			open = not open
-		end
-		if opened_color == def.id then
-			fheight = fheight + size + 8
-			UiTranslate(-4, 6 + size * 1.5)
-			UiAlign( "center middle" )
-			UiPush()
-				UiTranslate(0, 0)
-				UiScale(100/64, size/64)
-				UiTranslate(-64 - 12*size/64, 0)
-				UiColor( 1, 0, 0 )
-				UiImage("ui/common/hgradient-right-64.png")
-				UiTranslate(64 + 12*size/64, 0)
-				UiColor( 0, 1, 0 )
-				UiImage("ui/common/hgradient-right-64.png")
-				UiTranslate(64 + 12*size/64, 0)
-				UiColor( 0, 0, 1 )
-				UiImage("ui/common/hgradient-right-64.png")
-			UiPop()
-			UiPush()
-				UiScale(2,30/size)
-				UiTranslate(-25 - 56, 0)
-				r = UiSlider( "ui/hud/meterline.png", "x", r*50, 0, 50 ) / 50
-				UiTranslate(56, 0)
-				g = UiSlider( "ui/hud/meterline.png", "x", g*50, 0, 50 ) / 50
-				UiTranslate(56, 0)
-				b = UiSlider( "ui/hud/meterline.png", "x", b*50, 0, 50 ) / 50
-			UiPop()
-			value = string.format("%f;%f;%f", r, g, b)
-			setvalue( def.id, value, SetString )
-		end
-		return lw + 100, fheight + padt + padb
-	end
-end
- end)();
---src/util/meta.lua
-(function() ----------------
--- Metatable Utilities
--- @script util.meta
-local coreloaded = UMF_SOFTREQUIRE "src/core/_index.lua"
-
-local registered_meta = {}
-local reverse_meta = {}
-
---- Defines a new metatable type.
----
----@param name string
----@param parent? string
----@return table
-function global_metatable( name, parent, usecomputed )
-	local meta = registered_meta[name]
-	if meta then
-		if not parent and not usecomputed then
-			return meta
-		end
-	else
-		meta = {}
-		meta.__index = meta
-		meta.__type = name
-		registered_meta[name] = meta
-		reverse_meta[meta] = name
-		if coreloaded then
-			hook.saferun( "api.newmeta", name, meta )
-		end
-	end
-	local newindex = rawset
-	if usecomputed then
-		local computed = {}
-		meta._C = computed
-		meta.__index = function( self, k )
-			local c = computed[k]
-			if c then
-				return c( self )
-			end
-			return meta[k]
-		end
-		meta.__newindex = function( self, k, v )
-			local c = computed[k]
-			if c then
-				return c( self, true, v )
-			end
-			return newindex( self, k, v )
-		end
-	end
-	if parent then
-		local parent_meta = global_metatable( parent )
-		if parent_meta.__newindex then
-			newindex = parent_meta.__newindex
-			if not meta.__newindex then
-				meta.__newindex = newindex
-			end
-		end
-		setmetatable( meta, { __index = parent_meta.__index } )
-	end
-	return meta
-end
-
---- Gets an existing metatable.
----
----@param name string
----@return table?
-function find_global_metatable( name )
-	if not name then
-		return
-	end
-	if type( name ) == "table" then
-		return reverse_meta[name]
-	end
-	return registered_meta[name]
-end
-
-local function findmeta( src, found )
-	if found[src] then
-		return
-	end
-	found[src] = true
-	local res
-	for k, v in pairs( src ) do
-		if type( v ) == "table" then
-			local dt
-			local m = getmetatable( v )
-			if m then
-				local name = reverse_meta[m]
-				if name then
-					dt = {}
-					dt[1] = name
-				end
-			end
-			local sub = findmeta( v, found )
-			if sub then
-				dt = dt or {}
-				dt[2] = sub
-			end
-			if dt then
-				res = res or {}
-				res[k] = dt
-			end
-		end
-	end
-	return res
-end
-
-function instantiate_global_metatable( name, base )
-	local t = base or {}
-	t.__UMF_GLOBAL_METATYPE = name
-	local meta = find_global_metatable( name )
-	if meta then
-		setmetatable( t, meta )
-		if meta._C then
-			for k, f in pairs( meta._C ) do
-				local v = rawget( t, k )
-				if v ~= nil then
-					rawset( t, k, nil )
-					f( t, v )
-				end
-			end
-		end
-	end
-	return t
-end
-
-local function restoremeta( t, explored )
-	if explored[t] then return end
-	explored[t] = true
-	for _, v in pairs( t ) do
-		if type( v ) == "table" then
-			local meta_type = rawget( v, "__UMF_GLOBAL_METATYPE" )
-			if meta_type then
-				setmetatable( v, global_metatable( meta_type ) )
-			end
-			restoremeta( v, explored )
-		end
-	end
-end
-
-function restore_global_metatables()
-	restoremeta( _G, {} )
-end
-
-if coreloaded then
-	hook.add( "base.command.quickload", "api.metatables.restore", function()
-		restore_global_metatables()
-	end )
-end
- end)();
---src/util/constraint.lua
-(function() ----------------
--- Constraint Utilities
--- @script util.constraint
-
-if not GetEntityHandle then
-	GetEntityHandle = function( handle )
-		return handle
-	end
-end
-
-constraint = {}
-_UMFConstraints = {}
-local solvers = {}
-
-function constraint.RunUpdate( dt )
-	local offset = 0
-	for i = 1, #_UMFConstraints do
-		local v = _UMFConstraints[i + offset]
-		if v.joint and IsJointBroken( v.joint ) then
-			table.remove( _UMFConstraints, i + offset )
-			offset = offset - 1
-		else
-			local result = { c = v }
-			for j = 1, #v.solvers do
-				local s = v.solvers[j]
-				solvers[s.type]( s, result )
-			end
-			if result.angvel then
-				local l = VecLength( result.angvel )
-				ConstrainAngularVelocity( v.parent, v.child, VecScale( result.angvel, 1 / l ), l * 10, 0, v.max_aimp )
-			end
-		end
-	end
-end
-
-local coreloaded = UMF_SOFTREQUIRE "src/core/_index.lua"
-if coreloaded then
-	hook.add( "base.update", "umf.constraint", constraint.RunUpdate )
-end
-
-local function find_index( t, v )
-	for i = 1, #t do
-		if t[i] == v then
-			return i
-		end
-	end
-end
-
-function constraint.Relative( val, body )
-	if type( val ) == "table" and val.handle or type( val ) == "number" then
-		body = val
-		val = nil
-	end
-	if type( val ) == "table" and val.body then
-		body = val.body
-		val = val.val
-	end
-	return { body = GetEntityHandle( body or 0 ), val = val }
-end
-
-local function resolve_point( relative_val )
-	return TransformToParentPoint( GetBodyTransform( relative_val.body ), relative_val.val )
-end
-
-local function resolve_axis( relative_val )
-	return TransformToParentVec( GetBodyTransform( relative_val.body ), relative_val.val )
-end
-
-local function resolve_orientation( relative_val )
-	return TransformToParentTransform( GetBodyTransform( relative_val.body ),
-	                                   Transform( Vec(), relative_val.val or Quat() ) )
-end
-
-local function resolve_transform( relative_val )
-	return TransformToParentTransform( GetBodyTransform( relative_val.body ), relative_val.val )
-end
-
-local constraint_meta = global_metatable( "constraint" )
-
-function constraint.New( parent, child, joint )
-	return instantiate_global_metatable( "constraint", {
-		parent = GetEntityHandle( parent ),
-		child = GetEntityHandle( child ),
-		joint = GetEntityHandle( joint ),
-		solvers = {},
-		tmp = {},
-		active = false,
-	} )
-end
-
-function constraint_meta:Rebuild()
-	if not self.active then
-		return
-	end
-	local index = self.lastbuild and find_index( _UMFConstraints, self.lastbuild ) or (#_UMFConstraints + 1)
-	local c = {
-		parent = self.parent,
-		child = self.child,
-		joint = self.joint,
-		solvers = {},
-		max_aimp = self.max_aimp or math.huge,
-		max_vimp = self.max_vimp or math.huge,
-	}
-	for i = 1, #self.solvers do
-		c.solvers[i] = self.solvers[i]:Build() or { type = "none" }
-	end
-	self.lastbuild = c
-	_UMFConstraints[index] = c
-end
-
-function constraint_meta:Activate()
-	self.active = true
-	self:Rebuild()
-	return self
-end
-
-local colors = { { 1, 0, 0 }, { 0, 1, 0 }, { 0, 0, 1 }, { 0, 1, 1 }, { 1, 0, 1 }, { 1, 1, 0 }, { 1, 1, 1 } }
-function constraint_meta:DrawDebug( c )
-	c = c or GetBodyTransform( self.child ).pos
-	for i = 1, #self.solvers do
-		local col = colors[(i - 1) % #colors + 1]
-		self.solvers[i]:DrawDebug( c, col[1], col[2], col[3] )
-	end
-end
-
-function constraint_meta:LimitAngularVelocity( maxangvel )
-	if self.tmp.asolver then
-		self.tmp.asolver.max_avel = maxangvel
-	else
-		self.tmp.max_avel = maxangvel
-	end
-	return self
-end
-
-function constraint_meta:LimitAngularImpulse( maxangimpulse )
-	self.max_aimp = maxangimpulse
-	return self
-end
-
-function constraint_meta:LimitVelocity( maxvel )
-	if self.tmp.vsolver then
-		self.tmp.vsolver.max_vel = maxvel
-	else
-		self.tmp.max_vel = maxvel
-	end
-	return self
-end
-
-function constraint_meta:LimitImpulse( maximpulse )
-	self.max_vimp = maximpulse
-	return self
-end
-
---------------------------------
---         Solver Base        --
---------------------------------
-
-local solver_meta = global_metatable( "constraint_solver" )
-
-function solver_meta:Build()
-end
-function solver_meta:DrawDebug()
-end
-
-function solvers:none()
-end
-
---------------------------------
---    Rotation Axis Solvers   --
---------------------------------
-
-function constraint_meta:ConstrainRotationAxis( axis, body )
-	self.tmp.vsolver = nil
-	self.tmp.asolver = nil
-	self.tmp.axis = constraint.Relative( axis, body )
-	return self
-end
-
-local solver_ra_sphere_meta = global_metatable( "constraint_ra_sphere_solver", "constraint_solver" )
-
-function constraint_meta:OnSphere( quat, body )
-	local s = instantiate_global_metatable( "constraint_ra_sphere_solver", {} )
-	s.axis = self.tmp.axis
-	s.quat = constraint.Relative( quat, body )
-	s.max_avel = self.tmp.max_avel
-	self.tmp.vsolver = nil
-	self.tmp.asolver = s
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-function constraint_meta:AboveLatitude( min )
-	self.tmp.asolver.min_lat = min
-	return self
-end
-
-function constraint_meta:BelowLatitude( max )
-	self.tmp.asolver.max_lat = max
-	return self
-end
-
-function constraint_meta:WithinLatitudes( min, max )
-	return self:AboveLatitude( min ):BelowLatitude( max )
-end
-
-function constraint_meta:WithinLongitudes( min, max )
-	self.tmp.asolver.min_lng = min
-	self.tmp.asolver.max_lng = max
-	return self
-end
-
-function solver_ra_sphere_meta:DrawDebug( c, r, g, b )
-	local tr = resolve_orientation( self.quat )
-	tr.pos = c
-	local axis = VecNormalize( resolve_axis( self.axis ) )
-
-	local start_lng = self.min_lng or 0
-	local len_lng = self.max_lng and (start_lng - self.max_lng) % 360
-	if self.min_lat then
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec( 0, math.sin( math.rad( self.min_lat ) ), 0 ) ) ),
-		                    math.cos( math.rad( self.min_lat ) ), -start_lng, 40, { arc = len_lng, r = r, g = g, b = b } )
-	end
-	if self.max_lat then
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec( 0, math.sin( math.rad( self.max_lat ) ), 0 ) ) ),
-		                    math.cos( math.rad( self.max_lat ) ), -start_lng, 40, { arc = len_lng, r = r, g = g, b = b } )
-	end
-	if self.min_lng then
-		local start_lat = self.min_lat or 360
-		local len_lat = start_lat - (self.max_lat or 0)
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec(), QuatEuler( 0, 180 - self.min_lng, 90 ) ) ), 1,
-		                    180 - start_lat, 20, { arc = len_lat, r = r, g = g, b = b } )
-		visual.drawpolygon( TransformToParentTransform( tr, Transform( Vec(), QuatEuler( 0, 180 - self.max_lng, 90 ) ) ), 1,
-		                    180 - start_lat, 20, { arc = len_lat, r = r, g = g, b = b } )
-	end
-
-	DrawLine( tr.pos, VecAdd( tr.pos, axis ), r, g, b )
-end
-
-function solver_ra_sphere_meta:Build()
-	local quat = constraint.Relative( self.quat )
-	local lng
-	if self.min_lng then
-		local mid = (self.max_lng + self.min_lng) / 2
-		if self.max_lng < self.min_lng then
-			mid = mid + 180
-		end
-		lng = math.acos( math.cos( math.rad( self.min_lng - mid ) ) )
-		quat.val = QuatRotateQuat( QuatAxisAngle( QuatRotateVec( quat.val or Quat(), Vec( 0, 1, 0 ) ), -mid ),
-		                           quat.val or Quat() )
-	end
-	local axis = constraint.Relative( self.axis )
-	axis.val = VecNormalize( axis.val )
-	return {
-		type = "ra_sphere",
-		axis = axis,
-		quat = quat,
-		lng = lng,
-		min_lat = self.min_lat and math.rad( self.min_lat ) or nil,
-		max_lat = self.max_lat and math.rad( self.max_lat ) or nil,
-		max_avel = self.max_avel,
-	}
-end
-
-function solvers:ra_sphere( result )
-	local axis = resolve_axis( self.axis )
-	local tr = resolve_orientation( self.quat )
-	local local_axis = TransformToLocalVec( tr, axis )
-	local resv
-	local lat = math.asin( local_axis[2] )
-	if self.min_lat and lat < self.min_lat then
-		local c = VecNormalize( VecCross( Vec( 0, -1, 0 ), local_axis ) )
-		resv = VecScale( c, lat - self.min_lat )
-	elseif self.max_lat and lat > self.max_lat then
-		local c = VecNormalize( VecCross( Vec( 0, -1, 0 ), local_axis ) )
-		resv = VecScale( c, lat - self.max_lat )
-	end
-	if self.lng then
-		local l = math.sqrt( local_axis[1] ^ 2 + local_axis[3] ^ 2 )
-		if l > 0.05 then
-			local n = math.acos( local_axis[3] / l ) - self.lng
-			if n < 0 then
-				local c = VecNormalize( VecCross( VecCross( Vec( 0, 1, 0 ), local_axis ), local_axis ) )
-				resv = VecAdd( resv, VecScale( c, local_axis[1] > 0 and -n or n ) )
-				-- local c = VecNormalize( VecCross( Vec( 0, 0, -1 ), local_axis ) )
-				-- resv = VecAdd( resv, VecScale( c, -n ) )
-			end
-		end
-	end
-	if resv then
-		if self.max_avel then
-			local len = VecLength( resv )
-			if len > self.max_avel then
-				resv = VecScale( resv, self.max_avel / len )
-			end
-		end
-		result.angvel = VecAdd( result.angvel, TransformToParentVec( tr, resv ) )
-	end
-end
-
---------------------------------
---     Orientation Solvers    --
---------------------------------
-
-function constraint_meta:ConstrainOrientation( quat, body )
-	self.tmp.vsolver = nil
-	self.tmp.asolver = nil
-	self.tmp.quat = constraint.Relative( quat, body )
-	return self
-end
-
-local solver_quat_quat_meta = global_metatable( "constraint_quat_quat_solver", "constraint_solver" )
-
-function constraint_meta:ToOrientation( quat, body )
-	local s = instantiate_global_metatable( "constraint_quat_quat_solver", {} )
-	s.quat1 = self.tmp.quat
-	s.quat2 = constraint.Relative( quat, body )
-	s.max_avel = self.tmp.max_avel
-	self.tmp.vsolver = nil
-	self.tmp.asolver = s
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-local cdirections = { Vec( 1, 0, 0 ), Vec( 0, 1, 0 ), Vec( 0, 0, 1 ) }
-function solver_quat_quat_meta:DrawDebug( c, r, g, b )
-	local tr1 = resolve_orientation( self.quat1 )
-	tr1.pos = c
-	local tr2 = resolve_orientation( self.quat2 )
-	tr2.pos = c
-	for i = 1, #cdirections do
-		local dir = cdirections[i]
-		local p1 = TransformToParentPoint( tr1, dir )
-		local p2 = TransformToParentPoint( tr2, dir )
-		DrawLine( tr1.pos, p1, r, g, b )
-		DrawLine( tr1.pos, p2, r, g, b )
-		DrawLine( p1, p2, r, g, b )
-	end
-end
-
-function solver_quat_quat_meta:Build()
-	return { type = "quat_quat", quat1 = self.quat1, quat2 = self.quat2, max_avel = self.max_avel or math.huge }
-end
-
-function solvers:quat_quat( result )
-	ConstrainOrientation( result.c.child, result.c.parent, resolve_orientation( self.quat1 ).rot,
-	                      resolve_orientation( self.quat2 ).rot, self.max_avel, result.c.max_aimp )
-end
-
---------------------------------
---      Position Solvers      --
---------------------------------
-
-function constraint_meta:ConstrainPoint( point, body )
-	self.tmp.vsolver = nil
-	self.tmp.asolver = nil
-	self.tmp.point = constraint.Relative( point, body )
-	return self
-end
-
-local solver_point_point_meta = global_metatable( "constraint_point_point_solver", "constraint_solver" )
-
-function constraint_meta:ToPoint( point, body )
-	local s = instantiate_global_metatable( "constraint_point_point_solver", {} )
-	s.point1 = self.tmp.point
-	s.point2 = constraint.Relative( point, body )
-	s.max_vel = self.tmp.max_vel
-	self.tmp.vsolver = s
-	self.tmp.asolver = nil
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-function solver_point_point_meta:DrawDebug( c, r, g, b )
-	local point1 = resolve_point( self.point1 )
-	local point2 = resolve_point( self.point2 )
-	DebugCross( point1, r, g, b )
-	DebugCross( point2, r, g, b )
-	DrawLine( point1, point2, r, g, b )
-end
-
-function solver_point_point_meta:Build()
-	return { type = "point_point", point1 = self.point1, point2 = self.point2, max_vel = self.max_vel or math.huge }
-end
-
-function solvers:point_point( result )
-	ConstrainPosition( result.c.child, result.c.parent, resolve_point( self.point1 ), resolve_point( self.point2 ),
-	                   self.max_vel, result.c.max_vimp )
-end
-
-local solver_point_space_meta = global_metatable( "constraint_point_space_solver", "constraint_solver" )
-
-function constraint_meta:ToSpace( transform, body )
-	local s = instantiate_global_metatable( "constraint_point_space_solver", {} )
-	s.point = self.tmp.point
-	s.transform = constraint.Relative( transform, body )
-	s.max_vel = self.tmp.max_vel
-	s.constraints = {}
-	self.tmp.vsolver = s
-	self.tmp.asolver = nil
-	self.solvers[#self.solvers + 1] = s
-	return self
-end
-
-function constraint_meta:WithinBox( center, min, max )
-	local rcenter = constraint.Relative( self.tmp.vsolver.transform )
-	rcenter.val = TransformToParentTransform( rcenter.val, center )
-	table.insert( self.tmp.vsolver.constraints, { type = "box", center = rcenter, min = min, max = max } )
-	return self
-end
-
-function constraint_meta:WithinSphere( center, radius )
-	local rcenter = constraint.Relative( self.tmp.vsolver.transform )
-	rcenter.val = TransformToParentPoint( rcenter.val, center )
-	table.insert( self.tmp.vsolver.constraints, { type = "sphere", center = rcenter, radius = radius } )
-	return self
-end
-
-function constraint_meta:AbovePlane( transform )
-	local rcenter = constraint.Relative( self.tmp.vsolver.transform )
-	rcenter.val = TransformToParentTransform( rcenter.val, transform )
-	table.insert( self.tmp.vsolver.constraints, { type = "plane", center = rcenter } )
-	return self
-end
-
-function constraint_meta:AlongPath( points, radius )
-	local rcenter = constraint.Relative( self.tmp.vsolver.transform )
-	table.insert( self.tmp.vsolver.constraints, { type = "path", center = rcenter, points = points, radius = radius or 0.01 } )
-	return self
-end
-
-
-function solver_point_space_meta:DrawDebug( c, r, g, b )
-	local point = resolve_point( self.point )
-	for i = 1, #self.constraints do
-		local c = self.constraints[i]
-		if c.type == "plane" then
-			local tr = resolve_transform( c.center )
-			local lp = TransformToLocalPoint( tr, point )
-			lp[2] = 0
-			tr.pos = TransformToParentPoint( tr, lp )
-			visual.drawpolygon( tr, 1.414, 45, 4, { r = r, g = g, b = b } )
-		elseif c.type == "box" then
-			local tr = resolve_transform( c.center )
-			visual.drawbox( tr, c.min, c.max, { r = r, g = g, b = b } )
-		elseif c.type == "sphere" then
-			local tr = Transform( resolve_point( c.center ), Quat() )
-			visual.drawwiresphere( tr, c.radius, 32, { r = r, g = g, b = b } )
-		elseif c.type == "path" then
-			local tr = resolve_transform( c.center )
-			for j = 1, #c.points - 1 do
-				local p1 = TransformToParentPoint( tr, c.points[j] )
-				local p2 = TransformToParentPoint( tr, c.points[j + 1] )
-				visual.drawline( nil, p1, p2, { r = r, g = g, b = b } )
-			end
-		end
-	end
-end
-
-function solver_point_space_meta:Build()
-	local consts = {}
-	for i = 1, #self.constraints do
-		local c = self.constraints[i]
-		if c.type == "box" then
-			local rcenter = constraint.Relative( c.center )
-			rcenter.val.pos = TransformToParentPoint( rcenter.val, VecScale( VecAdd( c.min, c.max ), 0.5 ) )
-			consts[i] = { type = "box", center = rcenter, size = VecScale( VecSub( c.max, c.min ), 0.5 ) }
-		else
-			consts[i] = c
-		end
-	end
-	return { type = "point_space", point = self.point, constraints = consts, max_vel = self.max_vel or math.huge }
-end
-
-local function segment_dist(a, b, p)
-	local s = VecSub(b, a)
-	local da = VecSub(p, a)
-	local dot = VecDot(s, da)
-	if dot < 0 then
-		return VecLength(da), a
-	else
-		local ds = s[1]^2 + s[2]^2 + s[3]^2
-		if dot > ds then
-			return VecLength(VecSub(p, b)), b
-		else
-			local f = dot/ds
-			local lp = VecAdd(a, VecScale(s, f))
-			return VecLength(VecSub(lp, p)), lp
-		end
-	end
-end
-
-function solvers:point_space( result )
-	local point = resolve_point( self.point )
-	local resv
-	for i = 1, #self.constraints do
-		local c = self.constraints[i]
-		if c.type == "plane" then
-			local tr = resolve_transform( c.center )
-			local lp = TransformToLocalPoint( tr, point )
-			if lp[2] < 0 then
-				resv = VecAdd( resv, TransformToParentVec( tr, Vec( 0, lp[2], 0 ) ) )
-			end
-		elseif c.type == "box" then
-			local tr = resolve_transform( c.center )
-			local lp = TransformToLocalPoint( tr, point )
-			local sx, sy, sz = c.size[1], c.size[2], c.size[3]
-			local nlp = Vec( lp[1] < -sx and lp[1] + sx or lp[1] > sx and lp[1] - sx or 0,
-			                 lp[2] < -sy and lp[2] + sy or lp[2] > sy and lp[2] - sy or 0,
-			                 lp[3] < -sz and lp[3] + sz or lp[3] > sz and lp[3] - sz or 0 )
-			if nlp[1] ~= 0 or nlp[2] ~= 0 or nlp[3] ~= 0 then
-				resv = VecAdd( resv, TransformToParentVec( tr, nlp ) )
-			end
-		elseif c.type == "sphere" then
-			local center = resolve_point( c.center )
-			local diff = VecSub( point, center )
-			local len = VecLength( diff )
-			if len > c.radius then
-				resv = VecAdd( resv, VecScale( diff, (len - c.radius) / len ) )
-			end
-		elseif c.type == "path" then
-			local ci, cd, cp = nil, math.huge, nil
-			local tr = resolve_transform( c.center )
-			local lp = TransformToLocalPoint( tr, point )
-			if not c.last_known then
-				for j = 1, #c.points - 1 do
-					local d, p = segment_dist( c.points[j], c.points[j + 1], lp )
-					if d < cd then
-						ci, cd, cp = j, d, p
-					end
-				end
-			else
-				--TODO: optimize for known previous location
-			end
-			local center = TransformToParentPoint( tr, cp )
-			local diff = VecSub( point, center )
-			local len = VecLength( diff )
-			if len > c.radius then
-				resv = VecAdd( resv, VecScale( diff, (len - c.radius) / len ) )
-			end
-			--c.last_known = ci
-		end
-	end
-	if resv then
-		local len = VecLength( resv )
-		resv = VecScale( resv, 1 / len )
-		if self.max_vel and len > self.max_vel then
-			len = self.max_vel
-		end
-		ConstrainVelocity( result.c.parent, result.c.child, point, resv, len * 10, 0, result.c.max_vimp )
-	end
-end
-
- end)();
---src/util/resources.lua
-(function() ----------------
--- Resources Utilities
--- @script util.resources
-
-util = util or {}
-
-local mod
-do
-	local stack = util.stacktrace()
-	local function findmods( file )
-		local matches = {}
-		while file and #file > 0 do
-			matches[#matches + 1] = file
-			file = file:match( "^(.-)/[^/]*$" )
-		end
-
-		local found
-		for _, key in ipairs( ListKeys( "mods.available" ) ) do
-			local path = GetString( "mods.available." .. key .. ".path" )
-			for _, subpath in ipairs( matches ) do
-				if path:sub( -#subpath ) == subpath then
-					if found then
-						return
-					end
-					found = key
-					break
-				end
-			end
-		end
-		return found
-	end
-	for i = 1, #stack do
-		if stack[i] ~= "[C]:?" then
-			local t = stack[i]:match( "%[string \"%.%.%.(.*)\"%]:%d+" ) or stack[i]:match( "%.%.%.(.*):%d+" )
-			if t then
-				local found = findmods( t )
-				if found then
-					mod = found
-					MOD = found
-					break
-				end
-			end
-		end
-	end
-end
-
---- Resolves a given mod path to an absolute path.
----
----@param path string
----@return string path Absolute path
-function util.resolve_path( path )
-	-- TODO: support relative paths (relative to the current file)
-	-- TODO: return multiple matches if applicable
-	local replaced, n = path:gsub( "^MOD/", GetString( "mods.available." .. mod .. ".path" ) .. "/" )
-	if n == 0 then
-		replaced, n = path:gsub( "^LEVEL/", GetString( "game.levelpath" ):sub( 1, -5 ) .. "/" )
-	end
-	if n == 0 then
-		replaced, n = path:gsub( "^MODS/([^/]+)", function( mod )
-			return GetString( "mods.available." .. mod .. ".path" )
-		end )
-	end
-	if n == 0 then
-		return path
-	end
-	return replaced
-end
-
---- Load a lua file from its mod path.
----
----@param path string
----@return function?
----@return string? error_message
-function util.load_lua_resource( path )
-	return loadfile( util.resolve_path( path ) )
-end
-
- end)();
---src/util/timer.lua
-(function() ----------------
--- Timer Utilities
---
---              WARNING
---   Timers are reset on quickload!
--- Keep this in mind if you use them.
---
--- @script util.timer
-
-timer = {}
-timer._backlog = {}
-
-local backlog = timer._backlog
-
-local function sortedinsert( tab, val )
-	for i = #tab, 1, -1 do
-		if val.time < tab[i].time then
-			tab[i + 1] = val
-			return
-		end
-		tab[i + 1] = tab[i]
-	end
-	tab[1] = val
-end
-
-local diff = GetTime() -- In certain realms, GetTime() is not 0 right away
-
---- Creates a simple timer to execute code in a specified amount of time.
----
----@param time number
----@param callback function
-function timer.simple( time, callback )
-	sortedinsert( backlog, { time = GetTime() + time - diff, callback = callback } )
-end
-
---- Creates a time to execute a function in the future
----
----@param id any
----@param interval number
----@param iterations number
----@param callback function
-function timer.create( id, interval, iterations, callback )
-	sortedinsert( backlog, {
-		id = id,
-		time = GetTime() + interval - diff,
-		interval = interval,
-		callback = callback,
-		runsleft = iterations - 1,
-	} )
-end
-
---- Waits a specified amount of time in a coroutine.
----
----@param time number
-function timer.wait( time )
-	local co = coroutine.running()
-	if not co then
-		error( "timer.wait() can only be used in a coroutine" )
-	end
-	timer.simple( time, function()
-		coroutine.resume( co )
-	end )
-	return coroutine.yield()
-end
-
-local function find( id )
-	for i = 1, #backlog do
-		if backlog[i].id == id then
-			return i, backlog[i]
-		end
-	end
-end
-
---- Gets the amount of time left of a named timer.
----
----@param id any
----@return number
-function timer.time_left( id )
-	local index, entry = find( id )
-	if entry then
-		return entry.time - GetTime()
-	end
-	return -1
-end
-
---- Gets the number of iterations left on a named timer.
----
----@param id any
----@return number
-function timer.iterations_left( id )
-	local index, entry = find( id )
-	if entry then
-		return entry.runsleft + 1
-	end
-	return -1
-end
-
---- Removes a named timer.
----
----@param id any
-function timer.remove( id )
-	local index, entry = find( id )
-	if index then
-		table.remove( backlog, index )
-	end
-end
-
-hook.add( "base.tick", "framework.timer", function( dt )
-	diff = 0
-	local now = GetTime()
-	while #backlog > 0 do
-		local first = backlog[#backlog]
-		if first.time > now then
-			break
-		end
-		backlog[#backlog] = nil
-		first.callback()
-		if first.runsleft and first.runsleft > 0 then
-			first.runsleft = first.runsleft - 1
-			first.time = first.time + first.interval
-			sortedinsert( backlog, first )
-		end
-	end
-end )
-
- end)();
---src/util/visual.lua
-(function() ----------------
--- Visual Utilities
--- @script util.visual
-visual = {}
-degreeToRadian = math.pi / 180
-COLOR_WHITE = { r = 255 / 255, g = 255 / 255, b = 255 / 255, a = 255 / 255 }
-COLOR_BLACK = { r = 0, g = 0, b = 0, a = 255 / 255 }
-COLOR_RED = { r = 255 / 255, g = 0, b = 0, a = 255 / 255 }
-COLOR_ORANGE = { r = 255 / 255, g = 128 / 255, b = 0, a = 255 / 255 }
-COLOR_YELLOW = { r = 255 / 255, g = 255 / 255, b = 0, a = 255 / 255 }
-COLOR_GREEN = { r = 0, g = 255 / 255, b = 0, a = 255 / 255 }
-COLOR_CYAN = { r = 0, g = 255 / 255, b = 128 / 255, a = 255 / 255 }
-COLOR_AQUA = { r = 0, g = 255 / 255, b = 255 / 255, a = 255 / 255 }
-COLOR_BLUE = { r = 0, g = 0, b = 255 / 255, a = 255 / 255 }
-COLOR_VIOLET = { r = 128 / 255, g = 0, b = 255 / 255, a = 255 / 255 }
-COLOR_PINK = { r = 255 / 255, g = 0, b = 255 / 255, a = 255 / 255 }
-
-if DrawSprite then
-	function visual.huergb( p, q, t )
-		if t < 0 then
-			t = t + 1
-		end
-		if t > 1 then
-			t = t - 1
-		end
-		if t < 1 / 6 then
-			return p + (q - p) * 6 * t
-		end
-		if t < 1 / 2 then
-			return q
-		end
-		if t < 2 / 3 then
-			return p + (q - p) * (2 / 3 - t) * 6
-		end
-		return p
-	end
-
-	--- Converts hue, saturation, and light to RGB.
-	---
-	---@param h number
-	---@param s number
-	---@param l number
-	---@return number[]
-	function visual.hslrgb( h, s, l )
-		local r, g, b
-
-		if s == 0 then
-			r = l
-			g = l
-			b = l
-		else
-			local huergb = visual.huergb
-
-			local q = l < .5 and l * (1 + s) or l + s - l * s
-			local p = 2 * l - q
-
-			r = huergb( p, q, h + 1 / 3 )
-			g = huergb( p, q, h )
-			b = huergb( p, q, h - 1 / 3 )
-
-		end
-		return Vec( r, g, b )
-	end
-
-	--- Draws a sprite facing the camera.
-	---
-	---@param sprite number
-	---@param source vector
-	---@param radius number
-	---@param info table
-	function visual.drawsprite( sprite, source, radius, info )
-		local r, g, b, a
-		local writeZ, additive = true, false
-		local target = GetCameraTransform().pos
-		local DrawFunction = DrawSprite
-
-		radius = radius or 1
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			target = info.target or target
-			if info.writeZ ~= nil then
-				writeZ = info.writeZ
-			end
-			if info.additive ~= nil then
-				additive = info.additive
-			end
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or DrawFunction
-		end
-
-		DrawFunction( sprite, Transform( source, QuatLookAt( source, target ) ), radius, radius, r, g, b, a, writeZ, additive )
-	end
-
-	--- Draws sprites facing the camera.
-	---
-	---@param sprites number[]
-	---@param sources vector[]
-	---@param radius number
-	---@param info table
-	function visual.drawsprites( sprites, sources, radius, info )
-		sprites = type( sprites ) ~= "table" and { sprites } or sprites
-
-		for i = 1, #sprites do
-			for j = 1, #sources do
-				visual.drawsprite( sprites[i], sources[j], radius, info )
-			end
-		end
-	end
-
-	--- Draws a line using a sprite.
-	---
-	---@param sprite number
-	---@param source vector
-	---@param destination vector
-	---@param info table
-	function visual.drawline( sprite, source, destination, info )
-		local r, g, b, a
-		local writeZ, additive = true, false
-		local target = GetCameraTransform().pos
-		local DrawFunction = DrawLine
-		local width = 0.03
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			width = info.width or width
-			target = info.target or target
-			if info.writeZ ~= nil then
-				writeZ = info.writeZ
-			end
-			if info.additive ~= nil then
-				additive = info.additive
-			end
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		if sprite then
-			local middle = VecScale( VecAdd( source, destination ), .5 )
-			local len = VecLength( VecSub( source, destination ) )
-			local transform = Transform( middle, QuatRotateQuat( QuatLookAt( source, destination ), QuatEuler( -90, 0, 0 ) ) )
-			local target_local = TransformToLocalPoint( transform, target )
-			target_local[2] = 0
-			local trlook = Transform( nil, QuatLookAt( target_local, nil ) )
-			if info and info.turn then
-				trlook.rot = QuatRotateQuat(trlook.rot, QuatEuler(0,0,90))
-				width, len = len, width
-			end
-			local transform_fixed = TransformToParentTransform( transform, trlook )
-
-			DrawSprite( sprite, transform_fixed, width, len, r, g, b, a, writeZ, additive )
-		else
-			DrawFunction( source, destination, r, g, b, a );
-		end
-	end
-
-	--- Draws lines using a sprite.
-	---
-	---@param sprites number[] | number
-	---@param sources vector[]
-	---@param connect boolean
-	---@param info table
-	function visual.drawlines( sprites, sources, connect, info )
-		sprites = type( sprites ) ~= "table" and { sprites } or sprites
-
-		for i = 1, #sprites do
-			local sourceCount = #sources
-
-			for j = 1, sourceCount - 1 do
-				visual.drawline( sprites[i], sources[j], sources[j + 1], info )
-			end
-
-			if connect then
-				visual.drawline( sprites[i], sources[1], sources[sourceCount], info )
-			end
-		end
-	end
-
-	--- Draws a debug axis.
-	---
-	---@param transform transform
-	---@param quat? quaternion
-	---@param radius number
-	---@param writeZ boolean
-	function visual.drawaxis( transform, quat, radius, writeZ )
-		local DrawFunction = writeZ and DrawLine or DebugLine
-
-		if not transform.pos then
-			transform = Transform( transform, quat or QUAT_ZERO )
-		end
-		radius = radius or 1
-
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( radius, 0, 0 ) ), 1, 0, 0 )
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, radius, 0 ) ), 0, 1, 0 )
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, 0, radius ) ), 0, 0, 1 )
-	end
-
-	--- Draws a polygon.
-	---
-	---@param transform transform
-	---@param radius number
-	---@param rotation number
-	---@param sides number
-	---@param info table
-	function visual.drawpolygon( transform, radius, rotation, sides, info )
-		sides = sides or 4
-		radius = radius or 1
-
-		local offset, interval = math.rad( rotation or 0 ), 2 * math.pi / sides
-		local arc = false
-		local r, g, b, a = 1, 1, 1, 1
-		local DrawFunction = DrawLine
-
-		if info then
-			r = info.r or r
-			g = info.g or g
-			b = info.b or b
-			a = info.a or a
-			if info.arc then
-				arc = true
-				interval = interval * info.arc / 360
-			end
-			DrawFunction = info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		local points = {}
-		for i = 0, sides - 1 do
-			points[i + 1] = TransformToParentPoint( transform, Vec( math.sin( offset + i * interval ) * radius, 0,
-			                                                        math.cos( offset + i * interval ) * radius ) )
-			if i > 0 then
-				DrawFunction( points[i], points[i + 1], r, g, b, a )
-			end
-		end
-		if arc then
-			points[#points + 1] = TransformToParentPoint( transform, Vec( math.sin( offset + sides * interval ) * radius, 0,
-			                                                              math.cos( offset + sides * interval ) * radius ) )
-			DrawFunction( points[#points - 1], points[#points], r, g, b, a )
-		else
-			DrawFunction( points[#points], points[1], r, g, b, a )
-		end
-
-		return points
-	end
-
-	--- Draws a 3D box.
-	---
-	---@param transform transform
-	---@param min vector
-	---@param max vector
-	---@param info table
-	function visual.drawbox( transform, min, max, info )
-		local r, g, b, a
-		local DrawFunction = DrawLine
-		local points = {
-			TransformToParentPoint( transform, Vec( min[1], min[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], min[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( min[1], max[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], max[2], min[3] ) ),
-			TransformToParentPoint( transform, Vec( min[1], min[2], max[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], min[2], max[3] ) ),
-			TransformToParentPoint( transform, Vec( min[1], max[2], max[3] ) ),
-			TransformToParentPoint( transform, Vec( max[1], max[2], max[3] ) ),
-		}
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		DrawFunction( points[1], points[2], r, g, b, a )
-		DrawFunction( points[1], points[3], r, g, b, a )
-		DrawFunction( points[1], points[5], r, g, b, a )
-		DrawFunction( points[4], points[3], r, g, b, a )
-		DrawFunction( points[4], points[2], r, g, b, a )
-		DrawFunction( points[4], points[8], r, g, b, a )
-		DrawFunction( points[6], points[5], r, g, b, a )
-		DrawFunction( points[6], points[8], r, g, b, a )
-		DrawFunction( points[6], points[2], r, g, b, a )
-		DrawFunction( points[7], points[8], r, g, b, a )
-		DrawFunction( points[7], points[5], r, g, b, a )
-		DrawFunction( points[7], points[3], r, g, b, a )
-
-		return points
-	end
-
-	--- Draws a prism.
-	---
-	---@param transform transform
-	---@param radius number
-	---@param depth number
-	---@param rotation number
-	---@param sides number
-	---@param info table
-	function visual.drawprism( transform, radius, depth, rotation, sides, info )
-		local points = {}
-		local iteration = 1
-		local pow, sqrt, sin, cos = math.pow, math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-
-		radius = sqrt( 2 * pow( radius, 2 ) ) or sqrt( 2 )
-		depth = depth or 1
-		rotation = rotation or 0
-		sides = sides or 4
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		for v = 0, 360, 360 / sides do
-			points[iteration] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius, depth,
-			                                                            cos( (v + rotation) * degreeToRadian ) * radius ) )
-			points[iteration + 1] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius,
-			                                                                -depth,
-			                                                                cos( (v + rotation) * degreeToRadian ) * radius ) )
-			if iteration > 2 then
-				DrawFunction( points[iteration], points[iteration + 1], r, g, b, a )
-				DrawFunction( points[iteration - 2], points[iteration], r, g, b, a )
-				DrawFunction( points[iteration - 1], points[iteration + 1], r, g, b, a )
-			end
-			iteration = iteration + 2
-		end
-
-		return points
-	end
-
-	--- Draws a sphere.
-	---
-	---@param transform transform
-	---@param radius number
-	---@param rotation number
-	---@param samples number
-	---@param info table
-	function visual.drawsphere( transform, radius, rotation, samples, info )
-		local points = {}
-		local sqrt, sin, cos = math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-
-		radius = radius or 1
-		rotation = rotation or 0
-		samples = samples or 100
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		-- Converted from python to lua, see original code https://stackoverflow.com/a/26127012/5459461
-		local points = {}
-		for i = 0, samples do
-			local y = 1 - (i / (samples - 1)) * 2
-			local rad = sqrt( 1 - y * y )
-			local theta = 2.399963229728653 * i
-
-			local x = cos( theta ) * rad
-			local z = sin( theta ) * rad
-			local point = TransformToParentPoint( Transform( transform.pos,
-			                                                 QuatRotateQuat( transform.rot, QuatEuler( 0, rotation, 0 ) ) ),
-			                                      Vec( x * radius, y * radius, z * radius ) )
-
-			DrawFunction( point, VecAdd( point, Vec( 0, .01, 0 ) ), r, g, b, a )
-			points[i + 1] = point
-		end
-
-		return points
-	end
-
-	--- Draws a wireframe sphere.
-	---
-	---@param transform transform
-	---@param radius number
-	---@param points number
-	---@param info table
-	function visual.drawwiresphere( transform, radius, points, info )
-		radius = radius or 1
-		points = points or 32
-		if not info or not info.nolines then
-			local tr_r = TransformToParentTransform( transform, Transform( Vec(), QuatEuler( 90, 0, 0 ) ) )
-			local tr_f = TransformToParentTransform( transform, Transform( Vec(), QuatEuler( 0, 0, 90 ) ) )
-			visual.drawpolygon( transform, radius, 0, points, info )
-			visual.drawpolygon( tr_r, radius, 0, points, info )
-			visual.drawpolygon( tr_f, radius, 0, points, info )
-		end
-
-		local cam = info and info.target or GetCameraTransform().pos
-		local diff = VecSub( transform.pos, cam )
-		local len = VecLength( diff )
-		if len < radius then
-			return
-		end
-		local a = math.pi / 2 - math.asin( radius / len )
-		local vtr = Transform( VecAdd( transform.pos, VecScale( diff, -math.cos( a ) / len ) ),
-		                       QuatRotateQuat( QuatLookAt( transform.pos, cam ), QuatEuler( 90, 0, 0 ) ) )
-		visual.drawpolygon( vtr, radius * math.sin( a ), 0, points, info )
-	end
-end
-
- end)();
---src/util/xml.lua
-(function() ----------------
--- XML Utilities
--- @script util.xml
-
----@class XMLNode
----@field __call fun(children: XMLNode[]): XMLNode
----@field attributes table<string, string|nil> | nil
----@field children XMLNode[] | nil
----@field type string
-local xml_meta
-xml_meta = global_metatable( "xmlnode" )
-
---- Defines an XML node.
----
----@param type string
----@return fun(attributes: table<string, string|nil>): XMLNode
-XMLTag = function( type )
-	return function( attributes )
-		return instantiate_global_metatable( "xmlnode", { type = type, attributes = attributes } )
-	end
-end
-
---- Parses XML from a string.
----
----@param xml string
----@return XMLNode
-ParseXML = function( xml )
-	local pos = 1
-	local function skipw()
-		local next = xml:find( "[^ \t\n]", pos )
-		if not next then
-			return false
-		end
-		pos = next
-		return true
-	end
-	local function expect( pattern, noskip )
-		if not noskip then
-			if not skipw() then
-				return false
-			end
-		end
-		local s, e = xml:find( pattern, pos )
-		if not s then
-			return false
-		end
-		local pre = pos
-		pos = e + 1
-		return xml:match( pattern, pre )
-	end
-
-	local readtag, readattribute, readstring
-
-	local rt = { n = "\n", t = "\t", r = "\r", ["0"] = "\0", ["\\"] = "\\", ["\""] = "\"" }
-	readstring = function()
-		local c = expect( "^([\"'])" )
-		if not c then
-			return false
-		end
-		local start = pos
-		while true do
-			local s = assert( xml:find( "[\\" .. c .. "]", pos ), "Invalid string" )
-			if xml:sub( s, s ) == "\\" then
-				pos = s + 2
-			else
-				pos = s + 1
-				break
-			end
-		end
-		return xml:sub( start, pos - 2 ):gsub( "\\(.)", rt )
-	end
-
-	readattribute = function()
-		local name = expect( "^([%d%w_]+)" )
-		if not name then
-			return false
-		end
-		if expect( "^=" ) then
-			return name, assert( readstring() )
-		else
-			return name, "1"
-		end
-	end
-
-	readtag = function()
-		local save = pos
-		if not expect( "^<" ) then
-			return false
-		end
-
-		local type = expect( "^([%d%w_]+)" )
-		if not type then
-			pos = save
-			return false
-		end
-		skipw()
-
-		local attributes = {}
-		repeat
-			local attr, val = readattribute()
-			if attr then
-				attributes[attr] = val
-			end
-		until not attr
-
-		local children = {}
-		if not expect( "^/>" ) then
-			assert( expect( "^>" ) )
-			repeat
-				local child = readtag()
-				if child then
-					children[#children + 1] = child
-				end
-			until not child
-			assert( expect( "^</" ) and expect( "^" .. type ) and expect( "^>" ) )
-		end
-
-		return XMLTag( type )( attributes )( children )
-	end
-
-	return readtag()
-end
-
----@type XMLNode
-
----@return XMLNode self
-function xml_meta:__call( children )
-	self.children = children
-	return self
-end
-
---- Renders this node into an XML string.
----
----@return string
-function xml_meta:Render()
-	local attr = ""
-	if self.attributes then
-		for name, val in pairs( self.attributes ) do
-			attr = string.format( "%s %s=%q", attr, name, val )
-		end
-	end
-	local children = {}
-	if self.children then
-		for i = 1, #self.children do
-			children[i] = self.children[i]:Render()
-		end
-	end
-	return string.format( "<%s%s>%s</%s>", self.type, attr, table.concat( children, "" ), self.type )
-end
-
- end)();
---src/vector/quat.lua
-(function() ----------------
--- Quaternion class and related functions
--- @script vector.quat
-
-local vector_meta = global_metatable( "vector" )
-
----@class quaternion
----@field [1] number
----@field [2] number
----@field [3] number
----@field [4] number
-
----@class Quaternion: quaternion
-local quat_meta
-quat_meta = global_metatable( "quaternion" )
-
---- Tests if the parameter is a quaternion.
----
----@param q any
----@return boolean
-function IsQuaternion( q )
-	return type( q ) == "table" and type( q[1] ) == "number" and type( q[2] ) == "number" and type( q[3] ) == "number" and
-		       type( q[4] ) == "number"
-end
-
---- Makes the parameter quat into a quaternion.
----
----@param q number[]
----@return Quaternion q
-function MakeQuaternion( q )
-	return instantiate_global_metatable( "quaternion", q )
-end
-
---- Creates a new quaternion.
----
----@param i? number
----@param j? number
----@param k? number
----@param r? number
----@return Quaternion
----@overload fun(q: quaternion): Quaternion
-function Quaternion( i, j, k, r )
-	if IsQuaternion( i ) then
----@diagnostic disable-next-line: need-check-nil
-		i, j, k, r = i[1], i[2], i[3], i[4]
-	end
-	return MakeQuaternion { i or 0, j or 0, k or 0, r or 1 }
-end
-
----@type Quaternion
-
----@param data string
----@return Quaternion self
-function quat_meta:__unserialize( data )
-	local i, j, k, r = data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*)" )
-	self[1] = tonumber( i )
-	self[2] = tonumber( j )
-	self[3] = tonumber( k )
-	self[4] = tonumber( r )
-	return self
-end
-
----@return string data
-function quat_meta:__serialize()
-	return string.format("%f;%f;%f;%f", self[1], self[2], self[3], self[4])
-end
-
-QUAT_ZERO = Quaternion()
-
---- Clones the quaternion.
----
----@return Quaternion clone
-function quat_meta:Clone()
-	return MakeQuaternion { self[1], self[2], self[3], self[4] }
-end
-
-local QuatStr = QuatStr
----@return string
-function quat_meta:__tostring()
-	return QuatStr( self )
-end
-
----@return Quaternion
-function quat_meta:__unm()
-	return MakeQuaternion { -self[1], -self[2], -self[3], -self[4] }
-end
-
---- Conjugates the quaternion.
----
----@return Quaternion
-function quat_meta:Conjugate()
-	return MakeQuaternion { -self[1], -self[2], -self[3], self[4] }
-end
-
---- Inverts the quaternion.
----
----@return Quaternion
-function quat_meta:Invert()
-	local l = quat_meta.LengthSquare( self )
-	return MakeQuaternion { -self[1] / l, -self[2] / l, -self[3] / l, self[4] / l }
-end
-
---- Adds to the quaternion.
----
----@param o quaternion | number
----@return Quaternion self
-function quat_meta:Add( o )
-	if IsQuaternion( o ) then
-		self[1] = self[1] + o[1]
-		self[2] = self[2] + o[2]
-		self[3] = self[3] + o[3]
-		self[4] = self[4] + o[4]
-	else
-		self[1] = self[1] + o
-		self[2] = self[2] + o
-		self[3] = self[3] + o
-		self[4] = self[4] + o
-	end
-	return self
-end
-
----@param a quaternion | number
----@param b quaternion | number
----@return Quaternion
-function quat_meta.__add( a, b )
-	if not IsQuaternion( a ) then
-		a, b = b, a
-	end
-	---@cast a quaternion
-	return quat_meta.Add( quat_meta.Clone( a ), b )
-end
-
---- Subtracts from the quaternion.
----
----@param o quaternion | number
----@return Quaternion self
-function quat_meta:Sub( o )
-	if IsQuaternion( o ) then
-		self[1] = self[1] - o[1]
-		self[2] = self[2] - o[2]
-		self[3] = self[3] - o[3]
-		self[4] = self[4] - o[4]
-	else
-		self[1] = self[1] - o
-		self[2] = self[2] - o
-		self[3] = self[3] - o
-		self[4] = self[4] - o
-	end
-	return self
-end
-
----@param a quaternion | number
----@param b quaternion | number
----@return Quaternion
-function quat_meta.__sub( a, b )
-	if not IsQuaternion( a ) then
-		a, b = b, a
-	end
-	---@cast a quaternion
-	return quat_meta.Sub( quat_meta.Clone( a ), b )
-end
-
---- Multiplies (~rotate) the quaternion.
----
----@param o quaternion
----@return Quaternion self
-function quat_meta:Mul( o )
-	local i1, j1, k1, r1 = self[1], self[2], self[3], self[4]
-	local i2, j2, k2, r2 = o[1], o[2], o[3], o[4]
-	self[1] = j1 * k2 - k1 * j2 + r1 * i2 + i1 * r2
-	self[2] = k1 * i2 - i1 * k2 + r1 * j2 + j1 * r2
-	self[3] = i1 * j2 - j1 * i2 + r1 * k2 + k1 * r2
-	self[4] = r1 * r2 - i1 * i2 - j1 * j2 - k1 * k2
-	return self
-end
-
----@param a quaternion | number
----@param b quaternion | number
----@return Quaternion
----@overload fun(a: Quaternion, b: vector): Vector
----@overload fun(a: Quaternion, b: transform): Transformation
-function quat_meta.__mul( a, b )
-	if not IsQuaternion( a ) then
-		a, b = b, a
-	end
-	---@cast a quaternion
-	if type( b ) == "number" then
-		return Quaternion( a[1] * b, a[2] * b, a[3] * b, a[4] * b )
-	end
-	if IsVector( b ) then
-		return vector_meta.__mul( b, a )
-	end
-	if IsTransformation( b ) then
-		---@diagnostic disable-next-line: cast-type-mismatch
-		---@cast b transform
-		return Transformation( vector_meta.Mul( vector_meta.Clone( b.pos ), a ), QuatRotateQuat( b.rot, a ) )
-	end
-	return MakeQuaternion( QuatRotateQuat( a, b ) )
-end
-
---- Divides the quaternion components.
----
----@param o number
----@return Quaternion self
-function quat_meta:Div( o )
-	if IsQuaternion( o ) then
-		quat_meta.Mul( self, { -o[1], -o[2], -o[3], o[4] } )
-	else
-		self[1] = self[1] / o
-		self[2] = self[2] / o
-		self[3] = self[3] / o
-		self[4] = self[4] / o
-	end
-	return self
-end
-
----@param a Quaternion
----@param b number
----@return Quaternion
-function quat_meta.__div( a, b )
-	return quat_meta.Div( quat_meta.Clone( a ), b )
-end
-
----@param a Quaternion
----@param b Quaternion
----@return boolean
-function quat_meta.__eq( a, b )
-	return a[1] == b[1] and a[2] == b[2] and a[3] == b[3] and a[4] == b[4]
-end
-
---- Gets the squared length of the quaternion.
----
----@return number
-function quat_meta:LengthSquare()
-	return self[1] ^ 2 + self[2] ^ 2 + self[3] ^ 2 + self[4] ^ 2
-end
-
---- Gets the length of the quaternion
----
----@return number
-function quat_meta:Length()
-	return math.sqrt( quat_meta.LengthSquare( self ) )
-end
-
-local QuatSlerp = QuatSlerp
---- S-lerps from the quaternion to another one.
----
----@param o quaternion
----@param n number
----@return Quaternion
-function quat_meta:Slerp( o, n )
-	return MakeQuaternion( QuatSlerp( self, o, n ) )
-end
-
---- Gets the left-direction of the quaternion.
----
----@return Vector
-function quat_meta:Left()
-	local x, y, z, s = self[1], self[2], self[3], self[4]
-
-	return Vector( 1 - (y ^ 2 + z ^ 2) * 2, (z * s + x * y) * 2, (x * z - y * s) * 2 )
-end
-
---- Gets the up-direction of the quaternion.
----
----@return Vector
-function quat_meta:Up()
-	local x, y, z, s = self[1], self[2], self[3], self[4]
-
-	return Vector( (y * x - z * s) * 2, 1 - (z ^ 2 + x ^ 2) * 2, (x * s + y * z) * 2 )
-end
-
---- Gets the forward-direction of the quaternion.
----
----@return Vector
-function quat_meta:Forward()
-	local x, y, z, s = self[1], self[2], self[3], self[4]
-
-	return Vector( (y * s + z * x) * 2, (z * y - x * s) * 2, 1 - (x ^ 2 + y ^ 2) * 2 )
-end
-
---- Gets the euler angle representation of the quaternion.
---- Note: This uses the same order as QuatEuler().
----
----@return number
----@return number
----@return number
-function quat_meta:ToEuler()
-	if GetQuatEuler then
-		return GetQuatEuler( self )
-	end
-	local x, y, z, w = self[1], self[2], self[3], self[4]
-	-- Credit to https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToEuler/index.htm
-
-	local bank, heading, attitude
-
-	local s = 2 * x * y + 2 * z * w
-	if s >= 1 then
-		heading = 2 * math.atan2( x, w )
-		bank = 0
-		attitude = math.pi / 2
-	elseif s <= -1 then
-		heading = -2 * math.atan2( x, w )
-		bank = 0
-		attitude = math.pi / -2
-	else
-		bank = math.atan2( 2 * x * w - 2 * y * z, 1 - 2 * x ^ 2 - 2 * z ^ 2 )
-		heading = math.atan2( 2 * y * w - 2 * x * z, 1 - 2 * y ^ 2 - 2 * z ^ 2 )
-		attitude = math.asin( s )
-	end
-
-	return math.deg( bank ), math.deg( heading ), math.deg( attitude )
-end
-
---- Gets the axis-angle representation of the quaternion.
---- Note: This returns the values QuatAxisAngle() needs.
----
----@return Vector
----@return number
-function quat_meta:ToAxisAngle()
-	local iw = math.sqrt( 1 - self[4] ^ 2 )
-	if iw <= 0 then return Vector( 0, 0, 0 ), 0 end
-	return Vector( self[1] / iw, self[2] / iw, self[3] / iw ), math.deg( math.asin( iw ) * 2 )
-end
-
---- Approachs another quaternion by the specified angle.
----
----@param dest quaternion
----@param rate number
----@return Quaternion
-function quat_meta:Approach( dest, rate )
-	local dot = self[1] * dest[1] + self[2] * dest[2] + self[3] * dest[3] + self[4] * dest[4]
-	if dot >= 1 then
-		return self
-	end
-	local corr_rate = rate / math.acos( 2 * dot ^ 2 - 1 )
-	if corr_rate >= 1 then
-		return MakeQuaternion( dest )
-	end
-	return MakeQuaternion( QuatSlerp( self, dest, corr_rate ) )
-end
-
- end)();
---src/vector/transform.lua
-(function() ---@diagnostic disable: duplicate-doc-field
-----------------
--- Transform class and related functions
--- @script vector.transform
-
-local vector_meta = global_metatable( "vector" )
-local quat_meta = global_metatable( "quaternion" )
-
----@class transform
----@field pos vector
----@field rot quaternion
-
----@class Transformation: transform
----@field pos Vector
----@field rot Quaternion
-local transform_meta
-transform_meta = global_metatable( "transformation" )
-
---- Tests if the parameter is a transformation.
----
----@param t any
----@return boolean
-function IsTransformation( t )
-	return type( t ) == "table" and t.pos and t.rot
-end
-
---- Makes the parameter transform into a transformation.
----
----@param t transform
----@return Transformation t
-function MakeTransformation( t )
-	instantiate_global_metatable( "vector", t.pos )
-	instantiate_global_metatable( "quaternion", t.rot )
-	return instantiate_global_metatable( "transformation", t )
-end
-
---- Creates a new transformation.
----
----@param pos? vector
----@param rot? quaternion
----@return Transformation
-function Transformation( pos, rot )
-	return MakeTransformation { pos = pos or { 0, 0, 0 }, rot = rot or { 0, 0, 0, 1 } }
-end
-
----@type Transformation
-
----@param data string
----@return Transformation self
-function transform_meta:__unserialize( data )
-	local x, y, z, i, j, k, r =
-		data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*)" )
-	self.pos = Vector( tonumber( x ), tonumber( y ), tonumber( z ) )
-	self.rot = Quaternion( tonumber( i ), tonumber( j ), tonumber( k ), tonumber( r ) )
-	return self
-end
-
----@return string data
-function transform_meta:__serialize()
-	return string.format("%f;%f;%f;%f;%f;%f;%f", self.pos[1], self.pos[2], self.pos[3], self.rot[1], self.rot[2], self.rot[3], self.rot[4])
-end
-
---- Clones the transformation.
----
----@return Transformation clone
-function transform_meta:Clone()
-	return MakeTransformation { pos = vector_meta.Clone( self.pos ), rot = quat_meta.Clone( self.rot ) }
-end
-
-local TransformStr = TransformStr
----@return string
-function transform_meta:__tostring()
-	return TransformStr( self )
-end
-
-local TransformToLocalPoint = TransformToLocalPoint
-local TransformToLocalTransform = TransformToLocalTransform
-local TransformToLocalVec = TransformToLocalVec
-local TransformToParentPoint = TransformToParentPoint
-local TransformToParentTransform = TransformToParentTransform
-local TransformToParentVec = TransformToParentVec
-
----@param a transform
----@param b transform | vector | quaternion
----@return Transformation
-function transform_meta.__add( a, b )
-	if not IsTransformation( b ) then
-		if IsVector( b ) then
-			---@cast b vector
-			b = Transformation( b, QUAT_ZERO )
-		elseif IsQuaternion( b ) then
-			---@cast b quaternion
-			b = Transformation( VEC_ZERO, b )
-		end
-	end
-	---@cast b transform
-	return MakeTransformation( TransformToParentTransform( a, b ) )
-end
-
---- Gets the local representation of a world-space transform, point or rotation
----
----@generic T : transform | vector | quaternion
----@param o T
----@return T
-function transform_meta:ToLocal( o )
-	if IsTransformation( o ) then
-		return MakeTransformation( TransformToLocalTransform( self, o ) )
-	elseif IsQuaternion( o ) then
-		return MakeQuaternion( TransformToLocalTransform( self, Transform( {}, o ) ).rot )
-	else
-		return MakeVector( TransformToLocalPoint( self, o ) )
-	end
-end
-
---- Gets the local representation of a world-space direction
----
----@param o vector
----@return Vector
-function transform_meta:ToLocalDir( o )
-	return MakeVector( TransformToLocalVec( self, o ) )
-end
-
---- Gets the global representation of a local-space transform, point or rotation
----
----@generic T : transform | vector | quaternion
----@param o T
----@return T
-function transform_meta:ToGlobal( o )
-	if IsTransformation( o ) then
-		return MakeTransformation( TransformToParentTransform( self, o ) )
-	elseif IsQuaternion( o ) then
-		return MakeQuaternion( TransformToParentTransform( self, Transform( {}, o ) ).rot )
-	else
-		return MakeVector( TransformToParentPoint( self, o ) )
-	end
-end
-
---- Gets the global representation of a local-space direction
----
----@param o vector
----@return Vector
-function transform_meta:ToGlobalDir( o )
-	return MakeVector( TransformToParentVec( self, o ) )
-end
-
---- Raycasts from the transformation
----
----@deprecated
----@param dist number
----@param mul? number
----@param radius? number
----@param rejectTransparent? boolean
----@return { hit: boolean, dist: number, normal: Vector, shape: Shape | number, hitpos: Vector }
-function transform_meta:Raycast( dist, mul, radius, rejectTransparent )
-	local dir = TransformToParentVec( self, VEC_FORWARD )
-	if mul then
-		vector_meta.Mul( dir, mul )
-	end
-	local hit, dist2, normal, shape = QueryRaycast( self.pos, dir, dist, radius, rejectTransparent )
-	return {
-		hit = hit,
-		dist = dist2,
-		normal = hit and MakeVector( normal ),
-		shape = hit and Shape and Shape( shape ) or shape,
-		hitpos = vector_meta.__add( self.pos, vector_meta.Mul( dir, hit and dist2 or dist ) ),
-	}
-end
-
- end)();
---src/vector/vector.lua
-(function() ----------------
--- Vector class and related functions
--- @script vector.vector
-
-local quat_meta = global_metatable( "quaternion" )
-
----@class vector
----@field [1] number
----@field [2] number
----@field [3] number
-
----@class Vector: vector
-local vector_meta
-vector_meta = global_metatable( "vector" )
-
---- Tests if the parameter is a vector.
----
----@param v any
----@return boolean
-function IsVector( v )
-	return type( v ) == "table" and type( v[1] ) == "number" and type( v[2] ) == "number" and type( v[3] ) == "number" and
-		       not v[4]
-end
-
---- Makes the parameter vec into a vector.
----
----@param v number[]
----@return Vector v
-function MakeVector( v )
-	return instantiate_global_metatable( "vector", v )
-end
-
---- Creates a new vector.
----
----@param x? number
----@param y? number
----@param z? number
----@return Vector
----@overload fun(v: vector): Vector
-function Vector( x, y, z )
-	if IsVector( x ) then
----@diagnostic disable-next-line: need-check-nil
-		x, y, z = x[1], x[2], x[3]
-	end
-	return MakeVector { x or 0, y or 0, z or 0 }
-end
-
----@type Vector
-
---- Unserialize a vector from its serialized form.
----
----@param data string
----@return Vector self
-function vector_meta:__unserialize( data )
-	local x, y, z = data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*)" )
-	self[1] = tonumber( x )
-	self[2] = tonumber( y )
-	self[3] = tonumber( z )
-	return self
-end
-
---- Serialize the vector to a string.
----
----@return string data
-function vector_meta:__serialize()
-	return string.format("%f;%f;%f", self[1], self[2], self[3])
-end
-
-VEC_ZERO = Vector()
-VEC_FORWARD = Vector( 0, 0, 1 )
-VEC_UP = Vector( 0, 1, 0 )
-VEC_LEFT = Vector( 1, 0, 0 )
-
---- Clones the vector.
----
----@return Vector clone
-function vector_meta:Clone()
-	return MakeVector { self[1], self[2], self[3] }
-end
-
-local VecStr = VecStr
---- Turn the vector into a string for printing.
----
----@return string
-function vector_meta:__tostring()
-	return VecStr( self )
-end
-
---- Unary operator `-v`
----
----@return Vector
-function vector_meta:__unm()
-	return MakeVector { -self[1], -self[2], -self[3] }
-end
-
---- Adds to the vector.
----
----@param o vector | number
----@return Vector self
-function vector_meta:Add( o )
-	if IsVector( o ) then
-		self[1] = self[1] + o[1]
-		self[2] = self[2] + o[2]
-		self[3] = self[3] + o[3]
-	else
-		self[1] = self[1] + o
-		self[2] = self[2] + o
-		self[3] = self[3] + o
-	end
-	return self
-end
-
---- Addition operator `v + o`
----
----@param a vector | number
----@param b vector | number
----@return Vector
----@overload fun(a: transform, b: Vector): Transformation
----@overload fun(a: Vector, b: transform): Transformation
-function vector_meta.__add( a, b )
-	if not IsVector( a ) then
-		a, b = b, a
-	end
-	---@cast a vector
-	if IsTransformation( b ) then
-		---@diagnostic disable-next-line: cast-type-mismatch
-		---@cast b transform
-		return Transformation( vector_meta.Add( vector_meta.Clone( a ), b.pos ), quat_meta.Clone( b.rot ) )
-	end
-	return vector_meta.Add( vector_meta.Clone( a ), b )
-end
-
---- Subtracts from the vector.
----
----@param o vector | number
----@return Vector self
-function vector_meta:Sub( o )
-	if IsVector( o ) then
-		self[1] = self[1] - o[1]
-		self[2] = self[2] - o[2]
-		self[3] = self[3] - o[3]
-	else
-		self[1] = self[1] - o
-		self[2] = self[2] - o
-		self[3] = self[3] - o
-	end
-	return self
-end
-
---- Subtraction operator `v - o`
----
----@param a vector | number
----@param b vector | number
----@return Vector
-function vector_meta.__sub( a, b )
-	if not IsVector( a ) then
-		a, b = b, a
-	end
-	---@cast a vector
-	return vector_meta.Sub( vector_meta.Clone( a ), b )
-end
-
---- Multiplies the vector.
----
----@param o vector | quaternion | number
----@return Vector self
-function vector_meta:Mul( o )
-	if IsVector( o ) then
-		self[1] = self[1] * o[1]
-		self[2] = self[2] * o[2]
-		self[3] = self[3] * o[3]
-	elseif IsQuaternion( o ) then
-		-- v2 = v + 2 * r X (s * v + r X v) / quat_meta.LengthSquare(self)
-		-- local s, r = o[4], Vector(o[1], o[2], o[3])
-		-- self:Add(2 * s * r:Cross(self) + 2 * r:Cross(r:Cross(self)))
-
-		local x1, y1, z1 = self[1], self[2], self[3]
-		local x2, y2, z2, s = o[1], o[2], o[3], o[4]
-
-		local x3 = y2 * z1 - z2 * y1
-		local y3 = z2 * x1 - x2 * z1
-		local z3 = x2 * y1 - y2 * x1
-
-		self[1] = x1 + (x3 * s + y2 * z3 - z2 * y3) * 2
-		self[2] = y1 + (y3 * s + z2 * x3 - x2 * z3) * 2
-		self[3] = z1 + (z3 * s + x2 * y3 - y2 * x3) * 2
-	else
-		self[1] = self[1] * o
-		self[2] = self[2] * o
-		self[3] = self[3] * o
-	end
-	return self
-end
-
---- Multiplication operator `v * o`
----
----@param a vector | quaternion | number
----@param b vector | quaternion | number
----@return Vector
-function vector_meta.__mul( a, b )
-	if not IsVector( a ) then
-		a, b = b, a
-	end
-	---@cast a vector
-	return vector_meta.Mul( vector_meta.Clone( a ), b )
-end
-
---- Divides the vector components.
----
----@param o number
----@return Vector self
-function vector_meta:Div( o )
-	self[1] = self[1] / o
-	self[2] = self[2] / o
-	self[3] = self[3] / o
-	return self
-end
-
---- Division operator `v / o`
----
----@param a vector
----@param b number
----@return Vector
-function vector_meta.__div( a, b )
-	return vector_meta.Div( vector_meta.Clone( a ), b )
-end
-
---- Applies the modulo operator on the vector components.
----
----@param o number
----@return Vector self
-function vector_meta:Mod( o )
-	self[1] = self[1] % o
-	self[2] = self[2] % o
-	self[3] = self[3] % o
-	return self
-end
-
---- Modulo operator `v % o`
----
----@param a vector
----@param b number
----@return Vector
-function vector_meta.__mod( a, b )
-	return vector_meta.Mod( vector_meta.Clone( a ), b )
-end
-
---- Applies the exponent operator on the vector components.
----
----@param o number
----@return Vector self
-function vector_meta:Pow( o )
-	self[1] = self[1] ^ o
-	self[2] = self[2] ^ o
-	self[3] = self[3] ^ o
-	return self
-end
-
---- Power operator `v ^ o`
----
----@param a vector
----@param b number
----@return Vector
-function vector_meta.__pow( a, b )
-	return vector_meta.Pow( vector_meta.Clone( a ), b )
-end
-
---- Equality comparison operator `v == o`
----
----@param a vector
----@param b vector
----@return boolean
-function vector_meta.__eq( a, b )
-	return a[1] == b[1] and a[2] == b[2] and a[3] == b[3]
-end
-
---- Strict inequality comparison operator `v < o`
----
----@param a vector
----@param b vector
----@return boolean
-function vector_meta.__lt( a, b )
-	return a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and (a[3] < b[3]))))
-end
-
---- Inequality comparison operator `v <= o`
----
----@param a vector
----@param b vector
----@return boolean
-function vector_meta.__le( a, b )
-	return a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and (a[3] <= b[3]))))
-end
-
-local VecDot = VecDot
---- Computes the dot product with another vector.
----
----@param b vector
----@return number
-function vector_meta:Dot( b )
-	return VecDot( self, b )
-end
-
-local VecCross = VecCross
---- Computes the cross product with another vector.
----
----@param b vector
----@return Vector
-function vector_meta:Cross( b )
-	return MakeVector( VecCross( self, b ) )
-end
-
-local VecLength = VecLength
---- Gets the length of the vector.
----
----@return number
-function vector_meta:Length()
-	return VecLength( self )
-end
-
---- Gets the volume of the vector (product of all its components).
----
----@return number
-function vector_meta:Volume()
-	return math.abs( self[1] * self[2] * self[3] )
-end
-
-local VecLerp = VecLerp
---- Lerps from the vector to another one.
----
----@param o vector
----@param n number
----@return Vector
-function vector_meta:Lerp( o, n )
-	return MakeVector( VecLerp( self, o, n ) )
-end
-
-local VecNormalize = VecNormalize
---- Gets the normalized form of the vector.
----
----@return Vector
-function vector_meta:Normalized()
-	return MakeVector( VecNormalize( self ) )
-end
-
---- Normalize the vector.
----
----@return Vector self
-function vector_meta:Normalize()
-	return vector_meta.Div( self, vector_meta.Length( self ) )
-end
-
---- Gets the squared distance to another vector.
----
----@param o vector
----@return number
-function vector_meta:DistSquare( o )
-	return (self[1] - o[1]) ^ 2 + (self[2] - o[2]) ^ 2 + (self[3] - o[3]) ^ 2
-end
-
---- Gets the distance to another vector.
----
----@param o vector
----@return number
-function vector_meta:Distance( o )
-	return math.sqrt( vector_meta.DistSquare( self, o ) )
-end
-
---- Gets the rotation to another vector.
----
----@param o vector
----@return Quaternion
-function vector_meta:LookAt( o )
-	return MakeQuaternion( QuatLookAt( self, o ) )
-end
-
---- Convert the direction vector into a Quaternion using an optional up vector.
---- This function behaves similarly to QuatLookAt, so "forward" is -z
----
----@param target_up? vector
----@return Quaternion
-function vector_meta:ToQuaternion( target_up )
-	local forward = VecScale( self, -1 / VecLength( self ) )
-	local right = VecNormalize( VecCross( target_up or Vec( 0, 1, 0 ), forward ) )
-	local up = VecCross( forward, right )
-
-	local m00, m01, m02 = right[1], right[2], right[3]
-	local m10, m11, m12 = up[1], up[2], up[3]
-	local m20, m21, m22 = forward[1], forward[2], forward[3]
-
-	if m22 < 0 then
-		if m00 > m11 then
-			local t = 1 + m00 - m11 - m22
-			local t2 = 0.5 / math.sqrt( t )
-			return Quaternion( t2 * t, t2 * (m01 + m10), t2 * (m20 + m02), t2 * (m12 - m21) )
-		else
-			local t = 1 - m00 + m11 - m22
-			local t2 = 0.5 / math.sqrt( t )
-			return Quaternion( t2 * (m01 + m10), t2 * t, t2 * (m12 + m21), t2 * (m20 - m02) )
-		end
-	else
-		if m00 < -m11 then
-			local t = 1 - m00 - m11 + m22
-			local t2 = 0.5 / math.sqrt( t )
-			return Quaternion( t2 * (m20 + m02), t2 * (m12 + m21), t2 * t, t2 * (m01 - m10) )
-		else
-			local t = 1 + m00 + m11 + m22
-			local t2 = 0.5 / math.sqrt( t )
-			return Quaternion( t2 * (m12 - m21), t2 * (m20 - m02), t2 * (m01 - m10), t2 * t )
-		end
-	end
-end
-
---- Approachs another vector by the specified distance.
----
----@param dest vector
----@param rate number
----@return Vector
-function vector_meta:Approach( dest, rate )
-	local dist = vector_meta.Distance( self, dest )
-	if dist < rate then
-		return MakeVector( dest )
-	end
-	return vector_meta.Lerp( self, dest, rate / dist )
-end
-
---- Get the minimum value for each vector component.
----
----@vararg Vector|number
----@return Vector
-function vector_meta:Min( ... )
-	local n = vector_meta.Clone( self )
-	for i = 1, select( "#", ... ) do
-		local o = select( i, ... )
-		if type( o ) == "number" then
-			n[1] = math.min( n[1], o )
-			n[2] = math.min( n[2], o )
-			n[3] = math.min( n[3], o )
-		else
-			n[1] = math.min( n[1], o[1] )
-			n[2] = math.min( n[2], o[2] )
-			n[3] = math.min( n[3], o[3] )
-		end
-	end
-	return n
-end
-
---- Get the maximum value for each vector component.
----
----@vararg Vector
----@return Vector
----@overload fun(o: number, ...): Vector
-function vector_meta:Max( ... )
-	local n = vector_meta.Clone( self )
-	for i = 1, select( "#", ... ) do
-		local o = select( i, ... )
-		if type( o ) == "number" then
-			n[1] = math.max( n[1], o )
-			n[2] = math.max( n[2], o )
-			n[3] = math.max( n[3], o )
-		else
-			n[1] = math.max( n[1], o[1] )
-			n[2] = math.max( n[2], o[2] )
-			n[3] = math.max( n[3], o[3] )
-		end
-	end
-	return n
-end
-
---- Clamp the vector components.
----
----@param min vector | number
----@param max vector | number
----@return Vector
-function vector_meta:Clamp( min, max )
-	if type( min ) == "number" then
-		---@cast min number
-		---@cast max number
-		return Vector( math.max( math.min( self[1], max ), min ), math.max( math.min( self[2], max ), min ),
-		               math.max( math.min( self[3], max ), min ) )
-	else
-		return Vector( math.max( math.min( self[1], max[1] ), min[1] ), math.max( math.min( self[2], max[2] ), min[2] ),
-		               math.max( math.min( self[3], max[3] ), min[3] ) )
-	end
-end
-
- end)();
---src/entities/entity.lua
-(function() ----------------
--- Entity class and related functions
--- @script entities.entity
-
----@class entity_handle: integer
-
----@class Entity
----@field handle entity_handle
----@field type string
----@field private _C table property contrainer (internal)
----@field description string (dynamic property)
----@field tags table (dynamic property -- readonly)
-local entity_meta = global_metatable( "entity" )
-
-local properties = {}
-
--- using these tables as keys to avoid quicksaving them
-local DATA_KEY = {}
-local TAGS_KEY = {}
-
-function entity_meta:__index( k )
-	if properties[k] then return properties[k]( self, false ) end
-	if entity_meta[k] then return entity_meta[k] end
-	local entdata = rawget( self, DATA_KEY )
-	if not entdata then
-		entdata = util.shared_table( "game.umf.entdata." .. rawget( self, "handle" ) )
-		rawset( self, DATA_KEY, entdata )
-	end
-	return entdata[k]
-end
-
-function entity_meta:__newindex( k, v )
-	if properties[k] then return properties[k]( self, true, v ) end
-	local entdata = rawget( self, DATA_KEY )
-	if not entdata then
-		entdata = util.shared_table( "game.umf.entdata." .. rawget( self, "handle" ) )
-		rawset( self, DATA_KEY, entdata )
-	end
-	entdata[k] = v
-end
-
-function properties:description( set, val )
-	if set then
-		SetDescription( self.handle, val )
-	else
-		return GetDescription( self.handle )
-	end
-end
-
-local tags_meta = {
-	__index = function( self, k )
-		if HasTag( self.__handle, k ) then
-			return GetTagValue( self.__handle, k )
-		end
-	end,
-	__newindex = function( self, k, v )
-		if v == nil then
-			RemoveTag( self.__handle, k )
-		else
-			SetTag( self.__handle, k, tostring( v ) )
-		end
-	end
-}
-
-function properties:tags( set )
-	if set then error( "cannot set tags key" ) end
-	local enttags = rawget( self, TAGS_KEY )
-	if not enttags then
-		enttags = setmetatable( { __handle = self.handle }, tags_meta )
-		rawset( self, TAGS_KEY, enttags )
-	end
-	return enttags
-end
-
---- Gets the handle of an entity.
----
----@param e Entity | integer
----@return entity_handle
-function GetEntityHandle( e )
-	if IsEntity( e ) then
-		return e.handle
-	end
-	---@cast e entity_handle
-	return e
-end
-
---- Gets the validity of a table by calling :IsValid() if it supports it.
----
----@param e any
----@return boolean
-function IsValid( e )
-	if type( e ) == "table" and e.IsValid then
-		return e:IsValid()
-	end
-	return false
-end
-
---- Tests if the parameter is an entity.
----
----@param e any
----@return boolean
-function IsEntity( e )
-	return type( e ) == "table" and type( e.handle ) == "number"
-end
-
---- Wraps the given handle with the entity class.
----
----@param handle integer | Entity
----@return Entity
-function Entity( handle )
-	if type( handle ) == "number" and handle > 0 then
-		---@cast handle entity_handle
-		local type = GetEntityType and GetEntityType( handle )
-		return instantiate_global_metatable( type or "entity", { handle = handle, type = type or "unknown" } )
-	end
-	---@cast handle Entity
-	return handle
-end
-
----@type Entity
-
----@param self Entity
----@param data string
----@return Entity self
-function entity_meta:__unserialize( data )
-	rawset( self, "handle", tonumber( data ) )
-	return self
-end
-
----@param self Entity
----@return string data
-function entity_meta:__serialize()
-	return tostring( self.handle )
-end
-
----@param self Entity
----@return string
-function entity_meta:__tostring()
-	return string.format( "Entity[%d]", self.handle )
-end
-
---- Gets the type of the entity.
----
----@param self Entity
----@return string type
-function entity_meta:GetType()
-	return rawget( self, "type" ) or "unknown"
-end
-
-local IsHandleValid = IsHandleValid
---- Gets the validity of the entity.
----
----@param self Entity
----@return boolean
-function entity_meta:IsValid()
-	return IsHandleValid( self.handle )
-end
-
-local SetTag = SetTag
---- Sets a tag value on the entity.
----
----@param self Entity
----@param tag string
----@param value string
-function entity_meta:SetTag( tag, value )
-	assert( self:IsValid() )
-	return SetTag( self.handle, tag, value )
-end
-
-local SetDescription = SetDescription
---- Sets the description of the entity.
----
----@param self Entity
----@param description string
-function entity_meta:SetDescription( description )
-	assert( self:IsValid() )
-	return SetDescription( self.handle, description )
-end
-
-local RemoveTag = RemoveTag
---- Removes a tag from the entity.
----
----@param self Entity
----@param tag string
-function entity_meta:RemoveTag( tag )
-	assert( self:IsValid() )
-	return RemoveTag( self.handle, tag )
-end
-
-local HasTag = HasTag
---- Gets if the entity has a tag.
----
----@param self Entity
----@param tag string
----@return boolean
-function entity_meta:HasTag( tag )
-	assert( self:IsValid() )
-	return HasTag( self.handle, tag )
-end
-
-local GetTagValue = GetTagValue
---- Gets the value of a tag.
----
----@param self Entity
----@param tag string
----@return string
-function entity_meta:GetTagValue( tag )
-	assert( self:IsValid() )
-	return GetTagValue( self.handle, tag )
-end
-
-local GetDescription = GetDescription
---- Gets the description of the entity.
----
----@param self Entity
----@return string
-function entity_meta:GetDescription()
-	assert( self:IsValid() )
-	return GetDescription( self.handle )
-end
-
-local Delete = Delete
---- Deletes the entity.
----@param self Entity
-function entity_meta:Delete()
-	return Delete( self.handle )
-end
-
- end)();
---src/entities/body.lua
-(function() ----------------
--- Body class and related functions
--- @script entities.body
-
----@class body_handle: integer
-
----@class Body: Entity
----@field handle body_handle
----@field private _C table property contrainer (internal)
----@field transform Transformation (dynamic property)
----@field velocity Vector (dynamic property)
----@field angularVelocity Vector (dynamic property)
----@field active boolean (dynamic property)
----@field dynamic boolean (dynamic property)
----@field broken boolean (dynamic property -- readonly)
----@field mass number (dynamic property -- readonly)
----@field shapes Shape[] (dynamic property -- readonly)
----@field vehicle Vehicle (dynamic property -- readonly)
-local body_meta = global_metatable( "body", "entity", true )
-
---- Tests if the parameter is a body entity.
----
----@param e any
----@return boolean
-function IsBody( e )
-	return IsEntity( e ) and e.type == "body"
-end
-
---- Wraps the given handle with the body class.
----
----@param handle number
----@return Body?
-function Body( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "body", { handle = handle, type = "body" } )
-	end
-end
-
---- Finds a body with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Body?
-function FindBodyByTag( tag, global )
-	return Body( FindBody( tag, global ) )
-end
-
---- Finds all bodies with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Body[]
-function FindBodiesByTag( tag, global )
-	local t = FindBodies( tag, global )
-	for i = 1, #t do
-		t[i] = Body( t[i] )
-	end
-	return t
-end
-
----@type Body
-
----@param self Body
----@return string
-function body_meta:__tostring()
-	return string.format( "Body[%d]", self.handle )
-end
-
---- Applies a force to the body at the specified world-space point.
----
----@param self Body
----@param pos vector World-space position
----@param vel vector World-space force and direction
-function body_meta:ApplyImpulse( pos, vel )
-	assert( self:IsValid() )
-	return ApplyBodyImpulse( self.handle, pos, vel )
-end
-
---- Applies a force to the body at the specified object-space point.
----
----@param self Body
----@param pos vector Object-space position
----@param vel vector Object-space force and direction
-function body_meta:ApplyLocalImpulse( pos, vel )
-	local transform = self:GetTransform()
-	return self:ApplyImpulse( transform:ToGlobal( pos ), transform:ToGlobalDir( vel ) )
-end
-
---- Draws the outline of the body.
----
----@param self Body
----@param r number
----@overload fun(self: Body, r: number, g: number, b: number, a: number)
-function body_meta:DrawOutline( r, ... )
-	assert( self:IsValid() )
-	return DrawBodyOutline( self.handle, r, ... )
-end
-
---- Draws a highlight of the body.
----
----@param self Body
----@param amount number
-function body_meta:DrawHighlight( amount )
-	assert( self:IsValid() )
-	return DrawBodyHighlight( self.handle, amount )
-end
-
---- Sets the transform of the body.
----
----@param self Body
----@param tr transform
-function body_meta:SetTransform( tr )
-	assert( self:IsValid() )
-	return SetBodyTransform( self.handle, tr )
-end
-
---- Sets if the body should be simulated.
----
----@param self Body
----@param bool boolean
-function body_meta:SetActive( bool )
-	assert( self:IsValid() )
-	return SetBodyActive( self.handle, bool )
-end
-
---- Sets if the body should move.
----
----@param self Body
----@param bool boolean
-function body_meta:SetDynamic( bool )
-	assert( self:IsValid() )
-	return SetBodyDynamic( self.handle, bool )
-end
-
---- Sets the velocity of the body.
----
----@param self Body
----@param vel vector
-function body_meta:SetVelocity( vel )
-	assert( self:IsValid() )
-	return SetBodyVelocity( self.handle, vel )
-end
-
---- Sets the angular velocity of the body.
----
----@param self Body
----@param avel vector
-function body_meta:SetAngularVelocity( avel )
-	assert( self:IsValid() )
-	return SetBodyAngularVelocity( self.handle, avel )
-end
-
---- Gets the transform of the body.
----
----@param self Body
----@return Transformation
-function body_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetBodyTransform( self.handle ) )
-end
-
---- Gets the mass of the body.
----
----@param self Body
----@return number
-function body_meta:GetMass()
-	assert( self:IsValid() )
-	return GetBodyMass( self.handle )
-end
-
---- Gets the velocity of the body.
----
----@param self Body
----@return Vector
-function body_meta:GetVelocity()
-	assert( self:IsValid() )
-	return MakeVector( GetBodyVelocity( self.handle ) )
-end
-
---- Gets the velocity at the position on the body.
----
----@param self Body
----@param pos vector
----@return Vector
-function body_meta:GetVelocityAtPos( pos )
-	assert( self:IsValid() )
-	return MakeVector( GetBodyVelocityAtPos( self.handle, pos ) )
-end
-
---- Gets the angular velocity of the body.
----
----@param self Body
----@return Vector
-function body_meta:GetAngularVelocity()
-	assert( self:IsValid() )
-	return MakeVector( GetBodyAngularVelocity( self.handle ) )
-end
-
---- Gets the shape of the body.
----
----@param self Body
----@return Shape[]
-function body_meta:GetShapes()
-	assert( self:IsValid() )
-	local shapes = GetBodyShapes( self.handle )
-	for i = 1, #shapes do
-		shapes[i] = Shape( shapes[i] )
-	end
-	return shapes
-end
-
---- Gets the vehicle of the body.
----
----@param self Body
----@return Vehicle?
-function body_meta:GetVehicle()
-	assert( self:IsValid() )
-	return Vehicle( GetBodyVehicle( self.handle ) )
-end
-
---- Gets the bounds of the body.
----
----@param self Body
----@return Vector min
----@return Vector max
-function body_meta:GetWorldBounds()
-	assert( self:IsValid() )
-	local min, max = GetBodyBounds( self.handle )
-	return MakeVector( min ), MakeVector( max )
-end
-
---- Gets the center of mas in object-space.
----
----@param self Body
----@return Vector
-function body_meta:GetLocalCenterOfMass()
-	assert( self:IsValid() )
-	return MakeVector( GetBodyCenterOfMass( self.handle ) )
-end
-
---- Gets the center of mass in world-space.
----
----@param self Body
----@return Vector
-function body_meta:GetWorldCenterOfMass()
-	return self:GetTransform():ToGlobal( self:GetLocalCenterOfMass() )
-end
-
---- Gets the closest point to the body from a given origin.
----
----@param self Body
----@param origin vector
----@return boolean hit
----@return Vector? point
----@return Vector? normal
----@return Shape? shape
-function body_meta:GetClosestPoint( origin )
-	local hit, point, normal, shape = GetBodyClosestPoint( self.handle, origin )
-	if not hit then
-		return false
-	end
-	return hit, MakeVector( point ), MakeVector( normal ), Shape( shape )
-end
-
---- Gets all the dynamic bodies in the jointed structure.
---- The result will include the current body.
----
----@param self Body
----@return Body[] jointed
-function body_meta:GetJointedBodies()
-	local list = GetJointedBodies( self.handle )
-	for i = 1, #list do
-		list[i] = Body( list[i] )
-	end
-	return list
-end
-
---- Gets if the body is currently being simulated.
----
----@param self Body
----@return boolean
-function body_meta:IsActive()
-	assert( self:IsValid() )
-	return IsBodyActive( self.handle )
-end
-
---- Gets if the body is dynamic.
----
----@param self Body
----@return boolean
-function body_meta:IsDynamic()
-	assert( self:IsValid() )
-	return IsBodyDynamic( self.handle )
-end
-
---- Gets if the body is visble on screen.
----
----@param self Body
----@param maxdist number
----@return boolean
-function body_meta:IsVisible( maxdist )
-	assert( self:IsValid() )
-	return IsBodyVisible( self.handle, maxdist )
-end
-
---- Gets if the body has been broken.
----
----@param self Body
----@return boolean
-function body_meta:IsBroken()
-	return not self:IsValid() or IsBodyBroken( self.handle )
-end
-
---- Gets if the body somehow attached to something static.
----
----@param self Body
----@return boolean
-function body_meta:IsJointedToStatic()
-	assert( self:IsValid() )
-	return IsBodyJointedToStatic( self.handle )
-end
-
-----------------
--- Properties implementation
-
----@param self Body
----@param setter boolean
----@param val transform
----@return Transformation?
-function body_meta._C:transform( setter, val )
-	if setter then
-		self:SetTransform( val )
-	else
-		return self:GetTransform()
-	end
-end
-
----@param self Body
----@param setter boolean
----@param val vector
----@return Vector?
-function body_meta._C:velocity( setter, val )
-	if setter then
-		self:SetVelocity( val )
-	else
-		return self:GetVelocity()
-	end
-end
-
----@param self Body
----@param setter boolean
----@param val vector
----@return Vector?
-function body_meta._C:angularVelocity( setter, val )
-	if setter then
-		self:SetAngularVelocity( val )
-	else
-		return self:GetAngularVelocity()
-	end
-end
-
----@param self Body
----@param setter boolean
----@param val boolean
----@return boolean?
-function body_meta._C:active( setter, val )
-	if setter then
-		self:SetActive( val )
-	else
-		return self:IsActive()
-	end
-end
-
----@param self Body
----@param setter boolean
----@param val boolean
----@return boolean?
-function body_meta._C:dynamic( setter, val )
-	if setter then
-		self:SetDynamic( val )
-	else
-		return self:IsDynamic()
-	end
-end
-
----@param self Body
----@param setter boolean
----@return boolean
-function body_meta._C:broken( setter )
-	assert(not setter, "cannot set broken")
-	return self:IsBroken()
-end
-
----@param self Body
----@param setter boolean
----@return number
-function body_meta._C:mass( setter )
-	assert(not setter, "cannot set mass")
-	return self:GetMass()
-end
-
----@param self Body
----@param setter boolean
----@return Shape[]
-function body_meta._C:shapes( setter )
-	assert(not setter, "cannot set shapes")
-	return self:GetShapes()
-end
-
----@param self Body
----@param setter boolean
----@return Vehicle?
-function body_meta._C:vehicle( setter )
-	assert(not setter, "cannot set vehicle")
-	return self:GetVehicle()
-end
- end)();
---src/entities/joint.lua
-(function() ----------------
--- Joint class and related functions
--- @script entities.joint
-
----@class joint_handle: integer
-
----@class Joint: Entity
----@field handle joint_handle
----@field private _C table property contrainer (internal)
----@field jointType string (dynamic property -- readonly)
----@field broken boolean (dynamic property -- readonly)
-local joint_meta = global_metatable( "joint", "entity", true )
-
---- Tests if the parameter is a joint entity.
----
----@param e any
----@return boolean
-function IsJoint( e )
-	return IsEntity( e ) and e.type == "joint"
-end
-
---- Wraps the given handle with the joint class.
----
----@param handle number
----@return Joint?
-function Joint( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "joint", { handle = handle, type = "joint" } )
-	end
-end
-
---- Finds a joint with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Joint?
-function FindJointByTag( tag, global )
-	return Joint( FindJoint( tag, global ) )
-end
-
---- Finds all joints with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Joint[]
-function FindJointsByTag( tag, global )
-	local t = FindJoints( tag, global )
-	for i = 1, #t do
-		t[i] = Joint( t[i] )
-	end
-	return t
-end
-
----@type Joint
-
----@param self Joint
----@return string
-function joint_meta:__tostring()
-	return string.format( "Joint[%d]", self.handle )
-end
-
---- Detatches the joint from the given shape.
----
----@param self Joint
----@param shape Shape
-function joint_meta:DetachFromShape( shape )
-	local shapeHandle = GetEntityHandle( shape )
-	---@cast shapeHandle shape_handle
-	DetachJointFromShape( self.handle, shapeHandle )
-end
-
---- Makes the joint behave as a motor.
----
----@param self Joint
----@param velocity number
----@param strength number
-function joint_meta:SetMotor( velocity, strength )
-	assert( self:IsValid() )
-	return SetJointMotor( self.handle, velocity, strength )
-end
-
---- Makes the joint behave as a motor moving to the specified target.
----
----@param self Joint
----@param target number
----@param maxVel number
----@param strength number
-function joint_meta:SetMotorTarget( target, maxVel, strength )
-	assert( self:IsValid() )
-	return SetJointMotorTarget( self.handle, target, maxVel, strength )
-end
-
---- Gets the type of the joint.
----
----@param self Joint
----@return string
-function joint_meta:GetJointType()
-	assert( self:IsValid() )
-	return GetJointType( self.handle )
-end
-
---- Finds the other shape the joint is attached to.
----
----@param self Joint
----@param shape Shape | integer
----@return Shape
-function joint_meta:GetOtherShape( shape )
-	assert( self:IsValid() )
-	local shapeHandle = GetEntityHandle( shape )
-	---@cast shapeHandle shape_handle
-	local otherShape = Shape( GetJointOtherShape( self.handle, shapeHandle ) )
-	---@cast otherShape Shape
-	return otherShape
-end
-
---- Gets the limits of the joint.
----
----@param self Joint
----@return number min
----@return number max
-function joint_meta:GetLimits()
-	assert( self:IsValid() )
-	return GetJointLimits( self.handle )
-end
-
---- Gets the current position or angle of the joint.
----
----@param self Joint
----@return number
-function joint_meta:GetMovement()
-	assert( self:IsValid() )
-	return GetJointMovement( self.handle )
-end
-
---- Gets if the joint is broken.
----
----@param self Joint
----@return boolean
-function joint_meta:IsBroken()
-	return not self:IsValid() or IsJointBroken( self.handle )
-end
-
-----------------
--- Properties implementation
-
----@param self Joint
----@param setter boolean
----@return string
-function joint_meta._C:jointType( setter )
-	assert(not setter, "cannot set jointType")
-	return self:GetType()
-end
-
----@param self Joint
----@param setter boolean
----@return boolean
-function joint_meta._C:broken( setter )
-	assert(not setter, "cannot set broken")
-	return self:IsBroken()
-end
-
- end)();
---src/entities/light.lua
-(function() ----------------
--- Light class and related functions
--- @script entities.light
-
----@class light_handle: integer
-
----@class Light: Entity
----@field handle light_handle
----@field private _C table property contrainer (internal)
----@field enabled boolean (dynamic property)
----@field color Vector (dynamic property -- writeonly)
----@field intensity number (dynamic property -- writeonly)
----@field transform Transformation (dynamic property -- readonly)
----@field shape Shape (dynamic property -- readonly)
-local light_meta = global_metatable( "light", "entity", true )
-
---- Tests if the parameter is a light entity.
----
----@param e any
----@return boolean
-function IsLight( e )
-	return IsEntity( e ) and e.type == "light"
-end
-
---- Wraps the given handle with the light class.
----
----@param handle number
----@return Light?
-function Light( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "light", { handle = handle, type = "light" } )
-	end
-end
-
---- Finds a light with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Light?
-function FindLightByTag( tag, global )
-	return Light( FindLight( tag, global ) )
-end
-
---- Finds all lights with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Light[]
-function FindLightsByTag( tag, global )
-	local t = FindLights( tag, global )
-	for i = 1, #t do
-		t[i] = Light( t[i] )
-	end
-	return t
-end
-
----@type Light
-
----@param self Light
----@return string
-function light_meta:__tostring()
-	return string.format( "Light[%d]", self.handle )
-end
-
---- Sets if the light is enabled.
----
----@param self Light
----@param enabled boolean
-function light_meta:SetEnabled( enabled )
-	assert( self:IsValid() )
-	return SetLightEnabled( self.handle, enabled )
-end
-
---- Sets the color of the light.
----
----@param self Light
----@param r number
----@param g number
----@param b number
-function light_meta:SetColor( r, g, b )
-	assert( self:IsValid() )
-	return SetLightColor( self.handle, r, g, b )
-end
-
---- Sets the intensity of the light.
----
----@param self Light
----@param intensity number
-function light_meta:SetIntensity( intensity )
-	assert( self:IsValid() )
-	return SetLightIntensity( self.handle, intensity )
-end
-
---- Gets the transform of the light.
----
----@param self Light
----@return Transformation
-function light_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetLightTransform( self.handle ) )
-end
-
---- Gets the shape the light is attached to.
----
----@param self Light
----@return Shape
-function light_meta:GetShape()
-	assert( self:IsValid() )
-	local shape = Shape( GetLightShape( self.handle ) )
-	---@cast shape Shape
-	return shape
-end
-
---- Gets if the light is active.
----
----@param self Light
----@return boolean
-function light_meta:IsActive()
-	assert( self:IsValid() )
-	return IsLightActive( self.handle )
-end
-
---- Gets if the specified point is affected by the light.
----
----@param self Light
----@param point vector
----@return boolean
-function light_meta:IsPointAffectedByLight( point )
-	assert( self:IsValid() )
-	return IsPointAffectedByLight( self.handle, point )
-end
-
-----------------
--- Properties implementation
-
----@param self Light
----@param setter boolean
----@param val boolean
----@return boolean?
-function light_meta._C:enabled( setter, val )
-	if setter then
-		self:SetEnabled( val )
-	else
-		return self:IsActive()
-	end
-end
-
----@param self Light
----@param setter boolean
----@param val vector
-function light_meta._C:color( setter, val )
-	assert(setter, "cannot get color")
-	return self:SetColor( val[1], val[2], val[3] )
-end
-
----@param self Light
----@param setter boolean
----@param val number
-function light_meta._C:intensity( setter, val )
-	assert(setter, "cannot get intensity")
-	return self:SetIntensity( val )
-end
-
----@param self Light
----@param setter boolean
----@return Transformation
-function light_meta._C:transform( setter )
-	assert(not setter, "cannot set transform")
-	return self:GetTransform()
-end
-
----@param self Light
----@param setter boolean
----@return Shape
-function light_meta._C:shape( setter )
-	assert(not setter, "cannot set shape")
-	return self:GetShape()
-end
-
- end)();
---src/entities/location.lua
-(function() ----------------
--- Location class and related functions
--- @script entities.location
-
----@class location_handle: integer
-
----@class Location: Entity
----@field handle location_handle
----@field private _C table property contrainer (internal)
----@field transform Transformation (dynamic property -- readonly)
-local location_meta = global_metatable( "location", "entity", true )
-
---- Tests if the parameter is a location entity.
----
----@param e any
----@return boolean
-function IsLocation( e )
-	return IsEntity( e ) and e.type == "location"
-end
-
---- Wraps the given handle with the location class.
----
----@param handle number
----@return Location?
-function Location( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "location", { handle = handle, type = "location" } )
-	end
-end
-
---- Finds a location with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Location?
-function FindLocationByTag( tag, global )
-	return Location( FindLocation( tag, global ) )
-end
-
---- Finds all locations with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Location[]
-function FindLocationsByTag( tag, global )
-	local t = FindLocations( tag, global )
-	for i = 1, #t do
-		t[i] = Location( t[i] )
-	end
-	return t
-end
-
----@type Location
-
----@param self Location
----@return string
-function location_meta:__tostring()
-	return string.format( "Location[%d]", self.handle )
-end
-
---- Gets the transform of the location.
----
----@param self Location
----@return Transformation
-function location_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetLocationTransform( self.handle ) )
-end
-
-----------------
--- Properties implementation
-
----@param self Location
----@param setter boolean
----@return Transformation
-function location_meta._C:transform( setter )
-	assert(not setter, "cannot set transform")
-	return self:GetTransform()
-end
- end)();
---src/entities/player.lua
-(function() ----------------
--- Player class and related functions
--- @script entities.player
-
----@class Player
-local player_meta
-player_meta = global_metatable( "player" )
-
----@type Player
-PLAYER = instantiate_global_metatable( "player" )
-
----@param self Player
----@param data string
----@return Player self
-function player_meta:__unserialize( data )
-	return self
-end
-
----@param self Player
----@return string data
-function player_meta:__serialize()
-	return ""
-end
-
----@param self Player
----@return string
-function player_meta:__tostring()
-	return string.format( "Player" )
-end
-
---- Gets the type of the entity.
----
----@param self Player
----@return string type
-function player_meta:GetType()
-	return "player"
-end
-
---- Repawns the player.
----@param self Player
-function player_meta:Respawn()
-	return RespawnPlayer()
-end
-
---- Release what the player is currently holding.
----
----@param self Player
-function player_meta:ReleaseGrab()
-	ReleasePlayerGrab()
-end
-
---- Sets the transform of the player.
----
----@param self Player
----@param transform transform
----@param includePitch? boolean
-function player_meta:SetTransform( transform, includePitch )
-	return SetPlayerTransform( transform, includePitch )
-end
-
---- Sets the transform of the camera.
----
----@param self Player
----@param transform transform
-function player_meta:SetCamera( transform )
-	return SetCameraTransform( transform )
-end
-
---- Sets the Field of View of the camera.
----
----@param self Player
----@param degrees number
-function player_meta:SetFov( degrees )
-	return SetCameraFov( degrees )
-end
-
---- Sets the Depth of Field of the camera.
----
----@param self Player
----@param distance number
----@param amount number
-function player_meta:SetDof( distance, amount )
-	return SetCameraDof( distance, amount )
-end
-
---- Sets the transform of the player spawn.
----
----@param self Player
----@param transform transform
-function player_meta:SetSpawnTransform( transform )
-	return SetPlayerSpawnTransform( transform )
-end
-
---- Sets the vehicle the player is currently riding.
----
----@param self Player
----@param handle Vehicle | number
-function player_meta:SetVehicle( handle )
-	local vehicleHandle = GetEntityHandle( handle )
-	---@cast vehicleHandle vehicle_handle
-	return SetPlayerVehicle( vehicleHandle )
-end
-
---- Sets the velocity of the player.
----
----@param self Player
----@param velocity vector
-function player_meta:SetVelocity( velocity )
-	return SetPlayerVelocity( velocity )
-end
-
---- Sets the screen the player is currently viewing.
----
----@param self Player
----@param handle Screen | number
-function player_meta:SetScreen( handle )
-	local screenHandle = GetEntityHandle( handle )
-	---@cast screenHandle screen_handle
-	return SetPlayerScreen( screenHandle )
-end
-
---- Sets the health of the player.
----
----@param self Player
----@param health number
-function player_meta:SetHealth( health )
-	return SetPlayerHealth( health )
-end
-
---- Sets the velocity of the ground for the player,
---- Effectively turning it into a conveyor belt of sorts.
----
----@param self Player
----@param vel vector
-function player_meta:SetGroundVelocity(vel)
-	SetPlayerGroundVelocity(vel)
-end
-
---- Gets the transform of the player.
----
----@param self Player
----@param includePitch? boolean
----@return Transformation
-function player_meta:GetTransform( includePitch )
-	return MakeTransformation( GetPlayerTransform( includePitch ) )
-end
-
---- Gets the transform of the player camera.
----
----@param self Player
----@return Transformation
-function player_meta:GetPlayerCamera()
-	return MakeTransformation( GetPlayerCameraTransform() )
-end
-
---- Gets the transform of the camera.
----
----@param self Player
----@return Transformation
-function player_meta:GetCamera()
-	return MakeTransformation( GetCameraTransform() )
-end
-
---- Gets the velocity of the player.
----
----@param self Player
----@return Vector
-function player_meta:GetVelocity()
-	return MakeVector( GetPlayerVelocity() )
-end
-
---- Gets the vehicle the player is currently riding.
----
----@param self Player
----@return Vehicle?
-function player_meta:GetVehicle()
-	return Vehicle( GetPlayerVehicle() )
-end
-
---- Gets the shape the player is currently grabbing.
----
----@param self Player
----@return Shape?
-function player_meta:GetGrabShape()
-	return Shape( GetPlayerGrabShape() )
-end
-
---- Gets the body the player is currently grabbing.
----
----@param self Player
----@return Body?
-function player_meta:GetGrabBody()
-	return Body( GetPlayerGrabBody() )
-end
-
---- Gets the pick-able shape the player is currently targetting.
----
----@param self Player
----@return Shape?
-function player_meta:GetPickShape()
-	return Shape( GetPlayerPickShape() )
-end
-
---- Gets the pick-able body the player is currently targetting.
----
----@param self Player
----@return Body?
-function player_meta:GetPickBody()
-	return Body( GetPlayerPickBody() )
-end
-
---- Gets the interactible shape the player is currently targetting.
----
----@param self Player
----@return Shape?
-function player_meta:GetInteractShape()
-	return Shape( GetPlayerInteractShape() )
-end
-
---- Gets the interactible body the player is currently targetting.
----
----@param self Player
----@return Body?
-function player_meta:GetInteractBody()
-	return Body( GetPlayerInteractBody() )
-end
-
---- Gets the screen the player is currently interacting with.
----
----@param self Player
----@return Screen?
-function player_meta:GetScreen()
-	return Screen( GetPlayerScreen() )
-end
-
---- Gets the player health.
----
----@param self Player
----@return number
-function player_meta:GetHealth()
-	return GetPlayerHealth()
-end
-
- end)();
---src/entities/screen.lua
-(function() ----------------
--- Screen class and related functions
--- @script entities.screen
-
----@class screen_handle: integer
-
----@class Screen: Entity
----@field handle screen_handle
----@field private _C table property contrainer (internal)
----@field enabled boolean (dynamic property)
----@field shape Shape (dynamic property -- readonly)
-local screen_meta
-screen_meta = global_metatable( "screen", "entity", true )
-
---- Tests if the parameter is a screen entity.
----
----@param e any
----@return boolean
-function IsScreen( e )
-	return IsEntity( e ) and e.type == "screen"
-end
-
---- Wraps the given handle with the screen class.
----
----@param handle number
----@return Screen?
-function Screen( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "screen", { handle = handle, type = "screen" } )
-	end
-end
-
---- Finds a screen with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Screen?
-function FindScreenByTag( tag, global )
-	return Screen( FindScreen( tag, global ) )
-end
-
---- Finds all screens with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Screen[]
-function FindScreensByTag( tag, global )
-	local t = FindScreens( tag, global )
-	for i = 1, #t do
-		t[i] = Screen( t[i] )
-	end
-	return t
-end
-
----@type Screen
-
----@param self Screen
----@return string
-function screen_meta:__tostring()
-	return string.format( "Screen[%d]", self.handle )
-end
-
---- Sets if the screen is enabled.
----
----@param self Screen
----@param enabled boolean
-function screen_meta:SetEnabled( enabled )
-	assert( self:IsValid() )
-	return SetScreenEnabled( self.handle, enabled )
-end
-
---- Gets the shape the screen is attached to.
----
----@param self Screen
----@return Shape
-function screen_meta:GetShape()
-	assert( self:IsValid() )
-	local shape = Shape( GetScreenShape( self.handle ) )
-	---@cast shape Shape
-	return shape
-end
-
---- Gets if the screen is enabled.
----
----@param self Screen
----@return boolean
-function screen_meta:IsEnabled()
-	assert( self:IsValid() )
-	return IsScreenEnabled( self.handle )
-end
-
-----------------
--- Properties implementation
-
----@param self Screen
----@param setter boolean
----@param val boolean
----@return boolean?
-function screen_meta._C:enabled( setter, val )
-	if setter then
-		self:SetEnabled( val )
-	else
-		return self:IsEnabled()
-	end
-end
-
----@param self Screen
----@param setter boolean
----@return Shape
-function screen_meta._C:shape( setter )
-	assert(not setter, "cannot set shape")
-	return self:GetShape()
-end
-
- end)();
---src/entities/shape.lua
-(function() ----------------
--- Shape class and related functions
--- @script entities.shape
-
----@class shape_handle: integer
-
----@class Shape: Entity
----@field handle shape_handle
----@field private _C table property contrainer (internal)
----@field transform Transformation (dynamic property)
----@field emissive number (dynamic property -- writeonly)
----@field body Body (dynamic property -- readonly)
----@field joints Joint[] (dynamic property -- readonly)
----@field lights Light[] (dynamic property -- readonly)
----@field size Vector (dynamic property -- readonly)
----@field broken boolean (dynamic property -- readonly)
-local shape_meta
-shape_meta = global_metatable( "shape", "entity", true )
-
---- Tests if the parameter is a shape entity.
----
----@param e any
----@return boolean
-function IsShape( e )
-	return IsEntity( e ) and e.type == "shape"
-end
-
---- Wraps the given handle with the shape class.
----
----@param handle number
----@return Shape?
-function Shape( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "shape", { handle = handle, type = "shape" } )
-	end
-end
-
---- Finds a shape with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Shape?
-function FindShapeByTag( tag, global )
-	return Shape( FindShape( tag, global ) )
-end
-
---- Finds all shapes with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Shape[]
-function FindShapesByTag( tag, global )
-	local t = FindShapes( tag, global )
-	for i = 1, #t do
-		t[i] = Shape( t[i] )
-	end
-	return t
-end
-
----@type Shape
-
----@param self Shape
----@return string
-function shape_meta:__tostring()
-	return string.format( "Shape[%d]", self.handle )
-end
-
---- Draws the outline of the shape.
----
----@param self Shape
----@param r number
----@overload fun(self: Shape, r: number, g: number, b: number, a: number)
-function shape_meta:DrawOutline( r, ... )
-	assert( self:IsValid() )
-	return DrawShapeOutline( self.handle, r, ... )
-end
-
---- Draws a highlight of the shape.
----
----@param self Shape
----@param amount number
-function shape_meta:DrawHighlight( amount )
-	assert( self:IsValid() )
-	return DrawShapeHighlight( self.handle, amount )
-end
-
---- Sets the transform of the shape relative to its body.
----
----@param self Shape
----@param transform transform
-function shape_meta:SetLocalTransform( transform )
-	assert( self:IsValid() )
-	return SetShapeLocalTransform( self.handle, transform )
-end
-
---- Sets the emmissivity scale of the shape.
----
----@param self Shape
----@param scale number
-function shape_meta:SetEmissiveScale( scale )
-	assert( self:IsValid() )
-	return SetShapeEmissiveScale( self.handle, scale )
-end
-
---- Sets the collision filter of the shape.
---- A shape will only collide with another if the following is true:
---- ```
---- (A.layer & B.mask) && (B.layer & A.mask)
---- ```
----
----@param self Shape
----@param layer? number bit array (8 bits, 0-255)
----@param mask? number bit mask (8 bits, 0-255)
-function shape_meta:SetCollisionFilter( layer, mask )
-	SetShapeCollisionFilter( self.handle, layer or 1, mask or 255 )
-end
-
---- Gets the transform of the shape relative to its body.
----
----@param self Shape
----@return Transformation
-function shape_meta:GetLocalTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetShapeLocalTransform( self.handle ) )
-end
-
---- Gets the transform of the shape.
----
----@param self Shape
----@return Transformation
-function shape_meta:GetWorldTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetShapeWorldTransform( self.handle ) )
-end
-
---- Gets the body of this shape.
----
----@param self Shape
----@return Body
-function shape_meta:GetBody()
-	assert( self:IsValid() )
----@diagnostic disable-next-line: return-type-mismatch
-	return Body( GetShapeBody( self.handle ) )
-end
-
---- Gets the joints attached to this shape.
----
----@param self Shape
----@return Joint[]
-function shape_meta:GetJoints()
-	assert( self:IsValid() )
-	local joints = GetShapeJoints( self.handle )
-	for i = 1, #joints do
-		joints[i] = Joint( joints[i] )
-	end
-	return joints
-end
-
---- Gets the lights attached to this shape.
----
----@param self Shape
----@return Light[]
-function shape_meta:GetLights()
-	assert( self:IsValid() )
-	local lights = GetShapeLights( self.handle )
-	for i = 1, #lights do
-		lights[i] = Light( lights[i] )
-	end
-	return lights
-end
-
---- Gets the bounds of the shape.
----
----@param self Shape
----@return Vector min
----@return Vector max
-function shape_meta:GetWorldBounds()
-	assert( self:IsValid() )
-	local min, max = GetShapeBounds( self.handle )
-	return MakeVector( min ), MakeVector( max )
-end
-
---- Gets the material and color of the shape at the specified position.
----
----@param self Shape
----@param pos vector
----@return string type
----@return number r
----@return number g
----@return number b
----@return number a
-function shape_meta:GetMaterialAtPos( pos )
-	assert( self:IsValid() )
-	return GetShapeMaterialAtPosition( self.handle, pos )
-end
-
---- Gets the size of the shape in voxels.
----
----@param self Shape
----@return number x
----@return number y
----@return number z
----@return number scale
-function shape_meta:GetSize()
-	assert( self:IsValid() )
-	return GetShapeSize( self.handle )
-end
-
---- Gets the count of voxels in the shape.
----
----@param self Shape
----@return number
-function shape_meta:GetVoxelCount()
-	assert( self:IsValid() )
-	return GetShapeVoxelCount( self.handle )
-end
-
---- Gets the closest point to the shape from a given origin.
----
----@param self Shape
----@param origin vector
----@return boolean hit
----@return Vector? point
----@return Vector? normal
-function shape_meta:GetClosestPoint( origin )
-	local hit, point, normal = GetShapeClosestPoint( self.handle, origin )
-	if not hit then
-		return false
-	end
-	return hit, MakeVector( point ), MakeVector( normal )
-end
-
---- Gets all the shapes touching the shape
----
----@param self Shape
----@return Shape[] shapes
-function shape_meta:GetTouching()
-	local min, max = self:GetWorldBounds()
-	local potential = QueryAabbShapes( min - { 0.1, 0.1, 0.1 }, max + { 0.1, 0.1, 0.1 } )
-	local found = {}
-	for i = 1, #potential do
-		if potential[i] ~= self.handle and self:IsTouching( potential[i] ) then
-			found[#found+1] = Shape( potential[i] )
-		end
-	end
-	return found
-end
-
---- Gets if the shape is currently visible.
----
----@param self Shape
----@param maxDist number
----@param rejectTransparent? boolean
----@return boolean
-function shape_meta:IsVisible( maxDist, rejectTransparent )
-	assert( self:IsValid() )
-	return IsShapeVisible( self.handle, maxDist, rejectTransparent )
-end
-
---- Gets if the shape has been broken.
----
----@param self Shape
----@return boolean
-function shape_meta:IsBroken()
-	return not self:IsValid() or IsShapeBroken( self.handle )
-end
-
---- Gets if the shape is touching a given shape.
----
----@param self Shape
----@param shape Shape | integer
----@return boolean
-function shape_meta:IsTouching( shape )
-	assert( self:IsValid() )
-	local shapeHandle = GetEntityHandle( shape )
-	---@cast shapeHandle shape_handle
-	return IsShapeTouching( self.handle, shapeHandle )
-end
-
-----------------
--- Properties implementation
-
----@param self Shape
----@param setter boolean
----@param val transform
----@return Transformation?
-function shape_meta._C:transform( setter, val )
-	if setter then
-		self:SetLocalTransform( val )
-	else
-		return self:GetLocalTransform()
-	end
-end
-
----@param self Shape
----@param setter boolean
----@param val number
-function shape_meta._C:emissive( setter, val )
-	assert(setter, "cannot get emissive")
-	self:SetEmissiveScale( val )
-end
-
----@param self Shape
----@param setter boolean
----@return Body
-function shape_meta._C:body( setter )
-	assert(not setter, "cannot set body")
-	return self:GetBody()
-end
-
----@param self Shape
----@param setter boolean
----@return Joint[]
-function shape_meta._C:joints( setter )
-	assert(not setter, "cannot set joints")
-	return self:GetJoints()
-end
-
----@param self Shape
----@param setter boolean
----@return Light[]
-function shape_meta._C:lights( setter )
-	assert(not setter, "cannot set lights")
-	return self:GetLights()
-end
-
----@param self Shape
----@param setter boolean
----@return Vector
-function shape_meta._C:size( setter )
-	assert(not setter, "cannot set size")
-	return Vector( self:GetSize() )
-end
-
----@param self Shape
----@param setter boolean
----@return boolean
-function shape_meta._C:broken( setter )
-	assert(not setter, "cannot set broken")
-	return self:IsBroken()
-end
-
- end)();
---src/entities/trigger.lua
-(function() ----------------
--- Trigger class and related functions
--- @script entities.trigger
-
----@class trigger_handle: integer
-
----@class Trigger: Entity
----@field handle trigger_handle
----@field private _C table property contrainer (internal)
----@field transform Transformation (dynamic property)
-local trigger_meta
-trigger_meta = global_metatable( "trigger", "entity", true )
-
---- Tests if the parameter is a trigger entity.
----
----@param e any
----@return boolean
-function IsTrigger( e )
-	return IsEntity( e ) and e.type == "trigger"
-end
-
---- Wraps the given handle with the trigger class.
----
----@param handle number
----@return Trigger?
-function Trigger( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "trigger", { handle = handle, type = "trigger" } )
-	end
-end
-
---- Finds a trigger with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Trigger?
-function FindTriggerByTag( tag, global )
-	return Trigger( FindTrigger( tag, global ) )
-end
-
---- Finds all triggers with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Trigger[]
-function FindTriggersByTag( tag, global )
-	local t = FindTriggers( tag, global )
-	for i = 1, #t do
-		t[i] = Trigger( t[i] )
-	end
-	return t
-end
-
----@type Trigger
-
----@param self Trigger
----@return string
-function trigger_meta:__tostring()
-	return string.format( "Trigger[%d]", self.handle )
-end
-
---- Sets the transform of the trigger.
----
----@param self Trigger
----@param transform transform
-function trigger_meta:SetTransform( transform )
-	assert( self:IsValid() )
-	return SetTriggerTransform( self.handle, transform )
-end
-
---- Gets the transform of the trigger.
----
----@param self Trigger
----@return Transformation
-function trigger_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetTriggerTransform( self.handle ) )
-end
-
---- Gets the distance to the trigger from a given origin.
---- Negative values indicate the origin is inside the trigger.
----
----@param self Trigger
----@param origin vector
-function trigger_meta:GetDistance( origin )
-	return GetTriggerDistance( self.handle, origin )
-end
-
---- Gets the closest point to the trigger from a given origin.
----
----@param self Trigger
----@param origin vector
-function trigger_meta:GetClosestPoint( origin )
-	return MakeVector( GetTriggerClosestPoint( self.handle, origin ) )
-end
-
---- Gets the bounds of the trigger.
----
----@param self Trigger
----@return Vector min
----@return Vector max
-function trigger_meta:GetWorldBounds()
-	assert( self:IsValid() )
-	local min, max = GetTriggerBounds( self.handle )
-	return MakeVector( min ), MakeVector( max )
-end
-
---- Gets if the specified body is in the trigger.
----
----@param self Trigger
----@param handle Body | number
----@return boolean
-function trigger_meta:IsBodyInTrigger( handle )
-	assert( self:IsValid() )
-	local bodyHandle = GetEntityHandle( handle )
-	---@cast bodyHandle body_handle
-	return IsBodyInTrigger( self.handle, bodyHandle )
-end
-
---- Gets if the specified vehicle is in the trigger.
----
----@param self Trigger
----@param handle Vehicle | number
----@return boolean
-function trigger_meta:IsVehicleInTrigger( handle )
-	assert( self:IsValid() )
-	local vehicleHandle = GetEntityHandle( handle )
-	---@cast vehicleHandle vehicle_handle
-	return IsVehicleInTrigger( self.handle, vehicleHandle )
-end
-
---- Gets if the specified shape is in the trigger.
----
----@param self Trigger
----@param handle Shape | number
----@return boolean
-function trigger_meta:IsShapeInTrigger( handle )
-	assert( self:IsValid() )
-	local shapeHandle = GetEntityHandle( handle )
-	---@cast shapeHandle shape_handle
-	return IsShapeInTrigger( self.handle, shapeHandle )
-end
-
---- Gets if the specified point is in the trigger.
----
----@param self Trigger
----@param point vector
----@return boolean
-function trigger_meta:IsPointInTrigger( point )
-	assert( self:IsValid() )
-	return IsPointInTrigger( self.handle, point )
-end
-
---- Gets if the trigger is empty.
----
----@param self Trigger
----@param demolision boolean
----@return boolean empty
----@return Vector? highpoint
-function trigger_meta:IsEmpty( demolision )
-	assert( self:IsValid() )
-	local empty, highpoint = IsTriggerEmpty( self.handle, demolision )
-	return empty, highpoint and MakeVector( highpoint )
-end
-
-----------------
--- Properties implementation
-
----@param self Trigger
----@param setter boolean
----@param val transform
----@return Transformation?
-function trigger_meta._C:transform( setter, val )
-	if setter then
-		self:SetTransform( val )
-	else
-		return self:GetTransform()
-	end
-end
-
- end)();
---src/entities/vehicle.lua
-(function() ----------------
--- Vehicle class and related functions
--- @script entities.vehicle
-
----@class vehicle_handle: integer
-
----@class Vehicle: Entity
----@field handle vehicle_handle
----@field private _C table property contrainer (internal)
----@field transform Transformation (dynamic property -- readonly)
----@field body Body (dynamic property -- readonly)
----@field health number (dynamic property -- readonly)
-local vehicle_meta = global_metatable( "vehicle", "entity", true )
-
---- Tests if the parameter is a vehicle entity.
----
----@param e any
----@return boolean
-function IsVehicle( e )
-	return IsEntity( e ) and e.type == "vehicle"
-end
-
---- Wraps the given handle with the vehicle class.
----
----@param handle number
----@return Vehicle?
-function Vehicle( handle )
-	if handle > 0 then
-		return instantiate_global_metatable( "vehicle", { handle = handle, type = "vehicle" } )
-	end
-end
-
---- Finds a vehicle with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Vehicle?
-function FindVehicleByTag( tag, global )
-	return Vehicle( FindVehicle( tag, global ) )
-end
-
---- Finds all vehicles with the specified tag.
---- `global` determines whether to only look in the script's hierarchy or the entire scene.
----
----@param tag string
----@param global boolean
----@return Vehicle[]
-function FindVehiclesByTag( tag, global )
-	local t = FindVehicles( tag, global )
-	for i = 1, #t do
-		t[i] = Vehicle( t[i] )
-	end
-	return t
-end
-
----@type Vehicle
-
----@param self Vehicle
----@return string
-function vehicle_meta:__tostring()
-	return string.format( "Vehicle[%d]", self.handle )
-end
-
---- Drives the vehicle by setting its controls.
----
----@param self Vehicle
----@param drive number
----@param steering number
----@param handbrake boolean
-function vehicle_meta:Drive( drive, steering, handbrake )
-	assert( self:IsValid() )
-	return DriveVehicle( self.handle, drive, steering, handbrake )
-end
-
---- Gets the transform of the vehicle.
----
----@param self Vehicle
----@return Transformation
-function vehicle_meta:GetTransform()
-	assert( self:IsValid() )
-	return MakeTransformation( GetVehicleTransform( self.handle ) )
-end
-
---- Gets the body of the vehicle.
----
----@param self Vehicle
----@return Body
-function vehicle_meta:GetBody()
-	assert( self:IsValid() )
-	local body = Body( GetVehicleBody( self.handle ) )
-	---@cast body Body
-	return body
-end
-
---- Gets the health of the vehicle.
----
----@param self Vehicle
----@return number
-function vehicle_meta:GetHealth()
-	assert( self:IsValid() )
-	-- TODO: calculate ourselves if we need to
-	return GetVehicleHealth( self.handle )
-end
-
---- Gets the position of the driver camera in object-space.
----
----@param self Vehicle
----@return Vector
-function vehicle_meta:GetDriverPos()
-	assert( self:IsValid() )
-	return MakeVector( GetVehicleDriverPos( self.handle ) )
-end
-
---- Gets the position of the driver camera in world-space.
----
----@param self Vehicle
----@return Vector
-function vehicle_meta:GetGlobalDriverPos()
-	return self:GetTransform():ToGlobal( self:GetDriverPos() )
-end
-
-----------------
--- Properties implementation
-
----@param self Vehicle
----@param setter boolean
----@return Transformation
-function vehicle_meta._C:transform( setter )
-	assert(not setter, "cannot set transform")
-	return self:GetTransform()
-end
-
----@param self Vehicle
----@param setter boolean
----@return Body
-function vehicle_meta._C:body( setter )
-	assert(not setter, "cannot set body")
-	return self:GetBody()
-end
-
----@param self Vehicle
----@param setter boolean
----@return number
-function vehicle_meta._C:health( setter )
-	assert(not setter, "cannot set health")
-	return self:GetHealth()
-end
-
- end)();
---src/animation/animation.lua
-(function() 
-local animator_meta = global_metatable( "animator" )
-
-function animator_meta:Update( dt )
-	self.value = self._func( self._state, self._modifier * dt ) or self._state.value or 0
-	return self.value
-end
-
-function animator_meta:Reset()
-	self._state = {}
-	if self._init then
-		self._init( self._state )
-	end
-	self.value = self._state.value or 0
-end
-
-function animator_meta:SetModifier( num )
-	self._modifier = num
-end
-
-function animator_meta:__newindex( k, v )
-	self._state[k] = v
-end
-
-function animator_meta:__index( k )
-	local v = animator_meta[k]
-	if v then
-		return v
-	end
-	return rawget( self, "_state" )[k]
-end
-
-Animator = {
-	Base = function( easing )
-		local t = instantiate_global_metatable( "animator", {
-			_state = {},
-			_func = type( easing ) == "table" and easing.update or easing,
-			_init = type( easing ) == "table" and easing.init,
-			_modifier = 1,
-			value = 0,
-		} )
-		if t._init then
-			t._init( t._state )
-		end
-		return t
-	end,
-}
-
-Animator.LinearApproach = function( init, speed, down_speed )
-	return Animator.Base {
-		update = function( state, dt )
-			if state.target < state.value then
-				state.value = state.value + math.max( state.target - state.value, dt * state.down_speed )
-			elseif state.target > state.value then
-				state.value = state.value + math.min( state.target - state.value, dt * state.speed )
-			end
-		end,
-		init = function( state )
-			state.value = init
-			state.speed = speed
-			state.down_speed = down_speed or -speed
-			state.target = init
-		end,
-	}
-end
-
-Animator.SpeedLinearApproach = function( init, acceleration, down_acceleration )
-	return Animator.Base {
-		update = function( state, dt )
-			state.driver.target = state.target
-			state.driver.speed = state.acceleration
-			state.driver.down_speed = state.down_acceleration
-			state.value = state.value + state.driver:Update( dt ) * dt
-		end,
-		init = function( state )
-			state.driver = Animator.LinearApproach( init, acceleration )
-			state.target = init
-			state.acceleration = acceleration
-			state.down_acceleration = down_acceleration
-			state.value = 0
-		end,
-	}
-end
-
- end)();
---src/animation/armature.lua
-(function() ----------------
--- Armature library
--- @script animation.armature
-
----@class Armature
----@field refs any
----@field root any
----@field scale number | nil
----@field dirty boolean
-local armature_meta
-armature_meta = global_metatable( "armature" )
-
---[[
-
-Armature {
-    shapes = {
-        "core_2",
-        "core_1",
-        "core_0",
-        "arm_21",
-        "arm_11",
-        "arm_01",
-        "arm_20",
-        "arm_10",
-        "arm_00",
-        "body"
-    },
-
-    bones = {
-        name = "root",
-        shapes = {
-            body = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-        },
-        {
-            name = "core_0",
-            shapes = {
-                core_0 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "core_1",
-            shapes = {
-                core_1 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "core_2",
-            shapes = {
-                core_2 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "arm_00",
-            shapes = {
-                arm_00 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_01",
-                shapes = {
-                    arm_01 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-        {
-            name = "arm_10",
-            shapes = {
-                arm_10 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_11",
-                shapes = {
-                    arm_11 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-        {
-            name = "arm_20",
-            shapes = {
-                arm_20 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_21",
-                shapes = {
-                    arm_21 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-    }
-}
-
-]]
-
---- Loads armature information from a prefab and a list of shapes.
----
----@param xml string
----@param parts table[]
----@param scale? number
-function LoadArmatureFromXML( xml, parts, scale ) -- Example below
-	scale = scale or 1
-	local dt = ParseXML( xml )
-	assert( (dt.type == "prefab" and dt.children[1] and dt.children[1].type == "group") or dt.type == "group", "Invalid Tool XML" )
-	local shapes = {}
-	local offsets = {}
-	for i = 1, #parts do
-		if type( parts[i] ) == "string" then
-			shapes[i] = parts[i] -- Offset computed at runtime
-		else
-			shapes[i] = parts[i][1]
-			local v = parts[i][2]
-			-- Compensate for the editor placing vox parts relative to the center of the base
-			offsets[parts[i][1]] = Vec( math.floor( v[1] / 2 ) / 10, 0, -math.floor( v[2] / 2 ) / 10 )
-		end
-	end
-
-	local function parseVec( str )
-		if not str then
-			return Vec( 0, 0, 0 )
-		end
-		local x, y, z = str:match( "([%d.-]+) ([%d.-]+) ([%d.-]+)" )
-		return Vec( tonumber( x ), tonumber( y ), tonumber( z ) )
-	end
-
-	local function parseTransform( attr )
-		local pos, angv = parseVec( attr.pos ), parseVec( attr.rot )
-		return Transform( Vec( pos[1], pos[2], pos[3] ), QuatEuler( angv[1], angv[2], angv[3] ) )
-	end
-
-	local function translatebone( node, isLocation )
-		local t = { name = node.attributes.name, transform = parseTransform( node.attributes ) }
-		local sub = t
-		if not isLocation then
-			t.name = "__FIXED_" .. node.attributes.name
-			t[1] = { name = node.attributes.name }
-			sub = t[1]
-		end
-		sub.shapes = {}
-		for i = 1, #node.children do
-			local child = node.children[i]
-			if child.type == "vox" then
-				local name = child.attributes.object
-				local tr = parseTransform( child.attributes )
-				local s = child.attributes.scale and tonumber( child.attributes.scale ) or 1
-				local shape = {
-					id = name,
-					attributes = child.attributes,
-				}
-				if offsets[name] then
-					shape.transform = TransformToParentTransform( tr, Transform(
-						VecScale( offsets[name], -s ),
-						QuatEuler( -90, 0, 0 )
-					) )
-				else
-					shape.transform = tr
-					shape.reoffset_scale = s
-				end
-				table.insert( sub.shapes, shape )
-			elseif child.type == "group" then
-				sub[#sub + 1] = translatebone( child )
-			elseif child.type == "location" then
-				sub[#sub + 1] = translatebone( child, true )
-			end
-		end
-		return t
-	end
-	local bones = translatebone( dt.type == "prefab" and dt.children[1] or dt )[1]
-	bones.transform = Transform( Vec(), QuatEuler( 0, 0, 0 ) )
-	bones.name = "root"
-
-	local arm = Armature { shapes = shapes, scale = scale, bones = bones }
-	arm:ComputeBones()
-	return arm, dt
-end
---[=[
---[[---------------------------------------------------
-    LoadArmatureFromXML is capable of taking the XML of a prefab and turning it into a useable armature object for tools and such.
-    Two things are required: the XML of the prefab itself, and a list of all the objects inside the vox for position correction.
-    The list of objects should be as it appears in MagicaVoxel, with every slot corresponding to an object in the vox file.
-    One notable limitation is that there can only be one vox file used and that all the objects inside it can only be used once.
---]]---------------------------------------------------
-
--- Loading the armature from the prefab and the objects list
-local armature = LoadArmatureFromXML([[
-<prefab version="0.7.0">
-    <group id_="1196432640" open_="true" name="instance=MOD/physgun.xml" pos="-3.4 0.7 0.0" rot="0.0 0.0 0.0">
-        <vox id_="1866644736" pos="-0.125 -0.125 0.125" file="MOD/physgun.vox" object="body" scale="0.5"/>
-        <group id_="279659168" open_="true" name="core0" pos="0.0 0.0 -0.075" rot="0.0 0.0 0.0">
-            <vox id_="496006720" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_0" scale="0.5"/>
-        </group>
-        <group id_="961930560" open_="true" name="core1" pos="0.0 0.0 -0.175" rot="0.0 0.0 0.0">
-            <vox id_="1109395584" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_1" scale="0.5"/>
-        </group>
-        <group id_="806535232" open_="true" name="core2" pos="0.0 0.0 -0.275" rot="0.0 0.0 0.0">
-            <vox id_="378362432" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_2" scale="0.5"/>
-        </group>
-        <group id_="1255943040" open_="true" name="arms_rot" pos="0.0 0.0 -0.375" rot="0.0 0.0 0.0">
-            <group id_="439970016" open_="true" name="arm0_base" pos="0.0 0.1 0.0" rot="0.0 0.0 0.0">
-                <vox id_="1925106432" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_00" scale="0.5"/>
-                <group id_="2122316288" open_="true" name="arm0_tip" pos="0.0 0.2 -0.0" rot="0.0 0.0 0.0">
-                    <vox id_="572557440" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_01" scale="0.5"/>
-                </group>
-            </group>
-            <group id_="516324128" open_="true" name="arm1_base" pos="0.087 -0.05 0.0" rot="180.0 180.0 -60.0">
-                <vox id_="28575440" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_10" scale="0.5"/>
-                <group id_="962454912" open_="true" name="arm1_tip" pos="0.0 0.2 0.0" rot="0.0 0.0 0.0">
-                    <vox id_="1966724352" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_11" scale="0.5"/>
-                </group>
-            </group>
-            <group id_="634361664" open_="true" name="arm2_base" pos="-0.087 -0.05 0.0" rot="180.0 180.0 60.0">
-                <vox id_="1049360960" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_20" scale="0.5"/>
-                <group id_="1428116608" open_="true" name="arm2_tip" pos="0.0 0.2 0.0" rot="0.0 0.0 0.0">
-                    <vox id_="1388661504" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_21" scale="0.5"/>
-                </group>
-            </group>
-        </group>
-        <group id_="1569551872" open_="true" name="nozzle" pos="0.0 0.0 -0.475">
-            <vox id_="506099872" pos="-0.025 -0.125 0.1" file="MOD/physgun.vox" object="cannon" scale="0.5"/>
-        </group>
-    </group>
-</prefab>
-]], {
-    -- The list of objects as it appears in MagicaVoxel. Each entry has the name of the object followed by the size as seen in MagicaVoxel.
-    -- Please note that the order MUST be the same as in MagicaVoxel and that there can be no gaps.
-    {"cannon", Vec(5, 3, 5)},
-    {"core_2", Vec(5, 2, 5)},
-    {"core_1", Vec(5, 2, 5)},
-    {"core_0", Vec(5, 2, 5)},
-    {"arm_21", Vec(1, 1, 2)},
-    {"arm_11", Vec(1, 1, 2)},
-    {"arm_01", Vec(1, 1, 2)},
-    {"arm_20", Vec(1, 1, 4)},
-    {"arm_10", Vec(1, 1, 4)},
-    {"arm_00", Vec(1, 1, 4)},
-    {"body", Vec(9, 6, 5)}
-})
------------------------------------------------------
-
--- Every frame you can animate the armature by setting the local transform of bones and then applying the changes to the shapes of the object.
-armature:SetBoneTransform("core0", Transform(Vec(), QuatEuler(0, 0, GetTime()*73)))
-armature:SetBoneTransform("core1", Transform(Vec(), QuatEuler(0, 0, -GetTime()*45)))
-armature:SetBoneTransform("core2", Transform(Vec(), QuatEuler(0, 0, GetTime()*83)))
-armature:SetBoneTransform("arms_rot", Transform(Vec(), QuatEuler(0, 0, GetTime()*20)))
-local tr = Transform(Vec(0,0,0), QuatEuler(-40 + 5 * math.sin(GetTime()), 0, 0))
-armature:SetBoneTransform("arm0_base", tr)
-armature:SetBoneTransform("arm0_tip", tr)
-armature:SetBoneTransform("arm1_base", tr)
-armature:SetBoneTransform("arm1_tip", tr)
-armature:SetBoneTransform("arm2_base", tr)
-armature:SetBoneTransform("arm2_tip", tr)
--- shapes is the list of all the shapes of the vox, it can be obtained with GetBodyShapes()
-armature:Apply(shapes)
-
---]=]
-
---- Creates a new armature.
----
----@param definition table
----@return Armature
-function Armature( definition )
-	local ids = {}
-	for i, name in ipairs( definition.shapes ) do
-		ids[name] = #definition.shapes - i + 1
-	end
-	local armature = {
-		root = definition.bones,
-		refs = {},
-		scale = definition.scale,
-		__noquickload = function()
-		end,
-		dirty = true,
-	}
-	local function dobone( b )
-		if b.name then
-			armature.refs[b.name] = b
-		end
-		b.transform = b.transform or Transform()
-		b.shapes = b.shapes or {}
-		b.dirty = true
-		for i = 1, #b.shapes do
-			local shape = b.shapes[i]
-			shape.num = ids[shape.id]
-			shape.transform.pos = VecScale( shape.transform.pos, definition.scale or 1 )
-		end
-		b.children = {}
-		for i = 1, #b do
-			b.children[i] = dobone( b[i] )
-		end
-		return b
-	end
-	dobone( armature.root )
-	return instantiate_global_metatable( "armature", armature )
-end
-
----@type Armature
-
-local function computebone( bone, transform, scale, dirty )
-	dirty = dirty or bone.dirty or bone.jiggle_transform
-	if dirty or not bone.gr_transform then
-		bone.gr_transform = TransformToParentTransform( transform, bone.transform )
-		if bone.jiggle_transform then
-			bone.gr_transform = TransformToParentTransform( bone.gr_transform, bone.jiggle_transform )
-		end
-		bone.g_transform = Transform( VecScale( bone.gr_transform.pos, scale ), bone.gr_transform.rot )
-		bone.dirty = false
-	end
-	for i = 1, #bone.children do
-		computebone( bone.children[i], bone.gr_transform, scale, dirty )
-	end
-end
-
---- Computes the bone positions.
-function armature_meta:ComputeBones()
-	computebone( self.root, Transform(), self.scale or 1 )
-	self.dirty = false
-end
-
-local function applybone( shapes, bone )
-	for i = 1, #bone.shapes do
-		local offset = bone.shapes[i]
-		local handle = GetEntityHandle and GetEntityHandle( shapes[offset.num] ) or shapes[offset.num]
-		---@cast handle shape_handle
-		SetShapeLocalTransform( handle, TransformToParentTransform( bone.g_transform, offset.transform ) )
-	end
-	for i = 1, #bone.children do
-		applybone( shapes, bone.children[i] )
-	end
-end
-
---- Applies the bone positions to a list of shapes.
----
---- Deprecated: Use `Armature:GetShapeTransforms()` instead.
----
----@param shapes Shape[] | number[]
----@deprecated
-function armature_meta:Apply( shapes )
-	if self.dirty or self.jiggle then
-		self:ComputeBones()
-	end
-	applybone( shapes, self.root )
-end
-
-local function getshapetransforms( offsets, bone )
-	for i = 1, #bone.shapes do
-		local shape = bone.shapes[i]
-		shape.global_transform = TransformToParentTransform( bone.g_transform, shape.transform )
-		offsets[#offsets + 1] = shape
-	end
-	for i = 1, #bone.children do
-		getshapetransforms( offsets, bone.children[i] )
-	end
-end
-
---- Get all the global shape transforms from the armature.
----
----@return { id: string, global_transform: transform }[] offsets
-function armature_meta:GetShapeTransforms()
-	if self.dirty or self.jiggle then
-		self:ComputeBones()
-	end
-	local offsets = {}
-	getshapetransforms( offsets, self.root )
-	return offsets
-end
-
---- Sets the local transform of a bone.
----
----@param bone string
----@param transform transform
-function armature_meta:SetBoneTransform( bone, transform )
-	local b = self.refs[bone]
-	if not b then
-		return
-	end
-	self.dirty = true
-	b.dirty = true
-	b.transform = transform
-end
-
---- Gets the local transform of a bone.
----
----@param bone string
----@return Transformation
-function armature_meta:GetBoneTransform( bone )
-	local b = self.refs[bone]
-	if not b then
-		return Transformation()
-	end
-	return b.transform
-end
-
---- Gets the global transform of a bone.
----
----@param bone string
----@return Transformation
-function armature_meta:GetBoneGlobalTransform( bone )
-	local b = self.refs[bone]
-	if not b then
-		return Transformation()
-	end
-	if self.dirty then
-		self:ComputeBones()
-	end
-	return b.g_transform
-end
-
----@alias JiggleConstaint { gravity?: number }
-
---- Sets the jiggle constraints of a bone.
----
----@param bone string
----@param jiggle number
----@param constraint? JiggleConstaint
-function armature_meta:SetBoneJiggle( bone, jiggle, constraint )
-	local b = self.refs[bone]
-	if not b then
-		return
-	end
-	self.dirty = true
-	if jiggle > 0 then
-		self.jiggle = true
-	end
-	b.jiggle = math.atan( jiggle ) / math.pi * 2
-	b.jiggle_constraint = constraint
-end
-
---- Gets the jiggle constraints of a bone.
----
----@param bone string
----@return number jiggle
----@return JiggleConstaint? constraints
-function armature_meta:GetBoneJiggle( bone )
-	local b = self.refs[bone]
-	if not b then
-		return 0
-	end
-	return b.jiggle, b.jiggle_constraint
-end
-
---- Resets the jiggle state of all bones.
-function armature_meta:ResetJiggle()
-	for _, b in pairs( self.refs ) do
-		b.jiggle_transform = nil
-	end
-	self.dirty = true
-end
-
-local function updatebone( bone, current_transform, prev_transform, dt, gravity )
-	local current_transform_local = TransformToParentTransform( current_transform, bone.transform )
-	local prev_transform_local = TransformToParentTransform( prev_transform, bone.old_transform or bone.transform )
-	bone.old_transform = bone.transform
-	if bone.jiggle then
-		prev_transform_local = TransformToParentTransform( prev_transform_local, bone.jiggle_transform or Transform() )
-
-		local local_diff = TransformToLocalTransform( current_transform_local, prev_transform_local )
-		local target = TransformToParentPoint( local_diff, Vec( 0, 0, -2 / dt ) )
-
-		if bone.jiggle_constraint and bone.jiggle_constraint.gravity then
-			target = VecAdd( target,
-			                 TransformToLocalVec( current_transform_local, VecScale( gravity, bone.jiggle_constraint.gravity ) ) )
-		end
-
-		local lookat = QuatLookAt( Vec(), target )
-
-		bone.jiggle_transform = Transform( Vec(), QuatSlerp( lookat, QuatEuler( 0, 0, 0 ), 1 - bone.jiggle ) )
-		current_transform_local = TransformToParentTransform( current_transform_local, bone.jiggle_transform )
-	end
-	for i = 1, #bone.children do
-		updatebone( bone.children[i], current_transform_local, prev_transform_local, dt, gravity )
-	end
-end
-
---- Updates the physics of the armature.
----
----@param diff transform
----@param dt number
----@param gravity? vector
-function armature_meta:UpdatePhysics( diff, dt, gravity )
-	dt = dt or 0.01666
-	updatebone( self.root, Transform(), Transform( VecScale( diff.pos, 1 / dt ), diff.rot ), dt, gravity or Vec( 0, -10, 0 ) )
-end
-
-local function DebugAxis( tr, s )
-	s = s or 1
-	DebugLine( tr.pos, TransformToParentPoint( tr, Vec( 1 * s, 0, 0 ) ), 1, 0, 0 )
-	DebugLine( tr.pos, TransformToParentPoint( tr, Vec( 0, 1 * s, 0 ) ), 0, 1, 0 )
-	DebugLine( tr.pos, TransformToParentPoint( tr, Vec( 0, 0, 1 * s ) ), 0, 0, 1 )
-end
-
---- Draws debug info of the armature at the specified transform.
----
----@param transform? transform
-function armature_meta:DrawDebug( transform )
-	transform = transform or Transform()
-	DebugAxis( transform, 0.05 )
-	for k, v in pairs( self.refs ) do
-		local r = TransformToParentTransform( transform, v.g_transform )
-		local g = v.name:find( "^__FIXED_" ) and 1 or 0
-		for i = 1, #v.children do
-			DebugLine( r.pos, TransformToParentTransform( transform, v.children[i].g_transform ).pos, 1, 1 - g, g, .4 )
-		end
-		for i = 1, #v.shapes do
-			local offset = v.shapes[i]
-			local p = TransformToParentTransform( transform, TransformToParentTransform( v.g_transform, offset.tr ) )
-			DebugAxis( p, 0.03 )
-			DebugLine( r.pos, p.pos, 0, 1, 1, .4 )
-		end
-	end
-end
-
- end)();
---src/tool/tool.lua
-(function() ----------------
--- Tool Framework
--- @script tool.tool
-
----@type table<string, Tool2>
-local UMF_tools = {}
-local post_init = false
-local previous
-local current_hook
-local current_hook_updated
-local transform_info = {}
-
--- #region Armature
-
-local function offset_shape( editor_transform, scale, x, y )
-	local vec = VecScale( Vec( -math.floor( x / 2 ), 0, math.floor( y / 2 ) ), scale / 10 )
-	return TransformToParentTransform( editor_transform, Transform( vec, QuatEuler( -90, 0, 0 ) ) )
-end
-
-local function parseVec( str )
-	if not str then
-		return Vec( 0, 0, 0 )
-	end
-	local x, y, z = str:match( "([%d.-]+) ([%d.-]+) ([%d.-]+)" )
-	return Vec( tonumber( x ), tonumber( y ), tonumber( z ) )
-end
-
-local function parseTransform( attr )
-	local pos, angv = parseVec( attr.pos ), parseVec( attr.rot )
-	return Transform( Vec( pos[1], pos[2], pos[3] ), QuatEuler( angv[1], angv[2], angv[3] ) )
-end
-
-local id_counter = 0
-local function translatebone( node, isLocation, modelinfo )
-	modelinfo = modelinfo or { vox = {} }
-	local t = { name = node.attributes.name, transform = parseTransform( node.attributes ) }
-	local sub = t
-	if not isLocation then
-		t.name = "__FIXED_" .. (node.attributes.name or "UNKNOWN")
-		t[1] = { name = node.attributes.name }
-		sub = t[1]
-	end
-	sub.shapes = {}
-	for i = 1, #node.children do
-		local child = node.children[i]
-		if child.type == "vox" then
-			id_counter = id_counter + 1
-			child.attributes.tags = (child.attributes.tags or "") .. " __UMF_TOOL_SHAPE_ID=" .. id_counter
-			child.id = id_counter
-			table.insert( sub.shapes, {
-				id = id_counter,
-				attributes = child.attributes,
-				transform = Transform(),
-				editor_transform = parseTransform( child.attributes ),
-				scale = child.attributes.scale and tonumber( child.attributes.scale ) or 1,
-			} )
-			table.insert( modelinfo.vox, child )
-		elseif child.type == "voxbox" then
-			id_counter = id_counter + 1
-			child.attributes.tags = (child.attributes.tags or "") .. " __UMF_TOOL_SHAPE_ID=" .. id_counter
-			table.insert( sub.shapes, {
-				id = id_counter,
-				attributes = child.attributes,
-				transform = parseTransform( child.attributes ),
-				scale = child.attributes.scale and tonumber( child.attributes.scale ) or 1,
-			} )
-			child.id = id_counter
-		elseif child.type == "group" then
-			sub[#sub + 1] = translatebone( child, false, modelinfo )
-		elseif child.type == "location" then
-			sub[#sub + 1] = translatebone( child, true, modelinfo )
-		end
-	end
-	return t, modelinfo
-end
-
-local function load_xml( xml )
-	local dt = ParseXML( xml )
-	local root = dt.type == "prefab" and dt.children[1] or dt
-	assert( root and root.type == "group", "Invalid Tool XML" )
-	local root_bone, modelinfo = translatebone( root )
-	root_bone.name = "root"
-	root_bone.transform = Transform() -- root bone is always at the "origin"
-
-	local armature = Armature { shapes = {}, bones = root_bone }
-	armature:ComputeBones()
-	armature.spawnable = root:Render()
-	armature.modelinfo = modelinfo
-
-	return armature, root
-end
-
-local allowed_types = { screen = true, light = true }
-local function attach_armature( armature, tool_body )
-	if not armature or not armature.spawnable then
-		return
-	end
-
-	local tool_shapes = GetBodyShapes( tool_body )
-	for i = 1, #tool_shapes do
-		Delete( tool_shapes[i] )
-	end
-
-	armature.shapes = {}
-	local spawned = Spawn( armature.spawnable, Transform( Vec( 10000, 10000, 10000 ) ), true, false )
-	local last
-	local removelist = {}
-	for i = 1, #spawned do
-		local etype = GetEntityType( spawned[i] )
-		if etype == "shape" then
-			local id = tonumber( GetTagValue( spawned[i], "__UMF_TOOL_SHAPE_ID" ) )
-			if id then
-				armature.shapes[id] = spawned[i]
-				if HasTag( spawned[i], "collider" ) and not last then
-					last = spawned[i]
-				else
-					SetShapeBody( spawned[i], tool_body )
-				end
-			else
-				removelist[#removelist + 1] = i
-			end
-		elseif not allowed_types[etype] then
-			removelist[#removelist + 1] = i
-		end
-	end
-	if last then
-		SetShapeBody( last, tool_body )
-	end
-
-	local shapes_data = armature:GetShapeTransforms()
-	for i = 1, #shapes_data do
-		local data = shapes_data[i]
-		---@diagnostic disable-next-line: undefined-field
-		if data.editor_transform then
-			local shape = armature.shapes[data.id]
-			data.transform = offset_shape( data.editor_transform, data.scale, GetShapeSize( shape ) )
-			-- data.editor_transform = nil
-		end
-	end
-
-	for i = 1, #removelist do
-		Delete( spawned[removelist[i]] )
-	end
-end
-
-local function detach_armature( armature )
-	if not armature or not armature.shapes then
-		return
-	end
-	for key, shape in pairs( armature.shapes ) do
-		Delete( shape )
-	end
-	armature.shapes = nil
-end
-
-local function apply_armature( armature )
-	if not armature then
-		return
-	end
-	local shapes_data = armature:GetShapeTransforms()
-	for i = 1, #shapes_data do
-		SetShapeLocalTransform( armature.shapes[shapes_data[i].id], shapes_data[i].global_transform )
-	end
-end
-
--- #endregion Armature
-
--- #region Metatable
-
----@class Tool2
----@field armature Armature|nil
----@field _C table
----@field model string
----@field printname string
----@field id string
----@field noregister boolean|nil
----@field group number|nil
-local tool_meta
-tool_meta = global_metatable( "tool", nil, true )
-
-function tool_meta._C:ammo( setter, val )
-	local key = "game.tool." .. self.id .. ".ammo"
-	local keystr = key .. ".display"
-	if setter then
-		if type( val ) == "number" then
-			SetFloat( key, val )
-			ClearKey( keystr )
-		else
-			SetFloat( key, 0 )
-			SetString( key .. ".display", tostring( val or "" ) )
-		end
-	elseif HasKey( keystr ) then
-		return GetString( keystr )
-	else
-		return GetFloat( key )
-	end
-end
-
-function tool_meta._C:enabled( setter, val )
-	local key = "game.tool." .. self.id .. ".enabled"
-	if setter then
-		SetBool( key, val )
-	else
-		return GetBool( key )
-	end
-end
-
---- Draws the tool in the world instead of the player view.
----
----@param self Tool2
----@param transform transform
-function tool_meta:DrawInWorld( transform )
-	SetToolTransform( TransformToLocalTransform( GetPlayerCameraTransform(), transform ) )
-end
-
-local function scale_transform( tr, s )
-	return Transform( VecLerp( Vec(), tr.pos, s ), QuatSlerp( Quat( 0, 0, 0, 1 ), tr.rot, s ) )
-end
-
-local function get_transform_info( key )
-	local t = transform_info[current_hook]
-	if not t then
-		t = {}
-		transform_info[current_hook] = t
-	end
-	if not current_hook_updated then
-		local current = GetBodyTransform( GetToolBody() )
-		t.old = t.current or current
-		t.olddt = t.currentdt or 1
-		t.current = current
-		t.currentdt = GetTimeStep()
-		t.diff = TransformToLocalTransform( t.current, t.old )
-		local rdiff = scale_transform( TransformToLocalTransform( t.old, t.current ), t.currentdt / t.olddt )
-		t.fix = TransformToParentTransform( t.current, rdiff )
-		current_hook_updated = true
-	end
-	return key and t[key] or t
-end
-
---- Gets the transform of the tool.
----
----@param self Tool2
----@return Transformation
-function tool_meta:GetTransform( predicted )
-	return MakeTransformation( get_transform_info( predicted and "fix" or "current" ) )
-end
-
---- Gets the transform delta of the tool.
----
----@return Transformation
-function tool_meta:GetTransformDelta()
-	return MakeTransformation( get_transform_info( "diff" ) )
-end
-
---- Gets the transform of a bone on the tool in world-space.
----
----@param self Tool2
----@param bone string
----@return Transformation
-function tool_meta:GetBoneGlobalTransform( bone, nopredicted )
-	if not self.armature then
-		return Transformation( Vec(), Quat() )
-	end
-	return self:GetTransform( not nopredicted ):ToGlobal( self.armature:GetBoneGlobalTransform( bone ) )
-end
-
---- Draws the debug armature of the tool.
----
----@param self Tool2
----@param nobones? boolean Don't draw bones.
----@param nobounds? boolean Don't draw bounds.
-function tool_meta:DrawDebug( nobones, nobounds, nopredicted )
-	if not self.armature then
-		return
-	end
-	local ptr = self:GetTransform( not nopredicted )
-	if not nobones then
-		self.armature:DrawDebug( ptr )
-	end
-	if not nobounds then
-		local shapes_data = self.armature:GetShapeTransforms()
-		for i = 1, #shapes_data do
-			local data = shapes_data[i]
-			local shape = self.armature.shapes[data.id]
-			visual.drawbox( ptr:ToGlobal( data.global_transform ), Vec( 0, 0, 0 ),
-			                VecScale( Vec( GetShapeSize( shape ) ), data.scale / 10 ),
-			                { r = 1, g = 1, b = 1, a = .2, writeZ = false } )
-		end
-	end
-end
-
---- Registers the tool.
----
----@param self Tool2
-function tool_meta:Register()
-	local enabledKey = "game.tool." .. self.id .. ".enabled"
-	if not self.noregister and not GetBool( enabledKey ) then -- TODO: find a better way to determine if a tool is already registered
-		RegisterTool( self.id, self.printname or self.id, self.model or "", self.group or 6 )
-		if not HasKey( enabledKey ) then
-			SetBool( enabledKey, true )
-		end
-	end
-end
-
---- Emit an event to the tool
----
----@param self Tool2
----@param event string
----@param ... any
-function tool_meta:Emit( event, ... )
-	if event then
-		local handler = rawget( self, event )
-		if handler then
-			return softassert( pcall( handler, self, ... ) )
-		end
-	end
-	return true
-end
-
--- #endregion Metatable
-
--- #region Hooks
-
-local function previous_tool( force )
-	return previous and (force or GetBool( "game.player.canusetool" )) and UMF_tools[previous]
-end
-
-local function active_tool( force )
-	return (force or GetBool( "game.player.canusetool" )) and UMF_tools[GetString( "game.player.tool" )]
-end
-
-hook.add( "base.init", "api.tool_loader", function()
-	for _, tool in pairs( UMF_tools ) do
-		tool:Register()
-		if tool.xml and not tool.armature then
-			tool.armature = load_xml( tool.xml )
-		end
-	end
-	post_init = true
-end )
-
-hook.add( "base.command.quickload", "api.tool_loader", function()
-	for _, tool in pairs( UMF_tools ) do
-		if tool.xml then
-			tool.armature = load_xml( tool.xml )
-		end
-	end
-end )
-
-hook.add( "api.mouse.wheel", "api.tool_loader", function( ds )
-	local tool = previous_tool()
-	if tool then
-		tool:Emit( "MouseWheel", ds )
-	end
-end )
-
-hook.add( "base.update", "api.tool_loader", function( dt )
-	current_hook = "update"
-	current_hook_updated = false
-	local tool = active_tool()
-	if tool then
-		if tool.armature then
-			tool.armature:UpdatePhysics( tool:GetTransformDelta(), GetTimeStep(),
-			                             TransformToLocalVec( tool:GetTransform(), Vec( 0, -10, 0 ) ) )
-		end
-		tool:Emit( "Update", dt )
-	end
-end )
-
-hook.add( "base.tick", "api.tool_loader", function( dt )
-	current_hook = "tick"
-	current_hook_updated = false
-	local cur = GetString( "game.player.tool" )
-
-	local prevtool = previous_tool( true )
-	if prevtool then
-		local _, dolock = prevtool:Emit( "ShouldLockMouseWheel" )
-		if dolock ~= nil then
-			SetBool( "game.input.locktool", dolock )
-			if previous ~= cur and dolock then
-				SetString( "game.player.tool", previous )
-				cur = previous
-			end
-		end
-		if previous ~= cur then
-			prevtool:Emit( "Holster" )
-			detach_armature( prevtool.armature )
-			prevtool._BODY = nil
-			prevtool._SHAPES = nil
-		end
-	end
-
-	local tool = UMF_tools[cur]
-	if tool then
-		local body = GetToolBody()
-		if (GetPlayerVehicle() ~= 0 or GetBool( "game.map.enabled" )) and tool._BODY then
-			tool:Emit( "Holster" )
-			detach_armature( tool.armature )
-			tool._BODY = nil
-			tool._SHAPES = nil
-			return
-		end
-		if body == 0 then
-			return
-		end
-		if previous == cur and (not tool._BODY or tool._BODY.handle ~= body) then
-			tool._BODY = Body( body )
-			attach_armature( tool.armature, body )
-			tool:Emit( "SetupModel", body, GetBodyShapes( body ) )
-			tool._SHAPES = tool._BODY:GetShapes()
-			tool:Emit( "Deploy" )
-			if tool.armature then
-				tool.armature:ResetJiggle()
-			end
-		end
-		if IsValid( tool._BODY ) then
-			if previous == cur then
-				tool:Emit( "Animate", tool._BODY, tool._SHAPES )
-			end
-			if tool.armature then
-				apply_armature( tool.armature )
-			end
-		end
-		if HasKey( "game.tool." .. tool.id .. ".ammo.display" ) then
-			-- Fix sandbox ammo string
-			SetInt( "game.tool." .. tool.id .. ".ammo", 0 )
-		end
-		tool:Emit( "Tick", dt )
-	end
-	previous = cur
-end )
-
-hook.add( "api.firsttick", "api.tool_loader", function()
-	for _, tool in pairs( UMF_tools ) do
-		tool:Emit( "Initialize" )
-	end
-end )
-
-hook.add( "base.draw", "api.tool_loader", function( dt )
-	current_hook = "draw"
-	current_hook_updated = false
-	local tool = active_tool()
-	if tool then
-		tool:Emit( "Draw", dt )
-	end
-end )
-
-hook.add( "api.mouse.pressed", "api.tool_loader", function( button )
-	local tool = active_tool()
-	if tool then
-		---@diagnostic disable-next-line: param-type-mismatch
-		tool:Emit( button == "lmb" and "LeftClick" or button == "rmb" and "RightClick" )
-		tool:Emit( "MousePressed", button )
-	end
-end )
-
-hook.add( "api.mouse.released", "api.tool_loader", function( button )
-	local tool = active_tool()
-	if tool then
-		---@diagnostic disable-next-line: param-type-mismatch
-		tool:Emit( button == "lmb" and "LeftClickReleased" or button == "rmb" and "RightClickReleased" )
-		tool:Emit( "MouseReleased", button )
-	end
-end )
-
--- #endregion Hooks
-
-function RegisterToolUMF( id, tool, immediateRegister )
-	tool.id = id
-	UMF_tools[id] = tool
-
-	if type( tool.model ) == "string" then
-		if tool.model:match( "^[\r\n\t ]*<" ) then
-			tool.xml = tool.model
-			tool.model = "vox/tool/wire.vox"
-		end
-	elseif type( tool.model ) == "table" and tool.model.prefab then
-		tool.xml = tool.model.prefab
-		tool.model = "vox/tool/wire.vox"
-	end
-
-	if not tool.group and HasKey( "game.tool." .. id .. ".skin.group" ) then
-		tool.group = GetInt( "game.tool." .. id .. ".skin.group" )
-	end
-
-	instantiate_global_metatable( "tool", tool )
-
-	if post_init or immediateRegister then
-		tool:Register()
-	end
-
-	return tool
-end
-
- end)();
---src/tdui/base.lua
-(function() 
---[[
--- prototype code (desired outcome)
-TDUI.Label = TDUI.Panel {
-
-	text = ""
-	font = RegisterFont("font/consolas.ttf"),
-	fontSize = 24,
-
-	Draw = function(self, w, h)
-		UiFont(self.font, self.fontSize)
-		UiAlign("left top")
-		UiText(self.text)
-		-- This example doesn't account for:
-		--  * custom alignment
-		--  * wrapping on width
-		--  * Layout calculation
-	end,
-}
-
-local window = TDUI.Frame {
-	title = "Test Window",
-
-	width = "80%h",
-	height = "80%h",
-	resizeable = true,
-
-	padding = 10,
-
-	TDUI.Label {
-		text = "Something"
-	}
-}
-]]
-
-local function createchild( self, def )
-	setmetatable( def, { __index = self, __call = createchild, __PANEL = true } )
-	if self and self.__PerformInherit then
-		self:__PerformInherit( def )
-	end
-	if def.__PerformRegister then
-		def:__PerformRegister()
-	end
-	return def
-end
-
-TDUI = createchild( nil, {} )
-
-local function parseFour( data )
-	local dtype = type( data )
-	if dtype == "number" then
-		return { data, data, data, data }
-	elseif dtype == "string" then
-		local tmp = {}
-		for match in data:gmatch( "[^ ]+" ) do
-			tmp[#tmp + 1] = tonumber( match )
-		end
-		data = tmp
-		dtype = "table"
-	end
-	if dtype == "table" then
-		if #data == 0 then
-			return { 0, 0, 0, 0 }
-		end
-		if #data == 1 then
-			return { data[1], data[1], data[1], data[1] }
-		end
-		if #data < 4 then
-			return { data[1], data[2], data[1], data[2] }
-		end
-		return data
-	end
-	return { 0, 0, 0, 0 }
-end
-
-local function parsePos( data, w, h, def )
-	if type( data ) == "number" then
-		return data
-	end
-	if type( data ) == "function" then
-		return data( w, h, def )
-	end
-	if type( data ) ~= "string" then
-		return 0
-	end
-	if data:find( "function" ) then
-		return 0
-	end
-
-	local code = "local _,_w,_h = ...\nreturn" .. data:gsub( "(-?)([%d.]+)(%%?)([wh]?)", function( sub, n, prc, mod )
-		if prc == "" and mod == "" then
-			return sub .. n
-		end
-		return sub .. "(" .. n .. "*_" .. mod .. ")"
-	end )
-	local fn, err = loadstring( code )
-	assert( fn, err )
-	setfenv( fn, {} )
-
-	return fn( def / 100, w / 100, h / 100 )
-end
-
-local function parseAlign( data )
-	local alignx, aligny = 1, 1
-	for str in data:gmatch( "%w+" ) do
-		if str == "left" then
-			alignx = 1
-		end
-		if str == "center" then
-			alignx = 0
-		end
-		if str == "right" then
-			alignx = -1
-		end
-		if str == "top" then
-			aligny = 1
-		end
-		if str == "middle" then
-			aligny = 0
-		end
-		if str == "bottom" then
-			aligny = -1
-		end
-	end
-	return alignx, aligny
-end
-
-TDUI.Slot = function( name )
-	return { __SLOT = name }
-end
-
--- Base Panel,
-TDUI.Panel = TDUI {
-	__alignx = 1,
-	__aligny = 1,
-	__realx = 0,
-	__realy = 0,
-	__realw = 0,
-	__realh = 0,
-	margin = { 0, 0, 0, 0 },
-	padding = { 0, 0, 0, 0 },
-	boxsizing = "parent",
-	align = "left top",
-	clip = false,
-	visible = true,
-
-	layout = TDUI.Layout,
-
-	oninit = function( self )
-	end,
-
-	predraw = function( self, w, h )
-	end,
-	ondraw = function( self, w, h )
-		-- UiColor(1, 1, 1)
-		-- UiTranslate(-40, -40)
-		-- UiImageBox("common/box-solid-shadow-50.png", w+80, h+81, 50, 50)
-		-- UiTranslate(40, 40)
-		-- UiColor(1, 0, 0, 0.2)
-		-- UiRect(w, h)
-	end,
-	postdraw = function( self, w, h )
-	end,
-
-	__Draw = function( self )
-		if not self.visible then
-			return
-		end
-		if not rawget( self, "__validated" ) then
-			self:InvalidateLayout( true )
-		end
-		local w, h = self:GetComputedSize()
-		self:predraw( w, h )
-		self:ondraw( w, h )
-
-		if self.clip then
-			UiPush()
-			UiWindow( w, h, true )
-		end
-
-		local x, y = 0, 0
-		for i = 1, #self do
-			local child = self[i]
-			local dfx, dfy = child:GetComputedPos()
-			UiTranslate( dfx - x, dfy - y )
-			child:__Draw()
-			x, y = dfx, dfy
-		end
-		UiTranslate( -x, -y )
-
-		if self.clip then
-			UiPop()
-		end
-
-		self:postdraw( w, h )
-	end,
-
-	__PerformRegister = function( self )
-		self.margin = parseFour( self.margin )
-		self.padding = parseFour( self.padding )
-		self.__alignx, self.__aligny = parseAlign( self.align )
-		local i = 1
-		self.__dynamic = {}
-		local hasslots, slots = false, rawget( self, "__SLOTS" ) or {}
-		while i <= #self do
-			if type( self[i] ) == "function" or (type( self[i] ) == "table" and type( self[i].__SLOT ) == "string") then
-				local id = #self.__dynamic + 1
-				local result
-				if self[i] == TDUI.Slot or (type( self[i] ) == "table" and type( self[i].__SLOT ) == "string") then
-					local name = self[i] == TDUI.Slot and "default" or self[i].__SLOT
-					result = {}
-					local content
-					slots[name] = function( c )
-						content = c
-						self:__RefreshDynamic( id )
-					end
-					self.__dynamic[id] = {
-						func = function()
-							return content
-						end,
-						min = i,
-						count = 0,
-					}
-					hasslots = true
-				else
-					result = self[i]( self, id )
-					self.__dynamic[id] = { func = self[i], min = i, count = #result }
-				end
-				if #result == 0 then
-					table.remove( self, i )
-				elseif #result == 1 then
-					self[i] = result[1]
-				else
-					for j = #self, i + 1, -1 do
-						self[j + #result - 1] = self[j]
-					end
-					for j = 1, #result do
-						self[i + j - 1] = result[j]
-					end
-				end
-				i = i - 1
-			else
-				local cslots = rawget( self[i], "__SLOTS" )
-				if cslots then -- TODO: WHY DOES THIS SECTION WORK???
-					hasslots = true -- need to use __dynamic to make sure the right child is being referenced
-					for name, update in pairs( cslots ) do
-						slots[name] = update
-					end
-					self[i].__SLOTS = nil
-				end
-				rawset( self[i], "__parent", self )
-			end
-			i = i + 1
-		end
-		if hasslots then
-			self.__SLOTS = slots
-		end
-		self:oninit()
-	end,
-
-	__PerformInherit = function( self, child )
-		local SLOTS = rawget( self, "__SLOTS" )
-		if SLOTS then
-			for name, update in pairs( SLOTS ) do
-				local src = name == "default" and child or child[name]
-				update( src )
-			end
-		end
-		if SLOTS and SLOTS.default then
-			for i = 1, #child do
-				child[i] = nil
-			end
-		end
-		if #self > 0 then
-			for i = #child, 1, -1 do
-				child[i + #self] = child[i]
-			end
-			for i = 1, #self do
-				local meta = getmetatable( self[i] )
-				if meta and meta.__PANEL then
-					child[i] = self[i] {}
-				else
-					child[i] = self[i]
-				end
-			end
-		end
-	end,
-
-	__RefreshDynamic = function( self, id )
-		local dyn = self.__dynamic[id]
-		if not dyn then
-			return
-		end
-		local result = dyn.func( self, id )
-		local d = #result - dyn.count
-		if d > 0 then
-			for i = #self, dyn.min + dyn.count, -1 do
-				self[i + d] = self[i]
-			end
-		elseif d < 0 then
-			for i = dyn.min + dyn.count, #self - d do
-				self[i + d] = self[i]
-			end
-		end
-		for i = 1, #result do
-			self[dyn.min + i - 1] = result[i]
-		end
-		dyn.count = #result
-		for i = id + 1, #self.__dynamic do
-			self.__dynamic[i].min = self.__dynamic[i].min + d
-		end
-		self:InvalidateLayout()
-	end,
-
-	onlayout = function( self, data, pw, ph, ew, eh )
-		-- onlayout must do 2 things:
-		--  1. Position its children within the available space
-		--  2. Compute its own size for the layout of its parent
-
-		-- TODO: Optimize for static sizes and unchanged bounds
-
-		local selflayout = self.layout
-		if selflayout then
-			local f = selflayout.onlayout
-			if f and f ~= self.onlayout then
-				return f( self, selflayout, pw, ph, ew, eh )
-			end
-		end
-		warning( "Unable to compute layout" )
-		self.__validated = true
-		self:ComputeSize( pw, ph )
-		for i = 1, #self do
-			local child = self[i]
-			child:onlayout( child, self.__realw, self.__realh, self.__realw, self.__realh )
-			child:ComputePosition( 0, 0, self.__realw, self.__realh )
-		end
-		return self.__realw, self.__realh
-
-		--[[self.__realx = self.x and parsePos(self.x, pw, ph, pw) or 0
-		self.__realy = self.y and parsePos(self.y, pw, ph, ph) or 0
-		self.__realw = self.width and parsePos(self.width, pw, ph, pw) or 256
-		self.__realh = self.height and parsePos(self.height, pw, ph, ph) or 256
-		self.__validated = true
-		for i = 1, #self do
-			local child = self[i]
-			child:__PerformLayout(self.__realw, self.__realh)
-		end]]
-	end,
-
-	ComputePosition = function( self, dx, dy, pw, ph )
-		if self.boxsizing == "parent" then
-			local parent = self:GetParent()
-			if parent then
-				pw = pw - self.margin[4] - self.margin[2]
-				ph = ph - self.margin[1] - self.margin[3]
-			end
-		end
-
-		local x = self.x and parsePos( self.x, pw, ph, pw ) or 0
-		if self.__alignx == 1 then
-			self.__realx = x + self.margin[4] + dx
-		elseif self.__alignx == 0 then
-			self.__realx = x + (pw - self.__realw) / 2 + dx
-		elseif self.__alignx == -1 then
-			self.__realx = x + pw - self.margin[2] - self.__realw + dx
-		end
-
-		local y = self.y and parsePos( self.y, pw, ph, ph ) or 0
-		if self.__aligny == 1 then
-			self.__realy = y + self.margin[1] + dy
-		elseif self.__aligny == 0 then
-			self.__realy = y + (ph - self.__realh) / 2 + dy
-		elseif self.__aligny == -1 then
-			self.__realy = y + ph - self.margin[3] - self.__realh + dy
-		end
-
-		return self.__realx, self.__realy
-	end,
-
-	ComputeSize = function( self, pw, ph )
-		if self.boxsizing == "parent" then
-			local parent = self:GetParent()
-			if parent then
-				pw = pw - self.margin[4] - self.margin[2]
-				ph = ph - self.margin[1] - self.margin[3]
-			end
-		end
-		self.__realw = (self.width and parsePos( self.width, pw, ph, pw ) or 0)
-		self.__realh = (self.height and parsePos( self.height, pw, ph, ph ) or 0)
-		if self.ratio then
-			if self.width and not self.height then
-				self.__realh = self.__realw * self.ratio
-			elseif self.height and not self.width then
-				self.__realw = self.__realh / self.ratio
-			end
-		end
-		return self.__realw - self.padding[4] - self.padding[2], self.__realh - self.padding[1] - self.padding[3]
-	end,
-
-	InvalidateLayout = function( self, immediate )
-		if immediate then
-			local cw, ch = self:GetComputedSize()
-			local pw, ph = self:GetParentSize()
-			self:onlayout( self, pw, ph, self.__prevew or pw, self.__preveh or ph )
-			local nw, nh = self:GetComputedSize()
-			if nw ~= cw or nh ~= ch then
-				self:InvalidateParentLayout( true )
-			end
-		else
-			self.__validated = false
-		end
-	end,
-
-	InvalidateParentLayout = function( self, immediate )
-		local parent = self:GetParent()
-		if parent then
-			return parent:InvalidateLayout( immediate )
-		else
-			local pw, ph = UiWidth(), UiHeight()
-			self:InvalidateLayout( immediate )
-			self.__realx = self.x and parsePos( self.x, pw, ph, pw ) or 0
-			self.__realy = self.y and parsePos( self.y, pw, ph, ph ) or 0
-		end
-	end,
-
-	SetParent = function( self, parent )
-		local prev = self:GetParent()
-		if prev then
-			for i = 1, #prev do
-				if prev[i] == self then
-					table.remove( prev, i )
-					prev:InvalidateLayout()
-					break
-				end
-			end
-		end
-		if parent then
-			parent[#parent + 1] = self
-			rawset( self, "__parent", parent )
-			parent:InvalidateLayout()
-		end
-	end,
-
-	GetParent = function( self )
-		return rawget( self, "__parent" )
-	end,
-
-	GetComputedPos = function( self )
-		return self.__realx, self.__realy
-	end,
-
-	GetComputedSize = function( self )
-		return self.__realw, self.__realh
-	end,
-
-	SetSize = function( self, w, h )
-		self.width, self.height = w, h
-		self:InvalidateLayout()
-	end,
-	SetWidth = function( self, w )
-		self.width = w
-		self:InvalidateLayout()
-	end,
-	SetHeight = function( self, h )
-		self.height = h
-		self:InvalidateLayout()
-	end,
-
-	SetPos = function( self, x, y )
-		self.x, self.y = x, y
-		self:InvalidateLayout()
-	end,
-	SetX = function( self, x )
-		self.x = x
-		self:InvalidateLayout()
-	end,
-	SetY = function( self, y )
-		self.y = y
-		self:InvalidateLayout()
-	end,
-
-	SetMargin = function( self, top, right, bottom, left )
-		if right then
-			top = { top, right, bottom, left }
-		end
-		self.margin = parseFour( top )
-		self:InvalidateLayout()
-	end,
-
-	SetPadding = function( self, top, right, bottom, left )
-		if right then
-			top = { top, right, bottom, left }
-		end
-		self.padding = parseFour( top )
-		self:InvalidateLayout()
-	end,
-
-	GetParentSize = function( self )
-		local parent = self:GetParent()
-		if parent then
-			return parent:GetComputedSize()
-		else
-			return UiWidth(), UiHeight()
-		end
-	end,
-
-	Hide = function( self )
-		self.visible = false
-	end,
-	Show = function( self )
-		self.visible = true
-	end,
-}
-
-TDUI.Layout = TDUI.Panel {
-	onlayout = function( self, data, pw, ph, ew, eh )
-		self.__validated = true
-		self.__prevew, self.__preveh = ew, eh
-		local nw, nh = self:ComputeSize( pw, ph )
-		local p1, p2, p3, p4 = self.padding[1], self.padding[2], self.padding[3], self.padding[4]
-		for i = 1, #self do
-			local child = self[i]
-			child:onlayout( child, nw, nh, ew, eh )
-			child:ComputePosition( p4, p1, nw, nh )
-		end
-		return self.__realw + self.margin[4] + self.margin[2], self.__realh + self.margin[1] + self.margin[3]
-	end,
-}
-
-TDUI.SimpleForEach = function( tab, callback )
-	return function()
-		local rt = {}
-		for i = 1, #tab do
-			local e = callback( tab[i], i, tab )
-			if e then
-				rt[#rt + 1] = e
-			end
-		end
-		return rt
-	end
-end
-
-TDUI.Panel.layout = TDUI.Layout
-
-local ScreenPanel = TDUI.Panel { x = 0, y = 0, width = 0, height = 0 }
-
-function TDUI.Panel:Popup( parent )
-	self:SetParent( parent or ScreenPanel )
-end
-
-function TDUI.Panel:Close()
-	self:SetParent()
-end
-
-hook.add( "base.draw", "api.tdui.ScreenPanel", function()
-	if ScreenPanel.width == 0 then
-		ScreenPanel:SetSize( UiWidth(), UiHeight() )
-	end
-	UiPush()
-	softassert( pcall( ScreenPanel.__Draw, ScreenPanel ) )
-	UiPop()
-end )
-
- end)();
---src/tdui/image.lua
-(function() 
-TDUI.Image = TDUI.Panel {
-	path = "",
-	fit = "fit",
-
-	ondraw = function( self, w, h )
-		if not HasFile( self.path ) then
-			return
-		end
-		local iw, ih = self:GetImageSize()
-		UiPush()
-		if self.fit == "stretch" then
-			UiScale( w / iw, h / ih )
-		elseif self.fit == "cover" then
-			local r, ir = w / h, iw / ih
-			UiWindow( w, h, true )
-			if r > ir then
-				UiTranslate( 0, h / 2 - ih * w / iw / 2 )
-				UiScale( w / iw )
-			else
-				UiTranslate( w / 2 - iw * h / ih / 2, 0 )
-				UiScale( h / ih )
-			end
-		elseif self.fit == "fit" then
-			local r, ir = w / h, iw / ih
-			if r > ir then
-				UiTranslate( w / 2 - iw * h / ih / 2, 0 )
-				UiScale( h / ih )
-			else
-				UiTranslate( 0, h / 2 - ih * w / iw / 2 )
-				UiScale( w / iw )
-			end
-		end
-		self:DrawImage( iw, ih )
-		UiPop()
-	end,
-
-	GetImageSize = function( self )
-		return UiGetImageSize( self.path )
-	end,
-	DrawImage = function( self, w, h )
-		UiImage( self.path )
-	end,
-}
-
-TDUI.AtlasImage = TDUI.Image {
-	atlas_width = 1,
-	atlas_height = 1,
-	atlas_x = 1,
-	atlas_y = 1,
-
-	GetImageSize = function( self )
-		local iw, ih = UiGetImageSize( self.path )
-		return iw / self.atlas_width, ih / self.atlas_height
-	end,
-	DrawImage = function( self, w, h )
-		UiWindow( w, h, true )
-		UiTranslate( (1 - self.atlas_x) * w, (1 - self.atlas_y) * h )
-		UiImage( self.path )
-	end,
-}
-
- end)();
---src/tdui/layout.lua
-(function() 
-TDUI.StackLayout = TDUI.Layout {
-	orientation = "vertical",
-
-	onlayout = function( self, data, pw, ph, ew, eh )
-		self.__validated = true
-		self.__prevew, self.__preveh = ew, eh
-		local isvertical = data.orientation == "vertical"
-		local nw, nh = self:ComputeSize( pw, ph )
-		local pdw, pdh = self.padding[4] + self.padding[2], self.padding[1] + self.padding[3]
-		local nfw, nfh = nw == -pdw, nh == -pdh
-		if not nfw then
-			ew = nw
-		else
-			ew = ew - pdw
-		end
-		if not nfh then
-			eh = nh
-		else
-			eh = eh - pdh
-		end
-		if isvertical then
-			if nfh then
-				nh = 0
-			end
-		else
-			if nfw then
-				nw = 0
-			end
-		end
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			if isvertical then
-				if nfw and cw > nw and cw <= ew then
-					nw = cw
-				end
-				if nfh then
-					nh = nh + ch
-				end
-			else
-				if nfw then
-					nw = nw + cw
-				end
-				if nfh and ch > nh and ch <= eh then
-					nh = ch
-				end
-			end
-		end
-		local dx, dy = self.padding[4], self.padding[1]
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			child:ComputePosition( dx, dy, nw, nh )
-			if isvertical then
-				dy = dy + ch
-			else
-				dx = dx + cw
-			end
-		end
-		if nfw then
-			self.__realw = nw + pdw
-		end
-		if nfh then
-			self.__realh = nh + pdh
-		end
-		return self.__realw + self.margin[4] + self.margin[2], self.__realh + self.margin[1] + self.margin[3]
-	end,
-}
-
-TDUI.WrapLayout = TDUI.Layout {
-	orientation = "vertical",
-
-	onlayout = function( self, data, pw, ph, ew, eh )
-		self.__validated = true
-		self.__prevew, self.__preveh = ew, eh
-		local isvertical = data.orientation == "vertical"
-		local nw, nh = self:ComputeSize( pw, ph )
-		local pdw, pdh = self.padding[4] + self.padding[2], self.padding[1] + self.padding[3]
-		local nfw, nfh = nw == -pdw, nh == -pdh
-		if not nfw then
-			ew = nw
-		else
-			ew = ew - pdw
-		end
-		if not nfh then
-			eh = nh
-		else
-			eh = eh - pdh
-		end
-		if isvertical then
-			if nfh then
-				nh = 0
-			end
-		else
-			if nfw then
-				nw = 0
-			end
-		end
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			if isvertical then
-				if nfw and cw > nw and cw <= ew then
-					nw = cw
-				end
-				if nfh then
-					nh = nh + ch
-				end
-			else
-				if nfw then
-					nw = nw + cw
-				end
-				if nfh and ch > nh and ch <= eh then
-					nh = ch
-				end
-			end
-		end
-		local dx, dy = self.padding[4], self.padding[1]
-		local curr = 0
-		for i = 1, #self do
-			local child = self[i]
-			local cw, ch = child:onlayout( child, nw, nh, ew, eh )
-			if isvertical then
-				if nw + pdw < dx + cw then
-					dx = self.padding[4]
-					dy = dy + curr
-					curr = 0
-				end
-				child:ComputePosition( dx, dy, nw, nh )
-				curr = math.max( curr, ch )
-				dx = dx + cw
-			else
-				if nh + pdh < dy + ch then
-					dy = self.padding[1]
-					dx = dx + curr
-					curr = 0
-				end
-				child:ComputePosition( dx, dy, nw, nh )
-				curr = math.max( curr, cw )
-				dy = dy + ch
-			end
-		end
-		if nfw then
-			self.__realw = nw + pdw
-		end
-		if nfh then
-			self.__realh = nh + pdh
-		end
-		return self.__realw + self.margin[4] + self.margin[2], self.__realh + self.margin[1] + self.margin[3]
-	end,
-}
-
- end)();
---src/tdui/panel.lua
-(function() 
-TDUI.SlicePanel = TDUI.Panel {
-	color = { 1, 1, 1, 1 },
-
-	predraw = function( self, w, h )
-		UiPush()
-		UiColor( self.color[1] or 1, self.color[2] or 1, self.color[3] or 1, self.color[4] or 1 )
-		local t = self.template
-		UiTranslate( -t.offset_left, -t.offset_top )
-		UiImageBox( t.image, w + t.offset_left + t.offset_right, h + t.offset_top + t.offset_bottom, t.slice_x, t.slice_y )
-		UiPop()
-	end,
-}
-
-TDUI.SlicePanel.SolidShadow50 = {
-	image = "ui/common/box-solid-shadow-50.png",
-	slice_x = 50,
-	slice_y = 50,
-	offset_left = 40,
-	offset_top = 40,
-	offset_bottom = 41,
-	offset_right = 40,
-}
-
-TDUI.SlicePanel.template = TDUI.SlicePanel.SolidShadow50
-
- end)();
---src/tdui/window.lua
-(function() 
-TDUI.Window = TDUI.Panel {
-	color = { 1, 1, 1, 1 },
-
-	predraw = function( self, w, h )
-	end,
-
-	TDUI.Panel { TDUI.Slot "title" },
-
-	TDUI.Panel { TDUI.Slot },
-}
-
- end)();
---src/_index.lua
-(function() -- 
- end)();
-for i = 1, #__RUNLATER do local f = loadstring(__RUNLATER[i]) if f then pcall(f) end end

```

---

# Migration Report: scripts\utility.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\utility.lua
+++ patched/scripts\utility.lua
@@ -1,76 +1,85 @@
-
-table.unpack = table.unpack or unpack
---[[VECTORS]]
-    -- Distance between two vectors.
-    function VecDist(vec1, vec2) return VecLength(VecSub(vec1, vec2)) end
-    -- Divide a vector by another vector.
-    function VecDiv(v, n) n = n or 1 return Vec(v[1] / n, v[2] / n, v[3] / n) end
-    -- Add all vectors in a table together.
-    function VecAddAll(vectorsTable) local v = Vec(0,0,0) for i = 1, #vectorsTable do VecAdd(v, vectorsTable[i]) end return v end
-    --- Returns a vector with random values.
-    function rdmVec(min, max) return Vec(rdm(min, max),rdm(min, max),rdm(min, max)) end
-    ---Print QuatEulers or vectors.
-    function VecPrint(vec, decimals, label)
+#version 2
+local debugSounds = {
+        beep = LoadSound("warning-beep"),
+        buzz = LoadSound("light/spark0"),
+        chime = LoadSound("elevator-chime"),
+        valu = LoadSound("valuable.ogg"),}
+
+function VecDist(vec1, vec2) return VecLength(VecSub(vec1, vec2)) end
+
+function VecDiv(v, n) n = n or 1 return Vec(v[1] / n, v[2] / n, v[3] / n) end
+
+function VecAddAll(vectorsTable) local v = Vec(0,0,0) for i = 1, #vectorsTable do VecAdd(v, vectorsTable[i]) end return v end
+
+function rdmVec(min, max) return Vec(rdm(min, max),rdm(min, max),rdm(min, max)) end
+
+function VecPrint(vec, decimals, label)
         DebugPrint(VecToStr(vec, decimals, label))
     end
-    function VecToStr(vec, decimals, label)
+
+function VecToStr(vec, decimals, label)
         return (label or "") .. 
             "  " .. sfn(vec[1], decimals or 2) ..
             "  " .. sfn(vec[2], decimals or 2) ..
             "  " .. sfn(vec[3], decimals or 2)
     end
-    function VecToTag(vec, decimals)
+
+function VecToTag(vec, decimals)
         return  sfn(vec[1], decimals or 2) ..
         "_" .. sfn(vec[2], decimals or 2) ..
         "_" .. sfn(vec[3], decimals or 2)
     end
-    function VecFromTag(tag)
+
+function VecFromTag(tag)
         local splitted = sSplit(tag, "_")
         return Vec(tonumber(splitted[1]), tonumber(splitted[2]), tonumber(splitted[3]))
     end
-    function QuatToTag(quat, decimals)
+
+function QuatToTag(quat, decimals)
         return  sfn(quat[1], decimals or 2) ..
         "_" .. sfn(quat[2], decimals or 2) ..
         "_" .. sfn(quat[3], decimals or 2) ..
         "_" .. sfn(quat[4], decimals or 2)
     end
-    function QuatFromTag(tag)
+
+function QuatFromTag(tag)
         local splitted = sSplit(tag, "_")
         return Quat(tonumber(splitted[1]), tonumber(splitted[2]), tonumber(splitted[3]), tonumber(splitted[4]))
     end
-    function TransformToTag(tr, decimals)
+
+function TransformToTag(tr, decimals)
         return  VecToTag(tr.pos, decimals) ..
         "/" .. QuatToTag(tr.rot, decimals)
     end
-    function TransformFromTag(tag)
+
+function TransformFromTag(tag)
         local splitted = sSplit(tag, "/")
         return Transform(VecFromTag(splitted[1]), QuatFromTag(splitted[2]))
     end
-    -- Tells if two vectors face in the same direction
-    function VecSameDir(vec1, vec2)
+
+function VecSameDir(vec1, vec2)
         return VecDot(vec1, vec2) >= 0
     end
-    -- Align a vector to face in the same direction as a reference vector
-    -- (negate its direction if needed)
-    function VecAlign(vec, vecRef)
+
+function VecAlign(vec, vecRef)
         return VecSameDir(vec, vecRef) and vec or VecScale(vec, -1)
     end
-    -- Redirect a vector to face in the same direction as a reference vector
-    function VecRedirect(vec, vecRef)
+
+function VecRedirect(vec, vecRef)
         return VecResize(vecRef, VecLength(vec))
     end
-    -- Set the length of a vector without changing its orientation
-    function VecResize(vec, size) return VecScale(VecNormalize(vec), size) end
-    -- Project a vec1 on vec2 and return the length of vec1 projected
-    function VecProjToVecLen(vec1, vec2) return VecDot(vec1, vec2) / VecLength(vec2) end
-    -- Reflect a vector on a surface
-    function VecReflect(vec, normal) return VecSub(vec, VecScale(normal, 2 * VecDot(vec, normal))) end
-    -- Removed the vertical component of a vector
-    function VecFlatten(vec) return Vec(vec[1], 0, vec[3]) end
-    -- Gets the minimal angle in degree between two vectors
-    function VecAngleBetween(vec1, vec2) return math.deg(math.acos(VecDot(vec1, vec2)/(VecLength(vec1)*VecLength(vec2)))) end
-    -- Gets a 2D vector ignoring given axis
-    function Vec3DTo2D(vec, axis)
+
+function VecResize(vec, size) return VecScale(VecNormalize(vec), size) end
+
+function VecProjToVecLen(vec1, vec2) return VecDot(vec1, vec2) / VecLength(vec2) end
+
+function VecReflect(vec, normal) return VecSub(vec, VecScale(normal, 2 * VecDot(vec, normal))) end
+
+function VecFlatten(vec) return Vec(vec[1], 0, vec[3]) end
+
+function VecAngleBetween(vec1, vec2) return math.deg(math.acos(VecDot(vec1, vec2)/(VecLength(vec1)*VecLength(vec2)))) end
+
+function Vec3DTo2D(vec, axis)
         if axis == "x" then
             return {vec[2], vec[3]}
         elseif axis == "y" then
@@ -80,14 +89,14 @@
         end
         return nil
     end
-    -- Gets the minimal angle in degree between two 2D vectors
-    function Vec2DOrientedAngleBetween(vec1, vec2)
+
+function Vec2DOrientedAngleBetween(vec1, vec2)
         local dot = vec1[1]*vec2[1] + vec1[2]*vec2[2]
         local det = vec1[1]*vec2[2] - vec1[2]*vec2[1]
         return math.deg(math.atan2(det, dot))
     end
-    -- Rotate a vector on a given world axis
-    function VecRotate(vec, axis, angle)
+
+function VecRotate(vec, axis, angle)
         local radAngle = math.rad(angle)
         if axis == "x" then
             local newY = (math.cos(radAngle)*vec[2])-(math.sin(radAngle)*vec[3])
@@ -104,21 +113,21 @@
         end
         return vec
     end
-    -- Rotate a vector to be vertically aligned with another vector
-    function VecAlignOnAxis(vec, vecRef, axis)
+
+function VecAlignOnAxis(vec, vecRef, axis)
         local vec1 = Vec3DTo2D(vec, axis)
         local vec2 = Vec3DTo2D(vecRef, axis)
         local angle = Vec2DOrientedAngleBetween(vec1, vec2)
         return VecRotate(vec, axis, angle)
     end
-    -- Return a vector pointing in the direction of the given quaternion (opposite operation of QuatLookAt())
-    function VecForward(quat) return QuatRotateVec(quat, Vec(0, 0, -1)) end
-    -- Return a vector pointing up based on the direction of the given quaternion
-    function VecUp(quat) return QuatRotateVec(quat, Vec(0, 1, 0)) end
-    -- Return a vector pointing right based on the direction of the given quaternion
-    function VecRight(quat) return QuatRotateVec(quat, Vec(-1, 0, 0)) end
-    -- Returns the oriented pitch and yaw angles to get vec pointing in the exact same direction as vecRef
-    function VecAimAtYawPitch(vec, vecRef)
+
+function VecForward(quat) return QuatRotateVec(quat, Vec(0, 0, -1)) end
+
+function VecUp(quat) return QuatRotateVec(quat, Vec(0, 1, 0)) end
+
+function VecRight(quat) return QuatRotateVec(quat, Vec(-1, 0, 0)) end
+
+function VecAimAtYawPitch(vec, vecRef)
         -- Compute yaw angle
         local normalVec = VecNormalize(vec)
         local normalVecRef = VecNormalize(vecRef)
@@ -134,8 +143,8 @@
         local pitchAngle = Vec2DOrientedAngleBetween(vertVec2D, vertVecRef2D)
         return yawAngle, pitchAngle
     end
-    -- Rotate vec to point in the same direction as vecRef with a max angle in degrees
-    function VecInterpAngleTorward(vec, vecRef, maxAngle)
+
+function VecInterpAngleTorward(vec, vecRef, maxAngle)
         local vecToVecRefAngle = VecAngleBetween(vec, vecRef)
         -- Angle is lower than the max angle? Just point vecotr in the right direction
         if vecToVecRefAngle <= maxAngle then
@@ -155,14 +164,16 @@
             return VecAdd(e1Component, e2Component)
         end
     end
-    function VecClamp(v, min, max)
+
+function VecClamp(v, min, max)
         return {
             clamp(v[1], min, max),
             clamp(v[2], min, max),
             clamp(v[3], min, max)
         }
     end
-    function VecRatio(v, mi, ma, nmi, nma)
+
+function VecRatio(v, mi, ma, nmi, nma)
         return {
             ratio(v[1], mi, ma, nmi, nma),
             ratio(v[2], mi, ma, nmi, nma),
@@ -170,30 +181,36 @@
         }
     end
 
-
-
---[[QUAT]]
-    function QuatLookDown(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, -1, 0))) end
-    function QuatLookUp(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, 1, 0))) end
-    function QuatTrLookDown(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,-1,0))) end
-    function QuatDir(dir) return QuatLookAt(Vec(0, 0, 0), dir) end -- Quat to 3d worldspace dir.
-    function GetQuatEulerVec(quat) local x,y,z = GetQuatEuler(quat) return Vec(x,y,z) end
-    function QuatConjugate(quat)
+function QuatLookDown(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, -1, 0))) end
+
+function QuatLookUp(pos) return QuatLookAt(pos, VecAdd(pos, Vec(0, 1, 0))) end
+
+function QuatTrLookDown(tr) return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0,-1,0))) end
+
+function QuatDir(dir) return QuatLookAt(Vec(0, 0, 0), dir) end
+
+function GetQuatEulerVec(quat) local x,y,z = GetQuatEuler(quat) return Vec(x,y,z) end
+
+function QuatConjugate(quat)
         return Quat(quat[1], -quat[2], -quat[3], -quat[4])
     end
-    function QuatMagnitude(quat)
+
+function QuatMagnitude(quat)
         return math.sqrt(math.pow(quat[1], 2) + math.pow(quat[2], 2) + math.pow(quat[3], 2) + math.pow(quat[4], 2))
     end
-    function QuatNormalize(quat)
+
+function QuatNormalize(quat)
         local mag = QuatMagnitude(quat)
         return Quat(quat[1]/mag, quat[2]/mag, quat[3]/mag, quat[4]/mag)
     end
-    function QuatInverse(quat)
+
+function QuatInverse(quat)
         local conjugate = QuatConjugate(quat)
         local squaredMagnitude = math.pow(QuatMagnitude(quat), 2)
         return Quat(conjugate[1]/squaredMagnitude, conjugate[2]/squaredMagnitude, conjugate[3]/squaredMagnitude, conjugate[4]/squaredMagnitude)
     end
-    function QuatWorldRotateQuat(a, b)
+
+function QuatWorldRotateQuat(a, b)
         -- Store current quat for later
         local initialQuat = QuatCopy(a)
         -- Negate current quat
@@ -203,7 +220,8 @@
         -- Re-apply old quat
         return QuatRotateQuat(tmpQuat, initialQuat)
     end
-    function QuatWorldRotateVec(a, vec)
+
+function QuatWorldRotateVec(a, vec)
         -- Get quat from vec
         local initialQuat = QuatDir(vec)
         -- Negate quat on vec
@@ -213,7 +231,8 @@
         -- Apply quat to vec
         return QuatRotateVec(tmpQuat, tmpVec)
     end
-    function QuatFlip(quat, keepRoll)
+
+function QuatFlip(quat, keepRoll)
         local forward = Vec(0, 0, -1)
         local dir = VecForward(quat)
         local flippedDir = VecScale(dir, -1)
@@ -227,7 +246,8 @@
         end
         return flippedQuat
     end
-    function QuatAlign(quat, localVector, worldVector)
+
+function QuatAlign(quat, localVector, worldVector)
         local parentVector = QuatRotateVec(quat, localVector)
         local axis = VecCross(parentVector, worldVector)
         local angle = math.deg(math.atan2(VecLength(axis), VecDot(parentVector, worldVector)))
@@ -236,19 +256,18 @@
     
         return alignedRot, offsetRot
     end
-    function TransformToParentQuat(parentT, quat)
+
+function TransformToParentQuat(parentT, quat)
         local childT = Transform(Vec(), quat)
         local t = TransformToParentTransform(parentT, childT)
         return t.rot
     end
-    function QuatRotateAroundAxis(rot, axisVec, angle)
+
+function QuatRotateAroundAxis(rot, axisVec, angle)
         return QuatRotateQuat(rot, QuatAxisAngle(axisVec, angle))
     end
 
-
-
---[[AABB]]
-    function AabbDraw(v1, v2, r, g, b, a)
+function AabbDraw(v1, v2, r, g, b, a)
         r = r or 1
         g = g or 1
         b = b or 1
@@ -277,22 +296,26 @@
         DebugLine(Vec(x1,y1,z2), Vec(x1,y1,z1), r, g, b, a)
         DebugLine(Vec(x1,y2,z2), Vec(x1,y2,z1), r, g, b, a)
     end
-    function AabbGetCenterPos(min, max)
+
+function AabbGetCenterPos(min, max)
         return VecLerp(min,max,0.5)
     end
-    function AabbCheckOverlap(aMin, aMax, bMin, bMax)
+
+function AabbCheckOverlap(aMin, aMax, bMin, bMax)
         return 
         (aMin[1] <= bMax[1] and aMax[1] >= bMin[1]) and
         (aMin[2] <= bMax[2] and aMax[2] >= bMin[2]) and
         (aMin[3] <= bMax[3] and aMax[3] >= bMin[3])
     end
-    function AabbCheckPointInside(aMin, aMax, p)
+
+function AabbCheckPointInside(aMin, aMax, p)
         return 
         (p[1] <= aMax[1] and p[1] >= aMin[1]) and
         (p[2] <= aMax[2] and p[2] >= aMin[2]) and
         (p[3] <= aMax[3] and p[3] >= aMin[3])
     end
-    function AabbClosestEdge(pos, shape)
+
+function AabbClosestEdge(pos, shape)
 
         local shapeAabbMin, shapeAabbMax = GetShapeBounds(shape)
         local bCenterY = VecLerp(shapeAabbMin, shapeAabbMax, 0.5)[2]
@@ -317,8 +340,8 @@
         end
         return closestEdge, index
     end
-    --- Sort edges by closest to startPos and closest to endPos. Return sorted table.
-    function AabbSortEdges(startPos, endPos, edges)
+
+function AabbSortEdges(startPos, endPos, edges)
         local s, startIndex = aabbClosestEdge(startPos, edges)
         local e, endIndex = aabbClosestEdge(endPos, edges)
         -- Swap first index with startPos and last index with endPos. Everything between stays same.
@@ -326,47 +349,54 @@
         edges = tableSwapIndex(edges, #edges, endIndex)
         return edges
     end
-    function AabbDimensions(min, max) return Vec(max[1] - min[1], max[2] - min[2], max[3] - min[3]) end
-    function AabbGetShapeCenterPos(shape)
+
+function AabbDimensions(min, max) return Vec(max[1] - min[1], max[2] - min[2], max[3] - min[3]) end
+
+function AabbGetShapeCenterPos(shape)
         local mi, ma = GetShapeBounds(shape)
         return VecLerp(mi,ma,0.5)
     end
-    function AabbGetBodyCenterPos(body)
+
+function AabbGetBodyCenterPos(body)
         local mi, ma = GetBodyBounds(body)
         return VecLerp(mi,ma,0.5)
     end
-    function AabbGetShapeCenterTopPos(shape, addY)
+
+function AabbGetShapeCenterTopPos(shape, addY)
         addY = addY or 0
         local mi, ma = GetShapeBounds(shape)
         local v =  VecLerp(mi,ma,0.5)
         v[2] = ma[2] + addY
         return v
     end
-    function AabbGetBodyCenterTopPos(body, addY)
+
+function AabbGetBodyCenterTopPos(body, addY)
         addY = addY or 0
         local mi, ma = GetBodyBounds(body)
         local v =  VecLerp(mi,ma,0.5)
         v[2] = ma[2] + addY
         return v
     end
-    function AabbGetBodyHeight(body)
+
+function AabbGetBodyHeight(body)
         local mi, ma = GetBodyBounds(body)
         return ma[2] - mi[2]
     end
-    function AabbGetShapeHeight(shape)
+
+function AabbGetShapeHeight(shape)
         local mi, ma = GetShapeBounds(shape)
         return ma[2] - mi[2]
     end
-    -- Get center point of the player
-    function AabbGetPlayerCenter()
-        local playerEyeTr = GetPlayerCameraTransform()
-        local playerFeetTr = GetPlayerTransform()
+
+function AabbGetPlayerCenter()
+        local playerEyeTr = GetPlayerCameraTransform(playerId)
+        local playerFeetTr = GetPlayerTransform(playerId)
         return VecAdd(playerFeetTr.pos, VecScale(VecSub(playerEyeTr.pos, playerFeetTr.pos), 0.5))
     end
-    -- Get bounding box of the player
-    function AabbGetPlayerBounds()
-        local playerEyeTr = GetPlayerCameraTransform()
-        local playerFeetTr = GetPlayerTransform()
+
+function AabbGetPlayerBounds()
+        local playerEyeTr = GetPlayerCameraTransform(playerId)
+        local playerFeetTr = GetPlayerTransform(playerId)
         local playerWidth = 1
         local minX = playerFeetTr.pos[1] - (playerWidth / 2)
         local maxX = playerEyeTr.pos[1] + (playerWidth / 2)
@@ -377,8 +407,6 @@
         return Vec(minX, minY, minZ), Vec(maxX, maxY, maxZ)
     end
 
-
---[[OBB]]
 function GetShapeObb(shape)
     local xsize, ysize, zsize, scale = GetShapeSize(shape)
     local min = Vec(0, 0, 0)
@@ -386,6 +414,7 @@
     local tr = GetShapeWorldTransform(shape)
     return tr, min, max
 end
+
 function GetBodyObb(body)
     local shapes = GetBodyShapes(body)
     local min = nil
@@ -418,6 +447,7 @@
     end
     return tr, min, max
 end
+
 function GetObbCorners(tr, min, max)
     local corners = {}
     local localCorners = {
@@ -435,6 +465,7 @@
     end
     return corners
 end
+
 function ObbDraw(c, r, g, b, a)
     r = r or 1
     g = g or 1
@@ -457,22 +488,20 @@
     DebugLine(c[4], c[8], r, g, b, a)
 end
 
-
---[[TABLES]]
-    function TableSwapIndex(t, i1, i2)
+function TableSwapIndex(t, i1, i2)
         local temp = t[i1]
         t[i1] = t[i2]
         t[i2] = temp
         return t
     end
 
-    function TableClone(tb)
+function TableClone(tb)
         local tbc = {}
         for k,v in pairs(tb) do tbc[k] = v end
         return tbc
     end
 
-    function TableRemove(t, fnKeep)
+function TableRemove(t, fnKeep)
         local j, n = 1, #t
     
         for i=1,n do
@@ -491,15 +520,15 @@
         return t
     end
 
-    function TableAppend(t, elem)
+function TableAppend(t, elem)
         t[#t+1] = elem
     end
 
-    function TableClear(t)
+function TableClear(t)
         for i=1,#t do t[i]=nil end
     end
 
-    function DeepCopy(orig)
+function DeepCopy(orig)
         local orig_type = type(orig)
         local copy
         if orig_type == 'table' then
@@ -514,16 +543,15 @@
         return copy
     end
 
-    function TableConcat(t1,t2)
+function TableConcat(t1,t2)
         local t3 = {table.unpack(t1)}
         for i=1,#t2 do
             t3[#t3+1] = t2[i]
         end
         return t3
     end
-    
-
-    function TableEqual(t1, t2)
+
+function TableEqual(t1, t2)
         -- Check length, or else the loop isn't valid.
         if #t1 ~= #t2 then
             return false
@@ -538,7 +566,7 @@
         return true
     end
 
-    function TableFind(t, elem)
+function TableFind(t, elem)
         -- Check each element.
         for i, v in ipairs(t) do
             if v == elem then
@@ -549,7 +577,7 @@
         return nil
     end
 
-    function TableBinarySearch(t, x)
+function TableBinarySearch(t, x)
         local lo = 1
         local hi = #t
         while lo < hi do
@@ -563,7 +591,7 @@
         return lo
      end
 
-    function TableIndexOf(t, cond)
+function TableIndexOf(t, cond)
         local elem = nil
         local elemIndex = nil
         -- Check each element.
@@ -577,15 +605,15 @@
         return elemIndex
     end
 
-    function TableIndexOfMax(t)
+function TableIndexOfMax(t)
         return TableIndexOf(t, function(elem, max) return elem > max end)
     end
 
-    function TableIndexOfMin(t)
+function TableIndexOfMin(t)
         return TableIndexOf(t, function(elem, min) return elem < min end)
     end
 
-    function TablePushFront(t, elem, maxLength)
+function TablePushFront(t, elem, maxLength)
         maxLength = maxLength or #t
         -- Move each element one step back (remove last one)
         for i=maxLength-1,1,-1 do
@@ -595,8 +623,7 @@
         t[1] = elem
     end
 
-    -- Multiply each value of the same index of two tables
-    function TableMultiply(t1, t2)
+function TableMultiply(t1, t2)
         local res = {}
         for i, v in pairs(t2) do
             table.insert(res, t1[i] * t2[i])
@@ -604,8 +631,7 @@
         return res
     end
 
-    -- Transpose a matrix (2D table)
-    function Matrixranspose(t)
+function Matrixranspose(t)
         local transposed = {}
         for i=1,#t do
             local line = t[i]
@@ -619,8 +645,7 @@
         return transposed
     end
 
-    -- Multiple 2 matrices (2D tables)
-    function MatrixMultiply(t1, t2)
+function MatrixMultiply(t1, t2)
         local multiplied = {}
         for i=1,#t1 do
             if not multiplied[i] then
@@ -637,19 +662,8 @@
         end
         return multiplied
     end
-      
-    
-
-
-
---[[RAYCASTING]]
----comment
----@param tr table
----@param distance number
----@param rad number
----@param rejectBodies table
----@param rejectShapes table
-    function RaycastFromTransform(tr, distance, rad, rejectBodies, rejectShapes)
+
+function RaycastFromTransform(tr, distance, rad, rejectBodies, rejectShapes)
 
         if distance ~= nil then distance = -distance else distance = -300 end
 
@@ -671,7 +685,7 @@
         end
     end
 
-    function QueryRequireTag(tag, value)
+function QueryRequireTag(tag, value)
         if not queryRequiredTags then
             queryRequiredTags = {}
             queryRequiredValues = {}
@@ -680,7 +694,7 @@
         queryRequiredValues[tag] = value
     end
 
-    function QueryRejectTag(tag, value)
+function QueryRejectTag(tag, value)
         if not queryRejectedTags then
             queryRejectedTags = {}
             queryRejectedValues = {}
@@ -689,14 +703,14 @@
         queryRejectedValues[tag] = value
     end
 
-    function QueryClearTags()
+function QueryClearTags()
         queryRequiredTags = {}
         queryRequiredValues = {}
         queryRejectedTags = {}
         queryRejectedValues = {}
     end
 
-    function HasRequiredTag(handle)
+function HasRequiredTag(handle)
         if not queryRequiredTags then
             queryRequiredTags = {}
             queryRequiredValues = {}
@@ -725,7 +739,7 @@
         return true
     end
 
-    function HasRejectedTag(handle)
+function HasRejectedTag(handle)
         if not queryRejectedTags then
             queryRejectedTags = {}
             queryRejectedValues = {}
@@ -754,11 +768,11 @@
         return false
     end
 
-    function MatchesTagFilter(handle)
+function MatchesTagFilter(handle)
         return HasRequiredTag(handle) and not HasRejectedTag(handle)
     end
 
-    function QueryXRaycast(origin, direction, maxDist, radius, rejectTransparent, rejectShapes)
+function QueryXRaycast(origin, direction, maxDist, radius, rejectTransparent, rejectShapes)
         direction = VecNormalize(direction)
         if rejectShapes == nil then
             rejectShapes = {}
@@ -786,7 +800,7 @@
         return {}, {}, {}
     end
 
-    function QueryRaycastClosest(origin, direction, maxDist, radius, rejectTransparent, target, bestDistToTarget, rejectShapes)
+function QueryRaycastClosest(origin, direction, maxDist, radius, rejectTransparent, target, bestDistToTarget, rejectShapes)
         direction = VecNormalize(direction)
         if rejectShapes == nil then
             rejectShapes = {}
@@ -817,25 +831,27 @@
         end
     end
 
-
---[[PHYSICS]]
-    function diminishBodyAngVel(body, rate)
+function diminishBodyAngVel(body, rate)
         local angVel = GetBodyAngularVelocity(body)
         local dRate = rate or 0.99
         local diminishedAngVel = Vec(angVel[1]*dRate, angVel[2]*dRate, angVel[3]*dRate)
         SetBodyAngularVelocity(body, diminishedAngVel)
     end
-    function IsMaterialUnbreakable(mat, shape)
+
+function IsMaterialUnbreakable(mat, shape)
         return mat == 'rock' or mat == 'heavymetal' or mat == 'unbreakable' or mat == 'hardmasonry' or
             HasTag(shape,'unbreakable') or HasTag(GetShapeBody(shape),'unbreakable')
     end
-    function IsBodyValid(body)
+
+function IsBodyValid(body)
         return IsHandleValid(body) and (GetBodyMass(body) > 0)
     end
-    function IsShapeValid(shape)
+
+function IsShapeValid(shape)
         return IsHandleValid(shape) and (GetShapeVoxelCount(shape) > 0)
     end
-    function IsFullBodyValid(body)
+
+function IsFullBodyValid(body)
         if not IsBodyValid(body) then
             return false
         end
@@ -847,7 +863,8 @@
         end
         return true
     end
-    function GetFullBodyMass(body)
+
+function GetFullBodyMass(body)
         local mass = 0
         local jointedBodies = GetJointedBodies(body)
         for i=1,#jointedBodies do
@@ -855,13 +872,15 @@
         end
         return mass
     end
-    function HighlightFullBody(body, r, g, b, a)
+
+function HighlightFullBody(body, r, g, b, a)
         local jointedBodies = GetJointedBodies(body)
         for i=1,#jointedBodies do
             DrawBodyOutline(jointedBodies[i], r, g, b, a)
         end
     end
-    function GetMainBody(body)
+
+function GetMainBody(body)
         local jointedBodies = GetJointedBodies(body)
         local maxMass = GetBodyMass(body)
         local mainBody = body
@@ -875,7 +894,8 @@
         end
         return mainBody
     end
-    function GetMainShape(body)
+
+function GetMainShape(body)
         local shapes = GetBodyShapes(body)
         local maxVoxels = 0
         local mainShape = nil
@@ -890,52 +910,45 @@
         return mainShape
     end
 
---[[VFX]]
-    colors = {
-        white = Vec(1,1,1),
-        black = Vec(0,0,0),
-        grey = Vec(0,0,0),
-        red = Vec(1,0,0),
-        blue = Vec(0,0,1),
-        yellow = Vec(1,1,0),
-        purple = Vec(1,0,1),
-        green = Vec(0,1,0),
-        orange = Vec(1,0.5,0),
-    }
-    function DrawDot(pos, l, w, r, g, b, a, dt)
+function DrawDot(pos, l, w, r, g, b, a, dt)
         local dot = LoadSprite("ui/hud/dot-small.png")
         local spriteRot = QuatLookAt(pos, GetCameraTransform().pos)
         local spriteTr = Transform(pos, spriteRot)
         if dt == nil then dt = true end
         DrawSprite(dot, spriteTr, l or 0.2, w or 0.2, r or 1, g or 1, b or 1, a or 1, dt and true)
     end
-    function RGBTosRGBChannel(channel)
+
+function RGBTosRGBChannel(channel)
         if channel < 0.0031308 then
             return channel * 12.92
         else
             return (1.055 * (channel ^ (1/2.4))) - 0.055
         end
     end
-    function RGBTosRGB(rgb)
+
+function RGBTosRGB(rgb)
         local sr = RGBTosRGBChannel(rgb[1])
         local sg = RGBTosRGBChannel(rgb[2])
         local sb = RGBTosRGBChannel(rgb[3])
         return Vec(sr, sg, sb)
     end
-    function sRGBToRGBChannel(channel)
+
+function sRGBToRGBChannel(channel)
         if channel < 0.04045 then
             return channel / 12.92
         else
             return ((channel + 0.055) / 1.055) ^ 2.4
         end
     end
-    function sRGBToRGB(srgb)
+
+function sRGBToRGB(srgb)
         local r = sRGBToRGBChannel(srgb[1])
         local g = sRGBToRGBChannel(srgb[2])
         local b = sRGBToRGBChannel(srgb[3])
         return Vec(r, g, b)
     end
-    function HSVToRGB(hsv)
+
+function HSVToRGB(hsv)
         local H = ratio(hsv[1], 0, 1, 0, 360)
         local S = hsv[2]
         local V = hsv[3]
@@ -958,7 +971,8 @@
         end
         return VecAdd(rgbPrime, Vec(m, m, m))
     end
-    function RGBToHSV(rgb)
+
+function RGBToHSV(rgb)
         local R = rgb[1]
         local G = rgb[2]
         local B = rgb[3]
@@ -983,8 +997,8 @@
         local V = Cmax
         return Vec(H, S, V)
     end
-    -- Moves the saturation and value components of color to make it move the same way as moving from templateOrigin to templateTarget
-    function offsetColor(color, templateOrigin, templateTarget)
+
+function offsetColor(color, templateOrigin, templateTarget)
         local colorHSV = RGBToHSV(color)
         local templateOriginHSV = RGBToHSV(templateOrigin)
         local templateTargetHSV = RGBToHSV(templateTarget)
@@ -998,64 +1012,59 @@
         return finalColor
     end
 
-
-
---[[SOUND]]
-    local debugSounds = {
-        beep = LoadSound("warning-beep"),
-        buzz = LoadSound("light/spark0"),
-        chime = LoadSound("elevator-chime"),
-        valu = LoadSound("valuable.ogg"),}
-    function beep(pos, vol) PlaySound(debugSounds.beep, pos or GetCameraTransform().pos, vol or 0.3) end
-    function buzz(pos, vol) PlaySound(debugSounds.buzz, pos or GetCameraTransform().pos, vol or 0.3) end
-    function chime(pos, vol) PlaySound(debugSounds.chime, pos or GetCameraTransform().pos, vol or 0.3) end
-    function valu(pos, vol) PlaySound(debugSounds.valu, pos or GetCameraTransform().pos, vol or 0.3) end
-
-
-
---[[MATH]]
-    function round(n, dec) local pow = 10^dec return math.floor(n * pow) / pow end
-    --- return number if > 0, else return 0.00000001
-    function gtZero(n) if n <= 0 then return 0.00000001 end return n end
-    --- return number if not = 0, else return 0.00000001
-    function nZero(n) if n == 0 then return 0.00000001 end return n end
-    --- return random float between min and max
-    function rdmf(min, max)
+function beep(pos, vol) PlaySound(debugSounds.beep, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function buzz(pos, vol) PlaySound(debugSounds.buzz, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function chime(pos, vol) PlaySound(debugSounds.chime, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function valu(pos, vol) PlaySound(debugSounds.valu, pos or GetCameraTransform().pos, vol or 0.3) end
+
+function round(n, dec) local pow = 10^dec return math.floor(n * pow) / pow end
+
+function gtZero(n) if n <= 0 then return 0.00000001 end return n end
+
+function nZero(n) if n == 0 then return 0.00000001 end return n end
+
+function rdmf(min, max)
         min = min or 0
         max = max or 1
         return min + (math.random() * (max-min))
     end
-    --- return random int between min and max
-    function rdm(min, max) return math.random(min or 0, max or 1) end
-    --- return a random number following a standard normal distribution (mean of 0 and standard deviation of 1)
-    function rdmsd()
+
+function rdm(min, max) return math.random(min or 0, max or 1) end
+
+function rdmsd()
         return math.sqrt(-2*math.log(rdmf()))*math.cos(2*math.pi*rdmf())
     end
-    function clamp(value, min, max)
+
+function clamp(value, min, max)
         min = min or 0
         max = max or 1
         if value < min then value = min end
         if value > max then value = max end
         return value
     end
-    function wrap(value, min, max)
+
+function wrap(value, min, max)
         min = min or 0
         max = max or 1
         return (value - min) % ((max + 1) - min) + min
     end
-    -- Brings a value from range [mi, ma] to range [nmi, nma]
-    function ratio(value, mi, ma, nmi, nma)
+
+function ratio(value, mi, ma, nmi, nma)
         nmi = nmi or 0
         nma = nma or 1
         return (value - mi) * (nma - nmi) / (ma - mi) + nmi
     end
-    function oscillate(time)
+
+function oscillate(time)
         local a = (GetTime() / (time or 1)) % 1
         a = a * math.pi
         return math.sin(a)
     end
-    -- return a random point on the surface of a sphere centered on center and of radius radius
-    function getRandPointOnSphere(center, radius)
+
+function getRandPointOnSphere(center, radius)
         local lambda = rdmf(-180, 180)
         local phi = math.acos(2 * rdmf() - 1)
         local x = math.cos(lambda) * math.cos(phi)
@@ -1063,10 +1072,12 @@
         local z = math.sin(lambda)
         return VecAdd(center, Vec(x * radius, y * radius, z * radius))
     end
-    function floatToInt(float)
+
+function floatToInt(float)
         return math.floor(float + .5)
     end
-    function getMinDistBetweenSpherePoints(transform, radius, samples)
+
+function getMinDistBetweenSpherePoints(transform, radius, samples)
 		local points = {}
 		local sqrt, sin, cos = math.sqrt, math.sin, math.cos
 		radius = radius or 1
@@ -1089,17 +1100,16 @@
         -- dbp("getMinDistBetweenSpherePoints radius="..radius..", samples="..samples..", dist="..dist)
 		return dist
 	end
-    -- Interpolate linearly between current value and target value at given speed
-    function linearInterp(startVal, endVal, speed)
+
+function linearInterp(startVal, endVal, speed)
         if endVal < startVal then
             return math.max(startVal - speed, endVal)
         else
             return math.min(startVal + speed, endVal)
         end
     end
-    -- Generate a uniformly distributed point on a 2D disk
-    -- and return its 3D coordinates
-    function getRandPointOnDisk(center, normal, radius)
+
+function getRandPointOnDisk(center, normal, radius)
         -- Find random 2D coordinates in the 2D disk centered on (0, 0)
         local r = math.sqrt(rdmf(0, radius*radius))
         local theta = rdmf(0, 2.0 * math.pi)
@@ -1111,43 +1121,39 @@
         dbw("y", y)
         return convert2DPointto3D(center, normal, x, y)
     end
-    -- Converts a 2D point onto a 3D plane,
-    -- assumig center is coordinate (0, 0) in 2D,
-    -- and using arbitrary unit vectors
-    function convert2DPointto3D(center, normal, x, y)
+
+function convert2DPointto3D(center, normal, x, y)
         local tr = Transform(center, QuatRotateQuat(QuatLookAt(center, VecAdd(center, normal)), QuatEuler(90, 0, 0)))
         local offset = TransformToParentVec(tr, Vec(x, 0, y))
         return VecAdd(center, offset)
     end
-    function sign(number)
+
+function sign(number)
         return number > 0 and 1 or (number == 0 and 0 or -1)
     end
 
-
---[[LOGIC]]
-    function ternary ( cond , T , F )
+function ternary ( cond , T , F )
         if cond then return T else return F end
     end
 
-
-
---[[FORMATTING]]
-    --- string format. default 2 decimals.
-    function sfn(numberToFormat, dec)
+function sfn(numberToFormat, dec)
         local s = (tostring(dec or 2))
         return string.format("%."..s.."f", numberToFormat)
     end
-    function sfnTime(dec) return sfn(' '..GetTime(), dec or 4) end
-    function sfnCommas(dec)
+
+function sfnTime(dec) return sfn(' '..GetTime(), dec or 4) end
+
+function sfnCommas(dec)
         return tostring(math.floor(dec)):reverse():gsub("(%d%d%d)","%1,"):gsub(",(%-?)$","%1"):reverse()
         -- https://stackoverflow.com/questions/10989788/format-integer-in-lua
     end
-    function TransformStrDeg(tr)
+
+function TransformStrDeg(tr)
         local x, y, z = GetQuatEuler(tr.rot)
         return VecStr(tr.pos)..'/'..VecStr(Vec(x, y, z))
     end
 
-    function sSplit(inputstr, sep)
+function sSplit(inputstr, sep)
         if sep == nil then
             sep = "%s"
         end
@@ -1157,10 +1163,12 @@
         end
         return t
     end
-    function BoolToStr(bool)
+
+function BoolToStr(bool)
         return bool and "true" or "false"
     end
-    function hasWord(list, word)
+
+function hasWord(list, word)
         local words = sSplit(list)
         for i=1,#words do
             if words[i] == word then
@@ -1169,7 +1177,8 @@
         end
         return false
     end
-    function StrToTable(str, isNum, delim)
+
+function StrToTable(str, isNum, delim)
         delim = delim or ","
         local splittedStr = sSplit(str, delim)
         local out = {}
@@ -1186,7 +1195,8 @@
         end
         return out
     end
-    function TableToStr(tab, delim)
+
+function TableToStr(tab, delim)
         delim = delim or ","
         local sepTab = {}
         for i=1,#tab do
@@ -1198,16 +1208,7 @@
         return table.concat(sepTab)
     end
 
-
-
-
---[[TIMERS]]
-
-    ---Run a timer and a table of functions.
-    ---@param timer table -- = {time, delay}
-    ---@param functions table -- Table of functions that are called when time = 0.
-    ---@param runTime boolean -- Decrement time when calling this function.
-    function TimerRunTimer(timer, functions, runTime)
+function TimerRunTimer(timer, functions, runTime)
         if timer.time <= 0 then
             TimerResetTime(timer)
 
@@ -1220,42 +1221,33 @@
         end
     end
 
-    -- Only runs the timer countdown if there is time left.
-    function TimerRunTime(timer)
-        if timer.time > 0 then
+function TimerRunTime(timer)
+        if timer.time ~= 0 then
             timer.time = timer.time - GetTimeStep()
         end
     end
 
-    -- Set time left to 0.
-    function TimerEndTime(timer)
+function TimerEndTime(timer)
         timer.time = 0
     end
 
-    -- Reset time to start delay.
-    function TimerResetTime(timer)
+function TimerResetTime(timer)
         timer.time = timer.delay
     end
 
---[[PLAYER]]
-
-    -- Get center point of the player
-    function GetPlayerCenter()
-        local playerEyeTr = GetPlayerCameraTransform()
-        local playerFeetTr = GetPlayerTransform()
+function GetPlayerCenter()
+        local playerEyeTr = GetPlayerCameraTransform(playerId)
+        local playerFeetTr = GetPlayerTransform(playerId)
         return VecAdd(playerFeetTr.pos, VecScale(VecSub(playerEyeTr.pos, playerFeetTr.pos), 0.5))
     end
 
-    -- Get direction the player is looking
-    function GetPlayerLookDir()
+function GetPlayerLookDir()
         local playerTr = GetCameraTransform()
         return TransformToParentVec(playerTr, Vec(0, 0, -1))
     end
 
-    -- Returns true if the given position is "inside" the player
-    function IsPointInPlayer(pos)
+function IsPointInPlayer(pos)
         local min, max = AabbGetPlayerBounds()
         return AabbCheckPointInside(min, max, pos)
     end
 
-    
```
