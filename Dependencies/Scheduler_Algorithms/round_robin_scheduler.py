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