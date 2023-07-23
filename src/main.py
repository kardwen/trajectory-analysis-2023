import tkinter as tk
from pathlib import Path
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.colors import rgb2hex

from app import utils
from app.functions import (
    closestPairDistance,
    douglasPeucker,
    dynamicTimeWarping,
    slidingWindow,
)
from app.trajectory import Trajectory

matplotlib.use("TkAgg")  # Set the backend before importing pyplot

# Import trajectories
trajectoriesDir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectoriesDir))


# Function to update the plot with selected trajectories and points highlight
def update_plot():
    selected_trajectory_ids = []
    for idx in listbox.curselection():
        item = listbox.get(idx)
        trajectory_number = int(
            item.split()[-1]
        )  # Extract the numeric part of the string
        selected_trajectory_ids.append(trajectory_number)
    highlight_points = (
        highlight_checkbox_var.get()
    )  # Get the state of the highlight checkbox
    axis.clear()

    increase_contrast = (
        contrast_checkbox_var.get()
    )  # Get the state of the highlight checkbox

    if increase_contrast:
        color_list = [
            colorMap(i) for i in np.linspace(0, 1, max(len(selected_trajectory_ids), 3))
        ]
    else:
        color_list = [colorMap(i) for i in np.linspace(0, 1, len(listOfTrajectories))]

    simplify = data_reduction_checkbox_var.get()

    # Distance metrics
    if len(selected_trajectory_ids) == 2:
        traj0 = None
        traj1 = None
        for trajectory in listOfTrajectories:
            if trajectory.number == selected_trajectory_ids[0]:
                traj0 = trajectory
                if simplify:
                    traj0 = preprocess_trajectory(traj0)
            if trajectory.number == selected_trajectory_ids[1]:
                traj1 = trajectory
                if simplify:
                    traj1 = preprocess_trajectory(traj1)
        closest_pair_dist = closestPairDistance(traj0, traj1)
        dtw_dist = dynamicTimeWarping(traj0, traj1)

        distance_measures_help_label.pack_forget()
        distance_measures_label.pack(side=tk.TOP, padx=10, pady=5, anchor="center")
        distance_measures_label.config(
            text=f"Closest Pair Distance:\n{closest_pair_dist:.12f}\n"
            + f"Dynamic Time Warping:\n{dtw_dist:.12f}"
        )

    else:
        distance_measures_help_label.pack(side=tk.TOP, padx=10, pady=5, anchor="center")
        distance_measures_label.pack_forget()

    count = 0
    for idx, traj in enumerate(listOfTrajectories):
        if traj.number in selected_trajectory_ids:
            count += 1
            # Preprocessing
            if simplify:
                traj = preprocess_trajectory(traj)

            color = color_list[count - 1] if increase_contrast else color_list[idx]

            # Set listbox item colors
            color_hex = rgb2hex(color)  # Convert RGBA to hexadecimal color
            listbox.itemconfig(idx, {"bg": "white", "selectbackground": color_hex})

            # Plot trajectories
            x = [point.x for point in traj.points]
            y = [point.y for point in traj.points]
            if highlight_points:
                axis.plot(
                    x,
                    y,
                    "o",
                    markersize=3,
                    alpha=0.5,
                    color=color,
                    label=f"Trajectory {traj.number}",
                )
            axis.plot(
                x,
                y,
                color=color,
                label=f"Trajectory {traj.number}",
            )
 
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.grid(True)
    figure.canvas.draw()


def preprocess_trajectory(trajectory: Trajectory) -> Trajectory:
    algorithm = algorithm_var.get()
    try:
        epsilon = float(epsilon_entry.get())
        if algorithm == "Douglas-Peucker":
            return douglasPeucker(trajectory, epsilon)
        elif algorithm == "Sliding Window":
            return slidingWindow(trajectory, epsilon)
    except ValueError:
        pass


# Function to select all trajectories in the Listbox
def select_all_trajectories():
    listbox.select_set(0, tk.END)
    update_plot()


# Function to deselect all trajectories in the Listbox
def deselect_all_trajectories():
    listbox.selection_clear(0, tk.END)
    update_plot()


# Function to handle epsilon entry change event
def on_epsilon_change(*args):
    try:
        # Try converting the entered value to a float
        epsilon = float(epsilon_entry.get())
        if epsilon < 0:
            raise ValueError("Value for epsilon cannot be a negative number.")
        epsilon_label.configure(foreground="black")
        update_plot()
    except ValueError:
        epsilon_label.configure(foreground="red")
        pass


# Function to handle algorithm selection change event
def on_algorithm_select(*args):
    update_plot()


# Function to handle listbox select event
def on_listbox_select(*args):
    update_plot()


# Function to handle the "WM_DELETE_WINDOW" event
def on_closing():
    root.quit()


# Create a Tkinter GUI
root = tk.Tk()
root.title("Trajectory Visualization")
root.geometry("1200x750")

# Create a frame to contain the listbox
sidebar_frame = ttk.Frame(root)
sidebar_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH)

# Set a minimum width
sidebar_frame.update_idletasks()  # Ensure widgets are drawn before setting the minsize
sidebar_frame.update()  # Ensure widgets are drawn before setting the minsize
sidebar_frame.pack_propagate(False)
sidebar_frame.config(width=max(sidebar_frame.winfo_reqwidth(), 180))

