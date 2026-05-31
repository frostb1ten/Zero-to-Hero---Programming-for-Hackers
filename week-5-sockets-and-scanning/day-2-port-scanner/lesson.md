# Day 2: Building a Port Scanner

## The Core Idea
Combine sockets with threading to scan ports fast.
This is the classic first pentesting tool.

## Simple Scanner (Slow)
```python
import socket

def scan_port(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except OSError:
        return False

# Scan ports 1-100 (very slow — one at a time)
for port in range(1, 101):
    if scan_port("10.0.0.1", port):
        print(f"[+] Port {port} is open")
```

## Threading — Do Many Things At Once
```python
import threading

def worker(name):
    print(f"Worker {name} starting")

# Create and start threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()
```

## Threaded Port Scanner
```python
import socket
import threading

open_ports = []
lock = threading.Lock()  # prevents race conditions

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                with lock:
                    open_ports.append(port)
    except OSError:
        pass

# Launch threads
target = "scanme.nmap.org"
threads = []

for port in range(1, 1025):
    t = threading.Thread(target=scan_port, args=(target, port))
    threads.append(t)
    t.start()

    # Limit concurrent threads
    if len(threads) >= 100:
        for t in threads:
            t.join()
        threads = []

# Wait for remaining
for t in threads:
    t.join()

print(f"Open ports: {sorted(open_ports)}")
```

## ThreadPoolExecutor — Cleaner Threading
```python
from concurrent.futures import ThreadPoolExecutor
import socket

def check_port(args):
    ip, port = args
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                return port
    except OSError:
        pass
    return None

target = "scanme.nmap.org"
port_range = [(target, p) for p in range(1, 1025)]

with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(check_port, port_range)

open_ports = [p for p in results if p is not None]
print(f"Open ports: {sorted(open_ports)}")
```

## Service Detection
```python
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt"
}

def get_service(port):
    return COMMON_SERVICES.get(port, "Unknown")
```
