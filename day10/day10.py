import numpy as np
import pdb
st = pdb.set_trace

type_dict = { # index type of bracket (0-indexed, because originally I misunderstood the task), indentation increase/decrease, score for part a
    '(': (0, 1, 3), ')': (0, -1, 3),
    '[': (1, 1, 57), ']': (1, -1, 57),
    '{': (2, 1, 1197), '}': (2, -1, 1197),
    '<': (3, 1, 25137), '>': (3, -1, 25137)
}

score = 0
scores_autoc = []

# with open("examplefile.txt", "r") as ifile:
with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        # depths = np.array([0, 0, 0, 0])
        chunk_stack = []
        close_score = 0
        chars = line.strip()

        for ch in chars:
            td = type_dict[ch]

            if td[1] == 1:
                chunk_stack.append(td[0])
            elif chunk_stack.pop() != td[0]: # wrong kind of closing delimiter
                score += td[2]
                chunk_stack = []
                break

        if chunk_stack:
            chunk_stack.reverse()
            for ch in chunk_stack:
                close_score = 5 * close_score + ch + 1

            scores_autoc.append(close_score)

print("Part a score: ", score)
print("Part b score: ", sorted(scores_autoc)[len(scores_autoc)//2])
