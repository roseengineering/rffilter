
Library for creating wideband and narrowband filters. Includes a table of predistorted q,k values from Zverek

rffilter.py python3 library
----------------------

Library for creating wideband lowpass, highpass, bandpass, and 
bandstop filters from lowpass element prototype values. The variable
g is a list of the g0,g1,..gn,gn+1 element values for the filter.
The element values g are contained in the dictionary LOWPASS.
They can either be accessed directly or using the function lowpass_g().

```
lowpass_g(name, n) - returns an iterator of g values
to_lowpass(g, fc, R)
to_highpass(g, fc, R)
to_bandpass(g, fo, BW, R)
to_bandstop(g, fo, BW, R)
```

LOWPASS provides the following lowpass responses:

```
BESSEL
BUTTERWORTH
CHEBYSHEV_001 (.01dB ripple)
CHEBYSHEV_004 (.04dB ripple) 
CHEBYSHEV_01 (.1dB ripple)
CHEBYSHEV_02 (.2dB ripple)
COHN 
GAUSSIAN_6 (to 6dB down)
GAUSSIAN_12 (to 12dB down)
LINEAR_PHASE_05 (.05 deg ripple)
LINEAR_PHASE_5 (.5 deg ripple)
QUASI_EQUIRIPPLE (derived from q,k in ARRL 2017 Handbook)
```

The library also provides functions for creating either
parallel resonant or series resonant coupled bandpass filters.
For the below functions L0 can either be a single value
or a list of the nodal inductor values to be used.
Likewise RE is either the value of both end filter resistors or
a list of the two resistors' values.  QU is the unloaded Q
of the resonators.

The q,k values can be generated with using the to_coupling()
function from the lossless g values retrieved above.  
The q,k values can also be found by using the Zverev q,k predistored
table OCRed into the library.  The table is located in the
dictionary ZVEREV.  The q,k values for a normalized Q, qo,
can be retrieved directly or using the zverev_qk() function.  
The lower bound qo and insertion loss for a filter can 
found using the zverev_min() function.

```
zverev_qk(name, n, qo) - returns an iterator of q,k values
zverev_min(name, n, qo=inf) - returns the minimum qo and IL of the response
to_coupling(g)
to_topc(q, k, fo, BW, RE=None, L0=None, QU=inf)
to_shuntc(q, k, fo, BW, RE=None, L0=None, fd=None, QU=inf)
```

ZVEREV provides the following q,k responses:

```
BESSEL
BUTTERWORTH
CHEBYSHEV_001 (.01dB ripple)
CHEBYSHEV_01 (.1dB ripple)
CHEBYSHEV_05 (.5dB ripple)
GAUSSIAN 
GAUSSIAN_6 (to 6db down)
GAUSSIAN_12 (to 12db down)
LEGENDRE 
LINEAR_PHASE_5 (.5 deg ripple)
LINEAR_PHASE_05 (.05 deg ripple)
```

COUPLED provides the following q,k responses:

```
BESSEL
BUTTERWORTH
CHEBYSHEV_001
CHEBYSHEV_01
CHEBYSHEV_05
CHEBYSHEV_1
GAUSSIAN_12
GAUSSIAN_6
LINEAR_PHASE_05
LINEAR_PHASE_5
```

To get a particular response and order from COUPLED you can use:

```
coupled_qk(name, n)- returns an iterator of q,k values
```

crystal filters
-------------------

Hayward provides a formula for the effective Lm of a crystal when
a capacitance Co shunts it.  This is provided by the function to_leff().
f is the frequency to use to find the effective Lm for, while fo, LM, and CP
are the series resonant frequency, motional inductance and holder capacitance
of the crystal respectively.

```
to_leff(f, fo, LM, CP, RM) - returns new_LM, new_fo, Q_unloaded
```
 

The zverev data OCR
-------------------

The zverev data was OCRed using the following files.  The num.traineddata
are the digits used to train the OCR reader.  The zverev.dat is the
cleaned up result of the OCR process - with the INF. rows removed.
The zverek.sh contains the script used to scan the pages.

```
num.traineddata
zverev.dat
zverev.py
zverev.sh
```

Example
----------

```
$ python3 example.py

name= LINEAR_PHASE_05 N(poles)= 8 BW= 500.0 fo= 4000000.0
QU= 200000.0 qo= 25.0 qo(lossless)= 18.724
Lm=0.17 Cm=9.3126e-15 Co=2.0488e-12 Rm=21.36
fd = 4001.125 kHz
CK 22.925e-12,39.47e-12,36.155e-12,47.303e-12,94.465e-12,68.055e-12,34.992e-12
R0 27.825,27.825,27.825,27.825,27.825,27.825,27.825,27.825
L0 0.22144,0.22144,0.22144,0.22144,0.22144,0.22144,0.22144,0.22144
C0 7.149e-15,7.149e-15,7.149e-15,7.149e-15,7.149e-15,7.149e-15,7.149e-15,7.149e-15
CS 39.47e-12,-0.001434,62.649e-12,49.609e-12,26.86e-12,22.896e-12,38.935e-12,24.766e-12
RE 1932.9,1778.6
Q  2839.2,3081.7
K  0.00031169,0.00018104,0.00019763,0.00015106,0.000075641,0.000105,0.00020421
Kf 1247.1,724.35,790.75,604.4,302.65,420.1,817.05
...

# CK is the coupling cap and CS is the tuning.
# The negative tuning capacitor above should be considered a short.
```

Open [example.sch](example.sch) in Qucs to simulate the above crystal filter.

