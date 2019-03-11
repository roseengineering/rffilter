


filename = "zverev.dat"
n = None
print("ZVEREV = {")
print("    #    qo    q1    q2    k12   k23 ...")
with open(filename) as f:
    for line in f.read().splitlines():
        d = line.split()
        if len(d) == 0: continue
        if len(d) == 1:
            if n is not None: print("    ],")
            print("    '%s': [" % d[0].upper())
            n = None
            continue

        if n is None: 
            n = len(d)
        elif len(d) == n + 1:
            n += 1
        elif len(d) != n:
            raise ValueError

        print('    [', ','.join(d), '],')

print("    ],")
print("}")
