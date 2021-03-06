import argparse
import os
import sys
import numpy as np
from collections import OrderedDict
import matplotlib
import colorsys
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{amssymb}']
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

sys.path.append(os.getcwd())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find the shortest path')
    parser.add_argument('--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--line', choices=['horizontal'], default='horizontal')
    parser.add_argument('--gammas',nargs='*',default=None)
    parser.add_argument('-y', type=int, default=0)
    parser.add_argument('-m', default='all')
    args = parser.parse_args()

gamma = {}
k = None
    
horizontal_line = set()
    
for line in args.infile.read().splitlines():
    if len(line)>0:
        v = line.split(' ')
        if k is None:
            k = len(v)/2 - 2
        f = v[0]
        i = 1
        for x in xrange(k+1):
            y,x = int(v[i]), int(v[i+1])
            if y == args.y:
                horizontal_line.add((y,x))
            i += 2
        idx = tuple([int(x) for x in v[1:i]])
        if idx not in gamma: 
            gamma[idx] = {}
        gamma[idx][f] = float(v[i])
        
gamma_names = gamma.values()[0].keys()
values = {g: [] for g in gamma_names}
colors = {g: [] for g in gamma_names}
hues = {g: [] for g in gamma_names}
for idx,v in gamma.items():
    _, j, _, rL, _, rR = idx
    hue = 1.0-np.power(1.0/(np.abs(j-rL)+1)+1.0/(np.abs(j-rR)+1),0.5)
    #hue = 1.0/np.min([np.abs(j-rL),np.abs(j-rR)])
    print(hue)
    clr = matplotlib.colors.hsv_to_rgb([hue, 1.0, 1.0])
    if len(v)==5:
        for f, value in v.items():
            values[f].append(value)
            colors[f].append(clr)
            hues[f].append(hue)

for f in ['depthmse','ssim','dsqm','mse']:
    plt.scatter(hues[f], values[f], color=colors[f], s=2)
    plt.xlabel('hue')
    plt.ylabel(f)
    plt.ylim([0,np.max(values[f])])
    plt.show()