# Day 1: Windows Architecture & API

## Windows Architecture Layers
```
User Mode (Ring 3):
┌─────────────────────────────────────────┐
│  Applications (notepad, chrome, etc.)    │
├─────────────────────────────────────────┤
│  Subsystem DLLs (kernel32, user32, etc.) │
├─────────────────────────────────────────┤
│  ntdll.dll (syscall stubs)               │
└────────────────┬────────────────────────┘
                 │ SYSCALL instruction
┌────────────────▼────────────────────────┐
│  NT Kernel (ntoskrnl.exe)                │  Kernel Mode (Ring 0)
├─────────────────────────────────────────┤
│  HAL (Hardware Abstraction Layer)        │
├─────────────────────────────────────────┤
│  Drivers (.sys files)                    │
└─────────────────────────────────────────┘
```

## Key Windows Components
```
kernel32.dll  — Process/thread/file management
ntdll.dll     — Native API (syscall interface)
user32.dll    — Window management, messages
ws2_32.dll    — Winsock (networking)
advapi32.dll  — Registry, security, services
```

## Windows API Calling Pattern
```python
import ctypes
from ctypes import wintypes

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)

# Get current process info
pid = kernel32.GetCurrentProcessId()
tid = kernel32.GetCurrentThreadId()
print(f"PID: {pid}, TID: {tid}")

# Open a process
PROCESS_ALL_ACCESS = 0x1F0FFF
handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, target_pid)
if not handle:
    error = ctypes.get_last_error()
    print(f"Failed: error {error}")
```

## Important Windows Structures
```
PEB (Process Environment Block):
  - Loaded modules list (DLLs)
  - Process parameters
  - Heap information
  - Being debugged flag ← anti-debug checks read this

TEB (Thread Environment Block):
  - Stack base and limit
  - Exception handler chain (SEH)
  - PEB pointer
  - TLS (Thread Local Storage)

EPROCESS (kernel):
  - Full process information
  - Security token
  - Handle table
  - Process links (for hiding)
```

## Processes and Threads
```python
import ctypes

kernel32 = ctypes.windll.kernel32

# Create a new process
class STARTUPINFO(ctypes.Structure):
    _fields_ = [("cb", ctypes.c_ulong)] + [("_pad", ctypes.c_void_p)] * 17

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", ctypes.c_void_p),
        ("hThread", ctypes.c_void_p),
        ("dwProcessId", ctypes.c_ulong),
        ("dwThreadId", ctypes.c_ulong),
    ]

si = STARTUPINFO()
si.cb = ctypes.sizeof(si)
pi = PROCESS_INFORMATION()

# CreateProcessW
kernel32.CreateProcessW(
    "C:\\Windows\\System32\\notepad.exe",  # app
    None,                                    # cmd line
    None, None,                              # security attrs
    False,                                   # inherit handles
    0,                                       # creation flags
    None,                                    # environment
    None,                                    # current dir
    ctypes.byref(si),
    ctypes.byref(pi)
)
print(f"Created process PID: {pi.dwProcessId}")
```

## Security Tokens and Privileges
```
Every process has a token containing:
- User SID (who you are)
- Group SIDs (what groups you're in)
- Privileges (SeDebugPrivilege, SeShutdownPrivilege, etc.)

SeDebugPrivilege = can open ANY process (needed for injection)
SeLoadDriverPrivilege = can load kernel drivers
SeTakeOwnershipPrivilege = own any object

Privilege escalation = getting a token with more privileges
```
