# =============================================================
# EXERCISES — File I/O
# These exercises create and clean up their own temp files.
# =============================================================
import os


# --- Exercise 1: Write a file ---
# Write 3 IP addresses to a file called "targets.txt", one per line
with open("targets.txt", ___) as f:
    ___
    ___
    ___
print("[+] Exercise 1: wrote targets.txt")


# --- Exercise 2: Read a file ---
# Read targets.txt and print each line (stripped of whitespace)
with open("targets.txt", ___) as f:
    for line in f:
        print(f"  Target: {___}")


# --- Exercise 3: Read into a list ---
# Read all lines into a list called 'targets' (stripped, no blanks)
with open("targets.txt", "r") as f:
    targets = ___
print(f"Loaded {len(targets)} targets: {targets}")


# --- Exercise 4: Append to a file ---
# Add two more IPs to targets.txt WITHOUT overwriting
with open("targets.txt", ___) as f:
    f.write("10.0.0.4\n")
    f.write("10.0.0.5\n")
print("[+] Exercise 4: appended to targets.txt")


# --- Exercise 5: Write a CSV report ---
# Write this data as CSV with header: ip,port,status
data = [
    ("10.0.0.1", 22, "open"),
    ("10.0.0.1", 80, "closed"),
    ("10.0.0.2", 443, "open"),
]

with open("report.csv", "w") as f:
    ___  # write the header line
    for ip, port, status in data:
        ___  # write each row
print("[+] Exercise 5: wrote report.csv")


# --- Exercise 6: Check if file exists ---
# Only read the file if it exists, otherwise print an error
filename = "report.csv"
if ___:
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
