#!/bin/bash

REFSEQ_PATH=/work/data/refseq
THREADS=24
MIN_SEQ_LEN=750

if [ ! -e refseq_cds.tsv -o ]; then
	./refseq_cds_extractor.py --refseq_path $REFSEQ_PATH \
			--output_file refseq_cds.tsv --threads $THREADS
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

if [ ! -e refseq_cds_train.mat -o ! -e refseq_cds_valid.mat -o ! -e refseq_cds_test.mat ]; then
	./refseq_cds_savemat.py family Enterobacteriaceae refseq_cds_balanced.tsv --trim $MIN_SEQ_LEN
fi
