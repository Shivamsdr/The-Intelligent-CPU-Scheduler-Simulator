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

