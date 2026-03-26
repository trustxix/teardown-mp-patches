"""PostToolUse hook for Write/Edit -- auto-fix LF/ASCII on Lua files.

After any .lua file in the working mods dir is written or edited:
1. Convert CRLF to LF (Teardown preprocessor fails on CRLF)
2. Strip non-ASCII characters (preprocessor fails on UTF-8 multibyte)
"""
import sys
import json
import os

WORKING_DIR = "D:/The Vault/Modding/Games/Teardown/"


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

    if WORKING_DIR.lower() not in fp_lower:
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

    sys.exit(0)  # PostToolUse — never block

if __name__ == "__main__":
    main()
