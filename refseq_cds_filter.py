#!/usr/bin/env python

import argparse
import sys

import numpy as np
import pandas as pd
import scipy.io

parser = argparse.ArgumentParser(description='filter cds for minimum sequence length',
            usage='e.g., ./refseq_cds_filter.py refseq_cds_matched.tsv 1000 refseq_cds_matched_filtered.tsv')
parser.add_argument('infile', help='inputut file containing the samples')
parser.add_argument('length', type=int,
        help='minimum length of a sequence to pass the filtering')
parser.add_argument('outfile',
        help='output file containing the filtered samples')
args = parser.parse_args()
infile = args.infile
length = args.length
outfile = args.outfile

print(f"reading tsv data file {infile}")
df = pd.read_csv(infile, sep='\t')
print(f"filtering {df.shape[0]} samples for minimum sequence length of {length}")
df = df.loc[df.sequence.str.len() < length]
print(f"saving {df.shape[0]} filtered samples to {outfile}")
df.to_csv(outfile, sep='\t', index=False)
