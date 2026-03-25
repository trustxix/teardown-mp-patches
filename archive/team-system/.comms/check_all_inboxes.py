"""PostToolUse hook — checks killswitch and all inboxes. Only prints if action needed."""
import glob
import os

COMMS = os.path.join(os.path.dirname(__file__))

# Check killswitch FIRST
stop_file = os.path.join(COMMS, "STOP")
if os.path.exists(stop_file):
    print("*** KILLSWITCH ACTIVE — Finish current task and HALT. Do not pick up new work. ***")

# Check inboxes
ROLES = ["qa_lead", "api_surgeon", "mod_converter", "docs_keeper"]
# Dynamically add any other role directories
for d in os.listdir(COMMS):
    full = os.path.join(COMMS, d, "inbox")
    if os.path.isdir(full) and d not in ROLES and d != "__pycache__":
        ROLES.append(d)

alerts = []
for role in ROLES:
    inbox = os.path.join(COMMS, role, "inbox", "*.md")
    files = glob.glob(inbox)
    count = len(files)
    if count > 0:
        critical = 0
        has_stop = False
        for f in files:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                header = fh.read(300)
                if "priority: critical" in header or "priority: high" in header:
                    critical += 1
                if "STOP ORDER" in header:
                    has_stop = True
        if has_stop:
            alerts.append(f"*** STOP ORDER in [{role}] inbox — HALT after current task ***")
        elif critical:
            alerts.append(f"URGENT MAIL [{role}]: {count} message(s), {critical} high/critical!")
        else:
            alerts.append(f"MAIL [{role}]: {count} message(s)")

if alerts:
    print("\n".join(alerts))
