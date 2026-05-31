# Day 1: Error Handling

## The Core Idea
Errors will happen — bad input, missing files, network timeouts. 
**try/except** lets your code handle errors instead of crashing.

## Basic try/except
```python
try:
    port = int(input("Enter port: "))
    print(f"Port: {port}")
except ValueError:
    print("That's not a valid number!")
```

## Catching Specific Errors
```python
try:
    with open("targets.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("Access denied!")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## try / except / else / finally
```python
try:
    f = open("config.txt", "r")
except FileNotFoundError:
    print("Config missing, using defaults")
else:
    # Only runs if NO error occurred
    data = f.read()
    f.close()
    print("Config loaded")
finally:
    # ALWAYS runs, error or not
    print("Setup complete")
```

## Common Errors in Security Scripts
```python
# ValueError — bad type conversion
int("not_a_number")

# FileNotFoundError — missing file
open("doesnt_exist.txt")

# KeyError — dict key doesn't exist
d = {"ip": "10.0.0.1"}
d["port"]

# IndexError — list index out of range
ports = [22, 80]
ports[5]

# ConnectionRefusedError — network connection failed
# TimeoutError — operation timed out
```

## Raising Your Own Errors
```python
def scan_port(port):
    if port < 1 or port > 65535:
        raise ValueError(f"Invalid port: {port}")
    print(f"Scanning port {port}")

try:
    scan_port(99999)
except ValueError as e:
    print(f"Error: {e}")
```

## Practical Pattern: Retry Loop
```python
def get_valid_port():
    while True:
        try:
            port = int(input("Port: "))
            if 1 <= port <= 65535:
                return port
            print("Must be 1-65535")
        except ValueError:
            print("Enter a number!")
```
