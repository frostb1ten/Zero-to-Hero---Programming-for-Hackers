# Day 2: Structs, Unions & File I/O

## Structs — Custom Data Types
```c
struct Host {
    char ip[16];
    int port;
    char service[32];
    int is_open;
};

// Use it
struct Host target;
strcpy(target.ip, "192.168.1.1");
target.port = 22;
strcpy(target.service, "SSH");
target.is_open = 1;

// With typedef (cleaner)
typedef struct {
    char ip[16];
    int port;
} Target;

Target t = {"10.0.0.1", 80};
```

## Struct Memory Layout (Critical for Exploits)
```c
struct Example {
    char a;     // 1 byte + 3 padding
    int b;      // 4 bytes
    char c;     // 1 byte + 3 padding
    int d;      // 4 bytes
};
// Total: 16 bytes (not 10!) because of alignment/padding

// Packed struct — no padding (used in network protocols)
struct __attribute__((packed)) PacketHeader {
    uint8_t  version;
    uint16_t length;
    uint32_t sequence;
};
// Total: exactly 7 bytes
```

## Unions — Overlapping Memory
```c
union Value {
    int as_int;
    float as_float;
    char as_bytes[4];
};

union Value v;
v.as_int = 0x41424344;
printf("Bytes: %c%c%c%c\n", v.as_bytes[0], v.as_bytes[1],
       v.as_bytes[2], v.as_bytes[3]);
// Prints the individual bytes of the int — useful for binary analysis
```

## File I/O
```c
// Write
FILE *fp = fopen("results.txt", "w");
if (fp) {
    fprintf(fp, "Port 22: open\n");
    fprintf(fp, "Port 80: open\n");
    fclose(fp);
}

// Read
FILE *fp = fopen("targets.txt", "r");
char line[256];
while (fgets(line, sizeof(line), fp)) {
    printf("Target: %s", line);
}
fclose(fp);

// Binary read/write (for binary files, exploits)
FILE *fp = fopen("shellcode.bin", "rb");
unsigned char buf[1024];
size_t bytes = fread(buf, 1, sizeof(buf), fp);
fclose(fp);
```
