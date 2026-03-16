# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,28 +1,25 @@
---dont judge the organization of this I threw it together quickly
+#version 2
+function render(dt)
+    GrappleRender()
+end
 
-#include "script/ui.lua"
-#include "script/vfx.lua"
-#include "script/utilities.lua"
-#include "script/screwdriver.lua"
-#include "script/grapplehook.lua"
-#include "script/bondanchor.lua"
-#include "script/gravityinterceptor.lua"
-
-function init()
+function server.init()
     ScrewdriverInit()
     GrappleInit()
     AnchorInit()
     InterceptInit()
 end
 
-function tick(dt)
-    ScrewdriverTick(dt)
-    GrappleTick(dt)
-    AnchorTick(dt)
-    InterceptTick(dt)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        ScrewdriverTick(dt)
+        GrappleTick(dt)
+        AnchorTick(dt)
+        InterceptTick(dt)
+    end
 end
 
-function draw(dt)
+function client.draw()
     UiPush()
         ScrewdriverDraw(dt)
     UiPop()
@@ -31,184 +28,3 @@
     InterceptDraw(dt)
 end
 
-function render(dt)
-    GrappleRender()
-end
-
-UiParticles = {}
-
-sprites = {laser = LoadSprite("MOD/gfx/beam.png")}
-
-Ui = {
-    backgrounds = {
-        gradient = "MOD/ui/terminal/background/gradient.png",
-        gradient2 = "MOD/ui/terminal/background/gradient2.png",
-        grain = "MOD/ui/terminal/background/grain.png",
-        noise ="MOD/ui/terminal/background/noise.png",
-        fade_box = "MOD/ui/terminal/background/fade.png",
-        cash = "MOD/ui/terminal/background/cash.png",
-        tile_banners = {
-            layer_mask = "MOD/ui/terminal/background/layer_mask.png",
-            layer_mask2 = "MOD/ui/terminal/background/layer_mask2.png",
-            achievements = "MOD/ui/terminal/background/trophies.png",
-            scrapbook = "MOD/ui/terminal/background/props.png",
-            shop = "MOD/ui/terminal/background/shop.png"
-        },
-        showcase = {
-            crownzy = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/crownzy.png",
-            },
-            chair = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/chair.png",			
-            },
-            container = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/container.png",
-            },
-            lamp = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/lamps.png",
-            },
-            construct = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/td_construct.png",
-            },
-            bluetide = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/blutide.png",
-            },
-            lab = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/lab_heisenberg.png",
-            },
-            robot = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/robot.png",					
-            },
-            entertainment = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/entertainment.png",
-            },
-            fixtures = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/fixtures.png",
-            },		
-            foliage = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/foliage.png",
-            },
-            foodstuffs = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/foodstuffs.png",
-            },	
-            functional = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/functional.png",
-            },
-            misc = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/misc.png",
-            },	
-            nautical = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/nautical.png",
-            },	
-            parts = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/parts.png",
-            },				
-            textile = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/textile.png",
-            },	
-            signage = {
-                color = "MOD/ui/terminal/background/scrapbook_showcases/signage.png",
-            },						
-        }
-    },
-    icons = {
-        shop = "MOD/ui/terminal/icons/shop.png",
-        scrapbook = "MOD/ui/terminal/icons/scrapbook.png",
-        achievements = "MOD/ui/terminal/icons/trophy.png",
-        options = "MOD/ui/terminal/icons/options.png",
-        quests = "MOD/ui/terminal/icons/info_board.png",
-        lock = "data/ui/menu/lock-small.png",
-        info = "data/ui/common/search_ico.png",
-        info_hq = "MOD/ui/terminal/icons/info.png",
-        eye = "MOD/ui/terminal/icons/range.png",
-        eye_1 = "MOD/ui/terminal/icons/eye_1.png",
-        eye_book = "MOD/ui/terminal/icons/eye_book.png",
-        eye_price = "MOD/ui/terminal/icons/eye_price.png",			
-        cart = "MOD/ui/terminal/icons/cart.png",
-        flatbed = "MOD/ui/terminal/icons/flatbed.png",
-        grapple = "MOD/ui/terminal/icons/grapple.png",
-        ammo = "MOD/ui/terminal/icons/ammo.png",
-        tick = "MOD/ui/terminal/icons/tick2.png",
-        cross = "MOD/ui/terminal/icons/cross.png",
-        ammo_ui = "MOD/ui/terminal/icons/ammonition.png",
-        like = "data/ui/common/img_557_1276.png",
-        save = "MOD/ui/terminal/icons/load.png",
-        load = "MOD/ui/terminal/icons/save.png",
-        restart = "MOD/ui/terminal/icons/restart.png",
-        terdon = "MOD/ui/terminal/icons/terdon.png",
-
-        --Modifers
-        midas_touch = "MOD/ui/terminal/icons/midas_base.png",
-        midas_touch_alpha = "MOD/ui/terminal/icons/midas.png",
-        flooded = "MOD/ui/terminal/icons/flood_base.png",
-        flooded_alpha = "MOD/ui/terminal/icons/flood.png",
-        
-        -- Stats Icons
-        cargo = "MOD/ui/terminal/icons/cargo.png",
-        handling = "MOD/ui/terminal/icons/handling.png",
-        size = "MOD/ui/terminal/icons/size.png",
-        speed = "MOD/ui/terminal/icons/speed.png",
-        
-        thumbs = {
-            ammo = "MOD/ui/terminal/icons/thumbnails/ammo.png",
-            anchor = "MOD/ui/terminal/icons/thumbnails/anchor.png",
-            crane_big = "MOD/ui/terminal/icons/thumbnails/crane_big_future.png",
-            crane_small = "MOD/ui/terminal/icons/thumbnails/crane_small_future.png",
-            deckboat = "MOD/ui/terminal/icons/thumbnails/deckboat_future.png",
-            flatbed = "MOD/ui/terminal/icons/thumbnails/flatbed_future.png",
-            flatbed_large = "MOD/ui/terminal/icons/thumbnails/flatbed_future_large.png",
-            gravity = "MOD/ui/terminal/icons/thumbnails/gravity.png",
-            grapple = "MOD/ui/terminal/icons/thumbnails/grapple.png",
-            screwdriver = "MOD/ui/terminal/icons/thumbnails/screwdriver.png",
-            trawler = "MOD/ui/terminal/icons/thumbnails/trawler_future.png",
-            scanner = "MOD/ui/terminal/icons/thumbnails/scanner.png",
-            future_basket = "MOD/ui/terminal/icons/thumbnails/future_basket.png",
-            future_dumpster = "MOD/ui/terminal/icons/thumbnails/future_dumpster.png",
-            future_spotlight = "MOD/ui/terminal/icons/thumbnails/spotlight.png",
-        },
-        upgrade = {
-            reach = "MOD/ui/terminal/icons/reach.png",
-            range = "MOD/ui/terminal/icons/range_scan.png",
-            longetivity = "MOD/ui/terminal/icons/long.png",
-            cooldown = "MOD/ui/terminal/icons/cooldown.png",
-            detonate = "MOD/ui/terminal/icons/detonate.png"
-        }
-    },
-    shapes = {
-        semicircle1 = "MOD/ui/semicircle1.png",
-        semicircle2 = "MOD/ui/semicircle2.png",
-        circle = "MOD/ui/circle.png"
-    },
-    adverts = "MOD/ui/terminal/adverts/advert"
-}
-
---Configs!
-TerminalFont = "MOD/font/ModeNine.TTF"
-TerminalConf = {
-    keybinds = {
-        toggle = "R",
-        back = "RMB"
-    },
-    control = {
-        scroll_sensitivity = 8
-    }
-}
-TerminalColor = {
-    textColor = {
-        default = Vec(1,1,1),
-        header = Vec(0, 0.133, 0.071),
-        danger = Vec(1, 0.25, 0.25),
-        warning = Vec(1,1,0),
-        success = Vec(0,1,0),
-        info = Vec(0.322, 0.882, 1)
-    },
-    BackgroundColor = {
-        primary = Vec(0, 0.19, 0.1),
-        secondary = Vec(0.22, 0.725, 0.2),
-        darkened = Vec(0, 0.133, 0.071),
-        button = Vec(0.6, 1, 0.26),
-        button_cancel = Vec(0, 0.133, 0.071),
-        active = Vec(0.6, 1, 0.26),
-        denail = Vec(1,0.12,0.12)
-    }
-}
```

---

# Migration Report: script\bondanchor.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\bondanchor.lua
+++ patched/script\bondanchor.lua
@@ -1,23 +1,24 @@
+#version 2
 local GrappleIndicatorPosition = {x = 0, y = 0}
 local closestDrone = 0
 
 function AnchorInit()
     RegisterTool("anchor", "Bond Anchor", "MOD/prefab/anchor.xml")
-    SetBool("game.tool.anchor.enabled", true)
+    SetBool("game.tool.anchor.enabled", true, true)
 
     --[[
     if not HasKey("savegame.mod.upgrades.anchor.time") then
-        SetInt("savegame.mod.upgrades.anchor.time", 0)
+        SetInt("savegame.mod.upgrades.anchor.time", 0, true)
     end
     if not HasKey("savegame.mod.upgrades.anchor.ammo") then
-        SetInt("savegame.mod.upgrades.anchor.ammo", 0)
+        SetInt("savegame.mod.upgrades.anchor.ammo", 0, true)
     end
     if not HasKey("savegame.mod.upgrades.anchor.self_destruct") then
-        SetInt("savegame.mod.upgrades.anchor.self_destruct", 0)
+        SetInt("savegame.mod.upgrades.anchor.self_destruct", 0, true)
     end]]
 
-    SetInt("game.tool.anchor.ammo.max", 150)--15 + GetInt("savegame.mod.upgrades.anchor.ammo") * 10)
-    SetInt("game.tool.anchor.ammo", GetInt("game.tool.anchor.ammo.max"))
+    SetInt("game.tool.anchor.ammo.max", 150, true)--15 + GetInt("savegame.mod.upgrades.anchor.ammo") * 10)
+    SetInt("game.tool.anchor.ammo", GetInt("game.tool.anchor.ammo.max"), true)
 
     throw = LoadSound("throw/s0.ogg")
     hover = LoadLoop("MOD/snd/anchor/drone_hover3.ogg")
@@ -37,7 +38,7 @@
 
 local function GetDistanceFromCursor(origin)
     local _,_,_,_,aimDirection = GetAimPos()
-    local directionTowardsDrone = VecSub(origin,GetPlayerCameraTransform().pos)
+    local directionTowardsDrone = VecSub(origin,GetPlayerCameraTransform(playerId).pos)
     local distance = VecLength(directionTowardsDrone)
     directionTowardsDrone = VecNormalize(directionTowardsDrone)
 
@@ -52,8 +53,7 @@
         bav.max_time = maxtime
         bav.time = maxtime
 
-
-        SetInt("game.tool.anchor.ammo.max",150)--15 + GetInt("savegame.mod.upgrades.anchor.ammo") * 10)
+        SetInt("game.tool.anchor.ammo.max",150, true)--15 + GetInt("savegame.mod.upgrades.anchor.ammo") * 10)
 
         ShowTool()
         local ammo = GetInt("game.tool.anchor.ammo")
@@ -63,7 +63,7 @@
             toolpos = VecScale(Vec(7,-14.5,-3.5), 0.04)
             toolrot = QuatEuler(-22,-69,-6)
             SetToolHandPoseLocalTransform(Transform(Vec(0.04,-0.07,-0.08), QuatEuler(0,160,0)), nil)
-            if InputDown("usetool") and ammo > 0 then
+            if InputDown("usetool") and ammo ~= 0 then
                 toolpos = VecScale(Vec(7.5,-11.5,-11.5), 0.04)
                 toolrot = QuatEuler(-22,-69,-6)
                 HideTool()
@@ -82,7 +82,7 @@
         local dir = QuatRotateVec(camtr.rot, Vec(0, 0, -1))
         local hit, d, n, s = QueryRaycast(camtr.pos, dir, 100)
         local b = GetShapeBody(s)
-        if hit and b ~= GetWorldBody() and GetPlayerVehicle() == 0 and (HasTag(b, "dronetarget") or not HasTag(b, "unbreakable")) then
+        if hit and b ~= GetWorldBody() and GetPlayerVehicle(playerId) == 0 and (HasTag(b, "dronetarget") or not HasTag(b, "unbreakable")) then
             drawBodyBounds(b, 1, 1, 1, 0.5)
             if (InputPressed("usetool") and GetBool("game.player.canusetool")) and ammo > 0 and not bav.cooldown then
                 local spawned = Spawn("MOD/prefab/anchordrone.xml", GetBodyTransform(GetToolBody()))
@@ -92,7 +92,7 @@
                 SetBodyAngularVelocity(spawned[1], VecScale(Vec(rnd(-1,1),rnd(-1,1),rnd(-1,1)),1000))
 
                 bav.cooldown = GetTime() + 0.5
-                SetInt("game.tool.anchor.ammo", ammo-1)
+                SetInt("game.tool.anchor.ammo", ammo-1, true)
 
                 --Setup Ui Particles / i got a new toy slip so of course im gonna use it
                 bav.handle = spawned[1]
@@ -129,7 +129,7 @@
             local targetpos = CenterOfMass(targetbody)
 
             local newrot = QuatSlerp(bodytr.rot, QuatLookAt(bodytr.pos, targetpos.pos), dt*5)
-            if GetPlayerGrabBody() ~= body then
+            if GetPlayerGrabBody(playerId) ~= body then
                 SetBodyTransform(body, Transform(bodytr.pos, newrot))
             end
 
@@ -228,7 +228,7 @@
         
         local mx = 20
 
-        if d > 0 then
+        if d ~= 0 then
             UiAlign("center middle")
             UiTranslate(GrappleIndicatorPosition.x,GrappleIndicatorPosition.y)
             UiFont(TerminalFont,32)
@@ -291,7 +291,7 @@
             local x, y, dist = UiWorldToPixel(offsetPos)
             local x2,y2 = UiWorldToPixel(bodypos.pos)
 
-            if dist > 0 then
+            if dist ~= 0 then
                 UiFont(TerminalFont, 24)
                 local w, h = UiGetTextSize(timer)
 
@@ -447,7 +447,7 @@
         local timer = tonumber(GetTagValue(body, "timer"))
         local starttime = tonumber(GetTagValue(body, "starttime"))
 
-        if timer > 0 then
+        if timer ~= 0 then
             local bodypos = GetBodyTransform(body).pos
             local fill = math.max(timer/starttime, 0.25)
 
@@ -498,3 +498,4 @@
 
     return visible
 end
+

```

