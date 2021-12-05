import numpy as np
import pdb
st = pdb.set_trace

starts, ends = [], []

with open("inputfile.txt", "r") as ifile:
# with open("test.txt", "r") as ifile:
    for line in ifile:
        pairs = line.strip().split('->')
        start, end = ( (int(m) for m in k.split(',')) for k in pairs)
        starts.append(tuple(start))
        ends.append(tuple(end))
        # starts.append(pairs[0]

# Nummpyify the data
starts, ends = np.array(starts), np.array(ends)

grid = np.zeros([np.max(starts) + 2, np.max(ends) + 2], dtype=int)

# part 2 of the challenge or not -- count diagonals
part2 = True

for sta, end in zip(starts, ends):
    if sta[0] == end[0]: # vertical
        a, b = np.min([sta[1], end[1]]), np.max([sta[1], end[1]])
        grid[sta[0], a : b + 1] += 1
    elif sta[1] == end[1]: # horizontal
        a, b = np.min([sta[0], end[0]]), np.max([sta[0], end[0]])
        grid[a : b + 1, sta[1]] += 1
    elif part2:
        ## ugly -- but quick. Could use this code for the other two cases too.
        if sta[0] > end[0]:
            xran = range(sta[0], end[0] - 1, -1)
        else:
            xran = range(sta[0], end[0] + 1)

        if sta[1] > end[1]:
            yran = range(sta[1], end[1] - 1, -1)
        else:
            yran = range(sta[1], end[1] + 1)

        for x, y in zip(xran, yran):
            grid[x, y] += 1 # ugly

print(grid.T)

import matplotlib.pyplot as plt
plt.imshow(grid.T); plt.show()

print("Overlapping points: ", np.sum(grid > 1))
