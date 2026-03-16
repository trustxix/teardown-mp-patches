"""Generate README dashboard from mod metadata."""

import json
from pathlib import Path

HEADER = """# Teardown MP Patches

Unofficial multiplayer compatibility patches for Teardown Steam Workshop mods.

> **Note:** These are community patches. Please subscribe to the original mods on the Steam Workshop to support the original authors.

## Status Dashboard

| Mod | Author | Type | Complexity | Status | Workshop | Download |
|-----|--------|------|------------|--------|----------|----------|
"""

STATUS_EMOJI = {
    "pending": "⏳ Pending",
    "analyzed": "🔍 Analyzed",
    "rewrite_failed": "❌ Rewrite Failed",
    "validation_failed": "⚠️ Validation Failed",
    "patched": "✅ Patched",
    "packaged": "📦 Packaged",
    "released": "🚀 Released",
}


def generate_dashboard(mods_dir: Path) -> str:
    """Generate README.md content from all mod metadata."""
    rows = []

    for mod_dir in sorted(mods_dir.iterdir()):
        meta_path = mod_dir / "metadata.json"
        if not meta_path.exists():
            continue

        meta = json.loads(meta_path.read_text())
        analysis_path = mod_dir / "analysis.json"
        analysis = json.loads(analysis_path.read_text()) if analysis_path.exists() else {}

        wid = meta["workshop_id"]
        name = meta.get("name", "Unknown")
        author = meta.get("author", "Unknown")
        mod_type = analysis.get("mod_type", "unknown").capitalize()
        complexity = analysis.get("complexity", "unknown").capitalize()
        status = STATUS_EMOJI.get(meta.get("status", "pending"), meta.get("status", "pending"))
        workshop_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={wid}"

        download = ""
        zip_files = list(mod_dir.glob("*.zip"))
        if zip_files:
            tag = f"mod-{wid}-v{meta.get('patch_version', '1.0')}"
            download = f"[Download](../../releases/tag/{tag})"

        rows.append(
            f"| {name} | {author} | {mod_type} | {complexity} | {status} | [Workshop]({workshop_url}) | {download} |"
        )

    return HEADER + "\n".join(rows) + "\n"
