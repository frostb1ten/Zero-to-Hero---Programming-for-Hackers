# =============================================================
# SOLUTIONS — Reading Code for Vulnerabilities
# =============================================================
import os
import subprocess
import json
import ast


# --- Exercise 1 ---
# VULNERABILITY: Command Injection
# EXPLOIT: ip = "127.0.0.1 & whoami" or "127.0.0.1; cat /etc/passwd"
# FIX: Use subprocess with a list (no shell=True)

def ping_host_safe(ip):
    # Validate IP format first
    import re
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        print("Invalid IP format")
        return
    subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True)


# --- Exercise 2 ---
# VULNERABILITY: Code Execution via eval()
# EXPLOIT: expr = "__import__('os').system('whoami')"
# FIX: Use ast.literal_eval or manual parsing

def admin_panel_safe(user_input):
    if user_input == "show config":
        print("Config: ...")
    elif user_input == "calc":
        expr = input("Expression: ")
        try:
            # Only allows simple literals (numbers, strings, etc.)
            result = ast.literal_eval(expr)
            print(result)
        except (ValueError, SyntaxError):
            print("Invalid expression")


# --- Exercise 3 ---
# VULNERABILITY: Path Traversal
# EXPLOIT: report_name = "../../../etc/passwd"
# FIX: Validate the resolved path stays within allowed directory

def download_report_safe(report_name):
    base_dir = "/var/reports"
    safe_path = os.path.realpath(os.path.join(base_dir, report_name))
    if not safe_path.startswith(base_dir):
        raise ValueError("Access denied: path traversal detected")
    with open(safe_path, "r") as f:
        return f.read()


# --- Exercise 4 ---
# VULNERABILITY: Insecure Deserialization (Remote Code Execution)
# WHY: pickle can execute arbitrary code during deserialization.
#   An attacker crafts malicious pickle bytes that run commands.
# FIX: Use JSON instead of pickle for untrusted data

def load_session_safe(session_data):
    """Load session from JSON (safe)."""
    return json.loads(session_data)


# --- Exercise 5 ---
# VULNERABILITY: SQL Injection
# EXPLOIT: name = "' OR '1'='1' --"
#   Query becomes: SELECT * FROM users WHERE name LIKE '%' OR '1'='1' --%'
#   Returns all users
# FIX: Use parameterized queries

def search_users_safe(name):
    import sqlite3
    conn = sqlite3.connect("app.db")
    results = conn.execute(
        "SELECT * FROM users WHERE name LIKE ?",
        (f"%{name}%",)
    ).fetchall()
    return results


# --- Exercise 6 ---
# FIX: Whitelist allowed commands, use subprocess with list args

ALLOWED_COMMANDS = {
    "status": ["systemctl", "status"],
    "uptime": ["uptime"],
    "disk": ["df", "-h"],
    "netstat": ["netstat", "-tlnp"],
}

def safe_run(user_command):
    """Only allow whitelisted commands."""
    if user_command not in ALLOWED_COMMANDS:
        print(f"Unknown command: {user_command}")
        print(f"Allowed: {', '.join(ALLOWED_COMMANDS.keys())}")
        return

    cmd = ALLOWED_COMMANDS[user_command]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)


print("[+] All solutions demonstrate safe patterns.")
print("[+] Key takeaways:")
print("  1. Never pass user input to os.system() or shell=True")
print("  2. Never use eval()/exec() on user input")
print("  3. Always validate file paths to prevent traversal")
print("  4. Never pickle.loads() untrusted data")
print("  5. Always use parameterized SQL queries")
print("  6. Whitelist allowed operations, don't blacklist")
