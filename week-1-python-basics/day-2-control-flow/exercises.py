# =============================================================
# EXERCISES — Control Flow
# Fill in the blanks (___) to make each section work.
# =============================================================


# --- Exercise 1: if/elif/else ---
# Check the port and print the right service name
port = 80

if ___:
    print("FTP")
elif ___:
    print("SSH")
elif ___:
    print("HTTP")
else:
    print("Unknown service")
# Expected: HTTP


# --- Exercise 2: Combining conditions ---
# Print "CRITICAL" if port is 22 AND the connection is remote
port = 22
is_remote = True

if ___ and ___:
    print("CRITICAL: Remote SSH access!")
else:
    print("OK")
# Expected: CRITICAL: Remote SSH access!


# --- Exercise 3: 'in' keyword ---
# Check if the protocol is in the allowed list
protocol = "ssh"
allowed = ["http", "https", "ssh"]

if ___:
    print(f"{protocol} is allowed")
else:
    print(f"{protocol} is blocked")
# Expected: ssh is allowed


# --- Exercise 4: for loop ---
# Loop through the IPs and print "Scanning <ip>..." for each one
targets = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

for ___:
    print(f"Scanning {ip}...")
# Expected: 3 lines of output


# --- Exercise 5: range() ---
# Print port numbers from 8080 to 8085 (inclusive!)
for port in ___:
    print(f"Checking port {port}")
# Expected: 8080, 8081, 8082, 8083, 8084, 8085


# --- Exercise 6: while loop ---
# Count from 1 to 5, printing each number
count = 1

while ___:
    print(f"Count: {count}")
    ___
# Expected: Count: 1 through Count: 5


# --- Exercise 7: break ---
# Search through ports. When you find 443, print "Found HTTPS!" and stop
ports = [22, 80, 443, 8080, 3306]

for port in ports:
    if ___:
        print("Found HTTPS!")
        ___
    print(f"Checked port {port}")
# Expected: Checked 22, Checked 80, then Found HTTPS! (no 8080 or 3306)


print("\n--- All exercises complete! ---")
