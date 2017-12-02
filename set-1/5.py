#!/usr/bin/env python
#
# Implement repeating-key XOR

import binascii
import itertools


PLAINTEXT = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
KEY = 'ICE'
TARGET_CIPHERTEXT = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

pt_bytes = bytearray(PLAINTEXT)

key_iter = itertools.cycle(bytearray(KEY))
ct_bytes = []
for pt_byte in pt_bytes:
    ct_bytes.append(pt_byte ^ key_iter.next())
ct_hex = binascii.hexlify(''.join([chr(x) for x in ct_bytes]))

print ct_hex == TARGET_CIPHERTEXT
