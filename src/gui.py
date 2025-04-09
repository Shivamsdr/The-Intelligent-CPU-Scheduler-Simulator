import tkinter as tk
from tkinter import messagebox, ttk, font
from algorithms import fcfs, sjf, round_robin, priority_scheduling, srtf
from visualization import draw_gantt_chart, draw_gantt_chart_p, draw_gantt_chart_r, calculate_metrics

#from suggest_algorithm import suggest_algorithm
from suggest2 import suggest_algorithm
process_list = []

def add_process(entry_pid, entry_arrival, entry_burst, entry_priority, treeview, algo_label, algo_var, best_tt_label):
    """Add a process to the list"""
    try:
        pid = entry_pid.get().strip()
        arrival_time = int(entry_arrival.get())
        burst_time = int(entry_burst.get())
        priority = entry_priority.get().strip()
        if priority == "" or priority == "optional": #So that it doesn't consider 'optional' as actual value 
            priority = 0
        else:
            priority = int(priority)

        if not pid:
            messagebox.showerror("Invalid Input", "Process ID cannot be empty!")
            return

        process_list.append({
            "id": pid, 
            "arrival_time": arrival_time, 
            "burst_time": burst_time,
            "priority": priority,
            "initial_burst_time": burst_time
        })
        
        # Insert into treeview
        treeview.insert('', 'end', values=(f"P{pid}", arrival_time, burst_time, priority))
        
        # Clear input fields after adding
        entry_pid.delete(0, tk.END)
        entry_arrival.delete(0, tk.END)
        entry_burst.delete(0, tk.END)
        entry_priority.delete(0, tk.END)
        add_placeholder(entry_priority, "optional")

        # Suggestion
        suggested_algo = suggest_algorithm(process_list)
        algo_label.config(text=f"Suggested Algorithm: {suggested_algo}")
        
        results = {
            "FCFS": calculate_metrics2(fcfs(process_list)),
            "SJF": calculate_metrics2(sjf(process_list)),
            "SRTF": calculate_metrics2(srtf(process_list)),
            "Round Robin": calculate_metrics2(round_robin(process_list, quantum=2)),
            "Priority": calculate_metrics2(priority_scheduling(process_list))
        }
        
        best_algo_tt = min(results, key=lambda algo: results[algo]['avg_turnaround_time'])
        best_algo_wt = min(results, key=lambda algo: results[algo]['avg_waiting_time'])

        # Update labels
        best_tt_label.config(text=f"Best TT: {best_algo_tt} | Best WT: {best_algo_wt}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for Arrival time, Burst time, and Priority.")

def calculate_metrics2(result): #for adding process usecase
    """Calculate metrics for result."""
    total_turnaround_time = sum(p['turnaround_time'] for p in result)
    total_waiting_time = sum(p['waiting_time'] for p in result)
    return {
        'avg_turnaround_time': total_turnaround_time,
        'avg_waiting_time': total_waiting_time
    }

def remove_process(treeview, algo_label, algo_var, best_tt_label):
    """Remove the selected process from the list and update backend data."""
    try:
        # Get the selected item
        selected_item = treeview.selection()[0]
        selected_index = treeview.index(selected_item)
        
        # Remove from backend
        if 0 <= selected_index < len(process_list):
            del process_list[selected_index]
            
            # Remove from treeview
            treeview.delete(selected_item)
            
            # Update the suggested algorithm and metrics if processes remain
            if process_list:
                # Update the suggested algorithm
                suggested_algo = suggest_algorithm(process_list)
                algo_label.config(text=f"Suggested Algorithm: {suggested_algo}")

                # Recalculate metrics for all algorithms
                results = {
                    "FCFS": calculate_metrics2(fcfs(process_list)),
                    "SJF": calculate_metrics2(sjf(process_list)),
                    "SRTF": calculate_metrics2(srtf(process_list)),
                    "Round Robin": calculate_metrics2(round_robin(process_list, quantum=2)),
                    "Priority": calculate_metrics2(priority_scheduling(process_list))
                }

                best_algo_tt = min(results, key=lambda algo: results[algo]['avg_turnaround_time'])
                best_algo_wt = min(results, key=lambda algo: results[algo]['avg_waiting_time'])

                # Update the labels
                best_tt_label.config(text=f"Best TT: {best_algo_tt} | Best WT: {best_algo_wt}")
            else:
                # If no processes remain, reset the labels
                algo_label.config(text="Suggested Algorithm: None")
                algo_var.set("Select Algorithm")
                best_tt_label.config(text="Best TT: None | Best WT: None")
        else:
            messagebox.showerror("Error", "Selected index is out of range.")

    except IndexError:
        # Handle the case where no process is selected
        messagebox.showerror("Selection Error", "Please select a process to remove.")

