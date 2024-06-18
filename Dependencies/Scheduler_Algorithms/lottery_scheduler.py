import random

# Function for the Lottery Scheduler Algorithm
def lottery_scheduling(processes, time_units):
    """
    Simulates a lottery scheduling algorithm over a specified number of time units.

    :param processes: List of Process instances
    :param time_units: Number of time units the scheduler should run
    :return: List of strings representing the event log of the scheduler
    """
    event_log = []
    current_time = 0
    active_processes = processes[:]  # Keeps only active (not finished) processes
    last_selected_process = None  # Tracks the last selected process
    tick_events = {}  # Dictionary to hold events for each tick

    def calculate_total_tickets():
        # Only active processes are considered for ticket assignment
        return sum(max(1, 10 - p.remaining_burst_time) for p in active_processes if p.arrival_time <= current_time)
    
    while current_time < time_units:
        total_tickets = calculate_total_tickets()
        current_process = None

        # Initialize the list of events for the current tick if not already initialized
        if current_time not in tick_events:
            tick_events[current_time] = []

        # Check and log arrivals at the current time
        for process in processes:
            if process.arrival_time == current_time:
                tick_events[current_time].append(f"Time {current_time} : {process.name} arrived")

        if total_tickets > 0:
            lottery = random.randint(1, total_tickets)
            current_ticket = 0

            # Lottery selection process
            for process in active_processes:
                if process.arrival_time <= current_time:
                    current_ticket += max(1, 10 - process.remaining_burst_time)
                    if current_ticket >= lottery:
                        current_process = process
                        break

            # Process execution and logging
            if current_process:
                if current_process.remaining_burst_time > 0:
                    if last_selected_process != current_process:
                        if current_process.response_time == -1:
                            current_process.response_time = 0  # Set response time to 0 if it is -1
                        tick_events[current_time].append(f"Time {current_time} : {current_process.name} selected (burst {max(0, current_process.remaining_burst_time)})")
                    last_selected_process = current_process

                    current_process.remaining_burst_time -= 1

                    # Log when a process finishes
                    if current_process.remaining_burst_time == 0:
                        current_process.set_finish_time(current_time + 1)
                        tick_events[current_time + 1] = tick_events.get(current_time + 1, []) + [f"Time {current_time + 1} : {current_process.name} finished"]
                        active_processes.remove(current_process)  # Remove finished process from active list
                        last_selected_process = None  # Reset last selected process as it has finished
        else:
            # Log idle without conditionally checking other events
            tick_events[current_time].append(f"Time {current_time} : Idle")

        current_time += 1
    
    # Compile events from tick_events dictionary into event_log list
    for time in sorted(tick_events.keys()):
        event_log.extend(tick_events[time])

    return event_log