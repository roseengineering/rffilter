
Library for creating wideband and narrowband filters. Includes a table of predistorted q, k values from Zverek

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
QUASI_EQUIRIPPLE (derived from q, k in ARRL 2017 Handbook)
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
The q,k values can also be found by using the Zverev q, k predistored
table OCRed into the library.  The table is located in the
dictionary ZVEREV.  The q, k values for a normalized Q, qo,
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

ZVEREV provides the following q, k responses:

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

COUPLED provides the following q, k responses:

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
# A BESSEL 8 pole filter, 500Hz wide, using 4.0Mhz crystals with Qu of 200000

$ python3 example.py

fd=4003.544 kHz Lm=0.17 Cm=-9.3126e-15 Co=-2.0488e-12 Rm=21.36
CK [-4.6753e-12 -1.0183e-11 -1.4906e-11 -1.8942e-11 -2.2595e-11 -2.7308e-11 -4.3716e-11]
R0 [57.4162 57.4162 57.4162 57.4162 57.4162 57.4162 57.4162 57.4162]
L0 [0.4571 0.4571 0.4571 0.4571 0.4571 0.4571 0.4571 0.4571]
C0 [-3.4613e-15 -3.4613e-15 -3.4613e-15 -3.4613e-15 -3.4613e-15 -3.4613e-15 -3.4613e-15 -3.4613e-15]
CS [-1.0183e-11  6.9284e-04 -6.8118e-12 -5.2025e-12 -4.6503e-12 -4.3250e-12 -3.9588e-12 -3.4576e-12]
RE [14669.8172   704.6607]
Q  [  780.6911 15086.9557]
K  [7.3954e-04 3.3955e-04 2.3196e-04 1.8254e-04 1.5303e-04 1.2661e-04 7.9092e-05]
Kf [2960.8  1359.4   928.65  730.8   612.65  506.9   316.65]

# Note, capacitance is given as negative.  CK is the coupling cap and CS is the tuning.
# The tuning capacitor of .69284mH above should be considered a short.
```