def run_simulation(selected_algo):
    """Run the selected scheduling algorithm"""
    if not process_list:
        messagebox.showwarning("Zero Processes", "Add at least one process")
        return
    
    p = 0  # preemptive flag
    if selected_algo == "FCFS":
        result = fcfs(process_list)
    elif selected_algo == "SJF":
        result = sjf(process_list)
    elif selected_algo == "Round Robin":
        result = round_robin(process_list, quantum=3)
        p = 2
    elif selected_algo == "Priority":
        result = priority_scheduling(process_list)
    elif selected_algo == "SRTF":
        result = srtf(process_list)
        p = 1
    else:
        messagebox.showerror("Invalid Algorithm", "Please select a valid scheduling algorithm")
        return
    
    calculate_metrics(result)
    if p == 1 or p == 2:
        print(result)
        draw_gantt_chart_p(result, selected_algo)
    else:
        draw_gantt_chart(result, selected_algo)

# Quality of life UI enhancements
def add_placeholder(entry, placeholder):
    """Add placeholder text to an entry widget - works with both tk.Entry and ttk.Entry"""
    entry.insert(0, placeholder)
    
    # Handle different entry types (tk.Entry vs ttk.Entry)
    if isinstance(entry, tk.Entry):
        entry.config(fg='grey')
    else:  # ttk.Entry - use style
        style = ttk.Style()
        style.map('Placeholder.TEntry', foreground=[('focus', 'black'), ('!focus', 'grey')])
        entry['style'] = 'Placeholder.TEntry'

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            if isinstance(entry, tk.Entry):
                entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder)
            if isinstance(entry, tk.Entry):
                entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def create_tooltip(widget, text):
    """Create a tooltip for a widget"""
    def enter(event):
        global tooltip
        x = y = 0
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()
    
    def leave(event):
        global tooltip
        if 'tooltip' in globals():
            tooltip.destroy()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

