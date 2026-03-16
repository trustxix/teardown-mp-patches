# Migration Report: environment.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/environment.lua
+++ patched/environment.lua
@@ -1,3 +1,4 @@
+#version 2
 function GetCurrentEnvironment()
     local env = {}
 
@@ -48,4 +49,5 @@
     env.waterhurt = GetEnvironmentProperty('waterhurt')
 
     return env
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
@@ -1,112 +1 @@
-ModName = 'Improved Simple Tornado'
-
-env = {}
-
-tornadoMenu = false
-menuKey = 'L'
-waitForKey = false
-mapBounds = {}
-
-originalSkybox = ''
-
-Debug = false
-
-#include "vk_filtered_keys.lua"
-#include "vk_utils.lua"
-#include "tornado.lua"
-#include "menu.lua"
-
-function init()
-	AddKeyNE('tornado.speed', 60, EDType.Float)
-	AddKeyNE('tornado.SubvortRadius', 50, EDType.Float) 
-	AddKeyNE('tornado.SubvortStrength', 50, EDType.Float)
-	AddKeyNE('tornado.SubvortSize', 50, EDType.Float)
-	AddKeyNE('tornado.Dirt_cloud_Color_R', 100, EDType.Float)
-	AddKeyNE('tornado.Dirt_cloud_Color_G', 100, EDType.Float)
-	AddKeyNE('tornado.Dirt_cloud_Color_B', 100, EDType.Float)
-	AddKeyNE('tornado.Color_R', 100, EDType.Float)
-	AddKeyNE('tornado.Color_G', 100, EDType.Float)
-	AddKeyNE('tornado.Color_B', 100, EDType.Float)
-	AddKeyNE('tornado.Dirt_cloud_Transparency', 100, EDType.Float)
-	AddKeyNE('tornado.Transparency', 100, EDType.Float)
-	AddKeyNE('tornado.Rope_Amount', 15)
-	AddKeyNE('tornado.Rope_Speed', 10)
-	AddKeyNE('tornado.pull_radius', 28)
-	AddKeyNE('tornado.Sim_Quality', 28)
-	AddKeyNE('tornado.strength', 30)
-	AddKeyNE('tornado.rotate_speed', 8)
-	AddKeyNE('tornado.min_radius', 1)
-	AddKeyNE('tornado.max_radius', 8)
-	AddKeyNE('tornado.height', 130)
-	AddKeyNE('tornado.MultipleVortex', false, EDType.Bool)
-	AddKeyNE('tornado.CondensationalFunnel', false, EDType.Bool)
-	AddKeyNE('tornado.DestructionParticles', true, EDType.Bool)
-	AddKeyNE('tornado.WindfieldEffects', true, EDType.Bool)
-	AddKeyNE('tornado.Firenado', false, EDType.Bool)
-	AddKeyNE('tornado.randomize', false, EDType.Bool)
-	AddKeyNE('tornado.affect_weather', false, EDType.Bool)
-	AddKeyNE('tornado.pull_player', true, EDType.Bool)
-	AddKeyNE('tornado.damage_player', false, EDType.Bool)
-	AddKeyNE('tornado.camera_shake', true, EDType.Bool)
-	AddKeyNE('tornado.light_flicker', false, EDType.Bool)
-	AddKeyNE('tornado.Ground_Scour', true, EDType.Bool)
-	AddKeyNE('tornado.Debris', true, EDType.Bool)
-	AddKeyNE('tornado.Dirt_cloud', true, EDType.Bool)
-	AddKeyNE('tornado.Wall_cloud', true, EDType.Bool)
-	AddKeyNE('tornado.particle_collision', true, EDType.Bool)
-	AddKeyNE('tornado.dirtparticle_collision', true, EDType.Bool)
-	AddKeyNE('tornado.Realistic_Damage', false, EDType.Bool)
-	AddKeyNE('tornado.state', Tornado.states['STATIC'])
-	AddKeyNE('show_lights', false, EDType.Bool)
-	AddKeyNE('menuKey', 'L')
-
-	menuKey = GetKey('menuKey')
-
-	Colours.SliderBackground = Colours.New('#262626')
-    Colours.MenuBackground = Colours.New({38, 38, 38, 155})
-
-	originalSkybox = GetEnvironmentProperty('skybox')
-
-	Tornado.Initialize()
-end
-
-function tick(dt)
-	if Tornado and Tornado.Tick then
-		Tornado.Tick(dt)
-	end
-
-    if not waitForKey and InputPressed(menuKey) then
-        tornadoMenu = not tornadoMenu
-    end
-
-    if waitForKey then
-        lastKeyPressed = InputLastPressedKey()
-        if lastKeyPressed ~= '' and not IsKeyFiltered(lastKeyPressed) then
-            waitForKey = false
-            menuKey = lastKeyPressed
-            SetKey('menuKey', menuKey)
-        end
-
-        if InputPressed('esc') then
-            waitForKey = false
-        end
-    end
-
-	if PauseMenuButton('Tornado Options') then
-		tornadoMenu = not tornadoMenu
-	end
-end
-
-function draw()
-	if tornadoMenu then
-		UiPush()
-			--[[ Initial Setup ]]--
-			UiMakeInteractive()
-			UiFont('regular.ttf', 26)
-			UiBlur(0.75)
-			UiButtonPressColor(1, 1, 1, 1)
-
-			DrawMenu()
-		UiPop()
-	end
-end+#version 2

