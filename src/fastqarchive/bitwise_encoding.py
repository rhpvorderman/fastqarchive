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

from typing import Iterable, List


def int_list_to_bitstring(int_list: Iterable[int], bit_length: int) -> int:
    bitstring = 0  # type: int # Because a python integer is a list of bits.
    for integer in int_list:
        if integer.bit_length() > bit_length:
            raise ValueError(
                "Integer '{0} is bigger than {1}".format(
                    integer, 2 ** bit_length - 1
                )
            )
        bitstring = bitstring << bit_length  # Same as bitstring * (2 ** bit_length -1)  # noqa: E501
        bitstring += integer

    return bitstring


def bitstring_to_int_list(bitstring: int, bit_length: int) -> List[int]:

    if bitstring.bit_length() % bit_length != 0:
        raise ValueError(
            "Bitstring of length {0} is not divisible by {1}".format(
                bitstring.bit_length(),
                bit_length
            )
        )

    integer_list = []  # type: List[int]

    # If bit_length = 5, bit_mask = "0b11111" bl=6 bm="0b111111" etc.
    bit_mask = 2 ** bit_length - 1

    while bitstring > 0:
        # Get the integer encoded in the last <bit_length> bits.
        integer_list.append(bitstring & bit_mask)
        bitstring = bitstring >> bit_length

    # This means we get the last bits first. Hence we have to reverse the list.
    integer_list.reverse()

    return integer_list


def bitstring_to_right_padded_bytes(bitstring) -> bytes:
    """
    The int.to_bytes() method right-padded mode.
    Example:
        300 in binary is 100101100. That is 9-bits. Each byte contains 8 bits.
        Therefore a minimal of 2 bytes is needed. Which have 16 bits.
        300 will be represented in bytes the following way:
            0000 0001 0010 1100
        The 7 zero's are left padded.
        This function right-pads the bytes. 300 will be represented in this
        way:
            1001 0110 0000 0000
        The advantage being if we know that this is a string of 9-bit numbers
        we can read from the left to the right. The first 9 bits are
        1001 0110 0. We then know for certain that the remaining 7 are left
        over.
    :param bitstring: An integer that can be interpreted as a string of bits
    (example: 001101001011101)
    :return: the right-padded integer.
    """
    # Pad the end with zeros to make sure it fits exactly in a number of bytes.
    bit_overhead = bitstring.bit_length() % 8
    if bit_overhead != 0:
        bitstring = bitstring << (8 - bit_overhead)
    return bitstring.to_bytes(
        length=bitstring.bit_length() // 8,
        byteorder="big",  # Should be big. So it can be read from left to right. # noqa: E501
        signed=False)  # Signed integers do not make sense in a bitstring


def right_padded_bytes_to_bitstring(right_padded_bytes, bit_length) -> int:
    bitstring = int.from_bytes(right_padded_bytes,
                               byteorder="big",
                               signed=False)

    minimum_pad_length = bitstring.bit_length() % bit_length
    bitstring = bitstring >> minimum_pad_length

    max_empty_bitchars = (8 // bit_length - 1
                          if bit_length % 2 == 0
                          else 8 // bit_length)

    for _ in range(max_empty_bitchars):
        # shift if there is an empty bit char
        if bitstring & (2 ** bit_length - 1) == 0:
            bitstring >> bit_length

    return bitstring
