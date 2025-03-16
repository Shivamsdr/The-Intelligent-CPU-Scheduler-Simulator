import tkinter as tk
from tkinter import messagebox
from algorithms import fcfs, sjf, round_robin, priority_scheduling, srtf
from visualization import draw_gantt_chart, draw_gantt_chart_p, calculate_metrics

from suggest_algorithm import suggest_algorithm
process_list = []

def add_process(entry_pid, entry_arrival, entry_burst, entry_priority, listbox, algo_label,algo_var,best_tt_label):
#Add a process to the list
    try:
        pid = entry_pid.get().strip()
        arrival_time = int(entry_arrival.get())
        burst_time = int(entry_burst.get())
        priority = entry_priority.get().strip()
        if priority == "" or priority == "optional": #So that it doent consider 'optional' as actualy value 
            priority = 0
        else:
            priority = int(priority)

        if not pid:
            messagebox.showerror("Invalid Input", "Process ID cannot be empty!")
            return

        process_list.append({"id": pid, "arrival_time": arrival_time, "burst_time": burst_time, "priority": priority,"initial_burst_time": burst_time})
        #listbox.insert(tk.END, f"   Process {pid} - Arrival: {arrival_time}, Burst: {burst_time}, Priority: {priority}")
        listbox.insert(tk.END, f"       P{pid}     -     {arrival_time}        {burst_time}        {priority}")
        # Clear input fields after adding
        entry_pid.delete(0, tk.END)
        entry_arrival.delete(0, tk.END)
        entry_burst.delete(0, tk.END)
        entry_priority.delete(0, tk.END)

        #suggestion
        suggested_algo = suggest_algorithm(process_list)
        algo_label.config(text=f"heuritics_Suggestion: {suggested_algo}")
        results = {
            "FCFS": calculate_metrics(fcfs(process_list)),
            "SJF": calculate_metrics(sjf(process_list)),
            "SRTF": calculate_metrics(srtf(process_list)),
            "Round Robin": calculate_metrics(round_robin(process_list, quantum=2)),
            "Priority": calculate_metrics(priority_scheduling(process_list))
        }
        best_algo_tt = min(results, key=lambda algo: results[algo]['avg_turnaround_time'])
        best_algo_wt = min(results, key=lambda algo: results[algo]['avg_waiting_time'])

        #update labels
        best_tt_label.config(text=f"BestTT-Algorithm: {best_algo_tt} && BestWT-Algorithm: {best_algo_wt}")
        #best_wt_label.config(text=f"")

        # suggested algorithm in the dropdown
        algo_var.set(suggested_algo)


    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid only numeric values for Arrival time, Burst time, and Priority.")
def calculate_metrics(result): #for adding process usecase
    #Calculate metrics for result.
    total_turnaround_time = sum(p['turnaround_time'] for p in result)
    total_waiting_time = sum(p['waiting_time'] for p in result)
    n = len(result)
    return {
        'avg_turnaround_time': total_turnaround_time,
        'avg_waiting_time': total_waiting_time
    }
def remove_process(listbox,algo_label,algo_var):
    #Remove the selected process from the list
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
        del process_list[selected_index - 1]  # Adjust index to account for header
        if process_list:  # If there are still processes left
            suggested_algo = suggest_algorithm(process_list)
            algo_label.config(text=f"Suggested Algorithm: {suggested_algo}")
            algo_var.set(suggested_algo)  # Update the dropdown menu
        else:  # If no processes are left
            algo_label.config(text="Suggested Algorithm: None")
            algo_var.set("Select Scheduling Algorithm:")

    except IndexError:
        messagebox.showerror("Selection Error", "Please select a process to remove.")
        
def run_simulation(selected_algo):
    #Run the selected scheduling algorithm
    if not process_list:
        messagebox.showwarning("Zero Processes", "Add at least one process")
        return
    p=0 #preemptive flag
    if selected_algo == "FCFS":
        result = fcfs(process_list)
    elif selected_algo == "SJF":
        result = sjf(process_list)
    elif selected_algo == "Round Robin":
        result = round_robin(process_list, quantum=2)
        p=1
    elif selected_algo == "Priority":
        result = priority_scheduling(process_list)
    elif selected_algo == "SRTF":
        result = srtf(process_list)
        p=1
    else:
        messagebox.showerror("Invalid Algorithm is selected", "Please select a valid scheduling algorithm")
        return

    if(p):
        draw_gantt_chart_p(result)
    else:
        draw_gantt_chart(result)
    calculate_metrics(result)

