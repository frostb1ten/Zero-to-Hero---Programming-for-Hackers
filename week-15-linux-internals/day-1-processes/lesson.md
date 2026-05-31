# Day 1: Linux Process Management

## Process Basics
- Every running program is a process
- Identified by PID (Process ID)
- Created via fork() → child is a copy of parent
- Programs loaded via execve() → replaces process image

## /proc Filesystem — Kernel's Window
```bash
/proc/[pid]/maps      # memory mappings (find ASLR base)
/proc/[pid]/status    # process state, UID, memory info
/proc/[pid]/cmdline   # how the process was started
/proc/[pid]/fd/       # open file descriptors
/proc/[pid]/exe       # symlink to the binary
/proc/[pid]/environ   # environment variables
/proc/self/           # current process
```

## Python Process Manipulation
```python
import os
import signal

# Process info
print(f"PID: {os.getpid()}")
print(f"Parent: {os.getppid()}")
print(f"UID: {os.getuid()}")

# Fork (create child process)
pid = os.fork()
if pid == 0:
    print("I'm the child!")
    os._exit(0)
else:
    print(f"Child PID: {pid}")
    os.waitpid(pid, 0)

# Replace process image
os.execve("/bin/sh", ["/bin/sh"], os.environ)

# Signals
os.kill(target_pid, signal.SIGTERM)
os.kill(target_pid, signal.SIGKILL)  # cannot be caught
```

## Memory Maps (for exploit dev)
```python
def get_memory_maps(pid):
    """Parse /proc/pid/maps for memory layout."""
    maps = []
    with open(f"/proc/{pid}/maps", "r") as f:
        for line in f:
            parts = line.split()
            addr_range = parts[0].split("-")
            maps.append({
                "start": int(addr_range[0], 16),
                "end": int(addr_range[1], 16),
                "perms": parts[1],      # rwxp
                "path": parts[-1] if len(parts) > 5 else ""
            })
    return maps

# Find executable regions (where shellcode can run)
for m in get_memory_maps(os.getpid()):
    if 'x' in m['perms']:
        print(f"  0x{m['start']:012x}-0x{m['end']:012x} {m['perms']} {m['path']}")
```

## Process Injection (Linux)
```python
# ptrace — attach to a process and control it
import ctypes

PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_POKETEXT = 4
PTRACE_GETREGS = 12

libc = ctypes.CDLL("libc.so.6")

# Attach to target process
libc.ptrace(PTRACE_ATTACH, target_pid, 0, 0)
# Now you can read/write its memory and registers
# This is how debuggers and injection tools work
```
