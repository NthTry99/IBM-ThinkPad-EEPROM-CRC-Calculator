""" This is a massive bunch of attempts to decode the CRC and how it is generated.
The problem is the "CRCs" are not CRCs at all. There were many false positives.
These are attempts to make the polynomial work, across multiple test EEPROM dumps,
by testing combinations of different masks/salts based on the SVP, APP/ID page,
final XOR 0xFFFF or 0x0000 masks, etc. None of them worked, here are the attempts

This whole project was a bit of a longshot, as I have very little experience with
writing data validation programs or reverse engineering this sort of thing.
So yes I did vibe code some of it. But I am able to identify when it is
right and when it isn't, and how to steer the model in the right direction.
"""




# from pathlib import Path

# script_dir = Path(__file__).parent

# # output_file = script_dir /  "output.bin"
# filename = "dump.bin"

# test = bytearray(range(0x54, 0x58))
# # print(test)

# filename = script_dir / filename
# # print(filename)

# with open(filename, "wb") as f:
#     f.write(test)
# print(f"Backup saved to {filename}")





# TRY 1
# import sys

# def calculate_crc16_ccitt(data):
#     """CRC-16-CCITT with Poly 0x1021, Init 0xFFFF."""
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def check_dump(file_path):
#     try:
#         with open(file_path, 'rb') as f:
#             dump = f.read()
        
#         # Define typical T40 CRC block ranges
#         # Block 1: 0x00 to 0x2D (46 bytes)
#         data1 = dump[0x00:0x2E]
#         stored_crc1 = (dump[0x2E] << 8) | dump[0x2F]
#         calc_crc1 = calculate_crc16_ccitt(data1)
        
#         # Block 2: 0x30 to 0x7D (78 bytes)
#         data2 = dump[0x30:0x7E]
#         stored_crc2 = (dump[0x7E] << 8) | dump[0x7F]
#         calc_crc2 = calculate_crc16_ccitt(data2)

#         print(f"CRC1 (Offset 0x2E): Stored: {stored_crc1:04X}, Calculated: {calc_crc1:04X}")
#         print(f"CRC2 (Offset 0x7E): Stored: {stored_crc2:04X}, Calculated: {calc_crc2:04X}")
        
#         if calc_crc1 == stored_crc1 and calc_crc2 == stored_crc2:
#             print("\nSUCCESS: All CRCs match.")
#         else:
#             print("\nWARNING: CRC mismatch detected. The dump may be corrupt or modified.")

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python scratchpad.py your_dump.bin")
#     else:
#         check_dump(sys.argv[1])






# TRY 2
# import sys
# import struct

# def calculate_crc16(data):
#     """Standard CRC-16-CCITT (0x1021) calculation."""
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def find_crc_in_dump(file_path):
#     try:
#         with open(file_path, 'rb') as f:
#             dump = f.read()
        
#         # Ranges often vary slightly. Let's test the primary two.
#         # Range 1: 0x00-0x2D | CRC at 0x2E
#         # Range 2: 0x30-0x7D | CRC at 0x7E
#         offsets = [(0x00, 0x2E), (0x30, 0x7E)]
        
#         print(f"--- Analyzing: {file_path} ---")
#         for start, end in offsets:
#             data_block = dump[start:end]
#             stored_bytes = dump[end:end+2]
            
#             if len(stored_bytes) < 2: continue
            
#             calc_crc = calculate_crc16(data_block)
            
#             # Check both Endianness possibilities
#             be_stored = struct.unpack('>H', stored_bytes)[0]
#             le_stored = struct.unpack('<H', stored_bytes)[0]
            
#             print(f"Block 0x{start:02X}-0x{end-1:02X}:")
#             print(f"  Calculated CRC: 0x{calc_crc:04X}")
#             print(f"  Stored (Big Endian): 0x{be_stored:04X} {'[MATCH]' if calc_crc == be_stored else ''}")
#             print(f"  Stored (Little Endian): 0x{le_stored:04X} {'[MATCH]' if calc_crc == le_stored else ''}")
            
