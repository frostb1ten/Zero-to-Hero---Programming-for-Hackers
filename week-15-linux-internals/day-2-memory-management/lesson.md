# Day 2: Memory Management & Virtual Memory

## Virtual Memory Concepts
```
Every process gets its own virtual address space:

Process A sees:        Physical RAM:        Process B sees:
0x00000000            ┌────────────┐        0x00000000
    │                 │  Shared     │            │
    │         ┌──────►│  Libraries  │◄──────┐    │
    │         │       ├────────────┤       │    │
    ▼         │       │  Process A  │       │    ▼
0x08040000 ───┘       │  Code+Data  │       │ 0x08040000
                      ├────────────┤       │
                      │  Process B  │       │
                      │  Code+Data  ├───────┘
                      ├────────────┤
                      │  Kernel     │
                      └────────────┘

Key insight: Same virtual address in different processes
maps to DIFFERENT physical memory. This is isolation.
```

## Page Tables
- Memory divided into pages (typically 4096 bytes / 4KB)
- Page table maps virtual → physical addresses
- MMU (hardware) does translation on every memory access
- Kernel manages page tables per-process

## Memory Protections
```
Permissions per page:
  R = Readable
  W = Writable  
  X = Executable

Common combinations:
  r-x = Code (.text section) — execute but can't modify
  rw- = Data (.data, .bss, heap, stack) — read/write but can't execute
  r-- = Read-only data (.rodata)

Security mechanisms:
  NX/DEP:  Stack/heap marked non-executable → can't run shellcode there
  ASLR:    Randomize base addresses each run → can't hardcode addresses
  Stack Canary: Random value before return addr → detects overflow
  RELRO:   Read-only GOT → can't overwrite function pointers
```

## Checking Binary Protections
```bash
# checksec (from pwntools or checksec.sh)
checksec ./binary

# Output:
#   RELRO:    Full RELRO
#   Stack:    Canary found
#   NX:       NX enabled
#   PIE:      PIE enabled
#   ASLR:     Enabled (system-wide)
```

## Python: Examining Memory Layout
```python
import ctypes
import struct

# Get address of a Python object
x = 42
addr = id(x)
print(f"Object at: 0x{addr:016x}")

# mmap — allocate memory with specific permissions
import mmap
import os

# Allocate executable memory (for shellcode testing)
mem = mmap.mmap(-1, 4096, 
    prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
mem.write(b"\x90" * 100 + b"\xc3")  # NOPs + RET

# ASLR demonstration
print("Run this multiple times — addresses change each time:")
print(f"  Stack variable: 0x{id(addr):016x}")
```

## Heap Management
```
malloc(size):
  1. Check free list for suitable chunk
  2. If none: ask kernel for more memory (brk/mmap)
  3. Return pointer to usable area

free(ptr):
  1. Mark chunk as free
  2. Add to free list
  3. Maybe coalesce with adjacent free chunks

Heap vulnerabilities:
  - Use-after-free: access freed chunk → attacker controls data
  - Double-free: corrupt free list → arbitrary write
  - Heap overflow: overflow into next chunk's metadata
```
