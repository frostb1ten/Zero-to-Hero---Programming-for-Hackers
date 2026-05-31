# =============================================================
# EXAMPLES · Week 1 · Day 1 · Variables & Types
# =============================================================
# Run:  python examples.py
# PREDICT each output before you see it. If wrong, figure out why.
# =============================================================

# --- 1. Creating variables ---
target = "192.168.1.1"
port = 443
protocol = "https"
is_secure = True

print(f"[*] Target: {protocol}://{target}:{port}")
print(f"[*] Secure: {is_secure}")
print(f"[*] Types: target={type(target).__name__}, port={type(port).__name__}")
print()

# --- 2. Type conversion ---
user_port = "8080"            # THIS IS A STRING
real_port = int(user_port)    # NOW it's a number
print(f"[*] Port: {real_port} + 1 = {real_port + 1}")
print(f"[*] Can't do: '8080' + 1 → TypeError!")
print()

# --- 3. String methods (chain them) ---
raw_url = "   HTTPS://Target.COM/Admin   "
clean = raw_url.strip().lower()
print(f"[*] Raw:   '{raw_url}'")
print(f"[*] Clean: '{clean}'")
print()

# --- 4. split + join ---
ip = "192.168.1.100"
octets = ip.split(".")
print(f"[*] Split '{ip}' → {octets}")
print(f"[*] First: {octets[0]}, Last: {octets[-1]}")

mac_parts = ["DE", "AD", "BE", "EF", "CA", "FE"]
mac = ":".join(mac_parts)
print(f"[*] Joined: {mac}")
print()

# --- 5. f-string calculations ---
open_ports = 5
total = 1024
pct = (open_ports / total) * 100
print(f"[+] {open_ports}/{total} ports open ({pct:.2f}%)")
print()

# --- 6. Boolean expressions ---
port = 22
print(f"[*] port < 1024: {port < 1024}")
print(f"[*] port == 22:  {port == 22}")
print(f"[*] 'admin' in 'administrator': {'admin' in 'administrator'}")
print(f"[*] '443'.isdigit(): {'443'.isdigit()}")
print()

# --- 7. Parsing a target string ---
target_str = "https://10.0.0.5:8443"
parts = target_str.split("://")
proto = parts[0]                    # "https"
host_port = parts[1].split(":")
host = host_port[0]                 # "10.0.0.5"
port = int(host_port[1])            # 8443
print(f"[*] Parsed: proto={proto}, host={host}, port={port}")
