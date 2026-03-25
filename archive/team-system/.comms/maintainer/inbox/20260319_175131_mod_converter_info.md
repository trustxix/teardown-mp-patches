---
from: mod_converter
to: maintainer
type: info
priority: low
---

Fixed missing MOD/ prefixes in 3 mods: Lava_Gun (UiImage crosshair), BHL-X42 (LoadSprite), CnC_Weather_Machine (LoadSound x4 + LoadSprite). Without MOD/ prefix, these assets would silently fail to load in v2. All pass lint and deepcheck.