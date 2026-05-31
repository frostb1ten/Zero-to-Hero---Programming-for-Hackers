# Day 2: Control Flow & Functions in C

## if/else
```c
int port = 22;

if (port == 22) {
    printf("SSH\n");
} else if (port == 80) {
    printf("HTTP\n");
} else {
    printf("Unknown: %d\n", port);
}
```

## switch (faster than if/else chains)
```c
switch (port) {
    case 21: printf("FTP\n"); break;
    case 22: printf("SSH\n"); break;
    case 80: printf("HTTP\n"); break;
    default: printf("Unknown\n"); break;
}
```

## Loops
```c
// for loop
for (int i = 0; i < 10; i++) {
    printf("%d ", i);
}

// while loop
int attempts = 0;
while (attempts < 3) {
    printf("Attempt %d\n", attempts);
    attempts++;
}

// do-while (runs at least once)
do {
    // try connection
} while (retry);
```

## Functions
```c
// Declaration (prototype)
int add(int a, int b);
void print_banner(const char *name);
int is_valid_port(int port);

// Definition
int add(int a, int b) {
    return a + b;
}

void print_banner(const char *name) {
    printf("========== %s ==========\n", name);
}

int is_valid_port(int port) {
    return (port >= 1 && port <= 65535);
}
```

## Passing by Value vs Pointer
```c
// By value (copy — changes don't affect original)
void try_modify(int x) {
    x = 999;  // only changes local copy
}

// By pointer (changes the original)
void actually_modify(int *x) {
    *x = 999;  // changes the original value
}

int main() {
    int val = 42;
    try_modify(val);
    printf("%d\n", val);  // still 42

    actually_modify(&val);
    printf("%d\n", val);  // now 999
}
```

## Header Files
```c
// scanner.h — declarations
#ifndef SCANNER_H
#define SCANNER_H

int scan_port(const char *ip, int port);
void print_results(int *ports, int count);

#endif

// scanner.c — implementations
#include "scanner.h"
#include <stdio.h>

int scan_port(const char *ip, int port) {
    // implementation
    return 0;
}
```

## Key Differences from Python
- Must declare variable types
- Use `{}` braces instead of indentation
- End statements with `;`
- Arrays have fixed size at compile time
- No garbage collector — YOU manage memory
- Functions must be declared before use (or use prototypes)
