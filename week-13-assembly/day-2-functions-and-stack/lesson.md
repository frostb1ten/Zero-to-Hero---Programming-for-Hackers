# Day 2: Functions, Calling Conventions & The Stack

## How Function Calls Work at the Assembly Level
```nasm
; C code: result = add(5, 3);

; Assembly:
push 3              ; push second argument
push 5              ; push first argument
call add            ; push return address, jump to add
add esp, 8          ; clean up arguments (caller cleanup - cdecl)
mov [result], eax   ; store return value

; Inside add():
add:
    push ebp            ; save old base pointer
    mov ebp, esp        ; set up stack frame
    mov eax, [ebp+8]    ; first arg (5)
    add eax, [ebp+12]   ; add second arg (3)
    pop ebp             ; restore base pointer
    ret                 ; return (pop EIP from stack)
```

## Stack Frame Layout
```
High addresses
┌─────────────────────┐
│ arg2 (3)            │ [ebp + 12]
├─────────────────────┤
│ arg1 (5)            │ [ebp + 8]
├─────────────────────┤
│ Return Address      │ [ebp + 4]  ← CALL pushed this
├─────────────────────┤
│ Saved EBP           │ [ebp]      ← push ebp
├─────────────────────┤
│ Local var 1         │ [ebp - 4]
├─────────────────────┤
│ Local buffer[64]    │ [ebp - 68]
├─────────────────────┤
│ ...                 │ ← ESP points here
└─────────────────────┘
Low addresses
```

## Calling Conventions
```
cdecl (C default, 32-bit):
  - Args pushed right to left onto stack
  - CALLER cleans up stack
  - Return value in EAX

stdcall (Windows API, 32-bit):
  - Args pushed right to left
  - CALLEE cleans up stack (ret N)
  - Return value in EAX

System V AMD64 (Linux 64-bit):
  - First 6 integer args: RDI, RSI, RDX, RCX, R8, R9
  - Remaining on stack
  - Return in RAX

Microsoft x64 (Windows 64-bit):
  - First 4 args: RCX, RDX, R8, R9
  - Return in RAX
  - 32 bytes shadow space on stack
```

## Function Prologue & Epilogue
```nasm
; Prologue (every function starts with this):
push ebp           ; save caller's base pointer
mov ebp, esp       ; new base pointer = current stack pointer
sub esp, N         ; allocate N bytes for local variables

; Epilogue (every function ends with this):
mov esp, ebp       ; deallocate locals
pop ebp            ; restore caller's base pointer
ret                ; pop return address into EIP

; "leave" instruction = mov esp, ebp + pop ebp
```

## Why This Matters for Exploits
```
When you overflow a local buffer:

1. You write past the buffer → hits saved EBP
2. Keep writing → hits the RETURN ADDRESS
3. When the function returns:
   - ret pops YOUR value into EIP
   - CPU starts executing at YOUR address
   - You've hijacked execution

This is literally how every classic buffer overflow works.
```

## Linux Syscalls (32-bit)
```nasm
; Syscall numbers go in EAX
; Arguments in EBX, ECX, EDX, ESI, EDI, EBP
; Trigger with: int 0x80

; exit(0):
mov eax, 1          ; syscall: exit
mov ebx, 0          ; status: 0
int 0x80

; write(1, "Hello\n", 6):
mov eax, 4          ; syscall: write
mov ebx, 1          ; fd: stdout
mov ecx, msg        ; buffer
mov edx, 6          ; length
int 0x80

; execve("/bin/sh", NULL, NULL):
mov eax, 11         ; syscall: execve
mov ebx, addr_binsh ; path
mov ecx, 0          ; argv
mov edx, 0          ; envp
int 0x80
```
