# =============================================================
# SOLUTIONS — Decorators & Generators
# =============================================================
import functools
import time

# --- Exercise 1 ---
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIMER] {func.__name__}: {elapsed:.4f}s")
        return result
    return wrapper

@timer
def waste_time():
    total = sum(range(500_000))
    return total
waste_time()

# --- Exercise 2 ---
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}({args})")
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b
add(10, 20)

# --- Exercise 3 ---
def retry(attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
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

# --- Exercise 4 ---
def ip_range(base, start, end):
    for i in range(start, end + 1):
        yield f"{base}.{i}"

ips = list(ip_range("192.168.1", 1, 5))
print(f"IPs: {ips}")

# --- Exercise 5 ---
def words():
    yield "hi"
    yield "admin"
    yield "root"
    yield "me"
    yield "password"

def filter_long(gen, min_len=4):
    for word in gen:
        if len(word) >= min_len:
            yield word

def append_numbers(gen):
    for word in gen:
        yield word + "123"

pipeline = append_numbers(filter_long(words()))
print(f"Pipeline: {list(pipeline)}")

# --- Exercise 6 ---
def mutate(word):
    yield word
    yield word.capitalize()
    yield word + "123"
    yield word + "!"
    yield word.upper()

mutations = list(mutate("hack"))
print(f"Mutations: {mutations}")

print("\n--- All exercises complete! ---")
