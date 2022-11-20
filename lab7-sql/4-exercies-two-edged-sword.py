#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import datetime
import enum
import itertools
import mmap
import pathlib
import sqlite3
import sys
import textwrap
# from itertools import pairwise

# Public Names
__all__ = (
    'DEFAULT_ENCODING',
    'BIBLE_TXT',
    'BIBLE_DB',
    'SQL',
    'main',
    'parse_bible',
    'sniff_next_line',
    'read_until_locked',
    'make_database',
    'table_exists',
    'populate_database',
    'has_rows',
    'test_database',
    'parse_book_names',
    'read_table_of_contents',
    'get_reference_and_text',
    'get_bible_reference',
    'clean',
    'retrieve_bible_verse',
    'Bible',
    'TableOfContents',
    'PD'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 11, 7)
__author__ = 'Aurel Villyani'
__credits__ = 'CS 331'

# Symbolic Constants
DEFAULT_ENCODING = 'latin_1'
_ROOT = pathlib.Path(sys.argv[0]).parent
BIBLE_TXT = _ROOT / 'pg30.txt'
BIBLE_DB = _ROOT / 'bible.db'
SQL = {'count table': '''\
SELECT count(*) AS size
  FROM sqlite_master
 WHERE type = 'table'
   AND name = ?''',
       'create table': '''\
CREATE TABLE bible (
    book     INTEGER NOT NULL CHECK (book > 0),
    chapter     INTEGER NOT NULL CHECK (chapter > 0),
    verse     INTEGER NOT NULL CHECK (verse > 0),
    value     TEXT    NOT NULL CHECK (length(value) > 0),
    PRIMARY KEY (book, chapter, verse)
)''',
       'count bible': '''\
SELECT count(*) AS size
  FROM bible''',
       'insert bible': '''\
INSERT INTO bible (
    book,
    chapter,
    verse,
    value
) VALUES (
    ?,
    ?,
    ?,
    ?
)''',
       'select bible': '''\
SELECT value
  FROM bible
 WHERE book = ?
   AND chapter = ?
   AND verse = ?'''}


def main():
    """Parse the Bible; then build, populate, and test a SQLite database."""
    the_bible = parse_bible(BIBLE_TXT, DEFAULT_ENCODING)
    make_database(BIBLE_DB)
    populate_database(BIBLE_DB, the_bible)
    test_database(BIBLE_TXT, BIBLE_DB, DEFAULT_ENCODING)


def parse_bible(bible_path, encoding):
    """Attempt to build a data structure representing the Bible."""
    with bible_path.open('rb') as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as bible_map:
            next_line = sniff_next_line(bible_map)
            the_bible = Bible()
            read_until_locked(bible_map, next_line * 2, the_bible, encoding)
            return the_bible


def sniff_next_line(memory_map):
    """Determine the next-line character(s) used for the given file."""
    for next_line in b'\r\n', b'\r', b'\n':
        if memory_map.find(next_line) >= 0:
            return next_line
    raise EOFError('could not find any line delimiters')


def read_until_locked(bible_map, end_of_verse, the_bible, encoding):
    """Work through the memory map until the Bible is completely built."""
    start = 0
    while not the_bible.locked:
        sub = the_bible.reference.encode(encoding)
        index = bible_map.find(sub, start)
        if index >= 0:
            start = index + len(sub)
            end = bible_map.find(end_of_verse, start)
            if end < 0:
                raise EOFError('could not find the end of the verse')
            bible_map.seek(start)
            the_bible += bible_map.read(end - start).decode(encoding)
            start = end
        else:
            the_bible += the_bible.NEXT


def make_database(db_path, table_name='bible'):
    """If the path does not exist, create a database for storing the Bible."""
    if not db_path.exists():
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        if not table_exists(connection, table_name):
            with connection:
                connection.execute(SQL['create table'])
            if not table_exists(connection, table_name):
                raise RuntimeError(f'table {table_name!r} was not created')


def table_exists(database, table_name):
    """Find out if a table exists in a SQLite database."""
    with database:
        cursor = database.execute(SQL['count table'], [table_name])
        total = cursor.fetchone()['size']
    return {0: False, 1: True}[total]


