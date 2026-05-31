# =============================================================
# EXAMPLES — Functions
# Run:  python examples.py
# =============================================================

# --- 1. Simple function ---
def banner(tool_name):
    line = "=" * 40
    print(line)
    print(f"  {tool_name}")
    print(line)

banner("Port Scanner v1.0")
print()


# --- 2. Return values ---
def calculate_subnet_hosts(prefix):
    """Calculate the number of usable hosts in a subnet."""
    total = 2 ** (32 - prefix)
    usable = total - 2  # subtract network + broadcast
    return usable

hosts = calculate_subnet_hosts(24)
print(f"/24 subnet has {hosts} usable hosts")

hosts = calculate_subnet_hosts(16)
print(f"/16 subnet has {hosts} usable hosts")
print()


# --- 3. Default parameters ---
def log_event(message, level="INFO"):
    print(f"[{level}] {message}")

log_event("Scan started")
log_event("Port 22 open", "SUCCESS")
log_event("Connection refused", "ERROR")
print()


# --- 4. Multiple returns ---
def parse_target(target_string):
    """Parse 'ip:port' into separate values."""
    parts = target_string.split(":")
    ip = parts[0]
    port = int(parts[1]) if len(parts) > 1 else 80
    return ip, port

ip, port = parse_target("10.0.0.1:443")
print(f"IP: {ip}, Port: {port}")

ip, port = parse_target("10.0.0.1")
print(f"IP: {ip}, Port: {port} (default)")
print()


# --- 5. Functions calling functions ---
def is_private_ip(ip):
    first = int(ip.split(".")[0])
    return first == 10 or first == 172 or first == 192

def classify_target(ip):
    if is_private_ip(ip):
        return "internal"
    return "external"

targets = ["192.168.1.1", "8.8.8.8", "10.0.0.5"]
for t in targets:
    print(f"  {t} -> {classify_target(t)}")
