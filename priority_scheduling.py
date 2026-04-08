from metricsCalc import metrics
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
    input_dict_jobs = []
    for job in input_dict["jobs"]:
        input_dict_jobs.append(job)
        
    
    # Loop while the given scheduling policy object has jobs within the job array
    # In this case, we will be removing the job from the input dictionary job array as they are assigned to the result gantt array
    while len(input_dict["jobs"]) > 0:
        # Next process will be equal to the first in the jobs array
        nextProcess = input_dict["jobs"][0]

        # Loop through each job in the input dictionary jobs array
        for job in input_dict["jobs"]:
            # Only when the current job has an earlier or equal arrival time and a higher priority (lower priority value)...
            if (job["arrival"] <= nextProcess["arrival"] and job["priority"] < nextProcess["priority"]):
                # ... the next process is assigned the current job as it is higher priority or earlier arrival time
                nextProcess = job
        
        # After the for loop, find the starting value of the current process.
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
        
        # Afterwards, search through each job within the input object and remove the corresponding job with the id equal to the next process' id
        for job in input_dict["jobs"]:   
            if (job["pid"] == nextProcess["pid"]): 
                input_dict["jobs"].remove(job)
        
    results["metrics"] = metrics(input_dict_jobs, results["gantt"])  
    # Return the results  
    return results