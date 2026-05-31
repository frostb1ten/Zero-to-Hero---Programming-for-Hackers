# =============================================================
# EXAMPLES — Regex
# =============================================================
import re

# --- 1. Finding IPs in text ---
log = """
[2026-05-30] Connection from 192.168.1.100 to 10.0.0.5
[2026-05-30] Failed login from 203.0.113.50
[2026-05-30] Blocked 198.51.100.23
"""

ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log)
print(f"[1] Found IPs: {ips}")
print()

# --- 2. Extracting IP:port pairs ---
text = "Connect to 10.0.0.1:22 and 10.0.0.2:443 for testing"
matches = re.findall(r"(\d+\.\d+\.\d+\.\d+):(\d+)", text)
print("[2] IP:Port pairs:")
for ip, port in matches:
    print(f"    {ip} port {port}")
print()

# --- 3. Email extraction ---
page = "Contact admin@example.com or security@corp.org for info"
emails = re.findall(r"[\w.-]+@[\w.-]+\.\w+", page)
print(f"[3] Emails: {emails}")
print()

# --- 4. Log parsing ---
log_line = "2026-05-30 14:30:22 ERROR [auth] Failed login for user 'admin' from 10.0.0.50"
match = re.search(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.+)", log_line)
if match:
    date, time, level, module, message = match.groups()
    print(f"[4] Log entry:")
    print(f"    Date:    {date}")
    print(f"    Time:    {time}")
    print(f"    Level:   {level}")
    print(f"    Module:  {module}")
    print(f"    Message: {message}")
print()

# --- 5. Validation ---
def is_valid_ip(ip):
    pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    match = re.match(pattern, ip)
    if not match:
        return False
    return all(0 <= int(g) <= 255 for g in match.groups())

test_ips = ["192.168.1.1", "999.1.1.1", "10.0.0", "abc.def.ghi.jkl"]
print("[5] IP validation:")
for ip in test_ips:
    print(f"    {ip:<20} -> {is_valid_ip(ip)}")
print()

# --- 6. Search and replace ---
messy = "Port   22   is    open"
clean = re.sub(r"\s+", " ", messy)
print(f"[6] Cleaned: '{clean}'")

# Redact IPs
redacted = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "[REDACTED]", log)
print(f"[6] Redacted log:\n{redacted}")
