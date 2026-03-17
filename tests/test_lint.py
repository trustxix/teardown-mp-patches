"""Tests for tools/lint.py — tier-1 hard error checks."""

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
    def test_clean_source_no_findings(self):
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
        # tier param is accepted without error (ignored for now)
        src = "for i, p in ipairs(Players()) do end"
        findings = lint_source(src, "x.lua", tier="tier1")
        assert len(findings) >= 1

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
        src = "for i, p in ipairs(Players()) do end"
        findings = lint_source(src, "foo.lua")
        assert len(findings) == 1
        f = findings[0]
        assert set(f.keys()) == {"check", "line", "severity", "file", "detail"}
        assert f["severity"] == "error"
        assert f["file"] == "foo.lua"
        assert isinstance(f["line"], int)
        assert isinstance(f["detail"], str)
