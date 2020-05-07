
import numpy as np
from rffilter import to_coupling_qk

def butterworth_singlyterminated(n):
    """
    From page 107 of Microwave Filters, Impedance-Maching 
    Networks, and Coupling Structures, by Matthaei, Young,
    and Jones
    """
    k = np.array([ n for n in range(1, n + 1) ])
    a = np.sin((2 * k - 1) * np.pi / (2 * n))
    c = np.cos(k * np.pi / (2 * n))**2
    g = np.ones(n + 2)
    g[1] = a[0]
    for i in range(2, n + 1):
       g[i] = a[i-1] * a[i-2] / (c[i-2] * g[i-1])
    g[-1] = np.inf
    if n % 2 == 0: g[-1] = 0
    return g
    
def csv(row):
    return ','.join([ '{:.4f}'.format(x) for x in row ])

def main(stop=15):
    stop = int(stop)
    print("N g0   g1 ... gn    rs")
    for n in range(1, stop + 1):
        g = butterworth_singlyterminated(n)
        print('    [ {} ], # {}'.format(csv(g), n))
    print()
    print("N q1 qn k12 k23 k34 k45 k56 ...")
    for n in range(1, stop + 1):
        g = butterworth_singlyterminated(n)
        with np.errstate(divide='ignore'):
            qk = to_coupling_qk(g)
        print('    [ {} ], # {}'.format(csv(np.concatenate(qk)), n))

if __name__ == '__main__':
    import sys
    np.set_printoptions(precision=4, linewidth=132)
    main(*sys.argv[1:])