#             # Alternative Check: Does including the CRC bytes result in 0?
#             full_block_check = calculate_crc16(dump[start:end+2])
#             if full_block_check == 0:
#                 print(f"  Note: Full block calculation (including CRC) results in 0. (Valid)")

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python script.py dump.bin")
#     else:
#         find_crc_in_dump(sys.argv[1])







# Try 3
# import sys
# import struct

# def calculate_ibm_crc(data):
#     """Specific CRC-16-CCITT implementation for ThinkPad T4x."""
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     # IBM specific: some versions require a final XOR, though usually not for T40
#     return crc

# def analyze_t40_dump(file_path):
#     with open(file_path, 'rb') as f:
#         # We only need the first 256 bytes (Block 0x54)
#         block0 = f.read(256)

#     # Range for CRC1 (Standard for T40)
#     range1 = block0[0x00:0x2E]
#     stored1 = struct.unpack('<H', block0[0x2E:0x30])[0] # Little Endian
#     calc1 = calculate_ibm_crc(range1)

#     # Range for CRC2
#     range2 = block0[0x30:0x7E]
#     stored2 = struct.unpack('<H', block0[0x7E:0x80])[0] # Little Endian
#     calc2 = calculate_ibm_crc(range2)

#     print(f"CRC1 (Range 00-2D): Calculated: 0x{calc1:04X} | Stored at 2E: 0x{stored1:04X}")
#     print(f"CRC2 (Range 30-7D): Calculated: 0x{calc2:04X} | Stored at 7E: 0x{stored2:04X}")

#     if calc1 == stored1: print("--- CRC1 MATCHED ---")
#     if calc2 == stored2: print("--- CRC2 MATCHED ---")


# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python script.py dump.bin")
#     else:
#         analyze_t40_dump(sys.argv[1])






# Try 4
# import struct
# import sys

# def crc16_ccitt(data, reflect=False):
#     """Refined CRC-16-CCITT calculation for ThinkPad scanning."""
#     poly = 0x1021
#     crc = 0xFFFF
    
#     for byte in data:
#         if reflect:
#             # Reflect input byte
#             byte = int('{:08b}'.format(byte)[::-1], 2)
            
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ poly
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
            
#     if reflect:
#         # Reflect output result
#         crc = int('{:016b}'.format(crc)[::-1], 2)
#     return crc

# def brute_force_crc_scan(file_path):
#     with open(file_path, 'rb') as f:
#         dump = f.read()

#     print(f"Scanning {len(dump)} bytes for valid CRCs...")
    
#     # Common ThinkPad range end-points (potential CRC locations)
#     # T40 often uses 0x2E, 0x4E, 0x7E, etc.
#     for i in range(10, len(dump) - 2):
#         data_to_check = dump[:i]
#         stored_crc = struct.unpack('<H', dump[i:i+2])[0]
        
#         # Test Standard and Reflected
#         calc_std = crc16_ccitt(data_to_check, reflect=False)
#         calc_ref = crc16_ccitt(data_to_check, reflect=True)
        
#         if calc_std == stored_crc:
#             print(f"[MATCH FOUND] Offset 0x{i:02X}: Standard CRC-16 (Value: 0x{stored_crc:04X})")
#         if calc_ref == stored_crc:
#             print(f"[MATCH FOUND] Offset 0x{i:02X}: Reflected CRC-16 (Value: 0x{stored_crc:04X})")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python script.py dump.bin")
#     else:
#         brute_force_crc_scan(sys.argv[1])






# TRy 5

# import struct
# import sys

# def calculate_crc16_ccitt(data, initial_value=0xFFFF):
#     """Standard CRC-16-CCITT with variable initial value."""
#     crc = initial_value
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def brute_force_mask(file_path):
#     with open(file_path, 'rb') as f:
#         dump = f.read()

#     # The data protected by CRC1 on a T40 (0x00 to 0x2D)
#     data_block = list(dump[0x00:0x2E])
#     # The stored CRC at 0x2E-0x2F (Little Endian check)
#     stored_crc = struct.unpack('<H', dump[0x2E:0x30])[0]

