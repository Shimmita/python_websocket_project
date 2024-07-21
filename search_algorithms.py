"""
This module contains the implementation of various such algorithms
Will be used for testing and evaluation purposes.
These algorithms include but not limited to the following:

linear search algorithm
binary search algorithm
breadth-first search algorithm
depth-first search algorithm
exponential search algorithm
greedy search algorithm
hash table search algorithm

"""

# for queueing operations that are associated with breadth-first search
from collections import deque
# for static typing
from typing import List, Optional, Set


def linear_search(all_lines: Optional[List[str]] | Optional[Set[str]], q_string: str) -> bool:
    """
    Perform a linear search to find an exact match of the search string.
    Linear search is performed sequentially through the data until
    the search string is found.
    It is inefficient if the data sample space is very large but
    efficient if it is relatively small.
    Time complexity is O(n) where n is the number of elements in the sample space.

    Args:
        all_lines (Optional[List[str]]|Optional[Set[str]]):
        A list or set of strings to search through.
        q_string (str): The query string to search

    Returns:
        bool: True if the string is found, False otherwise.
    """
    result: bool = False
    # handle if no all_lines_present
    if all_lines is None:
        print('\ncannot perform searching operation on empty data\n')
    # handle if no search_string
    if q_string is None:
        print('string to be searched is empty, provide query string')
    # if data is a list, perform linear search
    if isinstance(all_lines, list):
        result = any(line.strip() == q_string for line in all_lines)
    # if data is a set, perform linear search
    if isinstance(all_lines, set):
        result = q_string in all_lines

    # handle invalid data type
    if not isinstance(all_lines, (set, list)):
        print(f'Invalid data type passed ({all_lines}) expected a set or list')

    return result


def breadth_search(all_lines: Optional[List[str]] | Optional[Set[str]], q_string: str) -> bool:
    """
    Breadth-first search works by starting from a given node, called the root node,
    and visiting all its adjacent nodes, called the neighbors. 
    Then, it visits all the neighbors of the neighbors, and so on, 
    until it reaches the target node or exhausts all the nodes
    The time complexity of breadth-first search is O(m + n),
    where m is the number of edges and n is the number of nodes in the graph.
    implementations are based on Queue data structure which works on FIFO pattern
    First In First Out

    Args:
        all_lines (List[str]):
        List of lines to search through.
        q_string (str): String to search for.

    Returns:
        bool: True if the string is found, False otherwise.
    """

    # handle if no all_lines_present
    if all_lines is None:
        print('\ncannot perform searching operation on empty data\n')
        return False
    if q_string is None:
        print('string to be searched is empty, provide query string')
        return False

    # data being passed is not allowed for this project
    if not isinstance(all_lines, (set, list)):
        print(f'Invalid data type passed ({all_lines}) expected a set or list')

    # converting the list into Queue
    queue = deque(all_lines)
    # valid if the queue is not empty
    while queue:
        # getting the popped element from the queue and use for comparison
        current_line = queue.popleft()
        # comparing the element with the query string
        if current_line.strip() == q_string:
            print(current_line)
            return True
    return False


def depth_search(all_lines: Optional[List[str]] | Optional[Set[str]], q_string: str) -> bool:
    """
    works by starting from a given node, called the source,
    and following one path as deep as possible, 
    until it reaches the target node. 
    Then, it backtracks and tries another path, until it visits all the nodes or finds the target.
    The time complexity of depth first search is O(m + n), 
    where m is the number of edges and n is the number of nodes in the graph.
    It's slightly slower than  breadth first search especially if the backtracking process is longer
    Implementations is based on the stack data structure to facilitate backtracking

    Args:
        all_lines (List[str]):
        List of lines to search through.
        q_string (str): String to search for.

    Returns:
        bool: True if the string is found, False otherwise.
    """

    # handle if no all_lines_present
    if all_lines is None:
        print('\ncannot perform searching operation on empty data\n')
        return False
    if q_string is None:
        print('string to be searched is empty, provide query string')
        return False

    # data being passed is not allowed for this project
    if not isinstance(all_lines, (set, list)):
        print(f'Invalid data type passed ({all_lines}) expected a set or list')

    # make the list behave like stack data structure and removing lines one by one
    # and the valued popped is used to compare till we find the matching line.
    # stack work on LIFO Last In First Out

    # data is a set thus we need to make it a list
    if isinstance(all_lines, set):
        stack_data_structure = list(all_lines)
        while stack_data_structure:
            current_line = stack_data_structure.pop()
            if current_line.strip() == q_string:
                return True

    # data is list thus no need to make it a list
    else:
        while all_lines:
            current_line = all_lines.pop()
            if current_line.strip() == q_string:
                return True

    return False


