import sys

from Dependencies.data_structure import *
from Dependencies.write_output_file import *
from Dependencies.input_file_parsing import *
from Dependencies.generate_html_file import *

from Dependencies.Scheduler_Algorithms.sjf_scheduler import *
from Dependencies.Scheduler_Algorithms.fifo_scheduler import *
from Dependencies.Scheduler_Algorithms.lottery_scheduler import *
from Dependencies.Scheduler_Algorithms.round_robin_scheduler import *




# Main function that sets the flow of the program
def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Getting algoritm, its parameters, and the processes from the input file
    process_list, run_for, algorithm, quantum = parse_input_file(input_file)

    event_log = []  # Array of lines to print in the output file

    if algorithm == 'rr':
        event_log = round_robin_scheduler(process_list, run_for, quantum)
    elif algorithm == 'lottery':
        event_log = lottery_scheduling(process_list, run_for)
    elif algorithm == 'sjf':
        event_log = preemptive_sjf_scheduler(process_list, run_for)
    elif algorithm == 'fcfs':
        event_log = fifo_scheduler(process_list, run_for)    
        
    output_file = input_file.replace(".in", ".out")
    write_output_file(output_file, process_list, algorithm, quantum, event_log, run_for)
    
    html_file = input_file.replace(".in", "_out.html")
    generate_html_file(output_file, input_file, html_file)

if __name__ == "__main__":
    main()