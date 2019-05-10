#!/usr/bin/env python

import argparse
import sys

import numpy as np
import numpy.testing
import pandas as pd
import selene_sdk.sequences
import scipy.io


def df_named_subset_savemat(title, outfile, frac, df, start, end):
    print(f"saving {title} data to {outfile} ({frac * 100.}% = {len(range(start, end))} samples)")
    sequences = np.array(df.iloc[range(start, end)]['sequence'].values.tolist())
    targets = np.array(df.iloc[range(start, end)]['target'].values.tolist())
    scipy.io.savemat(outfile, { 'sequence' : sequences,
        'target' : targets})


parser = argparse.ArgumentParser(description='convert refseq cds tsv to .mat file in hdf5 format',
            usage='e.g., ./refseq_cds_savemat.py family Enterobacteriaceae refseq_cds_balanced.tsv refseq_cds_balanced.mat')
parser.add_argument('taxlevel', 
        choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus'],
        help='what taxonomy level should be used as the class')
parser.add_argument('taxa', 
        help='the taxonomy class that will be class 0')
parser.add_argument('infile',
        help='the balanced refseq cds tsv file to be converted to .mat')
parser.add_argument('--train_frac', dest='train_frac', default=0.7,
        help='fraction of sequences to use for training')
parser.add_argument('--valid_frac', dest='valid_frac', default=0.2,
        help='fraction of sequences to use for validation')
parser.add_argument('--test_frac', dest='test_frac', default=0.1,
        help='fraction of sequences to use for testing')
parser.add_argument('--trim', dest='trim_length', default=None,
        help='trim sequences to a given length')
args = parser.parse_args()
taxlevel = args.taxlevel
taxa = args.taxa
infile = args.infile
trim_length = args.trim_length
train_frac = args.train_frac
valid_frac = args.valid_frac
test_frac = args.test_frac
numpy.testing.assert_almost_equal(train_frac + valid_frac + test_frac, 1.,
    err_msg="the fractions of training, validation and test data do not equal 1")

print(f"reading tsv data file {infile}")
df = pd.read_csv(infile, sep='\t').filter(items=['sequence', taxlevel])

print(f"encoding {df.shape[0]} sequences")
bases_arr = np.array(['A', 'C', 'G', 'T'])
bases_encoding = { 'A': 0, 'C': 1, 'G': 2, 'T': 3 }
if trim_length is None:
    df['sequence'] = df['sequence'].apply(lambda x:
        selene_sdk.sequences.sequence_to_encoding(x, bases_encoding, bases_arr))
else:
    trim_length = int(trim_length)
    print(f"trimming sequences during encoding to max length of {trim_length}")
    df['sequence'] = df['sequence'].apply(lambda x:
            selene_sdk.sequences.sequence_to_encoding(x[:trim_length], bases_encoding, bases_arr))

print("creating final data frame")
df['target'] = np.array(df[taxlevel] == taxa, dtype=int)
df.drop(taxlevel, axis=1, inplace=True)

print("splitting in training, validation, and test sets")

max_train = int(train_frac * df.shape[0])
df_named_subset_savemat('training', 'refseq_cds_train.mat', train_frac, df, 0, max_train)
valid_i = int(valid_frac * df.shape[0])
df_named_subset_savemat('validation', 'refseq_cds_valid.mat', valid_frac, df, max_train, max_train+valid_i)
df_named_subset_savemat('test', 'refseq_cds_test.mat', test_frac, df, max_train+valid_i, df.shape[0])
