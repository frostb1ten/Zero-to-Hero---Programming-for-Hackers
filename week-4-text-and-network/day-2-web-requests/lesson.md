# Day 2: Web Requests

## The Core Idea
The `requests` library lets you talk to websites and APIs from Python.
GET data, POST forms, check headers — essential for web recon.

## Install First
```
pip install requests
```

## Basic GET Request
```python
import requests

response = requests.get("https://httpbin.org/get")
print(response.status_code)   # 200
print(response.text)          # HTML or JSON as a string
print(response.headers)       # response headers dict
```

## Response Object
```python
r = requests.get("https://httpbin.org/get")

r.status_code    # 200, 404, 500, etc.
r.text           # response body as string
r.json()         # parse JSON response into a dict
r.headers        # response headers
r.url            # final URL (after redirects)
r.elapsed        # time taken
```

## Adding Headers & Parameters
```python
# Custom headers (e.g., User-Agent)
headers = {"User-Agent": "Mozilla/5.0 (Security Audit)"}
r = requests.get("https://example.com", headers=headers)

# Query parameters
params = {"q": "python", "page": 1}
r = requests.get("https://example.com/search", params=params)
# URL becomes: https://example.com/search?q=python&page=1
```

## POST Requests
```python
# Form data
data = {"username": "admin", "password": "test123"}
r = requests.post("https://httpbin.org/post", data=data)

# JSON data
import json
payload = {"target": "10.0.0.1", "scan_type": "full"}
r = requests.post("https://api.example.com/scan", json=payload)
```

## Handling Errors
```python
import requests

try:
    r = requests.get("https://example.com", timeout=5)
    r.raise_for_status()  # raises error for 4xx/5xx
    print(f"OK: {r.status_code}")
except requests.ConnectionError:
    print("Cannot connect")
except requests.Timeout:
    print("Request timed out")
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")
```

## Sessions — Persistent Connections
```python
session = requests.Session()
session.headers.update({"User-Agent": "SecurityBot/1.0"})

# All requests in this session share headers/cookies
r1 = session.get("https://example.com/login")
r2 = session.get("https://example.com/dashboard")
```

## Checking Response Headers for Recon
```python
r = requests.get("https://target.com")

server = r.headers.get("Server", "N/A")
powered = r.headers.get("X-Powered-By", "N/A")
print(f"Server: {server}")
print(f"Powered by: {powered}")
```
