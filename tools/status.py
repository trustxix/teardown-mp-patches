"""Session boot script — single-command project status report."""

import subprocess
from pathlib import Path

import click

from tools.common import LIVE_MODS_DIR, LOG_PATH, discover_mods, read_lua_files


def build_status_report(mods_dir: Path | None = None, skip_git: bool = False, skip_log: bool = False) -> str:
    if mods_dir is None:
        mods_dir = LIVE_MODS_DIR

    lines = []
    lines.append("TEARDOWN MP PATCHER -- Status")
    lines.append("=" * 50)

    # Mod count
    mods = discover_mods(mods_dir)
    lines.append(f"Mods installed:   {len(mods)}")

    # Git
    if skip_git:
        lines.append("Last commit:      N/A")
    else:
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                capture_output=True, text=True, timeout=5,
                cwd=str(Path(__file__).parent.parent)
            )
            commit = result.stdout.strip() if result.returncode == 0 else "N/A"
            lines.append(f"Last commit:      {commit}")
        except Exception:
            lines.append("Last commit:      N/A")

    # Game log
    if skip_log:
        lines.append("Game log:         N/A")
    else:
        try:
            log_path = LOG_PATH
            if log_path.exists():
                from tools.logparse import parse_log
                content = log_path.read_text(encoding="utf-8", errors="replace")
                log_result = parse_log(content)
                total_errors = sum(len(errs) for errs in log_result["mods"].values())
                mod_count = len(log_result["mods"])
                if total_errors == 0:
                    lines.append(f"Game log:         Teardown {log_result['version']} - 0 errors")
                else:
                    lines.append(f"Game log:         {mod_count} mod(s) with errors, {total_errors} total")
                    for mod_name, errors in sorted(log_result["mods"].items())[:3]:
                        err = errors[0]
                        if err["type"] == "runtime":
                            lines.append(f"  - {mod_name} line {err['line']}: {err['message'][:60]}")
                        else:
                            lines.append(f"  - {mod_name}: {err['type']}")
            else:
                lines.append("Game log:         not found")
        except Exception:
            lines.append("Game log:         N/A")

    # Lint tier-1
    try:
        from tools.lint import lint_source
        tier1_errors = []
        for mod_dir in mods:
            for rel_path, source in read_lua_files(mod_dir):
                if rel_path == "options.lua":
                    continue
                findings = lint_source(source, rel_path, tier="1")
                for f in findings:
                    f["mod"] = mod_dir.name
                    tier1_errors.append(f)

        lines.append("")
        if not tier1_errors:
            lines.append(f"Lint (Tier 1):    0 hard errors across {len(mods)} mods [OK]")
        else:
            lines.append(f"Lint (Tier 1):    {len(tier1_errors)} hard errors")
            for e in tier1_errors[:5]:
                lines.append(f"  - {e['mod']}/{e['file']}:{e['line']} {e['check']}")
    except Exception:
        lines.append("\nLint (Tier 1):    N/A")

    # Missing features summary
    try:
        from tools.audit import detect_features
        missing_shoot = 0
        missing_aim = 0
        missing_pickup = 0
        gun_count = 0

        for mod_dir in mods:
            combined: dict[str, bool] = {}
            for rel_path, source in read_lua_files(mod_dir):
                features = detect_features(source)
                for k, v in features.items():
                    combined[k] = combined.get(k, False) or v

            if combined.get("is_gun_mod"):
                gun_count += 1
                if not combined.get("has_shoot"):
                    missing_shoot += 1
                if not combined.get("has_aim_info"):
                    missing_aim += 1
            if not combined.get("has_ammo_pickup"):
                missing_pickup += 1

        lines.append(f"Missing features: {missing_shoot}/{gun_count} gun mods need Shoot(), "
                     f"{missing_aim}/{gun_count} need AimInfo, "
                     f"{missing_pickup}/{len(mods)} need AmmoPickup")
    except Exception:
        lines.append("Missing features: N/A")

    return "\n".join(lines)


@click.command("status")
def status_cli():
    """Show project status report."""
    click.echo(build_status_report())


if __name__ == "__main__":
    status_cli()
