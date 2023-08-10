import numpy as np
from typing import TextIO
from collections import namedtuple
from Bio.SeqIO.FastaIO import SimpleFastaParser


def fasta_reader(ffasta: TextIO) -> list[tuple]:
    record = namedtuple('record', 'fid seq len')
    records = []
    with open(ffasta) as fa:
        for fid, fsq in SimpleFastaParser(fa):
            fsq = fsq.lower()
            records.append(record(fid, fsq, len(fsq)))
    return records

def tokenize(sequence: str) -> list:
    """Transform nucleotide sequences into an list of integers."""
    nt_dict = {'a': 1, 'c': 2, 'g': 3, 't': 4}
    return [nt_dict.get(n, 5) for n in sequence]


def zero_padder(self, arr: list, pad_len: int = 800) -> np.ndarray:
    """Appends zeros to inner arrays of list of arrays to make all arrays the same length."""

    return np.array([np.hstack([a[:pad_len], np.zeros(pad_len - len(a[:pad_len]))]) for a in arr])
