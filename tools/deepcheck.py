"""Deep semantic analysis for Teardown v2 mods.

Traces code logic chains, validates assets, cross-references IDs.
Complements lint.py (single-line regex) with multi-function analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from tools.common import read_lua_files


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    """Single finding from a deepcheck validator."""
    validator: str
    status: str  # PASS, FAIL, WARN, INCONCLUSIVE
    detail: str
    line: int = 0
    file: str = ""

    def to_dict(self) -> dict:
        return {
            "check": self.validator,
            "line": self.line,
            "severity": {"FAIL": "error", "WARN": "warn", "PASS": "info",
                         "INCONCLUSIVE": "info"}.get(self.status, "info"),
            "file": self.file,
            "detail": self.detail,
        }


@dataclass
class AssetFinding(Finding):
    """Asset validation finding."""
    path: str = ""


@dataclass
class ChainFinding(Finding):
    """Chain validation finding (firing, effect, HUD)."""
    chain: list[str] = field(default_factory=list)


@dataclass
class DeepcheckReport:
    """Complete deepcheck results for one mod."""
    mod_name: str
    assets: list[AssetFinding] = field(default_factory=list)
    firing_chain: list[ChainFinding] = field(default_factory=list)
    effect_chain: list[ChainFinding] = field(default_factory=list)
    hud: list[Finding] = field(default_factory=list)
    id_xref: list[Finding] = field(default_factory=list)
    servercall_params: list[Finding] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        all_findings = (
            self.assets + self.firing_chain + self.effect_chain +
            self.hud + self.id_xref + self.servercall_params
        )
        if any(f.status == "FAIL" for f in all_findings):
            return "FAIL"
        if any(f.status == "INCONCLUSIVE" for f in all_findings):
            return "INCONCLUSIVE"
        if any(f.status == "WARN" for f in all_findings):
            return "WARN"
        return "PASS"


# ---------------------------------------------------------------------------
# 1.4 Asset Validator
# ---------------------------------------------------------------------------

_ASSET_REF_RE = re.compile(r'"(MOD/[^"]+\.(?:ogg|vox|png|jpg|xml|kv6))"')


def check_assets(mod_dir: Path) -> list[AssetFinding]:
    """Check that all MOD/ asset references point to existing files."""
    findings = []
    seen: set[str] = set()

    for rel_path, source in read_lua_files(mod_dir):
        for m in _ASSET_REF_RE.finditer(source):
            asset_ref = m.group(1)
            if asset_ref in seen:
                continue
            seen.add(asset_ref)

            local_path = asset_ref.replace("MOD/", "", 1)
            full_path = mod_dir / local_path

            # Also check .tde variant (Teardown's encrypted asset format)
            # Engine transparently loads .ogg.tde when code references .ogg
            tde_path = mod_dir / (local_path + ".tde")

            if full_path.exists() or tde_path.exists():
                findings.append(AssetFinding(
                    validator="ASSET",
                    status="PASS",
                    detail=f"Asset found: {local_path}",
                    file=rel_path,
                    path=local_path,
                ))
            else:
                line_no = 0
                for i, line in enumerate(source.splitlines(), 1):
                    if asset_ref in line:
                        line_no = i
                        break
                findings.append(AssetFinding(
                    validator="ASSET",
                    status="FAIL",
                    detail=f"Asset NOT found: {local_path}",
                    file=rel_path,
                    line=line_no,
                    path=local_path,
                ))

    return findings


# ---------------------------------------------------------------------------
# 1.5 ID Cross-Reference Validator
# ---------------------------------------------------------------------------

_REGISTER_TOOL_ID_RE = re.compile(r'RegisterTool\s*\(\s*"([^"]+)"')
_SET_TOOL_ENABLED_ID_RE = re.compile(r'SetToolEnabled\s*\(\s*"([^"]+)"')
_SET_TOOL_AMMO_ID_RE = re.compile(r'SetToolAmmo\s*\(\s*"([^"]+)"')
_GET_PLAYER_TOOL_ID_RE = re.compile(r'GetPlayerTool\s*\([^)]*\)\s*[~=]=\s*"([^"]+)"')
_AMMO_DISPLAY_ID_RE = re.compile(r'SetString\s*\(\s*"game\.tool\.([^.]+)\.ammo\.display"')


def check_id_xref(mod_dir: Path) -> list[Finding]:
    """Verify tool IDs are consistent across Register/Enable/Ammo/HUD."""
    findings: list[Finding] = []
    all_source = ""
    for _, source in read_lua_files(mod_dir):
        all_source += source + "\n"

    registered_ids = _REGISTER_TOOL_ID_RE.findall(all_source)
    if not registered_ids:
        return []

    enabled_ids = _SET_TOOL_ENABLED_ID_RE.findall(all_source)
    ammo_ids = _SET_TOOL_AMMO_ID_RE.findall(all_source)
    hud_ids = _GET_PLAYER_TOOL_ID_RE.findall(all_source)

    for tool_id in registered_ids:
        # Check SetToolEnabled
        if tool_id not in enabled_ids:
            case_matches = [eid for eid in enabled_ids if eid.lower() == tool_id.lower()]
            if case_matches:
                findings.append(Finding(
                    validator="ID-XREF", status="FAIL",
                    detail=f'Case mismatch: RegisterTool("{tool_id}") vs SetToolEnabled("{case_matches[0]}")',
                ))
            elif not enabled_ids:
                findings.append(Finding(
                    validator="ID-XREF", status="WARN",
                    detail=f'No SetToolEnabled found for "{tool_id}" — tool may not appear for joining players',
                ))
            else:
                findings.append(Finding(
                    validator="ID-XREF", status="FAIL",
                    detail=f'SetToolEnabled uses "{enabled_ids[0]}" but RegisterTool uses "{tool_id}"',
                ))

        # Check SetToolAmmo
        if tool_id not in ammo_ids:
            case_matches = [aid for aid in ammo_ids if aid.lower() == tool_id.lower()]
            if case_matches:
                findings.append(Finding(
                    validator="ID-XREF", status="FAIL",
                    detail=f'Case mismatch: RegisterTool("{tool_id}") vs SetToolAmmo("{case_matches[0]}")',
                ))
            else:
                findings.append(Finding(
                    validator="ID-XREF", status="WARN",
                    detail=f'No SetToolAmmo found for "{tool_id}" — tool may not appear in toolbar',
                ))

        # Check GetPlayerTool in HUD
        if hud_ids and tool_id not in hud_ids:
            case_matches = [hid for hid in hud_ids if hid.lower() == tool_id.lower()]
            if case_matches:
                findings.append(Finding(
                    validator="ID-XREF", status="FAIL",
                    detail=f'Case mismatch: RegisterTool("{tool_id}") vs GetPlayerTool check "{case_matches[0]}"',
                ))

    return findings


# ---------------------------------------------------------------------------
# Lua function extraction helpers
# ---------------------------------------------------------------------------

_FUNC_DEF_RE = re.compile(r'^\s*function\s+([\w.]+)\s*\(([^)]*)\)', re.MULTILINE)
# Also match assignment-style: name.func = function(params)
_FUNC_ASSIGN_RE = re.compile(r'^\s*([\w.]+)\s*=\s*function\s*\(([^)]*)\)', re.MULTILINE)
_SERVERCALL_RE = re.compile(r'ServerCall\s*\(\s*"([^"]+)"')
_CLIENTCALL_RE = re.compile(r'ClientCall\s*\(\s*([^,]+),\s*"([^"]+)"')
_SHOOT_CALL_RE = re.compile(r'(?<!\.)\bShoot\s*\(')
_QUERYSHOT_CALL_RE = re.compile(r'(?<!\.)\bQueryShot\s*\(')
_APPLY_DAMAGE_RE = re.compile(r'(?<!\.)\bApplyPlayerDamage\s*\(')
_USETOOL_INPUT_RE = re.compile(r'Input(?:Pressed|Down)\s*\(\s*"usetool"')
_PLAYSOUND_RE = re.compile(r'(?<!\.)\bPlaySound\s*\(')
_SPAWNPARTICLE_RE = re.compile(r'(?<!\.)\bSpawnParticle\s*\(')
_POINTLIGHT_RE = re.compile(r'(?<!\.)\bPointLight\s*\(')
_EXPLOSION_RE = re.compile(r'(?<!\.)\bExplosion\s*\(')


def _extract_functions(source: str) -> dict[str, str]:
    """Extract function name -> body mapping from Lua source.

    Uses depth tracking with Lua block counting from lint.py approach.
    Handles the tricky case where 'if x then return end' is a single-line
    block (opens and closes on the same line).
    """
    funcs: dict[str, str] = {}
    lines = source.splitlines()

    # Find all top-level function definitions and their line numbers
    # Handles both: function name() and name = function()
    func_starts: list[tuple[str, int]] = []
    for m in _FUNC_DEF_RE.finditer(source):
        func_name = m.group(1)
        start_line = source[:m.start()].count('\n')
        func_starts.append((func_name, start_line))
    for m in _FUNC_ASSIGN_RE.finditer(source):
        func_name = m.group(1)
        start_line = source[:m.start()].count('\n')
        func_starts.append((func_name, start_line))
    # Sort by line number so body extraction works correctly
    func_starts.sort(key=lambda x: x[1])

    for idx, (func_name, start_line) in enumerate(func_starts):
        # The function body ends either at the next top-level function or at a matching 'end'
        # Use the next function's line as a hard stop
        if idx + 1 < len(func_starts):
            max_line = func_starts[idx + 1][1]
        else:
            max_line = len(lines)

        depth = 1
        body_lines = []
        for i in range(start_line + 1, max_line):
            line = lines[i]
            stripped = line.strip()
            # Skip empty lines and comments for block counting
            code = stripped.split('--')[0].strip() if '--' in stripped else stripped

            # Count openers on this line
            opens = 0
            opens += len(re.findall(r'\bfunction\b', code))
            opens += len(re.findall(r'\bif\b', code))
            opens += len(re.findall(r'\bfor\b', code))
            opens += len(re.findall(r'\bwhile\b', code))
            opens += len(re.findall(r'\brepeat\b', code))

            # Count closers on this line
            closes = 0
            closes += len(re.findall(r'\bend\b', code))
            closes += len(re.findall(r'\buntil\b', code))

            depth += opens - closes

            if depth <= 0:
                break
            body_lines.append(line)
        funcs[func_name] = '\n'.join(body_lines)

    return funcs


def _is_client_context(func_name: str) -> bool:
    """Check if function runs in client context.
    Matches: client.tick, client.draw, clientTickPlayer, clientGetHit, etc."""
    return func_name.startswith('client.') or func_name.startswith('client')


def _is_server_context(func_name: str) -> bool:
    """Check if function runs in server context.
    Matches: server.tick, server.init, serverTickPlayer, serverShoot, etc."""
    return func_name.startswith('server.') or func_name.startswith('server')


# ---------------------------------------------------------------------------
# 1.1 Firing Chain Validator
# ---------------------------------------------------------------------------

def check_firing_chain(mod_dir: Path) -> list[ChainFinding]:
    """Trace input -> ServerCall -> server handler -> Shoot/damage."""
    findings: list[ChainFinding] = []
    all_source = ""
    for _, source in read_lua_files(mod_dir):
        all_source += source + "\n"

    if not _USETOOL_INPUT_RE.search(all_source):
        return []  # Not a weapon mod

    # Skip firing chain check if mod has @deepcheck-ok firing-chain annotation
    if '@deepcheck-ok firing-chain' in all_source:
        return []

    funcs = _extract_functions(all_source)

    # Detect custom global functions that shadow Teardown API names
    # (e.g., Attack_Drone defines "function Shoot(p, data)" for projectile visuals)
    _api_names = {"Shoot", "QueryShot", "Explosion", "ApplyPlayerDamage"}
    shadowed_apis = {fn for fn in funcs if fn in _api_names}

    # Check if mod has ANY damage APIs — if not, it's a tool mod, not a weapon
    # Exclude calls with @lint-ok annotations (e.g., environmental Explosion)
    def _has_unannotated(regex: re.Pattern[str], source: str) -> bool:
        for m in regex.finditer(source):
            line_start = source.rfind('\n', 0, m.start()) + 1
            line_end = source.find('\n', m.end())
            line = source[line_start:line_end if line_end != -1 else len(source)]
            if '@lint-ok' not in line and '@deepcheck-ok' not in line:
                return True
        return False

    has_any_damage = (_has_unannotated(_SHOOT_CALL_RE, all_source) or
                      _has_unannotated(_QUERYSHOT_CALL_RE, all_source) or
                      _has_unannotated(_APPLY_DAMAGE_RE, all_source) or
                      _has_unannotated(_EXPLOSION_RE, all_source))
    if not has_any_damage:
        return []  # Tool mod with no damage — firing chain N/A

    # Check for server-side usetool handling (valid: action names work with player param on server)
    # Usetool must be in a server function; damage can be in ANY non-client function (helpers count)
    server_has_usetool = False
    server_damage_apis = set()
    for func_name, body in funcs.items():
        if _is_server_context(func_name) and _USETOOL_INPUT_RE.search(body):
            server_has_usetool = True
        # Damage APIs can be in server functions OR non-prefixed helpers
        if not _is_client_context(func_name):
            if _SHOOT_CALL_RE.search(body): server_damage_apis.add("Shoot()")
            if _QUERYSHOT_CALL_RE.search(body): server_damage_apis.add("QueryShot()")
            if _EXPLOSION_RE.search(body): server_damage_apis.add("Explosion()")
            if _APPLY_DAMAGE_RE.search(body): server_damage_apis.add("ApplyPlayerDamage()")
            if re.search(r'\bMakeHole\s*\(', body): server_damage_apis.add("MakeHole()")

    server_has_usetool_and_damage = False
    if server_has_usetool and server_damage_apis:
        server_has_usetool_and_damage = True
        apis = sorted(server_damage_apis)
        findings.append(ChainFinding(
            validator="FIRING-CHAIN", status="PASS",
            detail=f"Complete chain: server handles usetool with {' + '.join(apis)}",
            chain=["server.usetool", *apis],
        ))

    # Find ServerCall targets from client functions that handle usetool
    # Also trace one level of function call indirection (e.g., usetool → client.shoot() → ServerCall)
    servercall_targets: list[str] = []
    for func_name, body in funcs.items():
        if _is_client_context(func_name) and _USETOOL_INPUT_RE.search(body):
            targets = _SERVERCALL_RE.findall(body)
            servercall_targets.extend(targets)
            # Trace calls to other functions and check those for ServerCalls
            for called_fn in re.findall(r'\b((?:client\.)?[\w]+)\s*\(', body):
                if called_fn in funcs:
                    indirect_targets = _SERVERCALL_RE.findall(funcs[called_fn])
                    servercall_targets.extend(indirect_targets)

    # Check for Shoot() in client context (wrong side)
    # Skip if mod defines a custom global "Shoot" function (shadows the API)
    if "Shoot" not in shadowed_apis:
        for func_name, body in funcs.items():
            if _is_client_context(func_name):
                if _SHOOT_CALL_RE.search(body) and _USETOOL_INPUT_RE.search(body):
                    findings.append(ChainFinding(
                        validator="FIRING-CHAIN", status="FAIL",
                        detail=f"Shoot() called in client function {func_name} — must be on server",
                        chain=[func_name, "Shoot()"],
                    ))

    # If no ServerCall targets found from client AND no server-side usetool handling
    if not servercall_targets:
        if server_has_usetool_and_damage:
            return findings  # Server handles it directly — chain is valid

        # Check if server has usetool + damage exists elsewhere in server code (indirect chain)
        server_has_usetool = any(
            _is_server_context(fn) and _USETOOL_INPUT_RE.search(body)
            for fn, body in funcs.items()
        )
        server_has_damage_anywhere = any(
            _is_server_context(fn) and (
                _SHOOT_CALL_RE.search(body) or _EXPLOSION_RE.search(body) or
                _QUERYSHOT_CALL_RE.search(body) or _APPLY_DAMAGE_RE.search(body)
            )
            for fn, body in funcs.items()
        )
        if server_has_usetool and server_has_damage_anywhere:
            # Damage chain exists but through deeper indirect calls — WARN not FAIL
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="WARN",
                detail="Server handles usetool and has damage APIs — chain exists through indirect calls",
                chain=["server.usetool", "...", "damage"],
            ))
            return findings

        # Check for bare (entity) functions that handle both usetool + damage
        # v2 entity scripts use bare functions that run on both server+client;
        # Shoot()/Explosion() only take effect server-side, which is valid
        bare_has_usetool_and_damage = any(
            not _is_client_context(fn) and not _is_server_context(fn) and
            _USETOOL_INPUT_RE.search(body) and (
                _SHOOT_CALL_RE.search(body) or _EXPLOSION_RE.search(body) or
                _QUERYSHOT_CALL_RE.search(body) or _APPLY_DAMAGE_RE.search(body)
            )
            for fn, body in funcs.items()
        )
        if bare_has_usetool_and_damage:
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="WARN",
                detail="Entity script: bare function handles usetool + damage (runs on both sides, damage is server-only)",
                chain=["usetool", "Shoot()/damage", "(entity script)"],
            ))
            return findings

        has_client_shoot = any(
            _SHOOT_CALL_RE.search(body) for fn, body in funcs.items() if _is_client_context(fn)
        )
        if not has_client_shoot:
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="FAIL",
                detail="usetool input detected but no ServerCall to server — weapon won't fire",
                chain=["usetool", "???"],
            ))
        return findings

    # Verify each ServerCall target exists and calls Shoot/damage
    for target in servercall_targets:
        if target not in funcs:
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="FAIL",
                detail=f'ServerCall target "{target}" not found — function does not exist',
                chain=["usetool", f"ServerCall:{target}", "MISSING"],
            ))
            continue

        body = funcs[target]
        has_shoot = _SHOOT_CALL_RE.search(body)
        has_queryshot = _QUERYSHOT_CALL_RE.search(body)
        has_damage = _APPLY_DAMAGE_RE.search(body)

        if has_shoot:
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="PASS",
                detail=f"Complete chain: usetool -> ServerCall -> {target} -> Shoot()",
                chain=["usetool", f"ServerCall:{target}", "Shoot()"],
            ))
        elif has_queryshot and has_damage:
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="PASS",
                detail=f"Complete chain: usetool -> ServerCall -> {target} -> QueryShot+ApplyPlayerDamage",
                chain=["usetool", f"ServerCall:{target}", "QueryShot()", "ApplyPlayerDamage()"],
            ))
        elif has_queryshot:
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="WARN",
                detail=f'{target} calls QueryShot but no ApplyPlayerDamage — may not deal damage',
                chain=["usetool", f"ServerCall:{target}", "QueryShot()", "???"],
            ))
        else:
            findings.append(ChainFinding(
                validator="FIRING-CHAIN", status="WARN",
                detail=f'{target} exists but has no Shoot/QueryShot — may not deal damage',
                chain=["usetool", f"ServerCall:{target}", "???"],
            ))

    return findings


# ---------------------------------------------------------------------------
# 1.2 Effect Chain Validator
# ---------------------------------------------------------------------------

_EFFECT_APIS = [
    ("PlaySound", _PLAYSOUND_RE),
    ("SpawnParticle", _SPAWNPARTICLE_RE),
    ("PointLight", _POINTLIGHT_RE),
]


def check_effect_chain(mod_dir: Path) -> list[ChainFinding]:
    """Trace damage -> ClientCall -> PlaySound/SpawnParticle on client."""
    findings: list[ChainFinding] = []
    all_source = ""
    for _, source in read_lua_files(mod_dir):
        all_source += source + "\n"

    # Check if mod has damage calls at all
    has_shoot = _SHOOT_CALL_RE.search(all_source)
    has_explosion = _EXPLOSION_RE.search(all_source)
    has_queryshot = _QUERYSHOT_CALL_RE.search(all_source)
    if not (has_shoot or has_explosion or has_queryshot):
        return []  # Not a damage-dealing mod

    funcs = _extract_functions(all_source)

    # Check for effect APIs in server functions that ALSO do damage (wrong side)
    # Only flag damage-related server functions — utility functions may legitimately
    # use PlaySound for UI feedback that lint.py's server_side_effects check handles
    for func_name, body in funcs.items():
        if _is_server_context(func_name):
            has_damage = (_SHOOT_CALL_RE.search(body) or _EXPLOSION_RE.search(body) or
                         _QUERYSHOT_CALL_RE.search(body) or _APPLY_DAMAGE_RE.search(body))
            if has_damage:
                for api_name, api_re in _EFFECT_APIS:
                    # Check each matching line — skip if suppressed with @lint-ok
                    unsuppressed = False
                    for line in body.splitlines():
                        stripped = line.strip()
                        if stripped.startswith('--'):
                            continue  # Skip Lua comments
                        if api_re.search(line) and '@lint-ok' not in line:
                            unsuppressed = True
                            break
                    if unsuppressed:
                        findings.append(ChainFinding(
                            validator="EFFECT-CHAIN", status="FAIL",
                            detail=f"{api_name}() called in damage function {func_name} — "
                                   f"effects must be on client (other players won't see/hear them)",
                            chain=[func_name, f"{api_name}()"],
                        ))

    # Find ClientCall targets from server functions that have damage
    clientcall_targets: list[tuple[str, str]] = []  # (target_player, func_name)
    for func_name, body in funcs.items():
        if _is_server_context(func_name):
            if _SHOOT_CALL_RE.search(body) or _EXPLOSION_RE.search(body) or _QUERYSHOT_CALL_RE.search(body):
                for m in _CLIENTCALL_RE.finditer(body):
                    target_player = m.group(1).strip()
                    target_func = m.group(2)
                    clientcall_targets.append((target_player, target_func))

    # If server has damage but no ClientCall → may be silent
    # Shoot() and Explosion() are auto-replicated by the engine (sounds + visuals
    # on all clients), so they don't need explicit ClientCall for effects.
    # Only QueryShot+ApplyPlayerDamage (custom damage) needs explicit ClientCall.
    if not clientcall_targets:
        server_fails = [f for f in findings if f.status == "FAIL"]
        if not server_fails:
            # Only warn if using QueryShot (custom damage) without ClientCall
            if has_queryshot and not has_shoot and not has_explosion:
                findings.append(ChainFinding(
                    validator="EFFECT-CHAIN", status="WARN",
                    detail="Server has QueryShot damage but no ClientCall — weapon may be silent (no sound/particles for other players)",
                    chain=["QueryShot()", "no ClientCall"],
                ))
            elif has_queryshot:
                findings.append(ChainFinding(
                    validator="EFFECT-CHAIN", status="WARN",
                    detail="Server has QueryShot damage but no ClientCall — beam/melee effects may be silent for other players",
                    chain=["QueryShot()", "no ClientCall"],
                ))
        return findings

    # Verify ClientCall targets exist and have effects
    for target_player, target_func in clientcall_targets:
        if target_func not in funcs:
            findings.append(ChainFinding(
                validator="EFFECT-CHAIN", status="FAIL",
                detail=f'ClientCall target "{target_func}" not found — effects function missing',
                chain=[f"ClientCall:{target_func}", "MISSING"],
            ))
            continue

        body = funcs[target_func]
        has_effects = any(api_re.search(body) for _, api_re in _EFFECT_APIS)

        if has_effects:
            findings.append(ChainFinding(
                validator="EFFECT-CHAIN", status="PASS",
                detail=f"Effect chain: damage -> ClientCall -> {target_func} -> effects",
                chain=[f"ClientCall:{target_func}", "effects"],
            ))
        else:
            findings.append(ChainFinding(
                validator="EFFECT-CHAIN", status="WARN",
                detail=f'{target_func} exists but has no PlaySound/SpawnParticle/PointLight',
                chain=[f"ClientCall:{target_func}", "no effects"],
            ))

    return findings


# ---------------------------------------------------------------------------
# 1.3 HUD Validator
# ---------------------------------------------------------------------------

_CLIENT_DRAW_RE = re.compile(r'function\s+client\.draw\s*\(')
_UITEXT_RE = re.compile(r'\bUiText\s*\(')


def check_hud(mod_dir: Path) -> list[Finding]:
    """Check that client.draw() exists and has a tool guard."""
    findings: list[Finding] = []
    all_source = ""
    for _, source in read_lua_files(mod_dir):
        all_source += source + "\n"

    # Only relevant for tool mods
    if not _REGISTER_TOOL_ID_RE.search(all_source):
        return []

    funcs = _extract_functions(all_source)

    # Check client.draw exists
    if "client.draw" not in funcs:
        findings.append(Finding(
            validator="HUD", status="WARN",
            detail="No client.draw() found — tool mod has no HUD",
        ))
        return findings

    draw_body = funcs["client.draw"]

    # Check for GetPlayerTool guard
    has_tool_guard = _GET_PLAYER_TOOL_ID_RE.search(draw_body)
    if not has_tool_guard:
        findings.append(Finding(
            validator="HUD", status="WARN",
            detail="client.draw() has no GetPlayerTool guard — HUD may show for all tools",
        ))
    else:
        findings.append(Finding(
            validator="HUD", status="PASS",
            detail="client.draw() has GetPlayerTool guard",
        ))

    # Check for UiText (has visible content)
    if _UITEXT_RE.search(draw_body):
        findings.append(Finding(
            validator="HUD", status="PASS",
            detail="client.draw() renders UiText",
        ))

    return findings


# ---------------------------------------------------------------------------
# 1.6 ServerCall Parameter Validator
# ---------------------------------------------------------------------------

_SERVERCALL_START_RE = re.compile(r'ServerCall\s*\(\s*"([^"]+)"\s*')


def _extract_balanced_args(source: str, start: int) -> str | None:
    """Extract argument string from source starting after the function name,
    handling nested parentheses correctly."""
    depth = 1  # we're already inside the outer ServerCall(
    i = start
    while i < len(source) and depth > 0:
        ch = source[i]
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return source[start:i]
        elif ch == '"':
            # skip string literals
            i += 1
            while i < len(source) and source[i] != '"':
                if source[i] == '\\':
                    i += 1
                i += 1
        i += 1
    return None


def _split_args_balanced(args_str: str) -> list[str]:
    """Split comma-separated args respecting nested parentheses."""
    args = []
    depth = 0
    current = []
    for ch in args_str:
        if ch == '(' or ch == '{':
            depth += 1
            current.append(ch)
        elif ch == ')' or ch == '}':
            depth -= 1
            current.append(ch)
        elif ch == ',' and depth == 0:
            token = ''.join(current).strip()
            if token:
                args.append(token)
            current = []
        else:
            current.append(ch)
    token = ''.join(current).strip()
    if token:
        args.append(token)
    return args


def check_servercall_params(mod_dir: Path) -> list[Finding]:
    """Verify ServerCall targets exist and argument counts match."""
    findings: list[Finding] = []
    all_source = ""
    for _, source in read_lua_files(mod_dir):
        all_source += source + "\n"

    funcs = _extract_functions(all_source)

    for m in _SERVERCALL_START_RE.finditer(all_source):
        # Skip matches in Lua comments (-- to end of line)
        line_start = all_source.rfind('\n', 0, m.start()) + 1
        line_prefix = all_source[line_start:m.start()]
        if '--' in line_prefix:
            continue
        target = m.group(1)
        # Extract the full argument list with balanced parentheses
        after_name = m.end()
        args_str_raw = _extract_balanced_args(all_source, after_name)
        if args_str_raw is None:
            continue

        # Strip the leading comma separator after the function name string
        args_str = args_str_raw.strip()
        if args_str.startswith(","):
            args_str = args_str[1:].strip()

        # Split args respecting nested parens
        if args_str:
            call_args = _split_args_balanced(args_str)
        else:
            call_args = []

        if target not in funcs:
            # Also check for assignment-style: target = function(...)
            assign_re = re.compile(
                rf'{re.escape(target)}\s*=\s*function\s*\(([^)]*)\)'
            )
            assign_match = assign_re.search(all_source)
            if not assign_match:
                # Check for alias assignment: target = existing_function
                alias_re = re.compile(
                    rf'{re.escape(target)}\s*=\s*([\w.]+)\s*$', re.MULTILINE
                )
                alias_match = alias_re.search(all_source)
                if alias_match:
                    aliased_to = alias_match.group(1)
                    # Valid if aliased to a known function (direct def or in funcs dict)
                    if aliased_to in funcs or re.search(
                        rf'function\s+{re.escape(aliased_to)}\s*\(', all_source
                    ):
                        continue
                findings.append(Finding(
                    validator="SERVERCALL-PARAMS", status="FAIL",
                    detail=f'ServerCall target "{target}" does not exist',
                ))
            # If found via assignment, check param count against call args
            elif assign_match:
                params_str = assign_match.group(1).strip()
                if params_str:
                    func_params = [p.strip() for p in params_str.split(",") if p.strip()]
                else:
                    func_params = []
                if len(call_args) != len(func_params):
                    # Check optional params
                    is_optional = False
                    if len(call_args) < len(func_params):
                        extra = func_params[len(call_args):]
                        # Can't check body easily for assignment funcs, skip
                        is_optional = False
                    if not is_optional:
                        findings.append(Finding(
                            validator="SERVERCALL-PARAMS", status="FAIL",
                            detail=f'ServerCall("{target}") passes {len(call_args)} args '
                                   f'but function expects {len(func_params)} params ({", ".join(func_params)})',
                        ))
            continue

        # Count function params
        func_match = re.search(
            rf'function\s+{re.escape(target)}\s*\(([^)]*)\)',
            all_source
        )
        if func_match:
            params_str = func_match.group(1).strip()
            if params_str:
                func_params = [p.strip() for p in params_str.split(",") if p.strip()]
            else:
                func_params = []

            if len(call_args) != len(func_params):
                # Check for optional params (Lua pattern: param = param or default)
                is_optional_mismatch = False
                if len(call_args) < len(func_params):
                    extra_params = func_params[len(call_args):]
                    func_body = funcs.get(target, "")
                    optional_count = sum(
                        1 for pm in extra_params
                        if re.search(rf'\b{re.escape(pm)}\s*=\s*{re.escape(pm)}\s+or\b', func_body)
                    )
                    if optional_count == len(extra_params):
                        is_optional_mismatch = True
                if not is_optional_mismatch:
                    findings.append(Finding(
                        validator="SERVERCALL-PARAMS", status="FAIL",
                        detail=f'ServerCall("{target}") passes {len(call_args)} args '
                               f'but function expects {len(func_params)} params ({", ".join(func_params)})',
                    ))

    return findings


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def run_deepcheck(mod_dir: Path, is_weapon: bool = True) -> DeepcheckReport:
    """Run all deepcheck validators on a mod and return a report."""
    report = DeepcheckReport(mod_name=mod_dir.name)
    report.assets = check_assets(mod_dir)
    report.id_xref = check_id_xref(mod_dir)
    report.servercall_params = check_servercall_params(mod_dir)
    if is_weapon:
        report.firing_chain = check_firing_chain(mod_dir)
        report.effect_chain = check_effect_chain(mod_dir)
        report.hud = check_hud(mod_dir)
    return report
