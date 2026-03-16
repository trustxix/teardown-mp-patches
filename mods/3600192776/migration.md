# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,64 +1,7 @@
-pbVersion = 1.4
-commanderPlaneTool = "pb_commander_plane"
+#version 2
+function server.init()
+    RegisterTool(commanderPlaneTool, "Commander Plane", "MOD/vox/3x3x3.vox")
+    SetBool(string.format("game.tool.%s.enabled", commanderPlaneTool), true, true)
+    initMod()
+end
 
---[[
-#include "script/common.lua"
-
-#include "src/sdk/symbols.lua"
-#include "src/colors.lua"
-#include "src/vectors.lua"
-#include "src/common.lua"
-#include "src/ui.lua"
-#include "src/sdk/base.lua"
-#include "src/sdk/weapons.lua"
-#include "src/sdk/commands.lua"
-#include "src/mod_options.lua"
-#include "src/randomizer.lua"
-#include "src/debugger.lua"
-#include "src/timer.lua"
-#include "src/sprites.lua"
-#include "src/vision.lua"
-#include "src/obstacle-avoid.lua"
-#include "src/crosshair.lua"
-#include "src/sounds.lua"
-#include "src/debris.lua"
-#include "src/particles.lua"
-#include "src/plane.lua"
-#include "src/ballistics.lua"
-#include "src/materials.lua"
-#include "src/milvision.lua"
-#include "src/ammo/base.lua"
-#include "src/ammo/small-caliber.lua"
-#include "src/ammo/debris-shrapnel.lua"
-#include "src/effects/fireball.lua"
-#include "src/ammo/artillery.lua"
-#include "src/ammo/rocketry.lua"
-#include "src/ammo/rocketry-advanced.lua"
-#include "src/ammo/rockets-incendiary.lua"
-#include "src/ammo/hand-held.lua"
-#include "src/ammo/bombs.lua"
-#include "src/rnd.lua"
-#include "src/tracker.lua"
-#include "src/autoaim.lua"
-#include "src/autopilot.lua"
-#include "src/weapons.lua"
-#include "src/phalanxPro.lua"
-#include "src/ironDome.lua"
-#include "src/antiAir.lua"
-#include "src/info.lua"
-#include "src/weapons/fx.lua"
-#include "src/weapons/casings.lua"
-#include "src/weapons/hand-held.lua"
-#include "src/weapons/hand-held-rotary.lua"
-#include "src/spotter.lua"
-#include "src/extensions/mods.lua"
-#include "src/api/pb.weapons.lua"
-#include "src/api/pb.commands.lua"
-#include "src/main.lua"
-]]
-function init()
-    RegisterTool(commanderPlaneTool, "Commander Plane", "MOD/vox/3x3x3.vox")
-    SetBool(string.format("game.tool.%s.enabled", commanderPlaneTool), true)
-    initMod()
-    --SetInt("game.fire.spread",2)
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
@@ -1,474 +1,7 @@
---[[
-#include "src/sdk/symbols.lua"
-#include "src/common.lua"
-#include "src/sdk/base.lua"
-#include "src/mod_options.lua"
-]]
-OptionHandler = {
-    lineH        = 35,
-    margin       = 10,
-    buttonWidth  = 150,
-    buttonHeight = 30,
-    editedAction = nil,
-    specialKeys  = {
-        esc = true,
-        shift = true,
-        tab = true,
-        rmb = true,
-        ["return"] = true,
-    },
-    process      = function(self)
-        if self.editedAction ~= nil then
-            local keyPressed = RealInputLastPressedKey()
-
-            if keyPressed ~= nil then
-                DebugPrint("Pressed:" .. keyPressed)
-
-                if self.specialKeys[keyPressed] ~= nil then
-                    if keyPressed == 'rmb' then
-                        self.editedAction = nil
-                        InputClear()
-                    end
-                else
-                    ModOptions:setKeyBind(self.editedAction, keyPressed)
-                    self.editedAction = nil
-                end
-            end
-        end
-    end,
-    page         = "home",
-    pages        = {
-        home = {
-            title = "",
-            links = {
-                { keybindings = 'Keybindings' },
-                { settings = 'Settings' },
-            },
-        },
-        settings = {
-            title = "Settings",
-            links = {
-                { gameplaySettings = 'Gameplay' },
-                { simulationSettings = 'Simulation' },
-                { effectsSettings = 'Effects' },
-                { soundSettings = 'Sound' },
-                { home = 'Back' },
-            },
-
-        },
-        gameplaySettings = {
-            title = "Gameplay Settings",
-            links = {
-                { settings = 'Back' },
-            },
-            settings = {
-                gameRedDotScale = {
-                    label = "Red-dot scale",
-                    suffix = "x",
-                    type = _buttonCycle,
-                    options = { 1, 1.25, 1.5, 2, 2.5 },
-                },
-                gameRedDotFlicker = {
-                    label = "Red-dot flicker",
-                    type = _buttonSwitch,
-                },
-                showDistanceMeter = {
-                    label = "Show distance meter",
-                    type = _buttonSwitch,
-                },
-                showIncomingTracker = {
-                    label = "Show incoming missiles tracker",
-                    type = _buttonSwitch,
-                },
-                ejectCasings = {
-                    label = "Weapons eject shell casings",
-                    type = _buttonSwitch,
-                },
-                gameScopeWindAid = {
-                    label = "Visual wind Aid in Sniper Scope",
-                    type = _buttonSwitch,
-                },
-                gameRealismScale = {
-                    label = "Realism(sway&recoil rate, reload times, wind strength)",
-                    suffix = "x",
-                    type = _buttonCycle,
-                    options = { 1.5, 1, .5, .25 },
-                },
-            },
-        },
-        soundSettings = {
-            title = "Sound Settings",
-            links = {
-                { settings = 'Back' },
-            },
-            settings = {
-                soundVolume = {
-                    label = "Global [PB] sound volume",
-                    suffix = "x",
-                    type = _buttonCycle,
-                    options = { .25, .5, .75, 1, 1.25, 1.5, 1.75, 2 },
-                },
-                casingSound = {
-                    label = "Shell casings produce sounds",
-                    type = _buttonSwitch,
-                },
-            },
-        },
-        simulationSettings = {
-            title = "Simulation Settings",
-            links = {
-                { settings = 'Back' },
-            },
-            settings = {
-                simApplyForce = {
-                    label = "Projectiles apply force on hit objects",
-                    type = _buttonSwitch,
-                },
-                randomWind = {
-                    label = "Random wind on level start",
-                    type = _buttonSwitch,
-                },
-                simPrecisePenetration = {
-                    label = "Sub-frame material penetration",
-                    type = _buttonSwitch,
-                },
-            },
-        },
-        effectsSettings = {
-            title = "Effects Settings",
-            links = {
-                { settings = 'Back' },
-            },
-            settings = {
-                effectsMpl = {
-                    label = "Effects level(# of sparks,shrapnel,muzzleflash,subprojectiles)",
-                    suffix = "x",
-                    type = _buttonCycle,
-                    options = { .25, .5, 1, 2, 4 },
-                },
-                barrelGlowMpl = {
-                    label = "Barrel glow rate",
-                    suffix = "x",
-                    type = _buttonCycle,
-                    options = { .25, .5, 1, 2, 5, 7.5, 10 },
-                },
-                effectsDebrisParticles = {
-                    label = "Spawn material debris",
-                    type = _buttonSwitch,
-                },
-                effectsDebrisSmoke = {
-                    label = "Debris dust",
-                    type = _buttonSwitch,
-                },
-                effectsApplyToVanilla = {
-                    label = "Apply effects to vanilla explosions",
-                    type = _buttonSwitch,
-                },
-                effectsVanillaShrapnel = {
-                    label = "Vanilla explosions produce shrapnel",
-                    type = _buttonSwitch,
-                },
-                effectsPhysicalProjectiles = {
-                    label = "Projectiles have physical bodies",
-                    type = _buttonSwitch,
-                },
-                effectsDebrisParticlesMpl = {
-                    label = "Material debris level",
-                    suffix = "x",
-                    type = _buttonCycle,
-                    options = { .5, 1, 1.5, 2, 2.5 },
-                },
-                effectsRocketTrail = {
-                    label = "Rockets smoke trail",
-                    type = _buttonSwitch,
-                },
-            },
-        },
-
-        keybindings = {
-            title = "Keybindings",
-            links = {
-                { keysGlobal = 'Global' },
-                { keysCommander = 'Commander Plane' },
-                { keysShared = 'Shared' },
-                { keysHandHeld = 'Hand-held weapons' },
-                { home = 'Back' },
-            },
-        },
-        keysGlobal = {
-            title = "Global Keybindings",
-            actions = {
-                { keyHelp = 'Show keybindings' },
-                { keyVisionMode = 'Cycle vision modes' },
-                { keyCycleOverlay = 'Cycle overlays/(+shift)Cycle HUD visibility level' },
-                { keyViewDistance = 'Viewing distance: Increase/(+shift)Deacrease' },
-                { keyViewDistance = '(+ctrl)Reset environment settings' },
-                { keyEffectsUp = 'Increase effects' },
-                { keyEffectsDown = 'Decrease effects' },
-                { keyRemoteTargeting = 'Remote targeting' },
-                { keyAutoAimMark = 'Auto-Aim: mark target/(+shift)mark 10 random targets' },
-                { keyAutoAimReset = 'Auto-Aim: reset targets' },
-                { keyAutoAimMode = 'Auto-Aim: switch mode' },
-                { keyAutoAimSpeedUp = 'Auto-Aim: speed up(smooth mode)' },
-                { keyAutoAimSlowDown = 'Auto-Aim: speed down(smooth mode)' },
-                { keySlowMo = 'SlowMo: realtime/(+shift)slow/(+shift)super slow' },
-                { keyShowTrajectory = 'Show projectile trajectory' },
-            },
-            links = {
-                { keybindings = 'Back' },
-            },
-        },
-        keysCommander = {
-            title = "Commander Plane Keybindings",
-            actions = {
-                { keyTiltRight = 'Aim: tilt right' },
-                { keyTiltLeft = 'Aim: tilt left' },
-                { keyElevationUp = 'Aim: up/(+shift)right' },
-                { keyElevationDown = 'Aim: down/(+shift)left' },
-                { keySpreadUp = 'Aim: spread up' },
-                { keySpreadDown = 'Aim: spread down' },
-                { keyAutoAimShoot = 'Auto-Aim: shoot' },
-                { keyGimbalLock = 'Switch aim-lock(Gimbal)' },
-                { keyHoverLock = 'Switch hover lock' },
-                { keyAutopilot = 'Switch autopilot' },
-            },
-            links = {
-                { keybindings = 'Back' },
-            },
-        },
-        keysHandHeld = {
-            title = "Hand-held Weapons Keybindings",
-            actions = {
-                { keyStance1 = 'Switch to 1st stance' },
-                { keyStance2 = 'Switch to 2nd stance' },
-                { keyFireMode = 'Cycle fire mode' },
-                { keyRedDot = 'Switch red dot ' },
-                { keySpotterCamera = 'Place spotter camera/(+alt)remove last spotter camera' },
-                { keySpotterCamera = '(+shift)Switch to spotter camera/(+shift+alt)remove all spotter camera' },
-                { keySpotterNext = 'Next spotter camera' },
-                { keySpotterPrev = 'Previous spotter camera' },
-            },
-            links = {
-                { keybindings = 'Back' },
-            },
-        },
-        keysShared = {
-            title = "Shared tools keybindings",
-            actions = {
-                { keyForward = 'Move: forward' },
-                { keyBackward = 'Move: backward' },
-                { keyRight = 'Move: right' },
-                { keyLeft = 'Move: left' },
-                { keyUp = 'Move: up/jump' },
-                { keyDown = 'Move: down/crouch' },
-                { keySwitchAmmo = 'Switch ammo slot' },
-                { keySwitchWeaponSlot = 'Switch weapon slot' },
-                { keyReload = 'Reload ammo slot' },
-                { keyAntiAirPlace = 'Place anti-air turret/(+shift)Switch anti-air system' },
-                { keyAntiAirClear = 'Remove last turret/(+shift) all turrets of a type' },
-                { keyAntiAirCamera = 'Switch to next anti-air camera/(+shift)switch off' },
-            },
-            links = {
-                { keybindings = 'Back' },
-            },
-        },
-    },
-    actions      = {
-        { keyHelp = 'Show keybindings' },
-        { keyForward = 'Move: forward' },
-        { keyBackward = 'Move: backward' },
-        { keyRight = 'Move: right' },
-        { keyLeft = 'Move: left' },
-        { keyUp = 'Move: up' },
-        { keyDown = 'Move: down' },
-        { keySwitchAmmo = 'Switch ammo slot' },
-        { keySwitchWeaponSlot = 'Switch weapon slot' },
-        { keyTiltRight = 'Aim: tilt right' },
-        { keyTiltLeft = 'Aim: tilt left' },
-        { keyElevationUp = 'Aim: up/(+shift)right' },
-        { keyElevationDown = 'Aim: down/(+shift)left' },
-        { keySpreadUp = 'Aim: spread up' },
-        { keySpreadDown = 'Aim: spread down' },
-        { keyAutoAimShoot = 'Auto-Aim: shoot' },
-        { keyAutoAimMark = 'Auto-Aim: mark target/(+shift)mark 10 random targets' },
-        { keyAutoAimReset = 'Auto-Aim: reset targets' },
-        { keyAutoAimMode = 'Auto-Aim: switch mode' },
-        { keyAutoAimSpeedUp = 'Auto-Aim: speed up(smooth mode)' },
-        { keyAutoAimSlowDown = 'Auto-Aim: speed down(smooth mode)' },
-        { keyGimbalLock = 'Switch aim-lock(Gimbal)' },
-        { keyVisionMode = 'Cycle vision modes' },
-        { keyHoverLock = 'Switch hover lock' },
-        { keyAutopilot = 'Switch autopilot' },
-        { keyCycleOverlay = 'Cycle overlays/(+shift)Cycle HUD visibility level' },
-        { keyAntiAirPlace = 'Place anti-air turret/(+shift)Switch anti-air system' },
-        { keyAntiAirClear = 'Remove last turret/(+shift) all turrets of a type' },
-        { keyAntiAirCamera = 'Switch to next anti-air camera/(+shift)switch off' },
-        { keyRemoteTargeting = 'Remote targeting' },
-        { keyViewDistance = 'Viewing distance: Increase/(+shift)Deacrease' },
-        { keyViewDistance = '(+ctrl)Reset environment settings' },
-        { keyProjectileCameraQuit = 'Quit POV camera' },
-        { keyEffectsUp = 'Increase effects' },
-        { keyEffectsDown = 'Decrease effects' },
-    },
-    edit         = function(self, action)
-        self.editedAction = action
-        InputClear()
-    end,
-    draw         = function(self)
-        if self.pages[self.page] == nil then
-            DebugPrint(string.format("Unknown page: %s", self.page))
-            self.page = "home"
-            return
-        end
-        local content = self.pages[self.page]
-        UiFont("RobotoMono-Regular.ttf", 26)
-        UiColor(1, 1, 1, 0.5)
-
-        local w, h, maxWidth, maxLines, titleH
-        maxLines = 25
-        h        = maxLines * self.lineH + self.margin
-        maxWidth = 0
-        w        = UiWidth() - self.margin * 2
-        titleH   = 40
-
-        --title
-        UiPush()
-        UiAlign("center top")
-        UiTranslate(UiCenter(), UiHeight() - UiHeight() + self.margin)
-        UiText("ProBallistics " .. content.title)
-        UiPop()
-        UiTranslate(0, titleH)
-        UiPush()
-        UiTranslate(self.margin, UiHeight() - UiHeight() + self.margin)
-        UiAlign("left top")
-        UiColor(0.05, 0.05, 0.05, 0.25)
-        UiRoundedRect(w, h, math.floor(self.margin / 2), 1)
-        UiColor(0.2, 0.2, 0.2, 0.5)
-        UiRoundedRectOutline(w, h, math.floor(self.margin / 2), 5)
-        UiColor(0, 1, 0, 1)
-        UiRoundedRectOutline(w, h, math.floor(self.margin / 2), 1)
-        UiPop()
-
-        UiPush()
-
-        UiAlign("left top")
-        UiTextOutline(0, 1, 0, 1)
-        local actions = content.actions ~= nil and #content.actions > 0
-        local links = content.links ~= nil and #content.links > 0
-        local settings = content.settings ~= nil
-        --actions
-        if actions or links or settings then
-            UiPush()
-
-            UiTranslate(self.margin * 2, self.margin * 2)
-            local tW, i, text
-            i = 0
-            UiColor(0, 1, 0)
-            if actions then
-                for _, actionSet in ipairs(content.actions) do
-                    for action, description in pairs(actionSet) do
-                        if action == self.editedAction then
-                            UiColor(0, 1, 0)
-                            UiButtonImageBox("ui/common/box-outline-6.png", 6, 10)
-                            --UiButtonImageBox("ui/common/box-solid-6.png", 6, 6)
-                            text = "press key"
-                        else
-                            UiColor(0, 1, 0, .75)
-                            UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-                            text = string.upper(ModOptions:getKeyBind(action))
-                        end
-                        if UiTextButton(text, ModOptions.buttonWidth, ModOptions.buttonHeight) then
-                            self:edit(action)
-                            DebugPrint(action)
-                        end
-                        UiPush()
-                        UiTranslate(ModOptions.buttonWidth + self.margin, 5)
-                        tW = UiText(string.format("%-50s", description))
-                        UiPop()
-                        UiTranslate(0, self.lineH)
-                        if tW > maxWidth then
-                            maxWidth = tW
-                        end
-                        i = i + 1
-                        if i >= maxLines then
-                            UiPop()
-                            UiPush()
-                            UiTranslate(maxWidth + ModOptions.buttonWidth + self.margin * 4,
-                                UiMiddle() - (UiHeight() / 2) + self.margin * 2)
-                            maxWidth = 0
-                            i        = 0
-                        end
-                    end
-                end
-            end
-            if settings then
-                for name, options in pairs(content.settings) do
-                    UiColor(0, 1, 0, .75)
-                    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-                    ModOptions:button(name, options)
-                    UiPush()
-                    UiTranslate(ModOptions.buttonWidth + self.margin, 5)
-                    tW = UiText(string.format("%-50s", options.label or "?undefined?"))
-                    UiPop()
-                    UiTranslate(0, self.lineH)
-                    if tW > maxWidth then
-                        maxWidth = tW
-                    end
-                    i = i + 1
-                    if i >= maxLines then
-                        UiPop()
-                        UiPush()
-                        UiTranslate(maxWidth + ModOptions.buttonWidth + self.margin * 4,
-                            UiMiddle() - (UiHeight() / 2) + self.margin * 2)
-                        maxWidth = 0
-                        i        = 0
-                    end
-                end
-            end
-            if links then
-                for _, linkSet in ipairs(content.links) do
-                    for page, description in pairs(linkSet) do
-                        UiColor(0, 1, 0, .75)
-                        UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-                        if UiTextButton(description, ModOptions.buttonWidth, ModOptions.buttonHeight) then
-                            self.page = page
-                            DebugPrint(page)
-                            return
-                        end
-                        UiTranslate(0, self.lineH)
-                        i = i + 1
-                        if i >= maxLines then
-                            UiPop()
-                            UiPush()
-                            UiTranslate(maxWidth + ModOptions.buttonWidth + self.margin * 4,
-                                UiMiddle() - (UiHeight() / 2) + self.margin * 2)
-                            maxWidth = 0
-                            i        = 0
-                        end
-                    end
-                end
-            end
-            UiPop()
-        end
-        UiTranslate(UiCenter(), h + self.margin * 2)
-        UiAlign("center top")
-        if actions then
-            UiText(string.format("Excluded keys: %s.", table.concat(keys(self.specialKeys), ", ")))
-            UiTranslate(0, self.margin * 2)
-            UiText("Press 'rmb' to cancel binding.")
-        end
-        UiColor(0, 1, 0, .75)
-        UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-        UiTranslate(0, self.margin * 3)
-        if UiTextButton("Reset to defaults", ModOptions.buttonWidth * 2, ModOptions.buttonHeight) then
-            ModOptions:init(true)
-            DebugPrint("RESET TO DEFAULT")
-        end
-        UiPop()
-    end,
-}
-function draw()
+#version 2
+function client.draw()
     ModOptions:init()
     OptionHandler:draw()
     OptionHandler:process()
 end
+

```

---

# Migration Report: src\ammo\artillery.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\artillery.lua
+++ patched/src\ammo\artillery.lua
@@ -1,554 +1,3 @@
+#version 2
 local cannonOffset          = Vec(-5, -2, 0)
-munition150mmArtillery      = New(Shell, {
-    barrelOffset  = cannonOffset,
-    vox           = "150mmHE",
-    voxScale      = .5,
-    initialV      = 1.325,
-    type          = "canon2",
-    name          = "150mm HE",
-    KE            = 1000 + minKE,
-    proxyDistance = 0,
-    specialEvent  = -1,
-    caliber       = 0.15,
-    penetration   = { .75, .5 },
-    ricochet      = 15,
-    hitEvent      = nil,
-    recoil        = 0.03,
-    rounds        = 1,
-    burst         = 1,
-    tracer        = -1,
-    gunSpread     = 9,
-    delay         = 1,
-    trackable     = 1,
-    forceRender   = true,
-    effects       = {
-        explosion     = 2,
-        fire          = 1,
-        sparks        = {
-            n        = 100,
-            life     = 15,
-            light    = 125,
-            lightMax = 300,
-        },
-        shrapnel      = {
-            n      = 125,
-            spread = 180
-        },
-        subProjectile = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 50,
-                    n     = 150,
-                    shell = munitionShrapnelSmall
-                },
-                {
-                    min   = 50,
-                    n     = 100,
-                    shell = munitionShrapnelMedium
-                },
-                {
-                    min   = 25,
-                    n     = 50,
-                    shell = munitionShrapnelHeavy
-                },
-                {
-                    min   = 2,
-                    max   = 5,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 1,
-                --    max   = 2,
-                --    shell = EffectsFireballMedium
-                --},
-                --{
-                --    min   = 1,
-                --    max   = 3,
-                --    shell = EffectsFireballHeavy
-                --},
-                --{
-                --    min   = 1,
-                --    max   = 2,
-                --    shell = EffectsFireballHeavyLow
-                --},
-            }
-        }
-    },
-    effectsActive = {
-        smoke    = 1,
-        fire     = 1,
-        shrapnel = {
-            n      = 20,
-            spread = 180
-        },
-        sparks   = {
-            n        = 50,
-            life     = 10,
-            light    = 25,
-            lightMax = 75,
-        },
-    }
-})
-munition150mmArtilleryAP    = New(munition150mmArtillery, {
-    name          = "150mm AP HE",
-    KE            = 2000 + minKE,
-    penetration   = { 1.75, 1.5 },
-    effectsActive = {
-        smoke    = 1,
-        fire     = 1,
-        shrapnel = {
-            n      = 10,
-            spread = 180
-        },
-        sparks   = {
-            n        = 25,
-            life     = 10,
-            light    = 25,
-            lightMax = 75,
-        },
-    }
-})
-munition75mmArtillerySalvo  = New(Shell, {
-    barrelOffset  = cannonOffset,
-    voxScale      = .35,
-    vox           = "75mmHE",
-    initialV      = 1.25,
-    type          = "canon2",
-    name          = "75mm Salvo",
-    KE            = 1000 + minKE,
-    proxyDistance = 0,
-    specialEvent  = -1,
-    caliber       = 0.075,
-    penetration   = { 1.5, 1.25 },
-    ricochet      = 15,
-    hitEvent      = nil,
-    recoil        = 0.03,
-    rounds        = 1,
-    burst         = 1,
-    tracer        = -1,
-    gunSpread     = 6.5,
-    delay         = 0.5,
-    forceRender   = false,
-    trackable     = 1,
-    effects       = {
-        explosion     = 1.5,
-        fire          = 1,
-        sparks        = {
-            n        = 250,
-            life     = 15,
-            light    = 75,
-            lightMax = 250,
-        },
-        shrapnel      = {
-            n      = 75,
-            spread = 180
-        },
-        subProjectile = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 10,
-                    n     = 25,
-                    shell = munitionShrapnelSmall
-                },
-                {
-                    min   = 10,
-                    n     = 25,
-                    shell = munitionShrapnelMedium
-                },
-                {
-                    min   = 5,
-                    n     = 15,
-                    shell = munitionShrapnelHeavy
-                },
-                {
-                    min   = 1,
-                    max   = 2,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 0,
-                --    max   = 2,
-                --    shell = EffectsFireballMedium
-                --},
-                --{
-                --    min   = 0,
-                --    max   = 2,
-                --    shell = EffectsFireballHeavy
-                --},
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballHeavyLow
-                --},
-            }
-        }
-    },
-    effectsActive = {
-        smoke  = 1,
-        fire   = 1,
-        sparks = {
-            n        = 75,
-            life     = 10,
-            light    = 25,
-            lightMax = 75,
-        },
-    }
-})
-munition75mmArtillerySalvoA = New(munition75mmArtillerySalvo, {
-    fixedElevation = 20,
-    name           = "Test"
-})
 
-munition45mmHE              = New(Shell, {
-    barrelOffset  = cannonOffset,
-    initialV      = .9,
-    type          = "canon",
-    streamFire    = false,
-    vox           = "30mmHE",
-    voxScale      = .35,
-    name          = "45mm HE",
-    KE            = 250 + minKE,
-    proxyDistance = 0,
-    specialEvent  = -1,
-    caliber       = .03,
-    penetration   = { 1.35, 1.25 },
-    ricochet      = 45,
-    hitEvent      = nil,
-    recoil        = .01,
-    rounds        = 1,
-    burst         = 1,
-    tracer        = -1,
-    tracerColor   = { 1, .2, 0 },
-    gunSpread     = 20,
-    delay         = .125,
-    forceRender   = true,
-    effects       = {
-        explosion     = 0.5,
-        --explosionDebris = 0.05,
-        fire          = 1,
-        --smoke           = 1,
-        shrapnel      = {
-            n      = 75,
-            spread = 180
-        },
-        sparks        = {
-            n        = 75,
-            life     = 10,
-            light    = 50,
-            lightMax = 100,
-        },
-        subProjectile = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 0,
-                    n     = 1,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 0.5,
-                    max   = 1.75,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballMedium
-                --},
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballHeavyLow
-                --},
-            }
-        }
-    },
-    effectsActive = {
-        smoke  = 1,
-        fire   = 0,
-        sparks = {
-            n        = 20,
-            life     = 15,
-            light    = 10,
-            lightMax = 25,
-        },
-    }
-})
-
-munition30mmDU              = New(munition45mmHE, {}, {
-    initialV      = 0.95,
-    type          = 2,
-    streamFire    = true,
-    vox           = "30mm",
-    name          = "30mm DU",
-    KE            = 350 + minKE,
-    delay         = shotDelay * 2,
-    volMpl        = 5,
-    recoil        = .001,
-    ricochet      = 15,
-    tracer        = 2,
-    gunSpread     = 10,
-    effects       = {
-        fire     = 0,
-        shrapnel = {
-            n      = 20,
-            spread = 180
-        },
-        sparks   = {
-            n        = 25,
-            life     = 10,
-            light    = 25,
-            lightMax = 50,
-        },
-    },
-    effectsActive = {
-        fire   = 1,
-        sparks = {
-            n        = 15,
-            life     = 15,
-            light    = 5,
-            lightMax = 10,
-        },
-    }
-})
-munition40mmAP              = New(munition45mmHE, {}, {
-    initialV      = 1.5,
-    vox           = "30mmHE",
-    name          = "40mm AP",
-    KE            = 1500 + minKE,
-    tracer        = -1,
-    delay         = .1,
-    gunSpread     = 8,
-    effects       = {
-        smoke    = 2,
-        fire     = 1,
-        shrapnel = {
-            n      = 20,
-            spread = 180
-        },
-        sparks   = {
-            n        = 25,
-            life     = 10,
-            light    = 25,
-            lightMax = 50,
-        },
-    },
-    effectsActive = {
-        smoke    = 1,
-        fire     = 0,
-        shrapnel = {
-            n      = 5,
-            spread = 180
-        },
-        sparks   = {
-            n        = 15,
-            life     = 15,
-            light    = 5,
-            lightMax = 10,
-        },
-    }
-})
-munition30mmAB              = New(Shell, {}, {
-    barrelOffset  = cannonOffset,
-    initialV      = 0.85,
-    vox           = "30mmAB",
-    voxScale      = .35,
-    type          = "canon",
-    streamFire    = false,
-    name          = "45mm Frag Air-Burst",
-    KE            = 350 + minKE,
-    proxyDistance = 15,
-    proxyEvent    = function(self, dt, distance, ballistics)
-        self.hit = true
-        --ProExplosionWrapper(
-        --    self.pos,
-        --    0.2 + math.random(0, 250) * 0.001
-        --)
-        ExplosionSparks(self.pos, 150, 5, self.v)
-        SoundManager:explosion(.6, self.pos)
-        Smoke(self.pos, 3, 5, 5, VecNormalize(self.v))
-        ballistics:projectileEffects(
-            self,
-            self.pos,
-            self.effects,
-            {
-                material = materialAir,
-                materialName = "air",
-                speed = 2,
-                resolution = .035,
-            }
-        )
-        Shrapnel(self, 15, 25, 10)
-        Shrapnel(self, 15, 25, 30)
-
-        return false
-    end,
-    specialEvent  = -1,
-    caliber       = 0.03,
-    penetration   = defaultPenetration,
-    ricochet      = 90,
-    hitEvent      = nil,
-    recoil        = 0.00075,
-    rounds        = 1,
-    burst         = 1,
-    tracer        = -1,
-    gunSpread     = 20,
-    delay         = .125,
-    forceRender   = true,
-    effects       = {
-        fire            = 1,
-        --smoke     = 2,
-        smokeRing       = .2,
-        sparks          = {
-            n        = 50,
-            life     = 10,
-            light    = 50,
-            lightMax = 125,
-        },
-    },
-    effectsActive = {
-        fire   = 1,
-        sparks = {
-            n        = 50,
-            life     = 15,
-            light    = 25,
-            lightMax = 50,
-        },
-    }
-})
-munition30mmIncAB           = New(Shell, {
-    barrelOffset  = cannonOffset,
-    initialV      = 0.85,
-    vox           = "30mmAB",
-    voxScale      = .35,
-    type          = "canon",
-    streamFire    = false,
-
-    name          = "45mm Incendiary Air-Burst",
-    KE            = 350 + minKE,
-    proxyDistance = 10,
-    proxyEvent    = function(self, dt, distance, ballistics)
-        self.hit = true
-        ExplosionSparks(self.pos, 200, 10, self.v)
-        SoundManager:explosion(.5, self.pos)
-        ballistics:projectileEffects(
-            self,
-            self.pos,
-            self.effects,
-            {
-                material = materialAir,
-                materialName = "air",
-                speed = 1.25,
-            }
-        )
-        return false
-    end,
-    specialEvent  = -1,
-    caliber       = 0.03,
-    penetration   = defaultPenetration,
-    ricochet      = 90,
-    hitEvent      = nil,
-    recoil        = 0.00075,
-    rounds        = 1,
-    burst         = 1,
-    tracer        = -1,
-    gunSpread     = 25,
-    delay         = .4,
-    forceRender   = true,
-    effects       = {
-        fire          = 1,
-        smoke         = 2,
-        smokeRing     = .2,
-        shrapnel      = {
-            n      = 20,
-            spread = 60
-        },
-        sparks        = {
-            n        = 100,
-            life     = 10,
-            light    = 50,
-            lightMax = 125,
-        },
-        incendiary    = {
-            n = 10,
-            spread = 80,
-        },
-        subProjectile = {
-            shellSets = {
-                {
-                    min    = 5,
-                    n      = 15,
-                    spread = 25,
-                    shell  = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min    = 10,
-                    n      = 25,
-                    spread = 35,
-                    shell  = munitionShrapnelMediumIncendiary
-                },
-            }
-        }
-    },
-    effectsActive = {
-        fire   = 1,
-        sparks = {
-            n        = 50,
-            life     = 15,
-            light    = 25,
-            lightMax = 50,
-        },
-    }
-})
-munition30mmInc             = New(munition30mmIncAB, {
-        initialV      = 0.85,
-        vox           = "30mmAB",
-        voxScale      = .35,
-        type          = "canon",
-        streamFire    = false,
-        penetration   = { 1.5, 1.25 },
-        ricochet      = 45,
-        name          = "45mm Incendiary",
-        KE            = 250 + minKE,
-        proxyDistance = 0,
-        gunSpread     = 10,
-    },
-    {
-        proxyEvent = nil,
-        effects    = {
-            fire          = 1,
-            smoke         = 2,
-            smokeRing     = nil,
-            shrapnel      = {
-                n      = 20,
-                spread = 120
-            },
-            sparks        = {
-                n        = 100,
-                life     = 10,
-                light    = 50,
-                lightMax = 125,
-            },
-            incendiary    = {
-                n = 100,
-            },
-            subProjectile = {
-                spread = 180,
-                shellSets = {
-                    {
-                        min   = 5,
-                        n     = 15,
-                        shell = munitionShrapnelHeavyIncendiary
-                    },
-                    {
-                        min   = 10,
-                        n     = 25,
-                        shell = munitionShrapnelMediumIncendiary
-                    },
-                }
-            }
-        },
-    }
-)

```

---

# Migration Report: src\ammo\base.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\base.lua
+++ patched/src\ammo\base.lua
@@ -1,26 +1,4 @@
-tracersEnabled          = true
-gravity                 = Vec(0, -9.2, 0)
-drag                    = 0.992
-velocityMpl             = 400
-shotDelay               = 0.01
-recoilMpl               = 0.02
-minKE                   = 500
-rocketThrustMpl         = 8
-ammoMaxLife             = 60
-defaultPenetration      = { 1, .35, .75 }
-
-SpecialEventDiffCompare = function(projectile, diff)
-    diff = diff or 1
-    if projectile.specialEvent < projectile.data.previousEvent + diff then
-        return false
-    end
-    projectile.data.previousEvent = projectile.specialEvent
-    return true
-end
-SpecialEventDiff        = function(projectile)
-    return projectile.specialEvent - projectile.data.previousEvent
-end
-
+#version 2
 function proxyAirHit(self, dt, preDistance, ballistics)
     self.hit = true
     ballistics:projectileEffects(
@@ -59,4 +37,3 @@
     return false;
 end
 
-randomSpawnDir = { rSign(), rSign() }

```

---

# Migration Report: src\ammo\bombs.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\bombs.lua
+++ patched/src\ammo\bombs.lua
@@ -1,354 +1 @@
-munitionBomb100lb = New(Shell, {
-    name          = "100lb Bomb",
-    vox           = "100lb",
-    explosive     = true,
-    spin          = 1,
-    weight        = 5,
-    voxScale      = .75,
-    caliber       = 0.15,
-    initialV      = 0.05,
-    KE            = 1100 + minKE,
-    delay         = 1,
-    recoil        = 0,
-    ricochet      = 15,
-    maxLifetime   = 25,
-    tracer        = 0,
-    barrelOffset  = Vec(1, 0, 0),
-    --tracker        = {
-    --    drawTrace  = true,
-    --    leaveMarks = 5,
-    --},
-    length        = .75,
-    effects       = {
-        explosion       = 3,
-        explosionDebris = 1.25,
-        fire            = 1,
-        fireball        = 3,
-        sparks          = {
-            n        = 350,
-            life     = 15,
-            light    = 100,
-            lightMax = 300,
-        },
-        shrapnel        = {
-            n      = 125,
-            spread = 180
-        },
-        subProjectile   = {
-            spread    = 180,
-            shellSets = {
-                {
-                    n     = 25,
-                    shell = munitionShrapnelMedium,
-                },
-                {
-                    n     = 25,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 2,
-                    n     = 3,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 2,
-                    max   = 4,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 1,
-                --    max   = 2,
-                --    shell = EffectsFireballMedium
-                --},
-                {
-                    min   = 0,
-                    max   = .25,
-                    shell = EffectsFireballHeavy
-                },
-                {
-                    min   = 0,
-                    max   = .45,
-                    shell = EffectsFireballHeavyLow
-                },
-            }
-        }
-    },
-    effectsActive = {
-        smoke         = 1,
-        fire          = 0,
-        fireball      = 1,
-        sparks        = {
-            n        = 40,
-            life     = 5,
-            light    = 100,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 5,
-            spread = 200
-        },
-        subProjectile = nil
-    }
-})
-munitionBomb200lb = New(munitionBomb100lb, {
-    name          = "200lb Bomb",
-    vox           = "100lb",
-    voxScale      = 1,
-    spin          = .75,
-    caliber       = 0.25,
-    KE            = 1500 + minKE,
-    ricochet      = 10,
-    weight        = 6,
-    delay         = 1.25,
-    effects       = {
-        explosion       = 5,
-        explosionDebris = 1.25,
-        fire            = 2,
-        smoke           = 2,
-        fireball        = 5,
-        sparks          = {
-            n        = 350,
-            life     = 15,
-            light    = 100,
-            lightMax = 300,
-        },
-        shrapnel        = {
-            n      = 150,
-            spread = 180
-        },
-        subProjectile   = {
-            spread    = 180,
-            shellSets = {
-                {
-                    n     = 50,
-                    shell = munitionShrapnelMedium,
-                },
-                {
-                    n     = 25,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 5,
-                    n     = 8,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 4,
-                    max   = 6,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 0,
-                --    max   = 2,
-                --    shell = EffectsFireballMedium
-                --},
-                {
-                    min   = 0,
-                    max   = 1.5,
-                    shell = EffectsFireballHeavy
-                },
-                {
-                    min   = 0,
-                    max   = 1.5,
-                    shell = EffectsFireballHeavyLow
-                },
-            }
-        }
-    },
-    effectsActive = {
-        smoke         = 1,
-        fire          = 1,
-        fireball      = 1,
-        sparks        = {
-            n        = 45,
-            life     = 5,
-            light    = 100,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 8,
-            spread = 200
-        },
-        subProjectile = nil
-    }
-})
-munitionBomb500lb = New(munitionBomb100lb, {
-    name          = "500lb Bomb",
-    vox           = "500lb",
-    voxScale      = 1,
-    spin          = .5,
-    caliber       = 0.35,
-    KE            = 1750 + minKE,
-    ricochet      = 10,
-    weight        = 8,
-    delay         = 2.5,
-    effects       = {
-        explosion       = 7.5,
-        explosionDebris = 1.5,
-        smoke           = 2,
-        fire            = 3,
-        fireball        = 8,
-        sparks          = {
-            n        = 350,
-            life     = 15,
-            light    = 250,
-            lightMax = 500,
-        },
-        shrapnel        = {
-            n      = 175,
-            spread = 180
-        },
-        subProjectile   = {
-            spread    = 180,
-            shellSets = {
-                {
-                    n     = 75,
-                    shell = munitionShrapnelMedium,
-                },
-                {
-                    n     = 35,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 6,
-                    n     = 10,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 4,
-                    max   = 8,
-                    shell = EffectsFireballFastShort
-                },
-                {
-                    min   = 1,
-                    max   = 2.5,
-                    shell = EffectsFireballMedium
-                },
-                {
-                    min   = 1,
-                    max   = 3,
-                    shell = EffectsFireballHeavy
-                },
-                {
-                    min   = .5,
-                    max   = 2,
-                    shell = EffectsFireballHeavyLow
-                },
-            }
-        }
-    },
-    effectsActive = {
-        smoke         = 1,
-        fire          = 1,
-        fireball      = 1,
-        sparks        = {
-            n        = 45,
-            life     = 5,
-            light    = 150,
-            lightMax = 300,
-        },
-        shrapnel      = {
-            n      = 15,
-            spread = 200
-        },
-        subProjectile = nil
-    }
-})
-munitionBomblet5lb = New(munitionBomb100lb, {
-    name          = "5lb Bomblet",
-    vox           = "10lb",
-    voxScale      = .5,
-    spin          = 2,
-    caliber       = 0.1,
-    KE            = 1000 + minKE,
-    ricochet      = 10,
-    burst         = 1,
-    rounds        = 1,
-    weight        = 3.5,
-    gunSpread     = 80,
-    delay         = .1,
-    effects       = {
-        explosion       = 1.25,
-        explosionDebris = 1.25,
-        fire            = 2,
-        fireball        = 3,
-        sparks          = {
-            n        = 150,
-            life     = 15,
-            light    = 100,
-            lightMax = 300,
-        },
-        shrapnel        = {
-            n      = 75,
-            spread = 180
-        },
-        subProjectile   = {
-            spread    = 180,
-            shellSets = {
-                {
-                    n     = 15,
-                    shell = munitionShrapnelMedium,
-                },
-                {
-                    n     = 5,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = .5,
-                    n     = 3,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = .5,
-                    max   = 1.25,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballMedium
-                --},
-                {
-                    min   = 0,
-                    max   = .05,
-                    shell = EffectsFireballHeavy
-                },
-                {
-                    min   = 0,
-                    max   = .05,
-                    shell = EffectsFireballHeavyLow
-                },
-            }
-        }
-    },
-    effectsActive = {
-        smoke         = 1,
-        fire          = 0,
-        fireball      = 0,
-        sparks        = {
-            n        = 25,
-            life     = 5,
-            light    = 100,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 3,
-            spread = 200
-        },
-        subProjectile = nil
-    }
-})
-munitionBomblet5lbX10 = New(munitionBomblet5lb, {
-    name      = "5lb BombletX10",
-    initialV  = 0.05,
-    gunSpread = 1080,
-    rounds    = 2,
-    burst     = 5,
-    delay     = 1,
-})
-munitionBomblet5lbX2 = New(munitionBomblet5lb, {
-    name      = "5lb BombletX2",
-    gunSpread = 100,
-    rounds    = 2,
-    delay     = .2,
-})
+#version 2

```

---

# Migration Report: src\ammo\debris-shrapnel.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\debris-shrapnel.lua
+++ patched/src\ammo\debris-shrapnel.lua
@@ -1,405 +1 @@
-munitionDebrisMetal              = New(
-    Shell,
-    {
-        type          = 'debris',
-        name          = 'metal',
-        KE            = 250,
-        initialV      = .5,
-        minKE         = 10,
-        caliber       = 0.01,
-        tracer        = 0,
-        specialEvent  = 0,
-        maxLifetime   = 7.5,
-        data          = {
-            noPenetration = true,
-            hitKEMpl      = 1,
-            noDust        = true,
-            previousEvent = -1,
-            keDropRate    = .85,
-            vDropRate     = .95,
-        },
-        debug         = { 1, 1, 1, 1 },
-        penetration   = {
-            rMed  = 1.5,
-            rHard = 1.75
-        },
-        effects       = {
-            noSound = true,
-            smoke   = 0,
-            fire    = 0,
-            sparks  = {
-                n     = 5,
-                life  = 3,
-                light = 0,
-            },
-        },
-        effectsActive = {
-            noSound = true,
-            smoke   = 0,
-            fire    = 0,
-            sparks  = {
-                n     = 10,
-                life  = 3,
-                light = 0,
-            },
-        }
-    },
-    {
-        event = function(projectile, dt)
-            projectile.KE = projectile.KE * (1 - (1 - projectile.data.keDropRate) * legacyTimeCorrection)
-            --projectile.v  = VecScale(projectile.v, 1 - (1 - projectile.data.vDropRate) * legacyTimeCorrection)
-
-            local sKE     = math.sqrt(projectile.KE)
-            if projectile.color ~= nil then
-                local r, g, b = _unpackColor(projectile.color)
-                PointLight(projectile.pos, r, g, b, sKE * .2)
-            else
-                PointLight(projectile.pos, 0.72, 0.27, 0.05, sKE * .2)
-            end
-            if not ProBallistics:timeScaleRand() then
-                local dir = VecNormalize(projectile.v)
-
-                if projectile.effectsActive.smoke > 0 and projectile.KE > projectile.minKE * .5
-                    and projectile.totalDistance < highRand(17, 25) then
-                    if not projectile.data.smokeColor ~= nil then
-                        projectile.data.smokeColor = (lowRand(25, 50) + highRand(0, 25)) * .01
-                    end
-
-                    local cPerM = 2
-                    local c, sPos, sV
-
-                    c           = math.max(1, projectile.distance * cPerM)
-                    sPos        = projectile.pos
-                    sV          = VecScale(dir, 1 / cPerM)
-                    for i = 1, c do
-                        _Smoke(
-                            sPos,
-                            5,
-                            10,
-                            projectile.effectsActive.smoke,
-                            sKE * .15 + .35,
-                            lowRand(15, 50) * .1,
-                            dir,
-                            projectile.data.smokeColor
-                        )
-                        sPos = VecSub(sPos, sV)
-                    end
-                end
-            end
-            -- TODO: Double-Check for sparks artifacts
-            --_Sparks(
-            --    projectile.pos,
-            --    math.random(0, 3),
-            --    5,
-            --    defaultSparkTile, --DEPRECATED
-            --    lowRand(15, 50) * .1,
-            --    1
-            --)
-            return projectile.KE > 1
-        end
-    }
-)
-
-munitionDebrisExplosion          = New(munitionDebrisMetal, {
-    maxLifetime   = 1,
-    effects       = {
-        smoke  = 0,
-        fire   = 0,
-        sparks = {
-            n     = 5,
-            life  = 3,
-            light = 0,
-        },
-    },
-    debug         = { 0, 1, 1, 1 },
-    effectsActive = {
-        smoke  = 2,
-        fire   = 1,
-        sparks = {
-            n     = 15,
-            life  = 3,
-            light = 0,
-        },
-    }
-})
-
-munitionShrapnel                 = New(Shell, {
-    maxLifetime       = 1.5,
-    name              = "shrapnel",
-    initialV          = 1,
-    tracerMinDistance = 1,
-    constructor       = function(self)
-        self.initialV = self.initialV * math.random(75, 125) * .01
-        self.tracerMinDistance = self.tracerMinDistance * math.random(75, 125) * .01
-    end,
-})
-
-munitionShrapnelMedium           = New(munitionShrapnel, {
-    --vox           = "shrapnelMedium",
-    --voxScale       = .2,
-    initialV       = 1.3,
-    type           = 1,
-    name           = 4,
-    KE             = 600 + minKE,
-    specialEvent   = -1,
-    caliber        = 0.01,
-    penetration    = defaultPenetration,
-    ricochet       = 120,
-    hitEvent       = nil,
-    tracerWidthMpl = 2.5,
-    effects        = {
-        sparks = {
-            n        = 5,
-            life     = 10,
-            light    = 10,
-            lightMax = 25,
-
-        }
-    },
-    effectsActive  = {
-        fire   = 0,
-        sparks = {
-            n        = 10,
-            life     = 5,
-            light    = 15,
-            lightMax = 40,
-        }
-    }
-})
-munitionShrapnelHeavy            = New(munitionShrapnel, {
-    --vox            = "shrapnelHeavy",
-    --voxScale       = .2,
-    initialV       = 1.1,
-    type           = 1,
-    name           = 4,
-    KE             = 1500 + minKE,
-    specialEvent   = -1,
-    caliber        = 0.02,
-    penetration    = { 2.5, 4 },
-    ricochet       = 10,
-    hitEvent       = nil,
-    tracer         = -1,
-    tracerStrength = 0.25,
-    tracerWidthMpl = 2.5,
-    debug          = { 0, 0, 1, 1 },
-    effects        = {
-        shrapnel = {
-            n      = 2,
-            spread = 180
-        },
-        sparks   = {
-            n        = 10,
-            life     = 10,
-            light    = 10,
-            lightMax = 25,
-        },
-    },
-    effectsActive  = {
-        fire   = 0,
-        sparks = {
-            n        = 15,
-            life     = 10,
-            light    = 20,
-            lightMax = 50,
-        },
-    },
-}, {
-    constructor = function(self)
-        self.initialV       = math.random(75, 110) * .01
-        self.KE             = math.random(1000, 1750) + minKE
-        self.tracerWidthMpl = self.tracerWidthMpl * math.random(250, 1000) * .001
-        self.tracer         = 1
-    end,
-})
-
-munitionShrapnelAP               = New(munitionShrapnelHeavy, {
-    --vox           = "shrapnelMedium",
-    KE             = 2600 + minKE,
-    debug          = { 1, 0, 1, 1 },
-    tracerWidthMpl = 4,
-    effects        = {
-        fire     = 1,
-        shrapnel = {
-            min    = 3,
-            n      = 5,
-            spread = 60
-        },
-        sparks   = {
-            n        = 10,
-            life     = 5,
-            light    = 10,
-            lightMax = 30,
-        },
-    },
-    effectsActive  = {
-        shrapnel = {
-            n      = 2,
-            spread = 180
-        },
-        sparks   = {
-            n        = 5,
-            life     = 2.5,
-            light    = 10,
-            lightMax = 25,
-        },
-    },
-}, {
-    constructor = function(self)
-        self.initialV       = math.random(75, 110) * .01
-        self.KE             = math.random(2000, 3000) + minKE
-        self.tracerWidthMpl = self.tracerWidthMpl * math.random(250, 1000) * .001
-        self.tracer         = 1
-    end,
-})
-
-munitionShrapnelMediumIncendiary = New(munitionShrapnelMedium, {
-    tracer        = -1,
-    initialV      = .75,
-    maxLifetime   = 1,
-    ricochet      = 45,
-    penetration   = { .75, .25, .5 },
-    effects       = {
-        fire   = 1,
-        sparks = {
-            n        = 12,
-            life     = 5,
-            light    = 15,
-            lightMax = 50,
-        }
-    },
-    effectsActive = {
-        fire   = 1,
-        sparks = {
-            n        = 7,
-            life     = 2.5,
-            light    = 10,
-            lightMax = 40,
-        }
-    }
-})
-munitionShrapnelHeavyIncendiary  = New(munitionShrapnelMediumIncendiary, {
-        specialEvent  = 0,
-        maxLifetime   = 5,
-        initialV      = .125,
-        KE            = 1600 + minKE,
-        vRate         = .85,
-        ricochet      = 30,
-        penetration   = { .25, .1, .25 },
-        data          = {
-            keDropRate = .98,
-            vDropRate = .995,
-        },
-        effects       = {
-            fire    = 1,
-            noSound = 1,
-            smoke   = 1,
-            sparks  = {
-                n        = 5,
-                life     = 5,
-                light    = 2,
-                lightMax = 20,
-            }
-        },
-        effectsActive = {
-            fire    = 1,
-            noSound = 1,
-            smoke   = 1,
-            sparks  = {
-                n        = 25,
-                life     = 5,
-                light    = 10,
-                lightMax = 40,
-            }
-        },
-    },
-    {
-        constructor = function(self)
-            self.KE          = self.KE * lowRand(750, 1500, 3) * .001
-            self.initialV    = lowRand(100, 350) * .001
-            self.maxLifetime = self.maxLifetime * lowRand(100, 400) * .01
-        end,
-        --hitEvent    = function(self, hitMaterial, hitNormal, debrisCount)
-        --    Incendiary(self, math.random(3, 5), 60, hitNormal)
-        --end,
-        event       = function(self, dt)
-            self.KE   = self.KE * (1 - (1 - self.data.keDropRate) * legacyTimeCorrection)
-            self.v    = VecScale(self.v, 1 - (1 - self.data.vDropRate) * legacyTimeCorrection)
-            local sKE = math.sqrt(self.KE)
-            if self.color ~= nil then
-                local r, g, b = _unpackColor(self.color)
-                PointLight(self.pos, r, g, b, sKE)
-            else
-                PointLight(self.pos, 0.72, 0.27, 0.05, sKE)
-            end
-
-            if not ProBallistics:timeScaleRand() then
-                local dir = VecNormalize(self.v)
-
-                if (self.effectsActive.smoke or 0) > 0 and self.KE > self.minKE * .5
-                    and self.totalDistance < 50 then
-                    if not self.data.smokeColor ~= nil then
-                        self.data.smokeColor = (highRand(25, 50) + lowRand(0, 25)) * .01
-                    end
-
-                    local cPerM = 2.5
-                    local c, sPos, sV
-
-                    c           = math.max(1, self.distance * cPerM)
-                    sPos        = self.pos
-                    sV          = VecScale(dir, 1 / cPerM)
-                    for i = 1, c do
-                        _Smoke(
-                            sPos,
-                            5,
-                            10,
-                            self.effectsActive.smoke,
-                            sKE * .01 + .01,
-                            lowRand(15, 50) * .1,
-                            dir,
-                            self.data.smokeColor
-                        )
-                        sPos = VecSub(sPos, sV)
-                    end
-                end
-            end
-            -- TODO: Double-Check for sparks artifacts
-            _Sparks(
-                self.pos,
-                math.random(0, 3),
-                5,
-                lowRand(15, 50) * .1,
-                nil,
-                nil,
-                dir
-            )
-            return self.KE > 1
-        end
-    })
-munitionShrapnelSmall            = New(munitionShrapnel, {
-    initialV      = 1.1 * 1.5,
-    type          = 1,
-    name          = 4,
-    KE            = 400 + minKE,
-    specialEvent  = -1,
-    caliber       = 0.01,
-    penetration   = defaultPenetration,
-    ricochet      = 130 or 60,
-    hitEvent      = nil,
-    effects       = {
-        sparks = {
-            n        = 2,
-            life     = 8,
-            light    = 2,
-            lightMax = 10,
-        }
-    },
-    effectsActive = {
-        fire   = 0,
-        sparks = {
-            n        = 3,
-            life     = 5,
-            light    = 2.5,
-            lightMax = 15,
-        }
-    }
-})
+#version 2

```

---

# Migration Report: src\ammo\hand-held.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\hand-held.lua
+++ patched/src\ammo\hand-held.lua
@@ -1,660 +1 @@
-munition5_56mmFMJ           = New(
-    Shell,
-    {
-        vox           = "fmj",
-        casing        = "shell1x3",
-        type          = "rifle1",
-        name          = '5.56mm FMJ',
-        burst         = 1,
-        rounds        = 1,
-        recoil        = 0.35,
-        recoilTimer   = shotDelay * 11,
-        gunSpread     = 8,
-        delay         = shotDelay * 9,
-        KE            = 450,
-        initialV      = 0.9,
-        minKE         = 10,
-        caliber       = 0.02,
-        tracer        = 0,
-        ricochet      = 145,
-        penetration   = defaultPenetration,
-        streamFire    = false,
-        data          = {
-            noPenetration = false,
-            hitKEMpl      = 1,
-            noDust        = false,
-        },
-        effects       = {
-            shrapnel = {
-                n      = 1,
-                spread = 180
-            },
-            sparks   = {
-                n        = 5,
-                life     = 5,
-                light    = .5,
-                lightMax = 2,
-            },
-        },
-        effectsActive = {
-            sparks = {
-                n        = 10,
-                life     = 5,
-                light    = .5,
-                lightMax = 3,
-            },
-        },
-    }
-)
-munition5_56mmFMJT          = New(munition5_56mmFMJ, {
-    name           = '5.56mm FMJ Tracer',
-    tracer         = 2,
-    tracerStrength = .5,
-    effects        = {
-        shrapnel = {
-            n      = 1,
-            spread = 180
-        },
-        sparks   = {
-            n        = 10,
-            life     = 5,
-            light    = .75,
-            lightMax = 3,
-        },
-    },
-    effectsActive  = {
-        sparks = {
-            n        = 15,
-            life     = 5,
-            light    = .75,
-            lightMax = 4,
-        },
-    },
-})
-munition5_56mmAP            = New(munition5_56mmFMJ, {
-    name        = '5.56mm AP',
-    vox         = "ap",
-    KE          = 750,
-    initialV    = 0.95,
-    ricochet    = 80,
-    penetration = { 1.1, 1.1, .75 },
-})
-
-params_munition5_56mm_EPR   = {
-    type        = "sniper",
-    recoilTimer = shotDelay * 12,
-    gunSpread   = 2,
-    delay       = shotDelay * 15,
-    temp        = 8,
-}
-munition5_56mmFMJ_EPR       = New(munition5_56mmFMJ, params_munition5_56mm_EPR)
-munition5_56mmFMJT_EPR      = New(munition5_56mmFMJT, params_munition5_56mm_EPR)
-munition5_56mmAP_EPR        = New(munition5_56mmAP, params_munition5_56mm_EPR)
-munition5_56mmFMJ_EPR.name  = munition5_56mmFMJ_EPR.name .. " EPR"
-munition5_56mmFMJT_EPR.name = munition5_56mmFMJT_EPR.name .. " EPR"
-munition5_56mmAP_EPR.name   = munition5_56mmAP_EPR.name .. " EPR"
-
-params_munition5_56mm_CTR   = {
-    recoilTimer = shotDelay * 9,
-    gunSpread   = 10,
-    delay       = shotDelay * 5,
-    recoil      = .4,
-    type        = "smg",
-}
-munition5_56mmFMJ_CTR       = New(munition5_56mmFMJ, params_munition5_56mm_CTR)
-munition5_56mmFMJT_CTR      = New(munition5_56mmFMJT, params_munition5_56mm_CTR)
-munition5_56mmAP_CTR        = New(munition5_56mmAP, params_munition5_56mm_CTR)
-munition5_56mmFMJ_CTR.name  = munition5_56mmFMJ_CTR.name .. " CTR"
-munition5_56mmFMJT_CTR.name = munition5_56mmFMJT_CTR.name .. " CTR"
-munition5_56mmAP_CTR.name   = munition5_56mmAP_CTR.name .. " CTR"
-
-
-params_munition9mm = {
-    recoilTimer = shotDelay * 12,
-    gunSpread   = 10,
-    delay       = shotDelay * 10,
-    recoil      = .3,
-    caliber     = 0.03,
-    type        = "pistol",
-    temp        = 15,
-
-}
-munition9mmFMJ     = New(munition5_56mmFMJ, New(params_munition9mm, {
-    name = "9mm FMJ",
-}))
-munition9mmHP      = New(munition5_56mmFMJ, New(params_munition9mm, {
-    name        = "9mm HP",
-    KE          = 400,
-    penetration = { 1, .2, .75 },
-    ricochet    = 35,
-
-}))
-munition9mmJHP     = New(munition5_56mmFMJ, New(params_munition9mm, {
-    name        = "9mm JHP",
-    KE          = 550,
-    penetration = { 1, .2, .75 },
-    ricochet    = 15,
-}))
-munition9mmAP      = New(munition5_56mmAP, New(params_munition9mm, {
-    name = "9mm AP",
-}))
-
-
-params_munition7_62mm   = {
-    recoilTimer = shotDelay * 10,
-    gunSpread   = 7,
-    delay       = shotDelay * 8.5,
-    name        = "7.62mm",
-    caliber     = 0.0225,
-    KE          = 750,
-    type        = "lmg",
-    temp        = 6.5,
-}
-munition7_62mmFMJ       = New(munition5_56mmFMJ, params_munition7_62mm)
-munition7_62mmFMJT      = New(munition5_56mmFMJT, params_munition7_62mm)
-munition7_62mmAP        = New(munition5_56mmAP, params_munition7_62mm)
-munition7_62mmFMJ.name  = munition7_62mmFMJ.name .. " FMJ"
-munition7_62mmFMJT.name = munition7_62mmFMJT.name .. " FMJ Tracer"
-munition7_62mmAP.name   = munition7_62mmAP.name .. " AP"
-munition7_62mmAP.KE     = 1250
-
-munition50BMG           = New(munition12mmAP,
-    {
-        vox           = "bmg",
-        casing        = "shell1x4",
-        type          = "sniper_bmg",
-        name          = '.50 BMG',
-        streamFire    = false,
-        initialV      = 1.1,
-        delay         = .25,
-        recoil        = 0.5,
-        recoilTimer   = shotDelay * 10,
-        gunSpread     = 1,
-        ricochet      = 10,
-        tracer        = -1,
-        temp          = 20,
-        KE            = 500 + minKE,
-        penetration   = { 2, 3 },
-        effects       = {
-            shrapnel = {
-                n      = 2,
-                spread = 180
-            },
-            sparks   = {
-                n        = 15,
-                life     = 12,
-                light    = 4,
-                lightMax = 10,
-            },
-        },
-        effectsActive = {
-            shrapnel = {
-                n      = 1,
-                spread = 180
-            },
-            sparks   = {
-                n        = 7,
-                life     = 10,
-                light    = 3,
-                lightMax = 7,
-            },
-        }
-    }
-)
-munition50BMG_AP        = New(munition50BMG,
-    {
-        vox           = "bmgW",
-        name          = '.50 BMG AP',
-        ricochet      = 6,
-        KE            = 1500 + minKE,
-        penetration   = { 2.5, 4 },
-        effects       = {
-            shrapnel = {
-                n      = 5,
-                spread = 180
-            },
-            sparks   = {
-                n        = 25,
-                life     = 10,
-                light    = 25,
-                lightMax = 50,
-            },
-        },
-        effectsActive = {
-            sparks = {
-                n        = 15,
-                life     = 15,
-                light    = 5,
-                lightMax = 10,
-            },
-        }
-    }
-)
-munition50BMG_INC       = New(munition50BMG,
-    {
-        vox           = "bmgY",
-        name          = '.50 BMG Incendiary',
-        effects       = {
-            fire          = 1,
-            shrapnel      = {
-                n      = 5,
-                spread = 180
-            },
-            sparks        = {
-                n        = 20,
-                life     = 15,
-                light    = 50,
-                lightMax = 75,
-            },
-            subProjectile = {
-                spread    = 180,
-                shellSets = {
-                    {
-                        min   = 0,
-                        n     = 1,
-                        shell = munitionShrapnelHeavyIncendiary
-                    },
-                }
-            }
-        },
-        effectsActive = {
-            fire   = 1,
-            sparks = {
-                n        = 10,
-                life     = 7.5,
-                light    = 25,
-                lightMax = 50,
-            },
-        },
-        hitEvent      = function(self, hitMaterial, hitNormal, debrisCount)
-            Incendiary(self, math.random(3, 5), 60, hitNormal)
-        end,
-    }
-)
-munition50BMG_AB        = New(munition50BMG_AP,
-    {
-        vox           = "bmgR",
-        name          = '.50 BMG Air Burst',
-        delay         = .5,
-        caliber       = 0.02,
-        gunSpread     = 3,
-        proxyDistance = 5,
-        tracer        = -1,
-        effects       = {
-            fire   = 1,
-            smoke  = 1,
-            sparks = {
-                n        = 100,
-                life     = 10,
-                light    = 50,
-                lightMax = 125,
-            },
-        },
-        proxyEvent    = function(projectile, dt, distance, ballistics)
-            projectile.hit = true
-            --ProExplosion(
-            --    projectile.pos,
-            --    0.35,
-            --    nil,
-            --    nil,
-            --    false
-            --)
-            ExplosionSparks(projectile.pos, 500, 15, projectile.v)
-            SoundManager:explosion(1, projectile.pos)
-            Shrapnel(projectile, 20, 35, 20, nil, 175)
-            Shrapnel(projectile, 5, 10, 45, nil, 175)
-            ballistics:projectileEffects(
-                projectile,
-                projectile.pos,
-                projectile.effects,
-                {
-                    material = materialAir,
-                    materialName = "air",
-                }
-            )
-            return false
-        end,
-
-    }
-)
-munition50BMG_RB        = New(munition50BMG_AP,
-    {
-        vox       = "bmgR",
-        name      = '.50 BMG Room Buster',
-        delay     = .5,
-        caliber   = 0.02,
-        gunSpread = 3,
-        tracer    = -1,
-        KE        = 900 + minKE,
-        data      = {
-            timeFuse = .2,
-            distanceFuse = 1,
-        },
-        effects   = {
-            shrapnel      = {
-                min    = 25,
-                max    = 50,
-                spread = 180
-            },
-            smoke         = 1,
-            fire          = 1,
-            sparks        = {
-                n        = 50,
-                life     = 10,
-                light    = 25,
-                lightMax = 100,
-            },
-            subProjectile = {
-                spread    = 90,
-                shellSets = {
-                    {
-                        min   = 5,
-                        max   = 10,
-                        shell = munitionShrapnelSmall
-                    },
-
-                }
-            }
-        },
-        hitEvent  = function(projectile, material, normal)
-            if not projectile.hit then
-                projectile.specialEvent = 000
-                projectile.data.firstHitAt = projectile.totalDistance
-            end
-        end,
-        event     = function(projectile, dt, ballistics)
-            if
-                (projectile.totalDistance > (projectile.data.distanceFuse + projectile.data.firstHitAt))
-                or projectile.specialEvent > projectile.data.timeFuse
-            then --explode
-                ExplosionSparks(projectile.pos, 500, 15, projectile.v)
-                SoundManager:explosion(1, projectile.pos)
-                ballistics:projectileEffects(
-                    projectile,
-                    projectile.pos,
-                    projectile.effects,
-                    {
-                        material = materialAir,
-                        materialName = "air",
-                    }
-                )
-                return false
-            end
-
-            return true
-        end,
-    }
-)
-munitionM6HEP           = New(munition50mmRocket, {
-    initialV    = 0.1,
-    caliber     = .1,
-    vox         = "rpg",
-    spin        = 3,
-    gunSpread   = 5,
-    recoilTimer = shotDelay * 11,
-    delay       = 1,
-    name        = "M6 HEP",
-    tracer      = 0,
-    KE          = minKE + 75,
-    data        = {
-        engineLifetime   = 2.5,
-        engineDelay      = 0.25,
-        thrust           = 55,
-        thrustShake      = 550,
-        engineShake      = 2000,
-        distanceToTarget = 0,
-    },
-    effects     = {
-        explosion     = 1,
-        fire          = 1,
-        fireball      = 2,
-        sparks        = {
-            n        = 200,
-            life     = 15,
-            light    = 75,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 40,
-            spread = 180,
-        },
-        subProjectile = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 10,
-                    n     = 50,
-                    shell = munitionShrapnelSmall
-                },
-                {
-                    min   = 5,
-                    n     = 25,
-                    shell = munitionShrapnelMedium
-                },
-                {
-                    n     = 10,
-                    shell = munitionShrapnelHeavy
-                },
-                {
-                    min   = 0,
-                    n     = 1,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                --{
-                --    min   = .75,
-                --    max   = 1.5,
-                --    shell = EffectsFireballFastShort
-                --},
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballMedium
-                --},
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballHeavy
-                --},
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballHeavyLow
-                --},
-            }
-        }
-    },
-})
-munitionM6HEAT          = New(munitionM6HEP, {
-    initialV      = 0.1,
-    vox           = "rpg",
-    gunSpread     = 5,
-    delay         = 1,
-    name          = "M6 HEAT",
-    tracer        = 0,
-    data          = {
-        engineLifetime   = 2.5,
-        engineDelay      = 0.25,
-        thrust           = 55,
-        thrustShake      = 550,
-        engineShake      = 2000,
-        distanceToTarget = 0,
-    },
-    effects       = {
-        explosion     = .5,
-        fire          = 1,
-        fireball      = 1,
-        --HEAT          = {
-        --    focal     = 2,
-        --    shellSets = {
-        --        {
-        --            min   = 20,
-        --            n     = 35,
-        --            shell = munitionShrapnelMediumIncendiary,
-        --        },
-        --        {
-        --            min   = 15,
-        --            n     = 20,
-        --            shell = munitionShrapnelAP,
-        --        },
-        --    }
-        --},
-        subProjectile = {
-            spread =2,
-            shellSets = {
-                {
-                    min   = 5,
-                    n     = 10,
-                    shell = munitionShrapnelMediumIncendiary,
-                },
-                {
-                    min   = 5,
-                    n     = 15,
-                    shell = munitionShrapnelAP,
-                },
-            }
-        },
-        smoke         = .5,
-        shrapnel      = {
-            n      = 10,
-            spread = 180
-        },
-        sparks        = {
-            n        = 15,
-            life     = 5,
-            light    = .45,
-            lightMax = 1.5,
-        },
-    },
-    effectsActive = {
-        sparks = {
-            n        = 25,
-            life     = 5,
-            light    = 1,
-            lightMax = 5,
-        },
-    },
-    proxyDistance = 1,
-    proxyEvent    = proxyHEAT,
-})
-
-munition12gauge         = New(munition5_56mmFMJ, {
-    initialV      = 0.9,
-    vox           = symbolicValue(nil),
-    delay         = .25,
-    caliber       = 0.015,
-    name          = "12 Gauge",
-    type          = "shotgun",
-    recoil        = 0.5,
-    rounds        = 12,
-    burst         = 1,
-    gunSpread     = 35,
-    ricochet      = 50,
-    KE            = minKE + 450,
-    penetration   = { 1, .75, .25 },
-    effects       = {
-        makeHole = { .01, .01, .01 },
-        sparks = {
-            n        = 2,
-            life     = 5,
-            light    = .45,
-            lightMax = 1.5,
-        },
-    },
-    effectsActive = {
-        sparks = {
-            n        = 3,
-            life     = 5,
-            light    = .45,
-            lightMax = 2,
-        },
-    },
-})
-
-munitionBirdShot        = New(munition12gauge, {
-    initialV      = 0.9,
-    delay         = .25,
-    caliber       = 0.005,
-    name          = "Bird Shot",
-    type          = "shotgun",
-    rounds        = 16,
-    burst         = 1,
-    gunSpread     = 45,
-    KE            = 250,
-    ricochet      = 60,
-    penetration   = { .75, .5, .1 },
-    effects       = {
-        sparks = {
-            n        = 1,
-            life     = 3,
-            light    = .25,
-            lightMax = 1,
-        },
-    },
-    effectsActive = {
-        sparks = {
-            n        = 2,
-            life     = 3,
-            light    = .35,
-            lightMax = 2.5,
-        },
-    },
-})
-
-munitionSlug            = New(munition5_56mmFMJ, {
-    initialV      = 0.9,
-    vox           = "slug",
-    delay         = .25,
-    caliber       = 0.025,
-    name          = "Slug",
-    type          = "shotgun",
-    burst         = 1,
-    gunSpread     = 12.5,
-    recoil        = 0.75,
-    KE            = 3500,
-    ricochet      = 35,
-    penetration   = { 1.25, 1, .5 },
-    effects       = {
-        makeHole = { .02, .015, .01 },
-        shrapnel = {
-            n      = 3,
-            spread = 180
-        },
-        sparks = {
-            n        = 1,
-            life     = 3,
-            light    = .25,
-            lightMax = 1,
-        },
-    },
-    effectsActive = {
-        makeHole = { .01, .01, .01 },
-        sparks = {
-            n        = 5,
-            life     = 5,
-            light    = .5,
-            lightMax = 2.5,
-        },
-    },
-})
-munition7_62mmFMJ_Fast  = New(munition7_62mmFMJ, {
-    recoilTimer = shotDelay * 4.25,
-    gunSpread   = 10,
-    delay       = shotDelay * 2,
-    name        = "7.62mm FMJ",
-    caliber     = 0.0225,
-    KE          = 750,
-    type        = "minigunLoud",
-    tracer      = 3,
-    streamFire  = true,
-})
-munition7_62mmAP_Fast   = New(munition7_62mmAP, {
-    recoilTimer = shotDelay * 4.25,
-    gunSpread   = 10,
-    delay       = shotDelay * 2,
-    name        = "7.62mm AP",
-    caliber     = 0.0225,
-    KE          = 1750,
-    type        = "minigunLoud",
-    tracer      = 2,
-    streamFire  = true,
-})
+#version 2

```

---

# Migration Report: src\ammo\rocketry-advanced.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\rocketry-advanced.lua
+++ patched/src\ammo\rocketry-advanced.lua
@@ -1,46 +1,7 @@
-munition200mmVacuumRocket = New(munition150mmRocketGuidedFrag)
-function munition200mmVacuumRocket:constructor()
-    munition150mmRocketGuidedFrag.constructor(self)
-    self.effects       = {
-        explosion = 7,
-        makeHole  = { 4, 3, 3 }, --soft, medium, hard
-        sparks    = {
-            n        = 25,
-            life     = 10,
-            light    = 250,
-            lightMax = 500,
-        },
-    }
-    self.proxyDistance = 1
-end
-
-munition100mmJammedRocket = New(munition100mmRocketGuided, {
-    name   = "100mm (Broken/Jammed)",
-    delay  = 1,
-    recoil = 0.01,
-})
-function munition100mmJammedRocket:constructor()
-    self.data = {
-        engineLifetime = 8 * math.random(100, 105) / 100,
-        engineDelay    = 0.5,
-        thrust         = 30 * math.random(95, 105) / 100,
-        guided         = true,
-        guidanceMethod = 1,
-        thrustShake    = 450,
-        engineShake    = 3000,
-    }
-end
-
-function munition100mmJammedRocket:physics(dt, localTimeScale)
-    munition50mmRocket.physics(self, dt, localTimeScale)
-    if self.lifetime > self.data.engineDelay + 0.2 and self.data.guidanceMethod == 1 then
-        self.data.guidanceMethod = 'jammed'
-    end
-end
-
+#version 2
 local callbackStageSeparation = function(projectile, dt, ballistics)
     -- when no stages just disable special events and let the projectile continue
-    if #projectile.stages > 0 then
+    if #projectile.stages ~= 0 then
         local stage = projectile.stages[1]
         local delay = stage.delay or 1
         if projectile.specialEvent > delay then
@@ -83,104 +44,41 @@
 
     return true
 end
-callbackSubStageCloneAim      = function(stage, projectile, dt, ballistics)
-    if stage.shell ~= nil then
-        stage.shell.aimAt = projectile.aimAt
+
+function munition200mmVacuumRocket:constructor()
+    munition150mmRocketGuidedFrag.constructor(self)
+    self.effects       = {
+        explosion = 7,
+        makeHole  = { 4, 3, 3 }, --soft, medium, hard
+        sparks    = {
+            n        = 25,
+            life     = 10,
+            light    = 250,
+            lightMax = 500,
+        },
+    }
+    self.proxyDistance = 1
+end
+
+function munition100mmJammedRocket:constructor()
+    self.data = {
+        engineLifetime = 8 * math.random(100, 105) / 100,
+        engineDelay    = 0.5,
+        thrust         = 30 * math.random(95, 105) / 100,
+        guided         = true,
+        guidanceMethod = 1,
+        thrustShake    = 450,
+        engineShake    = 3000,
+    }
+end
+
+function munition100mmJammedRocket:physics(dt, localTimeScale)
+    munition50mmRocket.physics(self, dt, localTimeScale)
+    if self.lifetime > self.data.engineDelay + 0.2 and self.data.guidanceMethod == 1 then
+        self.data.guidanceMethod = 'jammed'
     end
 end
-callbackStageRestartEngine    = function(stage, projectile, dt, ballistics)
-    projectile.data.engineStarted = false
-    projectile.lifetime           = 0
-end
 
-callbackStageInitialV         = function(stage, projectile, dt, ballistics)
-    projectile.initialV = VecLength(projectile.v) / velocityMpl * (stage.vMpl or 0.75) -- * dt
-end
-callbackSubStageInitialV      = function(stage, projectile, dt, ballistics)
-    if stage.shell ~= nil then
-        stage.shell.initialV = VecLength(projectile.v) * (stage.vMpl or 1) / velocityMpl
-    end
-end
-callbackStageTargetShake      = function(stage, projectile, dt, ballistics)
-    projectile.aimAt = VecShake2d(projectile.aimAt, stage.targetShake or 50)
-end
-callbackGroupStarkStage       = {
-    --callbackStageTargetShake,
-    callbackStageRestartEngine,
-    callbackStageInitialV
-}
-munitionStarkMissile          = New(
-    munition200mmRocketBunkerBuster,
-    {
-        name         = "Jericho",
-        recoil       = 0.00,
-        specialEvent = 0,
-        stages       = {
-            {
-                delay   = 1,
-                min     = 3,
-                max     = 3,
-                spread  = 30,
-                shell   = nil,
-                --targetShake = 15,
-                effects = {
-                    explosion = 0.5,
-                    smoke     = 1,
-                    sparks    = {
-                        n        = 200,
-                        life     = 10,
-                        light    = 50,
-                        lightMax = 100,
-                    }
-                },
-                event   = callbackGroupStarkStage
-            },
-            {
-                delay   = 0.5,
-                min     = 3,
-                max     = 3,
-                spread  = 30,
-                shell   = nil,
-                --targetShake = 15,
-                effects = {
-                    explosion = 0.5,
-                    smoke     = 1,
-                    sparks    = {
-                        n        = 200,
-                        life     = 10,
-                        light    = 50,
-                        lightMax = 100,
-                    }
-                },
-                event   = callbackGroupStarkStage
-            },
-            {
-                delay   = 0.5,
-                min     = 2,
-                max     = 2,
-                spread  = 15,
-                shell   = munition50mmRocket,
-                --targetShake = 45,
-                effects = {
-                    sparks = {
-                        n        = 150,
-                        life     = 10,
-                        light    = 25,
-                        lightMax = 75,
-                    }
-                },
-                event   = {
-                    callbackStageTargetShake,
-                    callbackSubStageCloneAim,
-                    callbackSubStageInitialV,
-                }
-            }
-        }
-    },
-    {
-        event = callbackStageSeparation
-    }
-)
 function munitionStarkMissile:constructor()
     munition200mmRocketBunkerBuster.constructor(self)
     self.delay               = 1.5 --take it easy!
@@ -199,153 +97,6 @@
     }
 end
 
-munitionTomahawkMissile       = New(
-    munition100mmVisRocketHE,
-    {},
-    {
-        name                = "Tomahawk",
-        vox                 = "250mmR",
-        --vox             = "150mmR",
-        caliber             = 0.35,
-        length              = 2,
-        ricochet            = 5,
-        fixedSpawnPoint     = { math.random(2500, 3000) * randomSpawnDir[1], math.random(50, 100), math.random(2500, 2750) * randomSpawnDir[2], 500 },
-        fixedSpawnDirection = VecRotateRandom(Vec(0, 1, 0), 10, 0.1),
-        initialV            = 0.5,
-        KE                  = 1200 + minKE,
-        tracker             = {
-            drawTrace  = true,
-            leaveMarks = 15,
-        },
-        effects             = {
-            explosion     = 6,
-            --explosionDebris = 2,
-            fire          = 1,
-            fireball      = 3,
-            smoke         = 4,
-            makeHole      = { 6, 4.25, 3 },
-            --heat          = {
-            --    amount = 10000,
-            --    range  = 4,
-            --    n      = 64,
-            --},
-            sparks        = {
-                n        = 500,
-                life     = 15,
-                light    = 500,
-                lightMax = 750,
-            },
-            shrapnel      = {
-                n      = 300,
-                spread = 180
-            },
-            subProjectile = {
-                spread    = 180,
-                shellSets = {
-                    {
-                        min   = 75,
-                        n     = 125,
-                        shell = munitionShrapnelSmall
-                    },
-                    {
-                        min   = 50,
-                        n     = 75,
-                        shell = munitionShrapnelMedium
-                    },
-                    {
-                        min   = 30,
-                        n     = 50,
-                        shell = munitionShrapnelHeavy
-                    },
-                    {
-                        n     = 15,
-                        shell = New(munitionDebrisMetal, { KE = 5000, initialV = 0.3 }),
-                    },
-                    {
-                        min   = 2.5,
-                        n     = 4,
-                        shell = munitionShrapnelHeavyIncendiary
-                    },
-                    {
-                        min   = 4,
-                        n     = 6,
-                        shell = EffectsFireballFastShort
-                    },
-                    {
-                        min   = 2.5,
-                        n     = 4,
-                        shell = New(EffectsFireballHeavy, {
-                            initialV = .02,
-                        })
-                    },
-
-                    --{
-                    --    min   = 1,
-                    --    n     = 2,
-                    --    shell = munitionEffectsFireball
-                    --},
-                    --{
-                    --    min   = 1,
-                    --    n     = 2,
-                    --    shell = munitionEffectsFireballHeavy
-                    --},
-                }
-            }
-        }
-    }
-)
-
-defaultFlightAltitude         = 750
-defaultVerticalAttackDistance = 500
-callbackTomahawkGuidance      = function(projectile, thrustDirection)
-    local uplift                   = Vec(0, 1, 0)
-    local distanceToTarget         = VecDistance(projectile.aimAt, projectile.pos)
-    local distanceToTargetVertical = VecDistance(projectile.aimAt,
-        Vec(projectile.pos[1], projectile.aimAt[2], projectile.pos[3]))
-    local flightAltitude           = projectile.data.flightAltitude or defaultFlightAltitude
-    local verticalAttackDistance   = projectile.data.verticalAttackDistance or defaultVerticalAttackDistance
-    local aimHeight                = 150
-
-    if
-        projectile.lifetime > projectile.data.engineDelay
-        and distanceToTarget > flightAltitude * 2.5
-        and projectile.pos[2] < flightAltitude
-        and distanceToTargetVertical > verticalAttackDistance
-    then
-        projectile.data.engineStatus = 'Lift'
-        return VecNormalize(VecDirAdd(VecDirAdd(thrustDirection, uplift), thrustDirection))
-    elseif distanceToTargetVertical > verticalAttackDistance * 3 then
-        projectile.data.engineStatus = 'Aim High'
-        thrustDirection              = VecNormalize(VecSub(
-            Vec(projectile.aimAt[1], aimHeight + projectile.aimAt[2], projectile.aimAt[3]),
-            projectile.pos))
-        return thrustDirection
-    elseif distanceToTargetVertical > verticalAttackDistance then
-        aimHeight                    = aimHeight *
-            ((distanceToTargetVertical - verticalAttackDistance) / (verticalAttackDistance * 2))
-        projectile.data.engineStatus = 'Progressive Aim'
-        thrustDirection              = VecNormalize(VecSub(
-            Vec(projectile.aimAt[1], aimHeight + projectile.aimAt[2], projectile.aimAt[3]),
-            projectile.pos))
-        return thrustDirection
-    end
-
-    projectile.data.engineStatus = 'Target Lock'
-
-    local steeringPower          = projectile.data.steeringPower or 0.03
-
-    projectile.v                 = VecScale(
-        VecNormalize(
-            VecAdd(
-                VecNormalize(projectile.v),
-                VecScale(thrustDirection, steeringPower)
-            )
-        ),
-        VecLength(projectile.v)
-    )
-
-    return thrustDirection
-end
 function munitionTomahawkMissile:constructor()
     self.data = {
         engineLifetime = 20 * math.random(100, 105) / 100,
@@ -358,79 +109,6 @@
     }
 end
 
-munitionExosetMissile                   = New(
-    munitionTomahawkMissile,
-    {},
-    {
-        name         = "Exoset",
-        delay        = 0.25,
-        shootNoSound = true,
-        specialEvent = -1,
-        effects      = {
-            explosion     = 3.5,
-            fire          = 1,
-            fireball      = 5,
-            smoke         = 8,
-            makeHole      = { 5, 4, 3 },
-            sparks        = {
-                n        = 400,
-                life     = 15,
-                light    = 450,
-                lightMax = 700,
-            },
-            shrapnel      = {
-                n      = 250,
-                spread = 180
-            },
-            subProjectile = {
-                spread    = 180,
-                shellSets = {
-                    {
-                        min   = 75,
-                        n     = 125,
-                        shell = munitionShrapnelSmall
-                    },
-                    {
-                        min   = 75,
-                        n     = 100,
-                        shell = munitionShrapnelMedium
-                    },
-                    {
-                        min   = 25,
-                        n     = 75,
-                        shell = munitionShrapnelHeavy
-                    },
-                    {
-                        n     = 25,
-                        shell = New(munitionDebrisMetal, { KE = 5000, initialV = 0.3 }),
-                    },
-                    {
-                        min   = 1,
-                        n     = 2,
-                        shell = munitionShrapnelHeavyIncendiary
-                    },
-                    {
-                        min   = 1,
-                        n     = 2,
-                        shell = EffectsFireballHeavy
-                    },
-                    --{
-                    --    min   = 1,
-                    --    n     = 1,
-                    --    shell = munitionEffectsFireball
-                    --},
-                    --{
-                    --    min   = 2,
-                    --    n     = 3,
-                    --    shell = munitionEffectsFireballHeavy
-                    --},
-                }
-            }
-        }
-    }
-)
-munitionExosetMissile.obstacleDetection = nil
-munitionExosetMissile.preCheck          = nil
 function munitionExosetMissile:constructor()
     munitionTomahawkMissile.constructor(self)
     self.data.visionDetached         = true
@@ -441,102 +119,6 @@
 function munitionExosetMissile:destructor()
 
 end
-
-munition150mmLRM = New(munition100mmRocketGuided, {}, {
-    name                = "150mm Ballistic Missile",
-    vox                 = "150mmR",
-    fixedSpawnPoint     = { math.random(2000, 2500) * randomSpawnDir[1], math.random(50, 100), math.random(2000, 2500) * randomSpawnDir[2], 250 },
-    fixedSpawnDirection = VecRotateRandom(Vec(0, 1, 0), 10, 0.1),
-    caliber             = 0.15,
-    initialV            = 1,
-    KE                  = 500 + minKE,
-    delay               = 0.25,
-    shootNoSound        = true,
-    tracker             = {
-        drawTrace  = true,
-        leaveMarks = 10,
-    },
-    length              = 1.5,
-    effects             = {
-        explosion       = 1.5,
-        explosionDebris = 1.25,
-        makeHole        = nil,
-        fire            = 1,
-        fireball        = 2,
-        sparks          = {
-            n        = 500,
-            life     = 15,
-            light    = 100,
-            lightMax = 300,
-        },
-        shrapnel        = {
-            n      = 70,
-            spread = 180
-        },
-        subProjectile   = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 5,
-                    n     = 25,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 0,
-                    n     = 2,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 1,
-                    max   = 3,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 0,
-                --    max   = 2,
-                --    shell = EffectsFireballMedium
-                --},
-                --
-                {
-                    min   = 0,
-                    max   = 1.25,
-                    shell = New(EffectsFireballHeavy, {
-                        data = {
-                            keDropRate = .925,
-                            fireLifeMpl = .045,
-                        },
-                    }, {
-                        KE = 650,
-                        initialV = .015,
-                    })
-                },
-
-                --{
-                --    min   = 2,
-                --    max   = 2,
-                --    shell = EffectsFireballHeavyLow
-                --},
-            }
-        }
-    },
-    effectsActive       = {
-        explosion     = 0.35,
-        fire          = 0,
-        fireball      = 1,
-        smoke         = 1,
-        sparks        = {
-            n        = 50,
-            life     = 5,
-            light    = 100,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 5,
-            spread = 200
-        },
-        subProjectile = nil
-    }
-})
 
 function munition150mmLRM:constructor()
     self.data = {
@@ -551,116 +133,6 @@
     }
 end
 
-munition150mmSR                     = New(munition150mmLRM, {
-    shootNoSound    = _falseValue,
-    fixedSpawnPoint = _nilValue,
-    data            = {
-        guidanceMethod = 1,
-        engineDelay    = .25,
-    }
-}, {
-    fixedSpawnDirection = VecRotateRandom(Vec(0, 1, 0), 5, 0.1),
-})
-
-munition150mmSR.data.guidanceMethod = 1
-munition150mmSR.data.engineDelay    = .25
-munition250mmSR                     = New(munition150mmSR, {}, {
-    name     = "250mm Ballistic Missile",
-    voxScale = 1.25,
-    effects  = {
-        explosion     = 2.5,
-        fireball      = 4,
-        incendiary    = { n = 25, spread = 180 },
-        subProjectile = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 5,
-                    n     = 10,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 3,
-                    n     = 6,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 4,
-                    n     = 8,
-                    shell = munitionEffectsFireball
-                },
-                {
-                    min   = 3,
-                    n     = 6,
-                    shell = EffectsFireballFastShort
-                },
-                {
-                    min   = 2,
-                    n     = 3,
-                    shell = EffectsFireballHeavyLow
-                },
-                {
-                    min   = 2,
-                    n     = 3,
-                    shell = EffectsFireballHeavy
-                },
-            }
-        }
-    }
-})
-
-munition500mmSR                     = New(munition250mmSR, {}, {
-    name     = "500mm Ballistic Missile",
-    voxScale = 1,
-    vox      = "250mmR",
-    effects  = {
-        explosion     = 4,
-        fireball      = 4,
-        incendiary    = { n = 25, spread = 180 },
-        subProjectile = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 5,
-                    n     = 10,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 5,
-                    n     = 8,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 4,
-                    n     = 8,
-                    shell = munitionEffectsFireball
-                },
-                {
-                    min   = 4,
-                    n     = 6,
-                    shell = EffectsFireballFastShort
-                },
-                {
-                    min   = 2,
-                    n     = 4,
-                    shell = EffectsFireballHeavyLow
-                },
-                {
-                    min   = 3,
-                    n     = 5,
-                    shell = EffectsFireballHeavy
-                },
-                {
-                    min   = 1,
-                    n     = 3,
-                    shell = EffectsFireballHeavyVeryHot
-                },
-            }
-        }
-    }
-})
-
-munition150mmGuided                 = New(munition150mmSR)
 function munition150mmGuided:constructor()
     self.name                = "150mm Guided"
     self.initialV            = .2
@@ -679,157 +151,6 @@
     }
 end
 
--- munition150mmSR.data.guidanceMethod=1
-
-munitionBMxHyS                  = New(munitionExosetMissile, {}, {
-    name                = "500mm Hyper-Sonic Missile",
-    vox                 = "250mmR",
-    voxScale            = .5,
-    fixedSpawnPoint     = { math.random(4000, 5000) * randomSpawnDir[1], math.random(50, 100), math.random(5000, 6500) * randomSpawnDir[2], 1000 },
-    fixedSpawnDirection = VecRotateRandom(Vec(0, 1, 0), 10, 0.1),
-    caliber             = .5,
-    initialV            = 1,
-    KE                  = 1250 + minKE,
-    delay               = 0.25,
-    recoil              = 0.25,
-    shootNoSound        = true,
-    tracker             = {
-        drawTrace  = true,
-        leaveMarks = 10,
-    },
-    maxLifetime         = 45,
-    length              = 7,
-    effects             = {
-        explosion       = 5.5,
-        explosionDebris = 2,
-        makeHole        = nil,
-        fireball        = 5,
-        sparks          = {
-            n        = 500,
-            life     = 25,
-            light    = 600,
-            lightMax = 1200,
-        },
-        shrapnel        = {
-            n      = 125,
-            spread = 180
-        },
-        subProjectile   = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 50,
-                    n     = 75,
-                    shell = munitionShrapnelSmall,
-                },
-                {
-                    min   = 25,
-                    n     = 40,
-                    shell = munitionShrapnelMedium,
-                },
-                {
-                    min   = 5,
-                    n     = 15,
-                    shell = munitionShrapnelMediumIncendiary,
-                },
-                {
-                    min   = 20,
-                    n     = 30,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 3,
-                    n     = 6,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 3,
-                    max   = 4,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 2,
-                --    max   = 4,
-                --    shell = EffectsFireballMedium
-                --},
-                {
-                    min   = 2,
-                    max   = 3,
-                    shell = EffectsFireballHeavy,
-                },
-
-                {
-                    min   = 2,
-                    max   = 3,
-                    shell = EffectsFireballHeavyLow
-                },
-            }
-        }
-    },
-    effectsActive       = {
-        explosion     = 0.35,
-        fire          = 0,
-        fireball      = 2,
-        smoke         = 1,
-        sparks        = {
-            n        = 200,
-            life     = 5,
-            light    = 400,
-            lightMax = 700,
-        },
-        shrapnel      = {
-            n      = 15,
-            spread = 200
-        },
-        subProjectile = nil
-    }
-})
-
-callbackHyperSonicBoostGuidance = function(projectile, thrustDirection)
-    local uplift                   = Vec(0, 2, 0)
-    local distanceToTarget         = VecDistance(projectile.aimAt, projectile.pos)
-    local distanceToTargetVertical = VecDistance(projectile.aimAt,
-        Vec(projectile.pos[1], projectile.aimAt[2], projectile.pos[3]))
-    local distanceFromTurret       = VecDistance(projectile.shotFrom, projectile.pos)
-
-    if distanceToTarget > distanceFromTurret * 1.5 then
-        projectile.data.engineStatus = 'Flight #1'
-        return VecNormalize(VecDirAdd(thrustDirection, uplift))
-    elseif distanceToTargetVertical > 1250 then
-        projectile.data.engineStatus = 'Flight #2'
-        thrustDirection              = VecNormalize(VecSub(Vec(projectile.aimAt[1], 350, projectile.aimAt[3]),
-            projectile.pos))
-        return thrustDirection
-    end
-
-    projectile.data.engineStatus = 'Final Approach'
-
-    local steeringPower          = projectile.data.steeringPower or 0.02
-
-    projectile.v                 = VecScale(
-        VecNormalize(
-            VecAdd(
-                VecNormalize(projectile.v),
-                VecScale(thrustDirection, steeringPower)
-            )
-        ),
-        VecLength(projectile.v)
-    )
-    if distanceToTarget > 10000 then
-        if distanceFromTurret > 500 then
-            projectile.data.engineStatus = projectile.data.engineStatus .. '+B1'
-            projectile.data.thrust       = projectile.data.thrust * 1.0035
-        end
-
-        if distanceToTarget < 2500 then
-            projectile.data.engineStatus = projectile.data.engineStatus .. '+B2'
-            projectile.data.thrust       = projectile.data.thrust * 1.0025
-        end
-    end
-
-    return thrustDirection
-end
-
 function munitionBMxHyS:constructor()
     munitionExosetMissile.constructor(self)
     self.data = {
@@ -843,201 +164,3 @@
     }
 end
 
-munitionRV50mm   = New(
-    munition75mmArtillerySalvo,
-    {
-        caliber        = .05,
-        length         = .5,
-        rounds         = 1,
-        burst          = 1,
-        tracer         = 1,
-        tracerStrength = 1.75,
-        trackable      = 1,
-        penetration    = { 1, .75 },
-        KE             = 100,
-        weight         = 4,
-    },
-    {
-        vox = _nilValue,
-        effects = {
-            explosion     = 1.25,
-            fire          = 1,
-            fireball      = 2,
-            sparks        = {
-                n        = 200,
-                life     = 15,
-                light    = 150,
-                lightMax = 400,
-            },
-            shrapnel      = {
-                n      = 75,
-                spread = 180
-            },
-            subProjectile = {
-                spread    = 180,
-                shellSets = {
-                    {
-                        n     = 15,
-                        shell = munitionShrapnelMedium,
-                    },
-                    {
-                        n     = 15,
-                        shell = munitionShrapnelHeavy,
-                    },
-                    {
-                        min   = 0,
-                        n     = 1,
-                        shell = munitionShrapnelHeavyIncendiary,
-                    },
-                    {
-                        min   = 1,
-                        max   = 2,
-                        shell = EffectsFireballFastShort
-                    },
-                    {
-                        min   = 0,
-                        n     = .75,
-                        shell = New(EffectsFireballHeavy, {
-                            initialV = .02,
-                        })
-                    },
-                    --{
-                    --    min   = 0,
-                    --    max   = 1,
-                    --    shell = EffectsFireballMedium
-                    --},
-                    --{
-                    --    min   = 0,
-                    --    max   = 1,
-                    --    shell = EffectsFireballHeavy
-                    --},
-                    --{
-                    --    min   = 0,
-                    --    max   = 1,
-                    --    shell = EffectsFireballHeavyLow
-                    --},
-                }
-            }
-        },
-    }
-)
-munitionMRVx5    = New(
-    munitionBMxHyS,
-    {},
-    {
-        name                = "MRV 5x50mm",
-        caliber             = 0.45,
-        length              = 3.5,
-        recoil              = 0.00,
-        fixedSpawnPoint     = { math.random(2500, 3000) * randomSpawnDir[1], math.random(50, 100), math.random(2500, 2750) * randomSpawnDir[2], 500 },
-        fixedSpawnDirection = VecRotateRandom(Vec(0, 1, 0), 10, 0.1),
-        specialEvent        = -1,
-        proxyDistance       = 450,
-        effects             = {},
-        stages              = {
-            {
-                delay   = 0.001,
-                min     = 5,
-                max     = 5,
-                spread  = 5,
-                vMpl    = .75,
-                shell   = munitionRV50mm,
-                --targetShake = 45,
-                effects = {
-                    sparks = {
-                        n        = 150,
-                        life     = 10,
-                        light    = 150,
-                        lightMax = 350,
-                    }
-                },
-                event   = {
-                    --callbackStageTargetShake,
-                    --callbackSubStageCloneAim,
-                    callbackSubStageInitialV,
-                }
-            }
-        },
-        proxyEvent          = function()
-            return true
-        end,
-        event               = callbackStageSeparation,
-    }
-)
-
-munitionMRVx10   = New(
-    munitionBMxHyS,
-    {},
-    {
-        name                = "MRV 10x50mm",
-        caliber             = 0.55,
-        length              = 3.75,
-        recoil              = 0.00,
-        fixedSpawnPoint     = { math.random(2500, 3000) * randomSpawnDir[1], math.random(50, 100), math.random(2500, 2750) * randomSpawnDir[2], 500 },
-        fixedSpawnDirection = VecRotateRandom(Vec(0, 1, 0), 10, 0.1),
-        specialEvent        = -1,
-        proxyDistance       = 500,
-        effects             = {},
-        stages              = {
-            {
-                delay   = 0.001,
-                min     = 10,
-                max     = 10,
-                spread  = 7,
-                vMpl    = .85,
-                shell   = munitionRV50mm,
-                --targetShake = 45,
-                effects = {
-                    sparks = {
-                        n        = 150,
-                        life     = 10,
-                        light    = 150,
-                        lightMax = 350,
-                    }
-                },
-                event   = {
-                    --callbackStageTargetShake,
-                    --callbackSubStageCloneAim,
-                    callbackSubStageInitialV,
-                }
-            }
-        },
-        proxyEvent          = function()
-            return true
-        end,
-        event               = callbackStageSeparation
-    }
-)
-munitionMRVx10SR = New(
-    munitionMRVx5,
-    {},
-    {
-        name          = "MRV 10x50mm Short Reentry",
-        proxyDistance = 150,
-        effects       = {},
-        stages        = {
-            {
-                delay   = 0.001,
-                min     = 10,
-                max     = 10,
-                spread  = 12.5,
-                vMpl    = .75,
-                shell   = munitionRV50mm,
-                --targetShake = 45,
-                effects = {
-                    sparks = {
-                        n        = 150,
-                        life     = 10,
-                        light    = 150,
-                        lightMax = 350,
-                    }
-                },
-                event   = {
-                    --callbackStageTargetShake,
-                    --callbackSubStageCloneAim,
-                    callbackSubStageInitialV,
-                }
-            }
-        }
-    }
-)

```

---

# Migration Report: src\ammo\rocketry.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\rocketry.lua
+++ patched/src\ammo\rocketry.lua
@@ -1,23 +1,4 @@
-munitionRocketBase = New(Shell, {
-    explosive   = true,
-    length      = 1,
-    type        = 6,
-    tracer      = 0,
-    --tracerStrength = 1.25,
-    trackable   = 1,
-    maxLifetime = 20,
-    streamFire  = false,
-    penetration = { .65, .25, .35 },
-    vDebris     = 500,
-    data        = {
-        engineLifetime   = 1.5,
-        engineDelay      = 0.25,
-        thrust           = 55,
-        thrustShake      = 550,
-        engineShake      = 2000,
-        distanceToTarget = 0,
-    }
-})
+#version 2
 function munitionRocketBase:render(dt, localTimeScale)
     local d = VecNormalize(VecInvert(self.v))
     if self.data.effectFreeFlight then
@@ -135,118 +116,11 @@
     return thrustDirection
 end
 
-munition50mmRocket = New(munitionRocketBase, {
-    initialV      = 0.5,
-    name          = "50mm",
-    KE            = 150 + minKE,
-    proxyDistance = 0,
-    specialEvent  = -1,
-    caliber       = 0.05,
-    --penetration   = { 2, 3 },
-    lifetime      = 0,
-    ricochet      = 10,
-    hitEvent      = nil,
-    recoil        = 0.1,
-    rounds        = 1,
-    burst         = 1,
-    tracer        = -1,
-    gunSpread     = 30,
-    delay         = 0.1,
-    effects       = {
-        explosion     = 1,
-        fireball      = 1,
-        sparks        = {
-            n        = 200,
-            life     = 15,
-            light    = 75,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 30,
-            spread = 180,
-        },
-        subProjectile = {
-            spread    = 180,
-            shellSets = {
-                {
-                    min   = 10,
-                    n     = 50,
-                    shell = munitionShrapnelSmall
-                },
-                {
-                    min   = 5,
-                    n     = 25,
-                    shell = munitionShrapnelMedium
-                },
-                {
-                    n     = 10,
-                    shell = munitionShrapnelHeavy
-                },
-                {
-                    min   = .5,
-                    max   = 1,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballHeavy
-                --},
-                --{
-                --    min   = 0,
-                --    max   = 1,
-                --    shell = EffectsFireballHeavyLow
-                --},
-            }
-        }
-    },
-    effectsActive = {
-        smoke  = 1,
-        fire   = 0,
-        sparks = {
-            n        = 100,
-            life     = 10,
-            light    = 25,
-            lightMax = 75,
-        },
-    }
-})
-
 function munition50mmRocket:constructor()
     self.data.engineLifetime = self.data.engineLifetime * math.random(100, 105) / 100
     self.data.thrust         = self.data.thrust * math.random(95, 105) / 100
 end
 
-munition40mmRocketSalvo = New(munition50mmRocket, {
-    name      = "40mm Salvo 2x",
-    caliber   = 0.04,
-    KE        = 200 + minKE,
-    delay     = 0.35,
-    rounds    = 2,
-    burst     = 1,
-    recoil    = 0.20,
-    gunSpread = 65,
-    effects   = {
-        explosion     = 1,
-        fire          = 1,
-        fireball      = 1,
-        sparks        = {
-            n        = 100,
-            life     = 10,
-            light    = 75,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 30,
-            spread = 180
-        },
-        subProjectile = {
-            n      = 10,
-            spread = 360,
-            shell  = munitionShrapnelHeavy
-        }
-    },
-})
 function munition40mmRocketSalvo:constructor()
     self.data.engineLifetime = self.data.engineLifetime * math.random(90, 110) / 100
     self.data.thrust         = self.data.thrust * math.random(85, 125) / 100
@@ -254,146 +128,6 @@
     --local pointA, pointB
     local hit                = QueryRaycast(pointA, VecNormalize(VecSub(pointB, pointA)))
 end
-
-munition100mmRocketGuided       = New(munition50mmRocket, {}, {
-    name           = "100mm Guided",
-    vox            = "100mmR",
-    caliber        = 0.1,
-    initialV       = 0.2,
-    KE             = 500 + minKE,
-    delay          = 0.5,
-    recoil         = 0.25,
-    tracerStrength = 1.4,
-    maxLifetime    = 25,
-    tracker        = {
-        drawTrace  = true,
-        leaveMarks = 5,
-    },
-    length         = 1.25,
-    data           = {
-        engineLifetime = 5.5 * math.random(100, 105) / 100,
-        engineDelay    = 0.4,
-        thrust         = 45 * math.random(95, 105) / 100,
-        guided         = true,
-        guidanceMethod = 1,
-        thrustShake    = 450,
-        engineShake    = 3000,
-    },
-    effects        = {
-        explosion       = 1.5,
-        explosionDebris = 1,
-        fire            = 1,
-        fireball        = 2,
-        sparks          = {
-            n        = 350,
-            life     = 15,
-            light    = 100,
-            lightMax = 300,
-        },
-        shrapnel        = {
-            n      = 75,
-            spread = 180
-        },
-        subProjectile   = {
-            spread    = 180,
-            shellSets = {
-                {
-                    n     = 25,
-                    shell = munitionShrapnelMedium,
-                },
-                {
-                    n     = 15,
-                    shell = munitionShrapnelHeavy,
-                },
-                {
-                    min   = 0,
-                    n     = 1.5,
-                    shell = munitionShrapnelHeavyIncendiary
-                },
-                {
-                    min   = 1,
-                    max   = 1.25,
-                    shell = EffectsFireballFastShort
-                },
-                --{
-                --    min   = 1,
-                --    max   = 2,
-                --    shell = EffectsFireballMedium
-                --},
-                --{
-                --    min   = 1,
-                --    max   = 2,
-                --    shell = EffectsFireballHeavy
-                --},
-                --{
-                --    min   = 1,
-                --    max   = 2,
-                --    shell = EffectsFireballHeavyLow
-                --},
-                {
-                    min   = 0,
-                    max   = .45,
-                    shell = New(EffectsFireballHeavy, {
-                        data = {
-                            keDropRate = .925,
-                            fireLifeMpl = .05,
-                        },
-                    }, {
-                        KE = 500,
-                        initialV = .02,
-                    })
-                },
-            }
-        }
-    },
-    effectsActive  = {
-        smoke         = 1,
-        fire          = 0,
-        fireball      = 1,
-        sparks        = {
-            n        = 40,
-            life     = 5,
-            light    = 100,
-            lightMax = 200,
-        },
-        shrapnel      = {
-            n      = 5,
-            spread = 200
-        },
-        subProjectile = nil
-    }
-})
-
-callbackJavelinGuidance         = function(projectile, thrustDirection)
-    local uplift = Vec(0, 1, 0)
-    if projectile.lifetime < 0.5 + projectile.data.engineDelay then
-        return VecDirAdd(thrustDirection, uplift)
-    elseif projectile.lifetime < 0.75 + projectile.data.engineDelay then
-        return VecDirAdd(VecDirAdd(thrustDirection, uplift), thrustDirection)
-    end
-
-    thrustDirection = VecReflect(VecNormalize(projectile.v), thrustDirection)
-
-    if
-        VecDistance(projectile.aimAt, VecAdd(projectile.pos, thrustDirection)) > VecDistance(projectile.aimAt, projectile.pos)
-    then
-        thrustDirection = VecInvert(thrustDirection)
-    end
-
-    return VecNormalize(thrustDirection)
-end
-munition200mmRocketBunkerBuster = New(munition100mmRocketGuided, {
-    name                = "200mm Bunker Buster",
-    fixedSpawnDirection = VecRotateRandom(Vec(0, -1, 0), 10, 0.1),
-    fixedSpawnPoint     = {
-        0,
-        math.random(2750, 3250),
-        0,
-        500,
-        250
-    },
-
-})
 
 function munition200mmRocketBunkerBuster:constructor()
     self.initialV      = 0.2
@@ -485,10 +219,6 @@
     }
 end
 
-munition150mmRocketGuidedFrag = New(munition200mmRocketBunkerBuster, {
-    name = "150mm Frag",
-    vox  = "150mmR",
-})
 function munition150mmRocketGuidedFrag:constructor()
     munition200mmRocketBunkerBuster.constructor(self)
     self.initialV      = 0.1
@@ -548,132 +278,6 @@
     self.proxyEvent    = proxyAirHit
 end
 
-munition100mmGuidedSCHE   = New(munition100mmRocketGuided, {
-    name          = "100mm Guided SC-HE",
-    proxyDistance = 3,
-    proxyEvent    = proxyAirHit,
-    effects       = {
-        explosion     = 1,
-        fireball      = 1,
-        sparks        = {
-            n        = 250,
-            life     = 10,
-            light    = 250,
-            lightMax = 500,
-        },
-        shrapnel      = {
-            min    = 25,
-            n      = 75,
-            spread = 100
-        },
-        subProjectile = {
-            spread    = 20,
-            shellSets = {
-                {
-                    min   = 20,
-                    n     = 50,
-                    shell = munitionShrapnelSmall
-                },
-                {
-                    spread = 12.5,
-                    min    = 15,
-                    n      = 25,
-                    shell  = munitionShrapnelMedium
-                },
-                {
-                    spread = 2,
-                    min    = 5,
-                    n      = 15,
-                    shell  = New(munitionShrapnelHeavy, {}, {
-                        tracer = 1,
-                        tracerStrength = 0.35,
-                        tracerWidthMpl = 3,
-                    })
-                },
-                {
-                    spread = 1,
-                    min    = 5,
-                    n      = 15,
-                    shell  = New(munitionShrapnelAP, {}, {
-                        tracer = 1,
-                        tracerStrength = 0.45,
-                        tracerWidthMpl = 3,
-                    })
-                },
-            }
-        }
-    },
-})
-munition100mmGuidedSCFrag = New(munition100mmRocketGuided, {
-    name          = "100mm Guided SC-Frag",
-    KE            = minKE,
-    effects       = {
-        --explosion     = 0.5,
-        --makeHole      = { 1, 0.5, 0.25 }, --soft, medium, hard
-        fire          = 1,
-        sparks        = {
-            n        = 250,
-            life     = 10,
-            light    = 250,
-            lightMax = 500,
-        },
-        shrapnel      = {
-            min    = 15,
-            n      = 50,
-            spread = 180
-        },
-        subProjectile = {
-            spread    = 20,
-            shellSets = {
-                {
-                    min   = 25,
-                    n     = 75,
-                    shell = munitionShrapnelSmall
-                },
-                {
-                    spread = 5,
-                    min    = 25,
-                    n      = 50,
-                    shell  = munitionShrapnelMediumIncendiary
-                },
-                {
-                    min   = 10,
-                    n     = 25,
-                    shell = munitionShrapnelHeavy
-                },
-                {
-                    spread = 2.5,
-                    min    = 25,
-                    n      = 50,
-                    shell  = munitionShrapnelAP
-                },
-            }
-        }
-    },
-    effectsActive = {
-        fire     = 1,
-        smoke    = 1,
-        sparks   = {
-            n        = 50,
-            life     = 5,
-            light    = 100,
-            lightMax = 200,
-        },
-        shrapnel = {
-            n      = 25,
-            spread = 200
-        },
-    }
-})
-munition100mmVisRocketHE  = New(munition100mmRocketGuided, {
-    name         = "100mm HE MilVision",
-    delay        = 0.5,
-    recoil       = 0,
-    initialV     = 0.5,
-    specialEvent = 0,
-    --fixedSpawnDirection = VecRotateRandom(Vec(0, 1, 0), 10, 0.1),
-
-})
 function munition100mmVisRocketHE:event(dt, ballistics)
     self.specialEvent    = -1
     MilVision.projectile = self
@@ -681,24 +285,6 @@
     return true
 end
 
-callbackJavelinSimpleGuidance = function(projectile, thrustDirection)
-    if projectile.lifetime < .5 + projectile.data.engineDelay then
-        projectile.data.engineStatus = 'Lift #1'
-        return VecDirAdd(thrustDirection, Vec(0, 1, 0))
-    end
-
-    projectile.data.engineStatus = 'Final Approach'
-    local distanceToTarget       = VecDistance(projectile.aimAt, projectile.pos)
-    thrustDirection              = VecReflect(VecNormalize(projectile.v), thrustDirection)
-
-    if
-        VecDistance(projectile.aimAt, VecAdd(projectile.pos, thrustDirection)) > distanceToTarget
-    then
-        thrustDirection = VecInvert(thrustDirection)
-    end
-
-    return VecNormalize(thrustDirection)
-end
 function munition100mmVisRocketHE:constructor()
     self.id        = id()
     self.obstacles = New(TwoWayListWrapper)
@@ -781,11 +367,6 @@
     --end
 end
 
-MilVisObstacleDetection = {
-    range          = { 10, 650 },
-    maxObstacles   = 500,
-    maxSearchAngle = 15,
-}
 function munition100mmVisRocketHE:obstacleDetection()
     if self.obstacles.count < MilVisObstacleDetection.maxObstacles then
         local diff = MilVisObstacleDetection.maxObstacles - self.obstacles.count
@@ -829,3 +410,4 @@
         end
     end
 end
+

```

---

# Migration Report: src\ammo\rockets-incendiary.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\rockets-incendiary.lua
+++ patched/src\ammo\rockets-incendiary.lua
@@ -1,4 +1,4 @@
-munition150mmFuel = New(munition150mmGuided)
+#version 2
 function munition150mmFuel:constructor()
     self.name    = "150mm Incendiary"
     self.effects = {
@@ -33,7 +33,6 @@
     }
 end
 
-munition150mmFuelX = New(munition150mmGuided)
 function munition150mmFuelX:constructor()
     self.name            = "150mm Incendiary X"
     self.penetration     = { .35, .1, .25 }
@@ -82,7 +81,6 @@
     }
 end
 
-munition500mmFuel = New(munition150mmFuelX)
 function munition500mmFuel:constructor()
     self.name                    = "500mm Incendiary X"
     self.effects.explosion       = 4
@@ -131,7 +129,6 @@
     }
 end
 
-munition500mmNapalm = New(munition150mmFuelX)
 function munition500mmNapalm:constructor()
     self.name                  = "500mm Napalm X"
     self.effects.explosion     = 3
@@ -155,7 +152,6 @@
     }
 end
 
-munition500mmNapalmI = New(munition150mmFuelX)
 function munition500mmNapalmI:constructor()
     self.name                  = "500mm Napalm I"
     self.effects.explosion     = 3
@@ -179,7 +175,6 @@
     }
 end
 
-munition500mmNapalmIX = New(munition150mmFuelX)
 function munition500mmNapalmIX:constructor()
     self.name                  = "500mm Napalm I-X"
     self.proxyDistance         = 7.5
@@ -217,7 +212,6 @@
     }
 end
 
-munition500mmNapalmIXX = New(munition150mmFuelX)
 function munition500mmNapalmIXX:constructor()
     self.name                  = "500mm Napalm I-XX"
     self.proxyDistance         = 7.5
@@ -256,7 +250,6 @@
     }
 end
 
-munition250mmFuel = New(munition150mmFuelX)
 function munition250mmFuel:constructor()
     self.name                  = "250mm Incendiary X"
     self.effects.explosion     = 2.5
@@ -298,3 +291,4 @@
         }
     }
 end
+

```

---

# Migration Report: src\ammo\small-caliber.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ammo\small-caliber.lua
+++ patched/src\ammo\small-caliber.lua
@@ -1,267 +1,3 @@
--- NEW AMMO FORMAT --
+#version 2
 local minigunOffset    = Vec(5, 0, 0)
 
-munition12mmFMJ        = New(
-    Shell,
-    {
-    barrelOffset=minigunOffset,
-        vox            = "bmg",
-        type           = 1,
-        name           = '12.7mm FMJ',
-        burst          = 2,
-        rounds         = 1,
-        recoil         = 0.00005,
-        gunSpread      = 20,
-        delay          = shotDelay * 2,
-        KE             = 450,
-        initialV       = 0.9,
-        minKE          = 10,
-        caliber        = 0.015,
-        tracer         = 5,
-        ricochet       = 160,
-        penetration    = defaultPenetration,
-        streamFire     = true,
-        tracerStrength = .75,
-        data           = {
-            noPenetration = false,
-            hitKEMpl      = 1,
-            noDust        = false,
-        },
-        effects        = {
-            shrapnel = {
-                n      = 1,
-                spread = 180
-            },
-            sparks   = {
-                n        = 10,
-                life     = 5,
-                light    = 1,
-                lightMax = 4,
-            },
-        },
-        effectsActive  = {
-            sparks = {
-                n        = 5,
-                life     = 5,
-                light    = 2,
-                lightMax = 5,
-            },
-        },
-    }
-)
-munition12mmAP         = New(
-    munition12mmFMJ,
-    {
-        vox           = "bmgW",
-        type          = 1,
-        name          = '12.7mm AP',
-        burst         = 1,
-        rounds        = 1,
-        recoil        = 0.0001,
-        gunSpread     = 15,
-        delay         = shotDelay * 3,
-        KE            = 1000,
-        initialV      = 1.1,
-        caliber       = 0.02,
-        tracer        = 3,
-        ricochet      = 10,
-        penetration   = { 2.5, 4 },
-        streamFire    = true,
-        data          = {
-            noPenetration = false,
-            hitKEMpl      = 1,
-            noDust        = false,
-        },
-        effects       = {
-            smoke    = 1,
-            shrapnel = {
-                n      = 5,
-                spread = 180
-            },
-            sparks   = {
-                n        = 15,
-                life     = 12,
-                light    = 4,
-                lightMax = 10,
-            },
-        },
-        effectsActive = {
-            shrapnel = {
-                n      = 3,
-                spread = 180
-            },
-            sparks   = {
-                n        = 7,
-                life     = 10,
-                light    = 3,
-                lightMax = 7,
-            },
-        }
-    }
-)
-munition12mmIncendiary = New(
-    munition12mmFMJ,
-    {
-        type          = 1,
-        vox           = "bmgY",
-        name          = '12.7mm Incendiary',
-        burst         = 1,
-        rounds        = 1,
-        recoil        = 0.0005,
-        gunSpread     = 10,
-        delay         = shotDelay * 2,
-        KE            = 350,
-        initialV      = 0.88,
-        caliber       = 0.02,
-        tracer        = 2,
-        ricochet      = 120,
-        penetration   = defaultPenetration,
-        streamFire    = true,
-        hitEvent      = function(self, hitMaterial, hitNormal, debrisCount)
-            Incendiary(self, math.random(3, 5), 60, hitNormal)
-        end,
-        data          = {
-            noPenetration = false,
-            hitKEMpl      = 1,
-            noDust        = false,
-        },
-        effects       = {
-            fire   = 1,
-            sparks = {
-                n        = 20,
-                life     = 15,
-                light    = 50,
-                lightMax = 75,
-            },
-        },
-        effectsActive = {
-            fire   = 1,
-            sparks = {
-                n        = 10,
-                life     = 7.5,
-                light    = 25,
-                lightMax = 50,
-            },
-        }
-    }
-)
-munition12mmHeat       = New(
-    munition12mmFMJ,
-    {
-        type          = 1,
-        name          = '12.7mm Heat',
-        burst         = 1,
-        rounds        = 1,
-        recoil        = 0.0005,
-        gunSpread     = 10,
-        delay         = shotDelay * 2,
-        KE            = 550,
-        initialV      = 0.88,
-        caliber       = 0.02,
-        tracer        = 5,
-        ricochet      = 120,
-        penetration   = defaultPenetration,
-        streamFire    = true,
-        data          = {
-            noPenetration = false,
-            hitKEMpl      = 1,
-            noDust        = false,
-        },
-        effects       = {
-            fire   = 1,
-            heat   = {
-                amount = 10000,
-                n      = 16,
-                range  = 1
-            },
-            sparks = {
-                n        = 20,
-                life     = 15,
-                light    = 75,
-                lightMax = 125,
-            },
-        },
-        effectsActive = {
-            fire   = 1,
-            sparks = {
-                n        = 10,
-                life     = 7.5,
-                light    = 25,
-                lightMax = 50,
-            },
-        }
-    }
-)
-munition25mmFlare      = New( --unfinished
-    munition12mmFMJ,
-    {
-        type          = 1,
-        name          = '25mm Flares',
-        burst         = 1,
-        rounds        = 1,
-        recoil        = 0.002,
-        gunSpread     = 10,
-        delay         = 0.3,
-        KE            = 300,
-        initialV      = 0.9,
-        caliber       = 0.025,
-        tracer        = 20,
-        ricochet      = 90,
-        proxyDistance = 50,
-        penetration   = defaultPenetration,
-        hitEvent      = function(self, hitMaterial, hitNormal, debrisCount)
-            Incendiary(self, math.random(3, 5), 60, hitNormal)
-        end,
-        proxyEvent    = function(projectile, dt, distance)
-            _Sparks(projectile.pos, 250, 20, 50)
-            Smoke(projectile.pos)
-            PointLight(pos, 0.72, 0.27, 0.05, math.random(50, 100))
-
-            for i = 1, 5 do
-                local newFlareShell = projectile:clone(
-                    {
-                        v = VecRotateRandom(VecScale(projectile.v, math.random(10, 100) * 0.001), 100, 1)
-                    }
-                )
-                ProBallistics.ballistics:AddShell(newFlareShell)
-            end
-            projectile.v = VecScale(projectile.v, 0.5)
-            return true
-        end,
-        event         = function(projectile, dt)
-            if not SpecialEventDiffCompare(projectile, dt) then
-                return true
-            end
-            _Sparks(projectile.pos, 25, 20, 3, { 1, 0.9, 0.3 })
-            if math.random(0, 2) == 0 then
-                _Dust(projectile.pos, 2, 8)
-            end
-            PointLight(projectile.pos, 1, 0.9, 0.3, 75 + 50 * math.abs(math.sin(time * 3)) + math.random(0, 15))
-            return true
-        end,
-        data          = {
-            noPenetration = false,
-            hitKEMpl      = 1,
-            noDust        = false,
-        },
-        effects       = {
-            smoke  = 1,
-            fire   = 1,
-            sparks = {
-                n        = 150,
-                life     = 10,
-                light    = 75,
-                lightMax = 125,
-            },
-        },
-        effectsActive = {
-            fire   = 1,
-            sparks = {
-                n        = 50,
-                life     = 7.5,
-                light    = 25,
-                lightMax = 50,
-            },
-        }
-    }
-)

```

---

# Migration Report: src\antiAir.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\antiAir.lua
+++ patched/src\antiAir.lua
@@ -1,52 +1,4 @@
-AntiAir = {
-    rocketTracker = nil,
-    systems       = New(
-        Options,
-        {
-        },
-        {
-            options = {
-                PhalanxSystem:New(
-                    _,
-                    {
-                        turretClass = PhalanxCIWS
-                    }
-                ),
-                PhalanxSystem:New(
-                    _,
-                    {
-                        turretClass = Phalanx12
-                    }
-                ),
-                PhalanxSystem:New(
-                    _,
-                    {
-                        turretClass = Phalanx45
-                    }
-                ),
-                PhalanxSystem:New(
-                    _,
-                    {
-                        turretClass = Phalanx30
-                    }
-                ),
-                PhalanxSystem:New(
-                    _,
-                    {
-                        turretClass = IronDome
-                    }
-                ),
-                PhalanxSystem:New(
-                    _,
-                    {
-                        turretClass = PatriotSystem
-                    }
-                ),
-            }
-        }
-    ),
-}
-
+#version 2
 function AntiAir:setRocketTracker(rocketTracker)
     self.rocketTracker = rocketTracker
     for _, system in pairs(self.systems.options) do
@@ -153,3 +105,4 @@
         end
     end
 end
+

```

---

# Migration Report: src\api\pb.commands.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\api\pb.commands.lua
+++ patched/src\api\pb.commands.lua
@@ -1,83 +1,4 @@
-ProBallisticsCommands = {
-    commands = {
-        shoot = function(self, args)
-            if args.shell ~= nil then
-                local ammo = self.getAmmo(args.shell, args.shellExtra)
-                ProBallistics.ballistics:shoot(
-                    ammo,
-                    args.from,
-                    args.at,
-                    args.aimExtra
-                )
-            end
-        end,
-        subProjectilesMixed = function(self, args)
-            if args.shellSets ~= nil then
-                local ammo = {}
-
-                for k, v in pairs(args.shellSets) do
-                    ammo = self.getAmmo(v.shell, v.shellExtra)
-                    if not ammo then
-                        table.remove(args.shellSets, k)
-                    else
-                        v.shell = ammo
-                    end
-                end
-                ProBallistics.ballistics:subProjectileMixed(
-                    {
-                        pos = args.pos or Vec(),
-                        v = args.v or Vec(),
-                        KE = args.KE or minKE,
-                    },
-                    args.spread or 90,
-                    args.normal or nil,
-                    args.shellSets
-                )
-            end
-        end,
-        subProjectiles = function(self, args)
-            if args.shell ~= nil then
-                local ammo = self.getAmmo(args.shell, args.shellExtra)
-                if ammo then
-                    ProBallistics.ballistics:subProjectile(
-                        {
-                            pos = args.pos or Vec(),
-                            v = args.v or Vec(),
-                            KE = args.KE or minKE,
-                        },
-                        args.min or 0,
-                        args.max or 1,
-                        args.spread or 90,
-                        ammo,
-                        args.normal or nil
-                    )
-                    --DebugWatch("PBC",{
-                    --    {
-                    --        pos = args.pos or Vec(),
-                    --        v = args.v or Vec(),
-                    --        KE = args.KE or minKE,
-                    --    },
-                    --    args.min or 0,
-                    --    args.max or 1,
-                    --    args.spread or 90,
-                    --    ammo,
-                    --    args.normal or nil
-                    --})
-                    return true
-                else
-                    DebugPrint("No Ammo?")
-                end
-            end
-
-            return false
-        end,
-        explode = function(self, args) end,
-        effects = function(self, args)
-            -- ProBallistics.ballistics:projectileEffects()
-        end,
-        sound = function(self, args) end,
-    },
-}
+#version 2
 function ProBallisticsCommands.getAmmo(shellName, extra)
     if ProBallistics.registeredAmmo[shellName] ~= nil then
         return
@@ -100,4 +21,3 @@
     ProBallisticsCommands:dispatch(cmd, args)
 end
 
-RegisterListenerTo(_pbCmd, "cmdListener")

```

---

# Migration Report: src\api\pb.weapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\api\pb.weapons.lua
+++ patched/src\api\pb.weapons.lua
@@ -1,6 +1,4 @@
-ProBallisticsApi = {
-    initialized = false,
-}
+#version 2
 function ProBallisticsApi:init()
     if self.initialized then
         return
@@ -15,7 +13,6 @@
         [_munition12mmFMJ] = munition12mmFMJ,
         [_munition12mmAP] = munition12mmAP,
         [_munition12mmInc] = munition12mmIncendiary,
-
 
         [_munition5_56mmFMJ] = munition5_56mmFMJ,
         [_munition5_56mmFMJT] = munition5_56mmFMJT,
@@ -202,3 +199,4 @@
     end
     return parsed
 end
+

```

---

# Migration Report: src\artillery.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\artillery.lua
+++ patched/src\artillery.lua
@@ -1,9 +1,4 @@
--- Unfinished
-Artillery = {
-    aimPos        = Vec(),
-    autoAim       = nil,
-    weaponLoadOut = nil,
-}
+#version 2
 function Artillery:inputs()
     if InputDown(ProBallistics.keyAutoAimShoot) then
         if not self:shoot(self.autoAim:processAiming()) then
@@ -21,6 +16,7 @@
     self.autoAim         = New(AutoAim)
     self.autoAim.vehicle = self
 end
+
 function Artillery:New ()
 
     return New(
@@ -33,6 +29,7 @@
             }
     )
 end
+
 function Artillery:shoot(aimAt)
 
     local shell, prototype = self.weaponLoadOut:getShell(true)
@@ -46,4 +43,5 @@
     end
 
     return false
-end+end
+

```

---

# Migration Report: src\autoaim.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\autoaim.lua
+++ patched/src\autoaim.lua
@@ -1,335 +1 @@
-autoAimSpeed    = 0.5
-autoAimMinSpeed = 0.05
-autoAimMaxSpeed = 3
-_smooth         = "smooth"
-_point          = "point"
-_zigzag         = "zigzag"
-AutoAim         = {
-    vehicle        = nil,
-    dir            = Vec(),
-    distance       = 0,
-    targetPoint    = Vec(),
-    aimPos         = nil,
-    targets        = New(TwoWayListWrapper),
-    layers         = New(TwoWayListWrapper),
-    layerCount     = 10,
-    cycleBack      = false,
-    mode           = _smooth,
-    modes          = { _smooth, _point, _zigzag },
-    uiAim          = false,
-    constructor    = function(self)
-        for i = 1, self.layerCount do
-            self.layers:add({ layer = New(TwoWayListWrapper, { id = i }) })
-        end
-        self.layers:reset()
-        self.targets = self.layers.current.layer
-    end,
-    cycleLayer     = function(self)
-        self.targets = self.layers:next(true).layer
-        DebugPrint(string.format("Switched to %d target layer.", self.targets.id))
-    end,
-    recalculate    = function(self)
-        if not self.targets.current or not self.targets.current.next then
-            self.aimPos = nil
-            return false
-        end
-
-        self.dir         = VecNormalize(VecSub(self.targets.current.next.pos, self.targets.current.pos))
-        self.aimPos      = self.targets.current.pos
-        self.targetPoint = self.targets.current.next.pos
-
-        return true
-    end,
-    processBack    = function(self)
-        if self.mode == _point then
-            if not self.targets:prev() then
-                self.targets.current = self.targets.last
-            end
-        end
-    end,
-    processAiming  = function(self)
-        local switch, travel
-        if self.mode == _smooth then
-            if not self.aimPos and not self:recalculate() then
-                return
-            end
-
-            local currentPos = self.aimPos
-            local travelVec  = VecScale(self.dir, autoAimSpeed)
-            travel           = VecLength(travelVec)
-            self.distance    = self.distance + VecLength(travelVec)
-            self.aimPos      = VecAdd(self.aimPos, travelVec)
-
-            if VecDistance(self.aimPos, self.targetPoint)
-                > VecDistance(currentPos, self.targetPoint)
-            then
-                self.targets:next()
-                if not self:recalculate() then
-                    self.targets:reset()
-                    switch = true
-                end
-            end
-
-            return currentPos, switch, travel
-        elseif self.mode == _zigzag then
-            if not self.aimPos and not self:recalculate() then
-                return
-            end
-
-            local currentPos = self.aimPos
-            local travelVec  = VecScale(VecRotateRandom2d(self.dir, 3, 10), autoAimSpeed)
-            travel           = VecLength(travelVec)
-            self.distance    = self.distance + VecLength(travelVec)
-            self.aimPos      = VecAdd(self.aimPos, travelVec)
-
-            if VecDistance(self.aimPos, self.targetPoint)
-                > VecDistance(currentPos, self.targetPoint)
-            then
-                self.targets:next()
-                if not self:recalculate() then
-                    self.targets:reset()
-                    switch = true
-                end
-            end
-
-            return currentPos, switch, travel
-        elseif self.mode == _point then
-            if not self.targets.current then
-                return false
-            end
-
-            travel        = VecLength(VecSub(self.targets.current.pos, self.aimPos))
-            self.distance = self.distance + travel
-            self.aimPos   = self.targets.current.pos
-
-            if not self.targets:next() then
-                switch = true
-                self.targets:reset()
-            end
-
-            return self.aimPos, switch, travel
-        end
-    end,
-    drawTargetLock = function(self)
-        if self.vehicle.aimVehicle > 0 and false then
-            UiPush()
-            if ProBallistics.targetLock then
-                UiColor(1, 0, 0)
-            else
-                UiColor(1, 1, 1)
-            end
-            local x, y, distance = UiWorldToPixel(GetEntityTransform(self.vehicle.aimVehicle).pos)
-            if distance > 0 then
-                UiAlign("center middle")
-                UiTranslate(x, y)
-                UiRectOutline(20, 20, 1)
-                UiCircleOutline(50, 2)
-                --UiTranslate(0,-50)
-                --UiAlign("center top")
-                --DebugWatch("VehicleDesc",GetDescription(self.vehicle.aimVehicle))
-                --DebugWatch("VehicleDesc",GetEntityName(self.vehicle.aimVehicle))
-                --UiText(GetDescription(self.vehicle.aimVehicle))
-                --UiText(GetEntityName(self.vehicle.aimVehicle))
-            end
-            --UiResetPos()
-            UiTranslate(UiCenter() - 500, UiMiddle() - 500)
-            if ProBallistics.targetLock then
-                local minX, minY, maxX, maxY, min, max, x, y, distance = 10000, 10000, -10000, -10000
-                local sMinX, sMinY, sMaxX, sMaxY = false, false, false, false
-                children = GetEntityChildren(self.vehicle.aimVehicle, "", true, "body")
-                for j = 1, #children do
-                    min, max = GetBodyBounds(children[j])
-                    x, y, distance = UiWorldToPixel(min)
-                    if distance > 0 then
-                        if x > maxX then
-                            maxX = x
-                            sMaxX = true
-                        elseif x < minX then
-                            minX = x
-                            sMinX = true
-                        end
-                        if y > maxY then
-                            maxY = y
-                            sMaxY = true
-                        elseif y < minY then
-                            minY = y
-                            sMinY = true
-                        end
-                    end
-                    x, y, distance = UiWorldToPixel(max)
-                    if distance > 0 then
-                        if x > maxX then
-                            maxX = x
-                            sMaxX = true
-                        elseif x < minX then
-                            minX = x
-                            sMinX = true
-                        end
-                        if y > maxY then
-                            maxY = y
-                            sMaxY = true
-                        elseif y < minY then
-                            minY = y
-                            sMinY = true
-                        end
-                    end
-                end
-
-                if sMinX and sMinY and sMaxX and sMaxY then
-                    local targetLockCoord =
-                        FluidChange:tween(
-                            "aaTargetLock",
-                            {
-                                x = minX,
-                                y = minY,
-                                w = maxX - minX,
-                                h = maxY - minY,
-                                t = 2,
-                            },
-                            .175
-                        )
-                    UiTranslate(targetLockCoord.x, targetLockCoord.y)
-                    UiAlign("left top")
-
-                    UiRectOutline(targetLockCoord.w, targetLockCoord.h, targetLockCoord.t)
-                    --DrawBodyOutline(children[j], 1, 1, 1, .85)
-                end
-            end
-            --local min, max = GetBodyBounds(mainBody)
-            --local x, y, distance = UiWorldToPixel(min)
-            --local x2, y2, distance2 = UiWorldToPixel(max)
-            --
-            --if distance > 0 and distance2 > 0 then
-            --    local w, h = x - x2, y - y2
-            --    UiAlign("center middle")
-            --    UiTranslate(x, y)
-            --    UiRectOutline(w, h, 2)
-            --end
-            UiPop()
-        end
-    end,
-    drawUi         = function(self)
-        self:drawTargetLock()
-        if not ProBallistics.overlay == _overlayAntiAir then
-            return
-        end
-        UiPush()
-        UiColor(1, 0, 0)
-
-        self.targets:iterate(function(element)
-            local x, y, distance = UiWorldToPixel(element.pos)
-            local sqSize         = 15
-            local sqSizeHalf     = math.floor(sqSize * 0.5)
-
-            if distance > 0 then
-                UiTranslate(x - sqSizeHalf, y - sqSizeHalf)
-                UiRectOutline(sqSize, sqSize, 1)
-            end
-        end)
-
-        UiPop()
-
-        if self.uiAim then
-            self.uiAim = false
-            UiPush()
-            UiTranslate(UiCenter(), UiMiddle())
-            local dir, pos, hit, dist
-            local offset = 250
-            for i = 1, 10 do
-                dir       = UiPixelToWorld(
-                    math.random(0, offset) * rSign(),
-                    math.random(0, offset) * rSign()
-                )
-                pos       = GetCameraTransform().pos
-                hit, dist = QueryRaycast(pos, dir, 1500)
-                if hit then
-                    self.targets:add(TwoWayVectorList(VecAdd(pos, VecScale(dir, dist))))
-                end
-            end
-            UiPop()
-        end
-    end,
-    drawInfoUi     = function(self)
-        local w, h, margin, lineH, maxWidth
-        lineH    = 30
-        margin   = 10
-        h        = 2 * lineH + margin
-        maxWidth = 0
-        UiPush()
-
-        UiTranslate(UiWidth() - margin * 2, UiHeight() - h)
-        UiAlign("right top")
-        UiTextOutline(0, 1, 0, 1)
-        local tW
-        for label, value in pairs({ ["Layer"] = self.targets.id, ["Targets"] = self.targets.count }) do
-            UiPush()
-            UiColor(0, 1, 0)
-            tW = UiText(string.format("[%d]", value))
-            UiTranslate(-(tW + margin), 0)
-            tW = tW + UiText(label)
-            UiPop()
-            UiTranslate(0, lineH)
-            if tW > maxWidth then
-                maxWidth = tW
-            end
-        end
-        UiPop()
-
-        w = maxWidth + margin * 3
-        UiPush()
-        UiTranslate(UiWidth() - margin, UiHeight() - margin)
-        UiAlign("right bottom")
-        UiColor(0.2, 0.2, 0.2, 0.5)
-        UiRoundedRectOutline(w, h, math.floor(margin / 2), 5)
-        UiColor(0, 1, 0, 1)
-        UiRoundedRectOutline(w, h, math.floor(margin / 2), 1)
-        UiPop()
-    end,
-    reset          = function(self)
-        self.targets:flush()
-        self.distance = 0
-    end,
-    inputs         = function(self)
-        if self.mode == _smooth then
-            if InputDown(ProBallistics.keyAutoAimMark) and ticks % 3 == 0 then
-                self.targets:add(TwoWayVectorList(self.vehicle.aimPos))
-            end
-        elseif InputPressed(ProBallistics.keyAutoAimMark) then
-            if self.mode == _point then
-                if not InputDown("shift") then
-                    self.targets:add(TwoWayVectorList(self.vehicle.aimPos))
-                else
-                    self.uiAim = true
-                end
-            else
-                if not InputDown("shift") then
-                    self.targets:add(TwoWayVectorList(self.vehicle.aimPos))
-                else
-                    self.uiAim = true
-                end
-            end
-        end
-
-        if InputPressed(ProBallistics.keyAutoAimReset) then
-            self:reset()
-        end
-
-        if InputPressed(ProBallistics.keyAutoAimMode) then
-            if not InputDown("shift") then
-                self.mode = cycle(self.mode, self.modes)
-                self.targets:reset()
-                self:recalculate()
-            else
-                self:cycleLayer()
-            end
-        end
-
-        if InputPressed(ProBallistics.keyAutoAimSpeedUp) then
-            autoAimSpeed = autoAimSpeed * 1.1;
-        elseif InputPressed(ProBallistics.keyAutoAimSlowDown) then
-            autoAimSpeed = autoAimSpeed * 0.90909;
-        end
-
-        autoAimSpeed = clamp(autoAimSpeed, autoAimMinSpeed, autoAimMaxSpeed)
-    end
-}
+#version 2

```

---

# Migration Report: src\autopilot.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\autopilot.lua
+++ patched/src\autopilot.lua
@@ -1,19 +1,10 @@
-AutoPilot    = {
-    path                  = {},
-    enabled               = false,
-    thrust                = 4,
-    altitude              = 175,
-    vehicle               = nil,
-    circlingDistance      = 350,
-    circlingTurnDirection = Vec(0, 90, 0)
-}
-
+#version 2
 function AutoPilot:getThrust()
     if not self.enabled then
         return false
     end
 
-    if #self.path > 0 then
+    if #self.path ~= 0 then
         --follow path
     else
         --around player
@@ -41,4 +32,5 @@
     if InputPressed(ProBallistics.keyAutopilot) then
         self.enabled = not self.enabled
     end
-end+end
+

```

---

# Migration Report: src\ballistics.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ballistics.lua
+++ patched/src\ballistics.lua
@@ -1,59 +1,4 @@
-Shell                     = New(
-    TwoWayList,
-    {
-        vox           = nil,
-        object        = nil,
-        pos           = Vec(),
-        prevPos       = Vec(),
-        type          = nil,
-        name          = "Unknown munition",
-        v             = Vec(),
-        KE            = 0,
-        minKE         = 10,
-        tracer        = 0,
-        caliber       = 0,
-        length        = .25,
-        ricochet      = 180,
-        lifetime      = 0,
-        specialEvent  = -1,
-        hitEvent      = nil,
-        proxyEvent    = nil,
-        proxyDistance = 0,
-        penetration   = { 1, .5 },
-        prevHitPos    = Vec(),
-        distance      = 0,
-        totalDistance = 0,
-        burst         = 1,
-        rounds        = 1,
-        recoil        = 0,
-        gunSpread     = 0,
-        trackable     = 0, --trackable by Anti Air systems
-        --tracker       = {
-        --    leaveMarks = 10
-        --},
-        hit           = false,
-        active        = true,
-        maxLifetime   = 12.5,
-        weight        = 1,
-        wind          = .5,
-        data          = {},
-    }
-)
-DelayedHit                = New(
-    TwoWayList,
-    {
-        distance = 0,
-        pos      = nil,
-        material = nil,
-        normal   = nil,
-        event    = nil,
-    }
-)
-ProjectileTracker         = New(TwoWayListWrapper)
-ProjectileTracker.log     = New(TwoWayListWrapper)
-ProjectileTracker.log.min = 0
-ProjectileTracker.log.max = 0
-
+#version 2
 function ProjectileTracker:add(projectile)
     TwoWayListWrapper.add(
         self,
@@ -96,10 +41,10 @@
     UiPush()
     self:iterate(
         function(item)
-            if item.projectile.locks ~= nil and item.projectile.locks > 0 then
+            if item.projectile.locks ~= nil and item.projectile.locks ~= 0 then
                 local x, y, distance = UiWorldToPixel(item.projectile.pos)
 
-                if distance > 0 then
+                if distance ~= 0 then
                     UiAlign("center middle")
                     UiTranslate(x, y)
                     UiColor(1, 0, 0, 1)
@@ -117,7 +62,7 @@
             if item.projectile.target ~= nil and item.projectile.aimAt ~= nil then
                 local x, y, distance = UiWorldToPixel(item.projectile.aimAt)
 
-                if distance > 0 then
+                if distance ~= 0 then
                     UiAlign("center middle")
                     UiTranslate(x, y)
                     UiColor(1, 0, 0, 1)
@@ -138,12 +83,6 @@
         end
     )
 end
-
-Ballistics = {
-    delayedHits = New(TwoWayListWrapper),
-    projectiles = New(TwoWayListWrapper, { name = "projectilesList" }),
-    groupedProjectiles = {},
-}
 
 function Ballistics:New()
     local copy         = New(self)
@@ -335,12 +274,12 @@
             -- randomize shell velocity so they don't hit at the same time if shot in burst
             loadedShell.v = VecScale(v, math.random(98, 103) * 0.01)
 
-            if j > 0 then
+            if j ~= 0 then
                 loadedShell.pos = VecSub(loadedShell.pos,
                     VecScale(VecNormalize(v), (j - math.ceil(shellTemplate.burst * 0.5)) /
                         (shellTemplate.burst * 10)))
             end
-            if loadedShell.proxyDistance > 0 then
+            if loadedShell.proxyDistance ~= 0 then
                 loadedShell.proxyDistance = loadedShell.proxyDistance * math.random(90, 120) * 0.01
             end
 
@@ -365,7 +304,7 @@
             self:AddShell(loadedShell)
             self:createShellShape(loadedShell)
 
-            if loadedShell.trackable > 0 then
+            if loadedShell.trackable ~= 0 then
                 self.rocketTracker:add(loadedShell)
             end
             lastSalvo:add(loadedShell)
@@ -532,7 +471,7 @@
         self:prependGroupedShell(newShell)
         self:createShellShape(newShell)
 
-        if newShell.trackable > 0 then
+        if newShell.trackable ~= 0 then
             self.rocketTracker:add(newShell)
         end
 
@@ -725,7 +664,7 @@
         end
     end
 
-    if effects.explosion ~= nil and effects.explosion > 0 then
+    if effects.explosion ~= nil and effects.explosion ~= 0 then
         ProExplosionWrapper(projectile, hitPos, math.min(effects.explosion, 4), lHitNormal, hitProps)
 
         ExplosionDebris(hitPos, effects.explosion, effects.explosionDebris or 1, lHitNormal)
@@ -740,7 +679,6 @@
         --testRing(hitPos, effects.smoke, nil, nil, lHitNormal, nil, clamp(effects.explosion or .5, .25, 2))
     end
 
-
     if effects.fire then
         Incendiary(projectile, effects.fire, 180)
     end
@@ -748,8 +686,6 @@
     if effects.incendiary ~= nil then
         Incendiary(projectile, effects.incendiary.n, effects.incendiary.spread)
     end
-
-
 
     if effects.fireball ~= nil then
         self:fireballEffects(projectile, effects)
@@ -841,7 +777,7 @@
 end
 
 function Ballistics:renderProjectile(projectile, dt)
-    if tracersEnabled and projectile.tracer > 0 then
+    if tracersEnabled and projectile.tracer ~= 0 then
         Tracer(projectile.pos, projectile.tracerStrength or 1, projectile.tracerColor)
         if projectile.class == _munitionClassEnergy then
             Sprites:renderEnergyProjectileTrace(projectile, dt)
@@ -994,3 +930,4 @@
         dt
     )
 end
+

```

---

# Migration Report: src\colors.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\colors.lua
+++ patched/src\colors.lua
@@ -1,88 +1,7 @@
+#version 2
 local _constByteDiv = 0.003921569
+
 function rgbToFloat(r, g, b)
     return r * _constByteDiv, g * _constByteDiv, b * _constByteDiv
 end
 
-Colors = {
-    fireBall = {
-        {
-            start = { rgbToFloat(230, 200, 100) },
-            finish = { rgbToFloat(80, 30, 10) },
-        },
-        {
-            start = { rgbToFloat(200, 165, 0) },
-            finish = { rgbToFloat(139, 69, 19) },
-        },
-        {
-            start = { rgbToFloat(200, 145, 0) },
-            finish = { rgbToFloat(80, 30, 10) },
-        },
-        --{
-        --    start = { rgbToFloat(100, 50, 0) },
-        --    finish = { rgbToFloat(25, 0, 0) },
-        --},
-
-        {
-            start = { rgbToFloat(255, 230, 20) },
-            finish = { rgbToFloat(80, 30, 10) },
-        },
-        {
-            start = {
-                rgbToFloat( --random "sparky" colour
-                    1 - math.random(0, 45) * 0.01,
-                    0.9 - math.random(0, 80) * 0.01,
-                    0.15 - math.random(0, 150) * 0.001
-                ),
-            },
-            finish = { 0, 0, 0 },
-        },
-        {
-            start = {
-                rgbToFloat( --random "fiery" colour
-                    .85 - math.random(0, 30) * .01,
-                    .4 - math.random(0, 30) * .01,
-                    .1 - math.random(0, 100) * .001
-                ),
-            },
-            finish = { 0, 0, 0 },
-        },
-    },
-    sparks = {
-            {
-                start = { rgbToFloat(230, 200, 100) },
-                finish = { rgbToFloat(80, 30, 10) },
-            },
-            {
-                start = { rgbToFloat(200, 165, 0) },
-                finish = { rgbToFloat(139, 69, 19) },
-            },
-            {
-                start = { rgbToFloat(200, 145, 0) },
-                finish = { rgbToFloat(80, 30, 10) },
-            },
-            {
-                start = { rgbToFloat(255, 230, 20) },
-                finish = { rgbToFloat(80, 30, 10) },
-            },
-            {
-                start = {
-                    rgbToFloat( --random "sparky" colour
-                        1 - math.random(0, 45) * 0.01,
-                        0.9 - math.random(0, 80) * 0.01,
-                        0.15 - math.random(0, 150) * 0.001
-                    ),
-                },
-                finish = { 0, 0, 0 },
-            },
-            {
-                start = {
-                    rgbToFloat( --random "fiery" colour
-                        .85 - math.random(0, 30) * .01,
-                        .4 - math.random(0, 30) * .01,
-                        .1 - math.random(0, 100) * .001
-                    ),
-                },
-                finish = { 0, 0, 0 },
-            },
-        }
-}

```

---

# Migration Report: src\common.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\common.lua
+++ patched/src\common.lua
@@ -1,11 +1,4 @@
-globalDeltaTime = 1 / 60
-time            = 0
-ticks           = 0
-math.randomseed(
-    GetTimeStep()
-    + GetTime()
-    + math.random(0, 1000)
-)
+#version 2
 function notRandom(n)
     math.randomseed(665)
     local numbers = {}
@@ -15,17 +8,11 @@
     return numbers
 end
 
-_oId = 0
 function oId()
     _oId = _oId + 1
     return _oId
 end
 
-_indexFunction = function(self, k)
-    if k == "__id" then
-        return self.__id
-    end
-end
 function New(orig, template, references, id)
     local copy
 
@@ -131,7 +118,6 @@
     return sliced
 end
 
--- DEPRECATED: replace usages with explicit logic
 function t(c, a, b)
     --
     if c and c ~= nil then
@@ -139,11 +125,6 @@
     end
     return b
 end
-
-TwoWayList = {
-    next = nil,
-    prev = nil,
-}
 
 function TwoWayList:clone(template, references)
     local next = self.next
@@ -162,13 +143,6 @@
     end
 end
 
-TwoWayListWrapper = {
-    current = nil,
-    count   = 0,
-    first   = nil,
-    last    = nil,
-    max     = nil
-}
 function TwoWayListWrapper:next(wrapAround)
     if not self.current then
         self.current = self.first
@@ -222,7 +196,7 @@
 end
 
 function TwoWayListWrapper:merge(wrapper)
-    if wrapper.count ~= nil and wrapper.count > 0 then
+    if wrapper.count ~= nil and wrapper.count ~= 0 then
         TwoWayListWrapper.add(self, wrapper.first)
         self.last = wrapper.last
     end
@@ -365,10 +339,6 @@
     return backward and options[#options] or options[1] or nil
 end
 
-Options = {
-    options  = {},
-    selected = 1,
-}
 function Options:getSelected()
     return self.options[self.selected]
 end
@@ -380,7 +350,6 @@
     end
 end
 
-Animation = {}
 function Animation.cycleUniform(cycle, n)
     local total = 0
     local r     = ticks % (cycle * n)
@@ -610,58 +579,7 @@
     DefaultVision.fogParams = fogParams
 end
 
-envDefault              = getEnv()
---envDefault.fogParams = { 250, 1000, 1, 6 }
-envDefault.fogParams[1] = 0
-
-FluidChange             = {
-    vars = {},
-    calc = function(a, b, rate)
-        rate = clamp(rate or .1, .001, 1.99)
-        return (a * rate + b * (2 - rate)) * .5
-    end,
-    --set = function(self, name, value)
-    --    self.vars[name] = value
-    --end,
-    set = function(self, name, value)
-        local valueType = type(value)
-
-        if valueType == "table" then
-            for k, v in pairs(value) do
-                self:set(name .. '.' .. k, v)
-            end
-        else
-            self.vars[name] = value
-        end
-    end,
-    clear = function(self, name)
-        self.vars[name] = nil
-    end,
-    tween = function(self, name, value, rate, default)
-        return self:change(name, value, rate * ProBallistics.timeScale, default)
-    end,
-    read = function(self, name, default)
-        return self.vars[name] or default
-    end,
-    change = function(self, name, value, rate, default)
-        local fluidValue
-        local valueType = type(value)
-
-        if valueType == "table" then
-            fluidValue = {}
-            for k, v in pairs(value) do
-                fluidValue[k] = self:change(name .. '.' .. k, v, rate, v)
-            end
-            value = fluidValue
-        elseif valueType == "number" then
-            fluidValue = self.calc(value, self.vars[name] or (default ~= nil and default) or value, rate)
-            self.vars[name] = fluidValue
-            value = fluidValue
-        end
-
-        return value
-    end,
-}
 function UiResetPos()
     UiTranslate(UiWidth() - UiWidth(), UiHeight() - UiHeight())
 end
+

```

---

# Migration Report: src\crosshair.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\crosshair.lua
+++ patched/src\crosshair.lua
@@ -1,46 +1,4 @@
-Crosshair = {
-    res = {
-        {
-            "MOD/img/hud/cs-1-1.png",
-            "MOD/img/hud/cs-1-3.png",
-            "MOD/img/hud/cs-1-2.png",
-            "MOD/img/hud/cs-1-3.png",
-        },
-        {
-            "MOD/img/hud/cs-2-1.png",
-            "MOD/img/hud/cs-2-2.png",
-        },
-        {
-            "MOD/img/hud/cs-3-4.png",
-            "MOD/img/hud/cs-3-3.png",
-            "MOD/img/hud/cs-3-1.png",
-            "MOD/img/hud/cs-3-2.png",
-            "MOD/img/hud/cs-3-1.png",
-            "MOD/img/hud/cs-3-3.png",
-        },
-        {
-            "MOD/img/hud/cs-4-1.png",
-            "MOD/img/hud/cs-4-2.png",
-        },
-        {
-            "MOD/img/hud/cs-6-1.png",
-            "MOD/img/hud/cs-6-2.png",
-        },
-        {
-            "MOD/img/hud/cs-5-1.png",
-            "MOD/img/hud/cs-5-2.png",
-        },
-        {
-            "MOD/img/hud/cs-7-1.png",
-            "MOD/img/hud/cs-7-2.png",
-        },
-        {
-            "MOD/img/hud/cs-6-1.png",
-            "MOD/img/hud/cs-6-2.png",
-        },
-
-    }
-}
+#version 2
 function Crosshair:get(id, cycle)
     cycle = cycle or 15
 
@@ -50,3 +8,4 @@
 
     return self.res[1][Animation.cycleUniform(cycle, #self.res[1])]
 end
+

```

---

# Migration Report: src\debris.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\debris.lua
+++ patched/src\debris.lua
@@ -1,8 +1,4 @@
-DebrisManager = {
-    shapes = New(TwoWayListWrapper),
-    deferredSearch = {},
-}
-
+#version 2
 function DebrisManager:addDeferredSearch(pos, w)
     self.deferredSearch[#self.deferredSearch + 1] = { pos = pos, w = w }
 end
@@ -159,3 +155,4 @@
     --    true
     --)
 end
+

```

---

# Migration Report: src\debugger.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\debugger.lua
+++ patched/src\debugger.lua
@@ -1,9 +1,4 @@
-Debugger = {
-    hits = New(TwoWayListWrapper, { max = 1500 }),
-    transforms = New(TwoWayListWrapper, { max = 100 }),
-    numValues = {},
-}
-
+#version 2
 function Debugger:logNumValue(name, value)
     if self.numValues[name] == nil then
         self.numValues[name] = {
@@ -116,3 +111,4 @@
         end
     )
 end
+

```

---

# Migration Report: src\effects\fireball.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\effects\fireball.lua
+++ patched/src\effects\fireball.lua
@@ -1,502 +1,7 @@
+#version 2
 function WeightOscilationInit(self)
     self.data.originalWeight   = self.weight
     self.data.oscilationOffset = rnd(0, 5)
     self.data.oscilationSpeed  = rnd(2.5, 5)
 end
 
-EffectsFireballBase         = New(munitionShrapnelMediumIncendiary, {}, {
-    specialEvent    = 0,
-    ricochet        = 180,
-    penetration     = { .25, .1, .75 },
-    groupBy         = _projectile,
-    KE              = 650,
-    caliber         = .05,
-    minKE           = 4.5,
-    initialV        = .1,
-    maxLifetime     = 1,
-    keRate          = .75,
-    splitTime       = 0,
-    data            = {
-        keDropRate = .85,
-        vDropRate = .925,
-        lightMpl = .01,
-        smokeMinKe = 5,
-        smokeMaxKe = 1000,
-        smokeMaxDistance = 35,
-        fireMinKe = 10,
-        fireMaxDistance = 25,
-        attractMpl = .5,
-        minDistance = .75,
-        smokeGravity = { 50, 200 },
-        emberRate = .15,
-        --emberMinKe = 50,
-        emberMaxKe = 1250,
-        fireLifeMpl = .15,
-        fireMpl = .045,
-        --fireMpl = .03,
-    },
-    effects         = {
-        fire    = 1,
-        noSound = 1,
-        smoke   = 1,
-    },
-    effectsActive   = {
-        fire    = 1,
-        noSound = 1,
-        smoke   = 2,
-    },
-    --projectile:hitEvent(self, hitProps, debrisCount, hitKE)
-
-    hitEvent        = function(self, ballistics, hitProps, debrisCount, hitKE)
-        local hitForce = clamp(debrisCount * hitKE * .001, .5, 4)
-        ballistics:fireballEffects(self, {
-            fireball = 1,
-            explosion = hitForce,
-        })
-    end,
-    debug           = { 1, 1, 1, 1 },
-    --attract         = function(self, dt, neighbour)
-    --    local distance, dir =
-    --        VecDistance(self.pos, neighbour.pos) - self.data.minDistance,
-    --        VecDir(self.pos, neighbour.pos)
-    --
-    --    local force = VecScale(dir, self.data.attractMpl * distance)
-    --    if ProBallistics.debug then
-    --        DrawLine(self.pos, VecAdd(self.pos, force), 1, 1, 1, .5)
-    --    end
-    --    self.v = VecAdd(self.v, VecScale(force, dt))
-    --end,
-    attract         = function(self, dt, neighbour, ballistics)
-        local distance, dir =
-            VecDistance(self.pos, neighbour.pos) --[[- self.data.minDistance]],
-            VecDir(neighbour.pos, self.pos)
-        --optimize, dont process more than once
-        --        local force = VecScale(dir, self.data.attractMpl * distance)
-        local force = 2.5 * self.data.attractMpl / math.max(distance, .1)
-
-        if distance < self.data.minDistance then
-            force = -force * 2.5
-        end
-
-        force = force * math.min(1, neighbour.lifetime * 2) * self.data.effectsLifetimeMpl
-
-        local forceVector = VecScale(dir, force)
-
-        if ProBallistics.debug then
-            DrawLine(neighbour.pos, VecAdd(neighbour.pos, forceVector), 1, 1, 1, .5)
-        end
-        neighbour.v = VecAdd(neighbour.v, VecScale(forceVector, dt))
-
-        --if
-        --    neighbour.splitTime > .5
-        --    and distance < self.data.minDistance * .75
-        --then
-        --    self.split(neighbour, .5, ballistics)
-        --end
-    end,
-    split           = function(projectile, efficiency, ballistics)
-        efficiency = (efficiency or 1) * .5
-        projectile.KE = projectile.KE * .5
-        projectile.splitTime = 0
-        local clone = projectile:clone()
-        clone.lifetime = 0
-        clone.v = VecRotateRandom(clone.v, 900, .1)
-        ballistics:prependGroupedShell(clone)
-    end,
-    attractPrevious = function(self, dt, n, ballistics)
-        if self.prev then
-            self:attract(dt, self.prev, ballistics)
-            if n > 0 then
-                self:attractPrevious(dt, n - 1, ballistics)
-            end
-        end
-    end,
-    attractNext     = function(self, dt, n, ballistics)
-        if self.next then
-            self:attract(dt, self.next, ballistics)
-            if n > 0 then
-                self:attractNext(dt, n - 1, ballistics)
-            end
-        end
-    end,
-    physics         = function(self, dt, ballistics)
-        self.splitTime = self.splitTime + dt
-        self.data.effectsLifetimeMpl = math.min(1, self.lifetime * 2)
-
-        self:attractPrevious(dt, self.data.attractN or 3, ballistics)
-        self:attractNext(dt, self.data.attractN or 3, ballistics)
-        if self.data.originalWeight then
-            self:oscilateWeight()
-        end
-    end,
-    oscilateWeight  = function(self)
-        self.weight =
-            self.data.originalWeight *
-            (
-                math.sin(time * self.data.oscilationSpeed + self.data.oscilationOffset) * .5 + .75
-            )
-    end,
-    constructor     = function(self)
-        self.KE              = self.KE * lowRand(50, 200) * .01 + minKE
-        self.initialV        = self.initialV * lowRand(50, 150) * .01
-        self.maxLifetime     = self.maxLifetime * lowRand(50, 150) * .01
-        self.weight          = math.random(-250, -50) * .01
-        self.wind            = math.random(150, 350) * .01
-        self.data.smokeMaxKe = math.random(self.KE * .25, self.KE * .5)
-        WeightOscilationInit(self)
-    end,
-    event           = function(self, dt)
-        self.KE          = self.KE * (1 - (1 - self.data.keDropRate) * legacyTimeCorrection)
-        self.v           = VecScale(self.v, 1 - (1 - self.data.vDropRate) * legacyTimeCorrection)
-        local sKE        = math.sqrt(self.KE)
-        local luminosity = math.max(.01, sKE - 3) * math.random(125, 175) * self.data.lightMpl
-        if self.color ~= nil then
-            local r, g, b = _unpackColor(self.color)
-            PointLight(self.pos, r, g, b, luminosity)
-        else
-            PointLight(self.pos, 0.72, 0.27, 0.05, luminosity)
-        end
-
-        if not ProBallistics:timeScaleRand() then
-            local dir   = VecNormalize(self.v)
-            local cPerM = 2.5
-            local c, sPos, sV, fireVal
-            c           = math.max(1, self.distance * cPerM)
-            sV          = VecScale(dir, 1 / cPerM)
-
-            if
-                (self.data.emberRate or 0) > 0
-                and self.KE > self.data.fireMinKe * 2
-                --and projectile.KE > projectile.data.emberMinKe
-                and self.KE < self.data.emberMaxKe
-                --and projectile.totalDistance < projectile.data.smokeMaxDistance
-                and math.random() < self.data.emberRate
-            then
-                _Ember(RandomizeVec(self.pos, .5, 2), 1, 7.5, rnd(5, 25))
-            end
-            if
-                (self.effectsActive.smoke or 0) > 0
-                and self.KE > self.data.smokeMinKe
-                and self.KE < self.data.smokeMaxKe
-                and self.totalDistance < self.data.smokeMaxDistance
-            then
-                --if not projectile.data.smokeColor ~= nil then
-                --    projectile.data.smokeColor = highRand(0, 50) * .01
-                --end
-
-                sPos = self.pos
-                for i = 1, c do
-                    _Smoke(
-                        sPos,
-                        7.5,
-                        15,
-                        1,
-                        sKE * .075 + .5,
-                        lowRand(25, 75) * .1,
-                        dir,
-                        --projectile.data.smokeColor,
-                        highRand(0, 50) * .01,
-                        .5,
-                        nil,
-                        self.data.smokeGravity,
-                        { 150, 250, 0 },
-                        { 250, 500, 75, 150 },
-                        true
-                    )
-                    sPos = VecSub(sPos, sV)
-                end
-            end
-
-            if self.KE > self.data.fireMinKe
-                and self.totalDistance < self.data.fireMaxDistance
-            then
-                sPos              = self.pos
-                fireVal           = self.effectsActive.fire or 1
-                local lifetimeMpl = math.min(1, self.lifetime * 2)
-                for i = 1, c do
-                    _FireBall(
-                        sPos,
-                        fireVal --[[* 4 * ProBallistics.timeScale]],
-                        --sKE * .4 + .25,
-                        clamp(sKE * self.data.fireMpl + (highRand(0, 25)) * .1, .2, 2.5) --[[ * lifetimeMpl]],
-                        sKE * .065 + .35,
-                        dir,
-                        clamp(sKE * self.data.fireLifeMpl, .25, 1.25),
-                        { _fireBallColor() }
-                    )
-                    sPos = VecSub(sPos, sV)
-                end
-            end
-        end
-
-        return
-            self.KE > math.min(self.data.fireMinKe, self.data.smokeMinKe, self.minKE)
-    end
-})
-EffectsFireballFastShort    = New(EffectsFireballBase, {
-    data = {
-        keDropRate = .75,
-        vDropRate = .8,
-        lightMpl = .02,
-        emberRate = 0,
-        fireMpl = .065,
-    },
-    debug = { 1, 1, 1, 1 }
-}, {
-    constructor = function(self)
-        self.KE          = lowRand(650, 1000) + minKE
-        self.initialV    = lowRand(15, 250) * .001
-        self.maxLifetime = lowRand(250, 750, 3) * .001
-        self.weight      = math.random(-150, 25) * .01
-        self.wind        = math.random(100, 250) * .01
-    end,
-})
-
-EffectsFireballMedium       = New(EffectsFireballBase, {
-    data = {
-        keDropRate = .9,
-        vDropRate = .9,
-        lightMpl = .025,
-        smokeGravity = { 50, 250 },
-        emberRate = 0,
-    },
-    debug = { 0, 0, 1, 1 }
-}, {
-    constructor = function(self)
-        self.KE          = lowRand(650, 1000) + minKE
-        self.initialV    = lowRand(15, 200) * .001
-        self.maxLifetime = lowRand(500, 750, 2) * .01
-        --self.maxLifetime = lowRand(750, 1500, 3) * .001
-        self.weight      = math.random(-200, -75) * .01
-        self.wind        = math.random(100, 250) * .01
-        WeightOscilationInit(self)
-    end,
-})
-
-EffectsFireballHeavy        = New(EffectsFireballBase, {
-    data = {
-        keDropRate   = .975,
-        lightMpl     = .025,
-        fireMinKe    = 25,
-        smokeMinKe   = 10,
-        minDistance  = 1,
-        attractN     = 5,
-        smokeGravity = { 50, 350 },
-    },
-    --initialV = .025,
-    --KE = 2500,
-    debug = { 1, 0, 0, 1 }
-}, {
-    constructor = function(self)
-        self.KE               = 2500 * lowRand(1000, 4000) * .001 + minKE
-        --self.initialV         = .025 * lowRand(100, 250) * .01
-        self.initialV         = .05 * lowRand(100, 250) * .01
-        self.maxLifetime      = 0
-        --self.maxLifetime      = lowRand(550, 1000, 2) * .01
-        self.weight           = math.random(-225, -150) * .01
-        --self.data.attractMpl  = math.random(50, 200) * .01
-        self.data.attractMpl  = 0
-        self.data.vDropRate   = math.random(950, 975) * .001
-        --self.data.vDropRate   = math.random(925, 950) * .001
-        self.data.minDistance = math.random(50, 75) * .01
-        self.data.smokeMaxKe  = math.random(self.KE * .5, self.KE * .75)
-        --self.data.smokeMaxKe  = math.random(self.KE * .2, self.KE * .35)
-        self.wind             = math.random(100, 250) * .01
-        WeightOscilationInit(self)
-    end,
-})
-
-EffectsFireballHeavyVeryHot = New(EffectsFireballHeavy, {
-    data = {
-        lightMpl     = .03,
-        fireMinKe    = 50,
-        smokeMinKe   = 7.5,
-        smokeGravity = { 250, 500 },
-    },
-    debug = { 0, 1, 1, 1 }
-}, {
-    constructor = function(self)
-        self.KE               = lowRand(8000, 16000, 2) + minKE
-        self.initialV         = lowRand(25, 100) * .001
-        self.maxLifetime      = 0
-        --self.maxLifetime      = highRand(550, 1200, 2) * .01
-        self.weight           = math.random(-225, -150) * .01
-        self.data.attractMpl  = math.random(50, 200) * .01
-        self.data.vDropRate   = math.random(875, 925) * .001
-        self.data.minDistance = math.random(50, 75) * .01
-        self.data.smokeMaxKe  = math.random(self.KE * .5, self.KE * .75)
-        --self.data.smokeMaxKe  = math.random(self.KE * .2, self.KE * .35)
-        self.wind             = math.random(100, 250) * .01
-        --self.data.originalWeight = self.weight
-    end,
-})
-
-EffectsFireballNapalm       = New(EffectsFireballHeavy, {
-    KE = 8000,
-    data = {
-        lightMpl     = .03,
-        fireMinKe    = 50,
-        smokeMinKe   = 7.5,
-        smokeGravity = { 150, 450 },
-    },
-    debug = { 1, 0, 0, 1 }
-}, {
-    constructor = function(self)
-        self.KE               = self.KE * lowRand(1000, 2000, 2) * .001 + minKE
-        self.initialV         = lowRand(25, 100) * .001
-        self.maxLifetime      = highRand(550, 1200, 2) * .01
-        self.weight           = math.random(125, 200) * .01
-        self.data.attractMpl  = math.random(25, 75) * .01
-        self.data.vDropRate   = math.random(940, 965) * .001
-        self.data.minDistance = math.random(50, 75) * .01
-        self.data.smokeMaxKe  = math.random(self.KE * .5, self.KE * .75)
-        --self.data.smokeMaxKe  = math.random(self.KE * .2, self.KE * .35)
-        self.wind             = math.random(100, 250) * .01
-    end,
-})
-EffectsFireballHeavyLow     = New(EffectsFireballHeavy, {
-    debug = { 0, 1, 0, 1 },
-    KE = 2000,
-}, {
-    constructor = function(self)
-        self.KE                = self.KE * lowRand(1000, 3000, 3) * .001 + minKE
-        self.initialV          = lowRand(75, 125) * .001
-        self.maxLifetime      = 0
-        --self.maxLifetime       = lowRand(550, 1000, 3) * .01
-        self.weight            = lowRand(-50, 50) * .01
-        self.wind              = math.random(75, 175) * .01
-        self.data.vDropRate    = math.random(900, 935) * .001
-        self.data.attractN     = 3
-        self.data.smokeMaxKe   = math.random(self.KE * .5, self.KE * .75)
-        --self.data.smokeMaxKe   = math.random(self.KE * .25, self.KE * .35)
-        self.data.minDistance  = math.random(50, 100) * .01
-        self.data.attractMpl   = math.random(100, 200) * .01
-        self.data.smokeGravity = { -25, 50 }
-    end,
-})
-EffectsFireballGeneric      = New(EffectsFireballBase, {
-    debug = { 1, 1, 1, 1 }
-}, {
-    constructor = function(self)
-        EffectsFireballBase.constructor(self)
-        Randomizer:generateScalars(self, self.init or {})
-        Randomizer:generateScalars(self.data, self.initData or {})
-        WeightOscilationInit(self)
-    end,
-})
-
-
--- OLDER
-
-munitionEffectsFireball      = New(munitionShrapnelMediumIncendiary, {}, {
-    specialEvent  = 0,
-    ricochet      = 60,
-    penetration   = { .25, .1, .2 },
-    data          = {
-        keDropRate = .975,
-        vDropRate = .9,
-        lightMpl = .0025
-    },
-    effects       = {
-        fire    = 1,
-        noSound = 1,
-        smoke   = 1,
-    },
-    effectsActive = {
-        fire    = 2,
-        noSound = 1,
-        smoke   = 2,
-    },
-    debug         = { 1, 0, 1, 1 },
-    constructor   = function(self)
-        self.KE          = lowRand(350, 1200, 3) + minKE
-        self.initialV    = lowRand(50, 100) * .001
-        self.maxLifetime = lowRand(100, 250) * .01
-        self.weight      = math.random(-250, -50) * .01
-        self.wind        = math.random(150, 350) * .01
-    end,
-    --hitEvent    = function(self, hitMaterial, hitNormal, debrisCount)
-    --    Incendiary(self, math.random(3, 5), 60, hitNormal)
-    --end,
-    event         = function(projectile, dt)
-        projectile.KE    = projectile.KE * (1 - (1 - projectile.data.keDropRate) * legacyTimeCorrection)
-        projectile.v     = VecScale(projectile.v, 1 - (1 - projectile.data.vDropRate) * legacyTimeCorrection)
-        local sKE        = math.sqrt(projectile.KE)
-        local luminosity = math.max(.01, sKE - 3) * math.random(125, 175) * projectile.data.lightMpl
-        if projectile.color ~= nil then
-            local r, g, b = _unpackColor(projectile.color)
-            PointLight(projectile.pos, r, g, b, luminosity)
-        else
-            PointLight(projectile.pos, 0.72, 0.27, 0.05, luminosity)
-        end
-
-        if not ProBallistics:timeScaleRand() then
-            local dir = VecNormalize(projectile.v)
-
-            if (projectile.effectsActive.smoke or 0) > 0 and projectile.KE > projectile.minKE * .5
-                and projectile.totalDistance < 15 then
-                if not projectile.data.smokeColor ~= nil then
-                    projectile.data.smokeColor = (highRand(25, 50) + lowRand(0, 25)) * .01
-                end
-
-                local cPerM       = 2.5
-                local c, sPos, sV, fireVal
-
-                c                 = math.max(1, projectile.distance * cPerM)
-                sPos              = projectile.pos
-                sV                = VecScale(dir, 1 / cPerM)
-                fireVal           = projectile.effectsActive.fire or 1
-                local lifetimeMpl = math.min(1, projectile.lifetime * 2)
-
-                for i = 1, c do
-                    _FireBall(
-                        sPos,
-                        fireVal --[[ projectile.effectsActive.fire * 4 * ProBallistics.timeScale]],
-                        --sKE * .4 + .25,
-                        --highRand(25, 75) * .1,
-                        clamp((sKE * .75 + highRand(25, 50)) * .25, .35, 1.5) --[[ * lifetimeMpl]],
-                        sKE * .025 + .35,
-                        dir,
-                        sKE * .1,
-                        { _fireBallColor() }
-                    )
-                    _Smoke(
-                        sPos,
-                        7.5,
-                        15,
-                        1,
-                        (sKE * .1 + .5) * lifetimeMpl,
-                        lowRand(10, 25) * .1,
-                        dir,
-                        projectile.data.smokeColor,
-                        .5,
-                        nil,
-                        projectile.data.smokeGravity,
-                        nil, nil,
-                        true
-                    )
-                    sPos = VecSub(sPos, sV)
-                end
-            end
-        end
-
-        return projectile.KE > (lowRand(25, 250, 3) * .01)
-    end
-})
-munitionEffectsFireballHeavy = New(munitionEffectsFireball, {
-    data = {
-        keDropRate = .95,
-        vDropRate = .9,
-        lightMpl = .025
-    },
-    debug = { 1, 0, 0, 1 }
-}, {
-    constructor = function(self)
-        self.KE                 = lowRand(650, 2000) + minKE
-        self.initialV           = lowRand(15, 150) * .001
-        self.maxLifetime        = lowRand(150, 500, 3) * .01
-        self.weight             = math.random(-550, -100) * .01
-        self.effectsActive.fire = 1
-        self.wind               = math.random(200, 450) * .01
-    end,
-})

```

---

# Migration Report: src\extensions\mods.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\extensions\mods.lua
+++ patched/src\extensions\mods.lua
@@ -1,33 +1,4 @@
-ModManager = {
-    pbExtIds = {
-        ["3622787557"] = "LMG",
-        ["3611419174"] = "AP1",
-        ["3619318834"] = "AP2",
-        ["3632274316"] = "Overhaul",
-    },
-    pbExtCount = 0,
-    pbExt = {
-        ["AP1"] = {
-            id = 3611419174,
-            enabled = false,
-        },
-        ["AP2"] = {
-            id = 3619318834,
-            enabled = false,
-
-        },
-        ["LMG"] = {
-            id = 3622787557,
-            enabled = false,
-
-        },
-        ["Overhaul"] = {
-            id = 3632274316,
-            enabled = false,
-        },
-    },
-}
-
+#version 2
 function ModManager:initExtensions()
     local words, id, author, name, path, tags
     local list = ListKeys("mods.available")
@@ -132,3 +103,4 @@
     --        }
     --    )
 end
+

```

---

# Migration Report: src\info.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\info.lua
+++ patched/src\info.lua
@@ -1,9 +1,4 @@
-Info = {
-    lineH  = 30,
-    margin = 10,
-    lines  = {},
-}
-
+#version 2
 function Info:update()
     self.lines = {
         {
@@ -207,3 +202,4 @@
     UiPop()
     UiPop()
 end
+

```

---

# Migration Report: src\ironDome.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ironDome.lua
+++ patched/src\ironDome.lua
@@ -1,305 +1,4 @@
-callbackIronDomeGuidance      = function(projectile, thrustDirection)
-    local uplift           = Vec(0, 1.5, 0)
-    local distanceToTarget = VecDistance(projectile.aimAt, projectile.pos)
-
-    if (projectile.lifetime < 0.35 + projectile.data.engineDelay)
-        or (projectile.lifetime < 0.55 + projectile.data.engineDelay and not pRand(3))
-        or (projectile.lifetime < 0.7 + projectile.data.engineDelay and not pRand(2))
-    then
-        return VecDirAdd(VecDirAdd(thrustDirection, uplift), thrustDirection)
-    end
-
-    local steeringPower = (projectile.data.steeringPower or .75) * (1 - .5 * distanceToTarget / IronDome.maxDistance)
-    --local v             = VecScale(
-    --    VecNormalize(
-    --        VecAdd(
-    --            VecNormalize(projectile.v),
-    --            VecScale(thrustDirection, steeringPower)
-    --        )
-    --    ),
-    --    VecLength(projectile.v)
-    --)
-    local v             = VecScale(
-        VecRotateTowards(projectile.v,thrustDirection,.025),
-        VecLength(projectile.v)
-    )
-
-    --if VecLength(v) > 50
-    --    and VecDistance(projectile.shotFrom, projectile.pos) > 50
-    --then
-    --    local vD, angle    = VecDistance(v, projectile.v), VecAngleBetween(v, projectile.v)
-    --    local turningForce = vD * angle
-    --
-    --    if vD > 50 or angle > 30 or turningForce > (projectile.maxTurningForce or 375) then
-    --        projectile.active = false
-    --        return Vec()
-    --    end
-    --end
-
-    projectile.v                 = v
-    local minAltDiff, upliftRate = 25, .75
-    local altDiff                = projectile.aimAt[2] - projectile.pos[2]
-
-    if altDiff > minAltDiff then
-        thrustDirection = VecNormalize(
-            VecAdd(
-                thrustDirection,
-                VecScale(uplift, altDiff * upliftRate)
-            )
-        )
-    end
-
-    return thrustDirection
-end
-callbackIronDomeGuidanceBoost = function(projectile, thrustDirection)
-    if projectile.lifetime > (projectile.data.engineDelay + (projectile.data.engineBoostDelay or 1.5)) and not projectile.data.boosted then
-        if projectile.data.boostTarget == nil then
-            projectile.data.boostTarget = projectile.data.thrust + math.random(200, 250) * .1
-            projectile.tracerStrength   = projectile.tracerStrength * lowRand(115, 135) * .01
-        end
-
-        projectile.data.thrust = clamp(projectile.data.thrust * 1.025, 0, projectile.data.boostTarget)
-        Sparks(projectile.pos, math.random(5, 25), math.random(1, 5), 400, 650)
-
-        if projectile.data.thrust == projectile.data.boostTarget then
-            projectile.data.boosted = true
-        end
-    end
-
-    return callbackIronDomeGuidance(projectile, thrustDirection)
-end
-
-callbackIronDomeAim           = function(pos, projectileV, target, offset)
-    projectileV         = projectileV * .95
-    local aimAt         = target.pos
-    local distance      = VecDistance(pos, aimAt)
-
-    --naive method
-    local timeToTarget, newTimeToTarget
-    local timeTolerance = globalDeltaTime * .1
-    local maxIterations = 5
-    --local targetV       = VecScale(target.v, 2.5)
-    local targetV       = VecScale(target.v, 1)
-    --local aimEstimates  = {}
-    offset              = offset or math.sqrt(VecToKph(targetV))
-    local offsetV       = VecScale(VecNormalize(targetV), offset)
-    timeToTarget        = distance / projectileV
-
-    for i = 1, maxIterations do
-        aimAt           = VecAdd(target.pos, VecScale(targetV, timeToTarget * globalDeltaTime * rocketThrustMpl))
-        --aimAt           = VecAdd(target.pos, VecScale(targetV, timeToTarget * globalDeltaTime))
-        newTimeToTarget = VecDistance(pos, aimAt) / projectileV
-
-        --table.insert(aimEstimates, aimAt)
-
-        if math.abs(timeToTarget - newTimeToTarget) < timeTolerance then
-            break
-        end
-        timeToTarget = newTimeToTarget
-    end
-    aimAt           = VecAdd(aimAt, offsetV)
-    --aimAt           = VecAverage(aimEstimates)
-    newTimeToTarget = VecDistance(pos, aimAt) / projectileV
-
-    return aimAt, newTimeToTarget
-end
-munition75mmRocketHE          = New(
-    munition100mmRocketGuided,
-    {
-        name              = "75mm HE",
-        vox               = "150mmR",
-        caliber           = 0.075,
-        delay             = .5,
-        tracer            = -1,
-        maxLifetime       = 15,
-        tracerStrength    = 1.25,
-        initialV          = 0.1,
-        trackable         = -1,
-        gunSpread         = 7.5,
-        effects           = {
-            smoke  = 1,
-            sparks = {
-                n        = 35,
-                life     = 3,
-                light    = 350,
-                lightMax = 850,
-            },
-        },
-        effectsActive     = {},
-        data              = {
-            engineLifetime      = 12.5,
-            engineDelay         = 0.15,
-            thrust              = 35,
-            guided              = -1,
-            guidanceMethod      = callbackIronDomeGuidance,
-            thrustShake         = 10,
-            engineShake         = 200,
-            topAltitude         = 0,
-            targetLock          = 2,
-            engineStartLightMpl = 1.5,
-        },
-        specialEvent      = 0,
-        minTargetDistance = 10,
-        event             = function(self, dt, ballistics)
-            if self.pos[2] > self.data.topAltitude then
-                self.data.topAltitude = self.pos[2]
-            end
-
-            if self.target.active and (
-                    VecDistance(self.pos, self.target.pos) < self.minTargetDistance
-                    or VecDistance(VecAdd(self.pos, VecScale(self.v, dt)), self.target.pos) < self.minTargetDistance
-                    or VecDistance(VecAdd(self.target.pos, VecScale(self.target.v, dt)), self.pos) < self.minTargetDistance
-                ) then
-                self.target.active = false
-                ballistics:projectileEffects(
-                    self.target,
-                    self.target.pos,
-                    self.target.effects,
-                    {
-                        material = materialAir,
-                        materialName = "air",
-                    }
-                )
-
-                return false
-            end
-
-            if
-                (VecDistance(self.pos, self.shotFrom) > VecDistance(self.target.pos, self.shotFrom) and pRand(5))
-                or (self.lifetime > self.timer and pRand(3))
-                or (self.pos[2] < self.data.topAltitude * .35 and pRand(3))
-                or (self.data.topAltitude > self.pos[2] and self.pos[2] < self.data.minAltitude * .75 and pRand(3))
-                or (self.data.topAltitude > self.data.minAltitude and self.pos[2] < self.data.minAltitude and pRand(2))
-            then
-                return false
-            end
-
-            if self.lifetime > self.data.engineDelay * 1.025
-                and self.target.active
-            then
-                self.aimAt = callbackIronDomeAim(
-                    self.pos,
-                    VecLength(self.v),
-                    self.target,
-                    self.data.aimingOffset or nil
-                )
-                self.timer = self.lifetime + 1
-            end
-
-            return true
-        end,
-        destructor        = function(self, ballistics)
-            if self.target ~= nil then
-                self.target.locks = self.target.locks - self.data.targetLock
-                self.target       = nil
-            end
-
-            ballistics:projectileEffects(
-                self,
-                self.pos,
-                self.effects,
-                {
-                    material = materialAir,
-                    materialName = "air",
-                }
-            )
-        end
-    }
-)
-munition60mmRocketHE          = New(
-    munition75mmRocketHE,
-    {
-        name              = "60mm HE",
-        delay             = .2,
-        caliber           = 0.06,
-        type              = 8,
-        maxLifetime       = 8,
-        initialV          = 0.15,
-        gunSpread         = 10,
-        minTargetDistance = 10,
-        effects           = {
-            smoke  = 1,
-            sparks = {
-                n        = 35,
-                life     = 3,
-                light    = 300,
-                lightMax = 700,
-            },
-        },
-        data              = {
-            engineLifetime      = 7,
-            engineDelay         = 0.075,
-            thrust              = 30,
-            boostTarget         = 55,
-            guided              = -1,
-            guidanceMethod      = callbackIronDomeGuidanceBoost,
-            thrustShake         = 5,
-            engineShake         = 150,
-            topAltitude         = 0,
-            targetLock          = 2.5,
-            engineStartLightMpl = 1.5,
-            aimingOffset        = 5,
-        },
-    }
-)
-
-IronDome                      = New(
-    Phalanx12,
-    {
-        label          = "ID",
-        normal         = nil,
-        minDistance    = 650,
-        maxDistance    = 2500,
-        minAltitude    = 400,
-        maxTargetLocks = 3.5,
-        targetLock     = 0,
-        aimExtra       = New(AimExtra),
-        weaponLoadOut  = New(WeaponLoadOut, {
-            options = {
-                New(LoadOut,
-                    {
-                        name       = "IronDome",
-                        options    = { munition75mmRocketHE },
-                        magazine   = {
-                            size   = 3,
-                            reload = 5,
-                        },
-                        randomizer = {
-                            tracerStrength = {
-                                min          = 95,
-                                max          = 135,
-                                distribution = "lowRand",
-                            },
-                            delay          = {
-                                min = 90,
-                                max = 150,
-                            },
-                            initialV       = {
-                                min          = 100,
-                                max          = 150,
-                                distribution = "lowRand",
-                            },
-                            data           = {
-                                engineDelay = {
-                                    min          = 95,
-                                    max          = 175,
-                                    distribution = "lowRand",
-                                    n            = 3
-                                },
-                                thrust      = {
-                                    min = 95,
-                                    max = 105,
-                                },
-                            },
-                        },
-                    }
-                ),
-            }
-        }),
-        projectiles    = New(ProjectileTracker)
-    }
-)
-
+#version 2
 function IronDome:drawUi()
     self.projectiles:drawUi()
 
@@ -309,7 +8,7 @@
 
     if self.target ~= nil then
         x, y, distance = UiWorldToPixel(self.target.pos)
-        if distance > 0 then
+        if distance ~= 0 then
             UiTranslate(x, y)
             UiColor(1, 1, 0, 1)
             UiRoundedRectOutline(15, 15, 4, 2)
@@ -318,7 +17,7 @@
 
     x, y, distance = UiWorldToPixel(self.pos)
 
-    if distance > 0 then
+    if distance ~= 0 then
         UiPush()
         UiTranslate(x, y)
         UiColor(1, 1, 1, 1)
@@ -333,7 +32,7 @@
 
     x, y, distance = UiWorldToPixel(VecAdd(self.pos, self.normal))
 
-    if distance > 0 then
+    if distance ~= 0 then
         UiTranslate(x, y)
         UiColor(1, 1, 1, .75)
         UiRoundedRectOutline(10, 10, 4, 2)
@@ -423,53 +122,3 @@
     self.barrel.rotation.current = self.normal
 end
 
-PatriotSystem = New(
-    IronDome,
-    {
-        label          = "PAT",
-        normal         = nil,
-        minDistance    = 500,
-        maxDistance    = 1250,
-        minAltitude    = 375,
-        maxTargetLocks = 4.5,
-        targetLock     = .5,
-        aimExtra       = New(AimExtra),
-        weaponLoadOut  = New(WeaponLoadOut, {
-            options = {
-                New(LoadOut,
-                    {
-                        name       = "Patriot",
-                        options    = { munition60mmRocketHE },
-                        magazine   = {
-                            size   = 3,
-                            reload = 3.5,
-                        },
-                        randomizer = {
-                            tracerStrength = {
-                                min          = 95,
-                                max          = 135,
-                                distribution = "lowRand",
-                            },
-                            delay          = {
-                                min          = 95,
-                                max          = 150,
-                                distribution = "lowRand",
-                            },
-                            initialV       = {
-                                min          = 100,
-                                max          = 110,
-                                distribution = "lowRand",
-                            },
-                            data           = {
-                                thrust = {
-                                    min = 95,
-                                    max = 105,
-                                },
-                            },
-                        },
-                    }
-                ),
-            }
-        })
-    }
-)

```

---

# Migration Report: src\main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\main.lua
+++ patched/src\main.lua
@@ -1,12 +1,6 @@
-playerTransform = GetPlayerTransform()
+#version 2
 local D         = false
-ProBallistics   = {
-    debug = D,
-    disableSmoke = D,
-    disableFireball = D,
-    registeredWeapons = {},
-    registeredAmmo = {},
-}
+
 function ProBallistics:timeScaleRand()
     return
         ProBallistics.timeScaleInverse > 1 and not pRand(ProBallistics.timeScaleInverse)
@@ -180,12 +174,6 @@
     ProBallistics.extensionsInitialized = true
 end
 
-function update()
-    time = GetTime()
-    SetTimeScale(ProBallistics.timeScale)
-end
-
-newDT = true
 function globalInputs()
     _mx, _my = InputValue("mousedx"), InputValue("mousedy")
     if InputDown(ProBallistics.keyAutoAimShoot) then
@@ -262,39 +250,68 @@
     ProBallistics.defaultFov = GetInt("options.gfx.fov")
 end
 
-targetFPS = 60
-_mx, _my = InputValue("mousedx"), InputValue("mousedy")
-legacyTimeCorrection = 1
-timeCorrectedDrag = drag
---TODO: Refactor this mess
-function tick(dt)
-    initMod()
-    hideCommanderPlaneVox()
-    initExtensions()
-    ticks = ticks + 1
-    updateOptions()
-    globalInputs()
-    --SetEnvironmentProperty("fogParams", fogStart, fogEnd, fogAmount, fogExp)
-    playerTransform = GetPlayerTransform()
-    local rt        = dt / (1 / targetFPS)
-    local dtTarget  = 1 / targetFPS
-
-    if dt > dtTarget then
-        dt = dtTarget
-    end
-
-    dt                   = dt * ProBallistics.timeScaleCorrection * ProBallistics.timeScale
-    legacyTimeCorrection = dt * targetFPS
-    timeCorrectedDrag    = 1 - (1 - drag) * legacyTimeCorrection
-    globalDeltaTime      = dt
-
-    SetTimeScale(ProBallistics.timeScale)
-    Timer:tick(dt)
-    ProBallistics.forceAim       = false
-    ProBallistics.activeGuidance = false
-
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        initMod()
+        hideCommanderPlaneVox()
+        initExtensions()
+        ticks = ticks + 1
+        updateOptions()
+        globalInputs()
+        --SetEnvironmentProperty("fogParams", fogStart, fogEnd, fogAmount, fogExp)
+        playerTransform = GetPlayerTransform(playerId)
+        local rt        = dt / (1 / targetFPS)
+        local dtTarget  = 1 / targetFPS
+        if dt > dtTarget then
+            dt = dtTarget
+        end
+        dt                   = dt * ProBallistics.timeScaleCorrection * ProBallistics.timeScale
+        legacyTimeCorrection = dt * targetFPS
+        timeCorrectedDrag    = 1 - (1 - drag) * legacyTimeCorrection
+        globalDeltaTime      = dt
+        SetTimeScale(ProBallistics.timeScale)
+        Timer:tick(dt)
+        ProBallistics.forceAim       = false
+        ProBallistics.activeGuidance = false
+        ProBallistics.antiAir:process(dt)
+        ProBallistics.commanderPlane.autoAim:inputs()
+        ProBallistics.commanderPlane.autoPilot:inputs()
+        weaponTick(dt)
+        ProBallistics.ballistics:tick(dt)
+        ProBallistics.commanderPlane:tick(dt)
+        Sprites:tick(dt)
+        --ProBallistics.playerGroundScanner:scan()
+        local x, y, z = GetQuatEuler(playerTransform.rot)
+        --ProBallistics.playerGroundScanner:scan(VecAdd(Vec(0, 5, 0), playerTransform.pos), y)
+        --ProBallistics.ballistics.rocketTracker:process()
+        ProBallistics.commanderPlane.activeAim = false
+        if ProBallistics.visionMode == _lidarVisionMode then
+            ProBallistics.lidar:cameraDetect()
+        end
+        ProBallistics.effects.thermalSmoke = false
+        if ProBallistics.visionMode == _thermalVisionMode then
+            ThermalScanner:scan()
+            if ProBallistics.dedicatedThermalEffects then
+                ProBallistics.effects.thermalSmoke = true
+            end
+        end
+        CasingsHandler:tick(dt)
+        DebrisManager:tick(dt)
+        DelayedSmoke:tick(dt)
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        time = GetTime()
+        SetTimeScale(ProBallistics.timeScale)
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if ProBallistics.isExternalCamera then
-        SetString("game.player.tool", commanderPlaneTool)
+        SetString("game.player.tool", commanderPlaneTool, true)
         ProBallistics.activeGuidance = true
     elseif InputDown(ProBallistics.keyRemoteTargeting) then
         ProBallistics.commanderPlane.aimPos = GetAimPos()
@@ -326,22 +343,7 @@
             setFogParams(fogParams)
         end
     end
-
-    ProBallistics.antiAir:process(dt)
-    ProBallistics.commanderPlane.autoAim:inputs()
-    ProBallistics.commanderPlane.autoPilot:inputs()
-    weaponTick(dt)
-    ProBallistics.ballistics:tick(dt)
-    ProBallistics.commanderPlane:tick(dt)
-    Sprites:tick(dt)
-    --ProBallistics.playerGroundScanner:scan()
-    local x, y, z = GetQuatEuler(playerTransform.rot)
-
-    --ProBallistics.playerGroundScanner:scan(VecAdd(Vec(0, 5, 0), playerTransform.pos), y)
-    --ProBallistics.ballistics.rocketTracker:process()
-    ProBallistics.commanderPlane.activeAim = false
-
-    if GetString("game.player.tool") == commanderPlaneTool and GetPlayerVehicle() == 0 then
+    if GetString("game.player.tool") == commanderPlaneTool and GetPlayerVehicle(playerId) == 0 then
         ProBallistics.commanderPlaneEnabled = true
 
         if InputPressed(ProBallistics.keyExternalCamera) then
@@ -361,28 +363,9 @@
     else
         ProBallistics.commanderPlaneEnabled = false
     end
-
-
-    if ProBallistics.visionMode == _lidarVisionMode then
-        ProBallistics.lidar:cameraDetect()
-    end
-
-    ProBallistics.effects.thermalSmoke = false
-
-    if ProBallistics.visionMode == _thermalVisionMode then
-        ThermalScanner:scan()
-        if ProBallistics.dedicatedThermalEffects then
-            ProBallistics.effects.thermalSmoke = true
-        end
-    end
-
-    CasingsHandler:tick(dt)
-    DebrisManager:tick(dt)
-    DelayedSmoke:tick(dt)
-end
-
---TODO: REFACTOR this mess
-function draw()
+end
+
+function client.draw()
     if ProBallistics.debug then
         Debugger:draw()
     end
@@ -433,7 +416,7 @@
         or ProBallistics.camReserved
         or InputDown(ProBallistics.keyShowTrajectory)
     then
-        if ProBallistics.commanderPlane.recoilBlur > 0 then
+        if ProBallistics.commanderPlane.recoilBlur ~= 0 then
             UiBlur(ProBallistics.commanderPlane.recoilBlur)
         end
         DrawTrackerUi()
@@ -451,7 +434,7 @@
         --)
     end
     if not ProBallistics.camReserved then
-        if (ProBallistics.commanderPlaneEnabled and GetPlayerVehicle() == 0) or ProBallistics.forceHud then
+        if (ProBallistics.commanderPlaneEnabled and GetPlayerVehicle(playerId) == 0) or ProBallistics.forceHud then
             ProBallistics.commanderPlane:draw(ProBallistics.uiMode < _UiModerate)
         end
     end
@@ -467,3 +450,4 @@
 
     Info:drawUi()
 end
+

```

---

# Migration Report: src\materials.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\materials.lua
+++ patched/src\materials.lua
@@ -1,351 +1 @@
-defaultMaterial        = {
-    dust           = nil,
-    sparks         = 1,
-    keMin          = 200,
-    keRand         = 150,
-    holeMpl        = 1,
-    ricochetMpl    = 1,
-    indestructible = false
-}
-materialIndestructible = New(
-    defaultMaterial,
-    {
-        keMin          = 100,
-        keRand         = 500,
-        indestructible = true
-    }
-)
-materialAir            = New(
-    defaultMaterial,
-    {
-        keMin       = 100,
-        keRand      = 250,
-        sparks      = 2,
-        dust        = { lifeMin = 1, lifeMax = 4 },
-        holeMpl     = 2.5,
-        ricochetMpl = 0
-    }
-)
-materialNone           = New(
-    materialIndestructible,
-    {
-        sparks      = 3,
-        dust        = { lifeMin = 2, lifeMax = 5, n = 3 },
-        ricochetMpl = 2,
-    }
-)
-_materialEnergyShield  = "energyShield"
-materialEnergyShield   = New(
-    materialIndestructible,
-    {
-        sparks      = 3,
-        ricochetMpl = 2,
-    }
-)
-materialRock           = New(
-    materialIndestructible,
-    {
-        sparks      = 2,
-        dust        = { lifeMin = 2, lifeMax = 5, n = 4 },
-        ricochetMpl = 2,
-    }
-)
-materials              = {
-    air         = materialAir,
-    none        = materialNone,
-    rock        = materialRock,
-    plaster     = New(
-        defaultMaterial,
-        {
-            keMin       = 100,
-            keRand      = 250,
-            sparks      = 0.2,
-            dust        = { lifeMin = 1, lifeMax = 4 },
-            holeMpl     = 1.25,
-            ricochetMpl = 0.85
-        }
-    ),
-    metal       = New(
-        defaultMaterial,
-        {
-            keMin       = 500,
-            keRand      = 400,
-            sparks      = 3,
-            ricochetMpl = 1.85
-        }
-    ),
-    hardmetal   = New(
-        defaultMaterial,
-        {
-            keMin       = 750,
-            keRand      = 600,
-            sparks      = 4,
-            ricochetMpl = 2
-        }
-    ),
-    weakmetal   = New(
-        defaultMaterial,
-        {
-            keMin       = 400,
-            keRand      = 300,
-            sparks      = 2.5,
-            ricochetMpl = 1.5
-        }
-    ),
-    heavymetal  = New(
-        defaultMaterial,
-        {
-            keMin          = 750,
-            keRand         = 600,
-            sparks         = 4,
-            ricochetMpl    = 2,
-            indestructible = true,
-        }
-    ),
-    masonry     = New(
-        defaultMaterial,
-        {
-            keMin       = 300,
-            keRand      = 300,
-            sparks      = 0.35,
-            dust        = { lifeMin = 1, lifeMax = 5, n = 5 },
-            ricochetMpl = 1.3
-        }
-    ),
-    hardmasonry = New(
-        defaultMaterial,
-        {
-            keMin       = 450,
-            keRand      = 300,
-            sparks      = 0.5,
-            dust        = { lifeMin = 0.5, lifeMax = 3, n = 4 },
-            ricochetMpl = 1.5
-        }
-    ),
-    foliage     = New(
-        defaultMaterial,
-        {
-            keMin       = 50,
-            keRand      = 100,
-            sparks      = 0.05,
-            ricochetMpl = 0.1
-        }
-    ),
-    wood        = New(
-        defaultMaterial,
-        {
-            keMin       = 200,
-            keRand      = 200,
-            sparks      = 0.15,
-            ricochetMpl = 0.35
-        }
-    ),
-    plastic     = New(
-        defaultMaterial,
-        {
-            keMin       = 100,
-            keRand      = 100,
-            sparks      = 0.1,
-            ricochetMpl = 0.15
-        }
-    ),
-    dirt        = New(
-        defaultMaterial,
-        {
-            keMin   = 50,
-            keRand  = 500,
-            sparks  = 0.1,
-            holeMpl = 1.75,
-            dust    = { lifeMin = 0.5, lifeMax = 2 },
-        }
-    ),
-    concrete    = New(
-        defaultMaterial,
-        {
-            keMin       = 50,
-            keRand      = 500,
-            sparks      = 0.2,
-            dust        = { lifeMin = 1, lifeMax = 4, n = 6 },
-            ricochetMpl = 1.2
-        }
-    ),
-    glass       = New(
-        defaultMaterial,
-        {
-            keMin       = 50,
-            keRand      = 25,
-            sparks      = 0,
-            holeMpl     = 1.5,
-            ricochetMpl = .025
-        }
-    ),
-    grass       = New(
-        defaultMaterial,
-        {
-            keMin       = 50,
-            keRand      = 25,
-            sparks      = 0,
-            holeMpl     = 1,
-            ricochetMpl = 0.01
-        }
-    ),
-}
-defaultDebris          = {
-    threshold = 0,
-    event     = function(self, projectile, debris, hitProps, effects)
-    end
-}
-simpleDebris           = {
-    threshold = 1,
-    color     = nil,
-    alpha     = { 1, .5 },
-    mpl       = 10,
-    angle     = 45,
-    size      = .015,
-    gravity   = nil,
-    event     = function(self, projectile, debris, hitProps, effects)
-        if ProBallistics.effectsDebrisParticles then
-            SimpleParticle(
-                projectile.pos,
-                clamp(math.ceil(debris * self.mpl * ProBallistics.effectsDebrisParticlesMpl * .5), 10, 250),
-                self.life or 1,
-                math.sqrt(projectile.vDebris or VecLength(projectile.v) or hitProps.speed or 1),
-                VecRotateRandom(hitProps.normal, 50, .1), --TODO: mix  hitAngle into the picture
-                hitProps.color or self.color,
-                (hitProps.color[4] and { hitProps.color[4], hitProps.color[4] / 2 }) or self.alpha,
-                projectile.angle or self.angle,
-                self.gravity,
-                self.size,
-                self.emissive
-            )
-        end
-    end
-}
-energyDebris           = New(simpleDebris,
-    {
-        color    = { 0.25, 0.25, 1 },
-        alpha    = { 1.5, .5 },
-        gravity  = { 0, 0 },
-        emissive = { 2.5, .5 },
-        life     = 2,
-    },
-    {
-        event = function(self, projectile, debris, hitProps, effects)
-            if ProBallistics.effectsDebrisParticles then
-                SimpleParticle(
-                    projectile.pos,
-                    clamp(math.ceil(debris * self.mpl * ProBallistics.effectsDebrisParticlesMpl * .5), 10, 250),
-                    self.life or 1,
-                    math.sqrt(projectile.vDebris or VecLength(projectile.v) or hitProps.speed or 1) * .5,
-                    VecRotateRandom(hitProps.normal, 50, .1), --TODO: mix  hitAngle into the picture
-                    hitProps.color or self.color,
-                    (hitProps.color[4] and { hitProps.color[4], hitProps.color[4] / 2 }) or self.alpha,
-                    projectile.angle or self.angle,
-                    self.gravity,
-                    self.size,
-                    self.emissive
-                )
-            end
-        end
-    }
-)
-indestructibleDebris   = New(simpleDebris,
-    {
-        threshold = -1,
-        mpl       = 15,
-        size      = .015,
-        gravity   = { -60, -30 },
-        alpha     = { 1, .75 },
-    },
-    {
-        event = function(self, projectile, debris, hitProps, effects)
-            if effects and effects.explosion then
-                self.size = .04
-                --self.size = .15
-                self.life = 5
-                self.mpl = 25
-                debris = ((debris or 1) + (effects.explosion * 25)) * (effects.explosion + 1)
-            else
-                self.size = .015
-                self.life = 1
-                self.mpl = 15
-            end
-            simpleDebris.event(self, projectile, debris, hitProps, effects)
-        end
-    }
-)
-materialDebris         = {
-    glass                   = New(simpleDebris,
-        { mpl = 25, size = .01, alpha = { 1, .25 }, angle = 180, gravity = { -40, -5 } }),
-    rock                    = New(indestructibleDebris, { color = { .75, .75, .75 }, }),
-    none                    = New(indestructibleDebris, { color = { .231, .137, 0 }, }),
-    [_materialEnergyShield] = New(energyDebris, {}),
-    plaster                 = New(simpleDebris, { color = { .51, .51, .51 }, angle = 85 }),
-    masonry                 = New(simpleDebris, { color = { .51, .51, .51 }, angle = 75 }),
-    concrete                = New(simpleDebris, { color = { .65, .65, .65 }, angle = 70 }),
-    hardmasonry             = New(simpleDebris, { color = { .5, 0, 0 }, angle = 55 }),
-    foliage                 = New(simpleDebris, { color = { 0, .65, 0 }, angle = 89 }),
-    grass                   = New(simpleDebris, { color = { 0, .75, 0 }, angle = 89 }),
-    dirt                    = New(simpleDebris, { color = { .35, .18, 0 }, angle = 80 }),
-    wood                    = New(simpleDebris, { color = { .5, .25, 0 }, angle = 75 }),
-    plastic                 = New(simpleDebris, { mpl = 7.5, color = { .9, .9, .9 }, angle = 75 }),
-    weakmetal               = New(simpleDebris, { color = { .51, .51, .51 } }),
-    metal                   = New(simpleDebris, {
-        threshold = 4,
-        event     = function(self, projectile, debris, hitProps)
-            simpleDebris.event(self, projectile, debris / 2, hitProps)
-            local c = math.floor(debris / self.threshold) * math.random(2, 5) * ProBallistics.effectsDebrisParticlesMpl
-            for i = 1, c do
-                ProBallistics.ballistics:PrependShell(
-                    New(munitionDebrisMetal, {
-                        KE  = projectile.KE / c * math.random(50, 100) * 0.01,
-                        pos = projectile.pos,
-                        v   = VecScale(
-                            VecRotateRandom(
-                                hitProps.normal,
-                                900,
-                                0.1
-                            ),
-                            math.random(5, 25) * 0.01
-                        ),
-
-                    })
-                )
-            end
-            return true
-        end
-    }),
-    hardmetal               = New(simpleDebris, {
-        threshold = 3,
-        event     = function(self, projectile, debris, hitProps)
-            simpleDebris.event(self, projectile, debris / 2, hitProps)
-            local c = math.floor(debris / self.threshold) * math.random(2, 4) * ProBallistics.effectsDebrisParticlesMpl
-            for i = 1, c do
-                ProBallistics.ballistics:PrependShell(
-                    New(munitionDebrisMetal, {
-                        KE  = (projectile.KE or minKE) / c * math.random(50, 100) * 0.01,
-                        pos = projectile.pos,
-                        v   = VecScale(
-                            VecRotateRandom(
-                                hitProps.normal,
-                                900,
-                                0.1
-                            ),
-                            math.random(5, 25) * 0.01
-                        ),
-                    })
-                )
-            end
-            return true
-        end
-    })
-}
-CombustibleMaterials   = {
-    masonry = 2,
-    foliage = 3,
-    wood = 5,
-    plastic = 2,
-    grass = 2,
-    metal = 1,
-    weakmetal = 2,
-}
+#version 2

```

---

# Migration Report: src\milvision.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\milvision.lua
+++ patched/src\milvision.lua
@@ -1,14 +1,4 @@
-_fallback   = 'fallback'
-_turret     = 'turret'
-_projectile = 'projectile'
-MilVision   = {
-    projectile = nil,
-    turret     = nil,
-    fallback   = nil,
-    fov        = 60,
-    fovSpeed   = .25,
-    current    = _fallback,
-}
+#version 2
 function MilVision:turretCamera(dt)
     if self.turret == nil then
         return false
@@ -23,7 +13,7 @@
 
     local fovDiff = self.fov - targetFov
 
-    if fovDiff > 0 then
+    if fovDiff ~= 0 then
         self.fov = clamp(self.fov - self.fovSpeed, targetFov, self.fov)
     elseif fovDiff < 0 then
         self.fov = clamp(self.fov + self.fovSpeed, self.fov, targetFov)
@@ -126,3 +116,4 @@
         or self:spotterCamera(dt)
         or self:fallbackCamera(dt)
 end
+

```

---

# Migration Report: src\mod_options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\mod_options.lua
+++ patched/src\mod_options.lua
@@ -1,203 +1 @@
-_none = "none"
-extraKeys = ",./;'[]-="
---extraInputs = { "rmb" }
-_buttonSwitch = "__switchButton"
-_buttonCycle = "__cycleButton"
-RealInputLastPressedKey = function()
-    local keyPressed = InputLastPressedKey()
-    if string.len(keyPressed) > 0 then
-        return keyPressed
-    end
-
-    for i = 1, string.len(extraKeys), 1 do
-        keyPressed = string.sub(extraKeys, i, i)
-        if InputPressed(keyPressed) then
-            return keyPressed
-        end
-    end
-
-    if InputPressed("rmb") then
-        return "rmb"
-    end
-
-    return nil
-end
-
-ModOptions = {
-    initialized    = false,
-    buttonWidth    = 150,
-    buttonHeight   = 30,
-    init           = function(self, force)
-        if self.initialized and not force then
-            return
-        end
-
-        local defaultSettings = {
-            simApplyForce = true,
-            gameRedDotScale = 1,
-            gameRedDotFlicker = true,
-            gameRealismScale = 1,
-            gameScopeWindAid = false,
-            effectsRocketTrail = true,
-            effectsDebrisParticles = true,
-            effectsDebrisParticlesMpl = 1,
-            effectsMpl = 1,
-            barrelGlowMpl = 1,
-            randomWind = true,
-            effectsDebrisSmoke = false,
-            effectsApplyToVanilla = false,
-            simPrecisePenetration = false,
-            effectsVanillaShrapnel = true,
-            effectsPhysicalProjectiles = true,
-            ejectCasings = true,
-            casingSound = true,
-            soundVolume = 1,
-        }
-        for setting, key in pairs(defaultSettings) do
-            if force then
-                self:setSetting(setting, key)
-            else
-                self:defaultSetting(setting, key)
-            end
-        end
-
-        local defaultKeys = {
-            keyHelp                 = "f2",
-            keyOptions              = "f3",
-            keySwitchAmmo           = "x",
-            keySwitchWeaponSlot     = "z",
-            keyHoverLock            = "b",
-            keySpreadUp             = "8",
-            keySpreadDown           = "7",
-            keyElevationUp          = ".",
-            keyElevationDown        = ",",
-            keyVisionMode           = "n",
-            keyAutopilot            = "i",
-            keyEffectsUp            = "pgup",
-            keyEffectsDown          = "pgdown",
-            keyAntiAirPlace         = "home",
-            keyAntiAirClear         = "end",
-            keyAntiAirCamera        = "f7",
-            keyCycleOverlay         = "f8",
-            keyAutoAimShoot         = "y",
-            keyAutoAimMark          = "insert",
-            keyAutoAimReset         = "delete",
-            keyAutoAimMode          = "p",
-            keyAutoAimSpeedUp       = "0",
-            keyAutoAimSlowDown      = "9",
-            keyRemoteTargeting      = "alt",
-            keyShowTrajectory       = "o",
-            keyGimbalLock           = "l",
-            keyViewDistance         = "u",
-            keyProjectileCameraQuit = "f6",
-            keyForward              = "w",
-            keyBackward             = "s",
-            keyRight                = "a",
-            keyLeft                 = "d",
-            keyTiltRight            = "q",
-            keyTiltLeft             = "e",
-            keyUp                   = "space",
-            keyDown                 = "ctrl",
-            keyReload               = "r",
-            keyStance1              = "q",
-            keyStance2              = "e",
-            keyFireMode             = "v",
-            keyRedDot               = "b",
-            keySlowMo               = "t",
-            keySpotterCamera        = "k",
-            keySpotterNext          = "rightarrow",
-            keySpotterPrev          = "leftarrow",
-        }
-        for action, key in pairs(defaultKeys) do
-            if action ~= nil then
-                if force then
-                    self:setKeyBind(action, key)
-                else
-                    self:defaultKeyBind(action, key)
-                end
-            end
-        end
-
-        self.initialized = true
-    end,
-    defaultKeyBind = function(self, action, default)
-        if self:getKeyBind(action, _none) == _none then
-            self:setKeyBind(action, default)
-        end
-    end,
-    defaultSetting = function(self, name, default)
-        if self:getSetting(name, _none) == _none then
-            self:setSetting(name, default)
-        end
-    end,
-    prefix         = "savegame.mod.",
-    getOptionName  = function(self, path)
-        local name = path[1]
-        local first = true
-
-        for _, v in ipairs(path) do
-            if first then
-                first = false
-            else
-                name = name .. _delimiterInfix .. v
-            end
-        end
-
-        return self.prefix .. name
-    end,
-    getOption      = function(self, path, default)
-        local option = RegLoadSetting(self:getOptionName(path))
-
-        if option ~= nil then
-            return option
-        end
-
-        return default or _none
-    end,
-    setOption      = function(self, path, value)
-        return RegSaveSetting(self:getOptionName(path), value)
-    end,
-    getKeyBind     = function(self, action, default)
-        return self:getOption({ "keys", action }, default)
-    end,
-    setKeyBind     = function(self, action, value)
-        return self:setOption({ "keys", action }, value)
-    end,
-    getSetting     = function(self, name, default)
-        return self:getOption({ "settings", name }, default)
-    end,
-    setSetting     = function(self, name, value)
-        return self:setOption({ "settings", name }, value)
-    end,
-    switchButton   = function(self, name)
-        local val = self:getSetting(name, false)
-        --local val = false
-        local text = val and "On" or "Off"
-
-        if UiTextButton(text, self.buttonWidth, self.buttonHeight) then
-            DebugPrint(string.format("%s:%s", name, (not val) and "On" or "Off"))
-            self:setSetting(name, not val)
-        end
-    end,
-    cycleButton    = function(self, name, options, suffix)
-        local val = self:getSetting(name)
-        local text = val .. suffix
-
-        if UiTextButton(text, self.buttonWidth, self.buttonHeight) then
-            val = cycle(val, options)
-            DebugPrint(string.format("%s:%s", name, val))
-            self:setSetting(name, val)
-        end
-    end,
-    button         = function(self, name, options)
-        if options.type ~= nil then
-            if options.type == _buttonCycle then
-                return self:cycleButton(name, options.options, options.suffix)
-            elseif options.type == _buttonSwitch then
-                return self:switchButton(name)
-            end
-        else
-            return self:switchButton(name)
-        end
-    end,
-}
+#version 2

```

---

# Migration Report: src\obstacle-avoid.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\obstacle-avoid.lua
+++ patched/src\obstacle-avoid.lua
@@ -1,4 +1,4 @@
-ObstacleAvoid = {}
+#version 2
 function ObstacleAvoid:avoidDirections(pos, distance, directions)
     distance = distance or 10
     local avoidanceVector, invertDistance, hit, hitDistance, force = Vec(), 1 / distance
@@ -48,3 +48,4 @@
     )
     return avoidanceVector
 end
+

```

---

# Migration Report: src\particles.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\particles.lua
+++ patched/src\particles.lua
@@ -1,12 +1,4 @@
-smokeTiles          = { 0, 1, 3 }
-smokeDiverseTiles   = { 0, 1, 3, 5, 14 }
-dustTiles           = { 1, 3, 5 }
---dustTiles           = { 1, 5, 14 }
---sparkTiles          = { 1, 3, 14 }
-sparkTiles          = { 0, 3, 4 }
-fireTiles           = { 1, 5, 14 }
-simpleParticleTiles = { 1, 4, 6, 8 }
-
+#version 2
 function Smoke(pos, n, speed, lifeMax, dir, color, size)
     n       = math.max(1, n or 1)
     lifeMax = lifeMax or 7.5
@@ -478,12 +470,11 @@
     PointLight(pos, color[1], color[2], color[3], math.random(3, 9) * (strength or 1))
 end
 
-defaultSparkTile = 14
 function Sparks(pos, n, life, light, lightMax, dir, speed, size, angle, color)
     light    = light or 10
     lightMax = lightMax or light * 1.25
 
-    if light > 0 then
+    if light ~= 0 then
         color = color or { 0.72, 0.27, 0.05 }
         PointLight(pos, color[1], color[2], color[3], math.random(light * 10, lightMax * 10) * .1)
     end
@@ -709,7 +700,7 @@
         AddHeat(shape, pos, amount)
     end
 
-    if n > 0 then
+    if n ~= 0 then
         local hit, distance, hitNormal, hitShape, dir
 
         for i = 1, n do
@@ -723,7 +714,6 @@
     end
 end
 
-fragHitMaxDistance = 100
 function Shrapnel(projectile, min, max, spread, hitNormal, speed)
     local maxDistance = fragHitMaxDistance
     local fragCount   = math.min(math.random(min, max) * ProBallistics.effectsMpl, ProBallistics.maxShrapnel)
@@ -1065,10 +1055,6 @@
     )
 end
 
-explosionRealStrength = nil
-explosionNormal = nil
-explosionWrapper = false
-explosionRelatedProjectile = false
 function ProExplosionWrapper(projectile, pos, power, normal, hitProps)
     explosionRealStrength = power
     explosionNormal = normal
@@ -1312,8 +1298,6 @@
     explosionRelatedProjectile = false
 end
 
--- TODO: Move to separate file
-DelayedSmoke = New(TwoWayListWrapper)
 function _DelayedSmoke(delay, pos, lifeMin, lifeMax, n, size, speed, dir, color, maxSizeMpl, angle)
     DelayedSmoke:add({
         delay = delay,
@@ -1402,3 +1386,4 @@
         )
     end
 end
+

```

---

# Migration Report: src\phalanxPro.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\phalanxPro.lua
+++ patched/src\phalanxPro.lua
@@ -1,124 +1,4 @@
-munition12mmRPHE = New(
-    munition12mmAP, {},
-    {
-        name              = "12mm RP-HE",
-        delay             = shotDelay * 3,
-        initialV          = 1.5,
-        tracer            = -1,
-        tracerStrength    = 3,
-        tracerColor       = { 0.925, 0.2, 0.05 },
-        maxLifetime       = 15,
-        type              = 7,
-        tracerWidthMpl    = 5,
-        effects           = {
-            smoke  = 1,
-            sparks = {
-                n        = 15,
-                life     = 3,
-                light    = 150,
-                lightMax = 400,
-            },
-        },
-        effectsActive     = {},
-        specialEvent      = 0,
-        minTargetDistance = 2.5,
-        event             = function(self, dt, ballistics)
-            if
-                VecDistance(self.pos, self.target.pos) < self.minTargetDistance
-                or VecDistance(VecAdd(self.pos, VecScale(self.v, dt)), self.target.pos) < self.minTargetDistance
-                or VecDistance(VecAdd(self.target.pos, VecScale(self.target.v, dt)), self.pos) < self.minTargetDistance
-            then
-                if self.target.active then
-                    ballistics:projectileEffects(
-                        self.target,
-                        self.target.pos,
-                        self.target.effects,
-                        {
-                            material = materialAir,
-                            materialName = "air",
-                        }
-                    )
-                end
-                ballistics:projectileEffects(
-                    self,
-                    self.pos,
-                    self.effects,
-                    {
-                        material = materialAir,
-                        materialName = "air",
-                    }
-                )
-                self.target.active = false
-                self.target = nil
-
-                return false
-            end
-            if self.lifetime > self.timer and pRand(5) then
-                self.target = nil
-                --explode
-                ballistics:projectileEffects(
-                    self,
-                    self.pos,
-                    self.effects,
-                    {
-                        material = materialAir,
-                        materialName = "air",
-                    }
-                )
-                return false
-            end
-
-            return true
-        end
-    }
-)
-Phalanx12        = {
-    label          = "PX-12mm",
-    handle         = nil,
-    pos            = Vec(),
-    barrel         = {
-        length   = 1,
-        rotation = {
-            current    = Vec(1, 0, 0),
-            v          = 1.65,
-            resolution = 1.75,
-        },
-        spin     = {
-            val     = 0,
-            current = 0,
-            v       = 0,
-            vAcc    = 5000,
-            vMax    = 7200,
-            drag    = 0.99,
-            target  = 1980,
-            minimum = 1900,
-        },
-    },
-    target         = nil,
-    aimAt          = Vec(),
-    minDistance    = 100,
-    maxDistance    = 1500,
-    minAltitude    = 125,
-    rocketTracker  = nil,
-    maxTargetLocks = 6.5,
-    targetLock     = 1,
-    aimExtra       = New(AimExtra, { fixedElevation = .9 }),
-    weaponLoadOut  = New(WeaponLoadOut, {
-        options = {
-            New(LoadOut,
-                {
-                    name     = "PhalanX-12mm",
-                    options  = { munition12mmRPHE },
-                    magazine = {
-                        size   = 1500,
-                        reload = .5,
-                    },
-                }
-            ),
-        }
-    }),
-}
-
+#version 2
 function Phalanx12:rotate(dir, dt)
     local angle     = VecAngleBetween(self.barrel.rotation.current, dir)
     local speed     = self.barrel.rotation.v * dt
@@ -157,12 +37,6 @@
 function Phalanx12:New(rocketTracker, template)
     return New(self, template, { rocketTracker = rocketTracker })
 end
-
-PhalanxSystem = {
-    turretClass   = Phalanx12,
-    turrets       = New(TwoWayListWrapper),
-    rocketTracker = nil,
-}
 
 function PhalanxSystem:New(rocketTracker, template)
     return New(self, template, { rocketTracker = rocketTracker })
@@ -202,7 +76,7 @@
 
     --if self.target ~= nil then
     --    x, y, distance = UiWorldToPixel(self.target.pos)
-    --    if distance > 0 then
+    --    if distance ~= 0 then
     --        UiTranslate(x, y)
     --        UiColor(1, 0, 0, 1)
     --        UiRoundedRectOutline(24, 24, 6, 2)
@@ -211,7 +85,7 @@
 
     if self.aimAt ~= nil then
         x, y, distance = UiWorldToPixel(self.aimAt)
-        if distance > 0 then
+        if distance ~= 0 then
             UiTranslate(x, y)
             UiColor(1, 1, 0, .25)
             UiCircleOutline(15, 2)
@@ -220,7 +94,7 @@
 
     x, y, distance = UiWorldToPixel(self.pos)
 
-    if distance > 0 then
+    if distance ~= 0 then
         UiPush()
         UiTranslate(x, y)
         UiColor(1, 1, 1, 1)
@@ -236,7 +110,7 @@
     local barrelEnd = VecAdd(self.pos, VecScale(self.barrel.rotation.current, self.barrel.length))
     x, y, distance  = UiWorldToPixel(barrelEnd)
 
-    if distance > 0 then
+    if distance ~= 0 then
         UiTranslate(x, y)
         UiColor(1, 1, 1, 1)
         UiRotate(self.barrel.spin.val)
@@ -431,150 +305,6 @@
     self:draw()
 end
 
-munition30mmRPHE = New(
-    munition12mmRPHE,
-    {
-        name              = "30mm RP-HE",
-        caliber           = .03,
-        type              = 3,
-        initialV          = 1.75,
-        delay             = .075,
-        minTargetDistance = 7.5,
-        maxLifetime       = 12,
-        tracerStrength    = 4,
-        tracerColor       = { 0.9, 0.2, 0.05 },
-        streamFire        = -1,
-        effects           = {
-            smoke  = 1,
-            sparks = {
-                n        = 50,
-                life     = 4,
-                light    = 300,
-                lightMax = 600,
-            },
-        },
-    },
-    {}
-)
-munition45mmRPHE = New(
-    munition30mmRPHE,
-    {
-        name              = "45mm RP-HE",
-        caliber           = .045,
-        type              = 5,
-        initialV          = 1.75,
-        delay             = .25,
-        minTargetDistance = 10,
-        maxLifetime       = 10,
-        tracerStrength    = 5.5,
-        tracerColor       = { 0.9, 0.25, 0.05 },
-        streamFire        = -1,
-        fragDistance      = 100,
-        event             = function(self, dt, ballistics)
-            if
-                VecDistance(self.pos, self.target.pos) < self.fragDistance
-                or VecDistance(VecAdd(self.pos, VecScale(self.v, dt)), self.target.pos) < self.fragDistance
-                or VecDistance(VecAdd(self.target.pos, VecScale(self.target.v, dt)), self.pos) < self.fragDistance
-                or (self.lifetime > self.timer and pRand(3))
-            then
-                ballistics:projectileEffects(
-                    self,
-                    self.pos,
-                    self.effects,
-                    {
-                        material = materialAir,
-                        materialName = "air",
-                    }
-                )
-                local subProjectiles = ballistics:subProjectile(
-                    self, 20, 25, 15,
-                    New(munition12mmRPHE)
-                )
-                subProjectiles:iterate(
-                    function(item, parent)
-                        item.projectile.target = parent.target
-                        item.projectile.timer  = .25 * math.random(90, 115) * .01
-                    end,
-                    self
-                )
-
-                self.target = nil
-
-                return false
-            end
-
-            return true
-        end,
-        effects           = {
-            smoke  = 1,
-            sparks = {
-                n        = 50,
-                life     = 4,
-                light    = 400,
-                lightMax = 700,
-            },
-        },
-    },
-    {}
-)
-
-Phalanx30        = New(
-    Phalanx12,
-    {
-        label                 = "PX-30mm",
-        normal                = nil,
-        minDistance           = 500,
-        maxDistance           = 2250,
-        minAltitude           = 50,
-        maxTargetLocks        = 5,
-        targetLock            = 1.5,
-        aimExtra              = New(AimExtra),
-        distanceElevationRate = .0075,
-        barrel                = {
-            length   = 1.25,
-            rotation = {
-                current    = Vec(1, 0, 0),
-                v          = 1.55,
-                resolution = 1.5,
-            },
-            spin     = {
-                val     = 0,
-                current = 0,
-                v       = 0,
-                vAcc    = 1500,
-                vMax    = 4000,
-                drag    = 0.995,
-                target  = 550,
-                minimum = 450,
-            },
-        },
-        weaponLoadOut         = New(WeaponLoadOut, {
-            options = {
-                New(LoadOut,
-                    {
-                        name       = "PhalanX-30mm",
-                        options    = { munition30mmRPHE },
-                        magazine   = {
-                            size   = 8,
-                            reload = .35,
-                        },
-                        randomizer = {
-                            tracerStrength = {
-                                min = 95,
-                                max = 125,
-                            },
-                            delay          = {
-                                min          = 95,
-                                max          = 125,
-                                distribution = "lowRand",
-                            },
-                        },
-                    }
-                ),
-            }
-        })
-    }
-)
 function Phalanx30:shootEffects(shell)
     local barrelEnd    = VecAdd(self.pos, VecScale(self.barrel.rotation.current, self.barrel.length))
     local barrelEndFar = VecAdd(self.pos, VecScale(self.barrel.rotation.current, self.barrel.length + .15))
@@ -592,108 +322,3 @@
     end
 end
 
-Phalanx45 = New(
-    Phalanx30,
-    {
-        label                 = "PX-45mm",
-        normal                = nil,
-        minDistance           = 150,
-        maxDistance           = 1000,
-        minAltitude           = 50,
-        maxTargetLocks        = 6,
-        targetLock            = 1.75,
-        aimExtra              = New(AimExtra),
-        distanceElevationRate = .006,
-        barrel                = {
-            length   = 1.25,
-            rotation = {
-                current    = Vec(1, 0, 0),
-                v          = 1.65,
-                resolution = 1.5,
-            },
-            spin     = {
-                val     = 0,
-                current = 0,
-                v       = 0,
-                vAcc    = 1500,
-                vMax    = 4000,
-                drag    = 0.995,
-                target  = 450,
-                minimum = 400,
-            },
-        },
-        weaponLoadOut         = New(WeaponLoadOut, {
-            options = {
-                New(LoadOut,
-                    {
-                        name       = "PhalanX-45mm",
-                        options    = { munition45mmRPHE },
-                        magazine   = {
-                            size   = 5,
-                            reload = 1,
-                        },
-                        randomizer = {
-                            tracerStrength = {
-                                min = 95,
-                                max = 125,
-                            },
-                            delay          = {
-                                min          = 95,
-                                max          = 115,
-                                distribution = "lowRand",
-                            },
-                        },
-                    }
-                ),
-            }
-        })
-    }
-)
-
-
-PhalanxCIWS        = New(
-    Phalanx12,
-    {
-        label                 = "PX-CIWS-12mm",
-        normal                = nil,
-        minDistance           = 50,
-        maxDistance           = 300,
-        minAltitude           = 25,
-        maxTargetLocks        = 7.5,
-        targetLock            = 1,
-        aimExtra              = New(AimExtra),
-        distanceElevationRate = .0075,
-        barrel                = {
-            length   = 1,
-            rotation = {
-                current    = Vec(1, 0, 0),
-                v          = 1.75,
-                resolution = 1.5,
-            },
-            spin     = {
-                val     = 0,
-                current = 0,
-                v       = 0,
-                vAcc    = 3500,
-                vMax    = 6000,
-                drag    = 0.995,
-                target  = 550,
-                minimum = 450,
-            },
-        },
-      weaponLoadOut  = New(WeaponLoadOut, {
-              options = {
-                  New(LoadOut,
-                      {
-                          name     = "CIWS-12mm",
-                          options  = { munition12mmRPHE },
-                          magazine = {
-                              size   = 1500,
-                              reload = .5,
-                          },
-                      }
-                  ),
-              }
-          }),
-    }
-)
```

---

# Migration Report: src\plane.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\plane.lua
+++ patched/src\plane.lua
@@ -1,48 +1,4 @@
-AimExtra = {
-    fixedElevation = 0,
-    elevation      = 0,
-    windCorrection = 0,
-    inertia        = Vec(),
-}
-Plane    = {
-    pos                 = Vec(0, 0, 100),
-    v                   = Vec(),
-    vAcc                = Vec(),
-    acceleration        = Vec(15, 10, 15),
-    hoverShake          = Vec(),
-    maxAcc              = 30,
-    drag                = 0.9,
-    rot                 = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0)),
-    barrel              = {
-        rot = Quat()
-    },
-    aim                 = {
-        rot = Quat()
-    },
-    aimPos              = Vec(),
-    aimSpread           = 1,
-    elevationProps      = {
-        min  = .1,
-        max  = 20,
-        tick = 0.025
-    },
-    windCorrectionProps = {
-        min  = -10,
-        max  = 10,
-        tick = 0.025
-    },
-    autoAim             = nil,
-    hoverLock           = false,
-    autoPilot           = nil,
-    weaponLoadOut       = nil,
-    aimExtra            = New(AimExtra, { elevation = 1, fixedElevation = 4 }),
-    aimVehicle          = 0,
-    recoilBlur          = 0,
-    recoilRot           = Quat(),
-    cameraRot           = Quat(),
-    groundScanner       = nil,
-    avoidObstacles       = true,
-}
+#version 2
 function Plane:inputs()
     if InputDown("usetool") then
         self:shoot()
@@ -177,7 +133,7 @@
     --   )
     self.activeAim = true
 
-    SetPlayerTransform(GetPlayerTransform())
+    SetPlayerTransform(playerId, GetPlayerTransform(playerId))
     SoundManager:engine("commanderPlane", self.pos)
 end
 
@@ -310,7 +266,7 @@
     local aimPos = self.aimPos
     if ProBallistics.aimLock or ProBallistics.targetLock then
         local _, _, rz = GetQuatEuler(self.aim.rot)
-        if ProBallistics.targetLock and self.aimVehicle > 0 then
+        if ProBallistics.targetLock and self.aimVehicle ~= 0 then
             aimPos = TransformToParentPoint(GetEntityTransform(self.aimVehicle), self.aimVehicleOffset)
         end
         self.aim.rot = QuatDir(VecSub(aimPos, self.aim.pos))
@@ -348,7 +304,7 @@
             )
         end
     end
-    if self.aimVehicle > 0 then
+    if self.aimVehicle ~= 0 then
         self.aimVehicleOffset = TransformToLocalPoint(GetEntityTransform(self.aimVehicle), self.aimPos)
     end
     --DebugWatch("d.Aim", {
@@ -383,3 +339,4 @@
         --)
     end
 end
+

```

---

# Migration Report: src\randomizer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\randomizer.lua
+++ patched/src\randomizer.lua
@@ -1,9 +1,4 @@
-Randomizer = {
-    func = {}
-}
-_distributionRand = "rand"
-_distributionLowRand = "lowRand"
-_distributionHighRand = "highRand"
+#version 2
 function Randomizer.func.rand(min, max, n)
     return math.random(min, max)
 end
@@ -58,3 +53,4 @@
         end
     end
 end
+

```

---

# Migration Report: src\rnd.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\rnd.lua
+++ patched/src\rnd.lua
@@ -1,19 +1,4 @@
--- R&D
-munitionTest = New(munition12mmFMJ, {
-    name          = "Test munition",
-    rounds        = 1,
-    burst         = 1,
-    delay         = 0.25,
-    --proxyDistance = 10,
-    ricochet      = 1,
-    proxyEvent    = function(projectile, dt)
-        --local tile=7
-        --_SparksTest(projectile.pos, 10, 5, tile, 10, 2, { .5, .5, .5 }, 1)
-        _Fire(projectile.pos, 2, 10, 10, 1, 10, VecNormalize(projectile.v))
-        return false
-    end
-})
-
+#version 2
 function interceptA(posA, posB, velocityA, velocityB)
     local aimAt    = posB
     local distance = VecDistance(posA, aimAt)
@@ -46,6 +31,7 @@
 
     return aimAt, newTimeToTarget
 end
+
 function interceptB(posA, posB, velocityA, velocityB)
     local R = VecSub(posB, posA)
 
@@ -73,11 +59,11 @@
         local t1        = (-b + sqrt_disc) / (2 * a)
         local t2        = (-b - sqrt_disc) / (2 * a)
 
-        if t1 > 0 and t2 > 0 then
+        if t1 > 0 and t2 ~= 0 then
             t = math.min(t1, t2)
-        elseif t1 > 0 then
+        elseif t1 ~= 0 then
             t = t1
-        elseif t2 > 0 then
+        elseif t2 ~= 0 then
             t = t2
         else
             return nil
@@ -87,4 +73,5 @@
     local meetPos = VecAdd(posB, VecScale(velocityB, t))
 
     return meetPos, t
-end+end
+

```

---

# Migration Report: src\sdk\base.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\sdk\base.lua
+++ patched/src\sdk\base.lua
@@ -1,3 +1,4 @@
+#version 2
 function isAssociative(t)
     for k, _ in pairs(t) do
         if type(k) ~= "number" then
@@ -55,6 +56,7 @@
     end
     ClearKey(path)
 end
+
 function RegClearSetting(path)
     for _, v in pairs(ListKeys(path)) do
         RegClearSetting(path .. _delimiterInfix .. v)
@@ -82,37 +84,37 @@
     RegClear(path .. "-")
     local valueType = type(value)
     if valueType == "number" then
-        SetString(path .. "_", _number)
-        SetString(path, value)
+        SetString(path .. "_", _number, true)
+        SetString(path, value, true)
     elseif valueType == "string" then
-        SetString(path .. "_", _string)
-        SetString(path, value)
+        SetString(path .. "_", _string, true)
+        SetString(path, value, true)
     elseif valueType == "table" then
         if isVec(value) then
-            SetString(path .. "_", _vec)
+            SetString(path .. "_", _vec, true)
             SetColor(path, value[1], value[2], value[3])
             return value
         elseif isQuat(value) then
-            SetString(path .. "_", _quat)
+            SetString(path .. "_", _quat, true)
             SetColor(path, value[1], value[2], value[3], value[4])
             return value
         elseif isTrans(value) then
-            SetString(path .. "_", _trans)
+            SetString(path .. "_", _trans, true)
         else
-            SetString(path .. "_", _table)
+            SetString(path .. "_", _table, true)
         end
 
         for k, v in pairs(value) do
             local safeK = StringSafe(k)
             RegSave(path .. "." .. safeK, v)
             if not (type(k) == "number") then
-                SetString(path .. "." .. safeK .. "-", k)
+                SetString(path .. "." .. safeK .. "-", k, true)
             end
         end
     elseif value == false then
-        SetString(path .. "_", _falseValue)
+        SetString(path .. "_", _falseValue, true)
     elseif value == true then
-        SetString(path .. "_", _trueValue)
+        SetString(path .. "_", _trueValue, true)
     end
 
     return value
@@ -171,37 +173,37 @@
     RegClearSetting(path .. _indexSuffix)
     local valueType = type(value)
     if valueType == "number" then
-        SetString(path .. _typeSuffix, _number)
-        SetString(path, value)
+        SetString(path .. _typeSuffix, _number, true)
+        SetString(path, value, true)
     elseif valueType == "string" then
-        SetString(path .. _typeSuffix, _string)
-        SetString(path, value)
+        SetString(path .. _typeSuffix, _string, true)
+        SetString(path, value, true)
     elseif valueType == "table" then
         if isVec(value) then
-            SetString(path .. _typeSuffix, _vec)
+            SetString(path .. _typeSuffix, _vec, true)
             SetColor(path, value[1], value[2], value[3])
             return value
         elseif isQuat(value) then
-            SetString(path .. _typeSuffix, _quat)
+            SetString(path .. _typeSuffix, _quat, true)
             SetColor(path, value[1], value[2], value[3], value[4])
             return value
         elseif isTrans(value) then
-            SetString(path .. _typeSuffix, _trans)
+            SetString(path .. _typeSuffix, _trans, true)
         else
-            SetString(path .. _typeSuffix, _table)
+            SetString(path .. _typeSuffix, _table, true)
         end
 
         for k, v in pairs(value) do
             local safeK = StringSafe(k)
             RegSave(path .. _delimiterInfix .. safeK, v)
             if not (type(k) == "number") then
-                SetString(path .. _delimiterInfix .. safeK .. _indexSuffix, k)
+                SetString(path .. _delimiterInfix .. safeK .. _indexSuffix, k, true)
             end
         end
     elseif value == false then
-        SetString(path .. _typeSuffix, _falseValue)
+        SetString(path .. _typeSuffix, _falseValue, true)
     elseif value == true then
-        SetString(path .. _typeSuffix, _trueValue)
+        SetString(path .. _typeSuffix, _trueValue, true)
     end
 
     return value
@@ -252,4 +254,5 @@
     end
 
     return nil
-end+end
+

```

---

# Migration Report: src\sdk\commands.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\sdk\commands.lua
+++ patched/src\sdk\commands.lua
@@ -1,8 +1,8 @@
-cmdC = 0
-cmdId = math.random(1, 100000) .. "_" .. math.random(1, 100000)
+#version 2
 function PBCommand(name, args)
     cmdC = cmdC + 1
     local argsPath = commandsRegPath .. "." .. cmdId .. "_" .. cmdC
     RegSave(argsPath, args)
     TriggerEvent(_pbCmd, name .. " " .. argsPath)
 end
+

```

---

# Migration Report: src\sdk\symbols.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\sdk\symbols.lua
+++ patched/src\sdk\symbols.lua
@@ -1,86 +1 @@
-handHeldWeaponsRegPath  = "level.ProBallistics.weapons.handheld"
-commandsRegPath         = "level.ProBallistics.commands"
-
-_nilValue               = '_nil_'
-_falseValue             = '_false_'
-_trueValue              = '_true_'
-_zeroValue              = '_zero_'
-_number                 = "_number_"
-_string                 = "_string_"
-_boolean                = "_boolean_"
-_table                  = "_table_"
-_vec                    = "_vec_"
-_quat                   = "_quat_"
-_trans                  = "_trans_"
-_dot                    = "_dot_"
-
-_typeSuffix             = "_type"
-_typeSuffixLength       = string.len(_typeSuffix)
-
-_indexSuffix            = "_index"
-_delimiterInfix         = "_delim_"
-
-_aimPoseShoulder        = "shoulder"
-_aimPoseHip             = "hip"
-_aimPoseIron            = "iron"
-_aimPoseIronSideways    = "iron-sideways"
-_aimPoseTest            = "test"
-
-_munition12mmFMJ        = "12.7mm FMJ"
-_munition12mmAP         = "12.7mm AP"
-_munition12mmInc        = "12.7mm Incendiary"
-
-_munition5_56mmFMJ      = "5.56mm FMJ"
-_munition5_56mmFMJT     = "5.56mm FMJ Tracer"
-_munition5_56mmAP       = "5.56mm AP"
-_munition5_56mmFMJ_EPR  = "5.56mm FMJ EPR"
-_munition5_56mmFMJT_EPR = "5.56mm FMJ Tracer EPR"
-_munition5_56mmAP_EPR   = "5.56mm AP EPR"
-_munition5_56mmFMJ_CTR  = "5.56mm FMJ CTR"
-_munition5_56mmFMJT_CTR = "5.56mm FMJ Tracer CTR"
-_munition5_56mmAP_CTR   = "5.56mm AP CTR"
-_munition50BMG          = ".50 BMG"
-_munition50BMG_AP       = ".50 BMG AP"
-_munition50BMG_INC      = ".50 BMG Incendiary"
-_munition50BMG_AB       = ".50 BMG Air Burst"
-_munition50BMG_RB       = ".50 BMG Room Buster"
-_munitionM6HEP          = "M6 HEP"
-_munitionM6HEAT         = "M6 HEAT"
-_munition12gauge        = "12 Gauge"
-_munitionBirdShot       = "Bird Shot"
-_munitionSlug           = "Slug"
-_munition7_62mmFMJ      = "7.62mm FMJ"
-_munition7_62mmFMJT     = "7.62mm FMJ Tracer"
-_munition7_62mmAP       = "7.62mm AP"
-
-_munition9mmFMJ         = "9mm FMJ"
-_munition9mmHP          = "9mm HP"
-_munition9mmJHP         = "9mm JHP"
-_munition9mmAP          = "9mm AP"
-
-_munition7_62mmFMJ_Fast = "7.62mm FMJ Fast"
-_munition7_62mmAP_Fast  = "7.62mm AP Fast"
-
-_munitionPlasma100      = "Plasma 100KJ"
-_munitionPlasma200      = "Plasma 200KJ"
-_munitionPlasma500      = "Plasma 500KJ"
-_munitionPlasma750      = "Plasma 750KJ"
-
-_munitionClassKinetic   = "kinetic"
-_munitionClassEnergy    = "energy"
-
-
-_handHeldWeapon           = "HandHeld"
-_handHeldWeaponSciFi      = "HandHeldSciFi"
-_handHeldWeaponRotary     = "HandHeldRotary"
-
-_debrisMetal              = "Debris Metal"
-_shrapnelHeavy            = "Shrapnel Heavy"
-_shrapnelHeavyIncendiary  = "Shrapnel Heavy Incendiary"
-_shrapnelAP               = "Shrapnel AP"
-
-_projectile               = "__projectile"
-
-_pbCmd                    = "pbCmd"
-_pbCmdSubProjectiles      = "subProjectiles"
-_pbCmdSubProjectilesMixed = "subProjectilesMixed"
+#version 2

```

---

# Migration Report: src\sdk\weapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\sdk\weapons.lua
+++ patched/src\sdk\weapons.lua
@@ -1,62 +1,10 @@
-sampleWeaponSetup = {
-    aimPoses     = {
-        _aimPoseShoulder,
-        _aimPoseIronSideways,
-        _aimPoseIron,
-    },
-    aimOffset    = { x = 0, y = .2, z = 0, tilt = 0, fov = 90 },
-    aimOffsets   = {
-        [_aimPoseShoulder] = { x = -.05, y = .15, z = -.05, tilt = 0, fov = 90 },
-        [_aimPoseIron] = { x = -.325, y = .175, z = -.15, tilt = 0, fov = 65 },
-        [_aimPoseIronSideways] = { x = -.5, y = -.245, z = -.15, tilt = 55, fov = 50 },
-    },
-    fireModes    = { 0, 3, 5 },
-    fireMode     = 3,
-    elements     = {
-        barrel = {
-            zActionOffset = .05,
-            zActionDelay = .2,
-            transform = Transform(
-                Vec(0.3, -.4, -.85),
-                QuatEuler(-90, 0, 0)
-            ),
-        },
-        bolt = {
-            zActionOffset = .1,
-            transform = Transform(
-                Vec(0.3, -.45, -.55),
-                QuatEuler(-90, 0, 0)
-            ),
-        },
-        mode = {
-            transform = Transform(
-                Vec(0.2, -.45, -.25),
-                QuatEuler(-90, 0, 0)
-            ),
-        }
-    },
-    barrelOffset = Vec(0.325, -0.375, -1.16),
-    ammo         = {
-        ["munition5_56mmFMJ"] = {
-            size   = 30,
-            reload = 2,
-        },
-        ["munition5_56mmFMJT"] = {
-            size   = 30,
-            reload = 2,
-        },
-        ["munition5_56mmAP"] = {
-            size   = 30,
-            reload = 2,
-        },
-    },
-}
-
+#version 2
 function registerHandHeldWeapon(id, name, voxPath, group, weaponSetup)
     RegisterTool(id, "[PB]" .. name, voxPath, group)
-    SetBool(string.format("game.tool.%s.enabled", id), true)
+    SetBool(string.format("game.tool.%s.enabled", id), true, true)
     weaponSetup.id = id
     weaponSetup.name = name
     local path = handHeldWeaponsRegPath .. "." .. id
     RegSave(path, weaponSetup)
 end
+

```

---

# Migration Report: src\sounds.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\sounds.lua
+++ patched/src\sounds.lua
@@ -1,362 +1,4 @@
-Sound        = {
-    handle  = nil,
-    volume  = 1,
-    loop    = false,
-    dynamic = false
-}
-SoundManager = {
-    hitMaxDistance = 35,
-    soundVolume    = ModOptions:getSetting("soundVolume", 1),
-    shooting       = {
-        New(Sound, {
-            loop   = true,
-            volume = 0.75,
-            handle = LoadLoop("MOD/snd/shooting/minigun-107652.ogg")
-        }),
-        New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/shooting/auto-machine-gun-84533.ogg"),
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/shooting/single-gunshot-54-40780.ogg"),
-            volume = 0.5,
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/shooting/pvc-rocket-cannon_2-106658.ogg"),
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/shooting/shot-rifle-39-mm-37542.ogg"),
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/shooting/cas-missile-launching-with-some-reverb-66630.ogg"),
-            volume = 0.5,
-        }),
-        New(Sound, {
-            loop   = true,
-            volume = 0.25,
-            handle = LoadLoop("MOD/snd/shooting/minigun-107652.ogg")
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/shooting/pvc-rocket-cannon_2-106658.ogg"),
-            volume = 0.75,
-        }),
-    },
-    shots          = {
-        shotgun =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/spas-12-89800.ogg"),
-            }),
-        laser1 =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/energy/energy-weapon-90369.ogg"),
-            }),
-        laser2 =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/energy/laser_gun_sound-40813.ogg"),
-            }),
-        laser_medium =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/energy/laser-shot-92247.ogg"),
-            }),
-        laser_big1 =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/energy/071180_laser-gun-cannon-shotmp3-88117.ogg"),
-            }),
-        laser_big2 =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/energy/lazercannon-37980.ogg"),
-            }),
-        pistol_test =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/9mm-pistol-shot-6349.ogg"),
-            }),
-        sniper_bmg =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/sniper-rifle-firing-2-39885.ogg"),
-            }),
-        sniper =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/sniper-rifle-firing-shot-1-39789.ogg"),
-            }),
-
-        lmg =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/single-gunshot-54-40780.ogg"),
-                volume = .9
-            }),
-        pistol =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/single-gunshot-53-101733.ogg"),
-                volume = .75,
-                pitch  = 1.2,
-            }),
-        rifle1 =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/single-gunshot-54-40780.ogg"),
-                volume = .75,
-                pitch  = 1.1
-            }),
-        smg =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/single-gunshot-53-101733.ogg"),
-                volume = .85,
-                pitch  = 1.05,
-            }),
-        canon =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/shot-rifle-39-mm-37542.ogg"),
-            }),
-        canon2 =
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/shooting/gun-shot-1-176892"),
-            }),
-        minigunLoud = New(Sound, {
-            loop   = true,
-            volume = 1.25,
-            handle = LoadLoop("MOD/snd/shooting/minigun-107652.ogg")
-        }),
-    },
-    hits           = {
-        metal = {
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/metal/080887_bullet-39734.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/metal/080888_bullet-39736.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/metal/080889_bullet-39733.ogg"),
-            }),
-        },
-        other = {
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/other/078310_bullet-39808.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/other/080882_bullet-39720.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/other/080885_bullet-39809.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/other/080890_bullet-39507.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/other/080894_bullet-39807.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/other/080998_bullet-hit-39870.ogg"),
-            }),
-            New(Sound, {
-                loop   = false,
-                handle = LoadSound("MOD/snd/bullet/other/080884_bullet-hit-39872.ogg"),
-            }),
-
-        },
-    },
-    explosions     = {
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/gun-firing-from-a-distance-12-39881.ogg"),
-            volume = 2
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/gun-shots-from-a-distance-10-39761.ogg"),
-            volume = 3
-        }),
-        --New(Sound, {
-        --    loop   = false,
-        --    handle = LoadSound("MOD/snd/explosion/gun-shots-from-a-distance-13-39758.ogg"),
-        --    volume = 2.5
-        --}),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/gun-shots-from-a-distance-13-96423.ogg"),
-            volume = 2
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/sniper-rifle-5989.ogg"),
-            volume = 3
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/gun-shots-from-a-long-distance-9-39725.ogg"),
-            volume = 3
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/gun-shots-from-a-long-distance-9-39725.ogg"),
-            volume = 3
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/echoing-explosion-196259.ogg"),
-            volume = 3.25
-        }),
-        New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/explosion/realistic-gun-fire-100696.ogg"),
-            volume = 2.75
-        }),
-    },
-    engines        = {
-        rocket         = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/rocket/rocket-loop-99748-seamless.ogg"),
-            volume = 4
-        }),
-        rocketStart    = New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/shooting/cas-missile-launching-with-some-reverb-66630.ogg"),
-            volume = 0.5,
-        }),
-        commanderPlane = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/engines-and-machines/airplane-atmos-22955.ogg"),
-        }),
-        spinIdle       = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/engines-and-machines/harddrives-spinning-73174-seamless.ogg", 100),
-            volume = 7.5
-        }),
-        spinUp         = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/engines-and-machines/noisy-laptop-fan-97958-seamless1.ogg"),
-        }),
-        laser1         = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/effects/ecu-a-xx92-18908.ogg"),
-            volume = 1
-        }),
-        laser2         = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/effects/ecu-a-xx132-18641.ogg"),
-            volume = 2
-        }),
-        laser3         = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/effects/ecu-a-xx138-18635.ogg"),
-            volume = 5
-        }),
-    },
-    effects        = {
-        switch = New(Sound, {
-            loop   = false,
-            handle = LoadSound("MOD/snd/effects/click-1-94229.ogg"),
-            volume = 15
-        }),
-        laser1 = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/effects/ecu-a-xx92-18908.ogg"),
-            volume = 1
-        }),
-        laser2 = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/effects/ecu-a-xx132-18641.ogg"),
-            volume = 1
-        }),
-        laser3 = New(Sound, {
-            loop   = true,
-            handle = LoadLoop("MOD/snd/effects/ecu-a-xx138-18635.ogg"),
-            volume = 3,
-            pitch  = .5
-        }),
-        casing =
-        {
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing0.ogg", 7.5),
-            --}),
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing1.ogg", 7.5),
-            --}),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing2.ogg", 7.5),
-            }),
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing3.ogg", 7.5),
-            --}),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing4.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing5.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing6.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing7.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing8.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing9.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing10.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing12.ogg", 7.5),
-            }),
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing12.ogg", 7.5),
-            --}),
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing13.ogg", 7.5),
-            --}),
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing14.ogg", 7.5),
-            --}),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing15.ogg", 7.5),
-            }),
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing16.ogg", 7.5),
-            --}),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing17.ogg", 7.5),
-            }),
-            New(Sound, {
-                handle = LoadSound("MOD/snd/effects/casing/casing18.ogg", 7.5),
-            }),
-            --New(Sound, {
-            --    handle = LoadSound("MOD/snd/effects/casing/casing19.ogg", 7.5),
-            --}),
-        }
-    },
-}
+#version 2
 function SoundManager:playSound(sound, soundPos, vol, pitch)
     if sound.handle == nil then -- many sounds
         sound = randA(sound)
@@ -434,3 +76,4 @@
         self:playSound(sound, soundPos, math.min(12, 2.5 * (1 + power * .5)))
     end
 end
+

```

---

# Migration Report: src\spotter.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\spotter.lua
+++ patched/src\spotter.lua
@@ -1,84 +1 @@
-Spotter = {
-    enabled = false,
-    cameras = New(TwoWayListWrapper),
-    lastCamera = nil,
-    camera = function(self, smooth, startingFov)
-        if not self.enabled then
-            return false
-        end
-        if self.cameras.current ~= nil then
-            if smooth ~= nil and smooth > 0 then
-                return self:smoothCamera(self.cameras.current, smooth, startingFov)
-            else
-                return self.cameras.current
-            end
-        end
-
-        return false
-    end,
-    smoothCamera = function(self, camera, smooth, startingFov)
-        if self.lastCamera ~= nil then
-            self.lastCamera.transform.pos = FluidChange:tween(
-                "smoothCameraPos",
-                camera.transform.pos,
-                smooth,
-                self.lastCamera.transform.pos
-            )
-            self.lastCamera.fov = FluidChange:tween(
-                "smoothCameraFov",
-                camera.fov,
-                smooth,
-                self.lastCamera.fov
-            )
-            self.lastCamera.transform.rot =
-                QuatSlerp(
-                    self.lastCamera.transform.rot,
-                    camera.transform.rot,
-                    smooth * ProBallistics.timeScale * .5
-                )
-        else
-            FluidChange:clear("smoothCameraPos")
-            FluidChange:clear("smoothCameraFov")
-            self.lastCamera = {
-                fov = startingFov or 90,
-                transform = GetCameraTransform(),
-            }
-        end
-
-        return self.lastCamera
-    end,
-    inputs = function(self, context)
-        if InputDown("shift") then
-            if InputPressed(ProBallistics.keySpotterPrev) then
-                self.cameras:prev(true)
-            elseif InputPressed(ProBallistics.keySpotterNext) then
-                self.cameras:next(true)
-            end
-        end
-        if InputPressed(ProBallistics.keySpotterCamera) then
-            self.lastCamera = nil
-            if InputDown("shift") then
-                if InputDown("alt") then
-                    self.enabled = false
-                    self.cameras:flush()
-                else
-                    self.enabled = not self.enabled
-                end
-            else
-                if InputDown("alt") then
-                    self.cameras:remove()
-                    if self.cameras.count == 0 then
-                        self.enabled = false
-                    end
-                elseif not self.enabled then
-                    self.cameras:add(
-                        {
-                            fov = context.fov or ProBallistics.defaultFov,
-                            transform = GetCameraTransform(),
-                        }
-                    )
-                end
-            end
-        end
-    end,
-}
+#version 2

```

---

# Migration Report: src\sprites.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\sprites.lua
+++ patched/src\sprites.lua
@@ -1,321 +1,5 @@
-RenderSlowMoShield = function(self, projectile, dt, a)
-    local n = 1
-    if projectile.caliber > .02 then
-        n = n + 1
-        if projectile.caliber > .1 then
-            n = n + 1
-            if projectile.caliber > .15 then
-                n = n + 1
-            end
-        end
-    end
-    local dir = VecNormalize(projectile.v)
-    local pos = VecAdd(projectile.pos, VecScale(projectile.v, dt))
-    local h = clamp(projectile.caliber * 20, .2, 1)
-    PointLight(pos, math.random(0, 50) * .01, math.random(0, 50) * .01, math.random(50, 100) * .01,
-        h * 3 * lowRand(50, 150) * .01)
-    for i = 1, n do
-        self:renderSlowMoShieldShard(projectile, h * lowRand(75, 300) * .01, dir, pos, a * math.random(75, 150) * .01)
-    end
-end
-RenderEnergyShield = function(self, projectile, dt, a, centerPos)
-    if projectile.excludeSprites then
-        return
-    end
-    local n, mpl, life = 1, 4, .25
-    if projectile.caliber > .02 then
-        n = n + 1
-        mpl = mpl + .5
-        life = life + .25
-        if projectile.caliber > .1 then
-            n = n + 1
-            mpl = mpl + 1
-            life = life + .25
-            if projectile.caliber > .15 then
-                n = n + 1
-                mpl = mpl + 1.5
-                life = life + .25
-            end
-        end
-    end
-    local dir = VecDir(centerPos, projectile.pos)
-    local h = clamp(projectile.caliber * 20, .5, 2)
-    local l = projectile.length or .1
-    self.energyShieldShards:add(New(ShieldShard, {
-        h = h,
-        dir = dir,
-        pos = projectile.pos,
-        a = a,
-        mpl = mpl,
-        life = life,
-        n = n,
-    }))
-    n = n * 3
-    for i = 1, n do
-        self:renderEnergyShieldShard(
-            h,
-            dir,
-            projectile.pos,
-            a,
-            l,
-            100
-        )
-    end
-end
-ShieldShard = {
-    h = nil,
-    dir = nil,
-    pos = nil,
-    a = 1,
-    mpl = 2,
-    life = 1,
-    n = 1,
-}
+#version 2
 function ShieldShard:constructor()
     self.startLife = self.life * 1.25
 end
 
-Sprites = {
-    energyShieldShards = New(TwoWayListWrapper, { max = 50 }),
-    --trace = LoadSprite("MOD/img/fx/trace2.png"),
-    traceBackFace = LoadSprite("MOD/img/fx/trace_backface.png"),
-    trace = LoadSprite("MOD/img/fx/trace4.png"),
-    traceBackFaceLaser = LoadSprite("MOD/img/fx/trace_backface-laser.png"),
-    traceLaser = LoadSprite("MOD/img/fx/trace-laser.png"),
-    slowMoShield = {
-        --LoadSprite("MOD/img/fx/shield1.png"),
-        --LoadSprite("MOD/img/fx/shield2.png"),
-        --LoadSprite("MOD/img/fx/shield3.png"),
-        LoadSprite("MOD/img/fx/shield-1-1.png"),
-        LoadSprite("MOD/img/fx/shield-1-2.png"),
-        LoadSprite("MOD/img/fx/shield-1-3.png"),
-    },
-    energyShield = {
-        --LoadSprite("MOD/img/fx/e-shield-1-1.png"),
-        --LoadSprite("MOD/img/fx/e-shield-1-2.png"),
-        --LoadSprite("MOD/img/fx/e-shield-1-3.png"),
-        LoadSprite("MOD/img/fx/e-shield-2-1.png"),
-    },
-    --trace = LoadSprite("MOD/img/fx/trace3.png"),
-
-    renderEnergyShield = RenderEnergyShield,
-    renderSlowMoShield = RenderSlowMoShield,
-    renderSlowMoShieldShard = function(self, projectile, h, dir, pos, a)
-        local qDir =
-
-            QuatRotateQuat(
-                QuatDir(dir),
-                QuatEuler(
-                    math.random(-100, 100) * .3,
-                    math.random(-100, 100) * .3,
-                    math.random(-180, 180)
-                )
-            )
-
-        DrawSprite(
-            randA(self.slowMoShield),
-            Transform(
-                VecAdd(
-                    RandomVec(.01, .15),
-                    VecAdd(
-                        pos,
-                        VecScale(dir, .01 + (projectile.length or .1))
-                    )
-                ),
-                qDir
-            ),
-            h,
-            h,
-            math.random(25, 100) * .01, math.random(0, 100) * .01, math.random(75, 100) * .01,
-            a,
-            true,
-            true,
-            true
-        )
-    end,
-    processEnergyShards = function(self, dt)
-        self.energyShieldShards:iterate(
-            function(item, params)
-                item.life = item.life - params.dt
-                if item.life < 0 then
-                    return false, true, true
-                end
-                item.h = item.h + item.mpl * params.dt
-                item.a = math.max(item.a * (item.life / item.startLife), .1)
-                for i = 1, item.n do
-                    params.sprites:renderEnergyShieldShard(
-                        item.h,
-                        item.dir,
-                        VecAdd(
-                            RandomVec(.25, .5),
-                            item.pos
-                        ),
-                        item.a,
-                        item.l,
-                        150
-                    )
-                end
-            end,
-            { sprites = self, dt = dt }
-        )
-    end,
-    renderEnergyShieldShard = function(self, h, dir, pos, a, length, angle)
-        h = h * lowRand(75, 125) * .01
-        local qDir =
-
-            QuatRotateQuat(
-                QuatDir(dir),
-                QuatEuler(
-                    math.random(-angle, angle) * .1,
-                    math.random(-angle, angle) * .1,
-                    math.random(-180, 180)
-                )
-            )
-
-        DrawSprite(
-            randA(self.energyShield),
-            Transform(
-                VecAdd(
-                    RandomVec(.01, .15),
-                    VecAdd(
-                        pos,
-                        VecScale(dir, .01 + (length or .1))
-                    )
-                ),
-                qDir
-            ),
-            h,
-            h,
-            math.random(25, 100) * .01, math.random(0, 100) * .01, math.random(75, 100) * .01,
-            a * math.random(75, 125) * .01,
-            true,
-            true,
-            true
-        )
-    end,
-    renderProjectileTrace = function(self, projectile, dt, wMpl)
-        wMpl = wMpl or 1
-        local dir = VecNormalize(projectile.v)
-        local w, h, qDir = projectile.distance * wMpl, projectile.caliber * 3 * (projectile.tracerWidthMpl or 1),
-            QuatDir(dir)
-        --local pos = VecSub(projectile.pos, VecScale(projectile.v, .5 * dt))
-        local pos = VecSub(projectile.pos, VecScale(dir, .5 * w))
-        local minDistance, a = projectile.tracerMinDistance or 10, 0
-        if projectile.totalDistance > minDistance then
-            a = math.min(.9, ((projectile.totalDistance - minDistance) * .025) / w)
-        end
-        local r, g, b = 1, 1, 1
-        if projectile.tracerColor ~= nil then
-            r, g, b =
-                r + projectile.tracerColor[1],
-                g + projectile.tracerColor[2],
-                b + projectile.tracerColor[3]
-        end
-        DrawSprite(
-            self.traceBackFace,
-            Transform(
-                VecSub(projectile.pos, VecScale(dir, .005)),
-                qDir
-            ),
-            h,
-            h,
-            r, g, b,
-            a,
-            true,
-            true,
-            true
-        )
-        DrawSprite(
-            self.trace,
-            Transform(
-                pos,
-                QuatRotateQuat(
-                    qDir,
-                    QuatEuler(0, -90, 0)
-                )
-            ),
-            w,
-            h,
-            r, g, b,
-            a,
-            true,
-            true,
-            true
-        )
-        DrawSprite(
-            self.trace,
-            Transform(
-                pos,
-                QuatRotateQuat(
-                    qDir,
-                    QuatEuler(90, -90, 0)
-                )
-            ),
-            w,
-            h,
-            r, g, b,
-            a,
-            true,
-            true,
-            true
-        )
-    end,
-    renderEnergyProjectileTrace = function(self, projectile, dt)
-        local dir = VecNormalize(projectile.v)
-        local w, h, qDir = VecLength(projectile.v) * dt + projectile.length, projectile.caliber * 3, QuatDir(dir)
-        local pos = VecSub(projectile.pos, VecScale(projectile.v, .75 * dt))
-        local a = math.min(1, (projectile.totalDistance * .025) / w)
-        local color = projectile.tracerColor or { 1, 1, 1 }
-        DrawSprite(
-            self.traceBackFaceLaser,
-            Transform(
-                VecSub(projectile.pos, VecScale(dir, .005)),
-                qDir
-            ),
-            h,
-            h,
-            color[1], color[2], color[3],
-            a,
-            true,
-            true,
-            true
-        )
-        DrawSprite(
-            self.traceLaser,
-            Transform(
-                pos,
-                QuatRotateQuat(
-                    qDir,
-                    QuatEuler(0, -90, 0)
-                )
-            ),
-            w,
-            h,
-            color[1], color[2], color[3],
-            a,
-            true,
-            true,
-            true
-        )
-        DrawSprite(
-            self.traceLaser,
-            Transform(
-                pos,
-                QuatRotateQuat(
-                    qDir,
-                    QuatEuler(90, -90, 0)
-                )
-            ),
-            w,
-            h,
-            color[1], color[2], color[3],
-            a,
-            true,
-            true,
-            true
-        )
-    end,
-    tick = function(self, dt)
-        self:processEnergyShards(dt)
-    end,
-}

```

---

# Migration Report: src\timer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\timer.lua
+++ patched/src\timer.lua
@@ -1,6 +1,4 @@
-Timer = {
-    timers = {}
-}
+#version 2
 function Timer:tick(dt)
     for k, timer in pairs(self.timers) do
         self.timers[k] = self.timers[k] - dt
@@ -16,4 +14,5 @@
         return true
     end
     return false
-end+end
+

```

---

# Migration Report: src\tracker.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\tracker.lua
+++ patched/src\tracker.lua
@@ -1,6 +1,4 @@
---TODO:Refactor entire tracker
-trackerMarks = {}
-
+#version 2
 function InitTracker()
     if not trackerShell then
         trackerEnabled    = true
@@ -19,7 +17,6 @@
     end
 end
 
---TODO:Decouple from plane, replace with dedicated DTO
 function ProcessTracker(plane, dt)
     InitTracker()
     if not trackerEnabled then
@@ -106,7 +103,7 @@
     UiColor(0, 0, 1)
     for i, pos in ipairs(trackerMarks) do
         x, y, distance = UiWorldToPixel(pos)
-        if distance > 0 then
+        if distance ~= 0 then
             UiTranslate(x - sqSizeHalf, y - sqSizeHalf)
             UiRectOutline(sqSize, sqSize, 2)
         end
@@ -120,7 +117,6 @@
     UiPush()
     UiTranslate(UiCenter() + x, UiMiddle() + y)
     UiAlign("center top")
-
 
     ProBallistics.ballistics.rocketTracker:iterate(
         function(item)
@@ -131,7 +127,7 @@
             local minRange   = 500
             local finalRange = 50
             local distance   = math.min(item.projectile.data.distanceToTarget or 0, maxRange)
-            if distance > 0 then
+            if distance ~= 0 then
                 if distance > midRange then
                     barSize = math.floor(maxH * (distance / maxRange))
                     UiColor(0, 1, 0, 0.5)
@@ -160,12 +156,12 @@
     UiPush()
     UiTranslate(-130, 2)
     UiAlign("right top")
-    if ProBallistics.ballistics.rocketTracker.log.min > 0 then
+    if ProBallistics.ballistics.rocketTracker.log.min ~= 0 then
         UiText(string.format("%dm>", ProBallistics.ballistics.rocketTracker.log.min))
     end
     UiTranslate(260, 0)
     UiAlign("left top")
-    if ProBallistics.ballistics.rocketTracker.log.max > 0 then
+    if ProBallistics.ballistics.rocketTracker.log.max ~= 0 then
         UiText(string.format("<%dm", ProBallistics.ballistics.rocketTracker.log.max))
     end
     UiPop()
@@ -319,7 +315,7 @@
         local text = "Free Aim"
         UiColor(0, 1, 0)
         if ProBallistics.targetLock then
-            if ProBallistics.commanderPlane.aimVehicle > 0 then
+            if ProBallistics.commanderPlane.aimVehicle ~= 0 then
                 text = "Target Lock"
             else
                 text = "Hunt Mode"
@@ -505,3 +501,4 @@
 
     UiPop()
 end
+

```

---

# Migration Report: src\ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\ui.lua
+++ patched/src\ui.lua
@@ -1,10 +1,14 @@
+#version 2
 function UiTranslateReset()
     UiTranslate(UiCenter() - UiWidth() * .5, UiMiddle() - UiHeight() * .5)
 end
+
 function UiTranslateCenter()
     UiTranslate(UiCenter(), UiMiddle())
 end
+
 function UiTranslateAbsolute(x, y)
     UiTranslateReset()
     UiTranslate(x, y)
 end
+

```

---

# Migration Report: src\vectors.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\vectors.lua
+++ patched/src\vectors.lua
@@ -1,35 +1,28 @@
--- Tells if two vectors face in the same direction
+#version 2
 function VecSameDir(vec1, vec2)
     return VecDot(vec1, vec2) >= 0
 end
 
--- Align a vector to face in the same direction as a reference vector
--- (negate its direction if needed)
 function VecAlign(vec, vecRef)
     return VecSameDir(vec, vecRef) and vec or VecScale(vec, -1)
 end
 
--- Redirect a vector to face in the same direction as a reference vector
 function VecRedirect(vec, vecRef)
     return VecResize(vecRef, VecLength(vec))
 end
 
--- Set the length of a vector without changing its orientation
 function VecResize(vec, size)
     return VecScale(VecNormalize(vec), size)
 end
 
--- Project a vec1 on vec2 and return the length of vec1 projected
 function VecProjToVecLen(vec1, vec2)
     return VecDot(vec1, vec2) / VecLength(vec2)
 end
 
--- Reflect a vector on a surface
 function VecReflect(vec, normal)
     return VecSub(vec, VecScale(normal, 2 * VecDot(vec, normal)))
 end
 
--- Removed the vertical component of a vector
 function VecFlatten(vec)
     return Vec(vec[1], 0, vec[3])
 end
@@ -38,7 +31,6 @@
     return VecSub(Vec(), vec)
 end
 
--- Gets the minimal angle in degree between two vectors
 function VecAngleBetween(vec1, vec2)
     local vecLength = VecLength(vec1) * VecLength(vec2)
     if vecLength == 0 then
@@ -47,7 +39,6 @@
     return math.deg(math.acos(VecDot(vec1, vec2) / vecLength))
 end
 
--- Gets a 2D vector ignoring given axis
 function Vec3DTo2D(vec, axis)
     if axis == "x" then
         return { vec[2], vec[3] }
@@ -59,7 +50,6 @@
     return nil
 end
 
--- Gets the minimal angle in degree between two 2D vectors
 function Vec2DOrientedAngleBetween(vec1, vec2)
     local dot = vec1[1] * vec2[1] + vec1[2] * vec2[2]
     local det = vec1[1] * vec2[2] - vec1[2] * vec2[1]
@@ -71,17 +61,7 @@
     return length * math.cos(radians), length * math.sin(radians)
 end
 
---function calculateEndPosition(length, angle):
---    // Convert angle from degrees to radians
---    radians = angle * (π / 180)
---
---    // Calculate X and Y positions
---    X = length * cos(radians)
---    Y = length * sin(radians)
---
---    return (X, Y)
--- Rotate a vector on a given world axis
-function VecRotate(vec, axis, angle)
+unction VecRotate(vec, axis, angle)
     local radAngle = math.rad(angle)
     if axis == "x" then
         local newY = (math.cos(radAngle) * vec[2]) - (math.sin(radAngle) * vec[3])
@@ -99,7 +79,7 @@
     return vec
 end
 
-function VecElevate(vec, angle)
+unction VecElevate(vec, angle)
     return
         QuatRotateVec(
             QuatEuler(
@@ -111,7 +91,7 @@
         )
 end
 
-function VecRotateRandom(vec, maxVecAngle, mpl)
+unction VecRotateRandom(vec, maxVecAngle, mpl)
     mpl = mpl or 1
     return
         QuatRotateVec(
@@ -124,7 +104,7 @@
         )
 end
 
-function VecRotateRandom2d(vec, maxVecAngle, mpl)
+unction VecRotateRandom2d(vec, maxVecAngle, mpl)
     mpl = mpl or 1
     return
         QuatRotateVec(
@@ -137,7 +117,7 @@
         )
 end
 
-function VecRotateEuler(vec, euler)
+unction VecRotateEuler(vec, euler)
     return
         QuatRotateVec(
             QuatEuler(
@@ -147,44 +127,43 @@
         )
 end
 
-function VecDistance(vec1, vec2)
+unction VecDistance(vec1, vec2)
     return VecLength(VecSub(vec1, vec2))
 end
 
---[[QUAT]]
-function QuatLookDown(pos)
+unction QuatLookDown(pos)
     return QuatLookAt(pos, VecAdd(pos, Vec(0, -1, 0)))
 end
 
-function QuatLookUp(pos)
+unction QuatLookUp(pos)
     return QuatLookAt(pos, VecAdd(pos, Vec(0, 1, 0)))
 end
 
-function QuatTrLookDown(tr)
+unction QuatTrLookDown(tr)
     return QuatLookAt(tr.pos, TransformToParentPoint(tr, Vec(0, -1, 0)))
 end
 
-function QuatDir(dir)
+unction QuatDir(dir)
     return QuatLookAt(Vec(0, 0, 0), dir)
-end -- Quat to 3d worldspace dir.
-
-function GetQuatEulerVec(quat)
+end 
+
+unction GetQuatEulerVec(quat)
     local x, y, z = GetQuatEuler(quat)
     return Vec(x, y, z)
 end
 
-function VecDirAdd(d1, d2)
+unction VecDirAdd(d1, d2)
     return VecNormalize(VecAdd(d1, d2))
 end
 
-function RandomDir()
+unction RandomDir()
     return VecRotateRandom(
         Vec(1, 0, 0),
         180
     )
 end
 
-function RandomVec(min, max)
+unction RandomVec(min, max)
     return
         VecScale(
             RandomDir(),
@@ -195,18 +174,18 @@
         )
 end
 
-function RandomizeVec(v, min, max)
+unction RandomizeVec(v, min, max)
     return VecAdd(v, RandomVec(min, max))
 end
 
-function VecShake(v, max, min)
+unction VecShake(v, max, min)
     return VecAdd(
         v,
         RandomVec(min, max)
     )
 end
 
-function VecShake2d(v, max)
+unction VecShake2d(v, max)
     return VecAdd(
         v,
         Vec(
@@ -217,7 +196,7 @@
     )
 end
 
-function VecAverage(vectors)
+unction VecAverage(vectors)
     local c   = #vectors
     local avg = Vec()
     if c < 1 then
@@ -230,20 +209,20 @@
     return VecScale(avg, 1 / c)
 end
 
-function VecDir(v1, v2)
+unction VecDir(v1, v2)
     return VecNormalize(VecSub(v2, v1))
 end
 
-function VecMul(v1, v2)
+unction VecMul(v1, v2)
     return Vec(v1[1] * v2[1], v1[2] * v2[2], v1[3] * v2[3])
 end
 
-function VecToKph(v, dt)
+unction VecToKph(v, dt)
     dt = dt or 1
     return VecLength(v) * 3.6 / dt
 end
 
-function VecRotateTowards(v1, v2, angle)
+unction VecRotateTowards(v1, v2, angle)
     v1            = VecNormalize(v1)
     v2            = VecNormalize(v2)
 
@@ -267,4 +246,5 @@
     local rotated = VecAdd(term1, term2)
 
     return VecNormalize(rotated)
-end+end
+

```

---

# Migration Report: src\vision.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\vision.lua
+++ patched/src\vision.lua
@@ -1,35 +1,4 @@
-_defaultVisionMode      = "Def"
-_nightVisionMode        = "NV"
-_nightVisionHiMode      = "NVx"
-_lidarVisionMode        = "LIDAR"
-_thermalVisionMode      = "WhiteHot"
-_thermalVisionModeBlack = "BlackHot"
-fogParams               = nil
-DefaultVision           = New(envDefault)
-NightVision             = {}
-NightVisionHi           = {}
-LidarVision             = {}
-ThermalVision           = {}
-ThermalVisionBlack      = {}
-_overlayAutoAim         = "auto-aim"
-_overlayAntiAir         = "anti-air"
-Overlays                = {
-    _overlayAutoAim,
-    _overlayAntiAir,
-}
-VisionModesParams       = {
-    [_defaultVisionMode]      = DefaultVision,
-    [_nightVisionMode]        = NightVision,
-    [_nightVisionHiMode]      = NightVisionHi,
-    [_lidarVisionMode]        = LidarVision,
-    [_thermalVisionMode]      = ThermalVision,
-    [_thermalVisionModeBlack] = ThermalVision,
-}
-_UiOff                  = 0
-_UiMinimal              = 1
-_UiModerate             = 2
-_UiFull                 = 3
-UiModes                 = { _UiOff, _UiMinimal, _UiModerate, _UiFull }
+#version 2
 function refreshVisionEnv()
     DefaultVision = getEnv()
     if fogParams == nil then
@@ -88,10 +57,6 @@
     return envDefault
 end
 
-refreshVisionEnv()
-ThermalScanner = {
-    maxDistance = 5,
-}
 function ThermalScanner:getBodyHeat(body, viewPos, mpl)
     local mpl = mpl or 1
     if HasTag(body, "createdAt") then
@@ -178,14 +143,6 @@
     --    end
 end
 
-ObstacleDetection = {
-    range          = { 0.5, 125 },
-    maxObstacles   = 750,
-    maxSearchAngle = 30,
-    obstacles      = New(TwoWayListWrapper),
-    maxAlt         = 25,
-    bodies         = {},
-}
 function ObstacleDetection:cameraDetect()
     self:detect(GetCameraTransform())
 end
@@ -232,7 +189,7 @@
     self.obstacles:iterate(
         function(element, self)
             if element.spawnedAt < ticks - 15 then
-                if element.body > 0 then
+                if element.body ~= 0 then
                     self.bodies[element.body] = self.bodies[element.body] - 1
                 end
 
@@ -250,7 +207,7 @@
                 or math.abs(y) > UiHeight() / 2
             then
                 UiPop()
-                if element.body > 0 then
+                if element.body ~= 0 then
                     self.bodies[element.body] = self.bodies[element.body] - 1
                 end
 
@@ -282,7 +239,7 @@
     UiTranslate(UiCenter(), UiMiddle())
     local x, y, distance
     for body, count in pairs(self.bodies) do
-        if count > 0 then
+        if count ~= 0 then
             --outline
             DrawBodyOutline(body, 1, 1, 1, .5)
             --center of mass
@@ -301,3 +258,4 @@
     end
     UiPop()
 end
+

```

---

# Migration Report: src\weapons\casings.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\weapons\casings.lua
+++ patched/src\weapons\casings.lua
@@ -1,163 +1 @@
-Casing = {
-    name = "casing",
-    excludeSprites = true,
-    body = nil,
-    shape = nil,
-    v = Vec(),
-    angularV = Vec(),
-    pos = Vec(),
-    rot = Quat(),
-    active = true,
-    KE = 3500,
-    lifetime = 0,
-    specialEvent = -1,
-    totalDistance = 0,
-    proxyDistance = 0,
-    tracer = 0,
-    ricochet = 80,
-    noForce = true,
-    data = {
-        noPaint = true,
-        noPenetration = true,
-    },
-    weight = 1,
-    wind = .5,
-}
-CasingsHandler = {
-    casings = New(TwoWayListWrapper),
-    soundEnabled = ModOptions:getSetting("casingSound", true),
-    add = function(self, casing, transform, velocity, angularVelocity)
-        self.casings:add(
-            New(Casing, {
-                body = casing[1],
-                shape = casing[2],
-                v = velocity,
-                angularV = angularVelocity,
-                time = time,
-                pos = transform.pos,
-                rot = transform.rot,
-            })
-        )
-    end,
-    hitSound = function(self, pos)
-        if self.soundEnabled then
-            SoundManager:effect(
-                "casing",
-                pos,
-                1,
-                .250 - (math.random(0, 100) * .001)
-            )
-        end
-    end,
-    tick = function(self, dt)
-        self.casings:iterate(
-            function(casing, handler)
-                QueryRejectShape(casing.shape)
-                local _, hitProps = ProBallistics.ballistics:processProjectile(casing, dt)
-
-                if casing.hit and hitProps ~= nil then
-                    local r = { 10, 30 }
-                    casing.angularV = Vec(
-                        casing.angularV[1] * rSign() * lowRand(unpack(r)) * .1,
-                        casing.angularV[2] * rSign() * lowRand(unpack(r)) * .1,
-                        casing.angularV[3] * rSign() * lowRand(unpack(r)) * .1
-                    )
-                    self:hitSound(casing.pos)
-                end
-                local timeCorrectedDrag = 1 - (1 - .98) * legacyTimeCorrection
-
-                casing.angularV = VecScale(casing.angularV, timeCorrectedDrag) -- angular drag
-                local subDt = dt * 1
-                casing.rot = QuatRotateQuat(
-                    casing.rot,
-                    QuatEuler(
-                        casing.angularV[1] * subDt,
-                        casing.angularV[2] * subDt,
-                        casing.angularV[3] * subDt
-                    )
-                )
-                local vL = VecLength(casing.v)
-
-                if vL < 1 then
-                    local x, y, z = GetQuatEuler(casing.rot)
-                    casing.rot = QuatSlerp(casing.rot, QuatEuler(x, y, 0), 1 - vL)
-                end
-
-                SetBodyTransform(
-                    casing.body,
-                    Transform(
-                        casing.pos,
-                        casing.rot
-                    )
-                )
-                if
-                    not casing.active
-                --or casing.hit
-                then
-                    Delete(casing.body)
-                    return false, true, true
-                end
-            end,
-            self
-        )
-    end,
-    create = function(self, casing, transform, scale)
-        scale = scale or .25
-        local casing = Spawn(
-            string.format(
-                "<body tags='casing' dynamic='true' static='false'>" ..
-                "<vox file='MOD/vox/shells.vox' object='%s' scale='%f'/></body>",
-                casing,
-                scale
-            ),
-            transform
-        )
-        SetBodyDynamic(casing[1], false)
-        SetBodyActive(casing[1], false)
-        SetTag(casing[1], "createdAt", time)
-        local sX, sY, sZ = GetShapeSize(casing[2])
-        SetShapeLocalTransform(
-            casing[2],
-            Transform(
-                Vec(
-                    -sX * .05 * scale,
-                    -sY * .05 * scale,
-                    -sZ * .05 * scale
-                )
-            )
-        )
-        return casing
-    end,
-}
--- TODO: move somewhere else
-VoxManager = {
-    create = function(self, object, transform, scale, tags)
-        scale = scale or .25
-        tags = tags or "PBObject"
-        local object = Spawn(
-            string.format(
-                "<body tags='%s' dynamic='false' static='false'>" ..
-                "<vox file='MOD/vox/shells.vox' object='%s' scale='%f'/></body>",
-                tags,
-                object,
-                scale
-            ),
-            transform
-        )
-        SetBodyDynamic(object[1], false)
-        SetBodyActive(object[1], false)
-        local sX, sY, sZ = GetShapeSize(object[2])
-        SetShapeLocalTransform(
-            object[2],
-            Transform(
-                Vec(
-                    -sZ * scale * .05,
-                    -sY * scale * .05,
-                    0
-                ),
-                QuatEuler(0, 90, 0)
-            )
-        )
-        return object
-    end,
-}
+#version 2

```

---

# Migration Report: src\weapons\fx.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\weapons\fx.lua
+++ patched/src\weapons\fx.lua
@@ -1,3 +1,4 @@
+#version 2
 function RedDot(pos, intensity)
     intensity = intensity or 1
     PointLight(pos, 1, lowRand(0, 100) * .001, lowRand(0, 50) * .001, lowRand(5, 10) * .01 * intensity)
@@ -23,7 +24,7 @@
     ParticleReset()
     ParticleType("smoke")
     ParticleCollide(0) --?
-    local pVec = VecScale(GetPlayerVelocity(), .25)
+    local pVec = VecScale(GetPlayerVelocity(playerId), .25)
     local colorBase
     for i = 1, n do
         ParticleTile(randA(smokeTiles))
@@ -71,7 +72,7 @@
     ParticleReset()
     ParticleType("smoke")
     ParticleCollide(0) --?
-    local pVec = VecScale(GetPlayerVelocity(), .75)
+    local pVec = VecScale(GetPlayerVelocity(playerId), .75)
     for i = 1, n do
         ParticleTile(randA(smokeTiles))
         r, g, b = _sparkColor(color)
@@ -148,3 +149,4 @@
 
     return luminosity
 end
+

```

---

# Migration Report: src\weapons\hand-held-rotary.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\weapons\hand-held-rotary.lua
+++ patched/src\weapons\hand-held-rotary.lua
@@ -1,336 +1 @@
-HandWeaponRotary = New(HandWeapon, {
-    initMechanics    = function(self)
-        if self.mechanicsInitialized then
-            return
-        end
-        --DebugPrint("Initializing mechanics(rotary):" .. self.weaponLoadOut.options[1].name)
-        self.mechanics = {
-            bolt = WeaponMechanic:New(
-                {
-                    zOffset = 0,
-                    open = 0,
-                    shellTransform = Transform(
-                        Vec(.05, .1, .10),
-                        QuatEuler(0, 0, 90)
-                    ),
-                },
-                function(self, weapon, dt)
-                    if weapon.elements.bolt ~= nil then
-                        SetShapeLocalTransform(
-                            weapon.shapes.bolt,
-                            Transform(
-                                VecAdd(weapon.elements.bolt.transform.pos, Vec(0, 0, self.properties.zOffset)),
-                                weapon.elements.bolt.transform.rot
-                            )
-                        )
-                    end
-                    if not self.properties.active and self.properties.open >= 1 then
-                        SetValueInTable(
-                            self.properties,
-                            "zOffset",
-                            0,
-                            "easein",
-                            .2
-                        )
-                        SetValueInTable(
-                            self.properties,
-                            "open",
-                            0,
-                            "easein",
-                            .2
-                        )
-                    else
-                        self.properties.active = false
-                    end
-                end,
-                function(self, weapon, delay)
-                    if weapon.elements.bolt ~= nil then
-                        self.properties.active = true
-                        if not self.properties.open or self.properties.open <= 0 then
-                            SetValueInTable(
-                                self.properties,
-                                "zOffset",
-                                weapon.elements.bolt.zActionOffset,
-                                "easeout",
-                                delay
-                            )
-                            SetValueInTable(
-                                self.properties,
-                                "open",
-                                1,
-                                "easein",
-                                delay
-                            )
-                        end
-
-                        return self.properties.open >= 1
-                    end
-
-                    return true
-                end
-            ),
-            mode = WeaponMechanic:New(
-                {
-                    xRot = 0,
-                },
-                function(self, weapon, dt)
-                    if weapon.elements.mode ~= nil then
-                        SetShapeLocalTransform(
-                            weapon.shapes.mode,
-                            Transform(
-                                VecAdd(weapon.elements.mode.transform.pos, Vec(0, .0, 0)),
-                                QuatEuler(self.properties.xRot, 0, 0)
-                            )
-                        )
-                    end
-                end,
-                function(self, xRot)
-                    SetValueInTable(
-                        self.properties,
-                        "xRot",
-                        xRot,
-                        "easein",
-                        .15
-                    )
-                end
-            ),
-            barrel = WeaponMechanic:New(
-                {
-                    temperature = 25,
-                    zOffset     = 0,
-                    spin        = {
-                        val     = 0,
-                        current = 0,
-                        v       = 0,
-                        vAcc    = 16000,
-                        vMax    = 7200,
-                        drag    = 0.985,
-                        target  = 2700,
-                        minimum = 2600,
-                    },
-                },
-                function(self, weapon, dt)
-                    self.properties.temperature =
-                        clamp(
-                            self.properties.temperature -
-                            (math.sqrt(self.properties.temperature) * 1.5 + self.properties.spin.current * .035)
-                            * dt,
-                            25,
-                            self.properties.temperature
-                        )
-                    local glowTemp = 100
-                    if weapon.elements.barrel ~= nil then
-                        local spinVol = FluidChange:change(
-                            "spinVol-" .. self.__id,
-                            self.properties.spin.current / self.properties.spin.target,
-                            .25,
-                            0
-                        )
-
-                        local spinUpVol = FluidChange:change(
-                            "spinUpVol-" .. self.__id,
-                            self.properties.spin.v / self.properties.spin.vMax,
-                            .25,
-                            0
-                        )
-                        --DebugWatch("SpinCurrent", self.properties.spin.current)
-                        --DebugWatch("SpinRate", self.properties.spin.current / self.properties.spin.target)
-                        --DebugWatch("SpinVol", spinVol)
-                        --DebugWatch("SpinUpVol", spinUpVol)
-                        SoundManager:engine("spinIdle", weapon.pos, spinUpVol)
-                        SoundManager:engine("spinUp", weapon.pos, spinVol)
-                        if not self.properties.spinUp then --idle
-                            local timeCorrectedDrag      = 1 - (1 - self.properties.spin.drag) * legacyTimeCorrection
-                            self.properties.spin.v       =
-                                math.max(
-                                    self.properties.spin.v * timeCorrectedDrag * timeCorrectedDrag,
-                                    0.1
-                                )
-                            self.properties.spin.current =
-                                math.max(
-                                    self.properties.spin.current * timeCorrectedDrag,
-                                    1
-                                )
-                        end
-
-                        self.properties.spin.val =
-                            ((self.properties.spin.val + self.properties.spin.current * dt) * 100 % 36000) * .01
-
-                        local angle = -self.properties.spin.val
-                        local offsetX, offsetY = circleXY(.105, angle + 45)
-
-                        local t = Transform(
-                            VecAdd(weapon.elements.barrel.transform.pos,
-                                Vec(.075, .075, self.properties.zOffset)),
-                            QuatRotateQuat(
-                                QuatEuler(0, 0, angle),
-                                weapon.elements.barrel.transform.rot
-                            )
-                        )
-                        t.pos = VecSub(t.pos, Vec(offsetX, offsetY, 0))
-                        SetShapeLocalTransform(
-                            weapon.shapes.barrel,
-                            t
-                        )
-                        local bGlow = 0
-
-                        if self.properties.temperature > glowTemp then
-                            bGlow =
-                                math.min(
-                                    15,
-                                    (self.properties.temperature - glowTemp) * .01
-                                ) * ProBallistics.barrelGlowMpl
-                            if ProBallistics.visionMode == _thermalVisionMode then
-                                --bGlow = bGlow * 10
-                                DrawShapeHighlight(weapon.shapes.barrel, bGlow * .1)
-                            end
-                        end
-                        SetShapeEmissiveScale(
-                            weapon.shapes.barrel,
-                            bGlow
-                        )
-                        self.properties.spinUp = false
-                    end
-                end,
-                function(self, weapon, shell, dt)
-                    if shell ~= nil then
-                        self.properties.temperature =
-                            self.properties.temperature + (shell.temp or (shell.initialV * 3.5))
-                        if weapon.elements.barrel ~= nil then
-                            self.properties.zOffset = weapon.elements.barrel.zActionOffset
-                            SetValueInTable(
-                                self.properties,
-                                "zOffset",
-                                0,
-                                "easeout",
-                                weapon.elements.barrel.zActionDelay
-                            )
-                        end
-                        return true
-                    else
-                        self.properties.spinUp       = true
-                        self.properties.spin.v       =
-                            math.min(self.properties.spin.v + self.properties.spin.vAcc * dt,
-                                self.properties.spin.vMax
-                            )
-                        self.properties.spin.current =
-                            math.min(
-                                self.properties.spin.current + self.properties.spin.v * dt * .25,
-                                self.properties.spin.target * 1.1
-                            )
-
-                        return self.properties.spin.current >= self.properties.spin.minimum
-                    end
-                end
-            )
-        }
-        self.mechanicsInitialized = true
-        --SetString("game.player.tool", currentTool)
-    end,
-    shoot            = function(self, dt)
-        if not (self.mechanics.barrel:action(self, nil, dt) and self.mechanics.bolt:action(self, .25)) then
-            return
-        end
-        local shell, prototype = self.weaponLoadOut:getShell(true)
-
-        if shell then
-            if ProBallistics.ballistics:shoot(shell, self.pos, self.aimAt, self.aimExtra) then
-                local recoilTimer = shell.recoilTimer or math.min(shell.delay * 1.1, .25)
-                SoundManager:shoot(shell, self.pos)
-                self:shootEffects(TransformToDir(self.transform))
-                self.recoilTimer = recoilTimer
-                rot = self.ironsight and .5 or 0
-                local ironrot =
-                    (
-                        self.ironsight and (-recoilTimer * 3 - rot)
-                        or -recoilTimer * 20 - rot
-                    )
-                    * self:getRecoilRate()
-                self.recoil[1] = self.recoil[1] + ironrot * rSign() * self.realismScale
-                self.recoil[2] = self.recoil[2] + ironrot * rSign() * self.realismScale
-                ShakeCamera(shell.recoil * self:getShakeRate())
-                if shell.casing and self.ejectCasings then
-                    self:ejectShellCasing(shell.casing)
-                end
-                self.mechanics.barrel:action(self, shell, dt)
-                return true
-            end
-        elseif prototype.streamFire then
-            SoundManager:shoot(prototype, self.pos)
-        end
-    end,
-    evenShellCasing  = false,
-    ejectShellCasing = function(self, casing)
-        self.evenShellCasing = not self.evenShellCasing
-        local shellOffsetTransform =
-            self.evenShellCasing and
-            Transform(
-                Vec(.1, .2 - self.mechanics.bolt.properties.zOffset, .125),
-                QuatEuler(0, 0, 90)
-            ) or Transform(
-                Vec(.1, .2 - self.mechanics.bolt.properties.zOffset, .05),
-                QuatEuler(0, 0, 90)
-            )
-        local shellT = TransformToParentTransform(
-            self.transform,
-            TransformToParentTransform(
-                self.elements.bolt.transform,
-                shellOffsetTransform
-            )
-        )
-        local casing = CasingsHandler:create(casing, shellT)
-        local velocity = VecAdd(
-            GetPlayerVelocity(),
-            TransformToParentVec(
-                shellT,
-                VecScale(
-                    VecRotateRandom(
-                        (self.evenShellCasing and Vec(1, -3.5, 1.25) or Vec(1, -3.5, -1.25)),
-                        20,
-                        .1
-                    ),
-                    lowRand(150, 175) * .01 + highRand(25, 50) * .01 - .25
-                )
-            )
-        )
-        local angularVelocity = VecInvert(
-            VecAdd(
-                Vec(0, lowRand(500, 1500), lowRand(500, 1000)),
-                VecScale(
-                    GetBodyAngularVelocity(
-                        GetBoneBody(GetPlayerAnimator(), "arm_lower_r")
-                    ),
-                    2.5
-                )
-            )
-        )
-        CasingsHandler:add(casing, shellT, velocity, angularVelocity)
-    end,
-    initShapes       = function(self)
-        local shapes = GetBodyShapes(self.toolBody)
-        self.shapes = {
-            gun = shapes[1],
-            barrel = shapes[2],
-            bolt = shapes[3],
-            mag = shapes[4],
-            mode = shapes[5],
-            safety = shapes[6],
-            holo = shapes[7],
-            scope = shapes[8],
-            scopeDiagonal = shapes[9],
-        }
-        if self.shapes.scopeDiagonal ~= nil then
-            SetShapeLocalTransform(
-                self.shapes.scopeDiagonal,
-                Transform(
-                    VecAdd(GetShapeLocalTransform(self.shapes.scope).pos, Vec(.075, .02, -.05)),
-                    QuatEuler(-90, 0, 45)
-                )
-            )
-        end
-    end,
-    debugTick        = function(self, dt)
-        --DebugCross(self.pos)
-        return
-    end,
-})
+#version 2

```

---

# Migration Report: src\weapons\hand-held.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\weapons\hand-held.lua
+++ patched/src\weapons\hand-held.lua
@@ -1,6 +1,4 @@
-WeaponMechanic = {
-    baseTransform = nil,
-}
+#version 2
 function WeaponMechanic:New(properties, processCallback, actionCallback)
     return New(
         self,
@@ -14,867 +12,6 @@
     )
 end
 
-HandWeapon = {
-    init                 = function(self)
-        self:setPose()
-        if not self.redDotOffset then
-            self.redDotOffset = TransformToParentTransform(
-                self.transform,
-                Transform(
-                    VecAdd(
-                        self.barrelOffset,
-                        Vec(0, -.05, 0)
-                    )
-                )
-            )
-        end
-    end,
-    redDotScale          = ModOptions:getSetting("gameRedDotScale", 1),
-    redDotFlicker        = ModOptions:getSetting("gameRedDotFlicker", true),
-    realismScale         = ModOptions:getSetting("gameRealismScale", 1),
-    ejectCasings         = ModOptions:getSetting("ejectCasings", true),
-    mechanics            = nil,
-    mechanicsInitialized = false,
-    elements             = {
-
-    },
-    holoTransform        = Transform(Vec(.45, -.25, -.45), QuatEuler(0, 0, -90)),
-    holoSize             = .05,
-    initMechanics        = function(self)
-        if self.mechanicsInitialized then
-            return
-        end
-        --DebugPrint("Initializing mechanics:" .. self.weaponLoadOut.options[1].name)
-        self.mechanics = {
-            bolt = WeaponMechanic:New(
-                {
-                    zOffset = 0,
-                    shellTransform = Transform(
-                        Vec(.05, .1, .10),
-                        QuatEuler(0, 0, 90)
-                    ),
-                },
-                function(self, weapon, dt)
-                    if weapon.elements.bolt ~= nil then
-                        SetShapeLocalTransform(
-                            weapon.shapes.bolt,
-                            Transform(
-                                VecAdd(weapon.elements.bolt.transform.pos, Vec(0, 0, self.properties.zOffset)),
-                                weapon.elements.bolt.transform.rot
-                            )
-                        )
-                    end
-                end,
-                function(self, weapon, delay, casing)
-                    if weapon.elements.bolt ~= nil then
-                        self.properties.zOffset = weapon.elements.bolt.zActionOffset
-                        SetValueInTable(
-                            self.properties,
-                            "zOffset",
-                            0,
-                            "easein",
-                            delay
-                        )
-                        if casing and weapon.ejectCasings then
-                            weapon:ejectShellCasing(casing)
-                        end
-                    end
-                end
-            ),
-            mode = WeaponMechanic:New(
-                {
-                    xRot = 0,
-                },
-                function(self, weapon, dt)
-                    if weapon.elements.mode ~= nil then
-                        SetShapeLocalTransform(
-                            weapon.shapes.mode,
-                            Transform(
-                                VecAdd(weapon.elements.mode.transform.pos, Vec(0, .0, 0)),
-                                QuatEuler(self.properties.xRot, 0, 0)
-                            )
-                        )
-                    end
-                end,
-                function(self, xRot)
-                    SetValueInTable(
-                        self.properties,
-                        "xRot",
-                        xRot,
-                        "easein",
-                        .15
-                    )
-                end
-            ),
-            barrel = WeaponMechanic:New(
-                {
-                    temperature = 25,
-                    zOffset = 0,
-                },
-                function(self, weapon, dt)
-                    self.properties.temperature =
-                        clamp(
-                            self.properties.temperature - math.sqrt(self.properties.temperature) * dt,
-                            25,
-                            self.properties.temperature
-                        )
-                    local glowTemp = 100
-                    if weapon.elements.barrel ~= nil then
-                        SetShapeLocalTransform(
-                            weapon.shapes.barrel,
-                            Transform( --TODO replace with native operation TransformToVec or sth
-                                VecAdd(weapon.elements.barrel.transform.pos, Vec(0, 0, self.properties.zOffset)),
-                                weapon.elements.barrel.transform.rot
-                            )
-                        )
-                        local bGlow = 0
-
-                        if self.properties.temperature > glowTemp then
-                            bGlow =
-                                math.min(
-                                    5 ,
-                                    (self.properties.temperature - glowTemp) * .0033
-                                ) * ProBallistics.barrelGlowMpl
-                            if ProBallistics.visionMode == _thermalVisionMode then
-                                --bGlow = bGlow * 10
-                                DrawShapeHighlight(weapon.shapes.barrel, bGlow * .5)
-                            end
-                        end
-                        SetShapeEmissiveScale(
-                            weapon.shapes.barrel,
-                            bGlow
-                        )
-                    end
-                end,
-                function(self, weapon, shell)
-                    self.properties.temperature =
-                        self.properties.temperature + (shell.temp or (shell.initialV * 3.5))
-                    if weapon.elements.barrel ~= nil then
-                        self.properties.zOffset = weapon.elements.barrel.zActionOffset
-                        SetValueInTable(
-                            self.properties,
-                            "zOffset",
-                            0,
-                            "easeout",
-                            weapon.elements.barrel.zActionDelay
-                        )
-                    end
-                end
-            )
-        }
-        self.mechanicsInitialized = true
-        --SetString("game.player.tool", currentTool)
-    end,
-    processMechanics     = function(self, dt)
-        for _, mechanic in pairs(self.mechanics) do
-            mechanic:process(self, dt)
-        end
-    end,
-    initShapes           = function(self)
-        local shapes = GetBodyShapes(self.toolBody)
-        self.shapes = {
-            gun = shapes[1],
-            barrel = shapes[2],
-            bolt = shapes[3],
-            mag = shapes[4],
-            mode = shapes[5],
-            safety = shapes[6],
-            holo = shapes[7],
-            scope = shapes[8],
-            scopeDiagonal = shapes[9],
-            redDot = shapes[10],
-        }
-        if self.shapes.scopeDiagonal ~= nil then
-            SetShapeLocalTransform(
-                self.shapes.scopeDiagonal,
-                Transform(
-                --VecAdd(self.transform.pos, Vec(-.08, .275, -.1)),
-                    VecAdd(GetShapeLocalTransform(self.shapes.scope).pos, Vec(.075, .02, -.05)),
-                    QuatEuler(-90, 0, 45)
-                )
-            )
-        end
-    end,
-    getBody              = function(self)
-        local b = GetToolBody()
-        if b ~= 0 then
-            self.toolBody = b
-            self:initShapes()
-            self:initMechanics()
-            return true
-        end
-        return false
-    end,
-    ironsight            = false,
-    redDot               = true,
-    holo                 = false,
-    pos                  = Vec(),
-    transform            = Transform(),
-    aimExtra             = New(AimExtra, { fixedElevation = .75 }),
-    recoilTimer          = 0,
-    aimAt                = Vec(),
-    walkingSpeed         = .9,
-    aimPose              = _aimPoseShoulder,
-    aimPoses             = {
-        _aimPoseShoulder,
-        _aimPoseIron,
-        _aimPoseIronSideways,
-    },
-    aimOffsets           = {
-        [_aimPoseShoulder] = { x = 0, y = .2, z = 0, tilt = 0 },
-        [_aimPoseIron] = { x = -.32, y = .2, z = .35, tilt = 0, fov = 45 },
-        [_aimPoseIronSideways] = { x = -.5, y = -.2, z = .3, tilt = 50, fov = 75 },
-        --[_aimPoseHip] = { x = 0, y = -.375, z = 0, tilt = 0, fov = 90 },
-    },
-    aimOffset            = { x = 0, y = .2, z = 0, tilt = 0, fov = 90 },
-    barrelOffset         = Vec(0.325, -0.575, -2.01),
-    crouching            = false,
-    moving               = false,
-    running              = false,
-    fov                  = GetInt("options.gfx.fov"),
-    casingOffset         = Vec(.1, .15, .05),
-    ejectShellCasing     = function(self, casing)
-        local shellOffsetTransform = Transform(
-            VecSub(self.casingOffset, Vec(0, self.mechanics.bolt.properties.zOffset, 0)),
-            QuatEuler(0, 0, 90)
-        )
-        local shellT = TransformToParentTransform(
-            self.transform,
-            TransformToParentTransform(
-                self.elements.bolt.transform,
-                shellOffsetTransform
-            )
-        )
-        local casing = CasingsHandler:create(casing, shellT)
-        local velocity = VecAdd(
-            GetPlayerVelocity(),
-            TransformToParentVec(
-                shellT,
-                VecScale(
-                    VecRotateRandom(
-                        Vec(1, -3.5, 2),
-                        25,
-                        .1
-                    ),
-                    lowRand(100, 150) * .01 + highRand(0, 20) * .01 - .2
-                )
-            )
-        )
-        local angularVelocity = VecInvert(
-            VecAdd(
-                Vec(0, lowRand(500, 1500), lowRand(500, 1000)),
-                VecScale(
-                    GetBodyAngularVelocity(
-                        GetBoneBody(GetPlayerAnimator(), "arm_lower_r")
-                    ),
-                    2
-                )
-            )
-        )
-        CasingsHandler:add(casing, shellT, velocity, angularVelocity)
-    end,
-    weaponLoadOut        = New(WeaponLoadOut, {
-        options = {
-            New(LoadOut,
-                {
-                    name    = "",
-                    options = {},
-                }
-            ),
-        }
-    }),
-    setPose              = function(self, pose)
-        if pose ~= nil then
-            self.aimPose = pose
-        end
-        self.aimOffset = self.aimOffsets[self.aimPose]
-        --for k, v in pairs(self.aimOffsets[self.aimPose]) do
-        --    SetValueInTable(
-        --        self.aimOffset,
-        --        k,
-        --        v,
-        --        "easeout",
-        --        (k == "fov") and .75 or .25
-        --    )
-        --end
-    end,
-    ragdoll              = false,
-    switchFireMode       = function(self)
-        self.mechanics.mode:action(
-            self.fireModesRot[self.weaponLoadOut:switchFireMode()] or 0
-        )
-    end,
-    shrinkHead           = function()
-        local head = GetBoneBody(GetPlayerAnimator(), "head")
-        local shapes = GetBodyShapes(head)
-        for i = 1, #shapes do
-            ResizeShape(shapes[i], 0, 0, 0, 1, 1, 1)
-        end
-    end,
-    inputs               = function(self, dt)
-        self.crouching = InputDown("crouch")
-        self.moving = InputDown("up") or InputDown("down") or InputDown("left") or InputDown("right")
-        self.running = InputDown("shift")
-        self.steady = InputDown("rmb")
-        --if InputPressed(ProBallistics.keyGunCam) then
-        --    HandWeapon.realFPS = not HandWeapon.realFPS
-        --end
-        if InputPressed(ProBallistics.keyFireMode) then
-            self:switchFireMode()
-            SoundManager:effect("switch", self.pos)
-        end
-
-        if InputPressed(ProBallistics.keyRedDot) then
-            self.redDot = not self.redDot
-            SoundManager:effect("switch", self.pos)
-        end
-
-        if InputPressed(ProBallistics.keyStance1) then
-            if self.aimPose == _aimPoseIron then
-                self:setPose(_aimPoseShoulder)
-            else
-                self:setPose(_aimPoseIron)
-            end
-        end
-
-        if InputPressed(ProBallistics.keyStance2) then
-            if self.aimPose == _aimPoseIronSideways then
-                self:setPose(_aimPoseShoulder)
-            else
-                self:setPose(_aimPoseIronSideways)
-            end
-        end
-
-        self.weaponLoadOut:inputs()
-        Spotter:inputs({ fov = (self.aimOffset.fov or ProBallistics.defaultFov) })
-        if InputPressed(ProBallistics.keyReload) then
-            self:reload()
-        end
-        if InputDown("usetool") then
-            if InputDown(ProBallistics.keyRemoteTargeting) then
-                ProBallistics.commanderPlane:shoot()
-            else
-                self:shoot(dt)
-            end
-        end
-        local rMpl = self.running and 1.75 or 1
-        if self.steady then
-            if self.crouching then
-                self.walkSpeed(1.5 * rMpl)
-            else
-                self.walkSpeed(2.5 * rMpl)
-            end
-        else
-            self.walkSpeed(5 * rMpl)
-        end
-    end,
-    walkSpeed            = function(speed)
-        SetPlayerWalkingSpeed(speed --[[* ProBallistics.timeScale]])
-    end,
-    reload               = function(self)
-        -- reload animation
-    end,
-    steady               = false,
-    debugCamera          = false,
-    eyeSmooth            = nil,
-    realFPS              = false,
-    gunCamOffset         = Transform(
-        Vec(0, -.45, -.65),
-        QuatEuler(0, 0, 0)
-    ),
-    camera               = function(self, dt)
-        local camera = Spotter:camera(.2, self.aimOffset.fov or ProBallistics.defaultFov)
-        local zoomSensitivity = FluidChange:change("zoomSensitivity", self.aimOffset.zoomSensitivity or .25, .25)
-        if camera == false then
-            local aimDof = .1
-            local aimDistance = FluidChange:tween("aimDistance", self.aimDistance, .01) + 1
-            local panMpl = math.sqrt(math.abs(_mx) + math.abs(_my)) * .5
-            local mpl = (self.moving and 3.5 or 1) + panMpl
-            FluidChange:tween("panMpl", panMpl, .1, 0)
-            if self.steady then
-                aimDof = FluidChange:tween("aimDof", (self.aimOffset.zoomDof or .75) * mpl, .01, .75)
-            else
-                aimDof = FluidChange:tween("aimDof", (self.aimOffset.dof or .05) * mpl, .1, .05)
-            end
-
-            SetCameraFov(FluidChange:tween("aimFov", self.aimOffset.fov or ProBallistics.defaultFov, .3))
-
-            SetCameraDof(aimDistance, aimDof)
-        else
-            if camera.transform ~= nil then
-                SetCameraTransform(camera.transform)
-            end
-            if camera.fov ~= nil then
-                SetCameraFov(camera.fov)
-            end
-        end
-        SetToolAllowedZoom(.999, zoomSensitivity)
-    end,
-    swayVec              = Vec(),
-    sway                 = function(self, t, dt)
-        --local swayScale = .1 * (self.aimOffset.sway or 1)
-        local swayScale = .1 * FluidChange:change("aimSway-" .. self.id, self.aimOffset.sway or 1, .5, 1)
-        local noiseScale = self.steady and .25 or 1
-        if self.crouching then
-            swayScale = swayScale * .5
-        end
-        if self.moving then
-            noiseScale = noiseScale * 3
-            if self.crouching then
-                noiseScale = noiseScale * 1.25
-            end
-        end
-
-        noiseScale = noiseScale * legacyTimeCorrection
-
-        local noiseVec = Vec(
-            math.sin(time * 1.5 * (self.moving and 15 or 1)) * noiseScale * .75 * (self.running and 2 or 1),
-            math.sin(time * 1.5 * (self.moving and 7.5 or .5)) * noiseScale *
-            (self.moving and 3.5 or 1) * (self.running and 3 or 1),
-            math.sin(time * .1) * noiseScale * .2
-        )
-        local swayFadeOff = 1 - (1 - .96) * legacyTimeCorrection
-
-        self.swayVec = VecScale(self.swayVec, swayFadeOff)
-        self.swayVec = VecAdd(self.swayVec, noiseVec)
-
-        return
-            TransformToParentTransform(
-                t,
-                Transform(
-                    Vec(),
-                    QuatEuler(unpack(VecScale(self.swayVec, swayScale * self.realismScale)))
-                )
-            )
-    end,
-    rightHandTransform   =
-        Transform(
-            Vec(.375, -.6, -.225),
-            QuatAxisAngle(Vec(0, 1, 0), 90.0)
-        ),
-    leftHandTransform    =
-        Transform(
-            Vec(.21, -.475, -.6),
-            QuatEuler(0, 90, 0)
-        ),
-    tick                 = function(self, dt)
-        if self:getBody() then
-            self.aimAt, _, self.aimDistance = self:getAim()
-            self:inputs(dt)
-            self:camera(dt)
-            if self.redDot then
-                self.redDotSource, self.redDotAimAt, _, _, _, self.aimAtFloat = self:getRedDotAim()
-
-                RedDot(self.aimAtFloat, 1)
-                if self.shapes.redDot then
-                    SetShapeEmissiveScale(self.shapes.redDot, 100)
-                end
-                --RedDot(self.redDotSource.pos, .75)
-            else
-                SetShapeEmissiveScale(self.shapes.redDot, 0)
-            end
-
-
-            local recoilFadeRate = 1 - (1 - .9) * legacyTimeCorrection
-            self.recoil[1] = self.recoil[1] * recoilFadeRate
-            self.recoil[2] = self.recoil[2] * recoilFadeRate
-            local t =
-                Transform(
-                    Vec(self.aimOffset.x, self.aimOffset.y, self.recoilTimer + self.aimOffset.z),
-                    QuatEuler(-self.recoil[1] + .1, self.recoil[2] + .1, self.aimOffset.tilt)
-                )
-
-            t = FluidChange:tween(
-                "toolTransform-" .. self.id,
-                t,
-                .35,
-                t
-            )
-
-            SetToolTransform(self:sway(t, dt), .75)
-
-            self.recoilTimer = clamp(self.recoilTimer - dt, 0, 10)
-            self.transform = GetBodyTransform(self.toolBody)
-            self.pos = TransformToParentPoint(
-                self.transform,
-                VecAdd(
-                    self.barrelOffset,
-                    Vec(0, 0, self.mechanics.barrel.properties.zOffset)
-                )
-            )
-            SetToolHandPoseLocalTransform(
-                self.rightHandTransform,
-                self.leftHandTransform
-            )
-            self:processMechanics(dt)
-        end
-
-        self.weaponLoadOut:processTimers(dt)
-        self:debugTick(dt)
-    end,
-    getAim               = function(self)
-        return GetCamLookPos(Transform(self.pos, self.transform.rot))
-    end,
-    getRedDotAim         = function(self)
-        local t = TransformToParentTransform(
-            self.transform,
-            self.redDotOffset
-        )
-        return t, GetCamLookPos(t)
-    end,
-    recoil               = { 0, 0 },
-    getRecoilRate        = function(self)
-        return (self.crouching and .5 or 1) * (self.moving and 2 or 1) * ProBallistics.timeScale
-    end,
-    getShakeRate         = function(self)
-        return (self.crouching and .75 or 1) * (self.moving and 1.25 or 1) * (self.ironsight and .85 or 1)
-    end,
-    fireModesRot         = {
-        [0] = 89,
-        [1] = -89,
-        [3] = 0,
-        [5] = -89,
-    },
-    shoot                = function(self, dt)
-        local shell, prototype = self.weaponLoadOut:getShell(true)
-
-        if shell then
-            if ProBallistics.ballistics:shoot(shell, self.pos, self.aimAt, self.aimExtra) then
-                local recoilTimer = shell.recoilTimer or math.min(shell.delay * 1.1, .25)
-                SoundManager:shoot(shell, self.pos)
-                self:shootEffects(TransformToDir(self.transform))
-                self.recoilTimer = recoilTimer
-                rot = self.ironsight and .5 or 0
-                local ironrot =
-                    (
-                        self.ironsight and (-recoilTimer * 3 - rot)
-                        or -recoilTimer * 20 - rot
-                    )
-                    * self:getRecoilRate()
-                self.recoil[1] = self.recoil[1] + ironrot * rSign() * self.realismScale
-                self.recoil[2] = self.recoil[2] + ironrot * rSign() * self.realismScale
-                ShakeCamera(shell.recoil * self:getShakeRate())
-                self.mechanics.bolt:action(self, clamp(shell.delay * .95, 0, .25), shell.casing)
-                self.mechanics.barrel:action(self, shell, dt)
-                return true
-            end
-        elseif prototype.streamFire then
-            SoundManager:shoot(prototype, self.pos)
-        end
-    end,
-    effects              = 2,
-    shootEffects         = function(self, direction)
-        local barrelTemp = self.mechanics.barrel.properties.temperature
-        local sparksMpl, fireSizeMpl = 1, .75
-        local minTemp, maxTemp = 100, 750
-        if barrelTemp > minTemp then
-            sparksMpl = sparksMpl + (math.min(maxTemp, barrelTemp) - minTemp) * .003
-            fireSizeMpl = ((fireSizeMpl * 2) + (math.min(maxTemp, barrelTemp) - minTemp) / (maxTemp - minTemp)) * .5
-        end
-        local fxPos = VecAdd(self.pos, VecScale(direction, .1))
-        if self.effects == 0 then
-            GunSmoke(fxPos, direction, 3, 250, .2, .3)
-            Sparks(fxPos, 2.5 * sparksMpl, .1, 0, 1.3, direction, nil, 0.005, 15)
-        elseif self.effects == 1 then
-            GunFire(fxPos, direction, 2, 125, .1 * fireSizeMpl, .2)
-            GunSmoke(fxPos, direction, 4, 250, .2, .3)
-            Sparks(fxPos, 1.5 * sparksMpl, .1, 0, 1.3, direction, nil, 0.005, 10)
-        elseif self.effects == 2 then
-            GunFire(fxPos, direction, 2, 125, .15 * fireSizeMpl, .2)
-            GunSmoke(fxPos, direction, 4, 250, .2, .3)
-            Sparks(fxPos, 2.5 * sparksMpl, .1, 0, 1.3, direction, nil, 0.005, 10)
-        elseif self.effects == 3 then
-            GunFire(fxPos, direction, 4, 150, .2 * fireSizeMpl, .2)
-            GunSmoke(fxPos, direction, 4, 250, .2, .3)
-            Sparks(fxPos, 4 * sparksMpl, .1, 0, 2, direction, nil, 0.005, 10)
-        elseif self.effects == 4 then
-            GunSmoke(fxPos, direction, 4, 250, .3, .5)
-            GunSmoke(fxPos, direction, 4, 250, .3, 1)
-            Sparks(fxPos, 20 * sparksMpl, .75, 0, 2, direction, nil, 0.01, 7.5)
-        elseif self.effects == 10 then
-            GunFire(fxPos, direction, 4, 150, .3 * fireSizeMpl, .3)
-            GunSmoke(fxPos, direction, 2, 100, .5, 15)
-            GunSmoke(fxPos, direction, 7, 25, .25, 12)
-            Sparks(fxPos, 100 * sparksMpl, .75, 0, 5, direction, nil, 0.005, 7.5)
-        end
-    end,
-    getHoloCenter        = function(self)
-        return
-            TransformToParentTransform(
-                GetBodyTransform(self.toolBody),
-                TransformToParentTransform(
-                    self.holoTransform,
-                    Transform(
-                        Vec(self.holoSize / 2, self.holoSize / 2, 0)
-                    )
-                )
-            )
-    end,
-    drawHolo             = function(self)
-        local x, y, distance = UiWorldToPixel(self.aimAt)
-        local margin = .01
-        local centerT = self:getHoloCenter()
-        local LBT =
-            TransformToParentTransform(
-                GetBodyTransform(self.toolBody),
-                TransformToParentTransform(
-                    self.holoTransform,
-                    Transform(
-                        Vec(margin, margin, 0)
-                    )
-                )
-            )
-        local RTT =
-            TransformToParentTransform(
-                GetBodyTransform(self.toolBody),
-                TransformToParentTransform(
-                    self.holoTransform,
-                    Transform(
-                        Vec(self.holoSize - margin, self.holoSize - margin, 0)
-                    )
-                )
-            )
-
-        local RBT =
-            TransformToParentTransform(
-                GetBodyTransform(self.toolBody),
-                TransformToParentTransform(
-                    self.holoTransform,
-                    Transform(
-                        Vec(self.holoSize - margin, margin, 0)
-                    )
-                )
-            )
-        local LTT =
-            TransformToParentTransform(
-                GetBodyTransform(self.toolBody),
-                TransformToParentTransform(
-                    self.holoTransform,
-                    Transform(
-                        Vec(margin, self.holoSize - margin, 0)
-                    )
-                )
-            )
-
-        local Cx, Cy = UiWorldToPixel(centerT.pos)
-        local LBx, LBy = UiWorldToPixel(LBT.pos)
-        local RTx, RTy = UiWorldToPixel(RTT.pos)
-        local LTx, LTy = UiWorldToPixel(LTT.pos)
-        local RBx, RBy = UiWorldToPixel(RBT.pos)
-
-        if not (
-                (x > LBx) and (x < RTx)
-                and
-                (y < RBy) and (y > LTy)
-            )
-        then
-            return
-        end
-
-        x = (x * 4 + Cx) / 5
-        y = (y * 4 + Cy) / 5
-
-        UiPush()
-        if ProBallistics.visionMode == _nightVisionMode or ProBallistics.visionMode == _nightVisionHiMode then
-            UiColor(lowRand(0, 100) * .001, 1, lowRand(0, 100) * .001, lowRand(50, 75) * .01)
-        else
-            UiColor(1, lowRand(0, 100) * .001, lowRand(0, 50) * .001, lowRand(50, 75) * .01)
-        end
-
-        UiTranslate(x, y)
-        UiAlign("center middle")
-        local w = lowRand(20, 60, 3) * .1
-        UiCircleOutline(math.random(150, 160) * .1, w)
-        UiRotate(self.aimOffset.tilt)
-        UiPop()
-    end,
-    redDotOffset         = nil,
-    drawRedDot           = function(self)
-        local x, y, distance = UiWorldToPixel(self.redDotAimAt)
-        local r, g, b
-
-        UiPush()
-        if ProBallistics.visionMode == _nightVisionMode or ProBallistics.visionMode == _nightVisionHiMode then
-            r, g, b = lowRand(0, 100) * .001, 1, lowRand(0, 100) * .001
-        elseif ProBallistics.visionMode == _thermalVisionMode then
-            local brightness = highRand(50, 100, 3) * .01
-            r, g, b = brightness, brightness, brightness
-        else
-            r, g, b = 1, lowRand(0, 100) * .001, lowRand(0, 50) * .001
-        end
-
-        --Out of sync :/ damn animation synchronisation
-        --self.redDotSource, self.redDotAimAt, = self:getRedDotAim()
-        --for i = 1, 3 do
-        --    DrawLine(
-        --        VecAdd(
-        --            RandomVec(.0025, .005),
-        --            self.redDotSource.pos
-        --        ),
-        --        VecAdd(
-        --            RandomVec(.01, .02),
-        --            self.redDotAimAt
-        --        ),
-        --        r, g, b, lowRand(50, 150, 3) * .001
-        --    )
-        --end
-
-        if not (distance < 0 or self.aimOffset.scoped) then
-            local cPos = GetCameraTransform().pos
-            local hit, hitDistance = QueryRaycast(cPos, VecDir(cPos, self.redDotAimAt), distance)
-            if not (hit and (math.abs(hitDistance - distance) > .05)) then
-                local scale, baseFov, maxDistance = .15, 2, 125
-                distance = math.sqrt(distance)
-
-                scale = scale * (baseFov / math.sqrt(self.aimOffset.fov or ProBallistics.defaultFov))
-                scale = scale * (maxDistance / distance) * self.redDotScale
-
-                UiColor(r, g, b, lowRand(50, 75) * .01)
-                UiTranslate(x, y)
-                UiAlign("center middle")
-                UiCircle(
-                    (self.redDotFlicker and lowRand(10, 40, 3) or 20)
-                    * .1 * scale + 1
-                )
-                UiPop()
-            end
-        end
-    end,
-    holoEnabled          = 0,
-    drawScope            = function(self)
-        if not (self.elements.scope and self.shapes.scope) then
-            return
-        end
-        local aimScoped = self.aimOffset.scoped or 0.01
-        local fadeLevel
-        local scopedLevel = FluidChange:tween(
-            "ScopedLevel",
-            aimScoped,
-            .2
-        )
-        if scopedLevel > 1 then
-            fadeLevel = (scopedLevel - 1) / (aimScoped - 1)
-        else
-            fadeLevel = 0
-        end
-        fadeLevel = FluidChange:tween(
-            "ScopedFadeLevel",
-            fadeLevel,
-            .75
-        )
-        local scopeTransform = GetShapeWorldTransform(self.shapes.scope)
-        local spriteTransform = TransformToParentTransform(
-            scopeTransform,
-            self.elements.scope.offset
-        )
-        if UiHasImage(self.elements.scope.img) and scopedLevel > 1 then
-            UiPush()
-            local x, y, distance = UiWorldToPixel(spriteTransform.pos)
-            if distance > 0 then
-                UiTranslate(x, y)
-                UiColor(0, 0, 0, fadeLevel)
-                UiAlign("center middle")
-                UiScale(
-                    FluidChange:tween(
-                        "scopeScale",
-                        (self.aimOffset.scopeScale or 1),
-                        .5, 1
-                    )
-                )
-                UiImage(self.elements.scope.img)
-            end
-
-            x, y, distance = UiWorldToPixel(self.aimAt)
-            local wind = GetWindVelocity(self.aimAt)
-            local wX, wY = UiWorldToPixel(VecAdd(self.aimAt, wind))
-            local elevation = self.aimAt[2] - self.pos[2]
-            wX = (wX - x) * distance * .0001
-            wY = (wY - y) * distance * .0001
-            UiColor(0, 0, 0, .75)
-            UiAlign("left top")
-            if ProBallistics.scopeWindAid then
-                UiPush()
-                UiTranslate(0, -10)
-                UiRect(wX * 10, 7)
-                UiTranslate(-2, 2)
-                UiRect(7, wY * 10)
-                UiPop()
-            end
-
-            if self.aimOffset.windHelperOffset then
-                UiTranslate(self.aimOffset.windHelperOffset[1], self.aimOffset.windHelperOffset[2])
-                --UiTextOutline(0, 1, 0, 1)
-                --UiColor(0.0, 1, 0.0)
-                UiText(
-                    string.format(
-                        "WH:% 6s",
-                        string.format(
-                            "%2.2f",
-                            FluidChange:tween("wX", wX, .2)
-                        )
-                    )
-                )
-                UiTranslate(0, 40)
-                UiText(
-                    string.format(
-                        "WV:% 6s",
-                        string.format(
-                            "%2.2f",
-                            FluidChange:tween("wY", wY, .2)
-                        )
-                    )
-                )
-                UiTranslate(0, 40)
-                UiText(
-                    string.format(
-                        "D:% 5s",
-                        string.format(
-                            "%3dm",
-                            FluidChange:tween("aimScopeDistance", distance, .2)
-                        )
-                    )
-                )
-                UiTranslate(0, 40)
-                UiText(
-                    string.format(
-                        "E:% 4s",
-                        string.format(
-                            "%2dm",
-                            FluidChange:tween("elevation", elevation, .2)
-                        )
-                    )
-                )
-            end
-            local panMpl = FluidChange:read("panMpl") *
-                FluidChange:tween("scopeZoomSensitivity", self.steady and self.aimOffset.zoomSensitivity or 1, .1)
-            local blur
-            if panMpl < .05 then
-                blur = FluidChange:tween("scopeBlur", 0.05, .05)
-            else
-                blur = FluidChange:tween("scopeBlur", panMpl * (self.steady and 2 or .25), .5)
-            end
-            UiBlur(blur)
-            UiPop()
-        end
-    end,
-    drawUi               = function(self)
-        if self.aimPose == _aimPoseIronSideways and self.holoEnabled > 0 then
-            self:drawHolo()
-        end
-        if self.redDot then
-            self:drawRedDot()
-        end
-        self:drawScope()
-        if ProBallistics.uiMode == _UiOff then
-            return
-        end
-        self.weaponLoadOut:drawUiMinimal()
-    end,
-    debugTick            = function(self, dt)
-        --DebugCross(self.pos)
-    end,
-}
-
 function initHandheld()
     for _, handler in pairs(ProBallistics.registeredWeapons) do
         handler:init()
@@ -883,7 +20,7 @@
 
 function weaponTick(dt)
     local vanillaTool = true
-    if GetPlayerVehicle() == 0 then
+    if GetPlayerVehicle(playerId) == 0 then
         for id, handler in pairs(ProBallistics.registeredWeapons) do
             if GetString("game.player.tool") == id then
                 vanillaTool = false
@@ -891,17 +28,17 @@
             end
         end
     end
-    SetBool("hud.aimdot", vanillaTool)
+    SetBool("hud.aimdot", vanillaTool, true)
     --compatibility with Dynamic FOV mod
     if vanillaTool then
-        SetBool("level.usedynamicfov", true)
+        SetBool("level.usedynamicfov", true, true)
     else
-        SetBool("level.usedynamicfov", false)
+        SetBool("level.usedynamicfov", false, true)
     end
 end
 
 function weaponDraw()
-    if GetPlayerVehicle() == 0 then
+    if GetPlayerVehicle(playerId) == 0 then
         for id, handler in pairs(ProBallistics.registeredWeapons) do
             if GetString("game.player.tool") == id then
                 handler:drawUi()
@@ -909,3 +46,4 @@
         end
     end
 end
+

```

---

# Migration Report: src\weapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\weapons.lua
+++ patched/src\weapons.lua
@@ -1,12 +1,4 @@
-LoadOut = New(Options, {
-    name         = "Test munition",
-    timer        = 0,
-    counter      = 0,
-    counters     = {},
-    trackerMarks = false,
-    magazines    = nil,
-    reloading    = false,
-})
+#version 2
 function LoadOut:constructor()
     if self.magazine ~= nil and self.magazines == nil then
         self.magazines = {}
@@ -16,13 +8,6 @@
     end
 end
 
-WeaponLoadOut = New(Options, {
-    width         = _nilValue,
-    fireMode      = 0,
-    fireModes     = { 0 },
-    seriesCounter = 0,
-})
-
 function WeaponLoadOut:trackerMarks()
     return self:getSelected().trackerMarks or false
 end
@@ -33,7 +18,7 @@
 
 function WeaponLoadOut:processTimers(dt)
     for i, loadOut in ipairs(self.options) do
-        if loadOut.timer > 0 then
+        if loadOut.timer ~= 0 then
             loadOut.timer = loadOut.timer - dt
             if loadOut.timer <= 0 and loadOut.reloading then
                 loadOut.reloading = false
@@ -128,7 +113,7 @@
 
 function WeaponLoadOut:processLoadOutTimers(loadOut, shell)
     local selectedAmmoLoadOut = loadOut.selected
-    if self.fireMode > 0 then
+    if self.fireMode ~= 0 then
         self.seriesCounter = self.seriesCounter + shell.burst
     end
 
@@ -246,143 +231,3 @@
     return w, h
 end
 
-CommanderPlaneWeaponLoadOut = New(WeaponLoadOut, {
-    selected = 4,
-    options  = {
-        New(LoadOut,
-            {
-                name      = "M134D",
-                options   = { munition12mmFMJ, munition12mmAP, munition12mmIncendiary },
-                magazines = {
-                    {
-                        size   = 600,
-                        reload = .75,
-                        total  = 6000,
-                    },
-                    {
-                        size   = 400,
-                        reload = .75,
-                        total  = 4000,
-                    },
-                    {
-                        size   = 400,
-                        reload = .75,
-                        total  = 2000,
-                    },
-                },
-            }
-        ),
-        New(LoadOut,
-            {
-                name      = "GAU-8/A",
-                options   = {
-                    munition30mmDU, munition45mmHE, munition40mmAP, munition30mmAB, munition30mmIncAB, munition30mmInc
-                },
-                magazines = {
-                    {
-                        size   = 360,
-                        reload = .75,
-                        total  = 360 * 8,
-                    },
-                    {
-                        size   = 120,
-                        reload = 1,
-                        total  = 120 * 8,
-                    },
-                    {
-                        size   = 240,
-                        reload = 1,
-                        total  = 120 * 8,
-                    },
-                    {
-                        size   = 16,
-                        reload = 1,
-                        total  = 16 * 24,
-                    },
-                    {
-                        size   = 24,
-                        reload = 1.5,
-                        total  = 24 * 24,
-                    },
-                    {
-                        size   = 24,
-                        reload = 1.5,
-                        total  = 24 * 24,
-                    },
-                },
-            }
-        ),
-        New(LoadOut,
-            {
-                name         = "Tactical Support",
-                trackerMarks = true,
-                options      = {
-                    --munition250mmSR, munition500mmSR,
-                    munition150mmLRM,munitionBMxHyS,  munitionMRVx5, munitionMRVx10, munitionMRVx10SR
-                }
-            }
-        ),
-        New(LoadOut,
-            {
-                name         = "Rockets",
-                trackerMarks = true,
-                selected     = 3,
-                options      = {
-                    munition50mmRocket, munition40mmRocketSalvo, munition100mmRocketGuided, munition150mmGuided,
-                    munition150mmFuel, munition150mmSR,
-                    munition150mmRocketGuidedFrag, munition100mmGuidedSCHE, munition100mmGuidedSCFrag,
-                },
-                magazines    = {
-                    {
-                        size   = 6,
-                        reload = 1,
-                    },
-                },
-            }
-        ),
-        New(LoadOut,
-            {
-                name         = "Artillery",
-                trackerMarks = true,
-                selected     = 1,
-                options      = {
-                    munition75mmArtillerySalvo,
-                    munition150mmArtillery,
-                    munition150mmArtilleryAP,
-                },
-                magazines    = {
-                    {
-                        size   = 6,
-                        reload = 2,
-                    },
-                },
-            }
-        ),
-        New(LoadOut,
-            {
-                name         = "Missiles",
-                trackerMarks = true,
-                selected     = 3,
-                options      = {
-                    munition200mmRocketBunkerBuster, munition100mmVisRocketHE, --[[munitionExosetMissile,]]
-                    munitionTomahawkMissile, munitionStarkMissile
-                }
-            }
-        ),
-        New(LoadOut,
-            {
-                name         = "Bombs",
-                trackerMarks = true,
-                options      = {
-                    munitionBomb100lb,
-                    munitionBomb200lb,
-                    munitionBomblet5lb,
-                },
-                magazines    = {
-                    nil,
-                    nil,
-                },
-            }
-        ),
-    }
-})

```
