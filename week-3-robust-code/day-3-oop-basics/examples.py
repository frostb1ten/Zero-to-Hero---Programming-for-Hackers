# =============================================================
# EXAMPLES — OOP Basics
# =============================================================

# --- 1. Simple class ---
class Host:
    def __init__(self, ip, hostname="unknown", os_name="unknown"):
        self.ip = ip
        self.hostname = hostname
        self.os = os_name
        self.open_ports = []

    def add_port(self, port, service="unknown"):
        self.open_ports.append({"port": port, "service": service})

    def __str__(self):
        return f"{self.hostname} ({self.ip}) - {len(self.open_ports)} open ports"

    def summary(self):
        print(f"\n  Host: {self.hostname}")
        print(f"  IP:   {self.ip}")
        print(f"  OS:   {self.os}")
        print(f"  Open ports:")
        for p in self.open_ports:
            print(f"    {p['port']}/tcp — {p['service']}")


# Create hosts
web = Host("10.0.0.1", "web-server", "Linux")
web.add_port(22, "SSH")
web.add_port(80, "HTTP")
web.add_port(443, "HTTPS")

db = Host("10.0.0.2", "db-server", "Linux")
db.add_port(3306, "MySQL")

# Use __str__
print("[1] Hosts:")
print(f"    {web}")
print(f"    {db}")

# Detailed summary
web.summary()
print()

# --- 2. Class with methods that return values ---
class IPRange:
    def __init__(self, base, start, end):
        self.base = base
        self.start = start
        self.end = end

    def generate(self):
        return [f"{self.base}.{i}" for i in range(self.start, self.end + 1)]

    def count(self):
        return self.end - self.start + 1

print("[2] IP Range:")
subnet = IPRange("192.168.1", 1, 10)
print(f"    {subnet.count()} IPs: {subnet.generate()}")
print()

# --- 3. Inheritance ---
class Tool:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def banner(self):
        print(f"{'=' * 30}")
        print(f"  {self.name} v{self.version}")
        print(f"{'=' * 30}")

class PortScanner(Tool):
    def __init__(self, version="1.0"):
        super().__init__("PortScanner", version)
        self.results = []

    def scan(self, ip, ports):
        self.banner()
        for port in ports:
            result = {"ip": ip, "port": port, "status": "open"}
            self.results.append(result)
            print(f"  [+] {ip}:{port} — open")

print("[3] Inheritance:")
scanner = PortScanner("2.0")
scanner.scan("10.0.0.1", [22, 80, 443])