```

---

# Migration Report: menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/menu.lua
+++ patched/menu.lua
@@ -1,885 +1 @@
-#include "Tornado.lua"
-#include "vk_utils.lua"
-
----@param colour table
----@param alpha number
-function VUIColor(colour, alpha)
-    UiColor(GetColour(colour, alpha))
-end
-
----@param colour table
----@param alpha number
-function VUIButtonHoverColor(colour, alpha)
-    UiButtonHoverColor(GetColour(colour, alpha))
-end
-
----@param colour table
----@param alpha number
-function VUIColorFilter(colour, alpha)
-    UiColorFilter(GetColour(colour, alpha))
-end
-
-Colours = {
-    White = { 1, 1, 1, 1 },
-    Black = { 0, 0, 0, 1 },
-    Red = { 1, 0, 0, 1 },
-    Green = { 0, 1, 0, 1 },
-    Blue = { 0, 0, 1, 1 },
-
-    Cyan = { 0, 1, 1, 1 },
-
-    ---@param colour any
-    ---@return table
-    New = function(colour)
-        if type(colour) == 'table' then
-            return RGBToSomething(colour)
-        elseif type(colour) == 'string' then
-            return RGBToSomething(HexToRGB(colour))
-        else
-            return colour
-        end
-    end
-}
-
-local ButtonColour = Colours.New({55, 55, 55, 155})
-
-local uiWidth = 1200
-local uiHeight = 650
-local startPos = 130
-
-local function SliderBig(name, posx, posy, width, height, min, max, var, key, default, float)
-    local value
-    if not float then
-        value = GetKey(key)
-    else
-       value = GetKey(key, EDType.Float)
-    end
-
-    UiPush()
-        --[[ Slider Text ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 190, posy + - 20)
-        UiText(name)
-    UiPop()
-
-    UiPush()
-        --[[ Text ]]--
-        UiTranslate(posx + value + startPos / 2 + 65 , posy - 40)
-        if float then
-            if value >= max then
-                UiText(string.format('0.%d', value))
-            else
-                UiText(string.format('0.0%d', value))
-            end
-        else
-            UiText(tostring(value))
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Slider Background ]]--
-        UiTranslate(posx + startPos + UiCenter() + 490 - uiWidth, posy - 20)
-        VUIColor(Colours.SliderBackground)
-        UiRect(width, 20)
-    UiPop()
-
-    UiPush()
-        --[[ Slider ]]--
-        UiTranslate(posx + startPos, posy - 20)
-        VUIColor(Colours.White)
-        if float then
-            Tornado[var] = UiSlider('ui/common/dot.png', 'x', value, min, max)
-            SetKey(key, Tornado[var], EDType.Float)
-        else
-            Tornado[var] = math.floor(UiSlider('ui/common/dot.png', 'x', value, min, max))
-            SetKey(key, Tornado[var])
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Reset ]]--
-        UiTranslate(UiCenter() - 130 / 2 + 250, posy - 20)
-        UiButtonImageBox('MOD/sprites/ui/revert.png', 1, 1, 1, 1, 1, 1)
-        if UiBlankButton(20, 20) then
-            if not float then
-                SetKey(key, default)
-            else
-                SetKey(key, default, EDType.Float)
-            end
-        end
-    UiPop()
-end
-
-local function Slider(name, posx, posy, width, height, min, max, var, key, default, float)
-    local value
-    if not float then
-        value = GetKey(key)
-    else
-       value = GetKey(key, EDType.Float)
-    end
-
-    UiPush()
-        --[[ Slider Text ]]--
-        UiTranslate(posx, posy - 20)
-        UiText(name)
-    UiPop()
-
-    UiPush()
-        --[[ Text ]]--
-        UiTranslate(posx + value + startPos / 2 + 15 , posy - 40)
-        if float then
-            if value >= max then
-                UiText(string.format('0.%d', value))
-            else
-                UiText(string.format('0.0%d', value))
-            end
-        else
-            UiText(tostring(value))
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Slider Background ]]--
-        UiTranslate(posx + startPos, posy - 20)
-        VUIColor(Colours.SliderBackground)
-        UiRect(width, 20)
-    UiPop()
-
-    UiPush()
-        --[[ Slider ]]--
-        UiTranslate(posx + startPos - startPos / 2 + 19, posy - 20)
-        VUIColor(Colours.White)
-        if float then
-            Tornado[var] = UiSlider('ui/common/dot.png', 'x', value, min, max)
-            SetKey(key, Tornado[var], EDType.Float)
-        else
-            Tornado[var] = math.floor(UiSlider('ui/common/dot.png', 'x', value, min, max))
-            SetKey(key, Tornado[var])
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Reset ]]--
-        UiTranslate(UiCenter() - 130 / 2 + 250, posy - 20)
-        UiButtonImageBox('MOD/sprites/ui/revert.png', 1, 1, 1, 1, 1, 1)
-        if UiBlankButton(20, 20) then
-            if not float then
-                SetKey(key, default)
-            else
-                SetKey(key, default, EDType.Float)
-            end
-        end
-    UiPop()
-end
-
-local function Slider2(name, posx, posy, width, height, min, max, var, key, default, float)
-    local value
-    if not float then
-        value = GetKey(key)
-    else
-       value = GetKey(key, EDType.Float)
-    end
-
-    UiPush()
-        --[[ Slider Text ]]--
-        UiTranslate(posx, posy - 20)
-        UiText(name)
-    UiPop()
-
-    UiPush()
-        --[[ Text ]]--
-        UiTranslate(posx + value + startPos / 2 + 15 , posy - 40)
-        if float then
-            if value >= max then
-                UiText(string.format('0.%d', value))
-            else
-                UiText(string.format('0.0%d', value))
-            end
-        else
-            UiText(tostring(value))
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Slider Background ]]--
-        UiTranslate(posx + startPos, posy - 20)
-        VUIColor(Colours.SliderBackground)
-        UiRect(width, 20)
-    UiPop()
-
-    UiPush()
-        --[[ Slider ]]--
-        UiTranslate(posx + startPos - startPos / 2 + 15, posy - 20)
-        VUIColor(Colours.White)
-        if float then
-            Tornado[var] = UiSlider('ui/common/dot.png', 'x', value, min, max)
-            SetKey(key, Tornado[var], EDType.Float)
-        else
-            Tornado[var] = math.floor(UiSlider('ui/common/dot.png', 'x', value, min, max))
-            SetKey(key, Tornado[var])
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Reset ]]--
-        UiTranslate(UiCenter() - 130 / 2 + 568, posy - 20)
-        UiButtonImageBox('MOD/sprites/ui/revert.png', 1, 1, 1, 1, 1, 1)
-        if UiBlankButton(20, 20) then
-            if not float then
-                SetKey(key, default)
-            else
-                SetKey(key, default, EDType.Float)
-            end
-        end
-    UiPop()
-end
-
-local function Slider3(name, posx, posy, width, height, min, max, var, key, default, float)
-    local value
-    if not float then
-        value = GetKey(key)
-    else
-       value = GetKey(key, EDType.Float)
-    end
-
-    UiPush()
-        --[[ Slider Text ]]--
-        UiTranslate(posx-10, posy - 20)
-        UiText(name)
-    UiPop()
-
-    UiPush()
-        --[[ Text ]]--
-        UiTranslate(posx + value + startPos / 2 + 15 , posy - 40)
-        if float then
-            if value >= max then
-                UiText(string.format('0.%d', value))
-            else
-                UiText(string.format('0.0%d', value))
-            end
-        else
-            UiText(tostring(value))
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Slider Background ]]--
-        UiTranslate(posx + startPos, posy - 20)
-        VUIColor(Colours.SliderBackground)
-        UiRect(width, 20)
-    UiPop()
-
-    UiPush()
-        --[[ Slider ]]--
-        UiTranslate(posx + startPos - startPos / 2 + 15, posy - 20)
-        VUIColor(Colours.White)
-        if float then
-            Tornado[var] = UiSlider('ui/common/dot.png', 'x', value, min, max)
-            SetKey(key, Tornado[var], EDType.Float)
-        else
-            Tornado[var] = math.floor(UiSlider('ui/common/dot.png', 'x', value, min, max))
-            SetKey(key, Tornado[var])
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Reset ]]--
-        UiTranslate(UiCenter() - 130 / 2 + 968, posy - 20)
-        UiButtonImageBox('MOD/sprites/ui/revert.png', 1, 1, 1, 1, 1, 1)
-        if UiBlankButton(20, 20) then
-            if not float then
-                SetKey(key, default)
-            else
-                SetKey(key, default, EDType.Float)
-            end
-        end
-    UiPop()
-end
-
-local function SliderCol(name, posx, posy, width, height, min, max, var, key, default, float)
-    local value
-    if not float then
-        value = GetKey(key)
-    else
-       value = GetKey(key, EDType.Float)
-    end
-
-    UiPush()
-        --[[ Slider Text ]]--
-        UiTranslate(posx - 15, posy - 20)
-        UiText(name)
-    UiPop()
-
-    UiPush()
-        --[[ Text ]]--
-        UiTranslate(posx + value + startPos / 2 + 15 , posy - 40)
-        if float then
-            if value >= max then
-                UiText(string.format('0.%d', value))
-            else
-                UiText(string.format('0.0%d', value))
-            end
-        else
-            UiText(tostring(value))
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Slider Background ]]--
-        UiTranslate(posx + startPos, posy - 20)
-        VUIColor(Colours.SliderBackground)
-        UiRect(width, 20)
-    UiPop()
-
-    UiPush()
-        --[[ Slider ]]--
-        UiTranslate(posx + startPos - startPos / 2 + 15, posy - 20)
-        VUIColor(Colours.White)
-        if float then
-            Tornado[var] = UiSlider('ui/common/dot.png', 'x', value, min, max)
-            SetKey(key, Tornado[var], EDType.Float)
-        else
-            Tornado[var] = math.floor(UiSlider('ui/common/dot.png', 'x', value, min, max))
-            SetKey(key, Tornado[var])
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Reset ]]--
-        UiTranslate(UiCenter() - 130 / 2 + 600, posy - 20)
-        UiButtonImageBox('MOD/sprites/ui/revert.png', 1, 1, 1, 1, 1, 1)
-        if UiBlankButton(20, 20) then
-            if not float then
-                SetKey(key, default)
-            else
-                SetKey(key, default, EDType.Float)
-            end
-        end
-    UiPop()
-end
-
-local function SliderTransparency(name, posx, posy, width, height, min, max, var, key, default, float)
-    local value
-    if not float then
-        value = GetKey(key)
-    else
-       value = GetKey(key, EDType.Float)
-    end
-
-    UiPush()
-        --[[ Slider Text ]]--
-        UiTranslate(posx-35, posy - 20)
-        UiText(name)
-    UiPop()
-
-    UiPush()
-        --[[ Text ]]--
-        UiTranslate(posx + value + startPos / 2 + 15 , posy - 40)
-        if float then
-            if value >= max then
-                UiText(string.format('0.%d', value))
-            else
-                UiText(string.format('0.0%d', value))
-            end
-        else
-            UiText(tostring(value))
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Slider Background ]]--
-        UiTranslate(posx + startPos, posy - 20)
-        VUIColor(Colours.SliderBackground)
-        UiRect(width, 20)
-    UiPop()
-
-    UiPush()
-        --[[ Slider ]]--
-        UiTranslate(posx + startPos - startPos / 2 + 15, posy - 20)
-        VUIColor(Colours.White)
-        if float then
-            Tornado[var] = UiSlider('ui/common/dot.png', 'x', value, min, max)
-            SetKey(key, Tornado[var], EDType.Float)
-        else
-            Tornado[var] = math.floor(UiSlider('ui/common/dot.png', 'x', value, min, max))
-            SetKey(key, Tornado[var])
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Reset ]]--
-        UiTranslate(UiCenter() - 130 / 2 + 600, posy - 20)
-        UiButtonImageBox('MOD/sprites/ui/revert.png', 1, 1, 1, 1, 1, 1)
-        if UiBlankButton(20, 20) then
-            if not float then
-                SetKey(key, default)
-            else
-                SetKey(key, default, EDType.Float)
-            end
-        end
-    UiPop()
-end
-
-function DrawMenu()
-    UiPush()
-        --[[ Background ]]--
-        UiTranslate(UiCenter(), UiMiddle())
-        UiAlign('center middle')
-        VUIColor(Colours.MenuBackground)
-        UiColorFilter(1, 1, 1, 0.5)
-        UiRect(uiWidth, uiHeight)
-    UiPop()
-
-    VUIColor(Colours.White)
-    UiAlign("center middle")
-
-    -- name, posx, posy, width, height, min, max, value, key, default, float
-    SliderBig('Sim Quality', UiCenter() - uiWidth / 2 + 131, UiMiddle() - 275, 500, 0, 0, 500, 'SimQuality', 'tornado.Sim_Quality', 28)
-    SliderBig('Pull Radius', UiCenter() - uiWidth / 2 + 131, UiMiddle() - 235, 500, 0, 0, 500, 'pullRadius', 'tornado.pull_radius', 28)
-    SliderBig('Height', UiCenter() - uiWidth / 2 + 131, UiMiddle() - 190, 500, 0, 0, 500, 'height', 'tornado.height', 130)
-    Slider('Rope Amount', UiCenter() - uiWidth / 2 + 580, UiMiddle() - 140, 100, 0, 0.05, 100, 'ropefactor', 'tornado.Rope_Amount', 15)
-    Slider('Speed', UiCenter() - uiWidth / 2 + 580, UiMiddle() - 100, 100, 0, 0.05, 100, 'speed', 'tornado.speed', 10)
-    Slider('Strength', UiCenter() - uiWidth / 2 + 580, UiMiddle() - 60, 100, 0, 0.05, 100, 'strength', 'tornado.strength', 30)
-    Slider('Min Radius', UiCenter() - uiWidth / 2 + 580, UiMiddle() - 20, 100, 0, 0, 100, 'min_radius', 'tornado.min_radius', 1)
-    Slider('Max Radius', UiCenter() - uiWidth / 2 + 580, UiMiddle() + 20, 100, 0, 0, 100, 'max_radius', 'tornado.max_radius', 8)
-    Slider2('Rotate Speed', UiCenter() - uiWidth / 2 + 900, UiMiddle() - 235, 100, 100, 0, 100, 'rotate_speed', 'tornado.rotate_speed', 8)
-    Slider2('Rope Speed', UiCenter() - uiWidth / 2 + 900, UiMiddle() - 275, 100, 100, 0, 100, 'RopeSpeed', 'tornado.Rope_Speed', 10)
-    SliderCol('Dirtcloud Color R', UiCenter() - uiWidth / 2 + 930, UiMiddle() - 180, 100, 100, 0, 100,  'DirtcloudColorR', 'tornado.Dirt_cloud_Color_R', 100)
-    SliderCol('Dirtcloud Color G', UiCenter() - uiWidth / 2 + 930, UiMiddle() - 140, 100, 100, 0, 100,  'DirtcloudColorG', 'tornado.Dirt_cloud_Color_G', 100)
-    SliderCol('Dirtcloud Color B', UiCenter() - uiWidth / 2 + 930, UiMiddle() - 99, 100, 100, 0, 100,  'DirtcloudColorB', 'tornado.Dirt_cloud_Color_B', 100)
-    SliderCol('Tornado Color R', UiCenter() - uiWidth / 2 + 930, UiMiddle() - 60, 100, 100, 0, 100,  'ColorR', 'tornado.Color_R', 100)
-    SliderCol('Tornado Color G', UiCenter() - uiWidth / 2 + 930, UiMiddle() - 20, 100, 100, 0, 100,  'ColorG', 'tornado.Color_G', 100)
-    SliderCol('Tornado Color B', UiCenter() - uiWidth / 2 + 930, UiMiddle() + 20, 100, 100, 0, 100,  'ColorB', 'tornado.Color_B', 100)
-    SliderTransparency('Tornado Transparency', UiCenter() - uiWidth / 2 + 930, UiMiddle() + 240, 100, 100, 0, 100,  'Transparency', 'tornado.Transparency', 100)
-    SliderTransparency('Dirtcloud Transparency', UiCenter() - uiWidth / 2 + 930, UiMiddle() + 280, 100, 100, 0, 100,  'DirtcloudTransparency', 'tornado.Dirt_cloud_Transparency', 100)
-    
-
-    if Tornado.MultipleVortex then
-
-        UiPush()
-            --[[ Background ]]--
-            UiTranslate( UiCenter()+ 770, UiMiddle() + -175)
-            UiAlign('center middle')
-            VUIColor(Colours.MenuBackground)
-            UiColorFilter(1, 1, 1, 0.5)
-            local uiWidth1 = 330
-            local uiHeight1 = 300
-            UiRect(uiWidth1, uiHeight1)
-        UiPop()
-
-        Slider3('Subvort Radius', UiCenter() - uiWidth / 2 + 1310, UiMiddle() - 240, 100, 0, 0.05, 100, 'SubvortRadius', 'tornado.SubvortRadius', 50)
-        Slider3('Subvort Strength', UiCenter() - uiWidth / 2 + 1310, UiMiddle() - 175, 100, 0, 0, 100, 'SubvortStrength', 'tornado.SubvortStrength', 50)
-        Slider3('Subvort Size', UiCenter() - uiWidth / 2 + 1310, UiMiddle() - 110, 100, 0, 0, 100, 'SubvortSize', 'tornado.SubvortSize', 50)
-
-    end
-
-    if Efpresets == nil then
-    Efpresets = false
-    end
-
-    if Efpresets then
-
-        UiPush()
-            --[[ Background ]]--
-            UiTranslate( UiCenter()- 770, UiMiddle())
-            UiAlign('center middle')
-            VUIColor(Colours.MenuBackground)
-            UiColorFilter(1, 1, 1, 0.5)
-            local uiWidth1 = 330
-            local uiHeight1 = 650
-            UiRect(uiWidth1, uiHeight1)
-        UiPop()
-        
-        UiPush()
-            UiTranslate( UiCenter()- 770, UiMiddle() + 260)
-            UiText("Not 100% accurate to real life.")
-        UiPop()
-
-        UiPush()
-            UiTranslate(UiCenter() - 770, UiMiddle() - 280)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('Randomize', 300, 60) then
-                SetKey("Tornado.strength", math.random(0,100))
-                Efpresets = false
-            end
-        UiPop()
-
-        UiPush()
-            UiTranslate(UiCenter() - 770, UiMiddle() - 210)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('EFU', 300, 60) then
-                SetKey("Tornado.strength", math.random(0,20))
-                Efpresets = false
-            end
-        UiPop()
-
-        UiPush()
-            UiTranslate(UiCenter() - 770, UiMiddle() - 140)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('EF0', 300, 60) then
-                SetKey("Tornado.strength", math.random(20, 26))
-                Efpresets = false
-            end
-        UiPop()
-    
-        UiPush()
-            UiTranslate(UiCenter() - 770, UiMiddle() - 70)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('EF1', 300, 60) then
-                SetKey("Tornado.strength", math.random(27, 31))
-                Efpresets = false
-            end
-        UiPop()
-    
-        UiPush()
-            UiTranslate(UiCenter() - 770, UiMiddle() - 0)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('EF2', 300, 60) then
-                SetKey("Tornado.strength", math.random(32, 39))
-                Efpresets = false
-            end
-        UiPop()
-    
-        UiPush()
-            UiTranslate(UiCenter() - 770, UiMiddle()+ 70)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('EF3', 300, 60) then
-                SetKey("Tornado.strength", math.random(40, 49))
-                Efpresets = false
-            end
-        UiPop()
-    
-        UiPush()
-
-            UiTranslate(UiCenter() - 770, UiMiddle() + 140)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('EF4', 300, 60) then
-                Efpresets = false
-                SetKey("Tornado.strength", math.random(50, 69))
-            end
-        UiPop()
-    
-        UiPush()
-            UiTranslate(UiCenter() - 770, UiMiddle() + 210)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('EF5', 300, 60) then
-                Efpresets = false
-                SetKey("Tornado.strength", math.random(70, 100))
-            end
-        UiPop()    
-
-    end
-
-    if Tornado.pullPlayer then
-        UiPush()
-            --[[ Damage player Button ]]--
-            if Tornado.DamagePlayer then VUIColor(Colours.Red) end
-
-            UiTranslate(UiCenter() - uiWidth / 2 + 250, UiMiddle() + 205)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton('Damage Player', 200, 40) then
-                Tornado.DamagePlayer = not Tornado.DamagePlayer
-                SetKey('tornado.damage_player', Tornado.DamagePlayer, EDType.Bool)
-            end
-        UiPop()
-    end
-
-
-    UiPush()
-    --[[ Ef preset Button ]]--
-    if Efpresets then VUIColor(Colours.Black) end
-    UiTranslate(UiCenter() - uiWidth / 2 + 130, UiMiddle() + 155)
-    UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-    if UiTextButton('Set EF', 200, 40) then
-        Efpresets = not Efpresets
-    end
-    UiPop()
-
-
-    UiPush()
-        --[[ Spawn Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 370, UiMiddle() + 55)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Spawn', 250, 40) then
-            Tornado.Spawn(Vec(0, 0, 0), Vec(0, 0, 0))
-            Tornado.active = true
-        end
-    UiPop()
- 
-    UiPush()
-    if Tornado.GroundScour then VUIColor(Colours.Cyan) end
-        --[[ Scouring Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 370, UiMiddle() + 0)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Scouring (Visual Only)', 250, 40) then
-            Tornado.GroundScour = not Tornado.GroundScour
-            SetKey('tornado.Ground_Scour', Tornado.GroundScour, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.Wallcloud then VUIColor(Colours.Cyan) end
-        --[[ Wallcloud Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 370, UiMiddle() - 55)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Wall cloud', 250, 40) then
-            Tornado.Wallcloud = not Tornado.Wallcloud
-            SetKey('tornado.Wall_cloud', Tornado.Wallcloud, EDType.Bool)
-        end
-    UiPop()
-    
-    UiPush()
-    if Tornado.Dirtcloud then VUIColor(Colours.Cyan) end
-        --[[ Dirtcloud Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 370, UiMiddle() - 110)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Dirt cloud', 250, 40) then
-            Tornado.Dirtcloud = not Tornado.Dirtcloud
-            SetKey('tornado.Dirt_cloud', Tornado.Dirtcloud, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.Debris then VUIColor(Colours.Cyan) end
-        --[[ Debris Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 370, UiMiddle() - 165)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Debris', 250, 40) then
-            Tornado.Debris = not Tornado.Debris
-            SetKey('tornado.Debris', Tornado.Debris, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.Firenado then VUIColor(Colours.Red) end
-        --[[ Firenado Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 130, UiMiddle() - 165)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Firenado', 200, 40) then
-            Tornado.Firenado = not Tornado.Firenado
-            SetKey('tornado.Firenado', Tornado.Firenado, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.MultipleVortex then VUIColor(Colours.Blue) end
-        --[[ MultiVort Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 130, UiMiddle() - 110)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('MultiVortex', 200, 40) then
-            Tornado.MultipleVortex = not Tornado.MultipleVortex
-            SetKey('tornado.MultipleVortex', Tornado.MultipleVortex, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.CondensationalFunnel then VUIColor(Colours.Cyan) end
-        --[[ Condensation Tornado Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 130, UiMiddle() - 55)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Condensational', 200, 40) then
-            Tornado.CondensationalFunnel = not Tornado.CondensationalFunnel
-            SetKey('tornado.CondensationalFunnel', Tornado.CondensationalFunnel, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.DestructionParticles then VUIColor(Colours.Cyan) end
-        --[[ Destruction Effects Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 130, UiMiddle() - 0)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Destruction Effects', 200, 40) then
-            Tornado.DestructionParticles = not Tornado.DestructionParticles
-            SetKey('tornado.DestructionParticles', Tornado.DestructionParticles, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.WindfieldEffects then VUIColor(Colours.Cyan) end
-        --[[ Windfield Visuals Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 130, UiMiddle() + 55)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Windfield Effects', 200, 40) then
-            Tornado.WindfieldEffects = not Tornado.WindfieldEffects
-            SetKey('tornado.WindfieldEffects', Tornado.WindfieldEffects, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    if Tornado.RealisticDamage then VUIColor(Colours.Cyan) end
-        --[[ Realistic Damage Visuals Button ]]--
-        UiTranslate(UiCenter() - uiWidth / 2 + 130, UiMiddle() + 105)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('"Realistic" Damage', 200, 40) then
-            Tornado.RealisticDamage = not Tornado.RealisticDamage
-            SetKey('tornado.Realistic_Damage', Tornado.RealisticDamage, EDType.Bool)
-        end
-    UiPop()    
-
-    UiPush()
-        --[[ Despawn Button ]]--
-        UiTranslate(UiCenter() + 5, UiMiddle() + 55)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Despawn', 120, 40) then
-            if Tornado.active then
-                -- for light, _ in pairs(Lights) do
-                --     SetLightEnabled(light, true)
-                -- end
-
-                for k, v in pairs(DefaultEnvironment) do
-                    if type(v) == 'table' then
-                        SetEnvironmentProperty(k, v[1], v[2], v[3], v[4])
-                    else
-                        SetEnvironmentProperty(k, v)
-                    end
-                end
-                Tornado.active = false
-            end
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Show Lights Button ]]--
-        if Tornado.showLights then VUIColor(Colours.Cyan) end
-
-        UiTranslate(UiCenter() + 130, UiMiddle() + 55)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Show Lights', 120, 40) then
-            Tornado.showLights = not Tornado.showLights
-            SetKey('show_lights', Tornado.showLights, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Freeroam Button ]]--
-        if Tornado.state == Tornado.states['FREEROAM'] then VUIColor(Colours.Cyan) end
-
-        UiTranslate(UiCenter() - uiWidth / 2 + 370, UiMiddle() + 105)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Freeroam', 250, 40) then
-            if Tornado.state == Tornado.states['FREEROAM'] then
-                Tornado.SetState('STATIC')
-            else
-                Tornado.SetState('FREEROAM')
-            end
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Follow Player Button ]]--
-        if Tornado.state == Tornado.states['FOLLOWING'] then VUIColor(Colours.Cyan) end
-
-        UiTranslate(UiCenter() + 5, UiMiddle() + 105)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Follow', 120, 40) then
-            if Tornado.state == Tornado.states['FOLLOWING'] then
-                Tornado.SetState('STATIC')
-            else
-                Tornado.SetState('FOLLOWING')
-            end
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Affect Weather Button ]]--
-        if Tornado.affectWeather then VUIColor(Colours.Cyan) end
-
-        UiTranslate(UiCenter() + 130, UiMiddle() + 105)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Weather', 120, 40) then
-            Tornado.affectWeather = not Tornado.affectWeather
-            SetKey('tornado.affect_weather', Tornado.affectWeather, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Pull Player Button ]]--
-        if Tornado.pullPlayer then VUIColor(Colours.Cyan) end
-
-        UiTranslate(UiCenter() - uiWidth / 2 + 370, UiMiddle() + 155)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Pull Player', 250, 40) then
-            Tornado.pullPlayer = not Tornado.pullPlayer
-            SetKey('tornado.pull_player', Tornado.pullPlayer, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-        --[[ Light Flicker Button ]]--
-        if Tornado.lightFlicker then VUIColor(Colours.Cyan) end
-
-        UiTranslate(UiCenter() + 5, UiMiddle() + 155)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Light Flicker', 120, 40) then
-            Tornado.lightFlicker = not Tornado.lightFlicker
-            SetKey('tornado.light_flicker', Tornado.lightFlicker, EDType.Bool)
-        end
-    UiPop()
-
-    UiPush()
-    --[[ Funnel Collide Button ]]--
-    if Tornado.ParticleCollision then VUIColor(Colours.Cyan) end
-
-    UiTranslate(UiCenter() - uiWidth / 2 + 1000, UiMiddle() + 155)
-    UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-    if UiTextButton('Funnel Collision', 250, 40) then
-        Tornado.ParticleCollision = not Tornado.ParticleCollision
-        SetKey('tornado.particle_collision', Tornado.ParticleCollision, EDType.Bool)
-    end
-    UiPop()
-
-    UiPush()
-    --[[ Dirtcloud Collide Button ]]--
-    if Tornado.DirtParticleCollision then VUIColor(Colours.Cyan) end
-
-    UiTranslate(UiCenter() - uiWidth / 2 + 1000, UiMiddle() + 105)
-    UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-    if UiTextButton('Dirtcloud Collision', 250, 40) then
-        Tornado.DirtParticleCollision = not Tornado.DirtParticleCollision
-        SetKey('tornado.dirtparticle_collision', Tornado.DirtParticleCollision, EDType.Bool)
-    end
-    UiPop()
-
-    UiPush()
-        --[[ Shake Button ]]--
-        if Tornado.cameraShake then VUIColor(Colours.Cyan) end
-
-        UiTranslate(UiCenter() + 130, UiMiddle() + 155)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Shake', 120, 40) then
-            Tornado.cameraShake = not Tornado.cameraShake
-            SetKey('tornado.camera_shake', Tornado.cameraShake, EDType.Bool)
-        end
-    UiPop()
-
-    -- Bottom buttons
-    UiPush()
-        --[[ Close Button ]]--
-        UiTranslate(UiCenter() - 120 / 2, UiMiddle() + uiHeight / 2 - 40 / 2 - 10)
-        UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-        if UiTextButton('Close', 120, 40) then
-            tornadoMenu = false
-        end
-    UiPop()
-
-    if not waitForKey then
-        UiPush()
-            --[[ Key Input Button ]]--
-            UiTranslate(UiCenter() + 120 / 2 + 10, UiMiddle() + uiHeight / 2 - 40 / 2 - 10)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            if UiTextButton(menuKey, 120, 40) then
-                waitForKey = true
-            end
-        UiPop()
-    else
-        UiPush()
-            --[[ Key Input Button ]]--
-            UiTranslate(UiCenter() + 120 / 2 + 10, UiMiddle() + uiHeight / 2 - 40 / 2 - 10)
-            UiButtonImageBox("MOD/sprites/ui/square.png", 6, 6, 0, 0, 0, 0.5)
-            UiColor(0.8, 0.8, 0.8, 0.2)
-            if UiTextButton(menuKey, 120, 40) then
-                waitForKey = false
-            end
-        UiPop()
-    end
-end
-
+#version 2

```

