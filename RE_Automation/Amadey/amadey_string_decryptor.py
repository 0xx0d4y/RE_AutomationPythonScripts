import base64
from colorama import Fore, Style, init

'''

    Title: Python Amadey's String Decryptor 
    Author: 0x0d4y

'''

init(autoreset=True) 

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
    amadey_encrypted_str_list = ['FT82BmAZGm01MbYXEh==', 'E3ImDJcw5rRxLVfmQHQ8Cowkat==', 'GSVADD==', 'NyRm2KQr', 'CSSt4T==', 'ESMt4T==', 'SDPyCJJkFDMwZJ==', '6mwuP0ksS1dj', 'N00HLI zNoRaTPfb4n4D33UWVy3medSw73EdG6Rw6qRsdyTd4oIt3309SgKrWT6kSQ==', 'N00HLI zNoRaTPfb4n4D33UWVy3medSw73EdG6Rw6qRsdyTd4oIt3309PQ7tex zSXAdL0Jj6mxRazPk3DwK33sgXQyw', 'N3Ii3qNZ6E==', 'NmMu', 'R2SlyF5BBJFLRxfKzD4DC4zc', 'N00HLI zNoRaTPfb4n4D33UWVy3medSw73EdG6Rw6qRsdyTd4oIt3309SgKr', '6nMvPJtqFDEe', 'NHAwP6Ff51I=', 'N00HLI zNoRaTPfb4n4D33UWVy3medSw73EdG6Rw6qRsdyTd4oIt3309PQ7tex zSXAdK5dj5KseRf3kQHQC4x==', 'CVMUHYFONo5ESNrxAR==', 'QEwx3D==', 'NE0ULD==', 'K0MV', '4WH7', '7nD7', '62H7', '53D7', 'Rmb7', 'RXz7', '6GD7', '7WV7', 'SGR7', 'RXP7', '5HP7', '5247', '6jR=', 'R3AmPF1i5Kt6YVrh4D0o3Hs4', 'R3AmPF1i5Ks=', 'R2oq3F1i5Ks=', 'SDv=', 'STv=', 'STz=', 'STD=', 'MWwq2j==', '4HI13GktEA==', '4HI13KI4EC4=', 'SX9m', 'SGot', 'R2Sl', '6HDy', '5XEq', '8mcx', 'E3w21ZRY', 'IGD+', 'IGH+', 'E1st4Z n5rIt', 'Dyjs', 'Bw==', '9A==', 'CnMv10M7', 'IQ==', '629m2JsxFm1ibzq=', '42Mz2pRqFDEsZzrk', 'K2M1JpBY41VjUWfr5HQxJX0i p==', 'NHAwP6Ff5YNfdzz5', 'JVQCK4MeN65kdA8 4nP=', 'JXQq3pA=', 'L2wA3JRw66p3Ixr Ph==', 'KVEGLD==', 'NGwvPJAeN6RhdQDh5If=', 'KG0k4J5wBJ jY ==', 'JVQI', 'FzPxLJ5YR0tRZPHT4ng46R==', 'Jmc1PJRkS01iZQC=', 'Mm0z4J5s', 'N20x1J5x', 'J20u25Nt', 'O2cvHJRkS01iZQC=', 'FDvzCCMZGn92OJ==', '6mz=', '72z=', 'J20v4JRs7GXSeQvdFjwx5XsW9QqefeRwSm0z2VXiR1NfOrva34QyQHAucMPqOJ1u', 'ESRuBVWr', 'wQgE251YS01YLNLh44wz43gW9PYrR Cn53AuBZNf7KA5IzZ 3XPcznMdbztfRpCn4Wom2pBrSXWg', 'BgRLG55s7KRsdvVM6YwpFjwdaAqpdNOi7Gcw2l5tR7NjdvVr5IEpPXVJA PH', 'wQfuBVWrEWW=', 'ESROsj==', 'I3Ek3mWv', 'EmgxPz==', 'J20v4JRs7GXSeQvdFjwl4Iwo9PCegxmw5i05B0 17CXkbWDlCYQC3HQqWVYh2NR=', 'N1cULHRLQIJZcgDd3oMH330WafYpXTW1QEEw2qNw56taQV3l4IQ4QYEKWPQi0vOw5Xs24JRwMqBrZJ==', 'J20u3KRYS1FMYPVd', 'RWAkPJRkS6dnafnk3X0z4IAuaWGYgee58XfxCWExGHQ0NsaXCW3=', 'EXMv1ZJtSKQr', 'N1cULHRLQIJZcgDd3oMH330WafYpXTW1QEEw2qNw56taVPZh5HQoMnggXPY TR POFAQJItULYNDTUq=', 'N1cULHRLQIJtbgLq33sXQYLsKwu XTWz7mckP0JaJqBxaPHw2YIA3HA1VyOm2xWw', 'OmclPZ5HKE==', 'QDrxCGw=', 'KGMnO0Rq7JJjdALh3n9DCmcOXQCseyW14W0v', 'KGMnO0Rq7JJjdALh3n9DCmgOXQCseyW14W0v', 'N00HLI zNoRaTPfb4n4D33UWVy3medSw73DhJoNaJ7RwcfPm5GUp4oIl VT=', 'NHAwPKRh7I1fbPO=', 'FjryET==', 'FjrzCj==', 'FjryDj==', 'FjrzDT==', 'J3Mz3pRs7IFZaPrc', 'QA==', 'Hjf7', '6nMvPJtqFDEsZQbd', 'E2jh', 'BnIi35pp40tqIv3ezD4t3Tve', 'BirnzlxY40XjbWPSzEzkAjTcXzKpLr==', 'CiPhH0dn7GE=', 'BirnzlxwS00e', 'BCPnyD==', 'NG04P0Fx4KRqbvZd6HP=', 'EWM5PZJZ7Khtbgvn3Hgn6TwuXPQsgxWA4W5vPZMeEYVnbzO9zh==', 'Bg==', '62924JNt760eLQG9CYLkDB==', '63H 3z==', '6mwvPJ5r', 'L2M6Op5f6qMeTzzX34Q4OGwuXPms1NR=', 'FDrxCGwYFXg=', 'FDrxCGwYFnE=', 'FDrxCGwYFnI=', 'FDrxCGwYF6U=']

    key = "4a2b1d794e79a4532b6e2b679408d2bb" # <- Put your key here

    for encrypted_str in amadey_encrypted_str_list:
        try:
            decrypted_bytes = amadey_custom_str_decryption(encrypted_str, key)
            decrypted_str = decrypted_bytes.decode('utf-8', errors='replace')
            print(
                f"{Fore.YELLOW}Amadey String Decrypted{Style.RESET_ALL}: "
                f"{Fore.RED}{encrypted_str}{Style.RESET_ALL} -> {Fore.GREEN}{decrypted_str}{Style.RESET_ALL}"
            )
        except ValueError as err:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error in Decoding {encrypted_str}: {err}")
