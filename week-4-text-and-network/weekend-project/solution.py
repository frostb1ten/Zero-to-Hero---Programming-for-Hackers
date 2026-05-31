# =============================================================
# SOLUTION — Week 4 Project: Log Analyzer & Recon Tool
# =============================================================
import re
import os
import json
import subprocess
import platform

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("[!] 'requests' not installed. URL checking disabled.")
    print("    Install with: pip install requests")


SAMPLE_LOG = """2026-05-30 10:00:01 INFO Connection from 192.168.1.100
2026-05-30 10:00:05 ERROR Failed login from 10.0.0.50 user admin
2026-05-30 10:00:10 INFO Email sent to user@example.com
2026-05-30 10:00:15 ERROR Connection refused from 203.0.113.5
2026-05-30 10:00:20 INFO Report sent to security@corp.org
2026-05-30 10:00:25 ERROR Failed login from 10.0.0.50 user root
2026-05-30 10:00:30 INFO Connection from 192.168.1.100 port 443
"""


def create_sample_log(filename="sample.log"):
    with open(filename, "w") as f:
        f.write(SAMPLE_LOG)
    print(f"[+] Created {filename}")
    return filename


def parse_log(filename):
    with open(filename, "r") as f:
        content = f.read()
        lines = content.strip().split("\n")

    # Extract IPs
    ips = set(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", content))

    # Extract emails
    emails = re.findall(r"[\w.-]+@[\w.-]+\.\w+", content)

    # Find error lines
    errors = [line for line in lines if re.search(r"error|failed", line, re.IGNORECASE)]

    return {
        "unique_ips": sorted(ips),
        "emails": emails,
        "errors": errors,
        "total_lines": len(lines)
    }


def ping_host(ip):
    if platform.system() == "Windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def dns_lookup(ip):
    try:
        result = subprocess.run(
            ["nslookup", ip],
            capture_output=True, text=True, timeout=5
        )
        # Try to find the hostname in the output
        match = re.search(r"Name:\s+(.+)", result.stdout)
        if match:
            return match.group(1).strip()
        return "No reverse DNS"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "Lookup failed"


def check_url(url):
    if not HAS_REQUESTS:
        return {"error": "requests library not installed"}

    try:
        r = requests.get(url, timeout=10)

        # Check security headers
        security_headers = {}
        for header in ["Server", "X-Powered-By", "X-Frame-Options",
                       "Content-Security-Policy", "Strict-Transport-Security"]:
            security_headers[header] = r.headers.get(header, "Not set")

        # Extract links
        links = re.findall(r'href=["\']([^"\']+)["\']', r.text)

        return {
            "url": url,
            "status_code": r.status_code,
            "headers": security_headers,
            "links_found": len(links),
            "sample_links": links[:10]
        }
    except requests.RequestException as e:
        return {"url": url, "error": str(e)}


def save_report(data, filename="recon_report.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Report saved to {filename}")


def main():
    print("=" * 45)
    print("  Log Analyzer & Recon Tool")
    print("=" * 45)

    # Step 1: Parse log
    log_file = create_sample_log()
    parsed = parse_log(log_file)

    print(f"\n[*] Log Analysis ({parsed['total_lines']} lines):")
    print(f"    Unique IPs: {parsed['unique_ips']}")
    print(f"    Emails: {parsed['emails']}")
    print(f"    Errors: {len(parsed['errors'])} lines")
    for err in parsed['errors']:
        print(f"      > {err}")

    # Step 2: Ping IPs
    print(f"\n[*] Host Discovery:")
    host_results = {}
    for ip in parsed['unique_ips']:
        alive = ping_host(ip)
        dns = dns_lookup(ip) if alive else "Skipped"
        status = "UP" if alive else "DOWN"
        host_results[ip] = {"alive": alive, "dns": dns}
        print(f"    {ip}: {status} (DNS: {dns})")

    # Step 3: URL check
    url_result = {}
    if HAS_REQUESTS:
        print(f"\n[*] URL Recon:")
        url_result = check_url("https://httpbin.org")
        print(f"    Status: {url_result.get('status_code', 'N/A')}")
        if "headers" in url_result:
            for h, v in url_result["headers"].items():
                print(f"    {h}: {v}")

    # Step 4: Save report
    report = {
        "log_analysis": parsed,
        "host_discovery": host_results,
        "url_recon": url_result
    }
    save_report(report)

    # Cleanup
    os.remove(log_file)
    print("\n[*] Done!")


if __name__ == "__main__":
    main()
