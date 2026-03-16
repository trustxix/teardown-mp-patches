# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,445 +1,4 @@
-#include "tdmp/utilities.lua"
-#include "tdmp/networking.lua"
-#include "tdmp/hooks.lua"
-#include "tdmp/player.lua"
-#include "tdmp/json.lua"
-
-if TDMP_LocalSteamId then
-    Hook_AddListener("ZigbertSpellSpawn", "Spawn", TDMP_ReceiveSpawn)
-end
-
-
-function init()
-    pi = 3.14159265
-
-    if TDMP_LocalSteamId then
-        multiplayer = true
-        
-        TDMP_RegisterEvent("ChangeSpell", 
-        function(data, steamid)
-            data = json.decode(data)
-            steamid = steamid or data[2]
-
-            otherSelectedSpells[steamid] = data[1]
-            if not TDMP_IsServer() then return end
-            data[2] = steamid
-            TDMP_ServerStartEvent("ChangeSpell", 
-            {
-                Reliable = true,
-                Receiver = TDMP.Enums.Receiver.ClientsOnly,
-                Data = data
-            })
-        end)
-
-    else
-        multiplayer = false
-    end
-
-    RegisterTool("zigbertSpells", "Spells", "")
-    SetBool("game.tool.zigbertSpells.enabled", true)
-
-    if GetFloat("savegame.mod.power") == 0 then
-        SetFloat("savegame.mod.power", 1)
-        SetFloat("savegame.mod.shake", 1)
-        SetFloat("savegame.mod.volume", 1)
-        SetBool("savegame.mod.idle", true)
-        SetFloat("savegame.mod.handColour", Random())
-        DebugPrint("Spells Mod Controls: Use Shift and Alt with the Scroll Wheel to select spells, and Lmb and Rmb to cast the spells, have fun!")
-    end
-
-    powerModifier = GetFloat("savegame.mod.power")
-    if multiplayer then power = 1 end
-    handColour = GetFloat("savegame.mod.handColour")
-    cameraShake = GetFloat("savegame.mod.shake")
-    volume = GetFloat("savegame.mod.volume")
-    idleSounds = GetBool("savegame.mod.idle")
-    robotDmg = 1
-    useKeybindL = "lmb"
-    useKeybindR = "rmb"
-    selectKeybindL = "shift"
-    selectKeybindR = "alt"
-    scrollKeybind = "mousewheel"
-
-    skinToneA = {210 / 255, 180 / 255, 140 / 255}
-    skinToneB = {53 / 255, 40 / 255, 30 / 255}
-
-    handsRGB = tostring(Lerp(skinToneA[1], skinToneB[1], handColour)) .. " " .. tostring(Lerp(skinToneA[2], skinToneB[2], handColour)) .. " " .. tostring(Lerp(skinToneA[3], skinToneB[3], handColour))
-    handModels = {'<body name="handL" dynamic="false">\n    <location rot="90 180 0">\n        <voxbox pos="0.2 0.0 0.13" rot="0.0 180.0 10.0" size="1 5 2" color="' .. handsRGB .. '" collide="false">\n            <location pos="-0.0 0.4 0.0" rot="-10.0 0.0 0.0">\n                <voxbox pos="-0.02 0.0 0.0" rot="0.0 0.0 0.0" size="2 1 2" color="' .. handsRGB .. '" collide="false">\n                    <voxbox pos="0.0 0.1 0.08" rot="70.0 0.0 0.0" size="2 1 1" color="' .. handsRGB .. '" collide="false">\n                        <voxbox pos="0.0 0.05 0.05" rot="-40.0 0.0 0.0" size="2 2 1" color="' .. handsRGB .. '" collide="false"/>\n                    </voxbox>\n                    <voxbox pos="0.2 0.1 0.0" rot="180.0 -150.0 0.0" size="1 2 1" color="' .. handsRGB .. '" collide="false">\n                        <voxbox pos="0.0 0.15 0.1" rot="90.0 90.0 -45.0" size="1 1 2" color="' .. handsRGB .. '" collide="false"/>\n                    </voxbox>\n                </voxbox>\n            </location>\n            <voxbox pos="0.1 0.0 0.2" rot="0.0 110.0 0.0" size="1 5 1" color="' .. handsRGB .. '" collide="false">\n                <voxbox pos="-0.0 -0.0 0.1" rot="0.0 60.0 0.0" size="1 5 1" color="' .. handsRGB .. '" collide="false"/>\n            </voxbox>\n        </voxbox>\n        <location pos="0.2 0.0 0.2" rot="-10 0 -10">\n            <voxbox pos="-0.2 0.0 0.0" rot="0.0 90.0 0" size="1 5 2" color="' .. handsRGB .. '" collide="false"/>\n        </location>\n    </location>\n</body>', '<body name="handR" dynamic="false">\n    <location rot="90 180 0">\n        <voxbox pos="-0.2 0.0 -0.07" rot="0.0 0.0 10.0" size="1 5 2" color="' .. handsRGB .. '" collide="false">\n            <location pos="-0.0 0.4 0.2" rot="10.0 0.0 0.0">\n                <voxbox pos="-0.02 0.0 0.0" rot="0.0 90.0 0" size="2 1 2" color="' .. handsRGB .. '" collide="false">\n                    <voxbox pos="0.08 0.1 0.0" rot="0.0 0.0 -70.0" size="1 1 2" color="' .. handsRGB .. '" collide="false">\n                        <voxbox pos="0.05 0.05 0.0" rot="0.0 0.0 40.0" size="1 2 2" color="' .. handsRGB .. '" collide="false"/>\n                    </voxbox>\n                    <voxbox pos="0.0 -0.1 0.2" rot="0.0 60.0 0.0" size="1 2 1" color="' .. handsRGB .. '" collide="false">\n                        <voxbox pos="0.0 0.05 0.1" rot="-45.0 0.0 0.0" size="1 1 2" color="' .. handsRGB .. '" collide="false"/>\n                    </voxbox>\n                </voxbox>\n            </location>\n            <voxbox pos="0.1 0.0 -0.0" rot="0.0 -20.0 0.0" size="1 5 1" color="' .. handsRGB .. '" collide="false">\n                <voxbox pos="0.1 -0.0 -0.0" rot="0.0 -60.0 0.0" size="1 5 1" color="' .. handsRGB .. '" collide="false"/>\n            </voxbox>\n        </voxbox>\n        <voxbox pos="-0.2 0.0 0.2" rot="-10.2 88.2 -9.8" size="1 5 2" color="' .. handsRGB .. '" collide="false"/>\n    </location>\n</body>'}
-    
-
-
-    spellNum = 18
-    cooldowns = {1, 1, 60, 1, 1, 1, 80, 1, 1, 1, 20, 1, 30, 1, 1, 1, 1, 120}
-    spellSounds = {5, 1, 17, 10, 2, 4, 20, 9, 4, 3, 18, 8, 19, 6, 7, 11, 9, 21}
-    spells = {"MagicBlast", "FireBeam", "Lightning", "WindGust", "Freeze", "Light", "BoulderThrow", "WaterBeam", "Fly", "Hold", "Slash", "CarnageVortex", "Vines", "Shield", "SunRay", "BlackHole", "Acid", "Teleport"}
-
-    player = {}
-    player.selectedSpell = {1, 1}
-    player.selectedSpellSmooth = {1, 1}
-    player.cooldown = {0, 0}
-    player.handBody = {0, 0}
-    player.handState = {0, 0}
-    player.scrollFade = {0, 0}
-    player.handMoveSmooth = {0, 0}
-    player.uiSelectSize = {0, 0}
-    player.spellsEquipped = false
-    player.lastScroll = 0
-    player.currentScroll = 0
-    player.magicLight = 0
-    player.heldBody = 0
-    player.castingHold = false
-    player.distance = 0
-    player.shieldBody = 0
-
-    soundLoops = {LoadLoop("MOD/snd/fireLoop.ogg"), LoadLoop("MOD/snd/freezeLoop.ogg"), LoadLoop("MOD/snd/holdLoop.ogg"), LoadLoop("MOD/snd/lightLoop.ogg"), LoadLoop("MOD/snd/magicBlastLoop.ogg"), LoadLoop("MOD/snd/shieldLoop.ogg"), LoadLoop("MOD/snd/sunLoop.ogg"), LoadLoop("MOD/snd/vortexLoop.ogg"), LoadLoop("MOD/snd/waterLoop.ogg"), LoadLoop("MOD/snd/windLoop.ogg"), LoadLoop("MOD/snd/blackHoleLoop.ogg"), LoadLoop("")}
-    sounds = {LoadSound("thunder0.ogg"), LoadSound("MOD/snd/cut0.ogg"), LoadSound("MOD/snd/vines.ogg"), LoadSound("masonry/break-l0.ogg"), LoadSound("MOD/snd/teleport.ogg")}
-    sndRobotDestroy = LoadSound("robot/disable0.ogg")
-    sndlightning = LoadSound("thunder-strike.ogg")
-    sndHit = LoadLoop("MOD/snd/hit.ogg")
-
-    spellStuffThing = {}
-    spellStuffThing.magicLight = 0
-    spellStuffThing.heldBody = 0
-    spellStuffThing.castingHold = false
-    spellStuffThing.distance = 0
-    spellStuffThing.shieldBody = 0
-
-    if multiplayer then
-        otherSelectedSpells = {}
-        otherSpellsCooldown = {}
-        spellStuff = {}
-    end
-end
-
-function tick(dt)
-    if multiplayer then 
-        local players = TDMP_GetPlayers()
-        for playerNum, pl in ipairs(players) do
-            currentPlayer = Player(pl.steamId)
-            if  (not currentPlayer:IsMe()) and (currentPlayer:CurrentTool() == "zigbertSpells") and (not currentPlayer:IsDrivingVehicle()) then
-                otherSelectedSpells[currentPlayer.steamId] = otherSelectedSpells[currentPlayer.steamId] or {1, 1}
-                otherSpellsCooldown[currentPlayer.steamId] = otherSpellsCooldown[currentPlayer.steamId] or {100, 100}
-                spellStuff[currentPlayer.steamId] = spellStuff[currentPlayer.steamId] or spellStuffThing
-
-
-
-                --if (not (spellStuff[currentPlayer.steamId].heldBody == 0)) and (not spellStuff[currentPlayer.steamId].castingHold) then
-                --    spellStuff[currentPlayer.steamId].heldBody = 0
-                --end
-                --spellStuff[currentPlayer.steamId].castingHold = false
-                if not (spellStuff[currentPlayer.steamId].magicLight == 0) then
-                    Delete(spellStuff[currentPlayer.steamId].magicLight)
-                    spellStuff[currentPlayer.steamId].magicLight = 0
-                end
-                if not (spellStuff[currentPlayer.steamId].shieldBody == 0) then
-                    Delete(spellStuff[currentPlayer.steamId].shieldBody)
-                    spellStuff[currentPlayer.steamId].shieldBody = 0
-                end
-        
-
-                
-                mpDual = false
-                if (currentPlayer:IsInputDown("lmb") and currentPlayer:IsInputDown("rmb")) then
-                    mpDual = true
-                    if ((otherSpellsCooldown[currentPlayer.steamId][1]) == 0) and ((otherSpellsCooldown[currentPlayer.steamId][2]) == 0) then
-                        powerMod = 1.5
-                        cam = currentPlayer:GetCamera()
-                        if cooldowns[otherSelectedSpells[currentPlayer.steamId][1]] < 3 then
-                            powerMod = 2
-                        end
-                        CastSpell(VecAdd(cam.pos, TransformToParentVec(cam, Vec(0, -0.4, -1.3))), cam, otherSelectedSpells[currentPlayer.steamId][1], powerMod, Vec(0, 0, 0), currentPlayer.steamId)
-                        otherSpellsCooldown[currentPlayer.steamId][1] = cooldowns[otherSelectedSpells[currentPlayer.steamId][1]]
-                        otherSpellsCooldown[currentPlayer.steamId][2] = cooldowns[otherSelectedSpells[currentPlayer.steamId][2]]
-                    end
-                    for i=1, 2 do
-                        otherSpellsCooldown[currentPlayer.steamId][i] = otherSpellsCooldown[currentPlayer.steamId][i] - 0.5
-                        if otherSpellsCooldown[currentPlayer.steamId][i] < 0 then otherSpellsCooldown[currentPlayer.steamId][i] = 0 end
-                    end
-                end
-                if (currentPlayer:IsInputDown("lmb") and (not mpDual)) and ((otherSpellsCooldown[currentPlayer.steamId][1]) == 0) then
-                    cam = currentPlayer:GetCamera()
-                    CastSpell(VecAdd(cam.pos, TransformToParentVec(cam, Vec(-0.5, -0.4, -1.1))), cam, otherSelectedSpells[currentPlayer.steamId][1], 1, Vec(0, 0, 0), currentPlayer.steamId)
-                    otherSpellsCooldown[currentPlayer.steamId][1] = cooldowns[otherSelectedSpells[currentPlayer.steamId][1]]
-                end
-                if (currentPlayer:IsInputDown("rmb") and (not mpDual)) and ((otherSpellsCooldown[currentPlayer.steamId][2]) == 0) then
-                    cam = currentPlayer:GetCamera()
-                    CastSpell(VecAdd(cam.pos, TransformToParentVec(cam, Vec(0.5, -0.4, -1.1))), cam, otherSelectedSpells[currentPlayer.steamId][2], 1, Vec(0, 0, 0), currentPlayer.steamId)
-                    otherSpellsCooldown[currentPlayer.steamId][2] = cooldowns[otherSelectedSpells[currentPlayer.steamId][2]]
-                end
-                for i=1, 2 do
-                    otherSpellsCooldown[currentPlayer.steamId][i] = otherSpellsCooldown[currentPlayer.steamId][i] - 1
-                    if otherSpellsCooldown[currentPlayer.steamId][i] < 0 then otherSpellsCooldown[currentPlayer.steamId][i] = 0 end
-                end
-
-            end
-        end
-    end
-    
-    if true then
-        use = {InputDown(useKeybindL), InputDown(useKeybindR)}
-        spellSelect = {InputDown(selectKeybindL), InputDown(selectKeybindR)}
-        scroll = InputValue(scrollKeybind)
-        vehicle = GetPlayerVehicle()
-        currentEquip = (GetString("game.player.tool") == "zigbertSpells")
-
-        player.lastScroll = player.currentScroll
-        player.currentScroll = player.currentScroll + scroll
-        if (player.spellsEquipped) and (not (currentEquip)) then
-            if spellSelect[1] or spellSelect[2] or use[1] or use[2] then
-                SetString("game.player.tool", "zigbertSpells")
-                currentEquip = true
-            end
-        end
-        player.spellsEquipped = currentEquip
-
-        desiredhandState = {0, 0}
-        if currentEquip then
-            ReleasePlayerGrab()
-            desiredhandState[1] = 1
-            desiredhandState[2] = 1
-        else
-            desiredhandState[1] = 0
-            desiredhandState[2] = 0
-        end
-        if not (vehicle == 0) then
-            desiredhandState[1] = 0
-            desiredhandState[2] = 0
-        end
-
-
-
-        if (not (player.heldBody == 0)) and (not player.castingHold) then
-            player.heldBody = 0
-        end
-        player.castingHold = false
-        if not (player.magicLight == 0) then
-            Delete(player.magicLight)
-            player.magicLight = 0
-        end
-        if not (player.shieldBody == 0) then
-            Delete(player.shieldBody)
-            player.shieldBody = 0
-        end
-
-
-
-        for i=1, 2 do
-            if use[i] and desiredhandState[i] == 1 then desiredhandState[i] = 2 end
-        end
-
-
-        dual = false
-        if player.selectedSpell[1] == player.selectedSpell[2] and desiredhandState[1] == 2 and desiredhandState[2] == 2 then
-            dual = true
-            if player.cooldown[1] == 0 and player.cooldown[2] == 0 then
-                powerMod = 1.5
-                if cooldowns[player.selectedSpell[1]] < 3 then
-                    powerMod = 2
-                end
-                velSet = CastSpell(VecAdd(GetPlayerCameraTransform().pos, TransformToParentVec(GetPlayerCameraTransform(), Vec(0, -0.4, -1.3))), GetPlayerCameraTransform(), player.selectedSpell[1], powerMod * powerModifier, GetPlayerVelocity(), 0)
-                SetPlayerVelocity(velSet)
-                MagicParticle(VecAdd(GetPlayerCameraTransform().pos, TransformToParentVec(GetPlayerCameraTransform(), Vec(0, -0.4, -1.3))), player.selectedSpell[1], 0.2)
-                ShakeCamera(cameraShake * 0.35)
-                for i=1, 2 do
-                    player.cooldown[i] = cooldowns[player.selectedSpell[i]]
-                end
-            end
-            for i=1, 2 do
-                player.cooldown[i] = player.cooldown[i] - 0.5
-            end
-        end
-
-
-
-        for i=1, 2 do
-            player.uiSelectSize[i] = player.uiSelectSize[i] - 0.08
-            if player.uiSelectSize[i] < 0 then player.uiSelectSize[i] = 0 end
-
-            if spellSelect[i] then 
-                if not (scroll == 0) then player.uiSelectSize[i] = 1 end
-                spellSelect[i] = true
-                player.scrollFade[i] = player.scrollFade[i] + 0.1 
-                if player.scrollFade[i] > 2 then player.scrollFade[i] = 2 end
-            else
-                player.scrollFade[i] = player.scrollFade[i] - 0.05
-                if player.scrollFade[i] < 0.1 then player.scrollFade[i] = 0.1 end
-            end
-
-            if player.handState[i] == 0 and desiredhandState[i] > 0 then
-                player.handState[i] = 1
-                temp = Spawn(handModels[i], GetPlayerCameraTransform())
-                player.handBody[i] = temp[1]
-            end
-            if player.handState[i] > 0 then
-                if desiredhandState[i] == 0 and (not (spellSelect[1] or spellSelect[2])) then
-                    player.handState[i] = 0
-                    Delete(player.handBody[i])
-                end
-                if desiredhandState[i] == 1 then
-                    player.handMoveSmooth[i] = player.handMoveSmooth[i] - 0.1
-                    MagicParticle(VecAdd(TransformToParentVec(GetPlayerCameraTransform(), Vec(-0.45 + ((i - 1) * 0.9), -0.1, -0.95)), GetPlayerCameraTransform().pos), player.selectedSpell[i], ((cooldowns[(player.selectedSpell[i])] - player.cooldown[i]) / cooldowns[(player.selectedSpell[i])]) * 0.1)
-                    if idleSounds then
-                        SpellSound(VecAdd(TransformToParentVec(GetPlayerCameraTransform(), Vec(-0.45 + ((i - 1) * 0.9), -0.1, -0.95)), GetPlayerCameraTransform().pos), player.selectedSpell[i], 0.4, 0.01)
-                    end
-                    else
-                    player.handMoveSmooth[i] = player.handMoveSmooth[i] + 0.1
-                end
-            end
-            if player.handMoveSmooth[i] < 0 then player.handMoveSmooth[i] = 0 end
-            if player.handMoveSmooth[i] > 1 then player.handMoveSmooth[i] = 1 end
-
-
-
-            if currentEquip then
-                if spellSelect[i] then
-                    player.selectedSpell[i] = player.selectedSpell[i] + scroll
-                end
-                player.selectedSpellSmooth[i] = Lerp(player.selectedSpellSmooth[i], player.selectedSpell[i], 0.1)
-                if player.selectedSpell[i] < 1 then
-                    player.selectedSpell[i] = spellNum
-                    player.selectedSpellSmooth[i] = spellNum + 1 - (1 - player.selectedSpellSmooth[i])
-                end
-                if player.selectedSpell[i] > spellNum then
-                    player.selectedSpell[i] = 1 
-                    player.selectedSpellSmooth[i] = player.selectedSpellSmooth[i] - spellNum
-                end
-
-                if not dual then
-                    if desiredhandState[i] == 2 and player.cooldown[i] == 0 then
-                        velSet = CastSpell(VecAdd(GetPlayerCameraTransform().pos, TransformToParentVec(GetPlayerCameraTransform(), Vec(-0.5 + (i - 1), -0.4, -1.1))), GetPlayerCameraTransform(), player.selectedSpell[i], powerModifier, GetPlayerVelocity(), 0)
-                        SetPlayerVelocity(velSet)
-                        ShakeCamera(cameraShake * 0.25)
-                        player.cooldown[i] = cooldowns[player.selectedSpell[i]]
-                    end
-                end
-
-
-                player.cooldown[i] = player.cooldown[i] - 1
-                if player.cooldown[i] < 0 then player.cooldown[i] = 0 end
-            
-                centerOffset = 0.4
-                rotationOffset = 0
-                if dual then 
-                    centerOffset = 0.15
-                    rotationOffset = 1
-                end
-                posTarget = VecLerp(VecAdd(TransformToParentVec(GetPlayerCameraTransform(), Vec(-0.65 + ((i - 1) * 1.3), -0.75, -0.8)), GetPlayerCameraTransform().pos), VecAdd(TransformToParentVec(GetPlayerCameraTransform(), Vec((-1 * centerOffset) + ((i - 1) * centerOffset * 2), -0.4, -0.5)), GetPlayerCameraTransform().pos), player.handMoveSmooth[i])
-                rotTarget = QuatSlerp(QuatRotateQuat(GetPlayerCameraTransform().rot, QuatEuler(90, -120 + ((i - 1) * 240), 0)), QuatRotateQuat(GetPlayerCameraTransform().rot, QuatEuler(10 * rotationOffset, 0, (45 - ((i - 1) * 90)) * rotationOffset)), player.handMoveSmooth[i])
-                pos = VecAdd(VecLerp(posTarget, GetBodyTransform(player.handBody[i]).pos, 0.15), VecScale(GetPlayerVelocity(), 1/60))
-                rot = QuatSlerp(rotTarget, GetBodyTransform(player.handBody[i]).rot, 0.15)
-                SetBodyTransform(player.handBody[i], Transform(pos, rot))
-            end
-
-        end
-    end
-
-    if (not (scroll == 0)) and currentEquip and (spellSelect[1] or spellSelect[2]) and multiplayer then
-        TDMP_ClientStartEvent("ChangeSpell", 
-        {
-            Reliable = true,
-            Data = {player.selectedSpell}
-        })
-    end
-end
-
-function draw(dt)
-    if player.spellsEquipped then
-        points = spellNum * 2
-        UiFont("bold.ttf", 40)
-        for i=1, 2 do
-            if i == 1 then UiAlign("left middle") end
-            if i == 2 then UiAlign("right middle") end
-            UiColor(0.5, 0.5, 0.5, player.scrollFade[i])
-            UiPush()
-                UiTranslate(-100 + ((i - 1) * (UiWidth() + 200)), UiHeight() / 2)
-                for j=1, points do
-                    display = j
-                    while display > spellNum do
-                        display = display - spellNum
-                    end
-                    UiPush()
-                        angle = (2 - ((i - 1) * 4)) * pi * ((j - player.selectedSpellSmooth[i]) / points)
-                        UiTranslate(math.cos(angle) * 150, math.sin(angle) * 300)
-                        if display == player.selectedSpell[i] then
-                            UiScale(1 + math.pow(player.uiSelectSize[i], 2) * 0.25)
-                            UiColor(1, 1, 1, player.scrollFade[i])
-                        end
-                        UiText(spells[display])
-                    UiPop()
-                end
-            UiPop()
-        end
-    end
-end
-
-function Lerp(a, b, x)
-    return(a * (1 - x) + b * x)
-end
-
-function RejectBodies()
-    QueryRejectBody(player.handBody[1])
-    QueryRejectBody(player.handBody[2])
-    if not (player.shieldBody == 0) then
-        QueryRejectBody(player.shieldBody)
-    end
-end
-
-function RandomVector(magnitude)
-    local x = Random()
-    local y = Random()
-    local z = Random()
-    return Vec((x - 0.5) * 2 * magnitude, (y - 0.5) * 2 * magnitude, (z - 0.5) * 2 * magnitude)
-end
-
-function Random()
-    return math.random(0, 1000) / 1000
-end
-
-function VecClamp(vec)
-    if vec[1] > 1 then vec[1] = 1 end
-    if vec[1] < -1 then vec[1] = -1 end
-    if vec[2] > 1 then vec[2] = 1 end
-    if vec[2] < -1 then vec[2] = -1 end
-    if vec[3] > 1 then vec[3] = 1 end
-    if vec[3] < -1 then vec[3] = -1 end
-    return vec
-end
-
-function Damage(pos, dmgType, soft, med, hard, robotMod)
-    if dmgType == 0 then
-        MakeHole(pos, soft, med, hard, false)
-        local hit, point, normal, shape = QueryClosestPoint(pos, 0.3)
-        if robotMod == nil then
-            robotMod = 1
-        end
-        if hit then 
-            SetFloat("level.destructible-bot.hitCounter", 0)
-            SetInt("level.destructible-bot.hitShape", shape)
-            SetString("level.destructible-bot.weapon", "SpellMod")
-            SetFloat("level.destructible-bot.damage", Lerp(soft, med, 0.5) * 3 * robotDmg * robotMod)
-        end 
-        len = VecLength(VecSub(GetPlayerPos(), pos))
-        if len < Lerp(soft, med, 0.5) + 1.2 then
-            SetPlayerHealth(GetPlayerHealth() - (2 / (len + 1) * Lerp(soft, med, 0.5) * 1/60))
-        end
-    end
-    if dmgType == 1 then
-        Explosion(pos, soft)
-    end
-end
-
-function SpellSound(pos, id, power, frequency)
-    if spellSounds[id] > 16 then
-        if frequency < 1 then
-            PlayLoop(soundLoops[spellSounds[6]], pos, volume * math.min(power, 2))
-        else
-            PlaySound(sounds[spellSounds[id] - 16], pos, volume * math.min(power, 2))
-        end
-    else
-        PlayLoop(soundLoops[spellSounds[id]], pos, volume * math.min(power, 2))
-    end
-end
-
+#version 2
 function SpellSpawn(xml, transform, allowStatic, jointExisting, normalSpawn)
     if normalSpawn or (not multiplayer) then
         return Spawn(xml, transform, allowStatic, jointExisting)
