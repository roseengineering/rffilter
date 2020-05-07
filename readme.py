#!/usr/bin/python3

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

{ run("rffilter.py -g") }
{ run("rffilter.py -k") }
{ run("rffilter.py -zverev") }

## Coupling bandwidth and group delay

Print out coupling design information.  CBW is the coupling bandwidth between resonators and the bandwidth of the two resonators at the end.
TD0 and TDn are the group delay
at the center freqency for each resonator looking from either end, see 
Ness' "A Unified Approach to the
Design, Measurement, and Tuning of Coupled-Resonator Filters" in MTT.

{ run("rffilter.py -g chebyshev_0.2 -n 8 -bw 1000") }

## Nodal narrow-band filters.

Generate a narrow-band filter using LC resonators top coupled by capacitors.
The -expose option exposes the resonators of the filter as ports.
The input port is the port 1 while the port with the highest number
is the output port.  The exposed resonators ports are numbered in increasing order.

{ run("rffilter.py -k chebyshev_0.1 -nodal -expose -f 10e6 -bw 400e3 -n 5 -qu 2000 | tee examples/nodal.cir") }
![nodal](examples/nodal.png)

## Mesh narrow-band filters.

{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8 | tee examples/mesh.cir") }
![mesh lossy](examples/mesh.png)

## Crystal mesh filters.


### 1. The "Crystal Ladder Filters for All" filter.

Build a 2400 Hz bandwidth crystal filter.  This filter is from an example in Steder's 
"Crystal Ladder Filters for All" paper in QEX.  

{ run("rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12 | tee examples/xtal.cir") }
![crystal](examples/xtal.png)

Same filter with an unloaded Q of 150000.  See the above Steder article for a figure of the loaded filter's response.

{ run("rffilter.py -g chebyshev_0.2 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12 -qu 150000 | tee examples/xtalloss.cir") }
![crystal lossy](examples/xtalloss.png)

### 2. The Dishal program's owners manual filter.

A crystal filter with multiple crystals of different frequencies.  No parallel capacitance was used.
The filter, less the holder capacitance, is an example from the Dishal program's owners manual.

{ run("rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3 | tee examples/multiple.cir") }
![multiple](examples/multiple.png)

The same crystal filter as above but with holder parallel capacitance across the crystals.
The filter is an example from the Dishal program's owners manual.

{ run("rffilter.py -k chebyshev_0.5 -bw 2500 -n 8 -l 70e-3 -crystal -cp 3.7e-12 -f 5000.680e3,5000.123e3,4999.670e3,5000.235e3,5000.320e3,4999.895e3,5000.010e3,5000.485e3 | tee examples/broken.cir") }
![broken](examples/broken.png)

### 3. The Design Filter in N6NWP's QEX 1995 article.

N6NWP recommends using the lowest frequency crystal for the reference mesh, while the Dishal program recommends using a crystal in the middle.  Using the middle crystal for the reference mesh seems to require more pulling of the crystal.  In general, you want the crystals meshes to use the same series capacitor, except for the reference meshes.

The following example uses the lowest crystal for the reference mesh:

{ run("rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -f 8000017.0,7999933.0,7999940.0,7999945.0,7999985.0,7999996.0,8000000.0,7999991.0,7999966.0,7999945.0,7999939.0,8000026.0 | tee examples/qexlow.cir") }
![qexlow](examples/qexlow.png)

The above crystal filter with 120,000 Q crystals:

{ run("rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -qu 120000 -f 8000017.0,7999933.0,7999940.0,7999945.0,7999985.0,7999996.0,8000000.0,7999991.0,7999966.0,7999945.0,7999939.0,8000026.0 > examples/qexloss.cir") }
![qexloss](examples/qexloss.png)

The following example uses a middle crystal for the reference mesh:

{ run("rffilter.py -g chebyshev_0.1 -bw 2500 -n 12 -l .0155 -crystal -cp 5e-12 -f 8000017.0,7999966.0,7999940.0,7999945.0,7999985.0,8000000.0,7999996.0,7999991.0,7999939.0,7999933.0,7999945.0,8000026.0 | tee examples/qexmiddle.cir") }

## Lowpass and highpass filters.

{ run("rffilter.py -g butterworth -lowpass -f 10e6 -n 5") }
![lowpass](examples/lowpass.png)

## Wide band bandpass filters.

{ run("rffilter.py -g butterworth -bandpass -f 10e6 -bw 1e6 -n 4") }

## Use of Zverev filter tables with an unloaded Q.

{ run("rffilter.py -zverev butterworth -nodal -qu 2500 -bw 1e6 -f 10e6 -n 3") }
{ run("rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8") }

## More examples

{ run("rffilter.py -k butterworth -nodal -f 10e6 -bw 1e6 -n 5") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -l 100e-9,100e-9,100e-9,100e-9,100e-9") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -r 100,120") }
{ run("rffilter.py -g butterworth -lowpass -f 10e6 -n 5 -r 75") }
{ run("rffilter.py -g butterworth -highpass -f 10e6 -n 5 -r 75") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 8 -qu 2000") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -l 100e-9") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100,120") }

Build a 500 Hz bandwidth crystal filter.

Expose the ports.  Note, sequential ports must be connected together - and broken to short resonators for mesh filters.  See example.

{ run("rffilter.py -k chebyshev_0.1 -n 8 -crystal -l .170 -f 4e6 -bw 500 -cp 2.05e-12 -expose | tee examples/xtaltune.cir") }

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

# chebyshev.py

Python script chebyshev.py prints out a table of normalized low pass chebyshev filter coefficients.

Usage: python chebyshev.py [<ripple_in_db=.1> [<maximum_order=15>]]

{ run("chebyshev.py") }
{ run("chebyshev.py .01 10") }

# butterworth.py

Python script butterworth.py prints out a table of normalized low pass butterworth, ie maximally flat, filter coefficients.

Usage: python butterworth.py [<maximum_order=15>]

{ run("butterworth.py 10") }

# buttersingly.py

Python script buttersingly.py prints out a table of normalized low pass butterworth, ie maximally flat, singly terminated filter coefficients.

Usage: python buttersingly.py [<maximum_order=15>]

{ run("buttersingly.py 10") }

""")


