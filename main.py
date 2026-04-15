import sys #importing sys to access arguments
import json #importing json to use json files
from metricsCalc import metrics

# normalize JSON keys/values: strip whitespace from keys and string values
def _normalize_value(val):
    if isinstance(val, dict):
        new = {}
        for k, v in val.items():
            new_k = k.strip().lower()
            new[new_k] = _normalize_value(v)
        return new
    if isinstance(val, list):
        return [_normalize_value(v) for v in val]
    if isinstance(val, str):
        s = val.strip()
        if s.isdigit():
            try:
                return int(s)
            except:
                return s
        try:
            f = float(s)
            return f
        except:
            return s
    return val

#function to load data
def load_data(file_name):
    input_dict = {}
    try:
        with open(file_name, "r") as input:
            data = input.read()
            input_dict = json.loads(data) # loading the data
            # normalize keys/values so whitespace does not mess it up
            input_dict = _normalize_value(input_dict)
    except FileNotFoundError:
        print("File was not found")
        exit()
    return input_dict

#function to provide output
def output_data(results): #assuming results is a dictionary
    # json with indentation fpr readability
    output_data = json.dumps(results, indent=4)
    print(output_data)

#All algorithm methods

## Author: Serge Rumyantsev
## Date: April 15, 2026

def fifo(data):
    
    #extract the list of jobs from input data
    #each job has: pid, arrival, burst, priority
    jobs = data["jobs"]
    
    #sort jobs by arrival time (FIFO)
    #for same arrival time, sort by PID lexicographically
    jobs_sorted = sorted(jobs, key=lambda x: (x["arrival"], x["pid"]))
    
    #gantt chart will store execution segments
    #each segment: {"pid": "A", "start": 0, "end": 6}
    gantt = []
    
    #track current CPU time as we simulate execution
    current_time = 0
    
    #dictionaries to store metrics for each process
    turnaround = {}  #completion time - arrival time
    waiting = {}     #start time - arrival time
    
    #process each job in FIFO order
    for job in jobs_sorted:
        #if CPU is idle (current_time < next job's arrival),
        #jump forward to when the next job arrives
        #handles gaps between processes
        if current_time < job["arrival"]:
            current_time = job["arrival"]
        
        #record when process starts executing
        start = current_time
        
        #calculate when it finishes (start + burst time)
        #Non-preemptive: runs entire burst at once
        end = current_time + job["burst"]
        
        #add this execution segment to Gantt chart
        gantt.append({
            "pid": job["pid"], 
            "start": start, 
            "end": end
        })
        
        #calculate turnaround time: time from arrival to completion
        #finish time - arrival time
        turnaround[job["pid"]] = end - job["arrival"]
        
        #calculate waiting time (time spent in ready queue)
        #start time - arrival time
        waiting[job["pid"]] = start - job["arrival"]
        
        #advance current time to the end of this process
        current_time = end
    
    #calculate average turnaround time across all processes
    avg_turnaround = sum(turnaround.values()) / len(turnaround)
    
    #calculate average waiting time across processes
    avg_waiting = sum(waiting.values()) / len(waiting)
    
    #return results in JSON format
    return {
        "policy": "FIFO",    #Algorithm name
        "gantt": gantt,                       
        "metrics": {
            "turnaround": turnaround, #per-process turnaround times
            "waiting": waiting,       #per-process waiting times
            "avg_turnaround": round(avg_turnaround, 2),  #average (2 decimals)
            "avg_waiting": round(avg_waiting, 2)  #average (2 decimals)
        }
    }


def sjf(input_dict):
    results = {
        "policy": "SJF",
        "gantt": []
    }
    # Make a copy of the original jobs for metrics
    input_dict_jobs = []
    for job in input_dict["jobs"]:
        input_dict_jobs.append(job.copy())

    current_time = 0

    # Keep scheduling until all jobs are done
    while len(input_dict["jobs"]) > 0:
        available_jobs = []

        # Find all jobs that have arrived by current_time
        for job in input_dict["jobs"]:
            if job["arrival"] <= current_time:
                available_jobs.append(job)

        # If no job has arrived yet, jump to the next arrival time
        if len(available_jobs) == 0:
            next_job = input_dict["jobs"][0]
            for job in input_dict["jobs"]:
                if job["arrival"] < next_job["arrival"]:
                    next_job = job
            current_time = next_job["arrival"]
            continue

        # Pick the shortest available job
        next_process = available_jobs[0]
        for job in available_jobs:
            if job["burst"] < next_process["burst"]:
                next_process = job
            elif job["burst"] == next_process["burst"]:
                # Tie-breaker: earlier arrival first
                if job["pid"] < next_process["pid"]:
                    next_process = job

        start_time = current_time
        end_time = start_time + next_process["burst"]

        results["gantt"].append({
            "pid": next_process["pid"],
            "start": start_time,
            "end": end_time
        })

        current_time = end_time

        # Remove scheduled job from the job list
        for job in input_dict["jobs"]:
            if job["pid"] == next_process["pid"]:
                input_dict["jobs"].remove(job)
                break

    results["metrics"] = metrics(input_dict_jobs, results["gantt"])
    return results

