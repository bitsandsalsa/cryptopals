#!/usr/bin/env python
#
# Fixed XOR

import binascii

IN_HEX_STR_1 = '1c0111001f010100061a024b53535009181c'
IN_HEX_STR_2 = '686974207468652062756c6c277320657965'
TARGET_XOR_RESULT = '746865206b696420646f6e277420706c6179'

raw1 = bytearray(IN_HEX_STR_1.decode('hex'))
raw2 = bytearray(IN_HEX_STR_2.decode('hex'))

assert len(raw1) == len(raw2), 'Length of inputs do not match.'

# hexlify a string of XOR'd bytes
result = binascii.hexlify(''.join([chr(raw1[i] ^ raw2[i]) for i in range(len(raw1))]))

print result == TARGET_XOR_RESULT
