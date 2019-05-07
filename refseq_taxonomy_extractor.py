#!/usr/bin/env python

import os
from datetime import datetime

from Bio import SeqIO
import numpy as np
import pandas as pd

homedir = "/work/data/refseq/"

start_time = datetime.now()
print("begining data extraction")

file_count = 0
for root, dirs, files in os.walk(homedir):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith(".gbff"):
            file_count = file_count + 1

current_file = 0
f = open("refseq_taxonomy.tsv", "w")
f.write("locus\ttax0\ttax1\ttax2\ttax3\ttax4\ttax5\n")
for root, dirs, files in os.walk(homedir):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith(".gbff"):
            current_file += 1
            if current_file % 100 == 0:
                print("{:.2%} complete ({} of {} files)".format(current_file/file_count, current_file, file_count))
            try:
                for seq_record in SeqIO.parse(filepath, "genbank"):
                    #organism = seq_record.annotations["organism"]
                    taxonomy = seq_record.annotations["taxonomy"]
                    f.write(f"{seq_record.id}\t{taxonomy[0] if len(taxonomy) > 0 else np.nan}\t{taxonomy[1] if len(taxonomy) > 1 else np.nan}\t{taxonomy[2] if len(taxonomy) > 2 else np.nan}\t{taxonomy[3] if len(taxonomy) > 3 else np.nan}\t{taxonomy[4] if len(taxonomy) > 4 else np.nan}\t{taxonomy[5] if len(taxonomy) > 5 else np.nan}\n")
                    #f.flush()
                    #for feature in seq_record.features:
                    #    if feature.type == 'CDS':
                    #        f.write(f"{organism}\t{seq_record.id}\t{feature.qualifiers['product'][0] if 'product' in feature.qualifiers else np.nan}\t{feature.qualifiers['protein_id'][0] if 'protein_id' in feature.qualifiers else np.nan}\t{taxonomy[0]}\t{taxonomy[1]}\t{taxonomy[2]}\t{taxonomy[3]}\t{taxonomy[4]}\t{taxonomy[5]}\n")
                    #        # commented out the line below to speed up code
                    #        # f.flush() 
            except AttributeError:
                print(f"parsing of file {filepath} failed")

f.close()

stop_time = datetime.now()
total_time = stop_time - start_time
print("run time was:", total_time)
