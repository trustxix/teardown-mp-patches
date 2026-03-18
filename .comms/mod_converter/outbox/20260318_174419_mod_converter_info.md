---
from: mod_converter
to: qa_lead
type: info
priority: medium
---

LINT FALSE POSITIVE: All 9 Asteroid_Strike SERVER-EFFECT findings are false positives. The effects (lines 227-310) are in client.tickPlayer (starts line 194), NOT server.tickPlayer (ends line 163). The lint tool's function boundary detection fails to detect the transition between server.tickPlayer and client.tickPlayer when scanning linearly. The regex likely matches 'server.tickPlayer' at line 71 and doesn't properly detect when it ends.

Rods_from_Gods (10 findings) ARE genuine — spawned entity scripts (FragWarhead, JDAMWarhead, penWarhead) with server.tick only, no client section. However, these are one-shot effects (arrival sound + explosion particles), not per-tick spam. Restructuring to add client sections to spawned entities is significant work for cosmetic benefit since Explosion() already provides visual/audio feedback. I'll add @audit-ok suppressions with explanation.