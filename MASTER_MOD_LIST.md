# Teardown MP Mod Patcher — Master Mod List

> Last updated: 2026-03-21 (mod set changed — 112 installed, ~34 new from workshop backlog, some old removed)

## Summary

| Status | Count |
|--------|-------|
| **Currently installed** | **112** |
| **Lint clean (tier 1)** | **112/112** |
| **Removed (user unsubscribed)** | 66+ (53 on 2026-03-19, more since) |
| **New installs (from workshop backlog)** | ~34 (maps, vehicles, tools) |
| **Deferred (documented, not convertible)** | 13 (5 installed, 8 not) |
| **Previously installed (before all cleanups)** | 178 |
| **Total workshop items (incl. maps)** | 243 |

> Counts updated 2026-03-21. **112 mods installed, all 112 lint clean** (was 125 on 2026-03-20, was 178 before 2026-03-19 cleanup). User changed mod set: unsubscribed additional mods beyond the original 53 removals, and installed ~34 new mods from the workshop backlog. QA Lead resolved all 38 tier-1 findings in the new installs: 13 false-positive suppressions (MISSING-VERSION2 in framework files), 1 entity script v2 conversion (SVERLOVSK tv.lua), backup file cleanup (Light_Saber, WIP_GYM), API Surgeon fixed RAW-KEY-PLAYER bugs in 3 mods (Light_Saber, Portal_Gun_MP, Thruster_Tool_Multiplayer — Issue #73). Deep analysis: re-running (T168 in progress — previous results were 16h old with 178 tested, now 112 mods). **Removed mods (original 53 on 2026-03-19):** All 39 RMW weapon pack mods (Batch 7), plus: 500_Magnum, SG553, Liquify, Shape_Collapsor, Easy_Chat, Performance_Mod, Easy_Admin_Menu, Jetpack, ARM_NOVA, FELL_TITAN, American_High_School, Poltergeists, Ultimate_Jetpack, Always_Up. Additional mods removed since then (exact list TBD — user changed subscriptions).

## Fully Patched Mods (Batch 1 — 35 mods)

- ~~.500 Magnum (2401591426)~~ — **REMOVED (2026-03-18): v1 tool ID conflict with Batch 3 v2 rewrite (Issue #38)**
- [MP] AC130 Airstrike WIP (3667283920)
- AK-47 (2401590749)
- AWP (2401577826) — full v2 rewrite 2026-03-18: 4 ammo types, zoom scope, custom projectile physics, server/client split
- Attack Drone (2419814408)
- Bee Gun (2425682439)
- Black Hole (2401574819)
- C4 (2415643616) — full v2 rewrite 2026-03-18: explosives planting, timed detonation, keybind system, server/client split
- Charge Shotgun (2401590321)
- Desert Eagle (2401591803)
- Dragonslayer (2880985063)
- Dual Berettas (2401592266)
- Dual Miniguns (2455771839)
- Exploding Star (2401872536)
- Guided Missile (2401872753)
- HADOUKEN (2416310614)
- High Tech Drone (2965297478)
- Holy Grenade (2401873154)
- Hook Shotgun (2412621869)
- Laser Cutter (2401589688)
- Lightkatana (2401592617)
- Lightsaber (2547915810)
- M1 Garand (2408922595)
- M249 (2401591017)
- M4A1 (2401590490)
- Magic Bag (2401576135)
- Minigun (2401575951)
- Mjölner (2401593417) — full v2 rewrite 2026-03-18: lightning, heavy strike, boost jump, server/client split, 480 lines
- Multi Grenade Launcher (2401871778)
- Nova Shotgun (2401871202)
- P90 (2401590906)
- SCAR-20 (2401590057)
- ~~SG553 (2401591104)~~ — **REMOVED (2026-03-19): user unsubscribed**
- Scorpion (2401577403)
- Vacuum Cleaner (2401577133)

## Fully Patched Mods (Batch 2 — 10 mods)

- Acid Gun (2826557844)
- Airstrike Arsenal (2877387699)
- Lava Gun (2854539326)
- Lightning Gun (3173859813)
- M2A1 Flamethrower (3661732417)
- Multiple Grenade Launcher (3600437109)
- ODM Gear (3661214063)
- Revengeance Katana (2648760922)
- Thruster Tool (2515871265)
- Winch (3681340622)

## Fully Patched Mods (Batch 3 — 5 mods)

- ~~500 Magnum (2401591426)~~ — **REMOVED (2026-03-19): user unsubscribed** (`500_Magnum/` dir removed)
- Asteroid Strike (2614499023)
- Fire Locator (2622849832)
- Swap Button (2728464103)
- Welding Tool (2840497593)

## Fully Patched Mods (Batch 4 — 4 mods)

- Molotov Cocktail (2424838731) — polished from workshop (mostly v2), fixed raw key bug
- [MP] Tripmine (3662075963) — polished from workshop (already v2), added ammo HUD + hints
- Remote Explosives (3621598329) — full v2 conversion, fixed iterators + raw key bugs
- Rods from God (3633035942) — full v2 conversion, uses shared table for cross-player visibility

## Fully Patched Mods (Batch 5 — 2 mods, converted from v1)

- ~~Liquify (2782511908)~~ — **REMOVED (2026-03-19): user unsubscribed** (was full v2 conversion, voxel decomposition + anti-gravity mode + options menu)
- MEGAGUN (2497213038) — full v2 conversion, 3 ammo types + 6-barrel rotation + wind-up state machine

## Fully Patched Mods (Batch 6 — 7 mods, installed from workshop pre-v2)

- Bomb Attack (3656255489) — polished, added audit annotations
- CnC Weather Machine (2531655676) — polished, fixed draw() signature + ammo setup
- Drivable Plane (2649954750) — polished, fixed mousedx→camerax + ammo setup
- Ion Cannon Beacon (2511805965) — fixed 3 RAW-KEY-PLAYER bugs + ammo setup
- Jackhammer (3628059485) — fixed 3 ipairs bugs → proper v2 iterators + ammo setup
- Object Possession (2562082522) — fixed textbox raw keys + ammo setup
- ~~Shape Collapsor (2643910768)~~ — **REMOVED (2026-03-19): user unsubscribed** (was fixed 5 RAW-KEY-PLAYER bugs + ammo setup)

## ~~Fully Patched Mods (Batch 7 — 39 mods, RMW weapon pack by Mr. Rubyyy)~~ **ALL 39 REMOVED (2026-03-19): user unsubscribed**

> All 39 RMW weapon pack mods removed from Steam Workshop subscriptions. Patches were complete and working but user chose to remove the entire pack.

**Rocket launchers (exemplar: SMAW):**
- ~~MK 153 SMAW (3401161858)~~ — REMOVED
- ~~RPG-7 (3401161673)~~ — REMOVED

**Hitscan guns (exemplar: USP45):**
- ~~USP45 (3408725894)~~ — REMOVED
- ~~MP443 (3401402900)~~ — REMOVED
- ~~Stoeger Double Defense (3405943128)~~ — REMOVED
- ~~PKP Pecheneg (3404747101)~~ — REMOVED
- ~~AUG A3 (3414850251)~~ — REMOVED

**Mass batch conversion (32 mods, template-applied from USP45):**
- ~~RMW_92FS (3401402675), RMW_AA12 (3414873272), RMW_AK74 (3453623778), RMW_AK74M (3401161489), RMW_AKM (3416512833), RMW_BarrettM82 (3420845311), RMW_BoforsAK5 (3575990304), RMW_CZBren2 (3456192497), RMW_ColtKingCobra (3404784805), RMW_DesertEagle (3405979963), RMW_FAMAS (3453503295), RMW_FNP90 (3575668960), RMW_FNSCAR (3401417008), RMW_G17 (3401403081), RMW_G36C (3407553780), RMW_G3A1 (3453220485), RMW_HK416 (3512024787), RMW_KrissVector (3408682775), RMW_M110SASS (3404785331), RMW_M16 (3418348908), RMW_M16A2 (3512026573), RMW_M249 (3404747328), RMW_M4A1 (3401161277), RMW_M870 (3405104694), RMW_MG3 (3499183286), RMW_MK18 (3407023588), RMW_MP5 (3405573992), RMW_MP7 (3581952805), RMW_QBZ95 (3582628842), RMW_SA80 (3454536933), RMW_SIGSpear (3528009592), RMW_SVD (3404785067)~~ — ALL REMOVED

## Fully Patched Mods (Batch 8 — 2 mods, new workshop conversions)

- Explosive Pack (2604914470) — 6 explosive types (C4, EMP, Claymore, Landmine, Incendiary, Door Breach), full server/client split, OptionsMenu, claymore player damage
- Portal Gun (2421609769) — per-player portal pairs, server-authoritative teleportation/physics, custom raycast shader, object pickup, options menu, keybind hints. 3208→~850 lines. Mod #103.

## Fully Patched Mods (Batch 9 — 20 mods, conversion sprint 2026-03-18)

> Originally targeted 38 unpatched mods. 20 converted, remainder deferred to UMF/complexity.

**Standalone conversions (T56 — api_surgeon):**
- Gasoline Flamethrower (2739855429) — mod #105. 590→~290 lines. Server SpawnFire, client multi-layer particles, adjustable nozzle velocity, OptionsMenu. Lint clean.
- Bombard (2843848555) — mod #107. 843→~450 lines (6 files). First entity mod with full v2 split: lightning stick tool + cannon entity (server-authoritative firing) + 3 cannonball variants. Lint clean.
- Sith Saber (2598610013) — mod #116. 2550→~460 lines. Melee arc (12 QueryShot rays), saber throw (registry sync projectile), force crush/jump, 10 blade variants, 3-layer spark effects via ClientCall. Lint clean.
- Final Flash (3553116743) — mod #117. 2958→~340 lines. Energy beam weapon (Dragon Ball Z). Charge-up, terrain destruction via MakeHole, player damage via QueryShot+ApplyPlayerDamage, body push. Lint clean.

**Utility conversions:**
- Magnetizer V2 (3008661123) — mod #119. 1716→~470 lines (6 files). Magnet physics tool with 3 modes (attract selected/attract nearby/attract to player), lightning effects, tip rotation, options menu. Lint clean.
- Artillery Barrage RELOADED (3592259278) — mod #120. 3731→~957 lines v2 main.lua + 170 lines options.lua + 151 lines i18n.lua. Area-effect tool: server handles barrage timing + MakeHole/Explosion/SpawnFire + ApplyPlayerDamage, client handles sounds/particles/camera/circle selection UI/drone view. Lint clean (1 INFO: MANUAL-AIM @audit-ok).
- Spells (2906575554) — mod #121. 1063→~620 lines. Magic tool with 18 spells: dual-hand system, terrain destruction, physics manipulation, teleport, flying, telekinesis. Lint clean.
- Vortexes and Tornadoes (2983703634) — mod #122. 3092→~480 lines. Shared world tornado entity: server handles tornado movement, MakeHole destruction, body suction, player damage. Client handles funnel particles, sounds, camera shake, options menu. Tornado position synced via registry. Lint clean.
- Hurricanes and Blizzards (3669298473) — mod #123. Already v2 from workshop (author: Riv), installed and fixed 6 raw key bugs (InputDown/InputPressed with player param in UI textbox code). Lint clean.

**G17 framework (T54 — mod_converter):**
- G17 Framework (2597745035) — mod #106. 2638→~470 lines. Replaced custom projectile system with Shoot() API. Template for 8+ framework guns. Lint clean.
- Kriss Vector (2595780161) — mod #108. 3314→554 lines. Cloned from G17 template. Full auto SMG.
- AK-105 (2536589821) — mod #109. 3845→553 lines. From G17 template.
- AK-12 (2653176229) — mod #110. 3524→553 lines. From G17 template.
- AK-74 (2682043380) — mod #111. 3861→553 lines. From G17 template.
- G36K (2588821225) — mod #112. 3362→553 lines. From G17 template.
- SCAR (2686729186) — mod #113. 3565→553 lines. From G17 template.
- Saiga-12 (2651403234) — mod #114. 2350→553 lines. From G17 template.
- Dragunov SVU (2670830203) — mod #115. 2195→553 lines. From G17 template.
- M4A1 Framework (2637503043) — mod #118. 4027→554 lines. From G17 template. 3 fire modes (Safe/Semi/Full), grenade launcher, toolId "ar15".
- *All 9 framework gun clones lint clean. Template pattern: ~553 lines each, all features Y.*

**Telekinesis (mod_converter):**
- Telekinesis (3330426273) — mod #104. 796→~630 lines. State-driven input: 8 raw keys batched into one ServerCall/tick. Grab/push/pull/rotate/implode/explode/freeze/float/liquify/cut/detach. Lint clean. **DONE**

## Fully Patched Mods (Batch 10 — 18 mods, workshop expansion sprint 2026-03-18)

> Workshop scan for non-UMF, already-v2 or easily convertible mods. Vehicle/gameplay mods included for first time.

**Vehicles:**
- Jetskis (3493864419) — mod #124. Author: Pufv. Vehicle pack, already v2, lint clean.
- Toyota Supra MP (3623476589) — mod #125. Author: Highexer/ironmjp. Vehicle, already v2. **Lint clean** (was 50 WARN — door sounds moved server→client via ClientCall pattern, 2026-03-18).
- Armored Vehicles MP (3641794940) — mod #126. Author: TurtleBravo85. Vehicles, already v2. 2 INFO (MANUAL-AIM, SHOOT-NO-ATTRIB in boat turret — accepted).
- Soviet Vehicle Pack MP (3656187063) — mod #127. Author: ZvezdaKot. Vehicles, already v2, lint clean.
- Haul Truck MP (3678137931) — mod #128. Author: tislericsm. Vehicle, already v2, lint clean.

**Weapons/Gameplay:**
- Spawnable Missiles MP (3632821615) — mod #129. Author: Sky. Missiles/bombs, already v2. 5 WARN + 2 INFO (CRJ-200 FUEL system: SERVER-EFFECT/PER-TICK-SPATIAL — needs complete rewrite).
- Predator Missile MP (3653080381) — mod #130. Author: unknown. Guided missile, already v2. 3 INFO (MAKEHOLE-DAMAGE, 2x PER-TICK-SPATIAL — accepted).

**Utilities:**
- ~~Easy Chat (3621818416)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #131, MP chat system)
- ~~Performance Mod (3635399720)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #132, perf optimizations)
- VectorRazor (3578552621) — mod #133. Author: TheKnook. Precision cutting tool, already v2 from workshop. Fixed 7 MP bugs (raw key+player param on all keybinds, missing PlayersAdded/SetToolAmmo/AmmoPickup, PointLight in server, missing options sync). 3 INFO remaining (accepted).
- ~~Easy Admin Menu (3623360646)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #134, host admin utility)
- Bunker Buster MP (3629456835) — mod #135. Author: ekzesh. Missile strike tool, already v2. Added SetToolAmmoPickupAmount + ammo display. 31 SERVER-EFFECT WARNs accepted (host-only sounds/particles, functional).
- ~~Jetpack (3684366389)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #136, official Tuxedo Labs mod)

**Batch 1 upgrades (same session):**
- AWP — full v2 rewrite: 4 ammo types, zoom scope, custom projectile physics
- C4 — full v2 rewrite: explosives planting, timed detonation, keybind system
- Mjolner — full v2 rewrite: lightning, heavy strike, boost jump, server/client split

**Lint cleanup sweep (2026-03-18):**
> mod_converter: Toyota_Supra_MP door sounds (50→0), MrRandoms_Vehicles turrets (22→11), Predator_Missile_MP (8→3), vehicle annotations. qa_lead: HANDLE-GT-ZERO ARM exclusions, CLIENT-SERVER-FUNC regex. VectorRazor installed+fixed (10→3). Overall: **134→40 findings** (94 eliminated). 0 Tier 1 FAIL. 127/138 mods lint clean. 350 tests.

**Graduated from review (QA approved 2026-03-19):**
- ARM Glock (workshop v2+ARM framework) — mod #154. Lint suppressions for ARM framework patterns.
- ARM M4A4 (workshop v2+ARM framework) — mod #155. Lint suppressions for ARM framework patterns.
- ~~ARM NOVA (workshop v2+ARM framework)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #156)
- MrRandoms Vehicles (workshop v2) — mod #157. 11 INFO only (vehicle turret attribution — accepted).
- Multiplayer Spawnable Pack (workshop v2) — mod #158. 3 INFO only (sensor/trampoline QueryRaycast — accepted).

**Rejected during sprint (not installed):**
- ~~6 vehicle packs~~ — **ALL NOW INSTALLED** via auto-fixers in Batch 11 (#138-#144, #149)
- Tool_Menu (v1-only, no MP support — removed from disk)
- Multiplayer_C4 (duplicate of Remote_Explosives — Issue #54, not installed)

## Fully Patched Mods (Batch 11 — 17 mods, auto-fixer sprint 2026-03-18/19)

> Workshop fully exhausted after this batch. Key enablers: fix_raw_key_player (fixer #8) unlocked 6 previously rejected vehicle mods, fix_missing_version2 (fixer #9) unlocked 2 large mods. 9 auto-fixers total, 408 tests.

**T65 — Vehicles (mod_converter):**
- Dumb Stupid Fast Cars (2905643568) — mod #137. Author: Davvv. Vehicle/asset pack. Fixed draw()→client.draw() + #version 2 in entity script.
- Vehicle Pack Remastered MP (3625284752) — mod #138. Author: Highexer. 140+ vehicles. Fixed steering_wheel (raw key→client+ServerCall), mousedx→camerax, draw()→client.draw() x2.

**T66 — Auto-fix unlocked (mod_converter):**
- FPV Drone Tool (3665352411) — mod #139. Author: Okidoki. FPV drone tool. Auto-fixed 36→0 FAIL. Added AmmoPickup + version header.
- Light Katana MP (3636049807) — mod #140. Light katana weapon. Auto-fixed 13→0 FAIL. Added AmmoPickup.

**T67 — Previously rejected, now auto-fixable (mod_converter):**
- Legacy Tank MP (3685326977) — mod #141. Author: volifnap. Tank mod. Auto-fixed + #version 2 headers.
- Armour Framework MP (3662000095) — mod #142. Author: Kooshing. Armoured vehicle framework. Auto-fixed.
- DAM Helis (3647839189) — mod #143. Author: Kooshing. Dynamic helicopters. Auto-fixed.
- Koenigsegg Agera MP (3661548934) — mod #144. Author: entity. High-detail vehicle. Auto-fixed, lint clean.
- The Office US (3681605791) — mod #145. Author: Starspiker. Content/map, TV show recreation. Auto-fixed, lint clean.

**T68 — Final workshop sweep (mod_converter):**
- ~~FELL TITAN (3324149490)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #146, content/map)
- PPAN Vehicle Pack (2417100319) — mod #147. Author: Please Pick a Name. Vehicle pack (YLVF framework). Auto-fixed 8 issues (mousedx, draw→client.draw, handle-gt-zero). Added #version 2 to 6 entity scripts.
- ~~American High School (3543507771)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #148, content/map)
- Service Vehicles MP (3624449716) — mod #149. Author: Tortoise Work. Vehicle pack (tow truck, police car, bus, crane, garbage truck, SWAT van). Auto-fixed 2 raw-key-player issues.

**T69-T72 — QA Lead direct installs:**
- All-In-One Utilities (3622561177) — mod #150. Author: thicc putin. Multi-tool utility. Auto-fixed 17→0 FAIL (fixer #9: fix_missing_version2).
- Minecraft Building Tool (2755694436) — mod #151. Author: NLferdiNL. Building tool, 7980 lines. Auto-fixed 9→0 FAIL (fixer #9).
- Hide and Seek (3624969238) — mod #152. Author: BisocM. MP game mode (hide & seek). Apache 2.0 license, GitHub source. Features: admin controls, hider abilities, infection mode, spectators, localization.
- Gwel Mall (3683526762) — mod #153. Author: Gwel. Content/map, large mall environment.

## Fully Patched Mods (Batch 12 — 3 mods, Very High conversions + workshop install 2026-03-19)

> First successful conversions of "Very High" complexity mods. Session also: FPV_Drone_Tool server PlaySound→ClientCall fix, keybind hints added to all 4 ARM mods, cross-mod duplicate tool ID detection in audit, 12 @lint-ok suppressions removed (improved MISSING-OPTIONS-GUARD). Plan docs: `docs/superpowers/plans/2026-03-19-infinity-technique-v2.md`.

- Infinity Technique (3549181010) — mod #159. Author: DiggolBick. Satoru Gojo's Limitless/Infinity cursed technique: Blue, Red, Purple, Infinity barrier, Domain Expansion, Fly, Teleport, Telekinesis, Lock, Strength, Time Control, Performance mode. 3505→~950 lines. Full v2 server/client split with registry sync for VFX, 30+ assets. First "Very High" mod converted. Lint clean.
- ARM AK-47 (3665100521) — mod #160. Author: ARM framework. Already v2 from workshop. Auto-fixed 7→0 findings (5 raw-key-player removed, 1 #version 2 header added to projectile.lua, 1 MANUAL-AIM suppressed). Keybind hints added: [R] Reload [MMB] Fire Mode [Shift] ADS. Lint clean.
- GYM Ragdoll (3668043935) — mod #161. Author: GLaD. 3 medical tools (bandages, resurrect, sedatives) + body part health HUD + ragdoll entity script. 294→320 lines v2 main.lua (server/client split, HUD helpers). gore.lua: added #version 2 header. Removed 9 backup lua files. Second "Very High" mod converted. Lint clean.

## Fully Patched Mods (Batch 13 — 16 mods, UMF Bypass + v1→v2 conversions 2026-03-19)

> UMF-blocked mods converted without porting the framework. Strategy: rewrite each mod's game logic as standalone v2 (~119-1071 lines), dropping the ~7000-12000 line UMF framework entirely. API Surgeon built UMF-to-v2 translation guide (`docs/UMF_TRANSLATION_GUIDE.md`). Also includes v1→v2 conversions (TABS_Effect, Adjustable_Fire). **16 mods total** (14 UMF bypass + 2 v1→v2), completing the workshop exhaustion milestone.

- Omni Gun (2994616319) — mod #162. Author: Geneosis. Physics projectile spawner that copies voxel shapes. 370 lines standalone v2 (replaces ~11K UMF framework). 15 configurable settings via options menu (fire rate, spread, velocity, density, friction, bounce, solid, unbreakable, explosive, ghost), shape copy system (CopyShapePalette + CopyShapeContent), cleanup command. Lint clean.
- Magnets (2783125614) — mod #163. Author: Geneosis. Place N/S polarity magnets that attract/repel via physics simulation. ~330 lines standalone v2. Server-authoritative magnet physics (force/factor configurable), place/drop/remove/flip-polarity/attach-detach commands, polarity visualization (client-throttled FindBodies at 4Hz), options menu with 5 settings. Lint clean.
- ~~Ultimate Jetpack (2776716903)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #164, UMF bypass conversion, 310 lines)
- ~~Poltergeists (2744169679)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #165, UMF bypass conversion, 580 lines)
- Melt (3005988296) — mod #166. Author: Geneosis. Aim at any shape and melt it away voxel by voxel. 350 lines standalone v2. 3 melt modes, options menu, heat effects. UMF bypass conversion. Lint clean.
- Bouncepad (2706150164) — mod #167. Author: Geneosis. Place trampolines, bouncepads, jumppads and antipads to bounce players and objects. 500 lines standalone v2. Server physics, client rendering via ClientCall sync. UMF bypass conversion. Lint clean.
- Corrupted Crystal (2969580627) — mod #168. Author: Geneosis. Place corrupted crystals that grow and spread across surfaces. 400 lines standalone v2. Auto-grow configurable crystals. UMF bypass conversion. Lint clean.
- Singularity (2759823622) — mod #169. Author: Geneosis. 10 singularity physics effects. 530 lines standalone v2. UMF bypass conversion. Lint clean.
- Solid Sphere Summoner (3234758956) — mod #170. Author: Geneosis. Summon solid spheres, charge and launch them. Grab and spin any object. 460 lines standalone v2. UMF bypass conversion. Lint clean.
- Control (3134340282) — mod #171. Author: Geneosis. Telekinetic powers — grab/throw objects, super jump, ground slam, hover, dash. 430 lines standalone v2. UMF bypass conversion. Lint clean.
- BHL-X42 (2721596235) — mod #172. Author: Geneosis. Launch tiny black holes and watch them grow. UMF bypass conversion (T85). Lint clean.
- TABS Effect (3541730926) — mod #173. Author: Okidoki. Adds fire/smoke effects to TABS-tagged vehicles (broken engines smoke, hulls catch fire, fuel leaks). Global mod, v1→v2 conversion (T87). Lint clean.
- Adjustable Fire (2622040244) — mod #174. Author: NLferdiNL. Global fire settings mod (max count, spread, no-fire mode, clear all). v1→v2 conversion (T88). 119 lines. Lint clean.
- Enchanter (3576567190) — mod #175. Author: Geneosis. Apply and dispel enchantments on objects. UMF bypass conversion (T91). 1071 lines standalone v2. Lint clean.
- ~~Always Up (3240423177)~~ — **REMOVED (2026-03-19): user unsubscribed** (was mod #176, UMF bypass conversion, 572 lines)
- Hungry Slimes (2695893023) — mod #177. Author: Geneosis. Launch slimes that eat voxels, duplicate, and consume everything. UMF bypass conversion (T92). 602 lines standalone v2 (replaces ~12K UMF). Lint clean.

---

## Unpatched Workshop Tool Mods — Conversion Candidates

> Inventory built 2026-03-18 from 162 Tool-tagged workshop items. Excludes: 13 duplicate IDs of already-patched mods, 32 already-converted RMW mods, 14 already-v2 workshop mods, 10 non-tool items (frameworks, maps, model packs).

### Large Guns (1000+ lines) — Complex Conversions

| Name | Workshop ID | Lines | Notes |
|------|------------|-------|-------|
| ~~M4A1 (Tesseractahedron)~~ | ~~2637503043~~ | ~~4027~~ | **DONE — mod #118 as M4A1_Framework, toolId "ar15" (no conflict)** |
| ~~AK-74~~ | ~~2682043380~~ | ~~3861~~ | **DONE — mod #111, from G17 template** |
| ~~AK-105~~ | ~~2536589821~~ | ~~3845~~ | **DONE — mod #109, from G17 template** |
| ~~SCAR~~ | ~~2686729186~~ | ~~3565~~ | **DONE — mod #113, from G17 template** |
| ~~AK-12~~ | ~~2653176229~~ | ~~3524~~ | **DONE — mod #110, from G17 template** |
| ~~Infinity Technique~~ | ~~3549181010~~ | ~~4004 total~~ | **DONE — mod #159, full v2 rewrite. 12 abilities (Blue, Red, Purple, Infinity barrier, Domain Expansion, etc.)** |
| ~~G36K~~ | ~~2588821225~~ | ~~3362~~ | **DONE — mod #112, from G17 template** |
| ~~Kriss Vector~~ | ~~2595780161~~ | ~~3314~~ | **DONE — mod #108, from G17 template** |
| ~~Final Flash~~ | ~~3553116743~~ | ~~2958~~ | **DONE — mod #117** |
| ~~G17~~ | ~~2597745035~~ | ~~2638~~ | **DONE — mod #106 as G17_Framework** |
| ~~Saiga-12~~ | ~~2651403234~~ | ~~2350~~ | **DONE — mod #114, from G17 template** |
| ~~Dragunov SVU~~ | ~~2670830203~~ | ~~2195~~ | **DONE — mod #115, from G17 template** |
| ~~Thermite Cannon~~ | ~~2539026789~~ | ~~1691~~ | **BLOCKED — UMF dependency (moved to UMF section)** |
| ~~Artillery Barrage RELOADED~~ | ~~3592259278~~ | ~~1505~~ | **DONE — mod #120** |
| GLARE | 3114561159 | 6100+ total | Gamma laser beam weapon (not started — needs full v2 rewrite, LnL framework) |
| ~~Sith Saber~~ | ~~2598610013~~ | ~~1225~~ | **DONE — mod #116** |
| ~~Spells~~ | ~~2906575554~~ | ~~1063~~ | **DONE — mod #121** |

### Medium Tools (200-999 lines)

| Name | Workshop ID | Lines | Notes |
|------|------------|-------|-------|
| ~~Telekinesis~~ | ~~3330426273~~ | ~~796~~ | **DONE — mod #104** |
| ~~Magnetizer V2~~ | ~~3008661123~~ | ~~718~~ | **DONE — mod #119** |
| The Lockonauts Toolbox | 3586166386 | 8412 total | Multi-tool utility (misleading — 213 main.lua, 8k+ across all files) |

### Small Standalone Tools (<200 lines) — Convertible

| Name | Workshop ID | Lines | Notes |
|------|------------|-------|-------|
| ~~Vortexes and Tornadoes~~ | ~~2983703634~~ | ~~3092 total~~ | **DONE — mod #122, tornado physics entity** |
| ~~Gasoline Flamethrower~~ | ~~2739855429~~ | ~~66~~ | **DONE — mod #105** |
| ~~Bombard~~ | ~~2843848555~~ | ~~238~~ | **DONE — mod #107, spawn-only asset** |

### Small Tools — UMF DEPENDENT (NOT convertible without UMF v2 port)

> These mods depend on the UMF (Universal Mod Framework) by Geneosis. Each mod's main.lua is 47-71 lines, but the UMF framework adds 10,000-14,000 lines with v1 callbacks that bypass RegisterTool. **UMF bypass strategy (2026-03-19):** Rewriting each mod without UMF (~300-1100 lines each) — proven viable. **14 mods converted** (Batch 13: #162-#177). Translation guide: `docs/UMF_TRANSLATION_GUIDE.md`. **4 remaining DEFERRED:** Ascended Sword Master, AI Trainer, Blight Gun, Thermite Cannon + Shards Summoner.

| Name | Workshop ID | Lines | Notes |
|------|------------|-------|-------|
| Ascended Sword Master | 3358293229 | 74 | **DEFERRED** — ~4,577 game logic lines, 14 sword stances, too complex for bypass |
| ~~Hungry Slimes~~ | ~~2695893023~~ | ~~72~~ | **DONE — mod #177, UMF bypass conversion (T92), 602 lines** |
| ~~Poltergeists~~ | ~~2744169679~~ | ~~72~~ | **DONE — mod #165, UMF bypass conversion** |
| ~~BHL-X42~~ | ~~2721596235~~ | ~~71~~ | **DONE — mod #172, UMF bypass conversion (T85)** |
| ~~Bouncepad~~ | ~~2706150164~~ | ~~70~~ | **DONE — mod #167, UMF bypass conversion** |
| ~~Singularity~~ | ~~2759823622~~ | ~~63~~ | **DONE — mod #169, UMF bypass conversion** |
| Shards Summoner | 2888719505 | 60 | **DEFERRED** — 2,677 lines game logic |
| ~~Magnets~~ | ~~2783125614~~ | ~~60~~ | **DONE — mod #163, UMF bypass conversion** |
| ~~Enchanter~~ | ~~3576567190~~ | ~~58~~ | **DONE — mod #175, UMF bypass conversion (T91), 1071 lines** |
| AI Trainer | 2918508637 | 58 | **DEFERRED** — UMF dependent |
| ~~Control~~ | ~~3134340282~~ | ~~57~~ | **DONE — mod #171, UMF bypass conversion** |
| ~~Melt~~ | ~~3005988296~~ | ~~57~~ | **DONE — mod #166, UMF bypass conversion** |
| ~~Corrupted Crystal~~ | ~~2969580627~~ | ~~54~~ | **DONE — mod #168, UMF bypass conversion** |
| Blight Gun | 3004952393 | 51 | **DEFERRED** — UMF dependent |
| ~~Solid Sphere Summoner~~ | ~~3234758956~~ | ~~47~~ | **DONE — mod #170, UMF bypass conversion** |
| ~~Omni Gun~~ | ~~2994616319~~ | ~~47~~ | **DONE — mod #162, UMF bypass conversion** |
| ~~Ultimate Jetpack~~ | ~~2776716903~~ | ~~68~~ | **DONE — mod #164, UMF bypass conversion** |
| ~~Always Up~~ | ~~3240423177~~ | ~~68~~ | **DONE — mod #176, UMF bypass conversion (T90), 572 lines** |
| Thermite Cannon | 2539026789 | 1691 | **DEFERRED** — UMF dependent (reclassified from Large Guns) |

### Already V2-Compatible (workshop) — Status Tracker

> Tested during workshop expansion sprint (2026-03-18). Originally 10+ mods with 7-36 FAIL each. Auto-fixers #8 and #9 resolved most. **All DONE** (13 mods patched, 2 duplicates skipped).

| Name | Workshop ID | Lines | Notes |
|------|------------|-------|-------|
| ~~Light Katana~~ | ~~3636049807~~ | ~~2509~~ | **DONE — mod #140, fully patched** (auto-fixed 13→0 FAIL, fixer #8) |
| ~~Bunker Buster Missile [MP]~~ | ~~3629456835~~ | ~~2195~~ | **DONE — mod #135, fully patched** (AmmoPickup+AmmoDisplay added, 31 SERVER-EFFECT accepted) |
| ~~Minecraft Building Tool~~ | ~~2755694436~~ | ~~2087~~ | **DONE — mod #151, fully patched** (auto-fixed 9→0 FAIL, fixer #9: fix_missing_version2) |
| ~~(ARM) NOVA [MP]~~ | ~~3665100095~~ | ~~1628~~ | **DONE then REMOVED (2026-03-19)** — was mod #156, user unsubscribed |
| ~~(ARM) M4A4 [MP]~~ | ~~3667727633~~ | ~~1533~~ | **DONE — mod #155, graduated** (ARM framework lint suppressions) |
| ~~(ARM) Glock [MP]~~ | ~~3665100775~~ | ~~1502~~ | **DONE — mod #154, graduated** (ARM framework lint suppressions) |
| ~~(ARM) AK-47 [MP]~~ | ~~3665100521~~ | ~~1494~~ | **DONE — mod #160, fully patched** (auto-fixed 7→0, keybind hints added) |
| ~~FPV Drone Tool [MP]~~ | ~~3665352411~~ | ~~1406~~ | **DONE — mod #139, fully patched** (auto-fixed 36→0 FAIL, fixer #8: fix_raw_key_player) |
| Portal Gun [MP] | 3659913820 | 1325 | v2, workshop MP fork (our conversion uses original 2421609769) |
| ~~VectorRazor [MP Update]~~ | ~~3578552621~~ | ~~1067~~ | **DONE — mod #133, fully patched** (7 MP bugs fixed: raw key+player param, missing PlayersAdded/AmmoPickup, server PointLight, options sync) |
| ~~All-In-One Utilities [MP]~~ | ~~3622561177~~ | ~~584~~ | **DONE — mod #150, fully patched** (auto-fixed 17→0 FAIL, fixer #9: fix_missing_version2) |
| ~~Easy Admin Menu~~ | ~~3623360646~~ | ~~528~~ | **DONE — mod #134, fully patched** (host admin utility, lint false positives annotated) |
| Thruster Tool (MP) | 3625787751 | 310 | v2, duplicate of our Thruster_Tool |

### Excluded (Not Convertible)

- RPM Playermodels (3401098159) — model pack, no script
- Zombies [AUTUMNATIC] (3011292197) — map/gameplay, no tool script
- ~~[GLaD] GYM Ragdoll (3668043935)~~ — **DONE — mod #161** (v2 conversion, 294→320 lines, 9 backup files removed)
- GNOME ZONE (3209546457) — map mod
- ~~Tool Menu (2418422455)~~ — **REMOVED from disk 2026-03-18** (v1-only utility, no MP support)
- Prop Gallery (3043828547) — spawner utility
- Debug Scanner (2885663661) — debug utility

### Deferred Mods (13 — documented, not convertible)

> All 243+ workshop items assessed. These 13 mods are deferred with documented reasons. Updated 2026-03-21.

| Name | Workshop ID | Reason | Lines | Installed? |
|------|------------|--------|-------|------------|
| Flying_Planes | 2423986361 | TDSU framework dependency, vehicle/map | 24,565 | Yes |
| GLARE | 3114561159 | LnL framework dependency, full v2 rewrite needed | 6,100+ | Yes |
| Robot_Vehicles | 2673451391 | UMF framework dependency, vehicles | 20,805 | Yes |
| Synthetic Swarm | 3289269367 | **DO NOT CONVERT** — drone swarm factory, too complex | ~3,000+ | Yes |
| Thermite Cannon | 2539026789 | UMF dependent | 1,691 | Yes |
| The Lockonauts Toolbox | 3586166386 | Deceptively large multi-tool, custom UI rewrite needed | 8,412 | No |
| Chaos_Mod | 2433702881 | Described as 429 lines but actually 8,100 across all files | 8,100 | No |
| Player_Scaler | 2598890168 | MP-incompatible physics (player size manipulation) | 464 | No |
| Ascended Sword Master | 3358293229 | UMF — 4,577 game logic lines, 14 sword stances, too complex for bypass | 4,577 | No |
| Shards Summoner | 2888719505 | UMF — 2,677 lines game logic | 2,677 | No |
| AI Trainer | 2918508637 | UMF dependent | ~1,000+ | No |
| Blight Gun | 3004952393 | UMF dependent | ~1,000+ | No |
| Tameable Dragon | 2945997960 | UMF — 5,037 lines AI (dragon behavior too complex) | 5,037 | No |

### Conversion Priority Recommendation (COMPLETED)

> All convertible mods done. Workshop fully exhausted 2026-03-19. Original plan from API Surgeon T50 pre-analysis (2026-03-18).

1. ~~**Portal Gun:**~~ **DONE** — mod #103. 3208→~850 lines.
2. ~~**G17 framework gun series (10 mods):**~~ **ALL DONE** — G17 template + 9 clones. ~553 lines each.
3. ~~**Standalone weapons:**~~ **ALL DONE** — Sith Saber, Final Flash, Artillery Barrage, Gasoline Flamethrower, Bombard.
4. ~~**Complex mods:**~~ **2 DONE, 2 DEFERRED** — ~~Infinity Technique~~ (#159), ~~GYM Ragdoll~~ (#161). Deferred: GLARE, Lockonauts Toolbox.
5. ~~**Already-v2 review (13 mods):**~~ **ALL DONE** — auto-fixers resolved most, remainder graduated.
6. ~~**UMF bypass (14 converted):**~~ **ALL VIABLE MODS DONE** — 14 mods converted via bypass strategy. 5 UMF mods deferred (too complex for bypass).

## New Installs from Workshop Backlog (2026-03-21)

> ~34 mods installed from the ~75 pending workshop subscriptions. Most are maps/vehicles/content with no main.lua. 6 mods with scripts identified by QA Lead — all now lint clean after suppressions + fixes.

### New Mods with Scripts (6 — identified and resolved)

| Mod | Workshop ID | Type | Status |
|-----|------------|------|--------|
| Flying_Planes | 2423986361 | Vehicle/map (TDSU framework) | DEFERRED — 24,565 lines, TDSU framework dependency. 2 FPs suppressed. |
| Light_Saber | 3686903220 | Tool | Patched — fixed RAW-KEY-PLAYER + MOUSEDX bugs (T166). **Separate from Lightsaber (2547915810).** |
| MP_Hide_Multiplayer_Names | 3684710351 | Utility (mplib) | Suppressed — 6 mplib FPs. Mod works as-is. |
| Robot_Vehicles | 2673451391 | Vehicle (UMF) | DEFERRED — 20,805 lines, UMF framework dependency. 2 FPs suppressed. |
| SVERLOVSK_TOWN_2_Multiplayer | 3684105073 | Map | Fixed — tv.lua entity script converted to v2. |
| WIP_GYM_Ragdoll_Framework_MP | 3681634144 | Tool (framework) | Cleaned up — backup files removed. **Separate from GYM_Ragdoll (3668043935).** |

### Known Duplicate/Variant Pairs

| Installed (active) | Also installed as | Notes |
|-------------------|------------------|-------|
| Portal_Gun_MP (3659913820) | Portal_Gun (2421609769, our conversion) | MP fork from workshop vs our v2 conversion. Both may be present. |
| Thruster_Tool_Multiplayer (3625787751) | Thruster_Tool (2515871265, our conversion) | MP fork from workshop vs our v2 conversion. Fixed Issue #73 (hidden dynamic keybind bugs). |

### New Maps/Vehicles/Content (no main.lua — no patching needed)

AVF_Vehicles, Ability_to_read, Active_Volatile_Aviation, Advanced_Tornado, AndRe's_BMW_E36, Bikes_Ramps_&_Ragdolls_Collection, Bridge_Luancher_System, Bright_Valley_Correctional_Center, Centurion_C-RAM_Phalanx_CIWS, Colossus_Attack, Dynamic_AT-AT_Map, EVF_International_Emergency_Vehicles, Futuristic_Vehicle_pack, Geardown, Improved_Spawnable_Missile_&_Bomb_MP (3680249134, already v2), Kooshing's_Dynamic_Aircraft_Mod, Micro_Metropolis, Miniature_World_v1.1, Modern_Soldier_NPCs, New_York_mini, Public_Library, RPM_Modern_Military_Playermodels, Russian_Town_6_Summer_Multiplayer, STAR_WARS_AI_PACK, SW's_ADVANCED_GORE_MOD_2, Steve's_NPCS, The_World_Trade_Center, Vida_Hospital, gm_construct_MP, and others.
