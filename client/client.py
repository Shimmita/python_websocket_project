"""
This is the client side of the project that will be responsible for the following:
Make use of socket programming module to connect to the server with the connection
established under the foundation of SSL Enabled or SSL Disabled.
This will depend on the boolean status of use_ssl parameter that will be passed in the
client_configuration function. The default value is False
"""

# contains the socket programming functionality that facilitates server and client communication
import socket

# this module is used for file path compatibility i.e. windows, linux or macOS
import os

# ssl module for ssl related functionality
import ssl

# this module is for parsing the configuration files in config.ini file in config folder
import configparser

# typing module for static typing related functionality
from typing import Optional

# server connection address or Internet Protocol address of the server
SERVER_ADDRESS: str = 'localhost'
# the configuration parser initialization
configuration_file = configparser.ConfigParser()

# reading the config.ini file located in the config folder
configuration_file.read(os.path.join(os.getcwd(), 'config.ini'))

# SSL boolean value indicating whether SSL is enabled or disabled when connecting to the server
USE_SSL: bool = configuration_file['DEFAULT'].getboolean('SSL_ENABLED')
# retrieving port number of the server from the configuration file
PORT_NUMBER: int = configuration_file['DEFAULT'].getint('PORT_NUMBER')

# Query string that will be searched by the server for results.
# This string is present in the 200k.text
QUERY_STRING: str = '13;0;23;11;0;16;5;000;'

# Self Signed Certificate that will be used to verify with the server certificate
CLIENT_SELF_SIGNED_CERT = os.path.join(f'{os.getcwd()}/client/cert', 'combined.pem')


def create_ssl_connection_context() -> Optional[ssl.SSLContext]:
    """ 
    This function creates and returns a new SSL connection context.
    This context is used to establish secure connections to servers.

    Args:
    None
    
    Returns:
    Optional[ssl.SSLContext]: An SSL context object if successful, otherwise None.

    Raises:
    FileNotFoundError: If the SSL certificate file or key file is not found.

    Note:
    The SSL context is configured to verify the server's certificate using the 
    CLIENT_SELF_SIGNED_CERT file. The ssl.CERT_REQUIRED mode ensures that the 
    server's certificate is verified.
    """
    ssl_context: ssl.SSLContext
    # Try-except block to handle potential errors during SSL context creation
    try:
        # Create a new SSL context for server authentication
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        # Load the SSL certificate and key file into the SSL context
        ssl_context.load_verify_locations(CLIENT_SELF_SIGNED_CERT)
        # Set the SSL verification mode to require a valid certificate
        ssl_context.verify_mode = ssl.CERT_REQUIRED
    except FileNotFoundError as e:
        # Print an error message instead of raising an exception
        print(f'Error: SSL cert file or keyfile is invalid check in ssl_keys folder!\n{e}')
        return None
    # Return the SSL context object
    return ssl_context


def client_config(server_addr: str, server_port: int, query_string: str, use_ssl: bool = False):
    """
    This function is responsible for sending a query_string to the server.
    The server will search for the specified query string in its data directory
    which contains string file(s) with a .txt extension.
    The response from the server will either be STRING EXISTS or STRING NOT FOUND.

    Args:
        server_addr (str): The server's address.
        server_port (int): The port number to connect to.
        query_string (str): The query string to send.
        use_ssl (bool): Whether to use SSL for the connection. Default is False.

    Returns:
        None. Prints the response from the server.

    Raises:
        Exception: If there is an error sending the query.
    """
    try:
        # creating a socket connection to connect to the server
        with socket.create_connection((server_addr, server_port)) as sock:
            if use_ssl:
                # getting SSL connection context from the predefined function
                context = create_ssl_connection_context()
                # tunneling the connection socket in encrypted SSL protocol environment
                with context.wrap_socket(sock, server_hostname=server_addr) as server_sock:
                    # sending encoded request to the server socket for processing
                    server_sock.sendall(query_string.encode('utf-8'))
                    # response from the server socket is decoded into a string representation
                    # once in a chunk of 1024 bytes
                    response = server_sock.recv(1024).decode('utf-8')
            # No SSL connection to the server
            else:
                # sending encoded request to the server socket for processing
                sock.sendall(query_string.encode('utf-8'))
                # response from the server socket is decoded into a string representation
                # once in a chunk of 1024 bytes
                response = sock.recv(1024).decode('utf-8')
            print(response)
    except NotImplementedError as e:
        # printing the exception for debugging purposes
        print(f"Error:Failed to create SSL context: {e}")


# main function that calls the client_configuration function to begin client execution
if __name__ == "__main__":
    # The main entry point of the client application
    # handling connection errors
    try:
        client_config(SERVER_ADDRESS, PORT_NUMBER, QUERY_STRING, USE_SSL)
        # The server is using SSL connections thus client may be using no SSL or
        # wrong SSL certificates
    except ConnectionResetError as reset:
        print(f'authentication failed check your SSL credentials or SSL connection status: {reset}')
        # probably the server is not running and maybe offline
    except ConnectionRefusedError as cref:
        print(f'connection refused server may be offline check the server and try again: {cref}')
        # The server is probably not using SSL connections thus we need to ensure that our client is
        # also not running in SSL mode. Thus make USE_SSL to False at the client side
    except ssl.SSLEOFError as error:
        print(f'server is not running in SSL mode default USE_SSL to False:{error} ')
