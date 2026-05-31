#!/usr/bin/env python3
"""Week 7 Project: Async Mass Scanner"""
import argparse
import asyncio
import functools
import json
import time
from datetime import datetime


SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt"
}


# --- Decorators ---
def timer(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"\n[TIMER] {func.__name__}: {elapsed:.2f}s")
        return result, elapsed
    return wrapper


# --- Generators ---
def target_generator(subnet, ports):
    """Yield (ip, port) tuples for a full /24."""
    for host in range(1, 255):
        for port in ports:
            yield (f"{subnet}.{host}", port)


# --- Async Scanner ---
async def check_port(sem, ip, port, timeout=1.0):
    async with sem:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=timeout
            )
            # Try banner grab
            banner = ""
            try:
                if port in (80, 8080):
                    writer.write(f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n".encode())
                    await writer.drain()

                data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                banner = data.decode(errors="ignore").strip().split("\n")[0][:80]
            except:
                pass

            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass

            return {
                "ip": ip,
                "port": port,
                "state": "open",
                "service": SERVICES.get(port, "Unknown"),
                "banner": banner
            }
        except:
            return None


@timer
async def scan_subnet(subnet, ports, max_concurrent=500):
    sem = asyncio.Semaphore(max_concurrent)
    targets = list(target_generator(subnet, ports))

    print(f"[*] Scanning {subnet}.0/24 on ports {ports}")
    print(f"[*] {len(targets)} total probes, {max_concurrent} concurrent max")
    print()

    tasks = [check_port(sem, ip, port) for ip, port in targets]
    results = await asyncio.gather(*tasks)

    open_results = [r for r in results if r is not None]
    open_results.sort(key=lambda x: (x["ip"], x["port"]))

    for r in open_results:
        banner = f"  {r['banner']}" if r['banner'] else ""
        print(f"  {r['ip']}:{r['port']:<6} OPEN   {r['service']:<10}{banner}")

    # Unique hosts with open ports
    hosts = set(r["ip"] for r in open_results)
    print(f"\n[*] {len(open_results)} open ports across {len(hosts)} hosts")

    return open_results


def main():
    parser = argparse.ArgumentParser(description="Async Mass Scanner")
    parser.add_argument("subnet", help="Subnet base (e.g., 192.168.1)")
    parser.add_argument("-p", "--ports", default="22,80,443",
                        help="Comma-separated ports (default: 22,80,443)")
    parser.add_argument("-c", "--concurrent", type=int, default=500,
                        help="Max concurrent connections (default: 500)")
    parser.add_argument("-o", "--output", default="subnet_scan.json",
                        help="Output file")
    args = parser.parse_args()

    ports = [int(p) for p in args.ports.split(",")]

    results, elapsed = asyncio.run(
        scan_subnet(args.subnet, ports, args.concurrent)
    )

    # Save report
    report = {
        "subnet": f"{args.subnet}.0/24",
        "ports_scanned": ports,
        "timestamp": datetime.now().isoformat(),
        "duration": round(elapsed, 2),
        "total_open": len(results),
        "results": results
    }
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[+] Saved to {args.output}")


if __name__ == "__main__":
    main()
