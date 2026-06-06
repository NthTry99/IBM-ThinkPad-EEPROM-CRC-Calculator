""" This is a useful quick tool to calculate the sum of a bunch of hex data.
simply copy data from a hex dump and paste it in the " " in the following format:

a = ("AA BB CC")

and it shall be printed."""

# Below are previously used and labeled groups of hex data I calculated during the development of my script
# To try one of these, simply uncomment a line such as a = ("AA BB CC")


### SER# DATA -- supposed CRC1 or sum at 0x07-0x08 (maybe just 0x08)

# from R51.BIN SER#
# ALL ADD UP TO 0x1100
# a = ("53 45 52 23 14 0C 01 D2 E3 00 00 00 00 00 00 00 40 33 39 54 35 32 34 30 5A 56 4A 30 42 30 35 37 45 31 34 43 20 B1 53 31 38 33 30 57 4A 42 4C 33 4E 4E 57 44 44 00 00 00 08 33 38 4C 35 33 34 30 5A 4A 31 57 30 38 35 37 48 35 46 42")

# from MY T40 SER# data
# ALL ADD UP TO 0x1100
# a = ("53 45 52 23 14 0C 01 D2 E1 00 00 00 00 00 00 00 40 31 33 52 31 31 32 33 5A 4A 31 55 52 59 34 33 50 31 52 47 20 B1 53 32 33 37 33 37 32 55 39 39 35 5A 47 4E 36 00 00 00 08 33 38 4C 35 30 30 31 5A 4A 31 4E 55 50 34 34 31 30 35 44")

# From an unknown T22 found at https://www.allservice.ro/forum/viewtopic.php?t=1003&sid=b018c33c4e44b119001327270828f465
# ALL ADD UP TO 0x1100
# a = ("53 45 52 23 14 0c 01 d2 8d 00 00 00 00 00 00 00 08 33 38 4c 33 38 35 31 5a 31 4e 31 35 36 31 41 56 32 41 46 20 b1 53 32 36 34 37 53 46 4d 37 38 37 48 41 4d 52 20 20 20 40 33 30 4c 32 32 36 31 5a 4a 31 4b 47 4e 31 41 4c 31 50 34 00 00 00 00")

#L540 SER#
# ALL ADD UP TO 0XE00
# a = ("53 45 52 23 18 0A 02 CF BA 40 30 43 31 38 32 32 33 5A 56 51 32 4D 4C 34 42 52 32 45 44 C0 B1 53 32 30 41 55 53 30 34 58 30 30 52 39 30 42 4B 4C 54 31")





### CON# DATA

# MY T40 with changed SVP to heyalex.
# this is its CON# block
# All ADD UP TO 0x1A00
# a = ("43 4F 4E 23 60 00 02 9B 36 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 60 0A 01 00 86 80 1E 10 00 02 A8 04 13 1F 91 08 00 0D 60 8B C0 A3")

# MY T40 with ORIGINAL SVP (MUDGE21)
# this is its CON# block
# ALL ADD UP TO 0x1600
# a = ("43 4F 4E 23 58 00 02 A3 24 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 05 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 60 0A 01 00 86 80 1E 10 00 02 A8 04 13 1F")

# MY T40 with SVP = 3rdtest. This is the same CON# as 4thtest and iamback.
# this is its CON# block
# ALL ADD UP TO 0x1900
# a = ("43 4F 4E 23 60 00 02 9B 30 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 05 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 60 0A 01 00 86 80 1E 10 00 02 A8 04 13 1F 91 08 00 0D 60 8B C0 A3")

# MY T40 with SVP = MMMMMM (6 M's)
# this is its CON# block
# ALL ADD UP TO 0x1600
# a = ("43 4F 4E 23 58 00 02 A3 24 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 05 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 60 0A 01 00 86 80 1E 10 00 02 A8 04 13 1F 00 00 00 00 00 00 00 00")

