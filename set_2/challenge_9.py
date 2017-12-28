#!/usr/bin/env python
#
# Implement PKCS#7 padding

import logging

IN_PLAINTEXT = 'YELLOW SUBMARINE'
IN_BLOCK_SZ = 20

OUT_PADDED_PLAINTEXT = IN_PLAINTEXT + ('\x04' * 4)

logger = logging.getLogger(__name__)

def pkcs7_pad(data, block_sz):
    final_block_sz = len(data) % block_sz
    pad_sz = final_block_sz if final_block_sz == 0 else block_sz - final_block_sz
    return data + (chr(pad_sz) * pad_sz)

def run_test(data, block_sz, expected_padded_block):
    logger.info('Padding %d bytes of data for %d byte blocks.', len(data), block_sz)
    padded_data = pkcs7_pad(data, block_sz)
    assert expected_padded_block == padded_data, (
        'Failed to pad "{}" for {:d} byte blocks.'.format(data, block_sz))

def run_tests():
    run_test(IN_PLAINTEXT, IN_BLOCK_SZ, OUT_PADDED_PLAINTEXT)

    block_sz = 8

    data = ''
    run_test(data, block_sz, data)

    data = 'A'
    run_test(data, block_sz, data + ('\x07' * 7))

    data = 'A' * (block_sz - 1)
    run_test(data, block_sz, data + ('\x01' * 1))

    data = 'A' * block_sz
    run_test(data, block_sz, data)

    data = 'A' * (block_sz + 1)
    run_test(data, block_sz, data + ('\x07' * 7))

    data = 'A' * (2 * block_sz - 1)
    run_test(data, block_sz, data + ('\x01' * 1))

    data = 'A' * (2 * block_sz)
    run_test(data, block_sz, data)

    data = 'A' * (2 * block_sz + 1)
    run_test(data, block_sz, data + ('\x07' * 7))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
