

# rffilter.py

Python 3 script for calculating RF filters.
The script requires the numpy library.

For nodal and mesh filters (including crystal filters) the script
prints resonator group delays from Ness as well as 
resonator coupling bandwidths from Dishal.  They are 
also printed when no filter frequency selection type 
is requested, provided the bandwidth is given.

# Library functions

The script provides the following public functions for import.

```
# find filter coefficients or prototype values

g    = lowpass_g(name, n)
q, k = coupling_qk(name, n)
q, k = zverev_k(name, n, qo=np.inf)
qo   = zverev_qo(name, n, qo=np.inf)

# coupling coefficent conversion

q, k = to_coupling_qk(g)
cbw  = to_coupling_bw(q, k, BW)
Q, K = denormalize_qk(q, k, fo, BW)
td   = to_group_delay(q, k, BW)

# wide-band filter design

xs, xp, re = to_lowpass(g, fo, R)
xs, xp, re = to_highpass(g, fo, R)
xs, xp, re = to_bandpass(g, fo, BW, R)
xs, xp, re = to_bandstop(g, fo, BW, R)

# narrow-band filter design

xs, xp, re           = to_nodal(q, k, fo, BW, R=None, L=None)
xs, xp, re           = to_mesh(q, k, fo, BW, R=None, L=None)
xs, xp, re, mesh, fo = to_crystal_mesh(q, k, fo, BW, LM, CP=0, QU=np.inf)
```

# Command Line

The program takes the following command line options:

```
-g             : lowpass prototype element response types
-k             : q, k coupling response types
-zverev        : predistorted q, k coupling response types from Zverev.
-n             : number of filter poles or resonators
-r             : end resistors, can be given in common notation
-l             : resonator inductor values, can be given in common notation
-f             : design frequency
-bw            : design bandwidth
-qu            : unload Q of resonators
-cp            : parallel capacitance, C0, of crystals
-expose        : expose resonators in spice netlist for nodal and mesh filters
-lowpass       : generate a lowpass filter
-highpass      : generate a highpass filter
-bandpass      : generate a wideband bandpass filter
-bandstop      : generate a wideband bandstop filter
-nodal         : generate a narrow-band nodal bandpass filter
-mesh          : generate a narrow-band mesh bandpass filter
-crystal       : generate a narrow-band crystal bandpass filter
```

# Examples

## List of filter response types provided


```
$ rffilter.py -g
G LOWPASS         POLES
bessel            2  3  4  5  6  7  8  9 10
butterworth       1  2  3  4  5  6  7  8  9 10 11
chebyshev_0.01    3  4  5  6  7  8  9 10 11
chebyshev_0.044   3  4  5  6  7  8  9 10 11
chebyshev_0.1     2  3  4  5  6  7  8  9 12
chebyshev_0.2     3  4  5  6  7  8  9 10 11
gaussian_12       3  4  5  6  7  8  9 10
gaussian_6        3  4  5  6  7  8  9 10
linear_phase_05   2  3  4  5  6  7  8  9 10
linear_phase_5    2  3  4  5  6  7  8  9 10
```


```
$ rffilter.py -k
QK COUPLING       POLES
bessel            2  3  4  5  6  7  8
butterworth       2  3  4  5  6  7  8
chebyshev_0.01    2  3  4  5  6  7  8
chebyshev_0.1     2  3  4  5  6  7  8
chebyshev_0.5     2  3  4  5  6  7  8
chebyshev_1.0     2  3  4  5  6  7
gaussian_12       3  4  5  6  7  8
gaussian_6        3  4  5  6  7  8
linear_phase_05   2  3  4  5  6  7  8
linear_phase_5    2  3  4  5  6  7  8
```


```
$ rffilter.py -zverev
QK ZVEREV         POLES
bessel            2  3  4  5  6  7  8
butterworth       2  3  4  5  6  7  8
chebyshev_0.01    2  3  4  5  6  7  8
chebyshev_0.1     2  3  4  5  6  7  8
chebyshev_0.5     2  3  4  5  6  7  8
gaussian          2  3  4  5  6  7  8
gaussian_12       3  4  5  6  7  8
gaussian_6        3  4  5  6  7  8
legendre          3  4  5  6  7  8
linear_phase_05   2  3  4  5  6  7  8
linear_phase_5    2  3  4  5  6  7  8
```


## Coupling bandwidth and group delay

Print out coupling design information.  CBW is the coupling bandwidth between resonators and the bandwidth of the two resonators at the end.
TD0 and TDn are the group delay
at the center freqency for each resonator looking from either end, see 
Ness' "A Unified Approach to the
Design, Measurement, and Tuning of Coupled-Resonator Filters" in MTT.


```
$ rffilter.py -g chebyshev_0.2 -n 8 -bw 1000
* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.3800  878.5353e-06             -  724.6377e+00             -
* 12     0.7225  883.6282e-06    3.3733e-03  722.5464e+00             -
* 23     0.5602    2.3402e-03    5.1911e-03  560.1693e+00             -
* 34     0.5349    1.8526e-03    2.8023e-03  534.9420e+00             -
* 45     0.5298    3.8305e-03    3.8317e-03  529.7756e+00             -
* 56     0.5349    2.8030e-03    1.8522e-03  534.8960e+00             -
* 67     0.5601    5.1897e-03    2.3410e-03  560.1072e+00             -
* 78     0.7225    3.3742e-03  883.4691e-06  722.5309e+00             -
* 89     1.3803             -  878.7312e-06  724.4761e+00             -
```


## Nodal narrow-band filters.

Generate a narrow-band filter using LC resonators top coupled by capacitors.
The -expose option exposes the resonators of the filter as ports.
The input port is the port 1 while the port with the highest number
is the output port.  The exposed resonators ports are numbered in increasing order.


```
$ rffilter.py -k chebyshev_0.1 -nodal -expose -f 10e6 -bw 400e3 -n 5 -qu 2000 | tee examples/nodal.cir
.SUBCKT F1 1 2 3 4 5
* COMMAND  : rffilter.py -k chebyshev_0.1 -nodal -expose -f 10e6 -bw 400e3 -n 5 -qu 2000
* TYPE     : CHEBYSHEV_0.1
* FILTER   : NODAL
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : 2000.0

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.3010    2.0706e-06             -  307.4558e+03   32.5250e+00
* 12     0.7030    2.4753e-06    7.7031e-06  281.2000e+03   28.1200e-03
* 23     0.5360    5.6325e-06    4.9506e-06  214.4000e+03   21.4400e-03
* 34     0.5360    4.9506e-06    5.6325e-06  214.4000e+03   21.4400e-03
* 45     0.7030    7.7031e-06    2.4753e-06  281.2000e+03   28.1200e-03
* 56     1.3010             -    2.0706e-06  307.4558e+03   32.5250e+00

L1  1    1001   24.4666e-09
R1  1001 0     768.6395e-06
C2  1    0      10.0619e-09
C3  1    2     291.1272e-12

L4  2    1004   24.4666e-09
R4  1004 0     768.6395e-06
C5  2    0       9.8399e-09
C6  2    3     221.9689e-12

L7  3    1007   24.4666e-09
R7  1007 0     768.6395e-06
C8  3    0       9.9091e-09
C9  3    4     221.9689e-12

L10 4    1010   24.4666e-09
R10 1010 0     768.6395e-06
C11 4    0       9.8399e-09
C12 4    5     291.1272e-12

L13 5    1013   24.4666e-09
R13 1013 0     768.6395e-06
C14 5    0      10.0619e-09
.ends
.end

```

![nodal](examples/nodal.png)

## Mesh narrow-band filters.


```
$ rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8 | tee examples/mesh.cir
.SUBCKT F1 1 17
* COMMAND  : rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8
* TYPE     : BUTTERWORTH
* FILTER   : MESH
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.3902  620.9908e-09             -    1.0252e+06    9.7545e+00
* 12     1.5187    1.7684e-06    8.1580e-06  607.4955e+03   60.7496e-03
* 23     0.7357    3.2676e-06    8.1580e-06  294.2641e+03   29.4264e-03
* 34     0.5537    4.8904e-06    7.5370e-06  221.4725e+03   22.1472e-03
* 45     0.5098    6.3896e-06    6.3896e-06  203.9183e+03   20.3918e-03
* 56     0.5537    7.5370e-06    4.8904e-06  221.4725e+03   22.1472e-03
* 67     0.7357    8.1580e-06    3.2676e-06  294.2641e+03   29.4264e-03
* 78     1.5187    8.1580e-06    1.7684e-06  607.4955e+03   60.7496e-03
* 89     0.3902             -  620.9908e-09    1.0252e+06    9.7545e+00

L1  1    2       7.7624e-06
C2  2    3      34.7427e-12

C3  3    0     537.1580e-12
L4  3    4       7.7624e-06
C5  4    5      35.8664e-12

C6  5    0       1.1089e-09
L7  5    6       7.7624e-06
C8  6    7      34.4066e-12

C9  7    0       1.4734e-09
L10 7    8       7.7624e-06
C11 8    9      34.0819e-12

C12 9    0       1.6003e-09
L13 9    10      7.7624e-06
C14 10   11     34.0819e-12

C15 11   0       1.4734e-09
L16 11   12      7.7624e-06
C17 12   13     34.4066e-12

C18 13   0       1.1089e-09
L19 13   14      7.7624e-06
C20 14   15     35.8664e-12

C21 15   0     537.1580e-12
L22 15   16      7.7624e-06
C23 16   17     34.7427e-12
.ends
.end

```

![mesh lossy](examples/mesh.png)

## Crystal mesh filters.


### 1. The "Crystal Ladder Filters for All" filter.

