# =============================================================
# EXERCISES · Week 1 · Day 1 · Variables & Types
# =============================================================
# Fill every ___ · Run after each fix: python exercises.py
# =============================================================


# ─── 1. Create variables ─────────────────────────────────────
# target_ip = "10.0.0.1", port = 445, service = "SMB", is_open = True
___
___
___
___
print(f"[+] {target_ip}:{port} ({service}) open={is_open}")


# ─── 2. Type conversion ──────────────────────────────────────
port_input = "3389"
next_port = ___                  # convert to int, add 1
print(f"[*] RDP: {port_input} → next: {next_port}")
# Expected: RDP: 3389 → next: 3390


# ─── 3. f-string ─────────────────────────────────────────────
host = "192.168.1.1"
port = 22
service = "SSH"
message = ___                    # "[OPEN] 192.168.1.1:22 — SSH"
print(message)


# ─── 4. strip + lower ────────────────────────────────────────
raw = "   HtTpS://EVIL-CORP.com/Login   "
cleaned = ___
print(f"[*] '{cleaned}'")
# Expected: 'https://evil-corp.com/login'


# ─── 5. split ────────────────────────────────────────────────
ip = "172.16.50.100"
octets = ___
print(f"[*] {ip} → {len(octets)} octets, network={octets[0]}.{octets[1]}.x.x")


# ─── 6. join ─────────────────────────────────────────────────
parts = ["DE", "AD", "BE", "EF", "CA", "FE"]
mac = ___
print(f"[*] MAC: {mac}")
# Expected: DE:AD:BE:EF:CA:FE


# ─── 7. Boolean expressions ──────────────────────────────────
port = 80
is_common = ___          # True if port < 1024
is_http = ___            # True if port == 80
is_web = ___             # True if port is 80 OR 443
print(f"[*] common={is_common}, http={is_http}, web={is_web}")


# ─── 8. input + convert ──────────────────────────────────────
ip = ___                 # ask user for IP
port = ___               # ask user for port (must be int!)
print(f"[*] Connecting to {ip}:{port}...")


# ─── 9. Parse URL protocol ───────────────────────────────────
url = "https://target.com/admin"
protocol = ___           # extract "https" (hint: split on "://")
print(f"[*] Protocol: {protocol}")


# ─── 10. CHALLENGE: Full URL parsing ─────────────────────────
# Parse "ftp://10.0.0.5:21" into protocol, ip (str), port (int)
target_string = "ftp://10.0.0.5:21"
protocol = ___
ip = ___
port = ___               # must be int!
print(f"[*] {protocol} | {ip} | {port} (type={type(port).__name__})")


print("\n[+] All exercises complete!")
