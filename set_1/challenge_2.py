#!/usr/bin/env python
#
# Fixed XOR

import binascii
import logging

import cp_lib


IN_HEX_STR_1 = '1c0111001f010100061a024b53535009181c'
IN_HEX_STR_2 = '686974207468652062756c6c277320657965'
OUT_XOR = '746865206b696420646f6e277420706c6179'

logger = logging.getLogger(__name__)

def xor_hex_strings(hex1, hex2):
    if len(hex1) != len(hex2):
        raise cp_lib.ValueError('Length of inputs do not match.')

    raw1 = bytearray(hex1.decode('hex'))
    raw2 = bytearray(hex2.decode('hex'))

    # hexlify a string of XOR'd bytes
    return binascii.hexlify(''.join([chr(raw1[i] ^ raw2[i]) for i in range(len(raw1))]))

def test(in1, in2, out):
    logger.info('Test case. XOR 2 hex strings.')
    assert xor_hex_strings(in1, in2) == out, 'Failed to XOR 2 hex strings.'

def run_tests():
    test(IN_HEX_STR_1, IN_HEX_STR_2, OUT_XOR)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
