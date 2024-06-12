import sys

from inputFileParsing import *
from dataStructure import *
from SchedulerAlgorithms.roundRobinScheduler import *
from writeOutputFile import *

# Main function that sets the flow of the program
def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Getting algoritm, its parameters, and the processes from the input file
    process_list, run_for, algorithm, quantum = parse_input_file(input_file)

    event_log = []  # Array of lines to print in the output file

    # Uncomment those as their respective algorithm is completed
    """
    if algorithm == 'fcfs':
        event_log = fifo_scheduler(process_list, run_for)
    elif algorithm == 'sjf':
        event_log = preemptive_sjf_scheduler(process_list, run_for)
    """

    if algorithm == 'rr':
        event_log = round_robin_scheduler(process_list, run_for, quantum)
        
    output_file = input_file.replace(".in", ".out")
    write_output_file(output_file, process_list, algorithm, quantum, event_log, run_for)
    

if __name__ == "__main__":
    main()