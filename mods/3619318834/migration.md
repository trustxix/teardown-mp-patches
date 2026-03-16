# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,9 +1,5 @@
-#include "src/sdk/symbols.lua"
-#include "src/sdk/base.lua"
-#include "src/sdk/weapons.lua"
+#version 2
+function server.init()
+    initAssaultPack2()
+end
 
-#include "src/assault-pack2.lua"
-
-function init()
-    initAssaultPack2()
-end
```

---

# Migration Report: src\assault-pack2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\assault-pack2.lua
+++ patched/src\assault-pack2.lua
@@ -1,11 +1,8 @@
---[[
-#include "bazooka.lua"
-#include "shotgun.lua"
-]]
-
+#version 2
 function initAssaultPack2()
     DebugPrint("AssaultPack2:Initializing")
     registerHandHeldWeapon(_weaponBazooka, "M9 Bazooka", "MOD/vox/Bazooka.vox", "4", Bazooka)
     registerHandHeldWeapon(_weaponShotgun, "Shotgun", "MOD/vox/Shotgun.vox", "2", Shotgun)
     DebugPrint("AssaultPack2:Initialized")
 end
+

```

---

# Migration Report: src\bazooka.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\bazooka.lua
+++ patched/src\bazooka.lua
@@ -1,42 +1 @@
-_weaponBazooka = "pb_bazooka"
-
-Bazooka =
-{
-    aimPoses          = {
-        _aimPoseShoulder,
-        _aimPoseIron,
-        _aimPoseIronSideways,
-    },
-    aimOffset         = { x = 0, y = .2, z = 0, tilt = 0 },
-    aimOffsets        = {
-        [_aimPoseShoulder] = { x = -.1, y = .35, z = .15, tilt = 0, sway = 1 },
-        [_aimPoseIron] = { x = -.1, y = .35, z = .15, tilt = 5, fov = 80, sway = .5 },
-        [_aimPoseIronSideways] = { x = -.1, y = .35, z = .15, tilt = 5, fov = 60, sway = .35 },
-    },
-    leftHandTransform =
-        Transform(
-            Vec(.31, -.575, -.575),
-            QuatEuler(0, 90, 0)
-        ),
-    elements          = {},
-    barrelOffset      = Vec(0.325, -0.375, -1.31),
-    effects           = 10,
-    otherEffects      = {
-        {
-            transform = Transform(),
-            effects = 10,
-        }
-    },
-    fireModes         = { 1 },
-    fireMode          = 1,
-    ammo              = {
-        [_munitionM6HEP] = {
-            size   = 5,
-            reload = 2.5,
-        },
-        [_munitionM6HEAT] = {
-            size   = 5,
-            reload = 2.5,
-        },
-    },
-}+#version 2

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

# Migration Report: src\sdk\symbols.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\sdk\symbols.lua
+++ patched/src\sdk\symbols.lua
@@ -1,49 +1 @@
-handHeldWeaponsRegPath  = "level.ProBallistics.weapons.handheld"
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
@@ -1,57 +1,4 @@
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
 function compare(a, b, path)
     path = path or "::"
     local typeA = type(a)
@@ -88,9 +35,10 @@
 
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

# Migration Report: src\shotgun.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/src\shotgun.lua
+++ patched/src\shotgun.lua
@@ -1,57 +1 @@
-_weaponShotgun = "pb_shotgun"
-
-Shotgun =
-{
-    aimPoses     = {
-        _aimPoseShoulder,
-        _aimPoseIron,
-        _aimPoseIronSideways,
-    },
-    aimOffset    = { x = 0, y = .2, z = 0, tilt = 0 },
-    aimOffsets   = {
-        [_aimPoseShoulder] = { x = -.05, y = .15, z = .1, tilt = 0, sway = 1 },
-        [_aimPoseIron] = { x = -.325, y = .22, z = -.1, tilt = 0, fov = 70, sway = .35 },
-        [_aimPoseIronSideways] = { x = -.05, y = -.2, z = .1, tilt = 0, fov = 100, sway = 1.25 },
-    },
-    elements     = {
-        barrel = {
-            transform = Transform(
-                Vec(.3, -.4, -1.15),
-                QuatEuler(-90, 0, 0)
-            ),
-            zActionOffset = 0,
-            zActionDelay = .25,
-        },
-        bolt = {
-            zActionOffset = .1,
-            transform = Transform(
-                Vec(0.3, -.45, -.45),
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
-    barrelOffset = Vec(0.325, -0.375, -1.46),
-    fireModes    = { 1 },
-    fireMode     = 1,
-    effects      = 4,
-    ammo         = {
-        [_munition12gauge] = {
-            size   = 12,
-            reload = 2,
-        },
-        [_munitionBirdShot] = {
-            size   = 12,
-            reload = 2,
-        },
-        [_munitionSlug] = {
-            size   = 12,
-            reload = 2,
-        },
-    },
-}
+#version 2

```
