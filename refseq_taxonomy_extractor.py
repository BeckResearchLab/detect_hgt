#!/usr/bin/env python

import os
import io
from datetime import datetime

from Bio import SeqIO
import click
from multiprocessing import Pool
import numpy as np
import pandas as pd


def gff_taxonomy_extract(filepath):
    output = io.StringIO()
    output.write('gff_file\tkingdom\tphylum\tclass\torder\tfamily\tgenus\n')
    try:
        for seq_record in SeqIO.parse(filepath, 'genbank'):
            taxonomy = seq_record.annotations['taxonomy']
            output.write(f'{filepath}\t{taxonomy[0] if len(taxonomy) > 0 else np.nan}\t{taxonomy[1] if len(taxonomy) > 1 else np.nan}\t{taxonomy[2] if len(taxonomy) > 2 else np.nan}\t{taxonomy[3] if len(taxonomy) > 3 else np.nan}\t{taxonomy[4] if len(taxonomy) > 4 else np.nan}\t{taxonomy[5] if len(taxonomy) > 5 else np.nan}\n')
            break
    except AttributeError:
        print(f'parsing of file {filepath} failed')
    output.seek(0)
    df = pd.read_csv(output, sep='\t')
    return df
    

@click.command()
@click.option('-t', '--threads', 'threads', default=16, type=int,
        help='number of parallel Genbank parser threads')
@click.option('-r', '--refseq_path', 'refseq_path', type=str, required=True,
        help='path to the root of the refseq download')
@click.option('-o', '--output_file', 'output_file', type=str, required=True,
        help='name of the output file containing taxonomy annotations')
def refseq_taxonomy_extractor(threads, refseq_path, output_file):
    """Extract the taxonomy info from a collection of GBFF files"""
    start_time = datetime.now()
    print('begining data extraction')

    gbff_files = []
    for root, dirs, files in os.walk(refseq_path):
        for file_ in files:
            filepath = os.path.join(root, file_)
            if filepath.endswith('.gbff'):
                gbff_files.append(filepath)

    with Pool(threads) as p:
        dfs = p.map(gff_taxonomy_extract, gbff_files)

    df = dfs.pop(0)
    df.to_csv(outfile, sep='\t', index=False)
    for df_i in dfs:
        df_i.to_csv(outfile, sep='\t', index=False, header=False, mode='a')

    stop_time = datetime.now()
    total_time = stop_time - start_time
    print('run time was:', total_time)


if __name__ == '__main__':
    refseq_taxonomy_extractor()
