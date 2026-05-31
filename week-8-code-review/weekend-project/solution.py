#!/usr/bin/env python3
"""PyAudit v1.0 — Python Security Scanner"""
import argparse
import ast
import json
import os
import re
import sys
from datetime import datetime


# ===================== RULES =====================
REGEX_RULES = [
    {"id": "CMD-001", "severity": "HIGH",
     "pattern": r"os\.system\s*\(", "msg": "os.system() — command injection risk"},
    {"id": "CMD-002", "severity": "HIGH",
     "pattern": r"subprocess.*shell\s*=\s*True", "msg": "subprocess shell=True — command injection risk"},
    {"id": "CMD-003", "severity": "HIGH",
     "pattern": r"os\.popen\s*\(", "msg": "os.popen() — command injection risk"},
    {"id": "SQL-001", "severity": "HIGH",
     "pattern": r'\.execute\s*\(\s*f["\']', "msg": "SQL f-string — injection risk"},
    {"id": "SQL-002", "severity": "HIGH",
     "pattern": r'\.execute\s*\([^)]*\+', "msg": "SQL concatenation — injection risk"},
    {"id": "EXEC-001", "severity": "CRITICAL",
     "pattern": r'\beval\s*\(', "msg": "eval() — code execution risk"},
    {"id": "EXEC-002", "severity": "CRITICAL",
     "pattern": r'\bexec\s*\(', "msg": "exec() — code execution risk"},
    {"id": "DESER-001", "severity": "CRITICAL",
     "pattern": r'pickle\.loads?\s*\(', "msg": "pickle deserialization — RCE risk"},
    {"id": "DESER-002", "severity": "HIGH",
     "pattern": r'yaml\.load\s*\((?!.*Loader)', "msg": "yaml.load() without SafeLoader"},
    {"id": "CRED-001", "severity": "CRITICAL",
     "pattern": r'password\s*=\s*["\'][^"\']{4,}["\']', "msg": "Hardcoded password"},
    {"id": "CRED-002", "severity": "CRITICAL",
     "pattern": r'(?:api_key|secret|token)\s*=\s*["\'][^"\']{4,}["\']', "msg": "Hardcoded secret"},
    {"id": "HASH-001", "severity": "MEDIUM",
     "pattern": r'hashlib\.md5\s*\(', "msg": "MD5 — weak hash algorithm"},
    {"id": "HASH-002", "severity": "MEDIUM",
     "pattern": r'hashlib\.sha1\s*\(', "msg": "SHA-1 — weak hash algorithm"},
    {"id": "DEBUG-001", "severity": "MEDIUM",
     "pattern": r'debug\s*=\s*True', "msg": "Debug mode enabled"},
    {"id": "RAND-001", "severity": "MEDIUM",
     "pattern": r'\brandom\.(?:randint|choice|random)\s*\(', "msg": "Non-cryptographic random for possible security use"},
]

SEV_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}


# ===================== SCANNERS =====================
def regex_scan(code, filepath, rules):
    findings = []
    for line_num, line in enumerate(code.split("\n"), 1):
        # Skip comments
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for rule in rules:
            if re.search(rule["pattern"], line, re.IGNORECASE):
                findings.append({
                    "file": filepath,
                    "line": line_num,
                    "rule": rule["id"],
                    "severity": rule["severity"],
                    "message": rule["msg"],
                    "code": stripped
                })
    return findings


class ASTScanner(ast.NodeVisitor):
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []

    def visit_Call(self, node):
        # eval(), exec()
        if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
            self.findings.append({
                "file": self.filepath,
                "line": node.lineno,
                "rule": f"AST-EXEC",
                "severity": "CRITICAL",
                "message": f"{node.func.id}() call detected (AST)",
                "code": ""
            })

        # os.system(), os.popen()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ("system", "popen"):
                self.findings.append({
                    "file": self.filepath,
                    "line": node.lineno,
                    "rule": "AST-CMD",
                    "severity": "HIGH",
                    "message": f"os.{node.func.attr}() call detected (AST)",
                    "code": ""
                })

        self.generic_visit(node)


def ast_scan(code, filepath):
    try:
        tree = ast.parse(code)
        scanner = ASTScanner(filepath)
        scanner.visit(tree)
        return scanner.findings
    except SyntaxError:
        return []


# ===================== MAIN SCANNER =====================
def scan_file(filepath, rules):
    try:
        with open(filepath, "r", errors="ignore") as f:
            code = f.read()
    except Exception:
        return []

    findings = regex_scan(code, filepath, rules)
    findings.extend(ast_scan(code, filepath))

    # Deduplicate (same file+line+severity)
    seen = set()
    unique = []
    for f in findings:
        key = (f["file"], f["line"], f["rule"])
        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique


def scan_path(path, rules, severity_filter=None):
    all_findings = []
    file_count = 0

    if os.path.isfile(path):
        files = [path]
    else:
        files = []
        for root, dirs, filenames in os.walk(path):
            # Skip hidden dirs and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for fname in filenames:
                if fname.endswith(".py"):
                    files.append(os.path.join(root, fname))

    file_count = len(files)
    for filepath in files:
        all_findings.extend(scan_file(filepath, rules))

    # Filter by severity
    if severity_filter:
        all_findings = [f for f in all_findings if f["severity"] in severity_filter]

    # Sort by severity then file
    all_findings.sort(key=lambda f: (SEV_ORDER.get(f["severity"], 99), f["file"], f["line"]))

    return all_findings, file_count


def print_findings(findings, file_count):
    print("=" * 50)
    print("  PyAudit v1.0 — Python Security Scanner")
    print("=" * 50)
    print(f"[*] Scanned {file_count} .py files\n")

    if not findings:
        print("[+] No issues found!")
        return

    for f in findings:
        sev_colors = {"CRITICAL": "!!", "HIGH": "! ", "MEDIUM": "* ", "LOW": "  "}
        marker = sev_colors.get(f["severity"], "  ")

        print(f"  [{marker}] {f['severity']:<8}  {f['file']}:{f['line']:<4}  {f['rule']}")
        print(f"           {f['message']}")
        if f["code"]:
            print(f"           > {f['code'][:80]}")
        print()

    # Summary
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items(), key=lambda x: SEV_ORDER.get(x[0], 99)))
    print(f"[*] Total: {len(findings)} findings ({summary})")


def main():
    parser = argparse.ArgumentParser(description="PyAudit — Python Security Scanner")
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument("-s", "--severity", default=None,
                        help="Filter by severity (e.g., HIGH,CRITICAL)")
    parser.add_argument("-o", "--output", help="Save JSON report to file")
    parser.add_argument("-f", "--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    sev_filter = args.severity.split(",") if args.severity else None
    findings, file_count = scan_path(args.path, REGEX_RULES, sev_filter)

    if args.format == "json" or args.output:
        report = {
            "tool": "PyAudit v1.0",
            "timestamp": datetime.now().isoformat(),
            "target": args.path,
            "files_scanned": file_count,
            "total_findings": len(findings),
            "findings": findings
        }
        if args.output:
            with open(args.output, "w") as f:
                json.dump(report, f, indent=2)
            print(f"[+] Report saved to {args.output}")
        else:
            print(json.dumps(report, indent=2))
    else:
        print_findings(findings, file_count)


if __name__ == "__main__":
    main()
