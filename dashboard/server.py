"""Team Dashboard Server — visual overview of all terminals, tasks, and project health.

Run: python dashboard/server.py
Opens: http://localhost:8420
"""

import json
import os
import re
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timedelta, timezone
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
LINT_CACHE_SECONDS = 60


def get_inboxes():
    """Get inbox/outbox counts for each role."""
    roles = ["qa_lead", "api_surgeon", "mod_converter", "docs_keeper"]
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
                h = m.read_text(encoding="utf-8", errors="replace")[:500]
                if "priority: critical" in h or "priority: high" in h:
                    urgent += 1
            except Exception:
                pass
        result[role] = {"inbox": len(msgs), "outbox": len(sent), "urgent": urgent}
    return result


def get_tasks():
    """Get task queue state."""
    if not TASKS_FILE.exists():
        return {"open": [], "in_progress": [], "done_count": 0, "pending_review": 0, "total": 0, "by_role": {}}
    try:
        data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"open": [], "in_progress": [], "done_count": 0, "pending_review": 0, "total": 0, "by_role": {}}

    tasks = data.get("tasks", [])
    open_t = [t for t in tasks if t.get("status") == "open"]
    progress = [t for t in tasks if t.get("status") == "in_progress"]
    done = [t for t in tasks if t.get("status") == "done"]
    pending_review = [t for t in tasks if t.get("review_status") == "pending"]

    by_role = {}
    for t in tasks:
        r = t.get("role", "unknown")
        by_role.setdefault(r, {"open": 0, "in_progress": 0, "done": 0})
        status = t.get("status", "open")
        if status in by_role[r]:
            by_role[r][status] += 1

    archived_count = 0
    if ARCHIVE_FILE.exists():
        try:
            arch = json.loads(ARCHIVE_FILE.read_text(encoding="utf-8"))
            archived_count = len(arch.get("archived", []))
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "open": [{"id": t.get("id", "?"), "title": t.get("title", "?"), "role": t.get("role", "?"), "priority": t.get("priority", "medium")} for t in open_t],
        "in_progress": [{"id": t.get("id", "?"), "title": t.get("title", "?"), "role": t.get("assigned_to", t.get("role", "?")), "started": t.get("started_at", "")} for t in progress],
        "done_count": len(done) + archived_count,
        "pending_review": len(pending_review),
        "total": len(tasks) + archived_count,
        "by_role": by_role,
    }


def get_lint():
    """Run lint and parse results. Cached for LINT_CACHE_SECONDS."""
    now = time.time()
    if _lint_cache["data"] and (now - _lint_cache["time"]) < LINT_CACHE_SECONDS:
        return _lint_cache["data"]

    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.lint", "--json-output"],
            capture_output=True, text=True,
            cwd=str(PROJECT), timeout=60,
        )
        if result.returncode not in (0, 1):
            return {"error": f"lint exited {result.returncode}", "FAIL": 0, "WARN": 0, "INFO": 0, "by_check": {}, "mods_scanned": 0, "mods_clean": 0}

        all_results = json.loads(result.stdout)
        fail = 0
        warn = 0
        info = 0
        by_check = {}
        mods_with_findings = 0

        for mod_name, findings in all_results.items():
            if findings:
                mods_with_findings += 1
            for f in findings:
                sev = f.get("severity", "info")
                check = f.get("check", "UNKNOWN")
                if sev == "error":
                    fail += 1
                elif sev == "warn":
                    warn += 1
                else:
                    info += 1
                by_check[check] = by_check.get(check, 0) + 1

        data = {
            "FAIL": fail,
            "WARN": warn,
            "INFO": info,
            "by_check": by_check,
            "mods_scanned": len(all_results),
            "mods_clean": len(all_results) - mods_with_findings,
        }
        _lint_cache["data"] = data
        _lint_cache["time"] = now
        return data
    except subprocess.TimeoutExpired:
        return {"error": "lint timed out", "FAIL": 0, "WARN": 0, "INFO": 0, "by_check": {}, "mods_scanned": 0, "mods_clean": 0}
    except Exception as e:
        return {"error": str(e), "FAIL": "?", "WARN": "?", "INFO": "?", "by_check": {}, "mods_scanned": 0, "mods_clean": 0}


