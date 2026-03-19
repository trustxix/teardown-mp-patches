"""Tests for tools/deepcheck.py — deep semantic analysis."""

import pytest
from pathlib import Path

from tools.deepcheck import check_assets, AssetFinding

FIXTURES = Path(__file__).parent / "fixtures" / "deepcheck"


# ===========================================================================
# check_assets
# ===========================================================================

class TestAssetValidator:
    def test_missing_vox_flagged(self):
        mod_dir = FIXTURES / "missing_asset"
        findings = check_assets(mod_dir)
        vox_findings = [f for f in findings if "vox/tool.vox" in f.path]
        assert len(vox_findings) == 1
        assert vox_findings[0].status == "FAIL"

    def test_missing_sound_flagged(self):
        mod_dir = FIXTURES / "missing_asset"
        findings = check_assets(mod_dir)
        snd_findings = [f for f in findings if "snd/shoot.ogg" in f.path]
        assert len(snd_findings) == 1
        assert snd_findings[0].status == "FAIL"

    def test_existing_asset_passes(self, tmp_path):
        mod = tmp_path / "good_mod"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Good\nversion = 2")
        (mod / "snd").mkdir()
        (mod / "snd" / "bang.ogg").write_bytes(b"fake")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'PlaySound(LoadSound("MOD/snd/bang.ogg"))\n'
        )
        findings = check_assets(mod)
        assert all(f.status == "PASS" for f in findings)

    def test_no_assets_returns_empty(self, tmp_path):
        mod = tmp_path / "no_assets"
        mod.mkdir()
        (mod / "info.txt").write_text("name = NoAssets\nversion = 2")
        (mod / "main.lua").write_text('#version 2\n-- no asset refs\n')
        findings = check_assets(mod)
        assert findings == []

    def test_complete_gun_assets_pass(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_assets(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0
