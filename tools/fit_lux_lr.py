#! /usr/bin/env python
import argparse

import numpy as np
from scipy.optimize import lsq_linear


parser = argparse.ArgumentParser(description='Fits least-squares model to lux-resistance data')
parser.add_argument('-I', required=True, help='File with recorded data')
parser.add_argument('-O', required=True, help='Parameters path')

args = parser.parse_args()

data = np.loadtxt(args.I, dtype=float, delimiter=',')
Y = np.log10(data[:,0])

inp = np.log10(data[:,1]).reshape(-1, 1)
ones = np.ones_like(inp)

x = np.concatenate([inp, ones], axis = 1)
res = lsq_linear(x, Y)
print('Optimization Report:')
print(res)
err = (inp**res.x[0]) * (10 ** res.x[1])
print(f"Root Mean Squared Error \n{err}")
np.savetxt(args.O, res.x)