def get_focus():
    """Read current team focus from FOCUS.md."""
    fp = COMMS / "FOCUS.md"
    if not fp.exists():
        return "Not set"
    try:
        content = fp.read_text(encoding="utf-8", errors="replace")
        for line in content.split("\n"):
            if line.startswith("## Focus:"):
                return line.replace("## Focus:", "").strip()
    except Exception:
        pass
    return "Not set"


def get_mod_stats():
    """Count mods using the same method as discover_mods (info.txt check)."""
    if not MODS_DIR.exists():
        return {"total": 0, "with_v2": 0, "with_options": 0, "with_hints": 0}

    total = 0
    with_v2 = 0
    with_options = 0
    with_hints = 0

    for mod_dir in MODS_DIR.iterdir():
        if not mod_dir.is_dir() or not (mod_dir / "info.txt").exists():
            continue
        total += 1

        # Check info.txt for version = 2
        try:
            info_content = (mod_dir / "info.txt").read_text(encoding="utf-8", errors="replace")
            if re.search(r"version\s*=\s*2", info_content):
                with_v2 += 1
        except Exception:
            pass

        # Check main.lua for features
        main = mod_dir / "main.lua"
        if not main.exists():
            continue
        try:
            src = main.read_text(encoding="utf-8", errors="replace")
            if "optionsOpen" in src or "optionsopen" in src or "settingsOpen" in src:
                with_options += 1
            if "UiText(" in src and ("Fire" in src or "Reload" in src or "Options" in src):
                with_hints += 1
        except Exception:
            pass

    return {"total": total, "with_v2": with_v2, "with_options": with_options, "with_hints": with_hints}


def get_killswitch():
    return (COMMS / "STOP").exists()


def get_changes():
    """Get recent changes from change tracker."""
    if not CHANGES_FILE.exists():
        return {"total": 0, "undocumented": 0, "recent": []}
    try:
        data = json.loads(CHANGES_FILE.read_text(encoding="utf-8"))
        changes = data.get("changes", [])
        undoc = [c for c in changes if not c.get("documented", False)]
        recent = sorted(changes, key=lambda c: c.get("timestamp", ""), reverse=True)[:5]
        return {
            "total": len(changes),
            "undocumented": len(undoc),
            "recent": [
                {
                    "mod": c.get("mod", "?"),
                    "type": c.get("type", "?"),
                    "description": c.get("description", "")[:120],
                    "role": c.get("role", "?"),
                    "timestamp": c.get("timestamp", "")[:16],
                }
                for c in recent
            ],
        }
    except (json.JSONDecodeError, OSError):
        return {"total": 0, "undocumented": 0, "recent": []}


def get_docs():
    """Check which key docs exist and their sizes."""
    docs = [
        ("OFFICIAL_DEVELOPER_DOCS.md", "docs/OFFICIAL_DEVELOPER_DOCS.md"),
        ("MPLIB_INTERNALS.md", "docs/MPLIB_INTERNALS.md"),
        ("PER_TICK_RPC_FIX_GUIDE.md", "docs/PER_TICK_RPC_FIX_GUIDE.md"),
        ("RESEARCH.md", "docs/RESEARCH.md"),
        ("V2_SYNC_PATTERNS.md", "docs/V2_SYNC_PATTERNS.md"),
        ("MP_DESYNC_PATTERNS.md", "docs/MP_DESYNC_PATTERNS.md"),
        ("ISSUES_AND_FIXES.md", "ISSUES_AND_FIXES.md"),
    ]
    result = []
    for name, rel_path in docs:
        full = PROJECT / rel_path
        exists = full.exists()
        size = full.stat().st_size if exists else 0
        result.append({"name": name, "exists": exists, "size": size})
    return result


