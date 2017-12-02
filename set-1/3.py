#!/usr/bin/env python
#
# Single-byte XOR cipher

import collections
import string

XOR_RESULT = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
FREQ = {'E': 12.02,
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
freq_list = sorted(FREQ.items(), None, lambda x:x[1])
freq_by_letter, _ = zip(*freq_list)

raw_result = bytearray(XOR_RESULT.decode('hex'))

in_order_list = []
for key in string.ascii_letters:
    print '+++Trying key "{}"+++'.format(key)
    tmp_result = [chr(ord(key) ^ raw_byte) for raw_byte in raw_result]  # try key
    print 'XOR : {!r}'.format(tmp_result)
    result = [b.upper() for b in tmp_result if b.isalpha()]  # filter valid ASCII and store as uppercase
    print 'XOR then filtered for valid ASCII then uppercased: {}'.format(result)
    letters_from_attempt = list(zip(*collections.Counter(result).most_common())[0])[::-1]  # from least common to most
    print 'Ordered from least common to most: {}'.format(letters_from_attempt)
    in_order_cnt = 0
    for a in freq_by_letter:
        if a == letters_from_attempt[-1]:
            in_order_cnt += 1
            letters_from_attempt.pop()
    print 'Number of letters in order: {}'.format(in_order_cnt)
    in_order_list.append(in_order_cnt)

print
print 'Summary of in order letters for each attempted key:'
print sorted(zip(string.ascii_letters, in_order_list), None, lambda x:x[1])
