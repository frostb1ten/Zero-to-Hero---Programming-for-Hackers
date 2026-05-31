# =============================================================
# EXERCISES — Web Requests
# Make sure requests is installed: pip install requests
# =============================================================
import requests


# --- Exercise 1: Basic GET ---
# Make a GET request to https://httpbin.org/get and print the status code
r = ___
print(f"Status: {___}")
# Expected: Status: 200


# --- Exercise 2: Parse JSON ---
# GET https://httpbin.org/json and parse the response as JSON
r = requests.get("https://httpbin.org/json", timeout=10)
data = ___
print(f"Type: {type(data).__name__}")
print(f"Keys: {list(data.keys())}")


# --- Exercise 3: Custom headers ---
# Make a request with User-Agent set to "PentestBot/1.0"
headers = {___}
r = requests.get("https://httpbin.org/headers", headers=___, timeout=10)
print(r.json()["headers"]["User-Agent"])
# Expected: PentestBot/1.0


# --- Exercise 4: Error handling ---
# Try to connect to a URL that will fail. Handle the error gracefully.
___:
    r = requests.get("https://httpbin.org/status/404", timeout=10)
    r.raise_for_status()
    print("Success!")
___ requests.HTTPError:
    print("Got an HTTP error!")
___ requests.RequestException as e:
    print(f"Request failed: {e}")


# --- Exercise 5: Header checker ---
# Write a function that takes a URL and prints key security headers
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
        value = ___
        print(f"    {header}: {value}")

check_headers("https://httpbin.org")


print("\n--- All exercises complete! ---")
