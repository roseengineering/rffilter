
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

# -g             : lowpass prototype filter type

print(f"""

rffilter
----------

Python 3 script for calculating RF filters.
The script requires the numpy library.

For nodal and mesh filters (including crystal filters) the script
will output resonator group delays from Ness as well as 
resonator coupling bandwidths from Dishal.

Command Line
-------------

The program takes the following command line options:

```
(see examples below)
```

Examples
--------

List filters provided.

{ run("rffilter.py -g") }
{ run("rffilter.py -k") }
{ run("rffilter.py -zverev") }

Lowpass and highpass filters.

{ run("rffilter.py -g butterworth -lowpass -f 10e6 -n 5") }
{ run("rffilter.py -g butterworth -lowpass -f 10e6 -n 5 -r 75") }
{ run("rffilter.py -g butterworth -highpass -f 10e6 -n 5 -r 75") }

Wide band bandpass filters.

{ run("rffilter.py -g butterworth -bandpass -f 10e6 -bw 1e6 -n 4") }

Narrow-band nodal filters.

{ run("rffilter.py -k butterworth -nodal -f 10e6 -bw 1e6 -n 5") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -l 100e-9") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -r 100") }
{ run("rffilter.py -g butterworth -nodal -f 10e6 -bw 400e3 -n 5 -r 100,120") }

Narrow-band mesh filters.

{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -l 100e-9") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100") }
{ run("rffilter.py -g butterworth -mesh -f 10e6 -bw 400e3 -n 4 -r 100,120") }

Use the Zverev filter tables with an unloaded Q.

{ run("rffilter.py -zverev butterworth -nodal -qu 2500 -bw 1e6 -f 10e6 -n 3") }
{ run("rffilter.py -zverev bessel -nodal -qu 2500 -bw 1e6 -f 10e6 -n 8") }

Build a 500 Hz bandwidth crystal filter.

{ run("rffilter.py -g chebyshev_001 -n 8 -crystal -l .170 -f 4e6 -bw 500 -cp 2.05e-12") }

Build a 2400 Hz bandwidth crystal filter.  This filter is from an example in Steder's 
"Crystal Ladder Filters for All" paper in QEX.  

{ run("rffilter.py -g chebyshev_02 -n 8 -crystal -l 69.7e-3 -f 4913.57e3 -bw 2400 -cp 3.66e-12") }
""")

"""
{ run("") }
{ run("") }
{ run("") }
{ run("") }
{ run("") }

Install 
-------------

Use 'pip install .' to install (or use 'pip install git+https://github.com/roseengineering/rffilter').

"""
