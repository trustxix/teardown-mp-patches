"""Tests for tools/test.py — test orchestrator and report generation."""

import pytest
from pathlib import Path

from tools.test import generate_report, TestReport
from tools.deepcheck import DeepcheckReport, Finding


class TestReportGeneration:
    def test_all_pass_report(self):
        static = DeepcheckReport(mod_name="TestMod")
        report = generate_report(
            mod_name="TestMod",
            static_report=static,
            runtime=None,
            test_type="static",
        )
        assert report.overall_status == "PASS"
        assert "TestMod" in report.to_text()

    def test_fail_report_from_static(self):
        static = DeepcheckReport(mod_name="BadMod")
        static.id_xref = [Finding(
            validator="ID-XREF", status="FAIL",
            detail="Case mismatch: RegisterTool vs SetToolEnabled"
        )]
        report = generate_report(
            mod_name="BadMod", static_report=static,
            runtime=None, test_type="static",
        )
        assert report.overall_status == "FAIL"
        assert "FAIL" in report.to_text()
        assert "Case mismatch" in report.to_text()

    def test_crash_report(self):
        static = DeepcheckReport(mod_name="CrashMod")
        report = generate_report(
            mod_name="CrashMod", static_report=static,
            runtime={"crashed": True, "session_duration": 5.0},
            test_type="full",
        )
        assert report.overall_status == "CRASH"

    def test_runtime_errors_fail(self):
        static = DeepcheckReport(mod_name="ErrMod")
        report = generate_report(
            mod_name="ErrMod", static_report=static,
            runtime={
                "compile_errors": [{"file": "main.lua", "message": "syntax error"}],
                "runtime_errors": [],
                "session_duration": 10.0,
                "mod_loaded": True,
            },
            test_type="full",
        )
        assert report.overall_status == "FAIL"

    def test_report_text_format(self):
        static = DeepcheckReport(mod_name="MyGun")
        report = generate_report(
            mod_name="MyGun", static_report=static,
            runtime=None, test_type="static",
        )
        text = report.to_text()
        assert "TEST REPORT: MyGun" in text
        assert "STATIC ANALYSIS" in text
        assert "RESULT:" in text

    def test_warn_status(self):
        static = DeepcheckReport(mod_name="WarnMod")
        static.hud = [Finding(
            validator="HUD", status="WARN",
            detail="No client.draw() found"
        )]
        report = generate_report(
            mod_name="WarnMod", static_report=static,
            runtime=None, test_type="static",
        )
        assert report.overall_status == "WARN"


class TestRunTest:
    """Tests that run_test works on fixture mods."""

    def test_static_test_on_fixture(self):
        from tools.test import run_test
        from unittest.mock import patch

        fixture = Path(__file__).parent / "fixtures" / "deepcheck" / "complete_gun"
        with patch("tools.test.discover_mods", return_value=[fixture]):
            report = run_test("complete_gun", static_only=True)
            assert report.test_type == "static"
            assert report.overall_status in ("PASS", "WARN")

    def test_missing_mod_raises(self):
        from tools.test import run_test
        from unittest.mock import patch

        with patch("tools.test.discover_mods", return_value=[]):
            with pytest.raises(Exception):
                run_test("nonexistent_mod", static_only=True)
