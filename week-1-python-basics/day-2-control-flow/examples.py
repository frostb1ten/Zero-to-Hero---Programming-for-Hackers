# =============================================================
# EXAMPLES — Control Flow
# Run:  python examples.py
# =============================================================

# --- 1. Basic if/elif/else ---
port = 22

if port == 22:
    print("[*] SSH detected")
elif port == 80:
    print("[*] HTTP detected")
elif port == 443:
    print("[*] HTTPS detected")
else:
    print(f"[*] Unknown service on port {port}")
print()

# --- 2. Combining conditions ---
port = 3306
is_local = True

if port == 3306 and is_local:
    print("[!] MySQL exposed on local network")
elif port == 3306 and not is_local:
    print("[!!] MySQL exposed to the internet!")
print()

# --- 3. Membership check with 'in' ---
common_ports = [21, 22, 23, 25, 80, 443, 445, 3389]
target_port = 445

if target_port in common_ports:
    print(f"Port {target_port} is a commonly targeted port")
else:
    print(f"Port {target_port} is uncommon")
print()

# --- 4. for loop with a list ---
targets = ["192.168.1.1", "192.168.1.5", "192.168.1.10"]

for ip in targets:
    print(f"[*] Pinging {ip}...")
print()

# --- 5. range() patterns ---
print("Counting ports 80-85:")
for port in range(80, 86):
    print(f"  Port {port}")
print()

# --- 6. while loop with break ---
secret = "letmein"
tries = 0

while tries < 3:
    guess = f"attempt{tries}"  # simulating input for demo
    if guess == secret:
        print("Access granted!")
        break
    tries += 1
    print(f"  Attempt {tries}: wrong password")
else:
    print("  Locked out after 3 attempts.")
print()

# --- 7. continue — skip even ports ---
print("Odd ports only (1-10):")
for port in range(1, 11):
    if port % 2 == 0:
        continue
    print(f"  Port {port}")
