# Day 3: Arrays, Strings & Pointers

## This Is THE Most Important Day
Pointers are why C is powerful AND dangerous. Every buffer overflow,
every use-after-free, every kernel exploit exists because of pointers.

## Arrays
```c
int ports[5] = {22, 80, 443, 8080, 3389};
char name[32] = "scanner";

// Access
printf("%d\n", ports[0]);   // 22
printf("%d\n", ports[4]);   // 3389

// NO bounds checking — this compiles and runs, but corrupts memory:
// ports[100] = 9999;  ← buffer overflow!

// Array size
int count = sizeof(ports) / sizeof(ports[0]);  // 5
```

## Strings = char arrays + null terminator
```c
// These are equivalent:
char str1[] = "Hello";
char str2[] = {'H', 'e', 'l', 'l', 'o', '\0'};

// String functions (include <string.h>)
strlen(str1)              // 5 (doesn't count \0)
strcmp(str1, str2)         // 0 (equal)
strcpy(dest, src)          // DANGEROUS — no bounds check
strncpy(dest, src, n)      // safer — copies at most n bytes
snprintf(buf, size, fmt)   // safest — bounded formatting

// NEVER use: gets(), strcpy(), sprintf()
// ALWAYS use: fgets(), strncpy(), snprintf()
```

## Pointers — The Heart of C
```c
int x = 42;
int *ptr = &x;    // ptr holds the ADDRESS of x

printf("Value: %d\n", x);       // 42
printf("Address: %p\n", &x);    // 0x7ffd12345678
printf("Pointer: %p\n", ptr);   // 0x7ffd12345678 (same)
printf("Deref: %d\n", *ptr);    // 42 (follow the pointer)

*ptr = 100;  // change the value AT that address
printf("x = %d\n", x);  // 100 — x changed!
```

## Pointer Arithmetic
```c
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;  // points to first element

printf("%d\n", *p);       // 10
printf("%d\n", *(p+1));   // 20 (moves by sizeof(int) = 4 bytes)
printf("%d\n", *(p+2));   // 30

// arr[i] is exactly the same as *(arr + i)
```

## Arrays and Pointers Are Related
```c
int arr[5] = {1, 2, 3, 4, 5};

// These are equivalent:
arr[3]       // subscript notation
*(arr + 3)   // pointer arithmetic

// When passed to a function, arrays decay to pointers:
void process(int *data, int len) {
    for (int i = 0; i < len; i++) {
        printf("%d ", data[i]);
    }
}
process(arr, 5);
```

## Why Pointers Cause Vulnerabilities
```c
// 1. Buffer Overflow — writing past array bounds
char buf[64];
strcpy(buf, very_long_string);  // overwrites stack!

// 2. Null Pointer Dereference
int *p = NULL;
*p = 42;  // CRASH (segfault)

// 3. Use After Free
int *p = malloc(sizeof(int));
free(p);
*p = 42;  // undefined behavior — data corruption

// 4. Dangling Pointer
int *get_local() {
    int x = 42;
    return &x;  // x is destroyed when function returns!
}
```

## The Stack — Where Overflows Happen
```
When a function is called:

HIGH ADDRESS
┌──────────────────┐
│ Return Address    │ ← attacker wants to overwrite THIS
├──────────────────┤
│ Saved EBP        │
├──────────────────┤
│ Local buffer[64]  │ ← overflow starts HERE, goes UP
├──────────────────┤
│ Other locals      │
└──────────────────┘
LOW ADDRESS

If buffer is 64 bytes but you write 80 bytes:
the extra 16 bytes overwrite EBP and Return Address
```
