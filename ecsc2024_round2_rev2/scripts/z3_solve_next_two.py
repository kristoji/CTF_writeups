#!/usr/bin/env python3
import sys
from z3 import *
from out import screen_out

def ror(value, bits):
    value &= 0xFFFFFFFF
    return (LShR(value, bits) | (value << (32 - bits))) & 0xFFFFFFFF

# sub_4AC
def encrypt(a1, a2):

    # sub_614
    VALUES[0] = a1
    VALUES[1] = a2

    for i in range(10):

        # sub_630
        VALUES[0] ^= i ^ VALUES[(i & 1) + 2]
        VALUES[1] ^= VALUES[(i & 1) + 3]

        # sub_660
        v1, v2, v3, v4 = 0, 0, 0, 0

        VALUES[0] += ror(VALUES[1], 31)
        VALUES[0] &= 0xFFFFFFFF
        VALUES[1] ^= ror(VALUES[0], 24)
        index = i - ((((0xCCCCCCCD * i) >> 32) & 0xFFFFFFFC) + i // 5)
        v1 = LOOKUP[index % len(LOOKUP)]
        VALUES[0] ^= v1
        v2 = VALUES[0] + ror(VALUES[1], 17)
        v2 &= 0xFFFFFFFF
        VALUES[1] ^= ror(v2, 17)
        v3 = (v2 ^ v1) + VALUES[1]
        v3 &= 0xFFFFFFFF
        VALUES[1] ^= ror(v3, 31)
        v4 = (v3 ^ v1) + ror(VALUES[1], 24)
        v4 &= 0xFFFFFFFF
        VALUES[1] ^= ror(v4, 16)
        VALUES[0] = v1 ^ v4
    
    # sub_630
    VALUES[0] ^= VALUES[2]
    VALUES[1] ^= VALUES[3]

    # sub_620
    return VALUES[0], VALUES[1]

# sub_504: main_loop
def main_loop(screen_in):

    prev = VALUES[0:2]
    
    for i in range(0, len(screen_in), 2):
        screen_in[i] ^= prev[0]
        screen_in[i + 1] ^= prev[1]

        prev[0], prev[1] = encrypt(screen_in[i], screen_in[i + 1])

        screen_in[i] = prev[0]
        screen_in[i + 1] = prev[1]

    return screen_in


OFFSET = int(sys.argv[1])

# sub_600
VALUES = [int(x) for x in sys.argv[2:8]]
LOOKUP = [3084996962, 3211876480, 951376470, 844003128, 3138487787]


# I only need the next 2 VALUES
LN = 2

screen_plain = [BitVec(f"screen_plain_{i}", 32) for i in range(LN)]
screen_cp = [x for x in screen_plain]
screen_enc = main_loop(screen_cp)

s = Solver()
for i in range(LN):
    s.add(screen_enc[i] == screen_out[i + OFFSET])

if s.check() == sat:
    print("SAT!")
    m = s.model()
    print(", ".join([hex(m[screen_plain[i]].as_long()) for i in range(LN)]))

else:
    print("NO SAT!")