@@ -893,7 +452,7 @@
             SpawnParticle(VecAdd(VecLerp(endPos, pos, Random()), RandomVector(1)), RandomVector(1), 1)
         end
         if caster == 0 then
-            SetPlayerTransform(Transform(endPos, GetPlayerTransform().rot))
+            SetPlayerTransform(playerId, Transform(endPos, GetPlayerTransform(playerId).rot))
         end
     end
     return velSet
@@ -1061,4 +620,5 @@
     if spell == 18 then Particle("purple", size) end
     if spell == 18 then ParticleTile(0) end
     SpawnParticle(pos, Vec(0, 0, 0), 0.2)
-end+end
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
@@ -1,14 +1,15 @@
---This script will run on all levels when mod is active.
---Modding documentation: http://teardowngame.com/modding
---API reference: http://teardowngame.com/modding/api.html
+#version 2
+function Lerp(a, b, x)
+    return(a * (1 - x) + b * x)
+end
 
-function init()
+function server.init()
     if GetFloat("savegame.mod.power") == 0 then
-        SetFloat("savegame.mod.power", 1)
-        SetFloat("savegame.mod.shake", 1)
-        SetFloat("savegame.mod.volume", 1)
-        SetBool("savegame.mod.idle", true)
-        SetFloat("savegame.mod.handColour", math.random(0, 100) / 100)
+        SetFloat("savegame.mod.power", 1, true)
+        SetFloat("savegame.mod.shake", 1, true)
+        SetFloat("savegame.mod.volume", 1, true)
+        SetBool("savegame.mod.idle", true, true)
+        SetFloat("savegame.mod.handColour", math.random(0, 100) / 100, true)
     end
     powerModifier = GetFloat("savegame.mod.power")
     handColour = GetFloat("savegame.mod.handColour")
