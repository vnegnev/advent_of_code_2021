import numpy as np
import pdb
st = pdb.set_trace

called_numbers = None

boards = []

with open("inputfile.txt", "r") as ifile:
# with open("examplefile.txt", "r") as ifile:
    firstline = True
    row = 0
    board = None
    for line in ifile:
        if firstline:
            nums = line.strip().split(',')
            called_numbers = np.array([int(k) for k in nums])
            firstline = False
            continue

        # other lines
        if line.strip() == '':
            # make a new board
            row = 0
            board = np.empty([5, 5], dtype=int)
        else:
            nums = line.strip().split()
            board[row, :] = np.array([int(k) for k in nums])
            row += 1
            if row == 5:
                boards.append(board)

matches = []

for k in boards:
    # print(k)
    matches.append(np.zeros([5,5], dtype=bool))

# Testing
# called_numbers = np.array([60, 68, 8, 2, 53])
winners = []

for n in called_numbers:
    for idx, (m, b) in enumerate(zip(matches, boards)):
        if idx in winners:
            continue # skip already-winning boards
        co = np.where(b == n)
        m[co[0], co[1]] = True

        # Check for winner
        winner = np.any(m.sum(axis=0) == 5) or np.any(m.sum(axis=1) == 5)

        # count score
        if winner:
            score = np.sum( ~m * b ) * n
            winners.append(idx)
            print("Idx: ", idx, "Score: ", score)

print("Winners: ", winners)
