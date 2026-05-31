# Day 2: Vulnerability Patterns

## The OWASP Top Vulnerabilities You Need to Know

### 1. Command Injection
```python
# VULNERABLE
os.system(f"nmap {user_input}")

# SAFE
subprocess.run(["nmap", "-sV", validated_ip], capture_output=True)
```

### 2. SQL Injection
```python
# VULNERABLE
cursor.execute(f"SELECT * FROM users WHERE id = {uid}")

# SAFE
cursor.execute("SELECT * FROM users WHERE id = ?", (uid,))
```

### 3. Cross-Site Scripting (XSS)
```python
# VULNERABLE — reflects user input into HTML
return f"<h1>Hello {username}</h1>"

# SAFE — escape HTML entities
from html import escape
return f"<h1>Hello {escape(username)}</h1>"
```

### 4. Path Traversal
```python
# VULNERABLE
open(f"/data/{filename}")

# SAFE
real = os.path.realpath(os.path.join("/data", filename))
assert real.startswith("/data/")
```

### 5. Insecure Deserialization
```python
# VULNERABLE — pickle executes code on load
obj = pickle.loads(untrusted_bytes)

# SAFE — JSON can't execute code
obj = json.loads(untrusted_string)
```

### 6. Server-Side Request Forgery (SSRF)
```python
# VULNERABLE — user controls the URL
response = requests.get(user_provided_url)

# SAFE — validate against allowlist
from urllib.parse import urlparse
parsed = urlparse(user_url)
if parsed.hostname not in ALLOWED_HOSTS:
    raise ValueError("Blocked")
```

### 7. Hardcoded Secrets
```python
# VULNERABLE
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "admin123"

# SAFE
API_KEY = os.environ.get("API_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
```

### 8. Race Conditions (TOCTOU)
```python
# VULNERABLE — check and use are separate
if os.path.exists(filepath):
    # attacker swaps file between check and open
    data = open(filepath).read()

# SAFER — just try it
try:
    data = open(filepath).read()
except FileNotFoundError:
    handle_missing()
```

### 9. Weak Cryptography
```python
# VULNERABLE
hashlib.md5(password.encode())   # fast, crackable
random.randint(0, 999999)        # predictable tokens

# SAFE
import secrets
import bcrypt
token = secrets.token_hex(32)    # cryptographically random
hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
```

### 10. Information Disclosure
```python
# VULNERABLE — leaks internals
except Exception as e:
    return {"error": str(e)}     # reveals stack traces, paths, versions

# SAFE
except Exception as e:
    log.error(f"Internal error: {e}")
    return {"error": "Something went wrong"}
```

## Code Review Grep Cheatsheet
```
# Find all the danger zones fast:
os.system          → command injection
subprocess.*shell  → command injection
eval(              → code execution
exec(              → code execution
pickle.load        → deserialization RCE
yaml.load          → deserialization
execute.*f"        → SQL injection
execute.*+         → SQL injection
open(.*+           → path traversal
password.*=.*"     → hardcoded creds
secret.*=.*"       → hardcoded secrets
debug.*True        → debug mode in prod
```
