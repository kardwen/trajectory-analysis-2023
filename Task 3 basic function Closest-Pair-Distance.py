import math
import os
import tkinter as tk
from tkinter import filedialog

def euclidean_distance(p1, p2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_pair_distance(trajectory1, trajectory2):
    """Calculate the Closest Pair Distance between two trajectories."""
    min_distance = float('inf')

    for point1 in trajectory1:
        for point2 in trajectory2:
            distance = euclidean_distance(point1, point2)
            min_distance = min(min_distance, distance)

    return min_distance

def read_trajectory_file(file_path):
    trajectory = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            x, y = map(float, values[:2])
            trajectory.append((x, y))
    return trajectory

def select_trajectory_file(entry_widget):
    file_path = filedialog.askopenfilename(initialdir="./", title="Select Trajectory File", filetypes=(("Text Files", "*.txt"),))
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def calculate_closest_pair_distance():
    file_path1 = entry_trajectory1.get()
    file_path2 = entry_trajectory2.get()

    if file_path1 and file_path2:
        trajectory1 = read_trajectory_file(file_path1)
        trajectory2 = read_trajectory_file(file_path2)

        distance = closest_pair_distance(trajectory1, trajectory2)
        lbl_result.config(text="Closest Pair Distance: {:.6f}".format(distance))
    else:
        lbl_result.config(text="Please select two trajectory files.")

# Create the GUI window
window = tk.Tk()
window.title("Closest Pair Distance Calculator")

# Create and position the widgets
lbl_trajectory1 = tk.Label(window, text="Trajectory 1:")
lbl_trajectory1.grid(row=0, column=0, sticky="w")

entry_trajectory1 = tk.Entry(window, width=40)
entry_trajectory1.grid(row=0, column=1)

btn_select_trajectory1 = tk.Button(window, text="Select", command=lambda: select_trajectory_file(entry_trajectory1))
btn_select_trajectory1.grid(row=0, column=2)

lbl_trajectory2 = tk.Label(window, text="Trajectory 2:")
lbl_trajectory2.grid(row=1, column=0, sticky="w")

entry_trajectory2 = tk.Entry(window, width=40)
entry_trajectory2.grid(row=1, column=1)

btn_select_trajectory2 = tk.Button(window, text="Select", command=lambda: select_trajectory_file(entry_trajectory2))
btn_select_trajectory2.grid(row=1, column=2)

btn_calculate = tk.Button(window, text="Calculate", command=calculate_closest_pair_distance)
btn_calculate.grid(row=2, column=0, columnspan=3)

lbl_result = tk.Label(window, text="")
lbl_result.grid(row=3, column=0, columnspan=3)

# Get all .txt files in the current directory
file_list = [file for file in os.listdir() if file.endswith(".txt")]

# Display the .txt files in the GUI
if file_list:
    lbl_file_list = tk.Label(window, text="Available Trajectory Files:")
    lbl_file_list.grid(row=4, column=0, columnspan=3)

    for i, file_name in enumerate(file_list):
        lbl_file = tk.Label(window, text=file_name)
        lbl_file.grid(row=i+5, column=0, columnspan=3)
else:
    lbl_no_files = tk.Label(window, text="No .txt files found in the directory.")
    lbl_no_files.grid(row=4, column=0, columnspan=3)

# Start the GUI event loop
window.mainloop()
