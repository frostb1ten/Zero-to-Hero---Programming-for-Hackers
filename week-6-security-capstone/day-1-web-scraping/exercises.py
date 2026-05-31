# =============================================================
# EXERCISES — Web Scraping
# pip install requests beautifulsoup4
# =============================================================
import requests
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[!] Run: pip install beautifulsoup4")
    exit()


# --- Exercise 1: Get page title ---
# Fetch a webpage and extract its <title>
def get_title(url):
    r = requests.get(url, timeout=10)
    soup = ___
    return ___

print(f"Title: {get_title('https://example.com')}")


# --- Exercise 2: Extract all links ---
# Return a list of all href values on the page
def get_links(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for a in ___:
        links.append(___)
    return links

links = get_links("https://example.com")
print(f"Found {len(links)} links")
for link in links[:5]:
    print(f"  {link}")


# --- Exercise 3: Extract emails ---
# Find all email addresses on a page using regex
def scrape_emails(url):
    r = requests.get(url, timeout=10)
    emails = ___
    return emails

# Test with httpbin (won't have emails, but tests the function)
print(f"Emails: {scrape_emails('https://example.com')}")


# --- Exercise 4: Check robots.txt ---
# Fetch robots.txt and return all Disallowed paths
def get_disallowed(domain):
    url = f"https://{domain}/robots.txt"
    try:
        r = requests.get(url, timeout=10)
        paths = []
        for line in r.text.split("\n"):
            if line.startswith("Disallow"):
                path = ___
                if path:
                    paths.append(path)
        return paths
    except:
        return []

paths = get_disallowed("google.com")
print(f"Google has {len(paths)} disallowed paths")


# --- Exercise 5: Form finder ---
# Find all forms on a page and list their actions and methods
def find_forms(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    forms = []
    for form in soup.find_all("form"):
        info = {
            "action": ___,
            "method": ___,
        }
        forms.append(info)
    return forms

# Note: example.com has no forms, but the function is correct
forms = find_forms("https://example.com")
print(f"Found {len(forms)} forms")


print("\n--- All exercises complete! ---")
