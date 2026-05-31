# Day 1: Web Scraping

## The Core Idea
Web scraping extracts data from websites. For pentesting: find subdomains,
harvest emails, discover endpoints, and map the attack surface.

## Install
```
pip install requests beautifulsoup4
```

## Beautiful Soup Basics
```python
from bs4 import BeautifulSoup
import requests

r = requests.get("https://example.com")
soup = BeautifulSoup(r.text, "html.parser")

# Get the page title
print(soup.title.string)

# Find all links
for link in soup.find_all("a"):
    href = link.get("href")
    text = link.get_text()
    print(f"{text}: {href}")

# Find by CSS class
items = soup.find_all("div", class_="content")

# Find by ID
header = soup.find(id="main-header")
```

## Extracting Links
```python
def extract_links(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        links.append(a["href"])
    return links
```

## Extracting Emails from a Page
```python
import re
import requests

def scrape_emails(url):
    r = requests.get(url, timeout=10)
    emails = set(re.findall(r"[\w.-]+@[\w.-]+\.\w+", r.text))
    return emails
```

## Finding Forms (Useful for Testing)
```python
def find_forms(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    forms = []
    for form in soup.find_all("form"):
        details = {
            "action": form.get("action"),
            "method": form.get("method", "GET"),
            "inputs": []
        }
        for inp in form.find_all("input"):
            details["inputs"].append({
                "name": inp.get("name"),
                "type": inp.get("type", "text"),
                "value": inp.get("value", "")
            })
        forms.append(details)
    return forms
```

## Robots.txt — Free Recon
```python
def get_robots(domain):
    """Check robots.txt for hidden paths."""
    url = f"https://{domain}/robots.txt"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            for line in r.text.split("\n"):
                if "Disallow" in line:
                    print(f"  Hidden path: {line.split(':')[1].strip()}")
    except requests.RequestException:
        print("  Could not fetch robots.txt")
```

## Respecting Boundaries
- Always get permission before scraping
- Check robots.txt
- Use delays between requests
- Set a descriptive User-Agent
- Don't hammer servers
