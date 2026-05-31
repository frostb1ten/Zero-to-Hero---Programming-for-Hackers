# =============================================================
# SOLUTIONS — struct, Bytes & Binary Data
# =============================================================
import struct

# --- Exercise 1 ---
text = "HACK"
as_bytes = text.encode()
as_hex = as_bytes.hex()
print(f"'{text}' → bytes: {as_bytes} → hex: {as_hex}")

# --- Exercise 2 ---
address = 0xcafebabe
packed = struct.pack('<I', address)
print(f"Packed: {packed.hex()}")

# --- Exercise 3 ---
raw = b"\x1f\x90"
port = struct.unpack('>H', raw)[0]
print(f"Port: {port}")

# --- Exercise 4 ---
buf = bytearray(20)
buf[0:4] = b"AAAA"
buf[4:8] = struct.pack('<I', 0xdeadbeef)
print(f"Buffer: {buf.hex()}")

# --- Exercise 5 ---
def xor_encrypt(data, key):
    return bytes([b ^ key for b in data])

original = b"SECRET"
encrypted = xor_encrypt(original, 0x41)
decrypted = xor_encrypt(encrypted, 0x41)
print(f"Original:  {original}")
print(f"Encrypted: {encrypted.hex()}")
print(f"Decrypted: {decrypted}")

# --- Exercise 6 ---
def xor_multi(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

msg = b"ATTACK"
key = b"AB"
enc = xor_multi(msg, key)
dec = xor_multi(enc, key)
print(f"Multi XOR: {msg} → {enc.hex()} → {dec}")

# --- Exercise 7 ---
header = struct.pack('>HBBI', 0x1337, 1, 0, 256)
print(f"Header: {header.hex()}")

print("\n--- All exercises complete! ---")
