#!/usr/bin/env python
#
# Single-byte XOR cipher

import collections
import logging
import string


OUT_CIPHERTEXT_HEX_STR = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
OUT_PLAINTEXT_STR = "Cooking MC's like a pound of bacon"
FREQ_MAP = {'E': 12.02,
        'T': 9.10,
        'A': 8.12,
        'O': 7.68,
        'I': 7.31,
        'N': 6.95,
        'S': 6.28,
        'R': 6.02,
        'H': 5.92,
        'D': 4.32,
        'L': 3.98,
        'U': 2.88,
        'C': 2.71,
        'M': 2.61,
        'F': 2.30,
        'Y': 2.11,
        'W': 2.09,
        'G': 2.03,
        'P': 1.82,
        'B': 1.49,
        'V': 1.11,
        'K': 0.69,
        'X': 0.17,
        'Q': 0.11,
        'J': 0.10,
        'Z': 0.07}
NUM_HIGHEST_SCORES = 5

def score_text(s):
    score = 0
    counter = collections.Counter(s.upper())
    for byte, count in counter.items():
        try:
            score += FREQ_MAP[byte] * count
        except KeyError:
            # ignore unrecognized bytes
            pass
    return score

def brute_force_xor(keys, ciphertext_bytes):
    scores = {}
    for key in keys:
        pt_str = ''.join([chr(ord(key) ^ byte) for byte in ciphertext_bytes])
        scores[key] = score_text(pt_str)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:NUM_HIGHEST_SCORES]

def test(keys, ciphertext_hex_str, plaintext_str):
    logging.info('Test case. Decrypt with guessed keys.')

    ciphertext_bytes = bytearray(ciphertext_hex_str.decode('hex'))
    top_scores = brute_force_xor(keys, ciphertext_bytes)
    logging.info('Top {} scores: {}'.format(len(top_scores), top_scores))
    for key, _ in top_scores:
        decrypted_plaintext = ''.join([chr(ord(key) ^ byte) for byte in ciphertext_bytes])
        if decrypted_plaintext == plaintext_str:
            print 'Found key: {}'.format(key)
            break
    else:
        raise AssertionError('Failed to guess a key.')

def run_tests():
    logging.info('Trying each ASCII letter as a key.')
    test(string.ascii_letters, OUT_CIPHERTEXT_HEX_STR, OUT_PLAINTEXT_STR)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_tests()
    print 'Success'
