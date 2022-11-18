#! /usr/bin/env python3
# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
"""
    a palindrome recognizer that accepts a filename from the user, reads each line, 
    andprints the line to the screen if it is a palindrome. The file should be
    a list of words, phrases, and/or sequences (one per line).
"""

import argparse
import datetime

# Public Names
__all__ = (
    'main',
    'is_palindrome'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 10, 24)
__author__ = 'Aurel Villyani'

# Symbolic Constant
PUNCTUATION = ' ",<>./?@#$%^&*_~'


def main():
    """Print out lines that are palindromes from a file."""
    parser = argparse.ArgumentParser(description='show palindrome lines')
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
        for line in args.input:
            line = line.replace('\n', '')
            if is_palindrome(line):
                print(line)


def is_palindrome(line):
    """This function will validate if the word is palindrome or not."""
    for word in line:
        line += word.casefold()
        if line == line[::-1] and word in PUNCTUATION:
            line.replace(word, "")
            return True


if __name__ == '__main__':
    main()
