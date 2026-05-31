# =============================================================
# SOLUTIONS — Control Flow
# =============================================================

# --- Exercise 1 ---
port = 80
if port == 21:
    print("FTP")
elif port == 22:
    print("SSH")
elif port == 80:
    print("HTTP")
else:
    print("Unknown service")

# --- Exercise 2 ---
port = 22
is_remote = True
if port == 22 and is_remote:
    print("CRITICAL: Remote SSH access!")
else:
    print("OK")

# --- Exercise 3 ---
protocol = "ssh"
allowed = ["http", "https", "ssh"]
if protocol in allowed:
    print(f"{protocol} is allowed")
else:
    print(f"{protocol} is blocked")

# --- Exercise 4 ---
targets = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
for ip in targets:
    print(f"Scanning {ip}...")

# --- Exercise 5 ---
for port in range(8080, 8086):
    print(f"Checking port {port}")

# --- Exercise 6 ---
count = 1
while count <= 5:
    print(f"Count: {count}")
    count += 1

# --- Exercise 7 ---
ports = [22, 80, 443, 8080, 3306]
for port in ports:
    if port == 443:
        print("Found HTTPS!")
        break
    print(f"Checked port {port}")

print("\n--- All exercises complete! ---")
