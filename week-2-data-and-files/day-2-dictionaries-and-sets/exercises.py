# =============================================================
# EXERCISES — Dictionaries & Sets
# =============================================================


# --- Exercise 1: Create a dict ---
# Create a dict called 'target' with keys: ip, port, protocol
target = {___}
print(f"Attacking {target['ip']}:{target['port']} via {target['protocol']}")
# Expected: Attacking 10.0.0.1:443 via https


# --- Exercise 2: Safe access with .get() ---
# Access the 'os' key — but it doesn't exist! Use .get() with a default
server = {"ip": "10.0.0.5", "port": 22}
os_name = ___
print(f"OS: {os_name}")
# Expected: OS: Unknown


# --- Exercise 3: Loop through a dict ---
# Print each key-value pair on its own line
host_info = {"ip": "10.0.0.1", "status": "up", "ports": 5}
for ___:
    print(f"  {key} = {value}")


# --- Exercise 4: Build a dict from lists ---
# Use zip() and dict() to combine these two lists into a dictionary
ports = [22, 80, 443]
services = ["SSH", "HTTP", "HTTPS"]
port_map = ___
print(port_map)
# Expected: {22: 'SSH', 80: 'HTTP', 443: 'HTTPS'}


# --- Exercise 5: Count occurrences ---
# Count how many times each port appears in the list
port_hits = [80, 443, 80, 22, 80, 443, 22, 80]
counts = {}
for port in port_hits:
    ___
print(counts)
# Expected: {80: 4, 443: 2, 22: 2}


# --- Exercise 6: Sets ---
# Find which IPs appear in BOTH scan results
scan_a = {"10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.5"}
scan_b = {"10.0.0.2", "10.0.0.4", "10.0.0.5", "10.0.0.6"}
common = ___
print(f"IPs in both scans: {common}")
# Expected: IPs found in both (order may vary)


print("\n--- All exercises complete! ---")
