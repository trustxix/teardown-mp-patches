# Plugins & Agents Available to the Team

> You have access to powerful plugins via the `Agent` tool and `Skill` tool.
> **USE THEM.** Don't do manually what a plugin can do better.

---

## When to Use What — Quick Decision Table

| You're about to... | Use this |
|---------------------|----------|
| Fix a bug or test failure | `Skill: superpowers:systematic-debugging` |
| Write or fix tests | Agent: `test-writer-fixer:test-writer-fixer` |
| Review code you just wrote | Agent: `superpowers:code-reviewer` or `feature-dev:code-reviewer` |
| Simplify messy code | Agent: `code-simplifier:code-simplifier` |
| Plan a multi-step change | `Skill: superpowers:writing-plans` then `Skill: superpowers:executing-plans` |
| Run 2+ independent tasks | `Skill: superpowers:dispatching-parallel-agents` |
| Claim work is "done" | `Skill: superpowers:verification-before-completion` |
| Deep-dive a codebase area | Agent: `feature-dev:code-explorer` |
| Design a new feature | Agent: `feature-dev:code-architect` |
| Find similar code patterns | Agent: `agent-codebase-pattern-finder:codebase-pattern-finder` |
| Debug with structured method | Agent: `debugger:debugger` |
| Search for files/code | Agent: `Explore` (subagent_type) |
| Look up official Teardown API | Read `docs/OFFICIAL_DEVELOPER_DOCS.md` first, then `WebFetch` the API page |

---

## Tier 1 — Use These Constantly

### Systematic Debugging
**Skill:** `superpowers:systematic-debugging`
**When:** Any bug, test failure, or unexpected behavior. BEFORE guessing at fixes.
**Why:** Forces root-cause analysis instead of shotgun debugging.
**Team use:** When a mod crashes in-game, when lint finds something unexpected, when `tools.logparse` shows errors.

### Verification Before Completion
**Skill:** `superpowers:verification-before-completion`
**When:** About to mark a task done, claim a fix works, or complete a mod conversion.
**Why:** Catches things you missed. Runs through a checklist.
**Team use:** Before `complete_task()`. Before telling QA Lead "mod X is done."

### Dispatching Parallel Agents
**Skill:** `superpowers:dispatching-parallel-agents`
**When:** 2+ independent tasks that don't share state.
**Why:** Run them simultaneously instead of sequentially.
**Team use:** Fix lint warnings across multiple mods at once. Run audit + lint + logparse in parallel.

### Code Review
**Agent:** `superpowers:code-reviewer` or `feature-dev:code-reviewer`
**When:** After completing a mod conversion or fixing a batch of mods.
**Why:** Catches bugs, style issues, and patterns you missed.
**Team use:** QA Lead should dispatch this after reviewing a batch of changes.

### Code Simplifier
**Agent:** `code-simplifier:code-simplifier` or `pr-review-toolkit:code-simplifier`
**When:** After writing or modifying code.
**Why:** Simplifies for clarity and maintainability while preserving functionality.
**Team use:** After a mod conversion, run this on the main.lua to clean it up.

---

## Tier 2 — Use for Specific Situations

### Test Writer/Fixer
**Agent:** `test-writer-fixer:test-writer-fixer`
**When:** Need to write tests for a new lint rule, fix, or tool feature.
**Why:** Generates comprehensive test cases automatically.
**Team use:** After adding a lint check to `tools/lint.py`, dispatch this to generate tests.

### Code Explorer
**Agent:** `feature-dev:code-explorer`
**When:** Need to understand how something works across multiple files.
**Why:** Traces execution paths, maps architecture layers, documents dependencies.
**Team use:** Understanding a complex mod before converting it. Tracing how the MCP server routes messages.

### Code Architect
**Agent:** `feature-dev:code-architect`
**When:** Designing a new tool, lint rule, or infrastructure change.
**Why:** Analyzes existing patterns, provides implementation blueprints.
**Team use:** Before building a new `tools/*.py` command or MCP tool.

### Pattern Finder
**Agent:** `agent-codebase-pattern-finder:codebase-pattern-finder`
**When:** Looking for similar implementations or usage examples.
**Why:** Finds concrete code examples based on what you're looking for.
**Team use:** "Show me all mods that use ServerCall in tickPlayer" or "find all registry sync patterns."

### Debugger
**Agent:** `debugger:debugger`
**When:** Stuck on a specific error or failure.
**Why:** Specialized debugging with Read, Edit, Bash, Grep, Glob.
**Team use:** When `tools.logparse` shows a mod error and you can't figure out why.

### Writing Plans
**Skill:** `superpowers:writing-plans`
**When:** Multi-step task that needs a plan before coding.
**Why:** Creates structured implementation plans.
**Team use:** Before converting a complex mod (500+ lines). Before refactoring a tool.

### Executing Plans
**Skill:** `superpowers:executing-plans`
**When:** Have a written plan to execute.
**Why:** Step-by-step execution with review gates.
**Team use:** After writing a plan for a batch conversion.

---

## Tier 3 — Specialized (Use When Relevant)

| Agent | When |
|-------|------|
| `agents-language-specialists:python-expert` | Improving tools/*.py, writing complex Python |
| `agents-quality-security:test-automator` | Setting up new test infrastructure |
| `agents-quality-security:performance-engineer` | Optimizing tool performance (lint/audit speed) |
| `experienced-engineer:code-quality-reviewer` | Deep code quality review |
| `experienced-engineer:testing-specialist` | Test strategy and coverage |
| `agents-quality-security:security-auditor` | If mods handle user input or network data |
| `coderabbit:code-reviewer` | Thorough CodeRabbit-style code review |

---

## Skills the Team Should Know

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `superpowers:brainstorming` | Before any creative work | Structured brainstorming before building |
| `superpowers:systematic-debugging` | Any bug or failure | Root-cause analysis workflow |
| `superpowers:verification-before-completion` | Before claiming "done" | Final verification checklist |
| `superpowers:dispatching-parallel-agents` | 2+ independent tasks | Run agents in parallel |
| `superpowers:writing-plans` | Multi-step task | Create implementation plan |
| `superpowers:executing-plans` | Have a plan | Execute with review gates |
| `superpowers:test-driven-development` | Implementing new features | TDD workflow |
| `simplify` | After writing code | Review for reuse, quality, efficiency |

---

## How to Use Agents

```
# In your work loop, dispatch agents with the Agent tool:

Agent(
    subagent_type="feature-dev:code-reviewer",
    description="Review mod conversion",
    prompt="Review C:/Users/trust/Documents/Teardown/mods/MyMod/main.lua for v2 MP compliance against CLAUDE.md rules..."
)

# Or invoke skills:
Skill(skill="superpowers:systematic-debugging")
```

## Anti-Patterns — Don't Do These

- **Don't manually debug** when `superpowers:systematic-debugging` exists
- **Don't claim "done"** without `superpowers:verification-before-completion`
- **Don't review your own code** without dispatching a code-reviewer agent
- **Don't do 5 tasks sequentially** when they could run as parallel agents
- **Don't write tests manually** when `test-writer-fixer` can generate them
- **Don't guess at patterns** when `codebase-pattern-finder` can search for you
