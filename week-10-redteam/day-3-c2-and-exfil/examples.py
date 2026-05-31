# =============================================================
# EXAMPLES — C2 & Exfiltration Concepts (Educational)
# =============================================================
import json
import base64
import hashlib
import time
import random
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


# --- 1. C2 message format ---
print("[1] C2 message protocol:")

def build_checkin(agent_id, hostname):
    """Build a check-in message."""
    return {
        "type": "checkin",
        "id": agent_id,
        "host": hostname,
        "time": time.time(),
    }

def build_task(command):
    """Build a task for an agent."""
    return {
        "type": "task",
        "cmd": command,
        "id": hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    }

def build_result(task_id, output):
    """Build a result message."""
    return {
        "type": "result",
        "task_id": task_id,
        "output": base64.b64encode(output.encode()).decode(),
        "time": time.time()
    }

checkin = build_checkin("agent-001", "WORKSTATION-1")
task = build_task("whoami")
result = build_result(task["id"], "frost\\user")

print(f"  Checkin: {json.dumps(checkin, indent=2)}")
print(f"  Task:    {json.dumps(task)}")
print(f"  Result:  {json.dumps(result)}")
print()


# --- 2. Jittered beaconing ---
print("[2] Jittered beacon timing:")

def jitter_interval(base_seconds, jitter_pct=0.2):
    jitter = base_seconds * jitter_pct
    return max(1, base_seconds + random.uniform(-jitter, jitter))

# Show what jittered intervals look like
intervals = [jitter_interval(60, 0.3) for _ in range(10)]
print(f"  Base: 60s, Jitter: 30%")
print(f"  Intervals: {[f'{i:.1f}s' for i in intervals]}")
print(f"  Range: {min(intervals):.1f}s - {max(intervals):.1f}s")
print()


# --- 3. Simple encrypted transport ---
print("[3] Encrypted message transport:")

def encrypt_message(data, key):
    """Simple XOR encryption (use AES in production)."""
    json_bytes = json.dumps(data).encode()
    key_bytes = hashlib.sha256(key.encode()).digest()
    encrypted = bytes([json_bytes[i] ^ key_bytes[i % len(key_bytes)]
                       for i in range(len(json_bytes))])
    return base64.b64encode(encrypted).decode()

def decrypt_message(encoded, key):
    """Decrypt a message."""
    encrypted = base64.b64decode(encoded)
    key_bytes = hashlib.sha256(key.encode()).digest()
    decrypted = bytes([encrypted[i] ^ key_bytes[i % len(key_bytes)]
                       for i in range(len(encrypted))])
    return json.loads(decrypted.decode())

secret_key = "MyC2SecretKey!"
original = {"cmd": "whoami", "id": "task-001"}
encrypted = encrypt_message(original, secret_key)
decrypted = decrypt_message(encrypted, secret_key)

print(f"  Original:  {original}")
print(f"  Encrypted: {encrypted[:50]}...")
print(f"  Decrypted: {decrypted}")
print(f"  Match:     {original == decrypted}")
print()


# --- 4. HTTP C2 server (demo — runs briefly) ---
print("[4] HTTP C2 server demo:")

class MiniC2(BaseHTTPRequestHandler):
    task_queue = ["whoami", "hostname"]
    results = []

    def do_GET(self):
        if self.path == "/task":
            cmd = self.task_queue.pop(0) if self.task_queue else ""
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"cmd": cmd}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/result":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            self.results.append(json.loads(body))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    def log_message(self, *args):
        pass

print("  (C2 server template ready — not running in demo)")
print(f"  Task queue: {MiniC2.task_queue}")
print()


# --- 5. Data staging for exfil ---
print("[5] Data staging:")

def stage_data(data, chunk_size=1024):
    """Break data into chunks for staged exfiltration."""
    encoded = base64.b64encode(json.dumps(data).encode()).decode()
    chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
    return {
        "total_chunks": len(chunks),
        "total_size": len(encoded),
        "chunks": chunks
    }

big_data = {"files": [f"secret_{i}.txt" for i in range(100)]}
staged = stage_data(big_data, chunk_size=200)
print(f"  Data size: {staged['total_size']} bytes")
print(f"  Chunks:    {staged['total_chunks']}")
print(f"  Chunk[0]:  {staged['chunks'][0][:50]}...")
