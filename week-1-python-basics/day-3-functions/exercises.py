# =============================================================
# EXERCISES — Functions
# Fill in the blanks (___) to make each section work.
# =============================================================


# --- Exercise 1: Basic function ---
# Create a function that takes a port number and prints its service name

___ identify_service(port):
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

identify_service(22)   # Expected: SSH
identify_service(443)  # Expected: HTTPS


# --- Exercise 2: Return values ---
# Make this function RETURN the sum (don't print it)

def add_ports(port1, port2):
    ___

result = add_ports(80, 443)
print(f"Sum: {result}")
# Expected: Sum: 523


# --- Exercise 3: Default parameters ---
# Add a default timeout of 1.0 seconds to the function

def ping_host(ip, timeout=___):
    print(f"Pinging {ip} with timeout {timeout}s")

ping_host("10.0.0.1")        # Expected: ... timeout 1.0s
ping_host("10.0.0.1", 5.0)   # Expected: ... timeout 5.0s


# --- Exercise 4: Write a function from scratch ---
# Write a function called 'is_valid_port' that:
# - Takes a port number
# - Returns True if it's between 1 and 65535
# - Returns False otherwise

___
___
___

print(is_valid_port(80))      # Expected: True
print(is_valid_port(0))       # Expected: False
print(is_valid_port(99999))   # Expected: False


# --- Exercise 5: Multiple return values ---
# Write a function that splits "ip:port" and returns both parts
# If no port is given, default to 80

def split_target(target):
    parts = target.split(":")
    ip = ___
    port = ___
    return ip, port

ip, port = split_target("192.168.1.1:8080")
print(f"IP={ip}, Port={port}")
# Expected: IP=192.168.1.1, Port=8080

ip, port = split_target("192.168.1.1")
print(f"IP={ip}, Port={port}")
# Expected: IP=192.168.1.1, Port=80


# --- Exercise 6: Build a complete function ---
# Write a function called 'generate_ip_range' that:
# - Takes a base IP like "192.168.1" and a count like 5
# - Returns a list of IPs: ["192.168.1.1", "192.168.1.2", ...]

___

ips = generate_ip_range("192.168.1", 5)
print(ips)
# Expected: ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5']


print("\n--- All exercises complete! ---")
