#!/usr/bin/env python3
"""
Recon Toolkit v1.0 — Capstone Project Solution
A complete recon automation tool combining everything from weeks 1-6.
"""
import argparse
import json
import logging
import os
import re
import socket
import subprocess
import platform
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ===================== SERVICE MAP =====================
SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPCBind",
    135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
}


# ===================== PORT SCANNER =====================
class PortScanner:
    def __init__(self, ip, timeout=1):
        self.ip = ip
        self.timeout = timeout
        self.results = []

    def check_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                if s.connect_ex((self.ip, port)) == 0:
                    return port
        except OSError:
            pass
        return None

    def scan(self, ports, threads=100):
        with ThreadPoolExecutor(max_workers=threads) as pool:
            results = pool.map(self.check_port, ports)
        self.results = sorted([p for p in results if p is not None])
        return self.results

    def grab_banner(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((self.ip, port))

                try:
                    s.settimeout(1)
                    banner = s.recv(1024).decode(errors="ignore").strip()
                    if banner:
                        return banner[:100]
                except socket.timeout:
                    pass

                if port in (80, 8080, 8443):
                    req = f"HEAD / HTTP/1.1\r\nHost: {self.ip}\r\nConnection: close\r\n\r\n"
                    s.send(req.encode())
                    resp = s.recv(4096).decode(errors="ignore")
                    return resp.split("\r\n")[0][:100]
        except Exception:
            pass
        return ""


# ===================== WEB RECON =====================
class WebRecon:
    def __init__(self, target):
        self.target = target

    def check_headers(self, url):
        if not HAS_REQUESTS:
            return {"error": "requests not installed"}
        try:
            r = requests.get(url, timeout=10, verify=False)
            headers = {}
            for h in ["Server", "X-Powered-By", "X-Frame-Options",
                       "Content-Security-Policy", "Strict-Transport-Security",
                       "X-Content-Type-Options", "X-XSS-Protection"]:
                headers[h] = r.headers.get(h, "Not set")
            return {"status": r.status_code, "headers": headers}
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_robots(self, url):
        if not HAS_REQUESTS:
            return []
        try:
            r = requests.get(f"{url}/robots.txt", timeout=10)
            if r.status_code == 200:
                paths = []
                for line in r.text.split("\n"):
                    if "Disallow" in line:
                        path = line.split(":", 1)[1].strip()
                        if path:
                            paths.append(path)
                return paths
        except requests.RequestException:
            pass
        return []

    def extract_links(self, url):
        if not HAS_REQUESTS:
            return []
        try:
            r = requests.get(url, timeout=10, verify=False)
            return re.findall(r'href=["\']([^"\']+)["\']', r.text)
        except requests.RequestException:
            return []


# ===================== REPORTER =====================
class Reporter:
    def __init__(self, target, output_dir="results"):
        self.target = target
        self.output_dir = output_dir
        safe_name = target.replace(".", "_").replace(":", "_")
        date = datetime.now().strftime("%Y-%m-%d")
        self.base_name = f"{safe_name}_{date}"

    def save_json(self, data):
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, f"{self.base_name}.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return path

    def save_csv(self, port_data):
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, f"{self.base_name}.csv")
        with open(path, "w") as f:
            f.write("port,state,service,banner\n")
            for entry in port_data:
                f.write(f"{entry['port']},{entry['state']},"
                        f"{entry['service']},{entry['banner']}\n")
        return path

    def save_text(self, text):
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, f"{self.base_name}.txt")
        with open(path, "w") as f:
            f.write(text)
        return path


