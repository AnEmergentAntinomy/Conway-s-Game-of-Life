import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
EMPTY, NEW_CELL, LIVING_CELL, DEAD_CELL = 0, 1, 2, 3
# Colours for visualization: brown for EMPTY, dark green for NEW CELLS and orange
# for LIVING_CELLS. Note that for the colormap to work, this list and the bounds list
# must be one larger than the number of different values in the array.
colors_list = [(0.2,0,0), (0,0.5,0), 'yellow', 'orange', 'red']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

show_new = False
show_dead = False

def iterate(X):
    """Iterate the forest according to the forest-fire rules."""

    # The boundary of the grid is always empty, so only consider cells
    # indexed from 1 to nx-2, 1 to ny-2
    X1 = np.zeros((ny, nx))
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            alive_neighbors = 0
            for dx,dy in neighbourhood:
                if X[iy+dy,ix+dx] == NEW_CELL or X[iy+dy,ix+dx] == LIVING_CELL:
                    alive_neighbors += 1
            if X[iy,ix] == NEW_CELL or X[iy,ix] == LIVING_CELL:
                if alive_neighbors == 2 or alive_neighbors == 3:
                    X1[iy,ix] = LIVING_CELL
                else:
                    if show_dead == True:
                        X1[iy,ix] = DEAD_CELL
            if X[iy,ix] == EMPTY or X[iy,ix] == DEAD_CELL:
                if alive_neighbors == 3:
                    if show_new == True:
                        X1[iy,ix] = NEW_CELL
                    else:
                        X1[iy,ix] = LIVING_CELL
                else:
                    X1[iy,ix] = EMPTY

    return X1

# The initial fraction of the grid occupied by cells.
grid_fraction = 0.33
# Forest size (number of cells in x and y directions).
nx, ny = 32, 32
# Initialize the forest grid.
X  = np.zeros((ny, nx))
X[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
X[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < grid_fraction

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)#, interpolation='nearest')

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X

# Interval between frames (ms).
interval = 100
anim = animation.FuncAnimation(fig, animate, interval=interval)
plt.show()
