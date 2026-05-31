# =============================================================
# EXAMPLES — Lists & Tuples
# =============================================================

# --- 1. Building and modifying a list ---
scan_results = []

scan_results.append(("10.0.0.1", 22, "open"))
scan_results.append(("10.0.0.1", 80, "open"))
scan_results.append(("10.0.0.1", 443, "closed"))

print("[*] Scan results:")
for ip, port, status in scan_results:
    symbol = "+" if status == "open" else "-"
    print(f"  [{symbol}] {ip}:{port} — {status}")
print()

# --- 2. List comprehension ---
all_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080]

# Filter only "well-known" ports (under 1024)
well_known = [p for p in all_ports if p < 1024]
print(f"Well-known ports: {well_known}")

# Generate a target list
targets = [f"192.168.1.{i}" for i in range(1, 6)]
print(f"Targets: {targets}")
print()

# --- 3. Sorting ---
ports = [443, 22, 8080, 80, 21]
print(f"Original:  {ports}")
print(f"Sorted:    {sorted(ports)}")
print(f"Reversed:  {sorted(ports, reverse=True)}")
print()

# --- 4. Slicing ---
top_10 = list(range(1, 11))
print(f"All:       {top_10}")
print(f"First 3:   {top_10[:3]}")
print(f"Last 3:    {top_10[-3:]}")
print(f"Middle:    {top_10[3:7]}")
print(f"Every 2nd: {top_10[::2]}")
print()

# --- 5. enumerate for numbered output ---
services = ["SSH", "HTTP", "HTTPS", "MySQL", "RDP"]
print("Select a service to probe:")
for i, svc in enumerate(services, start=1):
    print(f"  [{i}] {svc}")
