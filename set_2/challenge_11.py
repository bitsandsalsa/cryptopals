#!/usr/bin/env python
#
# An ECB/CBC detection oracle

import collections
import logging
import random

import Crypto.Random
from Crypto.Cipher import AES

import cp_lib


MODE_ECB = 0
MODE_CBC = 1
MODE_2_TXT = {
    MODE_ECB: 'ECB',
    MODE_CBC: 'CBC'
}

module_logger = logging.getLogger(__name__)
random_generator = Crypto.Random.new()

class BlackBoxEncryptor(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

    def encrypt(self, data):
        return self._aes_ecb_or_cbc_encrypt(data)

    def _aes_ecb_or_cbc_encrypt(self, data):
        key = random_generator.read(AES.block_size)
        mode = random.choice([MODE_ECB, MODE_CBC])

        data_prefix = random_generator.read(random.randint(5, 10))
        self.logger.info('Injecting a %d byte prefix to data.', len(data_prefix))
        data_suffix = random_generator.read(random.randint(5, 10))
        self.logger.info('Injecting a %d byte suffix to data.', len(data_suffix))
        new_data = cp_lib.pkcs7_pad(data_prefix + data + data_suffix, AES.block_size)
        if mode == MODE_ECB:
            self.logger.info('Encrypting in AES ECB mode.')
            ciphertext = cp_lib.aes_ecb_encrypt(new_data, key)
        elif mode == MODE_CBC:
            self.logger.info('Encrypting in AES CBC mode.')
            iv = random_generator.read(AES.block_size)
            ciphertext = cp_lib.aes_cbc_encrypt(new_data, key, iv)
        else:
            raise cp_lib.CPValueError('Unknown AES mode: {}.'.format(mode))

        return (ciphertext, mode)

def detect_aes_ecb(ciphertext, common_block_cnt_threshold=1):
    module_logger.info('Looking for common AES blocks in ciphertext.')
    counter = collections.Counter()
    for ct_block in cp_lib.iter_over_blocks(ciphertext, AES.block_size):
        counter[ct_block] += 1
        if counter[ct_block] > common_block_cnt_threshold:
            break
    else:
        return False
    return True

def detect_aes_ecb_or_cbc_mode(encryptor):
    # We need to compare 2 ciphertext blocks, but black box is adding a 5 to 10 byte prefix and
    # suffix so we need to compensate by spilling over into more blocks.
    min_sz = AES.block_size * 2
    min_compensation = 2 * (AES.block_size - 5)
    sz = min_sz + min_compensation

    # Additionally, we don't want any padding bytes.
    final_block_sz = sz % AES.block_size
    pad_sz = final_block_sz if final_block_sz == 0 else AES.block_size - final_block_sz

    ciphertext, actual = encryptor.encrypt('\x00' * (sz + pad_sz))

    if detect_aes_ecb(ciphertext):
        detected = MODE_ECB
    else:
        detected = MODE_CBC
    return (detected, actual)

def run_tests():
    encryptor = BlackBoxEncryptor()

    for i in range(25):
        detected, actual = detect_aes_ecb_or_cbc_mode(encryptor)

        assert detected == actual, (
            'Detected mode "{}" not equal to actual mode "{}".'.format(
                MODE_2_TXT[detected],
                MODE_2_TXT[actual]
            )
        )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    module_logger = logging.getLogger()
    run_tests()
    print 'Success'
