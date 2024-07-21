""" 
This module implements the visualization aspect of the performance of the search algorithms
used in this project. This graph helps for easier decision-making and comparison.
As per the documentation of this module, the tests results below were the most appropriate
average performance.

"""
# Library for visualization
import matplotlib.pyplot as plt

# search algorithms
algorithms = ["Linear", "Depth_FS", "Hash_Table", "Binary"]

# file sizes
file_sizes = [10000, 100000, 200000, 500000, 1000000]

# Execution times in milliseconds
# REREAD_ON_QUERY = True

execution_times = [
    [1.85, 20.50, 40.18, 98.40, 188.54],  # Linear
    [2.10, 24.00, 40.85, 115.46, 225.13],  # Depth_FS
    [2.40, 25.50, 65.75, 124.28, 244.60],  # Breadth_FS
    [3.05, 38.74, 105.63, 206.11, 410.75],  # Hash_Table
    [4.50, 75.20, 200.42, 450.30, 900.20],  # Binary
]

# line graph visualization plot
# defining the size of the graph in terms of height and width
plt.figure(figsize=(12, 6))
for algorithm, times in zip(algorithms, execution_times):
    plt.plot(file_sizes, times, marker='o', linestyle='-', label=algorithm)

# the X axis labeling
plt.xlabel("File Size (bytes)")
# The Y axis labeling
plt.ylabel("Average Time (milliseconds)")
# Title at the Top of The graph
plt.title("Comparison of File Search Algorithm Performance")

# Customize the plot
# the ticks marks for X axis will be file sizes in K(kilobytes)
plt.xticks(ticks=file_sizes, labels=[f"{size // 1000}K" for size in file_sizes])
# this ensures that the labeling are drawn and shown when plotting
plt.legend()
# grid squares
plt.grid(True)

# Display the graph
plt.tight_layout()

if __name__ == '__main__':
    # run the main program and show the benchmark results in graphical format
    plt.show()
