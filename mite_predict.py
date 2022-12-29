#!/usr/bin/env python3

import os
import sys
import numpy as np
import pandas as pd
from Bio import SeqIO
from numpy import array
from numpy import argmax
# Hide warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
sys.stderr = stderr


def fasta_frame(fasta_file):
    # Initialize fasta ids and fasta sequences lists
    fids = []
    fseq = []
    with open(fasta_file) as fasta:
        # Parse fasta file
        for record in SeqIO.parse(fasta, 'fasta'):
            fids.append(record.description) # append ids to list
            fseq.append(str(record.seq).lower()) # append sequences to list
    # lists to pandas series
    s1 = pd.Series(fids, name = 'id')
    s2 = pd.Series(fseq, name = 'sequence')
    # create dictionary
    data = {'id': s1, 'sequence': s2}
    # create dataframe
    df = pd.concat(data, axis=1)
    return df


def tok_seqs(fseqs):
    nt_to_token = { 'a':1, 't':2, 'g':3, 'c':4 }
    sequencias = []
    for s in fseqs:
        s = [ nt_to_token[nt] if nt in nt_to_token.keys() else 5 for nt in s ]
        sequencias.append(s)
    return sequencias

def label_pred_dataframe(fasta_ids, prediction_results):
    # Labels
    prediction_results = prediction_results[:,1:]
    # Create dataframe
    colunas = ['stowaway', 'tourist', 'nt']
    label_pred_df = pd.DataFrame(prediction_results, columns = colunas)
    label_pred_df = pd.concat([fasta_ids,label_pred_df], axis=1)
    # Create label column
    label_pred_df['prediction'] = label_pred_df[colunas].idxmax(axis=1)
    return label_pred_df

def label_prediction(IN_FASTA, batch_size_value=4):
    modelo = 'model_embedded_MITES_20221229-195502/model_embedded_MITES_20221229-195502.hdf5'
    label_model = modelo
    PADVALUE=10_000
    # Read fasta as dataframe
    fas_df = fasta_frame(IN_FASTA)
    fas_df = fas_df.loc[fas_df['sequence'].str.len() <= 800].reset_index(drop=True)
    identifiers = fas_df['id']
    sequences = fas_df['sequence'].str.lower()
    # Tokenize sequences
    tokenized_seqs = tok_seqs(sequences)
    # Pad sequences
    padded_seqs = pad_sequences(tokenized_seqs, padding='post', maxlen = PADVALUE, truncating='post')
    # Load model
    modelo = load_model(label_model)
    pred_values = modelo.predict(padded_seqs, batch_size = batch_size_value, verbose = 1)
    # Predict labels
    results_df = label_pred_dataframe(identifiers, pred_values)
    return results_df


if __name__ == '__main__':
    entrada = sys.argv[1]
    print('Running...')
    df = label_prediction(entrada)
    print(df)
    saida = sys.argv[2]
    df.to_csv(saida, index=False, sep='\t')
    print('Done!')

