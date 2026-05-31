# =============================================================
# EXERCISES — Lists & Tuples
# =============================================================


# --- Exercise 1: Create and access ---
# Create a list of ports: 21, 22, 80, 443, 3389
# Print the first port and the last port

ports = ___
print(f"First: {___}, Last: {___}")
# Expected: First: 21, Last: 3389


# --- Exercise 2: Modify a list ---
# Start with [22, 80], add 443 to the end, insert 21 at the beginning
ports = [22, 80]
___
___
print(ports)
# Expected: [21, 22, 80, 443]


# --- Exercise 3: List comprehension ---
# Create a list of all even numbers from 1 to 20
evens = [___]
print(evens)
# Expected: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


# --- Exercise 4: Filter with comprehension ---
# From the list below, keep only the ports above 1000
all_ports = [22, 80, 443, 3306, 5432, 8080, 8443]
high_ports = [___]
print(f"High ports: {high_ports}")
# Expected: High ports: [3306, 5432, 8080, 8443]


# --- Exercise 5: Generate IPs ---
# Use a list comprehension to make ["10.0.0.1", "10.0.0.2", ..., "10.0.0.10"]
ips = [___]
print(ips)


# --- Exercise 6: enumerate ---
# Print each target with a number starting at 1
targets = ["web-server", "db-server", "mail-server"]
for ___:
    print(f"[{num}] {target}")
# Expected: [1] web-server, [2] db-server, [3] mail-server


# --- Exercise 7: Tuple unpacking ---
# Unpack this tuple into 3 variables and print them
server_info = ("10.0.0.5", 3306, "MySQL")
___, ___, ___ = server_info
print(f"Server {ip} runs {service} on port {port}")
# Expected: Server 10.0.0.5 runs MySQL on port 3306


print("\n--- All exercises complete! ---")