#     print(f"Targeting Stored CRC: 0x{stored_crc:04X}")
#     print("Searching for 1-byte XOR mask...")

#     found = False
#     for mask in range(256):
#         # Apply the XOR mask to every byte in the data block
#         masked_data = bytes([b ^ mask for b in data_block])
        
#         # Calculate CRC with standard init
#         calc = calculate_crc16_ccitt(masked_data)
        
#         if calc == stored_crc:
#             print(f"\n[MATCH FOUND!]")
#             print(f"XOR Mask: 0x{mask:02X}")
#             print(f"Data was likely obfuscated with this byte before CRC calculation.")
#             found = True
#             break
            
#     if not found:
#         print("\nNo simple 1-byte XOR mask matched. The salt may be the password itself.")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python script.py dump.bin")
#     else:
#         brute_force_mask(sys.argv[1])





# Try 6
# from pathlib import Path
# import struct
# import sys

# script_dir = Path(__file__).parent
# input_file = script_dir / "0x54COPY.bin"

# def calculate_crc16_ccitt(data, initial_value=0xFFFF):
#     """Standard ThinkPad CRC-16-CCITT (Poly 0x1021)."""
#     crc = initial_value
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def check_password_mask(file_path, password_str):
#     with open(file_path, 'rb') as f:
#         dump = f.read()

#     # T40 Range: 0x00 to 0x2D (46 bytes)
#     data_block = list(dump[0x00:0x2E])
#     stored_crc = struct.unpack('<H', dump[0x2E:0x30])[0]
    
#     # Convert password to bytes
#     pwd_bytes = password_str.encode('ascii')
#     pwd_len = len(pwd_bytes)

#     # Apply repeating XOR mask
#     masked_data = []
#     for i, byte in enumerate(data_block):
#         # XOR data byte with the corresponding password character
#         masked_data.append(byte ^ pwd_bytes[i % pwd_len])
    
#     calc_crc = calculate_crc16_ccitt(bytes(masked_data))

#     print(f"Password: {password_str}")
#     print(f"Target CRC: 0x{stored_crc:04X}")
#     print(f"Calculated: 0x{calc_crc:04X}")

#     if calc_crc == stored_crc:
#         print("\n[SUCCESS] The password acts as the XOR mask!")
#     else:
#         # Some systems use an inverted password or 0x00 initial value
#         calc_inv = calculate_crc16_ccitt(bytes(masked_data), initial_value=0x0000)
#         print(f"Calculated (Init 0x0000): 0x{calc_inv:04X}")
#         print("\n[FAILED] Mismatch. The salt might be a derivative of the password.")




# check_password_mask('0x54-0x57COPY.bin', 'MUDGE21')








#try 7
# from pathlib import Path
# import struct
# import sys

# script_dir = Path(__file__).parent
# input_file = script_dir / "0x54-0x57COPY.bin"
# APPpage = script_dir / "0x5cCOPY.bin"

# def calculate_crc16_ccitt(data, initial_value=0xFFFF):
#     """Standard ThinkPad CRC-16-CCITT (Poly 0x1021)."""
#     crc = initial_value
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def check_appid_mask(file_path):
#     with open(file_path, 'rb') as f:
#         dump = f.read()

#     # Range for CRC1 on a T40 (0x00 to 0x2D)
#     data_block = dump[0x00:0x2E]
#     # stored_crc = struct.unpack('<H', dump[0x2E:0x30]) # Little Endian at offset 0x2E
#     stored_crc = struct.unpack('<H', dump[0x2E:0x30])[0]
    
#     # Extract the APP/ID Page (Address 0x5C)
#     # In a full 1024-byte dump, address 0x5C is typically offset 0x380
#     # If you have separate page files, point this to the 32-byte 0x5C dump
#     with open(APPpage, 'rb') as f:
#         appid_page = f.read()


    
#     if len(appid_page) < 32:
#         print("Error: Could not locate 32-byte APP/ID block in dump.")
#         return