Build a 2400 Hz bandwidth crystal filter.  This filter is from an example in Steder's 
"Crystal Ladder Filters for All" paper in QEX.  


```
$ rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12 | tee examples/xtal.cir
.SUBCKT F1 1 25
* COMMAND  : rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12
* TYPE     : CHEBYSHEV_0.2
* FILTER   : CRYSTAL_MESH
* ORDER    : 8
* FREQ     : 4.915464 MHz
* RS       : 1153.4
* RL       : 1153.1
* CP       : 3.6600e-12
* BW       : 2.4000e+03
* QL       : 2048.1
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.3800  366.0564e-06             -    1.7391e+03    2.8264e+03
* 12     0.7225  368.1784e-06    1.4056e-03    1.7341e+03  352.7869e-06
* 23     0.5602  975.0893e-06    2.1630e-03    1.3444e+03  273.5055e-06
* 34     0.5349  771.9015e-06    1.1676e-03    1.2839e+03  261.1881e-06
* 45     0.5298    1.5961e-03    1.5965e-03    1.2715e+03  258.6656e-06
* 56     0.5349    1.1679e-03  771.7423e-06    1.2838e+03  261.1657e-06
* 67     0.5601    2.1624e-03  975.4158e-06    1.3443e+03  273.4751e-06
* 78     0.7225    1.4059e-03  368.1121e-06    1.7341e+03  352.7793e-06
* 89     1.3803             -  366.1380e-06    1.7387e+03    2.8270e+03

* Xtal    Xtal freq     Mesh freq   Mesh offset   Xtal offset
* 1       4913570.0     4914792.0        -672.3           0.0
* 2       4913570.0     4915464.3          -0.0           0.0
* 3       4913570.0     4915239.1        -225.1           0.0
* 4       4913570.0     4915202.7        -261.6           0.0
* 5       4913570.0     4915202.6        -261.7           0.0
* 6       4913570.0     4915239.0        -225.3           0.0
* 7       4913570.0     4915464.2          -0.1           0.0
* 8       4913570.0     4914792.0        -672.3           0.0

* ij              CKij            CSi
* 12       28.1538e-12    36.3145e-12
* 23       36.3147e-12     5.8570e-06
* 34       38.0273e-12   108.4305e-12
* 45       38.3981e-12    93.3131e-12
* 56       38.0306e-12    93.2934e-12
* 67       36.3188e-12   108.3680e-12
* 78       28.1544e-12   250.9392e-09
* 89                 -    36.3135e-12

C1  1    2      15.0527e-15
L2  2    3      69.7000e-03
C3  1    3       3.6600e-12
C4  3    4      36.3145e-12

C5  4    0      28.1538e-12
C6  4    5      15.0527e-15
L7  5    6      69.7000e-03
C8  4    6       3.6600e-12
C9  6    7       5.8570e-06

C10 7    0      36.3147e-12
C11 7    8      15.0527e-15
L12 8    9      69.7000e-03
C13 7    9       3.6600e-12
C14 9    10    108.4305e-12

C15 10   0      38.0273e-12
C16 10   11     15.0527e-15
L17 11   12     69.7000e-03
C18 10   12      3.6600e-12
C19 12   13     93.3131e-12

C20 13   0      38.3981e-12
C21 13   14     15.0527e-15
L22 14   15     69.7000e-03
C23 13   15      3.6600e-12
C24 15   16     93.2934e-12

C25 16   0      38.0306e-12
C26 16   17     15.0527e-15
L27 17   18     69.7000e-03
C28 16   18      3.6600e-12
C29 18   19    108.3680e-12

C30 19   0      36.3188e-12
C31 19   20     15.0527e-15
L32 20   21     69.7000e-03
C33 19   21      3.6600e-12
C34 21   22    250.9392e-09

C35 22   0      28.1544e-12
C36 22   23     15.0527e-15
L37 23   24     69.7000e-03
C38 22   24      3.6600e-12
C39 24   25     36.3135e-12
.ends
.end

```

![crystal](examples/xtal.png)

Same filter with an unloaded Q of 150000.  See the above Steder article for a figure of the loaded filter's response.


```
$ rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12 -qu 150000 | tee examples/xtalloss.cir
.SUBCKT F1 1 33
* COMMAND  : rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12 -qu 150000
* TYPE     : CHEBYSHEV_0.2
* FILTER   : CRYSTAL_MESH
* ORDER    : 8
* FREQ     : 4.915464 MHz
* RS       : 1153.4
* RL       : 1153.1
* CP       : 3.6600e-12
* BW       : 2.4000e+03
* QL       : 2048.1
* QU       : 150000.0

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.3800  366.0564e-06             -    1.7391e+03    2.8264e+03
* 12     0.7225  368.1784e-06    1.4056e-03    1.7341e+03  352.7869e-06
* 23     0.5602  975.0893e-06    2.1630e-03    1.3444e+03  273.5055e-06
* 34     0.5349  771.9015e-06    1.1676e-03    1.2839e+03  261.1881e-06
* 45     0.5298    1.5961e-03    1.5965e-03    1.2715e+03  258.6656e-06
* 56     0.5349    1.1679e-03  771.7423e-06    1.2838e+03  261.1657e-06
* 67     0.5601    2.1624e-03  975.4158e-06    1.3443e+03  273.4751e-06
* 78     0.7225    1.4059e-03  368.1121e-06    1.7341e+03  352.7793e-06
* 89     1.3803             -  366.1380e-06    1.7387e+03    2.8270e+03

* Xtal    Xtal freq     Mesh freq   Mesh offset   Xtal offset
* 1       4913570.0     4914792.0        -672.3           0.0
* 2       4913570.0     4915464.3          -0.0           0.0
* 3       4913570.0     4915239.2        -225.1           0.0
* 4       4913570.0     4915202.7        -261.6           0.0
* 5       4913570.0     4915202.6        -261.7           0.0
* 6       4913570.0     4915239.0        -225.3           0.0
* 7       4913570.0     4915464.2          -0.1           0.0
* 8       4913570.0     4914792.0        -672.3           0.0

* ij              CKij            CSi
* 12       28.1540e-12    36.3149e-12
* 23       36.3150e-12    12.6852e-06
* 34       38.0276e-12   108.4323e-12
* 45       38.3984e-12    93.3146e-12
* 56       38.0308e-12    93.2949e-12
* 67       36.3190e-12   108.3699e-12
* 78       28.1546e-12   256.8649e-09
* 89                 -    36.3139e-12

C1  1    2      15.0527e-15
L2  2    3      69.7000e-03
R3  3    4      14.3511e+00
C4  1    4       3.6600e-12
C5  4    5      36.3149e-12

C6  5    0      28.1540e-12
C7  5    6      15.0527e-15
L8  6    7      69.7000e-03
R9  7    8      14.3511e+00
C10 5    8       3.6600e-12
C11 8    9      12.6852e-06

C12 9    0      36.3150e-12
C13 9    10     15.0527e-15
L14 10   11     69.7000e-03
R15 11   12     14.3511e+00
C16 9    12      3.6600e-12
C17 12   13    108.4323e-12

C18 13   0      38.0276e-12
C19 13   14     15.0527e-15
L20 14   15     69.7000e-03
R21 15   16     14.3511e+00
C22 13   16      3.6600e-12
C23 16   17     93.3146e-12

C24 17   0      38.3984e-12
C25 17   18     15.0527e-15
L26 18   19     69.7000e-03
R27 19   20     14.3511e+00
C28 17   20      3.6600e-12
C29 20   21     93.2949e-12

C30 21   0      38.0308e-12
C31 21   22     15.0527e-15
L32 22   23     69.7000e-03
R33 23   24     14.3511e+00
C34 21   24      3.6600e-12
C35 24   25    108.3699e-12

C36 25   0      36.3190e-12
C37 25   26     15.0527e-15
L38 26   27     69.7000e-03
R39 27   28     14.3511e+00
C40 25   28      3.6600e-12
C41 28   29    256.8649e-09

C42 29   0      28.1546e-12
C43 29   30     15.0527e-15
L44 30   31     69.7000e-03
R45 31   32     14.3511e+00
C46 29   32      3.6600e-12
C47 32   33     36.3139e-12
.ends
.end

```

![crystal lossy](examples/xtalloss.png)

### 2. The Dishal program's owners manual filter.

A crystal filter with multiple crystals of different frequencies.  No parallel capacitance was used.
The filter, less the holder capacitance, is an example from the Dishal program's owners manual.


