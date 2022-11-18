#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime

# Public Names
__all__ = (
    'BILINGUAL_LEXICON',
    'TEST_SENTENCE',
    'ROT_13_KEY',
    'SECRET_MESSAGE',
    'main',
    'translate',
    'run_rot_13',
    'execute_rot_13_command_line_program'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 10, 10)
__author__ = 'Aurel Villyani'

# Symbolic Constants
BILINGUAL_LEXICON = {
    'merry': 'god',
    'christmas': 'jul',
    'and': 'och',
    'happy': 'gott',
    'new': 'nytt',
    'year': 'år'
}
TEST_SENTENCE = 'Have yourself a merry christmas and a happy new year please.'
ROT_13_KEY = {
    65: 78, 66: 79, 67: 80, 68: 81, 69: 82, 70: 83, 71: 84, 72: 85, 73: 86,
    74: 87, 75: 88, 76: 89, 77: 90, 78: 65, 79: 66, 80: 67, 81: 68, 82: 69,
    83: 70, 84: 71, 85: 72, 86: 73, 87: 74, 88: 75, 89: 76, 90: 77, 97: 110,
    98: 111, 99: 112, 100: 113, 101: 114, 102: 115, 103: 116, 104: 117,
    105: 118, 106: 119, 107: 120, 108: 121, 109: 122, 110: 97, 111: 98,
    112: 99, 113: 100, 114: 101, 115: 102, 116: 103, 117: 104, 118: 105,
    119: 106, 120: 107, 121: 108, 122: 109
}
SECRET_MESSAGE = 'Pnrfne pvcure? V zhpu cersre Pnrfne fnynq!'


def main():
    """Run each of the scripts as specified in the lab's instructions."""
    try:
        print(' '.join(translate(TEST_SENTENCE.split())))
        print(run_rot_13(SECRET_MESSAGE))
        execute_rot_13_command_line_program()
    except KeyError:
        print("This information is not available.")


def translate(english_words):
    """Translate english to swedish words with bilingual lexicon."""
    for word in english_words:
        yield BILINGUAL_LEXICON.get(word, word)
    return word


def run_rot_13(message):
    """Encode and decode message by using ROT-13 key."""
    return message.translate(ROT_13_KEY)


def execute_rot_13_command_line_program():
    """Show the parser for the command-line options."""
    parser = argparse.ArgumentParser\
            (description='translate file using ROT 13')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + '.'.join(map(str, __version__)))
    parser.add_argument('-i','--input',
                        type=argparse.FileType('r', encoding='latin_1'),
                        metavar='<input file>',
                        required=True,
                        help='path to the file that should be processed')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w', encoding='latin_1'),
                        metavar='<output file>',
                        required=True,
                        help='path where the results will be saved to')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", '--encode',
                       action='store_true',
                       help='specify that the input file should be encoded')
    group.add_argument('-d', '--decode',
                       action='store_true',
                       help='specify that the input file should be decoded')
    args = parser.parse_args()
    assert args.encode != args.decode, '-e and -d are configured incorrectly'
    with args.input, args.output as output_file:
        for line in args.input:
            rot_13_line = run_rot_13(line)
            output_file.write(rot_13_line)


if __name__ == '__main__':
    main()
