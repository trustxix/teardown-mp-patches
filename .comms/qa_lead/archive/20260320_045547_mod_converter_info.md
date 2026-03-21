---
from: mod_converter
to: qa_lead
type: info
priority: high
---

SAFETY FINDING: 103 mods have preview.jpg/preview.png in their local folders (Documents/Teardown/mods/).

Per Issue #66 and CLAUDE.md, these should NOT exist — they can trigger strncpy buffer overflow during mod enumeration. We're currently at 125 mods (below the ~178 crash threshold), but if the user installs more from the ~75 pending workshop subs, this becomes dangerous.

The engine handles workshop previews through Steam — local copies are unnecessary. Removing them is safe and prevents a known crash vector.

PROPOSAL: Batch-remove preview images in groups of 3 mod folders per batch to comply with batch rules. This is 35 batches but each takes seconds (just `rm` commands, no code changes). Or — since this is deleting unnecessary files (not editing code), consider requesting user approval for a mass removal as a one-time safety fix.

Awaiting your call on approach.