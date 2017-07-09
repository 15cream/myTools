__author__ = 'allblues020201'
import argparse
# Used for address transformation in Shellcode


def trans(address, width, endian):

    addr_out = []
    addr_in = address.upper().split('X')[-1]
    addr_bytes = [addr_in[i:i+2] for i in range(0, len(addr_in), 2)]
    hidden_byte = int(width) / 8 - len(addr_bytes)
    for c in range(hidden_byte):
        addr_bytes.insert(0, "00")
    if endian == 'l':
        addr_bytes = reversed(addr_bytes)
    for byte in addr_bytes:
        addr_out.append('\\x' + byte)
    return "".join(addr_out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", choices=['32', '64'], help="64 for 64-bit; 32 for 32-bit")
    parser.add_argument("-e", choices=['l', 'b'], help="l for little endian; b for big endian")
    parser.add_argument("address", help="the address you want to be transfered")
    args = parser.parse_args()
    print trans(args.address, args.w, args.e)


