import pandas as pd
import sys
import os
import time  # To measure execution time

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.algorithms import srtf, round_robin  # Assuming your round_robin function is here

#Path to the Excel file
file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\SamplePr.xlsx'
start_time = time.time()
print("Reading Excel file...")
df = pd.read_excel(file_path, usecols=['id', 'arrival_time', 'burst_time', 'priority'])
print(f"Excel file read successfully in {time.time() - start_time:.2f} seconds.\n\n")
df.rename(columns={'a': 'arrival_time', 'b': 'burst_time', 'p': 'priority'}, inplace=True)
print("Columns renamed.\n\n")
start_time = time.time()
processes = df.to_dict('records')
for process in processes:
    process['initial_burst_time'] = process['burst_time']

print(f"Converted to list of dictionaries in {time.time() - start_time:.2f} seconds.\n\n")
# for try ball 
# processes = [
# {"id": "P1", "arrival_time": 0, "burst_time": 2, "priority": 0},
# {"id": "P2", "arrival_time": 1, "burst_time": 50, "priority":0},
# {"id": "P3", "arrival_time": 2, "burst_time": 3, "priority": 0},
# {"id": "P4", "arrival_time": 3, "burst_time": 100, "priority": 0},
# {"id": "P5", "arrival_time": 4, "burst_time": 5, "priority": 0},
# ]

# Step 4: Run the Round Robin scheduling algorithm
print("Running Round Robin scheduling algorithm...")
start_time = time.time()
result = round_robin(processes, quantum=4)
print(f"Round Robin scheduling algorithm completed in {time.time() - start_time:.2f} seconds.\n\n")

# Step 5: Print the results
total_completion_time = 0
total_turnaround_time = 0
total_waiting_time = 0

for process in result:
    print(f"Process {process['id']}: Start Time = {process['start_time']}, "
          f"Completion Time = {process['completion_time']}, "
          f"Turnaround Time = {process['turnaround_time']}, "
          f"Waiting Time = {process['waiting_time']}")
    total_completion_time += process['completion_time']
    total_turnaround_time += process['turnaround_time']
    total_waiting_time += process['waiting_time']

# Step 6: Calculate and print averages
n = len(result)
avg_completion_time = total_completion_time / n
avg_turnaround_time = total_turnaround_time / n
avg_waiting_time = total_waiting_time / n

print("\nAverage Completion Time:", avg_completion_time)
print("Average Turnaround Time:", avg_turnaround_time)
print("Average Waiting Time:", avg_waiting_time)
