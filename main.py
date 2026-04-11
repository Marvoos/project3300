import sys #importing sys to access arguments
import json #importing json to use json files
from priority_scheduling import priority
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
def fifo(input_dict):
    results = {}
    #write round robin algorithm here
    return results

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