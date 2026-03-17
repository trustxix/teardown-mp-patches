"""Parse Teardown log.txt and extract mod errors grouped by mod name."""

import re
from collections import defaultdict

import click

from tools.common import LOG_PATH

# [string "...path.../mods/MOD_NAME/FILE"]:LINE: MESSAGE
_RUNTIME_RE = re.compile(
    r'\[string ".*?[/\\]mods[/\\]([^/\\]+)[/\\]([^"]+)"\]:(\d+):\s*(.+)'
)

# Error compiling: ...path.../mods/MOD_NAME/FILE
_COMPILE_RE = re.compile(
    r"Error compiling:\s*.*?[/\\]mods[/\\]([^/\\]+)[/\\](.+)"
)

# Teardown 2.0.0 (20260315)
_VERSION_RE = re.compile(r"Teardown\s+([\d.]+)")


def parse_log(content: str) -> dict:
    """Parse Teardown log content and return errors grouped by mod name.

    Returns:
        {
            "version": "2.0.0",
            "mods": {
                "ModName": [
                    {"file": "main.lua", "line": 45, "type": "runtime", "message": "..."},
                ],
            }
        }
    """
    version = "unknown"
    mods: dict[str, list] = defaultdict(list)

    for line in content.splitlines():
        # Extract version from first matching line
        if version == "unknown":
            m = _VERSION_RE.search(line)
            if m:
                version = m.group(1)

        # Runtime error
        m = _RUNTIME_RE.search(line)
        if m:
            mod_name, file_path, line_no, message = m.group(1), m.group(2), m.group(3), m.group(4)
            mods[mod_name].append({
                "file": file_path,
                "line": int(line_no),
                "type": "runtime",
                "message": message.strip(),
            })
            continue

        # Compile error
        m = _COMPILE_RE.search(line)
        if m:
            mod_name, file_path = m.group(1), m.group(2)
            mods[mod_name].append({
                "file": file_path,
                "line": 0,
                "type": "compile",
                "message": "Error compiling",
            })

    return {"version": version, "mods": dict(mods)}


@click.command("logparse")
@click.option("--mod", "mod_name", default=None, help="Filter to single mod")
@click.option("--raw", is_flag=True, help="Show full error lines")
def logparse_cli(mod_name, raw):
    """Parse Teardown log for mod errors."""
    if not LOG_PATH.exists():
        click.echo(f"Log not found: {LOG_PATH}")
        raise SystemExit(1)

    content = LOG_PATH.read_text(encoding="utf-8", errors="replace")
    result = parse_log(content)

    click.echo(f"Teardown {result['version']}")
    click.echo("-" * 40)

    mods = result["mods"]
    if mod_name:
        mods = {k: v for k, v in mods.items() if k == mod_name}

    if not mods:
        click.echo("No errors found" + (f" for {mod_name}" if mod_name else ""))
        return

    total_errors = 0
    for name, errors in sorted(mods.items()):
        click.echo(f"\n{name}/")
        for err in errors:
            total_errors += 1
            if err["type"] == "runtime":
                click.echo(f"  line {err['line']}: {err['type']} - {err['message']}")
            else:
                click.echo(f"  {err['file']}: {err['type']} - {err['message']}")

    click.echo(f"\n{len(mods)} mod(s) with errors, {total_errors} total errors")


if __name__ == "__main__":
    logparse_cli()