#Quality of LIFE gui (*wink*)
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def run_gui():
    """Run the GUI"""
    root = tk.Tk()
    root.title("CPU Scheduler Simulator")
    root.geometry("480x750") #adjusts width for vertical rectagle
    root.configure(bg="#f0f0f0")

    # Title
    tk.Label(root, text="Intelligent CPU Scheduler Simulator", font=("MS Serif", 20, "bold"), bg="#f0f0f0").pack(pady=20)

    # Input Section
    input_frame = tk.Frame(root, bg="#f0f0f0")
    input_frame.pack(pady=10,anchor="w")

    tk.Label(input_frame, text="Process ID:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_pid = tk.Entry(input_frame)
    entry_pid.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(input_frame, text="Arrival Time:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_arrival = tk.Entry(input_frame)
    entry_arrival.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(input_frame, text="Burst Time:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_burst = tk.Entry(input_frame)
    entry_burst.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(input_frame, text="Priority:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_priority = tk.Entry(input_frame)
    entry_priority.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    add_placeholder(entry_priority, "optional")

    # Suggested Algorithm Label
    algo_label = tk.Label(root, text="Suggested Algorithm: None", font=("MS Serif", 18, 'bold'), bg="#f0f0f0", fg="darkgreen")
    algo_label.pack(pady=10)
    # BestWT-Algorithm Label
    #best_wt_label = tk.Label(root, text="BestWT-Algorithm: None", font=("MS Serif", 14), bg="#f0f0f0", fg="darkgrey")
    #best_wt_label.pack(pady=5)

    # Process List
    listbox = tk.Listbox(root, width=60, height=10, selectbackground="#cce7ff")
    listbox.pack(pady=10)
    listbox.insert(tk.END, f"  Process ID  Arrival  Burst  Priority  ")
    # BestTT-Algorithm Label
    best_tt_label = tk.Label(root, text="BestTT-Algorithm: None && BestWT-Algorithm: None", font=("MS Serif", 13, 'bold'), bg="#f0f0f0", fg="grey")
    best_tt_label.pack(pady=5)
    # Algorithm Selection
    tk.Label(root, bg="#f0f0f0").pack()
    algo_var = tk.StringVar(value="Select Scheduling Algorithm:")
    tk.OptionMenu(root, algo_var, "FCFS", "SJF", "Round Robin", "Priority", "SRTF").pack(pady=5)

    # Buttons Frame
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)

    # ADD-REMOVE Buttons
    button_width = 10
    tk.Button(button_frame, text="Add Process", command=lambda: add_process(entry_pid, entry_arrival, entry_burst, entry_priority, listbox,algo_label, algo_var,best_tt_label), bg="#4CAF50", fg="white", padx=10, pady=5, width = button_width).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Remove Process", command=lambda: remove_process(listbox,algo_label, algo_var,best_tt_label), bg="#f44336", fg="white", padx=10, pady=5, width = button_width).pack(side=tk.LEFT, padx=5)
    # Run-Simulation Button
    tk.Button(root, text="Run Simulation", command=lambda: run_simulation(algo_var.get()), bg="#008CBA", fg="white", padx=10, pady=5, width = (button_width*2)+5).pack(pady=10)
    
    root.mainloop()
    '''
    Previously in 1000 B.C.E (aka earlier commit)
    # Algorithm Selection
    tk.Label(root, bg="#f0f0f0").pack()
    algo_var = tk.StringVar(value="Select Scheduling Algorithm:")
    tk.OptionMenu(root, algo_var, "FCFS", "SJF", "Round Robin", "Priority", "SRTF").pack(pady=5)
    # Buttons Frame
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)
    # Buttons
    tk.Button(button_frame, text="Add Process", command=lambda: add_process(entry_pid, entry_arrival, entry_burst, entry_priority, listbox), bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Run Simulation", command=lambda: run_simulation(algo_var.get()), bg="#008CBA", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    '''
    
