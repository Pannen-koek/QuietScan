import subprocess

# define the command to list installed programs using wmic
scan = 'wmic product get name,version'

output_file = 'programs.txt'

# run the command and save the output to a text file
with open(output_file, 'w') as file:
    result = subprocess.run(scan, stdout=file, stderr=subprocess.PIPE, text=True, shell=True)

if result.returncode == 0:
    print(f"Installed programs list saved to {output_file}")
else:
    print("Error:", result.stderr)