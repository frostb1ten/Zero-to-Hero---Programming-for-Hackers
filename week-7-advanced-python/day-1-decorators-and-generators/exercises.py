# =============================================================
# EXERCISES — Decorators & Generators
# =============================================================
import functools
import time


# --- Exercise 1: Write a timer decorator ---
# It should print how long the function took

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = ___
        result = ___
        elapsed = ___
        print(f"[TIMER] {func.__name__}: {elapsed:.4f}s")
        return result
    return wrapper

@timer
def waste_time():
    total = sum(range(500_000))
    return total

waste_time()


# --- Exercise 2: Write a logger decorator ---
# Print the function name and args when called

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {___}({args})")
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

add(10, 20)
# Expected: [LOG] Calling add((10, 20))


# --- Exercise 3: Retry decorator ---
# Complete the retry decorator to catch exceptions and retry

def retry(attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                ___:
                    return func(*args, **kwargs)
                ___ Exception as e:
                    print(f"  Attempt {i+1} failed: {e}")
            return None
        return wrapper
    return decorator

call_count = 0

@retry(attempts=3)
def unreliable():
    global call_count
    call_count += 1
    if call_count < 3:
        raise RuntimeError("Not yet!")
    return "Success!"

print(unreliable())


# --- Exercise 4: Write a generator ---
# Generate IP addresses from base.start to base.end

def ip_range(base, start, end):
    for i in range(start, end + 1):
        ___

ips = list(ip_range("192.168.1", 1, 5))
print(f"IPs: {ips}")
# Expected: ['192.168.1.1', '192.168.1.2', ..., '192.168.1.5']


# --- Exercise 5: Generator pipeline ---
# Chain: generate words → filter short ones → add "123"

def words():
    yield "hi"
    yield "admin"
    yield "root"
    yield "me"
    yield "password"

def filter_long(gen, min_len=4):
    for word in gen:
        if ___:
            yield word

def append_numbers(gen):
    for word in gen:
        yield ___

pipeline = append_numbers(filter_long(words()))
print(f"Pipeline: {list(pipeline)}")
# Expected: ['admin123', 'root123', 'password123']


# --- Exercise 6: Password mutation generator ---
# Write a generator that yields all mutations of a word

def mutate(word):
    ___  # original
    ___  # capitalized
    ___  # word + "123"
    ___  # word + "!"
    ___  # uppercase

mutations = list(mutate("hack"))
print(f"Mutations: {mutations}")
# Expected: ['hack', 'Hack', 'hack123', 'hack!', 'HACK']


print("\n--- All exercises complete! ---")
