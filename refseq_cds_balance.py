#!/usr/bin/env python

import argparse
import sys

import numpy as np
import pandas as pd
import scipy.io

parser = argparse.ArgumentParser(description='balance sample refseq cds for both classes',
            usage='e.g., ./refseq_cds_balance.py family Enterobacteriaceae refseq_cds_balanced.tsv refseq_cds_matched.tsv refseq_cds_not_matched.tsv')
parser.add_argument('taxlevel', 
        choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus'],
        help='what taxonomy level should be used as the class')
parser.add_argument('taxa', 
        help='the taxonomy class that will be class 0')
parser.add_argument('outfile',
        help='output file containing the balanced samples')
parser.add_argument('filenames', nargs='*',
        help='the refseq cds tsv files to be concatenated and sample classes balanced')
args = parser.parse_args()
taxlevel = args.taxlevel
taxa = args.taxa
outfile = args.outfile
filenames = args.filenames

print(f"reading tsv data file {filenames[0]}")
df = pd.read_csv(filenames.pop(0), sep='\t').filter(items=['sequence', taxlevel])
for filename in filenames:
    print(f"reading tsv data file {filename}")
    df = df.append(pd.read_csv(filename, sep='\t').filter(items=['sequence', taxlevel]))

print(f"finding positive examples")
positives = df.loc[df[taxlevel] == taxa]
print(f"{positives.size[0]} samples")
print(f"finding negative examples")
negatives = df.loc[df[taxlevel] != taxa]
print(f"{negatives.size[0]} samples with be randomly sampled down")
negsamples = negatives.sample(n=positives.size[0], random_state=42)
print(f"concatenating positive and negative samples")
df = positives.append(negsamples)
print(f"shuffling the order of samples")
df = df.sample(frac=1).reset_index(drop=True)
print(f"saving balanced samples to {outfile}")
df.to_csv(outfile, sep='\t', index=False)
