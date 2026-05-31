# =============================================================
# SOLUTIONS — Modules & Packages
# =============================================================

# --- Exercise 1 ---
import os
print(f"Current dir: {os.getcwd()}")

# --- Exercise 2 ---
import json
data = {"ip": "10.0.0.1", "ports": [22, 80], "status": "up"}
json_string = json.dumps(data, indent=2)
print(json_string)
parsed = json.loads(json_string)
print(f"IP from parsed JSON: {parsed['ip']}")

# --- Exercise 3 ---
import hashlib
password = "secret123"
hashed = hashlib.sha256(password.encode()).hexdigest()
print(f"SHA-256 of '{password}': {hashed}")

# --- Exercise 4 ---
import base64
original = "user:pass"
encoded = base64.b64encode(original.encode()).decode()
decoded = base64.b64decode(encoded).decode()
print(f"Encoded: {encoded}")
print(f"Decoded: {decoded}")

# --- Exercise 5 ---
import random
import string
chars = string.ascii_letters + string.digits
random_str = ''.join(random.choice(chars) for _ in range(12))
print(f"Random: {random_str}")

# --- Exercise 6 ---
import sys
arg_count = len(sys.argv) - 1
print(f"You passed {arg_count} arguments")

print("\n--- All exercises complete! ---")
