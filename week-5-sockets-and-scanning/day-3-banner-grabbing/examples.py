# =============================================================
# EXAMPLES — Banner Grabbing
# =============================================================
import socket
import ssl


def grab_banner(ip, port, timeout=3):
    """Try to grab a banner from a service."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))

            # Try receiving (some services auto-send)
            try:
                banner = s.recv(1024).decode(errors="ignore").strip()
                if banner:
                    return banner
            except socket.timeout:
                pass

            # If nothing received, try an HTTP probe
            s.send(b"HEAD / HTTP/1.1\r\nHost: target\r\nConnection: close\r\n\r\n")
            response = s.recv(4096).decode(errors="ignore").strip()
            return response.split("\n")[0] if response else "No banner"

    except ConnectionRefusedError:
        return "Connection refused"
    except socket.timeout:
        return "Timeout"
    except OSError as e:
        return f"Error: {e}"


def http_header_grab(ip, port=80, timeout=5):
    """Get HTTP response headers."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
            s.send(request.encode())
            response = s.recv(4096).decode(errors="ignore")
            return response
    except Exception as e:
        return f"Error: {e}"


# --- 1. Basic banner grab ---
print("[1] Banner grab attempts on well-known services:")
targets = [
    ("scanme.nmap.org", 22),
    ("scanme.nmap.org", 80),
]
for ip, port in targets:
    banner = grab_banner(ip, port)
    print(f"    {ip}:{port} → {banner[:80]}")
print()

# --- 2. HTTP headers ---
print("[2] HTTP Headers from httpbin.org:")
headers = http_header_grab("httpbin.org", 80)
for line in headers.split("\r\n")[:8]:
    if line.strip():
        print(f"    {line}")
print()

# --- 3. SSL connection info ---
print("[3] SSL/TLS info:")
try:
    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw:
        raw.settimeout(5)
        with context.wrap_socket(raw, server_hostname="google.com") as s:
            s.connect(("google.com", 443))
            print(f"    TLS version: {s.version()}")
            print(f"    Cipher: {s.cipher()[0]}")
except Exception as e:
    print(f"    SSL Error: {e}")
print()

# --- 4. Multi-port banner scan ---
print("[4] Quick banner scan (localhost):")
for port in [22, 80, 135, 443, 445, 3389, 8080]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                try:
                    s.settimeout(1)
                    banner = s.recv(1024).decode(errors="ignore").strip()
                    if not banner:
                        banner = "(no auto-banner)"
                except socket.timeout:
                    banner = "(no auto-banner)"
                print(f"    [+] {port}/tcp OPEN — {banner[:60]}")
    except OSError:
        pass
