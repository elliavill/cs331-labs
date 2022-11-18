#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

# Public Names
__all__ = (
    'main',
    'max_',
    'max_of_three',
    'len_',
    'sum_',
    'multiply',
    'reversed_',
    'is_vowel',
    'is_member',
    'overlapping',
    'translate'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 9, 19)
__author__ = 'Aurel Villyani'


def main():
    """Run each of the scripts as specified in the lab's instructions."""
    print(max_(7, 5))
    print(max_of_three(11, 17, 13))
    print(len_('Stephen Paul Chappell'))
    print(sum_((1, 2, 3, 4)))
    print(multiply((1, 2, 3, 4)))
    print(reversed_('I am testing.'))
    print(is_vowel('y'))
    print(is_member(2, [1, 2, 3]))
    print(overlapping([1, 2, 3], [3, 4, 5]))
    print(translate('this is fun'))


def max_(a, b):
    """Return the largest of two values without using the max function."""
    largest_value = a if a > b else b
    return largest_value


def max_of_three(a, b, c):
    """Return the largest of three values without using the max function."""
    largest_value = a;
    if b >= a and b >= c:
        largest_value = b
    elif c >= a and c >= b:
        largest_value = c
    return largest_value


def len_(data):
    """Calculate the length of the data parameter."""
    counter = 0
    for letter in data:
        counter += 1
    return counter


def sum_(data):
    """Calculate the sum of the numbers in the data parameter."""
    total_sum = 0
    for value in data:
        total_sum += value
    return total_sum


def multiply(data):
    """Calculate the product of the values in the data parameter."""
    total_product = 1
    for value in data:
        total_product *= value
    return total_product


def reversed_(text):
    """Return the reverse of a string."""
    reversed_string = ""
    for items in range(1, len(text) + 1):
        reversed_string += text[len(text) - items]
    return reversed_string


def is_vowel(character, vowels='AEIOUaeiou'):
    """Check if the character is a vowel or not."""
    for data in vowels:
        if data == character:
            return True
    return False


def is_member(item, array):
    """Find out if the item is part of the array."""
    for data in array:
        if data == item:
            break
    else:
        return False
    return True


def overlapping(list_a, list_b):
    """Return whether the two lists have any item in common."""
    for item_a in list_a:
        for item_b in list_b:
            if item_a == item_b:
                return True
    return False


def translate(text, consonant='bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'):
    """Translate the text into robber's language."""
    letter_and_o = ''
    for character in text:
        if character in consonant:
            letter_and_o += character + 'o'
        letter_and_o += character
    return letter_and_o


if __name__ == '__main__':
    main()
