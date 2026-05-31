# =============================================================
# WEEK 7 PROJECT: Async Mass Scanner
# =============================================================
# Build an async scanner that scans a full /24 subnet (256 hosts)
# across multiple ports simultaneously.
#
# Requirements:
# 1. Accept a subnet base (e.g., "192.168.1") via command line
# 2. Scan all 256 hosts (.0 to .255) on common ports
# 3. Use asyncio with semaphore for rate limiting
# 4. Grab banners on open ports
# 5. Use decorators: @timer on the main scan, @retry on connections
# 6. Use generators to produce the target list
# 7. Save results as JSON
#
# Architecture:
# - Generator: yield (ip, port) tuples for all targets
# - Async scanner with semaphore (configurable concurrency)
# - @timer decorator on main scan
# - Banner grab with timeout
# - JSON report with timing data
#
# Example:
#   python project.py 192.168.1 --ports 22,80,443 --concurrent 500
#
#   [*] Scanning 192.168.1.0/24 on ports [22, 80, 443]
#   [*] 768 total probes, 500 concurrent max
#
#   192.168.1.1:22    OPEN   SSH-2.0-OpenSSH_8.9
#   192.168.1.1:80    OPEN   HTTP/1.1 200 OK
#   192.168.1.50:22   OPEN   SSH-2.0-OpenSSH_7.6
#   ...
#
#   [*] Scan complete: 12 open ports across 4 hosts in 8.3s
#
# Write your code below:
# =============================================================


