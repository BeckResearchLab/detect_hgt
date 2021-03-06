#!/usr/bin/env python

import click
import numpy as np
import numpy.testing
import pandas as pd
import selene_sdk.sequences
import scipy.io


def df_named_subset_savemat(title, outfile, frac, df, start, end):
    print(f"saving {title} data to {outfile} ({frac * 100.}% = {len(range(start, end))} samples)")
    sequences = np.array(df.iloc[range(start, end)]['sequence'].values.tolist())
    targets = np.array(df.iloc[range(start, end)]['target'].values.tolist())
    scipy.io.savemat(outfile, { 'sequence' : sequences,
        'target' : targets})


@click.command()
@click.option('-i', '--input_file', 'input_file', type=str, required=True,
                help='the location of the balanced sequences sets for classification')
@click.option('-r', '--train_file', 'train_file', type=str, required=True,
                help='name of the output file for the training data set')
@click.option('-v', '--valid_file', 'valid_file', type=str, required=True,
                help='name of the output file for the validation data set')
@click.option('-s', '--test_file', 'test_file', type=str, required=True,
                help='name of the output file for the test data set')
@click.option('-i', '--train_frac', 'train_frac', type=float, default=0.7,
                show_default=True,
                help='the fraction of samples to use for the training data set')
@click.option('-a', '--valid_frac', 'valid_frac', type=float, default=0.2,
                show_default=True,
                help='the fraction of samples to use for the validation data set')
@click.option('-e', '--test_frac', 'test_frac', type=float, default=0.1,
                show_default=True,
                help='the fraction of samples to use for the test data set')
@click.option('-l', '--tax_level', 'tax_level', required=True,
                type=click.Choice(['kingdom', 'phylum', 'class', 'order',
                                    'family', 'genus']),
                help='what taxonomy level should the binary classification be ')
@click.option('-t', '--taxa', 'taxa', type=str, required=True,
                help='the taxonomy class that will be targeted for classifcation')
def refseq_cds_savemat(input_file, train_file, valid_file, test_file, train_frac, valid_frac, test_frac, tax_level, taxa):
    """split a set of taxonomy annoted sequences into training, validation and test tests"""

    numpy.testing.assert_almost_equal(train_frac + valid_frac + test_frac, 1.,
        err_msg='the fractions of training, validation and test data do not equal 1')

    print(f'reading cds data from tsv file {input_file}')
    df = pd.read_csv(input_file, sep='\t').filter(items=['sequence', tax_level])

    print(f'encoding {df.shape[0]} sequences')
    bases_arr = np.array(['A', 'C', 'G', 'T'])
    bases_encoding = { 'A': 0, 'C': 1, 'G': 2, 'T': 3 }
    df['sequence'] = df['sequence'].apply(lambda x:
        selene_sdk.sequences.sequence_to_encoding(x, bases_encoding, bases_arr))

    print('creating final data frame with encoded taxonomy flags')
    df['target'] = np.array(df[tax_level] == taxa, dtype=int)
    df.drop(tax_level, axis=1, inplace=True)

    print('splitting in training, validation, and test sets')

    max_train = int(train_frac * df.shape[0])
    df_named_subset_savemat('training', train_file, train_frac, df, 0, max_train)
    valid_i = int(valid_frac * df.shape[0])
    df_named_subset_savemat('validation', valid_file, valid_frac, df, max_train, max_train+valid_i)
    df_named_subset_savemat('test', test_file, test_frac, df, max_train+valid_i, df.shape[0])


if __name__ == '__main__':
    refseq_cds_savemat()
