import glob
import gzip
import json
import os

import numpy as np
from Bio import SeqIO


def calculate_params(sequences):
    batch_size = 64
    checkpoints = 100

    seq_lengths = [len(seq.seq) for seq in sequences]
    num_seqs = len(sequences)

    if num_seqs == 0:
        seq_len = 0
    else:
        seq_len = int(np.percentile(seq_lengths, 75))

    if seq_len <= 80:
        target_models = 500
    elif seq_len <= 120:
        target_models = 600
    elif seq_len <= 150:
        target_models = 700
    elif seq_len <= 200:
        target_models = 800
    elif seq_len <= 300:
        target_models = 1000
    else:
        target_models = 1000

    target_batches = target_models * checkpoints

    batches_per_epoch = int(np.ceil(num_seqs / batch_size))

    if batches_per_epoch == 0:
        epochs = 1
    else:
        epochs = int(np.ceil(target_batches / batches_per_epoch))

    if batches_per_epoch >= target_batches:
        epochs = 1

    return num_seqs, seq_len, epochs


def main():
    family_files = glob.glob("fasta_files/RF*.gz")
    families_data = []

    for f_path in sorted(family_files):
        family_id = os.path.basename(f_path).split(".")[0]

        with gzip.open(f_path, "rt") as handle:
            sequences = list(SeqIO.parse(handle, "fasta"))

        num_seqs, seq_len_75th, epochs = calculate_params(sequences)

        family_info = {
            "id": family_id,
            "sequence_count": num_seqs,
            "75th_percentile_seq_len": seq_len_75th,
            "epoch_count": epochs,
        }
        families_data.append(family_info)

    with open("rfam-families.json", "w") as outfile:
        json.dump(families_data, outfile, indent=4)


if __name__ == "__main__":
    main()
