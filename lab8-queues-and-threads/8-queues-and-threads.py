#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# noinspection GrazieInspection

import collections
import csv
import datetime
import itertools
import pathlib
import queue
import random
import statistics
import sys
import textwrap
import threading

# Public Names
__all__ = (
    'DATA_FILE',
    'HEADERS',
    'main',
    'ReadCsvFile',
    'GenerateNumericResponses',
    'GenerateNumericSummaries',
    'GenerateTextualSummaries',
    'PrintSpooler'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 11, 14)
__author__ = 'Aurel Villyani'
__credits__ = 'CS 331'

# Symbolic Constants
_ROOT = pathlib.Path(sys.argv[0]).parent
DATA_FILE = _ROOT / 'Student Perceptions of Instruction ' \
                    'Survey Student Analysis Report.csv'
HEADERS = tuple('''\
Organizing the course:
Explaining course requirements, grading criteria, and expectations:
Communicating ideas and/or information:
Showing respect and concern for students:
Stimulating interest in the course:
Creating an environment that helps students learn:
Giving useful feedback on course objectives:
Helping students achieve course objectives:
Use of Canvas to support my learning in this course was:
Use of Canvas to communicate important course information was:
Overall, the effectiveness of the instructor in the course was:
What suggestions do you have for improving how the instructor taught the \
course?
What did you like best about how the instructor taught the course?
What did you like best about the course?
What suggestions do you have for improving the course?'''.splitlines())


def main():
    """Read a data file, process its records, and display the needed output."""
    nri_queue = queue.SimpleQueue()
    nsi_queue = queue.SimpleQueue()
    tsi_queue = queue.SimpleQueue()
    reader = ReadCsvFile(DATA_FILE, HEADERS, (nri_queue, nsi_queue, tsi_queue))
    nro_queue = queue.SimpleQueue()
    nso_queue = queue.SimpleQueue()
    tso_queue = queue.SimpleQueue()
    nr_generator = GenerateNumericResponses(HEADERS, nri_queue, nro_queue)
    ns_generator = GenerateNumericResponses(HEADERS, nsi_queue, nso_queue)
    ts_generator = GenerateNumericResponses(HEADERS, tsi_queue, tso_queue)
    printer = PrintSpooler((nro_queue, nso_queue, tso_queue))
    for thread in reader, nr_generator, ns_generator, ts_generator, printer:
        thread.start()


class _NamedHolyThread(threading.Thread):
    """A base class that names the thread and sets daemon to False."""

    COUNTER = collections.defaultdict(lambda: itertools.count(1).__next__)

    def __init__(self):
        """Initialize the _NamedHolyThread instance."""
        name = type(self).__name__
        super().__init__(name=f'{name}-{self.COUNTER[name]()}', daemon=False)


class ReadCsvFile(_NamedHolyThread):
    """A class that can read CSV files and send records to multiple queues."""

    def __init__(self, file_path, headers, output_queues):
        """Initialize the ReadCsvFile instance."""
        super().__init__()
        self.__file_path = file_path
        self.__headers = headers
        self.__output_queues = output_queues

    def run(self):
        """Generate records from the CSV file and send them to the queues."""
        try:
            with self.__file_path.open(newline='') as source:
                for row in csv.DictReader(source):
                    record = self.__create_record(row)
                    for destination in self.__output_queues:
                        destination.put(record)
        finally:
            for destination in self.__output_queues:
                destination.put(_DataProcessor.END_OF_DATA)

    def __create_record(self, row):
        """Clean up a row so that it can be used in the rest of the program."""
        record = {}
        for header in self.__headers:
            for key in row:
                if key.endswith(header):
                    break
            else:
                raise KeyError(f'{header!r} not found')
            value = row[key]
            try:
                value = int(value)
                assert header.endswith(_DataProcessor.NUMERIC_SUFFIX), \
                    'textual data confused for numeric data'
            except ValueError:
                value = ' '.join(value.split())
                assert header.endswith(_DataProcessor.TEXTUAL_SUFFIX), \
                    'numeric data confused for textual data'
            record[header] = value
        return record