---

# Migration Report: tornado.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tornado.lua
+++ patched/tornado.lua
@@ -1,36 +1,6 @@
-#include "environment.lua"
-#include "vk_utils.lua"
-#include "tornado_helper.lua"
-
-DefaultEnvironment = {}
-
-Trees = {}
-Lights = {}
-
+#version 2
 local windSound
 local lightSound
-
-Tornado = {}
-Tornado.pos = Vec(0, 0, 0)
-Tornado.age = 0
-Tornado.lifetime = 0
-Tornado.spawnAngle = 0
-Tornado.active = false
-Tornado.sound = nil
-
-Tornado.states = {
-    ['STATIC'] = 0,
-    ['FOLLOWING'] = 1,
-    ['FREEROAM'] = 2
-}
-
-function Tornado.SetState(state)
-    if Tornado.states[state] then
-        Tornado.state = Tornado.states[state]
-        SetKey('tornado.state', Tornado.state)
-    end
-end
-
 local BodyTypes = {
     ['GROUND'] = 0,
     ['VEHICLE'] = 1,
@@ -40,6 +10,14 @@
     ['LARGE_OBJECT'] = 5,
     ['ROOF'] = 6
 }
+local lastPosY = 0
+
+function Tornado.SetState(state)
+    if Tornado.states[state] then
+        Tornado.state = Tornado.states[state]
+        SetKey('tornado.state', Tornado.state)
+    end
+end
 
 local function GetBodyType(shape)
     local body = GetShapeBody(shape)
