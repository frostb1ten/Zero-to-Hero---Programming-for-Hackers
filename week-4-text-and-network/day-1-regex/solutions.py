# =============================================================
# SOLUTIONS — Regex
# =============================================================
import re

# --- Exercise 1 ---
text = "Port 22 and port 443 are open, 8080 is filtered"
numbers = re.findall(r"\d+", text)
print(f"Numbers: {numbers}")

# --- Exercise 2 ---
log = "Connections from 192.168.1.5 and 10.0.0.100 detected"
ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log)
print(f"IPs: {ips}")

# --- Exercise 3 ---
urls = "Visit https://example.com and http://test.org/page"
domains = re.findall(r"https?://([\w.-]+)", urls)
print(f"Domains: {domains}")

# --- Exercise 4 ---
def is_valid_email(email):
    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
    return bool(re.match(pattern, email))

print(is_valid_email("user@example.com"))
print(is_valid_email("not-an-email"))
print(is_valid_email("admin@corp.org"))

# --- Exercise 5 ---
config = "host=10.0.0.1 port=22 user=admin timeout=30"
pairs = re.findall(r"(\w+)=([\w.]+)", config)
print(f"Config: {dict(pairs)}")

# --- Exercise 6 ---
text = "Send results to admin@corp.com and backup@corp.com"
redacted = re.sub(r"[\w.-]+@[\w.-]+\.\w+", "[REDACTED]", text)
print(redacted)

print("\n--- All exercises complete! ---")
