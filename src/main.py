import matplotlib
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

matplotlib.use("TkAgg")  # Set the backend before importing pyplot
import tkinter as tk
from pathlib import Path
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex

from app import utils
from app.functions import douglasPeucker, slidingWindow

# Import trajectories
trajectoriesDir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectoriesDir))

# Create a Tkinter GUI
root = tk.Tk()
root.title("Trajectory Visualization")
root.geometry("800x600")

# Create a frame to contain the listbox
listbox_frame = ttk.Frame(root)
listbox_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH)


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
            colorMap(i) for i in np.linspace(0, 1, len(selected_trajectory_ids))
        ]
    else:
        color_list = [colorMap(i) for i in np.linspace(0, 1, len(listOfTrajectories))]

    count = 0
    for idx, traj in enumerate(listOfTrajectories):
        if traj.number in selected_trajectory_ids:
            count += 1
            # Preprocessing
            if data_reduction_checkbox_var.get():
                algorithm = algorithm_var.get()
                try:
                    epsilon = float(epsilon_entry.get())
                    if algorithm == "Douglas-Peucker":
                        traj = douglasPeucker(traj, epsilon)
                    elif algorithm == "Sliding Window":
                        traj = slidingWindow(traj, epsilon)
                except ValueError:
                    pass

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
    axis.axis("equal")
    figure.tight_layout()
    figure.canvas.draw()


# Function to select all trajectories in the Listbox
def select_all_trajectories():
    listbox.select_set(0, tk.END)
    update_plot()


# Function to deselect all trajectories in the Listbox
def deselect_all_trajectories():
    listbox.selection_clear(0, tk.END)
    update_plot()


# Create a Label for trajectory number
label_trajectory_number = ttk.Label(listbox_frame, text="Trajectories:")
label_trajectory_number.pack(side=tk.TOP, padx=10, pady=(10, 0), anchor="w")

# Initial plot with all trajectories and points highlighted
colorMap = matplotlib.colormaps["viridis"]

# Create a Listbox to select multiple trajectory IDs and display colors
listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=15)
colors = [colorMap(i) for i in np.linspace(0, 1, len(listOfTrajectories))]
for i, origTrajectory in enumerate(listOfTrajectories):
    color_hex = rgb2hex(colors[i % len(colors)])  # Convert RGBA to hexadecimal color
    listbox.insert(tk.END, f"Trajectory {origTrajectory.number}")
    listbox.itemconfig(i, {"bg": "white", "selectbackground": color_hex})
listbox.pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create buttons to select and deselect all trajectories
select_all_button = ttk.Button(
    listbox_frame, text="Select All", command=select_all_trajectories
)
select_all_button.pack(side=tk.TOP, padx=10, pady=(0, 5), fill=tk.X)

deselect_all_button = ttk.Button(
    listbox_frame, text="Deselect All", command=deselect_all_trajectories
)
deselect_all_button.pack(side=tk.TOP, padx=10, pady=(0, 5), fill=tk.X)

# Create a checkbox for increasing contrast
contrast_checkbox_var = tk.BooleanVar()
contrast_checkbox = ttk.Checkbutton(
    listbox_frame,
    text="Increase Contrast",
    variable=contrast_checkbox_var,
    command=update_plot,
)
contrast_checkbox.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

# Create a checkbox to toggle point highlighting
highlight_checkbox_var = tk.BooleanVar()
highlight_checkbox = ttk.Checkbutton(
    listbox_frame,
    text="Highlight Points",
    variable=highlight_checkbox_var,
    command=update_plot,
)
highlight_checkbox.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

# Create a horizontal line below "Highlight Points"
highlight_separator = ttk.Separator(listbox_frame, orient="horizontal")
highlight_separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Preprocessing header
preprocessing_label = ttk.Label(listbox_frame, text="Preprocessing")
preprocessing_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

# Apply algorithm checkbox
data_reduction_checkbox_var = tk.BooleanVar()
data_reduction_checkbox = ttk.Checkbutton(
    listbox_frame,
    text="Enable Data Reduction",
    variable=data_reduction_checkbox_var,
    command=update_plot,
)
data_reduction_checkbox.pack(side=tk.TOP, padx=10, pady=(0, 5), fill=tk.X)

# Algorithm selection
algorithm_var = tk.StringVar()
algorithm_var.set("Douglas-Peucker")  # Default algorithm
algorithm_label = ttk.Label(listbox_frame, text="Select Algorithm:")
algorithm_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

algorithm_menu = ttk.OptionMenu(
    listbox_frame,
    algorithm_var,
    "Douglas-Peucker",
    "Douglas-Peucker",
    "Sliding Window",
)
algorithm_menu.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

# Epsilon entry
epsilon_label = ttk.Label(listbox_frame, text="Epsilon Value:")
epsilon_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

epsilon_entry = ttk.Entry(listbox_frame)
epsilon_entry.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
epsilon_entry.insert(0, "0.0001")  # Default epsilon value

# Create a frame to contain the plot and toolbar
plot_frame = ttk.Frame(root)
plot_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create a matplotlib figure and axis for the plot
figure = plt.figure(figsize=(6, 4), dpi=100)
axis = figure.add_subplot(1, 1, 1)


# Function to handle listbox select event
def on_listbox_select(*args):
    update_plot()


# Function to handle epsilon entry change event
def on_epsilon_change(*args):
    try:
        # Try converting the entered value to a float
        epsilon = float(epsilon_entry.get())
        if epsilon <= 0:
            raise ValueError("Epsilon value must be greater than zero.")
        epsilon_label.configure(foreground="black")
        update_plot()
    except ValueError:
        epsilon_label.configure(foreground="red")
        pass


# Function to handle algorithm selection change event
def on_algorithm_select(*args):
    update_plot()


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


# Function to handle the "WM_DELETE_WINDOW" event
def on_closing():
    root.quit()


# Bind the "WM_DELETE_WINDOW" event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()
