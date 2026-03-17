"""Team Dashboard Server — visual overview of all terminals, tasks, and project health.

Run: python dashboard/server.py
Opens: http://localhost:8420
"""

import json
import glob
import os
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse

PROJECT = Path(__file__).parent.parent
MODS_DIR = Path("C:/Users/trust/Documents/Teardown/mods")
COMMS = PROJECT / ".comms"
TASKS_FILE = PROJECT / "mcp_task_server" / "tasks.json"
ARCHIVE_FILE = PROJECT / "mcp_task_server" / "tasks_archive.json"
CHANGES_FILE = PROJECT / "mcp_change_tracker" / "changes.json"

# Cache lint results (expensive to run)
_lint_cache = {"data": None, "time": 0}
LINT_CACHE_SECONDS = 30


def get_inboxes():
    roles = ["qa_lead", "api_surgeon", "mod_converter", "docs_keeper"]
    # Also detect dynamic roles
    if COMMS.exists():
        for d in COMMS.iterdir():
            if d.is_dir() and (d / "inbox").is_dir() and d.name not in roles and d.name != "__pycache__":
                roles.append(d.name)
    result = {}
    for role in roles:
        inbox = COMMS / role / "inbox"
        outbox = COMMS / role / "outbox"
        msgs = list(inbox.glob("*.md")) if inbox.exists() else []
        sent = list(outbox.glob("*.md")) if outbox.exists() else []
        urgent = 0
        for m in msgs:
            try:
                h = m.read_text(encoding="utf-8", errors="replace")[:300]
                if "priority: critical" in h or "priority: high" in h:
                    urgent += 1
            except:
                pass
        result[role] = {"inbox": len(msgs), "outbox": len(sent), "urgent": urgent}
    return result


def get_tasks():
    if not TASKS_FILE.exists():
        return {"active": [], "open": [], "counts": {}, "by_role": {}}
    data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])

    open_t = [t for t in tasks if t["status"] == "open"]
    progress = [t for t in tasks if t["status"] == "in_progress"]
    done = [t for t in tasks if t["status"] == "done"]
    pending_review = [t for t in tasks if t.get("review_status") == "pending"]

    by_role = {}
    for t in tasks:
        r = t["role"]
        by_role.setdefault(r, {"open": 0, "in_progress": 0, "done": 0})
        by_role[r][t["status"]] = by_role[r].get(t["status"], 0) + 1

    # Count archived too
    archived_count = 0
    if ARCHIVE_FILE.exists():
        try:
            arch = json.loads(ARCHIVE_FILE.read_text(encoding="utf-8"))
            archived_count = len(arch.get("archived", []))
        except:
            pass

    return {
        "open": [{"id": t["id"], "title": t["title"], "role": t["role"], "priority": t.get("priority", "medium")} for t in open_t],
        "in_progress": [{"id": t["id"], "title": t["title"], "role": t.get("assigned_to", t["role"]), "started": t.get("started_at", "")} for t in progress],
        "done_count": len(done) + archived_count,
        "pending_review": len(pending_review),
        "total": len(tasks) + archived_count,
        "by_role": by_role,
    }


def get_lint():
    now = time.time()
    if _lint_cache["data"] and (now - _lint_cache["time"]) < LINT_CACHE_SECONDS:
        return _lint_cache["data"]

    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.lint"],
            capture_output=True, text=True,
            cwd=str(PROJECT), timeout=30,
        )
        output = result.stdout + result.stderr
        fail = output.count("[FAIL]")
        warn = output.count("[WARN]")
        info = output.count("[INFO]")

        # Get summary line
        summary = ""
        for line in output.strip().split("\n"):
            if "mods scanned" in line:
                summary = line.strip()

        data = {"FAIL": fail, "WARN": warn, "INFO": info, "summary": summary}
        _lint_cache["data"] = data
        _lint_cache["time"] = now
        return data
    except:
        return {"FAIL": "?", "WARN": "?", "INFO": "?", "summary": "lint unavailable"}


def get_focus():
    fp = COMMS / "FOCUS.md"
    if fp.exists():
        content = fp.read_text(encoding="utf-8", errors="replace")
        for line in content.split("\n"):
            if line.startswith("## Focus:"):
                return line.replace("## Focus:", "").strip()
    return "Not set"


def get_mod_stats():
    if not MODS_DIR.exists():
        return {"total": 0, "with_options": 0, "with_hints": 0}

    total = 0
    with_options = 0
    with_hints = 0

    for mod_dir in MODS_DIR.iterdir():
        main = mod_dir / "main.lua"
        if not main.exists():
            continue
        total += 1
        try:
            src = main.read_text(encoding="utf-8", errors="replace")
            if "optionsOpen" in src or "optionsopen" in src or "settingsOpen" in src:
                with_options += 1
            if "UiText(" in src and ("Fire" in src or "Reload" in src or "Options" in src):
                with_hints += 1
        except:
            pass

    return {"total": total, "with_options": with_options, "with_hints": with_hints}


def get_killswitch():
    return (COMMS / "STOP").exists()


def get_changes():
    if not CHANGES_FILE.exists():
        return {"total": 0, "undocumented": 0, "recent": []}
    try:
        data = json.loads(CHANGES_FILE.read_text(encoding="utf-8"))
        changes = data.get("changes", [])
        undoc = [c for c in changes if not c.get("documented", False)]
        recent = sorted(changes, key=lambda c: c.get("timestamp", ""), reverse=True)[:5]
        return {"total": len(changes), "undocumented": len(undoc), "recent": recent}
    except:
        return {"total": 0, "undocumented": 0, "recent": []}


def get_servers():
    mcp_json = PROJECT / ".mcp.json"
    if not mcp_json.exists():
        return []
    try:
        data = json.loads(mcp_json.read_text(encoding="utf-8"))
        servers = []
        for name, config in data.get("mcpServers", {}).items():
            script = config.get("args", [""])[0] if config.get("args") else ""
            exists = Path(script).exists() if script else False
            servers.append({"name": name, "script": os.path.basename(script), "exists": exists})
        return servers
    except:
        return []


def build_api_response():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "killswitch": get_killswitch(),
        "focus": get_focus(),
        "inboxes": get_inboxes(),
        "tasks": get_tasks(),
        "lint": get_lint(),
        "mods": get_mod_stats(),
        "changes": get_changes(),
        "servers": get_servers(),
    }


DASHBOARD_HTML_FILE = Path(__file__).parent / "index.html"




class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            data = build_api_response()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = DASHBOARD_HTML_FILE.read_text(encoding="utf-8")
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress request logging


def main():
    port = 8420
    server = HTTPServer(("localhost", port), DashboardHandler)
    print(f"Dashboard running at http://localhost:{port}")
    print("Press Ctrl+C to stop")

    # Open in browser
    def open_browser():
        time.sleep(1)
        webbrowser.open(f"http://localhost:{port}")

    Thread(target=open_browser, daemon=True).start()
    server.serve_forever()


if __name__ == "__main__":
    main()
