#!/usr/bin/env python

import argparse
import sys

import click
import pandas as pd


@click.command
@click.option('-l', '--tax_level', 'tax_level', type=str, required=True,
        help='what taxonomy level should the data be partitioned on')
@click.option('-t', '--taxa', 'taxa', type=str, required=True,
        help='the taxonomy class that will be partition out')
@click.option('-m', '--output_file_matched', 'output_file_matched',
        type=str, required=True,
        help='name of the output file containing matched
                help='name of the output file containing taxonomy annotations')

parser = argparse.ArgumentParser(description='refseq taxonomy partition',
            usage='e.g., ./refseq_taxonomy_partition.py family Enterobacteriaceae')
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
