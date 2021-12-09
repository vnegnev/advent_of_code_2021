import numpy as np
import pdb
st = pdb.set_trace

# 7 segments
# start: each input letter (a - g) maps to a - g
# with each revealed pattern, rule out some mappings
#
# 0: 6 segments a, b, c, e, f, g
# 1: 2 segments c, f
# 2: 5 segments a, c, d, e, g
# 3: 5 segments a, c, d, f, g
# 4: 4 segments b, c, d, f
# 5: 5 segments a, b, d, f, g
# 6: 6 segments a, b, d, e, f, g
# 7: 3 segments a, c, f
# 8: 7 segments a, b, c, d, e, f, g
# 9: 6 segments a, b, c, d, f, g
#
# Reasonable logic: '8' gives no information,
# #1 (2 segments) tells us which segments are c and f
# #7 (3 segments, 2 shared with #1) tells us segment a (which is not in #1)
# #3 (5 segments, 3 shared with #7) tells us segments d and g (which are not in #7)
# #4 (4 segments, 3 shared with #3) tells us segments b and d (which are not in #1, and d is also in #3), and g is then known from #3
# (interlude: know segments a, b, d, g)
# 5 (5 segments, including a, b, d, g) tells us segment f by elimination
# (know segments a, b, d, f, g)
# 1 (2 segments) tells us c by elimination
# by elimination, know segment e

# original combo: replace with strings of digits 0 -> 6, since it's easier to handle than a->g with arrays
# correct_strings = [ na([0, 1, 2, 4, 5, 6]) ]
correct_strings = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

# test algorithm
unknown_strings = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']


## helper functions

def str_withlen(slist, L):
    return [a for a in slist if len(a) == L]

def shared_string(substr, string):
    # return letters shared by substr and string
    inst = ''.join([lett for lett in substr if lett in string])
    return inst

def not_shared_string(substr, string):
    # return letters in substr which are not in string
    inst = ''.join([lett for lett in substr if not lett in string])
    return inst

## main logic

def figure_out_coding(strings_unsrt):
    strings = [''.join(sorted(a)) for a in strings_unsrt] # sort each string alphabetically
    # convenience
    d1 = str_withlen(strings, 2)[0] # digit 1
    d7 = str_withlen(strings, 3)[0] # digit 7

    # which letter of d7 isn't in d1
    sa = not_shared_string(d7, d1)

    # 5-character strings
    d235 = [a for a in strings if len(a) == 5]
    d3 = [ a for a in d235 if shared_string(d7, a) == d7 ][0] # digit 3
    sdg = not_shared_string(d3, d7) # segments d and g

    # 4-character strings
    d4 = str_withlen(strings, 4)[0]
    sbd = not_shared_string(d4, d1) # segments b and d
    sd = shared_string(sbd, sdg) # segment d
    sg = not_shared_string(sdg, sd)
    sb = not_shared_string(sbd, sd)

    # digit 5
    sabdg = sa + sb + sd + sg
    d5 = [a for a in d235 if shared_string(sabdg, a) == sabdg][0]
    sf = not_shared_string(d5, sabdg)

    # digit 1 again
    sc = not_shared_string(d1, sf)

    # and by elimination:
    sabcdfg = sa + sb + sc + sd + sf + sg
    d8 = 'abcdefg'
    se = not_shared_string(d8, sabcdfg)

    # Decoding map
    return {sa: 'a', sb: 'b', sc: 'c', sd: 'd', se: 'e', sf: 'f', sg: 'g'}

def decode(strings, decmap):
    decstrings = []
    for s in strings:
        decstrings.append(''.join(sorted([decmap[a] for a in s])))

    return decstrings

digmap = {'abcefg': 0, 'cf': 1, 'acdeg': 2, 'acdfg': 3, 'bcdf': 4,
          'abdfg': 5, 'abdefg': 6, 'acf': 7, 'abcdefg': 8, 'abcdfg': 9}

all_digits = []

with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        coding, display = line.strip().split('|')
        strings = coding.strip().split(' ')
        digits = display.strip().split(' ')
        decmap = figure_out_coding(strings)
        decoded_digits = decode(digits, decmap)
        digits = np.array([digmap[k] for k in decoded_digits])
        all_digits.append(digits)

# find 1, 4, 7, 8
count, tally = 0, 0
for ad in all_digits:
    tally += 1000 * ad[0] + 100 * ad[1] + 10 * ad[2] + ad[3]
    for m in ad:
        if m in [1, 4, 7, 8]:
            count += 1

print("Part 1: ", count, " part 2: ", tally)
