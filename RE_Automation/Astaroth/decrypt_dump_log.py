import argparse
import base64
from pathlib import Path


PAIR_BIAS = 0x3F2
DEFAULT_INPUT = Path(__file__).with_name("dump.log")


def decode_envelope(data: bytes) -> str:
    compact_data = b"".join(data.split())
    pair_text = base64.b64decode(compact_data, validate=True).decode("ascii")

    if not pair_text:
        raise ValueError("\n[1] the decoded envelope is empty")
    if (len(pair_text) - 1) % 2 != 0:
        raise ValueError("[!] the salted pair stream has an invalid length")

    salt = ord(pair_text[0]) - ord("A")
    plaintext = []

    for offset in range(1, len(pair_text), 2):
        high = ord(pair_text[offset]) - ord("A")
        low = ord(pair_text[offset + 1]) - ord("A")
        value = high * 25 + low - salt - PAIR_BIAS
        plaintext.append(chr(value))

    return "".join(plaintext)


def decode_configuration(envelope: str) -> list[tuple[str, str]]:
    configuration = []

    for line_number, line in enumerate(envelope.splitlines(), start=1):
        if not line:
            continue
        if "=" not in line:
            raise ValueError(f"[!] line {line_number} is not a key=value record")

        key, encoded_value = line.split("=", 1)
        value = base64.b64decode(encoded_value, validate=True).decode("utf-8")
        configuration.append((key, value))

    return configuration


def main() -> None:
    parser = argparse.ArgumentParser(
        description="[+] Decrypt an Astaroth dump.log configuration file [+]"
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT,
        help="[!] path to the C&C config file (the default is the dump.log in current directory)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="[!] write the decrypted key=value records to this file",
    )
    args = parser.parse_args()

    try:
        envelope = decode_envelope(args.input.read_bytes())
        configuration = decode_configuration(envelope)
    except (OSError, ValueError, UnicodeError) as error:
        parser.error(str(error))

    result = "\n".join(f"{key}={value}" for key, value in configuration) + "\n"

    if args.output:
        args.output.write_text(result, encoding="utf-8")
        print(f"[+] Wrote {len(configuration)} fields to {args.output}")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
