# =============================================================
# EXERCISES — Networking & Sockets
# =============================================================
import socket


# --- Exercise 1: DNS resolution ---
# Resolve "google.com" to an IP address
ip = socket.___("google.com")
print(f"google.com → {ip}")


# --- Exercise 2: Port checker function ---
# Write a function that returns True if a port is open

def is_port_open(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = ___
            return ___
    except OSError:
        return False

print(f"Google 80:  {is_port_open('google.com', 80)}")   # Likely True
print(f"Google 22:  {is_port_open('google.com', 22)}")   # Likely False


# --- Exercise 3: Get your hostname and IP ---
hostname = socket.___
local_ip = socket.___
print(f"You are: {hostname} ({local_ip})")


# --- Exercise 4: Scan multiple ports ---
# Scan ports 20-25 on localhost and report open ones
target = "127.0.0.1"
open_ports = []

for port in range(20, 26):
    if ___:
        open_ports.append(port)

print(f"Open ports on {target}: {open_ports}")


# --- Exercise 5: Reverse DNS ---
# Try to get the hostname for 8.8.8.8
try:
    result = socket.___("8.8.8.8")
    print(f"8.8.8.8 → {result[0]}")
except ___:
    print("Reverse DNS failed")


print("\n--- All exercises complete! ---")
