import pyglet
from grid import Grid
from flow import Flow
import generator
from math import floor
from random import random
import sys

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_ORIGIN = (50, 50)
GRID_WIDTH = WINDOW_WIDTH - 2 * GRID_ORIGIN[0]
GRID_HEIGHT = WINDOW_HEIGHT - 2 * GRID_ORIGIN[1]

DEFAULT_ROWS = 5
DEFAULT_COLS = 5

# get the grid dimensions from the command line arguments
try:
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])

except ValueError:
    print("Grid dimensions must be integers; using a 5x5 grid by default")
    rows, cols = DEFAULT_ROWS, DEFAULT_COLS

except IndexError:
    if len(sys.argv) == 1:
        print("No dimensions provided; using a 5x5 grid by default")
        rows, cols = DEFAULT_ROWS, DEFAULT_COLS
    else:
        cols = rows

# create the window and the grid
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
grid = Grid(    GRID_ORIGIN,
                GRID_WIDTH,
                GRID_HEIGHT,
                rows,
                cols,
                (179, 179, 179),
                thickness = 5.0,    )

paths = generator.generateFlows(grid)

# make sure all cells in the list of paths are unique
flatten = lambda multi : [x for arr in multi for x in arr]
assert len(flatten(paths)) == len(set(flatten(paths)))

flows = []
for path in paths:
    flows.append(   Flow(   grid,
                            [ floor(random() * 256) for x in range(3) ],
                            len(flows),
                            path = path   )  )

# update all the flows' graphics so they can be drawn
for flow in flows:
    flow.updateGraphics()

@window.event
def on_draw():
    grid.draw()

    for flow in flows:
        flow.draw()

pyglet.app.run()
