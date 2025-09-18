# rfam-families

This repository contains scripts to download and process RNA families from the Rfam database.

## Overview

The goal is to generate a JSON summary of all Rfam families, which can then be filtered for downstream modeling and analysis.

## Workflow

1.  **Download FASTA files**
    The `01-rsync-fasta.sh` script uses `rsync` to download all gzipped FASTA files from the Rfam FTP server into the `fasta_files/` directory.

2.  **Process families**
    The `02-process-families.py` script reads all the downloaded FASTA files, calculates statistics for each family (like number of sequences and 75th percentile of sequence length), and outputs them into `rfam-families.json`.

## Filtering

The `rfam-families.json` file contains an array of objects, where each object represents an RNA family. You can use `jq` to filter this data.

For example, to select families with at least 128 sequences and a 75th percentile sequence length of no more than 300 nucleotides, you can use the following command:

```bash
jq '[.[] | select(.sequence_count >= 128 and .["75th_percentile_seq_len"] <= 300)]' rfam-families.json > rfam-whitelist.json
```
