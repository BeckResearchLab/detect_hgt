#!/usr/bin/env python

import argparse
import sys

import pandas as pd


parser = argparse.ArgumentParser(description='refseq taxonomy partition')
parser.add_argument('taxlevel', 
        choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus'],
        help='what taxonomy level should the data be partitioned on')
parser.add_argument('taxa', 
        help='the taxonomy class that will be partition out')
args = parser.parse_args()
taxlevel = args.taxlevel
taxa = args.taxa

refseq_tax = pd.read_csv('refseq_taxonomy.tsv', sep='\t')

refseq_tax_match = refseq_tax.loc[refseq_tax[taxlevel] == taxa]
refseq_tax_match.to_csv('refseq_taxonomy_matched.tsv', sep='\t', index=False)

refseq_tax_nomatch = refseq_tax.loc[refseq_tax[taxlevel] != taxa]
refseq_tax_nomatch.to_csv('refseq_taxonomy_not_matched.tsv', sep='\t',
        index=False)
