""" 
This module implements tests for the server-side and ensures that the server
is able to handle multiple client connections concurrently and that it works properly
"""

# for multithreading connections
import threading
# for mock operations
from unittest.mock import patch, MagicMock, mock_open
# for ssl support and testing
import ssl

# Allow some time for the server to start
import time

# main testing module used
import pytest

from server.server import SSL_CERT
from server.server import SSL_KEY
from server.server import algorithms
from server.server import server_configuration
from server.server import client_conn
from server.server import retrieve_all_file_lines
from server.server import searching_string
from server.server import create_ssl_connection_context


def test_create_ssl_connection_context_success():
    """
    Test case for creating an SSL connection context with valid certificate and key files.

    This function uses the `unittest.mock.patch` decorator to mock 
    the `ssl.create_default_context` function.
    It also creates a mock SSL context object and sets up its methods to return specific values.
    The function then calls the `create_ssl_connection_context` 
    function and verifies that it returns the expected SSL context object.
    Additionally, it checks that the `ssl.create_default_context` 
    function and the `load_cert_chain` method of the SSL context object 
    are called with the correct parameters.

    Returns:
        None
    """
    with patch('ssl.create_default_context') as mock_create_default_context:
        mock_context = MagicMock()
        mock_create_default_context.return_value = mock_context
        mock_context.load_cert_chain.return_value = None

        # Call the function under test
        context = create_ssl_connection_context()

        # Verify that the ssl.create_default_context function is called with the correct parameters
        mock_create_default_context.assert_called_once_with(ssl.Purpose.CLIENT_AUTH)

        # Verify that the load_cert_chain method of the SSL context
        # object is called with the correct parameters
        mock_context.load_cert_chain.assert_called_once_with(certfile=SSL_CERT, keyfile=SSL_KEY)

        # Verify that the function returns the expected SSL context object
        assert context == mock_context


def test_create_ssl_connection_context_file_not_found():
    """
    Test case for creating an SSL connection context when 
    the certificate or key files are not found.

    This function uses the `unittest.mock.patch` 
    decorator to mock the `ssl.create_default_context` function.
    It also creates a mock SSL context object and sets
    up its methods to raise a `FileNotFoundError`.
    The function then calls the `create_ssl_connection_context`
    function and verifies that it raises a `FileNotFoundError`.
    Additionally, it checks that the `ssl.create_default_context` 
    function and the `load_cert_chain` method of the SSL context object 
    are called with the correct parameters.

    Parameters:
    None

    Returns:
    None

    Raises:
    FileNotFoundError: If the certificate or key files are not found.

    Effects:
    Calls the `ssl.create_default_context` function and the `load_cert_chain`
    method of the SSL context object.
    """
    with patch('ssl.create_default_context') as mock_create_default_context:
        mock_context = MagicMock()
        mock_create_default_context.return_value = mock_context
        mock_context.load_cert_chain.side_effect = FileNotFoundError

        with pytest.raises(FileNotFoundError):
            create_ssl_connection_context()

        mock_create_default_context.assert_called_once_with(ssl.Purpose.CLIENT_AUTH)
        mock_context.load_cert_chain.assert_called_once_with(certfile=SSL_CERT, keyfile=SSL_KEY)


def test_retrieve_all_file_lines_success():
    """
    Test function to verify the behavior of retrieve_all_file_lines function
    when a file is opened successfully.

    Parameters:
    None

    Returns:
    None

    Effects:
    Uses the mock 'open' function from the 'unittest.mock' module to
    simulate opening a file that contains specific content.
    Calls the retrieve_all_file_lines function with a dummy file path.
    Asserts that the function returns a list of strings, where each string 
    represents a line in the file.
    """

    # Mock file content
    mock_file_content = "line1\nline2\nline3\n"
    expected_res = ["line1\n", "line2\n", "line3\n"]

    # Use mock_open to simulate opening a file that contains the mock content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        res = retrieve_all_file_lines("dummy_path")
        assert res == expected_res, "The function should return all lines in the file as a list."


