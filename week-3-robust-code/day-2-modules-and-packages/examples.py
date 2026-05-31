# =============================================================
# EXAMPLES — Modules & Packages
# =============================================================
import os
import sys
import json
import hashlib
import base64
import datetime
import random
import string

# --- 1. os module ---
print("[1] OS Module:")
print(f"    Current dir: {os.getcwd()}")
print(f"    Platform: {sys.platform}")
print(f"    Python: {sys.version.split()[0]}")
print()

# --- 2. JSON ---
print("[2] JSON:")
scan_data = {
    "target": "10.0.0.1",
    "ports": [22, 80, 443],
    "timestamp": str(datetime.datetime.now()),
    "status": "complete"
}
json_str = json.dumps(scan_data, indent=2)
print(json_str)

# Parse it back
parsed = json.loads(json_str)
print(f"    Target from JSON: {parsed['target']}")
print()

# --- 3. Hashing ---
print("[3] Hashing:")
passwords = ["password", "admin123", "letmein"]
for pw in passwords:
    md5 = hashlib.md5(pw.encode()).hexdigest()
    sha256 = hashlib.sha256(pw.encode()).hexdigest()[:16]  # truncated for display
    print(f"    {pw:<12} MD5={md5[:16]}...  SHA256={sha256}...")
print()

# --- 4. Base64 ---
print("[4] Base64:")
original = "admin:password123"
encoded = base64.b64encode(original.encode()).decode()
decoded = base64.b64decode(encoded).decode()
print(f"    Original: {original}")
print(f"    Encoded:  {encoded}")
print(f"    Decoded:  {decoded}")
print()

# --- 5. Random password generator ---
print("[5] Random password:")
chars = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choice(chars) for _ in range(16))
print(f"    Generated: {password}")
print()

# --- 6. Command line args ---
print("[6] sys.argv:")
print(f"    Script: {sys.argv[0]}")
print(f"    Args: {sys.argv[1:]}")
print(f"    (Run with: python examples.py arg1 arg2)")
