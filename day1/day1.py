import numpy as np

from datafile_day1 import data

# data = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])

# day 1 pt 1
data_up = np.sum(np.diff(data) > 0)
print("Day 1 part 1: ", data_up)

# day 1 pt 2
data_filt = np.convolve([1, 1, 1], data, mode='valid')
data_filt_up = np.sum(np.diff(data_filt) > 0)
print("Day 1 part 2: ", data_filt_up)
