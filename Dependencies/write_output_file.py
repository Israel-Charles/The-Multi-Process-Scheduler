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
