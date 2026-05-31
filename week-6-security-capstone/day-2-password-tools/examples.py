# =============================================================
# EXAMPLES — Password & Hash Tools
# =============================================================
import hashlib
import os
import time


# --- 1. Hashing demo ---
print("[1] Hash types:")
password = "admin123"
hashes = {
    "MD5":    hashlib.md5(password.encode()).hexdigest(),
    "SHA-1":  hashlib.sha1(password.encode()).hexdigest(),
    "SHA-256": hashlib.sha256(password.encode()).hexdigest(),
}
for name, h in hashes.items():
    print(f"    {name:<8}: {h}")
print()


# --- 2. Hash identifier ---
print("[2] Hash identification:")

def identify_hash(h):
    length = len(h)
    types = {32: "MD5", 40: "SHA-1", 64: "SHA-256", 128: "SHA-512"}
    return types.get(length, f"Unknown ({length} chars)")

test_hashes = [
    "0192023a7bbd73250516f069df18b500",
    "f865b53623b121fd34ee5426c792e5c33af8c227",
    "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
]
for h in test_hashes:
    print(f"    {h[:20]}... → {identify_hash(h)}")
print()


# --- 3. Dictionary attack (small wordlist) ---
print("[3] Dictionary attack demo:")
target_hash = hashlib.md5("letmein".encode()).hexdigest()
print(f"    Target MD5: {target_hash}")

wordlist = ["password", "123456", "admin", "letmein", "welcome", "monkey"]
start = time.time()

found = None
for word in wordlist:
    if hashlib.md5(word.encode()).hexdigest() == target_hash:
        found = word
        break

elapsed = time.time() - start
if found:
    print(f"    CRACKED: '{found}' in {elapsed:.4f}s")
else:
    print(f"    Not found in {elapsed:.4f}s")
print()


# --- 4. Password mutations ---
print("[4] Password mutations:")

def mutate(word):
    mutations = set()
    mutations.add(word)
    mutations.add(word.capitalize())
    mutations.add(word.upper())
    mutations.add(word + "123")
    mutations.add(word + "!")
    mutations.add(word + "1")
    mutations.add(word.replace("a", "@"))
    mutations.add(word.replace("e", "3"))
    mutations.add(word.replace("o", "0"))
    return sorted(mutations)

base = "password"
muts = mutate(base)
print(f"    Base: '{base}' → {len(muts)} mutations:")
for m in muts:
    print(f"      {m}")
print()


# --- 5. File hashing ---
print("[5] File hashing:")
test_file = "test_hash_file.txt"
with open(test_file, "w") as f:
    f.write("This is a test file for hashing")

def hash_file(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

for algo in ["md5", "sha1", "sha256"]:
    print(f"    {algo.upper()}: {hash_file(test_file, algo)}")

os.remove(test_file)
print()


# --- 6. Salted hashing ---
print("[6] Salted hash:")
salt = os.urandom(16).hex()
pw = "secure_password"
salted = hashlib.sha256(f"{salt}{pw}".encode()).hexdigest()
print(f"    Salt: {salt}")
print(f"    Hash: {salted}")
# Verify
check = hashlib.sha256(f"{salt}{pw}".encode()).hexdigest()
print(f"    Verify match: {check == salted}")
