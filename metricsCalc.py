# Metric function with two parameters.
# @param1: <type array(dict(pid, arrival, burst, priority))> - Consists of an array of all jobs in the inital job query
# @param2: <type array(dict(pid, start, end))> - Consists of an array of the corresponding jobs in gantt form. 
def metrics(input_jobs, gantt_jobs):
    # Initialize both average turnaround and average waiting to 0
    averageTurnaround = 0
    averageWaiting = 0
    # Initalize the turnaround and waiting property to a dictionary object
    metrics_obj = {
        "turnaround": {},
        "waiting": {},
    }
    
    # Go through each job in each input parameter and only perform operations when their process ids match
    for input_job in input_jobs:
        
        for gantt_job in gantt_jobs:
            
            if (input_job["pid"] == gantt_job["pid"]):
                # Assign turnaround time for the current process id to job end time - job arrival time
                turnaround = gantt_job["end"] - input_job["arrival"]
                # Assign wait time to the turnaround time - burst time
                waitTime = turnaround - input_job["burst"]
                
                # Create a new dictionary property in both turnaround and waiting properties that consist of the current process id
                # Assign the turnaround time for the current process id
                metrics_obj["turnaround"][input_job["pid"]] = turnaround
                # Assign the waiting time for the current process id
                metrics_obj["waiting"][input_job["pid"]] = waitTime
                
                # Increase the average turnaround time by the current turnaround time
                averageTurnaround += turnaround
                # Increase the average waiting time by the current wait time
                averageWaiting += waitTime
    
    # After calculating all turnaround and waiting times, divide the average, currently sums, by the number of processes
    averageTurnaround /= len(input_jobs)
    averageWaiting /= len(input_jobs)
    
    # Create two new properties which include the average turnaround time and the average waiting time
    metrics_obj["avg_turnaround"] = round(averageTurnaround, 2)
    metrics_obj["avg_waiting"] = round(averageWaiting, 2)
    
    # Return the metrics object which is a dictionary to be assigned to the overall result object
    return metrics_obj
    
