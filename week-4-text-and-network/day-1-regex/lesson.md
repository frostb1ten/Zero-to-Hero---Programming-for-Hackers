# Day 1: Regular Expressions (Regex)

## The Core Idea
Regex lets you search for PATTERNS in text, not just exact strings.
Essential for parsing logs, extracting IPs, validating input, finding secrets.

## Basics
```python
import re

# re.search() — find first match
result = re.search(r"error", "Connection error on port 80")
if result:
    print(f"Found: {result.group()}")  # "error"

# re.findall() — find ALL matches
ips = re.findall(r"\d+\.\d+\.\d+\.\d+", log_text)

# re.sub() — search and replace
cleaned = re.sub(r"\s+", " ", messy_text)
```

## Pattern Cheat Sheet
```
.       Any character (except newline)
\d      Any digit (0-9)
\w      Any word char (letter, digit, underscore)
\s      Any whitespace (space, tab, newline)
\D \W \S   Opposite of above

*       0 or more
+       1 or more
?       0 or 1 (optional)
{3}     Exactly 3
{2,4}   Between 2 and 4

^       Start of string
$       End of string
[abc]   Any of a, b, or c
[^abc]  NOT a, b, or c
(...)   Capture group
|       OR
```

## Practical Patterns
```python
import re

# IP addresses
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# Email addresses
email_pattern = r"[\w.-]+@[\w.-]+\.\w+"

# URLs
url_pattern = r"https?://[\w./\-?&=]+"

# Port numbers in "host:port" format
port_pattern = r":(\d{1,5})"

# MAC addresses
mac_pattern = r"([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}"
```

## Groups — Extracting Pieces
```python
text = "Server 192.168.1.1:443 is responding"
match = re.search(r"(\d+\.\d+\.\d+\.\d+):(\d+)", text)

if match:
    ip = match.group(1)     # "192.168.1.1"
    port = match.group(2)   # "443"
    full = match.group(0)   # "192.168.1.1:443"
```

## re.compile() — Reuse Patterns
```python
ip_regex = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

# Now use it multiple times efficiently
ips_in_log = ip_regex.findall(log_data)
if ip_regex.search(user_input):
    print("Contains an IP!")
```
