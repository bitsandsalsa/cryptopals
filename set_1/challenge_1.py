#!/usr/bin/env python
#
# Convert hex to base64

import logging


IN_HEX_STR = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
OUT_BASE64 = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def hex_to_base64(hex_str):
    return hex_str.decode('hex').encode('base64').strip()

def test(in1, out):
    logging.info('Test case. Convert hex to base 64.')
    assert hex_to_base64(in1) == out, 'Failed to convert hex to base64.'

def run_tests():
    test(IN_HEX_STR, OUT_BASE64)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_tests()
    print 'Success'
