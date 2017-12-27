#!/usr/bin/env python
#
# Detect AES in ECB mode

import collections
import logging


IN_CIPHERTEXT_FILE = '8.txt'

OUT_LINE_IDX = 132
OUT_COMMON_BLOCK_CNT = 4
OUT_CIPHERTEXT = 'd880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a'

logger = logging.getLogger(__name__)

def run_tests():
    common_blocks = []  # list of tuples (line_idx, block_cnt, hex_ciphertext)
    logger.info('Looking for common AES blocks in ECB mode ciphertexts.')
    for line_idx, line in enumerate(open(IN_CIPHERTEXT_FILE).readlines()):
        ciphertext = line.strip().decode('hex')
        ct_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
        counter = collections.Counter(ct_blocks)
        _, block_cnt = counter.most_common(1)[0]
        if block_cnt > 1:
            common_blocks.append((line_idx, block_cnt, line.strip()))

    for line_idx, block_cnt, _ in common_blocks:
        logger.info('Line %2d ciphertext has %d common blocks.', line_idx, block_cnt)

    assert (OUT_LINE_IDX, OUT_COMMON_BLOCK_CNT, OUT_CIPHERTEXT) in common_blocks, (
        'Failed to find common blocks in a given ciphertext.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
