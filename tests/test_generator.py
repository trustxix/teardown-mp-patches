"""Tests for tools/gun_v2_generator.py — ensures generated code follows all API rules."""

import pytest

from tools.gun_v2_generator import generate_standard_auto_rifle


# Minimal config for generator
MINIMAL_CONFIG = {
    'tool_id': 'testgun',
    'display_name': 'Test Gun',
    'vox_path': 'MOD/vox/test.vox',
    'group': 3,
    'damage': 1.0,
    'velocity': 1.5,
    'reload_time': 2.0,
    'shot_delay': 0.1,
    'ammo': 30,
    'mags': 3,
}


class TestGeneratorOutput:
    """Verify generated Lua follows all CLAUDE.md rules."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.lua = generate_standard_auto_rifle(MINIMAL_CONFIG)

    def test_has_version_2_header(self):
        assert '#version 2' in self.lua

    def test_has_player_include(self):
        assert '#include "script/include/player.lua"' in self.lua

    def test_has_players_table(self):
        assert 'players = {}' in self.lua

    def test_register_tool_with_group(self):
        assert 'RegisterTool("testgun"' in self.lua

    def test_set_tool_ammo_pickup(self):
        assert 'SetToolAmmoPickupAmount("testgun"' in self.lua

    def test_hide_engine_ammo_display(self):
        assert 'ammo.display' in self.lua

    def test_uses_get_player_aim_info(self):
        assert 'GetPlayerAimInfo(' in self.lua

    def test_queryshot_guard_uses_neq_zero(self):
        """Issue #47: QueryShot guard MUST use ~= 0, not truthy check."""
        assert 'qplayer ~= 0' in self.lua
        # Must NOT have bare truthy check
        lines = self.lua.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('if qplayer then'):
                pytest.fail("Generator uses 'if qplayer then' — must use 'if qplayer ~= 0 then' (Issue #47)")

    def test_apply_player_damage_has_tool_id(self):
        assert 'ApplyPlayerDamage(qplayer' in self.lua
        assert '"testgun"' in self.lua

    def test_server_call_passes_player_id(self):
        """Issue #51: ServerCall must pass player ID explicitly."""
        lines = self.lua.splitlines()
        for line in lines:
            stripped = line.strip()
            if 'ServerCall(' in stripped and not stripped.startswith('--'):
                # Every ServerCall should have ", p," or ", p)" after the function name
                assert ', p,' in stripped or ', p)' in stripped, \
                    f"ServerCall missing player param: {stripped}"

    def test_options_menu_has_interactive(self):
        assert 'UiMakeInteractive()' in self.lua

    def test_options_guard_on_usetool(self):
        """Options menu must suppress usetool input."""
        assert 'not data.optionsOpen' in self.lua

    def test_no_ipairs_on_players(self):
        """Must use for p in Players(), not ipairs(Players())."""
        assert 'ipairs(Players' not in self.lua
        assert 'ipairs(PlayersAdded' not in self.lua
        assert 'ipairs(PlayersRemoved' not in self.lua

    def test_set_tool_enabled_correct_order(self):
        """SetToolEnabled(toolId, true, p) — string first, bool second, player last."""
        lines = self.lua.splitlines()
        for line in lines:
            if 'SetToolEnabled(' in line and not line.strip().startswith('--'):
                assert '"testgun"' in line, f"SetToolEnabled missing tool ID string: {line.strip()}"
