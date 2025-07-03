encrypted_hex = """
PLACE HERE THE ENCRYPTED RAW BYTES OF 2nd STAGE
"""

encrypted_hex = encrypted_hex.replace(" ", "").replace("\n", "").strip()

encrypted_bytes = bytes.fromhex(encrypted_hex)

decrypted_bytes = bytearray()
for byte in encrypted_bytes:
    decrypted_bytes.append(byte ^ 0x99)

with open('second-stage.bin', 'wb') as f:
    f.write(decrypted_bytes)

print(f"[+] Decrypted {len(encrypted_bytes)} bytes")
print(f"[+] Saved to: second-stage.bin")

if len(decrypted_bytes) >= 16:
    print(f"[+] First 16 bytes: {decrypted_bytes[:16].hex()}")
    
    if decrypted_bytes[:2] == b'MZ':
        print("[+] Detected PE file signature!")