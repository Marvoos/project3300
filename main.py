import sys #importing sys to access arguments
import json #importing json to use json files
from priority_scheduling import priority
from metricsCalc import metrics

#function to load data
def load_data(file_name):
    input_dict = {}
    try:
        with open(file_name, "r") as input:
            data = input.read()
            input_dict = json.loads(data)#loading the data
    except FileNotFoundError:
        print("File was not found")
        exit()
    return input_dict

#function to provide output
def output_data(results): #assuming results is a dictionary
    output_data = json.dumps(results)
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
    results = {}
    #write round robin algorithm here
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