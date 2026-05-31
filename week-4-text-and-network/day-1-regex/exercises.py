# =============================================================
# EXERCISES — Regex
# =============================================================
import re


# --- Exercise 1: Find all numbers ---
text = "Port 22 and port 443 are open, 8080 is filtered"
numbers = re.findall(___, text)
print(f"Numbers: {numbers}")
# Expected: ['22', '443', '8080']


# --- Exercise 2: Find all IPs ---
log = "Connections from 192.168.1.5 and 10.0.0.100 detected"
ips = re.findall(___, log)
print(f"IPs: {ips}")
# Expected: ['192.168.1.5', '10.0.0.100']


# --- Exercise 3: Extract domains from URLs ---
urls = "Visit https://example.com and http://test.org/page"
# Hint: pattern should capture the domain after http(s)://
domains = re.findall(___, urls)
print(f"Domains: {domains}")
# Expected: ['example.com', 'test.org']


# --- Exercise 4: Validate email ---
# Write a function that returns True if the string is a valid email format
def is_valid_email(email):
    pattern = ___
    return bool(re.match(pattern, email))

print(is_valid_email("user@example.com"))    # True
print(is_valid_email("not-an-email"))        # False
print(is_valid_email("admin@corp.org"))      # True


# --- Exercise 5: Parse key=value pairs ---
config = "host=10.0.0.1 port=22 user=admin timeout=30"
pairs = re.findall(___, config)
print(f"Config: {dict(pairs)}")
# Expected: Config: {'host': '10.0.0.1', 'port': '22', 'user': 'admin', 'timeout': '30'}


# --- Exercise 6: Replace/redact ---
# Replace all email addresses with [REDACTED]
text = "Send results to admin@corp.com and backup@corp.com"
redacted = re.sub(___, "[REDACTED]", text)
print(redacted)
# Expected: Send results to [REDACTED] and [REDACTED]


print("\n--- All exercises complete! ---")
