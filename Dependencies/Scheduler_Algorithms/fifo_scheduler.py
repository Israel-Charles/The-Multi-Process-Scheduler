
# Function for the FIFO scheduler algorithm    
def fifo_scheduler(process_list, run_for):
    current_time = 0
    event_log = []
    process_queue = sorted(process_list, key=lambda p: p.arrival_time)
    while current_time < run_for and process_queue:
        current_process = process_queue.pop(0)
        if current_time < current_process.arrival_time:
            event_log.append(f"Time {current_time} : Idle")
            current_time = current_process.arrival_time
        
        current_process.set_start_time(current_time)
        event_log.append(f"Time {current_time} : {current_process.name} selected (burst {current_process.burst_time})")
        current_time += current_process.burst_time
        current_process.finish_time = current_time
        current_process.update_metrics(current_time)
        event_log.append(f"Time {current_time} : {current_process.name} finished")
    
    while current_time < run_for:
        event_log.append(f"Time {current_time} : Idle")
        current_time += 1
    
    return event_log
