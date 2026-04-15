## Author: Serge Rumyantsev
## Date: April 15, 2026

def fifo_schedule(data):
    
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
