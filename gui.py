import tkinter as tk
from tkinter import messagebox
from algorithms import fcfs, sjf, round_robin, priority_scheduling, srtf, priority_scheduling_p
from visualization import draw_gantt_chart, calculate_metrics

process_list = []

def add_process(entry_pid, entry_arrival, entry_burst, entry_priority, listbox):
    """Add a process to the list"""
    try:
        pid = entry_pid.get().strip()
        arrival_time = int(entry_arrival.get())
        burst_time = int(entry_burst.get())
        priority = int(entry_priority.get() or 0)

        if not pid:
            messagebox.showerror("Invalid Input", "Process ID cannot be empty!")
            return

        process_list.append({"id": pid, "arrival_time": arrival_time, "burst_time": burst_time, "priority": priority})
        listbox.insert(tk.END, f"P{pid} - Arrival: {arrival_time}, Burst: {burst_time}, Priority: {priority}")

        # Clear input fields after adding
        entry_pid.delete(0, tk.END)
        entry_arrival.delete(0, tk.END)
        entry_burst.delete(0, tk.END)
        entry_priority.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for Arrival, Burst, and Priority times.")

def run_simulation(selected_algo):
    """Run the selected scheduling algorithm"""
    if not process_list:
        messagebox.showwarning("No Processes", "Add at least one process!")
        return

    if selected_algo == "FCFS":
        result = fcfs(process_list)
    elif selected_algo == "SJF":
        result = sjf(process_list)
    elif selected_algo == "Round Robin":
        result = round_robin(process_list, quantum=2)
    elif selected_algo == "Priority":
        result = priority_scheduling(process_list)
        elif selected_algo == "SRTF":
        result = srtf(process_list)
    else:
        messagebox.showerror("Invalid Algorithm", "Please select a valid scheduling algorithm.")
        return

    draw_gantt_chart(result)
    calculate_metrics(result)

def run_gui():
    """Run the GUI"""
    root = tk.Tk()
    root.title("CPU Scheduler Simulator")
    root.geometry("400x650")
    root.configure(bg="#f0f0f0")

    # Title
    tk.Label(root, text="CPU Scheduler Simulator", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

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

    # Process List
    listbox = tk.Listbox(root, width=60, height=10, selectbackground="#cce7ff")
    listbox.pack(pady=10)

    # Algorithm Selection
    tk.Label(root, bg="#f0f0f0").pack()
    algo_var = tk.StringVar(value="Select Scheduling Algorithm:")
    tk.OptionMenu(root, algo_var, "FCFS", "SJF", "SRTF", "Round Robin", "Priority").pack(pady=5)

    # Buttons
    tk.Button(root, text="Add Process", command=lambda: add_process(entry_pid, entry_arrival, entry_burst, entry_priority, listbox), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)
    tk.Button(root, text="Run Simulation", command=lambda: run_simulation(algo_var.get()), bg="#008CBA", fg="white", padx=10, pady=5).pack()

    root.mainloop()
