"""Phase 1: Ingest mods from Steam Workshop folder."""

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


def parse_info_txt(info_path: Path) -> dict:
    """Parse a Teardown info.txt into a dict."""
    data = {}
    for line in info_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line:
            key, _, value = line.partition("=")
            data[key.strip()] = value.strip()
    return data


def is_already_v2(mod_dir: Path) -> bool:
    """Check if a mod is already version 2."""
    info_path = mod_dir / "info.txt"
    if info_path.exists():
        info = parse_info_txt(info_path)
        if info.get("version") == "2":
            return True
    return False


def _hash_directory(dir_path: Path) -> str:
    """SHA-256 hash of all file contents in a directory."""
    h = hashlib.sha256()
    for f in sorted(dir_path.rglob("*")):
        if f.is_file():
            h.update(f.read_bytes())
    return h.hexdigest()


def _find_lua_files(mod_dir: Path) -> list[str]:
    """List all .lua files relative to mod root."""
    return [str(f.relative_to(mod_dir)) for f in mod_dir.rglob("*.lua")]


def ingest_mod(
    mod_dir: Path, output_dir: Path, workshop_id: str
) -> dict | None:
    """Ingest a single mod. Returns metadata dict or None if skipped."""
    if is_already_v2(mod_dir):
        return None

    info = parse_info_txt(mod_dir / "info.txt")
    mod_output = output_dir / workshop_id
    original_dir = mod_output / "original"

    # Copy original files
    if original_dir.exists():
        shutil.rmtree(original_dir)
    shutil.copytree(mod_dir, original_dir)

    # Build metadata
    metadata = {
        "workshop_id": workshop_id,
        "name": info.get("name", "Unknown"),
        "author": info.get("author", "Unknown"),
        "description": info.get("description", ""),
        "tags": info.get("tags", ""),
        "lua_files": _find_lua_files(mod_dir),
        "sha256": _hash_directory(mod_dir),
        "status": "pending",
        "manual_edits": False,
        "patch_version": "1.0",
        "ingested_at": datetime.now().isoformat(),
    }

    (mod_output / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    return metadata


def ingest_batch(workshop_dir: Path, output_dir: Path) -> list[dict | None]:
    """Ingest all mods in a Workshop content directory."""
    results = []
    for sub in sorted(workshop_dir.iterdir()):
        if sub.is_dir() and (sub / "info.txt").exists():
            workshop_id = sub.name
            result = ingest_mod(sub, output_dir, workshop_id)
            results.append(result)
    return results
