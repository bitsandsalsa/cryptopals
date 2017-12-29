#!/usr/bin/env python
#
# Detect single-character XOR

import logging
import string

import cp_lib


IN_CIPHERTEXT_FILE = '4.txt'

OUT_LINE_IDX = 170
OUT_KEY = '5'
OUT_PLAINTEXT = 'Now that the party is jumping\n'

logger = logging.getLogger(__name__)

def guess_key(ct, score_threshold=2.0):
    key_guesses = []
    scores = cp_lib.brute_force_xor([chr(x) for x in range(256)], bytearray(ct))
    logger.info('Top 5 scores: {}'.format(scores[:5]))
    for score_idx in range(len(scores) - 1):
        score_diff = scores[score_idx][1] - scores[score_idx+1][1]
        key_guesses.append(scores[score_idx])
        if score_diff > score_threshold:
            break
    return key_guesses

def run_tests():
    key_guesses = []  # list of tuples (line idx, key, score, plaintext)
    for line_idx, line in enumerate(open(IN_CIPHERTEXT_FILE).readlines()):
        ciphertext = line.strip().decode('hex')
        key, score = guess_key(ciphertext, 5.0)[0]  #XXX: top key only
        pt = cp_lib.repeating_key_xor(key, ciphertext)
        key_guesses.append((line_idx, key, score, pt))

    top_guesses = sorted(key_guesses, key=lambda x:x[2], reverse=True)
    print 'Top 5 guesses'
    for line_idx, key, score, pt in top_guesses[:5]:
        print 'line idx: {:d}, key: {}, score: {:f}, plaintext: {!r}'.format(
            line_idx,
            key,
            score,
            pt)
    top_line_idx = top_guesses[0][0]
    top_key = top_guesses[0][1]
    top_pt = top_guesses[0][3]
    assert (OUT_LINE_IDX, OUT_KEY, OUT_PLAINTEXT) == (top_line_idx, top_key, top_pt), (
        'Failed to find key to decrypt one of the lines to an ASCII string.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    run_tests()
    print 'Success'
