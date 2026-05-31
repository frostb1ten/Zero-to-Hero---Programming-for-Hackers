# =============================================================
# SOLUTION — Week 5 Project: Full Port Scanner Tool
# Usage: python solution.py <target> [--ports 1-1024] [--threads 100]
# =============================================================
import socket
import sys
import time
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPCBind",
    135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    27017: "MongoDB"
}


class PortScanner:
    def __init__(self, target, ports, threads=100, timeout=1):
        self.target = target
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        self.results = []

        # Resolve hostname
        try:
            self.ip = socket.gethostbyname(target)
        except socket.gaierror:
            print(f"[!] Cannot resolve: {target}")
            sys.exit(1)

    def check_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                if s.connect_ex((self.ip, port)) == 0:
                    return port
        except OSError:
            pass
        return None

    def grab_banner(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((self.ip, port))

                # Try auto-receive first
                try:
                    s.settimeout(1)
                    banner = s.recv(1024).decode(errors="ignore").strip()
                    if banner:
                        return banner[:80]
                except socket.timeout:
                    pass

                # Try HTTP probe
                if port in (80, 8080, 8443, 443):
                    request = f"HEAD / HTTP/1.1\r\nHost: {self.target}\r\nConnection: close\r\n\r\n"
                    s.send(request.encode())
                    response = s.recv(4096).decode(errors="ignore")
                    first_line = response.split("\r\n")[0]
                    return first_line[:80]

        except Exception:
            pass
        return ""

    def scan(self):
        print(f"[*] Target: {self.target} ({self.ip})")
        print(f"[*] Scanning {len(self.ports)} ports with {self.threads} threads...")
        print()

        start = time.time()

        # Phase 1: Find open ports
        with ThreadPoolExecutor(max_workers=self.threads) as pool:
            results = pool.map(self.check_port, self.ports)

        open_ports = sorted([p for p in results if p is not None])

        # Phase 2: Grab banners
        for port in open_ports:
            banner = self.grab_banner(port)
            service = SERVICES.get(port, "Unknown")
            result = {
                "port": port,
                "state": "open",
                "service": service,
                "banner": banner
            }
            self.results.append(result)
            print(f"[+]  {port:<6}/tcp   OPEN   {service:<12} {banner}")

        elapsed = time.time() - start
        print(f"\n[*] Scan complete: {len(open_ports)} open ports in {elapsed:.1f}s")

        return self.results

    def save_report(self, filename=None):
        if not filename:
            filename = f"scan_{self.target.replace('.', '_')}.json"

        report = {
            "target": self.target,
            "ip": self.ip,
            "timestamp": datetime.now().isoformat(),
            "ports_scanned": len(self.ports),
            "open_ports": len(self.results),
            "results": self.results
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

        print(f"[+] Results saved to {filename}")
        return filename


def parse_port_range(port_str):
    """Parse port specification: '1-1024', '22,80,443', or '80'."""
    ports = []
    for part in port_str.split(","):
        if "-" in part:
            start, end = part.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports


def print_banner():
    print("=" * 45)
    print("  PortScanner v1.0")
    print("=" * 45)


def main():
    print_banner()

    # Parse arguments
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <target> [--ports 1-1024] [--threads 100]")
        print(f"\nExamples:")
        print(f"  python {sys.argv[0]} scanme.nmap.org")
        print(f"  python {sys.argv[0]} 10.0.0.1 --ports 22,80,443")
        print(f"  python {sys.argv[0]} 10.0.0.1 --ports 1-100 --threads 50")
        sys.exit(1)

    target = sys.argv[1]
    ports = list(range(1, 1025))  # default
    threads = 100

    # Parse optional flags
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--ports" and i + 1 < len(args):
            ports = parse_port_range(args[i + 1])
            i += 2
        elif args[i] == "--threads" and i + 1 < len(args):
            threads = int(args[i + 1])
            i += 2
        else:
            i += 1

    # Run scan
    scanner = PortScanner(target, ports, threads)
    scanner.scan()
    scanner.save_report()


if __name__ == "__main__":
    main()
