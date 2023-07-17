import os
import numpy as np
import tkinter as tk
from tkinter import filedialog

def dtw_distance(trajectory1, trajectory2):
    """Calculate the Dynamic Time Warping (DTW) distance between two trajectories."""
    len_traj1 = len(trajectory1)
    len_traj2 = len(trajectory2)

    # Create a distance matrix and initialize with infinite distances
    distance_matrix = np.zeros((len_traj1, len_traj2))
    distance_matrix.fill(np.inf)

    # Calculate the distance matrix using the DTW algorithm
    for i in range(len_traj1):
        for j in range(len_traj2):
            distance = np.linalg.norm(trajectory1[i, :2] - trajectory2[j, :2])
            if i == 0 and j == 0:
                distance_matrix[i][j] = distance
            else:
                distance_matrix[i][j] = distance + min(
                    distance_matrix[i-1][j],
                    distance_matrix[i][j-1],
                    distance_matrix[i-1][j-1]
                )

    return distance_matrix[-1][-1]

def read_trajectory_file(file_path):
    trajectory = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            x, y = map(float, values[:2])
            trajectory.append([x, y])
    return np.array(trajectory)

def select_trajectory_file(entry_widget):
    file_path = filedialog.askopenfilename(initialdir="./", title="Select Trajectory File", filetypes=(("Text Files", "*.txt"),))
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def calculate_dtw_distance():
    file_path1 = entry_trajectory1.get()
    file_path2 = entry_trajectory2.get()

    if file_path1 and file_path2:
        trajectory1 = read_trajectory_file(file_path1)
        trajectory2 = read_trajectory_file(file_path2)

        distance = dtw_distance(trajectory1, trajectory2)
        lbl_result.config(text="DTW Distance: {:.6f}".format(distance))
    else:
        lbl_result.config(text="Please select two trajectory files.")

# Create the GUI window
window = tk.Tk()
window.title("DTW Distance Calculator")

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

btn_calculate = tk.Button(window, text="Calculate", command=calculate_dtw_distance)
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
