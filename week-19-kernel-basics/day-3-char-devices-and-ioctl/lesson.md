# Day 3: Character Devices & IOCTL

## Character Devices
User space communicates with kernel modules through device files.
`/dev/mydevice` → your module gets read/write/ioctl calls.

## Registering a Char Device
```c
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "frostdev"
#define BUF_SIZE 1024

static int major_num;
static char device_buffer[BUF_SIZE];
static int buffer_len = 0;

// Called when user reads from device
static ssize_t dev_read(struct file *f, char __user *buf,
                        size_t len, loff_t *off) {
    int bytes = min(len, (size_t)(buffer_len - *off));
    if (bytes <= 0) return 0;
    if (copy_to_user(buf, device_buffer + *off, bytes))
        return -EFAULT;
    *off += bytes;
    return bytes;
}

// Called when user writes to device
static ssize_t dev_write(struct file *f, const char __user *buf,
                         size_t len, loff_t *off) {
    int bytes = min(len, (size_t)(BUF_SIZE - 1));
    if (copy_from_user(device_buffer, buf, bytes))
        return -EFAULT;
    device_buffer[bytes] = '\0';
    buffer_len = bytes;
    printk(KERN_INFO "frostdev: received %d bytes\n", bytes);
    return bytes;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .read = dev_read,
    .write = dev_write,
};

static int __init dev_init(void) {
    major_num = register_chrdev(0, DEVICE_NAME, &fops);
    printk(KERN_INFO "frostdev: registered with major %d\n", major_num);
    // Create device: mknod /dev/frostdev c <major> 0
    return 0;
}
```

## IOCTL — Custom Commands
```c
// ioctl lets user space send custom commands to your driver
// Define commands in a shared header:

#define FROST_IOC_MAGIC 'F'
#define FROST_GET_INFO    _IOR(FROST_IOC_MAGIC, 1, struct frost_info)
#define FROST_SET_CONFIG  _IOW(FROST_IOC_MAGIC, 2, struct frost_config)
#define FROST_DO_SCAN     _IO(FROST_IOC_MAGIC, 3)

struct frost_info {
    int version;
    int num_targets;
    char status[32];
};

// In the driver:
static long dev_ioctl(struct file *f, unsigned int cmd, unsigned long arg) {
    struct frost_info info;

    switch (cmd) {
    case FROST_GET_INFO:
        info.version = 1;
        info.num_targets = 42;
        strcpy(info.status, "active");
        if (copy_to_user((void __user *)arg, &info, sizeof(info)))
            return -EFAULT;
        return 0;

    case FROST_DO_SCAN:
        printk(KERN_INFO "frostdev: scan triggered!\n");
        return 0;

    default:
        return -EINVAL;
    }
}

// Add to file_operations:
// .unlocked_ioctl = dev_ioctl,
```

## Using From User Space
```c
// userspace_client.c
#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include "frost_ioctl.h"  // shared header with IOCTL definitions

int main() {
    int fd = open("/dev/frostdev", O_RDWR);
    if (fd < 0) { perror("open"); return 1; }

    // Send IOCTL command
    struct frost_info info;
    if (ioctl(fd, FROST_GET_INFO, &info) == 0) {
        printf("Version: %d\n", info.version);
        printf("Targets: %d\n", info.num_targets);
        printf("Status: %s\n", info.status);
    }

    // Write data
    write(fd, "Hello kernel!", 13);

    // Read data back
    char buf[256];
    int n = read(fd, buf, sizeof(buf));
    buf[n] = '\0';
    printf("Read back: %s\n", buf);

    close(fd);
    return 0;
}
```

## Or From Python
```python
import fcntl
import struct
import ctypes

fd = open("/dev/frostdev", "rb+", buffering=0)

# Write
fd.write(b"Hello from Python!")

# IOCTL
FROST_DO_SCAN = 0x4603  # _IO('F', 3)
fcntl.ioctl(fd, FROST_DO_SCAN)

fd.close()
```

## Vulnerability Angle
```
IOCTL handlers are a MASSIVE attack surface:
- Missing copy_from_user validation → kernel memory corruption
- Integer overflows in size calculations
- Race conditions (TOCTOU)
- Null pointer dereferences from bad user input

Many kernel exploits target buggy IOCTL handlers in drivers.
```
