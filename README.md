# The-ChatGPT-Process-Scheduler
This software should implement 4 process scheduling algorithms: FIFO (First In, First Out), Pre-emptive Shortest Job First (SJF), Round Robin (RR), and Linux's CFS (Completely Fair Scheduler), — using ChatGPT in Python. The implementation should be able to simulate the scheduling of multiple processes under each algorithm and calculate their turnaround time, response time, and wait time. The following key components are required:

- Process Data Structure: Representing each process with its arrival time, execution time, and status.
- Scheduler Functions: One function for each algorithm to handle a list of processes and implement the respective scheduling logic.
- Time Slice Parameter: A Q-value for the Round Robin algorithm to determine the maximum time a process can run before being preempted.
- Metric Calculation Functions: Functions to compute turnaround time, waiting time, and response time for each process.


Input File Format
The input file will have the following format:
```
processcount <number of processes>
runfor <total number of time units to run>
use <algorithm> [quantum <time units>] (if using Round Robin)
process name <name> arrival <arrival time> burst <burst time>
...
end
```

Output File Format
The output file will document the events and results as follows:
```
<Number of processes> processes
Using <algorithm that is being used>
[Quantum <time units> (if using Round Robin)]
Time <time unit>: <event status>
...
Time <final time unit>:  <event status>
Finished at time <total time units>

<process name> wait <waiting time> turnaround <turnaround time> response <response time>
...
[<process name> did not finish (if there is a process that did not finish within the allocated time)]
...
```

Error Handling
Errors should be handled gracefully with specific messages:
  - Missing parameter: "Error: Missing parameter <parameter>"
  - Missing quantum for Round Robin: "Error: Missing quantum parameter when use is 'rr'"
  - No input file: "Usage: scheduler-gpt.py <input file>"

Deliverables
  - Individual Prompts and Iterations: Each team member provides their prompts and iteration history.
  - Final Submission: The best result from the team, both in code and in the final conversation, with comments listing team members.
  - Final Report: A detailed evaluation of the AI-generated code, including correctness, efficiency, readability, completeness, innovation, and overall quality.
