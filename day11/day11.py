import numpy as np
import pdb
st = pdb.set_trace

numlist = []

# with open("examplefile.txt", "r") as ifile:
with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        lis = line.strip()
        numlist.append([int(l) for l in lis])


energies = np.array(numlist)

# testing
# energies = np.array([[7, 9, 5], [0, 0, 0], [0, 0, 0]])

energies_h = np.hstack([ energies[:,[0]], energies, energies[:,[-1]] ])
energies_pad = np.vstack([ energies_h[[0],:], energies_h, energies_h[[-1],:] ]) # padded edges
en = energies_pad

def clear_edges():
    # make sure padded edges can never flash
    en[:,[0, -1]] = 0
    en[[0, -1],:] = 0

clear_edges()

steps = 1000

## Ugly but easy
offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

flashes = []
sync_flashes = []

for ste in range(steps):
    en += 1
    flashed = en > 9
    flashed_sum = flashed

    while flashed.any():
        for y, x in zip(*np.where(flashed)):
            en[y, x] = 0
            for offs in offsets:
                en[y + offs[1], x + offs[0]] += 1

        flashed = en > 9
        flashed_sum += flashed

    en[flashed_sum != 0] = 0
    clear_edges()

    if False:
        print("Round ", ste + 1)
        print(flashed_sum.astype(int))

    flashes.append(flashed_sum.sum())

    if np.all(flashed_sum[1:-1, 1:-1]):
        sync_flashes.append(ste)

print("Total flashes: ", np.array(flashes).sum())
print("Rounds when synced: ", np.array(sync_flashes) + 1)
