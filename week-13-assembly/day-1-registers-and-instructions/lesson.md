# Day 1: x86/x64 Registers & Instructions

## Why Assembly
- Shellcode is written in assembly
- Reverse engineering requires reading disassembly
- Exploit dev requires understanding instruction-level execution
- Kernel code drops to assembly for critical sections

## x86 (32-bit) Registers
```
General Purpose:
  EAX — accumulator (return values, math)
  EBX — base (general purpose)
  ECX — counter (loops)
  EDX — data (I/O, multiplication)

  ESI — source index (string operations)
  EDI — destination index (string operations)

Stack:
  ESP — stack pointer (top of stack)
  EBP — base pointer (bottom of current stack frame)

  EIP — instruction pointer (NEXT instruction to execute)
        ↑ THIS is what you overwrite in a buffer overflow

Flags:
  EFLAGS — status bits (zero, carry, overflow, sign)
```

## x64 (64-bit) Registers
```
RAX, RBX, RCX, RDX     (64-bit versions)
RSI, RDI, RSP, RBP
RIP                      (64-bit instruction pointer)
R8-R15                   (extra registers)

Lower portions still accessible:
RAX → EAX (lower 32) → AX (lower 16) → AH:AL (high:low 8-bit)
```

## Basic Instructions
```nasm
; Data movement
mov eax, 42        ; eax = 42
mov ebx, eax       ; ebx = eax (copy)
mov [addr], eax    ; store eax at memory address
mov eax, [addr]    ; load from memory into eax

; Arithmetic
add eax, 10        ; eax += 10
sub eax, 5         ; eax -= 5
inc eax            ; eax++
dec eax            ; eax--
mul ebx            ; eax *= ebx (result in EDX:EAX)
xor eax, eax       ; eax = 0 (fastest way to zero)

; Stack
push eax           ; push eax onto stack (ESP -= 4)
pop eax            ; pop top of stack into eax (ESP += 4)

; Comparison & jumps
cmp eax, ebx       ; compare (sets flags)
jmp label          ; unconditional jump
je label           ; jump if equal (ZF=1)
jne label          ; jump if not equal
jg label           ; jump if greater
jl label           ; jump if less

; Function calls
call function      ; push return address, jump to function
ret                ; pop return address, jump to it
                   ; ↑ THIS is what executes after overflow

; System calls (Linux)
int 0x80           ; 32-bit syscall interrupt
syscall            ; 64-bit syscall instruction

; NOP
nop                ; no operation (0x90) — used in NOP sleds
```

## Reading Disassembly
```
(gdb) disassemble main

0x08041000 <+0>:   push   ebp           ; save old base pointer
0x08041001 <+1>:   mov    ebp,esp       ; set up new frame
0x08041003 <+3>:   sub    esp,0x40      ; allocate 64 bytes for locals
0x08041006 <+6>:   lea    eax,[ebp-0x40] ; load address of buffer
0x08041009 <+9>:   push   eax           ; push buffer as arg
0x0804100a <+10>:  call   0x8041050     ; call gets()  ← VULNERABLE
0x0804100f <+15>:  leave                ; restore frame
0x08041010 <+16>:  ret                  ; return ← WE CONTROL THIS
```

## NASM Syntax (Intel) vs AT&T Syntax
```
Intel (NASM):        AT&T (GAS/GDB default):
mov eax, 42          movl $42, %eax
mov [ebp-4], eax     movl %eax, -4(%ebp)
add eax, ebx         addl %ebx, %eax

; Intel: destination FIRST    (mov dst, src)
; AT&T:  destination LAST     (mov src, dst)
; Use: set disassembly-flavor intel   (in GDB)
```
