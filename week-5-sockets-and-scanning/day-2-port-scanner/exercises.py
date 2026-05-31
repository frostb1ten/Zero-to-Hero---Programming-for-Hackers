# =============================================================
# EXERCISES — Port Scanner
# =============================================================
import socket
import time
from concurrent.futures import ThreadPoolExecutor


# --- Exercise 1: Basic port check ---
# Write is_open() that returns True if a port is open

def is_open(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            ___
            ___
    except OSError:
        return False

print(f"Localhost 135: {is_open('127.0.0.1', 135)}")


# --- Exercise 2: Sequential scanner ---
# Scan ports 1-100 on localhost. Store open ones in a list.
open_ports = []

for port in ___:
    if ___:
        open_ports.append(port)

print(f"Open ports (1-100): {open_ports}")


# --- Exercise 3: Add service detection ---
# Map port numbers to service names using a dictionary

SERVICES = {
    21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS",
    135: "RPC", 445: "SMB", 3389: "RDP"
}

def get_service(port):
    return ___

# Test it
for port in [22, 80, 9999]:
    print(f"  Port {port}: {get_service(port)}")


# --- Exercise 4: Timed scan ---
# Scan and measure how long it takes
start = ___
for port in range(1, 201):
    is_open("127.0.0.1", port, timeout=0.3)
elapsed = ___
print(f"Scanned 200 ports in {elapsed:.2f}s")


# --- Exercise 5: ThreadPoolExecutor scan ---
# Use ThreadPoolExecutor to scan ports 1-500 fast

def check(args):
    ip, port = args
    if is_open(ip, port, 0.5):
        return port
    return None

targets = ___  # list of (ip, port) tuples

start = time.time()
with ThreadPoolExecutor(max_workers=50) as pool:
    results = list(pool.map(check, targets))

found = sorted([p for p in results if p is not None])
elapsed = time.time() - start
print(f"Threaded scan: {len(found)} open ports in {elapsed:.2f}s")
print(f"Open: {found}")


print("\n--- All exercises complete! ---")
