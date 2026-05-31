# =============================================================
# SOLUTIONS — Async & Advanced Concurrency
# =============================================================
import asyncio
import time
import socket
from concurrent.futures import ThreadPoolExecutor

# --- Exercise 1 ---
def check_port(args):
    ip, port = args
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            return port if s.connect_ex((ip, port)) == 0 else None
    except:
        return None

targets = [("127.0.0.1", p) for p in range(1, 201)]
start = time.time()
with ThreadPoolExecutor(max_workers=50) as pool:
    results = list(pool.map(check_port, targets))
open_ports = sorted([p for p in results if p is not None])
elapsed = time.time() - start
print(f"Threaded scan: {len(open_ports)} open in {elapsed:.2f}s")

# --- Exercise 2 ---
async def async_resolve(hostname):
    loop = asyncio.get_event_loop()
    ip = await loop.getaddrinfo(hostname, None)
    return ip[0][4][0]

async def resolve_many():
    hosts = ["google.com", "github.com", "cloudflare.com"]
    tasks = [async_resolve(h) for h in hosts]
    results = await asyncio.gather(*tasks)
    for host, ip in zip(hosts, results):
        print(f"  {host} → {ip}")

asyncio.run(resolve_many())

# --- Exercise 3 ---
async def scan_port(ip, port, timeout=0.2):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return port
    except:
        return None

async def scan_range(ip, start, end):
    tasks = [scan_port(ip, p) for p in range(start, end + 1)]
    results = await asyncio.gather(*tasks)
    return sorted([p for p in results if p is not None])

open_ports = asyncio.run(scan_range("127.0.0.1", 1, 100))
print(f"Async scan: {open_ports}")

# --- Exercise 4 ---
async def limited_scan(ip, ports, max_concurrent=50):
    sem = asyncio.Semaphore(max_concurrent)
    async def check(port):
        async with sem:
            return await scan_port(ip, port)
    tasks = [check(p) for p in ports]
    results = await asyncio.gather(*tasks)
    return sorted([p for p in results if p is not None])

start = time.time()
result = asyncio.run(limited_scan("127.0.0.1", range(1, 501)))
print(f"Limited scan: {len(result)} open in {time.time()-start:.2f}s")

print("\n--- All exercises complete! ---")
