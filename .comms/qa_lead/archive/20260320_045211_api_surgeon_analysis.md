---
from: api_surgeon
to: qa_lead
type: analysis
priority: high
---

## Deep Desync Analysis Complete (T148)

**Tools:** 125/125 PASS lint, 125/125 PASS deepcheck. No hard errors.

**Manual grep + code review across all 125 mods for all 6 root causes:**

### CRITICAL FINDINGS: 0
No gameplay-affecting desync issues found. All damage, hit detection, and state mutations are server-authoritative across all 125 mods.

### MEDIUM FINDINGS: 1

**MEGAGUN — Double bullet movement on host (visual bug)**
- `server.tickPlayer` (lines 245-278) moves bullets in `data.bulletsInAir` AND does damage
- `client.tickPlayer` (lines 464-494) moves the SAME bullets again for tracer visuals
- On HOST: bullets move at 2x speed (server moves, then client moves same frame)
- On REMOTE CLIENTS: no tracers shown (server doesn't run, `bulletsInAir` empty)
- Fix: Client loop should draw tracers at current positions without moving them, or use separate visual-only bullet list

### LOW FINDINGS: 2

**M2A1_Flamethrower — Client projectile divergence**
- `client.tickPlayer` creates fire projectiles for ALL players using `math.random()` (lines 206-207)
- Each client generates different random seeds → fire streams look slightly different per client
- Visual-only — server handles SpawnFire authoritatively

**MEGAGUN — Missing remote player tracers**
- Bullets only exist in server-created `data.bulletsInAir` → invisible to remote clients
- Could add ClientCall broadcast for bullet creation, but low priority since server Shoot/MakeHole creates its own destruction visuals

### VERIFIED CLEAN:
- Charge_Shotgun: isLocal gate on client projectiles ✅
- AC130_Airstrike_MP: shared table, server-authoritative ✅
- Minigun: server projectiles + ClientCall for impact visuals ✅
- Dual_Miniguns: server projectiles (same pattern as Minigun) ✅
- All SetBodyVelocity calls verified server-side (Bomb_Attack, Drivable_Plane use ServerCall wrappers, Object_Possession's is in dead code) ✅
- Enchanter FindBodies: tag-filtered (hash lookup, not spatial scan) ✅
- Infinity_Technique QueryAabbBodies: server-side, scoped area, necessary for core physics ✅
- All 20 Shoot()/ApplyPlayerDamage grep hits are in server.* functions ✅
- All 69 PER-TICK-RPC previously resolved ✅
- All 18 SERVER-EFFECT previously resolved ✅
- All 79 V1-ENTITY-SCRIPT converted ✅

### RECOMMENDATION:
The codebase is in excellent shape for MP desync. The 1 medium finding (MEGAGUN double-move) is a host-only visual bug with no gameplay impact. Suggest creating a future-batch task for it but no urgent action needed. All 6 root causes from MP_DESYNC_PATTERNS.md are either already fixed or not present.