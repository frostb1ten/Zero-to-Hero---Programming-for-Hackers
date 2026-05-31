# =============================================================
# EXAMPLES — Web Requests
# Run: pip install requests   (if not already installed)
# =============================================================
import requests

# --- 1. Basic GET ---
print("[1] Basic GET request:")
try:
    r = requests.get("https://httpbin.org/get", timeout=10)
    print(f"    Status: {r.status_code}")
    print(f"    URL: {r.url}")
    print(f"    Time: {r.elapsed.total_seconds()}s")
except requests.RequestException as e:
    print(f"    Error: {e}")
print()

# --- 2. JSON API ---
print("[2] JSON API:")
try:
    r = requests.get("https://httpbin.org/json", timeout=10)
    data = r.json()
    print(f"    Type: {type(data).__name__}")
    print(f"    Keys: {list(data.keys())}")
except requests.RequestException as e:
    print(f"    Error: {e}")
print()

# --- 3. Custom headers ---
print("[3] Custom User-Agent:")
headers = {"User-Agent": "SecurityAudit/1.0"}
try:
    r = requests.get("https://httpbin.org/headers", headers=headers, timeout=10)
    echo = r.json()
    print(f"    Server saw: {echo['headers'].get('User-Agent', 'N/A')}")
except requests.RequestException as e:
    print(f"    Error: {e}")
print()

# --- 4. Query parameters ---
print("[4] Query params:")
params = {"name": "Frost", "tool": "scanner"}
try:
    r = requests.get("https://httpbin.org/get", params=params, timeout=10)
    print(f"    Final URL: {r.url}")
except requests.RequestException as e:
    print(f"    Error: {e}")
print()

# --- 5. Status code checking ---
print("[5] Status codes:")
test_urls = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
]
for url in test_urls:
    try:
        r = requests.get(url, timeout=10)
        code = url.split("/")[-1]
        print(f"    {code}: {r.status_code} {'OK' if r.ok else 'FAIL'}")
    except requests.RequestException as e:
        print(f"    Error: {e}")
print()

# --- 6. Header recon ---
print("[6] Header recon on httpbin.org:")
try:
    r = requests.get("https://httpbin.org", timeout=10)
    for header in ["Server", "Content-Type", "X-Powered-By"]:
        value = r.headers.get(header, "Not disclosed")
        print(f"    {header}: {value}")
except requests.RequestException as e:
    print(f"    Error: {e}")
