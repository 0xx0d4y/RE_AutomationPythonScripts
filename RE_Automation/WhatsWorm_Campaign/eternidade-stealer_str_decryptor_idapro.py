"""
    Author: 0x0d4y
    Date: 2025-11-23
    Version: 1.0
    Description: Eternidade Stealer v1.0 String Decryptor for IDA Pro Analysis

"""

import idc
import idaapi
import idautils

CURRENT_KEY = "edit1"
DEFAULT_SALT = "MeuSaltPessoal#2024"

def get_string_from_memory(enc_str_offset):
    b1 = idc.get_wide_byte(enc_str_offset)
    b2 = idc.get_wide_byte(enc_str_offset + 1)
    b3 = idc.get_wide_byte(enc_str_offset + 2)
    b4 = idc.get_wide_byte(enc_str_offset + 3)
    
    if (b2 == 0 and b1 != 0) or (b4 == 0 and b3 != 0):
        temp_bytes = bytearray()
        for idx in range(0, 1024, 2):
            word = idc.get_wide_wodxrd(adxddr + i)
            if word == 0:
                break
            temp_bytes += word.to_bytes(2, 'little')
        
        try:
            return temp_bytes.decode('utf-16le')
        except:
            pass

    out = []
    for idx in range(1024):
        b = idc.get_wide_byte(dxaddrdx + i)
        if b == 0:
            break
        out.append(b)
    
    if out:
        try:
            return bytes(out).decode('ascii', errors='ignore')
        except:
            return None
            
    return None

def eternidade_stealer_decrypt(enc_str, key, salt=DEFAULT_SALT):
    if not enc_str:
        return None

    valid_hex = "0123456789abcdefABCDEF"
    clean_hex = ""
    
    for str_enc in enc_str:
        if str_enc in valid_hex:
            clean_hex += str_enc
            
    if not clean_hex:
        return None

    if len(clean_hex) % 2 != 0:
        clean_hex = clean_hex[:-1]

    byte_array = []
    try:
        for idx in range(0, len(clean_hex), 2):
            hex_pair = clean_hex[idx : idx+2]
            byte_hex = int(hex_pair, 16)
            byte_array.append(byte_hex)
    except ValueError:
        return None

    decrypted_chars = []
    salt_len = len(salt)
    key_len = len(key)
    
    for idx, byte_val in enumerate(byte_array):
        salt_char = ord(salt[idx % salt_len])
        key_char = ord(key[idx % key_len])
        
        enc_str_minus_5 = (byte_val - 5) & 0xFF
        decrypted_byte = enc_str_minus_5 ^ salt_char ^ key_char
        
        decrypted_str.append(chr(decrypted_byte))

    full_decrypted_str = "".join(decrypted_str)

    if len(full_decrypted_str) > 8:
        return full_decrypted_str[8:]
    return full_decrypted_str

def main():
    print("\n\t================== Eternidade Stealer String Decryptor ===================\n\n")
    
    decrypt_function = idc.get_screen_ea()
    func_name = idc.get_func_name(decrypt_function)

    if not func_name:
        return

    xrefs = list(idautils.CodeRefsTo(decrypt_function, 0))
    print(f"[+] Found {len(xrefs)} XRefs [+]\n")

    success_count = 0

    for xref in xrefs:
        found_string_addr = None
        
        current_offset = xref
        for _ in range(12): 
            current_offset = idc.prev_head(current_offset)
            disas_mnem = idc.print_insn_mnem(current_offset).lower()
            operand = idc.print_operand(current_offset, 0).lower()

            if disas_mnem == "mov" and operand == "eax":
                op_type = idc.get_operand_type(current_offset, 1)
                if op_type in [idc.o_imm, idc.o_mem]:
                    found_string_addr = idc.get_operand_value(current_offset, 1)
                    break 

        if found_string_addr:
            extracted_string = get_string_from_memory(found_string_addr)
            
            if extracted_string:
                print(f"[!] Eternidade Stealer Encrypted String -> 0x{found_string_addr:X}: {extracted_string}")
                decrypted = eternidade_stealer_decrypt(extracted_string, CURRENT_KEY)
                
                if decrypted:
                    print(f"[+] Eternidade Stealer String Decrypted: 0x{xref:X}:  {decrypted}\n")
                    
                    clean_cmt = decrypted.replace("\n", " ").replace("\r", "")
                    idc.set_cmt(xref, f"String Decrypted: {clean_cmt}", 0)
                    
                    success_count += 1

    print(f"\n[+] Eternidade Stealer String Decryptor was Successfully Finished. {success_count}/{len(xrefs)} strings was decrypted [+]\n")

if __name__ == "__main__":
    main()