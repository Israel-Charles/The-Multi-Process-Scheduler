import sys

# Data Structure of the processes. Used throughout the program to represent each process
class Process:
    def __init__(self, name, arrival_time, burst_time):
        """
        Initializes a new process with the given parameters. Some parameters are initialized 
        to -1 to indicate that the process has not yet started or not yet finished
        Any counter is initialized to 0

        :param name: The name of the process (string)
        :param arrival_time: The time at which the process arrives in the ready queue (int)
        :param burst_time: The total CPU burst time required by the process (int)
        """
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_burst_time = burst_time      # Time remaining for process execution
        self.start_time = -1                        # Time when the process starts execution 
        self.finish_time = -1                       # Time when the process finishes execution
        self.waiting_time = 0                       # Total waiting time in the ready queue
        self.turnaround_time = 0                    # Total time from arrival to completion
        self.response_time = -1                     # Time from arrival to first execution

    def update_metrics(self, current_time):
        """
        Updates the process metrics: turnaround time, waiting time, and response time.

        :param current_time: The current time in the scheduler simulation
        """
        self.turnaround_time = current_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time
        if self.start_time != -1:
            self.response_time = self.start_time - self.arrival_time

    def set_start_time(self, start_time):
        """
        Sets the start time of the process if it hasn't started yet.

        :param start_time: The time when the process starts execution
        """
        if self.start_time == -1:
            self.start_time = start_time

    def set_finish_time(self, finish_time):
        """
        Sets the finish time of the process and updates the metrics.

        :param finish_time: The time when the process finishes execution
        """
        self.finish_time = finish_time
        self.update_metrics(finish_time)

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

# Function that writes the output file
def write_output_file(output_file, process_list, algorithm, quantum, event_log, run_for):
    """
    Write the scheduling results to an output file.
    
    Parameters:
    output_file (str): The name of the output file.
    process_list (list of Process): List of processes that were scheduled.
    algorithm (str): The scheduling algorithm used.
    quantum (int): Time slice for Round Robin scheduling (if applicable).
    event_log (list of str): Event log detailing the scheduling process.
    run_for (int): Total time units the simulation ran.
    """
    with open(output_file, 'w') as file:
        file.write(f"{len(process_list)} processes\n")
        
        if algorithm == 'fcfs':
            file.write(f"Using First-Come First-Served\n")
        elif algorithm == 'sjf':
            file.write(f"Using Preemptive Shortest Job First\n")
        elif algorithm == 'rr':
            file.write(f"Using Round-Robin\n")
            
        if algorithm == 'rr':
            file.write(f"Quantum {quantum}\n")
        
        file.write("\n")
        
        for event in event_log:
            file.write(event + "\n")
        file.write(f"Finished at time {run_for}\n\n")
        
        for process in process_list:
            if process.finish_time == -1:
                file.write(f"{process.name} did not finish\n")
            else:
                file.write(f"{process.name} wait {process.waiting_time} turnaround {process.turnaround_time} response {process.response_time}\n")


# Round-Robin Scheduler Algorithm
def round_robin_scheduler(process_list, run_for, quantum):
    """
    Simulate the Round Robin scheduling algorithm.
    
    Parameters:
    process_list (list of Process): List of processes to be scheduled.
    run_for (int): Total time units to run the simulation.
    quantum (int): Time slice for Round Robin scheduling.

    Returns:
    list of str: Event log detailing the scheduling process.
    """
    current_time = 0                                # Initialize the current time
    event_log = []                                  # Initialize the event log
    ready_queue = []                                # Initialize the ready queue

    # Sort processes by arrival time
    process_queue = sorted(process_list, key=lambda p: p.arrival_time)

    while current_time < run_for and (process_queue or ready_queue):

        # Add processes to the ready queue as they arrive
        while process_queue and process_queue[0].arrival_time <= current_time:
            process = process_queue.pop(0)
            ready_queue.append(process)
            event_log.append(f"Time {current_time} : {process.name} arrived")

        if not ready_queue:
            # If no process is ready, CPU is idle
            event_log.append(f"Time {current_time} : Idle")
            current_time += 1
            continue

        # Get the next process from the ready queue
        current_process = ready_queue.pop(0)
        
        # Log process selection
        if current_process.start_time == -1:
            current_process.set_start_time(current_time)
        event_log.append(f"Time {current_time} : {current_process.name} selected (burst {current_process.remaining_burst_time})")
        
        # Determine the time slice for the current process
        execution_time = min(quantum, current_process.remaining_burst_time)

        # Simulate the execution of the process in smaller time increments to check for new arrivals
        for _ in range(execution_time):
            current_time += 1
            current_process.remaining_burst_time -= 1

            # Check for new arrivals during the execution
            while process_queue and process_queue[0].arrival_time <= current_time:
                process = process_queue.pop(0)
                ready_queue.append(process)
                event_log.append(f"Time {current_time} : {process.name} arrived")

            if current_process.remaining_burst_time == 0:
                break
        
        # Log process completion or re-queue if not finished
        if current_process.remaining_burst_time == 0:
            current_process.set_finish_time(current_time)
            event_log.append(f"Time {current_time} : {current_process.name} finished")
        else:
            ready_queue.append(current_process)
        
        # Check for new arrivals at the end of the time slice
        while process_queue and process_queue[0].arrival_time <= current_time:
            process = process_queue.pop(0)
            ready_queue.append(process)
            event_log.append(f"Time {current_time} : {process.name} arrived")

    # Fill the remaining time with idle events if simulation time is not exhausted
    while current_time < run_for:
        event_log.append(f"Time {current_time} : Idle")
        current_time += 1

    return event_log
    

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