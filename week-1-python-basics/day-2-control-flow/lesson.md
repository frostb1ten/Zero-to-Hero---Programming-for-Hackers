# Day 2: Control Flow

## The Core Idea
Control flow lets your code make decisions and repeat actions.
Two building blocks: **conditionals** (if/else) and **loops** (for/while).

## if / elif / else
```python
status_code = 200

if status_code == 200:
    print("OK — target is alive")
elif status_code == 403:
    print("Forbidden — access denied")
elif status_code == 404:
    print("Not Found")
else:
    print(f"Got status code: {status_code}")
```

## Comparison Operators
```python
==    # equals
!=    # not equals
>     # greater than
<     # less than
>=    # greater or equal
<=    # less or equal
in    # is inside a collection
not   # flips True/False
```

## Combining Conditions
```python
port = 443
protocol = "https"

if port == 443 and protocol == "https":
    print("Secure connection")

if port == 80 or port == 8080:
    print("HTTP port detected")

if not is_blocked:
    print("Access granted")
```

## for Loops — Do Something For Each Item
```python
ports = [22, 80, 443, 8080]

for port in ports:
    print(f"Scanning port {port}")
```

## range() — Generate Number Sequences
```python
# 0 to 4
for i in range(5):
    print(i)

# 1 to 10
for i in range(1, 11):
    print(i)

# 0 to 100, stepping by 10
for i in range(0, 101, 10):
    print(i)
```

## while Loops — Repeat Until a Condition Changes
```python
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    password = input("Enter password: ")
    if password == "admin123":
        print("Access granted!")
        break   # exit the loop immediately
    attempts += 1
    print(f"Wrong. {max_attempts - attempts} attempts left.")
else:
    print("Account locked.")  # runs if loop ends WITHOUT break
```

## break, continue, pass
```python
for port in range(1, 1001):
    if port == 445:
        print("Found SMB!")
        break       # stop the loop entirely

    if port % 100 != 0:
        continue    # skip to next iteration

    print(f"Checked {port} ports...")

# pass = "do nothing" placeholder
if is_admin:
    pass  # TODO: implement admin logic later
```