def populate_database(db_path, the_bible):
    """If the Bible is not in the database, store its complete contents."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    if not has_rows(connection, the_bible):
        with connection:
            connection.executemany(SQL['insert bible'], the_bible)
            if not has_rows(connection, the_bible):
                raise RuntimeError(f'table {table_name!r} was not created')


def has_rows(database, the_bible):
    """Check if the bible table has rows and validate the number."""
    with database:
        cursor = database.execute(SQL['count bible'])
        total = cursor.fetchone()['size']
    if total > 0:
        if total != len(the_bible):
            raise ValueError('Bible database has wrong number of rows in it')
        return True
    return False


def test_database(bible_path, db_path, encoding):
    """Demonstrate the Bible database was created and built successfully."""
    print('This program will take a reference and show you a verse.')
    toc = parse_book_names(bible_path, encoding)
    (book, chapter, verse), text = get_reference_and_text(toc, db_path)
    reference = f'{toc[book]} {chapter}:{verse}'
    print(f'\n{reference}\n{"=" * len(reference)}')
    print(*textwrap.wrap(text), sep='\n')


def parse_book_names(bible_path, encoding):
    """Get the names of all the books in the Bible."""
    with bible_path.open('rb') as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as bible_map:
            next_line = sniff_next_line(bible_map)
            toc = TableOfContents('Book {:02}', PD(13, 3, 1), PD(9, 3, 40))
            # noinspection PyTypeChecker
            read_table_of_contents(bible_map, next_line, toc, encoding)
    return toc


def read_table_of_contents(bible_map, end_of_line, toc, encoding):
    """Put the book names into the table of contents dictionary."""
    start = 0
    for (key, book_a), (_, book_b) in itertools.pairwise(itertools.chain(
            ((chapter, name.encode(encoding)) for chapter, name in toc),
            [(-1, end_of_line)])):
        index = bible_map.find(book_a, start)
        if index < 0:
            raise EOFError(f'{book_a} could not be found')
        start = index + len(book_a)
        end = min(bible_map.find(book_b, start),
                  bible_map.find(end_of_line, start))
        if end < 0:
            raise EOFError('an expected value could not be found')
        bible_map.seek(start)
        toc[key] = bible_map.read(end - start).decode(encoding)
        start = end


def get_reference_and_text(toc, db_path):
    """Enter a loop forcing user to enter a valid Bible reference."""
    while True:
        reference = get_bible_reference(toc)
        try:
            text = retrieve_bible_verse(db_path, reference)
        except KeyError:
            print('ERROR: Reference was parsed but not found in database.')
        else:
            return reference, text


def get_bible_reference(toc):
    """Try to get a valid reference composed of book, chapter, and verse."""
    while True:
        print('References should be formatted as "Book Chapter:Verse".')
        try:
            text = input('Please enter a reference: ')
        except EOFError:
            print('EOF detected; exiting the program.')
            sys.exit()
        else:
            try:
                prefix, pair = text.rsplit(None, 1)
            except ValueError:
                pass
            else:
                prefix = clean(prefix).casefold()
                for book, name in enumerate(map(str.casefold, toc.names), 1):
                    if name.startswith(prefix):
                        break
                else:
                    continue
                try:
                    chapter, verse = map(int, pair.split(':'))
                except ValueError:
                    pass
                else:
                    return book, chapter, verse


def clean(text):
    """Remove any access whitespace characters from the text."""
    return ' '.join(text.split())


def retrieve_bible_verse(db_path, reference):
    """Pull the text for the Bible reference from the database if possible."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    with connection:
        row = connection.execute(SQL['select bible'], reference).fetchone()
    if row is None:
        raise KeyError(f'could not find {reference} in database')
    return row['value']


