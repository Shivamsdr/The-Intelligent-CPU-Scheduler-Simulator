# algorithms.py

def fcfs(processes):
    """First-Come, First-Served (FCFS) Scheduling"""
    processes.sort(key=lambda x: x['arrival_time'])
    current_time = 0

    for process in processes:
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']

        process['start_time'] = current_time
        process['completion_time'] = current_time + process['burst_time']
        process['turnaround_time'] = process['completion_time'] - process['arrival_time']
        process['waiting_time'] = process['turnaround_time'] - process['burst_time']

        current_time = process['completion_time']

    return processes

def sjf(processes):
    """Shortest Job First (Non-Preemptive) Scheduling"""
    processes.sort(key=lambda x: (x['arrival_time'], x['burst_time']))
    current_time = 0

    for process in processes:
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']

        process['start_time'] = current_time
        process['completion_time'] = current_time + process['burst_time']
        process['turnaround_time'] = process['completion_time'] - process['arrival_time']
        process['waiting_time'] = process['turnaround_time'] - process['burst_time']

        current_time = process['completion_time']

    return processes

def srtf(processes):
    """Shortest Remaining Time First (Preemptive) Scheduling"""
    processes.sort(key=lambda x: x['arrival_time'])
    current_time = 0
    completed = 0
    n = len(processes)
    burst_remaining = [p['burst_time'] for p in processes]
    is_completed = [False] * n

    while completed != n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and not is_completed[i]:
                if burst_remaining[i] < min_burst:
                    min_burst = burst_remaining[i]
                    idx = i
                if burst_remaining[i] == min_burst:
                    if processes[i]['arrival_time'] < processes[idx]['arrival_time']:
                        idx = i

        if idx != -1:
            if burst_remaining[idx] == processes[idx]['burst_time']:
                processes[idx]['start_time'] = current_time
            burst_remaining[idx] -= 1
            current_time += 1
            if burst_remaining[idx] == 0:
                processes[idx]['completion_time'] = current_time
                processes[idx]['turnaround_time'] = processes[idx]['completion_time'] - processes[idx]['arrival_time']
                processes[idx]['waiting_time'] = processes[idx]['turnaround_time'] - processes[idx]['burst_time']
                is_completed[idx] = True
                completed += 1
        else:
            current_time += 1

    return processes

def round_robin():
    #abstract for now
    pass
def priority_scheduling():
    pass
    #abstract for now
def priority_scheduling_p():
    pass
    #abstract for now
