# Day 1: Kernel Architecture

## What The Kernel Does
The kernel is the core of the OS. It manages:
- **Memory** — virtual memory, page tables, allocation
- **Processes** — creation, scheduling, termination
- **Devices** — drivers, I/O requests
- **Security** — access control, capabilities, namespaces
- **Filesystems** — VFS layer, actual FS implementations
- **Networking** — TCP/IP stack, sockets

## Linux Kernel Architecture
```
User Space (Ring 3):
  Applications → libc → syscall interface
─────────────────────────────────────────────────
Kernel Space (Ring 0):
┌─────────────────────────────────────────────┐
│ System Call Interface                        │
├─────────────────────────────────────────────┤
│ Process Mgmt │ Memory Mgmt │ File Systems   │
│ (scheduler,  │ (page tables│ (VFS, ext4,    │
│  fork, exec) │  mmap, brk) │  procfs)       │
├──────────────┼─────────────┼────────────────┤
│ Device Drivers              │ Network Stack   │
│ (char, block, network)      │ (TCP/IP, socks)│
├─────────────────────────────┴────────────────┤
│ Architecture-Dependent Code (x86, ARM, etc.)  │
└───────────────────────────────────────────────┘
  Hardware (CPU, RAM, Disk, NIC)
```

## Monolithic vs Microkernel
```
Linux = Monolithic (everything in kernel space)
  + Fast (no context switches between components)
  - Bigger attack surface (bug in driver = kernel compromise)
  - A driver crash = kernel crash

Windows NT = Hybrid (some user-mode services)
macOS/iOS = Hybrid (Mach microkernel + BSD layer)
```

## Kernel Source Layout (Linux)
```
linux/
├── arch/        ← architecture-specific (x86, arm, etc.)
├── block/       ← block device layer
├── crypto/      ← cryptographic algorithms
├── drivers/     ← ALL device drivers
├── fs/          ← filesystems (ext4, procfs, etc.)
├── include/     ← header files
├── init/        ← startup code (main.c → start_kernel())
├── ipc/         ← inter-process communication
├── kernel/      ← core: scheduler, signals, fork
├── lib/         ← helper libraries
├── mm/          ← memory management
├── net/         ← networking stack
├── security/    ← LSM, SELinux, AppArmor
└── sound/       ← audio drivers
```

## Privilege Rings
```
Ring 0: Kernel — full hardware access, all instructions
Ring 1-2: (rarely used on x86)
Ring 3: User space — restricted, can't access hardware directly

Transition Ring 3 → Ring 0:
  - System calls (int 0x80, syscall, sysenter)
  - Hardware interrupts
  - Exceptions (page fault, divide by zero)

A kernel exploit = getting Ring 0 execution from Ring 3
```

## Key Kernel Concepts
```
1. Kernel Objects: task_struct (process), file_struct, inode, socket
2. Slab Allocator: kmalloc/kfree (kernel's malloc)
3. Interrupts: hardware signals that preempt execution
4. Context Switch: saving/restoring process state
5. DMA: Direct Memory Access (hardware writes directly to RAM)
6. IOCTL: Custom commands to drivers from userspace
7. procfs/sysfs: Virtual filesystems exposing kernel state
```

## Building the Kernel (for development)
```bash
# Get source
git clone https://github.com/torvalds/linux.git
cd linux

# Configure
make menuconfig   # or: make defconfig

# Build
make -j$(nproc)

# Install (on a VM!)
sudo make modules_install
sudo make install

# Boot into your kernel
# (update GRUB, select new kernel)
```
