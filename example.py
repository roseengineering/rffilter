
import sys
import numpy as np
from rffilter import to_leff, to_shuntc, zverev_qk, zverev_min
from decimal import Decimal, Context, Rounded, Inexact

def h(d):
    return ','.join([ Decimal(x).normalize(Context(prec=5)).to_eng_string().lower() for x in d ])

def calculate(q, k, BW, fo, LM, CM, CP, RM, name=''):
    fd = fo
    for i in range(10000):
        lm, fs, qu = to_leff(fd, fo, LM, CP, RM) 
        if name == 'QUASI_EQUIRIPPLE': lm = np.ones(len(k)+1) * lm; lm[0] /= 2; lm[-1] /= 2
        res = to_shuntc(q, k, fs, BW, fd=fd, L0=lm, QU=qu)
        delta = res[7].max() - fd
        if delta**2 < 1e-10: break
        fd += .01 * delta
    return res, fd, qu

def display(res, fd, qu):
    print('fd = %.3f kHz' % (fd / 1e3))
    print('CK', h(-res[0]))
    print('R0', h(2 * np.pi * fd * res[1] / qu))
    print('L0', h(res[1]))
    print('C0', h(-res[2]))
    print('CS', h(-res[3]))
    print('RE', h(res[4]))
    print('Q ', h(res[5]))
    print('K ', h(res[6]))
    print('Kf', h(res[6] * fd))
    print()

def main(fo=4e6, BW=500, LM=.170, QU=200000, name='LINEAR_PHASE_05', N=8):
    fo, LM, BW, QU, N = float(fo), float(LM), float(BW), float(QU), int(N)
    QL = fo / BW
    qo = QU / QL
    qo_lossless, _ = zverev_min(name, N, qo)
    for q, k in zverev_qk(name, N, qo):
        print('name=', name, 'N(poles)=', N, 'BW=', BW, 'fo=', fo)
        print('QU=', QU, 'qo=', qo, 'qo(lossless)=', qo_lossless)
        wo = 2 * np.pi * fo
        RM = wo * LM / QU
        CM = 1 / (wo**2 * LM)
        CP = 220 * CM
        print('Lm=%.5g' % LM, 'Cm=%.5g' % CM, 'Co=%.5g' % CP, 'Rm=%.2f' % RM)
        res, fd, qu = calculate(q, k, BW, fo, LM, CM, CP, RM)
        display(res, fd, qu)

if __name__ == "__main__":
    main(**{ k:v for k,v in [ d.split('=') for d in sys.argv[1:] ] })

