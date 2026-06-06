### "Multi-generational CRC1 and CRC2 (sum balancer) calculator"
import argparse
import sys

def main():
    # Setup the parser
    parser = argparse.ArgumentParser(description="Calculate CRC1 and CRC2 (additive checksums) from an EEPROM dump.")

    # Define the positional argument (no dashes means it's required in order)
    parser.add_argument("input_file", help="Path to the .bin file to be processed")

    # Parse the arguments from sys.argv
    args = parser.parse_args()

    # Read the file
    try:
        with open(args.input_file, 'rb') as f:
            dump = f.read()
    except FileNotFoundError as e:
        print(f"Error: {args.input_file}: {e}")
        sys.exit(1)

    try:   
        # --- BLOCK 2 (CON#) Logic ---
        start_2 = 0x200
        len_2 = dump[start_2 + 0x04]
        mode_2 = dump[start_2 + 0x06]
        
        # Universal CON# Constant Logic
        const_2 = (0xFD - mode_2) & 0xFF
        b207 = (const_2 - len_2) & 0xFF
        
        sum_2 = sum(dump[start_2:start_2+len_2]) - dump[start_2+7] - dump[start_2+8]
        b208 = (0x100 - ((sum_2 + b207) % 0x100)) & 0xFF

        # --- BLOCK 0 (SER#) Logic ---
        start_0 = 0x00
        len_0 = 128 # Identity blocks are usually fixed 128
        mode_0 = dump[start_0 + 0x06]
        
        if mode_0 <= 0x01: 
            # CLASSIC MODE (T20-T40 era)
            # 0x07 is D2 for ALL dumps I have found
            b007 = 0xD2 
        else:
            # EXP 2010s MODE (L540 era)
            # Based on the L540 find: Constant 0xE7
            b007 = (0xE7 - dump[start_0 + 0x04]) & 0xFF
        
        sum_0 = sum(dump[start_0:start_0+len_0]) - dump[start_0+7] - dump[start_0+8]
        b008 = (0x100 - ((sum_0 + b007) % 0x100)) & 0xFF

        print(f"--- CRC1 and CRC2 (additive checksum) Calculator ---")
        print(f"SER# (0x07-0x08):   {b007:X} {b008:X}")
        print(f"CON# (0x207-0x208): {b207:X} {b208:X}")
        print(f"Block 0 (SER#) sum: 0x{(sum(dump[start_0:start_0+len_0])):X}")
        print(f"Block 2 (CON#) sum: 0x{(sum(dump[start_2:start_2+128])):X}")

        return (b207, b208), (b007, b008)
    except IndexError as e:
        print(f"Error: {e} \nThis is either not a proper 1024-byte EEPROM dump, or it is the wrong file.")

if __name__ == "__main__":
    main()

# Results quick reference:

# (~2013 Lenovo - newer gen than rest) from internet
# "L540.BIN"                  - this matches actual data at 0x207-0x208
# "L540_CRCs_removed.BIN"     #same as above, with CRCs removed      - CRCs match

#ALL same generation (IBM)
# "0x54-0x57COPY.bin"        #MUDGE21 SVP original         - this matches actual data at 0x207-0x208
# "0x54-0x57COPYnoCRC.bin"  # same as above, CRCs removed
# "0x54-0x57heyalex.bin"     #HEYALEX SVP new              - this matches actual data at 0x207-0x208
# "0x54-0x57heyalexNOcrc.bin"  # same as above, CRCs removed
# "0x54-0x57_4thtestCOPY.bin"  # 4THTEST SVP               - this matches actual data at 0x207-0x208
# "0x54-0x57_3rdtest_ONLYuseFOR_CRC_no_svp_blockCOPY.bin"    #CRC2 is 9B 30, it matches

# "R51.BIN"                  #from internet          - does not match data, I think this data is not correct
# "T61conBlockOnly.bin"      #from internet                - this matches actual data at 0x207-0x208
# "T61russia.BIN"            #from internet                - this matches actual data at 0x207-0x208
# "T400.BIN" #from internet  #from internet                - this matches actual data at 0x207-0x208
# "T22.BIN"                  #T22 from internet            - this matches actual data at 0x207-0x208