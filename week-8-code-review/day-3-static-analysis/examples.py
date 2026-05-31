# =============================================================
# EXAMPLES — Static Analysis Tool
# =============================================================
import re
import ast
import os
import json


# --- The rules engine ---
RULES = [
    {"id": "CMD-001", "pattern": r"os\.system\s*\(", "severity": "HIGH",
     "msg": "os.system() — command injection risk"},
    {"id": "CMD-002", "pattern": r"subprocess.*shell\s*=\s*True", "severity": "HIGH",
     "msg": "subprocess with shell=True — command injection risk"},
    {"id": "SQL-001", "pattern": r'\.execute\s*\(\s*f["\']', "severity": "HIGH",
     "msg": "SQL f-string — SQL injection risk"},
    {"id": "SQL-002", "pattern": r'\.execute\s*\(.*\+', "severity": "HIGH",
     "msg": "SQL concatenation — SQL injection risk"},
    {"id": "EXEC-001", "pattern": r'\beval\s*\(', "severity": "CRITICAL",
     "msg": "eval() — code execution risk"},
    {"id": "EXEC-002", "pattern": r'\bexec\s*\(', "severity": "CRITICAL",
     "msg": "exec() — code execution risk"},
    {"id": "DESER-001", "pattern": r'pickle\.loads?\s*\(', "severity": "CRITICAL",
     "msg": "pickle deserialization — RCE risk"},
    {"id": "CRED-001", "pattern": r'password\s*=\s*["\'][^"\']{3,}["\']', "severity": "CRITICAL",
     "msg": "Hardcoded password"},
    {"id": "CRED-002", "pattern": r'(?:api_key|secret|token)\s*=\s*["\'][^"\']{3,}["\']',
     "severity": "CRITICAL", "msg": "Hardcoded secret/key"},
    {"id": "HASH-001", "pattern": r'hashlib\.md5\s*\(', "severity": "MEDIUM",
     "msg": "MD5 used — weak hash algorithm"},
    {"id": "DEBUG-001", "pattern": r'debug\s*=\s*True', "severity": "MEDIUM",
     "msg": "Debug mode enabled"},
]


def scan_string(code, rules):
    """Scan a code string with regex rules."""
    findings = []
    for line_num, line in enumerate(code.split("\n"), 1):
        for rule in rules:
            if re.search(rule["pattern"], line, re.IGNORECASE):
                findings.append({
                    "line": line_num,
                    "rule": rule["id"],
                    "severity": rule["severity"],
                    "message": rule["msg"],
                    "code": line.strip()
                })
    return findings


# --- Test code with vulnerabilities ---
SAMPLE_CODE = '''
import os
import sqlite3
import pickle
import hashlib

API_KEY = "sk-live-1234567890abcdef"
password = "admin123"
debug = True

def run_cmd(user_input):
    os.system(f"echo {user_input}")

def find_user(name):
    conn = sqlite3.connect("db.sqlite")
    return conn.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchone()

def calc(expr):
    return eval(expr)

def load_prefs(data):
    return pickle.loads(data)

def hash_pw(pw):
    return hashlib.md5(pw.encode()).hexdigest()
'''


# --- 1. Run the regex scanner ---
print("[1] Regex-based scan results:")
print("=" * 60)
findings = scan_string(SAMPLE_CODE, RULES)

for f in findings:
    color = {"CRITICAL": "!!", "HIGH": "! ", "MEDIUM": "* "}
    sev = color.get(f["severity"], "  ")
    print(f"  [{sev}] Line {f['line']:>3} | {f['severity']:<8} | {f['rule']}")
    print(f"       {f['message']}")
    print(f"       Code: {f['code']}")
    print()

print(f"Total: {len(findings)} findings")
print()


# --- 2. AST-based scanner ---
print("[2] AST-based scan:")
print("=" * 60)

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        # eval()
        if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
            self.findings.append({
                "line": node.lineno,
                "type": f"{node.func.id}() call",
                "severity": "CRITICAL"
            })

        # os.system()
        if (isinstance(node.func, ast.Attribute) and
            node.func.attr == "system"):
            self.findings.append({
                "line": node.lineno,
                "type": "os.system() call",
                "severity": "HIGH"
            })

        # pickle.loads()
        if (isinstance(node.func, ast.Attribute) and
            node.func.attr in ("loads", "load") and
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == "pickle"):
            self.findings.append({
                "line": node.lineno,
                "type": "pickle deserialization",
                "severity": "CRITICAL"
            })

        self.generic_visit(node)

tree = ast.parse(SAMPLE_CODE)
visitor = SecurityVisitor()
visitor.visit(tree)

for f in visitor.findings:
    print(f"  Line {f['line']:>3} | {f['severity']:<8} | {f['type']}")

print(f"\nAST found {len(visitor.findings)} issues")
