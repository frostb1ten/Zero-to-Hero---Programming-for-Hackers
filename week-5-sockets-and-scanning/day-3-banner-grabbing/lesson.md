# Day 3: Banner Grabbing

## The Core Idea
When you connect to an open port, many services announce themselves
with a "banner" — version info, software name, OS hints.
This is gold for enumeration.

## Basic Banner Grab
```python
import socket

def grab_banner(ip, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))

            # Some services send a banner immediately
            banner = s.recv(1024).decode(errors="ignore").strip()
            return banner
    except Exception:
        return None
```

## HTTP Banner Grab
```python
def http_banner(ip, port=80, timeout=3):
    """Send an HTTP request and grab the Server header."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))

            # Send a minimal HTTP request
            request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            s.send(request.encode())

            response = s.recv(4096).decode(errors="ignore")

            # Parse the Server header
            for line in response.split("\r\n"):
                if line.lower().startswith("server:"):
                    return line
            return response.split("\r\n")[0]  # return status line
    except Exception as e:
        return f"Error: {e}"
```

## Probing Different Services
```python
# FTP (port 21) — usually sends banner on connect
# SSH (port 22) — sends version string on connect
# SMTP (port 25) — sends greeting on connect
# HTTP (port 80) — need to send a request first
# MySQL (port 3306) — sends version on connect

# Services that auto-send banners:
AUTO_BANNER_PORTS = [21, 22, 25, 110, 143, 3306]

# Services that need a probe:
PROBE_NEEDED = {
    80: b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n",
    443: None,  # needs SSL
    8080: b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n",
}
```

## SSL/TLS Banner Grab
```python
import socket
import ssl

def ssl_banner(ip, port=443, timeout=3):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw:
            raw.settimeout(timeout)
            with context.wrap_socket(raw, server_hostname=ip) as s:
                s.connect((ip, port))

                # Get certificate info
                cert = s.getpeercert(binary_form=False)

                # Send HTTP request
                s.send(f"HEAD / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode())
                response = s.recv(4096).decode(errors="ignore")

                return {
                    "response": response.split("\r\n")[0],
                    "cipher": s.cipher(),
                    "version": s.version()
                }
    except Exception as e:
        return {"error": str(e)}
```
