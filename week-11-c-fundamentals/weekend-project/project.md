# Week 11 Project: C Port Scanner

Build a simple TCP port scanner in C.

## Requirements
1. Accept target IP and port range from command line
2. Use `socket()`, `connect()` to check ports
3. Print open ports with service names
4. Handle timeouts properly
5. Compile with: `gcc scanner.c -o scanner`

## Usage
```
./scanner 192.168.1.1 1 1024
```

## Key C Functions You'll Need
```c
#include <sys/socket.h>   // socket(), connect()
#include <netinet/in.h>   // sockaddr_in
#include <arpa/inet.h>    // inet_addr()
#include <unistd.h>       // close()
#include <fcntl.h>        // fcntl() for non-blocking

int sock = socket(AF_INET, SOCK_STREAM, 0);

struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(port);
addr.sin_addr.s_addr = inet_addr(ip);

int result = connect(sock, (struct sockaddr*)&addr, sizeof(addr));
close(sock);
```

## Compare With Your Python Scanner
After building this in C, you'll understand:
- Why Python is slower (it wraps all of this)
- Why C overflows happen (raw memory management)
- How sockets actually work at the OS level
