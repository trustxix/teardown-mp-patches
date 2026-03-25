"""MCP Template Engine Server — generates lint-clean Lua code from templates.

Eliminates copy-paste errors by producing complete, correct code blocks
with all required patterns (UiMakeInteractive, optionsOpen guard, server sync, etc.).
"""

import json
from mcp.server import FastMCP

mcp = FastMCP(
    name="template-engine",
    instructions="Generates lint-clean Teardown v2 Lua code from templates. Use to create options menus, keybind hints, player data, and server init blocks without copy-paste errors.",
)


@mcp.tool(description="Generate a complete O-key options menu with UiMakeInteractive, server sync, and all guards. Returns Lua code for: createPlayerData addition, server.setOptionsOpen function, O-key handler, client.draw menu, and keybind hint.")
def generate_options_menu(tool_id: str, display_name: str, settings: list[dict]) -> dict:
    """Generate a full options menu.

    tool_id: the RegisterTool id (e.g., "ak47")
    display_name: human-readable name (e.g., "AK-47")
    settings: list of dicts, each with:
        - name: savegame key suffix (e.g., "unlimitedammo" → savegame.mod.unlimitedammo)
        - type: "bool" or "float"
        - label: display text (e.g., "Unlimited Ammo")
        - default: default value
        - min/max: for float type only
    """
    # createPlayerData field
    player_data_field = "\t\toptionsOpen = false,"

    # server.setOptionsOpen function
    server_func = """function server.setOptionsOpen(p, open)
\tlocal data = players[p]
\tif data then data.optionsOpen = open end
end"""

    # O-key handler (goes in client.tickPlayer after isLocal declaration)
    okey_handler = """\tif isLocal and InputPressed("o") then
\t\tdata.optionsOpen = not data.optionsOpen
\t\tServerCall("server.setOptionsOpen", p, data.optionsOpen)
\tend"""

    # Build menu UI
    # Calculate panel height based on settings count
    setting_height = 75  # per setting
    panel_height = 160 + len(settings) * setting_height
    half_height = panel_height // 2

    menu_lines = []
    menu_lines.append(f"\tif data.optionsOpen then")
    menu_lines.append(f"\t\tUiMakeInteractive()")
    menu_lines.append(f"\t\tUiPush()")
    menu_lines.append(f"\t\tUiTranslate(UiCenter(), UiHeight() / 2 - {half_height // 2})")
    menu_lines.append(f"\t\tUiAlign(\"center middle\")")
    menu_lines.append(f"\t\tUiColor(0, 0, 0, 0.85)")
    menu_lines.append(f"\t\tUiRect(360, {panel_height})")
    menu_lines.append(f"\t\tUiColor(1, 1, 1)")
    menu_lines.append(f"\t\tUiFont(\"bold.ttf\", 32)")
    menu_lines.append(f"\t\tUiTranslate(0, -{half_height // 2 - 40})")
    menu_lines.append(f"\t\tUiText(\"{display_name} Options\")")
    menu_lines.append(f"\t\tUiFont(\"regular.ttf\", 24)")

    for i, s in enumerate(settings):
        key = f"savegame.mod.{s['name']}"
        label = s["label"]

        if s["type"] == "bool":
            menu_lines.append(f"\t\tUiTranslate(0, {60 if i == 0 else 50})")
            menu_lines.append(f"\t\tlocal opt_{s['name']} = GetBool(\"{key}\")")
            menu_lines.append(f"\t\tUiText(\"{label}: \" .. (opt_{s['name']} and \"ON\" or \"OFF\"))")
            menu_lines.append(f"\t\tUiTranslate(0, 35)")
            menu_lines.append(f"\t\tUiButtonImageBox(\"ui/common/box-outline-6.png\", 6, 6)")
            menu_lines.append(f"\t\tif UiTextButton(opt_{s['name']} and \"Disable\" or \"Enable\", 120, 30) then")
            menu_lines.append(f"\t\t\tSetBool(\"{key}\", not opt_{s['name']})")
            menu_lines.append(f"\t\tend")

        elif s["type"] == "float":
            mi = s.get("min", 0)
            ma = s.get("max", 100)
            menu_lines.append(f"\t\tUiTranslate(0, {60 if i == 0 else 50})")
            menu_lines.append(f"\t\tlocal opt_{s['name']} = HasKey(\"{key}\") and GetFloat(\"{key}\") or {s['default']}")
            menu_lines.append(f"\t\tUiText(\"{label}: \" .. math.floor(opt_{s['name']} * 100) / 100)")
            menu_lines.append(f"\t\tUiTranslate(0, 35)")
            menu_lines.append(f"\t\tUiButtonImageBox(\"ui/common/box-outline-6.png\", 6, 6)")
            menu_lines.append(f"\t\tif UiTextButton(\"-\", 40, 30) then")
            menu_lines.append(f"\t\t\tSetFloat(\"{key}\", math.max({mi}, opt_{s['name']} - {(ma - mi) / 10:.1f}))")
            menu_lines.append(f"\t\tend")
            menu_lines.append(f"\t\tUiTranslate(50, 0)")
            menu_lines.append(f"\t\tif UiTextButton(\"+\", 40, 30) then")
            menu_lines.append(f"\t\t\tSetFloat(\"{key}\", math.min({ma}, opt_{s['name']} + {(ma - mi) / 10:.1f}))")
            menu_lines.append(f"\t\tend")
            menu_lines.append(f"\t\tUiTranslate(-50, 0)")

    # Close button
    menu_lines.append(f"\t\tUiTranslate(0, 60)")
    menu_lines.append(f"\t\tif UiTextButton(\"Close [O]\", 100, 30) then")
    menu_lines.append(f"\t\t\tdata.optionsOpen = false")
    menu_lines.append(f"\t\t\tServerCall(\"server.setOptionsOpen\", p, false)")
    menu_lines.append(f"\t\tend")
    menu_lines.append(f"\t\tUiPop()")
    menu_lines.append(f"\t\treturn")
    menu_lines.append(f"\tend")

    menu_code = "\n".join(menu_lines)

    # usetool guard snippet
    usetool_guard = 'and not data.optionsOpen'

    return {
        "player_data_field": player_data_field,
        "server_function": server_func,
        "okey_handler": okey_handler,
        "menu_code": menu_code,
        "usetool_guard": usetool_guard,
        "instructions": "1. Add player_data_field to createPlayerData()\n2. Add server_function before server.tick()\n3. Add okey_handler in client.tickPlayer after isLocal\n4. Add 'and not data.optionsOpen' to all positive InputDown/InputPressed(\"usetool\", p) checks\n5. Add menu_code at the top of client.draw() after tool/vehicle check\n6. Run: python -m tools.lint --mod \"ModName\""
    }