```
$ rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3 | tee examples/multiple.cir
.SUBCKT F1 1 25
* COMMAND  : rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3
* TYPE     : CHEBYSHEV_0.5
* FILTER   : CRYSTAL_MESH
* ORDER    : 8
* FREQ     : 5.001612 MHz
* RS       : 615.9
* RL       : 615.9
* BW       : 2.5000e+03
* QL       : 2000.6
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.7850  454.5465e-06             -    1.4006e+03    3.5712e+03
* 12     0.6580  329.4960e-06    1.2579e-03    1.6450e+03  328.8940e-06
* 23     0.5330    1.1473e-03    2.5078e-03    1.3325e+03  266.4141e-06
* 34     0.5150  682.4272e-06    1.0299e-03    1.2875e+03  257.4170e-06
* 45     0.5110    1.8509e-03    1.8509e-03    1.2775e+03  255.4177e-06
* 56     0.5150    1.0299e-03  682.4272e-06    1.2875e+03  257.4170e-06
* 67     0.5330    2.5078e-03    1.1473e-03    1.3325e+03  266.4141e-06
* 78     0.6580    1.2579e-03  329.4960e-06    1.6450e+03  328.8940e-06
* 89     1.7850             -  454.5465e-06    1.4006e+03    3.5712e+03

* Xtal    Xtal freq     Mesh freq   Mesh offset   Xtal offset
* 1       5000680.0     5001502.4        -109.2        1010.0
* 2       5000123.0     5001611.5          -0.0         453.0
* 3       4999670.0     5000979.6        -631.9           0.0
* 4       5000235.0     5001517.3         -94.3         565.0
* 5       5000320.0     5001602.3          -9.2         650.0
* 6       4999895.0     5001204.7        -406.8         225.0
* 7       5000010.0     5001498.5        -113.0         340.0
* 8       5000485.0     5001307.3        -304.2         815.0

* ij              CKij            CSi
* 12       43.9918e-12   331.3895e-12
* 23       54.3143e-12     9.8994e-06
* 34       56.2120e-12    57.2732e-12
* 45       56.6483e-12   383.8459e-12
* 56       56.2103e-12     3.9129e-09
* 67       54.3137e-12    88.9534e-12
* 78       43.9931e-12   320.1661e-12
* 89                 -   118.9382e-12

C1  1    2      14.4705e-15
L2  2    3      70.0000e-03
C3  3    4     331.3895e-12

C4  4    0      43.9918e-12
C5  4    5      14.4737e-15
L6  5    6      70.0000e-03
C7  6    7       9.8994e-06

C8  7    0      54.3143e-12
C9  7    8      14.4764e-15
L10 8    9      70.0000e-03
C11 9    10     57.2732e-12

C12 10   0      56.2120e-12
C13 10   11     14.4731e-15
L14 11   12     70.0000e-03
C15 12   13    383.8459e-12

C16 13   0      56.6483e-12
C17 13   14     14.4726e-15
L18 14   15     70.0000e-03
C19 15   16      3.9129e-09

C20 16   0      56.2103e-12
C21 16   17     14.4751e-15
L22 17   18     70.0000e-03
C23 18   19     88.9534e-12

C24 19   0      54.3137e-12
C25 19   20     14.4744e-15
L26 20   21     70.0000e-03
C27 21   22    320.1661e-12

C28 22   0      43.9931e-12
C29 22   23     14.4716e-15
L30 23   24     70.0000e-03
C31 24   25    118.9382e-12
.ends
.end

```

![multiple](examples/multiple.png)

The same crystal filter as above but with holder parallel capacitance across the crystals.
The filter is an example from the Dishal program's owners manual.


```
$ rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -cp 3.7e-12 -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3 | tee examples/broken.cir
.SUBCKT F1 1 25
* COMMAND  : rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -cp 3.7e-12 -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3
* TYPE     : CHEBYSHEV_0.5
* FILTER   : CRYSTAL_MESH
* ORDER    : 8
* FREQ     : 5.001933 MHz
* RS       : 810.2
* RL       : 848.6
* CP       : 3.7000e-12
* BW       : 2.5000e+03
* QL       : 2000.8
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.7850  454.5465e-06             -    1.4006e+03    3.5714e+03
* 12     0.6580  329.4960e-06    1.2579e-03    1.6450e+03  328.8729e-06
* 23     0.5330    1.1473e-03    2.5078e-03    1.3325e+03  266.3970e-06
* 34     0.5150  682.4272e-06    1.0299e-03    1.2875e+03  257.4005e-06
* 45     0.5110    1.8509e-03    1.8509e-03    1.2775e+03  255.4013e-06
* 56     0.5150    1.0299e-03  682.4272e-06    1.2875e+03  257.4005e-06
* 67     0.5330    2.5078e-03    1.1473e-03    1.3325e+03  266.3970e-06
* 78     0.6580    1.2579e-03  329.4960e-06    1.6450e+03  328.8729e-06
* 89     1.7850             -  454.5465e-06    1.4006e+03    3.5714e+03

* Xtal    Xtal freq     Mesh freq   Mesh offset   Xtal offset
* 1       5000680.0     5001720.4        -212.7        1010.0
* 2       5000123.0     5001933.1          -0.0         453.0
* 3       4999670.0     5001420.7        -512.4           0.0
* 4       5000235.0     5001854.0         -79.1         565.0
* 5       5000320.0     5001910.5         -22.6         650.0
* 6       4999895.0     5001586.4        -346.7         225.0
* 7       5000010.0     5001839.8         -93.3         340.0
* 8       5000485.0     5001571.5        -361.6         815.0

* ij              CKij            CSi
* 12       31.2521e-12   129.3251e-12
* 23       34.0134e-12     4.1971e-06
* 34       35.6967e-12    41.7146e-12
* 45       39.0856e-12   312.2147e-12
* 56       37.1512e-12     1.1170e-09
* 67       34.5346e-12    65.3900e-12
* 78       30.1050e-12   250.3087e-12
* 89                 -    72.6241e-12

C1  1    2      14.4705e-15
L2  2    3      70.0000e-03
C3  1    3       3.7000e-12
C4  3    4     129.3251e-12

C5  4    0      31.2521e-12
C6  4    5      14.4737e-15
L7  5    6      70.0000e-03
C8  4    6       3.7000e-12
C9  6    7       4.1971e-06

C10 7    0      34.0134e-12
C11 7    8      14.4764e-15
L12 8    9      70.0000e-03
C13 7    9       3.7000e-12
C14 9    10     41.7146e-12

C15 10   0      35.6967e-12
C16 10   11     14.4731e-15
L17 11   12     70.0000e-03
C18 10   12      3.7000e-12
C19 12   13    312.2147e-12

C20 13   0      39.0856e-12
C21 13   14     14.4726e-15
L22 14   15     70.0000e-03
C23 13   15      3.7000e-12
C24 15   16      1.1170e-09

C25 16   0      37.1512e-12
C26 16   17     14.4751e-15
L27 17   18     70.0000e-03
C28 16   18      3.7000e-12
C29 18   19     65.3900e-12

C30 19   0      34.5346e-12
C31 19   20     14.4744e-15
L32 20   21     70.0000e-03
C33 19   21      3.7000e-12
C34 21   22    250.3087e-12

C35 22   0      30.1050e-12
C36 22   23     14.4716e-15
L37 23   24     70.0000e-03
C38 22   24      3.7000e-12
C39 24   25     72.6241e-12
.ends
.end

```

![broken](examples/broken.png)

### 3. The Design Filter in N6NWP's QEX 1995 article.

N6NWP recommends using the lowest frequency crystal for the reference mesh, while the Dishal program recommends using a crystal in the middle.   
Using the middle crystal for the reference mesh seems to require more pulling of the crystal.
In general, you want the crystals meshes to use the same series capacitor, except for the reference meshes.

The following example uses the lowest crystal for the reference mesh.


```
$ rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -f 8000017.0,7999933.0,7999940.0,7999945.0,7999985.0,7999996.0,8000000.0,7999991.0,7999966.0,7999945.0,7999939.0,8000026.0 | tee examples/qexlow.cir
.SUBCKT F1 1 37
* COMMAND  : rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -f 8000017.0,7999933.0,7999940.0,7999945.0,7999985.0,7999996.0,8000000.0,7999991.0,7999966.0,7999945.0,7999939.0,8000026.0
* TYPE     : CHEBYSHEV_0.1
* FILTER   : CRYSTAL_MESH
* ORDER    : 12
* FREQ     : 8.001741 MHz
* RS       : 241.8
* RL       : 239.7
* CP       : 5.0000e-12
* BW       : 2.5000e+03
* QL       : 3200.7
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.2010  305.8321e-06             -    2.0816e+03    3.8440e+03
* 12     0.7560  371.0220e-06    2.2617e-03    1.8899e+03  236.1861e-06
* 23     0.5646  854.0891e-06    3.0755e-03    1.4115e+03  176.4021e-06
* 34     0.5322  788.6446e-06    2.0360e-03    1.3304e+03  166.2691e-06
* 45     0.5214    1.4253e-03    2.5726e-03    1.3035e+03  162.8992e-06
* 56     0.5172    1.2131e-03    1.6315e-03    1.2929e+03  161.5746e-06
* 67     0.5160    1.9990e-03    2.0066e-03    1.2900e+03  161.2156e-06
* 78     0.5171    1.6359e-03    1.2101e-03    1.2927e+03  161.5552e-06
* 89     0.5213    2.5635e-03    1.4312e-03    1.3032e+03  162.8616e-06
* 910    0.5320    2.0418e-03  786.8382e-06    1.3299e+03  166.1990e-06
* 1011   0.5642    3.0655e-03  858.3063e-06    1.4104e+03  176.2658e-06
* 1112   0.7538    2.2691e-03  370.3100e-06    1.8846e+03  235.5240e-06
* 1213   1.2101             -  308.1454e-06    2.0660e+03    3.8731e+03

* Xtal    Xtal freq     Mesh freq   Mesh offset   Xtal offset
* 1       8000017.0     8001111.5        -629.2          84.0
* 2       7999933.0     8001739.0          -1.7           0.0
* 3       7999940.0     8001469.7        -271.0           7.0
* 4       7999945.0     8001418.5        -322.2          12.0
* 5       7999985.0     8001435.0        -305.7          52.0
* 6       7999996.0     8001436.6        -304.1          63.0
* 7       8000000.0     8001440.0        -300.7          67.0
* 8       7999991.0     8001439.2        -301.4          58.0
* 9       7999966.0     8001436.4        -304.2          33.0
* 10      7999945.0     8001472.3        -268.3          12.0
* 11      7999939.0     8001740.7          -0.0           6.0
* 12      8000026.0     8001116.5        -624.2          93.0

* ij              CKij            CSi
* 12       90.2069e-12   136.0937e-12
* 23      120.2819e-12    51.2891e-09
* 34      127.6944e-12   313.3347e-12
* 45      130.6506e-12   263.6841e-12
* 56      132.0819e-12   279.1111e-12
* 67      132.4822e-12   280.9150e-12
* 78      132.1684e-12   284.2570e-12
* 89      130.8699e-12   283.2620e-12
* 910     127.9264e-12   279.9100e-12
* 1011    120.4459e-12   316.6422e-12
* 1112     90.5331e-12    12.2375e-06
* 1213               -   137.3105e-12

C1  1    2      25.5345e-15
L2  2    3      15.5000e-03
C3  1    3       5.0000e-12
C4  3    4     136.0937e-12

C5  4    0      90.2069e-12
C6  4    5      25.5350e-15
L7  5    6      15.5000e-03
C8  4    6       5.0000e-12
C9  6    7      51.2891e-09

C10 7    0     120.2819e-12
C11 7    8      25.5350e-15
L12 8    9      15.5000e-03
C13 7    9       5.0000e-12
C14 9    10    313.3347e-12

C15 10   0     127.6944e-12
C16 10   11     25.5349e-15
L17 11   12     15.5000e-03
C18 10   12      5.0000e-12
C19 12   13    263.6841e-12

C20 13   0     130.6506e-12
C21 13   14     25.5347e-15
L22 14   15     15.5000e-03
C23 13   15      5.0000e-12
C24 15   16    279.1111e-12

C25 16   0     132.0819e-12
C26 16   17     25.5346e-15
L27 17   18     15.5000e-03
C28 16   18      5.0000e-12
C29 18   19    280.9150e-12

C30 19   0     132.4822e-12
C31 19   20     25.5346e-15
L32 20   21     15.5000e-03
C33 19   21      5.0000e-12
C34 21   22    284.2570e-12

C35 22   0     132.1684e-12
C36 22   23     25.5346e-15
L37 23   24     15.5000e-03
C38 22   24      5.0000e-12
C39 24   25    283.2620e-12

C40 25   0     130.8699e-12
C41 25   26     25.5348e-15
L42 26   27     15.5000e-03
C43 25   27      5.0000e-12
C44 27   28    279.9100e-12

C45 28   0     127.9264e-12
C46 28   29     25.5349e-15
L47 29   30     15.5000e-03
C48 28   30      5.0000e-12
C49 30   31    316.6422e-12

C50 31   0     120.4459e-12
C51 31   32     25.5350e-15
L52 32   33     15.5000e-03
C53 31   33      5.0000e-12
C54 33   34     12.2375e-06

C55 34   0      90.5331e-12
C56 34   35     25.5344e-15
L57 35   36     15.5000e-03
C58 34   36      5.0000e-12
C59 36   37    137.3105e-12
.ends
.end

```


