# =============================================================
# SOLUTIONS — Dictionaries & Sets
# =============================================================

# --- Exercise 1 ---
target = {"ip": "10.0.0.1", "port": 443, "protocol": "https"}
print(f"Attacking {target['ip']}:{target['port']} via {target['protocol']}")

# --- Exercise 2 ---
server = {"ip": "10.0.0.5", "port": 22}
os_name = server.get("os", "Unknown")
print(f"OS: {os_name}")

# --- Exercise 3 ---
host_info = {"ip": "10.0.0.1", "status": "up", "ports": 5}
for key, value in host_info.items():
    print(f"  {key} = {value}")

# --- Exercise 4 ---
ports = [22, 80, 443]
services = ["SSH", "HTTP", "HTTPS"]
port_map = dict(zip(ports, services))
print(port_map)

# --- Exercise 5 ---
port_hits = [80, 443, 80, 22, 80, 443, 22, 80]
counts = {}
for port in port_hits:
    counts[port] = counts.get(port, 0) + 1
print(counts)

# --- Exercise 6 ---
scan_a = {"10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.5"}
scan_b = {"10.0.0.2", "10.0.0.4", "10.0.0.5", "10.0.0.6"}
common = scan_a & scan_b
print(f"IPs in both scans: {common}")

print("\n--- All exercises complete! ---")