def round_robin(input_dict):
    results = {
        # policy name
        "policy": "RR",
        # gant assigned as empty arrao
        "gantt": []
    }

    # make a copy of the original jobs for metrics
    input_dict_jobs = []
    for job in input_dict["jobs"]:
        input_dict_jobs.append(job.copy())

    # jobs[] array is a working job list with remaining times
    jobs = []
    for job in input_dict["jobs"]:
        jobs.append({
            "pid": job["pid"],
            "arrival": job["arrival"],
            "burst": job["burst"],
            "remaining": job["burst"]
        })

    # sort by arrival and tie breaker smallest pid for ordering
    jobs.sort(key=lambda j: (j["arrival"], j["pid"]))

    #set quantum value
    quantum = input_dict.get("quantum", 1)
    #simulated time starting at 0 
    current_time = 0
    #ready_queue for jobs that have arrived but not finished
    ready_queue = []

    # run until all jobs are finished, when jobs array AND ready_queue are empty
    while jobs or ready_queue:
        # add jobs that have just arrived now at the current_time, to end of queue
        while jobs and jobs[0]["arrival"] <= current_time:
            ready_queue.append(jobs.pop(0))
        # no jobs in ready_queue, but jobs will come later
        if not ready_queue:
            # skip to the next arrival 
            next_job = jobs.pop(0)
            # update time to match
            current_time = next_job["arrival"]
            # add to ready queue
            ready_queue.append(next_job)

        # take the next job from the ready queue
        current = ready_queue.pop(0)
        start_time = current_time
        run_time = min(quantum, current["remaining"])
        end_time = start_time + run_time

        results["gantt"].append({
            "pid": current["pid"],
            "start": start_time,
            "end": end_time
        })

        current_time = end_time
        current["remaining"] -= run_time

        # add any jobs that arrived during this slice
        while jobs and jobs[0]["arrival"] <= current_time:
            ready_queue.append(jobs.pop(0))

        # ff the job isnt finished, requeue it
        if current["remaining"] > 0:
            ready_queue.append(current)

    results["metrics"] = metrics(input_dict_jobs, results["gantt"])
    return results

# @author Kayden Ions
# @date 04/08/2026

# Non-preemptive priority scheduling.
# 'Higher priority' directly correlated to 'higher number'
def priority(input_dict):
    # Result dictionary object
    results = {
        # Assign the policy name
        "policy": "PRIORITY",
        # Assign the gant property to an empty array
        "gantt": [],
    }

    jobs = input_dict["jobs"].copy()
    original_jobs = input_dict["jobs"].copy()
    # Loop while the given scheduling policy object has jobs within the job array
    # In this case, we will be removing the job from the input dictionary job array as they are assigned to the result gantt array
    while len(jobs) > 0:
        # Get current time
        if len(results["gantt"]) == 0:
            current_time = 0
        else:
            current_time = results["gantt"][-1]["end"]

        nextProcess = None
        # Loop through each job in the input dictionary jobs array
        for job in jobs:
            if job["arrival"] <= current_time:
                # Only when the current job has an earlier or equal arrival time and a higher priority (lower priority value)...
                if (nextProcess == None or job["priority"] > nextProcess["priority"] or (job["priority"] == nextProcess["priority"] and job["arrival"] < nextProcess["arrival"])):
                    # ... the next process is assigned the current job as it is higher priority or earlier arrival time
                    nextProcess = job
        # After the for loop, find the starting value of the current process and ensure that if the next process has value none, select the next arriving job
        if nextProcess is None:
            nextProcess = min(jobs, key=lambda x: x["arrival"])
        
        # If this current process is the first process then assign the starting value the the arrival of the process
        if (len(results["gantt"]) == 0):
            currentStart = nextProcess["arrival"]
        # Otherwise, if the arrival time of the current process is earlier than the end of the previous process..
        elif (nextProcess["arrival"] <= results["gantt"][len(results["gantt"]) - 1]["end"]):
            # Assign the start time to the end time of the previous process
            currentStart = results["gantt"][len(results["gantt"]) - 1]["end"]
        else:
            # If all else, assign the start time to the arrival time of the current process
            currentStart = nextProcess["arrival"]
        
        # After figuring out the starting time, append the following to the resulting gantt array
        results["gantt"].append({
            # The process id
            "pid": nextProcess["pid"],
            # The process' starting time
            "start": currentStart,
            # The process' end time which is the total time it takes for the process to finish
            # This is the easiest way to tell whether an algorithm is non-preemptive
            "end": currentStart + nextProcess["burst"]         
        })
        
        jobs.remove(nextProcess)
        
    results["metrics"] = metrics(original_jobs, results["gantt"])  
    # Return the results  
    return results

file_name = sys.argv[1] #the input filename

input_dict = load_data(file_name) #calling the function
results = {} #dict for results
if(input_dict["policy"].upper()=="FIFO"):
    results = fifo(input_dict)
elif(input_dict["policy"].upper()=="SJF"):
    results = sjf(input_dict)
elif(input_dict["policy"].upper()=="RR"):
    results = round_robin(input_dict)
elif(input_dict["policy"].upper()=="PRIORITY"):
    results = priority(input_dict)
else:
    print("It's not part of our policies")


output_data(results) #outputing data