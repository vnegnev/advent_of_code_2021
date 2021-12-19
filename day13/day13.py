import numpy as np
import pdb
st = pdb.set_trace

coords = []
folds = []
xmax = 0
ymax = 0

# with open("examplefile.txt", "r") as ifile:
with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        try:
            xx, yy = line.strip().split(',')
            x, y = int(xx), int(yy)
            coords.append( [x, y] )
        except ValueError:
            if line[0] != '\n':
                # fold instructions
                _, _, fold = line.strip().split(' ')
                axis, offset = fold.split('=')
                folds.append( (axis, int(offset) ) )

coords = np.array(coords)
paper = np.zeros( (coords[:,1].max() + 1, coords[:,0].max() + 1), dtype=bool)

for coord in coords:
    paper[coord[1], coord[0]] = True

folded_paper = [paper]

for axis, offset in folds:
    pap = folded_paper[-1] #[:] # final colon copies
    if axis == 'x':
        folded = pap[:, :offset] | pap[:, :offset:-1]
    else:
        folded = pap[:offset, :] | pap[:offset:-1, :]

    print("Dots visible: ", folded.sum() )

    folded_paper.append(folded)

final = folded_paper[-1].astype(int)

# couldn't print nicely in the console
with open("output.txt", "w") as outfile:
    for k in final:
        for n in k:
            if n:
                outfile.write('X')
            else:
                outfile.write(' ')
        outfile.write("\n")
