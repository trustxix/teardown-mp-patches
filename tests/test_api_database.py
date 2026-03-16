import json
from pathlib import Path

API_DB_PATH = Path(__file__).parent.parent / "tools" / "api_database.json"

def test_api_database_loads():
    with open(API_DB_PATH) as f:
        db = json.load(f)
    assert len(db) > 50, f"Database should have 50+ entries, got {len(db)}"

def test_api_database_structure():
    with open(API_DB_PATH) as f:
        db = json.load(f)
    required_fields = {"domain", "needs_player_id"}
    valid_domains = {"server", "client", "both"}
    for name, entry in db.items():
        assert required_fields.issubset(entry.keys()), f"{name} missing fields: {required_fields - set(entry.keys())}"
        assert entry["domain"] in valid_domains, f"{name} invalid domain: {entry['domain']}"
        assert isinstance(entry["needs_player_id"], bool), f"{name} needs_player_id not bool"

def test_key_functions_present():
    with open(API_DB_PATH) as f:
        db = json.load(f)
    must_have = [
        "SetPlayerHealth", "GetPlayerTransform", "UiText",
        "InputPressed", "SetInt", "RegisterTool", "PlaySound",
        "GetAllPlayers", "ClientCall", "ServerCall",
        "FindBody", "QueryRaycast", "MakeHole", "Vec",
        "GetPlayerVehicle", "SpawnParticle", "DriveVehicle",
    ]
    for fn in must_have:
        assert fn in db, f"Missing key function: {fn}"

def test_ui_functions_restricted():
    with open(API_DB_PATH) as f:
        db = json.load(f)
    ui_fns = [k for k in db if k.startswith("Ui")]
    assert len(ui_fns) >= 10, "Should have 10+ UI functions"
    for fn in ui_fns:
        assert db[fn].get("restricted_to") == "client.draw", f"{fn} should be restricted to client.draw"

def test_player_functions_need_player_id():
    with open(API_DB_PATH) as f:
        db = json.load(f)
    player_fns = ["SetPlayerHealth", "GetPlayerHealth", "GetPlayerTransform",
                  "SetPlayerTransform", "ApplyPlayerDamage", "GetPlayerVehicle"]
    for fn in player_fns:
        assert db[fn]["needs_player_id"], f"{fn} should need playerId"

def test_deprecated_marked():
    with open(API_DB_PATH) as f:
        db = json.load(f)
    assert "GetPlayerRigTransform" in db
    assert db["GetPlayerRigTransform"].get("deprecated") == "GetPlayerRigWorldTransform"
