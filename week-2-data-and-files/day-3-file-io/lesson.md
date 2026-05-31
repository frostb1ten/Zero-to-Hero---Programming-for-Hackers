# Day 3: File I/O

## The Core Idea
Read from files, write to files. Essential for logging, parsing configs,
saving scan results, and reading wordlists.

## Reading a File
```python
# The safe way — 'with' auto-closes the file
with open("targets.txt", "r") as f:
    content = f.read()  # entire file as one string
print(content)

# Read line by line (better for big files)
with open("targets.txt", "r") as f:
    for line in f:
        print(line.strip())  # strip() removes the newline

# Read all lines into a list
with open("targets.txt", "r") as f:
    lines = f.readlines()    # ['line1\n', 'line2\n', ...]
    lines = [l.strip() for l in lines]  # clean version
```

## Writing to a File
```python
# "w" = write (creates file or OVERWRITES existing)
with open("results.txt", "w") as f:
    f.write("Scan Results\n")
    f.write("============\n")
    f.write("Port 22: open\n")

# "a" = append (adds to end, doesn't overwrite)
with open("results.txt", "a") as f:
    f.write("Port 80: open\n")
```

## Checking if a File Exists
```python
import os

if os.path.exists("targets.txt"):
    print("File found!")
else:
    print("File not found.")

# Also useful:
os.path.isfile("targets.txt")   # True if it's a file
os.path.isdir("logs/")          # True if it's a directory
```

## Working With Paths
```python
import os

# Join paths safely (handles / vs \ across OS)
full_path = os.path.join("output", "scans", "results.txt")

# Get parts of a path
os.path.basename("/home/user/scan.txt")   # "scan.txt"
os.path.dirname("/home/user/scan.txt")    # "/home/user"
os.path.splitext("scan.txt")              # ("scan", ".txt")
```

## Real-World Pattern: Reading a Wordlist
```python
def load_wordlist(filepath):
    """Load a wordlist file, one word per line."""
    words = []
    with open(filepath, "r") as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith("#"):  # skip blanks and comments
                words.append(word)
    return words
```

## CSV Files (Quick Method)
```python
# Writing CSV
with open("ports.csv", "w") as f:
    f.write("ip,port,status\n")
    f.write("10.0.0.1,22,open\n")
    f.write("10.0.0.1,80,closed\n")

# Reading CSV (simple)
with open("ports.csv", "r") as f:
    header = f.readline()  # skip header
    for line in f:
        ip, port, status = line.strip().split(",")
        print(f"  {ip}:{port} — {status}")
```
