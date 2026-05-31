# =============================================================
# SOLUTIONS — Subprocess & OS
# =============================================================
import subprocess
import os
import platform
import shutil

# --- Exercise 1 ---
result = subprocess.run(["whoami"], capture_output=True, text=True)
print(f"You are: {result.stdout.strip()}")

# --- Exercise 2 ---
target = "127.0.0.1"
if platform.system() == "Windows":
    cmd = ["ping", "-n", "1", "-w", "2000", target]
else:
    cmd = ["ping", "-c", "1", "-W", "2", target]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
if result.returncode == 0:
    print(f"{target} is alive!")
else:
    print(f"{target} is down!")

# --- Exercise 3 ---
os.makedirs("output/scans/results", exist_ok=True)
print(f"Directory exists: {os.path.exists('output/scans/results')}")

# --- Exercise 4 ---
for item in os.listdir("."):
    if os.path.isfile(item):
        size = os.path.getsize(item)
        print(f"  {item}: {size} bytes")

# --- Exercise 5 ---
def ping(ip):
    if platform.system() == "Windows":
        cmd = ["ping", "-n", "1", "-w", "2000", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "2", ip]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.returncode == 0

print(f"Localhost alive: {ping('127.0.0.1')}")

# Cleanup
if os.path.exists("output"):
    shutil.rmtree("output")

print("\n--- All exercises complete! ---")
