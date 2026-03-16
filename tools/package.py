"""Phase 5: Package patched mods for distribution."""

import json
import zipfile
from difflib import unified_diff
from pathlib import Path


def generate_migration_md(original: str, patched: str, filename: str) -> str:
    """Generate a migration document showing changes."""
    diff = list(unified_diff(
        original.splitlines(keepends=True),
        patched.splitlines(keepends=True),
        fromfile=f"original/{filename}",
        tofile=f"patched/{filename}",
    ))
    diff_text = "".join(diff) if diff else "(no changes)"

    return f"""# Migration Report: {filename}

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
{diff_text}
```
"""


def package_mod(mod_dir: Path) -> dict:
    """Package a patched mod into a release-ready zip."""
    metadata = json.loads((mod_dir / "metadata.json").read_text())
    patched_dir = mod_dir / "patched"
    original_dir = mod_dir / "original"
    mod_name = metadata["name"].replace(" ", "_")
    workshop_id = metadata["workshop_id"]

    # Generate migration docs
    migration_parts = []
    for lua_file in sorted(patched_dir.rglob("*.lua")):
        rel = str(lua_file.relative_to(patched_dir))
        original_file = original_dir / rel
        orig_text = original_file.read_text(encoding="utf-8") if original_file.exists() else ""
        patch_text = lua_file.read_text(encoding="utf-8")
        migration_parts.append(generate_migration_md(orig_text, patch_text, rel))

    migration_md = "\n---\n\n".join(migration_parts)
    migration_path = mod_dir / "migration.md"
    migration_path.write_text(migration_md, encoding="utf-8")

    # Create zip
    zip_name = f"{mod_name}-mp-patch-v{metadata.get('patch_version', '1.0')}.zip"
    zip_path = mod_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(patched_dir.rglob("*")):
            if f.is_file():
                arc_name = f"{mod_name}/{f.relative_to(patched_dir)}"
                zf.write(f, arc_name)

    # Update metadata
    metadata["status"] = "packaged"
    (mod_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

    return {"zip_path": zip_path, "migration_md": migration_path}
