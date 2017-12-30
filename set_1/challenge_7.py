#!/usr/bin/env python
#
# AES in ECB mode

import logging

from Crypto.Cipher import AES


IN_KEY = 'YELLOW SUBMARINE'
IN_CIPHERTEXT_FILE = '7.txt'

OUT_PLAINTEXT_LINE0 = "I'm back and I'm ringin' the bell "
OUT_PLAINTEXT_LINE78 = "Play that funky music "  # last line before padding

logger = logging.getLogger(__name__)

#XXX: does not handle padding
def aes_ecb_encrypt(data, key):
    cipher = AES.new(key, mode=AES.MODE_ECB)
    return cipher.encrypt(data)

#XXX: does not handle padding
def aes_ecb_decrypt(data, key):
    cipher = AES.new(key, mode=AES.MODE_ECB)
    return cipher.decrypt(data)

def run_tests():
    ciphertext = open(IN_CIPHERTEXT_FILE).read().decode('base64')
    logger.info('Decrypting data using AES in ECB mode.')
    plaintext = aes_ecb_decrypt(ciphertext, IN_KEY)
    logger.debug('Decrypted data:\n-----\n%s\n-----', plaintext)

    plaintext_lines = plaintext.split('\n')
    assert OUT_PLAINTEXT_LINE0 == plaintext_lines[0], 'Failed to decrypt line 0.'
    assert OUT_PLAINTEXT_LINE78 == plaintext_lines[78], 'Failed to decrypt line 78.'

    logger.info('Re-encrypting the plaintext using AES in ECB mode.')
    test_ct = aes_ecb_encrypt(plaintext, IN_KEY)
    assert ciphertext == test_ct, 'Failed to re-encrypt decrypted data.'

if __name__ == '__main__':
    # increase logging level to DEBUG to see decrypted data
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
