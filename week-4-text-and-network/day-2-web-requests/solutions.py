# =============================================================
# SOLUTIONS — Web Requests
# =============================================================
import requests

# --- Exercise 1 ---
r = requests.get("https://httpbin.org/get", timeout=10)
print(f"Status: {r.status_code}")

# --- Exercise 2 ---
r = requests.get("https://httpbin.org/json", timeout=10)
data = r.json()
print(f"Type: {type(data).__name__}")
print(f"Keys: {list(data.keys())}")

# --- Exercise 3 ---
headers = {"User-Agent": "PentestBot/1.0"}
r = requests.get("https://httpbin.org/headers", headers=headers, timeout=10)
print(r.json()["headers"]["User-Agent"])

# --- Exercise 4 ---
try:
    r = requests.get("https://httpbin.org/status/404", timeout=10)
    r.raise_for_status()
    print("Success!")
except requests.HTTPError:
    print("Got an HTTP error!")
except requests.RequestException as e:
    print(f"Request failed: {e}")

# --- Exercise 5 ---
def check_headers(url):
    r = requests.get(url, timeout=10)
    security_headers = [
        "Server",
        "X-Powered-By",
        "X-Frame-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security"
    ]
    print(f"\n[*] Headers for {url}:")
    for header in security_headers:
        value = r.headers.get(header, "Not set")
        print(f"    {header}: {value}")

check_headers("https://httpbin.org")

print("\n--- All exercises complete! ---")
