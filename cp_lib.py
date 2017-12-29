from set_1.challenge_3 import brute_force_xor
from set_1.challenge_5 import repeating_key_xor

class CPValueError(Exception):
    pass

def iter_over_blocks(data, block_sz):
    for i in xrange(0, len(data), block_sz):
        yield data[i:i+block_sz]