@@ -20,15 +21,13 @@
     sliderThreeState = 0
     sliderFourState = 0
     firstButtonClick = false
-
     spellNum = 9
     spells = {"MagicBlast", "FireBeam", "Lightning", "WindGust", "Freeze", "Light", "BoulderThrow", "WaterBeam", "Fly"}
-
     skinToneA = {210 / 255, 180 / 255, 140 / 255}
     skinToneB = {53 / 255, 40 / 255, 30 / 255}
 end
 
-function draw(dt)
+function client.draw()
     mouseX, mouseY = UiGetMousePos()
 
     if (mouseX > (UiWidth() / 2) + (handColour * 200) + 32.5) and (mouseX < (UiWidth() / 2) + (handColour * 200) + 67.5) and (mouseY > 182.5) and (mouseY < 217.5) then
@@ -44,7 +43,7 @@
     end
     if sliderOneState == 2 then
         handColour = handColour + (InputValue("mousedx") / 400)
-        SetFloat("savegame.mod.handColour", handColour)
+        SetFloat("savegame.mod.handColour", handColour, true)
         if (not InputDown("lmb")) then
             sliderOneState = 0 
         end
@@ -64,7 +63,7 @@
     end
     if sliderTwoState == 2 then
         powerModifier = powerModifier + (InputValue("mousedx") / 400)
