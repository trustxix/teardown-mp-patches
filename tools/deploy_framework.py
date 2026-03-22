"""Deploy Trust Realism framework to mod directories with safety checks.

Copies lib/realistic_ballistics.lua to a mod's lib/ballistics.lua with:
- CRLF -> LF conversion (Teardown preprocessor fails on CRLF)
- Non-ASCII stripping (preprocessor fails on UTF-8 multibyte)
- Verification of the deployed file

Usage:
    python -m tools.deploy_framework --mod "Hook_Shotgun"
    python -m tools.deploy_framework --all          # deploy to all mods that have lib/ballistics.lua
    python -m tools.deploy_framework --fix-lua       # fix ALL .lua files in Documents/Teardown/mods/
"""
import os
import sys
import click
from pathlib import Path

FRAMEWORK_SRC = Path(__file__).parent.parent / "lib" / "realistic_ballistics.lua"
MODS_DIR = Path(r"C:\Users\trust\Documents\Teardown\mods")


def sanitize_lua(data: bytes) -> bytes:
    """Convert CRLF to LF and strip non-ASCII bytes from Lua source."""
    # CRLF -> LF
    data = data.replace(b"\r\n", b"\n")
    # Strip non-ASCII (replace with closest ASCII equivalent or space)
    result = bytearray()
    i = 0
    while i < len(data):
        b = data[i]
        if b <= 127:
            result.append(b)
            i += 1
        else:
            # UTF-8 multibyte: skip all continuation bytes
            if b >= 0xC0:
                # Em dash (e2 80 94) -> --
                if i + 2 < len(data) and data[i:i+3] == b"\xe2\x80\x94":
                    result.extend(b"--")
                    i += 3
                    continue
                # Degree symbol (c2 b0) -> deg
                if i + 1 < len(data) and data[i:i+2] == b"\xc2\xb0":
                    result.extend(b" deg")
                    i += 2
                    continue
                # Any other multibyte: skip
                if b < 0xE0:
                    i += 2
                elif b < 0xF0:
                    i += 3
                else:
                    i += 4
            else:
                i += 1
    return bytes(result)


def deploy_to_mod(mod_name: str) -> dict:
    """Deploy framework to a specific mod. Returns status dict."""
    mod_dir = MODS_DIR / mod_name
    if not mod_dir.exists():
        return {"mod": mod_name, "status": "not_found"}

    lib_dir = mod_dir / "lib"
    lib_dir.mkdir(exist_ok=True)
    dest = lib_dir / "ballistics.lua"

    with open(FRAMEWORK_SRC, "rb") as f:
        data = f.read()

    clean = sanitize_lua(data)

    with open(dest, "wb") as f:
        f.write(clean)

    # Verify
    crlf = clean.count(b"\r\n")
    non_ascii = len([b for b in clean if b > 127])

    return {
        "mod": mod_name,
        "status": "ok" if crlf == 0 and non_ascii == 0 else "warning",
        "crlf": crlf,
        "non_ascii": non_ascii,
        "bytes": len(clean),
    }


def fix_lua_file(path: Path) -> dict:
    """Fix CRLF and non-ASCII in any Lua file."""
    with open(path, "rb") as f:
        original = f.read()

    clean = sanitize_lua(original)

    if clean != original:
        with open(path, "wb") as f:
            f.write(clean)
        return {"path": str(path), "fixed": True, "removed_bytes": len(original) - len(clean)}
    return {"path": str(path), "fixed": False}


@click.command()
@click.option("--mod", help="Deploy to a specific mod")
@click.option("--all", "deploy_all", is_flag=True, help="Deploy to all mods that have lib/ballistics.lua")
@click.option("--fix-lua", "fix_all", is_flag=True, help="Fix CRLF/non-ASCII in ALL .lua files under Documents/Teardown/mods/")
def main(mod, deploy_all, fix_all):
    if not FRAMEWORK_SRC.exists():
        click.echo(f"Framework source not found: {FRAMEWORK_SRC}")
        sys.exit(1)

    if mod:
        result = deploy_to_mod(mod)
        click.echo(f"  {result['mod']}: {result['status']} ({result.get('bytes', 0)} bytes)")

    elif deploy_all:
        count = 0
        for mod_dir in sorted(MODS_DIR.iterdir()):
            if not mod_dir.is_dir():
                continue
            dest = mod_dir / "lib" / "ballistics.lua"
            if dest.exists():
                result = deploy_to_mod(mod_dir.name)
                click.echo(f"  {result['mod']}: {result['status']} ({result.get('bytes', 0)} bytes)")
                count += 1
        click.echo(f"\nDeployed to {count} mods")

    elif fix_all:
        fixed = 0
        total = 0
        for lua_file in MODS_DIR.rglob("*.lua"):
            total += 1
            result = fix_lua_file(lua_file)
            if result["fixed"]:
                fixed += 1
                click.echo(f"  Fixed: {lua_file.relative_to(MODS_DIR)} (-{result['removed_bytes']} bytes)")
        click.echo(f"\n{fixed}/{total} files fixed")

    else:
        click.echo("Usage: --mod NAME, --all, or --fix-lua")
        sys.exit(1)


if __name__ == "__main__":
    main()
