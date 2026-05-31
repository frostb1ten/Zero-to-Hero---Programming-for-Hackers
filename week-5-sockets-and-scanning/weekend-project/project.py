# =============================================================
# WEEK 5 PROJECT: Full Port Scanner Tool
# =============================================================
# Build a complete, command-line port scanner like a mini-nmap.
#
# Usage:
#   python project.py <target> [--ports 1-1024] [--threads 100]
#
# Features:
# 1. Accept target IP/hostname via command line (sys.argv)
# 2. Scan a range of ports using ThreadPoolExecutor
# 3. Grab banners on open ports
# 4. Identify services by port number
# 5. Show timing info (how long the scan took)
# 6. Save results to JSON
#
# Expected output:
# ==========================================
#  PortScanner v1.0
# ==========================================
# [*] Target: scanme.nmap.org (45.33.32.156)
# [*] Scanning ports 1-1024...
#
# [+]  22/tcp   OPEN   SSH          SSH-2.0-OpenSSH_6.6.1p1
# [+]  80/tcp   OPEN   HTTP         HTTP/1.1 200 OK
#
# [*] Scan complete: 2 open ports found in 15.3s
# [+] Results saved to scan_results.json
#
# ARCHITECTURE HINTS:
# - Create a Scanner class with scan() and grab_banner() methods
# - Use sys.argv or argparse for command-line arguments
# - Use ThreadPoolExecutor for concurrent scanning
# - Use a service dictionary for port→name mapping
# - Wrap network calls in try/except
#
# BONUS:
# - Add a --verbose flag for extra output
# - Add UDP scanning
# - Support comma-separated ports: --ports 22,80,443
# - Add OS detection based on TTL
#
# Write your code below:
# =============================================================


