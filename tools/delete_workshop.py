"""Delete all Teardown workshop items owned by the user."""
import urllib.request
import re
import subprocess
import os
import sys

STEAM_USER = os.environ.get("STEAM_USER", "")
STEAM_PASS = os.environ.get("STEAM_PASS", "")
if not STEAM_USER or not STEAM_PASS:
    print("ERROR: Set STEAM_USER and STEAM_PASS environment variables.")
    sys.exit(1)
APP_ID = "1167630"
STEAMCMD = r"C:\steamcmd\steamcmd.exe"
ID_STORE = r"C:\Users\trust\teardown-mp-patches\workshop_ids"

print("=== Delete All Teardown Workshop Items ===")
print(flush=True)

# Step 1: Find Steam64 ID
print("Looking up Steam ID...", flush=True)
steam_id = None

for root, dirs, files in os.walk(r"C:\steamcmd"):
    for f in files:
        if "config" in f.lower() and f.endswith(".vdf"):
            try:
                path = os.path.join(root, f)
                with open(path, "r", errors="ignore") as fh:
                    content = fh.read()
                for m in re.finditer(r"(\d{17})", content):
                    if m.group(1).startswith("7656"):
                        steam_id = m.group(1)
                        break
                if steam_id:
                    break
            except:
                pass

if not steam_id:
    print("Could not find Steam ID. Enter your Steam64 ID:", flush=True)
    steam_id = input("> ").strip()

print(f"Steam ID: {steam_id}", flush=True)
print(flush=True)

# Step 2: Fetch workshop items
print("Fetching your Teardown workshop items...", flush=True)
all_ids = []

for page in range(1, 20):
    url = f"https://steamcommunity.com/profiles/{steam_id}/myworkshopfiles/?appid={APP_ID}&numperpage=30&p={page}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=30)
        html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  Page {page}: fetch failed ({e})", flush=True)
        break

    ids = re.findall(r"sharedfiles/filedetails/\?id=(\d+)", html)
    ids = list(dict.fromkeys(ids))

    if not ids:
        break

    all_ids.extend(ids)
    print(f"  Page {page}: found {len(ids)} items", flush=True)

all_ids = list(dict.fromkeys(all_ids))

if not all_ids:
    print("\nNo workshop items found.", flush=True)
    sys.exit(0)

print(f"\nFound {len(all_ids)} items to delete.", flush=True)
print(flush=True)

# Step 3: Build single SteamCMD script with all delete commands
script_path = os.path.join(os.environ.get("TEMP", "/tmp"), "td_delete_all.txt")
with open(script_path, "w") as f:
    f.write(f"login {STEAM_USER} {STEAM_PASS}\n")
    for wid in all_ids:
        f.write(f"workshop_build_item_delete {APP_ID} {wid}\n")
    f.write("quit\n")

print(f"Deleting {len(all_ids)} items in one SteamCMD session...", flush=True)
print("(Steam Guard code may be needed)", flush=True)
print(flush=True)

# Step 4: Run single SteamCMD session — stream output live
process = subprocess.Popen(
    [STEAMCMD, "+runscript", script_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

for line in process.stdout:
    line = line.rstrip()
    if line:
        print(line, flush=True)

process.wait()

# Step 5: Clear saved IDs
if os.path.exists(ID_STORE):
    cleared = 0
    for f in os.listdir(ID_STORE):
        if f.endswith(".id"):
            os.remove(os.path.join(ID_STORE, f))
            cleared += 1
    if cleared:
        print(f"\nCleared {cleared} saved workshop IDs", flush=True)

print("\nDone! Run Publish_Teardown_Mods.bat for a clean publish.", flush=True)
