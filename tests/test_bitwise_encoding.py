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

from fastqarchive.bitwise_encoding \
    import bitstring_to_int_list, bitstring_to_right_padded_bytes, \
    int_list_to_bitstring

import pytest

INT_LISTS_BITSTRINGS = [
    ([1,2,3], 3, 0b0010100110000000.to_bytes(2, "big")),
    ([1,2,3], 4, 0b0001001000110000.to_bytes(2, "big")),
    ([1,2,3], 5, 0b0000100010000110.to_bytes(2, "big")),
    ([12,25], 5, 0b0110011001000000.to_bytes(2, "big"))
]


@pytest.mark.parametrize(["int_list", "bit_length", "bitstring"], INT_LISTS_BITSTRINGS)
def test_int_list_to_bitstring(int_list, bit_length, bitstring):
    assert int_list_to_bitstring(int_list, bit_length) == bitstring


@pytest.mark.parametrize(["int_list", "bit_length", "bitstring"], INT_LISTS_BITSTRINGS)
def test_bitstring_to_int_list(bitstring, bit_length, int_list):
    assert bitstring_to_int_list(bitstring, bit_length) == int_list