def run_gui():
    """Run the GUI"""
    root = tk.Tk()
    root.title("Intelligent CPU Scheduler Simulator")
    root.geometry("550x850")
    
    # Set theme colors
    bg_color = "#f5f5f5"
    decent_color = "#3498db"
    acc_color = "#db3485"
    secondary_color = "#2ecc71"
    text_color = "#2c3e50"
    button_text_color = "white"
    accent_color = "#6a7370"
    
    root.configure(bg=bg_color)
    
    # Custom fonts
    title_font = font.Font(family="Ms Serif", size=20, weight="bold")
    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    normal_font = font.Font(family="Helvetica", size=10)
    
    # Apply a style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure colors for Treeview
    style.configure("Treeview", 
                    background=bg_color,
                    foreground=text_color,
                    rowheight=25,
                    fieldbackground=bg_color,
                    font=normal_font)
    style.configure("Treeview.Heading", 
                    font=header_font, 
                    background=accent_color, 
                    foreground="white")
    style.map('Treeview', background=[('selected', accent_color)])
    
    # Configure styles for entry widgets
    style.configure('Placeholder.TEntry', foreground='grey')
    
    # Configure colors for buttons
    style.configure("Accent.TButton", 
                    background=accent_color)
    style.map("Accent.TButton",
              foreground=[('pressed', button_text_color), ('active', button_text_color)],
              background=[('pressed', '!disabled', accent_color), ('active', accent_color)])
              
    style.configure("Secondary.TButton", 
                    background=secondary_color)
    style.map("Secondary.TButton",
              foreground=[('pressed', button_text_color), ('active', button_text_color)],
              background=[('pressed', '!disabled', secondary_color), ('active', secondary_color)])
              
    style.configure("Warning.TButton", 
                    background="#e74c3c")
    style.map("Warning.TButton",
              foreground=[('pressed', button_text_color), ('active', button_text_color)],
              background=[('pressed', '!disabled', "#e74c3c"), ('active', "#e74c3c")])
    
    # Main container - using Frame instead of ttk.Frame for background color control
    main_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title with logo-like styling
    title_frame = tk.Frame(main_frame, bg=bg_color)
    title_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = tk.Label(
        title_frame, 
        text="Intelligent CPU Scheduler",
        font=title_font,
        foreground=acc_color,
        bg=bg_color
    )
    title_label.pack(side=tk.LEFT)
    
    # Subtitle
    subtitle_label = tk.Label(
        title_frame,
        text="- Simulation Tool",
        font=header_font,
        foreground=decent_color,
        bg=bg_color
    )
    subtitle_label.pack(side=tk.LEFT, padx=(5, 0), pady=(5, 0))
    
    # Input Section with card-like styling
    input_card = tk.LabelFrame(main_frame, text="Process Information", font=header_font, bg=bg_color, padx=15, pady=15)
    input_card.pack(fill=tk.X, pady=10)
    
    # Grid for inputs
    input_grid = tk.Frame(input_card, bg=bg_color)
    input_grid.pack(fill=tk.X, expand=True)
    
    # Process ID
    tk.Label(input_grid, text="Process ID:", font=normal_font, bg=bg_color).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    entry_pid = tk.Entry(input_grid, width=15, font=normal_font)
    entry_pid.grid(row=0, column=1, padx=10, pady=8, sticky="w")
    create_tooltip(entry_pid, "Enter a unique process identifier")
    
    # Arrival Time
    tk.Label(input_grid, text="Arrival Time:", font=normal_font, bg=bg_color).grid(row=0, column=2, padx=10, pady=8, sticky="w")
    entry_arrival = tk.Entry(input_grid, width=15, font=normal_font)
    entry_arrival.grid(row=0, column=3, padx=10, pady=8, sticky="w")
    create_tooltip(entry_arrival, "Time at which process arrives")
    
    # Burst Time
    tk.Label(input_grid, text="Burst Time:", font=normal_font, bg=bg_color).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    entry_burst = tk.Entry(input_grid, width=15, font=normal_font)
    entry_burst.grid(row=1, column=1, padx=10, pady=8, sticky="w")
    create_tooltip(entry_burst, "CPU time required by the process")
    
    # Priority
    tk.Label(input_grid, text="Priority:", font=normal_font, bg=bg_color).grid(row=1, column=2, padx=10, pady=8, sticky="w")
    entry_priority = tk.Entry(input_grid, width=15, font=normal_font)
    entry_priority.grid(row=1, column=3, padx=10, pady=8, sticky="w")
    add_placeholder(entry_priority, "optional")
    create_tooltip(entry_priority, "Lower value means higher priority (optional)")
    
    # Action buttons for the input section
    button_frame = tk.Frame(input_card, bg=bg_color)
    button_frame.pack(fill=tk.X,  pady=(10, 0))

    button_grid = tk.Frame(button_frame, bg=bg_color)
    button_grid.pack(fill=tk.X, expand=True)

    add_button = tk.Button(
        button_grid,
        text="Add Process",
        bg=secondary_color,
        fg=button_text_color,
        font="comic",
        width=15,
        relief=tk.RAISED,
        cursor="hand2"
    )
    add_button.grid(row=0, column=3, padx=10, pady=8, sticky="w")
    # # Tree actions
    # tree_actions = tk.Frame(input_card, bg=bg_color)
    # tree_actions.pack(fill=tk.X, pady=(10, 0))
    
    remove_button = tk.Button(
        button_grid,
        text="Remove Process",
        bg="#e74c3c",
        fg=button_text_color,
        font="comic",
        width=15,
        relief=tk.RAISED,
        cursor="hand2"
    )
    remove_button.grid(row=0, column=4, padx=10, pady=8, sticky="w")
    
    # Process List as Treeview
    # process_frame = tk.LabelFrame(main_frame, text="Process Queue", font=header_font, bg=bg_color, padx=15, pady=15)
    # process_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    process_frame = tk.LabelFrame(main_frame, text="Process Queue", font=header_font, bg=bg_color, padx=15, pady=15)
    process_frame.pack(fill=tk.BOTH, expand=False, pady=10)  # `expand=False` makes it less dominant
    process_frame.configure(height=50)  # Shrinks the height slightly
    
    # Create Treeview with scrollbar
    tree_frame = tk.Frame(process_frame, bg=bg_color)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    process_tree = ttk.Treeview(
        tree_frame, 
        columns=("pid", "arrival", "burst", "priority"),
        show="headings",
        height=8,
        yscrollcommand=tree_scroll.set
    )
    
    process_tree.heading("pid", text="Process ID")
    process_tree.heading("arrival", text="Arrival Time")
    process_tree.heading("burst", text="Burst Time")
    process_tree.heading("priority", text="Priority")
    
    process_tree.column("pid", width=100, anchor="center")
    process_tree.column("arrival", width=100, anchor="center")
    process_tree.column("burst", width=100, anchor="center")
    process_tree.column("priority", width=100, anchor="center")
    
    process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree_scroll.config(command=process_tree.yview)
    
    
    
    # Suggestion and Algorithm frame
    # algo_frame = tk.LabelFrame(main_frame, text="Algorithm Selection", font=header_font, bg=bg_color, padx=15, pady=15)
    # algo_frame.pack(fill=tk.X, pady=10)
    # Increase the size of the Algorithm Selection section
    algo_frame = tk.LabelFrame(main_frame, text="Algorithm Selection", font=header_font, bg=bg_color, padx=15, pady=15)
    algo_frame.pack(fill=tk.BOTH, expand=True, pady=10)  # `expand=True` makes it larger
    algo_frame.pack_propagate(False)  # Prevent the frame from shrinking to its contents
    algo_frame.configure(height=250,width=550)  # Increase the height to make it more spacious

    
    # Suggested Algorithm
    algo_label = tk.Label(
        algo_frame, 
        text="Suggested Algorithm: None", 
        font=header_font,
        foreground=secondary_color,
        bg=bg_color
    )
    algo_label.pack(anchor="w", pady=(0, 10))
    
    # Best Algorithm metrics
    best_tt_label = tk.Label(
        algo_frame,
        text="Best TT: None | Best WT: None",
        font=normal_font,
        foreground=text_color,
        bg=bg_color
    )
    best_tt_label.pack(anchor="w", pady=(0, 10))
    
    # Algorithm Selection dropdown and run button
    algo_select_frame = tk.Frame(algo_frame, bg=bg_color)
    algo_select_frame.pack(fill=tk.X, expand=True)
    
    algo_var = tk.StringVar(value="Select Algorithm")
    algo_dropdown = ttk.Combobox(
        algo_select_frame,
        textvariable=algo_var,
        values=["FCFS", "SJF", "Round Robin", "Priority", "SRTF"],
        state="readonly",
        font=normal_font,
        width=30
    )
    algo_dropdown.pack(side=tk.LEFT, padx=5)
    
    run_button = tk.Button(
        algo_select_frame,
        text="Run Simulation",
        bg="grey",
        fg=button_text_color,
        font=normal_font,
        width=18,
        relief=tk.RAISED,
        cursor="hand2"
    )
    run_button.pack(side=tk.RIGHT, padx=5)
    
    # Connect button commands with functions
    add_button.config(command=lambda: add_process(
        entry_pid, entry_arrival, entry_burst, entry_priority, 
        process_tree, algo_label, algo_var, best_tt_label
    ))
    
    remove_button.config(command=lambda: remove_process(
        process_tree, algo_label, algo_var, best_tt_label
    ))
    
    run_button.config(command=lambda: run_simulation(algo_var.get()))
    
    # Status bar at the bottom
    status_bar = tk.Label(
        root, 
        text="Ready to simulate CPU scheduling",
        relief=tk.SUNKEN,
        anchor=tk.W,
        padx=10,
        pady=2,
        font=normal_font
    )
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()