"""Functional tests for the File Lock MCP Server."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_lock_server.server import lock_file, unlock_file, list_locks, force_unlock

# Test 1: Lock a file
r = lock_file("api_surgeon", "C:/Users/trust/Documents/Teardown/mods/AK-47/main.lua")
assert r["success"] == True, f"Lock failed: {r}"
print("1. Lock acquired:", r["message"])

# Test 2: Same role re-lock refreshes
r = lock_file("api_surgeon", "C:/Users/trust/Documents/Teardown/mods/AK-47/main.lua")
assert r["success"] == True, f"Re-lock failed: {r}"
print("2. Re-lock OK:", r["message"])

# Test 3: Different role gets blocked
r = lock_file("mod_converter", "C:/Users/trust/Documents/Teardown/mods/AK-47/main.lua")
assert r["success"] == False, f"Should be blocked: {r}"
assert r["held_by"] == "api_surgeon", f"Wrong holder: {r}"
print("3. Conflict detected:", r["message"])

# Test 4: Path normalization (backslashes + case)
r = lock_file("mod_converter", r"C:\Users\trust\Documents\Teardown\mods\AK-47\main.lua")
assert r["success"] == False, f"Normalization failed: {r}"
print("4. Path normalization works")

# Test 5: List locks
r = list_locks()
assert r["count"] == 1, f"Expected 1 lock: {r}"
print("5. List locks:", r["count"], "lock(s)")

# Test 6: Wrong role cant unlock
r = unlock_file("mod_converter", "C:/Users/trust/Documents/Teardown/mods/AK-47/main.lua")
assert r["success"] == False, f"Should fail: {r}"
print("6. Wrong role blocked from unlock:", r["error"])

# Test 7: Force unlock restricted to qa_lead
r = force_unlock("api_surgeon", "C:/Users/trust/Documents/Teardown/mods/AK-47/main.lua")
assert r["success"] == False, f"Should fail: {r}"
print("7. Force unlock restricted:", r["error"])

# Test 8: QA lead can force unlock
r = force_unlock("qa_lead", "C:/Users/trust/Documents/Teardown/mods/AK-47/main.lua")
assert r["success"] == True, f"QA force unlock failed: {r}"
print("8. QA force unlock OK:", r["message"])

# Test 9: Verify empty after unlock
r = list_locks()
assert r["count"] == 0, f"Expected 0 locks: {r}"
print("9. Locks empty after force unlock")

# Test 10: Invalid role
r = lock_file("hacker", "somefile.lua")
assert r["success"] == False, f"Invalid role accepted: {r}"
print("10. Invalid role rejected")

# Test 11: Unlock non-locked file
r = unlock_file("api_surgeon", "nonexistent.lua")
assert r["success"] == True, f"Unlock nonexistent failed: {r}"
print("11. Unlock non-locked file OK")

# Test 12: Correct unlock by holder
lock_file("mod_converter", "test.lua")
r = unlock_file("mod_converter", "test.lua")
assert r["success"] == True, f"Correct unlock failed: {r}"
print("12. Holder unlock OK")

print()
print("ALL 12 TESTS PASSED")
