"""Tests for tools/lint.py — tier-1 hard error checks and tier-2 best-practice checks."""

import pytest

from tools.lint import (
    check_ipairs_iterator,
    check_raw_key_player,
    check_tool_enabled_order,
    check_alttool,
    check_goto_label,
    check_mousedx,
    check_set_player_transform_client,
    check_draw_not_client,
    # Tier-2
    check_missing_ammo_display,
    check_missing_tool_ammo,
    check_missing_ammo_pickup,
    check_missing_options_guard,
    check_missing_options_sync,
    check_handle_gt_zero,
    check_manual_aim,
    check_makehole_damage,
    check_server_side_effects,
    check_missing_keybind_hints,
    check_set_player_health_order,
    # New checks
    check_server_only_in_client,
    check_per_tick_rpc,
    check_missing_version2,
    check_info_txt,
    check_shoot_missing_attribution,
    check_queryshot_player_guard,
    check_explosion_no_player_damage,
    check_missing_interactive,
    check_per_tick_spatial,
    check_setplayer_arg_order,
    check_damage_no_attacker,
    lint_source,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lines(findings):
    return [f["line"] for f in findings]


def _checks(findings):
    return [f["check"] for f in findings]


# ===========================================================================
# check_ipairs_iterator
# ===========================================================================

class TestIpairsIterator:
    def test_players_flagged(self):
        src = "for i, p in ipairs(Players()) do\nend"
        findings = check_ipairs_iterator(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "IPAIRS-ITERATOR"
        assert findings[0]["line"] == 1

    def test_players_added_flagged(self):
        src = "for i, p in ipairs(PlayersAdded()) do end"
        findings = check_ipairs_iterator(src)
        assert len(findings) == 1
        assert "PlayersAdded" in findings[0]["detail"]

    def test_players_removed_flagged(self):
        src = "for i, p in ipairs(PlayersRemoved()) do end"
        findings = check_ipairs_iterator(src)
        assert len(findings) == 1
        assert "PlayersRemoved" in findings[0]["detail"]

    def test_correct_iterator_clean(self):
        src = "for p in Players() do\n    print(p)\nend"
        assert check_ipairs_iterator(src) == []

    def test_ipairs_on_table_clean(self):
        src = "for i, v in ipairs(myTable) do end"
        assert check_ipairs_iterator(src) == []

    def test_whitespace_variations(self):
        src = "for i,p in ipairs( Players () ) do end"
        findings = check_ipairs_iterator(src)
        assert len(findings) == 1

    def test_comment_ignored(self):
        # The ipairs call is in a comment
        src = "-- for i, p in ipairs(Players()) do end"
        assert check_ipairs_iterator(src) == []

    def test_multiple_lines(self):
        src = (
            "for p in Players() do\n"
            "    local x = ipairs(PlayersAdded())\n"
            "end"
        )
        findings = check_ipairs_iterator(src)
        assert len(findings) == 1
        assert findings[0]["line"] == 2


# ===========================================================================
# check_raw_key_player
# ===========================================================================

class TestRawKeyPlayer:
    def test_rmb_with_player_flagged(self):
        src = 'if InputPressed("rmb", p) then end'
        findings = check_raw_key_player(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "RAW-KEY-PLAYER"
        assert "rmb" in findings[0]["detail"]

    def test_lmb_with_player_flagged(self):
        src = 'if InputDown("lmb", player) then end'
        findings = check_raw_key_player(src)
        assert len(findings) == 1

    def test_letter_key_with_player_flagged(self):
        src = 'if InputReleased("e", p) then end'
        findings = check_raw_key_player(src)
        assert len(findings) == 1

    def test_usetool_with_player_clean(self):
        # "usetool" is NOT in RAW_KEYS — it's a player-input action key
        src = 'if InputPressed("usetool", p) then end'
        assert check_raw_key_player(src) == []

    def test_interact_with_player_clean(self):
        src = 'if InputDown("interact", p) then end'
        assert check_raw_key_player(src) == []

    def test_rmb_without_player_clean(self):
        # No second arg — this is fine (no player param)
        src = 'if InputPressed("rmb") then end'
        assert check_raw_key_player(src) == []

    def test_comment_ignored(self):
        src = '-- if InputPressed("rmb", p) then end'
        assert check_raw_key_player(src) == []

    def test_multiple_findings_on_one_line(self):
        src = 'local a = InputPressed("lmb", p); local b = InputDown("rmb", p)'
        findings = check_raw_key_player(src)
        assert len(findings) == 2

    def test_f1_key_flagged(self):
        src = 'if InputPressed("f1", p) then end'
        findings = check_raw_key_player(src)
        assert len(findings) == 1

    def test_camerax_with_player_clean(self):
        src = 'local dx = InputDown("camerax", p)'
        assert check_raw_key_player(src) == []


# ===========================================================================
# check_tool_enabled_order
# ===========================================================================

class TestToolEnabledOrder:
    def test_correct_order_clean(self):
        src = 'SetToolEnabled("ak47", true, p)'
        assert check_tool_enabled_order(src) == []

    def test_correct_order_false_clean(self):
        src = 'SetToolEnabled("sword", false, p)'
        assert check_tool_enabled_order(src) == []

    def test_wrong_order_flagged(self):
        src = 'SetToolEnabled(p, "ak47", true)'
        findings = check_tool_enabled_order(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "TOOL-ENABLED-ORDER"

    def test_variable_first_arg_flagged(self):
        src = 'SetToolEnabled(player, "sword", true)'
        findings = check_tool_enabled_order(src)
        assert len(findings) == 1

    def test_comment_ignored(self):
        src = '-- SetToolEnabled(p, "ak47", true)'
        assert check_tool_enabled_order(src) == []

    def test_line_number_correct(self):
        src = "local x = 1\nSetToolEnabled(p, \"gun\", true)\nlocal y = 2"
        findings = check_tool_enabled_order(src)
        assert findings[0]["line"] == 2

    def test_upper_case_constant_clean(self):
        """UPPER_CASE constants like TOOL_ID are accepted as valid string args."""
        src = 'SetToolEnabled(TOOL_ID, true, p)'
        assert check_tool_enabled_order(src) == []

    def test_upper_case_weapon_id_clean(self):
        src = 'SetToolEnabled(WEAPON_ID, false, p)'
        assert check_tool_enabled_order(src) == []

    def test_generic_variable_clean(self):
        """Generic variables (loop vars, table keys) are not flagged."""
        src = 'SetToolEnabled(key, value, playerId)'
        assert check_tool_enabled_order(src) == []

    def test_tool_name_variable_clean(self):
        src = 'SetToolEnabled(toolName, true, p)'
        assert check_tool_enabled_order(src) == []

    def test_playerid_first_flagged(self):
        src = 'SetToolEnabled(playerId, "gun", true)'
        findings = check_tool_enabled_order(src)
        assert len(findings) == 1

    def test_toolid_variable_clean(self):
        """toolId is a tool identifier, not a player — should not be flagged."""
        src = 'SetToolEnabled(toolId, true, p)'
        assert check_tool_enabled_order(src) == []

    def test_weaponid_variable_clean(self):
        src = 'SetToolEnabled(weaponId, true, p)'
        assert check_tool_enabled_order(src) == []


# ===========================================================================
# check_alttool
# ===========================================================================

class TestAlttool:
    def test_alttool_flagged(self):
        src = 'if InputPressed("alttool") then end'
        findings = check_alttool(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "ALTTOOL"
        assert "rmb" in findings[0]["detail"]

    def test_alttool_in_set_flagged(self):
        src = 'SetString("game.tool.alttool", "value")'
        # No: this is NOT the key literal "alttool" by itself — only exact "alttool"
        # The check looks for the string literal "alttool"
        findings = check_alttool(src)
        # "alttool" does not appear as a standalone string literal here
        assert len(findings) == 0

    def test_alttool_string_literal_flagged(self):
        src = 'local key = "alttool"'
        findings = check_alttool(src)
        assert len(findings) == 1

    def test_rmb_clean(self):
        src = 'if InputPressed("rmb") then end'
        assert check_alttool(src) == []

    def test_comment_ignored(self):
        src = '-- InputPressed("alttool")'
        assert check_alttool(src) == []

    def test_line_number_correct(self):
        src = "local x = 1\n-- ok\nInputPressed(\"alttool\")"
        findings = check_alttool(src)
        assert findings[0]["line"] == 3


# ===========================================================================
# check_goto_label
# ===========================================================================

class TestGotoLabel:
    def test_goto_flagged(self):
        src = "goto myLabel"
        findings = check_goto_label(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "GOTO-LABEL"

    def test_label_flagged(self):
        src = "::myLabel::"
        findings = check_goto_label(src)
        assert len(findings) == 1
        assert "label" in findings[0]["detail"].lower()

    def test_clean_code(self):
        src = "local x = getvalue()\nreturn x"
        assert check_goto_label(src) == []

    def test_goto_in_comment_ignored(self):
        src = "-- goto somewhere"
        assert check_goto_label(src) == []

    def test_label_in_comment_ignored(self):
        src = "-- ::myLabel::"
        assert check_goto_label(src) == []

    def test_goto_with_spaces(self):
        src = "    goto   myTarget"
        findings = check_goto_label(src)
        assert len(findings) == 1
        assert findings[0]["line"] == 1


# ===========================================================================
# check_mousedx
# ===========================================================================

class TestMousedx:
    def test_mousedx_flagged(self):
        src = 'local dx = InputDown("mousedx")'
        findings = check_mousedx(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MOUSEDX"
        assert "camerax" in findings[0]["detail"]

    def test_mousedy_flagged(self):
        src = 'local dy = InputDown("mousedy")'
        findings = check_mousedx(src)
        assert len(findings) == 1
        assert "cameray" in findings[0]["detail"]

    def test_camerax_clean(self):
        src = 'local dx = InputDown("camerax")'
        assert check_mousedx(src) == []

    def test_cameray_clean(self):
        src = 'local dy = InputDown("cameray")'
        assert check_mousedx(src) == []

    def test_comment_ignored(self):
        src = '-- local dx = InputDown("mousedx")'
        assert check_mousedx(src) == []

    def test_line_number_correct(self):
        src = "function client.tick(dt)\n    local dx = InputDown(\"mousedx\")\nend"
        findings = check_mousedx(src)
        assert findings[0]["line"] == 2


# ===========================================================================
# check_set_player_transform_client
# ===========================================================================

class TestSetPlayerTransformClient:
    def test_in_client_tick_flagged(self):
        src = (
            "function client.tick(dt)\n"
            "    SetPlayerTransform(p, t)\n"
            "end"
        )
        findings = check_set_player_transform_client(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "SPT-CLIENT"
        assert "client.tick" in findings[0]["detail"]

    def test_in_client_draw_flagged(self):
        src = (
            "function client.draw()\n"
            "    SetPlayerTransform(p, t)\n"
            "end"
        )
        findings = check_set_player_transform_client(src)
        assert len(findings) == 1

    def test_in_server_tick_clean(self):
        src = (
            "function server.tick(dt)\n"
            "    SetPlayerTransform(p, t)\n"
            "end"
        )
        assert check_set_player_transform_client(src) == []

    def test_in_server_init_clean(self):
        src = (
            "function server.init()\n"
            "    SetPlayerTransform(p, t)\n"
            "end"
        )
        assert check_set_player_transform_client(src) == []

    def test_in_helper_function_clean(self):
        # Helper function (no dot) — ambiguous context, should not flag
        src = (
            "function doTeleport(p, t)\n"
            "    SetPlayerTransform(p, t)\n"
            "end"
        )
        assert check_set_player_transform_client(src) == []

    def test_at_top_level_clean(self):
        # Not inside any function
        src = "SetPlayerTransform(p, t)"
        assert check_set_player_transform_client(src) == []

    def test_comment_ignored(self):
        src = (
            "function client.tick(dt)\n"
            "    -- SetPlayerTransform(p, t)\n"
            "end"
        )
        assert check_set_player_transform_client(src) == []

    def test_line_number_correct(self):
        src = (
            "function client.tick(dt)\n"
            "    local x = 1\n"
            "    SetPlayerTransform(p, t)\n"
            "end"
        )
        findings = check_set_player_transform_client(src)
        assert findings[0]["line"] == 3


# ===========================================================================
# check_draw_not_client
# ===========================================================================

class TestDrawNotClient:
    def test_bare_draw_flagged(self):
        src = "function draw()\n    UiText('hi')\nend"
        findings = check_draw_not_client(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "DRAW-NOT-CLIENT"

    def test_client_draw_clean(self):
        src = "function client.draw()\n    UiText('hi')\nend"
        assert check_draw_not_client(src) == []

    def test_other_function_clean(self):
        src = "function server.tick(dt)\nend"
        assert check_draw_not_client(src) == []

    def test_draw_in_comment_ignored(self):
        src = "-- function draw()"
        assert check_draw_not_client(src) == []

    def test_indented_bare_draw_flagged(self):
        # Still top-level despite indentation
        src = "    function draw()\n    end"
        findings = check_draw_not_client(src)
        assert len(findings) == 1

    def test_nested_draw_not_flagged(self):
        # draw defined inside another function is not at top-level depth 0
        src = (
            "function server.init()\n"
            "    function draw()\n"
            "    end\n"
            "end"
        )
        # Nested draw — not at top level, should NOT be flagged
        findings = check_draw_not_client(src)
        assert len(findings) == 0

    def test_some_helper_draw_clean(self):
        # function someHelper.draw() — has a dot prefix, not bare draw
        src = "function someHelper.draw()\nend"
        assert check_draw_not_client(src) == []

    def test_line_number_correct(self):
        src = "local x = 1\nfunction draw()\nend"
        findings = check_draw_not_client(src)
        assert findings[0]["line"] == 2


# ===========================================================================
# lint_source aggregation
# ===========================================================================

class TestLintSource:
    def test_clean_source_no_tier1_findings(self):
        """A well-formed v2 mod produces no tier-1 errors."""
        src = (
            "#version 2\n"
            "function server.init()\n"
            '    RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            "end\n"
            "\n"
            "function server.tick(dt)\n"
            "    for p in PlayersAdded() do\n"
            '        SetToolEnabled("gun", true, p)\n'
            "    end\n"
            "    for p in Players() do\n"
            '        if GetBool("game.tool.gun.trigger." .. p) then\n'
            "            SetPlayerTransform(p, Transform())\n"
            "        end\n"
            "    end\n"
            "end\n"
            "\n"
            "function client.tick(dt)\n"
            '    if InputPressed("usetool") then\n'
            '        ServerCall("fire")\n'
            "    end\n"
            "end\n"
            "\n"
            "function client.draw()\n"
            "    UiText('Score')\n"
            "end\n"
        )
        findings = lint_source(src, "test.lua", tier="1")
        assert findings == []

    def test_fully_clean_source_no_findings(self):
        """A fully-featured v2 mod with all tier-2 best practices produces no findings."""
        src = (
            "#version 2\n"
            "function server.init()\n"
            '    RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            '    SetString("game.tool.gun.ammo.display", "")\n'
            '    SetToolAmmoPickupAmount("gun", 10)\n'
            "end\n"
            "\n"
            "function server.tick(dt)\n"
            "    for p in PlayersAdded() do\n"
            '        SetToolEnabled("gun", true, p)\n'
            '        SetToolAmmo("gun", 30, p)\n'
            "    end\n"
            "    for p in Players() do\n"
            '        if GetBool("game.tool.gun.trigger." .. p) then\n'
            "            SetPlayerTransform(Transform(), p)\n"
            "        end\n"
            "    end\n"
            "end\n"
            "\n"
            "function client.tick(dt)\n"
            '    if InputPressed("usetool") then\n'
            '        ServerCall("fire")\n'
            "    end\n"
            "end\n"
            "\n"
            "function client.draw()\n"
            "    UiText('Score')\n"
            "end\n"
        )
        findings = lint_source(src, "test.lua")
        assert findings == []

    def test_multiple_errors_aggregated(self):
        src = (
            "for i, p in ipairs(Players()) do end\n"   # IPAIRS-ITERATOR
            'InputPressed("rmb", p)\n'                  # RAW-KEY-PLAYER
            "function draw()\nend\n"                    # DRAW-NOT-CLIENT
        )
        findings = lint_source(src, "bad.lua")
        check_ids = {f["check"] for f in findings}
        assert "IPAIRS-ITERATOR" in check_ids
        assert "RAW-KEY-PLAYER" in check_ids
        assert "DRAW-NOT-CLIENT" in check_ids

    def test_filename_set_on_all_findings(self):
        src = (
            "for i, p in ipairs(Players()) do end\n"
            "function draw()\nend\n"
        )
        findings = lint_source(src, "mymod/script.lua")
        assert all(f["file"] == "mymod/script.lua" for f in findings)

    def test_tier_param_accepted(self):
        # Unknown tier string falls back to running all checks
        src = "for i, p in ipairs(Players()) do end"
        findings = lint_source(src, "x.lua", tier="tier1")
        assert len(findings) >= 1

    def test_tier_1_only(self):
        # tier="1" runs only tier-1 checks (IPAIRS-ITERATOR is tier-1)
        src = "for i, p in ipairs(Players()) do end"
        findings = lint_source(src, "x.lua", tier="1")
        assert any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_tier_2_only_no_tier1(self):
        # tier="2" should not produce tier-1 findings like IPAIRS-ITERATOR
        src = "for i, p in ipairs(Players()) do end"
        findings = lint_source(src, "x.lua", tier="2")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_tier_2_only_produces_tier2(self):
        # tier="2" should produce tier-2 findings like MAKEHOLE-DAMAGE
        src = "MakeHole(pos, 1.0, false)"
        findings = lint_source(src, "x.lua", tier="2")
        assert any(f["check"] == "MAKEHOLE-DAMAGE" for f in findings)

    def test_all_checks_appear_in_aggregation(self):
        src = "\n".join([
            "for i, p in ipairs(Players()) do end",      # IPAIRS-ITERATOR
            'InputPressed("rmb", p)',                     # RAW-KEY-PLAYER
            'SetToolEnabled(p, "gun", true)',             # TOOL-ENABLED-ORDER
            'InputPressed("alttool")',                    # ALTTOOL
            "goto myLabel",                               # GOTO-LABEL
            'InputDown("mousedx")',                       # MOUSEDX
            # SPT-CLIENT and DRAW-NOT-CLIENT need function context
        ])
        # Add client context checks
        src += "\nfunction client.tick(dt)\n    SetPlayerTransform(p, t)\nend"
        src += "\nfunction draw()\nend"

        findings = lint_source(src, "full.lua")
        check_ids = {f["check"] for f in findings}
        assert "IPAIRS-ITERATOR" in check_ids
        assert "RAW-KEY-PLAYER" in check_ids
        assert "TOOL-ENABLED-ORDER" in check_ids
        assert "ALTTOOL" in check_ids
        assert "GOTO-LABEL" in check_ids
        assert "MOUSEDX" in check_ids
        assert "SPT-CLIENT" in check_ids
        assert "DRAW-NOT-CLIENT" in check_ids

    def test_finding_structure(self):
        src = "#version 2\nfor i, p in ipairs(Players()) do end"
        findings = lint_source(src, "foo.lua")
        assert len(findings) == 1
        f = findings[0]
        assert set(f.keys()) == {"check", "line", "severity", "file", "detail"}
        assert f["severity"] == "error"
        assert f["file"] == "foo.lua"
        assert isinstance(f["line"], int)
        assert isinstance(f["detail"], str)

    def test_lint_ok_suppresses_finding(self):
        src = "for i, p in ipairs(Players()) do end -- @lint-ok IPAIRS-ITERATOR"
        findings = lint_source(src, "foo.lua", tier="1")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_does_not_suppress_other_checks(self):
        src = 'for i, p in ipairs(Players()) do end -- @lint-ok RAW-KEY-PLAYER'
        findings = lint_source(src, "foo.lua", tier="1")
        assert any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_multiple_checks(self):
        src = 'for i, p in ipairs(Players()) do end -- @lint-ok IPAIRS-ITERATOR, DRAW-NOT-CLIENT'
        findings = lint_source(src, "foo.lua", tier="1")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_case_insensitive(self):
        src = "for i, p in ipairs(Players()) do end -- @lint-ok ipairs-iterator"
        findings = lint_source(src, "foo.lua", tier="1")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_file_suppresses_all_lines(self):
        src = (
            "-- @lint-ok-file IPAIRS-ITERATOR\n"
            "for i, p in ipairs(Players()) do end\n"
            "for j, q in ipairs(PlayersAdded()) do end\n"
        )
        findings = lint_source(src, "foo.lua", tier="1")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_file_does_not_suppress_other_checks(self):
        src = (
            "-- @lint-ok-file RAW-KEY-PLAYER\n"
            "for i, p in ipairs(Players()) do end\n"
        )
        findings = lint_source(src, "foo.lua", tier="1")
        assert any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_file_multiple_checks(self):
        src = (
            "-- @lint-ok-file IPAIRS-ITERATOR, DRAW-NOT-CLIENT\n"
            "for i, p in ipairs(Players()) do end\n"
        )
        findings = lint_source(src, "foo.lua", tier="1")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_file_case_insensitive(self):
        src = (
            "-- @lint-ok-file ipairs-iterator\n"
            "for i, p in ipairs(Players()) do end\n"
        )
        findings = lint_source(src, "foo.lua", tier="1")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)

    def test_lint_ok_file_anywhere_in_file(self):
        src = (
            "for i, p in ipairs(Players()) do end\n"
            "-- @lint-ok-file IPAIRS-ITERATOR\n"
        )
        findings = lint_source(src, "foo.lua", tier="1")
        assert not any(f["check"] == "IPAIRS-ITERATOR" for f in findings)


# ===========================================================================
# Tier-2 checks
# ===========================================================================

# ---------------------------------------------------------------------------
# check_missing_ammo_display
# ---------------------------------------------------------------------------

class TestMissingAmmoDisplay:
    def test_missing_flagged(self):
        src = 'RegisterTool("gun", "Gun", "MOD/vox/gun.vox")'
        findings = check_missing_ammo_display(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-AMMO-DISPLAY"
        assert findings[0]["severity"] == "warn"
        assert "gun" in findings[0]["detail"]

    def test_present_clean(self):
        src = (
            'RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            'SetString("game.tool.gun.ammo.display", "")\n'
        )
        assert check_missing_ammo_display(src) == []

    def test_no_register_tool_clean(self):
        src = 'SetString("game.tool.gun.ammo.display", "")'
        assert check_missing_ammo_display(src) == []

    def test_multiple_tools_one_missing(self):
        src = (
            'RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            'RegisterTool("sword", "Sword", "MOD/vox/sword.vox")\n'
            'SetString("game.tool.gun.ammo.display", "")\n'
        )
        findings = check_missing_ammo_display(src)
        assert len(findings) == 1
        assert "sword" in findings[0]["detail"]

    def test_multiple_tools_both_present_clean(self):
        src = (
            'RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            'RegisterTool("sword", "Sword", "MOD/vox/sword.vox")\n'
            'SetString("game.tool.gun.ammo.display", "")\n'
            'SetString("game.tool.sword.ammo.display", "")\n'
        )
        assert check_missing_ammo_display(src) == []

    def test_line_number_correct(self):
        src = "-- header\nRegisterTool(\"gun\", \"Gun\", \"MOD/vox/gun.vox\")"
        findings = check_missing_ammo_display(src)
        assert findings[0]["line"] == 2

    def test_comment_ignored(self):
        src = '-- RegisterTool("gun", "Gun", "MOD/vox/gun.vox")'
        assert check_missing_ammo_display(src) == []


# ---------------------------------------------------------------------------
# check_missing_tool_ammo
# ---------------------------------------------------------------------------

class TestMissingToolAmmo:
    def test_missing_flagged(self):
        src = 'SetToolEnabled("gun", true, p)'
        findings = check_missing_tool_ammo(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-TOOL-AMMO"
        assert findings[0]["severity"] == "warn"

    def test_both_present_clean(self):
        src = (
            'SetToolEnabled("gun", true, p)\n'
            'SetToolAmmo("gun", 30, p)\n'
        )
        assert check_missing_tool_ammo(src) == []

    def test_no_set_tool_enabled_clean(self):
        src = 'SetToolAmmo("gun", 30, p)'
        assert check_missing_tool_ammo(src) == []

    def test_neither_clean(self):
        src = 'RegisterTool("gun", "Gun", "MOD/vox/gun.vox")'
        assert check_missing_tool_ammo(src) == []


# ---------------------------------------------------------------------------
# check_missing_ammo_pickup
# ---------------------------------------------------------------------------

class TestMissingAmmoPickup:
    def test_missing_flagged(self):
        src = 'RegisterTool("gun", "Gun", "MOD/vox/gun.vox")'
        findings = check_missing_ammo_pickup(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-AMMO-PICKUP"
        assert findings[0]["severity"] == "warn"

    def test_present_clean(self):
        src = (
            'RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            'SetToolAmmoPickupAmount("gun", 10)\n'
        )
        assert check_missing_ammo_pickup(src) == []

    def test_no_register_tool_clean(self):
        src = 'SetToolAmmoPickupAmount("gun", 10)'
        assert check_missing_ammo_pickup(src) == []

    def test_line_number_correct(self):
        src = "-- header\nRegisterTool(\"gun\", \"Gun\", \"MOD/vox/gun.vox\")"
        findings = check_missing_ammo_pickup(src)
        assert findings[0]["line"] == 2


# ---------------------------------------------------------------------------
# check_missing_options_guard
# ---------------------------------------------------------------------------

class TestMissingOptionsGuard:
    def test_missing_flagged(self):
        # optionsOpen exists in the file but is far from the usetool check
        src = (
            "local optionsOpen = data.optionsOpen\n"
            "local a = 1\n"
            "local b = 2\n"
            "local c = 3\n"
            "local d = 4\n"
            'if InputPressed("usetool") then\n'
            "end\n"
        )
        findings = check_missing_options_guard(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-OPTIONS-GUARD"
        assert findings[0]["severity"] == "warn"

    def test_guard_same_line_clean(self):
        src = (
            "local optionsOpen = false\n"
            'if not optionsOpen and InputPressed("usetool") then\n'
            "end\n"
        )
        assert check_missing_options_guard(src) == []

    def test_guard_nearby_clean(self):
        src = (
            "local optionsOpen = false\n"
            "if not optionsOpen then\n"
            '    if InputPressed("usetool") then\n'
            "    end\n"
            "end\n"
        )
        assert check_missing_options_guard(src) == []

    def test_no_options_open_skipped(self):
        # No optionsOpen concept → skip entirely (not our concern)
        src = 'if InputPressed("usetool") then end'
        assert check_missing_options_guard(src) == []

    def test_guard_within_3_lines_clean(self):
        src = (
            "local optionsOpen = data.optionsOpen\n"
            "local x = 1\n"
            "local y = 2\n"
            'if InputPressed("usetool") then\n'
            "end\n"
        )
        assert check_missing_options_guard(src) == []

    def test_guard_too_far_flagged(self):
        src = (
            "local optionsOpen = data.optionsOpen\n"
            "local a = 1\n"
            "local b = 2\n"
            "local c = 3\n"
            "local d = 4\n"
            'if InputPressed("usetool") then\n'
            "end\n"
        )
        findings = check_missing_options_guard(src)
        assert len(findings) == 1

    def test_function_level_early_return_guard(self):
        """Function-level 'if optionsOpen then return end' guards all usetool calls."""
        src = (
            "local optionsOpen = false\n"
            "function clientLocalInput(p, data, dt)\n"
            "    if data.optionsOpen then return end\n"
            "    local cam = GetPlayerCameraTransform(p)\n"
            "    local a = 1\n"
            "    local b = 2\n"
            "    local c = 3\n"
            "    local d = 4\n"
            "    local e = 5\n"
            "    local f = 6\n"
            '    if InputPressed("usetool") then\n'
            "    end\n"
            "end\n"
        )
        assert check_missing_options_guard(src) == []

    def test_function_level_guard_no_return_still_flagged(self):
        """optionsOpen without return at function entry is not a guard."""
        src = (
            "local optionsOpen = false\n"
            "function clientLocalInput(p, data, dt)\n"
            "    local x = data.optionsOpen\n"
            "    local a = 1\n"
            "    local b = 2\n"
            "    local c = 3\n"
            "    local d = 4\n"
            '    if InputPressed("usetool") then\n'
            "    end\n"
            "end\n"
        )
        findings = check_missing_options_guard(src)
        assert len(findings) == 1

    def test_guard_on_next_line_multi_line_if(self):
        """optionsOpen on the next line of a multi-line if condition is valid."""
        src = (
            "local optionsOpen = false\n"
            "function server.tickPlayer(p)\n"
            "    local data = players[p]\n"
            '    if data.fireMode == 1 and InputDown("usetool", p)\n'
            "        and not data.optionsOpen and data.timer <= 0 then\n"
            "        server.doShoot(p)\n"
            "    end\n"
            "end\n"
        )
        assert check_missing_options_guard(src) == []


# ---------------------------------------------------------------------------
# check_missing_options_sync
# ---------------------------------------------------------------------------

class TestMissingOptionsSync:
    def test_missing_flagged(self):
        src = "local optionsOpen = data.optionsOpen"
        findings = check_missing_options_sync(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-OPTIONS-SYNC"
        assert findings[0]["severity"] == "warn"

    def test_present_clean(self):
        src = (
            "local optionsOpen = data.optionsOpen\n"
            "function server.setOptionsOpen(p, v)\n"
            "    data[p].optionsOpen = v\n"
            "end\n"
        )
        assert check_missing_options_sync(src) == []

    def test_no_options_open_clean(self):
        src = "function server.tick(dt)\nend"
        assert check_missing_options_sync(src) == []


# ---------------------------------------------------------------------------
# check_handle_gt_zero
# ---------------------------------------------------------------------------

class TestHandleGtZero:
    def test_flagged(self):
        src = "if handle > 0 then\nend"
        findings = check_handle_gt_zero(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "HANDLE-GT-ZERO"
        assert findings[0]["severity"] == "warn"

    def test_neq_zero_clean(self):
        src = "if handle ~= 0 then\nend"
        assert check_handle_gt_zero(src) == []

    def test_number_comparison_clean(self):
        # Non-handle variable names are excluded from the check
        src = "if count > 0 then\nend"
        findings = check_handle_gt_zero(src)
        assert len(findings) == 0

    def test_dist_excluded(self):
        # dist from UiWorldToPixel is not a handle
        src = "if dist > 0 then\nend"
        assert check_handle_gt_zero(src) == []

    def test_comment_ignored(self):
        src = "-- if handle > 0 then"
        assert check_handle_gt_zero(src) == []

    def test_line_number_correct(self):
        src = "local x = 1\nif body > 0 then\nend"
        findings = check_handle_gt_zero(src)
        assert findings[0]["line"] == 2

    def test_arm_framework_names_excluded(self):
        """ARM framework variables: mag, blend, smoke, decays are numeric."""
        for name in ("mag", "blend", "blendout", "smoke", "decays"):
            src = f"if {name} > 0 then\nend"
            assert check_handle_gt_zero(src) == [], f"{name} should be excluded"

    def test_arm_framework_suffixes_excluded(self):
        """Suffixes like Remaining, Damage, Frame, Temp, Executions are numeric."""
        for var in ("BurstShotsRemaining", "finalDamage", "endFrame", "MagTemp", "shotCombo"):
            src = f"if {var} > 0 then\nend"
            assert check_handle_gt_zero(src) == [], f"{var} should be excluded"

    def test_underscore_prefix_stripped(self):
        """Leading underscores should be stripped for suffix matching."""
        src = "if _thirdExecutions > 0 then\nend"
        assert check_handle_gt_zero(src) == []

    def test_interpolation_t_excluded(self):
        """Single-letter t is a common time/interpolation variable."""
        src = "if t > 0 then\nend"
        assert check_handle_gt_zero(src) == []


# ---------------------------------------------------------------------------
# check_manual_aim
# ---------------------------------------------------------------------------

class TestManualAim:
    def test_query_raycast_alone_no_weapon_clean(self):
        """QueryRaycast without weapon APIs is suppressed (non-aim use)."""
        src = "local hit, dist, normal = QueryRaycast(pos, dir, 100)"
        assert check_manual_aim(src) == []

    def test_query_raycast_with_weapon_api_flagged(self):
        """QueryRaycast in a file with weapon APIs is flagged."""
        src = (
            "local hit, dist, normal = QueryRaycast(pos, dir, 100)\n"
            "Shoot(pos, dir, 'bullet', 1, 100, p, 'gun')\n"
        )
        findings = check_manual_aim(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MANUAL-AIM"
        assert findings[0]["severity"] == "info"

    def test_query_raycast_audit_ok_clean(self):
        """QueryRaycast with @audit-ok aiminfo is suppressed."""
        src = (
            "-- @audit-ok aiminfo\n"
            "local hit = QueryRaycast(pos, dir, 100)\n"
            "Shoot(pos, dir, 'bullet', 1, 100, p, 'gun')\n"
        )
        assert check_manual_aim(src) == []

    def test_get_player_aim_info_present_clean(self):
        src = (
            "local hit, dist, normal = QueryRaycast(pos, dir, 100)\n"
            "local aim = GetPlayerAimInfo(muzzle, 200, p)\n"
        )
        assert check_manual_aim(src) == []

    def test_no_query_raycast_clean(self):
        src = "local aim = GetPlayerAimInfo(muzzle, 200, p)"
        assert check_manual_aim(src) == []

    def test_neither_clean(self):
        src = "function server.tick(dt)\nend"
        assert check_manual_aim(src) == []

    def test_comment_ignored(self):
        src = "-- local hit = QueryRaycast(pos, dir, 100)"
        assert check_manual_aim(src) == []


# ---------------------------------------------------------------------------
# check_makehole_damage
# ---------------------------------------------------------------------------

class TestMakeholeDamage:
    def test_makehole_flagged(self):
        src = "MakeHole(pos, 1.5, false)"
        findings = check_makehole_damage(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MAKEHOLE-DAMAGE"
        assert findings[0]["severity"] == "info"

    def test_multiple_makehole_flagged(self):
        src = "MakeHole(pos, 1.0, false)\nMakeHole(pos2, 2.0, true)"
        findings = check_makehole_damage(src)
        assert len(findings) == 2

    def test_no_makehole_clean(self):
        src = "Shoot(pos, dir, 'bullet', 1, 100, p, 'gun')"
        assert check_makehole_damage(src) == []

    def test_comment_ignored(self):
        src = "-- MakeHole(pos, 1.5, false)"
        assert check_makehole_damage(src) == []

    def test_line_number_correct(self):
        src = "local x = 1\nMakeHole(pos, 1.0, false)"
        findings = check_makehole_damage(src)
        assert findings[0]["line"] == 2


# ---------------------------------------------------------------------------
# check_server_side_effects
# ---------------------------------------------------------------------------

class TestServerSideEffects:
    def test_playsound_in_server_flagged(self):
        src = (
            "function server.handleHit(pos)\n"
            '    PlaySound(LoadSound("boom.ogg"), pos, 1.0)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "SERVER-EFFECT"
        assert "PlaySound" in findings[0]["detail"]
        assert "server.handleHit" in findings[0]["detail"]

    def test_spawnparticle_in_server_flagged(self):
        src = (
            "function server.tick(dt)\n"
            '    SpawnParticle("smoke", pos, vel, 1.0, 0.5)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 1
        assert "SpawnParticle" in findings[0]["detail"]

    def test_pointlight_in_server_flagged(self):
        src = (
            "function server.updateProjectile(p)\n"
            "    PointLight(p.pos, 1, 1, 1, 2)\n"
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 1
        assert "PointLight" in findings[0]["detail"]

    def test_playloop_in_server_flagged(self):
        src = (
            "function server.tick(dt)\n"
            '    PlayLoop(engineSound, pos, 0.5)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 1
        assert "PlayLoop" in findings[0]["detail"]

    def test_server_init_is_info_severity(self):
        """Effects in server.init are INFO (one-time) not WARN (per-frame)."""
        src = (
            "function server.init()\n"
            '    PlaySound(LoadSound("startup.ogg"), pos, 1.0)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 1
        assert findings[0]["severity"] == "info"

    def test_server_tick_is_warn_severity(self):
        """Effects in server.tick are WARN (per-frame)."""
        src = (
            "function server.tick(dt)\n"
            '    PlaySound(shootSnd, pos, 1.0)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 1
        assert findings[0]["severity"] == "warn"

    def test_playsound_in_client_clean(self):
        src = (
            "function client.tick(dt)\n"
            '    PlaySound(LoadSound("boom.ogg"), pos, 1.0)\n'
            "end"
        )
        assert check_server_side_effects(src) == []

    def test_spawnparticle_in_client_clean(self):
        src = (
            "function client.draw()\n"
            '    SpawnParticle("smoke", pos, vel, 1.0)\n'
            "end"
        )
        assert check_server_side_effects(src) == []

    def test_effects_in_helper_function_clean(self):
        src = (
            "function SpawnFireParticles(pos, dir)\n"
            '    SpawnParticle(pos, dir, 1.0)\n'
            "end"
        )
        assert check_server_side_effects(src) == []

    def test_effects_at_top_level_clean(self):
        src = 'PlaySound(LoadSound("click.ogg"), pos, 0.5)'
        assert check_server_side_effects(src) == []

    def test_block_comment_excluded(self):
        src = (
            "function server.tick(dt)\n"
            "    --[[\n"
            '    SpawnParticle("smoke", pos, vel, 1.0)\n'
            "    ]]--\n"
            "end"
        )
        assert check_server_side_effects(src) == []

    def test_line_comment_excluded(self):
        src = (
            "function server.tick(dt)\n"
            '    -- SpawnParticle("smoke", pos, vel, 1.0)\n'
            "end"
        )
        assert check_server_side_effects(src) == []

    def test_multiple_findings(self):
        src = (
            "function server.handleHit(pos)\n"
            '    PlaySound(LoadSound("boom.ogg"), pos, 1.0)\n'
            '    SpawnParticle("smoke", pos, Vec(0,1,0), 1.5)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 2

    def test_mixed_server_client(self):
        src = (
            "function server.tick(dt)\n"
            '    PlaySound(snd, pos, 1.0)\n'
            "end\n"
            "function client.tick(dt)\n"
            '    PlaySound(snd, pos, 1.0)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert len(findings) == 1
        assert "server.tick" in findings[0]["detail"]

    def test_severity_is_warn(self):
        src = (
            "function server.tick(dt)\n"
            '    PlaySound(snd, pos, 1.0)\n'
            "end"
        )
        findings = check_server_side_effects(src)
        assert findings[0]["severity"] == "warn"


# ---------------------------------------------------------------------------
# check_missing_keybind_hints
# ---------------------------------------------------------------------------

class TestMissingKeybindHints:
    def test_two_raw_keys_no_hint_flagged(self):
        src = (
            'if InputPressed("r") then reload() end\n'
            'if InputPressed("f") then flashlight() end\n'
        )
        findings = check_missing_keybind_hints(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-KEYBIND-HINTS"
        assert findings[0]["severity"] == "warn"

    def test_one_raw_key_clean(self):
        # Only one single-letter key — below threshold
        src = 'if InputPressed("r") then reload() end\n'
        assert check_missing_keybind_hints(src) == []

    def test_two_raw_keys_with_hint_clean(self):
        src = (
            'if InputPressed("r") then reload() end\n'
            'if InputPressed("f") then flashlight() end\n'
            'UiText("Press R to reload, F for flashlight")\n'
        )
        assert check_missing_keybind_hints(src) == []

    def test_two_raw_keys_with_lmb_hint_clean(self):
        src = (
            'if InputPressed("r") then reload() end\n'
            'if InputPressed("f") then flashlight() end\n'
            'UiText("LMB to shoot")\n'
        )
        assert check_missing_keybind_hints(src) == []

    def test_three_raw_keys_no_hint_flagged(self):
        src = (
            'if InputPressed("r") then end\n'
            'if InputPressed("f") then end\n'
            'if InputPressed("g") then end\n'
        )
        findings = check_missing_keybind_hints(src)
        assert len(findings) == 1
        assert "3" in findings[0]["detail"]

    def test_no_keys_clean(self):
        src = 'if InputPressed("usetool") then fire() end'
        assert check_missing_keybind_hints(src) == []


# ===========================================================================
# check_set_player_health_order
# ===========================================================================

class TestSetPlayerHealthOrder:
    def test_swapped_args_flagged(self):
        """SetPlayerHealth(p, 1) — variable first, number second — is wrong."""
        src = 'SetPlayerHealth(p, 1)'
        findings = check_set_player_health_order(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "HEALTH-ARG-ORDER"

    def test_correct_order_clean(self):
        """SetPlayerHealth(1, p) — number first, variable second — is correct."""
        src = 'SetPlayerHealth(1, p)'
        assert check_set_player_health_order(src) == []

    def test_two_variables_clean(self):
        """SetPlayerHealth(health, player) — two variables — not flagged."""
        src = 'SetPlayerHealth(health, player)'
        assert check_set_player_health_order(src) == []

    def test_two_numbers_clean(self):
        """SetPlayerHealth(1, 0) — two numbers — not flagged (first is number)."""
        src = 'SetPlayerHealth(1, 0)'
        assert check_set_player_health_order(src) == []

    def test_float_second_arg_flagged(self):
        """SetPlayerHealth(player, 0.5) — float literal second arg."""
        src = 'SetPlayerHealth(player, 0.5)'
        findings = check_set_player_health_order(src)
        assert len(findings) == 1

    def test_in_comment_ignored(self):
        """Commented-out code should not trigger."""
        src = '-- SetPlayerHealth(p, 1)'
        assert check_set_player_health_order(src) == []

    def test_line_number_correct(self):
        src = 'local x = 1\nSetPlayerHealth(p, 1)\nlocal y = 2'
        findings = check_set_player_health_order(src)
        assert findings[0]["line"] == 2


# ===========================================================================
# check_server_only_in_client
# ===========================================================================

class TestServerOnlyInClient:
    def test_shoot_in_client_flagged(self):
        src = (
            "function client.tick(dt)\n"
            '    Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "CLIENT-SERVER-FUNC"
        assert "Shoot" in findings[0]["detail"]
        assert "client.tick" in findings[0]["detail"]

    def test_makehole_in_client_flagged(self):
        src = (
            "function client.tickPlayer(p, dt)\n"
            "    MakeHole(pos, 1.5)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "MakeHole" in findings[0]["detail"]

    def test_explosion_in_client_flagged(self):
        src = (
            "function client.tick(dt)\n"
            "    Explosion(pos, 5)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "Explosion" in findings[0]["detail"]

    def test_disable_player_input_in_client_flagged(self):
        src = (
            "function client.tick(dt)\n"
            "    DisablePlayerInput(p)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "DisablePlayerInput" in findings[0]["detail"]

    def test_shoot_in_server_clean(self):
        src = (
            "function server.tick(dt)\n"
            '    Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
            "end"
        )
        assert check_server_only_in_client(src) == []

    def test_shoot_in_helper_clean(self):
        src = (
            "function doShoot(pos, dir, p)\n"
            '    Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
            "end"
        )
        assert check_server_only_in_client(src) == []

    def test_shoot_at_top_level_clean(self):
        src = 'Shoot(pos, dir, "bullet", 1, 100, p, "gun")'
        assert check_server_only_in_client(src) == []

    def test_method_call_not_api(self):
        """client.Shoot() and server.Shoot() are custom methods, not the Shoot() API."""
        src = (
            "function client.tickPlayer(p, dt)\n"
            "    client.Shoot(data, sharedData, mt, p, WeaponLoc)\n"
            "end"
        )
        assert check_server_only_in_client(src) == []

    def test_method_definition_not_api(self):
        """function client.Shoot() definition should not be flagged."""
        src = (
            "function client.Shoot(data, sharedData, mt, p, WeaponLoc)\n"
            "    PlaySound(shootSnd, pos, 0.6)\n"
            "end"
        )
        assert check_server_only_in_client(src) == []

    def test_multiple_findings(self):
        src = (
            "function client.tick(dt)\n"
            '    Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
            "    MakeHole(pos, 1.5)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 2

    def test_comment_ignored(self):
        src = (
            "function client.tick(dt)\n"
            '    -- Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
            "end"
        )
        assert check_server_only_in_client(src) == []

    def test_severity_is_warn(self):
        src = (
            "function client.tick(dt)\n"
            '    Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
            "end"
        )
        findings = check_server_only_in_client(src)
        assert findings[0]["severity"] == "warn"

    def test_set_body_velocity_in_client_flagged(self):
        src = (
            "function client.tickPlayer(p, dt)\n"
            "    SetBodyVelocity(body, vel)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "SetBodyVelocity" in findings[0]["detail"]

    def test_spawn_fire_in_client_flagged(self):
        src = (
            "function client.tick(dt)\n"
            "    SpawnFire(pos)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "SpawnFire" in findings[0]["detail"]

    def test_set_player_health_in_client(self):
        src = (
            "function client.tick(dt)\n"
            "    SetPlayerHealth(1.0, p)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "SetPlayerHealth" in findings[0]["detail"]

    def test_apply_player_damage_in_client(self):
        src = (
            "function client.tickPlayer(p, dt)\n"
            '    ApplyPlayerDamage(target, 0.5, "sword", p)\n'
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "ApplyPlayerDamage" in findings[0]["detail"]

    def test_set_tool_enabled_in_client(self):
        src = (
            "function client.tick(dt)\n"
            '    SetToolEnabled("gun", true, p)\n'
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "SetToolEnabled" in findings[0]["detail"]

    def test_respawn_player_in_client(self):
        src = (
            "function client.tick(dt)\n"
            "    RespawnPlayer(p)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "RespawnPlayer" in findings[0]["detail"]

    def test_queryshot_in_client_flagged(self):
        """QueryShot() is server-only — flagged in client code."""
        src = (
            "function client.tick(dt)\n"
            "    local hit, dist, shape, player = QueryShot(pos, dir, 100)\n"
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "QueryShot" in findings[0]["detail"]

    def test_spawn_in_client_flagged(self):
        """Spawn() is server-only — flagged in client code."""
        src = (
            "function client.tick(dt)\n"
            '    Spawn("<voxbox/>", Transform())\n'
            "end"
        )
        findings = check_server_only_in_client(src)
        assert len(findings) == 1
        assert "Spawn" in findings[0]["detail"]

    def test_queryshot_in_server_clean(self):
        """QueryShot() in server code — correct."""
        src = (
            "function server.tick(dt)\n"
            "    local hit, dist, shape, player = QueryShot(pos, dir, 100, 0, p)\n"
            "end"
        )
        assert check_server_only_in_client(src) == []


# ===========================================================================
# check_per_tick_rpc
# ===========================================================================

class TestPerTickRpc:
    def test_servercall_in_server_tick_flagged(self):
        src = (
            "function server.tick(dt)\n"
            '    ServerCall("server.doThing")\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "PER-TICK-RPC"
        assert "ServerCall" in findings[0]["detail"]

    def test_clientcall_in_server_tick_flagged(self):
        src = (
            "function server.tick(dt)\n"
            '    ClientCall(0, "client.updatePos", x, y, z)\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert len(findings) == 1
        assert "ClientCall" in findings[0]["detail"]

    def test_servercall_in_client_tick_flagged(self):
        src = (
            "function client.tick(dt)\n"
            '    ServerCall("server.syncPos", x, y, z)\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert len(findings) == 1

    def test_servercall_in_update_flagged(self):
        src = (
            "function server.update(dt)\n"
            '    ServerCall("server.doThing")\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert len(findings) == 1

    def test_servercall_in_tickplayer_flagged(self):
        src = (
            "function server.tickPlayer(p, dt)\n"
            '    ClientCall(p, "client.sync", x)\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert len(findings) == 1

    def test_servercall_in_init_clean(self):
        src = (
            "function server.init()\n"
            '    ServerCall("server.setup")\n'
            "end"
        )
        assert check_per_tick_rpc(src) == []

    def test_servercall_in_helper_clean(self):
        src = (
            "function onFire(p, x, y, z)\n"
            '    ServerCall("server.fire", p, x, y, z)\n'
            "end"
        )
        assert check_per_tick_rpc(src) == []

    def test_servercall_at_top_level_clean(self):
        src = 'ServerCall("server.doThing")'
        assert check_per_tick_rpc(src) == []

    def test_comment_ignored(self):
        src = (
            "function server.tick(dt)\n"
            '    -- ServerCall("server.doThing")\n'
            "end"
        )
        assert check_per_tick_rpc(src) == []

    def test_severity_is_warn(self):
        src = (
            "function client.tick(dt)\n"
            '    ServerCall("server.sync")\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert findings[0]["severity"] == "warn"

    def test_input_guard_clean(self):
        src = (
            "function client.tick(dt)\n"
            '    if InputPressed("usetool") then\n'
            '        ServerCall("server.onFire", p, x, y, z)\n'
            "    end\n"
            "end"
        )
        assert check_per_tick_rpc(src) == []

    def test_one_time_event_clean(self):
        src = (
            "function server.tick(dt)\n"
            '    ClientCall(0, "client.onExplode", pos)\n'
            "    already_exploded = true\n"
            "end"
        )
        assert check_per_tick_rpc(src) == []

    def test_makehole_nearby_clean(self):
        """MakeHole within ±10 lines means impact event, not per-tick RPC."""
        src = (
            "function server.tick(dt)\n"
            "    MakeHole(hitPos, 0.5, 0.5, 0.5)\n"
            '    ClientCall(0, "client.onHitSparks", hitPos)\n'
            "end"
        )
        assert check_per_tick_rpc(src) == []

    def test_explosion_nearby_clean(self):
        """Explosion within ±10 lines means impact event, not per-tick RPC."""
        src = (
            "function server.tick(dt)\n"
            "    Explosion(hitPos, 2.5)\n"
            '    ClientCall(0, "client.onBigBoom", hitPos)\n'
            "end"
        )
        assert check_per_tick_rpc(src) == []

    def test_commented_makehole_still_flags(self):
        """Commented-out MakeHole should NOT suppress the finding."""
        src = (
            "function server.tick(dt)\n"
            "    --MakeHole(hitPos, 0.5, 0.5, 0.5)\n"
            '    ClientCall(0, "client.onEffect", hitPos)\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert len(findings) == 1

    def test_makehole_far_away_still_flags(self):
        """MakeHole >10 lines away should NOT suppress the finding."""
        padding = "\n".join(f"    local x{i} = {i}" for i in range(15))
        src = (
            "function server.tick(dt)\n"
            "    MakeHole(pos, 1, 1, 1)\n"
            f"{padding}\n"
            '    ClientCall(0, "client.onEffect", pos)\n'
            "end"
        )
        findings = check_per_tick_rpc(src)
        assert len(findings) == 1


# ===========================================================================
# check_missing_version2
# ===========================================================================

class TestMissingVersion2:
    def test_v2_patterns_without_header_flagged(self):
        src = (
            "function server.init()\n"
            '    RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            "end"
        )
        findings = check_missing_version2(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-VERSION2"
        assert findings[0]["severity"] == "error"
        assert findings[0]["line"] == 1

    def test_with_header_clean(self):
        src = (
            "#version 2\n"
            "function server.init()\n"
            '    RegisterTool("gun", "Gun", "MOD/vox/gun.vox")\n'
            "end"
        )
        assert check_missing_version2(src) == []

    def test_no_v2_patterns_clean(self):
        src = (
            "function init()\n"
            "    local x = 1\n"
            "end"
        )
        assert check_missing_version2(src) == []

    def test_players_in_server_func_without_header_flagged(self):
        src = (
            "function server.tick(dt)\n"
            "    for p in Players() do end\n"
            "end"
        )
        findings = check_missing_version2(src)
        assert len(findings) == 1

    def test_client_without_header_flagged(self):
        src = (
            "function client.tick(dt)\n"
            "    local x = 1\n"
            "end"
        )
        findings = check_missing_version2(src)
        assert len(findings) == 1

    def test_header_with_whitespace_clean(self):
        src = (
            "  #version 2\n"
            "function server.init()\nend"
        )
        assert check_missing_version2(src) == []

    def test_include_file_defining_players_clean(self):
        """player.lua include defines Players() — should not be flagged."""
        src = (
            "function Players()\n"
            "    return iter(GetAllPlayers())\n"
            "end"
        )
        assert check_missing_version2(src) == []


# ===========================================================================
# check_info_txt
# ===========================================================================

class TestCheckInfoTxt:
    def test_missing_version2_with_v2_lua(self, tmp_path):
        """info.txt without version=2 when lua has #version 2."""
        mod_dir = tmp_path / "test_mod"
        mod_dir.mkdir()
        (mod_dir / "info.txt").write_text("name = Test Mod\nauthor = Me\n")
        (mod_dir / "main.lua").write_text("#version 2\nfunction server.init()\nend\n")
        findings = check_info_txt(mod_dir)
        checks = [f["check"] for f in findings]
        assert "INFO-MISSING-VERSION2" in checks
        # Should be error severity
        version_finding = [f for f in findings if f["check"] == "INFO-MISSING-VERSION2"][0]
        assert version_finding["severity"] == "error"

    def test_with_version2_clean(self, tmp_path):
        """info.txt with version=2 should be clean."""
        mod_dir = tmp_path / "test_mod"
        mod_dir.mkdir()
        (mod_dir / "info.txt").write_text("name = Test Mod\nversion = 2\n")
        (mod_dir / "main.lua").write_text("#version 2\nfunction server.init()\nend\n")
        findings = check_info_txt(mod_dir)
        checks = [f["check"] for f in findings]
        assert "INFO-MISSING-VERSION2" not in checks

    def test_missing_name_warned(self, tmp_path):
        """info.txt without name field should warn."""
        mod_dir = tmp_path / "test_mod"
        mod_dir.mkdir()
        (mod_dir / "info.txt").write_text("version = 2\nauthor = Me\n")
        findings = check_info_txt(mod_dir)
        checks = [f["check"] for f in findings]
        assert "INFO-MISSING-NAME" in checks

    def test_no_info_txt_errors(self, tmp_path):
        """Missing info.txt should error."""
        mod_dir = tmp_path / "test_mod"
        mod_dir.mkdir()
        findings = check_info_txt(mod_dir)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-INFO-TXT"

    def test_v1_mod_without_version2_clean(self, tmp_path):
        """v1 mod (no #version 2 in lua) should NOT flag missing version=2 in info.txt."""
        mod_dir = tmp_path / "test_mod"
        mod_dir.mkdir()
        (mod_dir / "info.txt").write_text("name = Test Mod\nauthor = Me\n")
        (mod_dir / "main.lua").write_text("function init()\nend\n")
        findings = check_info_txt(mod_dir)
        checks = [f["check"] for f in findings]
        assert "INFO-MISSING-VERSION2" not in checks


# ---------------------------------------------------------------------------
# SHOOT-NO-ATTRIB (Check 22)
# ---------------------------------------------------------------------------

class TestShootMissingAttribution:
    def test_full_7_param_clean(self):
        src = 'Shoot(pos, dir, "bullet", 1, 100, p, "gun")'
        assert check_shoot_missing_attribution(src) == []

    def test_missing_player_and_toolid_flagged(self):
        src = 'Shoot(r, Vec(0, -1, 0), "rocket", 4, 5000)'
        findings = check_shoot_missing_attribution(src)
        assert len(findings) == 1
        assert "SHOOT-NO-ATTRIB" in findings[0]["check"]

    def test_missing_toolid_only_flagged(self):
        src = 'Shoot(pos, dir, "bullet", 1, 100, p)'
        findings = check_shoot_missing_attribution(src)
        assert len(findings) == 1

    def test_nested_vec_args_counted_correctly(self):
        src = 'Shoot(VecAdd(pos, Vec(1,2,3)), Vec(0,-1,0), "rocket", 4, 5000, p, "gun")'
        assert check_shoot_missing_attribution(src) == []

    def test_user_defined_shoot_skipped(self):
        src = (
            "function Shoot(p, data)\n"
            "    -- custom shoot\n"
            "end\n"
            "Shoot(p, data)\n"
        )
        assert check_shoot_missing_attribution(src) == []

    def test_qualified_method_skipped(self):
        src = 'server.Shoot(playerId)'
        assert check_shoot_missing_attribution(src) == []

    def test_commented_out_ignored(self):
        src = '-- Shoot(pos, dir, "bullet", 1, 100)'
        assert check_shoot_missing_attribution(src) == []

    def test_severity_is_info(self):
        src = 'Shoot(r, Vec(0,-1,0), "rocket", 4, 5000)'
        findings = check_shoot_missing_attribution(src)
        assert findings[0]["severity"] == "info"

    def test_multiple_calls_multiple_findings(self):
        src = (
            'Shoot(r1, Vec(0,-1,0), "rocket", 4, 5000)\n'
            'Shoot(r2, Vec(0,-1,0), "bullet", 1, 5000)\n'
        )
        findings = check_shoot_missing_attribution(src)
        assert len(findings) == 2


# ===========================================================================
# T1-11: QueryShot player=0 truthy guard (Issue #47)
# ===========================================================================

class TestQueryShotPlayerGuard:
    """Detect `if player then ApplyPlayerDamage` without ~= 0 guard."""

    def test_single_line_truthy_guard_flagged(self):
        src = 'if player then ApplyPlayerDamage(player, 2.0, "tool", p) end'
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "QUERYSHOT-PLAYER-GUARD"

    def test_multi_line_truthy_guard_flagged(self):
        src = (
            'if hit then\n'
            '    if player then\n'
            '        ApplyPlayerDamage(player, damage, "tool", p)\n'
            '    end\n'
            'end\n'
        )
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 1

    def test_neq_zero_guard_clean(self):
        src = 'if player ~= 0 then ApplyPlayerDamage(player, 2.0, "tool", p) end'
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 0

    def test_multi_line_neq_zero_clean(self):
        src = (
            'if hit then\n'
            '    if player ~= 0 then\n'
            '        ApplyPlayerDamage(player, damage, "tool", p)\n'
            '    end\n'
            'end\n'
        )
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 0

    def test_different_variable_names(self):
        src = 'if shotPlayer then ApplyPlayerDamage(shotPlayer, 1.0, "beam", p) end'
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 1

    def test_hookplayer_variable(self):
        src = 'if hookPlayer then ApplyPlayerDamage(hookPlayer, 0.5, "hook", p) end'
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 1

    def test_gt_zero_guard_clean(self):
        src = 'if player > 0 then ApplyPlayerDamage(player, 2.0, "tool", p) end'
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 0

    def test_no_apply_player_damage_clean(self):
        src = 'if player then SetPlayerHealth(1, player) end'
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 0

    def test_severity_is_error(self):
        src = 'if player then ApplyPlayerDamage(player, 2.0, "tool", p) end'
        findings = check_queryshot_player_guard(src)
        assert findings[0]["severity"] == "error"

    def test_and_condition_truthy_flagged(self):
        src = (
            'if player and not playerHit then\n'
            '    ApplyPlayerDamage(player, 2.0, "tool", p)\n'
            'end\n'
        )
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 1

    def test_nested_condition_with_proper_outer_guard(self):
        """player used as func arg in nested if, but outer if has ~= 0 guard."""
        src = (
            'if player ~= 0 then\n'
            '    if GetPlayerHealth(player) < 0.21 and GetPlayerHealth(player) > 0 then\n'
            '        ApplyPlayerDamage(player, 1, "loc@DAMAGE_CAUSE_EXPLOSION", 0)\n'
            '    end\n'
            'end\n'
        )
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 0

    def test_function_arg_not_flagged_as_truthy(self):
        """player inside GetPlayerHealth(player) is a function arg, not a truthy check."""
        src = (
            'if GetPlayerHealth(player) > 0 then\n'
            '    ApplyPlayerDamage(player, 1, "tool", p)\n'
            'end\n'
        )
        findings = check_queryshot_player_guard(src)
        assert len(findings) == 0


# ===========================================================================
# check_explosion_no_player_damage
# ===========================================================================

class TestExplosionNoPlayerDamage:
    def test_explosion_without_damage_in_weapon_mod_flagged(self):
        """Weapon mod using Explosion() without ApplyPlayerDamage → flagged."""
        src = (
            'function server.init()\n'
            '    RegisterTool("bomb", "Bomb", "MOD/bomb.xml")\n'
            'end\n'
            'function server.tick(dt)\n'
            '    Explosion(pos, 3)\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "EXPLOSION-NO-DAMAGE"
        assert findings[0]["line"] == 5

    def test_explosion_with_apply_player_damage_clean(self):
        """Weapon mod with Explosion + ApplyPlayerDamage → clean."""
        src = (
            'function server.init()\n'
            '    RegisterTool("bomb", "Bomb", "MOD/bomb.xml")\n'
            'end\n'
            'function server.tick(dt)\n'
            '    Explosion(pos, 3)\n'
            '    ApplyPlayerDamage(target, 1.0, "bomb", p)\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 0

    def test_explosion_with_shoot_still_flags(self):
        """Weapon mod with Explosion + Shoot but no ApplyPlayerDamage → flags.

        Shoot() handles direct-hit projectile damage but NOT splash damage
        from Explosion(). ApplyPlayerDamage with distance falloff is needed
        for area-of-effect damage (Issue #56 miss in Multiple_Grenade_Launcher).
        """
        src = (
            'function server.init()\n'
            '    RegisterTool("rpg", "RPG", "MOD/rpg.xml")\n'
            'end\n'
            'function server.tick(dt)\n'
            '    Explosion(pos, 3)\n'
            '    Shoot(pos, dir, "rocket", 1, 100, p, "rpg")\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "EXPLOSION-NO-DAMAGE"

    def test_explosion_with_shoot_and_damage_clean(self):
        """Weapon mod with Explosion + Shoot + ApplyPlayerDamage → clean."""
        src = (
            'function server.init()\n'
            '    RegisterTool("rpg", "RPG", "MOD/rpg.xml")\n'
            'end\n'
            'function server.tick(dt)\n'
            '    Explosion(pos, 3)\n'
            '    Shoot(pos, dir, "rocket", 1, 100, p, "rpg")\n'
            '    ApplyPlayerDamage(target, dmg, "rpg", p)\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 0

    def test_no_register_tool_clean(self):
        """Non-weapon script (no RegisterTool) with Explosion → clean."""
        src = (
            'function server.tick(dt)\n'
            '    Explosion(pos, 3)\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 0

    def test_audit_ok_suppression_clean(self):
        """@audit-ok explosion annotation suppresses the check."""
        src = (
            '-- @audit-ok explosion (weather effect, not weapon)\n'
            'function server.init()\n'
            '    RegisterTool("weather", "Weather", "MOD/weather.xml")\n'
            'end\n'
            'function server.tick(dt)\n'
            '    Explosion(pos, 1)\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 0

    def test_explosion_in_comment_ignored(self):
        """Explosion in a comment should not be flagged."""
        src = (
            'function server.init()\n'
            '    RegisterTool("bomb", "Bomb", "MOD/bomb.xml")\n'
            'end\n'
            'function server.tick(dt)\n'
            '    -- Explosion(pos, 3)\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 0

    def test_multiple_explosions_flagged(self):
        """Multiple Explosion calls → multiple findings."""
        src = (
            'function server.init()\n'
            '    RegisterTool("bomb", "Bomb", "MOD/bomb.xml")\n'
            'end\n'
            'function server.tick(dt)\n'
            '    Explosion(pos, 3)\n'
            '    Explosion(pos2, 5)\n'
            'end\n'
        )
        findings = check_explosion_no_player_damage(src)
        assert len(findings) == 2
        assert findings[0]["line"] == 5
        assert findings[1]["line"] == 6


# ===========================================================================
# check_missing_interactive
# ===========================================================================

class TestMissingInteractive:
    def test_options_button_without_interactive_flagged(self):
        """optionsOpen + UiTextButton but no UiMakeInteractive → flagged."""
        src = (
            'if data.optionsOpen then\n'
            '    UiPush()\n'
            '    UiTextButton("Close")\n'
            '    UiPop()\n'
            'end\n'
        )
        findings = check_missing_interactive(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "MISSING-INTERACTIVE"

    def test_options_button_with_interactive_clean(self):
        """optionsOpen + UiMakeInteractive + UiTextButton → clean."""
        src = (
            'if data.optionsOpen then\n'
            '    UiMakeInteractive()\n'
            '    UiPush()\n'
            '    UiTextButton("Close")\n'
            '    UiPop()\n'
            'end\n'
        )
        findings = check_missing_interactive(src)
        assert len(findings) == 0

    def test_no_options_open_clean(self):
        """No optionsOpen reference → clean."""
        src = (
            'UiTextButton("Click me")\n'
        )
        findings = check_missing_interactive(src)
        assert len(findings) == 0

    def test_no_button_clean(self):
        """optionsOpen but no UiTextButton → clean."""
        src = (
            'if data.optionsOpen then\n'
            '    UiPush()\n'
            '    UiText("Info only")\n'
            '    UiPop()\n'
            'end\n'
        )
        findings = check_missing_interactive(src)
        assert len(findings) == 0

    def test_settings_open_variant_flagged(self):
        """settingsOpen variant also detected."""
        src = (
            'if data.settingsOpen then\n'
            '    UiPush()\n'
            '    UiTextButton("Save")\n'
            '    UiPop()\n'
            'end\n'
        )
        findings = check_missing_interactive(src)
        assert len(findings) == 1

    def test_reports_first_button_line(self):
        """Finding should report the first UiTextButton line."""
        src = (
            'if data.optionsOpen then\n'
            '    UiPush()\n'
            '    UiText("Title")\n'
            '    UiTextButton("Option A")\n'
            '    UiTextButton("Option B")\n'
            '    UiPop()\n'
            'end\n'
        )
        findings = check_missing_interactive(src)
        assert len(findings) == 1
        assert findings[0]["line"] == 4

    def test_commented_interactive_still_flagged(self):
        """Commented-out UiMakeInteractive should NOT suppress the warning."""
        src = (
            'if data.optionsOpen then\n'
            '    -- UiMakeInteractive()\n'
            '    UiPush()\n'
            '    UiTextButton("Close")\n'
            '    UiPop()\n'
            'end\n'
        )
        findings = check_missing_interactive(src)
        assert len(findings) == 1


# ===========================================================================
# check_per_tick_spatial
# ===========================================================================

class TestPerTickSpatial:
    def test_find_shapes_in_server_tick_flagged(self):
        """FindShapes inside server.tick → flagged."""
        src = (
            'function server.tick(dt)\n'
            '    local shapes = FindShapes("tag", true)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "PER-TICK-SPATIAL"
        assert findings[0]["line"] == 2

    def test_find_shapes_in_client_tick_flagged(self):
        """FindShapes inside client.tick → flagged."""
        src = (
            'function client.tick(dt)\n'
            '    local shapes = FindShapes("tag", true)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 1

    def test_find_shapes_in_server_update_flagged(self):
        """FindShapes inside server.update (60Hz) → flagged."""
        src = (
            'function server.update(dt)\n'
            '    local shapes = FindShapes("tag", true)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 1

    def test_find_shapes_in_server_init_clean(self):
        """FindShapes in server.init (one-time) → clean."""
        src = (
            'function server.init()\n'
            '    local shapes = FindShapes("tag", true)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 0

    def test_find_shapes_at_top_level_clean(self):
        """FindShapes at top level (not in a function) → clean."""
        src = (
            'local shapes = FindShapes("tag", true)\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 0

    def test_query_aabb_bodies_flagged(self):
        """QueryAabbBodies in server.tick → flagged."""
        src = (
            'function server.tick(dt)\n'
            '    local bodies = QueryAabbBodies(min, max)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 1

    def test_query_aabb_shapes_flagged(self):
        """QueryAabbShapes in server.tick → flagged."""
        src = (
            'function server.tick(dt)\n'
            '    local s = QueryAabbShapes(min, max)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 1

    def test_find_bodies_flagged(self):
        """FindBodies in client.update → flagged."""
        src = (
            'function client.update(dt)\n'
            '    local bodies = FindBodies("tag", true)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 1

    def test_throttled_with_timer_clean(self):
        """FindShapes with nearby throttle timer → clean."""
        src = (
            'function server.tick(dt)\n'
            '    shapeTimer = shapeTimer + dt\n'
            '    if shapeTimer > 0.25 then\n'
            '        shapeTimer = 0\n'
            '        local shapes = FindShapes("tag", true)\n'
            '    end\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 0

    def test_throttled_with_cache_keyword_clean(self):
        """FindShapes with nearby cache keyword → clean."""
        src = (
            'function server.tick(dt)\n'
            '    if not cached then\n'
            '        cached = true\n'
            '        local shapes = FindShapes("tag", true)\n'
            '    end\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 0

    def test_in_comment_ignored(self):
        """FindShapes in a comment → clean."""
        src = (
            'function server.tick(dt)\n'
            '    -- FindShapes("tag", true)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 0

    def test_tick_player_flagged(self):
        """FindShapes in server.tickPlayer → flagged."""
        src = (
            'function server.tickPlayer(p, dt)\n'
            '    local shapes = FindShapes("tag", true)\n'
            'end\n'
        )
        findings = check_per_tick_spatial(src)
        assert len(findings) == 1


# ---------------------------------------------------------------------------
# SETPLAYER-ARG-ORDER
# ---------------------------------------------------------------------------


class TestSetPlayerArgOrder:

    def test_correct_order_clean(self):
        """SetPlayerVelocity(vel, p) — correct order, no findings."""
        src = 'SetPlayerVelocity(vel, p)\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 0

    def test_swapped_velocity(self):
        """SetPlayerVelocity(p, vel) — player first = swapped."""
        src = 'SetPlayerVelocity(p, vel)\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "SETPLAYER-ARG-ORDER"

    def test_swapped_transform(self):
        """SetPlayerTransform(player, tr) — player first = swapped."""
        src = 'SetPlayerTransform(player, Transform())\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 1

    def test_swapped_color(self):
        """SetPlayerColor(playerId, r, g, b) — player first = swapped."""
        src = 'SetPlayerColor(playerId, 1, 0, 0)\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 1

    def test_correct_color_clean(self):
        """SetPlayerColor(1, 0, 0, p) — correct order."""
        src = 'SetPlayerColor(1, 0, 0, p)\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 0

    def test_non_player_name_clean(self):
        """SetPlayerVelocity(vel, p) where first arg is not player-like."""
        src = 'SetPlayerVelocity(thrust, p)\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 0

    def test_swapped_walking_speed(self):
        """SetPlayerWalkingSpeed(pid, 1.5) — player first = swapped."""
        src = 'SetPlayerWalkingSpeed(pid, 1.5)\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 1

    def test_comment_ignored(self):
        """Commented-out line should not trigger."""
        src = '-- SetPlayerVelocity(p, vel)\n'
        findings = check_setplayer_arg_order(src)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# DAMAGE-NO-ATTACKER
# ---------------------------------------------------------------------------


class TestDamageNoAttacker:

    def test_4_args_clean(self):
        """ApplyPlayerDamage(target, dmg, toolId, attacker) — correct."""
        src = 'ApplyPlayerDamage(target, 0.5, "gun", p)\n'
        findings = check_damage_no_attacker(src)
        assert len(findings) == 0

    def test_3_args_missing_attacker(self):
        """ApplyPlayerDamage(target, dmg, toolId) — missing attacker."""
        src = 'ApplyPlayerDamage(target, 0.5, "gun")\n'
        findings = check_damage_no_attacker(src)
        assert len(findings) == 1
        assert findings[0]["check"] == "DAMAGE-NO-ATTACKER"

    def test_2_args_missing_both(self):
        """ApplyPlayerDamage(target, dmg) — missing toolId and attacker."""
        src = 'ApplyPlayerDamage(target, 0.5)\n'
        findings = check_damage_no_attacker(src)
        assert len(findings) == 1

    def test_nested_function_call(self):
        """ApplyPlayerDamage with nested fn call shouldn't miscount commas."""
        src = 'ApplyPlayerDamage(target, math.max(0.1, dmg), "gun", p)\n'
        findings = check_damage_no_attacker(src)
        assert len(findings) == 0

    def test_environmental_attacker_zero(self):
        """ApplyPlayerDamage(t, d, "env", 0) — attacker=0 is valid."""
        src = 'ApplyPlayerDamage(player, 1, "loc@DAMAGE_CAUSE_EXPLOSION", 0)\n'
        findings = check_damage_no_attacker(src)
        assert len(findings) == 0

    def test_comment_ignored(self):
        """Commented-out line should not trigger."""
        src = '-- ApplyPlayerDamage(target, 0.5)\n'
        findings = check_damage_no_attacker(src)
        assert len(findings) == 0

    def test_multiline_4_args_clean(self):
        """Multi-line ApplyPlayerDamage with 4 args → clean."""
        src = (
            'ApplyPlayerDamage(\n'
            '    shotPlayer,\n'
            '    1 * 0.25 * factor,\n'
            '    "Fragmentation",\n'
            '    p.owner\n'
            ')\n'
        )
        findings = check_damage_no_attacker(src)
        assert len(findings) == 0

    def test_multiline_3_args_flagged(self):
        """Multi-line ApplyPlayerDamage with 3 args → missing attacker."""
        src = (
            'ApplyPlayerDamage(\n'
            '    shotPlayer,\n'
            '    1 * 0.25,\n'
            '    "Fragmentation"\n'
            ')\n'
        )
        findings = check_damage_no_attacker(src)
        assert len(findings) == 1
