# =============================================================
# SOLUTIONS — Lists & Tuples
# =============================================================

# --- Exercise 1 ---
ports = [21, 22, 80, 443, 3389]
print(f"First: {ports[0]}, Last: {ports[-1]}")

# --- Exercise 2 ---
ports = [22, 80]
ports.append(443)
ports.insert(0, 21)
print(ports)

# --- Exercise 3 ---
evens = [n for n in range(1, 21) if n % 2 == 0]
print(evens)

# --- Exercise 4 ---
all_ports = [22, 80, 443, 3306, 5432, 8080, 8443]
high_ports = [p for p in all_ports if p > 1000]
print(f"High ports: {high_ports}")

# --- Exercise 5 ---
ips = [f"10.0.0.{i}" for i in range(1, 11)]
print(ips)

# --- Exercise 6 ---
targets = ["web-server", "db-server", "mail-server"]
for num, target in enumerate(targets, start=1):
    print(f"[{num}] {target}")

# --- Exercise 7 ---
server_info = ("10.0.0.5", 3306, "MySQL")
ip, port, service = server_info
print(f"Server {ip} runs {service} on port {port}")

print("\n--- All exercises complete! ---")
