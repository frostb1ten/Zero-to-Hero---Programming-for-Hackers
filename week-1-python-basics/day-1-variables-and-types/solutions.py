# =============================================================
# SOLUTIONS · Week 1 · Day 1
# =============================================================

# 1
target_ip = "10.0.0.1"
port = 445
service = "SMB"
is_open = True
print(f"[+] {target_ip}:{port} ({service}) open={is_open}")

# 2
port_input = "3389"
next_port = int(port_input) + 1
print(f"[*] RDP: {port_input} → next: {next_port}")

# 3
host = "192.168.1.1"
port = 22
service = "SSH"
message = f"[OPEN] {host}:{port} — {service}"
print(message)

# 4
raw = "   HtTpS://EVIL-CORP.com/Login   "
cleaned = raw.strip().lower()
print(f"[*] '{cleaned}'")

# 5
ip = "172.16.50.100"
octets = ip.split(".")
print(f"[*] {ip} → {len(octets)} octets, network={octets[0]}.{octets[1]}.x.x")

# 6
parts = ["DE", "AD", "BE", "EF", "CA", "FE"]
mac = ":".join(parts)
print(f"[*] MAC: {mac}")

# 7
port = 80
is_common = port < 1024
is_http = port == 80
is_web = port == 80 or port == 443
print(f"[*] common={is_common}, http={is_http}, web={is_web}")

# 8
ip = input("[?] Enter IP: ")
port = int(input("[?] Enter port: "))
print(f"[*] Connecting to {ip}:{port}...")

# 9
url = "https://target.com/admin"
protocol = url.split("://")[0]
print(f"[*] Protocol: {protocol}")

# 10
target_string = "ftp://10.0.0.5:21"
parts = target_string.split("://")
protocol = parts[0]
host_port = parts[1].split(":")
ip = host_port[0]
port = int(host_port[1])
print(f"[*] {protocol} | {ip} | {port} (type={type(port).__name__})")

print("\n[+] All exercises complete!")
