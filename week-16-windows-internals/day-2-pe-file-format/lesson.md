# Day 2: PE File Format

## PE = Portable Executable (Windows binaries: .exe, .dll, .sys)

## PE Structure
```
┌────────────────────┐
│ DOS Header         │ ← MZ magic, pointer to PE header
│ DOS Stub           │ ← "This program cannot be run in DOS mode"
├────────────────────┤
│ PE Signature       │ ← "PE\0\0"
├────────────────────┤
│ COFF Header        │ ← Machine type, number of sections, timestamp
├────────────────────┤
│ Optional Header    │ ← Entry point, image base, section alignment
│  - Data Dirs       │ ← Import table, export table, relocation, etc.
├────────────────────┤
│ Section Headers    │ ← .text, .data, .rdata, .rsrc, etc.
├────────────────────┤
│ Sections           │
│  .text             │ ← Executable code
│  .rdata            │ ← Read-only data (strings, imports)
│  .data             │ ← Writable data (globals)
│  .rsrc             │ ← Resources (icons, manifests)
│  .reloc            │ ← Relocation table (for ASLR)
└────────────────────┘
```

## Parsing PE in Python
```python
import struct

def parse_pe(path):
    with open(path, "rb") as f:
        # DOS Header
        assert f.read(2) == b"MZ"
        f.seek(0x3C)
        pe_offset = struct.unpack("<I", f.read(4))[0]

        # PE Header
        f.seek(pe_offset)
        assert f.read(4) == b"PE\x00\x00"

        # COFF Header (20 bytes)
        machine = struct.unpack("<H", f.read(2))[0]
        num_sections = struct.unpack("<H", f.read(2))[0]
        timestamp = struct.unpack("<I", f.read(4))[0]
        f.read(8)  # skip PointerToSymbolTable + NumberOfSymbols
        opt_header_size = struct.unpack("<H", f.read(2))[0]
        characteristics = struct.unpack("<H", f.read(2))[0]

        # Optional Header
        magic = struct.unpack("<H", f.read(2))[0]
        is_64 = (magic == 0x20B)  # PE32+ = 64-bit

        f.read(2)  # linker version
        f.read(12)  # sizes
        entry_rva = struct.unpack("<I", f.read(4))[0]
        f.read(8 if not is_64 else 12)
        image_base = struct.unpack("<Q" if is_64 else "<I",
                                    f.read(8 if is_64 else 4))[0]

        return {
            "machine": "x64" if machine == 0x8664 else "x86",
            "sections": num_sections,
            "entry_point": f"0x{image_base + entry_rva:x}",
            "image_base": f"0x{image_base:x}",
            "is_dll": bool(characteristics & 0x2000),
            "is_64bit": is_64
        }
```

## Import Address Table (IAT)
```
When a PE calls kernel32!CreateFileW:
1. Call goes to IAT entry (a pointer)
2. At load time, Windows fills IAT with actual addresses
3. IAT is writable at load time → IAT hooking target!

# Find imports
import pefile  # pip install pefile

pe = pefile.PE("malware.exe")
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print(f"\n{entry.dll.decode()}:")
    for imp in entry.imports:
        print(f"  {imp.name.decode() if imp.name else 'ordinal'} @ 0x{imp.address:x}")
```

## Why PE Matters for Security
- **Malware analysis**: Understand what a binary imports/does
- **Packing**: Packers compress/encrypt sections, add unpacker stub
- **Injection**: Know where to write code in another process
- **Hooking**: Know where function pointers live (IAT, EAT)
- **Shellcode**: Resolve API addresses at runtime via PEB→LDR
