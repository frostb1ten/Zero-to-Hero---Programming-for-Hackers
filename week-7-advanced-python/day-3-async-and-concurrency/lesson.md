# Day 3: Async & Advanced Concurrency

## Why This Matters
Scanning 65,535 ports one at a time takes forever. Threading helps,
but asyncio can handle **thousands** of concurrent connections with
less overhead. Faster scans, faster brute-force, faster recon.

## Threading Review (From Week 5)
```python
from concurrent.futures import ThreadPoolExecutor

def scan(port):
    # check if port is open
    pass

with ThreadPoolExecutor(max_workers=200) as pool:
    pool.map(scan, range(1, 65536))
```

## asyncio — The Event Loop
```python
import asyncio

async def scan_port(ip, port):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=1.0
        )
        writer.close()
        await writer.wait_closed()
        return port
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None

async def main():
    ip = "scanme.nmap.org"
    tasks = [scan_port(ip, p) for p in range(1, 1025)]
    results = await asyncio.gather(*tasks)
    open_ports = [p for p in results if p]
    print(f"Open: {open_ports}")

asyncio.run(main())
```

## Semaphores — Rate Limiting
```python
import asyncio

async def scan_port(sem, ip, port):
    async with sem:  # only N concurrent scans
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=1.0
            )
            writer.close()
            await writer.wait_closed()
            return port
        except:
            return None

async def main():
    sem = asyncio.Semaphore(500)  # max 500 concurrent
    ip = "scanme.nmap.org"
    tasks = [scan_port(sem, ip, p) for p in range(1, 65536)]
    results = await asyncio.gather(*tasks)
    open_ports = sorted([p for p in results if p])
    print(f"Open: {open_ports}")

asyncio.run(main())
```

## Multiprocessing — True Parallelism
```python
from multiprocessing import Pool
import hashlib

def crack_chunk(args):
    """Try a chunk of passwords against a hash."""
    target_hash, words = args
    for word in words:
        if hashlib.md5(word.encode()).hexdigest() == target_hash:
            return word
    return None

# Split wordlist into chunks for each CPU core
wordlist = ["password", "admin", "letmein", ...]
chunks = [wordlist[i::4] for i in range(4)]  # 4 cores

with Pool(4) as pool:
    results = pool.map(crack_chunk, [(target, c) for c in chunks])
    found = [r for r in results if r]
```

## Queue — Producer/Consumer Pattern
```python
import queue
import threading

work_queue = queue.Queue()
results = []

def worker():
    while True:
        item = work_queue.get()
        if item is None:
            break
        # process item
        results.append(process(item))
        work_queue.task_done()

# Start workers
threads = []
for _ in range(10):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Feed work
for port in range(1, 1025):
    work_queue.put(port)

# Signal workers to stop
for _ in range(10):
    work_queue.put(None)

for t in threads:
    t.join()
```

## When to Use What
| Approach | Best For | Speed |
|----------|----------|-------|
| Sequential | Simple scripts, < 100 items | Slowest |
| ThreadPoolExecutor | I/O-bound (network, files), 100-10K items | Fast |
| asyncio | Many concurrent connections, 1K-100K | Fastest for I/O |
| multiprocessing | CPU-bound (hashing, crypto), needs real parallelism | Uses all cores |
