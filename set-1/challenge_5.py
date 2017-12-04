#!/usr/bin/env python
#
# Implement repeating-key XOR

import binascii
import itertools
import logging


IN_PLAINTEXT = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
IN_KEY = 'ICE'
OUT_CIPHERTEXT = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

def encrypt(key, plaintext):
    pt_bytes = bytearray(plaintext)

    key_iter = itertools.cycle(bytearray(key))
    ct_bytes = []
    for pt_byte in pt_bytes:
        ct_bytes.append(pt_byte ^ key_iter.next())
    return binascii.hexlify(''.join([chr(x) for x in ct_bytes]))

def test(key, plaintext, out):
    logging.info('Test case. Repeating key XOR.')
    assert encrypt(key, plaintext) == out, 'Failed to encrypt.'

def run_tests():
    logging.basicConfig(level=logging.INFO)
    test(IN_KEY, IN_PLAINTEXT, OUT_CIPHERTEXT)

run_tests()
print 'Success'
