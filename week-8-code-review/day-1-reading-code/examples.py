# =============================================================
# EXAMPLES — Reading Code for Vulnerabilities
# These are INTENTIONALLY vulnerable examples for learning.
# DO NOT use these patterns in real code.
# =============================================================

# =============================================================
# EXAMPLE 1: Can you spot the vulnerability?
# =============================================================

import os
import subprocess

def search_logs(query):
    """Search system logs for a pattern."""
    result = os.popen(f"grep {query} /var/log/syslog")
    return result.read()

# VULNERABILITY: Command Injection
# If query = "; cat /etc/passwd", the command becomes:
#   grep ; cat /etc/passwd /var/log/syslog
# Which runs TWO commands — grep AND cat /etc/passwd
#
# FIX:
# result = subprocess.run(["grep", query, "/var/log/syslog"],
#                         capture_output=True, text=True)


# =============================================================
# EXAMPLE 2: Can you spot the vulnerability?
# =============================================================

def get_user(user_id):
    """Look up a user by ID."""
    import sqlite3
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()

# VULNERABILITY: SQL Injection
# If user_id = "1 OR 1=1", the query becomes:
#   SELECT * FROM users WHERE id = 1 OR 1=1
# Which returns ALL users
#
# FIX:
# cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))


# =============================================================
# EXAMPLE 3: Can you spot the vulnerability?
# =============================================================

def read_file(filename):
    """Read a user's uploaded file."""
    filepath = f"/uploads/{filename}"
    with open(filepath, "r") as f:
        return f.read()

# VULNERABILITY: Path Traversal
# If filename = "../../etc/passwd", the path becomes:
#   /uploads/../../etc/passwd → /etc/passwd
#
# FIX:
# import os
# safe_path = os.path.realpath(os.path.join("/uploads", filename))
# if not safe_path.startswith("/uploads"):
#     raise ValueError("Invalid path")


# =============================================================
# EXAMPLE 4: Can you spot the vulnerability?
# =============================================================

def calculate(expression):
    """Simple calculator that evaluates expressions."""
    result = eval(expression)
    return result

# VULNERABILITY: Code Execution via eval()
# If expression = "__import__('os').system('whoami')"
# It runs arbitrary Python code!
#
# FIX:
# import ast
# result = ast.literal_eval(expression)  # only allows literals
# Or better: parse the expression manually


# =============================================================
# EXAMPLE 5: Can you spot the vulnerability?
# =============================================================

import hashlib

def check_password(username, password):
    """Verify a user's password."""
    stored_hash = get_hash_from_db(username)
    input_hash = hashlib.md5(password.encode()).hexdigest()
    return stored_hash == input_hash

def get_hash_from_db(username):
    # placeholder
    return "5f4dcc3b5aa765d61d8327deb882cf99"

# VULNERABILITIES (multiple!):
# 1. MD5 is broken — use bcrypt or argon2
# 2. No salt — identical passwords have identical hashes
# 3. Timing attack — string comparison leaks info
#
# FIX:
# import bcrypt
# stored = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# bcrypt.checkpw(password.encode(), stored)


# =============================================================
# EXAMPLE 6: Can you spot the vulnerability?
# =============================================================

def run_tool(tool_name, target):
    """Run a security tool on a target."""
    cmd = f"{tool_name} {target}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# VULNERABILITY: Command Injection via BOTH parameters
# tool_name = "nmap; rm -rf /"
# target = "10.0.0.1; cat /etc/shadow"
#
# FIX:
# ALLOWED_TOOLS = ["nmap", "ping", "traceroute"]
# if tool_name not in ALLOWED_TOOLS:
#     raise ValueError("Invalid tool")
# result = subprocess.run([tool_name, target], capture_output=True, text=True)


print("[*] These examples contain intentional vulnerabilities.")
print("[*] Study each one — find the bug, understand why, know the fix.")
print("[*] The comments explain each vulnerability.")
