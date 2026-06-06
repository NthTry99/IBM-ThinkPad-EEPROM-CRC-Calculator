# Originally when I thought the CRC1 and CRC2 were calculated by a polynomial.
# This finds the range of the data (if possible) used to calculate the given CRC with a given seed.
# Used when I was experimenting with the possibility that CRC2 used data from CRC1 as a seed.

def calculate_ibm_crc(data, seed):
    crc = seed
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc

def find_range_with_fixed_seed(hex_string, seeds, target_crc):
    block_data = bytes.fromhex(hex_string)
    
    # Try both standard and Final XOR 0xFFFF
    for final_xor in [0xFFFF, 0xFFFF]: # one of these was originally 0x0000
        for seed in seeds:
            print(f"Testing Seed: {hex(seed)} | Final XOR: {hex(final_xor)}...")
            
            for start in range(len(block_data)):
                for end in range(start + 1, len(block_data) + 1):
                    # Create the slice
                    test_range = bytearray(block_data[start:end])
                    
                    # Correctly zero out the CRC hole (at absolute offset 0x07-0x08)
                    # only if those offsets are within our current 'test_range'
                    for crc_offset in [7, 8]:
                        if start <= crc_offset < end:
                            test_range[crc_offset - start] = 0
                    
                    # Calculate and compare
                    res = calculate_ibm_crc(test_range, seed) ^ final_xor
                    if res == target_crc:
                        print(f"--- MATCH FOUND! ---")
                        print(f"Start Offset: {hex(start)}")
                        print(f"End Offset:   {hex(end)}")
                        print(f"Seed Used:    {hex(seed)}")
                        print(f"Final XOR:    {hex(final_xor)}")
                        print(f"Data Length:  {len(test_range)} bytes")
                        return # Stop at first match

# YOUR DATA
# Pass in the 128 bytes starting at 0x200 (CON#)
# this is orig
con_data_hex = "43 4F 4E 23 58 00 02 A3 24 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 05 00 00 00 FF 00"
target = 0xA324
seeds_to_test = [0x7A01, 0x017A]

# Target is the original CRC2 from that block
# this is CRC2 for alex 
# con_data_hex = "43 4F 4E 23 60 00 02 9B 36 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00"
# target = 0x9B36 
# seeds_to_test = [0x1DB2, 0xB21D]

#this is crc1 (SER#) 
# con_data_hex = "53 45 52 23 14 0C 01 D2 E1 00 00 00 00 00 00 00 40 31 33 52 31 31 32 33 5A 4A 31 55 52 59 34 33 50 31 52 47 20 B1 53 32 33 37 33 37 32 55 39 39 35 5A 47 4E 36 00 00 00 08 33 38 4C 35 30 30 31"




#this is for SER# target = 0xD2E1

# Try seed in both Endianness
# seeds_to_test = [0xD2E1, 0xE1D2]
# seeds_to_test = [0x9B36, 0x369B]



find_range_with_fixed_seed(con_data_hex, seeds_to_test, target)


# GIVES: 
# --- MATCH FOUND! ---
# Start Offset: 0x0
# End Offset:   0x40
# Seed Used:    0x7a01
# Final XOR:    0xffff
# Data Length:  64 bytes