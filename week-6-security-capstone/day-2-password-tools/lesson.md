# Day 2: Password & Hash Tools

## The Core Idea
Understand hashing, build hash identifiers, create wordlist tools.
These are core skills for password auditing.

## Common Hash Types
```python
import hashlib

password = "admin123"

# MD5 (32 hex chars) — fast, weak, still common
md5 = hashlib.md5(password.encode()).hexdigest()

# SHA-1 (40 hex chars) — deprecated but still around
sha1 = hashlib.sha1(password.encode()).hexdigest()

# SHA-256 (64 hex chars) — current standard
sha256 = hashlib.sha256(password.encode()).hexdigest()

# SHA-512 (128 hex chars)
sha512 = hashlib.sha512(password.encode()).hexdigest()
```

## Identifying Hash Types by Length
```python
def identify_hash(hash_str):
    length = len(hash_str)
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
```

## Dictionary Attack Pattern
```python
import hashlib

def crack_md5(target_hash, wordlist_path):
    """Try every word in the wordlist against the hash."""
    with open(wordlist_path, "r", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if hashlib.md5(word.encode()).hexdigest() == target_hash:
                return word
    return None

# Usage
target = "0192023a7bbd73250516f069df18b500"  # MD5 of "admin123"
result = crack_md5(target, "wordlist.txt")
```

## Generating Wordlists
```python
import itertools
import string

# All 4-character lowercase combos
for combo in itertools.product(string.ascii_lowercase, repeat=4):
    word = ''.join(combo)
    # aaaa, aaab, aaac, ...

# Common mutations
def mutate(word):
    mutations = [
        word,
        word.capitalize(),
        word.upper(),
        word + "123",
        word + "!",
        word + "1",
        word.replace("a", "@"),
        word.replace("e", "3"),
        word.replace("o", "0"),
    ]
    return mutations
```

## Salted Hashes
```python
import hashlib
import os

# Creating a salted hash (how passwords SHOULD be stored)
salt = os.urandom(16).hex()
password = "mypassword"
salted = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

# To verify: you need the same salt
test = "mypassword"
check = hashlib.sha256(f"{salt}{test}".encode()).hexdigest()
print(f"Match: {check == salted}")
```

## File Hashing (Integrity Checking)
```python
import hashlib

def hash_file(filepath, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
```
