# Day 2: Dynamic Analysis — Debugging Live Binaries

## Tools
- **x64dbg** (Windows) — modern, free, plugin-rich
- **GDB + pwndbg** (Linux) — scripting powerhouse
- **WinDbg** (Windows) — kernel debugging
- **Frida** — dynamic instrumentation framework
- **API Monitor** (Windows) — intercept API calls

## Dynamic Analysis Workflow
```
1. Set up isolated environment (VM!)
2. Take snapshot before running
3. Start monitoring (ProcMon, Wireshark, strace)
4. Run binary under debugger
5. Observe: What does it do?
   - Files created/modified?
   - Registry changes?
   - Network connections?
   - Processes spawned?
6. Set breakpoints at interesting functions
7. Trace execution path
```

## Frida — Dynamic Instrumentation
```python
# pip install frida frida-tools

import frida

# Attach to a running process
session = frida.attach("target.exe")

# Inject JavaScript to hook functions
script = session.create_script("""
    // Hook MessageBoxW
    var MessageBoxW = Module.findExportByName("user32.dll", "MessageBoxW");
    Interceptor.attach(MessageBoxW, {
        onEnter: function(args) {
            console.log("[*] MessageBoxW called!");
            console.log("    Text: " + args[1].readUtf16String());
            console.log("    Title: " + args[2].readUtf16String());
        }
    });

    // Hook strcmp to see password checks
    var strcmp = Module.findExportByName(null, "strcmp");
    Interceptor.attach(strcmp, {
        onEnter: function(args) {
            console.log("[strcmp] " + args[0].readCString() +
                        " vs " + args[1].readCString());
        }
    });
""")
script.load()
```

## Anti-Debugging Techniques & Bypasses
```python
# Common anti-debug checks:

# 1. IsDebuggerPresent (Windows)
# Reads PEB.BeingDebugged flag
# Bypass: Set PEB.BeingDebugged = 0 in debugger

# 2. CheckRemoteDebuggerPresent
# Bypass: Hook NtQueryInformationProcess

# 3. Timing checks
# rdtsc or GetTickCount differences
# Bypass: Patch the comparison or skip the check

# 4. Hardware breakpoint detection
# DR0-DR7 registers
# Bypass: Clear debug registers

# 5. INT 3 scanning (looking for software breakpoints)
# Bypass: Use hardware breakpoints instead

# Frida bypass for IsDebuggerPresent:
"""
var IsDebuggerPresent = Module.findExportByName("kernel32.dll", "IsDebuggerPresent");
Interceptor.replace(IsDebuggerPresent, new NativeCallback(function() {
    return 0;  // always return "not debugged"
}, 'int', []));
"""
```

## Process Monitor (ProcMon) Filters
```
Useful filters for malware analysis:
  Process Name = malware.exe
  Operation = WriteFile         → what files it creates
  Operation = RegSetValue       → registry persistence
  Operation = TCP Connect       → C2 communication
  Operation = CreateFile        → what it reads/accesses
  Path contains = \Run          → persistence keys
  Path contains = \Startup      → startup folder drops
```
