
import os, subprocess 

def run(command):
    proc = subprocess.Popen("PYTHONPATH=. python " + command, shell=True, stdout=subprocess.PIPE)
    buf = proc.stdout.read().decode()
    proc.wait()
    return f"""
```
$ {command}
{buf}\
```
"""

print(f"""

rffilter
----------

Python 3 script for calculating RF filters.
The script requires the numpy library.

For nodal and mesh filters (including crystal filters) the script
will output resonator group delays from Ness as well as 
resonator coupling bandwidths from Dishal.

Library functions
-----------------

The script provides the following public functions for import.

```
# find filter coefficients or prototype values

g    = lowpass_g(name, n):
q, k = coupling_qk(name, n):
q, k = zverev_k(name, n, qo=np.inf):
qo   = zverev_qo(name, n, qo=np.inf):

# coupling coefficent conversion

q, k = to_coupling_qk(g):
cbw  = to_coupling_bw(q, k, BW):
td   = to_group_delay(q, k, BW):

# wide-band filter design

xs, xp, re = to_lowpass(g, fo, R):
xs, xp, re = to_highpass(g, fo, R):
xs, xp, re = to_bandpass(g, fo, BW, R):
xs, xp, re = to_bandstop(g, fo, BW, R):

# narrow-band filter design

xs, xp, re     = to_nodal(q, k, fo, BW, R=None, L=None):
xs, xp, re     = to_mesh(q, k, fo, BW, R=None, L=None):
xs, xp, re, fo = to_crystal_mesh(q, k, fo, BW, LM, CP=0, QU=np.inf):
```

Command Line
-------------

The program takes the following command line options:

```
-g             : lowpass prototype element values
-k             : ideal q, k coupling coefficients
-zverev        : q, k coupling coefficients from Zverev's QO tables
-n             : number of filter poles or resonators
-r             : end resistors, can be given in common notation
-l             : resonator inductor values, can be given in common notation
-f             : design frequency
-bw            : design bandwidth
-qu            : unload Q of resonators
-cp            : parallel capacitance, C0, of crystals
-lowpass       : generate a lowpass filter
-highpass      : generate a highpass filter
-bandpass      : generate a wideband bandpass filter
-bandstop      : generate a wideband bandstop filter
-nodal         : generate a narrow-band nodal bandpass filter
-mesh          : generate a narrow-band mesh bandpass filter
-crystal       : generate a narrow-band crystal bandpass filter
```

Examples
--------

List filters provided.

{ run("rffilter.py -g") }
{ run("rffilter.py -k") }
{ run("rffilter.py -zverev") }

Print out coupling design information.  CBW is the coupling bandwidth between resonators and the bandwidth of the two resonators at the end.
TD0 and TDn are the group delay
at the center freqency for each resonator looking from either end, see 
Ness' "A Unified Approach to the
Design, Measurement, and Tuning of Coupled-Resonator Filters" in MTT.

{ run("rffilter.py -g chebyshev_0.2 -n 8 -bw 1000") }

Lowpass and highpass filters.

{ run("rffilter.py -g butterworth -lowpass -f 10e6 -n 5") }

![lowpass](examples/lowpass.png)

{ run("rffilter.py -g butterworth -lowpass -f 10e6 -n 5 -r 75") }
{ run("rffilter.py -g butterworth -highpass -f 10e6 -n 5 -r 75") }

Wide band bandpass filters.

{ run("rffilter.py -g butterworth -bandpass -f 10e6 -bw 1e6 -n 4") }

Narrow-band nodal filters.

{ run("rffilter.py -k butterworth -nodal -f 10e6 -bw 1e6 -n 5") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -l 100e-9") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -r 100,120") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 | tee examples/nodal.cir") }

![nodal](examples/nodal.png)

{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -qu 200 | tee examples/nodalloss.cir") }

![nodal lossy](examples/nodalloss.png)

Narrow-band mesh filters.

{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -l 100e-9") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100,120") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8 | tee examples/mesh.cir") }

![mesh lossy](examples/mesh.png)

{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8 -qu 2000 | tee examples/meshloss.cir") }

![mesh lossy](examples/meshloss.png)

Use the Zverev filter tables with an unloaded Q.

{ run("rffilter.py -zverev butterworth -nodal -qu 2500 -bw 1e6 -f 10e6 -n 3") }
{ run("rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8") }

Build a 500 Hz bandwidth crystal filter.

{ run("rffilter.py -g chebyshev_0.01 -n 8 -crystal -l .170 -f 4e6 -bw 500 -cp 2.05e-12") }

Build a 2400 Hz bandwidth crystal filter.  This filter is from an example in Steder's 
"Crystal Ladder Filters for All" paper in QEX.  

{ run("rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12 | tee examples/xtal.cir") }

![crystal](examples/xtal.png)

Same filter with an unloaded Q of 150000.

{ run("rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12 -qu 150000 | tee examples/xtalloss.cir") }

![crystal lossy](examples/xtalloss.png)

A crystal filter with multiple crystals of different frequencies.  No parallel capacitance was used.

{ run("rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3 | tee examples/multiple.cir") }

![multiple](examples/multiple.png)

The same crystal filter as above but with holder parallel capacitance across the crystals.  

{ run("rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -cp 3.7e-12 -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3 | tee examples/broken.cir") }

![broken](examples/broken.png)

""")


