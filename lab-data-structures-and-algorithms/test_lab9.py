#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lab set 9 - Data structures and algorithms.

Installation: Pensacola Christian College

I pledge all of the lines in this Python program are my own original
work and that none of the lines in this Python program have been copied
from anyone else unless I was specifically authorized to do so by
my CS 331 instructor.

    Signed: _______________________Stephen_Paul_Chappell_______________________
                                        (signature)

In this lab, write one Python program file. In this program file, you will be
writing code to satisfy the tests provided in a separate module. There are 113
individual checks that need to be satisfied for the module you will be creating
this week. After you have verified the program works correctly, upload the
Python program to this assignment in Canvas."""

import datetime
import inspect
import operator
import random
import test.support
import unittest

try:
    from itertools import pairwise
except ImportError:
    from itertools import tee as _tee


    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = _tee(iterable)
        next(b, None)
        return zip(a, b)

import modules

# Public Names
__all__ = (
    'TestTreeFunctions',
    'TestBinaryTreeNode',
    'TestHeapQueue',
    'TestAdvHeapQueue',
    'TestRevHeapQueue'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2021, 11, 19)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'CS 331'


class TestTreeFunctions(unittest.TestCase):
    """Test all the tree-related functions in modules."""

    def test_create_tree_doc(self):
        """Build an example tree a total of levels deep."""
        self.assertEqual(
            'Build an example tree a total of levels deep.',
            inspect.getdoc(modules.create_tree))

    def test_create_node_doc(self):
        """Recursively build nodes based on the current level"""
        self.assertEqual(
            'Recursively build nodes based on the current level.',
            inspect.getdoc(modules._create_node))

    def test_display_tree_doc(self):
        """Print a representation of the tree to standard output."""
        self.assertEqual(
            'Print a representation of the tree to standard output.',
            inspect.getdoc(modules.display_tree))

    def test_display_node_doc(self):
        """Print a single node at a time using recursion."""
        self.assertEqual(
            'Print a single node at a time using recursion.',
            inspect.getdoc(modules._display_node))

    def test_invert_tree_doc(self):
        """Swap all of the left and right nodes with each other."""
        self.assertEqual(
            'Swap all of the left and right nodes with each other.',
            inspect.getdoc(modules.invert_tree))

    def test_invert_node_doc(self):
        """Recursively swap the left and right leaves of a node."""
        self.assertEqual(
            'Recursively swap the left and right leaves of a node.',
            inspect.getdoc(modules._invert_node))

    def test_tree_to_list_doc(self):
        """Take all values from the tree and place them in a list."""
        self.assertEqual(
            'Take all values from the tree and place them in a list.',
            inspect.getdoc(modules.tree_to_list))

    def test_node_to_list_doc(self):
        """Use recursion to add the values of each node to a list."""
        self.assertEqual(
            'Use recursion to add the values of each node to a list.',
            inspect.getdoc(modules._node_to_list))

    def test_iter_tree_doc(self):
        """After checking the root's type, iterate over all item in a tree."""
        self.assertEqual(
            "After checking the root's type, iterate over all item in a tree.",
            inspect.getdoc(modules.iter_tree))

    def test_iter_node_doc(self):
        """Recursively iterate over each node's item and yield it back."""
        self.assertEqual(
            "Recursively iterate over each node's item and yield it back.",
            inspect.getdoc(modules._iter_node))

    def test_breadth_first_search_tree_doc(self):
        """Attempt to find the shortest path to an item found in a tree."""
        self.assertEqual(
            'Attempt to find the shortest path to an item found in a tree.',
            inspect.getdoc(modules.breadth_first_search_tree))

    def test_get_item_from_tree_doc(self):
        """Retrieve the item that corresponds with the given path."""
        self.assertEqual(
            'Retrieve the item that corresponds with the given path.',
            inspect.getdoc(modules.get_item_from_tree))

    def test_get_item_from_node_doc(self):
        """Get an item specified by path using a recursive algorithm."""
        self.assertEqual(
            'Get an item specified by path using a recursive algorithm.',
            inspect.getdoc(modules._get_item_from_node))

    def test_create_tree_zero(self):
        """Test what happens when an empty tree is created."""
        tree = modules.create_tree(0)
        self.assertIsNone(tree)

    def test_create_tree_one(self):
        """Test the creation of a tree with just a single node."""
        tree = modules.create_tree(1)
        self.assertIsNotNone(tree)
        self.assertEqual(1, tree.item)
        self.assertIsNone(tree.left)
        self.assertIsNone(tree.right)

    def test_display_tree_root_type(self):
        """Test the type checking in the display_tree function."""
        with self.assertRaises(TypeError):
            modules.display_tree(None)

    def test_display_tree_root_error(self):
        """Test the error message for the display_tree function."""
        with self.assertRaises(TypeError) as cm:
            modules.display_tree(None)
        self.assertEqual(
            ('root of tree must be of type BinaryTreeNode',),
            cm.exception.args)

    def test_display_tree_left_right_type(self):
        """Test the type checking for the left and right arguments."""
        with self.assertRaises(TypeError):
            modules.display_tree(modules.BinaryTreeNode(None),
                                     left=None)
        with self.assertRaises(TypeError):
            modules.display_tree(modules.BinaryTreeNode(None),
                                     right=None)

    def test_display_tree_left_right_error(self):
        """Test the error message for the left and right arguments."""
        with self.assertRaises(ValueError) as cm:
            modules.display_tree(modules.BinaryTreeNode(None),
                                     left='left')
        self.assertEqual(
            ('left and right must be a single character',),
            cm.exception.args)
        with self.assertRaises(ValueError) as cm:
            modules.display_tree(modules.BinaryTreeNode(None),
                                     right='right')
        self.assertEqual(
            ('left and right must be a single character',),
            cm.exception.args)

    def test_display_tree_normal(self):
        """Test that display_tree prints to stdout as expected."""
        tree = modules.create_tree(4)
        with test.support.captured_stdout() as stdout:
            modules.display_tree(tree)
        self.assertEqual('''\
ROOT: 1
L: 2
LL: 3
LLL: 4
LLR: 5
LR: 6
LRL: 7
LRR: 8
R: 9
RL: 10
RLL: 11
RLR: 12
RR: 13
RRL: 14
RRR: 15
''', stdout.getvalue())

    def test_tree_to_list_root_type(self):
        """Test the type checking in the tree_to_list function."""
        with self.assertRaises(TypeError):
            modules.tree_to_list(None)

    def test_tree_to_list_root_error(self):
        """Test the error message for the tree_to_list function."""
        with self.assertRaises(TypeError) as cm:
            modules.tree_to_list(None)
        self.assertEqual(
            ('root of tree must be of type BinaryTreeNode',),
            cm.exception.args)

    def test_tree_to_list(self):
        """Test that tree_to_list is able to correctly collect the items."""
        tree = modules.create_tree(4)
        items = modules.tree_to_list(tree)
        self.assertSequenceEqual(items, range(1, 1 << 4))

    def test_invert_tree_root_type(self):
        """Test the type checking in the invert_tree function."""
        with self.assertRaises(TypeError):
            modules.invert_tree(None)

    def test_invert_tree_root_error(self):
        """Test the error message for the invert_tree function."""
        with self.assertRaises(TypeError) as cm:
            modules.invert_tree(None)
        self.assertEqual(
            ('root of tree must be of type BinaryTreeNode',),
            cm.exception.args)

    def test_invert_tree(self):
        """Test that invert_tree will swap the left and right leaves."""
        tree = modules.create_tree(2)
        modules.invert_tree(tree)
        self.assertIsNotNone(tree)
        self.assertEqual(1, tree.item)
        self.assertIsNotNone(tree.left)
        self.assertIsNotNone(tree.right)
        self.assertEqual(3, tree.left.item)
        self.assertEqual(2, tree.right.item)
        self.assertIsNone(tree.left.left)
        self.assertIsNone(tree.left.right)
        self.assertIsNone(tree.right.left)
        self.assertIsNone(tree.right.right)

    def test_display_tree_custom(self):
        """Test create_tree with custom left and right signals."""
        tree = modules.create_tree(4)
        modules.invert_tree(tree)
        with test.support.captured_stdout() as stdout:
            modules.display_tree(tree, '<', '>')
        self.assertEqual('''\
ROOT: 1
<: 9
<<: 13
<<<: 15
<<>: 14
<>: 10
<><: 12
<>>: 11
>: 2
><: 6
><<: 8
><>: 7
>>: 3
>><: 5
>>>: 4
''', stdout.getvalue())

    def test_iter_tree_root_type(self):
        """Test the type checking in the iter_tree function."""
        with self.assertRaises(TypeError):
            next(modules.iter_tree(None))

    def test_iter_tree_root_error(self):
        """Test the error message for the iter_tree function."""
        with self.assertRaises(TypeError) as cm:
            next(modules.iter_tree(None))
        self.assertEqual(
            ('root of tree must be of type BinaryTreeNode',),
            cm.exception.args)

    def test_iter_tree(self):
        """Test iter_tree in the context of printing out values."""
        tree = modules.create_tree(4)
        modules.invert_tree(tree)
        with test.support.captured_stdout() as stdout:
            print('ITEMS:', *modules.iter_tree(tree), sep=' ')
        self.assertEqual(
            'ITEMS: 1 9 13 15 14 10 12 11 2 6 8 7 3 5 4\n',
            stdout.getvalue())

    def test_breadth_first_search_tree_root_type(self):
        """Test the type checking in the BFS_tree function."""
        with self.assertRaises(TypeError):
            modules.breadth_first_search_tree(None, None)

    def test_breadth_first_search_tree_root_error(self):
        """Test the error message for the BFS_tree function."""
        with self.assertRaises(TypeError) as cm:
            modules.breadth_first_search_tree(None, None)
        self.assertEqual(
            ('root of tree must be of type BinaryTreeNode',),
            cm.exception.args)

    def test_breadth_first_search_tree(self):
        """Test all possibilities for trying to find tree items."""
        tree = modules.create_tree(2)
        for item, answer in (1, 'ROOT'), (2, '/'), (3, '\\'), (4, None):
            path = modules.breadth_first_search_tree(tree, item)
            self.assertEqual(answer, path)

    def test_get_item_from_tree_root_type(self):
        """Test the type checking in the get_item_from_tree function."""
        with self.assertRaises(TypeError):
            modules.get_item_from_tree(None, None)

    def test_get_item_from_tree_root_error(self):
        """Test the error message for the get_item_from_tree function."""
        with self.assertRaises(TypeError) as cm:
            modules.get_item_from_tree(None, None)
        self.assertEqual(
            ('root of tree must be of type BinaryTreeNode',),
            cm.exception.args)

    def test_get_item_from_tree_path_type(self):
        """Test that the path argument's type is validated."""
        with self.assertRaises(TypeError):
            modules.get_item_from_tree(modules.BinaryTreeNode(None),
                                           None)

    def test_get_item_from_tree_path_error(self):
        """Test that the error message for the path argument is sensible."""
        with self.assertRaises(TypeError) as cm:
            modules.get_item_from_tree(modules.BinaryTreeNode(None),
                                           None)
        self.assertEqual(
            ('path must be of type str',),
            cm.exception.args)

    def test_get_item_from_tree_path_value(self):
        """Test what happens when an invalid path is provided."""
        with self.assertRaises(ValueError) as cm:
            modules.get_item_from_tree(modules.BinaryTreeNode(None),
                                           ' ')
        self.assertEqual(
            ("direction ' ' is not valid",),
            cm.exception.args)

    def test_get_item_from_tree(self):
        """Test that get_item_from_tree can follow paths correctly."""
        tree = modules.create_tree(4)
        modules.invert_tree(tree)
        for item in modules.tree_to_list(tree):
            path = modules.breadth_first_search_tree(tree, item)
            self.assertEqual(item, modules.get_item_from_tree(tree, path))


