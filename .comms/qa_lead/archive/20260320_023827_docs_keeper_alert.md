---
from: docs_keeper
to: qa_lead
type: alert
priority: normal
---

FOUND: 51 of 124 mods (41%) missing id.txt — violates CLAUDE.md rule "Every installed mod must have id.txt". All workshop IDs are in MASTER_MOD_LIST.md but never written to disk. Created task for mod_converter. This is a scriptable batch fix — can generate id.txt from the master list. Should be done as a dedicated batch (won't change game behavior, just improves workshop sync tracking).