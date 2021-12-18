import numpy as np
import pdb
st = pdb.set_trace

numlist = []

# with open("examplefile.txt", "r") as ifile:
with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        lis = line.strip()
        numlist.append([int(l) for l in lis])

heights = np.array(numlist)

heights_h = np.hstack([ heights[:,[0]], heights, heights[:,[-1]] ])
heights_pad = np.vstack([ heights_h[[0],:], heights_h, heights_h[[-1],:] ]) # padded edges
p = heights_pad

# kernel = np.array([[0,1,0],[1,1,1],[0,1,0]])

heights_min = np.zeros_like(heights)

rows, cols = heights.shape

## Ugly but easy
offsets = [(0,1), (1,0), (1,1), (1,2), (2,1)]

for r in range(rows):
    for c in range(cols):
        vals = np.array([ p[a + r, b + c] for a, b in offsets ])

        if np.all(vals == vals[0]): # avoid peak plateaus
            continue

        heights_min[r, c] = vals.min()

mins = np.array(heights == heights_min, dtype=int)

## debugging
if False:
    import matplotlib.pyplot as plt
    ## continue here with something like
    for k in range(2):
        plt.plot(heights[k])
        plt.plot(mins[k], ':')

    # plt.legend(['0','m0','1','m1','2','m2'])
    plt.legend(['0','m0','1','m1'])
    plt.show()

if False:
    import matplotlib.pyplot as plt
    # offset = np.zeros_like(heights)
    # offset[0][0] = 15
    # plt.imshow(heights + offset)
    # plt.figure()
    # plt.imshow(heights + mins * 15)
    plt.imshow(heights)
    plt.show()

min_points = heights == heights_min
risk_levels = ( min_points + 1 ).sum()
print("Part a: ", risk_levels.sum())

## Part 2: finding basins
# Had to look up https://en.wikipedia.org/wiki/Flood_fill for inspiration (to see if there was an easier way than what I'm doing below)

basins_y, basins_x = np.where(min_points)

# deepest point coordinates
basin_sizes = []
counted = heights == 9 # keep track of which locations have already been included, or can never be included

def add_basin_neighbours(coord):
    x, y = coord
    # print("Adding ", x, y)
    xd, xu = x - 1, x + 1
    yd, yu = y - 1, y + 1
    count = 0
    pts = []

    # add basin neighbours to be counted
    for xx, yy in zip([x, xd, x, xu], [yu, y, yd, y]):
        if xx < 0 or xx == cols or yy < 0 or yy == rows:
            continue # don't go outside boundary of board

        if not counted[yy, xx]:
            pts.append( (xx, yy) )
            count += 1
            counted[yy, xx] = True

    return count, pts

for x, y in zip(basins_x, basins_y):
    xl, yl = x, y # current point
    basin_size = 1
    counted[yl, xl] = True
    uncounted_pts = [ (xl, yl) ]

    while uncounted_pts: # nonzero
        loc_count, loc_pts = add_basin_neighbours( uncounted_pts.pop() )
        basin_size += loc_count
        uncounted_pts += loc_pts

    basin_sizes.append(basin_size)

print("Part b: ", np.array(sorted(basin_sizes)[-3:]).prod() )
