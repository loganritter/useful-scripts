# String replace every n+2 lines
import numpy as np

atom_labels = np.loadtxt("atom_labels.txt", dtype='str')
lines = open('configs.fit', 'r').readlines()

n_atoms = len(atom_labels)

for i, line in enumerate(lines):
    mod_i = i % (n_atoms+2)
    if mod_i < 2:
        continue
    atom_i = mod_i - 2
    lines[i] = ' '.join( [atom_labels[atom_i]] + line.split(' ')[1:] )

f = open('configs.fit.fixed', 'w')
f.writelines(lines)
f.close()
