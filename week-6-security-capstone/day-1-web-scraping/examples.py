# =============================================================
# EXAMPLES — Web Scraping
# pip install requests beautifulsoup4
# =============================================================
import requests
import re

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("[!] Install beautifulsoup4: pip install beautifulsoup4")


# --- 1. Extract page title ---
print("[1] Page title:")
try:
    r = requests.get("https://example.com", timeout=10)
    if HAS_BS4:
        soup = BeautifulSoup(r.text, "html.parser")
        print(f"    Title: {soup.title.string}")
    else:
        title = re.search(r"<title>(.*?)</title>", r.text)
        print(f"    Title: {title.group(1) if title else 'N/A'}")
except requests.RequestException as e:
    print(f"    Error: {e}")
print()


# --- 2. Extract all links ---
print("[2] Links from example.com:")
try:
    r = requests.get("https://example.com", timeout=10)
    if HAS_BS4:
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a", href=True):
            print(f"    {link.get_text().strip()}: {link['href']}")
    else:
        links = re.findall(r'href="([^"]+)"', r.text)
        for link in links:
            print(f"    {link}")
except requests.RequestException as e:
    print(f"    Error: {e}")
print()


# --- 3. Check robots.txt ---
print("[3] Robots.txt analysis:")
try:
    r = requests.get("https://google.com/robots.txt", timeout=10)
    if r.status_code == 200:
        lines = r.text.strip().split("\n")
        disallowed = [l for l in lines if l.startswith("Disallow")]
        print(f"    Found {len(disallowed)} disallowed paths")
        for line in disallowed[:5]:
            print(f"    {line}")
        if len(disallowed) > 5:
            print(f"    ... and {len(disallowed) - 5} more")
except requests.RequestException as e:
    print(f"    Error: {e}")
print()


# --- 4. Extract emails with regex ---
print("[4] Email extraction:")
sample_html = """
<html>
<body>
Contact us at info@example.com or support@example.com.
Admin: admin@internal.corp
</body>
</html>
"""
emails = set(re.findall(r"[\w.-]+@[\w.-]+\.\w+", sample_html))
print(f"    Found: {emails}")
print()


# --- 5. Header recon ---
print("[5] Security header check:")
try:
    r = requests.get("https://example.com", timeout=10)
    headers_to_check = [
        "Server", "X-Powered-By", "X-Frame-Options",
        "Content-Security-Policy", "Strict-Transport-Security"
    ]
    for h in headers_to_check:
        val = r.headers.get(h, "NOT SET")
        status = "+" if val != "NOT SET" else "!"
        print(f"    [{status}] {h}: {val}")
except requests.RequestException as e:
    print(f"    Error: {e}")
