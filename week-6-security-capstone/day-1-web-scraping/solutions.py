# =============================================================
# SOLUTIONS — Web Scraping
# =============================================================
import requests
import re
from bs4 import BeautifulSoup

# --- Exercise 1 ---
def get_title(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.title.string if soup.title else "No title"

print(f"Title: {get_title('https://example.com')}")

# --- Exercise 2 ---
def get_links(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        links.append(a["href"])
    return links

links = get_links("https://example.com")
print(f"Found {len(links)} links")
for link in links[:5]:
    print(f"  {link}")

# --- Exercise 3 ---
def scrape_emails(url):
    r = requests.get(url, timeout=10)
    emails = set(re.findall(r"[\w.-]+@[\w.-]+\.\w+", r.text))
    return emails

print(f"Emails: {scrape_emails('https://example.com')}")

# --- Exercise 4 ---
def get_disallowed(domain):
    url = f"https://{domain}/robots.txt"
    try:
        r = requests.get(url, timeout=10)
        paths = []
        for line in r.text.split("\n"):
            if line.startswith("Disallow"):
                path = line.split(":", 1)[1].strip()
                if path:
                    paths.append(path)
        return paths
    except:
        return []

paths = get_disallowed("google.com")
print(f"Google has {len(paths)} disallowed paths")

# --- Exercise 5 ---
def find_forms(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    forms = []
    for form in soup.find_all("form"):
        info = {
            "action": form.get("action"),
            "method": form.get("method", "GET").upper(),
        }
        forms.append(info)
    return forms

forms = find_forms("https://example.com")
print(f"Found {len(forms)} forms")

print("\n--- All exercises complete! ---")
