# THIS IS JUNK! This is when I thought the CRC1 was stored at 0x2E-0x2F, but that is wrong!
# That is in the middle of the model type and serial number!
# Nevertheless, I didn't know that at the time.
# THis calculates that supposed CRC1 using a complex 0x1021 polynomial (which is also not how CRC1 is calculated)
# Also CRC1 is actually not a CRC at all, it is a balancing byte (at 0x07-0x08) to make the block add up to a multiple of 0x100

from pathlib import Path

def calculate_ibm_crc(data, seed=0x21D7):
    """Calculates the CRC-16-CCITT using the discovered hardware seed."""
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

def run_final_verification():
    # Setup paths
    script_dir = Path(__file__).parent
    dump_path = script_dir / "0x54-0x57COPY.bin"
    app_path = script_dir / "0x5cCOPY.bin"

    if not dump_path.exists() or not app_path.exists():
        print("Error: Missing input files.")
        return

    dump = dump_path.read_bytes()
    app_id = app_path.read_bytes()

    # Grab the known Password Scancodes (7 bytes)
    pwd_scancodes = dump[0x338:0x33F]
    
    # Extract Data Block (0x00 - 0x2D) and Stored CRC (0x2E - 0x2F)
    data_range = dump[0x00:0x2E]
    stored_crc_raw = dump[0x2E:0x30]
    stored_crc_val = (dump[0x2E] << 8) | dump[0x2F]

    # Unmask the data using the Layered Scancode + APP/ID mask
    unmasked_data = bytes([
        b ^ pwd_scancodes[i % 7] ^ app_id[i % 32] 
        for i, b in enumerate(data_range)
    ])

    # Run the calculation
    calculated_val = calculate_ibm_crc(unmasked_data)

    print("=== IBM ThinkPad T40 Security Validator ===")
    print(f"Data Range:       0x00 - 0x2D")
    print(f"Stored CRC (Hex): {stored_crc_raw.hex(' ').upper()}")
    print(f"Hardware Seed:    0x21D7")
    print("-" * 43)
    print(f"RESULT:           0x{calculated_val:04X}")
    
    if calculated_val == stored_crc_val:
        print("\n[STATUS: VALID] Match found! The laptop's POST check will pass.")
    else:
        print("\n[STATUS: INVALID] Checksum mismatch. This would trigger Error 0175.")

if __name__ == "__main__":
    run_final_verification()