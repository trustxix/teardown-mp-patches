# Migration Report: animation.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/animation.lua
+++ patched/animation.lua
@@ -1,16 +1,9 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------
-model = {}
-model.animator = 0
-
-
-------------------------------------------------------------------------
-function init()
-	model.animator = FindAnimator()
+#version 2
+function server.init()
+    model.animator = FindAnimator()
 end
 
-
-function tick(dt)
+function server.tick(dt)
     MakeRagdoll(model.animator)
 end
+

```

---

# Migration Report: prefab\ragdoll\animation.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/prefab\ragdoll\animation.lua
+++ patched/prefab\ragdoll\animation.lua
@@ -1,16 +1,9 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------
-model = {}
-model.animator = 0
-
-
-------------------------------------------------------------------------
-function init()
-	model.animator = FindAnimator()
+#version 2
+function server.init()
+    model.animator = FindAnimator()
 end
 
-
-function tick(dt)
+function server.tick(dt)
     MakeRagdoll(model.animator)
 end
+

```
