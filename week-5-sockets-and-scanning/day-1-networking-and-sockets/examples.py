# =============================================================
# EXAMPLES — Networking & Sockets
# =============================================================
import socket

# --- 1. Your machine info ---
print("[1] Your Machine:")
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"    Hostname: {hostname}")
print(f"    Local IP: {local_ip}")
print()

# --- 2. DNS resolution ---
print("[2] DNS Resolution:")
domains = ["google.com", "github.com", "cloudflare.com"]
for domain in domains:
    try:
        ip = socket.gethostbyname(domain)
        print(f"    {domain:<20} → {ip}")
    except socket.gaierror:
        print(f"    {domain:<20} → FAILED")
print()

# --- 3. Check if a port is open ---
print("[3] Port check (localhost):")

def check_port(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except OSError:
        return False

# Check common ports on localhost
for port in [80, 135, 443, 445, 3389, 8080]:
    status = "OPEN" if check_port("127.0.0.1", port) else "closed"
    print(f"    127.0.0.1:{port} — {status}")
print()

# --- 4. Simple HTTP request via raw socket ---
print("[4] Raw HTTP request:")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect(("httpbin.org", 80))
        request = b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\nConnection: close\r\n\r\n"
        s.send(request)

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

        # Show first 3 lines of response
        lines = response.decode(errors="ignore").split("\n")
        for line in lines[:3]:
            print(f"    {line.strip()}")
except Exception as e:
    print(f"    Error: {e}")
print()

# --- 5. Reverse DNS ---
print("[5] Reverse DNS:")
test_ips = ["8.8.8.8", "1.1.1.1"]
for ip in test_ips:
    try:
        hostname = socket.gethostbyaddr(ip)
        print(f"    {ip} → {hostname[0]}")
    except socket.herror:
        print(f"    {ip} → No reverse DNS")
