#!/usr/bin/env python

import argparse
import sys

import numpy as np
import pandas as pd
import scipy.io

parser = argparse.ArgumentParser(description='convert refseq cds tsv to .mat file',
            usage='e.g., ./refseq_cds_savemat.py family Enterobacteriaceae refseq_cds_matched.tsv')
parser.add_argument('taxlevel', 
        choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus'],
        help='what taxonomy level should be used as the class')
parser.add_argument('taxa', 
        help='the taxonomy class that will be class 0')
parser.add_argument('filename', 
        help='the refseq cds tsv file to convert to .mat')
args = parser.parse_args()
taxlevel = args.taxlevel
taxa = args.taxa
filename = args.filename

print(f"reading tsv data file {filename}")
df = pd.read_csv(filename, sep='\t')
print(f"saving mat data to file {filename + '.mat'}")

target = np.array(df[taxlevel] == taxa, dtype=int)
scipy.io.savemat(filename, { 'sequence' : df['sequence'],
        'target' : target}, appendmat = True)
