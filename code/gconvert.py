#!/usr/bin/env python3

import numpy as np
import argparse
from sys import argv
from sys import stderr
import h5py
import nbody
from os.path import splitext


parser = argparse.ArgumentParser(description='Create a density plot of dark matter for a Gadget-4 snapshot (hdf5 format only).')
parser.add_argument('filename', type=str, help='file name to read in')

args = parser.parse_args()


# get positions of dark matter particles
f = h5py.File(argv[1])

t = f['Header'].attrs['Time']
L = f['Parameters'].attrs['UnitLength_in_cm']
V = f['Parameters'].attrs['UnitVelocity_in_cm_per_s']
t *= L / V / (60*60*24*365*1e9)

pos = np.array(f['PartType1']['Coordinates'])
m = f['Header'].attrs['MassTable'][1]
N = len(pos)
print(N)

parts = np.zeros(N, dtype=nbody.System._particle_type)
parts['mass'] = m
parts['position'] = pos

s = nbody.System(time = t, particles=parts)


s.write(splitext(args.filename)[0] + ".dnc")


