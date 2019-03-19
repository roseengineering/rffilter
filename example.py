
import numpy as np
from rffilter import to_leff, to_shuntc, zverev_qk

def calculate(q, k, BW, fo, LM, CM, CP, RM):
    fd = fo
    for i in range(10000):
        lm, fs, qu = to_leff(fd, fo, LM, CP, RM) 
        lm = np.ones(N) * lm
        res = to_shuntc(q, k, fs, BW, fd=fd, L0=lm, QU=qu)
        delta = res[7].max() - fd
        if delta**2 < 1e-10: break
        fd += .01 * delta
    return res, fd, qu

def display(res, fd, qu):
    np.set_printoptions(precision=4, linewidth=135)
    print('fd = %.3f kHz' % (fd / 1e3))
    print('CK', res[0])
    print('R0', 2 * np.pi * fd * res[1] / qu)
    print('L0', res[1])
    print('C0', res[2])
    print('CS', res[3])
    print('RE', res[4])
    print('Q ', res[5])
    print('K ', res[6])
    print('Kf', res[6] * fd)

name, N = 'BESSEL', 8
fo, LM, BW, QU = 4e6, .170, 500, 200000

wo = 2 * np.pi * fo
QL = fo / BW
RM = wo * LM / QU
CM = 1 / (wo**2 * LM)
CP = 220 * CM

print('fo=%.0f' % fo, 'Lm=%.5g' % LM, 'Cm=%.5g' % CM, 'Co=%.5g' % CP, 'Rm=%.2f' % RM)
q, k = next(zverev_qk(name, N, QU / QL))
res, fd, qu = calculate(q, k, BW, fo, LM, CM, CP, RM)
display(res, fd, qu)

