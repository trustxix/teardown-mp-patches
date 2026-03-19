"""Autonomous test platform for Teardown MP mods.

Usage:
    python -m tools.test --mod "ModName"           # Full test (static + runtime)
    python -m tools.test --mod "ModName" --static   # Static analysis only
    python -m tools.test --batch all                # Test all mods (static)
    python -m tools.test --setup                    # First-time calibration
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import click

from tools.common import LIVE_MODS_DIR, discover_mods, TEST_RESULTS_DIR, TEST_CONFIG_PATH, TEST_HARNESS_DIR
from tools.deepcheck import run_deepcheck, DeepcheckReport, Finding


# ---------------------------------------------------------------------------
# Report types
# ---------------------------------------------------------------------------

@dataclass
class TestReport:
    """Combined results from all test layers."""
    mod_name: str
    test_type: str  # "static", "full"
    timestamp: str = ""
    static_report: DeepcheckReport | None = None
    runtime: dict | None = None
    screenshots: list[Path] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        statuses = []
        if self.static_report:
            statuses.append(self.static_report.overall_status)
        if self.runtime:
            if self.runtime.get("crashed"):
                return "CRASH"
            if self.runtime.get("compile_errors"):
                return "FAIL"
            if self.runtime.get("runtime_errors"):
                return "FAIL"
        if not statuses:
            return "PASS"
        if "FAIL" in statuses:
            return "FAIL"
        if "INCONCLUSIVE" in statuses:
            return "INCONCLUSIVE"
        if "WARN" in statuses:
            return "WARN"
        return "PASS"

    def to_text(self) -> str:
        lines = []
        lines.append(f"TEST REPORT: {self.mod_name}")
        lines.append("=" * 54)
        lines.append(f"Generated: {self.timestamp}")
        lines.append(f"Test type: {self.test_type}")
        lines.append("")

        if self.static_report:
            lines.append("STATIC ANALYSIS")
            r = self.static_report

            # Assets
            asset_fails = [f for f in r.assets if f.status == "FAIL"]
            asset_total = len(r.assets)
            if asset_fails:
                lines.append(f"  Asset validation:  FAIL — {len(asset_fails)}/{asset_total} assets missing")
                for f in asset_fails:
                    lines.append(f"    - {f.detail}")
            elif asset_total > 0:
                lines.append(f"  Asset validation:  PASS — {asset_total} assets found")
            else:
                lines.append("  Asset validation:  N/A — no asset references")

            # ID xref — empty = all matched (PASS), only N/A if no firing_chain either
            id_fails = [f for f in r.id_xref if f.status == "FAIL"]
            id_warns = [f for f in r.id_xref if f.status == "WARN"]
            if id_fails:
                lines.append(f"  ID cross-ref:      FAIL — {len(id_fails)} mismatches")
                for f in id_fails:
                    lines.append(f"    - {f.detail}")
            elif id_warns:
                lines.append(f"  ID cross-ref:      WARN — {len(id_warns)} warnings")
                for f in id_warns:
                    lines.append(f"    - {f.detail}")
            elif r.firing_chain or r.id_xref:
                lines.append("  ID cross-ref:      PASS — all IDs consistent")
            else:
                lines.append("  ID cross-ref:      N/A — no tools registered")

            # Firing chain
            fc_fails = [f for f in r.firing_chain if f.status == "FAIL"]
            fc_passes = [f for f in r.firing_chain if f.status == "PASS"]
            if fc_fails:
                lines.append(f"  Firing chain:      FAIL")
                for f in fc_fails:
                    lines.append(f"    - {f.detail}")
            elif fc_passes:
                lines.append(f"  Firing chain:      PASS — {fc_passes[0].detail}")
            elif r.firing_chain:
                lines.append(f"  Firing chain:      WARN")
            else:
                lines.append("  Firing chain:      N/A — not a weapon mod")

            # Effect chain
            ec_fails = [f for f in r.effect_chain if f.status == "FAIL"]
            ec_passes = [f for f in r.effect_chain if f.status == "PASS"]
            if ec_fails:
                lines.append(f"  Effect chain:      FAIL")
                for f in ec_fails:
                    lines.append(f"    - {f.detail}")
            elif ec_passes:
                lines.append(f"  Effect chain:      PASS")
            elif r.effect_chain:
                lines.append(f"  Effect chain:      WARN")
                for f in r.effect_chain:
                    if f.status == "WARN":
                        lines.append(f"    - {f.detail}")
            else:
                lines.append("  Effect chain:      N/A")

            # HUD
            hud_fails = [f for f in r.hud if f.status == "FAIL"]
            hud_warns = [f for f in r.hud if f.status == "WARN"]
            if hud_fails:
                lines.append("  HUD validation:    FAIL")
                for f in hud_fails:
                    lines.append(f"    - {f.detail}")
            elif hud_warns:
                lines.append("  HUD validation:    WARN")
                for f in hud_warns:
                    lines.append(f"    - {f.detail}")
            elif r.hud:
                lines.append("  HUD validation:    PASS")
            else:
                lines.append("  HUD validation:    N/A")

            # ServerCall params
            sc_fails = [f for f in r.servercall_params if f.status == "FAIL"]
            if sc_fails:
                lines.append(f"  ServerCall params: FAIL — {len(sc_fails)} issues")
                for f in sc_fails:
                    lines.append(f"    - {f.detail}")
            else:
                lines.append("  ServerCall params: PASS")

        if self.runtime:
            lines.append("")
            lines.append(f"RUNTIME (game session: {self.runtime.get('session_duration', 0):.1f}s)")
            lines.append(f"  Mod loaded:        {'PASS' if self.runtime.get('mod_loaded') else 'FAIL'}")
            ce = self.runtime.get("compile_errors", [])
            re_ = self.runtime.get("runtime_errors", [])
            lines.append(f"  Compile errors:    {'PASS' if not ce else f'FAIL — {len(ce)} errors'}")
            lines.append(f"  Runtime errors:    {'PASS' if not re_ else f'FAIL — {len(re_)} errors'}")
            diag = self.runtime.get("diagnostic_data", {})
            if diag:
                st = diag.get("server_ticks", 0)
                ct = diag.get("client_ticks", 0)
                sc = diag.get("shoot_count", 0)
                snd = diag.get("sound_count", 0)
                part = diag.get("particle_count", 0)
                lines.append(f"  Diagnostic data:   S:{st} C:{ct} | Shoot:{sc} Snd:{snd} Part:{part}")

        lines.append("")
        lines.append("-" * 54)
        lines.append(f"RESULT: {self.overall_status}")
        lines.append("=" * 54)

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Test orchestration
# ---------------------------------------------------------------------------

def generate_report(mod_name: str, static_report: DeepcheckReport | None,
                    runtime: dict | None, test_type: str) -> TestReport:
    return TestReport(
        mod_name=mod_name,
        test_type=test_type,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        static_report=static_report,
        runtime=runtime,
    )


def _detect_is_weapon(mod_dir: Path) -> bool:
    """Detect if a mod is a weapon/tool mod using audit heuristics."""
    try:
        from tools.audit import audit_mod
        result = audit_mod(mod_dir)
        features = result.get("features", result)  # audit_mod wraps in {"name":..., "features":...}
        return features.get("is_gun_mod", False) or features.get("has_register_tool", False)
    except Exception:
        # Fallback: check for RegisterTool in source
        for lua_file in mod_dir.rglob("*.lua"):
            if lua_file.name == "options.lua":
                continue
            source = lua_file.read_text(encoding="utf-8", errors="replace")
            if "RegisterTool" in source:
                return True
        return False


def run_test(mod_name: str, static_only: bool = False, no_input: bool = False,
             verbose: bool = False) -> TestReport:
    """Run the full test pipeline on a mod."""
    mod_dirs = discover_mods(mod_name=mod_name)
    if not mod_dirs:
        raise click.ClickException(f"Mod not found: {mod_name}")
    mod_dir = mod_dirs[0]

    is_weapon = _detect_is_weapon(mod_dir)

    # Layer 1: Deep semantic analysis
    static_report = run_deepcheck(mod_dir, is_weapon=is_weapon)

    runtime = None
    if not static_only:
        try:
            from tools.injector import inject_diagnostics, restore_from_backup
            from tools.gamerunner import (
                GameRunnerConfig, acquire_test_lock, release_test_lock,
                run_game_test,
            )

            config = GameRunnerConfig.load()
            if not config.teardown_exe or not config.teardown_exe.exists():
                click.echo("WARN: Teardown.exe not configured. Run: python -m tools.test --setup")
                click.echo("      Skipping runtime test, showing static results only.")
            elif not acquire_test_lock():
                click.echo("WARN: Another test is running. Skipping runtime test.")
            else:
                try:
                    # Layer 2: Inject diagnostics
                    click.echo(f"Injecting diagnostics into {mod_name}...")
                    inject_diagnostics(mod_dir)

                    # Layer 3: Launch game and test
                    click.echo("Launching Teardown...")
                    game_result = run_game_test(mod_name, config, no_input=no_input)

                    # Convert GameTestResult to dict for report
                    runtime = {
                        "mod_loaded": game_result.mod_loaded,
                        "compile_errors": game_result.compile_errors,
                        "runtime_errors": game_result.runtime_errors,
                        "diagnostic_data": game_result.diagnostic_data,
                        "session_duration": game_result.session_duration,
                        "crashed": game_result.crashed,
                        "screenshot_count": len(game_result.screenshot_paths),
                        "screenshots": [str(p) for p in game_result.screenshot_paths],
                    }
                    click.echo(f"Game session: {game_result.session_duration:.1f}s, "
                              f"{len(game_result.screenshot_paths)} screenshots captured")
                finally:
                    # Always restore mod and release lock
                    restore_from_backup(mod_dir)
                    release_test_lock()
        except ImportError as e:
            click.echo(f"WARN: Runtime dependencies not installed ({e}). Run: python -m tools.test --setup")

    report = generate_report(
        mod_name=mod_name,
        static_report=static_report,
        runtime=runtime,
        test_type="static" if static_only or runtime is None else "full",
    )

    _save_report(report)

    return report


def _save_report(report: TestReport) -> None:
    """Save report to test_results/ModName/YYYY-MM-DD_HH-MM-SS/."""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result_dir = TEST_RESULTS_DIR / report.mod_name / ts
    result_dir.mkdir(parents=True, exist_ok=True)
    (result_dir / "report.txt").write_text(report.to_text(), encoding="utf-8")
    if report.runtime:
        (result_dir / "diagnostic_data.json").write_text(
            json.dumps(report.runtime, indent=2, default=str),
            encoding="utf-8",
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.command("test")
@click.option("--mod", "mod_name", required=False, help="Mod folder name")
@click.option("--static", "static_only", is_flag=True, help="Layer 1 only, no game launch")
@click.option("--batch", default=None, help="Test category: guns, all")
@click.option("--no-input", "no_input", is_flag=True, help="Game launch without input simulation")
@click.option("--verbose", is_flag=True)
@click.option("--setup", is_flag=True, help="First-time calibration")
def test_cli(mod_name, static_only, batch, no_input, verbose, setup):
    """Run autonomous tests on Teardown mods."""
    if setup:
        _run_setup()
        return

    if batch:
        mods = discover_mods()
        total = len(mods)
        passes = 0
        fails = 0
        warns = 0
        for i, mod_dir in enumerate(mods, 1):
            try:
                report = run_test(mod_dir.name, static_only=True, verbose=verbose)
                status = report.overall_status
                tag = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}.get(status, status)
                if verbose or status != "PASS":
                    click.echo(f"  [{tag}] {mod_dir.name}")
                if status == "PASS":
                    passes += 1
                elif status == "WARN":
                    warns += 1
                else:
                    fails += 1
            except Exception as e:
                click.echo(f"  [ERROR] {mod_dir.name}: {e}")
                fails += 1
        click.echo(f"\n{total} mods tested: {passes} PASS, {warns} WARN, {fails} FAIL")
        return

    if not mod_name:
        raise click.ClickException("Specify --mod or --batch")

    report = run_test(mod_name, static_only=static_only, no_input=no_input, verbose=verbose)
    click.echo(report.to_text())


def _run_setup():
    """First-time setup: find exe, install harness, check deps, save config."""
    from tools.gamerunner import find_teardown_exe, install_test_harness, GameRunnerConfig

    click.echo("=== Teardown Test Platform Setup ===\n")

    # Check runtime deps
    missing = []
    for pkg in ["mss", "pyautogui", "pygetwindow", "PIL"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        click.echo(f"Missing packages: {', '.join(missing)}")
        click.echo("Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install",
                       "mss", "pyautogui", "PyGetWindow", "Pillow"],
                      check=True)
        click.echo("Dependencies installed.\n")
    else:
        click.echo("Dependencies: all installed\n")

    # Find exe
    exe = find_teardown_exe()
    if exe:
        click.echo(f"Found Teardown: {exe}")
    else:
        click.echo("Teardown.exe not found in standard Steam locations.")
        click.echo("Runtime tests unavailable until configured. Static analysis works without it.\n")

    # Install test harness mod
    install_test_harness()
    click.echo(f"Test harness mod installed: {TEST_HARNESS_DIR}")

    # Save config
    config = GameRunnerConfig(teardown_exe=exe)
    config.save()
    click.echo(f"Config saved: {TEST_CONFIG_PATH}\n")

    click.echo("Setup complete!")
    click.echo("  Static test:  python -m tools.test --mod \"ModName\" --static")
    click.echo("  Runtime test: python -m tools.test --mod \"ModName\"")
    click.echo("  Batch test:   python -m tools.test --batch all --static")


if __name__ == "__main__":
    test_cli()
