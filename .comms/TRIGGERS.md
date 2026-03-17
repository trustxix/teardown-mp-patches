# When to Message Other Terminals

## API Surgeon → QA Lead inbox
- **After editing any mod:** Send `result` with mod name, what changed, lint output
- **After hitting a bug you can't fix:** Send `question` with error details, what you tried
- **After finding work that's not your role:** Send `info` describing what you found

## Mod Converter → QA Lead inbox
- **After converting a new mod:** Send `result` with mod name, workshop ID, lint output
- **After adding keybind hints or polish:** Send `result` with mod name, what was added
- **After hitting a structural issue:** Send `question` with details

## QA Lead → API Surgeon inbox
- **When new API migration work is found:** Send `task` with mod names, what to fix, priority
- **When reviewing their work and finding issues:** Send `review` with mod name, what's wrong, how to fix
- **When approving their work:** Send `info` with confirmation

## QA Lead → Mod Converter inbox
- **When new conversion/polish work is found:** Send `task` with mod names, what to do, priority
- **When reviewing their work and finding issues:** Send `review` with mod name, what's wrong
- **When approving their work:** Send `info` with confirmation

## QA Lead → Both (broadcast)
- **After updating CLAUDE.md rules:** Broadcast `info` so they pick up new rules
- **After discovering a new bug pattern:** Broadcast `info` with the pattern to avoid
- **When reprioritizing work:** Broadcast `info` with new priorities

## API Surgeon → Docs Keeper inbox
- **After fixing a bug:** Send `result` with mod name, what the bug was, how you fixed it, the rule to add
- **After discovering a new API pattern:** Send `result` with the pattern details for RESEARCH.md

## Mod Converter → Docs Keeper inbox
- **After converting a new mod:** Send `result` with mod name, workshop ID, batch number
- **After fixing a bug during conversion:** Send `result` with bug details and fix

## QA Lead → Docs Keeper inbox
- **After adding a new rule to the workflow:** Send `info` with the rule for CLAUDE.md
- **After a focus area completes:** Send `info` summarizing what was accomplished
- **After reviewing and approving work:** Send `result` with what was approved for the issue log

## Docs Keeper → QA Lead inbox
- **After updating docs:** Send `info` confirming what was updated
- **When doc drift is detected:** Send `question` asking for clarification
- **When CLAUDE.md rules conflict or are outdated:** Send `question` with details

## Anyone → Anyone
- **When you complete ALL your tasks and inbox is empty:** Send `info` to QA Lead saying "queue empty, awaiting work"
- **When you notice a file conflict (another terminal edited same file):** Send `question` to QA Lead to resolve

## DO NOT message for:
- Routine lint passes (just log in complete_task summary)
- Asking what to do next (use get_task instead)
- Status updates with no actionable info
