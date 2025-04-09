# algorithms.py
import pandas as pd
import time

def priority_scheduling(processes):
    """Priority Scheduling"""
    processes_copy = sorted(processes, key=lambda x: (x['arrival_time'], x['priority']))
    current_time = 0
    for process in processes_copy:
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']
        process['start_time'] = current_time
        process['completion_time'] = current_time + process['burst_time']
        process['turnaround_time'] = process['completion_time'] - process['arrival_time']
        process['waiting_time'] = process['turnaround_time'] - process['burst_time']
        current_time = process['completion_time']
    return processes_copy

def fcfs(processes):
    """First-Come, First-Served (FCFS) Scheduling"""
    processes_copy = sorted(processes, key=lambda x: x['arrival_time'])
    current_time = 0
    for process in processes_copy:
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']
        process['start_time'] = current_time
        process['completion_time'] = current_time + process['burst_time']
        process['turnaround_time'] = process['completion_time'] - process['arrival_time']
        process['waiting_time'] = process['turnaround_time'] - process['burst_time']
        current_time = process['completion_time']
    return processes_copy

def sjf(processes):
    """Shortest Job First (Non-Preemptive) Scheduling"""
    processes_copy = sorted(processes, key=lambda x: (x['arrival_time'], x['burst_time']))
    current_time = 0
    for process in processes_copy:
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']
        process['start_time'] = current_time
        process['completion_time'] = current_time + process['burst_time']
        process['turnaround_time'] = process['completion_time'] - process['arrival_time']
        process['waiting_time'] = process['turnaround_time'] - process['burst_time']
        current_time = process['completion_time']
    return processes_copy

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
    """Round Robin Scheduling with fixed time quantum"""
    processes.sort(key=lambda x: x['arrival_time'])
    n = len(processes)
    current_time = 0
    burst_remaining = [p['burst_time'] for p in processes]
    is_completed = [False] * n
    queue = []
    
    # Initialize process segments
    for process in processes:
        process['segments'] = []
    
    while True:
        flag = True
        # Check for new arrivals and add to queue
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and not is_completed[i] and i not in queue:
                queue.append(i)
                flag = False
        
        if not queue and flag:  # All processes complete
            break
        
        if queue:
            idx = queue.pop(0)  # Get the first process from queue
            
            # If process is starting for the first time
            if burst_remaining[idx] == processes[idx]['burst_time']:
                processes[idx]['start_time'] = current_time
            
            # Calculate execution time for this cycle
            execution_time = min(quantum, burst_remaining[idx])
            
            # Update segments
            if not processes[idx]['segments'] or processes[idx]['segments'][-1][1] != current_time:
                processes[idx]['segments'].append([current_time, current_time + execution_time])
            else:
                processes[idx]['segments'][-1][1] = current_time + execution_time
            
            # Update time and remaining burst
            current_time += execution_time
            burst_remaining[idx] -= execution_time
            
            # Check if process is complete
            if burst_remaining[idx] == 0:
                processes[idx]['completion_time'] = current_time
                processes[idx]['turnaround_time'] = processes[idx]['completion_time'] - processes[idx]['arrival_time']
                processes[idx]['waiting_time'] = processes[idx]['turnaround_time'] - processes[idx]['burst_time']
                is_completed[idx] = True
            else:
                # Add process back to queue if it's not complete
                # But first check for any new arrivals
                for i in range(n):
                    if processes[i]['arrival_time'] <= current_time and not is_completed[i] and i not in queue and i != idx:
                        queue.append(i)
                queue.append(idx)
        else:
            # No process in queue but not all complete - advance time to next arrival
            next_arrival = float('inf')
            for i in range(n):
                if not is_completed[i] and processes[i]['arrival_time'] > current_time:
                    next_arrival = min(next_arrival, processes[i]['arrival_time'])
            if next_arrival != float('inf'):
                current_time = next_arrival
            else:
                break
    
    return processes
# def round_robin(processes, quantum=2):
#     """Round Robin Scheduling"""
#     processes.sort(key=lambda x: x['arrival_time'])
#     n = len(processes)
#     burst_remaining = [p['burst_time'] for p in processes]
#     current_time = 0
#     completed = 0
#     queue = []
#     result = []

#     for process in processes:
#         process['waiting_time'] = 0
#         process['start_time'] = -1  # Initialize start time
#         process['segments'] = []
#         process['initial_burst_time'] = process['burst_time']

#     while completed != n:
#         # Add newly arrived processes to the queue
#         for i in range(n):
#             if processes[i]['arrival_time'] <= current_time and burst_remaining[i] > 0 and processes[i] not in queue:
#                 queue.append(processes[i])

#         if queue:
#             current_process = queue.pop(0)
#             idx = processes.index(current_process)

#             # Set start time if this is the first execution of the process
#             if current_process['start_time'] == -1:
#                 current_process['start_time'] = current_time

#             # Execute the process for a time slice (quantum) or until it finishes
#             if burst_remaining[idx] > quantum:
#                 if not current_process['segments'] or current_process['segments'][-1][1] != current_time:
#                     current_process['segments'].append([current_time, current_time + quantum])
#                 else:
#                     current_process['segments'][-1][1] = current_time + quantum
#                 current_time += quantum
#                 burst_remaining[idx] -= quantum

