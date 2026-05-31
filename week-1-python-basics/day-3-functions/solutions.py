# =============================================================
# SOLUTIONS — Functions
# =============================================================

# --- Exercise 1 ---
def identify_service(port):
    if port == 21:
        print("FTP")
    elif port == 22:
        print("SSH")
    elif port == 80:
        print("HTTP")
    elif port == 443:
        print("HTTPS")
    else:
        print("Unknown")

identify_service(22)
identify_service(443)


# --- Exercise 2 ---
def add_ports(port1, port2):
    return port1 + port2

result = add_ports(80, 443)
print(f"Sum: {result}")


# --- Exercise 3 ---
def ping_host(ip, timeout=1.0):
    print(f"Pinging {ip} with timeout {timeout}s")

ping_host("10.0.0.1")
ping_host("10.0.0.1", 5.0)


# --- Exercise 4 ---
def is_valid_port(port):
    return 1 <= port <= 65535

print(is_valid_port(80))
print(is_valid_port(0))
print(is_valid_port(99999))


# --- Exercise 5 ---
def split_target(target):
    parts = target.split(":")
    ip = parts[0]
    port = int(parts[1]) if len(parts) > 1 else 80
    return ip, port

ip, port = split_target("192.168.1.1:8080")
print(f"IP={ip}, Port={port}")
ip, port = split_target("192.168.1.1")
print(f"IP={ip}, Port={port}")


# --- Exercise 6 ---
def generate_ip_range(base_ip, count):
    ips = []
    for i in range(1, count + 1):
        ips.append(f"{base_ip}.{i}")
    return ips

ips = generate_ip_range("192.168.1", 5)
print(ips)

print("\n--- All exercises complete! ---")
