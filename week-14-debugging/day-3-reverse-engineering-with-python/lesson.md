# Day 3: Reverse Engineering with Python

## Python as a RE Tool
Python is the glue language for reverse engineering:
- Parse binary file formats (PE, ELF)
- Automate disassembly analysis
- Write scripts for IDA Pro, Ghidra, Binary Ninja
- Build custom deobfuscators and unpackers

## Parsing ELF Headers
```python
import struct

def parse_elf(filepath):
    with open(filepath, "rb") as f:
        # ELF magic: 7f 45 4c 46
        magic = f.read(4)
        assert magic == b"\x7fELF", "Not an ELF file"

        ei_class = struct.unpack("B", f.read(1))[0]  # 1=32bit, 2=64bit
        ei_data = struct.unpack("B", f.read(1))[0]   # 1=LE, 2=BE
        ei_version = struct.unpack("B", f.read(1))[0]
        ei_osabi = struct.unpack("B", f.read(1))[0]

        f.seek(16)  # skip padding
        e_type = struct.unpack("<H", f.read(2))[0]
        e_machine = struct.unpack("<H", f.read(2))[0]
        e_version = struct.unpack("<I", f.read(4))[0]
        e_entry = struct.unpack("<Q" if ei_class == 2 else "<I",
                                f.read(8 if ei_class == 2 else 4))[0]

        return {
            "bits": 64 if ei_class == 2 else 32,
            "endian": "little" if ei_data == 1 else "big",
            "type": {1: "relocatable", 2: "executable", 3: "shared", 4: "core"}.get(e_type),
            "entry_point": f"0x{e_entry:x}"
        }
```

## Parsing PE Headers (Windows Executables)
```python
import struct

def parse_pe(filepath):
    with open(filepath, "rb") as f:
        # DOS header
        mz = f.read(2)
        assert mz == b"MZ", "Not a PE file"

        f.seek(0x3C)  # e_lfanew offset
        pe_offset = struct.unpack("<I", f.read(4))[0]

        # PE signature
        f.seek(pe_offset)
        sig = f.read(4)
        assert sig == b"PE\x00\x00"

        # COFF header
        machine = struct.unpack("<H", f.read(2))[0]
        num_sections = struct.unpack("<H", f.read(2))[0]
        timestamp = struct.unpack("<I", f.read(4))[0]

        return {
            "machine": "x64" if machine == 0x8664 else "x86",
            "sections": num_sections,
            "timestamp": timestamp
        }
```

## Capstone — Disassembly Engine
```python
# pip install capstone
from capstone import *

# x86 32-bit disassembly
code = b"\x55\x89\xe5\x83\xec\x10\xb8\x00\x00\x00\x00\xc9\xc3"
md = Cs(CS_ARCH_X86, CS_MODE_32)

for insn in md.disasm(code, 0x1000):
    print(f"  0x{insn.address:x}: {insn.mnemonic}\t{insn.op_str}")

# Output:
#   0x1000: push    ebp
#   0x1001: mov     ebp, esp
#   0x1003: sub     esp, 0x10
#   0x1006: mov     eax, 0
#   0x100b: leave
#   0x100c: ret
```

## Keystone — Assembler Engine
```python
# pip install keystone-engine
from keystone import *

ks = Ks(KS_ARCH_X86, KS_MODE_32)
code = "push ebp; mov ebp, esp; xor eax, eax; ret"
encoding, count = ks.asm(code)
shellcode = bytes(encoding)
print(f"Assembled: {shellcode.hex()}")
```

## Automating Analysis
```python
# Pattern: Find all function prologues in a binary
import re

def find_functions(binary_data):
    """Find common x86 function prologues."""
    # push ebp; mov ebp, esp = 55 89 e5
    pattern = b"\x55\x89\xe5"
    offsets = []
    start = 0
    while True:
        idx = binary_data.find(pattern, start)
        if idx == -1:
            break
        offsets.append(idx)
        start = idx + 1
    return offsets

with open("target.bin", "rb") as f:
    data = f.read()

funcs = find_functions(data)
print(f"Found {len(funcs)} potential functions")
```

## Deobfuscation Script Example
```python
def deobfuscate_xor_strings(binary_data, key):
    """Find and decode XOR-encoded strings in a binary."""
    results = []
    # Look for sequences of printable XOR'd bytes
    for offset in range(len(binary_data) - 4):
        decoded = bytes([b ^ key for b in binary_data[offset:offset+50]])
        # Check if result looks like a readable string
        try:
            text = decoded.split(b"\x00")[0].decode("ascii")
            if len(text) > 4 and text.isprintable():
                results.append((offset, text))
        except:
            pass
    return results
```
