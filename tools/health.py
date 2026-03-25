"""Per-mod health report combining lint, classify, and diff status.

Usage:
    python -m tools.health                    # All mods
    python -m tools.health --mod "AC130"      # One mod
"""
import sys
from pathlib import Path
from tools.common import LIVE_MODS_DIR
from tools.classify import classify_mod, BUILTIN_MODS
from tools.diff import diff_mod
from tools.lint import lint_source


def health_report(mod_dir: Path) -> dict:
    """Generate combined health report for a single mod."""
    report = {"name": mod_dir.name}

    # Classification
    classification = classify_mod(mod_dir)
    report["version"] = classification["version"]
    report["type"] = classification["type"]
    report["mp_status"] = classification["mp_status"]
    report["classify_issues"] = classification.get("issues", [])

    # Diff vs workshop
    diff_result = diff_mod(mod_dir, summary_only=True)
    report["diff_status"] = diff_result["status"]
    report["diff_lines"] = diff_result.get("diff_lines", 0)
    report["files_changed"] = len(diff_result.get("files_changed", []))

    # Lint
    main_lua = mod_dir / "main.lua"
    lint_findings = []
    lint_errors = 0
    lint_warnings = 0
    if main_lua.exists():
        try:
            source = main_lua.read_text(errors="ignore")
            if not source.strip().startswith("<"):  # Skip XML scene files
                findings = lint_source(source, str(main_lua))
                for f in findings:
                    if f["severity"] == "error":
                        lint_errors += 1
                    else:
                        lint_warnings += 1
                    lint_findings.append(f"{f['check']}:{f['line']}")
        except Exception:
            pass
    report["lint_errors"] = lint_errors
    report["lint_warnings"] = lint_warnings
    report["lint_findings"] = lint_findings

    # Overall health score
    if classification["mp_status"] == "disabled":
        report["health"] = "DEAD"
    elif classification["mp_status"] == "content":
        report["health"] = "OK"
    elif lint_errors > 0:
        report["health"] = "FAIL"
    elif lint_warnings > 3 or classification.get("issues"):
        report["health"] = "WARN"
    else:
        report["health"] = "OK"

    return report


def main():
    mod_filter = None
    if "--mod" in sys.argv:
        idx = sys.argv.index("--mod")
        if idx + 1 < len(sys.argv):
            mod_filter = sys.argv[idx + 1]

    reports = []
    for d in sorted(LIVE_MODS_DIR.iterdir()):
        if not d.is_dir() or d.name.lower() in BUILTIN_MODS or d.name.startswith("__"):
            continue
        if mod_filter and mod_filter.lower() not in d.name.lower():
            continue
        reports.append(health_report(d))

    # Print
    print(f"{'Mod':<38} {'Health':<6} {'Ver':<4} {'Type':<8} {'MP':<10} {'Lint':<12} {'Diff':<10}")
    print("-" * 100)

    ok_count = 0
    warn_count = 0
    fail_count = 0
    dead_count = 0

    for r in reports:
        lint_str = f"{r['lint_errors']}E/{r['lint_warnings']}W" if r['lint_errors'] or r['lint_warnings'] else "clean"
        diff_str = f"+{r['diff_lines']}" if r["diff_status"] == "modified" else r["diff_status"]

        # Color coding via prefix
        prefix = " "
        if r["health"] == "FAIL":
            prefix = "!"
            fail_count += 1
        elif r["health"] == "WARN":
            prefix = "~"
            warn_count += 1
        elif r["health"] == "DEAD":
            prefix = "X"
            dead_count += 1
        else:
            ok_count += 1

        print(f"{prefix} {r['name']:<37} {r['health']:<6} {r['version']:<4} {r['type']:<8} {r['mp_status']:<10} {lint_str:<12} {diff_str}")

    print("-" * 100)
    print(f"Total: {len(reports)} | OK: {ok_count} | WARN: {warn_count} | FAIL: {fail_count} | DEAD: {dead_count}")


if __name__ == "__main__":
    main()