# MY T40 with SVP = MMMMMM (6 M's) but after BIOS settings restored to defaults
# this is its CON# block
# ALL ADD UP TO 0x1A00
# a = ("43 4F 4E 23 60 00 02 9B 36 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 60 0A 01 00 86 80 1E 10 00 02 A8 04 13 1F 91 08 00 0D 60 8B C0 A3")





# R51 CON# data (downloaded online)
# ALL add up to 0x1D72
# this is the same one where MY CRC calculator doesn't get same balancing bytes at 0x207-0x208
# a = ("43 4F 4E 23 72 00 02 EB 9C 00 00 00 00 00 00 00 90 12 02 11 25 D1 47 2B 11 CB 80 EC A4 E3 8B F5 A6 C9 AA 03 01 AB 0E 54 68 69 6E 6B 50 61 64 20 52 35 31 F0 0B 18 07 05 20 00 00 00 00 00 08 05 B9 A4 06 88 06 00 01 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 05 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 A8 04 13 1F 91 08 00 11 25 D1 5B 2B")

# T61 EEPROM dump I found online (T61conBlockOnly.bin)
# this its CON# block
# ALL ADD UP TO 0x1F00
# a = ("43 4F 4E 23 72 00 02 89 D9 00 00 00 00 00 00 00 90 12 8C 48 2A 01 4A 80 11 CB 86 AB AB D7 A1 B5 EB 95 AA 03 00 AB 0E 54 68 69 6E 6B 50 61 64 20 54 36 31 F0 0B 13 02 08 20 00 00 00 00 00 08 05 01 D0 07 88 06 00 04 00 00 30 03 00 78 1A FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 A8 04 9A 1F 91 08 00 1C 25 72 F1 F3 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

#L540 CON# --- BALANCING BYTES SUPPESEDLY BC 2C
# ALL ADD UP TO 0x1100
# a = ("43 4F 4E 23 3F 02 BC 2C 90 12 53 04 99 81 53 5F 11 CB BF 8D 8A 6D C7 83 23 94 AA 03 AB 0F 54 68 69 6E 6B 50 61 64 20 4C 35 34 30 F0 0B 30 11 14 20")

# From an unknown T22 found at https://www.allservice.ro/forum/viewtopic.php?t=1003&sid=b018c33c4e44b119001327270828f465
# ALL ADD UP TO 0x1300
# a = ("43 4f 4e 23 4e 00 01 ae da 00 00 00 00 00 00 00 90 12 80 b7 8c 01 44 0c 11 cb 9c 92 f4 66 7b 98 88 2b 08 05 11 84 03 88 06 00 01 00 00 30 03 40 78 1a 7f 38 77 00 ff 00 00 00 05 00 00 00 ff 00 00 00 ff 00 00 00 ff 00 00 00 a8 04 13 1f 00 00")


a = ("43 4F 4E 23 60 00 02 9B 36 00 00 00 00 00 00 00 90 12 E1 90 DE 01 47 04 11 CB BE C9 88 B2 7B 3F E9 A2 08 05 B9 DC 05 88 06 00 04 00 00 30 03 40 78 1A FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 FF 00 00 00 60 0A 01 00 86 80 1E 10 00 02 A8 04 13 1F 91 08 00 0D 60 8B C0 A3")


#MUDGE21 SVP SCANCODES: - total is 0xA1
# a = ("32 16 20 22 12 03 02")

#MMMMMM (6 M's) SVP SCANCODES - total is 0x12C -- the SVP checksum byte for this SVP is 0x2C
# a = ("32 32 32 32 32 32")

#HEYALEX SVP SCANCODES: - total is 0xCD
# a = ("23 12 15 1E 26 12 2D")

# This formats and prints out the sum:
print("Sum of bytes:")
print(hex(sum(bytearray.fromhex(a))))

# This prints out the string of hex as they were in a = ("AA BB CC")
print(f"Bytes used in calculation:\n{a}")




# To print a bytearray back as a string:
# test = bytearray.fromhex("32 16 20 22 12 03 02")
# print(test.hex(' ').upper())