# ===================== RECON ENGINE =====================
class ReconEngine:
    def __init__(self, target, ports, threads, timeout, output_dir, verbose):
        self.target = target
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        self.reporter = Reporter(target, output_dir)
        self.report = {"target": target, "timestamp": datetime.now().isoformat()}
        self.logger = logging.getLogger("recon")

    def resolve_dns(self):
        self.logger.info(f"Target: {self.target}")
        try:
            self.ip = socket.gethostbyname(self.target)
            self.report["ip"] = self.ip
            self.logger.info(f"Resolved: {self.ip}")
            return True
        except socket.gaierror:
            self.logger.error(f"Cannot resolve: {self.target}")
            return False

    def ping_host(self):
        if platform.system() == "Windows":
            cmd = ["ping", "-n", "1", "-w", "2000", self.ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "2", self.ip]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            alive = result.returncode == 0
            self.report["alive"] = alive
            self.logger.info(f"Host is {'ALIVE' if alive else 'DOWN'}")
            return alive
        except subprocess.TimeoutExpired:
            self.report["alive"] = False
            return False

    def scan_ports(self):
        scanner = PortScanner(self.ip, self.timeout)
        self.logger.info(f"Scanning {len(self.ports)} ports with {self.threads} threads...")

        open_ports = scanner.scan(self.ports, self.threads)
        self.logger.info(f"Found {len(open_ports)} open ports")

        # Grab banners
        port_results = []
        for port in open_ports:
            banner = scanner.grab_banner(port)
            service = SERVICES.get(port, "Unknown")
            entry = {
                "port": port,
                "state": "open",
                "service": service,
                "banner": banner
            }
            port_results.append(entry)
            self.logger.info(
                f"  {port:<6}/tcp   OPEN   {service:<12} {banner}"
            )

        self.report["ports"] = port_results
        return port_results

    def web_recon(self):
        web = WebRecon(self.target)
        open_ports = [p["port"] for p in self.report.get("ports", [])]

        if 443 in open_ports:
            url = f"https://{self.target}"
        elif 80 in open_ports:
            url = f"http://{self.target}"
        else:
            return

        self.logger.info("HTTP Recon:")

        # Headers
        header_info = web.check_headers(url)
        self.report["http"] = header_info
        if "headers" in header_info:
            for h, v in header_info["headers"].items():
                status = "+" if v != "Not set" else "!"
                self.logger.info(f"    [{status}] {h}: {v}")

        # robots.txt
        robots = web.get_robots(url)
        self.report["robots"] = robots
        if robots:
            self.logger.info(f"robots.txt: {len(robots)} disallowed paths")
            for path in robots[:5]:
                self.logger.info(f"    {path}")

        # Links
        links = web.extract_links(url)
        self.report["links"] = links[:20]
        self.logger.info(f"Links found: {len(links)}")

    def run(self):
        start = time.time()

        print("=" * 50)
        print("  Recon Toolkit v1.0")
        print("=" * 50)

        if not self.resolve_dns():
            return

        self.ping_host()
        self.scan_ports()
        self.web_recon()

        elapsed = time.time() - start
        self.report["duration"] = round(elapsed, 2)

        # Save reports
        json_path = self.reporter.save_json(self.report)
        csv_path = self.reporter.save_csv(self.report.get("ports", []))

        # Text summary
        text = self.build_text_report()
        txt_path = self.reporter.save_text(text)

        self.logger.info(f"\nReports saved:")
        self.logger.info(f"  {json_path}")
        self.logger.info(f"  {csv_path}")
        self.logger.info(f"  {txt_path}")
        self.logger.info(f"\nScan complete in {elapsed:.1f}s")

    def build_text_report(self):
        lines = []
        lines.append("=" * 50)
        lines.append(f"  Recon Report: {self.target}")
        lines.append(f"  Date: {self.report['timestamp']}")
        lines.append("=" * 50)
        lines.append(f"\nIP: {self.report.get('ip', 'N/A')}")
        lines.append(f"Alive: {self.report.get('alive', 'N/A')}")
        lines.append(f"\nOpen Ports:")
        for p in self.report.get("ports", []):
            lines.append(f"  {p['port']}/tcp  {p['service']:<12}  {p['banner']}")
        if self.report.get("http", {}).get("headers"):
            lines.append(f"\nHTTP Headers:")
            for h, v in self.report["http"]["headers"].items():
                lines.append(f"  {h}: {v}")
        if self.report.get("robots"):
            lines.append(f"\nRobots.txt Disallowed:")
            for path in self.report["robots"]:
                lines.append(f"  {path}")
        lines.append(f"\nDuration: {self.report.get('duration', 0)}s")
        return "\n".join(lines)


# ===================== MAIN =====================
def parse_ports(port_str):
    ports = []
    for part in port_str.split(","):
        if "-" in part:
            start, end = part.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports


def main():
    parser = argparse.ArgumentParser(
        description="Recon Toolkit — Automated reconnaissance tool"
    )
    parser.add_argument("target", help="Target hostname or IP")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range (default: 1-1024)")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0,
                        help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("-o", "--output", default="results",
                        help="Output directory (default: results)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    # Parse ports
    ports = parse_ports(args.ports)

    # Run recon
    engine = ReconEngine(
        target=args.target,
        ports=ports,
        threads=args.threads,
        timeout=args.timeout,
        output_dir=args.output,
        verbose=args.verbose
    )
    engine.run()


if __name__ == "__main__":
    main()
