#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lab set 9 - Data structures and algorithms.

Installation: Pensacola Christian College

I pledge all of the lines in this Python program are my own original
work and that none of the lines in this Python program have been copied
from anyone else unless I was specifically authorized to do so by
my CS 331 instructor.

    Signed: __________________________Aurel_Villyani___________________________
                                        (signature)

In this lab, write one Python program file. In this program file, you will be
writing code to satisfy the tests provided in a separate module. There are 113
individual checks that need to be satisfied for the module you will be creating
this week. After you have verified the program works correctly, upload the
Python program to this assignment in Canvas."""

import collections
import datetime
import heapq

# Public Names
__all__ = (
    'create_tree',
    'display_tree',
    'invert_tree',
    'tree_to_list',
    'iter_tree',
    'breadth_first_search_tree',
    'get_item_from_tree',
    'BinaryTreeNode',
    'NODE_TYPES',
    'HeapQueue',
    'AdvHeapQueue',
    'RevHeapQueue'
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2022, 11, 21)
__author__ = 'Aurel Villyani'
__credits__ = 'CS 331'

# Symbolic Constants
LEFT_NODE = '/'
RIGHT_NODE = '\\'


def create_tree(levels):
    """Build an example tree a total of levels deep."""
    source = iter(range(1, 1 << levels))
    root = _create_node(source, levels)
    try:
        next(source)
    except StopIteration:
        return root
    else:
        raise RuntimeError('source was not exhausted when building tree')


def _create_node(iterable, level):
    """Recursively build nodes based on the current level."""
    if level > 0:
        node = BinaryTreeNode(next(iterable))
        next_level = level - 1
        node.left = _create_node(iterable, next_level)
        node.right = _create_node(iterable, next_level)
        return node


def display_tree(root, left='L', right='R'):
    """Print a representation of the tree to standard output."""
    if not isinstance(root, BinaryTreeNode):
        raise TypeError('root of tree must be of type BinaryTreeNode')
    for direction in left, right:
        if not isinstance(direction, str):
            raise TypeError('left and right must be of type str')
        if len(direction) != 1:
            raise ValueError('left and right must be a single character')
    _display_node(root, '', left, right)


def _display_node(node, path, left, right):
    """Print a single node at a time using recursion."""
    if node is not None:
        print(f'{path if path else "ROOT"!s}: {node.item!r}')
        _display_node(node.left, f'{path!s}{left!s}', left, right)
        _display_node(node.right, f'{path!s}{right!s}', left, right)


def invert_tree(root):
    """Swap all of the left and right nodes with each other."""
    if not isinstance(root, BinaryTreeNode):
        raise TypeError('root of tree must be of type BinaryTreeNode')
    _invert_node(root)


def _invert_node(node):
    """ Recursively swap the left and right leaves of a node."""
    if node is not None:
        # Swap the values of the left and right properties.
        node.left, node.right = node.right, node.left
        _invert_node(node.left)
        _invert_node(node.right)


def tree_to_list(root):
    """Take all values from the tree and place them in a list."""
    if not isinstance(root, BinaryTreeNode):
        raise TypeError('root of tree must be of type BinaryTreeNode')
    # Create a list called items.
    items = []
    _node_to_list(root, items)
    return items


def _node_to_list(node, items):
    """Use recursion to add the values of each node to a list."""
    if node is not None:
        items.append(node.item)
        _node_to_list(node.left, items)
        _node_to_list(node.right, items)


def iter_tree(root):
    """After checking the root's type, iterate over all item in a tree."""
    if not isinstance(root, BinaryTreeNode):
        raise TypeError('root of tree must be of type BinaryTreeNode')
    yield from _iter_node(root)


def _iter_node(node):
    """Recursively iterate over each node's item and yield it back."""
    if node is not None:
        yield node.item
        yield from _iter_node(node.left)
        yield from _iter_node(node.right)


