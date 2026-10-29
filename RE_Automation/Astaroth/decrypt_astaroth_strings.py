import struct

KEY = b"RSPAUVCWE6BPGL310W8R2"
DELPHI_UNICODE_HEADER = b"\xb0\x04\x02\x00\xff\xff\xff\xff"
HEX_CHARS = set("0123456789abcdefABCDEF")
NESTED_ALPHABET = (
    "zxcvbnmlkjhgfdsaqwertyuiop?=&:/.-_!@#$%*+\\0987654321,; "
    "ZXCVBNMLKJHGFDSAQWERTYUIOP\"()[]{}çÇãÃõÕóÓéÉíÍáÁúÚ¨,XYU"
)

def decode_base25_pairs(text):
    salt = ord(text[0]) - ord("A")
    output = []
    for index in range(1, len(text), 2):
        high = ord(text[index]) - ord("A")
        low = ord(text[index + 1]) - ord("A")
        output.append(chr(high * 25 + low - salt - 100))
    return "".join(output)


def decrypt_string(encrypted_string):
    encrypted = bytes.fromhex(encrypted_string)
    previous = encrypted[0]
    delta = []

    for index, current in enumerate(encrypted[1:]):
        mixed = KEY[index % len(KEY)] ^ current
        if mixed > previous:
            delta.append(mixed - previous)
        else:
            delta.append(mixed + 0xFF - previous)
        previous = current

    stage = "".join(chr(value) for value in reversed(delta)).encode("cp1252")
    stage = bytes((9 - value) & 0xFF for value in stage).decode("cp1252")
    stage = decode_base25_pairs(stage)[::-1].encode("cp1252")
    plaintext = bytes((len(KEY) + 0x20 - value) & 0xFF for value in stage)
    return plaintext.decode("cp1252")


def decrypt_nested_string(text):
    if len(text) <= 6:
        return None

    payload = text[::-1][4:-2]
    if len(payload) % 2:
        return None

    output = []
    for index in range(0, len(payload), 2):
        high, low = payload[index:index + 2]
        if not ("A" <= high <= "K" and "0" <= low <= "9"):
            return None
        digit = 10 if low == "0" else int(low)
        alphabet_index = (ord(high) - ord("A")) * 10 + digit
        if not 1 <= alphabet_index <= len(NESTED_ALPHABET):
            return None
        output.append(NESTED_ALPHABET[alphabet_index - 1])

    return "".join(output) if len(output) >= 2 else None


def display_string(text):
    return text.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")


def set_decrypted_comment(container, address, plaintext):
    new_line = "Decrypted String -> " + display_string(plaintext)
    old_comment = container.get_comment_at(address) or ""
    old_lines = [
        line for line in old_comment.splitlines()
        if not line.startswith("Decrypted String -> ")
    ]
    container.set_comment_at(address, "\n".join(old_lines + [new_line]))


def find_encrypted_strings(view):
    results = []
    seen = set()
    for segment in view.segments:
        data = view.read(segment.start, segment.end - segment.start)
        position = 0
        while True:
            header_offset = data.find(DELPHI_UNICODE_HEADER, position)
            if header_offset < 0:
                break
            position = header_offset + 1
            if header_offset + 12 > len(data):
                continue
            length = struct.unpack_from("<I", data, header_offset + 8)[0]
            string_offset = header_offset + 12
            string_end = string_offset + length * 2
            if length < 8 or length % 2 or string_end > len(data):
                continue
            try:
                encrypted = data[string_offset:string_end].decode("utf-16le")
            except UnicodeDecodeError:
                continue
            if not encrypted or any(char not in HEX_CHARS for char in encrypted):
                continue
            address = segment.start + string_offset
            if address not in seen:
                seen.add(address)
                results.append((address, encrypted))

    return sorted(results)


def main(view):
    print("============ Astaroth Decryptor ============\n\n")
    for address, encrypted in find_encrypted_strings(view):
        try:
            first_layer = decrypt_string(encrypted)
        except (ValueError, UnicodeError, IndexError):
            continue
        nested = decrypt_nested_string(first_layer)
        plaintext = nested if nested is not None else first_layer
        plaintext_for_display = display_string(plaintext)

        print("\n[0x{:08X}] Encrypted String -> {}".format(address, encrypted))
        print("         Deccrypted String -> {}".format(plaintext_for_display))

        commented_locations = set()
        for reference in view.get_code_refs(address):
            function = reference.function
            location = (
                function.start if function is not None else None,
                reference.address,
            )
            if location in commented_locations:
                continue
            commented_locations.add(location)

            container = function if function is not None else view
            set_decrypted_comment(container, reference.address, plaintext)

try:
    bv
except NameError:
    raise RuntimeError("\n[-] What the fuck is happening? Even the Binary Ninja is open my friend? :)")

main(bv)