# =============================================================
# EXAMPLES — Automation & Scripting
# =============================================================
import json
import os
import time
import logging
import socket
import subprocess
import platform

# --- 1. Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("recon")

# --- 2. Config file ---
print("[2] Config management:")
config = {
    "default_ports": [22, 80, 443, 8080],
    "timeout": 2,
    "threads": 50,
    "output_dir": "results"
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
print("    Saved config.json")

with open("config.json", "r") as f:
    loaded = json.load(f)
print(f"    Loaded: {loaded['default_ports']}")
os.remove("config.json")
print()

# --- 3. Quick recon pipeline ---
print("[3] Recon pipeline:")

def quick_recon(target):
    logger.info(f"Starting recon on {target}")
    results = {"target": target}

    # DNS
    try:
        ip = socket.gethostbyname(target)
        results["ip"] = ip
        logger.info(f"Resolved: {target} -> {ip}")
    except socket.gaierror:
        logger.error(f"Cannot resolve {target}")
        return results

    # Ping
    if platform.system() == "Windows":
        cmd = ["ping", "-n", "1", "-w", "2000", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "2", ip]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    alive = result.returncode == 0
    results["alive"] = alive
    logger.info(f"Ping: {'alive' if alive else 'down'}")

    # Port scan
    open_ports = []
    for port in [22, 80, 443]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    results["open_ports"] = open_ports
    logger.info(f"Open ports: {open_ports}")

    return results

report = quick_recon("google.com")
print(f"    Report: {json.dumps(report, indent=2)}")
print()

# --- 4. Saving structured output ---
print("[4] Structured output:")
os.makedirs("results", exist_ok=True)

with open("results/recon.json", "w") as f:
    json.dump(report, f, indent=2)
print("    Saved results/recon.json")

# CSV output
with open("results/ports.csv", "w") as f:
    f.write("target,port,status\n")
    for port in report.get("open_ports", []):
        f.write(f"{report['target']},{port},open\n")
print("    Saved results/ports.csv")

# Cleanup
import shutil
shutil.rmtree("results")
print("    Cleaned up")
print()

# --- 5. Timing a scan ---
print("[5] Timing:")
start = time.time()
for _ in range(10):
    socket.gethostbyname("google.com")
elapsed = time.time() - start
print(f"    10 DNS lookups in {elapsed:.3f}s ({elapsed/10:.3f}s each)")
