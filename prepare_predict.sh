#!/bin/bash

awk -F'\t' '{ printf(">%s\t%s\n%s\n", $9, $7, $10); }' refseq_cds_filtered.tsv
