# =============================================================
# EXAMPLES — Decorators & Generators
# =============================================================
import functools
import time
import socket


# --- 1. Timer decorator ---
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  [TIMER] {func.__name__}: {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_scan(count):
    total = 0
    for i in range(count):
        total += i
    return total

print("[1] Timer decorator:")
slow_scan(1_000_000)
print()


# --- 2. Retry decorator ---
def retry(max_attempts=3, delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  [RETRY] Attempt {attempt}/{max_attempts}: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.1)
def flaky_connect(ip, port):
    """Simulates a connection that fails sometimes."""
    import random
    if random.random() < 0.7:  # 70% failure rate
        raise ConnectionRefusedError(f"Cannot connect to {ip}:{port}")
    return f"Connected to {ip}:{port}"

print("[2] Retry decorator:")
result = flaky_connect("10.0.0.1", 80)
print(f"  Result: {result}")
print()


# --- 3. Stacking decorators ---
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [LOG] → {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"  [LOG] ← {func.__name__}() = {result}")
        return result
    return wrapper

@log_call
@timer
def resolve_host(hostname):
    return socket.gethostbyname(hostname)

print("[3] Stacked decorators:")
resolve_host("google.com")
print()


# --- 4. Generator basics ---
print("[4] Generator vs list:")

# List — all in memory
ip_list = [f"10.0.0.{i}" for i in range(1, 6)]
print(f"  List: {ip_list} (type: {type(ip_list).__name__})")

# Generator — lazy
def gen_ips(base, start, end):
    for i in range(start, end + 1):
        yield f"{base}.{i}"

ip_gen = gen_ips("10.0.0", 1, 5)
print(f"  Generator: {ip_gen} (type: {type(ip_gen).__name__})")
print(f"  Consumed: {list(ip_gen)}")
print()


# --- 5. Generator pipeline ---
print("[5] Generator pipeline:")

def number_source(n):
    """Generate numbers 1 to n."""
    for i in range(1, n + 1):
        yield i

def only_odd(numbers):
    """Filter to only odd numbers."""
    for n in numbers:
        if n % 2 != 0:
            yield n

def squared(numbers):
    """Square each number."""
    for n in numbers:
        yield n ** 2

# Chain them: source → filter → transform
pipeline = squared(only_odd(number_source(10)))
print(f"  Odd squares 1-10: {list(pipeline)}")
print()


# --- 6. Wordlist generator ---
print("[6] Wordlist mutation generator:")

def mutate_words(words):
    for word in words:
        yield word
        yield word.capitalize()
        yield word.upper()
        yield word + "123"
        yield word + "!"
        yield word.replace("a", "@").replace("e", "3")

base_words = ["password", "admin", "test"]
mutations = list(mutate_words(base_words))
print(f"  {len(base_words)} words → {len(mutations)} mutations")
for m in mutations[:8]:
    print(f"    {m}")
print(f"    ... ({len(mutations) - 8} more)")
