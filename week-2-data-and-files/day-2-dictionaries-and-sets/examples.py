# =============================================================
# EXAMPLES — Dictionaries & Sets
# =============================================================

# --- 1. Building a scan report with dicts ---
scan = {
    "target": "192.168.1.1",
    "open_ports": [22, 80, 443],
    "os_guess": "Linux",
    "scan_time": 12.5
}

print(f"[*] Scan Report for {scan['target']}")
print(f"    OS: {scan['os_guess']}")
print(f"    Open ports: {len(scan['open_ports'])}")
print(f"    Duration: {scan['scan_time']}s")
print()

# --- 2. Port-to-service mapping ---
services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}

open_ports = [22, 80, 443, 3306]
print("[*] Identified services:")
for port in open_ports:
    service = services.get(port, "Unknown")
    print(f"    {port}/tcp — {service}")
print()

# --- 3. Nested dict — multiple hosts ---
network = {
    "10.0.0.1": {"hostname": "web01", "ports": [80, 443]},
    "10.0.0.2": {"hostname": "db01", "ports": [3306, 5432]},
    "10.0.0.3": {"hostname": "mail01", "ports": [25, 587]},
}

for ip, info in network.items():
    print(f"  {ip} ({info['hostname']}): ports {info['ports']}")
print()

# --- 4. Sets for deduplication ---
scan1_ports = {22, 80, 443}
scan2_ports = {80, 443, 8080, 8443}

all_ports = scan1_ports | scan2_ports
common = scan1_ports & scan2_ports
new_in_scan2 = scan2_ports - scan1_ports

print(f"Scan 1: {scan1_ports}")
print(f"Scan 2: {scan2_ports}")
print(f"All unique: {all_ports}")
print(f"In both: {common}")
print(f"New in scan 2: {new_in_scan2}")
