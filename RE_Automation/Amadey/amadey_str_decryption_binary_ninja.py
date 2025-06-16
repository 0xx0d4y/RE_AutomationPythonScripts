import base64
import binaryninja

'''

    Title: Binary Ninja Amadey's String Decryptor
    Author: 0x0d4y

'''

def amadey_custom_str_decryption(encrypted_string: str, decryption_key: str) -> bytes:
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
    expanded_key = ''.join(decryption_key[i % len(decryption_key)] for i in range(len(encrypted_string)))
    translated_chars = [
        char if char not in alphabet else
        alphabet[(alphabet.index(char) - alphabet.index(key_char)) % len(alphabet)]
        for char, key_char in zip(encrypted_string, expanded_key)
    ]
    try:
        decrypted_base64 = ''.join(translated_chars)
        return base64.b64decode(decrypted_base64)
    except Exception:
        return None

if __name__ == "__main__":
    key = "4a2b1d794e79a4532b6e2b679408d2bb" # <- Put your key here
    function = 0x422b80                      # <- Put the address of the caller function here
    xrefs = bv.get_code_refs(function)
    for refs in xrefs:
        arg = refs.mlil.params[1]
        if not isinstance(arg, binaryninja.mediumlevelil.MediumLevelILConstPtr):
            continue
        s = arg.string
        if s is None:
            continue 
        encrypted_string = s[0]

        decrypted_string = amadey_custom_str_decryption(encrypted_string, key)
        if decrypted_string:
            print(f"Amadey's Encrypted String: {encrypted_string}")
            print(f"Amadey's Decrypted String: {decrypted_string}")
            comment = f"Decrypted String -> {decrypted_string}"
            bv.set_comment_at(refs.address, comment)