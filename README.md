# The All MITE

The All MITE is a MITE classifier tool using artificial neural networks.
It's on **alpha** stage.

You can run on your transposable element sequences to evaluate if there are MITEs among them.

At first, it filter sequences by length, then, the remaining sequences are classified as either being MITE or not MITE; finally, sequences classified as MITEs by the first model are classified as either Stowaway or Tourist.

## What are MITEs?

MITEs, or Miniature Inverted-repeat Transposable Elements, are a type of transposable element found in the genomes of various organisms, including plants and some animals. Transposable elements (TEs) are DNA sequences that have the ability to move, or transpose, within a genome. They can have significant impacts on the structure and function of genomes, as well as contribute to genetic diversity and evolution.
MITEs are characterized by their small size, typically ranging from around 100 to 800 base pairs in length, and are non-autonomous transposable elements, which means they lack the coding sequences necessary for their own transposition. Instead, they rely on the machinery of other transposable elements, known as autonomous elements, to facilitate their movement. These autonomous elements provide the necessary enzymes and proteins for transposition, allowing MITEs to hitch a ride and be copied and inserted into new genomic locations.

## Installation

It's recommended to install it in a virtual environment.

`Python >= 3.8` and `pip` are required to install the dependencies. To install run:

`pip install -r requirements.txt`

## Usage

To run it use:

`python3 the_all_mite.py /path/to/your/file.fasta`

Example: 

`python3 the_all_mite.py /home/User/fastas/my_te_library.fasta`

The output is a TSV file containing the prediction results as below:
| id | len | prediction_1 | accuracy_1 | prediction_2 | accuracy_2 |
| --- | --- | ---------- | ------------ | ----------- | ---------- |
| MITE_MS    miniature inverted repeat   Medicago sativa | 184 | MITE | 1.0 | Tourist | 1.0 |
| MITE_AA    MITE    Aedes aegypti | 521 | MITE | 1.0 | Stowaway | 0.7799 |
| ORGANDY_BM MITE    Bombyx mori | 548 | MITE | 0.9042 | Tourist | 0.9999 |
| MERMITE18A MuDR    Oryza sativa   | 526 | MITE | 1.0 | Tourist | 0.9997 |
| AgaP8MITE2450  P   Anopheles gambiae | 2456 | NM | 1.0 | NM | 1.0 |

NM: not MITE.

## To do

- [x] Accuracy score in the output table.
- [ ] Output FASTA file for MITE sequences.
- [ ] Add command-line options.
- [ ] Add repeat extraction tool to use in genomes.
- [ ] Add a conda recipe.

