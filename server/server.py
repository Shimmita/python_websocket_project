""" 
The server module will facilitate socket programming functionality for client.py
to connect and search for a string and if the string is found the server returns
STRING EXISTS  else STRING NOT FOUND with a new line character at the end

The server will make use of multithreading capabilities to facilitate asynchronous
connection from the client.
The advantage of using threads is that no waiting is required to process the next
request all of them are processed simultaneously and overwhelming the server in 
processing the client's requests is minimised absolutely since different threads
will be dispatched to handle requests in a given process
"""

# contains the socket programming functionality that facilitates server and client communication
import socket

# this module is for parsing the configuration files in config.ini file in config folder
import configparser

# this module is used for file path compatibility i.e. windows, linux or macOS
import os

# import datetime module for time logging
from datetime import datetime

# provides functions to manipulate time. I used it to get time deference between executions
import time

# this module enables static typing functionality
from typing import Optional, List, Set, Tuple

# ssl module for ssl related functionality
import ssl

# threading module helps in achieving multithread execution to the server
import threading
# this module contains various search algorithms defined in
from search_algorithms import (
    linear_search,
    depth_search,
    breadth_search,
    hash_search,
    binary_search
)

# creating a dictionary of search algorithms that maps to the respective search algorithm
algorithms = {
    "linear": linear_search,
    "depth": depth_search,
    "breadth": breadth_search,
    "hash": hash_search,
    "binary": binary_search,
}

# the configuration parser initialization
CONFIG_FILE = configparser.ConfigParser()

# reading the config.ini file located in the config folder
CONFIG_FILE.read(os.path.join(os.getcwd(), 'config.ini'))

# retrieving data dir path containing the text file from config.ini
TEMP_DIR: str = CONFIG_FILE['DEFAULT'].get('linuxpath')

# retrieving the dir path containing the ssl files from config.ini
SSL_KEYS_DIR: str = CONFIG_FILE['DEFAULT'].get('SSL_DIR_FILES')
# getting file path using the os module to  read the text file from the data directory
# this directory holds dummy text files for testing the performance of the search algorithm
# across different file sizes when the file "performance.py is executed for it creates text files"
# that are custom and saves them in the data directory. the default file is 200k.txt which contains
# 200,000 lines of text can be replaced with any text within the directory
# when the file "performance.py"  is executed for it creates other text files.
FILE_PATH: str = os.path.join(f'{os.getcwd()}/{TEMP_DIR}', '200k.txt')

# retrieving REREAD_ON_QUERY from the config.ini file
REREAD_ON_QUERY: bool = CONFIG_FILE['DEFAULT'].getboolean('REREAD_ON_QUERY')
# retrieve the path to the SSL certificate from the ssl_keys folder
SSL_CERT: str = os.path.join(SSL_KEYS_DIR, 'self_signed_cert.pem')

# retrieve the path to the SSL private key from the ssl_keys folder
SSL_KEY: str = os.path.join(SSL_KEYS_DIR, 'private_key.pem')

# the max size of the payload the server will receive from the client
MAX_PAYLOAD_SIZE: int = CONFIG_FILE['DEFAULT'].getint('MAX_PAYLOAD_SIZE')

# retrieving port number from the configuration file
PORT_NUMBER: int = CONFIG_FILE['DEFAULT'].getint('PORT_NUMBER')

# retrieving the boolean variable from the configuration file for checking ssl flag
USE_SSL_CONNECTION: bool = CONFIG_FILE['DEFAULT'].getboolean('SSL_ENABLED')

# the SSLContext variable
SSL_CONTEXT: ssl.SSLContext | None = None
# Global variable to store file lines if reread_on_query is False
ALL_LINES: Optional[Set[str]] | Optional[List[str]] = None


def create_ssl_connection_context() -> Optional[ssl.SSLContext]:
    """ 
    This function creates and returns a new SSL connection context.

    The SSL context is used to manage settings for SSL/TLS connections. 
    It encapsulates the protocol version, cipher suites, certificate validation, 
    and other SSL/TLS parameters.

    Args:
    None
    
    Returns:
    Optional[ssl.SSLContext]: An SSL context object if the creation is successful, 
    or None if an error occurs.
    """
    # Try-except block to handle potential errors during SSL context creation
    try:
        current_context: ssl.SSLContext = SSL_CONTEXT
        # Create a default SSL context for server-client authentication
        current_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # Load the SSL certificate and private key files into the SSL context
        current_context.load_cert_chain(certfile=SSL_CERT, keyfile=SSL_KEY)
        print('\nSSL Connection Context Created Successfully\n')
        return current_context

    except FileNotFoundError as e:
        # Handle the case where the SSL certificate or private key files are not found
        print(f'Error: SSL cert file or keyfile is invalid. Check in ssl_keys folder!\n{e}')
        raise


