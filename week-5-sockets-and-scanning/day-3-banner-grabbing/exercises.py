# =============================================================
# EXERCISES — Banner Grabbing
# =============================================================
import socket


# --- Exercise 1: Basic banner grab ---
# Connect to a port and try to receive data
def grab_banner(ip, port, timeout=3):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            ___  # connect
            banner = ___  # receive up to 1024 bytes and decode
            return banner.strip() if banner else "No banner"
    except Exception as e:
        return f"Error: {e}"

# Test on a known service
print(grab_banner("scanme.nmap.org", 22))


# --- Exercise 2: HTTP banner ---
# Send an HTTP HEAD request and return the first line of the response
def http_probe(ip, port=80, timeout=5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            request = ___  # build the HEAD request as bytes
            s.send(request)
            response = s.recv(4096).decode(errors="ignore")
            return ___  # return just the first line
    except Exception as e:
        return f"Error: {e}"

print(http_probe("httpbin.org"))
# Expected: something like "HTTP/1.1 200 OK"


# --- Exercise 3: Combined scan + banner ---
# Scan ports, then grab banners only on open ports
def scan_and_grab(ip, ports):
    results = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                banner = ___  # call grab_banner
                results.append({"port": port, "banner": banner})
    return results

# Test
results = scan_and_grab("scanme.nmap.org", [22, 80, 443])
for r in results:
    print(f"  Port {r['port']}: {r['banner'][:60]}")


# --- Exercise 4: Parse an SSH banner ---
# SSH banners look like: "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3"
# Extract the SSH version and OS info
def parse_ssh_banner(banner):
    parts = banner.split("-")
    if len(parts) >= 3:
        protocol = ___    # e.g., "2.0"
        software = ___    # e.g., "OpenSSH_8.9p1 Ubuntu-3"
        return {"protocol": protocol, "software": software}
    return None

test_banner = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"
parsed = parse_ssh_banner(test_banner)
if parsed:
    print(f"Protocol: {parsed['protocol']}")
    print(f"Software: {parsed['software']}")


print("\n--- All exercises complete! ---")
