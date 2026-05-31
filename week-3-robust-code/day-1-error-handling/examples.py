# =============================================================
# EXAMPLES — Error Handling
# =============================================================

# --- 1. Basic try/except ---
print("[1] Safe number conversion:")
for value in ["80", "abc", "443", "", "99999"]:
    try:
        port = int(value)
        print(f"    '{value}' -> {port}")
    except ValueError:
        print(f"    '{value}' -> INVALID")
print()

# --- 2. File handling with errors ---
print("[2] Safe file reading:")
import os

for filename in ["exists.txt", "missing.txt"]:
    try:
        with open(filename, "r") as f:
            print(f"    Read {filename}: {f.read().strip()}")
    except FileNotFoundError:
        print(f"    {filename}: NOT FOUND")
print()

# --- 3. Dictionary safe access vs try/except ---
print("[3] Dict access patterns:")
host = {"ip": "10.0.0.1", "port": 22}

# Method 1: .get() with default
os_name = host.get("os", "Unknown")
print(f"    .get(): {os_name}")

# Method 2: try/except
try:
    os_name = host["os"]
except KeyError:
    os_name = "Unknown"
print(f"    try/except: {os_name}")
print()

# --- 4. Raising errors ---
print("[4] Custom validation:")

def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError(f"IP must have 4 octets, got {len(parts)}")
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            raise ValueError(f"Invalid octet: {part}")
    return True

test_ips = ["192.168.1.1", "10.0.0", "256.1.1.1", "10.0.0.1"]
for ip in test_ips:
    try:
        validate_ip(ip)
        print(f"    {ip} -> VALID")
    except ValueError as e:
        print(f"    {ip} -> ERROR: {e}")
print()

# --- 5. Multiple except blocks ---
print("[5] Multiple error types:")

def process_target(target_str):
    parts = target_str.split(":")
    ip = parts[0]
    port = int(parts[1])
    return ip, port

test_targets = ["10.0.0.1:80", "10.0.0.1", "10.0.0.1:abc"]
for target in test_targets:
    try:
        ip, port = process_target(target)
        print(f"    '{target}' -> {ip}:{port}")
    except IndexError:
        print(f"    '{target}' -> Missing port")
    except ValueError:
        print(f"    '{target}' -> Port not a number")
