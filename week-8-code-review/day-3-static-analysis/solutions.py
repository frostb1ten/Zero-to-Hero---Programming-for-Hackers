# =============================================================
# SOLUTIONS — Build Your Own Static Analyzer
# =============================================================
import re
import ast
import os


# --- Exercise 1 ---
RULES = [
    {"id": "CMD-001", "pattern": r"os\.system\s*\(", "severity": "HIGH",
     "msg": "os.system() usage"},
    {"id": "EXEC-001", "pattern": r"\beval\s*\(", "severity": "CRITICAL",
     "msg": "eval() usage"},
    {"id": "DESER-001", "pattern": r"yaml\.load\s*\((?!.*Loader)", "severity": "HIGH",
     "msg": "yaml.load() without SafeLoader — deserialization risk"},
]


# --- Exercise 2 ---
def scan_code(code_string, rules):
    findings = []
    for line_num, line in enumerate(code_string.split("\n"), 1):
        for rule in rules:
            if re.search(rule["pattern"], line):
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


# --- Exercise 3 ---
class VulnFinder(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec"):
                self.findings.append({
                    "line": node.lineno,
                    "type": f"{node.func.id}() call"
                })

        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "system":
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


# --- Exercise 4 ---
def scan_directory(path, rules):
    all_findings = []
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.endswith(".py"):
                filepath = os.path.join(root, fname)
                try:
                    with open(filepath, "r", errors="ignore") as f:
                        code = f.read()
                    file_findings = scan_code(code, rules)
                    for finding in file_findings:
                        finding["file"] = filepath
                    all_findings.extend(file_findings)
                except Exception as e:
                    print(f"  Error scanning {filepath}: {e}")
    return all_findings

print("\n--- All exercises complete! ---")