---

# Migration Report: script\grapplehook.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\grapplehook.lua
+++ patched/script\grapplehook.lua
@@ -1,12 +1,13 @@
+#version 2
 function GrappleInit()
     RegisterTool("grapple", "Grappling Hook", "MOD/prefab/grapplebody.xml")
-    SetBool("game.tool.grapple.enabled", true)
-
-    SetString("game.tool.grapple.ammo.display","")
+    SetBool("game.tool.grapple.enabled", true, true)
+
+    SetString("game.tool.grapple.ammo.display","", true)
 
     --[[
     if not HasKey("savegame.mod.upgrades.grapple.reach") then
-        SetInt("savegame.mod.upgrades.grapple.reach", 0)
+        SetInt("savegame.mod.upgrades.grapple.reach", 0, true)
     end]]
 
     gpv = {
@@ -29,6 +30,7 @@
     GrappleIndicatorPosition = {x = 0, y = 0}
 
 end
+
 function GrappleTick(dt)
 
     gpv.maxdist = 50 --5 + GetInt("savegame.mod.upgrades.grapple.reach") * 5
@@ -88,18 +90,18 @@
                 else
                     SetBodyTransform(gpv.grapplebody, TransformToParentTransform(GetBodyTransform(gpv.attachbody), gpv.attachoffset))
 
-                    local playervel = GetPlayerVelocity()
+                    local playervel = GetPlayerVelocity(playerId)
                     local pitch = VecLength(playervel) / 10
                     if pitch > 0.2 then
                         PlayLoop(gpv.loop, GetCameraTransform().pos, 1, true, pitch)
                     end
-                    local pull = VecScale(VecNormalize(VecSub(hookpos.pos, GetPlayerTransform().pos)), dt * 50)
-                    SetPlayerVelocity(VecAdd(playervel, pull))
+                    local pull = VecScale(VecNormalize(VecSub(hookpos.pos, GetPlayerTransform(playerId).pos)), dt * 50)
+                    SetPlayerVelocity(playerId, VecAdd(playervel, pull))
 
                     if IsBodyDynamic(gpv.attachbody) then
                         local bodyvel = GetBodyVelocity(gpv.attachbody)
                         SetBodyVelocity(gpv.attachbody, VecAdd(bodyvel, VecScale(pull, -1 / (GetBodyMass(gpv.attachbody)*0.05) )))
-                        if VecLength(VecSub(hookpos.pos, GetPlayerTransform().pos)) < 0.2 then
+                        if VecLength(VecSub(hookpos.pos, GetPlayerTransform(playerId).pos)) < 0.2 then
                             gpv.attachbody = true
                             gpv.returning = true
                         end
@@ -124,9 +126,9 @@
                     PlaySound(gpv.snd1)
                     PlayLoop(gpv.loop, GetCameraTransform().pos)
 
-                    local playervel = GetPlayerVelocity()
-                    local pull = VecScale(VecNormalize(VecSub(hookpos.pos, GetPlayerTransform().pos)), dt * 50)
-                    SetPlayerVelocity(VecAdd(playervel, pull))
+                    local playervel = GetPlayerVelocity(playerId)
+                    local pull = VecScale(VecNormalize(VecSub(hookpos.pos, GetPlayerTransform(playerId).pos)), dt * 50)
+                    SetPlayerVelocity(playerId, VecAdd(playervel, pull))
 
                     if gpv.attachbody ~= GetWorldBody() then
                         local bodyvel = GetBodyVelocity(body)
@@ -261,9 +263,10 @@
 end
 
 function canUseGrapple()
-	local vehicle = GetPlayerVehicle()
+	local vehicle = GetPlayerVehicle(playerId)
 	if vehicle ~= 0 then
 		return false
 	end
 	return true
 end
+

```

---

# Migration Report: script\gravityinterceptor.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\gravityinterceptor.lua
+++ patched/script\gravityinterceptor.lua
@@ -1,23 +1,24 @@
+#version 2
 local GrappleIndicatorPosition = {x = 0, y = 0}
 local closestDrone = 0
 
 function InterceptInit()
     RegisterTool("intercept", "Gravity Interceptor", "MOD/prefab/interceptor.xml")
-    SetBool("game.tool.intercept.enabled", true)
+    SetBool("game.tool.intercept.enabled", true, true)
 
     --[[
     if not HasKey("savegame.mod.upgrades.intercept.time") then
-        SetInt("savegame.mod.upgrades.interceptor.time", 0)
+        SetInt("savegame.mod.upgrades.interceptor.time", 0, true)
     end
     if not HasKey("savegame.mod.upgrades.intercept.ammo") then
-        SetInt("savegame.mod.upgrades.intercept.ammo", 0)
+        SetInt("savegame.mod.upgrades.intercept.ammo", 0, true)
     end
      if not HasKey("savegame.mod.upgrades.intercept.self_destruct") then
-        SetInt("savegame.mod.upgrades.intercept.self_destruct", 0)
+        SetInt("savegame.mod.upgrades.intercept.self_destruct", 0, true)
     end]]
 
-    SetInt("game.tool.intercept.ammo.max", 150)--15 + GetInt("savegame.mod.upgrades.intercept.ammo") * 10)
-    SetInt("game.tool.intercept.ammo", GetInt("game.tool.intercept.ammo.max"))
+    SetInt("game.tool.intercept.ammo.max", 150, true)--15 + GetInt("savegame.mod.upgrades.intercept.ammo") * 10)
+    SetInt("game.tool.intercept.ammo", GetInt("game.tool.intercept.ammo.max"), true)
 
     throw = LoadSound("throw/s0.ogg")
     hover = LoadLoop("MOD/snd/anchor/drone_hover3.ogg")
@@ -37,7 +38,7 @@
 
 local function GetDistanceFromCursor(origin)
     local _,_,_,_,aimDirection = GetAimPos()
-    local directionTowardsDrone = VecSub(origin,GetPlayerCameraTransform().pos)
+    local directionTowardsDrone = VecSub(origin,GetPlayerCameraTransform(playerId).pos)
     local distance = VecLength(directionTowardsDrone)
     directionTowardsDrone = VecNormalize(directionTowardsDrone)
 
@@ -53,7 +54,7 @@
         giv.max_time = maxtime
         giv.time = maxtime
 
-        SetInt("game.tool.intercept.ammo.max", 150)--15 + GetInt("savegame.mod.upgrades.intercept.ammo") * 10)
+        SetInt("game.tool.intercept.ammo.max", 150, true)--15 + GetInt("savegame.mod.upgrades.intercept.ammo") * 10)
 
         ShowTool()
         local ammo = GetInt("game.tool.intercept.ammo")
@@ -63,7 +64,7 @@
             toolpos = VecScale(Vec(7,-14.5,-3.5), 0.04)
             toolrot = QuatEuler(-22,-69,-6)
             SetToolHandPoseLocalTransform(Transform(Vec(0.04,-0.07,-0.08), QuatEuler(0,160,0)), nil)
-            if InputDown("usetool") and ammo > 0 then
+            if InputDown("usetool") and ammo ~= 0 then
                 toolpos = VecScale(Vec(7.5,-11.5,-11.5), 0.04)
                 toolrot = QuatEuler(-22,-69,-6)
                 HideTool()
@@ -82,7 +83,7 @@
         local dir = QuatRotateVec(camtr.rot, Vec(0, 0, -1))
         local hit, d, n, s = QueryRaycast(camtr.pos, dir, 100)
         local b = GetShapeBody(s)
-        if hit and b ~= GetWorldBody() and GetPlayerVehicle() == 0 and (HasTag(b, "dronetarget") or not HasTag(b, "unbreakable")) then
+        if hit and b ~= GetWorldBody() and GetPlayerVehicle(playerId) == 0 and (HasTag(b, "dronetarget") or not HasTag(b, "unbreakable")) then
             drawBodyBounds(b, 1, 1, 1, 0.5)
             if (InputPressed("usetool") and GetBool("game.player.canusetool")) and ammo > 0 and not giv.cooldown then
                 local spawned = Spawn("MOD/prefab/interceptordrone.xml", GetBodyTransform(GetToolBody()))
@@ -92,7 +93,7 @@
                 SetBodyAngularVelocity(spawned[1], VecScale(Vec(rnd(-1,1),rnd(-1,1),rnd(-1,1)),1000))
 
                 giv.cooldown = GetTime() + 0.5
-                SetInt("game.tool.intercept.ammo", ammo-1)
+                SetInt("game.tool.intercept.ammo", ammo-1, true)
 
                 --Setup Ui Particles / i got a new toy slip so of course im gonna use it
                 giv.handle = spawned[1]
@@ -127,7 +128,7 @@
             local targetpos = CenterOfMass(targetbody)
 
             local newrot = QuatSlerp(bodytr.rot, QuatLookAt(bodytr.pos, targetpos.pos), dt*5)
-            if GetPlayerGrabBody() ~= body then
+            if GetPlayerGrabBody(playerId) ~= body then
                 SetBodyTransform(body, Transform(bodytr.pos, newrot))
             end
 
@@ -224,7 +225,7 @@
         
         local mx = 20
 
-        if d > 0 then
+        if d ~= 0 then
             UiAlign("center middle")
             UiTranslate(GrappleIndicatorPosition.x,GrappleIndicatorPosition.y)
             UiFont(TerminalFont,32)
@@ -287,7 +288,7 @@
             local x, y, dist = UiWorldToPixel(offsetPos)
             local x2,y2 = UiWorldToPixel(bodypos.pos)
 
-            if dist > 0 then
+            if dist ~= 0 then
                 UiFont(TerminalFont, 24)
                 local w, h = UiGetTextSize(timer)
 
@@ -352,11 +353,6 @@
         end
     end
 end
-
---Ui stuff
-
-
---End of novena dark magic
 
 function CenterOfMass(body)
     local com = GetBodyCenterOfMass(body)
@@ -460,7 +456,7 @@
         local timer = tonumber(GetTagValue(body, "timer"))
         local starttime = tonumber(GetTagValue(body, "starttime"))
 
-        if timer > 0 then
+        if timer ~= 0 then
             local bodypos = GetBodyTransform(body).pos
             local fill = math.max(timer/starttime, 0.25)
 
@@ -510,4 +506,5 @@
     end
 
     return visible
-end+end
+

```

---

# Migration Report: script\screwdriver.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\screwdriver.lua
+++ patched/script\screwdriver.lua
@@ -1,10 +1,7 @@
---this got a little messy as I added more stuff
---add the tag "not_unscrewable" to any body with joints that should not be unscrewable (add it to both bodies attatched to the joint)
-
+#version 2
 local max_cursor_movement = 800
 local screwdriver_rotation = 0
 local screwdriver_rotation_abs = 0
-
 local screwdriving = false
 local unscrew_body = nil
 local hit = false
@@ -12,33 +9,21 @@
 local grabbable = "yes"
 local error_alpha = 0
 local last_error_message = "Too Far!"
-
 local shoot_snd = LoadSound("MOD/snd/screwdriver/shoot.ogg")
 local hold_loop = LoadLoop("MOD/snd/screwdriver/hold_loop.ogg")
-local release_sound = LoadSound("MOD/snd/screwdriver/release0.ogg") --3 variations
+local release_sound = LoadSound("MOD/snd/screwdriver/release0.ogg")
 local tick_sound = LoadSound("MOD/snd/screwdriver/tick.ogg")
 local click_on_sound = LoadSound("MOD/snd/screwdriver/click_on.ogg")
 local warn_sound = LoadSound("MOD/snd/screwdriver/warn.ogg")
 local on_sound_played = false
 local tick_sound_played = false
 local prev_body = nil
-
 local rot_dt = 0
 local small_arrows_sprite = LoadSprite("MOD/ui/screwdriver/rotation_arrows_small.png")
 local big_arrows_sprite = LoadSprite("MOD/ui/screwdriver/rotation_arrows_big.png")
-
 local reach = 1
 local mass = 1
 
---no modifiers on toolbox version
---registry keys and their defaults
---[[each will have "savegame.mod.upgrades.screwdriver." prepended to it
-local savekey_value_pairs = {
-    ["active"] = false,
-    ["reach"] = 0, --1 starts at 10, each increment by 10 until level 10 (max)
-    ["mass"] = 0 --1 starts at 150, expo. increase until 10 (max)    = 150^(.2*(mass+4))
-}]]
-
 function ScrewdriverInit()
 
     InitializeTool("lockonauts_screwdriver", "Electro-Mag Screwdriver", "MOD/vox/screwdriver.vox", 2, false, "MOD/prefab/screwdriver.xml")
@@ -50,16 +35,16 @@
 
     --[[debug menu option retrieval
     if debugMenuRetrieveOptionValue("driver","values") then
-        SetBool("savegame.mod.upgrades.screwdriver.active", debugMenuRetrieveOptionValue("driver","active"))
-        SetFloat("savegame.mod.upgrades.screwdriver.reach", debugMenuRetrieveOptionValue("driver","reach"))
-        SetFloat("savegame.mod.upgrades.screwdriver.mass", debugMenuRetrieveOptionValue("driver","mass"))
+        SetBool("savegame.mod.upgrades.screwdriver.active", debugMenuRetrieveOptionValue("driver","active"), true)
+        SetFloat("savegame.mod.upgrades.screwdriver.reach", debugMenuRetrieveOptionValue("driver","reach"), true)
+        SetFloat("savegame.mod.upgrades.screwdriver.mass", debugMenuRetrieveOptionValue("driver","mass"), true)
     end]]
 
     --turn off tool if not unlocked
     --if not active then
-      --  SetBool("game.tool.lockonauts_screwdriver.enabled", false)
+      --  SetBool("game.tool.lockonauts_screwdriver.enabled", false, true)
     --else
-        --SetBool("game.tool.lockonauts_screwdriver.enabled", true)
+        --SetBool("game.tool.lockonauts_screwdriver.enabled", true, true)
     --end
 
     local color_accept = TerminalColor.BackgroundColor.active
@@ -89,7 +74,7 @@
 
             if hit then
                 if not tick_sound_played then
-                    PlaySound(tick_sound, GetPlayerCameraTransform().pos, 0.5)
+                    PlaySound(tick_sound, GetPlayerCameraTransform(playerId).pos, 0.5)
                     tick_sound_played = true
                 end
 
@@ -105,7 +90,7 @@
                     DrawBodyOutline(unscrew_body, color_deny[1], color_deny[2], color_deny[3], 1)
 
                     if InputPressed("usetool") then
-                        PlaySound(warn_sound, GetPlayerCameraTransform().pos, 0.5)
+                        PlaySound(warn_sound, GetPlayerCameraTransform(playerId).pos, 0.5)
                         error_alpha = 2
                         last_error_message = grabbable
                     end
@@ -139,7 +124,7 @@
     SetBodyActive(body, true)
 
     --[[fun broken shit (turns it into a beyblade ripcord)
-    local qla = QuatLookAt(pos, GetPlayerCameraTransform().pos)
+    local qla = QuatLookAt(pos, GetPlayerCameraTransform(playerId).pos)
     local force = VecScale(VecNormalize(QuatEuler(qla)), 100)
     SetBodyVelocity(body, force)
     --]]
@@ -169,7 +154,7 @@
             --stuff that uses the rotation amount
             ShakeCamera(screwdriver_rotation_abs*0.4)
             DrawBodyOutline(unscrew_body, color[1], color[2], color[3], 1)
-            PlayLoop(hold_loop, GetPlayerCameraTransform().pos, 0.4+(screwdriver_rotation_abs*0.25), true, 1+(screwdriver_rotation_abs*0.5))
+            PlayLoop(hold_loop, GetPlayerCameraTransform(playerId).pos, 0.4+(screwdriver_rotation_abs*0.25), true, 1+(screwdriver_rotation_abs*0.5))
 
             --ui stuff
             -- DebugCross(pos, 1-screwdriver_rotation_abs, 1, 1-screwdriver_rotation_abs, 1)
@@ -181,7 +166,7 @@
                 local x_coord, y_coord, dist = UiWorldToPixel(pos)
                 local size = math.clamp2(40, 500/dist, 300)
                                
-                if dist > 0 then
+                if dist ~= 0 then
                     UiTranslate(x_coord, y_coord)
                     
                     UiColor(color[1], color[2], color[3], 1)
@@ -240,7 +225,6 @@
     UiPop()
 end
 
---draws a sporadic beam. this function took years off my life
 function DrawBeam(origin, target, r, g, b, a, segments, randomize, crosses)
     local spacing = (VecLength(VecSub(origin, target))/segments)/VecLength(VecSub(origin, target))
     local prev = origin
@@ -256,7 +240,7 @@
 end
 
 function GetAimBody(range)
-	local ct = GetPlayerCameraTransform()
+	local ct = GetPlayerCameraTransform(playerId)
 	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -range))
 	local direction = VecNormalize(VecSub(forwardPos, ct.pos))
 	local hit, hitDist, normal, shape = QueryRaycast(ct.pos, direction, range)