-        SetFloat("savegame.mod.power", powerModifier)
+        SetFloat("savegame.mod.power", powerModifier, true)
         if (not InputDown("lmb")) then
             sliderTwoState = 0 
         end
@@ -84,7 +83,7 @@
     end
     if sliderThreeState == 2 then
         cameraShake = cameraShake + (InputValue("mousedx") / 400)
-        SetFloat("savegame.mod.shake", cameraShake)
+        SetFloat("savegame.mod.shake", cameraShake, true)
         if (not InputDown("lmb")) then
             sliderThreeState = 0 
         end
@@ -104,7 +103,7 @@
     end
     if sliderFourState == 2 then
         volume = volume + (InputValue("mousedx") / 400)
-        SetFloat("savegame.mod.volume", volume)
+        SetFloat("savegame.mod.volume", volume, true)
         if (not InputDown("lmb")) then
             sliderFourState = 0 
         end
@@ -114,7 +113,7 @@
 
     if firstButtonClick then
         idleSounds = not idleSounds
-        SetBool("savegame.mod.idle", idleSounds)
+        SetBool("savegame.mod.idle", idleSounds, true)
     end
     UiAlign("center bottom")
     UiFont("bold.ttf", 50)
@@ -179,6 +178,3 @@
     UiPop()
 end
 