class TestBinaryTreeNode(unittest.TestCase):
    """Test the class used to organize binary trees in the lab 9 module."""

    def test_class_doc(self):
        """Test that the documentation for the class is correct."""
        self.assertEqual(
            'A node that can store an item and link to left and right leaves.',
            inspect.getdoc(modules.BinaryTreeNode))

    def test_init_doc(self):
        """Test that the documentation for the initializer is correct."""
        self.assertEqual(
            'Initialize the BinaryTreeNode instance.',
            inspect.getdoc(modules.BinaryTreeNode.__init__))

    def test_init(self):
        """Test that the class constructor creates instances correctly."""
        instance = modules.BinaryTreeNode(None)
        self.assertIsInstance(instance, modules.BinaryTreeNode)

    def test_item_doc(self):
        """Test that the item documentation is correct."""
        self.assertEqual(
            'Property for reading and writing the item value.',
            inspect.getdoc(modules.BinaryTreeNode.item))

    def test_item(self):
        """Test that the item property appears to work correctly."""
        argument = object()
        instance = modules.BinaryTreeNode(argument)
        self.assertIs(instance.item, argument)
        new_argument = object()
        instance.item = new_argument
        self.assertIs(instance.item, new_argument)

    def test_left_doc(self):
        """Test that the left documentation is correct."""
        self.assertEqual(
            'Property for reading and writing the left value.',
            inspect.getdoc(modules.BinaryTreeNode.left))

    def test_left(self):
        """Test that the item property appears to work correctly."""
        instance = modules.BinaryTreeNode(None)
        self.assertIsNone(instance.left)
        instance.left = instance
        self.assertIs(instance.left, instance)

    def test_left_type_error(self):
        """Test the left's type checking."""
        with self.assertRaises(TypeError):
            modules.BinaryTreeNode(None, left=[])

    def test_left_error_message(self):
        """Test the error message for the left property."""
        with self.assertRaises(TypeError) as cm:
            modules.BinaryTreeNode(None, left=[])
        self.assertEqual(
            ("left must be of type "
             "(<class 'modules.BinaryTreeNode'>, "
             "<class 'NoneType'>)",),
            cm.exception.args)

    def test_right_doc(self):
        """Test that the right documentation is correct."""
        self.assertEqual(
            'Property for reading and writing the right value.',
            inspect.getdoc(modules.BinaryTreeNode.right))

    def test_right(self):
        """Test that the item property appears to work correctly."""
        instance = modules.BinaryTreeNode(None)
        self.assertIsNone(instance.right)
        instance.right = instance
        self.assertIs(instance.right, instance)

    def test_right_type_error(self):
        """Test the right's type checking."""
        with self.assertRaises(TypeError):
            modules.BinaryTreeNode(None, right=[])

    def test_right_error_message(self):
        """Test the error message for the right property."""
        with self.assertRaises(TypeError) as cm:
            modules.BinaryTreeNode(None, right=[])
        self.assertEqual(
            ("right must be of type "
             "(<class 'modules.BinaryTreeNode'>, "
             "<class 'NoneType'>)",),
            cm.exception.args)


