import numpy as np
import pdb
st = pdb.set_trace

# Make a graph of cave nodes (won't use libraries)
#
# Create list of cave lists, each of which has a list of connecting cave indices, a 'max_visits' status (large for the big caves), and a 'visits' status. Use indices rather than letters.
# e.g. a cave might have entries [[4,2], 2, 1].
# Would make a class normally, but too lazy

caves = []

cavedict = {}
startcave = 0
endcave = 0

with open("examplefile.txt", "r") as ifile:
# with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        if line[0] == "#":
            continue
        s, e = line.strip().split('-')
        try:
            si = cavedict[s] # start cave index
        except KeyError:
            caves.append([[], 100000 if s.isupper() else 1, False]) # add new cave object
            si = len(caves) - 1 # cave index
            cavedict[s] = si

        try:
            ei = cavedict[e] # end cave index
        except KeyError:
            caves.append([[], 100000 if e.isupper() else 1, False]) # add new cave object
            ei = len(caves) - 1 # cave index
            cavedict[e] = ei

        # add connection between caves
        caves[si][0].append(ei)
        caves[ei][0].append(si)

        if s == 'start':
            startcave = cavedict[s]
            caves[startcave][2] = 1
        elif e == 'end':
            endcave = cavedict[e]
            caves[endcave][2] = 0

# Figure out total paths from start to end
paths_taken = []
paths_left = True

# trial path
cave_indices = [startcave]
trial_indices = [0]
ti = trial_indices
cave = startcave

## Algorithm
# Start at starting cave, and see the range of possibilities.
# Record path trial index 0 for this cave, which corresponds to
valid_paths = []

# optional debugging prints
def dprint(*args, **kwargs):
    if True:
        print(*args, **kwargs)

while cave_indices:
    # start trying paths in the current cave
    next_caves = caves[cave][0]

    # debugging
    dprint(" cave ", cave, " path trial indices ", ti, " next caves ", next_caves, " cave indices ", cave_indices)

    if cave == endcave:
        dprint("Found end cave ", cave)
        valid_paths.append(cave_indices[:])
        caves[cave][-1] -= 1 # clear last cave's presence
        ti.pop()
        cave_indices.pop()
        cave = cave_indices[-1]
        ti[-1] += 1 # try next potential path in case there are more than one from second-last cave
        dprint("Moving back to cave ", cave)
    elif ti[-1] >= len(next_caves):
        dprint("Tried all next caves")
        ti.pop() # exhausted all the paths, go back a cave
        caves[cave][-1] -= 1 # clear last cave's presence
        cave_indices.pop()
        try:
            cave = cave_indices[-1]
        except IndexError: # caves fully explored
            break
        ti[-1] += 1
    else: # still more paths to try at this level
        next_cave_idx = next_caves[ti[-1]]
        next_cave = caves[next_cave_idx]
        if next_cave[-1] == next_cave[1]: # visited max times already
            dprint("Visited cave ", next_cave_idx, " max times already")
            ti[-1] += 1 # try new cave, since can't visit this one again
        else: # move into this cave
            dprint("Moving to cave ", next_cave_idx)
            next_cave[-1] += 1 # record visit if a small cave
            cave = next_cave_idx
            cave_indices.append(cave)
            ti.append(0)

print("Paths found: ", len(valid_paths))
if True:
    for path in valid_paths:
        print(path)
