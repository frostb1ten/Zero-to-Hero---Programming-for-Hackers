# =============================================================
# SOLUTIONS — Password & Hash Tools
# =============================================================
import hashlib

# --- Exercise 1 ---
password = "password123"
md5_hash = hashlib.md5(password.encode()).hexdigest()
sha256_hash = hashlib.sha256(password.encode()).hexdigest()
print(f"MD5:    {md5_hash}")
print(f"SHA256: {sha256_hash}")

# --- Exercise 2 ---
def identify_hash(hash_string):
    length = len(hash_string)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA-1"
    elif length == 64:
        return "SHA-256"
    elif length == 128:
        return "SHA-512"
    else:
        return f"Unknown ({length} chars)"

print(identify_hash("5f4dcc3b5aa765d61d8327deb882cf99"))
print(identify_hash("5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"))

# --- Exercise 3 ---
target = "5f4dcc3b5aa765d61d8327deb882cf99"
wordlist = ["123456", "password", "admin", "letmein", "qwerty"]
cracked = None
for word in wordlist:
    if hashlib.md5(word.encode()).hexdigest() == target:
        cracked = word
        break
print(f"Cracked: {cracked}")

# --- Exercise 4 ---
words = ["admin", "root", "test", "guest"]
hash_table = {}
for word in words:
    h = hashlib.md5(word.encode()).hexdigest()
    hash_table[h] = word

test_hash = hashlib.md5("root".encode()).hexdigest()
print(f"Reverse lookup: {hash_table.get(test_hash, 'Not found')}")

# --- Exercise 5 ---
def mutate(word):
    mutations = []
    mutations.append(word)
    mutations.append(word.capitalize())
    mutations.append(word + "123")
    mutations.append(word + "!")
    mutations.append(word.upper())
    return mutations

muts = mutate("test")
print(f"Mutations: {muts}")

print("\n--- All exercises complete! ---")