```
$ rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -qu 120000 -f 8000017.0,7999933.0,7999940.0,7999945.0,7999985.0,7999996.0,8000000.0,7999991.0,7999966.0,7999945.0,7999939.0,8000026.0 > examples/qexloss.cir
```


The following example uses a middle crystal for the reference mesh.


```
$ rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -f 8000017.0,7999966.0,7999940.0,7999945.0,7999985.0,8000000.0,7999996.0,7999991.0,7999939.0,7999933.0,7999945.0,8000026.0 | tee examples/qexmiddle.cir
.SUBCKT F1 1 37
* COMMAND  : rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -f 8000017.0,7999966.0,7999940.0,7999945.0,7999985.0,8000000.0,7999996.0,7999991.0,7999939.0,7999933.0,7999945.0,8000026.0
* TYPE     : CHEBYSHEV_0.1
* FILTER   : CRYSTAL_MESH
* ORDER    : 12
* FREQ     : 8.001775 MHz
* RS       : 242.7
* RL       : 240.6
* CP       : 5.0000e-12
* BW       : 2.5000e+03
* QL       : 3200.7
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.2010  305.8321e-06             -    2.0816e+03    3.8441e+03
* 12     0.7560  371.0220e-06    2.2617e-03    1.8899e+03  236.1850e-06
* 23     0.5646  854.0891e-06    3.0755e-03    1.4115e+03  176.4013e-06
* 34     0.5322  788.6446e-06    2.0360e-03    1.3304e+03  166.2684e-06
* 45     0.5214    1.4253e-03    2.5726e-03    1.3035e+03  162.8985e-06
* 56     0.5172    1.2131e-03    1.6315e-03    1.2929e+03  161.5739e-06
* 67     0.5160    1.9990e-03    2.0066e-03    1.2900e+03  161.2149e-06
* 78     0.5171    1.6359e-03    1.2101e-03    1.2927e+03  161.5545e-06
* 89     0.5213    2.5635e-03    1.4312e-03    1.3032e+03  162.8609e-06
* 910    0.5320    2.0418e-03  786.8382e-06    1.3299e+03  166.1983e-06
* 1011   0.5642    3.0655e-03  858.3063e-06    1.4104e+03  176.2650e-06
* 1112   0.7538    2.2691e-03  370.3100e-06    1.8846e+03  235.5230e-06
* 1213   1.2101             -  308.1454e-06    2.0660e+03    3.8731e+03

* Xtal    Xtal freq     Mesh freq   Mesh offset   Xtal offset
* 1       8000017.0     8001115.7        -659.5          84.0
* 2       7999966.0     8001775.2          -0.0          33.0
* 3       7999940.0     8001474.6        -300.7           7.0
* 4       7999945.0     8001424.6        -350.7          12.0
* 5       7999985.0     8001440.8        -334.4          52.0
* 6       8000000.0     8001446.2        -329.0          67.0
* 7       7999996.0     8001442.2        -333.0          63.0
* 8       7999991.0     8001446.3        -328.9          58.0
* 9       7999939.0     8001418.8        -356.4           6.0
* 10      7999933.0     8001468.5        -306.7           0.0
* 11      7999945.0     8001752.7         -22.5          12.0
* 12      8000026.0     8001122.0        -653.2          93.0

* ij              CKij            CSi
* 12       90.0326e-12   129.3563e-12
* 23      120.0486e-12    13.1039e-06
* 34      127.2212e-12   281.3962e-12
* 45      130.1670e-12   241.4203e-12
* 56      131.6219e-12   254.2288e-12
* 67      131.9927e-12   258.8368e-12
* 78      131.6518e-12   255.6140e-12
* 89      130.1970e-12   258.6378e-12
* 910     127.1859e-12   237.3806e-12
* 1011    119.9609e-12   275.6183e-12
* 1112     90.2273e-12     3.7629e-09
* 1213               -   130.7340e-12

C1  1    2      25.5345e-15
L2  2    3      15.5000e-03
C3  1    3       5.0000e-12
C4  3    4     129.3563e-12

C5  4    0      90.0326e-12
C6  4    5      25.5348e-15
L7  5    6      15.5000e-03
C8  4    6       5.0000e-12
C9  6    7      13.1039e-06

C10 7    0     120.0486e-12
C11 7    8      25.5350e-15
L12 8    9      15.5000e-03
C13 7    9       5.0000e-12
C14 9    10    281.3962e-12

C15 10   0     127.2212e-12
C16 10   11     25.5349e-15
L17 11   12     15.5000e-03
C18 10   12      5.0000e-12
C19 12   13    241.4203e-12

C20 13   0     130.1670e-12
C21 13   14     25.5347e-15
L22 14   15     15.5000e-03
C23 13   15      5.0000e-12
C24 15   16    254.2288e-12

C25 16   0     131.6219e-12
C26 16   17     25.5346e-15
L27 17   18     15.5000e-03
C28 16   18      5.0000e-12
C29 18   19    258.8368e-12

C30 19   0     131.9927e-12
C31 19   20     25.5346e-15
L32 20   21     15.5000e-03
C33 19   21      5.0000e-12
C34 21   22    255.6140e-12

C35 22   0     131.6518e-12
C36 22   23     25.5346e-15
L37 23   24     15.5000e-03
C38 22   24      5.0000e-12
C39 24   25    258.6378e-12

C40 25   0     130.1970e-12
C41 25   26     25.5350e-15
L42 26   27     15.5000e-03
C43 25   27      5.0000e-12
C44 27   28    237.3806e-12

C45 28   0     127.1859e-12
C46 28   29     25.5350e-15
L47 29   30     15.5000e-03
C48 28   30      5.0000e-12
C49 30   31    275.6183e-12

C50 31   0     119.9609e-12
C51 31   32     25.5349e-15
L52 32   33     15.5000e-03
C53 31   33      5.0000e-12
C54 33   34      3.7629e-09

C55 34   0      90.2273e-12
C56 34   35     25.5344e-15
L57 35   36     15.5000e-03
C58 34   36      5.0000e-12
C59 36   37    130.7340e-12
.ends
.end

```


## Lowpass and highpass filters.


```
$ rffilter.py -g butterworth -lowpass -f 10e6 -n 5
.SUBCKT F1 1 4
* COMMAND  : rffilter.py -g butterworth -lowpass -f 10e6 -n 5
* TYPE     : BUTTERWORTH
* FILTER   : LOWPASS
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0

L1  1    2     491.8126e-09

C2  2    0     515.0349e-12
L3  2    3       1.5915e-06

C4  3    0     515.0349e-12
L5  3    4     491.8126e-09
.ends
.end

.SUBCKT F1 1 3
* COMMAND  : rffilter.py -g butterworth -lowpass -f 10e6 -n 5
* TYPE     : BUTTERWORTH
* FILTER   : LOWPASS
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0

C1  1    0     196.7251e-12
L2  1    2       1.2876e-06

C3  2    0     636.6198e-12
L4  2    3       1.2876e-06

C5  3    0     196.7251e-12
.ends
.end

```

