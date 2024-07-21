""" 
This module has been designed to facilitate easier way for measuring
the performance of various search algorithms by generating text files that
are saved in the data directory

"""

# static typing
from typing import List

# for random number generation
import random

# for IO operations
import os


def generate_text_files(sizes: List[int]) -> bool:
    """
    This function generates a list of text files that will be used for testing performance
    of search algorithms across different file sizes. The files are saved in the data directory 
    with a .txt extension. 
    You can use these text files to perform search queries for different file sizes. 
    
    Args:
        sizes (list[int]): A list of text file sizes to generate, e.g., [1000, 10000, 250000].

    Returns:
        bool: True if all the list of files are generated,
        or if all files are appropriately handled.
        bool: False if all the list of files are not generated 
        or if any of the files are not generated.
    """
    results = True  # Default to True, only set to False on encountering an unhandled error

    try:
        # Create the directory if it doesn't exist
        os.makedirs(f'{os.getcwd()}/data', exist_ok=True)

        for size in sizes:
            # List of file lines as content of the file
            lines = [f'{i};{random.randrange(size)};{random.randrange(size)};\n' for i in range(size)]

            try:
                # Write the lines to the file
                with open(f'{os.getcwd()}/data/{size // 1000}k.txt', 'w', encoding='utf-8') as f:
                    f.writelines(lines)
            except FileExistsError as e:
                print(f'File already exists: {e}')
            except OSError as e:
                results = False
                print(f'Error writing file data: {e}')
    except TypeError as e:
        print(f'Invalid data type passed as argument: {e}')
        results = False

    return results


if __name__ == '__main__':
    # start the  generation process. You can pass any number of argument
    # and the file size corresponding to the number will be generated and then
    # saved to the directory named data in the project's root directory
    generate_text_files([10000, 100000, 250000, 500000, 1000000])
