# Day 2: Python ctypes — Bridge Python and C

## Why ctypes
- Call C functions and Windows API from Python
- Access raw memory
- Build exploits that interact with OS APIs
- Load DLLs and call their functions
- Essential for Windows exploit dev and malware

## Loading Libraries
```python
import ctypes

# Load standard C library
if sys.platform == "win32":
    libc = ctypes.cdll.msvcrt
    kernel32 = ctypes.windll.kernel32
    ntdll = ctypes.windll.ntdll
else:
    libc = ctypes.CDLL("libc.so.6")

# Call printf from C
libc.printf(b"Hello from C! %d\n", 42)
```

## C Types in Python
```python
import ctypes

# Type mapping:
# ctypes.c_int      → int (4 bytes)
# ctypes.c_uint     → unsigned int
# ctypes.c_char     → char (1 byte)
# ctypes.c_char_p   → char* (string pointer)
# ctypes.c_void_p   → void* (generic pointer)
# ctypes.c_size_t   → size_t
# ctypes.c_byte     → signed byte
# ctypes.c_ubyte    → unsigned byte
# ctypes.POINTER(type) → pointer to type
```

## Windows API Calls
```python
import ctypes

kernel32 = ctypes.windll.kernel32

# GetCurrentProcessId
pid = kernel32.GetCurrentProcessId()
print(f"PID: {pid}")

# MessageBox
user32 = ctypes.windll.user32
user32.MessageBoxW(0, "Hello from Python!", "ctypes", 0)

# VirtualAlloc — allocate executable memory
MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40
addr = kernel32.VirtualAlloc(0, 1024, MEM_COMMIT, PAGE_EXECUTE_READWRITE)
print(f"Allocated at: 0x{addr:08x}")
```

## Execute Shellcode via ctypes (Windows)
```python
import ctypes

# Shellcode bytes (example: MessageBox)
shellcode = bytearray(b"\x90\x90\x90\xcc")  # NOP NOP NOP INT3

# Allocate executable memory
kernel32 = ctypes.windll.kernel32
ptr = kernel32.VirtualAlloc(
    ctypes.c_int(0),
    ctypes.c_int(len(shellcode)),
    ctypes.c_int(0x3000),  # MEM_COMMIT | MEM_RESERVE
    ctypes.c_int(0x40)     # PAGE_EXECUTE_READWRITE
)

# Copy shellcode into allocated memory
ctypes.memmove(ptr, bytes(shellcode), len(shellcode))

# Create a thread to execute it
handle = kernel32.CreateThread(
    ctypes.c_int(0), ctypes.c_int(0),
    ctypes.c_int(ptr), ctypes.c_int(0),
    ctypes.c_int(0), ctypes.pointer(ctypes.c_int(0))
)

kernel32.WaitForSingleObject(handle, -1)
```

## Structures in ctypes
```python
import ctypes

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.c_ulong),
        ("lpReserved", ctypes.c_char_p),
        ("lpDesktop", ctypes.c_char_p),
        ("lpTitle", ctypes.c_char_p),
        ("dwX", ctypes.c_ulong),
        ("dwY", ctypes.c_ulong),
        # ... more fields
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", ctypes.c_void_p),
        ("hThread", ctypes.c_void_p),
        ("dwProcessId", ctypes.c_ulong),
        ("dwThreadId", ctypes.c_ulong),
    ]
```

## Reading/Writing Process Memory
```python
import ctypes

kernel32 = ctypes.windll.kernel32

# Open a process
PROCESS_ALL_ACCESS = 0x1F0FFF
handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, target_pid)

# Read memory
buffer = ctypes.create_string_buffer(64)
bytes_read = ctypes.c_size_t(0)
kernel32.ReadProcessMemory(handle, address, buffer, 64, ctypes.byref(bytes_read))

# Write memory
data = b"\x90\x90\x90\x90"
kernel32.WriteProcessMemory(handle, address, data, len(data), None)
```
