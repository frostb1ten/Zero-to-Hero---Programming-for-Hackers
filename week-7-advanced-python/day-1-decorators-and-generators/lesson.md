# Day 1: Decorators & Generators

## Why This Matters for Security Work
- **Decorators**: wrap functions with logging, timing, retry logic, auth checks
- **Generators**: process massive wordlists/logs without eating all your RAM

## Decorators — Functions That Wrap Functions
```python
def timer(func):
    """Measure how long a function takes."""
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

@timer
def scan_ports(ip, ports):
    # scanning logic here
    pass

scan_ports("10.0.0.1", range(1, 1025))
# Automatically prints: [TIMER] scan_ports took 12.345s
```

## Practical Decorators for Security Tools
```python
import functools
import time

# Retry on failure
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts - 1:
                        print(f"[RETRY] Attempt {attempt+1} failed: {e}")
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def connect_to_target(ip, port):
    # flaky connection logic
    pass

# Logging decorator
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result}")
        return result
    return wrapper
```

## Generators — Lazy Sequences
```python
# Regular function: builds entire list in memory
def get_all_ips(subnet, count):
    ips = []
    for i in range(1, count + 1):
        ips.append(f"{subnet}.{i}")
    return ips  # 10 million IPs = 10 million strings in RAM

# Generator: produces one at a time
def gen_ips(subnet, count):
    for i in range(1, count + 1):
        yield f"{subnet}.{i}"
    # Only ONE string in memory at a time

# Usage is identical
for ip in gen_ips("10.0.0", 1000000):
    scan(ip)
```

## Generator Expressions
```python
# List comprehension (builds full list)
ports = [p for p in range(1, 65536)]

# Generator expression (lazy — builds nothing upfront)
ports = (p for p in range(1, 65536))

# Use generators when the list is huge
with open("rockyou.txt", "r", errors="ignore") as f:
    passwords = (line.strip() for line in f)
    for pw in passwords:
        try_login(pw)
```

## Chaining Generators (Pipelines)
```python
def read_lines(filepath):
    with open(filepath, "r", errors="ignore") as f:
        for line in f:
            yield line.strip()

def filter_blanks(lines):
    for line in lines:
        if line and not line.startswith("#"):
            yield line

def add_mutations(words):
    for word in words:
        yield word
        yield word.capitalize()
        yield word + "123"
        yield word + "!"

# Pipeline: file → filter → mutate → use
words = read_lines("wordlist.txt")
words = filter_blanks(words)
words = add_mutations(words)

for password in words:
    try_crack(password)
```

## Context Managers (bonus)
```python
from contextlib import contextmanager
import socket

@contextmanager
def tcp_connect(ip, port, timeout=2):
    """Reusable socket connection."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
        yield sock
    finally:
        sock.close()

# Usage
with tcp_connect("10.0.0.1", 80) as s:
    s.send(b"GET / HTTP/1.1\r\n\r\n")
    print(s.recv(4096))
```
