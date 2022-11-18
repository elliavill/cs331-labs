#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Calculate the average word length of a text
    stored in a file (i.e., the sum of all the lengths of the word tokens
    in the text divided by the number of word tokens).
"""

import argparse
import datetime

# Public Names
__all__ = (
    'main',
    'average_word_length'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 10, 24)
__author__ = 'Aurel Villyani'
__credits__ = 'CS 331'


def main():
    """Calculate the average length of words from a file."""
    parser = argparse.ArgumentParser(description='calculate average word size')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=f'%(prog)s {".".join(map(str, __version__))}')
    parser.add_argument('-i', '--input',
                        type=argparse.FileType('rt', -1, 'latin_1'),
                        required=True,
                        help='path to the file that should be processed',
                        metavar='(<input file> | "-" for stdin)')
    args = parser.parse_args()
    with args.input:
        average_word_length(args.input)


def average_word_length(lines):
    """Calculate the average word length of a text stored in a file."""
    total_word_count = 0
    total_word_length = 0
    for line in lines:
        words = line.split()
        total_word_count += len(words)
        for word in words:
            total_word_length += len(word)
    average = total_word_length / total_word_count
    print("Average word length = ", average)


if __name__ == "__main__":
    main()
