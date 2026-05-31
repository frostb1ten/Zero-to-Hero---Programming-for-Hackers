# Day 1: C Programming Basics

## Why C for Security
- Kernel, drivers, and OS are written in C
- Most exploits target C programs (buffer overflows, format strings)
- You can't do kernel dev without C — period
- Understanding C makes you understand memory, which makes you understand exploits

## Setup
```bash
# Windows: Install MinGW or use WSL
# Linux: gcc comes preinstalled usually
gcc --version

# Compile and run:
gcc hello.c -o hello
./hello
```

## Hello World
```c
#include <stdio.h>    // standard I/O library

int main() {
    printf("Hello, World!\n");
    return 0;  // 0 = success
}
```

## Variables & Types
```c
#include <stdio.h>

int main() {
    // Integer types
    char c = 'A';            // 1 byte  (-128 to 127)
    short s = 1000;          // 2 bytes
    int i = 42;              // 4 bytes
    long l = 100000L;        // 4-8 bytes
    long long ll = 999999LL; // 8 bytes

    // Unsigned (no negatives, double the positive range)
    unsigned char uc = 255;
    unsigned int ui = 4294967295U;

    // Floating point
    float f = 3.14f;         // 4 bytes
    double d = 3.14159;      // 8 bytes

    // Size matters — this is why exploits work
    printf("char:  %zu bytes\n", sizeof(char));
    printf("int:   %zu bytes\n", sizeof(int));
    printf("long:  %zu bytes\n", sizeof(long));
    printf("ptr:   %zu bytes\n", sizeof(void*));  // 4 on 32-bit, 8 on 64-bit

    return 0;
}
```

## Format Strings (printf)
```c
printf("%d\n", 42);          // integer
printf("%x\n", 255);         // hex: ff
printf("%08x\n", 255);       // hex padded: 000000ff
printf("%s\n", "hello");     // string
printf("%c\n", 'A');         // character
printf("%p\n", &variable);   // pointer address
printf("%zu\n", sizeof(int));// size_t

// FORMAT STRING VULNERABILITY — never do this:
// printf(user_input);  ← attacker controls format = RCE
// Always: printf("%s", user_input);
```

## Input
```c
char name[64];
int age;

printf("Name: ");
fgets(name, sizeof(name), stdin);  // SAFE — bounded

printf("Age: ");
scanf("%d", &age);  // & = "address of"

// NEVER use gets() — no bounds checking = buffer overflow
// gets(name);  ← ALWAYS vulnerable
```

## Python ↔ C Comparison
```
Python              C
─────────           ─────────
x = 42              int x = 42;
name = "Frost"      char name[] = "Frost";
print(x)            printf("%d", x);
if x > 0:           if (x > 0) {
    print("yes")        printf("yes");
                    }
for i in range(10): for (int i = 0; i < 10; i++) {
    print(i)            printf("%d\n", i);
                    }
```
