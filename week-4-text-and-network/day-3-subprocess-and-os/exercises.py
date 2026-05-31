# =============================================================
# EXERCISES — Subprocess & OS
# =============================================================
import subprocess
import os
import platform


# --- Exercise 1: Run a command ---
# Run "whoami" and print the output
result = subprocess.run(___, capture_output=True, text=True)
print(f"You are: {result.stdout.strip()}")


# --- Exercise 2: Ping a host ---
# Ping 127.0.0.1 (localhost) once and check if it succeeded
target = "127.0.0.1"
result = subprocess.run(
    ___,
    capture_output=True, text=True, timeout=10
)
if ___:
    print(f"{target} is alive!")
else:
    print(f"{target} is down!")


# --- Exercise 3: Create a directory structure ---
# Create "output/scans/results" (nested directories)
___
print(f"Directory exists: {os.path.exists('output/scans/results')}")
# Expected: True


# --- Exercise 4: List files with details ---
# List all files in the current directory and print their sizes
for item in os.listdir("."):
    if os.path.isfile(item):
        size = ___
        print(f"  {item}: {size} bytes")


# --- Exercise 5: Cross-platform ping function ---
# Write a function that works on both Windows and Linux
def ping(ip):
    if platform.system() == "Windows":
        cmd = ___
    else:
        cmd = ___

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.returncode == 0

print(f"Localhost alive: {ping('127.0.0.1')}")


# Cleanup
import shutil
if os.path.exists("output"):
    shutil.rmtree("output")

print("\n--- All exercises complete! ---")