-function Lerp(a, b, x)
-    return(a * (1 - x) + b * x)
-end
```

---

# Migration Report: tdmp\hooks.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdmp\hooks.lua
+++ patched/tdmp\hooks.lua
@@ -1,12 +1,4 @@
---[[-------------------------------------------------------------------------
-Hooks allows you to "talk" with other lua statements(mods).
-Hooks aren't synced, so they're running only on your local machine
----------------------------------------------------------------------------]]
-
-if not TDMP_LocalSteamID then return end
-
-#include "json.lua"
-
+#version 2
 function Hook_Run(eventName, data, noPack)
 	data = data or ""
 	return TDMP_RunGlobalHook(eventName, noPack and tostring(data) or data ~= "" and json.encode(data) or "")
@@ -16,5 +8,5 @@
 	TDMP_AddGlobalHookListener(eventName, id, callback)
 end
 
--- deprecated
-function TDMP_Hook_Queue()end+function TDMP_Hook_Queue()end
+

```

---

# Migration Report: tdmp\json.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdmp\json.lua
+++ patched/tdmp\json.lua
@@ -1,367 +1 @@
-json = { _version = "0.1.2" }
-
-do
-	-------------------------------------------------------------------------------
-	-- Encode
-	-------------------------------------------------------------------------------
-
-	local encode
-
-	local escape_char_map = {
-	  [ "\\" ] = "\\",
-	  [ "\"" ] = "\"",
-	  [ "\b" ] = "b",
-	  [ "\f" ] = "f",
-	  [ "\n" ] = "n",
-	  [ "\r" ] = "r",
-	  [ "\t" ] = "t",
-	}
-
-	local escape_char_map_inv = { [ "/" ] = "/" }
-	for k, v in pairs(escape_char_map) do
-	  escape_char_map_inv[v] = k
-	end
-
-
-	local function escape_char(c)
-	  return "\\" .. (escape_char_map[c] or string.format("u%04x", c:byte()))
-	end
-
-
-	local function encode_nil(val)
-	  return "null"
-	end
-
-
-	local function encode_table(val, stack)
-	  local res = {}
-	  stack = stack or {}
-
-	  -- Circular reference?
-	  if stack[val] then error("circular reference") end
-
-	  stack[val] = true
-
-	  if rawget(val, 1) ~= nil or next(val) == nil then
-	    -- Treat as array -- check keys are valid and it is not sparse
-	    local n = 0
-	    for k in pairs(val) do
-	      if type(k) ~= "number" then
-	        error("invalid table: mixed or invalid key types")
-	      end
-	      n = n + 1
-	    end
-	    if n ~= #val then
-	      error("invalid table: sparse array")
-	    end
-	    -- Encode
-	    for i, v in ipairs(val) do
-	      table.insert(res, encode(v, stack))
-	    end
-	    stack[val] = nil
-	    return "[" .. table.concat(res, ",") .. "]"
-
-	  else
-	    -- Treat as an object
-	    for k, v in pairs(val) do
-	      if type(k) ~= "string" then
-	        error("invalid table: mixed or invalid key types")
-	      end
-	      table.insert(res, encode(k, stack) .. ":" .. encode(v, stack))
-	    end
-	    stack[val] = nil
-	    return "{" .. table.concat(res, ",") .. "}"
-	  end
-	end
-
-
-	local function encode_string(val)
-	  return '"' .. val:gsub('[%z\1-\31\\"]', escape_char) .. '"'
-	end
-
-	local function mathRound(num, decs)
-		local mult = 10 ^ (decs or 0)
-		return math.floor(num * mult + .5) / mult
-	end
-
-	local function encode_number(val)
-	  -- Check for NaN, -inf and inf
-	  if val ~= val or val <= -math.huge or val >= math.huge then
-	    error("unexpected number value '" .. tostring(val) .. "'")
-	  end
-	  return string.format("%.5g", mathRound(val, 5))
-	end
-
-
-	local type_func_map = {
-	  [ "nil"     ] = encode_nil,
-	  [ "table"   ] = encode_table,
-	  [ "string"  ] = encode_string,
-	  [ "number"  ] = encode_number,
-	  [ "boolean" ] = tostring,
-	}
-
-
-	encode = function(val, stack)
-	  local t = type(val)
-	  local f = type_func_map[t]
-	  if f then
-	    return f(val, stack)
-	  end
-	  error("unexpected type '" .. t .. "'")
-	end
-
-
-	function json.encode(val)
-	  return ( encode(val) )
-	end
-
-
-	-------------------------------------------------------------------------------
-	-- Decode
-	-------------------------------------------------------------------------------
-
-	local parse
-
-	local function create_set(...)
-	  local res = {}
-	  for i = 1, select("#", ...) do
-	    res[ select(i, ...) ] = true
-	  end
-	  return res
-	end
-
-	local space_chars   = create_set(" ", "\t", "\r", "\n")
-	local delim_chars   = create_set(" ", "\t", "\r", "\n", "]", "}", ",")
-	local escape_chars  = create_set("\\", "/", '"', "b", "f", "n", "r", "t", "u")
-	local literals      = create_set("true", "false", "null")
-
-	local literal_map = {
-	  [ "true"  ] = true,
-	  [ "false" ] = false,
-	  [ "null"  ] = nil,
-	}
-
-
-	local function next_char(str, idx, set, negate)
-	  for i = idx, #str do
-	    if set[str:sub(i, i)] ~= negate then
-	      return i
-	    end
-	  end
-	  return #str + 1
-	end
-
-
-	local function decode_error(str, idx, msg)
-	  local line_count = 1
-	  local col_count = 1
-	  for i = 1, idx - 1 do
-	    col_count = col_count + 1
-	    if str:sub(i, i) == "\n" then
-	      line_count = line_count + 1
-	      col_count = 1
-	    end
-	  end
-	  error( string.format("%s at line %d col %d", msg, line_count, col_count) )
-	end
-
-
-	local function codepoint_to_utf8(n)
-	  -- http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=iws-appendixa
-	  local f = math.floor
-	  if n <= 0x7f then
-	    return string.char(n)
-	  elseif n <= 0x7ff then
-	    return string.char(f(n / 64) + 192, n % 64 + 128)
-	  elseif n <= 0xffff then
-	    return string.char(f(n / 4096) + 224, f(n % 4096 / 64) + 128, n % 64 + 128)
-	  elseif n <= 0x10ffff then
-	    return string.char(f(n / 262144) + 240, f(n % 262144 / 4096) + 128,
-	                       f(n % 4096 / 64) + 128, n % 64 + 128)
-	  end
-	  error( string.format("invalid unicode codepoint '%x'", n) )
-	end
-
-
-	local function parse_unicode_escape(s)
-	  local n1 = tonumber( s:sub(1, 4),  16 )
-	  local n2 = tonumber( s:sub(7, 10), 16 )
-	   -- Surrogate pair?
-	  if n2 then
-	    return codepoint_to_utf8((n1 - 0xd800) * 0x400 + (n2 - 0xdc00) + 0x10000)
-	  else
-	    return codepoint_to_utf8(n1)
-	  end
-	end
-
-
-	local function parse_string(str, i)
-	  local res = ""
-	  local j = i + 1
-	  local k = j
-
-	  while j <= #str do
-	    local x = str:byte(j)
-
-	    if x < 32 then
-	      decode_error(str, j, "control character in string")
-
-	    elseif x == 92 then -- `\`: Escape
-	      res = res .. str:sub(k, j - 1)
-	      j = j + 1
-	      local c = str:sub(j, j)
-	      if c == "u" then
-	        local hex = str:match("^[dD][89aAbB]%x%x\\u%x%x%x%x", j + 1)
-	                 or str:match("^%x%x%x%x", j + 1)
-	                 or decode_error(str, j - 1, "invalid unicode escape in string")
-	        res = res .. parse_unicode_escape(hex)
-	        j = j + #hex
-	      else
-	        if not escape_chars[c] then
-	          decode_error(str, j - 1, "invalid escape char '" .. c .. "' in string")
-	        end
-	        res = res .. escape_char_map_inv[c]
-	      end
-	      k = j + 1
-
-	    elseif x == 34 then -- `"`: End of string
-	      res = res .. str:sub(k, j - 1)
-	      return res, j + 1
-	    end
-
-	    j = j + 1
-	  end
-
-	  decode_error(str, i, "expected closing quote for string")
-	end
-
-
-	local function parse_number(str, i)
-	  local x = next_char(str, i, delim_chars)
-	  local s = str:sub(i, x - 1)
-	  local n = tonumber(s)
-	  if not n then
-	    decode_error(str, i, "invalid number '" .. s .. "'")
-	  end
-	  return n, x
-	end
-
-
-	local function parse_literal(str, i)
-	  local x = next_char(str, i, delim_chars)
-	  local word = str:sub(i, x - 1)
-	  if not literals[word] then
-	    decode_error(str, i, "invalid literal '" .. word .. "'")
-	  end
-	  return literal_map[word], x
-	end
-
-
-	local function parse_array(str, i)
-	  local res = {}
-	  local n = 1
-	  i = i + 1
-	  while 1 do
-	    local x
-	    i = next_char(str, i, space_chars, true)
-	    -- Empty / end of array?
-	    if str:sub(i, i) == "]" then
-	      i = i + 1
-	      break
-	    end
-	    -- Read token
-	    x, i = parse(str, i)
-	    res[n] = x
-	    n = n + 1
-	    -- Next token
-	    i = next_char(str, i, space_chars, true)
-	    local chr = str:sub(i, i)
-	    i = i + 1
-	    if chr == "]" then break end
-	    if chr ~= "," then decode_error(str, i, "expected ']' or ','") end
-	  end
-	  return res, i
-	end
-
-
-	local function parse_object(str, i)
-	  local res = {}
-	  i = i + 1
-	  while 1 do
-	    local key, val
-	    i = next_char(str, i, space_chars, true)
-	    -- Empty / end of object?
-	    if str:sub(i, i) == "}" then
-	      i = i + 1
-	      break
-	    end
-	    -- Read key
-	    if str:sub(i, i) ~= '"' then
-	      decode_error(str, i, "expected string for key")
-	    end
-	    key, i = parse(str, i)
-	    -- Read ':' delimiter
-	    i = next_char(str, i, space_chars, true)
-	    if str:sub(i, i) ~= ":" then
-	      decode_error(str, i, "expected ':' after key")
-	    end
-	    i = next_char(str, i + 1, space_chars, true)
-	    -- Read value
-	    val, i = parse(str, i)
-	    -- Set
-	    res[key] = val
-	    -- Next token
-	    i = next_char(str, i, space_chars, true)
-	    local chr = str:sub(i, i)
-	    i = i + 1
-	    if chr == "}" then break end
-	    if chr ~= "," then decode_error(str, i, "expected '}' or ','") end
-	  end
-	  return res, i
-	end
-
-
-	local char_func_map = {
-	  [ '"' ] = parse_string,
-	  [ "0" ] = parse_number,
-	  [ "1" ] = parse_number,
-	  [ "2" ] = parse_number,
-	  [ "3" ] = parse_number,
-	  [ "4" ] = parse_number,
-	  [ "5" ] = parse_number,
-	  [ "6" ] = parse_number,
-	  [ "7" ] = parse_number,
-	  [ "8" ] = parse_number,
-	  [ "9" ] = parse_number,
-	  [ "-" ] = parse_number,
-	  [ "t" ] = parse_literal,
-	  [ "f" ] = parse_literal,
-	  [ "n" ] = parse_literal,
-	  [ "[" ] = parse_array,
-	  [ "{" ] = parse_object,
-	}
-
-
-	parse = function(str, idx)
-	  local chr = str:sub(idx, idx)
-	  local f = char_func_map[chr]
-	  if f then
-	    return f(str, idx)
-	  end
-	  decode_error(str, idx, "unexpected character '" .. chr .. "'")
-	end
-
-
-	function json.decode(str)
-	  if type(str) ~= "string" then
-	    error("expected argument of type string, got " .. type(str))
-	  end
-	  local res, idx = parse(str, next_char(str, 1, space_chars, true))
-	  idx = next_char(str, idx, space_chars, true)
-	  if idx <= #str then
-	    decode_error(str, idx, "trailing garbage")
-	  end
-	  return res
-	end
-end+#version 2

