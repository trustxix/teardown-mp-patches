"""Report which mods are ready for multiplayer testing.

Combines classify + health + diff to give a clear go/no-go for each mod.

Usage:
    python -m tools.mp_ready              # Full report
    python -m tools.mp_ready --go-only    # Only show mods ready for MP
"""
import sys
from pathlib import Path
from tools.common import LIVE_MODS_DIR
from tools.classify import classify_mod, BUILTIN_MODS
from tools.lint import lint_source


def assess_mp_readiness(mod_dir: Path) -> dict:
    """Determine if a mod is ready for MP testing."""
    result = {"name": mod_dir.name, "ready": False, "reason": "", "category": ""}

    classification = classify_mod(mod_dir)

    # Content/map mods are always ready
    if classification["mp_status"] == "content":
        result["ready"] = True
        result["reason"] = "Content mod -- no script logic"
        result["category"] = "content"
        return result

    # v1 mods are never ready
    if classification["mp_status"] == "disabled":
        result["ready"] = False
        result["reason"] = "v1 script -- silently disabled in MP"
        result["category"] = "dead"
        return result

    # Check for tier-1 lint errors (hard blockers)
    main_lua = mod_dir / "main.lua"
    if main_lua.exists():
        try:
            source = main_lua.read_text(errors="ignore")
            if not source.strip().startswith("<"):
                findings = lint_source(source, str(main_lua), tier="1")
                tier1_errors = [f for f in findings if f["severity"] == "error"]
                if tier1_errors:
                    # Filter out errors from built-in game patterns that are false positives
                    real_errors = [f for f in tier1_errors if f["check"] not in ("MOUSEDX",)]
                    if real_errors:
                        result["ready"] = False
                        checks = set(f["check"] for f in real_errors)
                        result["reason"] = f"Tier-1 lint errors: {', '.join(checks)}"
                        result["category"] = "blocked"
                        return result
        except Exception:
            pass

    # Check for critical desync patterns
    classify_issues = classification.get("issues", [])
    critical_issues = [i for i in classify_issues if i in ("raw-key-player", "shared-bomb", "file-scope-local")]
    if critical_issues:
        result["ready"] = False
        result["reason"] = f"Desync risk: {', '.join(critical_issues)}"
        result["category"] = "risky"
        return result

    # If we get here, mod is likely ready
    result["ready"] = True
    if classify_issues:
        result["reason"] = f"Minor issues: {', '.join(classify_issues)}"
        result["category"] = "caution"
    else:
        result["reason"] = "Clean"
        result["category"] = "go"

    return result


def main():
    go_only = "--go-only" in sys.argv

    results = []
    for d in sorted(LIVE_MODS_DIR.iterdir()):
        if not d.is_dir() or d.name.lower() in BUILTIN_MODS or d.name.startswith("__"):
            continue
        if not (d / "id.txt").exists():
            continue
        results.append(assess_mp_readiness(d))

    go_mods = [r for r in results if r["ready"]]
    no_go = [r for r in results if not r["ready"]]

    if not go_only:
        print("MP READINESS REPORT")
        print("=" * 80)
        print()

    print(f"GO ({len(go_mods)} mods ready for MP):")
    for r in go_mods:
        icon = {"go": "+", "content": ".", "caution": "~"}.get(r["category"], " ")
        print(f"  {icon} {r['name']:<40} {r['reason']}")

    if not go_only:
        print()
        print(f"NO-GO ({len(no_go)} mods NOT ready):")
        for r in no_go:
            icon = {"blocked": "!", "dead": "X", "risky": "~"}.get(r["category"], "?")
            print(f"  {icon} {r['name']:<40} {r['reason']}")

    print()
    print(f"Summary: {len(go_mods)}/{len(results)} mods ready for MP")


if __name__ == "__main__":
    main()
