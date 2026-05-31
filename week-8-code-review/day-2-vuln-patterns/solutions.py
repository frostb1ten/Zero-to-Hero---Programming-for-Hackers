# =============================================================
# SOLUTIONS — Vulnerability Patterns
# =============================================================
import os
import subprocess
import re
import ast
import json


# --- Exercise 1: Command Injection Fix ---
def traceroute_safe(target):
    # Validate input is an IP or hostname
    if not re.match(r'^[a-zA-Z0-9.\-]+$', target):
        print("Invalid target")
        return
    subprocess.run(["tracert", target], capture_output=True, text=True)


# --- Exercise 2: SQL Injection Fix ---
def find_user_safe(conn, email):
    # Use parameterized query — the ? placeholder prevents injection
    return conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()


# --- Exercise 3: Path Traversal Fix ---
def serve_file_safe(filename):
    base_dir = os.path.realpath("/var/www/static")
    full_path = os.path.realpath(os.path.join(base_dir, filename))

    # Ensure the resolved path is still inside base_dir
    if not full_path.startswith(base_dir + os.sep):
        raise ValueError("Path traversal blocked")

    return open(full_path).read()


# --- Exercise 4: eval() Fix ---
def calculator_safe(expression):
    # ast.literal_eval only allows literals (numbers, strings, etc.)
    # It will reject function calls, imports, etc.
    try:
        return ast.literal_eval(expression)
    except (ValueError, SyntaxError):
        # For actual math, parse manually or use a safe math library
        # Simple approach: only allow digits and basic operators
        if re.match(r'^[\d\s+\-*/().]+$', expression):
            return eval(expression)  # OK because we validated the chars
        raise ValueError("Invalid expression")


# --- Exercise 5: Deserialization Fix ---
def load_data_safe(raw_string):
    # JSON cannot execute code — safe for untrusted data
    return json.loads(raw_string)


# --- Exercise 6: ALL the bugs ---
# 1. INSECURE DESERIALIZATION: pickle.loads(user_data["preferences"])
#    → Attacker sends crafted pickle bytes → Remote Code Execution
#    → Fix: use json.loads()
#
# 2. SQL INJECTION: f"SELECT * FROM users WHERE id = {user_data['user_id']}"
#    → Attacker sends "1 OR 1=1" → dumps all users
#    → Fix: parameterized query with ?
#
# 3. COMMAND INJECTION: os.system(user_data["command"])
#    → Attacker sends "whoami; cat /etc/shadow" → full system access
#    → Fix: whitelist allowed commands, use subprocess with list args
#
# 4. PATH TRAVERSAL: open(f"/uploads/{user_data['avatar']}")
#    → Attacker sends "../../etc/passwd" → reads any file
#    → Fix: validate resolved path stays in /uploads/

def process_request_safe(user_data):
    """Fixed version with all vulnerabilities patched."""
    import sqlite3

    # 1. Safe deserialization
    prefs = json.loads(user_data["preferences"])

    # 2. Parameterized query
    conn = sqlite3.connect("app.db")
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_data["user_id"],)
    ).fetchone()

    # 3. Whitelisted commands only
    ALLOWED = {"status", "info", "help"}
    if user_data.get("command") not in ALLOWED:
        raise ValueError("Command not allowed")
    subprocess.run([user_data["command"]], capture_output=True)

    # 4. Path traversal prevention
    base = os.path.realpath("/uploads")
    avatar_path = os.path.realpath(os.path.join("/uploads", user_data["avatar"]))
    if not avatar_path.startswith(base + os.sep):
        raise ValueError("Invalid avatar path")
    pic = open(avatar_path).read()

    return {"user": user, "prefs": prefs}


print("[+] Key rules for safe code:")
print("  1. Never shell=True or os.system() with user input")
print("  2. Always parameterize SQL queries")
print("  3. Always validate file paths against a base directory")
print("  4. Never eval/exec/pickle on untrusted data")
print("  5. Use allowlists, not blocklists")
