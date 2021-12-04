import sys, os
import pdb
st = pdb.set_trace

coord = [0, 0, 0] # forward, depth, aim

def add_x(k):
    coord[0] += k
    coord[1] += k * coord[2]

def add_y(k):
    coord[2] += k

def sub_y(k):
    coord[2] -= k

dirmap = {'forward': add_x,
          'down': add_y,
          'up': sub_y}

with open("inputfile.py", "r") as ifile:
    for line in ifile:
        dir, mag = line.strip(' ').split(' ')
        magi = int(mag)
        dirmap[dir](magi)

print("Coords: ", coord, "Product: ", coord[0]*coord[1])
