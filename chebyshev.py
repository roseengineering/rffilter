
import numpy as np
from rffilter import to_coupling_qk

def chebyshev(delta, n):
    """
    From page 99 of Microwave Filters, Impedance-Maching 
    Networks, and Coupling Structures, by Matthaei, Young,
    and Jones
    """
    beta = np.log(1 / np.tanh(delta / (40 / np.log(10))))
    gamma = np.sinh(beta / (2 * n))
    k = np.array([ n for n in range(1, n + 1) ])
    A = np.sin((2 * k - 1) * np.pi / (2 * n))
    B = gamma**2 + np.sin(k * np.pi / n)**2
    g = np.ones(n + 2)
    g[1] = 2 * A[0] / gamma
    for i in range(2, n + 1):
        g[i] = 4.0 * A[i-2] * A[i-1] / (B[i-2] * g[i-1])
    if n % 2 == 0:
        g[n+1] = np.tanh(beta / 4)**2  # is this right! shouldn't it be coth!
    return np.array(g)

def csv(row):
    return ','.join([ '{:.4f}'.format(x) for x in row ])

def main(delta=.1, stop=15):
    delta = float(delta)
    stop = int(stop)
    print("N g0   g1 ... gn    gn+1")
    for n in range(1, stop + 1):
        g = chebyshev(delta, n)
        print('{:<2d} [ {} ],'.format(n, csv(g)))
    print()
    print("N q1 qn k12 k23 k34 k45 k56 ...")
    for n in range(1, stop + 1):
        g = chebyshev(delta, n)
        qk = to_coupling_qk(g)
        print('{:<2d} [ {} ],'.format(n, csv(np.concatenate(qk))))

if __name__ == '__main__':
    import sys
    np.set_printoptions(precision=4, linewidth=132)
    main(*sys.argv[1:])

