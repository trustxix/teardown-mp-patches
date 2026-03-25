---
from: mod_converter
to: maintainer
type: info
priority: low
---

Fixed missing MOD/ prefix on asset paths in 4 more mods: Hurricanes_and_Blizzards (8 paths across 4 files), Ion_Cannon_Beacon (8 paths), Jetpack (1 path). Without MOD/ prefix, LoadSound/LoadSprite silently fail in v2. Total this session: 7 mods fixed for MOD/ prefix (Lava_Gun, BHL-X42, CnC_Weather_Machine, Hurricanes_and_Blizzards, Ion_Cannon_Beacon, Jetpack + M2A1_Flamethrower asset copy). All pass lint and deepcheck.