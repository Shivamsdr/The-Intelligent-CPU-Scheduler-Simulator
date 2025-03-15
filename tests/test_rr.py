import pandas as pd
from algorithms import srtf,round_robin

# Path to the Excel file
file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\test.xlsx'

# Read process data from the Excel file
print("Reading Excel file...")
df = pd.read_excel(file_path, usecols=['id', 'a', 'b', 'p'])
print("Excel file read successfully.\n\n")

# Rename columns
df.rename(columns={'a': 'arrival_time', 'b': 'burst_time', 'p': 'priority'}, inplace=True)
print("Columns renamed.\n\n")


# Convert DataFrame to list of dictionaries
processes = df.to_dict('records')
for process in processes:
    process['initial_burst_time'] = process['burst_time']
#print("Converted to list of dictionaries:", processes)


# Run the SRTF scheduling algorithm
print("Running SRTF scheduling algorithm...")
result = round_robin(processes, quantum=2)
print("SRTF scheduling algorithm completed.\n\n")

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
