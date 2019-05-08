# detect_hgt

---

Workflow:
1. `refseq_taxonomy_extractor.py` - extract the taxonomy of organisms in refseq and the nucleotide ids
2. `refseq_taxonomy_partition.py` - split the output of step 1. based on a given taxonomy level and taxa, e.g. `./refseq_taxonomy_partition.py family Enterobacteriaceae`
3. `refseq_cds_extractor.py` - extract the nucleotide coding sequences for the partitioned taxa in parallel, e.g. `./refseq_cds_extractor.py --threads 24`
4. `refseq_cds_savemat.py` - join and format the coding sequences tagged by taxa class and save into a `.mat` file for use with PyTorch

