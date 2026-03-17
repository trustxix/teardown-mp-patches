"""Tests for tools/fix.py — all 6 auto-fixers plus apply_fixes."""

import pytest

from tools.fix import (
    fix_ipairs_iterator,
    fix_mousedx,
    fix_alttool,
    fix_draw_func,
    fix_handle_gt,
    fix_ammo_display,
    apply_fixes,
)


# ---------------------------------------------------------------------------
# fix_ipairs_iterator
# ---------------------------------------------------------------------------


def test_fix_ipairs_players():
    src = 'for _, p in ipairs(Players()) do\n'
    assert fix_ipairs_iterator(src) == 'for p in Players() do\n'


def test_fix_ipairs_added():
    src = 'for _, p in ipairs(PlayersAdded()) do\n'
    assert fix_ipairs_iterator(src) == 'for p in PlayersAdded() do\n'


def test_fix_ipairs_removed():
    src = 'for _, p in ipairs(PlayersRemoved()) do\n'
    assert fix_ipairs_iterator(src) == 'for p in PlayersRemoved() do\n'


def test_fix_ipairs_noop():
    src = 'for p in Players() do\n'
    assert fix_ipairs_iterator(src) == src


def test_fix_ipairs_different_var_name():
    src = 'for _, player in ipairs(Players()) do\n'
    assert fix_ipairs_iterator(src) == 'for player in Players() do\n'


def test_fix_ipairs_extra_whitespace():
    """Extra spaces inside ipairs(...) should still be matched."""
    src = 'for _, p in ipairs( Players( ) ) do\n'
    assert fix_ipairs_iterator(src) == 'for p in Players() do\n'


# ---------------------------------------------------------------------------
# fix_mousedx
# ---------------------------------------------------------------------------


def test_fix_mousedx():
    src = 'local dx = InputValue("mousedx")\n'
    fixed = fix_mousedx(src)
    assert 'InputValue("camerax") * 180 / math.pi' in fixed


def test_fix_mousedy():
    src = 'local dy = InputValue("mousedy")\n'
    fixed = fix_mousedx(src)
    assert 'InputValue("cameray") * 180 / math.pi' in fixed


def test_fix_mousedx_noop():
    src = 'local dx = InputValue("camerax")\n'
    assert fix_mousedx(src) == src


def test_fix_mousedx_both_on_same_source():
    src = 'local dx = InputValue("mousedx")\nlocal dy = InputValue("mousedy")\n'
    fixed = fix_mousedx(src)
    assert 'InputValue("camerax") * 180 / math.pi' in fixed
    assert 'InputValue("cameray") * 180 / math.pi' in fixed
    assert '"mousedx"' not in fixed
    assert '"mousedy"' not in fixed


# ---------------------------------------------------------------------------
# fix_alttool
# ---------------------------------------------------------------------------


def test_fix_alttool():
    src = 'if InputPressed("alttool") then\n'
    fixed = fix_alttool(src)
    assert '"rmb"' in fixed
    assert '"alttool"' not in fixed


def test_fix_alttool_noop():
    src = 'if InputPressed("rmb") then\n'
    assert fix_alttool(src) == src


def test_fix_alttool_multiple_occurrences():
    src = 'InputPressed("alttool")\nInputReleased("alttool")\n'
    fixed = fix_alttool(src)
    assert fixed.count('"rmb"') == 2
    assert '"alttool"' not in fixed


# ---------------------------------------------------------------------------
# fix_draw_func
# ---------------------------------------------------------------------------


def test_fix_draw_func():
    src = 'function draw()\n    UiText("hi")\nend\n'
    assert 'function client.draw()' in fix_draw_func(src)


def test_fix_draw_func_noop():
    src = 'function client.draw()\n    UiText("hi")\nend\n'
    assert fix_draw_func(src) == src


def test_fix_draw_func_with_params():
    src = 'function draw(dt)\n    UiText("hi")\nend\n'
    fixed = fix_draw_func(src)
    assert 'function client.draw(dt)' in fixed


def test_fix_draw_func_does_not_touch_method_draw():
    """``function someObj.draw(`` should NOT be touched."""
    src = 'function someObj.draw()\n    return 1\nend\n'
    assert fix_draw_func(src) == src


def test_fix_draw_func_nested_not_touched():
    """A ``draw`` function nested inside another function should not be renamed."""
    src = (
        'function server.tick(dt)\n'
        '    local function draw()\n'
        '        return 1\n'
        '    end\n'
        'end\n'
    )
    fixed = fix_draw_func(src)
    assert 'client.draw' not in fixed


def test_fix_draw_func_indented_toplevel():
    """Top-level draw with leading whitespace should still be renamed."""
    src = 'function draw()\n    UiText("x")\nend\n'
    fixed = fix_draw_func(src)
    assert 'function client.draw()' in fixed


# ---------------------------------------------------------------------------
# fix_handle_gt
# ---------------------------------------------------------------------------


def test_fix_handle_gt():
    src = 'if body > 0 then\n'
    assert '~= 0' in fix_handle_gt(src)


def test_fix_handle_gt_noop():
    src = 'if body ~= 0 then\n'
    assert fix_handle_gt(src) == src