@@ -55,7 +33,7 @@
     if GetBodyVehicle(body) > 0 then return BodyTypes['VEHICLE'] end
 
     local bodyMass = GetBodyMass(body)
-    if bodyMass > 0 then -- Dynamic
+    if bodyMass ~= 0 then -- Dynamic
         if bodyMass <= 1500 then return BodyTypes['SMALL_OBJECT'] end
         if bodyMass > 1500 and bodyMass <= 5000 then return BodyTypes['MEDIUM_OBJECT'] end
         if bodyMass > 5000 then return BodyTypes['LARGE_OBJECT'] end
@@ -145,7 +123,6 @@
     end 
 end
 
-local lastPosY = 0
 local function GetClosestBody()
     local t = GetCameraTransform()
 	local dir = TransformToParentVec(t, {0, 0, -1})
@@ -197,9 +174,7 @@
 
 local function MoveFreeroam(dt)
     local dist = VecSub(Tornado.pos, Tornado.endPos)
-    local pp = GetPlayerTransform().pos
-
-
+    local pp = GetPlayerTransform(playerId).pos
 
     -- DebugWatch('Distance', dist)
 
@@ -251,292 +226,12 @@
 
 local function MoveFollowPlayer()
     Tornado.endPos = Vec(
-        GetPlayerTransform().pos[1],
+        GetPlayerTransform(playerId).pos[1],
         0,
-        GetPlayerTransform().pos[3]
+        GetPlayerTransform(playerId).pos[3]
     )
 
     local targetSubVec = VecScale(VecNormalize(VecSub(Tornado.endPos, Tornado.pos)), Tornado.speed)
     Tornado.pos = VecAdd(Tornado.pos, Vec(targetSubVec[1], 0, targetSubVec[3])) -- Move tornado pos at a constant rate towards the raycast hit pos.
 end
 
