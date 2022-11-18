#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    A hapax legomenon (often abbreviated to hapax) is a word which occurs
    only once in either the written record of a language, the works of an
    author, or in a single text. Define a function that, when given the
    filename of a text file, will return all its hapaxes. Make sure your
    program ignores capitalization, commas, semicolons, colons, periods,
    and exclamations. Please use the following file:

    2701-0.txt

    Based on this file, there should be 22695 unique words, 12267 hapaxes,
    and 14511 "the" in the text. Your answers should be within 5% of these
    numbers (i.e., within the following ranges):
    A.  Words: 21560 - 23830
    B.  Hapaxes: 11654 - 12880
    C.  "The" count: 13785 - 15237
"""

import argparse
import datetime
from itertools import count

# Public Names
__all__ = (
    'main',
    'counter'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 10, 24)
__author__ = 'Aurel Villyani'


def main():
    """Report all hapax legomenon words found in a file."""
    parser = argparse.ArgumentParser(description='count hapaxes in a file')
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
        counts = counter(args.input)
        # Count the total of unique words in the file
        unique_words = len(counts.keys())
        # Find and count how many hapaxes in the file
        hapaxes = 0
        for value in counts.values():
            if value == 1:
                hapaxes += 1
        # Find and count how many "the" words
        for i in zip(count(), counts):
            count_the = i[0]
        print("Words: ", unique_words)
        print("Hapaxes: ", hapaxes)
        print("\"The\" count:", count_the)
        

def counter(file):
    """Count and get total words from the user file."""
    word_counter = {}
    for line in file:
        for word in line.casefold().split():
            if word in word_counter: 
                word_counter[word] += 1
            else:
                word_counter[word] = 1
    return word_counter


if __name__ == '__main__':
    main()
