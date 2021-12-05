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
# def dfilt(data, bit, hi=True):
#     mask = 1 << bit
#     if hi: # which bits are 1
#         return data[data & mask > 0]
#     else: # which bits are 0
#         ## CONTINUE HERE
#         return data[~data & mask > 0]

# def mostcommon(data, bit):
#     mask = 1 << bit
#     return (data & mask != 0).mean() >= 0.5

# def filt_common(data, bits=N):
#     st()
#     data_new = data
#     for b in range(bits):
#         bit = bits - 1 - b
#         hi = mostcommon(data, bit)
#         data_new = dfilt(data, bit, hi)


## Better way still

testdata = np.array([
    0b00100,
    0b11110,
    0b10110,
    0b10111,
    0b10101,
    0b01111,
    0b00111,
    0b11100,
    0b10000,
    0b11001,
    0b00010,
    0b01010])


def filter_bits(data, bits, get_leastcommon=False, debug=False):
    pow2_sum = 0
    for bit in range(bits-1, -1, -1):
        pow2 = 2**bit
        pow2_cmp = pow2 + pow2_sum

        if debug:
            print(data, pow2_cmp)

        if get_leastcommon:
            subset = data < pow2_cmp
        else:
            subset = data >= pow2_cmp

        most_common = np.sum(data >= pow2_cmp) >= data.size / 2 # is 1 or 0 more common

        if most_common:
            if not get_leastcommon:
                pow2_sum = pow2_cmp
        else:
            subset = ~subset
            if get_leastcommon:
                pow2_sum = pow2_cmp

        data = data[subset]
        if data.size == 1:
            break

    return data

# print(list_filt(np.array([1, 2, 3]), 0x1))

# newdata = testdata
# for k in range(5):

print("Test data: ", filter_bits(testdata, bits=5, get_leastcommon=False))

real_data = []
with open("inputfile.txt", "r") as ifile:
    for line in ifile:
        real_data.append(int(line, 2))

real_data = np.array(real_data)

oxy = filter_bits(real_data, bits=12, get_leastcommon=False)
co2 = filter_bits(real_data, bits=12, get_leastcommon=True)

print("Product of oxy and co2: ", oxy * co2)
