#!/usr/bin/python3

import numpy as np
from rffilter import to_coupling_qk

def butterworth(n):
    """
    From page 97 of Microwave Filters, Impedance-Maching 
    Networks, and Coupling Structures, by Matthaei, Young,
    and Jones
    """
    g = np.ones(n + 2)
    k = np.array([ n for n in range(1, n + 1) ])
    g[1:-1] = 2 * np.sin((2 * k - 1) * np.pi / (2 * n))
    return g
    
def csv(row):
    return ','.join([ '{:.4f}'.format(x) for x in row ])

def main(stop=15):
    stop = int(stop)
    print("N g0   g1 ... gn    gn+1")
    for n in range(1, stop + 1):
        g = butterworth(n)
        print('    [ {} ], # {}'.format(csv(g), n))
    print()
    print("N q1 qn k12 k23 k34 k45 k56 ...")
    for n in range(1, stop + 1):
        g = butterworth(n)
        qk = to_coupling_qk(g)
        print('    [ {} ], # {}'.format(csv(np.concatenate(qk)), n))

if __name__ == '__main__':
    import sys
    np.set_printoptions(precision=4, linewidth=132)
    main(*sys.argv[1:])

