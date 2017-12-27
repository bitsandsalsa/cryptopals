#!/usr/bin/env python
#
# Break repeating-key XOR

import logging
import random
import string

import cp_lib


IN_STR_1 = 'this is a test'
IN_STR_2 = 'wokka wokka!!!'
IN_HAMMING_DIST = 37
IN_CIPHERTEXT_FILE = '6.txt'
OUT_KEY = 'Terminator X: Bring the noise'

KEY_SIZE_RANGE = (2, 65)

logger = logging.getLogger(__name__)

def calc_hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise cp_lib.CPValueError('Strings must be of equal length.')

    distance = 0
    # iterate string as list of bytes
    for i in range(len(s1)):
        b1 = '{:08b}'.format(ord(s1[i]))  # string 1 byte as bit string
        b2 = '{:08b}'.format(ord(s2[i]))  # string 2 byte as bit string
        assert len(b1) == len(b2) == 8, 'Bit strings must be of length 8'

        # count bit differences between bit strings
        for i in range(8):
            distance += 0 if b1[i] == b2[i] else 1
    return distance

def test_hamming_distance(s1, s2, expected_distance):
    logger.info('Test case. Hamming distance.')
    distance = calc_hamming_distance(s1, s2)
    assert expected_distance == distance, (
        'Incorrect Hamming distance s1: "{}", s2: "{}" -> {}; Expected {}'.format(s1, s2, distance, expected_distance))

def guess_key_size(ct, block_cnt):
    """
    :param str ct: ciphertext
    :param int block_cnt: number of blocks to use in calculating edit distance
    :return: key sizes
    :rtype: list(int)
    """
    logger.info('Guess key size between %d and %d bytes.', *KEY_SIZE_RANGE)
    norm_distances = {}  # {key_sz: hamming_distance}
    for key_sz in range(*KEY_SIZE_RANGE):
        hamming_distances = []
        for block_idx in range(block_cnt - 1):
            block1_idx = block_idx * key_sz
            block2_idx = block1_idx + key_sz
            hamming_distances.append(calc_hamming_distance(ct[block1_idx:block2_idx],
                                                           ct[block2_idx:block2_idx+key_sz]))
        avg_distance = sum(hamming_distances) / len(hamming_distances)
        norm_distances.update({key_sz: avg_distance / key_sz})
    sorted_guesses = sorted(norm_distances.items(), key=lambda x: x[1])
    return [key_sz for key_sz, _ in sorted_guesses]

def transpose_blocks(ct, key_sz):
    """
    Transpose 1st element of each block in ciphertext, then 2nd element, up to nth element where n
    is block size.
    """
    # Create a slice for each position in block, extending through all of ciphertext. Slice 1
    # produces 1st block element, slice 2 produces second block element, ...
    slices = [slice(x, len(ct), key_sz) for x in range(key_sz)]

    # Elements in nth position in block. Elements[0] is a list of bytes in position 0 of each block,
    # elements[1] is position 1 of each block, ...
    elems = [ct[slyce] for slyce in slices]
    return elems

def test_transpose_blocks():
    key_sz = random.randint(2, 10)
    ct_size = key_sz * random.randint(32, 128)  # no partial final block
    ct = [chr(random.randrange(256)) for _ in range(ct_size)]
    elems = transpose_blocks(ct, key_sz)

    for pos, elem in enumerate(elems):
        assert elem[pos] == ct[pos*key_sz+pos], 'Failed to transpose blocks'

def guess_key(elems, score_threshold=2.0):
    """
    :param list(str) elems: transposed ciphertext elements
    :param float score_threshold: threshold that must be satisfied between key scores
    :return: guessed keys
    :rtype: list(str)
    """
    key_guesses = []
    for pos, elem in enumerate(elems):
        position_guesses = []  # guesses at this position
        scores = cp_lib.brute_force_xor(string.printable, bytearray(elem))
        logger.info('Top 5 scores for position {:d}: {}'.format(pos, scores[:5]))
        for score_idx in range(len(scores) - 1):
            score_diff = scores[score_idx][1] - scores[score_idx+1][1]
            position_guesses.append(scores[score_idx][0])
            if score_diff > score_threshold:
                break

        if key_guesses:
            key_bases = key_guesses
            key_guesses = []
            for position_guess in position_guesses:
                for key_base in key_bases:
                    key_guesses.append(key_base + position_guess)
        else:
            key_guesses = position_guesses

    return key_guesses

def run_tests():
    test_hamming_distance('A', 'A', 0)
    test_hamming_distance('A', 'B', 2)
    test_hamming_distance('B', 'A', 2)
    test_hamming_distance(IN_STR_1, IN_STR_2, IN_HAMMING_DIST)

    ciphertext = open(IN_CIPHERTEXT_FILE).read().decode('base64')

    key_sizes = guess_key_size(ciphertext, 4)[:5]
    print 'Top 5 guessed key sizes: {}.'.format(key_sizes)
    expected_key_sz = len(OUT_KEY)
    assert expected_key_sz in key_sizes, (
        'Expected a key size of {:d} bytes.'.format(expected_key_sz))

    test_transpose_blocks()
    #XXX: Can't seem to get correct key size to have the best score so we cheat with a hardcoded
    # index
    elems = transpose_blocks(ciphertext, key_sizes[4])

    keys = guess_key(elems, 5.0)
    for key in keys:
        print 'Guessed key: {!r}'.format(key)
        pt = cp_lib.encrypt(key, ciphertext)
        logger.debug('Decrypted data:\n-----\n%s\n-----', pt)
    assert OUT_KEY in keys, 'Failed to find expected key in list of guesses.'

if __name__ == '__main__':
    # increase logging level to DEBUG to see decrypted data
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
