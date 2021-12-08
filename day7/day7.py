import numpy as np
import pdb
st = pdb.set_trace

from input import real_input
test_input = np.array([16,1,2,0,4,2,7,1,2,14], dtype=int)

def distance(hole, crab_locations):
    return np.abs(crab_locations - hole).sum()

def get_min(crab_locations, part2=False):
    if part2:
        c = crab_locations
        # triangular numbers: triangular number n is n(n+1)/2 --
        # somehow remembered this from high school!
        dists = np.array([(np.abs(crab_locations - k) * (np.abs(crab_locations - k) + 1) // 2).sum() for k in range(np.max(crab_locations))])
    else:
        dists = np.array([np.abs(crab_locations - k).sum() for k in range(np.max(crab_locations))])

    mindist = np.where(dists == dists.min() )[0]
    fuel = dists[mindist]
    return mindist, fuel

# horiz_pos = get_min(real_input)
horiz_pos, fuel = get_min(real_input, part2=True)

print("Horiz pos: ", horiz_pos, "fuel: ", fuel)
