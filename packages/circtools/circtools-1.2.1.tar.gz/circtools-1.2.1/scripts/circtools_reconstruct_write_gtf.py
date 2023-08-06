#!/usr/bin/env python3

# Copyright (C) 2019 Tobias Jakobi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import sys


def check_input_files(file):
    """Checks supplied file for existence.
    Will halt the program if file not accessible
    """
    # check if exists
    if not os.path.isfile(file):
        message = ("File " + str(file) + " cannot be found, exiting.")
        sys.exit(message)


# main script starts here


parser = argparse.ArgumentParser(description='Replaces the TCONS names of cuffmerge with transcript IDs in FASTA files')

group = parser.add_argument_group("Input")

group.add_argument("-i",
                   "--input",
                   dest="input_gtf",
                   help="BED file",
                   required=True
                   )

group.add_argument("-o",
                   "--output",
                   dest="output_file",
                   help="Full URI to new FASTA file",
                   required=True,
                   )

args = parser.parse_args()

check_input_files(args.input_gtf)

try:
    file_handle = open(args.input_gtf)
except PermissionError:
    message = ("Input file " + str(args.input_gtf) + " cannot be read, exiting.")
    sys.exit(message)
else:
    counter = 1
    output_file = open(args.output_file, "w")

    with file_handle:
        line_iterator = iter(file_handle)
        for line in line_iterator:
            # we skip any comment lines
            if line.startswith("#"):
                continue

            # get current name
            tmp = line.split('\t')

            chromosome = tmp[0].rstrip()
            start = tmp[1].rstrip()
            stop = tmp[2].rstrip()
            description = tmp[3].rstrip()
            number = tmp[4].rstrip()

            print(chromosome + "\t"
                               "circtools" + "\t" +
                                "gene" + "\t" +
                  start + "\t" +
                  stop + "\t" +
                  ".\t" +
                  ".\t" +
                  ".\t" +
                  "gene_id \"circtools_gene_" + str(counter) + "\"; " +
                  "gene_name \"circtools_gene_" + str(counter) + "\"; " +
                  "gene_source \"circtools\"; " +
                  "gene_biotype \"circular RNA\"",
                  file=output_file
                  )

            print(chromosome + "\t"
                               "circtools" + "\t" +
                                "transcript" + "\t" +
                  start + "\t" +
                  stop + "\t" +
                  ".\t" +
                  ".\t" +
                  ".\t" +
                  "gene_id \"circtools_gene_" + str(counter) + "\"; " +
                  "gene_name \"circtools_gene_" + str(counter) + "\"; " +
                  "transcript_id \"circtools_transcript_" + str(counter) + "\"; " +
                  "gene_source \"circtools\"; " +
                  "gene_biotype \"circular RNA\"",
                  file=output_file
                  )

            print(chromosome + "\t"
                               "circtools" + "\t" +
                                "exon" + "\t" +
                  start + "\t" +
                  stop + "\t" +
                  ".\t" +
                  ".\t" +
                  ".\t" +
                  "gene_id \"circtools_gene_" + str(counter) + "\"; " +
                  "gene_name \"circtools_gene_" + str(counter) + "\"; " +
                  "transcript_id \"circtools_transcript_" + str(counter) + "\"; " +
                  "gene_source \"circtools\"; " +
                  "gene_biotype \"circular RNA\"",
                  file=output_file
                  )
            counter += 1


