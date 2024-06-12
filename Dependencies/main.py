import sys

from inputFileParsing import *
from dataStructure import *

def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_list, run_for, algorithm, quantum = parse_input_file(input_file)

    event_log = []

    if algorithm == 'fcfs':
        event_log = fifo_scheduler(process_list, run_for)
    elif algorithm == 'sjf':
        event_log = preemptive_sjf_scheduler(process_list, run_for)
    elif algorithm == 'rr':
        event_log = round_robin_scheduler(process_list, run_for, quantum)

    output_file = input_file.replace(".in", ".out")
    with open(output_file, 'w') as file:
        file.write(f"{len(process_list)} processes\n")
        file.write(f"Using {algorithm.upper()}\n")
        if algorithm == 'rr':
            file.write(f"Quantum {quantum}\n")
        for event in event_log:
            file.write(event + "\n")
        file.write(f"Finished at time {run_for}\n")
        for process in process_list:
            if process.finish_time == -1:
                file.write(f"{process.name} did not finish\n")
            else:
                file.write(f"{process.name} wait {process.waiting_time} turnaround {process.turnaround_time} response {process.response_time}\n")


if __name__ == "__main__":
    main()