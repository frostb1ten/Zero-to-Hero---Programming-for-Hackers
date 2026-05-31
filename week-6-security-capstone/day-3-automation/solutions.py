# =============================================================
# SOLUTIONS — Automation & Scripting
# =============================================================
import json
import os
import socket
import time
import logging
import shutil

# --- Exercise 1 ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("exercises")
logger.info("Logging configured!")
logger.warning("This is a warning")

# --- Exercise 2 ---
config = {
    "target": "10.0.0.1",
    "ports": [22, 80, 443],
    "timeout": 2
}
with open("test_config.json", "w") as f:
    json.dump(config, f, indent=2)
with open("test_config.json", "r") as f:
    loaded = json.load(f)
print(f"Loaded target: {loaded['target']}")
os.remove("test_config.json")

# --- Exercise 3 ---
def basic_recon(target):
    results = {"target": target}
    try:
        results["ip"] = socket.gethostbyname(target)
    except socket.gaierror:
        results["ip"] = None
        return results

    results["open_ports"] = []
    for port in [22, 80, 443]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((results["ip"], port)) == 0:
                results["open_ports"].append(port)
    return results

report = basic_recon("google.com")
print(f"Recon: {json.dumps(report, indent=2)}")

# --- Exercise 4 ---
os.makedirs("output", exist_ok=True)
with open("output/report.json", "w") as f:
    json.dump(report, f, indent=2)
with open("output/report.csv", "w") as f:
    f.write("target,ip,port,status\n")
    for port in report.get("open_ports", []):
        f.write(f"{report['target']},{report['ip']},{port},open\n")
print("[+] Saved to output/report.json and output/report.csv")
shutil.rmtree("output")

# --- Exercise 5 ---
start = time.time()
result = basic_recon("cloudflare.com")
elapsed = time.time() - start
print(f"Recon took {elapsed:.2f}s")
print(f"Found {len(result.get('open_ports', []))} open ports")

print("\n--- All exercises complete! ---")
