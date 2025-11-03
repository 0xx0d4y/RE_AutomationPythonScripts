import idc
import idaapi
import idautils

ALPHABET = "pB1Q5ZyneCb6sR03u2OxfK8vVMkEaow_ciSDYIUmlF4hq9XLPJNzTHGgr.WtdA7"

def decrypt_scoringmathtea_string(encrypted: str) -> str:
    if isinstance(encrypted, bytes):
        try:
            encrypted = encrypted.decode('ascii')
        except UnicodeDecodeError:
            return "[-] Error [-]"

    key_state = 11
    decrypted_string = []

    for dec_str in encrypted:
        try:
            idx = ALPHABET.index(dec_str)
        except ValueError:
            decrypted_string.append(dec_str)
            continue

        dec_char = ALPHABET[(idx - key_state) & 0x3F]
        decrypted_string.append(dec_char)
        key_state = (key_state + ord(dec_char)) & 0x3F

    return "".join(decrypted_string)

def main():
    print("==== ScoringMathTea's String Obfuscator IDA Script ====")

    decrypt_function = idc.get_screen_ea()
    if decrypt_function == idaapi.BADADDR:
        print("[!] Error: Please place the cursor on the decryption function [!]")
        return

    decrypt_function_name = idc.get_func_name(decrypt_function)
    if not decrypt_function_name:
        print(f"[!] Error: The address 0x{decrypt_function:X} does not belong to a function.")
        return
    xrefs = list(idautils.CodeRefsTo(decrypt_function, 0))
    if not xrefs:
        print(f"[!] No XRefs to calls to the function {decrypt_function_name} were found.")
        return
    print(f"[+] Found {len(xrefs)} XRefs [+]")

    for xref in xrefs:
        encrypted_string = None

        current_offset = xref
        for _ in range(15):
            current_offset = idc.prev_head(current_offset)
            
            if idc.print_insn_mnem(current_offset) == "lea" and idc.print_operand(current_offset, 0) == "rdx":
                str_addr = idc.get_operand_value(current_offset, 1)
                
                str_bytes = idc.get_strlit_contents(str_addr)
                if str_bytes:
                    encrypted_string = str_bytes
                    break 

        if encrypted_string:
            decrypted_string = decrypt_scoringmathtea_string(encrypted_string)
            print(f"  -> At 0x{xref:X}: '{encrypted_string.decode('ascii', 'ignore')}' -> '{decrypted_string}'")

            comment = f"Decrypted String: {decrypted_string}"
            idc.set_cmt(xref, comment, 0) 

        else:
            print(f"  [-] Failed to find the encrypted string for the call at 0x{xref:X}\n")

    print(f"\n[+] ScoringMathTea's Obsfuscator was Successfully Executed [+]\n")

if __name__ == "__main__":
    main()