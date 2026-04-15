# PROJECT 3300

CPU scheduling policies simulation using python and JSON

## Group Members

| Group Member    | Responsibilities                                                              |
|--------------   |------------------                                                             |
|Kayden Ions      | Priority Scheduling and metrics calculation function.                         |
|Liana Bell       | Round Robin scheduling and output normalization.                              |
|Nashwan Masho    | Shortest Job first scheduling.                                                |
|Nazifa Tahsin    | Input and output functionality and JSON input files.                          |
|Serge Rumyantsev | First in first out scheduling.                                                |

## How to Run?

Use the following commands:

### On windows

__To output to a json file:__ ```python main.py input.json > output.json```

__To output to the console:__ ```python main.py input.json```

### On other platforms

__To output to a json file:__ ```python3 main.py input.json > output.json```

__To output to the console:__ ```python3 main.py input.json```

## How Each Policy Works

__Priority Scheduling (non-preemptive):__ Retrieves the highest priority or the first arrived in the list of jobs and executes each job until finished. Does not preemptively stop any processes if a new process is higher priority, rather, it picks from a list of already arrived and chooses the highest priority to process next.

__Round Robin:__ Utilizes a fixed quantum along with preemption to allow for a more interactive experience. Round Robin chooses the arrived from the list of jobs and runs each in an interval equal to the quantum. These intervals cycle through each arrived process (e.g. A, B, C, A, B, C, A, C, C) in bursts until the processes are complete. If we have our quantum = 2 and A runs for a length of six, then process A will run three times to complete.

__Shortest Job First:__ As apposed to shortest remaining time first, the policy, shortest job first does not use __preemption__. Shortest job first processes the shortest burst time first or the first arrived first. The shortest job first without preemption assumes that all jobs will arrive at the same time. If this is not the case, it behaves like a first-in-first-out algorithm until the algorithm can differentiate burst times of already arrived jobs.

__First-in-first_out:__ This policy is the simplest of the four. If a job arrives first, it is processes first until completion. Once completed, the next job is run and so on. If two jobs arrive at the same time, this policy uses a tie-breaking mechanism specific to the system.