def test_retrieve_all_lines_os_error():
    """
    Test function to verify the behavior of retrieve_all_file_lines 
    function when a file cannot be opened.

    Parameters:
    None

    Returns:
    None

    Effects:
    Uses the mock 'open' function from the 'unittest.mock' module to 
    simulate an OSError when trying to open a file.
    Calls the retrieve_all_file_lines function with a non-existent file path.
    Asserts that the function returns an empty list when the file cannot be opened.
    """

    # Simulate a OSError when trying to open the file
    with patch("builtins.open", side_effect=OSError):
        result = retrieve_all_file_lines("path/testing")
        assert result == [], "The function should return an empty list if the file is not found."


def test_search_string_present():
    """
    Test function to verify if a search string is present in a file.

    Parameters:
    mock_file_content (list): A list of strings representing the content of the file.
    search_string (str): The string to search for in the file.
    True (bool): A boolean flag indicating whether the search should be case-sensitive.
    search_algorithms['linear'] (function): The search algorithm to use for the search.

    Returns:
    bool: True if the search string is found in the file, False otherwise.

    """
    mock_file_content = ["line1\n", "line2\n"]
    search_string = "line1"
    with patch('server.server.retrieve_all_file_lines', return_value=mock_file_content):
        result = searching_string('dummy_filepath', search_string, True, algorithms['linear'])
        assert result is True

    search_string = "line3"
    with patch('server.server.retrieve_all_file_lines', return_value=mock_file_content):
        result = searching_string('dummy_filepath', search_string, True, algorithms['linear'])
        assert result is False


def test_client_connection_handling():
    """
    Test function for client_connection_handling function.

    This function tests the behavior of the client_connection_handling function 
    when a client connects to the server.
    It uses mock objects to simulate the client socket and the search_string_present function.

    Parameters:
    None

    Returns:
    None

    Effects:
    Calls the client_connection_handling function with a mock
    client socket, address, and search string.
    Verifies that the client_socket's recv method is called with the correct parameters.
    Verifies that the search_string_present function is called with the correct parameters.
    Verifies that the client_socket's sendall method is called with the correct
    response when the search string is found.
    """

    client_socket = MagicMock()  # Mock client socket object
    address = ('127.0.0.1', 12345)  # Mock client address
    search_string = "test_string"  # Mock search string
    response = "STRING EXISTS\n"  # Expected response when search string is found

    # Mock the search_string_present function to return True
    with patch('server.server.search_string_present', return_value=True):
        # Mock the recv method of the client socket to return the search string
        with patch.object(client_socket, 'recv', return_value=search_string.encode('utf-8')):
            # Mock the sendall method of the client socket to check if
            # it is called with the correct response
            with patch.object(client_socket, 'sendall') as mock_sendall:
                # Call the client_connection_handling function
                client_conn(client_socket, address)
                # Verify that the sendall method is called with the correct response
                mock_sendall.assert_called_once_with(response.encode('utf-8'))


# Function to test the server configuration
def test_server_configuration():
    """
    Test function for server_configuration function.

    This function tests the behavior of the server_configuration
    when the address and port are specified

    Parameters:
    None

    Returns:
    None

    """
    # Mock the socket object and its methods
    mock_socket = MagicMock()
    mock_client_socket = MagicMock()
    mock_address = ('127.0.0.1', 12345)

    with patch('socket.socket', return_value=mock_socket):
        # Set up the socket method mocks
        mock_socket.accept.return_value = (mock_client_socket, mock_address)

        # Run the server_configuration function in a separate thread to prevent blocking
        server_thread = threading.Thread(target=server_configuration, args=(8080,))
        server_thread.daemon = True
        server_thread.start()

        time.sleep(1)

        # Test that the socket methods were called correctly
        mock_socket.bind.assert_called_once_with(('0.0.0.0', 8080))
        mock_socket.listen.assert_called_once_with(5)
        mock_socket.accept.assert_called()


if __name__ == "__main__":
    pytest.main()