![lowpass](examples/lowpass.png)

## Wide band bandpass filters.


```
$ rffilter.py -g butterworth -bandpass -f 10e6 -bw 1e6 -n 4
.SUBCKT F1 1 5
* COMMAND  : rffilter.py -g butterworth -bandpass -f 10e6 -bw 1e6 -n 4
* TYPE     : BUTTERWORTH
* FILTER   : BANDPASS
* ORDER    : 4
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : inf

L1  1    2       6.0906e-06
C2  2    3      41.5890e-12

L3  3    0      43.0670e-09
C4  3    0       5.8816e-09
L5  3    4      14.7040e-06
C6  4    5      17.2268e-12

L7  5    0     103.9726e-09
C8  5    0       2.4362e-09
.ends
.end

.SUBCKT F1 1 5
* COMMAND  : rffilter.py -g butterworth -bandpass -f 10e6 -bw 1e6 -n 4
* TYPE     : BUTTERWORTH
* FILTER   : BANDPASS
* ORDER    : 4
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : inf

L1  1    0     103.9726e-09
C2  1    0       2.4362e-09
L3  1    2      14.7040e-06
C4  2    3      17.2268e-12

L5  3    0      43.0670e-09
C6  3    0       5.8816e-09
L7  3    4       6.0906e-06
C8  4    5      41.5890e-12
.ends
.end

```


## Use of Zverev filter tables with an unloaded Q.


```
$ rffilter.py -zverev butterworth -nodal -qu 2500 -bw 1e6 -f 10e6 -n 3
.SUBCKT F1 1 3
* COMMAND  : rffilter.py -zverev butterworth -nodal -qu 2500 -bw 1e6 -f 10e6 -n 3
* TYPE     : BUTTERWORTH
* FILTER   : NODAL
* ORDER    : 3
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 20.0

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.8041  511.9060e-09             -    1.2436e+06    8.0410e+00
* 12     0.7687    1.3399e-06    1.5619e-06  768.7000e+03   76.8700e-03
* 23     0.6582    1.2101e-06    1.0381e-06  658.2000e+03   65.8200e-03
* 34     1.4156             -  901.1989e-09  706.4142e+03   14.1560e+00

L1  1    1001   98.9646e-09
R1  1001 0       2.4873e-03
C2  1    0       2.3628e-09
C3  1    2     196.7511e-12

L4  2    1004   98.9646e-09
R4  1004 0       2.4873e-03
C5  2    0       2.1393e-09
C6  2    3     223.5287e-12

L7  3    1007   56.2147e-09
R7  1007 0       1.4128e-03
C8  3    0       4.2825e-09
.ends
.end

```


