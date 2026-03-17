# Team Collaboration Protocol

## Core Principle
All 3 terminals work on the SAME focus area simultaneously, each contributing from their expertise. QA Lead picks the focus area, the team brainstorms the approach, then everyone executes in parallel.

## Focus Areas
QA Lead maintains a file `.comms/FOCUS.md` that declares the current team focus. ALL terminals read this before starting work. When the focus changes, QA Lead broadcasts.

## Work Cycle

```
1. QA Lead sets FOCUS.md (e.g., "Options menu polish for gun mods")
2. QA Lead broadcasts a brainstorm request to both inboxes
3. All 3 terminals contribute ideas/analysis to QA Lead's inbox
4. QA Lead reads all input, makes decisions, creates tasks
5. QA Lead sends tasks to each terminal's inbox (same focus area, different mods/aspects)
6. All 3 work in parallel on the same focus area
7. Each terminal sends results to QA Lead on completion
8. QA Lead reviews, identifies next focus area
9. GOTO 1
```

## Brainstorming Protocol

When QA Lead sends a `brainstorm` type message:
1. Read the question/topic carefully
2. Analyze the codebase for relevant patterns
3. Send your analysis back to QA Lead's inbox as type `result`
4. Include: what you found, your recommendation, trade-offs, estimated effort
5. Wait for QA Lead's decision before starting work

## Inbox Checking Rules

**Check your inbox:**
- BEFORE starting any new task
- AFTER completing any task
- AFTER every 3-4 tool calls during a long task (quick `has_mail` check)
- When you notice files changed by another terminal

**React immediately to:**
- `priority: critical` messages — drop current work
- `priority: high` messages — finish current step, then switch
- `brainstorm` messages — respond before doing other work

## Focus Area Examples

```markdown
# Current Focus: Options Menu Polish
All terminals work on options menus this cycle.
- API Surgeon: add UiMakeInteractive to existing menus, fix button layouts
- Mod Converter: add keybind hint text with O - Options to all mods
- QA Lead: review menus, test savegame persistence, update docs
```

```markdown
# Current Focus: Gun Mod Damage System
All terminals work on player damage this cycle.
- API Surgeon: migrate MakeHole → Shoot/QueryShot for bullet mods
- Mod Converter: add kill attribution toolId strings to all weapons
- QA Lead: verify damage values, test PvP, document patterns
```

## Conflict Prevention
- QA Lead assigns SPECIFIC mods to each terminal — never the same mod to two terminals
- If you need to edit a mod assigned to someone else, send them a message instead
- QA Lead resolves all conflicts

## Team Autonomy Rules

Every terminal can:
- **Fix bugs** they find in any mod, even if not assigned — fix it, log it, notify docs_keeper
- **Create tasks** for any role when they spot work that needs doing
- **Reject tasks** with explanation if analysis shows they're unnecessary
- **Split tasks** into subtasks if they're too large
- **Help other terminals** by sending fixes/solutions to their inbox
- **Propose workflow improvements** to QA Lead
- **Improve tools** (lint rules, auto-fixes) when they find repeating patterns

No terminal should ever be idle. If your queue is empty:
1. Check inbox — maybe someone needs help
2. Run lint/audit — find new work
3. Read other terminals' outboxes — catch undocumented work
4. Create your own tasks from findings
5. Propose ideas to QA Lead

## Continuous Improvement

The team improves itself over time:
- **New bug pattern?** → API Surgeon adds a lint rule, Docs Keeper logs it
- **Repetitive manual work?** → Anyone proposes an auto-fix to QA Lead
- **Communication gap?** → QA Lead updates TRIGGERS.md or adds a hook
- **Missing capability?** → QA Lead builds a new MCP tool or skill
- **Role confusion?** → QA Lead updates the role file to clarify
