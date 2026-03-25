"""PreToolUse guard for Edit/Write -- blocks dangerous operations.

Checks (in order):
1. Wrong directory: editing in patches repo mods/ instead of game install mods dir
2. Asset protection: editing .vox/.xml/.png/.ogg/.jpg files in mod directories
3. Game running: editing mod files while teardown.exe is running
"""
import sys
import json
import subprocess
import os

def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)  # can't parse input, allow

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Normalize path separators
    fp = file_path.replace("\\", "/").lower()

    # --- Check 1: Wrong directory ---
    if "teardown-mp-patches/mods/" in fp:
        print("BLOCKED: Wrong directory!", file=sys.stderr)
        print("  You're editing the patches REPO, not the live mods folder.", file=sys.stderr)
        print("  Edit in: C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/", file=sys.stderr)
        print("  NOT in:  C:/Users/trust/teardown-mp-patches/mods/", file=sys.stderr)
        sys.exit(1)

    # --- Check 2: Asset file protection ---
    mod_dirs = [
        "steam/steamapps/common/teardown/mods/",
        "teardown-mp-patches/mods/",
    ]
    is_in_mod_dir = any(d in fp for d in mod_dirs)
    asset_exts = (".vox", ".xml", ".png", ".ogg", ".jpg", ".jpeg")
    if is_in_mod_dir and fp.endswith(asset_exts):
        # Allow info.txt-adjacent .xml only if it's clearly not a prefab
        # But block all asset files — only .lua and info.txt should be edited
        print("BLOCKED: Asset files must not be modified!", file=sys.stderr)
        print(f"  File: {file_path}", file=sys.stderr)
        print("  Only .lua scripts and info.txt can be edited in mod directories.", file=sys.stderr)
        print("  Modifying asset files (.vox, .xml, .png, .ogg) has caused game crashes.", file=sys.stderr)
        sys.exit(1)

    # --- Check 3: Game running ---
    if "documents/teardown/mods/" in fp:
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq teardown.exe", "/NH"],
                capture_output=True, text=True, timeout=5
            )
            if "teardown.exe" in result.stdout.lower():
                print("BLOCKED: Teardown is running!", file=sys.stderr)
                print("  Close the game before editing mod files.", file=sys.stderr)
                print("  Editing files mid-session can corrupt game state.", file=sys.stderr)
                sys.exit(1)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass  # can't check, allow

    sys.exit(0)

if __name__ == "__main__":
    main()
