#!/usr/bin/env python3

from pathlib import Path
import sys

from fastqarchive.fastq_properties import fastq_iterator

if __name__ == '__main__':
    fastq = Path(sys.argv[1])
    with fastq.open('rb') as fastq_handle:
        for name, sequence, qualities in fastq_iterator(fastq_handle):
            pass

