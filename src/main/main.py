from os import system
import subprocess
import ttkbootstrap as tb
from ttkbootstrap.constants import *


scan = 'wmic product get name,version'
output_file = 'programs.txt'
def systemScan():
# run the command and save the output to a text file
    with open(output_file, 'w') as file:
        result = subprocess.run(scan, stdout=file, stderr=subprocess.PIPE, text=True, shell=True)

    if result.returncode == 0:
        print(f"Installed programs list saved to {output_file}")
    else:
        print("Error:", result.stderr)

#Somewhere in this file we need to add the functionality for our front end UI

#We also need to add the functionality for the the systemScan function to be called when the user clicks the button



def insert_scan_here():  # TODO replace with system scan function when ready (remove #)
    # scan
    print("Executing system scan")


def button_fill():  # TODO implement screen change functionality as screens are made
    print("Navigation Occurring")


# initialize ui
root = tb.Window(themename="superhero")
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

# add commands
homeButton = tb.Button(navFrame, class_="homeButton", text="Home", command=button_fill, width=20)
homeButton.pack(side=tb.LEFT)

aboutButton = tb.Button(navFrame, class_="aboutButton", text="About", command=button_fill, width=20)
aboutButton.pack(side=tb.LEFT)

historyButton = tb.Button(navFrame, class_="historyButton", text="Scan History", command=button_fill, width=20)
historyButton.pack(side=tb.LEFT)

# body frame - initiate scan and scan checklist boxes from wireframe  # TODO implement and position these boxes
bodyFrame = tb.Frame(root, width=300, height=150)
bodyFrame.place(x=10, y=150)

scanButton = tb.Button(bodyFrame, text="Scan", command=insert_scan_here, width=25)
scanButton.place(x=0, y=100)

root.mainloop()
