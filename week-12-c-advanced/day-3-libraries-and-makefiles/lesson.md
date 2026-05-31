# Day 3: Libraries, Makefiles & Build Systems

## Static vs Shared Libraries
```bash
# Static library (.a) — compiled INTO your binary
gcc -c scanner.c -o scanner.o
ar rcs libscanner.a scanner.o
gcc main.c -L. -lscanner -o tool

# Shared library (.so / .dll) — loaded at runtime
gcc -shared -fPIC -o libscanner.so scanner.c
gcc main.c -L. -lscanner -o tool
# Must set LD_LIBRARY_PATH or install the .so
```

## Makefile Basics
```makefile
CC = gcc
CFLAGS = -Wall -Wextra -g
LDFLAGS =

TARGET = scanner
SRCS = main.c scanner.c utils.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
```

## Compilation Flags That Matter
```bash
gcc -Wall -Wextra          # all warnings (find bugs early)
gcc -g                      # debug symbols (for GDB)
gcc -O2                     # optimize (production)
gcc -fno-stack-protector    # disable stack canaries (for exploit testing)
gcc -z execstack            # make stack executable (for shellcode testing)
gcc -no-pie                 # disable ASLR for binary (testing)
gcc -m32                    # compile as 32-bit
```

## Project Structure
```
project/
├── Makefile
├── include/
│   ├── scanner.h
│   └── utils.h
├── src/
│   ├── main.c
│   ├── scanner.c
│   └── utils.c
└── bin/
    └── (compiled binary)
```
