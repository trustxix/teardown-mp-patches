"""PreToolUse hook — warns if editing a mod file that might be locked by another terminal.
Checks .comms/locks.json for active locks. Lightweight — only runs for Edit/Write tools."""

import json
import os
import sys
import time

LOCKS_FILE = os.path.join(os.path.dirname(__file__), "locks.json")
EXPIRY_SECONDS = 300  # 5 minutes

def check():
    # Read the tool input from stdin (Claude Code passes it as JSON)
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool = input_data.get("tool_name", "")
    if tool not in ("Edit", "Write"):
        return

    filepath = input_data.get("tool_input", {}).get("file_path", "")
    if not filepath or "Teardown/mods/" not in filepath.replace("\\", "/"):
        return

    if not os.path.exists(LOCKS_FILE):
        return

    try:
        with open(LOCKS_FILE, "r") as f:
            locks = json.load(f)
    except (json.JSONDecodeError, IOError):
        return

    # Normalize path for comparison
    norm = filepath.replace("\\", "/").lower()
    now = time.time()

    for locked_path, info in locks.items():
        locked_norm = locked_path.replace("\\", "/").lower()
        if norm == locked_norm:
            age = now - info.get("timestamp", 0)
            if age < EXPIRY_SECONDS:
                holder = info.get("role", "unknown")
                print(f"WARNING: {os.path.basename(filepath)} is locked by {holder} ({int(age)}s ago). Coordinate before editing.")
            return

if __name__ == "__main__":
    check()
