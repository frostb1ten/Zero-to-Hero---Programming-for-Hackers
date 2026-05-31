# =============================================================
# EXAMPLES — File I/O
# Run this first to create sample files, then study the output.
# =============================================================
import os

# --- 1. Create a sample targets file ---
with open("targets.txt", "w") as f:
    f.write("10.0.0.1\n")
    f.write("10.0.0.2\n")
    f.write("10.0.0.3\n")
    f.write("# this is a comment\n")
    f.write("10.0.0.5\n")
print("[+] Created targets.txt")

# --- 2. Read it back ---
print("\n[*] Reading targets.txt:")
with open("targets.txt", "r") as f:
    for line in f:
        cleaned = line.strip()
        if cleaned and not cleaned.startswith("#"):
            print(f"    Target: {cleaned}")

# --- 3. Write scan results ---
results = [
    ("10.0.0.1", 22, "open"),
    ("10.0.0.1", 80, "closed"),
    ("10.0.0.2", 22, "open"),
    ("10.0.0.2", 443, "open"),
]

with open("scan_results.csv", "w") as f:
    f.write("ip,port,status\n")
    for ip, port, status in results:
        f.write(f"{ip},{port},{status}\n")
print("\n[+] Wrote scan_results.csv")

# --- 4. Read the CSV back ---
print("\n[*] Scan Results:")
with open("scan_results.csv", "r") as f:
    header = f.readline().strip()
    print(f"    {header}")
    print(f"    {'-' * len(header)}")
    for line in f:
        ip, port, status = line.strip().split(",")
        symbol = "+" if status == "open" else "-"
        print(f"    [{symbol}] {ip}:{port}")

# --- 5. Append to a log ---
with open("scan.log", "w") as f:
    f.write("[2026-05-30 10:00] Scan started\n")

with open("scan.log", "a") as f:
    f.write("[2026-05-30 10:01] Found 3 hosts\n")
    f.write("[2026-05-30 10:02] Scan complete\n")

print("\n[*] Log file:")
with open("scan.log", "r") as f:
    print(f.read())

# --- 6. Check file existence ---
for name in ["targets.txt", "missing.txt", "scan_results.csv"]:
    exists = "EXISTS" if os.path.exists(name) else "NOT FOUND"
    print(f"    {name}: {exists}")

# Cleanup
for f in ["targets.txt", "scan_results.csv", "scan.log"]:
    os.remove(f)
print("\n[+] Cleaned up temp files")