# getting the SSLContext instance from the function create_ssl_connection_context
if USE_SSL_CONNECTION:
    SSL_CONTEXT = create_ssl_connection_context()
# There is no ssl connection context
else:
    print('\nNo SSL connection')


def retrieve_all_file_lines(path_to_file: str) -> List[str]:
    """
    Read all lines from the file specified by file_path.

    This function opens the file specified by the file_path, reads all lines from the file,
    and returns a list of these lines. The file is opened in read mode ('r') with UTF-8 encoding.

    Args:
        path_to_file (str): Path to the file. The file must exist and be accessible.

    Returns:
        List[str]: List of lines in the file. Each line is a string, and the list contains
        one string for each line in the file.

    Raises:
        FileNotFoundError: If the file specified by file_path does not exist.
        PermissionError: If the file specified by file_path cannot be opened
        due to insufficient permissions.
        IOError: If an I/O error occurs while reading the file.
    """
    try:
        # reading from the file
        with open(file=path_to_file, mode='r', encoding='utf-8') as f:
            # retrieves all lines in the file
            return f.readlines()

    except OSError as e:
        print(f'something went wrong check the file existence or permissions and try again: {e}')
        return []


def searching_string(path: str, search_string: str, reread: bool, algorithm_used: callable) -> bool:
    """
    Search for the exact string in the file using the specified algorithm.

    Args:
        path (str): Path to the file.
        search_string (str): String to search for.
        reread (bool): Whether to re-read the file on each query.
        algorithm_used (function): Search algorithm to use 
        (default is "linear" for linear search algorithm).

    Returns:
        bool: True if the string is found, False otherwise.

    Raises:
        Exception: If an error occurs while reading the file or the search algorithm is invalid.

    Global Variables:
        file_lines_present (List[str]): Global variable holding the list of lines in a file.
        current_algorithm (str): Global variable holding the name of the algorithm used.
    """
    # printing the name of the algorithm in use
    print('--------------------------------------------------------')
    print(f'\nDEBUG Algorithm: {str(algorithm_used).split()[1]}')
    # holding the list of lines in a file, and also I am suppressing for this reason
    global ALL_LINES  # pylint: disable=W0603
    # holds the True if the string is found and False if not or Exception occurs
    found_status: bool = False
    try:

        # if REREAD_ON_QUERY True reread the path afresh considering that it COULD change
        if reread:
            # using the list approach will be faster since retrieving the list
            # and then converting to it into a set will lead to poor performance
            # especially it is a repetitive operation due to rereading

            ALL_LINES = list(retrieve_all_file_lines(path))
        # no reread thus the best way to facilitate searching for preloaded files is Set
        # changing the list into a set that will contain only unique data without duplicates
        if ALL_LINES is None:
            ALL_LINES = {line.strip() for line in retrieve_all_file_lines(path)}
        # invocation of the search algorithm function
        found_status = algorithm_used(ALL_LINES, search_string)

    except ValueError as e:
        print(f"Error: Invalid algorithm type detected check the algorithm value.\n{e}")
        found_status = False
    # returning the status
    return found_status


