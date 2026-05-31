# Week 26: Final Capstone — Frost's Offensive Security Platform

## The Ultimate Test
Build a complete offensive security platform that proves mastery
across ALL 26 weeks. This isn't a toy — this is a real toolset
you'll use in your career.

## Platform Architecture
```
frost-toolkit/
├── core/
│   ├── __init__.py
│   ├── config.py          ← config management
│   ├── logging.py         ← unified logging
│   └── plugin_base.py     ← plugin architecture
├── recon/
│   ├── dns.py             ← DNS resolution & enumeration
│   ├── port_scanner.py    ← async port scanner
│   ├── banner_grab.py     ← service detection
│   ├── web_recon.py       ← headers, robots, links
│   └── osint.py           ← email/subdomain gathering
├── vuln/
│   ├── code_scanner.py    ← static analysis (PyAudit)
│   ├── web_vulns.py       ← SQLi/XSS/CMDi detection
│   └── fuzzer.py          ← protocol fuzzer
├── exploit/
│   ├── payload_builder.py ← overflow payloads
│   ├── rop_builder.py     ← ROP chain generator
│   ├── encoder.py         ← XOR/custom encoders
│   └── shellcode.py       ← shellcode management
├── post/
│   ├── enum.py            ← system enumeration
│   ├── privesc.py         ← privilege escalation checks
│   ├── persistence.py     ← persistence mechanisms
│   └── exfil.py           ← data exfiltration
├── passwords/
│   ├── hasher.py          ← hash/crack/identify
│   ├── wordlist.py        ← generation & mutation
│   └── brute.py           ← brute force engine
├── c2/
│   ├── server.py          ← C2 server
│   ├── agent.py           ← implant/agent
│   └── crypto.py          ← encrypted comms
├── binary/
│   ├── pe_parser.py       ← PE file analysis
│   ├── elf_parser.py      ← ELF file analysis
│   ├── disasm.py          ← disassembly (capstone)
│   └── packer_detect.py   ← packing detection
├── kernel/               (C code)
│   ├── rootkit_detector/  ← detect hidden processes/files
│   ├── syscall_monitor/   ← log syscalls
│   └── Makefile
├── main.py               ← unified CLI
├── requirements.txt
└── README.md
```

## Must-Have Features
1. **Plugin architecture** — easy to add new modules
2. **Unified CLI** with argparse subcommands
3. **Async scanning** for network operations
4. **Multiple output formats** (JSON, CSV, text, HTML)
5. **Logging** throughout with levels
6. **Error handling** — never crashes on bad input
7. **Config files** — persistent settings
8. **Documentation** — docstrings on everything

## Grading Yourself
Ask these questions:
- [ ] Can I scan a /24 subnet in under 30 seconds?
- [ ] Can I identify services on open ports?
- [ ] Can I find SQL injection in source code automatically?
- [ ] Can I build a buffer overflow payload given an offset?
- [ ] Can I generate a ROP chain?
- [ ] Can I encode shellcode to avoid bad characters?
- [ ] Can I parse a PE/ELF binary and list its imports?
- [ ] Can I detect if a binary is packed?
- [ ] Can I write a kernel module that hooks a syscall?
- [ ] Can I set up a basic C2 channel?
- [ ] Can I crack a hash given a wordlist?
- [ ] Did I write ALL of this myself?

If you check every box — you're not a beginner anymore.
You're Frost, and you build security tools.
