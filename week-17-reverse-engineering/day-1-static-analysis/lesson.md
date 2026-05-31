# Day 1: Static Analysis — Reading Disassembly

## Tools
- **Ghidra** (free, NSA) — decompiler + disassembler
- **IDA Pro** (paid) — industry standard
- **Binary Ninja** — modern alternative
- **radare2/Cutter** (free) — CLI + GUI
- **objdump** — quick command-line disassembly

## Static vs Dynamic Analysis
```
Static:  Examine binary WITHOUT running it
  - Disassembly, decompilation
  - String analysis, imports
  - Control flow graphs
  - Safe (malware can't execute)

Dynamic: Run the binary and observe behavior
  - Debugging (GDB, x64dbg)
  - API monitoring
  - Network capture
  - Memory inspection
  - Risk: malware actually runs!
```

## First Steps With Any Binary
```bash
# 1. What type of file?
file binary

# 2. Strings — often reveals a LOT
strings binary | grep -i "password\|http\|flag\|key"

# 3. Shared libraries needed
ldd binary              # Linux
dumpbin /dependents x.exe  # Windows

# 4. Symbols (function names)
nm binary               # Linux
objdump -t binary

# 5. Quick disassembly
objdump -d -M intel binary | less
```

## Reading Disassembly Patterns
```nasm
; Function that checks a password:
; if (strcmp(input, "s3cr3t") == 0) { grant_access(); }

check_password:
    push ebp
    mov ebp, esp
    sub esp, 0x10

    ; Load arguments
    mov eax, [ebp+8]         ; first arg = user input

    ; Call strcmp
    push 0x08048abc          ; address of "s3cr3t" string
    push eax                 ; user input
    call strcmp
    add esp, 8               ; clean up args

    ; Check result
    test eax, eax            ; is result 0?
    jne .fail                ; if not equal, jump to fail

    ; Success path
    call grant_access
    jmp .end

.fail:
    call deny_access

.end:
    leave
    ret

; KEY INSIGHT: The string "s3cr3t" is visible in the binary!
; This is why strings analysis works on simple programs.
```

## Common Patterns to Recognize
```
Pattern: Loop
    xor ecx, ecx        ; counter = 0
.loop:
    cmp ecx, 10         ; while (counter < 10)
    jge .done
    ; ... body ...
    inc ecx              ; counter++
    jmp .loop
.done:

Pattern: Function call with args (cdecl)
    push arg3
    push arg2
    push arg1
    call function
    add esp, 12          ; clean 3 args × 4 bytes

Pattern: Switch/jump table
    cmp eax, 5           ; if (x > 5) goto default
    ja .default
    jmp [jump_table + eax*4]  ; indexed jump
```

## Python-Assisted RE
```python
# Use capstone to disassemble specific sections
from capstone import *

def disassemble_function(binary_path, offset, size):
    with open(binary_path, "rb") as f:
        f.seek(offset)
        code = f.read(size)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for insn in md.disasm(code, offset):
        print(f"0x{insn.address:08x}: {insn.mnemonic:<8} {insn.op_str}")
```