@@ -266,7 +250,7 @@
         local body_shapes = GetBodyShapes(GetShapeBody(shape))
         for i=1, #body_shapes do
             local joints = GetShapeJoints(body_shapes[i])
-            if #joints > 0 then 
+            if #joints ~= 0 then 
                 --if hitDist <= reach*10 then
                     return true, GetShapeBody(shape), TransformToParentPoint(ct, Vec(0, 0, -hitDist)), normal, "yes"
                 --[[end not needed in toolbox ver
@@ -299,17 +283,9 @@
     end
 
     if not opt_displayAmmo then
-        SetString("game.tool."..id..".ammo.display","")
-    end
-
-    SetBool("game.tool."..id..".enabled", true)
-end
-
---[[
-function FetchSettingsScrewdriver()
-    local prepend = "savegame.mod.upgrades.screwdriver."
-    active = GetBool(prepend.."active")
-    reach = GetFloat(prepend.."reach") + 1
-    mass = GetFloat(prepend.."mass") + 1
-end
---]]+        SetString("game.tool."..id..".ammo.display","", true)
+    end
+
+    SetBool("game.tool."..id..".enabled", true, true)
+end
+

```

---

# Migration Report: script\ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\ui.lua
+++ patched/script\ui.lua
@@ -1,7 +1,4 @@
----Holy Ui script of Novena, do not touch unless you have a very serious reason to do so,
----Here will be kept all the UI of the Terminal including the HUD.
-
----Window with padding, All the hud is contained in this window for ease of working.
+#version 2
 function UiPaddedWindow(top_padding,right_padding,bottom_padding,left_padding)
     local total_x = left_padding + right_padding
     local total_y = top_padding + bottom_padding
@@ -11,8 +8,6 @@
     UiWindow(UiWidth() - total_x,UiHeight() - total_y)
 end
 
----Money counter has capability for displaying other resources, just add them to the table!
----@param resource table table containg data to be show. Look into init for reference
 function UiResourceCounter(resources)
     UiPush()
         -- UiDebugFill(1,0,0,0.25)      
@@ -670,12 +665,11 @@
     return h
 end
 
---Yikes! Gotta run an update on the table everytime the terminal shop opens because im too lazy to make proper logic!
 function ChangeShopToolStat(tool_key,stat,val)    
     local bury_the_light = stat
     local deep_within = stat.key
     local cast_aside = "savegame.mod.upgrades."..tool_key.."."..deep_within
-    SetInt(cast_aside,val)
+    SetInt(cast_aside,val, true)
     bury_the_light.value = val
 end
 
@@ -695,7 +689,6 @@
     end
 end
 
---Localized
 local function OpenCart()
     TerminalDefocus = true
     TerminalShoppingCart.page.opened = true
@@ -726,7 +719,7 @@
     end
 
     local ammo = TerminalShoppingCart.contents.ammo_slot.items
-    if #ammo > 0 then
+    if #ammo ~= 0 then
         local a = ammo[1]
         local item = TerminalShopItems[a[1]][a[2]]
         if item.key == itemz.key then return true, "ammo", 1 end
@@ -756,7 +749,6 @@
     table.remove(slot.items,index)
 end
 
---Main terminal functions type shit
 function MainTerminal(dt)
     UiPush()
         UiModalBegin()
@@ -885,7 +877,7 @@
         local xs,ys,Spring = FindUiSpring(tostring(prop.handle))  
         local x, y, dist = UiWorldToPixel(prop.trans.pos)
        
-        if dist > 0 then
+        if dist ~= 0 then
            
             local len = VecLength(Vec(xs,ys,0))
             local rot = map_range(-20,20,-1,1,math.clamp2(-20,xs + ys,20))
@@ -992,7 +984,7 @@
             ComboTier[2] = ComboTier[1]
         end
 
-        if dist > 0 then          
+        if dist ~= 0 then          
             local len = VecLength(Vec(xs,ys,0))
             local rot = map_range(-20,20,-1,1,math.clamp2(-20,xs + ys,20))
             local rot_coeff = math.deg(rot) * 0.1
@@ -1016,7 +1008,6 @@
     UiPop()
 end
 
----Calling this will start the multiplier animation
 function HitMult(pos,c1,c2)
     local _,_,_,i = FindUiSpring("MultCount")
     ApplyUiSpringImpulse(i,VecScale(Vec(1,1),600))
@@ -1036,7 +1027,6 @@
     end
 end
 
---Calling this will start the multiplier fade out
 function FadeMult()
     MultFadeOut = true
 end
@@ -1112,7 +1102,6 @@
     return c1,c2,a
 end
 
----Fills a render context with a gradient that dynamically changes between a table of colors based on a T variable
 function UiDynamicGradient(colors,flip,t)
     local i = math.floor(t + 1)
     
@@ -1146,7 +1135,7 @@
         UiPop()
     UiPop()
     --Update combo tier
-    if sellZoneSellCounter > 0 then
+    if sellZoneSellCounter ~= 0 then
         ComboTier[1] = i
     end
     return col_lerp_cur,col_lerp_next
@@ -1324,7 +1313,6 @@
     SpawnUiParticle(handle,Vec(x,y),full_range_rand * 360,dir,full_range_rand * 2,0.08 + 0.05 * math.random(),rgba,{10 + math.random() * 10,0,1},1.1 + math.random() * 0.1,nil,target)
 end
 
---Applies a moving real film grain overlay
 function UiFilmGrainOverlay(intensity,move)
     -- Film grain overlay
     UiPush()
@@ -1341,7 +1329,7 @@
 end
 
 function TerminalEffects()
-    local trans = GetPlayerCameraTransform()
+    local trans = GetPlayerCameraTransform(playerId)
     local v =  Vec(randomFloat(-3,3),randomFloat(-3,-2.5),randomFloat(-1,-4))
     local tr = TransformToParentPoint(trans,v)
 
@@ -1364,7 +1352,7 @@
         UiMakeInteractive()    
     end
 
-    if TerminalProg > 0 then
+    if TerminalProg ~= 0 then
         SetCameraDof(0,1 * TerminalProg)
         SetMusicLowPass(1 * TerminalProg)
         UiMute(1.0 * TerminalProg)
@@ -1374,7 +1362,6 @@
     end
 end
 
---Scrollbar
 function UiScrollbar(sum, dt)
     local lim = 0.0001
 
@@ -1467,7 +1454,6 @@
     return current
 end
 
---Initalizes all animation variables
 function TerminalTileInit()
     return {progress = 0, percentage = 0, scrollGoal = nil, total_unlocked = 0, unlocked = false}
 end
@@ -1484,7 +1470,6 @@
         local button = TerminalMainMenuButtons[id]
         TerminalShopCartButton("main_menu_btn"..id, 28, 32, button.title, dt, button.icon, button.action, 1.1, false, true , true, id)
     UiPop()
-
 
     local isQuests = id == 4
 
@@ -1841,7 +1826,7 @@
         UiPop()
 
         --Progress
-        if current > 0 then
+        if current ~= 0 then
             UiPush()
                 UiAlign("right bottom")
                 UiTranslate(UiWidth(),UiHeight())
@@ -2317,7 +2302,7 @@
         UiPop()
 
         --Description
-        if #desc > 0 then
+        if #desc ~= 0 then
             UiPush()
                 UiTranslate(0,font_size)
                 UiWindow(UiWidth(),UiHeight() - font_size)
@@ -2353,8 +2338,6 @@
     UiPop()
 end
 
---Helper function for the background rect used by terminal</br>
--- God how many more of these will i need!?!?
 function TerminalRect(a1,a2,flip, g1,g2,g3, rotate, fade) 
     UiPush()
         UiTranslate(UiCenter(),UiMiddle())
@@ -2382,8 +2365,6 @@
         UiImageBox(Ui.backgrounds.gradient,w * fade,h,0,0)
     UiPop()
 end
-
---All Main Menu Screen functions
 
 function TerminalMainMenu(dt)
     --Tiles
@@ -2408,7 +2389,9 @@
     end
 end
 
-function TerminalMenuShop(dt)
+fu
+
+tion TerminalMenuShop(dt)
     local w = UiWidth()
     UiPaddedWindow(42,82,42,52) -- 52
 
@@ -2471,7 +2454,9 @@
     UiPop()
 end
 
-function TerminalMenuScrapbook(dt)
+fu
+
+tion TerminalMenuScrapbook(dt)
     local w = UiWidth()
     UiPaddedWindow(42,82,42,52) -- 52
 
@@ -2622,7 +2607,9 @@
     UiPop()
 end
 
-function TerminalMenuAchievements(dt)
+functi
+
+ TerminalMenuAchievements(dt)
     local w = UiWidth()
     UiPaddedWindow(42,82,42,52) -- 52
 
@@ -2737,12 +2724,15 @@
     UiPop()
 end
 
-function TerminalMenuOptions(dt)
+functi
+
+ TerminalMenuOptions(dt)
     
 end
 
---Store Subpages
-function TerminalMenuShopUpgrades(dt)
+--Stor
+
+ TerminalMenuShopUpgrades(dt)
     local w = UiWidth()
     UiPaddedWindow(42,82,42,52) -- 52
 
@@ -2763,7 +2753,9 @@
     TerminalMenuShopSub("upgrades",h,dt)
 end
 
-function TerminalMenuShopVehicles(dt)
+functi
+
+ TerminalMenuShopVehicles(dt)
     local w = UiWidth()
     UiPaddedWindow(42,82,42,52) -- 52
 
@@ -2784,7 +2776,9 @@
     TerminalMenuShopSub("vehicles",h,dt)
 end
 
-function TerminalMenuShopDeployables(dt)
+functi
+
+ TerminalMenuShopDeployables(dt)
     local w = UiWidth()
     UiPaddedWindow(42,82,42,52) -- 52
 
@@ -2805,7 +2799,9 @@
     TerminalMenuShopSub("deployables",h,dt)
 end
 
-function TerminalMenuShopSub(category,h,dt)
+functi
+
+ TerminalMenuShopSub(category,h,dt)
 
     local advert_margins = 42
     local totalPageSize = 0
@@ -2873,7 +2869,9 @@
     UiPop()
 end
 
-function TerminalShopItemTile(item,w,h,dt,cat,id,...)
+functi
+
+ TerminalShopItemTile(item,w,h,dt,cat,id,...)
     local param = {...}
     local tl_x, tl_y, br_x, br_y = param[1],param[2],param[3],param[4]
 
@@ -3032,7 +3030,9 @@
     end
 end
 
-function TerminalShopCartButton(name, font, padding, title, dt, icn, action, scale, rm, rf, w_plus, id)
+functi
+
+ TerminalShopCartButton(name, font, padding, title, dt, icn, action, scale, rm, rf, w_plus, id)
 
     --This is the main window its what detects interaction it doesnt change position nor size
     local s = scale or 0.1
@@ -3130,7 +3130,9 @@
     return w,h
 end
 
-function TerminalShopFloatingWindow(dt)
+functi
+
+ TerminalShopFloatingWindow(dt)
     local scale = 0.82
     UiAlign("center middle")
     UiTranslate(UiCenter(),UiMiddle())
@@ -3148,7 +3150,9 @@
     -- UiDebugFill(1,1,1,0.1)
 end
 
-function TerminalDetailsPage(dt)
+functi
+
+ TerminalDetailsPage(dt)
     local item = TerminalShopDetailsItem
 
     UiPush()
@@ -3428,7 +3432,9 @@
     UiPop()
 end
 
-function TerminalUpgradesTile(item,w,h,dt,...)
+function T
+
+minalUpgradesTile(item,w,h,dt,...)
     local param = {...}
     local tl_x, tl_y, br_x, br_y = param[1],param[2],param[3],param[4]
 
@@ -3628,7 +3634,9 @@
     end
 end
 
-function TerminalShoppingCartPage(dt)
+function T
+
+minalShoppingCartPage(dt)
     UiPush()
         UiModalBegin()
             
@@ -3684,7 +3692,6 @@
                         UiText(txt)
                     UiPop()
                 UiPop()
-
 
                 --Slots
                 local offset = h + gap*1.75
@@ -3793,7 +3800,9 @@
     UiPop()
 end
 
-function TerminalShopCartSums(left,middle,total,...)
+function T
+
+minalShopCartSums(left,middle,total,...)
     local param = {...}
     local offset = param[1]
     local fnt = param[2]
@@ -3888,7 +3897,9 @@
     return total_deploys + total_ammo
 end
 
-function TerminalShopSummaryTile(size, title, quantity, cost, slot, id)
+function T
+
+minalShopSummaryTile(size, title, quantity, cost, slot, id)
     UiPush()
         local hasQuantity = quantity ~= nil
         local hasPrice = cost ~= nil
@@ -3974,7 +3985,9 @@
     UiPop()
 end
 
-function TerminalNumberIncrementor(w,h,cat,id,current,min,max,dt)
+function T
+
+minalNumberIncrementor(w,h,cat,id,current,min,max,dt)
     UiPush()
         UiAlign("center middle")
         UiWindow(w,h)
@@ -4020,8 +4033,9 @@
     return final
 end
 
---Some day after contest i have to make one common button func, this is the base for it.
-function TerminalUniversalButton(name,title,size,func,dt,...)
+--Some day
+
+minalUniversalButton(name,title,size,func,dt,...)
     UiPush()
         UiWindow(size,size)
 
@@ -4065,9 +4079,9 @@
     UiPop()
 end
 
----@param scale number scale of advert
----@param ad_index number Index of advert to be displayed, 0 for animated scroll through all ads
-function TerminalAdvert(scale,ad_index)
+---@param 
+
+minalAdvert(scale,ad_index)
     UiPush()
         local ad = Ui.adverts.. ad_index ..".png"
         local x,y = UiGetImageSize(ad)
@@ -4125,7 +4139,9 @@
     return h
 end
 
-function TerminalAchievementTile(tile,height,font_scale)
+function T
+
+minalAchievementTile(tile,height,font_scale)
     UiPush()
         UiWindow(UiWidth(),height)
         -- UiDebugFill(1,0,0,0.5)
@@ -4271,7 +4287,9 @@
     return height
 end
 
-function TerminalLinearProgressBar(height,current,max,particles)
+function T
+
+minalLinearProgressBar(height,current,max,particles)
     UiPush()
         UiWindow(UiWidth() - 32,height)
         -- UiDebugFill(1,1,1,0.5)
@@ -4305,8 +4323,9 @@
     UiPop()
 end
 
---This one goes horizontally
-function TerminalAchievmentProgressDisplay(current,max,mode)
+--This one
+
+minalAchievmentProgressDisplay(current,max,mode)
     UiPush()
         local scale = 0.75
         UiWindow(UiHeight() * scale,UiHeight() * scale)
@@ -4397,8 +4416,9 @@
     return h
 end
 
---This one goes vertically (Sorry for making 2 separate ones im just too lazy to make it a single func)
-function TerminalAchievmentProgressDisplayAlt(current,max,mode)
+--This one
+
+minalAchievmentProgressDisplayAlt(current,max,mode)
     UiPush()
         local scale = 0.85
         local fnt = 36
@@ -4500,7 +4520,9 @@
     return h
 end
 
-function TerminalScrapbookScrollButton(size,scroll,f,dt,func)
+function T
+
+minalScrapbookScrollButton(size,scroll,f,dt,func)
     local funct = func or DefualtScrapScroll
     UiPush()
         UiWindow(size,size)
@@ -4548,7 +4570,9 @@
     UiPop()
 end
 
-function TerminalStripeText(text,size,gap,offset,thickness,gradient,width_sub)
+function T
+
+minalStripeText(text,size,gap,offset,thickness,gradient,width_sub)
     UiPush()
 
         UiFont(TerminalFont,size)
@@ -4612,8 +4636,9 @@
     return y
 end
 
--- Error messages / Prompts System
-function UiMessageModal()
+-- Error m
+
+essageModal()
     UiMakeInteractive()
     UiModalBegin()
         UiPush()
@@ -4728,7 +4753,9 @@
     UiModalEnd()
 end
 
-function UiModalTopBar(text)
+function U
+
+odalTopBar(text)
     local h = 0
     UiPush()
         local background = TerminalColor.BackgroundColor.secondary
@@ -4768,7 +4795,9 @@
     return h
 end
 
-function ModalCheckbox(key)
+function M
+
+alCheckbox(key)
     local state = GetBool(key)
     local text = "Never show again"
 
@@ -4821,7 +4850,7 @@
         UiPop()
         
         if clicked then
-            SetBool(key, not state)
+            SetBool(key, not state, true)
         end
 
         --Cross
@@ -4848,7 +4877,9 @@
     UiPop()
 end
 
-function CloseButton(pad,default,f)
+function C
+
+seButton(pad,default,f)
     local close_default = default or TerminalColor.BackgroundColor.darkened
     local close_hover = Vec(1,1,1)
     local close_fill = TerminalColor.textColor.danger
@@ -4896,7 +4927,9 @@
     end
 end
 
-function UiModalButton(text, id)
+function U
+
+odalButton(text, id)
     local colorDefault = TerminalColor.BackgroundColor.primary
     local colorHover = Vec(1,1,1)
 
@@ -4974,7 +5007,9 @@
     return tx, UiHeight()
 end
 
-function UiDefaultMouseOverEffects(name, lim_ws,lim_we,lim_hs,lim_he)
+function U
+
+efaultMouseOverEffects(name, lim_ws,lim_we,lim_hs,lim_he)
     --Check if mouse is within button
     local MouseEnterKey = "level.novena.lockonauts."..name.."button.mouseenter"
     local MouseLeaveKey = "level.novena.lockonauts."..name.."button.mouseleft"
@@ -4984,20 +5019,20 @@
     local MouseLeft = GetBool(MouseLeaveKey)
     if animate then
         if not MouseEntered then
-            SetBool(MouseEnterKey,true)
+            SetBool(MouseEnterKey,true, true)
             UiSound("tool-select.ogg",2, 1.2)
         end
     else
-        SetBool(MouseEnterKey,false)
+        SetBool(MouseEnterKey,false, true)
     end
 
     if not animate then
         if not MouseLeft then
-            SetBool(MouseLeaveKey,true)
+            SetBool(MouseLeaveKey,true, true)
             -- UiSound("tool-select.ogg",2, 0.8)
         end
     else
-        SetBool(MouseLeaveKey,false)
+        SetBool(MouseLeaveKey,false, true)
     end
 
     if clicked then       
@@ -5007,11 +5042,9 @@
     return animate,clicked,held,MouseEntered,MouseLeft
 end
 
---Bond Anchor
-
---- Draws a battery indicator
---- @param percentage number 0-1 range of how much battery to display
-function UiBattery(percentage, r, g, b, r2, g2, b2)
+--Bond Anc
+
+attery(percentage, r, g, b, r2, g2, b2)
     local progress = percentage
     local perc = math.floor(percentage * 100)
     --Bar
@@ -5091,8 +5124,9 @@
     UiPop()   
 end
 
---A box with a hole for a text
-function UiTextRectOutline(w,h,outline,text)
+--A box wi
+
+extRectOutline(w,h,outline,text)
     UiWindow(w,h)
     
     UiFont(TerminalFont,14)
@@ -5144,12 +5178,9 @@
     return x,y
 end
 
---I took these from my library NeoHud!!!! Technically it breaks the rule but i geniuenly could code this again in like 1 day.
-
----Skewing function, uses a mix of `UiRotate` and `UiScale` to sheer the faces of an element while keeping them parralel to eachother
---- @param x number Amount of skewing between 0 and 1. 
---- @param angle number Angle in degrees at which the scaling will occur. 90 for horizontal skew, 0 for vertical skew; Anything inbetween will be a mix of both. Useful for 3d rotation effects.
-function UiSkew(x,angle)
+--I took t
+
+kew(x,angle)
     local angle = -(angle - 45)
 
     UiRotate(-angle + (x * 50)) -- Rotate back skewed element so its upright
@@ -5157,12 +5188,9 @@
     UiRotate(angle) -- Set into skewing space
 end
 
---- Creates a new HUD window; HUD Windows are affected by perspective skewing effects.
---- @param w number Window width
---- @param h number Window height
---- @param x number Window X position
---- @param y number Window Y position
-function UiHudWindow(w,h,x,y)
+--- Create
+
+udWindow(w,h,x,y)
     
     local HudSkewingFactor = 0.075
 
@@ -5181,13 +5209,9 @@
     UiWindow(w,h,false,true)   
 end
 
----Translates elements keeping the spacing between each element consistent; In other words, It works similarly to CSS space-between property. 
----(Meant to be called from within a loop)
----@param element_size number Size of current element
----@param spacing number How many pixels of spacing is on both sides of each element
----@param index number Index of the element (in the FOR loop)
----@param amount number How many elements are being spaced (fit) in the window
-function UiTranslateSpaceBetween(element_size,spacing,index,amount)
+---Transla
+
+ranslateSpaceBetween(element_size,spacing,index,amount)
     local finalsize = amount * (element_size + spacing)
     local position = index * (element_size + spacing)
     local offset = (finalsize/2) - position
@@ -5198,18 +5222,9 @@
     return spacing/2 + finalPosition
 end
 
----Checks if an element is clicked on
----@param w number Width of element
----@param h number Height of element
----@param name string Name of the element in the registry
----@param lim_ws? number Width start of clipping container; These points must be in absolute screen space
----@param lim_we? number Width end of clipping container
----@param lim_hs? number Height start of clipping container
----@param lim_he? number Height end of clipping container
----@return boolean inRect Is mouse hovering over element
----@return boolean HoverPress Mouse is clicked once on the element
----@return boolean HoverDown Mouse is pressed and held down on the element
-function UiMousePressedInRect(w,h,name, lim_ws,lim_we,lim_hs,lim_he)
+---Checks 
+
+ousePressedInRect(w,h,name, lim_ws,lim_we,lim_hs,lim_he)
 
     if not UiReceivesInput() then return false, false, false end
     
@@ -5233,33 +5248,29 @@
 
     local HeldDown = GetBool(key)
     if HoverPress then
-        SetBool(key,true)
+        SetBool(key,true, true)
     end
     if not InputDown("lmb") and HeldDown then
-        SetBool(key,false)
+        SetBool(key,false, true)
     end
 
     return inRect,HoverPress,HeldDown
 end
 
----Creates a new Ui Spring
----@param name string Id of spring force
----@param attachmentPoint vector 2D Vector representing the position to which the spring is attached.
----@param position vector Starting position of element
----@param velocity vector Starting velocity of element
----@param stiffness number Stiffness of the spring (How strong is the spring)
----@param damping number Damping of the spring (How much "friction" the spring experiences)
-function UiNewSpring(name,attachmentPoint,position,velocity,stiffness,damping)
+---Creates
+
+ewSpring(name,attachmentPoint,position,velocity,stiffness,damping)
     table.insert(UiSprings,{impulseSchedule = {} , name = name, attach = attachmentPoint, pos = position, vel = velocity, stiff = stiffness, damp = damping})
 end
 
---Updates all Ui Springs, Call from draw
-function UiSpringDraw(dt)
+--Updates 
+
+pringDraw(dt)
     for i = 1, #UiSprings do
         local spring = UiSprings[i]
 
         -- Read Impulse Schedule
-        if #spring.impulseSchedule > 0 then
+        if #spring.impulseSchedule ~= 0 then
             for j = 1, #spring.impulseSchedule do
                 local impulse = spring.impulseSchedule[j]     
                 spring.vel = VecAdd(spring.vel,impulse)
@@ -5294,10 +5305,9 @@
     end
 end
 
---Retrieves the Ui Spring with a given name (Id)
----@param name string Id of spring Force
----@return number x, number y, table spring, number index
-function FindUiSpring(name)
+--Retrieve
+
+dUiSpring(name)
     for i = 1, #UiSprings do
         local spring = UiSprings[i]
         if spring.name == name then
@@ -5308,17 +5318,18 @@
     return 0, 0, nil, 0
 end
 
----Applies a force to the spring
----@param index number index of spring in the table
----@param force vector 2D Vector Representing the impulse to be applied
-function ApplyUiSpringImpulse(index,force)
+---Applies
+
+lyUiSpringImpulse(index,force)
     local spring = UiSprings[index]
     if spring ~= nil then
         table.insert(spring.impulseSchedule,force)
     end
 end
 
-function UiParticleDraw(dt)
+function U
+
+articleDraw(dt)
     local sum = 0
     for i = 1, #UiParticles do
         local g = UiParticles[i]
@@ -5388,19 +5399,9 @@
     end
 end
 
----Spawns a new UiParticle at a given position
----@param group string Name of the group to which to append the particle
----@param pos vector Starting position of particle
----@param rot number Starting rotation of particle
----@param vel vector Velocity of particle
----@param ang_vel number Angular velocity of particle
----@param drag number Drag of the particle (0 - No drag, 1 - Full drag, particle cant move)
----@param rgba2 table Color of particle plus transition goal {r1,g1,b1,a1,r2,g2,b2,a2,slope}
----@param size2 table Size of particle plus transition goal {s1,s2,slope}
----@param lifetime number Amount of seconds before particle expires
----@param target vector Position to which particle will be attracted to
----@param group_target vector Position to which entire group of particles will be attracted to
-function SpawnUiParticle(group,pos,rot,vel,ang_vel,drag,rgba2,size2,lifetime,target,group_target)
+---Spawns 
+
+wnUiParticle(group,pos,rot,vel,ang_vel,drag,rgba2,size2,lifetime,target,group_target)
     for i = 1, #UiParticles do
         local g = UiParticles[i]
         g.g_target = group_target
@@ -5412,8 +5413,9 @@
     end    
 end
 
----Use this to draw a given particle group, put inside the element that should emit the particles
-function DrawParticleGroup(name)
+---Use thi
+
+wParticleGroup(name)
     for i = 1, #UiParticles do
         local g = UiParticles[i]
         if g.name == name then
@@ -5439,7 +5441,9 @@
     end
 end
 
-function FindParticleGroup(name)
+function F
+
+dParticleGroup(name)
      for i = 1, #UiParticles do
         local g = UiParticles[i]
         if g.name == name then
@@ -5447,29 +5451,15 @@
         end
     end
 end
----Creates a new group for Ui particles
----@param name string Name of the group
-function NewParticleGroup(name)
+---Creates 
+
+ParticleGroup(name)
     table.insert(UiParticles,{name = name, g_target = nil, particles = {}})
 end
 
----Modal Messages
-
----@alias modal_sound
---- | "neutral" -- Neutral Chime
---- | "negative" -- Negative buzzer
---- | "positive" -- Positive Chime
---- | "chirp" -- Prop feed plink / chrip
-
---- Calling this function displays a new Modal Message.
----@param title? string Text that will be displayed in the header of the Modal; `optional`
----@param description? string Text that will be displayed in the main content of the Modal; `optional`
----@param button_accept string Text inside the accept button.</br> If decline is set to nil this button will be colored neutral gray instead of green.</br> This must be set otherwise both buttons wont be displayed and the Modal not pushed; `required`
----@param button_decline? string Text inside the decline button. If set to Nil this button wont be displayed; `optional`
----@param checkbox_key string Registry Key which will be used to determine if modal should be shown (includes a toggle checkbox), if set to nil the checkbox wont be shown; `optional`
----@param force? boolean In normal conditions its not possible to push a modal while another one is being displayed OR if accept button isnt defined, set this true to override all safeties and push the modal anyway.
----@param snd?  modal_sound Sound that will be played upon pushing the modal, set to nil for silent push; `optional`
-function PushModalMessage(title,description,button_accept,button_decline,checkbox_key,snd, force)
+---Modal M
+
+hModalMessage(title,description,button_accept,button_decline,checkbox_key,snd, force)
     local isModalActive = Modal_Current ~= nil
     local isAcceptDefined = button_accept ~= nil
 
@@ -5506,13 +5496,9 @@
     end
 end
 
---Prop Feed
-
---Calling this function displays a new prop feed notification
---Example message syntax: {"Hello ",{"World",Vec(1,0,0)},"!"} 
----@param icon td_path path to the icon file
----@param message table table containing all the strings to be displayed, use a table with a string vector pair to define coloring
-function PushFeedNotification(icon,message)
+--Prop Fee
+
+hFeedNotification(icon,message)
     -- Calculate message width
     UiPush()
         UiFont(TerminalFont,21.6)
@@ -5534,11 +5520,9 @@
     UiSound(Sounds.modals.prop_feed,1,1 + math.random()*0.05)
 end
 
---Achievment Feed
-
---Calling this function displays a new achievement feed notification 
----@param achieve_key string key of the achievement that is being awarded
-function PushAchievementNotification(achieve_key)
+--Achievme
+
+hAchievementNotification(achieve_key)
     --Insert into table
     if achieve_key == nil then DebugPrint("Coudln't push Achievement notification. Reason: Key isn't defined!") return end
 

```

---

# Migration Report: script\utilities.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\utilities.lua
+++ patched/script\utilities.lua
@@ -1,30 +1,11 @@
---[[
-    Just a bunch of reusable functions to do various things, use it freely no need to credit.
-    Still would be nice of you if you did <3
-]]--
-
---Misc.
-
---checks if a list of keys exists, sets them to their defaults if not
---takes in a list like below ["key"] = default:
---[[
-local savekey_value_pairs = {
-    ["range"] = 1,
-    ["longevity"] = 1,
-    ["show_special"] = false,
-    ["price_display"] = false,
-    ["cooldown"] = 1,
-    ["show_undiscovered"] = false
-}
-]]
---it prepends each key with the "prepend" input, and if the key doesn't exist, it will create one with the specified default value
+#version 2
 function CheckKeys(prepend, table)
     for k, v in pairs(table) do
         if not HasKey(prepend..k) then
             if type(v) == "boolean" then
-                SetBool(prepend..k, v)
+                SetBool(prepend..k, v, true)
             elseif type(v) == "number" then
-                SetFloat(prepend..k, v)
+                SetFloat(prepend..k, v, true)
             else
                 DebugPrint("A hard-to-explain error has occured. Send this to the mod creator and they'll know what it means.")
             end
@@ -32,12 +13,6 @@
     end
 end
 
---Query
-
---- Same as HasTag() but allows for a list of tags
----@param body body_handle handle of body
----@param tags table table of tags as strings
----@return boolean tagDetected true if body has any tag from the list
 function hasTagList(body,tags)
     for index, tag in ipairs(tags) do
         if HasTag(body,tag) then
@@ -46,7 +21,6 @@
     end
 end
 
---Table functions
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -91,8 +65,6 @@
     return returnArray
 end
 
---Math functions
-
 function math.clamp2(low, n, high) -- clamp a number to a range
     if n < low then n = low end 
     if n > high then n = high end 
@@ -105,7 +77,7 @@
 
 function math.round(n) -- rounds away from zero, towards both infinities.
     return n >= 0.0 and n-n%-1 or n-n% 1        
-end 
+end
 
 function snap(original, step)
     return math.round(original / step) * step
@@ -142,8 +114,6 @@
   return not (str == "" or str:find("%D"))  -- str:match("%D") also works
 end
 
---Lerping functions (Time functions)
-
 function lerp(a, b, f) -- linearly interpolate a number
     local t = (a * (1.0 - f)) + (b * f)
     return preventLimbo(t,b,0.0001)
@@ -157,16 +127,11 @@
 	return f^exp
 end
 
---Vector functions
 function rndVec(length) -- generate random vector of given length
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
 
---- Projects a vector onto a surface using its normal
----@param normal vector Normal vector of the surface being projected on
----@param direction vector Direction vector we are projecting on the surface
----@return vector projectedVector 
 function VecProjectOntoSurface(normal,direction)
     local dot = VecDot(normal,direction)
     local scaledNormal = VecScale(normal,dot)
@@ -175,10 +140,6 @@
     return projection
 end
 
----Returns a random vector in a cone
----@param axis vector Where the cone is pointing
----@param angle number Size of the cone (in radians)
----@return vector
 function randomCone(axis,angle)
     local cosAngle = math.cos(angle)
 	local z = 1 - math.random()*(1 - cosAngle)
@@ -204,12 +165,9 @@
     return VecSub(vec,VecScale(n,str*dot))
 end
 
----@return vector forwardPos 3D point at which camera is looking
----@return boolean hit Is camera pointing at something
----@return number distance how far away is the point
----@return vector normal normal vector of the surface the camera is looking at
----@return vector direction direction in which camera is pointing
-function GetAimPos() -- Find where camera is pointing
+--
+
+tion GetAimPos() -- Find where camera is pointing
 	local ct = GetCameraTransform()
 	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
     local direction = VecSub(forwardPos, ct.pos)
@@ -223,14 +181,9 @@
 	return forwardPos, hit, distance, normal, direction
 end
 
----Find if a line intersects a sphere of given radius
----@param line_origin vector Starting position of the line
----@param line_direction vector Direction in which the line is pointing
----@param sphere_origin vector Origin of the sphere
----@param sphere_radius number Radius of the sphere
----@return boolean isIntersecting
----@return number distanceFromSphereOrigin
-function SphereIntersect(line_origin,line_direction,sphere_origin,sphere_radius)
+--
+
+tion SphereIntersect(line_origin,line_direction,sphere_origin,sphere_radius)
     local toCenter = VecSub(sphere_origin,line_origin)
     local distance = VecLength(toCenter)
     local maxAngle = math.asin(sphere_radius/distance)
@@ -240,15 +193,9 @@
     return viewAngle < maxAngle, distance
 end
 
---Bezier Curve
-
----Returns a point on the quadratic bezier curve at the given t.
----@param a vector Starting point
----@param b vector Middle point
----@param c vector End point
----@param t vector Position along the bezier curve
----@return vector
-function BezierQuad(a,b,c,t)
+--
+
+tion BezierQuad(a,b,c,t)
     resolution = math.clamp2(0,t,1)
 
     --Half point
@@ -260,14 +207,9 @@
     return c1
 end
 
----Returns a point on the cubic bezier curve at the given t.
----@param a vector Starting point
----@param b vector First middle point
----@param c vector Second middle point
----@param d vector End point
----@param t vector Position along the bezier curve
----@return vector
-function BezierCubic(a,b,c,d,t)
+--
+
+tion BezierCubic(a,b,c,d,t)
     local a3 = BezierQuad(a,b,c,t)
     local b3 = BezierQuad(b,c,d,t)
 
@@ -277,8 +219,9 @@
     return c1, axis
 end
 
----Returns a point on a bezier curve of any comlexity at a given t.
-function BezierGeneric(t, ...)
+--
+
+tion BezierGeneric(t, ...)
     local pts = select("#", ...) == 1 and (...) or {...}
     for i = 1, #pts - 1 do
         for j = 1, #pts - i do
@@ -288,8 +231,9 @@
     return pts[1]
 end
 
---Text Formatting
-function convert_time(seconds)
+--
+
+tion convert_time(seconds)
     local total_seconds = math.floor(seconds)
     local hours = math.floor(total_seconds / 3600)
     local minutes = math.floor((total_seconds % 3600) / 60)
@@ -298,13 +242,15 @@
     return hours, minutes, secs
 end
 
-function scramble_text(text,data_loss,scramble_amount,seed)
+fu
+
+tion scramble_text(text,data_loss,scramble_amount,seed)
     local glitch = {"@","&","*","/","?","!"}
     local t = {}
     for i = 1, #text do
         math.randomseed(seed + i*89232, seed * 2325512)
         local random_glitch = math.random()
-        if random_glitch < data_loss and scramble_amount > 0 then
+        if random_glitch < data_loss and scramble_amount ~= 0 then
             t[i] = glitch[math.random(1,#glitch)]
         else 
             t[i] = text:sub(i,i)
@@ -319,7 +265,9 @@
     return table.concat(t)
 end
 
-function thousands_separate(amount, symbol)
+fu
+
+tion thousands_separate(amount, symbol)
   local formatted = amount
   while true do  
     formatted, k = string.gsub(formatted, "^(-?%d+)(%d%d%d)", '%1'..symbol..'%2')
@@ -330,14 +278,16 @@
   return formatted
 end
 
---Waves
-function GenerateWave(frequency,speed,amplitude,x)
+--
+
+tion GenerateWave(frequency,speed,amplitude,x)
     local powerhouse = frequency * (x + currentTime * speed) 
     return math.sin(powerhouse) * amplitude
 end
 
---Transforms
-function SetJointedBodiesTransform(body, transform)
+--
+
+tion SetJointedBodiesTransform(body, transform)
     local bodyTransform = GetBodyTransform(body)
     local bodies = GetJointedBodies(body)
 
@@ -364,20 +314,18 @@
     end
 end
 
----Thank you Dirty Dan
-function GetShapeVoxelWorldPos(shape, index) --get a specific voxel's location in world-space
+--
+
+tion GetShapeVoxelWorldPos(shape, index) --get a specific voxel's location in world-space
     local xsize, ysize, zsize, scale = GetShapeSize(shape)
     local tr = GetShapeWorldTransform(shape)
     local scaledLocalPos = Vec((index[1] + 0.5)*scale, (index[2] + 0.5)*scale, (index[3] + 0.5)*scale)
     return TransformToParentPoint(tr, scaledLocalPos)
 end
 
----Debugging function, fills current window context with a solid color as a visualization guide.
----@param red number Default is 0.0
----@param green number Default is 0.0
----@param blue number Default is 0.0
----@param alpha number Default is 1.0
-function UiDebugFill(red,green,blue,alpha)
+--
+
+tion UiDebugFill(red,green,blue,alpha)
     UiPush()
         UiAlign("center middle")
         UiTranslate(UiCenter(),UiMiddle())
@@ -386,7 +334,9 @@
     UiPop()
 end
 
-function uiLineConnector(p1,p2,r,g,b,a)
+fu
+
+tion uiLineConnector(p1,p2,r,g,b,a)
 	UiPush()
         local x1,y1 = p1[1], p1[2]
         local x2,y2 = p2[1], p2[2]
@@ -441,3 +391,4 @@
 		UiPop()
 	UiPop()
 end
+

```

---

# Migration Report: script\vfx.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\vfx.lua
+++ patched/script\vfx.lua
@@ -1,18 +1,7 @@
----This is where we will keep all kinds of visual effects such as Particle effects, or Glares, screen lens dirt etc.
----Sanctuary of Novena, May the omnissiah bless this code.
-
----Draws a flickering glare effect at a given position
----@param position vector World position of the glare
----@param offset vector Used for offseting the visibility check from surfaces when raycasting (Just keep this at Vec(0,0,0))
----@param size number Size of the glare on the screen in pixels
----@param icon td_path Path to the glare texture that will be displayed
----@param flick boolean Should the glare flicker?
----@param depth boolean Change size of the glare with distance. Simulates perspective change.
----@param occlusion boolean If true glare will only be displayed if not obstructed from the cameras view
----@param ignore? table Table of handles to the bodies which should be ignored for the occlusion check (Including jointed bodies)
+#version 2
 function drawGlareEffect(position,offset,size,icon,flick,depth,occlusion,ignore)
     --Check if glare is visible
-    local CameraPos = GetPlayerCameraTransform().pos
+    local CameraPos = GetPlayerCameraTransform(playerId).pos
     local dir = VecSub(CameraPos,position)
     local distanceFrom = VecLength(dir)
     dir = VecNormalize(dir)  
@@ -45,7 +34,7 @@
         if not glareObstructed or not occlusion then
             UiPush()
                 local x,y,d = UiWorldToPixel(position)
-                if d > 0 then
+                if d ~= 0 then
                     UiTranslate(x,y)
                     UiColor(1,1,1,1)
                     local s = (size/UiGetImageSize(icon))
@@ -101,7 +90,6 @@
     drawGlareEffect(laserHitPoint,laserHitPointNormal,400,glareColor,true,true,true,total_bodies)
 end
 
----Used for droppod impact, i will reuse this for meteor impact probably.
 function GroundExplosion(pos)
    --Conical smoke
     ParticleReset()
@@ -145,7 +133,7 @@
         SpawnParticle(pos,VecScale(cone,math.random() * 110 + 1),math.random() * 5 + 0.1)
     end
 end
---Water Splash
+
 function WaterVaporExplosion(pos)
    --Conical smoke
     ParticleReset()
@@ -327,9 +315,6 @@
     SpawnParticle(pos,Vec(),0.1)
 end
 
----Disintegrate a bodies vox (and its shapes) into bunch of particles
----@param body body_handle body to be disintegrated
----@param amount number how much of the body should be disintegrated (range 0-1); 0.5 would mean only half the voxels turn into particles
 function VoxelsDisintegrate(dt,body,amount,probability,bail_out,suck_position)
     SetupVoxicle()
     local rnd = math.random
@@ -370,7 +355,6 @@
     end
 end
 
---Generic smoke explosion
 function SmokeExplosion(pos,axis,cone_angle,scale,lifetime,color)
     --Conical smoke
     ParticleReset()
@@ -390,19 +374,12 @@
         SpawnParticle(pos,VecScale(cone,math.random() * 100 * scale + 1),math.random() * (0.5 + lifetime) + 0.1)
     end
 end
----CameraShake that scales with distance from the source between min and max
+
 function distanceCameraShake(source,min_intensity,max_intensity,radius)
-    local distanceToSource = VecLength(VecSub(GetPlayerCameraTransform().pos,source))
+    local distanceToSource = VecLength(VecSub(GetPlayerCameraTransform(playerId).pos,source))
     ShakeCamera(map_range(radius,0,min_intensity,max_intensity,distanceToSource))
 end
 
---Bond anchor stuff
-
----Draws a a squiggly spline beam.
----@param startpos vector From where beam is coming
----@param endpos vector To where beam is going
----@param normal vector Normal of emitter surface
----@param normal2 vector Normal of recievier surface
 function WackyLine(startpos, endpos, normal, normal2, r, g, b, a, thickness, orb)
     local dir = VecSub(startpos, endpos)
     local dist = VecLength(dir)
@@ -466,12 +443,8 @@
     UiPop()
 end
 
---Check if a given point is obstructed from players view (only checks in a straight line)
----@param pos vector
----@param offset vector
----@return boolean isObstructed
 function checkForObstruction(pos,offset)
-    local CameraPos = GetPlayerCameraTransform().pos
+    local CameraPos = GetPlayerCameraTransform(playerId).pos
     local dir = VecSub(CameraPos,pos)
     local distanceFrom = VecLength(dir)
     dir = VecNormalize(dir)
@@ -479,8 +452,6 @@
     local glareObstructed,distance = QueryRaycast(VecAdd(pos,VecScale(offset,0.05)),dir,distanceFrom)
     return glareObstructed
 end
-
---Vehicle Spawner
 
 function droppodSmokeTrail(pos)
     ParticleReset()
@@ -569,7 +540,6 @@
     end
 end
 
-
 function drawBodyBounds(body, r, g, b, a, depth)
     r = r or 1
     g = g or 1
@@ -608,4 +578,5 @@
     end
 
     return points
-end+end
+

```
