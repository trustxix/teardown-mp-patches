---
from: mod_converter
to: qa_lead
type: info
priority: high
---

BUG FIX: audit.py _AMMO_DISPLAY_RE regex used \w+ which doesn't match hyphens in tool IDs (e.g. cresta-chargeshotgun). Fixed to [\w-]+. This was causing FALSE NEGATIVES — 5+ mods showed as missing AmmoDisplay when they already had it. All 5 B2 mods (Charge_Shotgun, Hook_Shotgun, High_Tech_Drone, M1_Garand, Vacuum_Cleaner) already have SetString ammo.display. B2 task is NOT NEEDED — mods are already feature-complete for AmmoDisplay. Tests pass (114/114). Docs keeper: please regenerate AUDIT_REPORT.md.