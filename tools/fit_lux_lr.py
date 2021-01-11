#! /usr/bin/env python
import argparse

import numpy as np
from scipy.optimize import lsq_linear

def rmse(pred: np.ndarray, target: np.ndarray) -> float:
    return np.sqrt(np.mean((pred-target)**2))

def lux(logr: np.ndarray, m: float, b: float) -> np.ndarray:
    return 10**(m * logr + b)


parser = argparse.ArgumentParser(description='Fits least-squares model to lux-resistance data')
parser.add_argument('--input', required=True, help='File with recorded data')
parser.add_argument('--output', required=True, help='Parameters path')
parser.add_argument('--robust', action='store_true', help='Robust fit using Huber Regression')

args = parser.parse_args()

if args.robust:
    from sklearn import linear_model

data = np.loadtxt(args.input, dtype=float, delimiter=',')
target = data[:,1]

# Preprocess data
Y = np.log10(target)
inp = np.log10(data[:,0])

print("")
if args.robust:
    print('Using huber regression ...')
    x = inp.reshape(-1,1)
    reg = linear_model.HuberRegressor()
    reg.fit(x, Y)
    m, b = reg.coef_[0], reg.intercept_
    print(f"Number of outliers: {reg.outliers_.sum()}")
    print(f"Number of iterations: {reg.n_iter_}")
else:
    print('Using least squares regression ...')
    ones = np.ones_like(inp)
    x = np.stack([inp, ones], axis = 1)
    res = lsq_linear(x, Y)
    print(res)
    m, b = res.x[0], res.x[1]

pred=lux(inp, m, b)
err = rmse(pred, target)
np.savetxt(args.output, [m, b])

print("\n\n")
print(f"Root Mean Squared Error: {err}")
print(f"Lux Model parameters: {m}, {b}")
print(f"Done!")