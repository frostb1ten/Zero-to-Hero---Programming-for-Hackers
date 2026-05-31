# Day 2: Writing Linux Kernel Modules

## What's a Kernel Module?
Code you can load into the running kernel WITHOUT rebooting.
Used for: drivers, filesystems, rootkits, security tools.

## Hello World Module
```c
// hello.c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Frost");
MODULE_DESCRIPTION("Hello World kernel module");

static int __init hello_init(void) {
    printk(KERN_INFO "Hello from kernel space!\n");
    return 0;  // 0 = success
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye from kernel space!\n");
}

module_init(hello_init);
module_exit(hello_exit);
```

## Building
```makefile
# Makefile
obj-m += hello.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

```bash
make
sudo insmod hello.ko   # load
dmesg | tail           # see output
lsmod | grep hello     # verify loaded
sudo rmmod hello       # unload
```

## Kernel API (Key Functions)
```c
// Memory allocation
void *kmalloc(size_t size, gfp_t flags);  // like malloc
void kfree(void *ptr);                     // like free
// flags: GFP_KERNEL (can sleep), GFP_ATOMIC (can't sleep)

// Printing
printk(KERN_INFO "message\n");
printk(KERN_ERR "error: %d\n", errno);
// Levels: KERN_EMERG, KERN_ALERT, KERN_CRIT, KERN_ERR,
//         KERN_WARNING, KERN_NOTICE, KERN_INFO, KERN_DEBUG

// Process info
current->pid            // current process PID
current->comm           // process name
current->cred->uid      // user ID

// Linked lists (kernel uses these everywhere)
struct list_head {
    struct list_head *next, *prev;
};
```

## Interacting with User Space
```c
#include <linux/uaccess.h>

// Copy data from user space to kernel
unsigned long copy_from_user(void *to, const void __user *from, unsigned long n);

// Copy data from kernel to user space
unsigned long copy_to_user(void __user *to, const void *from, unsigned long n);

// NEVER directly dereference user pointers in kernel!
// They might be invalid → kernel crash (panic)
```

## Creating a /proc Entry
```c
#include <linux/proc_fs.h>
#include <linux/seq_file.h>

static int my_show(struct seq_file *m, void *v) {
    seq_printf(m, "Hello from /proc/mymodule!\n");
    seq_printf(m, "Current PID: %d\n", current->pid);
    return 0;
}

static int my_open(struct inode *inode, struct file *file) {
    return single_open(file, my_show, NULL);
}

static const struct proc_ops my_fops = {
    .proc_open = my_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};

static int __init my_init(void) {
    proc_create("mymodule", 0, NULL, &my_fops);
    return 0;
}

static void __exit my_exit(void) {
    remove_proc_entry("mymodule", NULL);
}
```

## Security: Why This Matters
```
Kernel module = FULL kernel access
  - Read/write ANY memory
  - Hook ANY function
  - Hide ANY process/file/connection
  - Intercept ANY syscall
  - Impossible to detect from userspace alone

This is why:
  - Rootkits load as kernel modules
  - Secure systems restrict module loading
  - Module signing exists (won't load unsigned modules)
```
