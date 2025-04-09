import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
def draw_gantt_chart(processes,name):
    """Draw Gantt Chart for Process Execution Timeline"""
    start_times = [p['start_time'] for p in processes]
    burst_times = [p['burst_time'] for p in processes]
    process_ids = [p['id'] for p in processes]

    plt.figure(figsize=(10, 5))

    for i, process in enumerate(processes):
        plt.barh(f"P{process_ids[i]}", burst_times[i], left=start_times[i], edgecolor='black', color='skyblue')

        # Add process ID as label in the center of each bar
        mid_point = start_times[i] + burst_times[i] / 2
        plt.text(mid_point, f"P{process_ids[i]}", f"P{process_ids[i]}", ha='center', va='center',
                 color='black', fontsize=10, fontweight='bold')

    plt.xlabel('Time')
    plt.title(name)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
def draw_gantt_chart_p(processes,name):
    """Draw Gantt Chart for Process Execution Timeline"""
    plt.figure(figsize=(10, 5))

    for process in processes:
        for segment in process['segments']:
            start_time, end_time = segment
            plt.barh(f"P{process['id']}", end_time - start_time, left=start_time, edgecolor='black', color='skyblue')
            mid_point = start_time + (end_time - start_time) / 2
            plt.text(mid_point, f"P{process['id']}", f"P{process['id']}({start_time}-{end_time})", ha='center', va='center',
                     color='black', fontsize=10, fontweight='bold')

    plt.xlabel('Time')
    plt.title(name)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.xlim(left=0)
    plt.tight_layout()
    plt.show()
def draw_gantt_chart_r(processes,name):
    """Draw Gantt Chart for Round Robin Process Execution Timeline"""
    plt.figure(figsize=(10, 5))

    for process in processes:
        for segment in process['segments']:
            start_time, end_time = segment
            plt.barh(f"P{process['id']}", end_time - start_time, left=start_time, edgecolor='black', color='skyblue')
            mid_point = start_time + (end_time - start_time) / 2
            plt.text(mid_point, f"P{process['id']}", f"{start_time}-{end_time}", ha='center', va='center',
                     color='black', fontsize=8, fontweight='bold')

    plt.xlabel('Time')
    plt.ylabel('Processes')
    plt.title(name)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.xlim(left=0)
    plt.tight_layout()
    plt.show()

# def calculate_metrics(processes):
#     """Calculate and Display Performance Metrics in a Popup"""
#     total_waiting_time = sum(p['waiting_time'] for p in processes)
#     total_turnaround_time = sum(p['turnaround_time'] for p in processes)
#     total_completion_time = sum(p['completion_time'] for p in processes)
#     avg_completion_time = total_completion_time / len(processes)
#     avg_turnaround_time = total_turnaround_time / len(processes)
#     avg_waiting_time = total_waiting_time / len(processes)

#     # metrics
#     metrics = "\n".join([
#         f"Process {process['id']}:\n"
#         f"Start Time: {process['start_time']}\n"
#         f"Completion Time: {process['completion_time']}\n"
#         f"Turnaround Time: {process['turnaround_time']}\n"
#         f"Waiting Time: {process['waiting_time']}"
#         for process in processes
#     ])

#     summary = (
#         f"\n\nAverage Completion Time: {avg_completion_time:.2f}\n"
#         f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
#         f"Average Waiting Time: {avg_waiting_time:.2f}"
#     )

#     full_message = metrics + summary
#     metrics_window = tk.Toplevel()
#     metrics_window.title("Performance Metrics")
#     metrics_window.geometry("250x400") 
#     metrics_window.configure(bg="#f0f0f0")

#     # Add a scrollable text widget to display the metrics
#     text_widget = tk.Text(metrics_window, wrap="word", bg="#f0f0f0", fg="black", font=("Arial", 12))
#     text_widget.insert("1.0", full_message)
#     text_widget.config(state="disabled")  # Make the text widget read-only
#     text_widget.pack(expand=True, fill="both", padx=10, pady=10)

#     # Add a close button
#     close_button = tk.Button(metrics_window, text="Close", command=metrics_window.destroy, bg="#f44336", fg="white")
#     close_button.pack(pady=10)
#     # print('om')
#     # # Display the metrics in a popup
#     # messagebox.showinfo("Performance Metrics", full_message)
def calculate_metrics(processes):
    """Calculate and Display Performance Metrics in a Popup"""
    total_waiting_time = sum(p['waiting_time'] for p in processes)
    total_turnaround_time = sum(p['turnaround_time'] for p in processes)
    total_completion_time = max(p['completion_time'] for p in processes)
    # total_completion_time = processes[-1]['completion_time']  # Assuming the last process has the total completion time
    completion_time = total_completion_time
    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)

    # Beautified metrics
    metrics = "\n".join([
        f"Process {process['id']:>2}:\n"
        f"  Start Time      : {process['start_time']}\n"
        f"  Completion Time : {process['completion_time']}\n"
        f"  Turnaround Time : {process['turnaround_time']}\n"
        f"  Waiting Time    : {process['waiting_time']}\n"
        for process in processes
    ])

    # Beautified summary
    summary = (
        f"\n{'-' * 30}\n"
        f"  Average Metrics\n"
        f"{'-' * 30}\n"
        f"  Completion Time : {completion_time:.2f}\n"
        f"  Average Turnaround Time : {avg_turnaround_time:.2f}\n"
        f"  Average Waiting Time    : {avg_waiting_time:.2f}\n"
        f"{'-' * 30}"
    )

    full_message = metrics + summary

    # Create a popup window to display the metrics
    metrics_window = tk.Toplevel()
    metrics_window.title("Performance Metrics")
    metrics_window.geometry("400x500") 
    metrics_window.configure(bg="#f0f0f0")

    # Add a scrollable text widget to display the metrics
    text_widget = tk.Text(metrics_window, wrap="word", bg="#f0f0f0", fg="black", font=("Courier New", 12))
    text_widget.insert("1.0", full_message)
    text_widget.config(state="disabled")  # Make the text widget read-only
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Add a close button
    close_button = tk.Button(metrics_window, text="Close", command=metrics_window.destroy, bg="#f44336", fg="white")
    close_button.pack(pady=10)
if __name__ == "__main__":
    pr = [
        {"id": 1, "segments": [[0, 2], [6, 8]], "burst_time": 5},
        {"id": 2, "segments": [[2, 4], [8, 9]], "burst_time": 3},
        {"id": 3, "segments": [[4, 6], [9, 11]], "burst_time": 8}
    ]
    draw_gantt_chart_r(pr,'rr')
