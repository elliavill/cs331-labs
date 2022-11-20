#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

# Public Names
__all__ = (
    'main',
    'function_1',
    'function_2',
    'function_3',
    'function_4',
    'function_5',
    'function_6'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 9, 10)
__author__ = 'Aurel Villyani'


def main():
    """Run each of the scripts as specified in the lab's instructions."""
    print(function_1(7,5))
    print(function_2(11, 17, 13))
    print("Your name has ", function_3('Full Name'), " characters in it.")
    print("After adding all the numbers, ", function_4(list(range(1, 11))), " is your total.")
    print("After multiplying all the numbers, ", function_5(list(range(1, 11))), " is the product.")
    print(function_6('I am testing.'))


def function_1(a, b):
    """Print the largest of two values without using the max function."""
    if a >= b:
        return a
    else:
        return b 


def function_2(a, b, c):
    """Print the largest of three values without using the max function."""
    largest = a
    if b > largest:
       return b
    if c > largest:
       return c


def function_3(my_name):
    """Show the length of the my_name parameter."""
    counter = 0
    for letter in my_name:
       counter += 1
    return counter


def function_4(my_list):
    """Display the sum of the numbers in the my_list parameter."""
    return sum(my_list)


def function_5(my_list):
    """Get the product of my_list and print out the value."""
    product = 1
    for items in my_list:
        product *= items
    return product


def function_6(text):
    """Print out text in reverse without using [::-1] to do so."""
    reversedString = ""
    for items in range(1, len(text) + 1):
        reversedString += text[len(text) - items]
    return reversedString


if __name__ == '__main__':
    main()