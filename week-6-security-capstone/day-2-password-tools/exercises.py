# =============================================================
# EXERCISES — Password & Hash Tools
# =============================================================
import hashlib


# --- Exercise 1: Hash a password ---
# Hash "password123" with MD5 and SHA-256
password = "password123"
md5_hash = ___
sha256_hash = ___
print(f"MD5:    {md5_hash}")
print(f"SHA256: {sha256_hash}")


# --- Exercise 2: Hash identifier ---
# Write a function that identifies hash type by length
def identify_hash(hash_string):
    length = len(hash_string)
    ___

print(identify_hash("5f4dcc3b5aa765d61d8327deb882cf99"))   # MD5
print(identify_hash("5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"))  # SHA-1


# --- Exercise 3: Mini dictionary attack ---
# The hash below is MD5 of a common password. Crack it!
target = "5f4dcc3b5aa765d61d8327deb882cf99"
wordlist = ["123456", "password", "admin", "letmein", "qwerty"]

cracked = None
for word in wordlist:
    if ___:
        cracked = word
        break

print(f"Cracked: {cracked}")
# Expected: Cracked: password


# --- Exercise 4: Generate hash wordlist ---
# Take a list of words and create a dict mapping hash → word
words = ["admin", "root", "test", "guest"]
hash_table = {}
for word in words:
    h = ___
    hash_table[h] = word

# Now do a reverse lookup
test_hash = hashlib.md5("root".encode()).hexdigest()
print(f"Reverse lookup: {hash_table.get(test_hash, 'Not found')}")
# Expected: root


# --- Exercise 5: Password mutator ---
# Write a function that generates mutations of a base word
def mutate(word):
    mutations = []
    ___  # add original
    ___  # add capitalized
    ___  # add word + "123"
    ___  # add word + "!"
    ___  # add uppercase
    return mutations

muts = mutate("test")
print(f"Mutations: {muts}")
# Expected: ['test', 'Test', 'test123', 'test!', 'TEST']


print("\n--- All exercises complete! ---")
