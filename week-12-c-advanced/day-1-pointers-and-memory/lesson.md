# Day 1: Pointers Deep Dive & Dynamic Memory

## malloc / free — Manual Memory Management
```c
#include <stdlib.h>

// Allocate memory on the HEAP (persists until freed)
int *arr = (int *)malloc(100 * sizeof(int));  // 100 ints
if (arr == NULL) {
    perror("malloc failed");
    return 1;
}

// Use it
for (int i = 0; i < 100; i++) arr[i] = i;

// Free it — if you forget, MEMORY LEAK
free(arr);
arr = NULL;  // prevent dangling pointer

// calloc — allocates AND zeros memory
int *clean = (int *)calloc(100, sizeof(int));

// realloc — resize an allocation
arr = (int *)realloc(arr, 200 * sizeof(int));
```

## Double Pointers (pointer to pointer)
```c
void allocate_buffer(char **buf, int size) {
    *buf = (char *)malloc(size);
}

char *buffer = NULL;
allocate_buffer(&buffer, 1024);
// buffer is now allocated
free(buffer);
```

## Common Memory Bugs
```c
// 1. Buffer overflow
char buf[10];
strcpy(buf, "This string is way too long for the buffer");

// 2. Use-after-free
char *p = malloc(64);
free(p);
strcpy(p, "CRASH");  // undefined behavior

// 3. Double free
free(p);
free(p);  // heap corruption

// 4. Memory leak
char *data = malloc(1024);
// function returns without free(data)

// 5. Null dereference
int *ptr = NULL;
*ptr = 42;  // segfault
```

## Void Pointers — Generic Pointers
```c
void *generic = malloc(100);

// Cast to whatever type you need
int *int_ptr = (int *)generic;
char *str_ptr = (char *)generic;

// This is how malloc returns memory — void*
// You must cast it to the right type
```

## Function Pointers
```c
// Declare a function pointer
int (*operation)(int, int);

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

operation = add;
printf("%d\n", operation(10, 5));  // 15

operation = sub;
printf("%d\n", operation(10, 5));  // 5

// Used in: callbacks, vtables, hooking
```
