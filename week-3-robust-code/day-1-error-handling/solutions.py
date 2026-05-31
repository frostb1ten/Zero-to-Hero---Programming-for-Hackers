# =============================================================
# SOLUTIONS — Error Handling
# =============================================================

# --- Exercise 1 ---
user_input = "not_a_number"
try:
    number = int(user_input)
    print(f"Got: {number}")
except ValueError:
    print("Invalid number!")

# --- Exercise 2 ---
try:
    with open("nonexistent_file.txt", "r") as f:
        data = f.read()
    print(data)
except FileNotFoundError:
    print("File doesn't exist!")

# --- Exercise 3 ---
data = ["22", "80", "abc"]
for i in range(5):
    try:
        port = int(data[i])
        print(f"Port: {port}")
    except IndexError:
        print(f"Index {i} is out of range")
    except ValueError:
        print(f"'{data[i]}' is not a valid port number")

# --- Exercise 4 ---
def get_valid_number(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid number!")

# --- Exercise 5 ---
def validate_port(port):
    if port < 1 or port > 65535:
        raise ValueError(f"Port must be 1-65535, got {port}")
    return True

try:
    validate_port(80)
    print("Port 80: valid")
    validate_port(-1)
except ValueError as e:
    print(f"Error: {e}")

print("\n--- All exercises complete! ---")