# noinspection GrazieInspection
class _DataProcessor(_NamedHolyThread):
    """A base class that assists with processing records from CSV files."""

    NUMERIC_SUFFIX = ':'
    TEXTUAL_SUFFIX = '?'
    END_OF_DATA = object()
    ITERATOR_TIMEOUT = 0.1
    SECTION_HEADER = None  # Override in all child classes.
    DIVIDER_LENGTH = None  # Override in all child classes.

    def __init__(self, headers, input_queue, output_queue):
        """Initialize the _DataProcessor instance."""
        super().__init__()
        self.__headers = headers
        self.__input_queue = input_queue
        self.__output_queue = output_queue
        self.__record_cache = None

    def run(self):
        """Start the thread's activity and ensure proper cleanup at the end."""
        try:
            self.process_data()
        finally:
            self.signal_end_of_data()

    def process_data(self):
        """Handle incoming records. This method should be overridden."""
        raise NotImplementedError()

    def signal_end_of_data(self):
        """Let the queue consumer know that processing has been completed."""
        self.__output_queue.put(self.END_OF_DATA)

    def __iter__(self):
        """Allow queue records to be easily retrieved."""
        while True:
            item = self.get_item(self.__input_queue)
            # If the item is self.END_OF_DATA, then break out of the loop.
            if item is self.END_OF_DATA:
                break
            yield item

    @classmethod
    def get_item(cls, queue_obj):
        """Generate an error when the queue is not being used properly."""
        try:
            return queue_obj.get(True, cls.ITERATOR_TIMEOUT)
        except queue.Empty:
            raise RuntimeError('END_OF_DATA must be received when done')

    def show_section_header(self):
        """Send a section header to the print queue for later processing."""
        if self.SECTION_HEADER is None:
            raise ValueError('SECTION_HEADER should be overridden')
        non_root = '#' * (len(self.SECTION_HEADER) + 6)
        self.print(f'{non_root}\n#  {self.SECTION_HEADER}  #\n{non_root}\n')

    def print(self, *args, **kwargs):
        """Send the arguments and keyword arguments to the print queue."""
        self.__output_queue.put((args, kwargs))

    def get_numeric_headers(self):
        """Assist with getting the names for the numeric columns."""
        return self.get_items_ending_with(self.__headers, self.NUMERIC_SUFFIX)

    @staticmethod
    def get_items_ending_with(iterable, suffix):
        """Yield back those items that end with the provided suffix."""
        return (item for item in iterable if item.endswith(suffix))

    @staticmethod
    def calculate_mean_and_cv(data):
        """Efficiently calculate the mean and coefficient of variation."""
        mean = statistics.fmean(data)
        sample_standard_deviation = statistics.stdev(data, mean)
        cv = sample_standard_deviation / mean
        return mean, cv

    def show_record_break(self):
        """Send a record break to the print queue for later processing."""
        if self.DIVIDER_LENGTH is None:
            raise ValueError('DIVIDER_LENGTH should be overridden')
        self.print(f'{"=" * self.DIVIDER_LENGTH}\n')

    def get_column(self, name):
        """Assist with getting all of the values from a particular column."""
        return [record[name] for record in self.__records]

    @property
    def __records(self):
        """Handle the record cache to efficiently get and store records."""
        if self.__record_cache is None:
            self.__record_cache = tuple(self)
        return self.__record_cache

    def show_record_title(self, name):
        """Send a record title to the print queue for later processing."""
        self.print(f'{name}\n{"-" * len(name)}')

    def get_textual_headers(self):
        """Assist with getting the names for the textual columns."""
        return self.get_items_ending_with(self.__headers, self.TEXTUAL_SUFFIX)


class GenerateNumericResponses(_DataProcessor):
    """A class that creates a report for each individual record it receives."""
    SECTION_HEADER = 'Numeric Response'
    DIVIDER_LENGTH = 69

    def process_data(self):
        """Generate formatted print data for each record from the CSV file."""
        self.show_section_header()
        for record in self:
            values = []
            for key in self.get_numeric_headers():
                values.append(record[key])
                self.print(f'{key:68}{values[-1]}')
            mean, cv = self.calculate_mean_and_cv(values)
            self.print(f'{"Arithmetic Mean:":64}{mean:.3f}')
            self.print(f'{"Coefficient of Variation:":64}{cv:.3f}')
            self.show_record_break()


class GenerateNumericSummaries(_DataProcessor):
    """A class that attempts to summarize all numeric column data."""
    SECTION_HEADER = 'Numeric Summaries'
    DIVIDER_LENGTH = 31

    def process_data(self):
        """Create a summary for each numeric column from the CSV file."""
        self.show_section_header()
        for key in self.get_numeric_headers():
            column = self.get_column(key)
            mean, cv = self.calculate_mean_and_cv(column)
            self.show_record_title(key)
            self.print(f'{"Arithmetic Mean:":26}{mean:.3f}')
            self.print(f'{"Coefficient of Variation:":26}{cv:.3f}')
            self.show_record_break()


class GenerateTextualSummaries(_DataProcessor):
    """A class that creates anonymous (scrambled) summaries of text columns."""

    SECTION_HEADER = 'Textual Summaries'
    WRAP_WIDTH = 72
    DIVIDER_LENGTH = WRAP_WIDTH + 7

    def process_data(self):
        """Create a summary for each textual column from the CSV file."""
        self.show_section_header()
        for key in self.get_textual_headers():
            column = self.get_column(key)
            random.Random(key).shuffle(column)  # Make the values anonymous.
            self.show_record_title(key)
            self.__show_enumerated_answers(column)
            self.show_record_break()

    def __show_enumerated_answers(self, column):
        """Send the comments to the print queue in an easy-to-read format."""
        for counter, text in enumerate(column, 1):
            lines = textwrap.wrap(text, self.WRAP_WIDTH)
            for after_first, line in enumerate(lines):
                if not after_first:
                    self.print(f'  {counter:3}. {line}')
                else:
                    self.print(f'{" " * 7}{line}')


class PrintSpooler(_NamedHolyThread):
    """A class that takes predefined print queues and handles them in order."""

    def __init__(self, print_queues, **overrides):
        """Initialize the PrintSpooler instance."""
        super().__init__()
        self.__print_queues = print_queues
        self.__overrides = overrides

    def run(self):
        """Take all print instructions and display them with the overrides."""
        for print_queue in self.__print_queues:
            while True:
                item = _DataProcessor.get_item(print_queue)
                if item is _DataProcessor.END_OF_DATA:
                    break
                args, kwargs = item
                print(*args, **kwargs | self.__overrides)


if __name__ == '__main__':
    main()
