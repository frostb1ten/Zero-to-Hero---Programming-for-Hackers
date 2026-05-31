# =============================================================
# EXAMPLES — Subprocess & OS
# =============================================================
import subprocess
import os
import platform

# --- 1. System info ---
print("[1] System Info:")
print(f"    OS: {platform.system()} {platform.version()}")
print(f"    Hostname: {platform.node()}")
print(f"    Python: {platform.python_version()}")
print(f"    CWD: {os.getcwd()}")
print()

# --- 2. Run a command ---
print("[2] Running 'ipconfig' (or 'ifconfig' on Linux):")
if platform.system() == "Windows":
    cmd = ["ipconfig"]
else:
    cmd = ["ifconfig"]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
# Print first 5 lines only
lines = result.stdout.strip().split("\n")
for line in lines[:5]:
    print(f"    {line}")
if len(lines) > 5:
    print(f"    ... ({len(lines) - 5} more lines)")
print()

# --- 3. Ping a host ---
print("[3] Ping test:")
target = "8.8.8.8"
if platform.system() == "Windows":
    ping_cmd = ["ping", "-n", "1", "-w", "2000", target]
else:
    ping_cmd = ["ping", "-c", "1", "-W", "2", target]

result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=10)
if result.returncode == 0:
    print(f"    {target}: ALIVE")
else:
    print(f"    {target}: DOWN")
print()

# --- 4. DNS lookup ---
print("[4] DNS Lookup:")
try:
    result = subprocess.run(
        ["nslookup", "google.com"],
        capture_output=True, text=True, timeout=10
    )
    for line in result.stdout.strip().split("\n"):
        print(f"    {line}")
except FileNotFoundError:
    print("    nslookup not available")
print()

# --- 5. Directory operations ---
print("[5] Directory operations:")
os.makedirs("temp_scan_output", exist_ok=True)
print(f"    Created: temp_scan_output/")

# Write a test file
with open("temp_scan_output/test.txt", "w") as f:
    f.write("test data")

files = os.listdir("temp_scan_output")
print(f"    Files: {files}")

# Cleanup
os.remove("temp_scan_output/test.txt")
os.rmdir("temp_scan_output")
print("    Cleaned up")
print()

# --- 6. Environment variables ---
print("[6] Key environment variables:")
for var in ["USERNAME", "USERPROFILE", "COMPUTERNAME"]:
    print(f"    {var}: {os.environ.get(var, 'N/A')}")
