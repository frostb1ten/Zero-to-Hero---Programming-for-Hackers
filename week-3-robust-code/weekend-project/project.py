# =============================================================
# WEEK 3 PROJECT: Password Strength Analyzer
# =============================================================
# Build a tool that analyzes passwords and generates secure ones.
#
# Requirements:
# 1. Create a PasswordAnalyzer class with:
#    - check(password) → returns a dict with score and issues list
#    - Checks: length (8+), uppercase, lowercase, digit, special char
#    - Score: 0-5 based on how many checks pass
#    - Rating: "Weak" (0-2), "Medium" (3-4), "Strong" (5)
#
# 2. Create a PasswordGenerator class with:
#    - generate(length=16) → returns a random secure password
#    - Always includes upper, lower, digit, special
#
# 3. Main program:
#    - Menu: [1] Check a password  [2] Generate  [3] Check from file  [4] Quit
#    - Option 3: read passwords from a file, analyze each, save report
#
# Example:
# ==========================================
#  Password Strength Analyzer
# ==========================================
# [1] Check a password
# [2] Generate a password
# [3] Check from file
# [4] Quit
#
# Choice: 1
# Enter password: admin123
#
# [*] Analysis for: admin123
#     Score: 2/5 — Weak
#     Issues:
#       - No uppercase letter
#       - No special character
#       - Too short (min 8, got 8... barely)
#     Hash: 0192023a7bbd73250516f069df18b500
#
# HINTS:
# - Use the string module for character sets
# - Use hashlib to show the MD5 hash
# - Use error handling for file operations
# - The classes should be reusable (no input() inside them)
#
# Write your code below:
# =============================================================


