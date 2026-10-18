""""
    Eternidade Stealer's String Decryptor for Binary Ninja
"""

KEY = "edit1"
SALT = "MeuSaltPessoal#2024"
HEX = "0123456789abcdefABCDEF"


def decrypt(text):
    text = "".join(char for char in text if char in HEX)

    if len(text) < 2 or len(text) % 2:
        return None

    encrypted = bytes.fromhex(text)
    decrypted = bytearray()

    for index, value in enumerate(encrypted):
        value = (value - 5) & 0xFF
        value ^= ord(KEY[index % len(KEY)])
        value ^= ord(SALT[index % len(SALT)])
        decrypted.append(value)

    try:
        return decrypted.decode("utf-8")
    except UnicodeDecodeError:
        return None

print(f"======== Eternidade Stealer String Decoder ========\n\n")
for string in bv.strings:
    raw = bv.read(string.start, string.length)

    try:
        text = raw.decode("utf-16le")
    except UnicodeDecodeError:
        continue

    plaintext = decrypt(text)

    if plaintext and len(plaintext) > 8:
        prefix = plaintext[:8]
        str_value = plaintext[8:]
        print(f"    {string.start:#x}:      {str_value}")
        for reference in bv.get_code_refs(string.start):
            reference.function.set_comment_at(reference.address,f"Decrypted String -> {str_value}")
