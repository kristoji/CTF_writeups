from maze import maze
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from parse_input import retrieve_string_from_pts

fig, ax = plt.subplots()
for i, (a, b) in enumerate(maze):
    plt.plot([a[0], b[0]], [a[1], b[1]], '-', label=f'line {i}')

curr = [100, 90]
plt.plot(curr[0], curr[1], 'o', label='start')

circle = Circle((curr[0], curr[1]), 25, color='r', fill=False)
ax.add_artist(circle)

plt.axis('equal')
plt.xlim(curr[0]-50, curr[0]+50)
plt.ylim(curr[1]-50, curr[1]+50)

def onclick(event):
    circle.set_center((event.xdata, event.ydata))
    update_curr(event.xdata, event.ydata)
    fig.canvas.draw()

def update_curr(x, y):
    global curr
    with open('output.txt', 'a') as f:
        # f.write()
        # write the points
        f.write(f'{curr[0]} {curr[1]}\n')
    plt.plot([curr[0], x], [curr[1], y], 'o-')
    print(retrieve_string_from_pts(curr, [x, y]), end='')
    curr[0] = x
    curr[1] = y
    plt.xlim(curr[0]-50, curr[0]+50)
    plt.ylim(curr[1]-50, curr[1]+50)
    plt.plot(curr[0], curr[1], 'o', label='start')



fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

print()

