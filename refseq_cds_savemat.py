#!/usr/bin/env python

import argparse
import sys

import numpy as np
import pandas as pd
import selene_sdk.sequences
import scipy.io

parser = argparse.ArgumentParser(description='convert refseq cds tsv to .mat file',
            usage='e.g., ./refseq_cds_savemat.py family Enterobacteriaceae refseq_cds_balanced.tsv refseq_cds_balanced.mat')
parser.add_argument('taxlevel', 
        choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus'],
        help='what taxonomy level should be used as the class')
parser.add_argument('taxa', 
        help='the taxonomy class that will be class 0')
parser.add_argument('infile',
        help='the balanced refseq cds tsv file to be converted to .mat')
parser.add_argument('outfile',
        help='the balanced refseq cds .mat outputfile')
parser.add_argument('--trim', dest='trim_length', default=None,
        help='trim sequences to a given length')
args = parser.parse_args()
taxlevel = args.taxlevel
taxa = args.taxa
infile = args.infile
outfile = args.outfile
trim_length = args.trim_length

print(f"reading tsv data file {infile}")
df = pd.read_csv(infile, sep='\t').filter(items=['sequence', taxlevel])

print(f"encoding {df.shape[0]} sequences")
bases_arr = np.array(['A', 'C', 'G', 'T'])
bases_encoding = { 'A': 0, 'C': 1, 'G': 2, 'T': 3 }
if trim_length is None:
    df["sequence"] = df['sequence'].apply(lambda x:
        selene_sdk.sequences.sequence_to_encoding(x, bases_encoding, bases_arr))
else:
    trim_length = int(trim_length)
    print(f"trimming sequences during encoding to max length of {trim_length}")
    df["sequence"] = df['sequence'].apply(lambda x:
            selene_sdk.sequences.sequence_to_encoding(x[:trim_length], bases_encoding, bases_arr))

outfile = 'refseq_cds.mat'
print(f"saving mat data to file {outfile}")
target = np.array(df[taxlevel] == taxa, dtype=int)
scipy.io.savemat(outfile, { 'sequence' : df['sequence'],
        'target' : target }, appendmat=True)