-Tornado.Initialize = function()
-	Tornado.sound1 = LoadLoop("MOD/sounds/TornadoClose.ogg")
-    Tornado.sound2 = LoadLoop("MOD/sounds/EarsPoppingBackside.ogg")
-	windSound = LoadLoop('MOD/sounds/AmbientTornadoWind.ogg')
-	lightSound = LoadLoop('light/buzz2.ogg')
-
-    Tornado.speed = GetKey('tornado.speed', EDType.Float)
-    Tornado.ropefactor = GetKey('tornado.Rope_Amount')
-    Tornado.RopeSpeed = GetKey('tornado.Rope_Speed')
-	Tornado.pullRadius = GetKey('tornado.pull_radius')
-    Tornado.SimQuality = GetKey('tornado.Sim_Quality')
-	Tornado.strength = GetKey('tornado.strength')
-	Tornado.rotate_speed = GetKey('tornado.rotate_speed') 
-	Tornado.min_radius = GetKey('tornado.min_radius')
-	Tornado.max_radius = GetKey('tornado.max_radius')
-	Tornado.height = GetKey('tornado.height')
-    Tornado.DirtcloudColorR = GetKey('tornado.Dirt_cloud_Color_R', EDType.Float)
-    Tornado.DirtcloudColorG = GetKey('tornado.Dirt_cloud_Color_G', EDType.Float)
-    Tornado.DirtcloudColorB = GetKey('tornado.Dirt_cloud_Color_B', EDType.Float)
-    Tornado.ColorR = GetKey('tornado.Color_R', EDType.Float)
-    Tornado.ColorB = GetKey('tornado.Color_G', EDType.Float)
-    Tornado.ColorG = GetKey('tornado.Color_B', EDType.Float)
-    Tornado.SubvortRadius = GetKey('tornado.SubvortRadius', EDType.Float) 
-	Tornado.SubvortStrength = GetKey('tornado.SubvortStrength', EDType.Float)
-	Tornado.SubvortSize = GetKey('tornado.SubvortSize', EDType.Float)
-    Tornado.DirtcloudTransparency = GetKey('tornado.Dirt_cloud_Transparency', EDType.Float)
-    Tornado.Transparency = GetKey('tornado.Transparency', EDType.Float)
-    Tornado.ParticleCollision = GetKey('tornado.particle_collision', EDType.Bool)
-    Tornado.MultipleVortex = GetKey('tornado.MultipleVortex', EDType.Bool)
-    Tornado.CondensationalFunnel = GetKey('tornado.CondensationalFunnel', EDType.Bool)
-    Tornado.DestructionParticles = GetKey('tornado.DestructionParticles', EDType.Bool)
-    Tornado.WindfieldEffects = GetKey('tornado.WindfieldEffects', EDType.Bool)
-    Tornado.Firenado = GetKey('tornado.Firenado', EDType.Bool)
-    Tornado.DirtParticleCollision = GetKey('tornado.dirtparticle_collision', EDType.Bool)
-    Tornado.pullPlayer = GetKey('tornado.pull_player', EDType.Bool)
-    Tornado.DamagePlayer = GetKey('tornado.damage_player', EDType.Bool)
-    Tornado.affectWeather = GetKey('tornado.affect_weather', EDType.Bool)
-    Tornado.cameraShake = GetKey('tornado.camera_shake', EDType.Bool)
-    Tornado.lightFlicker = GetKey('tornado.light_flicker', EDType.Bool)
-    Tornado.showLights = GetKey('show_lights', EDType.Bool)
-    Tornado.GroundScour = GetKey('tornado.Ground_Scour', EDType.Bool)
-    Tornado.Wallcloud = GetKey('tornado.Wall_cloud',  EDType.Bool)
-    Tornado.Dirtcloud = GetKey('tornado.Dirt_cloud',  EDType.Bool)
-    Tornado.Debris = GetKey('tornado.Debris',  EDType.Bool)
-    Tornado.RealisticDamage = GetKey('tornado.Realistic_Damage',  EDType.Bool)
-
-	RegisterTool('tornado_controller', 'Tornado Controller')
-    SetBool('game.tool.tornado_controller.enabled', true)
-
-    Tornado.state = GetKey('tornado.state')
-
-end
-
-Tornado.Tick = function(dt)
-
-	local isUsingTool = GetString('game.player.tool') == 'tornado_controller' and (GetPlayerVehicle() == 0)
-	local isShooting = isUsingTool and InputDown('lmb')
-    SetToGround()
-    if Tornado.active then
-
-        if Tornado.GroundScour and not Tornado.MultipleVortex then
-            local pick = math.random(1,2)
-            if pick == 1 then
-                Paint(Tornado.pos, rnd(0.001, 1 + Tornado.min_radius), "explosion", 1)
-            end
-        end
-        local fadeIn = 5.0
-
-        if Tornado.age < fadeIn then
-            Tornado.amount = Tornado.age / fadeIn
-        end
-
-        local speed = GetKey('tornado.speed', EDType.Float)
-        if speed > 0 and speed < 100 then
-            speed = tonumber(string.format('0.0%d', speed))
-        else
-            speed = tonumber(string.format('0.%d', speed))
-        end
-
-        Tornado.speed = speed * 5
-        
-        PlayLoop(Tornado.sound1, Tornado.pos, 1 + Tornado.strength * 0.13 + Tornado.min_radius * 1 + Tornado.pullRadius * 0.1)
-        PlayLoop(Tornado.sound2, Tornado.pos, 1 + Tornado.strength * 0.005 + Tornado.min_radius * 0.3 + Tornado.pullRadius * 0.1)
-        PlayLoop(windSound, GetPlayerTransform().pos, 1.4)
-
-        for i=1, Tornado.SimQuality * 2 do
-            local breakDir = VecNormalize(Vec(math.random(-100, 100), math.random(-150, 100), math.random(-100, 100)))
-            local breakStartPos = VecAdd(Tornado.pos, Vec(Tornado.min_radius * rnd(-1, 1), rnd(5,30), Tornado.min_radius * rnd(-1, 1)))
-            
-            local val1 = Tornado.SimQuality
-            local t = 520
-            local a = val1
-            local c = t - a
-            local SimQual = c * 0.001
-            local breakval = 0.1
-
-            local hit, dist, normal, shape = QueryRaycast(
-                breakStartPos,
-                breakDir,
-                Tornado.pullRadius * 0.5,
-                0,
-                false)   
-                if hit and GetBodyVehicle(GetShapeBody(shape)) == 0 then
-                local breakPos = VecAdd(VecScale(breakDir, dist), breakStartPos)
-                if breakPos[2] >= Tornado.endPos[2] - 1 then
-                    local mat = GetShapeMaterialAtPosition(shape, breakPos)
-                    
-                    --DebugPrint("Raycast hit voxel made out of " .. mat)
-                   
-                    if mat == 'dirt' or mat == 'grass' or mat == 'foliage' then
-                        breakval = 0.08
-                        MakeHole(breakPos, rnd(0.05,0.02) * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual * 0.1, 0, 0, false)
-                    elseif mat == 'concrete' or mat == 'hard masonry' or mat == 'masonry' then
-                        breakval = 0.08
-                        MakeHole(breakPos, rnd(0.01,0.001) * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual * 0.1, 0.1 * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual * 0.1, 0.1 * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual * 0.1, false)
-                    else
-                        MakeHole(breakPos, rnd(0.1,0.3) * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual * 0.1, rnd(0.05,0.1) * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual, rnd(0.04,0.005) * Tornado.strength * breakval * SimQual, false)
-                        if Tornado.DestructionParticles == true and mat ~= "none" and mat ~= "heavymetal" and mat ~= "rock" then
-
-                            local ppos = breakPos 
-                            local tpos = VecCopy(Tornado.pos)
-                            tpos[2] = ppos[2] -- Same height on tornado
-                            local diff = VecSub(tpos, ppos)
-                            local length = VecLength(diff)
-                    
-                            local tornadoPoint = VecCopy(Tornado.pos)
-                            local toTornado = VecSub(tornadoPoint, breakPos)
-                            local dist = VecLength(toTornado)
-                    
-                            local grav = rnd(1500,1000) * (1.0 - length / (Tornado.pullRadius*1))
-                            local speed = rnd(70,100) * (1.0 - length / (Tornado.pullRadius*1))
-                            rndcolor = rnd(1, 0.8)
-
-                            local PI = math.pi
-                            local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), breakPos)
-                            local theta = math.atan2(delta[3], delta[1]) + PI
-                            local z = math.cos(1 * (theta - 0.35 * PI))
-                            local x = -math.sin(1 * (theta - 0.35 * PI))
-                            local flingVec = VecScale(VecNormalize(Vec(x, 0, z)), speed)
-                            local life = rnd(0.6,0.1)
-                            local HeightOffset = rnd(60,-60) * (1.0 - length / (Tornado.pullRadius*0.7))
-        
-                            ParticleReset()
-                            ParticleType("plain")
-                            ParticleRadius(rnd(5,8) * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual * 0.1)
-                            ParticleColor(Tornado.ColorR * 0.01 * rndcolor, Tornado.ColorG * 0.01 * rndcolor, Tornado.ColorB * 0.01 * rndcolor)
-                            ParticleAlpha(0.5, 0.5, "constant", 0.5, 0.5)
-                            ParticleCollide(math.random(0,1))
-                            ParticleTile(0)
-                            ParticleGravity(grav)
-                            SpawnParticle(breakPos, flingVec, life)
-
-
-                            rndcolor = rnd(1, 0)
-                            ParticleReset()
-                            ParticleType("plain")
-                            ParticleRadius(rnd(5,8) * Tornado.strength * breakval * Tornado.strength * breakval * Tornado.strength * breakval * SimQual * 0.1)
-                            ParticleColor(Tornado.ColorR * 0.01 * rndcolor, Tornado.ColorG * 0.01 * rndcolor, Tornado.ColorB * 0.01 * rndcolor)
-                            ParticleAlpha(0.5, 0.5, "constant", 0.5, 0.5)
-                            ParticleCollide(math.random(0,1))
-                            ParticleTile(8)
-                            ParticleGravity(grav)
-                            SpawnParticle(breakPos, flingVec, life)
-
-                        end
-                    end
-                end
-            end 
-        end
-
-        if Tornado.Firenado == true then
-            for i=1, 15 + Tornado.min_radius do
-
-                local breakDir = VecNormalize(
-                    Vec(math.random(-100, 100), math.random(-100, 100), math.random(-100, 100)))
-                local breakStartPos = VecAdd(Tornado.pos, Vec(Tornado.min_radius * rnd(-1, 1), rnd(1,30), Tornado.min_radius * rnd(-1, 1)))
-        
-                local hit, dist, normal, shape = QueryRaycast(
-                    breakStartPos,
-                    breakDir,
-                    Tornado.min_radius + 5 + 3 * Tornado.min_radius,
-                    0,
-                    false)   
-                    if hit and GetBodyVehicle(GetShapeBody(shape)) == 0 then
-                    local breakPos = VecAdd(VecScale(breakDir, dist), breakStartPos)
-                    if breakPos[2] >= Tornado.endPos[2] - 1 then
-                        SpawnFire(breakPos)
-                    end
-                end 
-            end
-        end
-
-        Tornado.pos[2] = 0
-
-        Suction(Tornado.pullPlayer)
-        EmitParticles()
-        
-        Tornado.age = Tornado.age + dt
-        
-        if Tornado.state == Tornado.states['STATIC'] then
-            MoveStatic(isUsingTool, isShooting)
-        elseif Tornado.state == Tornado.states['FREEROAM']  then
-            MoveFreeroam(dt)
-        elseif Tornado.state == Tornado.states['FOLLOWING'] then
-            MoveFollowPlayer()
-        end
-    
-
-        if Tornado.lightFlicker then
-
-            local lights = FindLights(nil, true)
-
-            local rad = Tornado.pullRadius
-            local lightRad = rad + 2
-
-            local amplitude = 0.50 -- above/below sine zeroline
-            local minOffset = 0.50 -- recalibrates zeroline - so this value results in a sine wave from 0 to 1
-            local frequency = 0.06 -- divide time by this factor - smaller values means faster
-            emitScale = 0
-            
-            for i = 1, #lights do
-                SetLightEnabled(lights[i], false)
-            end
-        end
-
-        if Tornado.showLights then
-            PointLight((Tornado.endPos), 1, 1, 0, 1)
-        end
-    end
-
-    if isUsingTool and isShooting and not Tornado.active and not tornadoMenu then
-        local hit, pos = RaycastFromTransform(GetCameraTransform())
-        if hit then
-            Tornado.pos = pos
-            Tornado.endPos = pos
-            Tornado.Spawn(pos, pos)
-        end
-    end
-end
-
-Tornado.Spawn = function(startPos, endPos, lifetime)
-
-    if not spawned then
-        DefaultEnvironment = GetCurrentEnvironment()
-    end
-
-    spawned = true
-
-    if Tornado.affectWeather then
-        SetEnvironmentProperty("skybox", "Tornado.dds")
-        SetEnvironmentProperty("skyboxtint", 1,1,1)
-        SetEnvironmentProperty("skyboxbrightness", 0)
-        SetEnvironmentProperty("skyboxrot", 0)
-        SetEnvironmentProperty("ambient", 0)
-        SetEnvironmentProperty("fogColor", 0.2,0.2,0.2)
-        SetEnvironmentProperty("fogParams", 0,0,0,0)
-        SetEnvironmentProperty("sunBrightness", 0)
-        SetEnvironmentProperty("sunColorTint", 1,1,1)
-        SetEnvironmentProperty("sunDir", "auto")
-        SetEnvironmentProperty("sunSpread", 0)
-        SetEnvironmentProperty("sunLength", 0)
-        SetEnvironmentProperty("sunFogScale", 0)
-        SetEnvironmentProperty("sunGlare", 0)
-        SetEnvironmentProperty("exposure", 1,5)
-        SetEnvironmentProperty("brightness", 0)
-        SetEnvironmentProperty("wetness", 0.8)
-        SetEnvironmentProperty("puddleamount", 0.8)
-        SetEnvironmentProperty("puddlesize", 0.8)
-        SetEnvironmentProperty("rain", 4)
-        SetEnvironmentProperty("nightlight", true)
-    end
-
-    Tornado.startPos = startPos
-    Tornado.endPos = endPos
-    Tornado.age = 0
-    Tornado.lifetime = lifetime
-    Tornado.spawnAngle = 0
-    Tornado.pos = startPos
-    Tornado.active = true
-end
```

---

# Migration Report: tornado_helper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/tornado_helper.lua
+++ patched/tornado_helper.lua
@@ -1,3 +1,25 @@
+#version 2
+local A = rnd(360,-360)
+local B = rnd(360,-360)
+local C = rnd(360,-360)
+local D = rnd(360,-360)
+local vary = 0
+local Subvort1 = Vec(999,0,0)
+local Subvort2 = Vec(999,0,0)
+local Subvort3 = Vec(999,0,0)
+local Subvort4 = Vec(999,0,0)
+local subvorts = {
+    Subvort1,
+    Subvort2,
+    Subvort3,
+    Subvort4,
+}
+local selectedtime = 0
+local guhtime = 0
+local SubvortStrengthMultiplier = 0
+local SubvortSize = 0
+local SecretSettingsFunnel = false
+
 function clamp(value, mi, ma) if value < mi then value = mi end if value > ma then value = ma end return value end
 
 function Lerp(a, b, t) return a + (b - a) * t end
@@ -56,31 +78,6 @@
         end
     end 
 end
-
-local A = rnd(360,-360) 
-local B = rnd(360,-360) 
-local C = rnd(360,-360) 
-local D = rnd(360,-360) 
-local vary = 0
-
-local Subvort1 = Vec(999,0,0)
-local Subvort2 = Vec(999,0,0)
-local Subvort3 = Vec(999,0,0)
-local Subvort4 = Vec(999,0,0)
-
-
-local subvorts = {
-    Subvort1,
-    Subvort2,
-    Subvort3,
-    Subvort4,
-}
-
-local selectedtime = 0
-local guhtime = 0
-
-local SubvortStrengthMultiplier = 0
-local SubvortSize = 0
 
 function Subvorts() 
 
@@ -255,11 +252,10 @@
 
         PlayLoop(Tornado.sound1, Tornado.pos, 1 + Tornado.strength*SubvortStrengthMultiplier * 0.13 + Tornado.min_radius*SubvortSize * 1)
         PlayLoop(Tornado.sound2, Tornado.pos, 1 + Tornado.strength*SubvortStrengthMultiplier * 0.005 + Tornado.min_radius*SubvortSize * 0.3)
-        PlayLoop(windSound, GetPlayerTransform().pos, 1.4)
+        PlayLoop(windSound, GetPlayerTransform(playerId).pos, 1.4)
         
         function GetVeLSubV(pos, mass, vel, angVel, player)
             -- Closest point on tornado
-
 
             local tornadoPoint = VecCopy(SubV)
             tornadoPoint[2] = pos[2]
@@ -342,8 +338,8 @@
         
             -- Affect player
             if pullPlayer then
-                if GetPlayerVehicle() == 0 and not GetBool("game.map.enabled") then
-                    local ppos = GetPlayerTransform().pos
+                if GetPlayerVehicle(playerId) == 0 and not GetBool("game.map.enabled") then
+                    local ppos = GetPlayerTransform(playerId).pos
                     ppos[2] = ppos[2] + 1.0 -- Chest height
                     local tpos = VecCopy(SubV)
                     tpos[2] = ppos[2] -- Same height on tornado
@@ -362,8 +358,8 @@
                                 SetPlayerGroundVelocity(VecScale(toTornado, strength))
             
                                 -- Modify player velocity
-                                local vel = GetVelForBody(ppos, 2000, GetPlayerVelocity(), Vec(0,30,0), true)
-                                SetPlayerVelocity(vel)
+                                local vel = GetVelForBody(ppos, 2000, GetPlayerVelocity(playerId), Vec(0,30,0), true)
+                                SetPlayerVelocity(playerId, vel)
                             
                         end
                     end
@@ -436,7 +432,6 @@
                         ParticleGravity(grav)
                         SpawnParticle(breakPos, flingVec, life)
 
-
                         rndcolor = rnd(1, 0)
                         ParticleReset()
                         ParticleType("plain")
@@ -480,8 +475,6 @@
 
     end
 end
-
-local SecretSettingsFunnel = false
 
 function EmitParticles()
 
@@ -515,7 +508,6 @@
         -- Particle properties
         rndcolor = rnd(1, 0.8)
 
-
         if Tornado.Firenado == true then
 
             if math.random(1,5) == 1 then 
@@ -583,7 +575,6 @@
 
             -- Particle properties
             rndcolor = rnd(1, 0.8)
-
 
             if Tornado.Firenado == true then
 
@@ -910,8 +901,7 @@
 
     if Tornado.affectWeather then
 
-
-        local ppos = GetPlayerTransform().pos
+        local ppos = GetPlayerTransform(playerId).pos
         ppos[2] = ppos[2] + 1.0 -- Chest height
         local tpos = VecCopy(Tornado.pos)
         tpos[2] = ppos[2] -- Same height on tornado
@@ -919,12 +909,10 @@
         local length = VecLength(diff)
 
         local tornadoPoint = VecCopy(Tornado.pos)
-        local toTornado = VecSub(tornadoPoint, GetPlayerCameraTransform().pos)
+        local toTornado = VecSub(tornadoPoint, GetPlayerCameraTransform(playerId).pos)
         local dist = VecLength(toTornado)
 
-
         local countrain = math.clamp(150 * (1.0 - length / (Tornado.pullRadius*0.98)),0, math.huge)
-
 
         for i = 0, 150+countrain do 
 
@@ -936,7 +924,6 @@
             ParticleCollide(0)
 
             ParticleGravity(-100)
-
 
                         
             if math.random(1,30) == 1 then 
@@ -949,7 +936,7 @@
             
             local speed = math.clamp(rnd(20,180) * (1.0 - length / (Tornado.pullRadius*1.5)), 1, math.huge)
             local PI = math.pi
-            local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform().pos)
+            local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform(playerId).pos)
             local theta = math.atan2(delta[3], delta[1]) + PI
             local z = math.cos(1 * (theta - 0.2 * PI))
             local x = -math.sin(1 * (theta - 0.2 * PI))
@@ -958,7 +945,7 @@
 
             ParticleRotation(0)
 
-            SpawnParticle(VecAdd(GetPlayerCameraTransform().pos,Vec(rnd(50,-50), rnd(30,0), rnd(50,-50))), flingVec, life)
+            SpawnParticle(VecAdd(GetPlayerCameraTransform(playerId).pos,Vec(rnd(50,-50), rnd(30,0), rnd(50,-50))), flingVec, life)
 
         end
 
@@ -966,7 +953,7 @@
     
     if Tornado.WindfieldEffects then
 
-        local ppos = GetPlayerTransform().pos
+        local ppos = GetPlayerTransform(playerId).pos
         ppos[2] = ppos[2] + 1.0 -- Chest height
         local tpos = VecCopy(Tornado.pos)
         tpos[2] = ppos[2] -- Same height on tornado
@@ -974,12 +961,11 @@
         local length = VecLength(diff)
 
         local tornadoPoint = VecCopy(Tornado.pos)
-        local toTornado = VecSub(tornadoPoint, GetPlayerCameraTransform().pos)
+        local toTornado = VecSub(tornadoPoint, GetPlayerCameraTransform(playerId).pos)
         local dist = VecLength(toTornado)
 
         if dist > 0.0 then toTornado = VecScale(toTornado, 1.0 / dist) end
             if dist < Tornado.pullRadius * 1 then
-
 
                 if Tornado.cameraShake then
                     ShakeCamera(1.5*(1.0 - length / Tornado.pullRadius))
@@ -992,7 +978,6 @@
                 local speed = rnd(90,180) * (1.0 - length / (Tornado.pullRadius*1))
 
                 for i = 0, count do 
-
 
                     ParticleReset()
                     ParticleType("plain")
@@ -1004,7 +989,7 @@
                     ParticleGravity(grav1)
 
                     local PI = math.pi
-                    local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform().pos)
+                    local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform(playerId).pos)
                     local theta = math.atan2(delta[3], delta[1]) + PI
                     local z = math.cos(1 * (theta - 0.2 * PI))
                     local x = -math.sin(1 * (theta - 0.2 * PI))
@@ -1012,8 +997,7 @@
                     local life = rnd(1,0.5)
                     local HeightOffset = rnd(60,-60) * (1.0 - length / (Tornado.pullRadius*0.7))
 
-
-                    SpawnParticle(VecAdd(GetPlayerCameraTransform().pos,Vec(rnd(60,-60), -1+HeightOffset, rnd(60,-60))), flingVec, life)
+                    SpawnParticle(VecAdd(GetPlayerCameraTransform(playerId).pos,Vec(rnd(60,-60), -1+HeightOffset, rnd(60,-60))), flingVec, life)
 
                 end
 
@@ -1054,13 +1038,13 @@
                     ParticleCollide(1)
 
                     local PI = math.pi
-                    local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform().pos)
+                    local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform(playerId).pos)
                     local theta = math.atan2(delta[3], delta[1]) + PI
                     local z = math.cos(1 * (theta - 0.2 * PI))
                     local x = -math.sin(1 * (theta - 0.2 * PI))
                     local flingVec = VecScale(VecNormalize(Vec(x, 0, z)), speed)
                     local life = rnd(1,0.5)
-                    SpawnParticle(VecAdd(GetPlayerCameraTransform().pos,Vec(rnd(20,-20), rnd(5,-5), rnd(20,-20))), flingVec, life)
+                    SpawnParticle(VecAdd(GetPlayerCameraTransform(playerId).pos,Vec(rnd(20,-20), rnd(5,-5), rnd(20,-20))), flingVec, life)
 
                 end
 
@@ -1100,13 +1084,13 @@
                     ParticleCollide(1)
 
                     local PI = math.pi
-                    local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform().pos)
+                    local delta = TransformToLocalPoint(Transform(Tornado.pos, QuatEuler()), GetPlayerCameraTransform(playerId).pos)
                     local theta = math.atan2(delta[3], delta[1]) + PI
                     local z = math.cos(1 * (theta - 0.2 * PI))
                     local x = -math.sin(1 * (theta - 0.2 * PI))
                     local flingVec = VecScale(VecNormalize(Vec(x, 0, z)), speed)
                     local life = rnd(1,0.5)
-                    SpawnParticle(VecAdd(GetPlayerCameraTransform().pos,Vec(rnd(30,-30), rnd(10,-10), rnd(30,-30))), flingVec, life)
+                    SpawnParticle(VecAdd(GetPlayerCameraTransform(playerId).pos,Vec(rnd(30,-30), rnd(10,-10), rnd(30,-30))), flingVec, life)
 
                 end
 
@@ -1132,7 +1116,6 @@
         local diff = VecSub(tpos, ppos)
         local length = VecLength(diff)
 
-
         if not player then
             strength = strength * (1 + tornadoHeight) + Tornado.strength / 4 * 0.4  * (1.0 - dist / Tornado.pullRadius*1.5)
         else
@@ -1185,7 +1168,7 @@
         return vel, angVel
     end
 end
-Damageplayer = true
+
 function Suction(pullPlayer)
     local lo = VecAdd(Tornado.pos, Vec(-Tornado.pullRadius, 0, -Tornado.pullRadius))
     local hi = VecAdd(Tornado.pos, Vec(Tornado.pullRadius, Tornado.height * 3, Tornado.pullRadius))
@@ -1201,8 +1184,8 @@
 
     -- Affect player
     if pullPlayer then
-        if GetPlayerVehicle() == 0 and not GetBool("game.map.enabled") then
-            local ppos = GetPlayerTransform().pos
+        if GetPlayerVehicle(playerId) == 0 and not GetBool("game.map.enabled") then
+            local ppos = GetPlayerTransform(playerId).pos
             ppos[2] = ppos[2] + 1.0 -- Chest height
             local tpos = VecCopy(Tornado.pos)
             tpos[2] = ppos[2] -- Same height on tornado
@@ -1222,11 +1205,11 @@
                     SetPlayerGroundVelocity(VecScale(toTornado, strength))
 
                     -- Modify player velocity
-                    local vel = GetVelForBody(ppos, 2000, GetPlayerVelocity(), Vec(0,100,0), true)
-                    SetPlayerVelocity(vel)
+                    local vel = GetVelForBody(ppos, 2000, GetPlayerVelocity(playerId), Vec(0,100,0), true)
+                    SetPlayerVelocity(playerId, vel)
                     if Tornado.DamagePlayer then
-                        local health = GetPlayerHealth()
-                        SetPlayerHealth(health - 0.05 * (Tornado.strength*0.1) * (1.0 - dist / (Tornado.pullRadius*0.7))*0.025)
+                        local health = GetPlayerHealth(playerId)
+                        SetPlayerHealth(playerId, health - 0.05 * (Tornado.strength*0.1) * (1.0 - dist / (Tornado.pullRadius*0.7))*0.025)
                     end
                 end
             end
@@ -1234,14 +1217,6 @@
     end
 end
 
-
-
--- !
----@param tr table
----@param distance number
----@param rad number
----@param rejectBodies table
----@param rejectShapes table
 function RaycastFromTransform(tr, distance, rad, rejectBodies, rejectShapes)
     if distance ~= nil then
         distance = -distance
@@ -1270,4 +1245,5 @@
     else
         return nil
     end
-end +end
+

```

