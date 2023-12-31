import sys
import subprocess
from typing import TextIO


repeats_fasta = sys.argv[1]
clustered_fasta = sys.argv[2]

def cluster_sequences(repeats_fasta: str, clustered_fasta: str) -> TextIO:
    """Run cd-hit-est to cluster most similar predicted TE sequences."""
    cdhit = subprocess.run(['cd-hit-est',
                            '-i',repeats_fasta,
                            '-o',clustered_fasta,
                            '-G','0', # use local sequence identity
                            '-aS','0.8', # alignment coverage for the shorter sequence
                            '-c','0.8', # sequence identity threshold
                            '-M','0', # Memory limit. 0 means no limit.
                            '-T','0']) # Number of threads to use. 0 means all threads.
    

if __name__ == "__main__":
    cluster_sequences(repeats_fasta, clustered_fasta)
