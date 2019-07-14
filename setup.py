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

from setuptools import find_packages, setup

with open("README.rst", "r") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name="fastqarchive",
    version="0.1.0-dev",
    description="Compress FASTQ data for archival purposes.",
    author="Ruben Vorderman",
    author_email="r.h.p.vorderman@lumc.nl",  # A placeholder for now
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    license="AGPL-3.0-or-later",
    keywords="",
    zip_safe=False,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url="https://github.com/rhpvorderman/fastqarchive",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    python_requires=">=3.5",  # Because we use type annotation.
    install_requires=[
        "xopen>=0.6.0",
    ],
)