class TestHeapQueue(unittest.TestCase):
    """Test the HeapQueue class located in modules."""

    CLASS = modules.HeapQueue
    CLASS_DOC = 'Priority Queue implementation based off the heapq module.'
    INIT_DOC = 'Initialize the HeapQueue instance.'
    PUSH_DOC = 'Add an item to the heap.'
    POP_DOC = 'Get an item from the heap and remove it.'
    EXAMPLE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    REVERSE = False

    def test_class_doc(self):
        """Test that the class's documentation is correct."""
        self.assertEqual(self.CLASS_DOC, inspect.getdoc(self.CLASS))

    def test_init_doc(self):
        """Test that the class initializer's documentation is correct."""
        self.assertEqual(self.INIT_DOC, inspect.getdoc(self.CLASS.__init__))

    def test_init_none(self):
        """Test creating an instance without arguments."""
        instance = self.CLASS()
        self.assertIsInstance(instance, self.CLASS)

    def test_init_list(self):
        """Test creating an instance with arguments."""
        instance = self.CLASS(self.EXAMPLE.copy())
        self.assertIsInstance(instance, self.CLASS)

    def test_init_type_error(self):
        """Test creating an instance with a TypeError exception."""
        with self.assertRaises(TypeError):
            self.CLASS(set(self.EXAMPLE))

    def test_init_error_message(self):
        """Test creating an instance with an error message."""
        with self.assertRaises(TypeError) as cm:
            self.CLASS(set(self.EXAMPLE))
        self.assertEqual(
            ('heap must be a list',),
            cm.exception.args)

    def test_len_doc(self):
        """Test that the length method's documentation is correct."""
        self.assertEqual(
            'Calculate the size of heap.',
            inspect.getdoc(self.CLASS.__len__))

    def test_len_zero(self):
        """Test creating an empty instance."""
        instance = self.CLASS()
        self.assertEqual(0, len(instance))

    def test_len_non_zero(self):
        """Test creating an instance with a list."""
        instance = self.CLASS(self.EXAMPLE.copy())
        self.assertEqual(len(self.EXAMPLE), len(instance))

    def test_push_doc(self):
        """Test that the push method's documentation is correct."""
        self.assertEqual(self.PUSH_DOC, inspect.getdoc(self.CLASS.push))

    def test_push(self):
        """Test pushing an item on an instance."""
        instance = self.CLASS()
        self.assertEqual(0, len(instance))
        instance.push(0)
        self.assertEqual(1, len(instance))

    def test_pop_doc(self):
        """Test that the pop method's documentation is correct."""
        self.assertEqual(self.POP_DOC, inspect.getdoc(self.CLASS.pop))

    def test_pop_non_zero(self):
        """Test popping an item off a non-empty instance."""
        instance = self.CLASS([0])
        self.assertEqual(1, len(instance))
        self.assertEqual(0, instance.pop())
        self.assertEqual(0, len(instance))

    def test_pop_zero(self):
        """Test popping an item off an empty instance."""
        instance = self.CLASS()
        with self.assertRaises(IndexError):
            instance.pop()
        self.assertEqual(0, len(instance))

    def test_priority_queue(self):
        """Test that items are popped off queue in correct order."""
        cmp = operator.lt if self.REVERSE else operator.gt
        for _ in range(30):
            while True:
                numbers = [random.randint(-1000, +1000) for _ in range(100)]
                if any(cmp(a, b) for a, b in pairwise(numbers)):
                    break
            instance = self.CLASS(numbers.copy())
            self.assertEqual(len(numbers), len(instance))
            numbers.sort(reverse=self.REVERSE)
            for number in numbers:
                self.assertEqual(number, instance.pop())
            self.assertEqual(0, len(instance))