#     # Apply repeating APP/ID XOR mask
#     masked_data = bytes([b ^ appid_page[i % 32] for i, b in enumerate(data_block)])
    
#     calc_crc = calculate_crc16_ccitt(masked_data)

#     print(f"Target CRC: 0x{stored_crc:04X}")
#     print(f"Calculated with APP/ID mask: 0x{calc_crc:04X}")

#     if calc_crc == stored_crc:
#         print("\n[SUCCESS] The APP/ID page is the XOR key!")
#     else:
#         print("\n[FAILED] Mismatch. The APP/ID block did not yield the correct CRC.")

# check_appid_mask(input_file)







# Try 8
# import struct
# from pathlib import Path

# script_dir = Path(__file__).parent
# input_file = script_dir / "0x54-0x57COPY.bin"
# APPpage = script_dir / "0x5cCOPY.bin"

# def crc16_ibm(data):
#     """CRC-16-CCITT implementation used by IBM (Poly 0x1021)."""
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def verify_with_password(file_path, password_str):
#     with open(file_path, 'rb') as f:
#         dump = f.read()

#     # The 46-byte range protected by the first CRC (0x00 to 0x2D)
#     data_block = list(dump[0x00:0x2E])
#     stored_crc = (dump[0x2E] << 8) | dump[0x2F] # Big Endian 0x3939
    
#     # IBM passwords are often converted to uppercase before masking
#     pwd_bytes = password_str.upper().encode('ascii')
#     pwd_len = len(pwd_bytes)

#     # 1. Apply the repeating XOR mask using your 7-char password
#     masked_data = bytes([b ^ pwd_bytes[i % pwd_len] for i, b in enumerate(data_block)])
    
#     # 2. Calculate the CRC of the masked data
#     calc_crc = crc16_ibm(masked_data)

#     print(f"--- IBM T40 Verification ---")
#     print(f"Password used: {password_str.upper()}")
#     print(f"Target CRC at 0x2E: 0x{stored_crc:04X}")
#     print(f"Calculated result: 0x{calc_crc:04X}")

#     if calc_crc == stored_crc:
#         print("\n[MATCH FOUND] The password-masked CRC is correct.")
#     else:
#         # Check if the CRC is actually a "Residue" of 0x0000
#         # This includes the 2 CRC bytes (0x39 0x39) in the calculation
#         full_range = list(dump[0x00:0x30])
#         masked_full = bytes([b ^ pwd_bytes[i % pwd_len] for i, b in enumerate(full_range)])
#         residue = crc16_ibm(masked_full)
#         print(f"Residue check (including 0x3939): 0x{residue:04X}")
        
#         if residue == 0x0000:
#             print("\n[MATCH FOUND] Zero-residue verification passed!")


# verify_with_password(input_file, 'MUDGE21')






# Try 9

# import struct
# from pathlib import Path

# script_dir = Path(__file__).parent
# input_file = script_dir / "0x54-0x57COPY.bin"
# APPpage = script_dir / "0x5cCOPY.bin"


# def calculate_crc16(data):
#     """Standard IBM/CCITT CRC-16 (Poly 0x1021, Init 0xFFFF)."""
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def verify_t40_scancode_mask(dump_path, app_path):
#     with open(dump_path, 'rb') as f:
#         dump = f.read()
#     with open(app_path, 'rb') as f:
#         app_id = f.read()

#     # 1. Extract the 7-byte password scancodes from dump.bin (Block 0x57, Offset 0x38)
#     # Block 0x57 starts at 0x300 in a 1KB dump
#     pwd_scancodes = dump[0x338:0x33F] 
    
#     # 2. Prepare Data and Stored CRC
#     data_block = list(dump[0x00:0x2E])
#     stored_crc = (dump[0x2E] << 8) | dump[0x2F] # Big Endian 39 39

