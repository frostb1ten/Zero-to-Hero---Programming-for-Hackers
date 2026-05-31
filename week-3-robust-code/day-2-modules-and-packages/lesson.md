# Day 2: Modules & Packages

## The Core Idea
Modules let you organize code into separate files and reuse code others wrote.
A module is just a `.py` file. A package is a folder of modules.

## Importing
```python
# Import the whole module
import os
print(os.getcwd())

# Import specific things
from os.path import exists, join
print(exists("file.txt"))

# Import with alias
import datetime as dt
now = dt.datetime.now()
```

## Useful Built-in Modules for Security
```python
import os          # file system, environment
import sys         # system info, command-line args
import json        # JSON parsing
import csv         # CSV files
import hashlib     # hashing (MD5, SHA)
import base64      # encoding/decoding
import random      # random numbers
import string      # string constants
import datetime    # dates and times
import time        # delays, timing
```

## sys.argv — Command Line Arguments
```python
import sys

# Running: python scanner.py 10.0.0.1 80
# sys.argv = ["scanner.py", "10.0.0.1", "80"]

if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} <ip> <port>")
    sys.exit(1)

target_ip = sys.argv[1]
target_port = int(sys.argv[2])
print(f"Scanning {target_ip}:{target_port}")
```

## JSON — Reading and Writing
```python
import json

# Write JSON
data = {"target": "10.0.0.1", "ports": [22, 80]}
with open("scan.json", "w") as f:
    json.dump(data, f, indent=2)

# Read JSON
with open("scan.json", "r") as f:
    loaded = json.load(f)
print(loaded["target"])
```

## hashlib — Hashing
```python
import hashlib

password = "admin123"
md5_hash = hashlib.md5(password.encode()).hexdigest()
sha256_hash = hashlib.sha256(password.encode()).hexdigest()

print(f"MD5:    {md5_hash}")
print(f"SHA256: {sha256_hash}")
```

## Creating Your Own Module
```python
# utils.py
def validate_ip(ip):
    parts = ip.split(".")
    return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

# main.py
from utils import validate_ip
print(validate_ip("192.168.1.1"))  # True
```

## if __name__ == "__main__"
```python
# This pattern lets a file work as BOTH a module and a script
def greet(name):
    return f"Hello, {name}"

if __name__ == "__main__":
    # Only runs when you execute THIS file directly
    print(greet("Frost"))
    # Does NOT run when someone imports this file
```
