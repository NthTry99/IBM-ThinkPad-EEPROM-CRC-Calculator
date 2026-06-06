import argparse
import sys

def main():
    # Setup the parser
    parser = argparse.ArgumentParser(description="Calculate SVP checksum from an EEPROM dump.")
    
    # Define the positional argument (no dashes means it's required in order)
    parser.add_argument("input_file", help="Path to the .bin file to be processed")

    # Parse the arguments from sys.argv
    args = parser.parse_args()

    # Read the file
    try:
        with open(args.input_file, 'rb') as f:
            data = f.read()
            # Get the 7 SVP bytes from 0x338-0x33E
            svp_bytes = data[0x338:0x33F]
            if len(svp_bytes) == 0:
                raise ValueError("No SVP data")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {args.input_file}: {e}")
        sys.exit(1)

    # Pass the SVP bytes to the checksum calculator
    svp_checksum = calculate_svp_checksum(svp_bytes)

    # Display the SVP data and SVP checksum
    print(f"SVP data from {args.input_file}:\n{svp_bytes.hex(' ')}")
    print(f"Calculated SVP checksum: {svp_checksum:X}")
    print(f"Actual SVP checksum at 0x33F: {data[0x33F]:X}")
    print(f"Actual SVP checksum at 0x347: {data[0x347]:X}")

    if svp_checksum == data[0x33F] == data[0x347]:
        print("Calculated SVP checksum matches the checksums in the data.")
    else:
        print("Calculated SVP checksum does NOT match one or both checksums in the data. This data may cause Error 0177: Bad SVP data.")

def calculate_svp_checksum(svp_bytes):
    """ Returns int. The CheckSum8 (Modulo 256; it is only 1 byte) of a given bytearray """
    svp_checksum = sum(svp_bytes) % 256
    return svp_checksum


if __name__ == "__main__":
    main()