class TestAdvHeapQueue(TestHeapQueue):
    """Test the AdvHeapQueue class located in modules."""

    CLASS = modules.AdvHeapQueue
    CLASS_DOC = "Advanced Priority Queue that extends HeapQueue's " \
                "functionality."

    def test_bool_doc(self):
        """Determine if the heap is empty or non-empty."""
        self.assertEqual(
            'Determine if the heap is empty or non-empty.',
            inspect.getdoc(self.CLASS.__bool__))

    def test_bool_false(self):
        """Test that an empty instance is considered False."""
        instance = self.CLASS()
        self.assertFalse(instance)

    def test_bool_true(self):
        """Test that a non-empty instance is considered True."""
        instance = self.CLASS(self.EXAMPLE.copy())
        self.assertTrue(instance)

    def test_extend_doc(self):
        """Test that the extend method's documentation is correct."""
        self.assertEqual(
            'Push each item in the iterable to the heap.',
            inspect.getdoc(self.CLASS.extend))

    def test_extend(self):
        """Test the extend method to push items on the instance."""
        instance = self.CLASS()
        self.assertFalse(instance)
        instance.extend(self.EXAMPLE)
        self.assertTrue(instance)

    def test_iter_doc(self):
        """Test that the iterator method's documentation is correct."""
        self.assertEqual(
            'Pop all items from the heap while removing them.',
            inspect.getdoc(self.CLASS.__iter__))

    def test_iter_non_zero(self):
        """Test iteration for popping all items off the instance."""
        instance = self.CLASS(self.EXAMPLE.copy())
        example = reversed(self.EXAMPLE) if self.REVERSE else self.EXAMPLE
        for value, item in zip(example, instance):
            self.assertEqual(value, item)
        self.assertFalse(instance)

    def test_iter_zero(self):
        """Test iteration on an empty instance."""
        instance = self.CLASS()
        counter = 0
        for _ in instance:
            counter += 1
        self.assertEqual(0, counter)


class TestRevHeapQueue(TestAdvHeapQueue):
    """Test the RevHeapQueue class located in modules."""

    CLASS = modules.RevHeapQueue
    CLASS_DOC = 'Reversed Priority Queue that pops the largest item first.'
    INIT_DOC = 'Initialize the RevHeapQueue instance.'
    PUSH_DOC = 'Wrap the item before pushing into onto the heap.'
    POP_DOC = 'Unwrap each item before returning it to the caller.'
    REVERSE = True


if __name__ == '__main__':
    unittest.main()