# Create a Label for trajectory number
label_trajectory_number = ttk.Label(sidebar_frame, text="Trajectories:")
label_trajectory_number.pack(side=tk.TOP, padx=10, pady=(10, 0), anchor="w")

# Initial plot with all trajectories and points highlighted
colorMap = matplotlib.colormaps["viridis"]

listbox_frame = ttk.Frame(sidebar_frame)
listbox_frame.pack(side=tk.TOP, padx=0, pady=0, fill=tk.BOTH)

# Create a Listbox to select multiple trajectory IDs and display colors
listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=15)
for i, origTrajectory in enumerate(listOfTrajectories):
    listbox.insert(tk.END, f"Trajectory {origTrajectory.number}")
    listbox.itemconfig(i, {"bg": "white", "selectbackground": "black"})
listbox.pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create buttons to select and deselect all trajectories
select_all_button = ttk.Button(
    sidebar_frame, text="Select All", command=select_all_trajectories
)
select_all_button.pack(side=tk.TOP, padx=10, pady=(0, 5), fill=tk.X)

deselect_all_button = ttk.Button(
    sidebar_frame, text="Deselect All", command=deselect_all_trajectories
)
deselect_all_button.pack(side=tk.TOP, padx=10, pady=(0, 5), fill=tk.X)

# Create a checkbox for increasing contrast
contrast_checkbox_var = tk.BooleanVar(value=True)
contrast_checkbox = ttk.Checkbutton(
    sidebar_frame,
    text="Increase Contrast",
    variable=contrast_checkbox_var,
    command=update_plot,
)
contrast_checkbox.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

# Create a checkbox to toggle point highlighting
highlight_checkbox_var = tk.BooleanVar()
highlight_checkbox = ttk.Checkbutton(
    sidebar_frame,
    text="Highlight Points",
    variable=highlight_checkbox_var,
    command=update_plot,
)
highlight_checkbox.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

# Create a horizontal line below "Highlight Points"
preprocessing_separator = ttk.Separator(sidebar_frame, orient="horizontal")
preprocessing_separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Preprocessing header
preprocessing_label = ttk.Label(sidebar_frame, text="Preprocessing")
preprocessing_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

# Apply algorithm checkbox
data_reduction_checkbox_var = tk.BooleanVar()
data_reduction_checkbox = ttk.Checkbutton(
    sidebar_frame,
    text="Simplify Trajectories",
    variable=data_reduction_checkbox_var,
    command=update_plot,
)
data_reduction_checkbox.pack(side=tk.TOP, padx=10, pady=(0, 5), fill=tk.X)

# Algorithm selection
algorithm_var = tk.StringVar()
algorithm_var.set("Douglas-Peucker")  # Default algorithm
algorithm_label = ttk.Label(sidebar_frame, text="Select Algorithm:")
algorithm_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

algorithm_menu = ttk.OptionMenu(
    sidebar_frame,
    algorithm_var,
    "Douglas-Peucker",
    "Douglas-Peucker",
    "Sliding Window",
)
algorithm_menu.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

# Epsilon entry
epsilon_label = ttk.Label(sidebar_frame, text="Epsilon Value:")
epsilon_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

epsilon_entry = ttk.Entry(sidebar_frame)
epsilon_entry.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
epsilon_entry.insert(0, "0.00005")  # Default epsilon value

distance_metrics_separator = ttk.Separator(sidebar_frame, orient="horizontal")
distance_metrics_separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

distance_metrics_label = ttk.Label(sidebar_frame, text="Distance Metrics")
distance_metrics_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

distance_measures_help_label = ttk.Label(
    sidebar_frame,
    text="Select two trajectories\nfor calculating\ndistance measures.",
    anchor="center",
    justify="center",
)
distance_measures_help_label.pack(side=tk.TOP, padx=10, pady=5, anchor="center")

distance_measures_label = ttk.Label(
    sidebar_frame, text="", anchor="center", justify="center"
)

# Create a frame to contain the plot and toolbar
plot_frame = ttk.Frame(root)
plot_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create a matplotlib figure and axis for the plot
figure = plt.figure(figsize=(6, 4), dpi=100)
axis = figure.add_subplot(1, 1, 1)
axis.axis("equal")
figure.tight_layout()

# Bind the algorithm variable's Configure event to the on_algorithm_select function
algorithm_var.trace("w", on_algorithm_select)

# Bind the KeyRelease event to the on_epsilon_change function
epsilon_entry.bind("<KeyRelease>", on_epsilon_change)

# Bind the listbox select event to the on_listbox_select function
listbox.bind("<<ListboxSelect>>", on_listbox_select)

# Embed the matplotlib figure in the Tkinter window
canvas = FigureCanvasTkAgg(figure, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a Navigation Toolbar for zooming, panning, and saving
toolbar = NavigationToolbar2Tk(canvas, plot_frame)
toolbar.pan()
toolbar.update()  # Required to initialize the toolbar
toolbar.pack(side=tk.BOTTOM, fill=tk.X)

# Initial plot with all trajectories and points highlighted
select_all_trajectories()

# Bind the "WM_DELETE_WINDOW" event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()
