
Library for creating wideband and narrowband filters. Includes table of predistorted q,k values from Zverek

rffilter.py python3 library
----------------------

Library for creating wideband lowpass, highpass, bandpass, and 
bandstop filters from lowpass element prototype values. The variable
g is a list of the g0,g1,..gn,gn+1 element values for the filter.
The element values g are contained in the dictionary LOWPASS.
They can either be accessed directly or using the function lowpass_g().

```
lowpass_g(name, n)
to_lowpass(g, fc, R)
to_highpass(g, fc, R)
to_bandpass(g, fo, BW, R)
to_bandstop(g, fo, BW, R)
```

LOWPASS provides the following lowpass responses:

```
BESSEL
BUTTERWORTH
CHEBYSHEV_01 (.01dB ripple)
CHEBYSHEV_04 (.04dB ripple) 
CHEBYSHEV_10 (.1dB ripple)
CHEBYSHEV_20 (.2dB ripple)
COHN 
GAUSSIAN_6 (6dB down)
GAUSSIAN_12 (12dB down)
LINEAR_PHASE_05 (.05 deg error)
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
The q,k values can also be found by using the Zverev k,q predistored
table OCRed into the library.  The table is located in the
dictionary ZVEREV.  The k,q values for a normalized Q, qo,
can be retrieved directly or using the zverev_qk() function.  
The lower bound qo and insertion loss for a filter can 
found using the zverev_min() function.

```
zverev_qk(name, n, qo)
zverev_min(name, n, qo=None)
to_coupling(g)
to_topc(q, k, fo, BW, RE=None, L0=None, QU=inf)
to_shuntc(q, k, fo, BW, RE=None, L0=None, fd=None, QU=inf)
```

ZVEREV provides the following k,q responses:

```
BESSEL
BUTTERWORTH
CHEBYSHEV_01 (.01dB ripple)
CHEBYSHEV_1 (.1dB ripple)
CHEBYSHEV_5 (.5dB ripple)
GAUSSIAN 
GAUSSIAN_6 (6db down)
GAUSSIAN_12 (12db down)
LEGENDRE 
LINEAR_PHASE_5 (.5 deg error)
LINEAR_PHASE_05 (.05 deg error)
```

crystal filters
-------------------

Hayward provides a formula for the effective Lm of a crystal when
a capacitance Co shunts it.  This is provided by the function to_leff().
f is the frequency to use to find the effective Lm for, while fo, LM, and CP
are the series resonant frequency, motional inductance and holder capacitance
of the crystal respectively.

```
to_leff(f, fo, LM, CP)
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
# A BESSEL 8 pole filter, 500Hz wide, using 4.0Mhz crystals with Qu of 200000

$ python3 example.py

fd=4002.161 kHz Lm=0.17 Cm=-9.3126e-15 Co=-2.0488e-12
CK [-7.3053e-12 -1.5911e-11 -2.3291e-11 -2.9597e-11 -3.5305e-11 -4.2670e-11 -6.8308e-11]
CS [-1.5911e-11  1.0872e-03 -1.0644e-11 -8.1291e-12 -7.2662e-12 -6.7579e-12 -6.1858e-12 -5.4026e-12]
RE [9391.716   451.0974]
Q  [  780.4213 15081.7423]
K  [7.3980e-04 3.3967e-04 2.3204e-04 1.8260e-04 1.5308e-04 1.2666e-04 7.9120e-05]
Kf [2960.8  1359.4   928.65  730.8   612.65  506.9   316.65]

# Note, capacitance is given as negative.  CK is the coupling cap and CS is the tuning.
# The tuning capacitor of 1.0872mH above should be considered a short.
```
