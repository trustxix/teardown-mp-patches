# Current Team Focus

## Focus: Final Polish Sprint + Milestone Commit
**Set by:** QA Lead
**Date:** 2026-03-18

### Previous Sprint: COMPLETE
PER-TICK-RPC sprint finished: **69 warnings → 0**. CLIENT-SERVER-FUNC: **3 warnings → 0**.
All tier-1 errors: 0. All tier-2 warnings: 0. 102 mods installed, all passing.

### Required Reading (Every Terminal On Boot)
1. **`docs/OFFICIAL_DEVELOPER_DOCS.md`** — GROUND TRUTH from teardowngame.com. Highest authority.
2. **`docs/TEAM_PLUGINS.md`** — All plugins, agents, skills. USE THEM.

### MANDATORY Plugin Usage Rules
- **Bug or test failure?** → `Skill: superpowers:systematic-debugging` BEFORE guessing
- **Marking a task done?** → `Skill: superpowers:verification-before-completion` FIRST
- **2+ independent tasks?** → `Skill: superpowers:dispatching-parallel-agents`
- **Just wrote code?** → Dispatch `code-simplifier:code-simplifier` or `feature-dev:code-reviewer`

### Current State
102 mods installed. **0 tier-1 errors. 0 tier-2 warnings.** 52 info-level findings (18 MAKEHOLE-DAMAGE + 32 MANUAL-AIM + 2 other). 24 lint checks. 309+ tests.

**3,452 uncommitted insertions across 24 files.** Commit needed after polish tasks complete.

### Priority Work

1. **HIGH: 3 gun mods missing polish features**
   - **Jackhammer** — Missing: OptionsMenu, OptionsGuard, KeybindHints
   - **Tripmine** — Missing: OptionsMenu, OptionsGuard
   - **Shape_Collapsor** — Missing: AmmoDisplay

2. **MEDIUM: Commit milestone** — Once polish tasks land, commit everything:
   `"feat: 102 mods, 0 errors/warnings, PER-TICK-RPC sprint complete, 24 lint rules"`

3. **LOW: Info findings triage** — 52 info-level findings. Most are intentional (projectile weapons using QueryRaycast, terrain tools using MakeHole). Case-by-case review, suppress with `@lint-ok` where appropriate.

4. **LOW: Docs consistency** — Docs Keeper fixing API signature inconsistencies in OFFICIAL_DEVELOPER_DOCS.md.

### Assignments
- **API Surgeon:** Fix Jackhammer (add OptionsMenu, OptionsGuard, KeybindHints). Then fix Shape_Collapsor (add AmmoDisplay).
- **Mod Converter:** Fix Tripmine (add OptionsMenu, OptionsGuard). Then review info-level findings for mods you converted — add `@lint-ok` where findings are intentional.
- **Docs Keeper:** Continue fixing API signature discrepancies in OFFICIAL_DEVELOPER_DOCS.md. Update MASTER_MOD_LIST to 102 mods. Prepare commit message.
- **QA Lead:** Review polish fixes. Run lint after each. Triage info-level findings. Approve commit.
