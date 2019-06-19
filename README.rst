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
- Long-term storage. Files should be readable 10 years from now.

Fastqarchive uses UTF-8 encoding to store bases and its qualities. UTF-8 can
store



uman-readable (text-based) archive format. Binary formats are less suitable
for archival as they can only be decoded by the program that wrote them and
are orders of magnitude harder to reverse engineer than binary formats. This
program is `free/libre software <https://www.gnu.org/philosophy/free-sw.html>`_
(and open-source) so its availability is not restricted by licenses in the
future.

This program is inspired by `Sander Bollen's fastqube project
<https://github.com/sndrtj/fastqube>`_.


Comparison with fastqube
------------------------
This program is inspired by `Sander Bollen's fastqube project
<https://github.com/sndrtj/fastqube>`_. Fastqube aims to represent fastq files
in a binary format to reduce redundancy and increase compression. To do so
it uses bitwise operations. It stores the A,G,C,T,N nucleotides in 3 bits
and the quality score as an integer in 6 bits. Requiring 9 bits in total for
each nucleotide and quality score combination. A regular fastq file requires
16 bits, since it uses two bytes, one for nucleotide and one for quality score.

Sander told me about this project, and I was stuck with the feeling that compr