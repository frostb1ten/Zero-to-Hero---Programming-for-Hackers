# Day 3: OOP Basics

## The Core Idea
A **class** is a blueprint. An **object** is a thing built from that blueprint.
OOP lets you bundle data + functions that belong together.

## Your First Class
```python
class Scanner:
    def __init__(self, target_ip):
        self.target = target_ip
        self.results = []

    def scan_port(self, port):
        # In real life, we'd check if the port is open
        self.results.append({"port": port, "status": "open"})
        print(f"[*] Scanned {self.target}:{port}")

    def report(self):
        print(f"\n[+] Results for {self.target}:")
        for r in self.results:
            print(f"    Port {r['port']}: {r['status']}")

# Using the class
s = Scanner("192.168.1.1")
s.scan_port(22)
s.scan_port(80)
s.report()
```

## __init__ — The Constructor
```python
class Host:
    def __init__(self, ip, hostname="unknown"):
        self.ip = ip           # 'self' = this specific object
        self.hostname = hostname
        self.ports = []

h1 = Host("10.0.0.1", "web-server")
h2 = Host("10.0.0.2")  # hostname defaults to "unknown"
```

## Methods — Functions Inside a Class
```python
class PasswordChecker:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def check(self, password):
        issues = []
        if len(password) < self.min_length:
            issues.append(f"Too short (min {self.min_length})")
        if not any(c.isupper() for c in password):
            issues.append("No uppercase letter")
        if not any(c.isdigit() for c in password):
            issues.append("No digit")
        return issues

checker = PasswordChecker(min_length=10)
problems = checker.check("weak")
# ['Too short (min 10)', 'No uppercase letter', 'No digit']
```

## __str__ — How Your Object Prints
```python
class Target:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"Target({self.ip}:{self.port})"

t = Target("10.0.0.1", 443)
print(t)  # Target(10.0.0.1:443)
```

## Inheritance — Building on Existing Classes
```python
class Scanner:
    def __init__(self, target):
        self.target = target

    def scan(self):
        print(f"Scanning {self.target}...")

class PortScanner(Scanner):
    def __init__(self, target, ports):
        super().__init__(target)  # call parent's __init__
        self.ports = ports

    def scan(self):
        for port in self.ports:
            print(f"  Checking {self.target}:{port}")

ps = PortScanner("10.0.0.1", [22, 80, 443])
ps.scan()
```
