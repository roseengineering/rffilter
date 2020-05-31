#!/usr/bin/python3

import numpy as np
from rffilter import to_coupling_qk

def cohn(n):
    g = 2 ** ((n-1) / n)
    return [1] + [g]*n + [1]

def csv(row):
    return ','.join([ '{:.4f}'.format(x) for x in row ])

def main(stop=15):
    stop = int(stop)
    print("    # g0 g1 ... gn gn+1")
    for n in range(1, stop + 1):
        g = cohn(n)
        print('    [ {} ], # n={}'.format(csv(g), n))
    print()
    print("    # q1 qn k12 k23 k34 k45 k56 ...")
    for n in range(1, stop + 1):
        g = cohn(n)
        qk = to_coupling_qk(g)
        print('    [ {} ], # n={}'.format(csv(np.concatenate(qk)), n))

if __name__ == '__main__':
    import sys
    np.set_printoptions(precision=4, linewidth=132)
    main(*sys.argv[1:])

