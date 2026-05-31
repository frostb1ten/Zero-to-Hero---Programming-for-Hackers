# Day 3: Building a Static Analysis Tool

## The Core Idea
Static analysis = scanning source code for bugs WITHOUT running it.
You're building your own mini version of tools like Bandit, Semgrep, or CodeQL.

## How Static Analysis Works
1. Read source files
2. Search for dangerous patterns (regex or AST)
3. Report findings with file, line number, and severity

## Approach 1: Regex-Based Scanning
```python
import re
import os

RULES = [
    {
        "id": "CMD-001",
        "name": "os.system() usage",
        "pattern": r"os\.system\s*\(",
        "severity": "HIGH",
        "description": "Possible command injection via os.system()"
    },
    {
        "id": "SQL-001",
        "name": "SQL string formatting",
        "pattern": r'\.execute\s*\(\s*f["\']',
        "severity": "HIGH",
        "description": "Possible SQL injection via f-string in query"
    },
]

def scan_file(filepath, rules):
    findings = []
    with open(filepath, "r", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            for rule in rules:
                if re.search(rule["pattern"], line):
                    findings.append({
                        "file": filepath,
                        "line": line_num,
                        "rule": rule["id"],
                        "severity": rule["severity"],
                        "code": line.strip(),
                        "message": rule["description"]
                    })
    return findings
```

## Approach 2: AST-Based Scanning (More Accurate)
```python
import ast

class DangerFinder(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        # Check for eval() calls
        if isinstance(node.func, ast.Name) and node.func.id == "eval":
            self.findings.append({
                "line": node.lineno,
                "type": "CODE-EXEC",
                "message": "eval() called — possible code execution"
            })

        # Check for os.system() calls
        if (isinstance(node.func, ast.Attribute) and
            node.func.attr == "system" and
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == "os"):
            self.findings.append({
                "line": node.lineno,
                "type": "CMD-INJ",
                "message": "os.system() — possible command injection"
            })

        self.generic_visit(node)

# Usage
with open("target.py", "r") as f:
    tree = ast.parse(f.read())

finder = DangerFinder()
finder.visit(tree)
for f in finder.findings:
    print(f"  Line {f['line']}: [{f['type']}] {f['message']}")
```

## Why AST is Better Than Regex
- Regex matches strings in comments (false positives)
- Regex can miss multi-line statements
- AST understands the actual code structure
- AST can trace variable assignments and function calls

## Combining Both Approaches
```python
# Use regex for:
# - Hardcoded secrets (patterns in strings)
# - Configuration issues (debug=True)
# - Quick scanning of non-Python files

# Use AST for:
# - Dangerous function calls
# - Data flow analysis
# - Complex patterns
```

## Building a Rule Engine
```python
# Rules as data — easy to add more
REGEX_RULES = {
    "CRED-001": {"pattern": r'password\s*=\s*["\'][^"\']+["\']', "sev": "CRITICAL"},
    "CRED-002": {"pattern": r'api_key\s*=\s*["\'][^"\']+["\']', "sev": "CRITICAL"},
    "DEBUG-001": {"pattern": r'debug\s*=\s*True', "sev": "MEDIUM"},
    "HASH-001": {"pattern": r'md5\(', "sev": "MEDIUM"},
}
```
