fastqarchive
============

Compress FASTQ data for archival purposes.

Introduction
------------
Fastqarchive reduces redundancy in FASTQ files in order to make them smaller
for long-term storage. It focuses on:

- Compression. Reducing redundancy in fastq files as much as possible.
- Reproducibility. The ability to recreate the original archived files to be
  bit-for-bit identical, even if these were compressed.

Fastqarchive uses UTF-8 encoding to store bases and its qualities. A
base-and-quality combination are mapped to an UTF-8 character. UTF-8
encodes 95 printable characters in 8-bits. Of these ' ' and '@' are omitted
meaning there are 93 characters available to hold the most common
base-and-quality combinations. The remaining base-and-quality combinations are
encoded with a 16-bit UTF-8 character.

Using UTF-8 has the added advantage that fastqarchive files are human-readable.
They can be printed on paper. Binary formats are less suitable
for archival as they can only be decoded by the program that wrote them and
are orders of magnitude harder to reverse engineer than binary formats. This
program is `free/libre software <https://www.gnu.org/philosophy/free-sw.html>`_
(and open-source) so its availability is not restricted by licenses in the
future.

This program is inspired by `Sander Bollen's fastqube project
<https://github.com/sndrtj/fastqube>`_. Fastqube aims to represent FASTQ files
in a binary format in order to optimize compression. Fastqarchive aims to
leverage UTF-8 in order to optimize compression.


Comparison with fastqube
------------------------
This program is inspired by `Sander Bollen's fastqube project
<https://github.com/sndrtj/fastqube>`_. Fastqube aims to represent fastq files
in a binary format to reduce redundancy and increase compression. To do so
it uses bitwise operations. It stores the A,G,C,T,N nucleotides in 3 bits
and the quality score as an integer in 6 bits. Requiring 9 bits in total for
each nucleotide and quality score combination. A regular fastq file requires
16 bits, since it uses two bytes, one for nucleotide and one for quality score.

I like fastqube but I was stuck with the feeling that
compression could be more efficient. There are 5 bases (AGCTN) and 42 phred
qualities, meaning there are 5*42=210 combinations. This only requires 8-bits.

Also fastqube does not support all `IUPAC codes for nucleotides
<https://www.bioinformatics.org/sms/iupac.html>`_ and requires a quality offset
in order to store the phred quality as a 6-bit-integer.

Fastqarchive stores each base-and-quality combination in a dictionary using a
UTF-8 character as a key. This has some advantages over fastqube:

- By assigning the most common base-and-quality combinations to an 8-bit UTF-8
  character, significant compression is achieved. The remaining
  base-and-quality combinations can be encoded using 16-bit UTF-8 characters.
- By using a dictionary all IUPAC codes can be supported.
- By storing the phred quality as a character in the dictionary, it does not
  have to be converted to an integer quality. It also does not have to be
  converted back when decompressing.
- By using UTF-8, the resulting format is human-readable and can be decoded
  even if this program is lost to the world. (Given there is enough information
  in the header.)

However this implementation will come at the cost of speed. As files will
always need to be decoded with UTF-8, and each character needs to be hashed in
order to find the correct base-and-quality combination.
Fastqube can just read its binary format without such limitations.