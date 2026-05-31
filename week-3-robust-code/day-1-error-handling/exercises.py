# =============================================================
# EXERCISES — Error Handling
# =============================================================


# --- Exercise 1: Basic try/except ---
# Wrap this in try/except to handle invalid input
user_input = "not_a_number"
___:
    number = int(user_input)
    print(f"Got: {number}")
___:
    print("Invalid number!")


# --- Exercise 2: File not found ---
# Try to open a file, handle the error if missing
___:
    with open("nonexistent_file.txt", "r") as f:
        data = f.read()
    print(data)
___:
    print("File doesn't exist!")


# --- Exercise 3: Multiple except ---
# Handle both IndexError and ValueError
data = ["22", "80", "abc"]

for i in range(5):  # intentionally goes out of range
    try:
        port = int(data[i])
        print(f"Port: {port}")
    except ___:
        print(f"Index {i} is out of range")
    except ___:
        print(f"'{data[i]}' is not a valid port number")


# --- Exercise 4: Retry loop ---
# Write a function that keeps asking until valid input is given
# (For testing, we'll simulate it instead of using real input)

def get_valid_number(prompt):
    """Keep asking until the user enters a valid integer."""
    while True:
        ___:
            value = int(input(prompt))
            return ___
        ___:
            print("Please enter a valid number!")

# Uncomment to test interactively:
# result = get_valid_number("Enter a number: ")
# print(f"You entered: {result}")


# --- Exercise 5: Raise your own error ---
# Complete the function to raise ValueError for invalid ports

def validate_port(port):
    if ___:
        raise ___
    return True

try:
    validate_port(80)
    print("Port 80: valid")
    validate_port(-1)
except ValueError as e:
    print(f"Error: {e}")


print("\n--- All exercises complete! ---")
