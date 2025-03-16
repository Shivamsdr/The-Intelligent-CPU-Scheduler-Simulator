import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.algorithms import srtf, round_robin

# Path to the Excel file
file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\SamplePr.xlsx'
print("Reading Excel file...")
df = pd.read_excel(file_path, usecols=['id', 'arrival_time', 'burst_time', 'priority'])
print("Excel file read successfully.\n")
df.rename(columns={'a': 'arrival_time', 'b': 'burst_time', 'p': 'priority'}, inplace=True)
processes = df.to_dict('records')
for process in processes:
    process['initial_burst_time'] = process['burst_time']

# Run the SRTF scheduling algorithm
print("Processing")
result = srtf(processes)

# Print the results
total_completion_time = 0
total_turnaround_time = 0
total_waiting_time = 0

for process in result:
    print(f"Process {process['id']}: Start Time = {process['start_time']}, Completion Time = {process['completion_time']}, Turnaround Time = {process['turnaround_time']}, Waiting Time = {process['waiting_time']}")
    total_completion_time += process['completion_time']
    total_turnaround_time += process['turnaround_time']
    total_waiting_time += process['waiting_time']

# Calculate and print averages
n = len(result)
avg_completion_time = total_completion_time / n
avg_turnaround_time = total_turnaround_time / n
avg_waiting_time = total_waiting_time / n

print("\nAverage Completion Time:", avg_completion_time)
print("Average Turnaround Time:", avg_turnaround_time)
print("Average Waiting Time:", avg_waiting_time)