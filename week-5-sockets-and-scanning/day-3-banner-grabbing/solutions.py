# =============================================================
# SOLUTIONS — Banner Grabbing
# =============================================================
import socket

# --- Exercise 1 ---
def grab_banner(ip, port, timeout=3):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            banner = s.recv(1024).decode(errors="ignore")
            return banner.strip() if banner else "No banner"
    except Exception as e:
        return f"Error: {e}"

print(grab_banner("scanme.nmap.org", 22))

# --- Exercise 2 ---
def http_probe(ip, port=80, timeout=5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n".encode()
            s.send(request)
            response = s.recv(4096).decode(errors="ignore")
            return response.split("\r\n")[0]
    except Exception as e:
        return f"Error: {e}"

print(http_probe("httpbin.org"))

# --- Exercise 3 ---
def scan_and_grab(ip, ports):
    results = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                banner = grab_banner(ip, port)
                results.append({"port": port, "banner": banner})
    return results

results = scan_and_grab("scanme.nmap.org", [22, 80, 443])
for r in results:
    print(f"  Port {r['port']}: {r['banner'][:60]}")

# --- Exercise 4 ---
def parse_ssh_banner(banner):
    parts = banner.split("-")
    if len(parts) >= 3:
        protocol = parts[1]
        software = "-".join(parts[2:])
        return {"protocol": protocol, "software": software}
    return None

test_banner = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"
parsed = parse_ssh_banner(test_banner)
if parsed:
    print(f"Protocol: {parsed['protocol']}")
    print(f"Software: {parsed['software']}")

print("\n--- All exercises complete! ---")
