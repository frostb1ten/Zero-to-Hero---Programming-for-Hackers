# =============================================================
# EXAMPLES — Evasion & Persistence Concepts (Educational)
# =============================================================
import base64
import zlib
import platform
import os
import sys


# --- 1. String obfuscation techniques ---
print("[1] String obfuscation:")

# Original: "whoami"
target = "whoami"

# Method 1: chr() building
obf1 = chr(119)+chr(104)+chr(111)+chr(97)+chr(109)+chr(105)
print(f"  chr():     {obf1}")

# Method 2: Reverse
obf2 = "imaohw"[::-1]
print(f"  reverse:   {obf2}")

# Method 3: Base64
obf3 = base64.b64decode("d2hvYW1p").decode()
print(f"  base64:    {obf3}")

# Method 4: XOR
def xor_str(data, key):
    return bytes([b ^ key for b in data.encode()])

obf4_enc = xor_str(target, 0x42)
obf4_dec = bytes([b ^ 0x42 for b in obf4_enc]).decode()
print(f"  xor enc:   {obf4_enc.hex()}")
print(f"  xor dec:   {obf4_dec}")

print(f"  All match: {obf1 == obf2 == obf3 == obf4_dec == target}")
print()


# --- 2. Code obfuscation ---
print("[2] Code obfuscation:")
code = "print('Hello from obfuscated code')"

# Encode
encoded = base64.b64encode(code.encode()).decode()
print(f"  Original:  {code}")
print(f"  Encoded:   {encoded}")
print(f"  Decoder:   exec(base64.b64decode('{encoded}').decode())")
# exec(base64.b64decode(encoded).decode())  # this would run it
print()


# --- 3. Compression + encoding ---
print("[3] Compression + encoding:")
large_code = "print('x')\n" * 100
compressed = zlib.compress(large_code.encode())
b64_comp = base64.b64encode(compressed).decode()
print(f"  Original:    {len(large_code)} bytes")
print(f"  Compressed:  {len(compressed)} bytes")
print(f"  B64+Comp:    {len(b64_comp)} bytes")
print(f"  Ratio:       {len(b64_comp)/len(large_code)*100:.0f}%")
print()


# --- 4. Environment detection ---
print("[4] Environment analysis:")
checks = {
    "Platform": platform.system(),
    "Hostname": platform.node(),
    "Python":   platform.python_version(),
    "Is 64-bit": sys.maxsize > 2**32,
    "Interactive": hasattr(sys, 'ps1'),
    "Debugger": sys.gettrace() is not None,
    "Frozen": getattr(sys, 'frozen', False),
}
for check, value in checks.items():
    print(f"  {check:<14}: {value}")
print()


# --- 5. Common persistence locations ---
print("[5] Persistence locations (reference):")
if platform.system() == "Windows":
    locations = {
        "Startup": os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),
        "Run Key": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
        "Tasks": "schtasks",
    }
else:
    locations = {
        "Crontab": "crontab -l",
        "Profile": "~/.bashrc",
        "Systemd": "/etc/systemd/system/",
    }

for name, path in locations.items():
    print(f"  {name}: {path}")
print()


# --- 6. DNS exfiltration concept ---
print("[6] DNS exfiltration encoding:")

def encode_for_dns(data, domain="exfil.example.com"):
    """Encode data as DNS-safe subdomain labels."""
    encoded = base64.b32encode(data.encode()).decode().lower().rstrip("=")
    # DNS labels max 63 chars
    chunks = [encoded[i:i+60] for i in range(0, len(encoded), 60)]
    queries = [f"{chunk}.{domain}" for chunk in chunks]
    return queries

test = "password=admin123"
queries = encode_for_dns(test)
print(f"  Data: {test}")
print(f"  DNS queries needed: {len(queries)}")
for q in queries:
    print(f"    {q}")
