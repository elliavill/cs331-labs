#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

# Public Names
__all__ = (
    'ICAO_ALPHABET',
    'main',
    'convert_ICAO'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 10, 17)
__author__ = 'Aurel Villyani'

# Symbolic Constants
# noinspection PyTypeChecker
ICAO_ALPHABET = dict(line.split('-', 1) for line in '''\
a-alpha
b-bravo
c-charlie
d-delta
e-echo
f-foxtrot
g-golf
h-hotel
i-india
j-juliett
k-kilo
l-lima
m-mike
n-november
o-oscar
p-papa
q-quebe
r-romeo
s-sierra
t-tango
u-uniform
v-victor
w-whiskey
x-x-ray
y-yankee
z-zulu'''.splitlines())


def main():
    """Run each of the scripts as specified in the lab's instructions."""
    try:
        for word in input('Enter your message: ').split():
            print(word, '-->', '-'.join(convert_ICAO(word)))
    except EOFError:
        print("Exiting")


# noinspection PyPep8Naming
def convert_ICAO(word):
    """Assign the words to the letters of English alphabet acrophonically."""
    # Can you write a generator expression that does the following?
    #   1. Folds the case of each character in the word.
    #   2. Checks if the character is alphabetic or not.
    #   3. Uses a dictionary to find their correct word.
    generator = (ICAO_ALPHABET[letter] for letter in word.casefold()
                 if letter.isalpha())
    return generator


if __name__ == '__main__':
    main()
