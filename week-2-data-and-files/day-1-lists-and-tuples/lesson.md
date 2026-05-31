# Day 1: Lists & Tuples

## The Core Idea
Lists and tuples hold multiple values in order.
**Lists** are mutable (you can change them). **Tuples** are immutable (locked in).

## Lists — Your Workhorse
```python
ports = [22, 80, 443, 8080]
targets = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
mixed = ["ssh", 22, True]  # can mix types (but usually don't)
empty = []
```

## Accessing Items (Indexing)
```python
ports = [22, 80, 443, 8080]
ports[0]    # 22        (first item)
ports[-1]   # 8080      (last item)
ports[1:3]  # [80, 443] (slice: index 1 up to but not including 3)
```

## Modifying Lists
```python
ports = [22, 80, 443]

ports.append(8080)       # add to end → [22, 80, 443, 8080]
ports.insert(0, 21)      # insert at position → [21, 22, 80, 443, 8080]
ports.remove(80)         # remove by value → [21, 22, 443, 8080]
popped = ports.pop()     # remove & return last → 8080
ports.extend([3306, 5432])  # add multiple items
```

## Useful List Operations
```python
ports = [443, 22, 80, 22, 8080]

len(ports)        # 5
sorted(ports)     # [22, 22, 80, 443, 8080] (returns new list)
ports.sort()      # sorts in place
ports.count(22)   # 2
ports.index(80)   # position of 80
22 in ports       # True
```

## List Comprehensions — The Pythonic Way
```python
# Instead of this:
squares = []
for n in range(1, 6):
    squares.append(n ** 2)

# Write this:
squares = [n ** 2 for n in range(1, 6)]
# [1, 4, 9, 16, 25]

# With a condition:
open_ports = [p for p in all_ports if p < 1024]
```

## Tuples — Immutable Lists
```python
# Use when data shouldn't change
server = ("192.168.1.1", 443, "HTTPS")
ip, port, protocol = server  # unpacking

# Common use: return multiple values from functions
def get_target():
    return ("10.0.0.1", 22)

ip, port = get_target()
```

## Looping With enumerate()
```python
targets = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

for index, ip in enumerate(targets):
    print(f"  [{index + 1}] {ip}")
# [1] 10.0.0.1
# [2] 10.0.0.2
# [3] 10.0.0.3
```
