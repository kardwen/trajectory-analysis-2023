import tkinter as tk
import tkinter.filedialog as filedialog
import matplotlib.pyplot as plt
import glob

def plot_trajectories():
    # Clear any existing plots
    plt.clf()

    # Get the selected file paths
    selected_files = listbox.curselection()
    file_paths = [file_list[i] for i in selected_files]

    # Get the selected plot style
    plot_style = style_var.get()

    # Define a list of colors for each plot
    colors = ['red', 'blue', 'green', 'orange', 'purple']

    # Plot each selected trajectory file with the chosen style and a different color
    for i, file_path in enumerate(file_paths):
        # Create a new figure and subplot
        fig, ax = plt.subplots()

        # Read trajectory data from file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extract x and y coordinates from the data
        x = []
        y = []
        for line in lines:
            line_data = line.strip().split(' ')
            x.append(float(line_data[0]))
            y.append(float(line_data[1]))

        # Plot the trajectory with the chosen style and color
        ax.plot(x, y, color=colors[i % len(colors)], linestyle=plot_style)
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title(file_path)

    # Display each plot separately
    plt.show()

def browse_files():
    # Clear the current listbox selection and items
    listbox.selection_clear(0, tk.END)
    listbox.delete(0, tk.END)

    # Open a file dialog to choose trajectory files
    file_paths = filedialog.askopenfilenames(filetypes=[('Text files', '*.txt')])

    # Populate the listbox with the selected file paths
    for file_path in file_paths:
        listbox.insert(tk.END, file_path)

# Create the main GUI window
window = tk.Tk()
window.title("Trajectory Plotter")

# Create a listbox to display the selected trajectories
listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
listbox.pack(padx=10, pady=10)

# Create a button to browse and select trajectory files
browse_button = tk.Button(window, text="Browse Files", command=browse_files)
browse_button.pack(pady=5)

# Create a label and dropdown menu to choose the plot style
style_label = tk.Label(window, text="Plot Style:")
style_label.pack()
style_var = tk.StringVar()
style_dropdown = tk.OptionMenu(window, style_var, "solid", "dashed", "dotted", "dashdot")
style_dropdown.pack()

# Create a button to plot the selected trajectories
plot_button = tk.Button(window, text="Plot Trajectories", command=plot_trajectories)
plot_button.pack(pady=5)

# Get a list of all .txt files in the directory
file_list = glob.glob('*.txt')

# Populate the listbox with the available trajectory files
for file_path in file_list:
    listbox.insert(tk.END, file_path)

# Start the GUI event loop
window.mainloop()
