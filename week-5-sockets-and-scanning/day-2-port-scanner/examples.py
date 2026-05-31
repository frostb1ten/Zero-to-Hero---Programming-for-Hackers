# =============================================================
# EXAMPLES — Port Scanner
# Scans localhost by default — safe for testing
# =============================================================
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}


def check_port(ip, port, timeout=0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except OSError:
        return False


# --- 1. Simple sequential scan ---
print("[1] Sequential scan (ports 1-100 on localhost):")
start = time.time()
open_ports = []

for port in range(1, 101):
    if check_port("127.0.0.1", port):
        service = SERVICES.get(port, "Unknown")
        open_ports.append(port)
        print(f"    [+] {port}/tcp — {service}")

elapsed = time.time() - start
print(f"    Scanned 100 ports in {elapsed:.2f}s")
print(f"    Found {len(open_ports)} open ports")
print()


# --- 2. Threaded scan (much faster) ---
print("[2] Threaded scan (ports 1-1000 on localhost):")
start = time.time()
open_ports = []
lock = threading.Lock()

def scan_worker(ip, port):
    if check_port(ip, port):
        with lock:
            open_ports.append(port)

threads = []
for port in range(1, 1001):
    t = threading.Thread(target=scan_worker, args=("127.0.0.1", port))
    threads.append(t)
    t.start()

    if len(threads) >= 100:
        for t in threads:
            t.join()
        threads = []

for t in threads:
    t.join()

elapsed = time.time() - start
print(f"    Scanned 1000 ports in {elapsed:.2f}s")
for port in sorted(open_ports):
    print(f"    [+] {port}/tcp — {SERVICES.get(port, 'Unknown')}")
print()


# --- 3. ThreadPoolExecutor (cleanest) ---
print("[3] ThreadPoolExecutor (ports 1-1000):")
start = time.time()

def pool_check(args):
    ip, port = args
    if check_port(ip, port):
        return port
    return None

targets = [("127.0.0.1", p) for p in range(1, 1001)]

with ThreadPoolExecutor(max_workers=100) as pool:
    results = list(pool.map(pool_check, targets))

found = sorted([p for p in results if p])
elapsed = time.time() - start
print(f"    Scanned 1000 ports in {elapsed:.2f}s")
print(f"    Open: {found}")
