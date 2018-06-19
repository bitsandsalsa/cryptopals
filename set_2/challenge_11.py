#!/usr/bin/env python
#
# An ECB/CBC detection oracle

import collections
import logging
import random

import Crypto.Random
from Crypto.Cipher import AES

import cp_lib


module_logger = logging.getLogger(__name__)
random_generator = Crypto.Random.new()

class BlackBoxEncryptor(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

    def encrypt(self, data):
        return self._aes_ecb_or_cbc_encrypt(data)

    def _aes_ecb_or_cbc_encrypt(self, data):
        """
        Encrypt using AES in either ECB or CBC mode chosen at random, but add a 5 to 10 byte prefix
        and suffix to the plaintext.
        """
        key = random_generator.read(16)
        mode = random.choice([cp_lib.MODE_ECB, cp_lib.MODE_CBC])

        data_prefix = random_generator.read(random.randint(5, 10))
        self.logger.info('Injecting a %d byte prefix to data.', len(data_prefix))
        data_suffix = random_generator.read(random.randint(5, 10))
        self.logger.info('Injecting a %d byte suffix to data.', len(data_suffix))
        new_data = cp_lib.pkcs7_pad(data_prefix + data + data_suffix, AES.block_size)
        if mode == cp_lib.MODE_ECB:
            self.logger.info('Encrypting in AES ECB mode.')
            ciphertext = cp_lib.aes_ecb_encrypt(new_data, key)
        elif mode == cp_lib.MODE_CBC:
            self.logger.info('Encrypting in AES CBC mode.')
            iv = random_generator.read(AES.block_size)
            ciphertext = cp_lib.aes_cbc_encrypt(new_data, key, iv)
        else:
            raise cp_lib.ValueError('Unknown AES mode: {}.'.format(mode))

        return (ciphertext, mode)

def run_tests():
    encryptor = BlackBoxEncryptor()

    for i in range(25):
        mode = cp_lib.detect_aes_ecb_or_cbc_mode(encryptor)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    module_logger = logging.getLogger()
    run_tests()
    print 'Success'
