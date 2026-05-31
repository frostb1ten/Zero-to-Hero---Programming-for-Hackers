# =============================================================
# SOLUTIONS — File I/O
# =============================================================
import os

# --- Exercise 1 ---
with open("targets.txt", "w") as f:
    f.write("10.0.0.1\n")
    f.write("10.0.0.2\n")
    f.write("10.0.0.3\n")
print("[+] Exercise 1: wrote targets.txt")

# --- Exercise 2 ---
with open("targets.txt", "r") as f:
    for line in f:
        print(f"  Target: {line.strip()}")

# --- Exercise 3 ---
with open("targets.txt", "r") as f:
    targets = [line.strip() for line in f if line.strip()]
print(f"Loaded {len(targets)} targets: {targets}")

# --- Exercise 4 ---
with open("targets.txt", "a") as f:
    f.write("10.0.0.4\n")
    f.write("10.0.0.5\n")
print("[+] Exercise 4: appended to targets.txt")

# --- Exercise 5 ---
data = [
    ("10.0.0.1", 22, "open"),
    ("10.0.0.1", 80, "closed"),
    ("10.0.0.2", 443, "open"),
]
with open("report.csv", "w") as f:
    f.write("ip,port,status\n")
    for ip, port, status in data:
        f.write(f"{ip},{port},{status}\n")
print("[+] Exercise 5: wrote report.csv")

# --- Exercise 6 ---
filename = "report.csv"
if os.path.exists(filename):
    with open(filename, "r") as f:
        print(f.read())
else:
    print(f"[!] {filename} not found")

# Cleanup
for f in ["targets.txt", "report.csv"]:
    if os.path.exists(f):
        os.remove(f)
print("[+] Cleaned up temp files")

print("\n--- All exercises complete! ---")
