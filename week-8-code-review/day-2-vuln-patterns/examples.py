# =============================================================
# EXAMPLES — Vulnerability Pattern Recognition
# Spot-the-bug exercises with increasing difficulty
# =============================================================

# =============================================================
# VULN 1: Command Injection — Subprocess with shell=True
# =============================================================
import subprocess

def dns_lookup_vuln(domain):
    """Vulnerable: shell=True + user input."""
    cmd = f"nslookup {domain}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def dns_lookup_safe(domain):
    """Safe: list args, no shell."""
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain):
        return "Invalid domain"
    result = subprocess.run(["nslookup", domain],
                           capture_output=True, text=True)
    return result.stdout


# =============================================================
# VULN 2: SQL Injection — String formatting in queries
# =============================================================

def login_vuln(username, password):
    """Vulnerable: string concatenation in SQL."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (username TEXT, password TEXT)")
    conn.execute("INSERT INTO users VALUES ('admin', 'secret123')")

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"  Query: {query}")
    result = conn.execute(query).fetchone()
    return result is not None

# Test the vulnerability
print("[VULN 2] SQL Injection:")
print(f"  Normal login: {login_vuln('admin', 'secret123')}")
print(f"  SQLi bypass:  {login_vuln(\"' OR '1'='1' --\", 'anything')}")
print()


# =============================================================
# VULN 3: Path Traversal
# =============================================================
import os

def read_user_file_vuln(filename):
    """Vulnerable: no path validation."""
    path = os.path.join("uploads", filename)
    return f"Would read: {path}"

def read_user_file_safe(filename):
    """Safe: validates resolved path."""
    base = os.path.realpath("uploads")
    full = os.path.realpath(os.path.join("uploads", filename))
    if not full.startswith(base):
        return "BLOCKED: Path traversal detected!"
    return f"Would read: {full}"

print("[VULN 3] Path Traversal:")
print(f"  Normal: {read_user_file_vuln('report.pdf')}")
print(f"  Attack: {read_user_file_vuln('../../etc/passwd')}")
print(f"  Safe normal: {read_user_file_safe('report.pdf')}")
print(f"  Safe attack: {read_user_file_safe('../../etc/passwd')}")
print()


# =============================================================
# VULN 4: Information Disclosure
# =============================================================

def api_handler_vuln(data):
    """Vulnerable: exposes internal errors."""
    try:
        result = int(data["value"]) / int(data["divisor"])
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}

def api_handler_safe(data):
    """Safe: generic error, logs internally."""
    try:
        result = int(data["value"]) / int(data["divisor"])
        return {"result": result}
    except Exception as e:
        # In real code: logger.error(f"API error: {e}")
        return {"error": "Invalid input"}

print("[VULN 4] Information Disclosure:")
print(f"  Vuln: {api_handler_vuln({'value': '10', 'divisor': '0'})}")
print(f"  Safe: {api_handler_safe({'value': '10', 'divisor': '0'})}")
print()


# =============================================================
# VULN 5: Hardcoded Secrets
# =============================================================

# VULNERABLE — never do this
class Config:
    DATABASE_URL = "postgresql://admin:P@ssw0rd@db.internal:5432/prod"
    API_KEY = "sk-live-abcdef1234567890"
    JWT_SECRET = "super_secret_key_123"

# SAFE
class SafeConfig:
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    API_KEY = os.environ.get("API_KEY", "")
    JWT_SECRET = os.environ.get("JWT_SECRET", "")

print("[VULN 5] Hardcoded secrets found in Config class:")
print(f"  DB URL: {Config.DATABASE_URL[:30]}...")
print(f"  These should be in environment variables!")
