import random

def lottery_scheduling(processes, time_units):
    """
    Simulates a lottery scheduling algorithm over a specified number of time units.

    :param processes: List of Process instances
    :param time_units: Number of time units the scheduler should run
    :return: List of strings representing the event log of the scheduler
    """
    event_log = []
    current_time = 0
    process_queue = processes[:]
    
    # Assign tickets to each process; fewer burst_time means more tickets
    total_tickets = 0
    tickets = {}
    for process in processes:
        # Assuming here ticket count is inversely proportional to burst_time + 1 to avoid division by zero
        tickets[process.name] = max(1, 10 - process.burst_time)
        total_tickets += tickets[process.name]
    
    # Main scheduling loop
    while current_time < time_units:
        # Check for new arrivals
        for process in processes:
            if process.arrival_time == current_time:
                event_log.append(f"Time {current_time} : {process.name} arrived")
        
        # Select process based on lottery
        if total_tickets > 0:
            lottery = random.randint(1, total_tickets)
            current_ticket = 0
            for process in process_queue:
                current_ticket += tickets[process.name]
                if current_ticket >= lottery:
                    current_process = process
                    break

            # Log process selection
            event_log.append(f"Time {current_time} : {current_process.name} selected (burst {current_process.remaining_burst_time})")
            
            # Simulate process execution for one time unit
            current_process.remaining_burst_time -= 1
            if current_process.start_time == -1:
                current_process.set_start_time(current_time)
            
            # Check if process finishes
            if current_process.remaining_burst_time == 0:
                current_process.set_finish_time(current_time + 1)
                event_log.append(f"Time {current_time} : {current_process.name} finished")
                process_queue.remove(current_process)
                total_tickets -= tickets[current_process.name]
        else:
            # If no tickets are available, system is idle
            event_log.append(f"Time {current_time} : Idle")
        
        # Move to the next time unit
        current_time += 1
    
    return event_log