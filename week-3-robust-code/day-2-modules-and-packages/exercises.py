# =============================================================
# EXERCISES — Modules & Packages
# =============================================================


# --- Exercise 1: Import and use os ---
# Print the current working directory
import ___
print(f"Current dir: {___}")


# --- Exercise 2: JSON ---
# Convert this dict to a JSON string with indentation, then parse it back
import ___

data = {"ip": "10.0.0.1", "ports": [22, 80], "status": "up"}
json_string = ___
print(json_string)

parsed = ___
print(f"IP from parsed JSON: {parsed['ip']}")


# --- Exercise 3: Hashing ---
# Hash the password "secret123" with SHA-256 and print the hex digest
import ___

password = "secret123"
hashed = ___
print(f"SHA-256 of '{password}': {hashed}")


# --- Exercise 4: Base64 ---
# Encode "user:pass" to base64, then decode it back
import ___

original = "user:pass"
encoded = ___
decoded = ___
print(f"Encoded: {encoded}")
print(f"Decoded: {decoded}")


# --- Exercise 5: Generate a random string ---
# Generate a random 12-character alphanumeric string
import ___
import ___

chars = string.ascii_letters + string.digits
random_str = ___
print(f"Random: {random_str}")


# --- Exercise 6: sys.argv ---
# Print how many command-line arguments were passed
import ___
arg_count = ___
print(f"You passed {arg_count} arguments")


print("\n--- All exercises complete! ---")
