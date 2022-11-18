#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    When given a text file, will create a new text file in which all the
    lines from the original file are numbers from 1 to n.
"""

import argparse
import datetime

# Public Names
__all__ = (
    'main'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 10, 24)
__author__ = 'Aurel Villyani'


def main():
    """Add line numbers to a file and write to another file."""
    parser = argparse.ArgumentParser(description='add line numbers to file')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=f'%(prog)s {".".join(map(str, __version__))}')
    parser.add_argument('-i', '--input',
                        type=argparse.FileType('rt', -1, 'latin_1'),
                        required=True,
                        help='path to the file that should be processed',
                        metavar='(<input file> | "-" for stdin)')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('wt', -1, 'latin_1'),
                        required=True,
                        help='path where the results will be saved to',
                        metavar='(<output file> | "-" for stdout)')
    args = parser.parse_args()
    with args.input as src, args.output as dst:
        # Iterate through every line and display the line number
        line_number = 0
        for line in src:
            line_number += 1
            print(f'{line_number} {line}', end='', file=dst)


if __name__ == "__main__":
    main()
