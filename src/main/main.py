from os import system
import subprocess
import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk
from ttkbootstrap.constants import *

from about import about_text
from src.main.scan import system_scan


def scan_button_use(textbox):
    textbox.config(state=tb.NORMAL)
    textbox.insert(tb.END, "Executing system scan" + '\n')
    system_scan(textbox)
    textbox.config(state=tb.DISABLED)

def show_about_dialog():
    about_dialog = tk.Toplevel(root)
    about_dialog.title("About")
    about_dialog.geometry("1200x720")
    about_label = tk.Label(about_dialog, text=about_text, wraplength=500, justify="left", font=("Helvetica", 18))
    about_label.pack()

def button_fill():  # TODO implement screen change functionality as screens are made
    print("Navigation Occurring")


root = tk.Tk()
root.title("QuietScan")
root.geometry('1280x720')

# header frame
headerFrame = tb.Frame(root, width=1200, height=150)
headerFrame.place(x=10, y=10)

label = tb.Label(headerFrame, text="QuietScan", font=("Helvetica", 42))
label.pack(side=tb.LEFT)

# nav
navFrame = tb.Frame(root, width=700, height=50)
navFrame.place(x=10, y=100)

sep = tb.Separator  # TODO implement this seperator between buttons

homeButton = tb.Button(navFrame, class_="homeButton", text="Home", command=lambda: button_fill(), width=20)
homeButton.pack(side=tb.LEFT)

aboutButton = ttk.Button(navFrame, text="About", command=show_about_dialog, width=20)
aboutButton.pack(side=tk.LEFT)

historyButton = tb.Button(navFrame, class_="historyButton", text="Scan History", command=lambda: button_fill(),
                          width=20)
historyButton.pack(side=tb.LEFT)

# body frame - initiate scan and scan checklist boxes from wireframe  # TODO implement and position these boxes
bodyFrame = tb.Frame(root, width=300, height=150)
bodyFrame.place(x=10, y=150)

scanButton = tb.Button(bodyFrame, text="Start a new System Scan", command=lambda: scan_button_use(scan_output_box),
                       width=50)
scanButton.pack()

scan_output_box = tb.ScrolledText(bodyFrame, pady=5, padx=5, height=30, width=150, state=tb.DISABLED)
scan_output_box.pack()

root.mainloop()