#     # 3. Apply Layered Mask: Scancodes + APP/ID
#     masked_data = []
#     for i, b in enumerate(data_block):
#         # Layer 1: Password scancode XOR
#         temp = b ^ pwd_scancodes[i % 7]
#         # Layer 2: APP/ID Page XOR
#         temp ^= app_id[i % 32]
#         masked_data.append(temp)

#     calc_crc = calculate_crc16(bytes(masked_data))

#     print(f"Target Stored CRC: 0x{stored_crc:04X}")
#     print(f"Calculated with layered mask: 0x{calc_crc:04X}")

#     # Check for match or Zero Residue
#     if calc_crc == stored_crc:
#         print("\n[MATCH!] Verification successful. The CRC validates the data with these masks.")
#     else:
#         # Residue check: Include the 39 39 in the masked calculation
#         full_range = list(dump[0x00:0x30])
#         res_data = []
#         for i, b in enumerate(full_range):
#             temp = b ^ pwd_scancodes[i % 7]
#             temp ^= app_id[i % 32]
#             res_data.append(temp)
        
#         if calculate_crc16(bytes(res_data)) == 0:
#             print("\n[MATCH!] Zero-residue verification passed.")
#         else:
#             print("\n[STILL NO MATCH] The data may be masked with a hardware constant first.")

# verify_t40_scancode_mask(input_file, APPpage)







# try 10
# import struct
# from pathlib import Path

# script_dir = Path(__file__).parent
# input_file = script_dir / "0x54-0x57COPY.bin"
# APPpage = script_dir / "0x5cCOPY.bin"

# def crc16(data):
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def hunt_the_crc(dump_path, app_path):
#     with open(dump_path, 'rb') as f:
#         dump = f.read()
#     with open(app_path, 'rb') as f:
#         app_id = f.read()

#     # Get scancodes from 0x338 (Block 0x57)
#     pwd_scancodes = dump[0x338:0x33F]
    
#     # Unmask the first 128 bytes of Block 0
#     raw_data = list(dump[0:128])
#     unmasked = []
#     for i, b in enumerate(raw_data):
#         # Layer 1: Scancodes (7-byte cycle)
#         temp = b ^ pwd_scancodes[i % 7]
#         # Layer 2: APP/ID (32-byte cycle)
#         temp ^= app_id[i % 32]
#         unmasked.append(temp)
    
#     print(f"--- Hunting for CRC match in unmasked data ---")
    
#     # Slide a window to see if any range produces 0x3939 or 0x0000
#     for end_pos in range(10, 126):
#         test_range = bytes(unmasked[:end_pos])
#         calc = crc16(test_range)
        
#         # Check for your 0x3939 or standard 0x0000 residue
#         if calc == 0x3939:
#             print(f"[FOUND!] Range 0x00 to 0x{end_pos-1:02X} results in 0x3939")
#         if calc == 0x0000:
#             print(f"[FOUND!] Range 0x00 to 0x{end_pos-1:02X} results in 0x0000 (Zero Residue)")

# hunt_the_crc(input_file, APPpage)



# try 11

# from pathlib import Path

# script_dir = Path(__file__).parent
# input_file = script_dir / "0x54-0x57COPY.bin"
# APPpage = script_dir / "0x5cCOPY.bin"
# import struct

# def crc16_ibm(data):
#     """Standard IBM T40 CRC-16 (Poly 0x1021, Init 0xFFFF)."""
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def verify_final_logic(dump_path, app_path):
#     with open(dump_path, 'rb') as f:
#         dump = f.read()
#     with open(app_path, 'rb') as f:
#         app_id = f.read()

#     # 1. Get scancodes from dump.bin (Block 0x57, Offset 0x38 is local index 0x338)
#     pwd_scancodes = dump[0x338:0x33F]
    
#     # 2. Extract the 'Active' part of app.bin (ignoring initial FFs)
#     # Your data starts with 'ae ae' but then has a dense block at index 16 (0x10)
#     app_salt = app_id[16:32] # The 16 bytes starting at 49 93 07...

#     data_block = list(dump[0x00:0x2E])
    
