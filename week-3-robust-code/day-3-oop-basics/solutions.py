# =============================================================
# SOLUTIONS — OOP Basics
# =============================================================

# --- Exercise 1 ---
class Port:
    def __init__(self, number, service, status):
        self.number = number
        self.service = service
        self.status = status

    def __str__(self):
        return f"{self.number}/tcp ({self.service}) - {self.status}"

p = Port(22, "SSH", "open")
print(p)

# --- Exercise 2 ---
class Service:
    def __init__(self, port, name):
        self.port = port
        self.name = name

    def is_common(self):
        return self.port < 1024

s1 = Service(22, "SSH")
s2 = Service(8080, "HTTP-Alt")
print(f"{s1.name}: common={s1.is_common()}")
print(f"{s2.name}: common={s2.is_common()}")

# --- Exercise 3 ---
class Wordlist:
    def __init__(self, name):
        self.name = name
        self.words = []

    def add(self, word):
        self.words.append(word)

    def count(self):
        return len(self.words)

    def contains(self, word):
        return word in self.words

    def __str__(self):
        return f"Wordlist '{self.name}' ({self.count()} words)"

wl = Wordlist("passwords")
wl.add("admin")
wl.add("password123")
wl.add("letmein")
print(wl)
print(f"Contains 'admin': {wl.contains('admin')}")
print(f"Contains 'root': {wl.contains('root')}")
print(f"Count: {wl.count()}")

# --- Exercise 4 ---
class Scanner:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"Scanner: {self.name}"

class WebScanner(Scanner):
    def __init__(self, name, url):
        super().__init__(name)
        self.url = url

    def describe(self):
        return f"WebScanner: {self.name} -> {self.url}"

ws = WebScanner("DirBuster", "https://target.com")
print(ws.describe())

print("\n--- All exercises complete! ---")
