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
f.write("gff_file\tkingdom\tphylum\tclass\torder\tfamily\tgenus\n")
for root, dirs, files in os.walk(homedir):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith(".gbff"):
            current_file += 1
            if current_file % 100 == 0:
                print("{:.2%} complete ({} of {} files)".format(current_file/file_count, current_file, file_count))
            try:
                for seq_record in SeqIO.parse(filepath, "genbank"):
                    if "plasmid" in seq_record.description
                            or "extrachromosomal" in record.description:
                        continue
                    taxonomy = seq_record.annotations["taxonomy"]
                    f.write(f"{filepath}\t{taxonomy[0] if len(taxonomy) > 0 else np.nan}\t{taxonomy[1] if len(taxonomy) > 1 else np.nan}\t{taxonomy[2] if len(taxonomy) > 2 else np.nan}\t{taxonomy[3] if len(taxonomy) > 3 else np.nan}\t{taxonomy[4] if len(taxonomy) > 4 else np.nan}\t{taxonomy[5] if len(taxonomy) > 5 else np.nan}\n")
                    break
            except AttributeError:
                print(f"parsing of file {filepath} failed")

f.close()

stop_time = datetime.now()
total_time = stop_time - start_time
print("run time was:", total_time)
