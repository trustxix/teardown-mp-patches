"""Tests for tools/deepcheck.py — deep semantic analysis."""

import pytest
from pathlib import Path

from tools.deepcheck import (
    check_assets, check_id_xref, check_firing_chain, check_effect_chain,
    check_hud, check_servercall_params, run_deepcheck,
    AssetFinding, ChainFinding, Finding, DeepcheckReport,
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

    def test_auxiliary_servercall_targets_suppressed(self, tmp_path):
        """ServerCall targets like setOptionsOpen should not WARN when server already has damage chain."""
        mod = tmp_path / "aux_targets"
        mod.mkdir()
        (mod / "info.txt").write_text("name = AuxTargets\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            '#include "script/include/player.lua"\n'
            'function server.init()\n'
            '    RegisterTool("gun", "Gun", "MOD/vox/g.vox", 5)\n'
            'end\n'
            'function server.tick(dt)\n'
            '    for p in Players() do\n'
            '        if InputPressed("usetool", p) then\n'
            '            local aim = GetPlayerAimInfo(p)\n'
            '            Shoot(aim.pos, aim.dir, "bullet", 1, 100, p, "gun")\n'
            '        end\n'
            '    end\n'
            'end\n'
            'function server.setOptionsOpen(p, open)\n'
            '    -- no Shoot here, just options toggle\n'
            'end\n'
            'function client.tick(dt)\n'
            '    local p = GetLocalPlayer()\n'
            '    if InputPressed("usetool") then\n'
            '        ServerCall("server.fire", p)\n'
            '        ServerCall("server.setOptionsOpen", p, true)\n'
            '    end\n'
            'end\n'
            'function server.fire(p)\n'
            '    Shoot(Vec(0,0,0), Vec(0,0,1), "bullet", 1, 100, p, "gun")\n'
            'end\n'
        )
        findings = check_firing_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        # setOptionsOpen should NOT produce a WARN because server.fire has Shoot
        assert not any("setOptionsOpen" in f.detail for f in warns), \
            "Auxiliary ServerCall target should not WARN when another target has damage"


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
        """QueryShot+ApplyPlayerDamage without ClientCall should warn."""
        mod = tmp_path / "silent"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Silent\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.slash(p, pos, dir)\n'
            '    local hit, dist, shape, player = QueryShot(pos, dir, 5, 0.5, p)\n'
            '    if player ~= 0 then ApplyPlayerDamage(player, 0.5, "sword", p) end\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert any("no clientcall" in f.detail.lower() or "silent" in f.detail.lower() for f in warns)

    def test_auto_replicated_no_warn(self, tmp_path):
        """Shoot() and Explosion() are auto-replicated — no ClientCall needed."""
        mod = tmp_path / "autofx"
        mod.mkdir()
        (mod / "info.txt").write_text("name = AutoFX\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.fire(p, pos, dir)\n'
            '    Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert len(warns) == 0

    def test_non_weapon_empty(self, tmp_path):
        mod = tmp_path / "env"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Env\nversion = 2")
        (mod / "main.lua").write_text('#version 2\nfunction server.init()\nend\n')
        findings = check_effect_chain(mod)
        assert findings == []

    def test_lint_ok_file_suppresses_server_effects(self, tmp_path):
        """@lint-ok-file SERVER-EFFECT should suppress effect chain FAILs."""
        mod = tmp_path / "suppressed"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Suppressed\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            '-- @lint-ok-file SERVER-EFFECT\n'
            'function server.shoot(p, pos, dir)\n'
            '    Shoot(pos, dir, "bullet", 1, 100, p)\n'
            '    PlaySound(LoadSound("MOD/snd/bang.ogg"), pos)\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0, f"Expected no FAILs with @lint-ok-file, got: {fails}"

    def test_auxiliary_clientcall_suppressed_with_auto_replicate(self, tmp_path):
        """ClientCall target without effects should not WARN when Explosion() auto-replicates."""
        mod = tmp_path / "auxclient"
        mod.mkdir()
        (mod / "info.txt").write_text("name = AuxClient\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.detonate(p, x, y, z)\n'
            '    Explosion(Vec(x, y, z), 2)\n'
            '    ClientCall(0, "client.onBoom", x, y, z)\n'
            'end\n'
            'function client.onBoom(x, y, z)\n'
            '    -- UI counter, no sound/particle needed (Explosion auto-replicates)\n'
            '    booms = booms + 1\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert not any("onBoom" in f.detail for f in warns), \
            "Auxiliary ClientCall target should not WARN when Explosion auto-replicates effects"

    def test_registry_sync_suppresses_warn(self, tmp_path):
        """Mod using registry sync (SetFloat with sync=true) near damage should PASS, not WARN."""
        mod = tmp_path / "beamsync"
        mod.mkdir()
        (mod / "info.txt").write_text("name = BeamSync\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.tickPlayer(p, dt)\n'
            '    local hit, dist, shape, player, factor = QueryShot(pos, dir, 100, 0, p)\n'
            '    if player ~= 0 then\n'
            '        ApplyPlayerDamage(player, 1.0 * dt, "beam", p)\n'
            '    end\n'
            '    SetFloat("beam."..p..".hx", pos[1], true)\n'
            '    SetFloat("beam."..p..".hy", pos[2], true)\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        passes = [f for f in findings if f.status == "PASS"]
        assert len(warns) == 0, f"Registry sync should suppress WARN, got: {[f.detail for f in warns]}"
        assert any("registry sync" in f.detail for f in passes)

    def test_explosion_colocated_with_queryshot_passes(self, tmp_path):
        """Mod with QueryShot + Explosion in same function should PASS (Explosion is auto-replicated)."""
        mod = tmp_path / "rocketlauncher"
        mod.mkdir()
        (mod / "info.txt").write_text("name = RocketLauncher\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.tickProjectile(proj, p)\n'
            '    local hit, dist, shape, player, factor = QueryShot(proj.pos, proj.dir, 5, 0, p)\n'
            '    if hit then\n'
            '        local hitPos = VecAdd(proj.pos, VecScale(proj.dir, dist))\n'
            '        if player ~= 0 then\n'
            '            ApplyPlayerDamage(player, 5 * factor, "rocket", p)\n'
            '        end\n'
            '        Explosion(hitPos, 3)\n'
            '    end\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        passes = [f for f in findings if f.status == "PASS"]
        assert len(warns) == 0, f"Explosion co-location should suppress WARN, got: {[f.detail for f in warns]}"
        assert any("Explosion" in f.detail for f in passes)

    def test_lint_ok_file_only_suppresses_annotated_file(self, tmp_path):
        """@lint-ok-file in one file should not suppress a different file WITHOUT annotation."""
        mod = tmp_path / "partial"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Partial\nversion = 2")
        # File WITH suppression
        (mod / "suppressed.lua").write_text(
            '#version 2\n'
            '-- @lint-ok-file SERVER-EFFECT\n'
            'function server.okShoot(p, pos, dir)\n'
            '    Shoot(pos, dir, "bullet", 1, 100, p)\n'
            '    PlaySound(LoadSound("MOD/snd/ok.ogg"), pos)\n'
            'end\n'
        )
        # File WITHOUT suppression — different function name
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.badShoot(p, pos, dir)\n'
            '    Shoot(pos, dir, "bullet", 1, 100, p)\n'
            '    PlaySound(LoadSound("MOD/snd/bad.ogg"), pos)\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        fails = [f for f in findings if f.status == "FAIL"]
        # server.badShoot should still FAIL (not suppressed)
        assert any("server.badShoot" in f.detail for f in fails), \
            f"server.badShoot should FAIL without suppression, got: {[f.detail for f in fails]}"

    def test_cross_function_clientcall_passes(self, tmp_path):
        """ClientCall in server.tick should suppress WARN even when damage is in a helper function."""
        mod = tmp_path / "crossfunc"
        mod.mkdir()
        (mod / "info.txt").write_text("name = CrossFunc\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.tick(dt)\n'
            '    damage_system(pos, dir)\n'
            '    ClientCall(0, "client.onHit", pos[1], pos[2], pos[3])\n'
            'end\n'
            'function damage_system(pos, dir)\n'
            '    local hit, dist, shape, player = QueryShot(pos, dir, 50, 0, p)\n'
            '    if player ~= 0 then ApplyPlayerDamage(player, 1, "tool", p) end\n'
            'end\n'
            'function client.onHit(x, y, z)\n'
            '    PlaySound(snd, Vec(x, y, z))\n'
            '    SpawnParticle(Vec(x, y, z), Vec(0, 1, 0), 1)\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        passes = [f for f in findings if f.status == "PASS"]
        assert len(warns) == 0, f"Cross-function ClientCall should not WARN, got: {[f.detail for f in warns]}"
        assert any(f.status == "PASS" for f in passes)

    def test_shared_table_cross_function_passes(self, tmp_path):
        """Shared table writes in server + reads in client should suppress WARN."""
        mod = tmp_path / "sharedtbl"
        mod.mkdir()
        (mod / "info.txt").write_text("name = SharedTbl\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'shared = { projectiles = {} }\n'
            'function server.init()\n'
            '    shared.projectiles[1] = { active = false }\n'
            'end\n'
            'function server.updateProjectile(proj, p)\n'
            '    local hit, dist, shape, player = QueryShot(proj.pos, proj.dir, 50, 0, p)\n'
            '    if player ~= 0 then ApplyPlayerDamage(player, 1, "tool", p) end\n'
            '    proj.hitPos = VecCopy(hitPos)\n'
            'end\n'
            'function client.handleEffects()\n'
            '    for i, proj in ipairs(shared.projectiles) do\n'
            '        if proj.hitPos then PlaySound(snd, proj.hitPos) end\n'
            '    end\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert len(warns) == 0, f"Shared table cross-function should not WARN, got: {[f.detail for f in warns]}"

    def test_allplayer_client_effects_passes(self, tmp_path):
        """Client effects in InputDown('usetool', p) for all players should suppress WARN."""
        mod = tmp_path / "allplayer"
        mod.mkdir()
        (mod / "info.txt").write_text("name = AllPlayer\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.tickPlayer(p, dt)\n'
            '    local hit, dist, shape, player = QueryShot(pos, dir, 100, 0, p)\n'
            '    if player ~= 0 then ApplyPlayerDamage(player, 1 * dt, "beam", p) end\n'
            'end\n'
            'function client.tickPlayer(p, dt)\n'
            '    if InputDown("usetool", p) then\n'
            '        DrawLine(start, hitPos, 1, 0.3, 0.3)\n'
            '        PointLight(hitPos, 1, 0.2, 0.2, 0.5)\n'
            '        PlayLoop(snd, hitPos, 0.75)\n'
            '    end\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert len(warns) == 0, f"All-player client effects should not WARN, got: {[f.detail for f in warns]}"

    def test_deepcheck_ok_effect_suppresses(self, tmp_path):
        """@deepcheck-ok EFFECT in first 5 lines should suppress all effect chain findings."""
        mod = tmp_path / "effectok"
        mod.mkdir()
        (mod / "info.txt").write_text("name = EffectOK\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            '-- @deepcheck-ok EFFECT (complex broadcasting pattern)\n'
            'function server.slash(p, pos, dir)\n'
            '    local hit, dist, shape, player = QueryShot(pos, dir, 5, 0.5, p)\n'
            '    if player ~= 0 then ApplyPlayerDamage(player, 0.5, "sword", p) end\n'
            'end\n'
        )
        findings = check_effect_chain(mod)
        assert len(findings) == 0, f"@deepcheck-ok EFFECT should suppress all findings, got: {findings}"


# ===========================================================================
# check_assets suppressions
# ===========================================================================

class TestAssetSuppressions:
    def test_deepcheck_ok_asset_per_line(self, tmp_path):
        """@deepcheck-ok ASSET on a line suppresses that asset finding."""
        mod = tmp_path / "lineok"
        mod.mkdir()
        (mod / "info.txt").write_text("name = LineOK\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'local s = LoadSound("MOD/snd/missing.ogg") -- @deepcheck-ok ASSET\n'
        )
        findings = check_assets(mod)
        # Line-level suppression should skip the line entirely
        assert all(f.status != "FAIL" for f in findings), \
            f"Expected no FAILs with per-line @deepcheck-ok ASSET, got: {findings}"

    def test_deepcheck_ok_asset_file_level(self, tmp_path):
        """@deepcheck-ok ASSET in first 5 lines suppresses entire file."""
        mod = tmp_path / "fileok"
        mod.mkdir()
        (mod / "info.txt").write_text("name = FileOK\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            '-- @deepcheck-ok ASSET (upstream: assets never shipped)\n'
            'local s = LoadSound("MOD/snd/missing.ogg")\n'
            'local t = LoadSound("MOD/snd/also_missing.ogg")\n'
        )
        findings = check_assets(mod)
        assert len(findings) == 0, \
            f"Expected no findings with file-level @deepcheck-ok ASSET, got: {findings}"

    def test_commented_asset_ref_skipped(self, tmp_path):
        """Asset references inside Lua comments should be skipped."""
        mod = tmp_path / "commented"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Commented\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            '-- old: LoadSound("MOD/snd/removed.ogg")\n'
            'local s = LoadSound("MOD/snd/exists.ogg")\n'
        )
        (mod / "snd").mkdir()
        (mod / "snd" / "exists.ogg").write_bytes(b"fake")
        findings = check_assets(mod)
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0, \
            f"Commented-out asset ref should not FAIL, got: {fails}"


# ===========================================================================
# check_hud
# ===========================================================================

class TestHudValidator:
    def test_complete_gun_passes(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_hud(mod_dir)
        passes = [f for f in findings if f.status == "PASS"]
        assert len(passes) >= 1

    def test_no_draw_warns(self, tmp_path):
        mod = tmp_path / "no_draw"
        mod.mkdir()
        (mod / "info.txt").write_text("name = NoDraw\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.init()\n'
            '    RegisterTool("gun", "Gun", "MOD/vox/g.vox", 5)\n'
            'end\n'
        )
        findings = check_hud(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert any("client.draw" in f.detail.lower() for f in warns)

    def test_no_tool_guard_warns(self, tmp_path):
        mod = tmp_path / "no_guard"
        mod.mkdir()
        (mod / "info.txt").write_text("name = NoGuard\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.init()\n'
            '    RegisterTool("gun", "Gun", "MOD/vox/g.vox", 5)\n'
            'end\n'
            'function client.draw()\n'
            '    UiText("always shown")\n'
            'end\n'
        )
        findings = check_hud(mod)
        warns = [f for f in findings if f.status == "WARN"]
        assert any("GetPlayerTool" in f.detail for f in warns)

    def test_options_lua_does_not_shadow_main_tool_guard(self, tmp_path):
        """Regression: options.lua client.draw() must not shadow main.lua's tool guard."""
        mod = tmp_path / "dual_draw"
        mod.mkdir()
        (mod / "info.txt").write_text("name = DualDraw\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            '#include "script/include/player.lua"\n'
            'function server.init()\n'
            '    RegisterTool("gun", "Gun", "MOD/vox/g.vox", 5)\n'
            'end\n'
            'function client.draw()\n'
            '    local p = GetLocalPlayer()\n'
            '    if GetPlayerTool(p) ~= "gun" then return end\n'
            '    UiText("ammo: 10")\n'
            'end\n'
        )
        (mod / "options.lua").write_text(
            '#version 2\n'
            'function client.draw()\n'
            '    UiMakeInteractive()\n'
            '    UiText("Options Menu")\n'
            'end\n'
        )
        findings = check_hud(mod)
        passes = [f for f in findings if f.status == "PASS"]
        warns = [f for f in findings if f.status == "WARN"]
        assert any("GetPlayerTool" in f.detail for f in passes), \
            "main.lua tool guard should produce PASS even when options.lua has a guardless client.draw"
        assert not any("GetPlayerTool" in f.detail for f in warns), \
            "options.lua client.draw should not cause false-positive WARN"


# ===========================================================================
# check_servercall_params
# ===========================================================================

class TestServerCallParams:
    def test_complete_gun_passes(self):
        mod_dir = FIXTURES / "complete_gun"
        findings = check_servercall_params(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert len(fails) == 0

    def test_missing_target_fails(self):
        mod_dir = FIXTURES / "broken_chain"
        findings = check_servercall_params(mod_dir)
        fails = [f for f in findings if f.status == "FAIL"]
        assert any("server.shoot" in f.detail for f in fails)

    def test_param_count_mismatch(self, tmp_path):
        mod = tmp_path / "bad_params"
        mod.mkdir()
        (mod / "info.txt").write_text("name = BadParams\nversion = 2")
        (mod / "main.lua").write_text(
            '#version 2\n'
            'function server.shoot(p, pos, dir)\n'
            '    Shoot(pos, dir, "bullet", 1, 100, p)\n'
            'end\n'
            'function client.tick(dt)\n'
            '    ServerCall("server.shoot", pos, dir)\n'
            'end\n'
        )
        findings = check_servercall_params(mod)
        fails = [f for f in findings if f.status == "FAIL"]
        assert any("param" in f.detail.lower() or "argument" in f.detail.lower() for f in fails)


# ===========================================================================
# run_deepcheck orchestrator
# ===========================================================================

class TestRunDeepcheck:
    def test_complete_gun_no_fails(self):
        mod_dir = FIXTURES / "complete_gun"
        report = run_deepcheck(mod_dir, is_weapon=True)
        assert report.mod_name == "complete_gun"
        # May have WARNs (e.g., onRecoil has ShakeCamera but not PlaySound) but no FAILs
        assert report.overall_status in ("PASS", "WARN")

    def test_non_weapon_skips_chains(self, tmp_path):
        mod = tmp_path / "env_mod"
        mod.mkdir()
        (mod / "info.txt").write_text("name = Env\nversion = 2")
        (mod / "main.lua").write_text('#version 2\nfunction server.init()\nend\n')
        report = run_deepcheck(mod, is_weapon=False)
        assert report.firing_chain == []
        assert report.effect_chain == []
        assert report.hud == []

    def test_broken_mod_fails(self):
        mod_dir = FIXTURES / "broken_chain"
        report = run_deepcheck(mod_dir, is_weapon=True)
        assert report.overall_status == "FAIL"