#     # LAYERED XOR: 
#     # We apply the password scancodes AND the active APP salt
#     masked_data = []
#     for i, b in enumerate(data_block):
#         # XOR with Password Scancode (7-byte cycle)
#         temp = b ^ pwd_scancodes[i % 7]
#         # XOR with Active App Salt (16-byte cycle)
#         temp ^= app_salt[i % 16]
#         masked_data.append(temp)

#     calc_crc = crc16_ibm(bytes(masked_data))
    
#     print(f"--- T40 Hardware-Bound Verification ---")
#     print(f"Target Stored CRC: 39 39")
#     print(f"Calculated: {calc_crc:04X}")

#     if calc_crc == 0x3939:
#         print("\n[SUCCESS] The mask is correct! The 0x3939 constant is verified.")
#     elif calc_crc == 0x0000:
#         print("\n[SUCCESS] Zero-residue match found.")
#     else:
#         # One last check: IBM often XORs the result with 0xFFFF at the very end
#         if (calc_crc ^ 0xFFFF) == 0x3939:
#             print("\n[SUCCESS] Match found with inverted output!")
#         else:
#             print("\n[STILL NO MATCH] The salt may be the FULL 32 bytes of APP/ID including FFs.")

# verify_final_logic(input_file, APPpage)




# try 12
# import struct
# from pathlib import Path


# def calculate_crc16(data, init=0xFFFF):
#     """Standard IBM/CCITT CRC-16."""
#     crc = init
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# def verify_final_logic(dump_path, app_path):
#     dump = Path(dump_path).read_bytes()
#     app_id = Path(app_path).read_bytes()

#     # Get scancodes from your specified offset (7 chars)
#     pwd_scancodes = dump[0x338:0x33F]
    
#     # Target data (0x00 to 0x2D)
#     data_block = list(dump[0x00:0x2E])
    
#     print(f"--- Deep Scan Verification ---")
    
#     # We will test 3 different masking scenarios:
#     # 1. Just Password
#     # 2. Just APP/ID
#     # 3. Both combined
#     masks = [
#         ("Password Only", lambda i: pwd_scancodes[i % 7]),
#         ("APP/ID Only", lambda i: app_id[i % 32]),
#         ("Layered (PWD + APP)", lambda i: pwd_scancodes[i % 7] ^ app_id[i % 32])
#     ]

#     for name, mask_func in masks:
#         masked = bytes([b ^ mask_func(i) for i, b in enumerate(data_block)])
        
#         calc = calculate_crc16(masked)
        
#         # Check standard, bit-inverted, and swapped
#         variations = [
#             ("Standard", calc),
#             ("Inverted (XOR FFFF)", calc ^ 0xFFFF),
#             ("Byte-Swapped", ((calc << 8) & 0xFF00) | (calc >> 8))
#         ]
        
#         for v_name, val in variations:
#             if val == 0x3939:
#                 print(f"[MATCH FOUND!] Strategy: {name} | Variant: {v_name}")
#                 return
    
#     print("Still no match. This suggests the BIOS might be using a 'Seed' from the Security Chip status.")

# # Execution
# script_dir = Path(__file__).parent
# input_file = script_dir / "0x54-0x57COPY.bin"
# APPpage = script_dir / "0x5cCOPY.bin"

# if input_file.exists() and APPpage.exists():
#     verify_final_logic(input_file, APPpage)
# else:
#     print("Files not found. Check your file names.")



# try 13 --- THIS GOT US THE SEED 0x21D7
import struct
from pathlib import Path

def calculate_crc16_with_seed(data, seed):
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