def client_conn(connection: socket.socket, address: Tuple[str, int]):
    """
    Handle a client connection. This function is responsible for receiving
    a search query from a client,searching for the query in the file, 
    and sending a response back to the client. It also logs relevant information about
    the connection, search query, and execution time.

    Args:
        connection (socket.socket): The socket object representing the client connection.
        address (Tuple[str, int]): A tuple containing the client's IP address and port number.

    Returns:
        None

    Raises:
        Exception: If an error occurs while communicating with the client 
        or processing the search query. especially if the search algorithm is invalid or does
        not exist. i.e. not defined  in the search_algorithms.py file
    """

    # Record the start time before executing the search_string_present function
    start_time: float = time.time() * 1000  # milliseconds

    try:
        # The server strips any \x00 characters from the end of the payload it receives
        search_query = connection.recv(MAX_PAYLOAD_SIZE).strip(b'\x00').decode('utf-8')

        # Call the search_string_present method to check if the search query exists in the file
        # Pass the linear search algorithm as the search algorithm
        if searching_string(FILE_PATH, search_query, REREAD_ON_QUERY, algorithms['linear']):
            response = "STRING EXISTS\n"
        else:
            response = "STRING NOT FOUND\n"

        # Encode the response and send it to the client
        connection.sendall(response.encode('utf-8'))

        # Record the end time after executing the search_string_present function
        end_time: float = time.time() * 1000  # milliseconds

        # Generate a timestamp in the format (YYYY-MM-DD HH:MM:SS Day)
        date_stamp: str = datetime.today().strftime("%Y-%m-%d %H:%M:%S %A")

        # Print debug information about the search query, client IP, execution time, timestamp,
        # SSL status, search algorithm, and REREAD_ON_QUERY setting
        print(f"\nDEBUG: Search_query: {search_query}\n\nDEBUG IP: {address}")
        print(f"\nDEBUG Execution Time: {end_time - start_time:.2f} millisecond")
        print(f"\nDEBUG Timestamp: {date_stamp}\n\nDEBUG SSL: {USE_SSL_CONNECTION}")
        print(f"\nDEBUG REREAD_ON_QUERY: {REREAD_ON_QUERY}\n")
        print('----------------------------------------------------------------\n')
    # when the client is not running in SSL mode, the query string sent will be not decoded
    # this will lead to OS errors when server tries to decode thus OS Errors will be reported
    except OSError as oe:
        print(f'\ndecoding the client request failed: {oe} ')
    except KeyError as e:
        # Print an error message if an exception occurs while communicating with the client
        print(f"\n Error: Invalid search algorithm used check and try again: {e}")
        response = "STRING NOT FOUND\n"
        # Encode the response and send it to the client
        connection.sendall(response.encode('utf-8'))
    except UnicodeDecodeError as ud:
        print(f'\nfailed to decode client request, check your SSL authentication status:{ud}')
        print('\nclient request encoded when SSL is enabled, ensure server is using SSL\n')

    finally:
        # Close the client connection
        connection.close()


def server_configuration(port_number: int):
    """
    Start the server to listen for incoming connections from any available client.

    Args:
        port_number (int): Port number which the server will listen on.

    Returns:
        None

    The function initializes a TCP/IP socket for the server, binds it to the specified port number,
    and starts listening for incoming connections. It also handles SSL connections if enabled.
    For each client connection, it creates a new thread to handle the client's requests.
    """

    # Initialize a TCP/IP socket for the server
    socket_of_the_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server socket to the specified port number
    # Binding to 0.0.0.0 means the server will listen on all available network interfaces
    # This helps the server to accept connections not only from the localhost (127.0.0.1)
    # but also from other machines on the network
    socket_of_the_server.bind(('0.0.0.0', port_number))

    # Start listening for incoming connections
    # The backlog value of 5 defines the maximum number of pending connections
    # that can be present in the queue
    socket_of_the_server.listen(5)

    print(f"Server is Running and Listening on Port: {port_number}")

    while True:
        # Accept a client connection
        # This function will block until a client connects to the server
        # It returns a new socket object representing the client connection and
        # the client's IP address and port number
        client_sock, client_addr = socket_of_the_server.accept()

        # If SSL is enabled, wrap the client socket with an SSL connection
        if USE_SSL_CONNECTION:
            try:
                # Wrap the client socket with an SSL connection
                client_sock = SSL_CONTEXT.wrap_socket(client_sock, server_side=True)
            # ssl context  totally not created
            except NotImplementedError as e:
                print(f'\nError:SSL context not created; client sent invalid SSL files: {e}\n')
            # client is not using SSL connections while the server is
            except ssl.SSLError as err:
                print(f'\nclient is not running in SSL mode flag the server to no SSL:{err}')
        # Create a new thread to handle the client connection
        # The target function for the thread is client_connection_handling
        # The arguments for the target function are the client socket
        # and the client's IP address and port number
        client_thread = threading.Thread(target=client_conn, args=(client_sock, client_addr))

        # Start the thread to handle the client connection
        client_thread.start()


# Here  the program will be started for execution it's the entry point
if __name__ == "__main__":
    # run the server_configuration function as entry point to start the server
    server_configuration(PORT_NUMBER)
