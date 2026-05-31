# Day 3: DLLs, Services & Registry

## DLLs (Dynamic Link Libraries)
```
DLLs are shared code libraries loaded at runtime.
Every Windows process loads: ntdll.dll, kernel32.dll, etc.

Key concepts:
- DllMain() — called when DLL is loaded/unloaded
- Export table — functions the DLL exposes
- DLL search order — where Windows looks for DLLs
- DLL hijacking — place malicious DLL where app looks first
```

## DLL Injection Techniques
```python
# Classic DLL Injection via CreateRemoteThread:
# 1. OpenProcess(target)
# 2. VirtualAllocEx — allocate memory in target
# 3. WriteProcessMemory — write DLL path into target
# 4. CreateRemoteThread — call LoadLibraryA with DLL path

import ctypes

kernel32 = ctypes.windll.kernel32

def inject_dll(pid, dll_path):
    # Open target process
    PROCESS_ALL_ACCESS = 0x1F0FFF
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    # Allocate memory for DLL path
    dll_bytes = dll_path.encode() + b"\x00"
    remote_mem = kernel32.VirtualAllocEx(
        h_process, 0, len(dll_bytes), 0x3000, 0x40)

    # Write DLL path
    kernel32.WriteProcessMemory(
        h_process, remote_mem, dll_bytes, len(dll_bytes), None)

    # Get LoadLibraryA address
    load_lib = kernel32.GetProcAddress(
        kernel32.GetModuleHandleA(b"kernel32.dll"),
        b"LoadLibraryA")

    # Create remote thread calling LoadLibraryA(dll_path)
    kernel32.CreateRemoteThread(
        h_process, None, 0, load_lib, remote_mem, 0, None)
```

## Windows Services
```
Services run in the background as SYSTEM (highest privilege).
Managed by SCM (Service Control Manager).

# Query services
sc query
sc qc ServiceName        # configuration
sc queryex type=service  # extended info

# Security relevance:
# - Weak service permissions → privilege escalation
# - Unquoted service paths → binary planting
# - Writable service binary → code execution as SYSTEM
```

## Registry — Windows Configuration Database
```
Hives:
  HKLM (HKEY_LOCAL_MACHINE) — system-wide settings
  HKCU (HKEY_CURRENT_USER)  — per-user settings
  HKU  (HKEY_USERS)         — all user profiles

Security-relevant keys:
  HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run  ← persistence
  HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run  ← user persist
  HKLM\SYSTEM\CurrentControlSet\Services              ← services
  HKLM\SAM\SAM                                        ← password hashes
```

## Python Registry Access
```python
import winreg

# Read a value
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
    r"SOFTWARE\Microsoft\Windows\CurrentVersion")
value, _ = winreg.QueryValueEx(key, "ProgramFilesDir")
print(f"Program Files: {value}")
winreg.CloseKey(key)

# Enumerate Run keys (persistence check)
def get_run_keys():
    locations = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
    ]
    for hive, path in locations:
        try:
            key = winreg.OpenKey(hive, path)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    print(f"  {name}: {value}")
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
```
