# Week 1 · Day 1: Variables & Types

> **After today:** You can store data, convert between types, and build formatted output — the atoms of every tool you'll ever write.

## Variables
A variable is a name for a value. Python figures out the type.

```python
target_ip = "192.168.1.1"      # string (text)
port = 443                      # integer (whole number)
timeout = 1.5                   # float (decimal)
is_alive = True                 # boolean (True/False)
result = None                   # nothing yet
```

No declaration needed. No semicolons. Just `name = value`.

## Types That Matter

| Type | Example | Use Case |
|------|---------|----------|
| `str` | `"10.0.0.1"` | IPs, hostnames, URLs, any text |
| `int` | `443` | Ports, counts, offsets, bytes |
| `float` | `0.5` | Timeouts, percentages |
| `bool` | `True` | Flags, states |
| `None` | `None` | "Not set yet" |

Check a type: `type(port)` → `<class 'int'>`

## Type Conversion (You'll Do This Constantly)
```python
# input() ALWAYS returns a string — you must convert
port_str = "8080"
port_num = int(port_str)       # "8080" → 8080

# Building output often needs str()
count = 5
msg = "Found " + str(count) + " open ports"

# Float for calculations
ratio = float("0.85")
```

## Strings — Your Most-Used Type
```python
# f-strings (memorize this — you'll use it 1000 times)
ip = "10.0.0.1"
port = 22
print(f"[*] Connecting to {ip}:{port}")

# Methods you need TODAY:
"  HTTPS://Evil.COM  ".strip()          # "HTTPS://Evil.COM"
"  HTTPS://Evil.COM  ".strip().lower()  # "https://evil.com"
"192.168.1.1".split(".")               # ["192", "168", "1", "1"]
":".join(["AA", "BB", "CC"])           # "AA:BB:CC"
len("hello")                            # 5

# Checking content
"192".isdigit()                # True
"admin" in "administrator"     # True
"hello".startswith("he")       # True
```

## input() — Getting User Data
```python
target = input("[?] Enter target IP: ")
port = int(input("[?] Enter port: "))    # convert immediately
print(f"[*] Target: {target}:{port}")
```

## Naming Convention
```python
target_ip = "10.0.0.1"     # snake_case — always
```

## Tomorrow
You'll use variables inside `if/else` and loops to build a login brute-force simulator.
