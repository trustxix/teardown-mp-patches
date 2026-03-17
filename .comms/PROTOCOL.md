# Inter-Terminal Communication Protocol

## Folder Structure
```
.comms/
  qa_lead/inbox/        ← QA Lead reads from here
  qa_lead/outbox/       ← QA Lead's sent messages (log)
  api_surgeon/inbox/    ← API Surgeon reads from here
  api_surgeon/outbox/   ← API Surgeon's sent messages (log)
  mod_converter/inbox/  ← Mod Converter reads from here
  mod_converter/outbox/ ← Mod Converter's sent messages (log)
```

## Message Format

Files are named: `{timestamp}_{from}_{type}.md`
Example: `20260317_143022_qa_lead_task.md`

```markdown
---
from: qa_lead
to: api_surgeon
type: task | question | review | info | result
priority: critical | high | medium | low
re: (optional — reference to a previous message filename)
---

[message content]
```

## Message Types

| Type | Purpose | Expected Response |
|------|---------|-------------------|
| task | Work assignment | result message when done |
| question | Need input/decision | info or result message |
| review | Review this work | info message with approval/notes |
| info | FYI, no action needed | none |
| result | Task output/completion | review message (from QA) |
| brainstorm | QA wants team input on a decision | result message with your analysis |

### Brainstorm Messages
When you receive a `brainstorm` message from QA Lead:
1. STOP current work after finishing your current step
2. Read the topic carefully
3. Analyze the codebase for relevant context
4. Send your recommendations to QA Lead's inbox as type `result`
5. Include: what you found, your recommendation, trade-offs, estimated effort
6. Resume normal work while waiting for QA Lead's decision

## Terminal Loop

Every terminal follows this loop after each task:

1. Check your inbox: `ls .comms/{your_role}/inbox/`
2. Process messages oldest-first (sort by filename = chronological)
3. Delete processed messages from inbox
4. Do the work
5. Write results to the sender's inbox (or broadcast)
6. Check for more inbox messages
7. If inbox empty, check task queue via MCP `get_task()`
8. If no tasks, run `python -m tools.lint` to find work, create tasks
9. Repeat forever

## Sending Messages

To send to another terminal:
1. Write the message file to `.comms/{recipient}/inbox/`
2. Copy to your own `.comms/{your_role}/outbox/` for logging

## Broadcasting

Write the same message to all inboxes (except your own).

## Conventions

- Always process inbox before checking task queue
- Include enough context in messages that the recipient doesn't need to ask questions
- For task results, include: what was done, which files changed, lint output
- For review requests, include: mod names, what to verify
- Delete inbox messages after processing (keeps inbox clean)
- Outbox is append-only log (never delete)
