import numpy as np
import pdb
st = pdb.set_trace

N = 12
digits = []
totals = np.zeros(N)
lines = 0

with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        lines += 1
        digits.append(int(line, 2))
        for k, digit in enumerate(line):
            try:
                totals[k] += int(digit)
            except IndexError: # newline character
                continue

gamma, epsilon = totals > lines/2, totals < lines/2
gamma_dec, epsilon_dec = 0, 0 # decimal


for k in range(N):
    gamma_dec += gamma[N-k-1] * 2**k
    epsilon_dec += epsilon[N-k-1] * 2**k

print("Gamma: ", gamma_dec, "Epsilon: ", epsilon_dec)
print("Product: ", gamma_dec * epsilon_dec)

## Part 2, better way than before
def dfilt(data, bit, hi=True):
    mask = 1 << bit
    if mask_hi: # which bits are 1
        return data[data & mask > 0]
    else: # which bits are 0
        ## CONTINUE HERE
        return data[~data & mask > 0]

def mostcommon(data, bit):
    mask = 1 << bit
    return (data & mask != 0).mean() >= 0.5

def filt_common(data):
    data_new = data
    for b in range(N):
        bit = N - 1 - b
        hi = mostcommon(data, bit)
        data_new = dfilt(data, bit, hi)

testdata = np.array([10, 11, 01, 10])

# print(list_filt(np.array([1, 2, 3]), 0x1))

# print(mostcommon(np.array([1, 2, 3, 4]), 1))
