import collections
import logging

from Crypto.Cipher import AES

from set_1.challenge_3 import brute_force_xor
from set_1.challenge_5 import repeating_key_xor
from set_1.challenge_7 import aes_ecb_encrypt
from set_2.challenge_9 import pkcs7_pad
from set_2.challenge_10 import aes_cbc_encrypt


logger = logging.getLogger(__name__)

MODE_ECB = 0
MODE_CBC = 1
MODE_2_TXT = {
    MODE_ECB: 'ECB',
    MODE_CBC: 'CBC'
}

class ValueError(Exception):
    pass

class RuntimeError(Exception):
    pass

def iter_over_blocks(data, block_sz):
    for i in xrange(0, len(data), block_sz):
        yield data[i:i+block_sz]

def detect_aes_ecb(ciphertext, common_block_cnt_threshold=1):
    logger.info('Looking for common AES blocks in ciphertext.')
    counter = collections.Counter()
    for ct_block in iter_over_blocks(ciphertext, AES.block_size):
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

    assert detected == actual, (
        'Detected mode "{}" not equal to actual mode "{}".'.format(
            MODE_2_TXT[detected],
            MODE_2_TXT[actual]
        )
    )

    logger.info('Detected AES mode: %s.', MODE_2_TXT[detected])

    return detected
