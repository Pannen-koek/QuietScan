import customtkinter
import ttkbootstrap as tb
import tkinter as tk
from tkinter import Scrollbar
import os

from tkinter import Scrollbar
from about import about_text
from src.main.scan import system_scan

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def raise_frame(focusedFrame, button):
    # TODO Regenerate nav buttons with selected button different color if time allows in dev
    # customtkinter.CTkButton.configure(button, fg_color='black')
    focusedFrame.tkraise()


def scan_button_use(textbox):
    textbox.config(state=tb.NORMAL)
    textbox.insert(tb.END, "Executing system scan" + '\n')
    system_scan(textbox)
    textbox.config(state=tb.DISABLED)


def display_scan_history():
    # List all files in the scan_history folder
    scan_history_folder = os.path.join(CURRENT_DIR, "scan_history")
    if not os.path.exists(scan_history_folder):
        return []

    # Create buttons for each scan file
    scan_files = os.listdir(scan_history_folder)
    scan_buttons = []
    for filename in scan_files:
        formatted_filename = filename.replace(".txt", "")
        button = customtkinter.CTkButton(historyFrame, text=formatted_filename,
                                         command=lambda file=filename: show_scan_result(file), width=50)

        history_text_widget.window_create(tk.END, window=button)
        history_text_widget.insert(tk.END, "\n\n")  # Add spacing between buttons

    return scan_buttons


def layout_history_frame():
    global history_text_widget
    history_text_widget = None
    historyFrame = tb.Frame(root, width=1400, height=500)
    historyFrame.place(x=20, y=150)

    history_text_widget = tb.ScrolledText(historyFrame, height=27, width=300, wrap=tk.WORD, font=("Helvetica", 12))
    history_text_widget.pack(side="left", fill="both", expand=True)

    scan_buttons = display_scan_history()
    for button in scan_buttons:
        button.pack()


def show_scan_result(filename):
    scan_history_folder = os.path.join(CURRENT_DIR, "scan_history")
    file_path = os.path.join(scan_history_folder, filename)
    with open(file_path, "r") as file:
        content = file.read()

    result_window = tk.Toplevel()
    result_window.title("Scan Result")

    text_widget = tk.Text(result_window, wrap=tk.WORD, width=160, height=40)
    scrollbar = Scrollbar(result_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    text_widget.insert(tk.END, content)
    text_widget.config(state=tk.DISABLED)


def button_fill():
    print("Navigation Occurring")


root = tk.Tk()
root.title("QuietScan")
root.geometry('1280x720')

f1 = tk.Frame(root)

# header frame
headerFrame = tb.Frame(root, width=1200, height=150)
headerFrame.place(x=10, y=10)

label = tb.Label(headerFrame, text="QuietScan", font=("Helvetica", 42))
label.pack(side=tb.LEFT)

# nav
navFrame = tb.Frame(root, width=700, height=50)
navFrame.place(x=20, y=75)
sep = tb.Separator(navFrame, orient="vertical")
sep2 = tb.Separator(navFrame, orient="vertical")
homeButton = customtkinter.CTkButton(navFrame, text="Scan", command=lambda: raise_frame(scanFrame, homeButton),
                                     width=20)
homeButton.pack(side=tb.LEFT)
sep.pack(side=tb.LEFT, padx=20)
aboutButton = customtkinter.CTkButton(navFrame, text="About", command=lambda: raise_frame(aboutFrame, aboutButton),
                                      width=20)
aboutButton.pack(side=tb.LEFT)
sep2.pack(side=tb.LEFT, padx=20)
historyButton = customtkinter.CTkButton(navFrame, text="Scan History",
                                        command=lambda: raise_frame(historyFrame, historyButton), width=20)
historyButton.pack(side=tb.LEFT)

scanFrame = tb.Frame(root, width=1400, height=500)
aboutFrame = tb.Frame(root, width=1400, height=500)
historyFrame = tb.Frame(root, width=1400, height=500)

frames = (scanFrame, aboutFrame, historyFrame)

for frame in frames:
    frame.place(x=20, y=150)

# scan frame - initiate scan and scan checklist boxes from wireframe
scanButton = customtkinter.CTkButton(scanFrame, text="Start a new System Scan",
                                     command=lambda: scan_button_use(scan_output_box), width=50)
scanButton.grid(row=0, column=0, columnspan=2, sticky=tb.W + tb.E)

scan_output_box = tb.ScrolledText(scanFrame, height=30, width=150, state=tb.DISABLED)
scan_output_box.grid(row=1, column=0, columnspan=2, sticky=tb.W + tb.E)

space = tb.Frame(scanFrame, width=20)
space.grid(row=1, column=2)

scan_checklist = tb.LabelFrame(scanFrame, height=450, text="Scan Checklist")
scan_checklist.grid(row=1, column=3, sticky=tb.W + tb.E + tb.N + tb.S)

step1 = tb.IntVar()
scan_step1 = tb.Checkbutton(scan_checklist, padding=10, width=40, text="Collect running applications", variable=step1)
scan_step1.grid(row=0)

# about frame - display information about the vulnerability scanner
about_text_widget = tb.Label(aboutFrame, width=250, text=about_text)
about_text_widget.place(relx=0, rely=0)

# history frame - display scan history
history_text_widget = tb.ScrolledText(historyFrame, height=27, width=135, wrap=tk.WORD, font=("Helvetica", 12))
history_text_widget.insert(tk.END, display_scan_history())
history_text_widget.config(state=tb.DISABLED)
history_text_widget.pack()

# start in home panel
raise_frame(scanFrame, homeButton)

root.mainloop()
