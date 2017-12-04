#!/usr/bin/env python
#
# Break repeating-key XOR

import collections
import logging
import string
from pprint import pprint

import cp_lib
from challenge_3 import brute_force_xor


IN_STR_1 = 'this is a test'
IN_STR_2 = 'wokka wokka!!!'
IN_HAMMING_DIST = 37
IN_CIPHERTEXT_FILE = '6.txt'

KEY_SIZE_RANGE = (2, 65)

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
    logging.info('Test case. Hamming distance.')
    distance = calc_hamming_distance(s1, s2)
    assert expected_distance == distance, (
        'Incorrect Hamming distance s1: "{}", s2: "{}" -> {}; Expected {}'.format(s1, s2, distance, expected_distance))

def guess_key_size(ct):
    logging.info('Guess key size between %d and %d bytes.', *KEY_SIZE_RANGE)
    norm_distances = {}
    for key_sz in range(*KEY_SIZE_RANGE):
        hamming_distance = calc_hamming_distance(ct[0:key_sz], ct[0+key_sz:key_sz*2])
        norm_distances.update({key_sz: hamming_distance / key_sz})
    sorted_guesses = sorted(norm_distances.items(), key=lambda x: x[1])
    logging.info('Top 5 guesses: %s', [sz for sz, dist in sorted_guesses[:5]])
    return sorted_guesses[0][0]

def run_tests():
    logging.basicConfig(level=logging.INFO)

    test_hamming_distance('A', 'A', 0)
    test_hamming_distance('A', 'B', 2)
    test_hamming_distance('B', 'A', 2)
    test_hamming_distance(IN_STR_1, IN_STR_2, IN_HAMMING_DIST)

    key_sz = guess_key_size(open(IN_CIPHERTEXT_FILE).read().decode('base64'))
    logging.info('Guessed key size: %d', key_sz)

#run_tests()
#print 'Success'

def transpose_blocks(ct, key_sz):
    """
    Transpose 1st element of each block in ciphertext, then 2nd element, up to nth element where n
    is block size.
    """
    # Create a slice for each position in block, extending through all of ciphertext. Slice 1
    # produces 1st element, slice 2 produces second element, ...
    slices = [slice(x, len(ct), key_sz) for x in range(key_sz)]

    # Elements in nth position in block. Elements[0] is a list of bytes in position 0 of each block,
    # elements[1] is position 1 of each block, ...
    elems = [ct[slyce] for slyce in slices]

    for elem in elems:
        for block_idx in range(0, len(elem), key_sz):
            top_scores = brute_force_xor(string.ascii_letters,
                                         bytearray(elem[block_idx:block_idx+key_sz]))
            logging.info('Top {} scores: {}'.format(len(top_scores), top_scores))

key_sz = guess_key_size(open(IN_CIPHERTEXT_FILE).read().decode('base64'))
transpose_blocks(open(IN_CIPHERTEXT_FILE).read().decode('base64'), key_sz)