```
$ rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.0975   62.0704e-09             -   10.2564e+06  975.0000e-03
* 12     5.9216  186.2076e-09    1.8516e-06    5.9216e+06  592.1600e-03
* 23     2.7188  356.5183e-09    2.1501e-06    2.7188e+06  271.8800e-03
* 34     1.8573  585.2213e-09    1.7763e-06    1.8573e+06  185.7300e-03
* 45     1.4616  831.9798e-09    1.9966e-06    1.4616e+06  146.1600e-03
* 56     1.2253    1.1530e-06    1.4191e-06    1.2253e+06  122.5300e-03
* 67     1.0138    1.5265e-06    1.6676e-06    1.0138e+06  101.3800e-03
* 78     0.6333    2.6079e-06  842.4306e-09  633.3000e+03   63.3300e-03
* 89     1.8842             -    1.1995e-06  530.7292e+03   18.8420e+00

L1  1    1001  816.1792e-09
R1  1001 0      20.5128e-03
C2  1    0     126.5740e-12
C3  1    2     183.7781e-12

L4  2    1004  816.1792e-09
R4  1004 0      20.5128e-03
C5  2    0      42.1955e-12
C6  2    3      84.3785e-12

L7  3    1007  816.1792e-09
R7  1007 0      20.5128e-03
C8  3    0     168.3319e-12
C9  3    4      57.6417e-12

L10 4    1010  816.1792e-09
R10 1010 0      20.5128e-03
C11 4    0     207.3494e-12
C12 4    5      45.3611e-12

L13 5    1013  816.1792e-09
R13 1013 0      20.5128e-03
C14 5    0     226.9636e-12
C15 5    6      38.0274e-12

L16 6    1016  816.1792e-09
R16 1016 0      20.5128e-03
C17 6    0     240.8612e-12
C18 6    7      31.4635e-12

L19 7    1019  816.1792e-09
R19 1019 0      20.5128e-03
C20 7    0     192.4863e-12
C21 7    8      86.4023e-12

L22 8    1022   42.2341e-09
R22 1022 0       1.0615e-03
C23 8    0       5.9112e-09
.ends
.end

.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.1192   75.8851e-09             -    8.3893e+06    1.1920e+00
* 12     4.8959  222.8121e-09    2.6848e-06    4.8959e+06  489.5900e-03
* 23     2.3142  415.5257e-09    1.4829e-06    2.3142e+06  231.4200e-03
* 34     1.6364  668.4290e-09    2.6052e-06    1.6364e+06  163.6400e-03
* 45     1.3128  943.2432e-09    1.2707e-06    1.3128e+06  131.2800e-03
* 56     1.1222    1.2783e-06    2.2486e-06    1.1222e+06  112.2200e-03
* 67     0.6417    2.5571e-06  846.2446e-09  641.7000e+03   64.1700e-03
* 78     0.9493    1.5569e-06    1.6945e-06  949.3000e+03   94.9300e-03
* 89     0.4169             -  265.4068e-09    2.3987e+06    4.1690e+00

L1  1    1001  667.5962e-09
R1  1001 0      16.7785e-03
C2  1    0     193.6625e-12
C3  1    2     185.7629e-12

L4  2    1004  667.5962e-09
R4  1004 0      16.7785e-03
C5  2    0     105.8559e-12
C6  2    3      87.8066e-12

L7  3    1007  667.5962e-09
R7  1007 0      16.7785e-03
C8  3    0     229.5296e-12
C9  3    4      62.0892e-12

L10 4    1010  667.5962e-09
R10 1010 0      16.7785e-03
C11 4    0     267.5252e-12
C12 4    5      49.8110e-12

L13 5    1013  667.5962e-09
R13 1013 0      16.7785e-03
C14 5    0     287.0353e-12
C15 5    6      42.5791e-12

L16 6    1016  667.5962e-09
R16 1016 0      16.7785e-03
C17 6    0     312.4985e-12
C18 6    7      24.3477e-12

L19 7    1019  667.5962e-09
R19 1019 0      16.7785e-03
C20 7    0     287.7168e-12
C21 7    8      67.3609e-12

L22 8    1022  190.8790e-09
R22 1022 0       4.7973e-03
C23 8    0       1.2597e-09
.ends
.end

.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.1474   93.8378e-09             -    6.7843e+06    1.4740e+00
* 12     4.0137  268.0975e-09    1.5752e-06    4.0137e+06  401.3700e-03
* 23     1.9766  480.7655e-09    2.5273e-06    1.9766e+06  197.6600e-03
* 34     1.4331  778.1060e-09    1.4780e-06    1.4331e+06  143.3100e-03
* 45     1.2361    1.0009e-06    2.2687e-06    1.2361e+06  123.6100e-03
* 56     0.6818    2.4545e-06    1.0769e-06  681.8000e+03   68.1800e-03
* 67     0.6825    1.5199e-06    1.7766e-06  682.5000e+03   68.2500e-03
* 78     2.1762    2.6194e-06  537.9182e-09    2.1762e+06  217.6200e-03
* 89     0.2499             -  159.0913e-09    4.0016e+06    2.4990e+00

L1  1    1001  539.8743e-09
R1  1001 0      13.5685e-03
C2  1    0     280.8705e-12
C3  1    2     188.3183e-12

L4  2    1004  539.8743e-09
R4  1004 0      13.5685e-03
C5  2    0     188.1306e-12
C6  2    3      92.7399e-12

L7  3    1007  539.8743e-09
R7  1007 0      13.5685e-03
C8  3    0     309.2095e-12
C9  3    4      67.2394e-12

L10 4    1010  539.8743e-09
R10 1010 0      13.5685e-03
C11 4    0     343.9529e-12
C12 4    5      57.9964e-12

L13 5    1013  539.8743e-09
R13 1013 0      13.5685e-03
C14 5    0     379.2031e-12
C15 5    6      31.9893e-12

L16 6    1016  539.8743e-09
R16 1016 0      13.5685e-03
C17 6    0     405.1773e-12
C18 6    7      32.0221e-12

L19 7    1019  539.8743e-09
R19 1019 0      13.5685e-03
C20 7    0     304.2189e-12
C21 7    8     132.9477e-12

L22 8    1022  318.4373e-09
R22 1022 0       8.0032e-03
C23 8    0     662.5087e-12
.ends
.end

.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.2034  129.4885e-09             -    4.9164e+06    2.0340e+00
* 12     3.1367  318.1143e-09    2.6241e-06    3.1367e+06  313.6700e-03
* 23     1.6246  612.1961e-09    1.5171e-06    1.6246e+06  162.4600e-03
* 34     1.3923  751.2365e-09    2.4902e-06    1.3923e+06  139.2300e-03
* 45     0.7691    2.1941e-06    1.2094e-06  769.1000e+03   76.9100e-03
* 56     0.6027    1.4565e-06    1.9911e-06  602.7000e+03   60.2700e-03
* 67     1.2931    2.5378e-06  790.5759e-09    1.2931e+06  129.3100e-03
* 78     3.2425    1.5687e-06  355.3453e-09    3.2425e+06  324.2500e-03
* 89     0.1704             -  108.4800e-09    5.8685e+06    1.7040e+00

L1  1    1001  391.2363e-09
R1  1001 0       9.8328e-03
C2  1    0     444.3591e-12
C3  1    2     203.0832e-12

L4  2    1004  391.2363e-09
R4  1004 0       9.8328e-03
C5  2    0     339.1756e-12
C6  2    3     105.1835e-12

L7  3    1007  391.2363e-09
R7  1007 0       9.8328e-03
C8  3    0     452.1154e-12
C9  3    4      90.1434e-12

L10 4    1010  391.2363e-09
R10 1010 0       9.8328e-03
C11 4    0     507.5041e-12
C12 4    5      49.7948e-12

L13 5    1013  391.2363e-09
R13 1013 0       9.8328e-03
C14 5    0     558.6262e-12
C15 5    6      39.0213e-12

L16 6    1016  391.2363e-09
R16 1016 0       9.8328e-03
C17 6    0     524.7002e-12
C18 6    7      83.7208e-12

L19 7    1019  391.2363e-09
R19 1019 0       9.8328e-03
C20 7    0     371.5715e-12
C21 7    8     192.1500e-12

L22 8    1022  467.0039e-09
R22 1022 0      11.7371e-03
C23 8    0     350.2500e-12
.ends
.end

.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.1332   84.7978e-09             -    7.5075e+06    1.3320e+00
* 12     4.3253  255.4721e-09    1.5909e-06    4.3253e+06  432.5300e-03
* 23     2.0981  445.1809e-09    2.4956e-06    2.0981e+06  209.8100e-03
* 34     1.4629  780.9646e-09    1.4955e-06    1.4629e+06  146.2900e-03
* 45     1.1695    1.0091e-06    2.2684e-06    1.1695e+06  116.9500e-03
* 56     0.6307    2.5878e-06    1.0903e-06  630.7000e+03   63.0700e-03
* 67     0.7436    1.4147e-06    1.8011e-06  743.6000e+03   74.3600e-03
* 78     2.1384    2.8063e-06  456.1605e-09    2.1384e+06  213.8400e-03
* 89     0.3052             -  194.2964e-09    3.2765e+06    3.0520e+00

L1  1    1001  597.4285e-09
R1  1001 0      15.0150e-03
C2  1    0     240.6009e-12
C3  1    2     183.3879e-12

L4  2    1004  597.4285e-09
R4  1004 0      15.0150e-03
C5  2    0     151.6438e-12
C6  2    3      88.9571e-12

L7  3    1007  597.4285e-09
R7  1007 0      15.0150e-03
C8  3    0     273.0064e-12
C9  3    4      62.0253e-12

L10 4    1010  597.4285e-09
R10 1010 0      15.0150e-03
C11 4    0     312.3780e-12
C12 4    5      49.5855e-12

L13 5    1013  597.4285e-09
R13 1013 0      15.0150e-03
C14 5    0     347.6623e-12
C15 5    6      26.7410e-12

L16 6    1016  597.4285e-09
R16 1016 0      15.0150e-03
C17 6    0     365.7200e-12
C18 6    7      31.5278e-12

L19 7    1019  597.4285e-09
R19 1019 0      15.0150e-03
C20 7    0     255.2201e-12
C21 7    8     137.2409e-12

L22 8    1022  260.7388e-09
R22 1022 0       6.5531e-03
C23 8    0     834.2409e-12
.ends
.end

.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.1772  112.8090e-09             -    5.6433e+06    1.7720e+00
* 12     3.3376  322.5135e-09    2.5625e-06    3.3376e+06  333.7600e-03
* 23     1.0876    1.1752e-06    1.9523e-06    1.0876e+06  108.7600e-03
* 34     1.3420  534.3404e-09    2.5140e-06    1.3420e+06  134.2000e-03
* 45     0.6980    5.1022e-06    1.2016e-06  698.0000e+03   69.8000e-03
* 56     0.6410  785.5151e-09    2.0576e-06  641.0000e+03   64.1000e-03
* 67     1.3675    5.9651e-06  708.4631e-09    1.3675e+06  136.7500e-03
* 78     2.9724  838.6790e-09  370.6546e-09    2.9724e+06  297.2400e-03
* 89     0.1944             -  123.7589e-09    5.1440e+06    1.9440e+00

L1  1    1001  449.0828e-09
R1  1001 0      11.2867e-03
C2  1    0     375.7894e-12
C3  1    2     188.2557e-12

L4  2    1004  449.0828e-09
R4  1004 0      11.2867e-03
C5  2    0     314.4439e-12
C6  2    3      61.3455e-12

L7  3    1007  449.0828e-09
R7  1007 0      11.2867e-03
C8  3    0     427.0047e-12
C9  3    4      75.6949e-12

L10 4    1010  449.0828e-09
R10 1010 0      11.2867e-03
C11 4    0     448.9799e-12
C12 4    5      39.3703e-12

L13 5    1013  449.0828e-09
R13 1013 0      11.2867e-03
C14 5    0     488.5195e-12
C15 5    6      36.1553e-12

L16 6    1016  449.0828e-09
R16 1016 0      11.2867e-03
C17 6    0     450.7567e-12
C18 6    7      77.1332e-12

L19 7    1019  449.0828e-09
R19 1019 0      11.2867e-03
C20 7    0     311.3067e-12
C21 7    8     175.6052e-12

L22 8    1022  409.3491e-09
R22 1022 0      10.2881e-03
C23 8    0     443.1892e-12
.ends
.end

.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.2476  157.6271e-09             -    4.0388e+06    2.4760e+00
* 12     2.5022  410.6629e-09    1.5610e-06    2.5022e+06  250.2200e-03
* 23     1.5729  556.5349e-09    2.5503e-06    1.5729e+06  157.2900e-03
* 34     0.7831    2.0674e-06    1.3976e-06  783.1000e+03   78.3100e-03
* 45     0.6019    1.2318e-06    2.1541e-06  601.9000e+03   60.1900e-03
* 56     1.1206    2.5454e-06  984.1625e-09    1.1206e+06  112.0600e-03
* 67     1.7580    1.5061e-06  555.5318e-09    1.7580e+06  175.8000e-03
* 78     3.8868    2.6431e-06  284.3463e-09    3.8868e+06  388.6800e-03
* 89     0.1482             -   94.3471e-09    6.7476e+06    1.4820e+00

L1  1    1001  321.3953e-09
R1  1001 0       8.0775e-03
C2  1    0     590.9281e-12
C3  1    2     197.2072e-12

L4  2    1004  321.3953e-09
R4  1004 0       8.0775e-03
C5  2    0     466.9623e-12
C6  2    3     123.9658e-12

L7  3    1007  321.3953e-09
R7  1007 0       8.0775e-03
C8  3    0     602.4506e-12
C9  3    4      61.7189e-12

L10 4    1010  321.3953e-09
R10 1010 0       8.0775e-03
C11 4    0     678.9785e-12
C12 4    5      47.4379e-12

L13 5    1013  321.3953e-09
R13 1013 0       8.0775e-03
C14 5    0     652.3790e-12
C15 5    6      88.3184e-12

L16 6    1016  321.3953e-09
R16 1016 0       8.0775e-03
C17 6    0     561.2627e-12
C18 6    7     138.5542e-12

L19 7    1019  321.3953e-09
R19 1019 0       8.0775e-03
C20 7    0     412.5847e-12
C21 7    8     236.9964e-12

L22 8    1022  536.9600e-09
R22 1022 0      13.4953e-03
C23 8    0     234.7389e-12
.ends
.end

.SUBCKT F1 1 8
* COMMAND  : rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8
* TYPE     : BESSEL
* FILTER   : NODAL
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : 2500.0
* QO       : 250.0
* qo       : 11.2

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.4606  293.2271e-09             -    2.1711e+06    4.6060e+00
* 12     2.1216  307.0642e-09    2.6107e-06    2.1216e+06  212.1600e-03
* 23     0.9547    1.7413e-06    1.5248e-06  954.7000e+03   95.4700e-03
* 34     0.5810    1.1362e-06    2.3019e-06  581.0000e+03   58.1000e-03
* 45     0.9670    2.2641e-06    1.2332e-06  967.0000e+03   96.7000e-03
* 56     1.4066    1.5280e-06  776.8161e-09    1.4066e+06  140.6600e-03
* 67     2.1941    2.4789e-06  445.9809e-09    2.1941e+06  219.4100e-03
* 78     4.9228    1.6059e-06  226.2682e-09    4.9228e+06  492.2800e-03
* 89     0.1161             -   73.9116e-09    8.6133e+06    1.1610e+00

L1  1    1001  172.7692e-09
R1  1001 0       4.3422e-03
C2  1    0       1.1551e-09
C3  1    2     311.0553e-12

L4  2    1004  172.7692e-09
R4  1004 0       4.3422e-03
C5  2    0       1.0151e-09
C6  2    3     139.9719e-12

L7  3    1007  172.7692e-09
R7  1007 0       4.3422e-03
C8  3    0       1.2410e-09
C9  3    4      85.1825e-12

L10 4    1010  172.7692e-09
R10 1010 0       4.3422e-03
C11 4    0       1.2392e-09
C12 4    5     141.7753e-12

L13 5    1013  172.7692e-09
R13 1013 0       4.3422e-03
C14 5    0       1.1181e-09
C15 5    6     206.2266e-12

L16 6    1016  172.7692e-09
R16 1016 0       4.3422e-03
C17 6    0     938.2240e-12
C18 6    7     321.6848e-12

L19 7    1019  172.7692e-09
R19 1019 0       4.3422e-03
C20 7    0     782.0905e-12
C21 7    8     362.3601e-12

L22 8    1022  685.4218e-09
R22 1022 0      17.2265e-03
C23 8    0       7.1977e-12
.ends
.end

```


