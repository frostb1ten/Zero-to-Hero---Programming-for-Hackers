# Day 3: Subprocess & OS Commands

## The Core Idea
Run system commands (ping, nslookup, nmap, etc.) from Python
and capture their output. This is how you automate CLI tools.

## subprocess.run() — The Modern Way
```python
import subprocess

# Run a command and capture output
result = subprocess.run(
    ["ping", "-n", "1", "8.8.8.8"],
    capture_output=True,
    text=True
)

print(result.stdout)        # standard output
print(result.stderr)        # error output
print(result.returncode)    # 0 = success, non-zero = error
```

## Checking if a Command Succeeded
```python
result = subprocess.run(["ping", "-n", "1", "10.0.0.1"],
                        capture_output=True, text=True)

if result.returncode == 0:
    print("Host is alive!")
else:
    print("Host is down or unreachable")
```

## Timeout
```python
try:
    result = subprocess.run(
        ["ping", "-n", "4", "10.0.0.1"],
        capture_output=True, text=True,
        timeout=5
    )
except subprocess.TimeoutExpired:
    print("Command timed out!")
```

## os Module — System Interaction
```python
import os

# Environment variables
home = os.environ.get("USERPROFILE", "")
path = os.environ.get("PATH", "")

# Current directory
cwd = os.getcwd()

# List files
files = os.listdir(".")

# Create directories
os.makedirs("output/scans", exist_ok=True)

# Check if path exists
os.path.exists("output/scans")

# Get file size
os.path.getsize("file.txt")
```

## Platform Detection
```python
import platform

print(platform.system())      # "Windows", "Linux", "Darwin"
print(platform.node())        # hostname
print(platform.version())     # OS version

# Adjust commands per OS
import sys
if sys.platform == "win32":
    ping_flag = "-n"
else:
    ping_flag = "-c"
```

## Practical: Ping Sweep
```python
import subprocess

def ping_host(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "1000", ip],
        capture_output=True, text=True
    )
    return result.returncode == 0

for i in range(1, 11):
    ip = f"192.168.1.{i}"
    status = "UP" if ping_host(ip) else "DOWN"
    print(f"  {ip}: {status}")
```

## Security Note
```python
# NEVER use shell=True with user input — command injection risk!
# BAD:
subprocess.run(f"ping {user_input}", shell=True)

# GOOD:
subprocess.run(["ping", "-n", "1", user_input])
```