---

# Migration Report: vk_filtered_keys.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vk_filtered_keys.lua
+++ patched/vk_filtered_keys.lua
@@ -1,3 +1,4 @@
+#version 2
 local filteredKeys = {}
 
 function LoadDefaultFilteredKeys()
@@ -30,4 +31,5 @@
 function IsKeyFiltered(key)
     if not filteredKeys[key] then return false end
     return true
-end+end
+

```

---

# Migration Report: vk_logging.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vk_logging.lua
+++ patched/vk_logging.lua
@@ -1,23 +1,6 @@
-ELogLevels = {
-    Debug = 0,
-    Info = 1,
-    Warn = 2,
-    Error = 3,
-}
-
+#version 2
 local DebugMode = false
 
-CLog = {}
-CLog.__index = CLog
-
-setmetatable(CLog, {
-    __call = function(class, ...)
-        return class.new(...)
-    end
-})
-
----@param name string
----@param logLevel number
 function CLog.new(name, logLevel)
     local self = setmetatable({}, CLog)
 
@@ -35,50 +18,31 @@
     output = output .. '\n'
 end
 
----@return string
 function CLog:GetName()
     return self.name
 end
 
----Set log level
----@param level number
 function CLog:SetLevel(level)
     self.logLevel = level
 end
 
----@return number
 function CLog:GetLevel()
     return self.logLevel
 end
 
--- Debug Log
----```lua
------Make sure to enable debug mode
----SetLogDebug(true)
----```
----@param message any
----@param ... any
 function CLog:Debug(message, ...)
     message = tostring(string.format('[DEBUG]: %s', message)) Log(self, message, ELogLevels.Debug, ...)
 end
 
--- Info Log
----@param message any
----@param ... any
 function CLog:Info(message, ...)
     message = tostring(string.format('[INFO]: %s', message)) Log(self, message, ELogLevels.Info, ...)
 end
 
--- Warning Log
----@param message any
----@param ... any
 function CLog:Warn(message, ...)
     message = tostring(string.format('[WARN]: %s', message)) Log(self, message, ELogLevels.Warn, ...)
 end
 
--- Error Log
----@param message any
----@param ... any
 function CLog:Error(message, ...)
     message = tostring(string.format('[ERROR]: %s', message)) Log(self, message, ELogLevels.Error, ...)
-end+end
+

```

