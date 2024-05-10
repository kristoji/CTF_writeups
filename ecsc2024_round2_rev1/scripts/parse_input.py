import math

def parse_string(s):
    v5 = 26 * (ord(s[0]) - ord('A')) + ord(s[1]) - ord('A')
    v2 = 3.141592653589793 * ((float(v5) / 675.0 + float(v5) / 675.0))
    angle = float(v2)

    v6 = 26 * (ord(s[2]) - ord('A')) + ord(s[3]) - ord('A')
    v3 = 25.0 * ((float(v6) / 675.0))
    length = float(v3)
    return angle, length

def retrieve_string(angle, length):
    if angle < 0:
        angle += 2*math.pi
    v5 = 675.0 * angle / (2*math.pi)
    v6 = 675.0 * length / 25.0
    s = ''
    s += chr(int(v5 / 26) + ord('A'))
    s += chr(int(v5 % 26) + ord('A'))
    s += chr(int(v6 / 26) + ord('A'))
    s += chr(int(v6 % 26) + ord('A'))
    return s

def retrieve_string_from_pts(start, end):  
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    return retrieve_string(angle, length)