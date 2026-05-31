# Day 3: Unpacking & Deobfuscation

## What is Packing?
```
Original binary:
  [.text: readable code] [.data: strings] [imports: visible]

Packed binary:
  [.packed: encrypted/compressed blob] [unpacker stub]

At runtime:
  1. Unpacker stub runs first
  2. Decrypts/decompresses the original code
  3. Fixes imports (resolves API addresses)
  4. Jumps to Original Entry Point (OEP)
```

## Common Packers
```
UPX         — open source, easy to unpack (upx -d file.exe)
Themida     — commercial, heavy protection
VMProtect   — virtualizes code into custom bytecode
ASPack      — simple compression
Custom      — malware often uses custom packers
```

## Detecting Packed Binaries
```python
import pefile
import math

def entropy(data):
    """Calculate Shannon entropy (randomness)."""
    if not data:
        return 0
    freq = [0] * 256
    for byte in data:
        freq[byte] += 1
    ent = 0
    for f in freq:
        if f > 0:
            p = f / len(data)
            ent -= p * math.log2(p)
    return ent

def check_packed(filepath):
    pe = pefile.PE(filepath)
    print(f"Sections in {filepath}:")
    for section in pe.sections:
        name = section.Name.decode().rstrip('\x00')
        ent = entropy(section.get_data())
        suspicious = "PACKED?" if ent > 7.0 else "normal"
        print(f"  {name:<10} entropy={ent:.2f} {suspicious}")
    
    # High entropy (>7.0) in code sections = likely packed/encrypted

# Other packing indicators:
# - Very few imports (just LoadLibrary + GetProcAddress)
# - Section names like .UPX, .packed, .vmp
# - Entry point not in first section
# - Large difference between virtual size and raw size
```

## Manual Unpacking Process
```
1. Run packed binary in debugger
2. Let unpacker stub execute
3. Find the OEP (Original Entry Point):
   - Set breakpoint on VirtualAlloc/VirtualProtect
   - Look for JMP to different section
   - Watch for pushad/popad pattern (UPX)
4. When at OEP: dump the process from memory
5. Fix the import table (use tools like Scylla)
6. Result: unpacked binary you can analyze normally
```

## Deobfuscation with Python
```python
def decode_stack_strings(instructions):
    """
    Detect and decode strings built on the stack:
    mov [ebp-0x10], 0x6c6c6548  ; 'lleH'
    mov [ebp-0x0c], 0x6f57206f  ; 'oW o'
    """
    import struct
    stack_data = {}
    for addr, mnemonic, op_str in instructions:
        if mnemonic == "mov" and "ebp-" in op_str and "0x" in op_str:
            # Extract offset and value
            parts = op_str.split(",")
            offset = int(parts[0].split("0x")[1].rstrip("]"), 16)
            value = int(parts[1].strip(), 16)
            stack_data[offset] = struct.pack("<I", value)
    
    # Reconstruct string from stack
    result = b""
    for offset in sorted(stack_data.keys(), reverse=True):
        result += stack_data[offset]
    return result.decode(errors="ignore").rstrip("\x00")

def deobfuscate_xor_loop(data, key_byte):
    """Decode XOR-encoded data (common in malware)."""
    return bytes([b ^ key_byte for b in data])
```

## Automation: OLE/Macro Analysis
```python
# For malicious Office documents (macros)
# pip install oletools

# olevba — extract VBA macros
# oleid — identify OLE file characteristics
# oletimes — check timestamps

# Common macro malware patterns:
# - Shell() or WScript.Shell
# - PowerShell download cradles
# - Base64/XOR encoded payloads
# - Auto_Open or Document_Open triggers
```
