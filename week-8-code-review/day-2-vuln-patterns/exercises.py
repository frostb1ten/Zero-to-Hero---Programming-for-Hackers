# =============================================================
# EXERCISES — Vulnerability Patterns
# For each snippet, identify the vuln and write a safe version.
# =============================================================
import os
import subprocess


# --- Exercise 1: Fix the command injection ---
# VULNERABLE VERSION:
def traceroute_vuln(target):
    os.system(f"tracert {target}")

# YOUR SAFE VERSION:
def traceroute_safe(target):
    ___


# --- Exercise 2: Fix the SQL injection ---
# VULNERABLE VERSION:
def find_user_vuln(conn, email):
    query = "SELECT * FROM users WHERE email = '" + email + "'"
    return conn.execute(query).fetchone()

# YOUR SAFE VERSION:
def find_user_safe(conn, email):
    ___


# --- Exercise 3: Fix the path traversal ---
# VULNERABLE VERSION:
def serve_file_vuln(filename):
    return open(f"/var/www/static/{filename}").read()

# YOUR SAFE VERSION:
def serve_file_safe(filename):
    base_dir = "/var/www/static"
    ___


# --- Exercise 4: Fix the eval ---
# VULNERABLE VERSION:
def calculator_vuln(expression):
    return eval(expression)

# YOUR SAFE VERSION (hint: use ast.literal_eval or manual parsing):
def calculator_safe(expression):
    ___


# --- Exercise 5: Fix the deserialization ---
# VULNERABLE VERSION:
import pickle

def load_data_vuln(raw_bytes):
    return pickle.loads(raw_bytes)

# YOUR SAFE VERSION:
import json

def load_data_safe(raw_string):
    ___


# --- Exercise 6: Spot ALL the bugs ---
# This function has MULTIPLE vulnerabilities. List them all.

def process_request(user_data):
    """Process incoming request data."""
    import sqlite3
    import pickle

    # Load user preferences
    prefs = pickle.loads(user_data["preferences"])

    # Look up user
    conn = sqlite3.connect("app.db")
    user = conn.execute(
        f"SELECT * FROM users WHERE id = {user_data['user_id']}"
    ).fetchone()

    # Run their requested command
    os.system(user_data["command"])

    # Read their profile picture
    pic = open(f"/uploads/{user_data['avatar']}").read()

    return {"user": user, "prefs": prefs}

# ANSWER — List ALL vulnerabilities:
# 1. ___
# 2. ___
# 3. ___
# 4. ___


print("Fix each function, then check solutions.py")
