import sys
import subprocess

IN_FASTA = sys.argv[1]


subprocess.run(["python","find_repeats.py",IN_FASTA])
