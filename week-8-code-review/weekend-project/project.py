# =============================================================
# WEEK 8 PROJECT: PyAudit — Python Security Scanner
# =============================================================
# Build a complete static analysis tool that scans Python codebases
# for security vulnerabilities.
#
# Features:
# 1. Regex scanner with 10+ rules (cmd inj, SQLi, XSS, creds, etc.)
# 2. AST scanner for dangerous function calls
# 3. Scan individual files or entire directories
# 4. Output findings sorted by severity
# 5. Save report as JSON and formatted text
# 6. CLI interface with argparse
#
# Usage:
#   python project.py scan /path/to/project
#   python project.py scan app.py --format json --output report.json
#   python project.py scan . --severity HIGH,CRITICAL
#
# Example output:
#   =============================================
#    PyAudit v1.0 — Python Security Scanner
#   =============================================
#   [*] Scanning /path/to/project (42 .py files)
#
#   CRITICAL  app/auth.py:15     CRED-001   Hardcoded password
#             password = "admin123"
#
#   HIGH      app/views.py:42    CMD-001    os.system() with user input
#             os.system(f"ping {request.args['host']}")
#
#   HIGH      app/db.py:28       SQL-001    SQL injection via f-string
#             cursor.execute(f"SELECT * FROM users WHERE id = {uid}")
#
#   MEDIUM    app/utils.py:10    HASH-001   Weak hash (MD5)
#             hashlib.md5(data.encode())
#
#   [*] Scan complete: 4 findings (2 CRITICAL, 1 HIGH, 1 MEDIUM)
#
# Write your code below:
# =============================================================


