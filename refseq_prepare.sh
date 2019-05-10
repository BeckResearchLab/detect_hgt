#!/bin/bash

REFSEQ_PATH=/work/data/refseq
THREADS=24
MIN_SEQ_LEN=750

if [ ! -e refseq_cds.tsv ]; then
	./refseq_cds_extractor.py --refseq_path $REFSEQ_PATH \
			--output_file refseq_cds.tsv --threads $THREADS
fi

if [ ! -e refseq_cds_filtered.tsv ]; then
	./refseq_cds_filter.py --input_file refseq_cds.tsv --output_file refseq_cds_filtered.tsv \
			--min_seq_length $MIN_SEQ_LEN --trim_seq_length $MIN_SEQ_LEN

if [ ! -e refseq_cds_filtered_balanced.tsv ]; then
	./refseq_cds_balance.py --tax_level family --taxa Enterobacteriaceae \
			--output_file refseq_cds_filtered_balanced.tsv \
			--input_file refseq_cds_filtered.tsv --random_seed 42
fi

if [ ! -e refseq_cds_train.mat -o ! -e refseq_cds_valid.mat -o ! -e refseq_cds_test.mat ]; then
	./refseq_cds_savemat.py family Enterobacteriaceae refseq_cds_balanced.tsv --trim $MIN_SEQ_LEN
fi