```

---

# Migration Report: tdmp\networking.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdmp\networking.lua
+++ patched/tdmp\networking.lua
@@ -1,78 +1,4 @@
---[[-------------------------------------------------------------------------
-Simple functions for networking stuff
----------------------------------------------------------------------------]]
-
-if not TDMP_LocalSteamID then return end
-
-#include "json.lua"
-
-TDMP = TDMP or {}
-TDMP.Enums = {
-	Receiver = {
-		All = 1, -- Everyone including server
-		ClientsOnly = 2, -- Everyone excluding server
-	}
-}
-
---[[-------------------------------------------------------------------------
-Event structure:
-
-(SERVER ONLY)
-Receiver = Who'd receive event?
-	"all" - broadcast event to all clients
-	"steamid" - send event only to client with this steamid
-	{"table", "of", "steamids"} - send event to each client in this table
-
-(SHARED)
-Reliable[bool] - If set to false/nil/not filled, the message is not guaranteed to reach its destination or reach in sending order.
-Keep it as true in very important data (such as shots, chat, etc), and keep it false/nil/not filled with not important data (such as physics)
-
-(optional)Data - table of custom data to be sent
-
-(optional)DontPack[bool] - if set to true, Data field wont be packed in json, instead, it would be turned into a string.
-Useful for network performance, if you need to send only bool, number or something what doesn't really need to be packed into a table
----------------------------------------------------------------------------]]
-
---[[-------------------------------------------------------------------------
-Server sends/broadcasts event to client(s)
----------------------------------------------------------------------------]]
-function TDMP_ServerStartEvent(eventName, eventData)
-	assert(eventName, "eventName is nil!")
-	assert(eventData.Receiver, "receiver is nil! (" .. eventName .. ")")
-
-	local data = eventData.Data and (eventData.DontPack and tostring(eventData.Data) or json.encode(eventData.Data)) or ""
-
-	local t = type(eventData.Receiver)
-	if t == "number" then
-		TDMP_BroadcastEvent(eventName, eventData.Reliable, eventData.Receiver == TDMP.Enums.Receiver.All, data)
-	elseif t == "string" then
-		TDMP_SendEvent(eventName, eventData.Receiver, eventData.Reliable, data)
-	elseif t == "table" then
-		for i, steamId in ipairs(eventData.Receiver) do
-			TDMP_SendEvent(eventName, steamId, eventData.Reliable, data)
-		end
-	else
-		error("Unknown type in TDMP_ServerStartEvent(".. eventName .. "): " .. t)
-	end
-
-	return data
-end
-
---[[-------------------------------------------------------------------------
-Client sends event to the server
----------------------------------------------------------------------------]]
-function TDMP_ClientStartEvent(eventName, eventData)
-	assert(eventName, "eventName is nil!")
-
-	local data = eventData.Data and (eventData.DontPack and tostring(eventData.Data) or json.encode(eventData.Data)) or ""
-	TDMP_SendEvent(eventName, nil, eventData.Reliable, data)
-
-	return data
-end
-
---[[-------------------------------------------------------------------------
-Spawns an entity for all clients. SERVER ONLY
----------------------------------------------------------------------------]]
+#version 2
 function TDMP_Spawn(hookName, xml, transform, allowStatic, jointExisting)
 	if not TDMP_IsServer() then return end
 
@@ -129,26 +55,3 @@
 	end
 end
 
--- local lastShapeNetworkId = 0
--- shapeIdToNetworkId = {}
--- networkIdToShape = {}
--- function TDMP_RegisterNetworkShape(shape, netId)
--- 	if not netId then
--- 		netId = lastShapeNetworkId
-
--- 		lastShapeNetworkId = lastShapeNetworkId + 1
--- 	end
-
--- 	shapeIdToNetworkId[shape] = netId
--- 	networkIdToShape[netId] = shape
-
--- 	return netId
--- end
-
--- function TDMP_GetShapeNetworkId(shape)
--- 	return shapeIdToNetworkId[shape]
--- end
-
--- function TDMP_GetShapeByNetworkId(networkId)
--- 	return networkIdToShape[networkId]
--- end
```

