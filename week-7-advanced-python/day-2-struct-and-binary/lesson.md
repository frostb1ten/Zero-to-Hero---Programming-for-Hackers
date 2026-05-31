# Day 2: struct, Bytes & Binary Data

## Why This Matters
Exploit dev and malware work operate at the byte level.
You need to pack/unpack binary data, manipulate bytes, understand
memory layouts, and work with raw network protocols.

## Bytes vs Strings
```python
# Strings = human text (Unicode)
text = "Hello"

# Bytes = raw data (0-255 per byte)
raw = b"Hello"
raw = b"\x48\x65\x6c\x6c\x6f"  # same thing in hex

# Convert between them
text.encode()        # str → bytes (UTF-8)
raw.decode()         # bytes → str

# You CANNOT mix them
# b"hello" + "world"  ← TypeError!
```

## Hex, Binary, and Representations
```python
# Decimal, hex, binary, octal
n = 255
print(f"Dec: {n}")
print(f"Hex: {hex(n)}")      # 0xff
print(f"Bin: {bin(n)}")      # 0b11111111
print(f"Oct: {oct(n)}")      # 0o377

# From hex string to int
int("0xff", 16)   # 255
int("ff", 16)     # 255

# Hex string to bytes
bytes.fromhex("48656c6c6f")   # b'Hello'
b"Hello".hex()                 # '48656c6c6f'
```

## struct — Pack/Unpack Binary Data
```python
import struct

# Pack Python values into bytes (like C does in memory)
# '<' = little-endian, '>' = big-endian (network byte order)
# 'I' = unsigned int (4 bytes)
# 'H' = unsigned short (2 bytes)
# 'B' = unsigned byte (1 byte)

packed = struct.pack('<I', 0xdeadbeef)
print(packed)        # b'\xef\xbe\xad\xde' (little-endian)
print(packed.hex())  # efbeadde

packed = struct.pack('>I', 0xdeadbeef)
print(packed)        # b'\xde\xad\xbe\xef' (big-endian)

# Unpack bytes back into values
data = b'\xef\xbe\xad\xde'
value = struct.unpack('<I', data)[0]
print(f"0x{value:08x}")  # 0xdeadbeef
```

## Format Characters
```
Format  C Type           Python Type    Size
------  ------           -----------    ----
B       unsigned char    int            1
H       unsigned short   int            2
I       unsigned int     int            4
Q       unsigned long    int            8
s       char[]           bytes          N
<       little-endian
>       big-endian (network)
```

## Packing Addresses (Exploit Dev Essential)
```python
import struct

# Pack a return address for a buffer overflow
ret_addr = 0x7fff1234
payload = struct.pack('<I', ret_addr)
print(f"Packed address: {payload.hex()}")
# 34127fff — notice reversed order (little-endian)

# Pack multiple values
header = struct.pack('>HHI', 
    0x1337,    # magic number (2 bytes)
    80,        # port (2 bytes)  
    0xc0a80001 # IP 192.168.0.1 as int (4 bytes)
)
```

## Bytearray — Mutable Bytes
```python
# bytes is immutable, bytearray is mutable
buf = bytearray(b"\x00" * 100)  # 100 null bytes
buf[0] = 0x41                    # set first byte to 'A'
buf[4:8] = struct.pack('<I', 0xdeadbeef)  # overwrite bytes 4-7

# Build a payload
nop_sled = bytearray(b"\x90" * 50)   # NOP sled
shellcode = bytearray(b"\xcc\xcc")    # INT3 breakpoints
payload = nop_sled + shellcode
```

## Bitwise Operations
```python
# AND, OR, XOR, NOT, shifts
a = 0b11001010
b = 0b10110011

a & b    # AND:  0b10000010 (both bits set)
a | b    # OR:   0b11111011 (either bit set)
a ^ b    # XOR:  0b01111001 (different bits)
~a       # NOT:  inverts all bits
a << 2   # shift left by 2
a >> 2   # shift right by 2

# XOR encryption (simple but real)
def xor_encrypt(data, key):
    return bytes([b ^ key for b in data])

encrypted = xor_encrypt(b"SECRET", 0x42)
decrypted = xor_encrypt(encrypted, 0x42)  # XOR again to decrypt
print(decrypted)  # b'SECRET'
```
