import numpy as np
import pdb
st = pdb.set_trace

risks = []

with open("examplefile.txt", "r") as ifile:
# with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        riskints = line.strip()
        riskrow = []
        for r in riskints:
            riskrow.append(int(r))

        risks.append(riskrow)

risks = np.array(risks)

R, C = risks.shape

## Problem is coming up with an algorithm; can think of many that might come close but get stuck in local minima.
# Assume the path is always either down or right.
#
# Start from simpler problem: path for a 2x2 grid -- enter on top-left 3 squares, exit on bottom-right 3 squares?
#
# Too hard for me, for the time being!
#
