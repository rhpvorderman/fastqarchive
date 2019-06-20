# Copyright (C) 2019 Leiden University Medical Center
# This file is part of fastqarchive
#
# fastqarchive is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# fastqarchive is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with fastqarchive.  If not, see <https://www.gnu.org/licenses/

from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import dnaio

import xopen


def count_base_and_quality_combinations(
        fastq: Path) -> Dict[Tuple[str, str], int]:
    """
    Counts base and quality combinations.
    :param fastq: The fastq file.
    :return: A dictionary {(Base, Quality): Count}
    """
    counts_dict = {}
    with xopen.xopen(fastq, mode='rb') as fastq_handle:
        fastq_reader = dnaio.FastqReader(fastq_handle)
        for record in fastq_reader:  # type: dnaio.Sequence
            for base_qual_combo in zip(record.sequence, record.qualities):
                try:
                    counts_dict[base_qual_combo] += 1
                except KeyError:
                    counts_dict[base_qual_combo] = 1
    return counts_dict


def counts_to_encode_dict(counts_dict: Dict[Tuple[str, str], int]
                          ) -> Dict[Tuple[str, str], str]:
    pass


def printable_two_byte_utf_eight_chars(excludes: Optional[List[str]] = None
                                       ) -> Iterator[str]:
    if excludes is None:
        excludes = []

    excluded_char_numbers = []

    # Exclude user defined exclude characters
    excluded_char_numbers += [ord(char) for char in excludes]

    # Exclude ranges which cannot be printed as a single character
    excluded_char_numbers += list(range(32))        # Control characters
    excluded_char_numbers += [127]                  # Control character (Delete)
    excluded_char_numbers += list(range(128, 160))  # control characters
    excluded_char_numbers += list(range(688, 768))  # Spacing Modifier Letters
    # Exclude all non-printable and space characters known by python
    for i in range(2048):
        char = chr(i)
        if char.isprintable() and not char.isspace():
            excluded_char_numbers.append(i)
