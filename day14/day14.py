import numpy as np
import pdb
st = pdb.set_trace

polymer = None
transforms = {}
letters = []

# with open("examplefile.txt", "r") as ifile:
with open("inputfile.txt", "r") as ifile:
    polymer = ifile.readline().strip()
    ifile.readline() # skip the newline
    for line in ifile:
        pair, sub = line.strip().split(" -> ")
        transforms[pair] = sub
        if sub not in letters:
            letters.append(sub) # assume that every letter is produced by some transformation rule

orig_polymer = polymer # copy

for k in range(10):
    newpol = polymer
    m = 1
    for a, b in zip(polymer[:-1], polymer[1:]):
        # ugly but easy
        pair = a + b
        try:
            sub = transforms[pair]
            newpol = newpol[:m] + sub + newpol[m:]
            m += 2
        except KeyError:
            m += 1

    polymer = newpol

    # print(len(polymer))

def count_letters(stri):
    minc = 1000000000
    minl = ''
    maxc = 0
    maxl = ''

    for k in letters:
        count = len( list( filter( lambda m: m == k, stri ) ) )
        if count < minc:
            minc = count
            minl = k
        if count > maxc:
            maxc = count
            maxl = k

    return minc, maxc, minl, maxl

minc, maxc, _, _ = count_letters(polymer)

print("[OLD APPROACH, NOT IN USE] Min/max/diff: ", minc, maxc, maxc - minc)

## Part 2 -- the above approach is too inefficient
#
# Observation: every pair of characters either matches a rule, in
# which case two new pairs are created (i.e. 'NN' -> 'NCN' which is
# 'NC' and 'CN') or they don't. Don't need the full strings, only a
# count of the pairs present and the mappings at each stage. This
# feels like a vector-matrix multiplication could do it.
#
# First, go through and create a vector of NxN letter pairs
pairsv = []
for a in letters:
    for b in letters:
        pairsv.append(a+b)

polymern = np.zeros([len(pairsv), 1], dtype=int)
for a, b in zip(orig_polymer[:-1], orig_polymer[1:]):
    try:
        polymern[pairsv.index(a+b)] += 1
    except IndexError:
        pass

# construct the polymerisation matrix
polmat = np.zeros([len(pairsv), len(pairsv)], dtype=int)
for k in transforms:
    old_idx = pairsv.index(k)
    lett = transforms[k]
    newa, newb = pairsv.index(k[0] + lett), pairsv.index(lett + k[1])
    polmat[newa, old_idx] = 1
    polmat[newb, old_idx] = 1

# take the 40th power
polmatn = polmat[:]
poww = 40
for k in range(poww - 1):
    polmatn = polmatn @ polmat

# Produce final polymer vector
polymern_final = polmatn @ polymern
# polymern_final = polymern

# Count letters
counts = np.zeros_like(letters, dtype=int)
for k in np.nonzero(polymern_final[:,0])[0]:
    ab = pairsv[k]
    paircnt = polymern_final[k]
    for a in ab:
        counts[letters.index(a)] += paircnt

# avoid counting letters twice + add on first and last letters in the
# polymer
counts_corr = counts // 2
counts_corr[letters.index(orig_polymer[0])] += 1
counts_corr[letters.index(orig_polymer[-1])] += 1

diff = counts_corr.max() - counts_corr.min()
print("Diff: ", diff)
