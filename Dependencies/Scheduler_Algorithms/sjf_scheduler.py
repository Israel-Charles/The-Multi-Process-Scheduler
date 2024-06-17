import heapq

# Function for the SJF Scheduler Algorithm  
def preemptive_sjf_scheduler(process_list, run_for):
    """
    Simulate the Preemptive Shortest Job First (SJF) scheduling algorithm, ensuring proper event order.
    
    Parameters:
    process_list (list of Process): List of processes to be scheduled.
    run_for (int): Total time units to run the simulation.

    Returns:
    list of str: Event log detailing the scheduling process.
    """
    current_time = 0
    tick_events = {}  # Dictionary to store events by tick
    ready_queue = []  # Initialize the ready queue as a min-heap
    last_process = None  # Track the last process that was running

    heapq.heapify(ready_queue)
    process_queue = sorted(process_list, key=lambda p: p.arrival_time)

    while current_time < run_for:
        if current_time not in tick_events:
            tick_events[current_time] = []

        # Check and handle arrivals first to ensure they are logged before finishes
        while process_queue and process_queue[0].arrival_time <= current_time:
            process = process_queue.pop(0)
            heapq.heappush(ready_queue, (process.remaining_burst_time, process))
            tick_events[current_time].append(f"Time {current_time} : {process.name} arrived")

        if not ready_queue:
            tick_events[current_time].append(f"Time {current_time} : Idle")
            current_time += 1
            continue

        # Process the queue and handle execution
        _, current_process = heapq.heappop(ready_queue)

        if last_process != current_process:
            if current_process.start_time == -1:
                current_process.start_time = current_time
            current_process.response_time = max(current_process.response_time, current_time - current_process.arrival_time)
            tick_events[current_time].append(f"Time {current_time} : {current_process.name} selected (burst {current_process.remaining_burst_time})")
        last_process = current_process

        # Simulate execution for 1 time unit
        current_time += 1
        if current_time not in tick_events:
            tick_events[current_time] = []
        current_process.remaining_burst_time -= 1

        # Check for completion within the same tick
        if current_process.remaining_burst_time == 0:
            current_process.set_finish_time(current_time)
            tick_events[current_time].append(f"Time {current_time} : {current_process.name} finished")
            last_process = None
        else:
            # Re-add the process to the ready queue
            heapq.heappush(ready_queue, (current_process.remaining_burst_time, current_process))

    # Compile the final event log from the tick_events dictionary
    event_log = []
    for time in sorted(tick_events.keys()):
        event_log.extend(tick_events[time])

    return event_log