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
