# =============================================================
# EXERCISES — Async & Advanced Concurrency
# =============================================================
import asyncio
import time
import socket
from concurrent.futures import ThreadPoolExecutor


# --- Exercise 1: ThreadPoolExecutor ---
# Scan ports 1-200 on localhost using 50 threads

def check_port(args):
    ip, port = args
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            return port if s.connect_ex((ip, port)) == 0 else None
    except:
        return None

targets = ___  # list of ("127.0.0.1", port) tuples

start = time.time()
with ThreadPoolExecutor(max_workers=___) as pool:
    results = list(pool.map(___, ___))

open_ports = sorted([p for p in results if p is not None])
elapsed = time.time() - start
print(f"Threaded scan: {len(open_ports)} open in {elapsed:.2f}s")


# --- Exercise 2: Basic async function ---
# Write an async function that resolves a hostname

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


# --- Exercise 3: Async port scanner ---
# Write an async scanner for ports 1-100

async def scan_port(ip, port, timeout=0.2):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return ___
    except:
        return ___

async def scan_range(ip, start, end):
    tasks = ___
    results = await asyncio.gather(*tasks)
    return sorted([p for p in results if p is not None])

open_ports = asyncio.run(scan_range("127.0.0.1", 1, 100))
print(f"Async scan: {open_ports}")


# --- Exercise 4: Semaphore rate limiting ---
# Modify the scanner to limit to 50 concurrent connections

async def limited_scan(ip, ports, max_concurrent=50):
    sem = ___

    async def check(port):
        async with ___:
            return await scan_port(ip, port)

    tasks = [check(p) for p in ports]
    results = await asyncio.gather(*tasks)
    return sorted([p for p in results if p is not None])

start = time.time()
result = asyncio.run(limited_scan("127.0.0.1", range(1, 501)))
print(f"Limited scan: {len(result)} open in {time.time()-start:.2f}s")


print("\n--- All exercises complete! ---")
