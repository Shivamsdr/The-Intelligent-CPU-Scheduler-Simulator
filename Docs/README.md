# The Intelligent CPU Scheduler Simulator
A practical CPU scheduling simulation tool with real-time visualization with heuristic suggestions and TestBased conclusions for various scheduling algorithms, With given implementation, to train AI/ML or prediction models, using Large-Sample-Tests methods provided in the simulator  

## Overview
This project is a CPU scheduling simulator that helps visualize and analyze different scheduling algorithms. It currently supports:

### Implemented:  
Process Scheduling using following algorithms  
1. First Come First Serve (FCFS) -NP  
2. Shortest Job First (SJF) -NP  
3. Round Robin (RR) -P  
4. Priority Scheduling -NP 
5. Shortest Remaining Time First (SRTF) -P  
Non-preemptive -NP && Preemptive -P  

### Planned Enhancements:
+ Priority Scheduling (Preemptive)  
+ Adding AI/ML training { on existing DataGenerating Methods} for dynamic scheduling [ and better suggestions to user]  
+ Advanced heuristics parameters than existings ones  
+ More interactive GUI features for user-friendly simulations  

### Features
+ Gantt Chart Visualization (Both preemptive and Non-preemptive)  
+ Multiple Scheduling Algorithms (fcfs,sjf,srtf,rr,priority)  
+ Performance Metrics (Avg. Waiting Time, Turnaround Time, Response Times)  
+ Testing Programs for Algorithms (For large Sample data testing)
+ Population and Sample Data implementations to train AI/ML prediction models

### Project Structure
```
/src  
  |--- algorithms.py          # Scheduling algorithms  
  |--- gui.py                 # GUI implementation 
  |--- visualization.py       # Visualization 
  |--- main.py                # Entry point
  |--- suggest_algorithm.py   # Heuristic Methods
/tests
  |--- LargeSampleGraph.py    # Graph visualisation for Large Data
  |--- test_rr.py             # Round Robin test
  |--- test_srtf.py           # SRTF test
  |--- test_suggest_algorithm.py #Heuristics Test
  |--- datagen.py             # Sample & Population Data Generator 
  |--- SamplePr.xlsx          # Population DataSet for tests  
  |--- RandSamples.xlsx       # Sample population generator  
/docs  
  |--- README.md              # Documentation  
  |--- requirements.txt       # Required Libraries
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
**Aryan Kumar** https://github.com/Aryan114mehta

Feel free to suggest improvements, report issues, or contribute to this project. If you have ideas for adding AI/ML-based, let’s collaborate