def get_heartbeats():
    """Read terminal heartbeats."""
    hb_file = COMMS / "heartbeats.json"
    if not hb_file.exists():
        return {}
    try:
        return json.loads(hb_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def get_team_log():
    """Get last 10 entries from team.log."""
    log_file = PROJECT / "team.log"
    if not log_file.exists():
        return []
    try:
        lines = log_file.read_text(encoding="utf-8", errors="replace").strip().split("\n")
        return lines[-10:]  # Last 10 entries
    except Exception:
        return []


def get_errors():
    """Get recent errors from error log."""
    errors_file = PROJECT / "logs" / "errors.json"
    if not errors_file.exists():
        return {"total": 0, "recent": []}
    try:
        errors = json.loads(errors_file.read_text(encoding="utf-8"))
        now = datetime.now(timezone.utc)
        one_hour_ago = (now - timedelta(hours=1)).isoformat()
        recent = [e for e in errors if e.get("timestamp", "") >= one_hour_ago]
        return {"total": len(recent), "recent": recent[-5:]}
    except (json.JSONDecodeError, OSError):
        return {"total": 0, "recent": []}


def get_metrics_data():
    """Get team metrics."""
    try:
        from mcp_task_server import metrics
        return metrics.compute()
    except Exception:
        return {"throughput_per_hour": 0, "avg_time_minutes": 0, "by_role": {}, "completed_in_window": 0}


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
        "docs": get_docs(),
        "heartbeats": get_heartbeats(),
        "team_log": get_team_log(),
        "errors": get_errors(),
        "metrics": get_metrics_data(),
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

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}

        if parsed.path == "/api/task":
            try:
                sys.path.insert(0, str(PROJECT))
                from mcp_task_server import task_store
                tid = task_store.create_task(
                    body["title"], body["role"], body.get("priority", "medium"),
                    body.get("description", ""), body.get("mods", []),
                )
                self._json_response(200, {"success": True, "task_id": tid})
            except Exception as e:
                self._json_response(400, {"error": str(e)})

        elif parsed.path == "/api/killswitch":
            if not body.get("confirm"):
                self._json_response(400, {"error": "Must include confirm: true"})
                return
            stop_file = COMMS / "STOP"
            if body.get("action") == "activate":
                stop_file.write_text("STOP", encoding="utf-8")
                self._json_response(200, {"success": True, "active": True})
            elif body.get("action") == "deactivate":
                if stop_file.exists():
                    stop_file.unlink()
                self._json_response(200, {"success": True, "active": False})
            else:
                self._json_response(400, {"error": "action must be activate or deactivate"})

        elif parsed.path == "/api/focus":
            focus_file = COMMS / "FOCUS.md"
            focus_file.write_text(body.get("content", ""), encoding="utf-8")
            self._json_response(200, {"success": True})

        elif parsed.path == "/api/message":
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            to_role = body.get("to", "")
            msg_type = body.get("type", "info")
            priority = body.get("priority", "medium")
            content = body.get("content", "")
            fn = f"{ts}_user_{msg_type}.md"
            full = f"---\nfrom: user\nto: {to_role}\ntype: {msg_type}\npriority: {priority}\n---\n\n{content}"
            inbox = COMMS / to_role / "inbox"
            inbox.mkdir(parents=True, exist_ok=True)
            (inbox / fn).write_text(full, encoding="utf-8")
            self._json_response(200, {"success": True, "filename": fn})

        else:
            self._json_response(404, {"error": "not found"})

    def _json_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass


def main():
    port = 8420
    server = HTTPServer(("localhost", port), DashboardHandler)
    print(f"Dashboard running at http://localhost:{port}")
    print("Press Ctrl+C to stop")

    def open_browser():
        time.sleep(1)
        webbrowser.open(f"http://localhost:{port}")

    Thread(target=open_browser, daemon=True).start()
    server.serve_forever()


if __name__ == "__main__":
    main()
