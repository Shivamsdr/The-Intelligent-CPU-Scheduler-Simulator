def suggest_algorithm(processes):
    # Check same arrival time
    same_arrival_time = all(p['arrival_time'] == processes[0]['arrival_time'] for p in processes)

    # Check priorities
    has_priority = all('priority' !=0 in p for p in processes)

    # Check burst times if similar
    burst_times = [p['burst_time'] for p in processes]
    burst_time_variance = max(burst_times) - min(burst_times)

    # Suggest algorithm
    if same_arrival_time and not has_priority:
        if burst_time_variance <= 2:  # burst times are similar
            return "FCFS"
        else:
            return "SJF"
    elif not same_arrival_time and not has_priority:
        return "SRTF"
    elif has_priority:
        return "Priority"
    else:
        return "Round Robin"  # Default  Round Robin (for fairness)