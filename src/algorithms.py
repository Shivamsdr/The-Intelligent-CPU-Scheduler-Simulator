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

    for process in processes:
        process['segments'] = []

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
            if not processes[idx]['segments'] or processes[idx]['segments'][-1][1] != current_time:
                processes[idx]['segments'].append([current_time, current_time + 1])
            else:
                processes[idx]['segments'][-1][1] = current_time + 1
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

def round_robin(processes, quantum):
    #Round Robin Scheduling
    n = len(processes)
    burst_remaining = [p['burst_time'] for p in processes]
    current_time = 0
    completed = 0
    queue = []
    result = []

    for process in processes:
        process['waiting_time'] = 0
        process['start_time'] = -1  # Initialize start time
        process['segments'] = []

    while completed != n:
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and burst_remaining[i] > 0 and processes[i] not in queue:
                queue.append(processes[i])

        if queue:
            current_process = queue.pop(0)
            idx = processes.index(current_process)
            if current_process['start_time'] == -1:
                current_process['start_time'] = current_time  # Set start_time
            if burst_remaining[idx] > quantum:
                if not current_process['segments'] or current_process['segments'][-1][1] != current_time:
                    current_process['segments'].append([current_time, current_time + quantum])
                else:
                    current_process['segments'][-1][1] = current_time + quantum
                current_time += quantum
                burst_remaining[idx] -= quantum
                # Added arrived processes to the queue before readding this curr process
                for i in range(n):
                    if processes[i]['arrival_time'] <= current_time and burst_remaining[i] > 0 and processes[i] not in queue:
                        queue.append(processes[i])
                queue.append(current_process)
            else:
                if not current_process['segments'] or current_process['segments'][-1][1] != current_time:
                    current_process['segments'].append([current_time, current_time + burst_remaining[idx]])
                else:
                    current_process['segments'][-1][1] = current_time + burst_remaining[idx]
                current_time += burst_remaining[idx]
                burst_remaining[idx] = 0
                completed += 1
                current_process['completion_time'] = current_time
                current_process['turnaround_time'] = current_process['completion_time'] - current_process['arrival_time']
                current_process['waiting_time'] = current_process['turnaround_time'] - current_process['initial_burst_time']
                result.append(current_process)
        else:
            current_time += 1

    return result

def priority_scheduling(processes):
    """Priority Scheduling"""
    processes.sort(key=lambda x: (x['priority'], x['arrival_time']))
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

import time
processes = [
    {"id": 1, "arrival_time": 0, "burst_time": 5, "priority": 1, "initial_burst_time": 5},
    {"id": 2, "arrival_time": 1, "burst_time": 4, "priority": 2, "initial_burst_time": 4},
    {"id": 3, "arrival_time": 2, "burst_time": 2, "priority": 3, "initial_burst_time": 2},
    {"id": 4, "arrival_time": 3, "burst_time": 3, "priority": 4, "initial_burst_time": 3},
    {"id": 5, "arrival_time": 4, "burst_time": 1, "priority": 5, "initial_burst_time": 1}
]
if __name__ == "__main__":
    # Measure the time taken for round robin scheduling
    start_time = time.time()
    result = round_robin(processes, quantum=2)
    end_time = time.time()
    print(f"Round Robin scheduling took {end_time - start_time:.2f} seconds.")
    result = fcfs(processes)
    print(f"FCFS scheduling took {end_time - start_time:.2f} seconds.")
    result = sjf(processes)
    print(f"SJF scheduling took {end_time - start_time:.2f} seconds.")
    result = srtf(processes)
    print(f"SRTF scheduling took {end_time - start_time:.2f} seconds.")
    result = priority_scheduling(processes)
    print(f"Priority scheduling took {end_time - start_time:.2f} seconds.")


'''
#faster using deque
from collections import deque
def round_robin(processes, quantum):
    # Round Robin Scheduling
    n = len(processes)
    burst_remaining = [p['burst_time'] for p in processes]
    current_time = 0
    completed = 0
    queue = deque()  # Using deque for efficient pops from the front and appends to the back
    result = []

    # Initialize processes
    for process in processes:
        process['waiting_time'] = 0
        process['start_time'] = -1  # Initialize start time
        process['segments'] = []

    while completed != n:
        # Add newly arrived processes to the queue
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and burst_remaining[i] > 0 and processes[i] not in queue:
                queue.append(processes[i])

        if queue:
            current_process = queue.popleft()  # Pop the process from the front of the queue
            idx = processes.index(current_process)

            if current_process['start_time'] == -1:
                current_process['start_time'] = current_time  # Set start time

            if burst_remaining[idx] > quantum:
                # Add a new time segment for the process
                if not current_process['segments'] or current_process['segments'][-1][1] != current_time:
                    current_process['segments'].append([current_time, current_time + quantum])
                else:
                    current_process['segments'][-1][1] = current_time + quantum

                current_time += quantum
                burst_remaining[idx] -= quantum

                # Recheck processes and add newly arrived ones to the queue
                for i in range(n):
                    if processes[i]['arrival_time'] <= current_time and burst_remaining[i] > 0 and processes[i] not in queue:
                        queue.append(processes[i])

                # Re-add the current process to the queue if it’s not finished
                if burst_remaining[idx] > 0:
                    queue.append(current_process)

            else:
                # Process completes
                if not current_process['segments'] or current_process['segments'][-1][1] != current_time:
                    current_process['segments'].append([current_time, current_time + burst_remaining[idx]])
                else:
                    current_process['segments'][-1][1] = current_time + burst_remaining[idx]

                current_time += burst_remaining[idx]
                burst_remaining[idx] = 0
                completed += 1
                current_process['completion_time'] = current_time
                current_process['turnaround_time'] = current_process['completion_time'] - current_process['arrival_time']
                current_process['waiting_time'] = current_process['turnaround_time'] - current_process['initial_burst_time']
                result.append(current_process)
        else:
            current_time += 1  # Idle time if no process is ready to run

    return result

'''