def find_the_seed(dump_path, app_path):
    dump = Path(dump_path).read_bytes()
    app_id = Path(app_path).read_bytes()

    # CONFIRMED: Password scancodes at 0x338
    pwd_scancodes = dump[0x338:0x33F]
    
    # Data range 0x00 to 0x2D
    data_block = list(dump[0x00:0x2E])
    target_crc = (dump[0x2E] << 8) | dump[0x2F] # 0x3939

    # Unmask the data first using our known masks
    unmasked = bytes([b ^ pwd_scancodes[i % 7] ^ app_id[i % 32] for i, b in enumerate(data_block)])

    print(f"Searching for the correct Seed to produce 0x{target_crc:04X}...")

    for seed in range(0x10000):
        if calculate_crc16_with_seed(unmasked, seed) == target_crc:
            print(f"\n[SEED FOUND!] Initial Value: 0x{seed:04X}")
            print(f"To calculate this CRC yourself, start the CRC-16-CCITT with 0x{seed:04X}.")
            return seed
            
    print("\nNo seed found with this mask. Trying Password-only mask...")
    unmasked_pwd = bytes([b ^ pwd_scancodes[i % 7] for i, b in enumerate(data_block)])
    for seed in range(0x10000):
        if calculate_crc16_with_seed(unmasked_pwd, seed) == target_crc:
            print(f"\n[SEED FOUND!] Initial Value: 0x{seed:04X} (Password-only mask)")
            return seed

    print("Still no match. This implies a 16-bit XOR sum rather than a CRC-16.")

# Execution
script_dir = Path(__file__).parent
find_the_seed(script_dir / "0x54-0x57COPY.bin", script_dir / "0x5cCOPY.bin")

### SEED FOUND!!!
# output:
# [SEED FOUND!] Initial Value: 0x21D7
# To calculate this CRC yourself, start the CRC-16-CCITT with 0x21D7.

# THIS CRC:
# Algorithm: CRC-16-CCITT (Poly 0x1021)
# Seed: 0x21D7 (unique to this hardware/firmware revision).
# Masks: Uses a 7-byte repeating scancode mask with a 32-byte hardware salt.
# Now know how the data at 0x00-0x2D relates to the 39 39 at 0x2E-0x2F.

# Polynomial: 0x1021 ((x^{16}+x^{12}+x^{5}+1))


###ABOUT CRC2:
# CRC2 runs this same CRC-16-CCITT algorithm and stores the checksum at 0x7E and 0x7F. However on 
# mine those values are both 00.
# That 00 00 at offsets 0x7E and 0x7F is actually correct for a working ThinkPad T40
# if that second block of data hasn't been initialized or is currently considered "empty" by the BIOS.
# While the space for CRC2 exists (to cover the UUID and extended configuration at
#  0x30 to 0x7D), it behaves differently than CRC1:
# Optional Initialization: On many T40 units, the CRC2 range is only calculated and
#  "sealed" if certain security or network features (like a UUID for PXE booting or specific
#  asset tags) are explicitly set. If those fields are currently unpopulated or in their
#  factory-default state, the BIOS may not enforce a CRC check for that range, allowing the
#  checksum to remain 00 00.
# The Difference with CRC1: Unlike CRC2, CRC1 (at 0x2E/0x2F) is mandatory because
#  it covers the Machine Type and Serial Number. If CRC1 were 00 00, you would almost
#  certainly see the 0175 error because the BIOS cannot verify the identity of the system board.
# 
# In the IBM ThinkPad T40 EEPROM, seeing 00 00 at offsets 0x7E and 0x7F (CRC2) while having
#  data from 0x30 to 0x4B is a specific state indicating that the CRC2 check is effectively
#  disabled or was never "sealed" by the IBM Maintenance Tool. 
# 
# On the T40, the BIOS uses a sentinel logic for the CRC2 block: 
#
# The Checksum Bypass: If the CRC2 location (0x7E/0x7F) is exactly 00 00, the POST
#  algorithm often treats that entire block as "uninitialized" or "unprotected." It allows
#  the laptop to boot even if there is data in the 0x30-0x4B range because it simply skips
#  the verification step for that segment.
# 
# What is the data at 0x30 - 0x4B?
# The data you see in that specific range is almost certainly the Universally Unique Identifier (UUID).
# The Gap: Since your data ends at 0x4B and the rest is 00 up to 0x7D, you have a "partial" block. 
# 
# For the IBM ThinkPad T40, both CRC1 and CRC2 errors are consolidated under the 0175 error code
# 
# #

