""" 
This module implements tests for the client side of the project and ensures that
the client is able to handle multiple client connections concurrently and that it works properly
"""
# for ssl connections
import ssl
# for simulating mocking the client side of the project
from unittest.mock import patch, MagicMock
# for path IO related functions
import os
# import of functions from the client for testing
from client.client import create_ssl_connection_context, client_config

# Self Signed Certificate that will be used to verify with the server certificate
CLIENT_SELF_SIGNED_CERT = os.path.join(f'{os.getcwd()}/client/cert', 'combined.pem')


def test_create_ssl_connection_context_success():
    """
    This function tests the create_ssl_connection_context function when it succeeds.

    Parameters:
    None

    Returns:
    None

    """
    # Patch the ssl.create_default_context function to create a mock context
    with patch('ssl.create_default_context') as mock_create_default_context:
        # Create a mock context object
        mock_context = MagicMock()
        # Set the return value of the mock context object
        mock_create_default_context.return_value = mock_context
        # Set the return value of the load_verify_locations method of the mock context object
        mock_context.load_verify_locations.return_value = None
        # Call the create_ssl_connection_context function
        context = create_ssl_connection_context()
        # Assert that the ssl.create_default_context function was called with the correct parameters
        mock_create_default_context.assert_called_once_with(ssl.Purpose.SERVER_AUTH)
        # Assert that the load_verify_locations method of the mock context object
        # was called with the correct parameters
        mock_context.load_verify_locations.assert_called_once_with(CLIENT_SELF_SIGNED_CERT)
        # Assert that the returned context is equal to the mock context object
        assert context == mock_context


def test_create_ssl_connection_context_file_not_found():
    """
    This function tests the create_ssl_connection_context function 
    when the certificate file is not found.

    Parameters:
    None

    Returns:
    None

    """
    # Patch the ssl.create_default_context function to create a mock context
    with patch('ssl.create_default_context') as mock_create_default_context:
        # Create a mock context object
        mock_context = MagicMock()
        # Set the return value of the mock context object
        mock_create_default_context.return_value = mock_context
        # Set the side effect of the load_verify_locations method
        # the mock context object to FileNotFoundError
        mock_context.load_verify_locations.side_effect = FileNotFoundError
        # Call the create_ssl_connection_context function
        context = create_ssl_connection_context()
        # Assert that the ssl.create_default_context function was called
        # with the correct parameters
        mock_create_default_context.assert_called_once_with(ssl.Purpose.SERVER_AUTH)
        # Assert that the load_verify_locations method of the mock context
        # object was called with the correct parameters
        mock_context.load_verify_locations.assert_called_once_with(CLIENT_SELF_SIGNED_CERT)
        # Assert that the returned context is None
        assert context is None


@patch('socket.create_connection')
@patch('ssl.create_default_context')
def test_client_configuration_ssl(mock_create_default_context, mock_create_connection):
    """
    This function tests the client_configuration function when SSL is enabled.

    Parameters:
    mock_create_default_context (MagicMock): A mock object for ssl.create_default_context function.
    mock_create_connection (MagicMock): A mock object for socket.create_connection function.

    Returns:
    None

    """
    mock_socket = MagicMock()
    mock_ssl_context = MagicMock()
    mock_server_socket = MagicMock()

    # Mock context manager behavior for socket and ssl
    mock_create_connection.return_value.__enter__.return_value = mock_socket
    mock_create_default_context.return_value = mock_ssl_context
    mock_ssl_context.wrap_socket.return_value.__enter__.return_value = mock_server_socket
    mock_server_socket.recv.return_value = b'STRING EXISTS'
    client_config('localhost', 7777, 'test_query', use_ssl=True)
    # Assert that the socket.create_connection function was called with the correct parameters
    mock_create_connection.assert_called_once_with(('localhost', 7777))
    # Assert that the ssl.create_default_context function was called with the correct parameters
    mock_create_default_context.assert_called_once_with(ssl.Purpose.SERVER_AUTH)
    # Assert that the load_verify_locations method of the ssl context object
    # was called with the correct parameters
    mock_ssl_context.load_verify_locations.assert_called_once_with(CLIENT_SELF_SIGNED_CERT)
    # Assert that the wrap_socket method of the ssl context object
    # was called with the correct parameters
    mock_ssl_context.wrap_socket.assert_called_once_with(mock_socket, server_hostname='localhost')
    # Assert that the sendall method of the socket object was called with the correct parameters
    mock_server_socket.sendall.assert_called_once_with(b'test_query')
    # Assert that the recv method of the socket object was called with the correct parameters
    mock_server_socket.recv.assert_called_once_with(1024)


@patch('socket.create_connection')
def test_client_configuration_no_ssl(mock_create_connection):
    """
    This function tests the client_configuration function when SSL is not enabled.

    Parameters:
    mock_create_connection (MagicMock): A mock object for socket.create_connection function.

    Returns:
    None

    """
    # Create a mock socket object
    mock_socket = MagicMock()

    # Mock context manager behavior for socket
    # When the socket is created, return the mock socket
    mock_create_connection.return_value.__enter__.return_value = mock_socket
    # Set the return value of the recv method of the mock socket to 'STRING EXISTS'
    mock_socket.recv.return_value = b'STRING EXISTS'
    # Call the client_configuration function with SSL disabled
    client_config('localhost', 7777, 'test_query', use_ssl=False)
    # Assert that the socket.create_connection function was called with the correct parameters
    mock_create_connection.assert_called_once_with(('localhost', 7777))
    # Assert that the sendall method of the socket object was called with the correct parameters
    mock_socket.sendall.assert_called_once_with(b'test_query')
    # Assert that the recv method of the socket object was called with the correct parameters
    mock_socket.recv.assert_called_once_with(1024)
