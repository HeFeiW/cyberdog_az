# main.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from data_module import get_data

# Create a figure and axes
fig, ax = plt.subplots()

# Create a line object. This will be updated in the animation.
line, = ax.plot([], [], 'o')

# Initialization function for the animation
def init():
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return line,

# Update function for the animation
def update(frame):
    x, y = get_data()
    line.set_data(x, y)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(100), init_func=init, blit=True)

plt.show()