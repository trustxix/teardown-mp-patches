"""PostToolUse hook for Write/Edit -- auto-fix LF/ASCII and sync between dirs.

After any file in either mods dir is written or edited:
1. Convert CRLF to LF (Teardown preprocessor fails on CRLF)
2. Strip non-ASCII characters (preprocessor fails on UTF-8 multibyte)
3. Auto-copy the file to the OTHER mods directory (Documents <-> game install)

This keeps both directories in sync automatically.
"""
import sys
import json
import os
import shutil

DOCS_MODS = "C:/Users/trust/Documents/Teardown/mods/"
GAME_MODS = "C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/"


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
    fp_lower = fp.lower()

    # Determine which mods dir the edit is in
    in_docs = DOCS_MODS.lower() in fp_lower
    in_game = GAME_MODS.lower() in fp_lower

    if not in_docs and not in_game:
        sys.exit(0)

    # Fix LF/ASCII for .lua files
    if fp_lower.endswith(".lua"):
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            original = content

            # CRLF -> LF
            content = content.replace(b"\r\n", b"\n")

            # Strip non-ASCII
            cleaned = bytearray()
            for b in content:
                if b > 127:
                    cleaned.append(63)  # '?'
                else:
                    cleaned.append(b)
            content = bytes(cleaned)

            if content != original:
                with open(file_path, "wb") as f:
                    f.write(content)
                print(f"Auto-fixed LF/ASCII: {os.path.basename(file_path)}", file=sys.stderr)
        except Exception as e:
            print(f"LF/ASCII fix failed: {e}", file=sys.stderr)

    # Auto-sync to the other directory
    try:
        if in_docs:
            rel = fp[len(DOCS_MODS):]
            other_path = GAME_MODS + rel
        else:
            rel = fp[len(GAME_MODS):]
            other_path = DOCS_MODS + rel

        # Only sync if the other directory's mod folder exists
        other_dir = os.path.dirname(other_path)
        if os.path.isdir(other_dir):
            os.makedirs(os.path.dirname(other_path), exist_ok=True)
            shutil.copy2(file_path, other_path)
            direction = "docs->game" if in_docs else "game->docs"
            print(f"Auto-synced ({direction}): {os.path.basename(file_path)}", file=sys.stderr)
    except Exception as e:
        print(f"Auto-sync failed: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