def breadth_first_search_tree(root, item):
    """Attempt to find the shortest path to an item found in a tree."""
    if not isinstance(root, BinaryTreeNode):
        raise TypeError('root of tree must be of type BinaryTreeNode')
    nodes = collections.deque([(root, '')])
    while nodes:
        node, path = nodes.popleft()
        if node is not None:
            if node.item == item:
                return path if path else 'ROOT'
            nodes.append((node.left, path + LEFT_NODE))
            nodes.append((node.right, path + RIGHT_NODE))


def get_item_from_tree(root, path):
    """Retrieve the item that corresponds with the given path."""
    if not isinstance(root, BinaryTreeNode):
        raise TypeError('root of tree must be of type BinaryTreeNode')
    if not isinstance(path, str):
        raise TypeError('path must be of type str')
    if path == 'ROOT':
        return root.item
    return _get_item_from_node(root, path)


def _get_item_from_node(node, path):
    """Get an item specified by path using a recursive algorithm."""
    if not path:
        return node.item
    direction, *path = path
    if direction == '/':
        return _get_item_from_node(node.left, path)
    if direction == '\\':
        return _get_item_from_node(node.right, path)
    raise ValueError(f'direction {direction!r} is not valid')


class BinaryTreeNode:
    """A node that can store an item and link to left and right leaves."""

    def __init__(self, item, left=None, right=None):
        """Initialize the BinaryTreeNode instance."""
        self.item = item
        self.left = left
        self.right = right

    @property
    def item(self):
        """Property for reading and writing the item value."""
        return self.__item

    @item.setter
    def item(self, value):
        self.__item = value

    @property
    def left(self):
        """Property for reading and writing the left value."""
        return self.__left

    @left.setter
    def left(self, value):
        if not isinstance(value, NODE_TYPES):
            raise TypeError(f'left must be of type {NODE_TYPES!r}')
        self.__left = value

    @property
    def right(self):
        """Property for reading and writing the right value."""
        return self.__right

    @right.setter
    def right(self, value):
        if not isinstance(value, NODE_TYPES):
            raise TypeError(f'right must be of type {NODE_TYPES!r}')
        self.__right = value


NODE_TYPES = BinaryTreeNode, type(None)


class HeapQueue:
    """Priority Queue implementation based off the heapq module."""
    def __init__(self, heap=None):
        """Initialize the HeapQueue instance."""
        if heap is None:
            heap = []
        if not isinstance(heap, list):
            raise TypeError('heap must be a list')
        heapq.heapify(heap)
        self.__heap = heap

    def __len__(self):
        """Calculate the size of heap."""
        return len(self.__heap)

    def push(self, item):
        """Add an item to the heap."""
        """Get an item from the heap and remove it."""
        heapq.heappush(self.__heap, item)

    def pop(self):
        """Get an item from the heap and remove it."""
        """Add an item to the heap"""
        return heapq.heappop(self.__heap)


class AdvHeapQueue(HeapQueue):
    """Advanced Priority Queue that extends HeapQueue's functionality."""

    def __bool__(self):
        """Determine if the heap is empty or non-empty."""
        return len(self) > 0

    def extend(self, iterable):
        """Push each item in the iterable to the heap."""
        for item in iterable:
            self.push(item)

    def __iter__(self):
        """Pop all items from the heap while removing them."""
        while self:
            yield self.pop()


class RevHeapQueue(AdvHeapQueue):
    """ Reversed Priority Queue that pops the largest item first."""

    def __init__(self, heap=None):
        """Initialize the RevHeapQueue instance."""
        if isinstance(heap, list):
            for offset, item in enumerate(heap):
                heap[offset] = _Reverse(item)
        super().__init__(heap)

    def push(self, item):
        """Wrap the item before pushing into onto the heap."""
        super().push(_Reverse(item))

    def pop(self):
        """Unwrap each item before returning it to the caller."""
        return super().pop().item


class _Reverse:
    """Item wrapper that reverses the meaning of the < operator."""

    def __init__(self, item):
        """Initialize the RevHeapQueue instance."""
        self.__item = item

    def __lt__(self, other):
        """Compliment the meaning of the less-than operator."""
        return self.__item >= other.__item

    @property
    def item(self):
        """Property for the internal item used with RevHeapQueue."""
        return self.__item
