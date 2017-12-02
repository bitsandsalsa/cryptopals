#!/usr/bin/env python
#
# Convert hex to base64

HEX_STR = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
TARGET_B64 = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

raw = HEX_STR.decode('hex')
b64 = raw.encode('base64').strip()

print 'Hex string: {}'.format(HEX_STR)
print 'Base64: {}'.format(b64)
print 'Target base64: {}'.format(TARGET_B64)
print 'Base64 == Target base64 -> {}'.format(b64 == TARGET_B64)
