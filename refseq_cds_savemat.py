#!/usr/bin/env python

import argparse
import sys

import numpy as np
import pandas as pd
import scipy.io

parser = argparse.ArgumentParser(description='convert refseq cds tsv to .mat file',
            usage='e.g., ./refseq_cds_savemat.py family Enterobacteriaceae refseq_cds_matched.tsv refseq_cds_nonmatched.tsv')
parser.add_argument('taxlevel', 
        choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus'],
        help='what taxonomy level should be used as the class')
parser.add_argument('taxa', 
        help='the taxonomy class that will be class 0')
parser.add_argument('filenames', nargs='*',
        help='the refseq cds tsv files to be concatenated and converted to .mat')
args = parser.parse_args()
taxlevel = args.taxlevel
taxa = args.taxa
filenames = args.filenames

print(f"reading tsv data file {filenames[0]}")
df = pd.read_csv(filenames.pop(0), sep='\t').filter(items=['sequence', taxlevel])
for filename in filenames:
    print(f"reading tsv data file {filename}")
    df.append(pd.read_csv(filename, sep='\t').filter(items=['sequence', taxlevel]))

outfile = 'refseq_cds.mat'
print(f"saving mat data to file {outfile}")
target = np.array(df[taxlevel] == taxa, dtype=int)
scipy.io.savemat(outfile, { 'sequence' : df['sequence'],
        'target' : target}, appendmat = True)
