# =============================================================
# WEEK 1 PROJECT: Target Info Collector
# =============================================================
# Build a CLI tool that collects scan target info from the user
# and displays a formatted summary.
#
# Requirements:
# 1. Ask for: target IP, port, protocol (http/https), scan type (quick/full)
# 2. Validate the port is between 1-65535
# 3. Build the full URL (e.g., "https://10.0.0.1:443")
# 4. Print a formatted summary box
#
# Expected output:
# ==========================================
#  [*] Target Info Collector
# ==========================================
# Enter target IP: 10.0.0.1
# Enter port: 443
# Enter protocol (http/https): https
# Enter scan type (quick/full): full
#
# ==========================================
#  [+] Scan Summary
# ==========================================
#  Target:    10.0.0.1
#  Port:      443
#  Protocol:  HTTPS
#  Scan Type: FULL
#  Full URL:  https://10.0.0.1:443
# ==========================================
#
# HINTS:
# - Use a function for the banner (you'll reuse this pattern a lot)
# - Use a function to validate the port
# - Use .strip() on inputs (users add accidental spaces)
# - Use .lower() or .upper() to normalize protocol/scan type
#
# BONUS:
# - If port is invalid, keep asking until they give a valid one (while loop!)
# - Add color-coding if you want (print("\033[92mGREEN\033[0m"))
#
# Write your code below:
# =============================================================


