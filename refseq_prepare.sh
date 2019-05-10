#!/bin/bash

THREADS=24
MIN_SEQ_LEN=750

if [ ! -e refseq_taxonomy.tsv ]; then
	./refseq_taxonomy_extractor.py
fi

if [ ! -e refseq_taxonomy_matched.tsv -o ! -e refseq_taxonomy_not_matched.tsv ]; then
	./refseq_taxonomy_partition.py family Enterobacteriaceae
fi

if [ ! -e refseq_cds_matched.tsv -o ! -e refseq_cds_not_matched.tsv ]; then
	./refseq_cds_extractor.py --threads $THREADS
fi

if [ ! -e refseq_cds_matched_filtered.tsv ]; then
	./refseq_cds_filter.py refseq_cds_matched.tsv $MIN_SEQ_LEN refseq_cds_matched_filtered.tsv&
fi

if [ ! -e refseq_cds_not_matched_filtered.tsv ]; then
	./refseq_cds_filter.py refseq_cds_not_matched.tsv $MIN_SEQ_LEN refseq_cds_not_matched_filtered.tsv&
fi

wait

if [ ! -e refseq_cds_balanced.tsv ]; then
	./refseq_cds_balance.py family Enterobacteriaceae refseq_cds_balanced.tsv refseq_cds_matched_filtered.tsv refseq_cds_not_matched_filtered.tsv
fi

if [ ! -e refseq_cds_balanced.mat ]; then
	./refseq_cds_savemat.py family Enterobacteriaceae refseq_cds_balanced.tsv refseq_cds_balanced.mat --trim $MIN_SEQ_LEN
fi