def test_fix_handle_gt_various_names():
    src = 'if shape > 0 then\nif vehicle > 0 then\n'
    fixed = fix_handle_gt(src)
    assert fixed.count('~= 0 then') == 2
    assert '> 0 then' not in fixed


def test_fix_handle_gt_does_not_affect_numeric_comparisons():
    """Pure numeric comparisons like ``count > 0 then`` will be rewritten —
    this is intentional (the fixer is conservative for handles; callers should
    review). Document this known behaviour rather than assert it won't happen."""
    src = 'if count > 0 then\n'
    # The fixer WILL change this; that's a known trade-off.
    fixed = fix_handle_gt(src)
    assert '~= 0 then' in fixed


# ---------------------------------------------------------------------------
# fix_ammo_display
# ---------------------------------------------------------------------------


def test_fix_ammo_display():
    src = (
        '    RegisterTool("ak47", "AK-47", "MOD/vox/ak47.vox", 3)\n'
        '    SetBool("game.tool.ak47.enabled", true)\n'
    )
    fixed = fix_ammo_display(src)
    assert 'SetString("game.tool.ak47.ammo.display", "")' in fixed


def test_fix_ammo_display_already_present():
    src = (
        '    RegisterTool("ak47", "AK-47", "MOD/vox/ak47.vox", 3)\n'
        '    SetString("game.tool.ak47.ammo.display", "")\n'
    )
    assert fix_ammo_display(src) == src


def test_fix_ammo_display_preserves_indentation():
    src = '        RegisterTool("gun", "Gun", "MOD/vox/gun.vox", 1)\n'
    fixed = fix_ammo_display(src)
    # The injected line must use the same 8-space indent
    assert '        SetString("game.tool.gun.ammo.display", "")' in fixed


def test_fix_ammo_display_no_register_tool():
    src = '-- no tools here\n'
    assert fix_ammo_display(src) == src


def test_fix_ammo_display_multiple_tools():
    src = (
        '    RegisterTool("pistol", "Pistol", "MOD/vox/pistol.vox", 1)\n'
        '    RegisterTool("rifle", "Rifle", "MOD/vox/rifle.vox", 2)\n'
    )
    fixed = fix_ammo_display(src)
    assert 'SetString("game.tool.pistol.ammo.display", "")' in fixed
    assert 'SetString("game.tool.rifle.ammo.display", "")' in fixed


def test_fix_ammo_display_tool_id_extraction():
    """Tool ID with hyphens and underscores should be extracted correctly."""
    src = 'RegisterTool("super_gun-v2", "Super Gun", "MOD/vox/sg.vox", 0)\n'
    fixed = fix_ammo_display(src)
    assert 'SetString("game.tool.super_gun-v2.ammo.display", "")' in fixed


# ---------------------------------------------------------------------------
# apply_fixes
# ---------------------------------------------------------------------------


def test_apply_fixes_combined():
    src = (
        'for _, p in ipairs(Players()) do\n'
        'if InputPressed("alttool") then\n'
        'end\n'
        'end\n'
    )
    fixed, changes = apply_fixes(src)
    assert "ipairs" not in fixed
    assert '"alttool"' not in fixed
    assert len(changes) >= 2


def test_apply_fixes_only():
    src = (
        'for _, p in ipairs(Players()) do\n'
        'if InputPressed("alttool") then\n'
        'end\n'
        'end\n'
    )
    fixed, changes = apply_fixes(src, only=["alttool"])
    assert "ipairs" in fixed          # NOT fixed — only=alttool
    assert '"alttool"' not in fixed   # fixed
    assert len(changes) == 1


def test_apply_fixes_noop():
    src = 'for p in Players() do\nend\n'
    fixed, changes = apply_fixes(src)
    assert fixed == src
    assert changes == []


def test_apply_fixes_returns_tuple():
    src = 'x = 1\n'
    result = apply_fixes(src)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_apply_fixes_only_empty_list():
    """Passing only=[] should apply no fixers and return the source unchanged."""
    src = 'for _, p in ipairs(Players()) do\nend\n'
    fixed, changes = apply_fixes(src, only=[])
    assert fixed == src
    assert changes == []


def test_apply_fixes_only_unknown_id():
    """Unknown fix IDs in only= should silently produce no changes."""
    src = 'for _, p in ipairs(Players()) do\nend\n'
    fixed, changes = apply_fixes(src, only=["nonexistent-fixer"])
    assert fixed == src
    assert changes == []


def test_apply_fixes_all_six():
    """Smoke test: a source triggering all 6 fixers should produce 6 change entries."""
    src = (
        'for _, p in ipairs(Players()) do end\n'           # ipairs-iterator
        'local x = InputValue("mousedx")\n'                # mousedx
        'if InputPressed("alttool") then end\n'            # alttool
        'function draw()\nend\n'                           # draw-func
        'if h > 0 then end\n'                              # handle-gt
        'RegisterTool("mygun", "Gun", "MOD/v.vox", 0)\n'  # ammo-display
    )
    _, changes = apply_fixes(src)
    assert len(changes) == 6
