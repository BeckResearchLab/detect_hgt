#!/usr/bin/env python

import os
from datetime import datetime

from Bio import SeqIO
import numpy as np
import pandas as pd

datafiles = ['refseq_taxonomy_matched.tsv', 'refseq_taxonomy_not_matched.tsv']
for datafile in datafiles:
    df = pd.read_csv(datafile, sep='\t')

    outfile = datafile.replace('taxonomy', 'cds')
    f = open(outfile, "w")
    f.write("gff_file\tlocus\tproduct_id\tsequence\n")

    for filepath in list(df['gff_file']):
        try:
            for seq_record in SeqIO.parse(filepath, "genbank"):
                taxonomy = seq_record.annotations["taxonomy"]
                for feature in seq_record.features:
                    if feature.type == 'CDS':
                        f.write(f"{filepath}\t{seq_record.id}\t{taxonomy[0] if len(taxonomy) > 0 else np.nan}\t{taxonomy[1] if len(taxonomy) > 1 else np.nan}\t{taxonomy[2] if len(taxonomy) > 2 else np.nan}\t{taxonomy[3] if len(taxonomy) > 3 else np.nan}\t{taxonomy[4] if len(taxonomy) > 4 else np.nan}\t{taxonomy[5] if len(taxonomy) > 5 else np.nan}\t{feature.location.extract(seq_record).seq}\n")
        except AttributeError:
            print(f"parsing of file {filepath} failed")
    f.close()
