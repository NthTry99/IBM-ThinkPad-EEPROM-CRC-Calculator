# this is from when i thought the CRC1 and CRC2 was made by using a seed and a polynomial.
# ### this is for brute force finding seed CRC2 (0x200 to 0x240 which is 64 bytes)
from pathlib import Path

def crc16_custom(data, seed, reflect_in=False, reflect_out=True, final_xor=0xFFFF):
    crc = seed
    for byte in data:
        if reflect_in:
            byte = int('{:08b}'.format(byte)[::-1], 2)
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    if reflect_out:
        # crc = int('{:016b}'.format(crc)[::-1], 2)    # little endian reflector, don't use i dont think
        return crc ^ final_xor    
    # return crc


def verify_con_variations(dump_path):
    script_dir = Path(__file__).parent

    dump = Path(dump_path).read_bytes()
    #TEMP TEST uncomment block below this when done
    data_range = dump[0x200:0x240]    

    # asdf = "43 4F 4E 23 58 00 02 00 00 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 05 00 00 00 FF 00"
    # # print(len(asdf))
    # data_range = bytes.fromhex(asdf)

    # app_id = Path(script_dir / "0x5cCOPY.bin").read_bytes()
    # pwd_scancodes = dump[0x338:0x33F]
    
    # Range of data to calculate CRC from
    # This is for CRC2
    # data_range = dump[0x200:0x22E]
    # # Actual checksum in code
    # target_crc = (dump[0x22E] << 8) | dump[0x22F]
    # target_crc = 0x0340



    # Actual checksum in code
    # target_crc = (dump[0x07] << 8) | dump[0x08]
    #this is alex
    target_crc = 0x9B36

    # this is orig
    # target_crc = 0xA324





    ### This is for CRC1
    # data_range = dump[0x00:0x2E]
    # # Actual checksum in code
    # target_crc = (dump[0x2E] << 8) | dump[0x2F]






    # Unmask (SVP XOR and APP/ID salt) --- for CRC1 gives seed 0x21D7
    # unmasked = bytes([b ^ pwd_scancodes[i % 7] ^ app_id[i % 32] for i, b in enumerate(data_range)])

    # Unmask (APP/ID salt ONLY) --- for CRC1 gives seed 0x5D9A
    # unmasked = bytes([b ^ app_id[i % 32] for i, b in enumerate(data_range)])

    # Unmask (SVP Only)
    # unmasked = bytes([b ^ pwd_scancodes[i % 7] for i, b in enumerate(data_range)])

    #no unmasking --- for CRC1 gives seed 0xB00C --i think this one is more reliable,
    #             --- for CRC2 gives seed 0xF904 (using wrong offsets)
    unmasked = data_range


    print("No match found. Attempting to reverse-engineer the seed from 0x2E...")
    # Brute force the seed specifically for THIS block's data and stored result
    for s in range(0x10000):
        if crc16_custom(unmasked, s) == target_crc:
            print(f"[SUCCESS] Custom Seed for Block 2 found: 0x{s:04X} \nThis makes {hex(target_crc)}")
            return

verify_con_variations("zzzLASTalex.bin")
# verify_con_variations("0x54-0x57COPY.bin")
# verify_con_variations("zzzLASTalex.bin")

##TO GET 0x3939 at 0x2E:
# Unmask (SVP Only)
    #seed = 0xCC41

# Unmask using NO XOR or salt:
    #seed = 0xB00C

# Unmask (SVP XOR and APP/ID salt)
    #seed = 0x21D7


