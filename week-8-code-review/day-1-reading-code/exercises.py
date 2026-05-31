# =============================================================
# EXERCISES — Reading Code for Vulnerabilities
# For each function, identify:
# 1. The vulnerability type
# 2. How an attacker would exploit it
# 3. How to fix it
#
# Write your answers in the comments marked ANSWER:
# =============================================================


# --- Exercise 1 ---
import os

def ping_host(ip):
    os.system(f"ping -n 1 {ip}")

# ANSWER — Vulnerability type: ___
# ANSWER — Exploit input: ___
# ANSWER — Fix: ___


# --- Exercise 2 ---
def admin_panel(user_input):
    if user_input == "show config":
        print("Config: ...")
    elif user_input == "calc":
        expr = input("Expression: ")
        print(eval(expr))

# ANSWER — Vulnerability type: ___
# ANSWER — Exploit input: ___
# ANSWER — Fix: ___


# --- Exercise 3 ---
def download_report(report_name):
    path = "/var/reports/" + report_name
    with open(path, "r") as f:
        return f.read()

# ANSWER — Vulnerability type: ___
# ANSWER — Exploit input: ___
# ANSWER — Fix: ___


# --- Exercise 4 ---
import pickle

def load_session(session_data):
    """Load a user's session from stored bytes."""
    return pickle.loads(session_data)

# ANSWER — Vulnerability type: ___
# ANSWER — Why is this dangerous: ___
# ANSWER — Fix: ___


# --- Exercise 5 ---
def search_users(name):
    import sqlite3
    conn = sqlite3.connect("app.db")
    results = conn.execute(
        "SELECT * FROM users WHERE name LIKE '%" + name + "%'"
    ).fetchall()
    return results

# ANSWER — Vulnerability type: ___
# ANSWER — Exploit input: ___
# ANSWER — Fix: ___


# --- Exercise 6: Fix this function ---
# Rewrite this function to be SAFE

def unsafe_run(user_command):
    """Let users run whitelisted commands."""
    os.system(user_command)

def safe_run(user_command):
    """Your safe version here."""
    # WRITE YOUR FIX:
    ___


print("Review each function, identify the vuln, and write fixes.")
print("Check solutions.py when done.")
