# Day 1: Networking & Sockets

## The Core Idea
Sockets are the low-level foundation of ALL networking.
Every time you visit a website or SSH into a box, sockets are doing the work.

## TCP vs UDP
- **TCP**: Reliable, ordered, connection-based (HTTP, SSH, FTP)
- **UDP**: Fast, no connection, no guarantee (DNS, DHCP, streaming)

## Creating a TCP Socket
```python
import socket

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
# socket.AF_INET  = IPv4
# socket.SOCK_STREAM = TCP

s.settimeout(2)  # 2-second timeout

# Connect to a server
s.connect(("192.168.1.1", 80))

# Send data
s.send(b"Hello")  # b"" = bytes, not string

# Receive data
data = s.recv(1024)  # receive up to 1024 bytes
print(data.decode())

# Close
s.close()
```

## The 'with' Pattern (Auto-Close)
```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(2)
    s.connect(("example.com", 80))
    s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    response = s.recv(4096)
    print(response.decode())
# Socket auto-closes when 'with' block ends
```

## Checking if a Port is Open
```python
import socket

def is_port_open(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
```

## DNS Resolution
```python
import socket

# Hostname → IP
ip = socket.gethostbyname("google.com")
print(f"google.com → {ip}")

# IP → Hostname (reverse DNS)
try:
    hostname = socket.gethostbyaddr("8.8.8.8")
    print(f"8.8.8.8 → {hostname[0]}")
except socket.herror:
    print("No reverse DNS")
```

## Getting Your Own IP
```python
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Hostname: {hostname}")
print(f"Local IP: {local_ip}")
```

## connect_ex() — Silent Connection Test
```python
# Returns 0 if connected, error code if not
# No exceptions thrown — cleaner for scanning
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
result = s.connect_ex(("10.0.0.1", 80))
if result == 0:
    print("Port is open")
else:
    print(f"Port closed (error code: {result})")
s.close()
```