def hash_search(all_lines: Optional[List[str]] | Optional[Set[str]], q_string: str) -> bool:
    """
    Hash table search algorithm makes use of hashing functions that are mathematically performed.
    Hash table search works by applying the hash function to the target
    and looking up the corresponding value in the hash table.
    If the value exists, the search is successful.
    If the value does not exist, the search fails
    finds the target in constant time regardless of the size of the data.
    time complexity is O(1).
    since the search works on unique hashes, the search uses Set Collections.

    Args:
        all_lines (List[str]): List of lines to search through.
        q_string (str): String to search for.

    Returns:
        bool: True if the string is found, False otherwise.
    """
    # handle if no all_lines_present
    if all_lines is None:
        print('\ncannot perform searching operation on empty data\n')
        return False
    if q_string is None:
        print('string to be searched is empty, provide query string')
        return False

        # data being passed is not allowed for this project
    if not isinstance(all_lines, (set, list)):
        print(f'Invalid data type passed ({all_lines}) expected a set or list')

    # converting the list to conform into a set data structure which only contains unique values
    if isinstance(all_lines, list):
        hash_table = set(line.strip() for line in all_lines)
        # return the boolean state of the presence of the query string in the hash table
        return q_string in hash_table

    # data passed is a set no need to convert
    else:
        # return the boolean state of the presence of the query string in the hash table
        return q_string in all_lines


def binary_search(all_lines: Optional[List[str]] | Optional[Set[str]], q_string: str) -> bool:
    """
    Binary search is a more efficient and faster algorithm than linear search.
    It works by dividing the data into two halves and comparing the target with the middle element. 
    If the target is equal to the middle element, the search is done. 
    If the target is smaller than the middle element,the search continues in the left half. 
    If the target is larger than the middle element, the search continues in the right half.
    This process is repeated until the target is found or the data is exhausted.

    Args:
        all_lines (List[str]): List of  lines to search through.
        q_string (str): String to search for.

    Returns:
        bool: True if the string is found, False otherwise.
    """
    # handle if no all_lines_present
    if all_lines is None:
        print('\ncannot perform searching operation on empty data\n')
        return False
    if q_string is None:
        print('string to be searched is empty, provide query string')
        return False

    if isinstance(all_lines, list):
        # change all_lines to a set for faster retrieval
        left_value: int
        right_value: int
        left_value, right_value = {0, len(all_lines) - 1}
        while left_value <= right_value:
            # midpoint string value of the line
            mid = (left_value + right_value) // 2
            midpoint = all_lines[mid].strip()
            # search is done and the string is found to exist at midpoint
            if midpoint == q_string:
                return True
            # checking midpoint position in relation to the search string
            elif midpoint < q_string:
                # shift midpoint position to the right
                left_value = mid + 1
            else:
                # shift midpoint position to the left
                right_value = mid - 1
    if isinstance(all_lines, set):
        # change it to a set for faster retrieval
        all_lines = sorted(all_lines)
        left, right = 0, len(all_lines) - 1
        while left <= right:
            # getting the midpoint string value of the line
            mid = (left + right) // 2
            mid_value = all_lines[mid].strip()
            # the search is done and the string is found to exist at midpoint
            if mid_value == q_string:
                return True
            # checking the midpoint position in relation to the search string
            elif mid_value < q_string:
                # shift the midpoint position to the right
                left = mid + 1
            else:
                # shift the midpoint position to the left
                right = mid - 1

    # data being passed is not allowed for this project
    if not isinstance(all_lines, (set, list)):
        print(f'Invalid data type passed ({all_lines}) expected a set or list')

    # no match found
    return False
