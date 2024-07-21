"""
This module tests the implementation of search algorithms and helps to manage
and maintain the reliability of the search algorithms.
"""

# static typing
from typing import Optional, Any, Dict

# pytest library
import pytest

# function importation
from search_algorithms import (
    linear_search,
    binary_search,
    breadth_search,
    depth_search,
    hash_search
)


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """
    This function contains the sample data which is
    dummy data to be used for testing purposes.
    """
    return {
        "lines": ["line1", "line2", "line3", "line4"],
        "search_string": "line3",
        "missing_string": "line5",
        "empty_lines": [],
        "set_lines": {"line1", "line2", "line3", "line4"}
    }


# pylint: disable=redefined-outer-name
def test_linear_search(sample_data: Optional[Dict[str, Any]]):
    """
    Test function for linear_search function.

    This function tests the linear_search function with various inputs, including
    valid and invalid data, to ensure its correctness.

    Parameters:
    sample_data (dict): A dictionary containing test data.
    The dictionary should contain the following keys:
                        - "lines": A list of strings to be searched.
                        - "search_string": The string to be searched for.
                        - "missing_string": A string that is not present in the list.
                        - "empty_lines": An empty list.
                        - "set_lines": A set of strings to be searched.

    Returns:
    None. This function is used for testing purposes only.
    """
    assert linear_search(sample_data["lines"], sample_data["search_string"]) is True
    assert linear_search(sample_data["lines"], sample_data["missing_string"]) is False
    assert linear_search(None, sample_data["search_string"]) is False
    # noinspection PyTypeChecker
    assert linear_search(sample_data["lines"], None) is False
    assert linear_search(sample_data["empty_lines"], sample_data["search_string"]) is False
    assert linear_search(sample_data["set_lines"], sample_data["search_string"]) is True


# pylint: disable=redefined-outer-name
def test_binary_search(sample_data: Optional[Dict[str, Any]]):
    """
    Test function for binary_search function.

    This function tests the binary_search function with various inputs, including
    valid and invalid data, to ensure its correctness.

    Parameters:
    sample_data (dict): A dictionary containing test data.
    The dictionary should contain the following keys:
                        - "lines": A list of strings to be searched.
                        - "search_string": The string to be searched for.
                        - "missing_string": A string that is not present in the list.
                        - "empty_lines": An empty list.
                        - "set_lines": A set of strings to be searched.

    Returns:
    None. This function is used for testing purposes only.
    """
    assert binary_search(sample_data["lines"], sample_data["search_string"]) is True
    assert binary_search(sample_data["lines"], sample_data["missing_string"]) is False
    assert binary_search(None, sample_data["search_string"]) is False
    # noinspection PyTypeChecker
    assert binary_search(sample_data["lines"], None) is False
    assert binary_search(sample_data["empty_lines"], sample_data["search_string"]) is False
    assert binary_search(sample_data["set_lines"], sample_data["search_string"]) is True


# pylint: disable=redefined-outer-name
def test_breadth_first_search(sample_data: Optional[Dict[str, Any]]):
    """
    Test function for breadth_first_search function.

    This function tests the breadth_first_search function with various inputs, including
    valid and invalid data, to ensure its correctness.

    Parameters:
    sample_data (dict): A dictionary containing test data.
    The dictionary should contain the following keys:
                        - "lines": A list of strings to be searched.
                        - "search_string": The string to be searched for.
                        - "missing_string": A string that is not present in the list.
                        - "empty_lines": An empty list.
                        - "set_lines": A set of strings to be searched.

    Returns:
    None. This function is used for testing purposes only.
    """
    assert breadth_search(sample_data["lines"], sample_data["search_string"]) is True
    assert breadth_search(sample_data["lines"], sample_data["missing_string"]) is False
    assert breadth_search(None, sample_data["search_string"]) is False
    # noinspection PyTypeChecker
    assert breadth_search(sample_data["lines"], None) is False
    assert breadth_search(sample_data["empty_lines"], sample_data["search_string"]) is False
    assert breadth_search(sample_data["set_lines"], sample_data["search_string"]) is True


# pylint: disable=redefined-outer-name
def test_depth_first_search(sample_data: Optional[Dict[str, Any]]):
    """
    Test function for depth_first_search function.

    This function tests the depth_first_search function with various inputs, including
    valid and invalid data, to ensure its correctness.

    Parameters:
    sample_data (dict): A dictionary containing test data.
    The dictionary should contain the following keys:
                        - "lines": A list of strings to be searched.
                        - "search_string": The string to be searched for.
                        - "missing_string": A string that is not present in the list.
                        - "empty_lines": An empty list.
                        - "set_lines": A set of strings to be searched.

    Returns:
    None. This function is used for testing purposes only.
    """
    assert depth_search(sample_data["lines"], sample_data["search_string"]) is True
    assert depth_search(sample_data["lines"], sample_data["missing_string"]) is False
    assert depth_search(None, sample_data["search_string"]) is False
    # noinspection PyTypeChecker
    assert depth_search(sample_data["lines"], None) is False
    assert depth_search(sample_data["empty_lines"], sample_data["search_string"]) is False
    assert depth_search(sample_data["set_lines"], sample_data["search_string"]) is True


# pylint: disable=redefined-outer-name
def test_hash_table_search(sample_data: Optional[Dict[str, Any]]):
    """
    Test function for hash_table_search function.

    Parameters:
    sample_data (dict): A dictionary containing test data.

    Returns:
    None. This function is used for testing purposes only.
    """
    assert hash_search(sample_data["lines"], sample_data["search_string"]) is True
    assert hash_search(sample_data["lines"], sample_data["missing_string"]) is False
    assert hash_search(None, sample_data["search_string"]) is False
    # noinspection PyTypeChecker
    assert hash_search(sample_data["lines"], None) is False
    assert hash_search(sample_data["empty_lines"], sample_data["search_string"]) is False
    assert hash_search(sample_data["set_lines"], sample_data["search_string"]) is True


# run the main program
if __name__ == "__main__":
    pytest.main()
