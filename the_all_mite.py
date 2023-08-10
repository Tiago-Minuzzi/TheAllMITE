import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
# Hide warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from tensorflow.keras.models import load_model
from utils.preprocessing import fasta_reader, tokenize, zero_padder

# Get the current directory
THEALLMITE_DIR = Path(__file__).parent

# Input fasta file
IN_FASTA = Path(sys.argv[1])
BASE_NAME = IN_FASTA.stem

# Output files
OUT_TABLE = f"TheAllMITE_{BASE_NAME}.tsv"

# load models
MODEL_1 = load_model(THEALLMITE_DIR / 'models/mite_class_1.h5')
MODEL_2 = load_model(THEALLMITE_DIR / 'models/mite_class_2.h5')

# Read input fasta
records = fasta_reader(IN_FASTA)
long_records = []  # store sequences above the MITE lenght (set to 800)
test_records = []  # store sequences <= 800 nt

# filter sequences by size
for i in records:
    if i.len > 800:
        long_records.append(i)
    else:
        test_records.append(i)

# Tokenized and padded sequences
sequence_arrays = zero_padder([tokenize(record.seq) for record in test_records])

# Sequences too long to be a MITE
print("### Step 01: Filtering sequences longer than 800 bases.")
not_mite_filtered = pd.DataFrame(long_records)
not_mite_filtered['prediction_1'] = 'NM'
not_mite_filtered = not_mite_filtered.loc[:, ['id', 'len', 'prediction_1']]
print(">>> Step 01 done!\n")


# create dataframe from model 1 predictions
print("### Step 02: Starting first prediction: MITE/not MITE")
results_1 = np.argmax(MODEL_1.predict(sequence_arrays), axis=1)
df1 = pd.DataFrame(test_records)
df1['prediction_1'] = results_1
df1['prediction_1'] = df1['prediction_1'].map({0: 'NM', 1: 'MITE'})
print(">>> Step 02 done!\n")


# select sequences classified as not MITE
not_mite_pred_1 = df1.loc[df1['prediction_1'] != 'MITE']
drop_not_mite = df1.loc[df1['prediction_1'] != 'MITE'].index.to_list()  # get index to drop from sequence array
not_mite_pred_1 = not_mite_pred_1.loc[:, ['id', 'len', 'prediction_1']]

# Concatenate sequences filtered as not MITE by length and the ones classified as not MITE
not_mite = pd.concat([not_mite_filtered, not_mite_pred_1])

# drop sequences not classified as MITE by model 1
sequence_arrays = np.delete(sequence_arrays, drop_not_mite, axis=0)

# Select sequences classified as MITE by model 1
mites = df1.loc[df1['prediction_1'] == 'MITE']

# Predict Stowaway and Tourist
print("### Step 03: Starting second prediction: Stowaway/Tourist")
results_2 = np.argmax(MODEL_2.predict(sequence_arrays), axis=1)
mites['prediction_2'] = results_2
mites['prediction_2'] = mites['prediction_2'].map({0: 'Stowaway', 1: 'Tourist'})
mites = mites.loc[:, ['id', 'len', 'prediction_1', 'prediction_2']]
print(">>> Step 03 done!\n")

# Create final table
final_results = pd.concat([mites, not_mite]).fillna('NM')
final_results.to_csv(OUT_TABLE, sep='\t', index=False)