@mcp.tool(description="Generate a keybind hints block for client.draw(). Returns complete Lua code.")
def generate_keybind_hints(keybinds: list[dict], position: str = "bottom_left") -> str:
    """Generate keybind hint UI code.

    keybinds: list of dicts with "key" and "action" (e.g., {"key": "LMB", "action": "Fire"})
    position: "bottom_left" (default) or "bottom_center"
    """
    hint_text = "\\n".join(f"{kb['key']} - {kb['action']}" for kb in keybinds)

    if position == "bottom_center":
        return f"""\tUiPush()
\tUiTranslate(UiCenter(), UiHeight() - 30)
\tUiAlign("center middle")
\tUiFont("regular.ttf", 18)
\tUiColor(1, 1, 1)
\tUiTextOutline(0, 0, 0, 1, 0.1)
\tUiText("{hint_text}")
\tUiPop()"""

    y_offset = 60 + len(keybinds) * 20
    return f"""\tUiPush()
\tUiTranslate(10, UiHeight() - {y_offset})
\tUiAlign("left bottom")
\tUiColor(1, 1, 1, 0.8)
\tUiFont("bold.ttf", 20)
\tUiTextOutline(0, 0, 0, 1, 0.1)
\tUiText("{hint_text}")
\tUiPop()"""


@mcp.tool(description="Generate a createPlayerData() function with specified fields. Returns complete Lua code.")
def generate_player_data(fields: list[dict]) -> str:
    """Generate createPlayerData() function.

    fields: list of dicts with "name", "type", "default"
        type: "number", "bool", "string", "vec", "table"
        For tables, default should be a Lua table literal string like "{}"
    """
    lines = ["function createPlayerData()", "\treturn {"]

    type_defaults = {
        "number": "0",
        "bool": "false",
        "string": '""',
        "vec": "Vec()",
        "table": "{}",
    }

    for f in fields:
        name = f["name"]
        default = f.get("default")
        if default is None:
            default = type_defaults.get(f["type"], "nil")
        lines.append(f"\t\t{name} = {default},")

    # Always include optionsOpen
    if not any(f["name"] == "optionsOpen" for f in fields):
        lines.append("\t\toptionsOpen = false,")

    lines.append("\t}")
    lines.append("end")

    return "\n".join(lines)