class Bible:
    """Data structure to assist with parsing the Bible"""

    NEXT = object()

    def __init__(self):
        """Initialize the Bible instance."""
        self.__book = self.__chapter = self.__verse = 1
        self.__book_list, self.__chapter_list, self.__verse_list = [], [], []
        self.__lock = False
        self.__size = 0

    def __add__(self, other):
        """Add something to this Bible instance and return a new one."""
        return NotImplemented

    def __sub__(self, other):
        """Subtract something from this Bible instance and return a new one."""
        return NotImplemented

    def __mul__(self, other):
        """Multiply something with this Bible instance and return a new one."""
        return NotImplemented

    def __truediv__(self, other):
        """Divide something with this Bible instance and return a new one."""
        return NotImplemented

    def __iadd__(self, other):
        """Add something in-place to this Bible instance."""
        if self.__lock:
            raise ArithmeticError('Bible is locked and cannot in-place add')
        if other is self.NEXT:
            self.__reference_not_found()
        elif isinstance(other, str):
            self.__add_verse_text(other)
        else:
            return NotImplemented
        return self

    def __reference_not_found(self):
        """Alter the verses, chapters, and books based on internal state."""
        if self.__verse != 1:
            self.__chapter_list.append(tuple(self.__verse_list))
            self.__verse_list.clear()
            self.__chapter += 1
            self.__verse = 1
        elif self.__chapter != 1:
            # noinspection PyUnresolvedReferences
            self.__book_list.append(tuple(self.__chapter_list))
            self.__chapter_list.clear()
            self.__book += 1
            self.__chapter = 1
        elif self.__book != 1:
            self.__lock = True
            self.__book_list = tuple(self.__book_list)
        else:
            raise EOFError('Bible is empty and parsing may have failed')

    def __add_verse_text(self, value):
        """Clean up the text and then add it to internal storage."""
        self.__verse_list.append(clean(value))
        self.__verse += 1
        self.__size += 1

    def __gt__(self, other):
        """Check if this Bible instance is greater than another one."""
        return (self.__size > other.__size
                if isinstance(other, type(self)) else
                NotImplemented)

    def __lt__(self, other):
        """Check if this Bible instance is less than another one."""
        return (self.__size < other.__size
                if isinstance(other, type(self)) else
                NotImplemented)

    def __bool__(self):
        """Determine if this Bible instance is currently not empty."""
        return self.__size > 0

    def __len__(self):
        """Provide the number of verses currently in this Bible instance."""
        return self.__size

    def __del__(self):
        """Cleanup any resources that need special attention upon deletion."""
        print('\nMatthew 24:35'
              '\n=============')
        print('Heaven and earth shall pass away, '
              'but my words shall not pass away.')

    @property
    def reference(self):
        """Give a string to search for the next verse."""
        if not self.__lock:
            return f'{self.__book:02}:{self.__chapter:03}:{self.__verse:03} '
        raise ValueError('reference is not available when Bible is locked')

    @property
    def books(self):
        """Give the books the Bible if and only if this instance is locked."""
        if self.__lock:
            return self.__book_list
        raise ValueError('books cannot be retrieved until Bible is complete')

    @property
    def locked(self):
        """Give an indicator if no more verses can be added to the Bible."""
        return self.__lock

    def __iter__(self):
        """Iterate over the Bible with book, chapter, verse, and value."""
        if not self.__lock:
            raise RuntimeError('iteration not possible on incomplete Bible')
        for book, chapter_tuple in enumerate(self.__book_list, 1):
            for chapter, verse_tuple in enumerate(chapter_tuple, 1):
                for verse, value in enumerate(verse_tuple, 1):
                    yield book, chapter, verse, value


class TableOfContents:
    """Data structure to assist with parsing the Bible's TOC"""

    STATE = enum.Enum('STATE', 'new, started, stopped, locked')

    def __init__(self, chapter_format, *pivot_descriptions):
        """Initialize the TableOfContents instance."""
        self.__chapter_format = chapter_format
        self.__pivot_descriptions = pivot_descriptions
        self.__state = self.STATE.new
        self.__chapter_names = {}

    def __bool__(self):
        """Find out if anything is currently stored in the chapter names."""
        return bool(self.__chapter_names)

    def __len__(self):
        """Return the number of items currently stored in chapter names."""
        return len(self.__chapter_names) if self.__chapter_names else 0

    def __del__(self):
        """Cleanup any resources that need special attention upon deletion."""
        print(f'Program by {__author__} for {__credits__} due {__date__}.')

    def __iter__(self):
        """Using the pivot descriptions, create the chapter names."""
        if self.__state is not self.STATE.new:
            raise RuntimeError('iterator may only be run once')
        self.__state = self.STATE.started
        for description in self.__pivot_descriptions:
            if not isinstance(description, PD):
                raise TypeError('generator can only work with PD instances')
            for row in range(description.rows):
                head = row + description.start
                for column in range(description.columns):
                    chapter = head + column * description.rows
                    yield chapter, self.__chapter_format.format(chapter)
        self.__state = self.STATE.stopped

    def __setitem__(self, key, value):
        """Set the name for the chapter using value and key respectively."""
        if self.__state not in {self.STATE.started, self.STATE.stopped}:
            raise RuntimeError('chapter name cannot currently be set')
        self.__chapter_names[key] = clean(value)
        if self.__state is self.STATE.stopped:
            self.__cleanup_chapter_names()

    def __cleanup_chapter_names(self):
        """Validate the chapter names and optimize their storage."""
        self.__state = self.STATE.locked
        required_chapters = range(1, len(self.__chapter_names) + 1)
        if set(self.__chapter_names) != set(required_chapters):
            self.__chapter_names = None
            raise ValueError('chapter names were incorrectly constructed')
        self.__chapter_names = tuple(map(
            self.__chapter_names.__getitem__, required_chapters))

    def __getitem__(self, key):
        """Given a chapter number, return its name back to the caller."""
        self.__validate_end_state()
        return self.__chapter_names[key - 1]

    def __validate_end_state(self):
        """Verify that the chapter names can be referenced."""
        if self.__state is not self.STATE.locked:
            raise RuntimeError('instance must be locked first')
        if self.__chapter_names is None:
            raise ValueError('chapter names were incorrectly constructed')

    @property
    def current_state(self):
        """Give a value indicating how the iterator is operating."""
        return self.__state

    @property
    def names(self):
        """Give the tuple of chapter names if it is available."""
        self.__validate_end_state()
        return self.__chapter_names


# PD is short for Pivot Description.
PD = collections.namedtuple('PD', 'rows, columns, start')

if __name__ == '__main__':
    main()
