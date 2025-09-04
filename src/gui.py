import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import string

# Define colors
bg_color = "#334257"  # Background color for the window
widget_bg_color = "#476072"  # Background color for widgets
text_color = "#FFFFFF"  # Text color
button_color = "#FFD32D"  # Button background color
button_text_color = bg_color  # Button text color
error_color = "#FF5959"  # Error message background color

file_names = []

def extractor(s):
    last_slash_index = s.rfind('/')
    file_name = s[last_slash_index + 1:]
    return file_name

def execute_command(command_string):
    try:
        result = subprocess.run(command_string, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        error = result.stderr.decode('utf-8')
        
        if output:
            messagebox.showinfo("Output", output)
        if error:
            messagebox.showerror("Error", error)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Execution Error", f"Error executing command '{command_string}': {e}")

def go():
    if len(file_names) < 3:
        messagebox.showwarning("Warning", "Please upload all three required files.")
        return
    execute_command("g++ -o main src/main.cpp")
    command2 = ".\\main examples/tests/" + extractor(file_names[0]) + " examples/tests/" + extractor(file_names[1]) + " examples/tests/" + extractor(file_names[2])
    execute_command(command2)

def go_2():
    execute_command("code src/Graphing/output.sim")
    execute_command("python -m src.Graphing.simulation_graphing")

def upload_file():
    filename = filedialog.askopenfilename()
    if filename:
        file_names.append(filename)
        update_uploaded_files_label()

def update_uploaded_files_label():
    files = '\n'.join([extractor(fn) for fn in file_names])
    label.config(text=f"Uploaded Files:\n{files}")

root = tk.Tk()
root.title("Logic Simulator")
root.config(bg=bg_color)

title_frame = tk.Frame(root, bg=bg_color)
title_frame.pack(padx=10, pady=(10, 0))
project_title = tk.Label(title_frame, text="Logic Simulator", bg=bg_color, fg=text_color, font=("Helvetica", 24))
project_title.pack()

frame = tk.Frame(root, bg=bg_color)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="No files uploaded.", padx=10, pady=10, bg=widget_bg_color, fg=text_color, font=("Helvetica", 12))
label.pack()

button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)

upload_buttons = [
    ("Upload LIB File", upload_file),
    ("Upload CIR File", upload_file),
    ("Upload STIM File", upload_file),
    ("Run Code", go),
    ("Open Simulation File", go_2)
]

for text, command in upload_buttons:
    button = tk.Button(button_frame, text=text, command=command, bg=button_color, fg=button_text_color, font=("Helvetica", 14), height=2, width=20)
    button.pack(fill=tk.X, pady=2, padx=10)

root.mainloop()
