"""
Author: Ícaro César (0x0d4y)
Date: 2025-11-23
Description: Script to decrypt and decompress the loader of the Eternidade Stealer, developed by me and used in the WhatsWorm campaign analyzed by Heimdall Security Research from ISH Tecnologia.
Research: https://ish.com.br/wp-content/uploads/2025/11/Analise-da-Campanha-do-WhatsWorm-levando-a-implementacao-do-Eternidade-Stealer-1.pdf

"""

import os
import ctypes
import struct

def loader_eternidade_decryptor(data):
    
    key_I = 3333
    key_II = 3434
    state = 1000
    
    decrypted = bytearray()
    
    for byte in data:
        p = byte ^ ((state >> 8) & 0xFF)
        decrypted.append(p)
        state = (((p + state) & 0xFF) * key_I + key_II) & 0xFFFF
        
    return decrypted

def decompress(data):
    compression_format = 2
    
    uncompressed_size = len(data) * 20
    uncompressed_buffer = ctypes.create_string_buffer(uncompressed_size)
    final_size = ctypes.c_ulong(0)
    
    ntdll = ctypes.windll.ntdll
    status = ntdll.RtlDecompressBuffer(
        compression_format,
        uncompressed_buffer,
        uncompressed_size,
        ctypes.c_char_p(bytes(data)),
        len(data),
        ctypes.byref(final_size)
    )
    
    if status != 0:
        print(f"[!] Decompression was Failed: {hex(status)} [!]")
        return None
        
    return uncompressed_buffer.raw[:final_size.value]

def process_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        decrypted = loader_eternidade_decryptor(data)
        if not decrypted:
            print("[!] Decompression was Failed: ")
            return

        decompressed = decompress(decrypted)
        if decompressed:
            out_path = filepath + ".decrypted.bin"
            with open(out_path, 'wb') as f:
                f.write(decompressed)
            
            if len(decompressed) > 2 and decompressed[:2] == b'MZ':
                print("\t[+] The sample was Successfully Decrypted. The MZ Header was detected [+]")
            else:
                print("[-] The decrypted sample do not contains a MZ Header [-]")
                print(f"\t[-] First 16 bytes: {decompressed[:16].hex()}")
        else:
            print("[-] Decompression was Failed [-]")
            
    except Exception as e:
        print(f"[-] Error processing the file {filepath}: {e}")

if __name__ == "__main__":
    target_dir = r"<dir_with_encrypted_samples>"
    print("\n\t================= Heimdal Security Research Decryption and Decompression Tool =================\n\n")
    if os.path.exists(target_dir):
        for filename in os.listdir(target_dir):
            if filename.endswith(".tda") or filename.endswith(".dmp"):
                process_file(os.path.join(target_dir, filename))
                print("[+] Sample {} was Decrypted and Decompressed [+]\n".format(filename))
    else:
        print(f"[-] Directory was no found: {target_dir}")
