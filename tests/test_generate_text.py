"""
This module implements tests for the generate_text function

"""

# for mocking purposes
from unittest.mock import patch, mock_open

# pytest library
import pytest

# Import the generate_text_files function from the module where it's defined
from generate_text import generate_text_files


def test_generate_text_files_success():
    """
    Test case for the generate_text_files function when successful.

    Parameters:
    None

    Returns:
    None

    Raises:
    None

    Effects:
    Calls the generate_text_files function with a mock sizes list.
    Mocks os.getcwd, os.makedirs, builtins. Open, and random.randrange.
    Asserts that the function returns True and verifies 
    that open is called with the correct parameters.
    """

    # Mock sizes list
    sizes = [1000, 2000]

    # Mock for os.getcwd and os.makedirs
    with patch("os.getcwd", return_value="/mocked/path"), \
            patch("os.makedirs"), \
            patch("builtins.open", mock_open()) as mocked_file, \
            patch("random.randrange", return_value=0):
        # Call the function
        result = generate_text_files(sizes)

        # Assertions
        assert result is True, "True if all files are generated successfully."

        # Check that open is called with the correct parameters
        mocked_file.assert_any_call('/mocked/path/data/1k.txt', 'w', encoding='utf-8')
        mocked_file.assert_any_call('/mocked/path/data/2k.txt', 'w', encoding='utf-8')


def test_generate_text_files_type_error():
    """
    Test case for the generate_text_files function when an invalid data type is passed.

    Parameters:
    sizes (str): A string instead of a list. This is an invalid input for the function.

    Returns:
    bool: False if the function correctly identifies and handles the invalid data type.

    Raises:
    None

    Effects:
    Calls the generate_text_files function with an invalid sizes list.
    Asserts that the function returns False and verifies that it correctly
    handles the invalid data type.
    """

    # Pass an invalid type to the sizes list
    sizes = "not a list"
    # noinspection PyTypeChecker
    result = generate_text_files(sizes)
    assert result is False, "The function should return False if an invalid data type is passed."


def test_generate_text_files_os_error():
    """
    Test case for the generate_text_files function when an OSError occurs during file writing.

    Parameters:
    sizes (list): A list of integers representing the sizes of the text files to be generated.

    Returns:
    bool: False if the function correctly identifies and handles the OSError.

    Raises:
    None

    Effects:
    Calls the generate_text_files function with a mock sizes list.
    Mocks os.getcwd, os.makedirs, and builtins.open.
    Simulates an OSError during file writing.
    Asserts that the function returns False and verifies that it correctly handles the OSError.
    """

    # Mock sizes list
    sizes = [1000]

    # Mock for os.getcwd, os.makedirs, and open
    with patch("os.getcwd", return_value="/mocked/path"), \
            patch("os.makedirs"), \
            patch("builtins.open", mock_open()) as mocked_file:
        # Simulate an OSError during file writing
        # noinspection PyArgumentList
        mocked_file().writelines.side_effect = OSError

        result = generate_text_files(sizes)
        assert result is False, "return False if an OSError occurs during file writing."


def test_generate_text_files_file_exists_error():
    """
    Test case for the generate_text_files function when a 
    FileExistsError occurs during file writing.

    Parameters:
    sizes (list): A list of integers representing the sizes of the text files to be generated.

    Returns:
    bool: True if the function correctly handles the FileExistsError and continues.

    Raises:
    None

    Effects:
    Calls the generate_text_files function with a mock sizes list.
    Mocks os.getcwd, os.makedirs, and builtins.open.
    Simulates a FileExistsError during file writing.
    Asserts that the function returns True and verifies 
    that it correctly handles the FileExistsError.
    """

    # Mock sizes list
    sizes = [1000]

    # Mock for os.getcwd, os.makedirs, and open
    with patch("os.getcwd", return_value="/mocked/path"), \
            patch("os.makedirs"), \
            patch("builtins.open", mock_open()) as mocked_file:
        # Simulate a FileExistsError during file writing
        # noinspection PyArgumentList
        mocked_file().writelines.side_effect = FileExistsError

        result = generate_text_files(sizes)
        assert result is True, "The function should handle FileExistsError and continue."


# Run the tests
if __name__ == "__main__":
    pytest.main()
