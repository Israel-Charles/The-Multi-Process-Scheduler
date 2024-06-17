import sys
from Dependencies.data_structure import *

"""
This file contain the file parsing function and is dependent of the file 'ProcessDataStructure' that has
the data structure of the Processes
"""

# Function that takes in the input file and parse in the data of the file
def parse_input_file(file_path):
    """
    Parses the input file to extract process details and scheduling parameters.

    :param file_path: Path to the input file
    :return: Tuple (process_list, run_for, algorithm, quantum) if parsing is successful, otherwise prints an error and exits.
    """
    process_list = []
    process_count = None
    run_for = None
    algorithm = None
    quantum = None

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: Input file not found.")
        sys.exit(1)

    for line in lines:
        parts = line.split()
        if not parts:
            continue

        if parts[0] == "processcount":
            process_count = int(parts[1])
        elif parts[0] == "runfor":
            run_for = int(parts[1])
        elif parts[0] == "use":
            algorithm = parts[1].lower()
            if algorithm not in ['fcfs', 'sjf', 'rr']:
                print("Error: Invalid scheduling algorithm.")
                sys.exit(1)
        elif parts[0] == "quantum":
            if algorithm == 'rr':
                quantum = int(parts[1])
        elif parts[0] == "process":
            if parts[1] != "name" or parts[3] != "arrival" or parts[5] != "burst":
                print("Error: Invalid process specification.")
                sys.exit(1)
            name = parts[2]
            arrival = int(parts[4])
            burst = int(parts[6])
            process_list.append(Process(name, arrival, burst))
        elif parts[0] == "end":
            break

    # Check for missing required parameters
    if process_count is None:
        print("Error: Missing parameter for 'processcount'.")
        sys.exit(1)
    if run_for is None:
        print("Error: Missing parameter for 'runfor'.")
        sys.exit(1)
    if algorithm is None:
        print("Error: Missing parameter for 'use'.")
        sys.exit(1)
    if algorithm == 'rr' and quantum is None:
        print("Error: Missing 'quantum' parameter when use is 'rr'.")
        sys.exit(1)
    if len(process_list) != process_count:
        print("Error: Number of processes does not match 'processcount'.")
        sys.exit(1)

    return process_list, run_for, algorithm, quantum