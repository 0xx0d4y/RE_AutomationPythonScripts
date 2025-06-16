import pyshark
import arc4
import binascii
from colorama import Fore, Style, init


pcap = input(f"\n{Fore.MAGENTA}Enter the Amadey Packet Capture File{Style.RESET_ALL}: ")
key = input(f"{Fore.MAGENTA}Enter the Decryption Key{Style.RESET_ALL} [{Fore.YELLOW}You can find it in the strings{Style.RESET_ALL}]: ")
key_unhex = key.encode()

init_pcap = pyshark.FileCapture(pcap, display_filter='http.request.method == "POST"')

def extract_encrypted_data(packet_captured):

    if hasattr(packet_captured, 'file_data'):
        data = packet_captured.file_data.binary_value
        raw_packet = data.decode(errors='ignore')
    else:
        raw_packet = packet_captured.get_field_value('request_line') or ''
    for rpacket in raw_packet.split('&'):
        if rpacket.startswith('r='):
            return rpacket.split('=',1)[1]
    return None

for net_capture in init_pcap:
    try:
        packet = net_capture.http
    except AttributeError:
        continue

    encrypted_data = extract_encrypted_data(packet)
    if not encrypted_data:
        continue

    print(f"\n{Fore.GREEN}==================== AMADEY HTTP POST PACKET FOUND ===================={Style.RESET_ALL}")
    try:
        # --- IP Layer ---
        print(f"{Fore.WHITE}Layer IP:{Style.RESET_ALL}")
        print(f"        Source Address: {Fore.YELLOW}{net_capture.ip.src}{Style.RESET_ALL}")
        print(f"        Destination Address: {Fore.YELLOW}{net_capture.ip.dst}{Style.RESET_ALL}")

        # --- TCP Layer ---
        print(f"{Fore.WHITE}\nLayer TCP:{Style.RESET_ALL}")
        print(f"        Destination Port: {Fore.YELLOW}{net_capture.tcp.dstport}{Style.RESET_ALL}")

        # --- HTTP Layer ---
        print(f"{Fore.WHITE}\nLayer HTTP:{Style.RESET_ALL}")
        # getattr é usado para segurança, caso um campo não exista
        request_line = getattr(net_capture.http, 'request_line', 'N/A').strip()
        print(f"        {request_line}")
        print(f"        Request Method: {Fore.YELLOW}{getattr(net_capture.http, 'request_method', 'N/A')}{Style.RESET_ALL}")
        print(f"        Request URI: {Fore.YELLOW}{getattr(net_capture.http, 'request_uri', 'N/A')}{Style.RESET_ALL}")
        print(f"        Full request URI: {Fore.YELLOW}{getattr(net_capture.http, 'request_full_uri', 'N/A')}{Style.RESET_ALL}")
        print(f"        File Data: {Fore.YELLOW}{len(encrypted_data)} bytes{Style.RESET_ALL}")
        print(f"{Fore.WHITE}\nLayer URLENCODED-FORM:{Style.RESET_ALL}")
        print(f'        Form item: "r" = "{Fore.RED}{encrypted_data}{Style.RESET_ALL}"')

    except AttributeError as e:
        print(f"{Fore.RED}[!] Could not extract all details from packet {net_capture.number}: {e}{Style.RESET_ALL}")


    print(f"\n{Fore.YELLOW}[+] Encrypted Data Founded{Style.RESET_ALL} = {Fore.RED}{encrypted_data}{Style.RESET_ALL} {Fore.BLUE}(Lenght{len(encrypted_data)}){Style.RESET_ALL}")
    amadey_encrypted_data = binascii.unhexlify(encrypted_data)

    rc4_key = arc4.ARC4(key_unhex)
    decrypted = rc4_key.decrypt(amadey_encrypted_data)

    try:
        decrypted_data = decrypted.decode('ascii', errors='replace')
        print(f"\n{Fore.GREEN}[+] Amadey POST Data Decrypted:{Style.RESET_ALL} {Fore.BLUE}{decrypted_data}{Style.RESET_ALL}\n")
    except None:
        None

init_pcap.close()