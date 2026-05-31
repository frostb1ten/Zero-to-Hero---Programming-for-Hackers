# Day 3: System Calls & Tracing

## System Calls — The Kernel Interface
Every interaction with the OS goes through syscalls:
- open(), read(), write(), close() — files
- socket(), connect(), send(), recv() — network
- fork(), execve(), exit() — processes
- mmap(), mprotect(), brk() — memory

## strace — Trace System Calls
```bash
# See every syscall a program makes
strace ./binary

# Useful flags
strace -f ./binary           # follow child processes
strace -e open ./binary      # only show open() calls
strace -e network ./binary   # only network syscalls
strace -p 1234               # attach to running PID
strace -o output.log ./binary # save to file
strace -c ./binary           # summary statistics

# Example output:
# open("/etc/passwd", O_RDONLY) = 3
# read(3, "root:x:0:0:...", 4096) = 1024
# connect(4, {sa_family=AF_INET, sin_port=htons(443)...}) = 0
```

## ltrace — Trace Library Calls
```bash
# See calls to shared libraries (libc, etc.)
ltrace ./binary
ltrace -e strcmp ./binary     # only strcmp calls

# Output:
# strcmp("user_input", "s3cr3t") = -1  ← password leak!
# malloc(128) = 0x55a123456789
# strcpy(0x55a123456789, "AAAA...") ← overflow!
```

## Writing Syscalls in Python (Linux)
```python
import ctypes
import os

# Direct syscall via libc
libc = ctypes.CDLL("libc.so.6")

# write(fd, buf, count)
message = b"Direct syscall!\n"
libc.write(1, message, len(message))  # fd 1 = stdout

# getpid via syscall
libc.syscall.restype = ctypes.c_long
pid = libc.syscall(39)  # syscall 39 = getpid (x86_64)
print(f"PID via syscall: {pid}")
print(f"PID via os: {os.getpid()}")
```

## Building a Simple Tracer (ptrace)
```python
import ctypes
import os
import signal

PTRACE_TRACEME = 0
PTRACE_PEEKTEXT = 1
PTRACE_POKETEXT = 4
PTRACE_CONT = 7
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS = 12
PTRACE_ATTACH = 16
PTRACE_DETACH = 17

libc = ctypes.CDLL("libc.so.6")

def trace_program(binary_path):
    """Fork and trace a child process."""
    pid = os.fork()
    
    if pid == 0:
        # Child: request to be traced, then exec
        libc.ptrace(PTRACE_TRACEME, 0, 0, 0)
        os.execv(binary_path, [binary_path])
    else:
        # Parent: trace the child
        os.waitpid(pid, 0)  # wait for child to stop
        
        # Read memory at entry point
        word = libc.ptrace(PTRACE_PEEKTEXT, pid, entry_addr, 0)
        print(f"Instruction at entry: 0x{word & 0xFFFFFFFF:08x}")
        
        # Single step
        libc.ptrace(PTRACE_SINGLESTEP, pid, 0, 0)
        os.waitpid(pid, 0)
        
        # Detach
        libc.ptrace(PTRACE_DETACH, pid, 0, 0)
```

## seccomp — Syscall Filtering
```python
# Sandboxes restrict which syscalls a process can make
# Used by: Chrome, Docker, systemd
# If your shellcode uses a blocked syscall → it fails

# Check what's allowed:
# strace shows EPERM or process gets killed by SIGSYS
```
