from nbody import *
from random import *
import numpy as np
import argparse
from sys import argv
from sys import stderr
from os.path import splitext

parser = argparse.ArgumentParser(description='Create a Plummer sphere.')
parser.add_argument('filename', type=str, help='output file name')
parser.add_argument('-n', type=int, dest='N', default=10000, help='Number of particles')
parser.add_argument('-r', type=float, dest='r_scale', default=1.0, help='Scale radius')
parser.add_argument('-v', type=float, dest='v_scale', default=1.0, help='Scale velocity')
parser.add_argument('-c', action='store_true', dest='cm', help='Adjust for centre of mass')
parser.add_argument('-vc', type=float, dest='v_coll', default=1.0, help='velocity which plummer 2 moves')
parser.add_argument('-theta', type=float, dest='theta', default=0.0, help=' velocity direction')
args = parser.parse_args()


M = 1.0

def plummer_mass(x):
    return 1.0 / np.sqrt(np.power(x, -2.0/3.0) - 1.0)
    
def plummer_potential(x):
    return -1.0 / np.sqrt(1.0 + x**2)
    
def plummer_g(x):
    return x**2 * np.power(1.0 - x**2, 3.5)
    
def pick_shell(radius):
    theta = np.arccos(np.random.uniform(-1.0, 1.0))
    phi = 2.0 * np.pi * np.random.random()
    
    x = radius * np.cos(phi) * np.sin(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(theta)
    
    return x, y, z


N_half = args.N//2
print(N_half)
parts1 = np.zeros(N_half, dtype=System._particle_type)
parts1['mass'] = M / (N_half)  # total mass is half!

parts2 = np.zeros(N_half, dtype=System._particle_type)
parts2['mass'] = M / N_half  # total mass is half!

g_max = 0.1 # See Aarseth et al

for i in range(N_half):
    radius = plummer_mass(0.999 * np.random.random())
    
    x1, y1, z1 = pick_shell(radius)
    x2, y2, z2 = pick_shell(radius)
    
    q = np.random.random()
    test = g_max * np.random.random()
    while test > plummer_g(q):
        q = np.random.random()
        test = g_max * np.random.random()
        
    velocity = args.v_scale * q * np.sqrt(-2.0 * plummer_potential(radius))
    vx1, vy1, vz1 = pick_shell(velocity)
    vx2, vy2, vz2 = pick_shell(velocity)
       
    parts1[i]['position'][0] = x1
    parts1[i]['position'][1] = y1
    parts1[i]['position'][2] = z1
    
    parts2[i]['position'][0] = x2 + 30
    parts2[i]['position'][1] = y2 
    parts2[i]['position'][2] = z2
    
    parts1[i]['velocity'][0] = vx1
    parts1[i]['velocity'][1] = vy1
    parts1[i]['velocity'][2] = vz1
    
    parts2[i]['velocity'][0] = vx2 -args.v_coll*np.cos(args.theta)
    parts2[i]['velocity'][1] = vy2 #-args.v_coll*np.sin(args.theta)
    parts2[i]['velocity'][2] = vz2
    
#s is a system object   
s = System(particles=np.concatenate((parts1, parts2)))

if args.cm:
	s.translate_to(s.centre_of_mass())

s.write(args.filename)
        
