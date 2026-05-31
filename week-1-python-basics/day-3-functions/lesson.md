# Day 3: Functions

## The Core Idea
A function is a reusable block of code you give a name.
Instead of copying the same 10 lines everywhere, write it once and call it.

## Basic Function
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Frost")   # Hello, Frost!
greet("Admin")    # Hello, Admin!
```

## Parameters and Return Values
```python
def add(a, b):
    return a + b

result = add(10, 20)
print(result)  # 30
```

## Why return instead of print?
```python
# BAD — prints but can't reuse the result
def bad_add(a, b):
    print(a + b)

# GOOD — returns so you can use it anywhere
def good_add(a, b):
    return a + b

total = good_add(5, 3)  # total = 8, usable later
```

## Default Parameters
```python
def scan_port(ip, port=80, timeout=1.0):
    print(f"Scanning {ip}:{port} (timeout: {timeout}s)")

scan_port("10.0.0.1")              # uses defaults: port=80, timeout=1.0
scan_port("10.0.0.1", 443)         # port=443, timeout=1.0
scan_port("10.0.0.1", timeout=5)   # port=80, timeout=5
```

## Multiple Return Values
```python
def analyze_ip(ip):
    parts = ip.split(".")
    first_octet = int(parts[0])

    if first_octet < 128:
        ip_class = "A"
    elif first_octet < 192:
        ip_class = "B"
    else:
        ip_class = "C"

    return ip_class, first_octet

net_class, octet = analyze_ip("192.168.1.1")
print(f"Class {net_class}, first octet: {octet}")
```

## Scope — Where Variables Live
```python
name = "Global"  # lives everywhere

def my_func():
    name = "Local"  # only lives inside this function
    print(name)     # prints "Local"

my_func()
print(name)  # prints "Global" — unchanged
```

## Functions Calling Functions
```python
def is_valid_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if int(part) < 0 or int(part) > 255:
            return False
    return True

def scan_target(ip):
    if not is_valid_ip(ip):
        print(f"Invalid IP: {ip}")
        return
    print(f"Scanning {ip}...")

scan_target("192.168.1.1")   # Scanning 192.168.1.1...
scan_target("999.999.999.999")  # Invalid IP: 999.999.999.999
```
