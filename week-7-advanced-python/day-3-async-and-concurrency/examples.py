# =============================================================
# EXAMPLES — Async & Advanced Concurrency
# =============================================================
import asyncio
import socket
import time
from concurrent.futures import ThreadPoolExecutor
import hashlib


# --- 1. Speed comparison: sequential vs threaded ---
print("[1] Sequential vs Threaded port scan (localhost 1-500):")

def check_port_sync(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            return s.connect_ex((ip, port)) == 0
    except:
        return False

# Sequential
start = time.time()
seq_open = []
for p in range(1, 501):
    if check_port_sync("127.0.0.1", p):
        seq_open.append(p)
seq_time = time.time() - start

# Threaded
def check_wrapper(args):
    ip, port = args
    if check_port_sync(ip, port):
        return port
    return None

start = time.time()
targets = [("127.0.0.1", p) for p in range(1, 501)]
with ThreadPoolExecutor(max_workers=100) as pool:
    results = list(pool.map(check_wrapper, targets))
thread_open = sorted([p for p in results if p])
thread_time = time.time() - start

print(f"  Sequential: {seq_time:.2f}s (found {len(seq_open)} open)")
print(f"  Threaded:   {thread_time:.2f}s (found {len(thread_open)} open)")
print(f"  Speedup:    {seq_time / thread_time:.1f}x")
print()


# --- 2. Async port scanner ---
print("[2] Async port scan (localhost 1-500):")

async def async_check_port(ip, port, timeout=0.1):
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

async def async_scan(ip, ports):
    tasks = [async_check_port(ip, p) for p in ports]
    results = await asyncio.gather(*tasks)
    return sorted([p for p in results if p])

start = time.time()
async_open = asyncio.run(async_scan("127.0.0.1", range(1, 501)))
async_time = time.time() - start
print(f"  Async:      {async_time:.2f}s (found {len(async_open)} open)")
print()


# --- 3. Async with semaphore (rate limiting) ---
print("[3] Async with semaphore:")

async def limited_scan(ip, ports, max_concurrent=200):
    sem = asyncio.Semaphore(max_concurrent)

    async def check(port):
        async with sem:
            return await async_check_port(ip, port)

    tasks = [check(p) for p in ports]
    results = await asyncio.gather(*tasks)
    return sorted([p for p in results if p])

start = time.time()
limited_open = asyncio.run(limited_scan("127.0.0.1", range(1, 1001), 200))
limited_time = time.time() - start
print(f"  1000 ports, 200 concurrent: {limited_time:.2f}s, {len(limited_open)} open")
print()


# --- 4. CPU-bound: hash cracking with multiprocessing ---
print("[4] Hash cracking speed comparison:")

target = hashlib.md5("zebra".encode()).hexdigest()
words = [f"word{i}" for i in range(10000)] + ["zebra"]

# Single thread
start = time.time()
found = None
for w in words:
    if hashlib.md5(w.encode()).hexdigest() == target:
        found = w
        break
single_time = time.time() - start
print(f"  Single-thread: found '{found}' in {single_time:.4f}s")

# ThreadPool (I/O doesn't help much for CPU work, but let's see)
def crack_word(args):
    word, target_hash = args
    if hashlib.md5(word.encode()).hexdigest() == target_hash:
        return word
    return None

start = time.time()
with ThreadPoolExecutor(max_workers=4) as pool:
    results = pool.map(crack_word, [(w, target) for w in words])
    found = next((r for r in results if r), None)
pool_time = time.time() - start
print(f"  ThreadPool:    found '{found}' in {pool_time:.4f}s")
