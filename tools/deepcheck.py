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

            if full_path.exists():
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
_GET_PLAYER_TOOL_ID_RE = re.compile(r'GetPlayerTool\s*\([^)]*\)\s*==\s*"([^"]+)"')
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
_SERVERCALL_RE = re.compile(r'ServerCall\s*\(\s*"([^"]+)"')
_CLIENTCALL_RE = re.compile(r'ClientCall\s*\(\s*([^,]+),\s*"([^"]+)"')
_SHOOT_CALL_RE = re.compile(r'\bShoot\s*\(')
_QUERYSHOT_CALL_RE = re.compile(r'\bQueryShot\s*\(')
_APPLY_DAMAGE_RE = re.compile(r'\bApplyPlayerDamage\s*\(')
_USETOOL_INPUT_RE = re.compile(r'Input(?:Pressed|Down)\s*\(\s*"usetool"')
_PLAYSOUND_RE = re.compile(r'\bPlaySound\s*\(')
_SPAWNPARTICLE_RE = re.compile(r'\bSpawnParticle\s*\(')
_POINTLIGHT_RE = re.compile(r'\bPointLight\s*\(')
_EXPLOSION_RE = re.compile(r'\bExplosion\s*\(')


def _extract_functions(source: str) -> dict[str, str]:
    """Extract function name -> body mapping from Lua source.

    Uses depth tracking with Lua block counting from lint.py approach.
    Handles the tricky case where 'if x then return end' is a single-line
    block (opens and closes on the same line).
    """
    funcs: dict[str, str] = {}
    lines = source.splitlines()

    # Find all top-level function definitions and their line numbers
    func_starts: list[tuple[str, int]] = []
    for m in _FUNC_DEF_RE.finditer(source):
        func_name = m.group(1)
        start_line = source[:m.start()].count('\n')
        func_starts.append((func_name, start_line))

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
    return func_name.startswith('client.')


def _is_server_context(func_name: str) -> bool:
    return func_name.startswith('server.')


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

    funcs = _extract_functions(all_source)

    # Find ServerCall targets from client functions that handle usetool
    servercall_targets: list[str] = []
    for func_name, body in funcs.items():
        if _is_client_context(func_name) and _USETOOL_INPUT_RE.search(body):
            targets = _SERVERCALL_RE.findall(body)
            servercall_targets.extend(targets)

    # Check for Shoot() in client context (wrong side)
    for func_name, body in funcs.items():
        if _is_client_context(func_name):
            if _SHOOT_CALL_RE.search(body) and _USETOOL_INPUT_RE.search(body):
                findings.append(ChainFinding(
                    validator="FIRING-CHAIN", status="FAIL",
                    detail=f"Shoot() called in client function {func_name} — must be on server",
                    chain=[func_name, "Shoot()"],
                ))

    # If no ServerCall targets found
    if not servercall_targets:
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
                    if api_re.search(body):
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

    # If server has damage but no ClientCall → silent weapon
    if not clientcall_targets:
        # Only warn if there are no FAIL findings (server-side effects already reported)
        server_fails = [f for f in findings if f.status == "FAIL"]
        if not server_fails:
            findings.append(ChainFinding(
                validator="EFFECT-CHAIN", status="WARN",
                detail="Server has Shoot/Explosion but no ClientCall — weapon may be silent (no sound/particles for other players)",
                chain=["Shoot()", "no ClientCall"],
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

_SERVERCALL_FULL_RE = re.compile(r'ServerCall\s*\(\s*"([^"]+)"\s*([^)]*)\)')


def check_servercall_params(mod_dir: Path) -> list[Finding]:
    """Verify ServerCall targets exist and argument counts match."""
    findings: list[Finding] = []
    all_source = ""
    for _, source in read_lua_files(mod_dir):
        all_source += source + "\n"

    funcs = _extract_functions(all_source)

    for m in _SERVERCALL_FULL_RE.finditer(all_source):
        target = m.group(1)
        args_str = m.group(2).strip()

        # Count args (split by comma, accounting for nested parens)
        if args_str:
            # Simple comma split — good enough for most cases
            call_args = [a.strip() for a in args_str.split(",") if a.strip()]
        else:
            call_args = []

        if target not in funcs:
            findings.append(Finding(
                validator="SERVERCALL-PARAMS", status="FAIL",
                detail=f'ServerCall target "{target}" does not exist',
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
