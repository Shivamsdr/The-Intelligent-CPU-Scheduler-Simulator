import statistics

def suggest_algorithm(processes):
    # Check same arrival time and arrival time standard deviation
    same_arrival_time = all(p['arrival_time'] == processes[0]['arrival_time'] for p in processes)
    arrival_times = [p['arrival_time'] for p in processes]
    arrival_time_stddev = statistics.stdev(arrival_times) if len(arrival_times) > 1 else 0

    # Check burst times if similar
    burst_times = [p['burst_time'] for p in processes]
    burst_time_stddev = statistics.stdev(burst_times) if len(burst_times) > 1 else 0
    burst_time_avg = statistics.mean(burst_times)
    burst_time_min = min(burst_times)
    burst_time_max = max(burst_times)

    # Binary dividing burst into 2
    burst_times_sorted = sorted(burst_times)
    mid_index = len(burst_times_sorted) // 2
    first_half = burst_times_sorted[:mid_index]
    second_half = burst_times_sorted[mid_index:]
    btme1 = statistics.median(first_half) if first_half else 0
    btme2 = statistics.median(second_half) if second_half else 0

    # Check priorities
    has_no_priority = any(p.get('priority', 0) != 0 for p in processes)

    '''first check'''
    if has_no_priority:
        return "Priority"

    if len(processes) == 1:
        return "fcfs"
    '''second check'''
    if len(processes) <= 3:  # At max 3 (i.e. small) processes
        if same_arrival_time:
            if burst_time_max >= 1.5 * burst_time_min:  # One process is much longer
                return "srtf"  # {Note by OM: here although theoretically theyll be equal,
            else:
                return "sjf"  # but practically SRTF is will have overhead so SJF is fine too}
        else:
            if arrival_time_stddev < 2:
                return "fcfs"  # different A.T but very close
    if btme1 - btme2 > 2 * burst_time_stddev:  # Small processes arrived later '''third check'''
        return "srtf"
    if arrival_time_stddev < 2:  # checks for low preemptivity '''fourth check - consider rr with all others respecting the avg burst'''
        if burst_time_stddev <= 3:  # if burst times are similar
            if burst_time_avg < 4:
                return "fcfs"  # small processes -> fast flow of execution
            elif burst_time_avg < 6:
                return "rr"
            else:
                return "srtf"  # better response time/ fairness
        elif burst_time_stddev <= 5:  # burst varies more than 9 but less than 25 units {assumed para}
            if burst_time_avg < 4:
                return "sjf"
            elif burst_time_avg < 6:
                return "rr"
            else:
                return "srtf"
        else:
            if burst_time_avg < 4:
                return "srtf"
            elif burst_time_avg < 6:
                return "rr"
            else:
                return "srtf"
    return "srtf"

