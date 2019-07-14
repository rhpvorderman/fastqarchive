#!/usr/bin/env python3

from pathlib import Path
import sys

from dnaio import FastqReader, Sequence

if __name__ == '__main__':
    fastq = Path(sys.argv[1])
    with fastq.open('rb') as fastq_handle:

        for sequence in FastqReader(fastq_handle):  # type: Sequence
            sequence.name
            sequence.sequence
            sequence.qualities



