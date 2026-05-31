# =============================================================
# WEEK 2 PROJECT: Network Inventory Manager
# =============================================================
# Build a CLI tool that manages a list of network hosts.
#
# Features:
# 1. Add a host (IP, hostname, OS, open ports)
# 2. List all hosts in a formatted table
# 3. Search for a host by IP
# 4. Save inventory to a CSV file
# 5. Load inventory from a CSV file
#
# Data structure — a list of dictionaries:
# inventory = [
#     {"ip": "10.0.0.1", "hostname": "web01", "os": "Linux", "ports": "22,80,443"},
#     {"ip": "10.0.0.2", "hostname": "db01", "os": "Linux", "ports": "3306"},
# ]
#
# Example session:
# ==========================================
#  Network Inventory Manager
# ==========================================
# [1] Add host
# [2] List hosts
# [3] Search by IP
# [4] Save to file
# [5] Load from file
# [6] Quit
#
# Choice: 1
# IP: 10.0.0.1
# Hostname: web01
# OS: Linux
# Open ports (comma-separated): 22,80,443
# [+] Host added!
#
# HINTS:
# - Use a while True loop for the main menu
# - Use a list of dicts for the inventory
# - CSV: "ip,hostname,os,ports" as header
# - Use functions for each menu option
#
# Write your code below:
# =============================================================


