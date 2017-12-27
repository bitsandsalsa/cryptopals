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

logger = logging.getLogger(__name__)

def encrypt(key, plaintext, out_format_func=lambda x:x):
    """
    :param str key: encryption key
    :param str plaintext: plaintext
    :param callable out_format_func
    :return: out_format_func is called with byte string after encryption
    """
    pt_bytes = bytearray(plaintext)

    key_iter = itertools.cycle(bytearray(key))
    ct_bytes = []
    for pt_byte in pt_bytes:
        ct_bytes.append(pt_byte ^ key_iter.next())
    return out_format_func(''.join([chr(x) for x in ct_bytes]))

def test(key, plaintext, out):
    logger.info('Test case. Repeating key XOR.')
    assert encrypt(key, plaintext, binascii.hexlify) == out, 'Failed to encrypt.'

def run_tests():
    test(IN_KEY, IN_PLAINTEXT, OUT_CIPHERTEXT)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
