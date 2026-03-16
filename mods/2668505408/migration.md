# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,19 +1,4 @@
---This script will run on all levels when mod is active.
---Modding documentation: http://teardowngame.com/modding
---API reference: http://teardowngame.com/modding/api.html
-
-function init()
-end
-
-function tick(dt)
-end
-
-function update(dt)
-end
-
-function draw(dt)
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type=type(orig)
     local copy
@@ -27,4 +12,5 @@
         copy=orig
     end
     return copy
-end+end
+

```
