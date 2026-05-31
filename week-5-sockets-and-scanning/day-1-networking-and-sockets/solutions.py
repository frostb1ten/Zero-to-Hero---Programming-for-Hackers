# =============================================================
# SOLUTIONS — Networking & Sockets
# =============================================================
import socket

# --- Exercise 1 ---
ip = socket.gethostbyname("google.com")
print(f"google.com → {ip}")

# --- Exercise 2 ---
def is_port_open(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except OSError:
        return False

print(f"Google 80:  {is_port_open('google.com', 80)}")
print(f"Google 22:  {is_port_open('google.com', 22)}")

# --- Exercise 3 ---
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"You are: {hostname} ({local_ip})")

# --- Exercise 4 ---
target = "127.0.0.1"
open_ports = []
for port in range(20, 26):
    if is_port_open(target, port):
        open_ports.append(port)
print(f"Open ports on {target}: {open_ports}")

# --- Exercise 5 ---
try:
    result = socket.gethostbyaddr("8.8.8.8")
    print(f"8.8.8.8 → {result[0]}")
except socket.herror:
    print("Reverse DNS failed")

print("\n--- All exercises complete! ---")
