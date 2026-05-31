# =============================================================
# WEEK 4 PROJECT: Log Analyzer & Recon Tool
# =============================================================
# Build a tool that combines regex, requests, and subprocess.
#
# Requirements:
# 1. Parse a log file and extract:
#    - All unique IP addresses
#    - All email addresses
#    - Failed login attempts (lines with "failed" or "error")
#
# 2. For each unique IP found:
#    - Ping it to check if alive
#    - Try to do a reverse DNS lookup
#
# 3. For a user-provided URL:
#    - GET the page
#    - Check security headers
#    - Extract all links from the page (regex)
#
# 4. Save results to a JSON report file
#
# Sample log file (create this for testing):
# """
# 2026-05-30 10:00:01 INFO Connection from 192.168.1.100
# 2026-05-30 10:00:05 ERROR Failed login from 10.0.0.50 user admin
# 2026-05-30 10:00:10 INFO Email sent to user@example.com
# 2026-05-30 10:00:15 ERROR Connection refused from 203.0.113.5
# 2026-05-30 10:00:20 INFO Report sent to security@corp.org
# """
#
# HINTS:
# - Use re.findall() with the IP and email patterns from Day 1
# - Use subprocess for ping (remember cross-platform!)
# - Use requests with timeout and error handling
# - Use json.dump() with indent=2 for the report
#
# Write your code below:
# =============================================================


