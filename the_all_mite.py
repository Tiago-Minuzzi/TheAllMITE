import os
import sys
import numpy as np
import pandas as pd
# Hide warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from tensorflow.keras.models import load_model
from utils.preprocessing import fasta_reader, tokenize, zero_padder

# IN_FASTA = sys.argv[1]
IN_FASTA = '/home/tiago/Downloads/MITES_soybase.fasta'

MODEL_1 = load_model('models/mite_class_1.h5')
MODEL_2 = load_model('models/mite_class_2.h5')

records = fasta_reader(IN_FASTA)
long_records = []
test_records = []

for i in records:
    if i.len > 800:
        long_records.append(i)
    else:
        test_records.append(i)

# Sequences too long to be a MITE
not_mite_filtered = pd.DataFrame(long_records)
not_mite_filtered['prediction_1'] = 'NM'
not_mite_filtered = not_mite_filtered.loc[:, ['id', 'len', 'prediction_1']]

# Tokenized and padded sequences
sequence_arrays = zero_padder([tokenize(record.seq) for record in test_records])

results_1 = np.argmax(MODEL_1.predict(sequence_arrays), axis=1)
df1 = pd.DataFrame(test_records)
df1['prediction_1'] = results_1
df1['prediction_1'] = df1['prediction_1'].map({0: 'NM', 1: 'MITE'})

not_mite_pred_1 = df1.loc[df1['prediction_1'] != 'MITE']
drop_not_mite = df1.loc[df1['prediction_1'] != 'MITE'].index.to_list()
not_mite_pred_1 = not_mite_pred_1.loc[:, ['id', 'len', 'prediction_1']]
not_mite = pd.concat([not_mite_filtered, not_mite_pred_1])

mites = df1.loc[df1['prediction_1'] == 'MITE']

sequence_arrays = np.delete(sequence_arrays, drop_not_mite, axis=0)

results_2 = np.argmax(MODEL_2.predict(sequence_arrays), axis=1)
mites['prediction_2'] = results_2
mites['prediction_2'] = mites['prediction_2'].map({0: 'Stowaway', 1: 'Tourist'})
mites = mites.loc[:, ['id', 'len', 'prediction_1', 'prediction_2']]
final_results = pd.concat([mites, not_mite]).fillna('NM')
final_results.to_csv('results_TheAllMITE.tsv', sep='\t', index=False)

