#!/usr/bin/env python3

from screen_in import screen_in
from result import result
from out import screen_out

LOOKUP = [3084996962, 3211876480, 951376470, 844003128, 3138487787]
VALUES = [0, 0, 0x22312, 0x5FA32B, 0x5AC810, 0x1337]


def ror(value, bits):
    value &= 0xFFFFFFFF
    return ((value >> bits) | (value << (32 - bits))) & 0xFFFFFFFF

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
        VALUES[1] &= 0xFFFFFFFF
        index = i - ((((0xCCCCCCCD * i) >> 32) & 0xFFFFFFFC) + i // 5)
        v1 = LOOKUP[index % len(LOOKUP)]
        VALUES[0] ^= v1
        VALUES[0] &= 0xFFFFFFFF
        v2 = VALUES[0] + ror(VALUES[1], 17)
        v2 &= 0xFFFFFFFF
        VALUES[1] ^= ror(v2, 17)
        VALUES[1] &= 0xFFFFFFFF
        v3 = (v2 ^ v1) + VALUES[1]
        v3 &= 0xFFFFFFFF
        VALUES[1] ^= ror(v3, 31)
        VALUES[1] &= 0xFFFFFFFF
        v4 = (v3 ^ v1) + ror(VALUES[1], 24)
        v4 &= 0xFFFFFFFF
        VALUES[1] ^= ror(v4, 16)
        VALUES[1] &= 0xFFFFFFFF
        VALUES[0] = v1 ^ v4
        VALUES[0] &= 0xFFFFFFFF

    # sub_630    
    VALUES[0] ^= VALUES[2]
    VALUES[1] ^= VALUES[3]

    # sub_620
    return VALUES[0], VALUES[1]

# sub_504: main_loop
def main_loop(screen_in):

    prev = [0, 0]
    
    for i in range(0, len(screen_in), 2):
        screen_in[i] ^= prev[0]
        screen_in[i + 1] ^= prev[1]

        prev[0], prev[1] = encrypt(screen_in[i], screen_in[i + 1])

        screen_in[i] = prev[0]
        screen_in[i + 1] = prev[1]

    return screen_in


# We add [0,0] to the current result to compare the last two values of the encrypted screen
screen_pl = result + [0,0]
screen_enc = main_loop(screen_pl)

if screen_enc[-2:] == screen_out[len(screen_pl)-2:len(screen_pl)]:
    print("Success")
else:
    print("Wrong")
    print(list(map(hex, screen_enc[-2:])))
    print(list(map(hex, screen_out[len(screen_pl)-2:len(screen_pl)])))