## More examples


```
$ rffilter.py -k butterworth -nodal -f 10e6 -bw 1e6 -n 5
.SUBCKT F1 1 5
* COMMAND  : rffilter.py -k butterworth -nodal -f 10e6 -bw 1e6 -n 5
* TYPE     : BUTTERWORTH
* FILTER   : NODAL
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 1.0000e+06
* QL       : 10.0
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.6180  393.4310e-09             -    1.6181e+06    6.1800e+00
* 12     1.0000    1.0301e-06    2.0595e-06    1.0000e+06  100.0000e-03
* 23     0.5560    1.6661e-06    2.0603e-06  556.0000e+03   55.6000e-03
* 34     0.5560    2.0603e-06    1.6661e-06  556.0000e+03   55.6000e-03
* 45     1.0000    2.0595e-06    1.0301e-06    1.0000e+06  100.0000e-03
* 56     0.6180             -  393.4310e-09    1.6181e+06    6.1800e+00

L1  1    0     128.7661e-09
C2  1    0       1.7704e-09
C3  1    2     196.7155e-12

L4  2    0     128.7661e-09
C5  2    0       1.6611e-09
C6  2    3     109.3738e-12

L7  3    0     128.7661e-09
C8  3    0       1.7484e-09
C9  3    4     109.3738e-12

L10 4    0     128.7661e-09
C11 4    0       1.6611e-09
C12 4    5     196.7155e-12

L13 5    0     128.7661e-09
C14 5    0       1.7704e-09
.ends
.end

```


```
$ rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -l 100e-9,100e-9,100e-9,100e-9,100e-9
.SUBCKT F1 1 5
* COMMAND  : rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -l 100e-9,100e-9,100e-9,100e-9,100e-9
* TYPE     : BUTTERWORTH
* FILTER   : NODAL
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 97.1
* RL       : 97.1
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.6180  983.6253e-09             -  647.2178e+03   15.4507e+00
* 12     1.0000    2.5752e-06    5.1503e-06  400.0018e+03   40.0002e-03
* 23     0.5559    4.1667e-06    5.1503e-06  222.3575e+03   22.2357e-03
* 34     0.5559    5.1503e-06    4.1667e-06  222.3575e+03   22.2357e-03
* 45     1.0000    5.1503e-06    2.5752e-06  400.0018e+03   40.0002e-03
* 56     0.6180             -  983.6253e-09  647.2178e+03   15.4507e+00

L1  1    0     100.0000e-09
C2  1    0       2.4317e-09
C3  1    2     101.3216e-12

L4  2    0     100.0000e-09
C5  2    0       2.3754e-09
C6  2    3      56.3238e-12

L7  3    0     100.0000e-09
C8  3    0       2.4204e-09
C9  3    4      56.3238e-12

L10 4    0     100.0000e-09
C11 4    0       2.3754e-09
C12 4    5     101.3216e-12

L13 5    0     100.0000e-09
C14 5    0       2.4317e-09
.ends
.end

```


```
$ rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -r 100,120
.SUBCKT F1 1 5
* COMMAND  : rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -r 100,120
* TYPE     : BUTTERWORTH
* FILTER   : NODAL
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 100.0
* RL       : 120.0
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.6180  983.6253e-09             -  647.2178e+03   15.4507e+00
* 12     1.0000    2.5752e-06    5.1503e-06  400.0018e+03   40.0002e-03
* 23     0.5559    4.1667e-06    5.1503e-06  222.3575e+03   22.2357e-03
* 34     0.5559    5.1503e-06    4.1667e-06  222.3575e+03   22.2357e-03
* 45     1.0000    5.1503e-06    2.5752e-06  400.0018e+03   40.0002e-03
* 56     0.6180             -  983.6253e-09  647.2178e+03   15.4507e+00

L1  1    0     103.0079e-09
C2  1    0       2.3607e-09
C3  1    2      98.3630e-12

L4  2    0     103.0079e-09
C5  2    0       2.3060e-09
C6  2    3      54.6791e-12

L7  3    0     103.0079e-09
C8  3    0       2.3497e-09
C9  3    4      54.6791e-12

L10 4    0     103.0079e-09
C11 4    0       2.3146e-09
C12 4    5      89.7927e-12

L13 5    0     123.6095e-09
C14 5    0       1.9594e-09
.ends
.end

```


```
$ rffilter.py -g butterworth -lowpass -f 10e6 -n 5 -r 75
.SUBCKT F1 1 4
* COMMAND  : rffilter.py -g butterworth -lowpass -f 10e6 -n 5 -r 75
* TYPE     : BUTTERWORTH
* FILTER   : LOWPASS
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 75.0
* RL       : 75.0

L1  1    2     737.7190e-09

C2  2    0     343.3566e-12
L3  2    3       2.3873e-06

C4  3    0     343.3566e-12
L5  3    4     737.7190e-09
.ends
.end

.SUBCKT F1 1 3
* COMMAND  : rffilter.py -g butterworth -lowpass -f 10e6 -n 5 -r 75
* TYPE     : BUTTERWORTH
* FILTER   : LOWPASS
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 75.0
* RL       : 75.0

C1  1    0     131.1500e-12
L2  1    2       1.9314e-06

C3  2    0     424.4132e-12
L4  2    3       1.9314e-06

C5  3    0     131.1500e-12
.ends
.end

```


```
$ rffilter.py -g butterworth -highpass -f 10e6 -n 5 -r 75
.SUBCKT F1 1 4
* COMMAND  : rffilter.py -g butterworth -highpass -f 10e6 -n 5 -r 75
* TYPE     : BUTTERWORTH
* FILTER   : HIGHPASS
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 75.0
* RL       : 75.0

C1  1    2     343.3597e-12

L2  2    0     737.7256e-09
C3  2    3     106.1033e-12

L4  3    0     737.7256e-09
C5  3    4     343.3597e-12
.ends
.end

.SUBCKT F1 1 3
* COMMAND  : rffilter.py -g butterworth -highpass -f 10e6 -n 5 -r 75
* TYPE     : BUTTERWORTH
* FILTER   : HIGHPASS
* ORDER    : 5
* FREQ     : 10.000000 MHz
* RS       : 75.0
* RL       : 75.0

L1  1    0       1.9314e-06
C2  1    2     131.1512e-12

L3  2    0     596.8310e-09
C4  2    3     131.1512e-12

L5  3    0       1.9314e-06
.ends
.end

```


```
$ rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8 -qu 2000
.SUBCKT F1 1 25
* COMMAND  : rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8 -qu 2000
* TYPE     : BUTTERWORTH
* FILTER   : MESH
* ORDER    : 8
* FREQ     : 10.000000 MHz
* RS       : 50.0
* RL       : 50.0
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : 2000.0

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.3902  620.9908e-09             -    1.0252e+06    9.7545e+00
* 12     1.5187    1.7684e-06    8.1580e-06  607.4955e+03   60.7496e-03
* 23     0.7357    3.2676e-06    8.1580e-06  294.2641e+03   29.4264e-03
* 34     0.5537    4.8904e-06    7.5370e-06  221.4725e+03   22.1472e-03
* 45     0.5098    6.3896e-06    6.3896e-06  203.9183e+03   20.3918e-03
* 56     0.5537    7.5370e-06    4.8904e-06  221.4725e+03   22.1472e-03
* 67     0.7357    8.1580e-06    3.2676e-06  294.2641e+03   29.4264e-03
* 78     1.5187    8.1580e-06    1.7684e-06  607.4955e+03   60.7496e-03
* 89     0.3902             -  620.9908e-09    1.0252e+06    9.7545e+00

L1  1    2       7.7624e-06
R2  2    3     243.8625e-03
C3  3    4      34.7427e-12

C4  4    0     537.1580e-12
L5  4    5       7.7624e-06
R6  5    6     243.8625e-03
C7  6    7      35.8664e-12

C8  7    0       1.1089e-09
L9  7    8       7.7624e-06
R10 8    9     243.8625e-03
C11 9    10     34.4066e-12

C12 10   0       1.4734e-09
L13 10   11      7.7624e-06
R14 11   12    243.8625e-03
C15 12   13     34.0819e-12

C16 13   0       1.6003e-09
L17 13   14      7.7624e-06
R18 14   15    243.8625e-03
C19 15   16     34.0819e-12

C20 16   0       1.4734e-09
L21 16   17      7.7624e-06
R22 17   18    243.8625e-03
C23 18   19     34.4066e-12

C24 19   0       1.1089e-09
L25 19   20      7.7624e-06
R26 20   21    243.8625e-03
C27 21   22     35.8664e-12

C28 22   0     537.1580e-12
L29 22   23      7.7624e-06
R30 23   24    243.8625e-03
C31 24   25     34.7427e-12
.ends
.end

```


