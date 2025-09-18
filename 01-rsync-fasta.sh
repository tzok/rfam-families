#! /usr/bin/env bash
mkdir -p fasta_files
rsync \
	--archive \
	--progress \
	rsync.ebi.ac.uk::pub/databases/Rfam/CURRENT/fasta_files/ \
	fasta_files/