
import numpy as np
from rffilter import *

np.set_printoptions(precision=4, linewidth=135)
N = 8
fo = 4e6
BW = 500
name = 'BESSEL'
LM = .170
QU = 200000
QL = fo / BW
qo = QU / QL
q, k = next(zverev_qk(name, N, qo))

wo = 2 * np.pi * fo
CM = 1 / (wo**2 * LM)
CP = 220 * CM
fd = fo
for i in range(10000):
    L0 = np.ones(N) * to_leff(fd, fo, LM, CP)
    if name == 'QUASI_EQUIRIPPLE': L0[0] /= 2; L0[-1] /= 2
    res = to_shuntc(q, k, fo, BW, fd=fd, L0=L0, QU=QU)
    delta = (res[7].max() - fd)
    if delta**2 < 1e-10: break
    fd += .01 * delta

print('fd=%.3f kHz' % (fd / 1e3), 'Lm=%.5g' % LM, 'Cm=%.5g' % -CM, 'Co=%.5g' % -CP)
print('CK', res[0])
print('CS', res[3])
print('RE', res[4])
print('Q ', res[5])
print('K ', res[6])
print('Kf', res[6] * fd)

