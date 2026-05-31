# =============================================================
# SOLUTIONS — Port Scanner
# =============================================================
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# --- Exercise 1 ---
def is_open(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except OSError:
        return False

print(f"Localhost 135: {is_open('127.0.0.1', 135)}")

# --- Exercise 2 ---
open_ports = []
for port in range(1, 101):
    if is_open("127.0.0.1", port, 0.5):
        open_ports.append(port)
print(f"Open ports (1-100): {open_ports}")

# --- Exercise 3 ---
SERVICES = {
    21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS",
    135: "RPC", 445: "SMB", 3389: "RDP"
}

def get_service(port):
    return SERVICES.get(port, "Unknown")

for port in [22, 80, 9999]:
    print(f"  Port {port}: {get_service(port)}")

# --- Exercise 4 ---
start = time.time()
for port in range(1, 201):
    is_open("127.0.0.1", port, timeout=0.3)
elapsed = time.time() - start
print(f"Scanned 200 ports in {elapsed:.2f}s")

# --- Exercise 5 ---
def check(args):
    ip, port = args
    if is_open(ip, port, 0.5):
        return port
    return None

targets = [("127.0.0.1", p) for p in range(1, 501)]

start = time.time()
with ThreadPoolExecutor(max_workers=50) as pool:
    results = list(pool.map(check, targets))

found = sorted([p for p in results if p is not None])
elapsed = time.time() - start
print(f"Threaded scan: {len(found)} open ports in {elapsed:.2f}s")
print(f"Open: {found}")

print("\n--- All exercises complete! ---")
