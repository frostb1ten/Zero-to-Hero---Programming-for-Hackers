# Day 1: Debugging with GDB & WinDbg

## Why Debuggers
- See exactly what's happening in memory during execution
- Find the crash point in a buffer overflow
- Verify your exploit overwrites the right address
- Reverse engineer binaries you don't have source for

## GDB Essentials
```bash
# Start debugging
gdb ./vulnerable_binary
gdb -q ./binary          # quiet mode (no banner)

# Run with arguments
(gdb) run AAAAAAAAAA
(gdb) run $(python3 -c "print('A'*100)")

# Set Intel syntax (easier to read)
(gdb) set disassembly-flavor intel
```

## GDB Core Commands
```
EXECUTION:
  run (r)            — start the program
  continue (c)       — resume after breakpoint
  next (n)           — step over (don't enter functions)
  step (s)           — step into function calls
  finish             — run until current function returns
  kill               — stop the program

BREAKPOINTS:
  break main         — break at function name
  break *0x08041234  — break at address
  break *main+15     — break at offset from function
  info breakpoints   — list breakpoints
  delete 1           — remove breakpoint #1

EXAMINING STATE:
  info registers     — show all registers
  print $eax         — show EAX value
  print/x $esp       — show ESP in hex

MEMORY:
  x/20x $esp         — 20 hex words at ESP
  x/s 0x08041234     — string at address
  x/10i $eip         — 10 instructions at EIP
  x/100x $esp-100    — examine stack

  Format: x/[count][format][size]
  Formats: x(hex) d(decimal) s(string) i(instruction)
  Sizes:   b(byte) h(halfword) w(word) g(giant/8byte)

STACK:
  backtrace (bt)     — show call stack
  frame 0            — select stack frame
  info frame         — detailed frame info

MODIFY:
  set $eax = 0x42    — change register
  set {int}0x... = 5 — write to memory
```

## Exploit Dev Workflow in GDB
```bash
# 1. Find the crash
(gdb) run $(python3 -c "print('A'*200)")
# Program received signal SIGSEGV
# EIP = 0x41414141 ← you control EIP!

# 2. Find exact offset with pattern
(gdb) run $(python3 -c "import sys; sys.stdout.write('Aa0Aa1Aa2...')")
# EIP = 0x63413163 ← look up in pattern

# 3. Verify control
(gdb) run $(python3 exploit.py)
# EIP = 0xdeadbeef ← exact value you set!

# 4. Find JMP ESP or useful gadget
(gdb) find /b 0x08040000, 0x08050000, 0xff, 0xe4
# 0x08041234 ← JMP ESP gadget

# 5. Set breakpoint at return, examine stack
(gdb) break *vuln_function+50
(gdb) run $(python3 exploit.py)
(gdb) x/20x $esp
```

## GDB with PEDA/GEF/pwndbg (Enhanced)
```bash
# Install pwndbg (recommended for exploit dev):
# git clone https://github.com/pwndbg/pwndbg
# cd pwndbg && ./setup.sh

# Enhanced commands:
pwndbg> checksec          # show binary protections
pwndbg> vmmap             # memory mappings
pwndbg> cyclic 200        # generate pattern
pwndbg> cyclic -l 0x6161  # find offset
pwndbg> rop               # find ROP gadgets
pwndbg> search -s "AAAA"  # search memory
```

## WinDbg Basics (Windows)
```
COMMANDS:
  g              — go (continue)
  p              — step over
  t              — step into
  bp address     — breakpoint
  bl             — list breakpoints
  r              — show registers
  dd esp         — display dwords at ESP
  da address     — display ASCII string
  db address     — display bytes
  u eip          — unassemble at EIP
  !address       — show memory layout
  lm             — list loaded modules
  .formats val   — convert value formats

EXPLOIT DEV:
  !exploitable   — analyze crash exploitability
  !heap          — heap information
  !teb           — thread environment block
  !peb           — process environment block
```
