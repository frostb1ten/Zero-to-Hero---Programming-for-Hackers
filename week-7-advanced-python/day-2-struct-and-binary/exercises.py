# =============================================================
# EXERCISES — struct, Bytes & Binary Data
# =============================================================
import struct


# --- Exercise 1: Bytes and hex ---
# Convert the string "HACK" to bytes, then print its hex representation
text = "HACK"
as_bytes = ___
as_hex = ___
print(f"'{text}' → bytes: {as_bytes} → hex: {as_hex}")
# Expected hex: 4841434b


# --- Exercise 2: Pack an address ---
# Pack 0xcafebabe as a little-endian unsigned int
address = 0xcafebabe
packed = struct.pack(___)
print(f"Packed: {packed.hex()}")
# Expected: bebafeca (reversed because LE)


# --- Exercise 3: Unpack bytes ---
# Unpack these bytes as a big-endian unsigned short (port number)
raw = b"\x1f\x90"
port = struct.unpack(___)[0]
print(f"Port: {port}")
# Expected: 8080


# --- Exercise 4: Build a buffer ---
# Create a 20-byte buffer:
# Bytes 0-3:  "AAAA"
# Bytes 4-7:  0xdeadbeef (little-endian)
# Bytes 8-19: null bytes

buf = bytearray(___)
buf[0:4] = ___
buf[4:8] = ___
print(f"Buffer: {buf.hex()}")


# --- Exercise 5: XOR encryption ---
# Write a function that XOR-encrypts data with a single byte key
# Then encrypt "SECRET" with key 0x41 and decrypt it back

def xor_encrypt(data, key):
    return bytes([___])

original = b"SECRET"
encrypted = xor_encrypt(original, 0x41)
decrypted = ___
print(f"Original:  {original}")
print(f"Encrypted: {encrypted.hex()}")
print(f"Decrypted: {decrypted}")
# Decrypted should match original


# --- Exercise 6: Multi-byte XOR ---
# XOR with a multi-byte key (cycle through key bytes)

def xor_multi(data, key):
    return bytes([___])

msg = b"ATTACK"
key = b"AB"
enc = xor_multi(msg, key)
dec = xor_multi(enc, key)
print(f"Multi XOR: {msg} → {enc.hex()} → {dec}")


# --- Exercise 7: Pack a custom protocol header ---
# Pack: magic=0x1337 (2B BE), version=1 (1B), flags=0 (1B), length=256 (4B BE)
header = struct.pack(___)
print(f"Header: {header.hex()}")
# Expected: 13370100 00000100


print("\n--- All exercises complete! ---")
