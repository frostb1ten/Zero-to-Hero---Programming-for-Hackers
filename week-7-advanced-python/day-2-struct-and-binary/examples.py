# =============================================================
# EXAMPLES — struct, Bytes & Binary Data
# =============================================================
import struct


# --- 1. Bytes basics ---
print("[1] Bytes vs strings:")
text = "ABCD"
raw = b"ABCD"
print(f"  String: {text} (type: {type(text).__name__})")
print(f"  Bytes:  {raw} (type: {type(raw).__name__})")
print(f"  Hex:    {raw.hex()}")
print(f"  Individual bytes: {list(raw)}")
print()


# --- 2. Hex conversions ---
print("[2] Hex conversions:")
value = 0xdeadbeef
print(f"  0xdeadbeef = {value} (decimal)")
print(f"  hex(255) = {hex(255)}")
print(f"  bin(255) = {bin(255)}")
print(f"  bytes.fromhex('41424344') = {bytes.fromhex('41424344')}")
print(f"  b'ABCD'.hex() = {b'ABCD'.hex()}")
print()


# --- 3. struct packing ---
print("[3] struct.pack():")
# Little-endian unsigned int
le = struct.pack('<I', 0xdeadbeef)
print(f"  LE 0xdeadbeef: {le.hex()} = {list(le)}")

# Big-endian unsigned int (network byte order)
be = struct.pack('>I', 0xdeadbeef)
print(f"  BE 0xdeadbeef: {be.hex()} = {list(be)}")

# Multiple values
packet = struct.pack('>BBH', 1, 2, 8080)
print(f"  Packet (ver=1, type=2, port=8080): {packet.hex()}")
print()


# --- 4. struct unpacking ---
print("[4] struct.unpack():")
data = bytes.fromhex("efbeadde")
value = struct.unpack('<I', data)[0]
print(f"  {data.hex()} (LE) = 0x{value:08x}")

# Unpack a multi-field header
header = bytes.fromhex("01021f90")
ver, msg_type, port = struct.unpack('>BBH', header)
print(f"  Header: version={ver}, type={msg_type}, port={port}")
print()


# --- 5. Building a payload buffer ---
print("[5] Payload construction:")
buf = bytearray(32)
buf[0:4] = b"AAAA"                          # padding
buf[4:8] = struct.pack('<I', 0x41414141)     # overwrite
buf[8:12] = struct.pack('<I', 0xdeadbeef)    # return address

print(f"  Buffer: {buf.hex()}")
print(f"  Printable: {buf}")
print()


# --- 6. XOR encryption ---
print("[6] XOR encrypt/decrypt:")

def xor_crypt(data, key):
    if isinstance(data, str):
        data = data.encode()
    return bytes([b ^ key for b in data])

original = b"ATTACK AT DAWN"
key = 0x55
encrypted = xor_crypt(original, key)
decrypted = xor_crypt(encrypted, key)

print(f"  Original:  {original}")
print(f"  Encrypted: {encrypted.hex()}")
print(f"  Decrypted: {decrypted}")
print()


# --- 7. Multi-byte XOR ---
print("[7] Multi-byte XOR key:")

def xor_multi(data, key):
    if isinstance(data, str):
        data = data.encode()
    if isinstance(key, str):
        key = key.encode()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

msg = b"Hello, World!"
key = b"KEY"
enc = xor_multi(msg, key)
dec = xor_multi(enc, key)
print(f"  Original:  {msg}")
print(f"  Encrypted: {enc.hex()}")
print(f"  Decrypted: {dec}")
print()


# --- 8. IP address as integer ---
print("[8] IP ↔ integer:")
import socket

ip_str = "192.168.1.1"
ip_int = struct.unpack('>I', socket.inet_aton(ip_str))[0]
print(f"  {ip_str} = {ip_int} = 0x{ip_int:08x}")

# Back to string
ip_back = socket.inet_ntoa(struct.pack('>I', ip_int))
print(f"  0x{ip_int:08x} = {ip_back}")
