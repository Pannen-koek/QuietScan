from os import system
import subprocess


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