```
$ rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -l 100e-9
.SUBCKT F1 1 9
* COMMAND  : rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -l 100e-9
* TYPE     : BUTTERWORTH
* FILTER   : MESH
* ORDER    : 4
* FREQ     : 10.000000 MHz
* RS       : 0.3
* RL       : 0.3
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.7654    1.2181e-06             -  522.6230e+03   19.1343e+00
* 12     0.8409    2.9408e-06    4.1589e-06  336.3578e+03   33.6358e-03
* 23     0.5412    4.1589e-06    4.1589e-06  216.4783e+03   21.6478e-03
* 34     0.8409    4.1589e-06    2.9408e-06  336.3578e+03   33.6358e-03
* 45     0.7654             -    1.2181e-06  522.6230e+03   19.1343e+00

L1  1    2     100.0000e-09
C2  2    3       2.6212e-09

C3  3    0      75.3076e-09
L4  3    4     100.0000e-09
C5  4    5       2.6813e-09

C6  5    0     117.0108e-09
L7  5    6     100.0000e-09
C8  6    7       2.6813e-09

C9  7    0      75.3076e-09
L10 7    8     100.0000e-09
C11 8    9       2.6212e-09
.ends
.end

```


```
$ rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100
.SUBCKT F1 1 9
* COMMAND  : rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100
* TYPE     : BUTTERWORTH
* FILTER   : MESH
* ORDER    : 4
* FREQ     : 10.000000 MHz
* RS       : 100.0
* RL       : 100.0
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.7654    1.2181e-06             -  522.6230e+03   19.1343e+00
* 12     0.8409    2.9408e-06    4.1589e-06  336.3578e+03   33.6358e-03
* 23     0.5412    4.1589e-06    4.1589e-06  216.4783e+03   21.6478e-03
* 34     0.8409    4.1589e-06    2.9408e-06  336.3578e+03   33.6358e-03
* 45     0.7654             -    1.2181e-06  522.6230e+03   19.1343e+00

L1  1    2      30.4531e-06
C2  2    3       8.6073e-12

C3  3    0     247.2904e-12
L4  3    4      30.4531e-06
C5  4    5       8.8046e-12

C6  5    0     384.2326e-12
L7  5    6      30.4531e-06
C8  6    7       8.8046e-12

C9  7    0     247.2904e-12
L10 7    8      30.4531e-06
C11 8    9       8.6073e-12
.ends
.end

```


```
$ rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100,120
.SUBCKT F1 1 9
* COMMAND  : rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100,120
* TYPE     : BUTTERWORTH
* FILTER   : MESH
* ORDER    : 4
* FREQ     : 10.000000 MHz
* RS       : 100.0
* RL       : 120.0
* BW       : 400.0000e+03
* QL       : 25.0
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     0.7654    1.2181e-06             -  522.6230e+03   19.1343e+00
* 12     0.8409    2.9408e-06    4.1589e-06  336.3578e+03   33.6358e-03
* 23     0.5412    4.1589e-06    4.1589e-06  216.4783e+03   21.6478e-03
* 34     0.8409    4.1589e-06    2.9408e-06  336.3578e+03   33.6358e-03
* 45     0.7654             -    1.2181e-06  522.6230e+03   19.1343e+00

L1  1    2      30.4531e-06
C2  2    3       8.6073e-12

C3  3    0     247.2904e-12
L4  3    4      30.4531e-06
C5  4    5       8.8046e-12

C6  5    0     384.2326e-12
L7  5    6      30.4531e-06
C8  6    7       8.8346e-12

C9  7    0     225.7442e-12
L10 7    8      36.5437e-06
C11 8    9       7.1511e-12
.ends
.end

```


Build a 500 Hz bandwidth crystal filter.

Expose the ports.  Note, sequential ports must be connected together - and broken to short resonators for mesh filters.  See example.


```
$ rffilter.py -k chebyshev_0.1 -n 8 -crystal -l .170 -f 4e6 -bw 500 -cp 2.05e-12 -expose | tee examples/xtaltune.cir
.SUBCKT F1 1 4 5 8 9 12 13 16 17 20 21 24 25 28 29 32
* COMMAND  : rffilter.py -k chebyshev_0.1 -n 8 -crystal -l .170 -f 4e6 -bw 500 -cp 2.05e-12 -expose
* TYPE     : CHEBYSHEV_0.1
* FILTER   : CRYSTAL_MESH
* ORDER    : 8
* FREQ     : 4.000330 MHz
* RS       : 459.7
* RL       : 459.7
* CP       : 2.0500e-12
* BW       : 500.0000e+00
* QL       : 8000.7
* QU       : inf

* ij        q,k           TD0           TDn           CBW           Q,K
* 01     1.2510    1.5928e-03             -  399.6803e+00   10.0088e+03
* 12     0.7280    1.9204e-03    7.3284e-03  364.0000e+00   90.9925e-06
* 23     0.5450    4.4349e-03    9.9522e-03  272.5000e+00   68.1194e-06
* 34     0.5160    4.0627e-03    6.1555e-03  258.0000e+00   64.4947e-06
* 45     0.5100    7.3443e-03    7.3443e-03  255.0000e+00   63.7447e-06
* 56     0.5160    6.1555e-03    4.0627e-03  258.0000e+00   64.4947e-06
* 67     0.5450    9.9522e-03    4.4349e-03  272.5000e+00   68.1194e-06
* 78     0.7280    7.3284e-03    1.9204e-03  364.0000e+00   90.9925e-06
* 89     1.2510             -    1.5928e-03  399.6803e+00   10.0088e+03

* Xtal    Xtal freq     Mesh freq   Mesh offset   Xtal offset
* 1       4000000.0     4000194.0        -136.3           0.0
* 2       4000000.0     4000330.2          -0.0           0.0
* 3       4000000.0     4000277.2         -53.0           0.0
* 4       4000000.0     4000268.5         -61.8           0.0
* 5       4000000.0     4000268.5         -61.8           0.0
* 6       4000000.0     4000277.2         -53.0           0.0
* 7       4000000.0     4000330.2          -0.0           0.0
* 8       4000000.0     4000194.0        -136.3           0.0

* ij              CKij            CSi
* 12       95.0313e-12   126.9354e-12
* 23      126.9409e-12     2.9216e-06
* 34      134.0752e-12   326.2975e-12
* 45      135.6526e-12   280.0655e-12
* 56      134.0752e-12   280.0655e-12
* 67      126.9409e-12   326.2975e-12
* 78       95.0313e-12     2.9216e-06
* 89                 -   126.9354e-12

C1  1    2       9.3126e-15
L2  2    3     170.0000e-03
C3  1    3       2.0500e-12
C4  3    4     126.9354e-12

C5  4    0      95.0313e-12
C6  5    6       9.3126e-15
L7  6    7     170.0000e-03
C8  5    7       2.0500e-12
C9  7    8       2.9216e-06

C10 8    0     126.9409e-12
C11 9    10      9.3126e-15
L12 10   11    170.0000e-03
C13 9    11      2.0500e-12
C14 11   12    326.2975e-12

C15 12   0     134.0752e-12
C16 13   14      9.3126e-15
L17 14   15    170.0000e-03
C18 13   15      2.0500e-12
C19 15   16    280.0655e-12

C20 16   0     135.6526e-12
C21 17   18      9.3126e-15
L22 18   19    170.0000e-03
C23 17   19      2.0500e-12
C24 19   20    280.0655e-12

C25 20   0     134.0752e-12
C26 21   22      9.3126e-15
L27 22   23    170.0000e-03
C28 21   23      2.0500e-12
C29 23   24    326.2975e-12

C30 24   0     126.9409e-12
C31 25   26      9.3126e-15
L32 26   27    170.0000e-03
C33 25   27      2.0500e-12
C34 27   28      2.9216e-06

C35 28   0      95.0313e-12
C36 29   30      9.3126e-15
L37 30   31    170.0000e-03
C38 29   31      2.0500e-12
C39 31   32    126.9354e-12
.ends
.end

```


# stodelay.py

Python script stodelay.py converts s-parameters to reflected time delay.

```
$ python stodelay.py <filename>.s?p
```
## Examples

Run against a two port to get the reflected time delay for each port

```
$ python stodelay.py 2n3904e_6ma.s2p 

# MHZ TDELAY
0.1      -168.5223e-12  984.1521e-12
0.137283 -167.1983e-12  979.6860e-12
0.188467 -163.7761e-12  968.1404e-12
0.258734 -157.4830e-12  946.9019e-12
0.355199 -146.1521e-12  908.6376e-12
0.487629 -126.5144e-12  842.2474e-12
0.669433  -94.6838e-12  734.4292e-12
0.91902   -48.5414e-12  577.6456e-12
1.26166     7.6854e-12  385.7018e-12
1.73205    61.0391e-12  202.3715e-12
2.37782    96.7446e-12   78.5342e-12
3.26435   110.0281e-12   31.5542e-12
4.4814    107.9325e-12   37.9820e-12
6.15222   100.3719e-12   63.7935e-12
8.44598    93.2559e-12   88.4288e-12
11.5949    88.3289e-12  105.7484e-12
15.9179    85.4208e-12  116.3786e-12
21.8526    83.9651e-12  122.4797e-12
30         83.5676e-12  124.4119e-12
```

Run against one port to get the reflected time delay for that port

```
$ python stodelay.py 2n3904e_6ma.s1p 

# MHZ TDELAY
0.1      -168.5223e-12
0.137283 -167.1983e-12
0.188467 -163.7761e-12
0.258734 -157.4830e-12
0.355199 -146.1521e-12
0.487629 -126.5144e-12
0.669433  -94.6838e-12
0.91902   -48.5414e-12
1.26166     7.6854e-12
1.73205    61.0391e-12
2.37782    96.7446e-12
3.26435   110.0281e-12
4.4814    107.9325e-12
6.15222   100.3719e-12
8.44598    93.2559e-12
11.5949    88.3289e-12
15.9179    85.4208e-12
21.8526    83.9651e-12
30         83.5676e-12
```


