# detect_hgt

---

An example preparation workflow is presented in `refseq_prepare.sh`

Workflow:
1. `refseq_taxonomy_extractor.py` - extract the taxonomy of organisms in refseq and the nucleotide ids
2. `refseq_taxonomy_partition.py` - split the output of step 1. based on a given taxonomy level and taxa, e.g. `./refseq_taxonomy_partition.py family Enterobacteriaceae`
3. `refseq_cds_extractor.py` - extract the nucleotide coding sequences for the partitioned taxa in parallel, e.g. `./refseq_cds_extractor.py --threads 24`
4. `refseq_cds_filter.py` - filter the extracted cds file by minimum sequence length
5. `refseq_cds_balance.py` - concatenate the matched and not matched taxa files and balance the number of sequences in each class
6. `refseq_cds_savemat.py` - format the coding sequences tagged by taxa class and save into a `.mat` file for use with PyTorch, also partitions train, validation and test