---

# Migration Report: vk_utils.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vk_utils.lua
+++ patched/vk_utils.lua
@@ -1,15 +1,4 @@
-#include "vk_logging.lua"
-
-CoreLogger = CLog('Core', ELogLevels.Error)
-
-EDType = {
-    String = 0,
-    Int = 1,
-    Float = 2,
-    Bool = 3,
-}
-
--- Quickly hacked up this function to only take in a number (this is for Tornado.speed)
+#version 2
 local function GetType(val)
     if type(val) == 'boolean' then return EDType.Bool end
     if math.floor(val) == val then
@@ -19,31 +8,26 @@
     return EDType.Float
 end
 
----@param key any
----@param default any
 function AddKeyNE(key, default, dtype)
     key = 'savegame.mod.' .. ModName .. '.' .. key
 
     if HasKey(key) then return end
 
     if dtype == EDType.Bool then
-        SetBool(key, default)
+        SetBool(key, default, true)
         return
     end
 
     if tonumber(default) then
         local type = GetType(default)
 
-        if type == EDType.Float then SetFloat(key, default) end
-        if type == EDType.Int then return SetInt(key, default) end
+        if type == EDType.Float then SetFloat(key, default, true) end
+        if type == EDType.Int then return SetInt(key, default, true) end
     else
