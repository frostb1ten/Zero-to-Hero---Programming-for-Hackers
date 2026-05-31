# Day 2: Dictionaries & Sets

## The Core Idea
**Dictionaries** store key-value pairs — like a phonebook.
**Sets** store unique values — no duplicates allowed.

## Dictionaries
```python
# Creating
host = {
    "ip": "192.168.1.1",
    "hostname": "web-server",
    "ports": [22, 80, 443],
    "os": "Linux"
}

# Accessing
print(host["ip"])           # "192.168.1.1"
print(host.get("os"))       # "Linux"
print(host.get("mac", "N/A"))  # "N/A" (default if key missing)

# Modifying
host["status"] = "up"       # add new key
host["os"] = "Ubuntu 22.04" # update existing
del host["hostname"]        # delete a key
```

## Looping Through Dicts
```python
host = {"ip": "10.0.0.1", "port": 22, "service": "SSH"}

# Keys only
for key in host:
    print(key)

# Values only
for value in host.values():
    print(value)

# Both key and value
for key, value in host.items():
    print(f"  {key}: {value}")
```

## Nested Dictionaries
```python
scan_results = {
    "10.0.0.1": {"ports": [22, 80], "os": "Linux"},
    "10.0.0.2": {"ports": [3389], "os": "Windows"},
}

# Access nested data
print(scan_results["10.0.0.1"]["os"])  # "Linux"
```

## Dictionary Comprehensions
```python
ports = [22, 80, 443]
port_status = {port: "open" for port in ports}
# {22: 'open', 80: 'open', 443: 'open'}
```

## Sets — Unique Values Only
```python
found_ports = {22, 80, 443, 80, 22}
print(found_ports)  # {80, 443, 22} — duplicates removed

# Useful operations
set_a = {22, 80, 443}
set_b = {80, 443, 8080}

set_a | set_b   # union:        {22, 80, 443, 8080}
set_a & set_b   # intersection: {80, 443}
set_a - set_b   # difference:   {22}
```

## When to Use What
| Structure | Use When |
|-----------|----------|
| List `[]` | Ordered collection, duplicates OK |
| Tuple `()` | Data that shouldn't change |
| Dict `{}` | Key-value lookups |
| Set `{}` | Need unique values or set math |
