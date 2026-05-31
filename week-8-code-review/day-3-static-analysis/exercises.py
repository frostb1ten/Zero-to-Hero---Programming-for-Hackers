# =============================================================
# EXERCISES — Build Your Own Static Analyzer
# =============================================================
import re
import ast


# --- Exercise 1: Add a new regex rule ---
# Add a rule that detects yaml.load() without SafeLoader
# (yaml.load without Loader= is a deserialization vuln)

RULES = [
    {"id": "CMD-001", "pattern": r"os\.system\s*\(", "severity": "HIGH",
     "msg": "os.system() usage"},
    {"id": "EXEC-001", "pattern": r"\beval\s*\(", "severity": "CRITICAL",
     "msg": "eval() usage"},
    # ADD YOUR RULE HERE:
    ___,
]


# --- Exercise 2: Write the scanner function ---
# Scan code line-by-line and return findings

def scan_code(code_string, rules):
    findings = []
    for line_num, line in enumerate(code_string.split("\n"), 1):
        for rule in rules:
            if ___:
                findings.append({
                    "line": line_num,
                    "rule": rule["id"],
                    "severity": rule["severity"],
                    "message": rule["msg"],
                    "code": line.strip()
                })
    return findings

test_code = """
import os
import yaml
os.system("whoami")
data = yaml.load(raw_input)
result = eval(user_input)
"""

results = scan_code(test_code, RULES)
for r in results:
    print(f"  Line {r['line']}: [{r['severity']}] {r['message']}")


# --- Exercise 3: AST visitor ---
# Complete the visitor to detect eval(), exec(), and os.system()

class VulnFinder(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        # Detect eval() and exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in ___:
                self.findings.append({
                    "line": node.lineno,
                    "type": f"{node.func.id}() call"
                })

        # Detect os.system()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == ___:
                self.findings.append({
                    "line": node.lineno,
                    "type": "os.system() call"
                })

        self.generic_visit(node)


code = """
import os
eval("1+1")
os.system("ls")
exec("print('hi')")
"""

tree = ast.parse(code)
finder = VulnFinder()
finder.visit(tree)
print("\nAST findings:")
for f in finder.findings:
    print(f"  Line {f['line']}: {f['type']}")


# --- Exercise 4: Scan a directory ---
# Write a function that scans all .py files in a directory

def scan_directory(path, rules):
    all_findings = []
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.endswith(".py"):
                filepath = os.path.join(root, fname)
                ___  # read file, scan it, add to all_findings
    return all_findings

import os
# Uncomment to test on your own code:
# results = scan_directory(".", RULES)
# print(f"Found {len(results)} issues")


print("\n--- All exercises complete! ---")
