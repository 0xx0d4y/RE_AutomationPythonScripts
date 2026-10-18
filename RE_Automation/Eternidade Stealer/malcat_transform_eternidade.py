"""
    Author: 0x0d4y
"""

from transforms.base import Transform

def eternidade_decrypt(data: bytes, key0: int = 3333, key1: int = 3434, state: int = 1000) -> bytes:
    output = bytearray(len(data))

    for i, cipher_byte in enumerate(data):
        key_byte = (state >> 8) & 0xFF

        plain_byte = cipher_byte ^ key_byte
        output[i] = plain_byte

        state = ((((plain_byte + state) & 0xFF) * key0) + key1) & 0xFFFF
    return bytes(output)


def lznt1_decompress_chunk(chunk: bytes) -> bytes:
    output = bytearray()
    offset = 0
    while offset < len(chunk):
        flags = chunk[offset]
        offset += 1
        for bit in range(8):
            if offset >= len(chunk):
                break
            if flags & (1 << bit):

                if offset + 2 > len(chunk):
                    raise ValueError(
                        "LZNT1: error for some reason my friend"
                    )
                token = (
                    chunk[offset]
                    | (chunk[offset + 1] << 8)
                )
                offset += 2
                length_mask = 0x0FFF
                displacement_shift = 12
                position = len(output) - 1
                while position >= 0x10:
                    length_mask >>= 1
                    displacement_shift -= 1
                    position >>= 1
                length = (token & length_mask) + 3
                displacement = (token >> displacement_shift) + 1
                if displacement > len(output):
                    raise ValueError("LZNT1: invalid... again.. for some reason "
                        f"(0x{displacement:x})")
                for _ in range(length):
                    output.append(output[-displacement])
            else:
                output.append(chunk[offset])
                offset += 1
    return bytes(output)


def lznt1_decompress(data: bytes) -> bytes:

    output = bytearray()
    offset = 0
    while offset < len(data):
        if offset + 2 > len(data):
            raise ValueError("LZNT1: header invalid")
        header = (data[offset]|(data[offset + 1] << 8))
        offset += 2
        if header == 0:
            break
        signature = (header >> 12) & 0x7
        if signature != 3:
            raise ValueError("LZNT1: invalid signature: "
                f"0x{header:04x}")
        chunk_size = (header & 0x0FFF) + 1
        if offset + chunk_size > len(data):
            raise ValueError("LZNT1: strange len")
        chunk = data[offset:offset + chunk_size]
        offset += chunk_size
        if header & 0x8000:
            output.extend(lznt1_decompress_chunk(chunk))
        else:
            output.extend(chunk)

    return bytes(output)


class lets_unpack_this_shit(Transform):

    __doc__ = (
        "Eternidade Stealer Unpacker. "
        "Decrypts the payload using the custom "
        "stateful XOR algorithm and then decompresses "
        "the resulting LZNT1 stream"
    )

    category = "Custom Malware Decryptors"
    name = "Eternidade Stealer  Decryptor"

    def run(
        self,
        data: bytes,
        initial_key_I: int = 3333,
        initial_key_II: int = 3434,
        state: int = 1000,
        test_pe_file: bool = True
    ):
        decrypted = eternidade_decrypt(data,initial_key_I, initial_key_II, state)
        unpacked = lznt1_decompress(decrypted)
        if test_pe_file:
            if len(unpacked) < 2:
                raise ValueError("Output is too small to be a PE")
            if unpacked[:2] != b"MZ":
                raise ValueError("Decompression completed, but "
                    "the output does not start with MZ.. you can cry my friend :')")
        return unpacked
