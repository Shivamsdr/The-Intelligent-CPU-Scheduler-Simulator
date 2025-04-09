from algorithms import fcfs, sjf, round_robin, priority_scheduling, srtf
from visualization import draw_gantt_chart, draw_gantt_chart_p, calculate_metrics
#from src.suggest_algorithm import suggest_algorithm
from suggest2 import suggest_algorithm
import pandas as pd

# data form excel
# file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\LargeG\1.xlsx'
ope = int(input("Open Any Excel File? f1,f2,f3,f4,f5 :- f"))
print()
if ope == 1:
    file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\LargeG\1.xlsx'
elif ope == 2:
    file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\LargeG\2.xlsx'
elif ope == 3:
    file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\LargeG\3.xlsx'
elif ope == 4:
    file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\LargeG\4.xlsx'
elif ope == 5:
    file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\LargeG\5.xlsx'
else:
    file_path = r'C:\Users\oms1n\OneDrive\Desktop\CS\LargeG\1.xlsx'
    print("Invalid input, defaulting to file 1.")
print("Reading Excel file...")
df = pd.read_excel(file_path, usecols=['id', 'arrival_time', 'burst_time', 'priority'])
print("Excel file read successfully.\n")
#df.rename(columns={'a': 'arrival_time', 'b': 'burst_time', 'p': 'priority'}, inplace=True)
processes = df.to_dict('records')
for process in processes:
    process['initial_burst_time'] = process['burst_time']






print("Choose a scheduling algorithm:")
print("1. First Come First Serve (FCFS)")
print("2. Shortest Job First (SJF)")
print("3. Round Robin (RR)")
print("4. Priority Scheduling")
print("5. Shortest Remaining Time First (SRTF)")

choice = int(input("Enter your choice: "))
p=0
if choice == 1:
    result = fcfs(processes)
elif choice == 2:
    result = sjf(processes)
elif choice == 3:
    time_quantum = int(input("Enter time quantum for Round Robin: "))
    time_quantum = time_quantum
    result = round_robin(processes, time_quantum)
    p=1
elif choice == 4:
    result = priority_scheduling(processes)
elif choice == 5:
    result = srtf(processes)
    p=1
else:
    print("Invalid choice. Exiting.")
    exit()
calculate_metrics(result)
if(p):
    draw_gantt_chart_p(processes,result)
else:
    draw_gantt_chart(processes,result)
