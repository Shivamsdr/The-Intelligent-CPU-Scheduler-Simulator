# The Intelligent CPU Scheduler Simulator
A practical CPU scheduling simulation tool with real-time visualization with heuristic suggestions for algorithm and planned AI/ML enhancements and prediction models.

## Overview
This project is a CPU scheduling simulator that helps visualize and analyze different scheduling algorithms. It currently supports:

### Implemented:
Process Scheduling using following algorithms
1. First Come First Serve (FCFS)  
2. Shortest Job First (SJF)
3. Round Robin (RR)
4. Priority Scheduling (non preemptive)
5. Shortest Remaining Time First (SRTF)  

### Planned Enhancements:
+ Priority Scheduling (Preemptive)  
+ Adding AI/ML-based heuristics for dynamic scheduling (or suggestions to the user)  
+ Advanced performance comparison metrics than existings ones  
+ More interactive GUI features for user-friendly simulations  

### Features
+ Gantt Chart Visualization (Both preemptive and non-preemptive)  
+ Multiple Scheduling Algorithms (fcfs,sjf,srtf,rr,priority)  
+ Performance Metrics (Avg. Waiting Time, Turnaround Time, Response Times)  
+ Testing Programs for Algorithms (For large Sample data testing)  

### Project Structure
```
/src  
  |--- algorithms.py      # Scheduling algorithms  
  |--- gui.py             # GUI implementation 
  |--- visualization.py   # Visualization 
  |--- main.py            # Entry point  
/tests  
  |--- test_rr.py         # Round Robin test
  |--- test_srtf.py       # SRTF test
  |--- test.xlsx          # DataSet for tests
/docs  
  |--- README.md          # Documentation  
  |--- requirements.txt   # Required Libraries
```
### How to Run

1. Clone the repository:
```
git clone https://github.com/Shivamsdr/The-Intelligent-CPU-Scheduler-Simulator.git  
cd The-Intelligent-CPU-Scheduler-Simulator
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run the simulator:
```
python3 main.py
```
 
### Contributors
**Shivam Yadav** https://github.com/Shivamsdr  
**Om Singh Chauhan** https://github.com/OmSingh2005  
**Aryan Kumar** https://github.com/AryanKumarLpu  

Feel free to suggest improvements, report issues, or contribute to this project. If you have ideas for adding AI/ML-based, let’s collaborate
