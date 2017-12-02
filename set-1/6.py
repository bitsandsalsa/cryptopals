#!/usr/bin/env python
#
# Break repeating-key XOR

import collections
import string

from pprint import pprint


TEST_STR_1 = 'this is a test'
TEST_STR_2 = 'wokka wokka!!!'
TEST_HAMMING_DIST = 37
CIPHERTEXT_FILE = '6.txt'

def calc_hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise RuntimeError('Strings must be of equal length.')

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

def test(s1, s2, expected_distance):
    distance = calc_hamming_distance(s1, s2)
    assert expected_distance == distance, (
        'Incorrect Hamming distance s1: "{}", s2: "{}" -> {}; Expected {}'.format(s1, s2, distance, expected_distance))

def run_tests():
    test('A', 'A', 0)
    test('A', 'B', 2)
    test('B', 'A', 2)
    test(TEST_STR_1, TEST_STR_2, TEST_HAMMING_DIST)

#run_tests()

def guess_key_size(ct):
    norm_distances = {}
    for key_sz in range(2, 65):
        hamming_distance = calc_hamming_distance(ct[0:key_sz], ct[0+key_sz:key_sz*2])
        norm_distances.update({key_sz: hamming_distance / key_sz})
    sorted_guesses = sorted(norm_distances.items(), None, lambda x: x[1])
    pprint(sorted_guesses)
    print 'Guessed key size: {}'.format(sorted_guesses[0][0])

#guess_key_size(open(CIPHERTEXT_FILE).read().decode('base64'))

#TODO
def char_histogram(s):
    counter = collections.Counter(s)

def brute_force_xor(ct, keys):
    """
    Try each key against ciphertext.
    """
    for key in keys:
        pt = map(chr, [ord(key) ^ ord(ct[byte_idx]) for byte_idx in range(0, len(ct), len(key))])
        char_histogram(pt)
        print 'Key: {} -> {!r}'.format(key, pt[:128])

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
            brute_force_xor(elem[block_idx:block_idx+key_sz], string.ascii_letters)

#brute_force_xor(open(CIPHERTEXT_FILE).read().decode('base64'), string.ascii_letters)
transpose_blocks(open(CIPHERTEXT_FILE).read().decode('base64'), 5)
