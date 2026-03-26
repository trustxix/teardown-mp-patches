"""PostToolUse hook for Edit/Write -- auto-runs lint after Lua edits.

After any .lua file in the working mods dir is edited, automatically
runs `python -m tools.lint --mod "ModName"` and prints results.
"""
import sys
import json
import subprocess
import os

PROJECT_DIR = "C:/Users/trust/teardown-mp-patches"
MODS_DIR = "D:/The Vault/Modding/Games/Teardown/"

def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    fp = file_path.replace("\\", "/")

    # Only lint .lua files in the mods directory
    if not fp.lower().endswith(".lua"):
        sys.exit(0)
    if MODS_DIR.lower() not in fp.lower():
        sys.exit(0)

    # Extract mod name from path: .../mods/MOD_NAME/...
    rel = fp[len(MODS_DIR):]
    mod_name = rel.split("/")[0]
    if not mod_name:
        sys.exit(0)

    # Run lint
    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.lint", "--mod", mod_name],
            capture_output=True, text=True, timeout=30,
            cwd=PROJECT_DIR
        )
        output = result.stdout.strip()
        if output:
            # Only print if there are findings (not just "1 mods scanned: 1 clean")
            if "0 total findings" not in output:
                print(f"\n[auto-lint] {mod_name}:", file=sys.stderr)
                print(output, file=sys.stderr)
            else:
                print(f"[auto-lint] {mod_name}: clean", file=sys.stderr)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"[auto-lint] Failed to lint {mod_name}: {e}", file=sys.stderr)

    sys.exit(0)  # PostToolUse — never block

if __name__ == "__main__":
    main()
