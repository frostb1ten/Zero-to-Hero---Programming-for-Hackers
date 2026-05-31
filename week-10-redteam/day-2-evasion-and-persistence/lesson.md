# Day 2: Evasion & Persistence Concepts

## Why Understand This
You need to know how malware works to defend against it.
Understanding evasion and persistence is core to both red team and blue team.

## Encoding & Obfuscation
```python
import base64
import zlib

# Base64 encoding
payload_code = "print('hello from payload')"
encoded = base64.b64encode(payload_code.encode()).decode()
# Decode and execute (this is what attackers do):
# exec(base64.b64decode(encoded))

# Compression + encoding
compressed = zlib.compress(payload_code.encode())
b64_compressed = base64.b64encode(compressed).decode()

# XOR with key
def xor_str(data, key):
    return bytes([b ^ key for b in data.encode()])

obfuscated = xor_str(payload_code, 0x42)
```

## String Obfuscation Techniques
```python
# Instead of: import os; os.system("whoami")

# Technique 1: chr() building
cmd = chr(119)+chr(104)+chr(111)+chr(97)+chr(109)+chr(105)  # "whoami"

# Technique 2: Reverse strings
cmd = "imaohw"[::-1]  # "whoami"

# Technique 3: Base64
import base64
cmd = base64.b64decode("d2hvYW1p").decode()  # "whoami"

# Technique 4: Split and join
parts = ["wh", "oa", "mi"]
cmd = "".join(parts)
```

## Anti-Analysis Checks
```python
import os
import platform
import sys

def detect_sandbox():
    """Check for signs of analysis environment."""
    indicators = []

    # Check for VM artifacts
    hostname = platform.node().lower()
    if any(vm in hostname for vm in ["sandbox", "malware", "virus", "analysis"]):
        indicators.append("suspicious hostname")

    # Check for debugger
    if sys.gettrace() is not None:
        indicators.append("debugger attached")

    # Check for low resources (VMs often have minimal specs)
    try:
        import psutil
        if psutil.cpu_count() <= 1:
            indicators.append("single CPU core")
        if psutil.virtual_memory().total < 2 * 1024**3:
            indicators.append("low RAM (<2GB)")
    except ImportError:
        pass

    return indicators
```

## Persistence Mechanisms (Concepts)
```python
import os
import platform

def persistence_locations():
    """Show common persistence locations (for study)."""
    system = platform.system()

    if system == "Windows":
        return {
            "Registry Run Key": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
            "Startup Folder": os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),
            "Scheduled Tasks": "schtasks /create ...",
            "WMI Events": "WMI event subscriptions",
        }
    else:
        return {
            "Cron Job": "/var/spool/cron/",
            "Systemd Service": "/etc/systemd/system/",
            "Bash Profile": "~/.bashrc or ~/.profile",
            "Init Script": "/etc/init.d/",
        }

# This is reference knowledge — understanding WHERE malware hides
# helps you find and remove it during incident response
```

## Process Injection Concepts
```python
# On Windows, malware commonly:
# 1. OpenProcess() — get handle to target process
# 2. VirtualAllocEx() — allocate memory in target
# 3. WriteProcessMemory() — write shellcode to allocated memory
# 4. CreateRemoteThread() — execute the shellcode

# In Python (conceptual — requires ctypes on Windows):
# import ctypes
# kernel32 = ctypes.windll.kernel32
# These APIs are used legitimately by debuggers and security tools
```

## Data Exfiltration Methods
```python
import base64
import json

def exfil_http(data, url):
    """Exfiltrate data via HTTP POST (conceptual)."""
    import requests
    encoded = base64.b64encode(json.dumps(data).encode()).decode()
    # requests.post(url, data={"d": encoded})
    return encoded

def exfil_dns(data, domain):
    """Exfiltrate data via DNS queries (conceptual)."""
    # Encode data as subdomain labels
    encoded = base64.b32encode(data.encode()).decode().lower()
    # Each DNS label max 63 chars, total max 253
    chunks = [encoded[i:i+60] for i in range(0, len(encoded), 60)]
    queries = [f"{chunk}.{domain}" for chunk in chunks]
    return queries
    # In reality: socket.gethostbyname(query) to trigger DNS lookup

# Understanding these helps you detect exfil in network traffic
```
