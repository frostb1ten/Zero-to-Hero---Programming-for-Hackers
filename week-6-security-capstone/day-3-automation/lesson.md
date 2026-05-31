# Day 3: Automation & Scripting

## The Core Idea
Combine everything you've learned into reusable automation scripts.
The goal: go from "I can write a script" to "I build tools."

## argparse — Professional CLI Arguments
```python
import argparse

parser = argparse.ArgumentParser(description="Recon Tool")
parser.add_argument("target", help="Target IP or hostname")
parser.add_argument("-p", "--ports", default="1-1024", help="Port range")
parser.add_argument("-t", "--threads", type=int, default=50, help="Thread count")
parser.add_argument("-o", "--output", help="Output file")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

args = parser.parse_args()
print(f"Target: {args.target}")
print(f"Ports: {args.ports}")
print(f"Verbose: {args.verbose}")
```

## Logging — Better Than print()
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tool.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.info("Scan started")
logger.warning("Port 22 seems filtered")
logger.error("Connection timed out")
logger.debug("Sent 1024 bytes")  # only shown if level=DEBUG
```

## Configuration Files
```python
import json

# Save config
config = {
    "default_ports": "1-1024",
    "timeout": 2,
    "threads": 50,
    "output_dir": "results"
}
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

# Load config
with open("config.json", "r") as f:
    config = json.load(f)
```

## Automating Multiple Steps
```python
import subprocess
import json
import requests
import socket

def full_recon(target):
    """Run a complete recon pipeline on a target."""
    results = {"target": target, "steps": []}

    # Step 1: DNS
    try:
        ip = socket.gethostbyname(target)
        results["ip"] = ip
        results["steps"].append({"dns": "resolved", "ip": ip})
    except socket.gaierror:
        results["steps"].append({"dns": "failed"})
        return results

    # Step 2: Ping
    ping_cmd = ["ping", "-n", "1", "-w", "1000", ip]
    result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=5)
    alive = result.returncode == 0
    results["steps"].append({"ping": "alive" if alive else "down"})

    # Step 3: Quick port scan
    open_ports = []
    for port in [21, 22, 80, 443, 8080]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    results["open_ports"] = open_ports
    results["steps"].append({"port_scan": f"{len(open_ports)} open"})

    # Step 4: HTTP check
    if 80 in open_ports or 443 in open_ports:
        proto = "https" if 443 in open_ports else "http"
        try:
            r = requests.get(f"{proto}://{target}", timeout=5)
            results["steps"].append({
                "http": r.status_code,
                "server": r.headers.get("Server", "N/A")
            })
        except requests.RequestException:
            results["steps"].append({"http": "failed"})

    return results
```

## Scheduling & Timing
```python
import time

def run_periodically(func, interval, count):
    """Run a function every N seconds."""
    for i in range(count):
        print(f"\n--- Run {i + 1}/{count} ---")
        func()
        if i < count - 1:
            time.sleep(interval)
```

## Building a Tool Template
```python
#!/usr/bin/env python3
"""
Tool Name - One-line description
Author: Your Name
"""
import argparse
import logging
import sys

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s")
    return logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("target", help="Target")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logger = setup_logging(args.verbose)
    logger.info(f"Starting against {args.target}")

    # Your tool logic here

    logger.info("Complete")

if __name__ == "__main__":
    main()
```
