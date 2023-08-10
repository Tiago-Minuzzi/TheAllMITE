import re
import sys
import shutil
import subprocess
from pathlib import Path
from pyfaidx import Fasta
from typing import TextIO

    
infasta = Path(sys.argv[1])
fa_stem = infasta.stem
curr_dir = infasta.absolute().parent
tmp = curr_dir / 'tmp'
rdout = curr_dir / 'redout'
msk = tmp / f'{fa_stem}.msk'
rpt = tmp / f'{fa_stem}.rpt'
out_fas = curr_dir / f'rpts_{fa_stem}.fasta'


def red_repeat_finder(input_fasta: str, temp_dir: str, redout_dir: str, klen = 13) -> None:
    """Run Red and find repeats"""
    # Change extensions to 'fa'
    renamed_fasta = Path(f'{input_fasta.stem}.fa')

    # Create temporary directory, if not exists.    
    if not temp_dir.exists():
        temp_dir.mkdir()

    # Create Red directory, if not exists.
    if not redout_dir.exists():
        redout_dir.mkdir()

    # Move input fasta to temp directory
    if input_fasta.exists():
        fasta_link = temp_dir/renamed_fasta
        fasta_link.symlink_to(input_fasta.absolute())

    # Run Red
    red_sftw = subprocess.run(['Red',
                             '-gnm',temp_dir,
                             '-len',str(klen),
                             '-msk',redout_dir,
                             '-rpt',redout_dir])

    # If Red succeeds, move output files out of Red directory 
    if red_sftw.returncode == 0:
        # Output files
        masked_fasta = f'{renamed_fasta.stem}.msk'
        repeats = f'{renamed_fasta.stem}.rpt'
        
        # move masked fasta to tmp folder
        masked_fasta_location = redout_dir / masked_fasta
        masked_new_location = temp_dir / masked_fasta
        shutil.move(masked_fasta_location,masked_new_location)

        # move repeat locations file to tmp folder
        repeats_location = redout_dir / repeats
        repeats_new_location = temp_dir / repeats
        shutil.move(repeats_location,repeats_new_location)
        
    elif red_sftw.returncode != 0:
        print(f'Red execution error: {red_sftw.returncode}')

    fasta_link.unlink()
    redout_dir.rmdir()

def repeats_to_fasta(masked_fasta: str, repeats_file: str, repeats_fasta: str) -> TextIO:
    """ Read repeat coordinates from Red output and save the repeats in a fasta file."""
    masked_fasta = Fasta(masked_fasta, read_long_names=True)
    with open(repeats_file) as rpts, open(repeats_fasta,'w') as sd:
        for linha in rpts:
            linha=linha.strip()[1:] # remove '>' from line
            # get sequence name and repeat coordinates
            fid, coords = linha.rsplit(':',1)
            sstart, send = coords.split('-')
            sstart, send = int(sstart), int(send)
            # get sequence
            if 50 <= (send - sstart) <= 30_000: # filter sequences by length
                fsq = masked_fasta[fid][sstart:send].seq
                sstart = sstart + 1
                fid = re.split('\s|\t',fid)[0]
                sid = f'{fid}:{sstart}-{send}'
                record = f'>{sid}\n{fsq}\n'
                # write sequences to file
                sd.write(record)

def main():
    red_repeat_finder(infasta, tmp, rdout)
    print("### Retrieving repeats...")
    repeats_to_fasta(msk, rpt, out_fas)
    if out_fas.exists():
        shutil.rmtree(tmp,ignore_errors=True)
    print('>>> Done.')


if __name__ == "__main__":
    main()