@mcp.tool(description="Generate a server.init() function with RegisterTool, ammo setup, and display config. Returns complete Lua code.")
def generate_server_init(tool_id: str, display_name: str, vox_path: str, group: int, ammo_pickup: int = 0) -> str:
    """Generate server.init() with all required setup.

    tool_id: RegisterTool id
    display_name: human-readable name
    vox_path: path to vox file (e.g., "MOD/vox/gun.vox")
    group: tool group number (1-6)
    ammo_pickup: ammo crate refill amount (0 for infinite tools)
    """
    return f"""function server.init()
\tRegisterTool("{tool_id}", "{display_name}", "{vox_path}", {group})
\tSetToolAmmoPickupAmount("{tool_id}", {ammo_pickup})
\tSetBool("game.tool.{tool_id}.enabled", true)
\tSetString("game.tool.{tool_id}.ammo.display", "")
end"""


@mcp.tool(description="Generate the full server.tick() boilerplate with PlayersAdded/Removed/Players loops. Returns complete Lua code.")
def generate_server_tick(tool_id: str, ammo_amount: int = 101, extra_init_lines: str = "") -> str:
    """Generate server.tick() with proper iterator loops.

    tool_id: the tool id for SetToolEnabled/SetToolAmmo
    ammo_amount: ammo to set on join (101 = effectively infinite display)
    extra_init_lines: additional Lua lines to run in PlayersAdded (indented with 2 tabs)
    """
    extra = ""
    if extra_init_lines:
        extra = "\n" + extra_init_lines

    return f"""function server.setOptionsOpen(p, open)
\tlocal data = players[p]
\tif data then data.optionsOpen = open end
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tplayers[p] = createPlayerData()
\t\tSetToolEnabled("{tool_id}", true, p)
\t\tSetToolAmmo("{tool_id}", {ammo_amount}, p){extra}
\tend

\tfor p in PlayersRemoved() do
\t\tplayers[p] = nil
\tend

\tfor p in Players() do
\t\tserver.tickPlayer(p, dt)
\tend
end"""


@mcp.tool(description="Generate the client.tick() boilerplate with proper iterator loops. Returns complete Lua code.")
def generate_client_tick() -> str:
    """Generate client.tick() with proper PlayersAdded/Removed/Players loops."""
    return """function client.tick(dt)
\tfor p in PlayersAdded() do
\t\tif not players[p] then
\t\t\tplayers[p] = createPlayerData()
\t\tend
\tend

\tfor p in PlayersRemoved() do
\t\tplayers[p] = nil
\tend

\tfor p in Players() do
\t\tclient.tickPlayer(p, dt)
\tend
end"""


@mcp.tool(description="Generate an ammo display HUD block for client.draw(). Shows ammo/reserve with reload text. Returns Lua code.")
def generate_ammo_display(mag_size: int, show_reload: bool = True) -> str:
    """Generate ammo counter HUD code.

    mag_size: rounds per magazine (for reserve calculation)
    show_reload: whether to show "Reloading" text
    """
    reload_block = ""
    if show_reload:
        reload_block = f"""\tif data.reloading then
\t\tUiText("Reloading")
\telse
\t\tUiText(data.ammo .. "/" .. {mag_size} * math.max(0, data.mags - 1))
\tend"""
    else:
        reload_block = f"\tUiText(data.ammo .. \"/{mag_size}\" .. \" * \" .. math.max(0, data.mags - 1))"

    return f"""\tUiPush()
\tUiTranslate(UiCenter(), UiHeight() - 60)
\tUiAlign("center middle")
\tUiColor(1, 1, 1)
\tUiFont("bold.ttf", 32)
\tUiTextOutline(0, 0, 0, 1, 0.1)
{reload_block}
\tUiPop()"""


if __name__ == "__main__":
    mcp.run(transport="stdio")
