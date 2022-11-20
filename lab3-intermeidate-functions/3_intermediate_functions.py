#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import string

# Public Names
__all__ = (
    'main',
    'generate_n_chars',
    'max_in_list',
    'find_longest_word',
    'filter_long_words',
    'is_pangram',
    'generate_song',
    'char_freq'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 9, 26)
__author__ = 'Aurel Villyani'


def main():
    """Run each of the scripts as specified in the lab's instructions."""
    print(generate_n_chars('x', 5))
    print(max_in_list([11, 17, 13]))
    print(find_longest_word('Chappell'.split()))
    print(filter_long_words('Chappell'.split(), 7))
    print(is_pangram('The quick brown fox jumps over the lazy dog.'))
    print(*generate_song(), sep='\n')
    print(char_freq('abbabcbdbabdbdbabababcbcbab'))


def generate_n_chars(character, number):
    """Return the character repeated number times."""
    if not isinstance(character, str):
        raise TypeError('character must be a string')
    if len(character) != 1:
        raise ValueError('character must be of length 1')
    answer = ''
    for _ in range(number):
        answer += character
    return answer


def max_in_list(list_of_numbers):
    """Return the largest value in the list."""
    if not isinstance(list_of_numbers, list):
        raise TypeError('list_of_numbers must be a list')
    if len(list_of_numbers) < 1:
        raise ValueError('list_of_numbers must have at least one item')
    if not all(isinstance(item, (int, float)) for item in list_of_numbers):
        raise TypeError('all items in list_of_numbers must be int or float')
    largest = list_of_numbers[0]
    for number in list_of_numbers:
        if number > largest:
            largest = number
    return largest


def find_longest_word(list_of_words):
    """Find the length of the longest word in the list."""
    return max_in_list(list(map(len, list_of_words)))


def filter_long_words(list_of_words, number):
    """Get a list of words having a length greater than number."""
    sentence = []
    for counter in range(len(list_of_words)):
        if len(list_of_words[counter]) > number:
            sentence.append(list_of_words[counter])
    return sentence


def is_pangram(sentence):
    """Verify whether the sentence is a pangram."""
    return set(string.ascii_lowercase) <= set(sentence.lower())


def generate_song(the_range=range(99, 0, -1), beverage='milk'):
    """Yield all the lines to the requested song."""
    for current_count in the_range:
        yield f"{current_count} bottle{'s' if current_count != 1 else ''}" \
              f" of {beverage} on the wall, {current_count}" \
              f" bottle{'s' if current_count != 1 else ''} of {beverage}."
        yield f"Take one down, pass it around, {current_count - 1}" \
              f" bottle{'s' if current_count - 1 > 1 else ''}"


def char_freq(characters):
    """Calculate the frequency of each character using a dictionary."""
    total_frequency = {}
    for counter in characters:
        if counter in total_frequency:
            total_frequency[counter] += 1
        else:
            total_frequency[counter] = 1
    return total_frequency


if __name__ == '__main__':
    main()
