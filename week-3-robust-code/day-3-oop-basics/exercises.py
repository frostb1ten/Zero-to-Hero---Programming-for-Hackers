# =============================================================
# EXERCISES — OOP Basics
# =============================================================


# --- Exercise 1: Create a basic class ---
# Make a class called 'Port' with: number, service, status
# Include a __str__ method that returns "22/tcp (SSH) - open"

class Port:
    def __init__(self, ___):
        ___
        ___
        ___

    def __str__(self):
        return ___

p = Port(22, "SSH", "open")
print(p)
# Expected: 22/tcp (SSH) - open


# --- Exercise 2: Class with methods ---
# Add a method 'is_common' that returns True for ports under 1024

class Service:
    def __init__(self, port, name):
        self.port = port
        self.name = name

    def is_common(self):
        ___

s1 = Service(22, "SSH")
s2 = Service(8080, "HTTP-Alt")
print(f"{s1.name}: common={s1.is_common()}")   # True
print(f"{s2.name}: common={s2.is_common()}")   # False


# --- Exercise 3: Build a complete class ---
# Create a 'Wordlist' class that:
# - Takes a name in __init__
# - Has an empty list of words
# - add(word) method to add a word
# - count() method returns number of words
# - contains(word) returns True/False
# - __str__ returns "Wordlist 'name' (N words)"

___

wl = Wordlist("passwords")
wl.add("admin")
wl.add("password123")
wl.add("letmein")
print(wl)                           # Wordlist 'passwords' (3 words)
print(f"Contains 'admin': {wl.contains('admin')}")   # True
print(f"Contains 'root': {wl.contains('root')}")     # False
print(f"Count: {wl.count()}")       # 3


# --- Exercise 4: Inheritance ---
# Create 'WebScanner' that inherits from 'Scanner'
# It should add a 'url' attribute and override describe()

class Scanner:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"Scanner: {self.name}"

class WebScanner(___):
    def __init__(self, name, url):
        ___
        ___

    def describe(self):
        return ___

ws = WebScanner("DirBuster", "https://target.com")
print(ws.describe())
# Expected: WebScanner: DirBuster -> https://target.com


print("\n--- All exercises complete! ---")
