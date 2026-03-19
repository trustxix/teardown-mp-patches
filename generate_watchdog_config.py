"""Generate watchdog_config.json for the terminal watchdog."""
import json
import sys
from pathlib import Path

project = Path(__file__).parent
mode = sys.argv[1] if len(sys.argv) > 1 else "full"

FULL_ROLES = [
    ("qa_lead", "QA Lead", "ROLE_QA_LEAD.md"),
    ("api_surgeon", "API Surgeon", "ROLE_API_SURGEON.md"),
    ("mod_converter", "Mod Converter", "ROLE_MOD_CONVERTER.md"),
    ("docs_keeper", "Docs Keeper", "ROLE_DOCS_KEEPER.md"),
]

MAINT_ROLES = [
    ("qa_lead", "QA Lead", "ROLE_QA_LEAD.md"),
    ("maintainer", "Maintainer", "ROLE_MAINTAINER.md"),
]

roles = FULL_ROLES if mode == "full" else MAINT_ROLES

config = {
    "terminals": [
        {
            "role": role,
            "title": title,
            "command": (
                f"cd {project}; claude --dangerously-skip-permissions "
                f"'Read {role_file} and start your autonomous work loop. "
                f"You are {role}. Run tools.status first, then read "
                f"docs/OFFICIAL_DEVELOPER_DOCS.md. Then get_focus, check_inbox, "
                f"and get_task. Keep working forever.'"
            ),
        }
        for role, title, role_file in roles
    ]
}

out = project / "watchdog_config.json"
out.write_text(json.dumps(config, indent=2), encoding="utf-8")
print(f"  [OK] watchdog_config.json ({len(roles)} terminals)")
