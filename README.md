# Frost's Offensive Security Dev Path

**26 weeks. Python → C → Assembly → Kernel. Zero to writing exploits.**

An AI built curriculum for learning to code with one goal: offensive security mastery. Not a tutorial collection — a single progressive path where every day builds on the last and every project is a stepping stone toward the final capstone.

---

## What This Is

A structured 26-week program that takes you from writing your first variable to writing kernel modules. Every example is security-themed. Every exercise builds a tool. Every project is something you'd actually use.

```
Phase 1 │ Python Foundations      │ Weeks 1-3   │ Write code from memory
Phase 2 │ Network & Automation    │ Weeks 4-6   │ Build real tools
Phase 3 │ Offensive Python        │ Weeks 7-10  │ Exploits, C2, code review
Phase 4 │ Systems Programming     │ Weeks 11-14 │ C, Assembly, debugging
Phase 5 │ OS Internals            │ Weeks 15-18 │ Linux/Windows, RE, binary exploitation
Phase 6 │ Kernel Development      │ Weeks 19-22 │ Modules, drivers, rootkits, fuzzing
Phase 7 │ Mastery                 │ Weeks 23-26 │ Malware analysis, vuln research, capstone
```

---

## Structure

```
learn-python/
├── START_HERE.md                         ← Read this first
├── CURRICULUM.md                         ← Full 26-week roadmap
├── PROGRESS.md                           ← Track completion
│
├── week-1-python-basics/
│   ├── day-1-variables-and-types/
│   │   ├── lesson.md                     ← Concept (read first)
│   │   ├── examples.py                   ← Working code to study
│   │   ├── exercises.py                  ← Fill in the ___ blanks
│   │   └── solutions.py                  ← Check your work
│   ├── day-2-control-flow/
│   ├── day-3-functions/
│   └── weekend-project/
│       ├── project.py                    ← Build spec (no hand-holding)
│       └── solution.py                   ← Reference implementation
│
├── week-2-data-and-files/
│   ...
└── week-26-final-capstone/
```

---

## What You Build (26 Projects)

| # | Project | Skills |
|---|---------|--------|
| 1 | Target Info Collector | Variables, input, f-strings |
| 2 | Network Inventory Manager | Dicts, lists, file I/O, menus |
| 3 | Password Strength Analyzer | OOP, hashlib, error handling |
| 4 | Log Analyzer & Recon Tool | Regex, requests, subprocess |
| 5 | Full Port Scanner | Sockets, threading, banners |
| 6 | Recon Automation Toolkit | Async, JSON reports, CLI |
| 7 | Async Subnet Scanner | asyncio, decorators, generators |
| 8 | PyAudit Security Scanner | AST parsing, static analysis |
| 9 | Exploit Dev Framework | struct, binary, payload building |
| 10 | Red Team Toolkit | C2, evasion, persistence |
| 11 | C Port Scanner | C sockets, compilation |
| 12 | C Network Tool | Pointers, dynamic memory |
| 13 | Custom Shellcode | x86 assembly, NASM |
| 14 | Debugger Helper | GDB scripting, ctypes |
| 15 | Process Monitor | /proc, ptrace, syscalls |
| 16 | PE Parser | Binary formats, struct parsing |
| 17 | CrackMe Solver | Reverse engineering |
| 18 | Advanced Exploit | ROP chains, ASLR bypass |
| 19 | Kernel Module | Linux LKM, /proc interface |
| 20 | Filter Driver | Device drivers |
| 21 | Rootkit Detector | Syscall hooking detection |
| 22 | Fuzzer | Coverage-guided bug finding |
| 23 | Malware Report | Full behavioral analysis |
| 24 | Security Framework | Plugin architecture |
| 25 | CVE PoC | Vulnerability research |
| 26 | **Frost's Offensive Platform** | **Everything combined** |

---

## How To Use

```bash
# Start here
cd week-1-python-basics/day-1-variables-and-types/

# 1. Read the lesson
cat lesson.md

# 2. Run examples — predict output before looking
python examples.py

# 3. Fill in the blanks
python exercises.py    # fix each ___ until it runs clean

# 4. Only then check solutions
cat solutions.py
```

### Rules
1. **Type everything yourself.** Copy-paste teaches nothing.
2. **Predict before you run.** If you're wrong, figure out why.
3. **15 minutes stuck → check solution.** Not before.
4. **Weekend projects have no hints.** You figure it out.
5. **If you can't write it from memory, you haven't learned it.**

---

## Requirements

```bash
python --version   # 3.10+
pip install requests beautifulsoup4

# Later weeks:
pip install pefile capstone keystone-engine pwntools
# Plus: gcc, nasm, gdb (for C/ASM weeks)
```

---

## End Goals

By week 26 you will:

- [x] Write Python/C/ASM without references
- [x] Build your own pentesting tools from scratch
- [x] Read code and find vulnerabilities (code review)
- [x] Write buffer overflow exploits (ROP, heap, kernel)
- [x] Understand malware at the binary level
- [x] Write Linux kernel modules and drivers
- [x] Reverse engineer binaries
- [x] Conduct original vulnerability research

---

