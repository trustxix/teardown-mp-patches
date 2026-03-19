"""Tests for tools/deepcheck.py — deep semantic analysis."""

import pytest
from pathlib import Path

from tools.deepcheck import (
    check_assets, check_id_xref, check_firing_chain, check_effect_chain,
    AssetFinding, ChainFinding, Finding,
)

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


# ===========================================================================
# check_id_xref
# ===========================================================================

class TestIdCrossRef:
    def test_mismatched_ids_flagged(self):
        mod_dir = FIXTURES / "id_mismatch"
        findings = check_id_xref(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        # RegisterTool("mygun") vs SetToolEnabled("MyGun"), SetToolAmmo("my_gun"), GetPlayerTool("MYGUN")
        assert len(fails) >= 2

    def test_consistent_ids_pass(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_id_xref(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0

    def test_missing_set_tool_ammo_warned(self, tmp_path):
        mod = tmp_path / "no_ammo"
        mod.mkdir()
        (mod / "info.txt").write_text("name = NoAmmo\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.init()\n'
            '    RegisterTool("gun", "Gun", "MOD/vox/g.vox", 5)\n'
            'end\n'
            'function server.tick(dt)\n'
            '    for p in PlayersAdded() do\n'
            '        SetToolEnabled("gun", true, p)\n'
            '    end\n'
            'end\n'
        )
        findings = check_id_xref(mod)
        warns = [f for f in findings if f.status == "WARN" and "SetToolAmmo" in f.detail]
        assert len(warns) == 1

    def test_no_register_tool_returns_empty(self, tmp_path):
        mod = tmp_path / "env_mod"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Env\nversion = 2")
        (mod / "main.lua").write_text('#version 2\nfunction server.init()\nend\n')
        findings = check_id_xref(mod)
        assert findings == []


# ===========================================================================
# check_firing_chain
# ===========================================================================

class TestFiringChain:
    def test_complete_chain_passes(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_firing_chain(mod_dir)
        assert all(f.status == "PASS" for f in findings)

    def test_missing_server_target_fails(self):
        mod_dir = FIXTURES / "broken_chain"
        findings = check_firing_chain(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert any("server.shoot" in f.detail.lower() for f in fails)

    def test_shoot_on_client_fails(self):
        mod_dir = FIXTURES / "wrong_side"
        findings = check_firing_chain(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert any("client" in f.detail.lower() for f in fails)

    def test_non_weapon_mod_no_fails(self, tmp_path):
        mod = tmp_path / "util_mod"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Util\nversion = 2")
        (mod / "main.lua").write_text('#version 2\nfunction server.init()\nend\n')
        findings = check_firing_chain(mod)
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0


# ===========================================================================
# check_effect_chain
# ===========================================================================

class TestEffectChain:
    def test_complete_gun_passes(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_effect_chain(mod_dir)
        assert all(f.status in ("PASS", "WARN") for f in findings)
        assert any(f.status == "PASS" for f in findings)

    def test_server_side_effects_fail(self, tmp_path):
        mod = tmp_path / "srvfx"
        mod.mkdir()
        (mod / "info.txt").write_text("name = SrvFx\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.shoot(p, pos, dir)\n'
            '    Shoot(pos, dir, "bullet", 1, 100, p)\n'
            '    PlaySound(LoadSound("MOD/snd/bang.ogg"), pos)\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        fails = [f for f in findings if f.status == "FAIL"]
        assert any("server" in f.detail.lower() and "PlaySound" in f.detail for f in fails)

    def test_silent_weapon_warns(self, tmp_path):
        mod = tmp_path / "silent"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Silent\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.shoot(p, pos, dir)\n'
            '    Shoot(pos, dir, "bullet", 1, 100, p)\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert any("no ClientCall" in f.detail.lower() or "silent" in f.detail.lower() for f in warns)

    def test_non_weapon_empty(self, tmp_path):
        mod = tmp_path / "env"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Env\nversion = 2")
        (mod / "main.lua").write_text('#version 2\nfunction server.init()\nend\n')
        findings = check_effect_chain(mod)
        assert findings == []
