#!/usr/bin/env python
#
# Implement CBC mode

import logging

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

import cp_lib


IN_KEY = 'YELLOW SUBMARINE'
IN_IV = '\x00' * 16
IN_CIPHERTEXT_FILE = '10.txt'

OUT_PLAINTEXT_LINE0 = "I'm back and I'm ringin' the bell "
OUT_PLAINTEXT_SHA256 = '368f2b80b437209451355b750181b378f425cc00af3922bcecc8d4a7d84a5198'

logger = logging.getLogger(__name__)

# We could use CBC mode from pycrypto package, but we are trying to learn here
#XXX: does not handle padding
def aes_cbc_decrypt(data, key, iv):
    cipher = AES.new(key, mode=AES.MODE_ECB, IV=iv)

    pt_blocks = []
    curr_iv = iv
    for ct_block in cp_lib.iter_over_blocks(data, AES.block_size):
        decrypted_block = cipher.decrypt(ct_block)
        pt_blocks.append(cp_lib.repeating_key_xor(curr_iv, decrypted_block))
        curr_iv = ct_block  # IV for next block is current ciphertext block
    return ''.join(pt_blocks)

# We could use CBC mode from pycrypto package, but we are trying to learn here
#XXX: does not handle paddign
def aes_cbc_encrypt(data, key, iv):
    cipher = AES.new(key, mode=AES.MODE_ECB, IV=iv)

    ct_blocks = []
    curr_iv = iv
    for pt_block in cp_lib.iter_over_blocks(data, AES.block_size):
        ct_blocks.append(cipher.encrypt(cp_lib.repeating_key_xor(curr_iv, pt_block)))
        curr_iv = ct_blocks[-1]  # IV for next block is current ciphertext block
    return ''.join(ct_blocks)

def run_tests():
    ciphertext = open(IN_CIPHERTEXT_FILE).read().decode('base64')
    logger.info('Decrypting data using AES in CBC mode.')
    plaintext = aes_cbc_decrypt(ciphertext, IN_KEY, IN_IV)
    assert plaintext.startswith(OUT_PLAINTEXT_LINE0), (
        'Decrypted data does not begin with expected contents.')
    assert SHA256.new(plaintext).hexdigest() == OUT_PLAINTEXT_SHA256, (
        'Unexpected digest of decrypted (AES CBC mode) data.')

    logger.info('Encrypting decrypted data using AES in CBC mode.')
    reencrypted = aes_cbc_encrypt(plaintext, IN_KEY, IN_IV)
    assert ciphertext == reencrypted, 'Failed to re-encrypt data.'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