-        SetString(key, default)
+        SetString(key, default, true)
     end
 end
 
--- Retrieve a key from the registry
----@param key any
----@return any
 function GetKey(key, dtype)
     dtype = dtype or nil
 
@@ -66,31 +50,25 @@
     end
 end
 
--- Set a key in the registry
----@param key any
----@param value any
 function SetKey(key, value, dtype)
     key = 'savegame.mod.' .. ModName .. '.' .. key
     if not HasKey(key) then CoreLogger:Error(string.format('Key ["%s"] does not exist', key)) return end
 
     if dtype == EDType.Bool then
-        SetBool(key, value)
+        SetBool(key, value, true)
         return
     end
 
     if tonumber(value) then
         local type = GetType(value)
 
-        if type == EDType.Float then SetFloat(key, value) end
-        if type == EDType.Int then SetInt(key, value) end
+        if type == EDType.Float then SetFloat(key, value, true) end
+        if type == EDType.Int then SetInt(key, value, true) end
     else
-        SetString(key, value)
+        SetString(key, value, true)
     end
 end
 
----@param colour table
----@param alpha number
----@return table
 function GetColour(colour, alpha)
     alpha = alpha or colour[4]
     colour[4] = alpha
@@ -116,4 +94,5 @@
     table.insert(colour, tonumber('0x' .. hex:sub(5,6)))
 
     return colour
-end+end
+

```
