
# convert s-parameters to reflected time delay
# $ python stodelay.py <filename>.s?p

import sys
import skrf as rf
import numpy as np

def unit(x):
    if np.isnan(x): return '            -'
    if np.isinf(x): return '          inf'
    exp = np.floor(np.log10(np.abs(x)))
    p = 3 * np.int(exp // 3)
    value = x / 10**p
    return '{:9.4f}e'.format(value) + '%+03d' % p

def main(filename):
    net = rf.Network(filename)
    print("# MHZ TDELAY")
    for f, gd in zip(net.f, net.group_delay):
        print('{:<8g}'.format(f / 1e6), end="")
        for i in range(len(gd)):
            td = gd[i,i].real
            print(' {}'.format(unit(td)), end="")
        print()

main(*sys.argv[1:])

