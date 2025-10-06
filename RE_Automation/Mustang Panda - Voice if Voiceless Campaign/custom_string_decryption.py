def decrypt_string(enc: bytes, keybase: bytes) -> bytes:

    key = bytes([keybase[0], keybase[4], keybase[8], keybase[12]])
    out = bytearray()
    for i, b in enumerate(enc):
        out.append(b ^ key[i & 3])
    return bytes(out)

if __name__ == "__main__":
    enc = b"rakp`qhw!-E$.Aqa`vf$.VM$#CgkcgF|qgqmdl`aLcmefgq&!-PG!ojjtvf$.OL$3\",PS\"!G;^SvneqelFbp`^B`n`fHhafjrkmcQnvchl_SG]B`n`f[mk`aoqjjf]kamrfv/g{a!Njgdlpmoe!"
    keybase = bytes([0x01,0x00,0x00,0x00,
                     0x02,0x00,0x00,0x00,
                     0x03,0x00,0x00,0x00,
                     0x04])
    dec = decrypt_string(enc, keybase)
    print("---------- Encrypted String ----------")
    print(enc)
    print("---------- Decrypted String ----------")
    print(dec.decode("latin-1"))
