import subprocess
import requests
import ttkbootstrap as tb
import os
import datetime


# Save scan result into a .txt file
def save_scan_result_to_file(output):
    # Create a directory named "scan_history" if it doesn't exist
    if not os.path.exists("scan_history"):
        os.makedirs("scan_history")

    # Generate a unique filename based on the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d  %H.%M.%S")
    filename = f"{timestamp} -- System Scan.txt"

    # Write the scan result to the file
    with open(os.path.join("scan_history", filename), "w") as file:
        file.write(output)


# Function to search for CVEs for a given application and version
def search_cve(application_name, version):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    cpe = f"cpe:2.3:a:{application_name}:{version}"

    params = {
        'resultsPerPage': '10',  # adjust as needed
        'cpeMatchString': cpe
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


def system_scan(textbox): # TODO implement threading
    # Define the command to list installed programs using wmic
    scan = 'wmic product get name,version'

    # Run the command
    result = subprocess.run(scan, capture_output=True, text=True, shell=True)

    if result.returncode == 0:
        output = result.stdout
        # Process each line of the output
        for line in output.splitlines():
            textbox.insert(tb.END, f"{line}" + '\n')
        save_scan_result_to_file(output)
        
            # parts = line.strip().split()
            # if len(parts) >= 2:
            # app_name = parts[0]
            # app_version = parts[1]
            # cve_results = search_cve(app_name, app_version)
            # textbox.insert(tb.END, f"{app_name} {app_version}" + '\n')
    # else:
    # textbox.insert(tb.END, "Error:", result.stderr + '\n')
