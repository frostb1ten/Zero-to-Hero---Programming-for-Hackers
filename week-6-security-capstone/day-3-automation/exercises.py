# =============================================================
# EXERCISES — Automation & Scripting
# =============================================================
import json
import os
import socket
import time
import logging


# --- Exercise 1: Setup logging ---
# Configure logging to print INFO and above with timestamps

logging.basicConfig(
    level=___,
    format=___
)
logger = logging.getLogger("exercises")

logger.info("Logging configured!")
logger.warning("This is a warning")


# --- Exercise 2: Config file ---
# Create a config dict, save it to JSON, load it back

config = {
    "target": "10.0.0.1",
    "ports": [22, 80, 443],
    "timeout": 2
}

# Save
with open("test_config.json", "w") as f:
    ___

# Load
with open("test_config.json", "r") as f:
    loaded = ___

print(f"Loaded target: {loaded['target']}")
os.remove("test_config.json")


# --- Exercise 3: Multi-step pipeline ---
# Write a function that does DNS + ping + port check

def basic_recon(target):
    results = {"target": target}

    # Step 1: DNS resolution
    try:
        results["ip"] = ___
    except socket.gaierror:
        results["ip"] = None
        return results

    # Step 2: Check 3 common ports
    results["open_ports"] = []
    for port in [22, 80, 443]:
        ___  # check if port is open, append to list if so

    return results

report = basic_recon("google.com")
print(f"Recon: {json.dumps(report, indent=2)}")


# --- Exercise 4: Save results to multiple formats ---
# Save the report as both JSON and CSV

os.makedirs("output", exist_ok=True)

# JSON
with open("output/report.json", "w") as f:
    ___

# CSV
with open("output/report.csv", "w") as f:
    ___  # write header
    for port in report.get("open_ports", []):
        ___  # write row

print("[+] Saved to output/report.json and output/report.csv")

# Cleanup
import shutil
shutil.rmtree("output")


# --- Exercise 5: Timed execution ---
# Measure how long the recon takes
start = ___
result = basic_recon("cloudflare.com")
elapsed = ___
print(f"Recon took {elapsed:.2f}s")
print(f"Found {len(result.get('open_ports', []))} open ports")


print("\n--- All exercises complete! ---")
