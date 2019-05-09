#!/usr/bin/env python

import argparse
import io
import os

from Bio import SeqIO
from multiprocessing import Pool
import numpy as np
import pandas as pd


def gff_cds_extract(filepath):
    output = io.StringIO()
    output.write("gff_file\tid\tkingdom\tphylum\tclass\torder\tfamily\tgenus\tlocus\tproduct_id\tsequence\n")

    try:
        for seq_record in SeqIO.parse(filepath, "genbank"):
            taxonomy = seq_record.annotations["taxonomy"]
            for feature in seq_record.features:
                if feature.type == 'CDS':
                    output.write(f"{filepath}\t{seq_record.id}\t{taxonomy[0] if len(taxonomy) > 0 else np.nan}\t{taxonomy[1] if len(taxonomy) > 1 else np.nan}\t{taxonomy[2] if len(taxonomy) > 2 else np.nan}\t{taxonomy[3] if len(taxonomy) > 3 else np.nan}\t{taxonomy[4] if len(taxonomy) > 4 else np.nan}\t{taxonomy[5] if len(taxonomy) > 5 else np.nan}\t{feature.qualifiers['protein_id'][0] if 'protein_id' in feature.qualifiers else np.nan}\t{feature.location.extract(seq_record).seq}\n")
    except AttributeError:
        print(f"parsing of file {filepath} failed")

    output.seek(0)
    df = pd.read_csv(output, sep='\t')
    return df


parser = argparse.ArgumentParser(description='refseq parallel cds extractor',
        usage='e.g., ./refseq_cds_extractor.py --threads 24')
parser.add_argument('--threads', dest='threads', type=int, default=8,
                help='number of parallel threads to use to proecss input files')
args = parser.parse_args()
threads = args.threads

datafiles = ['refseq_taxonomy_matched.tsv', 'refseq_taxonomy_not_matched.tsv']
for datafile in datafiles:
    df = pd.read_csv(datafile, sep='\t')

    print(f"discovering sequences from {datafile} with {threads} parallel threads")

    outfile = datafile.replace('taxonomy', 'cds')
    with Pool(threads) as p:
        dfs = p.map(gff_cds_extract, list(df['gff_file']))

    df = dfs.pop(0)
    for df_i in dfs:
        df = df.append(df_i)
    df.to_csv(outfile, sep='\t', index=False)
    print(f"extracted {df.shape[0]} cds sequences from metadata in {datafile} into {outfile}")
