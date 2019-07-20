# Copyright (C) 2019 Ruben Vorderman, Leiden University Medical Center
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

# cython: language_level=3

from typing import BinaryIO, Iterable, Tuple

def fastq_iterator(fastq_handle: BinaryIO, two_headers: bool = False
                   ) -> Iterable[Tuple[bytes, bytes, bytes]]:
    """
    Iterate over fastq records return name, sequence, qualities as bytes.
    :param fastq_handle: a fastq file handle.
    :param two_headers: Whether the iterator should check if the headers are
    the same.
    :return: name, sequences, qualities. All bytestrings
    """
    cdef bytes name
    cdef bytes sequence
    cdef bytes plus
    cdef bytes qualities
    while True:
        try:
            name = next(fastq_handle).rstrip()
        except StopIteration:
            return
        if not name.startswith(b"@"):
            raise ValueError("Record header should start with '@'.")

        try:
            sequence = next(fastq_handle).rstrip()
            plus_line = next(fastq_handle)
            qualities = next(fastq_handle).rstrip()
        except StopIteration:
            raise ValueError("Incomplete Fastq Record at end of file")

        if two_headers:
            if not plus_line.rstrip()[1:] == name[1:]:
                raise ValueError(
                    "Fastq record with unequal headers: '{0}' and '{1}'"
                    "".format(name, plus_line.rstrip()))

        if len(sequence) != len(qualities):
            raise ValueError(
                "Fastq record with sequence and qualities of unequal length"
            )
        yield name, sequence, qualities


def fastq_iterator2(fastq_handle: BinaryIO, two_headers: bool = False
                   ) -> Iterable[Tuple[bytes, bytes, bytes]]:
    """
    Iterate over fastq records return name, sequence, qualities as bytes.
    :param fastq_handle: a fastq file handle.
    :param two_headers: Whether the iterator should check if the headers are
    the same.
    :return: name, sequences, qualities. All bytestrings
    """
    cdef bytes name
    cdef bytes sequence
    cdef bytes plus
    cdef bytes qualities
    cdef bytes line
    cdef int i = 0
    for line in fastq_handle:
        i += 1
        if i == 1:
            name = line.rstrip()
            if not name.startswith(b"@"):
                raise ValueError("Record header should start with '@'.")
        elif i == 2:
            sequence = line.rstrip()
        elif i == 3 and two_headers:
            plus = line.rstrip()
            if not name[1:] == plus[1:]:
                raise ValueError(
                    "Fastq record with unequal headers: '{0}' and '{1}'"
                    "".format(name, plus))
        elif i == 4:
            qualities = line.rstrip()
            if len(sequence) != len(qualities):
                raise ValueError(
                    "Fastq record with sequence and qualities of unequal length"
                )
            yield name, sequence, qualities
            # reset counter.
            i = 0
        else:  # In case two_headers = False we don't check the plus line.
            pass
    if i != 0:
        # i should be zero if the file ended with a valid fastq record.
        raise ValueError("Incomplete Fastq Record at end of file")
    return