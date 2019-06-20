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

import unicodedata
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import dnaio

import xopen


def printable_utf_chars(exclude_chars: Optional[List[str]] = None
                        ) -> Iterator[str]:
    """
    A generator for printable utf chars that use one or two bytes.
    The characters are outputted in order of their decimal codes.
    :param exclude_chars: Characters that should be excluded
    :return: An iterator that returns one UTF-8 character per iteration.
    """

    if exclude_chars is None:
        exclude_chars = []

    # Check if excludes are single characters by using the ord function.
    for char in exclude_chars:
        try:
            ord(char)
        except TypeError as e:
            # Raise custom message.
            # Ord does not show the original input in its error.
            raise TypeError("'{0}' is not a character. {1}".format(
                char, str(e)))

    exclude_set = set(exclude_chars)

    # For two byte UTF-8 characters only accept characters from the following
    # categories:
    # 'Ll' : lower-case letters
    # 'Lu' : upper-case letters
    # Other categories do not uniformly have characters that are easy to
    # distinguish from whitespace. For example: '´' or '¸'
    two_byte_categories = {'Ll', 'Lu'}

    for i in range(2048):
        char = chr(i)
        if char in exclude_set:
            continue

        # One-byte UTF-8 characters
        elif i < 128 and char.isprintable() and not char.isspace():
            yield char

        # Two-byte UTF-8 characters
        elif i >= 128 and unicodedata.category(char) in two_byte_categories:
            yield char
        else:
            continue


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

    sorted_items = sorted(counts_dict.items(),
                          key=lambda _, count: count,
                          reverse=True)

    # '@' should be reserved for headers
    utf_iter = printable_utf_chars(exclude_chars=["@"])

    return {base_qual_combo: next(utf_iter)
            for base_qual_combo, count in sorted_items}


def encode_to_decode_dict(encode_dict: Dict[Tuple[str, str], str]
                          ) -> Dict[str, Tuple[str, str]]:
    return {utf_char: base_qual_combo
            for base_qual_combo, utf_char in encode_dict.items()}


def encode_fastq(fastq: Path, encode_dict: Dict[Tuple[str, str], str]
                 ) -> Iterator[Tuple[str, str]]:
    with xopen.xopen(fastq, mode='rb') as fastq_handle:
        fastq_iter = dnaio.FastqReader(fastq_handle)

        for sequence in fastq_iter:  # type: dnaio.Sequence

            # A generator expression that returns characters
            coded_chars = (
                encode_dict[base_qual_combo] for base_qual_combo
                in zip(sequence.sequence, sequence.qualities)
            )

            # use "".join to convert coded_chars into a string
            yield sequence.name, "".join(coded_chars)
