from string import ascii_uppercase
from pwn import *
from itertools import product

# we will bruteforce the length assuming the direction is correct
# 
# paste your solution made with solve_maze.py
# and delete the last 2 characters
s = 'SPXMRMQLQWSWQXWTQMQSWERJYDQHTYLSOZSAGYOINDKKQIYQKFGUEJOUFXUTQAPHPXMRHRZBIJZJIENYOCFNTLSGSYQONYLUUCKNBEOABA'

for c in product(ascii_uppercase, ascii_uppercase):
    c = ''.join(c)
    r = process(['../utils/FPFC'])
    r.sendline((s+c).encode())
    r.recvline()
    r.recvline()
    r.recvline()
    try:
        if b'Congratulations' in r.recvline():
            print("Result:")
            print(s+c)
            exit()
    except EOFError:
        r.close()
        log.info(f'=> {c} failed')
        continue
    r.interactive()
    exit()