---

# Migration Report: tdmp\player.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdmp\player.lua
+++ patched/tdmp\player.lua
@@ -1,15 +1,4 @@
---[[-------------------------------------------------------------------------
-Simple metatable for people who likes.. metatables? And also not using
-TDMP_GetPlayerTransformCameraRotationPositionBlablabla() each time, what
-makes code look more clear and easier to read
----------------------------------------------------------------------------]]
-
-if not TDMP_LocalSteamID then return end
-#include "utilities.lua"
-
-Player = Player or {}
-Player.__index = Player
-
+#version 2
 function Player:GetTransform()
 	return TDMP_GetPlayerTransform(self.id)
 end
@@ -130,22 +119,3 @@
 	return 0
 end
 
-setmetatable(Player,
-	{
-		__call = function(self, ply)
-			local data = {}
-
-			local t = type(ply)
-			if t == "table" then
-				data = ply
-			else
-				data = TDMP_GetPlayer(ply)
-			end
-
-			if not data then return end
-
-			data.steamid = data.steamId
-			return setmetatable(data, Player)
-		end
-	}
-)
```

---

# Migration Report: tdmp\utilities.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tdmp\utilities.lua
+++ patched/tdmp\utilities.lua
@@ -1,140 +1,4 @@
-if not TDMP_LocalSteamID then return end
-#include "json.lua"
-#include "hooks.lua"
-#include "player.lua"
-
-TDMP = TDMP or {}
-
-TDMP.Input = {
-	mouse1 = 0,
-	lmb = 0,
-	mouse2 = 1,
-	rmb = 1,
-	w = 2,
-	a = 3,
-	s = 4,
-	d = 5,
-	jump = 6,
-	space = 6,
-	crouch = 7,
-	ctrl = 7,
-	e = 8,
-	interact = 8
-}
-
-TDMP.InputToString = {
-	[0] = "lmb",
-	[1] = "rmb",
-	[2] = "w",
-	[3] = "a",
-	[4] = "s",
-	[5] = "d",
-	[6] = "space",
-	[7] = "ctrl",
-	[8] = "interact",
-}
-
---[[-------------------------------------------------------------------------
-steamId [string]: Who's arms to control?
-target [table]: target for an arm. Do not fill if you want to reset to default values.
-Structure:
-{
-	pos = world position of target,
-	bias = LOCAL position of elbow's location. Optional
-}
-
-time [number]: for how long it should use this target? 0 for permanent
----------------------------------------------------------------------------]]
-function TDMP_SetLeftArmTarget(steamId, target)
-	Hook_Run("SetPlayerArmsTarget", {
-		steamid = steamId,
-
-		leftArm = target,
-	})
-end
-
-function TDMP_SetRightArmTarget(steamId, target)
-	Hook_Run("SetPlayerArmsTarget", {
-		steamid = steamId,
-
-		rightArm = target,
-	})
-end
-
-function TDMP_OverrideToolTransform(steamId, tr)
-	Hook_Run("SetPlayerToolTransform", {
-		steamid = steamId,
-
-		tr = tr,
-	})
-end
-
-function TDMP_AddToolModel(toolUniqueId, data)
-	Hook_Run("AddToolModel", data)
-
-	Hook_AddListener(toolUniqueId .. "_CreateWorldModel", toolUniqueId, function(data)
-		local ents = Spawn(data[1], data[2])
-
-		return json.encode(ents)
-	end)
-end
-
--- https://www.iquilezles.org/www/articles/intersectors/intersectors.htm
-local function IntersectSphere(rayOrigin, rayDir, spherePos, sphereRad)
-	local oc = VecSub(rayOrigin, spherePos)
-	local b = VecDot(oc, rayDir)
-	local c = VecDot(oc, oc) - sphereRad*sphereRad
-	local h = b*b - c
-
-	if h < 0 then return false end
-
-	h = math.sqrt(h)
-
-	return true, -b-h, -b+h
-end
-
-local cacheMin = Vec(-.35, 0, -.35)
---[[-------------------------------------------------------------------------
-Raycasts players and returning hit player, hit position and distance
----------------------------------------------------------------------------]]
-function TDMP_RaycastPlayer(startPos, direction, raycastLocal, length, ignoreIds)
-	length = length or math.huge
-	local hit, dist = QueryRaycast(startPos, direction, length)
-
-	if not hit then
-		local plys = TDMP_GetPlayers()
-		for i, pl in ipairs(plys) do
-			if raycastLocal or not TDMP_IsMe(pl.id) and (not ignoreIds or not ignoreIds[pl.steamId]) then
-				local pos = TDMP_GetPlayerTransform(pl.id).pos
-				local driving = pl.veh and pl.veh > 0
-
-				pos[2] = driving and pos[2] - .9 or pos[2]
-
-				local min, max = cacheMin, Vec(.35, (TDMP_IsPlayerInputDown(pl.id, 7) or driving) and 1.1 or 1.8, .35)
-
-				local sphereBottom = VecAdd(pos, Vec(0,.35,0))
-				local sphereCenter = VecAdd(pos, Vec(0,max[2]/2,0))
-				local sphereTop = VecAdd(pos, Vec(0,max[2]-.35,0))
-				local sIntersect, sMin, sM = IntersectSphere(startPos, direction, sphereBottom, .35)
-				local sIntersect2, sMin2, sM2 = IntersectSphere(startPos, direction, sphereCenter, .35)
-				local sIntersect3, sMin3, sM3 = IntersectSphere(startPos, direction, sphereTop, .35)
-
-				local int1, int2, int3 = sIntersect and math.abs(sMin), sIntersect2 and math.abs(sMin2), sIntersect3 and math.abs(sMin3)
-				local pDist = int1 or int2 or int3
-				if (pDist and pDist <= length) then
-					return pl, int1 and sphereTop or int2 and sphereCenter or sphereBottom, pDist, int1 and "Head" or int2 and "Body" or "Legs"
-				end
-			end
-		end
-	end
-
-	return false
-end
-
---[[-------------------------------------------------------------------------
-Returns shape which player interacts with. Mostly used for syncing buttons
-and triggers on the maps
----------------------------------------------------------------------------]]
+#version 2
 function TDMP_AnyPlayerInteractWithShape()
 	local plys = TDMP_GetPlayers()
 	for i, v in ipairs(plys) do
@@ -146,4 +10,5 @@
 	end
 
 	return -1
-end+end
+

```
