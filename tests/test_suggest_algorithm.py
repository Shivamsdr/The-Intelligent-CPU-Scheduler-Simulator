import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.suggest_algorithm import suggest_algorithm

# data form excel
file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\SamplePr.xlsx'
print("Reading Excel file...")
df = pd.read_excel(file_path, usecols=['id', 'arrival_time', 'burst_time', 'priority'])
print("Excel file read successfully.\n")
df.rename(columns={'a': 'arrival_time', 'b': 'burst_time', 'p': 'priority'}, inplace=True)
processes = df.to_dict('records')
for process in processes:
    process['initial_burst_time'] = process['burst_time']

# default list of processes

processes = [
{"id": "P1", "arrival_time": 0, "burst_time": 2, "priority": 0},
{"id": "P2", "arrival_time": 1, "burst_time": 5, "priority":0},
{"id": "P3", "arrival_time": 2, "burst_time": 3, "priority": 0},
{"id": "P4", "arrival_time": 3, "burst_time": 100, "priority": 0},
{"id": "P5", "arrival_time": 4, "burst_time": 5, "priority": 0},
]


# Suggest the best algorithm
suggested_algo = suggest_algorithm(processes)
print(f"Suggested Algorithm: {suggested_algo}")