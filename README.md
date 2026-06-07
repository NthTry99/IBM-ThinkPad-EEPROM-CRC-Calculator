# IBM-ThinkPad-EEPROM-CRC-Calculator

The goal of this project is to research and understand the BIOS POST errors on IBM-era ThinkPads which result from problems with data stored in the EEPROM, specifically the following errors:

- 0175: Bad CRC1
- 0177: Bad SVP data
- 0182: Bad CRC2

These errors can effectively ruin an otherwise perfectly fine laptop. I believe I have determined how these "CRCs" are calculated and have created scripts which are able to calculate their expected values in the EEPROM data. The workflow goes as follows:

1. Obtain the EEPROM data using an external programmer
2. Run the data through the respective script depending on the specific error (i.e CRC1/CRC2/SVP CRC)
3. Write the correct CRC back to its proper memory offset in the EEPROM data

This is still a relatively new project for me, and I have not had an opportunity to physically test this hypothesis on a real IBM ThinkPad yet. However, through much research and differential analysis of many different sets of EEPROM data from that era, I am confident I am on the right track.

I am waiting to get my hands on a more suitable "test subject" laptop rather than risk bricking my perfectly-working T40. These laptops aren't exactly plentiful anymore, unfortunately.

More info available on [the website](https://frontdeskresearch.com/ibm_t40_crc_calculators/) and more to come!
