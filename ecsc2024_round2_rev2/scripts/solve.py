import subprocess
from out import screen_out
from screen_in import screen_in

def execute_z3_solve_next_two(offset, list_values):
    cmd = "python3 z3_solve_next_two.py " + str(offset) + " " + " ".join([str(x) for x in list_values])
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    output = output.decode("utf-8")
    output = output.split("\n")[1].split(", ")
    return output

def execute_check_next_zeros():
    cmd = "python3 check_next_are_zeros.py"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    output = output.decode("utf-8")
    return "Success\n" in output


with open("result.py", "w") as f:
        f.write("result = []")

# first 800 hex_char (= 400 bytes = 100 _DWORD) are the same
OFFSET = 100
result = list(map(str, screen_in[:OFFSET]))

# sub_600
VALUES = [140050, 6267691, 5949456, 4919]

# last known values after OFFSET
prev = [3983684781, 1999312935]

for i in range(0, 1024-OFFSET, 2):

    # print the prev encryption
    print(i + OFFSET - 2, end="\t")
    for v in prev:
        print(hex(v), end="\t")
    print()

    if execute_check_next_zeros():
        next_two = ['0x0', '0x0']

    else:
        next_two = execute_z3_solve_next_two(OFFSET+i, prev + VALUES)

    result += next_two
    prev = [screen_out[OFFSET+i], screen_out[OFFSET+i+1]]
    
    with open("result.py", "w") as f:
        f.write("result = [" + ", ".join(result) + "]")


# write the result in a byte array
screen_pl = []
for x in result:
    x = int(x, 16)
    for i in range(4):
        screen_pl.append((x >> (8 * i)) & 0xff)

with open("screen_pl.py", "w") as f:
    f.write("screen_pl = [" + ", ".join([str(x) for x in screen_pl]) + "]")