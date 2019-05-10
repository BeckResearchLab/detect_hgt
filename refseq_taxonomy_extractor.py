#!/usr/bin/env python

import os
from datetime import datetime

from Bio import SeqIO
import click
import multiprocessing
import numpy as np


def process_pool_init(lock, outfile):
    global output_file_lock
    output_file_lock = lock
    global output_f
    output_f = outfile

def gff_taxonomy_extract(filepath):
    try:
        for seq_record in SeqIO.parse(filepath, 'genbank'):
            taxonomy = seq_record.annotations['taxonomy']
            output_file_lock.acquire()
            output_f.write(f'{filepath}\t{taxonomy[0] if len(taxonomy) > 0 else np.nan}\t{taxonomy[1] if len(taxonomy) > 1 else np.nan}\t{taxonomy[2] if len(taxonomy) > 2 else np.nan}\t{taxonomy[3] if len(taxonomy) > 3 else np.nan}\t{taxonomy[4] if len(taxonomy) > 4 else np.nan}\t{taxonomy[5] if len(taxonomy) > 5 else np.nan}\n')
            output_f.flush()
            output_file_lock.release()
            break
    except AttributeError:
        print(f'parsing of file {filepath} failed')
    

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
    print(f'scanning {len(gbff_files)} files')

    f = open(output_file, 'w')
    f.write('gff_file\tkingdom\tphylum\tclass\torder\tfamily\tgenus\n')
    f.flush()

    lock = multiprocessing.Lock()
    process_pool = multiprocessing.Pool(threads,
            initializer=process_pool_init, initargs=(lock, f, ))
    process_pool.map(gff_taxonomy_extract, gbff_files)
    process_pool.close()
    process_pool.join()

    f.close()

    stop_time = datetime.now()
    total_time = stop_time - start_time
    print('run time was:', total_time)


if __name__ == '__main__':
    refseq_taxonomy_extractor()
