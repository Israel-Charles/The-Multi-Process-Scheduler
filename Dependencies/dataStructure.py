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