#                 # Add newly arrived processes to the queue before re-adding the current process
#                 for i in range(n):
#                     if processes[i]['arrival_time'] <= current_time and burst_remaining[i] > 0 and processes[i] not in queue:
#                         queue.append(processes[i])
#                 queue.append(current_process)  # Re-add the current process to the end of the queue
#             else:
#                 # Process finishes execution
#                 if not current_process['segments'] or current_process['segments'][-1][1] != current_time:
#                     current_process['segments'].append([current_time, current_time + burst_remaining[idx]])
#                 else:
#                     current_process['segments'][-1][1] = current_time + burst_remaining[idx]
#                 current_time += burst_remaining[idx]
#                 burst_remaining[idx] = 0
#                 completed += 1
#                 current_process['completion_time'] = current_time
#                 current_process['turnaround_time'] = current_process['completion_time'] - current_process['arrival_time']
#                 current_process['waiting_time'] = current_process['turnaround_time'] - current_process['initial_burst_time']

#                 # Add newly arrived processes to the queue before adding the finished process
#                 for i in range(n):
#                     if processes[i]['arrival_time'] <= current_time and burst_remaining[i] > 0 and processes[i] not in queue:
#                         queue.append(processes[i])
#                 result.append(current_process)  # Add the finished process to the result
#         else:
#             # If no process is ready, increment time
#             current_time += 1

#     return result
'''def round_robin(processes, quantum=2):
    #Round Robin Scheduling
    processes.sort(key=lambda x: x['arrival_time'])
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
        #if 'initial_burst_time' not in process:
        process['initial_burst_time'] = process['burst_time']

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

    return result'''
# def round_robin(processes, quantum=2):
#     # Round Robin Scheduling
#     processes.sort(key=lambda x: x['arrival_time'])
#     n = len(processes)
#     burst_remaining = [p['burst_time'] for p in processes]
#     current_time = 0
#     completed = 0
#     queue = []
#     result = []

#     for process in processes:
#         process['waiting_time'] = 0
#         process['start_time'] = -1  # Initialize start time
#         process['segments'] = []
#         process['initial_burst_time'] = process['burst_time']

#     while completed != n:
#         # Add processes that have arrived and are not yet completed to the queue
#         for i in range(n):
#             if (
#                 processes[i]['arrival_time'] <= current_time
#                 and burst_remaining[i] > 0
#                 and processes[i] not in queue
#             ):
#                 queue.append(processes[i])

#         if queue:
#             current_process = queue.pop(0)
#             idx = processes.index(current_process)

#             # Set start time if this is the first execution of the process
#             if current_process['start_time'] == -1:
#                 current_process['start_time'] = current_time

#             # Execute the process for a time slice (quantum) or until it finishes
#             execution_time = min(quantum, burst_remaining[idx])
#             burst_remaining[idx] -= execution_time

#             # Add the segment for this execution
#             if not current_process['segments'] or current_process['segments'][-1][1] != current_time:
#                 current_process['segments'].append([current_time, current_time + execution_time])
#             else:
#                 # Extend the last segment if it continues from the previous one
#                 current_process['segments'][-1][1] += execution_time

#             current_time += execution_time

#             # If the process is finished, calculate its metrics
#             if burst_remaining[idx] == 0:
#                 completed += 1
#                 current_process['completion_time'] = current_time
#                 current_process['turnaround_time'] = (
#                     current_process['completion_time'] - current_process['arrival_time']
#                 )
#                 current_process['waiting_time'] = (
#                     current_process['turnaround_time'] - current_process['initial_burst_time']
#                 )
#                 result.append(current_process)
#             else:
#                 # Re-add the process to the queue if it's not finished
#                 for i in range(n):
#                     if (
#                         processes[i]['arrival_time'] <= current_time
#                         and burst_remaining[i] > 0
#                         and processes[i] not in queue
#                     ):
#                         queue.append(processes[i])
#                 queue.append(current_process)
#         else:
#             # If no process is ready, increment time
#             current_time += 1

#     return result





if __name__ == "__main__":
    processes = [
    {"id": 1, "arrival_time": 0, "burst_time": 5, "priority": 1, "initial_burst_time": 5},
    {"id": 2, "arrival_time": 1, "burst_time": 4, "priority": 2, "initial_burst_time": 4},
    {"id": 3, "arrival_time": 2, "burst_time": 2, "priority": 3, "initial_burst_time": 2},
    {"id": 4, "arrival_time": 3, "burst_time": 3, "priority": 4, "initial_burst_time": 3},
    {"id": 5, "arrival_time": 4, "burst_time": 1, "priority": 5, "initial_burst_time": 1}
    ]
    processes= pd.read_excel(r'C:\Users\oms1n\OneDrive\Desktop\CS\SamplePr.xlsx',
                         usecols=['id', 'arrival_time', 'burst_time', 'priority']).to_dict('records')
    # Measure the time taken for round robin scheduling
    start_time = time.time()
    result = round_robin(processes, quantum=2)
    end_time = time.time()
    print(f"Round Robin scheduling took {end_time - start_time:.2f} seconds.")
    start_time = time.time()
    result = fcfs(processes)
    end_time = time.time()
    print(f"FCFS scheduling took {end_time - start_time:.2f} seconds.")
    start_time = time.time()
    result = sjf(processes)
    end_time = time.time()
    print(f"SJF scheduling took {end_time - start_time:.2f} seconds.")
    start_time = time.time()
    result = srtf(processes)
    end_time = time.time()
    print(f"SRTF scheduling took {end_time - start_time:.2f} seconds.")
    start_time = time.time()
    result = priority_scheduling(processes)
    end_time = time.time()
    print(f"Priority scheduling took {end_time - start_time:.2f} seconds.")

