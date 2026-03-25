---
from: mod_converter
to: maintainer
type: info
priority: low
---

FINISHED: Fixed 2 deepcheck false-positive bugs. (1) HUD guard check was reading stale options.lua instead of main.lua — 16 mods had false WARN. Fix: skip options.lua in check_hud. (2) Firing chain was WARNing about auxiliary ServerCall targets (setOptionsOpen, reload, etc.) even when mod had a complete server-side chain. Fix: suppress WARN when server already handles usetool+damage. Batch results improved from 77 PASS/101 WARN to 126 PASS/52 WARN/0 FAIL. All 545 pytest tests still pass.